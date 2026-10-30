import sys; sys.path.insert(0,'.')
from mk import mk
A="Auto-generated YouTube Show transcript; values are as spoken and approximate where the speaker says 'about' or 'around'."
mk("vzlZ4GabrAs","3 SIMPLE transitions WITHOUT using risers or snare roll build ups",
 "three-riser-free-transitions-solo-lead-pad-filter-down-drop-clap-on-beat-no-kick-hp-bass-single-tom-hit-strip-to-hats-tease-lead-variations-short-fill-all-in",
 "Three section transitions with no big risers or snare rolls, for simple two-chord tracks: (1) the lead plays alone while the pad's filter closes, a simple sweep and a lead variation, then kick, hats and bass drop in; (2) keep open hats, filter the pad down, put a clap on the beat with no kick and a high-passed bass, loop a lead variation, then one quarter-note tom hit opens the drop with the bass filter removed; (3) strip to the hat loop, tease lead variations (velocity, pan, spacing) with no kick or bass, then a very short fill and everything returns at once",
 "Make transitions by subtraction and re-entry instead of piling on FX. Simple material needs simple transitions. The kick-plus-bass re-entry is the payoff, and the kick acts as the track's metronome that listeners wait for. A riser-free counterpart to the section transition toolkit and the three-track automation sketch.",
 ["A loop-based arrangement with kick, closed and open hat loops, clap, bass, pad and a simple lead","A filter on the pad and bass, one tom or short-fill sample, optional short sweep"],
 [("sections","list","Intro, first drop, mid section, final payoff",True),("lead_variations","list","Small variations of the main lead (different velocities, pan, spacing)",True)],
 [("transition_map","list","Per-boundary list of what drops out, what stays and what re-enters"),("arrangement","daw-session","Track with three riser-free transitions")],
 ["Fits Matt's taste: keep a kick or drum loop running from early in the intro, since these transitions work by pulling the drums out briefly and slamming them back.",
  "Keep the payoff re-entry together: kick and bass on the same downbeat.",
  "Portable to Polyrhythm Studio as gain/filter automation per layer; no samples copied.", A],
 [("Intro to first drop: run the intro with just the kick and a closed-hat drum loop, and the pad opening and closing on a filter. At the end, let the pluck/lead play on its own with the pad filter coming down, a simple sweep and a lead variation as the last bar.","arrangement + filter","Energy drops to the bare lead just before the boundary"),
  ("Land the first drop with kick, closed hats, open hats and the bassline entering together.","arrangement","Clear drop without any fill"),
  ("Mid transition, part 1: play a lead variation, then return to the original. Keep the open hats, low-pass the pad steadily down, mute kick and closed hats, add a clap on the beat and high-pass the bassline.","mute + filter automation","Tension without low end"),
  ("Mid transition, part 2: loop the lead variation and let the clap settle. Place one tom hit (about a quarter note long) in the last beat's space before the downbeat.","arrangement","The single hit 'chops' the space and announces the drop"),
  ("Re-enter all drums with the second lead variation, open hats and the bass with its filter removed, so the low end hits with the kick.","arrangement","Second drop lands harder than the first"),
  ("Final payoff: strip back to the closed-hat loop and open hats with the pad dipping again, with no kick and no bass. Tease the lead with its variations (same notes, different velocity, pan and spacing, for example one extra bar of space).","arrangement","Listener waits for the kick"),
  ("End the tease with a very short drum fill (sweep plus clap/snare), then bring everything back at once: drums, bass, pad and lead.","arrangement","Big payoff from the contrast alone")],
 ["No boundary uses a riser longer than about one bar or a snare-roll build.","Each drop re-entry has kick and bass starting on the same downbeat.","The mid transition has a section with no kick and a high-passed bass, followed by a single tom hit.","The lead variations differ only in velocity, pan or spacing, not in new notes."],
 ["arrangement","transitions","song-structure","subtraction","drops","drums-early"])
