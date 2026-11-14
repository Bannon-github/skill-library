#!/usr/bin/env python3
"""Daily 3-skill test 2026-11-14 "Dub Hang":
  L envelope-matched-chord-spacing-... (Loscil: 3-voice saw pad 6.5 s attack/decay, filter env, chords spaced so tails meet, ~29 s echo-verb; note-gated field recording -> filter/multiband/pingpong/verb + slow LFOs; sparse sine sequence into dark verb; unison saw sub LP24 80-200 Hz, 4-bar LFO)
  D dub-stab-family-...  (2 detuned saws, osc2 toward square -> LP24 res ~100 Hz env 48 -> HP 120; hand-drawn cutoff per repeat; dual resonant BP swept by 2-bar LFO + chorus; dub verb 4 s ducked by kick, echo, 6 s verb + long echo in breaks; group sat/low-mid cut/auto filter)
  C climax-break-structures-... (8-bar phrases; committed turnaround bar 15; trilogy break fall 16-20 / rise 20-25 / hang bar 25 / return 26)
usage: render.py recipe.json out.wav"""
import sys, os, json, numpy as np, soundfile as sf, pyloudnorm as pyln
from scipy import signal as sg
from scipy.signal import lfilter
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
def seg(b0, b1, xf=0.5): return np.clip((bar - b0) / xf, 0, 1) * np.clip((b1 - bar) / xf, 0, 1)
def ramp(b0, b1): return np.clip((bar - b0) / (b1 - b0), 0, 1)
def saw(f, L, ph=0.0): return dsp.osc_va(np.full(L, f), 0, 0.5, ph, SR)
events = 0
# ================= L: Loscil pad (envelope-matched chord spacing)
P = R["pad"]; padb = np.zeros((N, 2))
for ci, (b0, ch) in enumerate(zip(P["chordBars"], P["chords"])):
    nxt = P["chordBars"][ci + 1] if ci + 1 < len(P["chordBars"]) else NB
    hold = (nxt - b0) * BL; dur = hold + P["release"]; L = int(dur * SR); tt_ = np.arange(L) / SR
    a, d, s_, r_ = P["attack"], P["decay"], P["sustain"], P["release"]
    adsr = np.where(tt_ < a, tt_ / a, np.where(tt_ < a + d, 1 - (1 - s_) * (tt_ - a) / d, s_))
    adsr = adsr * np.where(tt_ < hold, 1.0, np.exp(-(tt_ - hold) / (r_ / 4)))
    cs = np.zeros(L)
    for vi, m in enumerate(ch):                                                    # stagger starts by hand
        off = int(vi * P["staggerMs"] / 1000 * SR); Lv = L - off
        for u in range(P["unison"]):
            dc = (u - (P["unison"] - 1) / 2) * P["detuneCents"]
            cs[off:] += saw(hz(m) * 2 ** (dc / 1200), Lv, rng.uniform()) / P["unison"] * (0.7 if m > 70 else 1.0)
        events += 1
    fenv = np.where(tt_ < a + d * 0.5, np.sin(np.pi / 2 * np.clip(tt_ / (a + d * 0.5), 0, 1)), 1 - np.clip((tt_ - a - d * 0.5) / (dur - a - d * 0.5), 0, 1))  # 2nd long env on cutoff
    fc = P["cutLow"] * (P["cutPeak"] / P["cutLow"]) ** fenv
    y = dsp.ladder(C(cs * 0.4), C(fc), P["res"], 0.1, 0, 0, SR) * adsr
    wid = np.stack([y, np.roll(y, int(0.011 * SR))], 1)
    put(padb, wid, tb(b0))
pe = dly(padb, P["echoBeats"] * BT, P["echoBeats"] * BT * 1.33, P["echoFb"], 1, 200, 5000)
pv = verb(padb + pe * 0.5, P["verbRt"], 11, 6000.0, 2.2)                                   # ~29 s echo-reverb
padL = nm(padb) * (1 - P["verbMix"]) + nm(pv) * P["verbMix"]
# ---- L: note-gated field recording (one held MIDI note gates it through synth filter/multiband/pingpong/verb)
F = R["field"]; ln = int(8 * SR)
wind = bw("band", [250, 2500], rng.standard_normal(ln), 2) * (0.6 + 0.4 * sm(np.abs(rng.standard_normal(ln)), 400) / 0.8)
leaves = bw("band", [2500, 9000], rng.standard_normal(ln), 2) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.21 * np.arange(ln) / SR) ** 2)
stream = bw("band", [1200, 5000], rng.standard_normal(ln), 2) * 0.6
fr = nm(wind + leaves + stream); xf = int(1.0 * SR); lp_ = fr[:ln - xf].copy(); lp_[:xf] = lp_[:xf] * np.linspace(0, 1, xf) + fr[ln - xf:] * np.linspace(1, 0, xf)
frL = np.tile(lp_, N // len(lp_) + 2)[:N]; frR = np.roll(frL, len(lp_) // 2)
gate = np.clip(t / 2.0, 0, 1)                                                                       # held note across timeline
lfo = np.sin(2 * np.pi * t / (F["lfoBars"] * BL))
fcf = F["lpBase"] * 2 ** (F["lfoDepthOct"] * lfo)
fld = np.stack([dsp.svf(C(x * gate), C(fcf), 0.7, 0, SR) for x in (frL, frR)], 1)
fld = bw("high", F["hp"], fld, 2)
bands = [bw("low", 800, fld, 4), bw("band", [800, 4000], fld, 4), bw("high", 4000, fld, 4)]           # multiband compressor
fld = sum(b * dsp.env_follow_gain(C(np.abs(b).mean(1)), SR, -30.0, F["mbRatio"], 0.02, 0.3)[:, None] for b in bands)
fld = fld + dly(fld, F["pingBeats"][0] * BT, F["pingBeats"][1] * BT, F["pingFb"], 1, 400, 9000) * 0.4
fld = fld * 0.6 + nm(verb(fld, F["verbRt"], 21, 10000.0)) * np.max(np.abs(fld)) * 0.5
fld = nm(fld) * (1 - F["volLfoDepth"] * (0.5 + 0.5 * np.sin(2 * np.pi * t / (F["lfoBars"] * BL * 0.75) + 1.3)))[:, None]
# ---- L: sparse sine sequence -> dark long reverb
Q = R["sines"]; sn = np.zeros(N)
for p0 in np.arange(Q["startBar"] * 4, NB * 4, Q["patBeats"]):
    for bt, m in Q["pattern"]:
        L = int((Q["decay"] + Q["release"] + 0.5) * SR); tt_ = np.arange(L) / SR
        env = np.minimum(tt_ / 0.02, 1) * (Q["sustain"] + (1 - Q["sustain"]) * np.exp(-tt_ / (Q["decay"] / 3)))
        env *= np.where(tt_ < Q["decay"], 1, np.exp(-(tt_ - Q["decay"]) / (Q["release"] / 4)))
        put(sn, np.sin(2 * np.pi * hz(m) * tt_) * env, (p0 + bt) * BT); events += 1
sn2 = pan2(sn, 0.2); snv = verb(sn2, Q["verbRt"], 31, float(Q["damp"]), 2.0)
sines = nm(sn2) * 0.45 + nm(snv) * 0.8
# ---- L: unison saw sub, LP24 80-200 Hz, free 4-bar LFO
U = R["sub"]; sb = np.zeros(N)
for ci, (b0, m) in enumerate(zip(P["chordBars"], U["roots"])):
    nxt = P["chordBars"][ci + 1] if ci + 1 < len(P["chordBars"]) else NB
    L = int((nxt - b0) * BL * SR); tt_ = np.arange(L) / SR
    y = sum(saw(hz(m) * 2 ** (d / 1200), L, k * 0.3) for k, d in enumerate((-U["detuneCents"], U["detuneCents"]))) / 2
    y *= np.minimum(tt_ / 0.3, 1) * np.clip((L / SR - tt_) / 0.3, 0, 1); put(sb, y, tb(b0))
fcs = U["cutLo"] * (U["cutHi"] / U["cutLo"]) ** (0.5 + 0.5 * np.sin(2 * np.pi * t / (U["lfoBars"] * BL)))
sb = dsp.ladder(C(sb * 0.5), C(fcs), 0.1, 0.2, 0, 0, SR)
sub_on = sm(np.where(((bar >= S["drumsIn"]) & (bar < S["fall"])) | ((bar >= S["stabsBack"]) & (bar < S["hang"])) | ((bar >= S["back"]) & (bar < S["end"] - 0.5)), 1.0, 0.0), 400)
sb = bw("low", 160, sb, 4) * sub_on
# ================= C + kick: structure gates
K = R["kick"]
def kick1():
    L = int(0.45 * SR); tt_ = np.arange(L) / SR; f = K["f1"] + (K["f0"] - K["f1"]) * np.exp(-tt_ / 0.025)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt_ / K["decay"]) * np.minimum(tt_ / 0.002, 1); y[-960:] *= np.linspace(1, 0, 960); return y
kick = np.zeros(N); k1 = kick1()
full = lambda b: (S["drumsIn"] <= b < S["turn"]) or (S["back"] <= b < S["drumsOut"])
for b in range(NB):
    if full(b) or (S["rise"] <= b < S["hang"]):
        for q in range(4): put(kick, k1, tb(b) + q * BT); events += 1
kick_lp = np.where((bar >= S["rise"]) & (bar < S["hang"]), 150 * (20000 / 150) ** ramp(S["rise"], S["hang"]), 20000.0)   # C: rise brings percussion back through opening filter
kick = dsp.svf(C(kick), C(np.minimum(kick_lp, 20000)), 0.7, 0, SR)
# ================= D: dub stab family
D = R["stab"]; stb = np.zeros(N); env_ = np.zeros(N); onehot = np.zeros(N)
stab_bars = lambda b: full(b) or (S["stabsBack"] <= b < S["hang"]) or (S["drumsOut"] <= b < S["end"] - 1)
def stab_osc(L, one):
    y = np.zeros(L)
    for m in D["chord"]:
        y += saw(hz(m), L, rng.uniform())
        if not one:
            o2 = (1 - D["sqBlend"]) * saw(hz(m) * 2 ** (D["detuneCents"] / 1200), L, rng.uniform()) + D["sqBlend"] * dsp.osc_va(np.full(L, hz(m) * 2 ** (D["detuneCents"] / 1200)), 1, 0.5, rng.uniform(), SR)
            y += o2
    return y / len(D["chord"])
for p0 in range(0, NB * 4, D["patBeats"]):
    for bt, kind in D["pattern"]:
        beat = p0 + bt; b = int(beat // 4)
        if not stab_bars(b): continue
        if b == S["turn"] - 1 and beat % 4 >= 2: continue
        dec = D["mainDecay"] if kind == "m" else D["ansDecay"]; L = int((dec * 4 + 0.3) * SR); tt_ = np.arange(L) / SR
        amp = np.minimum(tt_ / (D["attackMs"] / 1000), 1) * np.exp(-tt_ / (dec * 1.4)); amp[-480:] *= np.linspace(1, 0, 480)
        put(stb, stab_osc(L, kind == "a") * amp * (1.0 if kind == "m" else 0.75), beat * BT)
        e = np.exp(-tt_ / dec); i = int(round(beat * BT * SR)); Le = min(L, N - i); env_[i:i + Le] = np.maximum(env_[i:i + Le], e[:Le]); events += 1
# turnaround throw: one stab on bar 15 beat 1, then cut (C1 committed turnaround)
tb15 = tb(S["turn"]); L = int(1.6 * SR); tt_ = np.arange(L) / SR
put(stb, stab_osc(L, False) * np.minimum(tt_ / 0.008, 1) * np.exp(-tt_ / 0.45), tb15); i = int(tb15 * SR); env_[i:i + L] = np.maximum(env_[i:i + L], np.exp(-tt_ / 0.5)); onehot[i:i + L] = 1
# hang bar: one unique element = swelling stab chord (C3 hang)
L = int(BL * SR); tt_ = np.arange(L) / SR; sw = stab_osc(L, False) * (tt_ / (L / SR)) ** 2 * np.clip((L / SR - tt_) / 0.05, 0, 1)
put(stb, sw * 0.8, tb(S["hang"])); i = int(tb(S["hang"]) * SR); env_[i:i + L] = np.maximum(env_[i:i + L], (tt_ / (L / SR)) ** 1.5); events += 2
# hand-drawn cutoff: piecewise-linear drawn curve, a different shape each 2-bar repeat
pts = []; 
for r_ in range(0, NB, 2):
    shape = rng.uniform(-1, 1, 5); pts += [(r_ + k / 2.5, v) for k, v in enumerate(shape)]
draw = np.interp(bar, [p[0] for p in pts], [p[1] for p in pts]) * D["drawDepthOct"]
fcs_ = D["cutBase"] * 2 ** (D["envOct"] * sm(env_, 2) + draw + 0.6)
st1 = dsp.ladder(C(stb * 0.6), C(np.clip(fcs_, 40, 18000)), D["res"], 0.25, 0, 0, SR)
st1 = bw("high", D["hp"], st1, 2)
bp = D["bp"]; lfb = np.sin(2 * np.pi * t / (bp["lfoBars"] * BL)) * bp["depthOct"] * 0.5        # dual resonant BP, 2-bar LFO ~50% depth
b1 = dsp.svf(C(st1), C(bp["f1"] * 2 ** lfb), float(bp["q"]), 1, SR); b2 = dsp.svf(C(st1), C(bp["f2"] * 2 ** (-lfb)), float(bp["q"]), 1, SR)
st2 = st1 * (1 - bp["mix"]) + (b1 + b2) * bp["mix"] * 1.2
cl, cr = dsp.chorus(C(st2), C(st2), SR, 1, 0.4, 3.0, 9.0, 0.1, 1.0, 0.5, 0.0, 0.0)
st3 = np.stack([cl, cr], 1)
st3 = np.tanh(st3 * 2.0 / (np.max(np.abs(st3)) + 1e-9)) / np.tanh(2.0)                     # group saturator
st3 = dsp_eq = np.stack([dsp.eq(C(st3[:, c]), "lowshelf", 350, 0.7, -4.0) for c in range(2)], 1)   # low-mid shelf cut
brk = (bar >= S["turn"]) & (bar < S["back"])
afc = np.where(brk, 18000 * (900 / 18000) ** np.clip((bar - S["turn"]) / 1.0, 0, 1), 18000.0)  # auto filter slopes down in break...
afc = np.where((bar >= S["stabsBack"]) & (bar < S["back"]), 600 * (18000 / 600) ** ramp(S["stabsBack"], S["back"]), afc)       # ...and reopens in the rise
afc = sm(afc, 60)
st3 = np.stack([dsp.svf(C(st3[:, c]), C(afc), 0.7, 0, SR) for c in range(2)], 1)
st3 = np.tanh(st3 * 1.2) / 1.2                                                                          # tube warmth
key = np.abs(kick); kenv = sm(np.maximum.accumulate(key[::-1])[::-1] * 0 + sm(key, 5), 120); kenv = kenv / (kenv.max() + 1e-9)
duck = 1 - (1 - 10 ** (-D["duckDb"] / 20)) * np.clip(kenv * 2.5, 0, 1)
dv = verb(st3 * D["dubSend"], D["dubVerbRt"], 41, 7000.0, 2.0) * duck[:, None]                  # dub verb ducked by kick
ec = dly(st3, D["echoBeats"] * BT, D["echoBeats"] * BT * 1.5, D["echoFb"], 1, 300, 4500)
lsend = D["longSendBreak"] * sm(brk.astype(float), 600) + 0.12
lv = verb(st3 * lsend[:, None], D["longVerbRt"], 51, 5500.0, 2.4)                                   # 6 s verb, send up in breaks
be = dly(st3 * sm(brk.astype(float), 300)[:, None], D["breakEchoBeats"] * BT, D["breakEchoBeats"] * BT * 0.75, 0.55, 1, 300, 3500)
stabs = nm(st3) + nm(dv) * 0.55 + nm(ec) * 0.35 + nm(lv) * 0.5 * np.max(lsend) + nm(be) * 0.35
# ================= C: rise noise sweep
W = R["sweep"]; nz = rng.standard_normal((N, 2)); rs = ramp(S["rise"] + 1, S["hang"])
sfc = W["from"] * (W["to"] / W["from"]) ** rs
nzs = np.stack([dsp.svf(C(nz[:, c]), C(sfc), 2.0, 1, SR) for c in range(2)], 1) * (rs ** 2 * (bar < S["hang"]))[:, None]
# ================= mix + master
Mm = R["master"]
padg = (0.75 + 0.25 * sm(np.where((bar >= S["fall"]) & (bar < S["back"]), 1.0, 0.0), 800))           # fall: pad is one of the few elements left
mix = (nm(padL) * P["level"] * padg[:, None] + fld * F["level"] + nm(sines) * Q["level"] + nm(stabs) * D["level"]
       + nm(nzs) * W["level"] + pan2(sb / (np.max(np.abs(sb)) + 1e-9) * U["level"] + kick * K["level"], 0) / np.sqrt(2))
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
  "lufs_intro_A_fall_rise_hang_return": [round(meter.integrated_loudness(sec(a, b)), 1) for a, b in ((0, 4), (4, 15), (16, 20), (20, 25), (25, 26), (26, 34))],
  "first_half_vs_second_half_lufs": round(meter.integrated_loudness(mix[:N // 2]) - meter.integrated_loudness(mix[N // 2:]), 1)}
json.dump(res, open(OUT + ".stats.json", "w"), indent=1, default=float)
print(json.dumps({"score": res["score"], "pass": res["pass"], "lufs": res["lufs"], "tp": res["extra"].get("true_peak_dbtp"), "gates": res["gates"], "subs": res["subs"], "tilt": res["extra"].get("tilt_db_oct"), "gr": round(gr_max, 2), "len": res["lengthSec"], "drumsIn": res["drumsInSec"], "checks": res["checks"]}, default=float))
