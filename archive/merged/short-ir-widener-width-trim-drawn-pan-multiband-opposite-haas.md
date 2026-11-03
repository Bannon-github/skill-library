# Mono-safe width tricks: a 100%-wet short room IR as a stealth widener with width trim and gain make-up, a drawn and smoothed auto-pan rhythm, and Haas kept ≤15 ms split across bands tilted in opposite directions

Goal: Widen one headline element so it still works in mono. (1) Stealth IR widener: convolution with a short, thin-room impulse at 100% wet and decay down to ~20% so there is no audible tail. It widens and re-colours the chords. Because width makes the part quieter in mono, trim stereo width to ~65% and add ~+6.5 dB to match levels instead of lowering the mix. (2) Rhythmic auto-pan: start ~50% amount, then draw a stepped pan curve that fits the arp, round it with smoothing, optionally switch to unsynced Hz set by ear, and add a touch of multiband treble reverb before the panner. (3) Haas without the lopsided, phasey mono sum: keep the L/R delay ≤15 ms, tune it while listening in mono, tilt a mid band to one side and the treble band to the other, then reduce width and re-level. Use it on incidental FX rather than lead vocals. Use width with restraint so the one wide element stands out. Delta vs our Haas/phase-offset, high-band pan and asymmetric L/R skills: the IR widener with width trim, drawn pan rhythm, and opposite-tilt multiband Haas.

Source: [3 Stereo Width Tricks (That Sound Great In Mono)](https://www.youtube.com/watch?v=Mm5eO24aAec)

1. Insert convolution reverb on the chords at 100% wet with a short, thin room IR and decay reduced to ~20% so no tail is heard. Audition other short IRs for different timbres.
2. Sum to mono: the widened chords drop in level. Instead of lowering the wet mix, follow with a width control at ~65% and raise gain ~6.5 dB to level-match.
3. Rhythmic pan for arps/synths: auto-pan at ~50% amount, try LFO shapes, then draw a custom stepped pan curve and add smoothing to round its edges. Optionally switch rate to unsynced Hz and set by ear to fit the part.
4. Add a touch of multiband treble-only reverb before the panner for air; adjust pan mix lower for just a flutter, or full for strong L/R jumps.
5. Haas: duplicate L/R with a delay on one side. Keep it at ≤15 ms and tune it while listening in mono until acceptable.
6. Fix the lopsided tilt: split into bands, tilt the mid band to the right and the treble band to the left, then reduce width and re-level.
7. Apply these to one headline sound (incidental FX/ear candy for Haas) while keeping most of the mix centred.

Batch: `2026-10-15-morning-hunt` · transcript: YouTube-provided (Show transcript) · Vendor-sponsored tutorial; plugin names mapped to generic convolution/width/pan modules; demo links dropped.
