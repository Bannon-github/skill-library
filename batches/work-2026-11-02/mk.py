import json, sys
from pathlib import Path
ROOT=Path('/workspace/skill-library')
AFF="Original synthesis recipe; not affiliated with any vendor named in the source. Recreate in browser/Web Audio (Polyrhythm Studio) or any hybrid synth with comparable modules; no presets, banks or samples copied."
def mk(vid,title,id,name,goal,prereq,inputs,outputs,constraints,steps,verification,tags,note=None):
    d={"schema_version":"1.0","id":id,"name":name,"goal":goal,"domain":"cinematic-synth",
       "source":{"kind":"youtube-transcript","video_id":vid,"url":f"https://www.youtube.com/watch?v={vid}","title":title,
                 "transcript":"youtube-provided","distilled_path":f"distilled/{vid}/agent-skill-{id}.json"},
       "prerequisites":prereq,
       "inputs":[{"name":a,"type":b,"description":c,"required":r} for a,b,c,r in inputs],
       "outputs":[{"name":a,"type":b,"description":c} for a,b,c in outputs],
       "constraints":[AFF]+constraints,
       "steps":[{"n":i+1,"action":s[0],"tool":s[1],"expect":s[2]} for i,s in enumerate(steps)],
       "verification":verification,"tags":tags+["portable","cinematic-synth"],
       "curriculum_ids":["curriculum-cinematic-hybrid-synth"],"mcp_resource":f"skill://{id}"}
    if note: d["source"]["transcript_note"]=note
    p=ROOT/'distilled'/vid; p.mkdir(parents=True,exist_ok=True)
    f=p/f"agent-skill-{id}.json"; f.write_text(json.dumps(d,indent=2,ensure_ascii=False)+"\n"); print(f)
