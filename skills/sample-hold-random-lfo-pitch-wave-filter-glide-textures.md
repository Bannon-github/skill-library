# Sample-and-hold / random-glide LFO textures: random steps on pitch, wave position and filter, random glide squelch, user-drawn step LFO

Goal: Use a random-hold (sample-and-hold) LFO as a sound-design engine: random stepped pitch on a saw (sci-fi computer with reverb/delay), the same LFO on wave/wavetable tuning and filter cutoff/resonance, a random-glide shape with legato + glide for squelchy psy-style lines, mod-wheel-scaled S&H on volume, and a user-defined 8-step (steps or lines) LFO as a repeatable pseudo-S&H for bass/leads — then bounce and chop the audio into SFX. Delta beyond general LFO routing and random pitch drift in pad skills.

Source: [Zebra 2 - Using LFO`s Random Features (Sample & Hold) - How To Tutorial](https://www.youtube.com/watch?v=IiWPL_v8Eqk)

1. On a basic saw oscillator, set LFO2 shape to random-hold (sample and hold) and route LFO2 → oscillator tune.
2. Add reverb and delay (adjust delay times) for the old sci-fi computer effect.
3. Swap to a stranger oscillator wave; keep the pitch depth low so it stays usable (even as a weird bassline).
4. Route the same LFO2 to the wave/wavetable position (with the wave set mid) as well as tune; add lots of delay.
5. Add a filter and route the S&H LFO to cutoff and resonance — be careful with high resonance.
6. Switch LFO shape to random glide; set legato mode and turn glide up for squelchy random glides (psytrance-style). Note long sustained notes vs retriggered behaviour; speed the LFO up as needed.
7. In the mod matrix, target voice volume with LFO2 scaled by the mod wheel.
8. Use a user-defined LFO with 8 steps as a predetermined S&H pattern (it repeats, so not truly random) for basslines or leads; switch steps → lines so glide ramps between values.
9. Bounce results to audio and chop short sections for SFX and quirky elements.

Batch: `2026-10-13-morning-hunt` · transcript: YouTube-provided (Show transcript)
