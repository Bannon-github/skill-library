# Eight-layer Euclidean pattern generator with two modes: drums (each layer = one MIDI drum note) and melody (each layer = a different note of a chosen scale and root, so stacked layers form in-key chords); per-layer steps, pulses, rotation, velocity and gate, a drift action that nudges each layer's pulses by ±1, layer or global randomise that never changes note assignment, and scale/root changes that keep the rhythm

Goal: Write in-key polyrhythmic melodies and grooves by stacking up to eight Euclidean layers. Each layer has steps (pattern length), pulses (hits spread as evenly as possible), rotation (offset, which shifts layers against each other), velocity and gate (note length). In drum mode each layer triggers its own drum note; in melody mode each layer is assigned a different note from a chosen scale and root, so layers of different lengths interlock into melodies and coinciding hits make chords, always in key. Generate the result into a clip, add layers one at a time, use drift to randomly move each active layer's pulse count up or down by one, and randomise a layer or everything except the note assignment. Keep a rhythm you like and change scale (e.g. to Phrygian) or root afterwards. Shorten gate if notes are too long. For Polyrhythm Studio: one Euclidean lane per scale degree with independent lengths.

Source: [Euclidean Weaver v1.2.0 | Generate Euclidean Rhythms and Melodies in Bitwig Studio](https://www.youtube.com/watch?v=UchJGizLiLM)

1. Choose drum mode and assign layers to drum notes (kick, snare, closed hat, etc.). Enable two layers, set steps/pulses/rotation, and generate.
2. Add layers one at a time (e.g. closed hat, crash), set each layer's velocity and gate, and regenerate.
3. Change a layer's rotation or pulses (e.g. move the snare), or press randomise for one layer; use drift to move every active layer's pulse count by ±1.
4. Switch to melody mode, choose scale and root. Each layer now plays a different scale note; enable several layers with different step lengths.
5. Shorten gate if notes overlap too much; randomise all (notes stay fixed) until a rhythm works.
6. Keep the rhythm and change the scale or root (e.g. to Phrygian) and regenerate.

Batch: `2026-10-21-morning-hunt` · transcript: YouTube-provided (Show transcript) · Script promo; Patreon/download and preset browsing dropped.
