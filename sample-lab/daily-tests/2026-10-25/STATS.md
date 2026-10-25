# Daily 3-skill test, 2026-10-25: "Glass Arc"

Track: `glass-arc-2026-10-25.mp3` (71.7 s incl. 5 s tail, 72 BPM, A minor Am-F-C-G, 20 bars). Audio stays local (repo excludes audio).
Renderer: `render.py recipe.json track.wav` (original synthesis, deterministic). Python: /home/box/audio-tools/bin/python.

| skill | role | what it added | where it fell short |
|---|---|---|---|
| modal partial resonator | source | string-model harp arpeggios, vibraphone+beam (parallel) climax melody, membrane->tube (series) ticks for the hat loop, beam bank in the cymbal swell; material/tone/hit/inharm and velocity->material gave clear per-note colour | no numeric defaults for material, hit or cross-feedback, so all were guessed; step 4 (manual partial snapshots + ratio morph) and step 6 (osc layer + filters) skipped |
| sample-and-hold as processor | modulation | S&H over a sine LFO set the vibraphone hit position (regular but stepped); riser with LFO rate ramp 0.5->24 Hz under a low S&H rate gives the "slowing down" alias effect; 1/8 step pattern -> S&H -> hat volume dips with inverse metallic comb mix on a duplicated layer | S&H on a volume lane needs smoothing (2 ms) or it zippers, which the skill doesn't mention; "reduce the amount until not excessive" is subjective (0.7 used) |
| emotional cinematic arrangement arc | structure | intro pad only, harp enters bar 4, angelic one-note tremolo swell bars 6-8, hats bar 8, riser 10-12, melody only in climax 12-16 (chord-arpeggio method with leap-editing), strings with vibrato faded in, outro fade with cymbal swell and short piano dialogue, light master (HP 20, saturation, limiter) | "appear from nowhere" intro fails the lab's silence gate (M13): iter2 intro sat at -70 dBFS; needed a 20% level floor |

Scores (TARGET.md v1, pad bands): iter1 89.2 (fail M7 13.1 dB low-mid hole, M13 0.15 silent frames) -> iter2 92.9 (M13 still fails, intro too quiet) -> **final 96.1 PASS**.
Final: -17.0 LUFS, true peak -3.1 dBTP, side/mid below 150 Hz -20.8 dB (side HP 150 Hz), mono-fold 0.33 dB, tilt -3.4 dB/oct, M7 10.3 dB (125 Hz band still under the fit), M9 presence -11.5 (just over -12), limiter GR 0 dB, all gates pass.
Next tweak: raise the low pad (lowPadLevel 0.12 -> 0.2) or add a cello line at 100-180 Hz to fill the 125 Hz octave, and trim hats another 2 dB to bring 2-5 kHz under -12.
