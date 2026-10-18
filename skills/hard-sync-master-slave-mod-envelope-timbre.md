# Hard oscillator sync: master sets pitch, slave pitch + mod envelope sets timbre

Goal: Build a classic hard-sync lead voice where oscillator 1 (master) resets oscillator 2 (slave) each cycle so master pitch is the note and slave pitch is timbre; sweep slave pitch with a mod envelope (high amount, slave starting an octave down) for the characteristic sync squeal, then add tempo delay, short reverb, and pitch-bend for performance.

Source: [Oscillator Syncing in Thor (Patch Design in Thor)](https://www.youtube.com/watch?v=C_d3SCz2u-c)

1. Init two oscillators. Enable hard sync so each time oscillator 1 completes a cycle it resets oscillator 2's phase. Raise amp-envelope sustain to full.
2. Mute/hear only the slave for clarity. Changing master octave changes perceived pitch even when only the slave is routed; changing slave pitch changes timbre, not the fundamental.
3. Set slave about one octave below master. Route mod envelope to slave pitch at nearly full amount (~94%). Give the mod envelope a little attack, fairly long decay, and release near zero. Bypass bright-cutting filters for a raw sync tone.
4. Add tempo-synced delay (transcript example: dotted/3+16th feel) with low dry/wet, set pitch-wheel range to ±12 st, and a short digital reverb at very low mix for space.
5. Perform with pitch-bend automation (full-range slides) and optional reverb dry/wet rides for breakdown/build gestures.

Batch: `2026-10-09-morning-hunt` · transcript: YouTube-provided (Show transcript)
