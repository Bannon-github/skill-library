# Generative ambient: drones, wind, sparkle layers and self-playing soundscapes

Goal: Build self-playing ambient pieces: noise beds and generative wind, tonic drones and PW drones, Eno-style sine pads, probability-gated seeded loops, follow-action clip pools, random-modulated loop voices, high-end sparkle layers and three-layer starters.

**Theory:** Generative music = rules + controlled randomness. Loops of different lengths and probabilities rarely line up, so the piece evolves; a tonic drone keeps everything in key.

**Hear it:** `sample-lab/theory/granular_cloud.py`

## Workflow
1. Foundation: reverbed noise bed or generative wind (3 filtered noises with slow LFOs) plus a tonic drone.
2. Pad: Eno-style sines (0/12/19 st) with slow cross-modulation, steady pitch.
3. Loops: several scale-locked note loops with different lengths and per-note probability; fixed seed.
4. Clip pools/follow actions: weighted random choice of next clip including silence clips.
5. Sparkle: random high scale notes + air noise, low level.
6. Mix: each layer its own range; long reverb; slow autopan.
7. Hear the theory: run `/home/box/audio-tools/bin/python sample-lab/theory/granular_cloud.py` from the repo root and compare the sections; reuse its functions as a starting point for renders.

## Source techniques (merged, numbers kept)

### Three-layer ambient starter in about 30 minutes: a slow-envelope wavetable pad with a 4-bar bipolar position LFO and random cutoff drift, a saw-plus-sine bass pad through a 24 dB low-pass, and a sustain-less detail voice whose filter is stepped by a sample-and-hold style modulator into heavy delay and reverb, all composed by frequency region
Source: [30 min Ambient Track for Beginners - Get Inspired & Find Your Sound](https://www.youtube.com/watch?v=CRWBHFIikqc) · was `ambient-three-layer-starter-slow-env-wt-pad-bipolar-4-bar-wt-lfo-random-cutoff-unfiltered-panned-osc-b-sub-saw-sine-bass-pad-24db-sustainless-stepped-filter-detail-voice`
- Set tempo to about 75 BPM and pick one minor key; set a 32-bar loop.
- Pad amp envelope: attack about 4 s (3-5 s range), decay about 4 s, sustain a couple of dB down, long release. Gain-stage the synth output down.
- Load a soft wavetable in osc A, set 5 unison voices and adjust detune between wild (wide) and tight. Modulate wavetable position with an LFO synced to 4 bars in bipolar mode.
- Turn on a low-pass filter and find the sweet spot where partials just peek out; put a random/chaos modulator on cutoff and lower its depth in the mod matrix.
- Send the pad to a dotted-eighth dual delay and a very long reverb (about 55 s decay, 100% wet on its return track).
- Add a sub osc one octave down at low level. Add osc B with a second wavetable bypassing the filter at low level, and auto-pan it with a 2-bar LFO (optionally its own bipolar WT-position LFO).
- In a 32-bar MIDI clip, place a minimal chord shape and only a few slow sustained notes; then lower the pad cutoff slightly and let the reverb open it.
- Bass pad: new instance, saw through a 24 dB/oct low-pass, faster envelope with some decay, add a sine (or sine sub) layer and a touch of reverb; write one long root note.
- Detail voice: attack-decay envelope with sustain at zero, 24 dB low-pass with cutoff stepped by a slow sample-and-hold/step modulator; send heavily to delay and reverb; write a few sparse notes.
- Check the master spectrum: confirm pad, bass pad and detail voice occupy different frequency regions; adjust levels or filters where they collide.

### Planetarium / Eno-style ambient space pad on any synth: sines at 0, +12 and +19 semitones, a triangle sub, two slow free-running smooth-random LFOs that modulate each other's rate and are mixed on every target, low-sustain amp envelope, gentle filter, and LFO-moved reverb/delay mix
Source: [How to make an ambient space pad in any synth.  Sound Design Tutorial 1](https://www.youtube.com/watch?v=Oq5TCAKw64Y) · was `eno-space-pad-sines-0-12-19-st-triangle-sub-cross-modulated-smooth-random-free-lfos-mixed-per-target-modulated-fx-mix`
- Init the patch and set the oscillators to sine waves: osc 1 at 0 st, osc 2 at +12 st (one octave), osc 3 at +19 st (an octave and a fifth).
- Set up two LFOs: rate in Hz (not tempo-synced) and very slow, smooth-random shape (random but gliding, not stepped), free-running so they do not restart on each key, bipolar.
- Cross-modulate the LFOs: send a small amount of LFO 3 to the rate of LFO 2, and of LFO 2 to the rate of LFO 3.
- Modulate the level of the +12 osc with LFO 3 and the +19 osc with LFO 2, plus a smaller amount on osc 1 (the root should move least). On every target, mix a bit of both LFOs, sometimes inverted.
- Add a sub oscillator one octave down using a triangle wave (square is too buzzy with sines). Add a trace of noise (pink, white or blue) for high-end character, barely audible.
- Amp envelope: long attack, long decay, sustain lowered (sloping down), long release.
- Low-pass filter for roundness with low resonance. Move cutoff only slightly with the LFOs.
- Effects: a big cathedral-type reverb and a delay. Put both LFOs, mixed, on reverb dry/wet, delay dry/wet and delay feedback, but not on delay time. Low-cut the effects returns to avoid mud.
- Turn on unison on the oscillators (several voices) with only slight LFO movement, then stop adding things. Save the patch, take a 5-15 minute break and come back for small balance tweaks.
- Optional: add shimmer reverb tuned to +7 st (a fifth) instead of the default octave, with its mix moved slowly in and out.
- Optional: add a low-level consistent noise bed (rain, metallic flow, forest) through a slow, subtle band-pass in parallel with the main filter. Add slow LFO on overall volume and pan, plus small EQ dips on any resonant buildup (not many narrow cuts, which cause a comb-filter effect).

### Self-running generative ambient soundscape built from per-layer clip pools that pick their next clip by weighted chance (about 50/50 repeat vs jump, with silent and sparse clips to weight density), over a reverbed noise/field-recording foundation, a tonic drone and a root bass note at random intervals, with sample-and-hold auto-pan on random one-shot FX and weighted-probability quantized note sequences
Source: [Creating Generative Ambient Soundscapes with Ableton Live & Pigments (Tutorial)](https://www.youtube.com/watch?v=fjO8HIZzhZs) · was `follow-action-clip-pool-generative-soundscape-reverbed-noise-foundation-tonic-drone-random-interval-root-bass-weighted-repeat-or-jump-silence-clips-sh-autopan-fx-weighted-note-probability-quantized-sequence`
- Create the foundation: a field-recording or noise track through a lot of reverb, plus a granular noise layer with its playheads/position modulated.
- Add a drone pad on the tonic chord and route several slow modulators (LFOs, random) to its macros.
- Add a simple FM bass with a little chorus that plays the root note at random intervals.
- For each track, build a pool of clips: varied patterns, sparser and busier ones, and at least one clip of pure silence.
- Turn on a follow action for every clip: after it finishes, repeat itself or jump to another clip in the pool; set the probability slider (about 50/50 to start) and weight it by clip content.
- Random one-shots: feed one MIDI note through a random-pitch MIDI effect into a drum rack/sampler holding your FX one-shots; on that FX track add an auto-pan whose LFO is sample-and-hold.
- In clips, set per-note chance (probability) and a velocity range; map velocity to a synth parameter so dynamics also change timbre.
- Inside the synth, run three independent sample-and-hold modulators on different parameters; for melodic voices use a repeating random (Turing-style) sequence on coarse pitch quantized to the minor scale, or a step sequencer with weighted note probabilities (root high, other notes medium/low).
- Let the set run for a while, record it, then cut out the passages you like for a later track or reuse the designed sounds.

### Generative 'noodle' wind with no MIDI: one noise source into three parallel filters (slow-swept LP, high resonant BP whistle, mid SVF BP), slightly different free-running sine LFOs with light LFO cross-mod, and an LFO-modulated three-VCA mixer
Source: [DevOcean Modular - Create A Wind Noodle Patch From Scratch #modularsynth  #sounddesign  #synthesiser](https://www.youtube.com/watch?v=_6mEzWHoxKo) · was `generative-wind-noise-three-filters-slow-lfos-lfo-modulated-vca-mix`
- Start a patch with output, a gain mixer and an EQ (disconnected). Add a white-noise oscillator at low volume, with a little extra gain on the noise module.
- Channel 1: noise → low-pass, fairly closed. Add a very slow free-running sine LFO (no MIDI, no retrigger) to its cutoff, slowed further if needed.
- Channel 2: same noise → band-pass (RBJ-type) set very high, resonance pulled way up but not to a tone, to make a resonating whistle. Add its own slow LFO.
- Channel 3: same noise → state-variable band-pass in the middle range, a mellower flavour, with its own slow LFO.
- Make all three LFO rates slightly different, still very slow, and let one LFO modulate another 'just a touch'.
- Mix the three channels in a 3-input mixer with per-channel modulation inputs (each channel = a VCA), in attenuation mode, bipolar depth set in the correct direction. Drive each modulation input with its own slow sine LFO at a different speed, positioned in the middle so channels go in and out but don't disappear.
- Add a bracket (low/high-cut) EQ to tame the bed, then a big wash reverb. Save it as a patch, then explore by changing LFO rates and shapes on both filters and mixers.

### Endless ambient texture from one looping MIDI clip: seeded random notes in a gap-free scale, per-note chance below 50%, randomised velocity/humanise, slow sine pad, scale-degree fifth chording and stereo/granular/reverb chain
Source: [The Secret to Endless Ambient Textures in Ableton Live](https://www.youtube.com/watch?v=U1t3ELd1LDI) · was `probability-gated-seeded-scale-loop-endless-ambient-sine-pad`
- Create a looping MIDI clip and set its scale (e.g. C minor, then switch to major pentatonic or Dorian; scales without half steps suit generative work). Use fit-to-scale after any scale change.
- Generate seeded random notes: set density, pitch register around 2–3 (mid range rather than 0–1), longer durations for smooth pad-like notes, and the number of voices.
- Randomise velocities and add deviation/humanise so timing and dynamics wiggle off the grid.
- Select all notes and set chance (play probability) to about 50%, then randomise it so some notes play ~90% and others ~15%. With many voices/density keep chance below 50% or even 30%. Re-apply after regenerating.
- Sound: simple sine pad (second oscillator off), attack just over 1 s, release ~6 s, extra voices for overlaps.
- Add a chord/interval effect before the synth in scale mode with a scale degree of 4 (perfect fifth), so every triggered note becomes a power-fifth.
- Effects: stereo doubler, parallel echo, a stereo pitch-loop/micro-delay for randomised stereo, granular delay (raise spray, lower frequency) for glitchy texture, then a long-decay reverb.

### Random-modulator soundscape loop: resampled-chord drone with one random modulator on each voice's start position and pan, randomly shortened arp-driven drums, a randomly retimed delay with a +12 st pitch shifter and stepped grain size in its feedback, and a step-scanned vocal sampler
Source: [Deconstructing a Textural Soundscape | Creative Sprint #5 Breakdown](https://www.youtube.com/watch?v=uEI2Ytxn7iI) · was `random-modulator-soundscape-loop-voice-playhead-pan-random-delay-octave-feedback`
- Resample a plucked chord into a sampler and set it up to sustain as a drone. Add one random modulator and map it to both sample playhead/start and pan.
- Process the drone through a standard delay in parallel with a convolution reverb.
- Drums at slow tempo: half-note hits from a drum machine with two samples (mallet, brush) driven by an arpeggiator. Add a random modulator that shortens the arp length by up to −12 steps (16 down to 4).
- Send drums to a delay: random modulator with smoothing on delay time in beats (about 1 to 8), a pitch shifter at +12 semitones inside the feedback loop, and a step modulator on the shifter's grain size.
- Add a background drone layer (e.g. a pad preset with longer envelope/filter and chorus) playing the same chords lower, plus an optional texture drone into a big reverb with modulated warp, kept low in the mix.
- Vocal layer: vocal loop in a sampler fed by an 8-step arp with transposition. Use a 16-step modulator to set a different playhead start per step, a slow LFO on a band-pass frequency, and a random modulator on pan.
- Vocal FX: distortion preset whose saturation macro is stepped through 16 values, then a delay with reverse blur.

### Scale-locked high-end atmosphere layer: sporadic random note 'sprays' (sine-like and brighter 'glass' voices) above ~3 kHz with a gravity/rate control, plus pitch-locked air and dust noise layers on random-drift LFO levels and a long reverb
Source: [Airglow Walkthrough: A High-End Atmosphere Instrument for Ambient Music](https://www.youtube.com/watch?v=LeChNmmtNsM) · was `scale-locked-high-end-sparkle-layer-random-notes-air-dust-noise`
- Analyse a reference ambient track's spectrum: note the active, sporadic, pitch-locked detail between ~3 kHz and 20 kHz.
- Set the key/scale lock to the track (e.g. B minor pentatonic) and trigger the generator; random notes from the scale are sprayed out.
- Slow it down with the gravity/rate control so notes arrive slowly; raise the reverb ('glow') amount for long trails. Alternatively switch to tempo sync and choose intervals from 1/16 up to 16 bars.
- Blend the two tonal voices: spray (standard sine-like tones) and glass (sharper, buzzier shine), each with a tone control and different patterns, so they don't fire together.
- Add the air layer (white noise that 'blows in the distance') and modulate its level with an LFO (e.g. smooth random drift) so it comes and goes. Add the dust layer (sand-scatter-like noise) the same way with the second LFO.
- Pitch-lock the noise layers: air follows spray's note pattern and dust follows glass, so the noise gains tonality in key.
- Shape the reverb (size, decay, tone, mix, pre-delay, diffusion, modulation/chorus), use the output limiter and +6 dB make-up if quiet. Optionally drive pitches from a glacially slow generative MIDI pattern. Then confirm on the full-mix spectrum that the high end is filled.
