# Turn a synth tom-style epic drum hit into a distant low explosion / drop boom: harmonic bass enhance plus an octave-down sub, a 6 dB/oct low-pass instead of an attack boost, reverb low-cut around 100 Hz at 24 dB/oct, a band-limited quarter-note delay with about 7 ms early/late L/R offsets, a parallel tremolo or auto-pan tail whose depth is faded in by a delayed envelope, and an optional low comb filter (about 14-40 Hz) for a modern metallic drop

Goal: Make a far-away 'whoa, what happened' cinematic boom for drops and section hits, starting from a synthesized drum hit (see the epic hybrid drum / taiko-from-noise skills for building the hit itself). This skill adds the distance, sub and tail processing: a rumbling, darker boom with a moving stereo tail.

Source: [Epic Drums 2 - Sound design tutorial](https://www.youtube.com/watch?v=ZYn08bUlmG0)

1. Play the hit lower on the keyboard so it sounds less like a tom. Reshape the body with filter-envelope decay, cutoff, resonance and noise amount.
2. Add harmonic bass enhancement plus a sub oscillator one octave down (two octaves only if needed). Move the low-cut EQ from about 83 Hz down to about 50 Hz and steepen it from 24 to 36 dB/oct.
3. Remove any attack/snap boost band and replace it with a gentle 6 dB/oct low-pass.
4. Reverb: low-cut the reverb itself at about 100 Hz with a 24 dB/oct slope (by ear), choose a large impulse and set the mix to about 40%.
5. Optional: add a tempo-synced quarter-note delay with resonance off, high-pass the delay at about 90 Hz and low-pass it at about 4 kHz, and lower its level. Offset the left repeat about 7.3 ms early and the right about 7.3 ms late.
6. Optional parallel tail: split the signal after the reverb into a parallel lane with a tremolo (rectangle, eighth notes, depth up, blend about 50%). Drive the tremolo depth with an envelope: delay about 140 ms, decay about 2 s (match the reverb length), sustain 0.
7. Alternative tail: replace the tremolo with a quarter-note auto-pan using the same envelope on depth, or put distortion or other modulation on the parallel lane.
8. Optional modern 'deep metal' drop: add a comb filter on the lane, tuned low, about 14-40 Hz (12 Hz is too low), with feedback about 50% and max frequency reduced to tame the highs. Blend it with the split ratio, and you can add the delay after it.

Batch: `2026-10-30-morning-hunt` · transcript: YouTube-provided (Show transcript)
