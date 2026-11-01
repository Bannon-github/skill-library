#!/usr/bin/env python3
"""Daily 3-skill test 2026-11-01 "Glimpses": hidden-context synth strings (source) + future-garage ambient drum groove
(drums) + four levels of loop-to-story arrangement (structure). usage: render.py recipe.json out.wav"""
import sys, os, json, numpy as np, soundfile as sf, pyloudnorm as pyln
from scipy import signal as sg
LAB = os.environ.get("LAB", "/workspace/skill-library/sample-lab"); sys.path.insert(0, LAB + "/engine")
import dsp, metrics
SR = 48000
R = json.load(open(sys.argv[1])); OUT = sys.argv[2]; rng = np.random.default_rng(R["seed"])
NB = R["bars"]; BL = 240 / R["bpm"]; tb = lambda x: x * BL; S = R["sections"]
T = NB * BL + R["tailSec"]; N = int(T * SR); t = np.arange(N) / SR
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
def flt(k, f, x, o=2): return sg.sosfilt(sg.butter(o, f, k, fs=SR, output="sos"), x, axis=0)
def pan2(x, p): return np.stack([x * np.cos((p + 1) * np.pi / 4), x * np.sin((p + 1) * np.pi / 4)], 1) * np.sqrt(2)
def put(buf, y, s, g=1.0):
    i = int(round(s * SR)); L = min(len(y), N - i)
    if L > 0 and i >= 0: buf[i:i + L] += y[:L] * g
def verb(x, rt, seed, damp=10000.0, size=1.6, mod=0.25, diff=0.75):
    l, r = dsp.fdn_reverb(np.ascontiguousarray(x[:, 0]), np.ascontiguousarray(x[:, 1]), SR, float(rt), size, damp, 0.03, mod, diff, 0.0, seed); return np.stack([l, r], 1)
def sm(x, ms=30): n = max(int(ms * SR / 1000), 1); return sg.filtfilt(np.ones(n) / n, [1], x)
def fade(y, ms=10, mi=0.0):
    n = int(ms * SR / 1000); y[-n:] *= np.linspace(1, 0, n)
    if mi: m = int(mi * SR / 1000); y[:m] *= np.linspace(0, 1, m)
    return y
lane = lambda pts: np.interp(t, [tb(p[0]) for p in pts], [p[1] for p in pts])
chord = lambda b: R["chords"][int(b) % 4]
nm = lambda x: x / (np.max(np.abs(x)) + 1e-9)
st2 = lambda f, x: np.stack([f(np.ascontiguousarray(x[:, c]), c) for c in range(2)], 1)
events = 0
# ===== SKILL C level 4 (additive) + step 7 support: soft chord stack from silence, big reverb, GATED tails, fader dip
K = R["stack"]; stack = np.zeros((N, 2)); sub = np.zeros(N); gate = np.zeros(N)
for b in range(0, NB):
    root, notes = chord(b); dur = BL * 0.9; L = int(dur * SR); tt = np.arange(L) / SR
    env = np.clip(tt / 0.6, 0, 1) * np.clip((dur - tt) / 0.3, 0, 1) * (1 - K["dip"] * np.clip(tt / BL * 2, 0, 1))  # starts large, smooths out
    for j, m in enumerate(notes + [notes[0] - 12]):
        y = (np.sin(2*np.pi*hz(m)*tt + rng.random()*6) + 0.3*np.sin(4*np.pi*hz(m)*tt) + 0.12*np.sin(6*np.pi*hz(m)*tt)) * env
        put(stack, pan2(y, (j - 1.5) * 0.35), tb(b))
    put(sub, np.sin(2*np.pi*hz(root)*tt) * env, tb(b)); put(gate, np.ones(L), tb(b)); events += 1
g = sg.lfilter([1 - np.exp(-1/(K["gateRel"]*SR))], [1, -np.exp(-1/(K["gateRel"]*SR))], gate)   # gate release so tails stop with chord
stack = stack + K["verbMix"] * verb(flt("high", 150, stack), K["verbRt"], 2) * np.clip(g * 1.4, 0, 1)[:, None]
stack = st2(lambda x, c: dsp.eq(x, "highshelf", 3000, 0.7, K["bright"]), stack)
# ===== SKILL A: two opposite-direction half-speed arps of saw plucks, brassy filter env, vibrato, phaser above fundamental
Q = R["strings"]; v = {k: np.zeros((N, 2)) for k in ("v1", "v2")}; v2oct = np.zeros((N, 2)); step = BL / 8   # 16th x2 = 8th steps
def pluck(m, V, dur):
    L = int(dur * SR); tt = np.arange(L) / SR
    vib = 1 + (2 ** (Q["vibCents"] / 1200) - 1) * np.sin(2*np.pi*Q["vibHz"]*tt) * np.clip((tt - Q["vibDelay"]) / 0.1, 0, 1)
    y = np.zeros(L)
    for k in range(V["unison"]):
        c = (k - (V["unison"] - 1) / 2) / max((V["unison"] - 1) / 2, 1) * V["detune"]
        y += dsp.osc_va(hz(m) * 2 ** (c / 1200) * vib, 0, 0.5, rng.random(), SR) / V["unison"]
    fc = V["fcBase"] + (V["fcPeak"] - V["fcBase"]) * np.clip(tt / 0.008, 0, 1) * np.exp(-tt / V["decay"])   # opens fast, decays
    y = dsp.svf(y, np.clip(fc, 80, 16000), 0.8, 0, SR) * np.clip(tt / 0.004, 0, 1) * np.exp(-tt / (V["decay"] * 2.2))
    return fade(y, 20)
for b in range(S["glimpse"] - 1, S["end"] - 1):
    root, notes = chord(b)
    for name in ("v1", "v2"):
        V = Q[name]; seq = notes if V["dir"] == "up" else notes[::-1]
        for k in range(8):
            m = seq[k % 3] + V["oct"]; put(v[name], pan2(pluck(m, V, step * (1.6 if name == "v1" else 3.0)), -0.35 if name == "v1" else 0.35), tb(b) + k * step); events += 1
arp = v["v1"] + 0.8 * v["v2"]
lo = flt("low", Q["phaserSplitHz"], arp, 4); hi = arp - lo                        # step 3: phase only partials above the fundamental
hi = st2(lambda x, c: dsp.phaser(x, Q["phaserRate"], 0.8, 0.3, 6, Q["phaserMix"], c * np.pi / 2, SR), hi)
arp = lo + hi
send = st2(lambda x, c: dsp.eq(x, "highshelf", 4000, 0.7, Q["preShelfDb"]), flt("high", Q["preHp"], arp))   # step 5: HP + lift before verb
shim = st2(lambda x, c: dsp.pitch_shift_delay(x, SR, Q["shimmerSemis"], 0.12, Q["shimmerFb"], 150.0, 6000.0, 0.08), send)
wet = verb(send + 0.5 * shim, Q["verbRt"], 7, 9000.0, Q["verbSize"], Q["verbMod"], Q["verbDiff"])
arp = nm(arp) + Q["verbMix"] * nm(wet)
protag = np.clip(sm(lane(Q["lane"]), 80), 0, 1)                                  # step 6 + Skill C level 3: performed level lane
arp *= protag[:, None]
# ===== SKILL B: future-garage drum groove (halftime kick+rim, base hat, swung accents, flair+reverse, foley chops)
D = R["drums"]; kick = np.zeros((N, 2)); rim = np.zeros((N, 2)); hats = np.zeros((N, 2)); foley = np.zeros((N, 2)); key = np.zeros(N)
def kickS(v):
    L = int(0.5 * SR); tt = np.arange(L) / SR; f = 48 * 2 ** (2.2 * np.exp(-tt / 0.03))
    return fade(np.tanh(1.4 * np.sin(2*np.pi*np.cumsum(f)/SR)) * np.exp(-tt / 0.22) * np.clip(tt / 0.0015, 0, 1) * v, 20)
def rimS(v):
    L = int(0.25 * SR); tt = np.arange(L) / SR
    y = 0.6 * np.sin(2*np.pi*1700*tt) * np.exp(-tt / 0.012) + 0.6 * flt("band", [1000, 5000], rng.standard_normal(L)) * np.exp(-tt / 0.03)
    return fade(y * np.clip(tt / 0.0008, 0, 1) * v, 10)
HAT = flt("high", 7000, rng.standard_normal(int(0.12 * SR))) * np.exp(-np.arange(int(0.12 * SR)) / SR / 0.03)
HAT = fade(HAT * np.clip(np.arange(len(HAT)) / SR / 0.0008, 0, 1), 10)
def chop(v):  # foley crunch: faded click (paper/silverware stand-in, synthesized)
    L = int(rng.uniform(0.02, 0.05) * SR); f0 = rng.uniform(2500, 7000)
    return fade(flt("band", [f0 * 0.7, min(f0 * 1.4, 20000)], rng.standard_normal(L)) * np.exp(-np.arange(L) / SR / 0.01) * v, 5, 2)
def knock(v):  # transient-heavy mid knock ("celery snap" stand-in)
    L = int(0.06 * SR); tt = np.arange(L) / SR
    return fade((flt("band", [1800, 4000], rng.standard_normal(L)) + 0.8 * np.sin(2*np.pi*420*tt)) * np.exp(-tt / 0.008) * v, 5, 0.5)
jit = lambda: rng.uniform(-1, 1) * D["jitterMs"] / 1000
for b in range(S["drumsIn"], S["drumsOut"]):
    s0 = tb(b); var = (b // 2) % 2; full = b < S["outro"]
    kpos = [] if S["dip"] <= b < S["peak"] or not full else ([0, 0.6875] if var else [0, 0.625])
    if b == S["turn2"]: kpos = [0]
    for p in kpos: put(kick, pan2(kickS(1.0 if p == 0 else 0.7), 0), s0 + p * BL); put(key, np.ones(int(0.05*SR)), s0 + p * BL); events += 1
    for p, vv in ((0.5, 1.0),) + (((0.9375, 0.45),) if var and full else ()):   # main rim on 3 (halftime two-step)
        put(rim, pan2(rimS(vv), 0.05), s0 + p * BL); put(key, 0.6 * np.ones(int(0.05*SR)), s0 + p * BL); events += 1
    for k in range(4): put(hats, pan2(HAT * 0.8, 0.15), s0 + (k + 0.5) / 4 * BL)              # base hat on every 'and'
    if b >= S["glimpse"] and full:
        for lay, pos in enumerate(((5, 7, 11, 13, 15), (3, 9, 14))):
            for p16 in pos:
                if b % 4 == 3 and p16 > 8 and lay == 0: continue                                # vary every 4 bars: stop a layer briefly
                sw = (D["swingMs"] / 1000) if p16 % 2 == 1 and rng.random() < 0.6 else 0
                put(hats, pan2(HAT * rng.uniform(0.6, 1.0) * D["accHat"] / D["baseHat"] * 0.5, -0.3 + 0.6 * lay), s0 + p16 / 16 * BL + sw + jit()); events += 1
        for p16 in (6, 10) if var else (7,):                                                     # accent rims, hand-swung
            put(rim, pan2(rimS(0.35), -0.2), s0 + p16 / 16 * BL + jit())
    if b >= S["peak"] and full:
        for p16, vv in ((2, 0.9), (3, 0.5), (12, 0.7)): put(hats, pan2(HAT * vv * D["flair"] / D["baseHat"] * 0.6, 0.4), s0 + p16 / 16 * BL)   # flair hats, velocity bounce
        if b % 2 == 1: put(hats, pan2(fade(HAT[::-1].copy() * 1.5, 3, 2), -0.4), s0 + BL - len(HAT) / SR)   # reversed copy into the bar line
    if b >= S["glimpse"] - 2:
        put(foley, pan2(chop(1.0), 0), s0 + (0.5 - 1 / 32) * BL)                                  # just before the main rim
        for p16 in (3, 11, 13): put(foley, pan2(chop(rng.uniform(0.5, 1)), 0), s0 + p16 / 16 * BL + (D["swingMs"] / 1000) * 0.7)
        if b >= S["glimpse"]: put(foley, pan2(knock(1.0), 0), s0 + 0.75 * BL + jit())
# processing (steps 6-11)
kick = st2(lambda x, c: dsp.eq(dsp.svf(x, np.full(len(x), D["kickLpHz"]), 0.707 + 2 * D["kickRes"], 0, SR), "peak", D["kickLpHz"], 2, 1.5), kick)
rim = st2(lambda x, c: np.tanh(1.5 * (0.6 * flt("band", [D["rimBpHz"] * 0.7, D["rimBpHz"] * 1.6], x) + 0.4 * flt("high", D["rimBpHz"], x))) / 1.5, rim)
rl, rr = dsp.chorus(np.ascontiguousarray(rim[:, 0]), np.ascontiguousarray(rim[:, 1]), SR, 0, 0.8, 3.0, 12.0, 0.0, 1.0, 0.4, 0.5, 0.98); rim = np.stack([rl, rr], 1)
an = sg.hilbert(hats, axis=0); hats = np.real(an * np.exp(2j * np.pi * D["hatShiftHz"] * t)[:, None])  # frequency shifter down
hats = flt("high", 400, hats)
ph = 2 * np.pi * D["foleyRate"] * t; foley = foley * np.stack([1 + 0.8 * np.sin(ph), 1 - 0.8 * np.sin(ph)], 1) / 1.8   # unsynced auto-pan 6.1 Hz
foley = st2(lambda x, c: dsp.phaser(x, D["foleyRate"], 0.7, 0.2, 4, 0.5, c * np.pi / 2, SR), foley)
hn = (t % (BL / 2)) / (BL / 2); duckH = 1 - D["hatDuck"] * np.exp(-hn * 6)          # half-note volume duck on hat/foley group
hf = (nm(hats) * D["baseHat"] / 0.18 * 0.35 + nm(foley) * D["foley"]) * duckH[:, None]
hold = np.floor(np.arange(N) * 22500 / SR) * SR / 22500; idx = np.clip(np.round(hold).astype(int), 0, N - 1); hf = hf[idx]
hf = np.round(hf * 2047) / 2047; hf = flt("low", 11000, hf)                         # 12-bit / 22.5 kHz sampler on hats
drums = nm(kick) * D["kick"] + nm(rim) * D["rim"] + hf + nm(foley) * 0 
drums = drums / (np.max(np.abs(drums)) + 1e-9)
drums = np.round(drums * 2047) / 2047                                               # drum bus: 12-bit/44.1 -> hard clip -> soft sat (subtle)
cg = 10 ** (D["busClipDb"] / 20); drums = np.clip(drums * cg, -1, 1) / cg
sg_ = 10 ** (D["busSatDb"] / 20); drums = np.tanh(drums * sg_) / np.tanh(sg_)
drums = flt("high", 30, drums) + 0.12 * verb(flt("high", 300, drums), 1.6, 13)
# ===== SKILL C level 2: turnarounds (low-end out + reverse reverb swell from own sounds) and downbeat markers
trans = np.zeros((N, 2)); lowcut = np.ones(N)
for bt, tgt in ((S["turn1"], S["peak"]), (S["turn2"], S["outro"])):
    lowcut *= 1 - 0.85 * np.interp(t, [tb(bt), tb(bt + 0.4), tb(tgt) - 0.02, tb(tgt)], [0, 1, 1, 0])
    hit = np.zeros((int(3 * SR), 2)); hit[:int(0.25*SR)] += pan2(rimS(1.0), 0); hit[:int(0.5*SR)] += pan2(kickS(0.5), 0)
    rev = verb(np.vstack([hit, np.zeros((int(1*SR), 2))]), 3.5, 21)[::-1][-int(2.4*SR):]   # reverse reverb swell, ends on the downbeat
    rev *= np.linspace(0, 1, len(rev))[:, None] ** 2; put(trans, nm(rev) * 0.6, tb(tgt) - len(rev) / SR)
    L = int(0.4 * SR); nz = flt("band", [800, 9000], rng.standard_normal((L, 2))) * np.exp(-np.arange(L) / SR / 0.08)[:, None]
    mk = np.zeros((int(4 * SR), 2)); mk[:L] = nz; mk[:int(0.25*SR)] += pan2(rimS(1.0), 0)      # marker: noise burst + perc hit into big reverb
    put(trans, 0.5 * nm(mk[:L]).copy() * 0.6 + 0 * 0, tb(tgt)); put(trans, 0.7 * nm(verb(mk, 4.5, 23)), tb(tgt)); events += 2
lowcutS = sm(lowcut, 40)
# ===== mix + master
kenv = sg.lfilter([1 - np.exp(-1/(0.18*SR))], [1, -np.exp(-1/(0.18*SR))], key); duck = 1 - D["sc"] * np.clip(kenv * 3, 0, 1)
low_stack = flt("low", 150, stack); stack_m = (stack - low_stack) + low_stack * lowcutS[:, None]
mix = nm(stack_m) * K["level"] + pan2(nm(sub) * K["subLevel"] * lowcutS, 0) * duck[:, None]
mix += arp * Q["level"] * duck[:, None] + drums * D["level"] + nm(trans) * 0.35
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
