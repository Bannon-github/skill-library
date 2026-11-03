# Buchla 291-style morphing bandpass: 6-pole bandpass with two clocked step sequencers (frequency and bandwidth) as filter snapshots, wet/dry crossfader

Goal: Build a free West-Coast-style morphing filter: a steep 6-pole bandpass (bandwidth instead of resonance) fed a harmonically rich complex oscillator, with two clocked, randomized 8-step sequencers — one on frequency (v/oct, ±10 V) and one on bandwidth (0–10 V) — so each clock step jumps to a new 'filter snapshot', blended with the dry signal on a crossfader like an aux, plus optional LFO on the main frequency; copy the voice for a triple morphing filter.

Source: [How to make your own Buchla Style Morphing Filter in VCV](https://www.youtube.com/watch?v=NFWAC2kLqvo)

1. Choose a multimode filter, set it to bandpass and the slope to 6 poles (type the value precisely); set bandwidth to 100%.
2. Feed a complex oscillator; brighten/complexify it and raise the pitch until the bandpass has harmonics to work with. Sweep bandwidth to hear the change.
3. Add two step sequencers: one to filter frequency (v/oct), output range ±10 V; one to bandwidth, range 0–10 V.
4. Put a crossfader after the filter: filtered signal on A, dry signal on B, so the filter acts like an aux/wet-dry morph.
5. Clock both sequencers, randomize all steps, set 8 steps forward, and run: each step recalls a different frequency+bandwidth 'snapshot'.
6. Adjust main frequency/bandwidth controls live and optionally modulate main frequency with an LFO via CV.
7. For a triple morphing filter, duplicate the whole voice (filter + two sequencers) and offset settings.

Batch: `2026-10-14-morning-hunt` · transcript: YouTube-provided (Show transcript)
