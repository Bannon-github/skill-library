# traveler-walkthrough-wavetable-morph-filter-motion

Goal: Create an evolving hybrid patch using a wavetable oscillator (Osc3 role), optional duo-stack/detune/stereo spread, and animated WT position + filter cutoff.

Source: https://www.youtube.com/watch?v=IU76c2Cygs4

1. Osc3 role: switch from analog waveforms to wavetable mode. Load an original/freely available WT (do not import Traveler proprietary tables).
2. Optional: enable 2-voice stack, detune, and stereo spread on the WT osc for width.
3. Optional drone mode: disconnect Osc3 from keyboard for a fixed-pitch layer, or use it as an extra LFO-rate modulator.
4. Modulate wavetable position from LFO or Control Track; keep depth subtle for evolving texture rather than obvious sweeps unless desired.
5. Stereo filter: ladder model (6–24 dB) or NJM-style; add HP that can link to primary cutoff for band-pass motion. Modulate cutoff from filter envelope and/or LFO.
6. Mixer: balance WT vs analog oscs; add noise (white/pink) sparingly; light drive into filter.

MCP: `skill://traveler-walkthrough-wavetable-morph-filter-motion`
