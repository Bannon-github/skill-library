#!/usr/bin/env python3
"""Daily 3-skill test 2026-11-09 "Ramp Tide":
  phaser-pad-four-bar-ramp-inverse-filter-peaks-reverb-mix-counter-automation (pad + motion)
  + synth-noise-osc-split-filter-env-air-plus-tuned-noise-layers (air at the source)
  + short-kick-three-sub-layers-hierarchical-ducking (low end)
usage: render.py recipe.json out.wav   (env NOAIR=1 mutes every noise layer for the A/B macro)"""
import sys, os, json, numpy as np, soundfile as sf, pyloudnorm as pyln
from scipy import signal as sg
LAB = os.environ.get("LAB", "/workspace/skill-library/sample-lab"); sys.path.insert(0, LAB + "/engine")
import dsp, metrics
SR = 48000
R = json.load(open(sys.argv[1])); OUT = sys.argv[2]; rng = np.random.default_rng(R["seed"])
NB = R["bars"]; BL = 240 / R["bpm"]; BT = BL / 4; tb = lambda x: x * BL; S = R["sections"]
T = NB * BL + R["tailSec"]; N = int(T * SR); t = np.arange(N) / SR
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
def flt(k, f, x, o=2):
    if isinstance(f, (list, tuple)):
        return sg.sosfilt(sg.butter(o, f, k, fs=SR, output="sos"), x, axis=0)
    if np.ndim(f) > 0:
        fc = np.ascontiguousarray(np.asarray(f, dtype=np.float64)); md = 0 if k == "low" else 2
        if x.ndim == 1: return dsp.svf(np.ascontiguousarray(x), fc, 0.707, md, SR)
        return np.stack([dsp.svf(np.ascontiguousarray(x[:, c]), fc, 0.707, md, SR) for c in range(x.shape[1])], 1)
    return sg.sosfilt(sg.butter(o, f, k, fs=SR, output="sos"), x, axis=0)
def pan2(x, p): return np.stack([x * np.cos((p + 1) * np.pi / 4), x * np.sin((p + 1) * np.pi / 4)], 1) * np.sqrt(2)
def put(buf, y, s, g=1.0):
    i = int(round(s * SR)); L = min(len(y), N - i)
    if L > 0 and i >= 0:
        if y.ndim == 1 and buf.ndim == 2: buf[i:i+L] += y[:L, None] * g
        elif y.ndim == 2 and buf.ndim == 1: buf[i:i+L] += y[:L, 0] * g
        else: buf[i:i+L] += y[:L] * g
def verb(x, rt, seed, damp=9000.0, size=1.8, mod=0.25, diff=0.75):
    l, r = dsp.fdn_reverb(np.ascontiguousarray(x[:, 0]), np.ascontiguousarray(x[:, 1]), SR, float(rt), size, damp, 0.03, mod, diff, 0.0, seed)
    return np.stack([l, r], 1)
def fade(y, ms=10, mi=0.0):
    n = max(1, int(ms * SR / 1000)); y = y.copy()
    if n < len(y): y[-n:] *= np.linspace(1, 0, n)
    if mi:
        m = int(mi * SR / 1000)
        if m > 0 and m < len(y): y[:m] *= np.linspace(0, 1, m)
    return y
nm = lambda x: x / (np.max(np.abs(x)) + 1e-9)
st2 = lambda f, x: np.stack([f(np.ascontiguousarray(x[:, c]), c) for c in range(2)], 1)
def sec(b):
    if b < S["drumsIn"]: return "intro"
    if b < S["build"]: return "groove"
    if b < S["peak"]: return "build"
from numba import njit
from scipy.signal import lfilter
events = 0
AIR = R["air"]["on"] and not os.environ.get("NOAIR")
CH = R["chords"]; ROOTS = R["roots"]; chordIdx = lambda b: (b // 2) % len(CH)
def env_adsr(L, a, r, dur):
    tt = np.arange(L) / SR
    return np.clip(tt / a, 0, 1) ** 1.5 * np.clip((dur - tt) / r, 0, 1)
def bell(x, f, g, q=0.8): return np.stack([dsp.eq(x[:, c], "peak", f, q, g) for c in range(2)], 1) if x.ndim == 2 else dsp.eq(x, "peak", f, q, g)
def shelf(x, k, f, g): return np.stack([dsp.eq(x[:, c], k, f, 0.7, g) for c in range(2)], 1) if x.ndim == 2 else dsp.eq(x, k, f, 0.7, g)

@njit(cache=True)
def ramp_phaser(x, lfo, fLo, octs, fb, stages, mix, sr):
    n = x.shape[0]; zs = np.zeros(24); y = np.zeros(n); last = 0.0
    for i in range(n):
        f = fLo * (2.0 ** (lfo[i] * octs)); tt = np.tan(np.pi * min(f, 0.45 * sr) / sr); a = (tt - 1.0) / (tt + 1.0)
        v = x[i] + fb * last
        for s in range(stages):
            o = a * v + zs[s]; zs[s] = v - a * o; v = o
        last = v; y[i] = (1.0 - mix) * x[i] + mix * v
    return y

# ===== SKILL A: phaser pad, 4-bar ramp, inverse filter peaks, counter-automated band reverb
P = R["phaserPad"]; raw = np.zeros((N, 2))
for b in range(0, S["end"], 2):
    notes = CH[chordIdx(b)]; dur = 2 * BL + P["release"]; L = int(dur * SR); e = env_adsr(L, P["attack"], P["release"], dur)
    y = np.zeros((L, 2))
    for m in notes:
        for u in range(P["unison"]):
            x = u / (P["unison"] - 1) - 0.5
            y += pan2(dsp.osc_va(np.full(L, hz(m) * 2 ** (x * P["detune"] / 1200)), 0, 0.5, rng.random(), SR), x * 1.6 * P["spread"])
    y = flt("low", P["cut"], y, 2) * e[:, None] / (P["unison"] * len(notes))
    put(raw, y, tb(b)); events += 1
ramp = (t / (P["rampBars"] * BL)) % 1.0                       # step 2: rising ramp, once per 4 bars
rampS = np.minimum(ramp / 0.97, (1 - ramp) / 0.03)            # tiny 3% fall so the reset never clicks
ph = np.stack([ramp_phaser(np.ascontiguousarray(raw[:, 0]), np.ascontiguousarray(rampS), P["fLo"], P["octaves"], P["fb"], P["stages"], P["phaserMix"], SR),
               ramp_phaser(np.ascontiguousarray(raw[:, 1]), np.ascontiguousarray(np.roll(rampS, int(P["rightOffset"] * P["rampBars"] * BL * SR))), P["fLo"], P["octaves"], P["fb"], P["stages"], P["phaserMix"], SR)], 1)
# step 3: delay-as-filter: resonant HP and LP peaks on sine LFOs of different rates, moving in opposite directions, onset delayed
onset = np.clip(t / (P["lfoDelayBars"] * BL), 0, 1)
lh = 0.5 + 0.5 * np.sin(2 * np.pi * t / (P["hpLfoBars"] * BL)) * onset
ll = 0.5 - 0.5 * np.sin(2 * np.pi * t / (P["lpLfoBars"] * BL)) * onset
fH = np.ascontiguousarray(P["peakHpLo"] * (P["peakHpHi"] / P["peakHpLo"]) ** lh); fL = np.ascontiguousarray(P["peakLpLo"] * (P["peakLpHi"] / P["peakLpLo"]) ** ll)
pk = np.stack([dsp.svf(np.ascontiguousarray(ph[:, c]), fH, P["peakQ"], 1, SR) for c in range(2)], 1)  # resonant HP peak (band at cutoff)
pk2 = np.stack([dsp.svf(np.ascontiguousarray(ph[:, c]), fL, P["peakQ"], 1, SR) for c in range(2)], 1)
# step 6: peak amount rises with the sweep; reverb mix is its mirror (dry at strongest peaks, wet as they fade)
pkAmt = P["peakMin"] + (P["peakMax"] - P["peakMin"]) * rampS
peaks = ph + (nm(pk) + nm(pk2)) * 0.5 * pkAmt[:, None] * 0.6
wetMix = P["wetMax"] - (P["wetMax"] - P["wetMin"]) * rampS
# step 5: reverb last, 100% wet, band-filtered to the peak band, no regen
wet = verb(flt("band", P["verbBand"], peaks, 2), P["verbRt"], 21, 6000.0, 2.0)
wet = flt("band", P["verbBand"], wet, 2)
pad = nm(peaks) * (1 - 0.6 * wetMix)[:, None] + nm(wet) * (0.9 * wetMix)[:, None]
padDry = nm(raw)

# ===== SKILL B: synth-native noise air (split filter 2 spike env), noise bed, bass noise, tuned drum noise, master noise
A = R["air"]; airPad = np.zeros((N, 2)); bed = np.zeros((N, 2)); bassNz = np.zeros(N); mnz = np.zeros((N, 2))
if AIR:
    rise = 1 + A["noiseRise"] * np.clip((t - tb(S["build"])) / (tb(S["peak"]) - tb(S["build"])), 0, 1) * (t < tb(S["outro"]))
    for b in range(0, S["end"], 2):   # steps 3-5: noise osc on filter 2 (LP), sharp spike env -> cutoff, low res
        dur = 2 * BL + P["release"]; L = int(dur * SR); tt = np.arange(L) / SR
        spike = np.clip(tt / A["spikeAtk"], 0, 1) * np.exp(-np.maximum(tt - A["spikeAtk"], 0) / A["spikeDec"])
        fc = np.ascontiguousarray(np.clip(A["f2Base"] + A["f2Env"] * spike, 200, 16000))
        nz = rng.standard_normal((L, 2)); e = env_adsr(L, 0.004, P["release"], dur)
        y = np.stack([dsp.svf(np.ascontiguousarray(nz[:, c]), fc, 0.6, 0, SR) for c in range(2)], 1) * (e * (0.25 + 0.75 * spike))[:, None]
        put(airPad, y, tb(b))
    airPad *= rise[:, None]
    bed = rng.standard_normal((N, 2)); bed = shelf(bed, "lowshelf", 400, A["bedShelfDb"]); bed = bell(bed, 6000, A["bedBellDb"])   # steps 1-2
    mph1 = 0.5 + 0.5 * np.sin(2 * np.pi * A["mLfoA"] * t); mph2 = 0.5 + 0.5 * np.sin(2 * np.pi * A["mLfoB"] * t + np.pi)   # step 8
    mnz = rng.standard_normal((N, 2))
    mnz = np.stack([dsp.svf(np.ascontiguousarray(mnz[:, c]), np.ascontiguousarray(2500 + 5000 * mph1), 1.2, 0, SR) for c in range(2)], 1)
    mnz = np.stack([dsp.svf(np.ascontiguousarray(mnz[:, c]), np.ascontiguousarray(1500 + 2000 * mph2), 1.0, 2, SR) for c in range(2)], 1)

# ===== SKILL C: short kick + three hierarchical subs ducked to a ghost kick
Lw = R["low"]; kicks = []; snr = []
for b in range(S["drumsIn"], S["drumsOut"]):
    for q in ([0, 2] if b < S["build"] else [0, 1.5, 2] if b < S["peak"] else [0, 1.5, 2, 3.5] if b < S["outro"] else [0, 2]):
        kicks.append(tb(b) + q * BT)
    if b >= S["drumsIn"] + 2: snr.append(tb(b) + 3 * BT)
def kick():   # step 1: short, light comp, 550 cut, low boost, mid-high overdrive, mono
    L = int(0.32 * SR); tt = np.arange(L) / SR; f = 52 + 110 * np.exp(-tt / 0.025)
    k = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / Lw["kickDec"])
    hi = flt("high", 800, k); k = k - hi + 0.25 * np.tanh(4 * hi)
    k = dsp.eq(dsp.eq(k, "peak", 550, 1.0, -5), "lowshelf", 80, 0.7, 2)
    if AIR:  # skill B step 7: envelope-following tuned noise ~5 kHz on the kick for snap
        nz = flt("band", [A["kickSnapHz"] * 0.8, A["kickSnapHz"] * 1.25], rng.standard_normal(L)); en = np.abs(sg.hilbert(k)); k = k + A["tunedNoise"] * nz * en * np.exp(-tt / 0.02)
    return fade(np.tanh(1.3 * k), 10, 1)
kb = np.zeros(N); ghost = np.zeros(N); dn = int(Lw["duckMs"] / 1000 * SR); shp = 1 - np.clip(np.arange(dn) / dn, 0, 1) ** 2
for k0 in kicks: put(kb, kick(), k0); put(ghost, shp, k0)        # step 2: muted ghost kick = sidechain key
ghost = np.clip(ghost, 0, 1)
def sm(x, ms): a = np.exp(-1 / (ms / 1000 * SR)); return lfilter([1 - a], [1, -a], x)
def subchain(x, lp):  # mid/high cut, dip <20 Hz, overdrive + tape-ish comp, mono, final LP
    x = flt("high", 28, flt("low", 110, x, 2), 2); x = np.tanh(1.8 * x / (np.max(np.abs(x)) + 1e-9)); return flt("low", lp, x, 4)
s1 = np.zeros(N); s2 = np.zeros(N); s3 = np.zeros(N)
for b in range(S["drumsIn"] - 2, S["outro"] + 2):
    r = ROOTS[chordIdx(b)]
    for q, ln in ((0, 1.4), (2.5, 1.2)):   # step 3: sub 1 master sine, root, two notes per bar
        L = int(ln * BT * SR); tt = np.arange(L) / SR; put(s1, fade(np.sin(2 * np.pi * hz(r + 12) * tt) * np.clip(tt / 0.008, 0, 1), 25), tb(b) + q * BT)
    if b >= S["drumsIn"]:
        for q in (0.75, 1.5, 2.0, 3.0, 3.5):   # step 4: sub 2 from a bass-drum tail, denser groove
            L = int(0.5 * BT * SR); tt = np.arange(L) / SR; f = hz(r + 12) * (1 + 0.3 * np.exp(-tt / 0.01))
            put(s2, fade(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.12) * np.clip(tt / 0.004, 0, 1), 15), tb(b) + q * BT)
s3 = np.sin(2 * np.pi * np.cumsum(np.array([hz(ROOTS[chordIdx(int(x / BL))] + 24) for x in t[::480]]).repeat(480)[:N]) / SR)  # step 5: long sine, focused higher
s3 = s3 * np.clip((t - tb(S["drumsIn"] - 2)) / 3, 0, 1) * np.clip((tb(S["outro"] + 2) - t) / 3, 0, 1)
s3 = dsp.eq(flt("high", 70, s3, 2), "peak", Lw["sub3Hz"], 1.0, 3)
s1 = subchain(s1, Lw["lp"]); s2 = subchain(s2, Lw["lp"]) * Lw["sub2Makeup"]
e1 = np.clip(sm(np.abs(s1), 30) / (np.abs(s1).max() + 1e-9) * 3, 0, 1); e2 = np.clip(sm(np.abs(s2), 30) / (np.abs(s2).max() + 1e-9) * 3, 0, 1)
D = Lw["duckDepth"]; H = Lw["hierDepth"]
s1 *= (1 - D * ghost); s2 *= (1 - D * ghost) * (1 - H * e1)                 # hierarchy: sub2 yields to sub1
s3 *= (1 - D * ghost) * (1 - H * e1) * (1 - H * 0.7 * e2)                   # sub3 lowest
grp = s1 * Lw["sub1"] + s2 * Lw["sub2"] + s3 * Lw["sub3"]
grp = dsp.eq(dsp.eq(grp, "peak", 550, 1.0, -4), "lowshelf", 40, 0.7, 1.5) * (1 - 0.5 * ghost)   # step 6
if AIR:   # skill B step 6: noise +24 st over the bass, sustain 0, short decay, ~-8 dB
    for b in range(S["drumsIn"], S["outro"]):
        r = ROOTS[chordIdx(b)]; fN = hz(r + 12 + 24)
        for q in (0, 2.5):
            L = int(0.4 * SR); tt = np.arange(L) / SR
            put(bassNz, fade(flt("band", [fN * 0.85, fN * 1.18], rng.standard_normal(L)) * np.exp(-tt / A["bassNoiseDec"]) * np.clip(tt / 0.003, 0, 1), 10), tb(b) + q * BT)
bus = kb * Lw["kick"] + grp                                                  # step 7: tape-sat glue, 550 cut, mono
bus = np.tanh(Lw["busDrive"] * bus / (np.abs(bus).max() + 1e-9)) / np.tanh(Lw["busDrive"]); bus = dsp.eq(bus, "peak", 550, 1.0, -3)
drm = np.zeros((N, 2))
def snare():
    L = int(0.3 * SR); tt = np.arange(L) / SR
    body = flt("band", [180, 2500], rng.standard_normal(L)) * np.exp(-tt / 0.09) * 0.5 + np.sin(2 * np.pi * 185 * tt) * np.exp(-tt / 0.06)
    s = pan2(body, 0)
    if AIR:   # step 7: decorrelated tuned noise ~7 kHz for a wide burst
        en = np.exp(-tt / 0.05); s += np.stack([flt("band", [A["snareHz"] * 0.8, A["snareHz"] * 1.25], rng.standard_normal(L)) * en for _ in range(2)], 1) * A["tunedNoise"]
    return np.stack([fade(s[:, c], 15, 1) for c in range(2)], 1)
for s0 in snr: put(drm, snare(), s0, Lw["snare"])
def hat():
    L = int(0.12 * SR); return fade(flt("band", [5000, 11000], rng.standard_normal(L)) * np.exp(-np.arange(L) / SR / 0.035), 10, 1)
for b in range(S["drumsIn"], S["drumsOut"]):
    for q in (1, 3): put(drm, pan2(hat(), 0.2), tb(b) + q * BT + 0.5 * BT, Lw["hat"])   # off-beat 8ths on 2&/4&, sparse
drm = drm + 0.1 * nm(verb(flt("high", 400, drm), 1.2, 13))

# ===== mix + master
Mm = R["master"]
mix = pad * P["level"] * (1 - Mm["padDuck"] * ghost)[:, None]
mix += pan2(nm(bus), 0) * Lw["level"] + nm(drm) * 0.22
if AIR:
    mix += nm(airPad) * A["noiseOsc"] * (1 - 0.3 * ghost)[:, None]
    mix += pan2(nm(bassNz), 0) * Lw["level"] * 10 ** (A["bassNoiseDb"] / 20) * 0.5
    mix += nm(bed) * A["bedLevel"]
mix = sg.sosfiltfilt(sg.butter(2, 20, "high", fs=SR, output="sos"), mix, axis=0)
mix = shelf(mix, "highshelf", 2500, Mm["shelfDb"])
if AIR: mix = mix + nm(mnz) * A["masterNoise"]     # step 8: parallel master noise after master FX
Mn = 0.5 * (mix[:, 0] + mix[:, 1]); Sd = 0.5 * (mix[:, 0] - mix[:, 1])
Sd = sg.sosfiltfilt(sg.butter(4, Mm["sideHpHz"], "high", fs=SR, output="sos"), Sd) * Mm["width"]
mix = np.stack([Mn + Sd, Mn - Sd], 1)
fo = np.clip((T - 0.3 - t) / Mm["fadeOutSec"], 0, 1) ** 2; mix *= fo[:, None]; mix -= mix.mean(0)
meter = pyln.Meter(SR); gr_max = 0.0
for it in range(6):
    mix *= 10 ** ((Mm["targetLufs"] - meter.integrated_loudness(mix)) / 20)
    tp = np.maximum(dsp.true_peak_env(mix[:, 0]), dsp.true_peak_env(mix[:, 1])); ceil = 10 ** (Mm["tpCeil"] / 20); la = int(0.005 * SR)
    g0 = np.minimum(1, ceil / np.maximum(tp, 1e-9)); gg = np.minimum.reduce([np.roll(g0, k) for k in range(-la, la + 1, 24)]); gg = np.minimum(sg.filtfilt(np.ones(la) / la, [1], gg), 1)
    gr_max = max(gr_max, -20 * np.log10(max(gg.min(), 1e-9))); mix *= gg[:, None]
    if abs(meter.integrated_loudness(mix) - Mm["targetLufs"]) < 0.3: break
mix -= mix.mean(0); mix[-int(0.3 * SR):] = 0; mix[:int(0.002*SR)] = 0
mix[int(0.002*SR):int(0.2*SR)] *= np.linspace(0, 1, int(0.198*SR))[:, None]
sf.write(OUT, mix.astype(np.float32), SR, subtype="PCM_24")
res = metrics.compute(mix, {"limiter_gr_db": gr_max}, R.get("category", "pad"), False, NB * BL, start_body_s=0.0, f_low=hz(26), bar_s=BL)
hfx = lambda x: float(np.sqrt(np.mean(flt("high", 6000, x, 4) ** 2)))
res["events"] = events; res["lengthSec"] = round(T, 2); res["lufs"] = round(meter.integrated_loudness(mix), 2); res["drumsInSec"] = round(tb(S["drumsIn"]), 2)
res["airOn"] = bool(AIR); res["hfRms6k"] = hfx(mix)
json.dump(res, open(OUT + ".stats.json", "w"), indent=1, default=float)
print(json.dumps({"score": res["score"], "pass": res["pass"], "lufs": res["lufs"], "tp": res["extra"].get("true_peak_dbtp"), "gates": res["gates"], "subs": res["subs"], "tilt": res["extra"].get("tilt_db_oct"), "gr": round(gr_max, 2), "len": res["lengthSec"], "drumsIn": res["drumsInSec"], "hf6k": res["hfRms6k"]}, default=float))
