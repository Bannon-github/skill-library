#!/usr/bin/env python3
"""Daily 3-skill test 2026-11-15 "Dust Choir" (F# minor, 120 BPM / 60 BPM halftime harmony):
  A ambient-chord-arrangement-one-chord-tone-per-instrument-... (sub root / dark pad third a tenth up / choir fifth above third /
    frozen strings doubling third; each swells at its own pace; parallel direction; spread voicing; reverse textures in key)
  P build-stereo-phaser-from-allpass-chain-... (N two-pole all-pass biquads, Q 0.7071, centre x 16^(lfo*depth), (dry+wet)*0.5,
    R-channel LFO offset (100% = 180 deg), dry/wet) -> on pad/choir/strings bus and on ghosts/shaker/break
  K ambient-dub-techno-kit-... (sub-50 Hz crushed kick, -2 st rim-clap on last beat of every 2nd bar into huge parallel verb,
    hand-placed hard-panned ghosts -> HP/phaser/delay/verb, 2-hit shaker w/ phaser, dusty hat bed, top-only crushed break, bus sat 50% wet)
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
def verb(x, rt, seed, damp=9000.0, size=1.8, mod=0.2, diff=0.75, pre=0.02):
    l, r = dsp.fdn_reverb(C(x[:, 0]), C(x[:, 1]), SR, float(rt), size, damp, pre, mod, diff, 0.0, seed); return np.stack([l, r], 1)
def dly(x, tl, tr, fb, pp=1, hp=200, lp=6000):
    return np.stack(dsp.stereo_delay(C(x[:, 0]), C(x[:, 1]), SR, tl, tr, fb, fb, 0.0, 0.0, pp, hp, lp, 0.1, 0.0, 0.2), 1)
nm = lambda x: x / (np.max(np.abs(x)) + 1e-9)
def sm(x, ms): a = np.exp(-1 / (ms / 1000 * SR)); return lfilter([1 - a], [1, -a], x, axis=0)
def saw(f, L, ph=0.0): return dsp.osc_va(np.full(L, f), 0, 0.5, ph, SR)
def gate(b0, b1, xf_ms=300): return sm(((bar >= b0) & (bar < b1)).astype(float), xf_ms)
events = 0

# ================= P: phaser built from an all-pass biquad chain (RBJ all-pass, Q, exp sweep, L/R offset)
@njit(cache=True)
def ap_chain(x, fc, q, stages, sr):
    n = x.shape[0]; z1 = np.zeros(8); z2 = np.zeros(8); y = np.zeros(n)
    for i in range(n):
        w = 2.0 * np.pi * fc[i] / sr; al = np.sin(w) / (2.0 * q); cw = np.cos(w); a0 = 1.0 + al
        b0 = (1.0 - al) / a0; b1 = -2.0 * cw / a0; b2 = 1.0  # b2 = a0/a0
        a1 = b1; a2 = b0
        v = x[i]
        for s in range(stages):                      # transposed direct form II all-pass biquad
            o = b0 * v + z1[s]
            z1[s] = b1 * v - a1 * o + z2[s]
            z2[s] = b2 * v - a2 * o
            v = o
        y[i] = v
    return y
def phaser(x, P):
    out = np.zeros_like(x)
    for c in range(2):
        ph = (t * P["rateHz"] + (0.5 * P["offset"] if c == 1 else 0.0)) % 1.0            # phasor + R offset (100% = 180 deg)
        lfo = np.sin(2 * np.pi * ph) if P["wave"] == "sine" else 1 - 4 * np.abs(ph - 0.5)  # bipolar sine / centred triangle
        fc = np.clip(P["center"] * 16.0 ** (lfo * P["depth"]), 50, 18000)                  # exponential sweep
        wet = 0.5 * (x[:, c] + ap_chain(C(x[:, c]), C(fc), P["q"], int(P["stages"]), SR))  # (dry + all-pass) * 0.5 -> notches
        out[:, c] = x[:, c] * (1 - P["wet"]) + wet * P["wet"]
    return out

# ================= A: one chord tone per instrument
CH = R["chords"]; nch = NB // CH["barsPer"]; chord_of = lambda k: CH["voices"][k % len(CH["voices"])]
def swell_line(voice_idx, attack, release, stagger, synth):
    buf = np.zeros(N)
    for k in range(nch):
        b0 = k * CH["barsPer"]; m = chord_of(k)[voice_idx]; st = tb(b0) + stagger
        hold = CH["barsPer"] * BL - stagger + (stagger if k < nch - 1 else 0); L = int((hold + release) * SR); tt_ = np.arange(L) / SR
        env = np.sin(np.pi / 2 * np.clip(tt_ / attack, 0, 1)) ** 2 * np.where(tt_ < hold, 1.0, np.cos(np.pi / 2 * np.clip((tt_ - hold) / release, 0, 1)) ** 2)
        put(buf, synth(hz(m), L) * env, st)
    return buf
# 1 sub: root only, swell (mod-wheel style), sine + a touch of 2nd harmonic
sub = swell_line(0, R["sub"]["attack"], 1.5, 0.0, lambda f, L: np.sin(2 * np.pi * f * np.arange(L) / SR) + 0.15 * np.sin(4 * np.pi * f * np.arange(L) / SR))
sub = bw("low", 200, sub, 2)
# 2 dark pad: third a tenth up, 2 detuned saws LP
PD = R["pad"]
pad = swell_line(1, PD["attack"], PD["release"], 0.0, lambda f, L: (saw(f * 2 ** (-5 / 1200), L, 0.1) + saw(f * 2 ** (5 / 1200), L, 0.6)) / 2)
pad = dsp.ladder(C(pad * 0.5), C(np.full(N, float(PD["lp"]))), 0.15, 0.1, 0, 0, SR)
# 3 choir: fifth above the third, saw through vowel 'ah' formant bank
CO = R["choir"]
def choir_syn(f, L):
    x = sum(saw(f * 2 ** (d / 1200), L, p) for d, p in ((-7, 0.2), (0, 0.5), (7, 0.8))) / 3
    return sum(g * bw("band", [fo / 1.25, fo * 1.25], x, 2) for fo, g in CO["formants"])
choir = swell_line(2, CO["attack"], CO["release"], CO["staggerSec"], choir_syn)
# 4 frozen strings: third +8va, ensemble saws LP, slow attack
STR = R["strings"]
strings = swell_line(3, STR["attack"], STR["release"], STR["staggerSec"], lambda f, L: sum(saw(f * 2 ** (d / 1200), L, p) for d, p in ((-9, 0.0), (-3, 0.3), (4, 0.55), (10, 0.85))) / 4)
strings = bw("low", STR["lp"], bw("high", 250, strings, 2), 2)
# reverse textures in key: reversed decaying sine-bell notes swelling into each chord change (fixed pitches)
RV = R["reverse"]; rev = np.zeros(N)
for k in range(1, nch):
    m = RV["notes"][k % len(RV["notes"])]; L = int(2.5 * SR); tt_ = np.arange(L) / SR
    bell = (np.sin(2 * np.pi * hz(m) * tt_) + 0.3 * np.sin(2 * np.pi * hz(m) * 2 * tt_)) * np.exp(-tt_ / 0.6) * np.minimum(tt_ / 0.005, 1)
    put(rev, bell[::-1] * np.minimum(np.arange(L)[::-1] / (0.02 * SR), 1), tb(k * CH["barsPer"]) - 2.5); events += 1
harm = (pan2(nm(pad), -0.35) * PD["level"] + pan2(nm(choir), 0.35) * CO["level"] + np.stack([nm(strings), np.roll(nm(strings), int(0.013 * SR))], 1) * STR["level"]
        + pan2(nm(rev), 0.0) * RV["level"])
harm = phaser(harm, R["phaser"])                                                     # P on the chord-tone bus
hv = verb(harm, 6.5, 11, 6500.0, 2.2)
harm = harm * 0.65 + nm(hv) * np.max(np.abs(harm)) * 0.6
events += nch * 4

# ================= K: ambient dub-techno kit
def crush(x, bits, div=1):
    q = 2 ** (bits - 1); y = np.round(x * q) / q
    if div > 1: y = np.repeat(y[::div], div)[:len(x)]
    return y
KK = R["kick"]
def kick1():
    L = int(0.6 * SR); tt_ = np.arange(L) / SR; f = KK["peakHz"] + (KK["startHz"] - KK["peakHz"]) * np.exp(-tt_ / 0.03)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt_ / KK["decay"]) * np.minimum(tt_ / 0.004, 1)
    y = 0.6 * y + 0.4 * crush(y, KK["bits"], KK["srDiv"])                                 # heavy crush (blended for body)
    y = dsp.eq(C(y), "peak", 800, 0.5, KK["midCutDb"]); y = bw("low", 300, y, 4)            # cut mids, no click
    y[-2400:] *= np.linspace(1, 0, 2400); return y
kick = np.zeros(N); k1 = kick1()
kick_on = lambda b: S["kickIn"] <= b < S["drumsOut"] and not (S["stripStart"] <= b < S["stripEnd"])
for b in range(NB):
    if kick_on(b):
        for q in range(4): put(kick, k1, tb(b) + q * BT); events += 1
# clap: 909-ish 3 bursts + tail, pitched -2 st (filter/rate), short decay -> rim feel, crushed, huge parallel verb
CL = R["clap"]; ps = 2 ** (CL["semis"] / 12)
def clap1():
    L = int(0.35 * SR); tt_ = np.arange(L) / SR; n = rng.standard_normal(L); env = np.zeros(L)
    for o in (0.0, 0.009, 0.018): env += (tt_ >= o) * np.exp(-np.clip(tt_ - o, 0, None) / 0.004) * np.minimum(np.clip(tt_ - o, 0, None) / 0.0008, 1)
    env += (tt_ >= 0.027) * np.exp(-np.clip(tt_ - 0.027, 0, None) / CL["decay"]) * 0.7
    y = bw("band", [900 * ps, 2400 * ps], n, 2) * env; y = bw("low", 7000, crush(y / np.max(np.abs(y)), CL["bits"]), 2); y[-480:] *= np.linspace(1, 0, 480); return y
clap = np.zeros(N)
for b in range(NB):
    if kick_on(b) and b % 2 == 1: put(clap, clap1(), tb(b) + 3 * BT); events += 1
clap2 = pan2(clap, 0.0); cv = verb(clap2, CL["verbRt"], 31, 5000.0, 2.6)
clapM = nm(clap2) * (1 - CL["verbMix"]) + nm(cv) * CL["verbMix"]
# ghosts: hand-placed blips (pitched sine+noise), hard L/R, HP -> phaser -> delay -> huge verb
GH = R["ghosts"]; gL = np.zeros(N); gR = np.zeros(N)
def ghost1(f):
    L = int(0.25 * SR); tt_ = np.arange(L) / SR
    y = (np.sin(2 * np.pi * f * tt_) * 0.8 + 0.3 * bw("band", [f * 2, f * 6], rng.standard_normal(L), 2)) * np.exp(-tt_ / 0.05) * np.minimum(tt_ / 0.003, 1)
    y[-240:] *= np.linspace(1, 0, 240); return y
for b in range(S["ghostsIn"], S["drumsOut"]):
    for bb, beat, side, f in GH["hits"]:
        if b % 8 == bb: put(gL if side == "L" else gR, ghost1(f), tb(b) + beat * BT); events += 1
gh = bw("high", 200, np.stack([gL, gR], 1), 2); gh = phaser(gh, R["drumPhaser"])
gh = gh + dly(gh, 3 * BT / 2, 3 * BT / 2, 0.45, 0, 300, 5000) * 0.5
gh = nm(gh) * 0.6 + nm(verb(gh, 8.0, 41, 6000.0, 2.6)) * 0.6
# shaker: two hits per bar, HP, phaser, big verb
SH = R["shaker"]; shk = np.zeros(N)
def shaker1():
    L = int(0.12 * SR); tt_ = np.arange(L) / SR
    y = rng.standard_normal(L) * np.minimum(tt_ / 0.015, 1) * np.exp(-tt_ / 0.035); y[-240:] *= np.linspace(1, 0, 240); return y
for b in range(S["ghostsIn"], S["drumsOut"]):
    for beat in SH["beats"]: put(shk, shaker1(), tb(b) + beat * BT); events += 1
shk = bw("high", SH["hp"], bw("low", 11000, shk, 2), 2); shk2 = phaser(pan2(shk, 0.15), R["drumPhaser"])
shk2 = nm(shk2) * 0.6 + nm(verb(shk2, 8.0, 43, 7000.0, 2.6)) * 0.5
# dust: old drum-machine hat as soft enveloped noise, offbeat 8ths, constant quiet bed (not a click roll)
DU = R["dust"]; dst = np.zeros(N)
def hat1():
    L = int(0.08 * SR); tt_ = np.arange(L) / SR
    y = rng.standard_normal(L) * np.minimum(tt_ / 0.010, 1) * np.exp(-tt_ / 0.03); y[-240:] *= np.linspace(1, 0, 240); return y
for b in range(S["kickIn"], S["drumsOut"]):
    for q in range(4): put(dst, hat1(), tb(b) + (q + 0.5) * BT); events += 1
dbed = rng.standard_normal(N) * 0.08 * gate(S["kickIn"], S["drumsOut"], 1500)                # constant dust under the hats
dst = bw("high", DU["hp"], bw("low", 10000, dst + dbed, 2), 2); dst = pan2(dst, -0.1)
# break: synthetic funk break chopped into a regular 8th grid, crushed, phaser, verb, HP 2.5 kHz (top-only)
BR = R["break"]; brk = np.zeros(N)
slices = {"k": (60, 0.12), "s": (190, 0.10), "h": (0, 0.04)}
def slice1(kind):
    f, d = slices[kind]; L = int(0.18 * SR); tt_ = np.arange(L) / SR; n = rng.standard_normal(L)
    body = np.sin(2 * np.pi * f * tt_) if f else 0
    y = (0.5 * body + n * (0.8 if kind == "s" else 0.5)) * np.exp(-tt_ / d) * np.minimum(tt_ / 0.008, 1); y[-240:] *= np.linspace(1, 0, 240); return y
pat = ["k", "h", "s", "h", "h", "k", "s", "h"]
for b in range(S["breakIn"], S["drumsOut"]):
    if S["stripStart"] <= b < S["stripEnd"]: continue
    for i, kd in enumerate(pat): put(brk, slice1(kd), tb(b) + i * BT / 2); events += 1
brk = crush(brk / (np.max(np.abs(brk)) + 1e-9), BR["bits"]); brk = bw("high", BR["hp"], bw("low", BR["postLp"], brk, 4), 4)   # LP after crush: tame step edges
brk2 = phaser(pan2(brk, -0.2), R["drumPhaser"]); brk2 = nm(brk2) * 0.7 + nm(verb(brk2, 3.0, 45, 7000.0, 1.6)) * 0.35
# drum bus: kick + clap + ghosts + shaker + dust + break, saturator 50% wet
dbus = (pan2(nm(kick), 0) / np.sqrt(2) * KK["level"] + clapM * CL["level"] + gh * GH["level"] + shk2 * SH["level"]
        + nm(dst) * DU["level"] + brk2 * BR["level"])
B = R["bus"]; pk = np.max(np.abs(dbus)) + 1e-9
dbus = dbus * (1 - B["wet"]) + np.tanh(dbus / pk * B["satDrive"]) / np.tanh(B["satDrive"]) * pk * B["wet"]
# kick-keyed compressor on the sub (dub-kit step 9 idea: bass never overlaps kick)
kenv = sm(np.abs(kick), 5); kenv = sm(kenv, 80); kenv /= kenv.max() + 1e-9
duck = 1 - (1 - 10 ** (-R["sub"]["duckDb"] / 20)) * np.clip(kenv * 2.5, 0, 1)
sub = nm(sub) * duck


if os.environ.get("DBG"):
    def spk(x):
        x = x.mean(1) if x.ndim == 2 else x; he = np.abs(bw("high", 8000, x, 4)); return int(np.sum(he > 8 * (sm(he, 50) + 1e-9)))
    for nmx, x in (("harm", harm), ("kick", kick), ("clap", clapM), ("gh", gh), ("shk", shk2), ("dst", dst), ("brk", brk2), ("sub", sub)): print(nmx, spk(x))
    sys.exit()
# ================= mix + master
Mm = R["master"]
mix = harm / (np.max(np.abs(harm)) + 1e-9) + pan2(sub * R["sub"]["level"], 0) / np.sqrt(2) + dbus
mix = sg.sosfiltfilt(sg.butter(2, 22, "high", fs=SR, output="sos"), mix, axis=0)
Mn = 0.5 * (mix[:, 0] + mix[:, 1]); Sd = 0.5 * (mix[:, 0] - mix[:, 1])
Sd = sg.sosfiltfilt(sg.butter(4, Mm["sideHpHz"], "high", fs=SR, output="sos"), Sd) * Mm["width"]
mix = np.stack([Mn + Sd, Mn - Sd], 1)
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
res["events"] = events; res["lengthSec"] = round(T, 2); res["lufs"] = round(meter.integrated_loudness(mix), 2); res["drumsInSec"] = round(tb(S["kickIn"]), 2)
side = 0.5 * (mix[:, 0] - mix[:, 1]); mid = 0.5 * (mix[:, 0] + mix[:, 1]); db = lambda x: 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)
hf = bw("high", 8000, mid, 4); he = np.abs(hf); spikes = int(np.sum(he > 8 * (sm(he, 50) + 1e-9)))
ed = sm(he, 5)[::480]; fq, Pw = sg.welch(ed - ed.mean(), fs=100, nperseg=1024)
sec = lambda b0, b1: mix[int(tb(b0) * SR):int(tb(b1) * SR)]
kspec = np.abs(np.fft.rfft(k1, 1 << 16)); kf = np.fft.rfftfreq(1 << 16, 1 / SR)
res["checks"] = {"side_below_120Hz_db": round(db(bw("low", 120, side, 4)) - db(bw("low", 120, mid, 4)), 1), "hf_spikes_over_8x": spikes,
  "hf_env_12_40_vs_0_12_db": round(10 * np.log10(Pw[(fq >= 12) & (fq <= 40)].mean() / Pw[(fq > 0.2) & (fq < 12)].mean()), 1),
  "kick_peak_hz": round(float(kf[np.argmax(kspec)]), 1),
  "break_below_2k_db": round(db(bw("low", 2000, brk, 4)) - db(brk), 1),
  "lufs_intro_A_B_strip_C_outro": [round(meter.integrated_loudness(sec(a, b)), 1) for a, b in ((0, 4), (4, 12), (12, 24), (24, 28), (28, 37), (37, 40))]}
json.dump(res, open(OUT + ".stats.json", "w"), indent=1, default=float)
print(json.dumps({"score": res["score"], "pass": res["pass"], "lufs": res["lufs"], "tp": res["extra"].get("true_peak_dbtp"), "gates": res["gates"], "subs": res["subs"], "tilt": res["extra"].get("tilt_db_oct"), "gr": round(gr_max, 2), "len": res["lengthSec"], "drumsIn": res["drumsInSec"], "checks": res["checks"]}, default=float))
