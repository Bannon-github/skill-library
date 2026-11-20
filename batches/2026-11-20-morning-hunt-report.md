# Morning synth YouTube hunt: 2026-11-20

Mode: compact library (fold-in), same as recent hunts. No standalone skills were published. All 5 skills passed `quality_check_skill.py` (clean) and `novelty_check_skill.py` (NOVEL, best overlap ≤0.12). I hand-checked each one against the target cluster's variants and folded it in with `pipeline/compact/fold_in.py`. LIBRARY.json went 285 → 290 entries (merge_log batch `2026-11-20-morning-hunt`). `mcp-publish/index.json` was refreshed (33 skills), and the new ids resolve through `mcp-publish/aliases.json` (checked with youtube-skills `get_skill`). All transcripts are YouTube-provided (pipeline fetcher). No Whisper/ASR was used. `route.py` was skipped to save tokens; it returned CANDIDATES_READY for everything in recent runs, so I gated every video by hand instead.

## Folded in (5)
| video | skill id (alias) | cluster | one-line goal |
|---|---|---|---|
| CW3jk3BgE1E | ambient-variation-sets-per-voice-presence-focus-map-frequency-slot-plan-texture-pad-melody | arrangement-ambient-cinematic-score | **Song-structure gap.** Build an ambient track from three voices (texture, pad, melody). Each voice gets lettered variations (filter low/mid/high, attenuated slow modulation), chained along a presence/focus map (focus, not volume) and matched to a low/mid/high frequency-slot plan, so the layers never fight. |
| JHiTUBVLmFI | dynamic-interest-16-bar-block-map-top-perc-gear-shifts-break-turnaround-squeeze-in-markers-reverses-plus-minus-layers-scoop-up-minimalism | arrangement-loop-to-song-build-drop | **Structure/breakdown gap.** Draw 10 blocks of 16 bars and plan: top-percussion gear shifts at every block, one committed break vs. half-block turnarounds, 1–3 bar squeeze-ins, sparing markers/reverses, +/− density from call-and-response or polymeter layers, scoop-ups and minimalism moments. |
| VSGYqvV4bTg | delay-as-instrument-mono-checked-haas-sweet-spot-delay-built-chorus-flanger-100-feedback-repitch-octave-looper-grain-delay-octave-shift | reverb-delay-space-and-shimmer | **Loops gap.** A 100%-feedback delay looper with overdubs. Repitch-mode delay-time halving/doubling gives clean octave steps (step up in the 2nd half to build energy), feedback 0 kills the loop, then resample it to audio. Also: chorus/flanger built from a delay, a mono-checked Haas sweet spot, and a 1 ms grain-delay octave shifter. |
| LcAcmBKryxE | correlation-meter-widening-haas-comb-fail-stereo-phaser-ms-side-gain-linear-vs-detune-chorus-multiband-width-map | stereo-width-haas-midside-mono-safe | **Stereo width / phaser gap (partial).** Widen while watching a correlation meter. Pure Haas is rejected (it combs in mono). Use a stereo phaser plus M/S side gain, pick linear vs. detuning chorus by source, and finish with a per-band width map: mono lows, slightly narrower low-mids, widest upper mids (correlation touches but never crosses 0), restrained highs. |
| haZ6byjMpOk | async-dual-bandpass-sweep-micro-loop-texture-parallel-delays-octave-down-lane-slow-autopan-bus | generative-ambient-drones-and-soundscapes | An evolving bed from a captured micro-loop: two parallel narrow band-pass lanes swept by unsynced slow LFOs, delays, an octave-down lane, and a summed bus with a very slow, also unsynced auto-pan. |

Matt's preferences are written into each skill's constraints. **Steady pitch:** VSGYqvV4bTg drops the random-LFO tape repitch and the echo "wobble"; its octave moves are exact 2:1 steps. CW3jk3BgE1E drops the random playback-speed modulation on the sample. LcAcmBKryxE keeps chorus subtle on held pads. haZ6byjMpOk moves only filter, delay and pan. **No clicking:** grain spray and delay feedback are capped, and JHiTUBVLmFI prefers soft, long top percussion over busy hat rolls. **Drums early:** ~8 counts / ~12 s. Everything is Ableton/MIDI-friendly.

## Rejected (8)
- Of6RLgo_XNI (Eno *Music for Airports* loops in Koala): covered by the uneven-loop-length and varispeed variants.
- Vx94sNJpu1c (Advanced Serum complex pad): preset walkthrough; its LFO-on-detune creates pitch wobble.
- oy8Cr-U2pwA (techno kick): covered by kick heart + transient; it adds a click top layer.
- 2bvdVDRpfAQ (ambient for beginners): beginner diatonic chord theory, already covered.
- -L-vpN2QZVc (ambient automation): beginner fades, and it ends on an LFO wobble.
- Jm06aG3hAr4 (suspense film music): music-only layer demo, thin.
- rd3-k_tJ4Po (plucky bass) and l1pxzjfwX1c (Zebra punchy bass): generic, already covered by the bass cluster.

## Carry-overs / no captions
- Transcripts disabled (dropped): DU_Wu9OBCCw.
- Rate-limited today (carry over): z7xVfv8aByI (Multigrain resampling, ambient), jYrz49kwOWg (3 basic bass patches).
- Already resolved on 2026-11-19 (rejected there, not retried): 5XGrxp0ANME, zEkCere2A_Y.

## Searches (2026-11-20)
`search_youtube_topics.py --skip-known` (240–3600 s) on 7 queries: film score cue structure tension release; ambient breakdown and drop-return arrangement; felt kick ambient low-pass transient; harmonic exciter synth pad air; phaser pad synth sound design; isochronic tones how to make; punchy bass synth sound design. Logs are in `batches/work-2026-11-20/`.

## Gaps still open
- **Isochronic gate-rate ramp:** still none on YouTube (only 1-hour listening tracks). Write it in-house in `sample-lab/theory/entrainment_tones.py`.
- **Exciter air on pads:** still open (hits were plugin demos, HISE, mixers).
- **Pure phaser pads:** still open. Only plugin-manual phaser chapters came up, but LcAcmBKryxE now covers the phaser as a widener.
- **Soft/felt kick:** still open (search returned generic sound-design videos).
- **Cinematic cue structure (tension → release):** still thin. Hits were music-only demos or long podcasts. yMJaUS776yQ (52 Cues podcast, 46 min) and efnKT5pHqUo (melodic cells for action cues) are worth trying next.
- **Breakdown → drop return inside an ambient beat track:** partly filled by JHiTUBVLmFI (break vs. turnaround vs. scoop-up).
