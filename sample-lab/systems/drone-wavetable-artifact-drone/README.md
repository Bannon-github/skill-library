# drone-wavetable-artifact-drone

Category: **drone** · found in round 12 · chain id `1e3dea2737`

**Firing order:** `ambient-organic-pluck-pad-ladder-chorus-space` → `traveler-walkthrough-stereo-ladder-lf-width` → `reverb-pads-type-choice-and-send-setup` → `shimmer-reverb-pitchshift-plus12-feedback` → `unison-odd-even-detune-width-clean-supersaw`

**Scores (TARGET v1.3):** search grid 6/6 pass, robust 100.0; extended grid (3 note sets × 4 seeds) **12/12 pass**, robust **98.73**, mean 99.85, deterministic: True

Typical metric values (note set 0, seed 11): M1=-15.5, M2=0.4832, M3=0.8241, M4=0.3105, M5=-24.0458, M6=-5.9534, M7=1.7031, M8=0.8743, M9=-14.9226, M12=-30.9742, M10=0.3301, M11=0.2471, M13=0.0, M14=-0.0, M15=1.186

Advisory (not scored): sub-30 Hz energy -51.5 dB re total.

Renders: [drone-wavetable-artifact-drone__38-45_seed11.wav](drone-wavetable-artifact-drone__38-45_seed11.wav), [drone-wavetable-artifact-drone__43-50_seed11.wav](drone-wavetable-artifact-drone__43-50_seed11.wav), [drone-wavetable-artifact-drone__36-43_seed11.wav](drone-wavetable-artifact-drone__36-43_seed11.wav) (spectrogram PNG alongside each).

Re-render: `.venv/bin/python render_system.py drone-wavetable-artifact-drone --notes 50,53,57,64 --seed 11 --score --spectrogram`

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
| cutoff | 650.0 | s3: ladder base (Hz conv) |
| env_amt | 1.9 | s3: env2 -> cutoff ~+24 semitones |
| res | 0.1 | s3: low resonance |
| env2_decay | 0.425 | s3: pluck contour (conv) |
| dist_drive | 0.4 | s4: moderate drive |
| dist_mix | 0.225 | s4: reduced mix |
| noise_level | 0.04 | s5: low pink noise -> BP |
| drift_c | 3.5 | s6: slow pitch drift |
| vel_amp | 0.4 | s7: velocity -> level |
| vel_cut | 1.5 | s7: velocity -> cutoff (oct conv) |
| chorus_fb | 0.6 | s8/C2: high feedback for long decay, metallic risk |
| chorus_depth | 5.5 | s8: raise depth/delay |
| chorus_hp | 300.0 | s8: high-pass |
| rev_send | 0.3 | s8: ~30% mix |
| rev_hp | 200.0 | s8: low cut |
| dly_mix | 0.3 | s8: dotted-quarter delay ~30% |
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
| lf_width_hz | 207.0521 | s5: mono below ~middle C (262 Hz) |

### 3. `reverb-pads-type-choice-and-send-setup`  (fx)

*Reverb for pads: pick type by texture, then set up 100%-wet EQ'd send returns*

Why here: Choose and route cinematic pad/synth reverb: decide if reverb is needed; pick type by texture not just length (hall lush 2–3s+ with mud risk, chamber thickening with less space, room/ambience intimate ~0.3–1s, plate bright attack→darker decay, spring metallic/boingy); keep 2–3 go-to returns (room ~1s, long plate ~6s, bright spring ~4s) at 100% wet on sends; high-pass returns ~200 Hz+; use pre-delay for clarity, layer short ambience under longer hall/plate, prefer shorter spaces in busy mixes, and pull send back on longer decays.

| knob | value | grounded in |
|---|---|---|
| type | hall | s3-s6: hall lush 2-3s+, plate ~6.2s, room ~1s |
| hall_rt60 | 3.25 | s3: hall ~2-3s+, longer for cinematic |
| plate_rt60 | 6.0 | s6: long ambient plate ~6.2s |
| room_rt60 | 1.0 | s6: room ~1s |
| predelay | 0.025 | s2: pre-delay for clarity |
| return_hp | 250.0 | s8: HP return ~200 Hz+ |
| send | 0.275 | s7/s10: send level; longer decays need less |
| high_cut | 0 | s9: optional high-cut darkens |

### 4. `shimmer-reverb-pitchshift-plus12-feedback`  (fx)

*Shimmer reverb: +12st pitch-shift into lush space*

Why here: Build a portable shimmer (Eno-style) send: pitch-shift the wet path by +12 semitones into a long lush reverb/convolution, optionally feedback the shifted delay for endless bloom, high-/low-cut the delay echoes before the reverb, and EQ the wet shimmer before dry blend.

| knob | value | grounded in |
|---|---|---|
| rt60 | 5.5 | s2: long lush reverb (capped by sample length) |
| feedback | 0.4 | s3: feedback for endless bloom |
| delay_s | 0.25 | s3: short = rapid, long = slower bloom |
| echo_hp | 300.0 | s4: cut lows on echoes |
| echo_lp | 5500.0 | s4: shave brittle highs |
| wet_hp | 275.0 | s5: HP the shimmer wet |
| send | 0.21 | s5: blend via send |

### 5. `unison-odd-even-detune-width-clean-supersaw`  (voice)

*Unison voicing: odd vs even voice counts, detune/blend/width, clean supersaw*

Why here: Set unison deliberately and build mix-ready supersaws: odd voice counts keep a centered in-tune voice for mono-compatible front-of-mix bass/leads/pads, even counts leave a center gap for ultra-wide off-center leads; keep detune/blend moderate; for supersaws use simple saw frames (not complex WT sweeps), ~6–12 voices, optional quieter Osc B, centered sub an octave down and quiet noise, EQ→compress→delay→reverb, subtle warp, and global unison width ~50% plus sparing stack modes for chord phase correlation.

| knob | value | grounded in |
|---|---|---|
| voices | 7 | s8: unison ~6-12; s4/C1: odd keeps a centered voice; even = ultra-wide |
| detune | 0.2 | s6/s8/C3: modest (~0.16 demo), near mid, conservative for chords |
| blend | 0.5 | s8: blend near mid |
| width | 0.4774 | s13/C3: global unison width ~50% for chord phase correlation |
| oscb | True | s9: optional Osc B |
| oscb_oct | 1 | s9: pitch +/-octaves |
| oscb_level | 0.4 | s9: lower level, fewer voices |
| sub_level | 0.3 | s10: optional centered saw sub one octave down (no unison) |
| noise_level | 0.04 | s10 + conv: quiet noise |
| eq_hp | 115.0 | s11: EQ cut lows (freq conv) |
| eq_hi_shelf_db | 2.0 | s11: EQ lift highs (amount conv) |
| comp_ratio | 3.0 | s11: compression (ratio conv) |
| attack | 1.1472 | conv: pad attack (skill gives none) |
| release | 3.2343 | conv: pad release |
| mode | layer | chain mode: base=init voice, layer=add as extra layer |
| layer_gain | 0.45 | chain layer gain |

## How the search got here

| round | id | mutation | robust (search grid) |
|---|---|---|---|
| 0 | `d6dc73c3dd` | seed | 86.43 |
| 1 | `bc6a12cbeb` | M6:ambient..lp_cut:1650.0->2183.2224; M6:ambient..hp_cut:325.0->441.2021; M7:ambient..lp_cut:2183.2224->1790.1739; M7:ambient..hp_cut:441.2021->319.8765 | 86.45 |
| 2 | `210baaa419` | +traveler-walkthrough-fx-eq-chorus-delay-reverb (for M6); M7:ambient..lp_cut:1790.1739->1287.8989; M7:ambient..hp_cut:319.8765->222.1577; M7:traveler..low_db:-1.75->-1.1067 | 87.69 |
| 4 | `93ee311d90` | +shimmer-reverb-pitchshift-plus12-feedback (for M6); M7:ambient..lp_cut:1287.8989->811.9333; M7:ambient..hp_cut:222.1577->150.0; M7:traveler..low_db:-1.1067->-0.5 | 90.44 |
| 5 | `7f78e33c2a` | +unison-odd-even-detune-width-clean-supersaw (for M6); M7:ambient..lp_cut:811.9333->800.0 | 97.54 |
| 6 | `e03aad5b93` | M15:ambient..attack:4.0->3.6904; M15:ambient..release:5.0->5.5632; M15:unison..attack:1.4->1.1472; M15:unison..release:2.75->3.2343 | 97.54 |
| 7 | `cb8e5b6720` | -keysol-venus-high-wt-artifact-pulse-layer | 97.95 |
| 8 | `2aa0dea30d` | sub ambient-wavetable-scratch-spectral-morph-pad->ambient-organic-pluck-pad-ladder-chorus-space | 99.87 |
| 9 | `c0528adf3d` | M4:traveler..lf_width_hz:230.0->207.0521; M4:unison..width:0.5->0.4774 | 100.0 |
| 12 | `1e3dea2737` | -traveler-walkthrough-fx-eq-chorus-delay-reverb | 100.0 |


## Perceptual check (spectrogram, by eye)

continuous evolving loop, no seam; dense/hissy top (shimmer + artifact layer) worth a taste check
