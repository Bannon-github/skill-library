# Wavefolded LFO wobble: fold a sine LFO for extra peaks/valleys, then slew-limit it before filter cutoff

Goal: Make complex but smooth filter wobbles by running a plain sine LFO through a wavefolder (fold amount, symmetry, fold shape add peaks and valleys) before it reaches filter cutoff, then put a slew limiter after the folder so the folded modulation is less jumpy — a modulation-shaping recipe distinct from audio-rate wavefolding.

Source: [Wavefolding LFO's in VCV Rack to make interesting wobble effects and unique waves Synth Sound Design](https://www.youtube.com/watch?v=k9ZURoAww0k)

1. Baseline: route a regular sine LFO to filter cutoff and listen.
2. Insert a wavefolder between LFO and filter cutoff; compare the folded and plain sine on a scope.
3. Slow the LFO down (folding multiplies apparent rate) and adjust fold amount, symmetry and fold shape.
4. Add a slew limiter after the wavefolder, before the cutoff input, to soften the jumps.

Batch: `2026-10-14-morning-hunt` · transcript: YouTube-provided (Show transcript)
