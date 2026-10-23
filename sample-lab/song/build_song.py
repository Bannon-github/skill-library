#!/usr/bin/env python3
"""Generic song-structure engine for the Sample Lab.

Reads a song recipe (JSON, see sample-lab/workflows/song-*.json) whose *section map* says, per section: bars, tempo,
chord loop, which layers play (gain / ramp / low-pass sweep), drums, melody motif and the transition into the next
section.  For every (layer, chord/phrase) it renders a clip with the existing Sample Lab renderers (systems/<name>/chain.json
through engine/render.py), places the clips on a bar grid, automates layer gains with cosine cross-fades, adds
transitions (riser, reverse-reverb swell, sub drop, impact, silence gap, low-end cut, snare roll, whoosh/downlifter),
then finalises (mono lows, loudness, true-peak limiter) and measures it against the planned section/energy map and
the applicable TARGET.md gates.

  python build_song.py --validate recipe.json            # parse + every skill id / system exists
  python build_song.py recipe.json out.wav [--workers 8] # render + stats (out.wav.stats.json)

Reuses: isochronic/render_flow_state_v2.py (ease(), riser = resonant SVF sweep + detuned saw, reverse-reverb swell via
IR convolution, sub-drop sine glide, mono-lows side HP, true-peak + flux measurement) and
boreal-stems/build_stems.py (clip-per-chord rendering through render.render with a patched schedule, circular add).
Original synthesis only; no samples or presets. Metrics measure deliverability and planned-curve fit, not taste."""
import sys, os, json, hashlib, re, time, glob
import numpy as np, soundfile as sf, pyloudnorm as pyln
from numpy.fft import rfft, irfft, rfftfreq
from scipy import signal as sg
from concurrent.futures import ProcessPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.environ.get("LAB", os.path.dirname(HERE))
LIB = os.path.dirname(LAB)
sys.path.insert(0, LAB + "/engine")
SR = 48000
CACHE = os.environ.get("SONG_CACHE", "/workspace/song-cache")
f32 = np.float32
db = lambda x: 10 ** (np.asarray(x, float) / 20)

# ------------------------------------------------------------------ validation
def skill_ids():
    ids = {os.path.basename(p)[:-5] for p in glob.glob(LIB + "/mcp-publish/skills/*.json")}
    return ids

def collect_skill_ids(obj, out):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("skillIds", "skills") and isinstance(v, list):
                for x in v:
                    if isinstance(x, str): out.add(x)
                    elif isinstance(x, dict) and "id" in x: out.add(x["id"])
            else: collect_skill_ids(v, out)
    elif isinstance(obj, list):
        for v in obj: collect_skill_ids(v, out)

def validate(R, quiet=False):
    errs = []; ids = skill_ids(); used = set(); collect_skill_ids(R, used)
    for s in sorted(used):
        if s not in ids: errs.append(f"skill id not in library: {s}")
    layers = R.get("layers", {})
    for n, L in layers.items():
        if L["kind"] in ("chords", "melody") and not os.path.exists(f"{LAB}/systems/{L['system']}/chain.json"):
            errs.append(f"layer {n}: system {L['system']} missing")
        if L["kind"] == "chords" and False: pass
        if L["kind"] in ("chords", "melody"):
            ch = json.load(open(f"{LAB}/systems/{L['system']}/chain.json"))
            for st in ch["steps"]:
                if st["skill"] not in ids: errs.append(f"layer {n}: chain skill {st['skill']} not in library")
        if L["kind"] == "file" and not os.path.exists(os.path.expandvars(L["path"].replace("$LAB", LAB))):
            errs.append(f"layer {n}: file missing {L['path']}")
    for sec in R["sections"]:
        for ln in (sec.get("layers") or {}):
            if ln not in layers: errs.append(f"section {sec['name']}: unknown layer {ln}")
        if sec.get("chords") and sec["chords"] not in R["chordLoops"]: errs.append(f"section {sec['name']}: unknown chord loop")
        m = sec.get("melody")
        if m and m["motif"] not in R["motifs"]: errs.append(f"section {sec['name']}: unknown motif {m['motif']}")
    bars = sum(s["bars"] for s in R["sections"])
    if R.get("totalBars") and R["totalBars"] != bars: errs.append(f"totalBars {R['totalBars']} != sum of sections {bars}")
    if not quiet:
        print(f"{R['id']}: sections={len(R['sections'])} bars={bars} skillIds={len(used)} layers={len(layers)} -> " + ("OK" if not errs else "ERRORS"))
        for e in errs: print("  ", e)
    return errs, used

# ------------------------------------------------------------------ clip rendering (worker side)
_PATCH = {}
def render_clip(task):
    import render, skills
    sysname = task["system"]
    if sysname not in _PATCH:
        chain = json.load(open(f"{LAB}/systems/{sysname}/chain.json")); _PATCH[sysname] = (chain, skills.build_patch(chain))
    chain, patch = _PATCH[sysname]
    patch = json.loads(json.dumps(patch)) if task.get("gateFloorDb") is not None else patch
    if task.get("gateFloorDb") is not None:
        for fx in patch["fx"]:
            if fx.get("type") == "gate": fx["floor_db"] = task["gateFloorDb"]
    cat = chain["category"]; render.BPM = float(task["bpm"]); render.TOTAL[cat] = task["total"]
    ev = [tuple(e) for e in task["events"]]
    render.schedule = lambda c, nn, ev=ev: ev
    audio, _ = render.render(patch, sorted({e[0] for e in ev}), task["seed"], loop=False)
    return audio.astype(f32)

def task_key(t): return hashlib.sha1(json.dumps(t, sort_keys=True).encode()).hexdigest()[:16]

def run_clips(tasks, workers):
    os.makedirs(CACHE, exist_ok=True); out = {}; todo = {}
    for t in tasks:
        k = task_key(t); p = f"{CACHE}/{k}.npy"
        if os.path.exists(p): out[k] = p
        else: todo[k] = t
    print(f"clips: {len(tasks)} placed, {len(set(map(task_key, tasks)))} unique, {len(todo)} to render", flush=True)
    if todo:
        with ProcessPoolExecutor(workers) as ex:
            for (k, t), a in zip(todo.items(), ex.map(render_clip, todo.values())):
                np.save(f"{CACHE}/{k}.npy", a); out[k] = f"{CACHE}/{k}.npy"
    return out

# ------------------------------------------------------------------ small DSP helpers
def ease(points, tt, db_mode=True):
    p = np.array([(a, (-200 if v is None else v)) for a, v in points], float)
    order = np.argsort(p[:, 0], kind="stable"); p = p[order]
    xs = p[:, 0] + np.arange(len(p)) * 1e-6; ys = p[:, 1]
    if db_mode: ys = np.where(ys <= -120, 0.0, 10 ** (ys / 20))
    if len(xs) == 1: return np.full(len(tt), ys[0])
    i = np.clip(np.searchsorted(xs, tt, side="right") - 1, 0, len(xs) - 2)
    u = np.clip((tt - xs[i]) / (xs[i + 1] - xs[i]), 0, 1); e = 0.5 - 0.5 * np.cos(np.pi * u)
    return ys[i] + (ys[i + 1] - ys[i]) * e

def fft_lp(x, hz, order=2):
    F = rfft(x, axis=0); f = rfftfreq(len(x), 1 / SR)
    F *= (1 / np.sqrt(1 + (f / hz) ** (2 * order)))[:, None]; return irfft(F, len(x), axis=0)

def fft_hp(x, hz, order=2):
    F = rfft(x, axis=0); f = rfftfreq(len(x), 1 / SR)
    F *= (1 / np.sqrt(1 + (hz / np.maximum(f, 1e-3)) ** (2 * order)))[:, None]; return irfft(F, len(x), axis=0)

def conv(x, ir):
    n = len(x) + len(ir) - 1; M = 1 << (n - 1).bit_length(); return irfft(rfft(x, M) * rfft(ir, M), M)[:n]

def make_ir(sec, rng, lp=3500):
    n = int(sec * SR); tt = np.arange(n) / SR; ir = rng.standard_normal(n) * np.exp(-tt * 6.9 / sec)
    F = rfft(ir); ff = rfftfreq(n, 1 / SR); F /= 1 + (ff / lp) ** 2; ir = irfft(F, n); return ir / np.abs(ir).sum() * 8

def tp_db(x, ch=480000):
    m = 0.0
    for c in range(x.shape[1]):
        for a in range(0, len(x), ch):
            seg = x[max(0, a - 2400):a + ch + 2400, c].astype(np.float64); F = rfft(seg)
            m = max(m, np.abs(irfft(np.concatenate([F, np.zeros(3 * len(F), complex)]), 4 * len(seg)) * 4).max())
    return 20 * np.log10(m + 1e-12)

# ------------------------------------------------------------------ built-in drum voices (original synthesis; no library skill covers drums)
def _bp(x, lo, hi, order=2): return sg.sosfilt(sg.butter(order, [lo, hi], "bandpass", fs=SR, output="sos"), x)
def _hp(x, f, order=4): return sg.sosfilt(sg.butter(order, f, "highpass", fs=SR, output="sos"), x)
def _lp(x, f, order=2): return sg.sosfilt(sg.butter(order, f, "lowpass", fs=SR, output="sos"), x)

def make_drums():
    r = np.random.default_rng(7); D = {}
    t = np.arange(int(0.5 * SR)) / SR; fr = 46 + 120 * np.exp(-t / 0.03); ph = 2 * np.pi * np.cumsum(fr) / SR
    k = np.sin(ph) * np.exp(-t / 0.15) * np.minimum(1, t / 0.002) + 0.35 * _bp(r.standard_normal(len(t)), 1500, 6000) * np.exp(-t / 0.004)
    k *= np.minimum(1, (len(t) - np.arange(len(t))) / 480); D["kick"] = k / np.abs(k).max()
    n = int(0.45 * SR); t = np.arange(n) / SR; z = _bp(r.standard_normal(n), 900, 7000)
    env = sum(np.exp(-np.clip(t - d, 0, None) / 0.012) * (t >= d) for d in (0, 0.011, 0.022)) * 0.6 + np.exp(-np.clip(t - 0.03, 0, None) / 0.11) * (t >= 0.03)
    c = z * env; D["clap"] = c / np.abs(c).max()
    n = int(0.35 * SR); t = np.arange(n) / SR
    s = _bp(r.standard_normal(n), 1200, 9000) * np.exp(-t / 0.09) + np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.05) * 0.8; D["snare"] = s / np.abs(s).max()
    n = int(0.12 * SR); t = np.arange(n) / SR; h = _lp(_hp(r.standard_normal(n), 6500), 14000) * np.exp(-t / 0.025); D["hat"] = h / np.abs(h).max()
    n = int(0.5 * SR); t = np.arange(n) / SR; h = _lp(_hp(r.standard_normal(n), 6000), 14000) * np.exp(-t / 0.12); D["ohat"] = h / np.abs(h).max()
    n = int(0.2 * SR); t = np.arange(n) / SR; h = _bp(r.standard_normal(n), 4000, 11000) * np.minimum(1, t / 0.012) * np.exp(-t / 0.05); D["shaker"] = h / np.abs(h).max()
    n = int(0.15 * SR); t = np.arange(n) / SR; h = (np.sin(2 * np.pi * 1750 * t) * np.exp(-t / 0.012) + 0.4 * _bp(r.standard_normal(n), 2000, 8000) * np.exp(-t / 0.006)); D["rim"] = h / np.abs(h).max()
    return D

PATTERNS = {"off": "." * 16, "four": "x...x...x...x...", "half": "x.......x.......", "eighth": "x.x.x.x.x.x.x.x.", "sixteenth": "x" * 16,
            "backbeat": "....x.......x...", "offbeat": "..x...x...x...x.", "eighth_hat": "x.x.x.x.x.x.x.x.", "sixteenth_hat": "xoxoxoxoxoxoxoxo",
            "shaker16": "o.o.o.o.o.o.o.o.", "rim_sparse": "x.......o.......", "kick_pop": "x.......x.x.....", "snare_roll8": "x.x.x.x.x.x.x.x."}
VEL = {"x": 0.85, "X": 1.0, "o": 0.45, ".": 0.0}

def drum_track(sec_spec, start_s, bars, bpm, D, N, levels, rng):
    """returns (stereo buffer region dict) -> list of (name, t_start, vel)"""
    hits = []; bar_s = 4 * 60 / bpm; step = bar_s / 16
    dr = sec_spec.get("drums") or {}
    by = dr.get("byBar", {})
    for voice, pat in dr.items():
        if voice in ("byBar", "stopAtBeat", "swing", "levelDb", "skillIds"): continue
        for b in range(bars):
            p = (by.get(voice) or [None] * bars)[b] if voice in by and b < len(by[voice]) else None
            p = PATTERNS.get(p or pat, p or pat)
            for i, ch in enumerate(p[:16]):
                v = VEL.get(ch, 0.0)
                if v > 0: hits.append((voice, start_s + b * bar_s + i * step + (step * dr.get("swing", 0.0) if i % 2 else 0.0), v))
    stop = dr.get("stopAtBeat")
    if stop is not None: hits = [h for h in hits if h[1] < start_s + stop * 60 / bpm]
    return hits

# ------------------------------------------------------------------ main build
def build(R, out_path, workers=8):
    t0 = time.time(); seed = R["seed"]; rng = np.random.default_rng(seed)
    errs, used = validate(R)
    if errs: sys.exit("recipe invalid")
    secs = R["sections"]; layers = R["layers"]; D = make_drums()
    # ---- timeline
    t = 0.0; T = []
    for s in secs:
        bpm = s.get("bpm", R["bpm"]); bar = 4 * 60 / bpm; T.append(dict(start=t, bars=s["bars"], bpm=bpm, bar=bar, end=t + s["bars"] * bar)); t += s["bars"] * bar
    body_s = t; tail_s = R.get("tailSec", 4.0); total_s = body_s + tail_s; N = int(total_s * SR); tt = np.arange(N) / SR
    # ---- clip tasks
    placements = []   # (layer, key-task, start_s, sectionIndex)
    tasks = []
    for si, (s, tm) in enumerate(zip(secs, T)):
        tr = s.get("transpose", 0)
        # chords
        if s.get("chords"):
            loop = R["chordLoops"][s["chords"]]; b = 0; i = s.get("chordStart", 0)
            while b < s["bars"]:
                ch = loop[i % len(loop)]; nb = min(ch["bars"], s["bars"] - b)
                for ln, L in layers.items():
                    if L["kind"] != "chords" or (s.get("layers") or {}).get(ln, None) is None: continue
                    notes = [n + tr + 12 * L.get("octave", 0) for n in ch["voices"][L["voice"]]]
                    bar_s = tm["bar"]; hold = nb * bar_s; ev = []
                    if L.get("rhythm"):
                        k = 0
                        for bb in range(nb):
                            for (beat, dur, vel) in L["rhythm"]:
                                st = bb * bar_s + beat * 60 / tm["bpm"]
                                if L.get("arp"):
                                    n_ = len(notes); cyc = list(range(n_)) if L["arp"] == "up" else list(range(n_)) + list(range(n_ - 2, 0, -1))
                                    pick = [notes[cyc[k % len(cyc)]]]; k += 1
                                else: pick = notes
                                ev += [(m, st, dur * 60 / tm["bpm"], vel) for m in pick]
                    else:
                        ev = [(m, 0.0, hold + L.get("overhang", 0.3), L.get("vel", 0.85)) for m in notes]
                    task = dict(system=L["system"], events=[[int(m), round(a, 4), round(d, 4), round(v, 3)] for m, a, d, v in ev], total=round(hold + L.get("tailSec", 5.0), 3),
                                bpm=tm["bpm"], seed=seed + L.get("seedOff", 0), gateFloorDb=L.get("gateFloorDb"))
                    tasks.append(task); placements.append((ln, task, tm["start"] + b * bar_s, si, nb))
                b += nb; i += 1
        # melody
        m = s.get("melody")
        if m:
            mo = R["motifs"][m["motif"]]; L = layers[m["layer"]]; tm_ = tm; pb = mo["bars"]
            b = m.get("startBar", 0); endb = m.get("endBar", s["bars"])
            while b + 0 < endb:
                nb = min(pb, endb - b)
                ev = [(n + tr + m.get("transpose", 0) + 12 * L.get("octave", 0), beat * 60 / tm["bpm"], dur * 60 / tm["bpm"], min(1.0, vel * m.get("velScale", 1.0)))
                      for beat, n, dur, vel in mo["notes"] if beat < nb * 4]
                task = dict(system=L["system"], events=[[int(a), round(b_, 4), round(d, 4), round(v, 3)] for a, b_, d, v in ev], total=round(nb * tm["bar"] + L.get("tailSec", 5.0), 3),
                            bpm=tm["bpm"], seed=seed + L.get("seedOff", 0), gateFloorDb=L.get("gateFloorDb"))
                tasks.append(task); placements.append((m["layer"], task, tm["start"] + b * tm["bar"], si, nb)); b += nb
    keys = run_clips(tasks, workers)
    # ---- determinism check (TARGET G4) on one clip
    g4 = True
    if tasks:
        a1 = np.load(keys[task_key(tasks[0])]); a2 = render_clip(tasks[0]); g4 = bool(np.array_equal(a1, a2))
    # ---- layer buffers
    buf = {ln: np.zeros((N, 2), f32) for ln in layers if layers[ln]["kind"] in ("chords", "melody")}
    first_clip = {}   # (layer, section) -> clip for reverse swell source
    for ln, task, st, si, nb in placements:
        a = np.load(keys[task_key(task)]); s0 = int(round(st * SR)); e = min(N, s0 + len(a)); buf[ln][s0:e] += a[:e - s0]
        first_clip.setdefault((ln, si), a)
    # file layers (looped stems), noise layers
    for ln, L in layers.items():
        if L["kind"] == "file":
            x, sr0 = sf.read(os.path.expandvars(L["path"].replace("$LAB", LAB)), dtype="float32")
            if sr0 != SR: x = np.stack([sg.resample_poly(x[:, c], SR, sr0) for c in range(2)], 1).astype(f32)
            reps = int(np.ceil(N / len(x))); buf[ln] = np.tile(x, (reps, 1))[:N].copy()
        elif L["kind"] == "noise":
            nz = np.zeros((N, 2), f32); f = rfftfreq(N, 1 / SR)
            for c in range(2):
                F = rfft(rng.standard_normal(N)); F /= np.sqrt(np.maximum(f, 20)); F /= 1 + (f / L.get("lpHz", 1500)) ** 2; nz[:, c] = irfft(F, N)
            nz /= np.abs(nz).max(); pan = 0.5 + 0.4 * np.sin(2 * np.pi * tt / L.get("panPeriodSec", 40)); nz[:, 0] *= np.cos(0.5 * np.pi * pan); nz[:, 1] *= np.sin(0.5 * np.pi * pan)
            buf[ln] = nz * f32(0.3)
    # ---- drums + kick envelope
    drum_hits = []
    for si, (s, tm) in enumerate(zip(secs, T)):
        if s.get("drums"): drum_hits += [(v, ts, vel, si) for v, ts, vel in drum_track(s, tm["start"], s["bars"], tm["bpm"], D, N, None, rng)]
    # transitions: snare roll (adds to drum hits)
    for si, (s, tm) in enumerate(zip(secs, T)):
        for tr_ in s.get("transitions", []):
            if tr_["type"] == "snare_roll":
                nb = tr_.get("bars", 1); t_end = tm["end"] - tr_.get("gapBeats", 0) * 60 / tm["bpm"]; t_st = tm["end"] - nb * tm["bar"]; ts = t_st; k = 0
                while ts < t_end - 1e-6:
                    u = (ts - t_st) / (t_end - t_st); div = 8 if u < 0.5 else (16 if u < 0.8 else 32)
                    drum_hits.append((tr_.get("voice", "snare"), ts, 0.35 + 0.65 * u, si)); ts += 4 * 60 / tm["bpm"] / div
    dbus = np.zeros((N, 2), f32); kick_t = []
    for voice, ts, vel, si in drum_hits:
        lv = db((secs[si].get("drums") or {}).get("levelDb", {}).get(voice, R.get("drumLevelDb", {}).get(voice, -6)))
        a = int(round(ts * SR)); w = D[voice]; e = min(N, a + len(w))
        if a >= N: continue
        pan = {"shaker": 0.25, "hat": -0.15, "ohat": 0.15, "rim": -0.2}.get(voice, 0.0); gl, gr = np.cos((pan + 1) * np.pi / 4) * 1.414, np.sin((pan + 1) * np.pi / 4) * 1.414
        dbus[a:e, 0] += w[:e - a] * vel * lv * gl; dbus[a:e, 1] += w[:e - a] * vel * lv * gr
        if voice == "kick": kick_t.append(ts)
    sc_env = np.ones(N)   # sidechain duck curve from the actual kick positions
    sc_env = np.ones(N)
    for ts in kick_t:
        a = int(ts * SR); n = int(0.45 * SR); e = min(N, a + n)
        if a < N:
            u = np.arange(e - a) / SR; sc_env[a:e] = np.minimum(sc_env[a:e], 1 - np.exp(-u / 0.12))   # 0 at the kick, recovers over ~0.35 s
    # ---- per-layer lp sweeps and gain automation
    levels_rms = {}; bed = np.zeros((N, 2), f32)
    import dsp
    for ln, L in layers.items():
        x = buf.get(ln)
        if x is None: continue
        if L.get("hpHz"): x = fft_hp(x, L["hpHz"]).astype(f32)
        if L.get("lpHz"): x = fft_lp(x, L["lpHz"], L.get("lpOrder", 2)).astype(f32)
        nodes = []
        for si, (s, tm) in enumerate(zip(secs, T)):
            spec = (s.get("layers") or {}).get(ln, None)
            d0, d1 = (None, None)
            if isinstance(spec, dict): d0 = spec["db"]; d1 = spec.get("toDb", d0)
            elif spec is not None: d0 = d1 = spec
            xf = s.get("xfadeSec", R.get("xfadeSec", 1.5)) if si > 0 else 0.0
            nodes.append((tm["start"] + xf / 2, d0))
            nodes.append((tm["end"] - (secs[si + 1].get("xfadeSec", R.get("xfadeSec", 1.5)) / 2 if si + 1 < len(secs) else 0.0), d1))
            if isinstance(spec, dict) and spec.get("lp"):
                a, e = int(tm["start"] * SR), int(tm["end"] * SR); fc = np.exp(np.interp(np.arange(e - a) / (e - a), [0, 1], np.log(spec["lp"])))
                for c in range(2): x[a:e, c] = dsp.svf(x[a:e, c].astype(np.float64), fc, 0.707, 0, SR).astype(f32)
        nodes.append((total_s, nodes[-1][1]))
        g = ease(nodes, tt).astype(f32)
        if L.get("sidechainDb"): g = g * (1 - (1 - sc_env) * (1 - 10 ** (-L["sidechainDb"] / 20))).astype(f32)
        x = x * g[:, None] * f32(db(L.get("levelDb", 0))); levels_rms[ln] = float(np.sqrt((x ** 2).mean() + 1e-20)); bed += x; buf[ln] = None
    levels_rms["drums"] = float(np.sqrt((dbus ** 2).mean() + 1e-20)); bed += dbus * f32(db(R.get("drumBusDb", 0)))
    # ---- transitions (bus FX)
    def region_rms(a_s, b_s):
        a, b = max(0, int(a_s * SR)), min(N, int(b_s * SR)); return float(np.sqrt((bed[a:b] ** 2).mean() + 1e-20))
    def place(sig, start, gain=1.0):
        a = int(start * SR); e = min(N, a + len(sig))
        if a < N: bed[a:e] += (sig[:e - a] * gain).astype(f32)
    gaps = []; lowcuts = []; tlog = []
    for si, (s, tm) in enumerate(zip(secs, T)):
        for k_, tr_ in enumerate(s.get("transitions", [])):
            ty = tr_["type"]; ref = region_rms(tm["end"] - 4 * tm["bar"], tm["end"]); r2 = np.random.default_rng(seed * 100 + si * 10 + k_)
            if ty == "riser":
                Lr = int(tr_["bars"] * tm["bar"] * SR); trs = np.arange(Lr) / SR; u = trs / (Lr / SR); curve = u ** tr_.get("curve", 2.2)
                nzr = r2.standard_normal(Lr); fcs = tr_.get("fHz", [250, 3800]); fcv = fcs[0] + (fcs[1] - fcs[0]) * curve
                pk = dsp.svf(nzr, fcv, tr_.get("q", 2.5), 1, SR); pk = pk / (np.abs(pk).max() + 1e-12) * curve
                saw = sum((2 * ((trs * tr_.get("sawHz", 65.41) * (2 ** (c / 1200))) % 1) - 1) for c in (-9, 0, 9)) / 3; saw = np.convolve(saw, np.ones(60) / 60, "same") * curve * 0.35
                mono = pk + saw * tr_.get("sawAmt", 1.0); pan = u; ris = np.stack([mono * np.cos(0.5 * np.pi * pan), mono * np.sin(0.5 * np.pi * pan)], 1)
                ris *= np.minimum(1, (Lr - np.arange(Lr)) / int(0.01 * SR))[:, None]
                place(ris, tm["end"] - Lr / SR, ref * db(tr_.get("gainDb", -8)) / (np.sqrt((ris ** 2).mean()) + 1e-9)); tlog.append((tm["end"], ty))
                if tr_.get("tailSec"):
                    ir = make_ir(tr_["tailSec"], r2); tail = np.stack([conv(ris[:, c], ir) for c in range(2)], 1)[Lr:]
                    tail *= np.minimum(1, np.arange(len(tail)) / (0.6 * SR))[:, None]
                    place(tail, tm["end"], ref * db(tr_.get("gainDb", -8) - 4) / (np.sqrt((ris ** 2).mean()) + 1e-9))
            elif ty == "reverse_swell":
                nxt = si + 1; src = first_clip.get((tr_["source"], nxt))
                if src is None: continue
                src = src[int(tr_.get("trim", [0.3, 4.3])[0] * SR):int(tr_.get("trim", [0.3, 4.3])[1] * SR)]; src = fft_lp(src, tr_.get("lpHz", 1800)).astype(np.float64)
                ir = make_ir(tr_.get("irSec", 5.0), r2, 3000); sw = np.stack([conv(src[::-1, c], ir)[::-1] for c in range(2)], 1)[:len(ir)]
                sw *= np.sin(0.5 * np.pi * np.minimum(1, np.arange(len(sw)) / (0.8 * tr_.get("irSec", 5.0) * SR)))[:, None] ** 2; sw[-int(0.02 * SR):] *= np.linspace(1, 0, int(0.02 * SR))[:, None]
                sw *= 1.0 / np.abs(sw).max() * ref * db(tr_.get("gainDbRel", -3)) * 3; place(sw, tm["end"] - len(sw) / SR); tlog.append((tm["end"], ty))
            elif ty in ("sub_drop", "impact"):
                Ls = int(tr_.get("lengthSec", 5) * SR); ts_ = np.arange(Ls) / SR; hz = tr_.get("hz", [72, 24]); fq = hz[0] * (hz[1] / hz[0]) ** (ts_ / (Ls / SR))
                sine = np.sin(2 * np.pi * np.cumsum(fq) / SR) * np.minimum(1, ts_ / 0.02) * np.minimum(1, ((Ls / SR) - ts_) / 1.5)
                sig = np.stack([sine, sine], 1) * 1.4
                if ty == "impact":
                    n = int(tr_.get("noiseSec", 3.0) * SR); tn = np.arange(n) / SR; nz = _lp(_hp(r2.standard_normal(n), 600), 9000) * np.exp(-tn / (tr_.get("noiseSec", 3.0) / 4)) * 0.5
                    sig[:n] += np.stack([nz, nz[::-1]], 1) * 0.6 if n <= Ls else 0
                place(sig, tm["end"] + tr_.get("offsetSec", 0.0), ref * db(tr_.get("gainDb", -10))); tlog.append((tm["end"], ty))
            elif ty == "whoosh":
                n = int(tr_.get("sec", 2.0) * SR); u = np.arange(n) / n; fcv = 400 * (6000 / 400) ** (u if tr_.get("dir", "up") == "up" else 1 - u)
                w = dsp.svf(r2.standard_normal(n), fcv, 1.5, 1, SR); w = w / (np.abs(w).max() + 1e-12) * np.sin(np.pi * u) ** 2
                place(np.stack([w, w[::-1]], 1), tm["end"] - (n / SR if tr_.get("dir", "up") == "up" else 0), ref * db(tr_.get("gainDb", -20)) / (np.sqrt((w ** 2).mean()) + 1e-9)); tlog.append((tm["end"], ty))
            elif ty == "downlifter":
                n = int(tr_.get("sec", 3.0) * SR); u = np.arange(n) / n; fcv = 7000 * (200 / 7000) ** u
                w = dsp.svf(r2.standard_normal(n), fcv, 1.0, 0, SR); w = w / (np.abs(w).max() + 1e-12) * (1 - u) ** 1.5
                place(np.stack([w, w[::-1]], 1), tm["end"], ref * db(tr_.get("gainDb", -14)) / (np.sqrt((w ** 2).mean()) + 1e-9)); tlog.append((tm["end"], ty))
            elif ty == "gap":
                gaps.append((tm["end"] - tr_["beats"] * 60 / tm["bpm"], tm["end"], tr_.get("floorDb", -60))); tlog.append((tm["end"], ty))
            elif ty == "lowcut":
                lowcuts.append((tm["end"] - tr_["bars"] * tm["bar"], tm["end"], tr_.get("hz", [30, 400]))); tlog.append((tm["end"], ty))
    for a_s, e_s, hz in lowcuts:
        a, e = int(a_s * SR), int(e_s * SR); fc = np.exp(np.interp(np.arange(e - a) / (e - a), [0, 1], np.log(hz)))
        for c in range(2): bed[a:e, c] = dsp.svf(bed[a:e, c].astype(np.float64), fc, 0.707, 2, SR).astype(f32)
    gain = np.ones(N, f32)
    for a_s, e_s, fl in gaps:
        a, e = int(a_s * SR), int(e_s * SR); r = int(0.015 * SR); gg = np.full(e - a, db(fl), f32); gg[:r] = np.linspace(1, db(fl), r); gain[a:e] = np.minimum(gain[a:e], gg)
    bed *= gain[:, None]
    # ---- master: mono lows, DC, fades, loudness, limiter
    mid = (bed[:, 0] + bed[:, 1]) / 2; side = (bed[:, 0] - bed[:, 1]) / 2; del bed
    ff = rfftfreq(N, 1 / SR); side = irfft(rfft(side) / np.sqrt(1 + (120 / np.maximum(ff, 1e-3)) ** 8), N).astype(f32)
    mix = np.stack([mid + side, mid - side], 1).astype(f32); del mid, side; mix -= mix.mean(0)
    mf = R.get("masterFade", {}); fi, fo = mf.get("inSec", 0.0), mf.get("outSec", 0.0)
    env = np.ones(N, f32)
    if fi: env[:int(fi * SR)] = (0.5 - 0.5 * np.cos(np.pi * np.arange(int(fi * SR)) / int(fi * SR)))
    if fo: n = int(fo * SR); env[-n:] *= (0.5 + 0.5 * np.cos(np.pi * np.arange(n) / n))
    mix *= env[:, None]; mix[-int(0.05 * SR):] *= np.linspace(1, 0, int(0.05 * SR))[:, None]
    meter = pyln.Meter(SR); lu = meter.integrated_loudness(mix.astype(np.float64)); mix *= f32(db(R["targetLufs"] - lu))
    L_, R_, gr = dsp.limiter(mix[:, 0].astype(np.float64), mix[:, 1].astype(np.float64), ceiling_db=R.get("peakCeilDb", -1.0) - 0.3)
    mix = np.stack([L_, R_], 1).astype(f32)
    p = tp_db(mix)
    if p > R.get("peakCeilDb", -1.0): mix *= f32(db(R.get("peakCeilDb", -1.0) - p - 0.05))
    sf.write(out_path, mix, SR, subtype="PCM_24")
    # ---- measure
    stats = measure(R, T, secs, mix, meter, gr, g4, levels_rms, tlog, total_s, body_s)
    stats["renderSec"] = round(time.time() - t0, 1)
    json.dump(stats, open(out_path + ".stats.json", "w"), indent=1, default=float)
    return stats

def measure(R, T, secs, mix, meter, gr, g4, levels_rms, tlog, total_s, body_s):
    N = len(mix); x = mix.astype(np.float64); mono = x.mean(1); out = {}
    out["id"] = R["id"]; out["lengthSec"] = round(N / SR, 2); out["bodySec"] = round(body_s, 2)
    lufs = meter.integrated_loudness(x); tp = tp_db(mix); out["lufs"] = round(lufs, 2); out["truePeakDb"] = round(tp, 2)
    mid = x.mean(1); side = (x[:, 0] - x[:, 1]) / 2; mid_l = (x[:, 0] + x[:, 1]) / 2
    lufs_mid = meter.integrated_loudness(np.stack([mid_l, mid_l], 1)); out["monoFoldLossDb"] = round(lufs - lufs_mid, 2)
    F_s = rfft(side); F_m = rfft(mid_l); ff = rfftfreq(N, 1 / SR); lo = ff < 150
    out["lowSideMidDb150"] = round(10 * np.log10((np.abs(F_s[lo]) ** 2).sum() / ((np.abs(F_m[lo]) ** 2).sum() + 1e-20) + 1e-20), 1)
    hi = ff > 12000; out["energyAbove12kDb"] = round(10 * np.log10((np.abs(F_m[hi]) ** 2).sum() / ((np.abs(F_m) ** 2).sum() + 1e-20) + 1e-20), 1)
    out["lrCorrelation"] = round(float(np.corrcoef(x[:, 0], x[:, 1])[0, 1]), 3); out["limiterGainReductionDb"] = round(float(gr), 2)
    out["gates"] = dict(
        G1_truePeak=tp <= R.get("peakCeilDb", -1.0) + 0.01, G2_clipped=int((np.abs(mix) >= 0.999).sum()) == 0, G3_dc=bool(np.all(np.abs(x.mean(0)) <= 0.001)),
        G4_determinism_clip=g4, G5_cleanTail=bool(10 * np.log10((x[-4800:] ** 2).mean() + 1e-20) <= -60), G6_cleanStart=bool(np.abs(x[:96]).max() <= 0.003),
        G7_finite=bool(np.isfinite(x).all()), M1_loudness=-18.0 <= lufs <= -13.0, M2_monoFold=out["monoFoldLossDb"] <= 3.0, M5_lowsCentered=out["lowSideMidDb150"] <= -15.0,
        M12_hiss=out["energyAbove12kDb"] <= -24.0, M14_limiter=gr <= 4.0)
    # section energy: short-term loudness of the section interior vs planned energy 1-10
    rows = []
    for s, tm in zip(secs, T):
        a, e = int((tm["start"] + 0.5) * SR), int((tm["end"] - 0.25) * SR); seg = x[a:e]
        l = meter.integrated_loudness(seg) if len(seg) > SR * 0.6 else float("nan")
        F = np.abs(rfft(seg.mean(1) * np.hanning(len(seg)))); fr = rfftfreq(len(seg), 1 / SR); cen = float((F * fr).sum() / (F.sum() + 1e-12))
        rows.append(dict(section=s["name"], bars=s["bars"], bpm=tm["bpm"], t0=round(tm["start"], 1), t1=round(tm["end"], 1), plannedEnergy=s["energy"], lufs=round(l, 1), centroidHz=round(cen)))
    from scipy.stats import spearmanr
    ok = [r for r in rows if np.isfinite(r["lufs"])]
    rho = spearmanr([r["plannedEnergy"] for r in ok], [r["lufs"] for r in ok])[0] if len(ok) > 2 and len({r["plannedEnergy"] for r in ok}) > 1 else float("nan")
    pr = np.corrcoef([r["plannedEnergy"] for r in ok], [r["lufs"] for r in ok])[0, 1] if len(ok) > 2 else float("nan")
    # also: centroid-based "brightness/density" correlation
    rho_c = spearmanr([r["plannedEnergy"] for r in ok], [r["centroidHz"] for r in ok])[0] if len(ok) > 2 else float("nan")
    out["sectionMap"] = rows; out["energyCurve"] = dict(spearmanLufsVsPlan=round(float(rho), 2), pearsonLufsVsPlan=round(float(pr), 2), spearmanCentroidVsPlan=round(float(rho_c), 2),
                                                          loudestSection=max(ok, key=lambda r: r["lufs"])["section"], plannedPeak=max(rows, key=lambda r: r["plannedEnergy"])["section"],
                                                          lufsRangeLU=round(max(r["lufs"] for r in ok) - min(r["lufs"] for r in ok), 1))
    # seams: spectral flux around section boundaries and chord joins; sample-step click check
    hop = int(0.1 * SR); bm = x[:, 0] + x[:, 1]
    fr_ = np.array([np.log10(np.abs(rfft(bm[i:i + hop] * np.hanning(hop))) + 1e-9) for i in range(0, N - hop, hop)])
    flux = np.r_[0, np.sqrt(((np.diff(fr_, axis=0)) ** 2).mean(1))]; med = float(np.median(flux) + 1e-9)
    loc = lambda s_: float(flux[max(0, int(s_ / 0.1) - 3):int(s_ / 0.1) + 5].max() / med)
    out["seams"] = dict(globalFlux99VsMedian=round(float(np.percentile(flux, 99) / med), 2),
                        sectionBoundaryFluxVsMedian={f"{tm['start']:.1f}s {s['name']}": round(loc(tm["start"]), 2) for s, tm in zip(secs[1:], T[1:])})
    st = np.abs(np.diff(x, axis=0)).max(1); out["seams"]["maxSampleStep"] = round(float(st.max()), 4); out["seams"]["stepVsP999"] = round(float(st.max() / (np.percentile(st, 99.9) + 1e-12)), 2)
    # loudness step across each boundary (0.8 s before vs after, K-weighted)
    steps = {}
    for s, tm in list(zip(secs, T))[1:]:
        b = int(tm["start"] * SR); w = int(0.8 * SR)
        if b - w > 0 and b + w < N: steps[f"{tm['start']:.1f}s {s['name']}"] = round(meter.integrated_loudness(x[b:b + w]) - meter.integrated_loudness(x[b - w:b]), 1)
    out["seams"]["loudnessStepAcrossBoundaryLU"] = steps
    out["layerRmsDb"] = {k: round(20 * np.log10(v + 1e-12), 1) for k, v in levels_rms.items()}; out["transitionsPlaced"] = [(round(a, 1), b) for a, b in tlog]
    out["pass"] = all(out["gates"].values()); return out

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]; flags = [a for a in sys.argv[1:] if a.startswith("--")]
    R = json.load(open(args[0]))
    if "--validate" in flags: sys.exit(1 if validate(R)[0] else 0)
    w = 8
    for f in flags:
        if f.startswith("--workers="): w = int(f.split("=")[1])
    s = build(R, args[1], w); print(json.dumps({k: v for k, v in s.items() if k not in ("sectionMap",)}, indent=1, default=float))
    for r in s["sectionMap"]: print(r)
