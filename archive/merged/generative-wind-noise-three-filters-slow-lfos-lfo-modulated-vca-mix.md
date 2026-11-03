# Generative 'noodle' wind with no MIDI: one noise source into three parallel filters (slow-swept LP, high resonant BP whistle, mid SVF BP), slightly different free-running sine LFOs with light LFO cross-mod, and an LFO-modulated three-VCA mixer

Goal: Patch a self-running wind ambience bed that moves without MIDI. Split one white-noise source into three filters: a low-pass swept by a very slow sine LFO (dark rumble that brightens and darkens); a band-pass set very high with resonance pulled well up but short of self-oscillation (resonant whistle); and a mellower state-variable band-pass in the middle. Give each filter its own very slow free-running sine LFO at slightly different rates, and let one LFO lightly modulate another. Mix through a three-channel mixer whose per-channel VCA inputs are driven by three more slow sine LFOs, centred so the layers drift in and out without ever disappearing. Finish with a bracket EQ to tame and a big wash reverb. For a generative noise layer under cinematic pads, this differs from our triple-bandpass pad, which filters a played saw, and from the recorded-whoosh skill.

Source: [DevOcean Modular - Create A Wind Noodle Patch From Scratch #modularsynth  #sounddesign  #synthesiser](https://www.youtube.com/watch?v=_6mEzWHoxKo)

1. Start a patch with output, a gain mixer and an EQ (disconnected). Add a white-noise oscillator at low volume, with a little extra gain on the noise module.
2. Channel 1: noise → low-pass, fairly closed. Add a very slow free-running sine LFO (no MIDI, no retrigger) to its cutoff, slowed further if needed.
3. Channel 2: same noise → band-pass (RBJ-type) set very high, resonance pulled way up but not to a tone, to make a resonating whistle. Add its own slow LFO.
4. Channel 3: same noise → state-variable band-pass in the middle range, a mellower flavour, with its own slow LFO.
5. Make all three LFO rates slightly different, still very slow, and let one LFO modulate another 'just a touch'.
6. Mix the three channels in a 3-input mixer with per-channel modulation inputs (each channel = a VCA), in attenuation mode, bipolar depth set in the correct direction. Drive each modulation input with its own slow sine LFO at a different speed, positioned in the middle so channels go in and out but don't disappear.
7. Add a bracket (low/high-cut) EQ to tame the bed, then a big wash reverb. Save it as a patch, then explore by changing LFO rates and shapes on both filters and mixers.

Batch: `2026-10-15-morning-hunt` · transcript: YouTube-provided (Show transcript) · Modular app walkthrough; route.py said COVERED but hand-check found no generative noise/wind bed skill. Factory patch names omitted.
