# Morning synth YouTube hunt — 2026-10-26 (PT)

## Counts
- MCP count: 191 → 198 (index.json = 198 = files in mcp-publish/skills, no duplicate ids). LIBRARY entries 189 → 196. Taxonomy cinematic-hybrid-synth 153 → 160; curriculum level 3 122 → 129. (Start count was 191, not 189: two mixing skills were added between runs.)
- New skills: 7. Rejected: 5 (+4 with no transcript available). Searches: 8. Transcripts fetched: 12 of 16 tried (no 429s this run; 12 s spacing between fetches, 20 s between searches). Crypto pivot: no.
- State backup taken first: `backups/2026-10-26-morning-hunt/` (LIBRARY.json, index.json, taxonomy.json, curriculum). Work files: `batches/work-2026-10-26/` (mk.py, c1.py, c2.py, publish.py, search.log, fetch.log, new.txt).

## Published (7)
Song structure / arrangement (priority 1):
- `eight-bar-phrase-repetition-variation-a-b-a-c-bars-d-bar-fill-or-empty-…-polymeter-shifting-loops` ← JE3QM_9sljI — **loop-based 8-bar phrasing**: A/B/A/C bars, then bar 8 is a fill or an "empty" to set up the next section
- `rule-of-three-phrase-repetition-play-idea-twice-then-third-pass-goes-somewhere-new-or-starts-same-and-diverges-halfway` ← iiL3K3ewfuc (10/23 carry-over) — **loop/A-B repetition rule**
- `section-transition-toolkit-layered-risers-downlifters-impacts-throw-to-delay-early-pickup-stacked-exponential-automation-…-hangover` ← lnJA5rOrp-M — **transitions** (ambient note: favour removal, reverse reverb and delay throws)
- `ambient-slow-harmony-motion-one-key-sus2-sus4-7sus4-chords-pedal-root-moving-top-static-chord-moving-bass-inversions-band-limited-1-2-3-cluster` ← tfJocFdYxsg — **long-form ambient/drone pacing** through harmony (one key, slow changes)
Drums / punch (priority 3):
- `cinematic-taiko-ensemble-drums-from-white-noise-velocity-to-amp-decay-and-filter-env-…-random-sample-layers` ← 6CWmImkHDgs — big cinematic drums from noise
- `drum-cut-through-band-passed-overdrive-…-dry-wet-parallel-level-matched` ← oc5YQf_Xy14 — punchy drums that cut through
Phaser (single allowed try):
- `high-pass-phaser-chord-pad-saw-resonant-highpass-automated-…-harmonizer-third-harmonic-bell-unison-light-compression` ← cR23JfH_33U

Checks: quality_check --strict 7/7 clean (library-wide non-strict: 198 checked, 0 failed, 28 warned, none of them new). novelty_check: 7/7 NOVEL (max overlap 0.154). distilled/ = mcp-publish/ for all 7; each is listed in index.json, LIBRARY.json, taxonomy, curriculum L3 and skills/*.md.

## Rejected
- 8GYXSO6zwxk (binaural beats in Ableton): near-duplicate of the existing binaural-beat meditation track skill.
- wHUn90VuwpM (binaural beat in Reason, 528 Hz / Schumann): duplicate two-sine recipe plus product-specific choices.
- EHJx3uVtHdc (risers/impacts/cymbals/drum rolls): thin, and fully covered by the lnJA5rOrp-M toolkit.
- sTc-ZN35_FU (sound-bath ambient techniques): a tour of specific add-on devices and preset packs; the portable parts are already covered.
- 55qkyBH9-6Y (film score, 10/23 carry-over): mostly preset browsing; what's left is already in the cinematic arrangement arc skill.
- No YouTube transcript (no ASR used): U-Tn1o83yDk (10/23 carry-over), FMIUZFElRB8, 8piC1ff9dA4 (isochronic+binaural how-to), PGSyt5zIDCE (cinematic impacts).

## Pipeline notes
- **New lexicon `pipeline/lexicons/arrangement.json`** (sections, phrases, repetition, fills/empties, transitions, pacing). Tested: JE3QM_9sljI now detects as domain `arrangement`; synth-heavy transcripts (lnJA5rOrp-M, 6CWmImkHDgs) still detect as `synth`, so existing routing is unchanged. route.py's COVERED false positives on arrangement content should drop. I didn't re-run route.py; transcripts were hand-read and checked with novelty_check.
- Isochronic/brainwave **production** searches (3 phrasings) return only basic binaural how-tos (already covered), finished tracks, or noise-removal videos. **Treat as exhausted on YouTube**; session-arc design remains a gap best filled by composing a skill from the existing isochronic/binaural skills plus the new long-form harmony and pacing skills (not a transcript distill).
- Auto-generated transcripts were partly garbled (e.g. JE3QM_9sljI bars 5–7 read "a a d"), noted in constraints. Vendor and preset names omitted.

## Carry-overs for the next hunt
- Unfetched hits worth a look: CRWBHFIikqc (30-min ambient track for beginners — long-form), gIVUpqVRf-w / EXx9At3iUOw (loop → full song structure), kSXHTJJ7D34, FL-TBkqqfIU (cinematic risers), nVpMD4IIH0A (airy pad), _cVKvtFm8J0 (synthetic orchestral strings), uI74d3nDC8I (ambient sound design), xlBInB7BOzE (drum sound design).
- From 10/22: cwwOLuAuvbc, aDgy_IB9Ets, P68bG3JEskQ, Qj2bLCq1PA4, P7-mewTtDts, LP1rbAbojkc, sFckKx8rsCs, QjrINfUCzjQ still unfetched; MH7YiOWQIhI / kHWOIE4YTZ4 still queued for tlang upgrade.
- Gaps: isochronic session-arc (compose, don't hunt); brightness and loops still thin; punchy bass is untouched this run.
