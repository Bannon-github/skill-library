# Drum synthesis and hybrid percussion (kick, snare, clap, hats, taiko, epic hits)

Goal: Synthesize a complete kit and cinematic percussion from oscillators and noise: kick pitch envelope, snare body + noise, 3-burst clap, hats, toms/taiko from noise with resonant filters, layered epic hybrid hits, ensemble multiplication, resampled velocity layers, and drive to cut through.

**Theory:** Drums are short envelopes on simple sources: kick = sine with fast pitch drop; snare = tuned body + noise; clap = repeated noise bursts; hats = high-passed noise. Layering + micro-timing (0-22 ms) creates ensemble size.

**Hear it:** `sample-lab/theory/drums_synthesis.py`

## Workflow
1. Kick: sine, pitch env 150 -> 45 Hz in ~35 ms, amp decay 200-400 ms, short click/noise transient; HP ~20 Hz, notch boxiness ~78 Hz if needed.
2. Snare: two sines (~180/330 Hz) + band-passed noise 1.5-9 kHz, decay 60-150 ms.
3. Clap: three noise bursts ~10 ms apart + tail, band 1-6 kHz; hats: noise HP >7 kHz, closed 20-40 ms, open 200-300 ms.
4. Toms/taiko: noise or sine through resonant HP/BP, velocity -> decay and filter, soft-clip + hall.
5. Epic hit: 4 parallel layers with pitch drops (+5/+29 st), noise burst, curved fast envelopes; distant boom = tom + sub + 6 dB LP + big reverb low-cut 100 Hz.
6. Ensemble: duplicate hits 4x with random 0-22 ms delays, ±40 pan, varied decay; resample to 8 velocity layers / round robins to avoid machine-gun.
7. Cut-through: band-pass a copy, overdrive it, blend parallel level-matched.
8. Hear the theory: run `/home/box/audio-tools/bin/python sample-lab/theory/drums_synthesis.py` from the repo root and compare the sections; reuse its functions as a starting point for renders.

## Source techniques (merged, numbers kept)

### Cinematic taiko-style ensemble drums from white noise: velocity sets the amp and filter decay, a resonant 60 Hz high-pass plus low boost adds weight, a tanh soft clip and limiter go before a large-hall convolution reverb, with optional detuned sine, FM sub and round-robin sample layers
Source: [EPIC Cinematic Drums from White Noise | A Sound Design Tutorial](https://www.youtube.com/watch?v=6CWmImkHDgs) · was `cinematic-taiko-ensemble-drums-from-white-noise-velocity-to-amp-decay-and-filter-env-resonant-hp-60hz-low-boost-tanh-softclip-limiter-before-convolution-hall-plus-detuned-sine-fm-sub-random-sample-layers`
- Load white noise in a fresh patch; set the amp envelope to sustain 0 and a short decay; widen the velocity-to-level range.
- Route velocity to amp decay so soft hits are short and hard hits ring out long.
- Add a low-pass (about 1 kHz) and a second envelope on cutoff with a short decay, opening bright at the attack and closing darker; scale its amount or decay by velocity and add a little filter drive.
- EQ for weight: resonant high-pass at about 60 Hz plus a low bell boost; cut mud, add some presence and a slight high shelf; add a little amp release.
- Soft clip with a tanh waveshaper (small drive), trim the output, filter a little extreme sub.
- Add a limiter, THEN a convolution reverb with a cathedral or large-hall impulse; shorten the decay, tame the low end, damp the highs and lift about 5 kHz.
- Optional layers: 3 detuned sines with a pitch-drop envelope (tone), an FM or sine sub at 20-50 Hz, and a round-robin layer of found-object or rattle hits with slight random pitch.

### Turn a synth tom-style epic drum hit into a distant low explosion / drop boom: harmonic bass enhance plus an octave-down sub, a 6 dB/oct low-pass instead of an attack boost, reverb low-cut around 100 Hz at 24 dB/oct, a band-limited quarter-note delay with about 7 ms early/late L/R offsets, a parallel tremolo or auto-pan tail whose depth is faded in by a delayed envelope, and an optional low comb filter (about 14-40 Hz) for a modern metallic drop
Source: [Epic Drums 2 - Sound design tutorial](https://www.youtube.com/watch?v=ZYn08bUlmG0) · was `distant-explosion-boom-from-synth-tom-sub-enhance-6db-lp-reverb-lowcut-100hz-stereo-offset-quarter-delay-env-delayed-tremolo-autopan-low-comb-metal-drop`
- Play the hit lower on the keyboard so it sounds less like a tom. Reshape the body with filter-envelope decay, cutoff, resonance and noise amount.
- Add harmonic bass enhancement plus a sub oscillator one octave down (two octaves only if needed). Move the low-cut EQ from about 83 Hz down to about 50 Hz and steepen it from 24 to 36 dB/oct.
- Remove any attack/snap boost band and replace it with a gentle 6 dB/oct low-pass.
- Reverb: low-cut the reverb itself at about 100 Hz with a 24 dB/oct slope (by ear), choose a large impulse and set the mix to about 40%.
- Optional: add a tempo-synced quarter-note delay with resonance off, high-pass the delay at about 90 Hz and low-pass it at about 4 kHz, and lower its level. Offset the left repeat about 7.3 ms early and the right about 7.3 ms late.
- Optional parallel tail: split the signal after the reverb into a parallel lane with a tremolo (rectangle, eighth notes, depth up, blend about 50%). Drive the tremolo depth with an envelope: delay about 140 ms, decay about 2 s (match the reverb length), sustain 0.
- Alternative tail: replace the tremolo with a quarter-note auto-pan using the same envelope on depth, or put distortion or other modulation on the parallel lane.
- Optional modern 'deep metal' drop: add a comb filter on the lane, tuned low, about 14-40 Hz (12 Hz is too low), with feedback about 50% and max frequency reduced to tame the highs. Blend it with the split ratio, and you can add the delay after it.

### Turn a flat sustained drone into rolling shaker-style percussion: loop and crossfade a stable bar, re-envelope it into rhythmic hits with a transient-preserving time-stretch gate at a fast note rate, then low-cut, boost one tuned mid harmonic, layer an organic shaker texture, snap it with a transient shaper and add a short parallel bright room
Source: [Crazy Percussions Out of a Pad in Serum 2](https://www.youtube.com/watch?v=EwxNeZttFEA) · was `drone-to-percussion-transient-gated-warp-mid-harmonic-eq-texture-layer-parallel-room`
- Find the most stable, least peaky bar of the drone and loop it. Crossfade at each loop join so there are no clicks, then consolidate to one file.
- Set a transient-preserving stretch mode with linear behaviour, choose a fast transient rate for shaker speed, then reduce the transient sustain/envelope until each step becomes a short hit. Raise level, add a small fade-in, and consolidate again.
- EQ: high-pass the low frequencies that are not part of the percussion, then boost one or two mid harmonics so the part has a pitch that fits the tune or groove.
- Layer an organic texture (tambourine/shaker-type) with less hold, more attack, a little more decay, slight pitch shift and higher density. EQ the texture to fill what is not poking through and reduce its decay.
- Add a transient shaper: raise attack, remove a lot of sustain, adjust speed so it is snappy but not overdone.
- Final EQ: bring up the gap left by processing, roll off extremes, and let the main harmonic breathe.
- Put a very short bright room (no pre-delay, little depth, ~22 ms) on a parallel chain beside the dry signal and mix it under.

### Make a weak drum (e.g. a clap) cut through and drive the groove with band-passed overdrive: choose the band that gets distorted, push the drive too far then back off, use tone to tame harsh top, set the dynamics control low for a tight punch, blend dry/wet, and level-match
Source: [Ableton Sound Design Tutorial - Drums That Cut Through The Mix](https://www.youtube.com/watch?v=oc5YQf_Xy14) · was `drum-cut-through-band-passed-overdrive-locate-band-push-drive-too-far-then-back-off-tone-as-top-cut-dynamics-low-for-tight-punch-dry-wet-parallel-level-matched`
- Solo the hit, bypass its reverb, keep its low-cut EQ.
- Insert band-pass -> overdrive -> gain utility in a group.
- Add a little drive and sweep the band-pass centre to find the range to emphasize; avoid murky lows; narrow the Q roughly.
- Push the drive too far to hear the effect, then back off (about 60%) until the brittle top isn't dominant; lower the tone to cut harsh upper mids if needed.
- Set the dynamics control low (about 20-30) for tight punch, or higher for a looser, washed-out feel.
- Set dry/wet (50-100%) in context with the full mix.
- Level-match with the utility against bypass, restore the reverb (adjust decay), and leave final tweaks to the mixdown.

### Epic trailer-style hybrid drum built from a four-layer synth hit (pitched additive and FM oscillators with very fast exponential pitch drops, e.g. +5 and +29 semitones, plus filtered white and pink noise bursts with overload, tube drive, MS-20-style low-pass and a high-pass) layered with any three acoustic drum samples including bleed/ambient mics, then glued with a scooped EQ, sub trim, multiband compression and gentle upward (OTT-style) compression
Source: [How to Make Your Own Epic Hybrid Drums WITHOUT Buying New Sounds (Tutorial)](https://www.youtube.com/watch?v=B75uC7h8bBo) · was `epic-hybrid-drum-four-channel-synth-hit-parallel-pitch-drops-plus5-plus29-st-curved-fast-envelopes-noise-bursts-fm-tube-layered-with-acoustic-bleed-mics-scooped-eq-multiband-upward-comp`
- Channel 1: additive/harmonic oscillator, stereo, with a pitch envelope dropping from about +5 semitones; fast exponential amp envelope.
- Channel 2: white noise into a low-pass whose cutoff envelope closes extremely fast with a strong curve.
- Channel 3: pink noise into an aggressive low-pass using the same envelope, then a second overloaded filter that also receives channel 1.
- Channel 3: FM (or triangle/square) oscillator with a very fast pitch drop into tube distortion, an MS-20-style low-pass, then a high-pass to cut rumble.
- Channel 4: a second additive high-content oscillator whose pitch drop starts about +29 semitones; play with channel 1 for parallel pitch drops.
- Add global EQ (two), compression and reverb; compare a less-curved envelope to confirm the strong curve is needed.
- Layer three acoustic drum samples, bringing up bleed/ambient mics (snare, hats, toms, room) so the low drum has life.
- On the combined layers: heavily scooped EQ, trim the very lowest subs, per-layer EQ (e.g. less top on the acoustic), multiband compression on the low band letting transients through.
- Optionally add OTT-style compression at low depth with more upward than downward; EQ after any extreme multiband effect.
- Render the acoustic element, set its notes to the sample's root pitch, apply the same fast envelope in the sampler and add velocity tracking to both layers.

### Resample a synthesized epic drum into a reusable sampler instrument: record 8 spaced hits on a velocity ramp into auto velocity-split layers (soften the velocity-to-amp curve so the softest layer is still audible), or record 8 slightly different hits as round-robins for fast repeats (16ths/32nds without machine-gunning), add velocity-to-low-pass (floor about 1-1.5 kHz) and small start-time jitter, and bounce a panned 4-5 instance ensemble as its own multisample
Source: [Epic Drums 4 - Sound design tutorial](https://www.youtube.com/watch?v=w8cSlVZ2KbI) · was `resample-synth-epic-drums-to-sampler-8-velocity-layers-vs-round-robin-anti-machine-gun-velocity-to-lowpass-1-5khz-start-jitter-ensemble-bounce`
- Set the sampler to record its input (external/aux input) with auto-advance to the next layer per hit. Turn off per-instance random envelope delay on the synth for a single-instance capture.
- Program 8 capture notes spaced far enough apart to decay fully (no dense 16ths), alternating a little for variation. For velocity mode, scale the velocities as a ramp from low (not too low) to high.
- Arm and play. For velocity mode, set the layer mode to auto velocity-split and reduce the velocity-to-amplitude amount so the softest layer is still audible.
- For repeated hits or rolls, instead record 8 hits at slightly different velocities (and random settings) and set the layer mode to round-robin.
- Add velocity to low-pass cutoff (floor about 1-1.5 kHz, harder hits open it) so soft hits sound softer even in round-robin mode. Optionally add start-time (pre-delay) jitter, a little under about 9 ms.
- Ensemble bounce: copy the MIDI to 4-5 synth instances with different pan (about 85 L/R and 46 L/R), randomness, pitch offset, snap frequency, decay and velocity curve. Sum them to one bus and capture that bus into the sampler the same way.
- Save the instrument with a clear name, for example 'big tom drum synth'.

### Make one synth epic-drum patch sound like an ensemble of drummers: copy it to about four instances on the same MIDI, give each a different global decay, snap-EQ frequency and pan (about ±40), and add per-note random envelope delay (about 0-22 ms, tighten to about 7 ms, too loose at 65 ms) so the hits flam naturally. Optionally drive a filter with a tempo-synced step sequencer for rhythmic patterns
Source: [Epic Drums 3 - Sound design tutorial](https://www.youtube.com/watch?v=ALHZHHPAdI0) · was `synth-drum-ensemble-four-instances-same-midi-per-hit-random-env-delay-0-22ms-decay-snap-eq-pan-plus-minus-40-step-seq-filter-rhythm`
- Add macros to the patch: global decay (amp-env and filter-env decay together), snap frequency (a peaking EQ band on the attack), global pitch in semitones (about ±4) and randomness depth.
- Add a per-note random modulator (new value on every MIDI note) on the amp-envelope delay and filter-envelope delay. Range about 0-22 ms at 50% randomness; 100% gives about 0-65 ms (too loose), and about 9% gives about 7 ms (tight).
- Write a simple pattern on instance 1, then duplicate the instance and its MIDI about three times.
- On each copy, move the macros differently: decay up or down, snap frequency up or down, randomness slightly different, small fixed pitch offset. Pan pairs about 39-40 left and right.
- Listen and tighten: if a layer is too loose, lower its randomness (for example 86 to 68, 90 to 60).
- Optional rhythmic variant: an arpeggiator on eighth notes or a tempo-synced step-sequencer LFO driving the filter cutoff range. Change the step pattern or rate (8 to 16 steps, double speed) for new grooves. Lengthen the attack to turn hits into reverse-drum or noise-sweep textures.

### Synthesize a whole drum kit (808, kick, clap, snare, closed and open hat) from a basic synth: sine and noise sources, envelope-drawn transients, fast pitch envelopes, and targeted EQ, then test and re-tweak each sound inside a real beat
Source: [The VITAL Drum Sound Design Tutorial!! (FREE PLUGIN)](https://www.youtube.com/watch?v=xlBInB7BOzE) · was `synth-drum-kit-from-scratch-808-sine-45hz-saw-noise-transient-gentle-20hz-hp-narrow-78hz-dip-kick-fast-pitch-env-clap-three-noise-bursts-1k-6k-snare-octave-sines-noise-hats-test-in-context`
- 808: sine osc tuned so the fundamental reads about 45 Hz on an analyser; add a saw and white noise whose levels follow a drawn envelope (quick dip at the start for a transient, then decay, about 1.6 s overall); low-pass the saw.
- 808 processing: small mid boost, soft distortion with modest drive, very gentle high-pass near 20 Hz (not steep), narrow bell cut around 78 Hz; optional parallel copy with reverb faded in, kept to the sides, then a limiter on the pair.
- Kick: sine pitched down an octave, very short amp envelope, a very fast envelope (about 0.07 s) routed to pitch, soft clip; then light bit-crush, multiband drive, a cut around 400 Hz for boxiness and a high-pass.
- Clap: white noise with a level envelope of three quick transients then one longer decay (grid of about 9 steps, about 0.085 s); band-pass it so energy sits above about 600 Hz with emphasis near 1 kHz and 6 kHz; add highs with bells not shelves and avoid much content above about 11 kHz.
- Clap finishing: a little chorus and very short delays for stereo, compression, then turn down side highs.
- Snare: two or three sines an octave apart (reference tones about 240 Hz, 484 Hz, 1 kHz), white noise with two quick transients, all through one filter; route a very short envelope to the pitch of every tone; add distortion; optionally layer the clap and blend.
- Closed hat: white noise with a very short envelope (about 0.22 s), filter to a tick, high-pass but keep some mids. Open hat: same noise, longer envelope with a second small transient, low-cut reverb and a 1/64 ping-pong delay, then shorten the decay.
- Render all pieces, build a short beat, and adjust each sound in context (EQ, decay, pitch shift a few semitones and re-export) until they sit together.
