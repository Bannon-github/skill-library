# Morning synth YouTube hunt: 2026-11-16

Mode: compact library (fold-in). No standalone skills were published. All 4 new skills passed `quality_check_skill.py` (clean) and `novelty_check_skill.py` (NOVEL, 0.90–0.93). I hand-checked each against the target cluster's variants and folded it in with `pipeline/compact/fold_in.py`. LIBRARY.json went 274 → 278 entries (merge_log batch `2026-11-16-morning-hunt`). `mcp-publish/index.json` was refreshed (33 skills) and the new ids resolve through `mcp-publish/aliases.json`. All transcripts are YouTube-provided (pipeline fetcher, auto-generated tracks). No Whisper/ASR was used.

Rate limiting was heavier than on 11-13. L9mQwW3ik_A and IH-zpS7gxxg failed on the first pass and were fetched on a second pass. 5XGrxp0ANME and TYU764RIkmE stayed `rate_limited_or_ip_blocked` after 3 retries and are carried over. `route.py --domain synth` returned CANDIDATES_READY for all 7 routed ids, including clear rejects (the false-novel pattern continues), so every result was hand-checked.

## Folded in (4)
| video | skill id (alias) | cluster | one-line goal |
|---|---|---|---|
| 00oV6DJkK3E | binaural-rate-ramp-eased-symmetric-offset-gearbox-dwell-shift-band-steps-harmonic-same-gap-isochronic-blend | brainwave-binaural-isochronic-layers | **Rate-ramp layer (gap now partly closed).** The beat rate moves over time while the carrier centre stays fixed (L = c − b/2, R = c + b/2). Two modes: one eased ramp (e.g. 6 → 1.5 Hz over minutes), or "gearbox" band steps (16 → 10 → 6 → 2 Hz, dwell about 4 min, shift about 1.5 min) with return-trip or fade-out endings. Also a same-gap harmonic pair, an isochronic blend for speakers and a brown-noise bed. Product demo distilled to portable automation; vendor "phi/intention" presets omitted. |
| rEXT0z75IyQ | orchestral-ostinato-bounce-to-sampler-octave-down-half-speed-pulse-stack-drive-filter-fader-console-shimmer-granular-position-modwheel-scan-remarry-live-orchestra | granular-and-spectral-texture-design | **Orchestral-sample manipulation hybrid (gap partly closed).** Bounce a string ostinato into a repitch sampler and stack it 0/−12/−24 (half and quarter speed) into a pulse. Chain: drive → fader-mapped morph filter → console comp → shimmer verb. Then a granular position scan on the mod wheel, and the result is blended back under the real orchestra. |
| X2xijc3S8cc | pad-vs-drone-roles-aux-verb-as-cohesion-layer-ensemble-split-octave-displace-tuned-field-drone-octave-copy-top-down-mix-drone-last | mix-eq-gain-staging-and-balance | Pad + drone bed from synth to mix. The aux reverb is treated as a cohesion layer. Chords are split between two layers (bottom 2 / top 2 notes, octaves +2/−1). A key-tuned field-recording drone gets a −2 oct double. Top-down mix: pad EQ'd around bass and vocal, light sidechain, drone in last at barely audible level. |
| MycI9ZOSPRk | ambient-meta-chord-loop-2-4-chords-one-step-voice-leading-mixed-interval-extensions-no-dominant-7-first-inversion-v-bvii-constant-ostinato-line | harmony-chords-voicing-and-slow-motion | Ambient "meta-chord" loops (David Wise-style): 2–4 chords with one-step voice leading and mixed-interval extensions, no dominant sevenths, V/bVII in first inversion, and one constant ostinato over every chord so dissonances become expected. |

Matt's preferences are written into each skill's constraints: steady pitch (dropped the granular "speed" spray and the stepped pitch-pulse effect from rEXT0z75IyQ, and the tape wow/flutter on X2xijc3S8cc's melodic pad). Rate ramps are eased with no random segments. Ostinatos stay fixed. Drums enter early (~8 counts / ~12 s). Everything is Ableton/MIDI-friendly with portable module mapping.

## Rejected (6)
- **4sereDbtdLw**: kick tuning opinion piece. Only "shorten + fade, transpose until it sits vs the bass", which is thin and covered by drum-synthesis.
- **sfO-0ht06SE**: looped envelopes / sequenced modulation. Thin (459 words), randomised steps, covered by the modulation cluster.
- **-QIN_4VybDQ**: hardware cassette tape loops. Hardware-specific, with a varispeed/pitch wobble sound. The portable part is covered by the looper-drone variant.
- **QPfIOH-CWhU**: Ableton delay device tour. Mostly random/glitch/physics-driven pitch (against Matt's taste). Grain-delay shimmer is already covered.
- **L9mQwW3ik_A**: "Positive Tension Filmmusic" walkthrough. The YouTube English track is garbled, so there was nothing groundable.
- **IH-zpS7gxxg**: the Two Loop Rule. Covered by arrangement-loop-to-song (rule of three, 8-bar A/B/A/C, four levels), relies on drum rolls, and ends in a course pitch.

Seen but skipped (beginner, product, off-genre, meditation uploads or duplicates): EbuQ2QYKTDg, 43vkiBrPbug, vHXi__0HQrk (glitch drums), 5v8KKg-hDP0, lADxAw8mtQQ, QE34PIkcRVo (product), 2-DxdKlp2XM, 6JkPQuaad80, mh8jV6IGI84, wuEFMBeLRwc / 6U_eHEhywlw / lI4YojaYPco / 0VYu_LBMG0s / lkXxL1OZmVU (meditation audio, not how-to), 0FmzFpHdwrc / APljvOxetas (lo-fi basics), UOuTV2n6xh0, NrqSbPBfMLg (drum loop), Or-lJzKVnRw, TpJ1EAerPN4, P9BAoDvC1e4 / cSbVsBbWlRg / bRPvvCnjQlI / UEQEDyKGl8g / sEC4_GYEbjk (mixer/hardware manuals), UF45TAe9KRg, ezuUuP_DJAI, Bzvn_6toM6M, uAQA7mPAI2g (seen), IJBnFIRKzTk, ZdKxOsK4nQ8 / uhC-5pwVHLw (phaser manuals), ZX62ADNX8ss / ZdhdC2wx2Ew / YF86PC5mTFE (beginner orchestration), 196-smqHUnY, -skr-sFCN9Q, jeHA_ndlNd4 / 3pO0wHhDMEs (product pads), N1gBBXJFh9k, huzpYujBGns / kwIFZQIuDtk / dFR57D7cFcs / 8whhdvA0hV4 / aIKhjXbjKUg (reese, bass cluster deep), lcnjiOU-0YA, JGGnla8RKP4, ZsADjChOVYE, 6UJIWjo-8g0, 7wcJShg8tn4 (vocal FX).

## Searches (2026-11-16)
`search_youtube_topics.py --skip-known` (240–3600 s): ambient breakdown without drums; building tension in ambient without drums; binaural beat frequency ramp over time; soft lo-fi kick synthesis; exciter/saturation air on pads; orchestral sample manipulation hybrid; phaser pad sound design; cinematic soundtrack arrangement structure; modulation for evolving pads; reese bass sound design; creative delay/reverb FX chains. Logs are in `batches/work-2026-11-16/`.

## Gaps still open
- **Brainwave rate-ramp:** now covered by the eased-ramp/gearbox variant. Still wanted: an isochronic-specific ramp (gate rate automation in a DAW) and a render generator in `sample-lab/theory/`.
- **Drumless ambient breakdowns / ambient build & breakdown transitions:** still open. Searches returned beginner ambient, glitch-drum or EDM content.
- **Soft/felt ambient kick + sub:** still open. Hits were lo-fi basics, kick-tuning opinion pieces and mix-frequency lists.
- **Exciter/air on pads:** still open. "Exciter" queries return live-mixer hardware manuals. Try "harmonic exciter synth pad" or "Aphex aural exciter on pads" next time.
- **Orchestral-sample manipulation hybrid:** partly closed. A deeper one on stretching or reversing orchestral hits is still wanted.
- **Pure phaser pads:** still open. Only plugin-manual phaser chapters came up.
- **Song structure for ambient/cinematic:** the harmony side improved with the meta-chord loop rules. Arrangement-only hits were beginner orchestration or EDM.

## Carry-overs
- **5XGrxp0ANME**: "Why 80s Pads Sound So Good (And How to Make Them)". Rate-limited after 3 retries.
- **TYU764RIkmE**: "Sound Design - Deep Reese Bass Tutorial". Rate-limited after 3 retries.
