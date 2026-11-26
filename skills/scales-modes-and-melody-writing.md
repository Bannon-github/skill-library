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

### Action/tension cue from melodic cells: build short rhythmic-melodic cells, reorder and transpose them (up minor thirds for tension), repeat them so they sound intentional, put tension in the bass against a tonic ostinato, release with major triads, and derive octatonic (diminished) chords by cycling the cell down half steps
Source: [Decode ACTION CUES with Melodic Cells](https://www.youtube.com/watch?v=efnKT5pHqUo) · was `melodic-cells-ostinato-repetition-legitimizes-tonic-against-bass-tension-major-triad-release-octatonic-half-step-cycle`
- Write the main ostinato and pull out its pitch set (e.g. 4 notes). Write new cells from the same pitches in a different order and rhythm for another voice (e.g. horn).
- Reduce a cell to its interval shape and transpose it; for tension move it up by minor thirds in a higher voice (strings).
- Repeat the cells often enough that each fast idea is heard as deliberate; choose a simple form and stick to it.
- Recontextualise on repeats: change the bass under the ostinato so it fights the ostinato's strong tonic (tension); to release, put major triads over the heavily minor ostinato.
- Derive the octatonic scale: play the cell four times in a row, each starting a half step lower; the collected pitches form a diminished (octatonic) scale. Blend it with the minor scale (shared notes) and borrow its clashes for tension chords; space a semitone clash into a major 7th so it sounds intentional.
- Optionally alternate between octatonic collections for major/minor triads over the ostinato to get ambiguous, uneasy colour.

### Three ambient-piano melody devices: a vector melody (one-direction Dorian scale run that may start and end on a dissonant 9th/11th), a classical sequence (a short phrase stepped down one scale degree at a time over chords that all keep one common tone in the bass), and modal transformation (two chord tones slip up a half step, maj7 -> min7 -> maj7, and the melody switches Lydian -> Dorian -> Lydian while the harmony keeps rising)
Source: [3 Simple Tricks for Beautiful Ambient Melodies](https://www.youtube.com/watch?v=liS9PQyHSa4) · was `ambient-melody-three-tricks-vector-melody-dissonant-start-end-scale-step-sequence-over-common-tone-a-bass-modal-transformation-maj7-to-min7-to-maj7-half-step-voice-slips-lydian-dorian`
- Set up the accompaniment: a repeating E minor pattern whose only change is one inner voice moving a step (Em6 -> Em7, C# -> D). Put a quiet pad under the piano and add reverb.
- Vector melody: play a simple E Dorian scale descending over the bed. Try starting it on the 9th (F#) and ending on the 11th (A) so it begins and ends on bitey tones (Em69 colour).
- Repeat the same scale shape from a new start note over a new chord (e.g. from high A over an A chord instead of E minor), then return to where you started.
- Sequence: write a short melodic ornament (a few notes) and repeat it, moving it down one scale degree each time, two or three times.
- Under the sequence, keep one common tone in the bass on the offbeat: Dm with A in the bass -> Am7 -> Bbmaj7 (A is its major 7th) -> A augmented -> A7 (the two upper notes step down). Let A7 (V of D) resolve to D at the next section.
- Modal transformation: play Gbmaj7 (Gb Bb Db F) with a Gb Lydian melody (raised 4th, C).
- Slip two notes up a half step (Gb -> G, Db -> D; Bb and F stay) to get Gm7, and re-fit the melody to G Dorian.
- Now slip Gm7's 3rd and 7th up a half step (Bb -> B, F -> F#) to get Gmaj7, and play G Lydian. Continue the climb the same way (Am7 -> Amaj7 by raising the 3rd and 7th), adjusting the melody each time.
