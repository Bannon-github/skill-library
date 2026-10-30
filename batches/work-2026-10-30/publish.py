import json, sys, shutil
from pathlib import Path
from datetime import datetime, timezone
ROOT=Path('/workspace/skill-library'); BATCH='2026-10-30-morning-hunt'
now=datetime.now(timezone.utc).isoformat()
files=[Path(f) for f in sys.argv[1:]]
L=json.load(open(ROOT/'LIBRARY.json')); I=json.load(open(ROOT/'mcp-publish/index.json'))
T=json.load(open(ROOT/'topics/taxonomy.json')); C=json.load(open(ROOT/'curriculums/curriculum-cinematic-hybrid-synth.json'))
lib_ids={e['id'] for e in L['entries']}; idx_ids={s['id'] for s in I['skills']}
cat=[c for c in T['categories'] if c['id']=='cinematic-hybrid-synth'][0]
lv3=[l for l in C['levels'] if l['level']==3][0]
added=[]
for f in files:
    d=json.load(open(f)); sid=d['id']; vid=d['source']['video_id']
    shutil.copy(f, ROOT/'mcp-publish/skills'/f'{sid}.json')
    if sid not in idx_ids:
        I['skills'].append({k:d[k] for k in ('id','name','goal','domain','tags','mcp_resource')}); idx_ids.add(sid)
    eid=f'cinematic-synth-{vid}'
    ent=[e for e in L['entries'] if e['id']==eid]
    if ent:
        if sid not in ent[0]['skills']: ent[0]['skills'].append(sid); ent[0]['summary']='Skills: '+', '.join(ent[0]['skills'])
    else:
        L['entries'].append({"id":eid,"video_id":vid,"url":d['source']['url'],"title":d['source']['title'],"topic":"cinematic-hybrid-synth",
          "transcript_source":"youtube-provided","transcript_file":f"raw/{vid}/raw.txt","summary":f"Skills: {sid}","skills":[sid]})
    if sid not in cat['skill_ids']: cat['skill_ids'].append(sid)
    if sid not in lv3['skills']: lv3['skills'].append(sid)
    md=[f"# {d['name']}","",f"Goal: {d['goal']}","",f"Source: [{d['source']['title']}]({d['source']['url']})",""]
    md+= [f"{s['n']}. {s['action']}" for s in d['steps']]
    note=d['source'].get('transcript_note')
    md+=["",f"Batch: `{BATCH}` · transcript: YouTube-provided (Show transcript)"+(f" · {note}" if note else "")]
    (ROOT/'skills'/f'{sid}.md').write_text("\n".join(md)+"\n")
    added.append(sid)
L['entry_count']=len(L['entries']); L['updated_at']=now
log=[m for m in L['merge_log'] if m.get('batch')==BATCH]
if log: log[0]['added']=sorted(set(log[0]['added'])|set(added)); log[0]['at']=now
else: L['merge_log'].append({"at":now,"batch":BATCH,"added":added})
I['count']=len(list((ROOT/'mcp-publish/skills').glob('*.json'))); I['updated_at']=now
C['updated_at']=now
for p,o in ((ROOT/'LIBRARY.json',L),(ROOT/'mcp-publish/index.json',I),(ROOT/'topics/taxonomy.json',T),(ROOT/'curriculums/curriculum-cinematic-hybrid-synth.json',C)):
    p.write_text(json.dumps(o,indent=2 if p.name!='LIBRARY.json' else 2,ensure_ascii=False)+"\n")
print('added',added,'entries',L['entry_count'],'mcp',I['count'],'cat',len(cat['skill_ids']),'lv3',len(lv3['skills']))
