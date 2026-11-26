#!/usr/bin/env python3
"""Daily 3-skill test 2026-11-26 "Borrowed Light" (D minor, 96 BPM): cinematic cue form intro-from-A/A1/A1prime/B/A2 (Fj3jwdLBD60) + ambient melody tricks vector/sequence/modal slip (liS9PQyHSa4) + 3-band wavetable pad rack (RPzAJFC_JkI). usage: render.py recipe.json out.wav"""
import sys, os, json, numpy as np, soundfile as sf, pyloudnorm as pyln
from scipy import signal as sg
from scipy.signal import lfilter
LAB = os.environ.get("LAB", "/workspace/skill-library/sample-lab"); sys.path.insert(0, LAB + "/engine")
import dsp, metrics
SR = 48000
R = json.load(open(sys.argv[1])); OUT = sys.argv[2]; rng = np.random.default_rng(R["seed"])
NB = R["bars"]; BL = 240 / R["bpm"]; BT = BL / 4; tb = lambda x: x * BL
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
def gate(b0, b1, xf_ms=30): return sm(sm(((bar >= b0) & (bar < b1)).astype(float), xf_ms / 2), xf_ms / 2)
def fade(y, ms=8):
    k = min(int(ms / 1000 * SR), len(y) // 2); y[-k:] *= np.cos(np.linspace(0, np.pi / 2, k)) ** 2; return y
def blep(p, dt):
    out = np.zeros_like(p); a = p < dt; x = p[a] / dt[a]; out[a] = x + x - x * x - 1
    b = p > 1 - dt; x = (p[b] - 1) / dt[b]; out[b] = x * x + x + x + 1; return out
def saw_osc(f, ph0=0.0):
    dt = f / SR; ph = (ph0 + np.cumsum(dt)) % 1.0; return 2 * ph - 1 - blep(ph, dt)
st = lambda b, s16: tb(b) + s16 * BT / 4
events = 0; SEC = R["sections"]; LV = R["levels"]
def sec_of(b):
    for s in SEC:
        if s["b"][0] <= b < s["b"][1]: return s
    return None
on = lambda name, b: (sec_of(b) is not None) and name in sec_of(b)["els"]
def chord_at(b):
    for c in R["chords"]:
        if c[0] <= b < c[1]: return c
    return R["chords"][-1]
CH = R["chords"]; P = R["pad"]
def elgate(name, xf_ms=60):
    g = np.zeros(N)
    for s in SEC:
        if name in s["els"]: g[int(tb(s["b"][0]) * SR):int(tb(s["b"][1]) * SR)] = 1
    return sm(sm(g, xf_ms / 2), xf_ms / 2)
def autom(lst, ms=400):
    a = np.zeros(N)
    for b0, b1, v in lst: a[int(tb(b0) * SR):min(int(tb(b1) * SR), N)] = v
    a[int(tb(lst[-1][1]) * SR):] = lst[-1][2]; return sm(sm(a, ms / 2), ms / 2)
def svf_lp(x, fc):
    fc = C(np.clip(fc, 30, 20000)); return np.stack([dsp.svf(C(x[:, c]), fc, 0.75, 0, SR) for c in range(2)], 1) if x.ndim == 2 else dsp.svf(C(x), fc, 0.75, 0, SR)
counts = {}
# ================= WT (RPzAJFC_JkI): 3-band wavetable rack; osc1/osc2 position = +LFO1 -LFO2 / opposite; retrigger off (global LFOs)
macro = autom(P["macro"], 2000)
def wt_band(cfg, tones_fn, tabA, tabB, uni, spreadPan):
    l1 = np.sin(2 * np.pi * cfg["lfo"][0] * t); l2 = np.sin(2 * np.pi * cfg["lfo"][1] * t + 1.3)
    pos1 = np.clip(0.5 + cfg["amt"] * (l1 - l2), 0, 1); pos2 = np.clip(0.5 - cfg["amt"] * (l1 - l2), 0, 1)
    out = np.zeros((N, 2)); global events
    for b0, b1, nmz, tones, root in CH:
        s0 = tb(b0); held = tb(b1) - s0; i0 = int(s0 * SR); i1 = min(int((tb(b1) + P["rel"] * 2.5) * SR), N); tt = t[i0:i1] - s0
        env = (1 - np.exp(-tt / (P["atk"] / 3))) * np.where(tt < held, 1.0, np.exp(-(tt - held) / (P["rel"] / 3)))
        for m in tones_fn(tones, root):
            for k, c in enumerate(uni):
                f = np.full(i1 - i0, hz(m) * 2 ** (c / 1200)); ph0 = rng.uniform()
                ph = (ph0 + np.cumsum(f / SR)) % 1.0
                o1 = (1 - pos1[i0:i1]) * tabA(ph, f) + pos1[i0:i1] * tabB(ph, f)
                f2 = f * 2 ** (cfg.get("det", 0) / 1200); ph2 = (rng.uniform() + np.cumsum(f2 / SR)) % 1.0
                o2 = (1 - pos2[i0:i1]) * tabB(ph2, f2) + pos2[i0:i1] * sq(ph2, f2)
                p = spreadPan * (2 * k / max(len(uni) - 1, 1) - 1) if len(uni) > 1 else 0
                out[i0:i1] += pan2((o1 * 0.55 + o2 * 0.45) * env / len(uni), p); events += 1
    return out
def warm(ph, f): return np.sin(2 * np.pi * ph) + 0.3 * np.sin(4 * np.pi * ph) + 0.12 * np.sin(6 * np.pi * ph)
def saw(ph, f): return 2 * ph - 1 - blep(ph, f / SR)
def sq(ph, f): return 0.5 * (saw(ph, f) - saw((ph + 0.5) % 1.0, f))
M_ = P["mids"]; H_ = P["highs"]; L_ = P["lows"]
mids = wt_band(M_, lambda tn, r: tn, warm, saw, M_["uni"], 0.5)
lastc = np.zeros(N)
for b0, b1, *_ in CH: lastc[int(tb(b0) * SR):] = tb(b0)
fenv = sm(np.exp(-(t - lastc) / 2.0), 80)
lm = 0.5 + 0.5 * np.sin(2 * np.pi * M_["lfo"][0] * t) * 0.5 - 0.25 * np.sin(2 * np.pi * M_["lfo"][1] * t)
fcM = M_["lp"][0] * (M_["lp"][1] / M_["lp"][0]) ** np.clip(macro * 0.8 + M_["envAmt"] * fenv + 0.12 * (lm - 0.5), 0, 1.2)
drv = 1 + 1.5 * macro
mids = np.tanh(svf_lp(mids, fcM) * drv[:, None]) / np.tanh(drv)[:, None]; mids = bw("high", M_["hp"], mids, 2)
highs = wt_band(H_, lambda tn, r: [x + 12 for x in tn[1:]], saw, sq, H_["uni"], 0.85)
highs = np.tanh(bw("low", H_["lp"], highs, 2) * 1.3); highs = bw("high", H_["hp"], highs, 2)
lows = np.zeros(N)
for b0, b1, nmz, tones, root in CH:
    s0 = tb(b0); held = tb(b1) - s0; i0 = int(s0 * SR); i1 = min(int((tb(b1) + P["rel"] * 2.5) * SR), N); tt = t[i0:i1] - s0
    env = (1 - np.exp(-tt / (P["atk"] / 3))) * np.where(tt < held, 1.0, np.exp(-(tt - held) / (P["rel"] / 3)))
    f = np.full(i1 - i0, hz(min(tones) - 12)); lows[i0:i1] += saw((rng.uniform() + np.cumsum(f / SR)) % 1, f) * env
fcL = L_["lp"] * (1 + 0.15 * np.sin(2 * np.pi * L_["lfo"] * t))
lows = bw("high", L_["hp"], svf_lp(lows, fcL), 4)
lows = np.stack([lows, lows], 1)
Mx = P["mix"]; pad = nm(lows) * Mx["lows"] + nm(mids) * Mx["mids"] + nm(highs) * Mx["highs"]
pad[:, :] *= (1 - 0.4 * elgate("bass", 2000))[:, None] ** 0 # keep
# FX chain: glue comp 4:1 -> 100% wet vintage verb -> soft clip -> long verb 50% -> limiter catching ~2.5 dB
e = sm(np.sqrt(sm(pad.mean(1) ** 2, 30)), 50); thr = np.percentile(e, 90)
gr = np.where(e > thr, (e / thr) ** (1 / P["comp"]["ratio"] - 1), 1.0); pad = pad * gr[:, None]
pad = nm(verb(pad, P["verb1"]["rt"], 11, P["verb1"]["damp"], 1.4)); pad = np.tanh(pad * P["sat"]) / np.tanh(P["sat"])
pad = nm(pad * (1 - P["verb2"]["mix"]) + nm(verb(pad, P["verb2"]["rt"], 12, 8000.0, 2.4)) * P["verb2"]["mix"])
pk = sm(np.abs(pad).max(1), 2); lim = np.minimum(1, 10 ** (-P["limDb"] / 20) / (pk + 1e-9)); pad = nm(pad * sm(lim, 20)[:, None])
# ================= CUE (Fj3jwdLBD60) voices
def tone(m, dur, kind, atk=0.008):
    Ln = int((dur + 1.5) * SR); tt = np.arange(Ln) / SR; f = np.full(Ln, hz(m)); ph = (np.cumsum(f / SR)) % 1.0
    if kind == "piano":
        y = np.sin(2 * np.pi * ph) + 0.35 * np.sin(4 * np.pi * ph) * np.exp(-tt / 0.4) + 0.12 * np.sin(6 * np.pi * ph) * np.exp(-tt / 0.2)
        e = np.minimum(tt / atk, 1) * np.exp(-tt / 1.1) * np.where(tt < dur, 1, np.exp(-(tt - dur) / 0.3))
    else:   # bowed strings / horn / cello: saw, slow attack, LP
        y = saw(ph, f) * 0.6 + saw((ph * 1.0 + 0.37) % 1, f * 1.002) * 0.4
        e = np.minimum(tt / atk, 1) * np.where(tt < dur, 1, np.exp(-(tt - dur) / 0.35))
    return fade(y * e, 40)
def line(evts, kind, lp, atk, tr=0):
    global events; y = np.zeros(N)
    for b, s16, m, l16 in evts:
        s0 = st(b, s16); put(y, tone(m + tr, l16 * BT / 4 * 0.95, kind, atk), s0); events += 1
        k = sec_of(s0 / BL)["name"].split(":")[0]; counts[k] = counts.get(k, 0) + 1
    return nm(bw("low", lp, y, 2))
mel = line(R["mel"], "piano", 7000, 0.006)
vio = line(R["vio"], "str", 6000, 0.09)
seqB = line(R["seqB"], "str", 5000, 0.12)
a2 = nm(line(R["a2"], "piano", 7000, 0.006) + 0.6 * line(R["a2"], "str", 5500, 0.06, 12))   # octaves
horn = line(R["horn"], "str", 1800, 0.12)
vec = line(R["vec"], "piano", 7000, 0.006)
cello = line(R["cello"], "str", 1300, 0.25)
pedal = line([[b, s, R["pedal"]["midi"], 4] for b in range(*R["pedal"]["bars"]) for s in (0, 8)], "piano", 8000, 0.006)
# ostinato: chord tones around middle C avoiding melody pitches, 8ths (pitched, soft attack, no ticks); fades in bars 6-8
O = R["ost"]; ost = np.zeros(N)
for b0, b1, nmz, tones, root in CH:
    pool = sorted({(x - O["lo"]) % 12 + O["lo"] for x in tones})
    for bb in range(b0, b1):
        for i, ai in enumerate(O["pat"]):
            s0 = st(bb, i * 2)
            if not on("ost", s0 / BL + 1e-6): continue
            m = pool[ai % len(pool)]; Ln = int(0.8 * SR); tt = np.arange(Ln) / SR; f = np.full(Ln, hz(m)); ph = np.cumsum(f / SR) % 1
            y = saw(ph, f) * np.minimum(tt / O["atk"], 1) * np.exp(-tt / O["decay"]); put(ost, fade(y, 30), s0); events += 1
ost = nm(bw("low", O["lp"], ost, 2)); ostg = elgate("ost", 200) * np.where(bar < 8, np.clip((bar - 6) / 2, 0, 1) ** 1.5, 1)
# horn crescendo into A1 + low brass chords in A1'
hs = np.zeros(N); br = np.zeros(N)
for b0, b1, nmz, tones, root in CH:
    for x in (root + 12, root + 19, root + 24):
        if b0 >= 6 and b1 <= 8: put(hs, tone(x, tb(b1) - tb(b0), "str", 0.4), tb(b0))
        if 16 <= b0 < 20: put(br, tone(x, tb(b1) - tb(b0) - 0.05, "str", 0.08), tb(b0))
cres = np.clip((bar - 6) / 2, 0, 1) ** 2 * (bar < 8.05); fcH = 500 + 2200 * cres
hs = nm(svf_lp(hs, fcH)) * cres; br = nm(bw("low", 1500, br, 2))
# pitched metallic hit -> 100% into very long floating reverb (only wet heard)
MT = R["metal"]; mt = np.zeros(N)
for b in MT["bars"]:
    Ln = int(2 * SR); tt = np.arange(Ln) / SR
    y = sum(a * np.sin(2 * np.pi * MT["base"] * r * tt) * np.exp(-tt / d) for r, a, d in ((1, 1, .8), (2.76, .6, .5), (5.4, .35, .3), (8.93, .2, .2)))
    put(mt, fade(y * np.minimum(tt / 0.003, 1), 50), tb(b))
metal = nm(verb(np.stack([mt, mt], 1), MT["rt"], 77, 9000.0, 2.6, 0.3))
# boom + soft low drum pulse (kick, steady), A2 toms + snare in second half, tam-tam punctuation
def boom1():
    Ln = int(2.5 * SR); tt = np.arange(Ln) / SR; f = 32 + 28 * np.exp(-tt / 0.15)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.9) + 0.15 * bw("low", 300, np.random.default_rng(3).standard_normal(Ln), 2) * np.exp(-tt / 0.25)
    return fade(y * np.minimum(tt / 0.004, 1), 200)
boom = np.zeros(N)
for b in (4, 8, 26): put(boom, boom1(), tb(b))
# ================= KK: 4-layer acoustic-style kick (sine body + pitch env, offset-phase transient, faded-in HP'd 'acoustic sample', pink noise tail), EQ + fast comp
KK = R["kick"]
def kick1(v=1.0):
    Ln = int(0.6 * SR); tt = np.arange(Ln) / SR
    f = KK["bodyHz"] * 2 ** (KK["bodyStartSt"] / 12 * np.exp(-tt / (KK["pitchTauMs"] / 1000)))
    body = np.sin(2 * np.pi * np.cumsum(f) / SR + np.pi / 2) * np.exp(-tt / KK["bodyDecay"])         # phase 90
    ft = KK["transHz"] * 2 ** (np.exp(-tt / 0.002))
    tr = np.sin(2 * np.pi * np.cumsum(ft) / SR + np.deg2rad(KK["transPhaseDeg"])) * np.exp(-tt / (KK["transMs"] / 1000)) * 0.25
    sh = sum(np.sin(2 * np.pi * fm * tt) * np.exp(-tt / dc) for fm, dc in ((172, 0.09), (268, 0.06), (395, 0.04)))
    sh += 0.3 * bw("band", [250, 1800], np.random.default_rng(5).standard_normal(Ln), 2) * np.exp(-tt / 0.03)   # 'acoustic one-shot' stand-in, fixed seed
    sh = bw("high", KK["shellHp"], sh * np.clip(tt / (KK["shellFadeInMs"] / 1000), 0, 1), 2) * KK["shellGain"]
    pk = np.random.default_rng(9).standard_normal(Ln); pk = lfilter([0.049922, -0.095993, 0.050612, -0.004408], [1, -2.494956, 2.017265, -0.522189], pk)
    tail = pk / (np.abs(pk).max() + 1e-9) * np.exp(-tt / KK["noiseDecay"]) * KK["noiseGain"] * np.clip(tt / 0.003, 0, 1)
    y = body + tr + sh + tail
    y = y + (10 ** (KK["lowShelfDb"] / 20) - 1) * bw("low", 90, y, 2) + (10 ** (KK["midDb"] / 20) - 1) * bw("band", [2000, 6000], y, 2)
    env = sm(np.abs(y), 1.0); gr = np.minimum(1, (0.35 / (env + 1e-9)) ** KK["compAmt"]); y = y * sm(gr, 0.3)   # fast-attack comp, ~half amount
    y = y * np.minimum(tt / 0.0008, 1); return fade(y / np.abs(y).max(), 80) * v
k1 = kick1(); kick = np.zeros(N)
for b in range(NB):
    for s16 in KK["steps"]:
        s0 = st(b, s16)
        if on("kick", s0 / BL + 1e-6): put(kick, k1 * (1.0 if s16 == 0 else 0.85), s0); events += 1
perc = np.zeros((N, 2))
def snare1():
    Ln = int(0.5 * SR); tt = np.arange(Ln) / SR
    y = 0.6 * np.sin(2 * np.pi * 190 * tt) * np.exp(-tt / 0.06) + bw("band", [300, 4500], np.random.default_rng(8).standard_normal(Ln), 2) * np.exp(-tt / 0.11) * 0.5
    return fade(y * np.minimum(tt / 0.004, 1), 60)
def tom1():
    Ln = int(0.8 * SR); tt = np.arange(Ln) / SR; f = 80 + 40 * np.exp(-tt / 0.05)
    return fade(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.3) * np.minimum(tt / 0.003, 1), 80)
sn, tm = snare1(), tom1(); pm = np.zeros(N); ps = np.zeros(N)
for b in range(26, 30):
    put(pm, tm, st(b, 12), 0.8); put(pm, tm, st(b, 14), 0.6); events += 2
    if b >= 28: put(ps, sn, st(b, 4)); put(ps, sn, st(b, 12)); events += 2
Ln = int(5 * SR); tt = np.arange(Ln) / SR
tam = sum(np.sin(2 * np.pi * f0 * tt + i) / (1 + i * 0.3) for i, f0 in enumerate((211, 287, 359, 431, 517, 643, 811, 977, 1213)))
tam = tam * (1 - np.exp(-tt / 0.25)) * np.exp(-tt / 1.8); tm2 = np.zeros(N); put(tm2, fade(tam, 300), tb(26) - 0.3)
perc = pan2(nm(pm), 0) + pan2(nm(ps), 0.0) * 0.6 + nm(verb(np.stack([tm2, tm2], 1), 4.0, 55, 8000.0, 2.0) + 0.4 * pan2(tm2, 0)) * 0.7
# bass: root steady 8th pulse (A sections), offbeat common-tone A in B; mono saw + sine sub
bs = np.zeros(N); fsub = np.zeros(N)
for b0, b1, nmz, tones, root in CH:
    fsub[int(tb(b0) * SR):int(tb(b1) * SR) if b1 < NB else N] = hz(root)
    for bb in range(b0, b1):
        steps = [2, 6, 10, 14] if 20 <= bb < 26 else [0, 2, 4, 6, 8, 10, 12, 14]
        for s16 in steps:
            s0 = st(bb, s16)
            if not on("bass", s0 / BL + 1e-6): continue
            Ln = int(0.4 * SR); tt = np.arange(Ln) / SR; f = np.full(Ln, hz(root)); ph = np.cumsum(f / SR) % 1
            y = (saw(ph, f) * 0.6 + saw((ph + 0.21) % 1, f * 1.003) * 0.4) * np.minimum(tt / 0.005, 1) * (0.35 + 0.65 * np.exp(-tt / 0.12))
            put(bs, fade(y, 30), s0, 1.0 if s16 % 4 == 0 else 0.8); events += 1
bs = nm(np.tanh(bw("low", 480, bs, 2) * 1.3)); sub = np.sin(2 * np.pi * np.cumsum(sm(fsub, 3)) / SR) * sm(np.abs(bs), 15) / (sm(np.abs(bs), 15).max() + 1e-9)
bassOn = elgate("bass", 80)
# ================= mix
LV = R["levels"]
kenv = sm(sm(np.abs(kick), 3), 120); kenv /= kenv.max() + 1e-9
bduck = 1 - (1 - 10 ** (-LV["bassDuckDb"] / 20)) * np.clip(kenv * 2.5, 0, 1)
G = lambda n, ms=300: elgate(n, ms)[:, None]
fg = (pan2(mel, 0.05) * LV["mel"] * G("mel") + pan2(vio, -0.1) * LV["vio"] * G("vio") + pan2(seqB, -0.05) * LV["seqB"] * G("seqB")
      + pan2(a2, 0.0) * LV["mel"] * G("a2") + pan2(horn, 0.3) * LV["horn"] * G("horn") + pan2(vec, 0.05) * LV["vec"] * G("vec")
      + pan2(cello, -0.2) * LV["cello"] * G("cello") + pan2(pedal, 0.35) * LV["pedal"] * G("pedal")
      + pan2(ost, -0.3) * LV["ost"] * ostg[:, None] + pan2(hs, 0.25) * LV["brass"] + pan2(br, -0.15) * LV["brass"] * G("brass"))
bg = pad * LV["pad"] + metal * LV["metal"] + perc * LV["perc"] * G("perc", 100)
vb = verb(C(fg * 0.6), 4.0, 41, 7000.0, 2.0)
mix = bg + fg + nm(vb) * LV["verb"]
mix += pan2((bs * LV["bass"] + sub * LV["sub"]) * bassOn * bduck + nm(kick) * LV["kick"] + nm(boom) * LV["boom"], 0) / np.sqrt(2)
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
res["events"] = events; res["lengthSec"] = round(T, 2); res["lufs"] = round(meter.integrated_loudness(mix), 2); res["drumsInSec"] = round(tb(R["drumsIn"]), 2)
side = 0.5 * (mix[:, 0] - mix[:, 1]); mid = 0.5 * (mix[:, 0] + mix[:, 1]); db = lambda x: 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)
hf = bw("high", 8000, mid, 4); he = np.abs(hf); spikes = int(np.sum(he > 8 * (sm(he, 50) + 1e-9)))
def cent(x):
    f_, tt_, Z = sg.stft(x.mean(1), SR, nperseg=4800); P_ = np.abs(Z) ** 2; c_ = (P_ * f_[:, None]).sum(0) / (P_.sum(0) + 1e-12); return float(np.median(c_))
blocks = [s["b"] for s in SEC]; sec = lambda b0, b1: mix[int(tb(b0) * SR):int(tb(b1) * SR)]
cents = [cent(sec(a, b)) for a, b in blocks]
res["checks"] = {"side_below_120Hz_db": round(db(bw("low", 120, side, 4)) - db(bw("low", 120, mid, 4)), 1), "hf_spikes_over_8x": spikes,
  "section_lufs": [round(meter.integrated_loudness(sec(a, b)), 1) if b - a >= 2 else None for a, b in blocks], "section_centroid_hz": [round(c) for c in cents],
  "centroid_span_oct": round(float(np.log2(max(cents) / min(cents))), 2), "lead_notes_per_section": counts}
json.dump(res, open(OUT + ".stats.json", "w"), indent=1, default=float)
print(json.dumps({"score": res["score"], "pass": res["pass"], "lufs": res["lufs"], "tp": res["extra"].get("true_peak_dbtp"), "gates": res["gates"], "subs": res["subs"], "tilt": res["extra"].get("tilt_db_oct"), "gr": round(gr_max, 2), "len": res["lengthSec"], "drumsIn": res["drumsInSec"], "checks": res["checks"]}, default=float))
