#!/usr/bin/env python3
"""Self-questioning router for the YouTube knowledge pipeline.

The agent asks itself explicit yes/no questions and picks the next skill/tool.
Every question, answer, evidence and chosen branch is logged:
  raw/<id>/route.json          (per video)
  pipeline/logs/route.jsonl    (append-only, all runs)

Decision tree (per video):
  Q-cool  Earlier video in this run got blocked?               yes -> DEFER without any request
  Q0  Pipeline env importable (youtube_transcript_api, yt_dlp)?   no -> scripts/ensure_env.sh
  Q1  Transcript already saved (raw/<id>/meta.json ok) and not --refetch?
                                                                yes -> reuse; skip to Q4
  Q2  Fetch via track ladder (fetch_youtube_transcript.save_transcript):
        manual EN > auto EN (original audio) > YouTube-translated tlang=en >
        EN auto of AI-dub track > original track + translate_transcript.py
      Q2a video unavailable/private/removed?                    -> STOP (drop from queue)
      Q2b 429 / IP-blocked after backoff?                       -> DEFER (pipeline/queue/deferred.json);
                                                                   hint: YT_TRANSCRIPT_PROXY / YTDLP_COOKIES
                                                                   set by Matt, or retry later
      Q2c no transcript track at all?                           -> STOP; flag ASR as last resort
                                                                   (only if Matt explicitly asks)
      Q2d machine translation failed / garbled?                 -> STOP; original kept; try other backend
  Q3  Transcript usable (>=150 words, not music/marker-only)?   no -> REJECT thin
  Q4  Translated (youtube-tlang or machine)?                    yes -> mark candidates translated_source;
                                                                   distill must cross-check original words
  Q4b Machine translation low-confidence?                     yes -> numbers/steps must be checked in original
  Q4c tlang rung skipped only due to 429?                       yes -> queue upgrade_to_tlang for a later --refetch
  Q5  Domain lexicon matched (>= 8 term hits)?                  no -> flag off-lexicon (extend lexicon /
                                                                   plain distill-transcript)
  Q6  Build term graph (extract_terms_graph.py)
  Q7  Gap check + KG merge (graph_gap_merge.py). Candidate outlines?
                                                                yes -> NEXT: distill-transcript on each span,
                                                                   then quality_check + novelty_check
                                                                no  -> covered; KG updated, no new skill

Usage:
  .venv/bin/python pipeline/route.py VIDEO_ID [VIDEO_ID ...] [--refetch] [--force-route R]
  .venv/bin/python pipeline/route.py --topic "cinematic pad sound design" --langs en,de --max 3
Options: --no-yt-translate, --no-machine-translate, --backend argos, --no-kg-update
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/workspace/skill-library")
HERE = Path(__file__).resolve().parent
RAW = ROOT / "raw"
LOGS = HERE / "logs"
QUEUE = HERE / "queue" / "deferred.json"
sys.path.insert(0, str(HERE))


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


class Log:
    def __init__(self, vid: str):
        self.vid = vid
        self.rows: list[dict] = []

    def ask(self, q: str, a, evidence=None, then: str | None = None):
        row = {"q": q, "a": a}
        if evidence is not None:
            row["evidence"] = evidence
        if then:
            row["then"] = then
        self.rows.append(row)
        mark = "yes" if a is True else "no" if a is False else str(a)
        print(f"  [{self.vid}] {q} -> {mark}" + (f"  => {then}" if then else ""), flush=True)
        return a


def env_ok() -> bool:
    try:
        import youtube_transcript_api  # noqa: F401
        import yt_dlp  # noqa: F401
        return True
    except ImportError:
        return False


def defer(vid: str, reason: str) -> None:
    QUEUE.parent.mkdir(parents=True, exist_ok=True)
    q = json.loads(QUEUE.read_text()) if QUEUE.exists() else {"deferred": []}
    q["deferred"] = [d for d in q["deferred"] if d["video_id"] != vid]
    q["deferred"].append({"video_id": vid, "reason": reason, "at": now()})
    QUEUE.write_text(json.dumps(q, indent=1) + "\n")


def run_json(cmd: list[str]) -> dict:
    p = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return json.loads(p.stdout.strip().splitlines()[-1])
    except Exception:  # noqa: BLE001
        return {"ok": False, "error": "subprocess_failed", "stderr_tail": p.stderr[-500:]}


COOLING = {"on": False}


def route_video(vid: str, a) -> dict:
    L = Log(vid)
    out = {"video_id": vid, "started_at": now(), "outcome": None}
    if COOLING["on"]:
        L.ask("Q-cool: did an earlier video in this run hit a 429/IP block?", True,
              then="DEFER without contacting YouTube (more requests extend the block)")
        defer(vid, "cooling_off_after_block")
        out["outcome"] = "DEFER_rate_limited"
        return finish(out, L)
    # Q0
    if not L.ask("Q0 pipeline env importable?", env_ok(), then=None if env_ok() else "run scripts/ensure_env.sh"):
        subprocess.run(["bash", str(ROOT / "scripts/ensure_env.sh")], check=False)
        if not env_ok():
            out["outcome"] = "STOP_env_broken"
            return finish(out, L)
    dest = RAW / vid
    meta_p = dest / "meta.json"
    meta = json.loads(meta_p.read_text()) if meta_p.exists() else {}
    have = bool(meta.get("ok")) and (dest / "transcript.txt").exists() and not a.refetch
    # Q1
    if not L.ask("Q1 transcript already saved?", have, evidence=meta.get("route"),
                 then="reuse saved transcript" if have else "fetch via track ladder"):
        import fetch_youtube_transcript as f
        meta = f.save_transcript(vid, target="en", allow_yt_translate=not a.no_yt_translate,
                                 allow_machine_translate=not a.no_machine_translate,
                                 translate_backend=a.backend, force_route=a.force_route)
        err = meta.get("error")
        L.ask("Q2 track ladder produced English text?", bool(meta.get("ok")),
              evidence=meta.get("route") or err)
        if not meta.get("ok"):
            if err in ("video_unavailable", "video_unplayable", "invalid_video_id", "age_restricted"):
                L.ask("Q2a video unavailable/private/removed/age-gated?", True, evidence=err, then="STOP, drop from queue")
                out["outcome"] = f"STOP_{err}"
            elif err == "rate_limited_or_ip_blocked":
                L.ask("Q2b rate-limited / IP-blocked after backoff?", True, evidence=meta.get("retries"),
                      then="DEFER to pipeline/queue/deferred.json; retry later or Matt sets YT_TRANSCRIPT_PROXY")
                defer(vid, err)
                COOLING["on"] = True
                if meta.get("kept_previous"):
                    L.ask("Q2b' earlier good transcript kept?", True, then="previous transcript/meta untouched")
                out["outcome"] = "DEFER_rate_limited"
            elif err == "translation_failed":
                L.ask("Q2d machine translation failed?", True, evidence=meta.get("translate"),
                      then="STOP; original words kept; try --backend libretranslate or another package")
                out["outcome"] = "STOP_translation_failed"
            else:
                L.ask("Q2c no transcript track at all?", True, evidence=err,
                      then="STOP; flag ASR/Whisper as last resort - only if Matt explicitly asks")
                out["outcome"] = "STOP_no_transcript_asr_flagged"
                out["asr_last_resort_flag"] = True
            return finish(out, L, meta)
    out["route"] = meta.get("route")
    out["language_code"] = meta.get("language_code")
    out["original_language"] = meta.get("original_language")
    out["is_generated"] = meta.get("is_generated")
    # Q3
    text = (dest / "raw.txt").read_text(errors="replace") if (dest / "raw.txt").exists() else ""
    words = len(text.split())
    music = text.lower().count("[music]")
    usable = words >= 150 and music < words / 20
    if not L.ask("Q3 transcript usable (>=150 words, not music-only)?", usable,
                 evidence={"words": words, "music_markers": music}, then=None if usable else "REJECT thin"):
        out["outcome"] = "REJECT_thin_transcript"
        return finish(out, L, meta)
    # Q4
    translated = bool(meta.get("translated"))
    L.ask("Q4 English text is a translation?", translated,
          evidence=meta.get("translation_method") or ("dub-derived" if meta.get("dub_derived") else "direct"),
          then="mark translated_source; distill cross-checks transcript.orig.*" if translated else None)
    out["translated"] = translated
    out["translation_method"] = meta.get("translation_method")
    if str(meta.get("translation_method", "")).startswith("machine"):
        tp = dest / "translation.json"
        tr = json.loads(tp.read_text()) if tp.exists() else (meta.get("translation") or {})
        low = tr.get("confidence") == "low"
        L.ask("Q4b machine translation low-confidence (ja/zh/ko source or >5% garbled)?", low,
              evidence={"confidence": tr.get("confidence"), "garbled_share": tr.get("garbled_share"),
                        "repeat_loops": tr.get("repeat_loops_collapsed")},
              then="graph terms OK as hints; numbers/steps must be verified in transcript.orig.*" if low else None)
        out["translation_confidence"] = tr.get("confidence")
        tl_blocked = any("youtube-translated" in str(d.get("q")) and d.get("evidence") == "rate_limited_or_ip_blocked"
                         for d in meta.get("decisions", []))
        if L.ask("Q4c was the YouTube-translated (tlang) rung skipped only because of a 429?", tl_blocked,
                 then="queue an upgrade: refetch later with --refetch to get YouTube's own English" if tl_blocked else None):
            QUEUE.parent.mkdir(parents=True, exist_ok=True)
            q = json.loads(QUEUE.read_text()) if QUEUE.exists() else {"deferred": []}
            ups = [u for u in q.get("upgrade_to_tlang", []) if u["video_id"] != vid]
            ups.append({"video_id": vid, "reason": "tlang 429; used machine translation", "at": now()})
            q["upgrade_to_tlang"] = ups
            QUEUE.write_text(json.dumps(q, indent=1) + "\n")
    # Q5 + Q6
    g = run_json([sys.executable, str(HERE / "extract_terms_graph.py"), vid] + (["--domain", a.domain] if a.domain else []))
    gj = json.loads((dest / "graph.json").read_text()) if (dest / "graph.json").exists() else {}
    best = max((gj.get("domain_scores") or {"?": 0}).values())
    on_lex = best >= 8
    L.ask("Q5 domain lexicon matched (>=8 hits)?", on_lex, evidence={"domain": gj.get("domain"), "scores": gj.get("domain_scores")},
          then=None if on_lex else "flag off-lexicon: extend pipeline/lexicons or plain distill-transcript")
    out["domain"] = gj.get("domain")
    out["graph"] = g
    L.ask("Q6 term graph built?", bool(gj), evidence={k: g.get(k) for k in ("nodes", "edges")})
    # Q7
    gp = run_json([sys.executable, str(HERE / "graph_gap_merge.py"), vid] + (["--no-kg-update"] if a.no_kg_update else [])
                  + (["--as-of", a.as_of] if a.as_of else []))
    out["gaps"] = gp
    # Q7: covered only on procedure/parameter-level overlap + novelty (graph_gap_merge.covered_verdict),
    # never on topic-term matches alone
    has_c = gp.get("decision", "GAP" if gp.get("candidates") else "COVERED") == "GAP"
    L.ask("Q7 gap vs library (procedure-level overlap < 0.5, uncovered technique, or NOVEL)?", has_c,
          evidence={k: gp.get(k) for k in ("gap_nodes_excl_phrases", "gap_edges", "candidates", "covered_verdict")},
          then=("NEXT: distill-transcript on each candidate span -> quality_check_skill.py -> novelty_check_skill.py"
                if has_c else "covered by library; KG updated; no new skill"))
    out["outcome"] = "CANDIDATES_READY" if has_c else ("COVERED" if on_lex else "OFF_LEXICON")
    return finish(out, L, meta)


def finish(out: dict, L: Log, meta: dict | None = None) -> dict:
    out["decisions"] = L.rows
    if not str(out.get("outcome")).startswith("DEFER") and QUEUE.exists():
        q = json.loads(QUEUE.read_text())
        q["deferred"] = [d for d in q["deferred"] if d["video_id"] != out["video_id"]]
        QUEUE.write_text(json.dumps(q, indent=1) + "\n")
    if meta and meta.get("decisions"):
        out["fetch_decisions"] = meta["decisions"]
    out["finished_at"] = now()
    d = RAW / out["video_id"]
    d.mkdir(parents=True, exist_ok=True)
    (d / "route.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    LOGS.mkdir(parents=True, exist_ok=True)
    with (LOGS / "route.jsonl").open("a") as fh:
        fh.write(json.dumps({k: v for k, v in out.items() if k not in ("fetch_decisions",)}, ensure_ascii=False) + "\n")
    print(f"  [{out['video_id']}] OUTCOME {out['outcome']}", flush=True)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="YouTube knowledge pipeline router")
    ap.add_argument("video_ids", nargs="*")
    ap.add_argument("--topic")
    ap.add_argument("--langs", default="en")
    ap.add_argument("--max", type=int, default=3)
    ap.add_argument("--within")
    ap.add_argument("--refetch", action="store_true")
    ap.add_argument("--force-route")
    ap.add_argument("--no-yt-translate", action="store_true")
    ap.add_argument("--no-machine-translate", action="store_true")
    ap.add_argument("--backend", default="argos")
    ap.add_argument("--domain")
    ap.add_argument("--no-kg-update", action="store_true")
    ap.add_argument("--as-of", help="replay the gap check against the library as it was before this date")
    a = ap.parse_args()
    ids = list(a.video_ids)
    if a.topic:
        print(f"Q-search: topic given -> search_youtube_topics.py ({a.topic!r}, langs={a.langs})")
        cmd = [sys.executable, str(HERE / "search_youtube_topics.py"), a.topic, "--langs", a.langs,
               "--precheck", "--require-transcript", "--skip-known", "--top", str(a.max)]
        if a.within:
            cmd += ["--within", a.within]
        res = run_json(cmd)
        if res.get("saved_to"):
            ids += [r["id"] for r in json.loads(Path(res["saved_to"]).read_text())["results"]][: a.max]
    if not ids:
        ap.error("give video ids or --topic")
    summary = [route_video(v, a) for v in ids]
    print(json.dumps([{k: s.get(k) for k in ("video_id", "outcome", "route", "translated", "domain")} for s in summary], indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
