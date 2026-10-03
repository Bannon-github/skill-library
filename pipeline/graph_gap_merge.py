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


def coverage(domain_lex: dict) -> dict:
    M = etg.Matcher(domain_lex)
    nodes: dict[str, set[str]] = {}
    step_pairs: dict[tuple[str, str], set[str]] = {}
    values: dict[str, set[str]] = {}
    for p in sorted(SKILLS.glob("*.json")):
        s = json.loads(p.read_text())
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


def analyze(g: dict, min_steps: int = 3) -> dict:
    lex = etg.load_lexicons()[g["domain"]]
    cov = coverage(lex)
    kg = load_kg()
    pri = prior_terms()
    vid = g["video_id"]
    node_cover, edge_cover = {}, {}
    gap_nodes, gap_edges = [], []
    for n in g["nodes"]:
        if n["type"] not in ("param", "module", "concept", "tool", "phrase", "value"):
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
    corpus = nov.load_corpus()
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
    return {"video_id": vid, "domain": g["domain"], "analyzed_at": now(),
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
    a = ap.parse_args()
    gp = Path(a.graph) if a.graph else RAW / a.video_id / "graph.json"
    g = json.loads(gp.read_text())
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
                      "candidate_ids": [c["candidate_id"] for c in res["candidates"]]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
