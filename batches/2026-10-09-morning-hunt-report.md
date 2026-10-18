# Morning synth YouTube hunt — 2026-10-09 (PT)

## Counts
- MCP before: 95 → after: 103
- New skills: 8
- Rejected: 11 (+1 stopped: no usable transcript)
- Pivoted to crypto/side-hustle: no (synth returns not exhausted)

## New skill IDs
- `casio-pd-piecewise-phase-warp-cosine-to-saw` ← `EW12RYc7QRA` (Casio CZ-style piecewise phase warp of a cosine into a modulatable saw (DCW node) without a filter)
- `casio-pd-wave-family-and-windowed-sync-resonance` ← `94vSgZXg1nQ` (CZ wave family (saw-pulse, double-sine, pulse, square) plus windowed-sync resonance and unison fattening)
- `phase-distortion-shapes-modular-phase-chain` ← `TrkXgDQbhjk` (Rebuild CZ-like PD shapes with external phase + skew/formant/sync/fold; EG on shape)
- `hard-sync-master-slave-mod-envelope-timbre` ← `C_d3SCz2u-c` (Hard sync lead: master pitch, slave timbre, mod-envelope on slave pitch)
- `uplifter-downlifter-pitchbend-filter-lfo` ← `t97TU3p7-kE` (Uplifter/downlifter via pitch-bend span, closed LP, accelerating LFO, unison, sidechain)
- `sub-drop-sine-freq-glide-80hz-to-20hz` ← `FULqquC3-Fc` (Custom sub-drop: automate sine ~80→20 Hz with bypass window and optional saturation)
- `fm-stack-uplifter-pitch-env-noise-swell` ← `G4Tc59aAeoE` (FM operator-stack uplifter with long pitch env and synced noise/FM swell)
- `cinematic-bass-distortion-stack-pitch-bend-downer` ← `PUBMG__czwg` (WT+sub through stacked distortion/compression bed, then pitch-bend braam/downer curves)

## Rejects
- `hlgl5lfdv48` Thin hardware overview (2 outline steps); no portable oscillator recipe. Prefer GroovyDSP PD skills.
- `vyZBa1eGvBs` Sample-download/arrangement tour, not synth recipe; transcript contains shared site logins (not republished). Covered by new uplifter + sub-drop skills.
- `2dtxabrZ8Wg` Thin (2 steps: bounce into noise osc). Prefer uplifter-downlifter-pitchbend-filter-lfo.
- `WZt_nok-ipk` Near-duplicate of whoosh + braam skills; remaining delta is DAW resample-into-sampler workflow.
- `It5a3bhLEb8` Covered by noise-layer-whoosh-doppler-and-rising-variants.
- `4rp4ZepdzoA` Product patch demo pointing to GroovyDSP; covered by new Casio PD skills.
- `lE_CG3bagwg` Overlaps warp-modes + new modular PD shapes skill; no unique CZ wave-family/windowed-sync delta.
- `acZPLjnha9o` Covered by existing braam skill / new cinematic-bass distortion bed.
- `gRh9BL-W8kQ` Low delta vs hybrid-noise-distortion and pulse/impact skills.
- `beZpH9X850s` Machine-translated sync basics; covered by hard-sync-master-slave-mod-envelope-timbre.
- `Vp66dS7o3R0` Covered by uplifter-downlifter-pitchbend-filter-lfo.

## Stopped (no transcript / translation)
- `mUDhWFNKO-Q` STOP_no_transcript_asr_flagged: Downlifter Idea

## Pipeline notes
- Pipeline .venv present; ran scripts/ensure_env.sh (all envs ok, argos packs de/es/ja/fr/pt/it).
- route.py --domain synth again returned COVERED for many real gaps (PD, uplifters, sub-drops, hard sync). Hand-checked against mcp-publish; distilled 8 gap skills anyway. COVERED remains unreliable for terms missing from the synth lexicon.
- Priority backlog from Oct 7 addressed: Casio PD (EW12RYc7QRA + 94vSgZXg1nQ), windowed-sync resonance (inside wave-family skill), uplifter/downlifter, sub-drop sine glide, hard sync. lE_CG3bagwg routed but rejected as overlap after modular PD skill.
- Windowed-sync dedicated search returned 0 kept videos; windowed-sync content came from GroovyDSP 'More Phase Distortion' resonance-wave section.
- Quality --strict: all 8 new skills clean (0 warnings). Novelty NOVEL for all 8 (max local overlap 0.118).
- Merged 8 skills into LIBRARY.json (+8 video entries → 97), topics/taxonomy.json cinematic-hybrid-synth (61→69 skill_ids), curriculum-cinematic-hybrid-synth level 3, and skills/<id>.md. Older backlog (Oct 5/6 taxonomy gaps) still not fully backfilled.
- Git sync skipped: no credentials on the box (no GH_TOKEN/GITHUB_TOKEN, gh not logged in).
- Deferred queue still empty; upgrade_to_tlang still has MH7YiOWQIhI, kHWOIE4YTZ4, BqE9S27CZfY (+ beZpH9X850s noted this run).

## Still thin for later hunts
- Deeper windowed-sync DSP (window shapes beyond decaying-sine envelope) — only approximate in 94vSgZXg1nQ
- Phase-distortion resonant-wave variants / wave alternation as a standalone performable skill (mentioned in 94vSgZXg1nQ but thin)
- Impact/boom from layered noise+pitch without overlapping braam/sub-drop skills
- More hybrid pad morphs if lexicon/COVERED improves
