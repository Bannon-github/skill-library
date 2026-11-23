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

### Ambient 'meta-chord' progressions (David Wise-style): a 2-4 chord loop that repeats until it fuses into one mood; smooth voice leading where as few voices as possible move, each by step (as little as one note per change); every chord made colourful with extensions voiced from mixed intervals (e.g. a third and a fifth stacked on the chord's third to give a minor-9 colour, then the same shape moved to the next chord with a sixth added on top); no dominant-seventh chords, and dominant-function triads (V in major, bVII in minor) used in first inversion (e.g. bVII add2 over its third, voiced minor 7th + two perfect 4ths); and one short melodic line repeated unchanged over every chord so passing dissonances become expected
Source: [4 Tips for Writing Ambient Chord Progressions](https://www.youtube.com/watch?v=MycI9ZOSPRk) · was `ambient-meta-chord-loop-2-4-chords-one-step-voice-leading-mixed-interval-extensions-no-dominant-7-first-inversion-v-bvii-constant-ostinato-line`
- Choose 2-4 diatonic chords in the key (e.g. i - bVI - iv - bVII in C minor) and plan to loop them for the whole section.
- Voice-lead smoothly: write the voicings so as few notes as possible change between chords and each changing note moves by a step (in the simplest form only one note moves per change).
- Colour each chord: add extensions and vary the intervals inside the voicing; e.g. over the bass root, stack a third and a fifth above the chord's third to get a minor-9 sound, then move the same shape down to the next chord and add a sixth on top.
- Remove expectation: replace any dominant seventh with a triad or add2, and put V (major key) or bVII (minor key) in first inversion, e.g. bVII add2 over its third voiced as a minor seventh with two perfect fourths above.
- Write one short line (e.g. a 3-note figure or an eighth-note arpeggio of a maj7 shape) and repeat it unchanged over every chord of the loop.
- Loop the progression with the ostinato for the section; let repetition fuse the chords into one meta-chord mood before any new section arrives.

### Turn one chord progression into a full set of ambient layers: parallel maj7 progression (e.g. Cmaj7-Gmaj7-Bbmaj7-Fmaj7, 4 bars of long sustained chords) copied to every part and thinned per role - bass keeps only the lowest note (optionally re-chosen, e.g. D under the last chord), pad keeps the upper three notes tightened by dropping the top note an octave, an FM arpeggio built on the note set that fits all chords (root-4th-5th-octave such as D-G-A-D), a second pad built from major/minor seconds that move by semitone (B->C, E->F) as a contrast to the third-based pad, a melody using those guide tones with anticipations into each chord plus the all-chord tones (G, A) as connectors, an octave-lower double on a different timbre, and long-attack reverb swells on the universal tones
Source: [How I Turned 1 Chord Into a Hypnotic, Melodic Ambient Track](https://www.youtube.com/watch?v=ET1CvImwzxw) · was `one-progression-to-ambient-layers-parallel-maj7-bass-root-split-upper-voicing-octave-tighten-common-tone-root-4-5-arp-seconds-dyad-pad-anticipated-melody-octave-double-long-attack-swells`
- Write the progression: build one chord shape (e.g. maj7 = root, +4, +3, +4 semitones) and move it in parallel to new roots (C, G, Bb, F), one long sustained chord per bar, 4 bars; or use any diatonic progression.
- Copy the clip to a bass track and delete everything except the lowest note; try alternative bass notes under a chord (e.g. D under Fmaj7) and keep the ones that sound good.
- Copy the clip to a pad (e.g. choir/voice pad) and delete the bass note so the upper three notes remain; move the highest note down an octave so voices move by small intervals rather than jumping fourths/fifths, then raise the whole pad an octave if needed for register.
- Find the common-tone set: test a note (and its 4th and 5th, e.g. D-G-A) against all chords; keep the set that fits every chord. Program an FM-keys arpeggio as root-4th-5th-octave (or step pattern 4-1-4) on that set, looping unchanged across the progression.
- Build a seconds-based dyad pad: pick a chord tone of chord 1 (e.g. B) and move it by a semitone to the next chord's tone (C), similarly E->F; add a third below or above to form two-note intervals and play as a slow dyad trill on a mallet/vibraphone sound.
- Write the melody from per-chord guide tones (e.g. E/B over bars 1-2, F/C over bars 3-4), arriving on the next chord's tone slightly before the downbeat (anticipation), and use the common tones (G, A) as connecting notes.
- Double the melody an octave lower on a contrasting synth timbre; slight timing looseness is fine.
- Add swells: a synth with a long attack and heavy reverb playing the common tones (G, A) a few times across the section, no pitch bend.
- Collect all clips; arrange by muting/unmuting layers per section (e.g. pad drops out leaving the dyad layer).

### Tension-to-release build: sus4 dissonance released on the last note, a theme stated on the dominant then the tonic, rising key steps, an Ab pedal with Bb over it (bVI then bVII over a bVI pedal) resolving to a big C, while dynamics and pitch range widen and the theme moves from unison to octaves
Source: [Tension and Release: How to Add Emotional Impact To Your Music](https://www.youtube.com/watch?v=PUycGHv-2Jo) · was `sus4-tension-rising-key-steps-pedal-bvi-bvii-over-pedal-big-tonic-release-widening-range-unison-to-octaves`
- Contrast: play the theme over a plain major chord, then over a sus4 that resolves to the major exactly as the melody lands on its last note.
- Open with anticipation: short repeated string figure (tremolo/trim) and a counter-line, then state the theme first on the dominant (sus4) and then in the tonic.
- Raise tension by stepping the key/harmony up at phrase ends (in the sketch: C -> Eb, then up again) while adding horns and light percussion. No release yet.
- Final approach: a low pedal on bVI (Ab in C) held for 2 bars, then a bVII (Bb) chord over the same pedal for 2 bars with added movement, then resolve onto a big tonic chord, with a roll (timpani or noise swell) leading into it.
- Grow dynamics and widen pitch range throughout: start narrow and soft, end wide (low brass/tuba under, high parts above). Double the theme in unison the first time, then in octaves once the bVII arrives.
- Add rising gliss/riser effects as audio clips placed exactly where needed (bounce them out first for precise placement).
