#!/usr/bin/env python3
"""Daily 3-skill test 2026-11-25 "Zone Gate" (A minor, 90 BPM): ambient zone owners + establish/expand/contrast/return (YdnMi_TIXso) + acoustic-style 4-layer kick (oRhBZ6L9rU8) + autopan phase-360 amplitude gate (RDubhupxDsw). usage: render.py recipe.json out.wav"""
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
# ---- chord timeline: 8-bar loop of 2-bar chords
CH = []
for rep in range(0, NB, 8):
    for b0, b1, nmz, tones, root in R["chords"]: CH.append([b0 + rep, b1 + rep, nmz, tones, root])
R["chords"] = CH
def elgate(name, xf_ms=60):
    g = np.zeros(N)
    for s in SEC:
        if name in s["els"]: g[int(tb(s["b"][0]) * SR):int(tb(s["b"][1]) * SR)] = 1
    return sm(sm(g, xf_ms / 2), xf_ms / 2)
# ================= ZO step 2: body pad = 2 loops of the SAME pad slightly out of sync, energy 150-800 Hz (supporting depth: medium attack, medium verb)
P = R["pad"]; padM = np.zeros(N)
for b0, b1, nmz, tones, _ in CH:
    s0 = tb(b0); held = tb(b1) - s0; i0 = int(s0 * SR); i1 = min(int((tb(b1) + P["rel"] * 2.5) * SR), N); tt = t[i0:i1] - s0
    env = (1 - np.exp(-tt / (P["atk"] / 3))) * np.where(tt < held, 1.0, np.exp(-(tt - held) / (P["rel"] / 3))) * np.minimum(tt / 0.01, 1)
    for m in tones:
        f = np.full(i1 - i0, hz(m)); o = saw_osc(f, rng.uniform()) * 0.6 + saw_osc(f * 2 ** (P["detuneCents"] / 1200), rng.uniform()) * 0.4
        padM[i0:i1] += o * env; events += 1
padM = bw("high", P["hp"], bw("low", P["lp"], padM, 2), 2); padM = nm(padM)
off = int(P["offsetBeats"] * BT * SR); padB = np.concatenate([np.zeros(off), padM[:-off]])
pad = pan2(padM, P["panA"]) + pan2(padB, P["panB"]) * LV["padB"]; pad = nm(pad)
# ================= ZO step 1: low zone owner = simple mono unison bass on the root (A1 home), only octaves/5th; plain sine sub
B = R["bass"]; fB = np.zeros(N)
for b0, b1, nmz, tones, root in CH: fB[int(tb(b0) * SR):int(tb(b1) * SR) if b1 < NB else N] = hz(root)
fB = sm(fB, 3)   # 3 ms glue only (no glide)
bs = sum(saw_osc(fB * 2 ** (c / 1200), rng.uniform()) for c in B["unisonCents"]) / len(B["unisonCents"])
bs = bw("low", B["lp"], bs, 2); bs = np.tanh(bs * B["drive"]) / np.tanh(B["drive"]); bs = nm(bs)
sub = np.sin(2 * np.pi * np.cumsum(fB) / SR)
bassOn = elgate("bass", 80)
# ================= ZO step 4: focal voice (fast attack, brighter, drier, louder) - steady fixed-pitch phrase
L_ = R["lead"]; lead = np.zeros(N); counts = {}
def lnote(m, dur):
    Ln = int((dur + 1.2) * SR); tt = np.arange(Ln) / SR; ph = (hz(m) * tt) % 1.0
    y = (1 - L_["tri"]) * np.sin(2 * np.pi * ph) + L_["tri"] * (4 * np.abs(ph - 0.5) - 1)
    e = np.minimum(tt / L_["atk"], 1) * (L_["sus"] + (1 - L_["sus"]) * np.exp(-tt / L_["decay"])) * np.where(tt < dur, 1, np.exp(-(tt - dur) / 0.25))
    return fade(y * e, 40)
for b in range(0, NB, 2):
    for s16, m, l16 in L_["phrase"]:
        s0 = st(b, s16)
        if on("lead", s0 / BL + 1e-6): put(lead, lnote(m, l16 * BT / 4 * 0.92), s0); events += 1; k = sec_of(s0 / BL)["name"].split(":")[0]; counts[k] = counts.get(k, 0) + 1
lead = nm(bw("low", L_["lp"], lead, 2))
# ================= ZO step 5: hand-off = ONE pluck sequence, simple env, long slow LFO on cutoff, rhythmic (dotted 1/8) delay
K_ = R["pluck"]; pl = np.zeros(N)
for b0, b1, nmz, tones, root in CH:
    for bb in range(b0, b1):
        for i, ai in enumerate(K_["arp"]):
            s0 = st(bb, i * 2)
            if not on("pluck", s0 / BL + 1e-6): continue
            m = sorted(tones)[ai] + K_["oct"]; Ln = int(1.2 * SR); tt = np.arange(Ln) / SR; ph = (hz(m) * tt) % 1.0
            y = (2 * ph - 1) * np.minimum(tt / K_["atk"], 1) * np.exp(-tt / K_["decay"]); put(pl, fade(y, 30), s0); events += 1
            k = sec_of(s0 / BL)["name"].split(":")[0]; counts[k] = counts.get(k, 0) + 1
fcp = K_["lpRange"][0] * (K_["lpRange"][1] / K_["lpRange"][0]) ** (0.5 - 0.5 * np.cos(2 * np.pi * K_["lfoHz"] * (t - tb(16))))
pl = nm(dsp.svf(C(pl), C(fcp), 0.9, 0, SR)); dtp = K_["delayBeats"] * BT
pel, per = dsp.stereo_delay(C(pl), C(pl), SR, dtp, dtp * 2 / 1.5 * 0.75, K_["fb"], K_["fb"], 0.0, 0.0, 1, 300.0, 4000.0, 0.0, 0.0, 0.0)
# ================= GA: long texture -> autopan (beats 1/16, phase 360 = L/R together = amplitude gate), rounded shape, reverb AFTER the gate, amount automated
G = R["gate"]; tex = np.zeros(N)
for b0, b1, nmz, tones, root in CH:
    i0 = int(tb(b0) * SR); i1 = min(int((tb(b1) + 2.0) * SR), N); tt = t[i0:i1] - tb(b0); held = tb(b1) - tb(b0)
    env = np.minimum(tt / 0.6, 1) * np.where(tt < held, 1, np.exp(-(tt - held) / 0.6))
    for m in tones[1:]: tex[i0:i1] += saw_osc(np.full(i1 - i0, hz(m + 12)), rng.uniform()) * env
tex = nm(bw("high", 300, bw("low", G["tex_lp"], tex, 2), 2))
rateHz = R["bpm"] / 60 * 4 / G["rate16"] / 4 * 4 / 4   # 1/16 -> BPM/15 Hz
rateHz = R["bpm"] / 15 / G["rate16"]
lfoP = 0.5 + 0.5 * np.sin(2 * np.pi * rateHz * t)           # autopan L & R LFOs; phase offset 360 deg -> identical
shaped = np.clip((lfoP - 0.5) * (1 + 3 * G["shape"]) + 0.5, 0, 1); shaped = 0.5 - 0.5 * np.cos(np.pi * shaped)   # shape = flatter tops, rounded edges
amt = np.zeros(N)
for b0, b1, a in G["amount"]:
    i0, i1 = int(tb(b0) * SR), min(int(tb(b1) * SR), N)
    amt[i0:i1] = np.linspace(0, 1, i1 - i0) if a == "ramp" else a
amt = sm(amt, 50); gL = 1 - amt * (1 - shaped); gR = gL.copy()     # phase 360: same gain both sides
gated = np.stack([tex * gL, tex * gR], 1) * elgate("gate", 200)[:, None]
gv = verb(gated, G["rt"], 23, 7000.0, 2.0); gated = nm(gated * 0.6 + nm(gv) * 0.7)
# ================= ZO step 6: quiet air bed: noise -> LP + fixed comb -> big reverb, about -20 dB under the pad
A = R["air"]; nz = rng.standard_normal(N); nz = bw("low", A["lp"], nz, 2); d = int(SR / A["combHz"]); nz[d:] = nz[d:] + 0.6 * nz[:-d]
nz = bw("high", 5000, nz, 2); av = verb(np.stack([nz, nz], 1) * 0.3, A["rt"], 31, 14000.0, 2.4); air = nm(av)
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
# ================= mix
kenv = sm(sm(np.abs(kick), 3), 120); kenv /= kenv.max() + 1e-9
bduck = 1 - (1 - 10 ** (-LV["bassDuckDb"] / 20)) * np.clip(kenv * 2.5, 0, 1)
fg = pan2(lead, 0.0) * LV["lead"] * elgate("lead", 400)[:, None] + (pan2(pl, 0.1) * LV["pluck"] + nm(np.stack([pel, per], 1)) * LV["echo"]) * elgate("pluck", 400)[:, None]
bg = pad * LV["pad"] + gated * LV["gate"]
padRms = np.sqrt(np.mean((pad * LV["pad"]) ** 2)); air = air / np.sqrt(np.mean(air ** 2)) * padRms * 10 ** (R["air"]["relDb"] / 20)
vb = verb(C(bg + fg * 0.5), 5.0, 41, 7000.0, 2.2)
mix = bg + fg + nm(vb) * LV["verb"] + air
mix += pan2((bs * LV["bass"] + sub * LV["sub"]) * bassOn * bduck + nm(kick) * LV["kick"], 0) / np.sqrt(2)
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
