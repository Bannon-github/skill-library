# Add an isochronic pulse layer under an existing track: a sine (or noise) carrier played by one long MIDI note, amplitude-pulsed at a chosen rate (e.g. 4 Hz) with a smooth-step pulse shape and a 0–100% isochronic blend, faded in and out by gain automation, with the pulse rate automated (e.g. 15 Hz → 4 Hz → 15 Hz) using ~10 ms parameter smoothing, carrier tuned by reference (440/432) or a custom note-to-frequency map and verified with a tuner, then mixed barely audible

Goal: Build the Mind Amend-style isochronic layer as its own track. A tone generator plays a sine carrier from MIDI; with beat frequency 0 it is just a plain sine. Pick the pulse rate (e.g. 4 Hz) and raise the isochronic blend from 0% (steady tone) through 50% to 100% (full on/off pulses); choose a smooth-step pulse shape for focused but soft pulses. An amplitude-pulsing (LFO/tremolo) device lets you pulse noise or any audio as well. Use one long MIDI note for an uninterrupted tone (chords also work and pulse together). Fade in over about 30 s and out over 30–60 s with gain automation. Automate the pulse rate with exact typed breakpoints (e.g. start 15 Hz, glide to 4 Hz, return to 15 Hz at the end) and set the device's parameter smoothing to its minimum (0.01 = 10 ms) for automation. Keep pulse rates low (the speaker suggests below ~100 Hz); carrier frequencies (e.g. 432 Hz reference tuning, or a custom mapping where a note equals 528 Hz) are a separate layer of choice; check the actual pitch with a tuner set to the same reference. Finally set the layer's level in the mixer so it sits barely audible under the music. Polyrhythm Studio: OscillatorNode → GainNode whose gain follows a pulse-shaped LFO at rate r(t) with a ramped automation curve.

Source: [How to Create Isochronic Tones in Ableton Live with Huon Studio](https://www.youtube.com/watch?v=WNewLv-kI2I)

1. Create a MIDI track with the tone generator; set the device output low (about -20 dB) so the layer starts quiet.
2. Program one long MIDI note (or loop a short note while designing; chords also work).
3. Set the pulse rate (e.g. 4 Hz) and raise isochronic blend from 0% to 100%; choose a smooth-step pulse shape.
4. Add a gain utility and automate a ~30 s fade-in at the start and a 30–60 s fade-out at the end.
5. Expose the pulse-rate parameter for automation, set parameter smoothing to 0.01 (10 ms), and draw breakpoints with typed values: 15 Hz at the start, 4 Hz in the middle section, back to 15 Hz at the end.
6. Optional carrier tuning: switch the tuning reference (440 → 432 Hz) or load a custom note-to-frequency map and find the note that gives the target frequency (e.g. 528 Hz); confirm with a tuner set to the same reference.
7. Set the track fader so the layer is barely audible under the music.

Batch: `2026-10-22-morning-hunt` · transcript: YouTube-provided (Show transcript) · Two-person screen-share session; off-topic chat dropped; product UI mapped to generic tone generator + amplitude pulse.
