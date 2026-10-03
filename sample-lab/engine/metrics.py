"""Quality metrics + composite score exactly as specified in ../TARGET.md (v1)."""
import numpy as np
import pyloudnorm as pyln
from scipy import signal
import dsp
from dsp import SR

BANDS = {  # (lo, hi) per category group; None = unbounded
    "pad":   dict(M1=(-18, -13), M2=(None, 3.0), M3=(0.15, 0.90), M4=(0.25, 0.85), M5=(None, -15), M6=(-6.5, -2.0),
                  M7=(None, 9), M8=(None, 8), M9=(None, -12), M10=(0.06, 0.9), M11=(0.010, 0.30), M12=(None, -24),
                  M13=(None, 0.0), M14=(None, 3.0), M15=(None, 1.5)),
    "pluck": dict(M1=(-18, -13), M2=(None, 3.0), M3=(0.15, 0.95), M4=(0.15, 0.80), M5=(None, -15), M6=(-6.5, -1.5),
                  M7=(None, 9), M8=(None, 8), M9=(None, -10), M10=(0.10, 1.5), M11=(0.02, 0.5), M12=(None, -22),
                  M13=(None, 0.0), M14=(None, 4.0), M15=(None, 1.5)),
    "bass":  dict(M1=(-17, -12), M2=(None, 1.0), M3=(0.80, None), M4=(0.0, 0.35), M5=(None, -20), M6=(-9, -3),
                  M7=(None, 10), M8=(None, 8), M9=(None, -16), M10=(0.04, 1.0), M11=(0.005, 0.3), M12=(None, -30),
                  M13=(None, 0.0), M14=(None, 4.0), M15=(None, 1.5)),
}
TOL = dict(M1=4, M2=3, M3=0.3, M4=0.3, M5=10, M6=2, M7=6, M8=6, M9=6, M10=0.05, M11=0.02, M12=8, M13=0.10, M14=4, M15=3)
WEIGHT = dict(M1=1.0, M2=1.5, M3=1.0, M4=1.0, M5=1.5, M6=1.0, M7=1.0, M8=1.5, M9=1.0, M10=1.5, M11=0.75, M12=0.75,
              M13=0.75, M14=1.0, M15=1.0)
PASS_SCORE = 85.0

def group_of(cat):
    return {"pluck": "pluck", "bass": "bass"}.get(cat, "pad")

def sub_score(v, band, tol):
    lo, hi = band
    if v is None or not np.isfinite(v):
        return 0.0
    if lo is not None and v < lo:
        return max(0.0, 1 - (lo - v) / tol)
    if hi is not None and v > hi:
        return max(0.0, 1 - (v - hi) / tol)
    return 1.0

def ltas(x, nper=16384):
    f, P = signal.welch(x, SR, nperseg=nper)
    return f, P

def compute(audio, info, category, is_loop, note_off_s, start_body_s=None):
    L, R = audio[:, 0], audio[:, 1]
    M = 0.5 * (L + R); S = 0.5 * (L - R)
    meter = pyln.Meter(SR)
    m = {}
    gates = {}
    gates["G7_finite"] = bool(np.all(np.isfinite(audio)))
    tp = max(np.max(dsp.true_peak_env(L)), np.max(dsp.true_peak_env(R)))
    m["true_peak_dbtp"] = 20 * np.log10(tp + 1e-12)
    gates["G1_true_peak"] = m["true_peak_dbtp"] <= -1.0
    m["clipped"] = int(np.sum(np.abs(audio) >= 0.999))
    gates["G2_no_clip"] = m["clipped"] == 0
    m["dc"] = float(np.max(np.abs(audio.mean(0))))
    gates["G3_dc"] = m["dc"] <= 0.001
    if is_loop:
        jump = float(np.max(np.abs(audio[0] - audio[-1])))
        m["loop_jump"] = jump
        gates["G5_tail_or_loopclick"] = jump <= 0.02
        gates["G6_start"] = True
    else:
        tail = audio[-int(0.1 * SR):]
        m["tail_rms_db"] = 20 * np.log10(np.sqrt(np.mean(tail ** 2)) + 1e-12)
        gates["G5_tail_or_loopclick"] = m["tail_rms_db"] <= -60
        m["start_peak_db"] = 20 * np.log10(np.max(np.abs(audio[:int(0.002 * SR)])) + 1e-12)
        gates["G6_start"] = m["start_peak_db"] <= -30
    v = {}
    v["M1"] = meter.integrated_loudness(audio)
    mono = np.stack([M, M], 1)
    v["M2"] = v["M1"] - meter.integrated_loudness(mono)
    v["M3"] = float(np.corrcoef(L, R)[0, 1])
    v["M4"] = float(np.sqrt(np.mean(S ** 2)) / (np.sqrt(np.mean(M ** 2)) + 1e-12))
    sos = signal.butter(4, 150, "low", fs=SR, output="sos")
    Ml = signal.sosfilt(sos, M); Sl = signal.sosfilt(sos, S)
    v["M5"] = 10 * np.log10((np.mean(Sl ** 2) + 1e-20) / (np.mean(Ml ** 2) + 1e-20))
    f, P = ltas(M + 1e-12 * 0 + 0.0 * S)
    Pst = ltas(L)[1] + ltas(R)[1]
    # octave bands 63..8k
    centres = 63 * 2.0 ** np.arange(0, 8)  # 63..8064
    ob = []
    for c in centres:
        sel = (f >= c / np.sqrt(2)) & (f < c * np.sqrt(2))
        ob.append(10 * np.log10(np.sum(Pst[sel]) + 1e-20))
    ob = np.array(ob)
    # tilt fit 100 Hz - 10 kHz using octave bands 125..8k
    sel = (centres >= 100) & (centres <= 10000)
    x = np.log2(centres[sel]); y = ob[sel]
    # band energy sums grow +3 dB/oct for flat-per-Hz; convert to per-Hz density slope
    y_d = y - 10 * np.log10(centres[sel])
    k, b = np.polyfit(x, y_d, 1)
    v["M6"] = float(k + 3.0)  # report as slope of octave-band level (pink = 0) minus 3 => pink=-3 dB/oct per-Hz density
    fit = k * np.log2(centres) + b + 10 * np.log10(centres)
    v["M7"] = float(np.max(np.abs(ob - fit)))
    # harshness prominence 1.5-8 kHz: 1/24-oct vs 1/3-oct smoothing on log grid
    fl = np.geomspace(100, 16000, 24 * 8)
    Pi = np.interp(fl, f, Pst) + 1e-20
    Pd = 10 * np.log10(Pi)
    win = 8  # 1/3 octave = 8 bins of 1/24
    sm = np.convolve(np.pad(Pd, win, mode="edge"), np.ones(2 * win + 1) / (2 * win + 1), mode="same")[win:-win]
    hs = (fl >= 1500) & (fl <= 8000)
    v["M8"] = float(np.max((Pd - sm)[hs]))
    tot = np.sum(Pst[f > 20]) + 1e-20
    v["M9"] = 10 * np.log10(np.sum(Pst[(f >= 2000) & (f <= 5000)]) / tot + 1e-20)
    v["M12"] = 10 * np.log10(np.sum(Pst[f >= 12000]) / tot + 1e-20)
    # temporal: frames of 100 ms over body
    hop = int(0.1 * SR)
    if is_loop:
        b0, b1 = 0, len(M)
    else:
        b0 = int((start_body_s if start_body_s is not None else 0.15 * note_off_s) * SR)
        b1 = int(note_off_s * SR)
    seg = M[b0:b1]
    frames = [seg[i:i + 4096] for i in range(0, len(seg) - 4096, hop)]
    win_h = np.hanning(4096)
    cents, specs, rms = [], [], []
    fr = np.fft.rfftfreq(4096, 1 / SR)
    for fr_x in frames:
        X = np.abs(np.fft.rfft(fr_x * win_h))
        specs.append(X)
        e = np.sum(X ** 2) + 1e-20
        cents.append(np.sum(fr * X ** 2) / e)
        rms.append(np.sqrt(np.mean(fr_x ** 2)))
    cents = np.array(cents); rms = np.array(rms)
    loud = rms > (np.max(rms) * 10 ** (-40 / 20))
    v["M10"] = float(np.std(np.log2(cents[loud] + 1))) if np.sum(loud) > 3 else 0.0
    specs = np.array(specs)
    if len(specs) > 2:
        nz = specs / (np.sum(specs, 1, keepdims=True) + 1e-20)
        v["M11"] = float(np.mean(np.sum(np.abs(np.diff(nz, axis=0)), 1)) / 2)
    else:
        v["M11"] = 0.0
    if category == "gated":
        v["M13"] = 0.0
    else:
        v["M13"] = float(np.mean(20 * np.log10(rms + 1e-12) < -60)) if len(rms) else 1.0
    v["M14"] = info.get("limiter_gr_db", 0.0)
    if is_loop:
        a = np.sqrt(np.mean(M[-int(0.05 * SR):] ** 2)); b_ = np.sqrt(np.mean(M[:int(0.05 * SR)] ** 2))
        v["M15"] = abs(20 * np.log10((a + 1e-12) / (b_ + 1e-12)))
    grp = group_of(category)
    bands = dict(BANDS[grp])
    if category == "gated":
        bands["M10"] = (0.10, 1.2)
    subs = {}
    for key, val in v.items():
        subs[key] = sub_score(val, bands[key], TOL[key])
    keys = list(subs)
    comp = 100 * sum(WEIGHT[k] * subs[k] for k in keys) / sum(WEIGHT[k] for k in keys)
    passed = all(gates.values()) and comp >= PASS_SCORE and min(subs.values()) >= 0.5
    return {"values": {k: round(float(x), 4) for k, x in v.items()}, "subs": {k: round(s, 3) for k, s in subs.items()},
            "gates": gates, "extra": {k: (round(float(x), 4) if isinstance(x, float) else x) for k, x in m.items()},
            "score": round(comp, 2), "pass": bool(passed)}
