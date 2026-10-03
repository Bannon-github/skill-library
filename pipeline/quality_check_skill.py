#!/usr/bin/env python3
"""Validate AgentConsumableSkill v1 JSON for the YouTube skills library.

Usage:
  python quality_check_skill.py                     # all mcp-publish/skills
  python quality_check_skill.py path/to/skill.json
  python quality_check_skill.py --dir /path/to/dir
  python quality_check_skill.py --strict            # warnings become failures

Exit codes: 0 = all pass, 1 = one or more failures, 2 = usage/IO error.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED = (
    "schema_version",
    "id",
    "name",
    "goal",
    "steps",
    "inputs",
    "outputs",
    "prerequisites",
    "constraints",
)

DEFAULT_SKILLS_DIR = Path("/workspace/skill-library/mcp-publish/skills")
PRIOR_ART_INDEX = Path("/workspace/skill-library/prior-art/index.json")
_PRIOR_CACHE: list[dict] | None = None
_STOP = {
    "a", "an", "the", "and", "or", "to", "of", "in", "on", "for", "with", "from",
    "using", "use", "via", "into", "as", "by", "is", "are", "be", "this", "that",
    "skill", "agent", "create", "make", "build",
}


def _tok(text: str) -> set[str]:
    toks = re.findall(r"[a-z0-9][a-z0-9+\-./]*", (text or "").lower())
    out: set[str] = set()
    for t in toks:
        if t in _STOP or len(t) < 2:
            continue
        out.add(t)
        for part in t.split("-"):
            if part and part not in _STOP and len(part) >= 2:
                out.add(part)
    return out


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def _load_prior_art() -> list[dict]:
    global _PRIOR_CACHE
    if _PRIOR_CACHE is not None:
        return _PRIOR_CACHE
    _PRIOR_CACHE = []
    if not PRIOR_ART_INDEX.exists():
        return _PRIOR_CACHE
    try:
        doc = json.loads(PRIOR_ART_INDEX.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return _PRIOR_CACHE
    for s in doc.get("skills", []):
        if s.get("source_collection") in ("youtube-skills",):
            continue
        blob = f"{s.get('id','')} {s.get('name','')} {s.get('goal_or_summary','')}"
        _PRIOR_CACHE.append({"id": s.get("id", ""), "source": s.get("source_collection", ""), "tokens": _tok(blob)})
    return _PRIOR_CACHE


def prior_art_overlap_warning(data: dict) -> str | None:
    """Warn if name/goal heavily overlaps external prior-art index."""
    prior = _load_prior_art()
    if not prior:
        return None
    cand = _tok(
        f"{data.get('id','')} {data.get('name','')} {data.get('goal','')} "
        f"{' '.join(data.get('tags') or [])}"
    )
    if len(cand) < 4:
        return None
    best = 0.0
    best_id = ""
    best_src = ""
    for row in prior:
        sc = 0.65 * _jaccard(cand, row["tokens"]) + 0.35 * _jaccard(
            cand, _tok(row["id"].replace("-", " "))
        )
        if sc > best:
            best = sc
            best_id = row["id"]
            best_src = row["source"]
    if best >= 0.42:
        return (
            f"prior-art high overlap ({best:.2f}) with {best_src}::{best_id} — "
            "reject or distill-only-delta (see novelty_check_skill.py)"
        )
    if best >= 0.25:
        return (
            f"prior-art near overlap ({best:.2f}) with {best_src}::{best_id} — "
            "prefer more specific stack/curriculum-tied goal"
        )
    return None


MIN_STEPS = 3
MIN_GOAL_LEN = 40
MIN_ACTION_LEN = 8


def check_skill(data: dict, path: Path, strict: bool = False) -> tuple[list[str], list[str]]:
    """Return (failures, warnings)."""
    fails: list[str] = []
    warns: list[str] = []

    if not isinstance(data, dict):
        return [f"{path}: root is not an object"], warns

    for key in REQUIRED:
        if key not in data:
            fails.append(f"missing required field: {key}")

    if data.get("schema_version") != "1.0":
        fails.append(f"schema_version must be '1.0', got {data.get('schema_version')!r}")

    for field in ("id", "name", "goal"):
        val = data.get(field)
        if field in data and (not isinstance(val, str) or not val.strip()):
            fails.append(f"{field} is empty")

    goal = data.get("goal") or ""
    if isinstance(goal, str) and goal.strip() and len(goal.strip()) < MIN_GOAL_LEN:
        msg = f"goal too short ({len(goal.strip())} < {MIN_GOAL_LEN}): {goal.strip()!r}"
        (fails if strict else warns).append(msg)

    steps = data.get("steps")
    if "steps" in data:
        if not isinstance(steps, list):
            fails.append("steps must be an array")
        elif len(steps) == 0:
            fails.append("steps is empty")
        elif len(steps) < MIN_STEPS:
            msg = f"fewer than {MIN_STEPS} steps ({len(steps)})"
            (fails if strict else warns).append(msg)
        else:
            for i, step in enumerate(steps):
                if not isinstance(step, dict):
                    fails.append(f"steps[{i}] is not an object")
                    continue
                if "n" not in step:
                    fails.append(f"steps[{i}] missing n")
                if "action" not in step:
                    fails.append(f"steps[{i}] missing action")
                else:
                    action = step.get("action")
                    if not isinstance(action, str) or not action.strip():
                        fails.append(f"steps[{i}] has empty action")
                    elif len(action.strip()) < MIN_ACTION_LEN:
                        msg = f"steps[{i}] action very short"
                        (fails if strict else warns).append(msg)
                if not step.get("expect"):
                    warns.append(f"steps[{i}] missing expect")

    for arr_name in ("prerequisites", "constraints", "inputs", "outputs"):
        if arr_name in data and not isinstance(data.get(arr_name), list):
            fails.append(f"{arr_name} must be an array")

    ver = data.get("verification")
    if ver is None:
        msg = "verification field missing"
        (fails if strict else warns).append(msg)
    elif not isinstance(ver, list):
        fails.append("verification must be an array")
    elif len(ver) == 0:
        msg = "verification is empty"
        (fails if strict else warns).append(msg)
    else:
        for i, v in enumerate(ver):
            if not isinstance(v, str) or not v.strip():
                fails.append(f"verification[{i}] empty")

    tags = data.get("tags")
    if tags is not None and not isinstance(tags, list):
        fails.append("tags must be an array")
    elif isinstance(tags, list) and len(tags) == 0:
        warns.append("tags is empty")

    cur = data.get("curriculum_ids")
    if cur is not None and not isinstance(cur, list):
        fails.append("curriculum_ids must be an array")
    elif isinstance(cur, list) and len(cur) == 0:
        warns.append("curriculum_ids is empty")

    # Soft promo / thin heuristics (skip meta pipeline skills that mention CTAs to strip)
    domain = data.get("domain")
    if domain != "meta-pipeline":
        blob = " ".join(
            [
                str(goal),
                " ".join(str(s.get("action", "")) for s in (steps or []) if isinstance(s, dict)),
            ]
        ).lower()
        # Prefer multi-word / finance-hype phrases to avoid "subscribe CTAs" meta text
        promo_hits = [
            p
            for p in (
                "like and subscribe",
                "smash that",
                "link in bio",
                "use my code",
                "guaranteed profit",
                "risk-free returns",
                "guaranteed apy",
            )
            if p in blob
        ]
        if promo_hits:
            msg = f"possible promo/finance-hype language: {promo_hits}"
            (fails if strict else warns).append(msg)

    domain = data.get("domain")
    if domain == "cinematic-synth" or (isinstance(tags, list) and "cinematic-synth" in tags):
        cons = data.get("constraints") or []
        if isinstance(cons, list) and len(cons) >= 4:
            # duplicated boilerplate is common; warn if many near-identical lines
            lowered = [c.lower().strip() for c in cons if isinstance(c, str)]
            originals = [c for c in lowered if "original synthesis" in c or "not affiliated" in c]
            if len(originals) >= 3:
                warns.append("constraints repeat affiliation/original-synthesis boilerplate (≥3)")

    pa = prior_art_overlap_warning(data)
    if pa:
        (fails if strict else warns).append(pa)

    return fails, warns


def load_json(path: Path) -> dict:
    with path.open() as f:
        return json.load(f)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path, help="Skill JSON files")
    parser.add_argument("--dir", type=Path, help="Directory of skill JSON files")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    parser.add_argument("--json", action="store_true", help="Machine-readable summary")
    args = parser.parse_args(argv)

    files: list[Path] = []
    if args.paths:
        files.extend(args.paths)
    if args.dir:
        files.extend(sorted(args.dir.glob("*.json")))
    if not files and not args.paths and not args.dir:
        files = sorted(DEFAULT_SKILLS_DIR.glob("*.json"))

    if not files:
        print("No skill files found", file=sys.stderr)
        return 2

    results = []
    n_fail = 0
    n_warn = 0
    for path in files:
        try:
            data = load_json(path)
        except (OSError, json.JSONDecodeError) as e:
            print(f"FAIL {path}: cannot parse ({e})")
            n_fail += 1
            results.append({"path": str(path), "ok": False, "failures": [str(e)], "warnings": []})
            continue
        fails, warns = check_skill(data, path, strict=args.strict)
        if fails:
            n_fail += 1
            status = "FAIL"
        elif warns:
            n_warn += 1
            status = "WARN"
        else:
            status = "OK"
        sid = data.get("id", path.stem) if isinstance(data, dict) else path.stem
        print(f"{status} {sid}")
        for f in fails:
            print(f"  - FAIL: {f}")
        for w in warns:
            print(f"  - warn: {w}")
        results.append(
            {
                "path": str(path),
                "id": sid,
                "ok": not fails,
                "failures": fails,
                "warnings": warns,
            }
        )

    summary = {
        "checked": len(files),
        "failed": n_fail,
        "warned": n_warn,
        "passed_clean": len(files) - n_fail - n_warn,
        "strict": args.strict,
    }
    print(
        f"\nChecked {summary['checked']}: "
        f"{summary['passed_clean']} clean, {summary['warned']} warned, {summary['failed']} failed"
    )
    if args.json:
        print(json.dumps({"summary": summary, "results": results}, indent=2))
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
