import sys; sys.path.insert(0,'/workspace/skill-library/batches/work-2026-11-02')
from mk import mk
A="Auto-generated YouTube Show transcript; values are as spoken and approximate where the speaker says 'about' or 'around'."
PS="Polyrhythm Studio / Web Audio mapping: OscillatorNode + GainNode per layer, BiquadFilterNode (lowpass/highpass/allpass) for filters, DelayNode/ConvolverNode for space, AudioParam automation or slow custom LFOs for movement."
TASTE_P="Steady pitch (Matt's taste): no random pitch or detune wobble; keep unison detune small and static."
TASTE_D="Drums early (Matt's taste): if the track has drums, the kick/drum loop enters by about count 8 (roughly 10-12 s), with only pad before that."

mk("MULPJOhSrZ0","Get BETTER ambient bass EVERY time",
 "ambient-bass-mono-voice-light-unison-one-slow-master-lfo-4-bars-on-12-targets-wt-cutoff-drive-formant-fm-macro-direct-out-sine-sub-hp-upper-layers-mono-below-100-120hz",
 "Ambient bass with a solid floor: one mono voice with light unison, a single slow retriggered master LFO (about 4 bars) on many timbre targets (wavetable position, both filter cutoffs, drive, formant, FX filter) so everything moves together, an FM macro for grit, and a clean sine sub sent direct-out past the filter while the upper layers are high-passed",
 "Make an ambient bass that guides the track with subtle, unified movement but keeps a solid low end: one mono voice, one slow master LFO driving many timbre parameters at once so the motion feels glued, an FM/osc-mix macro for extra character, and a plain sine sub routed around the filter and effects while the moving layers are high-passed above it. The everything-below-100-120 Hz stays mono.",
 ["Wavetable or hybrid synth with mono mode, unison, a mod matrix with many LFO destinations, two filters, distortion/FX and a sub or extra oscillator that can bypass the filter (direct out)","EQ with high-pass and a bass-mono/stereo-width utility"],
 [("bass_notes","midi","Long, mostly static root notes under the track",True),("tempo","bpm","Project tempo for the 4-bar LFO",True)],
 [("ambient_bass_patch","synth-preset","Mono bass with unified slow motion and a clean sine floor"),("bass_audio","audio","Bass render that moves subtly but sits solidly")],
 ["Mono below about 100-120 Hz: either one synth voice or a bass-mono utility at 100-120 Hz.",
  "Movement stays subtle: 'a little bit of motion goes a long way'. The master LFO moves timbre only, never pitch.",
  TASTE_P+" Unison here is slight and its detune is not modulated.",
  "Rebuild with original/free wavetables; no presets or patch packs.",
  TASTE_D, PS, A],
 [("Set the bass to a single voice (mono) and add light unison (the source uses 5 voices on two oscillators) for subtle motion that shows on an oscilloscope without smearing the low end.","synth","A mono bass with gentle internal movement"),
  ("Make one master LFO: retriggered on each note, slow (about 4 bars per cycle), and route it to many destinations at small amounts: wavetable position on both oscillators, filter 1 and filter 2 cutoff, distortion amount, spectral morph/harmonic stretch, a negative formant scale, and the FX distortion's filter and drive.","LFO + mod matrix","All timbre parameters drift together, so the sound stays unified and gets slightly grittier as the cycle peaks"),
  ("Add an FM macro: osc 2 frequency-modulates osc 1 (and vice versa), and the same macro brings in an offset distortion that only starts once FM is applied. Try it an octave up if it is muddy.","macro","A controllable grit/character amount"),
  ("Add an osc-mix macro that fades a third oscillator in from zero.","macro","Extra body available on demand"),
  ("For a solid floor, set a sub/extra oscillator to a plain sine with no LFO modulation and route it direct out (past the filter and effects).","sub osc routing","A stable sine sub that does not phase or move"),
  ("Put a high-pass EQ on the moving layers (or the full patch before the sub joins) so they are cut at the low end and leave room for the sine; balance the sub level by ear.","EQ","Oscilloscope shows a clean sine at the bottom with the movement above it"),
  ("Apply bass mono below about 100-120 Hz on the channel (or rely on the single voice), and A/B in the track: the bass should stand out a little and guide the track without dominating.","utility / mix","Long static notes that still feel like they are going somewhere")],
 ["The patch is mono (one voice) or mono below 100-120 Hz.",
  "One LFO drives at least 5 timbre destinations, and none of them is pitch.",
  "The sine sub is unmodulated and bypasses the filter; the moving layers are high-passed above it.",
  "Held notes change timbre slowly over about 4 bars without audible pitch wobble."],
 ["bass","sub-bass","ambient-bass","punchy-bass","modulation","wavetable","master-lfo","mono","steady-pitch"])
