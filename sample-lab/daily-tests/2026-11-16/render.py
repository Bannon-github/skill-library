#!/usr/bin/env python3
"""Daily 3-skill test 2026-11-16 "Quarter Light" (D minor, 90 BPM):
  H ambient-meta-chord-loop-... (i-bVI-iv-bVII/3 loop, one-step voice leading, mixed-interval extensions, no V7,
    bVII add2 first inversion, one unchanged maj7 ostinato over every chord, loop -> meta-chord)
  O orchestral-ostinato-bounce-to-sampler-... (bounce string ostinato, repitch x1 / -8va half speed / -15ma quarter speed,
    filtered arp bass + filtered lead, drive on sample layer, macro cutoff ride, console comp, shimmer verb, granular position scan,
    remarry with 'real' horns in heavy verb)
  P pad-vs-drone-roles-... (pad: saw + unison + attack/release + slow cutoff LFO, osc B triangle + slow pan LFO + chorus,
    100% wet aux verb low-cut + octave-up crystal + LFO'd overdrive mix, ping-pong one-note sampler pad, chord split
    bottom-2 -8va synth / top-2 +15ma sampler, group bus EQ/comp/opening filter, tuned field-recording drone + 2-oct copy, top-down mix drone last)
usage: render.py recipe.json out.wav"""
import sys, os, json, numpy as np, soundfile as sf, pyloudnorm as pyln
from scipy import signal as sg
from scipy.signal import lfilter
LAB = os.environ.get("LAB", "/workspace/skill-library/sample-lab"); sys.path.insert(0, LAB + "/engine")
import dsp, metrics
SR = 48000
R = json.load(open(sys.argv[1])); OUT = sys.argv[2]; rng = np.random.default_rng(R["seed"])
NB = R["bars"]; BL = 240 / R["bpm"]; BT = BL / 4; E8 = BT / 2; tb = lambda x: x * BL; S = R["sections"]
T = NB * BL + R["tailSec"]; N = int(T * SR); t = np.arange(N) / SR; bar = t / BL
hz = lambda m: 440 * 2 ** ((m - 69) / 12); C = np.ascontiguousarray
def bw(k, f, x, o=2): return sg.sosfilt(sg.butter(o, f, k, fs=SR, output="sos"), x, axis=0)
def pan2(x, p):
    p = np.asarray(p); return np.stack([x * np.cos((p + 1) * np.pi / 4), x * np.sin((p + 1) * np.pi / 4)], 1) * np.sqrt(2)
def put(buf, y, s, g=1.0):
    i = int(round(s * SR)); L = min(len(y), len(buf) - i)
    if L > 0 and i >= 0: buf[i:i+L] += y[:L] * g
def verb(x, rt, seed, damp=9000.0, size=1.8, mod=0.15, diff=0.75, pre=0.02):
    l, r = dsp.fdn_reverb(C(x[:, 0]), C(x[:, 1]), SR, float(rt), size, damp, pre, mod, diff, 0.0, seed); return np.stack([l, r], 1)
nm = lambda x: x / (np.max(np.abs(x)) + 1e-9)
def sm(x, ms): a = np.exp(-1 / (ms / 1000 * SR)); return lfilter([1 - a], [1, -a], x, axis=0)
def osc(f, L, shape=0, ph=0.0): return dsp.osc_va(np.full(L, float(f)), shape, 0.5, ph, SR)
def gate(b0, b1, xf_ms=300): return sm(((bar >= b0) & (bar < b1)).astype(float), xf_ms)
def ramp(pts):  # piecewise-linear automation in bars (smooth macro ride)
    b, v = zip(*pts); return np.interp(bar, b, v)
def env_ar(L, a, rel_at, rel):
    tt_ = np.arange(L) / SR
    return np.sin(np.pi / 2 * np.clip(tt_ / a, 0, 1)) ** 2 * np.where(tt_ < rel_at, 1.0, np.cos(np.pi / 2 * np.clip((tt_ - rel_at) / rel, 0, 1)) ** 2)
def resamp(x, ratio):  # repitch (non time-locked): ratio<1 -> slower + lower
    n = int(len(x) / ratio); return np.interp(np.arange(n) * ratio, np.arange(len(x)), x)
events = 0
CH = R["chords"]; nch = NB // CH["barsPer"]; ck = lambda k: k % len(CH["bass"])

# ================= H + O1: ostinato source (one unchanged maj7 eighth-note arpeggio), 'string' bounce
OS = R["ostinato"]
def string_note(f, L):
    x = sum(osc(f * 2 ** (d / 1200), L, 0, p) for d, p in ((-6, 0.1), (0, 0.4), (6, 0.7))) / 3
    return x * env_ar(L, 0.012, L / SR - 0.06, 0.06) * np.exp(-np.arange(L) / SR / 0.45)
src = np.zeros(int(BL * SR))
for i in range(8): put(src, string_note(hz(OS["notes"][i % 4]), int(E8 * SR * 1.6)), i * E8)   # 1-bar bounce (F A C E F A C E)
src = bw("low", OS["lp"], bw("high", 150, src, 2), 2); src = nm(src)
def tile(layer, b0, b1):
    out = np.zeros(N); Ls = len(layer); s = tb(b0)
    while s < tb(b1) - 1e-6: put(out, layer, s); s += Ls / SR
    return out * gate(b0, b1, 60)
SA = R["sampler"]
ost1 = tile(src, S["drumsIn"], S["drumsOut"])                                   # root layer (bars 4-28 incl. break for continuity)
half = tile(resamp(src, 0.5), S["layersIn"], S["drumsOut"])                     # -8va, half speed (quarter notes)
quart = tile(resamp(src, 0.25), S["layersIn"], S["end"])                        # -15ma, quarter speed (half notes)
events += 8
samp = ost1 * OS["level"] + half * SA["halfLevel"] + quart * SA["quarterLevel"]
samp = np.tanh(samp * SA["drive"]) / np.tanh(SA["drive"])                       # O4 drive on sample layer
cut = ramp(SA["cutoffPts"])                                                     # O5 macro cutoff ride (darker into the break)
samp = dsp.ladder(C(samp * 0.6), C(cut), 0.2, 0.1, 1, 0, SR)                     # multimode (LP12)
env = sm(sm(np.abs(samp), 10), 200); samp = samp / (1 + 1.5 * env / (env.max() + 1e-9))   # O6 console-style gentle comp
samp2 = pan2(samp, 0.0); sv = verb(samp2, 5.5, 7, 7000.0, 2.4)
sh = dsp.pitch_shift_delay(C(nm(sv.mean(1))), SR, 12.0, 0.18, 0.35, 400.0, 7000.0, 0.09)   # shimmer: +12 st in feedback loop
shim = np.stack([sh, np.roll(sh, int(0.021 * SR))], 1)
sampM = samp2 * 0.6 + nm(sv) * 0.45 * np.max(np.abs(samp2)) + nm(shim) * SA["shimmerMix"] * np.max(np.abs(samp2))
# O7 granular position scan (same bounce, -8va repitch in grains, slow sine scan, deterministic positions, Hann grains)
GR = R["granular"]; gsrc = bw("low", GR["lp"], np.tile(src, 4), 2); gsrc = sm(gsrc, 3)
gl = np.zeros(N); grr = np.zeros(N); Lg = int(GR["grainSec"] * SR); win = np.hanning(Lg); ratio = 2.0 ** GR["octave"]
nseg = int(Lg * ratio) + 2; phi = 0.0
for j in range(int(T * GR["density"])):
    st = j / GR["density"]; phi = (phi + 0.618034) % 1.0
    pos = (0.5 + 0.45 * np.sin(2 * np.pi * GR["scanHz"] * st)) * (len(gsrc) - nseg - 1) + phi * 0.02 * SR
    pos = int(np.clip(pos, 0, len(gsrc) - nseg - 1)); seg = gsrc[pos:pos + nseg]
    g = np.interp(np.arange(Lg) * ratio, np.arange(nseg), seg) * win
    put(gl if j % 2 == 0 else grr, g, st)
gran = bw("high", 120, np.stack([gl, grr], 1), 2); gran = nm(gran) * (0.6 * gate(S["layersIn"], S["end"] + 1, 2500) + 0.6 * gate(S["breakStart"], S["breakEnd"], 800))[:, None]
# O3 arpeggiated bass (filtered, not in your face) + simple analog lead filtered down further
BA = R["bassArp"]; bass = np.zeros(N); patt = [0, 12, 7, 12, 0, 12, 7, 12]
for b in range(S["drumsIn"], S["drumsOut"]):
    if S["breakStart"] <= b < S["breakEnd"]: continue
    root = CH["bass"][ck(b // CH["barsPer"])]
    for i, iv in enumerate(patt):
        L = int(E8 * SR * 0.95); f = hz(root + iv)
        put(bass, (osc(f, L, 0) * 0.6 + np.sin(2 * np.pi * f * np.arange(L) / SR)) * env_ar(L, 0.008, L / SR - 0.04, 0.04), tb(b) + i * E8); events += 1
bass = bw("low", BA["lp"], bass, 4)
LE = R["lead"]; lead = np.zeros(N)
for b0, m, nb in LE["notes"]:
    L = int((nb * BL + 1.0) * SR); f = hz(m)
    put(lead, (osc(f, L, 0, 0.2) + 0.5 * osc(f * 2 ** (4 / 1200), L, 1, 0.6)) * env_ar(L, 0.3, nb * BL, 1.0), tb(b0)); events += 1
lead = dsp.ladder(C(lead * 0.4), C(np.full(N, float(LE["lp"]))), 0.1, 0.0, 0, 0, SR)
leadS = pan2(nm(lead), 0.15); leadS = leadS * 0.7 + nm(verb(leadS, 4.0, 17, 6000.0, 2.0)) * 0.45
# O9 remarry with 'real' parts: sustained horn section (brass-ish saws, slow attack) drowned in heavy reverb
HO = R["horns"]; hor = np.zeros(N)
for k in range(nch):
    b0 = k * CH["barsPer"]
    if not (S["hornsIn"] <= b0 < S["drumsOut"]): continue
    for m in CH["upper"][ck(k)][:2]:
        L = int((CH["barsPer"] * BL + 1.2) * SR)
        put(hor, sum(osc(hz(m) * 2 ** (d / 1200), L, 0, p) for d, p in ((-5, 0.3), (5, 0.8))) * env_ar(L, 0.45, CH["barsPer"] * BL, 1.2), tb(b0)); events += 1
hor = bw("high", 180, dsp.ladder(C(hor * 0.4), C(np.full(N, float(HO["lp"]))), 0.1, 0.2, 0, 0, SR), 2)
horS = pan2(nm(hor), -0.2); horS = horS * 0.35 + nm(verb(horS, 6.5, 23, 5000.0, 2.6)) * 0.75

# ================= P: pad vs drone roles
PD = R["pad"]
# P6 split: synth keeps bottom two notes -8va, sampler takes top two +15ma
synL = np.zeros(N); synR = np.zeros(N); smp = np.zeros(N)
# P5 one-note sample pitched on C5, ping-pong loop (forward+reverse of a steady periodic tone = seamless), repitched
Ls = int(1.0 * SR); tt_ = np.arange(Ls) / SR; f0 = hz(72)
one = np.sin(2 * np.pi * f0 * tt_) + 0.35 * np.sin(4 * np.pi * f0 * tt_) + 0.12 * np.sin(6 * np.pi * f0 * tt_) + 0.04 * bw("band", [f0 * 2, f0 * 8], rng.standard_normal(Ls), 2)
pp = np.concatenate([one, one[::-1]])
for k in range(nch):
    b0 = k * CH["barsPer"]; up = CH["upper"][ck(k)]; hold = CH["barsPer"] * BL; L = int((hold + PD["release"]) * SR)
    en = env_ar(L, PD["attack"], hold, PD["release"])
    for j, m in enumerate(up[:2]):                                                # P2/P3 synth: saw unison + osc B triangle
        f = hz(m - 12)
        a = sum(osc(f * 2 ** (d / 1200), L, 0, p) for d, p in ((-7, 0.05), (0, 0.35), (7, 0.65))) / 3
        bq = osc(f * 2 ** (3 / 1200), L, 2, 0.5)
        lfo_p = 0.5 * np.sin(2 * np.pi * 0.05 * (tb(b0) + np.arange(L) / SR) + j * np.pi)   # slow pan LFO on osc B
        put(synL, (a * 0.7 + bq * 0.5 * np.cos((lfo_p + 1) * np.pi / 4) * np.sqrt(2)) * en, tb(b0))
        put(synR, (a * 0.7 + bq * 0.5 * np.sin((lfo_p + 1) * np.pi / 4) * np.sqrt(2)) * en, tb(b0))
    for m in up[2:]:
        r_ = 2 ** ((m + 24 - 72) / 12); need = int(L * r_) + 2
        loop = np.tile(pp, need // len(pp) + 1)[:need]
        put(smp, np.interp(np.arange(L) * r_, np.arange(need), loop) * en, tb(b0))
    events += 4
cf = PD["lp"] * 2 ** (PD["lfoDepth"] * np.sin(2 * np.pi * PD["lfoHz"] * t))      # small slow cutoff LFO
syn = np.stack([dsp.ladder(C(synL * 0.4), C(cf), 0.1, 0.1, 0, 0, SR), dsp.ladder(C(synR * 0.4), C(cf), 0.1, 0.1, 0, 0, SR)], 1)
cl, cr = dsp.chorus(C(syn[:, 0]), C(syn[:, 1]), SR, 0, 0.18, 1.2, 9.0, 0.0, 1.0, 0.35, 0.5, 0.0); syn = np.stack([cl, cr], 1)
smpS = bw("low", 7500, np.stack([smp, np.roll(smp, int(0.011 * SR))], 1), 2)
pads = nm(syn) * PD["level"] + nm(smpS) * PD["samplerLevel"]
# P4 aux: 100% wet verb, low-cut, octave-up crystal, overdrive with slow shallow LFO on mix -> treated as a layer
aux = bw("high", PD["auxLowCut"], verb(pads, 7.0, 3, 8000.0, 2.6), 2)
cry = dsp.pitch_shift_delay(C(nm(aux.mean(1))), SR, 12.0, 0.25, 0.2, 800.0, 9000.0, 0.1)
aux = nm(aux) + PD["crystalMix"] * np.stack([cry, np.roll(cry, int(0.017 * SR))], 1) / (np.max(np.abs(cry)) + 1e-9)
odm = (0.15 + 0.1 * np.sin(2 * np.pi * 0.04 * t))[:, None]; aux = aux * (1 - odm) + np.tanh(aux * 3) / np.tanh(3) * odm
pgrp = pads + nm(aux) * PD["auxLevel"]
# P7 group bus: shared EQ (HP where bass lives, dip where lead lives), light comp, slowly opening filter
pgrp = bw("high", PD["hp"], pgrp, 2); pgrp = np.stack([dsp.eq(C(pgrp[:, c]), "peak", 2500, 0.8, -3.0) for c in range(2)], 1)
ge = sm(sm(np.abs(pgrp).mean(1), 20), 300); pgrp = pgrp / (1 + 0.8 * ge / (ge.max() + 1e-9))[:, None]
op = PD["openFrom"] * (PD["openTo"] / PD["openFrom"]) ** np.clip(bar / NB, 0, 1)
pgrp = np.stack([dsp.ladder(C(pgrp[:, c] * 0.5), C(op), 0.05, 0.0, 1, 0, SR) for c in range(2)], 1)
# P8 drone: 'field recording' (wind noise) tuned to D by stacked resonant bands, looped, low-cut, verb; copy -2 oct
DR = R["drone"]; fd = hz(DR["midi"]); Ld = int(6 * SR); wn = sm(rng.standard_normal(Ld), 0.4)
fld = sum(g * dsp.svf(C(wn), C(np.full(Ld, fd * h)), 25.0, 1, SR) for h, g in ((1, 1.0), (2, 0.5), (3, 0.25)))  # bandpass
fld = nm(fld); xf = int(1.0 * SR); loopd = fld[xf:].copy(); loopd[-xf:] = loopd[-xf:] * np.linspace(1, 0, xf) + fld[:xf] * np.linspace(0, 1, xf)
dr1 = np.tile(loopd, N // len(loopd) + 2)[:N]; dr2 = np.tile(resamp(loopd, 0.25), N // (4 * len(loopd)) + 2)[:N]
dr = bw("high", 35, dr1 + 0.5 * bw("low", 200, dr2, 2), 2); drS = pan2(nm(dr), 0.0); drS = drS * 0.5 + nm(verb(drS, 5.0, 29, 4000.0, 2.2)) * 0.5
drS *= gate(0, S["end"] + 1, 4000)[:, None]

# ================= support drums (not under test; Matt: beat in by ~8 counts) -- kick 1&3, soft snare 2&4, soft offbeat shaker
DM = R["drums"]
def kick1():
    L = int(0.5 * SR); tt_ = np.arange(L) / SR; f = 50 + 70 * np.exp(-tt_ / 0.035)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt_ / 0.28) * np.minimum(tt_ / 0.004, 1); y = bw("low", 250, y, 4); y[-2400:] *= np.linspace(1, 0, 2400); return y
def snare1():
    L = int(0.4 * SR); tt_ = np.arange(L) / SR
    y = 0.5 * np.sin(2 * np.pi * 185 * tt_) * np.exp(-tt_ / 0.06) + bw("band", [1200, 5000], rng.standard_normal(L), 2) * np.exp(-tt_ / 0.09)
    y *= np.minimum(tt_ / 0.004, 1); y = bw("low", 6000, y, 2); y[-480:] *= np.linspace(1, 0, 480); return y
def shaker1():
    L = int(0.14 * SR); tt_ = np.arange(L) / SR
    y = rng.standard_normal(L) * np.minimum(tt_ / 0.015, 1) * np.exp(-tt_ / 0.04); y[-240:] *= np.linspace(1, 0, 240); return y
kick = np.zeros(N); sn = np.zeros(N); shk = np.zeros(N); k1 = kick1()
drum_on = lambda b: S["drumsIn"] <= b < S["drumsOut"] and not (S["breakStart"] <= b < S["breakEnd"])
for b in range(NB):
    if not drum_on(b): continue
    for q in (0, 2): put(kick, k1, tb(b) + q * BT); events += 1
    for q in (1, 3): put(sn, snare1(), tb(b) + q * BT); events += 1
    if b >= S["layersIn"]:
        for q in range(4): put(shk, shaker1(), tb(b) + (q + 0.5) * BT); events += 1
snS = pan2(sn, 0.05); snS = nm(snS) * 0.6 + nm(verb(snS, 3.0, 37, 6000.0, 2.0)) * 0.5
shS = pan2(bw("high", 5000, bw("low", 10000, shk, 2), 2), 0.2); shS = nm(shS) * 0.6 + nm(verb(shS, 3.0, 41, 7000.0, 2.0)) * 0.4
dbus = pan2(nm(kick), 0) / np.sqrt(2) * DM["kick"] + snS * DM["snare"] + shS * DM["shaker"]
kenv = sm(sm(np.abs(kick), 5), 90); kenv /= kenv.max() + 1e-9
duck = lambda d: (1 - (1 - 10 ** (-d / 20)) * np.clip(kenv * 2.5, 0, 1))[:, None]

if os.environ.get("DBG"):
    def spk(x):
        x = x.mean(1) if x.ndim == 2 else x; he = np.abs(bw("high", 8000, x, 4)); return int(np.sum(he > 8 * (sm(he, 50) + 1e-9)))
    for nmx, x in (("samp", sampM), ("gran", gran), ("pads", pgrp), ("drone", drS), ("drums", dbus), ("bass", bass), ("lead", leadS)): print(nmx, spk(x))
    sys.exit()
# ================= P9 top-down mix (pad in loud then cut; drone last, just audible, less sidechain) + master
Mm = R["master"]
mix = (nm(sampM) * 0.55 + gran * GR["level"] + pan2(nm(bass) * BA["level"], 0) / np.sqrt(2) + leadS * LE["level"] + horS * HO["level"]
       + nm(pgrp) * PD["level"] * duck(PD["duckDb"]) + drS * DR["level"] * duck(DR["duckDb"]) + dbus)
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
res["events"] = events; res["lengthSec"] = round(T, 2); res["lufs"] = round(meter.integrated_loudness(mix), 2); res["drumsInSec"] = round(tb(S["drumsIn"]), 2)
side = 0.5 * (mix[:, 0] - mix[:, 1]); mid = 0.5 * (mix[:, 0] + mix[:, 1]); db = lambda x: 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)
hf = bw("high", 8000, mid, 4); he = np.abs(hf); spikes = int(np.sum(he > 8 * (sm(he, 50) + 1e-9)))
ed = sm(he, 5)[::480]; fq, Pw = sg.welch(ed - ed.mean(), fs=100, nperseg=1024)
sec = lambda b0, b1: mix[int(tb(b0) * SR):int(tb(b1) * SR)]
res["checks"] = {"side_below_120Hz_db": round(db(bw("low", 120, side, 4)) - db(bw("low", 120, mid, 4)), 1), "hf_spikes_over_8x": spikes,
  "hf_env_12_40_vs_0_12_db": round(10 * np.log10(Pw[(fq >= 12) & (fq <= 40)].mean() / Pw[(fq > 0.2) & (fq < 12)].mean()), 1),
  "lufs_intro_A_B_break_C_outro": [round(meter.integrated_loudness(sec(a, b)), 1) for a, b in ((0, 4), (4, 12), (12, 20), (20, 22), (22, 28), (28, 30))]}
json.dump(res, open(OUT + ".stats.json", "w"), indent=1, default=float)
print(json.dumps({"score": res["score"], "pass": res["pass"], "lufs": res["lufs"], "tp": res["extra"].get("true_peak_dbtp"), "gates": res["gates"], "subs": res["subs"], "tilt": res["extra"].get("tilt_db_oct"), "gr": round(gr_max, 2), "len": res["lengthSec"], "drumsIn": res["drumsInSec"], "checks": res["checks"]}, default=float))
