# Three rules for making a randomised/Euclidean sequencer sound intentional: constrain (scale, octave range, pitches pulled close, phrase length), repeat (global randomness to zero, reset per-step random, restart points so the phrase retriggers each bar), and simplify (about three pitches, fewer pulses, complexity from layering simple parts), then add hand-made variations on chosen cycles and random pitch options on only the last few notes

Goal: Fix a generative patch that sounds aimlessly random. Rule 1, constrain: set a scale (e.g. minor), reduce octave range/voicing, and pull spread-out notes into closer octaves; limit phrase length. Rule 2, repetition creates anticipation: turn global continuous randomisation to zero, reset any per-step randomisation (use only a little, on a couple of notes), and set a restart point so the pitch and trigger lists start together each bar, so the ear can remember the hook. Rule 3, less is more: cut to about three pitches and fewer pulses; get complexity from several simple layers, not one complex one. Then add intentional variation: in a later cycle (e.g. bar 2) add extra notes, copy that variation to other cycles, move start points, push one note up an octave or add a roll; for controlled surprise, give only the last four notes extra pitch options. Apply the same rules to each part. Complements our probability/seeded generative skills as the taming pass.

Source: [Torso T1: The 3 Rules That Make Generative Sequencing Musical](https://www.youtube.com/watch?v=gyhfAdy6eq8)

1. Solo one part. Set a scale, reduce octave range, and move notes into nearby octaves.
2. Set global continuous randomisation to zero and reset per-step random amounts on all steps.
3. Add a restart point so pitch and trigger cycles realign at the start of every bar.
4. Reduce to about three pitches and fewer pulses; optionally add a second restart point.
5. Pick a cycle (e.g. bar 2) and hand-add notes; copy that variation to other cycles, change start points, raise one note an octave, add a roll.
6. Give only the last few notes (e.g. last four) extra pitch options or randomisation.
7. Repeat rules 1–3 for each other part and listen to them together.

Batch: `2026-10-21-morning-hunt` · transcript: YouTube-provided (Show transcript) · Hardware-sequencer walkthrough; membership promotion dropped.
