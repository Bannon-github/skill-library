# Sample Lab findings (rounds 0–12, target v1.3)

Full per-skill stats: `runs/skill_stats.md`. Winners: `leaderboard.md`.

## Skills that did the most work
- **traveler-walkthrough-stereo-ladder-lf-width**: in all 6 winning systems. Its stereo ladder plus "keep the lows mono" step fixed both M5 (LF side energy) and mono-fold loss. Adding it by mutation gave +3.5 robust on average.
- **unison-odd-even-detune-width-clean-supersaw**: in 4/6 winners, 76% of chains containing it were reliable, and it added +3.9 when added. Using it as a bright layer fixed the most common failure, a spectrum that came out too dark (M6/M7 tilt).
- **keysol-venus-high-wt-artifact-pulse-layer** and **traveler-walkthrough-super-unison-wide-lead**: the other bright "air" layers. These are what got the swell and pluck systems over the bar.
- **warm-heavenly-supersaw-pad-keytrack-fx**: passed 6/6 straight from the seed chain in round 0 (89% of its variants reliable). It's the best-specified recipe in the library.
- **evolving-pad-unison-filter-swell-fifth + trance-gate-sidechain-chop-texture**: worked well together (about 70% reliable). The gate only works when the loop starts on a downbeat.
- **midside-eq-bass-focus-width-depth** and **traveler-walkthrough-control-track-filter-wt-animation**: high reliability (70% / 53%) and big gains when added (+4.8 / +7.5), but neither ended up in a winning system.

## Skills that didn't help, under this target
- `velocity-filter-cutoff-envelope-amount`: 92 chains, 0% reliable. Its grounded cutoff and envelope ranges always came out too dark for M6/M7.
- `modulation-lfo-envelope-mod-matrix-routing`, `fm-carrier-modulator-ratio-basics`, `lush-stereo-saw-pad-random-pitch-texture`, `digital-wt-morph-bandpass-chorus-echo-space`, `audio-rate-am-wave-shape-texture`, `parallel-filter-rhythmic-pad-chains`: 0–9% reliable. They tend to fail on harshness, tilt or width, or else they only describe routing and give no actual sound.
- These were never exercised at all (0 evaluations; the search never added them): `granular-dual-saw-ambient-epic-pad`, `traveler-walkthrough-wavetable-morph-filter-motion`, `keysol-helpling-keytrack-bass-split-delay`.

## Gaps in the skills
- **Not implementable as written**: spectral-warp (needs a per-harmonic spectral oscillator), organic-looped-sample pad (needs original recorded samples), keysol fm-chase sequence (a performance/arp skill), and keysol noise audio-rate filter (aftertouch performance, unstable on purpose).
- **No skill covers overall spectral balance or brightness targets.** Most filter skills say "close the filter for warmth" without giving a cutoff in Hz, so they land dark. A skill like "pad brightness/tilt check: keep about −3 to −5 dB/oct" is missing.
- **Ambiguous units**: vendor detune "%" (mapped 1:1 to ±50 cents), reverb sizes of 10–11 s (capped at 8 s), cutoff given as "12 o'clock".
- **No loop-making skill** (downbeat start, tail-wrap). Loop seams were the main gated/drone failure until the engine handled this.
- **No subsonic guard**: bass "deep" mode puts a sine an octave under E1 (about 20 Hz). The target doesn't score this, so it's reported as an advisory only.

## Corrections to the target's metric definitions (no thresholds, weights or pass bar changed)
- v1.1: M8 harshness became 1/3-octave band prominence; M7 starts at 125 Hz.
- v1.2: definition of the onset-click gate; M7 starts at the lowest fundamental's octave; loop seam measured as a relative step one bar apart; loops downbeat-aligned. Round 0 was re-run.
- v1.3: M6 tilt fit uses the same band range as M7.
