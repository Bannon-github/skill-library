# Arrangement: loop to full song in 8-bar blocks (intro, build, drop, breakdown, outro)

Goal: Turn a loop into a finished electronic/pop arrangement: start from the full loop (the climax), subtract to make sections, change something every 8 bars, build-ups with risers and snare rolls, pre-drop low-end removal, breakdowns, withheld reveals and rule-of-three phrasing.

**Theory:** Energy curve: listeners need contrast; repetition builds expectation, change rewards it. Sections are 8/16 bars; a one-beat gap or bass removal before the drop maximizes impact.

**Hear it:** `sample-lab/theory/arrangement_energy.py`

## Workflow
1. Build the full 8-bar loop first (the drop/climax), then copy it across the timeline and subtract elements to create earlier sections.
2. Map the energy curve on a reference track: intro 16-32, build 8, drop 16-32, breakdown 16, build 8, drop 2, outro mirrors intro.
3. Every 8 bars add or remove at least one element; intro: high-passed kick, filtered bass, root pedal before the progression.
4. Build: 7 bars of risers and snare roll doubling (4->8->16), last bar remove low end / kick, double kick or vocal pickup.
5. Drop on the one with impact; breakdown strips rhythm and foreshadows melody through a low-pass.
6. Rule of three: play an idea twice, third time change it; withhold one key element (bass motion, melody) until the climax.
7. Transitions without risers: solo the lead, filter pad down, drop kick for a bar, single tom hit.
8. Outro mirrors the intro for DJ-friendly mixing.
9. Hear the theory: run `/home/box/audio-tools/bin/python sample-lab/theory/arrangement_energy.py` from the repo root and compare the sections; reuse its functions as a starting point for renders.

## Source techniques (merged, numbers kept)

### Breakdown arrangement after a drop: 4-bar break of impacts and reverse sweeps, two 8-bar breakdown halves (chords from the drop with rhythm removed, melody simplified then foreshadowed through a rising lowpass), then an 8-bar build-up of chopped parts and one silent bar before the drop
Source: [You'll Never Make Bad Breakdown & Buildup Again After Watching This - FL Studio 20 Tutorial](https://www.youtube.com/watch?v=ojDea0jCQ5o) · was `breakdown-arrangement-4-bar-break-two-8-bar-breakdowns-8-bar-build-up-rhythm-stripped-drop-chords-melody-foreshadowed-via-lowpass-automation`
- Place markers: Break (4 bars), Breakdown 1 (8), Breakdown 2 (8), Build-up (8), then the drop returns.
- Break: big impact, sub drop, reverse crashes, a reversed sweep going up, plus a background ambience effect.
- Breakdown background: repeat impacts and sub drops at the start of each breakdown, add smaller impacts, a motion loop and a shaker with reverb and reduced dry level.
- Chords: copy the drop chords, delete rhythm so notes become long chords (Ctrl+L to legato-join), remove offbeat notes, play on soft piano layered with a second synth; keep within one scale using scale highlighting.
- Tension motion: automate the synth's volume or cutoff rising at the end of each repetition; make a reverse piano by recording a piano hit and reversing it, then place it in the gap.
- Melody: take the first four notes of the drop melody, leave space, then the next five; for Breakdown 2 add drop-claps with reverb, a simple piano melody, and the full drop melody low-passed with an automation ramp from fully closed to open.
- Build-up: chop breakdown sounds to the first chord repeated, chop more in the second half, add up-filters, reverse sweeps and impacts at the start, a snare fill (four hits then doubled), keep the drop claps, bring in the real melody gradually filtered, put the melody ending in the last bar, and turn everything off one bar before the drop.

### Eight-bar build-up template: seven bars of risers, drums and sustained parts, one bar of pre-drop with everything cut, low end automated away, kick doubling schedule, filtered-in snare, single-note pad with pitch rise, and a readable vocal before the drop
Source: [3 Step Guide To Make The Perfect Build Up | Structure, Transitions & Core Elements](https://www.youtube.com/watch?v=nkNSlRVGb38) · was `eight-bar-build-up-seven-bars-risers-drums-then-one-bar-pre-drop-low-end-removal-kick-doubling-schedule-vocal-and-single-note-pad-transition`
- Set the length: 8 bars for 4/4 styles, 16 bars for faster drum and bass. Typical layout: 16-bar intro, optional 8-bar breakdown, 8-bar build-up, drop.
- Bars 1-7: risers, drums and sustained instruments; bar 8: pre-drop where everything else cuts off (snare roll, pre-drop vocal, sub build). Do not skip the pre-drop bar unless the groove rolls straight into the drop.
- Start quiet up-risers and down-filters at bar 1 of the build-up so the transition into it carries momentum; layer several risers, all low in level.
- Take one note of the previous chord pad, hold it for the whole build-up, keep it static for four bars, then automate pitch rising over the last four bars.
- Vocals: chop them in the first four bars; make the last four bars (pre-drop) say something recognisable. If a full vocal runs through the track, skip chops.
- Drums: with no breakdown, remove some drums in the transition so the return hits harder; with a breakdown, filter elements in gradually instead. Kick: every beat for 4 bars, double time for 2 bars, double again for 1 bar (continue through the pre-drop bar if the vocal matches), filtering out as it goes.
- Snare: a hit every step, filtered in starting already half-open; after 4 bars add a second low snare; add hats, claps and a percussion loop for movement. Stop all drums at the pre-drop.
- Remove low end as you approach the drop: automate bass, pads and risers' low frequencies down gradually. Optionally dip the loudest non-vocal elements (instruments/drums) rather than the master if vocals are present.

### Eight-bar rhythmic phrasing: spine beat on strong beats, bar-level A/B/A/C variation, and a last-bar D that is either a fill (adds syncopation and toms) or an empty (drops the kick or main rhythm) to set up the next section
Source: [Fundamentals of Rhythm for Electronic Music](https://www.youtube.com/watch?v=JE3QM_9sljI) · was `eight-bar-phrase-repetition-variation-a-b-a-c-bars-d-bar-fill-or-empty-spine-beat-weak-beat-frequency-mix-polymeter-shifting-loops`
- Build the spine beat: kick on beats 1-4, snare or clap on 2 and 4, closed hat on each offbeat eighth ('and').
- Add ghost or weak-beat hits on the 'e' and 'a' 16ths with quieter or lighter sounds (ghost snares, percussion, toms, synth hits), mixing low-mid and high-frequency sounds.
- Set the bar to A. Make bar 2 B: one small change only (add, remove or swap one hit). Bar 3 returns to A.
- Make bar 4 C: a slightly bigger variation than B (it doesn't need to include B's change). This closes the 4-bar half-phrase.
- Bars 5-7: return to A material (optionally a light B variant).
- Bar 8 = D. If the next section is a big lift, write a fill: extra syncopation, snares on weak beats, a couple of extra eighth-note kicks, toms stepping high to low. If you want a vacuum instead, write an empty: remove most or all main elements, e.g. drop the kick for the whole bar (or just its last beat).
- Line up section changes with the downbeat after D, and repeat the 8-bar scheme for every section, choosing fill or empty each time.
- Optional: add a polymeter layer (a 3-step pattern on the same grid as 4-beat bars) so its accent drifts against the downbeat.

### Four levels of loop-to-story arrangement: (1) subtractive Lego-block arrangement from a duplicated loop shaped by an energy contour, (2) turnaround-and-marker transitions at section edges, (3) a performed protagonist element that crescendos and decrescendos across sections, (4) an additive cinematic pass that starts from silence and adds only motivated elements
Source: [turn your loop into a story: an arrangement masterclass](https://www.youtube.com/watch?v=xY7vRHiSJSM) · was `four-levels-loop-to-story-arrangement-subtractive-lego-blocks-energy-contour-turnaround-and-marker-transitions-performed-protagonist-crescendo-element-additive-cinematic-start-from-silence`
- Decide the target length; select the loop and duplicate it end to end until the timeline exceeds that length; trim any extra.
- Sketch an energy contour: low start, additions toward the middle, dips where the kick goes away, a maximum, then an outro. Optionally align a reference track to the grid and copy its arrangement (not its sounds).
- Subtract in 8- or 16-bar blocks so each section boundary adds some elements and removes others. Insert a little silence at the start and leave space at the end for reverb tails.
- At each section edge, add a turnaround in the last bar(s): remove low-end energy and add a reverse reverb swell or noise riser built from the track's own sounds.
- On the new section's downbeat, add a marker: white noise burst, crash, one percussion hit into a big reverb, a stutter, or a false drop (withhold the first hit).
- Revisit breaks and drops: e.g. a very sparse moment, then build, build, build, then a short silence before the drop.
- Pick one protagonist element and perform it across the whole track (record filter/level/intensity moves) so it starts mellow, grows dominant and subsides, crossing section boundaries; split and rearrange the performance if needed.
- Additive pass: from silence, peel everything back to almost nothing and add elements one at a time only when the music needs them (when you notice boredom), giving each element time and space.

### Loop-to-track arrangement where the finished loop is the climax and everything before it 'gives away' that loop gradually: whole elements, the power of elements (high-passed kick, thin high-and-low-passed bass), and the chord progression itself (root-note pedal first), with a change at every 8-bar boundary and an outro that mirrors the intro
Source: [How to Structure Melodic House Tracks Like a Pro](https://www.youtube.com/watch?v=gIVUpqVRf-w) · was `loop-is-the-climax-give-away-arrangement-reference-section-notes-every-8-bars-high-passed-kick-intro-thin-filtered-bass-root-pedal-before-progression-kick-gaps-before-drop-mirrored-outro`
- Import a reference track, listen through and drop a marker each time something enters, leaves or changes (expect a change every 8 bars). Write the macro structure, e.g. intro, bass in, build, drop, breakdown, drop 2, outro.
- List what you can give away: whole elements; element power (kick without lows, bass without sub, thinner versions); the chord progression; stripped-back versions of parts.
- Drums first: copy the full drum loop to the start; high-pass the kick at about 120 Hz for the first 16 bars; remove shaker, hats and snare at first and stage them in later (shaker early, hats and snare saved for later).
- Delete the kick's last bar (or last 2 bars) before each full-kick entry or drop.
- Run the atmosphere/texture throughout to set the tone.
- Bass: write a single root-note pedal for the early sections with an octave jump at the end of each 8 bars. Add labelled HP and LP filters and automate from thin and dark to full and bright; switch to the full chord progression only at the main section.
- Melodic parts: enter with fragments (first bar only, fewer notes), filter them in rather than hard-cutting, then reveal the full progression, full lead and extra layers (piano chords, high pluck) only at later peaks; hold some back for drop 2.
- Before a drop, filter percussion/kick from thin and clicky to full, leave a short moment of near-silence, then hit the drop with everything un-high-passed.
- Outro: mirror the intro: high-pass the kick for 8 bars, filter the bass out and darker, return to the root pedal and end on a resolving note.

### Rule of three for repeating musical ideas: play a 4-bar idea twice so it sticks, then on the third pass either go somewhere new (new melody on the same chords, or new chords) or start the same and diverge halfway
Source: [This Arrangement Rule Will Change Your Music](https://www.youtube.com/watch?v=iiL3K3ewfuc) · was `rule-of-three-phrase-repetition-play-idea-twice-then-third-pass-goes-somewhere-new-or-starts-same-and-diverges-halfway`
- Write or pick a 4-bar idea (progression + melody) and place it once.
- Repeat it once (2 passes in total) so it is reinforced and memorable.
- Third pass, option 1: go somewhere different: keep the chords and write a new melody, or move to a new progression with a new melody.
- Third pass, option 2: start identical to the first two passes, then change the melody or chords about halfway through the phrase.
- Choose option 1 or 2 by the section's intent and audit the whole arrangement: anywhere an idea plays 3+ times unchanged, apply one of the two options.

### Three section transitions with no big risers or snare rolls, for simple two-chord tracks: (1) the lead plays alone while the pad's filter closes, a simple sweep and a lead variation, then kick, hats and bass drop in; (2) keep open hats, filter the pad down, put a clap on the beat with no kick and a high-passed bass, loop a lead variation, then one quarter-note tom hit opens the drop with the bass filter removed; (3) strip to the hat loop, tease lead variations (velocity, pan, spacing) with no kick or bass, then a very short fill and everything returns at once
Source: [3 SIMPLE transitions WITHOUT using risers or snare roll build ups](https://www.youtube.com/watch?v=vzlZ4GabrAs) · was `three-riser-free-transitions-solo-lead-pad-filter-down-drop-clap-on-beat-no-kick-hp-bass-single-tom-hit-strip-to-hats-tease-lead-variations-short-fill-all-in`
- Intro to first drop: run the intro with just the kick and a closed-hat drum loop, and the pad opening and closing on a filter. At the end, let the pluck/lead play on its own with the pad filter coming down, a simple sweep and a lead variation as the last bar.
- Land the first drop with kick, closed hats, open hats and the bassline entering together.
- Mid transition, part 1: play a lead variation, then return to the original. Keep the open hats, low-pass the pad steadily down, mute kick and closed hats, add a clap on the beat and high-pass the bassline.
- Mid transition, part 2: loop the lead variation and let the clap settle. Place one tom hit (about a quarter note long) in the last beat's space before the downbeat.
- Re-enter all drums with the second lead variation, open hats and the bass with its filter removed, so the low end hits with the kick.
- Final payoff: strip back to the closed-hat loop and open hats with the pad dipping again, with no kick and no bass. Tease the lead with its variations (same notes, different velocity, pan and spacing, for example one extra bar of space).
- End the tease with a very short drum fill (sweep plus clap/snare), then bring everything back at once: drums, bass, pad and lead.

### Arrangement that saves several 'firsts' for one climactic moment: keep a three-note ostinato unchanged from the start to that moment, keep the bass on one note until then, and change the ostinato, start the moving bassline and bring in a new percussion layer and the lead together; pull the constant pad from about -3 dB to about -14 dB in full sections, mark every entry or exit with a small FX hit, put a short silence before big mutes, and keep intro and outro loopable
Source: [Arrangement Hacks for MELODIC TECHNO | Jonas Saalbach | Ableton Live](https://www.youtube.com/watch?v=axLAIw6Iw7A) · was `withhold-the-reveal-arrangement-constant-ostinato-and-one-note-bass-until-stacked-firsts-climax-pad-minus-14db-in-full-parts-fx-marked-entries-silence-before-mutes-loopable-edges`
- Make the intro loopable: no fade-in noise or tails across the loop point so it can be repeated or mixed.
- Start the ostinato and a filtered kick from the beginning; add a building drone; bring in bassline, snare and other drums around the 1-minute mark (build-up shorter than about 2 minutes).
- Write the held-back list: ostinato change, moving bassline, a new percussion layer (e.g. off-beat shaker), the lead, pad switching to the ostinato's harmony.
- In the drops before the reveal, keep the bass on one note and low-cut it at times so focus stays on the ostinato.
- In full sections solo-check each channel and mute anything not needed; automate the constant pad from about -3 dB down to about -14 dB.
- Mark every entry or exit with a small FX hit, drum fill or (in the intro) an orchestral hit.
- Before muting many channels at once, insert a short moment of silence.
- At the reveal point change the ostinato for the first time, start the moving bassline, add the new percussion layer and the lead, and move the pad to the ostinato's harmony, all on the same downbeat.
- In the following drop let the bass stop briefly while hats keep running; then switch one element every 8 bars (add, remove, or octave shift).
- Build down slowly to a loopable outro; keep it shorter for album versions.

### Ambient loop to full track: split the chord progression into single-chord clips, intro from the loop, slower evolving section -> 'chorus' with faster chord changes -> slow outro; per-layer slow movement (band-pass pad filter with two LFOs, random LP and comb on the atmos, slow auto-pan), cutoff 'spikes' on the bass drone, arpeggiator rate automated whole -> half -> quarter -> eighth notes for energy, a double-speed drum clip and an arpeggiated pluck bass replacing the drone in the peak
Source: [Turn an Ambient Loop into a Full Track in Bitwig Studio (Part 2)](https://www.youtube.com/watch?v=PE3c8J6glho) · was `ambient-loop-to-track-arp-rate-energy`
- Duplicate the loop to a clip slot and cut the chord progression into single-chord clips (consolidate each first).
- Make a 16-bar intro from the loop scene.
- Pad: band-pass (2-pole) filter with two independent slow LFOs on frequency and resonance. Atmos: smooth slow random modulator (unipolar, subtle) on a low-pass cutoff, a comb filter with a slow LFO on feedback and smooth random on frequency, and a very slow bipolar LFO on pan.
- Automate the bass drone's oscillator cutoff in short 'spikes', copy the automation along the timeline and vary level/shape.
- Arrange: slower evolving section, then a chorus-like section with more frequent chord changes and higher dynamics, then a slower outro.
- Automate the arpeggiator rate: whole notes in the slow section, then half, quarter and eighth notes as energy rises (eighths in the chorus).
- Duplicate the drum clip and scale it to 50% length for a double-time peak section; sprinkle squelch hits, moving them by octaves for faster/slower squelches.
- For the peak, add an arpeggiated pluck bass fed with the pad chords (tune its ratio/octave lower for depth) and mute the bass drone there; finish with lightly EQ'd, delayed, reverbed one-shots.

### Arrange a minimal hypnotic track around one evolving drone: record filter-cutoff automation on a one-note drone and add dissonant extra notes per section, bring percussion layers in phrase by phrase with short volume-curve fade-ins, reach the climax with rising cutoff plus a high atonal noise layer, drop to a drone-and-atmo-only hypnotic break for 2-3 phrases, then keep energy by swapping the same sequence onto a different instrument instead of adding new loops
Source: [How I Arranged Hypnotic Techno Track – Arrangement Breakdown](https://www.youtube.com/watch?v=6x1_XZDcI8I) · was `hypnotic-drone-arrangement-phrase-layer-fade-ins-sequence-instrument-swap-drone-only-break`
- Hold one drone note through the track and record a pass of filter-cutoff automation while arranging, then tidy it by hand so overtones open up toward peaks.
- Add 1-2 extra held notes on the drone in later sections (e.g. G with D#, D, then G#) for dissonant tension.
- Build the groove phrase by phrase: lead percussion first, then a second hat layer (snappy + softer), then shakers, then a high noise pattern. Start some layers with a short volume curve (fade-in) so they blend in rather than hit on the downbeat.
- Climax: raise the drone cutoff and add the high atonal noise layer together, with a volume swell into it.
- Break: drop the drums so only the drone and atmo play for 2-3 phrases, changing atmo notes so it stays alive.
- Second section: introduce one new rhythmic element that carries its own automation, and reduce automation on the drone so focus shifts. Add a quiet 16th percussion to keep energy.
- Keep the groove fairly constant but swap sequences between instruments each phrase (the same pattern on a different hat/ride/perc sound) instead of repeating loops or adding layers. A 909 ride with reverb and a flanger/frequency-shifter adds movement.
- Before drops, filter-automate the top end down then bring high-end noise back for contrast. Add a sparse FX hit (a few hat notes into a high-feedback delay with filter modulation) at some phrase starts, not all.
- Listen through and remove any element that steals attention from the drone; export and check on different systems.

### Four climax/break structures for 8-bar phrased tracks: (1) committed turnaround, where the last part of an 8-bar loop is cut and deconstructed before the next section restarts; (2) linear rise, an 8-bar section with most elements removed that only builds (filters open, decay/release and reverb/delay times lengthen, new layers enter) until the full section returns; (3) trilogy break: fall (strip chords/rhythm to a few disorienting elements, optionally introduce a new chord progression), rise (percussion and opening filters build), hang (withhold the expected return for a bar with one unique phrase, then return); (4) double trilogy, where a long fall/rise is followed by a short fall/rise inside the same break
Source: [How to climax in electronic music](https://www.youtube.com/watch?v=dGGMbqe4QYQ) · was `climax-break-structures-committed-turnaround-linear-rise-trilogy-fall-rise-hang-double-trilogy-insert-time-last`
- Phrase the track in 8-bar loops and mark section boundaries.
- Committed turnaround: at the end of an 8-bar loop, cut the last bar or two of the loop and deconstruct it (drop elements, filter or reverb-throw what remains), then restart the next section; swap a couple of elements in or out at that point.
- Linear rise: take an 8-bar section, remove most elements, then from the moment of removal build continuously: open low-pass filters, lengthen decay/release, raise reverb/delay time and send, and bring in new sustained layers or a noise sweep, so energy releases when the full section returns.
- Trilogy break, chapter 1 (fall): coming out of a full section, remove chords and most rhythm, leaving a few elements; hold 4-8 bars. Optionally introduce a new chord progression here, kept low in energy.
- Chapter 2 (rise): 4-8 bars of building: percussion returns, filters open, sustained layers and noise sweeps enter.
- Chapter 3 (hang): where the full section would return, withhold it for about a bar with one unique element (a single pad swell, chord or phrase), then bring the full section back.
- Double trilogy: inside one break, do a long fall + rise, then where the return is expected do a second, shorter fall + rise before the section comes back (filters can bring percussion back in).
- When the arrangement is otherwise finished, insert the hang bar(s) with insert-time so everything after shifts together.

### Dynamic-interest block map for loop-based tracks: 10 x 16-bar blocks drawn on paper, top-percussion gear shifts at every block, one committed break vs half-block turnarounds, 1-3 bar squeeze-ins, sparing markers/reverses, +/- density from call-and-response or polymeter layers, scoop-ups and minimalism moments
Source: [6 key concepts for arranging techno](https://www.youtube.com/watch?v=JHiTUBVLmFI) · was `dynamic-interest-16-bar-block-map-top-perc-gear-shifts-break-turnaround-squeeze-in-markers-reverses-plus-minus-layers-scoop-up-minimalism`
- Finish one core groove you are happy with and design all the extra ingredients on it before spreading anything on the timeline.
- Draw the canvas: blocks of 16 bars (~30 s each at most dance tempos); a ~5-minute track is 10 blocks. Literally draw 10 stripes on paper.
- Tool 1, top-percussion gear shifts: prepare many top-percussion options (closed and open hats, rides, near and far, short and long, a backbeat clap, a short noise hit around 500 Hz, a rim). At every block boundary add and/or remove some so each block has its own high-end profile.
- Tool 2, breaks and turnarounds: mark one whole block as the break (e.g. block 6), removing the kick and low percussion and returning them at the drop. Mark turnarounds in the second half of some blocks (e.g. blocks 4 and 8): scoop out lows and/or add contrasting top material without interrupting the block flow. Prepare a contrasting timbre (effects that reset the sound world) for them.
- Squeeze-ins: in the middle of the track only, add 1-3 bars of contrast between blocks (e.g. after the first and last turnarounds). Prep by appending ~3 bars of silence after the 16-bar loop and designing contrast material there.
- Tool 3, markers and reverses: place a marker (cymbal or noise splash) at the start of only a few blocks, and reverses (a build of fullness, e.g. a synth opening filter and envelopes, or printed huge-reverb swells reversed) into a few block ends, e.g. into the break and before the last block. Print several reverse layers ahead of time, many in the highs, some in the mids.
- Tool 4, density marks: prepare a couple of call-and-response phrases (call, gap, response, small turnaround) and polymeter layers. Mark blocks with + (one layer), ++ (several) or - (stripped, e.g. intro/outro) and add or remove the layers accordingly.
- Tool 5, scoop-up and minimalism moments: at a block start, remove the lows for 1-4 bars and bring them straight back (scoop-up); after a dense passage, strip to the essentials (e.g. kick + lead, no hats) for 2-4 bars before everything returns.
- Tool 6 (optional): duplicate the main synth and perform cutoff and envelope lengths by hand across the arrangement, keeping the loop version as a fallback. Then lay out the track from the drawn plan and adjust where theory and practice disagree.

### Electronic tension levers: a pad on the minor sixth (or fourth) over the bass root only at the end of the bar resolving to a consonant note on the downbeat, an early resolve before the bar when energy should drop into a breakdown, a short silence before the kick and bass return, and a freeze-reverb riser whose size is automated from consonant into dissonant territory
Source: [Tips and Tricks for Creating Tension in Electronic Music](https://www.youtube.com/watch?v=IuscQShlL58) · was `end-of-bar-dissonant-pad-minor-sixth-over-root-resolve-on-downbeat-early-resolve-for-energy-drop-silence-break-freeze-reverb-size-riser`
- Loop a kick and bass on the root (e.g. C). Write a pad that holds the root for most of the bar, then steps to the minor sixth (G#) or fourth (F) for the last beat(s); bring its filter cutoff in by automation.
- Resolve on the downbeat: the next bar begins on a consonant note/chord (root or fifth). A/B against a version where the end-of-bar note is the fifth (G) to hear the difference.
- For an energy drop into a breakdown, resolve the pad just before the next downbeat (render the pad to audio for precise control of the reverb tail), then strip percussion and soften the synths in the new section.
- Before a return, cut the full mix to silence for a few beats at the end of a build; the kick and bass re-enter on the downbeat.
- Freeze riser: play a consonant chord into a reverb with size and decay high, write automation, freeze immediately, let it hold, then automate size on a long curve so the frozen tone moves into dissonance. Raise dry/wet more than usual, render to audio and fade it in.
- Place renders and pad tension only at structural points (bar ends before section changes) so the levers keep their effect.
