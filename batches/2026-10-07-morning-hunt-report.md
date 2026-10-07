# Morning synth YouTube hunt — 2026-10-07 (PT)

## Counts
- MCP before: 88 → after: 95
- New skills: 7
- Rejected: 8 (+4 stopped: no usable transcript)
- Pivoted to crypto/side-hustle: no (synth returns not exhausted)

## New skill IDs
- `asymmetric-left-right-processing-width-mono-safe` ← `Z2mgB3LYkgQ` (width delta: different L/R sources/EQ, one-sided saturation, formant-shifted duplicate, 50/75 ms slap, Haas+distortion only in a parallel blend beside a dry chain, mono-sum checks)
- `brooding-pw-drone-detuned-octave-stack-split-bend` ← `DFLshMLKkHE` (brooding drone: 3 PW-morph squares (two -12 st nudged sharp/flat, one 4-voice wide), vibrato on one osc, LFO on PW morph, 12 dB LP on mod wheel, reverb + filtered delay, per-osc pitch-wheel depth spread)
- `noise-layer-whoosh-doppler-and-rising-variants` ← `uFk9xUVg7Q0` (whooshes from printed noise + texture + HPF'd synth layers on one bus: swell envelope, Doppler pass-by, compress/limit -0.2 dB; rising-only pitch-shift + narrow EQ sweep variant; mod-wheel filter/noise/flanger performable whoosh)
- `pitch-ramp-riser-resonant-smear-filter-reverb` ← `9v-p2k8Nnec` (synth riser: saw, +-12 bend ramp over the clip with reset points, low-set high-resonance smear (comb/allpass-style) filter + slight LFO + reverb so the pitch isn't out-of-key obvious)
- `reverse-reverb-swell-print-reverse-print` ← `DpXw9UPrTDU` (manual reverse-reverb swell: duplicate, reverse, print 100%-wet large reverb, keep lead-in, re-reverse, normalize, align + fades, optional late-automated tail reverb)
- `shepard-tone-endless-riser-octave-crossfade-voices` ← `YvUbr8GaqUo` (endless Shepard riser: 3 mono voices, full-clip bend ramp, transposed by sweep span, top fades out/bottom fades in, group reverb hides reset; noise comb-filter variant with 4 staggered 25% fades)
- `warp-modes-as-phase-signal-transforms` ← `D4K5g8t3aIc` (warp modes rebuilt as phase-ramp transforms: PWM squeeze, bend/asym pinch-skew, mirror, sync wrap + window, comparator flip, quantize, remap curve; chainable in an AudioWorklet)

## Rejects
- `CKXV--9u5A4` Product-locked click path: recreates one synth's warp modes by hand-drawing helper wavetables in another plugin's editor (keyframe/point positions); the portable concepts are covered by warp-modes-as-phase-signal-transforms (D4K5g8t3aIc).
- `ZXhm-j0T3xo` Near-duplicate/promo: single-mode tour of a remap warp curve, covered by the new warp-modes skill; ends in store promo.
- `IvzsnMV0Cog` Near-duplicate: audio-source Shepard tone via pitch-shifted clip pairs uses the same octave-crossfade principle as shepard-tone-endless-riser-octave-crossfade-voices; remaining delta is DAW-specific fade/loop editing.
- `9V56-jd48_k` Thin/overlap: synth wind = noise -> 12 dB low-pass + slow, very light random cutoff LFO + delay/reverb + low-mid boost; already covered by hybrid-noise-distortion-separate-sub-layer and the new whoosh skill.
- `Ku3-RjDV3g8` Off-domain/thin: whooshes mostly from mic/field recording (mouth, swung objects, car pass-bys); synth part is one sentence.
- `MKgCvLOLdNk` Promo/near-duplicate: reverse-reverb vocal intro inside an EDM masterclass excerpt (mostly music, ends in subscription promo); same procedure as reverse-reverb-swell-print-reverse-print.
- `K4osI9yrQQY` Near-duplicate: same manual reverse-reverb procedure as DpXw9UPrTDU (English text is from the AI-dub track of a German video).
- `iFkph3sCmw0` Low delta: dark ambience (detuned sines -> distortion -> 100% wet reverb -> low-pass, tiny slow LFO on pitch/filter, stacked reverbs, layered pitched-down recordings, reversed bounce) overlaps existing pad/reverb/lo-fi skills.

## Stopped (no transcript / translation)
- `QZYa8lZeopk` STOP_translation_failed: Korean auto transcript only; argos ko->en pack not installed (not in the 6 installed packs).
- `Pyys6SsYn1g` STOP_no_transcript_asr_flagged: no transcript track (ASR not run).
- `Q7Pfza8--ZA` STOP_no_transcript_asr_flagged: no transcript track (ASR not run).
- `W8lublzkDtI` STOP_no_transcript_asr_flagged: no transcript track (ASR not run).

## Pipeline notes
- Pipeline .venv present at start; ran scripts/ensure_env.sh (all envs ok, argos packs de/es/ja/fr/pt/it).
- route.py --domain synth returned COVERED for every fetched video (15 routed with usable transcripts). All were checked by hand against mcp-publish; 7 had real gaps (warp modes, Shepard, risers, whooshes, reverse reverb, PW drone, L/R width). The synth lexicon is missing these terms, so COVERED stays unreliable.
- Reworded warp-mode search ('vital warp modes explained sync bend pwm') worked this time: D4K5g8t3aIc and CKXV--9u5A4.
- Operator typo: routed 'Q7pfza8--ZA' (wrong case) -> STOP_video_unavailable; removed its raw/ stub and re-routed the correct id Q7Pfza8--ZA (no transcript). A stray entry may remain in pipeline/logs/route.jsonl and knowledge/graph.json.
- QZYa8lZeopk needs argos ko->en (translate_transcript.py --install-langs ko) if wanted later.
- Quality check across all 95 published skills: 0 failed, 28 warnings (pre-existing, non-strict). The 7 new skills pass --strict with no warnings; novelty verdict NOVEL for all 7 (max local overlap 0.13).
- Merged the 7 new skills into LIBRARY.json (+7 entries, merge_log), topics/taxonomy.json (cinematic-hybrid-synth), curriculum-cinematic-hybrid-synth level 3, and skills/<id>.md. Skills published 2026-10-05/06 (and some earlier ones) are still missing from taxonomy/curriculum: backlog not touched.
- Git sync skipped: no credentials on the box (no GH_TOKEN/GITHUB_TOKEN, no credential helper, gh not logged in).

## Still thin for later hunts
- Phase-distortion (Casio-style) oscillator walkthroughs, e.g. EW12RYc7QRA and lE_CG3bagwg (found, not routed)
- Uplifter/downlifter + sub-drop synth recipes (the best hit W8lublzkDtI has no transcript)
- Windowed-sync emulation details (only approximate in source)
- Synth-built impacts/booms (sub-drop pitch envelope)
