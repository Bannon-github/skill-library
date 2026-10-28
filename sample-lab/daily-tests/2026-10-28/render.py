#!/usr/bin/env python3
"""Daily 3-skill test 2026-10-28 "Slow Reveal": fully wet extreme-reverb pad from percussive sources (pad/space)
+ epic hybrid drum (drums/FX hits) + withhold-the-reveal arrangement (structure). usage: render.py recipe.json out.wav"""
import sys, os, json, numpy as np, soundfile as sf, pyloudnorm as pyln
from scipy import signal as sg
LAB = os.environ.get("LAB", "/workspace/skill-library/sample-lab"); sys.path.insert(0, LAB + "/engine")
import dsp, metrics
SR = 48000
R = json.load(open(sys.argv[1])); OUT = sys.argv[2]; rng = np.random.default_rng(R["seed"])
bar = 240 / R["bpm"]; beat = bar / 4; T = R["bars"] * bar + R["tailSec"]; N = int(T * SR); t = np.arange(N) / SR
hz = lambda m: 440 * 2 ** ((m - 69) / 12); S = R["sections"]; D = R["drums"]; P = R["padSrc"]
def sos(k, f, o=2): return sg.butter(o, f, k, fs=SR, output="sos")
def flt(k, f, x, o=2): return sg.sosfilt(sos(k, f, o), x, axis=0)
def pan2(x, p): return np.stack([x * np.cos((p + 1) * np.pi / 4), x * np.sin((p + 1) * np.pi / 4)], 1) * np.sqrt(2)
def ramp(b0, b1): return np.clip((t - b0 * bar) / ((b1 - b0) * bar), 0, 1)
def gate(b0, b1, xf=0.0):
    if xf <= 0: return ((t >= b0 * bar) & (t < b1 * bar)).astype(float)
    return np.clip((t - b0 * bar) / xf + 0.5, 0, 1) * np.clip((b1 * bar - t) / xf + 0.5, 0, 1)
def smooth(x, ms=20): n = int(ms * SR / 1000); return sg.filtfilt(np.ones(n) / n, [1], x)
def put(buf, y, s, g=1.0):
    i = int(round(s * SR)); L = min(len(y), N - i)
    if L > 0: buf[i:i + L] += y[:L] * g
def db(x): return 10 ** (x / 20)
def verb(x, rt, seed, damp=None):
    damp = float(damp or P.get("damp", 9000.0))
    xs = x if x.ndim == 2 else pan2(x, 0.0)
    l, r = dsp.fdn_reverb(xs[:, 0].copy(), xs[:, 1].copy(), SR, float(rt), 1.6, damp, 0.03, 0.2, 0.75, 0.0, seed); return np.stack([l, r], 1)
events = 0
# ===== SKILL A: fully wet extreme-reverb pad from percussive sources
def strike(kind, m, L):
    tt = np.arange(L) / SR; f = hz(m); a = np.clip(tt / 0.002, 0, 1)
    if kind == "ep":   # distorted electric piano: FM tine with decaying index, overdriven
        idx = 2.5 * np.exp(-tt / 0.25); y = np.sin(2*np.pi*f*tt + idx*np.sin(2*np.pi*f*tt)) * np.exp(-tt / 1.4); y = np.tanh(2.5 * y)
    elif kind == "vib":  # vibraphone: fundamental + 4x partial, no tremolo (steady pitch)
        y = (np.sin(2*np.pi*f*tt) + 0.35*np.sin(2*np.pi*4*f*tt)*np.exp(-tt/0.3)) * np.exp(-tt / 2.5)
    elif kind == "pn":   # piano: inharmonic-ish partials with faster upper decays
        y = sum((0.7 ** k) * np.sin(2*np.pi*f*(k+1)*np.sqrt(1 + 0.0004*(k+1)**2)*tt) * np.exp(-tt / (2.0 / (k+1)**0.7)) for k in range(8))
    else:                # glockenspiel: 1, 2.76, 5.40 partials
        y = sum(g * np.sin(2*np.pi*f*r*tt) * np.exp(-tt / d) for r, g, d in ((1, 1, 1.8), (2.76, 0.5, 0.7), (5.40, 0.25, 0.3)))
    y = y * a; y[-480:] *= np.linspace(1, 0, 480); return y
def crush(x, bits, hold):
    q = 2 ** (bits - 1); y = np.round(x / (np.max(np.abs(x)) + 1e-9) * q) / q * np.max(np.abs(x)); return np.repeat(y[::hold], hold)[:len(x)]
def pad_group(times, notes, seed):
    src = {k: np.zeros(N) for k in ("ep", "vib", "pn", "gl")}
    for b in times:
        for i, m in enumerate(notes):                         # step 1: chord stacked across octaves, each source its own register
            for k, mm, g in (("ep", m, 1.0), ("pn", m, 0.8), ("vib", m + 12, 1.0), ("gl", m + 24, 0.6)):
                if k in ("vib", "gl") and i < 2: continue
                put(src[k], strike(k, mm, int(4 * SR)), b * bar + 0.006 * i, g)
    ep = verb(pan2(src["ep"], -0.25), P["epRt"], seed)                                            # step 2: 100% wet ~33 s
    vb = verb(verb(pan2(src["vib"], 0.25), P["vibRt"][0], seed + 1), P["vibRt"][1], seed + 2) * P["vibLevel"]  # step 3: two reverbs chained, turned down
    pn = flt("low", P["pnLp"], crush(src["pn"], P["pnBits"], P["pnHold"]), 4); pn = dsp.eq(pn, "peak", 3000, 1.0, -4)  # step 4: crush -> EQ -> verb 22 s
    pn = verb(pan2(pn, 0.1), P["pnRt"], seed + 3)
    gl = flt("low", P["glPreLp"], src["gl"]); gl = verb(verb(pan2(gl, -0.1), P["glRt"][0], seed + 4), P["glRt"][1], seed + 5) * P.get("glLevel", 0.6)  # step 5: top roll-off, ~40 s chained
    return ep + vb + pn + gl
PC = R["padChords"]; xf = 1.2
pad = (pad_group(*PC["pre"], 10) * gate(-1, S["reveal"], xf)[:, None] + pad_group(*PC["revealA"], 20) * gate(S["reveal"] - 0.05, PC["revealB"][0][0], xf)[:, None]
       + pad_group(*PC["revealB"], 30) * gate(PC["revealB"][0][0], S["outro"], xf)[:, None] + pad_group(*PC["outro"], 40) * gate(S["outro"] - 0.05, 99, xf)[:, None])
events += sum(len(v[0]) for v in PC.values())
# step 7: bus: low cut, compression, (sidechain applied later), LP filter; step 8: filter opens to introduce the pad
pad = flt("high", P["busHp"], pad, 2)
pad = np.stack([dsp.eq(pad[:, c], "highshelf", 2500, 0.7, P.get("busShelfDb", 0)) for c in range(2)], 1)   # bus EQ: tame low-mid build-up / lift air
g = dsp.env_follow_gain(np.mean(np.abs(pad), 1), SR, -20.0 + 20*np.log10(np.max(np.abs(pad)) + 1e-9), 2.0, 0.05, 0.6); pad *= g[:, None]
plp = P["busLpLo"] * (P["busLpHi"] / P["busLpLo"]) ** smooth(ramp(0, P["openBars"]), 50)
pad = np.stack([dsp.svf(pad[:, c].copy(), plp, 0.7, 0, SR) for c in range(2)], 1)
pad /= np.max(np.abs(pad)) + 1e-9
# ===== SKILL B: epic hybrid drum (4-channel synth hit + acoustic-style room layer, scooped and glued)
def hybrid(f0, dur, bright=1.0):
    L = int(dur * SR); tt = np.arange(L) / SR; amp = np.exp(-tt / D["ampTau"]); a = np.clip(tt / 0.0015, 0, 1)
    def sweep(up, tau): return f0 * 2 ** (up / 12 * np.exp(-tt / tau))
    f1 = sweep(D["pitchUp1"], D["pitchTau"]); ph1 = 2*np.pi*np.cumsum(f1)/SR
    ch1 = sum(np.sin(k * ph1) / k for k in (1, 2, 3)) * amp                                       # ch1 additive, +5 st drop
    fc = np.clip(200 + 9000 * np.exp(-tt / 0.006), 60, 20000)                                    # strongly curved closing env
    ch2 = dsp.svf(rng.standard_normal(L), fc, 0.9, 0, SR) * np.exp(-tt / 0.08) * 0.6             # ch2 white noise -> LP
    pink = dsp.noise(L, "pink", rng)
    ch3 = dsp.svf(np.asarray(pink, float), fc * 0.4, 1.2, 0, SR) * np.exp(-tt / 0.15)            # ch3 pink -> aggressive LP
    ch3 = dsp.svf(np.tanh(3.0 * (ch3 + 0.5 * ch1)), np.full(L, 900.0), 1.5, 0, SR) * 0.5          #   overloaded 2nd filter, also fed ch1
    fm = sweep(12, 0.008); phm = 2*np.pi*np.cumsum(fm)/SR
    ch4 = np.sin(phm + 1.8*np.exp(-tt/0.02)*np.sin(2*phm)); ch4 = np.tanh(2.5 * ch4) * np.exp(-tt / 0.12)  # FM fast drop -> tube
    ch4 = dsp.svf(ch4, np.full(L, 1800.0), 2.0, 0, SR); ch4 = flt("high", 45, ch4) * 0.6           #   MS-20-ish resonant LP -> HP
    f5 = sweep(D["pitchUp2"], D["pitchTau"] * 0.7); ch5 = sum(np.sin(k*2*np.pi*np.cumsum(f5)/SR)/k for k in range(1, 7)) * np.exp(-tt / 0.03) * 0.35 * bright  # ch4' +29 st top
    syn = (ch1 + ch2 + ch3 + ch4 + ch5) * a
    room = flt("band", [300, 6000], rng.standard_normal(L)) * np.exp(-tt / 0.25) * 0.12           # step 7 substitute: synthetic "bleed/room" layer (no acoustic samples in lab)
    room = flt("low", 5000, room)
    y = syn + room; y = dsp.eq(y, "peak", 450, 0.8, D["scoopDb"]); y = flt("high", D["subHp"], y)  # step 8: scooped EQ, trim subs
    lo = flt("low", 150, y); hi = y - lo; gl_ = dsp.env_follow_gain(np.abs(lo), SR, -12 + 20*np.log10(np.max(np.abs(lo)) + 1e-9), 3.0, 0.015, 0.12)
    y = lo * gl_ + hi                                                                             # multiband: low band compressed, 15 ms attack lets transient through
    y = np.tanh(1.3 * y / (np.max(np.abs(y)) + 1e-9)) / np.tanh(1.3); y[-480:] *= np.linspace(1, 0, 480); return y   # light OTT-ish density
kick = hybrid(D["kickF0"], 0.7, 0.5); toms = [hybrid(f, 0.6, 1.0) for f in D["tomF0"]]
fxhit = hybrid(D["tomF0"][1] * 1.5, 0.8, 1.2)
Lh = int(0.12 * SR); th = np.arange(Lh) / SR; hat = flt("band", [3000, 8000], rng.standard_normal(Lh)) * np.exp(-th / 0.02)
Lsh = int(0.09 * SR); tsh = np.arange(Lsh) / SR; shk = flt("band", [2500, 7000], rng.standard_normal(Lsh)) * np.clip(tsh / 0.012, 0, 1) * np.exp(-tsh / 0.03)
# ===== SKILL C: withhold-the-reveal arrangement
K = np.zeros(N); TM = np.zeros((N, 2)); HT = np.zeros(N); SH = np.zeros(N); FX = np.zeros(N)
sil = gate(*S["silence"], 0.01)
for b in range(S["kickIn"], S["kickOut"]):
    for k in range(16):
        tb = (b + k / 16) * bar
        if S["silence"][0] <= b + k/16 < S["silence"][1] or (b == S["reveal"] - 1 and k >= 12): continue   # step 7 silence / pre-reveal breath
        if k % 4 == 0: put(K, kick, tb); events += 1
        if b >= S["snareIn"] and b < S["outro"]:
            if k in (4, 12): put(TM, pan2(toms[0], 0.1), tb); events += 1
            if k == 14 and b % 2 == 1: put(TM, pan2(toms[1], -0.3), tb, 0.7); put(TM, pan2(toms[1], -0.3), tb + beat / 4, 0.5); events += 1  # flam
            if k % 2 == 0: put(HT, hat, tb, 0.7 + 0.3 * (k % 4 == 2))
        if b >= S["reveal"] and b < S["outro"] and k % 4 == 2: put(SH, shk, tb); events += 1             # held-back new percussion layer (off-beat shaker)
for b in (S["kickIn"], S["snareIn"], S["reveal"], S["outro"]): put(FX, fxhit, b * bar); events += 1    # step 6: FX hit marks each entry/exit
# step 2: filtered kick from the start of the beat (LP opens at the snare entry), full at reveal, filtered again in the outro
klp = D["kickLpLo"] * (20000 / D["kickLpLo"]) ** smooth(ramp(S["snareIn"] - 1, S["snareIn"]) * (1 - ramp(S["outro"], S["outro"] + 0.5)), 60)
K = dsp.svf(K, np.minimum(klp, 18000), 0.707, 0, SR)
# ostinato: three notes on 8ths, unchanged until the reveal (step 8: first change), C over the 2nd chord, A back in the outro (loopable)
O = R["ostinato"]; ost = np.zeros(N)
for b in range(S["ostIn"], S["end"]):
    pat = O["A"] if b < S["reveal"] or b >= S["outro"] else (O["B"] if b < R["padChords"]["revealB"][0][0] else O["C"])
    for k in range(8):
        if S["silence"][0] <= b + k/8 < S["silence"][1]: continue
        m = pat[(b * 8 + k) % 3]; L = int(beat * 0.9 * SR); tt = np.arange(L) / SR
        y = (dsp.osc_va(np.full(L, hz(m)), 0, 0.5, 0.0, SR) * 0.5 + np.sin(2*np.pi*hz(m)*tt)) * np.clip(tt/0.004, 0, 1) * np.exp(-tt/0.18); y[-240:] *= np.linspace(1, 0, 240)
        put(ost, y, (b + k / 8) * bar); events += 1
ost = dsp.svf(ost, np.full(N, float(O["lp"])), 0.8, 0, SR) * np.clip((t - S["ostIn"]*bar) / (2*bar), 0, 1)
# bass: one-note pedal until reveal (step 4, low-cut at times), moving line from the reveal, stops briefly at bassStop (step 9)
B = R["bass"]; bass = np.zeros(N)
for b in range(S["kickIn"], S["outro"]):
    if b < S["reveal"]:
        L = int(bar * SR * 1.01); tt = np.arange(L) / SR; f = hz(B["pedal"])
        y = np.sin(2*np.pi*f*tt) + 0.3*dsp.osc_va(np.full(L, f), 0, 0.5, 0.0, SR); y *= np.clip(tt/0.02, 0, 1) * np.clip((L/SR - tt)/0.03, 0, 1); put(bass, y, b * bar)
    else:
        line = B["lineB"] if b < R["padChords"]["revealB"][0][0] else B["lineC"]
        for k, m in enumerate(line):
            if b == S["bassStop"] and k < 2: continue
            if S["silence"][0] <= b + k/4 < S["silence"][1]: continue
            L = int(beat * 0.95 * SR); tt = np.arange(L) / SR; f = hz(m)
            y = (np.sin(2*np.pi*f*tt) + 0.35*dsp.osc_va(np.full(L, f), 0, 0.5, 0.0, SR)) * np.clip(tt/0.005, 0, 1) * np.clip((L/SR - tt)/0.02, 0, 1); put(bass, y, (b + k/4) * bar); events += 1
bhp = 30 + 90 * sum(gate(x, x + 1, 0.1) for x in B["lowcutBars"])
bass = dsp.svf(bass, smooth(bhp, 40), 0.707, 2, SR); bass = dsp.svf(bass, np.full(N, 900.0), 0.7, 0, SR)
# lead: held back until the reveal downbeat, steady pitch, 2 notes per bar
LD = R["lead"]; lead = np.zeros(N)
for j, m in enumerate(LD["notes"]):
    L = int(bar / 2 * 0.98 * SR); tt = np.arange(L) / SR; f = hz(m)
    y = (np.sin(2*np.pi*f*tt) + 0.25*dsp.osc_va(np.full(L, f), 1, 0.5, 0.0, SR)) * np.clip(tt/0.03, 0, 1) * np.clip((L/SR - tt)/0.08, 0, 1)
    put(lead, y, (S["reveal"] + j / 2) * bar); events += 1
lead = dsp.svf(lead, np.full(N, 3500.0), 0.7, 0, SR) * (1 - sil)
# building drone from the kick entry, LP opening toward the reveal
Dr = R["drone"]; drone = sum(dsp.osc_va(np.full(N, hz(m) * 2 ** (d / 1200)), 0, 0.5, rng.random(), SR) for m in Dr["notes"] for d in (-5, 5))
drone = dsp.svf(drone, 200 + 1200 * smooth(ramp(S["kickIn"], S["reveal"]), 50), 0.7, 0, SR); drone = flt("high", 140, drone)
drone *= gate(S["kickIn"], S["outro"], 2 * bar) * (0.4 + 0.6 * ramp(S["kickIn"], S["reveal"])) * (1 - sil)
# step 5: constant pad automated from about -3 dB (build/outro) to about -14 dB in the full section (post-reveal)
pdb = R["padDb"]["build"] + (R["padDb"]["full"] - R["padDb"]["build"]) * smooth(gate(S["reveal"], S["outro"], 0.5 * bar), 50)
kev = np.clip(sg.lfilter([1], [1, -np.exp(-1 / (0.12 * SR))], (np.abs(K) > 0.2).astype(float)) * 0.04, 0, 1); duck = 1 - 0.3 * kev   # bus sidechain
pad *= (db(pdb) * duck * (1 - 0.85 * sil))[:, None]
dry = pad * 0.9 + pan2(ost * O["level"] * duck, 0.15) + pan2(bass * B["level"] * duck, 0) + pan2(K * D["kick"], 0) + TM * D["tom"] + pan2(HT * D["hat"], -0.3)
dry += pan2(SH * D["shaker"], 0.35) + pan2(lead * LD["level"], -0.1) + pan2(drone * Dr["level"], 0.0) + pan2(FX * D["fx"], 0.0)
sendv = pan2(ost * O["level"], -0.2) * 0.5 + pan2(lead * LD["level"], 0.2) * 0.6 + TM * D["tom"] * 0.3 + pan2(FX * D["fx"], 0) * 0.8
wl = verb(flt("high", 250, sendv), 3.5, 7, 7000.0); mix = dry + 0.3 * wl
Mm = R["master"]; mix = sg.sosfiltfilt(sos("high", 20), mix, axis=0)
mix = np.tanh(Mm["satDrive"] * mix / (np.max(np.abs(mix)) + 1e-9)) / np.tanh(Mm["satDrive"])
M = 0.5 * (mix[:, 0] + mix[:, 1]); Sd = 0.5 * (mix[:, 0] - mix[:, 1]); Sd = sg.sosfiltfilt(sos("high", Mm["sideHpHz"], 4), Sd); mix = np.stack([M + Sd, M - Sd], 1)
fi = np.clip(t / Mm["fadeInSec"], 0, 1); fo = np.clip((T - 0.3 - t) / Mm["fadeOutSec"], 0, 1) ** 2; mix *= (fi * fo)[:, None]; mix -= mix.mean(0)
meter = pyln.Meter(SR); gr_max = 0.0
for it in range(5):
    mix *= 10 ** ((Mm["targetLufs"] - meter.integrated_loudness(mix)) / 20)
    tp = np.maximum(dsp.true_peak_env(mix[:, 0]), dsp.true_peak_env(mix[:, 1])); ceil = 10 ** (Mm["tpCeil"] / 20); la = int(0.005 * SR)
    g0 = np.minimum(1, ceil / np.maximum(tp, 1e-9)); g = np.minimum.reduce([np.roll(g0, k) for k in range(-la, la + 1, 24)]); g = np.minimum(sg.filtfilt(np.ones(la) / la, [1], g), 1)
    gr_max = max(gr_max, -20 * np.log10(g.min())); mix *= g[:, None]
    if abs(meter.integrated_loudness(mix) - Mm["targetLufs"]) < 0.3: break
mix -= mix.mean(0); mix[-int(0.3 * SR):] = 0; mix[:int(0.002*SR)] = 0; mix[int(0.002*SR):int(0.012*SR)] *= np.linspace(0, 1, int(0.010*SR))[:, None]
sf.write(OUT, mix.astype(np.float32), SR, subtype="PCM_24")
res = metrics.compute(mix, {"limiter_gr_db": gr_max}, R.get("category", "pad"), False, R["bars"] * bar, start_body_s=0.0, f_low=hz(38), bar_s=bar)
res["events"] = events; res["lengthSec"] = round(T, 2); res["lufs"] = round(meter.integrated_loudness(mix), 2)
json.dump(res, open(OUT + ".stats.json", "w"), indent=1, default=float)
print(json.dumps({"score": res["score"], "pass": res["pass"], "lufs": res["lufs"], "tp": res["extra"].get("true_peak_dbtp"), "gates": res["gates"], "subs": res["subs"], "events": events, "gr": round(gr_max, 2)}, default=float))
