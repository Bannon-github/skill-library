# Morning synth YouTube hunt — 2026-10-13 (PT)

## Counts
- MCP cinematic count before: 109 → after: 117 (mcp-publish files 111 → 119; LIBRARY entries 109 → 117)
- New skills: 8
- Rejected: 8
- Carryover (transcript saved, not distilled): 7
- Pivoted to crypto/side-hustle: no (synth returns not exhausted)

## New skill IDs
- `click-train-resonant-filter-feedback-delay-comb-texture` ← `acM4NM4lH0k` (Organic alien comb texture: sub-audio saw click train → high-resonance filter → very short, high-feedback delay played by hand)
- `harmonic-multiple-frequency-shift-layer-vocoder-clean` ← `54eGln75Y3Y` (Harmonic-locked frequency shifter layer (shift by multiples of f0) cleaned with EQ, micro-delay and a self-vocoder)
- `karplus-strong-keytracked-delay-pluck-damping-comp` ← `8b5EX9HcPGk` (Karplus-Strong pluck: noise-burst exciter into a key-tracked feedback delay with decay/damping and register compensation)
- `morph-filter-lp-bp-hp-notch-lfo-cycle` ← `Z4mMGSg6ebY` (Morph filter: LFO-cycle one filter continuously through LP → BP → HP → notch → LP)
- `resonant-filter-sample-rate-reduction-talking-formant` ← `gzJEQiTC_SQ` (Talking/vocal formant voice from a resonant filter into sample-rate reduction (sweet-spot aliasing formants))
- `sample-hold-random-lfo-pitch-wave-filter-glide-textures` ← `IiWPL_v8Eqk` (Sample-and-hold / random-glide LFO textures: random steps on pitch, wave position and filter, random glide squelch, user-drawn step LFO)
- `synthesized-noise-impact-tail-lfo-shaped` ← `q-N55tqLUr4` (Synthesize a cinematic hit tail from white noise (LFO-shaped level, low boost, shared-LFO drive, Haas stereo, dark reverb))
- `triple-bandpass-bank-unsynced-lfo-pad` ← `L0IXE_whmso` (Three-band parallel bandpass filter-bank pad with offset, unsynced cutoff LFOs)

## Rejects
- `btlEZphP8Kw` Sample-and-hold basics (S&H samples an LFO at trigger rate; attenuate range). Concept folded into sample-hold-random-lfo-pitch-wave-filter-glide-textures; too thin alone.
- `kohxe8q614M` Sample-library boom + sidechain duck + reverb/bus; overlaps sidechain-compressor-duck-synth-pads and prior sample-layer reject (lLAj2rvBouI).
- `jUBV73xZVrQ` Sample transient chop + distortion + ~8 s reverb, band-layered booms; sample-layering workflow, low delta vs existing impact skills (synth part covered by new noise-tail skill).
- `cUeaNUTJU9o` Part 2 of sample-layered booms (EQ/distortion/ping-pong/group glue); sample layering, same rationale as jUBV73xZVrQ.
- `70Gvdl3uyWI` Kontakt instrument product promo (Pulsing Phaser Pad); no adjustable recipe.
- `EN_X_IdPaog` Sync lead + phaser→flange + chorus + EQ cleanup; hard-sync covered, phaser step thin, lead not a cinematic bed.
- `t3fD_6JEies` Ring-mod sum/difference theory + dry/wet blend; near-dup of ring-mod-envelope-bell-stab-pulse.
- `m7yYTAQDhI4` Sampler-specific sine tips (sample-start LFO fake PWM, bit reduction); not portable / covered elsewhere.

## Carryover for next hunt
- `SfqgigefIu0` Renegade KS / tuned multi-tap delay as resonator insert (±99 feedback polarity, filter type in loop, mute dry). Good delta; distill next hunt.
- `0n23itgG0LU` 80s PWM string pad (free-running seconds LFO on PW, slight osc2 detune, slow env). Candidate for PWM-pad gap.
- `NFWAC2kLqvo` Buchla 291-style 6-pole bandpass with stepped v/oct + bandwidth sequencer snapshots via dry/wet crossfader.
- `-oFbaWsScJw` Trance atmosphere with reverb freeze (OFF_LEXICON, unread).
- `X9nxUb1wRkg` Ambient pads from vocals (route COVERED, unread).
- `4fpZFYG83fw` Distorted delays (unread).
- `k9ZURoAww0k` Wavefolding LFOs VCV (379 words, unread).

## Pipeline notes
- 14 searches saved as pipeline/searches/2026-10-13-*.json (precheck + require-transcript + skip-known).
- route.py on 23 ids: all fetched YouTube-provided transcripts (no 429, no ASR). Outcomes: 5 CANDIDATES_READY, 17 COVERED, 1 OFF_LEXICON. COVERED again unreliable (morph filter, noise tail, comb click-train, S&H, bandpass bank were false COVERED); hand-checked vs mcp-publish.
- L0IXE_whmso transcript = YouTube English auto transcript of an AI-dub track (original es-US); labelled in source.transcript_note and constraints.
- Quality --strict: 8/8 clean. Novelty: 8 NOVEL (max local overlap 0.146 triple-bandpass vs parallel-filter-rhythmic-pad-chains).
- Full-catalog strict check: 3 pre-existing FAILs (lightroom-select-and-develop-photo, python-pathlib-basic-file-workflow, volyraph-browser-splat-pipeline) — not from this batch, untouched.
- Merged into LIBRARY.json (+8 → 117), mcp-publish/index.json (count 119), topics/taxonomy.json cinematic-hybrid-synth (75→83), curriculum level 3 (44→52), skills/<id>.md. Backups in backups/2026-10-13-morning-hunt/.
- Web Audio portability notes added where relevant (feedback DelayNode 128-sample minimum → AudioWorklet for KS/comb; Hilbert SSB for freq shifter) and explicitly marked as implementation notes, not transcript content.
- Deferred queue still empty; upgrade_to_tlang unchanged (MH7YiOWQIhI, kHWOIE4YTZ4, BqE9S27CZfY, beZpH9X850s).
- Git sync skipped: no credentials (no GH_TOKEN/GITHUB_TOKEN; gh not logged in).

## Still thin for later hunts
- Phase-distortion resonant-wave / wave-alternation standalone (not searched today; still thin)
- Dedicated phaser cinematic bed (phaser searches returned promo/lead only)
- Spectral (FFT) freeze pad distinct from granular/reverb freeze
- Wavefolder cinematic pad/bass (only psytrance/LFO-folding hits)
- Parallel distortion wet/dry cinematic stack (hits were drum/mix-oriented)
- Vocoder pad with external carrier (only self-vocoder clean-up covered today)
