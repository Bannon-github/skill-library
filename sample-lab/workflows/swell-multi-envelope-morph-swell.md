---
schema: AgentConsumableSkill-draft v1
id: workflow-swell-multi-envelope-morph-swell
name: "Sample workflow: swell multi envelope morph swell"
domain: cinematic-synth
kind: workflow (ordered chain of library skills)
status: draft — validated offline by sample-lab, not yet reviewed for publish
skills_used: [cinematic-multi-envelope-osc-level-morph, traveler-walkthrough-stereo-ladder-lf-width, keysol-venus-high-wt-artifact-pulse-layer, chorus-ensemble-classic-vibrato-pad-modes, stereo-delay-pingpong-dual-parallel-two-tap, mix-pads-role-eq-width-clarity, traveler-walkthrough-super-unison-wide-lead, unison-odd-even-detune-width-clean-supersaw]
curriculum_ids: [curriculum-cinematic-hybrid-synth]
---

# Goal
Produce a ship-ready swell sample (48 kHz/24-bit stereo, 8–12 s) for Polyrhythm Studio by firing the library skills
below **in this order**. Original synthesis only (no presets/samples). Passed sample-lab TARGET v1.3 on
12/12 renders (3 note sets × 4 seeds), robust score 100.0.

# Prerequisites
- Offline renderer: `/workspace/skill-library/sample-lab` (`render_system.py swell-multi-envelope-morph-swell`), or any synth/Web Audio graph with
  the same modules (multi-osc + unison, ladder/SVF filters, envelopes, LFO/mod matrix, chorus, stereo delay, reverb).

# Inputs
- notes: MIDI chord/notes (category test sets in `engine/render.py:NOTESETS`), seed: integer for random sources.

# Steps
1. **Activate `cinematic-multi-envelope-osc-level-morph`** — Multi-envelope oscillator-level morphing pad. Apply with: release=4.5, a1=0.35, a2=1.85, a3=3.5, oct3=1, pan_amt=0.35, res=0.075, noise_level=0.065, wt_sync=1bar, rev_rt60=6.5.
2. **Activate `traveler-walkthrough-stereo-ladder-lf-width`** — dual stereo filter and LF-width imaging. Apply with: slope=lp24, stereo_off=0.25, hp=80.0, pan_spread=0.4, lf_width_hz=230.0.
3. **Activate `keysol-venus-high-wt-artifact-pulse-layer`** — high-pitch wavetable artifact over pulse sequence. Apply with: oct=2, level=0.08, wt_lfo_amt=0.275, wt_lfo_rate=0.09.
4. **Activate `chorus-ensemble-classic-vibrato-pad-modes`** — Chorus-Ensemble modes: Classic, Ensemble, Vibrato. Apply with: mode=ensemble, rate=0.5, depth_ms=2.0445, feedback=0.15, wet_hp=275.0, width=0.9, mix=0.375.
5. **Activate `stereo-delay-pingpong-dual-parallel-two-tap`** — Stereo delay motion: ping-pong, dual-parallel, two-tap, cross-feedback. Apply with: topology=pingpong, sync=1/4, feedback=0.45, mix=0.2, sat=0.1, cross=0.171, mod_depth=0.0015.
6. **Activate `mix-pads-role-eq-width-clarity`** — Mix pads for role, EQ clarity, energy, and width control. Apply with: role=lead_bed, hp=120.0, return_hp=150.0, narrow_hz=225.0.
7. **Activate `traveler-walkthrough-super-unison-wide-lead`** — super-unison wide stereo lead (osc2 stack). Apply with: wave_pos=0.125, voices=6, detune=0.3, width=0.9, drive=0.2, cutoff=3099.2663, slope=lp12, res=0.175, attack=0.65, sustain=0.8.
8. **Activate `unison-odd-even-detune-width-clean-supersaw`** — Unison voicing: odd vs even voice counts, detune/blend/width, clean supersaw. Apply with: voices=7, detune=0.2, blend=0.5, width=0.5, oscb=True, oscb_oct=1, oscb_level=0.4, sub_level=0.3, noise_level=0.04, eq_hp=115.0.
9. Master: loudness-normalize to -15.5 LUFS, true-peak limit at −1.3 dBTP, export.

# Verification
- Run `render_system.py swell-multi-envelope-morph-swell --score` → pass=true (TARGET.md v1.3: ≤ −1 dBTP, mono-fold loss, centered lows,
  tilt/balance, no harsh 1/3-oct bump, movement M10/M11, clean tail or seamless loop, deterministic).
- Look at the spectrogram PNG for clicks, aliasing fans, zipper modulation, hiss.

# Outputs
- WAV + spectrogram + score JSON per note set.

# Constraints
- Fire skills in the listed order: later skills refine the same rack slot (e.g. a later reverb skill re-tunes the
  reverb an earlier skill inserted) and FX-order constraints from the skills (sat → EQ → chorus → delay → reverb) hold.
- Knob values stay inside each skill's grounded ranges (see `systems/swell-multi-envelope-morph-swell/README.md` for the citation of every value).
