# Widen a pad without phase smear: high-band pan LFO or hard-panned chord split

Goal: Widen a narrow pad without chorus/imager/spreader phase damage using one of two portable methods: (A) multiband-pan only the high band with a slow (bar) or 16th-note sine L/R swirl, keeping lows/mids centered and pulling amount down if motion distracts; or (B) duplicate synth+MIDI, mute alternating chord tones on each copy, and hard-pan L vs R so each side plays different notes of the same harmony—then confirm healthier correlation than chorus.

Sources (merged 2026-10-03):
- https://www.youtube.com/watch?v=zHqFoN3FTTI (from `highband-pan-lfo-pad-width-keep-lows`)
- https://www.youtube.com/watch?v=EZG7Pdh9gms (from `mono-compatible-chord-split-stereo-pad`)

1. Start from a good but narrow pad. Avoid broadband chorus/imager wideners (phasy/warbly, phase issues in lows/mids) and frequency stereo-spread (often not truly wide, can sound inside-out). Choose a method: A) high-band pan LFO on the same patch (steps 2–5), or B) interleaved chord split across two hard-panned layers (steps 6–9).
2. Method A: Insert multiband pan / band-limited auto-pan. Solo or target the high band only so lows stay centered.
3. Method A: Draw a sine (or subdued sine) pan path so highs slowly swirl L↔R. Try bar-length (4/4) for gentle immersion or 16th-note rate for more motion.
4. Method A: If 16ths feel too pronounced: switch to a less extreme pan profile and/or lower overall mix/amount of the pan effect.
5. Method A: A/B before/after in context: pad should envelop more without the washy phase of chorus/imager on full-band signal.
6. Method B: Duplicate the synth instance with identical settings and copy the MIDI to both tracks.
7. Method B: On track A piano roll, mute every other note top→bottom; on track B mute the complementary set bottom→top so together they reconstruct the full chords but separately play different notes.
8. Method B: Hard-pan A fully left and B fully right; play together for maximum width.
9. Method B: Check a correlation/phase meter: split technique should sit near ~0 (very wide) without deep negative swings; compare vs chorus (often flangy + negative correlation) and spreader (weaker width).

Replaces: `highband-pan-lfo-pad-width-keep-lows`, `mono-compatible-chord-split-stereo-pad`

MCP: `skill://pad-width-no-phase-smear-highband-pan-or-chord-split`
