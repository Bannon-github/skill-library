# Morning synth YouTube hunt — 2026-10-23 (PT) — finished after interruption

## Counts
- MCP count: 182 → 189 (index.json = 189 = files in mcp-publish/skills, no duplicate ids). LIBRARY entries 180 → 187. Taxonomy cinematic-hybrid-synth 146 → 153; curriculum level 3 115 → 122.
- New skills: 7 (1 published by the interrupted run, 6 added when the hunt was finished). Rejected: 3. Carry-overs: see below. Searches: 8 (all run by the interrupted run). Crypto pivot: no.

## Interruption — what was found
- The interrupted run completed 8 searches (09:14–09:26 PT; `batches/work-2026-10-23/search.log`), published 1 skill (C871ckX4GfQ, ~09:20–09:22 PT; lydian layering) and fetched 9 Show transcripts (10:00–10:02 PT). It never ran `route.py` or distilled any of those 9. No error is recorded in the logs; the likely cause is YouTube rate-limiting (yt-dlp metadata calls were returning HTTP 429 / "sign in to confirm you're not a bot" when retried later). nkNSlRVGb38 had `title: null` in its meta.json for this reason; title taken from the search record.
- Half-published skill check: `lydian-ambient-soundscape-layering-…-arrangement` was consistent — valid v1 JSON, identical in distilled/ and mcp-publish/, listed once in index.json, LIBRARY.json, taxonomy and curriculum. quality_check --strict clean; novelty NOVEL. No rollback needed. (Backup of the 4 state files taken before the continued run: `backups/2026-10-23-morning-hunt/`.)

## Published (7)
Song structure / arrangement (the standing top priority — first real song-structure skills in the library):
- `lydian-ambient-soundscape-layering-by-frequency-range-…-swell-arrangement` ← C871ckX4GfQ (published by the interrupted run; frequency-range layering + fade-in/filter-open/reverb-mix arrangement) — **partly song structure**
- `ambient-44-bar-arrangement-map-low-pad-percussion-high-pad-piano-staggered-entry-strip-to-shaker-return-with-new-chords-coda-ending` ← wirMkOC-hGQ — **song structure**: bar-level intro → rising → strip-back → return with new chords → coda
- `ambient-multi-section-arrangement-drama-opening-textures-then-grounding-bass-drop-cue-signalled-sections-per-section-tempo-key-change-final-push-taper` ← 0bB8rWEcScA — **song structure**: sections signalled by small cues, per-section tempo, final push and taper
- `eight-bar-build-up-seven-bars-risers-drums-then-one-bar-pre-drop-low-end-removal-kick-doubling-schedule-vocal-and-single-note-pad-transition` ← nkNSlRVGb38 — **build/transition** (EDM 4/4; adapt density for ambient)
- `breakdown-arrangement-4-bar-break-two-8-bar-breakdowns-8-bar-build-up-rhythm-stripped-drop-chords-melody-foreshadowed-via-lowpass-automation` ← ojDea0jCQ5o — **breakdown + build-up structure** (EDM-leaning)
- `ambient-chord-arrangement-one-chord-tone-per-instrument-root-sub-third-pad-fifth-choir-third-reinforcement-strings-parallel-motion-spread-voicing-55-bpm-breath-tempo` ← CfyOOGAxJEs — chord-tone-per-instrument voicing (arrangement of a progression, not sections)
- `emotional-cinematic-arrangement-arc-subtle-intro-gradual-additions-climax-first-melody-only-in-climax-fade-out-outro-chord-arpeggio-melody-method` ← gtg27jkzY1s — **song structure**: cinematic arc intro → build → climax (melody only here) → outro

Checks: quality_check --strict 7/7 clean (library-wide non-strict: 189 checked, 0 failed; 3 pre-existing goal-too-short fails under --strict, not touched). novelty_check: 6/6 new NOVEL (max overlap ≈0.11).

## Rejected
- 8sfw9SwXqhc (Beginner's guide to ambient, Ep 2 — songwriting interview): opinion/interview, no procedure ("don't plan, let sections flow"). Advice-only.
- v11TzDYmarQ (How to Ambient Music without BORING everyone): personal story + philosophy (limits, mono/band-passed layering mentioned in passing, ebook promo); no usable ordered steps.
- peChlwCphgM (Phaser Effect? When Should you Use it?): router COVERED; one synth's phaser panel + preset-pack promo. Only possible delta (phaser placed before the shaper, envelope → phaser dry/wet, stepper → feedback) is product-specific — not published; see carry-overs.

## Pipeline notes
- `route.py` was run on the 9 fetched videos: 8 COVERED, 1 CANDIDATES_READY. Its COVERED verdict is a false positive for arrangement content (the term lexicon is synth-parameter based; song-structure terms aren't in it), so I overrode it with a hand read of the transcripts + novelty_check against mcp-publish. Suggest adding an arrangement/structure lexicon to `pipeline/lexicons/` so the gap check sees these. 
- All 6 new skills grounded in fetched Show-transcript text (auto-generated, partly garbled; noted in `source.transcript_note` and constraints). Vendor/library names omitted; no presets copied.
- No further YouTube requests made after the 429s. Work files: `batches/work-2026-10-23/` (mk.py, publish.py, c1.py, c2.py, search.log).

## Carry-overs for the next hunt
- Priority queue not yet searched/fetched: brainwave/isochronic **production** (one search done: `isochronic-tones-track-structure-ramp-tutorial`, top hit QYO2yHqutv8 "Alpha/Theta isochronic tones with heavy rain" — not fetched, likely a track not a tutorial), loops, brightness, punchy bass, drums.
- Unfetched hits from today's song-structure searches worth reading: 55qkyBH9-6Y (Film Score in FL Studio, Göransson/Zimmer), U-Tn1o83yDk (Make any song cinematic), Wcxw3BPSt3A (Sound design a video; probably video-sound, low value), iiL3K3ewfuc ("This Arrangement Rule Will Change Your Music" — no transcript at search time).
- Phaser pads: peChlwCphgM delta above; more phrasing attempts remain thin (stereo phaser ambient pad search returned product demos). Treat as near-exhausted.
- From 2026-10-22 report, still unfetched: cwwOLuAuvbc, aDgy_IB9Ets, P68bG3JEskQ, Qj2bLCq1PA4, P7-mewTtDts, LP1rbAbojkc (machine-translated), sFckKx8rsCs, QjrINfUCzjQ; MH7YiOWQIhI / kHWOIE4YTZ4 still queued for tlang upgrade.
- Gap remaining: real song-structure coverage is still EDM/ambient-demo level; no skill on long-form drone/cinematic pacing, loop-based structure (A/B sections, 8-bar phrasing), or isochronic session-arc design.
