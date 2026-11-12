#!/usr/bin/env python3
"""Daily 3-skill test 2026-11-12 "Phase Loop":
  L looper-drone-clips-... (sine -> gain swell -> 70% wet low-cut verb -> 1-bar looper; 4 clips on 0 dB-capped faders; group verb/pingpong/tape/glue)
  P phaser-drums-...       (short impulse pings an 8-pole all-pass bank with feedback; centre freq + feedback sequenced per step)
  K reverb-rumble-kick-... (4/4 kick, NY-comp / drive / short verb returns, verb ducked by kick, 1/8-synced LP, low-end enhancer)
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
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
C = np.ascontiguousarray
def bw(k, f, x, o=2): return sg.sosfilt(sg.butter(o, f, k, fs=SR, output="sos"), x, axis=0)
def pan2(x, p): return np.stack([x * np.cos((p + 1) * np.pi / 4), x * np.sin((p + 1) * np.pi / 4)], 1) * np.sqrt(2)
def put(buf, y, s, g=1.0):
    i = int(round(s * SR)); L = min(len(y), N - i)
    if L > 0 and i >= 0: buf[i:i+L] += y[:L] * g
def verb(x, rt, seed, damp=9000.0, size=1.8, mod=0.2, diff=0.75, pre=0.02):
    l, r = dsp.fdn_reverb(C(x[:, 0]), C(x[:, 1]), SR, float(rt), size, damp, pre, mod, diff, 0.0, seed); return np.stack([l, r], 1)
nm = lambda x: x / (np.max(np.abs(x)) + 1e-9)
def sm(x, ms): a = np.exp(-1 / (ms / 1000 * SR)); return lfilter([1 - a], [1, -a], x, axis=0)
def curve(pts):  # fader automation in bars -> per-sample gain, capped at 1.0 (0 dB)
    xs, ys = zip(*pts); return np.minimum(np.interp(bar, xs, ys), 1.0)
def seg(b0, b1, xf=0.5): return np.clip((bar - b0) / xf, 0, 1) * np.clip((b1 - bar) / xf, 0, 1)
events = 0
# ================= L: looper drone clips
Lp = R["looper"]; LoopN = int(BL * SR); lt = np.arange(LoopN) / SR; lv = Lp["loopVerb"]
clips = []
for ci, cl in enumerate(Lp["clips"]):
    dry = np.zeros(LoopN)
    for m, (st, pk) in zip(cl["notes"] * 3, cl["swells"]) if len(cl["swells"]) == len(cl["notes"]) else [(cl["notes"][k % len(cl["notes"])], s) for k, s in enumerate(cl["swells"])]:
        pass
    for k, m in enumerate(cl["notes"]):
        st, pk = cl["swells"][k % len(cl["swells"])]
        ph = (lt / BL - st) % 1.0                      # L step 2: hold note, ease gain up then down (wraps across the loop point)
        g = pk * np.sin(np.pi * np.clip(ph / 0.9, 0, 1)) ** 2
        dry += np.sin(2 * np.pi * hz(m) * lt + rng.random() * 6.28) * g
        events += 1
    dry /= max(1, len(cl["notes"])) ** 0.5
    # L step 1: sine -> utility -> long low-cut reverb 70% wet -> 1-bar looper. Overdub tails fold back onto the loop (circular steady state).
    reps = 4; x = np.tile(dry, reps); xs = np.stack([x, x], 1)
    w = bw("high", lv["lowCut"], verb(xs, lv["rt"], 50 + ci, 5000.0, 2.0, 0.15), 2)
    y = (1 - lv["wet"]) * xs + lv["wet"] * nm(w) * np.max(np.abs(xs)) * 0.9
    loop = y[(reps - 1) * LoopN: reps * LoopN]           # last pass = loop with wrapped tails
    clip = np.tile(loop, (NB + 2, 1))[:N]
    clips.append(clip * curve(cl["fader"])[:, None])    # L step 5: one fader per clip, max 0 dB
grp = sum(clips)
G = Lp["group"]
# L step 6: group reverb ~8 s low cut 50% wet; unsynced ping-pong 50% wet ~70% fb; tape colour (hum+noise low); glue comp
gv = bw("high", G["verbLowCut"], verb(grp, G["verbRt"], 61, 6000.0, 2.4, 0.2), 2); grp = grp * (1 - G["verbWet"]) + nm(gv) * np.max(np.abs(grp)) * G["verbWet"]
dl = np.stack(dsp.stereo_delay(C(grp[:, 0]), C(grp[:, 1]), SR, G["delayL"], G["delayR"], G["delayFb"], G["delayFb"], 0.0, 0.0, 1, 250, 4000, 0.15, 0.0, 0.2), 1)
grp = grp * (1 - G["delayWet"] * 0.5) + dl * G["delayWet"] * 0.5
pk = np.max(np.abs(grp)); grp = np.tanh(grp / pk * G["tapeDrive"]) / np.tanh(G["tapeDrive"]) * pk
grp += (10 ** (G["humDb"] / 20) * np.sin(2 * np.pi * 60 * t) * pk)[:, None] + 10 ** (G["noiseDb"] / 20) * pk * bw("low", 6000, rng.standard_normal((N, 2)))
# L step 7 (optional field-recording track): synthetic wind/air bed, band-passed noise with a slow sway, its own fader
Fd = Lp["field"]; fn = rng.standard_normal((N, 2)); fn = np.stack([lfilter([1, -0.97], [1, -0.995], fn[:, c]) for c in range(2)], 1)
fn = bw("band", [Fd["bandLo"], Fd["bandHi"]], fn, 2); fn = fn / np.std(fn) * Fd["level"] * np.std(grp)
fn *= (1 - Fd["swayDepth"] * 0.5 * (1 + np.sin(2 * np.pi * Fd["swayHz"] * t)))[:, None] * np.clip(bar / 2, 0, 1)[:, None]
grp = grp + fn
mid = 0.5 * (grp[:, 0] + grp[:, 1]); thr = 20 * np.log10(np.percentile(np.abs(mid), 99) + 1e-9) - 3
grp *= dsp.env_follow_gain(C(mid), SR, thr, G["glueRatio"], 0.03, 0.3)[:, None]
# ================= P: phaser drums (LTI per hit: 8 first-order all-passes in a feedback loop, LFO depth 0)
Pd = R["phaserDrums"]; NP = Pd["poles"]
from numba import njit
@njit(cache=True)
def ring_ir(x, fc, fb, poles, sr):   # P steps 1-4: LFO off, fixed centre, feedback loop around a bank of first-order all-passes
    tt_ = np.tan(np.pi * fc / sr); a = (tt_ - 1.0) / (tt_ + 1.0); zs = np.zeros(poles); y = np.zeros(x.shape[0]); last = 0.0
    for i in range(x.shape[0]):
        v = x[i] + fb * last
        for s in range(poles):
            o = a * v + zs[s]; zs[s] = v - a * o; v = o
        last = v; y[i] = v
    return y
cache = {}
def lowest_peak(y, fmax):
    Y = np.abs(np.fft.rfft(y, 1 << 16)); f = np.fft.rfftfreq(1 << 16, 1 / SR); sel = (f > 40) & (f < fmax)
    pk = sg.find_peaks(Y[sel], prominence=Y[sel].max() * 0.2)[0]; return f[sel][pk[0]] if len(pk) else f[sel][np.argmax(Y[sel])]
def tuned(m, fb):  # P step 5: find the sweep (centre) that puts the lowest ring on the note
    key = (m, fb)
    if key in cache: return cache[key]
    target = hz(m); lo, hi = target, target * 12; x = np.zeros(SR // 2); x[:imp_n] = imp
    for _ in range(30):
        fc = np.sqrt(lo * hi); pkf = lowest_peak(ring_ir(x, fc, fb, NP, SR), target * 3)
        lo, hi = (fc, hi) if pkf < target else (lo, fc)
    cache[key] = fc; return fc
imp_n = max(3, int(Pd["impulseMs"] / 1000 * SR)); imp = np.hanning(imp_n); imp = np.r_[imp, np.zeros(64)]; imp = bw("low", Pd.get("impulseLp", 20000), imp, 2); imp_n = len(imp)   # P step 2: very short (soft) impulse
pdr = np.zeros((N, 2)); pbeats = Pd["patternBeats"]
for b0 in np.arange(S["phaserIn"] * 4, S["kickOut"] * 4 + 4, pbeats):
    for pos, m, acc in Pd["pattern"]:
        beat = b0 + pos
        if beat >= S["end"] * 4 - 2: continue
        fb = Pd["fbAccent"] if acc else Pd["fbNormal"]                             # P step 6: feedback sequenced per step (accents ring longer)
        fc = tuned(m, fb); L = int(1.4 * SR); x = np.zeros(L); x[:imp_n] = imp
        y = ring_ir(x, fc, fb, NP, SR); y = y / (np.max(np.abs(y)) + 1e-9) * (1.0 if acc else 0.75)
        y *= np.clip((L - np.arange(L)) / (0.05 * SR), 0, 1)
        put(pdr, pan2(y, 0.3 * np.sin(beat * 1.7)), beat * BT); events += 1
pdr = bw("high", Pd["hp"], pdr, 2) * (1 - 0.7 * seg(S["break"], S["back"], 0.5))[:, None]
# ================= K: reverb / rumble kick (all mono)
K = R["kick"]; kick = np.zeros(N)
def kick1():
    L = int(0.42 * SR); tt_ = np.arange(L) / SR; f = K["f1"] + (K["f0"] - K["f1"]) * np.exp(-tt_ / 0.035)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt_ / 0.16) * np.clip(tt_ / 0.0025, 0, 1)
    y[-int(0.02 * SR):] *= np.linspace(1, 0, int(0.02 * SR)); return y
kon = lambda b: S["kickIn"] <= b < S["kickOut"] and not (S["break"] <= b < S["back"])
for b in range(NB):
    if not kon(b): continue
    for q in range(4): put(kick, kick1(), tb(b) + q * BT, K["vel"][q]); events += 1   # K step 1: weak beats ~80, medium ~90
kick *= 0.7                                                                          # leave headroom
A_ = K["retA"]; key = bw("low", 150, kick, 2); kp = 20 * np.log10(np.max(np.abs(key)) + 1e-9)
gA = dsp.env_follow_gain(C(key), SR, kp - A_["grDb"] / (1 - 1 / A_["ratio"]) * 1.0, A_["ratio"], A_["attMs"] / 1000, A_["relS"])
retA = dsp.eq(C(dsp.eq(C(kick * gA), "lowshelf", 90, 0.7, A_["lowShelfDb"])), "highshelf", 5000, 0.7, A_["highShelfDb"])
retA = retA / (np.max(np.abs(retA)) + 1e-9) * np.max(np.abs(kick))
B_ = K["retB"]; retB = np.tanh(kick / np.max(np.abs(kick)) * (1 + 10 * B_["drive"])) * np.max(np.abs(kick)) / (1 + 10 * B_["drive"]) * 3
Cc = K["retC"]; ks = np.stack([kick, kick], 1)
rv = verb(ks, Cc["rt"], 71, Cc["damp"], Cc["size"], 0.05, 0.8, 0.005); rv = 0.5 * (rv[:, 0] + rv[:, 1])    # small, high-cut, long decay -> rattle
rv = rv * dsp.env_follow_gain(C(kick), SR, kp - 24, 20.0, 0.002, Cc["duckRelS"])                         # ducked by the kick
lfo8 = np.sin(2 * np.pi * t / (BT * Cc["lfoDiv"])); slow = np.sin(2 * np.pi * Cc["slowHz"] * t)
cut = Cc["lpBase"] * 2 ** (Cc["lpOct"] * 0.5 * (lfo8 + 1) + Cc["slowOct"] * slow)
rv = dsp.svf(C(rv), C(cut), 0.7, 0, SR)
rumble = rv / (np.max(np.abs(rv)) + 1e-9) * np.max(np.abs(kick))
kb = kick + A_["level"] * retA + B_["level"] * retB + Cc["level"] * rumble
En = K["enhancer"]; kb = dsp.eq(C(kb), "lowshelf", 70, 0.7, En["shelfDb"]); pk = np.max(np.abs(kb)); kb = np.tanh(kb / pk * En["drive"]) / np.tanh(En["drive"]) * pk
kb = bw("low", 9000, kb, 2)
# phaser drums into the drone group verb (send)
pdV = bw("high", 250, verb(pdr, 3.5, 81, 6000.0, 1.6, 0.2), 2)
# ================= mix + master
Mm = R["master"]
mix = nm(grp) * Lp["level"] + nm(pdr) * Pd["level"] + nm(pdV) * Pd["level"] * Pd["send"] + pan2(nm(kb), 0) * K["level"] / np.sqrt(2)
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
res = metrics.compute(mix, {"limiter_gr_db": gr_max}, R.get("category", "pad"), False, NB * BL, start_body_s=0.0, f_low=hz(26), bar_s=BL)
res["events"] = events; res["lengthSec"] = round(T, 2); res["lufs"] = round(meter.integrated_loudness(mix), 2); res["drumsInSec"] = round(tb(S["kickIn"]), 2)
side = 0.5 * (mix[:, 0] - mix[:, 1]); mid = 0.5 * (mix[:, 0] + mix[:, 1])
db = lambda x: 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)
hf = bw("high", 8000, mid, 4); he = np.abs(hf); spikes = int(np.sum(he > 8 * (sm(he, 50) + 1e-9)))
ed = sm(he, 5)[::480]; fq, Pw = sg.welch(ed - ed.mean(), fs=100, nperseg=1024)
# phaser-drum tuning check: spectral peak of single test hits vs target note
tun = []
for m in (62, 69, 57):
    x = np.zeros(SR); x[:imp_n] = imp; y = ring_ir(x, tuned(m, Pd["fbNormal"]), Pd["fbNormal"], NP, SR)
    tun.append(round(1200 * np.log2(lowest_peak(y, hz(m) * 3) / hz(m))))
def t60(m, fb):
    x = np.zeros(SR); x[:imp_n] = imp; e = np.abs(sg.hilbert(ring_ir(x, tuned(m, fb), fb, NP, SR))); e /= e.max(); return round(float(np.argmax(e < 10 ** (-40 / 20))) / SR, 3)
ks_ = slice(int(tb(S["kickIn"] + 1) * SR), int(tb(S["break"]) * SR))
res["checks"] = {"side_below_120Hz_db": round(db(bw("low", 120, side, 4)) - db(bw("low", 120, mid, 4)), 1), "hf_spikes_over_8x": spikes,
  "hf_env_12_40_vs_0_12_db": round(10 * np.log10(Pw[(fq >= 12) & (fq <= 40)].mean() / Pw[(fq > 0.2) & (fq < 12)].mean()), 1),
  "phaser_tuning_cents_D4_A4_A3": tun, "phaser_ring_40dB_s_normal_vs_accent": [t60(62, Pd["fbNormal"]), t60(62, Pd["fbAccent"])],
  "retA_gr_db_max": round(float(-20 * np.log10(gA.min())), 1),
  "rumble_vs_dry_kick_db": round(db(Cc["level"] * rumble[ks_]) - db(kick[ks_]), 1),
  "first_half_vs_second_half_lufs": round(meter.integrated_loudness(mix[:N // 2]) - meter.integrated_loudness(mix[N // 2:]), 1)}
json.dump(res, open(OUT + ".stats.json", "w"), indent=1, default=float)
print(json.dumps({"score": res["score"], "pass": res["pass"], "lufs": res["lufs"], "tp": res["extra"].get("true_peak_dbtp"), "gates": res["gates"], "subs": res["subs"], "tilt": res["extra"].get("tilt_db_oct"), "gr": round(gr_max, 2), "len": res["lengthSec"], "drumsIn": res["drumsInSec"], "checks": res["checks"]}, default=float))
