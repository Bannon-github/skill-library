# Resample a synthesized epic drum into a reusable sampler instrument: record 8 spaced hits on a velocity ramp into auto velocity-split layers (soften the velocity-to-amp curve so the softest layer is still audible), or record 8 slightly different hits as round-robins for fast repeats (16ths/32nds without machine-gunning), add velocity-to-low-pass (floor about 1-1.5 kHz) and small start-time jitter, and bounce a panned 4-5 instance ensemble as its own multisample

Goal: Stop running several synth instances for one drum. Capture the epic drum (see the synth drum ensemble skill for the multi-instance setup) into a sampler with velocity layers or round-robins, so it can be reused across songs, played in fast rolls, and loaded into a Web Audio sample player for Polyrhythm Studio.

Source: [Epic Drums 4 - Sound design tutorial](https://www.youtube.com/watch?v=w8cSlVZ2KbI)

1. Set the sampler to record its input (external/aux input) with auto-advance to the next layer per hit. Turn off per-instance random envelope delay on the synth for a single-instance capture.
2. Program 8 capture notes spaced far enough apart to decay fully (no dense 16ths), alternating a little for variation. For velocity mode, scale the velocities as a ramp from low (not too low) to high.
3. Arm and play. For velocity mode, set the layer mode to auto velocity-split and reduce the velocity-to-amplitude amount so the softest layer is still audible.
4. For repeated hits or rolls, instead record 8 hits at slightly different velocities (and random settings) and set the layer mode to round-robin.
5. Add velocity to low-pass cutoff (floor about 1-1.5 kHz, harder hits open it) so soft hits sound softer even in round-robin mode. Optionally add start-time (pre-delay) jitter, a little under about 9 ms.
6. Ensemble bounce: copy the MIDI to 4-5 synth instances with different pan (about 85 L/R and 46 L/R), randomness, pitch offset, snap frequency, decay and velocity curve. Sum them to one bus and capture that bus into the sampler the same way.
7. Save the instrument with a clear name, for example 'big tom drum synth'.

Batch: `2026-10-30-morning-hunt` · transcript: YouTube-provided (Show transcript)
