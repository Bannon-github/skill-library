# Harmony: chord qualities, voicing, voice leading and slow ambient harmonic motion

Goal: Write chord progressions and voicings: diatonic chords in a key, extended/sus chords, spread voicings with one chord tone per instrument, voice leading (hold common tones, move by step), pedal points and slow one-key harmonic motion.

**Theory:** Chord quality comes from interval stacks (maj 4+3, min 3+4, sus2/sus4 remove the third). Voice leading minimises motion between chords; inversions and pedal bass create motion without changing the key.

**Hear it:** `sample-lab/theory/intervals_chords.py`

## Workflow
1. Pick key and mode; list diatonic triads/sevenths (e.g. A minor: i, III, iv, v, VI, VII).
2. Choose a progression (i-VI-III-VII, I-V-vi-IV, ii-V-I) and a harmonic rhythm (1 or 2 bars per chord; ambient: 2-4 bars).
3. Voice-lead: keep common tones, move other voices by step; use inversions to avoid jumps.
4. Colour: add 9ths, sus2/sus4/7sus4; pedal the root while top voices move, or hold chord while bass walks inversions.
5. Spread voicing across instruments: root in sub, 3rd in pad, 5th in choir, 3rd doubled in strings; keep low intervals wide (no 3rds below ~C3).
6. Add tension: brief 1-2-3 cluster or suspension before resolving at section changes.
7. Hear the theory: run `/home/box/audio-tools/bin/python sample-lab/theory/intervals_chords.py` from the repo root and compare the sections; reuse its functions as a starting point for renders.

## Source techniques (merged, numbers kept)

### Ambient chord arrangement: give each chord tone to a separate instrument (sub root, synth third a tenth up, choir fifth, string doubling the third), each swelling in on its own, moving in parallel and spread wide, at about 55 BPM
Source: [Tips for Ambient Music Arrangement](https://www.youtube.com/watch?v=CfyOOGAxJEs) · was `ambient-chord-arrangement-one-chord-tone-per-instrument-root-sub-third-pad-fifth-choir-third-reinforcement-strings-parallel-motion-spread-voicing-55-bpm-breath-tempo`
- Set tempo around 55 BPM (4/4 or 6/4) or 60/halftime; the source ties 55 BPM to a roughly six-second breathing cycle.
- Write the progression as plain triads (e.g. I, vi, I, V).
- Instrument 1: sub plays only the root of each chord, long notes with a swell (mod wheel).
- Instrument 2: dark pad plays the third, placed a tenth above the root; subtle, gives key/chord quality.
- Instrument 3: choir-like pad plays the fifth above; each instrument swells in uniquely.
- Instrument 4: frozen string reinforces the third to make the key strong. Move all voices in parallel (all up or all down).
- Spread the voicing: lift the third or the fifth by an octave, or place the fifth above the third, so the notes are not close together, especially in low registers; add reverse textures in the key.

### Slow ambient harmony in one key: suspended and 7sus4 chords, a held root under a changing upper chord, or a static chord over a moving bass note, plus inversions and a band-passed 1-2-3 scale-degree cluster for tension, all moved slowly over a long timeline
Source: [Music Theory for Ambient (theory you can actually use!)](https://www.youtube.com/watch?v=tfJocFdYxsg) · was `ambient-slow-harmony-motion-one-key-sus2-sus4-7sus4-chords-pedal-root-moving-top-static-chord-moving-bass-inversions-band-limited-1-2-3-cluster`
- Choose a single key or mode (a minor or modal key for dark or suspended moods) and keep every chord inside it.
- Open with a neutral suspended chord, sus2 (1-2-5) or sus4 (1-4-5), over a low root note, then move to the minor triad.
- Add contrast with a 7sus-style shape (root, 5th, 7th) and return to the suspended or minor chords; stick to 2-4 notes per chord.
- Make variants from the same notes: inversions (different chord tone in the bass), dropping tones down 1-2 octaves, or using a non-root chord tone as the next chord's root.
- Pedal-root motion: hold the root (e.g. A) and change the upper chord above it (e.g. Am, then Dm, then C).
- Moving-bass motion: hold the upper chord and step the bass note underneath (e.g. Am over the 6th degree).
- Tension colour: play scale degrees 1, 2 and 3 together and band-limit them with high-pass and low-pass filters to roughly 600-1000 Hz.
- Spread chord tones across several layered instruments and stretch all changes across the timeline (many bars per change).
