# Morning synth YouTube hunt: 2026-11-19

Mode: compact library (fold-in). No standalone skills were published. All 4 skills passed `quality_check_skill.py` (clean) and `novelty_check_skill.py` (NOVEL, best overlap ≤0.08). I hand-checked each against the target cluster's variants and folded it in with `pipeline/compact/fold_in.py`. LIBRARY.json went 281 → 285 entries (merge_log batch `2026-11-19-morning-hunt`). `mcp-publish/index.json` was refreshed (33 skills) and the new ids resolve through `mcp-publish/aliases.json` (verified via youtube-skills `get_skill`). All transcripts are YouTube-provided (pipeline fetcher / yt-dlp, auto-generated tracks). No Whisper/ASR was used.

Recovery of 2026-11-18: yesterday's run was interrupted after drafting two skills (uZfNc_oCwOc, EuPisVu55oU) but before fold-in, LIBRARY.json or a report. Today I re-read both drafts against their saved transcripts, confirmed every step is grounded, set their batch to 2026-11-19 and folded them in. Ky7jN8QmxDo, fetched yesterday, is rejected below.

Rate limiting: much better today. Carry-overs mmn6iSBKdp8, zEkCere2A_Y and 5XGrxp0ANME were fetched (5XGrxp0ANME on the 2nd attempt). 647i69GOaoc now reports `transcripts_disabled`, so it is dropped and is no longer a carry-over. `route.py --domain synth` again returned CANDIDATES_READY for every id, including clear rejects, so every result was hand-checked.

## Folded in (4)
| video | skill id (alias) | cluster | one-line goal |
|---|---|---|---|
| uZfNc_oCwOc | drumless-emotional-ambient-cue-sneak-in-layers-high-cut-pads-reverse-delay-piano-artifacts-bass-entry-note-root-vs-flat-six-pulsing-piano-filter-revealed-texture-motif-ebb | arrangement-ambient-cinematic-score | **Drumless-breakdown gap.** Build a drumless emotional ambient cue/breakdown layer by layer. Each layer sneaks in, and pads are high-cut below the lead/voice range. Reverse-delay piano artifacts add pacing. The bass-pad entry note sets the emotion (tonic = serious, flat-six = emotional lift), with slow pulsing piano undertones, a low-pass-revealed texture loop and a motif that ebbs and flows through modulation. |
| EuPisVu55oU | fifth-varispeed-resample-2-3-time-compress-up-fifth-bounce-unwarped-down-fifth-tape-texture-piano-strings | granular-and-spectral-texture-design | Fifth-ratio varispeed round trip (3:2) for a sampled-from-record piano/strings colour at the original tempo and pitch: MIDI time-compress to 2/3 length, +7 st, bounce, un-warped audio −7 st, then a quiet noise bed and saturation glue. |
| mmn6iSBKdp8 | velocity-to-lfo-rate-evolving-pad-smooth-wander-lfo-shape-filter-3-6-50-slow-adsr-parallel-doubler-grain-reverb-lanes-utility-trim-outer-lowpass-glue | modulation-lfo-envelope-random-routing | Evolving subtractive pad: a smooth ~0.2 Hz LFO on shape, cutoff and resonance, with velocity setting the LFO rate. Amp envelope is 3 s / 6 s / 50% / slow release. Parallel dry, doubler, grain-delay and wet-reverb lanes are trimmed −10 dB and glued with a reverb and an outer low-pass. |
| 0IgwdHg0ZwM | kick-heart-sine-sweep-goldilocks-sweep-time-not-clicky-not-laser-decay-leaves-silence-for-bass-low-start-freq-55hz-end-reference-clean-heart-parallel-saturation-layered-transient | drum-synthesis-and-hybrid-percussion | **Soft/punchy kick gap (partial).** Rules for the pitch-swept sine kick "heart": sweep time just right (too short = detached click, too long = laser), decay leaves silence for the bass, modest start frequency, end frequency against a ~55 Hz reference. Keep the heart clean, then add parallel saturation and an optional transient layer. |

Matt's preferences are written into each skill's constraints. Steady pitch: EuPisVu55oU drops the sample-and-hold frequency-shifter repitch, and mmn6iSBKdp8 routes its LFO to timbre only (smooth wander, no S&H, steady low-mod reverb). No clicking textures: EuPisVu55oU drops the vinyl crackle, mmn6iSBKdp8 swaps the bacon-grease sizzle foley for a smooth bed and caps the grain-delay lane, uZfNc_oCwOc fixes the "random" reverse-piano hits into a set in-key MIDI figure, and 0IgwdHg0ZwM turns its click-vs-laser diagnostic into a non-clicky soft-kick lever. Drums enter early (~8 counts / ~12 s). Everything is Ableton/MIDI-friendly.

## Rejected (5)
- **zEkCere2A_Y** (carry-over, punchy bass in Operator): beginner square-wave plus filter-envelope walkthrough. Already covered by bass-design-sub-reese-808-and-layering.
- **5XGrxp0ANME** (carry-over, 80s pads): the movement comes from oscillator drift, pitch-LFO and pitch envelopes (wobbly pitch). The rest is covered by the supersaw, wavetable and modulation clusters.
- **-HDM5IZARyg** ("How Exciters Work!"): really master-bus saturation for hip-hop, not pad exciters.
- **s3t02k1-G74** (sound-healing journey with Ableton & Push): course promo with no procedure.
- **Ky7jN8QmxDo** (lo-fi drums, fetched 2026-11-18): generic, covered by the drum, sidechain and mix clusters.

Transcripts disabled (dropped): r-CS6LWdMQM (Brain Entrainment BeeOne tutorial, the only isochronic/entrainment production hit) and 647i69GOaoc.

## Searches (2026-11-19)
`search_youtube_topics.py --skip-known` (240–3600 s): isochronic tone Ableton gate volume automation (0 results); brainwave entrainment music production; drumless breakdown ambient; arrange cinematic intro/build/climax/outro; soft kick drum synthesis; synth pad brightness exciter saturation; phaser pad sound design; ambient loop synth resampling. Logs are in `batches/work-2026-11-19/`.

## Gaps still open
- **Isochronic gate-rate ramp generator:** still open. YouTube has none (0 hits; the one BeeOne video has transcripts disabled). Write it in-house in `sample-lab/theory/entrainment_tones.py`.
- **Drumless ambient breakdowns:** partly filled (uZfNc_oCwOc). Still missing a breakdown → drop return inside a beat track.
- **Song structure, cinematic sections/builds:** search hits were beginner composition or video-editing content. Try "film score cue structure tension release tutorial".
- **Soft/felt kick:** partly filled (sweep/decay rules). Still missing a felt/muted acoustic-style kick (try "felt kick ambient sound design low-pass transient").
- **Exciter air on pads:** still open (hits were vocal, mastering and plugin demos).
- **Pure phaser pads:** still open (only plugin-manual phaser chapters again).

## Carry-overs
Not retried today, to keep the run bounded. These were rate-limited on 2026-11-18 and never logged because that run was interrupted: Of6RLgo_XNI, DU_Wu9OBCCw, Vx94sNJpu1c (Advanced Serum complex pad design), LcAcmBKryxE (Stereo Width Part 2: Widening), haZ6byjMpOk, z7xVfv8aByI (Multigrain resampling, ambient), VSGYqvV4bTg (6 unexpected uses for Ableton's delays), jYrz49kwOWg (3 basic bass patches), oy8Cr-U2pwA, CW3jk3BgE1E, 2bvdVDRpfAQ.
