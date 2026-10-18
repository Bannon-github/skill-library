# Morning synth YouTube hunt — 2026-10-15 (PT)

## Counts
- MCP count: 134 before → 150 after. mcp-publish files 134 → 150, LIBRARY entries 132 → 148, `cinematic-synth`-domain skill files 94 → 110. Taxonomy cinematic-hybrid-synth 98 → 114; curriculum level 3 67 → 83.
- New skills: 16 (9 from carryover, 7 from today's searches)
- Rejected: 11
- Carryover for the next hunt: 12 search hits not routed
- Pivoted to crypto/side-hustle: no (synth returns not exhausted)

## New skill IDs
Carryover:
- `wavetable-frames-as-animated-spectral-eq-curve-depth-floor-skew` ← `VrCSssDOxFc`: wavetable frames used as animated spectral EQ curves (±12 dB depth, floor for deep cuts, skew, smoothing, safe-bass ≤400 Hz, L/R time offset, keyframe steps + gate, latency offset)
- `dual-wt-interval-locked-per-osc-position-level-animators` ← `ysMPHY5oiGc`: dual-WT voice with an interval-locked tune/detune pair and per-osc position/level animators. Recipes: Reese bass (~15 cents, opposing position), −5 st harmony that fades in, +19 st S&H atmos pad, level-ramp pluck
- `live-rolling-buffer-granular-grain-behaviour-modes-mosaic-glide-bloom-tide` ← `3q-o772IYQY`: live one-bar ring-buffer granulator with grain-scheduling modes (mosaic interval clouds, per-grain glide, reverse+wow, ghost-grain bloom, LFO tide, fixed-position stars, orbit)
- `fm-operator-inline-effects-delayed-modulator-bell-noise-comb-string` ← `XnSE9X0-S9M`: effects inside the FM operator chain (delayed-modulator bell, noise→comb physical string ×3 detuned pairs, phase/EQ, decimator, waveshaper, punch)
- `operator-osc-filter-pairs-three-filters-into-master-fm-into-filter` ← `X4TPAWQw4ss`: subtractive architectures from operator pairs (six osc with their own envelopes; three osc→own-filter blocks into a master BP; fixed vs key-ratio filter frequency; FM into filter; series HP→LP)
- `three-layer-pad-key-tracked-ring-shift-cloud-macros-capped-ranges` ← `Rdt5Alxrg60`: three-layer pad with independent envelopes, plus key-ratio ring mod (×2), frequency shift and an octave-up granular cloud on capped macros (60% / half / 0.25 wet)
- `nested-modulation-depth-chain-velocity-env-lfo-lfo-cutoff` ← `pYbWRCrFsHQ`: four-degree nested modulation (velocity → env decay → LFO2 amount → LFO1 amount → cutoff). Route said COVERED; false positive
- `generative-wind-noise-three-filters-slow-lfos-lfo-modulated-vca-mix` ← `_6mEzWHoxKo`: no-MIDI wind bed (noise → slow LP, high resonant BP whistle, mid SVF BP; offset LFOs, LFO cross-mod, LFO-driven VCA mixer). Route said COVERED; false positive
- `scale-locked-high-end-sparkle-layer-random-notes-air-dust-noise` ← `LeChNmmtNsM`: generative, scale-locked >3 kHz sparkle layer (spray/glass random notes, gravity rate or 1/16–16-bar sync, air/dust noise on random LFOs, noise pitch-lock). Route said COVERED; false positive

New from searches:
- `noise-crackle-resonator-instrument-filtered-delayed-noise-into-harmonic-resonator` ← `GoMfKhol88k`: effects-only chime instrument (crackle → smoothed-S&H filter → ping-pong feedback delay → harmonic resonator with note/decay/harmonics ≥6/≤1 st pitch mod → "smudge" unison + lo-fi macro → reverb → limiter)
- `probability-gated-seeded-scale-loop-endless-ambient-sine-pad` ← `U1t3ELd1LDI`: one looping clip with seeded scale notes, per-note chance <50%, a slow sine pad (~1 s / ~6 s), scale-degree fifth chording, and stereo/granular/reverb FX
- `short-ir-widener-width-trim-drawn-pan-multiband-opposite-haas` ← `Mm5eO24aAec`: mono-safe width (100%-wet short room IR with decay ~20%, width 65% + ~6.5 dB, drawn+smoothed pan rhythm, Haas ≤15 ms with mid/treble tilted opposite ways)
- `dark-hybrid-choir-pad-natural-highs-synthetic-lows-notch-ramp-fx` ← `Futy449F9OY`: dark choir pad (choir WT + octave-up sample FM ~34%; LP on the synthetic layers only; LFO notch ~18%; single rising ramp drives the FX bloom)
- `random-modulator-soundscape-loop-voice-playhead-pan-random-delay-octave-feedback` ← `uEI2Ytxn7iI`: random/step-modulated soundscape (per-voice random playhead+pan drone, arp length 16→4, random 1–8-beat delay with +12 st shifter in feedback, step-scanned vocal)
- `stereo-unlinked-micro-loop-buffer-binary-random-freeze-reverse-cross-feedback` ← `KVtxIwYpGvQ`: micro-loop buffer (freeze/scan/segment, pitch cascade in feedback, sample-rate pitch dips, L +12 / R −12 cross feedback, binary-random LFOs on freeze/reverse per side). Route said COVERED; false positive
- `audio-rate-wavefolder-triangle-vs-sine-fold-gain-sweep-aliasing-wt-synth` ← `G3CIJ3l5Fd8`: audio-rate wavefolder from scratch (triangle vs sine fold sin(x·π/2), 0–50 dB gain, negative-modulo pitfall, aliasing/source choice, a 512-sample folded WT voice with S&H gain). **Fills the audio-rate wavefolder gap**

## Rejects
- `IVi2y9HYBTg` Grainsmith (route COVERED, hand-checked): thin product demo, no recipe
- `Ev4nV2G-47s` Descent granulator (COVERED): preset browsing; harmoniser delta covered by today's mosaic mode
- `S3-2yc9UJDE` Shimmer update (COVERED): sample-library promo
- `rRFGaDy3uUw` Zebra 3 evolving pads (COVERED, hand-checked): real overlap (unison detune mod, WT morph, comb)
- `FId1jUm0zxU` Serum 2 pad from scratch (COVERED): overlaps existing pads and today's choir pad (same creator)
- `7fLA01y1tu4` MS2000 classic pad (COVERED): basic detuned pad; uses chorus, not a phaser
- `x37IwHD-uQ4` Spectral Resonator explainer (COVERED): same device/creator as GoMfKhol88k; merge candidate
- `T64l4AAKFpM` Convergence track breakdown (CANDIDATES_READY): arrangement commentary + library promo, preset-based
- `NQ6tTIJpRDg` Synth layering for orchestral composers (STOP→retry OK): advice-heavy orchestration roles, low portability (curriculum-note candidate)
- `vfZhqBfXvdc` SP-404 vocode pads via loopback (CANDIDATES_READY): device cable workaround, too thin
- `rbcnLgmyjv8` Advanced synthesis guide ep5 (COVERED): narrated overview, advice-only

## Carryover for next hunt
Search hits not routed (YouTube transcript tracks per precheck):
- `aPsWzEfgEOo` Tessera sequenced resonator; `Py4XQbjvn4o` Philtor 12-band filterbank + sequencer
- `YQbj-HEk1xw` random sound → synth (Sample Alchemy); `ZVLM1XMT6Z0` granulate everything
- `-wDkxJ8PMn4` microKorg 2 vintage sounds (check for a vocoder section); `Uv4yk8_vZQc` Serum → vintage classics (manual en-GB)
- `b5QAsgvC9sk` Opsix modulation & filter sculpting; `yuQqY0dx2Rw` CV-3 FM core resonant tine
- `sGZr4PusB0U` "craziest synth effect" (formant query); `E8b_N1RBCxE` orchestral composer sound-design tips
- `y9eDmBUC8ZU` physically modelled MPE strings in Surge XT (55 min); `EwxNeZttFEA` percussion out of a pad
- Merge notes: fold `x37IwHD-uQ4` resonator explainer (spacing/stretch, scale quantise, spectral shift, modes) into the noise-crackle-resonator skill. The `eaQtf_vm9zA` random-LFO→unison-detune note is still unfolded (no substantive delta).

## Pipeline notes
- 14 searches saved as pipeline/searches/2026-10-15-*.json (12 planned + 2 rephrased retries; precheck + require-transcript + skip-known, within year). First-pass "vocoder … carrier" and "west coast wavefolder pad" returned 0 kept / 0 dropped (looks like an empty or failed result). The rephrased retries returned 5 and 6 hits.
- Routing was done in batches of 3–4 and never while searches ran: no DEFER_rate_limited. 2 ids (`NQ6tTIJpRDg`, `G3CIJ3l5Fd8` with a manual en track) returned STOP_no_transcript_asr_flagged and fetched fine on retry ≥1 min later. This confirms again that this STOP outcome is a disguised 429. No ASR/Whisper used.
- route.py on 27 ids: 13 CANDIDATES_READY, 12 COVERED, 2 STOP→retry OK. COVERED was unreliable again: 4 false positives published after a hand-check (pYbWRCrFsHQ, _6mEzWHoxKo, LeChNmmtNsM, KVtxIwYpGvQ); 8 confirmed overlaps or thin videos.
- No translated transcripts were used in published skills.
- Quality --strict: 16/16 clean. Novelty: 16/16 NOVEL (highest local overlap 0.150, between the micro-loop buffer and the random-modulator soundscape, both from today).
- Full-catalog strict check (150): 122 clean, 25 warned, same 3 legacy FAILs (lightroom-select-and-develop-photo, python-pathlib-basic-file-workflow, volyraph-browser-splat-pipeline). Not from this batch; left alone.
- Merged into LIBRARY.json (+16 → 148 entries), mcp-publish/index.json (count 150), topics/taxonomy.json cinematic-hybrid-synth (98→114), curriculum level 3 (67→83), skills/<id>.md. MCP server list_skills reports 150; get_skill serves the new ids. Pre-hunt backups in backups/2026-10-15-morning-hunt/.
- Web Audio notes (AudioWorklet ring buffers/FFT/fold, WaveShaper oversample, ConvolverNode IR widener, per-note probability scheduler) are labelled as implementation notes, not transcript content. Spoken values only; the GoMfKhol88k macro-range table was on screen only and is not reproduced.
- Git sync skipped: no credentials (no GH_TOKEN/GITHUB_TOKEN; gh not logged in).

## Still thin for later hunts
- Spectral (FFT) freeze pad: still none. Today's spectral wins were a frame-driven spectral EQ and a harmonic resonator, not an FFT freeze.
- Vocoder pad with an external carrier: only a thin SP-404 loopback hack (rejected). The microKorg 2 carryover may help.
- Phase-distortion resonant wave / wave alternation: the CZ query returned only synth reviews.
- Classic 4–12-stage phaser pad: the phaser query surfaced an MS2000 pad (chorus) and a barber-pole plugin (translated). Still open.
- Audio-rate wavefolder: now covered (G3CIJ3l5Fd8); a musical folded *pad/bass* patch would still be welcome.
