# Scale-locked high-end atmosphere layer: sporadic random note 'sprays' (sine-like and brighter 'glass' voices) above ~3 kHz with a gravity/rate control, plus pitch-locked air and dust noise layers on random-drift LFO levels and a long reverb

Goal: Fill the empty 3 kHz–20 kHz zone of an ambient track with musical, pitch-locked detail instead of generic noise. Lock everything to the track's key and scale (e.g. B minor pentatonic). Generate sporadic random notes from two voices on different patterns: a sine-like 'spray' and a buzzier, brighter 'glass' with tone controls. Set note density with a gravity/rate control, free or tempo-synced from 1/16 up to 16 bars. Add an 'air' white-noise layer and a 'dust' blown-sand noise layer, both of which can be pitch-locked so they take on tonality: air follows spray's pattern and dust follows glass. Move each layer's level with slow LFOs (including smooth random drift). Send it all to a big reverb (size, decay, tone, mix, pre-delay, diffusion, modulation), limit the output, and optionally feed note choices from a slow generative MIDI source. Check the result on a spectrum analyser. This is a generative high-band layer, not a pad or riser.

Source: [Airglow Walkthrough: A High-End Atmosphere Instrument for Ambient Music](https://www.youtube.com/watch?v=LeChNmmtNsM)

1. Analyse a reference ambient track's spectrum: note the active, sporadic, pitch-locked detail between ~3 kHz and 20 kHz.
2. Set the key/scale lock to the track (e.g. B minor pentatonic) and trigger the generator; random notes from the scale are sprayed out.
3. Slow it down with the gravity/rate control so notes arrive slowly; raise the reverb ('glow') amount for long trails. Alternatively switch to tempo sync and choose intervals from 1/16 up to 16 bars.
4. Blend the two tonal voices: spray (standard sine-like tones) and glass (sharper, buzzier shine), each with a tone control and different patterns, so they don't fire together.
5. Add the air layer (white noise that 'blows in the distance') and modulate its level with an LFO (e.g. smooth random drift) so it comes and goes. Add the dust layer (sand-scatter-like noise) the same way with the second LFO.
6. Pitch-lock the noise layers: air follows spray's note pattern and dust follows glass, so the noise gains tonality in key.
7. Shape the reverb (size, decay, tone, mix, pre-delay, diffusion, modulation/chorus), use the output limiter and +6 dB make-up if quiet. Optionally drive pitches from a glacially slow generative MIDI pattern. Then confirm on the full-mix spectrum that the high end is filled.

Batch: `2026-10-15-morning-hunt` · transcript: YouTube-provided (Show transcript) · Developer plugin walkthrough; route.py said COVERED but hand-check found no high-band generative sparkle skill. Plugin purchase CTA dropped.
