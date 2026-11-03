# Stereo width: Haas, mid/side, detune, short-IR and mono-safe widening

Goal: Widen sounds without phase problems: asymmetric L/R processing, Haas delays with phase offsets, short-IR wideners, band-split widening (highs wide, lows mono), chord-split panning and stereo filter/ladder spread.

**Theory:** Width comes from L/R differences (time, pitch, filtering). Correlation near +1 = mono, 0 = wide, negative = cancellation risk. Haas delays (5-30 ms) widen but comb-filter in mono.

**Hear it:** `sample-lab/theory/stereo_width.py`

## Workflow
1. Keep below ~120-150 Hz mono.
2. Prefer decorrelation: slight detune, different LFO phases, different filter cutoffs or chord notes split L/R.
3. Haas: 5-20 ms on one side, automate amount; check mono sum.
4. Mid/side: widen only the high band; short-IR widener with width trim.
5. Measure correlation; back off if it goes negative.
6. Hear the theory: run `/home/box/audio-tools/bin/python sample-lab/theory/stereo_width.py` from the repo root and compare the sections; reuse its functions as a starting point for renders.

## Source techniques (merged, numbers kept)

### Width by processing left and right differently (L/R EQ, one-sided saturation, formant shift, slap times) with a mono-safe parallel blend
Source: [12 Ways To Widen Your Sounds Like A Pro](https://www.youtube.com/watch?v=Z2mgB3LYkgQ) · was `asymmetric-left-right-processing-width-mono-safe`
- Most organic: make L and R different sources - record an analog synth part twice, or use two different claps/variants - and hard-pan one left and one right.
- L/R EQ: EQ each side differently (e.g. brighter left; right with highs reduced and mids boosted).
- Mid/side EQ only helps if the sound already has side content (a single mono output has none): boost sides more than mid.
- Parallel width chain: keep a dry chain untouched and add a second chain with a Haas/width effect followed by distortion; mix the wet chain in slowly until width appears while mono compatibility stays good.
- Saturate only one side (pan the drive to the right, leaving the left clean).
- Chorus as the old-school widener for mono synths - note it can sterilise the tone.
- Haas via delay (widest but sacrifices phase integrity): one side ~1 ms, the other ~6-20 ms, low feedback, EQ the delay; reserve it for supplemental pads/layers and avoid stacking it on already-reverbed/delayed sounds.
- Formant-shift one duplicate and leave the other unshifted, panned apart.
- Slap delay return: about 50 ms on one side and 75 ms on the other (tape-style delay preferred), feedback to taste - cleaner and less unnatural than Haas.
- Synth-side: two otherwise identical saws with a different waveform variant on one, panned L/R with the random(-phase) control turned down; or unison with per-voice pan and fine detune; or pan different filters per side; reverb also adds width.
- Check the mono sum after each method and back off the risky ones first.

### Haas delay + per-channel phase offset width, automated, with mono check
Source: [Principles of Mixing 38 - Stereo Widening with Haas Effect and Phase](https://www.youtube.com/watch?v=msDDpbSvdPc) · was `haas-plus-phase-offset-width-automated`
- Start with the mono source through a stereo tool set to pass-through; confirm it is centered.
- Add a delay between left and right. Large offsets are heard as an echo; stay in Haas range (≤ ~20 ms, and for some sounds even 15 ms is noticeable) so it reads as width/position instead.
- Sum to mono: time offsets cause comb filtering (static phaser-like coloration). Reduce the delay or skip the effect if the mono sum sounds hollow or wrong.
- Add phase offset (filter-based phase shift) to one channel instead of, or with, the delay; it only moves some frequencies so it is more mono compatible.
- Combine a small phase shift with a small delay shift (try either direction) to place the sound wide and out of the way of centered kick/snare; as an alternative to panning it stays on both sides.
- Automate the widener: off for verses, on (or wider) when a drop hits, or sweep from wide to mono for contrast.
- Before rendering, do a final mono check of the full mix.

### Widen a pad without phase smear: high-band pan LFO or hard-panned chord split
Source: [Merged from 2 YouTube how-to transcripts](None) · was `pad-width-no-phase-smear-highband-pan-or-chord-split`
- Start from a good but narrow pad. Avoid broadband chorus/imager wideners (phasy/warbly, phase issues in lows/mids) and frequency stereo-spread (often not truly wide, can sound inside-out). Choose a method: A) high-band pan LFO on the same patch (steps 2–5), or B) interleaved chord split across two hard-panned layers (steps 6–9).
- Method A: Insert multiband pan / band-limited auto-pan. Solo or target the high band only so lows stay centered.
- Method A: Draw a sine (or subdued sine) pan path so highs slowly swirl L↔R. Try bar-length (4/4) for gentle immersion or 16th-note rate for more motion.
- Method A: If 16ths feel too pronounced: switch to a less extreme pan profile and/or lower overall mix/amount of the pan effect.
- Method A: A/B before/after in context: pad should envelop more without the washy phase of chorus/imager on full-band signal.
- Method B: Duplicate the synth instance with identical settings and copy the MIDI to both tracks.
- Method B: On track A piano roll, mute every other note top→bottom; on track B mute the complementary set bottom→top so together they reconstruct the full chords but separately play different notes.
- Method B: Hard-pan A fully left and B fully right; play together for maximum width.
- Method B: Check a correlation/phase meter: split technique should sit near ~0 (very wide) without deep negative swings; compare vs chorus (often flangy + negative correlation) and spreader (weaker width).

### Mono-safe width tricks: a 100%-wet short room IR as a stealth widener with width trim and gain make-up, a drawn and smoothed auto-pan rhythm, and Haas kept ≤15 ms split across bands tilted in opposite directions
Source: [3 Stereo Width Tricks (That Sound Great In Mono)](https://www.youtube.com/watch?v=Mm5eO24aAec) · was `short-ir-widener-width-trim-drawn-pan-multiband-opposite-haas`
- Insert convolution reverb on the chords at 100% wet with a short, thin room IR and decay reduced to ~20% so no tail is heard. Audition other short IRs for different timbres.
- Sum to mono: the widened chords drop in level. Instead of lowering the wet mix, follow with a width control at ~65% and raise gain ~6.5 dB to level-match.
- Rhythmic pan for arps/synths: auto-pan at ~50% amount, try LFO shapes, then draw a custom stepped pan curve and add smoothing to round its edges. Optionally switch rate to unsynced Hz and set by ear to fit the part.
- Add a touch of multiband treble-only reverb before the panner for air; adjust pan mix lower for just a flutter, or full for strong L/R jumps.
- Haas: duplicate L/R with a delay on one side. Keep it at ≤15 ms and tune it while listening in mono until acceptable.
- Fix the lopsided tilt: split into bands, tilt the mid band to the right and the treble band to the left, then reduce width and re-level.
- Apply these to one headline sound (incidental FX/ear candy for Haas) while keeping most of the mix centred.
