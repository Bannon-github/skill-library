# Shepard-tone endless riser from three mono pitch-bent voices (plus rising noise-filter variant)

Goal: Build an endless-rising Shepard-tone riser from any synth: three monophonic copies of one sustained note swept by a full-length pitch-bend ramp, transposed by the sweep span so their ends dovetail, with the top voice fading out and the bottom voice fading in, then grouped into reverb to hide the reset click; plus a variant that applies the same overlap-and-crossfade trick to a ramp-LFO sweep of a resonant comb/flanging filter on white noise for a constantly rising jet/phaser texture.

Source: [Shepard Tone Tutorial - How to Create INFINITE Risers!](https://www.youtube.com/watch?v=YvUbr8GaqUo)

1. Understand the illusion: several copies of the same rising line spaced apart in pitch play together; the lowest copy fades in while the highest fades out, so the ear hears a constant rise.
2. Pick any synth where you can set the pitch-bend range and set it to a whole number of octaves (e.g. 12 semitones down and 12 up = a 2-octave sweep).
3. Draw one long sustained note across the whole clip and automate pitch bend from its minimum to its maximum exactly over the clip length, so it loops straight from bottom back to bottom.
4. Duplicate to three voices (high, mid, low). Transpose the high voice up by the sweep span (+2 octaves here) and the low voice down by the same span, so each voice's end pitch equals the next voice's start pitch.
5. Set every voice to monophonic (1 voice) so any release tail does not overlap and audibly fade out when the loop restarts.
6. Add volume automation: high voice 100% -> 0% across the clip, low voice 0% -> 100%, mid voice constant. Program the start/end points exactly at the clip boundaries.
7. Group the voices and put reverb on the group: it sits the riser back as a background effect and smooths the small click at pitch reset.
8. Noise/filter variant: white noise -> a resonant flanging/comb-style filter with many notches; replace the pitch ramp with a rising ramp LFO (retriggered, one ramp per 4 bars) on cutoff.
9. Make it endless: use four copies; give each a volume fade-in over the first 25% and fade-out over the last 25% of the clip, then duplicate the copies so they overlap and enter in turn (stagger is approximate from transcript).

Batch: `2026-10-07-morning-hunt` · transcript: YouTube-provided (Show transcript)
