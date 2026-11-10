import json
from pathlib import Path
R=Path('/workspace/skill-library')
AFF="Original synthesis/processing recipe; not affiliated with Ableton, Reason, Bitwig, Soundtoys, FabFilter, Eventide or any vendor. Map product devices to generic modules (sampler, noise osc, filter, envelope, LFO, EQ, saturator, compressor, delay, reverb) in any DAW, hardware or Web Audio."
STEADY="Steady pitch: no random pitch wobble or randomised notes; no rapid clicking textures (Matt's preference)."
def S(vid,title,sid,name,goal,pre,inputs,outputs,cons,steps,ver,tags):
    d={"schema_version":"1.0","id":sid,"name":name,"goal":goal,"domain":"cinematic-synth",
       "source":{"kind":"youtube-transcript","video_id":vid,"url":f"https://www.youtube.com/watch?v={vid}","title":title,"transcript":"youtube-provided",
                 "distilled_path":f"distilled/{vid}/agent-skill-{sid}.json","batch":"2026-11-10-morning-hunt"},
       "prerequisites":pre,"inputs":[dict(zip(("name","type","description","required"),i)) for i in inputs],
       "outputs":[dict(zip(("name","type","description"),o)) for o in outputs],
       "constraints":cons+[AFF,STEADY],
       "steps":[{"n":n+1,"action":a,"tool":t,"expect":e} for n,(a,t,e) in enumerate(steps)],
       "verification":ver,"tags":tags+["portable","cinematic-synth"],"curriculum_ids":["curriculum-cinematic-hybrid-synth"],"mcp_resource":f"skill://{sid}"}
    p=R/'distilled'/vid; p.mkdir(parents=True,exist_ok=True)
    (p/f'agent-skill-{sid}.json').write_text(json.dumps(d,indent=2,ensure_ascii=False)+"\n"); print(p/f'agent-skill-{sid}.json')

S("27ewHn5SAiI","The SCIENCE of Mixing Perfect Kick and Bass",
 "kick-bass-interval-aware-low-end-saturate-octave-harmonic-exciter-transient",
 "Interval-aware kick + bass low end: pick bass notes that avoid semitone-adjacent clashes with the kick fundamental (move the bass up an octave), EQ out kick overtones that crowd the bass fundamental, saturate the kick so its harmonics land on octaves, then exciter and a mild transient expander to separate both in the mids",
 "Make kick and bass distinct by combining composition and processing, based on the physics that low notes are only a few Hz apart (E1 41.2 Hz vs F1 43.6 Hz, ~6% steps) so near-neighbour low notes beat and phase-cancel. Delta vs bass cluster (four-level kick+bass lock, short kick + 3 ducked subs): this one chooses bass pitches against the kick's tuned fundamental and overtones and shapes kick harmonics to octaves rather than relying on ducking.",
 ["A tuned kick (know or measure its fundamental note, e.g. with a spectrum analyser)","EQ, saturator, exciter and transient shaper/expander on kick and bass"],
 [("kick","audio","Kick drum with a measurable fundamental",True),("bassline","midi","Bass part to place against the kick",True)],
 [("low_end","audio","Kick + bass with fewer beating/phase-cancelling clashes and clearer mid-range identity")],
 ["Use the 6%-per-semitone rule: in the lows adjacent semitones are only ~2-3 Hz apart and beat audibly; in the mids they are ~26 Hz apart.","Keep processing mild: transient expansion acts on roughly the first 50 ms; exciter and saturation are for distinction, not loudness.","Steady pitch only; no pitch-wobble tricks on kick or bass."],
 [("Find the kick's fundamental note (e.g. E1 = 41.2 Hz) with an analyser and note its main overtones (e.g. F#2).","Spectrum analyser","Kick fundamental and overtone notes written down"),
  ("Check where bass notes land on kick hits. If a bass note is a semitone or tone from the kick fundamental in the same octave (e.g. kick E1, bass F1), move the bass up an octave (F2) or re-voice it so it isn't adjacent.","MIDI edit","No near-neighbour low notes sound together on kick hits"),
  ("If a kick overtone sits next to the bass fundamental (kick F#2 vs bass F2), cut that overtone on the kick with a narrow EQ bell.","EQ on kick","Bass fundamental no longer beats against the kick"),
  ("Add a saturator to the kick so new harmonics are multiples of its fundamental (e.g. E3 above E1). These are more musical and clash less with the bass than the original stray overtone.","Saturator on kick","Kick has octave-related harmonics, sounds more distinct from bass"),
  ("Put an exciter on kick and on bass to add higher-order harmonics, lifting both into the mids and high mids where notes are far apart and phase cancellation is minor.","Exciter on kick and bass","Each is identifiable in the mids"),
  ("Add a mild transient expander to kick and bass to emphasise the overtones in the first ~50 ms (attack/decay).","Transient expander","Clearer attacks; instruments separate without more low end"),
  ("A/B the low end in solo and in the mix; listen for periodic beating (the binaural-beat-like wobble) on simultaneous hits.","A/B","No steady beating on kick+bass hits; both distinct")],
 ["No kick hit coincides with a bass note within ~2 semitones of the kick fundamental in the same octave.","Spectrum shows kick harmonics at octave multiples after saturation and the clashing overtone reduced.","Solo low-pass (<150 Hz) shows no periodic beating on simultaneous hits."],
 ["kick","bass","low-end","interval","phase-cancellation","saturation","exciter","transient-shaper","mix"])

S("u4tg0u-THS8","How to Combine Synths with Orchestra",
 "hybrid-orchestra-four-synth-roles-sub-pulse-pad-chord-tone-pluck-ostinati",
 "Hybrid orchestral cue: add four synth roles from the ground up to an orchestral arrangement — sine sub an octave under the bass, a straight quarter/eighth pulsing bass, quick-attack polyphonic chord pads, then 2-3 staccato pluck ostinati using only chord tones, each repeating every 1-2 beats and each layer slightly more complex",
 "Turn an orchestral arrangement into a hybrid (Spider-Verse-style) score by layering synths by role, bottom to top. Delta vs arrangement cluster (role-first hybrid layering, 7-section arc with chord-tone ostinato): a concrete ordered four-role recipe for synths over orchestra with a graded polyrhythmic chord-tone pluck stack.",
 ["An existing orchestral arrangement (bass line, chord progression)","Any synth (presets or simple self-made patches): sine, bass, poly pad, short plucks"],
 [("orchestral_arrangement","midi/audio","Main section with bass line and chords",True)],
 [("hybrid_section","midi/audio","Same section with sub, pulse bass, pads and a 2-3 layer pluck ostinato texture")],
 ["Sub must be a simple sine or low-harmonic patch; harmonically rich subs muddy the mix.","Pads need polyphony and a quick attack.","Plucks: quick attack and near-immediate release (staccato); only chord tones; no new melodies.","Steady, repeating patterns; no random or wobbling pitch (Matt's preference)."],
 [("Listen to the orchestral section alone and note its bass line and chords.","Playback","Reference before synths"),
  ("Sub bass: a simple sine (or low-harmonic synth) plays the bass line one octave below the other bass instruments. It should be felt more than heard.","Sine synth","Extra size and weight, no mud"),
  ("Pulsing bass: a simple bass synth plays the bass line in straight quarter or eighth notes (play or pencil them in).","Bass synth","Constant rhythmic floor for other rhythmic parts"),
  ("Harmonic pads: a polyphonic, quick-attack pad plays the chord progression as sustained chords, either doubling strings/brass or in its own register.","Poly pad","Chords sustained like strings"),
  ("Pluck layer 1: a staccato pluck plays a short pattern of the common tones between chords, repeating every beat or two, with at most one embellishment.","Pluck synth","Simple rhythmic base layer"),
  ("Pluck layer 2: a second pluck plays a rhythmic arpeggio of chord tones in a short repeating pattern.","Pluck synth","More motion, still chord-only"),
  ("Pluck layer 3 (optional): the most adventurous pattern spanning up to an octave, still chord tones only.","Pluck synth","Polyrhythmic composite texture"),
  ("Play all layers together with the orchestra and balance them.","Mix","Energetic, coloured hybrid texture")],
 ["Sub is exactly one octave below the lowest orchestral bass line.","Every pluck note is a chord tone of the current chord.","Each pluck pattern repeats within 1-2 beats; layer complexity rises from layer 1 to 3."],
 ["hybrid-score","orchestra","sub-bass","pulse-bass","ostinato","polyrhythm","arrangement","chord-tones"])
