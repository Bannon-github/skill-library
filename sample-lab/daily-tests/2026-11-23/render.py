#!/usr/bin/env python3
"""Daily 3-skill test 2026-11-23 "Pedal Lever" (D minor, 92 BPM): light-tension ABA cue form (yMJaUS776yQ) + melodic cells/octatonic tension (efnKT5pHqUo) + sus4 / bVI-bVII pedal tension-release (PUycGHv-2Jo). usage: render.py recipe.json out.wav"""
import sys, os, json, numpy as np, soundfile as sf, pyloudnorm as pyln
from scipy import signal as sg
from scipy.signal import lfilter
LAB = os.environ.get("LAB", "/workspace/skill-library/sample-lab"); sys.path.insert(0, LAB + "/engine")
import dsp, metrics
SR = 48000
R = json.load(open(sys.argv[1])); OUT = sys.argv[2]; rng = np.random.default_rng(R["seed"])
NB = R["bars"]; BL = 240 / R["bpm"]; BT = BL / 4; tb = lambda x: x * BL
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
def gate(b0, b1, xf_ms=30): return sm(sm(((bar >= b0) & (bar < b1)).astype(float), xf_ms / 2), xf_ms / 2)
events = 0
from numba import njit
def blep(p, dt):
    out = np.zeros_like(p); a = p < dt; x = p[a] / dt[a]; out[a] = x + x - x * x - 1
    b = p > 1 - dt; x = (p[b] - 1) / dt[b]; out[b] = x * x + x + x + 1; return out
def saw_osc(f, ph0=0.0):
    dt = f / SR; ph = (ph0 + np.cumsum(dt)) % 1.0; return 2 * ph - 1 - blep(ph, dt)
SEC = R["sections"]; LV = R["levels"]
def sec_of(b):
    for s in SEC:
        if s["b"][0] <= b < s["b"][1]: return s
    return SEC[-1]
on = lambda name, b: name in sec_of(b)["els"]
def chord_at(b):
    for c in R["chords"]:
        if c[0] <= b < c[1]: return c
    return R["chords"][-1]
from numba import njit
def blep(p, dt):
    out = np.zeros_like(p); a = p < dt; x = p[a] / dt[a]; out[a] = x + x - x * x - 1
    b = p > 1 - dt; x = (p[b] - 1) / dt[b]; out[b] = x * x + x + x + 1; return out
def saw_osc(f, ph0=0.0):
    dt = f / SR; ph = (ph0 + np.cumsum(dt)) % 1.0; return 2 * ph - 1 - blep(ph, dt)
def fade(y, ms=8):
    k = min(int(ms / 1000 * SR), len(y) // 2); y[-k:] *= np.cos(np.linspace(0, np.pi / 2, k)) ** 2; return y
def env_ad(L, atk, dec, hold=None):
    tt = np.arange(L) / SR; e = np.minimum(tt / atk, 1) * np.exp(-tt / dec); return fade(e, 10), tt
st = lambda b, s16: tb(b) + s16 * BT / 4
# ================= drone pad (steady pitch; movement = slow filter + level only, no bends)  [ABA step 1, constraint: no drone pitch bend]
P = R["pad"]; padL = np.zeros(N); padR = np.zeros(N)
for b0, b1, nmz, tones, _ in R["chords"]:
    s0 = tb(b0); held = tb(b1) - s0; i0 = int(s0 * SR); i1 = min(int((tb(b1) + P["rel"] * 2.5) * SR), N); tt = t[i0:i1] - s0
    env = (1 - np.exp(-tt / (P["atk"] / 3))) * np.where(tt < held, 1.0, np.exp(-(tt - held) / (P["rel"] / 3))) * np.minimum(tt / 0.01, 1)
    tl = [(m, 1.0) for m in tones]
    if P["octaveBars"][0] <= b0 < P["octaveBars"][1]: tl += [(m + 12, P["octaveGain"]) for m in tones[1:3]]  # B: add an octave to the pad
    for m, g in tl:
        for v in (0, 1):
            f = np.full(i1 - i0, hz(m) * 2 ** (((v - 0.5) * P["spreadCents"]) / 1200))
            (padL if v == 0 else padR)[i0:i1] += saw_osc(f, rng.uniform()) * env * g; events += 1
pad = np.stack([padL, padR], 1); fc = P["lpHz"] * (1 + P["lfoDepth"] * np.sin(2 * np.pi * P["lfoHz"] * t))
pad = np.stack([dsp.svf(C(pad[:, c]), C(fc), 0.7, 0, SR) for c in (0, 1)], 1); pad = bw("high", P["hpHz"], pad, 2); pad = nm(pad)
# ================= mallet lead (2-op FM, fixed pitch) + call/response voices
LD = R["lead"]
def mallet(m, dur, g=1.0):
    L = int((dur + 1.2) * SR); e, tt = env_ad(L, 0.008, LD["decay"] * (1 + dur)); f = hz(m)
    idx = LD["fmIndex"] * np.exp(-tt / LD["fmDecay"]); y = np.sin(2 * np.pi * f * tt + idx * np.sin(2 * np.pi * f * LD["fmRatio"] * tt))
    return y * e * g
def piano(m, dur, g=1.0):
    L = int((dur + 1.5) * SR); tt = np.arange(L) / SR; f = hz(m); y = np.zeros(L)
    for k, a in ((1, 1), (2, .5), (3, .25), (4, .12), (5, .06)): y += a * np.sin(2 * np.pi * f * k * 1.0006 ** (k - 1) * tt) * np.exp(-tt / (0.9 / k ** 0.7))
    return fade(y * np.minimum(tt / 0.003, 1), 20) * g
def pluck(m, dur, g=1.0):  # metal/tank-drum-like: inharmonic partials, soft attack
    L = int(1.2 * SR); tt = np.arange(L) / SR; f = hz(m)
    y = sum(a * np.sin(2 * np.pi * f * r * tt) * np.exp(-tt / d) for r, a, d in ((1, 1, .5), (2.76, .4, .25), (5.4, .15, .12)))
    return fade(y * np.minimum(tt / 0.004, 1), 20) * g
lead = np.zeros(N); pno = np.zeros(N); plk = np.zeros(N); chi = np.zeros(N)
H = R["hook"]; HD = R["hookDom"]
for b in range(0, R["bars"], 2):
    if not on("lead", b) or b == 23: continue
    hk = HD if 6 <= b < 8 else H
    for s16, m, d in hk:
        bb = b + s16 // 16
        if not on("lead", bb) or bb == 23: continue
        s0 = st(b, s16); dur = d * BT / 4
        put(lead, mallet(m, dur), s0); events += 1
        if b >= LD["octaveFrom"] and b not in (16, 18, 20, 22): put(lead, mallet(m + 12, dur, LD["octGain"]), s0)   # gear: octaves
        if b >= LD["tripleFrom"]: put(lead, mallet(m + 24, dur, LD["tripleGain"]), s0)  # triple, lower velocity going up
    if on("piano", b + 1) and b >= 8 and not (16 <= b < 24):
        for s16, m, d in R["pianoResp"]: put(pno, piano(m, d * BT / 4), st(b, s16)); events += 1
    if on("pluck", b + 1):
        for s16, m, d in R["pluckResp"]: put(plk, pluck(m, d * BT / 4), st(b, s16)); events += 1
CB = R["cliff"]; put(lead, mallet(CB["midi"], BL * 0.9, 1.0), tb(CB["bar"])); put(lead, mallet(74, BL, 1.0), tb(30)); events += 2
# breakdown: piano sprinkles the hook (bars 16-18), then melodic cells (bars 18-22 and in the A+B return)
for s16, m, d in H[:4]: put(pno, piano(m - 12, d * BT / 4, 0.8), st(16, s16)); events += 1
cell = R["cell"]
for b in list(range(*R["cellBars"])) + list(range(24, 30)):
    for q in range(8):  # steady 8ths, same 4-pitch set reordered (repetition legitimizes)
        put(pno, piano(cell[q % 4] - 12, BT / 2, 0.55 if b >= 24 else 0.7), tb(b) + q * BT / 2); events += 1
CU = R["cellUpThirds"]
for i, b in enumerate(range(*CU["bars"])):
    for h in range(2):
        tr = CU["steps"][i * 2 + h]
        for q in range(4): put(chi, mallet(CU["base"][q] - 12 + tr, BT / 2, 0.6), tb(b) + h * BL / 2 + q * BT / 2); events += 1
# ================= rhythmic engine: dotted bass pulse on roots, offbeat pulses (nothing stacked on strong downbeats)
PU = R["pulse"]; p1 = np.zeros(N); p2 = np.zeros(N); bass = np.zeros(N); sub = np.zeros(N)
def pulse(m, g=1.0):
    L = int(0.5 * SR); e, tt = env_ad(L, 0.009, PU["decay"]); y = saw_osc(np.full(L, hz(m))) * e; return y * g
for b in range(R["bars"]):
    c = chord_at(b + 0.01); tones = c[3]
    for k, s16 in enumerate(PU["p1steps"]):
        if on("p1", b): put(p1, pulse(tones[1] if k % 2 == 0 else tones[2]), st(b, s16)); events += 1
    for k, s16 in enumerate(PU["p2steps"]):
        if on("p2", b): put(p2, pulse(tones[-1] + 12 if k % 2 == 0 else tones[-2] + 12), st(b, s16)); events += 1
    for s16 in R["bassSteps"]:
        if on("bass", b):
            L = int(0.42 * SR); e, tt = env_ad(L, 0.008, 0.35); f = hz(c[4] + 12 if c[4] < 36 else c[4])
            put(bass, (np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(4 * np.pi * f * tt)) * e, st(b, s16)); events += 1
    if on("sub", b):
        L = int(BL * SR); tt = np.arange(L) / SR; put(sub, fade(np.sin(2 * np.pi * hz(c[4]) * tt) * np.minimum(tt / 0.05, 1), 60), tb(b))
pulses = nm(bw("low", PU["lp"], pan2(nm(p1), -0.35) + pan2(nm(p2) * 0.8, 0.35), 2))
# ================= drums: soft kick, light backbeat, booms, riser, roll / reverse swell
K = R["kick"]
def kick1(v=1.0):
    L = int(K["gate"] * SR); tt = np.arange(L) / SR; f = K["endHz"] + (K["startHz"] - K["endHz"]) * np.exp(-tt / (K["tauMs"] / 1000))
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / K["decay"]) * np.minimum(tt / 0.004, 1); return fade(y, 60) * v
kick = np.zeros(N); clap = np.zeros(N); boom = np.zeros(N)
for b in range(R["bars"]):
    if on("kick", b):
        for s16 in (K["denseSteps"] if b >= 24 else K["steps"]): put(kick, kick1(1.0 if s16 == 0 else 0.75), st(b, s16)); events += 1
    if on("clap", b):
        for s16 in (4, 12):
            L = int(0.35 * SR); tt = np.arange(L) / SR
            y = bw("band", [700, 2400], rng.standard_normal(L), 2) * np.exp(-tt / 0.08) * np.minimum(tt / 0.006, 1); put(clap, fade(y, 20), st(b, s16)); events += 1
for b in R["booms"]:
    L = int(3.0 * SR); tt = np.arange(L) / SR; f = 34 + 40 * np.exp(-tt / 0.15)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.9) * np.minimum(tt / 0.005, 1) + 0.3 * bw("low", 300, rng.standard_normal(L), 2) * np.exp(-tt / 0.25)
    put(boom, fade(y, 200), tb(b)); events += 1
rs = np.zeros((N, 2))
def swell(b0, b1, f0, f1, rev=False):
    i0, i1 = int(tb(b0) * SR), int(tb(b1) * SR); L = i1 - i0; nz = rng.standard_normal((L, 2)); fc = f0 * (f1 / f0) ** np.linspace(0, 1, L)
    y = np.stack([dsp.svf(C(nz[:, c]), C(fc), 1.0, 1, SR) for c in (0, 1)], 1) * (np.linspace(0, 1, L) ** 2)[:, None]
    y[-int(0.03 * SR):] *= np.linspace(1, 0, int(0.03 * SR))[:, None]; rs[i0:i1] += nm(y)
swell(15, 16, 500, 4500); swell(23, 24, 300, 5000)   # cymbal-swell riser into B, roll/whoosh into the release
# ================= stereo delay on lead/pluck/cell voice: L dotted 1/8, R 1/4, LP inside the loop (each echo darker); sends automated off
@njit(cache=True)
def sdelay(x, d, fb, a):
    n = x.shape[0]; y = np.zeros(n); buf = np.zeros(n); z = 0.0
    for i in range(n):
        r = buf[i - d] if i >= d else 0.0; z = z + a * (r - z); y[i] = z; buf[i] = x[i] + fb * z
    return y
DL = R["delay"]; sendG = np.ones(N)
for a_, b_ in DL["offBars"]: sendG *= 1 - gate(a_, b_, 120)
snd = (nm(lead) + 0.6 * nm(plk) + 0.5 * nm(chi)) * sendG; aLP = 1 - np.exp(-2 * np.pi * DL["lpHz"] / SR)
dly = np.stack([sdelay(C(snd), int(DL["Lbeats"] * BT * SR), DL["fb"], aLP), sdelay(C(snd), int(DL["Rbeats"] * BT * SR), DL["fb"], aLP)], 1)
dly *= sm(sendG, 300)[:, None]
leadS = pan2(nm(lead), 0.1); kenv = sm(sm(np.abs(kick), 3), 120); kenv /= kenv.max() + 1e-9
mel = leadS * LV["lead"] + pan2(nm(pno), -0.2) * LV["piano"] + pan2(nm(plk), 0.4) * LV["pluck"] + pan2(nm(chi), 0.25) * LV["cellhi"] + nm(dly) * LV["delay"]
vb = verb(C(mel + pad * 0.3), 3.4, 41, 6500.0, 1.9) * sm(sendG, 400)[:, None]
mix = (pad * LV["pad"] + mel + pulses * (LV["p1"] + LV["p2"]) + nm(vb) * LV["verb"] + nm(rs) * LV["riser"]) * (1 - 0.12 * np.clip(kenv * 2.5, 0, 1))[:, None]
bass *= 1 - (1 - 10 ** (-LV["bassDuckDb"] / 20)) * np.clip(kenv * 2.5, 0, 1)
mix += pan2(nm(bass) * LV["bass"] + nm(sub) * LV["sub"] + nm(kick) * LV["kick"] + nm(boom) * LV["boom"], 0) / np.sqrt(2) + pan2(nm(clap), 0) * LV["clap"]
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
res["events"] = events; res["lengthSec"] = round(T, 2); res["lufs"] = round(meter.integrated_loudness(mix), 2); res["drumsInSec"] = round(tb(R["drumsIn"]), 2)
side = 0.5 * (mix[:, 0] - mix[:, 1]); mid = 0.5 * (mix[:, 0] + mix[:, 1]); db = lambda x: 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)
hf = bw("high", 8000, mid, 4); he = np.abs(hf); spikes = int(np.sum(he > 8 * (sm(he, 50) + 1e-9)))
def cent(x):
    f_, tt_, Z = sg.stft(x.mean(1), SR, nperseg=4800); P_ = np.abs(Z) ** 2; c_ = (P_ * f_[:, None]).sum(0) / (P_.sum(0) + 1e-12); return float(np.median(c_))
blocks = [s["b"] for s in SEC]; sec = lambda b0, b1: mix[int(tb(b0) * SR):int(tb(b1) * SR)]
cents = [cent(sec(a, b)) for a, b in blocks]
res["checks"] = {"side_below_120Hz_db": round(db(bw("low", 120, side, 4)) - db(bw("low", 120, mid, 4)), 1), "hf_spikes_over_8x": spikes,
  "section_lufs": [round(meter.integrated_loudness(sec(a, b)), 1) if b - a >= 2 else None for a, b in blocks], "section_centroid_hz": [round(c) for c in cents],
  "centroid_span_oct": round(float(np.log2(max(cents) / min(cents))), 2)}
json.dump(res, open(OUT + ".stats.json", "w"), indent=1, default=float)
print(json.dumps({"score": res["score"], "pass": res["pass"], "lufs": res["lufs"], "tp": res["extra"].get("true_peak_dbtp"), "gates": res["gates"], "subs": res["subs"], "tilt": res["extra"].get("tilt_db_oct"), "gr": round(gr_max, 2), "len": res["lengthSec"], "drumsIn": res["drumsInSec"], "checks": res["checks"]}, default=float))
