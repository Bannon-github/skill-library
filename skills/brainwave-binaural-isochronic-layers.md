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

### Speaker-safe brainwave layer in a DAW: either two fixed-frequency sines a few Hz apart summed in mono (e.g. carrier + 8 Hz for alpha), or a tremolo (auto-pan set to tremolo, high amount, ~40% shape) at the entrainment rate on a playable pad so chords themselves pulse, optionally with the sine pair underneath
Source: [How to Create Monaural Beats in Ableton Live (Step-By-Step Tutorial)](https://www.youtube.com/watch?v=aBiz2axINMA) · was `monaural-beat-two-fixed-sines-or-tremolo-at-entrainment-rate-on-playable-pad-speaker-safe`
- Option A: load a sine synth, set the oscillator to fixed frequency at the carrier (a key note).
- Put it in a rack/group, duplicate the chain, and set the second sine to carrier + target rate (e.g. +8 Hz). Keep both centred (mono).
- Check: mute one chain and the wobble disappears; both together give the monaural beat.
- Option B: on a pad or chord track, add a tremolo (auto-pan in tremolo mode), raise the amount high, set shape ~40%, and set the rate to the target Hz (e.g. 8 Hz).
- Turn off fixed pitch so the instrument plays normally; play chords and melodies so the whole harmony pulses.
- Add reverb after the tremolo and, if wanted, keep the Option A sine pair quietly underneath.
- Optionally copy the same tremolo onto other tracks of a meditation piece, then test-listen at length before sharing.

### Rate-ramp brainwave layer: a binaural pair centred on a fixed carrier (e.g. 200 Hz) with the beat split symmetrically (carrier minus beat/2 left, plus beat/2 right) and the beat rate moved over time, either as one eased (slow-fast-slow) ramp from a start to a target rate (e.g. 6 -> 1.5 Hz over minutes) or as a 'gearbox' of band steps (16 -> 10 -> 6 -> 2 Hz) that dwell for minutes and shift over ~1-1.5 min, with an optional return trip; a harmonic second pair (fifth/octave/12th) keeping the same gap, an isochronic amplitude pulse at the same rate blended in for speakers, and a brown-noise bed
Source: [Binaural Beats Explained: Build One in Your DAW with Binaura](https://www.youtube.com/watch?v=00oV6DJkK3E) · was `binaural-rate-ramp-eased-symmetric-offset-gearbox-dwell-shift-band-steps-harmonic-same-gap-isochronic-blend`
- Pick the carrier: e.g. 200 Hz, or an octave above the bed's drone root (A2 drone -> 220 Hz carrier) so it stays above the bass.
- Set the start beat: left sine = carrier - beat/2, right sine = carrier + beat/2 (6 Hz at 200 -> 197 L / 203 R); hard-pan each.
- Classic ramp: draw automation on both oscillators so the gap moves from the start to the target rate (e.g. 6 -> 1.5 Hz) over the ramp time, with an S-shaped (eased) curve; both frequencies move symmetrically.
- Gearbox alternative: write a schedule of band steps without skipping a band (e.g. 16 beta -> 10 alpha -> 6 theta -> 2 delta Hz), hold each for a dwell (default ~4 min; 30 s for previews) and shift between them over a gear-shift time (~1.5 min; 15 s for previews).
- Decide the ending: return trip (back up 2 -> 6 -> 10 -> 16), hold the last band and fade out after one dwell, or hold the final rate to the end.
- Optional harmonic: add a second pair at octave (397/403 for 200 Hz + 6), fifth (1.5x) or 12th (3x) of the carrier with the same gap, both pairs following the same rate automation.
- Optional isochronic blend: tremolo/VCA on the tones at the current beat rate (follows the same automation), depth ~0.6 for a partial dip or 1.0 to silence.
- Add a brown-noise bed (~-26 dB) and fade the whole layer in over ~10 s; set tone peak ~-14 dBFS; place under the pad/drone.

### Binaural 'meet them where they are' staged rate ramp: two fixed-frequency sine voices hard-panned L/R, right voice automated by clip envelope from beta to alpha (and on to theta and back), fast early drop then slow glide, one long note per layer so there is no loop-restart click, sat at about -24 dB under a 60 BPM drone bed
Source: [BINAURAL BEATS IN ABLETON - How to create and how to use them for healing and meditation music](https://www.youtube.com/watch?v=k40nANMRnG4) · was `binaural-staged-rate-ramp-meet-listener-in-beta-clip-envelope-presets-long-note-no-loop-click-minus-24db-bed`
- Create a MIDI track with a fixed-frequency synth (Operator: disable oscillators B-D, set A to Fixed, 200 Hz). Group it into an instrument rack and duplicate the chain; name the chains Left and Right and pan them hard left and hard right.
- Draw one note in a long clip (e.g. 144 bars, grid set to 8 bars, note stretched across the whole clip). The pitch of the MIDI note does not matter because the frequency is fixed.
- Make static preset clips: in each clip's envelope set the Right chain's frequency to carrier + beat (204 Hz = 4 Hz theta, 210 Hz = 10 Hz alpha) and name the clip after the state.
- Make a ramp clip: put a breakpoint at the start at the listener's likely state (e.g. 215 Hz = 15 Hz low beta) and one at about 4-5 minutes at alpha (207-208 Hz). Name it '15 Hz beta to 8 Hz alpha'.
- Longer journey (optional): start at 240 Hz (40 Hz) and drop most of the way within the first minute (e.g. to ~225 Hz by bar 17 at 60 BPM), then continue slowly to 214 Hz (14 Hz). Chain further stages into alpha, theta, then back to alpha. Copy the clips to the arrangement timeline for a fixed release, or launch them live from clip view for sessions.
- Set the project to 60 BPM, add a drone or pad bed (plus optional nature/water ambience and a soft lead), and pull the binaural layer down to about -24 dB. Check on headphones.

### Tempo-synced amplitude gate on a long ambient texture made from an auto-pan: beats mode at 1/16, stereo phase raised to 360 deg so left/right move together (on/off volume instead of panning), edge softness set with the shape and waveform controls, then a reverb after the gate to smooth it; amount knob brings the gate in and out
Source: [Ableton Live Tutorial - Gated Textures using Autopan](https://www.youtube.com/watch?v=RDubhupxDsw) · was `tempo-synced-autopan-phase-360-amplitude-gate-on-long-ambient-texture-shape-softened-edges-reverb-after-gate-amount-as-on-off`
- Drop the long texture on an audio track (an intro or breakdown element) and add an auto-pan; turn its amount up to hear it move left and right.
- Switch the auto-pan to beats (tempo-sync) mode and set the rate to 1/16.
- Raise the phase offset to 360 degrees.
- Fine-tune the gate edges with the shape control and the waveform selector (rounded/sine-like for soft pulses).
- Add a reverb after the auto-pan and raise its decay for a large room/hall, to soften the gating.
- Play it with the beat and automate the auto-pan amount down/up to take the gate off and bring it back between sections.
