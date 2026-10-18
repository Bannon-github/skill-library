# Evolving cinematic drone: random-modulated LFO rates on WT position and two parallel, opposite-panned filters, plus a randomized granular sample layer and FX chain

Goal: Build a one-key evolving cinematic drone where nothing repeats: a wavetable oscillator whose position is swept by a very slow free-running LFO whose RATE is itself nudged by a slow smooth random modulator (small amount, ~0.07), super-unison (~2.4 detune), 1 s positive-curve attack / ~4 s decay / lower sustain / 2 s release, filter 1 (resonance, keytrack, drive, filter envelope, tiny random LFO on cutoff) and a parallel 12 dB MS-20-style filter 2 driven by a second slow LFO with its own random rate modulation (~0.13), the two filters panned ~40% left/right; add a granular sample engine (triangle grains, randomized density/size/volume/pitch, LFO-scanned start position) and a touch of white noise into both filters; FX: shimmer → ping-pong tape echo (dotted 1/8) → gentle multiband compression on lows/highs, plus reverb → soft tape distortion → second reverb, mod wheel to drive.

Source: [Create Evolving Cinematic Drones In Pigments - Full Tutorial](https://www.youtube.com/watch?v=fxh2ccZKEb0)

1. Wavetable engine: pick a folded/rich table; route LFO1 (free-running, very slow) to wavetable position from a start around the table's middle.
2. Make LFO1's speed drift: route a slow, smooth, free-running random modulator to LFO1 rate with a small amount (~0.07) so the sweep speeds up and slows down unpredictably.
3. Size: super-unison with ~2.4 detune, main tune 0; no glide/legato.
4. Amp envelope: ~1 s attack with slightly positive curve, ~4 s decay, slightly lower sustain, ~2 s release. Second envelope similar for filter.
5. Filter 1: lowered cutoff with filter envelope, some resonance, keytracking (higher keys open more) and a little drive; add LFO1 to cutoff with a tiny range.
6. LFO2: another slow free-running LFO whose rate is modulated by a second random source (~0.13). Add filter 2 as a 12 dB low-pass with character (MS-20-like), set filters to PARALLEL, send sources to both, and let LFO2 move filter 2 cutoff. Pan filter 1 ~40% left and filter 2 ~40% right.
7. Engine 2 (granular): load an original granular-friendly sample into both filters; enable granular with random density both directions, random size, some random volume and pitch; change grain shape to triangle (smoother than the rhythmic default); scan the start position with LFO1.
8. Add a little white noise into both filters (no sub needed).
9. FX A: shimmer (bigger size) → tape echo ping-pong dotted 1/8 → multiband compression mostly taming lows (and some highs) while letting mids through. FX B: reverb (longer decay) → soft tape distortion → second reverb.
10. Map mod wheel to distortion drive; trim low end/clipping as needed and save.

Batch: `2026-10-14-morning-hunt` · transcript: YouTube-provided (Show transcript)
