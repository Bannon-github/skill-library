---
schema: AgentConsumableSkill-draft v1
id: workflow-pluck-organic-velocity-pluck
name: "Sample workflow: pluck organic velocity pluck"
domain: cinematic-synth
kind: workflow (ordered chain of library skills)
status: draft — validated offline by sample-lab, not yet reviewed for publish
skills_used: [ambient-organic-pluck-pad-ladder-chorus-space, keysol-venus-high-wt-artifact-pulse-layer, traveler-walkthrough-stereo-ladder-lf-width, stereo-delay-pingpong-dual-parallel-two-tap, reverb-pads-type-choice-and-send-setup, traveler-walkthrough-fx-eq-chorus-delay-reverb, unison-odd-even-detune-width-clean-supersaw]
curriculum_ids: [curriculum-cinematic-hybrid-synth]
---

# Goal
Produce a ship-ready pluck sample (48 kHz/24-bit stereo, 8–12 s) for Polyrhythm Studio by firing the library skills
below **in this order**. Original synthesis only (no presets/samples). Passed sample-lab TARGET v1.3 on
12/12 renders (3 note sets × 4 seeds), robust score 97.66.

# Prerequisites
- Offline renderer: `/workspace/skill-library/sample-lab` (`render_system.py pluck-organic-velocity-pluck`), or any synth/Web Audio graph with
  the same modules (multi-osc + unison, ladder/SVF filters, envelopes, LFO/mod matrix, chorus, stereo delay, reverb).

# Inputs
- notes: MIDI chord/notes (category test sets in `engine/render.py:NOTESETS`), seed: integer for random sources.

# Steps
1. **Activate `ambient-organic-pluck-pad-ladder-chorus-space`** — Organic ambient pluck-pad with ladder, velocity, chorus-space. Apply with: decay=0.9, sustain=0.4, release=0.7, warp=0.275, cutoff=517.5041, env_amt=2.0, res=0.1, env2_decay=0.425, dist_drive=0.4, dist_mix=0.225.
2. **Activate `keysol-venus-high-wt-artifact-pulse-layer`** — high-pitch wavetable artifact over pulse sequence. Apply with: oct=2, level=0.08, wt_lfo_amt=0.275, wt_lfo_rate=0.09.
3. **Activate `traveler-walkthrough-stereo-ladder-lf-width`** — dual stereo filter and LF-width imaging. Apply with: slope=lp24, stereo_off=0.25, hp=80.0, pan_spread=0.4, lf_width_hz=230.0.
4. **Activate `stereo-delay-pingpong-dual-parallel-two-tap`** — Stereo delay motion: ping-pong, dual-parallel, two-tap, cross-feedback. Apply with: topology=pingpong, sync=1/4, feedback=0.45, mix=0.2, sat=0.1, cross=0.15, mod_depth=0.0015.
5. **Activate `reverb-pads-type-choice-and-send-setup`** — Reverb for pads: pick type by texture, then set up 100%-wet EQ'd send returns. Apply with: type=room, hall_rt60=3.25, plate_rt60=6.0, room_rt60=1.0, predelay=0.025, return_hp=250.0, send=0.275, high_cut=0.
6. **Activate `traveler-walkthrough-fx-eq-chorus-delay-reverb`** — EQ chorus dual-delay multi-algo reverb FX chain. Apply with: low_db=-0.5, mid_db=1.0, high_db=1.0, chorus_mix=0.225, delay=pingpong, dly_mix=0.17, rev=hall, rev_send=0.275.
7. **Activate `unison-odd-even-detune-width-clean-supersaw`** — Unison voicing: odd vs even voice counts, detune/blend/width, clean supersaw. Apply with: voices=7, detune=0.2, blend=0.5, width=0.5, oscb=True, oscb_oct=1, oscb_level=0.4, sub_level=0.3, noise_level=0.04, eq_hp=115.0.
8. Master: loudness-normalize to -15.5 LUFS, true-peak limit at −1.3 dBTP, export.

# Verification
- Run `render_system.py pluck-organic-velocity-pluck --score` → pass=true (TARGET.md v1.3: ≤ −1 dBTP, mono-fold loss, centered lows,
  tilt/balance, no harsh 1/3-oct bump, movement M10/M11, clean tail or seamless loop, deterministic).
- Look at the spectrogram PNG for clicks, aliasing fans, zipper modulation, hiss.

# Outputs
- WAV + spectrogram + score JSON per note set.

# Constraints
- Fire skills in the listed order: later skills refine the same rack slot (e.g. a later reverb skill re-tunes the
  reverb an earlier skill inserted) and FX-order constraints from the skills (sat → EQ → chorus → delay → reverb) hold.
- Knob values stay inside each skill's grounded ranges (see `systems/pluck-organic-velocity-pluck/README.md` for the citation of every value).
