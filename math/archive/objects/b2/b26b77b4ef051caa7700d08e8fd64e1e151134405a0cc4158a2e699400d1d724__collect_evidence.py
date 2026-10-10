"""Reviewer-authored byte/archive metadata checks; no source execution or parsing."""
from pathlib import Path
import json,hashlib,zipfile,io
OUT=Path(__file__).parent;ROOT=Path('fft_research_master_20261009')
G={a['sha256']:a for a in json.load(open('code_coverage_audit_0228/ARCHIVE_GRAPH.json'))}
rows=json.load(open(OUT/'ASSIGNED_SOURCES.json'));cache={};ev={};provenance=[]
def get_archive(h):
 if h in cache:return cache[h]
 parts=G[h]['first_observed_at'].split('!');b=(ROOT/parts[0]).read_bytes()
 for name in parts[1:]:
  with zipfile.ZipFile(io.BytesIO(b)) as z:b=z.read(name)
 assert hashlib.sha256(b).hexdigest()==h;cache[h]=b;return b
for r in rows:
 os=[o for o in r['occurrences'] if o.get('archive_sha256') in G]
 if not os:
  provenance.append({'index':r['index'],'sha256':r['sha256'],'archive_status':'No listed archive occurrence accessible through graph','occurrences':r['occurrences'],'snapshot_verified':True});continue
 o=min(os,key=lambda o:(o['name'].startswith('originals/'),o['name'].count('/'),len(G[o['archive_sha256']]['first_observed_at'])))
 h=o['archive_sha256'];a=G[h];deps=[];es=[]
 with zipfile.ZipFile(io.BytesIO(get_archive(h))) as z:
  m=z.infolist()[o['member_index']];assert m.filename==o['name'];assert hashlib.sha256(z.read(m)).hexdigest()==r['sha256']
  prefix='' if str(Path(o['name']).parent)=='.' else str(Path(o['name']).parent)+'/'
  for m in a['members']:
   if not m['name'].startswith(prefix):continue
   if m['is_code']:deps.append({'name':m['name'],'sha256':m['sha256']});continue
   if m['is_zip'] or m['size_bytes']>2000000 or not m['name'].lower().endswith(('.json','.jsonl','.txt','.md','.csv','.log','.sha256')):continue
   b=z.read(z.infolist()[m['member_index']]);eh=hashlib.sha256(b).hexdigest();assert eh==m['sha256'];es.append(eh)
   if eh not in ev:
    local='evidence/'+eh+'__'+Path(m['name']).name;(OUT/local).write_bytes(b);ev[eh]={'sha256':eh,'size_bytes':len(b),'local':local,'archive_sha256':h,'member':m['name']}
 provenance.append({'index':r['index'],'sha256':r['sha256'],'archive_sha256':h,'archive_first_observed_at':a['first_observed_at'],'member_index':o['member_index'],'member':o['name'],'byte_identity_verified':True,'related_archived_code_metadata_only':deps,'stored_evidence_hashes':es,'origin_class':r['origin_class'],'origin_basis':r['origin_basis'],'note':'Exact bytes and selected archived occurrence verified; authorship and stored execution claims remain separate.'})
(OUT/'PROVENANCE.json').write_text(json.dumps(provenance,indent=2));(OUT/'EVIDENCE_INDEX.json').write_text(json.dumps(list(ev.values()),indent=2))
print('provenance',len(provenance),'archive identities',len(cache),'evidence',len(ev),'bytes',sum(x['size_bytes'] for x in ev.values()))
