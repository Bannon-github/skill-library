# Marimba/pluck WT LFO attack into granular freeze pad stack

Goal: Turn mallet-like material into an evolving pad: synthesize a pluck from a wavetable that starts bright and ends as sine, scrub position with a very fast LFO for a clicky attack (amp: ~0.5s decay, 0 sustain, ~1s release) plus a long-attack twin for swell; print chord tones, freeze them in a granular engine (random on, loop on, tune grain spacing/attack/hold), then space with short delay, room (~20%) and very long parallel verbs, plus a quiet triangle+chorus bass.

Source: [Tutorial #21 | Turning A Marimba Into Granular Synthesis Pads](https://www.youtube.com/watch?v=Daqws1QWgXw)

1. Pluck layer: one osc with a mallet-like WT (rich highs at frame 0 → sine at the end). Modulate WT position with LFO1 at a very high rate so you mostly hear the bright click, then the sine body.
2. Amp envelope: decay ~0.5 s, sustain 0, release ~1 s. Add delay+reverb. Optional: set LFO to trigger (retrigger) mode so fast WT scrubbing repeats like a decaying delay while amp has no sustain.
3. Swell twin: duplicate the pluck patch and add substantial amp attack so the same WT becomes a slow pad swell (works with one-shots too — just raise attack).
4. Sequence sparse chord tones (e.g. B D F#) split across two octaves so each note can ring; render/print pluck and swell passes to audio.
5. Load both into a granular engine: random fully up (forward/back from random points, occasional overlaps), loop on, raise grain attack and adjust grain spacing to slow frantic textures, increase hold for more sustain. Match settings on the swell buffer.
6. FX: delay with low feedback (~3 repeats), room reverb ~20% mix with highs eased, plus a parallel bus of very long verbs (~10–12 s) at 100% wet while keeping a dry path for clarity.
7. Optional bass: quiet triangle with chorus and long attack (mallet pads rarely need loud subs). Optional high air: heavily blurred/smudged print of the pluck and/or low-level ambience into the same reverb bus.

Batch: `2026-10-12-morning-hunt` · transcript: YouTube-provided (Show transcript)
