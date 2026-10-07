# Build whooshes from noise and synth layers: bus envelope + Doppler pass-by, rising-only variant, and mod-wheel performable whoosh

Goal: Create transition whooshes without stock whoosh packs: record steady white/pink noise plus air/texture layers and a high-passed synth render into one bus, shape it with a volume swell and a Doppler-style pass-by (start/centre/end, attenuated pitch change), compress and limit it, add a rising-only variant using an upward pitch-shift curve plus a narrow EQ band swept up, or play a synth whoosh live with one mod-wheel macro that opens the filter, raises noise and raises flanger wet together.

Source: [How to design 'Whoosh' sound effects [EASY]](https://www.youtube.com/watch?v=uFk9xUVg7Q0)

1. Generate steady white noise and record/print it to audio so the generator is not running constantly.
2. Add texture layers (e.g. a cymbal/metal tail, heavy wind) and route all layers to one whoosh bus.
3. Draw a volume envelope on the bus that swells in and back out to give the basic 'wash'.
4. Add a Doppler-style pass-by: set where the action starts, where it ends, and the centre/listener point where the pass is heard; attenuate the pitch change if it is too big and move the transition/listener points to taste. Portable alias: pitch up-then-down curve + level peak at the centre + pan sweep.
5. Vary the character by muting/swapping layers: drop the metal layer for a more airy result; swap white for pink noise, low wind for higher wind, add rain for whiter noise.
6. Compress the bus (a whoosh should not be in your face) and add a limiter with a ceiling around -0.2 dB.
7. Add a synth layer: render one or two notes of a noisy/FX patch, high-pass/cut the excess low frequencies, and send it to the whoosh bus.
8. For longer actions, stretch the Doppler start/end across the longer selection and increase pitch for a stronger transition; add reverb on an FX return.
9. Rising-only whoosh (Doppler always goes up then down): use a pitch-shift effect with an upward curve, reduce the range, start lower, pick a smoother algorithm; also set a narrow EQ band very low and automate its frequency sweeping upward (reduce gain if too strong); time-stretch faster/slower with a tape-style algorithm, then add reverb.
10. Performable synth whoosh: map one mod wheel/macro to open the filter, raise the white-noise amount and raise a flanger's wet mix together; play the whoosh live to any length - no stretching artifacts, and the flanger keeps the sustained top moving so it is not annoying.

Batch: `2026-10-07-morning-hunt` · transcript: YouTube-provided (Show transcript)
