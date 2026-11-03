# Stereo delay motion: ping-pong, dual-parallel, two-tap, cross-feedback

Goal: Build musical stereo delay motion for synths/pads: tempo-synced ping-pong (feedback ~40–50%, wet ~15–25%, repeats band-limited ~100 Hz–3 kHz, optional saturation, even or offset L/R), dual-parallel (independent L/R subdivisions such as dotted-eighth vs quarter, self-feedback then cross-feedback, optional modulation/diffusion for reverb-like density), two-tap tape-head (long tap feeds short; short has no self/cross feedback), ping-pong recognized as a 2:1 two-tap, LFO panning delay and feedback-phase invert; prefer send routing and automate for evolving motion.

Sources (merged 2026-10-03):
- https://www.youtube.com/watch?v=GcZILAUGEyU (from `ping-pong-delay-filtered-motion-recipe`)
- https://www.youtube.com/watch?v=eSXZWFjCeiY (from `dual-delay-parallel-two-tap-crossfeedback`)

1. Pick the delay topology for the job: ping-pong bounce (discreet L↔R, steps 2–5), dual-parallel with optional cross-feedback (dense poly-rhythmic space, steps 6–9), two-tap tape-head style (cleaner bounce, steps 10–11), or LFO panning delay (step 12). Then route and animate it (steps 13–14).
2. Ping-pong: Enable ping-pong / stereo bounce delay. Set delay time to a musical subdivision (quarter or eighth) so repeats lock to groove.
3. Ping-pong: Set feedback ~40–50% so repeats fade without clutter; wet/dry ~15–25% as a starting mix.
4. Ping-pong: Filter the delayed signal: cut lows below ~100 Hz and highs above ~3 kHz to avoid mud/harshness. Optionally add tiny saturation/distortion on wet for warmth.
5. Ping-pong: Maximize stereo width of the bounce when desired; link L/R times for even bounce, or slightly offset L vs R times for a more complex image.
6. Start dual-parallel: set different tempo subdivisions per channel (e.g. dotted-eighth left, quarter right) so the shorter and longer echoes interact as a delay poly-rhythm (classic 3-against-4 feel with those two).
7. Set self-feedback per channel (example starting points from transcript: ~45% left into left, ~30% right into right) with no cross-feedback yet; hear space/energy without stacked interaction.
8. Add cross-feedback (right→left, then optionally left→right with complementary amounts) to stack interacting delays and fill the stereo field toward a faux-reverb density.
9. Optional lush pad/ambient path: raise delay modulation depth (~20% in source demo) and diffusion (~50%) so dual-delay + cross-feedback reads more like reverb-space.
10. Build two-tap (multi-head tape style): keep long + short times, but only the longer delay self-feeds and also feeds the shorter delay; give the shorter delay zero self-feedback and zero cross-feedback so taps never line up like dual-parallel — cleaner stereo around a center dry signal.
11. Recognize ping-pong as a two-tap with ~2:1 time ratio (e.g. 400 ms / 800 ms) and the same long→short + long self-feedback topology; prefer dedicated ping-pong mode when available. Contrast with dual-parallel at 2:1 (short and long land together, soft-panned long tap).
12. Optional: panning delay uses an LFO to move repeats (syncable for ping-pong-like motion or offset rates). Feedback-phase invert (negative feedback phase) flips polarity each regeneration to enhance spatial width on cross-feedback designs. Keep mix lower in practice; use ducking/EQ on wet for dense sources.
13. Prefer send routing so you can EQ/compress the wet alone before blend; if insert, mind wet/dry carefully.
14. Automate or modulate feedback, delay time, or filter cutoff across sections; optional subtle chorus/flanger on delayed signal only. Use on synths (also vocals/guitars/perc) especially in sparse/breakdown sections.

Replaces: `ping-pong-delay-filtered-motion-recipe`, `dual-delay-parallel-two-tap-crossfeedback`

MCP: `skill://stereo-delay-pingpong-dual-parallel-two-tap`
