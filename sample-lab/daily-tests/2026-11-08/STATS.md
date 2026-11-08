# 2026-11-08 daily 3-skill test: "Pedal Bloom"

75 s (incl. 4 s tail), G minor over a D pedal (G pedal at the peak), 88 BPM, 26 bars. Drums in at 10.9 s (bar 4), pad only before that.

Skills
- staggered-attack-octave-layer-pad: per chord a sine-unison core (0.9 s attack), saw unison on its own filter (2.2 s attack, 4-bar slow-open/fast-close LFO on cutoff, ±15% random cutoff per chord), triangle +12 on a second filter (4.2 s attack, sine LFO on pan). Chords brighten as they hold. Foley step adapted: soft band-passed noise with a random level instead of clicks (Matt dislikes rapid clicking). Chorus, a crude 2-band upward lift for detail, ping-pong delay, reverb. Too dark on its own (tilt -9.0 dB/oct on iter 1) until the saw/triangle levels and cutoffs came up.
- drone-role-pedal-point-and-polychords: D2 sine pedal for the whole track with the chords (Ebmaj7, Cm9, Bb, Gm/D) moving above it; the pedal steps to G2 for the peak (step 6, the big recolour). Root-repeat 8th pulse, a fixed-pitch D4 through-line with a slow 8-bar sine-to-saw/square sweep (stand-in for wavetable position), and a static A4+D5 drone stack from the build for polychord rubs. Steps clear and applied.
- dynamics-restoring-saturation: drum bus through tanh (drive 3) in chain B, gain mapped from a muted peak follower on the dry bus (base 0.35, amount 0.65). Drum crest dry 16.8 dB, saturated 11.6 dB, restored 14.5 dB, so about 55% of the lost punch came back with warmth kept. Melodic parts ducked to the kick (step 5). Step 4 "adjust until hits match" has no numeric target; used crest factor as the check.

Score: 99.56 pass on iteration 3 (iter 1 92.71 fail, M6 tilt -9.0; iter 2 97.92, tilt -7.1; iter 3 tilt -6.63, M6 0.93). -17.0 LUFS, true peak -4.4 dBTP, limiter 0 dB GR. Side below 120 Hz -22.1 dB vs mid. HF transients only in the drum sections (none in the pad-only intro/outro).

Tweak: true peak is still -4.4 dBTP with zero limiting; raise folBase to 0.45 (less peak restoration) or add 2 dB of bus glue so the mix holds -17 LUFS with less wasted headroom. Library gap: a real multiband-compression step for pads (the skill names it but gives no bands or ratios).
