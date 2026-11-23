# Morning synth YouTube hunt: 2026-11-23

Mode: compact library (fold-in). Every new skill passed `quality_check_skill.py` (clean) and `novelty_check_skill.py` (NOVEL, best overlap 0.057–0.086). Each was then folded into a cluster with `pipeline/compact/fold_in.py`. LIBRARY.json went from 290 to 294 entries (merge_log batch `2026-11-23-morning-hunt`). `mcp-publish/index.json` was refreshed (33 skills), and the aliases were updated. All transcripts came from YouTube (auto captions via the pipeline fetcher). No ASR was used. `route.py` was skipped to save tokens, and videos were gated by hand.

YouTube rate-limited heavily today: 24 retry events, and 7 of 11 fetch attempts failed.

## Folded in (4)
| video | skill id (alias) | cluster | goal |
|---|---|---|---|
| yMJaUS776yQ | light-tension-cue-aba-every-4-bars-energy-pulse-engine-mediant-chord-lever-breakdown-simmer-a-plus-b-return-cliffhanger-edit-point | arrangement-ambient-cinematic-score | **Song-structure / tension-to-release gap.** A one-chord drone plus an offset pulse "rhythmic engine". A new gear every 4 bars. An i→VI mediant lever before the breakdown, where B means breakdown (development by reduction). The return is A+B with no new sounds, more octaves and booms every 2 bars. A cliffhanger edit point and the final button both have the delays automated off. |
| efnKT5pHqUo | melodic-cells-ostinato-repetition-legitimizes-tonic-against-bass-tension-major-triad-release-octatonic-half-step-cycle | scales-modes-and-melody-writing | **Tension gap.** Melodic cells are reordered and transposed up minor thirds, and repeated so they sound intentional. Tension comes from a bass that fights the tonic ostinato, and release from major triads. Octatonic chords come from cycling the cell down by half steps. |
| PUycGHv-2Jo | sus4-tension-rising-key-steps-pedal-bvi-bvii-over-pedal-big-tonic-release-widening-range-unison-to-octaves | harmony-chords-voicing-and-slow-motion | **Tension-to-release gap.** A sus4 that resolves on the melody's landing note. The theme is stated on the dominant, then the tonic. The key steps upward. A bVI pedal carries bVII over it, then resolves to a big I with a roll. The pitch range widens, and the theme moves from unison to octaves. |
| xO9CiDa3324 | phaser-static-notch-tone-shaping-few-notch-slow-swirl-pad-hat-loop-phaser-after-delay-send-section-bus-phaser-variation | pad-phaser-notch-comb-movement | **Phaser gap (partial, delta).** Static notch-centre tone shaping with the LFO at 0. A few-notch, high-spread slow swirl on pads. A phaser after the delay on a send to clear the centre. A bus phaser automated on for one section only. |

Matt's preferences: the drone pitch-bend and tremolo in yMJaUS776yQ were dropped in favour of steady pitch. Phaser LFOs stay slow on held pads, and hat phasing has to avoid a clicky texture. Drums enter early (~12 s) where a skill applies to a beat track.

## Rejected / skipped at title triage
None of the fetched transcripts were rejected. These search hits were skipped by title before fetching: video-editing transitions (kmnYxvGxLVE, TKXBAaQB03U, FZS0olGLPIw), off-topic art/photo results (wRFbO7OhKVk, vqCeek_ZwVo, QwtFYWczrXY), an AI-prompt music video (XO_Xsjp6bMo), a neurologist explainer with no production steps (Om3zB35xxTo), and plugin/preset walkthroughs (ExUaHaZ_sgg, ZdKxOsK4nQ8, -MGcBX0zYjc).

## Carry-overs (rate-limited today, not fetched)
z7xVfv8aByI (carry-over again), jYrz49kwOWg, GXNWpGSkgBo (seamless transition between themes), uKpK0L-0KwA (meditation track from scratch in Ableton; **priority** for the isochronic/brainwave gap, tried twice), IuscQShlL58 (tension in electronic music), k40nANMRnG4 (binaural beats in Ableton).
Already resolved earlier (rejected 2026-11-20): Of6RLgo_XNI, Vx94sNJpu1c.

## Searches
7 queries via `search_youtube_topics.py --skip-known`. Logs are in `batches/work-2026-11-23/`.

## Gaps still open
- Isochronic gate-rate ramp: still no YouTube source. Next try is uKpK0L-0KwA / k40nANMRnG4; otherwise write it in-house in `sample-lab/theory/entrainment_tones.py`.
- Exciter air on pads: open (search returned off-topic and plugin-demo hits).
- Soft/felt kick: open (only lo-fi drum mixing hits).
- Pure phaser pads: partly filled by xO9CiDa3324.
- Cinematic tension → release: much improved by today's 3 skills. Transitions between themes (GXNWpGSkgBo) is a carry-over.
