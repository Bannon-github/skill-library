# Findings: which skills mattered

Computed from every candidate in iterations.jsonl (latest score per chain).

| skill | in winners | chains evaluated | % reliable | mean robust | mean Δrobust when added by mutation (n) |
|---|---|---|---|---|---|
| `traveler-walkthrough-stereo-ladder-lf-width` | 6 | 263 | 50% | 94.9 | +3.5 (6) |
| `unison-odd-even-detune-width-clean-supersaw` | 4 | 112 | 76% | 98.3 | +3.9 (4) |
| `traveler-walkthrough-fx-eq-chorus-delay-reverb` | 2 | 254 | 25% | 92.9 | +0.5 (16) |
| `stereo-delay-pingpong-dual-parallel-two-tap` | 2 | 190 | 11% | 91.4 | — |
| `reverb-pads-type-choice-and-send-setup` | 2 | 165 | 13% | 91.4 | — |
| `keysol-venus-high-wt-artifact-pulse-layer` | 2 | 151 | 19% | 93.6 | +2.9 (6) |
| `ambient-organic-pluck-pad-ladder-chorus-space` | 2 | 114 | 16% | 93.2 | — |
| `traveler-walkthrough-super-unison-wide-lead` | 2 | 87 | 45% | 95.4 | -0.6 (9) |
| `chorus-ensemble-classic-vibrato-pad-modes` | 1 | 92 | 24% | 91.9 | -0.3 (2) |
| `mix-pads-role-eq-width-clarity` | 1 | 85 | 18% | 91.4 | -0.2 (3) |
| `cinematic-multi-envelope-osc-level-morph` | 1 | 82 | 17% | 91.1 | — |
| `soft-tape-saturation-pads-before-space` | 1 | 66 | 32% | 93.0 | -0.4 (11) |
| `evolving-pad-unison-filter-swell-fifth` | 1 | 50 | 70% | 95.3 | — |
| `trance-gate-sidechain-chop-texture` | 1 | 50 | 72% | 95.3 | -0.0 (1) |
| `hybrid-noise-distortion-separate-sub-layer` | 1 | 49 | 43% | 95.1 | — |
| `keysol-venus-velocity-hybrid-bass-impact` | 1 | 49 | 41% | 94.8 | — |
| `shimmer-reverb-pitchshift-plus12-feedback` | 1 | 48 | 58% | 94.6 | +0.2 (9) |
| `warm-heavenly-supersaw-pad-keytrack-fx` | 1 | 45 | 89% | 98.8 | — |
| `traveler-walkthrough-curved-envelope-evolving-pad` | 1 | 19 | 79% | 94.0 | +1.7 (1) |
| `velocity-filter-cutoff-envelope-amount` | 0 | 92 | 0% | 92.1 | — |
| `ambient-wavetable-scratch-spectral-morph-pad` | 0 | 48 | 25% | 91.4 | — |
| `traveler-walkthrough-control-track-filter-wt-animation` | 0 | 34 | 53% | 96.7 | +7.5 (1) |
| `midside-eq-bass-focus-width-depth` | 0 | 30 | 70% | 96.0 | +4.8 (3) |
| `osc-as-granular-pitch-step-delay` | 0 | 14 | 21% | 88.1 | -0.1 (3) |
| `modulation-lfo-envelope-mod-matrix-routing` | 0 | 14 | 0% | 89.4 | -0.1 (4) |
| `parallel-filter-rhythmic-pad-chains` | 0 | 11 | 9% | 87.1 | -2.3 (5) |
| `filter-ladder-diode-comb-formant-flavors` | 0 | 9 | 11% | 87.8 | +0.0 (1) |
| `fm-carrier-modulator-ratio-basics` | 0 | 6 | 0% | 81.0 | — |
| `sidechain-compressor-duck-synth-pads` | 0 | 6 | 17% | 85.4 | +0.0 (2) |
| `lush-stereo-saw-pad-random-pitch-texture` | 0 | 5 | 0% | 82.8 | — |
| `keysol-venus-polyrhythmic-control-track-pitch` | 0 | 5 | 0% | 88.0 | -0.9 (1) |
| `cinematic-warm-analog-pad-drift-stereo` | 0 | 4 | 0% | 89.2 | — |
| `digital-wt-morph-bandpass-chorus-echo-space` | 0 | 4 | 0% | 72.0 | — |
| `audio-rate-am-wave-shape-texture` | 0 | 4 | 0% | 85.2 | — |
| `pad-width-no-phase-smear-highband-pan-or-chord-split` | 0 | 4 | 75% | 96.7 | +0.0 (1) |
| `wavetable-crossfade-morph-modulate-pad` | 0 | 2 | 50% | 93.4 | — |
| `keysol-venus-fifths-pulsar-wt-impact` | 0 | 1 | 0% | 83.6 | — |
| `cinematic-formant-comb-pad-phaser-fx` | 0 | 1 | 0% | 86.9 | — |
| `granular-dual-saw-ambient-epic-pad` | 0 | 0 | — | — | — |
| `traveler-walkthrough-wavetable-morph-filter-motion` | 0 | 0 | — | — | — |
| `keysol-helpling-keytrack-bass-split-delay` | 0 | 0 | — | — | — |

Not implemented in the renderer (gaps): `spectral-warp-vocode-formant-stretch-smear` (no per-harmonic spectral-warp oscillator in the renderer); `organic-looped-sample-unison-voicing-pad` (needs original acoustic samples (none on the box; original-synthesis-only rule)); `keysol-venus-fm-lfo-evolving-chase-sequence` (arp/sequence performance skill; partially covered by control-track + FM skills); `keysol-venus-noise-audiorate-filter-texture` (audio-rate filter FM + aftertouch performance; intentionally unstable)
