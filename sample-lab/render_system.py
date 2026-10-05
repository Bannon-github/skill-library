#!/usr/bin/env python3
"""Render a saved Sample Lab system by name.

  ./render_system.py --list
  ./render_system.py <system-name> [--notes 50,53,57,64] [--seed 11] [--out DIR] [--score] [--spectrogram]
  ./render_system.py <system-name> --grid          # full TARGET.md test grid (3 note sets x 2 seeds) with scores

Systems live in systems/<name>/chain.json (ordered skill chain + knob values). Output: 48 kHz/24-bit stereo WAV.
Run with the lab venv:  .venv/bin/python render_system.py ...
"""
import argparse, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "engine"))
import lab, render, metrics  # noqa: E402

def load(name):
    p = os.path.join(HERE, "systems", name, "chain.json")
    if not os.path.exists(p):
        sys.exit(f"no system '{name}'. Try --list")
    return json.load(open(p))

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("name", nargs="?")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--notes", help="comma-separated MIDI notes (default: the category's first test note set)")
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--out", default=os.path.join(HERE, "renders"))
    ap.add_argument("--score", action="store_true")
    ap.add_argument("--spectrogram", action="store_true")
    ap.add_argument("--grid", action="store_true")
    a = ap.parse_args()
    if a.list or not a.name:
        for n in sorted(os.listdir(os.path.join(HERE, "systems"))):
            p = os.path.join(HERE, "systems", n, "chain.json")
            if os.path.exists(p):
                c = json.load(open(p))
                print(f"{n:34s} {c['category']:6s} " + " -> ".join(s['skill'] for s in c['steps']))
        return
    chain = load(a.name)
    os.makedirs(a.out, exist_ok=True)
    if a.grid:
        summary, results, audios = lab.eval_chain(chain, keep_audio=True)
        print(json.dumps(summary))
        for r, au in zip(results, audios):
            fn = os.path.join(a.out, f"{a.name}__ns{r['noteset']}_seed{r['seed']}.wav")
            lab.write_wav(fn, au)
            print(f"{fn}  score={r['score']} pass={r['pass']}")
        return
    cat = chain["category"]
    notes = [int(x) for x in a.notes.split(",")] if a.notes else render.NOTESETS[cat][0]
    import skills
    patch = skills.build_patch(chain)
    audio, info = render.render(patch, notes, a.seed)
    tag = "-".join(map(str, notes))
    fn = os.path.join(a.out, f"{a.name}__{tag}_seed{a.seed}.wav")
    lab.write_wav(fn, audio)
    print(fn)
    if a.spectrogram:
        lab.spectrogram(fn[:-4] + ".png", audio, f"{a.name} {tag} seed {a.seed}")
        print(fn[:-4] + ".png")
    if a.score:
        is_loop = cat in ("drone", "gated")
        r = metrics.compute(audio, info, cat, is_loop, lab.note_off_s(cat), start_body_s=0.15 * lab.note_off_s(cat) if cat != "pluck" else 0.0,
                            f_low=render.note_to_hz(min(notes)), bar_s=render.sync_s("1bar"))
        print(json.dumps({"score": r["score"], "pass": r["pass"], "values": r["values"], "gates": r["gates"]}, indent=1))

if __name__ == "__main__":
    main()
