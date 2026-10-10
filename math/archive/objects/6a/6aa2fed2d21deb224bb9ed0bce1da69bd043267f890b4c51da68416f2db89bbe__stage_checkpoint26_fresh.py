from pathlib import Path
import json, hashlib, shutil, datetime
B=Path('[local workspace]'); W=B/'master_v26_integration_20261010'; S=B/'fft_research_master_20261009'; D=W/S.name
A=D/'additions/0536_final_static_review_closure'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def inventory(p):return {str(x.relative_to(p)):{'bytes':x.stat().st_size,'sha256':sha(x)} for x in sorted(p.rglob('*')) if x.is_file()}
g=json.loads((B/'master_v25_integration_20261010/CANONICAL_SYNC_GUARD.json').read_text()); before=inventory(S)
assert before==g['candidate_files'], 'Canonical checkpoint25 does not match verified candidate guard'
assert len(before)==16665
assert not D.exists(),'Refusing to overwrite existing staging directory'
shutil.copytree(S,D,copy_function=shutil.copy2)
assert inventory(D)==before
roots={r:v for r,v in before.items() if '/' not in r}
H=D/'checkpoint_history/checkpoint25_root_before_checkpoint26'; H.mkdir()
for r in roots:shutil.copy2(S/r,H/r)
A.mkdir(parents=True)
(A/'preservation').mkdir(); (A/'packages').mkdir(); (A/'registry_snapshots').mkdir()
for n in ['CANONICAL_SYNC_RECEIPT.json','CANONICAL_SYNC_GUARD.json','LIBRARY_SAVE_RECEIPT.json','SOLID_ARCHIVE_VERIFICATION.json','FINAL_VERIFICATION.json']:
 shutil.copy2(B/'master_v25_integration_20261010'/n,A/'preservation'/n)
(W/'BASELINE_GUARD.json').write_text(json.dumps({'checkpoint':25,'canonical_files':before,'root_files':roots,'canonical_sync_receipt_sha256':sha(B/'master_v25_integration_20261010/CANONICAL_SYNC_RECEIPT.json'),'archive_root_snapshots':str(H.relative_to(D))},indent=2)+'\n')
(W/'STAGING_STATUS.json').write_text(json.dumps({'status':'BASELINE_COPIED_PENDING_ACCEPTED_PACKAGE_STAGING_AND_FINAL_ROOT_PIN','baseline_files':len(before),'archived_prior_root_files':len(roots),'original_copy_verified':True,'checkpoint25_guard_verified':True,'canonical_modified':False,'uploads':False,'source_programs_executed':False,'addition':str(A.relative_to(D)),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2)+'\n')
print(json.dumps({'baseline_files':len(before),'root_files_archived':len(roots),'addition':str(A),'canonical_byte_match':True}))
