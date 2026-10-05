---
schema: AgentConsumableSkill-draft v1
id: workflow-bass-velocity-hybrid-bass
name: "Sample workflow: bass velocity hybrid bass"
domain: cinematic-synth
kind: workflow (ordered chain of library skills)
status: draft — validated offline by sample-lab, not yet reviewed for publish
skills_used: [keysol-venus-velocity-hybrid-bass-impact, hybrid-noise-distortion-separate-sub-layer, traveler-walkthrough-stereo-ladder-lf-width, traveler-walkthrough-curved-envelope-evolving-pad, soft-tape-saturation-pads-before-space]
curriculum_ids: [curriculum-cinematic-hybrid-synth]
---

# Goal
Produce a ship-ready bass sample (48 kHz/24-bit stereo, 8–12 s) for Polyrhythm Studio by firing the library skills
below **in this order**. Original synthesis only (no presets/samples). Passed sample-lab TARGET v1.3 on
12/12 renders (3 note sets × 4 seeds), robust score 100.0.

# Prerequisites
- Offline renderer: `/workspace/skill-library/sample-lab` (`render_system.py bass-velocity-hybrid-bass`), or any synth/Web Audio graph with
  the same modules (multi-osc + unison, ladder/SVF filters, envelopes, LFO/mod matrix, chorus, stereo delay, reverb).

# Inputs
- notes: MIDI chord/notes (category test sets in `engine/render.py:NOTESETS`), seed: integer for random sources.

# Steps
1. **Activate `keysol-venus-velocity-hybrid-bass-impact`** — velocity-rewarding hybrid bass and impact. Apply with: osc=saw, wt_spice=0.15, decay=0.55, sustain=0.525, release=0.55, cutoff=199.2442, vel_cut=2.2682, env_amt=1.75, sub_level=0.4, bass_mode=deep.
2. **Activate `hybrid-noise-distortion-separate-sub-layer`** — Hybrid noise+distortion layer separate from sub/harmonic patch. Apply with: noise_level=0.45, noise_drive=0.5, noise_cut=2511.5843, noise_hp=325.0, sub_wave=pulse, sub_oct=0, attack=0.0265, decay=0.65, sustain=0.65, release=0.65.
3. **Activate `traveler-walkthrough-stereo-ladder-lf-width`** — dual stereo filter and LF-width imaging. Apply with: slope=lp24, stereo_off=0.25, hp=80.0, pan_spread=0.4, lf_width_hz=230.0.
4. **Activate `traveler-walkthrough-curved-envelope-evolving-pad`** — ADBSSR curved-envelope evolving pad. Apply with: attack=3.75, curve=2.0, release=4.0, fenv_amt=1.4, fenv_attack=4.5, menv_dest=wt_pos, vib_c=5.0, chorus_mix=0.2, rev_rt60=5.5, rev_send=0.275.
5. **Activate `soft-tape-saturation-pads-before-space`** — Soft tape/analog saturation on pads before space FX. Apply with: drive=0.325, option=console.
6. Master: loudness-normalize to -14.5 LUFS, true-peak limit at −1.3 dBTP, export.

# Verification
- Run `render_system.py bass-velocity-hybrid-bass --score` → pass=true (TARGET.md v1.3: ≤ −1 dBTP, mono-fold loss, centered lows,
  tilt/balance, no harsh 1/3-oct bump, movement M10/M11, clean tail or seamless loop, deterministic).
- Look at the spectrogram PNG for clicks, aliasing fans, zipper modulation, hiss.

# Outputs
- WAV + spectrogram + score JSON per note set.

# Constraints
- Fire skills in the listed order: later skills refine the same rack slot (e.g. a later reverb skill re-tunes the
  reverb an earlier skill inserted) and FX-order constraints from the skills (sat → EQ → chorus → delay → reverb) hold.
- Knob values stay inside each skill's grounded ranges (see `systems/bass-velocity-hybrid-bass/README.md` for the citation of every value).
