# Morning synth YouTube hunt — 2026-10-12 (PT)

## Counts
- MCP before: 103 → after: 109
- New skills: 6
- Rejected: 13 (+1 stopped: no usable transcript, listed under rejects)
- Pivoted to crypto/side-hustle: no (synth returns not exhausted)

## New skill IDs
- `windowed-sync-amplitude-modulator-drawable-window` ← `g0QRn65Mwwc` (Windowed sync via sine/drawable amplitude window on phase-synced osc; removes sync clicks)
- `vector-xy-four-oscillator-crossfade-blend` ← `SMB34GRgQWQ` (True 2D vector: four corner oscs, nested XY crossfades)
- `dual-layer-opposite-vector-morph-pad` ← `6aRgJoBxk4g` (Dual-layer opposite-rotation vector morph pad + filter-drive LFO)
- `marimba-wt-lfo-pluck-to-granular-pad` ← `Daqws1QWgXw` (WT-position LFO mallet pluck/swell → granular freeze pad)
- `granular-stack-freeze-infinite-sustain-texture` ← `dxWCEDePgaw` (Stack granular FX to freeze short sources into infinite sustain)
- `dual-path-filter-spread-inverse-amp-lfo-stereo` ← `02_MBQrqJS8` (Opposite filter freqs + inverse amp LFO stereo from mono)

## Rejects
- `JPV5hC-9Rv0` Preset/Super Knob FMX Smart Morph; no portable recipe.
- `lLAj2rvBouI` Sample cinematic-hit layering; overlaps braam/sub-drop/downer.
- `S1MhzVyQ_Jc` Near-dup of cinematic-formant-comb-pad-phaser-fx.
- `vRKL_Br_LjM` STOP_no_transcript_asr_flagged (GrainFreeze).
- `EoR-zmIgUwk` COVERED / low delta vs existing WT scratch & morph skills.
- `CSdXkkW-jn0` COVERED Absynth morph product tour.
- `y0mfaQpWYQw` / `yMWyPdSs_wE` Prior-art riser/downer overlap; not distilled.
- `AOuTGhfU1Lo` / `SyKSIWu0RTA` Product WT overview / resample; thin vs pad recipes.
- `k8cvlDaK2RA` Formant plugin promo.
- `MBwAboKVrXE` Windowed-sinc FIR ≠ windowed-sync oscillator.
- `7qQX6YGBQEA` Vital full tutorial (only comb/phaser search hit); not a focused bed skill.

## Stopped (no transcript / translation)
- `vRKL_Br_LjM` STOP_no_transcript_asr_flagged: Create Lush Soundscapes with GrainFreeze

## Pipeline notes
- Pipeline .venv present; env already ensured.
- route.py COVERED again unreliable for terms missing from the synth lexicon (windowed-sync amp window, vector XY, granular freeze stack, dual-path stereo). Hand-checked against mcp-publish; distilled 6 gap skills.
- Quality --strict: all 6 clean (0 warnings). Novelty: 5 NOVEL; `dual-path-filter-spread-inverse-amp-lfo-stereo` REVIEW at 0.192 vs asymmetric width — kept as more-specific delta.
- Merged 6 skills into LIBRARY.json (+6 video entries → 107), topics/taxonomy.json cinematic-hybrid-synth (69→75 skill_ids), curriculum-cinematic-hybrid-synth level 3 (38→44), and skills/<id>.md.
- Git sync skipped: no credentials on the box (no GH_TOKEN/GITHUB_TOKEN, gh not logged in).
- Deferred queue still empty; upgrade_to_tlang still has MH7YiOWQIhI, kHWOIE4YTZ4, BqE9S27CZfY, beZpH9X850s.
- Unrelated: batches/2026-10-12-batch-01.json is a separate weekly intake (Inkscape/drywall/OBS/Kdenlive), not this synth hunt.

## Still thin for later hunts
- Phase-distortion resonant-wave / wave-alternation as a standalone performable skill
- Impact/boom from layered noise+pitch without overlapping braam/sub-drop/whoosh
- Dedicated comb/phaser cinematic bed beyond existing formant+comb pad
- Dual-filter morph (crossfade between two filter paths) as its own recipe
- Formant vocal-pad delta beyond existing formant+comb skill
