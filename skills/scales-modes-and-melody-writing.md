# Scales, modes and melody writing (mode colour, motifs, phrasing)

Goal: Choose a scale/mode for the mood (Lydian bright -> Phrygian dark), use the characteristic note, and write motifs with call-and-response and rule-of-three phrasing.

**Theory:** Modes of the major scale share notes but change the tonal centre; each has a characteristic degree (Lydian #4, Dorian natural 6, Phrygian b2, Mixolydian b7). Pentatonics remove semitones for safe melodies.

**Hear it:** `sample-lab/theory/scales_modes.py`

## Workflow
1. Pick mood -> mode: Lydian dreamy, Ionian happy, Mixolydian bluesy, Dorian cool, Aeolian sad, Phrygian dark.
2. Emphasise the characteristic note on strong beats over a tonic drone.
3. Write a 1-2 bar motif using mostly steps with one leap; end phrases on chord tones.
4. Repeat motif twice, vary the third time (rhythm or ending).
5. Call and response between two instruments; keep melody in its own register.
6. For generative melodies lock to scale/pentatonic and limit range.
7. Hear the theory: run `/home/box/audio-tools/bin/python sample-lab/theory/scales_modes.py` from the repo root and compare the sections; reuse its functions as a starting point for renders.
