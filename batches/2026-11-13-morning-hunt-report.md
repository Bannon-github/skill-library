# Morning synth YouTube hunt: 2026-11-13

Mode: compact library (fold-in). No standalone skills were published. All 5 new skills passed `quality_check_skill.py` (clean) and `novelty_check_skill.py` (NOVEL, 0.91–0.93). I hand-checked each against the target cluster's variants and folded it in with `pipeline/compact/fold_in.py`. LIBRARY.json went 269 → 274 entries (merge_log batch `2026-11-13-morning-hunt`). `mcp-publish/index.json` was refreshed (33 skills) and the new ids resolve through `mcp-publish/aliases.json`. All transcripts are YouTube-provided captions (pipeline fetcher; Pf0at7zMSDw manual, the rest auto-generated). No Whisper/ASR was used.

Light rate limiting: the fetcher's internal retry recovered LANPsnGB_yY. Aqe3ISng8jA failed on the first pass (`rate_limited_or_ip_blocked`) and was fetched on a second pass about a minute later. `route.py` returned CANDIDATES_READY for all 10 routed ids, including clear rejects (the false-novel pattern continues), so every result was hand-checked.

## Folded in (5)
| video | skill id (alias) | cluster | one-line goal |
|---|---|---|---|
| dGGMbqe4QYQ | climax-break-structures-committed-turnaround-linear-rise-trilogy-fall-rise-hang-double-trilogy-insert-time-last | arrangement-loop-to-song-build-drop | Four named break/climax shapes for 8-bar phrased tracks (committed turnaround, linear rise, trilogy fall/rise/hang, double trilogy), each with an energy curve, built from filter/reverb/layer automation; hang time is inserted last. |
| Cx8mEhPdtB4 | envelope-matched-chord-spacing-6s-attack-filter-env-long-verb-tail-synth-note-gated-field-recording-fx-4bar-lfo-sub | arrangement-ambient-cinematic-score | Minimal Loscil-style bed: a ~6.5 s-attack saw pad whose chord spacing (8–9 bars) is set by envelope + ~29 s reverb tail; a field recording gated through a synth by a held MIDI note; a fixed sparse sine line; and a unison saw sub on LP24 with a 4-bar LFO. |
| LANPsnGB_yY | arp-smear-pad-grain-delay-resample-stretch-2x-high-wet-echo-spectral-freeze-retrigger-16th-eq-band-plus-feedback-bandpass-loop-motion | granular-and-spectral-texture-design | Arp-smear pad: a min9 arpeggio through grain delay is resampled, stretched 2× (pitch kept), smeared with a high-wet echo and a 1/16-retriggered spectral freeze, then band-limited. Also a feedback-band-pass (~3 kHz, 1-bar LFO on width) resampled loop layer. |
| Pf0at7zMSDw | punchy-808-2nd-3rd-harmonic-partials-subtle-unipolar-coarse-pitch-dive-convex-decay-fm-ratio-half-transient-two-stage-softclip-zero-cross-print | bass-design-sub-reese-808-and-layering | Punchy 808 from the source: character from the 2nd/3rd partials, a subtle unipolar coarse-tune dive that ends on the note, decay-curve shape (concave vs convex), an FM ratio-0.5 transient, two soft clippers + limiter, and a print trimmed to zero crossings. |
| Aqe3ISng8jA | noise-recording-tuned-to-key-stacked-max-q-eq-boosts-at-root-freeze-flatten-chromatic-sampler-pad-attack-verb-delay-sidechain-eq-automation | brightness-and-air-at-the-source | Key-tuned noise/air pad: 3–5 stacked max-Q, max-gain EQ boosts at the key root (e.g. 440 Hz) on blended recordings, then bounce, a chromatic sampler (root = that note), slow attack, verb/delay, light sidechain and arrangement EQ automation. |

Matt's preferences are written into each skill's constraints: steady pitch (dropped Cx8mEhPdtB4's random step patterns and random tuning LFO, LANPsnGB_yY's random MIDI generator, random velocity/pan and bass glide, Pf0at7zMSDw's pogo/long pitch bends, and Aqe3ISng8jA's 30 Hz loop-start scrubbing); no rapid clicking or rolls (rises use filter/reverb automation, not snare rolls; freeze retrigger and sampler loops must be crossfaded); drums early (~8 counts / ~12 s); Ableton/MIDI-friendly; and portable module mapping.

## Rejected (5)
- **6UYbsqHRrZ8**: crafting the outro. An EDM outro lesson (copy the intro, high-pass the kick, master fade). Thin and covered by arrangement-loop-to-song.
- **4fDLsJOP2MM**: texture clouds from field recordings. Built on random slice playback and LFO tape wobble (against steady pitch). The rest is covered by the granular and reverb clusters.
- **MlEt2outpJY**: "Mummy I F&%*ed the orchestra" quick tip. Bounce the orchestra and run an unpredictable formant/pitch plugin over it. No portable procedure, and the result is octave flicker.
- **wU6agSvjmgQ**: ambient pad from scratch. Beginner wavetable pad basics, covered by the wavetable and supersaw clusters. Its shimmer unison randomises pitch.
- **p0x7e9AKqFg**: Ableton Wavetable ambient pad walkthrough. Rambling and unplanned; covered by the wavetable counter-LFO and reverb/delay clusters.

Not fetched: none.

Seen but skipped (beginner, product, off-genre or duplicate titles): 2B6VnAY6QsI, C7sbXNSOyws, iKiJoupKGyk (trance structure), CbmWdKOmEBc / UxyrXqBQEpE (song-structure basics), FOaDweLRiKE (product), 2ONZ0NSK7I8 (Suno AI), kzkDoBupXKM (seen 11-11), _VB-CMv50So / FfTssBdaJEc (binaural app/product), PO8LnVrpHU4, dMJ3b5RHENI (M4L device manual), wf8tNNTG1Mw, Si5_mropWnA, g-bOLJTrldk / OtsAf7ptKVI (gate manuals), 0xdvueqPEm8, XfWHlZc-szA, YmFV7xS6-a0, vieGTqd3uhQ (beginner downtempo), gkql3wpySeU (Vital kick generator manual), vr0DHvuQX8E / UQpyAuq5vHk (seen), JhZU6JGvoHw (already in library), AMSLWvb2dGU, FlbAzM5w0bs (Diva house masterclass), 2ykDKH9jnQI (house atmosphere), WxK8rUl_qnU (seen), iynvuZf64Jo (deep-house strings preset), 2aVfWL1ybJs (Octatrack beginner), ruJmFNJ6VEA (SP-404), tzfzkTAQsnE (seen), vKKfxcMriCA (UI SFX), -gnAMoyi_AU, z9jq7YM-QXA / PEB5pkHjVeo / 7axJ6AK52KM (granular product demos), 96yrn_-KoYg (music piece), fX2AIWvsX3E (Harmor reso pads), cvu2YhN_QJk, BiZh0BrLDdQ / NQWiDznUlME / 9tG67QpFmCs (preset walkthroughs), dhgrrIrfViU / n0iWo5wZSsQ / vppdU0zIDFI (field-recording overviews, close to today's folds), zEkCere2A_Y / v97MvZ1XhXM / l1pxzjfwX1c (seen), -4ubGqqPHis, 9dJnmuFwFQY / VMbNomvpJk0 (wavetable ambient pad, covered), LlLCnbt61Hk (EDM layering), LuU3JgmAQvQ, 7rj31n2kC-o (seen), 6AbG3ODhhVQ / YJJ-MXZ5Ht0 (patch walkthroughs), Pc10zrXK4C8, uDXK1BEaB3s, yiF_cUEtMdY, XU7sWoTJEtE, eK5NGFH_Cg4, vqxibp_zN80 (stereo/mix basics; stereo cluster already deep).

## Searches (2026-11-13)
`search_youtube_topics.py --skip-known` (240–3600 s): ambient arrangement intro/build/climax/outro; cinematic ambient song structure sections; automating binaural beat frequency over time (Ableton); isochronic tone gate automation (Ableton); soft ambient kick synthesis; felt soft kick + sub ambient; noise on synth pad for air; orchestral sample mangling hybrid; resampling orchestral strings granular; phaser on pads; ambient loops from field recordings + synths; punchy bass synth; wavetable ambient pad from scratch; hybrid sample+synth pad layering; stereo width pads M/S. Logs are in `batches/work-2026-11-13/`.

## Gaps still open
- **Brainwave rate-ramp automation:** still open. Searches return Logic/static binaural, app demos or gate manuals. Write it in-house from the monaural/tremolo variants (automate tremolo Hz or the second sine's offset, e.g. 8 → 4 Hz).
- **Ambient/cinematic builds/breakdowns:** improved with the four climax/break shapes (adapted for ambient: no rolls, no pitch risers). An ambient-native, drumless walkthrough is still wanted.
- **Soft/felt ambient kick + sub:** still open. Hits were beginner/EDM kick tutorials and product manuals.
- **Noise/exciter air on pads:** improved with the key-tuned noise pad. Synth-native exciter (harmonic enhancer on pads) is still thin.
- **Orchestral-sample manipulation hybrid:** still open. Hits were quick tips and product demos.
- **Pure phaser pads:** still open (Harmor/preset walkthroughs only).
- **Punchy bass:** improved with the 808 partials/decay-curve recipe. **Loops:** improved with the arp-smear pad and feedback-loop layer.

## Carry-overs
- None. Aqe3ISng8jA was rate-limited once and fetched on retry.
