# Four-source morph engine: an XY/linear crossfade (centre = all four mixed, corners = one source) versus true parameter morphing of analysed (additive + spectral) sources, where the centre is a composite sound, with separate morph positions per element (additive, spectral, pitch, formant, analysed envelope), each driven by its own LFO type

Goal: Build evolving hybrid textures from four contrasting sources and know the difference between crossfading and morphing. Crossfade mode only mixes the four sources by an XY point (centre = all four at once, a corner = that source alone) or along X only (A-B, B-C, C-D). Parameter morph needs analysed sources (additive + spectral resynthesis of imported samples, not virtual-analog saws) at a similar pitch; after time alignment, the centre point produces a composite of all four, not a mix. Morph can be split per element: additive partials, spectral processing, pitch, formant and the analysed amplitude envelope of each sample (not the AHDSR), each with its own position. Give each element a different LFO (slow smooth, very fast, stepped) with depth raised, keep a manual centre point, and add reverb. For Polyrhythm Studio: four analysed partial sets interpolated per element by independent control lanes.

Source: [Logic Pro Advanced Tutorial : Morphing with Alchemy](https://www.youtube.com/watch?v=HXKz89TIlJI)

1. Init a patch, enable four sources with different waveforms and slightly different tuning, and choose XY crossfade. Move the XY point: centre plays all four, each corner plays one; try linear crossfade (X only: A-B, B-C, C-D). Optionally put a complex LFO on the XY point.
2. Re-init and import four contrasting sustained samples (drone, ghostly texture, atmospheric event, sustained vocal) as additive + spectral sources at similar pitch; wait for time alignment after each import.
3. Switch to morph XY with all elements linked and play a note; move between A, B, C, D and the centre.
4. Keep auto-align on; try fixed pitch off for a smoother morph and back on if the pitch wanders too much.
5. Split by element: reset all element points to centre, then move only the additive point; then spectral, pitch, formant and envelope (the samples' analysed envelopes, not the AHDSR). Per source, randomise morphable additive knobs, enable a spectral processor (e.g. metallize) on some, and shift formant settings so the sources differ.
6. Try morph linear: X only between A and B, C and D, or across all four.
7. Return to morph XY and assign a different LFO to each element point: slow smooth on additive, very fast on spectral, stepped on formant, smooth on another; raise each depth. Keep moving the centre manually. Add reverb on the whole patch.

Batch: `2026-10-22-morning-hunt` · transcript: YouTube-provided (Show transcript) · DAW synth walkthrough; factory sample names used only as examples of source types, not reproduced.
