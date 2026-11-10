#!/usr/bin/env python3
"""Daily 3-skill test 2026-11-10 "Drone Rack":
  three-band-wavetable-rack-counter-lfo-position-glue-reverb-saturate-reverb-macro-drive (drone instrument)
  + dark-short-kick-behind-busy-bass-transient-body-tail-73hz-start-eighth-note-length (kick under a busy bass)
  + hypnotic-drone-arrangement-phrase-layer-fade-ins-sequence-instrument-swap-drone-only-break (structure)
usage: render.py recipe.json out.wav"""
import sys, os, json, numpy as np, soundfile as sf, pyloudnorm as pyln
from scipy import signal as sg
from scipy.signal import lfilter
LAB = os.environ.get("LAB", "/workspace/skill-library/sample-lab"); sys.path.insert(0, LAB + "/engine")
import dsp, metrics
SR = 48000
R = json.load(open(sys.argv[1])); OUT = sys.argv[2]; rng = np.random.default_rng(R["seed"])
NB = R["bars"]; BL = 240 / R["bpm"]; BT = BL / 4; tb = lambda x: x * BL; S = R["sections"]
T = NB * BL + R["tailSec"]; N = int(T * SR); t = np.arange(N) / SR
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
C = np.ascontiguousarray
def bw(k, f, x, o=2): return sg.sosfilt(sg.butter(o, f, k, fs=SR, output="sos"), x, axis=0)
def svf(x, fc, q, md):
    fc = C(np.clip(fc, 20, 0.45 * SR))
    return dsp.svf(C(x), fc, q, md, SR) if x.ndim == 1 else np.stack([dsp.svf(C(x[:, c]), fc, q, md, SR) for c in range(2)], 1)
def pan2(x, p): return np.stack([x * np.cos((p + 1) * np.pi / 4), x * np.sin((p + 1) * np.pi / 4)], 1) * np.sqrt(2)
def put(buf, y, s, g=1.0):
    i = int(round(s * SR)); L = min(len(y), N - i)
    if L > 0 and i >= 0:
        if y.ndim == 1 and buf.ndim == 2: buf[i:i+L] += y[:L, None] * g
        else: buf[i:i+L] += y[:L] * g
def verb(x, rt, seed, damp=9000.0, size=1.8, mod=0.2, diff=0.75, pre=0.02):
    l, r = dsp.fdn_reverb(C(x[:, 0]), C(x[:, 1]), SR, float(rt), size, damp, pre, mod, diff, 0.0, seed); return np.stack([l, r], 1)
def fade(y, ms=10, mi=0.0):
    y = y.copy(); n = max(1, int(ms * SR / 1000))
    if n < len(y): y[-n:] *= np.linspace(1, 0, n)[:, None] if y.ndim == 2 else np.linspace(1, 0, n)
    if mi:
        m = int(mi * SR / 1000); y[:m] *= np.linspace(0, 1, m)[:, None] if y.ndim == 2 else np.linspace(0, 1, m)
    return y
nm = lambda x: x / (np.max(np.abs(x)) + 1e-9)
def sm(x, ms): a = np.exp(-1 / (ms / 1000 * SR)); return lfilter([1 - a], [1, -a], x, axis=0)
events = 0
D = R["drone"]; K = R["rack"]
# ===== SKILL C step 1: one recorded-style cutoff automation (the rack's one macro, skill A step 9); sec2 automation reduced (step 6)
mb, mv = zip(*D["macro"]); macro = np.interp(t / BL, mb, mv)
s2m = (t >= tb(S["sec2"])) & (t < tb(S["outro"])); mean2 = macro[s2m].mean(); macro[s2m] = mean2 + (macro[s2m] - mean2) * D["macroSec2Scale"]
macro = sm(macro, 200)
# pre-drop: filter the top end down over the last bar before sec2 (skill C step 8)
predrop = 1 - 0.7 * np.clip((t - tb(S["sec2"] - 1)) / BL, 0, 1) * (t < tb(S["sec2"]))
# ===== SKILL A: three-band wavetable rack playing the held drone notes
notes = [[0, S["end"], D["root"]]] + D["added"] + D["atmoBreak"]
tabMidA = {}; rack = {"mid": np.zeros((N, 2)), "high": np.zeros((N, 2)), "low": np.zeros(N)}
def lfo(rate, ph=0.0): return np.sin(2 * np.pi * rate * t + ph)
M = K["mid"]; H = K["high"]; Lo = K["low"]
for (b0, b1, m) in notes:
    s0 = tb(b0); s1 = min(tb(b1), T - 0.5); rel = M["envRelease"]
    i0 = int(s0 * SR); i1 = min(N, int((s1 + rel) * SR)); L = i1 - i0; tt = np.arange(L) / SR; dur = s1 - s0
    fin = D["fadeInSec"] if b0 == 0 else K["attack"]                                 # step 7: ~1 s attack (drone gets a short fade, skill C)
    amp = np.clip(tt / fin, 0, 1) ** 1.5 * np.clip((dur + rel - tt) / rel, 0, 1)
    fenv = np.exp(-tt / M["envDecay"]) * np.clip((dur + rel - tt) / rel, 0, 1)        # step 3: slow env (2 s decay, 3 s release) on cutoff
    tl = t[i0:i1]; mac = macro[i0:i1]; atmo = [b0, b1, m] in D["atmoBreak"]
    # steps 1-2: mids, osc1 warm table pos LFO1+ LFO2-, osc2 sweep table with the opposite directions, unison
    f = hz(m); tA = dsp.wavetable_frames("soft_to_complex", f); tB = dsp.wavetable_frames("saw_tri_square_sine", f)
    la = np.sin(2 * np.pi * M["lfoA"] * tl); lb = np.sin(2 * np.pi * M["lfoB"] * tl + 1.3)
    p1 = C(np.clip(0.45 + M["posDepth"] * (la - lb) / 2 + 0.08 * mac, 0, 1)); p2 = C(np.clip(0.45 - M["posDepth"] * (la - lb) / 2 + 0.08 * mac, 0, 1))
    y = np.zeros((L, 2)); U = K["unisonMid"]
    for u in range(U):
        x = u / (U - 1) - 0.5; fr = C(np.full(L, f * 2 ** (x * K["detuneMid"] / 1200)))
        y += pan2(dsp.osc_wt(fr, p1, tA, rng.random(), SR, 1) + 0.8 * dsp.osc_wt(fr, p2, tB, rng.random(), SR, 1), x * 1.4)
    cut = (M["cutBase"] + M["cutMacro"] * mac) * (1 + M["cutLfo"] * (la + lb) / 2) * (1 + M["envAmt"] * fenv) * predrop[i0:i1]
    y = svf(y, cut, 0.8, 0); y = np.tanh(y * (1 + 0.8 * mac)[:, None] / U) * U              # step 9: macro adds filter drive
    y = bw("high", M["lowCut"], y, 2) * amp[:, None] / U
    rack["mid"][i0:i1] += y * (0.7 if atmo else 1.0) * M["level"]
    # step 5: highs, brighter table an octave up, more open filter + light drive, noise-style wide unison, own slower LFOs; macro closes it
    fh = hz(m + H["octave"]); tH = dsp.wavetable_frames("artifact_high", fh); tH2 = dsp.wavetable_frames("digital_additive", fh)
    ha = np.sin(2 * np.pi * H["lfoA"] * tl + 0.5); hb = np.sin(2 * np.pi * H["lfoB"] * tl + 2.1)
    q1 = C(np.clip(0.5 + H["posDepth"] * (ha - hb) / 2, 0, 1)); q2 = C(np.clip(0.5 - H["posDepth"] * (ha - hb) / 2, 0, 1))
    yh = np.zeros((L, 2)); U = K["unisonHigh"]
    for u in range(U):
        x = u / (U - 1) - 0.5; fr = C(np.full(L, fh * 2 ** (x * K["detuneHigh"] / 1200))); fr2 = C(fr * 2 ** (7 / 1200))
        yh += pan2(dsp.osc_wt(fr, q1, tH, rng.random(), SR, 1) + 0.6 * dsp.osc_wt(fr2, q2, tH2, rng.random(), SR, 1), x * 1.9)
    yh = svf(yh, (H["cutBase"] + H["cutMacroClose"] * mac) * predrop[i0:i1], 0.7, 0); yh = np.tanh(H["drive"] * yh / U) / np.tanh(H["drive"])
    rack["high"][i0:i1] += bw("high", 1500, yh, 2) * amp[:, None] * H["level"] * (1.4 if atmo else 1.0)
    # step 6: lows, plain saw an octave down + sub, steep low-res HP, one very slow LFO on cutoff (mono)
    if not atmo and m <= D["root"] + 7:
        fl = hz(m + Lo["octave"]); sw = dsp.osc_va(C(np.full(L, fl)), 0, 0.5, rng.random(), SR)
        sw = svf(sw, (Lo["cutBase"] + Lo["cutMacro"] * mac) * (1 + Lo["cutLfo"] * np.sin(2 * np.pi * Lo["lfo"] * tl)), 0.6, 0)
        sub = np.sin(2 * np.pi * fl / 2 * tl) * Lo["subLevel"] if m == D["root"] else 0
        rack["low"][i0:i1] += bw("high", Lo["hp"], sw + sub, 4) * amp * Lo["level"] * (1 if m == D["root"] else 0.5)
    events += 1
# step 7 balance + step 8 FX chain on the summed rack: glue comp 4:1 -> 100% wet vintage verb (sent in parallel, see note) -> soft clip -> long verb 50%
rk = rack["mid"] + rack["high"] + pan2(rack["low"], 0) * 0.5
lvl = sm(np.max(np.abs(rk), 1), 30); thr = np.percentile(lvl, 90); g = np.where(lvl > thr, (thr + (lvl - thr) / K["glueRatio"]) / (lvl + 1e-9), 1.0); rk = rk * sm(g, 80)[:, None]
v1 = verb(bw("high", 200, rk), K["verb1Rt"], 31, K["verb1Damp"], 1.5); rk = rk + K["verb1Mix"] * nm(v1) * np.max(np.abs(rk))
rk = np.tanh(K["clipDrive"] * rk / np.max(np.abs(rk))) / np.tanh(K["clipDrive"])
v2 = verb(bw("high", 250, rk), K["verb2Rt"], 37, 7000.0, 2.4, 0.25); rk = (1 - K["verb2Mix"]) * rk + K["verb2Mix"] * nm(v2)
rk = rk / np.max(np.abs(rk))
# ===== SKILL B: dark short kick (transient / body / tail), 73 Hz start falling to A1, ~1/8 note, a few dB under the bass
Kk = R["kick"]; kicks = []
def kick():
    L = int(Kk["lenNotes"] * BT * SR); tt = np.arange(L) / SR
    f = Kk["endHz"] + (Kk["startHz"] - Kk["endHz"]) * np.exp(-tt / Kk["bodyTau"]) + (Kk["punchHz"] - Kk["startHz"]) * np.exp(-tt / Kk["punchTau"])  # step 2
    body = np.sin(2 * np.pi * np.cumsum(f) / SR)
    env = np.clip(tt / (Kk["atkMs"] / 1000), 0, 1) * np.clip((L / SR - tt) / (L / SR * 0.55), 0, 1) ** 1.3        # step 4: ends at an 8th note
    k = body * env
    k = bw("low", Kk["lpHz"], k, 2)                                                                                 # step 3: dark transient
    k = dsp.eq(k, "peak", 50, 1.2, Kk["trimDb50"])                                                                 # step 7: trim ~50 Hz toward ref curve
    return fade(np.tanh(1.2 * k), 8)
kb = np.zeros(N); ghost = np.zeros(N)
Bs = R["bass"]; dn = int(Bs["duckMs"] / 1000 * SR); shp = 1 - np.clip(np.arange(dn) / dn, 0, 1) ** 2
on = lambda b: S["drumsIn"] <= b < S["brk"] or S["sec2"] <= b < S["outro"] + 1
for b in range(NB):
    if on(b):
        for q in range(4): kicks.append(tb(b) + q * BT)
for k0 in kicks: put(kb, kick(), k0); put(ghost, shp, k0)
ghost = np.clip(ghost, 0, 1)
# busy bass (needed for skill B's premise): saw pluck, offbeat 8ths + syncopated 16ths on A1 / A2, same note as kick tail (interval-safe)
bass = np.zeros(N); pat = [(0.5, 45), (1.5, 45), (1.75, 57), (2.5, 45), (3.5, 45), (3.75, 52)]
for b in range(NB):
    if on(b):
        for q, m in pat:
            L = int(0.45 * BT * SR); tt = np.arange(L) / SR
            y = dsp.osc_va(C(np.full(L, hz(m))), 0, 0.5, 0.0, SR); fc = Bs["cut"] + Bs["envAmt"] * np.exp(-tt / 0.04)
            y = svf(y, fc, 0.9, 0) * np.exp(-tt / Bs["dec"]) * np.clip(tt / 0.003, 0, 1)
            put(bass, fade(y, 12), tb(b) + q * BT); events += 1
bass = bw("low", 300, np.tanh(1.5 * nm(bass)), 2) * (1 - Bs["duckDepth"] * ghost)
lowbus = kb * Kk["level"] + bass * Bs["level"]
# ===== SKILL C: phrase-by-phrase groove with fade-ins, climax, drone-only break, sequence swap in section 2
Pc = R["perc"]; drm = np.zeros((N, 2))
def lay_in(b, start, bars=1.0): return np.clip((b - start + 1) / bars, 0.25, 1.0)       # step 3: short volume curve so layers blend in
def nzhit(L, band, tau, atk=0.002):
    tt = np.arange(L) / SR; return fade(bw("band", band, rng.standard_normal(L)) * np.exp(-tt / tau) * np.clip(tt / atk, 0, 1), 10)
def rim():  # lead perc: soft tom-like rim from the kick idea, band-passed
    L = int(0.18 * SR); tt = np.arange(L) / SR; return fade(np.sin(2 * np.pi * 420 * tt) * np.exp(-tt / 0.035) + 0.4 * nzhit(L, [1200, 3500], 0.02), 10, 1)
seqSwap = lambda b: (b - S["sec2"]) // 2 % 2 if b >= S["sec2"] else 0
for b in range(NB):
    if not on(b): continue
    for q in (1.5, 3.25): put(drm, pan2(rim(), -0.25), tb(b) + q * BT, Pc["rim"] * lay_in(b, S["drumsIn"]))
    if b >= S["hats2"]:
        for q in (0.5, 1.5, 2.5, 3.5):   # second hat layer: snappy + softer
            if seqSwap(b) == 0:
                put(drm, pan2(nzhit(int(0.08 * SR), [6000, 11000], 0.02, 0.004), 0.2), tb(b) + q * BT, Pc["hat"] * lay_in(b, S["hats2"]))
                put(drm, pan2(nzhit(int(0.12 * SR), [4000, 8000], 0.04, 0.006), -0.2), tb(b) + q * BT + 0.012, Pc["hatSoft"] * lay_in(b, S["hats2"]))
            else:   # step 7: same pattern swapped onto a ride-like sound (longer, verb added below)
                put(drm, pan2(nzhit(int(0.4 * SR), [3500, 9000], 0.16, 0.004), 0.3), tb(b) + q * BT, Pc["ride"])
    if b >= S["shaker"]:
        for q in np.arange(0, 4, 0.5):   # shakers on 8ths (no 16th rolls: rapid-clicking preference)
            put(drm, pan2(nzhit(int(0.1 * SR), [5000, 12000], 0.03, 0.015), 0.35 if q % 1 else -0.35), tb(b) + q * BT + 0.25 * BT, Pc["shaker"] * (0.7 + 0.3 * (q % 1 == 0)) * lay_in(b, S["shaker"]))
# step 4: climax = cutoff rise (macro) + high atonal noise swell; step 8: noise back after the pre-drop filter
hn = bw("high", 6000, rng.standard_normal((N, 2)), 2)
hnEnv = np.clip((t - tb(S["climax"])) / (tb(S["brk"]) - tb(S["climax"])), 0, 1) ** 2 * (t < tb(S["brk"])) + \
        0.5 * np.clip((t - tb(S["sec2"])) / BL, 0, 1) * np.clip((tb(S["sec2"] + 4) - t) / (2 * BL), 0, 1) * (t >= tb(S["sec2"]))
hn = hn * sm(hnEnv, 50)[:, None]
# step 8: sparse FX hit at a few phrase starts: hat notes into a filtered feedback delay
fx = np.zeros((N, 2))
for b in (S["climax"], S["sec2"]):
    for q in (0, 0.5, 1.0): put(fx, pan2(nzhit(int(0.08 * SR), [3000, 8000], 0.02), 0), tb(b) - BL / 2 + q * BT)
fx = np.stack(dsp.stereo_delay(C(fx[:, 0]), C(fx[:, 1]), SR, 0.75 * BT, 0.5 * BT, 0.55, 0.55, 0.1, 0.1, 1, 800, 5000, 0.2, 0.002, 0.3), 1)
drm = drm + 0.15 * nm(verb(bw("high", 500, drm), 1.4, 13)) * np.max(np.abs(drm))
# ===== mix + master
Mm = R["master"]
mix = rk * K["level"] * (1 - Mm["padDuck"] * ghost)[:, None]
mix += pan2(lowbus, 0) * 0.55 + drm + hn * Pc["noiseRise"] + nm(fx) * Pc["fxDelay"]
mix = sg.sosfiltfilt(sg.butter(2, 22, "high", fs=SR, output="sos"), mix, axis=0)
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
mix -= mix.mean(0); mix[-int(0.3 * SR):] = 0; mix[:int(0.002 * SR)] = 0
sf.write(OUT, mix.astype(np.float32), SR, subtype="PCM_24")
res = metrics.compute(mix, {"limiter_gr_db": gr_max}, R.get("category", "pad"), False, NB * BL, start_body_s=0.0, f_low=hz(26), bar_s=BL)
res["events"] = events; res["lengthSec"] = round(T, 2); res["lufs"] = round(meter.integrated_loudness(mix), 2); res["drumsInSec"] = round(tb(S["drumsIn"]), 2)
# extra checks: side <120 Hz, HF spikes, 12-40 Hz HF envelope modulation (rapid-clicking guard), kick vs bass level
side = 0.5 * (mix[:, 0] - mix[:, 1]); mid = 0.5 * (mix[:, 0] + mix[:, 1])
db = lambda x: 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)
hf = bw("high", 8000, mid, 4); he = np.abs(hf); spikes = int(np.sum(he > 8 * (sm(he, 50) + 1e-9)))
ed = sm(he, 5)[::480]; fq, P = sg.welch(ed - ed.mean(), fs=100, nperseg=1024)
res["checks"] = {"side_below_120Hz_db": round(db(bw("low", 120, side, 4)) - db(bw("low", 120, mid, 4)), 1), "hf_spikes_over_8x": spikes,
  "hf_env_12_40_vs_0_12_db": round(10 * np.log10(P[(fq >= 12) & (fq <= 40)].mean() / P[(fq > 0.2) & (fq < 12)].mean()), 1),
  "kick_vs_bass_db": round(db(kb * Kk["level"]) - db(bass * Bs["level"]), 1)}
json.dump(res, open(OUT + ".stats.json", "w"), indent=1, default=float)
print(json.dumps({"score": res["score"], "pass": res["pass"], "lufs": res["lufs"], "tp": res["extra"].get("true_peak_dbtp"), "gates": res["gates"], "subs": res["subs"], "tilt": res["extra"].get("tilt_db_oct"), "gr": round(gr_max, 2), "len": res["lengthSec"], "drumsIn": res["drumsInSec"], "checks": res["checks"]}, default=float))
