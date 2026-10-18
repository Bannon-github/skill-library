# Karplus-Strong pluck: noise-burst exciter into a key-tracked feedback delay with decay/damping and register compensation

Goal: Build a playable Karplus-Strong plucked string in any modular/Web Audio environment: a short pink-noise burst (bandpass-filtered, velocity-scaled, optionally stereo) excites a delay line tuned to one period of the note (delay = 1/f, e.g. ~7.64 ms at C3; halve per octave up via 2^(−n/12) scaling), with feedback as decay and a low-pass in the loop as damping, both velocity-scalable and key-tracked to even out low-vs-high note ring time.

Source: [Karplus-Strong Synthesis in Bitwig Studio 3 - The Grid](https://www.youtube.com/watch?v=8b5EX9HcPGk)

1. Build the exciter: pink noise (fuller than white) → bandpass SVF → a very short pluck envelope on level; add a velocity multiplier to scale excitation, and gain to keep long exciters in check.
2. Feed the burst into a delay with built-in feedback and an in-loop low-pass. Set delay = one period of the target fundamental (7.64 ms ≈ C3) and feedback high so it keeps resonating.
3. Key-track the delay: delay time must scale by 2^(−n/12) (n = semitones from the reference). Going up an octave halves delay; down an octave doubles it. Convert the note-pitch value to that factor (exp base 2, invert, offset so the reference note = no change) before feeding the delay-time modulation.
4. Exciter variations: use the envelope itself as the exciter (attack time changes tone like pluck position); widen the noise stereo for a lush tone; long exciter envelopes give a reverb-like bloom.
5. Map Decay → feedback (near unity = rings forever; low = unpitched thump) and Damping → loop low-pass (palm-mute-like). Optionally scale both by velocity (harder = longer ring/less damping); keep velocity amounts low—it is touchy.
6. Compensate register: at equal feedback low notes ring longer than high notes, so key-track feedback up for high notes and adjust damping in the opposite direction so decay and brightness feel even across the scale.
7. Experiment: feed other sounds as the exciter into the tuned delay for pitched resonant textures.

Batch: `2026-10-13-morning-hunt` · transcript: YouTube-provided (Show transcript)
