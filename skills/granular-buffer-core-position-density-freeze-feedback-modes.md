# Granular buffer core from the ground up: grain size/shape/pitch, regular vs random density, triggered grains as a voice, position delay, freeze scrubbing, partial re-freeze, random pan, two feedback modes

Goal: Understand and drive a buffer-based granular processor (the kind we need as a Web Audio module) with reverb and feedback turned down first: grains are tens-of-ms-to-1-s micro-samples plucked from a rolling 1–8 s input buffer; set size, shape (gate → triangle → Hann for overlap), pitch; density from noon (none) toward regular spacing one way and random spacing the other, or fire grains from a trigger with sequenced pitch to make a playable voice; use position as a buffer read point (= delay, newest at one end), freeze to scrub inside captured audio, gate the freeze with semi-random gates to partially overwrite and blend the buffer, mind lo-fi buffer modes (low sample rate → low-pass before input; mu-law 8-bit → keep input mid-level), random L/R grain pan for mono→stereo, and know that feedback is true input feedback when live but a separate delay/all-pass diffuser when frozen.

Source: [Clouds (and clones) from the Ground Up: a reverbless explanation of a Granular icon](https://www.youtube.com/watch?v=mBvUObtJTJI)

1. Turn internal feedback and reverb down. Feed a simple source (sine) and listen to individual grains.
2. Grain structure: size sets grain length (tens of ms → ~1 s); shape/texture morphs from no contour (gate) through triangle to Hann-like windows; use gate-like shapes for individual grains and Hann for overlapping grains; pitch shifts each grain up/down.
3. Grain generation: density at noon = no grains; one direction = evenly spaced grains getting faster until they overlap; the other = randomly spaced grains until they overlap. Fine control near noon matters for counting individual grains.
4. Triggered voice: density at noon, feed clock-derived gates into the trigger input and quantized pitch per grain from a random/looping sequencer; send an occasional pulse into size to lengthen some notes.
5. Position: switch to a varied source (speech/radio). Small grains + enough density reconstructs the input; moving position away from the newest end adds a growing delay (there's always a tiny conversion delay at minimum).
6. Freeze (fully wet): buffer stops updating; the same grain repeats at the current position; shrink size from a whole word to a tiny tone, then sweep position to scrub through captured audio (note: newest audio sits at one end, so 'forward' playback means moving position toward the older end).
7. Evolving buffer: gate the freeze input with semi-random gates so it briefly unfreezes, writing a few seconds of new audio at the front while the rest of the buffer is kept.
8. Post-processing: set wet/dry blend; use random L/R grain panning to turn a mono input into a stereo output; add reverb externally if preferred.
9. Feedback: when live, it's true feedback of output into the buffer input (can run away — tame by modulating size/position); when frozen, feedback becomes a separate delay + all-pass diffusion that sounds reverb-like without altering the buffer. Watch for jumps when unfreezing.

Batch: `2026-10-14-morning-hunt` · transcript: YouTube-provided (Show transcript)
