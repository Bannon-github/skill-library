---
schema: AgentConsumableSkill-draft v1
id: workflow-gated-fifth-swell-trance-gate
name: "Sample workflow: gated fifth swell trance gate"
domain: cinematic-synth
kind: workflow (ordered chain of library skills)
status: draft — validated offline by sample-lab, not yet reviewed for publish
skills_used: [evolving-pad-unison-filter-swell-fifth, trance-gate-sidechain-chop-texture, traveler-walkthrough-stereo-ladder-lf-width, traveler-walkthrough-super-unison-wide-lead, traveler-walkthrough-fx-eq-chorus-delay-reverb]
curriculum_ids: [curriculum-cinematic-hybrid-synth]
---

# Goal
Produce a ship-ready gated sample (48 kHz/24-bit stereo, 8–12 s) for Polyrhythm Studio by firing the library skills
below **in this order**. Original synthesis only (no presets/samples). Passed sample-lab TARGET v1.3 on
12/12 renders (3 note sets × 4 seeds), robust score 98.83.

# Prerequisites
- Offline renderer: `/workspace/skill-library/sample-lab` (`render_system.py gated-fifth-swell-trance-gate`), or any synth/Web Audio graph with
  the same modules (multi-osc + unison, ladder/SVF filters, envelopes, LFO/mod matrix, chorus, stereo delay, reverb).

# Inputs
- notes: MIDI chord/notes (category test sets in `engine/render.py:NOTESETS`), seed: integer for random sources.

# Steps
1. **Activate `evolving-pad-unison-filter-swell-fifth`** — Evolving unison pad with filter swell and fifth layer. Apply with: amp_attack=0.05, release=3.5, env2_attack=2.0, cutoff=700.0, env_amt=4.0, res=0.1, voices=7, width=0.85, detune=0.21, lfo_amt=0.25.
2. **Activate `trance-gate-sidechain-chop-texture`** — Trance-gate: sidechain-gate chop a sustained pad. Apply with: pattern=[1, 1, 1, 0], release=0.12, hold=0.575, power_chord=False, post_reverb=True, post_send=0.225.
3. **Activate `traveler-walkthrough-stereo-ladder-lf-width`** — dual stereo filter and LF-width imaging. Apply with: slope=lp24, stereo_off=0.25, hp=80.0, pan_spread=0.4, lf_width_hz=230.0.
4. **Activate `traveler-walkthrough-super-unison-wide-lead`** — super-unison wide stereo lead (osc2 stack). Apply with: wave_pos=0.125, voices=6, detune=0.3, width=0.9, drive=0.2, cutoff=6396.7421, slope=lp12, res=0.175, attack=0.9706, sustain=0.8.
5. **Activate `traveler-walkthrough-fx-eq-chorus-delay-reverb`** — EQ chorus dual-delay multi-algo reverb FX chain. Apply with: low_db=-0.7341, mid_db=1.0, high_db=0.1687, chorus_mix=0.225, delay=dual, dly_mix=0.17, rev=hall, rev_send=0.275.
6. Master: loudness-normalize to -15.5 LUFS, true-peak limit at −1.3 dBTP, export.

# Verification
- Run `render_system.py gated-fifth-swell-trance-gate --score` → pass=true (TARGET.md v1.3: ≤ −1 dBTP, mono-fold loss, centered lows,
  tilt/balance, no harsh 1/3-oct bump, movement M10/M11, clean tail or seamless loop, deterministic).
- Look at the spectrogram PNG for clicks, aliasing fans, zipper modulation, hiss.

# Outputs
- WAV + spectrogram + score JSON per note set.

# Constraints
- Fire skills in the listed order: later skills refine the same rack slot (e.g. a later reverb skill re-tunes the
  reverb an earlier skill inserted) and FX-order constraints from the skills (sat → EQ → chorus → delay → reverb) hold.
- Knob values stay inside each skill's grounded ranges (see `systems/gated-fifth-swell-trance-gate/README.md` for the citation of every value).
