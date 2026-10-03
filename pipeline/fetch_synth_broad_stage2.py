#!/usr/bin/env python3
"""Fetch YouTube-provided captions for broad cinematic-synth shortlist."""
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

# Prioritized for cinematic/ambient pads, unison, WT morph, FM, FX mixing.
# Cap later at 12-16 distilled skills; fetch a slightly wider set then skip thin.
VIDEOS = [
    {"video_id": "XvPgfdf9MSk", "title": "How To MAKE Lush Cinematic PAD Sound in Serum 2 (BIGGEST Ambient Sound EVER)"},
    {"video_id": "oW4C7txJEgM", "title": "Beautiful Pads with Serum 2"},
    {"video_id": "CcXGRCXv8lQ", "title": "Serum Tutorial - Warm 'Analog' Cinematic Pad Synth"},
    {"video_id": "AYVmdcgKt_s", "title": "This One Technique Changes EVERYTHING // Vital Pad Sound Design Tutorial"},
    {"video_id": "EUlrANFXLs4", "title": "How to Make Pads in Vital // FREE Sound Design"},
    {"video_id": "ehKoz6ILmxQ", "title": "Making Dreamy & Organic Pads | Vital Sound Design Tutorial"},
    {"video_id": "KnbAOrM62Ks", "title": "5 Power Tips for Better Supersaws in Serum"},
    {"video_id": "am6KBGUVtXE", "title": "Odd vs Even Unison in Serum | The Secret to Wide & Focused Sounds"},
    {"video_id": "ImWJixBPZj0", "title": "Ambient Pads in Vital From Scratch"},
    {"video_id": "pQFr594QwI4", "title": "How to make LUSH ambient pads in Vital"},
    {"video_id": "e1ZQssAW7R0", "title": "Arturia Pigments: Creating A Digital Pad"},
    {"video_id": "CMkXW17LYyA", "title": "Phase Plant | Creating Lush Organic Pads"},
    {"video_id": "FZ9oXRJIR6o", "title": "Amazing pads with the new Granular Generator in Phase Plant"},
    {"video_id": "vvBl3YUBUyY", "title": "FM SYNTHS in under 4 minutes"},
    {"video_id": "UxGswh6XLto", "title": "Sound Design Theory: LFO & Envelope explained!"},
    {"video_id": "Z-yfQSWU0TA", "title": "UVI Falcon Texture / Pad Tutorial [Ambient // Cinematic // Sound Design]"},
    {"video_id": "cF5ku3Og0Nk", "title": "How to Make Super Warm, Heavenly Pads with Vital"},
    {"video_id": "6NXqV9jWJ1s", "title": "5 Tips for Mixing Pads and Synths for a Full, Clear Sound"},
    {"video_id": "TmoP3i6-jl0", "title": "HOW TO MAKE THE WEEKND CINEMATIC PAD | Serum 2 Sound Design Tutorial"},
    {"video_id": "rv0X7eZNnEo", "title": "Sound Design with VITAL - Wide BASS - Evolving PAD - Lead PLUCK"},
]


def srt_to_plain(text: str) -> str:
    lines = []
    for block in re.split(r"\n\s*\n", text.strip()):
        parts = block.strip().splitlines()
        if not parts:
            continue
        content = []
        for p in parts:
            if re.match(r"^\d+$", p.strip()):
                continue
            if re.match(r"^\d{2}:\d{2}:\d{2}[,.]\d{3}\s*-->", p.strip()):
                continue
            content.append(p.strip())
        if content:
            lines.append(" ".join(content))

    cleaned = []
    for line in lines:
        line = re.sub(r"\s+", " ", line).strip()
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
            max_k = min(len(prev_words), len(line_words))
            overlap = 0
            for k in range(max_k, 0, -1):
                if prev_words[-k:] == line_words[:k]:
                    overlap = k
                    break
            if overlap:
                cleaned[-1] = " ".join(prev_words + line_words[overlap:])
                continue
        cleaned.append(line)
    return "\n".join(cleaned).strip() + "\n"


def vtt_to_plain(text: str) -> str:
    text = re.sub(r"^WEBVTT.*?\n\n", "", text, flags=re.S)
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
            p = re.sub(r"<[^>]+>", "", p)
            content.append(p.strip())
        if content:
            lines.append(" ".join(c for c in content if c))
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
    candidates = list(outdir.glob("*.srt")) + list(outdir.glob("*.vtt"))
    if not candidates:
        return None, (proc.stderr or proc.stdout or "")[-800:]
    # Prefer en-orig then en
    preferred = sorted(
        candidates,
        key=lambda p: (
            0 if "en-orig" in p.name else 1 if re.search(r"\.en\.", p.name) else 2,
            len(p.name),
        ),
    )
    return preferred[0], None


def fetch_one(v: dict) -> dict:
    vid = v["video_id"]
    url = f"https://www.youtube.com/watch?v={vid}"
    out_dir = RAW / vid
    out_dir.mkdir(parents=True, exist_ok=True)

    # Skip if already have usable raw
    existing = out_dir / "raw.txt"
    if existing.exists() and existing.stat().st_size > 200:
        return {
            "video_id": vid,
            "ok": True,
            "source": "cached",
            "chars": existing.stat().st_size,
            "skipped_fetch": True,
        }

    plain = None
    source = None
    err = None

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        # Try manual first
        path, err = run_ytdlp(url, td, ["en", "en-orig"], auto=False)
        if path:
            text = path.read_text(encoding="utf-8", errors="replace")
            plain = srt_to_plain(text) if path.suffix == ".srt" else vtt_to_plain(text)
            source = "youtube-manual-en"
        if plain is None or len(plain.strip()) < 80:
            for f in td.glob("*"):
                f.unlink()
            path, err = run_ytdlp(url, td, ["en", "en-orig"], auto=True)
            if path:
                text = path.read_text(encoding="utf-8", errors="replace")
                plain = srt_to_plain(text) if path.suffix == ".srt" else vtt_to_plain(text)
                source = "youtube-auto-en"
                # keep a copy of srt/vtt for audit
                shutil.copy2(path, out_dir / path.name)
            else:
                return {"video_id": vid, "ok": False, "error": err or "no subtitles"}
        else:
            shutil.copy2(path, out_dir / path.name)

    if not plain or len(plain.strip()) < 80:
        return {"video_id": vid, "ok": False, "error": "transcript too short / empty"}

    raw_txt = out_dir / "raw.txt"
    raw_alias = out_dir / "raw"
    raw_txt.write_text(plain, encoding="utf-8")
    if raw_alias.exists() or raw_alias.is_symlink():
        raw_alias.unlink()
    shutil.copy2(raw_txt, raw_alias)

    meta = {
        "video_id": vid,
        "url": url,
        "title": v["title"],
        "source": source,
        "transcript": "youtube-provided",
        "raw_path": str(raw_txt),
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

    report = ROOT / "pipeline/searches/2026-09-24-broad-synth-fetch-results.json"
    report.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    ok = [r for r in results if r.get("ok")]
    fail = [r for r in results if not r.get("ok")]
    print("DONE", len(ok), "ok", len(fail), "fail", flush=True)


if __name__ == "__main__":
    main()
