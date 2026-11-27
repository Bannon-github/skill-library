import sys,json; sys.path.insert(0,'/workspace/skill-library/batches/work-2026-11-27')
from lib_s import S,R
EARLY="If the kick is used in a track, drums enter early (~8 counts / ~10-12 s); only pad before that (Matt's preference)."
OURS="Values marked (ours) are starting points added by us; the source gives no number for them."

# 1 JhZU6JGvoHw -> drum-synthesis
S("JhZU6JGvoHw","Make Your Own Kick Drums - Punchy and Deep Kicks",
 "punchy-deep-kick-tuned-to-track-root-sine-sub-hold-decay-unipolar-pitch-env-driven-lp-filter-env-noise-attack-eq-transient-compression",
 "Punchy, deep kick in one synth tuned to the track's root: sine sub, hold+decay amp envelope, a unipolar pitch envelope that falls onto the note, the same envelope on a driven low-pass, a low-level one-shot noise attack, then EQ / transient / compression shaping",
 "Synthesize a punchy deep kick from scratch in three parts (sub, harmonic body, attack): mono, max oscillator quality; sine 2 octaves down tuned to the track's fundamental; amp envelope hold ~100 ms, decay ~100 ms, sustain -inf; a second envelope (sustain 0) routed UNIPOLAR to coarse pitch so it starts high and falls exactly onto the note (steeper = punchier, more amount = pitchier); the same envelope on a low-pass cutoff that clears the mids, with the filter driven for harmonics; a one-shot noise attack layer mixed low; then lengthen/shorten with hold+decay against the snare and hats, low boost, cut 300-400 Hz mud, transient shaper for more/less attack, heavy compression with make-up gain (slower attack keeps the transient, faster attack fattens).",
 ["A synth with 1 oscillator, noise oscillator, filter and two envelopes (any DAW)","EQ, transient shaper, compressor"],
 [("track_root","string","Track key root for kick tuning, e.g. F#",True),("tempo","number","Track tempo",False)],
 [("kick","audio","One-shot kick tuned to the track root"),("kick_patch","preset","Patch with hold/decay and pitch-envelope amount exposed")],
 ["Pitch and filter envelope modulation must be unipolar (one-direction) so the sweep ends exactly on the played note.","Noise attack stays a single short transient per hit, mixed low; no rolls or rapid clicking.",EARLY,"Check on both headphones and speakers."],
 [("Init the synth; set oscillator quality to max and voice mode to mono (no overlapping kicks).","Synth global","Mono, clean kick voice"),
  ("Osc 1 = sine, transposed down 2 octaves; play the track's root (e.g. F#) so the kick is tuned to the song's fundamental.","Oscillator","Deep sub tone in key"),
  ("Amp envelope: attack 0, hold ~100 ms, decay ~100 ms, sustain -inf. Adjust hold/decay for length; extend the MIDI note so it doesn't cut the tail.","Envelope 1","Kick-shaped sub"),
  ("Envelope 2 (attack 0, short decay, sustain 0) -> osc coarse pitch, set unipolar so it starts high and falls onto the note; steepen the curve. Less amount/slower = more body; more/faster = more attack and pitchiness.","Envelope 2 + mod matrix","Punchy pitch drop ending on the root"),
  ("Route the same envelope (unipolar) to a low-pass cutoff so mids/highs sweep away quickly; lower master level and drive the filter for extra harmonics.","Filter + drive","Fuller, thicker body without mud"),
  ("Add a noise oscillator in one-shot mode (an attack/kick-noise sample, or a layered click sample if the synth has no noise) through the filter; raise it only until the start feels consistent.","Noise osc","Defined, consistent attack"),
  ("Play against snare and hats; fine-tune hold, decay and pitch-envelope amount so the kick fits the groove.","Piano roll","Kick sits with the drums"),
  ("Mixer: boost low end if needed, cut around 300-400 Hz to clear mud, optional high boost for more attack.","EQ","Clean low end, controlled click"),
  ("Optional light overdrive/clipping for grit; transient shaper attack up/down to dial the click.","Saturator + transient shaper","Kick character matched to the track"),
  ("Compress the kick fairly hard with make-up gain: slower attack keeps the transient, faster attack trades click for fatness. Check on speakers and headphones.","Compressor","Fat, punchy kick")],
 ["Kick fundamental (end of pitch drop) equals the track root within 1 semitone.","Pitch envelope is one-directional: the pitch never dips below the note.","Amp envelope reaches silence within hold+decay (+ tail) and does not overlap the next hit (mono).","Spectrum shows a reduced 300-400 Hz region versus the unprocessed kick.","Drums in by ~8 counts in any track demo; peak below 0 dBFS."],
 ["kick","drum-synthesis","punchy","sub","pitch-envelope","tuned-kick","compression","transient"])

# 2 8eAQ0VdW0Cw -> drum-synthesis
S("8eAQ0VdW0Cw","How To Kick (a discussion of kick drum synthesis)",
 "soft-felt-to-punchy-kick-dial-attack-vs-tone-pitch-env-amount-x-time-separate-attack-layer-saw-or-bandpass-noise-fm-body",
 "Soft/felt-to-punchy kick dial: treat the kick as attack + tone, set character with pitch-envelope amount x time, then soften the body and give the attack its own blendable layer (short pitch-dropped saw or short band-passed noise)",
 "Delta over the punchy/acoustic kick variants: one map for the whole soft-to-punchy range. Kick = attack (beater on skin) + tone (sustaining body). Character comes from balancing pitch-envelope AMOUNT against its decay TIME: big amount + slow = tom/zap, big + very fast = click, moderate + slower with a softened amp attack = soft/felt kick, zero = tubby sine. For a felt kick, make the body layer soft (small, slower pitch drop, amp attack softened, shorter decay) and add the attack on a SECOND layer whose tone and level are independent: a very short saw with a fast pitch drop, or very short band-passed noise whose pitch knob sets the band centre; combining both feels more acoustic. The body layer can be swapped for FM, and drive/wavefold/bit-reduction add grit.",
 ["A synth or drum voice with two layers/oscillators, pitch envelope, noise (band-pass) and optional FM/drive"],
 [("character","string","soft/felt | balanced | punchy",True),("track_root","string","Key root for the body pitch",False)],
 [("kick","audio","Kick at the chosen character"),("attack_layer","audio","Separate attack layer for blending")],
 ["Attack layer is one short transient per hit (no repeats, no rapid clicking); keep it subtle for soft/felt kicks.","Body pitch drop is a single smooth fall, not wobble.",EARLY,OURS],
 [("Layer 1 only: sine body, linear or exponential attack-decay envelope, short decay, pitched low. Note a near-zero amp attack already gives an implied click.","Layer 1","Plain 'tubby' sine kick"),
  ("Add a pitch envelope (attack-decay) to layer 1 and sweep its amount and time: large + slow = tom/zap, large + very fast = a click, moderate = punch. Pick the balance for the target character.","Pitch envelope","Character set by amount x time"),
  ("Soft/felt: lower the amount, slow the drop (40-80 ms, ours), soften the amp attack (2-5 ms, ours) and shorten the decay so the front is no longer clicky.","Layer 1 envelopes","Soft, rounded body without a hard click"),
  ("Layer 2 attack option A: sawtooth with a high, very fast pitch drop and a very short decay; set its level and tone independently of the body (pitch higher = pingier, lower = scratchier).","Layer 2 oscillator","Blendable beater attack"),
  ("Layer 2 attack option B: band-passed noise with a very short decay; the noise 'pitch' moves the band centre. Works best when the body is short too.","Layer 2 noise","Felt/acoustic-feeling attack (room/snare-wire impression)"),
  ("Optionally combine A on layer 1's pitch drop with B noise on layer 2 for a classic sine kick plus noise punch.","Both layers","Fuller, more 'real' kick"),
  ("Optional colour: swap the body to fast FM, or add gentle drive / wavefold / bit reduction for higher harmonics.","FM / drive","Body variations beyond the plain sine")],
 ["Soft/felt version: no single-sample spike at onset; first 5 ms ramps rather than jumps (ours: amp attack >= 2 ms).","Attack layer level adjustable without changing body pitch or decay.","Punchy version has a faster pitch drop than the soft version (measured pitch reaches the root sooner).","Drums in by ~8 counts in any track demo; peak below 0 dBFS."],
 ["kick","drum-synthesis","soft-kick","felt-kick","punchy","pitch-envelope","attack-layer","band-pass-noise","fm"])

# 3 0qOs9e5UwAU -> brightness-and-air-at-the-source
S("0qOs9e5UwAU","How to Create Unique PADS in VITAL, Serum and Phaseplant",
 "four-role-atmospheric-pad-lp-low-wavetable-hp-harsh-high-layer-octave-up-triangle-key-tracked-noise-sample-chorus-phaser-flanger-delay-reverb-eq-placement",
 "Four-role atmospheric pad with air built in at the source: low-passed low wavetable layer, high-passed harsh high layer an octave up on an unsynced morph rate, an unfiltered octave-up triangle for tone, and a key-tracked noise sample through the same high-pass; then chorus, a little phaser/flanger, ping-pong delay, reverb and EQ placement",
 "Beyond 'attack + release + unison + reverb': split one patch into roles. Osc 1 low layer (smooth wavetable, position on a 1-bar LFO, unison, attack, low-pass). Osc 2 high layer (harsh/digital wavetable +1 octave, position LFO at a free rate in seconds so it never morphs in step with osc 1, unison, through a HIGH-PASS so only its upper harmonics remain: this is the air). Osc 3 triangle +1 octave with unison, unfiltered, carries the pitch. Noise/sample osc: a steady broadband recording (e.g. a box fan) with key tracking ON, pitched to match osc 3, through the high-pass. Balance levels, then chorus, phaser and flanger mixed in lightly (flanger feedback down), ping-pong delay with one side at 1/4, a long large reverb, EQ to place the pad high or low. Macro the unison detune of all three oscillators.",
 ["A multi-oscillator wavetable synth with a sample/noise oscillator and two filters (Vital is free)","Chorus, phaser, flanger, delay, reverb, EQ"],
 [("chords","list","Pad chords/notes",True),("tempo","number","For the 1-bar LFO and 1/4 delay",True),("placement","string","high | full | low pad",False)],
 [("pad","audio","Atmospheric pad with built-in air layer"),("patch","preset","Patch with detune macro")],
 ["Wavetable-position LFOs move timbre only, never pitch; the free-rate LFO is a steady periodic LFO (not random/S&H).","Phaser/flanger mixed low as colour, not a sweeping effect; no rapid clicking textures.","Noise layer must be key-tracked so its colour follows the chord."],
 [("Osc 1 (low layer): choose a smooth wavetable, LFO 1 (1 bar) -> wavetable position, add unison and a slow attack, send to filter 1 low-pass and bring the cutoff down.","Osc 1 + LFO 1 + LP","Deep smooth foundation"),
  ("Osc 2 (high layer): choose a harsh/digital wavetable with rich highs, +1 octave, LFO 2 -> position at a free rate in seconds (not tempo-synced) so it morphs out of step with osc 1, unison, send to filter 2 set to HIGH-PASS.","Osc 2 + LFO 2 + HP","Shimmering upper 'air' only"),
  ("Osc 3 (tonal layer): basic triangle, +1 octave, unison, bypass the filters.","Osc 3","Clear pitch centre that backs the other layers"),
  ("Noise/sample osc: load a steady broadband sample (e.g. box fan), turn keyboard tracking on and tune it to osc 3, route through the high-pass filter.","Sample osc + HP","Key-tracked textural air"),
  ("Balance the four layers; the high layer may sound piercing alone but sits once blended.","Mixer","Rich layered tone"),
  ("FX: chorus; then a phaser and a flanger mixed in a little (flanger feedback down).","Chorus / phaser / flanger","Smoother, more atmospheric motion"),
  ("Ping-pong delay with one side at 1/4, then a long, large reverb with mix up; skip the reverb filter.","Delay + reverb","Spacious atmospheric pad"),
  ("EQ to place the pad (cut lows for a high pad, cut highs for a deep pad); if still too bright/tonal/noisy, rebalance the source layers.","EQ","Pad fits its slot in the track"),
  ("Map one macro to the unison detune of oscs 1-3 for later tweaking.","Macro","Quick width/detune control")],
 ["Spectral centroid of the full pad is higher than the low layer alone, and the high layer alone has little energy below its HP cutoff.","Noise layer pitch follows the played chord (key tracking on).","Osc 1 and osc 2 position LFO rates are not integer-related to the tempo pair (they drift apart).","No pitch modulation on any oscillator; peak below 0 dBFS."],
 ["pad","air","brightness","wavetable","high-pass","noise-layer","key-tracking","layering","chorus","phaser"])
