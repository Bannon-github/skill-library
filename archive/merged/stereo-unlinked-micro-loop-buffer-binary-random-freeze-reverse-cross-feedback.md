# Glitchy micro-loop buffer for ambient textures: freeze-and-scan buffer with segment length, pitch that cascades through feedback, temporary pitch from sample-rate steps, unlinked L/R (+12 / −12 st with cross feedback) and binary-random LFOs toggling freeze and reverse per side

Goal: Recreate boutique 'micro-looper' pedal textures with one buffer-delay device. A delay whose position = delay time, feedback = repeats, and segment = how much of the capture plays, plus reverse and a hold/freeze that captures the buffer so position scans it. Add random start position (plus an LFO), a short range for finer control, pitch shift (an octave or a fifth; it cascades up with every feedback pass, so use the high-cut), sample-rate steps that create temporary pitch drops and crunch, vibrato, and a low/high-cut band-pass. Unlink L and R for independent positions, segments, pitch and LFOs: L +12 st, R −12 st with cross feedback. Then automate with binary (random on/off) LFOs at unequal rates on freeze L/R and on reverse L/R, plus a random LFO stepping the sample-rate/bandwidth, and optionally a hybrid reverb. Lower dry/wet for a background whisper. Delta vs our granular-freeze, reverb-freeze and shimmer skills: per-channel random binary freeze/reverse and octave-split cross feedback.

Source: [Ableton's best kept secret for ambient textures](https://www.youtube.com/watch?v=KVtxIwYpGvQ)

1. Insert the buffer delay. Learn the basics: position = delay time, feedback = repeats, segment = how much of the captured audio plays back, reverse toggle.
2. Freeze/hold: play a phrase and engage hold. Now position scans through the frozen buffer and segment sets the loop length. Add random start position (and/or an LFO), and use short mode for fine, small segments.
3. Pitch: set +12 st (or a fifth). Each feedback pass pitches up again, so engage the high-cut to tame the cascading brightness. Try sample-rate steps (e.g. 10k, down an octave and again) for temporary pitch effects and crunch; add a little vibrato. Low and high cut together give band-pass tones.
4. Unlink L/R channels so each has its own position, segment, pitch and LFO. Set L +12 st and R −12 st, and set the feedback routing to cross (each side feeds the other).
5. Map the important controls to macros. Add two LFOs in binary (random on/off) mode at different rates on freeze L and freeze R, set as remote control so they aren't hand-moved.
6. Add two more binary LFOs on reverse L and reverse R, and one random (not binary) LFO with full range on the sample-rate/bandwidth control that steps between octave settings.
7. Optionally add a hybrid reverb, and lower dry/wet so the effect becomes a whisper in the background.

Batch: `2026-10-15-morning-hunt` · transcript: YouTube-provided (Show transcript) · Stock-device deep dive; route.py said COVERED but hand-check found per-channel binary freeze/reverse and cross-feedback not covered. Gumroad promo dropped.
