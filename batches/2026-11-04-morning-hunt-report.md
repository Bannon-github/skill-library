# Morning synth YouTube hunt: 2026-11-04

Mode: compact library (fold-in). No standalone skills were published. All 4 new skills passed `quality_check_skill.py` (clean) and `novelty_check_skill.py` (NOVEL, scores 0.90-0.94). I hand-checked each against the target cluster's variants and folded it in with `pipeline/compact/fold_in.py`. LIBRARY.json has 4 new entries (236 → 240 entries, merge_log batch `2026-11-04-morning-hunt`), and `mcp-publish/index.json` was refreshed (33 skills). New ids resolve through `mcp-publish/aliases.json`. All transcripts are YouTube-provided. No ASR was used.

## Folded in (4)
| video | skill id (alias) | cluster | one-line goal |
|---|---|---|---|
| TosV3erGfsg | start-bright-then-filter-pad | brightness-and-air-at-the-source (first video variant) | Start from a bright, rich oscillator and filter it smooth inside the synth, so cutoff automation can bring the air back. Odd unison (5-9) for solid, even for unstable; imager after a big low-cut reverb; attack-free swell pad from any played source. The source's pitch-drift LFO was dropped (steady pitch). |
| UrpnB5YlGL8 | kick-bass-four-level-lock | bass-design-sub-reese-808-and-layering | Kick+bass punch in 4 levels: duck the bass; split a mono sub (<~120 Hz) and duck it harder; lock the sub phase (random phase 0, start phase chosen on the oscilloscope, micro-delay alignment); light bus glue (subtle saturation, ~30 ms-attack glue comp at 1-2 dB, soft clip). |
| L0mST_BaaBA | genre-drum-pattern-families-tempo-map | drum-groove-programming-swing-and-ghosts | Four-on-the-floor vs two-step families on a kick-1 / snare-2-and-4 foundation, a tempo-to-genre map (house 120-130 … DnB 170-180, halftime 140), set syncopation spots, uniform swing offsets, and 2/4-bar variations with a tom fill and crash. |
| xeuYUFZpOdA | atmospheric-liquid-dnb-break-layering | drum-synthesis-and-hybrid-percussion | Liquid DnB break: quieter second kick, mid-dip kick EQ, decay-tightened one-shots, a sliced high-passed break, tops grouped and ducked to kick/snare, a soft-clipped glue bus, and a tiny no-pre-delay drum room. |

## Rejected (7)
- **y1YmvAO_5ko / uTKYIv4xnYE** (tension cue for TV/film, parts 1-2): thin walkthroughs with a promo. Sync points and the reverse-cymbal intro are already in the arrangement and riser clusters. Delta noted: a drum gap on the last beat of every 8 bars as an editor cut point.
- **q7OQdzGZwNA**: off-domain (film editing and storytelling).
- **5A8mI4l-erg / HJZG-qD4oso** (EtherLoops ambient loop): promo (the creator's own MIDI apps and wavetable pack) and already covered by the wavetable and loop-to-song clusters. Delta noted: a texture LFO cycle equal to the loop length.
- **FTdXOWKIQc4**: off-domain (acoustic kick-drum head tuning).
- **oZsiE6KckQM** (mono stack method): near-duplicate of the stereo-width cluster's chord-split Method B. Delta noted in REJECTED.md.

## Router note
`route.py` returned CANDIDATES_READY for all 5 videos routed. This time it gave a false *novel*: hand-checking showed oZsiE6KckQM is covered. Keep hand-checking in both directions.

## Searches (2026-11-04)
These queries were run: "airy pad presence sound design tutorial", "pad brightness high end sound design", "cinematic kick and bass punch tutorial" and "stereo width synth pad mono compatible tutorial". Fetching: the first 2 fetches were rate-limited (TosV3erGfsg, p5ETZc7Zfw4). After that, 11 of 11 succeeded at 30 s spacing, including the TosV3erGfsg retry. p5ETZc7Zfw4 was not retried.

## Gaps still open
- **Brightness/air:** the cluster now has 1 video variant (filter-from-bright). A dedicated "air" source (exciter/shelf/noise-air layering on pads) is still missing. Search hits were mostly synth demos (4Dub1HigXtU "INFINITE ambient pads like The 1975" was not fetched and might be worth trying).
- **Kick+bass punch:** an EDM-general workflow is now covered. A specifically ambient/cinematic soft-kick + sub workflow is still thin.
- **Wavetable, hybrid, FX, modulation:** not searched today, to stay within the token budget. Stereo width was searched, but nothing new was found beyond the existing cluster.

## Carry-overs
- p5ETZc7Zfw4 (lush evolving pads in Wavetable): rate-limited, retry.
- Search leads not fetched: 4Dub1HigXtU (infinite ambient pads), A52l7uG3Sq4 (kicks hit harder, 4 steps), ZKR8ODDIWqE (mix kicks masterclass), zscsukQNOLU (stop making everything wide), 5oW5Mb-3sF0 (wide bass mono-compatible).
- MH7YiOWQIhI / kHWOIE4YTZ4: tlang upgrade still optional and not done.
