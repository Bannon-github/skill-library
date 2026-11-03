# Brightness and air at the source for pads and textures

Goal: Make pads bright and airy from the start (instead of boosting treble at the end): choose harmonically rich oscillators, open and key-track the filter, add octave/fifth layers, excite upper harmonics, add a quiet air-noise layer, brighten before reverb and only then a gentle shelf.

**Theory:** Perceived brightness tracks spectral centroid, which rises with energy in upper harmonics. EQ can only boost what exists; saturation/exciters create new harmonics; octave layers add bright partials that are musically related.

**Hear it:** `sample-lab/theory/brightness_air.py`

## Workflow
1. Measure first: spectral centroid of the pad vs a reference (ambient pads ~1.5-3 kHz; dark tests sat ~0.8 kHz).
2. Oscillator: saw/supersaw or bright wavetable frames rather than sine/triangle; keep enough harmonics (no low-passed sources).
3. Filter: cutoff 3-6 kHz, key-tracking 50-100%, filter env to open on attack; avoid treble-cut on the pad.
4. Layer: octave-up sine/triangle or glock/bell partials at -12 to -18 dB; pluck/struck layers bring natural brightness.
5. Exciter: high-pass a copy at ~3 kHz, saturate (tanh/tube), blend -12 dB; or pitch-shift +12 in reverb (shimmer).
6. Air: high-passed noise >8 kHz at -24 to -30 dB following the pad envelope.
7. Brighten before reverb/delay (pre-send), not on the master; finish with a gentle 10-12 kHz shelf (+1-3 dB) only if needed.
8. Check harshness at 2-5 kHz and on small speakers; re-measure centroid.
9. Hear the theory: run `/home/box/audio-tools/bin/python sample-lab/theory/brightness_air.py` from the repo root and compare the sections; reuse its functions as a starting point for renders.
