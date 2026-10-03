# Unison voicing: odd vs even voice counts, detune/blend/width, clean supersaw

Goal: Set unison deliberately and build mix-ready supersaws: odd voice counts keep a centered in-tune voice for mono-compatible front-of-mix bass/leads/pads, even counts leave a center gap for ultra-wide off-center leads; keep detune/blend moderate; for supersaws use simple saw frames (not complex WT sweeps), ~6–12 voices, optional quieter Osc B, centered sub an octave down and quiet noise, EQ→compress→delay→reverb, subtle warp, and global unison width ~50% plus sparing stack modes for chord phase correlation.

Sources (merged 2026-10-03):
- https://www.youtube.com/watch?v=am6KBGUVtXE (from `odd-even-unison-center-vs-width`)
- https://www.youtube.com/watch?v=KnbAOrM62Ks (from `supersaw-clean-unison-detune-width`)

1. Start from 1 voice, then set 2 voices: expect one left and one right with a center gap; default detune often sounds harsh—lower detune.
2. Switch to 3 (odd) voices: confirm a center voice appears; with blend lowered you hear more of that center while keeping similar detune.
3. Compare 4 (even) vs 5 (odd) at similar detune: higher even counts can sound more detuned/wide; very high odd counts (e.g. ~15) pack many voices near center so the patch can sound *less* detuned than a mid even count.
4. For reese/detuned saw bass or other front-and-present mix parts, prefer odd voice counts for mono compatibility (center represented).
5. For an uber-wide lead you will pan off-center, even counts (2/4/…) with blend favoring outer voices are acceptable.
6. Example starting detune for chord/lead work: modest (~0.16 in the video’s demo); reset blend to default then adjust; always A/B odd vs even in context.
7. Supersaw: Load a simple saw (or rounded/noisy saw variant), not a multi-frame complex WT you plan to sweep aggressively.
8. Supersaw (apply the odd/even rule above when choosing the count): Set unison ~6–12 (example ~10); set detune and blend near mid — extreme detune+blend is for FX, not clean chords.
9. Optional Osc B: fewer unison voices, pitch ±octaves, lower level to thicken without doubling chaos.
10. Optional centered saw sub one octave down (no unison) for mono mid-weight; quiet unique noise sample for texture.
11. FX order example: EQ (cut lows, lift highs) → compression → ping-pong delay → reverb last; optional light hyper/dimension detune on the bus (can widen even the sub).
12. Subtle warp (e.g. bend+/−) via envelope/LFO for 3D motion — keep amounts small on supersaws.
13. Global unison: reduce width (~50%) for better chord phase correlation; try stack modes (super, fifths, center−2, octave) sparingly; warp-offset per voice only if warp is intentional.

Replaces: `odd-even-unison-center-vs-width`, `supersaw-clean-unison-detune-width`

MCP: `skill://unison-odd-even-detune-width-clean-supersaw`
