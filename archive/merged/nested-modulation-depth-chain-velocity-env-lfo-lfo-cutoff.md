# Nested modulation depth chain: velocity → envelope decay → LFO 2 amount → LFO 1 amount → filter cutoff, for touch-sensitive rhythmic filter motion

Goal: Chain modulators so that each one sets the depth of the next, the 'modulate the modulations' approach of modular synthesis, inside any synth mod matrix. A unipolar, tempo-synced sawtooth LFO 1 (16ths, phase-bent for snap) acts as a looping filter envelope on cutoff. LFO 1's amount is zeroed and handed to a unipolar square LFO 2 (quarter notes, then quarter-note triplets) so it gates LFO 1 rhythmically. LFO 2's amount is zeroed and handed to a spare envelope whose decay brings the whole motion in and out. That envelope's decay is zeroed and driven by velocity, so soft playing gives no motion and hard playing gives the full rhythmic filter. Finish with velocity also on filter depth, key tracking, a longer 'slow' envelope tail and velocity on release. Delta vs our mod-matrix routing skill: the four-degree nested chain where only the last LFO touches the sound.

Source: [Modulate the modulations to expand your sound design with Magnolia!](https://www.youtube.com/watch?v=pYbWRCrFsHQ)

1. Start from a default patch: simple subtractive tone, close the low-pass filter, play in a lower register.
2. Degree 1: LFO 1 → cutoff. Sawtooth, unipolar (acts like a looping envelope); add phase bend for a snappier shape; tempo-sync to 16ths, and raise the tempo a little if needed.
3. Degree 2: set LFO 1's amount to zero. LFO 2 = square, unipolar, synced to quarter notes; assign it to LFO 1's amount so it ducks LFO 1 on and off. Try other resolutions; the presenter likes quarter-note triplets. Optionally add more cutoff modulation.
4. Degree 3: set LFO 2's amount to zero. Assign a spare envelope (e.g. one otherwise used for FM) to LFO 2's amount, fully up. Sustain sets the overall motion; use decay to bring the whole modulation up then away.
5. Degree 4: set that envelope's decay to zero and assign velocity to the decay. Soft playing gives no modulation; harder strikes emphasise it.
6. Refine for consistency: use the same velocity on filter modulation, add keyboard tracking so upper notes are brighter, use the envelope's slow mode for a longer tail, add release time and put velocity on the release too.

Batch: `2026-10-15-morning-hunt` · transcript: YouTube-provided (Show transcript) · Short tutorial; route.py said COVERED but hand-check found the nested depth-chain not covered by the mod-matrix basics skill.
