# Casio-style phase distortion: piecewise phase warp of a cosine into a saw (DCW node)

Goal: Implement Casio CZ-style phase distortion so a cosine (or sine) table becomes a variable saw by warping the 0→1 read phase with a two-slope piecewise line (breakpoint node at half-amplitude), then modulate that node for filter-like brightness without a resonant filter.

Source: [GroovyDSP: Introduction to Phase Distortion Synthesis](https://www.youtube.com/watch?v=EW12RYc7QRA)

1. Treat the oscillator as: play a cosine (or sine) table by reading it with a linear phase ramp 0→1 once per note cycle. At warp=0 the output must equal the untouched cosine.
2. Define a breakpoint node that always sits at half amplitude on the warped phase (y=0.5) but can slide left on the x-axis to position x1 (how far 'cocked back'). More cock-back = sharper transition from cosine toward saw.
3. Build the warped phase with two line equations meeting at (x1, 0.5): m1 = 0.5 / x1 for the fast first segment (y = m1 * x); m2 = 0.5 / (1 - x1) and b2 = 1 - m2 for the slow second segment (y = m2 * x + b2). If phase < x1 use the first; else use the second.
4. Look up cos(2π * warped_phase) [or your cosine table at warped_phase]. Do not advance phase at two different increments across the threshold — that one missed sample at the knee throws the pitch out of tune when x1 moves.
5. Listen while moving x1: near 0.5 the tone is closer to a sinusoid; pulled far left toward 0 it approaches a near-pure saw. Route an envelope or LFO to x1 for filter-like sweeps without filter math.
6. Optional extensions (same warper): run the warper twice per cycle for other CZ shapes; feed a rich wave (e.g. square) through the same shaper to get pulse-width/symmetry-style squeezing of the first half vs elongation of the second.

Batch: `2026-10-09-morning-hunt` · transcript: YouTube-provided (Show transcript)
