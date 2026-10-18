# Filtered feedback-delay resonator: bipolar feedback, swappable loop filter type, dry mute, insert on existing sounds

Goal: Turn a single filtered feedback delay into a playable 'renegade' Karplus-Strong voice and a resonator insert: impulse (noise burst or fast sine sweep, no loop) into a ~1–24 ms delay with feedback limited to ±99% (negative = hollow/odd-harmonic, positive = brighter), macro the in-loop filter type (LP/HP/BP/notch, with resonance on BP/notch) and cutoff as timbre controls, mute the dry click, map keys inversely onto delay time (long = low), then reuse the same delay as a metallic-body resonator on basses/pads — the delta beyond our key-tracked KS pluck skill is bipolar feedback polarity, loop-filter-type morphing, dry-mute and the resonator-insert use.

Source: [KARPLUS-STRONG synthesis in Renoise and the •REZONATOR•](https://www.youtube.com/watch?v=SfqgigefIu0)

1. Prepare a full-frequency impulse: a short white-noise burst or a fast sine sweep from very high to low frequency. Set it to one-shot (no loop) so it is only a click.
2. Insert a delay with feedback and an in-loop filter. Start around 24 ms delay, feedback 50%, effect amount full, filter low-pass fully open.
3. Make performance macros: (1) L+R feedback with range −99…+99 (centre = almost no repeats; negative = hollow square-like character; positive = saw-like), (2) delay time L+R capped at ~24 ms as 'pitch', (3) filter cutoff.
4. For keyboard pitch: map key tracking onto delay time inversely — lowest key → ~24 ms (slow cycle = low pitch), highest key → ~1 ms.
5. Add a macro for filter type (LP/HP/BP/notch) and automate/record it. With bandpass or notch, raise resonance somewhat — they sound better slightly resonant.
6. Mute the dry signal so the impulse click disappears and only the resonance remains; optionally add drive in the loop (can scream) and a following delay.
7. Try different impulse sources (sine, saw, more or less pitched) — the impulse strongly changes the timbre.
8. Resonator insert: put the same delay (wrapped in a macro rack) on an existing bass or pad; tune delay/filter to taste (check filter isn't left on high-pass), keep it subtle or brighter/distorted.
9. Resample interesting results for further processing.

Batch: `2026-10-14-morning-hunt` · transcript: YouTube-provided (Show transcript)
