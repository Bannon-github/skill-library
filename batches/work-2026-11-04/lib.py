import json,sys,glob
from pathlib import Path
from datetime import datetime,timezone
R=Path('/workspace/skill-library'); now=datetime.now(timezone.utc).isoformat()
pairs=[a.split(':') for a in sys.argv[1:]]  # vid:cluster
L=json.load(open(R/'LIBRARY.json')); added=[]
for vid,cid in pairs:
    f=glob.glob(str(R/'distilled'/vid/'agent-skill-*.json'))[0]; d=json.load(open(f))
    eid=f'cinematic-synth-{vid}'; ent=[e for e in L['entries'] if e['id']==eid]
    if ent:
        if cid not in ent[0]['skills']: ent[0]['skills'].append(cid)
    else:
        L['entries'].append({"id":eid,"video_id":vid,"url":d['source']['url'],"title":d['source']['title'],"topic":"cinematic-hybrid-synth",
          "transcript_source":"youtube-provided","transcript_file":f"raw/{vid}/raw.txt","summary":f"Skills: {d['id']} (folded into {cid})","skills":[cid]})
    added.append({"video_id":vid,"skill":d['id'],"cluster":cid})
L['entry_count']=len(L['entries']); L['updated_at']=now
L.setdefault('merge_log',[]).append({"at":now,"batch":"2026-11-04-morning-hunt","folded":added})
(R/'LIBRARY.json').write_text(json.dumps(L,indent=2,ensure_ascii=False)+"\n")
I=json.load(open(R/'mcp-publish/index.json'))
allj=[json.load(open(p)) for p in sorted((R/'mcp-publish/skills').glob('*.json'))]
I['skills']=[{k:x.get(k) for k in ('id','name','goal','domain','tags','mcp_resource')} for x in allj]; I['count']=len(allj); I['updated_at']=now
(R/'mcp-publish/index.json').write_text(json.dumps(I,indent=2,ensure_ascii=False)+"\n")
print(len(added),'entries; library',L['entry_count'],'index',I['count'])
