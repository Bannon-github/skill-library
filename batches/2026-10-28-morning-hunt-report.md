# Morning synth YouTube hunt — 2026-10-28 (PT)

## Counts
- MCP count: 205 → 211 (index.json count = 211 index entries = 211 files in mcp-publish/skills, no duplicate ids). LIBRARY entries 203 → 209. Taxonomy cinematic-hybrid-synth 167 → 173; curriculum level 3 136 → 142.
- New skills: 6. Rejected: 22 (12 hand-rejected + 10 route.py COVERED/no gap). No transcript: 3. Searches: 8 (1 isochronic). Transcripts fetched: 28 of 31 tried (no 429s; 12 s spacing between fetches, 18 s between searches). Crypto pivot: no.
- State backup first: `backups/2026-10-28-morning-hunt/`. Work files: `batches/work-2026-10-28/` (mk.py, c1.py, c2.py, publish.py, fetch.sh, search.sh, queries.txt, search.log, fetch.log, fetch2.log, route.log, new.txt).
- route.py run on all carry-over IDs and the new hits: 8 CANDIDATES_READY, 10 COVERED/no gap. Each candidate was hand-read and checked with novelty_check.

## Published (6)
Loops / generative (carry-over):
- `follow-action-clip-pool-generative-soundscape-…-weighted-note-probability-quantized-sequence` ← fjO8HIZzhZs: build an ambient soundscape that plays itself. Each layer has a pool of clips (including silent ones) that repeat or jump to another clip by about 50/50 chance, over a reverbed noise bed, a tonic drone and a root bass note at random times. Random FX one-shots are auto-panned by sample-and-hold. Note: Matt prefers steady melodies, so the weighted note probability (root high) is the safe setting; keep pitch-random FX sparse.
Pads / brightness:
- `macro-randomizable-evolving-wavetable-pad-…-opposing-adsr-offsets-unison-shimmer` ← yZjQ2e4IREI: a slowly moving wavetable pad rack you can randomize safely. Two formant oscillators at −1/−2 octaves go through serial LP+HP filters on one macro. Envelope-on-envelope modulation plus a slow outside LFO pushes the amp times in opposite directions. ADSR is excluded from randomize.
- `fully-wet-extreme-reverb-pad-from-percussive-sources-…-sidechain-filter-reveal` ← mnledZoD4QE: turn e-piano, vibes, piano and glock into a pad with 100% wet 20–40 s reverbs (chain two for longer tails). Bit-crush before the reverb works as a brightness/harmonic exciter; EQ off the harsh top and the sub build-up, then reveal the pad with a filter. This fills part of the brightness gap.
Song structure / arrangement:
- `withhold-the-reveal-arrangement-constant-ostinato-…-loopable-edges` ← axLAIw6Iw7A: keep the ostinato and a one-note bass unchanged until one moment where several "firsts" land together (new arp, moving bass, new percussion, lead). Pull the constant pad from about −3 to about −14 dB in full parts, mark entries with FX hits and leave a short silence before big mutes. Novelty 0.139 vs loop-is-the-climax (delta stated).
- `dark-ambient-underscore-under-dialogue-five-sections-every-8-bars-…-mirrored-outro` ← E4eghKjWH1o: a tense dark ambient cue that sits under dialogue. Sections change every 8 bars (intro, build, breakdown, climax, outro), with a quiet sub-boom every 2 bars, a filter-grown intro, home-made whoosh risers and impacts, octave-up builds and a mirrored fading outro.
Drums:
- `epic-hybrid-drum-four-channel-synth-hit-…-multiband-upward-comp` ← B75uC7h8bBo: big trailer drums from a four-layer synth hit with very fast curved pitch drops (+5 and +29 st), noise bursts and tube drive, layered with acoustic samples and their bleed/room mics. Glue with a scooped EQ, multiband and gentle upward compression. Novelty 0.141 vs the taiko-from-noise skill.

Checks: quality_check --strict 6/6 clean. Library-wide non-strict: 211 checked, 0 failed, 28 warned, same as before and none new. Under --strict library-wide, 3 old off-domain skills (lightroom-select-and-develop-photo, python-pathlib-basic-file-workflow, volyraph-browser-splat-pipeline) fail on goal length; they are unchanged since 10-03 and are not from this hunt. novelty_check: 6 NOVEL (max 0.141). For all 6: distilled/ copy = mcp-publish/, listed in index.json, LIBRARY.json, taxonomy, curriculum L3 and skills/*.md. The youtube-skills MCP search_skills returns all 6 new skills.

## Rejected (22)
- 9Ba2boGeznQ (four bass types, Vital version): same series and the same 4 archetypes as H6i55lXAMh0 (10-27), so a duplicate.
- j4nHoXGXF8A (arrangement hacks): thin, mostly [Music], plugin-specific; covered by the arrangement skills.
- cwwOLuAuvbc (Morolith): plugin-locked demo. aDgy_IB9Ets (Hive 2): preset walkthrough. Qj2bLCq1PA4: Shepard library promo. P7-mewTtDts: Uplifter plugin promo.
- -nExQ2gNkTk (exciter basics): thin. Useful fact for brightness: use as little as is noticeable then back off; high band around 7 kHz; tube/tape modes; the low band distorts easily.
- 5HvqjMTpuyY (supersaw pad): generic and covered (HP about 450 Hz, phaser bass-sanctuary).
- sAdmSxajm-I (cinematic music breakdown): orchestral-library-heavy; overlaps the emotional cinematic arc.
- 62vHn7Ch1gQ: 8-word transcript.
- 5kIWJen9tcI (double-tracking synths for width: ±5–20 cents, Haas 10–35 ms on one side, complementary EQ): covered by the asymmetric L/R processing and Haas width skills.
- 36RxPGRMsZU (sine wave → ambient texture): mostly Serum 2 + Motion Fractal + Pro-R2 plugin chain. The portable bits (S&H smoothed to phase distortion, chaos LFO to FM at 20–30%) overlap existing FM/PD skills, and chaos on unison detune goes against Matt's steady-pitch taste.
- route.py COVERED / no gap: nRI9gJvZXXM (Bitwig generative chords), KrVtkC8usmI (VCV generative patch), zJmszSX8LPY (loopable ambient loop), 98XTwmm08K8 (wavetable matrix basics), rqMI1w8i3OA (M/S depth mastering), P68bG3JEskQ (external phase-ramp oscillator), Pd28UMiGoBI (isochronic tones in Ableton), sFckKx8rsCs (Bitwig stock ambient loop, three-layer starter already covered), LP1rbAbojkc (Wavegrab plugin walkthrough), --Z4hBMwCs0 (Surge pad tips; OFF_LEXICON, no gap).
- No YouTube transcript (no ASR used): iJSGbXXc8Fc (Richter/Arnalds-style ambient score), 9Du-pWfHk_I (Epic Drums 1, Chandler guitar), QjrINfUCzjQ (generative ambient botanica).

## Pipeline notes
- Isochronic: one quick search only. The how-to hit Pd28UMiGoBI routed COVERED. Session-arc design still needs to be composed from existing skills, not hunted.
- The brightness "exciter / harmonic enhancer on pads" search still returns mostly plugin demos. The best brightness idea today came indirectly (bit-crush before long reverb in mnledZoD4QE).
- Very long video IDs make filenames longer than 255 bytes (Errno 36); shorten skill ids before publishing. IDs starting with '-' need `--` before them for fetch_youtube_transcript.py and route.py. route.py with `--domain cinematic-synth` gave OFF_LEXICON for valid synth videos, so it was rerun without --domain.
- The router is coarse: it claimed overlap 1.0 / "no uncovered" in the outline while Q7 said yes (fjO8HIZzhZs). Always hand-read.

## Carry-overs for the next hunt
- Unfetched hits: pJ_mM8s3Cyo, 0Jj5qQQzDLU, lLaJk7ALJWY, XRCwoFjZFMc, G4u4BBDdtdE, 9MCc7wbYFQU, CuF7pb3Hw1E, ZYn08bUlmG0 / ALHZHHPAdI0 / w8cSlVZ2KbI (Epic Drums 2–4, Chandler guitar; part 1 had no transcript), Oq5TCAKw64Y (53-min ambient space pad on any synth), CPlLPFNRFJk, k7ZJge24Xbo, s8zR_x_cWZM, zjRTE41iu7s, 2Yt1Ae91fv0, zGkWtpmu31Y, HTLPQgNkXyc; isochronic hits 69LMnU3GwLo (arpeggiator method), vYRIXi4A6CU, hfjLuqOK9Co (low priority).
- From 10/22: MH7YiOWQIhI / kHWOIE4YTZ4 still queued for tlang upgrade.
- Gaps: brightness (still thin; try "saturation for air on pads" or "parallel distortion pad brightness"); phaser pads (no new hit today); isochronic session arc (compose).
