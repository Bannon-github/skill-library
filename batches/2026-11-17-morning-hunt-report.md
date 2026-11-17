# Morning synth YouTube hunt: 2026-11-17

Mode: compact library (fold-in). No standalone skills were published. All 3 new skills passed `quality_check_skill.py` (clean) and `novelty_check_skill.py` (NOVEL, 0.87–0.91). I hand-checked each against the target cluster's variants and folded it in with `pipeline/compact/fold_in.py`. LIBRARY.json went 278 → 281 entries (merge_log batch `2026-11-17-morning-hunt`). `mcp-publish/index.json` was refreshed (33 skills) and the new ids resolve through `mcp-publish/aliases.json`. All transcripts are YouTube-provided (pipeline fetcher, auto-generated tracks). No Whisper/ASR was used.

Rate limiting: TYU764RIkmE (carry-over) was fetched. 5XGrxp0ANME stayed `rate_limited_or_ip_blocked` again, as did 647i69GOaoc, mmn6iSBKdp8 and zEkCere2A_Y. TfBMKlJV96U and rK0pEiBYfq8 recovered on the fetcher's internal retry. `route.py --domain synth` returned CANDIDATES_READY for all 7 routed ids, including clear rejects (the false-novel pattern continues), so every result was hand-checked.

## Folded in (3)
| video | skill id (alias) | cluster | one-line goal |
|---|---|---|---|
| ET1CvImwzxw | one-progression-to-ambient-layers-parallel-maj7-bass-root-split-upper-voicing-octave-tighten-common-tone-root-4-5-arp-seconds-dyad-pad-anticipated-melody-octave-double-long-attack-swells | harmony-chords-voicing-and-slow-motion | Turn one progression into a full ambient layer set. Copy and thin the clip per role: bass keeps the root, the pad keeps the upper 3 notes with the top note dropped an octave. A common-tone root-4-5 arpeggio fits every chord. A seconds-based dyad pad contrasts the thirds-based pad. The melody anticipates each chord, with an octave-lower double and long-attack swells on the common tones. |
| TfBMKlJV96U | ambient-home-base-step-away-and-return-progression-static-sequence-anchor-expanding-harmonic-distance-stay-in-key-delayed-echo-copy | arrangement-ambient-cinematic-score | **Song-structure gap (partial).** Ambient that "goes somewhere": a steady tonic home-base sequence plus piano excursions that leave and return, going a little further each time, all in one key (no attention-grabbing key changes). A slightly late echo copy adds interest instead of more chords. |
| rK0pEiBYfq8 | friction-excited-modal-resonator-pad-string-beam-profile-harmonic-warp-low-partials-pinned-slow-lfo-partial-limited-wavetable-bed-serial-comb-keytracked-brilliance-washed-insert-shimmer | physical-modeling-plucks-strings-resonators | Evolving modal pad. A sustained friction-noise exciter drives a resonator bank (string or beam profile). Partial warp keeps the low partials pinned, under a slow LFO with per-voice rate offsets. A partial-limited wavetable bed sits underneath, then a serial comb into a low-pass. Brilliance is key-tracked, and the reverb/shimmer is washed out on inserts. Product walkthrough distilled to generic modules and a Web Audio mapping. |

Matt's preferences are written into each skill's constraints. ET1 dropped the beat-repeat/granulator stutter (clicking texture) and the pitch-bend swells. rK0 dropped the pitch-mod chorus and pitch-shift delay, and the friction density is kept continuous so it doesn't tick. Arpeggios and home-base lines are fixed and steady. Drums enter early (~8 counts / ~12 s). Everything is Ableton/MIDI-friendly.

## Rejected (4)
- **TYU764RIkmE** (carry-over, Deep Reese Bass): a basic Serum two-oscillator unison, LP24 and drive preset walkthrough. Already covered by bass-design-sub-reese-808-and-layering.
- **dMzMmnRT_HE** (12 transitions): generic EDM/pop list with a sponsor segment. Gaps, reverses, tails, fills, risers and fake-outs are already covered by arrangement-loop-to-song and risers-impacts-transition-fx.
- **HRtqWS5oqtA** (3 panning rules): generic indie mix advice, covered by stereo-width and mix clusters.
- **7idR6B2UyJg** (harmonics on kick): rambling, built around a vendor plugin (MaxxBass-type), with no portable procedure.

Seen but skipped (vocal, product, beginner or binaural-app content, or rate-limited): eDrCDYJkq6o, o9rydDg0G4U, i3GLybBxeEg, 5VH8cx7qfrc (exciter = vocal/hardware/product), 2d3Fu9vuPPI, vHXi__0HQrk, dO0Vzjf7c7A, cRsrn0vQF-M, eiN48Hca8kM / Ehciijs1Rr4 / mPJEfc6xqLA / EE1CqVWq0vc / PXN3t5p8MSM (binaural app how-tos; no isochronic DAW gate ramp), FlbAzM5w0bs, Yq70oXdZhok, lZbfWJdHZTg, CLS9KWODe_g, iguuPHZ3OkY, b3Nw3LexBOw, ZdKxOsK4nQ8 / eOgsuNaOKEk / uhC-5pwVHLw (phaser manual chapters), MTl-Sj8jR0M, I66_LmOTlSk, tzfzkTAQsnE, DY9SLPLBlO4, z6r7BhWq-Io, cqJKzJPKoZE, ws8yLOIkLms, ScZIslxpYaU, kyFvfD5XSHQ, un9HdSAoZrY, MRJt_i3eDMA, bxWHs8caTzw, uZ9WQDojQt8, yiF_cUEtMdY, NritylXfO7A, lORu0zmSKzc, Ww-2TtxrZTw, TPSFXI_fDuI, hblR9Q8clpo, v97MvZ1XhXM, xy_NbX2SNSc, l1pxzjfwX1c.

## Searches (2026-11-17)
`search_youtube_topics.py --skip-known` (240–3600 s): harmonic exciter synth pad; ambient breakdown section without drums; isochronic tones in a DAW; soft felt kick ambient; phaser pad synth; cinematic build & transition ambient; reversing/stretching orchestral samples; wavetable evolving cinematic pad; stereo width pads mid/side; punchy bass synth. Logs are in `batches/work-2026-11-17/`.

## Gaps still open
- **Isochronic gate-rate ramp generator:** still open. The searches only return binaural app tutorials (Gnaural, Audacity). Write it in-house in `sample-lab/theory/`.
- **Drumless ambient breakdowns:** still open. Song structure improved with the home-base/excursion rule and the one-progression layer set.
- **Soft/felt kick:** still open (hits were house/Diva masterclasses and found-sound drums).
- **Exciter air on pads:** still open. "harmonic exciter synth pad" returned vocal and hardware exciter videos. Next try: "parallel saturation high shelf pad air" or "Aphex exciter synth".
- **Pure phaser pads:** still open (only plugin-manual phaser chapters).
- **Orchestral sample stretching/reversing:** still open (hits were SFX/foley design).

## Carry-overs
- **5XGrxp0ANME**: "Why 80s Pads Sound So Good (And How to Make Them)". Rate-limited (2nd day).
- **647i69GOaoc**: "How to Make a Wavetable Evolving Pad in Arturia Pigments 2". Rate-limited.
- **mmn6iSBKdp8**: "How to Make HUGE Evolving Pads with Ableton Drift". Rate-limited.
- **zEkCere2A_Y**: "Sound Design Series: Punchy Bass using Subtractive Synthesis". Rate-limited.
