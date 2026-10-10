"""Fresh byte/manifest/coverage metadata verification only; no supplied code execution or parsing."""
from pathlib import Path, PurePosixPath
import json,hashlib,zipfile
O=Path(__file__).parent;M=Path('fft_research_master_20261009'); H=lambda b:hashlib.sha256(b).hexdigest()
rows=json.loads((O/'ASSIGNED_ROWS.json').read_text()); targets={r['sha256'] for r in rows};checks=[]
archives=['additions/1916/original_source.zip','additions/1930_phase26/source_archives/fft_green_research_phase26_2026-10-10.zip','additions/1954/originals/fft_divisor_spectrum_v13(1).zip','additions/2020_2027/hero1_phase14/original/fft_hero1_phase14_20261010.zip']
for rel in archives:
 p=M/rel; data=p.read_bytes();ar={'archive_path':str(p),'sha256':H(data),'bytes':len(data),'manifests':[],'source_targets':[]}
 with zipfile.ZipFile(p) as z:
  members=z.namelist()
  for name in members:
   if name.endswith(('MANIFEST.sha256','SHA256SUMS.txt')):
    manifest=z.read(name); records=[]
    for line in manifest.decode().splitlines():
     parts=line.split(maxsplit=1)
     if len(parts)!=2 or len(parts[0])!=64:continue
     expected, filename=parts; filename=filename.lstrip('*');member=str(PurePosixPath(name).parent/filename)
     if member not in members:records.append({'member':member,'expected':expected,'present':False});continue
     b=z.read(member);records.append({'member':member,'expected':expected,'actual':H(b),'bytes':len(b),'matches':H(b)==expected})
    ar['manifests'].append({'member':name,'sha256':H(manifest),'records':records})
  for name in members:
   if name.endswith('.py'):
    b=z.read(name);h=H(b)
    if h in targets:ar['source_targets'].append({'member':name,'sha256':h,'bytes':len(b),'matches_assigned_snapshot':True})
 checks.append(ar)
sparse=json.loads((M/'additions/1930_sparse/INDEPENDENT_CHECKS.json').read_text())
(O/'MANIFEST_CHECKS.json').write_text(json.dumps({'archives':checks,'sparse_result_checker_sha256':sparse['check_script_sha256'],'sparse_checker_identity_matches':sparse['check_script_sha256']==rows[11]['sha256'],'scope':'Fresh hashing and manifest metadata checks. ZIP members treated as bytes; Python source never parsed/imported/executed. Archive integrity is not mathematical correctness.'},indent=2)+'\n')
# Recheck originals after all source reads.
receipt=json.loads((O/'PRESERVATION_RECEIPT.json').read_text())
for r in receipt['sources']:
 for key in ['original_path','representative_master_path']:
  p=Path(r[key]);assert H(p.read_bytes())==r['sha256_before']
for r in rows:assert H((O/r['snapshot']).read_bytes())==r['sha256']
changes=[]
for m in receipt['metadata_inputs']:
 p=Path(m['path']);current=H(p.read_bytes());m['sha256_at_final_check']=current
 if current!=m['sha256']:
  changes.append({'path':str(p),'initial_sha256':m['sha256'],'final_sha256':current,'disposition':'Concurrent authorized parent update; initial exact snapshot retained. This worker did not edit the file.'})
receipt['concurrent_authorized_metadata_drift']=changes
receipt['final_original_source_identity_check']=True
receipt['central_registry_modified_by_this_worker']=False
receipt['all_originals_unchanged_scope']='33 assigned source hashes and representatives; mutable metadata drift is listed separately.'
(O/'PRESERVATION_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
# Final dedup includes concurrent completed work.
prior=[]
for p in sorted(Path('[local workspace]').rglob('COVERAGE.json')):
 if O in p.parents:continue
 b=p.read_bytes();hits=sorted(h for h in targets if h in b.decode())
 prior.append({'path':str(p),'sha256':H(b),'assigned_hash_matches':hits})
reg=Path('post_v22_review_registry_0308/ADDITIVE_CODE_COVERAGE.json'); rb=reg.read_bytes();rhits=sorted(h for h in targets if h in rb.decode())
assert not rhits and not any(p['assigned_hash_matches'] for p in prior)
(O/'FINAL_DEDUP_RECHECK.json').write_text(json.dumps({'coverage_files':prior,'coverage_count':len(prior),'registry_path':str(reg),'registry_sha256':H(rb),'registry_assigned_hash_matches':rhits,'new_unique_hashes':33,'result':'No assigned exact hash already covered; 33 new credits remain valid.'},indent=2)+'\n')
# Ensure review completeness and identities.
cov=json.loads((O/'COVERAGE.json').read_text());assert len(cov['rows'])==33
for r in cov['rows']:
 assert H((O/r['snapshot']).read_bytes())==r['sha256'];assert (O/r['review_file']).is_file();assert r['fully_read_line_intervals']==[[1,r['lines']]]
summary={'assigned_sources':33,'new_coverage_credit':33,'bytes':246583,'lines':6174,'all_assigned_complete':True,'source_execution':'none','no_source_parse':True,'prior_COVERAGE_files_final':len(prior),'metadata_drift_count':len(changes),'stored_evidence_files':len(json.loads((O/'EVIDENCE_IDENTITIES.json').read_text())['rows']),'archive_manifests_checked':sum(len(a['manifests']) for a in checks),'archive_manifest_entries':sum(len(m['records']) for a in checks for m in a['manifests']),'archive_manifest_entry_failures':sum(not e.get('matches',False) for a in checks for m in a['manifests'] for e in m['records']),'all_material_review_complete':False,'dependency_closure_complete':False}
(O/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
items=[]
for p in sorted(O.rglob('*')):
 if p.is_file() and p.name not in ['SHA256SUMS.txt','SEAL.json']:
  b=p.read_bytes();items.append((H(b),str(p.relative_to(O)),len(b)))
sums=''.join(h+'  '+p+'\n' for h,p,n in items);(O/'SHA256SUMS.txt').write_text(sums)
seal={'status':'sealed complete assigned static review','package':'phase26_sparse_source_review_0406','sealed_file_count':len(items),'sealed_file_bytes':sum(n for h,p,n in items),'sha256sums_sha256':H(sums.encode()),'coverage_sha256':H((O/'COVERAGE.json').read_bytes()),'preservation_receipt_sha256':H((O/'PRESERVATION_RECEIPT.json').read_bytes()),'new_coverage_credit':33,'source_execution':'none','source_parsing':'none','all_assigned_complete':True,'global_material_complete':False,'excluded_from_checksum_list':['SHA256SUMS.txt','SEAL.json']}
(O/'SEAL.json').write_text(json.dumps(seal,indent=2)+'\n')
for h,p,n in items:assert H((O/p).read_bytes())==h
print(json.dumps(summary,indent=2));print('SEAL_SHA256',H((O/'SEAL.json').read_bytes()));print('COVERAGE_SHA256',seal['coverage_sha256']);print('SHA256SUMS_SHA256',seal['sha256sums_sha256'])
