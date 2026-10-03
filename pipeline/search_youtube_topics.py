#!/usr/bin/env python3
"""Search YouTube for how-to videos on a topic, filtered and ranked for distilling.

Builds on skills/youtube-howto-search.md (stage 1). Uses yt-dlp search (no API key),
then optional per-video checks.

Filters / signals:
  --min-dur/--max-dur   seconds (default 180..3600; drops Shorts and 3h streams)
  --within              hour|today|week|month|year  (YouTube upload-date filter via sp=)
  --min-views           minimum view count
  --langs               comma list of query languages; topic is searched as given plus
                        how-to keyword variants per language (en,de,es,ja,fr,pt)
  --precheck            list transcript tracks per result (youtube-transcript-api);
                        records has_transcript, manual/auto, original language guess,
                        and whether a YouTube-translated English track is offered
  --require-transcript  drop results without any transcript track (needs --precheck)
  --skip-known          drop ids already in raw/ or LIBRARY.json
How-to score: title/channel signals (how to, tutorial, step by step, explained,
from scratch, anleitung, cómo, tutorial completo, 作り方, 使い方, 音作り ...) minus
negatives (reaction, unboxing, #shorts, live stream, preset pack, sample pack, review).

Writes pipeline/searches/<date>-<slug>.json and prints a ranked list.

Usage:
  .venv/bin/python pipeline/search_youtube_topics.py "cinematic pad sound design" \
      --langs en,de --within year --precheck --require-transcript --top 8
"""
from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
import sys
import time
from datetime import date
from pathlib import Path

ROOT = Path("/workspace/skill-library")
YTDLP = ROOT / ".venv/bin/yt-dlp"
OUT = ROOT / "pipeline" / "searches"
SP = {"hour": "EgIIAQ%3D%3D", "today": "EgIIAg%3D%3D", "week": "EgIIAw%3D%3D",
      "month": "EgIIBA%3D%3D", "year": "EgIIBQ%3D%3D"}
HOWTO_KW = {
    "en": "tutorial how to",
    "de": "tutorial anleitung deutsch",
    "es": "tutorial cómo español",
    "ja": "使い方 作り方 解説",
    "fr": "tutoriel comment",
    "pt": "tutorial como fazer",
}
POS = re.compile(r"how to|tutorial|step[- ]by[- ]step|explained|from scratch|walkthrough|guide|beginner|"
                 r"tips|in \d+ minutes|anleitung|erklärt|cómo|como |tutoriel|作り方|使い方|解説|音作り|入門|講座", re.I)
NEG = re.compile(r"#shorts|reaction|unboxing|live ?stream|preset pack|sample pack|free download|"
                 r"giveaway|review\b|vs\.? |trailer|music video|official video|full album|1 hour|"
                 r"no talking|asmr", re.I)


def _yt() -> list[str]:
    import shutil
    return [str(YTDLP)] + (["--js-runtimes", "node"] if shutil.which("node") else [])


def run_search(query: str, n: int, within: str | None) -> list[dict]:
    if within:
        url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}&sp={SP[within]}"
        cmd = _yt() + ["--flat-playlist", "-J", "--playlist-end", str(n), url]
    else:
        cmd = _yt() + ["--flat-playlist", "-J", f"ytsearch{n}:{query}"]
    for attempt in range(3):
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if p.returncode == 0:
            break
        if "429" in p.stderr:
            time.sleep(5 * (attempt + 1))
            continue
        print(f"search failed: {p.stderr[-300:]}", file=sys.stderr)
        return []
    data = json.loads(p.stdout or "{}")
    rows = []
    for e in data.get("entries") or []:
        if not e or not e.get("id") or e.get("ie_key") not in (None, "Youtube"):
            continue
        rows.append({"id": e["id"], "title": e.get("title") or "", "channel": e.get("channel") or e.get("uploader"),
                     "duration": e.get("duration"), "view_count": e.get("view_count"),
                     "url": f"https://www.youtube.com/watch?v={e['id']}", "query": query})
    return rows


def howto_score(r: dict, topic: str) -> float:
    t = r["title"]
    s = 0.0
    s += 2.0 * len(POS.findall(t))
    s -= 4.0 * len(NEG.findall(t))
    words = [w for w in re.findall(r"\w+", topic.lower()) if len(w) > 2]
    s += 1.0 * sum(1 for w in words if w in t.lower())
    d = r.get("duration") or 0
    if 300 <= d <= 1800:
        s += 1.5  # sweet spot for a distillable procedure
    v = r.get("view_count") or 0
    s += min(3.0, math.log10(v + 1) / 2)
    return round(s, 2)


def precheck(vid: str) -> dict:
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import fetch_youtube_transcript as f  # noqa: E402
        res = f.list_tracks(vid)
    except Exception as e:  # noqa: BLE001
        return {"has_transcript": None, "error": f"{type(e).__name__}"}
    if not res.get("ok"):
        return {"has_transcript": False if res.get("error") in ("transcripts_disabled", "no_transcript_found") else None,
                "error": res.get("error")}
    tr = res["tracks"]
    gen = [t for t in tr if t["is_generated"]]
    return {
        "has_transcript": bool(tr),
        "manual_langs": [t["language_code"] for t in tr if not t["is_generated"]],
        "auto_langs": [t["language_code"] for t in gen][:6],
        "auto_dub_suspected": len(gen) > 3,
        "english_direct": any(t["language_code"].startswith("en") for t in tr),
        "yt_translate_to_en": any("en" in t["translation_languages"] for t in tr),
    }


def known_ids() -> set[str]:
    ids = {p.name for p in (ROOT / "raw").iterdir() if p.is_dir()} if (ROOT / "raw").exists() else set()
    lib = ROOT / "LIBRARY.json"
    if lib.exists():
        ids |= set(re.findall(r'"video_id":\s*"([\w-]{11})"', lib.read_text()))
    return ids


def main() -> int:
    ap = argparse.ArgumentParser(description="Filtered YouTube how-to topic search")
    ap.add_argument("topic")
    ap.add_argument("--langs", default="en")
    ap.add_argument("--per-query", type=int, default=15)
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--min-dur", type=int, default=180)
    ap.add_argument("--max-dur", type=int, default=3600)
    ap.add_argument("--min-views", type=int, default=0)
    ap.add_argument("--within", choices=sorted(SP))
    ap.add_argument("--precheck", action="store_true")
    ap.add_argument("--require-transcript", action="store_true")
    ap.add_argument("--skip-known", action="store_true")
    ap.add_argument("--no-save", action="store_true")
    a = ap.parse_args()
    seen, rows = set(), []
    for lang in [x.strip() for x in a.langs.split(",") if x.strip()]:
        q = f"{a.topic} {HOWTO_KW.get(lang, '')}".strip()
        for r in run_search(q, a.per_query, a.within):
            if r["id"] in seen:
                continue
            seen.add(r["id"])
            r["query_lang"] = lang
            rows.append(r)
    kept = []
    known = known_ids() if a.skip_known else set()
    drop_log = []
    for r in rows:
        d = r.get("duration") or 0
        why = None
        if d and (d < a.min_dur or d > a.max_dur):
            why = f"duration {d}s"
        elif (r.get("view_count") or 0) < a.min_views:
            why = "views"
        elif NEG.search(r["title"]):
            why = "negative title signal"
        elif r["id"] in known:
            why = "already known"
        if why:
            drop_log.append({"id": r["id"], "why": why})
            continue
        r["howto_score"] = howto_score(r, a.topic)
        kept.append(r)
    kept.sort(key=lambda r: -r["howto_score"])
    kept = kept[: max(a.top * 2, a.top)]
    if a.precheck:
        for r in kept:
            r["transcript"] = precheck(r["id"])
            time.sleep(0.5)
        if a.require_transcript:
            for r in [r for r in kept if not r["transcript"].get("has_transcript")]:
                drop_log.append({"id": r["id"], "why": f"no transcript ({r['transcript'].get('error')})"})
            kept = [r for r in kept if r["transcript"].get("has_transcript")]
    kept = kept[: a.top]
    out = {"topic": a.topic, "date": date.today().isoformat(), "params": vars(a), "results": kept,
           "dropped": drop_log, "note": "Show-transcript availability only; nothing fetched yet."}
    if not a.no_save:
        OUT.mkdir(parents=True, exist_ok=True)
        path = OUT / f"{date.today().isoformat()}-{re.sub(r'[^a-z0-9]+', '-', a.topic.lower()).strip('-')[:50]}.json"
        path.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
        out["saved_to"] = str(path)
    for r in kept:
        tr = r.get("transcript", {})
        flag = "" if not tr else (" [T:" + ("manual " + ",".join(tr.get("manual_langs", [])) if tr.get("manual_langs") else "auto " + ",".join(tr.get("auto_langs", [])[:2])) + ("; yt->en" if tr.get("yt_translate_to_en") else "") + "]" if tr.get("has_transcript") else " [no transcript]")
        print(f"{r['howto_score']:5.1f}  {r['id']}  {r.get('duration') or '?':>5}s  {r['title'][:70]}{flag}")
    print(json.dumps({"saved_to": out.get("saved_to"), "kept": len(kept), "dropped": len(drop_log)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
