#!/usr/bin/env python3
"""Daily 3-skill test 2026-11-21 "Block Loop" (E minor, 92 BPM):
  P 80s PWM string pad (0n23itgG0LU): pulse osc, free-running 0.7 Hz LFO on pulse width, osc 2 slightly detuned,
    static LP (no filter env), slow attack / long release, 2 voices
  D delay as instrument (VSGYqvV4bTg): chorus built from a modulated 20 ms delay on the pad, mono-checked Haas clap,
    100%-feedback 1-bar looper overdubbed one note per cycle, repitch octave steps (exact 2:1), feedback 0 kill, resampled
    under the pattern, 1 ms grain-delay +12 octave layer (exact resample of the periodic loop)
  B 16-bar block map (JHiTUBVLmFI): blocks (scaled to 4 bars), top-perc gear shift per block, one break block, turnaround,
    squeeze-in/minimalism, marker + one reverse, +/++/- density, scoop-ups
usage: render.py recipe.json out.wav"""
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
CH = R["chords"]; BP = CH["barsPer"]; NCH = len(CH["names"]); BM = R["blockMap"]; events = 0
def blep(p, dt):
    out = np.zeros_like(p); a = p < dt; x = p[a] / dt[a]; out[a] = x + x - x * x - 1
    b = p > 1 - dt; x = (p[b] - 1) / dt[b]; out[b] = x * x + x + x + 1; return out
def pwm_osc(f, pw, ph0=0.0):  # band-limited pulse with per-sample pulse width (polyBLEP)
    dt = f / SR; ph = (ph0 + np.cumsum(dt)) % 1.0
    v = np.where(ph < pw, 1.0, -1.0) + blep(ph, dt) - blep((ph - pw) % 1.0, dt); return v - np.mean(v)
def saw_osc(f, ph0=0.0):
    dt = f / SR; ph = (ph0 + np.cumsum(dt)) % 1.0; return 2 * ph - 1 - blep(ph, dt)
def block_of(b):
    for k in BM["blocks"]:
        if k["b"][0] <= b < k["b"][1]: return k
    return BM["blocks"][-1]
# ================= P: 80s PWM string pad
P = R["pad"]; pw = P["pwCenter"] + P["pwDepth"] * np.sin(2 * np.pi * P["pwLfoHz"] * t)  # free-running seconds-based LFO
padL = np.zeros(N); padR = np.zeros(N)
for c0 in range(0, NB, BP):
    ci = (c0 // BP) % NCH; s0 = tb(c0); s1 = tb(min(c0 + BP, NB)); i0 = int(s0 * SR); i1 = min(int((s1 + P["rel"] * 2.5) * SR), N)
    tt = t[i0:i1] - s0; held = s1 - s0
    env = (1 - np.exp(-tt / (P["atk"] / 3))) * np.where(tt < held, 1.0, np.exp(-(tt - held) / (P["rel"] / 3)))
    env *= np.minimum(tt / 0.01, 1)
    for m in CH["tones"][ci]:
        for v in range(P["voices"]):
            cs = (v - (P["voices"] - 1) / 2) * P["voiceSpreadCents"]; f = np.full(i1 - i0, hz(m)) * 2 ** (cs / 1200)
            ph = rng.uniform(); y = pwm_osc(f, pw[i0:i1], ph) + P["osc2Level"] * saw_osc(f * 2 ** (P["osc2DetuneCents"] / 1200), (ph + 0.37) % 1)
            y *= env; (padL if v == 0 else padR)[i0:i1] += y; events += 1
pad = np.stack([padL, padR], 1)
pad = bw("low", P["lpHz"], pad, 2); pad = bw("high", R["pad"].get("hpHz", 110), pad, 2)  # static LP, filter env off
# D step 2: chorus built from a modulated ~20 ms delay (LFO phase offset != 0, feedback <= 60 %)
DC = R["delayChorus"]
cl, cr = dsp.chorus(C(pad[:, 0]), C(pad[:, 1]), SR, 0, DC["rate"], DC["depthMs"], DC["baseMs"], DC["fb"], 1.0, DC["mix"], DC["offset"], 0.0)
padC = np.stack([cl, cr], 1); padC = nm(padC) + 0.3 * nm(verb(padC, 4.0, 11, 6000.0, 2.0))
padC *= gate(0, NB + 3, 200)[:, None]
# ================= D step 4-6: 100%-feedback 1-bar looper, overdub one note per cycle, repitch octave steps, kill, resample
LP_ = R["looper"]; Ll = int(LP_["loopBars"] * BL * SR)
def pluck(m, L):
    tt = np.arange(L) / SR; f = np.full(L, hz(m))
    y = 0.6 * pwm_osc(f, np.full(L, 0.3)) + 0.4 * np.sin(2 * np.pi * hz(m) * tt)
    return y * np.exp(-tt / LP_["decay"]) * np.minimum(tt / 0.006, 1)
loopbuf = np.zeros(Ll); looper = np.zeros(N); nn = len(LP_["notes"])
up = np.zeros(NB + 4, bool)
for a, b in LP_["octaveUp"]: up[a:b] = True
cyc = 0; b = LP_["startBar"]; last = None
while b < NB + 2:
    if b < LP_["killBar"] and cyc < nn:  # overdub: a new note each cycle (feedback 100 % keeps old ones)
        beat, m = LP_["notes"][cyc]; y = pluck(m, Ll); i0 = int(beat * BT * SR); idx = (i0 + np.arange(Ll)) % Ll
        np.add.at(loopbuf, idx, y); events += 1
    if b > LP_["killBar"]: break  # feedback 0 at killBar: one more cycle then gone
    seg = loopbuf.copy()
    if up[b]:  # repitch: delay time halved -> exact 2:1 resample, plays twice per bar, +12 st (slightly darker tone)
        half = sg.resample_poly(seg, 1, 2); seg = np.concatenate([half, half])[:Ll]; seg = bw("low", 2600, seg, 1)
    i0 = int(tb(b) * SR); L = min(Ll, N - i0); looper[i0:i0 + L] += seg[:L]
    cyc += 1; b += LP_["loopBars"]
looper = sm(sm(looper, 2), 2)  # tiny smoothing at repitch switch points (no clicks)
looper = bw("low", LP_["lp"], looper, 2); looper = bw("high", 180, looper, 2)
go = LP_["grainOct"]; gw = sm(np.clip((bar - go["b"][0]) / (go["b"][1] - go["b"][0]), 0, 1) * (bar < go["b"][1] + 0.5), 300) * go["wetMax"]
octl = np.zeros(N)  # D step 7: 1 ms grain delay +12 st == exact 2:1 resample of the periodic loop (no spray -> no ticking)
for b in range(go["b"][0], go["b"][1] + 1):
    i0 = int(tb(b) * SR); L = min(Ll, N - i0); s = looper[i0:i0 + Ll]
    if len(s) < Ll: break
    h = sg.resample_poly(s, 1, 2); octl[i0:i0 + L] += np.concatenate([h, h])[:L]
looper = looper + gw * bw("low", 4500, octl, 2)
loopS = np.stack([looper, np.concatenate([np.zeros(int(0.011 * SR)), looper[:-int(0.011 * SR)]])], 1)
loopS = nm(loopS) * 0.7 + 0.35 * nm(verb(loopS, 3.5, 23, 6500.0, 2.0))
# ================= lead (call / response in the ++ drop and the squeeze-in)
LD = R["lead"]; fl = np.full(N, hz(69)); gl_ = np.zeros(N)
for b0, beat, m, d in LD["notes"]:
    s0 = tb(b0) + beat * BT; i0 = int(s0 * SR); L = int(d * BT * SR); tt = np.arange(L) / SR
    fl[i0:i0 + L] = hz(m); e = np.minimum(tt / 0.015, 1) * (0.4 + 0.6 * np.exp(-tt / LD["decay"])) * np.minimum((d * BT - tt) / 0.06, 1)
    gl_[i0:i0 + L] = np.maximum(gl_[i0:i0 + L], e); events += 1
fl = sm(fl, 3); lead = dsp.svf(C(0.5 * pwm_osc(fl, np.full(N, 0.5)) + 0.5 * saw_osc(fl)), C(np.full(N, float(LD["lp"]))), 0.8, 0, SR) * gl_
leadS = pan2(lead, 0.1); leadS = nm(leadS) * 0.8 + 0.35 * nm(verb(leadS, 3.0, 29, 7000.0, 1.8))
# ================= B: drums / top-perc gear shifts per block
K = R["kick"]
def kick1():
    L = int(K["gate"] * SR); tt = np.arange(L) / SR; f = K["endHz"] + (K["startHz"] - K["endHz"]) * np.exp(-tt / (K["tauMs"] / 1000))
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / K["decay"]) * np.minimum(tt / 0.003, 1)
    fw = int(0.08 * SR); y[-fw:] *= np.cos(np.linspace(0, np.pi / 2, fw)) ** 2; return y
def clap1():
    L = int(0.4 * SR); tt = np.arange(L) / SR
    y = bw("band", [900, 2600], rng.standard_normal(L), 2) * np.exp(-tt / 0.09) * np.minimum(tt / 0.004, 1)
    y = bw("low", 5000, y, 2); y[-480:] *= np.linspace(1, 0, 480); return y
def noise500():
    L = int(0.25 * SR); tt = np.arange(L) / SR
    y = bw("band", [380, 700], rng.standard_normal(L), 2) * np.exp(-tt / 0.05) * np.minimum(tt / 0.004, 1); y[-480:] *= np.linspace(1, 0, 480); return y
def ohat1():
    L = int(0.35 * SR); tt = np.arange(L) / SR
    y = bw("band", [5000, 9000], rng.standard_normal(L), 2) * np.exp(-tt / 0.12) * np.minimum(tt / 0.008, 1); y[-480:] *= np.linspace(1, 0, 480); return y
kick = np.zeros(N); clap = np.zeros(N); n5 = np.zeros(N); oh = np.zeros(N); bass = np.zeros(N); k1 = kick1()
for b in range(BM["drumsIn"], BM["drumsOut"]):
    blk = block_of(b)
    if blk.get("break"): continue
    for q in (0, 2): put(kick, k1, tb(b) + q * BT); events += 1
    top = blk.get("top", [])
    if "clap" in top:
        for q in (1, 3): put(clap, clap1(), tb(b) + q * BT); events += 1
    if "noise500" in top: put(n5, noise500(), tb(b) + 3.5 * BT); events += 1
    if "ohat" in top:
        for q in (0.5, 1.5, 2.5, 3.5): put(oh, ohat1(), tb(b) + q * BT); events += 1
# D step 1: Haas clap, right delay tuned while mono-summed (keep attack, avoid comb ringing / audible echo)
HA = R["haas"]; c1 = clap1(); pk = np.max(np.abs(c1)); best = None
for ms in range(HA["searchMs"][0], HA["searchMs"][1] + 1):
    d = int(ms / 1000 * SR); mono = 0.5 * (c1 + np.concatenate([np.zeros(d), c1[:-d]]))
    sp = 10 * np.log10(sg.welch(mono, SR, nperseg=4096)[1][20:400] / (sg.welch(c1, SR, nperseg=4096)[1][20:400] + 1e-20) + 1e-12)
    score = 20 * np.log10(np.max(np.abs(mono)) / pk) - 0.1 * np.std(sp)
    if best is None or score > best[0]: best = (score, ms, round(20 * np.log10(np.max(np.abs(mono)) / pk), 2))
dh = int(best[1] / 1000 * SR); clapS = np.stack([clap, np.concatenate([np.zeros(dh), clap[:-dh]])], 1)
clapS = nm(clapS) * 0.7 + 0.35 * nm(verb(clapS, 2.2, 37, 5500.0, 1.6))
ohS = pan2(oh, -0.3); ohS = bw("low", 9000, ohS, 2); n5S = pan2(n5, 0.25)
low_ok = np.ones(N)  # scoop-ups / turnaround / break: lows out
for blk in BM["blocks"]:
    if "turnaround" in blk: low_ok *= 1 - gate(*blk["turnaround"], 40)
    if "scoopUp" in blk: low_ok *= 1 - gate(*blk["scoopUp"], 40)
    if blk.get("minimal"): low_ok *= 1 - gate(*blk["b"], 40)
for b0 in range(BM["drumsIn"], BM["drumsOut"], BP):
    c = (b0 // BP) % NCH; L = int(BP * BL * SR); f = hz(CH["bass"][c] - 12); tt_ = np.arange(L) / SR
    if block_of(b0).get("break"): continue
    y = (np.sin(2 * np.pi * f * tt_) + 0.3 * np.sin(4 * np.pi * f * tt_)) * np.minimum(tt_ / 0.03, 1) * np.minimum((BP * BL - tt_) / 0.05, 1)
    put(bass, y, tb(b0)); events += 1
bass *= low_ok
kick_hp = bw("high", 160, kick, 2); kick = kick * low_ok + kick_hp * (1 - low_ok) * 0.6  # scooped kick keeps only its click-free body above 160
kenv = sm(sm(np.abs(kick), 3), 120); kenv /= kenv.max() + 1e-9
LV = R["levels"]; bass *= 1 - (1 - 10 ** (-LV["bassDuckDb"] / 20)) * np.clip(kenv * 2.5, 0, 1)
# marker splash + one reverse swell (sparingly)
rev = np.zeros((N, 2)); spl = np.zeros((N, 2))
for blk in BM["blocks"]:
    if "reverseInto" in blk:
        e = int(tb(blk["reverseInto"]) * SR); L = int(2 * BL * SR); src = padC[e - L:e].copy()[::-1]
        w = verb(np.ascontiguousarray(src), 6.0, 51, 5000.0, 2.4)[::-1]; w *= (np.linspace(0, 1, L) ** 2)[:, None]; w[-int(0.03 * SR):] *= np.linspace(1, 0, int(0.03 * SR))[:, None]
        rev[e - L:e] += nm(w)
    if "marker" in blk:
        i0 = int(tb(blk["marker"]) * SR); L = int(3 * SR); tt = np.arange(L) / SR
        y = bw("band", [2500, 8000], rng.standard_normal(L), 2) * np.minimum(tt / 0.03, 1) * np.exp(-tt / 0.8)
        spl[i0:i0 + L] += nm(verb(pan2(y, 0), 3.0, 61, 7000.0, 2.0))
mix = (padC * LV["pad"] + loopS * LV["loop"] + leadS * LV["lead"] + rev * LV["rev"] + spl * LV["splash"]) * (1 - 0.15 * np.clip(kenv * 2.5, 0, 1))[:, None]
mix += pan2(nm(bass) * LV["bass"], 0) / np.sqrt(2) + pan2(nm(kick) * LV["kick"], 0) / np.sqrt(2)
mix += clapS * LV["clap"] + nm(ohS) * LV["ohat"] + nm(n5S) * LV["noise500"]
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
res["events"] = events; res["lengthSec"] = round(T, 2); res["lufs"] = round(meter.integrated_loudness(mix), 2); res["drumsInSec"] = round(tb(BM["drumsIn"]), 2)
side = 0.5 * (mix[:, 0] - mix[:, 1]); mid = 0.5 * (mix[:, 0] + mix[:, 1]); db = lambda x: 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)
hf = bw("high", 8000, mid, 4); he = np.abs(hf); spikes = int(np.sum(he > 8 * (sm(he, 50) + 1e-9)))
ed = sm(he, 5)[::480]; fq, Pw = sg.welch(ed - ed.mean(), fs=100, nperseg=1024)
def cent(x):
    f_, tt_, Z = sg.stft(x.mean(1), SR, nperseg=4800); P_ = np.abs(Z) ** 2; c_ = (P_ * f_[:, None]).sum(0) / (P_.sum(0) + 1e-12); return float(np.median(c_))
blocks = [k["b"] for k in BM["blocks"]]; sec = lambda b0, b1: mix[int(tb(b0) * SR):int(tb(b1) * SR)]
cents = [cent(sec(a, b)) for a, b in blocks]
res["checks"] = {"haas_clap_ms": best[1], "haas_mono_peak_db": best[2], "side_below_120Hz_db": round(db(bw("low", 120, side, 4)) - db(bw("low", 120, mid, 4)), 1), "hf_spikes_over_8x": spikes,
  "hf_env_12_40_vs_0_12_db": round(10 * np.log10(Pw[(fq >= 12) & (fq <= 40)].mean() / Pw[(fq > 0.2) & (fq < 12)].mean()), 1),
  "block_lufs": [round(meter.integrated_loudness(sec(a, b)), 1) for a, b in blocks], "block_centroid_hz": [round(c) for c in cents],
  "centroid_span_oct": round(float(np.log2(max(cents) / min(cents))), 2)}
json.dump(res, open(OUT + ".stats.json", "w"), indent=1, default=float)
print(json.dumps({"score": res["score"], "pass": res["pass"], "lufs": res["lufs"], "tp": res["extra"].get("true_peak_dbtp"), "gates": res["gates"], "subs": res["subs"], "tilt": res["extra"].get("tilt_db_oct"), "gr": round(gr_max, 2), "len": res["lengthSec"], "drumsIn": res["drumsInSec"], "checks": res["checks"]}, default=float))
