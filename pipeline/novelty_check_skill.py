#!/usr/bin/env python3
"""Novelty / prior-art overlap check for candidate YouTube-distilled skills.

Usage:
  python novelty_check_skill.py path/to/candidate.json
  python novelty_check_skill.py --goal "Build a Blender donut with shade smooth"
  python novelty_check_skill.py --name "supersaw pad" --goal "..." --tags pad,unison
  python novelty_check_skill.py --json path/to/candidate.json --top 10

Exit codes: 0 = novel enough, 1 = high overlap (reject or distill-delta), 2 = usage/IO.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PRIOR_ART = Path("/workspace/skill-library/prior-art/index.json")
MCP_SKILLS = Path("/workspace/skill-library/mcp-publish/skills")

STOP = {
    "a", "an", "the", "and", "or", "to", "of", "in", "on", "for", "with", "from",
    "using", "use", "via", "into", "as", "by", "is", "are", "be", "this", "that",
    "your", "you", "how", "when", "skill", "agent", "create", "make", "build",
}


def tokenize(text: str) -> set[str]:
    toks = re.findall(r"[a-z0-9][a-z0-9+\-./]*", (text or "").lower())
    out = set()
    for t in toks:
        if t in STOP or len(t) < 2:
            continue
        out.add(t)
        # also add hyphen fragments
        for part in t.split("-"):
            if part and part not in STOP and len(part) >= 2:
                out.add(part)
    return out


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def load_corpus() -> list[dict]:
    rows: list[dict] = []
    if PRIOR_ART.exists():
        doc = json.loads(PRIOR_ART.read_text(encoding="utf-8"))
        for s in doc.get("skills", []):
            rows.append(
                {
                    "id": s.get("id", ""),
                    "name": s.get("name", ""),
                    "goal": s.get("goal_or_summary", ""),
                    "tags": s.get("domains", []),
                    "source": s.get("source_collection", "prior-art"),
                    "url": s.get("url", ""),
                    "kind": "prior-art",
                }
            )
    if MCP_SKILLS.exists():
        for p in sorted(MCP_SKILLS.glob("*.json")):
            try:
                d = json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                continue
            rows.append(
                {
                    "id": d.get("id", p.stem),
                    "name": d.get("name", ""),
                    "goal": d.get("goal", ""),
                    "tags": d.get("tags", []) or ([d.get("domain")] if d.get("domain") else []),
                    "source": "youtube-skills/mcp-publish",
                    "url": d.get("mcp_resource") or f"skill://{d.get('id', p.stem)}",
                    "kind": "local",
                }
            )
    for r in rows:
        blob = " ".join(
            [
                r["id"].replace("-", " "),
                r["name"],
                r["goal"],
                " ".join(str(t) for t in (r["tags"] or [])),
            ]
        )
        r["_tokens"] = tokenize(blob)
    return rows


def score_candidate(cand_tokens: set[str], row: dict) -> float:
    # weight id/name overlap slightly higher via re-tokenize of name+id alone
    base = jaccard(cand_tokens, row["_tokens"])
    name_toks = tokenize(f"{row['id']} {row['name']}")
    name_j = jaccard(cand_tokens, name_toks)
    return 0.65 * base + 0.35 * name_j


def classify(best: float) -> str:
    # Heuristic thresholds for token Jaccard blend
    if best >= 0.42:
        return "REJECT_OR_DELTA"
    if best >= 0.28:
        return "WARN_NEAR_DUPLICATE"
    if best >= 0.18:
        return "REVIEW"
    return "NOVEL"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path", nargs="?", help="Candidate skill JSON path")
    ap.add_argument("--json", dest="json_path", help="Alias for candidate JSON path")
    ap.add_argument("--goal", help="Goal string if no JSON")
    ap.add_argument("--name", help="Name string if no JSON")
    ap.add_argument("--tags", help="Comma-separated tags")
    ap.add_argument("--id", help="Candidate id")
    ap.add_argument("--top", type=int, default=8)
    ap.add_argument("--exclude-id", help="Ignore this id when scoring (self)")
    args = ap.parse_args()

    path = args.json_path or args.path
    cand = {"id": args.id or "", "name": args.name or "", "goal": args.goal or "", "tags": []}
    if args.tags:
        cand["tags"] = [t.strip() for t in args.tags.split(",") if t.strip()]

    if path:
        p = Path(path)
        if not p.exists():
            print(f"error: missing {p}", file=sys.stderr)
            return 2
        data = json.loads(p.read_text(encoding="utf-8"))
        if isinstance(data, str):
            cand["goal"] = data
        else:
            cand["id"] = data.get("id") or cand["id"]
            cand["name"] = data.get("name") or cand["name"]
            cand["goal"] = data.get("goal") or cand["goal"]
            cand["tags"] = data.get("tags") or cand["tags"]
            args.exclude_id = args.exclude_id or cand["id"]

    if not (cand["goal"] or cand["name"] or cand["id"]):
        print("error: provide a skill JSON or --goal/--name", file=sys.stderr)
        return 2

    cand_tokens = tokenize(
        " ".join(
            [
                cand["id"].replace("-", " "),
                cand["name"],
                cand["goal"],
                " ".join(cand["tags"] or []),
            ]
        )
    )
    corpus = load_corpus()
    scored = []
    for row in corpus:
        if args.exclude_id and row["id"] == args.exclude_id and row["kind"] == "local":
            continue
        s = score_candidate(cand_tokens, row)
        if s <= 0:
            continue
        scored.append((s, row))
    scored.sort(key=lambda x: -x[0])
    top = scored[: args.top]
    best = top[0][0] if top else 0.0
    verdict = classify(best)
    # novelty score: 1 - best overlap (clamped)
    novelty = max(0.0, min(1.0, 1.0 - best))

    print(f"candidate_id: {cand['id'] or '(none)'}")
    print(f"candidate_name: {cand['name'] or '(none)'}")
    print(f"tokens: {len(cand_tokens)}")
    print(f"best_overlap: {best:.3f}")
    print(f"novelty_score: {novelty:.3f}  (1.0 = fully novel vs index)")
    print(f"verdict: {verdict}")
    if verdict == "REJECT_OR_DELTA":
        print(
            "action: reject publish OR distill only the missing delta "
            "(state the delta explicitly in goal)."
        )
    elif verdict == "WARN_NEAR_DUPLICATE":
        print("action: prefer more specific stack/curriculum-tied delta before publish.")
    print("--- top matches ---")
    for s, row in top:
        print(
            f"{s:.3f}  [{row['kind']}] {row['source']} :: {row['id']}\n"
            f"       name={row['name'][:80]}\n"
            f"       goal={row['goal'][:120]}\n"
            f"       url={row['url']}"
        )

    return 1 if verdict == "REJECT_OR_DELTA" else 0


if __name__ == "__main__":
    sys.exit(main())
