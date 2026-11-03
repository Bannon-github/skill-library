# Endless ambient texture from one looping MIDI clip: seeded random notes in a gap-free scale, per-note chance below 50%, randomised velocity/humanise, slow sine pad, scale-degree fifth chording and stereo/granular/reverb chain

Goal: Make a single looping MIDI clip never sound the same twice. Generate seeded random notes locked to a scale without half steps (major pentatonic; Dorian also liked), in a mid register (pitch range ~2–3) with long durations. Then lower each note's play chance below 50% (or below 30% for sparse, many-voice clips) and randomise chance, velocity and timing deviation. Play a soft sine pad (~1 s attack, ~6 s release, so sparse notes overlap), add a scale-aware chord effect (scale degree +4 = fifth on every triggered note), then stereo doubling, a parallel echo, a stereo pitch-loop/micro-delay, granular delay (spray up, frequency down) and a big long reverb. For Polyrhythm Studio-style generative scheduling: probability per note, not a fixed sequence.

Source: [The Secret to Endless Ambient Textures in Ableton Live](https://www.youtube.com/watch?v=U1t3ELd1LDI)

1. Create a looping MIDI clip and set its scale (e.g. C minor, then switch to major pentatonic or Dorian; scales without half steps suit generative work). Use fit-to-scale after any scale change.
2. Generate seeded random notes: set density, pitch register around 2–3 (mid range rather than 0–1), longer durations for smooth pad-like notes, and the number of voices.
3. Randomise velocities and add deviation/humanise so timing and dynamics wiggle off the grid.
4. Select all notes and set chance (play probability) to about 50%, then randomise it so some notes play ~90% and others ~15%. With many voices/density keep chance below 50% or even 30%. Re-apply after regenerating.
5. Sound: simple sine pad (second oscillator off), attack just over 1 s, release ~6 s, extra voices for overlaps.
6. Add a chord/interval effect before the synth in scale mode with a scale degree of 4 (perfect fifth), so every triggered note becomes a power-fifth.
7. Effects: stereo doubler, parallel echo, a stereo pitch-loop/micro-delay for randomised stereo, granular delay (raise spray, lower frequency) for glitchy texture, then a long-decay reverb.

Batch: `2026-10-15-morning-hunt` · transcript: YouTube-provided (Show transcript) · Patreon/subscribe CTA dropped. Host-specific generator UI mapped to generic per-note probability.
