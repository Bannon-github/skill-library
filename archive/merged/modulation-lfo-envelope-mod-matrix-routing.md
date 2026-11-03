# Modulation basics: LFO vs envelope, then mod-matrix source→destination routing

Goal: Use LFOs for cyclic motion (tremolo, vibrato, wobble, WT/PWM drift; audio-rate into AM/FM) and ADSR envelopes for note-triggered shapes (amp dynamics, filter envelope ±amount for pluck/wah), then route any source (LFO, envelope, mod wheel, key, pedal) through a modulation matrix to one or more destinations (pitch, cutoff, amp, pan, delay time/feedback/amount) with set amounts—auditing hard-to-hear routes on pitch first.

Sources (merged 2026-10-03):
- https://www.youtube.com/watch?v=UxGswh6XLto (from `lfo-envelope-motion-routing-basics`)
- https://www.youtube.com/watch?v=Xuu03lhSK7c (from `mod-matrix-source-destination-routing-basics`)

1. Treat LFO as a very slow oscillator (usually below hearing): set shape (sine/tri/square/saw/custom) and rate, then assign to a destination so the parameter follows the oscillation.
2. Classic LFO recipes: → amp = tremolo; → pitch = vibrato; → low-pass cutoff = wobble; → waveform/PWM/WT position = evolving source timbre. Tempo-sync for rhythmic motion or keep slow free-rate for subtle drift.
3. Raise LFO rate into audio range: amp mod → AM sidebands; pitch mod → FM-like spectra; very fast FX-param mod (e.g. phaser) can become a distortion/timbre effect.
4. If available, try LFO one-shot mode—shape plays once, behaving like an envelope.
5. Amp envelope ADSR: Attack = fade-in time; Decay = time to sustain; Sustain = held level (if sustain = max, decay has no effect); Release = fade-out after key-up. Percussive: attack+sustain low, length from decay (+ some release). Pad/violin-like: longer attack+release, sustain full.
6. Filter envelope: assign to cutoff with ±amount/depth. Positive amount opens from a low cutoff (plucky bass with short A, some D, no S, short R). Negative amount with high cutoff can wah downward; longer attack + positive amount opens wah; raise sustain to keep open while held.
7. Ensure amp envelope lets enough signal through to hear filter motion. Also try envelopes on PWM or wavetable position so the source evolves per note.
8. Mod matrix: Treat the mod matrix as deep synthesis: any controller source (self-running LFO/env or performer control like wheel/key/pedal) can move any available audible destination (pitch, cutoff, amp, vibrato rate, pan, delay params, …).
9. On an init/simple patch, create a route: choose source, choose destination, raise amount. Prefer starting with destination = oscillator pitch so the modulation shape is immediately audible.
10. Example performer control: mod wheel → filter cutoff. Lower cutoff, raise amount, move wheel; set wheel to max while trimming amount for the brightest intended ceiling. Add resonance/delay for musicality.
11. Retarget or add destinations: pan, volume, delay amount/regen/time, etc. Stack multiple routes so several parameters move together for evolving pads.
12. If a route is hard to hear on its real destination, temporarily assign that source to pitch to audit the shape, then reconnect to the intended destination with an appropriate amount.

Replaces: `lfo-envelope-motion-routing-basics`, `mod-matrix-source-destination-routing-basics`

MCP: `skill://modulation-lfo-envelope-mod-matrix-routing`
