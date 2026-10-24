# Pendulum-wave arpeggio (measured from Virtual Riot "Pendulum Sequence 2"): one repeating short note per scale lane, lanes slightly slower going down, so the figure drifts into staircases and curves and realigns after ~408 cycles

Goal: A reusable polyrhythm texture. Each pitch lane loops one note, and the period grows slightly from lane to lane. Played against each other, the lanes make a descending staircase that keeps phasing apart and then snaps back together. Stack ~10 detuned, offset copies for a shimmering wash. Original synthesis; only the pattern idea comes from the video.

Source: Virtual Riot "I heard you like polyrhythms" (Ableton). I measured the timing from the piano-roll frames; see `sample-lab/pendulum/timing-analysis.md`.

1. Set the tempo to 30 BPM. Make 35 lanes, E8 at the top down to E1, using E minor without C (thinning in the low register).
2. The top lane plays a note every 1/2 beat. Lane i plays at frequency f0·(N−i)/N, with N = 408; that is about +0.245 % period per lane, so the bottom lane is ×1.083 slower.
3. Note length is 0.37 × the lane's own period. All lanes start at the same moment; the staircase comes from the drift.
4. Voice: a 3-saw stack, lowpass at about 2.4 kHz, fast attack, exponential decay, top lanes a few dB quieter.
5. Stack 10 copies with about ±7 cents of detune, about ±9 ms of offset, and panning spread; add a short cross-delay. Target −15 LUFS, about −4 dBTP and side about −11 dB.
6. Arrange it as: sparse intro (every 3rd lane), full phasing, a realign moment (start the pattern N·period − x seconds in so the realign lands where you want it), then an outro.

Tool: `sample-lab/pendulum/pendulum_sequence.py workflows/pendulum-sequence-template.json out.wav [--iso]`. It writes a WAV, a MIDI file (SMF type 0, layer 0) and stats. `--iso` adds a 40 Hz raised-cosine isochronic layer.
