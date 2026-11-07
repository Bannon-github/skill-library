#!/usr/bin/env python3
"""Daily 3-skill test 2026-11-04: start-bright-then-filter pad (brightness-and-air-at-the-source) +
kick+bass punch workflow in four levels (bass-design) + genre drum pattern families, halftime two-step at 140 (drum-groove).
usage: render.py recipe.json out.wav"""
import sys, os, json, numpy as np, soundfile as sf, pyloudnorm as pyln
from scipy import signal as sg
LAB = os.environ.get("LAB", "/workspace/skill-library/sample-lab"); sys.path.insert(0, LAB + "/engine")
import dsp, metrics
SR = 48000
R = json.load(open(sys.argv[1])); OUT = sys.argv[2]; rng = np.random.default_rng(R["seed"])
NB = R["bars"]; BL = 240 / R["bpm"]; BT = BL / 4; S16 = BT / 4; tb = lambda x: x * BL; S = R["sections"]
T = NB * BL + R["tailSec"]; N = int(T * SR); t = np.arange(N) / SR
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
def flt(k, f, x, o=2): return sg.sosfilt(sg.butter(o, f, k, fs=SR, output="sos"), x, axis=0)
def pan2(x, p): return np.stack([x * np.cos((p + 1) * np.pi / 4), x * np.sin((p + 1) * np.pi / 4)], 1) * np.sqrt(2)
def put(buf, y, s, g=1.0):
    i = int(round(s * SR)); L = min(len(y), N - i)
    if L > 0 and i >= 0: buf[i:i + L] += y[:L] * g
def verb(x, rt, seed, damp=9000.0, size=1.8, mod=0.25, diff=0.75):
    l, r = dsp.fdn_reverb(np.ascontiguousarray(x[:, 0]), np.ascontiguousarray(x[:, 1]), SR, float(rt), size, damp, 0.03, mod, diff, 0.0, seed); return np.stack([l, r], 1)
def fade(y, ms=10, mi=0.0):
    n = int(ms * SR / 1000); y[-n:] *= np.linspace(1, 0, n)
    if mi: m = int(mi * SR / 1000); y[:m] *= np.linspace(0, 1, m)
    return y
nm = lambda x: x / (np.max(np.abs(x)) + 1e-9)
st2 = lambda f, x: np.stack([f(np.ascontiguousarray(x[:, c]), c) for c in range(2)], 1)
def sec(b): return "intro" if b < S["drumsIn"] else "groove" if b < S["peak"] - 4 else "build" if b < S["peak"] else "peak" if b < S["outro"] else "outro"
chord = lambda b: R["chords"][(b // 2) % 4]
events = 0
# Main-melody revision: pitched harmonic lead, no pitch modulation or RNG.
lead = np.zeros((N, 2)); lead_events = []
# Four-bar call and answer: three notes, then a held answer and breathing room.
phrases = [ [(1., 1., 0), (2.5, 1., 1)], [(0., 2., 2)],
            [(0.5, 1., 1), (2., 1.25, 2)], [(0., 2.5, 0)] ]
for b in range(16, S["outro"]):
    notes = chord(b)[1]
    for off, beats, degree in phrases[(b-16)%4]:
        if b == 16 and off < 1: continue
        start = tb(b) + off * BT
        midi = notes[degree] + 12
        duration = beats * BT + 0.18
        ln = int(duration * SR); tt = np.arange(ln)/SR
        attack = 0.035; release = 0.18
        env = np.sin(0.5*np.pi*np.clip(tt/attack,0,1))**2
        env *= np.sin(0.5*np.pi*np.clip((duration-tt)/release,0,1))**2
        tone = sum(g*np.sin(2*np.pi*hz(midi)*h*tt) for h,g in [(1,1),(2,.26),(3,.13),(4,.05)])
        y = tone * env * (0.94 if b < S["peak"] else 1.0)
        assert abs(y[0]) < 1e-12 and abs(y[-1]) < 1e-5
        put(lead, pan2(y, -0.05), start)
        lead_events.append({"start":start,"midi":midi,"duration":duration})
lead = flt("high", 240, lead, 2)
lead = lead + .16 * verb(lead, 1.6, 73, 6500., 1.6, 0.0)
lead *= .11

# Preserve the approved original render rather than repeating its slow FIR master.
original, sr = sf.read(os.path.join(os.path.dirname(__file__), "track.wav"))
assert sr == SR and original.shape == lead.shape
onset = int(round(lead_events[0]["start"]*SR))
assert np.max(np.abs(lead[:onset])) == 0
mix = original + lead
meter = pyln.Meter(SR)
gain_db = -17.0 - meter.integrated_loudness(mix)
mix *= 10**(gain_db/20)
peak = np.max(np.abs(sg.resample_poly(mix,4,1,axis=0)))
assert peak < 10**(-1.5/20)
assert np.max(np.abs(mix[:onset] - original[:onset]*10**(gain_db/20))) < 1e-12
sf.write(OUT,mix,SR,subtype="PCM_24")
sf.write(OUT+".lead.wav",lead,SR,subtype="FLOAT")
report={"duration":len(mix)/SR,"lufs":meter.integrated_loudness(mix),"true_peak_dbtp":20*np.log10(peak),"melody_onset_sec":lead_events[0]["start"],"drums_in_sec":tb(S["drumsIn"]),"original_global_gain_db":gain_db,"original_audio_preserved":True,"notes":lead_events}
json.dump(report,open(OUT+".verification.json","w"),indent=2)
print(json.dumps({k:v for k,v in report.items() if k!="notes"}))
