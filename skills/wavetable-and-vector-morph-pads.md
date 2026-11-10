# Wavetable, vector and wave-sequence morphing for evolving pads

Goal: Create pads and textures whose timbre evolves by modulating wavetable position, crossfading two or four sources (vector/XY), or sequencing waves, instead of relying on a filter.

**Theory:** Each wavetable frame is a different harmonic spectrum; sweeping position changes the spectrum continuously (spectral motion). Crossfading sources mixes spectra; true morphing interpolates parameters.

**Hear it:** `sample-lab/theory/wavetable_morph.py`

## Workflow
1. Choose two contrasting tables or sources (dark/bright, vocal/metallic) on Osc A and B, often an interval apart (octave, fifth).
2. Modulate wavetable position with a slow LFO (4-16 bars), an envelope (bright attack -> dark sustain) or random smooth LFO.
3. Vector/XY: crossfade 2-4 oscillators with two slow LFOs at unrelated rates so the blend never repeats exactly.
4. Wave sequence: step through 4 waves either crossfaded (pad) or hard-switched to tempo (rhythmic).
5. Keep pitch steady (no wobble) unless asked; let modulation depth be macro-controlled with capped ranges so randomizing never breaks the patch.
6. Add filter only to tame top end, then chorus/reverb.
7. Hear the theory: run `/home/box/audio-tools/bin/python sample-lab/theory/wavetable_morph.py` from the repo root and compare the sections; reuse its functions as a starting point for renders.

## Source techniques (merged, numbers kept)

### From-scratch spectral-morph wavetable ambient pad
Source: [Ambient Pads in Vital From Scratch](https://www.youtube.com/watch?v=ImWJixBPZj0) · was `ambient-wavetable-scratch-spectral-morph-pad`
- In WT editor: start from sine; remove extra keyframes; add harmonics gradually; duplicate end frame; spectral-blend; alter phase/harmonics on the end frame so position morphs soft→complex.
- Synced LFO (e.g. 4 bars) → wavetable position at high depth so the custom table evolves.
- Second osc: draw/warp another shape; optional harmonic-stretch randomized slowly; unison with octave-stack mode at low detune (~3–4%).
- Amp env ~4s attack / ~6s release; optional curve bend.
- Dual filters (e.g. osc1 LP 12 dB, osc2 HP) with env→cutoff; randomize stereo-split/phase for width.
- Optional sample osc: original garage/Foley texture pitched −1–2 octaves, low level.
- FX: multiband compress for air → dotted delay with feedback → reverb time ~10–11s; bipolar random → pan on oscs for width.

### Multi-envelope oscillator-level morphing pad
Source: [This One Technique Changes EVERYTHING // Vital Pad Sound Design Tutorial](https://www.youtube.com/watch?v=AYVmdcgKt_s) · was `cinematic-multi-envelope-osc-level-morph`
- Lengthen the main amp release (~5s) so held chords trail instead of cutting off.
- Enable all target oscillators but set their levels to zero.
- Convert LFO1/2/3 (or dedicated envelopes) to envelope mode; draw distinct ADSR-like shapes with different attack times; route each to one oscillator’s level.
- Optionally octave-shift and pan layers so the staggered entries are obvious while designing.
- Assign different filters (e.g. one ladder vs another) to subsets of oscillators; reduce resonance; let early layers swoop while a late layer arrives darker/brighter.
- Add noise/sample with its own short attack–release envelope to level; optionally direct-out before main FX for drama.
- Animate wavetable position with synced LFOs; add mild unison/spread on select oscs; optional random bipolar pan.
- Finish with long ambient delay/reverb (tutorial example: long room ~tens of seconds decay) on a send or insert.

### Digital wavetable pad with series filter, chorus, echo, space
Source: [Arturia Pigments: Creating A Digital Pad](https://www.youtube.com/watch?v=e1ZQssAW7R0) · was `digital-wt-morph-bandpass-chorus-echo-space`
- Engine1 wavetable (additive/gentle digital): set mid position; env2 → WT position with long attack, slow decay, high sustain, long release.
- Amp/VCA env: attack ~2.8s, full sustain, release ~5s+.
- Unison classic ~3 voices, stereo 100%, detune ~1.5–2%.
- Engine2: basic sine WT, unison ~3 / stereo 100% / ~1% detune; blend under the bright digital engine for weight.
- Series filters: LP24 (cutoff low hundreds Hz, light resonance, key follow ~0.4) then HP12 (~50 Hz); both cutoffs also from env2 so morph opens LP while HP removes some sine weight over time.
- Velocity → amp slightly for playability.
- Insert Juno-like chorus (slow rate ~0.25 Hz, depth a few ms, phase ~180°); send to aux: chorus copy → tape/ping-pong echo (e.g. 1/4, ~50% wet, feedback ~0.35) → 100% wet long reverb (long predelay/decay, damping, HP/LP).

### Dual-layer opposite-rotation vector morph pad with filter-drive LFO
Source: [Synthmaster Tutorial - Vector oscillator "monster pad"](https://www.youtube.com/watch?v=6aRgJoBxk4g) · was `dual-layer-opposite-vector-morph-pad`
- Create vector oscillator A with four contrasting portable waves in the corners; set pitch display to semitones. Keep all four corners at the same base pitch for a coherent chord tone.
- Park the XY near a musically useful corner (tutorial favored a top-side start). Assign one slow synced sine LFO (~4 bars) to both X and Y indexes with opposite polarities/amounts so the path orbits (left-right on one axis, up-down on the other) instead of only sliding on a diagonal.
- Copy oscillator A settings to oscillator/layer B. Pitch two corners ~+13 st (octave-ish) and another ~+25 st (two octaves) for depth/air while leaving structural corners nearer the base if needed. Invert the XY modulation directions so B orbits the opposite way (clockwise vs anticlockwise) from the same LFO.
- Shared pad amp envelope on both parts: long attack (pull attack curve back), decay ~9 o'clock, sustain as-is, release ~3 o'clock (release doubles as a soft tail). Lengthen attack further if the swell should feel glacial.
- One analog-style low-pass on the layer: moderate cutoff (~12–1 o'clock), no resonance, standard key track, tiny static drive. Modulate filter drive from a second synced LFO (triangle, different phase/rate than the vector LFO) with only a small positive depth so drive washes in gently.
- Optional: second envelope → cutoff with some decay and sustain at zero for a slow open that uses decay/release. Insert light ensemble on one FX slot; send master reverb (aftertouch→reverb amount is optional). Ride master volume down whenever drive/distortion is added.

### Dual wavetable voice with an interval-locked tune/detune pair and a per-oscillator 'animator' on position and level: Reese bass, phasing-in harmony, S&H atmos pad and level-ramp pluck recipes
Source: [Wavefinder Tutorial // Wavetable on Tonverk with OS 1.3.0](https://www.youtube.com/watch?v=ysMPHY5oiGc) · was `dual-wt-interval-locked-per-osc-position-level-animators`
- Load a wavetable on each oscillator and balance them with the level controls. Set an interval with osc-2 detune (e.g. +7 st = fifth); transpose the pair with tune and confirm the interval stays.
- Learn the per-osc animator: raise position depth to scan from the current base position on each note (negative depth scans backwards). Choose a one-shot envelope shape or a looping, tempo-synced LFO shape; set speed. The same animator can also drive level.
- Reese bass: identical saw tables, osc-2 detune ~15 cents (or ~10 for subtler beating), lower tune slightly to darken. Set both to similar start positions, then positive position depth on osc 1 and negative on osc 2 so they move in opposite directions, subtle depth, slow speed.
- Harmony lead: saw on osc 1 and a metallic FM-style table on osc 2, detune −5 st (fourth / inverted fifth). Put a ramp-up one-shot shape on osc 2's level at a slow speed so the harmony fades in. Scan the table first (this one gets brighter toward the end), start osc 2 partway in, and add positive position depth so it brightens as it enters. Osc 1 gets a slow, deep triangle loop on position plus a little level modulation from the same shape.
- Optionally layer the track LFO subtly on position, a subtle pitch-envelope bend, a low-pass filter effect with slow modulation, and a reverb send; sequence per-step changes of modulation speed/depth for rhythmic variation.
- Atmospheric pad: airy/hollow table on osc 1, noisy/aggressive table on osc 2. Tempo-synced sample-and-hold on osc-1 position (jumps each step), faster; S&H on osc 2 at a slower speed (use the random/smooth shape instead for gentle drift). Detune osc 2 to +19 st (compound fifth) and lower its level with level modulation. Modulate osc-1 position depth and S&H speed so the steps alternate between slow subtle moves and busy bursts. Add the LP filter effect and reverb. Each chord note gets its own modulation.
- Pluck: main sound on osc 2 with a looping ramp-down shape on level, medium speed, full depth and low base level for a quick decay. Set base position near the bright part with positive depth so each note starts from the softer tone (or the reverse for a bright attack); compensate lost energy with overdrive. Layer a noisy table on osc 1 with the same level shape and speed. Use a long amp decay/release for a delay-like trail, then reverb and an LFO on pan.
- Texture variant: load a sample (vocal, field recording) in place of a wavetable and pitch it down a few octaves; the same tune/position/modulation tools give a glitchy texture.

### Four-layer wave-sequenced cinematic pad: crossfaded seconds-based wave sequence, released keys layer, LFO-rate-modulated analog layer, tempo-locked rhythmic step layer with shape/ratchet/probability
Source: [Wavestate Cinematic Pad in Minutes](https://www.youtube.com/watch?v=28uxHnQbulE) · was `four-layer-wave-sequence-cinematic-pad-crossfade-vs-rhythmic`
- Layer 1 (smooth wave sequence): choose 3–4 string-like sources moving from acoustic chamber/orchestral strings toward a synthetic string; set step time in seconds (~1 s per step) with crossfade on so each source melts into the next.
- Layer 1 envelope + FX: slower attack, some release, lengthen crossfade slightly; add compression, tape delay and master reverb (chorus not needed).
- Layer 2 (keys): a single piano/keys source with a long, nice release; optionally lower cutoff with a release-shaped filter envelope, make it velocity-sensitive, add a different delay. A phaser was tried but softened the attack — compression worked better to give the keys impact over the strings.
- Layer 3 (analog-style): wave-sequence between two different saw sources for variety; filter with filter envelope and tape delay.
- Layer 3 motion: route a free-running LFO to the layer (e.g. filter/level), then use a second, very slow free-running LFO (the spare pan LFO) to modulate the first LFO's speed so it speeds up and slows down; use that slow LFO also for a tiny pitch deviation and for panning.
- Layer 4 (rhythmic): new wave sequence in tempo mode (quarter notes, speed up later) through synthetic/spectral and vocal-like sources; turn crossfade off so steps are audible.
- Shape the steps: give the step lane a saw-down shape (a pulse of 100 that decays to 0 = pseudo-envelope per step), lower cutoff and apply the step shape to cutoff; add double/triple ratchets on some steps and lower their probability so it isn't jarring; add a tempo-synced filter LFO and interesting delays.
- Key-sync the rhythmic layer's steps so chords start in sync; optionally jump the last step up one or two octaves.
- Balance: bring the busy analog layer down, map it (or the rhythmic layer) to a macro knob for real-time control.

### Four-source morph engine: an XY/linear crossfade (centre = all four mixed, corners = one source) versus true parameter morphing of analysed (additive + spectral) sources, where the centre is a composite sound, with separate morph positions per element (additive, spectral, pitch, formant, analysed envelope), each driven by its own LFO type
Source: [Logic Pro Advanced Tutorial : Morphing with Alchemy](https://www.youtube.com/watch?v=HXKz89TIlJI) · was `four-source-morph-xy-crossfade-vs-true-parameter-morph-analysed-sources-per-element-additive-spectral-pitch-formant-envelope-lanes-separate-lfos`
- Init a patch, enable four sources with different waveforms and slightly different tuning, and choose XY crossfade. Move the XY point: centre plays all four, each corner plays one; try linear crossfade (X only: A-B, B-C, C-D). Optionally put a complex LFO on the XY point.
- Re-init and import four contrasting sustained samples (drone, ghostly texture, atmospheric event, sustained vocal) as additive + spectral sources at similar pitch; wait for time alignment after each import.
- Switch to morph XY with all elements linked and play a note; move between A, B, C, D and the centre.
- Keep auto-align on; try fixed pitch off for a smoother morph and back on if the pitch wanders too much.
- Split by element: reset all element points to centre, then move only the additive point; then spectral, pitch, formant and envelope (the samples' analysed envelopes, not the AHDSR). Per source, randomise morphable additive knobs, enable a spectral processor (e.g. metallize) on some, and shift formant settings so the sources differ.
- Try morph linear: X only between A and B, C and D, or across all four.
- Return to morph XY and assign a different LFO to each element point: slow smooth on additive, very fast on spectral, stepped on formant, smooth on another; raise each depth. Keep moving the centre manually. Add reverb on the whole patch.

### fifths-tuned pulsar hybrid impact
Source: [TRAVELER Track Walkthrough by Venus Theory](https://www.youtube.com/watch?v=jLGz5wq2CRE) · was `keysol-venus-fifths-pulsar-wt-impact`
- Build throbbing aggressive core on Osc1 (pulse/saw). Set Osc2 +7 semitones for fifths power; balance for deep power vs mid punch vs brighter transient emphasis.
- Enable duo/unison, detune, and stereo scatter/spread for width.
- Add wavetable oscillator not as a full replacement but as dimensional spice; animate WT position for movement.
- Play velocity-reactive syncopated rhythms into a bouncing delay so the part stays alive across long phrases.

### high-pitch wavetable artifact over pulse sequence
Source: [TRAVELER Track Walkthrough by Venus Theory](https://www.youtube.com/watch?v=jLGz5wq2CRE) · was `keysol-venus-high-wt-artifact-pulse-layer`
- Build a classic pulsating bass sequence: pulse/saw bed, Control Track or LFO → filter cutoff, use filter feedback/saturation/drive for grit and presence.
- Add wavetable oscillator tuned very high until it reads almost as an artifact rather than a clear tone.
- Modulate wavetable position slowly (LFO or Control Track) for continuous micro-variation so the sequence never feels static.
- Mix WT low under the pulse bed; A/B with WT muted to confirm it adds interest without dominating.

### Self-evolving wavetable pad rack you can safely randomize: two formant-style wavetable oscillators (-1 and -2 octaves) through serial 12 dB low-pass and high-pass filters on one macro, an internal matrix where envelope 2 drives both wavetable positions and envelope 3 drives envelope 2's attack, plus an external slow triangle LFO that pushes the amp envelope times in opposite directions, with ADSR excluded from macro randomization
Source: [Step-by-Step Guide: Beautiful Wavetable Pads (Ableton Live 12)](https://www.youtube.com/watch?v=yZjQ2e4IREI) · was `macro-randomizable-evolving-wavetable-pad-two-formant-wt-oscs-minus-1-and-2-oct-serial-12db-lp-hp-macro-env2-to-wt-positions-env3-to-env2-attack-external-triangle-lfo-opposing-adsr-offsets-unison-shimmer`
- Create a rack on a MIDI track and expose all 16 macros; insert the wavetable synth.
- Osc 1: formant/voice wavetable at -1 octave; enable osc 2 with a darker formant wavetable at -2 octaves; enable the sub; set synth volume to about -12 dB; unison mode 'shimmer' with 4 voices.
- Enable both filters as 12 dB types in serial (low-pass then high-pass), drive about 2 dB and 1 dB.
- Matrix: env 2 → osc 1 position 50, osc 2 position 75; LFO 1 → both positions 15; env 2 → filter 1 freq 10; LFO 1 → filter 1 freq 3; env 3 → env 2 attack 100; LFO 1 → env 2 sustain 50; env 2 → filter 2 freq -2. LFO 1: sine, retrigger off, slow.
- Map macros: osc 1 position, osc 1 warp, osc 1 fold, osc 2 position, osc 2 effect, osc 2 transpose, filter frequency (both filters on one knob), resonance (both), amp/env 2/env 3 ADSR, mod rate (LFO rate), mod amount, mod shape, shimmer amount.
- Add an external LFO after the synth, set to triangle at a low Hz rate; map its rate/depth to the mod-rate/mod-amount macros. Map it to filter frequency (50), amp attack (-60), decay (+30), sustain (-40), release (+40), osc 1 warp (50), osc 1 fold (20), osc 2 effect (50).
- Add a limiter last as a safety against level jumps.
- Exclude the ADSR macros from randomization, press randomize until a pad you like appears, and save each as a snapshot; save the rack.

### Per-voice, per-parameter random value drawn at each note-on (many synced sample-and-holds): offset compensation for bipolar values at a parameter's minimum or maximum, unison/chord voices that each get different timbre, random envelope times on an arpeggiated FM pluck, per-voice morph between two cloned-then-edited parts, and per-voice random LFO rate with depth brought in by aftertouch
Source: [Magnolia Polymove Explained: The Ultimate Randomization Tool](https://www.youtube.com/watch?v=X_zozWSx-RU) · was `per-voice-per-parameter-note-on-random-values-bipolar-offset-compensation-unison-chord-variation-envelope-times-morph-two-cloned-parts-per-voice-lfo-rate-aftertouch-depth`
- On an init patch set the wavefolder about halfway and assign the per-voice random source to it. Play repeated notes.
- Add through-zero FM as a target with its base at 0; then move the base up to compensate for the bipolar range.
- Set unison (e.g. 8 voices, mono) or chord mode and play.
- Add the filter cutoff as a target; with the filter fully open only negative draws act, so lower the base.
- Build a plucky FM patch with an up/down arp over two octaves at a lower tempo; randomise envelope times, then a little wavefolder, filter, resonance and filter-envelope amount.
- Add a tempo-synced ping-pong delay and randomise its mix or time.
- Clone part A to part B, change several parameters on B, set morph halfway, and randomise the morph.
- Set a unipolar saw LFO on the wavefolder or FM amount, randomise its rate per voice, set LFO depth to zero and map aftertouch to depth.

### Three-layer pad/key with independent envelopes plus pitch-aware (key-ratio) ring mod, frequency shift and an octave-up granular 'cloud', each brought in by a macro whose maximum is capped
Source: [Absynth 6  - Design a Patch From Scratch | Layers, Clouds, Macros & Note FX #absynth6  #sounddesign](https://www.youtube.com/watch?v=Rdt5Alxrg60) · was `three-layer-pad-key-tracked-ring-shift-cloud-macros-capped-ranges`
- Layer A: load a looping stereo synth sample (loop on). Give it a very long attack (seconds), with subtle per-segment envelope slope changes. Layer B: sine oscillator (with a little unison detune) with a tiny attack so it isn't sharp, then decay so it dies away while A swells in. Layer C: another looping sample with an immediate attack, sustain and some release.
- Balance levels: if a layer is too soft, add a waveshaper for gain/harmonics and a gentle high-pass to remove excess lows from the deep layer.
- Ring mod on all three layers in ratio mode, ratio 2 (the modulator is placed at 2× the played note's frequency). Set each layer's mix around 60% (they needn't be identical) and assign all three mixes to one macro named 'ring' so 0 = no ring mod and maximum = ~60%.
- Main filter: low-pass on the whole sound; add a very slow LFO (seconds-based) on the cutoff of the second filter slot.
- Cloud on layer A: add a granular cloud, set its pitch exactly one octave up, add slight random pitch for chorus-like detune, and put its mix on a macro capped at about half.
- Frequency shifter on the sine layer B: Hz mode at a slow value (e.g. 5 Hz) gives a rhythmic sway, or ratio mode adds a higher harmonic (ratio 2 gets dirty quickly). Cap its macro at ~50%.
- Assign main filter cutoff and resonance to macros 3–4, setting base values so the macros have the full range. Put FX-section wet on a macro, add only wet (don't trade dry), cap at about 0.25 and invert the mapping direction if it moves the wrong way.
- Performance finish: macros for layer volumes (A+C together vs B), increase the voice count for overlapping releases, keep velocity response gentle, and optionally let poly aftertouch drown layer A a little.

### control-track rhythmic filter and WT animation
Source: [TRAVELER: The Cinematic Hybrid Synthesizer | Official Walkthrough](https://www.youtube.com/watch?v=IU76c2Cygs4) · was `traveler-walkthrough-control-track-filter-wt-animation`
- Open sequencer/Control Tracks panel. Configure Track A: length ≤16 steps, direction forward or ping-pong, tempo-synced note value.
- Set Track A destination from the shared mod destination list (same as mod matrix): e.g. filter cutoff or wavetable position. Set depth, gate time, swing.
- Configure Track B with a complementary destination and optionally different length/rate for evolving polyrhythmic motion.
- Use utilities: copy A→B, reverse/flip, reset, or randomize steps when exploring — then refine by ear.
- Optionally pair with arpeggiator: many patterns; can target individual oscillators so one osc arps while another holds a pad; shape arp attacks with mod envelope when per-osc selected.

### wavetable morph plus filter motion patch
Source: [TRAVELER: The Cinematic Hybrid Synthesizer | Official Walkthrough](https://www.youtube.com/watch?v=IU76c2Cygs4) · was `traveler-walkthrough-wavetable-morph-filter-motion`
- Osc3 role: switch from analog waveforms to wavetable mode. Load an original/freely available WT (do not import Traveler proprietary tables).
- Optional: enable 2-voice stack, detune, and stereo spread on the WT osc for width.
- Optional drone mode: disconnect Osc3 from keyboard for a fixed-pitch layer, or use it as an extra LFO-rate modulator.
- Modulate wavetable position from LFO or Control Track; keep depth subtle for evolving texture rather than obvious sweeps unless desired.
- Stereo filter: ladder model (6–24 dB) or NJM-style; add HP that can link to primary cutoff for band-pass motion. Modulate cutoff from filter envelope and/or LFO.
- Mixer: balance WT vs analog oscs; add noise (white/pink) sparingly; light drive into filter.

### Vector synthesis: XY-blend four oscillators with nested crossfades
Source: [Vector Synthesis in Bitwig Grid with the Scrawl Oscillator](https://www.youtube.com/watch?v=SMB34GRgQWQ) · was `vector-xy-four-oscillator-crossfade-blend`
- Instantiate four oscillators. Load contrasting shapes into the four corners (e.g. sine, saw, a complex drawable, an odd/noisy shape). Keep pitches unified unless you intentionally detune later.
- Add an XY control set to bipolar mode so (0,0) is the center and each axis runs −1…+1 (unipolar XY only covers one quadrant and cannot reach all four corners).
- First vertical blends: mix top-left with bottom-left using the Y axis (positive Y favors the upper osc, negative the lower). Separately mix top-right with bottom-right with the same Y.
- Horizontal master blend: mix the left-column result with the right-column result using the X axis (wire X at full bipolar depth, e.g. ±50% into the blend if your modulator is bipolar).
- Verify interior points: center should combine all four; edges should be two-osc mixes. Contrast with a 1D wavetable scan that cannot jump sideways between non-adjacent frames.
- Finish with an ADSR (or similar) on the blended output level. Optionally LFO/automate X and Y slowly for evolving pads; keep mono compatibility in mind if later widening.

### Wavetable crossfade position + morph/PWM-style shaping
Source: [You Won’t Believe What the Modwave Can Do With Wavetables!](https://www.youtube.com/watch?v=yuHwGR1R7jY) · was `wavetable-crossfade-morph-modulate-pad`
- Load a multi-frame wavetable (e.g. saw→triangle→square→sine family). Enable smooth crossfade/interpolation between frames so in-between waves are audible; contrast with crossfade=0 hard switching for sharp digital hops.
- Assign LFO or other mod source to wavetable position/crossfade amount for evolving motion; keep depth musical for pads.
- Engage morph-style shaping: on pulse/square-like frames, morph acts like PWM; explore mirror, mirror-stretch/wavefold-like, narrowing (toward high-pass thinness) and window-narrow (toward low-pass softening).
- Optional vintage digital character: apply bit-resolution / stepped vintage modes (e.g. 8-bit buzzing overtones) and LFO them lightly for early-digital WT flavor through an analog-style filter.
- Finish with ladder/LP filter + envelopes, then EQ→chorus→delay→reverb for cinematic space. Prefer original/free tables—do not dump proprietary banks.

### Wavetable frames as an animated spectral EQ: each frame is a gain curve across the spectrum, with depth, floor, skew, smoothing, low-end bypass and per-channel time offset
Source: [Wavefield Tutorial Video](https://www.youtube.com/watch?v=VrCSssDOxFc) · was `wavetable-frames-as-animated-spectral-eq-curve-depth-floor-skew`
- Insert the processor on the source (or in parallel). Use a wavetable whose frames vary a lot. Each frame is read as a gain curve: left = low frequencies, right = highs.
- Set depth: 0 = unchanged; at maximum a frame peak/valley applies about ±12 dB to that frequency region. Lower depth for subtler curves.
- Set floor: lowering it stretches the negative (cut) part of the curve towards silence while boosts stay controlled by depth. Use low floor for deep notches or high-pass/low-pass/notch-style frames.
- Set skew to fit the source: negative spreads the shaping down into bass/low-mids (e.g. bass); positive concentrates it in the highs (hats, cymbals, airy pads).
- Raise smooth if sharp frames cause ringing/harsh artifacts (e.g. on vocals). Engage safe-bass (bypass below a set frequency, up to 400 Hz) on bass, full mixes or anything whose fundamental must stay solid.
- Choose the motion: trim start/end frames to the range with the character you want (re-adjust speed, since the trim becomes the whole cycle). Set speed (slow = evolving) or tempo-sync (e.g. 8 bars for slow cinematic evolution, quarter notes or faster for flutter). Pick playback forward, ping-pong, reverse, or random (jumps between frames at fixed intervals, beat-aligned when synced).
- For automation-driven motion, pin to a single frame and draw position automation to land spectral moves on specific moments in the arrangement.
- Draw your own table: up to 20 keyframes, interpolated to fill all frames (edited tables need faster speeds/smaller divisions for the same feel). Draw a simple high-pass shape and generate the remaining keyframes with a sweep fill (progressive shift without wrap-around), floor down, synced over 4 bars, for a classic analog-style HP sweep. Use a loop crossfade at the cycle boundary; export the table as WAV for other synths.
- Rhythmic variant: step through keyframes one per beat division instead of interpolating, and add gate (silence a % of each step's tail) for chopped, per-step spectral flavours on leads/arps. Using a keyframe count that doesn't divide the phrase (e.g. 20 vs 4/8 bars) gives polyrhythmic filter shaping.
- Width and layering: add stereo so L and R read the curve at different times (mono compatible). On parallel copies or several tracks with the same table, offset the start phase of each so they move out of sync with the same character. Use dry/wet for parallel blend, output gain to level-match, and a 0 dB limiter for aggressive boosts.

### Lush evolving pad from two saws (second −12 st), high unison (~8, shimmer-style detune ~30), long overlapping amp ADSR, a filter envelope that opens from a low start (~200 Hz) with ~2 s attack, plus a slow non-retriggering tempo-synced triangle LFO on cutoff so each chord catches the filter in a different place; optional analog-modelled filter drive and a long low-cut convolution/space
Source: [How to Make Lush Evolving Pads in Wavetable | Ableton Tutorial](https://www.youtube.com/watch?v=p5ETZc7Zfw4) · was `lush-dual-saw-filter-env-nonretrigger-lfo-pad`
- Oscillator 1: a saw or near-saw wavetable. Enable unison (classic or shimmer-style) at a high voice count (source uses 8) with detune around 30 — lush and smeared, not out of tune.
- Oscillator 2: same saw, pitched −12 semitones, to thicken with a lower octave. Balance levels.
- Amp envelope: attack ~2 s; sustain about half the peak (source ~−13 dB on that scale); decay ~6 s; release ~2 s so chord tails overlap instead of stopping dead.
- Filter envelope (env 2) → cutoff: start cutoff near ~200 Hz, envelope amount high enough to open clearly (source ~70). Shape env 2 with ~2 s attack and long decay/release so it swells open like the amp, not a pluck.
- LFO 1 → cutoff at moderate depth (source ~40): tempo-sync to a multi-bar rate (source 3 bars or 1.5), triangle shape, and turn retrigger OFF so each new chord catches a different LFO phase — the filter no longer repeats identically every note.
- Optional: switch the filter to an analog-modelled / driven mode for mild saturation instead of a separate distortion plugin. Optional: slow LFO or envelope on wavetable position for timbral morph (pitch stays fixed).
- Space: a long lush reverb or convolution (source uses a 'black hole'-style IR) with dry/wet raised and a low-cut on the reverb so the pad stays deep without rumble.

### Evolving cinematic pad/drone from a three-instance wavetable rack split by register (lows / mids / highs), each with two very slow free-running LFOs moving the two oscillators' wavetable positions in opposite directions, glue compression, a reverb→gentle saturation→long reverb sandwich, and one macro that opens filters and adds drive
Source: [How to Build Evolving Cinematic Pads with Wavetable Synths](https://www.youtube.com/watch?v=RPzAJFC_JkI) · was `three-band-wavetable-rack-counter-lfo-position-glue-reverb-saturate-reverb-macro-drive`
- Mids layer: wavetable osc 1 with a warm table, filter closed a little (drive-capable filter type), low cut to keep it in the mids. Two very slow LFOs at slightly different rates, retrigger off: LFO 1 + and LFO 2 − on osc 1 position.
- Osc 2 on the mids: a different table (e.g. sweep saw) with the same two LFOs in the opposite directions, so the movements sometimes cancel. Add shimmer-style unison.
- Filter 1 movement on the mids: a small amount of both LFOs and of a slow envelope (about 2 s decay, 3 s release) on cutoff.
- Group into a rack, duplicate the instance twice and name them lows / mids / highs.
- Highs: brighter, more aggressive tables, filter more open with light drive, noise-style unison with more voices; make its LFOs different speeds from the mids (one slower, around 0.04 Hz); keep mod amounts delicate. Osc 2 slightly detuned and optionally an octave down.
- Lows: simple saw an octave down without unison plus a sub; cut the lowest rumble with a steeper, low-resonance filter; one very slow LFO with a small amount on filter frequency.
- Set about 1 s attack on all three and balance their levels (turn highs down if they dominate).
- FX chain after the rack: glue compressor (4:1, threshold just catching peaks), algorithmic reverb 100% wet with a vintage character, gentle soft-clip saturation, then a long lush reverb at 50% mix, and a limiter catching 2-3 dB.
- Map one macro (mod wheel) on each instance to open filter 1 (or close it on the highs) and add filter drive, with only a small wavetable-position offset.
- Hold one chord, then a single note, and check that the sound keeps evolving with no loud jumps.
