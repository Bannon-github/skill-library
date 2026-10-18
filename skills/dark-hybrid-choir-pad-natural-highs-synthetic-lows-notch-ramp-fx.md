# Dark hybrid vocal pad: choir-like wavetable plus an octave-up choir sample FM'd in (~34%), with sub and a little noise. Lows/mids are low-passed while the natural sample keeps the highs, a subtle LFO notch moves the mids, and one slow rising ramp drives the FX

Goal: Build a dark, haunting vocal pad for intros, breakdowns or tension layers by blending a real choir sample with synthetic layers that sound vocal. Osc A: a choir-type wavetable with chorus-like unison and its position moved by a single slow, rising ramp (one main movement). Osc B: a choir multisample an octave up with light tube saturation, frequency-modulating A at ~34% for grit. Add a default sub (choir has little sub) and very low white noise (or hum) for full-spectrum air. Route A + sub through a low-pass, but keep B (natural) out of it so the high end comes from the real voice. Then all go into filter 2, a subtle notch (~18%) whose amount and cutoff move on the LFO for mid-range expression. FX: a blended, very wide frequency-shifter/blur stereo layer (mix ~half), dimension ~6%, hyper-chorus automated up to ~32% at the top of the ramp, ping-pong delay ~10–11%, distortion only above ~300 Hz, a little comb, reverb ~10%, then a high-end presence boost. Delta vs our pad skills: natural-highs / synthetic-lows routing and the single-ramp FX bloom on a vocal pad.

Source: [The Secret to HUGE Dark Vocal Pads in Serum 2](https://www.youtube.com/watch?v=Futy449F9OY)

1. Osc A: choir-like wavetable, unison for chorus, slight low-pass. Create one main modulator, a slow triangle that effectively ramps up, on wavetable position (and later FX amounts).
2. Osc B: choir multisample an octave higher with a bit of tube saturation, defaults otherwise. FM it into osc A at ~34% for a touch of grit.
3. Add a sub oscillator at default level under everything, and white noise (or hum) at a very low level for full-spectrum air.
4. Filter 1: low-pass on osc A + sub only; route osc B around it so the natural choir provides the high end.
5. Filter 2 on the combined signal: notch at ~18% mix (100% shows the full effect), with the amount rising on the LFO and the cutoff moving slightly too, for mid-range expression and cohesion.
6. FX 1: a frequency-shifter/blur stereo layer, mix ~half, blur ~half, shift and range lowered, blended in as a moving super-wide layer. Dimension ~6%. Hyper-chorus automated from low up to ~32% at the top of the ramp.
7. FX 2: ping-pong delay ~10–11%; distortion with a high-pass so only ~300 Hz upward is saturated; a little comb filter (macro candidate); reverb ~10%; final high-shelf presence boost.

Batch: `2026-10-15-morning-hunt` · transcript: YouTube-provided (Show transcript) · Preset walkthrough; factory content names omitted; pack promo dropped.
