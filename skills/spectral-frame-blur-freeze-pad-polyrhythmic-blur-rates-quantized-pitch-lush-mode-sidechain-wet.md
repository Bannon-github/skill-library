# Spectral blur/freeze pad: capture incoming audio as spectral frames and morph frame-to-frame at tempo-synced blur rates (quarter notes, plus simultaneous triplet/dotted rates for polyrhythms) with a per-frame attack/decay envelope, pitch the blurred signal ±24 st (semitone-quantised), choose clicky vs lush modes, play frames forward/backward, freeze completely, and modulate with curves, cross-modulation and a kick-sidechained follower on dry/wet

Goal: Turn any input into lush pads or frozen textures with a spectral frame effect. The input is analysed into momentary spectral snapshots (frames, like video frames). Instead of playing them in order, the effect morphs from one frame to the next at a blur rate (e.g. one frame per quarter note); several blur rates can run at once, including triplets and dotted values, for blur polyrhythms. A per-playback envelope (attack/decay) makes the stepping audible or smooth. Pitch the blurred signal up/down to 24 semitones, quantised to exact semitones when needed. Pick an algorithm flavour: the default/rhythmic sound is harsh and clicky-metallic; lush/melodic washes it out. Set playback direction forward/backward and use freeze to stop morphing entirely. Modulate the envelope and pitch with drawn curves (invert/shift/skew/morph between curves), cross-modulate the first layer's LFO rate, and use a sidechained envelope follower (kick) to move dry/wet and curve amounts. Partly fills our open spectral (FFT) freeze-pad gap.

Source: [Magic Blur - Overview and Tutorial](https://www.youtube.com/watch?v=mllvToyambI)

1. Insert the spectral blur on a source and set one blur rate (a quarter note: one frame morph per beat).
2. Adjust the per-playback envelope (attack/decay) to hear or hide the frame steps.
3. Add simultaneous blur rates including triplets and dotted notes for polyrhythmic blurring.
4. Pitch the blurred signal up or down (to ±24 st), enabling semitone quantisation for musical intervals.
5. Choose the flavour: rhythmic (clicky metallic), melodic or lush (washed out), or mixed; set playback direction forward/backward.
6. Enable freeze to stop the frame morphing and sustain the captured spectrum.
7. Modulate envelope and pitch with drawn curves (randomise, invert, shift, skew, morph between up to four curves); cross-modulate the first layer's LFO rate; add an envelope follower in sidechain mode from the kick to move dry/wet and curve amounts.

Batch: `2026-10-16-morning-hunt` · transcript: YouTube-provided (Show transcript) · Short product overview; procedure is spoken behaviour, not on-screen values.
