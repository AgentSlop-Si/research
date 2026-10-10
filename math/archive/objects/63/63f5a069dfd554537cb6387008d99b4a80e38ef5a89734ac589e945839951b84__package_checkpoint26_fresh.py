from pathlib import Path
import json,hashlib,zipfile,tarfile,subprocess,shutil,time
B=Path('[local workspace]');W=B/'master_v26_integration_20261010';D=W/'fft_research_master_20261009';A=D/'additions/0536_final_static_review_closure'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def inv(p):return {str(x.relative_to(p)):{'bytes':x.stat().st_size,'sha256':sha(x)} for x in sorted(p.rglob('*')) if x.is_file()}
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def zip_and_verify(src,out):
 expected=inv(src)
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
  for r in expected:
   info=zipfile.ZipInfo(src.name+'/'+r,date_time=(2026,10,10,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
   with (src/r).open('rb') as f,z.open(info,'w',force_zip64=True) as q:shutil.copyfileobj(f,q,1024*1024)
 with zipfile.ZipFile(out) as z:
  assert len(z.namelist())==len(set(z.namelist()))==len(expected)
  assert set(z.namelist())=={src.name+'/'+r for r in expected}
  for r,v in expected.items():
   h=hashlib.sha256();size=0
   with z.open(src.name+'/'+r) as f:
    for block in iter(lambda:f.read(1048576),b''):size+=len(block);h.update(block)
   assert size==v['bytes'] and h.hexdigest()==v['sha256'],(out,r)
 return {'path':str(out),'bytes':out.stat().st_size,'sha256':sha(out),'files':len(expected),'all_member_paths_sizes_and_hashes_match':True}
assert json.loads((W/'ROOT_FINAL_APPROVAL.json').read_text())['finalize_local_checkpoint26'] is True
expected=json.loads((W/'FINAL_FILE_INVENTORY.json').read_text());assert inv(D)==expected
T=W/'fft_checkpoint26_findings_20261010';assert not T.exists();T.mkdir()
for n in ['INTEGRATED_RESULTS.md','REVIEW_COVERAGE.md','PRACTICAL_FINDINGS.md','UNRESOLVED_REFERENCES.md','PUBLICATION_CANDIDATES.md','CONTENT_VERIFICATION.json']:
 shutil.copy2(A/n,T/n)
(T/'packages').mkdir()
# Compact readings preserve the package-relative report paths while omitting bulky source/evidence trees.
allow={'UNRESOLVED_ITEMS.json','REFERENCE_RECONCILIATION_SUMMARY.json','DEPENDENCY_COVERAGE_SUMMARY.json','ASSESSMENT.md','PRIMARY_SOURCE_LEDGER.md','REVIEW.md','REPORT.md','MAIN_REPORT.md','SOURCE_REVIEWS.md','SOURCE_REVIEWS.json','REVIEWS.json','FINDINGS.json','SEALED_PROOF.md','PRIMARY_SOURCE_COMPARISON.md','DATA_REVIEW.json','COVERAGE_AUDIT.json','MATERIAL_AUDIT.json','FINAL_CONCLUSION.md','REVIEW_CLOSURE.md','CLOSURE_REPORT.md','UNRESOLVED_EVIDENCE.md','UNRESOLVED_REFERENCES.md','FINAL_REPORT.md','REPORT.json','SUMMARY.json','README.md'}
for pack in sorted((A/'packages').iterdir()):
 if not pack.is_dir():continue
 dest=T/'packages'/pack.name;dest.mkdir()
 for p in pack.iterdir():
  if p.is_file() and (p.name in allow or (pack.name in {'pseudoforest_separator_independent_audit_0452','pseudoforest_separator_research_0452','final_review_closure_0535'} and p.suffix=='.md')):shutil.copy2(p,dest/p.name)
 if not any(dest.iterdir()):dest.rmdir()
# Retain the preceding full mathematical synthesis, which gives old accepted statements and scopes.
shutil.copy2(D/'checkpoint_history/checkpoint25_root_before_checkpoint26/CURRENT_CHECKPOINT.md',T/'CHECKPOINT25_MATHEMATICAL_RESULTS.md')
(T/'README.md').write_text('# Fourier research checkpoint 26 reading copy\n\nStart with INTEGRATED_RESULTS.md, then REVIEW_COVERAGE.md, PRACTICAL_FINDINGS.md, UNRESOLVED_REFERENCES.md and PUBLICATION_CANDIDATES.md.\n\nThis compact package includes the integrated summary, preceding mathematical synthesis, principal review reports and the new accepted separator proof. Full source snapshots, per-hash supporting files, historical archives and complete hash manifests are in the complete lossless master archive and the new-review supplement. Links inside preserved reports may refer to that fuller package. Report-local historical counts remain historical; REVIEW_COVERAGE.md gives the final accepted accounting.\n\n1,684 literal full-source reads plus two generated-source semantic/template audits cover all 1,686 frozen program hashes. This is available-material static-review closure, not blanket proof, runtime or novelty certification.\n')
(T/'SHA256SUMS').write_text(''.join(f"{sha(p)}  {p.relative_to(T)}\n" for p in sorted(T.rglob('*')) if p.is_file() and p!=T/'SHA256SUMS'))
findings=zip_and_verify(T,W/'fft_checkpoint26_findings_20261010.zip');print(json.dumps({'compact_ready':findings}),flush=True)
supp=zip_and_verify(A,W/'fft_reviewed_checkpoint26_20261010.zip');print(json.dumps({'supplement_ready':supp}),flush=True)
write(W/'PARTIAL_ARCHIVE_VERIFICATION.json',{'compact':findings,'supplement':supp,'full_master':'compressing; not verified yet'})
out=W/'fft_research_master_checkpoint26_20261010.tar.xz';assert not out.exists();start=time.time()
with out.open('wb') as dest:
 proc=subprocess.Popen(['xz','-T4','-6','-c'],stdin=subprocess.PIPE,stdout=dest)
 try:
  with tarfile.open(fileobj=proc.stdin,mode='w|',format=tarfile.PAX_FORMAT) as tar:
   for r,v in expected.items():
    info=tarfile.TarInfo(D.name+'/'+r);info.size=v['bytes'];info.mode=0o644;info.mtime=0;info.uid=info.gid=0;info.uname=info.gname=''
    with (D/r).open('rb') as f:tar.addfile(info,f)
  proc.stdin.close();rc=proc.wait();assert rc==0,('xz failed',rc)
 except BaseException:
  proc.kill();proc.wait();raise
print(json.dumps({'master_compressed_bytes':out.stat().st_size,'verifying_members':len(expected)}),flush=True)
seen=set()
with tarfile.open(out,'r|xz') as tar:
 for member in tar:
  assert member.isfile();assert member.name.startswith(D.name+'/');r=member.name[len(D.name)+1:];assert r not in seen;seen.add(r);v=expected[r];assert member.size==v['bytes'];h=hashlib.sha256()
  with tar.extractfile(member) as f:
   for block in iter(lambda:f.read(1048576),b''):h.update(block)
  assert h.hexdigest()==v['sha256'],r
assert seen==set(expected)
full={'path':str(out),'bytes':out.stat().st_size,'sha256':sha(out),'files':len(expected),'all_member_paths_sizes_and_hashes_match':True,'compression_and_verification_seconds':round(time.time()-start,3)}
# Final predecessor and source-candidate guard; packaging never modifies the master.
assert inv(D)==expected
base=json.loads((W/'BASELINE_GUARD.json').read_text());assert inv(B/D.name)==base['canonical_files']
verification={'checkpoint':26,'status':'COMPLETE_LOCAL_CHECKPOINT_VERIFIED_PENDING_SAVE','full_master':full,'supplement':supp,'compact_findings':findings,'prior_canonical_checkpoint25_unchanged':True,'staged_master_unchanged_during_packaging':True,'all_original_nonroot_bytes_preserved':True,'all_prior_root_bytes_archived':True,'full_static_reads':1684,'template_audits':2,'complete_static_inspections':1686,'program_static_inspections_open':0,'library_mutated':False,'drive_mutated':False,'canonical_synced':False,'source_programs_executed':False}
write(W/'FINAL_VERIFICATION.json',verification)
# Deliverables remain writable so the authorized save workflow can attach Library identity metadata; hashes remain the content-integrity authority.
print(json.dumps(verification),flush=True)
