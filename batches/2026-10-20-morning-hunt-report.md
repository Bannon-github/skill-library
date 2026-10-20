# Morning synth YouTube hunt — 2026-10-20 (PT)

Also finishes the interrupted 2026-10-19 run (no 10-19 report was written; its 3 drafts and 5 CANDIDATES_READY videos are published or rejected here).

## Counts
- MCP count: 160 → 168. LIBRARY entries 158 → 166. Taxonomy cinematic-hybrid-synth 124 → 132; curriculum level 3 93 → 101.
- New skills: 8 (3 drafted on 10-19, 3 from 10-19 CANDIDATES_READY, 2 from router-COVERED false positives hand-checked today). Rejected or skipped: 7. Crypto pivot: no.

## New skill IDs
- `modal-partial-resonator-exciter-material-tone-hit-inharmonic-series-parallel-velocity-random-hit` ← Pd9AFeTcl2k (10-19 draft; route COVERED was a false positive)
- `struck-string-model-pre-strike-brightness-frequency-dependent-decay-slope-mallet-bounce-polyrhythm-layers` ← B3n9GOT0Q9A (10-19 draft; COVERED false positive)
- `classic-fin-envelope-filter-sweep-dual-detuned-osc-mono-8-voice-unison-tape-echo-dual-filter-layer` ← xil_HpL1izg (10-19 draft; COVERED false positive)
- `four-phasor-wavetable-voices-per-voice-phase-shaper-cross-pm-matrix-modulator-only-operator-morph-filter-notch` ← JC-UA2C-sZU (phase-distortion gap: 4-voice PD + cross-PM)
- `hybrid-score-role-first-layering-synth-drone-string-swells-square-motor-dotted-pingpong-staggered-entry-reverse-render` ← m6wfGX7rwiQ
- `reese-bass-three-saw-octave-down-mixed-unison-fine-detune-mono-legato-glide-softclip-parallel-comp-hpf-automation-mono-below-120` ← 7OatKTrtmJ8
- `vocoder-as-insert-fx-any-patch-carrier-mic-modulator-mode-decay-formant-dry-mic-slot-order-arp-square-lfo-formant` ← MjijB6ExetI (route COVERED; false positive; first dedicated vocoder skill)
- `mono-reverb-pockets-narrow-width-before-pingpong-wet-dry-as-distance-post-reverb-bandpass-lfo-dry-left-reverb-right` ← e1AMHtuuuTQ (route COVERED; false positive)

## Rejects / skipped
Zgwxh3VrQZQ (sponsored preset browsing, thin), b2zwGqefZw8 (layering advice; near-dup of transient-splice / three-layer pad skills), pO5BOqCS9mo (hand-checked COVERED; commercial-preset layer tour), 7B2fWwkwYSU (transcript is music markers only), jC_ckXoCHYE and FOL9EDiLp4k (already rejected on 10-19: product demo / covered reverse-riser), Today's 2 searches gave 0 kept (all prechecks rate-limited).

## Pipeline notes
- Verified that all 3 10-19 drafts were grounded in fetched YouTube transcripts (raw/<id>/transcript.txt + raw.txt). Fixed the Pd9AFeTcl2k source title to match meta.json.
- Quality --strict: 8/8 clean. Novelty: 8/8 NOVEL (max overlap 0.152, Reese vs cinematic braam). All 8 are in mcp-publish/skills, index.json, LIBRARY.json, taxonomy, curriculum level 3 and skills/*.md. The full-catalogue strict check still shows 3 old non-synth failures (lightroom-select-and-develop-photo, python-pathlib-basic-file-workflow, volyraph-browser-splat-pipeline), which predate this batch.
- route.py COVERED stayed unreliable: 5 of 5 hand-checked synth COVERED verdicts had novel content (3 drafts plus MjijB6ExetI and e1AMHtuuuTQ).
- YouTube rate-limited the search prechecks (`no transcript (rate_limited_or_ip_blocked)`) from the first search today: paulstretch 0 kept / 2 blocked; euclidean-generative 0 kept / 11 blocked. The search loop was stopped after the third query started rather than retried. The remaining queries (sample & hold, vocoder chords pad, spectral morphing) were not run.
- Work dir: batches/work-2026-10-20 (mk.py, publish.py with BATCH 2026-10-20-morning-hunt, c1.py, c2.py, search.sh/log). Backups: backups/2026-10-20-morning-hunt/.

## Carryover for next hunt
- Searches to re-run after the rate limit clears: "sample and hold random modulation synth tutorial", "vocoder chords synth pad tutorial", "spectral morphing synth sound design tutorial", "paulstretch extreme time stretch ambient tutorial", "euclidean rhythm generative ambient synth tutorial".
- Prechecks blocked by the rate limit (re-check transcripts): 30n3rFgEHds, QmemFx2cpa0, ljC1F__Ds5w, UchJGizLiLM, WeOuxcN0pV8, mb3yqXO9JiE, PP6dAPAhIrQ, pIHoR1pqAYo, uiEE-2J2wqA, _76A4r3Nwl0, mPYP-IJmc_c, 6AimjzOBy5I, bIbOgZn1h_Y.
- Router COVERED with a local transcript, not yet hand-checked: nbS1pT8V7YU (classic house pads), rVRMgLa9Y9E, P_bIEn8FGzI; MH7YiOWQIhI / kHWOIE4YTZ4 (machine-translated, still queued for a tlang upgrade).
- Still thin: classic phaser pad (no good hits two days running). Vocoder and phase distortion are now partly covered.
