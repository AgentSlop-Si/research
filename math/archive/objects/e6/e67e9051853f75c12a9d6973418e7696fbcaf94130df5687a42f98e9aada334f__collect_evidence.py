"""Fresh reviewer metadata tooling: inert archive/byte reads only. No supplied source execution, imports, compilation or AST parsing."""
from pathlib import Path
import json,hashlib,zipfile,io
OUT=Path(__file__).parent; ROOT=Path('fft_research_master_20261009')
G={a['sha256']:a for a in json.load(open('code_coverage_audit_0228/ARCHIVE_GRAPH.json'))}
rows=json.load(open(OUT/'ASSIGNED_SOURCES.json'));cache={};ev={};provenance=[]
def read_archive(h):
 if h in cache:return cache[h]
 parts=G[h]['first_observed_at'].split('!');raw=(ROOT/parts[0]).read_bytes();chain=[]
 chain.append({'path':parts[0],'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)})
 for name in parts[1:]:
  with zipfile.ZipFile(io.BytesIO(raw)) as z:raw=z.read(name)
  chain.append({'member':name,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)})
 assert hashlib.sha256(raw).hexdigest()==h
 cache[h]=(raw,chain);return cache[h]
selected={17:'b9ad3',23:'2991',24:'4c013'}
for r in rows:
 occurrences=[]
 for o in r['occurrences']:
  v=dict(o)
  if o['kind']=='archive_member':
   h=o['archive_sha256'];raw,chain=read_archive(h)
   with zipfile.ZipFile(io.BytesIO(raw)) as z:
    info=z.infolist()[o['member_index']];assert info.filename==o['name'];b=z.read(info)
   v.update(archive_first_observed_at=G[h]['first_observed_at'],archive_chain=chain,byte_identity_verified=hashlib.sha256(b).hexdigest()==r['sha256'] and len(b)==r['size_bytes'])
  else:
   p=Path(o['path']);v['local_path_exists']=p.exists()
   v['byte_identity_verified']=p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']
  assert v['byte_identity_verified'];occurrences.append(v)
 oo=[o for o in occurrences if o['kind']=='archive_member']
 if r['index'] in selected:o=next(o for o in oo if o['archive_sha256'].startswith(selected[r['index']]))
 else:o=min(oo,key=lambda o:(o['name']!=r['representative_path'],len(o['archive_first_observed_at'])))
 h=o['archive_sha256'];a=G[h];raw,_=read_archive(h)
 prefix='fft130_adaptive_merge/' if r['index']==23 else ('fft_wide_scan_cutrank/' if r['index']==24 else '')
 es=[];deps=[]
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  for m in a['members']:
   if not m['name'].startswith(prefix):continue
   if m['is_code']:deps.append({'name':m['name'],'sha256':m['sha256'],'bytes':m['size_bytes']});continue
   if m['is_zip'] or not m['name'].lower().endswith(('.json','.jsonl','.txt','.md','.csv','.log','.gz','.tex')):continue
   b=z.read(z.infolist()[m['member_index']]);assert hashlib.sha256(b).hexdigest()==m['sha256'];eh=m['sha256'];es.append(eh)
   occurrence={'archive_sha256':h,'member':m['name'],'member_index':m['member_index']}
   if eh not in ev:
    local='evidence/'+eh+'__'+Path(m['name']).name;(OUT/local).write_bytes(b)
    ev[eh]={'sha256':eh,'size_bytes':len(b),'local':local,'archive_sha256':h,'member':m['name'],'occurrences':[occurrence]}
   elif occurrence not in ev[eh]['occurrences']:ev[eh]['occurrences'].append(occurrence)
 provenance.append({'index':r['index'],'sha256':r['sha256'],'archive_sha256':h,'archive_first_observed_at':a['first_observed_at'],'member_index':o['member_index'],'member':o['name'],'byte_identity_verified':True,'all_recorded_occurrences':occurrences,'related_archived_code_metadata_only':deps,'stored_evidence_hashes':es,'origin_class':r['origin_class'],'note':'Exact bytes independently matched across every recorded occurrence. Authorship and execution history remain unestablished; comments are source claims, not current-review actions.'})
(OUT/'PROVENANCE.json').write_text(json.dumps(provenance,indent=2)+'\n');(OUT/'EVIDENCE_INDEX.json').write_text(json.dumps(list(ev.values()),indent=2)+'\n')
(OUT/'RELATED_ARCHIVE_METADATA.json').write_text(json.dumps([G[h] for h in cache],indent=2)+'\n')
print('Sources',len(provenance),'occurrences',sum(len(p['all_recorded_occurrences'])for p in provenance),'archives',len(cache),'evidence',len(ev),'evidence bytes',sum(e['size_bytes']for e in ev.values()))
