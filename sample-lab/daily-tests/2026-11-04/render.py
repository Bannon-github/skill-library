#!/usr/bin/env python3
"""Daily 3-skill test 2026-11-04: start-bright-then-filter pad (brightness-and-air-at-the-source) +
kick+bass punch workflow in four levels (bass-design) + genre drum pattern families, halftime two-step at 140 (drum-groove).
usage: render.py recipe.json out.wav"""
import sys, os, json, numpy as np, soundfile as sf, pyloudnorm as pyln
from scipy import signal as sg
LAB = os.environ.get("LAB", "/workspace/skill-library/sample-lab"); sys.path.insert(0, LAB + "/engine")
import dsp, metrics
SR = 48000
R = json.load(open(sys.argv[1])); OUT = sys.argv[2]; rng = np.random.default_rng(R["seed"])
NB = R["bars"]; BL = 240 / R["bpm"]; BT = BL / 4; S16 = BT / 4; tb = lambda x: x * BL; S = R["sections"]
T = NB * BL + R["tailSec"]; N = int(T * SR); t = np.arange(N) / SR
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
def flt(k, f, x, o=2): return sg.sosfilt(sg.butter(o, f, k, fs=SR, output="sos"), x, axis=0)
def pan2(x, p): return np.stack([x * np.cos((p + 1) * np.pi / 4), x * np.sin((p + 1) * np.pi / 4)], 1) * np.sqrt(2)
def put(buf, y, s, g=1.0):
    i = int(round(s * SR)); L = min(len(y), N - i)
    if L > 0 and i >= 0: buf[i:i + L] += y[:L] * g
def verb(x, rt, seed, damp=9000.0, size=1.8, mod=0.25, diff=0.75):
    l, r = dsp.fdn_reverb(np.ascontiguousarray(x[:, 0]), np.ascontiguousarray(x[:, 1]), SR, float(rt), size, damp, 0.03, mod, diff, 0.0, seed); return np.stack([l, r], 1)
def fade(y, ms=10, mi=0.0):
    n = int(ms * SR / 1000); y[-n:] *= np.linspace(1, 0, n)
    if mi: m = int(mi * SR / 1000); y[:m] *= np.linspace(0, 1, m)
    return y
nm = lambda x: x / (np.max(np.abs(x)) + 1e-9)
st2 = lambda f, x: np.stack([f(np.ascontiguousarray(x[:, c]), c) for c in range(2)], 1)
def sec(b): return "intro" if b < S["drumsIn"] else "groove" if b < S["peak"] - 4 else "build" if b < S["peak"] else "peak" if b < S["outro"] else "outro"
chord = lambda b: R["chords"][(b // 2) % 4]
events = 0
# ===== SKILL A: start-bright-then-filter pad
P = R["pad"]; pad = np.zeros((N, 2)); wt = 0.5 - 0.5 * np.cos(2 * np.pi * t / (P["wtLfoBars"] * BL))   # slow 'wavetable position' sweep
for b in range(0, S["end"], 2):
    _, notes = chord(b); dur = 2 * BL + P["release"]; L = int(dur * SR); tt = np.arange(L) / SR; i0 = int(tb(b) * SR)
    amp = np.clip(tt / P["attack"], 0, 1) * np.clip((dur - tt) / P["release"], 0, 1)                        # step 1: ~450 ms attack/release
    w = wt[i0:i0 + L] if i0 + L <= N else np.pad(wt[i0:], (0, i0 + L - N), mode="edge")
    y = np.zeros((L, 2)); U = P["unison"]
    for m in notes:
        for k in range(U):                                                                                    # step 3: odd unison 7, static detune
            x = (k / (U - 1) - 0.5); f = np.full(L, hz(m) * 2 ** (x * P["detuneCents"] / 1200)); ph = rng.random()
            v = (1 - w) * dsp.osc_va(f, 0, 0.5, ph, SR) + w * dsp.osc_va(f, 1, P["pw"], ph, SR)              # step 2: bright buzzy saw <-> PWM
            y += pan2(v, x * 2 * P["spread"]) / (U * len(notes))
    put(pad, y * amp[:, None], tb(b)); events += 1
cut = np.zeros(N)                                                                                            # step 5: LP 18 dB/oct, cutoff automated for builds
for b in range(S["end"] + 1):
    s = sec(min(b, S["end"] - 1)); c0 = P["cut"][s]
    if s == "build": c0 = P["cut"]["groove"] * (P["cut"]["build"] / P["cut"]["groove"]) ** ((b - (S["peak"] - 4)) / 4)
    i = int(tb(b) * SR); cut[i:] = c0
cut = sg.filtfilt(np.ones(int(0.5 * SR)) / int(0.5 * SR), [1], cut)
pad = st2(lambda x, c: dsp.svf(x, cut, 0.707, 0, SR), pad)                                                   # 12 dB/oct SVF
a = np.exp(-2 * np.pi * cut / SR); p1 = np.zeros_like(pad); yl = np.zeros(2)                                 # + 6 dB/oct pole following cutoff -> 18 dB/oct
for i0 in range(0, N, 2400):
    sl = slice(i0, min(N, i0 + 2400)); aa = float(a[i0])
    out, _ = sg.lfilter([1 - aa], [1, -aa], pad[sl], axis=0, zi=(aa * yl)[None, :]); p1[sl] = out; yl = out[-1]
pad = p1 * 1.6                                                                                               # raise volume to compensate
wet = verb(flt("high", P["verbHp"], pad, 4), P["verbRt"], 5, 7000.0, 2.2)                                    # step 6: very large low-cut reverb, high mix
pad = (1 - P["verbMix"]) * nm(pad) + P["verbMix"] * nm(wet); pad = flt("high", P["lowCut"], pad, 2)          # EQ cuts excess low end
Mp = 0.5 * (pad[:, 0] + pad[:, 1]); Sp = 0.5 * (pad[:, 0] - pad[:, 1]) * P["imagerSide"]; pad = np.stack([Mp + Sp, Mp - Sp], 1)   # step 7: imager
pad = st2(lambda x, c: dsp.eq(x, "highshelf", 3000, 0.7, P["bright"]), pad)                                # air shelf (top-end headroom kept by the filter)
# ===== SKILL C: drums, halftime two-step family at 140 BPM, 16th swing, 2/4-bar variations, tom fill, crash
D = R["drums"]; drm = np.zeros((N, 2)); kicks = []
def kick(): L = int(0.4 * SR); tt = np.arange(L) / SR; f = 50 + 110 * np.exp(-tt / 0.03); return fade(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.2), 10)
def snare(): L = int(0.3 * SR); tt = np.arange(L) / SR; return fade(flt("band", [1500, 9000], rng.standard_normal(L)) * np.exp(-tt / 0.09) * 0.8 + np.sin(2 * np.pi * 190 * tt) * np.exp(-tt / 0.05), 10)
def rim(): L = int(0.1 * SR); tt = np.arange(L) / SR; return fade((flt("band", [1500, 3000], rng.standard_normal(L)) * 0.5 + np.sin(2 * np.pi * 900 * tt)) * np.exp(-tt / 0.025), 5)
def hat(v, d=0.02): L = int(0.15 * SR); return fade(flt("band", [6000, 14000], rng.standard_normal(L)) * np.exp(-np.arange(L) / SR / d) * v, 5)
def tom(f0): L = int(0.4 * SR); tt = np.arange(L) / SR; f = f0 * (1 + 0.5 * np.exp(-tt / 0.03)); return fade(np.tanh(1.5 * np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-tt / 0.15), 10)
def cym(d): L = int(d * 3 * SR); return fade(flt("high", 5000, rng.standard_normal(L)) * np.exp(-np.arange(L) / SR / d), 20)
sw = lambda q: q * S16 + (D["swing"] * S16 if q % 2 else 0.0)                                                   # identical offset on every second 16th
for b in range(S["drumsIn"], S["drumsOut"]):
    s = sec(b); rb = b - S["drumsIn"]; o = tb(b); bar2 = rb % 2 == 1
    for q in ([0.0] if not bar2 else [1.0]) if s != "outro" else ([0.0] if not bar2 else []):                # halftime two-step: kick 1, 'and of 3' doubled -> bar 2 beat 2
        put(drm, pan2(kick(), 0) * D["kick"], o + q * BT); kicks.append(o + q * BT); events += 1
    put(drm, pan2(snare(), 0.05) * D["snare"], o + 2 * BT); events += 1                                       # snare on doubled backbeat (beat 3)
    rims = [6, 14] if not bar2 else [10, 13]                                                                   # syncopated rims, changed in bar 2
    if s != "intro": [put(drm, pan2(rim(), 0.25) * D["rim"], o + sw(q)) for q in rims]
    hq = range(0, 16, 2) if s == "outro" else range(16)                                          # 8ths, then 16ths with varied velocity (trap)
    for q in hq:
        if rb < 2: break
        v = (0.9 if q % 4 == 2 else 0.55) * (0.75 + 0.25 * rng.random() if len(hq) == 16 else 1) * (0.7 if s == "groove" and q % 2 else 1)
        put(drm, pan2(hat(v), -0.3) * D["hat"], o + sw(q)); events += 1
    if s == "peak": [put(drm, pan2(hat(0.5, 0.12), 0.35) * D["ride"], o + k * BT) for k in range(4)]             # rides on every beat, low velocity
    if rb % 8 == 0: put(drm, pan2(cym(0.6), -0.2) * D["crash"], o)                                           # crash on phrase downbeat
    if rb % 8 == 7 and s != "outro":                                                                          # 4-bar-variation tom fill high->mid->low on syncopated 16ths
        for j, (q, f0) in enumerate([(9, 220), (11, 165), (13, 120), (15, 95)]): put(drm, pan2(tom(f0), 0.4 - 0.25 * j) * D["tom"], o + sw(q))
kd = drm.copy()
drm = drm + 0.2 * nm(verb(flt("high", 400, drm), 1.4, 11))
# ===== SKILL B: kick+bass punch workflow, four levels
B = R["bass"]; sub = np.zeros(N); mid = np.zeros(N);
kmono = np.zeros(N); [put(kmono, kick() * D["kick"], k) for k in kicks]
# level 3a/3b: fixed sub start phase, sweep and keep the loudest+steadiest kick+sub sum (one kick-length window)
kw = kick()[: int(0.25 * SR)]; f0 = hz(R["chords"][0][0]); tt = np.arange(len(kw)) / SR; best = (None, -1)
for ph in range(0, 360, 15):
    sm = kw + 0.8 * np.sin(2 * np.pi * f0 * tt + np.radians(ph)); env = np.abs(sg.hilbert(sm))
    sc = np.sqrt(np.mean(sm ** 2)) / (1 + np.std(env[: int(0.15 * SR)])); best = (ph, sc) if sc > best[1] else best
PH = best[0]
# level 3c: micro-delay (<1 ms) aligning sub cycles with the kick
lags = np.arange(0, int(0.0005 * SR) + 1); ss = np.sin(2 * np.pi * f0 * np.arange(len(kw) + len(lags)) / SR + np.radians(PH))
DLY = int(lags[np.argmax([np.dot(kw, ss[len(lags) - 1 - l: len(lags) - 1 - l + len(kw)]) for l in lags])])
for b in range(S["drumsIn"], S["drumsOut"] + 1):
    root, _ = chord(b); rb = b - S["drumsIn"]; bar2 = rb % 2 == 1
    starts = [0, 2.75] if not bar2 else [1.0, 2.75]                                                           # notes on the kick + one overlapping pickup
    if sec(b) == "outro" and bar2: starts = [0]
    for j, st in enumerate(starts):
        en = starts[j + 1] if j + 1 < len(starts) else 4.0; dur = (en - st) * BT; L = int(dur * SR); tt = np.arange(L) / SR
        env = np.clip(tt / 0.004, 0, 1) * np.clip((dur - tt) / 0.03, 0, 1)
        put(sub, np.sin(2 * np.pi * hz(root) * tt + np.radians(PH)) * env, tb(b) + st * BT + DLY / SR)          # level 2: mono sub, no unison
        v = sum(dsp.osc_va(np.full(L, hz(root + 12) * 2 ** (d * B["midDetune"] / 1200)), 0, 0.5, 0.0, SR) for d in (-1, 1)) / 2
        v = dsp.svf(v, np.clip(B["midCut"] * (1 + 1.5 * np.exp(-tt / 0.08)), 100, 8000), 0.8, 0, SR) * env
        put(mid, v, tb(b) + st * BT); events += 1
sub = flt("low", B["split"], sub, 4); mid = flt("high", B["split"], mid, 4)                                   # split at 120 Hz
kenv = np.zeros(N); dn = int(B["duckMs"] / 1000 * SR); shape = 1 - np.clip(np.arange(dn) / dn, 0, 1) ** 2      # level 1: hand-drawn duck shape
for k in kicks: put(kenv, shape, k)
kenv = np.clip(kenv, 0, 1); sub *= 1 - B["subDuck"] * kenv; mid *= 1 - B["midDuck"] * kenv                    # sub ducked fully, mid a little
bus = kmono * B["kickInBus"] + nm(sub) * B["subLevel"] + nm(mid) * B["midLevel"]                                        # level 4: kick + bass bus
lo = flt("low", 120, bus, 2); bus = bus - lo + np.tanh(B["sat"] * lo) / B["sat"]                              # subtle low-end saturation
for thr in np.arange(-6, -40, -0.5):
    g = dsp.env_follow_gain(bus, SR, float(thr), 3.0, B["glueAtt"], B["glueRel"])
    if -20 * np.log10(g.min()) >= B["glueGrDb"]: break
GLUE = -20 * np.log10(g.min()); bus = bus * g; bus = np.tanh(B["clip"] * bus / (np.max(np.abs(bus)) + 1e-9)) / np.tanh(B["clip"])   # glue ~1.5 dB, soft clip
# ===== mix + master (same chain as earlier daily tests)
mix = nm(pad) * P["level"] * (1 - 0.25 * kenv)[:, None] + pan2(bus, 0) * B["level"] + nm(drm - pan2(kmono, 0) * 0.98) * D["level"]
Mm = R["master"]; mix = sg.sosfiltfilt(sg.butter(2, 20, "high", fs=SR, output="sos"), mix, axis=0)
mix = np.stack([dsp.eq(mix[:, c], "highshelf", 2500, 0.6, Mm["shelfDb"]) for c in range(2)], 1)
mix = np.tanh(Mm["satDrive"] * mix / (np.max(np.abs(mix)) + 1e-9)) / np.tanh(Mm["satDrive"])
M = 0.5 * (mix[:, 0] + mix[:, 1]); Sd = 0.5 * (mix[:, 0] - mix[:, 1]); Sd = sg.sosfiltfilt(sg.butter(4, Mm["sideHpHz"], "high", fs=SR, output="sos"), Sd); mix = np.stack([M + Sd, M - Sd], 1)
fo = np.clip((T - 0.3 - t) / Mm["fadeOutSec"], 0, 1) ** 2; mix *= fo[:, None]; mix -= mix.mean(0)
meter = pyln.Meter(SR); gr_max = 0.0
for it in range(6):
    mix *= 10 ** ((Mm["targetLufs"] - meter.integrated_loudness(mix)) / 20)
    tp = np.maximum(dsp.true_peak_env(mix[:, 0]), dsp.true_peak_env(mix[:, 1])); ceil = 10 ** (Mm["tpCeil"] / 20); la = int(0.005 * SR)
    g0 = np.minimum(1, ceil / np.maximum(tp, 1e-9)); gg = np.minimum.reduce([np.roll(g0, k) for k in range(-la, la + 1, 24)]); gg = np.minimum(sg.filtfilt(np.ones(la) / la, [1], gg), 1)
    gr_max = max(gr_max, -20 * np.log10(gg.min())); mix *= gg[:, None]
    if abs(meter.integrated_loudness(mix) - Mm["targetLufs"]) < 0.3: break
mix -= mix.mean(0); mix[-int(0.3 * SR):] = 0; mix[:int(0.002*SR)] = 0; mix[int(0.002*SR):int(0.2*SR)] *= np.linspace(0, 1, int(0.198*SR))[:, None]
sf.write(OUT, mix.astype(np.float32), SR, subtype="PCM_24")
res = metrics.compute(mix, {"limiter_gr_db": gr_max}, R.get("category", "pad"), False, NB * BL, start_body_s=0.0, f_low=hz(28), bar_s=BL)
res["events"] = events; res["lengthSec"] = round(T, 2); res["lufs"] = round(meter.integrated_loudness(mix), 2); res["drumsInSec"] = round(tb(S["drumsIn"]), 2)
res["subPhaseDeg"] = PH; res["subDelaySamples"] = DLY; res["glueGrDb"] = round(float(GLUE), 2)
json.dump(res, open(OUT + ".stats.json", "w"), indent=1, default=float)
print(json.dumps({"score": res["score"], "pass": res["pass"], "lufs": res["lufs"], "tp": res["extra"].get("true_peak_dbtp"), "gates": res["gates"], "subs": res["subs"], "tilt": res["extra"].get("tilt_db_oct"), "events": events, "gr": round(gr_max, 2), "len": res["lengthSec"], "drumsIn": res["drumsInSec"], "ph": PH, "dly": DLY, "glue": round(float(GLUE), 2)}, default=float))
