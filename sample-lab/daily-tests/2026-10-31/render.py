#!/usr/bin/env python3
"""Daily 3-skill test 2026-10-31 "Lantern Drift": eerie dreamy phaser pad (source/FX) + synth drum ensemble (drums)
+ three-track cinematic sketch (structure: piano / orchestra / rhythmic swell, automation-only transitions, tempo ramp).
usage: render.py recipe.json out.wav"""
import sys, os, json, numpy as np, soundfile as sf, pyloudnorm as pyln
from scipy import signal as sg
LAB = os.environ.get("LAB", "/workspace/skill-library/sample-lab"); sys.path.insert(0, LAB + "/engine")
import dsp, metrics
SR = 48000
R = json.load(open(sys.argv[1])); OUT = sys.argv[2]; rng = np.random.default_rng(R["seed"])
TP = R["tempo"]; NB = len(TP); blen = np.array([240 / b for b in TP]); bstart = np.concatenate([[0], np.cumsum(blen)])
def tb(x):  # bar position (float) -> seconds, tempo map (skill C step 6: 95 -> 100 -> ramp to 112, ease back)
    b = int(min(np.floor(x), NB - 1)); return bstart[b] + (x - b) * blen[b]
T = bstart[NB] + R["tailSec"]; N = int(T * SR); t = np.arange(N) / SR; S = R["sections"]
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
def flt(k, f, x, o=2): return sg.sosfilt(sg.butter(o, f, k, fs=SR, output="sos"), x, axis=0)
def pan2(x, p): return np.stack([x * np.cos((p + 1) * np.pi / 4), x * np.sin((p + 1) * np.pi / 4)], 1) * np.sqrt(2)
def put(buf, y, s, g=1.0):
    i = int(round(s * SR)); L = min(len(y), N - i)
    if L > 0 and i >= 0: buf[i:i + L] += y[:L] * g
def verb(x, rt, seed, damp=10000.0):
    l, r = dsp.fdn_reverb(np.ascontiguousarray(x[:, 0]), np.ascontiguousarray(x[:, 1]), SR, float(rt), 1.6, damp, 0.03, 0.25, 0.75, 0.0, seed); return np.stack([l, r], 1)
def ramp(b0, b1, v0, v1):  # automation lane between bar positions
    return np.interp(t, [tb(b0), tb(b1)], [v0, v1])
def sm(x, ms=30): n = max(int(ms * SR / 1000), 1); return sg.filtfilt(np.ones(n) / n, [1], x)
fade = lambda y, ms=10: (y.__setitem__(slice(-int(ms*SR/1000), None), y[-int(ms*SR/1000):] * np.linspace(1, 0, int(ms*SR/1000))), y)[1]
chord = lambda b: R["chords"][(int(b) // 2) % 2]
events = 0
# ===== automation-only transitions (skill C step 5): LP close then open on runs, reverb mix swells
lpAuto = np.ones(N); vbAuto = np.zeros(N)
for b0, depth in zip((S["run"], S["smallRun"]), R["runDepth"]):
    lpAuto *= 1 - depth * np.clip(np.interp(t, [tb(b0 - 0.5), tb(b0 + 0.6), tb(b0 + 1.0), tb(b0 + 1.15)], [0, 1, 1, 0]), 0, 1)
    vbAuto += depth * np.interp(t, [tb(b0 - 0.25), tb(b0 + 0.9), tb(b0 + 1.6)], [0, 1, 0])
# ===== SKILL A: eerie dreamy phaser pad = "orchestra" chord bed
P = R["pad"]; pad = np.zeros((N, 2)); topf = np.zeros(N)
for b0 in range(0, NB, 2):
    root, notes = chord(b0); s0 = tb(b0); dur = tb(min(b0 + 2, NB)) - s0 + P["rel"]; L = int(dur * SR); tt = np.arange(L) / SR
    env = np.clip(tt / P["atk"], 0, 1) * np.clip((dur - tt) / P["rel"], 0, 1) ** 1.5           # step 2: long attack + release
    for m in notes:                                                                           # step 1: paraphonic 4 notes, supersaw
        for k in range(P["saws"]):
            c = (k - (P["saws"] - 1) / 2) / ((P["saws"] - 1) / 2) * P["detuneCents"]; f = hz(m) * 2 ** (c / 1200)
            y = dsp.osc_va(np.full(L, f), 0, 0.5, rng.random(), SR) * env / P["saws"]
            put(pad, pan2(y, np.clip((k / (P["saws"] - 1) - 0.5) * P["spread"], -1, 1)), s0)
    i0 = int(s0 * SR); topf[i0:i0 + L] = np.maximum(topf[i0:i0 + L], hz(max(notes)))
    events += 1
topf[topf == 0] = hz(64)
# steps 6-7: cyclic (looping rise/fall) envelope on cutoff, rise/fall times varied by a slow LFO that also hits cutoff
lfo = np.sin(2 * np.pi * P["lfoHz"] * t); ph = 0.0; cyc = np.zeros(N); dt = 1 / SR; kr = 64
for i in range(0, N, kr):
    rise = P["cycRise"] * (1 + P["lfoToTimes"] * lfo[i]); fall = P["cycFall"] * (1 - P["lfoToTimes"] * lfo[i])
    p = ph % 1; r_ = rise / (rise + fall)
    cyc[i:i + kr] = p / r_ if p < r_ else 1 - (p - r_) / (1 - r_); ph += kr * dt / (rise + fall)
cyc = sm(cyc, 20)
fc = P["cutoff"] * (topf / hz(64)) ** P["keytrack"] * 2 ** (P["cycAmt"] * cyc + P["lfoToCut"] * lfo)   # step 2 key tracking 50%
fc = np.clip(fc * (0.2 + 0.8 * lpAuto), 150, 16000)
pad = np.stack([dsp.svf(np.ascontiguousarray(pad[:, c]), fc, P["res"], 0, SR) for c in range(2)], 1)
for j, rate in enumerate(P["phaserRates"]):                                                    # step 3: dual slow phasers, low res, stereo
    pad = np.stack([dsp.phaser(np.ascontiguousarray(pad[:, c]), rate, P["phaserDepth"], P["phaserFb"], 6, P["phaserMix"], j * 1.3 + c * np.pi / 2, SR) for c in range(2)], 1)
d1 = P["dly1"]; d2 = P["dly2"]                                                                    # step 4: 0.5 s modulated delay, 1.5 s ping-pong
w1 = np.stack(dsp.stereo_delay(np.ascontiguousarray(pad[:, 0]), np.ascontiguousarray(pad[:, 1]), SR, d1["t"], d1["t"] * 1.01, d1["fb"], d1["fb"], 0.0, 0.0, 0, 200.0, 7000.0, 0.0, d1["mod"], 0.4), 1)
w2 = np.stack(dsp.stereo_delay(np.ascontiguousarray(pad[:, 0]), np.ascontiguousarray(pad[:, 1]), SR, d2["t"], d2["t"], 0.0, 0.0, d2["fb"], d2["fb"], 1, 250.0, 6000.0, 0.0, 0.0, 0.0), 1)
pad = pad + d1["mix"] * w1 + d2["mix"] * w2
pad = pad + (P["verbMix"] + 0.3 * vbAuto)[:, None] * verb(flt("high", 200, pad), P["verbRt"], 3)  # step 5: lush reverb, dwell 0 (no hold)
pad /= np.max(np.abs(pad)) + 1e-9
# ===== SKILL C track 1: piano (FM-ish), two-chord back and forth, high ostinato, roll-up runs
PI = R["piano"]; piano = np.zeros((N, 2))
def pnote(m, vel=1.0, dur=1.6):
    L = int(dur * SR); tt = np.arange(L) / SR; f = hz(m)
    y = (np.sin(2*np.pi*f*tt + 1.2 * np.exp(-tt / 0.25) * np.sin(2*np.pi*2*f*tt)) + 0.25 * np.sin(2*np.pi*3*f*tt) * np.exp(-tt / 0.3))
    y *= np.clip(tt / 0.002, 0, 1) * np.exp(-tt / 0.7) * vel; return fade(y)
for b in range(S["build"], S["outro"] + 2):
    root, notes = chord(b); pat = [notes[0] + 12, notes[2] + 12, notes[3] + 12, notes[1] + 24]   # high ostinato, goes UP each bar
    if b in (S["run"], S["smallRun"]): continue
    for k in range(8):
        put(piano, pan2(pnote(pat[k % 4], 0.55 + 0.25 * (k % 4 == 0)), 0.2 * ((k % 2) - 0.5)), tb(b + k / 8)); events += 1
for b0, nb in ((S["run"], 1.0), (S["smallRun"], 0.5)):                                          # step 1: big roll-up (string/piano run)
    root, notes = chord(b0); seq = [n + 12 * o for o in range(2) for n in notes] + [notes[0] + 24]
    for j, m in enumerate(seq[: int(len(seq) * nb) + 1]):
        put(piano, pan2(pnote(m, 0.5 + 0.5 * j / len(seq)), -0.3 + 0.6 * j / len(seq)), tb(b0 + j / len(seq))); events += 1
piano = np.stack([dsp.eq(dsp.eq(piano[:, c], "lowshelf", 200, 0.7, PI["lowShelf"]), "highshelf", 5000, 0.7, PI["highShelf"]) for c in range(2)], 1)
piano = np.stack([dsp.svf(np.ascontiguousarray(piano[:, c]), np.clip(14000 * lpAuto, 500, 16000), 0.7, 0, SR) for c in range(2)], 1)
pv = verb(piano, PI["verbRt"], 5)
pv *= dsp.env_follow_gain(np.ascontiguousarray(pv.mean(1)), SR, -30.0, 3.0, 0.03, 0.4)[:, None]     # compressor AFTER reverb (tail forward)
piano = piano + (PI["verbMix"] + 0.4 * vbAuto)[:, None] * pv / (np.max(np.abs(pv)) + 1e-9) * np.max(np.abs(piano))
# ===== SKILL C track 2: orchestra = bass roots + contrary-motion counter line (+ chorus main melody, woodwind sparkle)
O = R["orch"]; orch = np.zeros((N, 2)); bass = np.zeros(N)
def bowed(m, dur, atk=0.25):
    L = int(dur * SR); tt = np.arange(L) / SR; f = np.full(L, hz(m))
    y = 0.5 * dsp.osc_va(f, 0, 0.5, 0.0, SR) + 0.5 * dsp.osc_va(f * 1.003, 0, 0.5, 0.3, SR)
    y = flt("low", min(hz(m) * 6, 9000), y) * np.clip(tt / atk, 0, 1) * np.clip((dur - tt) / 0.25, 0, 1); return y
for b in range(S["build"], S["end"]):
    root, notes = chord(b); L = int((blen[b] * 0.98) * SR); tt = np.arange(L) / SR
    y = (np.sin(2*np.pi*hz(root - 12)*tt) + 0.25 * np.sin(2*np.pi*hz(root)*tt)) * np.clip(tt / 0.02, 0, 1) * np.clip((L/SR - tt) / 0.08, 0, 1)
    put(bass, y, tb(b)); events += 1
    if b < S["outro"]:                                                                          # counter: 5th -> 3rd -> root (down while piano goes up)
        third = notes[2] if root == 45 else notes[0]; fifth = root + 19
        for j, m in enumerate((fifth, third + 0 if third < fifth else third - 12, root + 12)):
            put(orch, pan2(bowed(m, blen[b] / 3 + 0.2), -0.25), tb(b + j / 3)); events += 1
mel = [76, 74, 72, 71, 72, 69, 69, 67, 76, 77, 76, 72, 74, 72, 71, 69]               # chorus main melody, half-bar notes, steady pitch
for b in range(S["chorus"], S["outro"]):
    for h in range(2):
        m = mel[((b - S["chorus"]) * 2 + h) % len(mel)]; d = blen[b] / 2 + 0.15
        put(orch, pan2(bowed(m, d, 0.08), 0.1) * O["leadLevel"] / O["counterLevel"], tb(b + h / 2))
        L = int(d * SR); tt = np.arange(L) / SR
        put(orch, pan2(np.sin(2*np.pi*hz(m + 12)*tt) * np.exp(-tt / 0.4) * np.clip(tt / 0.01, 0, 1), 0.35) * O["sparkle"] / O["counterLevel"], tb(b + h / 2)); events += 2
orch = np.stack([dsp.svf(np.ascontiguousarray(orch[:, c]), np.clip(12000 * lpAuto, 400, 16000), 0.7, 0, SR) for c in range(2)], 1)
orch = orch + (0.25 + 0.4 * vbAuto)[:, None] * verb(orch, 3.0, 11)
# ===== SKILL C track 3: synthetic swell layer with rhythmic auto-filter, dry/wet low in intro, full in chorus
SW = R["swell"]; swell = np.zeros((N, 2))
for b0 in range(S["build"], S["end"], 2):
    root, notes = chord(b0); notes = [root + 12] if b0 >= S["outro"] else notes                  # step 7: outro back to roots only
    dur = tb(min(b0 + 2, NB)) - tb(b0) + 0.5; L = int(dur * SR); tt = np.arange(L) / SR
    for m in notes:
        y = dsp.osc_va(np.full(L, hz(m - 12 if b0 < S["outro"] else m)), 0, 0.5, rng.random(), SR) * np.clip(tt / SW["atk"], 0, 1) * np.clip((dur - tt) / 0.5, 0, 1)
        put(swell, pan2(y, rng.uniform(-0.5, 0.5)), tb(b0))
sixteenth = np.zeros(N)
for b in range(NB):
    for k in range(16): s0 = tb(b + k / 16); sixteenth += np.exp(-np.clip(t - s0, 0, None) / 0.07) * (t >= s0) * (1 - (t >= tb(b + (k + 1) / 16)))
wetSw = ramp(S["build"], S["chorus"], SW["wetIntro"], SW["wetChorus"]) * (t < tb(S["outro"])) + 0.3 * (t >= tb(S["outro"]))
fcs = SW["fcBase"] * 2 ** (SW["fcOct"] * sixteenth)
swW = np.stack([dsp.svf(np.ascontiguousarray(swell[:, c]), fcs, 1.5, 0, SR) for c in range(2)], 1)
swD = flt("low", 1200, swell)
swell = swD * (1 - wetSw)[:, None] + swW * wetSw[:, None]
# ===== SKILL B: synth drum ensemble — one epic-drum patch x4 instances on the same MIDI
D = R["drums"]; drums = np.zeros((N, 2)); shaker = np.zeros((N, 2))
def epic(inst, vel):
    dec = 0.35 * inst["decay"]; L = int((dec * 3) * SR); tt = np.arange(L) / SR
    f = 75 * 2 ** (inst["pitch"] / 12) * 2 ** (1.6 * np.exp(-tt / 0.04))                    # macro: global pitch
    body = np.tanh(1.6 * np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-tt / dec)          # macro: global decay (amp + filter env)
    nz = flt("low", 9000, rng.standard_normal(L)) * np.exp(-tt / (0.05 * inst["decay"]))
    nz = dsp.eq(nz, "peak", inst["snap"], 1.2, 9.0)                                           # macro: snap EQ freq
    y = (body + 0.35 * nz) * np.clip(tt / 0.001, 0, 1) * vel; return fade(y, 15)
pat_build = [(0, 1.0), (0.375, 0.6), (0.5, 0.85), (0.875, 0.55)]
pat_chorus = [(k / 8, 1.0 if k in (0, 4) else 0.55 + 0.2 * (k % 2 == 0)) for k in range(8)] + [(0.9375, 0.5)]
for b in range(S["drumsIn"], S["end"] - 1):
    pat = pat_chorus if S["chorus"] <= b < S["outro"] else pat_build
    if b in (S["run"], S["smallRun"]): pat = [(0, 1.0), (0.5, 0.7)]                           # thin out under the runs
    for pos, v in pat:
        for inst in D["instances"]:                                                           # step 2: per-note random env delay 0..(rand*44) ms
            dly = rng.uniform(0, inst["rand"] * D["randMaxMs"] / 1000)
            put(drums, pan2(epic(inst, v), inst["pan"]), tb(b + pos) + dly)
        events += 1
    if b >= S["build"]:                                                                       # step 6: tempo-synced 16-step sequencer on filter
        for k in range(16):
            L = int(0.09 * SR); tt = np.arange(L) / SR; st = D["stepSeq"][k]
            y = flt("band", [2500 + 6000 * st, 3000 + 9000 * st], rng.standard_normal(L)) * np.exp(-tt / 0.025) * np.clip(tt / 0.002, 0, 1) * (0.4 + 0.6 * st)
            put(shaker, pan2(fade(y, 5), 0.3 * ((k % 2) - 0.5)), tb(b + k / 16))
shk = (0.4 + 0.6 * ((t >= tb(S["chorus"])) & (t < tb(S["outro"]))))
drums = flt("high", 30, drums)
dkey = np.abs(drums.mean(1)); kev = sg.lfilter([1], [1, -np.exp(-1 / (0.2 * SR))], (dkey > 0.3 * dkey.max()).astype(float)) * (1 - np.exp(-1 / (0.2 * SR))) * 40
duck = 1 - D["duck"] * np.clip(kev, 0, 1)
drums = drums + 0.18 * verb(flt("high", 250, drums), 2.2, 13)
# ===== mix + master (skill C step 8: mono lows, light comp/sat, EQ, limiter)
nm = lambda x: x / (np.max(np.abs(x)) + 1e-9)
mix = nm(pad) * P["level"] * duck[:, None] + nm(piano) * PI["level"] + nm(orch) * 0.45 + pan2(nm(bass) * O["bassLevel"], 0) * duck[:, None]
mix += nm(swell) * SW["level"] * duck[:, None] + nm(drums) * D["level"] + nm(shaker) * D["shaker"] * shk[:, None]
Mm = R["master"]; mix = sg.sosfiltfilt(sg.butter(2, 20, "high", fs=SR, output="sos"), mix, axis=0)
mix = np.stack([dsp.eq(mix[:, c], "highshelf", 2500, 0.6, Mm["shelfDb"]) for c in range(2)], 1)
mix = np.tanh(Mm["satDrive"] * mix / (np.max(np.abs(mix)) + 1e-9)) / np.tanh(Mm["satDrive"])
M = 0.5 * (mix[:, 0] + mix[:, 1]); Sd = 0.5 * (mix[:, 0] - mix[:, 1]); Sd = sg.sosfiltfilt(sg.butter(4, Mm["sideHpHz"], "high", fs=SR, output="sos"), Sd); mix = np.stack([M + Sd, M - Sd], 1)
fo = np.clip((T - 0.3 - t) / Mm["fadeOutSec"], 0, 1) ** 2; mix *= fo[:, None]; mix -= mix.mean(0)
meter = pyln.Meter(SR); gr_max = 0.0
for it in range(6):
    mix *= 10 ** ((Mm["targetLufs"] - meter.integrated_loudness(mix)) / 20)
    tp = np.maximum(dsp.true_peak_env(mix[:, 0]), dsp.true_peak_env(mix[:, 1])); ceil = 10 ** (Mm["tpCeil"] / 20); la = int(0.005 * SR)
    g0 = np.minimum(1, ceil / np.maximum(tp, 1e-9)); g = np.minimum.reduce([np.roll(g0, k) for k in range(-la, la + 1, 24)]); g = np.minimum(sg.filtfilt(np.ones(la) / la, [1], g), 1)
    gr_max = max(gr_max, -20 * np.log10(g.min())); mix *= g[:, None]
    if abs(meter.integrated_loudness(mix) - Mm["targetLufs"]) < 0.3: break
mix -= mix.mean(0); mix[-int(0.3 * SR):] = 0; mix[:int(0.002*SR)] = 0; mix[int(0.002*SR):int(0.2*SR)] *= np.linspace(0, 1, int(0.198*SR))[:, None]
sf.write(OUT, mix.astype(np.float32), SR, subtype="PCM_24")
res = metrics.compute(mix, {"limiter_gr_db": gr_max}, R.get("category", "pad"), False, bstart[NB], start_body_s=0.0, f_low=hz(33), bar_s=float(np.mean(blen)))
res["events"] = events; res["lengthSec"] = round(T, 2); res["lufs"] = round(meter.integrated_loudness(mix), 2)
res["drumsInSec"] = round(tb(S["drumsIn"]), 2); res["chorusSec"] = round(tb(S["chorus"]), 2)
json.dump(res, open(OUT + ".stats.json", "w"), indent=1, default=float)
print(json.dumps({"score": res["score"], "pass": res["pass"], "lufs": res["lufs"], "tp": res["extra"].get("true_peak_dbtp"), "gates": res["gates"], "subs": res["subs"], "tilt": res["extra"].get("tilt_db_oct"), "events": events, "gr": round(gr_max, 2), "len": res["lengthSec"], "drumsIn": res["drumsInSec"]}, default=float))
