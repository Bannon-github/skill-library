# Rebuild CZ-style phase-distortion shapes with an external phase chain (skew, formant, sync, fold)

Goal: Recreate Casio-like phase-distortion oscillator shapes in a modular/grid synth by driving a sine from an external phase ramp, then inserting skew, formant/PWM, fold+formant, and sync stages; animate the shape amount with an envelope for filterless brightness, and optionally raise a sync/frequency multiple for resonant overtones.

Source: [What is a Phase Distortion Oscillator and why is it](https://www.youtube.com/watch?v=TrkXgDQbhjk)

1. Start with a sine oscillator. Disable its internal phase (or set internal phase ratio to 0) and drive phase modulation from an external phaser/ramp at 100% so the sine returns.
2. Saw-like PD: insert a skew/bend on the phase so the ramp races through the first half and stretches the second (knee around 50% amplitude). Invert polarity if needed to match a reference Phase-1 oscillator.
3. PWM/formant-style: use a formant (or PWM) phase shaper so phase stays at the start, runs quickly through the cycle, then holds at the end until reset — classic pulse-width-like PD.
4. Folded variant: fold the lower half of the wave upward, then apply formant/PWM; for a precise match the transcript uses about −12 semitones on the formant stage and order matters (formant before the other stage).
5. Sync+skew: put a sync stage at +12 st (double frequency) then skew to slide the doubled humps together — another CZ-like bright shape. Whole-number octave sync ratios (12 or 24 st) keep the effect tonal.
6. Squeezed whole-wave: shift phase by about 25%, then move formant to squeeze the entire sine. Animate whichever shape control is primary with an ADSR (CZ historically used rich multi-stage envelopes on DCW).
7. Resonant tilt: raise the oscillator's frequency/sync multiple (or dedicated F control akin to sync) while modulating shape so overtones bloom like resonance — related to but not identical to plain sync.

Batch: `2026-10-09-morning-hunt` · transcript: YouTube-provided (Show transcript)
