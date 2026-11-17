#!/usr/bin/env python3
"""Daily 3-skill test 2026-11-17 "Home Resonance" (C major/Lydian colour, 84 BPM):
  M friction-excited-modal-resonator-pad-... (noise-friction exciter + soft collision, string-profile modal bank,
    detuned 2nd resonator, warp on partials > pin with slow per-voice LFO, long ring, partial-limited additive bed
    opening, serial comb low damping -> master LP, key-tracked brilliance/level, slow env, washed verb + shimmer)
  H one-progression-to-ambient-layers-... (parallel maj7 shapes, bass = lowest note (+ alt D under Fmaj7), pad = upper 3
    tightened, common-tone D-G-A FM arp root-4-5-8, seconds dyad trill mallet, guide-tone melody w/ anticipations +
    G/A connectors, -8va double other timbre, long-attack swells on G/A, mute/unmute per section)
  A ambient-home-base-step-away-and-return-... (unchanged tonic home-base sequence w/ timbre-only motion, dry; piano
    excursions ranked by distance C -> F/G -> two-step -> Bb (borrowed) -> home, late echo copy of piano)
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
CH = R["chords"]; PROG = R["prog"]; nb_ch = lambda b: PROG[min(int(b), NB - 1)]
VO = CH["upper"]; BASS = CH["bass"]
def fm_note(f, L, ratio=2.0, idx=1.6, dec=0.6):
    tt_ = np.arange(L) / SR; ie = idx * np.exp(-tt_ / 0.25)
    y = np.sin(2 * np.pi * f * tt_ + ie * np.sin(2 * np.pi * f * ratio * tt_))
    return y * env_ar(L, 0.006, L / SR - 0.08, 0.08) * np.exp(-tt_ / dec)
def piano_note(f, L, dec=1.4):
    tt_ = np.arange(L) / SR; y = sum(np.sin(2 * np.pi * f * k * (1 + 0.0004 * k * k) * tt_) * np.exp(-tt_ * k / dec) / k ** 1.3 for k in range(1, 9))
    return y * env_ar(L, 0.004, L / SR - 0.15, 0.15)

# ================= M: friction-excited modal resonator pad playing H's tightened upper voicing
MP = R["modal"]
def modal_voice(m, L, tstart, vseed, det_c):
    f = hz(m) * 2 ** (det_c / 1200); tt_ = np.arange(L) / SR; rr = np.random.default_rng(vseed)
    kt = (m - 60) / 12.0                                                   # key tracking (octaves from C4)
    beta = MP["tilt"] - MP["brilKT"] * kt; lev = 1 + MP["levelKT"] * kt
    w = MP["warp"] + MP["warpDepth"] * np.sin(2 * np.pi * MP["warpHz"] * (1 + MP["rateOffset"] * (vseed % 5 - 2)) * (tstart + tt_) + vseed)
    y = np.zeros(L); bwlp = 1 / (np.pi * MP["ringSec"])                   # ring time -> resonance bandwidth of each mode
    for k in range(1, MP["partials"] + 1):
        fk = f * k if k <= MP["pin"] else f * (MP["pin"] + (k - MP["pin"]) * (1 + w))
        if np.max(fk) > 15000: break
        nz = sm(rr.standard_normal(L), 1000 / (2 * np.pi * max(bwlp, 0.05)) )  # friction noise through mode resonance
        nz = nz / (np.std(nz) + 1e-9); a = (1 - MP["frictionVar"]) + MP["frictionVar"] * np.tanh(nz)
        ph = 2 * np.pi * np.cumsum(fk) / SR + rr.uniform(0, 2 * np.pi)
        y += np.sin(ph) * a / k ** beta
    hit = np.exp(-tt_ / 0.25) * MP["collision"]                            # soft collision impulse (gentle attack)
    return y * lev * (1 + hit)
padL = np.zeros(N); padR = np.zeros(N); bed = np.zeros(N); events = 0
b = 0
while b < NB:                                                              # merge repeated chords into one held note-on
    c = nb_ch(b); e = b
    while e < NB and nb_ch(e) == c: e += 1
    hold = (e - b) * BL; L = int((hold + MP["release"]) * SR); en = env_ar(L, MP["attack"], hold, MP["release"])
    for j, m in enumerate(VO[c]):
        put(padL, modal_voice(m, L, tb(b), 100 * b + j, -MP["detuneC"]) * en, tb(b))
        put(padR, modal_voice(m, L, tb(b), 100 * b + j + 50, MP["detuneC"]) * en, tb(b))
        # bed: partial-limited additive saw, partial count opening with an envelope, mixed lower
        tt_ = np.arange(L) / SR; cnt = MP["bedFrom"] + (MP["bedTo"] - MP["bedFrom"]) * np.clip(tt_ / MP["bedOpenSec"], 0, 1)
        f = hz(m - 12); bd = sum(np.sin(2 * np.pi * f * k * tt_ + k) / k * np.clip(cnt - k + 1, 0, 1) for k in range(1, int(MP["bedTo"]) + 1))
        put(bed, bd * en, tb(b)); events += 2
    b = e
pad = np.stack([padL, padR], 1) + pan2(nm(bed) * MP["bedLevel"] * np.max(np.abs(padL)), 0.0)
dl = np.full(N, SR / hz(MP["combMidi"]))                                   # serial comb, low damping (long ring), partial wet
pad = np.stack([dsp.comb_ff_fb(C(pad[:, c]), C(dl), MP["combFb"], MP["combMix"]) for c in range(2)], 1)
pad = bw("low", MP["lp"], bw("high", MP["hp"], pad, 2), 2)
pv = verb(pad, MP["verbRt"], 3, 9000.0, 2.6)
shm = dsp.pitch_shift_delay(C(nm(pv.mean(1))), SR, 12.0, 0.22, 0.3, 600.0, 9000.0, 0.1); shm = np.stack([shm, np.roll(shm, int(0.019 * SR))], 1)
pad = nm(pad) * (1 - MP["wet"]) + nm(pv) * MP["wet"] + nm(shm) * MP["shimmer"]
env = sm(sm(np.abs(pad).mean(1), 20), 300); pad = pad / (1 + 0.6 * env / (env.max() + 1e-9))[:, None]   # light leveller
S = R["sections"]
padG = gate(0, S["breakStart"], 1500) + gate(S["breakEnd"], S["end"] + 2, 1500)  # H9: pad drops out in the break
pad = pad * padG[:, None]

# ================= H: bass (lowest note; alt bass under some chords), FM arp, dyad trill, melody + double, swells
bass = np.zeros(N)
for b in range(S["drumsIn"], S["drumsOut"]):
    if S["breakStart"] <= b < S["breakEnd"]: continue
    c = nb_ch(b); m = R["altBass"].get(str(b), BASS[c]); L = int(BL * SR)
    f = hz(m); tt_ = np.arange(L) / SR
    put(bass, (np.sin(2 * np.pi * f * tt_) + 0.25 * np.sin(4 * np.pi * f * tt_)) * env_ar(L, 0.03, BL - 0.25, 0.25), tb(b)); events += 1
bass = bw("low", 300, bass, 2)
AR = R["arp"]; arp = np.zeros(N)
for b in range(S["arpIn"], S["drumsOut"]):
    for i in range(8):
        m = AR["notes"][i % len(AR["notes"])]; L = int(E8 * SR * 1.8)
        put(arp, fm_note(hz(m), L, AR["ratio"], AR["index"]), tb(b) + i * E8); events += 1
arp = bw("low", AR["lp"], bw("high", 200, arp, 2), 2); arpS = np.stack([arp, np.roll(arp, int(0.37 * BT * SR))], 1)
arpS = nm(arpS) * 0.7 + nm(verb(arpS, 3.5, 11, 7000.0, 2.0)) * 0.4
DY = R["dyads"]; dy = np.zeros(N)
for b in list(range(S["arpIn"], S["drumsOut"])):
    pair = DY["pairs"][nb_ch(b)]
    for h in range(2):                                         # slow trill: alternate two dyads every half bar
        top = pair[h]; L = int((BL / 2 + 1.2) * SR)
        for mm in (top, top - DY["third"][nb_ch(b)][h]):
            put(dy, fm_note(hz(mm), L, 4.0, 0.5, 1.1) * 0.8 + piano_note(hz(mm), L, 2.0) * 0.4, tb(b) + h * BL / 2); events += 1
dy = bw("low", 6000, dy, 2); dyS = pan2(nm(dy), -0.3); dyS = dyS * 0.55 + nm(verb(dyS, 5.0, 13, 7000.0, 2.2)) * 0.6
dyS *= (gate(S["arpIn"], S["drumsOut"], 400) * (DY["level"] + DY["breakBoost"] * gate(S["breakStart"], S["breakEnd"], 800)))[:, None]
ME = R["melody"]; mel = np.zeros(N); dbl = np.zeros(N)
for b in range(S["melIn"], S["melOut"]):
    if S["breakStart"] <= b < S["breakEnd"]: continue
    c = nb_ch(b); g = ME["guide"][c][b % 2]; ant = ME["anticipate"] * BT if (b > 0 and nb_ch(b) != nb_ch(b - 1)) else 0
    for s0, mm, dur in ((tb(b) - ant, g, 3 * BT + ant), (tb(b) + 3 * BT, ME["connectors"][b % 2], BT)):
        L = int((dur + 0.6) * SR); f = hz(mm)
        put(mel, (osc(f, L, 1, 0.3) * 0.6 + np.sin(2 * np.pi * f * np.arange(L) / SR)) * env_ar(L, 0.05, dur, 0.6), s0)
        put(dbl, osc(f / 2, L, 2, 0.1) * env_ar(L, 0.08, dur, 0.6), s0 + 0.012); events += 2
mel = bw("low", ME["lp"], mel, 2); dbl = bw("low", 1800, bw("high", 150, dbl, 2), 2)
melS = pan2(nm(mel), 0.1) * 0.7 + pan2(nm(dbl), -0.15) * ME["doubleLevel"]; melS = melS + nm(verb(melS, 4.5, 17, 7000.0, 2.2)) * 0.45
SW = R["swells"]; sw = np.zeros(N)
for b0, mm in SW["notes"]:
    L = int((2 * BL + 2.5) * SR); f = hz(mm)
    put(sw, sum(osc(f * 2 ** (d / 1200), L, 0, p) for d, p in ((-4, 0.2), (4, 0.7))) * env_ar(L, SW["attack"], 2 * BL, 2.5), tb(b0)); events += 1
sw = bw("low", 4000, bw("high", 250, sw, 2), 2); swS = nm(verb(pan2(nm(sw), 0.2), 7.0, 19, 6000.0, 2.8)) * 0.8 + pan2(nm(sw), 0.2) * 0.25

# ================= A: home base (unchanged tonic 2-voice sequence, timbre-only motion, dry) + piano excursions + late echo
HB = R["home"]; hb = np.zeros(N); step = HB["stepBeats"] * BT; k = 0; s0 = 0.0
while s0 < tb(S["end"]):
    mm = HB["notes"][k % len(HB["notes"])]; L = int(step * 1.6 * SR); f = hz(mm)
    put(hb, (osc(f, L, 1, 0.5) * 0.5 + np.sin(2 * np.pi * f * np.arange(L) / SR)) * env_ar(L, 0.03, step * 1.1, step * 0.5), s0); events += 1
    k += 1; s0 += step
hcut = HB["lpFrom"] * (HB["lpTo"] / HB["lpFrom"]) ** (0.5 - 0.5 * np.cos(2 * np.pi * HB["lfoHz"] * t))   # timbre motion only
hb = dsp.ladder(C(hb * 0.4), C(hcut), 0.15, 0.1, 0, 0, SR); hb = bw("high", 120, hb, 2)
hbS = pan2(nm(hb), 0.0) * gate(0, S["end"], 600)[:, None]
PI = R["piano"]; pn = np.zeros(N)
for b in range(S["drumsIn"], S["end"]):
    c = nb_ch(b); notes = [BASS[c] + 12] + VO[c]
    for q, sub in ((0, notes), (2, VO[c][1:])):
        for mm in sub:
            L = int(2.2 * BT * SR); put(pn, piano_note(hz(mm), L), tb(b) + q * BT + 0.006 * sub.index(mm)); events += 1
pn = bw("low", PI["lp"], bw("high", 140, pn, 2), 2)
echo = bw("low", 2500, np.roll(pn, int(PI["echoOffsetBeats"] * BT * SR)), 2)
pnS = pan2(nm(pn), -0.1) + pan2(nm(echo), 0.35) * PI["echoLevel"]; pnS = pnS + nm(verb(pnS, 3.5, 23, 6500.0, 2.0)) * 0.35
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
drum_on = lambda b: S["drumsIn"] <= b < S["drumsOut"] and not (S["breakStart"] <= b < S["breakEnd"])
for b in range(NB):
    if not drum_on(b): continue
    for q in (0, 2): put(kick, k1, tb(b) + q * BT); events += 1
    for q in (1, 3): put(sn, snare1(), tb(b) + q * BT); events += 1
    if b >= S["layersIn"]:
        for q in range(4): put(shk, shaker1(), tb(b) + (q + 0.5) * BT); events += 1
snS = pan2(sn, 0.05); snS = nm(snS) * 0.6 + nm(verb(snS, 3.0, 37, 6000.0, 2.0)) * 0.5
shS = pan2(bw("high", 5000, bw("low", 10000, shk, 2), 2), 0.2); shS = nm(shS) * 0.6 + nm(verb(shS, 3.0, 41, 7000.0, 2.0)) * 0.4
dbus = pan2(nm(kick), 0) / np.sqrt(2) * DM["kick"] + snS * DM["snare"] + shS * DM["shaker"]
kenv = sm(sm(np.abs(kick), 5), 90); kenv /= kenv.max() + 1e-9
duck = lambda d: (1 - (1 - 10 ** (-d / 20)) * np.clip(kenv * 2.5, 0, 1))[:, None]

if os.environ.get("DBG"):
    def spk(x):
        x = x.mean(1) if x.ndim == 2 else x; he = np.abs(bw("high", 8000, x, 4)); return int(np.sum(he > 8 * (sm(he, 50) + 1e-9)))
    for nmx, x in (("pad", pad), ("arp", arpS), ("dy", dyS), ("mel", melS), ("home", hbS), ("piano", pnS), ("drums", dbus)): print(nmx, spk(x))
    sys.exit()
# ================= mix + master
Mm = R["master"]
LV = R["levels"]
mix = (nm(pad) * LV["pad"] * duck(LV["padDuck"]) + arpS * LV["arp"] + dyS + melS * LV["melody"] + swS * LV["swells"] + hbS * LV["home"]
       + pnS * LV["piano"] + pan2(nm(bass) * LV["bass"], 0) / np.sqrt(2) + dbus)
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
sec = lambda b0, b1: mix[int(tb(b0) * SR):int(tb(b1) * SR)]
res["checks"] = {"side_below_120Hz_db": round(db(bw("low", 120, side, 4)) - db(bw("low", 120, mid, 4)), 1), "hf_spikes_over_8x": spikes,
  "hf_env_12_40_vs_0_12_db": round(10 * np.log10(Pw[(fq >= 12) & (fq <= 40)].mean() / Pw[(fq > 0.2) & (fq < 12)].mean()), 1),
  "lufs_intro_A_B_break_C_outro": [round(meter.integrated_loudness(sec(a, b)), 1) for a, b in ((0, 4), (4, 12), (12, 20), (20, 22), (22, 26), (26, 28))]}
json.dump(res, open(OUT + ".stats.json", "w"), indent=1, default=float)
print(json.dumps({"score": res["score"], "pass": res["pass"], "lufs": res["lufs"], "tp": res["extra"].get("true_peak_dbtp"), "gates": res["gates"], "subs": res["subs"], "tilt": res["extra"].get("tilt_db_oct"), "gr": round(gr_max, 2), "len": res["lengthSec"], "drumsIn": res["drumsInSec"], "checks": res["checks"]}, default=float))
