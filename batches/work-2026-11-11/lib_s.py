import json
from pathlib import Path
R=Path('/workspace/skill-library')
AFF="Original synthesis/processing recipe; not affiliated with Ableton, Reason, Bitwig, Soundtoys, FabFilter, Eventide or any vendor. Map product devices to generic modules (sampler, noise osc, filter, envelope, LFO, EQ, saturator, compressor, delay, reverb) in any DAW, hardware or Web Audio."
STEADY="Steady pitch: no random pitch wobble or randomised notes; no rapid clicking textures (Matt's preference)."
def S(vid,title,sid,name,goal,pre,inputs,outputs,cons,steps,ver,tags):
    d={"schema_version":"1.0","id":sid,"name":name,"goal":goal,"domain":"cinematic-synth",
       "source":{"kind":"youtube-transcript","video_id":vid,"url":f"https://www.youtube.com/watch?v={vid}","title":title,"transcript":"youtube-provided",
                 "distilled_path":f"distilled/{vid}/agent-skill-{sid}.json","batch":"2026-11-11-morning-hunt"},
       "prerequisites":pre,"inputs":[dict(zip(("name","type","description","required"),i)) for i in inputs],
       "outputs":[dict(zip(("name","type","description"),o)) for o in outputs],
       "constraints":cons+[AFF,STEADY],
       "steps":[{"n":n+1,"action":a,"tool":t,"expect":e} for n,(a,t,e) in enumerate(steps)],
       "verification":ver,"tags":tags+["portable","cinematic-synth"],"curriculum_ids":["curriculum-cinematic-hybrid-synth"],"mcp_resource":f"skill://{sid}"}
    p=R/'distilled'/vid; p.mkdir(parents=True,exist_ok=True)
    (p/f'agent-skill-{sid}.json').write_text(json.dumps(d,indent=2,ensure_ascii=False)+"\n"); print(p/f'agent-skill-{sid}.json')

