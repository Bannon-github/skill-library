# Sample Lab — Quality Target ("quality product" definition)

Defined **2026-10-03 before any candidate was rendered or iterated**. Thresholds were not tuned
after seeing results; any later change must be logged as a new target version (this is v1).

A *quality product* = a 48 kHz / 24-bit stereo WAV, 8–12 s, that a producer could drop into a
cinematic/ambient session (Polyrhythm Studio, Traveler-inspired) with **no technical fixes needed**:
correct loudness and headroom, mono-safe, centered low end, balanced tonal tilt, no harsh resonances,
audible movement over time (not static), clean start and tail, no hiss/dropouts, reproducible.

## 1. Hard gates (any failure ⇒ render FAILS regardless of score)

| id | metric | pass |
|---|---|---|
| G1 | True peak (4× oversampled) | ≤ −1.0 dBTP |
| G2 | Clipped samples (|x| ≥ 0.999) | 0 |
| G3 | DC offset per channel | |mean| ≤ 0.001 (−60 dBFS) |
| G4 | Determinism: same system + note + seed rendered twice | bit-identical (max abs diff = 0) |
| G5 | Clean tail: RMS of final 100 ms | ≤ −60 dBFS (sample ends in silence, no truncation) |
| G6 | Clean start: first 2 ms peak | ≤ −30 dBFS (no onset click) |
| G7 | Finite audio | no NaN/Inf |

## 2. Scored metrics (each → sub-score 0..1; 1 inside band, linear fall-off to 0 over the stated tolerance)

| id | metric | band (pads/drones/swells/gated) | band (pluck) | band (bass) | tol | weight |
|---|---|---|---|---|---|---|
| M1 | Integrated loudness (BS.1770, pyloudnorm) | −18 … −13 LUFS | −18 … −13 | −17 … −12 | 4 LU | 1.0 |
| M2 | Mono-fold loss = LUFS(stereo) − LUFS(mid-only) | ≤ 3.0 dB | ≤ 3.0 | ≤ 1.0 | 3 dB | 1.5 |
| M3 | Broadband L/R correlation | 0.15 … 0.90 | 0.15 … 0.95 | ≥ 0.80 | 0.3 | 1.0 |
| M4 | Stereo width = RMS(side)/RMS(mid) | 0.25 … 0.85 | 0.15 … 0.80 | 0.00 … 0.35 | 0.3 | 1.0 |
| M5 | Low end centered: side/mid energy < 150 Hz | ≤ −15 dB | ≤ −15 | ≤ −20 | 10 dB | 1.5 |
| M6 | Spectral tilt: LTAS slope 100 Hz–10 kHz (dB/oct, octave-band fit) | −6.5 … −2.0 | −6.5 … −1.5 | −9 … −3 | 2 dB/oct | 1.0 |
| M7 | Spectral balance: no octave band 63 Hz–8 kHz deviates > X dB from the tilt fit | ≤ 9 dB | ≤ 9 | ≤ 10 | 6 dB | 1.0 |
| M8 | Harshness: max narrow-peak prominence in 1.5–8 kHz (1/24-oct LTAS vs 1/3-oct smooth) | ≤ 8 dB | ≤ 8 | ≤ 8 | 6 dB | 1.5 |
| M9 | Harsh-band energy: 2–5 kHz energy relative to total | ≤ −12 dB | ≤ −10 | ≤ −16 | 6 dB | 1.0 |
| M10 | Temporal evolution: std of log2(spectral centroid), 100 ms frames, body region | 0.06 … 0.9 oct | 0.10 … 1.5 | 0.04 … 1.0 | 0.05 | 1.5 |
| M11 | Spectral flux (mean normalized frame-to-frame change), body region | 0.010 … 0.30 | 0.02 … 0.5 | 0.005 … 0.3 | 0.02 | 0.75 |
| M12 | Hiss: energy > 12 kHz relative to total | ≤ −24 dB | ≤ −22 | ≤ −30 | 8 dB | 0.75 |
| M13 | Dropouts: body frames below −60 dBFS (non-gated categories) | 0 % | 0 % | 0 % | 10 % | 0.75 |
| M14 | Limiter work: max gain reduction from the master safety limiter | ≤ 3 dB | ≤ 4 | ≤ 4 | 4 dB | 1.0 |
| M15 | Loop seam (drone + gated loop exports only): |level(last 50 ms) − level(first 50 ms)| | ≤ 1.5 dB | n/a | n/a | 3 dB | 1.0 |

"Body region" = from 15 % of the note-on time to note-off (where the held sound lives). Gated/rhythmic
pads are exempt from M13 (silences are intended) and use a 0.10–1.2 oct M10 band.

**Composite score** = 100 × Σ(weight·sub-score)/Σ(weight).

## 3. Pass bar

- A *render* passes if: all hard gates pass **and** composite ≥ **85** **and** no scored sub-score < 0.5.
- A *system* (workflow chain) passes **reliably** if every render passes across a test grid of
  **3 notes/chords × 2 seeds = 6 renders**, and its *robust score* = min composite over the grid.
- Leaderboard ranks by robust score, then mean score.

## 4. Perceptual sanity (lightweight)

For every winning system a log-frequency spectrogram PNG (L and Side) is generated and inspected by eye
(via Read) for obvious artifacts: aliasing fans, zipper/stair-step modulation, clicks (vertical lines),
broadband hiss, metallic ringing lines, abrupt tail cut. Any visible artifact disqualifies the system
even if metrics pass; findings are noted in the leaderboard.

## 5. Explicit non-goals / caveats

Metrics measure *technical deliverability and movement*, not taste or musicality. Passing = "safe to ship
and not static", not "beautiful". The offline numpy/numba renderer approximates Web Audio / Traveler modules.
