# Morning synth YouTube hunt — 2026-10-21 (PT)

## Counts
- MCP count: 168 → 175. LIBRARY entries 166 → 173. Taxonomy cinematic-hybrid-synth 132 → 139; curriculum level 3 101 → 108.
- New skills: 7 (5 from the 10-20 rate-limited prechecks / router-COVERED hand-checks, 2 from today's searches). Rejected or skipped: 11 (6 rejected on content, 5 with transcripts disabled). Searches: 7 run (5 carryover + 2 fresh), no rate limit during search; the limit returned during the follow-up transcript fetches. Crypto pivot: no.

## New skill IDs
- `dual-euclidean-pulse-generators-boolean-or-xor-and-sub-rotation-track-rotate-print-to-steps-melodic-redistribute-arp-fill` ← WeOuxcN0pV8 (carryover precheck)
- `generative-rhythmic-sequence-euclid-length-phase-against-step-count-chance-rests-random-octave-degree-random-accent-release-smooth-random-filter-wt` ← mb3yqXO9JiE (carryover precheck)
- `eight-layer-euclidean-weaver-drum-or-scale-melody-mode-one-scale-note-per-layer-steps-pulses-rotation-gate-drift-randomize-keep-rhythm-change-scale` ← UchJGizLiLM (carryover precheck; script promo but portable recipe)
- `classic-house-pad-ext-chords-16-voice-free-run-unison-width-vs-chorus-resonant-lp-plus-hp-slow-lfo-cutoff-slow-amp-noise-bypass-filter-chord-stab-loop-pad` ← nbS1pT8V7YU (router COVERED; false positive)
- `piano-resonance-multimic-contact-plus-air-mics-blend-sampler-then-paulstretch-fft-size-tonal-noise-extreme-stretch-and-sample-to-wavetable-patches` ← bIbOgZn1h_Y (carryover precheck; first Paulstretch / extreme-stretch skill)
- `risset-rhythm-endless-accelerando-tempo-doubling-fade-every-other-subdivision-half-and-third-speed-hemiola-layers-rising-gliss-dissonance` ← Z-VjDxckkg8 (fresh: shepard search; first Risset-rhythm skill)
- `tame-generative-sequencer-constrain-scale-octave-phrase-zero-global-random-restart-points-fewer-pitches-pulses-manual-cycle-variations-random-on-last-notes` ← gyhfAdy6eq8 (fresh: euclidean search)

## Rejects / skipped
- Content: rVRMgLa9Y9E (router COVERED, hand-checked: orchestration advice, near-dup of hybrid-score layering), P_bIEn8FGzI (router COVERED, hand-checked: thin live-stream noodling), PP6dAPAhIrQ (product tour), mPYP-IJmc_c (own-app sequencer demo), 30n3rFgEHds (Eurorack module survey), 6AimjzOBy5I (own-plugin demo/bug walkthrough).
- Transcripts disabled (not rate limit): QmemFx2cpa0, ljC1F__Ds5w, pIHoR1pqAYo, uiEE-2J2wqA, _76A4r3Nwl0.

## Pipeline notes
- All 7 grounded in fetched YouTube transcripts (raw/<id>/transcript.txt + raw.txt). Quality --strict: 7/7 clean. Novelty: 7/7 NOVEL (max overlap ≈0.10). All in mcp-publish/skills, index.json, LIBRARY.json, taxonomy, curriculum level 3 and skills/*.md. REJECTED.md written for the 6 content rejects.
- route.py COVERED: 1 of 3 hand-checked was a false positive (nbS1pT8V7YU); 2 were rejects anyway (on quality grounds rather than coverage).
- Rate limit had cleared by morning: all 13 carryover prechecks fetched or answered (8 transcripts, 5 disabled) and all 7 searches completed. After 2 fresh fetches, `rate_limited_or_ip_blocked` returned; fetching stopped there.
- Theme today: Euclidean/generative sequencing (previously a gap) + house pad + Paulstretch + Risset rhythm.
- Work dir: batches/work-2026-10-21 (mk.py, publish.py with BATCH 2026-10-21-morning-hunt, c1.py, c2.py, search.sh/log). Backups: backups/2026-10-21-morning-hunt/.

## Carryover for next hunt
- Fetch blocked by rate limit (search hits, not yet read): HXKz89TIlJI (Alchemy morphing), uorRN6iH87U (analog random gate generators), SZKIODnJuwU (Cubase S&H — check vs existing S&H skill).
- Other unread search hits: jfwv0Gasf6Q, X_zozWSx-RU, L1Vy2ZmHQ3Y, ypYhfCt874s (S&H query); LP1rbAbojkc (machine-translated), cwwOLuAuvbc (spectral); aDgy_IB9Ets, P68bG3JEskQ (phaser query); Qj2bLCq1PA4, P7-mewTtDts (shepard query; likely product demos).
- Vocoder-chords and paulstretch searches returned 0 kept again; treat as exhausted for now.
- Still thin: classic phaser pad (phaser query surfaced only phase-issue/product videos, third day running). MH7YiOWQIhI / kHWOIE4YTZ4 still queued for tlang upgrade.
