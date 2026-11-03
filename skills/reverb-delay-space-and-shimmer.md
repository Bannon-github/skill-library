# Reverb, delay, shimmer and freeze: creating depth and space

Goal: Place sounds in space with sends: choose reverb type, pre-delay and low-cut, tempo-synced and ping-pong delays, distorted/band-limited delay throws, shimmer (+12 pitch in feedback), reverb freeze/reverse swells and fully-wet extreme reverb pads.

**Theory:** Wet/dry ratio and pre-delay set perceived distance; early reflections give size; high-damping and low-cut on returns keep lows clean. Feedback < 1 decays; ~0.99 sustains (self-sustaining pad); pitch shift in the loop climbs octaves (shimmer).

**Hear it:** `sample-lab/theory/reverb_delay_space.py`

## Workflow
1. Use sends/returns, not inserts, for shared space; one short room (0.5-1 s) and one long hall/plate (2-5 s).
2. Set pre-delay 10-40 ms to keep the dry attack clear; low-cut return 150-300 Hz, high-cut 6-10 kHz for darker depth.
3. Delay: tempo-sync (1/4, dotted 1/8, 1/8T), feedback 30-50%, ping-pong for width; band-limit (HP 300 / LP 4 kHz) and optionally saturate the return for 'throws'.
4. Narrow a reverb to mono before a ping-pong delay to create focused 'pockets' instead of wash.
5. Shimmer: pitch-shift +12 st inside the reverb/delay feedback, mix 10-30%; self-sustaining pad: few notes into a ~99% feedback asymmetric stereo delay (e.g. 1 s L / 150 ms R).
6. Freeze/print: freeze a reverb tail or print it, reverse it for swells into downbeats, or loop it seamlessly as an atmos layer.
7. Extreme pad: send percussive sources (piano, vibes, glock) 100% wet into 20-40 s chained reverbs; bitcrush or brighten before the reverb; EQ the bus and sidechain it lightly.
8. Duck reverb returns to the dry source or kick if the mix gets washy.
9. Hear the theory: run `/home/box/audio-tools/bin/python sample-lab/theory/reverb_delay_space.py` from the repo root and compare the sections; reuse its functions as a starting point for renders.

## Source techniques (merged, numbers kept)

### Distorted-delay return: drive → ping-pong delay on a 100%-wet send, both band-limited to high mids, return pre-attenuated, played by riding the send
Source: [Ableton Sound Design Tutorial - Distorted Delays](https://www.youtube.com/watch?v=4fpZFYG83fw) · was `distorted-delay-return-bandlimited-send-throws`
- Create a spare return. Insert overdrive then delay (ping-pong).
- Set the overdrive's pre-filter to the high mids only, and do the same on the delay's filter so only that band is delayed.
- Delay: ping-pong for width, feedback ~56%; both devices 100% wet so only effect signal returns.
- Turn the send to maximum and dial drive and tone to the desired timbre.
- Pull the return fader down (~−6 dB start) so maxed sends never produce super-loud output.
- Perform: jam the send knob live to feel where echoes should happen, then tidy or draw send automation per note (some full, some partial).
- Check in context with the full track and adjust.

### Turn bright percussive or decaying instruments (electric piano, vibraphone, piano, glockenspiel) into an evolving ambient pad by running each through 100% wet reverbs of about 20-40 s (chaining two reverbs for longer tails), bit-crushing the piano before the reverb to sustain and add harmonics, taming harsh highs with EQ, then busing the layers with a low cut, compression, sidechain and a filter that reveals the pad
Source: [How to make an ambient pad in Logic Pro X - Trance Production Tutorials #10](https://www.youtube.com/watch?v=mnledZoD4QE) · was `fully-wet-extreme-reverb-pad-from-percussive-sources-20-40s-chained-reverbs-bitcrush-pre-reverb-for-sustained-harmonics-eq-tame-layered-epiano-vibes-piano-glock-bus-low-cut-sidechain-filter-reveal`
- Program a couple of chords stacked across several octaves; load bright sources (distorted electric piano, vibraphone, piano, glockenspiel) on separate tracks, panning a few slightly left or right.
- On the electric piano, insert a reverb at 100% wet / 0% dry with about 33 s decay.
- On the vibraphone, daisy-chain two algorithmic reverbs (fully wet) for an even longer tail; turn the track down.
- On the piano, insert bit crusher → EQ → reverb (fully wet, about 22 s); crush fairly hard to sustain and add harmonics, then cut the harsh upper-mid/top with EQ.
- On the glockenspiel, roll off some of the top with EQ before a fully wet reverb of about 40 s (chained reverbs).
- Listen to all layers together: different decays give multiple attack phases that morph over time.
- Route all layers to a bus: EQ out the low/sub build-up, add compression and sidechain compression, and a low-pass filter.
- Automate the bus filter open to introduce the pad in the arrangement.

### Mono (narrowed) reverb as a mixing and sound-design tool: narrow each 100%-wet reverb into a placeable 'pocket', pan pockets to separate parts, put a stereo ping-pong delay after the width stage so the pocket travels left-right, use the wet/dry mix as a distance control, filter the reverb tail post-reverb with an LFO-moved bandpass, and split dry left / mono reverb right for pseudo-stereo
Source: [STOP Using Stereo Reverb (Do This Instead) (Dub Techno Tutorial Mixing)](https://www.youtube.com/watch?v=e1AMHtuuuTQ) · was `mono-reverb-pockets-narrow-width-before-pingpong-wet-dry-as-distance-post-reverb-bandpass-lfo-dry-left-reverb-right`
- Solo through the parts and decide which stays stereo (e.g. an atmos bed with high-end detail through a moving notch filter into a 100% wet reverb) and which become mono/narrow pockets.
- For a pocket track, set its reverb 100% wet (on the insert) and narrow its width with a side-reducing imager or width utility, partly or fully.
- Pan each pocket to its own spot (e.g. short step pocket right, layered second step slightly wider and left, main part centre) and turn levels down: narrow reverbs are more audible, so they need less.
- Put the ping-pong delay after the width stage, with low feedback and a lowpass on the feedback, so the mono pocket is carried left and right.
- Use the reverb mix as a distance control: fully wet = far behind, fully dry = right in front. Shave highs for extra depth.
- Place a bandpass filter after the reverb and move it back and forth by hand or with an LFO; use the filter's mix to keep some high end. Post-reverb filtering shapes the tail as its own sound.
- Pseudo-stereo: send the sound to a mono reverb return, pan the dry sound hard left and the reverb hard right, then route both to a bus with a driven, resonant filter (cut lows, shorten the reverb, add movement).
- For a background wall: put a fully wet mono reverb on the atmos track and sidechain it to the lead or kick so it ducks out of the way.

### Reverb-freeze atmosphere print: freeze a 100%-wet reverb of a synth phrase, record it to audio, loop it seamlessly with overlapping tail, bus and process as an atmos layer
Source: [Trance Atmosphere Tutorial using Reverb Freeze 🥶](https://www.youtube.com/watch?v=-oFbaWsScJw) · was `reverb-freeze-print-seamless-loop-atmos-layer`
- Insert a freeze-capable reverb on (or as a send for) the synth phrase: cut the lows, mix 100% wet, raise diffusion, size and decay.
- Play the phrase and engage freeze at the musically richest moment; the reverb holds indefinitely even when playback stops. Release/turn down to end.
- Route the synth (with the freezing reverb) to a dedicated group bus, create an audio track whose input is that bus, and record a few bars (~4) of the frozen output. Then remove the temporary reverb and restore the synth's original output routing.
- On the printed track: EQ low end out and tame highs; add a sidechain-style volume shaper so it pumps with the groove.
- Add a second reverb on the print (low cut, ~5–6 s decay, larger size, modulation off) so the restart of the loop isn't heard as a jump.
- Make the clip loop seamlessly: add a small fade at the end, duplicate it onto a second track, and overlap clips so each new clip starts while the previous tail fades.
- Group both print tracks into an 'atmos' bus; process together (another large reverb with lows cut ~600–700 Hz and reduced feedback/mix, gentle top-end saturation/exciter).
- If the source filter opens later in the arrangement, print a second freeze with the filter open and use closed/open layers per section.

### Reverb for pads: pick type by texture, then set up 100%-wet EQ'd send returns
Source: [Merged from 2 YouTube how-to transcripts](None) · was `reverb-pads-type-choice-and-send-setup`
- Decide intentionally whether the source needs reverb (do not add by default). Match genre references.
- Recall controls: pre-delay separates dry from reverb onset (clarity); early reflections cue size/material; tail/late reflections = sustain; decay = fade. Think texture/tonality more than length alone.
- Hall: large auditorium character, often ~2–3s+ (longer for cinematic/atmosphere); lush/deep, thickens and pushes source back—high mud risk. Natural for piano/strings/orchestra.
- Chamber: studio reflective-room character—lush thickening with less mix real-estate than hall; very versatile (pads, strings, vocals). Room/ambience: smaller/intimate; ambiences often ~0.3–1s, ER-heavy—liveliness without takeover.
- Plate: mechanical metal-plate density; bright quick attack then darker decay—great sustain/sheen. Spring: metallic/boingy modulation in decay—character FX more than lush pad default.
- Build 2–3 saved returns: (1) room ~1s+ decay for basic space; (2) long ambient plate (transcript example ~6.2s); (3) spring or other bright flavor (~4s). Save in template.
- Use sends: set reverb mix to 100% wet on the return. Control amount only via send level so dry stays constant and wet can be EQ'd independently.
- EQ the reverb return after the algo: high-pass everything below ~200 Hz (or higher) so reverb does not invent mud. Optional cuts for metallic harshness (e.g. spring).
- Practice: pick type in solo for texture, set level in full mix. Layer short ambience under longer hall/plate. Busy mixes → shorter rooms/plates; sparse/ballad → longer halls/plates. Optional high-cut on reverb darkens and pushes wet further back.
- Add too much send, then back off to a musical amount. Longer decays usually need less send; shorter rooms can take more. Share one long plate across lead vs backgrounds with different send depths.

### Manual reverse-reverb swell: reverse, print 100%-wet reverb, re-reverse, trim and fade into the onset
Source: [Reverse Reverb Technique, Tips and Tricks in Cubase Music Production Tutorial](https://www.youtube.com/watch?v=DpXw9UPrTDU) · was `reverse-reverb-swell-print-reverse-print`
- Duplicate the source audio onto a second track.
- Reverse the duplicate (audio process -> reverse).
- Insert a large reverb (large live-stage/hall size) on that track with mix at 100% so you hear only the wet signal.
- Bounce/export the soloed wet signal to a new audio file (mono in the source example).
- Keep only the part that matters - the portion that leads into the first word/hit - and delete the rest and the temporary track.
- Reverse the printed clip back so the reverb now swells forward into the onset, and normalize it.
- Move it to just before the dry source and add short fade-in/fade-out at the clip edges to remove clicks.
- Optional: put another reverb (~50% mix) on the swell channel so it has a softer tail, and automate that reverb to come in only at the last split second so the whole tail does not wash out.
- Reuse on other sources: kick, cymbal crash into a breakdown, white-noise rise, pads/chords.

### Turn a few played notes into a self-sustaining shimmering pad by feeding them once into a clean stereo delay at 99% feedback with very different left/right times (about 1 s and 150 ms), so the melody dissolves into a continuous texture for the rest of the track
Source: [How to Create a Shimmering Pad](https://www.youtube.com/watch?v=r45X4PYH-fg) · was `self-sustaining-shimmer-pad-few-notes-into-99pct-feedback-asymmetric-stereo-delay-1s-left-150ms-right-melody-dissolves-into-texture-optional-tape-wow`
- Write a 3-4 note phrase and route it to a stereo delay set 100% wet on that channel (or on a send).
- Set left delay about 1 s and right delay about 150 ms; set feedback to 99% on both sides; leave cross-feed at zero.
- Play the phrase once and let it run; do not feed more notes in.
- Optional: swap to a tape-style delay with light wow/flutter to exaggerate shimmer.
- Add a limiter or level automation after the delay and check the level over the full track length.

### Shimmer reverb: +12st pitch-shift into lush space
Source: [Creating a Shimmer Reverb │ VAST Tips & Tutorials │ Heavyocity](https://www.youtube.com/watch?v=lzRl8gfa-M8) · was `shimmer-reverb-pitchshift-plus12-feedback`
- Route a send: place a delay/pitch stage before the long reverb. Set pitch shift to +12 semitones so the shifted copy washes into the lush space.
- Use a long lush reverb (or convolution with high lush/length) so the shifted signal sustains as a cloud.
- For endless blossom: enable feedback on the delay/pitch path so each loop shifts again. Short delay times → rapid expansions; longer times → slower bloom intervals.
- Tone-shape the delay echoes before reverb: cut lows so low end does not stack; shave brittle highs so the convolution/reverb is not harsh.
- EQ the overall shimmer wet (e.g. high-pass low band; gentle brightness if needed) before blending with dry via mix/send level. Optionally explore delay after reverb or ducking wet from dry later.

### One-knob reverb → drone instrument: macro range 0–99 = wet/dry, 100–110 = muted dead zone, 110–127 = freeze + overdub drone with LFO speed, plus LFO-modulated EQ/width, unsynced auto-filter, limiter and randomizable algorithm
Source: [Create Ambient Drones in Ableton Live 12.2 (Hybrid Reverb Tutorial)](https://www.youtube.com/watch?v=0NXGraBGWvE) · was `single-macro-reverb-mix-deadzone-freeze-overdub-drone`
- Build a rack: algorithmic reverb (convolution off) → LFO device → auto filter → limiter → utility (gain). Expose 16 macros: algorithm, decay, size, params 1–5 (map each algorithm's own 5 controls to the same macros), low/mid/high EQ, mid gain, vintage, width, pre-delay, drone.
- Reverb EQ: band 1 and band 4 as steep (48 dB/oct) edge filters mapped to 'low EQ' and 'high EQ'; bands 2+3 frequencies to 'mid EQ', their gains mapped inversely to 'mid gain'.
- Map the 'drone' macro: dry/wet over 0–99; utility on/off+gain so 100–110 is silent; freeze ('infinite') and overdub ('add') switch on at ≥110; LFO on/off, rate (fast at 110 → ~0.1 Hz at max), jitter and wave shape (≈75%→20%) across 110–127; auto-filter on and its LFO time also on this range.
- LFO device targets with depths: mid-EQ frequency 30, mid gain −25, low EQ 15, high EQ −20, width 15.
- Auto filter: frequency ~1500 Hz, resonance 10%, MS-type model, drive 5%, clip on; its own LFO in time mode at 10% amount, deliberately not synced to the rack LFO.
- Play: below 100 use as a normal reverb; above 110 play a note or two and let them overdub into the frozen space; adjust mid/high/low EQ in real time if boomy or trebly.
- Randomize the rack (exclude EQ, pre-delay and drone macros) to audition reverb spaces; save good results as rack variations and re-save the rack preset.

### Stereo delay motion: ping-pong, dual-parallel, two-tap, cross-feedback
Source: [Merged from 2 YouTube how-to transcripts](None) · was `stereo-delay-pingpong-dual-parallel-two-tap`
- Pick the delay topology for the job: ping-pong bounce (discreet L↔R, steps 2–5), dual-parallel with optional cross-feedback (dense poly-rhythmic space, steps 6–9), two-tap tape-head style (cleaner bounce, steps 10–11), or LFO panning delay (step 12). Then route and animate it (steps 13–14).
- Ping-pong: Enable ping-pong / stereo bounce delay. Set delay time to a musical subdivision (quarter or eighth) so repeats lock to groove.
- Ping-pong: Set feedback ~40–50% so repeats fade without clutter; wet/dry ~15–25% as a starting mix.
- Ping-pong: Filter the delayed signal: cut lows below ~100 Hz and highs above ~3 kHz to avoid mud/harshness. Optionally add tiny saturation/distortion on wet for warmth.
- Ping-pong: Maximize stereo width of the bounce when desired; link L/R times for even bounce, or slightly offset L vs R times for a more complex image.
- Start dual-parallel: set different tempo subdivisions per channel (e.g. dotted-eighth left, quarter right) so the shorter and longer echoes interact as a delay poly-rhythm (classic 3-against-4 feel with those two).
- Set self-feedback per channel (example starting points from transcript: ~45% left into left, ~30% right into right) with no cross-feedback yet; hear space/energy without stacked interaction.
- Add cross-feedback (right→left, then optionally left→right with complementary amounts) to stack interacting delays and fill the stereo field toward a faux-reverb density.
- Optional lush pad/ambient path: raise delay modulation depth (~20% in source demo) and diffusion (~50%) so dual-delay + cross-feedback reads more like reverb-space.
- Build two-tap (multi-head tape style): keep long + short times, but only the longer delay self-feeds and also feeds the shorter delay; give the shorter delay zero self-feedback and zero cross-feedback so taps never line up like dual-parallel — cleaner stereo around a center dry signal.
- Recognize ping-pong as a two-tap with ~2:1 time ratio (e.g. 400 ms / 800 ms) and the same long→short + long self-feedback topology; prefer dedicated ping-pong mode when available. Contrast with dual-parallel at 2:1 (short and long land together, soft-panned long tap).
- Optional: panning delay uses an LFO to move repeats (syncable for ping-pong-like motion or offset rates). Feedback-phase invert (negative feedback phase) flips polarity each regeneration to enhance spatial width on cross-feedback designs. Keep mix lower in practice; use ducking/EQ on wet for dense sources.
- Prefer send routing so you can EQ/compress the wet alone before blend; if insert, mind wet/dry carefully.
- Automate or modulate feedback, delay time, or filter cutoff across sections; optional subtle chorus/flanger on delayed signal only. Use on synths (also vocals/guitars/perc) especially in sparse/breakdown sections.

### EQ chorus dual-delay multi-algo reverb FX chain
Source: [TRAVELER: The Cinematic Hybrid Synthesizer | Official Walkthrough](https://www.youtube.com/watch?v=IU76c2Cygs4) · was `traveler-walkthrough-fx-eq-chorus-delay-reverb`
- Insert 3-band EQ first: sculpt low end, mid presence, and highs so the synth sits in a mix before time FX.
- Add chorus: choose type 1, type 2, or combined. Keep wet modest for cinematic width without seasick detune.
- Dual or ping-pong stereo modulated delay: independent L/R times, feedback, stereo spread, feedback filters, and classic delay modulation.
- Reverb: pick room, hall, or space algorithm (space can reach very long tails). Set size/decay/predelay manually with original settings.
- Map portable names: KeyTIME-like = tempo-synced modulated delay motion; KeySPACE-like = multi-algo cinematic reverb. Keep FX after synth engine; watch limiter on main out.

### Filtered feedback-delay resonator: bipolar feedback, swappable loop filter type, dry mute, insert on existing sounds
Source: [KARPLUS-STRONG synthesis in Renoise and the •REZONATOR•](https://www.youtube.com/watch?v=SfqgigefIu0) · was `tuned-filtered-delay-resonator-insert-bipolar-feedback`
- Prepare a full-frequency impulse: a short white-noise burst or a fast sine sweep from very high to low frequency. Set it to one-shot (no loop) so it is only a click.
- Insert a delay with feedback and an in-loop filter. Start around 24 ms delay, feedback 50%, effect amount full, filter low-pass fully open.
- Make performance macros: (1) L+R feedback with range −99…+99 (centre = almost no repeats; negative = hollow square-like character; positive = saw-like), (2) delay time L+R capped at ~24 ms as 'pitch', (3) filter cutoff.
- For keyboard pitch: map key tracking onto delay time inversely — lowest key → ~24 ms (slow cycle = low pitch), highest key → ~1 ms.
- Add a macro for filter type (LP/HP/BP/notch) and automate/record it. With bandpass or notch, raise resonance somewhat — they sound better slightly resonant.
- Mute the dry signal so the impulse click disappears and only the resonance remains; optionally add drive in the loop (can scream) and a following delay.
- Try different impulse sources (sine, saw, more or less pitched) — the impulse strongly changes the timbre.
- Resonator insert: put the same delay (wrapped in a macro rack) on an existing bass or pad; tune delay/filter to taste (check filter isn't left on high-pass), keep it subtle or brighter/distorted.
- Resample interesting results for further processing.
