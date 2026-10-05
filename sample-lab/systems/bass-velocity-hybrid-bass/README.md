# bass-velocity-hybrid-bass

Category: **bass** · found in round 11 · chain id `67af516950`

**Firing order:** `keysol-venus-velocity-hybrid-bass-impact` → `hybrid-noise-distortion-separate-sub-layer` → `traveler-walkthrough-stereo-ladder-lf-width` → `traveler-walkthrough-curved-envelope-evolving-pad` → `soft-tape-saturation-pads-before-space`

**Scores (TARGET v1.3):** search grid 6/6 pass, robust 100.0; extended grid (3 note sets × 4 seeds) **12/12 pass**, robust **100.0**, mean 100.0, deterministic: True

Typical metric values (note set 0, seed 11): M1=-14.6018, M2=0.0278, M3=0.993, M4=0.0594, M5=-40.4866, M6=-7.0535, M7=4.5697, M8=0.3673, M9=-24.7987, M12=-51.5902, M10=0.1282, M11=0.1452, M13=0.0, M14=-0.0

Advisory (not scored): sub-30 Hz energy -18.0 dB re total.

Renders: [bass-velocity-hybrid-bass__28_seed11.wav](bass-velocity-hybrid-bass__28_seed11.wav), [bass-velocity-hybrid-bass__33_seed11.wav](bass-velocity-hybrid-bass__33_seed11.wav), [bass-velocity-hybrid-bass__38_seed11.wav](bass-velocity-hybrid-bass__38_seed11.wav) (spectrogram PNG alongside each).

Re-render: `.venv/bin/python render_system.py bass-velocity-hybrid-bass --notes 50,53,57,64 --seed 11 --score --spectrogram`

## Steps (sequential skill activation)

### 1. `keysol-venus-velocity-hybrid-bass-impact`  (voice)

*velocity-rewarding hybrid bass and impact*

Why here: Design a thunderous hybrid bass/impact that responds exponentially to velocity (louder hits open filter/amp dramatically), usable as deep hits or high atmospheric stabs with HP + long space reverb.

| knob | value | grounded in |
|---|---|---|
| osc | saw | s1: dark saw/pulse |
| wt_spice | 0.15 | s1: optional WT |
| decay | 0.55 | s1: punchy decay |
| sustain | 0.525 | s1: moderate sustain |
| release | 0.55 | conv |
| cutoff | 199.2442 | s1: dark (Hz conv) |
| vel_cut | 2.2682 | s2: strong velocity -> cutoff |
| env_amt | 1.75 | s1/s2: transient bloom |
| sub_level | 0.4 | s4: optionally underscore with sub |
| bass_mode | deep | s3 atmospheric vs s4 deep |
| mode | base | chain mode: base=init voice, layer=add as extra layer |
| layer_gain | 0.45 | chain layer gain |

### 2. `hybrid-noise-distortion-separate-sub-layer`  (voice)

*Hybrid noise+distortion layer separate from sub/harmonic patch*

Why here: Build a portable hybrid stack: one patch/layer for filtered noise through asymmetric distortion (gritty air/texture) with EQ low-cut and slight top trim, and a separate patch/layer for sub/harmonic tones (e.g. square/WT) so you can retune harmonics or hold a fixed noise pitch without the noise timbre tracking every bass note—then blend; maps to sample/noise + WT + filter hybrid thinking for cinematic beds (not only neuro bass).

| knob | value | grounded in |
|---|---|---|
| noise_level | 0.45 | s1: noise ~50% |
| noise_drive | 0.5 | s2: asymmetric distortion ~50% |
| noise_cut | 2511.5843 | s2: filter noise path mid-high |
| noise_hp | 325.0 | s3: HP into low-mid region |
| sub_wave | pulse | s4: square favoured, or WT |
| sub_oct | 0 | s4: low tones |
| attack | 0.0265 | conv bass |
| decay | 0.65 | conv |
| sustain | 0.65 | conv |
| release | 0.65 | conv |
| sub_cut | 394.7078 | conv |
| for_pads | False | s5/C1: for pads lower distortion, lengthen amps |
| mode | layer | chain mode: base=init voice, layer=add as extra layer |
| layer_gain | 0.45 | chain layer gain |

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

### 4. `traveler-walkthrough-curved-envelope-evolving-pad`  (mod)

*ADBSSR curved-envelope evolving pad*

Why here: Design a long-evolving cinematic pad using multi-stage envelopes with adjustable curve handles, up to ~20s stages, optional breakpoint/slope expansion, and a modulation envelope that can start from alt control (e.g. sustain pedal) instead of note-on.

| knob | value | grounded in |
|---|---|---|
| attack | 3.75 | s2: long stages (up to ~20s; bounded by 6 s note) |
| curve | 2.0 | s1: curve handles (convex) |
| release | 4.0 | s2: long (bounded) |
| fenv_amt | 1.4 | s3: filter env -> stereo LPF moderate |
| fenv_attack | 4.5 | s2/s3: long bloom |
| menv_dest | wt_pos | s3: mod env -> WT pos/pan/second cutoff |
| vib_c | 5.0 | s5: pitch vibrato (cents conv) |
| chorus_mix | 0.2 | s6: light chorus |
| rev_rt60 | 5.5 | s6: long space/hall |
| rev_send | 0.275 | conv |

### 5. `soft-tape-saturation-pads-before-space`  (fx)

*Soft tape/analog saturation on pads before space FX*

Why here: Make digital/synth pads and string layers feel denser and less sterile by adding gentle tape or analog-style saturation early (before big reverb/space): zero-time tape-delay as low-CPU tape sat, or gentle console/tape emulations kept near 0 VU—fullness in low-mids without obvious distortion.

| knob | value | grounded in |
|---|---|---|
| drive | 0.325 | s3: input toward ~0 VU, not into red |
| option | console | s2 A zero-time tape delay vs s3 B console |

## How the search got here

| round | id | mutation | robust (search grid) |
|---|---|---|---|
| 0 | `5ebe7f2e40` | seed | 89.41 |
| 2 | `8124583241` | +traveler-walkthrough-control-track-filter-wt-animation (for M10); M7:keysol..cutoff:250.0->199.2442; M7:keysol..vel_cut:2.75->2.2682; M7:hybrid..noise_cut:3500.0->2511.5843; M7:hybrid..sub_cut:600.0->394.7078 | 96.89 |
| 3 | `8fe4394ed7` | knob traveler..dir_a=pingpong | 96.78 |
| 7 | `f3f6d014ab` | +traveler-walkthrough-stereo-ladder-lf-width | 98.32 |
| 8 | `82661e7281` | +traveler-walkthrough-curved-envelope-evolving-pad | 100.0 |
| 11 | `67af516950` | -traveler-walkthrough-control-track-filter-wt-animation | 100.0 |


## Perceptual check (spectrogram, by eye)

solid centered fundamental + harmonics in Mid; noise layer swells mostly in Side (peak ~4.5 s); no clicks; reads more 'textural sub' than punchy
