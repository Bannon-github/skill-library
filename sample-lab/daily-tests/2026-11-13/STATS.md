# Smear Key (2026-11-13)

Score 99.75 pass. LUFS -17.0, TP -4.3 dBTP, length 82.5 s, 808 + soft kick in at 11.4 s (bar 5 at 84 BPM; pads only before). Limiter GR 0 dB.

Skills (all three from the 11-13 morning hunt, first test):
- arp-smear-pad-grain-delay-resample-stretch-2x-high-wet-echo-spectral-freeze-retrigger-16th-eq-band-plus-feedback-bandpass-loop-motion
- noise-recording-tuned-to-key-stacked-max-q-eq-boosts-at-root-freeze-flatten-chromatic-sampler-pad-attack-verb-delay-sidechain-eq-automation
- punchy-808-2nd-3rd-harmonic-partials-subtle-unipolar-coarse-pitch-dive-convex-decay-fm-ratio-half-transient-two-stage-softclip-zero-cross-print

Checks: side<120 Hz -22.6 dB; tuned-noise spectral peak 220.0 Hz (A3 root, 4 series peaks Q30 +18 dB); 808 2nd/3rd partials -14.4/-15.2 dB vs fundamental, pitch -15 cents after 60 ms (dive +3 st, 35 ms, unipolar), tail ends on zero crossing; low<120 Hz -2.7 dB vs full mix in the main section; first/second half loudness equal.

A minor 84 BPM, 28 bars. Arp: Am9 down 2 octaves 8ths -> grain delay (70 ms grains, 120 ms + 35 ms spray, pitch 0) + reverse 1/4 repeats -> resample -> OLA stretch x2 -> echo 80% wet fb 0.62 -> STFT freeze recaptured every 1/16 with linear crossfade between captures (no stutter) -> band 220 Hz-10 kHz. Feedback layer: sparse A-minor sine loop -> dotted-1/2 feedback with ~3 kHz band-pass, 1-bar LFO crossfading narrow/wide width, tanh drive -> resampled -> bars 6-8 looped with crossfade, in bars 8-18 and 22-27.
Iter 1 91.95 fail: M6 tilt -9.8 (too dark: 6-harmonic arp LP 2.6k, tuned noise is almost pure 220 Hz after 72 dB of stacked boosts). Iter 2 93.2: arp brighter, still -9.1. Iter 3 86.0: added the raw (pre-EQ) noise as step-8 "more noise" layer HP 4k -> tilt ok but >12 kHz too hot (M12) and centroid swing (M10). Iter 4-5: air band-limited 3-9 kHz and kept out of the sidechain duck; M10 still 1.04 because the 808 dominated alternate frames. Iter 6: 808 level 0.55->0.36, kick 0.35->0.28 -> 99.75 pass.
Click check: hf_env 12-40 Hz -0.7 dB is the steady air-noise layer; A/B with air muted gives -17.8 dB (score 94.3, darker) -> no rapid clicking texture.
Unclear: arp-smear step 1 "rate as wanted" (used 1/8); freeze "retrigger 1/16" needs a crossfade length (used the whole 1/16 linear morph). Tuned-noise skill's 3-5 max-gain stacks leave almost no broadband noise, so the pad is dark/tonal unless the step-8 "more noise" EQ automation is read as blending the raw source back in (did that, band-limited 3-9 kHz). 808 skill gives no partial levels, dive amount or decay length (used h2 0.5, h3 0.12, +3 st/35 ms, 1.6 beats convex).
