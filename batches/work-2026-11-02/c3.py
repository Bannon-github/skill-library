import sys; sys.path.insert(0,'/workspace/skill-library/batches/work-2026-11-02')
from mk import mk
A="Auto-generated YouTube Show transcript; values are as spoken and approximate where the speaker says 'about' or 'around'."
PS="Polyrhythm Studio / Web Audio mapping: OscillatorNode + GainNode per layer, BiquadFilterNode (lowpass/highpass/allpass) for filters, DelayNode/ConvolverNode for space, AudioParam automation or slow custom LFOs for movement."
TASTE_P="Steady pitch (Matt's taste): no random pitch or detune wobble; keep unison detune small and static."
TASTE_D="Drums early (Matt's taste): if the track has drums, the kick/drum loop enters by about count 8 (roughly 10-12 s), with only pad before that."

mk("63FvtgN6Yrc",'Create "Audible" Sub Bass in Ableton Live',
 "audible-sub-bass-on-phones-sine-sub-20-60hz-plus-harmonics-60-200hz-volume-compensated-hard-clip-overtone-series-octave-fifth-low-mid-scoop-lowpass-plus-2-4-octave-sines-fast-comp-tilt",
 "Make a sine sub audible on phones and laptops: keep the 20-60 Hz fundamental but add pleasing harmonics in the 60-200 Hz bass range with volume-compensated hard clipping (odd harmonics) and/or an added overtone series (octave, fifth, octave), then scoop the honky low mids, low-pass the fizz, optionally add soft sine layers two and four octaves up, and tilt toward the top only if notes are still unclear",
 "Turn a pure sine/triangle sub into a bass line whose notes can be heard on small speakers without the listener noticing the distortion. Sub (20-60 Hz) is felt, not heard; consumer speakers reproduce 60-200 Hz, so the recipe adds controlled harmonics there and then cleans up their tone. Portable as a chain of generic processors (clipper, harmonic/octave layers, EQ scoop, low-pass, fast compressor, tilt EQ).",
 ["A sine or triangle sub bass track","Hard clipper or saturator with output gain compensation, EQ with a bell cut and low-pass, a fast (multiband) compressor and a tilt EQ, or a synth that can add octave/fifth sine layers","A spectrum analyzer"],
 [("sub_track","audio/midi","Sine/triangle sub line whose notes disappear on small speakers",True)],
 [("audible_sub","audio","Sub bass with harmonics in 60-200 Hz that translates to phones"),("processing_chain","fx-chain","Clip/harmonics → scoop → low-pass (→ fast comp → tilt) chain")],
 ["Keep the effect transparent: the goal is that the listener cannot tell the sine was distorted.",
  "Real sub is only about one octave of notes (roughly 30-60 Hz); most speakers make little below 30 Hz, so judge on small speakers as well as monitors.",
  "Steady pitch (Matt's taste): harmonics are fixed intervals (octaves, fifth); no pitch modulation, detune or wobble.",
  "Original processing chain; the free device in the source is not required or copied.",
  TASTE_D, PS, A],
 [("Check the sine sub on an analyzer: only the fundamental shows, inside 20-60 Hz, and the notes are hard to make out on small speakers.","analyzer","Baseline: felt but not heard"),
  ("Add volume-compensated hard clipping and raise it slowly until the bass line becomes audible. It adds odd harmonics (e.g. one at 139 Hz for a low F sharp).","clipper + gain comp","Notes become readable; level stays the same"),
  ("Alternatively or in addition, add the harmonic overtone series to the sine: an octave, a fifth above that, and the next octave, at low levels.","harmonic layers / additive osc","A warmer, more musical set of audible harmonics"),
  ("Scoop the low mid-range that the harmonics create with a bell cut, which also emphasizes the lows and makes the bass less honky.","EQ","Fuller, less honky tone"),
  ("Low-pass the result to tame the upper harmonics and any fizz.","low-pass filter","Clean, round tone that still reads on phones"),
  ("To keep a subby, 'wumpy' character instead of grit, add soft triangle/sine-like layers two octaves up and four octaves up and set their level with the low-pass. A little saturation on top goes a long way.","octave layers","Subby tone with audible upper octaves"),
  ("For a thinner, different distortion color, compress the sub with a very fast attack and fast release (multiband if available); low-pass afterwards to clean up the aliasing junk.","fast compressor","Extra odd harmonics with a thinner tone"),
  ("If notes are still unclear, tilt the EQ to favor the top and reduce the sub, re-scoop a little and low-pass again. Check on phone/laptop speakers and on headphones.","tilt EQ + test","Bass line clearly audible across playback systems")],
 ["On a spectrum analyzer the bass now has clear energy between 60 and 200 Hz, not only below 60 Hz.",
  "Bass notes can be identified on a phone or laptop speaker.",
  "The level matches the dry sub (gain-compensated) when A/B'd.",
  "No audible fizz or aliasing above the low-pass."],
 ["bass","sub-bass","punchy-bass","harmonics","saturation","translation","mixing","eq"])
