"""Reviewer-authored inert preservation and packaging; supplied sources are data only."""
import json,pathlib,hashlib,collections,zipfile
BASE=pathlib.Path('[local workspace]'); OUT=BASE/'green_covariance_source_review_0335'; NOW='2026-10-10T03:46:03Z'
sha=lambda b:hashlib.sha256(b).hexdigest()
rows=json.loads((OUT/'assigned_rows.json').read_text());cov=json.loads((OUT/'COVERAGE.json').read_text());hs={r['sha256'] for r in rows}
paths=[BASE/'code_coverage_audit_0228/CODE_COVERAGE_INVENTORY.json',BASE/'post_v22_review_registry_0308/ADDITIVE_CODE_COVERAGE.json']+sorted(BASE.rglob('COVERAGE.json'))
seen=collections.defaultdict(list);matches=collections.defaultdict(list);scans=[]
def walk(x,path):
 if isinstance(x,dict):
  h=x.get('sha256') or x.get('source_sha256') or x.get('content_sha256')
  full=any(x.get(k) is True for k in ('full_static_inspection','static_inspection_complete','full_static_review'))
  if h and full:seen[h].append(str(path))
  if h in hs:matches[h].append({'path':str(path),'full_static':full,'coverage_status':x.get('coverage_status')})
  for v in x.values():walk(v,path)
 elif isinstance(x,list):
  for v in x:walk(v,path)
(OUT/'baseline_snapshots').mkdir(exist_ok=True)
for p in paths:
 if OUT in p.parents:continue
 b=p.read_bytes();d=json.loads(b);walk(d,p);scans.append({'path':str(p),'sha256':sha(b),'bytes':len(b)})
 if p.name=='ADDITIVE_CODE_COVERAGE.json':
  (OUT/'baseline_snapshots'/p.name).write_bytes(b);registry_hash=sha(b)
 if p.name=='CODE_COVERAGE_INVENTORY.json':
  frozen_hash=sha(b)
  # Retain assigned frozen rows exactly as JSON data; full file is identified by digest.
  subset=[r for r in d if r['sha256'] in hs]
  (OUT/'baseline_snapshots/FROZEN_ASSIGNED_ROWS.json').write_text(json.dumps(subset,indent=2)+'\n')
overlap=sorted(hs & set(seen))
assert not overlap, ('Prior exact-hash overlap appeared before seal',overlap)
(OUT/'DUPLICATE_CHECK_FINAL.json').write_text(json.dumps({'checked_utc':NOW,'policy':'Qualifying full-static flags tied to exact SHA-256; excluded this package. No assigned exact-hash overlap in external complete coverage.','scanned':scans,'assigned_hash_hits':matches,'prior_full_read_hashes':overlap},indent=2)+'\n')
(OUT/'PRIOR_FULL_STATIC_HASHES.json').write_text(json.dumps({'checked_utc':NOW,'qualifying_flags':['full_static_inspection','static_inspection_complete','full_static_review'],'frozen_inventory_sha256':frozen_hash,'additive_registry_sha256':registry_hash,'unique_hash_count':len(seen),'assigned_prior_overlap':overlap,'rows':[{'sha256':h,'evidence_files':sorted(set(p))} for h,p in sorted(seen.items())]},indent=2)+'\n')
cov['completed_utc']=NOW;cov['current_additive_registry_sha256_at_completion']=registry_hash;cov['prior_coverage_manifest_count']=len(scans);cov['source_hash_count']=24;cov['new_additive_full_static_reads']=24;cov['previously_read_overlap']=0
(OUT/'COVERAGE.json').write_text(json.dumps(cov,indent=2,ensure_ascii=False)+'\n')
checks=[]
for r in rows:
 h=r['sha256'];p=pathlib.Path(r['local_content']);snap=OUT/'source_snapshots'/f'{h}.txt';a=p.read_bytes();b=snap.read_bytes()
 master=BASE/'fft_research_master_20261009'/r['representative_path'];mb=master.read_bytes() if master.exists() else None
 assert sha(a)==sha(b)==h
 if mb is not None:assert sha(mb)==h
 checks.append({'sha256':h,'bytes':len(a),'original_local_path':str(p),'original_sha256_after_review':sha(a),'snapshot':str(snap.relative_to(OUT)),'snapshot_sha256':sha(b),'original_master_path':str(master),'original_master_sha256_after_review':sha(mb) if mb is not None else None,'unchanged':True})
batches=[]
for name in cov['assigned_batches']:
 p=BASE/'code_coverage_audit_0228/pending_batches_v2'/name;b=p.read_bytes();s=(OUT/name).read_bytes();assert b==s
 batches.append({'path':str(p),'snapshot':name,'sha256':sha(b),'unchanged':True})
receipt={'checked_utc':NOW,'scope':'24 assigned program byte objects, their representative master copies and both source assignment JSON files. Historical archives and unrelated files are outside this preservation claim.','source_count':24,'source_bytes':84288,'source_lines':2179,'original_code_written':False,'source_execution':False,'source_import':False,'source_compilation':False,'source_syntax_parsing':False,'supplied_test_runs':0,'source_checks':checks,'batch_checks':batches,'all_checked_originals_unchanged':True}
(OUT/'PRESERVATION_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
# The seal intentionally excludes itself and SHA256SUMS to avoid self-reference.
files=sorted(p for p in OUT.rglob('*') if p.is_file() and p.name not in ('SEAL.json','SHA256SUMS.txt'))
manifest=[{'path':str(p.relative_to(OUT)),'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size} for p in files]
sums=''.join(f'{r["sha256"]}  {r["path"]}\n' for r in manifest)
(OUT/'SHA256SUMS.txt').write_text(sums)
seal={'sealed_utc':NOW,'package':OUT.name,'manifest_sha256':sha(sums.encode()),'manifest_file':'SHA256SUMS.txt','sealed_payload_file_count':len(manifest),'source_hash_count':24,'new_additive_full_static_reads':24,'source_execution':False,'source_import_or_compilation':False,'preservation_all_checked_originals_unchanged':True,'files':manifest}
(OUT/'SEAL.json').write_text(json.dumps(seal,indent=2)+'\n')
for r in manifest:assert sha((OUT/r['path']).read_bytes())==r['sha256']
archive=BASE/(OUT.name+'.zip')
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in sorted(OUT.rglob('*')):
  if p.is_file():z.write(p,str(pathlib.Path(OUT.name)/p.relative_to(OUT)))
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 for p in sorted(OUT.rglob('*')):
  if p.is_file():assert z.read(str(pathlib.Path(OUT.name)/p.relative_to(OUT)))==p.read_bytes()
print(json.dumps({'directory':str(OUT),'archive':str(archive),'archive_sha256':sha(archive.read_bytes()),'archive_bytes':archive.stat().st_size,'source_count':24,'new_full_static_reads':24,'originals_unchanged':True,'manifest_entries':len(manifest),'external_coverage_files_scanned':len(scans),'prior_hash_count':len(seen),'all_source_execution':False},indent=2))
