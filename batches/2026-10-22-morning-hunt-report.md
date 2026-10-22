# Morning synth YouTube hunt — 2026-10-22 (PT)

## Counts
- MCP count: 175 → 182. LIBRARY entries 173 → 180. Taxonomy cinematic-hybrid-synth 139 → 146; curriculum level 3 108 → 115.
- New skills: 7 (4 from 10-21 carryover, 3 from today's isochronic/binaural searches). Rejected: 4 on content. Rate-limited (not fetched): 6. Searches: 3 run. Crypto pivot: no.

## New skill IDs
- `four-source-morph-xy-crossfade-vs-true-parameter-morph-analysed-sources-per-element-additive-spectral-pitch-formant-envelope-lanes-separate-lfos` ← HXKz89TIlJI (carryover)
- `random-gate-generators-from-noise-sample-and-hold-window-comparator-and-logic-probability-skipper-free-random-burst-clock-feedback-bernoulli-two-voice` ← uorRN6iH87U (carryover)
- `sample-and-hold-as-processor-on-lfo-or-step-input-automate-lfo-rate-up-and-s-h-rate-for-noise-filter-riser-aliasing-slowdown-random-hat-volume-inverse-fx-mix-layer` ← SZKIODnJuwU (carryover; delta vs existing sample-hold-random-lfo skill: S&H as processor on another modulator)
- `per-voice-per-parameter-note-on-random-values-bipolar-offset-compensation-unison-chord-variation-envelope-times-morph-two-cloned-parts-per-voice-lfo-rate-aftertouch-depth` ← X_zozWSx-RU (carryover)
- `isochronic-tone-layer-under-music-sine-carrier-midi-note-amp-pulse-blend-smooth-step-shape-fade-in-out-automate-pulse-rate-15-to-4-hz-and-back-10ms-smoothing-carrier-tuning-432-or-custom-map` ← WNewLv-kI2I (new: isochronic; first isochronic skill)
- `binaural-beat-meditation-track-pad-foundation-long-reverb-glide-overlap-pingpong-echo-two-sines-440-432-panned-lr-8hz-narrow-notch-carrier-in-music-bus-fades-gentle-limiter-export` ← GndBM5EifHA (new: binaural)
- `layered-binaural-plus-isochronic-architecture-carrier-left-carrier-plus-beat-right-octave-layers-pulse-ratio-locked-to-beat-sine-pulse-pingpong-pulse-harmonic-layers-lowpass-sweep-noise-drift-drone-fifth-journey-ramps` ← bFaYEPLlIxQ (new: binaural+isochronic layering, journey ramps)

## Rejects (REJECTED.md written)
- jfwv0Gasf6Q: product feature tour, thin.
- L1Vy2ZmHQ3Y: hardware sequencer manual walkthrough; generic LFO params.
- ypYhfCt874s: generic LFO basics for one app; near-dup of modulation routing skill.
- gd0f-sFwD6A: plugin + chord-pack promo; generic layer list.

## Pipeline notes
- All 7 grounded in fetched YouTube transcripts (raw/<id>/transcript.txt + raw.txt). Quality --strict: 7/7 clean. Novelty: 7/7 NOVEL (max overlap ≈0.12).
- route.py was not run (its COVERED verdicts have been unreliable); coverage hand-checked against mcp-publish listing + novelty_check instead.
- The pipeline venv (.venv) was missing at start; rebuilt with scripts/ensure_env.sh (also rebuilt mcp-server/.venv and sample-lab/.venv; /tmp/ytvenv relinked).
- Rate limit: the 3 rate-limited carryover videos fetched fine at 09:20 PT; after 7 transcript fetches, `rate_limited_or_ip_blocked` came back for 6 more. Searches with precheck ran fine ~40 min later and 5 more fetches went through.
- Isochronic/binaural skills carry a no-health-claims constraint; solfeggio frequencies flagged as having no scientific backing (the source says so too).
- Work dir: batches/work-2026-10-22 (mk.py, c1.py, c2.py, publish.py BATCH 2026-10-22-morning-hunt, search.log). Backups: backups/2026-10-22-morning-hunt/.

## Carryover for next hunt
- Rate-limited (not fetched): cwwOLuAuvbc (spectral analysis), aDgy_IB9Ets, P68bG3JEskQ (phaser query), Qj2bLCq1PA4, P7-mewTtDts (shepard query; likely product demos), LP1rbAbojkc (machine-translated).
- Fetched but not distilled: C871ckX4GfQ (Lydian ambient soundscape layering by frequency range; read first third — maybe a pad-layering skill).
- Unread search hits: sFckKx8rsCs (Bitwig stock ambient loop, yt-translated), QjrINfUCzjQ (generative ambient botanica, Ableton), 1zRXcLV7e_g (solfeggio meditation in 5 min; likely thin), 5XcwTO7Z_L0 (stack app promo; likely reject).
- Phaser pad: still thin. "phaser pad synth tutorial" returned only product overviews again (4th day running) — try a different phrasing (e.g. "phaser on pads mixing", "stereo phaser ambient") or treat as exhausted.
- MH7YiOWQIhI / kHWOIE4YTZ4 still queued for tlang upgrade.
