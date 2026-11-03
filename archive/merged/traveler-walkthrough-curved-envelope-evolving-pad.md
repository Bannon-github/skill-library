# traveler-walkthrough-curved-envelope-evolving-pad

Goal: Design a long-evolving cinematic pad using multi-stage envelopes with adjustable curve handles, up to ~20s stages, optional breakpoint/slope expansion, and a modulation envelope that can start from alt control (e.g. sustain pedal) instead of note-on.

Source: https://www.youtube.com/watch?v=IU76c2Cygs4

1. Set three envelopes: filter, VCA, and modulation. Open the on-screen envelope editor and drag curve handles on time stages.
2. Use long time stages (up to ~20s each) for cinematic bloom. Expand envelope to add breakpoint + slope stages (ADBSSR-style) when you need a mid-bloom reshape.
3. Route filter envelope to stereo LPF cutoff with moderate amount; VCA envelope for amplitude; mod envelope to WT position, pan, or secondary cutoff.
4. Optional alt-control on mod envelope: start envelope from sustain pedal (or other mod-bus source) instead of key press for expressive delayed motion.
5. LFOs: choose from varied shapes including unipolar and slew/random; key-sync or free; tempo-sync optional; dedicate pitch or filter vibrato with fade-in on LFO1/2.
6. Finish with soft EQ, light chorus, long space/hall reverb (space algo up to very long tails). Keep limiter available as safety for dynamic patches.

MCP: `skill://traveler-walkthrough-curved-envelope-evolving-pad`
