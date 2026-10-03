#!/usr/bin/env python3
"""Fetch YouTube *Show transcript* text for a video (not caption-file framing).

Source of truth for Matt's distillery: the transcript you open from the video
info section (⋯ / description → Show transcript). That panel is backed by
YouTube's timed transcript track. We save:
  raw/<id>/transcript.txt  — panel-style lines (mm:ss + text)
  raw/<id>/raw.txt         — continuous prose for distill
  raw/<id>/raw             — same prose
  raw/<id>/meta.json       — provenance

Primary: youtube-transcript-api (same endpoint family as Show transcript).
Fallback: yt-dlp timed text → converted into transcript panel format.
Never invent spoken words.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/workspace/skill-library")
RAW = ROOT / "raw"
YTDLP = ROOT / ".venv/bin/yt-dlp"
PY = ROOT / ".venv/bin/python3"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _fmt_ts(sec: float) -> str:
    sec = max(0, int(sec))
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def cues_to_panel(cues: list[tuple[float, str]]) -> str:
    """Show-transcript style: timestamp + one line per spoken segment (deduped).

    Auto tracks often roll overlapping phrases; collapse like reading the panel
    for meaning, keeping the start time of each new segment.
    """
    rows: list[tuple[float, str]] = []
    for t, text in cues:
        line = re.sub(r"\s+", " ", text).strip()
        if not line:
            continue
        if rows:
            prev_t, prev = rows[-1]
            if line == prev:
                continue
            if line.startswith(prev) and len(line) > len(prev):
                rows[-1] = (prev_t, line)
                continue
            if prev.endswith(line) or line in prev:
                continue
            prev_words = prev.split()
            line_words = line.split()
            max_k = min(len(prev_words), len(line_words), 12)
            overlap = 0
            for k in range(max_k, 0, -1):
                if prev_words[-k:] == line_words[:k]:
                    overlap = k
                    break
            if overlap:
                rows[-1] = (prev_t, prev + " " + " ".join(line_words[overlap:]))
                continue
        rows.append((t, line))
    out: list[str] = []
    for t, text in rows:
        out.append(_fmt_ts(t))
        out.append(text)
    return "\n".join(out) + ("\n" if out else "")


def cues_to_prose(cues: list[tuple[float, str]]) -> str:
    """Merge rolling ASR overlaps into readable prose (like reading the panel)."""
    cleaned: list[str] = []
    for _, text in cues:
        line = re.sub(r"\s+", " ", text).strip()
        if not line:
            continue
        if cleaned:
            prev = cleaned[-1]
            if line == prev:
                continue
            if line.startswith(prev) and len(line) > len(prev):
                cleaned[-1] = line
                continue
            if prev.endswith(line) or line in prev:
                continue
            prev_words = prev.split()
            line_words = line.split()
            max_k = min(len(prev_words), len(line_words), 12)
            overlap = 0
            for k in range(max_k, 0, -1):
                if prev_words[-k:] == line_words[:k]:
                    overlap = k
                    break
            if overlap:
                cleaned[-1] = prev + " " + " ".join(line_words[overlap:])
                continue
        cleaned.append(line)
    return "\n\n".join(cleaned).strip() + ("\n" if cleaned else "")


def fetch_via_transcript_api(video_id: str) -> tuple[list[tuple[float, str]], dict] | None:
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        return None
    api = YouTubeTranscriptApi()
    try:
        listing = list(api.list(video_id))
    except Exception as e:
        return None
    # Prefer manually created English, then generated English
    chosen = None
    for prefer_generated in (False, True):
        for t in listing:
            code = (t.language_code or "").lower()
            if not code.startswith("en"):
                continue
            if t.is_generated == prefer_generated:
                chosen = t
                break
        if chosen:
            break
    if not chosen and listing:
        chosen = listing[0]
    if not chosen:
        return None
    try:
        fetched = chosen.fetch()
    except Exception:
        try:
            fetched = api.fetch(video_id, languages=["en", "en-US", "en-GB"])
        except Exception:
            return None
    cues: list[tuple[float, str]] = []
    for snip in fetched:
        # API 1.x: FetchedTranscriptSnippet with .start .text
        start = float(getattr(snip, "start", snip["start"] if isinstance(snip, dict) else 0))
        text = getattr(snip, "text", snip["text"] if isinstance(snip, dict) else str(snip))
        text = text.replace("\n", " ").strip()
        if text:
            cues.append((start, text))
    meta = {
        "method": "youtube-transcript-api",
        "source_ui": "youtube-show-transcript",
        "language_code": getattr(chosen, "language_code", None),
        "is_generated": getattr(chosen, "is_generated", None),
        "transcript_kind": "auto-generated" if getattr(chosen, "is_generated", False) else "manual",
    }
    return cues, meta


def _parse_srt(text: str) -> list[tuple[float, str]]:
    cues: list[tuple[float, str]] = []
    for block in re.split(r"\n\s*\n", text.strip()):
        parts = block.strip().splitlines()
        if not parts:
            continue
        tline = None
        content: list[str] = []
        for p in parts:
            if re.match(r"^\d+$", p.strip()):
                continue
            m = re.match(r"^(\d{2}):(\d{2}):(\d{2})[,.](\d{3})\s*-->", p.strip())
            if m:
                h, mi, s, ms = map(int, m.groups())
                tline = h * 3600 + mi * 60 + s + ms / 1000.0
                continue
            content.append(p.strip())
        if tline is not None and content:
            cues.append((tline, " ".join(content)))
    return cues


def fetch_via_ytdlp(video_id: str) -> tuple[list[tuple[float, str]], dict] | None:
    if not YTDLP.exists():
        return None
    url = f"https://www.youtube.com/watch?v={video_id}"
    with tempfile.TemporaryDirectory() as td:
        outtmpl = str(Path(td) / "%(id)s")
        cmd = [
            str(YTDLP),
            "--skip-download",
            "--write-auto-sub",
            "--write-sub",
            "--sub-langs",
            "en.*,en",
            "--sub-format",
            "vtt/srt/best",
            "--convert-subs",
            "srt",
            "-o",
            outtmpl,
            url,
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        srt_files = sorted(Path(td).glob("*.srt"))
        if not srt_files:
            return None
        # Prefer en-orig / non-auto-looking names first
        def rank(p: Path) -> tuple:
            n = p.name.lower()
            return (
                0 if "en-orig" in n else 1,
                0 if n.endswith(".en.srt") else 1,
                len(n),
            )

        srt_files.sort(key=rank)
        chosen = srt_files[0]
        cues = _parse_srt(chosen.read_text(errors="replace"))
        if not cues:
            return None
        meta = {
            "method": "yt-dlp-timedtext-as-transcript",
            "source_ui": "youtube-show-transcript",
            "srt_file": chosen.name,
            "ytdlp_exit": proc.returncode,
            "note": "Same timed transcript track as Show transcript; converted to panel text (not kept as caption deliverable).",
        }
        return cues, meta


def save_transcript(video_id: str, title: str | None = None) -> dict:
    RAW.mkdir(parents=True, exist_ok=True)
    dest = RAW / video_id
    dest.mkdir(parents=True, exist_ok=True)

    result = fetch_via_transcript_api(video_id)
    if result is None:
        result = fetch_via_ytdlp(video_id)
    if result is None:
        meta = {
            "video_id": video_id,
            "title": title,
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "ok": False,
            "error": "transcript_unavailable",
            "fetched_at": _now(),
            "source_ui": "youtube-show-transcript",
        }
        (dest / "meta.json").write_text(json.dumps(meta, indent=2) + "\n")
        return meta

    cues, method_meta = result
    panel = cues_to_panel(cues)
    prose = cues_to_prose(cues)
    (dest / "transcript.txt").write_text(panel)
    (dest / "raw.txt").write_text(prose)
    (dest / "raw").write_text(prose)
    meta = {
        "video_id": video_id,
        "title": title,
        "url": f"https://www.youtube.com/watch?v={video_id}",
        "ok": True,
        "fetched_at": _now(),
        "cue_count": len(cues),
        "transcript_path": str(dest / "transcript.txt"),
        "prose_path": str(dest / "raw.txt"),
        **method_meta,
    }
    (dest / "meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    # Remove caption-file artifacts if present — transcript is the deliverable
    for p in dest.glob("*.srt"):
        p.unlink(missing_ok=True)
    for p in dest.glob("*.vtt"):
        p.unlink(missing_ok=True)
    return meta


def main() -> int:
    ap = argparse.ArgumentParser(description="Fetch YouTube Show-transcript text")
    ap.add_argument("video_ids", nargs="+", help="YouTube video id(s)")
    ap.add_argument("--title", default=None, help="Optional title (single id)")
    args = ap.parse_args()
    code = 0
    for i, vid in enumerate(args.video_ids):
        title = args.title if len(args.video_ids) == 1 else None
        meta = save_transcript(vid, title=title)
        print(json.dumps(meta, indent=2))
        if not meta.get("ok"):
            code = 1
    return code


if __name__ == "__main__":
    raise SystemExit(main())
