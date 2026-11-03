# Binaural and isochronic tone layers under music (audio construction only)

Goal: Build binaural (L/R frequency difference) and isochronic (gated carrier) layers under music: carrier pitch in key, beat/pulse rate, raised-cosine gating, pad foundation, notching the bed at the carrier, fades. No health claims.

**Theory:** Binaural beat = |fL - fR| perceived on headphones only; isochronic = amplitude gating at the target rate audible on speakers. Raised-cosine edges (~3.75 ms) avoid clicks.

**Hear it:** `sample-lab/theory/entrainment_tones.py`

## Workflow
1. Choose carrier in the song key (e.g. C5 523.25 Hz) and rate (e.g. 10 Hz, 14-18 Hz beta, 40 Hz).
2. Binaural: left = carrier, right = carrier + rate; layer octaves if desired.
3. Isochronic: gate a sine carrier at the rate with raised-cosine edges; verify rate in 20 s windows.
4. Music bed: slow pad, long reverb, ping-pong echo; notch the bed at the carrier pitch so the pulse stays clear.
5. Fade the layer in/out over 10-30 s; keep it 10-20 dB below the music.
6. Do not make health or cognitive claims in titles or text.
7. Hear the theory: run `/home/box/audio-tools/bin/python sample-lab/theory/entrainment_tones.py` from the repo root and compare the sections; reuse its functions as a starting point for renders.

## Source techniques (merged, numbers kept)

### Produce a binaural-beat meditation track: a two-chord pad foundation with long reverb and overlapping glided notes, a sparse echoing piano and subtle bass, volume-automated arrangement, then a binaural layer of two pure sines (440 Hz and 432 Hz for an 8 Hz difference) panned hard left/right, a narrow high-Q EQ cut at the carrier frequency on the music bus so nothing masks it, fades, a gentle limiter (~3 dB input, no audible gain reduction) and WAV/MP3 export at 44.1 kHz
Source: [Producing a Binaural Beats Meditation Track in Ableton Live (Step-By-Step)](https://www.youtube.com/watch?v=GndBM5EifHA) · was `binaural-beat-meditation-track-pad-foundation-long-reverb-glide-overlap-pingpong-echo-two-sines-440-432-panned-lr-8hz-narrow-notch-carrier-in-music-bus-fades-gentle-limiter-export`
- Pick a soft pad, play a simple two-chord loop (e.g. A then D), add reverb with high decay and wet mix, capture the MIDI and align chord changes to the grid; loop it.
- Layer a second pad for texture and a sparse piano phrase; add an echo with more feedback and ping-pong, plus a reverb with moderated wet mix.
- Lengthen notes so they overlap at chord changes and enable glide so pitch slides between them.
- Add a subtle low bass on the roots; lower all instrument levels to avoid clipping.
- Arrange with volume automation: bring elements in and out gradually; high-shelf boost and mid cut on bright parts; put delay before reverb.
- Binaural layer: a sine instrument at 440 Hz and a duplicate at 432 Hz; listen unpanned (wobble), then pan one hard left and one hard right; program one note across the whole track.
- Group the music tracks and add a narrow, high-Q EQ cut at 440 Hz on the group.
- Fade the beat in and out; set its level so it is quiet but noticeably different when muted.
- On the master, loop the loudest section and add a limiter with about 3 dB input and no audible gain reduction; export WAV 44.1 kHz and an MP3; test-listen later in a calm setting and adjust.

### Add an isochronic pulse layer under an existing track: a sine (or noise) carrier played by one long MIDI note, amplitude-pulsed at a chosen rate (e.g. 4 Hz) with a smooth-step pulse shape and a 0–100% isochronic blend, faded in and out by gain automation, with the pulse rate automated (e.g. 15 Hz → 4 Hz → 15 Hz) using ~10 ms parameter smoothing, carrier tuned by reference (440/432) or a custom note-to-frequency map and verified with a tuner, then mixed barely audible
Source: [How to Create Isochronic Tones in Ableton Live with Huon Studio](https://www.youtube.com/watch?v=WNewLv-kI2I) · was `isochronic-tone-layer-under-music-sine-carrier-midi-note-amp-pulse-blend-smooth-step-shape-fade-in-out-automate-pulse-rate-15-to-4-hz-and-back-10ms-smoothing-carrier-tuning-432-or-custom-map`
- Create a MIDI track with the tone generator; set the device output low (about -20 dB) so the layer starts quiet.
- Program one long MIDI note (or loop a short note while designing; chords also work).
- Set the pulse rate (e.g. 4 Hz) and raise isochronic blend from 0% to 100%; choose a smooth-step pulse shape.
- Add a gain utility and automate a ~30 s fade-in at the start and a 30–60 s fade-out at the end.
- Expose the pulse-rate parameter for automation, set parameter smoothing to 0.01 (10 ms), and draw breakpoints with typed values: 15 Hz at the start, 4 Hz in the middle section, back to 15 Hz at the end.
- Optional carrier tuning: switch the tuning reference (440 → 432 Hz) or load a custom note-to-frequency map and find the note that gives the target frequency (e.g. 528 Hz); confirm with a tuner set to the same reference.
- Set the track fader so the layer is barely audible under the music.

### Layered binaural + isochronic track architecture: carrier in the left ear and carrier+beat in the right (e.g. 100/104 or 100/110 Hz), octave-up/down copies for depth, an isochronic pulse ratio-locked to the beat rate (1:1, 1:2, 2:1) with sine pulse shape, optional left-right ping-pong pulsing, extra harmonic/anchor tone layers pulsed at the same rate, a slow lowpass sweep that fades harmonic layers in and out, panned drifting pink/white/brown noise atmosphere, a drone a fifth below, and a 'journey' of timed beat-rate segments with smooth ramps (e.g. 10 → 1.5 Hz descent)
Source: [Binaural Beats Are Boring… So I Built Something Else | Bisochronic® Studio](https://www.youtube.com/watch?v=bFaYEPLlIxQ) · was `layered-binaural-plus-isochronic-architecture-carrier-left-carrier-plus-beat-right-octave-layers-pulse-ratio-locked-to-beat-sine-pulse-pingpong-pulse-harmonic-layers-lowpass-sweep-noise-drift-drone-fifth-journey-ramps`
- Set the carrier (e.g. 100 Hz pure sine) in the left ear and carrier + beat in the right (e.g. 104 Hz for 4 Hz). Check with headphones: removing one side leaves a steady tone.
- Add octave copies at half and double the carrier at lower level.
- Add an isochronic pulse with sine shape on a layer at ratio 1:1 to the beat; try half and double. Change the beat and confirm the pulse follows.
- Optional ping-pong: pulse the layer left/right instead of on/off and raise depth.
- Add harmonic/anchor tones (e.g. a fifth or 12th above, or chosen fixed tones) pulsed at the same rate or left steady.
- Put a slow lowpass sweep on the harmonic layers (start ~6 s period, then longer) with adjustable intensity.
- Add a low pink/white/brown noise layer with slow auto-pan, and a low drone a fifth below.
- Build a journey: hold each beat rate for set minutes and glide to the next (e.g. 5 Hz 5 min → 2 Hz 5 min → 1 Hz; or a 10 → 1.5 Hz descent); export and keep a card listing every frequency and ratio.
