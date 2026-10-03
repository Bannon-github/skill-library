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

Language ladder (2026-10-03): manual English > auto English spoken in the
original audio > YouTube-translated track (tlang=en) > English auto track of an
AI-dub audio track > original-language track + translate_transcript.py.
Translated routes keep transcript.orig.<lang>.txt and mark meta.translated.
429 / IP blocks: exponential backoff; optional YT_TRANSCRIPT_PROXY / YTDLP_COOKIES
set by Matt. No ASR/Whisper unless Matt asks (flagged as last_resort only).
Never invent spoken words.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import re
import time
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/workspace/skill-library")
RAW = ROOT / "raw"
YTDLP = ROOT / ".venv/bin/yt-dlp"
PY = ROOT / ".venv/bin/python3"


def ytdlp_cmd() -> list[str]:
    """yt-dlp + a JS runtime for YouTube's player challenges (node if installed).

    Without one yt-dlp warns 'No supported JavaScript runtime' and some
    extraction paths are skipped.
    """
    import shutil
    rt = os.environ.get("YTDLP_JS_RUNTIME") or ("node" if shutil.which("node") else None)
    return [str(YTDLP)] + (["--js-runtimes", rt] if rt else [])


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


# --------------------------------------------------------------------------
# Track discovery + language ladder (2026-10-03)
# --------------------------------------------------------------------------
BLOCK_ERRORS = ("RequestBlocked", "IpBlocked", "TooManyRequests")
TERMINAL_ERRORS = {
    "VideoUnavailable": "video_unavailable",
    "VideoUnplayable": "video_unplayable",
    "AgeRestricted": "age_restricted",
    "InvalidVideoId": "invalid_video_id",
    "TranscriptsDisabled": "transcripts_disabled",
    "NoTranscriptFound": "no_transcript_found",
    "PoTokenRequired": "po_token_required",
}


def _classify_error(e: Exception) -> str:
    name = type(e).__name__
    if name in TERMINAL_ERRORS:
        return TERMINAL_ERRORS[name]
    msg = str(e)
    if name in BLOCK_ERRORS or "429" in msg or "Too Many Requests" in msg:
        return "rate_limited_or_ip_blocked"
    return f"error:{name}"


def _api():
    """YouTubeTranscriptApi, optionally through a user-configured proxy.

    YT_TRANSCRIPT_PROXY=http://user:pass@host:port (set by Matt, never by an agent
    from scraped creds) routes transcript requests around cloud-IP blocks.
    """
    from youtube_transcript_api import YouTubeTranscriptApi
    proxy = os.environ.get("YT_TRANSCRIPT_PROXY")
    if proxy:
        from youtube_transcript_api.proxies import GenericProxyConfig
        return YouTubeTranscriptApi(proxy_config=GenericProxyConfig(http_url=proxy, https_url=proxy))
    return YouTubeTranscriptApi()


def _with_backoff(fn, *, tries: int = 4, base: float = 4.0, log: list | None = None):
    """Retry only on 429 / IP-block; terminal errors raise immediately."""
    last = None
    for i in range(tries):
        try:
            return fn()
        except Exception as e:  # noqa: BLE001
            kind = _classify_error(e)
            last = e
            if kind != "rate_limited_or_ip_blocked" or i == tries - 1:
                raise
            wait = base * (2 ** i) + random.uniform(0, 2)
            if log is not None:
                log.append({"retry": i + 1, "reason": kind, "sleep_s": round(wait, 1)})
            time.sleep(wait)
    raise last  # pragma: no cover


def probe_ytdlp_meta(video_id: str) -> dict:
    """Cheap yt-dlp metadata probe: availability + original spoken language.

    yt-dlp exposes `language` and auto tracks named '<lang>-orig' for the
    original audio. That tells real speech apart from YouTube auto-dub tracks.
    """
    out: dict = {"ok": False}
    if not YTDLP.exists():
        out["error"] = "yt-dlp_missing"
        return out
    cmd = ytdlp_cmd() + ["-J", "--skip-download", "--no-warnings",
           f"https://www.youtube.com/watch?v={video_id}"]
    cookies = os.environ.get("YTDLP_COOKIES")
    if cookies and Path(cookies).exists():
        cmd += ["--cookies", cookies]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    except subprocess.TimeoutExpired:
        out["error"] = "timeout"
        return out
    if proc.returncode != 0:
        err = (proc.stderr or "")[-400:]
        out["error"] = ("rate_limited_or_ip_blocked" if ("429" in err or "Sign in to confirm" in err)
                        else "video_unavailable" if ("unavailable" in err.lower() or "removed" in err.lower() or "private" in err.lower())
                        else "ytdlp_error")
        out["stderr_tail"] = err
        return out
    info = json.loads(proc.stdout)
    auto = info.get("automatic_captions") or {}
    subs = info.get("subtitles") or {}
    orig = [k[:-5] for k in auto if k.endswith("-orig")]
    out.update({
        "ok": True,
        "title": info.get("title"),
        "channel": info.get("channel"),
        "duration": info.get("duration"),
        "view_count": info.get("view_count"),
        "upload_date": info.get("upload_date"),
        "language": info.get("language"),
        "orig_auto_langs": orig,
        "manual_sub_langs": sorted(k for k in subs if k != "live_chat"),
        "live_status": info.get("live_status"),
    })
    out["original_language"] = (info.get("language") or (orig[0] if orig else None))
    return out


def list_tracks(video_id: str, log: list | None = None) -> dict:
    """All transcript tracks the Show-transcript panel could display."""
    api = _api()
    try:
        listing = _with_backoff(lambda: list(api.list(video_id)), log=log)
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": _classify_error(e), "detail": str(e).strip().splitlines()[0][:200] if str(e).strip() else ""}
    tracks = []
    for t in listing:
        tracks.append({
            "language_code": t.language_code,
            "language": t.language,
            "is_generated": bool(t.is_generated),
            "is_translatable": bool(t.is_translatable),
            "translation_languages": [x.language_code for x in (t.translation_languages or [])],
        })
    return {"ok": True, "tracks": tracks, "_listing": listing}


def _base(code: str | None) -> str:
    return (code or "").lower().split("-")[0]


def plan_track(tracks: list[dict], original_language: str | None, target: str = "en",
               allow_yt_translate: bool = True) -> list[dict]:
    """Ordered ladder of fetch options. First that fetches wins.

    1 manual-<target>
    2 auto-<target> spoken in original audio (not an auto-dub)
    3 youtube-translated: tlang=<target> from the original-language track (manual > auto)
    4 auto-<target> from an AI-dub audio track (orig != target)  [flagged dub-derived]
    5 original-language track -> machine translation (translate_transcript.py)
    """
    orig = _base(original_language)
    tgt = _base(target)
    # If yt-dlp gave no original language and several auto tracks exist, the
    # first-listed generated track is YouTube's original ASR in practice.
    gen = [t for t in tracks if t["is_generated"]]
    if not orig and len(gen) == 1:
        orig = _base(gen[0]["language_code"])
    plan: list[dict] = []
    for t in tracks:
        if _base(t["language_code"]) == tgt and not t["is_generated"]:
            plan.append({"rank": 1, "route": "manual-target", "track": t})
    for t in tracks:
        if _base(t["language_code"]) == tgt and t["is_generated"] and (not orig or orig == tgt):
            plan.append({"rank": 2, "route": "auto-target-original-audio", "track": t})
    orig_tracks = sorted(
        [t for t in tracks if orig and _base(t["language_code"]) == orig],
        key=lambda t: t["is_generated"])
    if not orig_tracks:  # unknown original: any non-target manual, then any generated
        orig_tracks = sorted([t for t in tracks if _base(t["language_code"]) != tgt],
                             key=lambda t: t["is_generated"])[:1]
    if allow_yt_translate:
        for t in orig_tracks:
            if (_base(t["language_code"]) != tgt and t["is_translatable"]
                    and any(_base(c) == tgt for c in t["translation_languages"])):
                plan.append({"rank": 3, "route": "youtube-translated", "track": t, "tlang": tgt})
    for t in tracks:
        if _base(t["language_code"]) == tgt and t["is_generated"] and orig and orig != tgt:
            plan.append({"rank": 4, "route": "auto-target-from-dub-track", "track": t})
    for t in orig_tracks:
        if _base(t["language_code"]) != tgt:
            plan.append({"rank": 5, "route": "original-plus-machine-translation", "track": t})
    seen, out = set(), []
    for p in sorted(plan, key=lambda p: p["rank"]):
        key = (p["route"], p["track"]["language_code"], p["track"]["is_generated"])
        if key not in seen:
            seen.add(key)
            out.append(p)
    return out


def _snips_to_cues(fetched) -> list[tuple[float, str]]:
    cues: list[tuple[float, str]] = []
    for snip in fetched:
        start = float(getattr(snip, "start", snip["start"] if isinstance(snip, dict) else 0))
        text = getattr(snip, "text", snip["text"] if isinstance(snip, dict) else str(snip))
        text = text.replace("\n", " ").strip()
        if text:
            cues.append((start, text))
    return cues


def fetch_planned(listing, option: dict, log: list | None = None) -> list[tuple[float, str]]:
    want = option["track"]
    obj = next(t for t in listing if t.language_code == want["language_code"]
               and bool(t.is_generated) == want["is_generated"])
    if option.get("tlang"):
        obj = obj.translate(option["tlang"])
    return _snips_to_cues(_with_backoff(obj.fetch, log=log))


def fetch_via_transcript_api(video_id: str) -> tuple[list[tuple[float, str]], dict] | None:
    """Back-compat: English-preferring fetch (manual en > auto en > first track)."""
    res = list_tracks(video_id)
    if not res.get("ok"):
        return None
    plan = plan_track(res["tracks"], None, "en", allow_yt_translate=False)
    for opt in plan:
        if opt["route"] == "original-plus-machine-translation":
            continue
        try:
            cues = fetch_planned(res["_listing"], opt)
        except Exception:  # noqa: BLE001
            continue
        t = opt["track"]
        return cues, {
            "method": "youtube-transcript-api",
            "source_ui": "youtube-show-transcript",
            "language_code": t["language_code"],
            "is_generated": t["is_generated"],
            "transcript_kind": "auto-generated" if t["is_generated"] else "manual",
        }
    return None

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


def fetch_via_ytdlp(video_id: str, langs: str = "en.*,en") -> tuple[list[tuple[float, str]], dict] | None:
    """Fallback transport for the same timed track (yt-dlp), converted to panel text.

    `langs` may include '<orig>-orig' or YouTube auto-translated 'en' tracks.
    """
    if not YTDLP.exists():
        return None
    url = f"https://www.youtube.com/watch?v={video_id}"
    with tempfile.TemporaryDirectory() as td:
        outtmpl = str(Path(td) / "%(id)s")
        cmd = ytdlp_cmd() + ["--skip-download", "--write-auto-sub", "--write-sub",
               "--sub-langs", langs, "--sub-format", "vtt/srt/best",
               "--convert-subs", "srt", "--sleep-subtitles", "2", "-o", outtmpl, url]
        cookies = os.environ.get("YTDLP_COOKIES")
        if cookies and Path(cookies).exists():
            cmd += ["--cookies", cookies]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        srt_files = sorted(Path(td).glob("*.srt"))
        if not srt_files:
            return None

        def rank(p: Path) -> tuple:
            n = p.name.lower()
            return (0 if "-orig" in n else 1, 0 if n.endswith(".en.srt") else 1, len(n))

        srt_files.sort(key=rank)
        chosen = srt_files[0]
        cues = _parse_srt(chosen.read_text(errors="replace"))
        if not cues:
            return None
        lang = chosen.name.split(".")[-2] if chosen.name.count(".") >= 2 else None
        meta = {
            "method": "yt-dlp-timedtext-as-transcript",
            "source_ui": "youtube-show-transcript",
            "srt_file": chosen.name,
            "language_code": lang.replace("-orig", "") if lang else None,
            "ytdlp_exit": proc.returncode,
            "note": "Same timed transcript track as Show transcript; converted to panel text (not kept as caption deliverable).",
        }
        return cues, meta


def _translate(dest: Path, src_lang: str, target: str, backend: str) -> dict:
    """Run translate_transcript.py (own venv: .venv-translate) on the original panel."""
    script = Path(__file__).with_name("translate_transcript.py")
    py = ROOT / ".venv-translate/bin/python"
    if not py.exists():
        return {"ok": False, "error": "translate_venv_missing (run scripts/ensure_env.sh)"}
    proc = subprocess.run([str(py), str(script), str(dest / f"transcript.orig.{src_lang}.txt"),
                           "--src", src_lang, "--tgt", target, "--backend", backend, "--json"],
                          capture_output=True, text=True, timeout=3600)
    try:
        return json.loads(proc.stdout.strip().splitlines()[-1])
    except Exception:  # noqa: BLE001
        return {"ok": False, "error": "translate_failed", "stderr_tail": proc.stderr[-400:]}


def _write_outputs(dest: Path, cues, header: str | None = None) -> None:
    panel = cues_to_panel(cues)
    prose = cues_to_prose(cues)
    if header:
        panel = header + "\n" + panel
    (dest / "transcript.txt").write_text(panel)
    (dest / "raw.txt").write_text(prose)
    (dest / "raw").write_text(prose)


def save_transcript(video_id: str, title: str | None = None, target: str = "en",
                    allow_yt_translate: bool = True, allow_machine_translate: bool = True,
                    translate_backend: str = "argos", force_route: str | None = None,
                    probe: bool = True) -> dict:
    """Fetch the best Show-transcript text in `target` language via the ladder.

    Writes transcript.txt (target language, panel style), raw.txt (prose), and
    for translated routes also transcript.orig.<lang>.txt (original words).
    meta.json records route, translated flag, method, and every decision.
    """
    RAW.mkdir(parents=True, exist_ok=True)
    dest = RAW / video_id
    dest.mkdir(parents=True, exist_ok=True)
    decisions: list[dict] = []
    retries: list[dict] = []
    base_meta = {
        "video_id": video_id,
        "title": title,
        "url": f"https://www.youtube.com/watch?v={video_id}",
        "fetched_at": _now(),
        "source_ui": "youtube-show-transcript",
        "target_language": target,
    }
    ymeta = probe_ytdlp_meta(video_id) if probe else {"ok": False, "error": "probe_skipped"}
    if ymeta.get("ok"):
        base_meta["title"] = title or ymeta.get("title")
        base_meta["original_language"] = ymeta.get("original_language")
        base_meta["channel"] = ymeta.get("channel")
        base_meta["duration"] = ymeta.get("duration")
    decisions.append({"q": "yt-dlp probe ok? (availability + original language)",
                      "a": ymeta.get("ok"), "evidence": ymeta.get("error") or ymeta.get("original_language")})

    res = list_tracks(video_id, log=retries)
    decisions.append({"q": "transcript tracks listed?", "a": res.get("ok"),
                      "evidence": res.get("error") or [
                          f"{t['language_code']}{'(auto)' if t['is_generated'] else ''}" for t in res["tracks"]]})

    def fail(err: str, **extra) -> dict:
        meta = {**base_meta, "ok": False, "error": err, "decisions": decisions, "retries": retries, **extra}
        if err in ("transcripts_disabled", "no_transcript_found", "no_track_fetchable"):
            meta["last_resort"] = ("ASR/Whisper on the audio is possible but NOT allowed unless Matt "
                                   "explicitly asks; flagged for review, nothing invented.")
        (dest / "meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
        return meta

    chosen = None
    cues = None
    if res.get("ok"):
        plan = plan_track(res["tracks"], base_meta.get("original_language"), target, allow_yt_translate)
        if force_route:
            plan = [p for p in plan if p["route"] == force_route]
        decisions.append({"q": "track ladder", "a": [f"{p['rank']}:{p['route']}:{p['track']['language_code']}" for p in plan]})
        for opt in plan:
            if opt["route"] == "original-plus-machine-translation" and not allow_machine_translate:
                continue
            try:
                cues = fetch_planned(res["_listing"], opt, log=retries)
                chosen = opt
                decisions.append({"q": f"fetch {opt['route']} ({opt['track']['language_code']})", "a": True})
                break
            except Exception as e:  # noqa: BLE001
                decisions.append({"q": f"fetch {opt['route']} ({opt['track']['language_code']})",
                                  "a": False, "evidence": _classify_error(e)})
                continue
    else:
        err = res.get("error", "")
        if err in ("video_unavailable", "video_unplayable", "invalid_video_id", "age_restricted"):
            return fail(err, detail=res.get("detail"))

    method_meta: dict
    if chosen is None:
        # yt-dlp transport fallback (same timed tracks); try target, then original
        orig = _base(base_meta.get("original_language")) or ""
        langs = f"{target}.*,{target}" + (f",{orig}-orig,{orig}" if orig and orig != _base(target) else ",.*-orig")
        yd = fetch_via_ytdlp(video_id, langs)
        decisions.append({"q": f"yt-dlp fallback ({langs})", "a": yd is not None})
        if yd is None:
            return fail(res.get("error") or "no_track_fetchable")
        cues, method_meta = yd
        lang = method_meta.get("language_code") or ""
        if _base(lang) == _base(target):
            chosen = {"route": "ytdlp-target", "track": {"language_code": lang, "is_generated": None}}
        else:
            chosen = {"route": "original-plus-machine-translation",
                      "track": {"language_code": lang, "is_generated": None}}
    else:
        t = chosen["track"]
        method_meta = {
            "method": "youtube-transcript-api",
            "language_code": t["language_code"],
            "is_generated": t["is_generated"],
            "transcript_kind": "auto-generated" if t["is_generated"] else "manual",
        }

    route = chosen["route"]
    meta = {**base_meta, "ok": True, "cue_count": len(cues), "route": route, **method_meta,
            "transcript_path": str(dest / "transcript.txt"), "prose_path": str(dest / "raw.txt")}
    if route == "youtube-translated":
        meta.update({"translated": True, "translation_method": "youtube-tlang",
                     "translated_from": chosen["track"]["language_code"], "tlang": chosen["tlang"]})
        _write_outputs(dest, cues, header=f"# YouTube-translated transcript ({chosen['track']['language_code']} -> {target}, tlang). Original words: transcript.orig.{_base(chosen['track']['language_code'])}.txt when fetched.")
        # keep the original words too (cheap, same listing)
        try:
            orig_opt = {"track": chosen["track"]}
            ocues = fetch_planned(res["_listing"], orig_opt, log=retries)
            ob = _base(chosen["track"]["language_code"])
            (dest / f"transcript.orig.{ob}.txt").write_text(cues_to_panel(ocues))
            meta["original_transcript_path"] = str(dest / f"transcript.orig.{ob}.txt")
        except Exception as e:  # noqa: BLE001
            decisions.append({"q": "keep original-language words", "a": False, "evidence": _classify_error(e)})
    elif route == "original-plus-machine-translation":
        ob = _base(chosen["track"]["language_code"])
        (dest / f"transcript.orig.{ob}.txt").write_text(cues_to_panel(cues))
        meta["original_transcript_path"] = str(dest / f"transcript.orig.{ob}.txt")
        tr = _translate(dest, ob, target, translate_backend)
        decisions.append({"q": f"machine-translate {ob}->{target} ({translate_backend})", "a": tr.get("ok"),
                          "evidence": tr.get("error")})
        if not tr.get("ok"):
            return fail("translation_failed", translate=tr, original_transcript_path=meta["original_transcript_path"])
        meta.update({"translated": True, "translation_method": f"machine:{translate_backend}",
                     "translated_from": ob, "translation": tr})
        # translate_transcript.py wrote transcript.txt/raw.txt in target language
    else:
        meta["translated"] = False
        if route == "auto-target-from-dub-track":
            meta["dub_derived"] = True
            meta["note"] = "English auto track of a YouTube AI-dub audio track (speech already machine-translated)."
        _write_outputs(dest, cues)
    meta["decisions"] = decisions
    meta["retries"] = retries
    (dest / "meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
    for p in list(dest.glob("*.srt")) + list(dest.glob("*.vtt")):
        p.unlink(missing_ok=True)
    return meta


def main() -> int:
    ap = argparse.ArgumentParser(description="Fetch YouTube Show-transcript text (language-aware ladder)")
    ap.add_argument("video_ids", nargs="+", help="YouTube video id(s)")
    ap.add_argument("--title", default=None, help="Optional title (single id)")
    ap.add_argument("--target", default="en", help="Target language (default en)")
    ap.add_argument("--list-tracks", action="store_true", help="Only list tracks + planned ladder")
    ap.add_argument("--no-yt-translate", action="store_true", help="Skip YouTube tlang translated track")
    ap.add_argument("--no-machine-translate", action="store_true", help="Never run translate_transcript.py")
    ap.add_argument("--backend", default="argos", help="Machine-translation backend (argos|libretranslate|none)")
    ap.add_argument("--force-route", default=None, help="Only try this ladder route (testing)")
    ap.add_argument("--no-probe", action="store_true", help="Skip yt-dlp metadata probe")
    args = ap.parse_args()
    code = 0
    for vid in args.video_ids:
        if args.list_tracks:
            y = {} if args.no_probe else probe_ytdlp_meta(vid)
            r = list_tracks(vid)
            r.pop("_listing", None)
            if r.get("ok"):
                r["plan"] = [{k: v for k, v in p.items() if k != "track"} | {"lang": p["track"]["language_code"]}
                             for p in plan_track(r["tracks"], y.get("original_language"), args.target, not args.no_yt_translate)]
            r["original_language"] = y.get("original_language")
            print(json.dumps({"video_id": vid, **r}, indent=2, ensure_ascii=False))
            continue
        title = args.title if len(args.video_ids) == 1 else None
        meta = save_transcript(vid, title=title, target=args.target,
                               allow_yt_translate=not args.no_yt_translate,
                               allow_machine_translate=not args.no_machine_translate,
                               translate_backend=args.backend, force_route=args.force_route,
                               probe=not args.no_probe)
        print(json.dumps({k: v for k, v in meta.items() if k not in ("decisions",)}, indent=2, ensure_ascii=False))
        if not meta.get("ok"):
            code = 1
    return code


if __name__ == "__main__":
    raise SystemExit(main())

