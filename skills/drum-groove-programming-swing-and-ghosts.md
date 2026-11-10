# Drum groove programming: genre patterns, swing, ghost notes and sparse ambient beats

Goal: Program grooves that feel right: four-on-floor, half-time future garage, sparse ambient kits with accent maps, ghost snares, swing amount, and phrase variation every 2/4/8 bars.

**Theory:** Groove = placement + velocity. Swing delays every second 16th (50% straight, ~58% subtle, 66% triplet). Ghost notes at 20-40% velocity fill gaps; backbeat on 2 and 4 anchors.

**Hear it:** `sample-lab/theory/rhythm_polyrhythm.py`

## Workflow
1. Pick tempo and feel: house 120-128 four-on-floor; garage/halftime 130-140 with snare on 3; ambient 70-100 sparse.
2. Place kick and backbeat first; bring drums in early (by bar 2-5, ~10-12 s) unless the arrangement calls otherwise.
3. Hats: 8ths/16ths with velocity accents; swing 54-62% for laid-back, keep kick/snare straight.
4. Ghost snares/rims at 20-40% velocity around the backbeat; reversed flairs before bar 4.
5. Vary: A-B-A-C over bars, fill or empty bar every 8; sparse ambient = kick on bar 1 of each phrase.
6. Process: LP kick in garage, band-limit rims, light sidechain of foley to kick, 12-bit grit optional.
7. Hear the theory: run `/home/box/audio-tools/bin/python sample-lab/theory/rhythm_polyrhythm.py` from the repo root and compare the sections; reuse its functions as a starting point for renders.

## Source techniques (merged, numbers kept)

### Build a loose future-garage/ambient drum groove in layers: halftime kick and rim, a guide 'base hat' on every 'and', accent hats and rims on hand-swung 16ths (some early, some late, some on the grid), flair hats from one sample with a reversed copy, then faded Foley chops for crunch. Process it with LP24 on the kick (about 1 kHz, 30% resonance) and a band-passed rim (about 1.5 kHz), a frequency shift on the hat group (example -898 Hz), the rims vocoding themselves with chorus, a fast unsynced auto-pan and phaser on Foley (about 6.1 Hz), a half-note volume duck on the hat group, and a 12-bit lo-fi sampler with gentle clip/saturation on the drum bus
Source: [Future garage / ambient drum patterns, layer by layer, plus post-processing](https://www.youtube.com/watch?v=e4zq3HQdcIY) · was `future-garage-ambient-drum-groove-halftime-kick-rim-base-hat-loose-swung-accent-hats-rims-reversed-flair-hat-faded-foley-chops-lp24-kick-1k-rim-1-5k-freq-shift-self-vocode-halfnote-duck-12bit`
- Core: kick plus main rim in a halftime two-step (one-drop/dub feel), or fulltime with the snare on 2 and near 4.
- Add a guide 'base hat' on the 'and' of every beat to feel out the spaces. It may be muted in the final mix.
- Add 2-3 accent-hat layers on other 16ths/8ths. Swing the 2nd and 4th 16ths by hand and not precisely: some hits on the grid, some a little late, some early, until it feels right. Do the same with accent rims for mid-range knock. Group and duplicate the loop, then vary it every 2-4 bars (move hits, swap a sound, stop a layer briefly, a small filter sweep).
- Make flair hats from one hat sample with velocity changes for bounce, plus a reversed copy placed every so often.
- Foley crunch: chop a recording (silverware, paper) into single clicks. Line the transients up roughly with a grid value just before the main rim, or on a swung 16th. Fade each chop in and out to soften the transients. Add a transient-heavy 'mid knock' layer (example: celery snaps).
- Filter the kick with LP24 at 30% resonance and the cutoff around 1 kHz (range 800 Hz-3 kHz depending on the kick). Put the rim through a band-pass/high-pass blend at about 1.5 kHz with a little resonance and filter saturation.
- Put a frequency shifter on the hat group (example: down 898 Hz), and on other groups as needed. Shifting up gives brighter chill percussion, shifting down gives darker lo-fi. EQ before and after, and re-tune individual elements if one goes weird.
- Vocoder on the mid-range rim group: use the self-carrier mode (left as carrier, right as modulator) and enable its chorus.
- Put an auto-pan and phaser at a fast unsynced rate (about 6.1 Hz) on the Foley layer, so each pass of the loop lands differently.
- Put a volume LFO ducking on half notes over the whole hat/Foley group.
- Lo-fi: put a 12-bit sampler at a 22.5 kHz sample rate on the hat group. On the drum bus, run a 12-bit/44.1 kHz stage into a hard clipper (about 2 dB drive) and a symmetric soft saturator (about 1.7 dB). Keep it subtle.

### Add drums to a gorgeous slow pad track without crushing it: map the track's accents first, put kicks only in bar 1 (plus one ghost note) of each 4-bar phrase, snares on bars 2 and 4 with a big reverb only on the second round and a reversed-reverb swell before bar 4's downbeat, view the grid at double tempo (67 to 134 BPM) to find off-kick hat spots, alternate two hats' brightness with a 2-bar LFO on an EQ, add a ride in only two places, and let a quiet high-passed noise bed seep into the gaps, ducked by the percussion with about a 3 s release
Source: [Spacious ambient / lo-fi drums that still have character](https://www.youtube.com/watch?v=BcbSwdsC7W8) · was `spacious-ambient-drums-accent-mapped-sparse-kick-bar-one-ghost-snares-bars-2-4-reverse-reverb-before-bar-4-only-double-tempo-grid-lfo-eq-hats-ducked-noise-bed-3s-release`
- Listen through the pad track and mark the accents (example: a big block chord at bars 9 and 13) and the space at the end of each 4-bar phrase. Decide per phrase whether that space stays empty for the listener or gets busier percussion.
- Kicks: put them in bar 1 of the 4-bar phrase only, plus one ghost note just before the repeat. Roll off the very low end. Put a compressor on the pad group, sidechained to the kick, so the pads gain a gentle bounce.
- Snares: put them on bars 2 and 4. On the second round only, send to a big lush reverb (EQ on the return). Print that reverb, reverse it and place the swell only before the downbeat of bar 4, not bar 1, so it doesn't get monotonous. Add a short widening delay to the swell.
- Shorten the snare and rim-shot tails: warp the snare in Beats mode, preserve transients, loop-forward, and set the envelope to 0 so it rings out less.
- Temporarily double the project tempo (example 67 to 134 BPM) so the click shows subdivisions. Place two hats outside the kick hits, slightly ahead of the bar line, then go back to the real tempo.
- Put an LFO on an EQ's frequency, alternating between about 80 and 100 (as spoken) at a 2-bar rate, so the second hat is always the darker one, like clockwork, without drawing automation.
- Make the main hat/percussion line soft and crackly. Apply a swing groove to the audio (a jazz 5/4 swing template), then pull the transient amount right down. Automate a stereo delay's width so the high notes are wide and the low ones go mono. Glue-compress the peaks and use gain automation to level the quiet hits.
- Add drummer character: a ride only at the end of bar 3 and straight on the downbeats of bars 7-8, a few panned glass Foley hits, and chopped toms. Saturate and low-cut the toms and lower their transients.
- Swap a stock cymbal for a cymbal/organic swirl through delay, large-hall reverb and a vocoder. Automate the vocoder, reverb and delay dry/wet and fade it in.
- Noise bed: run a noise generator through a ducking envelope (depth about x8, threshold low, release about 3 s), keyed by the percussion and high-passed. Set it very low, about -13 to -17 dB, so noise seeps into the gaps about 3 s after percussion stops.

### Human drums on any step sequencer: four-on-the-floor kick, eighth hats with the hats that land on the kick turned down, 56% swing, a 16th-hat layer only on the second bar with every other hit softer, open hat on the last step of bar 2, a loose clap built from 3-4 stacked clap tracks nudged early/late with varied velocity and pitch, a track with an odd 24-step second bar and an 8-bar reset, random sample-start drift on the closed hat, and a pumping bus compressor
Source: [Drum programming Tips for ANY machine](https://www.youtube.com/watch?v=Fj7E0DXML1o) · was `velocity-and-flam-groove-on-step-sequencer`
- Program a four-on-the-floor kick.
- Eighth hats: lower the velocity of the hats that coincide with the kick so the off-beat hats stand out; set swing to about 56%.
- On a second hat track, add 16th hats only in the second bar of a two-bar pattern, with every other hit lower in velocity.
- Put a softer, slightly pitched-down open hat on step 15 of bar 2 with a little reverb send.
- Loose clap: copy the clap to 3-4 tracks; leave one on the grid, push one a little early, one later and one even later; vary velocities and pitch one copy up (and one far down, quieter, high-passed); add a little reverb.
- Make one track 32 steps with the second bar shortened to 24 steps and a pattern reset every 8 bars (128 steps), so it cycles against the bar.
- On the closed hat, route a slow, free LFO (odd length) at low depth to sample start, with a soft attack.
- Balance the claps down, then add a pumping bus compressor; if the kick blooms too much, shorten it and tune it down slightly.

### Program drums for any electronic genre from one foundation (kick on 1, snare on 2 and 4): four-on-the-floor vs two-step (kick on 1 and the 'and' of 3) families, offbeat open hats and 16th closed hats, a tempo-to-genre map (house/techno 120-130, trance 138-150, garage 128-135, breaks 140-150, DnB 170-180, halftime dubstep/trap 140), set syncopation spots, uniform swing on every second 8th/16th, and 2/4-bar variations with a tom fill and crash
Source: [How To Write Drums for ANY Electronic Music Genre](https://www.youtube.com/watch?v=L0mST_BaaBA) · was `genre-drum-pattern-families-tempo-map`
- Foundation, 1 bar of 4/4 on a 16th grid: kick on the downbeat (beat 1), snare on the backbeats (beats 2 and 4).
- Four-on-the-floor family: kick on every beat, open hat on every offbeat (the third 16th of each beat), closed hats on every second 16th to fill gaps. Tempo map: 120-130 BPM house/techno (128 typical house), 130-140 techno to trance, 138 typical trance, 140-150 trance, 170-180 hardcore (mute the extra 16th hats at high tempo).
- Two-step family: foundation plus one kick on the 'and' (offbeat) of beat 3; closed hats on the remaining 8th notes (open hats can swap in on some). Tempo map: high 120s to mid 130s garage, 140-150 breaks, 170-180 drum & bass (174 typical).
- Halftime: at 140-150 BPM double every note length/position of the two-step (1 bar becomes 2) for dubstep; add 16th closed hats with varied velocity for trap.
- Syncopation for four-on-the-floor: claps on the last 16th of beat 1 and the offbeat of beat 2, repeated per beat pair, or moved to the second 16th of a beat; the same rhythm can go on a low tom. For two-step: rims on the last 16th of beat 2 and the second 16th of beat 3, and on 16ths leading into snares; extra kicks on offbeats or 16ths depending on tempo.
- Swing: delay every second 8th (8th swing) or every second 16th (16th swing) by the same amount. Every sound on a swung step (e.g. hat and clap together) must get the identical offset; or use the DAW's groove feature.
- Variation: duplicate to 2 bars and change the clap pattern in bar 2; duplicate to 4 bars and put a high-to-mid-to-low tom fill on syncopated 16ths in bar 4; crash on the downbeat of bar 1 and rides on every beat at low velocity.

### Organic downtempo/electronica groove at 115-120 BPM (Christian Löffler style): deep kick plus a tom made from the same kick (shorter, softer attack, band-passed), filtered rim with a small room, 3-4 layered hand claps with pre-claps placed slightly earlier and varied per hit, a shaker family cut from one sample at different transpositions, frequency-split hats, dark noise percussion and an ambient noise loop, all glued into small rooms; then a warm sidechained piano/pad bed
Source: [How to make ELECTRONICA and DOWNTEMPO like [Christian Löffler] [Cercle]](https://www.youtube.com/watch?v=3zIsQfKtUno) · was `organic-downtempo-groove-kick-tom-from-kick-layered-offset-claps-shaker-family-room-sends`
- Set the tempo to 115-120 BPM. Kick: a deep, thumping kick with an EQ low cut below its useful low end.
- Tom from the kick: duplicate the kick sample, shorten it, raise the attack so the initial thump/click disappears, and cut lows and super-highs (band-pass to the mids).
- Rim/snare: a rim sample with super-lows and super-highs cut, sent to a slightly longer, small room reverb with a little chorus.
- Clap crowd: a main organic clap on the backbeat plus 2-3 hand-clap layers placed slightly before it (one clearly earlier as a pre-clap, one in between). Vary each layer's placement a little per hit. Group, glue-compress with a fastish attack and send to a very small, narrow drum room (100% wet, short decay).
- Shaker family: copy one shaker sample three times, cut different pieces and transpose some (e.g. -6 and -2 semitones). The main piece plays at the start and half of each bar; the others fill the gaps; vary velocities. Darken one copy (e.g. a wet vocoder/filter) and pan it slightly behind.
- Hats: a bright transient hat with slight L/R panning, a lower shaker-like layer of the same sound, and a bright shaker loop on top, each in its own range.
- Percussion: a noise hit darkened and a second copy transposed down hard; a snare panned slightly left just before the end of the bar. Send to the room.
- Ambience: one or two noise/rain-like loops low under the groove.
- Warm bed: simple piano dyads at low velocity, smoothed attack, EQ out boom and super-highs, glue, sent to a long hall. Add a long reversed piano layer and a warm wavetable pad (closed filter, chord with an added octave). Sidechain both to the kick and keep them behind the drums.
