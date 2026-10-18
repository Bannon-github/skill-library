# Dual-layer opposite-rotation vector morph pad with filter-drive LFO

Goal: Build a lush evolving pad from two vector (4-corner XY) oscillators: same four portable shapes on both layers, layer B pitched up (~+12–13 st / +24–25 st on some corners for air), XY indexes modulated by one slow synced LFO but with opposite rotation directions per layer, long pad amp attack/release, then a mild driven low-pass whose drive is breathed by a second slow LFO, plus light ensemble and master reverb.

Source: [Synthmaster Tutorial - Vector oscillator "monster pad"](https://www.youtube.com/watch?v=6aRgJoBxk4g)

1. Create vector oscillator A with four contrasting portable waves in the corners; set pitch display to semitones. Keep all four corners at the same base pitch for a coherent chord tone.
2. Park the XY near a musically useful corner (tutorial favored a top-side start). Assign one slow synced sine LFO (~4 bars) to both X and Y indexes with opposite polarities/amounts so the path orbits (left-right on one axis, up-down on the other) instead of only sliding on a diagonal.
3. Copy oscillator A settings to oscillator/layer B. Pitch two corners ~+13 st (octave-ish) and another ~+25 st (two octaves) for depth/air while leaving structural corners nearer the base if needed. Invert the XY modulation directions so B orbits the opposite way (clockwise vs anticlockwise) from the same LFO.
4. Shared pad amp envelope on both parts: long attack (pull attack curve back), decay ~9 o'clock, sustain as-is, release ~3 o'clock (release doubles as a soft tail). Lengthen attack further if the swell should feel glacial.
5. One analog-style low-pass on the layer: moderate cutoff (~12–1 o'clock), no resonance, standard key track, tiny static drive. Modulate filter drive from a second synced LFO (triangle, different phase/rate than the vector LFO) with only a small positive depth so drive washes in gently.
6. Optional: second envelope → cutoff with some decay and sustain at zero for a slow open that uses decay/release. Insert light ensemble on one FX slot; send master reverb (aftertouch→reverb amount is optional). Ride master volume down whenever drive/distortion is added.

Batch: `2026-10-12-morning-hunt` · transcript: YouTube-provided (Show transcript)
