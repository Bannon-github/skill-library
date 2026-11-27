# Morning synth YouTube hunt: 2026-11-27

Mode: compact library (fold-in). All new skills passed `quality_check_skill.py` (clean) and `novelty_check_skill.py` (NOVEL, best overlap <= 0.06). Each was folded into a cluster with `pipeline/compact/fold_in.py`. LIBRARY.json went from 304 to 308 entries (merge_log batch `2026-11-27-morning-hunt`). `mcp-publish/index.json` refreshed (33 skills), aliases updated. All transcripts are YouTube captions via the pipeline fetcher (yt-dlp / youtube-transcript-api); no ASR. `route.py` skipped to save tokens; videos gated by hand. Note: the box had been refreshed, so `.venv` was rebuilt from `pipeline/requirements.txt` (+ numpy/scipy/soundfile for sample-lab).

Fetches: 9 tried, 6 transcripts, 1 transcripts disabled (Ewrxt0X2lmw basic impact), 1 rate-limited twice (3KHYguJIz48 ambient Bitwig structure: carry over). Carry-over JhZU6JGvoHw fetched first try.

## Folded in (4 from YouTube + 1 in-house)
| video | skill id (alias) | cluster | goal |
|---|---|---|---|
| JhZU6JGvoHw | punchy-deep-kick-tuned-to-track-root-... | drum-synthesis-and-hybrid-percussion | **Punchy kick gap.** Sine sub 2 oct down tuned to the track root, hold ~100 ms / decay ~100 ms, unipolar pitch env falling onto the note, same env on a driven LP, low one-shot noise attack, cut 300-400 Hz, transient shaper, compression attack trade-off. |
| 8eAQ0VdW0Cw | soft-felt-to-punchy-kick-dial-... | drum-synthesis-and-hybrid-percussion | **Felt kick gap.** Kick = attack + tone; character = pitch-env amount x time (tom/zap, click, punch, soft); soft/felt body plus a separate blendable attack layer (short pitch-dropped saw or short band-passed noise); FM body / drive options. |
| mxUQyUs1eGo | kick-punch-compression-threshold-...-40ms-attack-...-200ms-release | drum-synthesis-and-hybrid-percussion | **Punchy kick processing.** Threshold on the top section only (~-10.5 dB), 3:1, ~40 ms attack keeps the transient, ~200 ms release, ~+2.3 dB make-up, loudness-matched A/B. |
| 0qOs9e5UwAU | four-role-atmospheric-pad-...-key-tracked-noise-sample-... | brightness-and-air-at-the-source | **Air on pads gap.** LP low wavetable layer (1-bar position LFO), HP harsh high layer +1 oct on a free-rate position LFO (air), unfiltered +1 oct triangle for pitch, key-tracked noise sample through the HP; chorus, light phaser/flanger, ping-pong 1/4 delay, big reverb, EQ placement, detune macro. |
| (in-house) | isochronic-staged-gate-rate-ramp-phase-integrated-raised-cosine-edges-fixed-carrier | brainwave-binaural-isochronic-layers | **Isochronic gate-rate ramp gap (closed in-house).** Hold -> linear glide -> hold, gate phase = cumsum(rate)/SR so pulses never jump, ~4 ms raised-cosine edges capped at duty/2, fixed carrier. Code: `sample-lab/theory/entrainment_tones.py` `iso_ramp()`; render `out/entrainment_gate_rate_ramp.wav` (12 -> 6 Hz, measured 12,12,11.5,...,6.5,6,6). Not a LIBRARY entry (no video). |

Matt's preferences: kick attack layers are one short transient per hit (no rapid clicking); pitch drops are single smooth falls; pad LFOs move wavetable position only (free-rate but periodic, not random); iso ramp glides only, fixed carrier, no clicks. Drums by ~8 counts noted in each kick skill. No health claims.

## Rejected (1), note in distilled/<id>/REJECTED.md
- R3nsI3ZF0Vs: FL Studio cinematic impacts; sample-layering + glitch plugins, no synthesis steps; glitch conflicts with no-clicking rule; layered-hit idea already covered.

Skipped at title triage: 7rU85SaXsso / dbMa8g_jV2I / TpJ1EAerPN4 / ESKIgW-UWlE / n6ew5mMN2pQ / wYKf4o5-9iM (saturation plugin tours / vocal saturation, not pad air), vr0DHvuQX8E / 3lHVhdM83LI (Serum kick, overlaps today's kick folds), ndG-6-vONNc (27-min FM real kick, possible later), eE1Xg2BU_JE (product overview), I66_LmOTlSk / tzfzkTAQsnE (skipped before), OnDipGYsvEc (DnB foghorn), zSFZT79qiug / 7qQX6YGBQEA / Pj8JO_0qTa4 (general synth tutorials/stream), S8ijTLf-12s (phaser leads, not pads), uUOXzvOa7po (38-min ambient blueprint; too long for a lean run, possible later).

## Carry-overs
- 3KHYguJIz48 (From Blank Project to Full Ambient Track in Bitwig, song structure): rate-limited twice.
- Possible later: uUOXzvOa7po (ambient track blueprint, 38 min), ndG-6-vONNc (FM real kicks), TfwO3el-i1A, WZXXOkZ4-MM, kzkDoBupXKM (from 11/26).

## Searches
5 queries via `search_youtube_topics.py --skip-known`. Logs in `batches/work-2026-11-27/`.

## Gaps still open
- Pure phaser pads: still partial (today's only phaser hit was leads; pad recipe uses phaser as light colour only).
- Hybrid cinematic impact: still open (Ewrxt0X2lmw transcripts disabled, R3nsI3ZF0Vs thin).
- Exciter/air on pads: improved (four-role pad air layer) but no dedicated exciter recipe yet.
- Isochronic gate-rate ramp: closed in-house today.
- Punchy/felt kick: largely closed (3 kick folds).
