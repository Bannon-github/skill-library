# Morph filter: LFO-cycle one filter continuously through LP → BP → HP → notch → LP

Goal: Animate pads, leads and repetitive noisy synths with a single continuous morph filter whose shape glides LP → bandpass → highpass → notch → back to LP, driven by a free-running (non-retriggered) LFO at 20–80% depth, optionally followed by a static classic low-pass, with LFO2 on cutoff and a little per-note random on the morph — a dedicated filter-shape morph recipe, distinct from parallel-filter chains, dual-path stereo spread and filter-flavor (ladder/diode/comb) choice.

Source: [Why does nobody use this filter ? (Ableton Morph Filter Tutorial)](https://www.youtube.com/watch?v=Z4mMGSg6ebY)

1. Select the morph filter mode. Understand the morph control: 0 = low-pass leaning toward the next shape; at 100 it is fully bandpass, then it continues to highpass, then notch, then back toward low-pass.
2. Set the slope to 24 dB and add a bit of resonance so the shape changes are clearly visible/audible while sweeping morph by hand.
3. In the mod matrix route LFO1 → filter morph at 100%, then pull the LFO amount back into the 20–80% range. Turn retrigger OFF so the motion continues across notes.
4. Pick the LFO rate: slow for pad movement, faster or tempo-synced for rhythmic motion. Then adjust the morph default position, cutoff frequency, LFO amount and rate together to find the sweet spot.
5. Use the second filter slot as a static classic low-pass after the morph filter to keep the tone in check while the morph adds movement.
6. Optionally add LFO2 → cutoff frequency (subtle), or replace filter 2 with a second morph filter whose morph is driven by LFO2 (try a different waveform).
7. For percussive/noisy or robotic repetitive sounds, apply the morph filter with a different LFO waveform and rate to smooth the sound.
8. Add a small amount of per-note Random (MIDI/mod matrix) to the morph amount/position so each note lands on a slightly different filter shape; A/B with the filter bypassed.

Batch: `2026-10-13-morning-hunt` · transcript: YouTube-provided (Show transcript)
