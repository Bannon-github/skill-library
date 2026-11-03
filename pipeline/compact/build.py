"""Compact the library (2026-11-03): merge clusters, archive originals, rewrite indexes. Idempotent-ish: run once."""
import json, glob, shutil, sys, re
from pathlib import Path
from datetime import datetime, timezone
sys.path.insert(0, str(Path(__file__).parent)); from clusters import *
R=Path('/workspace/skill-library'); P=R/'mcp-publish/skills'; MD=R/'skills'; A=R/'archive'
now=datetime.now(timezone.utc).isoformat()
(A/'merged').mkdir(parents=True,exist_ok=True); (A/'removed').mkdir(parents=True,exist_ok=True)
docs={json.load(open(p))['id']:json.load(open(p)) for p in P.glob('*.json')}
md_only=[p.stem for p in MD.glob('*.md') if p.stem not in docs]
assign={}
for cid,prefs in MEMBERS.items():
    for pre in prefs:
        for i in list(docs)+md_only:
            if i.startswith(pre): assign[i]=cid
removed={}
for i in list(docs)+md_only:
    if i in assign or i in KEEP_TOOLING: continue
    reason=next((v for k,v in REMOVE_REASONS.items() if i.startswith(k)),None)
    if reason is None and i in md_only:
        reason="off-topic: non-music how-to (md-only, never published)" if i not in ("youtube-howto-search",) else None
    if reason: removed[i]=reason
mapping=[]
def move(i,sub):
    for src,ext in ((P/f'{i}.json','.json'),(MD/f'{i}.md','.md')):
        if src.exists(): shutil.move(str(src), str(A/sub/f'{i}{ext}'))
new_docs={}
for c in CLUSTERS:
    cid=c['id']; members=[i for i,v in assign.items() if v==cid]
    sources=[]; variants=[]; tags=set(); prereq=set(); cons=[]
    for i in sorted(members):
        d=docs.get(i)
        if d:
            s=d.get('source',{}); sources.append({"from_skill":i,"video_id":s.get('video_id'),"url":s.get('url'),"title":s.get('title')})
            variants.append({"from_skill":i,"name":d['name'],"goal":d['goal'],"steps":[st['action'] for st in d['steps']]})
            tags|=set(d.get('tags',[])); prereq|=set(d.get('prerequisites',[]))
        else:
            txt=(MD/f'{i}.md').read_text() if (MD/f'{i}.md').exists() else ''
            vid=re.search(r'watch\?v=([\w-]+)',txt)
            sources.append({"from_skill":i,"video_id":vid.group(1) if vid else None,"url":f"https://www.youtube.com/watch?v={vid.group(1)}" if vid else None,"title":(txt.splitlines() or [''])[0].lstrip('# ')})
            variants.append({"from_skill":i,"name":(txt.splitlines() or [''])[0].lstrip('# '),"steps":[l for l in txt.splitlines() if re.match(r'\d+\. ',l)]})
    gen=c['generator']
    steps=[{"n":k+1,"action":a,"expect":e} for k,(a,e) in enumerate(c['steps'])]
    steps.append({"n":len(steps)+1,"action":f"Hear the theory: run `/home/box/audio-tools/bin/python {gen}` from the repo root and compare the sections; reuse its functions as a starting point for renders.","expect":"WAV in sample-lab/theory/out/ demonstrating the principle"})
    doc={"schema_version":"1.0","id":cid,"name":c['name'],"goal":c['goal'],"domain":"music-production",
      "source":{"kind":"merged-youtube-transcripts","transcript":"youtube-provided","merged_at":now,"sources":sources} if sources else {"kind":"original-theory","note":"Written from established production practice to fill a library gap; no single source video.","merged_at":now},
      "theory":c['theory'],
      "generator":{"path":gen,"python":"/home/box/audio-tools/bin/python","output":"sample-lab/theory/out/"+Path(gen).stem+".wav"},
      "prerequisites":sorted(prereq)[:12] or ["DAW or the numpy renderer in sample-lab","Headphones and a reference track"],
      "inputs":[{"name":"key","type":"string","description":"Song key/mode","required":False},{"name":"bpm","type":"number","description":"Tempo","required":False}],
      "outputs":[{"name":"result","type":"audio-or-recipe","description":"Rendered part or recipe following the workflow"}],
      "constraints":["Portable recipe; not affiliated with any vendor; do not copy factory presets or sample packs.",
        "Numbers in variants come from the source video transcripts; workflow steps are the consolidated mainstream practice.",
        "Bring drums in early and avoid pitch wobble unless asked (user preferences from daily tests)."],
      "steps":steps,
      "verification":["Render a short test and A/B against a reference at matched loudness","Run the generator and confirm it writes a WAV without error","Check mono compatibility and that no element masks the kick/bass"],
      "variants":variants,"merged_from":sorted(members),
      "tags":sorted(tags|{"music-production","workflow",cid.split('-')[0]})[:30],"curriculum_ids":["curriculum-cinematic-hybrid-synth"],
      "mcp_resource":f"skill://{cid}","aliases":sorted(members)}
    new_docs[cid]=doc
    for i in members:
        mapping.append((i,cid,"merged")); move(i,'merged')
for i,r in removed.items(): mapping.append((i,None,r)); move(i,'removed')
for cid,d in new_docs.items():
    (P/f'{cid}.json').write_text(json.dumps(d,indent=2,ensure_ascii=False)+"\n")
    md=[f"# {d['name']}","",f"Goal: {d['goal']}","",f"**Theory:** {d['theory']}","",f"**Hear it:** `{d['generator']['path']}`","","## Workflow"]
    md+=[f"{s['n']}. {s['action']}" for s in d['steps']]
    if d['variants']:
        md+=["","## Source techniques (merged, numbers kept)"]
        for v in d['variants']:
            src=next((s for s in d['source'].get('sources',[]) if s['from_skill']==v['from_skill']),{})
            md+=["",f"### {v['name']}",f"Source: [{src.get('title')}]({src.get('url')}) · was `{v['from_skill']}`"]
            md+=[f"- {a if not re.match(r'^\d+\. ',a) else a.split('. ',1)[1]}" for a in v['steps']]
    (MD/f'{cid}.md').write_text("\n".join(md)+"\n")
# aliases
AL=json.load(open(R/'mcp-publish/aliases.json'))
for old,new,_ in mapping:
    if new: AL['aliases'][old]=new
for k,v in list(AL['aliases'].items()):
    if v in dict((o,n) for o,n,_ in mapping if n): AL['aliases'][k]=dict((o,n) for o,n,_ in mapping if n)[v]
AL['updated_at']=now; AL['note']+=" 2026-11-03 compaction: merged ids resolve to cluster skills; see archive/MAPPING.md."
(R/'mcp-publish/aliases.json').write_text(json.dumps(AL,indent=2)+"\n")
# index
I=json.load(open(R/'mcp-publish/index.json'))
allj=[json.load(open(p)) for p in sorted(P.glob('*.json'))]
I['skills']=[{k:d.get(k) for k in ('id','name','goal','domain','tags','mcp_resource')} for d in allj]; I['count']=len(allj); I['updated_at']=now
(R/'mcp-publish/index.json').write_text(json.dumps(I,indent=2,ensure_ascii=False)+"\n")
# library / taxonomy / curricula id remap
remap={o:n for o,n,_ in mapping}
def fix(lst):
    out=[]
    for x in lst:
        if not isinstance(x,str): out.append(x); continue
        y=remap.get(x,x)
        if y and y not in out and y not in removed: out.append(y)
    return out
L=json.load(open(R/'LIBRARY.json'))
for e in L['entries']:
    if 'skills' in e: e['skills']=fix(e['skills'])
L['updated_at']=now; L.setdefault('merge_log',[]).append({"at":now,"batch":"2026-11-03-compaction","merged":len([m for m in mapping if m[1]]),"removed":len(removed),"new":sorted(new_docs)})
(R/'LIBRARY.json').write_text(json.dumps(L,indent=2,ensure_ascii=False)+"\n")
T=json.load(open(R/'topics/taxonomy.json'))
for c in T['categories']:
    if 'skill_ids' in c: c['skill_ids']=fix(c['skill_ids'])
cat=[c for c in T['categories'] if c['id']=='cinematic-hybrid-synth'][0]
for cid in new_docs:
    if cid not in cat['skill_ids']: cat['skill_ids'].append(cid)
(R/'topics/taxonomy.json').write_text(json.dumps(T,indent=2,ensure_ascii=False)+"\n")
for cp in (R/'curriculums').glob('curriculum-*.json'):
    C=json.load(open(cp))
    for lv in C.get('levels',[]):
        for key in ('skills','skill_ids'):
            if key in lv: lv[key]=fix(lv[key])
    cp.write_text(json.dumps(C,indent=2,ensure_ascii=False)+"\n")
# mapping
lines=["# Archive mapping (2026-11-03 compaction)","","Originals are kept here unchanged. `merged/` = folded into a new skill (old id still resolves via mcp-publish/aliases.json). `removed/` = out of scope for a music-technique library.","","| old id | new id | note |","|---|---|---|"]
lines+=[f"| `{o}` | {('`'+n+'`') if n else '—'} | {r} |" for o,n,r in sorted(mapping,key=lambda m:(m[1] or 'zzz',m[0]))]
(A/'MAPPING.md').write_text("\n".join(lines)+"\n")
from collections import Counter
print("before json",len(docs),"md-only",len(md_only)); print("after json",len(allj)); print("merged",sum(1 for m in mapping if m[1])); print(Counter(removed.values()))
