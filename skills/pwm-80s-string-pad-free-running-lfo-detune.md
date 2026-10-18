# 80s PWM string pad: pulse wave with free-running (seconds-based) LFO on pulse width, slight osc-2 detune, slow attack/release, static filter

Goal: Build a classic 1980s string pad from an init patch: switch the oscillator from saw to pulse, modulate pulse width from an LFO set in seconds (free-running, ~0.7, not tempo-synced so the ensemble rate never changes with song tempo), blend a second oscillator ever so slightly detuned, low-pass to remove the very high end with the filter envelope and other filter mod sources switched off, slow fade-in attack and long release — a dedicated PWM string pad distinct from our PW drone and unison string-section skills.

Source: [80s String Pad Tutorial (1/2) - Pulse Width Modulation in Tyrell N6](https://www.youtube.com/watch?v=0n23itgG0LU)

1. Start from an init patch; keep a scope visible. Change oscillator 1 from saw to pulse (square = 50% duty cycle; pulse widths roughly 10–90% duty).
2. Route an LFO to pulse width and watch the scope: the pulse width sweeps.
3. Switch the PW LFO from tempo-sync to free-running seconds so the string movement keeps the same rate regardless of DAW tempo; set ~0.7 and a moderate depth.
4. Bring in oscillator 2 (presenter's level ~17.5) alongside osc 1, then detune osc 2 ever so slightly (fine ~0.20) — perfectly in-tune oscillators lose the effect.
5. Lower the low-pass cutoff to cut the really high end; reduce output level if hot.
6. Amp envelope: much slower attack (presenter ~38 display units) for a fade-in and a long release that tails naturally.
7. Set master transpose from −12 to 0 so A440 plays A440. Turn off the filter envelope and other filter modulation sources so the filter stays static.
8. Set the voice/unison count the presenter uses (2), play chords to confirm the 1980s string pad, and save it as a patch.

Batch: `2026-10-14-morning-hunt` · transcript: YouTube-provided (Show transcript)
