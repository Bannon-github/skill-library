# Four-layer wave-sequenced cinematic pad: crossfaded seconds-based wave sequence, released keys layer, LFO-rate-modulated analog layer, tempo-locked rhythmic step layer with shape/ratchet/probability

Goal: Build an evolving cinematic pad from four complementary layers: (1) a smooth wave sequence that crossfades between several string-like sources at seconds-based step times (~1 s) with slow attack/release, compression, tape delay and reverb; (2) a plain keys/piano layer with long release, gentle velocity-sensitive filter envelope and its own delay; (3) a synthetic layer sequencing between two different saw sources through a filter envelope, with a free-running LFO whose rate is itself modulated by a second slow free-running LFO (plus a touch of pitch deviation and panning from that LFO); (4) a tempo-locked (quarter-note) step layer with crossfade off, using saw-down/triangle step shapes on cutoff, double/triple ratchets at reduced probability and a tempo-synced filter LFO — then balance layers and put the busiest one on a macro.

Source: [Wavestate Cinematic Pad in Minutes](https://www.youtube.com/watch?v=28uxHnQbulE)

1. Layer 1 (smooth wave sequence): choose 3–4 string-like sources moving from acoustic chamber/orchestral strings toward a synthetic string; set step time in seconds (~1 s per step) with crossfade on so each source melts into the next.
2. Layer 1 envelope + FX: slower attack, some release, lengthen crossfade slightly; add compression, tape delay and master reverb (chorus not needed).
3. Layer 2 (keys): a single piano/keys source with a long, nice release; optionally lower cutoff with a release-shaped filter envelope, make it velocity-sensitive, add a different delay. A phaser was tried but softened the attack — compression worked better to give the keys impact over the strings.
4. Layer 3 (analog-style): wave-sequence between two different saw sources for variety; filter with filter envelope and tape delay.
5. Layer 3 motion: route a free-running LFO to the layer (e.g. filter/level), then use a second, very slow free-running LFO (the spare pan LFO) to modulate the first LFO's speed so it speeds up and slows down; use that slow LFO also for a tiny pitch deviation and for panning.
6. Layer 4 (rhythmic): new wave sequence in tempo mode (quarter notes, speed up later) through synthetic/spectral and vocal-like sources; turn crossfade off so steps are audible.
7. Shape the steps: give the step lane a saw-down shape (a pulse of 100 that decays to 0 = pseudo-envelope per step), lower cutoff and apply the step shape to cutoff; add double/triple ratchets on some steps and lower their probability so it isn't jarring; add a tempo-synced filter LFO and interesting delays.
8. Key-sync the rhythmic layer's steps so chords start in sync; optionally jump the last step up one or two octaves.
9. Balance: bring the busy analog layer down, map it (or the rhythmic layer) to a macro knob for real-time control.

Batch: `2026-10-14-morning-hunt` · transcript: YouTube-provided (Show transcript)
