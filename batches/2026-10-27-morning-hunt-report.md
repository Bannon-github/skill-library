# Morning synth YouTube hunt — 2026-10-27 (PT)

## Counts
- MCP count: 198 → 205 (index.json count = 205 index entries = 205 files in mcp-publish/skills, no duplicate ids). LIBRARY entries 196 → 203. Taxonomy cinematic-hybrid-synth 160 → 167; curriculum level 3 129 → 136.
- New skills: 7. Rejected: 9 (5 hand-rejected + 4 route.py COVERED). No transcript: 1. Searches: 8. Transcripts fetched: 16 of 17 tried (no 429s; 12 s spacing between fetches, 15–20 s between searches). Crypto pivot: no.
- State backup first: `backups/2026-10-27-morning-hunt/`. Work files: `batches/work-2026-10-27/` (mk.py, c1.py, c2.py, publish.py, search.log, fetch.log, new.txt).
- route.py run on the 9 carry-over IDs: 5 CANDIDATES_READY, 4 COVERED. The 8 newly found IDs were hand-read and checked with novelty_check.

## Published (7)
Song structure / arrangement (priority 1):
- `loop-is-the-climax-give-away-arrangement-…-mirrored-outro` ← gIVUpqVRf-w (10/26 carry-over): the loop is the climax. Give it away gradually by element, by element power (kick high-passed at about 120 Hz, thin HP+LP bass) and by harmony (root pedal before the progression). Something changes every 8 bars, the kick drops out for 1–2 bars before each drop, and the outro mirrors the intro. Novelty REVIEW 0.183 vs the eight-bar build-up skill; kept as more specific (delta stated in constraints).
- `four-levels-loop-to-story-arrangement-…-additive-cinematic-start-from-silence` ← xY7vRHiSJSM: four levels. (1) Subtractive "Lego blocks" shaped by an energy contour. (2) A turnaround before each section edge and a marker on it. (3) One performed "protagonist" element that crescendos then decrescendos. (4) An additive cinematic pass that starts from silence.
- `ambient-three-layer-starter-…-sustainless-stepped-filter-detail-voice` ← CRWBHFIikqc (10/26 carry-over): three layers composed by frequency region. A slow wavetable pad (4-bar bipolar WT-position LFO, random cutoff, unfiltered osc B auto-panned over 2 bars), a saw+sine bass pad through a 24 dB low-pass, and a sustain-less detail voice with a sample-and-hold stepped filter.
Drums / punchy bass (priority 3):
- `synth-drum-kit-from-scratch-808-…-hats-test-in-context` ← xlBInB7BOzE (carry-over): 808, kick, clap, snare and hats built from sine and noise with envelope-drawn transients, fast pitch envelopes and targeted EQ (gentle 20 Hz HP, about 78 Hz notch, clap at 1 kHz/6 kHz).
- `four-punchy-bass-archetypes-808-…-sub-sine-5ms-attack` ← H6i55lXAMh0: 808 with a 35 ms pitch-envelope punch (and an 80–100 ms attack delay when the kick already has punch), mono pluck with a wide unison top, LFO-ducked saw growl, click-free sine sub.
Pads / brightness / width:
- `self-sustaining-shimmer-pad-…-99pct-feedback-asymmetric-stereo-delay-…` ← r45X4PYH-fg: play 3–4 notes once into a stereo delay at 99% feedback (L about 1 s, R about 150 ms) to get an endless shimmer texture.
- `hidden-context-synth-strings-…-gated-glimpses-under-sidechain` ← _cVKvtFm8J0 (carry-over): two crossing arpeggiated saw plucks into a shared pitch-shift reverb. Level automation and sidechain let only glimpses through, so the layer reads as strings.

Checks: quality_check --strict 7/7 clean (library-wide: 205 checked, 0 failed, 28 warned, same as before and none new). novelty_check: 6 NOVEL (max 0.138), 1 REVIEW (0.183, kept with stated delta). For all 7: distilled/ copy = mcp-publish/, listed in index.json, LIBRARY.json, taxonomy, curriculum L3 and skills/*.md. The youtube-skills MCP search_skills returns the new skills.

## Rejected (9)
- EXx9At3iUOw (EDM loop → full song): already covered by today's gIVUpqVRf-w and xY7vRHiSJSM plus the existing arc skills. The one unique idea (an automated gain lane used as a reference energy map) is too thin for its own skill.
- VRgPQMSVCP0 (breakdowns & build-ups): mostly reference listening; breakdown-start types overlap the existing breakdown and build-up skills.
- QMueZaoCPMA (Zebra cinematic bass/drums): short preset walkthrough; the portable idea is covered by the 10-26 taiko-from-noise skill.
- 2GVSHTl2bY0 (punchy sounds from any source): locked to one Doppler plug-in, plus cheat-sheet promo.
- V43qcp4UFIA (isochronic track structure, Mind WorkStation): thin, a single parameter. Useful fact for the isochronic skills: at a 10 Hz pulse on a 180 Hz tone, depth 0 = solid tone, about 10 = barely audible, about 30 = clearly noticeable, 100 = fully chopped.
- route.py COVERED: nVpMD4IIH0A (airy pad), uI74d3nDC8I (Zebra ambient), FL-TBkqqfIU (cinematic risers), kSXHTJJ7D34 (house song strategy).
- No YouTube transcript (no ASR used): YguhHIt7DTA (generative ambient from a 6-bar loop).

## Pipeline notes
- Isochronic: one quick search only (exhausted per 10-26). The only how-to hit was the thin V43qcp4UFIA. Session-arc design still needs to be composed from existing skills, not hunted.
- The brightness search mostly returns vocal-mixing videos; "shimmer pad" phrasing worked better. The stereo-width search mostly returns master/mix tricks that are already covered.

## Carry-overs for the next hunt
- Unfetched hits: nRI9gJvZXXM / KrVtkC8usmI / fjO8HIZzhZs (generative ambient patches; loops), zJmszSX8LPY (ambient arrangement), 98XTwmm08K8 / yZjQ2e4IREI (wavetable matrix motion / wavetable pads), 9Ba2boGeznQ (bass, same series as H6i55lXAMh0, check for duplication), mnledZoD4QE (ambient pad), j4nHoXGXF8A / axLAIw6Iw7A (arrangement hacks), rqMI1w8i3OA (depth tricks).
- From 10/22: cwwOLuAuvbc, aDgy_IB9Ets, P68bG3JEskQ, Qj2bLCq1PA4, P7-mewTtDts, LP1rbAbojkc, sFckKx8rsCs, QjrINfUCzjQ still unfetched; MH7YiOWQIhI / kHWOIE4YTZ4 still queued for tlang upgrade.
- Gaps: brightness (still thin; try "exciter / harmonic enhancer on pads" phrasing); loops (generative-loop hits above); isochronic session arc (compose).
