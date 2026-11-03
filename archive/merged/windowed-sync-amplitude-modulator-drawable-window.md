# Windowed sync via amplitude window (sine or drawable) on a phase-synced oscillator

Goal: Rebuild Serum-style windowed sync (and half-window variants) portably: hard-sync a slave oscillator from an external phase, then multiply its amplitude by a same-rate window oscillator (sine shifted ~50% phase, or a drawable Hof/custom curve) so period start/end are forced to zero crossings — removing sync clicks when sync intensity is modulated — beyond the decaying-sine CZ resonance window already covered.

Source: [Windowed Sync in the Grid](https://www.youtube.com/watch?v=g0QRn65Mwwc)

1. Demo plain hard sync: feed a slave osc from an external phase with sync so raising sync amount packs more of the waveform in from the left and the cycle hard-jumps back to zero at the window end. Scope the discontinuity.
2. State the windowed-sync goal: force amplitude to zero at the beginning and end of each master period so the reset lands on a soft zero-crossing. Half-window is the same idea with a steeper decline at the ends.
3. Build the slave: wavetable/osc with internal phase off, driven by an external phase module that has a sync input from the master. Confirm the same crackle on modulation before windowing.
4. Duplicate the oscillator as a sine window source. Disconnect it from the sync output and feed it from the phase (not sync) tap so the window runs at the master period. Route the sine into an amplitude/level modulator on the slave.
5. Align phases: shift the window oscillator phase by about 50% so the zero of the window lines up with the sync reset (matching Serum-style windowed sync). Compare scope to the unwindowed sync.
6. Optional half-window / custom shapes: replace the sine with a drawable oscillator (or curve) that falls steeper at the ends (Hof-like) or any unorthodox amplitude curve — Bitwig Scrawl-style freedom. Keep window rate locked to the master phase.
7. Modulate sync amount with an LFO (saw or square work well for demo). Try bending/warping the slave and lighter waves (sine) when using aggressive FM-like mods. Keep the amplitude window engaged while sync moves.

Batch: `2026-10-12-morning-hunt` · transcript: YouTube-provided (Show transcript)
