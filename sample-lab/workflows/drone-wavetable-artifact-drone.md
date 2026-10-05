---
schema: AgentConsumableSkill-draft v1
id: workflow-drone-wavetable-artifact-drone
name: "Sample workflow: drone wavetable artifact drone"
domain: cinematic-synth
kind: workflow (ordered chain of library skills)
status: draft — validated offline by sample-lab, not yet reviewed for publish
skills_used: [ambient-organic-pluck-pad-ladder-chorus-space, traveler-walkthrough-stereo-ladder-lf-width, reverb-pads-type-choice-and-send-setup, shimmer-reverb-pitchshift-plus12-feedback, unison-odd-even-detune-width-clean-supersaw]
curriculum_ids: [curriculum-cinematic-hybrid-synth]
---

# Goal
Produce a ship-ready drone sample (48 kHz/24-bit stereo, 8–12 s) for Polyrhythm Studio by firing the library skills
below **in this order**. Original synthesis only (no presets/samples). Passed sample-lab TARGET v1.3 on
12/12 renders (3 note sets × 4 seeds), robust score 98.73.

# Prerequisites
- Offline renderer: `/workspace/skill-library/sample-lab` (`render_system.py drone-wavetable-artifact-drone`), or any synth/Web Audio graph with
  the same modules (multi-osc + unison, ladder/SVF filters, envelopes, LFO/mod matrix, chorus, stereo delay, reverb).

# Inputs
- notes: MIDI chord/notes (category test sets in `engine/render.py:NOTESETS`), seed: integer for random sources.

# Steps
1. **Activate `ambient-organic-pluck-pad-ladder-chorus-space`** — Organic ambient pluck-pad with ladder, velocity, chorus-space. Apply with: decay=0.9, sustain=0.4, release=0.7, warp=0.275, cutoff=650.0, env_amt=1.9, res=0.1, env2_decay=0.425, dist_drive=0.4, dist_mix=0.225.
2. **Activate `traveler-walkthrough-stereo-ladder-lf-width`** — dual stereo filter and LF-width imaging. Apply with: slope=lp24, stereo_off=0.25, hp=80.0, pan_spread=0.4, lf_width_hz=207.0521.
3. **Activate `reverb-pads-type-choice-and-send-setup`** — Reverb for pads: pick type by texture, then set up 100%-wet EQ'd send returns. Apply with: type=hall, hall_rt60=3.25, plate_rt60=6.0, room_rt60=1.0, predelay=0.025, return_hp=250.0, send=0.275, high_cut=0.
4. **Activate `shimmer-reverb-pitchshift-plus12-feedback`** — Shimmer reverb: +12st pitch-shift into lush space. Apply with: rt60=5.5, feedback=0.4, delay_s=0.25, echo_hp=300.0, echo_lp=5500.0, wet_hp=275.0, send=0.21.
5. **Activate `unison-odd-even-detune-width-clean-supersaw`** — Unison voicing: odd vs even voice counts, detune/blend/width, clean supersaw. Apply with: voices=7, detune=0.2, blend=0.5, width=0.4774, oscb=True, oscb_oct=1, oscb_level=0.4, sub_level=0.3, noise_level=0.04, eq_hp=115.0.
6. Master: loudness-normalize to -15.5 LUFS, true-peak limit at −1.3 dBTP, export.

# Verification
- Run `render_system.py drone-wavetable-artifact-drone --score` → pass=true (TARGET.md v1.3: ≤ −1 dBTP, mono-fold loss, centered lows,
  tilt/balance, no harsh 1/3-oct bump, movement M10/M11, clean tail or seamless loop, deterministic).
- Look at the spectrogram PNG for clicks, aliasing fans, zipper modulation, hiss.

# Outputs
- WAV + spectrogram + score JSON per note set.

# Constraints
- Fire skills in the listed order: later skills refine the same rack slot (e.g. a later reverb skill re-tunes the
  reverb an earlier skill inserted) and FX-order constraints from the skills (sat → EQ → chorus → delay → reverb) hold.
- Knob values stay inside each skill's grounded ranges (see `systems/drone-wavetable-artifact-drone/README.md` for the citation of every value).
