# Pendulum Sequence 2: timing analysis (measured from the video frames)
Source: the Virtual Riot "I heard you like polyrhythms" clip (Ableton, track "29-MIDI"). Frames at 20 s, 100 s (slowed to 0.25x) and 120 s.
Method: I measured the coloured runs of piano-roll notes in each of the 35 lane rows (where a row's saturation is >60), then ran a linear fit of note-to-note spacing against lane index. The bar/beat ruler gives the pixel scale (f_100: "1.4.3 … 3.1.3" = 262 px/beat; f_20: "38.1.3 … 38.2.3" = 1156 px/beat). Data: `timing-analysis.json`; crops: `analysis/`.

| measure | f_20 | f_100 | g_120 |
|---|---|---|---|
| top lane (E8) period | 578 px = 0.50 beat | 131.2 px = 0.501 beat | 426 px |
| period change per lane (downwards) | +0.244 % | +0.249 % | +0.241 % |
| bottom (E1) / top period | 1.083 | 1.085 | 1.082 |
| note length / period | 0.372 | 0.364 | 0.371 |
| fit residual (linear period / linear freq) | 0.8 / 0.8 px | 0.5 / 0.5 px | 0.6 / 0.6 px |

- **Tempo:** 30.00 BPM, 4/4 (transport readout).
- **Lanes (folded roll, top to bottom), 35 in all:** E8 D8 B7 A7 G7 F#7 E7 D7 B6 A6 G6 F#6 E6 D6 B5 A5 G5 F#5 E5 D5 B4 A4 G4 F#4 E4 D4 B3 G3 E3 D3 B2 G2 E2 B1 E1. This is E minor / G major with no C; below E4 it thins to E-G-B-D, then E-B.
- **Timing law in plain words:** every lane repeats one short note. The top lane repeats every half beat (1 s at 30 BPM), and each lane further down is about 0.245 % slower, so the bottom lane repeats about 8 % slower. Every note lasts about 37 % of its lane's period. All lanes start together, so the "descending staircase" isn't programmed: it is the drift. The top lanes run ahead, which draws a diagonal that keeps steepening into curves. The data can't tell "linear period" from "linear frequency" apart. Modelled as a pendulum wave (lane i makes N−i cycles while the top lane makes N, with N ≈ 408), every lane coincides again after about 408 top-lane cycles, about 6.8 min at 30 BPM.
- **Layers:** tracks 20–29 hold ~10 copies of the clip on "30-Massive" instruments, and the arrangement shows identical-looking clip patterns. I did not measure exact per-track offsets; the template uses ±9 ms and ±7 cents.
- **Spectrum readout:** the peak was −21.1 dB at 785.9 Hz (G5 +4 cents). The waterfall shows short notes with a fast decay and a dense harmonic comb that rolls off strongly above a few kHz. Template voice: a 3-saw stack, lowpass at 2.4 kHz, 3 ms attack and an exponential decay.
- **Not done:** the audio onset cross-check (optional) and per-track (20–29) offset measurement.
