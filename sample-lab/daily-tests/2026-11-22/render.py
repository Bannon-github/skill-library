#!/usr/bin/env python3
"""Daily 3-skill test 2026-11-22 "Phase Rumble" (F minor, 96 BPM): phaser pad depth chain (nIGiY1jYgWM) + reverb/rumble kick (q6TxzspNL9Q) + climax/break structures (dGGMbqe4QYQ). usage: render.py recipe.json out.wav"""
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
SEC = R["sections"]
def sec_of(b):
    for s in SEC:
        if s["b"][0] <= b < s["b"][1]: return s
    return SEC[-1]
def el_gate(name, xf=40):  # 0/1 per-sample gate for an element from the section list (minus turnarounds / kickOut)
    g = np.zeros(N)
    for s in SEC:
        if name in s["els"]:
            b1 = s.get("kickOut", s["b"][1]) if name == "kick" else s["b"][1]
            g += ((bar >= s["b"][0]) & (bar < b1))
            if "turnaround" in s and name not in ("pad", "peaks", "lead"): g -= ((bar >= s["turnaround"][0]) & (bar < s["turnaround"][1]))
    return sm(sm(np.clip(g, 0, 1), xf / 2), xf / 2)
@njit(cache=True)
def phaser_f(x, f, stages, fb, sr):  # 12-stage 1st-order all-pass chain, per-sample centre freq, feedback = resonance
    n = x.shape[0]; zs = np.zeros(stages); y = np.zeros(n); last = 0.0
    for i in range(n):
        t_ = np.tan(np.pi * f[i] / sr); a = (t_ - 1.0) / (t_ + 1.0); v = x[i] + fb * last
        for s in range(stages):
            o = a * v + zs[s]; zs[s] = v - a * o; v = o
        last = v; y[i] = v
    return y
# ================= pad source (2 detuned saw voices, L/R = stereo source for phaser spread)
CH = R["chords"]; P = R["pad"]; padL = np.zeros(N); padR = np.zeros(N)
for b0, b1, ci in CH["segments"]:
    s0 = tb(b0); s1 = tb(b1); i0 = int(s0 * SR); i1 = min(int((s1 + P["rel"] * 2.5) * SR), N); tt = t[i0:i1] - s0; held = s1 - s0
    atk = P["atk"] if ci != 6 else (s1 - s0) * 0.8  # hang bar: one slow swell
    env = (1 - np.exp(-tt / (atk / 3))) * np.where(tt < held, 1.0, np.exp(-(tt - held) / (P["rel"] / 3))) * np.minimum(tt / 0.01, 1)
    for m in CH["tones"][ci]:
        for v in (0, 1):
            f = np.full(i1 - i0, hz(m) * 2 ** (((v - 0.5) * P["spreadCents"]) / 1200))
            (padL if v == 0 else padR)[i0:i1] += saw_osc(f, rng.uniform()) * env; events += 1
pad = np.stack([padL, padR], 1); pad = bw("low", P["lpHz"], pad, 2); pad = bw("high", P["hpHz"], pad, 2)
# ================= S1 phaser: 12 stages, high resonance, RAMP-UP modulator looped every 4 bars (short fall to avoid a zipper reset)
PH = R["phaser"]
def ramp(off):
    r = (bar / PH["cycleBars"] + off) % 1.0; ff = PH["fallFrac"]
    return np.where(r < 1 - ff, r / (1 - ff), 0.5 + 0.5 * np.cos(np.pi * (r - (1 - ff)) / ff))
rL = ramp(0.0); rR = ramp(PH["spreadPhase"])  # spread: R channel ramp offset (stereo only in the phaser)
phL = phaser_f(C(pad[:, 0]), C(PH["loHz"] * 2 ** (rL * PH["octaves"])), PH["stages"], PH["fb"], SR)
phR = phaser_f(C(pad[:, 1]), C(PH["loHz"] * 2 ** (rR * PH["octaves"])), PH["stages"], PH["fb"], SR)
padP = (1 - PH["mix"]) * pad + PH["mix"] * np.stack([phL, phR], 1); padP = nm(padP)
padP *= el_gate("pad", 200)[:, None]
# ================= S2 delay used as a filter: mono echo, narrow resonant HP + LP peaks on sine LFOs moving in opposite directions
PK = R["peaks"]; mono = padP.mean(1); d = int(PK["delayBeats"] * BT * SR); dl = np.zeros(N)
for k in range(1, 8): dl[d * k:] += (PK["fb"] ** (k - 1)) * mono[:N - d * k]
on = sm(np.clip((bar - PK["onsetBars"] / 2) / PK["onsetBars"], 0, 1), 200)  # LFO onset delayed by an envelope
s1_ = np.sin(2 * np.pi * PK["hpRate"] * t); s2_ = np.sin(2 * np.pi * PK["lpRate"] * t)
hpF = np.sqrt(PK["hpHz"][0] * PK["hpHz"][1]) * (PK["hpHz"][1] / PK["hpHz"][0]) ** (0.5 * s1_ * on)
lpF = np.sqrt(PK["lpHz"][0] * PK["lpHz"][1]) * (PK["lpHz"][1] / PK["lpHz"][0]) ** (-0.5 * s2_ * on)  # opposite direction
pk = dsp.svf(C(dsp.svf(C(dl), C(hpF), PK["hpQ"], 2, SR)), C(lpF), PK["lpQ"], 0, SR); pk = nm(pk)
# automation: peak amount rises with the phaser sweep; band reverb mix runs opposite (dry at strongest peaks)
pAmt = sm(0.25 + 0.75 * 0.5 * (rL + rR), 150); pkS = pan2(pk * pAmt, 0) / np.sqrt(2) * el_gate("peaks", 200)[:, None]
BV = R["bandVerb"]; bsrc = bw("band", [BV["lo"], BV["hi"]], np.stack([pk, pk], 1), 2)
bv = verb(C(bsrc), BV["rt"], 71, 6000.0, 1.8); bv = bw("band", [BV["lo"], BV["hi"]], bv, 2); bv = nm(bv) * (1 - pAmt)[:, None] * el_gate("peaks", 200)[:, None]
# ================= S3 reverb/rumble kick
K = R["kick"]; RU = R["rumble"]
def kick1(v):
    L = int(K["gate"] * SR); tt = np.arange(L) / SR; f = K["endHz"] + (K["startHz"] - K["endHz"]) * np.exp(-tt / (K["tauMs"] / 1000))
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / K["decay"]) * np.minimum(tt / 0.003, 1)
    fw = int(0.08 * SR); y[-fw:] *= np.cos(np.linspace(0, np.pi / 2, fw)) ** 2; return y * v
kick = np.zeros(N)
for b in range(NB):
    for q in range(4): put(kick, kick1(K["vel"][q]), tb(b) + q * BT)
kg = el_gate("kick", 20); kick *= kg; events += int(np.sum([1 for b in range(NB) for q in range(4) if kg[min(int((tb(b)+q*BT)*SR)+100, N-1)] > 0.5]))
for s in SEC:  # rise: kick returns through an opening high-pass (filters open)
    if s.get("rise"):
        i0, i1 = int(tb(s["b"][0]) * SR), int(tb(s["b"][1]) * SR); seg = kick[i0:i1]
        hpc = 400 * (40 / 400) ** np.linspace(0, 1, i1 - i0); kick[i0:i1] = dsp.svf(C(seg), C(hpc), 0.7, 2, SR)
nyg = dsp.env_follow_gain(C(bw("low", 150, kick, 2)), SR, RU["nyThreshDb"], RU["nyRatio"], RU["nyAtk"], RU["nyRel"])  # sidechain EQ: lows trigger
retA = dsp.eq(dsp.eq(C(kick * nyg * 3.0), "lowshelf", 80, 0.707, 4.0), "highshelf", 4000, 0.707, 3.0)
retB = np.tanh(kick * (1 + 20 * RU["drive"])) / np.tanh(1 + 20 * RU["drive"])
kv = verb(C(np.stack([kick, kick], 1)), RU["verbRt"], 83, float(RU["verbDamp"]), RU["verbSize"], 0.05, 0.8, 0.0).mean(1)
kv = bw("high", 35, kv, 2)
duck = dsp.env_follow_gain(C(kick), SR, -28.0, 10.0, 0.002, RU["duckRel"]); kv = kv * duck
lfo = 0.5 + 0.5 * np.sin(2 * np.pi * (R["bpm"] / 60 * RU["lfoNote"] / 4) * t)  # tempo-synced 1/8
slow = 1 + 0.15 * np.sin(2 * np.pi * RU["slowHz"] * t)
kv = dsp.svf(C(kv), C(RU["lpLo"] * (RU["lpHi"] / RU["lpLo"]) ** lfo * slow), 0.9, 0, SR)
rum = nm(kick) + RU["nyLevel"] * nm(retA) + RU["driveLevel"] * nm(retB)
rumV = nm(kv); kenv = sm(sm(np.abs(kick), 3), 120); kenv /= kenv.max() + 1e-9
lowbus = np.tanh(1.3 * nm(rum)) / np.tanh(1.3)  # low-end enhancer: light drive on the kick bus
# ================= bass, clap, hat, lead, sweep, throws
LV = R["levels"]; bass = np.zeros(N)
for b0, b1, ci in CH["segments"]:
    L = int((b1 - b0) * BL * SR); f = hz(CH["bass"][ci]); tt_ = np.arange(L) / SR
    y = (np.sin(2 * np.pi * f * tt_) + 0.3 * np.sin(4 * np.pi * f * tt_)) * np.minimum(tt_ / 0.03, 1) * np.minimum(((b1 - b0) * BL - tt_) / 0.05, 1); put(bass, y, tb(b0))
bass *= el_gate("bass", 40); bass *= 1 - (1 - 10 ** (-LV["bassDuckDb"] / 20)) * np.clip(kenv * 2.5, 0, 1)
def clap1():
    L = int(0.4 * SR); tt = np.arange(L) / SR
    y = bw("band", [900, 2600], rng.standard_normal(L), 2) * np.exp(-tt / 0.09) * np.minimum(tt / 0.004, 1); y = bw("low", 5000, y, 2); y[-480:] *= np.linspace(1, 0, 480); return y
def ohat1():
    L = int(0.35 * SR); tt = np.arange(L) / SR
    y = bw("band", [5000, 9000], rng.standard_normal(L), 2) * np.exp(-tt / 0.12) * np.minimum(tt / 0.008, 1); y[-480:] *= np.linspace(1, 0, 480); return y
clap = np.zeros(N); oh = np.zeros(N)
for b in range(NB):
    for q in (1, 3): put(clap, clap1(), tb(b) + q * BT)
    for q in (0.5, 1.5, 2.5, 3.5): put(oh, ohat1(), tb(b) + q * BT)
clap *= el_gate("clap", 20); oh *= el_gate("ohat", 20)
clapS = pan2(clap, 0); clapS = nm(clapS) * 0.7 + 0.35 * nm(verb(C(clapS), 2.0, 37, 5500.0, 1.5)); ohS = bw("low", 9000, pan2(oh, -0.25), 2)
LD = R["lead"]; fl = np.full(N, hz(LD["notes"][0])); gl_ = np.zeros(N)
for b in range(NB):
    for q in range(4):
        s0 = tb(b) + q * BT; i0 = int(s0 * SR); L = int(0.9 * BT * SR); tt = np.arange(L) / SR
        fl[i0:i0 + L] = hz(LD["notes"][q]); e = np.minimum(tt / 0.015, 1) * (0.3 + 0.7 * np.exp(-tt / LD["decay"])) * np.minimum((0.9 * BT - tt) / 0.05, 1)
        gl_[i0:i0 + L] = np.maximum(gl_[i0:i0 + L], e)
fl = sm(fl, 3); lead = dsp.svf(C(saw_osc(fl) * gl_), C(np.full(N, float(LD["lp"]))), 0.8, 0, SR) * el_gate("lead", 60)
leadS = pan2(lead, 0.15); leadS = nm(leadS) * 0.8 + 0.35 * nm(verb(C(leadS), 3.0, 29, 7000.0, 1.8))
sw = np.zeros((N, 2))
for s in SEC:
    if s.get("rise"):
        i0, i1 = int(tb(s["b"][0]) * SR), int(tb(s["b"][1]) * SR); L = i1 - i0; nz = rng.standard_normal((L, 2))
        fc = 700 * (5000 / 700) ** np.linspace(0, 1, L); y = np.stack([dsp.svf(C(nz[:, c]), C(fc), 1.2, 1, SR) for c in (0, 1)], 1)
        y *= (np.linspace(0, 1, L) ** 1.5)[:, None]; y[-int(0.05 * SR):] *= np.linspace(1, 0, int(0.05 * SR))[:, None]; sw[i0:i1] = y
# committed turnarounds: deconstruct the last bar (rhythm out above) + reverb throw of pad/lead
tg = np.zeros(N)
for s in SEC:
    if "turnaround" in s: tg += gate(*s["turnaround"], 30)
throw = verb(C((padP * 0.6 + leadS) * tg[:, None]), 4.5, 91, 6000.0, 2.2)
mix = (padP * LV["pad"] + pkS * LV["peaks"] + bv * LV["bverb"] + leadS * LV["lead"] + nm(throw) * LV["throw"]) * (1 - 0.15 * np.clip(kenv * 2.5, 0, 1))[:, None]
mix += pan2(nm(bass) * LV["bass"], 0) / np.sqrt(2) + pan2(lowbus * LV["kick"] + rumV * LV["rumble"], 0) / np.sqrt(2)
mix += clapS * LV["clap"] + nm(ohS) * LV["ohat"] + nm(sw) * LV["sweep"]
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
