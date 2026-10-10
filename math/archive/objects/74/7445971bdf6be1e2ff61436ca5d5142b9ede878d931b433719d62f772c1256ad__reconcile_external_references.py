"""Fresh inert hash reconciliation of external manifest references; no source evaluation."""
import json,hashlib,zipfile,io
from pathlib import Path
O=Path(__file__).parent;G={a['sha256']:a for a in json.load(open('code_coverage_audit_0228/ARCHIVE_GRAPH.json'))};E=json.load(open(O/'EVIDENCE_INDEX.json'));e=next(e for e in E if e['member']=='macro/exact/source_manifest.json');d=json.loads((O/e['local']).read_text());cache={};records=[]
for name,want in d['files'].items():
 candidates=[(h,m)for h,a in G.items()for m in a['members']if m['sha256']==want and (m['name']==name or m['name'].endswith('/'+name))]
 if not candidates:
  records.append({'name':name,'expected_sha256':want,'status':'no_exact_name_and_hash_inventory_candidate'});continue
 h,m=min(candidates,key=lambda hm:len(G[hm[0]]['first_observed_at']))
 if h not in cache:
  parts=G[h]['first_observed_at'].split('!');b=(Path('fft_research_master_20261009')/parts[0]).read_bytes()
  for part in parts[1:]:
   with zipfile.ZipFile(io.BytesIO(b))as z:b=z.read(part)
  assert hashlib.sha256(b).hexdigest()==h;cache[h]=b
 with zipfile.ZipFile(io.BytesIO(cache[h]))as z:
  info=z.infolist()[m['member_index']];assert info.filename==m['name'];b=z.read(info)
 got=hashlib.sha256(b).hexdigest();records.append({'name':name,'expected_sha256':want,'observed_sha256':got,'status':'exact_external_archive_byte_match'if got==want else'mismatch','archive_sha256':h,'archive_first_observed_at':G[h]['first_observed_at'],'member':m['name'],'member_index':m['member_index'],'bytes':len(b),'full_source_read_credit':False})
(O/'STORED_HASH_REFERENCE_RECONCILIATION.json').write_text(json.dumps({'manifest_sha256':e['sha256'],'manifest_member':e['member'],'records':records,'scope':'External referenced bytes reconciled in separate original archives. These reads are metadata/provenance-only and earn no additional source coverage or mathematical certification.'},indent=2)+'\n')
print('external records',len(records),'matched',sum(r['status']=='exact_external_archive_byte_match'for r in records))
