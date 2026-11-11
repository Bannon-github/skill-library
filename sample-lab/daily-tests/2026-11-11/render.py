#!/usr/bin/env python3
"""Daily 3-skill test 2026-11-11 "Tide Descent":
  monaural-beat-two-fixed-sines-or-tremolo-at-entrainment-rate-on-playable-pad-speaker-safe (M: tremolo pad + mono sine pair)
  + filtered-vibey-drum-bus-lowpass-1k-boxy-mid-tube-drive-borrowed-verb-sends-automated-long-plate-throws (D: drum bus)
  + sleep-descent-arrangement-40-50bpm-descending-lines-staggered-fade-ins-lowpass-recede-key-tuned-binaural-notch (S: arc)
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
def svf(x, fc, q, md):
    fc = C(np.clip(fc, 20, 0.45 * SR))
    return dsp.svf(C(x), fc, q, md, SR) if x.ndim == 1 else np.stack([dsp.svf(C(x[:, c]), fc, q, md, SR) for c in range(2)], 1)
def pan2(x, p): return np.stack([x * np.cos((p + 1) * np.pi / 4), x * np.sin((p + 1) * np.pi / 4)], 1) * np.sqrt(2)
def put(buf, y, s, g=1.0):
    i = int(round(s * SR)); L = min(len(y), N - i)
    if L > 0 and i >= 0:
        if y.ndim == 1 and buf.ndim == 2: buf[i:i+L] += y[:L, None] * g
        else: buf[i:i+L] += y[:L] * g
def verb(x, rt, seed, damp=9000.0, size=1.8, mod=0.2, diff=0.75, pre=0.02):
    l, r = dsp.fdn_reverb(C(x[:, 0]), C(x[:, 1]), SR, float(rt), size, damp, pre, mod, diff, 0.0, seed); return np.stack([l, r], 1)
def fade(y, ms=10, mi=0.0):
    y = y.copy(); n = max(1, int(ms * SR / 1000))
    if n < len(y): y[-n:] *= np.linspace(1, 0, n)[:, None] if y.ndim == 2 else np.linspace(1, 0, n)
    if mi:
        m = int(mi * SR / 1000); y[:m] *= np.linspace(0, 1, m)[:, None] if y.ndim == 2 else np.linspace(0, 1, m)
    return y
nm = lambda x: x / (np.max(np.abs(x)) + 1e-9)
def sm(x, ms): a = np.exp(-1 / (ms / 1000 * SR)); return lfilter([1 - a], [1, -a], x, axis=0)
def ramp(b0, bars): return np.clip((bar - b0) / bars, 0, 1)
def chorus(x, depth_ms=4.0, rate=0.3, base_ms=14.0):   # simple stereo chorus (modulated delay, opposite phase L/R)
    out = np.zeros_like(x); idx = np.arange(N)
    for c, ph in ((0, 0.0), (1, np.pi)):
        d = (base_ms + depth_ms * np.sin(2 * np.pi * rate * t + ph)) / 1000 * SR
        out[:, c] = np.interp(idx - d, idx, x[:, c], left=0.0)
    return out
events = 0
Ch = R["chords"]; Ro = R["roots"]; chord_at = lambda b: b % len(Ch)
# ===== S steps 4/6: receding cutoff curves (descent-only after the peak)
recede = ramp(S["recede"], S["end"] - S["recede"])
# ===== M option B steps 4-6: playable pad with tremolo at the entrainment rate (~40% shape, high amount)
P = R["pad"]; Tr = R["trem"]; pad = np.zeros((N, 2))
for b in range(NB):
    notes = Ch[chord_at(b)]; s0 = tb(b); L = int((BL + 2.5) * SR); tt = np.arange(L) / SR
    amp = np.clip(tt / 1.2, 0, 1) ** 1.5 * np.clip((BL + 2.5 - tt) / 2.5, 0, 1)
    y = np.zeros((L, 2))
    for j, m in enumerate(notes):
        for u, p in ((-1, -0.6), (1, 0.6)):
            fr = C(np.full(L, hz(m) * 2 ** (u * P["detuneCents"] / 1200)))
            y += pan2(dsp.osc_va(fr, 0, 0.5, rng.random(), SR) + 0.5 * dsp.osc_va(fr, 2, 0.5, rng.random(), SR), p * (0.7 + 0.1 * j))
    i0 = int(s0 * SR); i1 = min(N, i0 + L); y = y[: i1 - i0]
    cut = P["cutStart"] + (P["cutEnd"] - P["cutStart"]) * recede[i0:i1]
    pad[i0:i1] += svf(y, cut, 0.7, 0) * amp[: i1 - i0, None] / len(notes); events += 1
pad *= (ramp(0, 1.5) ** 1.5)[:, None]                                    # S step 3: pad fades in first
# S step 5: fixed low cut on the pad, its amount blended in as the bass enters
padHp = bw("high", P["lowCutHz"], pad, 2); blend = ramp(S["bassIn"], P["lowCutBlendBars"])[:, None]
pad = pad * (1 - blend) + padHp * blend
k = 1 + Tr["shape"] * 3; lfoT = np.tanh(k * np.cos(2 * np.pi * Tr["rateHz"] * t)) / np.tanh(k)   # cos so peaks align with sine-pair beat
trem = 1 - Tr["amount"] * (1 - (lfoT + 1) / 2)
pad = pad * trem[:, None]
# ===== M step 7 (optional): same tremolo on strings, lighter. Strings: descending in-key line (S step 2)
St = R["strings"]; strg = np.zeros((N, 2))
for b in range(S["strings"], NB):
    for h, m in enumerate(R["stringsLine"][chord_at(b)]):
        s0 = tb(b) + h * BL / 2; L = int((BL / 2 + 1.5) * SR); tt = np.arange(L) / SR
        y = sum(pan2(dsp.osc_va(C(np.full(L, hz(m) * 2 ** (d / 1200))), 0, 0.5, rng.random(), SR), p) for d, p in ((-6, -0.5), (0, 0), (6, 0.5))) / 3
        y = bw("low", 4500, y, 2) * (np.clip(tt / 0.6, 0, 1) * np.clip((BL / 2 + 1.5 - tt) / 1.5, 0, 1))[:, None]
        put(strg, y, s0); events += 1
strg = bw("high", 250, strg) * (ramp(S["strings"], 2) ** 2)[:, None] * (1 - St.get("tremAmt", R["trem"]["stringsAmount"]) * (1 - (lfoT + 1) / 2))[:, None]
# ===== S step 2: soft pluck with echo, descending arpeggio; cutoff recedes (step 4)
Pl = R["pluck"]; pl = np.zeros(N)
for b in range(S["pluck"], NB - 1):
    notes = sorted(Ch[chord_at(b)][1:], reverse=True)
    for q, m in enumerate(notes[:4]):
        L = int(1.2 * SR); tt = np.arange(L) / SR
        y = dsp.osc_va(C(np.full(L, hz(m + 12))), 2, 0.5, 0.0, SR) * np.exp(-tt / 0.35) * np.clip(tt / 0.004, 0, 1)
        put(pl, fade(y, 40), tb(b) + q * BT); events += 1
pl = svf(pl, Pl["cutStart"] + (Pl["cutEnd"] - Pl["cutStart"]) * recede, 0.7, 0) * ramp(S["pluck"], 1.5)
plS = pan2(pl, 0.15); plD = np.stack(dsp.stereo_delay(C(plS[:, 0]), C(plS[:, 1]), SR, 0.75 * BT, 0.75 * BT * 2, 0.4, 0.4, 0.1, 0.1, 1, 400, 3000, 0.1, 0.0, 0.2), 1)
plS = plS + 0.5 * plD
# ===== S step 2: warm woodwind (sine + filtered triangle + breath), steady pitch, descending
Wd = R["wood"]; wd = np.zeros(N)
for i, m in enumerate(R["woodLine"]):
    b = S["wood"] + i
    if b >= NB - 1: break
    L = int((BL + 0.8) * SR); tt = np.arange(L) / SR; f = C(np.full(L, hz(m)))
    y = 0.7 * dsp.osc_va(f, 3, 0.5, 0.0, SR) + 0.3 * bw("low", 1800, dsp.osc_va(f, 2, 0.5, 0.0, SR)) + 0.04 * bw("band", [1500, 4000], rng.standard_normal(L))
    y *= np.clip(tt / 0.5, 0, 1) * np.clip((BL + 0.8 - tt) / 0.8, 0, 1)
    put(wd, y, tb(b)); events += 1
wdS = pan2(bw("high", 200, wd), -0.2)
# ===== mono sub bass on descending roots (mono lows), slow fade-in (S step 3: bass-heavy parts slowest)
Bs = R["bass"]; bass = np.zeros(N)
for b in range(S["bassIn"], NB):
    L = int((BL + 1.0) * SR); tt = np.arange(L) / SR; f = hz(Ro[chord_at(b)])
    y = (np.sin(2 * np.pi * f * tt) + 0.15 * np.sin(4 * np.pi * f * tt)) * np.clip(tt / 0.4, 0, 1) * np.clip((BL + 1.0 - tt) / 1.0, 0, 1)
    put(bass, y, tb(b)); events += 1
bass = bw("low", 200, bass) * ramp(S["bassIn"], Bs["fadeBars"]) ** 2
# ===== S steps 7-8 / M steps 1-3: monaural pair at the key root (E4) and root-rate, centred, own fades; notch carved in pad/strings
To = R["tone"]; f1 = To["rootHz"]; f2 = f1 - To["rateHz"]
tone = 0.5 * (np.sin(2 * np.pi * f1 * t) + np.sin(2 * np.pi * f2 * t))
toneEnv = ramp(1, To["fadeBars"]) * (1 - ramp(S["toneOut"], S["end"] - S["toneOut"])); tone *= toneEnv
bn, an = sg.iirnotch((f1 + f2) / 2, To["notchQ"] * (f1 + f2) / 2 / 50, fs=SR)   # narrow notch spanning both tones
pad = sg.filtfilt(bn, an, pad, axis=0); strg = sg.filtfilt(bn, an, strg, axis=0)
# ===== existing returns (shared space): A = pitched/chorused 100% wet verb (pluck, wood), B = chorused hall with HP/LP on the wet (pad, strings)
Db = R["drumBus"]
# ----- D step 1: plain, thin synthesized kit (half-time at 48 BPM: kick 1 & 3+, snare 3, hats on 8ths - no rolls)
kit = np.zeros((N, 2)); plateSend = np.zeros(N)
def kick():
    L = int(0.45 * SR); tt = np.arange(L) / SR; f = 48 + 70 * np.exp(-tt / 0.03)
    return fade(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.18) * np.clip(tt / 0.002, 0, 1), 20)
def snare():
    L = int(0.35 * SR); tt = np.arange(L) / SR
    return fade(0.6 * np.sin(2 * np.pi * 190 * tt) * np.exp(-tt / 0.05) + bw("band", [900, 6000], rng.standard_normal(L)) * np.exp(-tt / 0.09), 20, 1.5)
def hat(): L = int(0.09 * SR); tt = np.arange(L) / SR; return fade(bw("high", 6000, rng.standard_normal(L)) * np.exp(-tt / 0.025) * np.clip(tt / 0.003, 0, 1), 10)
drumOn = lambda b: S["drumsIn"] <= b < S["drumsOut"]
for b in range(NB):
    if not drumOn(b): continue
    for q in (0, 2.5): put(kit, pan2(kick(), 0), tb(b) + q * BT, 0.9 if q == 0 else 0.6)
    put(kit, pan2(snare(), 0.05), tb(b) + 2 * BT, 0.7)
    for q in np.arange(0, 4, 0.5): put(kit, pan2(hat(), 0.25), tb(b) + q * BT, 0.25 if q % 1 else 0.35)
    events += 1
    # D step 6: plate send opens only at phrase ends (last beat of bars 3,7,11) and longer near section end (bar 7-8 peak)
    if b % 4 == 3: plateSend[int(tb(b + 0.75) * SR): int(tb(b + 1) * SR)] = 1.0
    if b == S["peak"] - 1: plateSend[int(tb(b + 0.5) * SR): int(tb(b + 1) * SR)] = 1.0
plateSend = sm(plateSend, 60)
# D step 2: low-pass ~1 kHz + broad 500 Hz-1 kHz boxy boost
db_ = bw("low", Db["lpHz"], kit, 2)
db_ = np.stack([dsp.eq(C(db_[:, c]), "peak", Db["boxHz"], 0.6, Db["boxDb"]) for c in range(2)], 1)
# D step 3: gentle tube-style saturation (asymmetric, minimal tone)
pk = np.max(np.abs(db_)); x = db_ / pk * Db["drive"]; db_ = (np.tanh(x + 0.1) - np.tanh(0.1)) / Db["drive"] * pk
# D step 7: bus gain (utility) rises gently into the section end (peak), then the S descent takes over (drums fade out by drumsOut)
busG = 10 ** (Db["riseDb"] * ramp(S["drumsIn"], S["peak"] - S["drumsIn"]) / 20) * (1 - 0.6 * ramp(S["recede"], S["drumsOut"] - S["recede"]))
db_ = db_ * busG[:, None] * ramp(S["drumsIn"], 0.5)[:, None]
# returns fed by their owners + drum sends (D steps 4-5)
retA_in = 0.6 * plS + 0.6 * wdS + Db["sendA"] * db_
retB_in = 0.5 * pad + 0.6 * strg + Db["sendB"] * db_
retA = verb(bw("high", 300, chorus(retA_in, 3.0, 0.4)), 3.2, 41, 6000.0, 1.6, 0.3)
retA = retA + 0.3 * chorus(retA, 6.0, 0.2, 20.0)                                    # pitched/chorused wet
retB = verb(chorus(retB_in, 4.0, 0.25), 5.5, 43, 5000.0, 2.2, 0.25)
retB = bw("low", 4500, bw("high", 280, retB))                                     # heavy EQ on the hall wet itself
plate = verb(bw("high", Db["plateLowCut"], db_ * plateSend[:, None] * Db["plateSend"], 4), Db["plateRt"], 47, 4000.0, 2.0, 0.2)
plate = bw("high", Db["plateLowCut"], plate, 2)
# ===== mix + S step 6 long master recede + master
Mm = R["master"]
mix = pad * P["level"] + strg * St["level"] + plS * Pl["level"] + wdS * Wd["level"] + pan2(bass, 0) * Bs["level"] \
    + db_ * Db["level"] + nm(retA) * 0.10 + nm(retB) * 0.16 + nm(plate) * 0.08 * Db["level"] + pan2(tone, 0) * To["level"]
mix = sg.sosfiltfilt(sg.butter(2, 22, "high", fs=SR, output="sos"), mix, axis=0)
Mn = 0.5 * (mix[:, 0] + mix[:, 1]); Sd = 0.5 * (mix[:, 0] - mix[:, 1])
Sd = sg.sosfiltfilt(sg.butter(4, Mm["sideHpHz"], "high", fs=SR, output="sos"), Sd) * Mm["width"]
mix = np.stack([Mn + Sd, Mn - Sd], 1)
mix *= (10 ** (Mm["recedeDb"] * recede / 20))[:, None]
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
res["events"] = events; res["lengthSec"] = round(T, 2); res["lufs"] = round(meter.integrated_loudness(mix), 2); res["drumsInSec"] = round(tb(S["drumsIn"]), 2)
side = 0.5 * (mix[:, 0] - mix[:, 1]); mid = 0.5 * (mix[:, 0] + mix[:, 1])
db = lambda x: 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)
hf = bw("high", 8000, mid, 4); he = np.abs(hf); spikes = int(np.sum(he > 8 * (sm(he, 50) + 1e-9)))
ed = sm(he, 5)[::480]; fq, Pw = sg.welch(ed - ed.mean(), fs=100, nperseg=1024)
# tremolo/beat check: envelope modulation of the mid around the 6 Hz target vs neighbours
env = sm(np.abs(bw("band", [200, 2000], mid, 2)), 8)[::480]; fq2, P2 = sg.welch(env - env.mean(), fs=100, nperseg=2048)
rate = To["rateHz"]; band = (fq2 > rate - 0.3) & (fq2 < rate + 0.3); nb = ((fq2 > rate - 2) & (fq2 < rate - 0.8)) | ((fq2 > rate + 0.8) & (fq2 < rate + 2))
# drum-bus darkness: share of drum bus energy above 2 kHz
res["checks"] = {"side_below_120Hz_db": round(db(bw("low", 120, side, 4)) - db(bw("low", 120, mid, 4)), 1), "hf_spikes_over_8x": spikes,
  "hf_env_12_40_vs_0_12_db": round(10 * np.log10(Pw[(fq >= 12) & (fq <= 40)].mean() / Pw[(fq > 0.2) & (fq < 12)].mean()), 1),
  "pulse_6Hz_vs_neighbours_db": round(10 * np.log10(P2[band].max() / P2[nb].mean()), 1),
  "drumbus_above_2k_vs_raw_db": round(db(bw("high", 2000, db_[:, 0], 4)) - db(db_[:, 0]) - (db(bw("high", 2000, kit[:, 0], 4)) - db(kit[:, 0])), 1),
  "first_half_vs_second_half_lufs": round(meter.integrated_loudness(mix[:N // 2]) - meter.integrated_loudness(mix[N // 2:]), 1)}
json.dump(res, open(OUT + ".stats.json", "w"), indent=1, default=float)
print(json.dumps({"score": res["score"], "pass": res["pass"], "lufs": res["lufs"], "tp": res["extra"].get("true_peak_dbtp"), "gates": res["gates"], "subs": res["subs"], "tilt": res["extra"].get("tilt_db_oct"), "gr": round(gr_max, 2), "len": res["lengthSec"], "drumsIn": res["drumsInSec"], "checks": res["checks"]}, default=float))
