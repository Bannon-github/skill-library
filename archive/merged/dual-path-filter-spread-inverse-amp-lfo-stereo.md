# Stereo from mono: opposite filter frequencies plus inverse amplitude LFO

Goal: Widen a mono synth path without Haas delay: split into L/R, offset parallel filter cutoffs in opposite directions (plus/minus frequency spread), then apply a unipolar LFO to left amplitude and its inverse (1−x) to right amplitude so levels see-saw in opposite phase — a modular stereo image that differs from Haas, mid/side EQ, and double-tracked asymmetric processing.

Source: [How to Make your Synthesizer Stereo](https://www.youtube.com/watch?v=02_MBQrqJS8)

1. Start from a mono voice (tutorial: two simple waves + white noise → mixer → HP/LP → envelope). Confirm it is centered.
2. Frequency-spread stereo: put a filter (or filter pair) into a plus/minus or dual-cutoff mode and offset the cutoff so left and right emphasize different bands. This alone creates a static spectral stereo image.
3. Duplicate the signal into explicit left and right amplitude paths after the envelope (or duplicate the mixer into L/R).
4. Create a unipolar LFO. Multiply the left path by the LFO. Build the right modulator as inverse unipolar: multiply LFO by −1 then add 1 (or use 1−x) so when left is loud, right is quiet and vice versa. Multiply the right path by that inverse.
5. Alternate simpler wiring: two attenuators on L and R modulated with opposite depths from the same LFO. Compare against the multiply version — both yield opposite-amplitude stereo.
6. Audition in stereo and mono. Reduce spread or LFO depth if mono pumps or hollows. Combine later with gentle M/S EQ if lows got too wide.

Batch: `2026-10-12-morning-hunt` · transcript: YouTube-provided (Show transcript)
