#!/usr/bin/env python3
"""Fetch YouTube-provided captions for Blender shortlist stage 2."""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path("/workspace/skill-library")
YTDLP = str(ROOT / ".venv/bin/yt-dlp")
RAW = ROOT / "raw"
SEARCH = ROOT / "pipeline/searches/2026-09-23-blender-howto.json"

VIDEOS = [
    {
        "video_id": "peSv5IT5Ve4",
        "title": "ABSOLUTE Beginner Basics.. Blender For Noobs 2025",
        "prefer_manual": False,
        "manual_langs": [],
        "auto_langs": ["en", "en-orig"],
    },
    {
        "video_id": "z-Xl9tGqH14",
        "title": "Beginner Blender Tutorial (2026)",
        "prefer_manual": False,
        "manual_langs": [],
        "auto_langs": ["en", "en-orig"],
    },
    {
        "video_id": "Ci3Has4L5W4",
        "title": "Blender Tutorial for Beginners",
        "prefer_manual": True,
        "manual_langs": ["en"],
        "auto_langs": ["en", "en-orig"],
    },
    {
        "video_id": "x60zHw_z4NM",
        "title": "Blender Tutorial – How to Use AI to Create 3D Models (ChatGPT and Blender)",
        "prefer_manual": True,
        "manual_langs": ["en", "en-ehkg1hFWq8A"],
        "auto_langs": ["en", "en-orig"],
    },
    {
        "video_id": "smluafHtCeY",
        "title": "Learning BLENDER as a GAME DEV",
        "prefer_manual": True,
        "manual_langs": ["en-CA", "en"],
        "auto_langs": ["en", "en-orig", "en-CA"],
    },
    {
        "video_id": "TG_vamse41c",
        "title": "Watch This Before you Get Started with Blender (7 Tips)",
        "prefer_manual": True,
        "manual_langs": ["en", "en-ehkg1hFWq8A"],
        "auto_langs": ["en", "en-orig"],
    },
    {
        "video_id": "8_0RptMbhe0",
        "title": "How to 3D Model Using Blender - Easy Beginner Guide + Tips and Tricks",
        "prefer_manual": False,
        "manual_langs": [],
        "auto_langs": ["en", "en-orig"],
    },
    {
        "video_id": "nESaz92SJ0w",
        "title": "The World's Easiest Blender Tutorial for Beginners",
        "prefer_manual": False,
        "manual_langs": [],
        "auto_langs": ["en", "en-orig"],
    },
    {
        "video_id": "Use9T2IX1XE",
        "title": "Blender Low Poly Character Modeling Tutorial - Part 1",
        "prefer_manual": False,
        "manual_langs": [],
        "auto_langs": ["en", "en-orig"],
    },
    {
        "video_id": "98qKfdJRzr0",
        "title": "Blender Beginner Tutorial - Part 1",
        "prefer_manual": False,
        "manual_langs": [],
        "auto_langs": ["en", "en-orig"],
    },
    {
        "video_id": "uOmYInaX-wE",
        "title": "Getting started - Blender for complete beginners",
        "prefer_manual": True,
        "manual_langs": ["en"],
        "auto_langs": ["en", "en-orig"],
    },
]


def srt_to_plain(text: str) -> str:
    """Convert SRT to plain transcript; dedupe overlapping auto-caption lines."""
    lines = []
    for block in re.split(r"\n\s*\n", text.strip()):
        parts = block.strip().splitlines()
        if not parts:
            continue
        # drop index and timestamp lines
        content = []
        for p in parts:
            if re.match(r"^\d+$", p.strip()):
                continue
            if re.match(r"^\d{2}:\d{2}:\d{2}[,.]\d{3}\s*-->", p.strip()):
                continue
            content.append(p.strip())
        if content:
            lines.append(" ".join(content))

    # Dedupe: auto-captions often repeat rolling windows
    cleaned = []
    for line in lines:
        line = re.sub(r"\s+", " ", line).strip()
        if not line:
            continue
        if cleaned:
            prev = cleaned[-1]
            # skip if identical or fully contained as continuation echo
            if line == prev:
                continue
            if line.startswith(prev) and len(line) > len(prev):
                cleaned[-1] = line
                continue
            if prev.endswith(line) or line in prev:
                continue
            # merge partial overlap: last words of prev == first words of line
            prev_words = prev.split()
            line_words = line.split()
            max_k = min(len(prev_words), len(line_words))
            overlap = 0
            for k in range(max_k, 0, -1):
                if prev_words[-k:] == line_words[:k]:
                    overlap = k
                    break
            if overlap:
                merged = prev_words + line_words[overlap:]
                cleaned[-1] = " ".join(merged)
                continue
        cleaned.append(line)

    # join into readable paragraphs (~80-100 chars soft wrap not required)
    return "\n".join(cleaned).strip() + "\n"


def vtt_to_plain(text: str) -> str:
    # strip WEBVTT header and cues similarly
    text = re.sub(r"^WEBVTT.*?\n\n", "", text, flags=re.S)
    # remove NOTE blocks
    text = re.sub(r"^NOTE.*?(?:\n\n|\Z)", "", text, flags=re.M | re.S)
    lines = []
    for block in re.split(r"\n\s*\n", text.strip()):
        parts = block.strip().splitlines()
        content = []
        for p in parts:
            if re.match(r"^\d{2}:\d{2}:\d{2}\.\d{3}\s*-->", p.strip()):
                continue
            if p.strip().startswith("NOTE"):
                continue
            # strip simple tags
            p = re.sub(r"<[^>]+>", "", p)
            content.append(p.strip())
        if content:
            lines.append(" ".join(c for c in content if c))
    # reuse srt dedupe by faking srt join
    fake = "\n\n".join(f"{i}\n00:00:00,000 --> 00:00:01,000\n{l}" for i, l in enumerate(lines, 1))
    return srt_to_plain(fake)


def run_ytdlp(url: str, outdir: Path, langs: list[str], auto: bool) -> tuple[Path | None, str | None]:
    lang_arg = ",".join(langs)
    cmd = [
        YTDLP,
        "--skip-download",
        "--sub-langs",
        lang_arg,
        "--convert-subs",
        "srt",
        "-o",
        str(outdir / "%(id)s.%(ext)s"),
    ]
    if auto:
        cmd.append("--write-auto-sub")
    else:
        cmd.append("--write-sub")
    cmd.append(url)
    proc = subprocess.run(cmd, capture_output=True, text=True)
    # find downloaded srt/vtt
    candidates = list(outdir.glob("*.srt")) + list(outdir.glob("*.vtt"))
    if not candidates:
        return None, proc.stderr[-500:] if proc.stderr else proc.stdout[-500:]
    # prefer matching lang files
    return candidates[0], None


def fetch_one(v: dict) -> dict:
    vid = v["video_id"]
    url = f"https://www.youtube.com/watch?v={vid}"
    out_dir = RAW / vid
    out_dir.mkdir(parents=True, exist_ok=True)
    source = None
    plain = None
    err = None

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        if v["prefer_manual"] and v["manual_langs"]:
            path, err = run_ytdlp(url, td, v["manual_langs"], auto=False)
            if path:
                text = path.read_text(encoding="utf-8", errors="replace")
                plain = srt_to_plain(text) if path.suffix == ".srt" else vtt_to_plain(text)
                # detect which lang from filename
                name = path.name
                source = "youtube-manual-en"
                if "en-CA" in name:
                    source = "youtube-manual-en-CA"
                elif "ehkg" in name:
                    source = "youtube-manual-en"
        if plain is None or len(plain.strip()) < 40:
            # clear and try auto
            for f in td.glob("*"):
                f.unlink()
            path, err = run_ytdlp(url, td, v["auto_langs"] or ["en"], auto=True)
            if path:
                text = path.read_text(encoding="utf-8", errors="replace")
                plain = srt_to_plain(text) if path.suffix == ".srt" else vtt_to_plain(text)
                source = "youtube-auto-en"
            else:
                return {"video_id": vid, "ok": False, "error": err or "no subtitles"}

    if not plain or len(plain.strip()) < 40:
        return {"video_id": vid, "ok": False, "error": "transcript too short / empty"}

    raw_txt = out_dir / "raw.txt"
    raw_alias = out_dir / "raw"
    raw_txt.write_text(plain, encoding="utf-8")
    if raw_alias.exists() or raw_alias.is_symlink():
        raw_alias.unlink()
    # match existing style: duplicate file named `raw` (not necessarily symlink)
    shutil.copy2(raw_txt, raw_alias)

    meta = {
        "video_id": vid,
        "url": url,
        "title": v["title"],
        "source": source,
        "raw_path": str(raw_txt),
        "raw_alias": str(raw_alias),
    }
    (out_dir / "meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    return {
        "video_id": vid,
        "ok": True,
        "source": source,
        "chars": len(plain),
        "lines": plain.count("\n") + 1,
    }


def main():
    results = []
    for v in VIDEOS:
        print(f"Fetching {v['video_id']} ...", flush=True)
        r = fetch_one(v)
        results.append(r)
        print(json.dumps(r), flush=True)

    report_path = ROOT / "pipeline/searches/2026-09-23-blender-howto-fetch-results.json"
    report_path.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")

    # update search JSON note
    data = json.loads(SEARCH.read_text())
    ok = [r for r in results if r.get("ok")]
    fail = [r for r in results if not r.get("ok")]
    data["stage"] = 2
    data["note"] = (
        "Stage 2 complete for available videos (transcript_status==available). "
        f"Fetched {len(ok)}/{len(results)} raw transcripts. "
        "Skipped W337AL7n3dc (missing). "
        + (
            "Failures: " + ", ".join(f"{r['video_id']} ({r.get('error','?')[:80]})" for r in fail)
            if fail
            else "No fetch failures."
        )
    )
    data["stage2_fetch"] = {
        "fetched": [r["video_id"] for r in ok],
        "failures": fail,
        "skipped_missing": ["W337AL7n3dc"],
    }
    SEARCH.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print("DONE", len(ok), "ok", len(fail), "fail")


if __name__ == "__main__":
    main()
