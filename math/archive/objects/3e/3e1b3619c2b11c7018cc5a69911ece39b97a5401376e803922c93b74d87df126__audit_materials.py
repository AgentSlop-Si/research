#!/usr/bin/env python3
"""Fresh read-only exact byte checks of the frozen material identities and archive graph."""
import json,pathlib,hashlib,io,zipfile,collections
P=pathlib.Path('[local workspace]');O=P/'final_review_closure_0535';M=P/'fft_research_master_20261009';H=lambda b:hashlib.sha256(b).hexdigest()
def dump(n,x):(O/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def load_original(s):
 parts=s.split('!');f=pathlib.Path(parts[0]);f=f if f.is_absolute() else M/f;b=f.read_bytes()
 for member in parts[1:]:
  with zipfile.ZipFile(io.BytesIO(b)) as z:b=z.read(member)
 return b
rows=json.loads((P/'coverage_audit_20261010/CONSOLIDATED_SOURCE_VERSION_INDEX.json').read_text());out=[]
for r in rows:
 f=pathlib.Path(r['local_source']) if r.get('local_source') else None;present=f and f.exists();actual=H(f.read_bytes()) if present else None
 out.append({'library_file_id':r['library_file_id'],'name':r['name'],'observed_file_id':r['observed_file_id'],'observed_version':r['observed_version'],'expected_sha256':r['sha256'],'expected_size':r['size_bytes'],'preservation_status':r['preservation_status'],'actual_sha256':actual,'byte_snapshot_matches':bool(present and actual==r['sha256'] and f.stat().st_size==r['size_bytes']),'local_source':r['local_source']})
dump('MATERIAL_IDENTITY_CHECKS.json',out)
graph=json.loads((P/'code_coverage_audit_0228/ARCHIVE_GRAPH.json').read_text());ars=[];occ=[]
for r in graph:
 a={'archive_sha256':r['sha256'],'origin':r['first_observed_at'],'members':len(r['members'])}
 try:
  b=load_original(r['first_observed_at']);a['actual_sha256']=H(b);a['archive_hash_matches']=H(b)==r['sha256'];a['size_matches']=len(b)==r['size_bytes']
  with zipfile.ZipFile(io.BytesIO(b)) as z:
   for m in r['members']:
    info=z.infolist()[m['member_index']];data=z.read(info);got=H(data)
    occ.append({'archive_sha256':r['sha256'],'member_index':m['member_index'],'member':m['name'],'expected_sha256':m['sha256'],'actual_sha256':got,'name_matches':info.filename==m['name'],'size_matches':len(data)==m['size_bytes'],'hash_matches':got==m['sha256'],'is_code':m['is_code']})
  a['member_checks_complete']=True
 except Exception as e:a['error']=repr(e)
 ars.append(a)
dump('ARCHIVE_CONTAINER_CHECKS.json',ars);dump('ARCHIVE_MEMBER_CHECKS.json',occ)
summary={'material_identities':len(rows),'identity_unique_library_ids':len({r['library_file_id'] for r in rows}),'byte_originals_verified':sum(x['byte_snapshot_matches'] and x['preservation_status']=='original bytes matched by identity, size and saved version' for x in out),'matching_version_text_snapshots_verified':sum(x['byte_snapshot_matches'] and x['preservation_status']=='complete current-version text snapshot; original download unavailable' for x in out),'unavailable_frozen_versions':sum(x['preservation_status']=='current original version not byte-verified' for x in out),'material_mismatch_rows':[x for x in out if x['expected_sha256'] and not x['byte_snapshot_matches']],'archive_containers':len(ars),'archive_container_errors':[x for x in ars if not x.get('archive_hash_matches') or not x.get('size_matches') or not x.get('member_checks_complete')],'archive_member_occurrences_checked':len(occ),'archive_member_errors':[x for x in occ if not x['name_matches'] or not x['size_matches'] or not x['hash_matches']],'boundary':'Frozen accessible material identities and graph only. Original-byte availability, text-snapshot availability, semantic review, mathematical correctness and runtime closure are distinct.'}
dump('MATERIAL_AUDIT.json',summary);print(json.dumps(summary,indent=2))
