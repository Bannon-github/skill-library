# Transition FX: risers, downlifters, whooshes, impacts, braams and Shepard tones

Goal: Design transition sounds: noise risers with BP/HP sweeps, pitch-ramp and FM uplifters, downlifters, doppler whooshes, synthesized impacts with tails, braams, Shepard endless risers and one-bar mod-envelope transitions.

**Theory:** Rising pitch, rising filter cutoff, rising volume and increasing density all signal tension; resolution is a downbeat impact. Shepard tones use octave-spaced partials under a fixed spectral window -> endless rise.

**Hear it:** `sample-lab/theory/risers_transitions.py`

## Workflow
1. Length: riser = 2-8 bars ending exactly on the downbeat; downlifter = 1-2 bars after it.
2. Noise riser: white noise -> BP/HP swept 300 Hz -> 9 kHz, volume curve exponential, resonance for whistle, LFO rate speeding up.
3. Pitch riser: synth pitch +12 to +24 st ramp, FM index up, reverb send rising; downlifter = reverse or pitch down.
4. Impact: noise burst + sine sub drop (80 -> 20 Hz) + long reverb tail shaped by LFO; braam = detuned saws + sine sub with pitch curve and formant.
5. Shepard riser for endless tension under builds.
6. Mix: duck the reverb tail, keep riser out of the vocal band peak, cut it 1 beat before the drop for contrast.
7. Hear the theory: run `/home/box/audio-tools/bin/python sample-lab/theory/risers_transitions.py` from the repo root and compare the sections; reuse its functions as a starting point for renders.

## Source techniques (merged, numbers kept)

### Cinematic braam: sine sub + two light-unison saws, curved pitch envelope, swept formant layer
Source: [Vital Sound Design: Build Cinematic Braams from Scratch](https://www.youtube.com/watch?v=iBA0P7MTUEc) · was `cinematic-braam-sine-sub-dual-saw-pitch-curve-formant`
- Start from an init patch. Osc 1: basic sine, phase randomization 0, transpose −1 octave (the sub/body).
- Osc 2: saw, phase randomization 0, 3 unison voices, unison detune ~10%; apply a formant/spectral scale warp around ~36% and give it a small random-modulator amount for drift.
- Osc 3: saw, phase randomization 0, 3 voices, detune ~10 (no warp).
- Route osc 1–3 into Filter 1 (low-pass style): lower the resonance/peak slightly, cutoff around the lower third of the range (~35 on a 0–127-ish scale), and add a random modulator to cutoff at a small amount.
- Filter 2: formant type (A-O-I-E vowel), formant position 0, mix 0. Shape LFO 2 as a single rise, set it to one-shot/envelope mode at ~4 bars (4/1), and route it to Filter 2 mix so the vowel character fades in over the hit.
- LFO 1: draw a custom multi-point curve (low start, quick rise, dip, rise at end) with curved segments; envelope mode, 4/1 length. Route LFO 1 → global pitch transpose at a small amount (~5 in the source's units).
- FX order: distortion first (soft clip, ~10 dB drive) → EQ with high-pass on → FX filter with resonance 0 and cutoff low, LFO 1 opening that cutoff → reverb with its low-cut raised high (the source slides the band to ~102 semitones), time ~2.3 s, size ~40%, mix ~74% → multiband compressor with upper band pushed (~18 dB).
- After the synth: a utility set to mono everything below ~120 Hz, then also send the track to the shared reverb send channel.

### FM/operator-stack uplifter with long pitch envelope and synced noise swell
Source: [FM8 - FX Sounds - pt 1 - Uplifter - How To Tutorial](https://www.youtube.com/watch?v=G4Tc59aAeoE) · was `fm-stack-uplifter-pitch-env-noise-swell`
- Carrier/low layer: one operator to output at full level, ratio ~0.25, formant-ish wave (transcript: 3rd formant) for a low body.
- Add a raspy modulator into that carrier (~28 depth) with self-feedback on both (~5 on the mod, ~32 on the carrier); set mod ratio ~0.5 with a higher formant wave (transcript: 8th formant).
- Bright layers to output: triangle at ratio 4 and a square-ish (1+3+5) at ratio 1, each ~88 level, with some self-feedback on the triangle (~16).
- Distort a mid operator with two further ops (triangle at ratio ~1.25 into it ~54; saw-ish 1+2+3 at ratio 0.25 into that modulator) for a slight chord/cluster rasp.
- Master: monophonic, 2 voices, detune off, light pan (~25–26%) between voices; add mild bit-crush/digital (~65) for FX character.
- Envelopes: tempo-sync; give some operators a slow reverse/fade-in looped sustain shape (e.g. over 3/16) and others a stabby attack with sustain loop so layers move against each other.
- Pitch envelope: tempo-sync a long rising sustain envelope across ~8 bars (~31–32/4), amount ~54, slightly curved for a smoother bend; hold MIDI at a sustained note (e.g. C3).
- Noise operator to output (~58) with amp up, bright cutoff, mild resonance (~55–57); FM-noise into several tonal ops (e.g. ~50/30/16). Save/load the same rising pitch envelope onto the noise amp so noise and its FM distortion swell with the rise. EQ low-mids/highs; reverb ~33–34% wet.

### Build whooshes from noise and synth layers: bus envelope + Doppler pass-by, rising-only variant, and mod-wheel performable whoosh
Source: [How to design 'Whoosh' sound effects [EASY]](https://www.youtube.com/watch?v=uFk9xUVg7Q0) · was `noise-layer-whoosh-doppler-and-rising-variants`
- Generate steady white noise and record/print it to audio so the generator is not running constantly.
- Add texture layers (e.g. a cymbal/metal tail, heavy wind) and route all layers to one whoosh bus.
- Draw a volume envelope on the bus that swells in and back out to give the basic 'wash'.
- Add a Doppler-style pass-by: set where the action starts, where it ends, and the centre/listener point where the pass is heard; attenuate the pitch change if it is too big and move the transition/listener points to taste. Portable alias: pitch up-then-down curve + level peak at the centre + pan sweep.
- Vary the character by muting/swapping layers: drop the metal layer for a more airy result; swap white for pink noise, low wind for higher wind, add rain for whiter noise.
- Compress the bus (a whoosh should not be in your face) and add a limiter with a ceiling around -0.2 dB.
- Add a synth layer: render one or two notes of a noisy/FX patch, high-pass/cut the excess low frequencies, and send it to the whoosh bus.
- For longer actions, stretch the Doppler start/end across the longer selection and increase pitch for a stronger transition; add reverb on an FX return.
- Rising-only whoosh (Doppler always goes up then down): use a pitch-shift effect with an upward curve, reduce the range, start lower, pick a smoother algorithm; also set a narrow EQ band very low and automate its frequency sweeping upward (reduce gain if too strong); time-stretch faster/slower with a tape-style algorithm, then add reverb.
- Performable synth whoosh: map one mod wheel/macro to open the filter, raise the white-noise amount and raise a flanger's wet mix together; play the whoosh live to any length - no stretching artifacts, and the flanger keeps the sustained top moving so it is not annoying.

### One-bar transition FX built on a single mod-envelope 'timeline': a rising curve with an end drop drives noise level, full left-to-right pan and a resonant driven filter; an octave-down detuned unison saw on its own amp; a second up-and-down triangle envelope on oscillator sync (~50%); multiband mid distortion; master delay then a sidechain-ducked reverb that blooms after the riser cuts
Source: [How to Create Epic Sound FX and Risers That Transform Your Tracks | 100 Sound Design Tips Ep. 13](https://www.youtube.com/watch?v=Q_0QcuRePZ0) · was `one-bar-transition-riser-mod-envelope-timeline-atomized-targets-triangle-sync-ducked-reverb-tail`
- Pick the length (usually one bar). Draw mod envelope 1: start at the bottom at 0, rise to the top at the bar end (4 beats), then add a steep drop back to 0.
- Noise: oscillator gain at 0, noise level 0, mod envelope 1 → noise level with depth for loudness. Bend the curve for more impact; add a compressor or amp gain if it is too quiet.
- Pan: set noise pan hard left and modulate it 100% with the same envelope (unipolar), so it travels left to right.
- Filter: bright filter with some resonance and drive, cutoff modulated by the same envelope; add a little release.
- Second voice: a saw an octave down with unison and detune on a separate amp and FX bus. Its amp level starts at 0 and is modulated by envelope 1.
- Draw mod envelope 2 as a triangle over the same bar (up to the top then back down) and route it to oscillator sync (~50%). Try curve variants (fast-in or slow-drop before the downbeat).
- On the second voice's FX bus, modulate a multiband distortion's mid drive with envelope 1.
- Master tails after distortion: delay (lows and highs cut, more mix), then reverb with decay below ~70% and sidechain ducking so it stays down while the riser plays and blooms after it cuts. Optional: stutter FX between delay and reverb, a master filter sweep on envelope 1, bar-length macros (4/2/½ bars). Place a low impact/kick on the downbeat.

### Synth-built pitch riser: 2-octave bend ramp with reset points, smeared by a resonant diffusion filter and reverb
Source: [Serum Tutorial - How To Make Risers](https://www.youtube.com/watch?v=9v-p2k8Nnec) · was `pitch-ramp-riser-resonant-smear-filter-reverb`
- Start with a single oscillator on a saw wave (choose the tone you want); turn effects off while setting up.
- Set the pitch-bend range to 12 semitones so a full bend travels from -1 octave to +1 octave (two octaves total) - the bend range defines the distance the riser travels.
- Automate pitch bend as one ramp across the entire clip, starting exactly at the bottom (-1 oct) and ending exactly at the top (+1 oct). Add small reset points at the clip start and end that return bend to 0, so playback started partway through does not begin with a mangled/latched pitch.
- Recognise the problem: a constantly moving pitch only lands on an in-key note for a split second, so if the pitch is clearly discernible it makes the track sound sour - so smear it.
- Insert a phase-smearing resonant filter (source: a 'reverb'-type filter; portable alias: short comb/allpass diffusion filter). Set cutoff LOW with HIGH resonance - set high it affects too little of the sound; low with high resonance it blurs where the pitch was into where it is.
- Add an LFO for very slight, slow movement of that filter: with no movement it does not smudge, with too much movement the effect is lost.
- Add reverb afterwards to smear further (its micro-delays carry the pitch just passed into the current pitch).
- Optional finishing (not vital to the sound): sidechain compression, basic EQ, auto-pan pumping.

### Section transition toolkit: layered risers and impacts, throwing a part to a growing delay, a next-section instrument entering early, stacked exponential automation, resampled or reverse-reverb whooshes, removing elements or silence, and transitions that cross or hang over the bar line
Source: [25 song transition tips I wish I learned from the start](https://www.youtube.com/watch?v=lnJA5rOrp-M) · was `section-transition-toolkit-layered-risers-downlifters-impacts-throw-to-delay-early-pickup-stacked-exponential-automation-resampled-whooshes-reverse-reverb-removal-silence-across-barline-hangover`
- Pick 1-3 riser, whoosh or downlifter layers sized to the intensity; synthesize at least one (e.g. noise or saw with pitch and filter rising) so length and range fit the boundary. A smaller 'transition to the transition' can lead into a bigger swell.
- Put an impact on the landing downbeat: a crash, or any noisy hit sent into a big reverb.
- Throw a lead or vocal to a delay over the last bars: delay mix automated 0 to 100%, feedback rising, a resonant filter sweeping and blending in; optionally add upward multiband compression on the throw.
- Bring one instrument from the next section in early with a short pickup phrase.
- Stack automations together: drive on bass, shaper on drums, width, delay or grain mix, filter cutoff, envelope decay/release from short to ringing; compensate with output gain. Build the end sound first, then automate toward it.
- Shape every curve: exponential (default), hold-then-ramp, turn back at the end, or slam to full then recede.
- Resample parts of the track through effects, then time-stretch and pitch-automate them into custom whooshes and risers; or duplicate a part to a 100%-wet reverb, print it and reverse it into the hit; or chop audio for a stutter transition.
- Remove elements: cut drums, bass or atmosphere before the new entries, or insert a short silence before the downbeat.
- Work across the bar line: drop some instruments for the first beat of the new section, or let a delay or reverb tail hang over and fade under the new section.
- Combine 2-4 of the above per boundary, scaled to the intensity.

### Shepard-tone endless riser from three mono pitch-bent voices (plus rising noise-filter variant)
Source: [Shepard Tone Tutorial - How to Create INFINITE Risers!](https://www.youtube.com/watch?v=YvUbr8GaqUo) · was `shepard-tone-endless-riser-octave-crossfade-voices`
- Understand the illusion: several copies of the same rising line spaced apart in pitch play together; the lowest copy fades in while the highest fades out, so the ear hears a constant rise.
- Pick any synth where you can set the pitch-bend range and set it to a whole number of octaves (e.g. 12 semitones down and 12 up = a 2-octave sweep).
- Draw one long sustained note across the whole clip and automate pitch bend from its minimum to its maximum exactly over the clip length, so it loops straight from bottom back to bottom.
- Duplicate to three voices (high, mid, low). Transpose the high voice up by the sweep span (+2 octaves here) and the low voice down by the same span, so each voice's end pitch equals the next voice's start pitch.
- Set every voice to monophonic (1 voice) so any release tail does not overlap and audibly fade out when the loop restarts.
- Add volume automation: high voice 100% -> 0% across the clip, low voice 0% -> 100%, mid voice constant. Program the start/end points exactly at the clip boundaries.
- Group the voices and put reverb on the group: it sits the riser back as a background effect and smooths the small click at pitch reset.
- Noise/filter variant: white noise -> a resonant flanging/comb-style filter with many notches; replace the pitch ramp with a rising ramp LFO (retriggered, one ramp per 4 bars) on cutoff.
- Make it endless: use four copies; give each a volume fade-in over the first 25% and fade-out over the last 25% of the clip, then duplicate the copies so they overlap and enter in turn (stagger is approximate from transcript).

### Synthesize a cinematic hit tail from white noise (LFO-shaped level, low boost, shared-LFO drive, Haas stereo, dark reverb)
Source: [Sound Design Tutorial: Synthesizing Tails for Cinematic Hits & Impacts](https://www.youtube.com/watch?v=q-N55tqLUr4) · was `synthesized-noise-impact-tail-lfo-shaped`
- Audition the hit layers (pre-wash, sub, punch) together and note the missing body/tail.
- Init a synth: disable oscillator 1 and enable only white noise (any white-noise generator or sample works).
- Shape the noise volume over time with an LFO used as a one-shot level contour (or the main amp envelope) so it swells/decays like a tail.
- Drastically reshape the spectrum: filter to boost the lows a lot and cut the highs; make the bigger changes with EQ.
- Add distortion and modulate its amount with the same LFO so drive follows the volume movement.
- Add a multiband compressor; modulate its mix (and its high band) with the same LFO so it is not boosting the whole time.
- Make it stereo: delay in stereo mode, time in seconds/ms, both at the shortest setting, then delay only one of the two sides; feedback 0, mix 100%.
- Add reverb as the last step, cut the reverb's highs, and mix to taste.
- Play with the other hit layers, compress/raise the tail, EQ further if needed, and add gentle compression on the group of all elements (back off if too much).

### Uplifter / downlifter from any saw synth: pitch-bend span, closed LP, accelerating LFO
Source: [HOW TO MAKE UPLIFTERS & DOWNLIFTERS IN SERUM!!!](https://www.youtube.com/watch?v=t97TU3p7-kE) · was `uplifter-downlifter-pitchbend-filter-lfo`
- In the piano roll, draw a single root-note held for about 8 bars so the riser sits in key for a buildup.
- Set pitch-bend range to 6 or 12 semitones up and down (12 used in the transcript).
- Enable a low-pass filter (e.g. MG-style 12 dB) and pull cutoff down so highs are removed at the start.
- Map an LFO to cutoff. Draw an accelerating rate curve in the LFO (start slower ~1/4, then 1/8, then 1/16) and adjust LFO rate to taste.
- Map the same (or a second) LFO/envelope to pitch-bend position: from 50% toward 100% for an uplifter, or from 50% toward 0% for a downlifter.
- On a saw source, raise unison (e.g. ~7 voices), reduce detune for a tighter supersaw, and raise stereo blend slightly.
- Sidechain the riser to the kick (or a rhythmic duck envelope), easing mix if the duck is harsh (~75% wet in the transcript example). Add reverb/FX from the synth FX rack or inserts so it sits in the mix.

### Cinematic whoosh-hit: layer sub-whoosh, whoosh and three hit layers, edit the whoosh quieter than the hit and tighten the flam, resample at milestones, dark dual reverbs, upward/parallel compression, clipping, sub removed from the whoosh only, multiband then true-peak limiting
Source: [Sound Design Tutorial: Cinematic Whoosh hit](https://www.youtube.com/watch?v=3rCUdTDodrc) · was `whoosh-into-hit-layer-resample-chain`
- Layer: a sub layer made from the reversed tail of a sub kick, a resonant whoosh layer (e.g. noise or foley swept past a resonant body), and three short hit layers lightly pitched down, each with a small whoosh into a clean transient and a tail.
- Resample the sum at the first milestone and keep the original; work on a duplicate.
- Edit without plugins: chop the whoosh and lower its level below the hit; trim the hit layers so the transients flam only slightly (a small flam lengthens the body, too much sounds messy).
- Resample again, add gentle tape saturation to glue the layers.
- Send to two dark reverbs on returns: a room with about 2.75 s decay and a low filter, and a plate with about 3.6 s decay low-passed around 1.4 kHz; sum dry and reverbs into one bus.
- On the bus: tame the high-end noise in the tail after the transient (adaptive denoise or a dynamic high-shelf cut that acts after the hit), then two upward/downward multiband compressors in series at low mix, then aggressive parallel compression at 50% wet.
- Clip the peak hard (about 6 dB of clipping) to square off and prolong the transient, then limit lightly. Resample (milestone 3).
- Final pass: re-edit any unwanted whoosh section with fades; high-pass only the whoosh portion at about 60 Hz; a few EQ notches/boosts by ear; light clipping (~1.5 dB); a multiband limiter (lowest band ~0-100 Hz) with some transient emphasis; then a true-peak limiter as a safety net.

### Organic build-up tension without riser samples: one oscillator of the main riff slowly ramps up in pitch, an irregular-length loop of the vocal (or lead) with chorus gets pitch-shifted up over the build, and a fully fed 1/8 delay return is revealed by return-volume automation with rising feedback, all ducked under the dry part
Source: [How The Pros Build Tension (Without FX Samples)](https://www.youtube.com/watch?v=Pp88aLB3LpE) · was `organic-tension-from-track-sounds`
- Riff riser: on the riff synth, automate only one oscillator's pitch to glide gradually upward across the build while the other oscillator and the notes stay in tune.
- Irregular loop: load the vocal (or lead) into a sampler and loop a section whose length is not tied to the tempo; add a wide chorus.
- Automate that loop's volume and EQ to bring it in over the build; sidechain it lightly to the dry vocal so the main part stays clear.
- Pitch-shift the loop up gradually across the build with automation (a slow, steady upward shift).
- Send the vocal group to a return with a 1/8-note delay at 100% wet; set the send to full and leave it; automate the return's fader instead, revealing it only for the swell.
- Automate the delay feedback to ramp up slowly through the build (moderate maximum), lightly sidechain the echoes to the dry vocal, and fade the return to zero right before the drop.
