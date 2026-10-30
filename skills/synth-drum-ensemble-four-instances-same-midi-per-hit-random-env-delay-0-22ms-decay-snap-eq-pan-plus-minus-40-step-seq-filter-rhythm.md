# Make one synth epic-drum patch sound like an ensemble of drummers: copy it to about four instances on the same MIDI, give each a different global decay, snap-EQ frequency and pan (about ±40), and add per-note random envelope delay (about 0-22 ms, tighten to about 7 ms, too loose at 65 ms) so the hits flam naturally. Optionally drive a filter with a tempo-synced step sequencer for rhythmic patterns

Goal: Layer synthesized epic drums into a big, human-feeling ensemble quickly. Copying the same patch and MIDI usually just sounds like one louder hit. Put a few macro controls on the patch (global decay, snap frequency, global pitch, timing randomness) so each copy differs with a few slider moves, instead of editing each synth and the MIDI by hand.

Source: [Epic Drums 3 - Sound design tutorial](https://www.youtube.com/watch?v=ALHZHHPAdI0)

1. Add macros to the patch: global decay (amp-env and filter-env decay together), snap frequency (a peaking EQ band on the attack), global pitch in semitones (about ±4) and randomness depth.
2. Add a per-note random modulator (new value on every MIDI note) on the amp-envelope delay and filter-envelope delay. Range about 0-22 ms at 50% randomness; 100% gives about 0-65 ms (too loose), and about 9% gives about 7 ms (tight).
3. Write a simple pattern on instance 1, then duplicate the instance and its MIDI about three times.
4. On each copy, move the macros differently: decay up or down, snap frequency up or down, randomness slightly different, small fixed pitch offset. Pan pairs about 39-40 left and right.
5. Listen and tighten: if a layer is too loose, lower its randomness (for example 86 to 68, 90 to 60).
6. Optional rhythmic variant: an arpeggiator on eighth notes or a tempo-synced step-sequencer LFO driving the filter cutoff range. Change the step pattern or rate (8 to 16 steps, double speed) for new grooves. Lengthen the attack to turn hits into reverse-drum or noise-sweep textures.

Batch: `2026-10-30-morning-hunt` · transcript: YouTube-provided (Show transcript)
