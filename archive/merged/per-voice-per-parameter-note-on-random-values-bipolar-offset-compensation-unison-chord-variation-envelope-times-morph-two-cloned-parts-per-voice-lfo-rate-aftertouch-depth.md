# Per-voice, per-parameter random value drawn at each note-on (many synced sample-and-holds): offset compensation for bipolar values at a parameter's minimum or maximum, unison/chord voices that each get different timbre, random envelope times on an arpeggiated FM pluck, per-voice morph between two cloned-then-edited parts, and per-voice random LFO rate with depth brought in by aftertouch

Goal: Make every note and every voice differ slightly without sequencing anything. A per-voice random source picks a new value at each key press for each voice the key allocates and for each parameter it modulates (so 8 unison voices get 8 different wavefolder and FM values, and each note in a chord differs). Values are bipolar: if a parameter sits at its minimum, only positive values have an effect, and an open filter only moves when values are negative, so set the base knob to the middle (offset) to use the full range. Good targets: wavefolder, through-zero FM, filter, envelope times on a plucky FM arpeggio (2-octave up/down), filter envelope, and morph between two parts (clone part A to B, edit B, set morph halfway). A global effect at the end of the chain (e.g. ping-pong delay mix or time) cannot vary per voice and takes the highest value. Randomise LFO rate per voice with LFO depth at zero and aftertouch adding depth for expressive control. Maps to Polyrhythm Studio as a per-voice random draw at note-on.

Source: [Magnolia Polymove Explained: The Ultimate Randomization Tool](https://www.youtube.com/watch?v=X_zozWSx-RU)

1. On an init patch set the wavefolder about halfway and assign the per-voice random source to it. Play repeated notes.
2. Add through-zero FM as a target with its base at 0; then move the base up to compensate for the bipolar range.
3. Set unison (e.g. 8 voices, mono) or chord mode and play.
4. Add the filter cutoff as a target; with the filter fully open only negative draws act, so lower the base.
5. Build a plucky FM patch with an up/down arp over two octaves at a lower tempo; randomise envelope times, then a little wavefolder, filter, resonance and filter-envelope amount.
6. Add a tempo-synced ping-pong delay and randomise its mix or time.
7. Clone part A to part B, change several parameters on B, set morph halfway, and randomise the morph.
8. Set a unipolar saw LFO on the wavefolder or FM amount, randomise its rate per voice, set LFO depth to zero and map aftertouch to depth.

Batch: `2026-10-22-morning-hunt` · transcript: YouTube-provided (Show transcript) · Synth feature explainer; outro dropped; product UI mapped to generic per-voice random modulation.
