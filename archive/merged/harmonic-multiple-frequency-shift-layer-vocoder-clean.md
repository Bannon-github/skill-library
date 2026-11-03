# Harmonic-locked frequency shifter layer (shift by multiples of f0) cleaned with EQ, micro-delay and a self-vocoder

Goal: Tame a frequency shifter into musical harmonics: shift by whole multiples of the note's fundamental (e.g. +130 Hz on a 130 Hz C, or 6×40 = 240 Hz on a 40 Hz E) so new partials land on the harmonic series instead of dissonant arbitrary shifts, run it as a parallel wet layer with low-cut/band-reject EQ to tame the shifted fundamental, add ~1 ms signal delay to stop bubbly phasing, and clean messy upper harmonics with a self-vocoder whose lowest band sits above the sub, keeping the clean sub on a dry path.

Source: [Chaos To Order: Frequency Shifter & Vocoder (Sound Design Tutorial)](https://www.youtube.com/watch?v=54eGln75Y3Y)

1. Start on a plain sine to learn it: note C ≈ 130 Hz. Add 130 Hz shift → up an octave; add multiples (260, 390, 520 …) and listen to each land on further harmonic-series notes (fifth, octave, third…).
2. Compare with an arbitrary shift (e.g. 174 Hz) to hear dissonant overtones.
3. Apply to a richer sound (e.g. a bass an octave down); harmonics that already line up change little, other patches gain dark, cool harmonics. Blend with the original.
4. Build a dry/wet split; on the wet path add EQ to tame the loud shifted 'fundamental' (low cut, or a band reject; low cut before the shifter also works).
5. If the layer bubbles/phases (shifts under ~1 kHz), add a ~1 ms signal delay to the path to remove it.
6. Clean the messy layer with a vocoder on itself: lowest band set above the sub so lows are untouched, run it on another dry/wet chain so the clean sub stays; adjust band count/bandwidth (narrower = crystalline/metallic), formant and per-band levels as EQ.
7. Example bass: FM sine with modulator ×8, E at 40 Hz, shift ×6 = 240 Hz, EQ wet to keep only above ~400 Hz, vocoder, two saturators, rhythmic delay and a wash reverb; automate shifter/vocoder for performance.
8. Iterate non-linearly: revisit earlier FX settings after adding later ones.

Batch: `2026-10-13-morning-hunt` · transcript: YouTube-provided (Show transcript)
