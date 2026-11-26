# Morning synth YouTube hunt: 2026-11-26

Mode: compact library (fold-in). Both new skills passed `quality_check_skill.py` (clean) and `novelty_check_skill.py` (NOVEL, best overlap 0.070 and 0.083). Each was folded into a cluster with `pipeline/compact/fold_in.py`. LIBRARY.json went from 302 to 304 entries (merge_log batch `2026-11-26-morning-hunt`). `mcp-publish/index.json` refreshed (33 skills), aliases updated. All transcripts are YouTube captions via the pipeline fetcher (yt-dlp); no ASR. `route.py` skipped to save tokens; videos gated by hand.

Fetches: 14 videos tried, 10 transcripts, 3 with transcripts disabled (e_jWkqJSiMI, DG4fTyKAlvQ hybrid impact, GluePCHvKL0 BeeOne entrainment), 1 still rate-limited after 4 tries (JhZU6JGvoHw, punchy/deep kick: carry over). Heavy YouTube rate limiting today; several videos needed 2-3 slow retries.

## Folded in (2)
| video | skill id (alias) | cluster | goal |
|---|---|---|---|
| Fj3jwdLBD60 | cinematic-cue-intro-from-a-section-dna-...-a2-octaves-countermelody | arrangement-ambient-cinematic-score | **Arrangement gap (intro + development).** Write the A section first, then build the intro only from its DNA (first two chords on long strings, the motive augmented into long notes, booms, a high pedal, one pitched-up metallic hit in a long reverb), bridge with an ostinato fade-in under a horn crescendo, and develop A1 -> A1' (new melody instrument, low brass, borrowed major IV) -> B (keep one A element, drop percussion/ostinato) -> A2 (octave melody, metals, horn countermelody). |
| liS9PQyHSa4 | ambient-melody-three-tricks-vector-melody-...-lydian-dorian | scales-modes-and-melody-writing | **Melody (steady pitch).** Three ambient melody devices: vector melody (one-direction Dorian run that may start/end on the 9th/11th), a scale-step sequence over chords sharing a bass A (Dm/A -> Am7 -> Bbmaj7 -> Aaug -> A7 -> D), and modal transformation (two chord tones slip a half step: Gbmaj7 -> Gm7 -> Gmaj7, melody Lydian -> Dorian -> Lydian, rising). |

Matt's preferences: the cue's 16th-note ostinato stays pitched string/synth notes (no noise ticks); a soft low pulse is in by ~8 counts (source keeps intro percussion to sparse booms); melody skill bans bends/glides/random notes. No health claims.

## Rejected (7), with notes in distilled/<id>/REJECTED.md
- IwOpaxWJRPA: Sylenth stereo-widening tips; covered by stereo-width cluster, thin.
- uhC-5pwVHLw: Harmless phaser knob tour; thin.
- eOgsuNaOKEk: Diva chorus/phaser knob tour; the only usable move (depth 0, sweep centre) is already in the phaser cluster.
- HDqafhAl_pA: ambient arrangement breakdown; covered, and built on random modulation plus few-ms pitched glitch hats (clicking).
- OD5nzni_us0: 100/102 Hz delta binaural in 4 minutes; thin + health claims.
- z_QW-nrMAA0: 5 ambient pad methods; all covered, and puts LFOs on pitch.
- 0X7b2PJghZA: BandLab lo-fi loop-to-song arrangement; generic/covered.

Skipped at title triage: _sh-DO-5bOQ / 9QzrmWWuDU4 (guided sleep talkdowns), H8_A9seCnmw (off-topic), ZdKxOsK4nQ8 (already skipped 11/25), I66_LmOTlSk (film sound), y4w_mNuhxmw (digicore), EaB6SZEQM5w, FlbAzM5w0bs (40 min house masterclass), equNWJvGVio, EvTcHTCLRg0, rdP6yU-MJDY (custom wavetable promo), uZYDDjMj1aw / Om3zB35xxTo (science explainers), sDgz1X6vBjY (NP2 product), kzkDoBupXKM (binaural in Logic, covered), 0anOtgq4Obc, TfwO3el-i1A, JAtoSiZm-V0, VAdg4Mrt65Y (SFX library promo), tzfzkTAQsnE, WZXXOkZ4-MM.

## Carry-overs
- JhZU6JGvoHw (Make Your Own Kick Drums - Punchy and Deep Kicks): captions listed but fetch rate-limited 4 times.
- Still worth a look later: TfwO3el-i1A (synthwave pads), WZXXOkZ4-MM (riser sound design, 26 min), kzkDoBupXKM (alpha binaural in Logic).

## Searches
9 queries via `search_youtube_topics.py --skip-known` (two rounds). Logs are in `batches/work-2026-11-26/`.

## Gaps still open
- Isochronic gate-rate ramp: no new YouTube source again (searches return sleep talkdowns/science explainers). Note the brainwave cluster already has a 15 -> 4 Hz pulse-rate automation variant on a sine-carrier isochronic layer; a raised-cosine staged gate ramp still needs writing in-house in `sample-lab/theory/entrainment_tones.py`.
- Pure phaser pads: still partial (two phaser tours rejected as thin/covered; envelope-controlled phaser from 11/25 had transcripts disabled).
- Soft/felt and punchy kick: partial (JhZU6JGvoHw carried over).
- Hybrid cinematic impact: DG4fTyKAlvQ had transcripts disabled.
- Exciter/air on pads: still partial.
