"""Reviewer-authored inert metadata/archive reconciliation. Does not parse or run source code."""
from pathlib import Path
import json,hashlib,zipfile,io
OUT=Path(__file__).parent
ROOT=Path('fft_research_master_20261009')
GRAPH=json.load(open('code_coverage_audit_0228/ARCHIVE_GRAPH.json'))
G={a['sha256']:a for a in GRAPH}
rows=json.load(open(OUT/'ASSIGNED_SOURCES.json'))
cache={}; ev={}; provenance=[]
def read_archive(h):
 if h in cache:return cache[h]
 parts=G[h]['first_observed_at'].split('!'); raw=(ROOT/parts[0]).read_bytes()
 for name in parts[1:]:
  with zipfile.ZipFile(io.BytesIO(raw)) as z:raw=z.read(name)
 assert hashlib.sha256(raw).hexdigest()==h
 cache[h]=raw
 return raw
for r in rows:
 occurrences=[o for o in r['occurrences'] if o.get('archive_sha256') in G]
 o=min(occurrences,key=lambda v: (v['name']!=r['representative_path'],len(G[v['archive_sha256']]['first_observed_at'])))
 h=o['archive_sha256']; a=G[h]
 raw=read_archive(h)
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  info=z.infolist()[o['member_index']];assert info.filename==o['name'];source=z.read(info);assert hashlib.sha256(source).hexdigest()==r['sha256']
  parts=o['name'].split('/');cut=2 if parts[0] in ('fft_relation_research_hardened_20261008','fft_reuse_frontier_20261009') and len(parts)>2 else 1
  prefix='/'.join(parts[:cut])+'/'
  deps=[];es=[]
  for m in a['members']:
   if not m['name'].startswith(prefix):continue
   if m['is_code']:deps.append({'name':m['name'],'sha256':m['sha256']});continue
   if m['is_zip'] or m['size_bytes']>2000000:continue
   if not m['name'].lower().endswith(('.json','.jsonl','.txt','.md','.csv','.log','.gz')):continue
   b=z.read(z.infolist()[m['member_index']]);assert hashlib.sha256(b).hexdigest()==m['sha256']
   eh=m['sha256'];es.append(eh)
   if eh not in ev:
    local='evidence/'+eh+'__'+Path(m['name']).name;(OUT/local).write_bytes(b)
    ev[eh]={'sha256':eh,'size_bytes':len(b),'local':local,'archive_sha256':h,'member':m['name']}
 provenance.append({'index':r['index'],'sha256':r['sha256'],'archive_sha256':h,'archive_first_observed_at':a['first_observed_at'],'member_index':o['member_index'],'member':o['name'],'byte_identity_verified':True,'related_archived_code_metadata_only':deps,'stored_evidence_hashes':es,'origin_class':'origin_unresolved','note':'Archive provenance verified; authorship is not established by a filename, first-person comment, or stored PASS.'})
(OUT/'PROVENANCE.json').write_text(json.dumps(provenance,indent=2));(OUT/'EVIDENCE_INDEX.json').write_text(json.dumps(list(ev.values()),indent=2))
print('Verified archive-member source occurrences',len(provenance),'unique archives',len(cache),'evidence',len(ev),'evidence bytes',sum(x['size_bytes'] for x in ev.values()))
for e in ev.values():
 if e['member'].lower().endswith(('.json','.jsonl','.txt','.log')): print(e['sha256'][:8],e['size_bytes'],e['member'])
