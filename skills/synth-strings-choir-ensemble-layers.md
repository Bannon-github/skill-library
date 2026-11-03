# Synth strings, ensemble and choir layers

Goal: Build string-section and choir-like synth layers: PWM 80s strings, unison with delayed vibrato, saw/FM blends, opposite-direction arpeggiated plucks that read as strings, noise-comb ensemble pads and hybrid choir pads.

**Theory:** Ensemble = many slightly detuned, slightly late voices; delayed vibrato (5-6 Hz after ~0.3 s) and slow attacks mimic bowing; PWM produces chorus-like motion from one oscillator.

**Hear it:** `sample-lab/theory/detune_unison.py`

## Workflow
1. Oscillators: PWM pulse with free-running LFO (0.3-1 Hz), or 2 saws + unison, optional low FM for bite.
2. Attack 0.1-0.5 s, release 0.5-1.5 s; vibrato 5-6 Hz delayed ~0.3 s, depth a few cents.
3. Filter LP 2-5 kHz with velocity/brassy filter envelope for swells.
4. Voice the parts like a section: low strings root/fifth, violins in thirds/sixths above, keep voice-leading smooth.
5. Arp trick: two plucky saw arpeggios in opposite directions blur into a string texture under reverb.
6. Choir: formant/vocal tables or noise-comb lanes for highs, synthetic lows underneath; notch harsh bands.
7. Add ensemble/chorus and hall reverb; high-pass under 150 Hz.
8. Hear the theory: run `/home/box/audio-tools/bin/python sample-lab/theory/detune_unison.py` from the repo root and compare the sections; reuse its functions as a starting point for renders.

## Source techniques (merged, numbers kept)

### Dark hybrid vocal pad: choir-like wavetable plus an octave-up choir sample FM'd in (~34%), with sub and a little noise. Lows/mids are low-passed while the natural sample keeps the highs, a subtle LFO notch moves the mids, and one slow rising ramp drives the FX
Source: [The Secret to HUGE Dark Vocal Pads in Serum 2](https://www.youtube.com/watch?v=Futy449F9OY) · was `dark-hybrid-choir-pad-natural-highs-synthetic-lows-notch-ramp-fx`
- Osc A: choir-like wavetable, unison for chorus, slight low-pass. Create one main modulator, a slow triangle that effectively ramps up, on wavetable position (and later FX amounts).
- Osc B: choir multisample an octave higher with a bit of tube saturation, defaults otherwise. FM it into osc A at ~34% for a touch of grit.
- Add a sub oscillator at default level under everything, and white noise (or hum) at a very low level for full-spectrum air.
- Filter 1: low-pass on osc A + sub only; route osc B around it so the natural choir provides the high end.
- Filter 2 on the combined signal: notch at ~18% mix (100% shows the full effect), with the amount rising on the LFO and the cutoff moving slightly too, for mid-range expression and cohesion.
- FX 1: a frequency-shifter/blur stereo layer, mix ~half, blur ~half, shift and range lowered, blended in as a moving super-wide layer. Dimension ~6%. Hyper-chorus automated from low up to ~32% at the top of the ramp.
- FX 2: ping-pong delay ~10–11%; distortion with a high-pass so only ~300 Hz upward is saturated; a little comb filter (macro candidate); reverb ~10%; final high-shelf presence boost.

### Cinematic ensemble string pad from noise-excited combs: two comb lanes (static vs pink noise, different comb flavours) with fast random pitch drift for a section feel, key-tracked low-pass so low notes stop sounding metallic, a smoothed saw layer and an EQ'd sine/FM low end, a low-boosting resonator, mod-wheel cutoff, velocity that shortens attack and release, a tiny strike pitch envelope and offset triangle 'bow' LFOs on comb tilt
Source: [How to Design Cinematic Realistic String Pads - Zebra 3 Sound Design Tutorial](https://www.youtube.com/watch?v=leLAm3OigI0) · was `ensemble-string-pad-dual-noise-comb-lanes-random-drift-keytracked-darkening-velocity-env-bow-tilt-lfos`
- Lane A: static noise → amp envelope with slow attack and slow release → comb. Raise comb feedback until the tone is sharp and pitched; low-pass the noise to remove edge.
- Add an LFO set to random ramp, not tempo-synced, routed lightly to fine detune; speed it up until it reads as a group of players, stopping short of vibrato.
- Global FX: a little mod/diffusion (slow shape), reverb; set a non-resonant 6 dB linear filter as a starting point and increase width.
- Lane B: duplicate the idea with pink noise into a different comb flavour/complexity, detuned the same way. Mix lanes A and B and route both through one shared filter.
- Key-track the shared filter cutoff with the centre near middle E (about 64 in the middle). Add a little comb distortion if wanted.
- Body: add a saw oscillator smoothed with a curve filter in string range (double it for width) and a sine/FM layer EQ'd to keep only low end. Optionally add an EQ resonator boosting lows on lane 2 in the global FX.
- Playability: mod wheel → filter cutoff; velocity → attack and release so harder strikes get shorter attack and shorter release (keep a minimum above zero); compress only the top peaks.
- Strike pitch: a short curved envelope adding a tiny pitch rise to both comb pitches (exaggerate to hear, then reduce). Bow motion: triangle LFOs with rates in seconds on comb tilt/flavour, at different rates per lane so they do not move in unison.

### Make synth layers read as strings or orchestra by obscuring them: two saw-based arpeggiated plucks moving in opposite directions, a fast-open filter envelope and vibrato, a shared pitch-shifting modulated reverb, and level automation plus sidechain so the listener only hears brief glimpses without context
Source: [How To Synth 5: Synthetic Ambient Orchestraish Strings](https://www.youtube.com/watch?v=_cVKvtFm8J0) · was `hidden-context-synth-strings-two-opposite-direction-arpeggiated-saw-plucks-brassy-filter-env-vibrato-spectral-phaser-above-fundamental-shared-pitch-mod-shimmer-reverb-gated-glimpses-under-sidechain`
- Program the chords with a fixed note count (e.g. 3 notes) so arp cycles stay predictable; arp cycle length grows with note count.
- Voice 1: saw-like oscillator, light unison, vibrato on, filter envelope that opens fast then decays (brass-style smoothed pluck), arpeggiator going up at half speed (double the default step time).
- Add a phaser (or harmonic pitch modulation) masked so it only affects partials above the fundamental, so pitch stays clean while upper harmonics shimmer.
- Voice 2: same idea with a longer pluck decay, lower filter, a bit more unison, arp direction reversed (starts at the top) so the two layers cross.
- Send both voices to one shared reverb: large size and diffusion, low feedback, pitch shift down in the feedback, high modulation depth; high-pass and lift the top before the reverb.
- Automate the layer's level by feel so it only comes through at selected moments, and sidechain it under the drums.
- Optional support: a soft sustained chord stack with big reverb, gated so tails stop when the chord stops, with a fader dip so it starts large and smooths out.

### 80s PWM string pad: pulse wave with free-running (seconds-based) LFO on pulse width, slight osc-2 detune, slow attack/release, static filter
Source: [80s String Pad Tutorial (1/2) - Pulse Width Modulation in Tyrell N6](https://www.youtube.com/watch?v=0n23itgG0LU) · was `pwm-80s-string-pad-free-running-lfo-detune`
- Start from an init patch; keep a scope visible. Change oscillator 1 from saw to pulse (square = 50% duty cycle; pulse widths roughly 10–90% duty).
- Route an LFO to pulse width and watch the scope: the pulse width sweeps.
- Switch the PW LFO from tempo-sync to free-running seconds so the string movement keeps the same rate regardless of DAW tempo; set ~0.7 and a moderate depth.
- Bring in oscillator 2 (presenter's level ~17.5) alongside osc 1, then detune osc 2 ever so slightly (fine ~0.20) — perfectly in-tune oscillators lose the effect.
- Lower the low-pass cutoff to cut the really high end; reduce output level if hot.
- Amp envelope: much slower attack (presenter ~38 display units) for a fade-in and a long release that tails naturally.
- Set master transpose from −12 to 0 so A440 plays A440. Turn off the filter envelope and other filter modulation sources so the filter stays static.
- Set the voice/unison count the presenter uses (2), play chords to confirm the 1980s string pad, and save it as a patch.

### Synth string section: 7-voice unison saw, subtle bow-brightness envelope, LFO-on-detune vibrato with ramped rate, low FM blend
Source: [How To Make A Cinematic String Section - Sound Design Tutorial](https://www.youtube.com/watch?v=IK7cIBPKM1s) · was `synth-string-section-unison-vibrato-fm-blend`
- Init patch. Osc1 saw, 7 unison voices, ~7% detune; set the two osc start controls the video zeroes (unnamed in the transcript; typically phase/random-phase) to 0 to avoid clicks and pops. Route through filter 1: analog low-pass 12 dB/oct (6 dB works even better), resonance 0, cutoff ~450 Hz (later ~400 Hz), a little drive.
- Amp envelope: attack ~1.5 s, decay ~5 s, sustain ~70%, release ~2 s. Velocity sensitivity 100%; polyphony ~24 voices so notes don't cut each other off.
- Bowing brightness: envelope 2 attack ~0.5–0.6 s (rounded curve), decay ~4–5 s, sustain ~20–30%, release ~0.1 s → filter cutoff with a small amount (~15). Keep it subtle.
- Ensemble vibrato: LFO1 at 1 s period → unison detune amount ~0.06 (detune moves roughly 7% → 10–11% and back) rather than modulating global pitch.
- Variable vibrato speed: LFO2 as a ramp, 4–5 s period → LFO1 rate (amount ~0.2) via the mod matrix so vibrato starts slow and speeds up, then resets.
- Second osc: 7 unison voices ~10% detune through filter 1, FM from osc1 at a low amount (~30–35%; high amounts sound bad).
- FX: low-cut rumble (keep lows only for bass use), take a little off the top to reduce fizz, reverb with high mix and large size (decay up to 4–5 s), quarter-note mono delay with low feedback and low mix, soft-clip distortion with drive up and mix ~20–30% (end of chain, or before reverb so the reverb carries the grit).
- Macros: one macro → distortion drive, one → reverb mix, and one macro to several FX at once (reverb + delay) for quick performance control.
