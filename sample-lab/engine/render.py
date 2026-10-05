"""Patch -> stereo audio renderer.

A *patch* is a plain dict built step-by-step by skill appliers (engine/skills.py). Schema:
  category: pad|swell|drone|gated|pluck|bass
  layers: [ {osc: saw|pulse|triangle|sine|wt|fm|noise, oct, semi, fine_c, level, unison, detune (0..1, 1=±50c),
             width (0..1), blend (0..1 outer-voice weight), pan, pw, wt_table, wt_pos, wt_smooth, noise_color,
             fm_ratio, fm_index, am:{shape,ratio,depth,depth_src}, level_env:{a,d,s,r,curve}|None,
             keytrack_low:None|{full_below, zero_above}, group: 'A'|'B'|..., fixed_midi:None} ]
  filters: [ {type: ladder|diode|svf_lp|svf_hp|svf_bp|comb|formant, mode, cutoff, res, drive, keytrack (0..1),
              env:'env2'|None, env_amt_oct, stereo_off_oct, groups:[...]} ]   (serial, per group)
  amp_env: {a,d,s,r,curve};  envs: {name: {a,d,s,r,curve}}
  lfos: {name: {shape: sine|tri|random|square, rate_hz|sync, stereo_phase (rad), oneshot:bool}}
  ctracks: {name: {steps:[..], sync, direction}}
  mods: [ {src, dst, amt} ]   dst: cutoff:i | pitch | wt_pos | pan:k | level:k | am_depth | fm_index | detune
  drift_c: cents of slow random master-tune drift
  velocity: {to_amp, to_cutoff_oct}
  chord_split: bool ; lf_width_hz: None|Hz
  fx: [ {type: ..., ...} ]  ordered rack ;  master: {target_lufs}
"""
import zlib
import numpy as np
import pyloudnorm as pyln
from scipy import signal
import dsp
from dsp import SR

BPM = 90.0
SYNC_BEATS = {"4bar": 16, "2bar": 8, "1bar": 4, "1/2": 2, "1/4": 1, "1/4d": 1.5, "1/8": 0.5, "1/8d": 0.75,
              "1/16": 0.25, "1/8t": 1 / 3}

def sync_hz(s):
    return 1.0 / (SYNC_BEATS[s] * 60.0 / BPM)

def sync_s(s):
    return SYNC_BEATS[s] * 60.0 / BPM

# ------------------------------------------------------------------ test grid
TOTAL = {"pad": 12.0, "swell": 12.0, "drone": 16.0, "gated": 16.0, "pluck": 10.0, "bass": 9.0}
LOOP_LEN = 4 * sync_s("1bar")  # 10.667 s loop exports for drone/gated
NOTESETS = {
    "pad":   [[50, 53, 57, 64], [53, 57, 60, 64], [45, 52, 57, 60]],
    "swell": [[50, 57, 62, 65], [48, 55, 60, 64], [45, 52, 57, 64]],
    "gated": [[50, 53, 57, 62], [48, 52, 55, 62], [45, 52, 57, 60]],
    "drone": [[38, 45], [43, 50], [36, 43]],
    "pluck": [[62, 65, 69, 72], [60, 64, 67, 71], [57, 60, 64, 69]],
    "bass":  [[28], [33], [38]],
}

def schedule(category, notes):
    """-> list of (midi, start_s, dur_s, velocity)."""
    if category in ("pad", "swell"):
        return [(m, 0.0, 6.0, 0.85) for m in notes]
    if category in ("drone", "gated"):
        return [(m, 0.0, 14.5, 0.85) for m in notes]
    if category == "bass":
        return [(notes[0], 0.0, 5.0, 0.9)]
    if category == "pluck":
        pat = [0, 1, 2, 3, 2, 1, 0, 2]
        vels = [0.95, 0.6, 0.8, 0.55, 0.9, 0.5, 0.75, 0.65]
        step = sync_s("1/4") * 1.0
        return [(notes[p], i * step, 0.28, v) for i, (p, v) in enumerate(zip(pat, vels))]
    raise ValueError(category)

# ------------------------------------------------------------------ control signals
def adsr(n, off_i, a, d, s, r, curve=1.0):
    """Curved ADSR; curve>1 = convex/slow start, <1 = fast start. Times in seconds."""
    t = np.arange(n) / SR
    off_t = off_i / SR
    a = max(a, 0.001); d = max(d, 0.001); r = max(r, 0.002)
    e = np.empty(n)
    att = t < a
    e[att] = (t[att] / a) ** curve
    dec = (~att) & (t < a + d)
    e[dec] = 1.0 - (1.0 - s) * ((t[dec] - a) / d) ** (1.0 / curve if curve != 0 else 1)
    sus = (t >= a + d)
    e[sus] = s
    # level at note off
    if off_i < n:
        lvl = e[min(off_i, n - 1)]
        rel = t >= off_t
        tr = (t[rel] - off_t) / r
        e[rel] = lvl * np.exp(-6.9 * tr)   # -60 dB at r
    return e

def lfo_signal(n, spec, rng, t0=0.0):
    rate = spec.get("rate_hz") or sync_hz(spec["sync"])
    shape = spec.get("shape", "sine")
    sph = spec.get("stereo_phase", 0.0)
    t = np.arange(n) / SR + t0
    def one(phase_off):
        ph = 2 * np.pi * rate * t + phase_off
        if shape == "sine":
            return np.sin(ph)
        if shape == "tri":
            return signal.sawtooth(ph, 0.5)
        if shape == "square":
            return np.tanh(4 * np.sin(ph))
        if shape == "saw_down":
            return -signal.sawtooth(ph)
        if shape == "random":  # smooth random (cosine-interpolated S&H)
            nseg = int(np.ceil(t[-1] * rate)) + 3
            vals = rng.uniform(-1, 1, nseg)
            pos = t * rate + (phase_off / (2 * np.pi))
            i0 = np.floor(pos).astype(int) % nseg
            fr = pos - np.floor(pos)
            w = 0.5 - 0.5 * np.cos(np.pi * fr)
            return vals[i0] * (1 - w) + vals[(i0 + 1) % nseg] * w
        raise ValueError(shape)
    base_phase = rng.uniform(0, 2 * np.pi) if spec.get("free", True) and shape != "random" else 0.0
    L = one(base_phase)
    R = one(base_phase + sph) if sph else L
    if spec.get("unipolar"):
        L = 0.5 + 0.5 * L; R = 0.5 + 0.5 * R
    return L, R

def ctrack_signal(n, spec):
    steps = np.array(spec["steps"], float)
    if spec.get("direction") == "pingpong" and len(steps) > 2:
        steps = np.concatenate([steps, steps[-2:0:-1]])
    step_n = int(sync_s(spec["sync"]) * SR)
    idx = (np.arange(n) // step_n) % len(steps)
    v = steps[idx]
    # 5 ms slew to avoid zipper clicks
    a = np.exp(-1.0 / (0.005 * SR))
    v = signal.lfilter([1 - a], [1, -a], v, zi=[v[0] * a])[0]
    return v

def note_to_hz(m):
    return 440.0 * 2 ** ((m - 69) / 12.0)

def pan_gains(p):
    p = np.clip(p, -1, 1)
    ang = (p + 1) * np.pi / 4
    return np.cos(ang) * np.sqrt(2) * 0.5 ** 0.5 * np.sqrt(2) / np.sqrt(2), np.sin(ang) * 1.0

# ------------------------------------------------------------------ voice rendering
def render_note(patch, midi, start_s, dur_s, vel, n_total, rng, globals_):
    n = n_total - int(start_s * SR)
    off_i = int(dur_s * SR)
    f0 = note_to_hz(midi)
    t_start = int(start_s * SR)
    ctl = {}
    ctl["amp_env"] = adsr(n, off_i, **patch["amp_env"])
    for name, e in patch.get("envs", {}).items():
        ctl[name] = adsr(n, off_i, **e)
    for name, lf in globals_["lfo"].items():
        ctl[name] = (lf[0][t_start:], lf[1][t_start:])
    for name, ct in globals_["ctrack"].items():
        ctl[name] = ct[t_start:]
    ctl["velocity"] = np.full(n, vel)
    ctl["key"] = np.full(n, (midi - 60) / 12.0)

    def src(name):
        v = ctl[name]
        return v if isinstance(v, tuple) else (v, v)

    def mod_sum(dst, default=0.0):
        L = np.full(n, default); R = np.full(n, default)
        for m in patch.get("mods", []):
            if m["dst"] == dst:
                a, b = src(m["src"])
                L = L + m["amt"] * a; R = R + m["amt"] * b
        return L, R

    pitch_c = mod_sum("pitch")[0] + globals_["drift"][t_start:]
    detune_mod = mod_sum("detune")[0]
    groups = {}
    for li, ly in enumerate(patch["layers"]):
        if ly.get("level", 0) <= 0:
            continue
        lvl = ly["level"]
        if ly.get("keytrack_low"):
            kt = ly["keytrack_low"]
            lvl *= float(np.clip((kt["zero_above"] - midi) / (kt["zero_above"] - kt["full_below"]), 0, 1))
            if lvl <= 0:
                continue
        lvl *= 1.0 - patch.get("velocity", {}).get("to_layer_level", 0.0) * (1 - vel)
        m_midi = ly.get("fixed_midi") or midi
        base_semi = ly.get("oct", 0) * 12 + ly.get("semi", 0) + ly.get("fine_c", 0) / 100.0
        nv = max(1, int(ly.get("unison", 1)))
        det = ly.get("detune", 0.0) * 50.0
        width = ly.get("width", 0.0)
        blend = ly.get("blend", 0.5)
        if nv == 1:
            spread = np.array([0.0])
        else:
            spread = np.linspace(-1, 1, nv)
        vgain = np.where(np.abs(spread) < 1e-9, 1.0, 2 * blend) if nv > 1 else np.array([1.0])
        vgain = vgain / np.sqrt(np.sum(vgain ** 2))
        panmL, _ = mod_sum(f"pan:{li}")
        lpitch = mod_sum(f"pitch:{li}")[0]
        levm = mod_sum(f"level:{li}")[0]
        wtpos = None
        if ly["osc"] == "wt":
            tables = globals_["wt_cache"].setdefault((ly["wt_table"], m_midi + base_semi),
                                                      dsp.wavetable_frames(ly["wt_table"], note_to_hz(m_midi + base_semi)))
            wtpos = np.clip(ly.get("wt_pos", 0.0) + mod_sum("wt_pos")[0] + mod_sum(f"wt_pos:{li}")[0], 0, 1)
        outL = np.zeros(n); outR = np.zeros(n)
        if ly["osc"] == "noise":
            nz = dsp.noise(n, ly.get("noise_color", "pink"), rng)
            nz2 = dsp.noise(n, ly.get("noise_color", "pink"), rng)
            wdt = ly.get("width", 0.5)
            outL = (nz * (1 + wdt) + nz2 * (1 - wdt)) * 0.5
            outR = (nz * (1 - wdt) + nz2 * (1 + wdt)) * 0.5
            outL *= lvl; outR *= lvl
        else:
            for v in range(nv):
                cents = base_semi * 100 + spread[v] * det + pitch_c + lpitch + detune_mod * spread[v]
                freq = note_to_hz(m_midi) * 2 ** (cents / 1200.0)
                ph0 = rng.uniform(0, 1)
                o = ly["osc"]
                if o in ("saw", "pulse", "triangle", "sine"):
                    sh = {"saw": 0, "pulse": 1, "triangle": 2, "sine": 3}[o]
                    x = dsp.osc_va(freq, sh, ly.get("pw", 0.5), ph0, SR)
                elif o == "wt":
                    x = dsp.osc_wt(freq, wtpos, tables, ph0, SR, int(ly.get("wt_smooth", 1)))
                elif o == "fm":
                    idx = np.full(n, ly.get("fm_index", 1.0)) * (1 + mod_sum("fm_index")[0])
                    x = dsp.osc_fm(freq, ly.get("fm_ratio", 1.0), idx, ph0, SR)
                if ly.get("am"):
                    am = ly["am"]
                    msh = {"saw": 0, "pulse": 1, "triangle": 2, "sine": 3}[am.get("shape", "pulse")]
                    mod = dsp.osc_va(freq * am.get("ratio", 1.0), msh, 0.5, ph0, SR)
                    dsrc = ctl[am["depth_src"]] if am.get("depth_src") else 1.0
                    dsrc = dsrc[0] if isinstance(dsrc, tuple) else dsrc
                    d = am.get("depth", 0.5) * dsrc
                    d = np.clip(d + mod_sum("am_depth")[0], 0, 1)
                    x = x * ((1 - d) + d * mod)
                if o == "triangle":
                    x = x - np.mean(x)
                p = np.clip(ly.get("pan", 0.0) + spread[v] * width + panmL, -1, 1)
                ang = (p + 1) * np.pi / 4
                outL += x * np.cos(ang) * np.sqrt(2) * vgain[v]
                outR += x * np.sin(ang) * np.sqrt(2) * vgain[v]
            outL *= lvl; outR *= lvl
        lev = np.clip(1.0 + levm, 0, 2)
        if ly.get("level_env"):
            lev = lev * adsr(n, off_i, **ly["level_env"])
        outL *= lev; outR *= lev
        g = ly.get("group", "A")
        if g not in groups:
            groups[g] = [np.zeros(n), np.zeros(n)]
        groups[g][0] += outL; groups[g][1] += outR

    # filters per group (serial)
    vel_cut = patch.get("velocity", {}).get("to_cutoff_oct", 0.0) * (vel - 1.0)
    mixL = np.zeros(n); mixR = np.zeros(n)
    for g, (gl, gr) in groups.items():
        for fi, fl in enumerate(patch.get("filters", [])):
            if g not in fl.get("groups", ["A"]):
                continue
            oct_ = fl.get("keytrack", 0.0) * (midi - 60) / 12.0 + vel_cut * fl.get("vel_scale", 1.0)
            if fl.get("env"):
                oct_ = oct_ + fl.get("env_amt_oct", 0.0) * ctl[fl["env"]]
            mL, mR = mod_sum(f"cutoff:{fi}")
            so = fl.get("stereo_off_oct", 0.0) / 2.0
            base_c = fl.get("cutoff", 1000.0)
            cL = base_c * 2 ** np.clip(oct_ + mL - so, -8, 8)
            cR = base_c * 2 ** np.clip(oct_ + mR + so, -8, 8)
            ty = fl["type"]
            if ty in ("ladder", "diode"):
                mode = {"lp24": 0, "lp12": 1, "lp6": 2}[fl.get("mode", "lp24")]
                dio = 1 if ty == "diode" else 0
                gl = dsp.ladder(gl, cL, fl.get("res", 0.0), fl.get("drive", 0.0), mode, dio, SR)
                gr = dsp.ladder(gr, cR, fl.get("res", 0.0), fl.get("drive", 0.0), mode, dio, SR)
            elif ty.startswith("svf_"):
                mode = {"svf_lp": 0, "svf_bp": 1, "svf_hp": 2, "svf_notch": 3}[ty]
                q = 0.5 + fl.get("res", 0.0) * 4.0
                gl = dsp.svf(gl, cL, q, mode, SR); gr = dsp.svf(gr, cR, q, mode, SR)
            elif ty == "comb":
                fk = f0 * 2 ** (fl.get("semi", 0) / 12.0) if fl.get("keytrack", 1.0) > 0 else fl["cutoff"]
                d = np.full(n, SR / fk)
                gl = dsp.comb_ff_fb(gl, d, fl.get("res", 0.5) * (-1 if fl.get("minus") else 1), fl.get("mix", 0.5))
                gr = dsp.comb_ff_fb(gr, d * 1.0005, fl.get("res", 0.5) * (-1 if fl.get("minus") else 1), fl.get("mix", 0.5))
            elif ty == "formant":
                vowels = {"A": (800, 1150, 2900), "O": (450, 800, 2830), "I": (270, 2140, 2950),
                          "E": (400, 1600, 2700), "U": (325, 700, 2530)}
                va, vb = vowels[fl.get("vowel_a", "A")], vowels[fl.get("vowel_b", "O")]
                mL, mR = mod_sum(f"vowel:{fi}")
                mor = np.clip(0.5 + 0.5 * mL, 0, 1)
                outs = []
                for ch, mm in ((gl, mor), (gr, np.clip(0.5 + 0.5 * mR, 0, 1))):
                    acc = np.zeros(n)
                    for k, gk in enumerate((1.0, 0.6, 0.35)):
                        fc = va[k] * (1 - mm) + vb[k] * mm
                        acc += gk * dsp.svf(ch, fc, 4.0 + fl.get("res", 0.3) * 8, 1, SR)
                    outs.append(fl.get("mix", 0.7) * acc * 1.6 + (1 - fl.get("mix", 0.7)) * ch)
                gl, gr = outs
        mixL += gl; mixR += gr
    amp = ctl["amp_env"] * (1.0 - patch.get("velocity", {}).get("to_amp", 0.0) * (1.0 - vel))
    return t_start, mixL * amp, mixR * amp

# ------------------------------------------------------------------ FX rack
def fx_process(L, R, fx, patch, rng, globals_):
    ty = fx["type"]
    n = len(L)
    if ty == "eq":
        for b in fx["bands"]:
            L = dsp.eq(L, b["kind"], b["f"], b.get("q", 0.707), b.get("gain", 0.0))
            R = dsp.eq(R, b["kind"], b["f"], b.get("q", 0.707), b.get("gain", 0.0))
        return L, R
    if ty == "tape":
        # calibrate so RMS sits at 0 VU (= -18 dBFS), saturate, restore level
        rms = np.sqrt(np.mean(np.concatenate([L, R]) ** 2)) + 1e-12
        cal = 10 ** (-18 / 20) / rms
        k = 1.0 + fx.get("drive", 0.3) * 3.0
        def sat(x):
            y = np.tanh(k * x * cal * 2.0) / (k * 2.0) / cal
            return dsp.eq(y, "lp", fx.get("hf_roll", 16000))
        return sat(L), sat(R)
    if ty == "dist":
        dr = 1.0 + fx.get("drive", 0.4) * 6
        pk = np.max(np.abs(np.concatenate([L, R]))) + 1e-12
        def fold(x):
            y = np.sin(np.clip(x / pk * dr, -np.pi, np.pi) * 0.5 * np.pi / max(1, dr / 2)) * pk
            y = dsp.eq(y, "lp", fx.get("post_lp", 9000))
            return (1 - fx.get("mix", 0.25)) * x + fx.get("mix", 0.25) * y
        return fold(L), fold(R)
    if ty == "chorus":
        mode = {"classic": 0, "ensemble": 1, "vibrato": 2}[fx.get("mode", "classic")]
        hp = fx.get("wet_hp_hz", 0)
        a = np.exp(-2 * np.pi * hp / SR) if hp else 0.0
        yl, yr = dsp.chorus(L, R, SR, mode, fx.get("rate", 0.4), fx.get("depth_ms", 3.0), fx.get("base_ms", 9.0),
                            fx.get("feedback", 0.0), fx.get("width", 1.0), fx.get("mix", 0.35),
                            fx.get("offset", np.pi / 2), a)
        if mode == 2:
            return yl * 2, yr * 2
        return yl, yr
    if ty == "phaser":
        return (dsp.phaser(L, fx.get("rate", 0.15), fx.get("depth", 0.6), fx.get("fb", 0.3), 6, fx.get("mix", 0.25), 0.0, SR),
                dsp.phaser(R, fx.get("rate", 0.15), fx.get("depth", 0.6), fx.get("fb", 0.3), 6, fx.get("mix", 0.25), 1.2, SR))
    if ty == "delay":
        tl = fx.get("tl_s") or sync_s(fx["sync_l"]); tr = fx.get("tr_s") or sync_s(fx.get("sync_r", fx.get("sync_l")))
        if fx.get("mode") == "pingpong":
            wl, wr = dsp.stereo_delay(L, R, SR, tl, tl, 0.0, 0.0, 1.0, fx["feedback"], 1, fx.get("hp_hz", 100),
                                      fx.get("lp_hz", 3000), fx.get("sat", 0.0), 0.0, 0.0)
        else:
            wl, wr = dsp.stereo_delay(L, R, SR, tl, tr, fx.get("fb_l", 0.45), fx.get("fb_r", 0.3), fx.get("x_lr", 0.0),
                                      fx.get("x_rl", 0.0), 0, fx.get("hp_hz", 100), fx.get("lp_hz", 3000),
                                      fx.get("sat", 0.0), fx.get("mod_depth", 0.0), fx.get("mod_rate", 0.3))
        m = fx.get("mix", 0.2)
        return L + m * wl, R + m * wr
    if ty == "reverb":
        wl, wr = dsp.fdn_reverb(L, R, SR, fx["rt60"], fx.get("size", 1.0), fx.get("damp_hz", 7000),
                                fx.get("predelay_s", 0.02), fx.get("mod_ms", 0.3), fx.get("diffusion", 0.6),
                                fx.get("er", 0.5), 0)
        if fx.get("return_hp", 0):
            wl = dsp.eq(dsp.eq(wl, "hp", fx["return_hp"]), "hp", fx["return_hp"])
            wr = dsp.eq(dsp.eq(wr, "hp", fx["return_hp"]), "hp", fx["return_hp"])
        if fx.get("return_lp", 0):
            wl = dsp.eq(wl, "lp", fx["return_lp"]); wr = dsp.eq(wr, "lp", fx["return_lp"])
        if fx.get("post_filter_open"):  # filter after reverb slowly opening (bloom)
            pf = fx["post_filter_open"]
            cut = pf["from_hz"] * (pf["to_hz"] / pf["from_hz"]) ** np.clip(np.arange(n) / (pf["time_s"] * SR), 0, 1)
            wl = dsp.svf(wl, cut, 0.707, 0, SR); wr = dsp.svf(wr, cut, 0.707, 0, SR)
        s = fx.get("send", 0.3)
        return L * fx.get("dry", 1.0) + s * wl, R * fx.get("dry", 1.0) + s * wr
    if ty == "shimmer":
        mono = 0.5 * (L + R)
        sh = dsp.pitch_shift_delay(mono, SR, fx.get("semis", 12), fx.get("delay_s", 0.25), fx.get("feedback", 0.4),
                                   fx.get("echo_hp", 300), fx.get("echo_lp", 6000), 0.06)
        wl, wr = dsp.fdn_reverb(sh, sh, SR, fx["rt60"], fx.get("size", 1.4), fx.get("damp_hz", 6000), 0.03, 0.6,
                                0.7, 0.2, 1)
        for b in fx.get("wet_eq", [{"kind": "hp", "f": 250}]):
            wl = dsp.eq(wl, b["kind"], b["f"], b.get("q", 0.707), b.get("gain", 0.0))
            wr = dsp.eq(wr, b["kind"], b["f"], b.get("q", 0.707), b.get("gain", 0.0))
        s = fx.get("send", 0.25)
        return L + s * wl, R + s * wr
    if ty == "ms_eq":
        M = 0.5 * (L + R); S = 0.5 * (L - R)
        if fx.get("side_hp"):
            S = dsp.eq(dsp.eq(S, "hp", fx["side_hp"]), "hp", fx["side_hp"])
        if fx.get("mid_cut_db"):
            # locate the most prominent mid resonance 1-6 kHz (skill step 3: solo mid, find problem band)
            f, P = signal.welch(M, SR, nperseg=8192)
            Pd = 10 * np.log10(P + 1e-20)
            sm = np.convolve(Pd, np.ones(61) / 61, mode="same")
            band = (f > 1000) & (f < 6000)
            fk = f[band][np.argmax((Pd - sm)[band])]
            M = dsp.eq(M, "peak", fk, 2.0, -abs(fx["mid_cut_db"]))
            if fx.get("side_restore_same_band"):
                S = dsp.eq(S, "peak", fk, 2.0, abs(fx["mid_cut_db"]) * 0.5)
        if fx.get("side_uppermid_db"):
            S = dsp.eq(S, "peak", fx.get("side_uppermid_hz", 3000), 0.8, fx["side_uppermid_db"])
        return M + S, M - S
    if ty == "hb_pan":
        loL, hiL = dsp.lr4_split(L, fx.get("xover_hz", 2500)); loR, hiR = dsp.lr4_split(R, fx.get("xover_hz", 2500))
        rate = sync_hz(fx.get("sync", "1bar"))
        t = np.arange(n) / SR
        p = fx.get("amount", 0.6) * np.sin(2 * np.pi * rate * t)
        ang = (p + 1) * np.pi / 4
        hM = 0.5 * (hiL + hiR); hS = 0.5 * (hiL - hiR)
        return loL + hM * np.cos(ang) * np.sqrt(2) + hS, loR + hM * np.sin(ang) * np.sqrt(2) - hS
    if ty == "gate":
        step = int(sync_s("1/16") * SR)
        pat = fx.get("pattern", [1, 1, 1, 0])
        key = np.zeros(n)
        for i, s0 in enumerate(range(0, n, step)):
            if pat[i % len(pat)]:
                key[s0:s0 + int(0.006 * SR)] = 1.0   # silent trigger clicks (never mixed in)
        # gate: opens on trigger, holds ~ one 16th minus release, release sets snap
        hold = int(fx.get("hold_frac", 0.55) * step)
        g = np.zeros(n)
        for s0 in np.nonzero(np.diff(np.concatenate([[0], key])) > 0)[0]:
            g[s0:s0 + hold] = 1.0
        a = np.exp(-1.0 / (0.002 * SR)); r = np.exp(-1.0 / (fx.get("release_s", 0.05) * SR))
        env = dsp._release(1.0 - g, r)  # inverted trick: fast close smoothing
        g2 = 1.0 - env
        g2 = signal.lfilter([1 - a], [1, -a], g2)
        floor = 10 ** (fx.get("floor_db", -60) / 20)
        g2 = floor + (1 - floor) * g2
        return L * g2, R * g2
    if ty == "duck":
        beat = int(sync_s("1/4") * SR)
        key = np.zeros(n)
        kt = np.arange(int(0.12 * SR)) / SR
        kick = np.sin(2 * np.pi * 55 * kt) * np.exp(-kt / 0.05)
        for s0 in range(0, n, beat):
            m = min(len(kick), n - s0)
            key[s0:s0 + m] += kick[:m]
        g = dsp.env_follow_gain(key, SR, fx.get("thresh_db", -30.0), fx.get("ratio", 6.0),
                                fx.get("attack_s", 0.001), fx.get("release_s", 0.25))
        return L * g, R * g
    if ty == "comp":
        key = np.sqrt(0.5 * (L ** 2 + R ** 2))
        rms = 20 * np.log10(np.sqrt(np.mean(key ** 2)) + 1e-12)
        g = dsp.env_follow_gain(key, SR, rms + fx.get("thresh_rel_db", 3.0), fx.get("ratio", 2.0),
                                fx.get("attack_s", 0.02), fx.get("release_s", 0.2))
        return L * g, R * g
    if ty == "parallel_filter":
        t = np.arange(n) / SR
        rate = sync_hz(fx.get("sync", "1bar"))
        out = []
        for ch, off in ((L, 0.0), (R, fx.get("lr_offset", np.pi / 2))):
            l1 = 0.5 + 0.5 * signal.sawtooth(2 * np.pi * rate * t + off, 0.8)
            l2 = 0.5 + 0.5 * signal.sawtooth(2 * np.pi * rate * t + off + np.pi, 0.8)
            c1 = fx.get("lp_hz", 1200) * 2 ** (fx.get("depth_oct", 2.0) * l1)
            c2 = fx.get("bp_hz", 800) * 2 ** (fx.get("depth_oct", 2.0) * l2)
            a = dsp.svf(ch, c1, 0.9, 0, SR); b = dsp.svf(ch, c2, 1.5, 1, SR)
            out.append(fx.get("mix", 0.6) * (a + b) * 0.7 + (1 - fx.get("mix", 0.6)) * ch)
        L, R = out
        L, R = fx_process(L, R, {"type": "comp", "ratio": 3.0, "thresh_rel_db": 2.0}, patch, rng, globals_)
        hp = fx.get("post_hp", 90)
        return dsp.eq(L, "hp", hp), dsp.eq(R, "hp", hp)
    if ty == "lf_width":
        M = 0.5 * (L + R); S = 0.5 * (L - R)
        S = dsp.eq(dsp.eq(S, "hp", fx["hz"]), "hp", fx["hz"])
        return M + S, M - S
    if ty == "chord_split":
        return L, R  # handled at voice level
    raise ValueError(ty)

# ------------------------------------------------------------------ top level
def render(patch, notes, seed, loop=None):
    cat = patch["category"]
    total = TOTAL[cat]
    n = int(total * SR)
    rng = np.random.default_rng(seed)
    globals_ = {"lfo": {}, "ctrack": {}, "wt_cache": {}}
    for name, spec in patch.get("lfos", {}).items():
        globals_["lfo"][name] = lfo_signal(n, spec, np.random.default_rng(seed * 7919 + zlib.crc32(name.encode()) % 1000))
    for name, spec in patch.get("ctracks", {}).items():
        globals_["ctrack"][name] = ctrack_signal(n, spec)
    dr = patch.get("drift_c", 0.0)
    if dr:
        d, _ = lfo_signal(n, {"shape": "random", "rate_hz": 0.35}, np.random.default_rng(seed * 31 + 5))
        globals_["drift"] = d * dr
    else:
        globals_["drift"] = np.zeros(n)
    L = np.zeros(n); R = np.zeros(n)
    sched = schedule(cat, notes)
    order = sorted(range(len(sched)), key=lambda i: sched[i][0])
    for k, i in enumerate(order):
        midi, st, du, vel = sched[i]
        nrng = np.random.default_rng(seed * 1000 + k * 17 + midi)
        t0, nl, nr = render_note(patch, midi, st, du, vel, n, nrng, globals_)
        if patch.get("chord_split") and len(set(m for m, *_ in sched)) > 1:
            p = -1.0 if k % 2 == 0 else 1.0
            ang = (p * patch.get("chord_split_amt", 1.0) + 1) * np.pi / 4
            mono = 0.5 * (nl + nr)
            nl, nr = mono * np.cos(ang) * np.sqrt(2), mono * np.sin(ang) * np.sqrt(2)
        ns = patch.get("note_spread", 0.0)
        if ns and len(sched) > 1 and not patch.get("chord_split"):
            p = ns * (2 * k / (len(order) - 1) - 1)
            ang = (p + 1) * np.pi / 4
            nl, nr = nl * np.cos(ang) * np.sqrt(2), nr * np.sin(ang) * np.sqrt(2)
        L[t0:] += nl; R[t0:] += nr
    pk = np.max(np.abs(np.concatenate([L, R]))) + 1e-12
    L /= pk * 2; R /= pk * 2   # pre-FX headroom (-6 dBFS peak)
    for fx in patch.get("fx", []):
        L, R = fx_process(L, R, fx, patch, rng, globals_)
    if patch.get("lf_width_hz"):
        L, R = fx_process(L, R, {"type": "lf_width", "hz": patch["lf_width_hz"]}, patch, rng, globals_)
    return master(L, R, patch, loop)

def master(L, R, patch, loop):
    cat = patch["category"]
    # DC blocker (standard export hygiene)
    b, a = signal.butter(1, 8, "highpass", fs=SR)
    L = signal.lfilter(b, a, L); R = signal.lfilter(b, a, R)
    if cat in ("drone", "gated") and loop is not False:
        L, R = make_loop(L, R)
    tgt = patch.get("master", {}).get("target_lufs", -15.0)
    meter = pyln.Meter(SR)
    lufs = meter.integrated_loudness(np.stack([L, R], 1))
    if np.isfinite(lufs):
        g = 10 ** ((tgt - lufs) / 20)
        L *= g; R *= g
    L, R, gr = limiter(L, R)
    if cat not in ("drone", "gated"):
        fo = int(0.05 * SR)
        w = np.cos(np.linspace(0, np.pi / 2, fo)) ** 2
        L[-fo:] *= w; R[-fo:] *= w
    return np.stack([L, R], 1), {"limiter_gr_db": gr}

def limiter(L, R):
    return dsp.limiter(L, R, ceiling_db=-1.3)

def make_loop(L, R):
    """Seamless bar-aligned loop from the sustained region: equal-power crossfade of the region's
    continuation into its head (tail-wrap)."""
    S = int(sync_s("1bar") * SR)   # loop starts on a downbeat
    Ln = int(LOOP_LEN * SR)
    X = int(0.5 * SR)
    segL = L[S:S + Ln].copy(); segR = R[S:S + Ln].copy()
    cl = L[S + Ln:S + Ln + X]; cr = R[S + Ln:S + Ln + X]
    t = np.linspace(0, np.pi / 2, X)
    segL[:X] = segL[:X] * np.sin(t) + cl * np.cos(t)
    segR[:X] = segR[:X] * np.sin(t) + cr * np.cos(t)
    return segL, segR
