# Struck-string physical-model synth controls that differ from subtractive synthesis: brightness set before the strike (not a filter), frequency-dependent decay (cutoff + slope) instead of sustain, strike point, harmonicity, three-string unison, and mallet-bounce retriggers at different note values per layer for sequenced polyrhythmic patches

Goal: Design pads, basses and keys on a struck/plucked physical model and know which controls behave unlike a subtractive synth. Plucking brightness changes a sine-like tone into a saw-like one but only at the strike: lowering it while a note rings does nothing, so put a real filter after the model for sweeps. There is no sustain: decay and release plus a decay cutoff and slope define how partials above the cutoff die faster (low cutoff + high slope = more decay). Strike point acts like the pick position; harmonicity moves the tone from harmonic to inharmonic (steel-drum-like with more bloom); unison width detunes the three strings per note; smear softens transients. Mallet bounce makes a held note re-strike itself; stacking layers with different bounce values (dotted half, quarter, eight beats in the demo) gives sequenced, polyrhythmic patterns without a sequencer. Delta beyond our modal-partial skill: decay slope, pre-strike brightness and mallet-bounce layering.

Source: [Syngular: Pianoteq's New Physically Modeled Synth // Walkthrough & Demo](https://www.youtube.com/watch?v=B3n9GOT0Q9A)

1. Start from a sine-like init voice. Raise plucking/strike brightness to move toward a bright, saw-like tone. Test that turning it down while a note rings does not change that note.
2. Edit the harmonic profile (raise some partials, lower others) for a new basic colour, and set unison width to detune the three strings per note for synth-style thickness.
3. Shape length: fast attack for keys or slower for pads; decay and release for ring time. Set the decay cutoff and slope: partials above the cutoff die faster as slope rises (low cutoff + high slope = shortest, darkest tail).
4. Set strike point (like pick position) and harmonicity (harmonic → inharmonic). With higher brightness and more bloom, inharmonic settings give steel-drum-like tones. Use smear to soften transients.
5. Enable mallet bounce so a held note re-strikes; adjust bounce rate and decay over time.
6. Build a sequenced patch with 2–3 layers and different bounce note values (e.g. dotted half, quarter, 8 beats). Turning off bounce on one layer will not stop the pattern while the other layers still bounce.
7. Map mod wheel → LFO rate, vibrato and tremolo depth. Finish with EQ and effects (chorus, phaser, delay, compression) and a post filter if you need cutoff sweeps.

Batch: `2026-10-20-morning-hunt` · transcript: YouTube-provided (Show transcript) · Product walkthrough with affiliate mention; licence and preset-tour content dropped.
