# Generative rhythmic sequence from a hand-written 8-step pattern: live length and start-point changes, chance-based rests, a 5-step Euclidean trigger length phasing against the 8 steps (a 40-step cycle), random modulation of octave and scale degree kept subtle, random distortion and release for accents and note lengths, smooth-random slow LFOs on filter and wavetable position, introduced gradually in performance

Goal: Turn a short, intentional sequence into an evolving techno or ambient line without writing new notes. Start from a programmed 8-step pattern (or, for pure random, a one-step root note with random → scale degree attenuated to about 7–8 degrees, which gives quantised random melodies within one octave). Vary it by changing pattern length and start point while it plays. Add rests with chance (about 75% means roughly one in four steps silent) and/or a Euclidean trigger length that does not divide the step count (5 against 8): with chance slightly under 100% (about 90%) the 5-step trigger pattern shifts across the 8 notes and the cycle repeats only after 40 steps. Add a tempo-synced delay so echoes fill the rests. Then add pitch variation by patching random to octave (positive for up, negative for down jumps) and to scale degree (jumps of about 4–5 degrees), keeping both subtle so the line's shape survives. Add sound variation: random → distortion (accents) and random → release (note lengths, with a lower base release), and slow smooth-random LFOs (around 5 s) on filter cutoff and wavetable position. Don't use everything at once; bring modulations in gradually across a set.

Source: [Part 2: Generative Sequencing for Techno (or any other style of music)](https://www.youtube.com/watch?v=mb3yqXO9JiE)

1. Program an 8-step sequence (or one root step plus random → scale degree around 7–8 degrees for an instant quantised random melody). Save it as the base.
2. While playing, change pattern length and set a different start point to get variation from the same notes (e.g. steps 1–16 vs 17–32 for different song sections).
3. Set chance to about 75% for random rests. Alternatively set a Euclidean trigger length of 5 with chance about 90%, so the 5-step trigger pattern drifts across the 8 notes.
4. Add a tempo-synced delay so echoes land in the rests.
5. Patch random → octave (positive = up jumps, negative = down) and random → scale degree, attenuating until jumps of about 4–5 degrees appear. Optionally map degree to a knob to sweep between bassline and lead register.
6. Patch random → distortion for accents and random → release for varied note lengths; lower the base release so variation is audible.
7. Add LFO X (smooth random, slow) → filter cutoff and LFO Y (smooth random, about 5 s) → wavetable position, with base position above zero.
8. When performing, start with the plain sequence and introduce degree, octave and timbre modulation one by one over time.

Batch: `2026-10-21-morning-hunt` · transcript: YouTube-provided (Show transcript) · Hardware walkthrough; firmware-version, Discord, release-pricing talk and the closing jam (music only) dropped.
