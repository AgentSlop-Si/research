"""Fresh reviewer metadata collector; never executes/imports/parses source."""
from pathlib import Path
import json,hashlib
O=Path(__file__).parent;R=Path('fft_research_master_20261009')
rows=json.load(open(O/'ASSIGNED_SOURCES.json'));prov=json.load(open(O/'PROVENANCE.json'));ev={e['sha256']:e for e in json.load(open(O/'EVIDENCE_INDEX.json'))};checks=[]
for r in rows:
 contexts=[]
 for occ in r['occurrences']:
  if occ['kind']=='archive_member':continue
  pp=Path(occ['path']); pp=R/pp if occ['kind']=='master_standalone' else pp
  if not pp.is_file():checks.append({'index':r['index'],'path':str(pp),'status':'local occurrence unavailable'});continue
  b=pp.read_bytes();ok=hashlib.sha256(b).hexdigest()==r['sha256'];assert ok
  checks.append({'index':r['index'],'path':str(pp),'status':'exact identity verified','size':len(b)})
  if occ['kind']!='master_standalone':continue
  ehs=[];deps=[]
  for f in pp.parent.rglob('*'):
   if not f.is_file():continue
   if f.suffix in ('.py','.cpp','.cc','.h','.hpp','.sh'):
    deps.append({'path':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()});continue
   if f.suffix not in ('.json','.jsonl','.txt','.md','.csv','.log','.sha256') or f.stat().st_size>2000000:continue
   b=f.read_bytes();h=hashlib.sha256(b).hexdigest();ehs.append(h)
   if h not in ev:
    loc='evidence/'+h+'__'+f.name;(O/loc).write_bytes(b);ev[h]={'sha256':h,'size_bytes':len(b),'local':loc,'standalone_path':str(f),'member':str(f.relative_to(R))}
  contexts.append({'source_path':str(pp),'byte_identity_verified':True,'related_code_metadata_only':deps,'stored_evidence_hashes':ehs})
 prov[r['index']]['verified_standalone_contexts']=contexts
(O/'PROVENANCE.json').write_text(json.dumps(prov,indent=2));(O/'EVIDENCE_INDEX.json').write_text(json.dumps(list(ev.values()),indent=2));(O/'STANDALONE_IDENTITY_CHECKS.json').write_text(json.dumps(checks,indent=2))
print('standalone checks',len(checks),'all match',all(x['status']=='exact identity verified' for x in checks),'evidence',len(ev),'bytes',sum(x['size_bytes'] for x in ev.values()))
print('\n'.join(f'{i:03} {e["size_bytes"]:8} {e["sha256"][:8]} {e["member"]}' for i,e in enumerate(ev.values())))
