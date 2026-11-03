# Eerie, dreamy pad from a basic paraphonic supersaw patch plus outboard-style effects: cutoff key-tracked about 50%, long attack and release, two slow low-resonance phasers in stereo mode, about 0.5 s modulated delay, a second about 1.5 s ping-pong delay with a little more feedback and lower mix, a reverb with dwell at zero, then a looping (cyclic) envelope on cutoff whose rise/fall times an LFO slowly varies

Goal: Turn an init-patch supersaw into a wide, whooshing, dreamy pad using mainly a phaser-delay-reverb chain. The effects do most of the work: slow stereo phasing for the whoosh, two delay lengths for stereo spread, and an irregular filter breath from a cycling envelope whose speed drifts. Fills the phaser-pad gap with a non-high-pass recipe.

Source: [Synth + Pedal Sound Design Tutorial - Arturia MicroFreak and Zoom MS-70CDR](https://www.youtube.com/watch?v=XRCwoFjZFMc)

1. Start from an init patch, switch to paraphonic (up to 4 notes) and choose the supersaw oscillator at default settings.
2. Set filter cutoff and resonance by ear, then key-track cutoff by about 50% so higher notes open the filter. Raise attack and release for a pad envelope (shorten them temporarily while designing effects).
3. Add two phasers (dual phaser) for the whoosh. Reduce the rates for slow movement, lower resonance so the effect is subtle, turn on stereo mode and reduce depth a little.
4. Add a modulated delay at default (about half a second), then a second delay of about 1.5 s with slightly more feedback, lower mix, in ping-pong mode.
5. Add a lush (particle-style) reverb with dwell set to zero, other settings default.
6. Automate cutoff with a cyclic (looping rise/fall) envelope, and change rise and fall times to set its rate.
7. Route a slow LFO to the cyclic envelope's rise and fall times, and also directly to cutoff, so the breathing speed keeps changing.
8. Play chords, adjusting resonance, cutoff and cyclic-envelope amount live.

Batch: `2026-10-30-morning-hunt` · transcript: YouTube-provided (Show transcript)
