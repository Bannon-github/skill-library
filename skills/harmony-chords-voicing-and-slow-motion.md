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

### Cinematic voice-leading rule for pad/string layers: each two-voice layer alternates compressed seconds and expanded thirds, keeps one common tone between moves, and each new layer starts a perfect fourth, fifth or octave from the layer above, all inside one mode
Source: [The only trick you need for Epic Emotional Cinematic composing](https://www.youtube.com/watch?v=3cSsQw4CggE) · was `compress-expand-voice-leading-seconds-to-thirds-strata-a-perfect-consonance-apart-held-common-tone-preparation-modal-layers`
- Pick a mode and write the top layer as two voices that alternate a second (compressed) and a third (expanded), e.g. a second that falls out to a third.
- On each move, keep one of the two notes from the previous interval (a held common tone or preparation) and move only the other.
- Start the second layer a perfect consonance (4th, 5th or octave) below the top layer's top note, and run it in the opposite phase: where the top layer is compressed, this one starts expanded, and vice versa. Being less strict about common tones is OK here.
- Add further layers the same way (e.g. a scale-wise woodwind-like line), each starting a perfect consonance away from the layer above. Let some voices move in parallel and some in contrary motion.
- For a growing, expansive feeling, let the layers move wider and wider apart over the phrase.
- Assign layers to separate pad/string voices and listen; adjust by ear rather than analysis.

### Make drones interesting by role: a bass pedal point under changing harmony (or a repeated arpeggiated root), a non-key-tracked mid-range drone as a through-line with the bass and an upper note moving around it, layered drones tuned to a static chord with a progression underneath for polychords, and wavetable-position sweeps for texture
Source: [How to SYNTH DRONE without boring everyone](https://www.youtube.com/watch?v=9Re-L7z0068) · was `drone-role-pedal-point-and-polychords`
- Choose the drone's role: foundation (bass pedal point) or textural through-line in the mids/high mids.
- Pedal point: hold or repeat one bass note for the whole piece (an arpeggiator repeating the root counts); change chords, textures and rhythm above it, e.g. hold the dominant to build tension before resolving to the tonic.
- Through-line: switch off key tracking on one oscillator and tune it to a mid-range note; play bass notes and a note above that move around it, auditioning chords for the rubs they create. A second fixed partial (e.g. A440) can be added rhythmically.
- Polychords: tune several mid/high drones to a static chord and play a different chord progression underneath so the two combine into polychords that never fully resolve.
- Texture: on exposed drones, find sweet spots in a rich wavetable and sweep the position slowly with an LFO.
- Change the bass note under the drone at key moments; a single new pedal note recolours everything above it.
