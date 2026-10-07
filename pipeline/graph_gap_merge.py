#!/usr/bin/env python3
"""Check a video's term graph against the existing library; add gaps; outline skills.

Input : raw/<id>/graph.json (from extract_terms_graph.py)
Reads : mcp-publish/skills/*.json (our catalog), prior-art/index.json (public packs),
        knowledge/graph.json (accumulated knowledge graph)
Writes: raw/<id>/gaps.json                          (gap report, local)
        distilled/<id>/candidates/<cid>.outline.json (skill OUTLINES only; local)
        knowledge/graph.json                        (merged; evidence = {video_id, t} refs only,
                                                     no quote text, so it is safe for the public repo)

What counts as covered:
  node  (param/module/concept/tool): its canonical term is matched by the same lexicon
        inside some published skill's goal/steps/constraints/tags.
  edge  sets: skill text has the param AND the same value string ("24 db", "5 voices").
        affects: one skill STEP mentions both endpoints (source and target).
        part-of (lexicon): structural, never a gap.
Gap = uncovered by our skills. Each gap is also tagged:
  known_in_kg  - already seen in knowledge/graph.json from another video (repeat signal)
  prior_art    - a public pack mentions the term (generic; lower priority)

Candidate outlines: contiguous runs of transcript steps that touch >=2 gap items
and span >=3 steps. Each outline holds grounded step quotes + timestamps, gap
nodes/edges, nearest existing skills, and a novelty verdict (novelty_check_skill
logic). Outlines are NOT skills: they go to distill-transcript -> quality_check ->
novelty_check before anything is published.

Usage:
  python3 pipeline/graph_gap_merge.py <video_id> [--no-kg-update] [--min-steps 3]
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/workspace/skill-library")
HERE = Path(__file__).resolve().parent
RAW = ROOT / "raw"
SKILLS = ROOT / "mcp-publish" / "skills"
PRIOR = ROOT / "prior-art" / "index.json"
KG = ROOT / "knowledge" / "graph.json"
DISTILLED = ROOT / "distilled"


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


etg = _load("extract_terms_graph")
nov = _load("novelty_check_skill")


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def skill_texts(s: dict) -> tuple[str, list[str]]:
    steps = [f"{st.get('action') or ''} {st.get('expect') or ''}" if isinstance(st, dict) else str(st)
             for st in s.get("steps") or []]
    j = lambda xs: " ".join(str(x) for x in (xs or []))  # noqa: E731
    blob = " ".join([s.get("name") or "", s.get("goal") or "", j(s.get("constraints")),
                     j(s.get("tags")), j(s.get("verification"))] + steps)
    return blob, steps


DOMAIN: str | None = None
SKILL_DOMAINS = {"synth": {"cinematic-synth", "music-synthesis", "synth"},
                 "blender": {"3d-blender", "blender"}, "drone": {"spatial-3d-capture", "drone"},
                 "sidehustle": {"side-hustle", "sidehustle"}, "crypto": {"crypto-investing", "crypto"}}
AS_OF: str | None = None  # --as-of YYYY-MM-DD: replay against the library as it was before that date


def excluded_ids(vid: str) -> set[str]:
    """Skills that must not count as prior coverage: distilled from this video, or (with --as-of)
    published on/after the replay date."""
    out = set()
    for q in SKILLS.glob("*.json"):
        t = q.read_text()
        if vid in t:
            out.add(q.stem)
            continue
        dom = json.loads(t).get("domain")
        if DOMAIN and dom and dom not in SKILL_DOMAINS.get(DOMAIN, {DOMAIN}):
            out.add(q.stem)  # pipeline/meta skills quote the lexicons; they are not domain coverage
        elif AS_OF:
            pa = (json.loads(t).get("published_at") or "")[:10]
            if pa and pa >= AS_OF:
                out.add(q.stem)
    return out


def coverage(domain_lex: dict, exclude_video: str | None = None) -> dict:
    """exclude_video: skip skills distilled FROM this video, so a re-check is not self-covered."""
    M = etg.Matcher(domain_lex)
    excl = excluded_ids(exclude_video) if exclude_video else set()
    nodes: dict[str, set[str]] = {}
    step_pairs: dict[tuple[str, str], set[str]] = {}
    values: dict[str, set[str]] = {}
    for p in sorted(SKILLS.glob("*.json")):
        s = json.loads(p.read_text())
        if p.stem in excl:
            continue
        blob, steps = skill_texts(s)
        for h in M.find(blob):
            nodes.setdefault(f"{h['type']}:{h['canon']}", set()).add(s["id"])
        low = blob.lower()
        for vm in list(etg.VALUE_RE.finditer(low)) + list(etg.VALUE_RE2.finditer(low)):
            values.setdefault(etg.norm_value(vm.group(1), vm.group(2)), set()).add(s["id"])
        for st in steps:
            ids = {f"{h['type']}:{h['canon']}" for h in M.find(st)}
            for a in ids:
                for b in ids:
                    if a != b:
                        step_pairs.setdefault((a, b), set()).add(s["id"])
    return {"nodes": nodes, "pairs": step_pairs, "values": values}


def prior_terms() -> list[str]:
    if not PRIOR.exists():
        return []
    d = json.loads(PRIOR.read_text())
    return [(r.get("name", "") + " " + r.get("goal_or_summary", "")).lower() for r in d.get("skills", [])]


def load_kg() -> dict:
    if KG.exists():
        return json.loads(KG.read_text())
    return {"schema": "yt-knowledge-graph/kg-v1", "updated_at": None, "videos": {}, "nodes": {}, "edges": {}}


def ekey(e: dict) -> str:
    return f"{e['src']}|{e['type']}|{e['dst']}"


def merge_into_kg(kg: dict, g: dict, gaps: dict) -> dict:
    vid = g["video_id"]
    kg["videos"][vid] = {"domain": g["domain"], "title": g["source"].get("title"), "route": g["source"].get("route"),
                         "translated": g["source"].get("translated"), "merged_at": now(),
                         "gap_nodes": len(gaps["gap_nodes"]), "gap_edges": len(gaps["gap_edges"])}
    for n in g["nodes"]:
        if n["type"] in ("step",):
            continue  # steps are per-video procedure; kept in raw graph only
        k = n["id"]
        cur = kg["nodes"].setdefault(k, {"type": n["type"], "label": n["label"], "domain": g["domain"],
                                         "videos": [], "refs": [], "covered_by": []})
        if vid not in cur["videos"]:
            cur["videos"].append(vid)
        for ev in n["evidence"][:2]:
            ref = {"video_id": vid, "t": ev["t"]}
            if ref not in cur["refs"] and len(cur["refs"]) < 8:
                cur["refs"].append(ref)
        cur["covered_by"] = sorted(set(cur["covered_by"]) | set(gaps["node_cover"].get(k, [])))
    for e in g["edges"]:
        if e["type"] in ("mentions", "precedes"):
            continue
        k = ekey(e)
        cur = kg["edges"].setdefault(k, {"src": e["src"], "dst": e["dst"], "type": e["type"], "videos": [],
                                         "refs": [], "covered_by": []})
        if vid not in cur["videos"]:
            cur["videos"].append(vid)
        ref = {"video_id": vid, "t": e["evidence"][0]["t"]}
        if ref not in cur["refs"] and len(cur["refs"]) < 8:
            cur["refs"].append(ref)
        cur["covered_by"] = sorted(set(cur["covered_by"]) | set(gaps["edge_cover"].get(k, [])))
    kg["updated_at"] = now()
    kg["stats"] = {"videos": len(kg["videos"]), "nodes": len(kg["nodes"]), "edges": len(kg["edges"]),
                   "uncovered_nodes": sum(1 for n in kg["nodes"].values() if not n["covered_by"] and n["type"] in ("param", "module", "concept", "tool")),
                   "uncovered_edges": sum(1 for e in kg["edges"].values() if not e["covered_by"] and e["type"] in ("sets", "affects"))}
    return kg


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60]


GENERIC_PARAMS = {"attack", "decay", "sustain", "release", "cutoff", "resonance", "detune", "lfo_rate",
                  "lfo_depth", "mix", "volume", "gain", "pan", "pitch", "level", "waveform", "phase", "feedback",
                  "decay_time", "threshold", "env_amount", "lfo_shape", "voice_count", "blend", "glide"}


def covered_verdict(g: dict, node_cover: dict, edge_cover: dict, gap_nodes: list, candidates: list,
                    corpus: list) -> dict:
    """Video-level 'already covered?' decision.

    Topic terms (module/concept/tool: filter, envelope, pad, reverb...) are matched by almost
    every skill, so they are NOT evidence of coverage. Coverage needs procedure/parameter level
    overlap with ONE skill: its specific items = technique nodes + non-generic param nodes +
    sets/affects edges. COVERED only if
      - no uncovered technique node, and
      - a single existing skill covers >= 50% of the specific items, and
      - the whole-video novelty score (novelty_check_skill logic) is not NOVEL.
    Otherwise GAP.
    """
    vid = g["video_id"]
    spec = []
    for n in g["nodes"]:
        if (n["type"] == "technique" and n["count"] >= 2) or (n["type"] == "param" and n["id"].split(":", 1)[1] not in GENERIC_PARAMS):
            spec.append(("n", n["id"], set(node_cover.get(n["id"], []))))
    for e in g["edges"]:
        if e["type"] in ("sets", "affects"):
            spec.append(("e", ekey(e), set(edge_cover.get(ekey(e), []))))
    techniques = [n["id"] for n in g["nodes"] if n["type"] == "technique" and n["count"] >= 2]
    unc_tech = [x["id"] for x in gap_nodes if x["type"] == "technique" and x["count"] >= 2]
    per = Counter()
    for _, _, ss in spec:
        per.update(ss)
    best_skill, best_n = (per.most_common(1)[0] if per else (None, 0))
    # techniques the video is about must be in that same skill, not spread over several
    tech_split = [i for k, i, ss in spec if i.startswith("technique:") and best_skill not in ss]
    proc = round(best_n / len(spec), 3) if spec else 0.0
    # whole-video novelty: specific terms + title, scored like a candidate skill
    words = [g["source"].get("title") or ""] + [i.split(":", 1)[1].replace("_", " ") for _, i, _ in spec if _ == "n"]
    words += [n["label"] for n in g["nodes"] if n["type"] in ("module", "concept")]
    toks = nov.tokenize(" ".join(words))
    self_ids = excluded_ids(vid)
    rows = [r for r in corpus if r["id"] not in self_ids]
    sc = sorted(((nov.score_candidate(toks, r), r) for r in rows), key=lambda x: -x[0])[:3]
    vnov = round(sc[0][0], 3) if sc else 0.0
    vverd = nov.classify(vnov)
    reasons = []
    if candidates:
        reasons.append("dense gap-step candidates")
    if unc_tech:
        reasons.append("uncovered techniques: " + ", ".join(unc_tech))
    thin = len(spec) < 3
    prof = [n["id"] for n in g["nodes"] if n["type"] in ("module", "concept")]
    pc = Counter()
    for i in prof:
        pc.update(set(node_cover.get(i, [])))
    prof_skill, prof_n = (pc.most_common(1)[0] if pc else (None, 0))
    prof_share = round(prof_n / len(prof), 3) if prof else 0.0
    if thin:
        # too little procedure evidence to call it covered on parameters: require one skill to
        # hold nearly the whole topic profile (a beginner ADSR video vs. the ADSR skill)
        if prof_share < 0.8:
            reasons.append(f"thin procedure evidence ({len(spec)} items) and best single-skill "
                           f"topic profile {prof_share} < 0.8")
    elif proc < 0.5:
        reasons.append(f"best single-skill procedure overlap {proc} < 0.5")
    if tech_split and not unc_tech:
        reasons.append("techniques not in the best-overlap skill: " + ", ".join(tech_split))
    # whole-video novelty is reported as evidence only: transcript-level token sets score NOVEL
    # even for genuinely covered videos, so it cannot veto a procedure-level match
    return {"decision": "GAP" if reasons else "COVERED", "reasons": reasons or ["procedure-level overlap"],
            "specific_items": len(spec), "technique_split": tech_split,
            "profile_skill": prof_skill, "profile_share": prof_share, "best_skill": best_skill, "best_proc_overlap": proc,
            "techniques": techniques, "uncovered_techniques": unc_tech,
            "video_novelty": vnov, "video_novelty_verdict": vverd,
            "nearest_existing": [{"id": r["id"], "kind": r.get("kind"), "score": round(s, 3)} for s, r in sc]}


def analyze(g: dict, min_steps: int = 3) -> dict:
    global DOMAIN
    DOMAIN = g["domain"]
    lex = etg.load_lexicons()[g["domain"]]
    vid = g["video_id"]
    excl = excluded_ids(vid)
    cov = coverage(lex, exclude_video=vid)
    kg = load_kg()
    pri = prior_terms()
    node_cover, edge_cover = {}, {}
    gap_nodes, gap_edges = [], []
    for n in g["nodes"]:
        if n["type"] not in ("param", "module", "concept", "tool", "phrase", "value", "technique"):
            continue
        if n["type"] == "value":
            continue  # values are judged through their sets-edge
        covered = sorted(cov["nodes"].get(n["id"], set()))
        if n["type"] == "phrase":
            covered = [p.stem for p in SKILLS.glob("*.json") if n["label"] in p.read_text().lower()][:5]
        node_cover[n["id"]] = covered
        if not covered:
            kgn = kg["nodes"].get(n["id"])
            gap_nodes.append({"id": n["id"], "type": n["type"], "label": n["label"], "count": n["count"],
                              "known_in_kg": bool(kgn and any(v != vid for v in kgn["videos"])),
                              "prior_art": sum(1 for t in pri if n["label"] in t) if len(n["label"]) > 3 else 0,
                              "first_t": n["evidence"][0]["t"] if n["evidence"] else None})
    for e in g["edges"]:
        if e["type"] not in ("sets", "affects"):
            continue
        if e["type"] == "sets":
            val = e.get("value", "")
            src_cov = cov["nodes"].get(e["src"], set())
            covered = sorted(src_cov & cov["values"].get(val, set()))
        else:
            covered = sorted(cov["pairs"].get((e["src"], e["dst"]), set()))
        edge_cover[ekey(e)] = covered
        if not covered:
            kge = kg["edges"].get(ekey(e))
            gap_edges.append({"key": ekey(e), "src": e["src"], "dst": e["dst"], "type": e["type"],
                              "value": e.get("value"), "count": e["count"],
                              "known_in_kg": bool(kge and any(v != vid for v in kge["videos"])),
                              "t": e["evidence"][0]["t"], "quote": e["evidence"][0]["quote"]})
    gap_node_ids = {x["id"] for x in gap_nodes if x["type"] != "phrase"}
    gap_edge_ts = {}
    for x in gap_edges:
        gap_edge_ts.setdefault(x["t"], []).append(x)
    # steps in order, with gap score
    steps = [n for n in g["nodes"] if n["type"] == "step"]
    steps.sort(key=lambda n: etg.parse_ts(n["at"]))
    mentions = {}
    for e in g["edges"]:
        if e["type"] == "mentions":
            mentions.setdefault(e["src"], set()).add(e["dst"])
    scored = []
    for s in steps:
        gn = sorted(mentions.get(s["id"], set()) & gap_node_ids)
        ge = gap_edge_ts.get(s["at"], [])
        scored.append({"step": s, "gap_nodes": gn, "gap_edges": ge, "score": len(gn) + 2 * len(ge)})
    # runs: contiguous steps with score>0, allowing one zero-score step inside
    runs, cur, zeros = [], [], 0
    for r in scored:
        if r["score"] > 0:
            cur.append(r)
            zeros = 0
        elif cur and zeros == 0:
            cur.append(r)
            zeros = 1
        else:
            if cur:
                runs.append(cur)
            cur, zeros = [], 0
    if cur:
        runs.append(cur)
    runs = [[r for r in run] for run in runs]
    for run in runs:
        while run and run[-1]["score"] == 0:
            run.pop()
    candidates = []
    corpus = [r for r in nov.load_corpus() if r["id"] not in excl]
    for run in runs:
        items = sum(len(r["gap_nodes"]) + len(r["gap_edges"]) for r in run)
        if len(run) < min_steps or items < 2:
            continue
        gnodes = Counter(x for r in run for x in r["gap_nodes"])
        gedges = [x for r in run for x in r["gap_edges"]]
        all_terms = Counter(t for r in run for t in mentions.get(r["step"]["id"], set()))
        top_terms = [t.split(":", 1)[1].replace("_", " ") for t, _ in all_terms.most_common(4)]
        delta_bits = [f"{e['src'].split(':')[1]} {e['type']} {e['dst'].split(':')[1].replace('=', ' ')}" for e in gedges[:4]]
        delta_bits += [n.split(":")[1].replace("_", " ") for n, _ in gnodes.most_common(3)]
        cid = slug(f"{g['domain']} {' '.join(top_terms[:3])} {run[0]['step']['at']}")
        name = f"{g['source'].get('title') or vid}: {', '.join(top_terms[:3])} ({run[0]['step']['at']}-{run[-1]['step']['at']})"
        goal = ("Delta vs library: " + "; ".join(delta_bits) +
                f". Grounded in transcript {run[0]['step']['at']}-{run[-1]['step']['at']} of {vid}.")
        tags = [g["domain"], "from-youtube", "candidate"] + [t.replace(" ", "-") for t in top_terms]
        toks = nov.tokenize(" ".join([cid.replace("-", " "), name, goal, " ".join(tags)]))
        scored_c = sorted(((nov.score_candidate(toks, row), row) for row in corpus), key=lambda x: -x[0])[:3]
        best = scored_c[0][0] if scored_c else 0.0
        candidates.append({
            "candidate_id": cid,
            "status": "outline - needs distill-transcript + quality_check + novelty_check before publish",
            "video_id": vid,
            "domain": g["domain"],
            "name_draft": name,
            "goal_draft": goal,
            "translated_source": bool(g["source"].get("translated")),
            "span": [run[0]["step"]["at"], run[-1]["step"]["at"]],
            "grounded_steps": [{"t": r["step"]["at"], "quote": r["step"]["evidence"][0]["quote"],
                                "gap_terms": r["gap_nodes"], "gap_edges": [x["key"] for x in r["gap_edges"]]}
                               for r in run],
            "gap_nodes": [n for n, _ in gnodes.most_common()],
            "gap_edges": [x["key"] for x in gedges],
            "nearest_existing": [{"id": row["id"], "kind": row["kind"], "score": round(s, 3)} for s, row in scored_c],
            "novelty": {"best_overlap": round(best, 3), "verdict": nov.classify(best)},
            "tags": tags,
        })
    verdict = covered_verdict(g, node_cover, edge_cover, gap_nodes, candidates, corpus)
    if verdict["decision"] == "GAP" and not candidates:
        # no dense run of gap steps, but the procedure as a whole is not in any one skill:
        # outline the whole video so distill-transcript gets a grounded starting point
        steps_spec = [r for r in scored if any(t.split(":")[0] in ("technique", "param")
                                               for t in mentions.get(r["step"]["id"], set()))] or scored
        if steps_spec:
            tech = verdict["techniques"]
            cid = slug(f"{g['domain']} {' '.join(t.split(':')[1] for t in tech[:3]) or 'procedure'} whole-video")
            candidates.append({
                "candidate_id": cid,
                "status": "outline - needs distill-transcript + quality_check + novelty_check before publish",
                "video_id": vid, "domain": g["domain"],
                "name_draft": f"{g['source'].get('title') or vid}: whole-video procedure",
                "goal_draft": ("Delta vs library: procedure-level overlap with best skill "
                               f"{verdict['best_skill']} = {verdict['best_proc_overlap']}; uncovered techniques: "
                               + (", ".join(verdict["uncovered_techniques"]) or "none") + "."),
                "translated_source": bool(g["source"].get("translated")),
                "span": [steps_spec[0]["step"]["at"], steps_spec[-1]["step"]["at"]],
                "grounded_steps": [{"t": r["step"]["at"], "quote": r["step"]["evidence"][0]["quote"],
                                    "gap_terms": r["gap_nodes"], "gap_edges": [x["key"] for x in r["gap_edges"]]}
                                   for r in steps_spec[:25]],
                "gap_nodes": verdict["uncovered_techniques"], "gap_edges": [x["key"] for x in gap_edges],
                "nearest_existing": verdict["nearest_existing"],
                "novelty": {"best_overlap": verdict["video_novelty"], "verdict": verdict["video_novelty_verdict"]},
                "tags": [g["domain"], "from-youtube", "candidate", "whole-video"],
            })
    return {"video_id": vid, "domain": g["domain"], "analyzed_at": now(), "covered_verdict": verdict,
            "gap_nodes": gap_nodes, "gap_edges": gap_edges, "node_cover": node_cover, "edge_cover": edge_cover,
            "candidates": candidates,
            "stats": {"graph_nodes": g["stats"]["nodes"], "graph_edges": g["stats"]["edges"],
                      "terms_checked": len(node_cover), "terms_covered": sum(1 for v in node_cover.values() if v),
                      "gap_nodes": len(gap_nodes), "gap_nodes_excl_phrases": len(gap_node_ids),
                      "relations_checked": len(edge_cover), "gap_edges": len(gap_edges),
                      "candidates": len(candidates)}}


def main() -> int:
    ap = argparse.ArgumentParser(description="Graph vs library gap check + knowledge-graph merge")
    ap.add_argument("video_id")
    ap.add_argument("--graph", help="graph.json path (default raw/<id>/graph.json)")
    ap.add_argument("--no-kg-update", action="store_true")
    ap.add_argument("--min-steps", type=int, default=3)
    ap.add_argument("--as-of", help="replay: ignore skills published on/after this date (YYYY-MM-DD)")
    a = ap.parse_args()
    gp = Path(a.graph) if a.graph else RAW / a.video_id / "graph.json"
    g = json.loads(gp.read_text())
    global AS_OF
    AS_OF = a.as_of
    res = analyze(g, a.min_steps)
    (RAW / a.video_id / "gaps.json").write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n")
    cdir = DISTILLED / a.video_id / "candidates"
    if res["candidates"]:
        cdir.mkdir(parents=True, exist_ok=True)
        for c in res["candidates"]:
            (cdir / f"{c['candidate_id']}.outline.json").write_text(json.dumps(c, indent=1, ensure_ascii=False) + "\n")
    if not a.no_kg_update:
        KG.parent.mkdir(parents=True, exist_ok=True)
        kg = merge_into_kg(load_kg(), g, res)
        KG.write_text(json.dumps(kg, indent=1, ensure_ascii=False) + "\n")
        res["stats"]["kg"] = kg["stats"]
    print(json.dumps({"video_id": a.video_id, **res["stats"],
                      "candidate_ids": [c["candidate_id"] for c in res["candidates"]],
                      "decision": res["covered_verdict"]["decision"],
                      "covered_verdict": {k: res["covered_verdict"][k] for k in
                                          ("reasons", "best_skill", "profile_share", "best_proc_overlap", "specific_items",
                                           "uncovered_techniques", "video_novelty", "video_novelty_verdict")}}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
