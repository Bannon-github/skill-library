# FM/operator-stack uplifter with long pitch envelope and synced noise swell

Goal: Build a dense FM uplifter: stack multiple operators (low formant carrier, self-feedback raspy modulators, bright triangles/squares into the output, chord-ish ratios distorting a mid operator), mono with light voice pan, bit of digital crush, opposing looped envelopes (slow reverse swell vs stabby), a tempo-synced pitch envelope rising over ~8 bars, and a noise operator whose amp/FM depth shares that same rising envelope, finished with EQ and reverb.

Source: [FM8 - FX Sounds - pt 1 - Uplifter - How To Tutorial](https://www.youtube.com/watch?v=G4Tc59aAeoE)

1. Carrier/low layer: one operator to output at full level, ratio ~0.25, formant-ish wave (transcript: 3rd formant) for a low body.
2. Add a raspy modulator into that carrier (~28 depth) with self-feedback on both (~5 on the mod, ~32 on the carrier); set mod ratio ~0.5 with a higher formant wave (transcript: 8th formant).
3. Bright layers to output: triangle at ratio 4 and a square-ish (1+3+5) at ratio 1, each ~88 level, with some self-feedback on the triangle (~16).
4. Distort a mid operator with two further ops (triangle at ratio ~1.25 into it ~54; saw-ish 1+2+3 at ratio 0.25 into that modulator) for a slight chord/cluster rasp.
5. Master: monophonic, 2 voices, detune off, light pan (~25–26%) between voices; add mild bit-crush/digital (~65) for FX character.
6. Envelopes: tempo-sync; give some operators a slow reverse/fade-in looped sustain shape (e.g. over 3/16) and others a stabby attack with sustain loop so layers move against each other.
7. Pitch envelope: tempo-sync a long rising sustain envelope across ~8 bars (~31–32/4), amount ~54, slightly curved for a smoother bend; hold MIDI at a sustained note (e.g. C3).
8. Noise operator to output (~58) with amp up, bright cutoff, mild resonance (~55–57); FM-noise into several tonal ops (e.g. ~50/30/16). Save/load the same rising pitch envelope onto the noise amp so noise and its FM distortion swell with the rise. EQ low-mids/highs; reverb ~33–34% wet.

Batch: `2026-10-09-morning-hunt` · transcript: YouTube-provided (Show transcript)
