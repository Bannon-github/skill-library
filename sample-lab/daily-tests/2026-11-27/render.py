#!/usr/bin/env python3
"""Daily 3-skill test 2026-11-27 "Root Pulse" (G minor, 88 BPM): punchy deep kick tuned to the root (JhZU6JGvoHw) + four-role atmospheric pad with air at the source (0qOs9e5UwAU) + in-house isochronic staged gate-rate ramp. usage: render.py recipe.json out.wav"""
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
counts = {}
saw = lambda ph, f: 2 * ph - 1 - blep(ph, f / SR)
# ================= PAD (0qOs9e5UwAU): four roles
macro = autom(P["detuneMacro"], 3000); dc0, dc1 = P["detuneCents"]
lfo1 = 0.5 + 0.4 * np.sin(2 * np.pi * t / (P["low"]["lfoBars"] * BL))          # 1-bar position LFO (low layer)
lfo2 = 0.5 + 0.45 * np.sin(2 * np.pi * P["high"]["lfoHz"] * t + 0.7)           # free-rate (s) position LFO (high layer)
low = np.zeros((N, 2)); high = np.zeros((N, 2)); tri = np.zeros((N, 2)); nz = np.zeros((N, 2))
wn = rng.standard_normal((N, 2)) * 0.3
def uni_offsets(k): return np.linspace(-1, 1, k) if k > 1 else np.zeros(1)
for b0, b1, nmz, tones, root in CH:
    s0 = tb(b0); held = tb(b1) - s0; i0 = int(s0 * SR); i1 = min(int((tb(b1) + P["rel"] * 2.5) * SR), N); tt = t[i0:i1] - s0
    env = (1 - np.exp(-tt / (P["atk"] / 3))) * np.where(tt < held, 1.0, np.exp(-(tt - held) / (P["rel"] / 3)))
    dcent = dc0 + (dc1 - dc0) * macro[i0:i1]
    for vi, m in enumerate(tones):
        for role, mt, k in (("low", 0, P["low"]["uni"]), ("high", 12, P["high"]["uni"]), ("tri", 12, P["tri"]["uni"])):
            for j, o in enumerate(uni_offsets(k)):
                f = hz(m + mt) * 2 ** (o * dcent / 1200); ph = (0.37 * (j + 3 * vi) + np.cumsum(f / SR)) % 1
                pn = o * (0.3 if role == "low" else 0.7) if k > 1 else 0.0
                if role == "low":
                    p = lfo1[i0:i1]; y = (1 - p) * np.sin(2 * np.pi * ph) + p * 0.6 * saw(ph, f)
                    low[i0:i1] += pan2(y * env, pn) / k
                elif role == "high":
                    p = lfo2[i0:i1]; sq = saw(ph, f) - saw((ph + 0.5) % 1, f)
                    high[i0:i1] += pan2(((1 - p) * saw(ph, f) + p * 0.7 * sq) * env, pn) / k
                else:
                    tri[i0:i1] += pan2((2 * np.abs(2 * ph - 1) - 1) * env, pn) / k
        # key-tracked noise: broadband noise through a feedback comb tuned to the osc-3 note (+12)
        d = np.full(i1 - i0, SR / hz(m + 12))
        for c in range(2): nz[i0:i1, c] += dsp.comb_ff_fb(C(wn[i0:i1, c]), d, P["noise"]["fb"], 1.0) * env
low = bw("low", P["low"]["lp"], low, 2)
high = bw("low", P["high"]["lp"], bw("high", P["high"]["hp"], high, 2), 4); nz = bw("low", P["noise"]["lp"], bw("high", P["noise"]["hp"], nz, 2), 4)
pad = low * P["low"]["g"] + high * P["high"]["g"] + tri * P["tri"]["g"] + nz * P["noise"]["g"]
cf = P["chorus"]; l, r = dsp.chorus(C(pad[:, 0]), C(pad[:, 1]), SR, 1, cf["rate"], cf["depth"], cf["base"], 0.0, 1.0, cf["mix"], 0.0, 0.0); pad = np.stack([l, r], 1)
ph_ = P["phaser"]; pad = np.stack([dsp.phaser(C(pad[:, c]), ph_["rate"], 0.6, 0.3, 4, ph_["mix"], c * 0.5, SR) for c in range(2)], 1)
fl = P["flanger"]; l, r = dsp.chorus(C(pad[:, 0]), C(pad[:, 1]), SR, 0, fl["rate"], 1.0, fl["base"], fl["fb"], 1.0, fl["mix"], 0.25, 0.0); pad = np.stack([l, r], 1)
dl = P["delay"]; wl, wr = dsp.stereo_delay(C(pad[:, 0]), C(pad[:, 1]), SR, BL / 4, 3 * BL / 16, dl["fb"], dl["fb"], 0.0, 0.0, 1, 250.0, 6000.0, 0.0, 0.0, 0.0)
pad = pad + dl["mix"] * np.stack([wl, wr], 1)
vv = P["verb"]; pad = pad * (1 - vv["mix"] * 0.5) + vv["mix"] * nm(verb(C(pad), vv["rt"], 7, 9000.0, vv["size"])) * np.max(np.abs(pad))
pad = bw("low", P["eqLp"], bw("high", P["eqHp"], pad, 4), 2); pad = nm(pad)
# ================= KICK (JhZU6JGvoHw): sine sub 2 oct down on the root, hold/decay amp env, unipolar pitch env, same env -> driven LP, one-shot noise attack, EQ, sat, comp
K = R["kick"]; Lk = int(0.45 * SR); tk = np.arange(Lk) / SR
penv = np.exp(-tk / K["pitchTauS"]) ** K["curve"]                                    # unipolar, steep, ends at 0 -> lands on the root
fk = hz(K["rootMidi"]) * 2 ** (K["pitchSt"] * penv / 12); y = np.sin(2 * np.pi * np.cumsum(fk) / SR)
x = np.clip((tk - K["holdS"]) / K["decayS"], 0, 1); aenv = np.where(tk < K["holdS"], 1.0, np.cos(x * np.pi / 2) ** 2) * np.minimum(tk / 0.0008, 1)
nb = rng.standard_normal(Lk) * np.exp(-tk / (K["noiseMs"] / 1000)) * np.minimum(tk / 0.0005, 1)
nb = sg.sosfilt(sg.butter(2, K["noiseBp"], "band", fs=SR, output="sos"), nb); nb = nb / (np.abs(nb).max() + 1e-9) * 10 ** (K["noiseDb"] / 20)
k1 = np.tanh(K["drive"] * (y * aenv + nb)) / np.tanh(K["drive"])
k1 = dsp.svf(C(k1), C(K["lpBase"] + K["lpEnvHz"] * penv), 0.75, 0, SR)
k1 = dsp.eq(k1, "peak", K["mudHz"], 1.2, K["mudDb"]); k1 = dsp.eq(k1, "lowshelf", 70, 0.7, K["lowShelfDb"]); k1 = dsp.eq(k1, "highshelf", 4000, 0.7, K["highShelfDb"])
k1 = np.tanh(K["sat"] * k1); k1 /= np.abs(k1).max()
cp = K["comp"]; g = dsp.env_follow_gain(C(k1), SR, cp["thrDb"], cp["ratio"], cp["attS"], cp["relS"]); k1 = k1 * g * 10 ** (cp["makeupDb"] / 20)
k1 = fade(k1 / np.abs(k1).max(), 20)
kick = np.zeros(N)
for bb in range(NB):
    sname = sec_of(bb + 1e-6)["n"]
    if not (on("kick", bb + 1e-6) or (on("kickout", bb + 1e-6) and bb < 28)): continue
    beats = [0, 1, 2, 3] if on("kick4", bb + 1e-6) else [0, 2]
    if bb == 19 or bb == 7: beats = [0, 2]
    for q in beats: put(kick, k1, tb(bb) + q * BT); events += 1
# ================= BASS: mono root, saw LP + sine sub, ducked by kick
bs = np.zeros(N); fsub = np.zeros(N)
for b0, b1, nmz, tones, root in CH:
    fsub[int(tb(b0) * SR):int(tb(b1) * SR) if b1 < NB else N] = hz(root)
    for bb in range(b0, b1):
        for q in (0, 2) if not on("kick4", bb + 1e-6) else (0, 1.5, 2, 3.5):
            s0 = tb(bb) + q * BT
            if not on("bass", bb + 1e-6): continue
            Ln = int(0.55 * BT * SR if q % 1 else 0.95 * BT * SR); tt = np.arange(Ln) / SR; f = np.full(Ln, hz(root)); ph = np.cumsum(f / SR) % 1
            yb = (saw(ph, f) * 0.6 + saw((ph + 0.21) % 1, f * 1.003) * 0.4) * np.minimum(tt / 0.006, 1)
            put(bs, fade(yb, 30), s0, 1.0 if q % 1 == 0 else 0.75); events += 1
bs = nm(np.tanh(bw("low", 300, bs, 2) * 1.3)); be = sm(np.abs(bs), 15); sub = np.sin(2 * np.pi * np.cumsum(sm(fsub, 3)) / SR) * be / (be.max() + 1e-9)
bassOn = elgate("bass", 80)
# ================= ISO (in-house): hold -> linear glide -> hold, phase-integrated gate, raised-cosine edges, fixed carrier
I = R["iso"]; rate = np.zeros(N)
for b0, b1, r0, r1 in I["stagesBars"]:
    i0 = int(tb(b0) * SR); i1 = min(int(tb(b1) * SR), N); rate[i0:i1] = np.linspace(r0, r1, i1 - i0, endpoint=False)
rate[min(int(tb(I["stagesBars"][-1][1]) * SR), N):] = I["stagesBars"][-1][3]
gph = np.cumsum(rate) / SR % 1; e = np.minimum(I["edgeS"] * np.maximum(rate, 1e-3), I["duty"] / 2)
gg_ = np.clip(np.minimum(gph / e, (I["duty"] - gph) / e), 0, 1) * (gph < I["duty"]); gg_ = 0.5 - 0.5 * np.cos(np.pi * gg_)
iso = np.sin(2 * np.pi * hz(I["carrierMidi"]) * t) * gg_ * elgate("iso", 1500)
on_ = np.flatnonzero(np.diff((gg_ > 0.5).astype(int)) == 1) / SR
counts["iso_pulses_per_2s"] = [int(np.sum((on_ >= a) & (on_ < a + 2))) for a in np.arange(tb(8), tb(30) - 2, 4)]
# ================= LEAD: steady triangle, fixed pitch (B section)
lead = np.zeros(N)
for bb, s16, m, ln in R["lead"]:
    Ln = int((ln * BT / 4 + 0.4) * SR); tt = np.arange(Ln) / SR; ph = (hz(m) * tt) % 1
    yl = (2 * np.abs(2 * ph - 1) - 1) * np.minimum(tt / 0.012, 1) * np.where(tt < ln * BT / 4, 1, np.exp(-(tt - ln * BT / 4) / 0.12))
    put(lead, fade(yl, 30), st(bb, s16)); counts["lead"] = counts.get("lead", 0) + 1
lead = bw("low", 6000, lead, 2)
# ================= mix
kenv = sm(sm(np.abs(kick), 3), 120); kenv /= kenv.max() + 1e-9
bduck = 1 - (1 - 10 ** (-LV["bassDuckDb"] / 20)) * np.clip(kenv * 2.5, 0, 1)
fg = pan2(lead, 0.15) * LV["lead"] + pan2(iso, -0.1) * LV["iso"]
vb = verb(C(fg), 3.5, 41, 7000.0, 2.0)
mix = pad * LV["pad"] + fg + nm(vb) * LV["verb"] * np.max(np.abs(fg))
mix += pan2((bs * LV["bass"] + sub * LV["sub"]) * bassOn * bduck + kick * LV["kick"], 0) / np.sqrt(2)
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
