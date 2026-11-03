# Physical modelling: Karplus-Strong plucks, bowed/struck strings, modal and comb resonators

Goal: Synthesize plucked, bowed, struck and resonant instruments by exciting delay lines, comb filters and modal resonator banks with noise or clicks, controlling damping, brightness and body.

**Theory:** A delay line of length 1/f with a low-pass in its feedback loop is a string: high harmonics decay faster. Excitation brightness = pick hardness; loop gain = sustain. Modal banks of inharmonic partials model bars, bells and plates.

**Hear it:** `sample-lab/theory/karplus_strong.py`

## Workflow
1. Excite: short noise burst (pluck), continuous filtered noise (bow), click/mallet (strike).
2. Resonator: key-tracked delay/comb tuned to the note (Karplus-Strong), or modal bank with material-specific partial ratios.
3. Damping: low-pass in the loop and feedback 0.99-0.999 control decay; frequency-dependent decay for realism.
4. Brightness: pre-filter the excitation; velocity -> brightness and amplitude.
5. Body: add parallel combs/EQ for instrument body; MPE pressure -> bow noise level.
6. Scale-locked resonator banks or 12-voice strums for generative swarms; noise crackle into harmonic resonators for textures.
7. Hear the theory: run `/home/box/audio-tools/bin/python sample-lab/theory/karplus_strong.py` from the repo root and compare the sections; reuse its functions as a starting point for renders.

## Source techniques (merged, numbers kept)

### Physically modelled bowed string: key-tracked noise exciters into a 100%-wet key-tracked comb, MPE pressure on gain/resonance, MPE timbre fading in a 3rd-harmonic comb, and a three-comb instrument body that retunes cello to bass, viola or violin
Source: [Physically Modeled MPE Strings in Surge XT](https://www.youtube.com/watch?v=y9eDmBUC8ZU) · was `bowed-string-noise-exciter-keytracked-comb-mpe-pressure-timbre-body-combs`
- Initialise the patch. Route a basic noise oscillator into filter 1 set to comb positive with key tracking full, resonance maximum, 100% wet and cutoff C4. Keep the noise level low and set the overall gain very low before first playing.
- Add a concert-hall reverb, then set up an MSEG-style response curve driven by MPE pressure (loop off, rate disabled, phase ← pressure ~99%). Use it to raise exciter/output gain and to lift comb resonance from ~80 (unipolar) back toward full.
- Add filter 2 as a second key-tracked comb at G5 (third harmonic of C4), resonance ~40%, filter mode with two filters in series/blend (S2-type), filter balance fully toward filter 1. Make a second curve named 'timbre' driven by MPE Y (≈49% because it reads as bipolar, base 50%) and shape it so the balance only moves toward filter 2 at the top of the Y range; add pressure to its resonance.
- Add an instrument body with a three-comb FX block: pans 0, centre a little below 100 Hz (cello), offsets of almost an octave and closer to three octaves, feedback down to ~15%, tone low for a vintage recording sound or higher (or slightly less mix) for 'in the room'. Lower the mix of the upper combs so the centre resonates strongest.
- Resize the instrument: move the body centre to ~50 Hz and lower noise colour for double bass; raise centre, noise colour and tone by ear for viola and further for violin. Play in the instrument's own range.
- Tame noise: noise near the comb cutoff resonates nicely, noise far from it sounds like hiss. Key-track the noise colour upward. Better: mute the basic noise and use two S&H-noise oscillators (level ~−10, exciter gain ~−38 then ~−48), tune correlation/width by ear (width can give a formant-like bow character). Oscillator 1 handles high notes (low cut, key track +10) and oscillator 2 handles low notes (high cut, key track −10).
- Optionally stack a cello-body convolution IR after the combs (watch the low-end build-up and EQ it), then fine-tune levels.

### Karplus-Strong pluck: noise-burst exciter into a key-tracked feedback delay with decay/damping and register compensation
Source: [Karplus-Strong Synthesis in Bitwig Studio 3 - The Grid](https://www.youtube.com/watch?v=8b5EX9HcPGk) · was `karplus-strong-keytracked-delay-pluck-damping-comp`
- Build the exciter: pink noise (fuller than white) → bandpass SVF → a very short pluck envelope on level; add a velocity multiplier to scale excitation, and gain to keep long exciters in check.
- Feed the burst into a delay with built-in feedback and an in-loop low-pass. Set delay = one period of the target fundamental (7.64 ms ≈ C3) and feedback high so it keeps resonating.
- Key-track the delay: delay time must scale by 2^(−n/12) (n = semitones from the reference). Going up an octave halves delay; down an octave doubles it. Convert the note-pitch value to that factor (exp base 2, invert, offset so the reference note = no change) before feeding the delay-time modulation.
- Exciter variations: use the envelope itself as the exciter (attack time changes tone like pluck position); widen the noise stereo for a lush tone; long exciter envelopes give a reverb-like bloom.
- Map Decay → feedback (near unity = rings forever; low = unpitched thump) and Damping → loop low-pass (palm-mute-like). Optionally scale both by velocity (harder = longer ring/less damping); keep velocity amounts low—it is touchy.
- Compensate register: at equal feedback low notes ring longer than high notes, so key-track feedback up for high notes and adjust damping in the opposite direction so decay and brightness feel even across the scale.
- Experiment: feed other sounds as the exciter into the tuned delay for pitched resonant textures.

### Modal (partial-bank) physical-modelling voice: exciter into one or two resonators defined by a partial model, with material (decay vs frequency), tone (level tilt), hit (random partial emphasis), inharmonic stretch, parallel or series resonators, and velocity/random modulation for a playable mallet or string
Source: [reFX 𝑹𝒊𝒑𝒑𝒍𝒆𝒓 Walkthrough - New Physical Modeling Synth!](https://www.youtube.com/watch?v=Pd9AFeTcl2k) · was `modal-partial-resonator-exciter-material-tone-hit-inharmonic-series-parallel-velocity-random-hit`
- Mute the resonators and raise the exciter's direct output to audition exciters (impulse, long exciter, noise). Then turn the direct output back down and enable resonator 1.
- Pick a partial model and partial count for resonator 1 (start with the string model). Try beam, membrane, vibraphone and open tube to hear how partial patterns change the instrument.
- Shape the partials: decay/release for ring time; material down = high partials die faster (muted), up = the opposite; tone = cut highs or lows by level only; hit = random partial emphasis (pluck position); inharmonic multiplier up = stretched, metallic partials, down = compressed partials.
- Optional manual mode: edit partial positions and amplitudes (e.g. 4 partials), make two snapshots and use a ratio control to morph between them.
- Add resonator 2. Parallel: same exciter into both, set level and balance. Series: exciter → R1 → R2; use R1 with a very short decay (drum head) as an extended exciter for a tube in R2. Raise cross-feedback strength carefully.
- Optionally layer the two basic oscillators and route chosen sources through two filters (series or parallel), e.g. filter only the oscillators. Use the second layer for a second, different sound.
- Make it playable: velocity → resonator level, material (louder = more high partials) and exciter level; envelope 1 with a fast attack and low sustain/decay → level for a prominent attack over the tail; subtle random → tone; per-note random → hit; for a vibraphone, slow sine LFO → pitch at a very small depth.
- Finish: low-cut a resonator if it gets muddy, then stereo widener, compressor, chorus and reverb. If high notes are quieter, map key tracking → layer gain.

### Effects-only melodic instrument: crackle/noise source → smoothed-random filter → ping-pong feedback delay → spectral harmonic resonator (note, decay, harmonic count, pitch mod) → 'smudge' lo-fi/unison macro → reverb → limiter
Source: [Spectral Ambience: Turning Noise into Melodic Synths (Ableton Live 12)](https://www.youtube.com/watch?v=GoMfKhol88k) · was `noise-crackle-resonator-instrument-filtered-delayed-noise-into-harmonic-resonator`
- Create an effects rack (audio-effect track) with 16 macros. First device: crackle/noise generator; map only its density (crackle level) to a macro. Alternatively route external audio (e.g. bongo drums, vocals) into the rack.
- Add a filter in a resampling/character mode, LFO wave sample-and-hold with smoothing 100%, drive ~10%. Map cutoff, LFO amount and LFO rate to macros to sculpt which parts of the noise spectrum excite the resonator.
- Add a ping-pong delay at 100% wet. Map delay time (e.g. 6/16, 5/16, limited down to triplets for ambient use), a small L/R delay offset for stereo interest, and feedback (high).
- Add the spectral resonator: note mode, granular engine, quantise input on, unison 2, low damp fixed ~15% (cuts boomy lows). Map fundamental note, decay, number of harmonics (min 6) plus high damp on the same macro, pitch-mod amount (up to 1 st) and rate, and input level.
- Add a bit/sample-rate reducer after the resonator. Make one 'smudge' macro that raises the resonator's unison spread, lowers bit depth and lowers sample rate together (0 = 18 kHz/16-bit, i.e. off).
- Add reverb (size 100, diffusion-network filter on) and map decay time and dry/wet, then a final limiter to catch peaks.
- Play it: short decay for plucks and blips, long decay for pads. Save macro snapshots of good settings and randomise for new territory, with note, input level and reverb excluded from randomisation.

### Scale-locked resonator bank as an instrument: up to 12 tuned resonator voices on a root and scale (e.g. D minor 9, 6 voices, octave 3), excited by a stereo noise burst or drums, with motion modes (wave, strum, arpeggio, swarm), feedback/decay/damping/spread/diffusion and gated live-key voicing
Source: [Tessera by Audio Damage (Tuned Sequenced Resonator)](https://www.youtube.com/watch?v=aPsWzEfgEOo) · was `scale-locked-12-voice-sequenced-resonator-bank-wave-strum-arp-swarm-noise-exciter`
- Insert the resonator bank on a source. Set root (lockable) and scale, then the number of voices and octave (example D minor 9, 6 voices, octave 3).
- Choose a resonator model; test kick, snare and hats through it, trimming output when loud. On string models also set position and brightness.
- Build a noise exciter: an ADSR-gated stereo white-noise generator with no sustain, triggered on two steps of a sequencer.
- Pick a motion mode. Wave: adjust amplitude, per-voice frequency spread (more chaotic), phase and rate. Strum: spread, curvature, direction (one way, opposite, alternating) and alternate rate. Arp: rate, gate, up/down/up-down/random. Swarm: centre, cohesion (tight to loose) and rate. Set steps and window size, tempo-synced if wanted, and randomise.
- Shape the tail: feedback, decay, damping, stereo spread, diffusion; add vibrato rate/depth; balance dry/wet.
- Switch to live keys so the held notes set the voices (one note, two notes, four notes), or gated mode to sound only while keys are held. Try a pad or piano as input with mix fully wet.

### Struck-string physical-model synth controls that differ from subtractive synthesis: brightness set before the strike (not a filter), frequency-dependent decay (cutoff + slope) instead of sustain, strike point, harmonicity, three-string unison, and mallet-bounce retriggers at different note values per layer for sequenced polyrhythmic patches
Source: [Syngular: Pianoteq's New Physically Modeled Synth // Walkthrough & Demo](https://www.youtube.com/watch?v=B3n9GOT0Q9A) · was `struck-string-model-pre-strike-brightness-frequency-dependent-decay-slope-mallet-bounce-polyrhythm-layers`
- Start from a sine-like init voice. Raise plucking/strike brightness to move toward a bright, saw-like tone. Test that turning it down while a note rings does not change that note.
- Edit the harmonic profile (raise some partials, lower others) for a new basic colour, and set unison width to detune the three strings per note for synth-style thickness.
- Shape length: fast attack for keys or slower for pads; decay and release for ring time. Set the decay cutoff and slope: partials above the cutoff die faster as slope rises (low cutoff + high slope = shortest, darkest tail).
- Set strike point (like pick position) and harmonicity (harmonic → inharmonic). With higher brightness and more bloom, inharmonic settings give steel-drum-like tones. Use smear to soften transients.
- Enable mallet bounce so a held note re-strikes; adjust bounce rate and decay over time.
- Build a sequenced patch with 2–3 layers and different bounce note values (e.g. dotted half, quarter, 8 beats). Turning off bounce on one layer will not stop the pattern while the other layers still bounce.
- Map mod wheel → LFO rate, vibrato and tremolo depth. Finish with EQ and effects (chorus, phaser, delay, compression) and a post filter if you need cutoff sweeps.
