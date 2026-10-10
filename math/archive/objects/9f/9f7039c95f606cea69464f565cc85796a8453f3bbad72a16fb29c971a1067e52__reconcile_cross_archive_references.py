"""Reviewer inert cross-archive reference lookup and byte hashing only."""
from pathlib import Path
import json,hashlib,zipfile,io,collections
O=Path(__file__).parent;ROOT=Path('fft_research_master_20261009');G={a['sha256']:a for a in json.load(open('code_coverage_audit_0228/ARCHIVE_GRAPH.json'))};ix=collections.defaultdict(list);cache={}
for h,a in G.items():
 for m in a['members']:ix[m['sha256']].append((h,m))
def archive(h):
 if h not in cache:
  pieces=G[h]['first_observed_at'].split('!');b=(ROOT/pieces[0]).read_bytes()
  for n in pieces[1:]:
   with zipfile.ZipFile(io.BytesIO(b)) as z:b=z.read(n)
  assert hashlib.sha256(b).hexdigest()==h;cache[h]=b
 return cache[h]
out=[]
for f in ['STORED_MANIFEST_RECONCILIATION.json','STORED_HASH_REFERENCE_RECONCILIATION.json']:
 for r in json.load(open(O/f)):
  if r['status']!='unresolved_in_same_archive':continue
  sha=r.get('expected_sha256',r.get('sha256'));hits=ix[sha];verified=None
  if hits:
   h,m=min(hits,key=lambda hm:len(G[hm[0]]['first_observed_at']))
   with zipfile.ZipFile(io.BytesIO(archive(h))) as z:b=z.read(z.infolist()[m['member_index']])
   assert hashlib.sha256(b).hexdigest()==sha;verified={'archive_sha256':h,'member':m['name'],'archive_first_observed_at':G[h]['first_observed_at'],'bytes_rehashed':True}
  elif sha in G:
   b=archive(sha);verified={'archive_sha256':sha,'archive_first_observed_at':G[sha]['first_observed_at'],'archive_bytes_rehashed':True}
  out.append({'source_reconciliation':f,'reference':r,'global_exact_hash_occurrences':len(hits),'verified_external_occurrence':verified,'status':'found_and_rehashed_elsewhere' if verified else 'unresolved_in_archive_graph','note':'Cross-archive identity does not establish runtime import resolution, execution or original authorship.'})
(O/'CROSS_ARCHIVE_REFERENCE_RECONCILIATION.json').write_text(json.dumps(out,indent=2));print(collections.Counter(r['status'] for r in out))
print('Unresolved:',[(r['reference'].get('manifest',r['reference'].get('result')),r['reference'].get('target_reference',r['reference'].get('label'))) for r in out if not r['verified_external_occurrence']])
