#!/usr/bin/env python3
"""Daily 3-skill test 2026-11-18 "Ladder Pulse" (D minor, 96 BPM):
  P noof-synth-pulse-noise-saw-octave-unison-saw-closed-ladder-env-cutoff-energy-macro (noise + saw + 8va 5-voice unison saw
    -> one closed LP24 ladder opened per 8th by a fast env; one cutoff macro lane = energy)
  W width-by-juxtaposition-ms-sides-reverb (narrow sections before wide ones, two different lead takes panned ~30,
    mono-safe bed: M/S EQ mid -30 dB send -> reverb, dry centre untouched, light drum duck on wide layers)
  T organic-tension-from-track-sounds (build: only osc B glides up, irregular-length chorused lead loop faded in,
    ducked to dry lead and pitched up steadily, 100%-wet 1/8 delay return revealed by fader w/ rising fb, cut before drop)
usage: render.py recipe.json out.wav"""
import sys, os, json, numpy as np, soundfile as sf, pyloudnorm as pyln
from scipy import signal as sg
from scipy.signal import lfilter
LAB = os.environ.get("LAB", "/workspace/skill-library/sample-lab"); sys.path.insert(0, LAB + "/engine")
import dsp, metrics
SR = 48000
R = json.load(open(sys.argv[1])); OUT = sys.argv[2]; rng = np.random.default_rng(R["seed"])
NB = R["bars"]; BL = 240 / R["bpm"]; BT = BL / 4; E8 = BT / 2; tb = lambda x: x * BL; S = R["sections"]
T = NB * BL + R["tailSec"]; N = int(T * SR); t = np.arange(N) / SR; bar = t / BL
hz = lambda m: 440 * 2 ** ((m - 69) / 12); C = np.ascontiguousarray
def bw(k, f, x, o=2): return sg.sosfilt(sg.butter(o, f, k, fs=SR, output="sos"), x, axis=0)
def pan2(x, p):
    p = np.asarray(p); return np.stack([x * np.cos((p + 1) * np.pi / 4), x * np.sin((p + 1) * np.pi / 4)], 1) * np.sqrt(2)
def put(buf, y, s, g=1.0):
    i = int(round(s * SR)); L = min(len(y), len(buf) - i)
    if L > 0 and i >= 0: buf[i:i+L] += y[:L] * g
def verb(x, rt, seed, damp=9000.0, size=1.8, mod=0.15, diff=0.75, pre=0.02):
    l, r = dsp.fdn_reverb(C(x[:, 0]), C(x[:, 1]), SR, float(rt), size, damp, pre, mod, diff, 0.0, seed); return np.stack([l, r], 1)
nm = lambda x: x / (np.max(np.abs(x)) + 1e-9)
def sm(x, ms): a = np.exp(-1 / (ms / 1000 * SR)); return lfilter([1 - a], [1, -a], x, axis=0)
def osc(f, L, shape=0, ph=0.0): return dsp.osc_va(np.full(L, float(f)), shape, 0.5, ph, SR)
def gate(b0, b1, xf_ms=300): return sm(((bar >= b0) & (bar < b1)).astype(float), xf_ms)
def ramp(pts):  # piecewise-linear automation in bars (smooth macro ride)
    b, v = zip(*pts); return np.interp(bar, b, v)
def env_ar(L, a, rel_at, rel):
    tt_ = np.arange(L) / SR
    return np.sin(np.pi / 2 * np.clip(tt_ / a, 0, 1)) ** 2 * np.where(tt_ < rel_at, 1.0, np.cos(np.pi / 2 * np.clip((tt_ - rel_at) / rel, 0, 1)) ** 2)
def resamp(x, ratio):  # repitch (non time-locked): ratio<1 -> slower + lower
    n = int(len(x) / ratio); return np.interp(np.arange(n) * ratio, np.arange(len(x)), x)
events = 0
CH = R["chords"]; chord = lambda b: min(int(b), NB - 1) % 4
P = R["pulse"]; W = R["width"]; TN = R["tension"]; LV = R["levels"]
bS, bD = S["buildStart"], S["drop"]
inbuild = lambda b: bS <= b < bD
# ================= pad (support): two detuned saws, LP 1.8k, slow env, verb
pad = np.zeros((N, 2))
for b in range(NB):
    for i, m in enumerate(CH["upper"][chord(b)]):
        L = int((BL + 1.2) * SR)
        for dc, p in ((-6, -0.5), (6, 0.5)):
            y = osc(hz(m) * 2 ** (dc / 1200), L, 0, (i * 0.3 + dc) % 1) * env_ar(L, 0.9, BL - 0.2, 1.3)
            put(pad, pan2(y, p), tb(b), 0.25)
pad = bw("low", 1800, bw("high", 150, pad, 2), 2); pad = nm(pad) * 0.7 + nm(verb(pad, 5.0, 11, 6000.0, 2.0)) * 0.5
# ================= P: NOOF pulse
macro = ramp(P["cutoffMacro"])
glide = np.where(bar < bS, 0.0, np.where(bar < bD, (bar - bS) / (bD - bS), 0.0)) * TN["oscBGlideSt"]  # T: osc B only
f0 = np.zeros(N); gtrig = np.zeros(N); on = np.zeros(N)
for b in range(S["drumsIn"], NB):
    root = CH["bass"][chord(b)] + 12
    for k, iv in enumerate(P["line"]):
        s = int((tb(b) + k * E8) * SR); e = int((tb(b) + (k + 1) * E8) * SR)
        f0[s:e] = hz(root + iv); gtrig[s] = 1; on[s:e] = 1; events += 1
f0[f0 == 0] = hz(50)
oa = dsp.osc_va(C(f0), 0, 0.5, 0.0, SR)
ob = np.zeros(N)
for u in range(P["unison"]):
    dc = P["oscBDetuneC"] + (u - (P["unison"] - 1) / 2) / ((P["unison"] - 1) / 2) * P["uniSpreadC"] / 2
    ob += dsp.osc_va(C(f0 * 2 * 2 ** ((dc + 100 * glide) / 1200)), 0, 0.5, (u * 0.21) % 1, SR) / P["unison"]
nz = bw("low", 9000, dsp.noise(N, "white", rng), 2) * P["noiseLvl"] / 0.3
src = oa * 0.6 + ob * 0.55 + nz
# per-note filter env (fast attack, quick decay) retriggered each 8th
idx = np.flatnonzero(gtrig); since = np.zeros(N)
last = np.maximum.accumulate(np.where(gtrig > 0, np.arange(N), 0)); since = (np.arange(N) - last) / SR
fenv = np.clip(since / (P["envAtkMs"] / 1000), 0, 1) * np.exp(-np.maximum(since - P["envAtkMs"] / 1000, 0) / (P["envDecMs"] / 1000))
fc = P["baseHz"] * 2 ** (macro * P["macroOctaves"] + fenv * P["envOctaves"] * (0.4 + 0.6 * macro))
fc = np.clip(sm(fc, 1.5), 30, 16000)
pul = dsp.ladder(C(src), C(fc), P["res"], 1.2, 0, 0, SR)
amp = sm(sm(on, 4), 4) * (0.55 + 0.45 * np.exp(-since / 0.25)); pul = pul * amp
pul = bw("high", 90, pul, 2)
pulS = pan2(nm(pul), 0)
pulS = pulS * 0.85 + nm(verb(pan2(pul, 0), 2.2, 19, 7000.0, 1.6)) * 0.3
# ================= lead: two different takes (W), take A saw-tri LP 2.6k, take B pulse LP 3.4k + 9 ms later
def lead_take(shape, lp, off):
    y = np.zeros(N)
    for b0, m, nb in R["melody"]:
        L = int((nb * BL + 0.8) * SR)
        z = dsp.osc_va(np.full(L, hz(m)), shape, 0.42, 0.1 * shape, SR) * env_ar(L, 0.12, nb * BL - 0.15, 0.7)
        put(y, z, tb(b0) + off)
    return bw("low", lp, bw("high", 200, y, 2), 2)
tA = lead_take(0, 2600, 0.0); tB = lead_take(1, 3400, W["takeBOffsetMs"] / 1000)
for b0, m, nb in R["melody"]: events += 2
leadS = pan2(nm(tA), -W["doublePan"]) + pan2(nm(tB), W["doublePan"])
leadS = leadS + nm(verb(leadS, 3.2, 29, 6500.0, 1.8)) * 0.35
dryLead = 0.5 * (tA + tB)
# ================= bass (support): sine + soft 2nd, root per bar
bass = np.zeros(N)
for b in range(S["drumsIn"], S["drumsOut"]):
    L = int(BL * SR); f = hz(CH["bass"][chord(b)] - 12); tt_ = np.arange(L) / SR
    y = (np.sin(2 * np.pi * f * tt_) + 0.25 * np.sin(4 * np.pi * f * tt_)) * env_ar(L, 0.02, BL - 0.08, 0.08); put(bass, y, tb(b)); events += 1
# ================= T: irregular-length chorused loop of the lead, pitched up steadily through the build
src_s = int(tb(TN["loopSrcBar"]) * SR); Ls = int(TN["loopSec"] * SR); seg = dryLead[src_s:src_s + Ls].copy()
fw = int(0.02 * SR); seg[:fw] *= np.linspace(0, 1, fw); seg[-fw:] *= np.linspace(1, 0, fw)
loop = np.zeros(N); tpos = tb(bS); nrep = int((tb(bD) - tb(bS)) / TN["loopSec"]) + 1
for k in range(nrep):
    st = TN["loopUpSt"] * k / max(nrep - 1, 1); y = resamp(seg, 2 ** (st / 12))
    put(loop, y, tpos + k * TN["loopSec"]); events += 1
loop *= gate(bS, bD, 40) * ramp([(bS, 0.0), (bD - 0.5, 1.0), (bD, 1.0)])
loop = bw("low", 1500 + 4000 * np.clip((bar - bS) / 4, 0, 1).mean(), bw("high", 300, loop, 2), 2)
loopL, loopR = dsp.chorus(C(loop), C(loop), SR, 0, 0.6, 6.0, 12.0, 0.1, 1.0, TN["loopChorus"], 0.0, 0.0)
loopS = np.stack([loopL, loopR], 1)
le = sm(sm(np.abs(dryLead), 5), 120); le /= le.max() + 1e-9
loopS *= (1 - (1 - 10 ** (-TN["loopDuckDb"] / 20)) * np.clip(le * 2, 0, 1))[:, None]
# T: 1/8 delay return, 100% wet, send full; reveal by return fader, rising feedback, cut before drop
d = int(E8 * SR); fbk = ramp([(bS, TN["delayFb"][0]), (bD, TN["delayFb"][1])])
send = dryLead + 0.6 * loop; wet = np.zeros(N)
for k in range(1, 9):
    y = np.zeros(N); y[k * d:] = send[:-k * d]; wet += fbk ** (k - 1) * y * (0.5 if k % 2 == 0 else 1.0)
wet = bw("low", 4500, bw("high", 350, wet, 2), 2)
wet *= ramp(TN["returnPts"]) * (1 - 0.5 * np.clip(le * 2, 0, 1))
dlyS = np.stack([np.roll(wet, 0), np.roll(wet, int(0.011 * SR))], 1)
# ================= support drums (not under test; Matt: beat in by ~8 counts) -- kick 1&3, soft snare 2&4, soft offbeat shaker
DM = R["drums"]
def kick1():
    L = int(0.5 * SR); tt_ = np.arange(L) / SR; f = 50 + 70 * np.exp(-tt_ / 0.035)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt_ / 0.28) * np.minimum(tt_ / 0.004, 1); y = bw("low", 250, y, 4); y[-2400:] *= np.linspace(1, 0, 2400); return y
def snare1():
    L = int(0.4 * SR); tt_ = np.arange(L) / SR
    y = 0.5 * np.sin(2 * np.pi * 185 * tt_) * np.exp(-tt_ / 0.06) + bw("band", [1200, 5000], rng.standard_normal(L), 2) * np.exp(-tt_ / 0.09)
    y *= np.minimum(tt_ / 0.004, 1); y = bw("low", 6000, y, 2); y[-480:] *= np.linspace(1, 0, 480); return y
def shaker1():
    L = int(0.14 * SR); tt_ = np.arange(L) / SR
    y = rng.standard_normal(L) * np.minimum(tt_ / 0.015, 1) * np.exp(-tt_ / 0.04); y[-240:] *= np.linspace(1, 0, 240); return y
kick = np.zeros(N); sn = np.zeros(N); shk = np.zeros(N); k1 = kick1()
drum_on = lambda b: S["drumsIn"] <= b < S["drumsOut"]
for b in range(NB):
    if not drum_on(b): continue
    for q in (0, 2): put(kick, k1, tb(b) + q * BT); events += 1
    if inbuild(b): continue
    for q in (1, 3): put(sn, snare1(), tb(b) + q * BT); events += 1
    if b >= S["leadIn"]:
        for q in range(4): put(shk, shaker1(), tb(b) + (q + 0.5) * BT); events += 1
snS = pan2(sn, 0.05); snS = nm(snS) * 0.6 + nm(verb(snS, 3.0, 37, 6000.0, 2.0)) * 0.5
shS = pan2(bw("high", 5000, bw("low", 10000, shk, 2), 2), 0.2); shS = nm(shS) * 0.6 + nm(verb(shS, 3.0, 41, 7000.0, 2.0)) * 0.4
dbus = pan2(nm(kick), 0) / np.sqrt(2) * DM["kick"] + snS * DM["snare"] + shS * DM["shaker"]
kenv = sm(sm(np.abs(kick), 5), 90); kenv /= kenv.max() + 1e-9
duck = lambda d: (1 - (1 - 10 ** (-d / 20)) * np.clip(kenv * 2.5, 0, 1))[:, None]

# in the build keep kick only (tension), drop returns full
# ================= W: mono-safe sides bed (pad + bass + pulse send -> M/S, mid -30 dB -> reverb) + juxtaposed width
bedsrc = pad * 0.6 + pulS * 0.4 + pan2(bass, 0) * 0.3
bm = 0.5 * (bedsrc[:, 0] + bedsrc[:, 1]) * 10 ** (W["msMidCutDb"] / 20); bsd = 0.5 * (bedsrc[:, 0] - bedsrc[:, 1])
bed = np.stack([bm + bsd, bm - bsd], 1)
bed = verb(bed, W["sidesVerbRt"], 53, 7000.0, 2.2); bm2 = 0.5 * (bed[:, 0] + bed[:, 1]); bs2 = 0.5 * (bed[:, 0] - bed[:, 1])
bed = np.stack([bm2 * 0.15 + bs2, bm2 * 0.15 - bs2], 1); bed = nm(bed) * W["sidesSend"]
wid = ramp(W["widthPts"])
def setw(x, w):
    m = 0.5 * (x[:, 0] + x[:, 1]); s = 0.5 * (x[:, 0] - x[:, 1]) * w; return np.stack([m + s, m - s], 1)
if os.environ.get("DBG"):
    def spk(x):
        x = x.mean(1) if x.ndim == 2 else x; he = np.abs(bw("high", 8000, x, 4)); return int(np.sum(he > 8 * (sm(he, 50) + 1e-9)))
    for nmx, x in (("pad", pad), ("pulse", pulS), ("lead", leadS), ("loop", loopS), ("dly", dlyS), ("bed", bed), ("drums", dbus)): print(nmx, spk(x))
    sys.exit()
Mm = R["master"]
wideL = (leadS * LV["lead"] + bed * LV["bed"] * gate(S["leadIn"], S["drumsOut"] + 2, 800)[:, None] + loopS * LV["loop"] + dlyS * LV["delayRet"]) * duck(W["drumSideDuckDb"])
padW = setw(nm(pad) * LV["pad"] * duck(2.0), np.minimum(wid, 1.0))
wideW = setw(wideL, wid)
mix = padW + wideW + setw(nm(pulS) * LV["pulse"] * duck(1.5), np.minimum(wid, 1.0)) + pan2(nm(bass) * LV["bass"], 0) / np.sqrt(2) + dbus
mix = sg.sosfiltfilt(sg.butter(2, 22, "high", fs=SR, output="sos"), mix, axis=0)
Mn = 0.5 * (mix[:, 0] + mix[:, 1]); Sd = 0.5 * (mix[:, 0] - mix[:, 1])
Sd = sg.sosfiltfilt(sg.butter(4, Mm["sideHpHz"], "high", fs=SR, output="sos"), Sd)
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
  "lufs_intro_A_B_build_C_outro": [round(meter.integrated_loudness(sec(a, b)), 1) for a, b in ((0, 4), (4, 12), (12, 20), (20, 24), (24, 30), (30, 32))]}
json.dump(res, open(OUT + ".stats.json", "w"), indent=1, default=float)
print(json.dumps({"score": res["score"], "pass": res["pass"], "lufs": res["lufs"], "tp": res["extra"].get("true_peak_dbtp"), "gates": res["gates"], "subs": res["subs"], "tilt": res["extra"].get("tilt_db_oct"), "gr": round(gr_max, 2), "len": res["lengthSec"], "drumsIn": res["drumsInSec"], "checks": res["checks"]}, default=float))
