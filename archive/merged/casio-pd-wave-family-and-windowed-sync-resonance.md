# Casio PD wave family: saw-pulse, double-sine, pulse, square, and windowed-sync resonance

Goal: Expand Casio-style phase distortion beyond the basic saw: derive saw-pulse (sine table), double-sine (warp twice / half-rate), pulse (node at full height with end hold), true square (run the warper twice per cycle), and resonant 'windowed sync' waves (slave sync reset enveloped by a decaying window to remove the click), then thicken with unison.

Source: [GroovyDSP: More Phase Distortion!](https://www.youtube.com/watch?v=94vSgZXg1nQ)

1. Start from the piecewise phase warp (fast then slow read). For the classic saw, use a cosine table with the knee near mid-amplitude (y≈0.5).
2. Saw-pulse: swap the cosine table for a sine table under the same warp (first half read fast, second slow) to get the CZ saw-pulse family shape.
3. Double-sine: apply the same shaping so one full sine cycle is played fast and the next slow (or conceptually run at half rate with the warp), producing a weird octave/double-sine texture.
4. Pulse: raise the node height (y-position) toward 1.0 so the fast segment climbs higher and the cycle then waits/holds at the end before resetting — a pulse with end dwell. Cosine or sine both work; Casio often used sine.
5. Square: run the warping function twice per cycle (multiply phase by 2 then wrap 0→1 before the piecewise map), i.e. twice-per-cycle instead of once — Casio's fuller square uses the full 100% cycle read this way rather than a weaker half-cycle squish.
6. Resonance / windowed-sync: run a higher-rate sine (or oscillator) that is hard-synced/reset by the fundamental, then multiply by a decaying amplitude window each master cycle so the sync gap/click is enveloped away — an exponentially decaying sine burst that mimics filter resonance.
7. Optional CZ trick: alternate wave shapes cycle-by-cycle (e.g. square then saw) so the ear hears one compound cycle. Add a unison/detune ('fat') layer for organic thickness on leads/pads.
8. Expose skew/y as a continuous 'DCW' macro and modulate it with envelopes for plucky filterless motion; keep pitch from the master phase ramp only.

Batch: `2026-10-09-morning-hunt` · transcript: YouTube-provided (Show transcript)
