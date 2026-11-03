# Vocoder, formant and spectral voice effects

Goal: Use vocoders and formant tools: vocoder as an insert on any patch (carrier/modulator), formant shifting, frequency-shifted harmonic layers, spectral warp/stretch and five-stage hybrid transform chains (pitch, formant, saturation, key-tuned peak, LP push-back).

**Theory:** Formants are fixed resonant peaks that define vowels independent of pitch; a vocoder imposes the modulator's band envelopes onto a carrier's spectrum.

**Hear it:** `sample-lab/theory/formant_vowels.py`

## Workflow
1. Carrier: rich harmonic synth (saw, supersaw); modulator: voice or drums.
2. Set band count (16-32 for intelligibility), decay/release, formant shift.
3. Alternatively apply formant filters (vowel BP peaks) or frequency shift by harmonic multiples for clean layers.
4. Transform chain: pitch -> formant -> saturation -> key-tuned peak -> LP to push it back.
5. Blend dry for intelligibility; EQ out mud.
6. Hear the theory: run `/home/box/audio-tools/bin/python sample-lab/theory/formant_vowels.py` from the repo root and compare the sections; reuse its functions as a starting point for renders.

## Source techniques (merged, numbers kept)

### Harmonic-locked frequency shifter layer (shift by multiples of f0) cleaned with EQ, micro-delay and a self-vocoder
Source: [Chaos To Order: Frequency Shifter & Vocoder (Sound Design Tutorial)](https://www.youtube.com/watch?v=54eGln75Y3Y) · was `harmonic-multiple-frequency-shift-layer-vocoder-clean`
- Start on a plain sine to learn it: note C ≈ 130 Hz. Add 130 Hz shift → up an octave; add multiples (260, 390, 520 …) and listen to each land on further harmonic-series notes (fifth, octave, third…).
- Compare with an arbitrary shift (e.g. 174 Hz) to hear dissonant overtones.
- Apply to a richer sound (e.g. a bass an octave down); harmonics that already line up change little, other patches gain dark, cool harmonics. Blend with the original.
- Build a dry/wet split; on the wet path add EQ to tame the loud shifted 'fundamental' (low cut, or a band reject; low cut before the shifter also works).
- If the layer bubbles/phases (shifts under ~1 kHz), add a ~1 ms signal delay to the path to remove it.
- Clean the messy layer with a vocoder on itself: lowest band set above the sub so lows are untouched, run it on another dry/wet chain so the clean sub stays; adjust band count/bandwidth (narrower = crystalline/metallic), formant and per-band levels as EQ.
- Example bass: FM sine with modulator ×8, E at 40 Hz, shift ×6 = 240 Hz, EQ wet to keep only above ~400 Hz, vocoder, two saturators, rhythmic delay and a wash reverb; automate shifter/vocoder for performance.
- Iterate non-linearly: revisit earlier FX settings after adding later ones.

### Hybrid-score 'sonic signature' chain for any source (orchestral rips, vocal phrases, synth presets, percussion loops, creature SFX): pitch/formant shift → heavy saturation → low-pass with a key-tuned resonant peak → EQ/compression → delay → reverb pushback, plus panning and LFO movement so the result blends behind an orchestra
Source: [Sound Design Tips From an Orchestral Composer](https://www.youtube.com/watch?v=E8b_N1RBCxE) · was `hybrid-score-five-stage-transform-chain-pitch-formant-heavy-saturation-key-tuned-peak-lp-pushback`
- Pick a source (brass or woodwind rip, vocal phrase, synth preset found by auditioning many, percussion loop or creature SFX). Audition it dry.
- Pitch stage: shift pitch and/or formant (example +2 st pitch, formant −12; or transpose a vocal −12). Optionally mix in a robot/lo-fi mode with the dry/wet control.
- Distortion stage: an aggressive saturation/'punish' mode cranked, or a clipper preset, until the sound is gnarly.
- Filter stage: low-pass to cut the analog top end and leave room for low instruments, with a resonant peak at the cue's key (or ~500 Hz on percussion). Several filters in a row or a resonator bank can carve further; add an LFO to filter frequency for movement.
- Tone/dynamics: EQ (tame low-mid boxiness, lift highs if needed), light compression for loudness; on hits add subharmonic reinforcement.
- Space: add delay, then reverb (plate/hall/large) to push the sound back; add an auto-panner with a mix knob for movement rather than a static patch.
- Record parameter tweaks as automation while performing, and keep the version that best fits the character, place or story.

### Spectral warp modes: vocode, formant scale, harmonic stretch, smear
Source: [The ULTIMATE Guide To Master Vital - Spectral Warp Modes](https://www.youtube.com/watch?v=iqrPF8t72sU) · was `spectral-warp-vocode-formant-stretch-smear`
- Load a rich wavetable (complex/harmonic content). Open oscillator spectral warp / formant-style effect slot.
- Try vocode: shifts formants in a key-tracked way so formant character stays steadier across notes — good for vocal/vocoder-ish WT pads and text-to-speech tables without wild pitch-of-formant jumps.
- Compare formant scale: moves harmonics/formants more exaggeratedly than vocode while keeping relative harmonic structure, but without the same key-tracking steadiness — stronger vowel changes, more note-to-note timbre shift.
- Use harmonic stretch for even, patterned spectral expansion; modulate with LFO for spacey acid / high sci-fi alarm motion. Switch to inharmonic stretch for uneven metallic/bell/crystal textures and aggressive growls.
- Use smear as a spectral high-pass / additive smear: table starts at the bottom of the control and spreads harmonics upward until the sound thins/smears out (Razor/Harmor-like). Good for whippy high-pass spectral gestures.
- For cinematic pads: pick one warp mode, set modest amount, LFO or envelope the warp (and optionally WT position); follow with filter → chorus → delay → reverb. Avoid stacking every mode at once.

### Vocoder as an insert effect on any synth patch: the patch itself is the carrier and a microphone is the modulator, with mode (clean, vintage, narrow, gated), decay, formant (neutral or higher) and dry-mic controls, placement in the effects chain (before or after distortion and chorus), arpeggiated carriers and a slow square LFO on formant
Source: [The Minifreak Vocoder is Awesome!](https://www.youtube.com/watch?v=MjijB6ExetI) · was `vocoder-as-insert-fx-any-patch-carrier-mic-modulator-mode-decay-formant-dry-mic-slot-order-arp-square-lfo-formant`
- Start from an init patch or any existing preset. Put the vocoder (external input) in a free effect slot, replacing a less important effect such as EQ or delay if needed. Connect a microphone to the audio input.
- Pick the vocoder mode (clean, vintage, narrow, gated). Set decay for how long the bands hang on, formant at neutral or a bit higher, and the dry-mic amount to taste.
- Make the carrier rich: e.g. oscillator 1 a plucked-string type, oscillator 2 a 2-operator FM type; or a mono virtual-analog patch an octave down with filter-envelope movement. Use unison or mono as needed and play lead lines with pitch bend.
- Try different slot positions: vocoder first, then distortion, then chorus after the distortion; or vocoder after a chorus and distortion carrier. Add a long reverb after.
- Turn on the arpeggiator with a held chord so the vocoded voice is re-triggered rhythmically.
- Modulate formant with an LFO: square shape, slow rate, deep (even maximum) depth. Reduce unison spread if the result gets too smeared.
