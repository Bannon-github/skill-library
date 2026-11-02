#!/usr/bin/env python3
"""Daily 3-skill test 2026-11-02: struck-string model (source) + cinematic taiko ensemble from white noise (drums)
+ eight-bar phrase repetition A-B-A-C...D (structure). usage: render.py recipe.json out.wav"""
import sys, os, json, numpy as np, soundfile as sf, pyloudnorm as pyln
from scipy import signal as sg
LAB = os.environ.get("LAB", "/workspace/skill-library/sample-lab"); sys.path.insert(0, LAB + "/engine")
import dsp, metrics
SR = 48000
R = json.load(open(sys.argv[1])); OUT = sys.argv[2]; rng = np.random.default_rng(R["seed"])
NB = R["bars"]; BL = 240 / R["bpm"]; BT = BL / 4; tb = lambda x: x * BL; S = R["sections"]
T = NB * BL + R["tailSec"]; N = int(T * SR); t = np.arange(N) / SR
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
def flt(k, f, x, o=2): return sg.sosfilt(sg.butter(o, f, k, fs=SR, output="sos"), x, axis=0)
def pan2(x, p): return np.stack([x * np.cos((p + 1) * np.pi / 4), x * np.sin((p + 1) * np.pi / 4)], 1) * np.sqrt(2)
def put(buf, y, s, g=1.0):
    i = int(round(s * SR)); L = min(len(y), N - i)
    if L > 0 and i >= 0: buf[i:i + L] += y[:L] * g
def verb(x, rt, seed, damp=10000.0, size=1.6, mod=0.25, diff=0.75):
    l, r = dsp.fdn_reverb(np.ascontiguousarray(x[:, 0]), np.ascontiguousarray(x[:, 1]), SR, float(rt), size, damp, 0.03, mod, diff, 0.0, seed); return np.stack([l, r], 1)
def fade(y, ms=10, mi=0.0):
    n = int(ms * SR / 1000); y[-n:] *= np.linspace(1, 0, n)
    if mi: m = int(mi * SR / 1000); y[:m] *= np.linspace(0, 1, m)
    return y
nm = lambda x: x / (np.max(np.abs(x)) + 1e-9)
st2 = lambda f, x: np.stack([f(np.ascontiguousarray(x[:, c]), c) for c in range(2)], 1)
chord = lambda b: R["chords"][(int(b) // 2) % 4]
events = 0
# ===== support pad (not under test): soft chord bed, the only thing before the drums
K = R["pad"]; pad = np.zeros((N, 2)); sub = np.zeros(N)
for b in range(0, S["end"], 2):
    root, notes = chord(b); dur = 2 * BL + 0.6; L = int(dur * SR); tt = np.arange(L) / SR
    env = np.clip(tt / 1.2, 0, 1) * np.clip((dur - tt) / 0.9, 0, 1)
    for j, m in enumerate(notes):
        for d in (-6, 6):
            y = dsp.osc_va(np.full(L, hz(m) * 2 ** (d / 1200)), 0, 0.5, rng.random(), SR) * env * 0.5
            put(pad, pan2(flt("low", 2600, y), (j - 1) * 0.5 + d / 30), tb(b))
    put(sub, np.sin(2 * np.pi * hz(root + 12) * tt) * env, tb(b))
pad = pad + K["verbMix"] * verb(flt("high", 200, pad), K["verbRt"], 3)
pad = st2(lambda x, c: dsp.eq(x, "highshelf", 3000, 0.7, K["bright"]), pad)
# ===== SKILL A: struck-string model (modal partials, pre-strike brightness, freq-dependent decay slope, bounce polyrhythm layers)
Q = R["strings"]; strs = np.zeros((N, 2))
def strike(m, v, dur):
    L = int(dur * SR); tt = np.arange(L) / SR; f0 = hz(m); y = np.zeros(L); prof = Q["profile"]
    bright = Q["brightness"] * (0.6 + 0.4 * v)                              # step 1: brightness fixed at strike time
    for s in (-1, 0, 1):                                                    # step 2: three detuned strings per note
        fs = f0 * 2 ** (s * Q["unisonCents"] / 1200)
        for k in range(1, Q["partials"] + 1):
            fk = k * fs * np.sqrt(1 + Q["inharm"] * k * k)                   # step 4: harmonicity
            if fk > 16000: break
            a = abs(np.sin(np.pi * k * Q["strikePoint"])) / k ** (2.2 - 1.6 * bright) * prof[(k - 1) % len(prof)]   # step 4 strike point, step 2 profile
            tau = Q["decaySec"] / (1 + Q["decaySlope"] * max(0, fk - Q["decayCutoffHz"]) / Q["decayCutoffHz"])        # step 3 decay slope
            y += a * np.sin(2 * np.pi * fk * tt + rng.random() * 6) * np.exp(-tt / tau)
    y *= np.clip(tt / (Q["attackMs"] / 1000 + Q["smearMs"] / 1000), 0, 1)  # step 3 attack + step 4 smear
    return fade(y * v / 3, 30)
for b in range(0, S["end"], 2):                                             # steps 5-6: held chord re-strikes itself per layer
    root, notes = chord(b); held = 2 * BL
    for li, Ly in enumerate(Q["layers"]):
        if b < S[Ly["from"]] or b >= S["end"] - (1 if li == 0 else 0): continue
        n = int(held / (Ly["everyBeats"] * BT) + 0.999); v = 1.0
        for k in range(n):
            st = tb(b) + k * Ly["everyBeats"] * BT
            if st >= tb(b) + held: break
            m = notes[Ly["voice"]] + Ly["oct"]
            if li == 0 and (b // 2) % 2 == 1 and k % 4 == 3: m = notes[(Ly["voice"] + 1) % 3] + Ly["oct"]   # phrase B-style one-note change
            fadeout = 1.0 if b < S["outro"] else max(0.3, 1 - (b - S["outro"]) / 6)
            put(strs, pan2(strike(m, v * fadeout, min(Q["decaySec"] * 1.6, 4.0)), (-0.45, 0.0, 0.4)[li]), st); v *= Q["bounceDecay"]; events += 1
# step 7: vibrato-free tremolo (steady pitch per Matt), chorus, delay, gentle comp
trem = 1 - Q["tremDepth"] * (0.5 + 0.5 * np.sin(2 * np.pi * Q["tremHz"] * t)); strs *= trem[:, None]
cl, cr = dsp.chorus(np.ascontiguousarray(strs[:, 0]), np.ascontiguousarray(strs[:, 1]), SR, 0, 0.5, 2.5, 10.0, 0.0, 1.0, Q["chorusMix"], 0.5, 0.98); strs = np.stack([cl, cr], 1)
dl, dr = dsp.stereo_delay(np.ascontiguousarray(strs[:, 0]), np.ascontiguousarray(strs[:, 1]), SR, BT * 1.5, BT * 0.75, 0.35, 0.35, 0.0, 0.0, 1, 300.0, 7000.0, 0.0, 0.0, 0.0)
strs = strs + Q["delayMix"] * np.stack([dl, dr], 1)
strs = np.tanh(1.3 * nm(strs)) / np.tanh(1.3)
strs = nm(strs) + Q["verbMix"] * nm(verb(flt("high", 250, strs), Q["verbRt"], 7, 9000.0))
strs = flt("high", 90, strs)
# ===== SKILL B: taiko ensemble from white noise (vel->decay, LP 1k + env2, HP60 + low bell, tanh, limiter THEN hall, layers)
D = R["drums"]
def taiko(v, size=1.0):
    dec = (0.05 + 0.45 * v ** 2) * size; L = int((dec * 5 + 0.1) * SR); tt = np.arange(L) / SR   # step 2 velocity -> amp decay
    y = rng.standard_normal(L) * np.exp(-tt / dec) * np.clip(tt / 0.0008, 0, 1) * (0.25 + 0.75 * v)  # step 1 wide vel range
    fc = D["lpHz"] * (0.7 + 0.3 * size) + D["envPeakHz"] * v * np.exp(-tt / D["envDecay"])            # step 3 env2 on cutoff, vel-scaled
    y = dsp.svf(np.tanh(1.2 * y), np.clip(fc, 60, 16000), 1.0, 0, SR)
    f = 85 / size * 2 ** (0.6 * np.exp(-tt / 0.04)); ph = 2 * np.pi * np.cumsum(f) / SR                # step 7 tone: 3 detuned sines, pitch drop
    tone = sum(np.sin(ph * 2 ** (c / 1200)) for c in (-9, 0, 11)) / 3 * np.exp(-tt / (dec * 0.9))
    subw = np.sin(2 * np.pi * np.cumsum(np.full(L, 42.0 if size > 0.8 else 70.0)) / SR) * np.exp(-tt / (dec * 1.2)) * size   # 20-50 Hz sub
    y = y + D["sineLayer"] * tone * v + D["subLayer"] * subw * v
    y = flt("high", D["hpHz"], y)                                                                       # step 4 resonant HP + bell etc.
    y = dsp.eq(y, "peak", D["hpHz"] * 1.05, 2.5, 3.0); y = dsp.eq(y, "peak", D["lowBellHz"], 1.0, D["lowBellDb"])
    y = dsp.eq(y, "peak", 320, 1.2, D["mudCutDb"]); y = dsp.eq(y, "peak", 3000, 1.0, D["presenceDb"]); y = dsp.eq(y, "highshelf", 6000, 0.7, D["shelfDb"])
    y = np.tanh(D["drive"] * y / (np.max(np.abs(y)) + 1e-9)) / np.tanh(D["drive"])                      # step 5 tanh
    return fade(flt("high", 30, y) * v, 25)
def rattle(v):                                                                                          # step 7 round-robin rattle, random pitch
    L = int(0.09 * SR); f0 = 2600 * 2 ** rng.uniform(-0.3, 0.3)
    return fade(flt("band", [f0, min(f0 * 2.2, 20000)], rng.standard_normal(L)) * np.exp(-np.arange(L) / SR / 0.018) * v, 5, 0.5)
drm = np.zeros((N, 2)); key = np.zeros(N)
def hit(buf, y, st, p): put(buf, pan2(y, p), st + rng.uniform(-3, 3) / 1000)
# ===== SKILL C: 8-bar phrase A B A C A A A D, spine beat, ghosts, fill or empty, polymeter
for b in range(S["drumsIn"], S["drumsOut"]):
    s0 = tb(b); pos = (b - S["drumsIn"]) % 8; label = "ABACAAAD"[pos]; secB = b >= S["B"]; outro = b >= S["outro"]
    nxt = b + 1; fill = label == "D" and nxt == S["B"]; empty = label == "D" and nxt == S["outro"]
    for q in range(4):                                                    # step 1 spine: low taiko 1-4, high taiko on 2 & 4, rattle on 'and'
        if empty or (outro and q > 0): continue
        if label == "C" and q == 3: continue                               # C: drop last beat low hit, bigger change
        hit(drm, taiko((1.0, 0.6, 0.85, 0.6)[q], 1.0), s0 + q * BT, 0); put(key, np.ones(int(0.05 * SR)), s0 + q * BT); events += 1
    for q in (1, 3):
        if outro or (empty and q == 3): continue
        hit(drm, taiko(0.75, 0.55), s0 + q * BT, 0.25); events += 1
    if not outro:
        for q in range(4):
            if empty and q >= 2: continue
            hit(drm, rattle(0.7), s0 + (q + 0.5) * BT, -0.3); events += 1
    if label == "B": hit(drm, taiko(0.5, 0.55), s0 + 3.5 * BT, 0.3); events += 1      # B: one small added hit
    if label == "C":
        for p16 in (13, 14, 15): hit(drm, taiko(0.45 + 0.15 * (p16 - 13), 0.55), s0 + p16 / 16 * BL, 0.3); events += 1
    if secB and not outro and not empty:                                  # step 2 ghosts on e / a, soft = short (vel->decay)
        for p16 in (1, 7, 11, 15): hit(drm, taiko(0.22, 0.7), s0 + p16 / 16 * BL, -0.2 if p16 % 4 == 1 else 0.2); events += 1
        for k in range(16):                                               # step 8 polymeter: 3-step accent on 16ths
            gi = (b - S["B"]) * 16 + k
            if gi % 3 == 0: hit(drm, rattle(0.9 if gi % 6 == 0 else 0.5), s0 + k / 16 * BL, 0.45); events += 1
    if fill:                                                              # step 6 fill: syncopation, extra kicks, toms high -> low
        for p16, sz in ((10, 0.45), (11, 0.55), (12, 0.65), (13, 0.75), (14, 0.9), (15, 1.0)): hit(drm, taiko(0.8, sz), s0 + p16 / 16 * BL, 0.5 - sz * 0.5); events += 1
        hit(drm, taiko(0.7, 1.0), s0 + 2.5 * BT, 0); events += 1
# step 6 limiter THEN big hall; shorten decay, tame lows, damp highs, lift 5 kHz
drm = nm(drm); drm = np.tanh(2.0 * drm) / np.tanh(2.0)
wet = verb(flt("high", D["verbHp"], drm), D["verbRt"], 13, D["verbDamp"], 2.2, 0.15, 0.8)
wet = st2(lambda x, c: dsp.eq(x, "peak", 5000, 1.0, D["wetLift5kDb"]), wet)
drm = drm + D["verbMix"] * nm(wet)
# ===== mix + master (same chain as earlier daily tests)
kenv = sg.lfilter([1 - np.exp(-1/(0.2*SR))], [1, -np.exp(-1/(0.2*SR))], key); duck = 1 - D["sc"] * np.clip(kenv * 3, 0, 1)
mix = nm(pad) * K["level"] * duck[:, None] + pan2(nm(sub) * K["subLevel"], 0) * duck[:, None]
mix += strs * Q["level"] * (1 - 0.5 * D["sc"] * np.clip(kenv * 3, 0, 1))[:, None] + drm * D["level"]
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
res = metrics.compute(mix, {"limiter_gr_db": gr_max}, R.get("category", "pad"), False, NB * BL, start_body_s=0.0, f_low=hz(33), bar_s=BL)
res["events"] = events; res["lengthSec"] = round(T, 2); res["lufs"] = round(meter.integrated_loudness(mix), 2); res["drumsInSec"] = round(tb(S["drumsIn"]), 2)
json.dump(res, open(OUT + ".stats.json", "w"), indent=1, default=float)
print(json.dumps({"score": res["score"], "pass": res["pass"], "lufs": res["lufs"], "tp": res["extra"].get("true_peak_dbtp"), "gates": res["gates"], "subs": res["subs"], "tilt": res["extra"].get("tilt_db_oct"), "events": events, "gr": round(gr_max, 2), "len": res["lengthSec"], "drumsIn": res["drumsInSec"]}, default=float))
