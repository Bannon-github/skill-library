# Bass design: sub, Reese, 808, punchy bass and distortion layering

Goal: Design basses that translate: clean sine sub split from a distorted mid layer, Reese detuned saws, punchy 808 with pitch envelope, archetype punchy basses, sub drops and cinematic distortion stacks; keep kick/bass relationship clear.

**Theory:** Fundamental below ~100 Hz must stay mono and clean; harmonics (100 Hz-2 kHz) make bass audible on small speakers. Detuned saws beat to create Reese movement; fast pitch envelopes create punch.

**Hear it:** `sample-lab/theory/bass_design.py`

## Workflow
1. Pick the root note and check its Hz (e.g. A1 = 55 Hz); tune 808/kick to the key.
2. Sub layer: sine/triangle, mono, low-passed ~100 Hz; never distort it.
3. Mid layer: Reese (3 saws, ±10-20 cents, one octave down), or FM/noise grit; high-pass ~100 Hz then distort/saturate; parallel compress.
4. 808: sine with pitch envelope (+12 st -> 0 in ~35 ms), hold/decay to taste, tube drive for harmonics, glide between notes.
5. Kick relationship: either the kick owns the transient (delay bass attack ~10-30 ms) or sidechain the bass fully to the kick.
6. Sub drop: sine 80 -> 20 Hz over 1/2-2 bars at impacts.
7. Check on small speakers and mono; level bass against a reference.
8. Hear the theory: run `/home/box/audio-tools/bin/python sample-lab/theory/bass_design.py` from the repo root and compare the sections; reuse its functions as a starting point for renders.

## Source techniques (merged, numbers kept)

### Brooding cinematic drone: three pulse-width-morph oscillators, opposed octave detune, single-osc vibrato, LFO PW breathing and split pitch-bend depths
Source: [How to create Massive, Brooding, Cinematic Drones in any Synth](https://www.youtube.com/watch?v=DFLshMLKkHE) · was `brooding-pw-drone-detuned-octave-stack-split-bend`
- Use three oscillators, all set to a pulse-width-shifting square (a square whose pulse width can morph). Square/odd-harmonic content gives the hollow, brooding foundation.
- Osc 1: move the shape slightly away from pure square for a biting edge, use 2 voices slightly detuned, add a slight vibrato, tune -12 semitones.
- Osc 2: keep a square, tune -12 semitones, 4 unison voices detuned very wide.
- Osc 3: leave at the higher (unshifted) pitch, give it a different pulse shape, 2 voices slightly detuned.
- Amp envelope 'pad treatment': slow attack so the sound creeps in, long tapering release.
- Add drama/clash: nudge the two octave-down oscillators by a small fraction in opposite directions (presenter's display: about -12.10 and -11.90) and offset Osc 3 slightly (~.5 in the synth's fine units).
- Restrict vibrato to one oscillator only; the others get none.
- Set pitch-bend range to +-1 so you can bend up and down by small amounts.
- Assign a slow LFO to Osc 3's waveform/pulse-width morph for a little breathing.
- Add a 12 dB low-pass (cascade-style) to tame harshness and map the mod wheel to cutoff; start notes with the mod wheel up and ride it.
- Global FX: reverb with larger size and more wet so it holds on; then a delay (~140 in the presenter's units) with a little feedback and high-pass/low-pass on the repeats.
- Make bends spread: add a small extra pitch-wheel -> tune amount on Osc 1 (~20) and a larger one on Osc 3 (tried ~75, settled near 60 and then pulled slightly lower) so oscillators bend at slightly different rates.

### Cinematic bass FX bed: WT+sub through stacked distortion/compression, then pitch-bend downer
Source: [How To Sound Design Cinematic Basses and Subdrops](https://www.youtube.com/watch?v=PUBMG__czwg) · was `cinematic-bass-distortion-stack-pitch-bend-downer`
- Init WT osc; transpose −12 st. Apply a bend-style warp in small amounts to soften robotic digital WT character. Add modest unison width with reduced detune so it is wide but not chorus-wobbly.
- Stack several distortions and compressors in series. The more extreme the stack, the less the specific WT matters. Use some compressors to bring high-end back; disable multiband modes if the tone goes boxy.
- Place a filter or EQ early in the FX chain and modulate a morph/cutoff with one slow LFO plus a second LFO (different rate, limited depth) so movement is smashed into the distortion.
- Add a second oscillator +12 st with fewer unison voices for air. Keep a sine sub in the patch and intentionally run it through the same FX — bypassing FX shows how much the sub colors the grind; tweak sub pitch for large timbral changes.
- Post: more compression/saturation (soft-clip/inflator-style with low drive), limiter, enable legato/glide. For braams/bends draw a one-shot pitch curve (e.g. 2 bars). For downers invert the pitch gesture and automate filter cutoff with a fast-then-slow asymmetric curve over ~2 bars, optionally keeping lows less affected.

### Design four bass types from scratch with fit-to-kick rules: a punchy 808 (sine, hold and 1.5 s decay, a 35 ms pitch-envelope punch, tube drive, low boost, attack delayed 80-100 ms when the kick already punches), a pluck bass (mono square through an enveloped 24 dB low-pass plus a wide unison top layer), a sidechained saw growl, and a click-free sine sub
Source: [Bass Sound Design: 808s, Plucks, Growls and Sub Bass](https://www.youtube.com/watch?v=H6i55lXAMh0) · was `four-punchy-bass-archetypes-808-sine-hold-decay-35ms-pitch-env-punch-tube-drive-100hz-lift-attack-delay-vs-kick-pluck-mono-square-lp24-env-plus-wide-pwm-unison-saw-growl-lfo-duck-sub-sine-5ms-attack`
- 808 body: sine osc, attack near 0 then raised just enough to remove the click, hold about 300-400 ms, decay about 1.5 s, sustain 0; add a slight bend/warp to the wave for character.
- 808 punch: second envelope (attack about 0.5 ms, hold 0, decay about 35 ms, sustain 0, release about 15 ms) → master/global tune; set the amount between too little and too much.
- 808 FX: tube distortion with mix pulled back, EQ lift around 100 Hz. Play with the drums: if both kick and 808 punch, raise the 808 attack to about 80-100 ms so the kick provides the transient.
- Pluck bass: mono voicing, square osc into a 24 dB low-pass; amp envelope with tiny attack, no hold, low sustain, a bit of release; route the same envelope to cutoff and add a little filter drive.
- Pluck top layer: second osc with a PWM-style wave, 5-7 unison voices, detune set for width, through the same filter at lower level; add reverb and delay with their lows cut; keep lows mono below about 100-150 Hz.
- Growl bass: saw + low-pass, second saw osc with 7-8 unison voices, mono, very short release; draw an LFO shaped like a sidechain duck and route it to both osc levels; put cutoff (and optionally reverb/delay mix) on macros; boost around 140 Hz.
- Sub: sine, 1 voice, mono/legato, attack about 5 ms, short-but-not-instant release; play low.

### Hybrid noise+distortion layer separate from sub/harmonic patch
Source: [Serum Tutorial: White Noise Bass (Copycatt/Chee)](https://www.youtube.com/watch?v=EWe_Fnjcceo) · was `hybrid-noise-distortion-separate-sub-layer`
- Layer A (noise texture): start from a sine (or muted tonal osc), enable noise oscillator/source; set noise level ~50% and adjust noise pitch (~55% in source) to taste.
- Add asymmetric (or similar) distortion ~50% to grit the noise. Filter the noise path (source ~cutoff example in mid-high range) to pull harshness back.
- EQ the noise layer: high-pass/roll off the bottom (Q ~45% to flatten a hump), set HP frequency into the low-mid region so the noise isn’t muddy; optionally trim highs ~−2.5 dB. Mute the tonal osc on this layer if sub will be separate.
- Layer B (harmonics/sub): separate instance/patch for low tones so changing WT/harmonics won’t rewrite the noise timbre. Prefer a harmonically useful wave (transcript favors square) or WT; shape independently.
- Performance trick: hold one noise-layer pitch across moving sub notes so grit stays consistent while bass harmony moves—or map both together if you want noise to track. Blend to taste; for pads, lower distortion and lengthen amps, still keeping noise and WT/filter on independent paths.

### keytracked low-osc bass split with wet delay
Source: [TRAVELER | Behind the Scenes with David Helpling](https://www.youtube.com/watch?v=yJWS77wyVe0) · was `keysol-helpling-keytrack-bass-split-delay`
- Create a simple two-layer patch: mid/high tonal oscillator(s) plus a dedicated low oscillator.
- Modulate the low oscillator’s volume with keyboard tracking so it is strong only in the lower register (left hand / low keys) and fades as you play higher.
- Set delay wet very high (delay almost louder than the dry sound) to showcase modulation/space; filter delay feedback to taste.

### velocity-rewarding hybrid bass and impact
Source: [TRAVELER Track Walkthrough by Venus Theory](https://www.youtube.com/watch?v=jLGz5wq2CRE) · was `keysol-venus-velocity-hybrid-bass-impact`
- Start with dark hybrid oscillators (saw/pulse + optional WT). Fast amp attack, punchy decay, moderate sustain for bass; shorter for impacts.
- Map velocity strongly (near-exponential) to filter cutoff and/or drive so louder playing blooms dramatically.
- For atmospheric use: apply aggressive high-pass on the mix, play high register with pitch bend, and use a broad smooth space-style reverb so hits become huge pads/stingers.
- For deep bass: keep HP low/off, emphasize transient, optionally underscoring with sub; avoid static sine-only subs — keep some transient character.

### Reese bass from three octave-down saws (outer two with 3-voice unison at about 10% detune and zero phase randomization, middle one single voice, outer pair fine-tuned slightly up and down), mono legato always-glide, soft-clip drive, half-mix compressor, resonant high-pass, low-cut reverb, soft-clip saturation, high roll-off, automated high-pass movement, mono below 120 Hz and kick/snare sidechain
Source: [How to Make a HUGE Reese Bass in Vital | Deep Dubstep & DnB Sound Design Tutorial](https://www.youtube.com/watch?v=7OatKTrtmJ8) · was `reese-bass-three-saw-octave-down-mixed-unison-fine-detune-mono-legato-glide-softclip-parallel-comp-hpf-automation-mono-below-120`
- Oscillator 1: basic saw, −12 semitones, unison 3 voices, unison detune ~10%, phase randomization 0. Oscillator 2: saw, −12, one voice. Oscillator 3: same as oscillator 1.
- Fine-tune oscillator 1 slightly up and oscillator 3 slightly down.
- Set voices to 1 (mono), glide about halfway, enable always-glide and legato. Overlap the start of the next MIDI note with the end of the previous one to slide into it; separated notes do not bend.
- Synth FX: distortion in soft-clip mode at about 9 dB drive; compressor placed after the distortion with mix ~50%, release ~36%, attack ~56%.
- Add an EQ with a high-pass filter, a touch of resonance, and the cutoff set into the low-mid. Add a small reverb with its low end removed and a shorter time.
- After the synth: saturator in a soft-sine curve with soft clip on, drive just over 3 dB, output −2 dB. Then an EQ that rolls off the top end and makes a small mid dip.
- Automate the high-pass cutoff so it opens and closes over the phrase, and add a small pitch-wheel drift lane for extra movement. If it sounds muffled, ease the top roll-off back a little.
- Make everything below 120 Hz mono and lower the gain slightly. Add two compressors sidechained to the kick and to the snare so the bass dips on each hit. Optionally resample and chop the result.

### Custom sub-drop: automate a sine from ~80 Hz down to ~20 Hz
Source: [How to make custom bass drops / sub drops in Cubase (tutorial)](https://www.youtube.com/watch?v=FULqquC3-Fc) · was `sub-drop-sine-freq-glide-80hz-to-20hz`
- Create a mono track and insert a sine test-tone generator (or a sine-only oscillator). Name the track as a sub-drop layer.
- Pick a start frequency near 80 Hz (or look up the Hz for your song's root); set end near 20 Hz for a deep trailer-style drop.
- Draw frequency automation from start_hz to end_hz across the chosen length (e.g. 1 bar). Elongate or shorten the automation for brutal long drops vs fast stabs.
- Automate bypass/mute so the generator is only active during the drop window.
- Optional: add bass-harmonic exciters/saturation (e.g. 'max bass'-style) if you want audible upper harmonics; verify on a spectrum that harmonics appear only when desired. Export several lengths/keys into a personal drop folder.

### Clear-bass workflow: low-cut every other part at 100-150 Hz, keep bass notes at 40-80 Hz, then audition three bass-line roles (matching-rhythm, eighth-note pulsing pluck with saw plus same-octave sine and a duck, sustained root per bar) and pick the one that fits
Source: [I Fix A Beginner Producer's Weak Bass (in under 15 minutes)](https://www.youtube.com/watch?v=Z6IUhXyOvFc) · was `three-bassline-roles-clear-sub-40-80hz-lowcut-others-100-150hz-matching-rhythm-vs-eighth-pluck-pulse-vs-sustained-root-per-bar`
- Clean up first: mute or delete the old bass layers, thin out muddy duplicate chord layers, reduce heavy reverb on the lead/piano, and leave small gaps between melody notes so it reads more rhythmic.
- Low-cut every non-bass instrument at a sweet spot between about 100 and 150 Hz. Check the analyzer: nothing else should spill into the sub range.
- Make the bass patch: init synth, shift the octave until the fundamental sits below 100 Hz with notes landing between about 40 and 80 Hz, then use a tight low-pass to focus any waveform toward its lowest frequencies. Try several waveforms; add mid presence by opening the cutoff slightly or with light distortion.
- Option 1, matching bass: copy the chord roots to a new track and cut them to the exact rhythm of the melody, so bass and melody hit together.
- If any bass note gets lost in the chords or piano, move that note down an octave so the two parts sit in separate ranges.
- Option 2, pulsing bass: eighth notes (8 per bar) following the chord roots. Make it a pluck: put a spare envelope on a fully closed cutoff with sustain at zero; use a saw and add a sine at the same octave to thicken it; add a light sidechain-style duck to enhance the pulse.
- Option 3, sustained bass: one bass note per bar on the chord root. If it holds the energy back, try mono with a short glide between notes, or a wider high-unison saw version, optionally with a filter envelope; remember a mono sub sounds more anchored.
- Play the track with each option and pick the one that fits: matching moves the melody along, pulsing gives a tighter foundation, sustained is the calmest.

### Ambient bass with a solid floor: one mono voice with light unison, a single slow retriggered master LFO (about 4 bars) on many timbre targets (wavetable position, both filter cutoffs, drive, formant, FX filter) so everything moves together, an FM macro for grit, and a clean sine sub sent direct-out past the filter while the upper layers are high-passed
Source: [Get BETTER ambient bass EVERY time](https://www.youtube.com/watch?v=MULPJOhSrZ0) · was `ambient-bass-mono-voice-light-unison-one-slow-master-lfo-4-bars-on-12-targets-wt-cutoff-drive-formant-fm-macro-direct-out-sine-sub-hp-upper-layers-mono-below-100-120hz`
- Set the bass to a single voice (mono) and add light unison (the source uses 5 voices on two oscillators) for subtle motion that shows on an oscilloscope without smearing the low end.
- Make one master LFO: retriggered on each note, slow (about 4 bars per cycle), and route it to many destinations at small amounts: wavetable position on both oscillators, filter 1 and filter 2 cutoff, distortion amount, spectral morph/harmonic stretch, a negative formant scale, and the FX distortion's filter and drive.
- Add an FM macro: osc 2 frequency-modulates osc 1 (and vice versa), and the same macro brings in an offset distortion that only starts once FM is applied. Try it an octave up if it is muddy.
- Add an osc-mix macro that fades a third oscillator in from zero.
- For a solid floor, set a sub/extra oscillator to a plain sine with no LFO modulation and route it direct out (past the filter and effects).
- Put a high-pass EQ on the moving layers (or the full patch before the sub joins) so they are cut at the low end and leave room for the sine; balance the sub level by ear.
- Apply bass mono below about 100-120 Hz on the channel (or rely on the single voice), and A/B in the track: the bass should stand out a little and guide the track without dominating.

### Make a sine sub audible on phones and laptops: keep the 20-60 Hz fundamental but add pleasing harmonics in the 60-200 Hz bass range with volume-compensated hard clipping (odd harmonics) and/or an added overtone series (octave, fifth, octave), then scoop the honky low mids, low-pass the fizz, optionally add soft sine layers two and four octaves up, and tilt toward the top only if notes are still unclear
Source: [Create "Audible" Sub Bass in Ableton Live](https://www.youtube.com/watch?v=63FvtgN6Yrc) · was `audible-sub-bass-on-phones-sine-sub-20-60hz-plus-harmonics-60-200hz-volume-compensated-hard-clip-overtone-series-octave-fifth-low-mid-scoop-lowpass-plus-2-4-octave-sines-fast-comp-tilt`
- Check the sine sub on an analyzer: only the fundamental shows, inside 20-60 Hz, and the notes are hard to make out on small speakers.
- Add volume-compensated hard clipping and raise it slowly until the bass line becomes audible. It adds odd harmonics (e.g. one at 139 Hz for a low F sharp).
- Alternatively or in addition, add the harmonic overtone series to the sine: an octave, a fifth above that, and the next octave, at low levels.
- Scoop the low mid-range that the harmonics create with a bell cut, which also emphasizes the lows and makes the bass less honky.
- Low-pass the result to tame the upper harmonics and any fizz.
- To keep a subby, 'wumpy' character instead of grit, add soft triangle/sine-like layers two octaves up and four octaves up and set their level with the low-pass. A little saturation on top goes a long way.
- For a thinner, different distortion color, compress the sub with a very fast attack and fast release (multiband if available); low-pass afterwards to clean up the aliasing junk.
- If notes are still unclear, tilt the EQ to favor the top and reduce the sub, re-scoop a little and low-pass again. Check on phone/laptop speakers and on headphones.

### Parallel octave-down bass for a thin ambient stereo take: duplicate the mix, pitch it down an octave at the same tempo, low-pass it at ~100 Hz (12 dB/oct), high-pass the original at the same point (24 dB/oct), squash the copy with a limiter and blend it in quietly, checking phase correlation
Source: [Fix a Thin Mix: Easy Parallel Bass Trick for Ambient Music](https://www.youtube.com/watch?v=eDErfMlnh7c) · was `parallel-octave-down-bass-from-stereo-mix`
- Analyse the mix: find where the low end rolls off (e.g. steeply below ~100 Hz).
- Duplicate the track and pitch the copy down one octave while keeping the playback speed (warp/time-stretch). Energy at 100 Hz now appears at 50 Hz.
- Turn the copy well down, then low-pass it gently (12 dB/oct) at about the original's roll-off (~100 Hz).
- High-pass the original (24 dB/oct) at the same point so the two paths do not overlap.
- Check a phase-correlation meter around 100 Hz; adjust the crossover if correlation drops.
- Limit the copy aggressively (several dB of gain reduction, e.g. ~6-7 dB) so its dynamics are flattened, then set its level low and A/B on and off.

### Kick+bass punch workflow in four levels: (1) duck the bass to the kick, (2) split sub (<~100-120 Hz, mono, no unison) from mid-bass and duck the sub harder, (3) lock sub phase (fixed oscillator start phase, set by oscilloscope and blind A/B, then micro-delay alignment), (4) light bus glue on kick+bass: subtle subharmonic saturation, ~30 ms-attack glue compressor at 1-2 dB, soft clip
Source: [This Will Change How You Mix Kick And Bass FOREVER](https://www.youtube.com/watch?v=UrpnB5YlGL8) · was `kick-bass-four-level-lock`
- Mark bass notes that hit with the kick and those that overlap it. Check level and oscilloscope with kick solo vs kick+bass: overlapping notes make the combined peak swing.
- Level 1: duck the bass on every kick (sidechain compressor or volume shaper). Draw the duck shape by hand if the kick's exact shape is too long, so the bass sits in the pocket.
- Level 2: duplicate the bass into sub and mid-bass. High-pass the mid-bass at about 120 Hz (no fundamental there); low-pass the sub at the same point and turn its unison off so it is mono. Duck the sub fully on the kick and the mid-bass only a little. With one instrument only, use multiband ducking (below ~100 Hz ducked, above not), knowing the unison sub will still phase-cancel.
- Level 3a: on the sub oscillator set phase randomization to 0 so every note starts at the same point in the waveform. Overlay kick and sub on the oscilloscope.
- Level 3b: sweep the sub's fixed start phase while watching the summed waveform and listening; pick the setting where the sum is loudest and steadiest, confirming by blind A/B.
- Level 3c: if the sub's cycles are slightly offset from the kick's, add a tiny track delay (fractions of a ms) to the bass to line the waveforms up; blind A/B.
- Level 4: route kick and all bass layers to one bus. Add a small amount of low-end/subharmonic saturation (easy to overdo), then a glue compressor at about 30 ms attack for 1-2 dB gain reduction with make-up gain, then a soft clip. If more than ~2 dB is needed, fix earlier steps instead.

### Mono-compatible wide bass: strip the fundamental from a unison wavetable (FFT/harmonic editor), keep the wide upper harmonics with unison, then add a separate mono sine as the fundamental with phase-randomize at 0
Source: [How to make any "WIDE BASS" mono-compatible!](https://www.youtube.com/watch?v=5oW5Mb-3sF0) · was `wide-bass-remove-fundamental-add-mono-sine`
- Start from a saw (or similarly bright) wavetable. Optionally add a gentle low-pass so the raw tone is easier on the ears.
- Open the wavetable / FFT / harmonic editor. Identify the first harmonic (fundamental) and remove or zero it so the table is overtones only. Solo A/B: the tone should sound thinner and weaker.
- Enable unison on that weakened oscillator (e.g. 5 voices) with a small detune (source default ~0.25). This widens only the overtones.
- Enable a second oscillator as a pure sine at the same pitch. Leave its unison off. This sine is the new fundamental.
- Set the sine oscillator's phase-randomize / rand to 0 so every note starts at the same phase (stable for kick alignment). Do not zero rand on a normal full-spectrum unison Reese — that creates a sweeping laser artifact and still collapses in mono.
- A/B the patch in mono: the fundamental-stripped+sine version keeps power; a normal unison Reese pumps and thins. Optionally check an oscilloscope against the kick.
