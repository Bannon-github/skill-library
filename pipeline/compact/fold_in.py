"""Fold a newly distilled music skill into an existing cluster skill as a variant (keeps library compact).
Usage: python3 pipeline/compact/fold_in.py distilled/<vid>/agent-skill-<id>.json <cluster-id>
Archives nothing; adds variant + source + alias, and rewrites the cluster's skills/<cluster>.md section."""
import json, sys
from pathlib import Path
R=Path('/workspace/skill-library'); new=json.load(open(sys.argv[1])); cid=sys.argv[2]
p=R/'mcp-publish/skills'/f'{cid}.json'; d=json.load(open(p))
if new['id'] not in d['merged_from']:
    s=new.get('source',{})
    d['source'].setdefault('sources',[]).append({"from_skill":new['id'],"video_id":s.get('video_id'),"url":s.get('url'),"title":s.get('title')})
    d['variants'].append({"from_skill":new['id'],"name":new['name'],"goal":new['goal'],"steps":[x['action'] for x in new['steps']]})
    d['merged_from'].append(new['id']); d['aliases'].append(new['id'])
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+"\n")
A=json.load(open(R/'mcp-publish/aliases.json')); A['aliases'][new['id']]=cid
(R/'mcp-publish/aliases.json').write_text(json.dumps(A,indent=2)+"\n")
md=R/'skills'/f'{cid}.md'
md.write_text(md.read_text()+f"\n### {new['name']}\nSource: [{new['source'].get('title')}]({new['source'].get('url')}) · was `{new['id']}`\n"+"".join(f"- {x['action']}\n" for x in new['steps']))
print('folded',new['id'],'->',cid)
