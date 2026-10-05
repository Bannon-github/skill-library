# pluck-organic-velocity-pluck

Category: **pluck** · found in round 11 · chain id `3b74cf35e0`

**Firing order:** `ambient-organic-pluck-pad-ladder-chorus-space` → `keysol-venus-high-wt-artifact-pulse-layer` → `traveler-walkthrough-stereo-ladder-lf-width` → `stereo-delay-pingpong-dual-parallel-two-tap` → `reverb-pads-type-choice-and-send-setup` → `traveler-walkthrough-fx-eq-chorus-delay-reverb` → `unison-odd-even-detune-width-clean-supersaw`

**Scores (TARGET v1.3):** search grid 6/6 pass, robust 97.66; extended grid (3 note sets × 4 seeds) **12/12 pass**, robust **97.66**, mean 98.16, deterministic: True

Typical metric values (note set 0, seed 11): M1=-15.5, M2=0.2432, M3=0.8637, M4=0.2707, M5=-17.4716, M6=-6.9826, M7=3.1865, M8=1.811, M9=-15.9915, M12=-30.4631, M10=0.4056, M11=0.2966, M13=0.0, M14=-0.0

Advisory (not scored): sub-30 Hz energy -59.8 dB re total.

Renders: [pluck-organic-velocity-pluck__62-65-69-72_seed11.wav](pluck-organic-velocity-pluck__62-65-69-72_seed11.wav), [pluck-organic-velocity-pluck__60-64-67-71_seed11.wav](pluck-organic-velocity-pluck__60-64-67-71_seed11.wav), [pluck-organic-velocity-pluck__57-60-64-69_seed11.wav](pluck-organic-velocity-pluck__57-60-64-69_seed11.wav) (spectrogram PNG alongside each).

Re-render: `.venv/bin/python render_system.py pluck-organic-velocity-pluck --notes 50,53,57,64 --seed 11 --score --spectrogram`

## Steps (sequential skill activation)

### 1. `ambient-organic-pluck-pad-ladder-chorus-space`  (voice)

*Organic ambient pluck-pad with ladder, velocity, chorus-space*

Why here: Shape a soft sine-based ambient pluck that sustains as a pad: warp toward saw, ladder filter envelope, gentle distortion, pink-noise bed, pitch drift, velocity→level/cutoff, then chorus pushed toward long decay plus reverb/delay.

| knob | value | grounded in |
|---|---|---|
| decay | 0.9 | s1: raised decay |
| sustain | 0.4 | s1: mid sustain (not zero) |
| release | 0.7 | s1: some release |
| warp | 0.275 | s2: sine warped toward saw-sine hybrid (WT position conv) |
| cutoff | 517.5041 | s3: ladder base (Hz conv) |
| env_amt | 2.0 | s3: env2 -> cutoff ~+24 semitones |
| res | 0.1 | s3: low resonance |
| env2_decay | 0.425 | s3: pluck contour (conv) |
| dist_drive | 0.4 | s4: moderate drive |
| dist_mix | 0.225 | s4: reduced mix |
| noise_level | 0.04 | s5: low pink noise -> BP |
| drift_c | 3.5 | s6: slow pitch drift |
| vel_amp | 0.4 | s7: velocity -> level |
| vel_cut | 1.2929 | s7: velocity -> cutoff (oct conv) |
| chorus_fb | 0.6 | s8/C2: high feedback for long decay, metallic risk |
| chorus_depth | 5.5 | s8: raise depth/delay |
| chorus_hp | 300.0 | s8: high-pass |
| rev_send | 0.3 | s8: ~30% mix |
| rev_hp | 200.0 | s8: low cut |
| dly_mix | 0.3 | s8: dotted-quarter delay ~30% |
| mode | base | chain mode: base=init voice, layer=add as extra layer |
| layer_gain | 0.45 | chain layer gain |

### 2. `keysol-venus-high-wt-artifact-pulse-layer`  (layer)

*high-pitch wavetable artifact over pulse sequence*

Why here: Spice a classic pulsing bass/filter sequence by adding a very high-pitched wavetable oscillator mixed as an artifact-like layer, with WT-position modulation for constant subtle evolution.

| knob | value | grounded in |
|---|---|---|
| oct | 2 | s2: tuned very high until artifact-like |
| level | 0.08 | s4: mix low under the bed |
| wt_lfo_amt | 0.275 | s3: slow WT-position modulation |
| wt_lfo_rate | 0.09 | s3: slow |

### 3. `traveler-walkthrough-stereo-ladder-lf-width`  (filter)

*dual stereo filter and LF-width imaging*

Why here: Shape a cinematic tone with stereo ladder/NJM-style filters, left/right cutoff offset or per-key spread, linked high-pass for band-pass effects, and low-frequency width so bass stays centered while highs move.

| knob | value | grounded in |
|---|---|---|
| slope | lp24 | s1: ladder 6-24 dB |
| stereo_off | 0.25 | s2: L/R cutoff offset, subtle |
| hp | 80.0 | s3: dedicated HP (conv) |
| pan_spread | 0.4 | s4: pan-spread fans successive voices |
| lf_width_hz | 230.0 | s5: mono below ~middle C (262 Hz) |

### 4. `stereo-delay-pingpong-dual-parallel-two-tap`  (fx)

*Stereo delay motion: ping-pong, dual-parallel, two-tap, cross-feedback*

Why here: Build musical stereo delay motion for synths/pads: tempo-synced ping-pong (feedback ~40–50%, wet ~15–25%, repeats band-limited ~100 Hz–3 kHz, optional saturation, even or offset L/R), dual-parallel (independent L/R subdivisions such as dotted-eighth vs quarter, self-feedback then cross-feedback, optional modulation/diffusion for reverb-like density), two-tap tape-head (long tap feeds short; short has no self/cross feedback), ping-pong recognized as a 2:1 two-tap, LFO panning delay and feedback-phase invert; prefer send routing and automate for evolving motion.

| knob | value | grounded in |
|---|---|---|
| topology | pingpong | s1: ping-pong vs dual-parallel |
| sync | 1/4 | s2: quarter or eighth |
| feedback | 0.45 | s3: ~40-50% |
| mix | 0.2 | s3: wet ~15-25% |
| sat | 0.1 | s4: tiny saturation |
| cross | 0.15 | s8: cross-feedback |
| mod_depth | 0.0015 | s9: delay modulation (~20% conv) |

### 5. `reverb-pads-type-choice-and-send-setup`  (fx)

*Reverb for pads: pick type by texture, then set up 100%-wet EQ'd send returns*

Why here: Choose and route cinematic pad/synth reverb: decide if reverb is needed; pick type by texture not just length (hall lush 2–3s+ with mud risk, chamber thickening with less space, room/ambience intimate ~0.3–1s, plate bright attack→darker decay, spring metallic/boingy); keep 2–3 go-to returns (room ~1s, long plate ~6s, bright spring ~4s) at 100% wet on sends; high-pass returns ~200 Hz+; use pre-delay for clarity, layer short ambience under longer hall/plate, prefer shorter spaces in busy mixes, and pull send back on longer decays.

| knob | value | grounded in |
|---|---|---|
| type | room | s3-s6: hall lush 2-3s+, plate ~6.2s, room ~1s |
| hall_rt60 | 3.25 | s3: hall ~2-3s+, longer for cinematic |
| plate_rt60 | 6.0 | s6: long ambient plate ~6.2s |
| room_rt60 | 1.0 | s6: room ~1s |
| predelay | 0.025 | s2: pre-delay for clarity |
| return_hp | 250.0 | s8: HP return ~200 Hz+ |
| send | 0.275 | s7/s10: send level; longer decays need less |
| high_cut | 0 | s9: optional high-cut darkens |

### 6. `traveler-walkthrough-fx-eq-chorus-delay-reverb`  (fx)

*EQ chorus dual-delay multi-algo reverb FX chain*

Why here: Finish a cinematic patch with the Traveler-style FX order: 3-band EQ → multi-type chorus → dual/ping-pong modulated delay → room/hall/space reverb (long space tails).

| knob | value | grounded in |
|---|---|---|
| low_db | -0.5 | s1: sculpt low end |
| mid_db | 1.0 | s1: mid presence |
| high_db | 1.0 | s1: highs |
| chorus_mix | 0.225 | s2: chorus wet modest |
| delay | pingpong | s3: dual or ping-pong modulated |
| dly_mix | 0.17 | s3 (conv moderate) |
| rev | hall | s4: room/hall/space |
| rev_send | 0.275 | conv |

### 7. `unison-odd-even-detune-width-clean-supersaw`  (voice)

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
| eq_hi_shelf_db | 2.451 | s11: EQ lift highs (amount conv) |
| comp_ratio | 3.0 | s11: compression (ratio conv) |
| attack | 1.4 | conv: pad attack (skill gives none) |
| release | 2.75 | conv: pad release |
| mode | layer | chain mode: base=init voice, layer=add as extra layer |
| layer_gain | 0.45 | chain layer gain |

## How the search got here

| round | id | mutation | robust (search grid) |
|---|---|---|---|
| 0 | `e423978a6b` | seed | 86.05 |
| 1 | `4f569caf07` | +traveler-walkthrough-fx-eq-chorus-delay-reverb (for M6); M7:ambient..cutoff:650.0->486.9311; M7:ambient..vel_cut:1.5->1.1658; M7:traveler..low_db:-1.75->-1.073 | 86.89 |
| 2 | `50002356e8` | M6:ambient..cutoff:486.9311->649.8851; M6:ambient..env_amt:1.9->1.9596; M6:ambient..vel_cut:1.1658->1.379; M6:velocity..floor:600.0->763.7233; M6:velocity..eg_amt:2.5->3.0046; M6:traveler..high_db:-0.5->0.1756; M7:ambient..cutoff:649.8851->491.1465; M7:ambient..vel_cut:1.379->1.1186; M7:traveler..low_db:-1.073->-0.5 | 86.89 |
| 3 | `5fcd100047` | M6:ambient..cutoff:491.1465->607.7561; M6:ambient..env_amt:1.9596->2.0; M6:ambient..vel_cut:1.1186->1.3485; M6:velocity..floor:763.7233->900.0; M6:velocity..eg_amt:3.0046->3.5; M6:traveler..high_db:0.1756->1.0; M7:ambient..cutoff:607.7561->453.9756; M7:ambient..vel_cut:1.3485->1.1009 | 86.89 |
| 4 | `150a786976` | +keysol-venus-high-wt-artifact-pulse-layer (for M6); M7:ambient..cutoff:453.9756->400.0; M7:ambient..vel_cut:1.1009->1.0 | 93.44 |
| 9 | `aeebcfc0b7` | +unison-odd-even-detune-width-clean-supersaw (for M6) | 94.85 |
| 10 | `fe00b325fe` | M6:ambient..cutoff:400.0->517.5041; M6:ambient..vel_cut:1.0->1.2929; M6:unison..eq_hi_shelf_db:2.0->2.451; +traveler-walkthrough-stereo-ladder-lf-width (for M5) | 96.43 |
| 11 | `3b74cf35e0` | -velocity-filter-cutoff-envelope-amount | 97.66 |


## Perceptual check (spectrogram, by eye)

clear note onsets, decaying echo tail; each note's HF ends sharply at the next onset (mono retrigger), audition for tail truncation
