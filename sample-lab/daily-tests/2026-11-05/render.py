#!/usr/bin/env python3
"""Daily 3-skill test 2026-11-05:
  lush-dual-saw-filter-env-nonretrigger-lfo-pad (wavetable)
  + wide-bass-remove-fundamental-add-mono-sine (bass)
  + nested-lfo-layered-riser-downer-kit (risers)
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
chord = lambda b: R["chords"][(b // 2) % 4]
events = 0

# ===== SKILL A: lush-dual-saw-filter-env-nonretrigger-lfo-pad
P = R["pad"]; pad = np.zeros((N, 2))
# free-running non-retrigger LFO (triangle, multi-bar)
lfo = sg.sawtooth(2 * np.pi * t / (P["lfoBars"] * BL) + 0.3, 0.5)  # triangle-ish via phase
# precompute slow filter envelope open (shared shape, applied per note)
for b in range(0, S["end"], 2):
    _, notes = chord(b); dur = 2 * BL + P["release"]; L = int(dur * SR); tt = np.arange(L) / SR; i0 = int(tb(b) * SR)
    # amp ADSR-ish: attack 2s, decay 6s to sustain, release 2s
    att = np.clip(tt / P["attack"], 0, 1)
    # after attack, decay toward sustain
    post = np.clip((tt - P["attack"]) / max(P["decay"], 1e-6), 0, 1)
    sustain_lvl = P["sustain"]
    amp_body = att * (1 - post) + (att * sustain_lvl) * post  # rough
    amp_body = np.where(tt < P["attack"], att, sustain_lvl + (1 - sustain_lvl) * np.exp(-(tt - P["attack"]) / (P["decay"] * 0.45)))
    rel = np.clip((dur - tt) / P["release"], 0, 1)
    amp = amp_body * rel
    # filter env2: ~2s attack open from cutStart
    fenv = np.clip(tt / P["env2Attack"], 0, 1)
    # non-retrigger LFO slice
    lf = lfo[i0:i0+L] if i0+L <= N else np.pad(lfo[i0:], (0, max(0, i0+L-N)), mode="edge")[:L]
    cut = P["cutStart"] + P["env2Amt"] * fenv * (1 + P["lfoDepth"] * lf)
    cut = np.clip(cut, 80, 9000)
    y = np.zeros((L, 2)); U = P["unison"]
    for m in notes:
        # osc1 unison saws
        for k in range(U):
            x = (k / max(U - 1, 1) - 0.5)
            f = np.full(L, hz(m) * 2 ** (x * P["detuneCents"] / 1200))
            v = dsp.osc_va(f, 0, 0.5, rng.random(), SR)
            y += pan2(v, x * 2 * P["spread"]) / (U * len(notes))
        # osc2 saw -12 st (thicken)
        f2 = np.full(L, hz(m - 12))
        v2 = dsp.osc_va(f2, 0, 0.5, 0.17, SR)
        y += pan2(v2, 0.0) * P["oct2Level"] / len(notes)
    # time-varying LP via blocky SVF
    out = np.zeros_like(y)
    bs = 512
    for i in range(0, L, bs):
        sl = slice(i, min(L, i + bs)); c0 = float(cut[i])
        out[sl, 0] = dsp.svf(np.ascontiguousarray(y[sl, 0]), c0, 0.6, 0, SR)
        out[sl, 1] = dsp.svf(np.ascontiguousarray(y[sl, 1]), c0, 0.6, 0, SR)
    put(pad, out * amp[:, None], tb(b)); events += 1
wet = verb(flt("high", P["verbHp"], pad, 4), P["verbRt"], 7, 6500.0, 2.4)
pad = (1 - P["verbMix"]) * nm(pad) + P["verbMix"] * nm(wet)
pad = flt("high", P["lowCut"], pad, 2)
pad = st2(lambda x, c: dsp.eq(x, "highshelf", 3500, 0.7, P["bright"]), pad)

# ===== light ambient drums (supporting, not a claimed skill) early ~10s
D = R["drums"]; drm = np.zeros((N, 2)); kicks = []
def kick():
    L = int(0.45 * SR); tt = np.arange(L) / SR; f = 48 + 95 * np.exp(-tt / 0.028)
    return fade(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.22), 12)
def hat(v, d=0.025):
    L = int(0.12 * SR); return fade(flt("band", [5500, 13000], rng.standard_normal(L)) * np.exp(-np.arange(L) / SR / d) * v, 5)
def rim():
    L = int(0.09 * SR); tt = np.arange(L) / SR
    return fade((flt("band", [1600, 3200], rng.standard_normal(L)) * 0.45 + np.sin(2 * np.pi * 880 * tt)) * np.exp(-tt / 0.022), 4)
for b in range(S["drumsIn"], S["drumsOut"]):
    s = sec(b); o = tb(b); rb = b - S["drumsIn"]
    # sparse ambient: kick on 1, sometimes and-of-3
    put(drm, pan2(kick(), 0) * D["kick"], o); kicks.append(o); events += 1
    if s in ("build", "peak") and rb % 2 == 1:
        put(drm, pan2(kick(), 0) * D["kick"] * 0.7, o + 2.5 * BT); kicks.append(o + 2.5 * BT)
    if s != "intro" and rb >= 2:
        put(drm, pan2(rim(), 0.2) * D["rim"], o + 2 * BT)
        for q in (2, 6, 10, 14):
            put(drm, pan2(hat(0.55 + 0.35 * (q % 4 == 2)), -0.25) * D["hat"], o + q * (BT / 4)); events += 1
drm = drm + 0.15 * nm(verb(flt("high", 500, drm), 1.2, 13))

# ===== SKILL B: wide-bass-remove-fundamental-add-mono-sine
B = R["bass"]; sub = np.zeros(N); mid = np.zeros(N)
kmono = np.zeros(N); [put(kmono, kick() * D["kick"], k) for k in kicks]
# fixed phase for mono sine fundamental (phase-randomize = 0)
PH = 0.0
for b in range(S["drumsIn"], S["drumsOut"] + 1):
    root, _ = chord(b); s = sec(b)
    starts = [0.0, 2.0] if s != "outro" else [0.0]
    for j, st in enumerate(starts):
        en = starts[j + 1] if j + 1 < len(starts) else 4.0
        dur = (en - st) * BT; L = int(max(dur, 0.05) * SR); tt = np.arange(L) / SR
        env = np.clip(tt / 0.01, 0, 1) * np.clip((dur - tt) / 0.04, 0, 1)
        f0 = hz(root)
        # mono sine fundamental, phase locked
        put(sub, np.sin(2 * np.pi * f0 * tt + PH) * env, tb(b) + st * BT)
        # mid: unison saws with fundamental removed (subtract matching sine + gentle HP)
        U = B["unison"]; acc = np.zeros(L)
        for k in range(U):
            x = (k / max(U - 1, 1) - 0.5)
            # detune ~0.25 on synth scale → ~8 cents spread
            ff = np.full(L, f0 * 2 ** (x * (B["detune"] * 32) / 1200))
            saw = dsp.osc_va(ff, 0, 0.5, 0.0, SR)
            # remove fundamental: subtract sine at same f/phase
            fund = np.sin(2 * np.pi * np.cumsum(ff) / SR)
            # scale fund to cancel first harmonic approx
            saw = saw - 0.55 * fund
            acc += saw / U
        acc = flt("high", f0 * 1.6, acc, 2)  # ensure fundamental gone
        acc = dsp.svf(acc, B["midCut"], 0.7, 0, SR) * env
        # hard-pan unison voices already summed — keep mid stereo via light width later; mono-safe fundamental separate
        put(mid, acc, tb(b) + st * BT); events += 1
sub = flt("low", B["split"], sub, 4); mid = flt("high", B["split"], mid, 4)
kenv = np.zeros(N); dn = int(B["duckMs"] / 1000 * SR); shape = 1 - np.clip(np.arange(dn) / dn, 0, 1) ** 2
for k in kicks: put(kenv, shape, k)
kenv = np.clip(kenv, 0, 1); sub *= 1 - B["subDuck"] * kenv; mid *= 1 - B["midDuck"] * kenv
# mid stereo via mild opposite pan of a Haas-ish copy (overtones only); sub stays mono
mid_st = pan2(nm(mid), 0.0)
# slight side from detuned content already; keep modest
bus = kmono * B["kickInBus"] + nm(sub) * B["subLevel"]
bass_mid = mid_st * B["midLevel"]

# ===== SKILL C: nested-lfo-layered-riser-downer-kit (into peak)
RS = R["riser"]; riser = np.zeros((N, 2))
# place kit spanning 2 bars before peak
t0 = tb(S["peak"] - RS["bars"]); dur = RS["bars"] * BL; Lr = int(dur * SR); tt = np.arange(Lr) / SR
# LFO1 envelope mode ~2 bars (0→1 ramp)
lfo1 = np.clip(tt / dur, 0, 1)
# nested: LFO1 drives LFO2 rate (seconds → accelerating)
# LFO2 base rate starts slow and accelerates
phase2 = np.cumsum((0.5 + 14 * lfo1 ** 2) / SR) * 2 * np.pi
lfo2 = 0.5 + 0.5 * np.sin(phase2)

# Downer: sine falling pitch
f_down = 220 * (2 ** (-lfo1 * 2.2))  # fall ~2+ oct
down = np.sin(2 * np.pi * np.cumsum(f_down) / SR)
down *= (0.15 + 0.85 * lfo1) * np.clip(tt / 0.08, 0, 1)  # slight attack
# distortion drive accelerates via nested LFO2
drive = 1 + 3.5 * lfo1 * lfo2
down = np.tanh(drive * down) / np.maximum(drive, 1)
down = flt("low", 200 + 2400 * lfo1, down, 2)
put(riser, pan2(down, -0.15) * RS["downerLevel"], t0)

# High stutter riser: high sine, LFO2→level stutter accelerating
f_hi = 880 * (2 ** (lfo1 * 1.5))
hi = np.sin(2 * np.pi * np.cumsum(f_hi) / SR)
stutter = (lfo2 > 0.35).astype(float)
# soft edges
stutter = sg.filtfilt(np.ones(64)/64, [1], stutter)
hi *= stutter * lfo1 * np.clip(tt / 0.05, 0, 1)
hi = flt("high", 800 + 2000 * (1 - lfo1), hi, 2)
put(riser, pan2(hi, 0.35) * RS["stutterLevel"], t0)

# Main riser: multi-osc levels/drive/filter/reverb under LFO1
main = np.zeros(Lr)
for oct_off, w in ((24, 0.35), (0, 0.5), (-12, 0.4)):
    f = 110 * (2 ** (oct_off / 12)) * (2 ** (lfo1 * 1.8))
    main += w * dsp.osc_va(f, 0, 0.5, 0.0, SR)
main *= lfo1
main = np.tanh((1 + 2.5 * lfo1) * main)
main = dsp.svf(main, np.clip(400 + 5000 * lfo1, 100, 10000), 0.5, 0, SR)
# noise layer
noise = flt("band", [400, 8000], rng.standard_normal(Lr)) * lfo1 * RS["noiseLevel"]
main_st = pan2(main, 0.0) + pan2(noise, 0.2)
# reverb wet starts high then decreases while size grows — approximate with two verbs blended
dry_amt = 0.25 + 0.55 * lfo1  # wet decreases as rise completes
wet_r = verb(np.stack([main, main], 1) * 0.4, 2.0 + 4.0 * lfo1.mean(), 21, 7000.0, 1.5 + 1.5)
# simpler: fixed verb on main then crossfade
main_v = verb(main_st, 5.0, 21, 7000.0, 2.2)
main_mix = (dry_amt)[:, None] * main_st + (1 - dry_amt)[:, None] * nm(main_v)[:Lr]
# HP automate: early favour downer/stutter — main opens later
hp = 800 * (1 - lfo1) + 80
for i in range(0, Lr, 512):
    sl = slice(i, min(Lr, i+512)); c0 = float(max(hp[i], 40))
    main_mix[sl] = flt("high", c0, main_mix[sl], 2)
put(riser, main_mix * RS["mainLevel"], t0); events += 3

# Atmosphere bed: heavily detuned, lots of reverb, mild pitch rise
atmos = np.zeros((Lr, 2))
for d in (-18, -7, 5, 14):
    f = 165 * (2 ** (d / 1200)) * (2 ** (lfo1 * 0.35))
    v = dsp.osc_va(f, 1, 0.35, rng.random(), SR)  # square-ish
    atmos += pan2(v, np.sign(d) * 0.4) / 4
atmos *= (0.3 + 0.7 * lfo1)[:, None]
atmos = verb(atmos, 7.0, 29, 5000.0, 2.8)
put(riser, nm(atmos) * RS["atmosLevel"], t0)

# second smaller whoosh into outro
t1 = tb(S["outro"] - 1); L2 = int(1.0 * BL * SR); tt2 = np.arange(L2) / SR; e2 = tt2 / (1.0 * BL)
who = flt("band", [600, 6000], rng.standard_normal(L2)) * e2
who = fade(who, 30, 5)
put(riser, pan2(who, 0.1) * 0.1, t1)

# ===== width-by-juxtaposition idea on pad: narrow intro, then sides reverb bed
Mm = R["master"]
# narrow pad early
narrow_n = int(tb(Mm["narrowIntroBars"]) * SR)
pad_w = pad.copy()
# mono-safe sides bed: MS with mid cut on send + reverb on sides
Mp = 0.5 * (pad_w[:, 0] + pad_w[:, 1]); Sp = 0.5 * (pad_w[:, 0] - pad_w[:, 1])
sides_path = np.stack([Sp, -Sp], 1)  # almost mid-killed
sides_path = verb(sides_path, 3.5, 31, 8000.0, 1.6) * 0.35
# widen after intro
wide = np.ones(N); wide[:narrow_n] = 0.25
wide = sg.filtfilt(np.ones(int(0.2*SR))/int(0.2*SR), [1], wide)
pad_w = np.stack([Mp, Mp], 1) + Mm["wideSide"] * wide[:, None] * (np.stack([Sp, -Sp], 1) + sides_path * 0.5)
pad_w = flt("high", 70, pad_w, 2)

# ===== mix + master
mix = nm(pad_w) * P["level"] * (1 - 0.2 * kenv)[:, None]
mix = mix + pan2(bus, 0) * B["level"] + bass_mid * B["level"]
mix = mix + nm(drm - pan2(kmono, 0) * 0.95) * D["level"]
mix = mix + nm(riser) * 0.85
mix = sg.sosfiltfilt(sg.butter(2, 20, "high", fs=SR, output="sos"), mix, axis=0)
mix = np.stack([dsp.eq(mix[:, c], "highshelf", 2500, 0.6, Mm["shelfDb"]) for c in range(2)], 1)
# cloakroom-inspired low/mid shelf balance on bass region (light)
mix = np.stack([dsp.eq(mix[:, c], "lowshelf", 90, 0.7, -0.5) for c in range(2)], 1)
mix = np.stack([dsp.eq(mix[:, c], "highshelf", 400, 0.7, 0.4) for c in range(2)], 1)
mix = np.tanh(Mm["satDrive"] * mix / (np.max(np.abs(mix)) + 1e-9)) / np.tanh(Mm["satDrive"])
M = 0.5 * (mix[:, 0] + mix[:, 1]); Sd = 0.5 * (mix[:, 0] - mix[:, 1])
Sd = sg.sosfiltfilt(sg.butter(4, Mm["sideHpHz"], "high", fs=SR, output="sos"), Sd)
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
json.dump(res, open(OUT + ".stats.json", "w"), indent=1, default=float)
print(json.dumps({"score": res["score"], "pass": res["pass"], "lufs": res["lufs"], "tp": res["extra"].get("true_peak_dbtp"), "gates": res["gates"], "subs": res["subs"], "tilt": res["extra"].get("tilt_db_oct"), "events": events, "gr": round(gr_max, 2), "len": res["lengthSec"], "drumsIn": res["drumsInSec"]}, default=float))
