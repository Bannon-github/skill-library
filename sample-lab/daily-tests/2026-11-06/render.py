#!/usr/bin/env python3
"""Daily 3-skill test 2026-11-06: generative MIDI chord→arp→random→scale-quantize pad
(generative-ambient) + field-recording HPF/exciter air layer (brightness-and-air) +
cinematic 7-section arc with ostinato/countermelody/bookend (arrangement-ambient-cinematic).
usage: render.py recipe.json out.wav"""
import sys, os, json, numpy as np, soundfile as sf, pyloudnorm as pyln
from scipy import signal as sg
LAB = os.environ.get("LAB", "/workspace/skill-library/sample-lab"); sys.path.insert(0, LAB + "/engine")
import dsp, metrics
SR = 48000
R = json.load(open(sys.argv[1])); OUT = sys.argv[2]; rng = np.random.default_rng(R["seed"])
NB = R["bars"]; BL = 240 / R["bpm"]; BT = BL / 4; tb = lambda x: x * BL; S = R["sections"]
T = NB * BL + R["tailSec"]; N = int(T * SR); t = np.arange(N) / SR
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
def flt(k, f, x, o=2):
    if np.ndim(x) == 1: return sg.sosfilt(sg.butter(o, f, k, fs=SR, output="sos"), x)
    return sg.sosfilt(sg.butter(o, f, k, fs=SR, output="sos"), x, axis=0)
def pan2(x, p): return np.stack([x * np.cos((p + 1) * np.pi / 4), x * np.sin((p + 1) * np.pi / 4)], 1) * np.sqrt(2)
def put(buf, y, s, g=1.0):
    i = int(round(s * SR)); L = min(len(y), N - i)
    if L > 0 and i >= 0:
        if y.ndim == 1 and buf.ndim == 2: buf[i:i + L] += (y[:L] * g)[:, None]
        elif y.ndim == 1: buf[i:i + L] += y[:L] * g
        else: buf[i:i + L] += y[:L] * g
def verb(x, rt, seed, damp=8500.0, size=1.9, mod=0.22, diff=0.78):
    xl = np.ascontiguousarray(x[:, 0] if x.ndim == 2 else x)
    xr = np.ascontiguousarray(x[:, 1] if x.ndim == 2 else x)
    l, r = dsp.fdn_reverb(xl, xr, SR, float(rt), size, damp, 0.03, mod, diff, 0.0, seed)
    return np.stack([l, r], 1)
def fade(y, ms=10, mi=0.0):
    n = max(1, int(ms * SR / 1000)); y = y.copy()
    if n < len(y): y[-n:] *= np.linspace(1, 0, n)
    if mi:
        m = max(1, int(mi * SR / 1000))
        if m < len(y): y[:m] *= np.linspace(0, 1, m)
    return y
nm = lambda x: x / (np.max(np.abs(x)) + 1e-9)
st2 = lambda f, x: np.stack([f(np.ascontiguousarray(x[:, c]), c) for c in range(2)], 1)

# ---- section helpers (7-section compressed arc) ----
def sec(b):
    if b < S["strings"]: return "open"
    if b < S["ostinato"]: return "strings"
    if b < S["motif"]: return "ostinato"
    if b < S["peak"]: return "motif"
    if b < S["outro"]: return "peak"
    return "outro"

def chord_idx(b):
    order = R["chordOrderA"] if (b < S["strings"] + 2) or (b >= S["outro"]) else R["chordOrderB"]
    # 2 bars per chord in open/strings/outro; 1 bar elsewhere for motion
    step = 2 if sec(b) in ("open", "strings", "outro") else 1
    return order[(b // step) % 4]

def chord_at(b):
    return R["chords"][chord_idx(b)]

# D natural minor absolute MIDI degrees for scale quantize (root/fifth heavy map)
SCALE = np.array(R["scale"], dtype=int)  # D2..C3 base octave template
DEGREES = [0, 2, 3, 5, 7, 8, 10]  # D E F G A Bb C as semitone offsets from D

def quantize_to_scale(midi):
    """Nearest D-minor pitch class, preserving octave."""
    pc = int(round(midi)) % 12
    root_pc = 2  # D
    # allowed pcs in D natural minor
    allowed = {(root_pc + d) % 12 for d in DEGREES}
    best = min(allowed, key=lambda a: min((pc - a) % 12, (a - pc) % 12))
    # reconstruct near original
    octv = int(round(midi)) // 12
    cand = best + 12 * octv
    if abs(cand - midi) > abs(cand - 12 - midi): cand -= 12
    if abs(cand - midi) > abs(cand + 12 - midi): cand += 12
    return cand

def weighted_degree(rng):
    # skill probs: ~1/3 low root, ~1/6 high octave root, ~5/12 fifth, ~1/12 M2, rest sparse
    # mapped onto [root, M2, fifth, high-root, third-sparse]
    w = R["genPad"]["degreeWeights"]  # [root, M2, fifth, third, highroot-ish]
    # degrees relative: 0, 2, 7, 3, 12
    deg = [0, 2, 7, 3, 12]
    i = int(rng.choice(len(deg), p=np.array(w) / np.sum(w)))
    return deg[i]

events = 0

# =====================================================================
# SKILL A: generative MIDI chord → arp → random → scale-quantize pad
# Uneven loop lengths, send-return FX as layers, slow LFOs
# =====================================================================
G = R["genPad"]
gen = np.zeros((N, 2))
oct_send = np.zeros((N, 2))  # granular-ish octave-up return

# Precompute slow free-running LFOs (offset phases)
lfo_send = 0.5 - 0.5 * np.cos(2 * np.pi * t / (11 * BL) + 0.3)
lfo_hpf = 0.5 - 0.5 * np.cos(2 * np.pi * t / (7 * BL) + 1.7)
lfo_bass = 0.5 - 0.5 * np.cos(2 * np.pi * t / (13 * BL) + 2.4)
lfo_tone = 0.5 - 0.5 * np.cos(2 * np.pi * t / (9 * BL) + 0.9)

# Build generative note events for three uneven-length layers
# Layer roles: mid soft pad, high glass, low soft bass tone
layers = [
    {"name": "mid", "oct": 0, "loop": G["loopBars"][0], "unison": G["midUnison"], "detune": G["midDetune"], "spread": 0.7, "shape": 2, "level": 1.0},
    {"name": "high", "oct": 12, "loop": G["loopBars"][1], "unison": G["highUnison"], "detune": G["highDetune"], "spread": 1.1, "shape": 1, "level": 0.55},
    {"name": "bass", "oct": -12, "loop": G["loopBars"][2], "unison": 1, "detune": 0, "spread": 0.0, "shape": 0, "level": G["bassLevel"]},
]

def gen_midi_chain(root_midi, n_steps, layer_rng):
    """chord → arp → random → scale-quantize LAST. Returns list of (step_i, midi)."""
    # chord intervals from held root (minor-7 voicing)
    intervals = [0, 3, 7, 10]
    chord_notes = [root_midi + iv for iv in intervals]
    # arpeggiate up-down
    arp = chord_notes + chord_notes[-2:0:-1]
    out = []
    for i in range(n_steps):
        base = arp[i % len(arp)]
        # random/chance pitch
        if layer_rng.random() < G["randomChance"]:
            # jump by weighted scale degree from root of current chord
            base = root_midi + weighted_degree(layer_rng) + (12 if layer_rng.random() < 0.15 else 0)
        # scale quantize LAST
        out.append((i, quantize_to_scale(base)))
    return out

# Render generative layers across the whole track (fade with arrangement)
for li, Lspec in enumerate(layers):
    lrng = np.random.default_rng(R["seed"] + 17 * (li + 1))
    loop_bars = Lspec["loop"]
    # number of arp steps per bar
    steps_per_bar = int(round(4 / G["arpRateBeats"]))
    gate = G["arpGate"] * G["arpRateBeats"] * BT
    # tile uneven loops covering full piece
    b0 = 0
    while b0 < S["end"]:
        root, _ = chord_at(b0)
        root = root + Lspec["oct"]
        n_steps = loop_bars * steps_per_bar
        notes = gen_midi_chain(root, n_steps, lrng)
        for i, midi in notes:
            st = tb(b0) + i * G["arpRateBeats"] * BT
            if st >= tb(S["end"]): break
            # section presence: quieter in open, fuller later, soft in bookend
            sname = sec(min(int(st / BL), S["end"] - 1))
            sect_g = {"open": 0.55, "strings": 0.75, "ostinato": 0.9, "motif": 0.95, "peak": 1.0, "outro": 0.5}[sname]
            if Lspec["name"] == "bass":
                sect_g *= 0.7 + 0.3 * (1 - G["bassLfoDepth"] * lfo_bass[min(int(st * SR), N - 1)])
            dur = gate + G["release"] * (0.5 if Lspec["name"] == "high" else 0.85)
            Ln = int(dur * SR); tt = np.arange(Ln) / SR
            amp = np.clip(tt / G["attack"], 0, 1) * np.clip((dur - tt) / max(0.05, G["release"] * 0.6), 0, 1)
            y = np.zeros((Ln, 2)); U = max(1, Lspec["unison"])
            for k in range(U):
                x = (k / max(1, U - 1) - 0.5) if U > 1 else 0.0
                f0 = hz(midi) * 2 ** (x * Lspec["detune"] / 1200)
                ph = float(lrng.random())
                if Lspec["shape"] == 0:
                    v = np.sin(2 * np.pi * f0 * tt + ph)
                else:
                    v = dsp.osc_va(np.full(Ln, f0), Lspec["shape"], 0.4, ph, SR)
                y += pan2(v, x * 2 * Lspec["spread"]) / U
            # mild tone LFO via soft LP
            cut = G["cutBase"] + (G["cutPeak"] - G["cutBase"]) * lfo_tone[min(int(st * SR), N - 1)]
            if sname == "peak": cut *= 1.25
            if sname == "outro": cut *= 0.85
            y = st2(lambda x, c: dsp.svf(x, np.full(Ln, cut), 0.7, 0, SR), y)
            put(gen, y * (amp * Lspec["level"] * sect_g)[:, None], st)
            # octave-up send (simulates granular/octave return)
            if Lspec["name"] != "bass" and lrng.random() < 0.45:
                v2 = np.sin(2 * np.pi * hz(midi + 12) * tt + ph) * amp * 0.5
                put(oct_send, pan2(v2, (lrng.random() - 0.5) * 1.4), st + 0.03)
            events += 1
        b0 += loop_bars

# Slow LFO on HPF + send amount (send return as blendable layer)
hpf_hz = np.clip(G["hpfLfoBase"] + G["hpfLfoDepth"] * lfo_hpf, 40, 400)
# apply time-varying HPF in chunks
gen_f = np.zeros_like(gen)
chunk = int(0.05 * SR)
for i0 in range(0, N, chunk):
    sl = slice(i0, min(N, i0 + chunk)); fc = float(hpf_hz[i0])
    gen_f[sl] = flt("high", fc, gen[sl], 2)
gen = gen_f
send_amt = G["sendFloor"] + G["sendDepth"] * lfo_send
oct_cloud = verb(flt("high", 400, oct_send, 2), 4.5, 7, 7000.0, 2.2)
oct_cloud = nm(oct_cloud) * G["octUpLevel"]
# blend send as instrument layer (modulated)
gen = nm(gen) + (send_amt[:, None] * oct_cloud)
wet = verb(flt("high", G["verbHp"], gen, 4), G["verbRt"], 5, 6500.0, 2.3)
gen = (1 - G["verbMix"]) * nm(gen) + G["verbMix"] * nm(wet)
Mp = 0.5 * (gen[:, 0] + gen[:, 1]); Sp = 0.5 * (gen[:, 0] - gen[:, 1]) * G["imagerSide"]
gen = np.stack([Mp + Sp, Mp - Sp], 1)
gen = st2(lambda x, c: dsp.eq(x, "highshelf", 3200, 0.7, G["bright"]), gen)
gen = flt("high", 55, gen, 2)

# =====================================================================
# SKILL B: field-recording-style air layer — synthesized, HPF + exciter + shelf
# =====================================================================
A = R["air"]
# air hiss (room tone / wind)
hiss = rng.standard_normal(N)
hiss = flt("band", [2500, 12000], hiss, 2)
# sparse bird-like chirps: short FM sweeps at irregular intervals
chirps = np.zeros(N)
t_next = 2.5
while t_next < T - 2:
    # chirp duration 80–220 ms
    d = 0.08 + 0.14 * float(rng.random()); Ln = int(d * SR); tt = np.arange(Ln) / SR
    f0 = 2200 + 2800 * float(rng.random()); f1 = f0 * (1.2 + 0.6 * float(rng.random()))
    # quadratic chirp
    phase = 2 * np.pi * (f0 * tt + (f1 - f0) * tt ** 2 / 2)
    # light FM
    mod = 1 + 0.15 * np.sin(2 * np.pi * (18 + 10 * rng.random()) * tt)
    env = np.sin(np.pi * np.clip(tt / d, 0, 1)) ** 1.4
    v = np.sin(phase * mod) * env
    # occasional double call
    put(chirps, fade(v, 5, 3), t_next)
    if rng.random() < 0.35:
        put(chirps, fade(v * 0.7, 5, 3), t_next + 0.12 + 0.08 * rng.random())
    t_next += (0.9 + 2.8 * float(rng.random())) / max(0.15, A["chirpRate"])
    events += 1
# distant leaf/air detail: sparse filtered noise bursts
detail = np.zeros(N)
t_next = 1.0
while t_next < T - 1:
    d = 0.15 + 0.4 * float(rng.random()); Ln = int(d * SR)
    burst = flt("band", [4000, 11000], rng.standard_normal(Ln), 2)
    burst *= np.hanning(Ln) * (0.3 + 0.7 * rng.random())
    put(detail, burst, t_next); t_next += 0.6 + 2.2 * float(rng.random())

air_mono = A["hissLevel"] * hiss * 0.35 + A["chirpLevel"] * chirps + 0.45 * detail
# step 2: HPF muddy lows first
air_mono = flt("high", A["hpfHz"], air_mono, 4)
# step 3: subtle harmonic exciter on upper band (soft sat of highs, blend back)
hi = flt("high", 3000, air_mono, 2)
excited = np.tanh(A["exciterDrive"] * hi)
air_mono = air_mono + A["exciterMix"] * (excited - hi)
# step 4: light high shelf
air_mono = dsp.eq(air_mono, "highshelf", A["shelfHz"], 0.7, A["shelfDb"])
# step 5: slow tremolo + L↔R pan
trem = 1 - A["tremDepth"] * (0.5 - 0.5 * np.cos(2 * np.pi * A["tremRate"] * t))
pn = 0.55 * np.sin(2 * np.pi * A["panRate"] * t)
air = pan2(air_mono * trem, 0)
air = np.stack([
    air[:, 0] * np.cos((pn + 1) * np.pi / 4),
    air[:, 1] * np.sin((pn + 1) * np.pi / 4)
], 1) * np.sqrt(2)
# presence fades: softer in open, present through mid, gentle in bookend
air_env = np.ones(N)
for b in range(S["end"]):
    sname = sec(b); g = {"open": 0.55, "strings": 0.8, "ostinato": 1.0, "motif": 1.0, "peak": 0.85, "outro": 0.6}[sname]
    i0 = int(tb(b) * SR); i1 = int(tb(min(b + 1, S["end"])) * SR)
    air_env[i0:i1] = g
air = nm(air) * A["level"] * air_env[:, None]

# =====================================================================
# SKILL C: cinematic 7-section arc — piano, strings, ostinato, motif,
# countermelody climax, bookend
# =====================================================================
Pno = R["piano"]; piano = np.zeros((N, 2))
# reverse-piano-ish soft risers on downbeats of open/bookend
rev = np.zeros((N, 2))
Str = R["strings"]; strings = np.zeros((N, 2))
Ost = R["ostinato"]; ost = np.zeros(N)
Mel = R["melody"]; mel = np.zeros((N, 2)); counter = np.zeros((N, 2))
Pulse = R["pulse"]; pulse = np.zeros(N); subp = np.zeros(N)

def piano_hit(midi, dur, vel=1.0):
    Ln = int(dur * SR); tt = np.arange(Ln) / SR
    amp = np.clip(tt / Pno["attack"], 0, 1) * np.exp(-tt / (0.55 + 0.9 * vel)) * np.clip((dur - tt) / 0.15, 0, 1)
    y = np.zeros(Ln)
    for k, h in enumerate(Pno["harmonics"]):
        y += h * np.sin(2 * np.pi * hz(midi) * (k + 1) * tt) * np.exp(-tt * (0.4 + 0.5 * k))
    # soft hammer noise
    y += 0.04 * flt("band", [800, 4000], rng.standard_normal(Ln), 2) * np.exp(-tt / 0.02)
    return fade(y * amp * vel, 15, 2)

# Section 1+2 / 7: open + bookend piano chords (open-voiced)
for b in list(range(S["open"], S["strings"])) + list(range(S["outro"], S["end"])):
    root, notes = chord_at(b)
    # open voicing: drop lowest, spread
    voicing = [notes[0] - 12, notes[1], notes[2], notes[3] + 12] if len(notes) >= 4 else notes
    for j, m in enumerate(voicing):
        v = piano_hit(m, Pno["release"] + BL * 0.5, 0.75 if j else 0.95)
        put(piano, pan2(v, -0.35 + 0.25 * j), tb(b) + 0.01 * j)
        events += 1
    # quiet low drone / boom under open chords
    Ln = int((BL + 0.5) * SR); tt = np.arange(Ln) / SR
    boom = np.sin(2 * np.pi * hz(root) * tt) * np.exp(-tt / 1.2) * np.clip(tt / 0.05, 0, 1)
    put(piano, pan2(boom * 0.35, 0), tb(b))
    # reverse-piano continuity: soft swell into next bar
    if b + 1 < S["end"] and (b < S["strings"] or b >= S["outro"]):
        Ln = int(0.9 * BL * SR); tt = np.arange(Ln) / SR
        rv = piano_hit(notes[2], 1.2, 0.4)[::-1][:Ln] if True else None
        # build reverse from noise+sine
        rv = (0.6 * np.sin(2 * np.pi * hz(notes[1]) * tt) + 0.4 * flt("band", [400, 2500], rng.standard_normal(Ln), 2))
        rv *= (tt / (0.9 * BL)) ** 2 * np.exp(-((0.9 * BL) - tt) / 0.08)
        put(rev, pan2(fade(rv, 20), -0.2), tb(b) + 0.1 * BL)
        events += 1

# Also light piano doubles during motif/peak for continuity
for b in range(S["motif"], S["outro"]):
    root, notes = chord_at(b)
    if b % 2 == 0:
        v = piano_hit(notes[0], 1.5, 0.4)
        put(piano, pan2(v, -0.2), tb(b)); events += 1

piano = nm(piano + 0.55 * rev)
piano = piano + Pno["verbMix"] * nm(verb(flt("high", 180, piano, 2), 3.8, 13))
piano = nm(piano) * Pno["level"]

# Section 3: sustained strings under (from strings section through peak; soft in bookend)
for b in range(S["strings"], S["end"]):
    root, notes = chord_at(b)
    # hold 2 bars in early, 1 bar later
    nb = 2 if b < S["ostinato"] and b % 2 == 0 else 1
    if b < S["ostinato"] and b % 2 == 1: continue
    dur = nb * BL + Str["release"]; Ln = int(dur * SR); tt = np.arange(Ln) / SR
    amp = np.clip(tt / Str["attack"], 0, 1) * np.clip((dur - tt) / Str["release"], 0, 1)
    sname = sec(b); g = {"open": 0, "strings": 0.7, "ostinato": 0.85, "motif": 0.9, "peak": 1.0, "outro": 0.35}[sname]
    y = np.zeros((Ln, 2)); U = Str["unison"]
    for m in notes[:3]:
        for k in range(U):
            x = (k / (U - 1) - 0.5)
            f0 = hz(m) * 2 ** (x * Str["detune"] / 1200)
            # soft saw→triangle blend for string-ish
            v = 0.55 * dsp.osc_va(np.full(Ln, f0), 2, 0.5, float(rng.random()), SR) + 0.45 * np.sin(2 * np.pi * f0 * tt)
            y += pan2(v, x * 1.5) / (U * 3)
    y = st2(lambda x, c: dsp.svf(x, np.full(Ln, Str["cut"]), 0.65, 0, SR), y)
    put(strings, y * (amp * g)[:, None], tb(b)); events += 1
strings = nm(strings) * Str["level"]
strings = strings + 0.4 * nm(verb(flt("high", 200, strings, 2), 5.0, 17))

# Section 4: chord-tone ostinato (shape locked, transposed per chord)
pat = Ost["pattern"]
for b in range(S["ostinato"], S["outro"]):
    root, notes = chord_at(b)
    # chord tones only
    tones = list(notes)
    for si, deg_i in enumerate(pat):
        st = tb(b) + si * (BT / 2)  # 8th notes
        m = tones[deg_i % len(tones)]
        # keep shape: same degree index, retarget
        Ln = int((Ost["decay"] + 0.15) * SR); tt = np.arange(Ln) / SR
        env = np.exp(-tt / Ost["decay"]) * np.clip(tt / 0.004, 0, 1)
        v = dsp.osc_va(np.full(Ln, hz(m)), 0, 0.5, 0.0, SR)  # short/pluck-ish saw
        v = dsp.svf(v, np.full(Ln, Ost["cutoff"] * (1 + 0.8 * np.exp(-tt / 0.04))), 0.9, 0, SR) * env
        # quieter before motif, stronger at peak
        g = 0.7 if sec(b) == "ostinato" else (0.85 if sec(b) == "motif" else 1.0)
        put(ost, fade(v, 8) * g, st); events += 1
ost = pan2(flt("high", 160, ost), 0.1)
ost = ost + 0.25 * nm(verb(flt("high", 300, ost), 2.2, 19))
ost = nm(ost) * Ost["level"]
# mute ostinato in bookend
ost[int(tb(S["outro"]) * SR):] = 0

# Section 5+6: melody from 2-bar motif; highest note in second half; countermelody; doubles
def chord_tone_by_deg(notes, deg):
    # deg as scale-ish: 0=root, 2=third-ish index, etc. Map onto chord tones + octave
    base = notes[deg % len(notes)]
    return base + 12 * (deg // len(notes))

for b in range(S["motif"], S["outro"]):
    root, notes = chord_at(b)
    # 2-bar motif: bars motif..motif+1 use degA; next 2 use degB (higher peak)
    # then repeat rhythm for second half of 8-bar window with higher notes
    local = (b - S["motif"]) % 8
    half = local // 2  # 0..3
    degs = Mel["motifDegA"] if half < 2 else Mel["motifDegB"]
    # highest note forced into second half (already via degB including +7)
    for ri, off in enumerate(Mel["motifRhythm"]):
        st = tb(b) + off * BT
        if st >= tb(b + 1): continue
        m = chord_tone_by_deg(notes, degs[ri % len(degs)])
        # lift an octave for presence
        m += 12
        Ln = int((Mel["release"] + 0.4) * SR); tt = np.arange(Ln) / SR
        amp = np.clip(tt / Mel["attack"], 0, 1) * np.clip((Mel["release"] - tt) / 0.2, 0, 1) * np.exp(-tt / 1.1)
        v = 0.7 * np.sin(2 * np.pi * hz(m) * tt) + 0.3 * dsp.osc_va(np.full(Ln, hz(m)), 2, 0.5, 0.0, SR)
        v = dsp.svf(v, np.full(Ln, 4500), 0.7, 0, SR) * amp
        put(mel, pan2(v, -0.15), st)
        # climax doubles: unison + octave (violins+piano feel)
        if b >= S["peak"]:
            v2 = 0.55 * np.sin(2 * np.pi * hz(m - 12) * tt) * amp  # cello octave down
            put(mel, pan2(v2, 0.1) * Mel["doubleLevel"], st)
            v3 = 0.4 * np.sin(2 * np.pi * hz(m + 12) * tt) * amp * np.exp(-tt / 0.6)
            put(mel, pan2(v3, 0.25) * Mel["doubleLevel"] * 0.7, st)
        events += 1
    # countermelody in rests/sustains (between motif attacks)
    if b >= S["peak"]:
        # enter on long sustains: mid-bar and near end
        for off, deg in [(1.1, 2), (3.1, 4)]:
            st = tb(b) + off * BT
            if st >= tb(min(b + 1, S["outro"])): continue
            m = chord_tone_by_deg(notes, deg) + 12
            Ln = int(0.9 * SR); tt = np.arange(Ln) / SR
            amp = np.clip(tt / 0.1, 0, 1) * np.clip((0.7 - tt) / 0.15, 0, 1)
            v = np.sin(2 * np.pi * hz(m) * tt) * amp
            put(counter, pan2(v, 0.35) * Mel["counterLevel"], st); events += 1

mel = nm(mel + counter)
mel = mel + 0.3 * nm(verb(flt("high", 250, mel), 3.2, 23))
mel = nm(mel) * Mel["level"]
# silence melody before motif and after peak into bookend fade
mel[:int(tb(S["motif"]) * SR)] = 0
# gentle fade of mel into bookend
i0 = int(tb(S["outro"]) * SR); mel[i0:] *= np.linspace(1, 0, N - i0)[: N - i0, None] ** 2 if False else 0

# pulsing bass-synth on roots at climax
for b in range(S["peak"], S["outro"]):
    root, _ = chord_at(b)
    step = Pulse["rateBeats"] * BT
    st = tb(b)
    while st < tb(b + 1) - 1e-6:
        Ln = int(0.45 * SR); tt = np.arange(Ln) / SR
        env = np.clip(tt / 0.01, 0, 1) * np.exp(-tt / 0.22)
        v = np.tanh(1.4 * dsp.osc_va(np.full(Ln, hz(root)), 0, 0.5, 0.0, SR)) * env
        put(pulse, v, st)
        put(subp, np.sin(2 * np.pi * hz(root) * tt) * env, st)
        st += step; events += 1
pulse = flt("low", 400, pulse, 2); subp = flt("low", 110, subp, 4)
pulse_bus = nm(pulse) * 0.6 + nm(subp) * Pulse["subLevel"]
pulse_st = pan2(pulse_bus, 0) * Pulse["level"]

# Soft cinematic drums — early entry (~12 s / bar 4)
D = R["drums"]; drm = np.zeros((N, 2))
def kick():
    Ln = int(0.45 * SR); tt = np.arange(Ln) / SR
    f = 48 + 90 * np.exp(-tt / 0.025)
    return fade(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.22), 10)
def hat(v=0.6, d=0.03):
    Ln = int(0.12 * SR)
    return fade(flt("band", [6000, 14000], rng.standard_normal(Ln), 2) * np.exp(-np.arange(Ln) / SR / d) * v, 4)
def rim():
    Ln = int(0.08 * SR); tt = np.arange(Ln) / SR
    return fade((flt("band", [1800, 4500], rng.standard_normal(Ln), 2) * 0.5 + np.sin(2 * np.pi * 780 * tt)) * np.exp(-tt / 0.025), 4)
def cym(d=0.7):
    Ln = int(d * 2.5 * SR)
    return fade(flt("high", 4500, rng.standard_normal(Ln), 2) * np.exp(-np.arange(Ln) / SR / d), 25)

for b in range(S["drumsIn"], S["drumsOut"]):
    sname = sec(b); o = tb(b)
    # soft half-time: kick on 1, light on 3 sometimes
    put(drm, pan2(kick(), 0) * D["kick"], o); events += 1
    if sname in ("motif", "peak") and b % 2 == 1:
        put(drm, pan2(kick() * 0.55, 0) * D["kick"], o + 2 * BT)
    # soft hats on offbeats
    if b >= S["drumsIn"] + 1:
        for q in (1, 3):
            put(drm, pan2(hat(0.45 + 0.2 * rng.random()), -0.25) * D["hat"], o + q * BT)
    if sname == "peak":
        for q in range(4):
            put(drm, pan2(hat(0.35, 0.05), 0.3) * D["hat"] * 0.7, o + q * BT)
        if (b - S["peak"]) % 4 == 0:
            put(drm, pan2(cym(0.55), -0.15) * D["crash"], o)
    if sname in ("ostinato", "motif") and b % 4 == 3:
        put(drm, pan2(rim(), 0.2) * D["rim"], o + 2.5 * BT)
drm = drm + 0.15 * nm(verb(flt("high", 500, drm), 1.6, 29))
drm = nm(drm) * D["level"]

# =====================================================================
# Mix + master
# =====================================================================
# arrangement gains by time for generative pad
pad_env = np.ones(N)
for b in range(S["end"]):
    sname = sec(b)
    g = {"open": 0.7, "strings": 0.85, "ostinato": 0.9, "motif": 0.95, "peak": 1.0, "outro": 0.65}[sname]
    i0 = int(tb(b) * SR); i1 = int(tb(min(b + 1, S["end"])) * SR)
    pad_env[i0:i1] = g

mix = (nm(gen) * G["level"] * pad_env[:, None]
       + air
       + piano
       + strings
       + ost
       + mel
       + pulse_st
       + drm)

Mm = R["master"]
mix = sg.sosfiltfilt(sg.butter(2, 22, "high", fs=SR, output="sos"), mix, axis=0)
mix = np.stack([dsp.eq(mix[:, c], "highshelf", 2800, 0.6, Mm["shelfDb"]) for c in range(2)], 1)
mix = np.tanh(Mm["satDrive"] * mix / (np.max(np.abs(mix)) + 1e-9)) / np.tanh(Mm["satDrive"])
M = 0.5 * (mix[:, 0] + mix[:, 1]); Sd = 0.5 * (mix[:, 0] - mix[:, 1])
Sd = sg.sosfiltfilt(sg.butter(4, Mm["sideHpHz"], "high", fs=SR, output="sos"), Sd)
mix = np.stack([M + Sd, M - Sd], 1)
fo = np.clip((T - 0.35 - t) / Mm["fadeOutSec"], 0, 1) ** 2
mix *= fo[:, None]; mix -= mix.mean(0)

meter = pyln.Meter(SR); gr_max = 0.0
for it in range(6):
    loud = meter.integrated_loudness(mix)
    if not np.isfinite(loud): loud = -30
    mix *= 10 ** ((Mm["targetLufs"] - loud) / 20)
    tp = np.maximum(dsp.true_peak_env(mix[:, 0]), dsp.true_peak_env(mix[:, 1]))
    ceil = 10 ** (Mm["tpCeil"] / 20)
    la = int(0.005 * SR)
    g0 = np.minimum(1, ceil / np.maximum(tp, 1e-9))
    gg = np.minimum.reduce([np.roll(g0, k) for k in range(-la, la + 1, 24)])
    gg = np.minimum(sg.filtfilt(np.ones(la) / la, [1], gg), 1)
    gr_max = max(gr_max, -20 * np.log10(max(gg.min(), 1e-9)))
    mix *= gg[:, None]
    if abs(meter.integrated_loudness(mix) - Mm["targetLufs"]) < 0.3: break

mix -= mix.mean(0)
mix[-int(0.3 * SR):] = 0
mix[:int(0.002 * SR)] = 0
mix[int(0.002 * SR):int(0.25 * SR)] *= np.linspace(0, 1, int(0.248 * SR))[:, None]
sf.write(OUT, mix.astype(np.float32), SR, subtype="PCM_24")
res = metrics.compute(mix, {"limiter_gr_db": gr_max}, R.get("category", "pad"), False, NB * BL, start_body_s=0.0, f_low=hz(34), bar_s=BL)
res["events"] = events; res["lengthSec"] = round(T, 2)
res["lufs"] = round(float(meter.integrated_loudness(mix)), 2)
res["drumsInSec"] = round(tb(S["drumsIn"]), 2)
json.dump(res, open(OUT + ".stats.json", "w"), indent=1, default=float)
print(json.dumps({
    "score": res["score"], "pass": res["pass"], "lufs": res["lufs"],
    "tp": res["extra"].get("true_peak_dbtp"), "gates": res["gates"], "subs": res["subs"],
    "tilt": res["extra"].get("tilt_db_oct"), "events": events, "gr": round(gr_max, 2),
    "len": res["lengthSec"], "drumsIn": res["drumsInSec"]
}, default=float))
