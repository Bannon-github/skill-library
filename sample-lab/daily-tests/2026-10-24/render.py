#!/usr/bin/env python3
"""Daily 3-skill test 2026-10-24: Euclidean weaver (melody mode) -> per-voice note-on random FM/fold pluck -> mono reverb pockets.
usage: render.py recipe.json out.wav   (original synthesis, deterministic)"""
import sys, os, json, numpy as np, soundfile as sf, pyloudnorm as pyln
from scipy import signal as sg
LAB = os.environ.get("LAB", "/workspace/skill-library/sample-lab"); sys.path.insert(0, LAB + "/engine")
import dsp, metrics
SR = 48000
R = json.load(open(sys.argv[1])); OUT = sys.argv[2]
rng = np.random.default_rng(R["seed"])
step = 60 / R["bpm"] / 4; bar = step * R["stepsPerBar"]; W = R["weaver"]
nsteps = R["bars"] * R["stepsPerBar"]; T = R["bars"] * bar + R["tailSec"]; N = int(T * SR)
SCALES = {"dorian": [0,2,3,5,7,9,10], "phrygian": [0,1,3,5,7,8,10]}
def deg2midi(d, sc): s = SCALES[sc]; return W["root"] + 12 * (d // 7) + s[d % 7]
def euclid(steps, pulses, rot): return [((((i + rot) * pulses) % steps) < pulses) for i in range(steps)]
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
V = R["voice"]; A, B, RV = V["partA"], V["partB"], V["random"]
def bip(): return rng.uniform(-1, 1)   # per-voice bipolar note-on random draw (skill s1)
def note(m, vel, gate):
    morph = np.clip(0.5 + RV["morph"] * bip(), 0, 1)                       # s7: per-voice morph A<->B
    lerp = lambda k: A[k] * (1 - morph) + B[k] * morph
    idx = max(0.0, lerp("fmIndex") + RV["fmOffsetComp"] + RV["fmIndex"] * bip())  # s2: base raised to use full bipolar range
    fold = np.clip(lerp("fold") + RV["fold"] * bip(), 0.05, 1.0)            # s1: fold halfway +- random
    cut = lerp("cutoff") * 2 ** (RV["cutoffOct"] * bip() - 0.3)            # s4: base lowered so both draws act
    dec = lerp("decay") * 2 ** (RV["decayOct"] * bip()) * (0.6 + gate)       # s5: random envelope times
    L = int(min(dec * 6 + 0.05, 4.0) * SR); t = np.arange(L) / SR; f = hz(m)
    ratio = lerp("ratio")
    menv = np.exp(-t / (dec * 0.5))
    x = np.sin(2 * np.pi * f * t + idx * menv * np.sin(2 * np.pi * f * ratio * t))
    x = np.sin(np.pi / 2 * (1 + 3 * fold) * x) / 1.0                        # wavefolder
    b, a = sg.butter(2, min(cut, 16000) / (SR / 2)); x = sg.lfilter(b, a, x)
    env = (1 - np.exp(-t / 0.003)) * np.exp(-t / dec)
    rel = int(0.01 * SR); env[-rel:] *= np.linspace(1, 0, rel)
    return x * env * vel, RV["delaySend"] * (0.5 + 0.5 * bip())               # s6: per-note delay send
# ---- sequence (weaver s1-s6)
buses = {k: np.zeros(N) for k in ("front", "right", "left")}; dsend = np.zeros(N); events = 0
for li, Ly in enumerate(W["layers"]):
    for s in range(nsteps):
        b_ = s // R["stepsPerBar"]
        if not (Ly["enterBar"] <= b_ < Ly["exitBar"]): continue
        p = Ly["pulses"] + (W["drift"][li] if b_ >= W["driftBar"] else 0)    # s3 drift +-1
        pat = euclid(Ly["steps"], max(1, min(p, Ly["steps"] - 1)), Ly["rot"])
        if not pat[s % Ly["steps"]]: continue
        sc = W["scaleB"] if b_ >= W["rekeyBar"] else W["scaleA"]           # s6 keep rhythm, re-key
        fade = min(1, (b_ - Ly["enterBar"] + 1) / 2, (Ly["exitBar"] - b_) / 2)
        y, ds = note(deg2midi(Ly["deg"], sc), Ly["vel"] * fade, Ly["gate"])
        i = int(s * step * SR); e = min(N, i + len(y))
        buses[Ly["pocket"]][i:e] += y[:e - i]; dsend[i:e] += ds * y[:e - i]; events += 1
# ---- space: mono reverb pockets
def ir(rt, seed, n=1):
    g = np.random.default_rng(seed); L = int(rt * 1.2 * SR); t = np.arange(L) / SR
    h = g.standard_normal((L, n)) * np.exp(-6.9 * t / rt)[:, None]
    b, a = sg.butter(1, 10000 / (SR / 2)); h = sg.lfilter(b, a, h, axis=0); h[:int(0.012*SR)] = 0
    return h / np.sqrt(np.sum(h ** 2, 0))
P = R["pockets"]; rt = P["reverbRt60"]; hm = ir(rt, 7)[:, 0]
def pan(x, p): return np.stack([x * np.cos((p + 1) * np.pi / 4), x * np.sin((p + 1) * np.pi / 4)], 1) * np.sqrt(2)
lfo = 0.5 + 0.5 * np.sin(2 * np.pi * P["postReverbBandpass"]["lfoHz"] * np.arange(N) / SR)
def moving_bp(x):                                             # s6 post-reverb bandpass with LFO, block-wise
    bp = P["postReverbBandpass"]; y = np.zeros_like(x); blk = 2400; zi = None
    for i in range(0, len(x), blk):
        c = bp["lowHz"] * (bp["highHz"] / bp["lowHz"]) ** lfo[i]
        b, a = sg.butter(1, [c / 1.6 / (SR / 2), c * 1.6 / (SR / 2)], "band")
        if zi is None: zi = np.zeros(max(len(a), len(b)) - 1)
        y[i:i+blk], zi = sg.lfilter(b, a, x[i:i+blk], zi=zi)
    return bp["mix"] * y + (1 - bp["mix"]) * x
mix = np.zeros((N, 2)); pp_in = np.zeros(N)
for k, x in buses.items():
    c = P[k]; wet = sg.fftconvolve(x, hm)[:N]                 # s2 100% wet mono reverb (width -> 0 = narrowed)
    b, a = sg.butter(1, (11000 - 3000 * c["wet"]) / (SR / 2)); wet = sg.lfilter(b, a, wet)   # s5 shave highs with distance
    wet = moving_bp(wet) if k != "front" else wet
    mix += pan(x * (1 - c["wet"]) * 0.8, c.get("dryPan", c["pan"]))   # s5 wet/dry = distance
    mix += pan(wet * c["wet"] * 0.7, c["pan"])                        # s3 pan each pocket, lower level
    pp_in += wet * c["wet"] * 0.5
# s4 ping-pong after width stage, low feedback with LP in loop
pg = P["pingpong"]; d = int(pg["timeSteps"] * step * SR); src = pp_in * 0.3 + dsend
b, a = sg.butter(1, pg["fbLowpassHz"] / (SR / 2)); L_ = np.zeros(N); R_ = np.zeros(N); cur = src.copy(); side = 0
for r in range(8):
    cur = np.concatenate([np.zeros(d), cur[:-d]]); cur = sg.lfilter(b, a, cur) * (1 if r == 0 else pg["feedback"])
    (L_ if side == 0 else R_)[:] += cur; side ^= 1
mix += pg["mix"] * np.stack([L_, R_], 1)
# stereo atmos bed (s1: stays stereo, moving notch into 100% wet reverb)
t = np.arange(N) / SR; bed = np.zeros(N)
for m in (50, 57, 64, 69):
    ph = rng.random() * 6.28; bed += np.sin(2*np.pi*hz(m)*t + ph) + 0.3*np.sin(2*np.pi*hz(m+12)*1.002*t + ph)
nb = 0.02 * rng.standard_normal(N); b, a = sg.butter(2, [3000/(SR/2), 11000/(SR/2)], "band"); bed += sg.lfilter(b, a, nb) * 30
# move bed to Phrygian at re-key: crossfade in the b2 (Eb) color
rk = int(W["rekeyBar"] * bar * SR); eb = np.sin(2*np.pi*hz(51)*t) * np.clip((np.arange(N) - rk) / (2*bar*SR), 0, 1)
bed += 0.6 * eb
nlfo = 900 * 2 ** (2 * (0.5 + 0.5*np.sin(2*np.pi*P["bed"]["notchLfoHz"]*t)))
out = np.zeros(N); blk = 4800
for i in range(0, N, blk):
    b, a = sg.iirnotch(nlfo[i] / (SR/2), 2.0); out[i:i+blk] = sg.lfilter(b, a, bed[i:i+blk])
hs = ir(rt * 1.6, 11, 2); bedw = np.stack([sg.fftconvolve(out, hs[:, j])[:N] for j in range(2)], 1)
benv = np.clip(t / 8, 0, 1) * np.clip((R["bars"]*bar - t) / 6, 0, 1)
mix += bedw * benv[:, None] * 10 ** (P["bed"]["levelDb"] / 20) * 0.25
# ---- master: HP 30, mono lows (side HP 120), fades, loudness, true-peak limiter
Mm = R["master"]; b, a = sg.butter(2, 30/(SR/2), "high"); mix = sg.filtfilt(b, a, mix, axis=0)
M = 0.5 * (mix[:, 0] + mix[:, 1]); S = 0.5 * (mix[:, 0] - mix[:, 1])
b, a = sg.butter(4, Mm["sideHpHz"]/(SR/2), "high"); S = sg.filtfilt(b, a, S); mix = np.stack([M + S, M - S], 1)
fi = np.clip(t / Mm["fadeInSec"], 0, 1); fo = np.clip((T - 0.3 - t) / Mm["fadeOutSec"], 0, 1) ** 2
mix *= (fi * fo)[:, None]; mix -= mix.mean(0)
meter = pyln.Meter(SR); gr_max = 0.0
for it in range(4):
    mix *= 10 ** ((Mm["targetLufs"] - meter.integrated_loudness(mix)) / 20)
    tp = np.maximum(dsp.true_peak_env(mix[:, 0]), dsp.true_peak_env(mix[:, 1]))
    ceil = 10 ** (Mm["tpCeil"] / 20); g = np.minimum(1, ceil / np.maximum(tp, 1e-9))
    la = int(0.005 * SR); g0 = np.minimum(1, ceil / np.maximum(tp, 1e-9)); g = np.minimum.reduce([np.roll(g0, k) for k in range(-la, la + 1, 24)])
    g = sg.filtfilt(np.ones(la) / la, [1], g); g = np.minimum(g, 1)
    gr_max = max(gr_max, -20 * np.log10(g.min())); mix *= g[:, None]
    if abs(meter.integrated_loudness(mix) - Mm["targetLufs"]) < 0.3: break
mix[-int(0.3*SR):] = 0; mix[:2] = 0
sf.write(OUT, mix.astype(np.float32), SR, subtype="PCM_24")
res = metrics.compute(mix, {"limiter_gr_db": gr_max}, "pluck", False, R["bars"] * bar, start_body_s=0.0,
                      f_low=hz(W["root"]), bar_s=bar)
res["events"] = events; res["lengthSec"] = round(T, 2); res["lufs"] = round(meter.integrated_loudness(mix), 2)
json.dump(res, open(OUT + ".stats.json", "w"), indent=1)
print(json.dumps({"score": res["score"], "pass": res["pass"], "lufs": res["lufs"], "tp": res["extra"].get("true_peak_dbtp"),
                  "gates": res["gates"], "subs": res["subs"], "events": events, "gr": round(gr_max, 2)}))
