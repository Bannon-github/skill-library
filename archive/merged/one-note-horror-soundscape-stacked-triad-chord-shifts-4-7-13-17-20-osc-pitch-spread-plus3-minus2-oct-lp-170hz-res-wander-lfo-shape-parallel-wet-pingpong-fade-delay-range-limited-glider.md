# Atmospheric horror / unsettling soundscape from one held MIDI note and one simple synth: a chord MIDI effect stacks two clashing major triads (shifts +4 +7 +13 +17 +20), the two oscillators are spread far apart (+3 and -2 octaves), a low-pass around 170 Hz with resonance about 6, a smooth-random 'wander' LFO on oscillator shape, stereo voice mode, a 100%-wet ping-pong delay with fade on a parallel chain whose rate/time/filter/width are moved by a separate smooth-random LFO with a narrow min/max range, then a large reverb

Goal: Build an evolving, clashing, dark soundscape for horror or tense game moments from a single trigger note. Dissonance comes from the polychord, depth from the extreme pitch spread, and motion from smooth-random LFOs whose ranges are clamped so the movement stays understated.

Source: [How to Make HORROR Soundscapes in Ableton Live](https://www.youtube.com/watch?v=2Yt1Ae91fv0)

1. Trigger one note (C3) with a one-bar or longer MIDI clip into a chord effect that adds the shifts +4, +7, +13, +17, +20.
2. Put a large reverb after the synth before you start sound design.
3. Pitch spread: oscillator 1 up about +3 octaves and oscillator 2 down about -2 octaves. Use a saturated/sharp shape on the upper oscillator with shape raised. Use a sine on the low oscillator, mixed up about +2.5 dB.
4. Low-pass down to about 170 Hz with resonance about 6, and clear any default filter modulation.
5. Set the synth LFO to a smooth-random ('wander') shape and route it fully to the upper oscillator's shape. Switch the voice mode to stereo (voices panned L/R).
6. Parallel delay: wrap a delay in a rack/parallel chain with dry kept, delay 100% wet, feedback about 80%, fade (crossfade) time mode and ping-pong on.
7. Add a separate smooth-random ('glider') LFO and map it to the delay filter, width, rate and feedback, then turn its depth down so the motion is slow.
8. Optionally map the LFO to the synth filter cutoff with a narrow min/max window (for example about 33-39%), raising it only to let in more mid frequencies.

Batch: `2026-10-30-morning-hunt` · transcript: YouTube-provided (Show transcript)
