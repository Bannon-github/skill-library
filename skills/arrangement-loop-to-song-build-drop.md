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
