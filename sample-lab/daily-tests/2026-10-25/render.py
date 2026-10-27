#!/usr/bin/env python3
"""Daily 3-skill test 2026-10-25: modal partial resonator voices -> sample-and-hold as processor -> emotional cinematic arc.
usage: render.py recipe.json out.wav   (original synthesis, deterministic)"""
import sys, os, json, numpy as np, soundfile as sf, pyloudnorm as pyln
from scipy import signal as sg
LAB = os.environ.get("LAB", "/workspace/skill-library/sample-lab"); sys.path.insert(0, LAB + "/engine")
import dsp, metrics
SR = 48000
R = json.load(open(sys.argv[1])); OUT = sys.argv[2]
rng = np.random.default_rng(R["seed"])
bar = 4 * 60 / R["bpm"]; beat = bar / 4; T = R["bars"] * bar + R["tailSec"]; N = int(T * SR); t = np.arange(N) / SR
hz = lambda m: 440 * 2 ** ((m - 69) / 12); S_ = R["sections"]; MD = R["modal"]; SH = R["sh"]; ARC = R["arc"]
def bars(a, b): return int(a * bar * SR), min(N, int(b * bar * SR))
# ---------------- modal partial models (skill A step 2)
def ratios(model, n):
    k = np.arange(1, n + 1)
    if model == "string" or model == "tube": return k.astype(float)
    if model == "vibraphone": return np.array([1, 3.98, 10.6, 14.2, 18.6, 24.0][:n])
    if model == "beam": return np.array([1, 2.756, 5.404, 8.933, 13.34, 18.64][:n])
    if model == "membrane": return np.array([1, 1.594, 2.136, 2.296, 2.653, 2.918][:n])
def bank(f0, p, L, vel=1.0, hitpos=None, tone=0.0, lfo=None):
    """sum of decaying partials; material = decay-vs-frequency, tone = level tilt, hit = random emphasis, inharm = stretch"""
    r = ratios(p["model"], p["partials"]); r = 1 + (r - 1) * p.get("inharm", 1.0)          # step 3 inharmonic multiplier
    f = f0 * r; keep = f < 18000; f, r = f[keep], r[keep]
    mat = p["material"] * (1 - MD["velocity"]["toMaterial"] * (vel - 0.5))                    # step 7 louder = brighter
    tau = p["decay"] * r ** (-mat)                                                            # step 3 material
    amp = r ** (p.get("tone", 0.0) + tone)                                                    # step 3 tone (level only)
    if hitpos is not None: amp *= 1 + p.get("hit", 0) * (np.abs(np.sin(np.pi * np.arange(1, len(r) + 1) * hitpos)) * 2 - 1)  # step 3 hit
    tt = np.arange(L) / SR; ph = 2 * np.pi * np.outer(tt, f)
    if lfo is not None: ph *= (1 + lfo[:L, None])
    y = (np.sin(ph) * amp * np.exp(-tt[:, None] / tau)).sum(1)
    return y / (np.sum(np.abs(amp)) + 1e-9)
def exciter(kind, vel):
    L = int({"impulse": 0.002, "long": 0.012, "noise": 0.03}[kind] * SR); e = rng.standard_normal(L) * np.hanning(L)
    if kind == "impulse": e = np.hanning(L)
    b, a = sg.butter(1, (3000 + 9000 * vel) / (SR / 2)); return sg.lfilter(b, a, e) * (1 - MD["velocity"]["toExciter"] * (1 - vel))
def mallet(name, midi, vel, hitpos):
    p = MD[name]; f0 = hz(midi); L = int(min(p["decay"] * 5, 6) * SR)
    lfo = None
    if "lfoHz" in p and R.get("vibeLfo", True): lfo = (2 ** (p["lfoCents"] / 1200) - 1) * np.sin(2 * np.pi * p["lfoHz"] * np.arange(L) / SR)  # vibraphone pitch LFO
    tone = MD["randomTone"] * rng.uniform(-1, 1)                                               # subtle random tone
    y = bank(f0, p, L, vel, hitpos, tone, lfo)
    if "r2" in p: y = (1 - p["r2"]["blend"]) * y + p["r2"]["blend"] * bank(f0, p["r2"], L, vel, rng.random())  # step 5 parallel
    y = np.convolve(y, exciter(p["exciter"], vel))[:L]
    tt = np.arange(L) / SR; env = 1 + MD["attackEnvBoost"] * np.exp(-tt / 0.04)               # env1 fast attack over tail
    y *= env; y[-int(0.02*SR):] *= np.linspace(1, 0, int(0.02*SR))
    kg = 10 ** (MD["keyGainDbPerOct"] * (midi - 60) / 12 / 20)                                 # key -> layer gain
    return y * p["level"] * (1 - MD["velocity"]["toLevel"] * (1 - vel)) * kg
def tick(vel):
    p = MD["tick"]; f0 = hz(p["midi"]); L = int(0.35 * SR)
    r1 = bank(f0, p["r1"], L, vel, rng.random()); r1 = np.convolve(r1, exciter("noise", vel))[:L]
    h2 = bank(f0 * 0.5, p["r2"], L, vel)                                                      # step 5 series R1 -> R2 (tube)
    y = sg.fftconvolve(r1, h2)[:L] * 0.05; y += p["crossFb"] * r1                            # light cross-feed
    y[-int(0.01*SR):] *= np.linspace(1, 0, int(0.01*SR)); return y * p["level"]
def place(buf, y, sec, pan=0.0):
    i = int(sec * SR); e = min(N, i + len(y)); g = np.array([np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)]) * np.sqrt(2)
    buf[i:e] += y[:e - i, None] * g
# ---------------- sample-and-hold as processor (skill B)
def sh(inp_fn, sh_rate):
    """sample inp at instants set by integrating sh_rate (Hz per sample); hold between"""
    ph = np.cumsum(sh_rate) / SR; idx = np.flatnonzero(np.diff(np.floor(ph)) > 0) + 1; idx = np.r_[0, idx]
    held = np.repeat(inp_fn[idx], np.diff(np.r_[idx, N])); return held
chord_at = lambda b: R["chords"][int(b) % 4]
dry = np.zeros((N, 2)); verb_send = np.zeros((N, 2))
# mallet S&H: slow sine LFO stepped by S&H -> per-note hit position (keeps regularity, random-feeling steps)
mlfo = 0.5 + 0.5 * np.sin(2 * np.pi * SH["mallet"]["lfoHz"] * t); mhit = sh(mlfo, np.full(N, SH["mallet"]["shHz"]))
# ---------------- arc (skill C)
# intro: transparent warm pad that appears from nowhere, no melody
pad = np.zeros((N, 2))
for b in range(R["bars"] - 1):
    i0, i1 = bars(b, b + 1.15); L = i1 - i0; tt = np.arange(L) / SR
    for j, m in enumerate(chord_at(b)):
        for d, side in ((-R.get("padDetune", 6), 0), (R.get("padDetune", 6), 1)):
            f = hz(m) * 2 ** (d / 1200); ph = rng.random() * 6.28
            x = 0.6 * np.sin(2*np.pi*f*tt + ph) + 0.25 * np.sin(4*np.pi*f*tt + ph) + 0.12 * np.sin(6*np.pi*f*tt + ph)
            w = np.clip(tt / 0.8, 0, 1) * np.clip((L / SR - tt) / 0.5, 0, 1)
            pad[i0:i1, side] += x * w * 0.18
lowpad = np.zeros(N)
for b in range(R["bars"] - 1):
    i0, i1 = bars(b, b + 1.15); L = i1 - i0; tt = np.arange(L) / SR; m = chord_at(b)[0] - 12
    lowpad[i0:i1] += (np.sin(2*np.pi*hz(m)*tt) + 0.3*np.sin(4*np.pi*hz(m)*tt)) * np.clip(tt/0.8,0,1) * np.clip((L/SR-tt)/0.5,0,1)
padenv = (0.2 + 0.8 * np.clip(t / (ARC["padFadeInBars"] * bar), 0, 1)) * (0.6 + 0.4 * np.clip((t - 12*bar) / (2*bar), 0, 1))
padenv *= 0.08 + 0.92 * np.clip((R["bars"] * bar - t) / (ARC["outroFadeBars"] * bar), 0, 1)
dry += pad * padenv[:, None] * 0.7; dry += (lowpad * padenv * R.get("lowPadLevel", 0.0))[:, None]; verb_send += pad * padenv[:, None] * 0.5
if R.get("lowMidLevel", 0):  # v2: fill 150-400 Hz hole with steady chord-tone pad an octave down
    lm = np.zeros(N)
    for b in range(R["bars"] - 1):
        i0, i1 = bars(b, b + 1.15); L = i1 - i0; tt = np.arange(L) / SR
        for m in chord_at(b): lm[i0:i1] += (np.sin(2*np.pi*hz(m-12)*tt) + 0.2*np.sin(4*np.pi*hz(m-12)*tt)) * np.clip(tt/0.8,0,1) * np.clip((L/SR-tt)/0.5,0,1)
    dry += (lm * padenv * R["lowMidLevel"])[:, None]
# sub root, mono, enters build
sub = np.zeros(N)
for b in range(4, 19):
    i0, i1 = bars(b, b + 1); L = i1 - i0; tt = np.arange(L) / SR
    sub[i0:i1] += np.sin(2*np.pi*hz(chord_at(b)[0] - 12)*tt) * np.clip(tt/0.05, 0, 1) * np.clip((L/SR - tt)/0.05, 0, 1)
subenv = np.clip((t - 4*bar) / (2*bar), 0, 1) * np.clip((18.5*bar - t) / (2*bar), 0, 1) * (0.7 + 0.3*np.clip((t - 12*bar)/bar, 0, 1))
dry += (sub * subenv * R.get("subLevel", 0.22))[:, None]
# build: harp arpeggio (string model) forward/backward over chord tones, little by little
events = 0
for b in range(4, 18):
    ch = chord_at(b); notes = [ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[0] + 24]; seq = notes + notes[::-1][1:-1] + [notes[1]]
    dens = 4 if b < 8 else 8; vbase = 0.5 + 0.3 * np.clip((b - 4) / 8, 0, 1) * (0.6 if b >= 16 else 1)
    for k in range(dens):
        s = b * bar + k * bar / dens; m = seq[(k * 8 // dens) % len(seq)]
        y = mallet("harp", m, vbase * rng.uniform(0.85, 1), rng.random() * MD["randomHit"]); events += 1
        place(dry, y, s, 0.35 if k % 2 else -0.35); place(verb_send, y * 0.6, s)
# angelic-wind swell: one-note soft lead, tremolo, volume automation, octave-up double
i0, i1 = bars(*ARC["swellBars"]); L = i1 - i0; tt = np.arange(L) / SR
sw = np.sin(np.pi * tt / (L / SR)) ** 2 * (1 - R.get("tremoloDepth", 0.25) + R.get("tremoloDepth", 0.25) * np.sin(2*np.pi*ARC["tremoloHz"]*tt))
lead = (np.sin(2*np.pi*hz(ARC["swellMidi"])*tt) + 0.4*np.sin(2*np.pi*hz(ARC["swellMidi"]+12)*tt) + 0.08*np.sin(6*np.pi*hz(ARC["swellMidi"])*tt)) * sw * 0.12
dry[i0:i1] += lead[:, None] * 0.5; verb_send[i0:i1] += lead[:, None] * 0.8
# climax (written first): melody from chord arpeggios, edited to stepwise line, on modal vibraphone (parallel beam)
raw = []
for b in range(12, 16):
    ch = chord_at(b); arp = [ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[1] + 24 - 12]
    raw += arp if b % 2 == 0 else arp[::-1]
mel = [raw[0] + 12]
for m in raw[1:]:                                                     # edit pass: keep leaps <= 5 semitones, stay near register
    c = m + 12
    while c - mel[-1] > 5: c -= 12
    while mel[-1] - c > 5: c += 12
    mel.append(c)
rhythm = [0, 1.5, 2, 3]                                                # dotted, singing feel
for n, m in enumerate(mel):
    b = 12 + n // 4; s = b * bar + rhythm[n % 4] * beat
    y = mallet("vibe", m, 0.85 + 0.15 * (n % 4 == 0), mhit[int(s * SR)] * SH["mallet"]["toHit"] + 0.2); events += 1
    place(dry, y, s, 0.1 * np.sin(n)); place(verb_send, y * 0.7, s)
# strings: sustained climax chords with vibrato faded in
i0, i1 = bars(12, 17); L = i1 - i0; tt = np.arange(L) / SR; strings = np.zeros(L)
vib = np.clip(tt / (ARC["vibratoFadeBars"] * bar), 0, 1) * R.get("stringVib", 0.004) * np.sin(2*np.pi*5.2*tt)
for k in range(L // int(bar * SR) + 1):
    a0 = k * int(bar * SR); a1 = min(L, a0 + int(bar * SR * 1.1))
    for m in chord_at(12 + k):
        for d in (-R.get("stringDetune", 8), 0, R.get("stringDetune", 8)):
            f = hz(m) * 2 ** (d / 1200); ph = 2*np.pi*f*np.cumsum(1 + vib[a0:a1]) / SR
            x = sum(np.sin(h * ph) / h for h in range(1, 9))
            strings[a0:a1] += x * np.clip((np.arange(a1-a0))/SR/0.6, 0, 1) * np.clip(((a1-a0)/SR - np.arange(a1-a0)/SR)/0.5, 0, 1)
b, a = sg.butter(2, 4500 / (SR/2)); strings = sg.lfilter(b, a, strings)
senv = np.clip(tt / bar, 0, 1) * np.clip((L/SR - tt) / (2*bar), 0, 1)                    # legato fade into outro
st = np.stack([strings * 0.8, np.roll(strings, 240)], 1) * (senv * 0.035)[:, None]
dry[i0:i1] += st; verb_send[i0:i1] += st * 0.8
# hat loop (series modal ticks) + S&H on step pattern -> volume dips, inverse metallic comb FX mix, duplicated layer
hs = SH["hats"]; hb0, hb1 = S_["hats"]; loop = np.zeros(N)
for b in range(hb0, hb1):
    for k in range(hs["stepDiv"]):
        s = b * bar + k * bar / hs["stepDiv"]; v = 0.55 + 0.45 * (k % 2 == 0)
        y = tick(v); i = int(s * SR); e = min(N, i + len(y)); loop[i:e] += y[:e - i]
steps = rng.random(4 * hs["stepDiv"])                                   # random-drawn 4-bar step modulator at 1/8
stepsig = steps[((t / (bar / hs["stepDiv"])).astype(int)) % len(steps)]
shv = sh(stepsig, np.full(N, hs["stepDiv"] / bar * 0.5))               # S&H processes the step pattern (half rate -> held pairs)
shv = sg.filtfilt(np.ones(96) / 96, [1], shv)                           # 2 ms smoothing to avoid zipper clicks
vol = 1 - hs["volAmount"] * shv; fxmix = hs["fxMixMax"] * shv           # inverse: FX opens where volume dips
d = int(SR / hs["combHz"]); comb = np.zeros(N); comb[:] = loop
for r in range(1, 12): comb[r*d:] += loop[:-r*d] * hs["combFb"] ** r
comb *= 0.35; proc = loop * vol * (1 - fxmix) + comb * fxmix * vol.clip(0.4)
henv = np.clip((t - hb0*bar) / bar, 0, 1) * np.clip((hb1*bar - t) / bar, 0, 1) * (0.7 + 0.3 * np.clip((t - 12*bar)/bar, 0, 1))
b, a = sg.butter(2, 3000 / (SR/2), "high"); loop = sg.lfilter(b, a, loop); proc = sg.lfilter(b, a, proc)
dry += np.stack([loop * 0.6 + proc * 0.2, loop * 0.3 + proc * 0.6], 1) * henv[:, None] * 10 ** ((hs["dupLayerDb"] + R.get("hatTrimDb", 0)) / 20)
# riser: white noise -> LP, cutoff from S&H(sine LFO); LFO rate ramps to max, S&H rate starts low (aliasing slow-down)
rs = SH["riser"]; i0, i1 = bars(*S_["riser"]); L = i1 - i0; tt = np.arange(L) / SR; u = tt / tt[-1]
lfo_hz = rs["lfoHzStart"] * (rs["lfoHzEnd"] / rs["lfoHzStart"]) ** u
sh_hz = rs["shHzStart"] + (rs["shHzEnd"] - rs["shHzStart"]) * u ** 2 + R.get("riserWander", 1.5) * np.sin(2*np.pi*0.7*tt)  # own curve + random-ish moves
lsig = 0.5 + 0.5 * np.sin(2 * np.pi * np.cumsum(lfo_hz) / SR)
Nsave = N; N = L; held = sh(lsig, sh_hz); N = Nsave
held = R.get("riserSH", 1.0) * held + (1 - R.get("riserSH", 1.0)) * u
cut = rs["cutLow"] * (rs["cutHigh"] / rs["cutLow"]) ** (np.clip(rs["amount"] * held + 0.3 * u, 0, 1))
nz = rng.standard_normal((L, 2)); y = np.zeros((L, 2)); blk = 240; zi = np.zeros((2, 2))
for k in range(0, L, blk):
    b, a = sg.butter(2, min(cut[k], 15000) / (SR / 2))
    for c in range(2): y[k:k+blk, c], zi[c] = sg.lfilter(b, a, nz[k:k+blk, c], zi=zi[c] * 1)
renv = u ** 2 * np.clip((1 - u) / 0.03, 0, 1)
dry[i0:i1] += y * renv[:, None] * rs["level"]; verb_send[i0:i1] += y * renv[:, None] * rs["level"] * 0.6
# outro: single-note cymbal swell (modal metallic bank on noise) + short piano dialogue
i0, i1 = bars(*ARC["cymbalSwellBars"]); L = i1 - i0; tt = np.arange(L) / SR
nz = rng.standard_normal(L); b, a = sg.butter(2, [4000/(SR/2), 14000/(SR/2)], "band"); cy = sg.lfilter(b, a, nz)
cy = cy + 0.3 * bank(hz(93), {"model": "beam", "partials": 6, "decay": 2.0, "material": 0.3, "inharm": 1.15}, L)
cenv = (tt / tt[-1]) ** 3 * np.clip((tt[-1] - tt) / 0.4, 0, 1)
dry[i0:i1] += np.stack([cy, np.roll(cy, 300)], 1) * (cenv * 0.07)[:, None]; verb_send[i0:i1] += cy[:, None] * (cenv * 0.05)[:, None]
for s, m, p in ((18 * bar, 69, -0.4), (18.75 * bar, 64, 0.4), (19.25 * bar, 69, -0.2)):
    y = mallet("harp", m, 0.55, 0.3); place(dry, y, s, p); place(verb_send, y * 0.9, s); events += 1
# ---------------- space + light master (skill C step 7)
wl, wr = dsp.fdn_reverb(verb_send[:, 0].copy(), verb_send[:, 1].copy(), SR, 4.5, 1.2, 7000.0, 0.03, 0.3, 0.7, 0.4, 3)
mix = dry + 0.35 * np.stack([wl, wr], 1)
Mm = R["master"]; b, a = sg.butter(2, 20/(SR/2), "high"); mix = sg.filtfilt(b, a, mix, axis=0)      # HP 20 Hz
mix = np.tanh(Mm["satDrive"] * mix / (np.max(np.abs(mix)) + 1e-9)) / np.tanh(Mm["satDrive"])            # a little saturation
M = 0.5 * (mix[:, 0] + mix[:, 1]); S = 0.5 * (mix[:, 0] - mix[:, 1])
b, a = sg.butter(4, Mm["sideHpHz"]/(SR/2), "high"); S = sg.filtfilt(b, a, S); mix = np.stack([M + S, M - S], 1)
fi = np.clip(t / Mm["fadeInSec"], 0, 1); fo = np.clip((T - 0.3 - t) / Mm["fadeOutSec"], 0, 1) ** 2
mix *= (fi * fo)[:, None]; mix -= mix.mean(0)
meter = pyln.Meter(SR); gr_max = 0.0
for it in range(4):
    mix *= 10 ** ((Mm["targetLufs"] - meter.integrated_loudness(mix)) / 20)
    tp = np.maximum(dsp.true_peak_env(mix[:, 0]), dsp.true_peak_env(mix[:, 1]))
    ceil = 10 ** (Mm["tpCeil"] / 20); la = int(0.005 * SR); g0 = np.minimum(1, ceil / np.maximum(tp, 1e-9))
    g = np.minimum.reduce([np.roll(g0, k) for k in range(-la, la + 1, 24)]); g = np.minimum(sg.filtfilt(np.ones(la) / la, [1], g), 1)
    gr_max = max(gr_max, -20 * np.log10(g.min())); mix *= g[:, None]
    if abs(meter.integrated_loudness(mix) - Mm["targetLufs"]) < 0.3: break
mix[-int(0.3*SR):] = 0; mix[:2] = 0; mix -= mix.mean(0)
sf.write(OUT, mix.astype(np.float32), SR, subtype="PCM_24")
res = metrics.compute(mix, {"limiter_gr_db": gr_max}, R.get("category", "pad"), False, R["bars"] * bar, start_body_s=0.0, f_low=hz(45), bar_s=bar)
res["events"] = events; res["lengthSec"] = round(T, 2); res["lufs"] = round(meter.integrated_loudness(mix), 2)
json.dump(res, open(OUT + ".stats.json", "w"), indent=1, default=float)
print(json.dumps({"score": res["score"], "pass": res["pass"], "lufs": res["lufs"], "tp": res["extra"].get("true_peak_dbtp"),
                  "gates": res["gates"], "subs": res["subs"], "events": events, "gr": round(gr_max, 2)}, default=float))
