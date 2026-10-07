# Synth-built pitch riser: 2-octave bend ramp with reset points, smeared by a resonant diffusion filter and reverb

Goal: Build a synth-only riser that does not sour the key: one saw swept by a full-clip pitch-bend ramp from -1 to +1 octave (with reset points so mid-clip playback starts clean), then smeared by a low-set, high-resonance phase-smearing (comb/allpass-diffusion style) filter with a slight slow LFO and a reverb, so the listener hears a rising swarm rather than a clearly out-of-key moving pitch.

Source: [Serum Tutorial - How To Make Risers](https://www.youtube.com/watch?v=9v-p2k8Nnec)

1. Start with a single oscillator on a saw wave (choose the tone you want); turn effects off while setting up.
2. Set the pitch-bend range to 12 semitones so a full bend travels from -1 octave to +1 octave (two octaves total) - the bend range defines the distance the riser travels.
3. Automate pitch bend as one ramp across the entire clip, starting exactly at the bottom (-1 oct) and ending exactly at the top (+1 oct). Add small reset points at the clip start and end that return bend to 0, so playback started partway through does not begin with a mangled/latched pitch.
4. Recognise the problem: a constantly moving pitch only lands on an in-key note for a split second, so if the pitch is clearly discernible it makes the track sound sour - so smear it.
5. Insert a phase-smearing resonant filter (source: a 'reverb'-type filter; portable alias: short comb/allpass diffusion filter). Set cutoff LOW with HIGH resonance - set high it affects too little of the sound; low with high resonance it blurs where the pitch was into where it is.
6. Add an LFO for very slight, slow movement of that filter: with no movement it does not smudge, with too much movement the effect is lost.
7. Add reverb afterwards to smear further (its micro-delays carry the pitch just passed into the current pitch).
8. Optional finishing (not vital to the sound): sidechain compression, basic EQ, auto-pan pumping.

Batch: `2026-10-07-morning-hunt` · transcript: YouTube-provided (Show transcript)
