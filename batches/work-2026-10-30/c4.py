import sys; sys.path.insert(0,'.')
from mk import mk
A="Auto-generated YouTube Show transcript; values are as spoken and approximate where the speaker says 'about' or 'around'."
mk("XRCwoFjZFMc","Synth + Pedal Sound Design Tutorial - Arturia MicroFreak and Zoom MS-70CDR",
 "eerie-dreamy-phaser-pad-supersaw-keytracked-cutoff-dual-slow-stereo-phasers-low-res-half-second-mod-delay-1-5s-pingpong-reverb-cyclic-env-cutoff-lfo-on-rise-fall",
 "Eerie, dreamy pad from a basic paraphonic supersaw patch plus outboard-style effects: cutoff key-tracked about 50%, long attack and release, two slow low-resonance phasers in stereo mode, about 0.5 s modulated delay, a second about 1.5 s ping-pong delay with a little more feedback and lower mix, a reverb with dwell at zero, then a looping (cyclic) envelope on cutoff whose rise/fall times an LFO slowly varies",
 "Turn an init-patch supersaw into a wide, whooshing, dreamy pad using mainly a phaser-delay-reverb chain. The effects do most of the work: slow stereo phasing for the whoosh, two delay lengths for stereo spread, and an irregular filter breath from a cycling envelope whose speed drifts. Fills the phaser-pad gap with a non-high-pass recipe.",
 ["A synth with a supersaw/unison oscillator, key-tracking mod and a looping (cyclic) envelope or function generator","A phaser with stereo mode, a modulated delay, a ping-pong delay and a reverb (pedal, plugin or Web Audio)"],
 [("chords","list","Up to four-note chords (paraphonic is enough)",True)],
 [("phaser_pad","synth-plus-fx-chain","Saved patch and effects chain"),("pad_audio","audio","Held chords with slow whooshing stereo motion")],
 ["Gear in the video (a small hybrid synth and a multi-effects pedal) is mapped to generic supersaw, key-tracking, cyclic envelope, phaser, delay and reverb modules.",
  "Steady pitch (Matt's taste): the modulated delay adds slight pitch movement on the repeats. Keep its modulation depth minimal or use a plain delay. Keep phaser and filter motion slow.",
  "Web Audio mapping: two allpass-chain phasers (BiquadFilterNode type 'allpass' stages with slow LFOs), offset in phase for L/R; DelayNodes at about 0.5 s and 1.5 s (ping-pong via ChannelMerger cross-feedback); the cyclic envelope is a looping attack/decay ramp on filter.frequency whose times are drifted by a very slow LFO.", A],
 [("Start from an init patch, switch to paraphonic (up to 4 notes) and choose the supersaw oscillator at default settings.","synth","Fat chordal source"),
  ("Set filter cutoff and resonance by ear, then key-track cutoff by about 50% so higher notes open the filter. Raise attack and release for a pad envelope (shorten them temporarily while designing effects).","filter + mod matrix","High octaves no longer sound dull"),
  ("Add two phasers (dual phaser) for the whoosh. Reduce the rates for slow movement, lower resonance so the effect is subtle, turn on stereo mode and reduce depth a little.","phaser","Slow, wide stereo whoosh without a sharp resonant sweep"),
  ("Add a modulated delay at default (about half a second), then a second delay of about 1.5 s with slightly more feedback, lower mix, in ping-pong mode.","delays","Repeats alternate hard left/right for maximum width"),
  ("Add a lush (particle-style) reverb with dwell set to zero, other settings default.","reverb","Soft, diffuse tail under the delays"),
  ("Automate cutoff with a cyclic (looping rise/fall) envelope, and change rise and fall times to set its rate.","cyclic envelope","Filter opens and closes rhythmically, and the delays spread each opening in stereo"),
  ("Route a slow LFO to the cyclic envelope's rise and fall times, and also directly to cutoff, so the breathing speed keeps changing.","LFO + mod matrix","Irregular, non-looping filter breaths"),
  ("Play chords, adjusting resonance, cutoff and cyclic-envelope amount live.","performance","Eerie dreamy pad that evolves under held chords")],
 ["The phaser sweep period is several seconds or longer (no fast swirl).","The stereo correlation is clearly below mono, with delay repeats alternating L/R.","Spacing between filter openings varies over a 60 s render.","High notes are as bright as low notes relative to pitch (key-tracking active)."],
 ["pad","phaser","ambient","dreamy","stereo-width","delay","cyclic-envelope","supersaw"])
