#!/usr/bin/env python3
"""Daily 3-skill test 2026-10-26: HP phaser saw chord pad (source) + slow one-key ambient harmony + section transition toolkit.
usage: render.py recipe.json out.wav   (original synthesis, deterministic)"""
import sys, os, json, numpy as np, soundfile as sf, pyloudnorm as pyln
from scipy import signal as sg
LAB = os.environ.get("LAB", "/workspace/skill-library/sample-lab"); sys.path.insert(0, LAB + "/engine")
import dsp, metrics
SR = 48000
R = json.load(open(sys.argv[1])); OUT = sys.argv[2]; rng = np.random.default_rng(R["seed"])
bar = 4 * 60 / R["bpm"]; beat = bar / 4; T = R["bars"] * bar + R["tailSec"]; N = int(T * SR); t = np.arange(N) / SR
hz = lambda m: 440 * 2 ** ((m - 69) / 12); P = R["pad"]; PR = R["progression"]
def idx(b): return min(N, int(b * bar * SR))
def chord(b): return PR[min(int(b) // 2, len(PR) - 1)]
def fade(L, a, r):
    tt = np.arange(L) / SR; return np.clip(tt / a, 0, 1) * np.clip((L / SR - tt) / r, 0, 1)
def sos(kind, f): return sg.butter(2, f, kind, fs=SR, output="sos")
def pan2(x, p): return np.stack([x * np.cos((p + 1) * np.pi / 4), x * np.sin((p + 1) * np.pi / 4)], 1) * np.sqrt(2)
events = 0
# ---------- skill A steps 1,6,7: low saw chords, unison, harmonizer at 3rd harmonic (wide)
padL = np.zeros(N); padR = np.zeros(N)
nch = len(PR)
for c in range(nch):
    i0 = idx(2 * c); i1 = idx(2 * c + 2.25) if c < nch - 1 else idx(R["bars"]); L = i1 - i0; w = fade(L, 0.9, 0.7)
    for m in PR[c][1]:
        m -= 12                                                       # low chords (octave 3)
        for u in range(P["unison"]):
            d = (u - (P["unison"] - 1) / 2) * P["detuneCents"]; pn = (u / max(1, P["unison"] - 1)) * 2 - 1
            f = np.full(L, hz(m) * 2 ** (d / 1200))
            x = dsp.osc_va(f, 0, 0.5, rng.random(), SR) * w / P["unison"]
            h = dsp.osc_va(f * P["harmonizerRatio"], 0, 0.5, rng.random(), SR) * w / P["unison"] * P["harmonizerAmt"]
            padL[i0:i1] += x * (1 - P.get("spread", 0.4) * pn) + h * (1 - P["harmonizerWidth"] * pn)
            padR[i0:i1] += x * (1 + P.get("spread", 0.4) * pn) + h * (1 + P["harmonizerWidth"] * pn)
        events += 1
# ---------- step 2: resonant HP, cutoff automated across the chords (exponential rise per chord, plus transition-1 stack)
u = (t % (2 * bar)) / (2 * bar)
cut = P["hpLow"] * (P["hpHigh"] / P["hpLow"]) ** (0.15 + 0.55 * np.sin(np.pi * u) ** 2)
tr1 = R["trans1"]; b8 = tr1["atBar"] * bar; ramp1 = np.clip((t - (b8 - tr1["riserBars"] * bar)) / (tr1["riserBars"] * bar), 0, 1) * (t < b8)
cut *= 2 ** (2.0 * ramp1 ** 3)                                            # toolkit step 5/6: stacked exponential cutoff push
padL = dsp.svf(padL, cut, P["hpQ"], 2, SR); padR = dsp.svf(padR, cut * 1.03, P["hpQ"], 2, SR)
# step 5: phaser one cycle per 2 bars (L/R offset for width), mix rises in the transition stack
ph_rate = 1 / (P["phaserBars"] * bar)
pmix = P["phaserMix"]
padL = dsp.phaser(padL, ph_rate, P["phaserDepth"], P["phaserFb"], P["phaserStages"], pmix, 0.0, SR)
padR = dsp.phaser(padR, ph_rate, P["phaserDepth"], P["phaserFb"], P["phaserStages"], pmix, 0.8, SR)
# step 7: light compression, highs and some mids down
pad = np.stack([padL, padR], 1); pad /= np.max(np.abs(pad)) + 1e-9
g = dsp.env_follow_gain(0.5 * (pad[:, 0] + pad[:, 1]), SR, P["compThreshDb"], P["compRatio"], 0.02, 0.3); pad *= g[:, None]
for c in range(2):
    pad[:, c] = dsp.eq(pad[:, c], "highshelf", 5000, 0.707, P["highShelfDb"]); pad[:, c] = dsp.eq(pad[:, c], "peak", 1800, 0.8, P["midCutDb"])
penv = 0.25 + 0.75 * np.clip(t / (4 * bar), 0, 1)
gc = 1 / (1 + 0.6 * ramp1 ** 3)                                          # gain compensation for the HP push
if tr1["dropFirstBeat"]: penv *= 1 - 0.85 * ((t >= b8) & (t < b8 + beat)) * 1.0  # toolkit step 9: drop pad on first beat across the barline
penv = sg.filtfilt(np.ones(240) / 240, [1], penv)
pad *= (penv * gc * P["level"])[:, None]
# steps 3,4: ping-pong 1/4 delay low-cut 200 + big reverb low-cut 200
dl, dr = dsp.stereo_delay(pad[:, 0].copy(), pad[:, 1].copy(), SR, beat, beat, 0.0, 0.0, P["delayFb"], P["delayFb"], 1, P["delayHp"], 6000.0, 0.0, 0.0, 0.0)
dly = np.stack([dl, dr], 1) * P["delayMix"]
dry = pad + dly; verb_send = np.zeros((N, 2)); verb_send += pad * 0.6
# ---------- skill B: layers spread chord tones (step 8); pedal/moving bass (5,6); warm mid layer; bell carries top tone
bass = np.zeros(N); warm = np.zeros(N)
for c in range(nch):
    i0 = idx(2 * c); i1 = idx(2 * c + 2.1) if c < nch - 1 else idx(R["bars"]); L = i1 - i0; tt = np.arange(L) / SR; w = fade(L, 0.6, 0.5)
    fb = hz(PR[c][0] - 12 if PR[c][0] > 44 else PR[c][0]); bass[i0:i1] += np.sin(2 * np.pi * fb * tt + 0.3 * np.sin(2 * np.pi * fb * tt)) * w
    up = sorted(PR[c][1])
    for m in (PR[c][0] + 12, up[1] - 12):                            # inversion/drop: a chord tone dropped an octave into 110-260 Hz
        f = np.full(L, hz(m)); warm[i0:i1] += dsp.osc_va(f, 2, 0.5, rng.random(), SR) * w
warm = sg.sosfilt(sos("low", 700), warm)
tr2 = R["trans2"]; b16 = tr2["atBar"] * bar
benv = np.clip(t / (2 * bar), 0.3, 1) * (1 - ((t >= b16 - tr2["bassSilenceBeats"] * beat) & (t < b16)))   # toolkit step 8: bass removed for last beat
benv = sg.filtfilt(np.ones(480) / 480, [1], benv) * np.clip((R["bars"] * bar - t) / (2 * bar), 0, 1)
dry += (bass * benv * R["bassLevel"])[:, None]; dry += pan2(warm * benv * R["warmLevel"], 0.0) * np.array([1, 0.92])
verb_send += (warm * benv * R["warmLevel"] * 0.4)[:, None]
def bell(m, vel, L=int(3.5 * SR)):
    tt = np.arange(L) / SR; f = hz(m)
    y = np.sin(2*np.pi*f*tt) * np.exp(-tt / 1.6) + 0.35 * np.sin(2*np.pi*3*f*tt) * np.exp(-tt / 0.6) + 0.12 * np.sin(2*np.pi*5.4*f*tt) * np.exp(-tt / 0.25)
    y *= np.clip(tt / 0.004, 0, 1); y[-480:] *= np.linspace(1, 0, 480); return y * vel
bellbus = np.zeros((N, 2))
def put(buf, y, s, p=0.0):
    i = int(s * SR); e = min(N, i + len(y)); buf[i:e] += pan2(y[:e - i], p)
for b in range(8, 16):                                                # B section: bell takes one chord tone per half bar
    up = sorted(chord(b)[1]) + [chord(b)[1][0] + 12]
    for k in range(2):
        put(bellbus, bell(up[(b + k * 2) % len(up)] + 12, 0.8 if k == 0 else 0.6), b * bar + k * 2 * beat, 0.4 * (-1) ** (b + k)); events += 1
# toolkit step 4: B-section bell enters early with a 2-beat pickup before bar 8
for j, m in enumerate((76, 79)):
    put(bellbus, bell(m, 0.45 + 0.1 * j), b8 - (tr1["pickupBeats"] - j) * beat, -0.3); events += 1
# outro bell replies (tail hangs over)
for s, m in ((16.5, 81), (17.5, 76), (18.5, 72)): put(bellbus, bell(m, 0.5), s * bar, 0.3); events += 1
bellbus *= R["bellLevel"]
# toolkit step 3: throw bells into a delay over the last 2 bars before 16: mix 0->100%, feedback rising, resonant BP sweeping
thr0 = b16 - tr2["throwBars"] * bar; uu = np.clip((t - thr0) / (b16 - thr0), 0, 1); send = (uu ** 2) * (t < b16 + 0.05)
xs = bellbus * send[:, None]
wa = np.stack(dsp.stereo_delay(xs[:, 0].copy(), xs[:, 1].copy(), SR, beat * 0.75, beat * 0.75, 0, 0, tr2["throwFb"][0], tr2["throwFb"][0], 1, 300.0, 7000.0, 0.1, 0.002, 0.3), 1)
wb = np.stack(dsp.stereo_delay(xs[:, 0].copy(), xs[:, 1].copy(), SR, beat * 0.75, beat * 0.75, 0, 0, tr2["throwFb"][1], tr2["throwFb"][1], 1, 300.0, 7000.0, 0.1, 0.002, 0.3), 1)
fbx = np.clip((t - thr0) / (b16 - thr0), 0, 1)[:, None]; throw = wa * (1 - fbx) + wb * fbx
fc = 800 * 4 ** uu; throw = np.stack([dsp.svf(throw[:, c].copy(), fc, 3.0, 1, SR) * 0.6 + throw[:, c] * 0.4 for c in range(2)], 1)
dry_bell = bellbus * (1 - 0.7 * send)[:, None]
dry += dry_bell + throw * 0.9; verb_send += bellbus * 0.7 + throw * 0.3
# skill B step 7: 1-2-3 cluster band-limited to 600-1000 Hz (tension before the outro)
CL = R["cluster"]; i0, i1 = idx(CL["bars"][0]), idx(CL["bars"][1]); L = i1 - i0; cl = np.zeros(L)
for m in CL["notes"]: cl += dsp.osc_va(np.full(L, hz(m)), 0, 0.5, rng.random(), SR)
cl = sg.sosfilt(sos("high", CL["bpLow"]), cl); cl = sg.sosfilt(sos("high", CL["bpLow"]), cl)
cl = sg.sosfilt(sos("low", CL["bpHigh"]), cl); cl = sg.sosfilt(sos("low", CL["bpHigh"]), cl)
cl *= (np.linspace(0, 1, L) ** 1.5) * fade(L, 0.05, 0.08) * 0.1 * CL["level"]
dry[i0:i1] += pan2(cl, 0.2); verb_send[i0:i1] += pan2(cl, -0.2) * 0.8
# ---------- transition 1 (bar 8): synthesized noise riser (BP rising, exponential) + reverse-reverb whoosh + impact
i0, i1 = idx(tr1["atBar"] - tr1["riserBars"]), idx(tr1["atBar"]); L = i1 - i0; uq = np.linspace(0, 1, L)
nz = rng.standard_normal(L); rc = 300 * 2 ** (5 * uq ** 2)
rs = dsp.svf(nz, rc, 2.5, 1, SR); sawr = dsp.osc_va(hz(57) * 2 ** (uq * 12 / 12), 0, 0.5, 0.0, SR) * 0.3   # second layer: saw pitching up an octave
rs = (rs + sg.sosfilt(sos("high", 400), sawr)) * (uq ** 3) * fade(L, 0.01, 0.02) * tr1["riserLevel"]
dry[i0:i1] += pan2(rs, 0.0) * np.array([1, 0.95]); verb_send[i0:i1] += pan2(rs, 0.0) * 0.5
# toolkit step 7: print the last pad bar to a 100%-wet reverb, reverse it into the hit
src = pad[idx(tr1["atBar"] - 1):i1].copy(); wl, wr = dsp.fdn_reverb(src[:, 0].copy(), src[:, 1].copy(), SR, 4.0, 1.0, 6000.0, 0.0, 0.2, 0.7, 0.0, 7)
rv = np.stack([wl, wr], 1)[::-1]; rv *= (np.linspace(0, 1, len(rv)) ** 2)[:, None]; rv /= np.max(np.abs(rv)) + 1e-9
dry[i1 - len(rv):i1] += rv * 0.08 * tr1["reverseVerbLevel"]
# step 2: impact = noisy hit + low thump into big reverb on the landing downbeat
Li = int(2.5 * SR); ti = np.arange(Li) / SR
imp = sg.sosfilt(sos("high", 150), rng.standard_normal(Li)) * np.exp(-ti / 0.12) * 0.5 + np.sin(2 * np.pi * (55 + 60 * np.exp(-ti / 0.05)) * ti) * np.exp(-ti / 0.5)
imp[:48] *= np.linspace(0, 1, 48); imp *= tr1["impactLevel"] * 0.35
dry[i1:i1 + Li] += pan2(imp, 0.0); verb_send[i1:i1 + Li] += pan2(sg.sosfilt(sos("high", 200), imp), 0.0) * 1.2
# ---------- transition 2 tail: downlifter after bar 16 (noise LP falling, hangs over)
i0 = idx(tr2["atBar"]); L = int(tr2["downlifterBars"] * bar * SR); uq = np.linspace(0, 1, L)
dn = dsp.svf(rng.standard_normal(L), 6000 * 2 ** (-5 * uq), 1.5, 0, SR) * (1 - uq) ** 2 * fade(L, 0.005, 0.1) * tr2["downLevel"]
dry[i0:i0 + L] += pan2(dn, -0.2); verb_send[i0:i0 + L] += pan2(dn, 0.2) * 0.5
# ---------- reverb (low-cut 200 Hz per skill A step 4) + master
vs = np.stack([sg.sosfilt(sos("high", P["verbHp"]), verb_send[:, c]) for c in range(2)], 1)
wl, wr = dsp.fdn_reverb(vs[:, 0].copy(), vs[:, 1].copy(), SR, P["verbRt60"], 1.4, 5500.0, 0.03, 0.3, 0.75, 0.3, 3)
mix = dry + P["verbWet"] * np.stack([wl, wr], 1)
Mm = R["master"]; mix = sg.sosfiltfilt(sos("high", 20), mix, axis=0)
mix = np.tanh(Mm["satDrive"] * mix / (np.max(np.abs(mix)) + 1e-9)) / np.tanh(Mm["satDrive"])
M = 0.5 * (mix[:, 0] + mix[:, 1]); S = 0.5 * (mix[:, 0] - mix[:, 1]); S = sg.sosfiltfilt(sg.butter(4, Mm["sideHpHz"], "high", fs=SR, output="sos"), S)
mix = np.stack([M + S, M - S], 1)
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
