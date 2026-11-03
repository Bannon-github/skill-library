# Modulation: LFOs, envelopes, sample & hold, random and nested routing

Goal: Animate sounds with a mod matrix: LFO rate/sync/shape, envelopes and curves, sample & hold, smooth random, envelope followers, per-voice random offsets, nested modulation (mod of mod depth) and random/probability gates.

**Theory:** Modulation = control signal x depth added to a parameter. Rate decides perception: <1 Hz drift, 1-10 Hz rhythmic/vibrato, audio rate = new timbres (FM/AM). S&H samples a source at a clock -> stepped random.

**Hear it:** `sample-lab/theory/modulation_lfo.py`

## Workflow
1. List targets (cutoff, wavetable pos, pitch, pan, amp) and pick one source each in the matrix.
2. LFO: sine/triangle for smooth, square/saw for rhythmic; sync to tempo (1/8 wobble, 1-4 bars sweeps) or free for drift.
3. Envelopes: shape curves (exponential attack = natural); a second env can modulate the first's time.
4. Random: S&H for stepped, smoothed random for organic drift; per-voice note-on random offsets for analog variation (compensate bipolar offsets).
5. Envelope follower: drive cutoff or width from a drum bus for audio-reactive motion.
6. Nest: velocity -> env depth -> LFO depth -> cutoff; keep total depth capped so extremes stay musical.
7. Gates: noise-derived random gates, comparator windows and probability skippers for generative triggers.
8. Hear the theory: run `/home/box/audio-tools/bin/python sample-lab/theory/modulation_lfo.py` from the repo root and compare the sections; reuse its functions as a starting point for renders.

## Source techniques (merged, numbers kept)

### Envelope follower: audio loudness as a modulation source (fold, ring mod, ducking, playback rate)
Source: [Using Envelope Followers for Modulation in Your Music! The How, the When, the Why](https://www.youtube.com/watch?v=odosCwWVL2c) · was `envelope-follower-audio-driven-modulation`
- Contrast with an LFO: an LFO cycles a parameter regardless of the music; an envelope follower raises the parameter when the source gets louder and lowers it when quieter.
- Insert the follower on the source channel, set it to output its envelope as a control signal, and map it to the destination (e.g. wavefolder fold amount) via learn/assign; disable any competing LFO on that parameter.
- Tune Depth for how aggressive the effect is, and raise Rise/Fall times to reduce volatility (slower up and down movement); lower them for jittery, transient-tracking motion.
- Stereo opposing motion: use the left and right follower outputs on two separate lanes into two ring-mod (or similar) depths, invert one, so one rises as the other falls when the source gets louder.
- Kick-keyed motion: follow the kick and map to a pad's channel volume. Non-inverted = sidechain expansion (pad louder on kicks); inverted = ducking (quieter on kicks). Same mapping inverted onto fold or a filter opens the effect in the gaps between kicks.
- Texture rate: follow a looped percussive/mechanical sample and map to its own playback rate (faster when loud, slower when quiet); invert to speed up in the gaps. Optionally use that loop's follower to duck a synth.
- Optional follower types where available: pitch follower (higher pitch → higher value) and spectral-brightness follower (brighter → higher value) instead of amplitude.

### FM depth and LFO mix evolving chase sequence
Source: [TRAVELER Track Walkthrough by Venus Theory](https://www.youtube.com/watch?v=jLGz5wq2CRE) · was `keysol-venus-fm-lfo-evolving-chase-sequence`
- Establish rhythmic pulse/sequence foundation (arp or control-track → cutoff). Aim for cinematic intensity rather than clean EDM purity.
- Introduce FM: vary modulator frequency slightly and automate/modulate FM depth so timbre breathes over the phrase.
- Use LFOs to change oscillator mix balances over time; also modulate filter cutoff so the sequence refuses to feel static across long cues.
- Assign mod wheel / aftertouch to open tension (depth, cutoff, or drive) for scene dynamics.
- Play deeper registers for more body when the cue needs weight; keep FX (delay bounce) feeding syncopated rhythms for living grooves.

### irregular dual control-track pitch sequence
Source: [TRAVELER Track Walkthrough by Venus Theory](https://www.youtube.com/watch?v=jLGz5wq2CRE) · was `keysol-venus-polyrhythmic-control-track-pitch`
- Create a stable bed on Osc3 (e.g. pulse) an octave or two below; add delay/space lightly so the bed feels cinematic but steady.
- Raise Osc1 and Osc2 to much higher pitch registers; they need not sound pretty alone — they supply character over the bed.
- Control Track A → Osc1 pitch, length 15, rate dotted-quarter (or similar). Control Track B → Osc2 pitch, length 14, rate quarter. Keep modulation depth small so pitch breaks subtly rather than jumping wildly.
- Map mod wheel (or expression) to increase the depth of those pitch mods for performance tension.
- Mix: keep Osc3 dominant; blend high oscs underneath. Solo high pair to verify the irregular interlocking, then restore full mix.

### Modulation basics: LFO vs envelope, then mod-matrix source→destination routing
Source: [Merged from 2 YouTube how-to transcripts](None) · was `modulation-lfo-envelope-mod-matrix-routing`
- Treat LFO as a very slow oscillator (usually below hearing): set shape (sine/tri/square/saw/custom) and rate, then assign to a destination so the parameter follows the oscillation.
- Classic LFO recipes: → amp = tremolo; → pitch = vibrato; → low-pass cutoff = wobble; → waveform/PWM/WT position = evolving source timbre. Tempo-sync for rhythmic motion or keep slow free-rate for subtle drift.
- Raise LFO rate into audio range: amp mod → AM sidebands; pitch mod → FM-like spectra; very fast FX-param mod (e.g. phaser) can become a distortion/timbre effect.
- If available, try LFO one-shot mode—shape plays once, behaving like an envelope.
- Amp envelope ADSR: Attack = fade-in time; Decay = time to sustain; Sustain = held level (if sustain = max, decay has no effect); Release = fade-out after key-up. Percussive: attack+sustain low, length from decay (+ some release). Pad/violin-like: longer attack+release, sustain full.
- Filter envelope: assign to cutoff with ±amount/depth. Positive amount opens from a low cutoff (plucky bass with short A, some D, no S, short R). Negative amount with high cutoff can wah downward; longer attack + positive amount opens wah; raise sustain to keep open while held.
- Ensure amp envelope lets enough signal through to hear filter motion. Also try envelopes on PWM or wavetable position so the source evolves per note.
- Mod matrix: Treat the mod matrix as deep synthesis: any controller source (self-running LFO/env or performer control like wheel/key/pedal) can move any available audible destination (pitch, cutoff, amp, vibrato rate, pan, delay params, …).
- On an init/simple patch, create a route: choose source, choose destination, raise amount. Prefer starting with destination = oscillator pitch so the modulation shape is immediately audible.
- Example performer control: mod wheel → filter cutoff. Lower cutoff, raise amount, move wheel; set wheel to max while trimming amount for the brightest intended ceiling. Add resonance/delay for musicality.
- Retarget or add destinations: pan, volume, delay amount/regen/time, etc. Stack multiple routes so several parameters move together for evolving pads.
- If a route is hard to hear on its real destination, temporarily assign that source to pitch to audit the shape, then reconnect to the intended destination with an appropriate amount.

### Nested modulation depth chain: velocity → envelope decay → LFO 2 amount → LFO 1 amount → filter cutoff, for touch-sensitive rhythmic filter motion
Source: [Modulate the modulations to expand your sound design with Magnolia!](https://www.youtube.com/watch?v=pYbWRCrFsHQ) · was `nested-modulation-depth-chain-velocity-env-lfo-lfo-cutoff`
- Start from a default patch: simple subtractive tone, close the low-pass filter, play in a lower register.
- Degree 1: LFO 1 → cutoff. Sawtooth, unipolar (acts like a looping envelope); add phase bend for a snappier shape; tempo-sync to 16ths, and raise the tempo a little if needed.
- Degree 2: set LFO 1's amount to zero. LFO 2 = square, unipolar, synced to quarter notes; assign it to LFO 1's amount so it ducks LFO 1 on and off. Try other resolutions; the presenter likes quarter-note triplets. Optionally add more cutoff modulation.
- Degree 3: set LFO 2's amount to zero. Assign a spare envelope (e.g. one otherwise used for FM) to LFO 2's amount, fully up. Sustain sets the overall motion; use decay to bring the whole modulation up then away.
- Degree 4: set that envelope's decay to zero and assign velocity to the decay. Soft playing gives no modulation; harder strikes emphasise it.
- Refine for consistency: use the same velocity on filter modulation, add keyboard tracking so upper notes are brighter, use the envelope's slow mode for a longer tail, add release time and put velocity on the release too.

### Patch three random-gate tools from generic functions: noise sampled-and-held by a clock into a window comparator, ANDed with the clock, as a probability gate skipper (window size = probability); the same with S&H output fed back into the clock rate for free random bursts; and a Bernoulli gate where comparator out and not-out each AND the clock to trigger two panned voices
Source: [Patch Programmability - Episode 4 - Random Gate Generators](https://www.youtube.com/watch?v=uorRN6iH87U) · was `random-gate-generators-from-noise-sample-and-hold-window-comparator-and-logic-probability-skipper-free-random-burst-clock-feedback-bernoulli-two-voice`
- Run noise into a window comparator; trigger an envelope → VCA on a voice from the comparator output. Set window size very low and move shift.
- Add sample-and-hold: noise into S&H input, a cycling clock into S&H clock, S&H output into the comparator. Set shift high so only the top of the held range passes.
- AND the comparator output with the original clock (second comparator, logic module, or a VCA with clock as input and comparator as CV). Use window size as the probability: max = all clocks pass, closed = none. Listen against a second voice playing the raw clock.
- Free random variant: patch the S&H output into the clock's rate CV.
- Bernoulli variant: remove the feedback; take comparator out and not-out, AND each with a copy of the clock, and send them to two envelopes: one on a higher voice panned slightly left, one on a lower voice panned slightly right.
- Sweep size: fully clockwise = only the high voice, fully counter-clockwise = only the low voice, middle = random choice. Then modulate size with a slow LFO and add clock-rate feedback for a generative patch.

### Evolving cinematic drone: random-modulated LFO rates on WT position and two parallel, opposite-panned filters, plus a randomized granular sample layer and FX chain
Source: [Create Evolving Cinematic Drones In Pigments - Full Tutorial](https://www.youtube.com/watch?v=fxh2ccZKEb0) · was `random-rate-lfo-wt-drone-parallel-panned-filters-granular-layer`
- Wavetable engine: pick a folded/rich table; route LFO1 (free-running, very slow) to wavetable position from a start around the table's middle.
- Make LFO1's speed drift: route a slow, smooth, free-running random modulator to LFO1 rate with a small amount (~0.07) so the sweep speeds up and slows down unpredictably.
- Size: super-unison with ~2.4 detune, main tune 0; no glide/legato.
- Amp envelope: ~1 s attack with slightly positive curve, ~4 s decay, slightly lower sustain, ~2 s release. Second envelope similar for filter.
- Filter 1: lowered cutoff with filter envelope, some resonance, keytracking (higher keys open more) and a little drive; add LFO1 to cutoff with a tiny range.
- LFO2: another slow free-running LFO whose rate is modulated by a second random source (~0.13). Add filter 2 as a 12 dB low-pass with character (MS-20-like), set filters to PARALLEL, send sources to both, and let LFO2 move filter 2 cutoff. Pan filter 1 ~40% left and filter 2 ~40% right.
- Engine 2 (granular): load an original granular-friendly sample into both filters; enable granular with random density both directions, random size, some random volume and pitch; change grain shape to triangle (smoother than the rhythmic default); scan the start position with LFO1.
- Add a little white noise into both filters (no sub needed).
- FX A: shimmer (bigger size) → tape echo ping-pong dotted 1/8 → multiband compression mostly taming lows (and some highs) while letting mids through. FX B: reverb (longer decay) → soft tape distortion → second reverb.
- Map mod wheel to distortion drive; trim low end/clipping as needed and save.

### Use sample-and-hold as a processor on another modulator (not as a random source): step a sine LFO at a rate, automate the LFO rate and the S&H rate separately on a filtered-noise riser so the end seems to slow down through aliasing, and turn a regular step pattern into random hat-loop volume dips with the inverse amount on an FX mix, on a duplicated layer
Source: [This is Sample & Hold | Cubase Modulators Explained](https://www.youtube.com/watch?v=SZKIODnJuwU) · was `sample-and-hold-as-processor-on-lfo-or-step-input-automate-lfo-rate-up-and-s-h-rate-for-noise-filter-riser-aliasing-slowdown-random-hat-volume-inverse-fx-mix-layer`
- Add a sine LFO and a sample-and-hold modulator, both in Hz. Route LFO → S&H input, LFO unipolar at maximum amount. Sweep the S&H rate from about 1 upward.
- Generate white noise through a filter and route S&H → cutoff; reduce the amount until it is not excessive.
- Compare with a simple riser: an upward-ramp LFO over 4 bars on both rates. Note it is linear and not editable; remove it.
- Expose the LFO rate and S&H rate as automation lanes. Ramp the LFO rate up to maximum over the riser; start the S&H rate low and shape it with its own curve and a few random moves.
- For a hat loop: draw a random 4-bar step pattern on a step modulator at 1/8, route it to the S&H input (unipolar, max), and route S&H → loop volume (unipolar, ~80%).
- Route the same S&H to the mix of a metallic FX with inverted amount, so the FX closes where the volume is high.
- Duplicate the channel: keep the original loop and use the modulated version as a second layer; let other loops fill the quiet sections.

### Sample-and-hold / random-glide LFO textures: random steps on pitch, wave position and filter, random glide squelch, user-drawn step LFO
Source: [Zebra 2 - Using LFO`s Random Features (Sample & Hold) - How To Tutorial](https://www.youtube.com/watch?v=IiWPL_v8Eqk) · was `sample-hold-random-lfo-pitch-wave-filter-glide-textures`
- On a basic saw oscillator, set LFO2 shape to random-hold (sample and hold) and route LFO2 → oscillator tune.
- Add reverb and delay (adjust delay times) for the old sci-fi computer effect.
- Swap to a stranger oscillator wave; keep the pitch depth low so it stays usable (even as a weird bassline).
- Route the same LFO2 to the wave/wavetable position (with the wave set mid) as well as tune; add lots of delay.
- Add a filter and route the S&H LFO to cutoff and resonance — be careful with high resonance.
- Switch LFO shape to random glide; set legato mode and turn glide up for squelchy random glides (psytrance-style). Note long sustained notes vs retriggered behaviour; speed the LFO up as needed.
- In the mod matrix, target voice volume with LFO2 scaled by the mod wheel.
- Use a user-defined LFO with 8 steps as a predetermined S&H pattern (it repeats, so not truly random) for basslines or leads; switch steps → lines so glide ramps between values.
- Bounce results to audio and chop short sections for SFX and quirky elements.

### ADBSSR curved-envelope evolving pad
Source: [TRAVELER: The Cinematic Hybrid Synthesizer | Official Walkthrough](https://www.youtube.com/watch?v=IU76c2Cygs4) · was `traveler-walkthrough-curved-envelope-evolving-pad`
- Set three envelopes: filter, VCA, and modulation. Open the on-screen envelope editor and drag curve handles on time stages.
- Use long time stages (up to ~20s each) for cinematic bloom. Expand envelope to add breakpoint + slope stages (ADBSSR-style) when you need a mid-bloom reshape.
- Route filter envelope to stereo LPF cutoff with moderate amount; VCA envelope for amplitude; mod envelope to WT position, pan, or secondary cutoff.
- Optional alt-control on mod envelope: start envelope from sustain pedal (or other mod-bus source) instead of key press for expressive delayed motion.
- LFOs: choose from varied shapes including unipolar and slew/random; key-sync or free; tempo-sync optional; dedicate pitch or filter vibrato with fade-in on LFO1/2.
- Finish with soft EQ, light chorus, long space/hall reverb (space algo up to very long tails). Keep limiter available as safety for dynamic patches.

### Wavefolded LFO wobble: fold a sine LFO for extra peaks/valleys, then slew-limit it before filter cutoff
Source: [Wavefolding LFO's in VCV Rack to make interesting wobble effects and unique waves Synth Sound Design](https://www.youtube.com/watch?v=k9ZURoAww0k) · was `wavefolded-lfo-slew-filter-wobble`
- Baseline: route a regular sine LFO to filter cutoff and listen.
- Insert a wavefolder between LFO and filter cutoff; compare the folded and plain sine on a scope.
- Slow the LFO down (folding multiplies apparent rate) and adjust fold amount, symmetry and fold shape.
- Add a slew limiter after the wavefolder, before the cutoff input, to soften the jumps.
