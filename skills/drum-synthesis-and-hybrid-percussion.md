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

### Atmospheric liquid DnB break: 4-bar two-step kick/snare loop with the second kick quieter, kick EQ by dipping mids (not boosting lows/highs), one-shots tightened by shortening decay, a high-passed sliced break and percussive tops grouped and ducked to kick/snare, transient shaper + low-cut on tops, light glue compression into a soft clipper, and a very short no-pre-delay drum room
Source: [How to make Atmospheric Liquid DNB Drums Step by Step [Beginner Tutorial]](https://www.youtube.com/watch?v=xeuYUFZpOdA) · was `atmospheric-liquid-dnb-break-layering`
- Program a 4-bar two-step kick/snare loop; lower the second kick in each bar slightly so beat 1 is the strongest hit.
- EQ the kick by dipping the mids (focuses the low and top without boosting), tame its top a little, and cut any low noise bump.
- Tighten percussive one-shots and the shaker by pitching where useful and shortening their decay (one-shot/gate mode), since reverb is added later.
- Bring in a break: tighten its decay, slice it, rearrange slices to fit the kick/snare rhythm, and high-pass it so it only adds top-end movement.
- Group all top elements (break, percs, shaker). Duck the group on kick and snare (utility gain automation or sidechain) so tops never clash with the focal transients.
- On the tops group: a transient shaper, then an EQ that removes any low bleed and rolls off harsh highs.
- Drum bus: glue compressor with light compression and soft clip on, driving into the clipper so no spiky transient peaks too hard; then balance kick, snare and tops (levels change the compression).
- Send to a very short drum-room reverb with no pre-delay and short decay.

### Dark, short house kick that sits behind a busy bassline: think in transient / body / tail, keep the transient dark (not clicky), start the body pitch near 73 Hz and fall to the sub, cut the tail to an eighth (or sixteenth) note, tune to the key, layer only what's missing, and mix the kick a few dB lower than the bass
Source: [Disclosure's Signature Kick (How To Make It & Why It Sounds So Good)](https://www.youtube.com/watch?v=N60Jcn9zfBo) · was `dark-short-kick-behind-busy-bass-transient-body-tail-73hz-start-eighth-note-length`
- Split the kick into three parts: transient (the tiny start), body (the chest punch) and tail (the sub). Judge and fix each part separately.
- Synthesize the kick: a sine body tuned to the song key, with a pitch envelope starting higher, around 73 Hz, and falling to a lower sub note. Add a short pitch-envelope punch (around 100 Hz) for pop if needed.
- Keep the transient dark: low-pass or choose a soft attack rather than a bright click.
- Set decay so the whole kick lasts about an eighth note (sometimes a sixteenth) at the song tempo, leaving space for the bassline.
- Layer only if something is missing: e.g. a sub layer for the felt low end, a body layer with its sub removed for punch, and a quiet top layer. Check for phase issues after layering.
- Mix the kick a few dB lower than a typical melodic-house kick so the bass is the focus, with the kick still audible.
- Make a frequency guide from reference records: compare the kick and sub curve on an analyser and EQ the kick (e.g. trim excess around 50 Hz or deep sub) toward the reference.

### Reverb/rumble kick: feed a kick into three parallel returns (New York compression with release between a 1/16 and 1/8 note at the tempo, a 100% wet drive, and a 100% wet short, high-cut reverb), duck the reverb return with a sidechain compressor keyed by the kick, then low-pass the tail with a tempo-synced LFO and finish with a low-end enhancer
Source: [Music Production Tips and Tricks - Making a Techno Reverb Kick](https://www.youtube.com/watch?v=q6TxzspNL9Q) · was `reverb-rumble-kick-parallel-aux-ny-comp-release-between-16th-8th-drive-short-verb-ducked-by-kick-synced-lowpass`
- Program a 4/4 kick; lower velocity on the weak beats (~80) and the medium beat (~90). Pull the kick level down to leave headroom.
- Return A: compressor (sidechain EQ letting only lows trigger), threshold low, high ratio for ~10 dB gain reduction, fast-ish attack that still lets the transient through, release between a 1/16 and 1/8 note. Add EQ low and high shelf boosts after it. Blend under the dry kick.
- Return B: a drive/distortion at 100% wet, amount low (below ~20%), letting lows through.
- Return C: reverb at 100% wet, small size, high cut on, decay turned up so it rattles.
- Put a compressor after the reverb with external sidechain from the kick; set release to control how long the rumble swells back between hits.
- Add a low-pass filter after that to remove high frequencies; modulate cutoff with an LFO synced between 1/8 and 1/16, then optionally a slow LFO on cutoff with low depth for long-term movement.
- Optionally send some reverb into the drive return, then put a low-end enhancer/drum-bus device on the kick for sub weight with light drive.

### Kick 'heart' sweep rules: a pitch-swept sine whose sweep time is just right (too short = disconnected click, too long = laser), whose decay leaves silence for the bass, whose start frequency stays modest and whose end frequency is set against a ~55 Hz reference; keep the heart clean, then add saturation in parallel and an optional layered transient
Source: [How to not screw up your kickdrums!](https://www.youtube.com/watch?v=0IgwdHg0ZwM) · was `kick-heart-sine-sweep-goldilocks-sweep-time-not-clicky-not-laser-decay-leaves-silence-for-bass-low-start-freq-55hz-end-reference-clean-heart-parallel-saturation-layered-transient`
- Start from a plain sine oscillator with a pitch envelope rather than a 909-style preset, and watch it on a spectrum analyser.
- Set the amp decay so the kick thumps but leaves some silence before the next hit at your tempo, the space where the bassline or rumble will sit.
- Adjust the sweep time (time to reach the resting frequency) by ear. If you hear a mid click and a separate sub tone, lengthen it. If it sounds like a 'pew' laser, shorten it. Stop where it feels like one connected knock.
- Set the start frequency only as high as needed; very high starts (toward 5 kHz) don't add bang. Leave the brightness to saturation and layers, then re-check sweep and decay.
- Set the end (resting) frequency, i.e. the perceived kick pitch. Use ~55 Hz (909 reference) as a starting point, go a little lower for a modern feel, and check it is still audible on small speakers.
- Blend saturation in parallel (not hard in series) to add harmonics, keeping the clean heart intact.
- Optionally layer a short transient/top sample so the ear has something up to ~9-10 kHz in a busy mix. Balance levels so the thump stays dominant. Then keep refining end frequency and decay against the full mix.

### Acoustic-sounding punchy kick from one three-oscillator synth: sine body with level and pitch envelopes, a tiny high-pitched transient oscillator offset in phase, a one-shot acoustic sample layer faded in after the transient and high-passed, and a short quiet pink-noise tail, then low/mid EQ and fast-attack compression
Source: [Make Acoustic-Sounding Kick Drums in Serum 2 (Realistic & Punchy)](https://www.youtube.com/watch?v=oRhBZ6L9rU8) · was `acoustic-style-kick-four-layers-sine-body-pitch-env-phase-offset-transient-osc-faded-in-sample-layer-hp-filtered-short-pink-noise-tail`
- Osc A body: basic sine, random phase 0, phase 90. Assign envelope 1 to level with a short body decay; assign envelope 2 bipolar to coarse pitch at about +12 to +24 st with a fast drop; tune down a couple of semitones for weight.
- Osc B transient: same sine, random phase 0, phase about 95 so the two oscillators do not line up; a very short level envelope, the same pitch-envelope source tuned very high, and the shortest envelope you can draw.
- Osc C texture: one-shot acoustic kick sample. Pick a pleasing scan/start point, give it a level envelope with a short fade-in so its attack is skipped, and route it alone through a high-pass filter to roll off its lows.
- Balance the layers: bring the sample layer down until the kick sounds clean, then retune the body pitch and reshape body/transient envelopes to taste (higher body = thumpier).
- Noise tail: short envelope on a pink stereo noise oscillator, low level and short decay, like a faint top on the hit.
- FX: EQ boost on the lows (raise Q a little) and on the top/mids; single-band compressor with fast attack at about half amount, then make up gain.

### Punchy, deep kick in one synth tuned to the track's root: sine sub, hold+decay amp envelope, a unipolar pitch envelope that falls onto the note, the same envelope on a driven low-pass, a low-level one-shot noise attack, then EQ / transient / compression shaping
Source: [Make Your Own Kick Drums - Punchy and Deep Kicks](https://www.youtube.com/watch?v=JhZU6JGvoHw) · was `punchy-deep-kick-tuned-to-track-root-sine-sub-hold-decay-unipolar-pitch-env-driven-lp-filter-env-noise-attack-eq-transient-compression`
- Init the synth; set oscillator quality to max and voice mode to mono (no overlapping kicks).
- Osc 1 = sine, transposed down 2 octaves; play the track's root (e.g. F#) so the kick is tuned to the song's fundamental.
- Amp envelope: attack 0, hold ~100 ms, decay ~100 ms, sustain -inf. Adjust hold/decay for length; extend the MIDI note so it doesn't cut the tail.
- Envelope 2 (attack 0, short decay, sustain 0) -> osc coarse pitch, set unipolar so it starts high and falls onto the note; steepen the curve. Less amount/slower = more body; more/faster = more attack and pitchiness.
- Route the same envelope (unipolar) to a low-pass cutoff so mids/highs sweep away quickly; lower master level and drive the filter for extra harmonics.
- Add a noise oscillator in one-shot mode (an attack/kick-noise sample, or a layered click sample if the synth has no noise) through the filter; raise it only until the start feels consistent.
- Play against snare and hats; fine-tune hold, decay and pitch-envelope amount so the kick fits the groove.
- Mixer: boost low end if needed, cut around 300-400 Hz to clear mud, optional high boost for more attack.
- Optional light overdrive/clipping for grit; transient shaper attack up/down to dial the click.
- Compress the kick fairly hard with make-up gain: slower attack keeps the transient, faster attack trades click for fatness. Check on speakers and headphones.

### Soft/felt-to-punchy kick dial: treat the kick as attack + tone, set character with pitch-envelope amount x time, then soften the body and give the attack its own blendable layer (short pitch-dropped saw or short band-passed noise)
Source: [How To Kick (a discussion of kick drum synthesis)](https://www.youtube.com/watch?v=8eAQ0VdW0Cw) · was `soft-felt-to-punchy-kick-dial-attack-vs-tone-pitch-env-amount-x-time-separate-attack-layer-saw-or-bandpass-noise-fm-body`
- Layer 1 only: sine body, linear or exponential attack-decay envelope, short decay, pitched low. Note a near-zero amp attack already gives an implied click.
- Add a pitch envelope (attack-decay) to layer 1 and sweep its amount and time: large + slow = tom/zap, large + very fast = a click, moderate = punch. Pick the balance for the target character.
- Soft/felt: lower the amount, slow the drop (40-80 ms, ours), soften the amp attack (2-5 ms, ours) and shorten the decay so the front is no longer clicky.
- Layer 2 attack option A: sawtooth with a high, very fast pitch drop and a very short decay; set its level and tone independently of the body (pitch higher = pingier, lower = scratchier).
- Layer 2 attack option B: band-passed noise with a very short decay; the noise 'pitch' moves the band centre. Works best when the body is short too.
- Optionally combine A on layer 1's pitch drop with B noise on layer 2 for a classic sine kick plus noise punch.
- Optional colour: swap the body to fast FM, or add gentle drive / wavefold / bit reduction for higher harmonics.

### Kick punch by compression: threshold catches only the upper part of the kick, 3:1 ratio, slow ~40 ms attack lets the transient through, ~200 ms release returns before the tail sinks, then make-up gain so the transient stands taller than the sloped tail
Source: [How to add PUNCH to your KICKS using Compression (3 SIMPLE STEPS)](https://www.youtube.com/watch?v=mxUQyUs1eGo) · was `kick-punch-compression-threshold-on-top-section-3-to-1-slow-40ms-attack-keeps-transient-200ms-release-makeup-gain`
- Solo the kick in a basic loop; note the dry waveform (small transient, flat body).
- Lower the threshold until only the upper section of each kick crosses it (about -10.5 dB in the source).
- Set ratio about 3:1 (2-3:1 moderate, 5:1 strong, 10:1+ acts like a limiter).
- Raise attack to about 40 ms so the initial transient passes before gain reduction starts.
- Set release about 200 ms so it affects only the upper section and recovers before the next hit.
- Add make-up gain (~+2.3 dB) and A/B against the dry kick at equal loudness; compare waveforms.
