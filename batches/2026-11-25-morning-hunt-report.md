# Morning synth YouTube hunt: 2026-11-25

Mode: compact library (fold-in). Every new skill passed `quality_check_skill.py` (clean) and `novelty_check_skill.py` (NOVEL, best overlap 0.058–0.075). Each was folded into a cluster with `pipeline/compact/fold_in.py`. LIBRARY.json went from 298 to 302 entries (merge_log batch `2026-11-25-morning-hunt`). `mcp-publish/index.json` refreshed (33 skills), aliases updated. All transcripts are YouTube captions via the pipeline fetcher; no ASR. `route.py` skipped to save tokens; videos gated by hand.

Fetches: 13 tried, 9 transcripts, 4 with transcripts disabled (PXN3t5p8MSM, -4ubGqqPHis, hs7qpZthGlc, IWUVd0fiyH4). Some rate-limit retries, all recovered.

## Folded in (4)
| video | skill id (alias) | cluster | goal |
|---|---|---|---|
| YdnMi_TIXso | ambient-zone-owners-low-a1-body-150-800-focus-air-hand-off-foreground-one-sequence-quiet-noise-minus-20-establish-expand-contrast-return | arrangement-ambient-cinematic-score | **Arrangement gap.** One owner per frequency zone (bass on the key root, body 150–800 Hz, focal voice, air noise at about -20 dB). Depth comes from level, attack, brightness and reverb. Hand off the foreground to one new sequence per section, then shape the sections as establish → expand → contrast → return, with something new on the return. |
| oRhBZ6L9rU8 | acoustic-style-kick-four-layers-sine-body-pitch-env-phase-offset-transient-osc-faded-in-sample-layer-hp-filtered-short-pink-noise-tail | drum-synthesis-and-hybrid-percussion | **Drums / soft-kick gap (partial).** Acoustic-style kick from a sine body with +12–24 st pitch envelope, a phase-offset transient oscillator, a one-shot sample layer faded in after the transient and high-passed, and an optional quiet pink-noise tail, then EQ and fast-attack compression. |
| 2faaqrLjTs8 | empty-loop-seamless-drone-loop-record-silent-counted-loop-first-then-overdub-wet-only-reverb-drone-no-seam-gap | generative-ambient-drones-and-soundscapes | **Loops gap.** Set the loop length first with an empty, counted loop (in a DAW, a fixed bar-locked loop), then overdub wet-only long-reverb drones so there is no cut or click at the seam. |
| RDubhupxDsw | tempo-synced-autopan-phase-360-amplitude-gate-on-long-ambient-texture-shape-softened-edges-reverb-after-gate-amount-as-on-off | brainwave-binaural-isochronic-layers | **Isochronic gate (fixed rate).** Auto-pan in beats mode at 1/16 with phase 360 becomes an on/off volume gate (BPM/15 Hz). Soften the edges with shape/waveform, add reverb after it, and automate the amount per section. No rate ramp in the source. |

Matt's preferences: random comb-filter modulation (YdnMi_TIXso) dropped; kick oscillators use random phase 0, the transient is one attack per hit, and the noise tail is optional (mute if it reads as a per-beat tick); the gate uses rounded edges with reverb after it to avoid clicks; drums enter early (~10–12 s). No health claims.

## Rejected (5), with notes in distilled/<id>/REJECTED.md
- xy_NbX2SNSc (carry-over): generic wub bass routines with randomly picked warps; bass cluster already has 18 variants.
- 43vkiBrPbug (carry-over): beginner overview plus a masterclass pitch. Thin/promo.
- bYO_-HPp1Mg (carry-over): short five-section chillhop walkthrough; covered already, and its 40 s drumless intro conflicts with the early-drums preference.
- dBKqaNzXCPA (carry-over): hardware jam built on tape warble, random bend/break and vinyl pops.
- UbXpr5JV-Ps: transition sample-pack promo.

No transcript (transcripts disabled; dropped, not carried over): PXN3t5p8MSM, -4ubGqqPHis, hs7qpZthGlc (envelope-controlled phaser), IWUVd0fiyH4 (punchy snare).

Skipped at title triage: GL0r3HNblNI (Mind Workstation tempo editing, product-specific), BE4UV4HbPWw (sleep-hack hype), -B13nDMxC1k / I66_LmOTlSk (film editing/sound design for video), 3brTqe70XpU (Octatrack live-set prep), ZdKxOsK4nQ8 (old Serum FX overview), 5d7EYDdx2QU, u07PCfvBiYs (guitar pedalboard), lnG7_h6XDBQ, Y3IHvWksrLE, RdGYObhhhKQ, IkkT48T-fBQ (DnB clap/snare), Fr2ci50JsW8 (50 min Reason overview).

## Carry-overs
None outstanding. Candidates for later: lnG7_h6XDBQ (ambient texture rack breakdown), 5d7EYDdx2QU (slice-to-sampler evolving textures), Fr2ci50JsW8 (punchy drums + deep bass, long).

## Searches
5 queries via `search_youtube_topics.py --skip-known`. Logs are in `batches/work-2026-11-25/`.

## Gaps still open
- Isochronic gate-rate ramp: fixed-rate gate now sourced (RDubhupxDsw); a ramping-rate gate still has no YouTube source. Write in-house in `sample-lab/theory/entrainment_tones.py` (staged plan, raised-cosine gate).
- Pure phaser pads: still partial (envelope-controlled phaser video had transcripts disabled).
- Soft/felt kick: partial (acoustic-style layered kick); a dedicated soft/felt kick is still missing.
- Exciter/air on pads: still partial.
- Punchy bass: well covered.
