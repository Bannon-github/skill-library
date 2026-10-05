"""Evaluate workflow chains on the test grid (3 notesets x 2 seeds) per TARGET.md."""
import json, os, sys, time, hashlib
import numpy as np
import soundfile as sf
import render, metrics, skills
from dsp import SR

LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEEDS = [11, 23]

def note_off_s(cat):
    return {"pad": 6.0, "swell": 6.0, "bass": 5.0, "pluck": 5.6, "drone": 14.5, "gated": 14.5}[cat]

def render_chain(chain, notes, seed):
    patch = skills.build_patch(chain)
    cat = chain["category"]
    audio, info = render.render(patch, notes, seed)
    return audio, info, patch

def eval_one(chain, ni, seed, check_det=False):
    cat = chain["category"]
    notes = render.NOTESETS[cat][ni]
    audio, info, patch = render_chain(chain, notes, seed)
    is_loop = cat in ("drone", "gated")
    body0 = 0.15 * note_off_s(cat) if cat != "pluck" else 0.0
    res = metrics.compute(audio, info, cat, is_loop, note_off_s(cat), start_body_s=body0,
                          f_low=render.note_to_hz(min(notes)), bar_s=render.sync_s('1bar'))
    if check_det:
        a2, _, _ = render_chain(chain, notes, seed)
        same = bool(np.array_equal(audio, a2))
        res["gates"]["G4_determinism"] = same
        if not same:
            res["pass"] = False
    return audio, res

def eval_chain(chain, grid=None, check_det=True, keep_audio=False):
    grid = grid or [(ni, s) for ni in range(3) for s in SEEDS]
    results, audios = [], []
    for j, (ni, s) in enumerate(grid):
        audio, r = eval_one(chain, ni, s, check_det=(check_det and j == 0))
        r["noteset"], r["seed"] = ni, s
        results.append(r)
        if keep_audio:
            audios.append(audio)
    scores = [r["score"] for r in results]
    summary = {"robust": round(min(scores), 2), "mean": round(float(np.mean(scores)), 2),
               "pass_count": sum(r["pass"] for r in results), "n": len(results),
               "reliable": all(r["pass"] for r in results)}
    return summary, results, audios

def chain_hash(chain):
    return hashlib.sha1(json.dumps(chain, sort_keys=True, default=str).encode()).hexdigest()[:10]

def write_wav(path, audio):
    sf.write(path, audio.astype(np.float32), SR, subtype="PCM_24")

def spectrogram(path, audio, title):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from scipy import signal
    M = 0.5 * (audio[:, 0] + audio[:, 1]); S = 0.5 * (audio[:, 0] - audio[:, 1])
    fig, axs = plt.subplots(2, 1, figsize=(11, 6.5), sharex=True)
    for ax, x, nm in ((axs[0], M, "Mid"), (axs[1], S, "Side")):
        f, t, Z = signal.spectrogram(x, SR, nperseg=2048, noverlap=1536)
        Zd = 10 * np.log10(Z + 1e-14)
        ax.pcolormesh(t, f, Zd, vmin=Zd.max() - 90, vmax=Zd.max(), shading="auto", cmap="magma")
        ax.set_yscale("symlog", linthresh=200); ax.set_ylim(30, 24000); ax.set_ylabel(f"{nm} Hz")
    axs[0].set_title(title); axs[1].set_xlabel("s")
    fig.tight_layout(); fig.savefig(path, dpi=80); plt.close(fig)
