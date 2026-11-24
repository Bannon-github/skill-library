#!/usr/bin/env python3
"""Daily 3-skill test 2026-11-24 "Frozen Sixth" (E major, 94 BPM): four-part dreamy ambient (POMnaOf92UI) + end-of-bar dissonant pad tension / silence / freeze riser (IuscQShlL58) + ambient bass with master LFO and direct-out sine sub (MULPJOhSrZ0). usage: render.py recipe.json out.wav"""
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
def fade(y, ms=8):
    k = min(int(ms / 1000 * SR), len(y) // 2); y[-k:] *= np.cos(np.linspace(0, np.pi / 2, k)) ** 2; return y
def blep(p, dt):
    out = np.zeros_like(p); a = p < dt; x = p[a] / dt[a]; out[a] = x + x - x * x - 1
    b = p > 1 - dt; x = (p[b] - 1) / dt[b]; out[b] = x * x + x + x + 1; return out
def saw_osc(f, ph0=0.0):
    dt = f / SR; ph = (ph0 + np.cumsum(dt)) % 1.0; return 2 * ph - 1 - blep(ph, dt)
st = lambda b, s16: tb(b) + s16 * BT / 4
events = 0; SEC = R["sections"]; LV = R["levels"]
def sec_of(b):
    for s in SEC:
        if s["b"][0] <= b < s["b"][1]: return s
    return None
on = lambda name, b: (sec_of(b) is not None) and name in sec_of(b)["els"]
def chord_at(b):
    for c in R["chords"]:
        if c[0] <= b < c[1]: return c
    return R["chords"][-1]
# ================= (1) swarm pad: 2 detuned saws, linked slow-attack/full-sustain/long-release, Imaj7 <-> iii common-tone loop
P = R["pad"]; padL = np.zeros(N); padR = np.zeros(N)
for b0, b1, nmz, tones, _ in R["chords"]:
    s0 = tb(b0); held = tb(b1) - s0; i0 = int(s0 * SR); i1 = min(int((tb(b1) + P["rel"] * 2.5) * SR), N); tt = t[i0:i1] - s0
    env = (1 - np.exp(-tt / (P["atk"] / 3))) * np.where(tt < held, 1.0, np.exp(-(tt - held) / (P["rel"] / 3))) * np.minimum(tt / 0.01, 1)
    for m in tones:
        g = 0.6 if m < 48 else 1.0     # doubled bass note fattens, a bit lower
        f = np.full(i1 - i0, hz(m))
        o1 = saw_osc(f, rng.uniform()); o2 = saw_osc(f * 2 ** (P["detuneCents"] / 1200), rng.uniform())   # osc2 a touch brighter (sharper), mixed lower
        padL[i0:i1] += (o1 * 0.8 + o2 * 0.45) * env * g; padR[i0:i1] += (o1 * 0.45 + o2 * 0.8) * env * g; events += 1
pad = np.stack([padL, padR], 1)
open_ = np.clip(bar / NB, 0, 1)                     # step 7: pad filter opens across the whole track
fc = P["lpFrom"] * (P["lpTo"] / P["lpFrom"]) ** open_ * (1 + P["lfoDepth"] * np.sin(2 * np.pi * P["lfoHz"] * t))   # very slow, low-depth LFO
pad = np.stack([dsp.svf(C(pad[:, c]), C(fc), 0.7, 0, SR) for c in (0, 1)], 1); pad = bw("high", P["hpHz"], pad, 2)
cr = P["chorus"]; cl, crr = dsp.chorus(C(pad[:, 0]), C(pad[:, 1]), SR, 1, cr[0], cr[1], cr[2], cr[3], 1.0, 0.5, 0.0, 0.0)
pad = nm(np.stack([cl, crr], 1))
# ================= (2) vocal pad: formant 'ah' on root+5th, fixed loop, rate-reduced then smooth low-pass, big reverb
V = R["vox"]; vox = np.zeros(N)
for b0, b1, nmz, tones, root in R["chords"]:
    s0 = tb(b0); i0 = int(s0 * SR); i1 = min(int((tb(b1) + 2.5) * SR), N); tt = t[i0:i1] - s0; held = tb(b1) - s0
    env = (1 - np.exp(-tt / 0.8)) * np.where(tt < held, 1.0, np.exp(-(tt - held) / 0.8))
    for m in (root + 36, root + 43): vox[i0:i1] += saw_osc(np.full(i1 - i0, hz(m)), rng.uniform()) * env
vox = sum(g * dsp.svf(C(vox), C(np.full(N, f)), 6.0, 1, SR) for f, g in V["formants"])
hold = int(SR / V["holdSr"]); vox = np.repeat(vox[::hold], hold)[:N]; vox = np.pad(vox, (0, N - len(vox)))   # sample-rate reduction
vox = bw("low", V["lp"], vox, 4); vox = nm(bw("high", 200, vox, 2))
# ================= (3) ambient bass: mono, light static unison, ONE 4-bar retriggered master LFO on many timbre targets, FM macro, direct-out sine sub
B = R["bass"]; fB = np.zeros(N); fS = np.zeros(N); lfo = np.zeros(N)
for b0, b1, nmz, tones, root in R["chords"]:
    i0 = int(tb(b0) * SR); i1 = int(tb(b1) * SR) if b1 < NB else N
    fB[i0:i1] = hz(root + 12); fS[i0:i1] = hz(root)
    ph = (t[i0:i1] - tb(b0)) / (B["lfoBars"] * BL); lfo[i0:i1] = 0.5 - 0.5 * np.cos(2 * np.pi * ph)   # retriggered per note, 0->1->0 over 4 bars
lerp = lambda r: r[0] + (r[1] - r[0]) * lfo
up = np.zeros(N)
for k, dc in enumerate(B["detuneCents"]):
    f = fB * 2 ** (dc / 1200); f2 = f * 1.0
    mod = np.sin(2 * np.pi * np.cumsum(f2) / SR + rng.uniform() * 6.28)
    fm = f * (1 + B["fmIndex"] * 0.02 * mod)                    # FM macro (small, osc2 -> osc1)
    saw = saw_osc(fm, rng.uniform()); pls = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR + 0.3)) * 0.6
    w = lerp(B["pulseMix"]); up += ((1 - w) * saw + w * pls) / len(B["detuneCents"])
up = dsp.svf(C(up), C(lerp(B["lp1"])), 0.8, 0, SR)                       # filter 1 cutoff
up = up - 0.7 * dsp.svf(C(up), C(lerp(B["notch"])), 1.2, 1, SR)           # filter 2: slow notch auto-filter
up = np.tanh(up * lerp(B["drive"])) / np.tanh(lerp(B["drive"]))           # drive
up = up + 0.5 * dsp.svf(C(up), C(lerp(B["formant"])), 3.0, 1, SR)         # formant-ish peak
up = bw("high", B["upperHp"], up, 2)                                      # HP moving layers above the sub
sub = np.sin(2 * np.pi * np.cumsum(fS) / SR)                              # plain sine, unmodulated, direct out
bassOn = np.zeros(N)
for b in range(NB):
    if on("bass", b + 0.01): bassOn[int(tb(b) * SR):int(tb(b + 1) * SR)] = 10 ** (LV["bassBreakDb"] / 20) if (16 <= b < 20) else 1.0
bassOn = sm(sm(bassOn, 40), 40)
bassUp = nm(up) * bassOn; subS = sub * bassOn
# ================= (4) lead: sine->triangle pluck, light unison, free-running LFO on wave position, off-beat 8ths, density by un-muting
L_ = R["lead"]; lead = np.zeros(N); wash = np.zeros(N)
def pluck(m, g=1.0, tpos=0.3):
    Ln = int(2.0 * SR); tt = np.arange(Ln) / SR; y = np.zeros(Ln)
    for dc in (-L_["unisonCents"], L_["unisonCents"]):
        f = hz(m) * 2 ** (dc / 1200); ph = (f * tt) % 1.0
        tri = 4 * np.abs(ph - 0.5) - 1; y += (1 - tpos) * np.sin(2 * np.pi * ph) - tpos * tri
    e = np.minimum(tt / L_["atk"], 1) * np.exp(-tt / L_["decay"])         # compressor-softened attack
    y = np.tanh(L_["sat"] * y * e * 0.5) / np.tanh(L_["sat"] * 0.5)
    return fade(y, 60) * g
PH = R["phrase"]; nlead = 0; counts = {}
for b in range(0, NB, 2):
    act = None
    for d0, d1, idx in R["density"]:
        if d0 <= b < d1: act = idx
    if act is None: continue
    notes = [PH[i] for i in act if i != "x"] + (R["extras"] if "x" in act else [])
    for s16, m in notes:
        s0 = st(b, s16); bb = s0 / BL
        if (23.5 <= bb < 24) or not on("lead", bb): continue
        tpos = L_["triRange"][0] + (L_["triRange"][1] - L_["triRange"][0]) * (0.5 + 0.5 * np.sin(2 * np.pi * L_["triLfoHz"] * s0))
        y = pluck(m, 1.0, tpos); put(lead, y, s0); nlead += 1; events += 1
        key = sec_of(bb)["name"].split(":")[0]; counts[key] = counts.get(key, 0) + 1
        if b >= R["washFrom"]: put(wash, y, s0)
# ================= tension pad: root held, steps to minor 6th / 4th at the end of the bar, resolves on (or before) the downbeat
tens = np.zeros(N)
def tone(m, dur, atk=0.25, rel=0.35):
    Ln = int((dur + rel * 4) * SR); tt = np.arange(Ln) / SR; f = hz(m); ph = (f * tt) % 1.0
    y = np.sin(2 * np.pi * ph) + 0.3 * (4 * np.abs(ph - 0.5) - 1)
    e = np.minimum(tt / atk, 1) * np.where(tt < dur, 1.0, np.exp(-(tt - dur) / rel)); return fade(y * e, 50)
for b, hm, tm, tbeat, rm, rbeat, lab in R["tension"]:
    put(tens, tone(hm, tbeat * BT, 0.6) * np.linspace(0.4, 1, int((tbeat * BT + 1.4) * SR)), tb(b))      # cutoff/level brought in across the bar
    put(tens, tone(tm, (rbeat - tbeat) * BT, 0.03), tb(b) + tbeat * BT)
    put(tens, tone(rm, BT * (2 if rbeat == 4 else 1.5), 0.03, 0.6), tb(b) + rbeat * BT); events += 3
tens = nm(bw("low", 3000, tens, 2))
# ================= freeze riser: consonant chord frozen in a huge reverb, long curve into a dissonant (bigger-size) freeze, faded in
F = R["freeze"]; fz = np.zeros((N, 2))
def frozen(chord, size, seed):
    x = np.zeros(N); i0 = int(tb(F["b0"]) * SR); Ln = int(0.6 * SR); tt = np.arange(Ln) / SR
    for m in chord: x[i0:i0+Ln] += saw_osc(np.full(Ln, hz(m)), rng.uniform()) * np.minimum(tt / 0.05, 1) * np.exp(-tt / 0.25)
    x = bw("low", 3500, x, 2); return verb(np.stack([x, x], 1), F["rt"], seed, 5000.0, size, 0.0, 0.85, 0.0)
fa = frozen(F["chordA"], F["sizeA"], 7); fb_ = frozen(F["chordB"], F["sizeB"], 11)
xf = np.clip((bar - F["xf"][0]) / (F["xf"][1] - F["xf"][0]), 0, 1); xf = 0.5 - 0.5 * np.cos(np.pi * xf)
fin = np.clip((bar - F["b0"]) / 1.5, 0, 1) ** 2 * np.clip((F["end"] - bar) * BL / 0.04, 0, 1)   # 40 ms fade at the cut, no click
fz = (nm(fa) * (1 - xf)[:, None] + nm(fb_) * xf[:, None]) * (fin * (0.5 + 0.5 * np.clip((bar - F["b0"]) / (F["end"] - F["b0"]), 0, 1)))[:, None]
fz = bw("high", 150, fz, 2)
# ================= drums: soft kick, soft clap (no hats / no ticks)
K = R["kick"]
def kick1(v=1.0):
    Ln = int(K["gate"] * SR); tt = np.arange(Ln) / SR; f = K["endHz"] + (K["startHz"] - K["endHz"]) * np.exp(-tt / (K["tauMs"] / 1000))
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / K["decay"]) * np.minimum(tt / 0.004, 1); return fade(y, 60) * v
kick = np.zeros(N); clap = np.zeros(N)
for b in range(NB):
    for s16 in K["steps"]:
        bb = st(b, s16) / BL
        if on("kick", bb) and not (23.5 <= bb < 24): put(kick, kick1(1.0 if s16 == 0 else 0.8), st(b, s16)); events += 1
    if on("clap", b):
        for s16 in (4, 12):
            Ln = int(0.35 * SR); tt = np.arange(Ln) / SR
            y = bw("band", [700, 2200], rng.standard_normal(Ln), 2) * np.exp(-tt / 0.09) * np.minimum(tt / 0.008, 1); put(clap, fade(y, 20), st(b, s16)); events += 1
# ================= echo (dotted-1/8 ping-pong) + echo-wash duplicate + grain-delay shimmer (+12, low mix, automated in from the midpoint)
E_ = R["echo"]; dt_ = E_["beats"] * BT
el, er = dsp.stereo_delay(C(lead), C(lead), SR, dt_, dt_, E_["fb"], E_["fb"], 0.0, 0.0, 1, float(E_["hp"]), float(E_["lp"]), 0.0, 0.0, 0.0)
wl, wr = dsp.stereo_delay(C(wash), C(wash), SR, dt_, dt_ * 2, E_["washFb"], E_["washFb"], 0.0, 0.0, 1, float(E_["hp"]), 2800.0, 0.0, 0.0, 0.0)
S = R["shimmer"]; shin = 0.5 * (pad[:, 0] + pad[:, 1]) * 0.6 + nm(lead) * 0.4
sh = dsp.pitch_shift_delay(C(shin), SR, float(S["semis"]), S["delay"], S["fb"], 900.0, 11000.0, 0.09)
shAuto = np.clip((bar - S["from"]) / (S["to"] - S["from"]), 0, 1) ** 1.2 * S["maxSend"]
shS = np.stack([sh, np.roll(sh, int(0.011 * SR))], 1) * shAuto[:, None]
# ================= mix: duck everything lightly to the lead, kick ducks bass, huge reverb
lenv = sm(sm(np.abs(lead), 5), 200); lenv /= lenv.max() + 1e-9; duck = 1 - (1 - 10 ** (-LV["duckLeadDb"] / 20)) * np.clip(lenv * 2, 0, 1)
kenv = sm(sm(np.abs(kick), 3), 120); kenv /= kenv.max() + 1e-9
mel = pan2(nm(lead), 0.05) * LV["lead"] + nm(np.stack([el, er], 1)) * LV["echo"] + nm(np.stack([wl, wr], 1)) * LV["wash"]
padbus = (pad * LV["pad"] + pan2(vox, -0.15) * LV["vox"] + pan2(tens, 0.2) * LV["tens"]) * duck[:, None]
vb = verb(C(padbus + mel * 0.8), 6.0, 41, 6000.0, 2.2)
mix = padbus + mel + nm(vb) * LV["verb"] + nm(shS) * LV["shimmer"] + nm(fz) * LV["freeze"]
mix *= (1 - 0.1 * np.clip(kenv * 2.5, 0, 1))[:, None]
bduck = 1 - (1 - 10 ** (-LV["bassDuckDb"] / 20)) * np.clip(kenv * 2.5, 0, 1)
mix += pan2(bassUp * bduck * LV["bass"] + subS * bduck * LV["sub"] + nm(kick) * LV["kick"], 0) / np.sqrt(2) + pan2(nm(clap), 0) * LV["clap"]
sl = R["silence"]; gS = (1 - gate(sl[0], sl[1], 25))[:, None]; mix = (mix - nm(vb) * LV["verb"]) * gS + nm(vb) * LV["verb"] * (0.25 + 0.75 * gS)   # cut the full mix for 2 beats (only a -12 dB reverb tail rings); kick+bass snap back on the downbeat
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
res["events"] = events; res["lengthSec"] = round(T, 2); res["lufs"] = round(meter.integrated_loudness(mix), 2); res["drumsInSec"] = round(tb(R["drumsIn"]), 2)
side = 0.5 * (mix[:, 0] - mix[:, 1]); mid = 0.5 * (mix[:, 0] + mix[:, 1]); db = lambda x: 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)
hf = bw("high", 8000, mid, 4); he = np.abs(hf); spikes = int(np.sum(he > 8 * (sm(he, 50) + 1e-9)))
def cent(x):
    f_, tt_, Z = sg.stft(x.mean(1), SR, nperseg=4800); P_ = np.abs(Z) ** 2; c_ = (P_ * f_[:, None]).sum(0) / (P_.sum(0) + 1e-12); return float(np.median(c_))
blocks = [s["b"] for s in SEC]; sec = lambda b0, b1: mix[int(tb(b0) * SR):int(tb(b1) * SR)]
cents = [cent(sec(a, b)) for a, b in blocks]
res["checks"] = {"side_below_120Hz_db": round(db(bw("low", 120, side, 4)) - db(bw("low", 120, mid, 4)), 1), "hf_spikes_over_8x": spikes,
  "section_lufs": [round(meter.integrated_loudness(sec(a, b)), 1) if b - a >= 2 else None for a, b in blocks], "section_centroid_hz": [round(c) for c in cents],
  "centroid_span_oct": round(float(np.log2(max(cents) / min(cents))), 2), "lead_notes_per_section": counts}
json.dump(res, open(OUT + ".stats.json", "w"), indent=1, default=float)
print(json.dumps({"score": res["score"], "pass": res["pass"], "lufs": res["lufs"], "tp": res["extra"].get("true_peak_dbtp"), "gates": res["gates"], "subs": res["subs"], "tilt": res["extra"].get("tilt_db_oct"), "gr": round(gr_max, 2), "len": res["lengthSec"], "drumsIn": res["drumsInSec"], "checks": res["checks"]}, default=float))
