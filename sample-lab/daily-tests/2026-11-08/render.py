#!/usr/bin/env python3
"""Daily 3-skill test 2026-11-08 "Pedal Bloom":
  staggered-attack-octave-layer-pad (pad source)
  + drone-role-pedal-point-and-polychords (harmony / drone role)
  + dynamics-restoring-saturation (drum bus saturation with follower-restored peaks)
usage: render.py recipe.json out.wav"""
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
    if b < S["outro"]: return "peak"
    return "outro"
events = 0
prog = R["chords"]; chordAt = lambda b: prog[(b // 2) % len(prog)]
def env_adsr(L, a, r, dur):
    tt = np.arange(L) / SR
    return np.clip(tt / a, 0, 1) ** 1.5 * np.clip((dur - tt) / r, 0, 1)

# ===== SKILL A: staggered-attack-octave-layer-pad
P = R["pad"]; pad = np.zeros((N, 2)); grainBus = np.zeros((N, 2))
lfoPh = (t / (P["lfo1Bars"] * BL)) % 1.0
k = P["lfo1Skew"]  # triangle reshaped: slow open (k of cycle), quick close
lfo1 = np.where(lfoPh < k, lfoPh / k, 1 - (lfoPh - k) / (1 - k))
lfo2 = np.sin(2 * np.pi * t / (P["lfo2Bars"] * BL))  # bipolar sine on osc3 pan
for b in range(0, S["end"], 2):
    notes = chordAt(b)["pad"]; dur = 2 * BL + P["release"]; L = int(dur * SR); i0 = int(tb(b) * SR)
    sl = lambda a: (a[i0:i0 + L] if i0 + L <= N else np.pad(a[i0:], (0, i0 + L - N), mode="edge"))
    l1, l2 = sl(lfo1), sl(lfo2)
    e1 = env_adsr(L, P["att1"], P["release"], dur); e2 = env_adsr(L, P["att2"], P["release"], dur); e3 = env_adsr(L, P["att3"], P["release"], dur)
    y1 = np.zeros((L, 2)); y2 = np.zeros((L, 2)); y3 = np.zeros((L, 2))
    for m in notes:
        for u in range(P["unison"]):
            x = u / max(P["unison"] - 1, 1) - 0.5
            f = np.full(L, hz(m) * 2 ** (x * P["detune"] / 1200))
            y1 += pan2(np.sin(2 * np.pi * np.cumsum(f) / SR + rng.random() * 6.28), x * 0.4)  # osc1 sine core
            y2 += pan2(dsp.osc_va(f, 0, 0.5, rng.random(), SR), x * 1.4 * P["spread"])       # osc2 saw
            f3 = f * 2.0
            y3 += pan2(dsp.osc_va(f3, 2, 0.5, rng.random(), SR), x * P["spread"])             # osc3 tri +12
    nrm = P["unison"] * len(notes)
    # separate filters: saw filter = LFO1 (4/1) + small random offset per chord; tri filter static-ish
    rnd = 1 + P["randCut"] * (rng.random() * 2 - 1)
    c2 = np.clip((P["cut2"] + P["lfo1Amt"] * l1) * rnd, 120, 9000).astype(np.float64)
    y2 = np.stack([dsp.svf(np.ascontiguousarray(y2[:, c]), c2, 0.65, 0, SR) for c in range(2)], 1)
    c3 = np.full(L, float(P["cut3"]))
    y3 = np.stack([dsp.svf(np.ascontiguousarray(y3[:, c]), c3, 0.6, 0, SR) for c in range(2)], 1)
    # osc3 pan by LFO2 (rebalance)
    pl = 1 - 0.5 * P["lfo2Pan"] * (1 + l2); pr = 1 - 0.5 * P["lfo2Pan"] * (1 - l2)
    y3 = y3 * np.stack([pl, pr], 1)
    out = (y1 * e1[:, None] * P["l1"] + y2 * e2[:, None] * P["l2"] + y3 * e3[:, None] * P["l3"]) / nrm
    put(pad, out, tb(b)); events += 3
# foley grain in noise slot: soft, slow-moving filtered noise pitched to key region (no clicky transients)
gn = flt("band", [hz(P["grainCenter"]) * 0.7, hz(P["grainCenter"]) * 1.6], rng.standard_normal((N, 2)), 2)
rlev = sg.filtfilt(np.ones(int(1.5 * SR)) / int(1.5 * SR), [1], rng.random(N))  # random modulator on foley level
rlev = np.clip((rlev - rlev.min()) / (np.ptp(rlev) + 1e-9), 0, 1) ** 2
pad += nm(gn) * (rlev * P["grain"])[:, None]
# FX: chorus -> 2-band "multiband" upward lift of detail -> delay -> reverb
cl, cr = dsp.chorus(np.ascontiguousarray(pad[:, 0]), np.ascontiguousarray(pad[:, 1]), SR, 1, 0.35, 3.0, 12.0, 0.0, 1.0, P["chorusMix"], 0.0, 0.0)
pad = np.stack([cl, cr], 1)
lo = flt("low", 600, pad, 2); hi = pad - lo
henv = np.sqrt(sg.filtfilt(np.ones(int(0.2 * SR)) / int(0.2 * SR), [1], np.mean(hi ** 2, 1)) + 1e-12)
hg = np.clip((np.median(henv) / henv) ** P["mbUp"], 0.5, 2.5)  # upward-ish compression of the top band
pad = lo + hi * hg[:, None]
dw = dsp.stereo_delay(np.ascontiguousarray(pad[:, 0]), np.ascontiguousarray(pad[:, 1]), SR, 0.75 * BL, 0.5 * BL, 0.32, 0.32, 0.0, 0.0, 1, 300.0, 5000.0, 0.0, 0.0, 0.0)
pad = pad + P["delayMix"] * np.stack(dw, 1) if isinstance(dw, tuple) else pad + P["delayMix"] * dw
wet = verb(flt("high", 200, pad, 2), P["verbRt"], 11, 6500.0, 2.2)
pad = (1 - P["verbMix"]) * nm(pad) + P["verbMix"] * nm(wet)
pad = flt("high", P["lowCut"], pad, 2)

# ===== SKILL B: drone-role-pedal-point-and-polychords
DR = R["drone"]; sub = np.zeros(N); thru = np.zeros((N, 2))
# step 2: pedal point = one bass note held/repeated (dominant D builds tension), step 6: new pedal at key moment (tonic at peak)
for b in range(0, S["end"]):
    if b < S["drumsIn"] - 2: continue
    ped = DR["pedalPeak"] if S["peak"] <= b < S["outro"] else DR["pedal"]
    L = int(BL * SR) + int(0.05 * SR); tt = np.arange(L) / SR
    en = np.clip(tt / 0.02, 0, 1) * np.clip((BL + 0.03 - tt) / 0.05, 0, 1)
    put(sub, np.sin(2 * np.pi * hz(ped) * tt) * en, tb(b))
# repeat-the-root pulse above the sub (arp repeating root counts as pedal), soft 8ths, filtered
pulse = np.zeros((N, 2))
for b in range(S["drumsIn"], S["outro"]):
    ped = DR["pedalPeak"] if b >= S["peak"] else DR["pedal"]
    for q in range(8):
        Lp = int(0.6 * BT * 2 * SR); tt = np.arange(Lp) / SR
        v = dsp.osc_va(np.full(Lp, hz(ped + 12)), 0, 0.5, 0.0, SR) * np.clip(tt / 0.006, 0, 1) * np.exp(-tt / 0.16)
        v = fade(flt("low", 1400, v, 2), 15)
        put(pulse, pan2(v, 0.15 * (1 if q % 2 else -1)), tb(b) + q * BT * 2, 0.9 if q % 4 == 0 else 0.6)
# step 3/5: fixed-pitch mid through-line (key tracking off) with slow wavetable-position sweep
tl = np.sin(2 * np.pi * t / (DR["wtLfoBars"] * BL)) * 0.5 + 0.5
fth = np.full(N, hz(DR["thruNote"]))
sawv = dsp.osc_va(fth, 0, 0.5, 0.0, SR); sqv = dsp.osc_va(fth, 1, 0.5, 0.0, SR); sinv = np.sin(2 * np.pi * fth.cumsum() / SR)
wt = sinv * (1 - tl) + (0.5 * sawv + 0.5 * sqv) * tl
wt = dsp.svf(np.ascontiguousarray(wt), np.ascontiguousarray(900 + 1800 * tl), 0.6, 0, SR)
thEnv = np.clip((t - tb(DR["thruIn"])) / 6.0, 0, 1) * np.clip((tb(S["outro"] + 2) - t) / 4.0, 0, 1)
thru = pan2(wt * thEnv, 0.0); thru = thru + 0.5 * nm(verb(thru, 4.0, 5))
# step 4: polychord stack: static fifth-drones (D5+A5) over moving progression (pad chords) in build
poly = np.zeros(N)
for m in DR["polyStack"]:
    poly += dsp.osc_va(np.full(N, hz(m)), 2, 0.5, rng.random(), SR)
polyEnv = np.clip((t - tb(S["build"])) / (2 * BL), 0, 1) * np.clip((tb(S["outro"]) - t) / (1.5 * BL), 0, 1)
poly = dsp.svf(np.ascontiguousarray(poly), np.full(N, 2600.0), 0.6, 0, SR) * polyEnv
polyS = verb(pan2(poly, 0), 5.0, 9) * 0.6 + pan2(poly, 0) * 0.4

# ===== drums + SKILL C: dynamics-restoring-saturation on the drum bus
D = R["drums"]; drm = np.zeros((N, 2)); kicks = []
def kick():
    L = int(0.45 * SR); tt = np.arange(L) / SR; f = 46 + 90 * np.exp(-tt / 0.03)
    return fade(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.2), 12)
def snare():
    L = int(0.25 * SR); tt = np.arange(L) / SR
    return fade(flt("band", [900, 5000], rng.standard_normal(L)) * np.exp(-tt / 0.07) * 0.6 + np.sin(2 * np.pi * 190 * tt) * np.exp(-tt / 0.05), 10)
def hat(v):
    L = int(0.1 * SR); return fade(flt("band", [6000, 12000], rng.standard_normal(L)) * np.exp(-np.arange(L) / SR / 0.03) * v, 8)
kbus = np.zeros(N)
for b in range(S["drumsIn"], S["drumsOut"]):
    o = tb(b); peak = S["peak"] <= b < S["outro"]
    for kb in ([0, 2.5] if peak or b >= S["build"] else [0]):
        put(kbus, kick(), o + kb * BT); kicks.append(o + kb * BT)
    if b >= S["drumsIn"] + 2:
        put(drm, pan2(snare(), 0.05), o + 2 * BT, D["snare"])
    for q in (1, 3):  # off-beat quarters only: no rapid clicking texture
        put(drm, pan2(hat(0.7), -0.2), o + q * BT, D["hat"])
dry = drm + pan2(kbus, 0) * D["kick"]
# chain A: muted measuring follower on the dry bus
fol = np.abs(dry).max(1)
a = np.exp(-1 / (0.002 * SR)); r = np.exp(-1 / (0.09 * SR))
from scipy.signal import lfilter
fol = np.maximum(lfilter([1 - r], [1, -r], fol), lfilter([1 - a], [1, -a], fol))
fol = fol / (fol.max() + 1e-9)
# chain B: saturator then gain mapped from follower (base ~35%, amount ~65%)
drv = D["satDrive"]; sat = np.tanh(drv * dry / (np.abs(dry).max() + 1e-9)) / np.tanh(drv)
gainB = D["folBase"] + D["folAmt"] * fol
drmProc = sat * gainB[:, None]
pre_crest = 20 * np.log10(np.abs(dry).max() / (np.sqrt(np.mean(dry ** 2)) + 1e-12))
sat_crest = 20 * np.log10(np.abs(sat).max() / (np.sqrt(np.mean(sat ** 2)) + 1e-12))
post_crest = 20 * np.log10(np.abs(drmProc).max() / (np.sqrt(np.mean(drmProc ** 2)) + 1e-12))
drmProc = drmProc + 0.12 * nm(verb(flt("high", 400, drmProc), 1.0, 13))
# step 5: melodic parts ducked to the drum loop for pump
kenv = np.zeros(N); dn = int(D["duckMs"] / 1000 * SR); shape = 1 - np.clip(np.arange(dn) / dn, 0, 1) ** 2
for kk in kicks: put(kenv, shape, kk)
kenv = np.clip(kenv, 0, 1)

# ===== mix + master
Mm = R["master"]
sub = flt("low", 140, sub, 4) * (1 - 0.8 * kenv)
mix = nm(pad) * P["level"] * (1 - Mm["padDuck"] * kenv)[:, None]
mix += pan2(nm(sub), 0) * DR["subLevel"] + nm(pulse) * DR["pulseLevel"] * (1 - 0.4 * kenv)[:, None]
mix += nm(thru) * DR["thruLevel"] + nm(polyS) * DR["polyLevel"]
mix += nm(drmProc) * D["level"]
mix = sg.sosfiltfilt(sg.butter(2, 20, "high", fs=SR, output="sos"), mix, axis=0)
mix = np.stack([dsp.eq(mix[:, c], "highshelf", 2500, 0.6, Mm["shelfDb"]) for c in range(2)], 1)
mix = np.stack([dsp.eq(mix[:, c], "highshelf", 700, 0.6, Mm.get("midShelfDb", 0.0)) for c in range(2)], 1)
M = 0.5 * (mix[:, 0] + mix[:, 1]); Sd = 0.5 * (mix[:, 0] - mix[:, 1])
Sd = sg.sosfiltfilt(sg.butter(4, Mm["sideHpHz"], "high", fs=SR, output="sos"), Sd) * Mm["width"]
mix = np.stack([M + Sd, M - Sd], 1)
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
res["events"] = events; res["lengthSec"] = round(T, 2); res["lufs"] = round(meter.integrated_loudness(mix), 2); res["drumsInSec"] = round(tb(S["drumsIn"]), 2)
res["drumCrest"] = {"dry": round(pre_crest, 2), "saturated": round(sat_crest, 2), "restored": round(post_crest, 2)}
json.dump(res, open(OUT + ".stats.json", "w"), indent=1, default=float)
print(json.dumps({"score": res["score"], "pass": res["pass"], "lufs": res["lufs"], "tp": res["extra"].get("true_peak_dbtp"), "gates": res["gates"], "subs": res["subs"], "tilt": res["extra"].get("tilt_db_oct"), "gr": round(gr_max, 2), "len": res["lengthSec"], "drumsIn": res["drumsInSec"], "crest": res["drumCrest"]}, default=float))
