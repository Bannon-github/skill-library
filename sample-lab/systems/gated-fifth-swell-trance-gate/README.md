# gated-fifth-swell-trance-gate

Category: **gated** · found in round 9 · chain id `8abde1a620`

**Firing order:** `evolving-pad-unison-filter-swell-fifth` → `trance-gate-sidechain-chop-texture` → `traveler-walkthrough-stereo-ladder-lf-width` → `traveler-walkthrough-super-unison-wide-lead` → `traveler-walkthrough-fx-eq-chorus-delay-reverb`

**Scores (TARGET v1.3):** search grid 6/6 pass, robust 99.44; extended grid (3 note sets × 4 seeds) **12/12 pass**, robust **98.83**, mean 99.73, deterministic: True

Typical metric values (note set 0, seed 11): M1=-15.5, M2=0.7972, M3=0.689, M4=0.4293, M5=-17.6539, M6=-6.3354, M7=6.4185, M8=1.1267, M9=-13.5328, M12=-55.8464, M10=0.2156, M11=0.2556, M13=0.0, M14=-0.0, M15=1.5552

Advisory (not scored): sub-30 Hz energy -51.3 dB re total.

Renders: [gated-fifth-swell-trance-gate__50-53-57-62_seed11.wav](gated-fifth-swell-trance-gate__50-53-57-62_seed11.wav), [gated-fifth-swell-trance-gate__48-52-55-62_seed11.wav](gated-fifth-swell-trance-gate__48-52-55-62_seed11.wav), [gated-fifth-swell-trance-gate__45-52-57-60_seed11.wav](gated-fifth-swell-trance-gate__45-52-57-60_seed11.wav) (spectrogram PNG alongside each).

Re-render: `.venv/bin/python render_system.py gated-fifth-swell-trance-gate --notes 50,53,57,64 --seed 11 --score --spectrogram`

## Steps (sequential skill activation)

### 1. `evolving-pad-unison-filter-swell-fifth`  (voice)

*Evolving unison pad with filter swell and fifth layer*

Why here: From a Vital-style workflow: shape a pad with immediate amp and slow filter-open envelope, unison with spread, slow LFO→cutoff, layer a fifth (and optional higher) osc through the same filter with unison, compress, large reverb, optional chorus; keep peaks controlled.

| knob | value | grounded in |
|---|---|---|
| amp_attack | 0.05 | s1: amp can be quicker |
| release | 3.5 | conv |
| env2_attack | 2.0 | s1: env2 slow attack -> cutoff |
| cutoff | 700.0 | s1: tone arrives then opens (low base conv) |
| env_amt | 4.0 | s1: env2 depth (oct conv) |
| res | 0.1 | s1: low resonance |
| voices | 7 | s2: unison |
| width | 0.85 | s2: noticeable stereo spread |
| detune | 0.21 | conv moderate |
| lfo_amt | 0.25 | s2: optional slow LFO->cutoff |
| fifth_voices | 4 | s3: similar/less unison |
| fifth_level | 0.65 | s3: fifth (+7) into same filter |
| third_voice | False | s3: optional higher voice with LFO->level |
| comp_ratio | 2.5 | s4: glue compression |
| rev_rt60 | 4.0 | s4: large size/decay reverb |
| rev_send | 0.325 | s4: rising mix |
| chorus | False | s4: optional chorus |
| mode | base | chain mode: base=init voice, layer=add as extra layer |
| layer_gain | 0.45 | chain layer gain |

### 2. `trance-gate-sidechain-chop-texture`  (fx)

*Trance-gate: sidechain-gate chop a sustained pad*

Why here: Turn a long sustaining pad/wall-of-sound (or heavily reverbed short source) into rhythmic stuttered chunks by sidechain-gating it from a silent trigger pattern (e.g. clustered 16ths), then tune gate release for snap and optionally re-space with post-gate reverb.

| knob | value | grounded in |
|---|---|---|
| pattern | [1, 1, 1, 0] | s2: clusters of 3 sixteenths, or every 16th |
| release | 0.12 | s4: release for snap (shorter = choppier) |
| hold | 0.575 | s3: threshold/open time (conv) |
| power_chord | False | s1: optional root+octave+fifth thickening |
| post_reverb | True | s5: reverb after the gate |
| post_send | 0.225 | s5 (conv) |

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

### 4. `traveler-walkthrough-super-unison-wide-lead`  (voice)

*super-unison wide stereo lead (osc2 stack)*

Why here: Build a gigantic wide lead/pad layer using a multi-voice stereo unison oscillator (Traveler Osc2-style stack up to ~7 voices) with waveform morph and stereo spread.

| knob | value | grounded in |
|---|---|---|
| wave_pos | 0.125 | s1: continuous waveform saw->sine->thin pulse (near saw) |
| voices | 6 | s2: stack up to ~7 |
| detune | 0.3 | s2: increase detune until gigantic |
| width | 0.9 | s2: stereo spread |
| drive | 0.2 | s4: mild drive into filter |
| cutoff | 6396.7421 | s5: cutoff high enough to keep width |
| slope | lp12 | s5: 12-24 dB ladder |
| res | 0.175 | s5: modest resonance |
| attack | 0.9706 | s6: medium attack for pads |
| sustain | 0.8 | s6: sustain mid-high |
| release | 2.0 | s6: release 0.5-2s |
| mode | layer | chain mode: base=init voice, layer=add as extra layer |
| layer_gain | 0.45 | chain layer gain |

### 5. `traveler-walkthrough-fx-eq-chorus-delay-reverb`  (fx)

*EQ chorus dual-delay multi-algo reverb FX chain*

Why here: Finish a cinematic patch with the Traveler-style FX order: 3-band EQ → multi-type chorus → dual/ping-pong modulated delay → room/hall/space reverb (long space tails).

| knob | value | grounded in |
|---|---|---|
| low_db | -0.7341 | s1: sculpt low end |
| mid_db | 1.0 | s1: mid presence |
| high_db | 0.1687 | s1: highs |
| chorus_mix | 0.225 | s2: chorus wet modest |
| delay | dual | s3: dual or ping-pong modulated |
| dly_mix | 0.17 | s3 (conv moderate) |
| rev | hall | s4: room/hall/space |
| rev_send | 0.275 | conv |

## How the search got here

| round | id | mutation | robust (search grid) |
|---|---|---|---|
| 0 | `b0f6216234` | seed | 87.17 |
| 2 | `fc56a4b95c` | M6:evolving..cutoff:475.0->587.9597; M6:evolving..env_amt:3.0->3.5976; M7:evolving..cutoff:587.9597->464.909 | 91.12 |
| 3 | `992d92a597` | M6:evolving..cutoff:464.909->601.349; M6:evolving..env_amt:3.5976->4.0; M15:evolving..amp_attack:0.225->0.1483; M15:evolving..release:2.75->3.1676; M15:evolving..env2_attack:3.5->2.8531; M15:trance..release:0.07->0.1031 | 97.46 |
| 4 | `0128c22f9b` | M15:evolving..amp_attack:0.1483->0.05; M15:evolving..release:3.1676->3.5; M15:evolving..env2_attack:2.8531->2.0; M15:trance..release:0.1031->0.12; +traveler-walkthrough-super-unison-wide-lead (for M6) | 97.56 |
| 5 | `aed73878f5` | +traveler-walkthrough-fx-eq-chorus-delay-reverb (for M6); M15:traveler..attack:0.65->0.471; M15:traveler..release:1.25->1.7092 | 98.18 |
| 6 | `807e11c9e1` | M6:evolving..cutoff:601.349->700.0; M6:traveler..cutoff:5000.0->6396.7421; M6:traveler..high_db:-0.5->0.1687; M15:traveler..attack:0.471->0.3037; M15:traveler..release:1.7092->2.0 | 99.14 |
| 7 | `496c0f6f7c` | M15:traveler..attack:0.3037->0.3 | 99.14 |
| 9 | `8abde1a620` | knob traveler..low_db=-0.7341; knob traveler..delay=dual; knob traveler..attack=0.9706 | 99.44 |


## Perceptual check (spectrogram, by eye)

crisp, even 1/8-ish chops, no click lines at gate edges; loop seam invisible
