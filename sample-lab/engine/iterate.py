"""Evolutionary iteration over workflow chains. Logs every evaluated candidate to ../iterations.jsonl.
Usage: python iterate.py --rounds N [--resume]"""
import argparse, copy, json, os, sys, time
import numpy as np
from multiprocessing import Pool
import lab, skills
from skills import REGISTRY, K, KI, KC

LAB = lab.LAB
LOG = os.path.join(LAB, "iterations.jsonl")
POP = os.path.join(LAB, "runs", "population.json")
FX_POOL = [s for s, v in REGISTRY.items() if v["role"] in ("fx", "mix")]
MOD_POOL = [s for s, v in REGISTRY.items() if v["role"] in ("mod", "filter", "layer")]
VOICE_POOL = [s for s, v in REGISTRY.items() if v["role"] == "voice"]

# metric -> (skills to try adding, knob-nudge rules [(name-substring, direction)])
GUIDE = {
    "M5": (["midside-eq-bass-focus-width-depth", "traveler-walkthrough-stereo-ladder-lf-width", "mix-pads-role-eq-width-clarity"],
           [("width", -1), ("pan_amt", -1), ("side_hp", +1), ("lf_width", +1), ("narrow", +1), ("split_amt", -1)]),
    "M2": ([], [("width", -1), ("pan", -1), ("split_amt", -1), ("feedback", -1), ("stereo_off", -1)]),
    "M3": ([], [("width", -1), ("pan", -1), ("split_amt", -1), ("stereo_off", -1)]),
    "M4": (["pad-width-no-phase-smear-highband-pan-or-chord-split", "chorus-ensemble-classic-vibrato-pad-modes"], [("width", +1), ("pan_amt", +1), ("amount", +1)]),
    "M6": (["keysol-venus-high-wt-artifact-pulse-layer", "unison-odd-even-detune-width-clean-supersaw", "traveler-walkthrough-super-unison-wide-lead",
            "shimmer-reverb-pitchshift-plus12-feedback", "soft-tape-saturation-pads-before-space", "traveler-walkthrough-fx-eq-chorus-delay-reverb"], [("cutoff", +1), ("cut", +1), ("floor", +1), ("post_to", +1), ("high_db", +1), ("hi_shelf", +1), ("env_amt", +1), ("eg_amt", +1)]),
    "M7": (["keysol-venus-high-wt-artifact-pulse-layer", "unison-odd-even-detune-width-clean-supersaw", "shimmer-reverb-pitchshift-plus12-feedback",
            "traveler-walkthrough-fx-eq-chorus-delay-reverb"], [("cutoff", +1), ("cut", +1), ("mud_cut_db", +1), ("low_db", -1)]),
    "M8": (["midside-eq-bass-focus-width-depth"], [("res", -1), ("mid_cut_db", +1), ("echo_lp", -1), ("drive", -1)]),
    "M9": (["midside-eq-bass-focus-width-depth"], [("cutoff", -1), ("hi_shelf", -1), ("high_db", -1), ("res", -1)]),
    "M10": (["modulation-lfo-envelope-mod-matrix-routing", "traveler-walkthrough-control-track-filter-wt-animation"], [("lfo_amt", +1), ("cut_amt", +1), ("env_amt", +1), ("rand_amt", +1), ("depth", +1)]),
    "M11": (["modulation-lfo-envelope-mod-matrix-routing"], [("lfo_amt", +1), ("lfo_rate", +1)]),
    "M12": ([], [("noise_level", -1), ("hi_shelf", -1), ("high_db", -1)]),
    "M13": ([], [("sustain", +1), ("hold", +1)]),
    "M14": (["soft-tape-saturation-pads-before-space"], [("res", -1), ("feedback", -1), ("drive", -1)]),
    "M15": ([], [("attack", -1), ("release", +1)]),
    "M1": ([], []),
}
GATE_GUIDE = {"G5_tail_or_loopclick": [("rt60", -1), ("release", -1), ("feedback", -1), ("fb", -1), ("send", -1)],
              "G6_start": [("attack", +1)]}

def knob_space(sid):
    return REGISTRY[sid]["knobs"]

def nudge(chain, rules, rng, strength):
    changed = []
    for st in chain["steps"]:
        ks = knob_space(st["skill"])
        st.setdefault("knobs", {})
        for name, kn in ks.items():
            if name in ("mode", "layer_gain") or isinstance(kn, KC):
                continue
            for pat, d in rules:
                if pat in name:
                    cur = st["knobs"].get(name, kn.default())
                    span = kn.hi - kn.lo
                    new = kn.clamp(cur + d * span * strength * rng.uniform(0.6, 1.0))
                    if new != cur:
                        st["knobs"][name] = round(new, 4) if not isinstance(kn, KI) else new
                        changed.append(f"{st['skill'].split('-')[0]}..{name}:{cur}->{st['knobs'][name]}")
                    break
    return changed

def has(chain, sid):
    return any(s["skill"] == sid for s in chain["steps"])

def insert_skill(chain, sid, rng):
    role = REGISTRY[sid]["role"]
    pos = len(chain["steps"])
    if role in ("filter", "mod", "layer"):  # after voices, before FX
        idx = [i for i, s in enumerate(chain["steps"]) if REGISTRY[s["skill"]]["role"] in ("fx", "mix")]
        pos = idx[0] if idx else pos
    knobs = {}
    if role == "voice":
        knobs = {"mode": "layer"}
    chain["steps"].insert(pos, {"skill": sid, "knobs": knobs})

def failing(results):
    """Aggregate weakest metrics across grid renders."""
    agg = {}
    gates = {}
    for r in results:
        for m, s in r["subs"].items():
            agg[m] = min(agg.get(m, 1.0), s)
        for g, ok in r["gates"].items():
            if not ok:
                gates[g] = gates.get(g, 0) + 1
    return sorted([(s, m) for m, s in agg.items() if s < 1.0]), gates

def direction_for(metric, results, cat):
    """Infer whether value is above or below band (for two-sided metrics) to pick nudge direction."""
    from metrics import BANDS, group_of
    lo, hi = BANDS[group_of(cat)][metric]
    vals = [r["values"].get(metric) for r in results if metric in r["values"]]
    if not vals:
        return 1
    v = float(np.median(vals))
    if lo is not None and v < lo:
        return -1  # too low
    return 1   # too high

def mutate(parent, results, rng, guided):
    ch = copy.deepcopy(parent)
    ch.pop("summary", None)
    desc = []
    cat = ch["category"]
    if guided:
        fails, gates = failing(results)
        for g in gates:
            if g in GATE_GUIDE:
                desc += nudge(ch, GATE_GUIDE[g], rng, 0.4)
        for s, m in fails[:2]:
            adds, rules = GUIDE.get(m, ([], []))
            if m in ("M6", "M7", "M10", "M11", "M4") and direction_for(m, results, cat) > 0:
                rules = [(p, -d) for p, d in rules]   # too bright / too much motion / too wide: reverse
                adds = [] if m != "M4" else []
            if adds and rng.random() < 0.5:
                cand = [a for a in adds if not has(ch, a)]
                if cand:
                    a = cand[int(rng.integers(len(cand)))]
                    insert_skill(ch, a, rng); desc.append(f"+{a} (for {m})")
                    continue
            desc += [f"{m}:{c}" for c in nudge(ch, rules, rng, 0.35)]
    if not desc or not guided:
        op = rng.choice(["knob", "knob", "knob", "swap", "sub", "add", "remove"])
        steps = ch["steps"]
        if op == "knob":
            for _ in range(int(rng.integers(1, 4))):
                st = steps[int(rng.integers(len(steps)))]
                ks = knob_space(st["skill"])
                names = [n for n in ks if n not in ("mode",)]
                n = names[int(rng.integers(len(names)))]
                st.setdefault("knobs", {})[n] = ks[n].sample(rng)
                desc.append(f"knob {st['skill'].split('-')[0]}..{n}={st['knobs'][n]}")
        elif op == "swap" and len(steps) > 2:
            i = int(rng.integers(1, len(steps) - 1))
            steps[i], steps[i + 1] = steps[i + 1], steps[i]
            desc.append(f"swap {steps[i+1]['skill']}<->{steps[i]['skill']}")
        elif op == "sub":
            i = int(rng.integers(len(steps)))
            role = REGISTRY[steps[i]["skill"]]["role"]
            pool = {"voice": VOICE_POOL, "fx": FX_POOL, "mix": FX_POOL}.get(role, MOD_POOL)
            new = pool[int(rng.integers(len(pool)))]
            if not has(ch, new):
                knobs = {"mode": steps[i].get("knobs", {}).get("mode", "base")} if REGISTRY[new]["role"] == "voice" else {}
                desc.append(f"sub {steps[i]['skill']}->{new}")
                steps[i] = {"skill": new, "knobs": knobs}
        elif op == "add":
            pool = FX_POOL + MOD_POOL
            new = pool[int(rng.integers(len(pool)))]
            if not has(ch, new):
                insert_skill(ch, new, rng); desc.append(f"+{new}")
        elif op == "remove" and len(steps) > 2:
            i = int(rng.integers(1, len(steps)))
            desc.append(f"-{steps[i]['skill']}")
            steps.pop(i)
    ch["parent"] = parent.get("id")
    ch["mutation"] = "; ".join(desc) if desc else "noop"
    ch["id"] = lab.chain_hash({"c": ch["category"], "s": ch["steps"]})
    return ch

def _eval(chain):
    try:
        summary, results, _ = lab.eval_chain(chain)
        return chain, summary, results, None
    except Exception as e:
        import traceback
        return chain, None, None, traceback.format_exc()[-1500:]

def rank_key(c):
    s = c["summary"]
    return (s["reliable"], s["pass_count"], s["robust"], s["mean"])

def log(entry):
    with open(LOG, "a") as f:
        f.write(json.dumps(entry, default=str) + "\n")

def compact(results):
    out = []
    for r in results:
        bad = {m: r["values"][m] for m, s in r["subs"].items() if s < 1.0}
        badg = [g for g, ok in r["gates"].items() if not ok]
        out.append({"ns": r["noteset"], "seed": r["seed"], "score": r["score"], "pass": r["pass"], "weak": bad, "gates_failed": badg})
    return out

def run(rounds, resume, workers, per_cat_parents, children, immigrants=None):
    rng = np.random.default_rng(20261003)
    if resume and os.path.exists(POP):
        state = json.load(open(POP))
        pop, start = state["pop"], state["round"] + 1
        rng = np.random.default_rng(20261003 + start)
    else:
        seeds = json.load(open(os.path.join(LAB, "chains", "seeds.json")))
        for c in seeds:
            c["id"] = lab.chain_hash({"c": c["category"], "s": c["steps"]}); c["parent"] = None; c["mutation"] = "seed"
        pop, start = [], 0
        cands = seeds
    seen = {c["id"] for c in pop}
    for rnd in range(start, start + rounds):
        t0 = time.time()
        if rnd > 0 or (resume and pop):
            cands = []
            cats = sorted({c["category"] for c in pop})
            for cat in cats:
                ranked = sorted([c for c in pop if c["category"] == cat], key=rank_key, reverse=True)
                parents = ranked[:per_cat_parents]
                solved = ranked[0]["summary"]["reliable"]
                nchild = max(1, children - 1) if solved else children + 2
                for p in parents:
                    for j in range(nchild):
                        for _ in range(5):
                            ch = mutate(p, p["results"], rng, guided=(j % 2 == 0))
                            if ch["id"] not in seen:
                                break
                        if ch["id"] in seen:
                            continue
                        ch["name"] = p["name"]
                        seen.add(ch["id"]); cands.append(ch)
        if immigrants and rnd == start:
            for c in json.load(open(immigrants)):
                c["id"] = lab.chain_hash({"c": c["category"], "s": c["steps"]}); c["parent"] = None; c["mutation"] = "immigrant seed"
                if c["id"] not in seen:
                    seen.add(c["id"]); cands.append(c)
        with Pool(workers) as pool:
            out = pool.map(_eval, cands, chunksize=1)
        n_ok = 0
        for chain, summary, results, err in out:
            entry = {"round": rnd, "id": chain["id"], "name": chain["name"], "category": chain["category"], "parent": chain.get("parent"),
                     "mutation": chain.get("mutation"), "steps": chain["steps"]}
            if err:
                entry["error"] = err
                log(entry); print("ERR", chain["name"], err[-300:]); continue
            entry.update(summary=summary, renders=compact(results))
            log(entry)
            chain["summary"], chain["results"] = summary, compact_full(results)
            pop.append(chain)
            n_ok += summary["reliable"]
        # keep population bounded: top 4 per category
        newpop = []
        for cat in sorted({c["category"] for c in pop}):
            newpop += sorted([c for c in pop if c["category"] == cat], key=rank_key, reverse=True)[:4]
        pop = newpop
        json.dump({"round": rnd, "pop": pop}, open(POP, "w"), default=str)
        rel = [c for c in pop if c["summary"]["reliable"]]
        print(f"round {rnd}: evaluated {len(cands)} in {time.time()-t0:.0f}s; new reliable {n_ok}; "
              f"reliable in pop {len(rel)} ({sorted({c['category'] for c in rel})})", flush=True)
        for cat in sorted({c["category"] for c in pop}):
            b = sorted([c for c in pop if c["category"] == cat], key=rank_key, reverse=True)[0]
            print(f"   {cat:6s} best {b['name']:30s} {b['id']} robust={b['summary']['robust']} mean={b['summary']['mean']} pass={b['summary']['pass_count']}/6", flush=True)

def compact_full(results):
    return [{"values": r["values"], "subs": r["subs"], "gates": r["gates"], "score": r["score"], "pass": r["pass"], "noteset": r["noteset"], "seed": r["seed"]} for r in results]

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--rounds", type=int, default=1)
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--parents", type=int, default=2)
    ap.add_argument("--children", type=int, default=3)
    ap.add_argument("--immigrants")
    a = ap.parse_args()
    run(a.rounds, a.resume, a.workers, a.parents, a.children, a.immigrants)
