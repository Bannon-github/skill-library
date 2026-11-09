# Filter design: types, resonance, key-tracking, filter banks and envelopes

Goal: Choose and drive filters musically: LP/BP/HP/notch morphing, ladder/diode/comb flavours, resonance, key-tracking, velocity and envelope amount, parallel/serial and multi-band filter banks, talking/formant filtering and sample-rate reduction.

**Theory:** Subtractive synthesis removes harmonics from a rich oscillator; slope (12/24 dB/oct) sets steepness; resonance boosts the cutoff band (self-oscillates at high Q); cutoff = base + env*amount + keytrack*note + LFO.

**Hear it:** `sample-lab/theory/subtractive_filter.py`

## Workflow
1. Start with a rich oscillator (saw/square/noise).
2. Choose type: LP for warmth, HP to thin, BP for focused/telephone, notch/comb for hollow; ladder = fat/rounded, diode = squelchy.
3. Set cutoff and resonance (Q 0.7 neutral; 3-8 vocal/acid); enable key-tracking 50-100% so high notes stay bright.
4. Filter envelope: fast attack, decay 100-400 ms, sustain low for plucks; scale amount by velocity for dynamics.
5. Movement: LFO or stepped (S&H) modulation on cutoff, or morph LP->BP->HP->notch with an LFO.
6. Banks: 2-12 parallel band-passes with independent unsynced LFOs or a stereo step sequence for rhythmic pads.
7. Formant/talking: band-pass resonances at vowel formants, or resonant filter + sample-rate reduction for robotic speech.
8. Hear the theory: run `/home/box/audio-tools/bin/python sample-lab/theory/subtractive_filter.py` from the repo root and compare the sections; reuse its functions as a starting point for renders.

## Source techniques (merged, numbers kept)

### Organic alien comb texture: sub-audio saw click train → high-resonance filter → very short, high-feedback delay played by hand
Source: [Organic Alien Comb Filter Modulation Tutorial (Subtractive Synthesis)](https://www.youtube.com/watch?v=acM4NM4lH0k) · was `click-train-resonant-filter-feedback-delay-comb-texture`
- Init the patch. Use oscillator 1 only (osc balance fully to osc 1) with a saw.
- Turn the semitone/coarse knob all the way down until the saw becomes a click train where each tooth spike is audible.
- Use filter 1 only; lower the cutoff a notch and raise resonance to about 80–100%.
- Turn the delay mix all the way up, choose a very short delay time and very long feedback.
- Play with the delay time while sounds are running to sweep the comb pitch.
- Optional variations: add the synth's comb filter mode; add pitch modulation at a moderate speed.
- Reduce the delay slightly and add a little reverb on top.
- Do not modulate the filter: map cutoff (and FX parameters) to a MIDI controller via MIDI-learn and move them by hand while recording, changing timbre continuously.

### Stereo from mono: opposite filter frequencies plus inverse amplitude LFO
Source: [How to Make your Synthesizer Stereo](https://www.youtube.com/watch?v=02_MBQrqJS8) · was `dual-path-filter-spread-inverse-amp-lfo-stereo`
- Start from a mono voice (tutorial: two simple waves + white noise → mixer → HP/LP → envelope). Confirm it is centered.
- Frequency-spread stereo: put a filter (or filter pair) into a plus/minus or dual-cutoff mode and offset the cutoff so left and right emphasize different bands. This alone creates a static spectral stereo image.
- Duplicate the signal into explicit left and right amplitude paths after the envelope (or duplicate the mixer into L/R).
- Create a unipolar LFO. Multiply the left path by the LFO. Build the right modulator as inverse unipolar: multiply LFO by −1 then add 1 (or use 1−x) so when left is loud, right is quiet and vice versa. Multiply the right path by that inverse.
- Alternate simpler wiring: two attenuators on L and R modulated with opposite depths from the same LFO. Compare against the multiply version — both yield opposite-amplitude stereo.
- Audition in stereo and mono. Reduce spread or LFO depth if mono pumps or hollows. Combine later with gentle M/S EQ if lows got too wide.

### Filter design flavors: ladder, diode, comb, formant
Source: [Vital's Filter Types Explained | Sound Design Tutorial](https://www.youtube.com/watch?v=XvA4wRZsLsE) · was `filter-ladder-diode-comb-formant-flavors`
- Start with standard modes: low-pass, high-pass, band-pass, notch, peak. Note 12 vs 24 dB slopes; many multimode filters morph LP↔BP↔HP (or LP/HP via notch) with blend.
- A/B design flavors at same cutoff with LFO on cutoff: raise drive then resonance. Ladder/analog tend similar (ladder often more resonant); ‘dirty’ grit scales strongly with drive; digital may sound harsher or sometimes smoother/controlled.
- Try diode model (historically EMS workaround vs Moog transistor ladder; famous in TB-303 acid). Expect different resonance scaling—re-adjust resonance when switching from ladder.
- Formant filters: use XY-style controls for vowels (A/O/I/E or A/I/U/O sets); peak strength, spread between peaks, and formant transpose (pitch of the formant structure).
- Comb: duplicate + tiny delay + remix → peak/null series. Enable key tracking aligned to pitch to shape harmonics; type semitone offsets carefully to avoid inharmonic chaos unless desired. Resonance can go ±; useful for phasing/flanging-like motion and physical-ish string tones.
- Self-oscillation: with enough drive+resonance, ladder/analog/dirty/diode (and comb when tuned) can keep sounding after the osc dies if the note is held; digital/formant typically do not. Use for singing filter tones or comb pluck realism.
- Phaser-like filters resemble sparse combs; set pole/notch count via blend, reshape with resonance, add cutoff modulation for classic sweep. Pick model by ear for bass/lead/pad roles.

### noise and audio-rate filter texture lead
Source: [TRAVELER Track Walkthrough by Venus Theory](https://www.youtube.com/watch?v=jLGz5wq2CRE) · was `keysol-venus-noise-audiorate-filter-texture`
- Layer two fairly separate saw oscillators plus a wavetable osc for character. Slightly detune one osc; further detune can yield ring-mod-like artifacts.
- Optionally enable continuous Osc2 → low-pass cutoff (audio-rate-ish FM-of-filter) for granular grit; A/B it to hear the instability.
- Mix noise around ~30%. Map mod wheel to send noise into LPF cutoff modulation — annihilating cutoff with noise yields extremely unstable/distorted color.
- Use aftertouch (or pressure) to bring in a high-frequency oscillator for resonant overtones that feel like distortion byproducts when played low.
- Play as lead, texture, or pre-scare sting; leave headroom — this patch is intentionally unstable.

### Morph filter: LFO-cycle one filter continuously through LP → BP → HP → notch → LP
Source: [Why does nobody use this filter ? (Ableton Morph Filter Tutorial)](https://www.youtube.com/watch?v=Z4mMGSg6ebY) · was `morph-filter-lp-bp-hp-notch-lfo-cycle`
- Select the morph filter mode. Understand the morph control: 0 = low-pass leaning toward the next shape; at 100 it is fully bandpass, then it continues to highpass, then notch, then back toward low-pass.
- Set the slope to 24 dB and add a bit of resonance so the shape changes are clearly visible/audible while sweeping morph by hand.
- In the mod matrix route LFO1 → filter morph at 100%, then pull the LFO amount back into the 20–80% range. Turn retrigger OFF so the motion continues across notes.
- Pick the LFO rate: slow for pad movement, faster or tempo-synced for rhythmic motion. Then adjust the morph default position, cutoff frequency, LFO amount and rate together to find the sweet spot.
- Use the second filter slot as a static classic low-pass after the morph filter to keep the tone in check while the morph adds movement.
- Optionally add LFO2 → cutoff frequency (subtle), or replace filter 2 with a second morph filter whose morph is driven by LFO2 (try a different waveform).
- For percussive/noisy or robotic repetitive sounds, apply the morph filter with a different LFO waveform and rate to smooth the sound.
- Add a small amount of per-note Random (MIDI/mod matrix) to the morph amount/position so each note lands on a slightly different filter shape; A/B with the filter bypassed.

### Build subtractive 'architectures' from operator pairs: six oscillators with their own envelopes, or three oscillator→own-filter blocks (LP / LP+sub / fixed-frequency HP) into a master bandpass, FM pairs into filters, and series HP→LP
Source: [I Tried Building an Analog Synth Inside the Opsix…](https://www.youtube.com/watch?v=X4TPAWQw4ss) · was `operator-osc-filter-pairs-three-filters-into-master-fm-into-filter`
- Architecture A: choose an algorithm where all six operators are carriers (none modulating each other). Osc 1 = saw (HD/brighter version), osc 2 = saw an octave lower with some detune. Give both full sustain; soften the lower one's attack so it enters more slowly, and add release.
- Osc 3 = square with an LFO on pulse width (use a spare LFO, set to taste). Osc 4 = bright, higher saw with a sharp attack envelope for bite. Osc 5 = triangle with width adjusted and some self-feedback (pushing it toward saw), used as the lower layer.
- Osc 6 = noise with a slow envelope, and an LFO on its level so it comes in and out.
- Master filter: lower cutoff, add filter-envelope amount and resonance, a slight LFO on cutoff and key tracking (cutoff opens up the keyboard). Add exciter, auto-pan and an old-school spring reverb.
- Architecture B: pick an algorithm with three carrier/modulator pairs. Turn each carrier into a filter (its own oscillator level down) fed by its modulator set to saw. Block 1: MS-20-style low-pass with resonance, cutoff modulated by its envelope with velocity intensity.
- Block 2: another LP fed by a saw, this time keeping the filter operator's own sine mixed underneath. Because the filter's oscillator follows the pitch section, it can act like a sub oscillator (drop its pitch); detune the source slightly.
- Block 3: high-pass filter (own mix off) fed by a square, with the filter switched from ratio (key-tracked) to fixed frequency and set by ear for strings, and an LFO on the square's PW.
- Send all three blocks into the master filter set to band-pass with its own filter envelope.
- FM into filter: change an algorithm so a modulator stacks on an operator that feeds a filter (sine modulators), giving FM spectra into the analog-style filter and then the master filter (try HP or BP on top). For classic layouts, run two oscillators in series through HP then LP (MS-20-like), or a single oscillator into one filter (Polysix-like).

### Parallel filter chains for rhythmic pad motion
Source: [Make basic sounds interesting with parallel processing!](https://www.youtube.com/watch?v=i4ZZwzxTpf0) · was `parallel-filter-rhythmic-pad-chains`
- Start from layered pad material (body + harmonic spice + optional melodic layer). Route the group into a parallel FX rack rather than only serial inserts.
- Create a chain with two filters in parallel mode (example: low-pass on filter 1, band-pass on filter 2) so each path emphasizes different bands simultaneously.
- Drive both cutoffs from a tempo-synced rhythm/LFO shape (example: 1-bar custom shape, BPM-synced). Let the two filters move separately so motion is stereo/spectral, not a single sweep.
- Expect overlapping bands to stack in level; follow with a compressor on the parallel bus to squash volume spikes from constructive overlap. Prefer fixing sources when possible; bus compress is a lazy safety.
- EQ after the parallel filters to remove excess low end created by the stack. Optionally add further parallel chains (saturation, etc.) that may overlap bands—keep compressor/EQ as glue.
- Optional stereo trick from transcript: when a rhythm modulator supports stereo shapes, set phase/offset between L/R so upward ramps become opposing L/R motions for width.

### Talking/vocal formant voice from a resonant filter into sample-rate reduction (sweet-spot aliasing formants)
Source: [Creating a vocal formant speaking voice in VCV Rack](https://www.youtube.com/watch?v=gzJEQiTC_SQ) · was `resonant-filter-sample-rate-reduction-talking-formant`
- Patch a harmonically rich oscillator into a filter and add a healthy amount of resonance.
- Send the filter output into a sample-rate reduction stage (bit-crusher with sample-rate reduction) after the filter.
- Slowly sweep the sample-rate reduction amount (and cutoff) to find the sweet spots where formants appear and the sound starts to 'talk'.
- In a patch: sequence the rich oscillator, modulate the filter cutoff with a tempo-synced LFO, and use a step sequencer to change the LFO's rate multiplication per step.
- Slowly and randomly modulate the sample-rate reduction amount for different timbres; bring the reducer's wet signal up gradually.
- Send only the high frequencies (around 1500 Hz and above) through a delay as an extra layer.

### Animate a static pad with a stepped 12-band stereo filterbank: assign groups of bands to sequencer patterns (offset ups vs a big down note), set a Q slope with wider low bands and narrower high bands, tame resonant peaks with mild drive plus smoothing compression, alternate bands L/R for width, and use per-band versus group random triggering
Source: [Philtor 12 Band Sequencer Filter](https://www.youtube.com/watch?v=Py4XQbjvn4o) · was `sequenced-stereo-12-band-filterbank-rhythmic-pad-q-slope-lr-alternation-random-trigger`
- Insert the 12-band stereo filterbank on a static pad and use the band volumes as an EQ, turning down only the bands that are too much.
- Raise the global Q from fully open (no contour) until the bands become pointed, and apply a slope so low bands are wider and high bands narrower.
- Add a little drive and set the compression/'pull' control negative so peaks are smoothed without much distortion.
- Assign the first five bands to a step pattern; then unassign them and give three frequencies an offset pattern of up notes; finally give the last bands a single big down note.
- Alternate bands between left and right (flip-flop) for stereo spread, choosing the assignment that works in the mix.
- Enable random triggering: per-band mode makes each band trigger independently (subtle, dense); grouped mode makes grouped bands fire together (sparser, more extreme). Fine-tune band volumes to contour the result.

### Buchla 291-style morphing bandpass: 6-pole bandpass with two clocked step sequencers (frequency and bandwidth) as filter snapshots, wet/dry crossfader
Source: [How to make your own Buchla Style Morphing Filter in VCV](https://www.youtube.com/watch?v=NFWAC2kLqvo) · was `six-pole-bandpass-stepped-freq-bandwidth-snapshot-morph`
- Choose a multimode filter, set it to bandpass and the slope to 6 poles (type the value precisely); set bandwidth to 100%.
- Feed a complex oscillator; brighten/complexify it and raise the pitch until the bandpass has harmonics to work with. Sweep bandwidth to hear the change.
- Add two step sequencers: one to filter frequency (v/oct), output range ±10 V; one to bandwidth, range 0–10 V.
- Put a crossfader after the filter: filtered signal on A, dry signal on B, so the filter acts like an aux/wet-dry morph.
- Clock both sequencers, randomize all steps, set 8 steps forward, and run: each step recalls a different frequency+bandwidth 'snapshot'.
- Adjust main frequency/bandwidth controls live and optionally modulate main frequency with an LFO via CV.
- For a triple morphing filter, duplicate the whole voice (filter + two sequencers) and offset settings.

### dual stereo filter and LF-width imaging
Source: [TRAVELER: The Cinematic Hybrid Synthesizer | Official Walkthrough](https://www.youtube.com/watch?v=IU76c2Cygs4) · was `traveler-walkthrough-stereo-ladder-lf-width`
- Choose ladder-style LPF slope from gentle 6 dB to steep 24 dB (four ladder variants) OR NJM 2069-style model for DW/Poly-era character.
- Enable stereo filter path. Offset left vs right cutoff, or use automatic per-key spread, for subtle stereo timbre differences (good automation target).
- Add dedicated high-pass; optionally link HP to primary cutoff for band-pass style sweeps. Set keyboard tracking and envelope amounts for both LP and HP.
- Output section: set pan-spread so successive voices fan across the stereo field; optional random voice position.
- Engage low-frequency width / LF-width: narrow pan of content below ~middle C so bass stays mono-centered while upper spectrum keeps stereo motion.
- Optional vintage/voice-offset knob for slight per-voice drift of tune, mixer, filter, envelopes — keep near 0 for clean cinematic pads.

### Three-band parallel bandpass filter-bank pad with offset, unsynced cutoff LFOs
Source: [Sound Design 53: Pads 3 Bandpass](https://www.youtube.com/watch?v=L0IXE_whmso) · was `triple-bandpass-bank-unsynced-lfo-pad`
- Route oscillator 1 into filter 1, filter 2 and filter 3 in parallel, each also sent to the output. Change oscillator 1 from sine to saw.
- Set all three filters to bandpass with a little resonance: filter 1 low frequencies, filter 2 mids, filter 3 highs.
- Give it a pad envelope: slow attack, sustain, long release.
- On filter 1 cutoff add a slow LFO (global). Copy it to filters 2 and 3 but change the value/start slightly so they don't start the same or synchronize.
- Enable oscillator 2 an octave lower, also into all three filters, with the same pad envelope; nudge its speed slightly so the oscillators don't move too evenly.
- Add unison ~7 voices, raise volume/bass as needed; resonance amount and output mix are to taste.
- Add chorus for thickness and a long-decay reverb; play chords or a single sustained note.

### Velocity into filter cutoff / filter-envelope amount
Source: [Adjusting Velocity to Filter Cutoff – Synth Clips 7 – Daniel Fisher](https://www.youtube.com/watch?v=cWPfqPwXBos) · was `velocity-filter-cutoff-envelope-amount`
- Init: single bright oscillator (e.g. saw), 24 dB/oct LP, resonance off, filter EG amount 0, keytrack 0. Sweep cutoff to hear range (can go below fundamental).
- Set cutoff to the darkest tone you want when the envelope is not pushing (EG amount still 0).
- With sustain-full filter envelope, raise EG amount until held notes reach maximum intended brightness (hard-hit ceiling).
- Enable velocity→filter (or velocity→filter EG amount). Learn polarity: typical = harder = brighter; some synths (Subsequent/Sub 37 style) increase velocity sens to make soft playing darker instead—strategy reverses.
- Play slow soft velocities while raising velocity amount until darkest desired soft tone; verify fast hits still hit the bright ceiling. Trim EG amount if hard hits are too bright; resonance exaggerates the difference.

### NOOF cinematic synth pulse (Noise, Osc, Osc, Filter): white noise + mono saw + saw an octave up with 5 slightly detuned unison voices, all into a fully closed ladder low-pass opened per note by a fast envelope on an eighth-note MIDI line; automate cutoff as the single energy control
Source: [Use this 4 step formula to create epic synth pulses in any synth: Serum, Phase Plant, Pigment, Vital](https://www.youtube.com/watch?v=VhjJlD0Gck0) · was `noof-synth-pulse-noise-saw-octave-unison-saw-closed-ladder-env-cutoff-energy-macro`
- Noise: enable a white-noise oscillator at a low level as a small burst of energy on top.
- Osc A: default saw, one voice.
- Osc B: saw pitched one octave up, slightly detuned against osc A, unison about 5 voices with a little detune spread.
- Route all three into one ladder low-pass with cutoff fully down. Route envelope 2 (retriggered on each MIDI note) to cutoff with a fast attack and quick decay, so each eighth note opens the filter briefly and it falls straight back.
- Automate cutoff through the cue: low = plain pulse (noise and osc B barely audible); higher = osc B width and detune come through; highest = noise burst power on top. Use this single lane to add or remove energy.
- Check that muting noise or osc B matters a lot at high cutoff and little at low cutoff. Add effects on top only after the core works.
