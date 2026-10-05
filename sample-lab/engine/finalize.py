"""Pick winners, validate on an extended grid, and write deliverables (systems/, leaderboard.md, workflows/, FINDINGS.md)."""
import json, os, collections, shutil
import numpy as np
from multiprocessing import Pool
import lab, render, skills, metrics
from iterate import LOG, POP, rank_key

LAB = lab.LAB
LIB = "/workspace/skill-library/mcp-publish/skills"
EXT_SEEDS = [11, 23, 37, 51]
PERCEPTUAL = {}  # filled from perceptual.json if present
if os.path.exists(os.path.join(LAB, "runs", "perceptual.json")):
    PERCEPTUAL = json.load(open(os.path.join(LAB, "runs", "perceptual.json")))

def libskill(sid):
    return json.load(open(os.path.join(LIB, sid + ".json")))

def load_log():
    return [json.loads(l) for l in open(LOG)]

def full_chain(c):
    return {"name": c["name"], "category": c["category"],
            "steps": [{"skill": s["skill"], "knobs": skills.fill_knobs(s["skill"], s.get("knobs"))} for s in c["steps"]]}

def lineage(cid, byid):
    path = []
    while cid and cid in byid:
        e = byid[cid]
        path.append({"round": e["round"], "id": cid, "mutation": e.get("mutation"), "robust": e.get("summary", {}).get("robust")})
        cid = e.get("parent")
    return list(reversed(path))

def _ext(args):
    chain, ni, seed, det = args
    audio, r = lab.eval_one(chain, ni, seed, check_det=det)
    M = 0.5 * (audio[:, 0] + audio[:, 1])
    from scipy import signal
    f, P = signal.welch(M, render.SR, nperseg=16384)
    sub = 10 * np.log10(P[(f > 0) & (f < 30)].sum() / P[f > 0].sum() + 1e-20)
    r["advisory_subsonic_below30Hz_db"] = round(float(sub), 1)
    r["noteset"], r["seed"] = ni, seed
    return r

def pick_winners(pop, log):
    cands = {}
    for e in log:
        if "summary" in e and e["summary"]["reliable"] and "rescore" not in (e.get("mutation") or ""):
            cands.setdefault(e["category"], {})[e["id"]] = e
    # latest score per id (rescore entries override)
    latest = {}
    for e in log:
        if "summary" in e:
            latest[e["id"]] = e
    winners = []
    for cat, d in cands.items():
        ranked = sorted([latest[i] for i in d], key=lambda e: (e["summary"]["reliable"], e["summary"]["robust"], e["summary"]["mean"], -len(e["steps"])), reverse=True)
        ranked = [e for e in ranked if e["summary"]["reliable"]]
        if ranked:
            winners.append(ranked[0])
    return winners

def sysname(e):
    base = e["name"]
    return base if base.startswith(e["category"]) else f"{e['category']}-{base}"

def main():
    log = load_log()
    byid = {}
    for e in log:
        byid[e["id"]] = e if e["id"] not in byid or "rescore" not in (e.get("mutation") or "") else {**byid[e["id"]], "summary": e["summary"]}
    pop = json.load(open(POP))["pop"]
    winners = pick_winners(pop, log)
    os.makedirs(os.path.join(LAB, "systems"), exist_ok=True)
    os.makedirs(os.path.join(LAB, "workflows"), exist_ok=True)
    rows = []
    for e in winners:
        name = sysname(e)
        chain = full_chain(e)
        chain["name"] = name
        tasks = [(chain, ni, s, s == EXT_SEEDS[0]) for ni in range(3) for s in EXT_SEEDS]
        with Pool(5) as p:
            res = p.map(_ext, tasks, chunksize=1)
        scores = [r["score"] for r in res]
        ext = {"robust": round(min(scores), 2), "mean": round(float(np.mean(scores)), 2), "pass_count": sum(r["pass"] for r in res), "n": len(res),
               "determinism": all(r["gates"].get("G4_determinism", True) for r in res)}
        d = os.path.join(LAB, "systems", name)
        os.makedirs(d, exist_ok=True)
        chain_out = dict(chain, id=e["id"], found_in_round=e["round"], target_version="v1.3", search_grid=e["summary"], extended_grid=ext,
                         lineage=lineage(e["id"], byid))
        json.dump(chain_out, open(os.path.join(d, "chain.json"), "w"), indent=1, default=str)
        json.dump(res, open(os.path.join(d, "scores.json"), "w"), indent=1, default=str)
        # renders: 3 note sets, seed 11
        wavs = []
        for ni in range(3):
            notes = render.NOTESETS[chain["category"]][ni]
            patch = skills.build_patch(chain)
            audio, info = render.render(patch, notes, 11)
            fn = os.path.join(d, f"{name}__{'-'.join(map(str, notes))}_seed11.wav")
            lab.write_wav(fn, audio)
            lab.spectrogram(fn[:-4] + ".png", audio, f"{name}  notes {notes}  seed 11")
            wavs.append(os.path.basename(fn))
        json.dump(skills.build_patch(chain), open(os.path.join(d, "patch_resolved.json"), "w"), indent=1, default=str)
        write_readme(d, name, chain, ext, res, e, wavs, byid)
        write_workflow(name, chain, ext)
        rows.append((name, chain, ext, e, res))
        print(name, ext, flush=True)
    write_leaderboard(rows, log)
    write_findings(rows, log)

def step_doc(i, st):
    sk = libskill(st["skill"])
    reg = skills.REGISTRY[st["skill"]]
    lines = [f"### {i}. `{st['skill']}`  ({reg['role']})", "", f"*{sk['name']}*", "", f"Why here: {sk['goal']}", "", "| knob | value | grounded in |", "|---|---|---|"]
    for k, v in st["knobs"].items():
        kn = reg["knobs"][k]
        lines.append(f"| {k} | {v} | {kn.cite} |")
    return "\n".join(lines)

def write_readme(d, name, chain, ext, res, e, wavs, byid):
    by_ns = collections.defaultdict(list)
    for r in res:
        by_ns[r["noteset"]].append(r["score"])
    order = " → ".join(f"`{s['skill']}`" for s in chain["steps"])
    md = [f"# {name}", "", f"Category: **{chain['category']}** · found in round {e['round']} · chain id `{e['id']}`", "",
          f"**Firing order:** {order}", "",
          f"**Scores (TARGET v1.3):** search grid {e['summary']['pass_count']}/{e['summary']['n']} pass, robust {e['summary']['robust']}; "
          f"extended grid (3 note sets × 4 seeds) **{ext['pass_count']}/{ext['n']} pass**, robust **{ext['robust']}**, mean {ext['mean']}, deterministic: {ext['determinism']}", "",
          "Typical metric values (note set 0, seed 11): " + ", ".join(f"{k}={v}" for k, v in res[0]["values"].items()), "",
          f"Advisory (not scored): sub-30 Hz energy {res[0]['advisory_subsonic_below30Hz_db']} dB re total.", "",
          "Renders: " + ", ".join(f"[{w}]({w})" for w in wavs) + " (spectrogram PNG alongside each).", "",
          "Re-render: `.venv/bin/python render_system.py " + name + " --notes 50,53,57,64 --seed 11 --score --spectrogram`", "",
          "## Steps (sequential skill activation)", ""]
    for i, st in enumerate(chain["steps"], 1):
        md += [step_doc(i, st), ""]
    md += ["## How the search got here", "", "| round | id | mutation | robust (search grid) |", "|---|---|---|---|"]
    for p in lineage(e["id"], byid):
        md.append(f"| {p['round']} | `{p['id']}` | {p['mutation']} | {p['robust']} |")
    if name in PERCEPTUAL:
        md += ["", "## Perceptual sanity (spectrogram inspection)", "", PERCEPTUAL[name]]
    open(os.path.join(d, "README.md"), "w").write("\n".join(md) + "\n")

def write_workflow(name, chain, ext):
    cat = chain["category"]
    steps = []
    for i, st in enumerate(chain["steps"], 1):
        sk = libskill(st["skill"])
        key = ", ".join(f"{k}={v}" for k, v in list(st["knobs"].items())[:10])
        steps.append(f"{i}. **Activate `{st['skill']}`** — {sk['name']}. Apply with: {key}.")
    md = f"""---
schema: AgentConsumableSkill-draft v1
id: workflow-{name}
name: "Sample workflow: {name.replace('-', ' ')}"
domain: cinematic-synth
kind: workflow (ordered chain of library skills)
status: draft — validated offline by sample-lab, not yet reviewed for publish
skills_used: [{', '.join(s['skill'] for s in chain['steps'])}]
curriculum_ids: [curriculum-cinematic-hybrid-synth]
---

# Goal
Produce a ship-ready {cat} sample (48 kHz/24-bit stereo, 8–12 s) for Polyrhythm Studio by firing the library skills
below **in this order**. Original synthesis only (no presets/samples). Passed sample-lab TARGET v1.3 on
{ext['pass_count']}/{ext['n']} renders (3 note sets × 4 seeds), robust score {ext['robust']}.

# Prerequisites
- Offline renderer: `/workspace/skill-library/sample-lab` (`render_system.py {name}`), or any synth/Web Audio graph with
  the same modules (multi-osc + unison, ladder/SVF filters, envelopes, LFO/mod matrix, chorus, stereo delay, reverb).

# Inputs
- notes: MIDI chord/notes (category test sets in `engine/render.py:NOTESETS`), seed: integer for random sources.

# Steps
{chr(10).join(steps)}
{len(steps)+1}. Master: loudness-normalize to {skills.init_patch(cat)['master']['target_lufs']} LUFS, true-peak limit at −1.3 dBTP, export.

# Verification
- Run `render_system.py {name} --score` → pass=true (TARGET.md v1.3: ≤ −1 dBTP, mono-fold loss, centered lows,
  tilt/balance, no harsh 1/3-oct bump, movement M10/M11, clean tail or seamless loop, deterministic).
- Look at the spectrogram PNG for clicks, aliasing fans, zipper modulation, hiss.

# Outputs
- WAV + spectrogram + score JSON per note set.

# Constraints
- Fire skills in the listed order: later skills refine the same rack slot (e.g. a later reverb skill re-tunes the
  reverb an earlier skill inserted) and FX-order constraints from the skills (sat → EQ → chorus → delay → reverb) hold.
- Knob values stay inside each skill's grounded ranges (see `systems/{name}/README.md` for the citation of every value).
"""
    open(os.path.join(LAB, "workflows", f"{name}.md"), "w").write(md)

def write_leaderboard(rows, log):
    latest = {}
    for e in log:
        if "summary" in e:
            latest[e["id"]] = e
    rounds = max(e["round"] for e in log)
    md = ["# Sample Lab leaderboard", "", f"Target: TARGET.md v1.3 · rounds run: 0–{rounds} · candidate evaluations logged: {sum(1 for e in log if 'summary' in e)} "
          f"(each = 6 renders) · see iterations.jsonl", "",
          "## Winning systems (extended validation: 3 note sets × 4 seeds = 12 renders)", "",
          "| rank | system | category | skills fired (in order) | pass | robust | mean | perceptual check |", "|---|---|---|---|---|---|---|---|"]
    rows = sorted(rows, key=lambda r: (r[2]["pass_count"], r[2]["robust"], r[2]["mean"]), reverse=True)
    for i, (name, chain, ext, e, res) in enumerate(rows, 1):
        md.append(f"| {i} | [{name}](systems/{name}/README.md) | {chain['category']} | " + " → ".join(s["skill"] for s in chain["steps"]) +
                  f" | {ext['pass_count']}/{ext['n']} | {ext['robust']} | {ext['mean']} | {PERCEPTUAL.get(name, 'pending').split('.')[0]} |")
    md += ["", "## Best attempt per category (search grid, all rounds)", "", "| category | best chain id | name | pass/6 | robust | weakest metrics |", "|---|---|---|---|---|---|"]
    best = {}
    for e in latest.values():
        k = (e["summary"]["reliable"], e["summary"]["pass_count"], e["summary"]["robust"])
        if e["category"] not in best or k > best[e["category"]][0]:
            best[e["category"]] = (k, e)
    for cat, (k, e) in sorted(best.items()):
        weak = collections.Counter(m for r in e["renders"] for m in r["weak"])
        md.append(f"| {cat} | `{e['id']}` | {e['name']} | {e['summary']['pass_count']} | {e['summary']['robust']} | {', '.join(weak) or '—'} |")
    md += ["", "## Progress by round (best robust score per category)", "", "| round | " + " | ".join(sorted(best)) + " | reliable chains found |", "|---" * (len(best) + 2) + "|"]
    for rnd in range(rounds + 1):
        es = [e for e in log if e["round"] <= rnd and "summary" in e]
        cells = []
        for cat in sorted(best):
            v = [e["summary"]["robust"] for e in es if e["category"] == cat]
            cells.append(str(max(v)) if v else "—")
        nrel = len({e["id"] for e in es if e["summary"]["reliable"]})
        md.append(f"| {rnd} | " + " | ".join(cells) + f" | {nrel} |")
    open(os.path.join(LAB, "leaderboard.md"), "w").write("\n".join(md) + "\n")

def write_findings(rows, log):
    latest = {}
    for e in log:
        if "summary" in e:
            latest[e["id"]] = e
    stats = collections.defaultdict(lambda: {"n": 0, "rel": 0, "robust": []})
    for e in latest.values():
        for s in {st["skill"] for st in e["steps"]}:
            st = stats[s]; st["n"] += 1; st["rel"] += e["summary"]["reliable"]; st["robust"].append(e["summary"]["robust"])
    # effect of adding a skill: child robust - parent robust
    add_eff = collections.defaultdict(list)
    for e in log:
        if "summary" not in e or not e.get("parent") or e["parent"] not in latest:
            continue
        for part in (e.get("mutation") or "").split("; "):
            if part.startswith("+"):
                sid = part[1:].split(" ")[0]
                add_eff[sid].append(e["summary"]["robust"] - latest[e["parent"]]["summary"]["robust"])
    winners_skills = collections.Counter(s["skill"] for _, c, *_ in rows for s in c["steps"])
    md = ["# Findings: which skills mattered", "", "Computed from every candidate in iterations.jsonl (latest score per chain).", "",
          "| skill | in winners | chains evaluated | % reliable | mean robust | mean Δrobust when added by mutation (n) |", "|---|---|---|---|---|---|"]
    for sid in sorted(skills.REGISTRY, key=lambda s: (-winners_skills[s], -stats[s]["n"])):
        st = stats[sid]
        ae = add_eff.get(sid, [])
        md.append(f"| `{sid}` | {winners_skills[sid]} | {st['n']} | {100*st['rel']/st['n']:.0f}% | {np.mean(st['robust']):.1f} | "
                  f"{(f'{np.mean(ae):+.1f} ({len(ae)})') if ae else '—'} |" if st["n"] else f"| `{sid}` | 0 | 0 | — | — | — |")
    md += ["", "Not implemented in the renderer (gaps): " + "; ".join(f"`{k}` ({v})" for k, v in skills.NOT_IMPLEMENTED.items())]
    open(os.path.join(LAB, "runs", "skill_stats.md"), "w").write("\n".join(md) + "\n")

if __name__ == "__main__":
    main()
