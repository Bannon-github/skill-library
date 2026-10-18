# Turn a flat sustained drone into rolling shaker-style percussion: loop and crossfade a stable bar, re-envelope it into rhythmic hits with a transient-preserving time-stretch gate at a fast note rate, then low-cut, boost one tuned mid harmonic, layer an organic shaker texture, snap it with a transient shaper and add a short parallel bright room

Goal: Recycle a pad/drone into tuned percussion without a drum source. Pick the steadiest, least peaky bar of the drone, loop it with short crossfades to avoid clicks, consolidate, then use a transient-preserving warp/stretch mode with a fast transient rate (the presenter starts at a 1/60-type rate for shaker speed) and reduce the per-transient sustain/envelope so each grid step becomes a hit. Add a fade-in, consolidate again, high-pass the lows, boost the strongest mid harmonic so the hit is in key (the presenter's was G#), layer a shaker/tambourine texture (less hold, more attack, a little decay, slight pitch, denser), add a transient shaper (attack up, sustain way down), tidy with EQ and finish with a short, bright, no-pre-delay room in parallel (~22 ms, mixed under the dry).

Source: [Crazy Percussions Out of a Pad in Serum 2](https://www.youtube.com/watch?v=EwxNeZttFEA)

1. Find the most stable, least peaky bar of the drone and loop it. Crossfade at each loop join so there are no clicks, then consolidate to one file.
2. Set a transient-preserving stretch mode with linear behaviour, choose a fast transient rate for shaker speed, then reduce the transient sustain/envelope until each step becomes a short hit. Raise level, add a small fade-in, and consolidate again.
3. EQ: high-pass the low frequencies that are not part of the percussion, then boost one or two mid harmonics so the part has a pitch that fits the tune or groove.
4. Layer an organic texture (tambourine/shaker-type) with less hold, more attack, a little more decay, slight pitch shift and higher density. EQ the texture to fill what is not poking through and reduce its decay.
5. Add a transient shaper: raise attack, remove a lot of sustain, adjust speed so it is snappy but not overdone.
6. Final EQ: bring up the gap left by processing, roll off extremes, and let the main harmonic breathe.
7. Put a very short bright room (no pre-delay, little depth, ~22 ms) on a parallel chain beside the dry signal and mix it under.

Batch: `2026-10-16-morning-hunt` · transcript: YouTube-provided (Show transcript) · DAW-specific warp UI mapped to a generic transient gate.
