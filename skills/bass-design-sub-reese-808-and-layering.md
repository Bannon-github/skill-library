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
