# Stack granular processors to freeze any short sound into infinite sustain

Goal: Turn a short, gappy source into an endless sustained texture: run multi-band or multi-instance granular with linked bands, mild pitch/pan/delay randomization, one voice per band; stack the same granular chain ~4× with independent randomization so gaps fill; follow with upward dynamics (OTT-style), high-pass to stop low buildup, slow random EQ/filter motion, optional diffused 100% wet delay for smear, limiter, and a mono fold-down check.

Source: [Sound Design Trick - Creating Sustained Textures with Granular FX](https://www.youtube.com/watch?v=dxWCEDePgaw)

1. Start from a short source with silence gaps. Insert a granular processor; prefer a dense multi-band or 'schizophrenia-like' starting point, link bands, reduce pitch variation slightly, keep light rand on pitch/pan/delay, ~one voice per band.
2. Stack the same granular treatment about four times in series or parallel. Independent randomization + slowly moving band limits across instances fills holes into a complex continuous sustain.
3. Add upward compression/OTT-style processing to lift grain detail, then high-pass — sustained stacks often accumulate unwanted low end.
4. Animate tone: slow random modulation on a few EQ/filter bands (gentle boosts/cuts, light phasing at low mix, optional talking low-pass on the highs). Keep modulation subtle so it does not read as a phaser solo.
5. Optional smear path: 100% wet diffused delay (modulated delay time) when you want less discrete echoes and more smooth wash. Finish with a limiter to restore level.
6. Sum to mono and confirm the bed still works (point-source playback). Apply the same chain to non-synth sources (pebbles, debris) to verify generality.

Batch: `2026-10-12-morning-hunt` · transcript: YouTube-provided (Show transcript)
