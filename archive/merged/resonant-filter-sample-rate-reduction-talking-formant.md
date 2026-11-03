# Talking/vocal formant voice from a resonant filter into sample-rate reduction (sweet-spot aliasing formants)

Goal: Create a talking, vowel-like voice without a formant filter: send a harmonically rich oscillator through a filter with healthy resonance and then a sample-rate reducer, find the sweet spots where aliasing creates formants, then animate it with a tempo-synced LFO on cutoff whose rate multiplier is stepped by a sequencer plus slow random modulation of the reduction amount, and send only content above ~1.5 kHz to a delay — a formant-voice delta that differs from formant-filter / spectral-vocode skills.

Source: [Creating a vocal formant speaking voice in VCV Rack](https://www.youtube.com/watch?v=gzJEQiTC_SQ)

1. Patch a harmonically rich oscillator into a filter and add a healthy amount of resonance.
2. Send the filter output into a sample-rate reduction stage (bit-crusher with sample-rate reduction) after the filter.
3. Slowly sweep the sample-rate reduction amount (and cutoff) to find the sweet spots where formants appear and the sound starts to 'talk'.
4. In a patch: sequence the rich oscillator, modulate the filter cutoff with a tempo-synced LFO, and use a step sequencer to change the LFO's rate multiplication per step.
5. Slowly and randomly modulate the sample-rate reduction amount for different timbres; bring the reducer's wet signal up gradually.
6. Send only the high frequencies (around 1500 Hz and above) through a delay as an extra layer.

Batch: `2026-10-13-morning-hunt` · transcript: YouTube-provided (Show transcript)
