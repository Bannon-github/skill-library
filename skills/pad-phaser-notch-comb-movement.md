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

### Flanger sequence pad: triangle plus a pulse one octave up whose level fades out and in once per bar, low-pass, a flanger with its own rate at zero whose delay time is stepped by a square/synced LFO for an arpeggio-like comb movement, then resample pitched down with rising delay/reverb mix for a transition
Source: [Tutorial #36 | Flanger Sequence Pads](https://www.youtube.com/watch?v=QdveXtMhAnk) · was `flanger-sequence-pad-tri-plus-pulse-octave-1-bar-fade-lfo-static-flanger-time-stepped-by-square-lfo-vocoder-formant-slow-env-resample-down-swelling-fx-transition`
- Osc A: triangle with about 3 unison voices and low detune (it plays all the time). Osc B: pulse/square one octave up, level at zero, slightly more voices/detune.
- Put an LFO on osc B's level at a rate of about one bar, retriggered, with a shape that fades out and back in (or drops fast and comes back up slowly).
- Low-pass the sound for a mellow tone, with key tracking; filter the harsher upper oscillator more if needed.
- Add a flanger at full mix (or high), set its own rate to zero, and modulate its delay time (depth/time) with a second LFO: a square wave as an on/off switch, or a tempo-synced 1/8 saw, unipolar, at a small amount. Find a sweet spot by ear, then adjust flanger feedback and phase.
- Optionally add a vocoder/formant effect and adjust bandwidth, formant and band count for color. Lengthen the amp attack and release to remove sharp clicks.
- Record the pad. For a transition, resample it pitched down (slower), place it before a section change, send it to delay and reverb, automate both FX mixes to rise as the sample plays, and fade the sample's level from 0 up to about half.

### Build a phaser from scratch: a chain of 1-7 all-pass biquads summed with the dry signal at half gain to make notches, Q 0.7071 for 'spread', a center frequency (50 Hz-18 kHz, start 500 Hz) swept exponentially by a 0.05-30 Hz sine/triangle LFO, a per-channel LFO phase offset up to 180 degrees and a dry/wet mix
Source: [How to build a basic Phaser Effect | Max for Live Tutorial](https://www.youtube.com/watch?v=1s_wcjB31iA) · was `build-stereo-phaser-from-allpass-chain-1-7-stages-dry-plus-wet-half-gain-q-0-7071-center-500hz-exponential-lfo-16x-depth-right-channel-phase-offset-180`
- Chain up to seven all-pass biquad filters (two-pole all-pass coefficients) and use a selector so only the chosen number of stages (1-7, the 'order' or notch count) is in the path.
- Add the phase-shifted signal to the original and multiply the sum by 0.5 for gain matching.
- Controls for the filters: 'spread' = Q (range up to about 16, start at 0.7071 = square root of 0.5; higher means narrower notches) and 'center' frequency (50 Hz to about 18 kHz, start 500 Hz).
- Duplicate the whole chain for the right channel so left and right are processed separately.
- Build the LFO from a 0-1 ramp (phasor) at 0.05-30 Hz, starting at 1 Hz: map it to a triangle with a centered peak or to a sine, selectable.
- Sweep exponentially: center × 16^(LFO × depth), so at the LFO maximum the center is multiplied by a factor and at the minimum divided by the same factor. Scale with a depth control.
- For stereo, add an offset to the right channel's ramp before the wave shaper and wrap it with modulo 1. Scale the offset control by 0.5 so 100% equals 180 degrees.
- Add dry/wet: multiply the processed path by wet and the dry path by (1 - wet) per channel, then sum.

### Phaser + chorus pad from pure waves: triangle and sine unison stacks on one note in three octaves, slow filter-envelope opening, triplet-synced phaser, deep feedback chorus, notch the phaser whistle, dark church-style reverb
Source: [Sylenth 1 Tutorial "Phasing" Pad](https://www.youtube.com/watch?v=ZsbcQZtklGI) · was `phaser-chorus-pure-wave-octave-pad`
- Write the clip as the same note in three octaves (e.g. B0, B1, B2) following the progression of the bass.
- Osc 1: triangle, 6 unison voices, small static detune, wide stereo, centre pan, retrigger on. Osc 2: sine, 8 unison voices, slightly more detune, phase offset (~85 degrees), retrigger on. Raise polyphony since several notes play.
- Amp envelope: back the attack off so each note fades in slowly; keep sustain high.
- 24 dB/oct low-pass with a mod envelope on cutoff: cutoff a little below full (about 70% of range), slow envelope attack (about 65% of its range) and medium sustain (about 50%), so the filter opens gradually while notes hold.
- Phaser: spread at maximum, left/right offset centred, width about half, default feedback, dry/wet about 38-40%, LFO rate tempo-synced slightly slower than 1/8 (the source uses a 4/1-triplet style setting).
- Chorus after the phaser: delay about 4 ms, rate about 0.25 Hz, depth about 60%, feedback on (chorus feeds back into itself), width maximum, dry/wet about 40%.
- Solo the pad and listen for a resonant whistle the phaser creates; cut that band with a narrow, deep EQ notch.
- Reverb as an insert or send at about 35% wet: slow, large hall/church-type space, pre-delay about 10 ms, size and decay at maximum; on the reverb's EQ cut everything below 150 Hz and roll the highs off around 4.5 kHz. Add a light compressor after it (shorter release) to bring the reverb up.
- Sidechain-compress the pad to the kick for gentle pump and automate the pad filter so it comes in and out across sections.

### Phaser pad depth chain: 12-stage phaser on a slow 4-bar ramp modulator with high resonance, then a delay used as two narrow HP/LP filter peaks moving inversely, then a narrow-band 100%-wet reverb whose mix is automated opposite to the filter peaks
Source: [Using Phaser Effects](https://www.youtube.com/watch?v=nIGiY1jYgWM) · was `phaser-pad-four-bar-ramp-inverse-filter-peaks-reverb-mix-counter-automation`
- Test the phaser basics on the pad: compare 2 stages with 18 (more stages = stronger phasing; notches = stages/2), and spread 0 (mono/centred) with 100 (wide, needs a stereo source). Use a slow rate.
- Set the pad phaser to 12 stages with resonance pushed high. Use a ramp-up (rising) modulator shape instead of sine/triangle, looped once every 4 bars, for a gentle sweeping swell.
- After the phaser, insert a delay used mainly as a filter. Enable two narrow-bandwidth filters, one high-pass and one low-pass, and modulate their cutoffs with sine LFOs of different rates and glide, set in opposite directions (one rising while the other falls). Optionally delay the LFO onset with an envelope so the peaks drift slightly.
- Keep stereo/time modulation in only one of phaser or delay. If the phaser already spreads the sound, don't also widen in the delay.
- Add a reverb as the last insert, 100% wet, band-filtered to a small frequency range that highlights the moving peaks, feedback/regeneration at 0. Expect it to sound too wet at first.
- Automate: increase the delay's filter-peak amounts during the sweep, and automate the reverb mix in the opposite direction. Fully dry when the filter peaks are strongest, jumping to 100% wet as the peaks move away and fade.
- Check over 16 bars with a simple drum beat and compare with the dry pad.

### Phaser drums: ping a phaser's all-pass filter bank with a very short impulse (a gate/trigger or just the attack of a sample), raise feedback/resonance until the bank rings like a tom, use more poles for complex liquid timbres, and sequence the sweep (centre frequency) and resonance per step to get tuned, accented percussion
Source: [Phaser Drums - How to turn a Phaser into a Drum Synthesizer](https://www.youtube.com/watch?v=TSiH9MUh4Ec) · was `phaser-drums-ping-allpass-bank-short-impulse-feedback-ring-poles-sequenced-sweep-and-resonance`
- Set the phaser's LFO depth/rate to minimum so it doesn't sweep on its own; keep only the output up.
- Feed a very short impulse into the phaser: a gate/trigger pulse, or a sampler playing only the attack portion of any sample.
- Raise feedback/resonance until the click rings with body.
- Increase the pole/stage count (e.g. 4 to 8 to 12) for more complex, liquid timbres; try the phaser's alternative mode if it has one for a drummier tone.
- Turn the sweep/centre frequency by hand to find the tuning range, then sequence it per step (automation or CV/mod lane) to play a melodic percussion line in key.
- Sequence feedback/resonance per step too, so some hits ring longer as accents.
- Optionally modulate the phaser's internal LFO rate/amount slowly for evolving timbre, then add reverb.
