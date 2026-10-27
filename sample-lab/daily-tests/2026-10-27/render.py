#!/usr/bin/env python3
"""Daily 3-skill test 2026-10-27 "Held Light": self-sustaining shimmer pad (source/space) + synth drum kit from scratch (drums)
+ loop-is-the-climax give-away arrangement (structure). usage: render.py recipe.json out.wav (original synthesis, deterministic)"""
import sys, os, json, numpy as np, soundfile as sf, pyloudnorm as pyln
from scipy import signal as sg
LAB = os.environ.get("LAB", "/workspace/skill-library/sample-lab"); sys.path.insert(0, LAB + "/engine")
import dsp, metrics
SR = 48000
R = json.load(open(sys.argv[1])); OUT = sys.argv[2]; rng = np.random.default_rng(R["seed"])
bar = 240 / R["bpm"]; beat = bar / 4; T = R["bars"] * bar + R["tailSec"]; N = int(T * SR); t = np.arange(N) / SR
hz = lambda m: 440 * 2 ** ((m - 69) / 12); S = R["sections"]; PR = R["progression"]; D = R["drums"]
def sos(k, f, o=2): return sg.butter(o, f, k, fs=SR, output="sos")
def pan2(x, p): return np.stack([x * np.cos((p + 1) * np.pi / 4), x * np.sin((p + 1) * np.pi / 4)], 1) * np.sqrt(2)
def ramp(b0, b1): return np.clip((t - b0 * bar) / ((b1 - b0) * bar), 0, 1)
def gate(b0, b1): return ((t >= b0 * bar) & (t < b1 * bar)).astype(float)
def smooth(x, ms=20): n = int(ms * SR / 1000); return sg.filtfilt(np.ones(n) / n, [1], x)
def put(buf, y, s, g=1.0):
    i = int(round(s * SR)); L = min(len(y), N - i)
    if L > 0: buf[i:i + L] += y[:L] * g
def prog(b): return PR[int(b) % len(PR)]          # one chord per bar, 4-bar loop
events = 0
# ===== SKILL A: self-sustaining shimmer pad. Steps 1-3: 4-note phrase played ONCE into a 100%-wet stereo delay, L 1 s / R 150 ms, fb 0.99, no cross-feed
SH = R["shimmer"]; src = np.zeros(N)
for j, m in enumerate(SH["notes"]):
    L = int(SH["noteBeats"] * beat * SR); tt = np.arange(L) / SR; f = hz(m)
    y = (np.sin(2*np.pi*f*tt) + 0.3*np.sin(2*np.pi*2*f*tt) + 0.12*np.sin(2*np.pi*3*f*tt)) * np.clip(tt/0.01, 0, 1) * np.exp(-tt/0.5)
    y[-480:] *= np.linspace(1, 0, 480); put(src, y, 0.25 + j * SH["noteBeats"] * beat); events += 1
def fb_delay(x, d, fb, lp):
    y = x.copy(); a = np.exp(-2*np.pi*lp/SR)
    for i in range(d, N, d):              # block recursion y[n] = x[n] + fb*LP(y[n-d]); gentle in-loop LP keeps 99% fb from going brittle
        e = min(N, i + d); prev = sg.lfilter([1 - a], [1, -a], y[i - d:e - d]); y[i:e] += fb * prev
    return y
shL = fb_delay(src, int(SH["delayL"] * SR), SH["fb"], SH["loopLp"]); shR = fb_delay(src, int(SH["delayR"] * SR), SH["fb"], SH["loopLp"])
sh = np.stack([shL, shR], 1)
# step 5: level automation after the delay so the texture stays stable (slow RMS normalise), then arrangement level
rms = np.sqrt(smooth(np.mean(sh**2, 1), 800) + 1e-9); sh /= (rms / np.median(rms[int(4*SR):int(40*SR)]))[:, None] ** 0.85
sh = np.stack([sg.sosfilt(sos("high", 180), sh[:, c]) for c in range(2)], 1)
shenv = np.clip(t / 1.0, 0, 1) * (1 - 0.35 * ramp(S["outro"] + 4, S["end"]))
sh *= (shenv * SH["level"] / (np.max(np.abs(sh)) + 1e-9))[:, None]
dry = sh.copy(); verb = sh * 0.5
# ===== SKILL B: synth drum kit from scratch
# step 3 kick: sine pitched down an octave via a fast 0.07 s pitch env, short amp env, soft clip, light bitcrush, cut 400 Hz, HP
Lk = int(0.45*SR); tk = np.arange(Lk)/SR; fk = 52 * (1 + np.exp(-tk/0.07))
kick = np.tanh(2.2*np.sin(2*np.pi*np.cumsum(fk)/SR) * np.exp(-tk/0.16)); kick[:24] *= np.linspace(0, 1, 24)
kick = np.round(kick * 512) / 512; kick = dsp.eq(kick, "peak", 400, 1.2, -5); kick = sg.sosfilt(sos("high", 30), kick)
# steps 1-2 808: sine ~45-49 Hz + LP saw + noise on a dip-then-decay env (1.6 s), soft drive, gentle 1st-order 20 Hz HP, narrow 78 Hz bell cut
def b808(f0, dur):
    L = int(dur*SR); tt = np.arange(L)/SR; env = np.exp(-tt/0.7) * np.clip(tt/0.003, 0, 1)
    tr = np.exp(-tt/0.012) * (1 - 0.6*np.clip(tt/0.004, 0, 1))
    saw = sg.sosfilt(sos("low", 300), dsp.osc_va(np.full(L, f0), 0, 0.5, 0.0, SR))
    y = np.sin(2*np.pi*f0*tt)*env + 0.25*saw*tr + 0.15*rng.standard_normal(L)*tr
    y = dsp.eq(y, "peak", 900, 0.8, 2.0); y = np.tanh(1.6*y)/np.tanh(1.6)
    y = sg.sosfilt(sos("high", 20, 1), y); y = dsp.eq(y, "peak", D["notchHz"], 6.0, D["notchDb"]); y[-960:] *= np.linspace(1, 0, 960); return y
# step 4 clap: three quick transients then a longer decay (~0.085 s grid), BP above 600 with 1k/6k bells, little above 11 kHz; step 5 short-delay width
Lc = int(0.4*SR); tc = np.arange(Lc)/SR; g9 = 0.085/9
cenv = sum(np.exp(-np.clip(tc - k*g9, 0, None)/0.004)*(tc >= k*g9) for k in range(3)) + 1.2*np.exp(-np.clip(tc-3*g9, 0, None)/0.07)*(tc >= 3*g9)
clap = sg.sosfilt(sos("high", 600), rng.standard_normal(Lc)*cenv); clap = dsp.eq(dsp.eq(clap, "peak", 1000, 1.0, 5), "peak", 6000, 1.5, 3)
clap = sg.sosfilt(sos("low", 11000, 4), clap); clapS = np.stack([clap, np.concatenate([np.zeros(int(0.011*SR)), clap[:-int(0.011*SR)]])*0.9], 1)
# step 6 snare: sines 240/484/1000 with a short pitch env + noise with two transients through one filter, drive, blend some clap
Lsn = int(0.35*SR); ts = np.arange(Lsn)/SR; pe = 1 + 0.5*np.exp(-ts/0.01)
ton = sum(a*np.sin(2*np.pi*np.cumsum(f*pe)/SR)*np.exp(-ts/d) for f, a, d in ((240, 1.0, 0.09), (484, 0.5, 0.06), (1000, 0.2, 0.04)))
nz = rng.standard_normal(Lsn)*(np.exp(-ts/0.11) + 0.8*np.exp(-np.clip(ts-0.012, 0, None)/0.005)*(ts >= 0.012))
snare = np.tanh(1.8*sg.sosfilt(sos("band", [180, 9000]), 0.6*ton + 0.5*nz)); snare[:24] *= np.linspace(0, 1, 24)
snare = snare + 0.4*clap[:Lsn]
# step 7 hats: closed = short noise tick (HP but keep some mids); open = longer env with a 2nd small transient
Lh = int(0.22*SR); th = np.arange(Lh)/SR; hatc = sg.sosfilt(sos("high", 5000), rng.standard_normal(Lh))*np.exp(-th/0.025) + 0.15*sg.sosfilt(sos("band", [2500, 5000]), rng.standard_normal(Lh))*np.exp(-th/0.01)
Lo = int(0.5*SR); to = np.arange(Lo)/SR; hato = sg.sosfilt(sos("high", 5500), rng.standard_normal(Lo))*(np.exp(-to/0.14) + 0.4*np.exp(-np.clip(to-0.02, 0, None)/0.01)*(to >= 0.02))
# ===== SKILL C: loop-is-the-climax give-away arrangement (8-bar sections; drums from bar 5 per Matt, kick HP'd at 120 Hz until the drop)
K = np.zeros(N); CL = np.zeros((N, 2)); SN = np.zeros(N); HC = np.zeros(N); HO = np.zeros(N); B8 = np.zeros(N)
sw = 0.55
for b in range(S["introEnd"], S["end"]):
    for k in range(16):
        tb = (b + k/16) * bar; st = tb + (sw - 0.5)*2*(beat/4)*(k % 2)
        main = S["drop"] <= b < S["outro"]
        gap = b in S["kickGapBars"] or b == S["outro"] - 1 and k >= 12      # step 4: kick bar deleted before the drop; step 8: near-silence beat before outro
        if k % 4 == 0 and not gap and b < S["end"] - 1: put(K, kick, tb); events += 1
        if b >= 8 and k in (2, 6, 10, 14) and not (b == S["kickGapBars"][0] and k > 8) and b < S["end"] - 2: put(HC, hatc, st, 0.5 + 0.3*(k == 10)); events += 1  # shaker/hat staged early-ish
        if main and k % 2 == 1: put(HC, hatc, st, 0.3)
        if main and k in (4, 12) and not (b == S["outro"] - 1 and k == 12): put(SN, snare, tb); put(CL[:, 0], clapS[:, 0], tb); put(CL[:, 1], clapS[:, 1], tb); events += 1
        if main and k == 14 and b % 2 == 1: put(HO, hato, st); events += 1
    if S["drop"] <= b < S["outro"]:                                      # 808 only in the climax, following chord roots
        for k, dur in ((0, 1.4), (10, 0.9)): f0 = hz(prog(b)[0] - 12) if prog(b)[0] - 12 > 30 else hz(prog(b)[0]); put(B8, b808(max(f0, 38.0), dur), (b + k/16)*bar); events += 1
# step 3/8/9: kick high-passed at 120 Hz until the drop, opened over the last beat into it, HP again for the outro (mirror)
khp = S["kickHpHz"] * (1 - gate(S["drop"], S["outro"])) + 30 * gate(S["drop"], S["outro"])
khp = np.maximum(30, smooth(khp, 60)); K = np.concatenate([dsp.svf(K, khp, 0.707, 2, SR)])
# step 6: bass = root pedal (G) thin and dark early with octave jump at end of each 8 bars, HP/LP opening; full progression at the drop; outro back to pedal and darker
bass = np.zeros(N)
for b in range(S["introEnd"], S["end"]):
    root = 43 if not (S["drop"] <= b < S["outro"]) else prog(b)[0]
    if b in (S["drop"] - 1, S["outro"] + 7) : root += 12                 # octave jump at the end of 8 bars
    L = int(bar*SR*1.02); tt = np.arange(L)/SR; f = hz(root)
    y = dsp.osc_va(np.full(L, f), 0, 0.5, rng.random(), SR)*0.6 + np.sin(2*np.pi*f*tt)
    y *= np.clip(tt/0.02, 0, 1)*np.clip((L/SR - tt)/0.05, 0, 1); put(bass, y, b*bar)
bhp = 160 * (1 - ramp(S["kickHpEnd"] - 4, S["drop"])) + 30; bhp = bhp * (1 - gate(S["drop"], S["outro"])) + 30 * gate(S["drop"], S["outro"]) + 100 * ramp(S["outro"], S["end"])
blp = 400 + 1600 * ramp(S["introEnd"], S["drop"]) ; blp = blp * (1 - ramp(S["outro"], S["end"]) * 0.8)
bass = dsp.svf(bass, np.maximum(25, smooth(bhp, 80)), 0.707, 2, SR); bass = dsp.svf(bass, smooth(blp, 80), 0.9, 0, SR)
bass *= np.clip((S["end"]*bar - t)/bar, 0, 1) * (1 - 0.35*gate(S["drop"], S["outro"]))
# step 7: melody enters as fragments (first 2 notes of each 2-bar phrase, LP filtered in), full line + chord pad only at the climax
ML = R["melody"]; mel = np.zeros(N)
for b in range(8, S["outro"] + 4, 2):
    full = S["drop"] <= b < S["outro"]; notes = ML["notes"] if full else ML["notes"][:2] if b < S["drop"] else ML["notes"][::-1][:3]
    for j, m in enumerate(notes):
        L = int(beat*SR*(1.0 if full else 1.8)); tt = np.arange(L)/SR; f = hz(m)
        y = (dsp.osc_va(np.full(L, f), 2, 0.5, 0.0, SR) + 0.4*np.sin(2*np.pi*2*f*tt)) * np.clip(tt/0.008, 0, 1)*np.exp(-tt/0.6); y[-480:] *= np.linspace(1, 0, 480)
        put(mel, y, (b + j/4)*bar); events += 1
mlp = 900 + 4100*ramp(8, S["drop"]) - 3000*ramp(S["outro"], S["outro"] + 4)
mel = dsp.svf(mel, smooth(mlp, 50), 0.8, 0, SR) * ML["level"]
CP = R["chordPad"]; pad = np.zeros((N, 2))
for b in range(S["drop"] - 2, S["outro"] + 2):
    L = int(bar*SR*1.05)
    for i, m in enumerate(prog(b)[1]):
        for u, d in enumerate((-7, 7)):
            put(pad[:, u], dsp.osc_va(np.full(L, hz(m)*2**(d/1200)), 0, 0.5, rng.random(), SR)*np.clip(np.arange(L)/SR/0.3, 0, 1)*np.clip((L/SR - np.arange(L)/SR)/0.2, 0, 1), b*bar)
plp = CP["lpLo"] + (CP["lpHi"] - CP["lpLo"]) * smooth(ramp(S["drop"] - 2, S["drop"]) * (1 - ramp(S["outro"], S["outro"] + 2)), 30)
pad = np.stack([dsp.svf(pad[:, c], plp, 0.8, 0, SR) for c in range(2)], 1); pad = np.stack([sg.sosfilt(sos("high", 150), pad[:, c]) for c in range(2)], 1)
pad *= (CP["level"] / (np.max(np.abs(pad)) + 1e-9)) * (gate(S["drop"] - 2, S["outro"] + 2))[:, None] if False else (CP["level"] / (np.max(np.abs(pad)) + 1e-9))
# sidechain duck (strings/pad/bass under kick)
kev = np.clip(sg.lfilter([1], [1, -np.exp(-1/(0.1*SR))], (np.abs(K) > 0.3).astype(float))*0.05, 0, 1)
duck = 1 - 0.35*kev
dry += pan2(mel, -0.15) + pad*duck[:, None]; verb += pan2(mel, 0.2)*0.6 + pad*0.4
dry += pan2(bass*0.32*duck, 0.0) + pan2(B8*D["b808"], 0.0) + pan2(K*D["kick"], 0.0)
dry += CL*D["clap"] + pan2(SN*D["snare"], 0.05) + pan2(HC*D["hat"], 0.3) + pan2(HO*D["ohat"], -0.3)
verb += CL*D["clap"]*0.4 + pan2(HO*D["ohat"], 0.0)*0.6
vs = np.stack([sg.sosfilt(sos("high", 250), verb[:, c]) for c in range(2)], 1)
wl, wr = dsp.fdn_reverb(vs[:, 0].copy(), vs[:, 1].copy(), SR, 4.5, 1.3, 7000.0, 0.02, 0.0, 0.75, 0.3, 3)
mix = dry + 0.35*np.stack([wl, wr], 1)
Mm = R["master"]; mix = sg.sosfiltfilt(sos("high", 20), mix, axis=0)
mix = np.tanh(Mm["satDrive"]*mix/(np.max(np.abs(mix)) + 1e-9))/np.tanh(Mm["satDrive"])
M = 0.5*(mix[:, 0] + mix[:, 1]); Sd = 0.5*(mix[:, 0] - mix[:, 1]); Sd = sg.sosfiltfilt(sos("high", Mm["sideHpHz"], 4), Sd); mix = np.stack([M + Sd, M - Sd], 1)
fi = np.clip(t/Mm["fadeInSec"], 0, 1); fo = np.clip((T - 0.3 - t)/Mm["fadeOutSec"], 0, 1)**2; mix *= (fi*fo)[:, None]; mix -= mix.mean(0)
meter = pyln.Meter(SR); gr_max = 0.0
for it in range(5):
    mix *= 10**((Mm["targetLufs"] - meter.integrated_loudness(mix))/20)
    tp = np.maximum(dsp.true_peak_env(mix[:, 0]), dsp.true_peak_env(mix[:, 1])); ceil = 10**(Mm["tpCeil"]/20); la = int(0.005*SR)
    g0 = np.minimum(1, ceil/np.maximum(tp, 1e-9)); g = np.minimum.reduce([np.roll(g0, k) for k in range(-la, la + 1, 24)]); g = np.minimum(sg.filtfilt(np.ones(la)/la, [1], g), 1)
    gr_max = max(gr_max, -20*np.log10(g.min())); mix *= g[:, None]
    if abs(meter.integrated_loudness(mix) - Mm["targetLufs"]) < 0.3: break
mix[-int(0.3*SR):] = 0; mix[:2] = 0; mix -= mix.mean(0)
sf.write(OUT, mix.astype(np.float32), SR, subtype="PCM_24")
res = metrics.compute(mix, {"limiter_gr_db": gr_max}, R.get("category", "pad"), False, R["bars"]*bar, start_body_s=0.0, f_low=hz(43), bar_s=bar)
res["events"] = events; res["lengthSec"] = round(T, 2); res["lufs"] = round(meter.integrated_loudness(mix), 2)
json.dump(res, open(OUT + ".stats.json", "w"), indent=1, default=float)
print(json.dumps({"score": res["score"], "pass": res["pass"], "lufs": res["lufs"], "tp": res["extra"].get("true_peak_dbtp"), "gates": res["gates"], "subs": res["subs"], "events": events, "gr": round(gr_max, 2)}, default=float))
