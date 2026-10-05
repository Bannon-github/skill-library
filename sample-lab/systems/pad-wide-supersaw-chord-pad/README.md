# pad-wide-supersaw-chord-pad

Category: **pad** · found in round 8 · chain id `144a34381b`

**Firing order:** `warm-heavenly-supersaw-pad-keytrack-fx` → `unison-odd-even-detune-width-clean-supersaw` → `traveler-walkthrough-stereo-ladder-lf-width`

**Scores (TARGET v1.3):** search grid 6/6 pass, robust 100.0; extended grid (3 note sets × 4 seeds) **12/12 pass**, robust **100.0**, mean 100.0, deterministic: True

Typical metric values (note set 0, seed 11): M1=-15.5, M2=0.4812, M3=0.7739, M4=0.3582, M5=-18.0099, M6=-5.7692, M7=4.8717, M8=1.1392, M9=-16.2362, M12=-26.3106, M10=0.2527, M11=0.2505, M13=0.0, M14=-0.0

Advisory (not scored): sub-30 Hz energy -56.2 dB re total.

Renders: [pad-wide-supersaw-chord-pad__50-53-57-64_seed11.wav](pad-wide-supersaw-chord-pad__50-53-57-64_seed11.wav), [pad-wide-supersaw-chord-pad__53-57-60-64_seed11.wav](pad-wide-supersaw-chord-pad__53-57-60-64_seed11.wav), [pad-wide-supersaw-chord-pad__45-52-57-60_seed11.wav](pad-wide-supersaw-chord-pad__45-52-57-60_seed11.wav) (spectrogram PNG alongside each).

Re-render: `.venv/bin/python render_system.py pad-wide-supersaw-chord-pad --notes 50,53,57,64 --seed 11 --score --spectrogram`

## Steps (sequential skill activation)

### 1. `warm-heavenly-supersaw-pad-keytrack-fx`  (voice)

*Warm heavenly supersaw pad with keytrack and lush FX*

Why here: Dial warm heavenly pads: saw unison 5–7 with moderated detune, slow attack/long release (velocity can shorten attack), 24 dB low-pass with no resonance and key tracking, subtle slow LFO→cutoff, rich chorus + low-cut reverb (~3s) + dotted-eighth stereo delay; optional PWM layer, serial HP to control sub build-up, sine reinforce, and a separate shimmer layer.

| knob | value | grounded in |
|---|---|---|
| voices | 6 | s1: saw unison ~5-7 |
| detune | 0.175 | s1: reduce detune from max (conv moderate) |
| attack | 2.25 | s1: slow attack (conv) |
| release | 3.25 | s1: long release (conv) |
| cutoff | 1050.0 | s3: 24 dB LP, cutoff for warm lows (Hz conv) |
| keytrack | 0.75 | s3/C1: key track until high notes audible |
| filter_model | ladder | s3: compare analog/ladder/diode |
| lfo_rate | 0.19 | s5: subtle slow irregular LFO |
| lfo_amt | 0.325 | s5: subtle -> cutoff |
| chorus_mix | 0.425 | s4: rich chorus |
| rev_rt60 | 3.0 | s4: reverb ~3s |
| rev_hp | 225.0 | s4: reverb low cut |
| rev_send | 0.275 | conv moderate |
| dly_fb | 0.375 | s4: controlled feedback |
| dly_mix | 0.16 | conv moderate |
| pwm_layer | False | s6: optional PWM layer, less unison |
| serial_hp | True | s6: serial HP after LP if subs build |
| sine_reinforce | False | s6: optional unfiltered sine reinforce |
| mode | base | chain mode: base=init voice, layer=add as extra layer |
| layer_gain | 0.45 | chain layer gain |

### 2. `unison-odd-even-detune-width-clean-supersaw`  (voice)

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

## How the search got here

| round | id | mutation | robust (search grid) |
|---|---|---|---|
| 0 | `b70dd901a1` | seed | 100.0 |
| 1 | `144a34381b` | -midside-eq-bass-focus-width-depth | 100.0 |


## Perceptual check (spectrogram, by eye)

clean dense sustain, smooth release decay after note-off; no clicks/aliasing lines; very bright air up to 20 kHz
