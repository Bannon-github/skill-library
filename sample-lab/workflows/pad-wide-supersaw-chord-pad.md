---
schema: AgentConsumableSkill-draft v1
id: workflow-pad-wide-supersaw-chord-pad
name: "Sample workflow: pad wide supersaw chord pad"
domain: cinematic-synth
kind: workflow (ordered chain of library skills)
status: draft — validated offline by sample-lab, not yet reviewed for publish
skills_used: [warm-heavenly-supersaw-pad-keytrack-fx, unison-odd-even-detune-width-clean-supersaw, traveler-walkthrough-stereo-ladder-lf-width]
curriculum_ids: [curriculum-cinematic-hybrid-synth]
---

# Goal
Produce a ship-ready pad sample (48 kHz/24-bit stereo, 8–12 s) for Polyrhythm Studio by firing the library skills
below **in this order**. Original synthesis only (no presets/samples). Passed sample-lab TARGET v1.3 on
12/12 renders (3 note sets × 4 seeds), robust score 100.0.

# Prerequisites
- Offline renderer: `/workspace/skill-library/sample-lab` (`render_system.py pad-wide-supersaw-chord-pad`), or any synth/Web Audio graph with
  the same modules (multi-osc + unison, ladder/SVF filters, envelopes, LFO/mod matrix, chorus, stereo delay, reverb).

# Inputs
- notes: MIDI chord/notes (category test sets in `engine/render.py:NOTESETS`), seed: integer for random sources.

# Steps
1. **Activate `warm-heavenly-supersaw-pad-keytrack-fx`** — Warm heavenly supersaw pad with keytrack and lush FX. Apply with: voices=6, detune=0.175, attack=2.25, release=3.25, cutoff=1050.0, keytrack=0.75, filter_model=ladder, lfo_rate=0.19, lfo_amt=0.325, chorus_mix=0.425.
2. **Activate `unison-odd-even-detune-width-clean-supersaw`** — Unison voicing: odd vs even voice counts, detune/blend/width, clean supersaw. Apply with: voices=7, detune=0.2, blend=0.5, width=0.5, oscb=True, oscb_oct=1, oscb_level=0.4, sub_level=0.3, noise_level=0.04, eq_hp=115.0.
3. **Activate `traveler-walkthrough-stereo-ladder-lf-width`** — dual stereo filter and LF-width imaging. Apply with: slope=lp24, stereo_off=0.25, hp=80.0, pan_spread=0.4, lf_width_hz=230.0.
4. Master: loudness-normalize to -15.5 LUFS, true-peak limit at −1.3 dBTP, export.

# Verification
- Run `render_system.py pad-wide-supersaw-chord-pad --score` → pass=true (TARGET.md v1.3: ≤ −1 dBTP, mono-fold loss, centered lows,
  tilt/balance, no harsh 1/3-oct bump, movement M10/M11, clean tail or seamless loop, deterministic).
- Look at the spectrogram PNG for clicks, aliasing fans, zipper modulation, hiss.

# Outputs
- WAV + spectrogram + score JSON per note set.

# Constraints
- Fire skills in the listed order: later skills refine the same rack slot (e.g. a later reverb skill re-tunes the
  reverb an earlier skill inserted) and FX-order constraints from the skills (sat → EQ → chorus → delay → reverb) hold.
- Knob values stay inside each skill's grounded ranges (see `systems/pad-wide-supersaw-chord-pad/README.md` for the citation of every value).
