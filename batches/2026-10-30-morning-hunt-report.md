# Morning synth YouTube hunt — 2026-10-30 (PT)

## Counts
- MCP count: 211 → 221 (index.json count = 221 = files in mcp-publish/skills). LIBRARY entries 209 → 219. Taxonomy cinematic-hybrid-synth 173 → 183; curriculum level 3 142 → 152.
- New skills: 10. Rejected: 21 (all hand-read). No transcript: 0 (the 5 first-pass NO_TRANSCRIPT results were rate limits, and all 5 succeeded on retry). Searches: 8 (1 isochronic). Transcripts fetched: 31 of 31 tried (12 s spacing, raised to 20 s after the rate limits; 18 s between searches). Crypto pivot: no.
- State backup first: `backups/2026-10-30-morning-hunt/`. Work files: `batches/work-2026-10-30/` (mk.py, c1–c8.py, publish.py, fetch.sh, fetch2.sh, search.sh, queries.txt, search.log, fetch.log, retry.log, fetch2.log).
- 10-29 morning hunt: FAILED with no trace in the repo (no report, work dir, backup, raw/ or distilled/ files; git was clean and synced with origin). The 10-29 daily test is also missing. It most likely failed at the scheduler/agent level before any step ran, so nothing to clean up and nothing broken. Its carry-overs were folded into today's hunt.

## Published (10)
Pads / brightness / phaser:
- `eno-space-pad-sines-0-12-19-st-triangle-sub-…-modulated-fx-mix` ← Oq5TCAKw64Y (carry-over): a planetarium/Eno space pad on any synth. Sines at 0/+12/+19 st plus a triangle sub; two free-running smooth-random LFOs modulate each other's rate and are mixed on every target; LFO-moved reverb/delay mix. Pitch stays steady. Novelty max 0.123.
- `eerie-dreamy-phaser-pad-supersaw-keytracked-cutoff-dual-slow-stereo-phasers-…` ← XRCwoFjZFMc (carry-over): a supersaw pad with key-tracked cutoff, two slow stereo phasers at low resonance, a ~0.5 s modulated delay, a 1.5 s ping-pong delay and reverb, and a cyclic envelope/LFO on cutoff. Fills the phaser-pad gap. 0.138.
Cinematic FX / sound design:
- `one-note-horror-soundscape-stacked-triad-chord-shifts-…-range-limited-glider` ← 2Yt1Ae91fv0 (carry-over): a horror soundscape played from one held note (stacked chord shifts, osc spread, LP 170 Hz with wandering resonance, parallel wet ping-pong). Note: the shifts as spoken (+4 +7 +13 +17 +20) give C plus Db major, not the C plus A the speaker names. 0.130.
- `distant-explosion-boom-from-synth-tom-sub-enhance-6db-…-low-comb-metal-drop` ← ZYn08bUlmG0 (carry-over, Epic Drums 2): a distant explosion boom made from a synth tom (sub enhance +6 dB, LP'd reverb, 100 Hz low cut, stereo offset, quarter delay, delayed tremolo/auto-pan, low comb). 0.114.
Drums:
- `synth-drum-ensemble-four-instances-same-midi-per-hit-random-env-delay-0-22ms-…` ← ALHZHHPAdI0 (carry-over, Epic Drums 3): four synth-drum instances play the same MIDI with a random 0–22 ms per-hit envelope delay, varied decay/snap/EQ and ±40 pan, so it sounds like an ensemble. Timing jitter only, no pitch. 0.114.
- `resample-synth-epic-drums-to-sampler-8-velocity-layers-vs-round-robin-…` ← w8cSlVZ2KbI (carry-over, Epic Drums 4): resample synth drums into a sampler with 8 velocity layers or round-robins to avoid the machine-gun effect; velocity → LP up to about 1.5 kHz; start-offset jitter; bounce the ensemble. 0.107.
- `spacious-ambient-drums-accent-mapped-sparse-kick-bar-one-ghost-snares-bars-2-4-…-ducked-noise-bed-3s-release` ← BcbSwdsC7W8: sparse drums under slow pads. Map the accents first; kick only in bar 1 (plus a ghost note) of each 4-bar phrase; snares on bars 2 and 4 with reverse reverb only before bar 4; double-tempo grid for hat ideas; 2-bar LFO on an EQ for alternating hat brightness; noise bed ducked by percussion (about 3 s release, −13 to −17 dB). Novelty 0.108 vs loop-is-the-climax.
- `future-garage-ambient-drum-groove-halftime-kick-rim-…-freq-shift-self-vocode-halfnote-duck-12bit` ← e4zq3HQdcIY: a future-garage/ambient groove built in layers with hand-loosened swing, reversed flair hats and faded Foley chops. Processing: LP24 kick at about 1 kHz / 30% res, rim at about 1.5 kHz, a static −898 Hz frequency shift on hats, rims vocoding themselves, 6.1 Hz unsynced pan/phaser, a half-note duck and 12-bit lo-fi on the bus.
Song structure / arrangement / transitions:
- `three-track-cinematic-sketch-lp-filter-close-open-reverb-swell-on-runs-…-tempo-ramp-contrary-motion` ← 0Jj5qQQzDLU (carry-over): a three-track cinematic sketch where every transition is automation only (LP close/open, reverb swells on runs, rhythmic auto-filter mix), with a tempo ramp of 95→100→115 and contrary motion. 0.103.
- `three-riser-free-transitions-solo-lead-pad-filter-down-…-short-fill-all-in` ← vzlZ4GabrAs: three section transitions by subtraction and re-entry instead of risers or snare rolls (solo lead plus pad filter-down; clap with no kick, HP bass and a single tom hit; strip to hats, tease the lead, short fill, everything back at once). 0.130.

Checks: quality_check --strict 10/10 clean. Library-wide non-strict: 221 checked, 0 failed, 28 warned (same 28 as before, none new). novelty_check: 10 NOVEL (max 0.141 → today max 0.138). For all 10: distilled/ copy = mcp-publish/ (JSON-identical), listed in index.json, LIBRARY.json, taxonomy, curriculum L3 and skills/*.md. The youtube-skills MCP search_skills returns the new skills (spot-checked: future-garage, eno-space-pad, riser-free).
Matt-taste constraints are on every skill: steady pitch (random pitch/detune/delay-time modulation off or tiny), drums entering early (by about count 8), portable recipes.

## Rejected (21)
- lLaJk7ALJWY (ambient/FX tracks): thin. G4u4BBDdtdE (Harmor pads): rambling, vague. CuF7pb3Hw1E: Keepforest plugin promo. 9MCc7wbYFQU (Harmor watery phaser bass): plugin-heavy rambling (Disperser/OTT/Serum FX).
- pJ_mM8s3Cyo (UAD A-Type walkthrough): plugin walkthrough. Brightness facts kept here: an aural exciter adds no new harmonics, it raises existing low-level detail; Excite about 29% amount at full mix; Air mode works on high bands only, amount 100 with mix about 12% ("a little goes a long way"); Crush mode works as parallel compression, and a tilt sidechain makes it react to highs.
- CPlLPFNRFJk (comb pad): covered by cinematic-formant-comb-pad-phaser-fx. zjRTE41iu7s and s8zR_x_cWZM (stereo width): covered by the Haas/width skills.
- zGkWtpmu31Y (Vital random-of-random soundscape): covered by the random-rate LFO and wavetable skills; its pitch-random noise goes against Matt's taste.
- 69LMnU3GwLo (isochronic via arpeggiator): covered by the isochronic skills. Delta: an ms-mode rate keeps Hz constant under tempo automation, synced mode does not.
- k7ZJge24Xbo (underwater pad): generic, short. HTLPQgNkXyc (Ableton texture-mode warp): Ableton-locked, no values. SXgvMseKTDg (atmospheric pads): preset-based, vague.
- OfdrYDJ-NnA (physical cassette tape loop): hardware craft, and the tape warble goes against the steady-pitch taste. Loop ideas: one chord per loop faded in and out; half speed gives an octave down.
- EdDmm4LT_dw (loop to finished track: reference markers, energy map, root vs progression, filter → space → FX automation order): covered by loop-is-the-climax, the three-track sketch and the section transition toolkit. Delta: automate filters first, then reverb wash in/out, and only then add risers/crashes as "icing".
- uXl7iyyZF1M (punchy bass: transient splice with an inverted envelope crossfade, high-RMS sub, soft clip, OTT without upward compression): covered by transient-splice-attack-body-hybrid-voice and four-punchy-bass-archetypes; ends in a preset/sample-pack promo.
- 7xpMahhQoRA (rock band console mixing, Black Rebel Motorcycle Club): off-domain.
- 8nO5fje8OHI (hypnotic phaser sounds): rambling and few values (phaser feedback 40–50, two notches, phaser rate 16–64 Hz as an "oscillator", tiny-room reverb). Today's XRCwoFjZFMc covers the phaser pad.
- kX-ic0o-9Ac (reversed shimmer riser from any sound): covered by reverse-reverb-swell and the shimmer/pitch-ramp riser skills; vague values.
- 62oV1qEFjmI (song structure from a reference track in 8-bar blocks): covered; ends in an Ableton rack promo.
- jl8PFbT6iv0 (modular FM bell plus detuned wavetable pad): vague, generic.

## No transcript (0)
- None. The first pass had 5 false NO_TRANSCRIPT results from `rate_limited_or_ip_blocked`, and all 5 fetched fine on a later retry. No ASR used.

## Pipeline notes
- Rate limits: after about 15 fetches at 12 s spacing YouTube returned rate_limited_or_ip_blocked. Retrying later at 20 s spacing (fetch2.sh) cleared every one. fetch.sh only prints the last 4 lines, so grep the fetch log for the reason before counting anything as no-transcript.
- Brightness: "saturation for air on pads" / "parallel distortion pad brightness" still return mostly plugin walkthroughs (UAD A-Type). The only usable facts are recorded under pJ_mM8s3Cyo above. The gap is still thin.
- Isochronic: one search only, no new how-to (69LMnU3GwLo covered). The session arc should be composed from existing skills, not hunted.
- Backgrounded `cd X && (...) &` keeps the main shell's cwd. Use absolute paths in work scripts.

## Carry-overs for the next hunt
- Isochronic hits vYRIXi4A6CU, hfjLuqOK9Co (low priority).
- From 10/22: MH7YiOWQIhI / kHWOIE4YTZ4 still queued for tlang upgrade.
- Gaps: brightness (try "high shelf vs exciter on pads A/B", "bit crush before reverb brightness", or a composed skill from the mnledZoD4QE + A-Type notes); punchy bass (today's hit was covered, try "sub bass layering for ambient"); isochronic session arc (compose). The 10-29 daily test was missed.
