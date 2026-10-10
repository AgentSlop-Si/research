"""Reviewer-authored integrity/metadata checker; never executes reviewed source."""
import json, pathlib, hashlib, tarfile
OUT=pathlib.Path('spectral_green_source_review_0336');ROOT=OUT.parent
rows=json.loads((OUT/'ASSIGNED_SOURCE_INDEX.json').read_text());targets={r['sha256'] for r in rows}
dedup=json.loads((OUT/'DEDUPLICATION_CHECK.json').read_text())
def walk(x):
 if isinstance(x,dict):
  if x.get('sha256') in targets:yield x
  for v in x.values():yield from walk(v)
 elif isinstance(x,list):
  for v in x:yield from walk(v)
paths=[ROOT/'post_v22_review_registry_0308/ADDITIVE_CODE_COVERAGE.json']+sorted(ROOT.rglob('COVERAGE.json'))
scanned=[];matches=[]
for p in paths:
 if OUT in p.parents:continue
 b=p.read_bytes();d=json.loads(b);ms=list(walk(d))
 scanned.append({'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'matches':len(ms)})
 for r in ms:matches.append({'evidence_path':str(p),'row':r})
assert not matches, 'Concurrent coverage overlap requires reconciliation before seal'
dedup['scanned_evidence']=scanned;dedup['matches']=matches;dedup['final_recheck_complete']=True
(OUT/'DEDUPLICATION_CHECK.json').write_text(json.dumps(dedup,indent=2)+'\n')
cov=json.loads((OUT/'COVERAGE.json').read_text());assert len(rows)==len(targets)==len(cov['rows'])==24
for a,c in zip(rows,cov['rows']):
 data=(OUT/a['snapshot']).read_bytes();assert hashlib.sha256(data).hexdigest()==a['sha256']==c['sha256'];assert len(data)==a['size_bytes']==c['bytes'];assert len(data.splitlines())==a['lines']==c['lines'];assert c['fully_read_line_intervals']==[[1,a['lines']]]
 assert (OUT/c['review_file']).is_file();assert a['sha256'] in (OUT/c['review_file']).read_text()
 assert not any(c.get(k) for k in ('source_executed','source_executed_in_review','source_imported','source_compiled','source_parsed'))
 for p in (pathlib.Path(a['local_content']),ROOT/'fft_research_master_20261009'/a['representative_path']):assert hashlib.sha256(p.read_bytes()).hexdigest()==a['sha256']
assert sum(c['bytes'] for c in cov['rows'])==75464
assert sum(c['lines'] for c in cov['rows'])==2117
validation={'assigned_hashes':24,'unique_hashes':24,'new_full_read_hashes':24,'prior_duplicate_hashes':0,'completed_evidence_documents_scanned':len(scanned),'exact_snapshot_hashes_verified':24,'source_representatives_reverified':48,'per_source_reviews_verified':24,'source_bytes':75464,'source_lines':2117,'reviewed_source_execution':'none','validation_method':'Reviewer-authored JSON/path/hash/byte-count checks only; no source parsing or execution','global_material_completion':False}
(OUT/'VALIDATION.json').write_text(json.dumps(validation,indent=2)+'\n')
manifest=[]
for p in sorted(OUT.rglob('*')):
 if p.is_file() and p.name not in ('SHA256SUMS.txt','SEAL.json'):
  manifest.append((str(p.relative_to(OUT)),hashlib.sha256(p.read_bytes()).hexdigest()))
(OUT/'SHA256SUMS.txt').write_text(''.join(f'{h}  {name}\n' for name,h in manifest))
seal={'package':'spectral_green_source_review_0336','manifest':'SHA256SUMS.txt','manifest_sha256':hashlib.sha256((OUT/'SHA256SUMS.txt').read_bytes()).hexdigest(),'manifest_file_count':len(manifest),'coverage_sha256':hashlib.sha256((OUT/'COVERAGE.json').read_bytes()).hexdigest(),'report_sha256':hashlib.sha256((OUT/'REPORT.md').read_bytes()).hexdigest(),'all_manifest_entries_verified':True,'full_static_read_hashes':24,'new_coverage_hashes':24,'source_execution':False,'global_completion':False}
(OUT/'SEAL.json').write_text(json.dumps(seal,indent=2)+'\n')
for name,h in manifest:assert hashlib.sha256((OUT/name).read_bytes()).hexdigest()==h
archive=ROOT/'spectral_green_source_review_0336.tar.gz'
with tarfile.open(archive,'w:gz') as t:t.add(OUT,arcname=OUT.name)
print(json.dumps({'seal':seal,'validation':validation,'archive':str(archive),'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest()},indent=2))
