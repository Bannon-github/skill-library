#!/usr/bin/env python3
"""Weekly YouTube skills intake (search-term gated).

Commands (run from /workspace/skill-library with .venv/bin/python):
  check                      Stage 0 only. Prints STATUS READY or NEEDS_TERMS.
  set-terms T1 [T2 ...]      Fill EMPTY slots in priority order (1..5), then re-check.
                             --replace: clear all 5 slots first, then fill from slot 1.
  clear-terms                Empty all 5 slots.
  migrate                    Seed intake/history.json from LIBRARY.json, batches/, raw/, titles.json.
  run [--dry-run]            Stage 0 -> search slot 1 verbatim -> queue (<=10) -> per-item checks
                             -> transcript -> processing (pipeline/route.py) -> history.
                             --dry-run: search + history/title checks only, no transcript fetch.
Slot values: "" = empty/never answered (-> NEEDS_TERMS); null = declined/couldn't update (counts as filled).
  set-terms [T ...] --decline   fill empties with given terms, then mark remaining empties null.
Search uses the first non-null slot verbatim. All 5 null -> NO_TERMS.
Exit codes: 0 ok, 2 NEEDS_TERMS, 3 NO_TERMS, 1 error.
Data (intake/): search_terms.json, config.json, queue.json, history.json, runs/<ts>.json
"""
import argparse, glob, json, os, re, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "intake"
TERMS, CFG, QUEUE, HIST, RUNS = D / "search_terms.json", D / "config.json", D / "queue.json", D / "history.json", D / "runs"
PY = str(ROOT / ".venv/bin/python")
YTDLP = str(ROOT / ".venv/bin/yt-dlp")
DEFAULT_CFG = {
    "queue_max": 10,
    "title_match": {
        "min_shared_terms": 3,
        "min_overlap_ratio": 0.6,
        "compare_against": ["history", "library"],
        "ignore_words": ["how", "to", "the", "a", "an", "and", "or", "of", "in", "on", "for", "with", "your", "you",
                         "my", "is", "it", "this", "that", "from", "by", "at", "into", "vs", "tutorial", "tutorials",
                         "guide", "beginner", "beginners", "complete", "easy", "best", "minutes", "minute", "step",
                         "part", "full", "learn", "make", "use", "using", "2024", "2025", "2026", "new", "ultimate",
                         "quick", "simple", "tips", "basics", "like", "pro", "do"]},
    "route_args": ["--langs", "en"],
}


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load(p, default):
    return json.loads(p.read_text()) if p.exists() else default


def save(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(obj, indent=1, ensure_ascii=False) + "\n")
    tmp.replace(p)


def cfg():
    c = load(CFG, None)
    if c is None:
        save(CFG, DEFAULT_CFG); c = DEFAULT_CFG
    return c


def terms():
    t = load(TERMS, None)
    if t is None:
        t = {"slots": [{"priority": i, "term": ""} for i in range(1, 6)], "updated_at": None}
        save(TERMS, t)
    return t


def check(emit=True):
    t = terms()
    # "" = never answered (ask Matt); None/null = declined or couldn't update (counts as filled)
    empty = [s["priority"] for s in t["slots"] if s.get("term") is not None and not str(s["term"]).strip()]
    active = [s for s in t["slots"] if s.get("term") is not None and str(s["term"]).strip()]
    status = "NEEDS_TERMS" if empty else ("NO_TERMS" if not active else "READY")
    res = {"status": status, "empty_slots": empty,
           "null_slots": [s["priority"] for s in t["slots"] if s.get("term") is None],
           "search_slot": active[0]["priority"] if active and not empty else None,
           "search_term": active[0]["term"] if active and not empty else None,
           "slots": {s["priority"]: s["term"] for s in t["slots"]}}
    if emit:
        print("STATUS " + res["status"] + (f" empty_slots={empty}" if empty else ""))
        print(json.dumps(res, indent=1))
    return res


# ---------- history ----------
def hist():
    return load(HIST, {"videos": {}})


def blocks(entry):
    """True if a history entry means 'already considered' (rate-limited ones stay retryable)."""
    return entry is not None and not entry.get("retryable")


def log_hist(h, vid, title, status, reason, **extra):
    prev = h["videos"].get(vid, {})
    e = {"video_id": vid, "title": title or prev.get("title", ""), "status": status, "reason": reason,
         "retryable": status == "rate_limited", "attempts": prev.get("attempts", 0) + (1 if status != "skipped_duplicate" else 0),
         "first_seen": prev.get("first_seen", now()), "updated_at": now()}
    e.update(extra)
    h["videos"][vid] = e
    save(HIST, h)


def migrate():
    h = hist(); added = 0
    def add(vid, title, src):
        nonlocal added
        if not vid or not re.fullmatch(r"[\w-]{11}", vid):
            return
        e = h["videos"].get(vid)
        if e:
            if title and not e.get("title"): e["title"] = title
            return
        h["videos"][vid] = {"video_id": vid, "title": title or "", "status": "migrated", "reason": f"pre-existing ({src})",
                            "retryable": False, "attempts": 0, "first_seen": now(), "updated_at": now()}
        added += 1
    lib = load(ROOT / "LIBRARY.json", {})
    for e in lib.get("entries", []):
        add(e.get("video_id"), e.get("title"), "LIBRARY.json")
    for f in sorted(glob.glob(str(ROOT / "batches/*.json"))):
        try: b = json.load(open(f))
        except Exception: continue
        def walk(o):
            if isinstance(o, dict):
                if isinstance(o.get("video_id"), str): add(o["video_id"], o.get("title"), "batches/" + Path(f).name)
                for v in o.values(): walk(v)
            elif isinstance(o, list):
                for v in o: walk(v)
        walk(b)
    for m in glob.glob(str(ROOT / "raw/*/meta.json")):
        try: mj = json.load(open(m))
        except Exception: continue
        add(mj.get("video_id") or Path(m).parent.name, mj.get("title"), "raw/")
    for d in glob.glob(str(ROOT / "raw/*")):
        add(Path(d).name, "", "raw/")
    for vid, t in load(ROOT / "titles.json", {}).items():
        add(vid, t, "titles.json")
    save(HIST, h)
    print(json.dumps({"migrated_added": added, "history_total": len(h["videos"])}))


# ---------- title rule ----------
def toks(title, ignore):
    words = re.findall(r"[a-z0-9]+", (title or "").lower())
    return {w[:-1] if len(w) > 3 and w.endswith("s") and not w.endswith("ss") else w
            for w in words if w not in ignore and len(w) > 1}


def title_match(title, vid, h, c):
    tm = c["title_match"]; ign = set(tm["ignore_words"])
    cand = toks(title, ign)
    if not cand:
        return None
    pool = []
    if "history" in tm["compare_against"]:
        pool += [(v, e.get("title")) for v, e in h["videos"].items() if v != vid and e.get("title")]
    if "library" in tm["compare_against"]:
        pool += [(e.get("video_id"), e.get("title")) for e in load(ROOT / "LIBRARY.json", {}).get("entries", []) if e.get("title")]
    best = None
    for ov, ot in pool:
        if ov == vid: continue
        shared = cand & toks(ot, ign)
        ratio = len(shared) / len(cand)
        if len(shared) >= tm["min_shared_terms"] and ratio >= tm["min_overlap_ratio"]:
            if not best or ratio > best["ratio"]:
                best = {"against_video": ov, "against_title": ot, "shared": sorted(shared), "ratio": round(ratio, 2)}
    return best


# ---------- search / process ----------
def search(term, n):
    r = subprocess.run([YTDLP, "--flat-playlist", "-J", f"ytsearch{n}:{term}"], capture_output=True, text=True, timeout=180)
    if r.returncode != 0:
        raise RuntimeError("search failed: " + r.stderr[-400:])
    out = []
    for e in (json.loads(r.stdout).get("entries") or []):
        vid = e.get("id")
        if vid and len(out) < n and vid not in [o["video_id"] for o in out] and "/shorts/" not in (e.get("url") or ""):
            out.append({"video_id": vid, "url": f"https://www.youtube.com/watch?v={vid}", "title": e.get("title") or "",
                        "channel": e.get("channel") or e.get("uploader"), "duration": e.get("duration")})
    return out


def process(vid, c):
    """Existing processing step: pipeline/route.py (transcript ladder -> usability -> term graph -> gap check)."""
    r = subprocess.run([PY, str(ROOT / "pipeline/route.py"), vid] + c.get("route_args", []), capture_output=True, text=True, cwd=ROOT, timeout=1800)
    rj = load(ROOT / "raw" / vid / "route.json", {})
    return rj.get("outcome") or f"ERROR_rc{r.returncode}", rj, r


def classify(outcome):
    if outcome.startswith("DEFER"): return "rate_limited", "transcript fetch rate-limited/IP-blocked; retry later"
    if outcome.startswith("STOP_no_transcript") or outcome.startswith("STOP_"): return "no_transcript", outcome
    if outcome == "REJECT_thin_transcript": return "no_transcript", "transcript unusable (<150 words or music-only)"
    if outcome == "CANDIDATES_READY": return "processed", "transcript sent to processing; gap candidates ready for distill-transcript"
    if outcome in ("COVERED", "OFF_LEXICON"): return "processed", f"transcript sent to processing; {outcome}"
    return "error", outcome


def run(dry):
    c = cfg()
    st = check(emit=False)
    if st["status"] != "READY":
        print("STATUS " + st["status"] + (" empty_slots=" + str(st["empty_slots"]) if st["empty_slots"] else ""))
        print(json.dumps(st, indent=1)); return 2 if st["status"] == "NEEDS_TERMS" else 3
    term = st["search_term"]
    report = {"started_at": now(), "search_term": term, "dry_run": dry, "items": []}
    q = load(QUEUE, {"items": []})
    if q.get("items"):
        report["resumed_queue_from"] = q.get("search_term")
        print(f"Resuming {len(q['items'])} leftover queue items")
    else:
        found = search(term, int(c["queue_max"]))
        q = {"search_term": term, "filled_at": now(), "items": found[: int(c["queue_max"])]}
        save(QUEUE, q)
        print(f"Queue filled with {len(q['items'])} items for search term (verbatim): {term!r}")
    h = hist()
    while q["items"]:
        it = q["items"][0]; vid, title = it["video_id"], it["title"]
        rec = {"video_id": vid, "title": title}
        prev = h["videos"].get(vid)
        tm = None if blocks(prev) else title_match(title, vid, h, c)
        if blocks(prev):
            rec.update(result="skipped_duplicate", reason=f"already considered ({prev.get('status')})")
            prev["last_skipped_at"] = now(); save(HIST, h)
        elif tm:
            rec.update(result="skipped_title_match", reason=tm)
            log_hist(h, vid, title, "skipped_title_match", f"title shares {tm['shared']} ({tm['ratio']}) with {tm['against_video']}", match=tm, search_term=term)
        elif dry:
            rec.update(result="would_fetch_transcript")
        else:
            outcome, rj, _ = process(vid, c)
            status, reason = classify(outcome)
            rec.update(result=status, outcome=outcome, reason=reason)
            log_hist(h, vid, title, status, reason, outcome=outcome, search_term=term,
                     needs_distill=(outcome == "CANDIDATES_READY"), url=it["url"], channel=it.get("channel"))
        print(f"  {vid} | {title[:60]!r} -> {rec['result']}")
        report["items"].append(rec)
        q["items"].pop(0); save(QUEUE, q)
    report["finished_at"] = now()
    report["needs_distill"] = [r["video_id"] for r in report["items"] if r.get("outcome") == "CANDIDATES_READY"]
    if not dry:
        save(RUNS / (datetime.now().strftime("%Y-%m-%dT%H%M%S") + ".json"), report)
    print("STATUS DONE"); print(json.dumps({k: report[k] for k in ("search_term", "needs_distill")} |
          {"counts": {s: sum(r["result"] == s for r in report["items"]) for s in {r["result"] for r in report["items"]}}}, indent=1))
    return 0


def main():
    ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("check"); s = sp.add_parser("set-terms"); s.add_argument("terms", nargs="*"); s.add_argument("--decline", action="store_true", help="after filling, mark remaining empty slots null"); s.add_argument("--replace", action="store_true")
    sp.add_parser("clear-terms"); sp.add_parser("migrate"); r = sp.add_parser("run"); r.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(); cfg()
    if a.cmd == "check":
        return {"READY": 0, "NEEDS_TERMS": 2}.get(check()["status"], 3)
    if a.cmd in ("set-terms", "clear-terms"):
        t = terms()
        if a.cmd == "clear-terms" or a.replace:
            for s_ in t["slots"]: s_["term"] = ""
        new = [x.strip() for x in getattr(a, "terms", []) if x.strip()]
        for s_ in t["slots"]:
            if new and s_["term"] is not None and not s_["term"].strip(): s_["term"] = new.pop(0)
        if getattr(a, "decline", False):
            for s_ in t["slots"]:
                if s_["term"] is not None and not s_["term"].strip(): s_["term"] = None
        if new: print(f"WARNING: no empty slot left for {new}; use --replace to rewrite the list")
        t["updated_at"] = now(); save(TERMS, t)
        st = check()["status"]; return {"READY": 0, "NEEDS_TERMS": 2}.get(st, 3)
    if a.cmd == "migrate": migrate(); return 0
    if a.cmd == "run": return run(a.dry_run)


if __name__ == "__main__":
    sys.exit(main())
