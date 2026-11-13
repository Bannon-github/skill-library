# Granular and spectral texture design (freeze, clouds, blur, stretch)

Goal: Turn short sources into sustained, evolving textures with grain size, density, position, spray and freeze, live granular buffers, spectral blur/freeze/warp and extreme time-stretch.

**Theory:** Grains of 20-200 ms with smooth windows overlap into a continuous tone; position = which part of the source, density = grains/s, spray = randomness. Freezing position sustains a single spectrum.

**Hear it:** `sample-lab/theory/granular_cloud.py`

## Workflow
1. Pick a source with clear harmonic content (pluck chord, piano, voice, field recording).
2. Grain size 40-150 ms, density 20-80 grains/s, Hann/Gaussian window.
3. Modulate position slowly through the source, or freeze at a sweet spot for infinite sustain.
4. Add pitch spray quantized to octaves/fifths and stereo spray for width; keep pitch within scale.
5. Live buffer modes: feed a rolling buffer, map keys to slice positions, tempo-lock grain size for rhythmic mosaics.
6. Spectral: blur/freeze frames, warp formants, or stretch 8-50x (paulstretch) for tonal drones; layer with the dry source.
7. Finish with filter, reverb, and level under the main elements.
8. Hear the theory: run `/home/box/audio-tools/bin/python sample-lab/theory/granular_cloud.py` from the repo root and compare the sections; reuse its functions as a starting point for renders.

## Source techniques (merged, numbers kept)

### Frozen granular buffer as a playable 'wavetable' voice: capture an evolving sound, freeze, scan time position, sequence pitch via v/oct for overlapping grain polyphony, random-modulate time/size
Source: [Mutable Instruments Beads FREEZE Explained – Frozen Textures & Tricks](https://www.youtube.com/watch?v=Dazk-D79k5U) · was `frozen-granular-buffer-as-playable-wavetable-voice`
- Run the granular processor fully wet; generate grains with the seed control; set mid size and a triangle grain shape (fades in and out cleanly); add reverb — integral to big ambient textures.
- Patch a gate into the seed input and adjust density (grains per seed — it can reach audio rate).
- Select a lower-quality buffer mode to get more record time (presenter: ~10 s stereo / 20 s mono), play an evolving sound in, and freeze it.
- Scan the time/position control through the frozen audio — like creating your own wavetable.
- Patch a pitch sequence into v/oct so the frozen buffer is played melodically; use the internal random modulators (attenurandomizers) on time and size; add reverb and delay. Overlapping grains give a polyphony-like overlap.
- Try reversed grains for variation.
- Dark texture variant: capture a simple tone, pitch the frozen buffer down with density high and reverb high, keep slow random modulation on time so it scrolls and occasionally surfaces higher partials ('ominous wind chimes'); play root changes from a sequencer.
- Optional: modulate freeze itself with gates to alternate between live grains and long held frozen notes.

### Granular buffer core from the ground up: grain size/shape/pitch, regular vs random density, triggered grains as a voice, position delay, freeze scrubbing, partial re-freeze, random pan, two feedback modes
Source: [Clouds (and clones) from the Ground Up: a reverbless explanation of a Granular icon](https://www.youtube.com/watch?v=mBvUObtJTJI) · was `granular-buffer-core-position-density-freeze-feedback-modes`
- Turn internal feedback and reverb down. Feed a simple source (sine) and listen to individual grains.
- Grain structure: size sets grain length (tens of ms → ~1 s); shape/texture morphs from no contour (gate) through triangle to Hann-like windows; use gate-like shapes for individual grains and Hann for overlapping grains; pitch shifts each grain up/down.
- Grain generation: density at noon = no grains; one direction = evenly spaced grains getting faster until they overlap; the other = randomly spaced grains until they overlap. Fine control near noon matters for counting individual grains.
- Triggered voice: density at noon, feed clock-derived gates into the trigger input and quantized pitch per grain from a random/looping sequencer; send an occasional pulse into size to lengthen some notes.
- Position: switch to a varied source (speech/radio). Small grains + enough density reconstructs the input; moving position away from the newest end adds a growing delay (there's always a tiny conversion delay at minimum).
- Freeze (fully wet): buffer stops updating; the same grain repeats at the current position; shrink size from a whole word to a tiny tone, then sweep position to scrub through captured audio (note: newest audio sits at one end, so 'forward' playback means moving position toward the older end).
- Evolving buffer: gate the freeze input with semi-random gates so it briefly unfreezes, writing a few seconds of new audio at the front while the rest of the buffer is kept.
- Post-processing: set wet/dry blend; use random L/R grain panning to turn a mono input into a stereo output; add reverb externally if preferred.
- Feedback: when live, it's true feedback of output into the buffer input (can run away — tame by modulating size/position); when frozen, feedback becomes a separate delay + all-pass diffusion that sounds reverb-like without altering the buffer. Watch for jumps when unfreezing.

### Stack granular processors to freeze any short sound into infinite sustain
Source: [Sound Design Trick - Creating Sustained Textures with Granular FX](https://www.youtube.com/watch?v=dxWCEDePgaw) · was `granular-stack-freeze-infinite-sustain-texture`
- Start from a short source with silence gaps. Insert a granular processor; prefer a dense multi-band or 'schizophrenia-like' starting point, link bands, reduce pitch variation slightly, keep light rand on pitch/pan/delay, ~one voice per band.
- Stack the same granular treatment about four times in series or parallel. Independent randomization + slowly moving band limits across instances fills holes into a complex continuous sustain.
- Add upward compression/OTT-style processing to lift grain detail, then high-pass — sustained stacks often accumulate unwanted low end.
- Animate tone: slow random modulation on a few EQ/filter bands (gentle boosts/cuts, light phasing at low mix, optional talking low-pass on the highs). Keep modulation subtle so it does not read as a phaser solo.
- Optional smear path: 100% wet diffused delay (modulated delay time) when you want less discrete echoes and more smooth wash. Finish with a limiter to restore level.
- Sum to mono and confirm the bed still works (point-source playback). Apply the same chain to non-synth sources (pebbles, debris) to verify generality.

### Granular slicer workflow: map keys to grain position instead of pitch (key→transpose 0, key→position up) with glide between slices, lock grain size to tempo in ms, per-parameter variation and L/R pitch spread for an icy cloud, an envelope that morphs grain shape and size per note, scan + per-ear LFOs for glitch, and a square-LFO auto-recapture of live drums every two bars
Source: [granulate EVERYTHING](https://www.youtube.com/watch?v=ZVLM1XMT6Z0) · was `key-mapped-grain-position-slicing-glide-between-slices-tempo-locked-grain-size-auto-recapture`
- Load a recording into the granular sampler and learn the three modes: classic (overlapping, sustained), loop (non-overlapping; set reverse chance) and cloud (stacked grains, density control).
- For a pad: check the sample's pitch with a tuner and transpose so C3 plays C. In cloud mode turn up variation, with orange per-parameter amounts on grain size, a little transposition (chorus) and volume; reduce position variation if too scattered. Add spread for different L/R pitch.
- For slicing: set key→transpose and key→filter to 0, set key→position up. Each key now plays a different region. Enable mono + glide to glide between slices; reduce grain size so position changes faster. Use it for vocal-chop patterns and transpose to the song key.
- Tempo-lock grain size: measure a note length in ms (e.g. select a quarter note and read its duration, 408 ms in the example) and type it in. Remember +12 st transposition halves grain duration (76.1 → ~38 ms).
- Transient shaping: route the modulation envelope negatively to grain shape (pointy → regular) and to grain size (small → normal), decay ~1 s, in classic mode.
- Glitch motion: set scan to ~0.25× and modulate grain size and position with an LFO that differs per ear. Record knob automation while playing.
- Generative recapture: feed live drum clips (random follow actions, legato on) into the granulator's capture input; drive capture with a square, skewed LFO every two bars; hold one note and scan slowly; map an LFO to grain size/shape. Resample the result to layer under the beat.

### Live rolling-buffer granular processor with per-grain behaviour modes: interval 'mosaic' clouds, per-grain pitch glide, reverse+wow smear, ghost-grain bloom, LFO tide, fixed-position constellation patterns and orbiting read head
Source: [Celestine - A Realtime Granular Dream Machine (Full Walkthrough)](https://www.youtube.com/watch?v=3q-o772IYQY) · was `live-rolling-buffer-granular-grain-behaviour-modes-mosaic-glide-bloom-tide`
- Insert the processor on a track (balance dry/wet) or on a send at 100% wet. A one-bar ring buffer records whatever plays, and grains are read from it continuously.
- Set the base cloud: size (grain length), density (grains at once, sparse to dense), spray (how far from the playhead grains may be fetched; 0 = exactly at the playhead), pitch in perfect-fifth steps, jitter (slight per-grain pitch warble, good for cloudy drones), spread (any pitch per grain, extreme), stereo (grains scattered around the field; presenter keeps it high), reverse chance, and smooth (roll off top end if grains get clicky).
- Playhead: scrub manually, or quantise it to eight positions (eighth notes in the one-bar buffer) to land on downbeat transients, or set a move rate (slow/fast, forward or reverse) to scan automatically.
- Sync sub-mode: when synced, grains fire on time divisions (e.g. 16ths) and size switches to note lengths. Each behaviour mode below has a free and a synced variant.
- Mosaic: pitch successive grains into chordal intervals (a couple at root, then +7, +12 …) with a soft bloom and slight lo-fi. Pick an interval set: fifths, major, minor or discordant. Reduce density; add jitter or spread. Good for pads with lots of reverb.
- Glide: each grain glides up in pitch (micro-portamento). Glide depth sets the interval; grain size sets how long it takes, and a shape control sets the curve. Long grains give a smooth effect; percussive input makes a texture generator.
- Reverie: force all grains into reverse and add tape-like wow/flutter (wow depth control) with a slight lo-fi tone; longer sizes give stretched tape-echo smears. Reverse chance has no further effect here.
- Bloom: every triggered grain spawns a secondary ghost grain that enters slightly later, quieter and subtly detuned. Raise density and size for overlapping halos.
- Tide: a global LFO makes all grains swell and recede in playback rate together. Long size = ambient breathing; short size = tremolo-like.
- Stars: ignore the heads and read grains from fixed positions in the buffer. Spray becomes a pattern selector (forward, reverse, pendulum, random), which cycles each bar into recognisable melodic or rhythmic fragment loops.
- Orbit: grains circle the write head in a spiralling orbit. Spray becomes orbit width, plus a slop control for imperfection/lo-fi. Works best at slow tempos and lower densities and plays alongside the dry signal like its own loop.
- Finish inside the grain path: a wavefolder or bitcrusher with its own mix for grit, then a simple hall reverb (decay + mix); long decay feels almost frozen. Revisit playhead/spray/sync after picking a mode, since each changes the mode's result a lot.

### Marimba/pluck WT LFO attack into granular freeze pad stack
Source: [Tutorial #21 | Turning A Marimba Into Granular Synthesis Pads](https://www.youtube.com/watch?v=Daqws1QWgXw) · was `marimba-wt-lfo-pluck-to-granular-pad`
- Pluck layer: one osc with a mallet-like WT (rich highs at frame 0 → sine at the end). Modulate WT position with LFO1 at a very high rate so you mostly hear the bright click, then the sine body.
- Amp envelope: decay ~0.5 s, sustain 0, release ~1 s. Add delay+reverb. Optional: set LFO to trigger (retrigger) mode so fast WT scrubbing repeats like a decaying delay while amp has no sustain.
- Swell twin: duplicate the pluck patch and add substantial amp attack so the same WT becomes a slow pad swell (works with one-shots too — just raise attack).
- Sequence sparse chord tones (e.g. B D F#) split across two octaves so each note can ring; render/print pluck and swell passes to audio.
- Load both into a granular engine: random fully up (forward/back from random points, occasional overlaps), loop on, raise grain attack and adjust grain spacing to slow frantic textures, increase hold for more sustain. Match settings on the swell buffer.
- FX: delay with low feedback (~3 repeats), room reverb ~20% mix with highs eased, plus a parallel bus of very long verbs (~10–12 s) at 100% wet while keeping a dry path for clarity.
- Optional bass: quiet triangle with chorus and long attack (mallet pads rarely need loud subs). Optional high air: heavily blurred/smudged print of the pluck and/or low-level ambience into the same reverb bus.

### Oscillator-as-delay: LFO repeats + stepped pitch-shift grains
Source: [How to Turn Any Synth Into a Granular Delay ✨ | Vital Pad Tutorial](https://www.youtube.com/watch?v=XVHx0eCGf5g) · was `osc-as-granular-pitch-step-delay`
- Dry voice: osc1 on basic/WT shape; use a non-global envelope (env2) on osc1 level so amp envelope 1’s release can later control delay ring-out. Filter with driven LP (~24 dB), key track, env3→cutoff (decay/release up, sustain ~halfway, some attack).
- Optional: sculpt WT (sine↔saw spectral blend), macro→WT position + cutoff; velocity→filter attack and env3 depth for soft vs bright hits; light unison (~2%).
- Delay osc: enable osc2, copy osc1 waveform. Instead of an ADSR on level, draw an echo-like shape on LFO1 and map it to osc2 level; tempo-sync LFO1 to set delay time.
- Feedback/fade: use global envelope release to control how long repeats die out. Fade-in: another LFO in envelope mode with a ramp-up modulating the delay-level mod depth so repeats don’t pile on the dry attack.
- Granular pitch sanding: LFO in envelope/step mode → osc2 pitch; set amount to +24 semitones (two octaves) with steps aligned to the delay subdivision (e.g. each quarter step up) so each repeat rises in pitch like a granular pitch-shift delay.
- Link formant-scale / WT position macros so delay osc timbre tracks the dry sound. Optional reverse-delay style LFOs: leave space in the shape to fade down and avoid clicks; try faster eighth-note rates.

### Record a piano for maximum sustain and resonance with a contact/geophone pickup (about 10 Hz–1 kHz) at the most resonant spot plus air microphones inside and above the body for the highs, build a sampler with per-mic blend and a lowpassed 'muffled' mix, then make ambient textures by extreme time-stretching held notes and tails (FFT size: small = grainy, large = smooth; tonal vs noise emphasis) and reuse samples as wavetables, looped dual-sample pads and phaser-hollowed basses
Source: [Field Recording a Piano - Exploring Resonance & Sustain](https://www.youtube.com/watch?v=bIbOgZn1h_Y) · was `piano-resonance-multimic-contact-plus-air-mics-blend-sampler-then-paulstretch-fft-size-tonal-noise-extreme-stretch-and-sample-to-wavetable-patches`
- Attach the contact pickup at several spots and play the same notes; choose the spot with the longest natural sustain (bottom corner next to the lowest key in the video).
- Add air mics: one inside the closed lower body, one on the lid near the keys, to recover highs above about 1 kHz.
- Record every note several times, letting each ring out fully, and record the key-release noise too.
- Denoise, chop, and align all mic tracks; map them into a sampler with a volume control per mic, plus a mix lowpassed to about the contact-pickup range.
- Extreme-stretch held notes, chords and short tails with an FFT stretch tool. Try small FFT sizes for grain and large for smoothness; shift tonal vs noise emphasis; pitch-shift the results.
- Load samples as wavetables: try 16 unison voices with zero phase randomisation; for a bass, add an extreme phaser (many poles, high feedback) and a 'muted' lowpass macro.
- Make a pad or bass from two loops of the same note with slightly different loop lengths, panned left and right, blended with a resampled wavetable and drive.

### Spectral blur/freeze pad: capture incoming audio as spectral frames and morph frame-to-frame at tempo-synced blur rates (quarter notes, plus simultaneous triplet/dotted rates for polyrhythms) with a per-frame attack/decay envelope, pitch the blurred signal ±24 st (semitone-quantised), choose clicky vs lush modes, play frames forward/backward, freeze completely, and modulate with curves, cross-modulation and a kick-sidechained follower on dry/wet
Source: [Magic Blur - Overview and Tutorial](https://www.youtube.com/watch?v=mllvToyambI) · was `spectral-frame-blur-freeze-pad-polyrhythmic-blur-rates-quantized-pitch-lush-mode-sidechain-wet`
- Insert the spectral blur on a source and set one blur rate (a quarter note: one frame morph per beat).
- Adjust the per-playback envelope (attack/decay) to hear or hide the frame steps.
- Add simultaneous blur rates including triplets and dotted notes for polyrhythmic blurring.
- Pitch the blurred signal up or down (to ±24 st), enabling semitone quantisation for musical intervals.
- Choose the flavour: rhythmic (clicky metallic), melodic or lush (washed out), or mixed; set playback direction forward/backward.
- Enable freeze to stop the frame morphing and sustain the captured spectrum.
- Modulate envelope and pitch with drawn curves (randomise, invert, shift, skew, morph between up to four curves); cross-modulate the first layer's LFO rate; add an envelope follower in sidechain mode from the kick to move dry/wet and curve amounts.

### Glitchy micro-loop buffer for ambient textures: freeze-and-scan buffer with segment length, pitch that cascades through feedback, temporary pitch from sample-rate steps, unlinked L/R (+12 / −12 st with cross feedback) and binary-random LFOs toggling freeze and reverse per side
Source: [Ableton's best kept secret for ambient textures](https://www.youtube.com/watch?v=KVtxIwYpGvQ) · was `stereo-unlinked-micro-loop-buffer-binary-random-freeze-reverse-cross-feedback`
- Insert the buffer delay. Learn the basics: position = delay time, feedback = repeats, segment = how much of the captured audio plays back, reverse toggle.
- Freeze/hold: play a phrase and engage hold. Now position scans through the frozen buffer and segment sets the loop length. Add random start position (and/or an LFO), and use short mode for fine, small segments.
- Pitch: set +12 st (or a fifth). Each feedback pass pitches up again, so engage the high-cut to tame the cascading brightness. Try sample-rate steps (e.g. 10k, down an octave and again) for temporary pitch effects and crunch; add a little vibrato. Low and high cut together give band-pass tones.
- Unlink L/R channels so each has its own position, segment, pitch and LFO. Set L +12 st and R −12 st, and set the feedback routing to cross (each side feeds the other).
- Map the important controls to macros. Add two LFOs in binary (random on/off) mode at different rates on freeze L and freeze R, set as remote control so they aren't hand-moved.
- Add two more binary LFOs on reverse L and reverse R, and one random (not binary) LFO with full range on the sample-rate/bandwidth control that steps between octave settings.
- Optionally add a hybrid reverb, and lower dry/wet so the effect becomes a whisper in the background.

### Three-pillar cinematic drone (layering, movement, FX): wavetable VCO pair + self-feedback delay loop + granular layer, effects after filters with master low-cut as tension control
Source: [Ep. 04 | How to Build Powerful Cinematic Drone Sounds (Modular Synth Sound Design)](https://www.youtube.com/watch?v=aNVjrDQANMw) · was `three-pillar-drone-wt-feedback-loop-granular-filter-before-shimmer`
- Layer 1: two wavetable VCOs on separate VCA channels, VCO2 one octave below; slowly modulate VCO2's level so the sub appears sometimes; low-pass to cut buzzy harmonics.
- Movement on layer 1: very slow LFO on wavetable position/axis; optionally resonance/drive/wave-shaper for more harmonics.
- Layer 2 (feedback loop): with no input, raise the processor's feedback until it starts self-generating; keep delay lines close; run it into its own resonant low-pass; if feeding output back to input, attenuate it first and lower input gain.
- Layer 3 (granular): record 2–3 different short sources (even a click or mic sound) as layers; set intensity (grain count), short grain length for lo-fi, quantized pitch randomization; use follow mode to auto-scan through the recording, forward or reverse; overdub (e.g. whistling) for new tones.
- Movement on layer 3: sample-and-hold selects which recorded layer plays; an LFO modulates grain length.
- Sum layers, then a master low-pass with resonance BEFORE shimmer reverb and delay so resonant low harmonics feed the reverb.
- Use the master filter's low cut / cutoff as the tension control: more high frequencies = tension ('something is coming'), lows = suspense; choose reverb type for mood; end a scene by pulling inputs out and leaving a little wet.

### 90s sampler pad: loop a single bounced synth note in a repitching sampler, play chords so each voice scrubs the loop at its own speed, ping-pong loop, wide voicings, slow filter LFO, then resample the chord and play it again for parallel harmony
Source: [Use this 90s sampling technique for ethereal pads](https://www.youtube.com/watch?v=XAch1Q0Iodc) · was `sampler-loop-chord-scrub-parallel-harmony-pad`
- Play and bounce one sustained note from a synth pad to audio (for the parallel-harmony variant, bounce a full chord instead).
- Load it into a sampler in repitch mode, set a loop over the sustain, and raise the voice/polyphony count so chords can play.
- Play a chord and hold it. Each voice reads the loop at a different speed and pitch, so the loops drift and overlap. The longer you hold, the more the texture varies.
- Switch the loop to ping-pong so some voices bounce back from the loop end, for more texture variation. Try playing lower on the keyboard for a slower, darker drift.
- Shape voicings: keep the roots close together and put 7ths/9ths an octave or more up. Those upper voices scrub much faster, adding motion on top. Optionally move the root down a semitone or tone in a multi-sample map.
- Add a slow LFO to the sampler's filter cutoff so the pad breathes; also try transposing the whole sampler for different feels.
- Resample: bounce the played chord to audio, load it into a new sampler and play it. Each key now plays the whole chord shape (parallel harmony), with the drift texture baked in. Loop and repeat if you want.

### Turn a static one-shot or multisample into a playable synth with subtractive tools: map it chromatically, mono or poly with a set release, a low-pass with envelope depth for sweeps or plucks, resonance for acid, an eighth-note square LFO for stepped filter jumps, layer an octave copy (or different samples) through one filter so they fuse, then distortion/chorus, a reversed octave-up granular layer and reverb
Source: [How to Turn Samples into Synths](https://www.youtube.com/watch?v=HyXvY_PXI9Q) · was `sample-to-synth-keygroup-mono-lowpass-env-pluck-resonance-square-lfo-steps-octave-layer-through-one-filter-reversed-octave-granular`
- Load the sample as a keygroup/chromatic program with the root set correctly; for bass choose one-shot + mono, for chords choose poly with a longer amp release.
- Engage a low-pass filter, turn the cutoff down and the envelope depth up: a slower decay gives a sweep, a short decay gives a pluck.
- Raise resonance for an acid character, or raise amp attack and hold for a swelling pad.
- Assign a square LFO synced to 1/8 to cutoff with moderate depth for rhythmic stepped filter jumps.
- Layer a second copy of the sample an octave up (or a different sample), adjust pan and level, and run both through the same filter.
- Add FX to taste: gentle distortion to thicken, chorus (check phase), a granular layer pitched +12 and reversed for space, and reverb.
- Optionally resample the result or use the sample as a wavetable/granular source in a synth for further shaping.

### Arp-smear pad: arpeggiate a minor-9 chord (down pattern, long gate) through a grain delay and a delay with reverse, resample it, stretch the audio to double length with pitch-preserving warp, then smear it with a high-wet, high-feedback echo, a spectral freeze retriggered every 1/16 note and an EQ band-limit; plus a feedback-mode distortion on a melodic loop (100% feedback path, dotted 1/2 time, band-pass centred ~3 kHz with its width modulated by a 1-bar LFO) resampled and re-looped for a second melodic element
Source: [Made in Ableton Live: K. Hart on creative resampling, granular techniques and more](https://www.youtube.com/watch?v=LANPsnGB_yY) · was `arp-smear-pad-grain-delay-resample-stretch-2x-high-wet-echo-spectral-freeze-retrigger-16th-eq-band-plus-feedback-bandpass-loop-motion`
- Write a one-chord MIDI clip (A minor 9) into a soft synth; arpeggiator on, down pattern, rate as wanted, a few octave steps, long gate.
- Add a grain delay (pitch 0) and a delay with reverse repeats after the synth.
- Resample to a new audio track while adjusting grain-delay spray/frequency by hand.
- Warp the clip (pitch-preserving mode) and stretch it to double length.
- Add an echo with high dry/wet and raised feedback so notes smear together.
- Add a spectral freeze with freeze on and retrigger every 1/16 note to smooth the sound into a sustained pad; then an EQ to confine it to its frequency band.
- Feedback layer: on a melodic loop, a distortion in feedback routing with 100% blend to the feedback path, feedback amount up, time set to dotted 1/2, feedback band-pass centred ~3 kHz; modulate band-pass width with a 1-bar synced LFO; add light distortion.
- Resample it, then loop short regions of the recording (e.g. bars 18-22) and move the start point to find new phrases.
