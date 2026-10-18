# Complex-oscillator voice: bidirectional cross-FM, sync + pitch-follow slew between two VCOs, osc-modulated wavefolder into an S&H-swept self-resonant filter

Goal: Patch a West-Coast complex-oscillator voice from two VCOs: hard-wire exponential FM in both directions (osc1→osc2 and osc2→osc1) and dial sweet spots with both active, use soft/hard sync on osc1, add a 'follow' (osc1 slews to track osc2's v/oct at a set follow rate) for gliding harmonies, take osc2 through a wavefolder whose shape/angle are modulated by osc1 (mod bus), then split outputs: saw → multi-filter + chorus as bass, square → arpeggio with tiny vibrato into linear FM, folded output → filter at full resonance swept by sample-and-hold, into a clocked stereo delay.

Source: [Make Noise DPO — The Ultimate Complex Oscillator?](https://www.youtube.com/watch?v=c8aQMp0vkRg)

1. Exponential FM osc1→osc2: raise the amount and listen; then osc2→osc1 likewise; then use both simultaneously and find sweet spots (a little delay helps hear it).
2. Osc1 options: soft sync (lock) or hard sync to osc2 with a richer waveform; or switch osc1 to LFO mode as an internal modulator.
3. Follow: send v/oct to osc2; set osc1 to follow osc2's pitch with a follow (slew) rate so osc1 glides after it; combine sync + follow, then move osc1's pitch to find harmonies/harmonics, or disable follow so osc1 drones on one note.
4. Wavefolder output: lower the sine outputs, listen to the folder; adjust shape and angle (symmetry); bring up the mod bus so osc1 modulates the folder.
5. Bass: osc1 saw sequenced separately → analog filter → stereo chorus.
6. Arp: osc2 square plays an arpeggiated sequence with a tiny vibrato into the linear FM input.
7. Resonant layer: folded output → filter with resonance fully up, cutoff modulated by sample-and-hold; blend in some FM on the folder.
8. Send everything through a clocked stereo delay; record — results are hard to recreate.

Batch: `2026-10-14-morning-hunt` · transcript: YouTube-provided (Show transcript)
