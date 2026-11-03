# Supersaw / unison pads: detune, voice count, width and filter swell

Goal: Build a wide, warm detuned-saw pad (house, trance, cinematic) by choosing voice count and detune in cents, spreading voices in stereo, then shaping with a key-tracked low-pass, slow attack/release and space FX.

**Theory:** Detuned voices beat at |f1-f2| Hz; 5-16 voices at 10-30 cents produce a chorus-like shimmer. Odd/even voice spread keeps the centre solid; stereo decorrelation gives width that partly cancels in mono.

**Hear it:** `sample-lab/theory/detune_unison.py`

## Workflow
1. Pick the chord first (extended voicings: add9/maj7/min9 sound best detuned); play it as a held loop.
2. Oscillator: 1-2 saws, unison 5-16 voices, detune 10-25 cents (go to ~50 only for trance supersaw); free-running phase so each note starts differently.
3. Spread voices across stereo (width 60-100%) but keep one centre voice or a mono sub layer below ~150 Hz.
4. Filter: 12/24 dB low-pass, cutoff ~1.5-4 kHz, key-tracking ~50%, light resonance; optional slow LFO (0.05-0.3 Hz) on cutoff for drift.
5. Amp envelope: attack 0.3-1.5 s, sustain high, release 1-3 s; optional filter-envelope swell (or a fifth-up layer) to bloom into each chord.
6. Space: chorus or ensemble if unison is low, then plate/hall reverb send 2-4 s with low-cut ~200-300 Hz on the return; tape saturation before reverb for glue.
7. Mix: high-pass the pad at 150-250 Hz, duck it lightly to the kick (punch-only), check mono — reduce width if the pad thins out.
8. Hear the theory: run `/home/box/audio-tools/bin/python sample-lab/theory/detune_unison.py` from the repo root and compare the sections; reuse its functions as a starting point for renders.

## Source techniques (merged, numbers kept)

### Organic ambient pluck-pad with ladder, velocity, chorus-space
Source: [Making Dreamy & Organic Pads | Vital Sound Design Tutorial](https://www.youtube.com/watch?v=ehKoz6ILmxQ) · was `ambient-organic-pluck-pad-ladder-chorus-space`
- Init patch. Amp env: short attack, raised decay, mid sustain (not zero), some release so held notes act as pads.
- Osc: soft sine/basic shape; apply warp/squeeze toward a saw–sine hybrid for mild harmonics.
- Filter1 ladder (or analog): env2 pluck contour → cutoff (~+24 semitones depth); low resonance; key track on; drive near zero for subtlety.
- FX distortion (e.g. sine-fold): moderate drive, reduced mix; enable post-filter with high cutoff/low resonance/blend to control level vs harmonics.
- Low pink noise → band-pass filter2 with drive, key track, low resonance so noise blends and stays mid-focused.
- Add slow pitch drift; optional formant/warp random (stereo, ~2s) bipolar for organic movement.
- Velocity → osc level and warp/squeeze and cutoff so soft plays are darker/quieter.
- Chorus: freeze/tempo off, raise depth/delay, high feedback for long decay; high-pass; envelope → spread for note-ducked lush tails; then real reverb (~80 size, ~30% mix, low cut) and dotted-quarter delay (~30% mix).

### Warm analog cinematic pad with pitch drift and opposing pan
Source: [Serum Tutorial - Warm 'Analog' Cinematic Pad Synth](https://www.youtube.com/watch?v=CcXGRCXv8lQ) · was `cinematic-warm-analog-pad-drift-stereo`
- Before oscillators, route a slow chaos/random/noise mod source to master tune (or global pitch) for gentle analog-style pitch drift.
- Osc A: choose an analog/Juno-like saw; set ~5 unison voices; soften amp attack and release for a pad contour.
- Osc B: choose a softer/scuffed triangle-like analog wave; ~5 unison; pitch +1 octave; mix level slightly under Osc A.
- In global/unison settings, reduce per-oscillator unison stereo width to ~50% so later pan mods have room.
- Free-running very-slow LFO → Osc A pan and Osc B pan with inverted depth so they sweep opposite sides.
- Optional: layer a quiet granular/noise texture under the oscs for enharmonic air (original sample, not a ripped pack).
- 12 dB low-pass: tame Osc A + noise highs so Osc B harmonics read; also LFO-modulate filter pan/offset for extra stereo motion.
- Add spacious reverb; place another filter after reverb and slowly open it (or raise filter mix) over time for a blooming spacey finish.

### Classic swept analog pad/lead: two detuned oscillators into a state-variable (SEM-style) filter driven by a triangle 'fin' filter envelope that rises then falls, modest resonance, mono mode with 8-voice stereo unison, light compression and tape echo, and an optional second oscillator pair through a different filter type swept the same way
Source: [Why This Classic Filter Sweep Still Sounds So Good](https://www.youtube.com/watch?v=xil_HpL1izg) · was `classic-fin-envelope-filter-sweep-dual-detuned-osc-mono-8-voice-unison-tape-echo-dual-filter-layer`
- Init a patch. Choose a state-variable (SEM-style) lowpass, and if the synth offers vintage amp/envelope models, use them. Play in a low register with two oscillators slightly detuned.
- Shape the filter envelope as a triangle 'fin': slow rise to the peak, slow fall back down, low sustain. Set envelope intensity so the cutoff travels a wide range.
- Add a little resonance, just enough to make the sweep sing without whistling.
- Switch to mono mode with full stereo unison (8 voices) and add unison detune.
- Add light compression and a tape echo. Skip chorus, because unison already gives width.
- Optional: enable a second filter of a different type, send oscillators 3–4 to it, give it its own fin envelope and some detune, then blend both layers (pull back if it gets too dense).

### Classic house pad in any synth: minor 9 / minor 7 / major 7 chords, many-voice detuned unison with oscillator retrigger off (free-running), stereo spread from the unison width control or a chorus/ensemble if the synth has none, slightly resonant lowpass plus serial highpass to remove mud, slow LFO on cutoff, slow amp attack with no filter envelope, coloured noise partly bypassing the lowpass, delay + reverb sends; plus a quick pad from a looped chord-stab sample
Source: [How to Create Classic House Pads (Any Synth!)](https://www.youtube.com/watch?v=nbS1pT8V7YU) · was `classic-house-pad-ext-chords-16-voice-free-run-unison-width-vs-chorus-resonant-lp-plus-hp-slow-lfo-cutoff-slow-amp-noise-bypass-filter-chord-stab-loop-pad`
- Program extended chords (e.g. Em9, Em7, Emaj7) on an init saw patch with the filter open.
- Raise unison toward 16 voices and detune until wide and airy; add oscillator 2 with its own unison at a slightly different detune.
- Turn off oscillator retrigger so unison voices free-run.
- If voices are not spread in stereo, raise the unison width/spread control; if the synth has none, add a chorus/ensemble after it.
- Set the lowpass cutoff a little low with some resonance; add a highpass in series to remove muddy lows; add a slow LFO on cutoff.
- Set a slow amp attack with full sustain and remove filter-envelope amount.
- Optional colour: switch to pulse or mix pulse and saw, modulate pulse width with a slow LFO, add a sub oscillator; add coloured noise at low level, routing some of it straight to the highpass/output so its highs bypass the lowpass.
- Add delay and reverb on sends and check against drums.
- Chord-stab variant: load a chord stab into a sampler, loop a steady section after the transient (snap off), add loop crossfade and slow attack, then hide the repeat with delay, reverb and a filter.

### Evolving unison pad with filter swell and fifth layer
Source: [Sound Design with VITAL - Wide BASS - Evolving PAD - Lead PLUCK](https://www.youtube.com/watch?v=rv0X7eZNnEo) · was `evolving-pad-unison-filter-swell-fifth`
- Init tonal osc (saw/rich wave). Amp can be quicker; env2 slow attack → filter cutoff with low resonance so tone arrives then opens.
- Add unison with noticeable stereo spread; optional slow LFO→cutoff for ongoing motion.
- Second osc pitched a fifth (+7) into the same filter with similar/less unison so it coheres as a chordal pad; optional third higher voice with LFO→level for late shimmer.
- Multiband or glue compression to control peaks and bring highs; large size/decay reverb with rising mix; optional chorus for extra spread; watch distortion from overload.

### Dual-saw ladder pad with granular spice and FX macros
Source: [Amazing pads with the new Granular Generator in Phase Plant](https://www.youtube.com/watch?v=FZ9oXRJIR6o) · was `granular-dual-saw-ambient-epic-pad`
- Two analog saws: second −1 octave at ~20–25% level as low texture; lower master gain.
- Amp env attack ~4s, release ~4–5s.
- Ladder/diode filter, low cutoff; second envelope (attack ~2–3s, low sustain, longer decay/release, convex curve) → cutoff for slow open.
- Corrective EQ: high-pass ~60 Hz; gentle cut ~120–150 Hz mud.
- Chorus (e.g. 3 taps, high mix, moderate depth, slow rate) → sync delay (1/4) for chord transitions → large reverb (~35–40% mix).
- Add granular layer mid-position, bipolar grain jitter, +12 st, small pitch variation; blend under saws through same FX.
- Macros: cutoff, resonance, FX wet (chorus/delay/reverb mixes), granular level — start FX mapped from 0 so macro brings space in.

### Lush stereo saw pad with scale-snapped pitch texture
Source: [How to make LUSH ambient pads in Vital](https://www.youtube.com/watch?v=pQFr594QwI4) · was `lush-stereo-saw-pad-random-pitch-texture`
- Osc1+2: basic saws; pan opposite; fine-tune ~±5 cents.
- Add ~4 unison voices @ ~3% detune for depth.
- Filter1 dirty/12 dB on both oscs; set drive and resonance; env1 mid attack/decay/sustain + longer release for level.
- Env2: short attack, long decay, sustain <50%, release up → filter cutoff for per-chord harmonic bloom; also stereo random (1 bar) → cutoff.
- Osc3 texture: random (sine-interpolate, ~5.2s) → transpose with scale snap + global snap; +12 st base; map same random to pan (stereo mode for independent movers).
- Squeeze/distort osc3 via macro; optional random → fine pitch; slow stereo random → global voice detune (bipolar) for analog warp.
- Sample noise (e.g. HVAC) keytrack off; filter2 on osc3+sample; reverb ~50% mix; ping-pong delay 1/4; re-enable osc1/2.

### Organic looped-sample unison-voicing lush pad
Source: [Phase Plant | Creating Lush Organic Pads](https://www.youtube.com/watch?v=CMkXW17LYyA) · was `organic-looped-sample-unison-voicing-pad`
- Load an acoustic sample; loop with crossfade so the loop point is inaudible — treat it as a static organic oscillator.
- Layer a second contrasting organic loop (body vs air).
- Apply unison chord voicings (e.g. fifths on one, sus4 on the other); add tasteful detune/spread; amp env with soft attack and slightly reduced sustain for swell-then-settle.
- Add low-level WT + analog/saw stabilizers with mild unison for synthetic glue; macro to bring body in as needed.
- Post FX: ensemble/flanger/filter experiments; multiband — saturate lows, light ring-mod in mids, stereo widen+chorus on highs; light glue saturation/EQ/dynamics.
- Mod: LFO + random → filter (never identical motion); random → global fine pitch drift; random → WT position; aftertouch→filter; velocity→volume; macros for detune and cutoff.
- Space: convolution or character reverb from original impulse (~wet) plus long lush reverb (~15s, mostly wet) for dimension.

### Three-layer complementary pad with post-reverb tape/lo-fi degradation and tail-lifting expander
Source: [How To Create AMAZING Pads and Drones | A Sound Design Tutorial (Venus Theory)](https://www.youtube.com/watch?v=UShjYsGgWcM) · was `three-layer-complementary-pad-post-verb-lofi-degrade`
- Plan three complementary layers that each own a spectral job: layer 1 low/low-mid body, layer 2 upper-mid/air, layer 3 a hint of modulated noise for space. Use one multitimbral synth or several synth instances grouped to one bus.
- Layer 1: wavetable oscs with LFO 1 → wavetable position on osc 1 and 2; low-pass with some resonance and filter drive; NO filter envelope—cutoff moved only by a slow LFO (LFO 3); very long amp attack/decay/release.
- Layer 2: wavetable oscs with their own LFO-swept positions; 24 dB/oct band-pass with high resonance; long filter envelope (long attack/decay/release, closing back) plus the shared slow LFO on cutoff; a DIFFERENT long amp envelope from layer 1 so movements don't line up.
- Layer 3: oscillators off, noise only at ~6% level; noise into a 12 dB/oct band-pass (high-passed noise, fair resonance), cutoff moved by LFO; LFO 1 → noise volume ~15%. All these LFOs run at a fraction of a cycle per second.
- Use slow triangle LFOs/MSEGs on the fine tuning (and/or global pitch) of layers 1 and 2 for constant gentle detune drift; add filter drive and in-synth subtle slow phaser and chorus.
- Insert a large modulated reverb ~90% wet on the pad bus (outer-space/lush style; try several reverbs and pick by the character they give).
- AFTER the reverb, stack degradation: tape sim with wow and flutter (pitch warble + saturation/glue) → second saturator adding heat and drift (combine saturators for different colours) → tape/lo-fi stage with a bit-crush style harmonic grit on the top end, hiss, wow/shake, colour biased brighter, slower warble speed → noise-modulation (erosion-like) with band-pass noise around ~3 kHz, kept low.
- Last: a very subtle multiband upward expander/compressor (OTT-style at low depth) after the reverb to lift decaying tail detail between notes.
- Optionally place field recordings (e.g. rain) very low under it, and plan contrasting parts (warm low bass vs cold pad).

### super-unison wide stereo lead (osc2 stack)
Source: [TRAVELER: The Cinematic Hybrid Synthesizer | Official Walkthrough](https://www.youtube.com/watch?v=IU76c2Cygs4) · was `traveler-walkthrough-super-unison-wide-lead`
- Assign Oscillator 2 role as the Super/unison stack: continuous waveform from saw through sine to thin pulse.
- Enable stereo voice stack (up to ~7 voices). Increase detune and stereo spread until the stack alone sounds gigantic.
- Optionally add Osc1 as FM/sync carrier support (sync Osc2; FM from Osc2/3 linear or exponential, variable depth) for bite.
- Mixer: set Osc2 level primary; pan can be modulated later. Mild drive into filter if available.
- Route through stereo ladder-style LPF (12–24 dB). Keep cutoff high enough to preserve width; use modest resonance.
- Amp envelope: medium attack for pads or fast attack for leads; sustain mid-high; release 0.5–2s. Enable pan-spread / voice stereo distribution if available.

### Unison voicing: odd vs even voice counts, detune/blend/width, clean supersaw
Source: [Merged from 2 YouTube how-to transcripts](None) · was `unison-odd-even-detune-width-clean-supersaw`
- Start from 1 voice, then set 2 voices: expect one left and one right with a center gap; default detune often sounds harsh—lower detune.
- Switch to 3 (odd) voices: confirm a center voice appears; with blend lowered you hear more of that center while keeping similar detune.
- Compare 4 (even) vs 5 (odd) at similar detune: higher even counts can sound more detuned/wide; very high odd counts (e.g. ~15) pack many voices near center so the patch can sound *less* detuned than a mid even count.
- For reese/detuned saw bass or other front-and-present mix parts, prefer odd voice counts for mono compatibility (center represented).
- For an uber-wide lead you will pan off-center, even counts (2/4/…) with blend favoring outer voices are acceptable.
- Example starting detune for chord/lead work: modest (~0.16 in the video’s demo); reset blend to default then adjust; always A/B odd vs even in context.
- Supersaw: Load a simple saw (or rounded/noisy saw variant), not a multi-frame complex WT you plan to sweep aggressively.
- Supersaw (apply the odd/even rule above when choosing the count): Set unison ~6–12 (example ~10); set detune and blend near mid — extreme detune+blend is for FX, not clean chords.
- Optional Osc B: fewer unison voices, pitch ±octaves, lower level to thicken without doubling chaos.
- Optional centered saw sub one octave down (no unison) for mono mid-weight; quiet unique noise sample for texture.
- FX order example: EQ (cut lows, lift highs) → compression → ping-pong delay → reverb last; optional light hyper/dimension detune on the bus (can widen even the sub).
- Subtle warp (e.g. bend+/−) via envelope/LFO for 3D motion — keep amounts small on supersaws.
- Global unison: reduce width (~50%) for better chord phase correlation; try stack modes (super, fifths, center−2, octave) sparingly; warp-offset per voice only if warp is intentional.

### Warm heavenly supersaw pad with keytrack and lush FX
Source: [How to Make Super Warm, Heavenly Pads with Vital](https://www.youtube.com/watch?v=cF5ku3Og0Nk) · was `warm-heavenly-supersaw-pad-keytrack-fx`
- Saw osc, unison ~5–7, reduce detune from max; amp slow attack + long release; raise voice count for big chords.
- Optional: velocity → attack with inverted depth (harder = shorter attack); straighten release curve if needed.
- LP filter: zero resonance; 24 dB slope; cutoff for warm lows; compare analog/ladder/diode; enable key track until high notes remain audible in wide chords.
- FX: rich chorus for constant motion; reverb with low cut, ~3s; dotted-eighth delay with stereo spread/ping-pong and controlled feedback.
- Subtle slow irregular LFO → cutoff for life; EQ after FX as needed (gentle HP, optional shimmer highs).
- Optional layer: PWM wavetable with moderate unison and slower PWM LFO; combine with supersaw; if subs build, serial HP after LP; optional unfiltered sine to reinforce fundamental against phase cancellation.
- Optional second patch/layer for shimmer (additive/WT, little unison, LFO→level or short decay + harmonic stretch); pitch-up delay/shimmer on that layer only.

### Ambient pad from scratch with staggered layer attacks: sine foundation with light unison, saw and triangle layers on their own filters (triangle an octave up), a separate amp envelope per layer with longer attacks for higher layers, a pitched-down foley texture in the noise slot, slow 4-bar filter LFO, panning LFO, light random on one filter and random level on the foley, then chorus, multiband compression, delay and reverb
Source: [How To Make Ambient Pads 100% From Scratch (Vital Tutorial)](https://www.youtube.com/watch?v=bAovHufTsc8) · was `staggered-attack-octave-layer-pad`
- Osc 1: sine with a little unison as the foundation; set amp attack and release moderately long.
- Osc 2: saw with unison; Osc 3: triangle with unison, pitched up one octave. Route osc 2 and osc 3 to separate filters.
- Give each layer its own amp envelope (routed to its level): layer 2 a longer attack, layer 3 a much longer attack so the octave-up layer is mainly heard toward the end of each chord.
- Put a quiet ambient foley texture (e.g. clicks) in the noise slot; pitch it down to the key if it is tonal.
- LFO 1: triangle reshaped to open slowly and close quickly, tempo 4 bars (4/1), on one filter's cutoff. LFO 2: sine, bipolar, on osc 3 pan.
- Add a small random modulation on the saw layer's filter and a random modulator on the foley level so it comes and goes.
- FX: a bit of chorus to tie oscillators together, multiband compression to bring up subtle detail, then delay and reverb.
