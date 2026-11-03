# Custom sub-drop: automate a sine from ~80 Hz down to ~20 Hz

Goal: Design original sub/bass drops without sample packs by generating a mono sine (test tone or sine osc), automating frequency from about 80 Hz (or key-matched) down to about 20 Hz over a chosen length (half-bar to multi-bar), bypassing the generator outside that window, and optionally adding bass-harmonic saturation.

Source: [How to make custom bass drops / sub drops in Cubase (tutorial)](https://www.youtube.com/watch?v=FULqquC3-Fc)

1. Create a mono track and insert a sine test-tone generator (or a sine-only oscillator). Name the track as a sub-drop layer.
2. Pick a start frequency near 80 Hz (or look up the Hz for your song's root); set end near 20 Hz for a deep trailer-style drop.
3. Draw frequency automation from start_hz to end_hz across the chosen length (e.g. 1 bar). Elongate or shorten the automation for brutal long drops vs fast stabs.
4. Automate bypass/mute so the generator is only active during the drop window.
5. Optional: add bass-harmonic exciters/saturation (e.g. 'max bass'-style) if you want audible upper harmonics; verify on a spectrum that harmonics appear only when desired. Export several lengths/keys into a personal drop folder.

Batch: `2026-10-09-morning-hunt` · transcript: YouTube-provided (Show transcript)
