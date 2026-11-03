# Synthesize a cinematic hit tail from white noise (LFO-shaped level, low boost, shared-LFO drive, Haas stereo, dark reverb)

Goal: Give an existing cinematic hit (pre-wash + sub + punch layers) body and a realistic reverb-like tail using only a white-noise generator: one LFO (or amp envelope) shapes the noise level, the same LFO drives distortion amount and a multiband compressor's mix/high band, heavy low boost and high cut make it sound like the hit's own tail, a 0-feedback single-side short delay makes it stereo, and a high-cut reverb blends it — a synthesized noise tail, not sample layering, braam, sub-drop, whoosh or downer.

Source: [Sound Design Tutorial: Synthesizing Tails for Cinematic Hits & Impacts](https://www.youtube.com/watch?v=q-N55tqLUr4)

1. Audition the hit layers (pre-wash, sub, punch) together and note the missing body/tail.
2. Init a synth: disable oscillator 1 and enable only white noise (any white-noise generator or sample works).
3. Shape the noise volume over time with an LFO used as a one-shot level contour (or the main amp envelope) so it swells/decays like a tail.
4. Drastically reshape the spectrum: filter to boost the lows a lot and cut the highs; make the bigger changes with EQ.
5. Add distortion and modulate its amount with the same LFO so drive follows the volume movement.
6. Add a multiband compressor; modulate its mix (and its high band) with the same LFO so it is not boosting the whole time.
7. Make it stereo: delay in stereo mode, time in seconds/ms, both at the shortest setting, then delay only one of the two sides; feedback 0, mix 100%.
8. Add reverb as the last step, cut the reverb's highs, and mix to taste.
9. Play with the other hit layers, compress/raise the tail, EQ further if needed, and add gentle compression on the group of all elements (back off if too much).

Batch: `2026-10-13-morning-hunt` · transcript: YouTube-provided (Show transcript)
