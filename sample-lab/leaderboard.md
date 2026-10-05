# Sample Lab leaderboard

Target: TARGET.md v1.3 · rounds run: 0–12 · candidate evaluations logged: 470 (each = 6 renders) · see iterations.jsonl

## Winning systems (extended validation: 3 note sets × 4 seeds = 12 renders)

| rank | system | category | skills fired (in order) | pass | robust | mean | perceptual check |
|---|---|---|---|---|---|---|---|
| 1 | [pad-wide-supersaw-chord-pad](systems/pad-wide-supersaw-chord-pad/README.md) | pad | warm-heavenly-supersaw-pad-keytrack-fx → unison-odd-even-detune-width-clean-supersaw → traveler-walkthrough-stereo-ladder-lf-width | 12/12 | 100.0 | 100.0 | clean dense sustain, smooth release decay after note-off; no clicks/aliasing lines; very bright air up to 20 kHz |
| 2 | [bass-velocity-hybrid-bass](systems/bass-velocity-hybrid-bass/README.md) | bass | keysol-venus-velocity-hybrid-bass-impact → hybrid-noise-distortion-separate-sub-layer → traveler-walkthrough-stereo-ladder-lf-width → traveler-walkthrough-curved-envelope-evolving-pad → soft-tape-saturation-pads-before-space | 12/12 | 100.0 | 100.0 | solid centered fundamental + harmonics in Mid; noise layer swells mostly in Side (peak ~4.5 s); no clicks; reads more 'textural sub' than punchy |
| 3 | [swell-multi-envelope-morph-swell](systems/swell-multi-envelope-morph-swell/README.md) | swell | cinematic-multi-envelope-osc-level-morph → traveler-walkthrough-stereo-ladder-lf-width → keysol-venus-high-wt-artifact-pulse-layer → chorus-ensemble-classic-vibrato-pad-modes → stereo-delay-pingpong-dual-parallel-two-tap → mix-pads-role-eq-width-clarity → traveler-walkthrough-super-unison-wide-lead → unison-odd-even-detune-width-clean-supersaw | 12/12 | 100.0 | 100.0 | clean, gentle ~1.6 s periodic motion; but energy is present from t=0 so the 'swell' shape is weak visually |
| 4 | [gated-fifth-swell-trance-gate](systems/gated-fifth-swell-trance-gate/README.md) | gated | evolving-pad-unison-filter-swell-fifth → trance-gate-sidechain-chop-texture → traveler-walkthrough-stereo-ladder-lf-width → traveler-walkthrough-super-unison-wide-lead → traveler-walkthrough-fx-eq-chorus-delay-reverb | 12/12 | 98.83 | 99.73 | crisp, even 1/8-ish chops, no click lines at gate edges; loop seam invisible |
| 5 | [drone-wavetable-artifact-drone](systems/drone-wavetable-artifact-drone/README.md) | drone | ambient-organic-pluck-pad-ladder-chorus-space → traveler-walkthrough-stereo-ladder-lf-width → reverb-pads-type-choice-and-send-setup → shimmer-reverb-pitchshift-plus12-feedback → unison-odd-even-detune-width-clean-supersaw | 12/12 | 98.73 | 99.85 | continuous evolving loop, no seam; dense/hissy top (shimmer + artifact layer) worth a taste check |
| 6 | [pluck-organic-velocity-pluck](systems/pluck-organic-velocity-pluck/README.md) | pluck | ambient-organic-pluck-pad-ladder-chorus-space → keysol-venus-high-wt-artifact-pulse-layer → traveler-walkthrough-stereo-ladder-lf-width → stereo-delay-pingpong-dual-parallel-two-tap → reverb-pads-type-choice-and-send-setup → traveler-walkthrough-fx-eq-chorus-delay-reverb → unison-odd-even-detune-width-clean-supersaw | 12/12 | 97.66 | 98.16 | clear note onsets, decaying echo tail; each note's HF ends sharply at the next onset (mono retrigger), audition for tail truncation |

## Best attempt per category (search grid, all rounds)

| category | best chain id | name | pass/6 | robust | weakest metrics |
|---|---|---|---|---|---|
| bass | `82661e7281` | velocity-hybrid-bass | 6 | 100.0 | — |
| drone | `c0528adf3d` | wavetable-artifact-drone | 6 | 100.0 | — |
| gated | `8abde1a620` | fifth-swell-trance-gate | 6 | 99.44 | M15 |
| pad | `b70dd901a1` | wide-supersaw-chord-pad | 6 | 100.0 | — |
| pluck | `3b74cf35e0` | organic-velocity-pluck | 6 | 97.66 | M6 |
| swell | `8792041e0c` | multi-envelope-morph-swell | 6 | 100.0 | — |

## Progress by round (best robust score per category)

| round | bass | drone | gated | pad | pluck | swell | reliable chains found |
|---|---|---|---|---|---|---|---|
| 0 | 89.41 | 86.43 | 87.17 | 100.0 | 86.05 | 78.87 | 1 |
| 1 | 89.48 | 87.68 | 87.17 | 100.0 | 86.89 | 86.89 | 4 |
| 2 | 96.89 | 87.69 | 91.12 | 100.0 | 86.89 | 86.9 | 9 |
| 3 | 96.89 | 87.69 | 97.46 | 100.0 | 86.89 | 87.25 | 19 |
| 4 | 96.89 | 94.89 | 97.56 | 100.0 | 93.44 | 91.28 | 26 |
| 5 | 96.89 | 97.54 | 98.18 | 100.0 | 93.44 | 91.95 | 34 |
| 6 | 96.89 | 97.54 | 99.14 | 100.0 | 93.44 | 92.11 | 42 |
| 7 | 98.32 | 97.95 | 99.14 | 100.0 | 93.44 | 94.34 | 55 |
| 8 | 100.0 | 99.87 | 99.14 | 100.0 | 93.44 | 100.0 | 68 |
| 9 | 100.0 | 100.0 | 99.44 | 100.0 | 94.86 | 100.0 | 82 |
| 10 | 100.0 | 100.0 | 99.44 | 100.0 | 96.43 | 100.0 | 99 |
| 11 | 100.0 | 100.0 | 99.44 | 100.0 | 97.66 | 100.0 | 120 |
| 12 | 100.0 | 100.0 | 99.44 | 100.0 | 97.66 | 100.0 | 140 |
