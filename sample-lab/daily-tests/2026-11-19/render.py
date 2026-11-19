#!/usr/bin/env python3
"""Daily 3-skill test 2026-11-19 "Heart Drift" (G minor, 88 BPM):
  V velocity-to-LFO-rate evolving pad (mmn6iSBKdp8): 2 triangles, smooth 'wander' LFO -> shape 100% + LP cutoff + 30% res,
    velocity -> LFO rate, HP 40 / LP 430 / res .5, amp 3-6-50%-slow, parallel dry/doubler/grain-delay/100%-wet verb lanes,
    utility -10 dB, glue verb, outer LP
  R fifth-ratio varispeed resample (EuPisVu55oU): humanised piano phrase (flams, off-grid, velocities) rendered at 2/3 length
    +7 st, then played back un-warped -7 st (x1.5 slower); low noise bed EQ'd, gentle saturation glue; repeated for strings
  K kick 'heart' sweep rules (0IgwdHg0ZwM): clean sine sweep (modest start, ~55 Hz-ref end tuned to G1 49 Hz, connected sweep),
    decay leaves silence for the bass, parallel saturation, quiet layered transient
usage: render.py recipe.json out.wav"""
import sys, os, json, numpy as np, soundfile as sf, pyloudnorm as pyln
from scipy import signal as sg
from scipy.signal import lfilter
from numba import njit
LAB = os.environ.get("LAB", "/workspace/skill-library/sample-lab"); sys.path.insert(0, LAB + "/engine")
import dsp, metrics
SR = 48000
R = json.load(open(sys.argv[1])); OUT = sys.argv[2]; rng = np.random.default_rng(R["seed"])
NB = R["bars"]; BL = 240 / R["bpm"]; BT = BL / 4; tb = lambda x: x * BL; S = R["sections"]
T = NB * BL + R["tailSec"]; N = int(T * SR); t = np.arange(N) / SR; bar = t / BL
hz = lambda m: 440 * 2 ** ((m - 69) / 12); C = np.ascontiguousarray
def bw(k, f, x, o=2): return sg.sosfilt(sg.butter(o, f, k, fs=SR, output="sos"), x, axis=0)
def pan2(x, p): return np.stack([x * np.cos((p + 1) * np.pi / 4), x * np.sin((p + 1) * np.pi / 4)], 1) * np.sqrt(2)
def put(buf, y, s, g=1.0):
    i = int(round(s * SR)); L = min(len(y), len(buf) - i)
    if L > 0 and i >= 0: buf[i:i+L] += y[:L] * g
def verb(x, rt, seed, damp=9000.0, size=1.8, mod=0.15, diff=0.75, pre=0.02):
    l, r = dsp.fdn_reverb(C(x[:, 0]), C(x[:, 1]), SR, float(rt), size, damp, pre, mod, diff, 0.0, seed); return np.stack([l, r], 1)
nm = lambda x: x / (np.max(np.abs(x)) + 1e-9)
def sm(x, ms): a = np.exp(-1 / (ms / 1000 * SR)); return lfilter([1 - a], [1, -a], x, axis=0)
def gate(b0, b1, xf_ms=300): return sm(((bar >= b0) & (bar < b1)).astype(float), xf_ms)
def resamp(x, ratio):  # un-warped repitch: ratio<1 -> slower + lower
    n = int(len(x) / ratio); return np.interp(np.arange(n) * ratio, np.arange(len(x)), x)
@njit(cache=True)
def svf_q(x, fc, q, sr):  # TPT SVF LP with per-sample cutoff AND resonance (Q)
    n = x.shape[0]; y = np.zeros(n); ic1 = 0.0; ic2 = 0.0
    for i in range(n):
        g = np.tan(np.pi * min(max(fc[i], 20.0), 0.45 * sr) / sr); k = 1.0 / q[i]
        a1 = 1.0 / (1.0 + g * (g + k)); a2 = g * a1; a3 = g * a2
        v3 = x[i] - ic2; v1 = a1 * ic1 + a2 * v3; v2 = ic2 + a2 * ic1 + a3 * v3
        ic1 = 2.0 * v1 - ic1; ic2 = 2.0 * v2 - ic2; y[i] = v2
    return y
events = 0; CH = R["chords"]; BP = CH["barsPer"]; NCH = len(CH["names"])
# ================= V: velocity-to-LFO-rate evolving pad
V = R["pad"]
def wander(L, rate_hz, seed):  # smooth random (cosine-interpolated random points), NOT sample-and-hold
    r = np.random.default_rng(seed); ph = np.arange(L) / SR * rate_hz; k = ph.astype(int); fr = ph - k
    pts = r.uniform(-1, 1, k[-1] + 3); w = (1 - np.cos(np.pi * fr)) / 2; return pts[k] * (1 - w) + pts[k + 1] * w
def adsr(L, hold, a, d, s, r):
    tt = np.arange(L) / SR; e = np.where(tt < a, np.sin(np.pi / 2 * tt / a) ** 2, s + (1 - s) * np.exp(-(tt - a) / (d / 3)))
    lvl = np.interp(hold, tt, e); e = np.where(tt < hold, e, lvl * np.exp(-(tt - hold) / (r / 4)))
    fw = int(0.05 * SR); e[-fw:] *= np.linspace(1, 0, fw); return e
padM = np.zeros(N); ci = 0
for b0 in range(0, NB, BP):
    c = (b0 // BP) % NCH; vel = CH["velocity"][c]; hold = BP * BL; L = int((hold + V["rel"]) * SR)
    rate = V["lfoBaseHz"] * 2 ** (V["velToRateOct"] * (vel - 0.5))  # velocity -> LFO rate, full depth
    for i, m in enumerate(CH["pad"][c]):
        lfo = wander(L, rate, R["seed"] * 100 + ci * 10 + i)
        f = np.full(L, hz(m))
        a = dsp.osc_va(f, 2, 0.5, 0.17 * i, SR); bsc = dsp.osc_va(f, 2, 0.5, 0.5 + 0.11 * i, SR)  # two triangles, same octave
        x = 0.55 * a + 0.45 * bsc
        sh = V["shapeDepth"] * 0.5 * (lfo + 1)  # LFO -> osc shape 100% (triangle fold)
        x = np.sin(np.pi / 2 * x * (1 + 2.0 * sh)) * (0.6 + 0.4 * vel)
        fc = V["lpHz"] * 2 ** (V["lpModOct"] * lfo); q = V["res"] + 1.0 + V["resModAmt"] * 1.5 * lfo  # Q ~1.5 +/-
        y = svf_q(C(x), C(fc), C(q), SR) * adsr(L, hold, V["atk"], V["dec"], V["sus"], V["rel"])
        put(padM, y, tb(b0)); events += 1
    ci += 1
padM = bw("high", V["hpHz"], padM, 2)
padS = pan2(padM, 0)
dbl = np.stack(dsp.chorus(C(padM), C(padM), SR, 0, 0.12, 0.25, float(V["doublerMs"]), 0.0, 1.0, 1.0, 0.25, 0.0), 1)
dbl = dbl - dbl.mean(1, keepdims=True) * 0.9  # doubler lane = strong sides
def grain_delay(x, spray_ms, fb, seed, gms=90, hop_ms=30, base_ms=110):
    r = np.random.default_rng(seed); g = int(gms / 1000 * SR); w = np.hanning(g); out = np.zeros((len(x), 2)); src = x
    for p in range(3):
        y = np.zeros((len(x), 2))
        for c0 in range(0, len(x) - g, int(hop_ms / 1000 * SR)):
            d = int((base_ms + r.uniform(0, spray_ms)) / 1000 * SR); s0 = c0 - d
            if s0 < 0: continue
            y[c0:c0 + g] += pan2(src[s0:s0 + g] * w, r.uniform(-0.6, 0.6))
        y *= 0.5; out += y * fb ** p; src = y.mean(1) * 2
    return out
grn = grain_delay(padM, V["grainSprayMs"], V["grainFb"], 7)
pv = verb(padS, 7.0, 11, 5000.0, 2.4)
LN = V["lanes"]
padR = LN["dry"] * nm(padS) + LN["doubler"] * nm(dbl) + LN["grain"] * nm(grn) + LN["verb"] * nm(pv)
padR *= 10 ** (V["utilityDb"] / 20)
padR = padR + V["glueMix"] * nm(verb(padR, V["glueRt"], 13, 6000.0, 2.0)) * np.max(np.abs(padR))
padR = bw("low", V["outerLpHz"], padR, 2)
# V optional outer lane: looped smooth 'foley' air bed (noise, slow swell), lightly bit-reduced, mixed low under the pad
fol = bw("band", [1800, 9000], dsp.noise(N, "pink", np.random.default_rng(31)), 2)
fol = np.round(fol / (np.max(np.abs(fol)) + 1e-9) * 2048) / 2048 * (0.6 + 0.4 * np.sin(2 * np.pi * t / (4 * BL)) ** 2)
fol = np.stack([fol, np.roll(fol, int(0.37 * SR))], 1); fol = bw("low", 10000, fol, 2)
padR = padR + nm(fol) * np.max(np.abs(padR)) * V["foleyLvl"]
# ================= R: fifth-ratio varispeed resample
RV = R["varispeed"]; cmp = RV["compress"]; up = RV["upSt"]
def piano_note(m, v, dur):
    f = hz(m); L = int((dur + 1.6) * SR); tt = np.arange(L) / SR; y = np.zeros(L)
    for k in range(1, 17):
        fk = f * k * np.sqrt(1 + 0.0004 * k * k)
        if fk > 16000: break
        tau = 2.6 / (1 + 0.45 * k) * (261.0 / max(f, 130.0)) ** 0.35
        y += np.sin(2 * np.pi * fk * tt + 0.3 * k) * (1 / k ** 1.0) * (v ** (0.4 * k / 3)) * np.exp(-tt / tau)
    y *= np.minimum(tt / 0.003, 1) * np.where(tt < dur, 1.0, np.exp(-(tt - dur) / 0.12))  # damper
    y[-480:] *= np.linspace(1, 0, 480); return y * v
def strings_note(m, dur):
    f = hz(m); L = int((dur + 1.2) * SR); tt = np.arange(L) / SR; y = np.zeros(L)
    for dc in (-5, 0, 5):  # static detune, no vibrato
        y += dsp.osc_va(np.full(L, f * 2 ** (dc / 1200)), 0, 0.5, (dc + 5) / 13, SR)
    e = np.clip(tt / 0.45, 0, 1) ** 2 * np.where(tt < dur, 1.0, np.exp(-(tt - dur) / 0.35)); e[-480:] *= np.linspace(1, 0, 480)
    return bw("low", 2600, y, 2) * e / 3
def body(x):  # instrument body/mic colour in the source render (gets shifted down a fifth by the varispeed)
    x = dsp.eq(x, "peak", 2400, 0.9, 4.0) if hasattr(dsp, "eq") else x
    return bw("low", 12000, bw("high", 70, x, 2), 2)
nPh = 9 * BL * cmp  # clip one bar longer than the 8-bar phrase, compressed to 2/3
def render_phrase(kind):
    buf = np.zeros(int(nPh * SR) + SR); j = 0; nev = 0
    if kind == "piano":
        for b, beat, m, d, v in RV["melody"]:
            s = (b * BL + beat * BT + RV["jitterMs"][j % len(RV["jitterMs"])] / 1000) * cmp; j += 1
            put(buf, piano_note(m + up, v, d * BT * cmp * 0.95), max(s, 0)); nev += 1
        for c in range(4):  # left hand: flammed chord at chord start + soft repeat one bar later
            for rep, vv in ((0, 0.6), (1, 0.42)):
                notes = [CH["bass"][c] + 24, CH["bass"][c] + 31, CH["pad"][c][1] + 12 if CH["pad"][c][1] + 12 < 72 else CH["pad"][c][1]]
                for k, m in enumerate(notes):
                    s = ((2 * c + rep) * BL + RV["flamMs"][k] / 1000 + RV["jitterMs"][(j + k) % 12] / 1000) * cmp
                    put(buf, piano_note(m + up, vv - 0.05 * k, BL * cmp * 0.9), max(s, 0)); nev += 1
                j += 1
    else:
        b = 0
        for notes, nbar in RV["strings"]:
            for m in notes: put(buf, strings_note(m + up, nbar * BL * cmp * 0.97), b * BL * cmp); nev += 1
            b += nbar
    buf = body(buf)
    return resamp(buf, cmp), nev  # un-warped playback a fifth down: 3:2 -> back to ~original tempo/pitch
pia, n1 = render_phrase("piano"); strg, n2 = render_phrase("strings"); events += 2 * n1 + n2
grp = np.zeros(N)
for b0 in (S["pianoIn"], S["stringsIn"]): put(grp, pia, tb(b0), R["levels"]["piano"])
put(grp, strg, tb(S["stringsIn"]), R["levels"]["strings"])
nzb = bw("low", 7000, bw("high", 250, dsp.noise(N, "pink", rng), 2), 2)
nzb = nm(nzb) * 10 ** (RV["noiseBedDb"] / 20) * gate(S["pianoIn"], S["drumsOut"] + 1.5, 600)
grp = np.tanh(RV["satDrive"] * (grp + nzb)) / RV["satDrive"]  # gentle glue (crackle 0)
grpS = pan2(grp, -0.1); grpS = nm(grpS) * 0.8 + nm(verb(grpS, 3.0, 29, 5500.0, 1.8)) * 0.4
# ================= K: kick heart
K = R["kick"]
def kick_heart():
    L = int(K["gateSec"] * SR); tt = np.arange(L) / SR
    f = K["endHz"] + (K["startHz"] - K["endHz"]) * np.exp(-tt / (K["sweepTauMs"] / 1000))
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / K["decayTau"]) * np.minimum(tt / 0.002, 1)
    fw = int(0.08 * SR); y[-fw:] *= np.cos(np.linspace(0, np.pi / 2, fw)) ** 2; return y
heart = kick_heart()
sat = bw("high", 120, np.tanh(K["parSatDrive"] * heart), 2) * 10 ** (K["parSatDb"] / 20)  # parallel, heart stays clean
Lt = int(0.012 * SR); tt = np.arange(Lt) / SR
trn = bw("low", 9000, bw("high", 2500, np.random.default_rng(5).standard_normal(Lt), 2), 2) * np.minimum(tt / 0.0015, 1) * np.exp(-tt / 0.0035)
k1 = heart + sat; k1[:Lt] += trn * 10 ** (K["transientDb"] / 20)
kick = np.zeros(N); sn = np.zeros(N); bass = np.zeros(N)
def snare1():
    L = int(0.35 * SR); tt_ = np.arange(L) / SR
    y = 0.5 * np.sin(2 * np.pi * 196 * tt_) * np.exp(-tt_ / 0.05) + bw("band", [900, 4000], rng.standard_normal(L), 2) * np.exp(-tt_ / 0.08)
    y *= np.minimum(tt_ / 0.012, 1); y = bw("low", 4000, y, 2); y[-480:] *= np.linspace(1, 0, 480); return y
for b in range(S["drumsIn"], S["drumsOut"]):
    for q in (0, 2): put(kick, k1, tb(b) + q * BT); events += 1
    if b >= S["pianoIn"]:
        for q in (1, 3): put(sn, snare1(), tb(b) + q * BT); events += 1
# bass sits in the silence the kick heart leaves: sustained root, ducked by kick
for b0 in range(S["drumsIn"], S["drumsOut"], BP):
    c = (b0 // BP) % NCH; L = int(BP * BL * SR); f = hz(CH["bass"][c] + 12) if CH["bass"][c] < 31 else hz(CH["bass"][c]); tt_ = np.arange(L) / SR
    y = (np.sin(2 * np.pi * f * tt_) + 0.3 * np.sin(4 * np.pi * f * tt_)) * np.minimum(tt_ / 0.03, 1) * np.minimum((BP * BL - tt_) / 0.05, 1)
    put(bass, y, tb(b0)); events += 1
kenv = sm(sm(np.abs(heart if False else kick), 3), 120); kenv /= kenv.max() + 1e-9
LV = R["levels"]
bass *= 1 - (1 - 10 ** (-LV["bassDuckDb"] / 20)) * np.clip(kenv * 2.5, 0, 1)
snS = pan2(sn, 0.05); snS = nm(snS) * 0.6 + nm(verb(snS, 2.6, 37, 5000.0, 1.8)) * 0.5
duck = lambda d: (1 - (1 - 10 ** (-d / 20)) * np.clip(kenv * 2.5, 0, 1))[:, None]
if os.environ.get("DBG"):
    def spk(x):
        x = x.mean(1) if x.ndim == 2 else x; he = np.abs(bw("high", 8000, x, 4)); return int(np.sum(he > 8 * (sm(he, 50) + 1e-9)))
    for nmx, x in (("pad", padR), ("grp", grpS), ("kick", kick), ("snare", snS)): print(nmx, spk(x))
mix = nm(padR) * LV["pad"] * duck(2.0) + nm(grpS) * duck(1.0) + pan2(nm(bass) * LV["bass"], 0) / np.sqrt(2) \
    + pan2(nm(kick) * LV["kick"], 0) / np.sqrt(2) + snS * LV["snare"]
Mm = R["master"]
mix = sg.sosfiltfilt(sg.butter(2, 22, "high", fs=SR, output="sos"), mix, axis=0)
Mn = 0.5 * (mix[:, 0] + mix[:, 1]); Sd = 0.5 * (mix[:, 0] - mix[:, 1])
Sd = sg.sosfiltfilt(sg.butter(4, Mm["sideHpHz"], "high", fs=SR, output="sos"), Sd); mix = np.stack([Mn + Sd, Mn - Sd], 1)
mix *= (np.clip(t / 1.5, 0, 1) ** 2)[:, None]
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
res = metrics.compute(mix, {"limiter_gr_db": gr_max}, R.get("category", "pad"), False, NB * BL, start_body_s=0.0, f_low=hz(28), bar_s=BL)
res["events"] = events; res["lengthSec"] = round(T, 2); res["lufs"] = round(meter.integrated_loudness(mix), 2); res["drumsInSec"] = round(tb(S["drumsIn"]), 2)
side = 0.5 * (mix[:, 0] - mix[:, 1]); mid = 0.5 * (mix[:, 0] + mix[:, 1]); db = lambda x: 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)
hf = bw("high", 8000, mid, 4); he = np.abs(hf); spikes = int(np.sum(he > 8 * (sm(he, 50) + 1e-9)))
ed = sm(he, 5)[::480]; fq, Pw = sg.welch(ed - ed.mean(), fs=100, nperseg=1024)
sec = lambda b0, b1: mix[int(tb(b0) * SR):int(tb(b1) * SR)]
res["checks"] = {"side_below_120Hz_db": round(db(bw("low", 120, side, 4)) - db(bw("low", 120, mid, 4)), 1), "hf_spikes_over_8x": spikes,
  "hf_env_12_40_vs_0_12_db": round(10 * np.log10(Pw[(fq >= 12) & (fq <= 40)].mean() / Pw[(fq > 0.2) & (fq < 12)].mean()), 1),
  "lufs_intro_A_B_C_outro": [round(meter.integrated_loudness(sec(a, b)), 1) for a, b in ((0, 4), (4, 12), (12, 20), (20, 28), (28, 30))]}
json.dump(res, open(OUT + ".stats.json", "w"), indent=1, default=float)
print(json.dumps({"score": res["score"], "pass": res["pass"], "lufs": res["lufs"], "tp": res["extra"].get("true_peak_dbtp"), "gates": res["gates"], "subs": res["subs"], "tilt": res["extra"].get("tilt_db_oct"), "gr": round(gr_max, 2), "len": res["lengthSec"], "drumsIn": res["drumsInSec"], "checks": res["checks"]}, default=float))
