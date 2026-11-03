# Planetarium / Eno-style ambient space pad on any synth: sines at 0, +12 and +19 semitones, a triangle sub, two slow free-running smooth-random LFOs that modulate each other's rate and are mixed on every target, low-sustain amp envelope, gentle filter, and LFO-moved reverb/delay mix

Goal: Build the classic slow 'space / planetarium / Brian Eno' meditation pad from an init patch on any synth with three oscillators, two LFOs and a reverb and delay. Everything moves a little, and no two parameters move together, so the ear never locks onto a pattern. Pitch stays steady: all movement is in level, timbre and effect mix.

Source: [How to make an ambient space pad in any synth.  Sound Design Tutorial 1](https://www.youtube.com/watch?v=Oq5TCAKw64Y)

1. Init the patch and set the oscillators to sine waves: osc 1 at 0 st, osc 2 at +12 st (one octave), osc 3 at +19 st (an octave and a fifth).
2. Set up two LFOs: rate in Hz (not tempo-synced) and very slow, smooth-random shape (random but gliding, not stepped), free-running so they do not restart on each key, bipolar.
3. Cross-modulate the LFOs: send a small amount of LFO 3 to the rate of LFO 2, and of LFO 2 to the rate of LFO 3.
4. Modulate the level of the +12 osc with LFO 3 and the +19 osc with LFO 2, plus a smaller amount on osc 1 (the root should move least). On every target, mix a bit of both LFOs, sometimes inverted.
5. Add a sub oscillator one octave down using a triangle wave (square is too buzzy with sines). Add a trace of noise (pink, white or blue) for high-end character, barely audible.
6. Amp envelope: long attack, long decay, sustain lowered (sloping down), long release.
7. Low-pass filter for roundness with low resonance. Move cutoff only slightly with the LFOs.
8. Effects: a big cathedral-type reverb and a delay. Put both LFOs, mixed, on reverb dry/wet, delay dry/wet and delay feedback, but not on delay time. Low-cut the effects returns to avoid mud.
9. Turn on unison on the oscillators (several voices) with only slight LFO movement, then stop adding things. Save the patch, take a 5-15 minute break and come back for small balance tweaks.
10. Optional: add shimmer reverb tuned to +7 st (a fifth) instead of the default octave, with its mix moved slowly in and out.
11. Optional: add a low-level consistent noise bed (rain, metallic flow, forest) through a slow, subtle band-pass in parallel with the main filter. Add slow LFO on overall volume and pan, plus small EQ dips on any resonant buildup (not many narrow cuts, which cause a comb-filter effect).

Batch: `2026-10-30-morning-hunt` · transcript: YouTube-provided (Show transcript)
