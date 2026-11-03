# Generative rhythm: Euclidean patterns, polyrhythm, polymeter, probability and endless tempo illusions

Goal: Generate rhythms and melodies algorithmically: Euclidean E(k,n) with rotation and boolean combinations, multi-layer scale weavers, polymeter lengths, probability/chance gates with seeds, constrained random sequencers, Risset accelerando and pendulum-wave phasing.

**Theory:** E(k,n) spreads k hits as evenly as possible over n steps (E(3,8)=tresillo). Polyrhythm a:b = two pulse streams sharing a cycle; polymeter = loops of different lengths phasing. Probability with a fixed seed is repeatable.

**Hear it:** `sample-lab/theory/rhythm_polyrhythm.py`

## Workflow
1. Choose a grid (16ths) and base pattern E(k,n); rotate to move the accent.
2. Layer 2-8 Euclidean generators, each mapped to a drum or one scale note; combine with OR/XOR/AND for new patterns.
3. Set different loop lengths (e.g. 16 vs 12 vs 7 steps) for polymeter evolution.
4. Add chance rests, random octave/degree within scale, random accents; seed it so it's repeatable.
5. Tame: constrain to scale and 1-2 octaves, fewer pitches, phrase restart points, randomize only last notes.
6. Illusions: Risset rhythm (crossfaded doubling tempo layers), pendulum wave (lanes with slightly longer periods realign after N cycles).
7. Print to MIDI/steps and edit by ear.
8. Hear the theory: run `/home/box/audio-tools/bin/python sample-lab/theory/rhythm_polyrhythm.py` from the repo root and compare the sections; reuse its functions as a starting point for renders.

## Source techniques (merged, numbers kept)

### Two Euclidean pulse generators per track combined with Boolean logic (OR, XOR, AND, SUB), per-generator rotation and whole-track rotation, then printed to an ordinary step sequence for hand edits; also used to redistribute an existing bassline and to leave gaps an arpeggiator fills
Source: [How I Actually Use Euclidean Sequencing on Digitone 2](https://www.youtube.com/watch?v=WeOuxcN0pV8) · was `dual-euclidean-pulse-generators-boolean-or-xor-and-sub-rotation-track-rotate-print-to-steps-melodic-redistribute-arp-fill`
- Turn on Euclidean mode for a drum track. Set generator 1 to a simple count (e.g. 4 pulses over 16 steps) and listen; then try counts that do not divide 16 (5, 11).
- Enable generator 2 with a different count (e.g. 5 against 4) using OR. Rotate generator 2 to move its hits against generator 1.
- Switch the operator: XOR to remove overlapping hits and open space; AND to keep only overlaps (raise counts, e.g. 9 and 12, and rotate until notes appear); SUB to keep generator 1 except where generator 2 lands.
- When an emergent pattern makes a new downbeat, use whole-track rotation (e.g. +3 steps) to move both generators together so that hit becomes step 1.
- Print the pattern to the normal step sequencer, then hand-edit (move a note, leave room for a snare). Build hats on another track at length 32 with SUB to carve notes out of a dense generator 1.
- On a melodic (bass) track with notes already programmed, enable Euclidean mode so those notes are redistributed by the pulse pattern; add generator 2 with XOR and rotate the track. Randomise the Euclidean settings repeatedly until a version works.
- For sparse patterns, enable an arpeggiator and remove one arp note with its offset/step mask so it fills gaps without crowding.
- For performance, change rotations and pulses on all tracks at once, and keep a snapshot so you can jump back to the original pattern.

### Eight-layer Euclidean pattern generator with two modes: drums (each layer = one MIDI drum note) and melody (each layer = a different note of a chosen scale and root, so stacked layers form in-key chords); per-layer steps, pulses, rotation, velocity and gate, a drift action that nudges each layer's pulses by ±1, layer or global randomise that never changes note assignment, and scale/root changes that keep the rhythm
Source: [Euclidean Weaver v1.2.0 | Generate Euclidean Rhythms and Melodies in Bitwig Studio](https://www.youtube.com/watch?v=UchJGizLiLM) · was `eight-layer-euclidean-weaver-drum-or-scale-melody-mode-one-scale-note-per-layer-steps-pulses-rotation-gate-drift-randomize-keep-rhythm-change-scale`
- Choose drum mode and assign layers to drum notes (kick, snare, closed hat, etc.). Enable two layers, set steps/pulses/rotation, and generate.
- Add layers one at a time (e.g. closed hat, crash), set each layer's velocity and gate, and regenerate.
- Change a layer's rotation or pulses (e.g. move the snare), or press randomise for one layer; use drift to move every active layer's pulse count by ±1.
- Switch to melody mode, choose scale and root. Each layer now plays a different scale note; enable several layers with different step lengths.
- Shorten gate if notes overlap too much; randomise all (notes stay fixed) until a rhythm works.
- Keep the rhythm and change the scale or root (e.g. to Phrygian) and regenerate.

### Generative rhythmic sequence from a hand-written 8-step pattern: live length and start-point changes, chance-based rests, a 5-step Euclidean trigger length phasing against the 8 steps (a 40-step cycle), random modulation of octave and scale degree kept subtle, random distortion and release for accents and note lengths, smooth-random slow LFOs on filter and wavetable position, introduced gradually in performance
Source: [Part 2: Generative Sequencing for Techno (or any other style of music)](https://www.youtube.com/watch?v=mb3yqXO9JiE) · was `generative-rhythmic-sequence-euclid-length-phase-against-step-count-chance-rests-random-octave-degree-random-accent-release-smooth-random-filter-wt`
- Program an 8-step sequence (or one root step plus random → scale degree around 7–8 degrees for an instant quantised random melody). Save it as the base.
- While playing, change pattern length and set a different start point to get variation from the same notes (e.g. steps 1–16 vs 17–32 for different song sections).
- Set chance to about 75% for random rests. Alternatively set a Euclidean trigger length of 5 with chance about 90%, so the 5-step trigger pattern drifts across the 8 notes.
- Add a tempo-synced delay so echoes land in the rests.
- Patch random → octave (positive = up jumps, negative = down) and random → scale degree, attenuating until jumps of about 4–5 degrees appear. Optionally map degree to a knob to sweep between bassline and lead register.
- Patch random → distortion for accents and random → release for varied note lengths; lower the base release so variation is audible.
- Add LFO X (smooth random, slow) → filter cutoff and LFO Y (smooth random, about 5 s) → wavetable position, with base position above zero.
- When performing, start with the plain sequence and introduce degree, octave and timbre modulation one by one over time.

### Pendulum-wave arpeggio (measured from Virtual Riot "Pendulum Sequence 2"): one repeating short note per scale lane, lanes slightly slower going down, so the figure drifts into staircases and curves and realigns after ~408 cycles
Source: [Pendulum-wave arpeggio (measured from Virtual Riot "Pendulum Sequence 2"): one repeating short note per scale lane, lanes slightly slower going down, so the figure drifts into staircases and curves and realigns after ~408 cycles](None) · was `pendulum-wave-arpeggio-35-lanes-e-minor-e8-to-e1-top-period-half-beat-plus-0p245pct-per-lane-note-37pct-of-period-all-start-together-realign-after-408-cycles-10-stacked-detuned-saw-layers`
- Set the tempo to 30 BPM. Make 35 lanes, E8 at the top down to E1, using E minor without C (thinning in the low register).
- The top lane plays a note every 1/2 beat. Lane i plays at frequency f0·(N−i)/N, with N = 408; that is about +0.245 % period per lane, so the bottom lane is ×1.083 slower.
- Note length is 0.37 × the lane's own period. All lanes start at the same moment; the staircase comes from the drift.
- Voice: a 3-saw stack, lowpass at about 2.4 kHz, fast attack, exponential decay, top lanes a few dB quieter.
- Stack 10 copies with about ±7 cents of detune, about ±9 ms of offset, and panning spread; add a short cross-delay. Target −15 LUFS, about −4 dBTP and side about −11 dB.
- Arrange it as: sparse intro (every 3rd lane), full phasing, a realign moment (start the pattern N·period − x seconds in so the realign lands where you want it), then an outro.

### Endless-accelerando (Risset rhythm) illusion for cinematic tension: the same pattern at double speed fading out and at half speed fading in while tempo automates to double, dropped subdivisions (fade every other note of a six-pulse group as tempo doubles), half-speed (3/4) and third-speed (6/8) copies forming a 3:2 hemiola fractal, voices swapping roles across cycles, and a long note gliding slowly against a sustained pitch
Source: [Recreating The Impossible Rhythm Illusion In "The Odyssey" Soundtrack](https://www.youtube.com/watch?v=Z-VjDxckkg8) · was `risset-rhythm-endless-accelerando-tempo-doubling-fade-every-other-subdivision-half-and-third-speed-hemiola-layers-rising-gliss-dissonance`
- Build the basic form: one pattern, a double-speed copy fading out over the cycle, a half-speed copy fading in, and tempo automated to double over the same cycle. Loop it.
- Dropped subdivisions: play a group of six pulses; as tempo rises toward double, ramp down the level of every second note until silent.
- Add the same six-pulse pattern at half speed (three strong pulses, 3/4 feel) and at one-third speed (two pulses, 6/8 feel).
- Apply the dropped-subdivision fade to each layer in turn, staggering them, and fade whole layers in and out across cycles; let a voice move from the 2-pulse role to the 3-pulse role in the next section.
- Automate tempo doubling cycle by cycle (e.g. 150 → 300 → 600) and reset to the start tempo at a cycle boundary when you hit the tempo ceiling, with fades placed in those transition zones.
- Add tension: a long note gliding slowly upward against a sustained pitch, plus heavily reverberated vocal or texture layers.

### Three rules for making a randomised/Euclidean sequencer sound intentional: constrain (scale, octave range, pitches pulled close, phrase length), repeat (global randomness to zero, reset per-step random, restart points so the phrase retriggers each bar), and simplify (about three pitches, fewer pulses, complexity from layering simple parts), then add hand-made variations on chosen cycles and random pitch options on only the last few notes
Source: [Torso T1: The 3 Rules That Make Generative Sequencing Musical](https://www.youtube.com/watch?v=gyhfAdy6eq8) · was `tame-generative-sequencer-constrain-scale-octave-phrase-zero-global-random-restart-points-fewer-pitches-pulses-manual-cycle-variations-random-on-last-notes`
- Solo one part. Set a scale, reduce octave range, and move notes into nearby octaves.
- Set global continuous randomisation to zero and reset per-step random amounts on all steps.
- Add a restart point so pitch and trigger cycles realign at the start of every bar.
- Reduce to about three pitches and fewer pulses; optionally add a second restart point.
- Pick a cycle (e.g. bar 2) and hand-add notes; copy that variation to other cycles, change start points, raise one note an octave, add a roll.
- Give only the last few notes (e.g. last four) extra pitch options or randomisation.
- Repeat rules 1–3 for each other part and listen to them together.
