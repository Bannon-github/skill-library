# Phaser, flanger and comb movement on pads

Goal: Add sweeping notch movement to pads with phasers (all-pass notches), flangers/combs (harmonic notches) and chorus/ensemble, including the high-pass phaser chord pad and the dual slow stereo phaser dreamy pad.

**Theory:** A phaser sums the dry signal with an all-pass-shifted copy -> irregularly spaced notches; a flanger uses a 1-5 ms delay -> harmonically spaced comb notches. Slow LFOs (bars-long cycles) read as 'dreamy'; fast ones read as effects.

**Hear it:** `sample-lab/theory/phaser_notch.py`

## Workflow
1. Start from a harmonically rich source (detuned saw/supersaw pad); notches need harmonics to cut.
2. Optional resonant high-pass (cutoff automated 200-800 Hz) to make the pad hollow/glassy before the phaser.
3. Insert phaser: 4-12 stages, rate synced to 1-2 bars (or 0.05-0.3 Hz free), feedback 30-60%, low resonance for smooth, higher for whistling.
4. For width, run two phasers on L and R at slightly different rates (e.g. 0.11 and 0.13 Hz).
5. Alternative: flanger/comb (1-5 ms delay, feedback) for metallic jet sweeps, or chorus/ensemble for gentle 80s width.
6. Follow with ping-pong quarter delay and large reverb; low-cut reverb at ~200 Hz.
7. Check mono: deep stereo phasing can cancel; reduce depth or mix if the pad disappears in mono.
8. Hear the theory: run `/home/box/audio-tools/bin/python sample-lab/theory/phaser_notch.py` from the repo root and compare the sections; reuse its functions as a starting point for renders.

## Source techniques (merged, numbers kept)

### Chorus-Ensemble modes: Classic, Ensemble, Vibrato
Source: [Learn Live: Chorus-Ensemble](https://www.youtube.com/watch?v=25Uiav5UA9c) · was `chorus-ensemble-classic-vibrato-pad-modes`
- Choose mode: Classic duplicates the input twice with short delay; LFO modulates those delay times (also slight pitch) so stacked copies thicken/widen. Ensemble adds a third evenly-split copy for a richer full-bodied chorus. Vibrato modulates pitch only (feedback and dry/wet disabled in that mode).
- In Classic/Ensemble: set rate and amount to a warm sweet spot; raise both together only when you want obvious oscillations. Use feedback to stack more copies—extreme feedback turns metallic; Invert Polarity makes feedback hollow.
- Enable high-pass on the processed path and raise cutoff so lows are cut—prevents mud/clipping when feedback/rate are high.
- Set width: 0% = mono chorus; up to extreme (~200% when available) spreads copies L/R. Blend with dry/wet so the pad stays present.
- Optional warmth/saturation at end of the device for subtle drive. In Vibrato: use small amount + faster rate to humanize leads/pads; Offset splits LFO L vs R (up to 180°) for spatial vibrato; Shape sine→triangle for sharper edges.

### Cinematic multi-osc pad with formant/comb and slow FX motion
Source: [HOW TO MAKE THE WEEKND CINEMATIC PAD | Serum 2 Sound Design Tutorial](https://www.youtube.com/watch?v=TmoP3i6-jl0) · was `cinematic-formant-comb-pad-phaser-fx`
- Osc A: analog basic shapes + unison/detune for width.
- Osc B: same family, −1 octave, higher unison (tutorial ~14) + detune.
- Osc C: light unison (~2) + detune; Filter1 formant-style on C only — set cutoff/resonance for vocal-like body.
- Filter2 comb-minus (or comb) on A+B+C; set cutoff, resonance, drive.
- Amp env: raise attack and release for pad.
- Free slow LFO1 → filter cutoff(s) for movement.
- FX: phaser (lower mix) → flanger (lower mix) → chorus (tweak delay/depth/mix down) → extra FX filter (low 24 dB) with very slow free LFO2 (e.g. 2 bars) unipolar to cutoff → delay → reverb; keep mixes moderate.

### Eerie, dreamy pad from a basic paraphonic supersaw patch plus outboard-style effects: cutoff key-tracked about 50%, long attack and release, two slow low-resonance phasers in stereo mode, about 0.5 s modulated delay, a second about 1.5 s ping-pong delay with a little more feedback and lower mix, a reverb with dwell at zero, then a looping (cyclic) envelope on cutoff whose rise/fall times an LFO slowly varies
Source: [Synth + Pedal Sound Design Tutorial - Arturia MicroFreak and Zoom MS-70CDR](https://www.youtube.com/watch?v=XRCwoFjZFMc) · was `eerie-dreamy-phaser-pad-supersaw-keytracked-cutoff-dual-slow-stereo-phasers-low-res-half-second-mod-delay-1-5s-pingpong-reverb-cyclic-env-cutoff-lfo-on-rise-fall`
- Start from an init patch, switch to paraphonic (up to 4 notes) and choose the supersaw oscillator at default settings.
- Set filter cutoff and resonance by ear, then key-track cutoff by about 50% so higher notes open the filter. Raise attack and release for a pad envelope (shorten them temporarily while designing effects).
- Add two phasers (dual phaser) for the whoosh. Reduce the rates for slow movement, lower resonance so the effect is subtle, turn on stereo mode and reduce depth a little.
- Add a modulated delay at default (about half a second), then a second delay of about 1.5 s with slightly more feedback, lower mix, in ping-pong mode.
- Add a lush (particle-style) reverb with dwell set to zero, other settings default.
- Automate cutoff with a cyclic (looping rise/fall) envelope, and change rise and fall times to set its rate.
- Route a slow LFO to the cyclic envelope's rise and fall times, and also directly to cutoff, so the breathing speed keeps changing.
- Play chords, adjusting resonance, cutoff and cyclic-envelope amount live.

### High-pass phaser chord pad: saw chords through a heavily resonant high-pass whose cutoff is automated, ping-pong 1/4 delay and a big reverb both low-cut at about 200 Hz, a phaser on a slow 2-bar cycle, a harmonizer shifted to the 3rd harmonic for a bell tone, unison and light compression
Source: [Sound Design Weekly 6: High Pass Phaser Chord / Pad](https://www.youtube.com/watch?v=cR23JfH_33U) · was `high-pass-phaser-chord-pad-saw-resonant-highpass-automated-pingpong-quarter-delay-and-big-reverb-lowcut-200hz-two-bar-phaser-cycle-harmonizer-third-harmonic-bell-unison-light-compression`
- Play low chords on a single saw oscillator.
- Insert a high-pass with resonance very high; automate its cutoff across the chords.
- Add a ping-pong 1/4-note delay with a ~200 Hz low cut and some extra stereo width.
- Add a big reverb: low cut ~200 Hz, size up, decay slightly up, damping up, wet up.
- Add a phaser synced to one full cycle per 2 bars; choose its sweep direction (up or down).
- Add harmonic stacking: harmonizer amount and width high, interval shifted from the octave to the 3rd harmonic.
- Add unison voices to taste, light compression, and pull the highs and some mids down slightly.

### Nested multi-notch phaser techniques for pads: grouped notches (groups × notches-per-group), pinch spacing, slow pinch 'breathing', stepped cutoff wah→flanger, scale-quantized random cutoff, slow triangle-swept full-depth bed
Source: [You’ve Never Heard a Phaser Sound Like This](https://www.youtube.com/watch?v=H8fsiSJzKTA) · was `nested-multi-notch-phaser-pad-shimmer-pinch-breath-scale-random`
- Map the controls: groups ('nests'), notches per group ('peaks'), cutoff (moves all notches), resonance (notch width), depth (0 transparent → full phaser), pinch (squeeze/spread notches within each group).
- Shimmer layer on a pad: 4 groups, 9 notches, depth ~82; slowly raise pinch until a metallic bell-like shimmer appears without taking over.
- Tubular breathing: same density (4/9), depth ~63; modulate pinch with a slow LFO synced to ~1/4 note. Compare 4 groups vs 2 groups — same motion, different character.
- Static sculpt: 1 group, 1 notch, depth ~72 for a radio/telephone colour; move the notch up for 'pickup switch' tones; add groups to smooth it.
- Stepped wah→flanger: 1/16-synced sequencer on cutoff at ~40–50% amount, 1 notch (wah); raise to 7–9 notches for a flanger-like texture; add glide so steps don't snap.
- Vowel push on vocal-like material: 4 groups, 7 notches, depth 65, resonance low (~4), slowly lower cutoff.
- Tuned random: random modulator on cutoff at ~1/16, quantized to a scale (e.g. minor pentatonic), range ~7.2 octaves. Change the scale to change the mood.
- Breathing bed under a pad: 6 groups, 11 notches (maximum density), depth 100%, cutoff swept by a slow triangle sequence (rate ~2) with ~10% glide; then vary pattern, pinch and depth.

### Parallel FX network: same input to up to three effects, heavy drive alongside clean delay, phase-flip a loop to cancel its dry and keep only wet, per-loop EQ/levels, effects inside the delay loop
Source: [Pedals in Parallel - Discovering new ways to use effects you thought you knew](https://www.youtube.com/watch?v=t0X_HQ25jmg) · was `parallel-fx-network-phase-flip-dry-cancel-insert-loop`
- Baseline: compare serial distortion→echo with echo→distortion to hear order-dependence.
- Parallel: split the same dry input to drive and delay branches and sum. Keep drive high and sustaining in its branch while the delay branch handles clean repeats.
- Remove the dry from an effect that has no wet-only mode: flip the phase of that branch so its dry component cancels against the dry in the sum, leaving (mostly) the delay.
- Chorus = vibrato + dry: test phase flip on modulation effects; inverted dry won't fully 'unbake' into pure vibrato, and some pedals already invert phase, so pick the setting that sounds fuller.
- Balance each branch with its EQ, send and return levels and a master volume; take the dry out entirely when only effects are wanted.
- Insert loop: put another effect (e.g. modulation/space) inside the delay's insert/feedback path so delayed sound is processed again on each recirculation.
- Swap in different trios of effects (e.g. delay + modulation + tremolo, envelope-controlled tremolo) to discover combinations.
