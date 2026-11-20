#!/usr/bin/env python3
"""Daily 3-skill test 2026-11-20 "Wedge Lanes" (A minor, 90 BPM):
  A async dual band-pass micro-loop texture (haZ6byjMpOk): 3-beat seamless played loop -> two PARALLEL narrow BP lanes swept by
    free-running unrelated LFOs (0.0413 / 0.0659 Hz), delay per lane, octave-down (exact 2:1) on lane 2, bus with very slow
    unrelated auto-pan (0.0237 Hz) + reverb
  W correlation-meter widening (LcAcmBKryxE): Haas comb test (rejected, logged), stereo phaser on held pad + M/S side gain,
    subtle linear chorus on the lead, multiband width map (mono <120, low-mid 0.8, upper-mid widest until corr ~0, highs 0.9)
  F ambient variation sets + focus map (CW3jk3BgE1E): texture/pad/melody voices with lettered variations
    (pad low/mid/high filter sets, 3-step x 4-step paraphonic sequence, gate->decay env opens LP, attenuated smooth-random shape
    + LFO->VCA->FM; melody 1 osc HP+LP with attenuated LFOs on filter spread + wave shape), chained along a focus map + freq slots
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
def verb(x, rt, seed, damp=9000.0, size=1.8, mod=0.15, diff=0.75, pre=0.02):
    l, r = dsp.fdn_reverb(C(x[:, 0]), C(x[:, 1]), SR, float(rt), size, damp, pre, mod, diff, 0.0, seed); return np.stack([l, r], 1)
nm = lambda x: x / (np.max(np.abs(x)) + 1e-9)
def sm(x, ms): a = np.exp(-1 / (ms / 1000 * SR)); return lfilter([1 - a], [1, -a], x, axis=0)
def gate(b0, b1, xf_ms=300): return sm(((bar >= b0) & (bar < b1)).astype(float), xf_ms)
def wander(rate_hz, seed):  # smooth random (cosine-interpolated), timbre-only use
    r = np.random.default_rng(seed); ph = t * rate_hz; k = ph.astype(int); fr = ph - k
    pts = r.uniform(-1, 1, k[-1] + 3); w = (1 - np.cos(np.pi * fr)) / 2; return pts[k] * (1 - w) + pts[k + 1] * w
FM = R["focusMap"]; BD = FM["bounds"]
def focus(key, xf_bars=1.0):  # focus-map weight curve, crossfaded over ~1 bar (performed automation)
    v = np.zeros(N)
    for i in range(5): v += FM[key][i] * ((bar >= BD[i]) & (bar < BD[i + 1]))
    v[bar >= BD[-1]] = FM[key][-1]; return sm(sm(v, xf_bars * BL * 500), xf_bars * BL * 500)
def stereo_of(x): return x if x.ndim == 2 else pan2(x, 0)
events = 0; CH = R["chords"]; BP = CH["barsPer"]; NCH = len(CH["names"])
chord_at = lambda s: int(s / (BP * BL)) % NCH
# ================= F: pad voice (2 osc paraphonic polymetric 3 x 4 step sequences)
P = R["pad"]; stp = P["stepBeats"] * BT; nst = int(np.ceil(T / stp))
fA = np.zeros(N); fB = np.zeros(N); envd = np.zeros(N)
for k in range(nst):
    s0 = k * stp; i0 = int(s0 * SR); i1 = min(int((s0 + stp) * SR), N)
    if i0 >= N: break
    c = chord_at(s0 + 1e-6); tones = CH["tones"][c]
    fA[i0:i1] = hz(tones[P["seqA"][k % 3]] - 12); fB[i0:i1] = hz(tones[P["seqB"][k % 4]])
    tt = np.arange(i1 - i0) / SR; envd[i0:i1] = (1 - np.exp(-tt / 0.025)) * np.exp(-tt / P["envDecay"]) + 0.3 * np.exp(-tt / 0.025)  # gate -> decay env (opens LP)
    events += 2
fA = sm(fA, 4); fB = sm(fB, 4); envd = sm(envd, 3)  # 4 ms portamento-free smoothing (no slides, no clicks)
shp = 0.5 + 0.5 * P["shapeAtt"] * wander(P["shapeRandHz"], 3)  # attenuated smooth random -> osc A wave shape (saw<->tri)
oA = (1 - shp) * dsp.osc_va(C(fA), 0, 0.5, 0.0, SR) + shp * dsp.osc_va(C(fA), 2, 0.5, 0.0, SR)
fmlfo = 0.5 + 0.5 * np.sin(2 * np.pi * P["fmLfoHz"] * t)
oB = dsp.osc_fm(C(fB), P["fmRatio"], C(1.2 * P["fmAtt"] * fmlfo), 0.0, SR)  # LFO -> VCA -> FM input of osc B
padsrc = 0.55 * oA + 0.45 * oB
def padvar(v, envamt):
    fc = v["lp"] * 2 ** (envamt * envd); y = dsp.svf(C(padsrc), C(fc), 0.8, 0, SR)
    y = bw("high", v["hp"], y, 2); return bw("low", 6000, np.tanh(v["drive"] * y) / np.tanh(v["drive"]), 4)  # LP after drive: no regenerated edge fizz
PV = P["var"]; padL = padvar(PV["low"], P["envAmtOct"] * 0.6); padMd = padvar(PV["mid"], P["envAmtOct"]); padH = padvar(PV["high"], P["envAmtOct"])
padsrc_lp = None
padin = gate(S["padIn"], NB + 5, BL * 1000)
padM = (nm(padL) * focus("padLow") + nm(padMd) * focus("padMid") * 0.8 + nm(padH) * focus("padHigh") * 0.6) * padin
# ================= A: async dual band-pass micro-loop texture
X = R["texture"]; Ll = int(X["loopBeats"] * BT * SR); loop = np.zeros(Ll); loopo = np.zeros(Ll)
def bell(m, L):
    tt = np.arange(L) / SR; f = hz(m)
    y = (np.sin(2 * np.pi * f * tt) + 0.35 * np.sin(4 * np.pi * f * tt) + 0.12 * np.sin(6 * np.pi * f * tt)) * np.exp(-tt / 0.9)
    return y * np.minimum(tt / 0.006, 1)
for j, m in enumerate(X["loopNotes"]):  # played micro-loop, wrapped circularly -> seamless
    i0 = int(j * X["noteBeats"] * BT * SR)
    for buf, mm in ((loop, m), (loopo, m - 12)):  # octave-down copy = exact 2:1 (steady pitch)
        y = bell(mm, Ll); idx = (i0 + np.arange(Ll)) % Ll; np.add.at(buf, idx, y)
src = np.tile(loop, N // Ll + 1)[:N]; srco = np.tile(loopo, N // Ll + 1)[:N]
def sweep(fhz, ph): return X["bpLoHz"] * (X["bpHiHz"] / X["bpLoHz"]) ** (0.5 + 0.5 * np.sin(2 * np.pi * fhz * t + ph))
f1 = sweep(X["lfo1Hz"], 0.3); f2 = sweep(X["lfo2Hz"], 2.1)
lane1 = dsp.svf(C(src), C(f1), X["bpQ"], 1, SR)
lane2 = dsp.svf(C(src), C(f2), X["bpQ"], 1, SR); oct2 = dsp.svf(C(srco), C(f2 * 0.5), X["bpQ"], 1, SR)
def ldelay(x, d, fb):
    l, r = dsp.stereo_delay(C(x), C(x), SR, d, d * 1.07, fb, fb, 0.0, 0.0, 0, 150.0, 6000.0, 0.0, 0.0, 0.0); return np.stack([l, r], 1)
L1 = pan2(lane1, -0.35) + 0.6 * ldelay(lane1, *X["dly1"])
l2 = lane2 + X["octDownLvl"] * oct2; L2 = pan2(l2, 0.35) + 0.6 * ldelay(l2, *X["dly2"])
bus = nm(L1) + nm(L2)
pa = X["panDepth"] * np.sin(2 * np.pi * X["panHz"] * t + 1.0)  # very slow, unrelated-rate auto-pan (balance)
gl = np.sqrt(np.clip(1 - pa, 0, 2) / 2) * np.sqrt(2); gr = np.sqrt(np.clip(1 + pa, 0, 2) / 2) * np.sqrt(2)
bus = bus * np.stack([gl, gr], 1)
tex = nm(bus) + X["verbMix"] * nm(verb(bus, X["verbRt"], 17, 7000.0, 2.2))
TV = X["var"]
tDeep = bw("low", TV["deep"]["lp"], tex, 2)
tDeep = tDeep + (10 ** (TV["deep"]["lowShelfDb"] / 20) - 1) * bw("low", 300, tex, 2)
tThin = bw("high", TV["thin"]["hp"], tex, 2)
air = bw("high", 3000, dsp.noise(N, "pink", np.random.default_rng(41)), 2)
air = dsp.svf(C(air), C(np.clip(f1 * 3, 2500, 14000)), 2.0, 1, SR)  # air slice follows lane-1 sweep (steady, no ticks)
tBright = bw("high", TV["bright"]["hp"], tex, 2) + 0.35 * pan2(nm(air), 0) * np.stack([gr, gl], 1) * 0.5
texM = nm(tDeep) * focus("texDeep")[:, None] + nm(tThin) * focus("texThin")[:, None] * 0.8 + nm(tBright) * focus("texBright")[:, None] * 0.8
events += len(X["loopNotes"])
# ================= F: melody voice
ML = R["melody"]; melo = np.zeros(N); fmel = np.full(N, hz(69.0)); gm = np.zeros(N)
for ph0 in range(S["melodyIn"], S["drumsOut"], ML["phraseBars"]):
    for b, beat, m, d in ML["notes"]:
        s0 = tb(ph0 + b) + beat * BT; i0 = int(s0 * SR); L = int(d * BT * SR)
        if i0 + L > N: continue
        fmel[i0:i0 + L] = hz(m); tt = np.arange(L) / SR
        e = np.minimum(tt / 0.02, 1) * (0.35 + 0.65 * np.exp(-tt / ML["decay"])) * np.minimum((d * BT - tt) / 0.08, 1)
        gm[i0:i0 + L] = np.maximum(gm[i0:i0 + L], e); events += 1
fmel = sm(fmel, 3)
wsh = 0.5 + 0.5 * ML["pwAtt"] * np.sin(2 * np.pi * ML["pwLfoHz"] * t)  # attenuated LFO -> wave shape (saw<->pulse)
mo = (1 - wsh) * dsp.osc_va(C(fmel), 0, 0.5, 0.0, SR) + wsh * dsp.osc_va(C(fmel), 1, 0.5, 0.0, SR)
spr = ML["spreadAtt"] * np.sin(2 * np.pi * ML["spreadLfoHz"] * t + 0.7)  # attenuated LFO -> filter spread
mo = dsp.svf(C(mo), C(ML["lpBase"] * 2 ** spr), 0.9, 0, SR); mo = dsp.svf(C(mo), C(ML["hp"] * 2 ** (-spr)), 0.8, 2, SR)
melo = mo * gm * focus("melody")
# ================= W: correlation-meter widening
W = R["width"]
def corr(x): return float(np.sum(x[:, 0] * x[:, 1]) / (np.sqrt(np.sum(x[:, 0] ** 2) * np.sum(x[:, 1] ** 2)) + 1e-12))
def monoloss(x): m = x.mean(1); return 10 * np.log10((np.mean(x ** 2) + 1e-12) / (np.mean(m ** 2) + 1e-12))
seg = padMd[int(tb(4) * SR):int(tb(12) * SR)]
haas = np.stack([seg, np.concatenate([np.zeros(int(0.012 * SR)), seg[:-int(0.012 * SR)]])], 1)  # step 2: Haas test (rejected)
haas_mono = haas.mean(1); hspec = 10 * np.log10(sg.welch(haas_mono, SR, nperseg=8192)[1] + 1e-20) - 10 * np.log10(sg.welch(seg, SR, nperseg=8192)[1] + 1e-20)
def ms_side(x, g): m = x.mean(1); s = 0.5 * (x[:, 0] - x[:, 1]) * g; return np.stack([m + s, m - s], 1)
pl = dsp.phaser(C(padM), W["phaserRate"], W["phaserDepth"], 0.3, 4, W["phaserMix"], 0.0, SR)
pr = dsp.phaser(C(padM), W["phaserRate"], W["phaserDepth"], 0.3, 4, W["phaserMix"], np.pi / 2, SR)
padS = ms_side(np.stack([pl, pr], 1), W["sideGainPad"])
padS = padS + 0.35 * nm(verb(padS, 5.0, 11, 6000.0, 2.2)) * np.max(np.abs(padS))
cl, cr = dsp.chorus(C(melo), C(melo), SR, 0, W["chorusRate"], W["chorusDepthMs"], 8.0, 0.0, 1.0, W["chorusMix"], 0.25, 0.0)  # linear chorus (lead)
melS = np.stack([cl, cr], 1); melS = nm(melS) * 0.8 + 0.3 * nm(verb(melS, 3.2, 23, 7000.0, 1.8))
LV = R["levels"]
music = nm(padS) * LV["pad"] + nm(texM) * LV["tex"] + melS * LV["melody"]
corr_before = corr(music); ml_before = monoloss(music)
def zlp(x, f): return sg.sosfiltfilt(sg.butter(4, f, "low", fs=SR, output="sos"), x, axis=0)
def widthmap(x, gains):
    m = x.mean(1); s = 0.5 * (x[:, 0] - x[:, 1]); a, b, c = W["bandSplits"]
    sb = [zlp(s, a)]; r1 = s - sb[0]; lo2 = zlp(r1, b); sb.append(lo2); r2 = r1 - lo2; lo3 = zlp(r2, c); sb += [lo3, r2 - lo3]
    mb = [zlp(m, a)]; q1 = m - mb[0]; m2 = zlp(q1, b); mb.append(m2); q2 = q1 - m2; m3 = zlp(q2, c); mb += [m3, q2 - m3]
    return np.stack([m + sum(g * v for g, v in zip(gains, sb)), m - sum(g * v for g, v in zip(gains, sb))], 1), mb, sb
gains = list(W["bandSide"]); bandcorr = []
for _ in range(8):  # step 6: push upper mids until the band correlation touches (not crosses) the floor
    out, mb, sb = widthmap(music, gains)
    bc = [float((np.sum(m_ ** 2) - np.sum((g * s_) ** 2)) / (np.sum(m_ ** 2) + np.sum((g * s_) ** 2) + 1e-12)) for g, m_, s_ in zip(gains, mb, sb)]
    bandcorr = bc
    if bc[2] < W["corrFloor"]: gains[2] *= 0.85
    elif bc[2] > 0.35 and gains[2] < 2.2: gains[2] *= 1.1
    else: break
music = out
widthlog = {"haas12ms_mono_notch_db": round(float(np.percentile(hspec[(np.arange(len(hspec)) * SR / 8192 > 200) & (np.arange(len(hspec)) * SR / 8192 < 8000)], 2)), 1),
  "haas12ms_monoloss_db": round(monoloss(haas), 2), "phaserpad_corr": round(corr(padS), 3), "phaserpad_monoloss_db": round(monoloss(padS), 2),
  "music_corr_before_after": [round(corr_before, 3), round(corr(music), 3)], "music_monoloss_before_after": [round(ml_before, 2), round(monoloss(music), 2)],
  "band_side_gains": [round(g, 2) for g in gains], "band_corr": [round(c, 3) for c in bandcorr]}
# ================= drums + bass (support; enter bar 4)
K = R["kick"]
def kick1():
    L = int(K["gate"] * SR); tt = np.arange(L) / SR; f = K["endHz"] + (K["startHz"] - K["endHz"]) * np.exp(-tt / (K["tauMs"] / 1000))
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / K["decay"]) * np.minimum(tt / 0.003, 1)
    fw = int(0.08 * SR); y[-fw:] *= np.cos(np.linspace(0, np.pi / 2, fw)) ** 2; return y
def snare1():
    L = int(0.5 * SR); tt_ = np.arange(L) / SR
    y = 0.35 * np.sin(2 * np.pi * 185 * tt_) * np.exp(-tt_ / 0.05) + bw("band", [700, 3500], rng.standard_normal(L), 2) * np.exp(-tt_ / 0.13)
    y *= np.minimum(tt_ / 0.015, 1); y = bw("low", 3500, y, 2); y[-480:] *= np.linspace(1, 0, 480); return y
kick = np.zeros(N); sn = np.zeros(N); bass = np.zeros(N); k1 = kick1()
for b in range(S["drumsIn"], S["drumsOut"]):
    for q in (0, 2): put(kick, k1, tb(b) + q * BT); events += 1
    if b >= S["snareIn"]:
        for q in (1, 3): put(sn, snare1(), tb(b) + q * BT); events += 1
for b0 in range(S["drumsIn"], S["drumsOut"], BP):
    c = (b0 // BP) % NCH; L = int(BP * BL * SR); f = hz(CH["bass"][c] - 12); tt_ = np.arange(L) / SR
    y = (np.sin(2 * np.pi * f * tt_) + 0.3 * np.sin(4 * np.pi * f * tt_)) * np.minimum(tt_ / 0.03, 1) * np.minimum((BP * BL - tt_) / 0.05, 1)
    put(bass, y, tb(b0)); events += 1
kenv = sm(sm(np.abs(kick), 3), 120); kenv /= kenv.max() + 1e-9
bass *= 1 - (1 - 10 ** (-LV["bassDuckDb"] / 20)) * np.clip(kenv * 2.5, 0, 1)
snS = pan2(sn, 0.05); snS = nm(snS) * 0.6 + nm(verb(snS, 2.6, 37, 5000.0, 1.8)) * 0.5
duck = lambda d: (1 - (1 - 10 ** (-d / 20)) * np.clip(kenv * 2.5, 0, 1))[:, None]
if os.environ.get("DBG"):
    def spk(x):
        x = x.mean(1) if x.ndim == 2 else x; he = np.abs(bw("high", 8000, x, 4)); return int(np.sum(he > 8 * (sm(he, 50) + 1e-9)))
    def cen(x):
        x = x.mean(1) if x.ndim == 2 else x; f, tt_, Z = sg.stft(x, SR, nperseg=4800); P_ = np.abs(Z) ** 2; c_ = (P_ * f[:, None]).sum(0) / (P_.sum(0) + 1e-12); return round(float(np.std(np.log2(c_[50:-50] + 1))), 2)
    def hfp(x):
        x = x.mean(1) if x.ndim == 2 else x; return round(20 * np.log10(np.max(np.abs(bw("high", 8000, x, 4))) / (np.max(np.abs(x)) + 1e-12) + 1e-12), 1)
    for nmx, x in (("padM", padM), ("bass", bass), ("music", music), ("kick", kick)): print("hfpeak", nmx, hfp(x))
    for nmx, x in (("padS", padS), ("texM", texM), ("melS", melS), ("music", music), ("kick", kick), ("snare", snS)): print(nmx, spk(x), cen(x))
mix = music * duck(1.5) + pan2(nm(bass) * LV["bass"], 0) / np.sqrt(2) + pan2(nm(kick) * LV["kick"], 0) / np.sqrt(2) + snS * LV["snare"]
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
res["events"] = events; res["lengthSec"] = round(T, 2); res["lufs"] = round(meter.integrated_loudness(mix), 2); res["drumsInSec"] = round(tb(S["drumsIn"]), 2)
side = 0.5 * (mix[:, 0] - mix[:, 1]); mid = 0.5 * (mix[:, 0] + mix[:, 1]); db = lambda x: 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)
hf = bw("high", 8000, mid, 4); he = np.abs(hf); spikes = int(np.sum(he > 8 * (sm(he, 50) + 1e-9)))
ed = sm(he, 5)[::480]; fq, Pw = sg.welch(ed - ed.mean(), fs=100, nperseg=1024)
sec = lambda b0, b1: mix[int(tb(b0) * SR):int(tb(b1) * SR)]
res["checks"] = {"width": widthlog, "side_below_120Hz_db": round(db(bw("low", 120, side, 4)) - db(bw("low", 120, mid, 4)), 1), "hf_spikes_over_8x": spikes,
  "hf_env_12_40_vs_0_12_db": round(10 * np.log10(Pw[(fq >= 12) & (fq <= 40)].mean() / Pw[(fq > 0.2) & (fq < 12)].mean()), 1),
  "lufs_intro_A_B_C_outro": [round(meter.integrated_loudness(sec(a, b)), 1) for a, b in ((0, 4), (4, 12), (12, 22), (22, 26), (26, 30))]}
json.dump(res, open(OUT + ".stats.json", "w"), indent=1, default=float)
print(json.dumps({"score": res["score"], "pass": res["pass"], "lufs": res["lufs"], "tp": res["extra"].get("true_peak_dbtp"), "gates": res["gates"], "subs": res["subs"], "tilt": res["extra"].get("tilt_db_oct"), "gr": round(gr_max, 2), "len": res["lengthSec"], "drumsIn": res["drumsInSec"], "checks": res["checks"]}, default=float))
