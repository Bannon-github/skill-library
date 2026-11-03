# Vector synthesis: XY-blend four oscillators with nested crossfades

Goal: Build classic vector synthesis portably: place four distinct oscillator shapes at the corners of an XY pad (bipolar −1…+1), nest three crossfade/blend stages driven by the X and Y axes so each corner is soloable and the center mixes all four, then add an amp envelope — a 2D morph that is not a 1D wavetable scan.

Source: [Vector Synthesis in Bitwig Grid with the Scrawl Oscillator](https://www.youtube.com/watch?v=SMB34GRgQWQ)

1. Instantiate four oscillators. Load contrasting shapes into the four corners (e.g. sine, saw, a complex drawable, an odd/noisy shape). Keep pitches unified unless you intentionally detune later.
2. Add an XY control set to bipolar mode so (0,0) is the center and each axis runs −1…+1 (unipolar XY only covers one quadrant and cannot reach all four corners).
3. First vertical blends: mix top-left with bottom-left using the Y axis (positive Y favors the upper osc, negative the lower). Separately mix top-right with bottom-right with the same Y.
4. Horizontal master blend: mix the left-column result with the right-column result using the X axis (wire X at full bipolar depth, e.g. ±50% into the blend if your modulator is bipolar).
5. Verify interior points: center should combine all four; edges should be two-osc mixes. Contrast with a 1D wavetable scan that cannot jump sideways between non-adjacent frames.
6. Finish with an ADSR (or similar) on the blended output level. Optionally LFO/automate X and Y slowly for evolving pads; keep mono compatibility in mind if later widening.

Batch: `2026-10-12-morning-hunt` · transcript: YouTube-provided (Show transcript)
