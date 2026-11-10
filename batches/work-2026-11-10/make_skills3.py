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

S("3zIsQfKtUno","How to make ELECTRONICA and DOWNTEMPO like [Christian Löffler] [Cercle]",
 "organic-downtempo-groove-kick-tom-from-kick-layered-offset-claps-shaker-family-room-sends",
 "Organic downtempo/electronica groove at 115-120 BPM (Christian Löffler style): deep kick plus a tom made from the same kick (shorter, softer attack, band-passed), filtered rim with a small room, 3-4 layered hand claps with pre-claps placed slightly earlier and varied per hit, a shaker family cut from one sample at different transpositions, frequency-split hats, dark noise percussion and an ambient noise loop, all glued into small rooms; then a warm sidechained piano/pad bed",
 "Build an organic, human downtempo groove from a few samples and stock tools, then a warm bed that leaves it space. Delta vs drum-groove cluster (future-garage layers, drums under a slow pad, step-sequencer humanising, genre families): a frequency-layered organic percussion stack (kick→tom reuse, clap crowd with pre-claps, transposed shaker family, rooms) for downtempo/electronica.",
 ["A sampler/drum rack and a few organic samples (kick, rim, claps, shaker, noise/rain loop)","EQ, glue compressor, small-room reverb send, a larger hall send, sidechain compressor, simple piano and wavetable pad"],
 [("tempo","number","115-120 BPM",True),("chords","midi","Simple piano chord/dyad progression",True)],
 [("groove","audio","Layered organic drum groove"),("bed","audio","Warm piano and pad bed sidechained to the kick")],
 ["Each percussion layer takes its own frequency range so little EQ is needed.","Clap layers are offset by small amounts (a flam/pre-clap), not rolls; avoid rapid clicking textures (Matt's preference).","Play parts deliberately in key; skip the source's random-played arpeggio notes (Matt prefers steady melodies).","Drums enter early; build the break by bringing shakers in piece by piece."],
 [("Set the tempo to 115-120 BPM. Kick: a deep, thumping kick with an EQ low cut below its useful low end.","Sampler + EQ","Deep kick foundation"),
  ("Tom from the kick: duplicate the kick sample, shorten it, raise the attack so the initial thump/click disappears, and cut lows and super-highs (band-pass to the mids).","Sampler attack/decay + EQ","Tonal tom that doesn't fight the kick"),
  ("Rim/snare: a rim sample with super-lows and super-highs cut, sent to a slightly longer, small room reverb with a little chorus.","EQ + reverb send","Focused rim with room feeling"),
  ("Clap crowd: a main organic clap on the backbeat plus 2-3 hand-clap layers placed slightly before it (one clearly earlier as a pre-clap, one in between). Vary each layer's placement a little per hit. Group, glue-compress with a fastish attack and send to a very small, narrow drum room (100% wet, short decay).","Clap layers + glue + small room","Big, human 'many people clapping' clap"),
  ("Shaker family: copy one shaker sample three times, cut different pieces and transpose some (e.g. -6 and -2 semitones). The main piece plays at the start and half of each bar; the others fill the gaps; vary velocities. Darken one copy (e.g. a wet vocoder/filter) and pan it slightly behind.","Sampler slices + transpose + velocity","Hand-played shaker feel"),
  ("Hats: a bright transient hat with slight L/R panning, a lower shaker-like layer of the same sound, and a bright shaker loop on top, each in its own range.","Hats + EQ","Coherent top end without heavy EQ"),
  ("Percussion: a noise hit darkened and a second copy transposed down hard; a snare panned slightly left just before the end of the bar. Send to the room.","Noise + snare","Dynamic end-of-bar movement"),
  ("Ambience: one or two noise/rain-like loops low under the groove.","Audio loop","Constant ambient bed"),
  ("Warm bed: simple piano dyads at low velocity, smoothed attack, EQ out boom and super-highs, glue, sent to a long hall. Add a long reversed piano layer and a warm wavetable pad (closed filter, chord with an added octave). Sidechain both to the kick and keep them behind the drums.","Piano + reverse sampler + pad + sidechain","Warm emotional space that breathes with the kick")],
 ["Kick and tom don't mask each other (tom is band-passed, no initial click).","Clap layers start at slightly different times and each hit is placed a little differently.","Muting any one percussion layer removes a distinct frequency band."],
 ["downtempo","electronica","organic-drums","groove","clap-layering","shakers","room-reverb","sidechain","arrangement"])
