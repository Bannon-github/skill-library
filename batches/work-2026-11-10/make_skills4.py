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

S("6x1_XZDcI8I","How I Arranged Hypnotic Techno Track – Arrangement Breakdown",
 "hypnotic-drone-arrangement-phrase-layer-fade-ins-sequence-instrument-swap-drone-only-break",
 "Arrange a minimal hypnotic track around one evolving drone: record filter-cutoff automation on a one-note drone and add dissonant extra notes per section, bring percussion layers in phrase by phrase with short volume-curve fade-ins, reach the climax with rising cutoff plus a high atonal noise layer, drop to a drone-and-atmo-only hypnotic break for 2-3 phrases, then keep energy by swapping the same sequence onto a different instrument instead of adding new loops",
 "Turn a drone + groove sketch into a full, DJ-friendly minimal arrangement. Delta vs arrangement-loop-to-song cluster (build/drop, pre-drop): drone-led hypnotic structure where interest comes from recorded automation, added notes and instrument swaps, plus fade-in (curve) entries rather than hard starts.",
 ["A drone/pad patch with slow internal LFOs and a filter","Drum/percussion layers (two hat layers, shakers, noise pattern, ride), an atmo layer, delay with feedback for occasional FX","Automation recording in a DAW"],
 [("drone","midi/audio","One-note drone (e.g. on G) with slow modulation",True),("percussion_layers","audio/midi","Hats, shakers, noise pattern, ride, 16th percussion",True)],
 [("arrangement","daw arrangement","Minimal phrase-based arrangement with build, climax, drone-only break and second section")],
 ["Minimal: fewer elements give more dynamics and clarity and mix better in DJ sets; leave out sounds that pull attention from the drone.","Use few, gentle FX hits; avoid splashy or harsh noise FX every phrase and rapid clicking textures (Matt's preference).","Bring drums in early (Matt prefers drums by about bar 8); the source starts the drone abruptly — give it a short fade.","Added drone notes are steady held notes, not pitch wobble."],
 [("Hold one drone note through the track and record a pass of filter-cutoff automation while arranging, then tidy it by hand so overtones open up toward peaks.","Drone + automation record","Drone that evolves without new parts"),
  ("Add 1-2 extra held notes on the drone in later sections (e.g. G with D#, D, then G#) for dissonant tension.","MIDI","Harmonic change without a chord progression"),
  ("Build the groove phrase by phrase: lead percussion first, then a second hat layer (snappy + softer), then shakers, then a high noise pattern. Start some layers with a short volume curve (fade-in) so they blend in rather than hit on the downbeat.","Arrangement + volume automation","Steady build of intensity"),
  ("Climax: raise the drone cutoff and add the high atonal noise layer together, with a volume swell into it.","Automation","Peak intensity"),
  ("Break: drop the drums so only the drone and atmo play for 2-3 phrases, changing atmo notes so it stays alive.","Arrangement","Hypnotic drone-only moment"),
  ("Second section: introduce one new rhythmic element that carries its own automation, and reduce automation on the drone so focus shifts. Add a quiet 16th percussion to keep energy.","Arrangement","New focus without clutter"),
  ("Keep the groove fairly constant but swap sequences between instruments each phrase (the same pattern on a different hat/ride/perc sound) instead of repeating loops or adding layers. A 909 ride with reverb and a flanger/frequency-shifter adds movement.","MIDI clips + instruments","Variety at the same density"),
  ("Before drops, filter-automate the top end down then bring high-end noise back for contrast. Add a sparse FX hit (a few hat notes into a high-feedback delay with filter modulation) at some phrase starts, not all.","Filter automation + delay","Clear phrase markers"),
  ("Listen through and remove any element that steals attention from the drone; export and check on different systems.","Review","Lean, dynamic final arrangement")],
 ["New layers enter at phrase boundaries, some with a fade-in curve.","There is a drone-and-atmo-only break of at least 2 phrases.","At least two phrases reuse the same sequence on a different instrument."],
 ["arrangement","hypnotic-techno","drone","automation","phrase-building","break","minimal","transitions"])
