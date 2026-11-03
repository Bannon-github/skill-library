#!/usr/bin/env python3
"""Daily 3-skill test 2026-11-03: phaser+chorus pure-wave octave pad (source+movement) + ambient mono bass with one
slow master LFO and direct-out sine sub (bass) + ambient loop-to-track with arp rate as the energy dial (structure).
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
def sec(b): return "intro" if b < S["drumsIn"] else "slow" if b < S["peak"] else "peak" if b < S["outro"] else "outro"
def chord_at(b):  # skill C: slow section 1 chord / 2 bars, chorus-like peak 1 chord / bar
    i = (b // 2) % 4 if sec(b) != "peak" else b % 4
    return R["chords"][i]
def blocks():
    b = 0
    while b < S["end"]:
        L = 1 if sec(b) == "peak" else 2
        if sec(b) != "peak" and sec(b + 1) == "peak": L = 1
        yield b, min(L, S["end"] - b); b += min(L, S["end"] - b)
events = 0
# ===== SKILL A: phaser/chorus pure-wave octave pad
P = R["pad"]; pad = np.zeros((N, 2))
for b, nb in blocks():
    root, _ = chord_at(b); dur = nb * BL + P["release"]; L = int(dur * SR); tt = np.arange(L) / SR
    amp = np.clip(tt / P["attack"], 0, 1) * np.clip((dur - tt) / P["release"], 0, 1)            # step 3 slow attack, high sustain
    menv = np.clip(tt / P["envAttack"], 0, 1); menv = P["envSustain"] + (1 - P["envSustain"]) * menv  # step 4 mod env opens while held
    fc = np.clip(P["lpMaxHz"] * P["lpFrac"] * menv * P["lpSectionGain"][sec(b)], 200, 16000)      # step 9 filter in/out by section
    y = np.zeros((L, 2))
    for o in P["octaves"]:                                                                         # step 1 same note, 3 octaves
        f0 = hz(root + o)
        for k in range(P["triUnison"]):                                                            # step 2 osc1 triangle x6
            d = (k / (P["triUnison"] - 1) - 0.5) * P["triDetune"]
            v = dsp.osc_va(np.full(L, f0 * 2 ** (d / 1200)), 2, 0.5, 0.0, SR)                     # retrigger: phase 0
            y += pan2(v, (k / (P["triUnison"] - 1) - 0.5) * 1.6) / P["triUnison"]
        for k in range(P["sineUnison"]):                                                           # osc2 sine x8, phase offset 85 deg
            d = (k / (P["sineUnison"] - 1) - 0.5) * P["sineDetune"]
            v = np.sin(2 * np.pi * f0 * 2 ** (d / 1200) * tt + np.radians(P["sinePhaseDeg"]))
            y += pan2(v, -(k / (P["sineUnison"] - 1) - 0.5) * 1.6) * 0.8 / P["sineUnison"]
    y = st2(lambda x, c: dsp.svf(dsp.svf(x, fc, 0.707, 0, SR), fc, 0.707, 0, SR), y)            # 24 dB/oct LP
    put(pad, y * amp[:, None], tb(b)); events += 1
rate = 1 / (4 * BL * 2 / 3)                                                                       # step 5 slow synced LFO (4/1 triplet)
pad = np.stack([dsp.phaser(np.ascontiguousarray(pad[:, c]), rate, P["phaserDepth"], P["phaserFb"], P["phaserStages"], P["phaserMix"], np.radians(P["phaserLRdeg"]) * c, SR) for c in range(2)], 1)
cl, cr = dsp.chorus(np.ascontiguousarray(pad[:, 0]), np.ascontiguousarray(pad[:, 1]), SR, 0, P["chorusRate"], P["chorusDepthMs"], P["chorusMs"], P["chorusFb"], 1.0, P["chorusMix"], 0.5, 0.0)
pad = np.stack([cl, cr], 1)                                                                       # step 6 feedback chorus after phaser
f, Pxx = sg.welch(pad[:, 0] + pad[:, 1], SR, nperseg=8192); band = (f > 600) & (f < 6000)        # step 7 find & notch the whistle
sm = np.convolve(10 * np.log10(Pxx + 1e-20), np.ones(31) / 31, "same"); ex = (10 * np.log10(Pxx + 1e-20) - sm)
whistle = float(f[band][np.argmax(ex[band])]); pad = st2(lambda x, c: dsp.eq(x, "peak", whistle, 8.0, P["notchDepthDb"]), pad)
wet = verb(flt("low", P["verbLp"], flt("high", P["verbHp"], pad, 4)), P["verbRt"], 3, 6000.0, 2.0, 0.2, 0.8)   # step 8 big hall
wet = np.concatenate([np.zeros((int(0.01 * SR), 2)), wet[:-int(0.01 * SR)]]); wet = np.tanh(1.5 * nm(wet)) / np.tanh(1.5)
pad = nm(pad) + P["verbMix"] / (1 - P["verbMix"]) * wet
pad = st2(lambda x, c: dsp.eq(x, "highshelf", 3000, 0.7, P["bright"]), pad); pad = flt("high", 60, pad)
# ===== SKILL C pieces: arp (rate = energy dial), atmos (smooth random LP + comb + slow pan)
A = R["arp"]; arp = np.zeros(N)
for b in range(S["drumsIn"], S["end"] - 1):
    s = sec(b); r = A["rates"][s]; half = r[0] if (b - (S["drumsIn"] if s == "slow" else S["peak"] if s == "peak" else S["outro"])) < 4 else r[1]
    step = half * BT; _, notes = chord_at(b); seq = notes + [notes[1] + 12]; k = 0; st = tb(b)
    while st < tb(b + 1) - 1e-6:
        m = seq[k % len(seq)]; L = int(min(step, 1.2) * SR + 0.4 * SR); tt = np.arange(L) / SR
        e = np.exp(-tt / A["decay"]); fcs = A["cutoff"] + A["envHz"] * np.exp(-tt / 0.06)
        v = dsp.osc_va(np.full(L, hz(m)), 0, 0.5, 0.0, SR) * 0.6 + dsp.osc_va(np.full(L, hz(m) * 2 ** (7 / 1200)), 0, 0.5, 0.3, SR) * 0.4
        v = dsp.svf(v, np.clip(fcs, 100, 16000), 0.9, 0, SR) * e * np.clip(tt / 0.003, 0, 1)
        put(arp, fade(v, 20), st); st += step; k += 1; events += 1
arp = pan2(flt("high", 180, arp), 0.15); dl, dr = dsp.stereo_delay(np.ascontiguousarray(arp[:, 0]), np.ascontiguousarray(arp[:, 1]), SR, BT * 0.75, BT * 1.5, 0.35, 0.35, 0, 0, 1, 300.0, 6000.0, 0, 0, 0)
arp = arp + A["delayMix"] * np.stack([dl, dr], 1); arp = nm(arp) + A["verbMix"] * nm(verb(flt("high", 250, arp), 3.5, 9))
X = R["atmos"]; rnd = sg.sosfiltfilt(sg.butter(1, 0.15, fs=SR, output="sos"), rng.standard_normal(N)); rnd = rnd / (np.max(np.abs(rnd)) + 1e-9)
atm = dsp.svf(rng.standard_normal(N), np.clip(X["lpBase"] + X["lpRand"] * rnd, 200, 12000), 0.7, 0, SR)
dly = (X["combMs"] / 1000 * SR) * (1 + 0.3 * np.sin(2 * np.pi * 0.05 * t))
atm = dsp.comb_ff_fb(atm, dly, float(X["combFb"]), 0.6)
atm = pan2(flt("high", 300, atm) * np.clip(t / 6, 0, 1), 0) ; pn = 0.6 * np.sin(2 * np.pi * 0.02 * t)
atm = np.stack([atm[:, 0] * np.cos((pn + 1) * np.pi / 4), atm[:, 1] * np.sin((pn + 1) * np.pi / 4)], 1) * np.sqrt(2)
# ===== SKILL B: ambient mono bass, light unison, one slow retriggered master LFO, direct-out sine sub, HP on moving layer
B = R["bass"]; bass = np.zeros(N); subb = np.zeros(N)
for b, nb in blocks():
    if sec(b) == "intro" or b >= S["drumsOut"] + 1: continue
    root, notes = chord_at(b); dur = nb * BL; L = int(dur * SR); tt = np.arange(L) / SR
    env = np.clip(tt / 0.02, 0, 1) * np.clip((dur - tt) / 0.05, 0, 1)
    lfo = 0.5 - 0.5 * np.cos(2 * np.pi * tt / (B["lfoBars"] * BL))                               # step 2 retriggered 4-bar master LFO
    if sec(b) == "peak":                                                                          # skill C: mute drone, arp pluck bass on pad chords
        f0 = hz(root - 12 if root > 44 else root); y = np.zeros(L); step = BT / 2
        seq = [root, root + 12, root + 7, root + 12]
        for k in range(int(dur / step)):
            i = int(k * step * SR); Lk = min(int(step * SR), L - i); tk = np.arange(Lk) / SR
            m = seq[k % 4]; v = dsp.osc_va(np.full(Lk, hz(m)), 0, 0.5, 0.0, SR)
            v = dsp.svf(v, np.clip(250 + 1800 * np.exp(-tk / 0.05), 60, 9000), 0.8, 0, SR) * np.exp(-tk / 0.12)
            y[i:i + Lk] += fade(v, 5) ; events += 1
        put(bass, flt("high", B["hp"], y) * B["pluckLevel"], tb(b))
        put(subb, np.sin(2 * np.pi * hz(root - 12 if root > 44 else root) * tt) * env * 0.5, tb(b)); continue
    f0 = hz(root - 12 if root > 44 else root); spk = np.zeros(L)
    for q in range(nb * 4):                                                                       # skill C: cutoff 'spikes' automation
        if q % 3 == 2: i = int(q * BT * SR); Ls = min(int(0.4 * SR), L - i); spk[i:i + Ls] += B["spikes"] * np.exp(-np.arange(Ls) / SR / 0.12) * (0.7 + 0.3 * (q % 2))
    fmi = B["fmIdx"] + B["fmLfo"] * lfo; y = np.zeros(L)
    for k in range(B["unison"]):                                                                  # step 1 mono, 5 light unison voices
        d = (k / (B["unison"] - 1) - 0.5) * B["detune"]; fk = f0 * 2 * 2 ** (d / 1200)
        mod = np.sin(2 * np.pi * fk * 2 * tt)                                                     # step 3 FM macro: osc2 -> osc1
        y += np.sin(2 * np.pi * fk * tt + fmi * mod) * 0.5 + dsp.osc_va(np.full(L, fk), 0, 0.5, k / 7, SR) * 0.35
    y /= B["unison"]
    y = np.tanh((B["driveBase"] + B["driveLfo"] * lfo) * y)                                        # LFO -> drive
    y = dsp.svf(dsp.svf(y, np.clip(B["cutBase"] + B["cutLfo"] * lfo + 1500 * spk, 60, 8000), 0.8, 0, SR), np.clip(B["cutBase"] * 3 + B["cutLfo"] * lfo + 1500 * spk, 60, 9000), 0.707, 0, SR)
    y = flt("high", B["hp"], y, 4)                                                                # step 6 HP moving layer
    put(bass, y * env, tb(b)); put(subb, np.sin(2 * np.pi * f0 * tt) * env * B["subLevel"], tb(b)); events += 1   # step 5 sine direct out
bass = nm(bass) * 0.6 + nm(flt("low", 110, subb)) * 0.75                                          # step 7 mono (single channel)
# ===== support drums (not under test): kick/rim/hat; skill C double-time clip in the peak
drm = np.zeros((N, 2)); key = np.zeros(N); Dd = R["drums"]
def kick(): L = int(0.45 * SR); tt = np.arange(L) / SR; f = 48 + 90 * np.exp(-tt / 0.035); return fade(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.18), 10)
def hat(v): L = int(0.06 * SR); return fade(flt("band", [4500, 11000], rng.standard_normal(L)) * np.exp(-np.arange(L) / SR / 0.015) * v, 5)
def rim(): L = int(0.12 * SR); tt = np.arange(L) / SR; return fade((flt("band", [1200, 2600], rng.standard_normal(L)) * 0.6 + np.sin(2 * np.pi * 820 * tt)) * np.exp(-tt / 0.03), 5)
for b in range(S["drumsIn"], S["drumsOut"]):
    s = sec(b); dbl = s == "peak"; scale = 0.5 if dbl else 1.0; s0 = tb(b)
    for rep in range(2 if dbl else 1):
        o = s0 + rep * BL * scale
        for q in (0, 2.5) if not (s == "outro") else (0,):
            put(drm, pan2(kick(), 0), o + q * BT * scale); put(key, np.ones(int(0.05 * SR)), o + q * BT * scale); events += 1
        put(drm, pan2(rim(), 0.2) * Dd["rimLevel"], o + 3 * BT * scale)
        if b >= S["drumsIn"] + 2:
            for k in range(8): put(drm, pan2(hat((0.9 if k % 2 else 0.5)), -0.3) * Dd["hatLevel"], o + (k * 0.5 + (0.04 if k % 2 else 0)) * BT * scale); events += 1
drm = drm + 0.25 * nm(verb(flt("high", 300, drm), 1.8, 13))
# ===== mix + master (same chain as earlier daily tests)
kenv = sg.lfilter([1 - np.exp(-1/(0.2*SR))], [1, -np.exp(-1/(0.2*SR))], key); duck = 1 - P["sc"] * np.clip(kenv * 3, 0, 1)
mix = nm(pad) * P["level"] * duck[:, None] + nm(arp) * A["level"] + nm(atm) * X["level"] + pan2(bass * R["bass"]["level"], 0) * (1 - 0.6 * P["sc"] * np.clip(kenv * 3, 0, 1))[:, None] + nm(drm) * Dd["level"]
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
res["events"] = events; res["lengthSec"] = round(T, 2); res["lufs"] = round(meter.integrated_loudness(mix), 2); res["drumsInSec"] = round(tb(S["drumsIn"]), 2); res["whistleHz"] = round(whistle)
json.dump(res, open(OUT + ".stats.json", "w"), indent=1, default=float)
print(json.dumps({"score": res["score"], "pass": res["pass"], "lufs": res["lufs"], "tp": res["extra"].get("true_peak_dbtp"), "gates": res["gates"], "subs": res["subs"], "tilt": res["extra"].get("tilt_db_oct"), "events": events, "gr": round(gr_max, 2), "len": res["lengthSec"], "drumsIn": res["drumsInSec"]}, default=float))
