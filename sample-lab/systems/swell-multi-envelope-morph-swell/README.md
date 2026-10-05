# swell-multi-envelope-morph-swell

Category: **swell** · found in round 12 · chain id `7be644268a`

**Firing order:** `cinematic-multi-envelope-osc-level-morph` → `traveler-walkthrough-stereo-ladder-lf-width` → `keysol-venus-high-wt-artifact-pulse-layer` → `chorus-ensemble-classic-vibrato-pad-modes` → `stereo-delay-pingpong-dual-parallel-two-tap` → `mix-pads-role-eq-width-clarity` → `traveler-walkthrough-super-unison-wide-lead` → `unison-odd-even-detune-width-clean-supersaw`

**Scores (TARGET v1.3):** search grid 6/6 pass, robust 100.0; extended grid (3 note sets × 4 seeds) **12/12 pass**, robust **100.0**, mean 100.0, deterministic: True

Typical metric values (note set 0, seed 11): M1=-15.5, M2=0.4722, M3=0.7521, M4=0.3762, M5=-17.4759, M6=-5.9509, M7=7.0341, M8=1.4871, M9=-16.9233, M12=-28.9281, M10=0.2351, M11=0.2186, M13=0.0, M14=-0.0

Advisory (not scored): sub-30 Hz energy -57.4 dB re total.

Renders: [swell-multi-envelope-morph-swell__50-57-62-65_seed11.wav](swell-multi-envelope-morph-swell__50-57-62-65_seed11.wav), [swell-multi-envelope-morph-swell__48-55-60-64_seed11.wav](swell-multi-envelope-morph-swell__48-55-60-64_seed11.wav), [swell-multi-envelope-morph-swell__45-52-57-64_seed11.wav](swell-multi-envelope-morph-swell__45-52-57-64_seed11.wav) (spectrogram PNG alongside each).

Re-render: `.venv/bin/python render_system.py swell-multi-envelope-morph-swell --notes 50,53,57,64 --seed 11 --score --spectrogram`

## Steps (sequential skill activation)

### 1. `cinematic-multi-envelope-osc-level-morph`  (voice)

*Multi-envelope oscillator-level morphing pad*

Why here: Create an always-in-motion pad by silencing shared amp control of oscillators and assigning staggered envelope-mode LFOs to each oscillator level (plus optional noise), with differing filter and WT motion.

| knob | value | grounded in |
|---|---|---|
| release | 4.5 | s1: amp release ~5s |
| a1 | 0.35 | s3: staggered attacks |
| a2 | 1.85 | s3: staggered attacks |
| a3 | 3.5 | s3: staggered attacks |
| oct3 | 1 | s4: octave-shift layers |
| pan_amt | 0.35 | s4: pan layers |
| res | 0.075 | s5: reduce resonance |
| noise_level | 0.065 | s6: noise wash own envelope |
| wt_sync | 1bar | s7: synced LFO -> WT position |
| rev_rt60 | 6.5 | s8: long ambient reverb (capped 8s) |
| rev_send | 0.325 | conv |
| mode | base | chain mode: base=init voice, layer=add as extra layer |
| layer_gain | 0.45 | chain layer gain |

### 2. `traveler-walkthrough-stereo-ladder-lf-width`  (filter)

*dual stereo filter and LF-width imaging*

Why here: Shape a cinematic tone with stereo ladder/NJM-style filters, left/right cutoff offset or per-key spread, linked high-pass for band-pass effects, and low-frequency width so bass stays centered while highs move.

| knob | value | grounded in |
|---|---|---|
| slope | lp24 | s1: ladder 6-24 dB |
| stereo_off | 0.25 | s2: L/R cutoff offset, subtle |
| hp | 80.0 | s3: dedicated HP (conv) |
| pan_spread | 0.4 | s4: pan-spread fans successive voices |
| lf_width_hz | 230.0 | s5: mono below ~middle C (262 Hz) |

### 3. `keysol-venus-high-wt-artifact-pulse-layer`  (layer)

*high-pitch wavetable artifact over pulse sequence*

Why here: Spice a classic pulsing bass/filter sequence by adding a very high-pitched wavetable oscillator mixed as an artifact-like layer, with WT-position modulation for constant subtle evolution.

| knob | value | grounded in |
|---|---|---|
| oct | 2 | s2: tuned very high until artifact-like |
| level | 0.08 | s4: mix low under the bed |
| wt_lfo_amt | 0.275 | s3: slow WT-position modulation |
| wt_lfo_rate | 0.09 | s3: slow |

### 4. `chorus-ensemble-classic-vibrato-pad-modes`  (fx)

*Chorus-Ensemble modes: Classic, Ensemble, Vibrato*

Why here: Thicken cinematic pads with a multi-mode chorus: Classic (2 delayed copies + LFO on delay time), Ensemble (third evenly-split copy for fuller body), or Vibrato (pitch-only wobble); tune rate/amount/feedback/width/dry-wet, high-pass the wet to avoid mud, optional warmth/saturation, and LFO offset for stereo vibrato.

| knob | value | grounded in |
|---|---|---|
| mode | ensemble | s1: classic (2 copies) vs ensemble (3) |
| rate | 0.5 | s2: warm sweet spot |
| depth_ms | 2.0445 | s2: amount (ms conv) |
| feedback | 0.15 | s2: feedback; extreme turns metallic |
| wet_hp | 275.0 | s3: high-pass the processed path |
| width | 0.9 | s4: width (up to ~200%) |
| mix | 0.375 | s4: blend so pad stays present |

### 5. `stereo-delay-pingpong-dual-parallel-two-tap`  (fx)

*Stereo delay motion: ping-pong, dual-parallel, two-tap, cross-feedback*

Why here: Build musical stereo delay motion for synths/pads: tempo-synced ping-pong (feedback ~40–50%, wet ~15–25%, repeats band-limited ~100 Hz–3 kHz, optional saturation, even or offset L/R), dual-parallel (independent L/R subdivisions such as dotted-eighth vs quarter, self-feedback then cross-feedback, optional modulation/diffusion for reverb-like density), two-tap tape-head (long tap feeds short; short has no self/cross feedback), ping-pong recognized as a 2:1 two-tap, LFO panning delay and feedback-phase invert; prefer send routing and automate for evolving motion.

| knob | value | grounded in |
|---|---|---|
| topology | pingpong | s1: ping-pong vs dual-parallel |
| sync | 1/4 | s2: quarter or eighth |
| feedback | 0.45 | s3: ~40-50% |
| mix | 0.2 | s3: wet ~15-25% |
| sat | 0.1 | s4: tiny saturation |
| cross | 0.171 | s8: cross-feedback |
| mod_depth | 0.0015 | s9: delay modulation (~20% conv) |

### 6. `mix-pads-role-eq-width-clarity`  (mix)

*Mix pads for role, EQ clarity, energy, and width control*

Why here: Mix pads based on role (lead ambient vs background glue): infinite-average spectrum to see occupied bands, high-pass to protect kick/bass, filter reverb/delay lows (~100 Hz), manage mids/highs vs vocals with dynamic/sidechain EQ sparingly, automate filter/FX for section energy, and narrow stereo (or multiband width) when pads crowd the image.

| knob | value | grounded in |
|---|---|---|
| role | lead_bed | s1: pad role |
| hp | 120.0 | s3: HP pad to protect kick/bass |
| return_hp | 150.0 | s3: HP reverb/delay returns ~100 Hz |
| narrow_hz | 225.0 | s6: multiband-narrow conflicting bands |

### 7. `traveler-walkthrough-super-unison-wide-lead`  (voice)

*super-unison wide stereo lead (osc2 stack)*

Why here: Build a gigantic wide lead/pad layer using a multi-voice stereo unison oscillator (Traveler Osc2-style stack up to ~7 voices) with waveform morph and stereo spread.

| knob | value | grounded in |
|---|---|---|
| wave_pos | 0.125 | s1: continuous waveform saw->sine->thin pulse (near saw) |
| voices | 6 | s2: stack up to ~7 |
| detune | 0.3 | s2: increase detune until gigantic |
| width | 0.9 | s2: stereo spread |
| drive | 0.2 | s4: mild drive into filter |
| cutoff | 3099.2663 | s5: cutoff high enough to keep width |
| slope | lp12 | s5: 12-24 dB ladder |
| res | 0.175 | s5: modest resonance |
| attack | 0.65 | s6: medium attack for pads |
| sustain | 0.8 | s6: sustain mid-high |
| release | 1.25 | s6: release 0.5-2s |
| mode | layer | chain mode: base=init voice, layer=add as extra layer |
| layer_gain | 0.45 | chain layer gain |

### 8. `unison-odd-even-detune-width-clean-supersaw`  (voice)

*Unison voicing: odd vs even voice counts, detune/blend/width, clean supersaw*

Why here: Set unison deliberately and build mix-ready supersaws: odd voice counts keep a centered in-tune voice for mono-compatible front-of-mix bass/leads/pads, even counts leave a center gap for ultra-wide off-center leads; keep detune/blend moderate; for supersaws use simple saw frames (not complex WT sweeps), ~6–12 voices, optional quieter Osc B, centered sub an octave down and quiet noise, EQ→compress→delay→reverb, subtle warp, and global unison width ~50% plus sparing stack modes for chord phase correlation.

| knob | value | grounded in |
|---|---|---|
| voices | 7 | s8: unison ~6-12; s4/C1: odd keeps a centered voice; even = ultra-wide |
| detune | 0.2 | s6/s8/C3: modest (~0.16 demo), near mid, conservative for chords |
| blend | 0.5 | s8: blend near mid |
| width | 0.5 | s13/C3: global unison width ~50% for chord phase correlation |
| oscb | True | s9: optional Osc B |
| oscb_oct | 1 | s9: pitch +/-octaves |
| oscb_level | 0.4 | s9: lower level, fewer voices |
| sub_level | 0.3 | s10: optional centered saw sub one octave down (no unison) |
| noise_level | 0.04 | s10 + conv: quiet noise |
| eq_hp | 115.0 | s11: EQ cut lows (freq conv) |
| eq_hi_shelf_db | 2.0 | s11: EQ lift highs (amount conv) |
| comp_ratio | 3.0 | s11: compression (ratio conv) |
| attack | 1.4 | conv: pad attack (skill gives none) |
| release | 2.75 | conv: pad release |
| mode | layer | chain mode: base=init voice, layer=add as extra layer |
| layer_gain | 0.45 | chain layer gain |

## How the search got here

| round | id | mutation | robust (search grid) |
|---|---|---|---|
| 0 | `1cdcb26c7a` | seed | 78.87 |
| 1 | `efbdf554b7` | knob chorus..depth_ms=2.0445; knob stereo..cross=0.171 | 79.5 |
| 2 | `118e577bd3` | +traveler-walkthrough-fx-eq-chorus-delay-reverb (for M6); +traveler-walkthrough-stereo-ladder-lf-width (for M5) | 86.9 |
| 3 | `60f28a167e` | M6:traveler..high_db:-0.5->0.2055; M7:traveler..low_db:-1.75->-1.0695 | 87.24 |
| 4 | `aa407e3f0f` | +traveler-walkthrough-super-unison-wide-lead (for M6); M7:traveler..low_db:-1.0695->-0.5; M7:traveler..cutoff:5000.0->3895.6649 | 91.28 |
| 5 | `fe365b4ec2` | M6:traveler..high_db:0.2055->1.0; M6:traveler..cutoff:3895.6649->4958.463; M7:traveler..cutoff:4958.463->4055.2225 | 91.95 |
| 6 | `eec0fd0856` | M6:traveler..cutoff:4055.2225->5337.3296; M7:traveler..cutoff:5337.3296->4126.1805 | 92.11 |
| 7 | `fe0b56e583` | +keysol-venus-high-wt-artifact-pulse-layer (for M6); M7:traveler..cutoff:4126.1805->3099.2663 | 94.34 |
| 8 | `8792041e0c` | +unison-odd-even-detune-width-clean-supersaw (for M6) | 100.0 |
| 12 | `7be644268a` | -traveler-walkthrough-fx-eq-chorus-delay-reverb | 100.0 |


## Perceptual check (spectrogram, by eye)

clean, gentle ~1.6 s periodic motion; but energy is present from t=0 so the 'swell' shape is weak visually
