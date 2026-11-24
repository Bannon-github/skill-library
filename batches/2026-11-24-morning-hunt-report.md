# Morning synth YouTube hunt: 2026-11-24

Mode: compact library (fold-in). Every new skill passed `quality_check_skill.py` (clean) and `novelty_check_skill.py` (NOVEL, best overlap 0.030–0.045). Each was folded into a cluster with `pipeline/compact/fold_in.py`. LIBRARY.json went from 294 to 298 entries (merge_log batch `2026-11-24-morning-hunt`). `mcp-publish/index.json` was refreshed (33 skills), and the aliases were updated. All transcripts came from YouTube captions via the pipeline fetcher. No ASR was used. `route.py` was skipped to save tokens, and videos were gated by hand.

No rate limits today: 9 of 9 fetches succeeded, including all 6 carry-overs.

## Folded in (4)
| video | skill id (alias) | cluster | goal |
|---|---|---|---|
| k40nANMRnG4 | binaural-staged-rate-ramp-meet-listener-in-beta-clip-envelope-presets-long-note-no-loop-click-minus-24db-bed | brainwave-binaural-isochronic-layers | **Rate-ramp gap (binaural side).** Fixed-Hz L/R sine pair with per-state preset clips. A staged ramp starts where the listener is (15 Hz → 8 Hz over ~5 min, or 40 → 14 Hz with most of the drop in minute 1), uses one long note so the loop never clicks, and sits at about -24 dB under a 60 BPM drone bed. |
| GXNWpGSkgBo | theme-to-theme-transition-list-differences-sentence-form-half-cadence-iv-start-borrowed-motifs-register-walk-hybrid-timbre-breath | arrangement-ambient-cinematic-score | **Transitions gap.** List the differences between the themes. Write an 8-bar sentence that starts on IV and ends on a half cadence in the new key. Carry the old theme's last figure in and foreshadow the new motif. Walk the register toward the new theme, share the line across a hybrid timbre, and leave a breath before the new theme. |
| IuscQShlL58 | end-of-bar-dissonant-pad-minor-sixth-over-root-resolve-on-downbeat-early-resolve-for-energy-drop-silence-break-freeze-reverb-size-riser | arrangement-loop-to-song-build-drop | **Tension-to-release gap.** A minor-sixth/fourth pad at each bar end resolves on the downbeat. An early resolve signals an energy drop into the breakdown. A few beats of silence come before the kick and bass return. A freeze-reverb riser's size is automated from consonance into dissonance. |
| POMnaOf92UI | four-part-dreamy-ambient-common-tone-imaj7-iii-loop-melody-grows-by-unmuting-notes-pad-filter-opens-grain-delay-shimmer-air-ramp | arrangement-ambient-cinematic-score | **Arrangement + air on pads (partial).** Four parts with an Imaj7 → iii common-tone loop. The track grows by un-muting melody notes, not by adding tracks. The pad filter opens over the whole track, and an automated grain-delay shimmer adds top-end air toward the end. |

Matt's preferences: the source's pad glide into the tense note and its random note generation (IuscQShlL58) were replaced with stepped notes. Randomised loop length and bass glide (POMnaOf92UI) were dropped. The binaural ramp is a slow planned glide, not random wobble. Drums enter early (~12 s) wherever a skill applies to a beat track. No health claims.

## Rejected (5), with notes in distilled/<id>/REJECTED.md
- uKpK0L-0KwA (carry-over): duplicate of the existing sleep/meditation loop-first arrangement variant. No isochronic content.
- z7xVfv8aByI (carry-over): hardware-specific Multigrain jam that relies on random pitch and tape wobble.
- jYrz49kwOWg (carry-over): generic bass archetypes already covered (bass cluster has 18 variants).
- mPJEfc6xqLA: thin (411 words), with solfeggio "pain relief" claims.
- v97MvZ1XhXM: Serum 2 bass tips that duplicate existing bass variants, plus portamento glide.

Skipped at title triage: filter/vocal/mixing-generic air hits (5xg_j4hEXQ4, AeqRNnYYsQ0, L9kuxISxOVo), pad VST/plugin promos (BTiaUMiEjHo, 8drCLZTLFHI, zk2-OTBQ8SI), and acoustic kick-muffling/mixing/beater hits (Z1_PzzV7TJg, UOuTV2n6xh0, hKDmV_qz7bQ, g6-pHXsa_aw, FPLs8HO16os, ifCHVRyLlJE).

## Carry-overs
None from yesterday remain. Candidates for later: PXN3t5p8MSM (short "Creating a binaural beat"), xy_NbX2SNSc (Serum 2 bass routines), and ambient arrangement hits -4ubGqqPHis, 43vkiBrPbug, bYO_-HPp1Mg and dBKqaNzXCPA.

## Searches
5 queries via `search_youtube_topics.py --skip-known`. Logs are in `batches/work-2026-11-24/`.

## Gaps still open
- Isochronic gate-rate ramp: the binaural side is now filled (k40nANMRnG4), but there is still no YouTube source for gating an isochronic pulse at a ramping rate. Write it in-house in `sample-lab/theory/entrainment_tones.py` (same staged plan, raised-cosine gate).
- Exciter/air on pads: partly filled (grain-delay shimmer + filter-open ramp). A dedicated exciter/saturation-air source is still missing.
- Soft/felt kick: open (only acoustic kick-muffling/mixing hits).
- Punchy bass: well covered already; nothing new.
- Pure phaser pads: partly filled (xO9CiDa3324, 11/23).
