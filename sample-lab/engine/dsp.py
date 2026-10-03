"""Offline DSP modules for the Sample Lab renderer (numpy + numba).
All kernels are deterministic given inputs (RNG is always seeded by caller)."""
import numpy as np
from numba import njit
from scipy import signal

SR = 48000
TWO_PI = 2.0 * np.pi

# ---------------------------------------------------------------- oscillators
@njit(cache=True)
def _polyblep(t, dt):
    if t < dt:
        t = t / dt
        return t + t - t * t - 1.0
    elif t > 1.0 - dt:
        t = (t - 1.0) / dt
        return t * t + t + t + 1.0
    return 0.0

@njit(cache=True)
def osc_va(freq, shape, pw, phase0, sr):
    """freq: per-sample Hz. shape 0=saw 1=pulse 2=triangle 3=sine. Band-limited (polyBLEP)."""
    n = freq.shape[0]
    out = np.zeros(n)
    ph = phase0
    tri = 0.0
    for i in range(n):
        dt = freq[i] / sr
        if dt > 0.49:
            dt = 0.49
        if shape == 0:
            v = 2.0 * ph - 1.0
            v -= _polyblep(ph, dt)
        elif shape == 1 or shape == 2:
            v = 1.0 if ph < pw else -1.0
            v += _polyblep(ph, dt)
            p2 = ph - pw + 1.0
            if p2 >= 1.0:
                p2 -= 1.0
            v -= _polyblep(p2, dt)
            if shape == 2:  # leaky-integrated square -> triangle
                tri = dt * 4.0 * v + (1.0 - 0.0005) * tri
                v = tri
        else:
            v = np.sin(TWO_PI * ph)
        out[i] = v
        ph += dt
        if ph >= 1.0:
            ph -= 1.0
    return out

@njit(cache=True)
def osc_wt(freq, pos, tables, phase0, sr, smooth):
    """Wavetable osc. tables[F, N]; pos per-sample 0..1; smooth=1 crossfades frames, 0 = hard switch."""
    n = freq.shape[0]
    F = tables.shape[0]
    N = tables.shape[1]
    out = np.zeros(n)
    ph = phase0
    for i in range(n):
        p = pos[i]
        if p < 0.0:
            p = 0.0
        if p > 1.0:
            p = 1.0
        fp = p * (F - 1)
        f0 = int(fp)
        if f0 >= F - 1:
            f0 = F - 2
        fr = fp - f0
        if smooth == 0:
            fr = 1.0 if fr >= 0.5 else 0.0
        x = ph * N
        j = int(x)
        xf = x - j
        j1 = (j + 1) % N
        a = tables[f0, j] + xf * (tables[f0, j1] - tables[f0, j])
        b = tables[f0 + 1, j] + xf * (tables[f0 + 1, j1] - tables[f0 + 1, j])
        out[i] = a + fr * (b - a)
        ph += freq[i] / sr
        while ph >= 1.0:
            ph -= 1.0
    return out

@njit(cache=True)
def osc_fm(freq, ratio, index, phase0, sr):
    """2-op FM (phase modulation): sine carrier, sine modulator at ratio*freq, per-sample index."""
    n = freq.shape[0]
    out = np.zeros(n)
    pc = phase0
    pm = 0.0
    for i in range(n):
        m = np.sin(TWO_PI * pm)
        out[i] = np.sin(TWO_PI * pc + index[i] * m)
        pc += freq[i] / sr
        pm += freq[i] * ratio / sr
        if pc >= 1.0:
            pc -= 1.0
        if pm >= 1.0:
            pm -= 1.0
    return out

def wavetable_frames(kind, f0, sr=SR, N=2048):
    """Original additive wavetables, band-limited for fundamental f0 (Nyquist-safe for +1 oct pitch mod)."""
    H = max(1, min(256, int(0.45 * sr / (f0 * 2.0))))
    h = np.arange(1, H + 1)
    frames = []
    def make(amps, phases=None):
        ph = np.zeros_like(amps) if phases is None else phases
        t = np.arange(N) / N
        w = np.zeros(N)
        for k, (a, p) in enumerate(zip(amps, ph)):
            if a != 0:
                w += a * np.sin(2 * np.pi * (k + 1) * t + p)
        m = np.max(np.abs(w))
        return w / m if m > 0 else w
    if kind == "soft_to_complex":   # ambient-wavetable-scratch: sine -> harmonics added gradually -> phase-altered end frame
        for stage in range(5):
            nh = [1, 3, 6, 12, 24][stage]
            amps = np.where(h <= nh, 1.0 / h ** (1.6 - 0.15 * stage), 0.0)
            phases = (np.sin(h * 1.7) * 0.9 * stage / 4.0)
            frames.append(make(amps, phases))
    elif kind == "saw_tri_square_sine":  # wavetable-crossfade: saw -> triangle -> square -> sine family
        saw = 1.0 / h
        tri = np.where(h % 2 == 1, (1.0 / h ** 2) * np.where(((h - 1) // 2) % 2 == 0, 1, -1), 0)
        sq = np.where(h % 2 == 1, 1.0 / h, 0)
        sine = np.where(h == 1, 1.0, 0)
        for a in (saw, tri, sq, sine):
            frames.append(make(a))
    elif kind == "digital_additive":  # gentle digital: formant-ish bump that moves across frames
        for stage in range(6):
            centre = 3 + stage * 3
            amps = (1.0 / h) * (0.35 + np.exp(-0.5 * ((h - centre) / 2.5) ** 2))
            frames.append(make(amps))
    elif kind == "artifact_high":
        for stage in range(4):
            amps = np.where(h % (stage + 2) == 0, 1.0 / np.sqrt(h), 0.15 / h)
            frames.append(make(amps))
    else:
        raise ValueError(kind)
    return np.array(frames)

def noise(n, color, rng):
    w = rng.standard_normal(n)
    if color == "pink":
        # Paul Kellet economy pink filter (static IIR)
        b = [0.049922035, -0.095993537, 0.050612699, -0.004408786]
        a = [1, -2.494956002, 2.017265875, -0.522189400]
        w = signal.lfilter(b, a, w) * 3.0
    return w / (np.std(w) + 1e-12) * 0.3

# ---------------------------------------------------------------- filters
@njit(cache=True)
def ladder(x, fc, res, drive, mode, diode, sr):
    """ZDF 4-pole ladder (TPT one-poles, linear-solved feedback) with tanh input drive.
    mode 0 = LP24, 1 = LP12 (2-pole tap), 2 = LP6. diode=1 -> asymmetric saturation + res rescale."""
    n = x.shape[0]
    y = np.zeros(n)
    s1 = 0.0; s2 = 0.0; s3 = 0.0; s4 = 0.0
    k = res * (4.0 if diode == 0 else 3.2)
    dg = 1.0 + drive * 4.0
    for i in range(n):
        f = fc[i]
        if f < 20.0:
            f = 20.0
        if f > 0.45 * sr:
            f = 0.45 * sr
        g = np.tan(np.pi * f / sr)
        G = g / (1.0 + g)
        inp = x[i] * dg
        if diode == 1:
            inp = np.tanh(inp + 0.15 * inp * inp) - np.tanh(0.0)
        else:
            inp = np.tanh(inp)
        inp /= dg if drive < 1e-6 else (1.0 + drive * 1.5)
        b1 = s1 / (1.0 + g); b2 = s2 / (1.0 + g); b3 = s3 / (1.0 + g); b4 = s4 / (1.0 + g)
        if mode == 0:
            S = G * G * G * b1 + G * G * b2 + G * b3 + b4
            u = (inp - k * S) / (1.0 + k * G * G * G * G)
        else:
            S = G * b1 + b2
            u = (inp - 0.5 * k * S) / (1.0 + 0.5 * k * G * G)
        v = (u - s1) * G; y1 = v + s1; s1 = y1 + v
        v = (y1 - s2) * G; y2 = v + s2; s2 = y2 + v
        v = (y2 - s3) * G; y3 = v + s3; s3 = y3 + v
        v = (y3 - s4) * G; y4 = v + s4; s4 = y4 + v
        if mode == 0:
            y[i] = y4 * (1.0 + k * 0.5)
        elif mode == 1:
            y[i] = y2 * (1.0 + k * 0.25)
        else:
            y[i] = y1
    return y

@njit(cache=True)
def svf(x, fc, q, mode, sr):
    """TPT state-variable filter, 12 dB. mode 0 LP,1 BP,2 HP,3 notch. per-sample cutoff."""
    n = x.shape[0]
    y = np.zeros(n)
    ic1 = 0.0; ic2 = 0.0
    kq = 1.0 / q
    for i in range(n):
        f = fc[i]
        if f < 20.0:
            f = 20.0
        if f > 0.45 * sr:
            f = 0.45 * sr
        g = np.tan(np.pi * f / sr)
        a1 = 1.0 / (1.0 + g * (g + kq)); a2 = g * a1; a3 = g * a2
        v3 = x[i] - ic2
        v1 = a1 * ic1 + a2 * v3
        v2 = ic2 + a2 * ic1 + a3 * v3
        ic1 = 2.0 * v1 - ic1
        ic2 = 2.0 * v2 - ic2
        if mode == 0:
            y[i] = v2
        elif mode == 1:
            y[i] = v1 * kq
        elif mode == 2:
            y[i] = x[i] - kq * v1 - v2
        else:
            y[i] = x[i] - kq * v1
    return y

@njit(cache=True)
def comb_ff_fb(x, delay_samp, fb, mix):
    """Feedback comb with fractional (per-sample) delay; mix blends comb with dry."""
    n = x.shape[0]
    L = 8192
    buf = np.zeros(L)
    y = np.zeros(n)
    w = 0
    for i in range(n):
        d = delay_samp[i]
        if d < 2.0:
            d = 2.0
        if d > L - 2:
            d = L - 2.0
        rp = w - d
        while rp < 0:
            rp += L
        j = int(rp); fr = rp - j
        z = buf[j] + fr * (buf[(j + 1) % L] - buf[j])
        v = x[i] + fb * z
        buf[w] = v
        y[i] = (1.0 - mix) * x[i] + mix * v * (1.0 - abs(fb)) * 1.5
        w = (w + 1) % L
    return y

@njit(cache=True)
def phaser(x, rate, depth, fb, stages, mix, phase0, sr):
    n = x.shape[0]
    zs = np.zeros(12)
    y = np.zeros(n)
    last = 0.0
    for i in range(n):
        lfo = 0.5 + 0.5 * np.sin(TWO_PI * (rate * i / sr) + phase0)
        f = 200.0 * (2.0 ** (lfo * depth * 5.0))
        t = np.tan(np.pi * f / sr)
        a = (t - 1.0) / (t + 1.0)
        v = x[i] + fb * last
        for s in range(stages):
            o = a * v + zs[s]
            zs[s] = v - a * o
            v = o
        last = v
        y[i] = (1.0 - mix) * x[i] + mix * v
    return y

# ---------------------------------------------------------------- time FX
@njit(cache=True)
def _read(buf, w, d, L):
    rp = w - d
    while rp < 0:
        rp += L
    j = int(rp); fr = rp - j
    return buf[j] + fr * (buf[(j + 1) % L] - buf[j])

@njit(cache=True)
def chorus(xl, xr, sr, mode, rate, depth_ms, base_ms, feedback, width, mix, offset, wet_hp):
    """mode 0 classic (2 modulated copies), 1 ensemble (3 copies, 120deg), 2 vibrato (pitch only, no fb/mix).
    wet_hp: one-pole high-pass coefficient on processed path (0 = off)."""
    n = xl.shape[0]
    L = 8192
    bl = np.zeros(L); br = np.zeros(L)
    yl = np.zeros(n); yr = np.zeros(n)
    w = 0
    ncopy = 2 if mode == 0 else 3
    fbl = 0.0; fbr = 0.0
    hpl = 0.0; hpr = 0.0; pxl = 0.0; pxr = 0.0
    for i in range(n):
        bl[w] = xl[i] + (feedback * fbl if mode != 2 else 0.0)
        br[w] = xr[i] + (feedback * fbr if mode != 2 else 0.0)
        wl = 0.0; wr = 0.0
        for c in range(ncopy):
            ph = TWO_PI * rate * i / sr + c * TWO_PI / ncopy
            dl = (base_ms + depth_ms * (0.5 + 0.5 * np.sin(ph))) * sr / 1000.0
            dr = (base_ms + depth_ms * (0.5 + 0.5 * np.sin(ph + offset))) * sr / 1000.0
            a = _read(bl, w, dl, L); b = _read(br, w, dr, L)
            # copies alternate L/R emphasis by width
            pan = (1.0 if c % 2 == 0 else -1.0) * width * 0.5
            wl += a * (0.5 + 0.5 * -pan) + b * (0.5 * pan if pan > 0 else 0.0)
            wr += b * (0.5 + 0.5 * pan) + a * (-0.5 * pan if pan < 0 else 0.0)
        wl /= ncopy * 0.5; wr /= ncopy * 0.5
        fbl = wl; fbr = wr
        if wet_hp > 0.0:  # one-pole HP on wet
            hl = wet_hp * (hpl + wl - pxl); pxl = wl; hpl = hl; wl = hl
            hr = wet_hp * (hpr + wr - pxr); pxr = wr; hpr = hr; wr = hr
        if mode == 2:
            yl[i] = wl * 0.5 * ncopy / ncopy; yr[i] = wr * 0.5
        else:
            yl[i] = (1.0 - mix) * xl[i] + mix * wl * 0.7
            yr[i] = (1.0 - mix) * xr[i] + mix * wr * 0.7
        w = (w + 1) % L
    return yl, yr

@njit(cache=True)
def stereo_delay(xl, xr, sr, tl, tr, fb_ll, fb_rr, fb_lr, fb_rl, pingpong, hp_hz, lp_hz, sat, mod_depth, mod_rate):
    """Returns WET only. pingpong=1: mono sum enters L, L->R->L bounce (two-tap 2:1 style).
    Feedback path band-limited (one-pole HP/LP) with optional tanh saturation."""
    n = xl.shape[0]
    L = 1 << 18
    bl = np.zeros(L); br = np.zeros(L)
    yl = np.zeros(n); yr = np.zeros(n)
    ahp = np.exp(-TWO_PI * hp_hz / sr); alp = np.exp(-TWO_PI * lp_hz / sr)
    hpl = 0.0; hpr = 0.0; pl = 0.0; pr = 0.0; lpl = 0.0; lpr = 0.0
    w = 0
    for i in range(n):
        m = 1.0 + mod_depth * np.sin(TWO_PI * mod_rate * i / sr)
        dl = tl * sr * m; dr = tr * sr * (2.0 - m)
        ol = _read(bl, w, dl, L); orr = _read(br, w, dr, L)
        # filter repeats
        lpl = (1 - alp) * ol + alp * lpl; lpr = (1 - alp) * orr + alp * lpr
        h1 = ahp * (hpl + lpl - pl); pl = lpl; hpl = h1
        h2 = ahp * (hpr + lpr - pr); pr = lpr; hpr = h2
        ol = h1; orr = h2
        if sat > 0.0:
            ol = np.tanh(ol * (1.0 + sat * 3.0)) / (1.0 + sat * 3.0)
            orr = np.tanh(orr * (1.0 + sat * 3.0)) / (1.0 + sat * 3.0)
        if pingpong == 1:
            bl[w] = 0.5 * (xl[i] + xr[i]) + fb_rl * orr
            br[w] = fb_lr * ol
        else:
            bl[w] = xl[i] + fb_ll * ol + fb_rl * orr
            br[w] = xr[i] + fb_rr * orr + fb_lr * ol
        yl[i] = ol; yr[i] = orr
        w = (w + 1) & (L - 1)
    return yl, yr

@njit(cache=True)
def fdn_reverb(xl, xr, sr, rt60, size, damp_hz, predelay_s, mod_depth, diffusion, er_level, seed_off):
    """8-line FDN (Householder) with input allpass diffusion, per-line damping, light modulation.
    Returns WET stereo (100% wet, send-style)."""
    n = xl.shape[0]
    base = np.array([1031., 1327., 1523., 1789., 2053., 2311., 2579., 2851.])
    dls = base * size * (1.0 + 0.0007 * seed_off)
    L = 1 << 17
    bufs = np.zeros((8, L))
    gains = np.zeros(8)
    for k in range(8):
        gains[k] = 10.0 ** (-3.0 * (dls[k] / sr) / rt60)
    ad = np.exp(-TWO_PI * damp_hz / sr)
    lp = np.zeros(8)
    # allpass diffusers
    apd = np.array([142., 107., 379., 277.]) * (0.6 + 0.4 * size)
    apL = 4096
    apb = np.zeros((4, apL))
    pdL = 1 << 16
    pdb = np.zeros(pdL)
    pd = int(predelay_s * sr)
    if pd > pdL - 2:
        pd = pdL - 2
    erb_taps = np.array([0.0043, 0.0215, 0.0225, 0.0268, 0.0270, 0.0298, 0.0458, 0.0485])
    yl = np.zeros(n); yr = np.zeros(n)
    w = 0; wa = 0; wp = 0
    for i in range(n):
        x = 0.5 * (xl[i] + xr[i])
        pdb[wp] = x
        rp = wp - pd
        if rp < 0:
            rp += pdL
        v = pdb[rp]
        # early reflections from predelay buffer
        el = 0.0; er = 0.0
        for t in range(8):
            q = wp - pd - int(erb_taps[t] * sr * size)
            while q < 0:
                q += pdL
            if t % 2 == 0:
                el += pdb[q] * (0.8 - 0.07 * t)
            else:
                er += pdb[q] * (0.8 - 0.07 * t)
        for a in range(4):
            q = wa - int(apd[a])
            if q < 0:
                q += apL
            d = apb[a, q]
            g = diffusion
            o = -g * v + d
            apb[a, wa] = v + g * o
            v = o
        outs = np.zeros(8)
        for k in range(8):
            md = dls[k]
            if k < 2:
                md += mod_depth * sr * 0.001 * np.sin(TWO_PI * (0.31 + 0.17 * k) * i / sr)
            o = _read(bufs[k], w, md, L)
            lp[k] = (1 - ad) * o + ad * lp[k]
            outs[k] = lp[k] * gains[k]
        s = 0.0
        for k in range(8):
            s += outs[k]
        s *= 0.25  # Householder: x - 2/N * sum
        for k in range(8):
            bufs[k, w] = outs[k] - s + v * (0.5 if k % 2 == 0 else -0.5)
        yl[i] = (outs[0] + outs[2] + outs[4] + outs[6]) * 0.5 + er_level * el * 0.3
        yr[i] = (outs[1] + outs[3] + outs[5] + outs[7]) * 0.5 + er_level * er * 0.3
        w = (w + 1) & (L - 1)
        wa = (wa + 1) % apL
        wp = (wp + 1) & (pdL - 1)
    return yl, yr

@njit(cache=True)
def pitch_shift_delay(x, sr, semis, delay_s, fb, hp_hz, lp_hz, win_s):
    """Granular two-head pitch shifter inside a feedback delay loop (shimmer). Returns wet mono.
    Each pass through the loop is shifted again (endless bloom when fb>0)."""
    n = x.shape[0]
    L = 1 << 18
    buf = np.zeros(L)
    y = np.zeros(n)
    ratio = 2.0 ** (semis / 12.0)
    win = win_s * sr
    D = delay_s * sr
    ahp = np.exp(-TWO_PI * hp_hz / sr); alp = np.exp(-TWO_PI * lp_hz / sr)
    hp = 0.0; px = 0.0; lpv = 0.0
    ph = 0.0
    w = 0
    last = 0.0
    for i in range(n):
        ph += (1.0 - ratio) / win
        if ph < 0.0:
            ph += 1.0
        if ph >= 1.0:
            ph -= 1.0
        ph2 = ph + 0.5
        if ph2 >= 1.0:
            ph2 -= 1.0
        a = _read(buf, w, D + ph * win, L)
        b = _read(buf, w, D + ph2 * win, L)
        ga = np.sin(np.pi * ph); gb = np.sin(np.pi * ph2)
        o = a * ga * ga + b * gb * gb
        lpv = (1 - alp) * o + alp * lpv
        h = ahp * (hp + lpv - px); px = lpv; hp = h
        last = h
        buf[w] = x[i] + fb * last
        y[i] = last
        w = (w + 1) & (L - 1)
    return y

@njit(cache=True)
def env_follow_gain(key, sr, thresh_db, ratio, att_s, rel_s):
    """Feed-forward compressor gain (linear) from a key signal (abs-detected)."""
    n = key.shape[0]
    g = np.ones(n)
    aa = np.exp(-1.0 / (att_s * sr)); ar = np.exp(-1.0 / (rel_s * sr))
    env = 0.0
    for i in range(n):
        v = abs(key[i])
        if v > env:
            env = aa * env + (1 - aa) * v
        else:
            env = ar * env + (1 - ar) * v
        lv = 20.0 * np.log10(env + 1e-9)
        over = lv - thresh_db
        if over > 0.0:
            gr = over * (1.0 - 1.0 / ratio)
            g[i] = 10.0 ** (-gr / 20.0)
    return g

# ---------------------------------------------------------------- static EQ / misc
def biquad_sos(kind, f, q=0.707, gain_db=0.0, sr=SR):
    A = 10 ** (gain_db / 40)
    w0 = 2 * np.pi * f / sr
    al = np.sin(w0) / (2 * q)
    c = np.cos(w0)
    if kind == "peak":
        b = [1 + al * A, -2 * c, 1 - al * A]; a = [1 + al / A, -2 * c, 1 - al / A]
    elif kind == "lowshelf":
        sA = 2 * np.sqrt(A) * al
        b = [A * ((A + 1) - (A - 1) * c + sA), 2 * A * ((A - 1) - (A + 1) * c), A * ((A + 1) - (A - 1) * c - sA)]
        a = [(A + 1) + (A - 1) * c + sA, -2 * ((A - 1) + (A + 1) * c), (A + 1) + (A - 1) * c - sA]
    elif kind == "highshelf":
        sA = 2 * np.sqrt(A) * al
        b = [A * ((A + 1) + (A - 1) * c + sA), -2 * A * ((A - 1) + (A + 1) * c), A * ((A + 1) + (A - 1) * c - sA)]
        a = [(A + 1) - (A - 1) * c + sA, 2 * ((A - 1) - (A + 1) * c), (A + 1) - (A - 1) * c - sA]
    elif kind == "hp":
        return signal.butter(2, f, "highpass", fs=sr, output="sos")
    elif kind == "lp":
        return signal.butter(2, f, "lowpass", fs=sr, output="sos")
    else:
        raise ValueError(kind)
    b = np.array(b) / a[0]; a = np.array(a) / a[0]
    return np.hstack([b, a])[None, :]

def eq(x, kind, f, q=0.707, gain_db=0.0):
    return signal.sosfilt(biquad_sos(kind, f, q, gain_db), x)

def lr4_split(x, fc):
    lo = signal.sosfilt(signal.butter(2, fc, "low", fs=SR, output="sos"), x)
    lo = signal.sosfilt(signal.butter(2, fc, "low", fs=SR, output="sos"), lo)
    hi = signal.sosfilt(signal.butter(2, fc, "high", fs=SR, output="sos"), x)
    hi = signal.sosfilt(signal.butter(2, fc, "high", fs=SR, output="sos"), hi)
    return lo, hi

def true_peak_env(x):
    up = signal.resample_poly(x, 4, 1)
    n = len(x)
    up = np.abs(up[: n * 4]).reshape(n, 4).max(axis=1)
    return np.maximum(up, np.abs(x))

def limiter(l, r, ceiling_db=-1.3, look_s=0.005, rel_s=0.12):
    ceil = 10 ** (ceiling_db / 20)
    p = np.maximum(true_peak_env(l), true_peak_env(r))
    g = np.minimum(1.0, ceil / (p + 1e-12))
    W = max(1, int(look_s * SR))
    # running min over forward window
    from scipy.ndimage import minimum_filter1d, uniform_filter1d
    gm = minimum_filter1d(g, size=2 * W + 1, mode="nearest")
    gm = np.minimum(gm, np.roll(minimum_filter1d(g, size=W, mode="nearest"), 0))
    # release smoothing
    ar = np.exp(-1.0 / (rel_s * SR))
    gs = _release(gm, ar)
    gs = uniform_filter1d(gs, size=W, mode="nearest")
    gs = np.minimum(gs, gm + (1 - gm) * 0)  # never above instantaneous need within window
    return l * gs, r * gs, float(-20 * np.log10(np.min(gs) + 1e-12))

@njit(cache=True)
def _release(g, ar):
    out = np.empty_like(g)
    s = 1.0
    for i in range(g.shape[0]):
        if g[i] < s:
            s = g[i]
        else:
            s = ar * s + (1 - ar) * g[i]
        out[i] = s
    return out
