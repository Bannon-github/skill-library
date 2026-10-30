#!/usr/bin/env python3
"""Daily 3-skill test 2026-10-30 "Planetarium": Eno space pad (source/space) + spacious ambient drums (drums)
+ three riser-free transitions (structure). usage: render.py recipe.json out.wav"""
import sys, os, json, numpy as np, soundfile as sf, pyloudnorm as pyln
from scipy import signal as sg
LAB = os.environ.get("LAB", "/workspace/skill-library/sample-lab"); sys.path.insert(0, LAB + "/engine")
import dsp, metrics
SR = 48000
R = json.load(open(sys.argv[1])); OUT = sys.argv[2]; rng = np.random.default_rng(R["seed"])
bar = 240 / R["bpm"]; beat = bar / 4; T = R["bars"] * bar + R["tailSec"]; N = int(T * SR); t = np.arange(N) / SR
hz = lambda m: 440 * 2 ** ((m - 69) / 12); S = R["sections"]; P = R["pad"]; D = R["drums"]
def sos(k, f, o=2): return sg.butter(o, f, k, fs=SR, output="sos")
def flt(k, f, x, o=2): return sg.sosfilt(sos(k, f, o), x, axis=0)
def pan2(x, p): return np.stack([x * np.cos((p + 1) * np.pi / 4), x * np.sin((p + 1) * np.pi / 4)], 1) * np.sqrt(2)
def gate(b0, b1, xf=0.0):
    if xf <= 0: return ((t >= b0 * bar) & (t < b1 * bar)).astype(float)
    return np.clip((t - b0 * bar) / xf + 0.5, 0, 1) * np.clip((b1 * bar - t) / xf + 0.5, 0, 1)
def smooth(x, ms=20): n = int(ms * SR / 1000); return sg.filtfilt(np.ones(n) / n, [1], x)
def put(buf, y, s, g=1.0):
    i = int(round(s * SR)); L = min(len(y), N - i)
    if L > 0 and i >= 0: buf[i:i + L] += y[:L] * g
def verb(x, rt, seed, damp=12000.0):
    l, r = dsp.fdn_reverb(x[:, 0].copy(), x[:, 1].copy(), SR, float(rt), 1.6, damp, 0.03, 0.2, 0.75, 0.0, seed); return np.stack([l, r], 1)
events = 0
# ===== SKILL A: Eno space pad
# step 2-3: two free-running smooth-random LFOs, each one's rate nudged by the other (cross-modulation)
def smooth_random(seed, n_pts=400):
    r = np.random.default_rng(seed); return r.uniform(-1, 1, n_pts)
def lfo_pair(r1, r2, cross):
    a = smooth_random(R["seed"] + 1); b = smooth_random(R["seed"] + 2); dt = 1 / 200; ts = np.arange(0, T + 1, dt)
    pa = pb = 0.0; A = np.zeros(len(ts)); B = np.zeros(len(ts)); va = vb = 0.0
    for i in range(len(ts)):   # control-rate: phase accumulators with cosine interpolation between random points
        fa = np.interp(pa % 1, [0, 1], [a[int(pa) % 400], a[(int(pa) + 1) % 400]]); fb = np.interp(pb % 1, [0, 1], [b[int(pb) % 400], b[(int(pb) + 1) % 400]])
        ca = 0.5 - 0.5 * np.cos(np.pi * (pa % 1)); cb = 0.5 - 0.5 * np.cos(np.pi * (pb % 1))
        va = a[int(pa) % 400] * (1 - ca) + a[(int(pa) + 1) % 400] * ca; vb = b[int(pb) % 400] * (1 - cb) + b[(int(pb) + 1) % 400] * cb
        A[i] = va; B[i] = vb; pa += r1 * (1 + cross * vb) * dt; pb += r2 * (1 + cross * va) * dt
    return np.interp(t, ts, A), np.interp(t, ts, B)
L2, L3 = lfo_pair(*P["lfoRateHz"], P["cross"])
mixAB = lambda wa, wb: np.clip(wa * L2 + wb * L3, -1, 1)          # step 4: every target gets a blend of both, sometimes inverted
padL = np.zeros(N); padR = np.zeros(N)
def tri(ph): return 2 * np.abs(2 * (ph % 1) - 1) - 1
for ci, b0 in enumerate(range(0, R["bars"], 2)):                    # two-chord track, 2 bars each, re-struck with long attack
    root, notes = R["chords"][ci % 2]; L = int((2 * bar + 4.0) * SR); i0 = int(b0 * bar * SR); tt = np.arange(L) / SR; seg = slice(i0, i0 + L)
    if i0 >= N: break
    L = min(L, N - i0); tt = tt[:L]
    env = np.clip(tt / P["atk"], 0, 1) * (P["sus"] + (1 - P["sus"]) * np.exp(-tt / 3.0))      # step 6: long attack, sloping sustain
    env *= np.clip((2 * bar + 4.0 - tt) / 4.0, 0, 1) ** 1.5                                     #   long release overlapping next chord
    l2 = 1 + 0.6 * mixAB(0.3, 0.9)[i0:i0 + L]; l3 = 1 + 0.6 * mixAB(0.9, -0.3)[i0:i0 + L]; l1 = 1 + 0.15 * mixAB(0.5, 0.5)[i0:i0 + L]
    for vi, c in enumerate(P["unisonCents"]):                                                  # step 9: light unison, steady pitch (no pitch LFO)
        for m in notes:
            f = hz(m) * 2 ** (c / 1200); ph0 = rng.random()
            y = l1 * np.sin(2*np.pi*(f*tt + ph0)) + P["lvl12"] * l2 * np.sin(2*np.pi*(2*f*tt + ph0)) + P["lvl19"] * l3 * np.sin(2*np.pi*(hz(m + 19)/hz(m)*f*tt + ph0))
            p = (vi - 1) * 0.5 + (notes.index(m) - 1.5) * 0.15
            padL[seg] += y * env * np.cos((p + 1) * np.pi / 4); padR[seg] += y * env * np.sin((p + 1) * np.pi / 4)
    sub = tri(hz(root) * tt) * P["sub"] * env * 2                                               # step 5: triangle sub, octave down (chord root)
    padL[seg] += sub; padR[seg] += sub; events += 1
pad = np.stack([padL, padR], 1)
pad += pan2(flt("high", 3000, dsp.noise(N, "pink", rng)), 0) * P["noise"] * np.max(np.abs(pad))  # step 5: trace of noise for air
# step 7: gentle LP, cutoff moved only slightly by LFOs; transitions skill also closes/dips this filter
lpdip = 1 - 0.85 * smooth(gate(S["leadSolo"], S["drop1"], bar * 0.8) + gate(S["mid"], S["drop2"], bar * 1.2) * 0.8 + gate(S["tease"], S["allIn"], bar * 0.8), 200)
fc = np.clip(P["lpBase"] * (1 + P["lpMod"] * mixAB(0.5, -0.5)) * lpdip + P["lpDip"] * (1 - lpdip) * 0.3, 200, 18000)
pad = np.stack([dsp.svf(pad[:, c].copy(), fc, 0.6, 0, SR) for c in range(2)], 1)
pad = np.stack([dsp.eq(pad[:, c], "highshelf", 3000, 0.7, P["shelfDb"]) for c in range(2)], 1)
pad /= np.max(np.abs(pad)) + 1e-9
# step 8: cathedral reverb + delay, both LFOs on wet mixes and delay feedback (not time); low-cut the returns
fxin = flt("high", P["fxLowcut"], pad)
rv = verb(fxin, P["verbRt"], 3, 9000.0)
fbk = P["dlyFb"][0] + (P["dlyFb"][1] - P["dlyFb"][0]) * (0.5 + 0.5 * mixAB(-0.6, 0.6)); Dd = int(P["dlyBeats"] * beat * SR)
dl = fxin.copy()
for s0 in range(Dd, N, Dd):                                                                      # time-varying feedback, block recursion
    e = min(s0 + Dd, N); dl[s0:e] += dl[s0 - Dd:e - Dd] * fbk[s0:e, None]
dl = dl - fxin; dl = np.stack([dl[:, 1], dl[:, 0]], 1); dl = flt("low", 6000, dl)
vm = P["verbMix"][0] + (P["verbMix"][1] - P["verbMix"][0]) * (0.5 + 0.5 * mixAB(0.7, 0.3))
dm = P["dlyMix"][0] + (P["dlyMix"][1] - P["dlyMix"][0]) * (0.5 + 0.5 * mixAB(-0.3, 0.8))
sh = dsp.pitch_shift_delay(np.mean(fxin, 1).copy(), SR, 7.0, 0.25, 0.4, 400.0, 7000.0, 0.08)    # step 10: shimmer at +7 st, mix moved slowly
shm = P["shimmerMix"][0] + (P["shimmerMix"][1] - P["shimmerMix"][0]) * (0.5 + 0.5 * mixAB(0.4, 0.6))
sh = verb(pan2(sh * shm, 0), 5.0, 9, 8000.0)
pad = pad + rv * vm[:, None] + dl * dm[:, None] + sh
pad /= np.max(np.abs(pad)) + 1e-9
# ===== SKILL B: spacious ambient drums
Lk = int(0.6 * SR); tk = np.arange(Lk) / SR; fk = D["kickF0"] * 2 ** (1.5 * np.exp(-tk / 0.03))
kick = np.sin(2 * np.pi * np.cumsum(fk) / SR) * np.exp(-tk / 0.25) * np.clip(tk / 0.001, 0, 1); kick = flt("high", 35, kick); kick[-480:] *= np.linspace(1, 0, 480)  # roll off very low end
Ls = int(0.35 * SR); ts_ = np.arange(Ls) / SR
snare = (flt("band", [1500, 7000], rng.standard_normal(Ls)) * np.exp(-ts_ / 0.06) + 0.5 * np.sin(2*np.pi*190*ts_) * np.exp(-ts_ / 0.05)) * np.clip(ts_ / 0.001, 0, 1)
snare *= np.clip((0.35 - ts_) / 0.05, 0, 1)                                                         # step 4: shortened tail
def hat(lp, dur=0.06, soft=False):
    L = int(dur * SR); th = np.arange(L) / SR; y = flt("high", 6000, rng.standard_normal(L))
    y = flt("low", lp, y) * np.exp(-th / (dur / 3)) * np.clip(th / (0.004 if soft else 0.0005), 0, 1)
    if soft: y *= (rng.random(L) > 0.7) * 1.6 + 0.3                                               # step 7: soft, crackly, low transient
    return y
ohat = hat(10000, 0.35)
Lc = int(0.25 * SR); tcl = np.arange(Lc) / SR; clap = np.zeros(Lc)
for k, d in enumerate((0, 0.011, 0.022)): put_ = int(d * SR); clap[put_:] += np.exp(-np.arange(Lc - put_) / SR / (0.006 if k < 2 else 0.12))
clap = flt("band", [1000, 6000], rng.standard_normal(Lc)) * clap
Lt = int(0.6 * SR); tt_ = np.arange(Lt) / SR; tom = np.sin(2*np.pi*np.cumsum(110 * 2 ** (0.4 * np.exp(-tt_ / 0.05)))/SR) * np.exp(-tt_ / 0.18)
tom = np.tanh(1.8 * tom) * np.clip(tt_ / 0.003, 0, 1); tom = flt("high", 70, tom); tom[-480:] *= np.linspace(1, 0, 480)  # step 8: saturated, low-cut, soft transient
K = np.zeros(N); SN = np.zeros(N); HS = np.zeros((N, 2)); HP = np.zeros((N, 2)); HO = np.zeros(N); CL = np.zeros(N); TM = np.zeros(N); SWL = np.zeros((N, 2))
on = lambda b, *names: any(S[a] <= b < S[z] for a, z in names)
for b in range(S["drumsIn"], S["end"]):
    pb = b % 4; phrase = b // 4
    kick_on = on(b, ("drumsIn", "mid"), ("drop2", "tease"), ("allIn", "end"))
    full = on(b, ("drop1", "mid"), ("drop2", "tease"), ("allIn", "end"))
    if kick_on and pb == 0: put(K, kick, b * bar); events += 1                                   # step 2: kick only in bar 1 of the phrase
    if kick_on and pb == 3: put(K, kick, (b + 0.875) * bar, 0.45); events += 1                   #   plus one ghost before the repeat
    if full and pb in (1, 3): put(SN, snare, (b + 0.5) * bar); events += 1                       # step 3: snares on bars 2 and 4 (beat 3)
    if full and pb == 2 and phrase % 2 == 1:                                                     # step 3: reversed reverb swell before bar 4 only, 2nd round
        rs = verb(pan2(snare, 0), 3.0, 5)[: int(bar * SR)][::-1]
        rs = rs + np.roll(rs[:, ::-1], int(0.012 * SR), 0) * 0.5                                 #   short widening delay
        put(SWL[:, 0], rs[:, 0], b * bar, 1); put(SWL[:, 1], rs[:, 1], b * bar, 1); events += 1
    if on(b, ("drumsIn", "mid"), ("drop2", "end")):
        for k in range(8):                                                                       # step 7: soft crackly 8th hats, swung, low transients
            sw = D["swing"] * beat if k % 2 else 0; tb = (b + k / 8) * bar + sw
            put(HS[:, 0], hat(7000, 0.05, True), tb, 0.6 + 0.4 * (k % 2 == 0)); put(HS[:, 1], hat(7000, 0.05, True), tb + 0.004, 0.6 + 0.4 * (k % 2 == 0))
        for j, k in enumerate((1, 3)):                                                           # step 5: two hats outside the kick, slightly ahead of the beat
            lp = D["pairLp"][j]                                                                  # step 6: 2-bar EQ LFO -> second hat always darker
            put(HP[:, 0 if j == 0 else 1], hat(lp, 0.08), (b + k / 4) * bar - 0.025, 1.0); events += 1
    if on(b, ("drop1", "end")) and not on(b, ("tease", "fill")) or on(b, ("tease", "allIn")):
        if not (S["drop1"] <= b < S["drop1"]): 
            for k in (1, 3): put(HO, ohat, (b + k / 4 + 0.125) * bar); events += 1                # open hats on offbeats in drops, mid and tease
# ===== SKILL C: three riser-free transitions
for b in range(S["mid"], S["drop2"]):
    for k in range(4): put(CL, clap, (b + k / 4) * bar); events += 1                             # transition 2: clap on the beat, no kick
put(TM, tom, (S["drop2"] - 0.25) * bar); events += 1                                              # step 4: one tom in the last beat's space
fl0 = S["fill"] * bar                                                                              # step 7: very short fill (sweep + claps) then all in
for k in range(3): put(CL, clap, fl0 + k * beat / 3, 0.7 + 0.15 * k)
sweep = flt("high", 2000, rng.standard_normal(int(beat * SR))) * np.linspace(0, 1, int(beat * SR)) ** 2; put(CL, sweep, fl0, 0.4)
mute_kick = 1 - smooth(gate(S["tease"], S["allIn"], 0.02), 5)
# bass enters at drop1 with kick (step 2); high-passed in mid (step 3), filter removed at drop2 (step 5); out in tease (step 6)
B = R["bass"]; bass = np.zeros(N)
for b in range(S["drop1"], S["end"]):
    if on(b, ("tease", "allIn")): continue
    root = R["chords"][(b // 2) % 2][0] + 12; L = int(bar * 0.98 * SR); tb = np.arange(L) / SR
    for k in (0, 0.5):
        Lh = L // 2; y = (np.sin(2*np.pi*hz(root)*tb[:Lh]) + 0.3 * dsp.osc_va(np.full(Lh, hz(root)), 0, 0.5, 0.0, SR)) * np.clip(tb[:Lh]/0.008, 0, 1) * np.clip((Lh/SR - tb[:Lh])/0.04, 0, 1)
        put(bass, y, (b + k) * bar); events += 1
bass = dsp.svf(bass, np.full(N, float(B["lp"])), 0.7, 0, SR)
bhp = 25 + (B["hpMid"] - 25) * smooth(gate(S["mid"], S["drop2"], 0.3), 100)
bass = dsp.svf(bass, bhp, 0.707, 2, SR)
# lead: steady-pitch pluck. solo + variation at leadSolo; var1 then original in mid; var2 at drop2; tease with spacing/velocity/pan; all in at the end
LD = R["lead"]; lead = np.zeros((N, 2))
def pluck(m, vel=1.0):
    L = int(beat * 1.6 * SR); tt = np.arange(L) / SR; f = hz(m)
    y = (np.sin(2*np.pi*f*tt) + 0.4 * dsp.osc_va(np.full(L, f), 1, 0.5, 0.0, SR) * np.exp(-tt / 0.15)) * np.clip(tt / 0.003, 0, 1) * np.exp(-tt / 0.45) * vel
    y[-480:] *= np.linspace(1, 0, 480); return y
def phrase(notes, b0, nb=2, vel=1.0, p=0.0, gap=1):
    global events
    for j, m in enumerate(notes):
        put(lead, pan2(pluck(m, vel), p), (b0 + j * gap * nb / len(notes)) * bar); events += 1
for b0 in range(S["drop1"], S["mid"], 2): phrase(LD["notes"], b0)
phrase(LD["var1"], S["leadSolo"], 1, 0.9, -0.1)                                                  # transition 1: lead alone, last bar = variation
phrase(LD["var1"], S["mid"]); phrase(LD["var1"], S["mid"] + 1, 1, 0.8, 0.15)                   # transition 2: variation looped
for b0 in range(S["drop2"], S["tease"], 2): phrase(LD["var2"] if b0 == S["drop2"] else LD["notes"], b0)
phrase(LD["notes"][:4], S["tease"], 1, 0.7, -0.3); phrase(LD["notes"][4:], S["tease"] + 1, 0.75, 0.85, 0.3)  # tease: same notes, new velocity/pan/space
for b0 in range(S["allIn"], S["end"] - 2, 2): phrase(LD["var2"], b0)
phrase(LD["notes"], S["end"] - 2, 2, 0.7)
lead = flt("low", LD["lp"], lead)
# noise bed ducked by percussion, ~3 s release, high-passed, very low (spacious drums step 10)
perc = np.abs(K) + np.abs(SN) + np.abs(HS[:, 0]) + np.abs(CL)
bed = flt("high", 1500, np.stack([dsp.noise(N, "pink", rng), dsp.noise(N, "pink", rng)], 1))
penv = sg.lfilter([1], [1, -np.exp(-1 / (3.0 * SR))], (perc > 0.02).astype(float) * (1 - np.exp(-1 / (3.0 * SR))) * 8); bedg = 1 / (1 + 8 * np.clip(penv, 0, 1))
bed *= (bedg * gate(S["drumsIn"], S["end"] + 2, bar))[:, None] * D["bed"]
# sidechain: pad bounces under kick (step 2)
kev = sg.lfilter([1], [1, -np.exp(-1 / (0.25 * SR))], (np.abs(K) > 0.3).astype(float)) * (1 - np.exp(-1 / (0.25 * SR))) * 40; duck = 1 - D["duck"] * np.clip(kev, 0, 1)
padlvl = 1 - 0.3 * smooth(gate(S["tease"], S["allIn"], bar * 0.5), 100)                        # tease: pad dips again
dry = pad * 0.8 * (duck * padlvl)[:, None] + pan2(K * D["kick"] * mute_kick, 0) + pan2(SN * D["snare"], 0.05) + HS * D["hatSoft"] + HP * D["hatPair"]
dry += pan2(HO * D["hatOpen"], 0.3) + pan2(CL * D["clap"], -0.05) + pan2(TM * D["tom"], -0.2) + SWL * D["revSwell"] + pan2(bass * B["level"], 0) + lead * LD["level"] + bed
snv = verb(flt("high", 300, pan2(SN * D["snare"], 0) * (np.arange(N) // int(4 * bar * SR) % 2 == 1)[:, None] + lead * LD["level"] * 0.5), 4.5, 7, 7000.0)  # step 3: big verb on 2nd round
mix = dry + 0.35 * snv
Mm = R["master"]; mix = sg.sosfiltfilt(sos("high", 20), mix, axis=0)
mix = np.stack([dsp.eq(mix[:, c], "highshelf", 2500, 0.6, Mm.get("shelfDb", 0)) for c in range(2)], 1)  # master air shelf
mix = np.tanh(Mm["satDrive"] * mix / (np.max(np.abs(mix)) + 1e-9)) / np.tanh(Mm["satDrive"])
M = 0.5 * (mix[:, 0] + mix[:, 1]); Sd = 0.5 * (mix[:, 0] - mix[:, 1]); Sd = sg.sosfiltfilt(sos("high", Mm["sideHpHz"], 4), Sd); mix = np.stack([M + Sd, M - Sd], 1)
fo = np.clip((T - 0.3 - t) / Mm["fadeOutSec"], 0, 1) ** 2; mix *= fo[:, None]; mix -= mix.mean(0)
meter = pyln.Meter(SR); gr_max = 0.0
for it in range(5):
    mix *= 10 ** ((Mm["targetLufs"] - meter.integrated_loudness(mix)) / 20)
    tp = np.maximum(dsp.true_peak_env(mix[:, 0]), dsp.true_peak_env(mix[:, 1])); ceil = 10 ** (Mm["tpCeil"] / 20); la = int(0.005 * SR)
    g0 = np.minimum(1, ceil / np.maximum(tp, 1e-9)); g = np.minimum.reduce([np.roll(g0, k) for k in range(-la, la + 1, 24)]); g = np.minimum(sg.filtfilt(np.ones(la) / la, [1], g), 1)
    gr_max = max(gr_max, -20 * np.log10(g.min())); mix *= g[:, None]
    if abs(meter.integrated_loudness(mix) - Mm["targetLufs"]) < 0.3: break
mix -= mix.mean(0); mix[-int(0.3 * SR):] = 0; mix[:int(0.002*SR)] = 0; mix[int(0.002*SR):int(0.2*SR)] *= np.linspace(0, 1, int(0.198*SR))[:, None]
sf.write(OUT, mix.astype(np.float32), SR, subtype="PCM_24")
res = metrics.compute(mix, {"limiter_gr_db": gr_max}, R.get("category", "pad"), False, R["bars"] * bar, start_body_s=0.0, f_low=hz(41), bar_s=bar)
res["events"] = events; res["lengthSec"] = round(T, 2); res["lufs"] = round(meter.integrated_loudness(mix), 2)
json.dump(res, open(OUT + ".stats.json", "w"), indent=1, default=float)
print(json.dumps({"score": res["score"], "pass": res["pass"], "lufs": res["lufs"], "tp": res["extra"].get("true_peak_dbtp"), "gates": res["gates"], "subs": res["subs"], "extra": {k: res["extra"].get(k) for k in ("tilt_db_oct",)}, "events": events, "gr": round(gr_max, 2)}, default=float))
