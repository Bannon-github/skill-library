# One-knob reverb → drone instrument: macro range 0–99 = wet/dry, 100–110 = muted dead zone, 110–127 = freeze + overdub drone with LFO speed, plus LFO-modulated EQ/width, unsynced auto-filter, limiter and randomizable algorithm

Goal: Wrap an algorithmic reverb in a macro rack that doubles as an ambient drone generator: one 'drone' macro maps wet/dry over its lower range, a 100–110 dead zone that mutes the rack (utility gain/off) to avoid the loud boom when leaving freeze, and from 110 up engages freeze-with-overdub so new notes add into the held reverb while the same macro sets a jittered, shaped LFO from fastest (at 110) to ~0.1 Hz (at the top); that LFO modulates mid-EQ frequency (+30), mid gain (−25), low edge (+15), high edge (−20) and stereo width (+15); a parallel-moving auto filter (~1.5 kHz, 10% res, ~5% drive, its own time-mode LFO at 10%) stays out of sync; a limiter guards overdub build-up; other reverb parameters (algorithm, decay, size, per-algorithm params) are randomizable, EQ/pre-delay/drone excluded, and good results saved as variations.

Source: [Create Ambient Drones in Ableton Live 12.2 (Hybrid Reverb Tutorial)](https://www.youtube.com/watch?v=0NXGraBGWvE)

1. Build a rack: algorithmic reverb (convolution off) → LFO device → auto filter → limiter → utility (gain). Expose 16 macros: algorithm, decay, size, params 1–5 (map each algorithm's own 5 controls to the same macros), low/mid/high EQ, mid gain, vintage, width, pre-delay, drone.
2. Reverb EQ: band 1 and band 4 as steep (48 dB/oct) edge filters mapped to 'low EQ' and 'high EQ'; bands 2+3 frequencies to 'mid EQ', their gains mapped inversely to 'mid gain'.
3. Map the 'drone' macro: dry/wet over 0–99; utility on/off+gain so 100–110 is silent; freeze ('infinite') and overdub ('add') switch on at ≥110; LFO on/off, rate (fast at 110 → ~0.1 Hz at max), jitter and wave shape (≈75%→20%) across 110–127; auto-filter on and its LFO time also on this range.
4. LFO device targets with depths: mid-EQ frequency 30, mid gain −25, low EQ 15, high EQ −20, width 15.
5. Auto filter: frequency ~1500 Hz, resonance 10%, MS-type model, drive 5%, clip on; its own LFO in time mode at 10% amount, deliberately not synced to the rack LFO.
6. Play: below 100 use as a normal reverb; above 110 play a note or two and let them overdub into the frozen space; adjust mid/high/low EQ in real time if boomy or trebly.
7. Randomize the rack (exclude EQ, pre-delay and drone macros) to audition reverb spaces; save good results as rack variations and re-save the rack preset.

Batch: `2026-10-14-morning-hunt` · transcript: YouTube-provided (Show transcript)
