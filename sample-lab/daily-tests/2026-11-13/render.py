#!/usr/bin/env python3
"""Daily 3-skill test 2026-11-13 "Smear Key":
  A arp-smear-pad-...  (Am9 down arp -> grain delay pitch 0 + reverse repeats -> resample -> stretch 2x pitch kept -> high-wet echo -> 1/16 spectral freeze crossfaded -> band EQ; feedback-bandpass loop layer -> resample -> loop region)
  N noise-recording-tuned-to-key-... (ambience+harsh noise -> 4 series max-Q peaks at root -> bounce -> sampler chords, fixed start, crossfaded loop, slow attack, verb/delay, sidechain duck, EQ automation)
  B punchy-808-...     (sine + 2nd/3rd partials, unipolar short coarse dive, convex decay, FM ratio 0.5 transient LP, 2 soft clips + limiter, zero-cross print)
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
nm = lambda x: x / (np.max(np.abs(x)) + 1e-9)
def sm(x, ms): a = np.exp(-1 / (ms / 1000 * SR)); return lfilter([1 - a], [1, -a], x, axis=0)
def seg(b0, b1, xf=0.5): return np.clip((bar - b0) / xf, 0, 1) * np.clip((b1 - bar) / xf, 0, 1)
events = 0
# ================= A: arp smear pad
A = R["arp"]; SN = int(A["srcBars"] * BL * SR); st_ = np.arange(SN) / SR
seq = [m + 12 * o for o in range(A["octaves"]) for m in A["chord"]][::-1]       # A1: down pattern, 2 octave steps
step = A["rate"] * BT; src = np.zeros(SN); k = 0; ts = 0.0
while ts < SN / SR - 0.05:
    m = seq[k % len(seq)]; L = int(step * A["gate"] * SR * 2.2); tt_ = np.arange(L) / SR      # long gate overlaps notes
    f = hz(m); y = sum(np.sin(2 * np.pi * f * h * tt_) / h for h in range(1, A.get('harm', 7)))            # soft saw-ish, steady pitch
    y *= np.minimum(tt_ / 0.01, 1) * np.exp(-tt_ / 0.45) * np.clip((L / SR - tt_) / 0.05, 0, 1)
    put(src, y, ts, 0.3); ts += step; k += 1; events += 1
src = bw("low", A["cut"], src, 2)
G = A["grain"]; gl = int(G["ms"] / 1000 * SR); win = np.hanning(gl); gr = np.zeros(SN + gl)   # A2: grain delay, pitch 0
for c in np.arange(0, SN - gl, int(G["everyMs"] / 1000 * SR)):
    d = int((G["delayMs"] + rng.uniform(0, G["sprayMs"])) / 1000 * SR); s0 = c - d
    if s0 < 0: continue
    gr[c:c + gl] += src[s0:s0 + gl] * win
gr = gr[:SN] * 0.5
Rv = A["rev"]; qb = int(BT * SR); rv = np.zeros(SN)                                          # A2: delay with reverse repeats
for i in range(0, SN - qb, qb):
    chunk = src[i:i + qb][::-1] * np.hanning(qb); g = Rv["wet"]
    for r_ in range(1, 4):
        j = i + r_ * qb
        if j + qb > SN: break
        rv[j:j + qb] += chunk * g; g *= Rv["fb"]
res1 = src * 0.6 + gr * G["mix"] + rv                                                           # A3: resample
def stretch(x, ratio, wl=0.12, hs=0.03):                                                        # A4: OLA stretch, pitch kept
    W = int(wl * SR); Hs = int(hs * SR); Ha = int(Hs / ratio); w = np.hanning(W); n = int((len(x) - W) / Ha)
    y = np.zeros(n * Hs + W); nrm = np.zeros_like(y)
    for i in range(n): y[i * Hs:i * Hs + W] += x[i * Ha:i * Ha + W] * w; nrm[i * Hs:i * Hs + W] += w
    return y / np.maximum(nrm, 1e-3)
st2 = stretch(res1, 2.0); st2 = np.pad(st2, (0, max(0, N - len(st2))))[:N]
E_ = A["echo"]; el, er = dsp.stereo_delay(C(st2), C(st2), SR, E_["time"] * BL / 2, E_["time"] * BL / 2 * 1.5, E_["fb"], E_["fb"], 0.0, 0.0, 1, 150, 6000, 0.1, 0.0, 0.2)
ech = np.stack([st2, st2], 1) * (1 - E_["wet"]) + np.stack([el, er], 1) * E_["wet"]           # A5: high wet + feedback
F = A["freeze"]; nf = F["nfft"]; hp_ = F["hop"]; win2 = sg.get_window("hann", nf)                         # A6: spectral freeze, retrigger 1/16 crossfaded
def freeze(x):
    _, _, Z = sg.stft(x, SR, window=win2, nperseg=nf, noverlap=nf - hp_, boundary=None, padded=True)
    mag = np.abs(Z); nfr = mag.shape[1]; ft = np.arange(nfr) * hp_ / SR; per = BT / 4
    idx = np.minimum((np.floor(ft / per) * per * SR / hp_).astype(int), nfr - 1)
    nxt = np.minimum((np.floor(ft / per + 1) * per * SR / hp_).astype(int), nfr - 1); fr = (ft % per) / per
    M = mag[:, idx] * (1 - fr) + mag[:, nxt] * fr
    adv = 2 * np.pi * np.arange(mag.shape[0])[:, None] * hp_ / nf
    ph = np.cumsum(np.repeat(adv, nfr, 1), 1) + rng.uniform(0, 2 * np.pi, (mag.shape[0], 1))
    _, y = sg.istft(M * np.exp(1j * ph), SR, window=win2, nperseg=nf, noverlap=nf - hp_, boundary=False); return y
fz = np.stack([np.pad(freeze(ech[:, c]), (0, N))[:N] for c in range(2)], 1)
pad = ech * (1 - F["mix"]) + nm(fz) * np.max(np.abs(ech)) * F["mix"]
pad = bw("band", A["band"], pad, 2)                                                                  # A6: confine to band
pad = nm(pad) * (0.55 + 0.45 * np.clip(bar / 4, 0, 1))[:, None]
# A7-8: feedback band-pass loop layer -> resample -> loop region
Fb = R["feedback"]; LB = int(Fb["loopBeats"] * BT * SR); mel = np.zeros(LB); lt = np.arange(LB) / SR
for b, m in Fb["notes"]:
    L = int(0.9 * BT * SR); tt_ = np.arange(L) / SR; y = np.sin(2 * np.pi * hz(m) * tt_) + 0.3 * np.sin(4 * np.pi * hz(m) * tt_)
    put(mel, y * np.minimum(tt_ / 0.008, 1) * np.exp(-tt_ / 0.35), b * BT); events += 1
FN = int(10 * BL * SR); fin = np.tile(mel, FN // LB + 1)[:FN]; D = int(0.75 * BL * SR); sub = D // 12
sosN = sg.butter(2, [Fb["bpHz"] * (1 - 0.5 / Fb["qNarrow"]), Fb["bpHz"] * (1 + 0.5 / Fb["qNarrow"])], "band", fs=SR, output="sos")
sosW = sg.butter(1, [Fb["bpHz"] / 2 ** (0.5 / Fb["qWide"] * 2), Fb["bpHz"] * 2 ** (0.5 / Fb["qWide"] * 2)], "band", fs=SR, output="sos")
zN = np.zeros((sosN.shape[0], 2)); zW = np.zeros((sosW.shape[0], 2)); fy = np.zeros(FN)
for i in range(0, FN, sub):
    j = min(i + sub, FN); prev = fy[i - D:j - D] if i >= D else np.zeros(j - i)
    sat = np.tanh(prev * Fb["drive"]) / Fb["drive"]
    a, zN = sg.sosfilt(sosN, sat, zi=zN); b2, zW = sg.sosfilt(sosW, sat, zi=zW)
    w_ = 0.5 + 0.5 * np.sin(2 * np.pi * (i / SR) / BL)                                                  # 1-bar LFO on width
    fy[i:j] = fin[i:j] + Fb["fb"] * (w_ * a * 2.5 + (1 - w_) * b2)
fy = np.tanh(fy * 1.2) / 1.2
r0, r1 = [int(x * BL * SR) for x in Fb["loopRegionBars"]]; reg = fy[r0:r1].copy(); xf = int(0.05 * SR)
reg[:xf] *= np.linspace(0, 1, xf); reg[-xf:] *= np.linspace(1, 0, xf)
fbl = np.zeros(N); RL = len(reg) - xf
for p in range(0, N, RL): put(fbl, reg, p / SR)
fbl = bw("high", 200, fbl, 2) * (seg(8, S["break"], 1) + seg(S["back"], S["end"] - 1, 1)); fbl = pan2(nm(fbl), -0.25)
fbl = fbl * 0.7 + 0.5 * nm(verb(fbl, 3.0, 31, 7000.0)) * np.max(np.abs(fbl))
# ================= N: key-tuned noise pad
Np = R["noisePad"]; ln = int(4 * SR)
amb = bw("band", [300, 3000], rng.standard_normal(ln), 2) * (0.6 + 0.4 * np.abs(np.sin(2 * np.pi * 3.3 * np.arange(ln) / SR + rng.uniform(0, 6, 1))))  # "voices/ambience"
hs = bw("high", 1500, rng.standard_normal(ln), 2)                                                        # harsh noise
ns = nm(amb + 0.6 * hs) * 0.05                                                                           # N1: blend, bounce
for _ in range(Np["eqCount"]): ns = dsp.eq(C(ns), "peak", Np["rootHz"], Np["eqQ"], Np["eqGain"]); ns = ns / np.max(np.abs(ns)) * 0.5   # N2-3 (fader down each copy)
ns = nm(ns); raw = nm(amb + 0.6 * hs)                                                                   # N4: print (raw kept for N8 'more noise')
s0 = int(Np["startSec"] * SR); Ls = int(Np["loopSec"] * SR); Xf = int(Np["xfadeSec"] * SR)
def voice(semi, dur):                                                                                   # N5/N7: sampler, fixed start, crossfaded loop
    rate = 2 ** (semi / 12); need = int(dur * SR * rate) + 10
    lp = ns[s0:s0 + Ls].copy(); out = list(ns[:s0]) if False else []
    body = ns[s0:s0 + Ls + Xf]; loop = body[:Ls].copy(); loop[:Xf] = loop[:Xf] * np.linspace(0, 1, Xf) + body[Ls:Ls + Xf] * np.linspace(1, 0, Xf)
    y = np.tile(loop, need // Ls + 2)[:need]; pos = np.arange(int(dur * SR)) * rate
    return np.interp(pos, np.arange(len(y)), y)
npd = np.zeros((N, 2)); cb = 2
for ci, b0 in enumerate(range(0, NB, cb)):
    ch = Np["chords"][ci % len(Np["chords"])]; dur = cb * BL + Np["release"]; tt_ = np.arange(int(dur * SR)) / SR
    env = np.minimum(tt_ / Np["attack"], 1) * np.clip((dur - tt_) / Np["release"], 0, 1)                   # N6: slow attack
    for vi, m in enumerate(ch):
        put(npd, pan2(voice(m - 57, dur) * env, (vi - 1) * 0.5), tb(b0), 0.4); events += 1
nv = verb(npd, 5.0, 41, 8000.0, 2.0); dl_ = np.stack(dsp.stereo_delay(C(npd[:, 0]), C(npd[:, 1]), SR, BT * 0.75, BT * 1.0, 0.4, 0.4, 0, 0, 1, 300, 5000, 0.1, 0.0, 0.2), 1)
npd = npd * 0.5 + nm(nv) * np.max(np.abs(npd)) * 0.6 + dl_ * 0.3                                       # N6: verb/delay blur
lpc = np.where(bar < S["drumsIn"], Np["lpIntro"], np.where((bar >= S["break"]) & (bar < S["back"]), 2500.0, Np["lpMain"]))  # N8: EQ automation
lpc = sm(lpc, 1500)
npd = np.stack([dsp.svf(C(npd[:, c]), C(lpc), 0.7, 0, SR) for c in range(2)], 1)
air = np.stack([np.tile(raw, N // ln + 1)[:N], np.roll(np.tile(raw, N // ln + 1)[:N], ln // 2)], 1); air = bw("low", Np["airLp"], bw("high", Np["airHp"], air, 2), 4)
airg = sm(np.where((bar >= S["drumsIn"]) & ~((bar >= S["break"]) & (bar < S["back"])), 1.0, 0.8), 1500)   # N8: more noise in main sections
npd = nm(npd); airL = air / np.std(air) * np.std(npd) * Np["airLevel"] * airg[:, None]   # air layer kept out of the duck (steady top)
# ================= B: punchy 808
Bp = R["bass808"]
def b808(m, lb):
    L = int(lb * BT * SR); tt_ = np.arange(L) / SR; f0 = hz(m)
    dive = 2 ** (Bp["diveSemis"] / 12 * np.exp(-tt_ / (Bp["diveMs"] / 1000)) * (tt_ < 0.2))                # B3: unipolar dive ends on the note
    ph = 2 * np.pi * np.cumsum(f0 * dive) / SR
    fm = Bp["fmIndex"] * np.exp(-tt_ / (Bp["fmMs"] / 1000)) * np.sin(ph * Bp["fmRatio"])                    # B7: FM ratio 0.5 transient
    y = np.sin(ph + fm) + Bp["h2"] * np.sin(2 * ph) + Bp["h3"] * np.sin(3 * ph)                             # B1-2: sine + 2nd/3rd partials
    u = tt_ / (L / SR); env = (1 - u ** 3) if Bp["decay"] == "convex" else (1 - u) ** 3                       # B5: convex = long sustain
    y = y * env * np.minimum(tt_ / 0.002, 1)
    y = bw("low", Bp["fmLp"], y, 2)
    y = np.tanh(y * Bp["clip1"]) / np.tanh(Bp["clip1"]); y = np.tanh(y * Bp["clip2"]) / np.tanh(Bp["clip2"])   # B8: two soft clips
    zc = np.where(np.diff(np.signbit(y)))[0]; e = zc[-1] if len(zc) else L; y = y[:e + 1]                     # B9: end on zero crossing
    fl = int(0.01 * SR); y[-fl:] *= np.linspace(1, 0, fl); return y
bass = np.zeros(N); kick = np.zeros(N); K = R["kick"]
def kick1():
    L = int(0.3 * SR); tt_ = np.arange(L) / SR; f = K["f1"] + (K["f0"] - K["f1"]) * np.exp(-tt_ / 0.03)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt_ / 0.09) * np.minimum(tt_ / 0.003, 1); y[-480:] *= np.linspace(1, 0, 480); return y
on = lambda b: S["drumsIn"] <= b < S["drumsOut"] and not (S["break"] <= b < S["back"])
for b in range(0, NB, 2):
    for (beat, m, lb) in Bp["notes"]:
        bb = b + beat / 4
        if on(int(bb)): put(bass, b808(m + 12 if m < 30 else m, lb), tb(b) + beat * BT); events += 1
for b in range(NB):
    if on(b):
        for q, v in enumerate(K["vel"]):
            if v: put(kick, kick1(), tb(b) + q * BT, v); events += 1
lowbus = bass * Bp["level"] + kick * K["level"]
pk = np.max(np.abs(lowbus)); lowbus = np.clip(lowbus, -0.9, 0.9)                                # B8: limiter-ish ceiling
# N8: sidechain duck of noise pad (and arp pad lightly) from the low bus
key = np.abs(bw("low", 150, lowbus, 2)); ke = key / (key.max() + 1e-9)
att = sm(ke, 3); duck = 1 - (1 - 10 ** (-Np["duckDb"] / 20)) * np.clip(sm(att, 180) * 3, 0, 1)
# ================= mix + master
Mm = R["master"]
mix = nm(pad) * A["level"] * (1 - 0.3 * (1 - duck))[:, None] + nm(npd) * Np["level"] * duck[:, None] + airL * Np["level"] + nm(fbl) * Fb["level"] + pan2(lowbus / 0.9, 0) * 0.85 / np.sqrt(2)
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
# skill checks
Sp = np.abs(np.fft.rfft(ns[:SR * 2])); fr_ = np.fft.rfftfreq(SR * 2, 1 / SR); pkf = fr_[np.argmax(Sp)]
one = b808(45, 1.6); O = np.abs(np.fft.rfft(one[int(0.1 * SR):int(0.5 * SR)], 1 << 16)); fo_ = np.fft.rfftfreq(1 << 16, 1 / SR)
hdb = [round(20 * np.log10(O[np.argmin(np.abs(fo_ - hz(45) * h))] / O[np.argmin(np.abs(fo_ - hz(45)))]), 1) for h in (2, 3)]
inst = np.diff(np.unwrap(np.angle(sg.hilbert(bw("low", 200, one, 4))))) * SR / 2 / np.pi
res["checks"] = {"side_below_120Hz_db": round(db(bw("low", 120, side, 4)) - db(bw("low", 120, mid, 4)), 1), "hf_spikes_over_8x": spikes,
  "hf_env_12_40_vs_0_12_db": round(10 * np.log10(Pw[(fq >= 12) & (fq <= 40)].mean() / Pw[(fq > 0.2) & (fq < 12)].mean()), 1),
  "noise_peak_hz": round(float(pkf), 1), "b808_h2_h3_db": hdb, "b808_pitch_after_60ms_cents": round(float(1200 * np.log2(np.median(inst[int(0.06 * SR):int(0.3 * SR)]) / hz(45))), 1),
  "b808_end_sample": float(one[-1]), "first_half_vs_second_half_lufs": round(meter.integrated_loudness(mix[:N // 2]) - meter.integrated_loudness(mix[N // 2:]), 1)}
json.dump(res, open(OUT + ".stats.json", "w"), indent=1, default=float)
print(json.dumps({"score": res["score"], "pass": res["pass"], "lufs": res["lufs"], "tp": res["extra"].get("true_peak_dbtp"), "gates": res["gates"], "subs": res["subs"], "tilt": res["extra"].get("tilt_db_oct"), "gr": round(gr_max, 2), "len": res["lengthSec"], "drumsIn": res["drumsInSec"], "checks": res["checks"]}, default=float))
