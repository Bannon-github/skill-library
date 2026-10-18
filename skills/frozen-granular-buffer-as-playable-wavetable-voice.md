# Frozen granular buffer as a playable 'wavetable' voice: capture an evolving sound, freeze, scan time position, sequence pitch via v/oct for overlapping grain polyphony, random-modulate time/size

Goal: Turn a granular processor's freeze into an instrument: capture an evolving sound into the buffer (lower-quality mode for ~10 s stereo / 20 s mono), freeze it, trigger seeds from gates, scan the time/position control through the capture like a homemade wavetable, sequence the frozen audio's pitch via v/oct so overlapping grains create a polyphonic illusion, use built-in random modulators on time and grain size, triangle grain window, reverb/delay, and for dark textures pitch the frozen capture down with high density and heavy reverb — the delta vs our granular-stack-freeze skill is pitched, sequenced playback of the frozen buffer.

Source: [Mutable Instruments Beads FREEZE Explained – Frozen Textures & Tricks](https://www.youtube.com/watch?v=Dazk-D79k5U)

1. Run the granular processor fully wet; generate grains with the seed control; set mid size and a triangle grain shape (fades in and out cleanly); add reverb — integral to big ambient textures.
2. Patch a gate into the seed input and adjust density (grains per seed — it can reach audio rate).
3. Select a lower-quality buffer mode to get more record time (presenter: ~10 s stereo / 20 s mono), play an evolving sound in, and freeze it.
4. Scan the time/position control through the frozen audio — like creating your own wavetable.
5. Patch a pitch sequence into v/oct so the frozen buffer is played melodically; use the internal random modulators (attenurandomizers) on time and size; add reverb and delay. Overlapping grains give a polyphony-like overlap.
6. Try reversed grains for variation.
7. Dark texture variant: capture a simple tone, pitch the frozen buffer down with density high and reverb high, keep slow random modulation on time so it scrolls and occasionally surfaces higher partials ('ominous wind chimes'); play root changes from a sequencer.
8. Optional: modulate freeze itself with gates to alternate between live grains and long held frozen notes.

Batch: `2026-10-14-morning-hunt` · transcript: YouTube-provided (Show transcript)
