"""Reviewer-authored metadata-only packaging. Never imports, parses or runs supplied programs."""
import pathlib,json,hashlib,datetime,collections
R=pathlib.Path(__file__).parent
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def digest(b):return hashlib.sha256(b).hexdigest()
def readj(p):return json.loads(pathlib.Path(p).read_text())
def write(name,obj):(R/name).write_text(json.dumps(obj,indent=2)+'\n')
rows=readj(R/'ASSIGNED_SOURCES.json');reports=readj(R/'SOURCE_REPORTS.json');base=readj(R/'BASELINE_METADATA.json');oldcov=readj(R/'RECURSIVE_COVERAGE_BASELINE.json');H={r['sha256'] for r in rows}
assert len(rows)==len(H)==len(reports)==46
prior=collections.defaultdict(list)
def exact_full_claims(obj):
 if isinstance(obj,dict):
  h=obj.get('sha256',obj.get('source_sha256'))
  if h in H and (obj.get('full_static_inspection') is True or obj.get('static_inspection_complete') is True):yield h
  for x in obj.values():yield from exact_full_claims(x)
 elif isinstance(obj,list):
  for x in obj:yield from exact_full_claims(x)
paths=[pathlib.Path('code_coverage_audit_0228/CODE_COVERAGE_INVENTORY.json'),pathlib.Path('post_v22_review_registry_0308/ADDITIVE_CODE_COVERAGE.json')]
paths+=sorted(p for p in pathlib.Path('[local workspace]').rglob('COVERAGE.json') if R not in p.parents)
paths=list(dict.fromkeys(paths));observations=[];rawmentions=[]
for p in paths:
 b=p.read_bytes();h=digest(b);snap=R/'evidence_snapshots'/f'completion_dedup__{h}.json'
 if not snap.exists():snap.write_bytes(b)
 x=json.loads(b);claims=set(exact_full_claims(x));mentions=[s for s in H if s.encode() in b]
 for s in claims:prior[s].append(str(p))
 if claims or mentions:rawmentions.append({'path':str(p),'exact_hash_mentions':mentions,'qualifying_full_read_claims':sorted(claims)})
 observations.append({'path':str(p),'sha256':h,'size_bytes':len(b),'snapshot':str(snap.relative_to(R))})
write('COMPLETION_DEDUP_SNAPSHOT.json',{'observed_utc':now,'files':observations})
# A frozen row mentions all hashes but is not previous full-source review unless its scope flag qualifies.
write('DEDUP_RECONCILIATION.json',{'observed_utc':now,'method':'Exact SHA256 equality; full_static_inspection or static_inspection_complete must be true. No basename, AST or theorem/manifest inference. All recursive COVERAGE files searched as well as frozen inventory and additive registry.','recursive_coverage_files':len(paths)-2,'assigned_hash_count':len(H),'previously_covered_hashes':len(prior),'new_credit_hashes':len(H)-len(prior),'previous_full_scope_matches':dict(prior),'mention_vs_scope_evidence':rawmentions,'all_originals_in_frozen_inventory':H<={x['sha256'] for x in readj(paths[0])}})
# Record only exact-source preservation, separate from mutable metadata.
source_checks=[]
for s in readj(R/'SOURCE_BASELINE.json'):
 p=pathlib.Path(s['path']);b=p.read_bytes();h=digest(b);source_checks.append(dict(s,completion_sha256=h,unchanged_since_baseline=h==s['observed_sha256'],matches_expected=h==s['source_sha256']))
byte_checks=[]
for r in rows:
 p=pathlib.Path(r['local_content']);q=R/'source_snapshots'/f'{r["sha256"]}.txt';b=p.read_bytes();s=q.read_bytes();byte_checks.append({'sha256':r['sha256'],'code_bytes_path':str(p),'snapshot':str(q.relative_to(R)),'code_bytes_match':digest(b)==r['sha256'],'snapshot_match':digest(s)==r['sha256'],'snapshot_byte_identical':b==s,'line_count':len(s.splitlines())})
assert all(s['matches_expected'] and s['unchanged_since_baseline'] for s in source_checks)
assert all(s['code_bytes_match'] and s['snapshot_match'] and s['snapshot_byte_identical'] for s in byte_checks)
write('ORIGINAL_PRESERVATION_CHECK.json',{'observed_utc':now,'master_standalone_occurrences':len(source_checks),'source_hashes':len(byte_checks),'all_assigned_originals_unchanged':True,'all_snapshots_byte_identical':True,'source_checks':source_checks,'byte_snapshot_checks':byte_checks,'source_execution':False,'source_import':False,'source_compilation':False,'source_syntax_parse':False,'original_source_writes':False,'central_registry_writes':False})
metadata=[]
for f in base['files']+oldcov:
 p=pathlib.Path(f['path']);new=digest(p.read_bytes()) if p.is_file() else None;metadata.append({'path':str(p),'baseline_sha256':f['sha256'],'completion_sha256':new,'changed':new!=f['sha256']})
historical=readj('code_coverage_audit_0228/INPUT_SNAPSHOT.json');root=pathlib.Path(historical['master_path']);rootstatus=[]
for name,h in historical['master_root_seals_sha256'].items():
 p=root/name;got=digest(p.read_bytes()) if p.exists() else None;rootstatus.append({'path':str(p),'historical_frozen_sha256':h,'current_sha256':got,'matches_historical':got==h,'comparison_note':'Historical frozen input versus completion only, not an observed start/end drift interval.'})
write('METADATA_DRIFT.json',{'observed_utc':now,'changed_metadata_files':[x for x in metadata if x['changed']],'baseline_metadata_checks':metadata,'root_seal_historical_comparison':rootstatus,'interpretation':'Concurrent registry/coverage/root metadata may be updated by other workers or parent. This review wrote none of them. Source bytes are independently checked in ORIGINAL_PRESERVATION_CHECK.json; metadata drift is not source tampering.'})
cover=[]
for r,report in zip(rows,reports):
 assert report['source_sha256']==r['sha256'] and report['read_intervals']==[[1,r['lines']]]
 prior_sources=prior[r['sha256']]
 cover.append({'index':r['index'],'sha256':r['sha256'],'representative_path':r['representative_path'],'batch':r['batch'],'bytes':r['size_bytes'],'lines':r['lines'],'full_static_inspection':True,'static_inspection_complete':True,'read_ranges':[[1,r['lines']]],'new_coverage_credit':not bool(prior_sources),'new_full_read_credit':not bool(prior_sources),'previously_covered':bool(prior_sources),'prior_full_read_evidence':prior_sources,'source_executed':False,'source_executed_in_review':False,'source_imported':False,'source_compiled':False,'source_parsed':False,'source_syntax_parsed':False,'snapshot':report['source_snapshot'],'report':report['report_path'],'report_sha256':digest((R/report['report_path']).read_bytes()),'origin_class_preserved':r['origin_class'],'origin_basis_preserved':r['origin_basis'],'dependency_closure_complete':False})
write('COVERAGE.json',{'package':R.name,'completed_utc':now,'assigned_batches':list(dict.fromkeys(r['batch'] for r in rows)),'assigned_batch_hashes':len(rows),'fully_read_hashes_this_review':len(rows),'new_full_read_hashes':sum(r['new_coverage_credit'] for r in cover),'new_coverage_credit':sum(r['new_coverage_credit'] for r in cover),'previously_covered_hashes':sum(r['previously_covered'] for r in cover),'total_source_bytes_read':sum(r['bytes'] for r in cover),'total_source_lines_read':sum(r['lines'] for r in cover),'all_assigned_source_reads_complete':True,'all_research_material_checks_finished':False,'dependency_closure_complete':False,'source_execution':'none','source_import_compilation_syntax_parse':'none','scope_note':'46 assigned exact hashes only; first-to-last inert source inspection, static mathematical/cost/guard analysis and stored-result provenance. No current runtime regression or blanket theorem/novelty acceptance. Dependency snapshots alone earn no source-read credit.','rows':cover})
write('FINDINGS.json',{'status':'complete assigned inert source review','high_signal_findings':['F8 contraction sources are finite positive local-existence certificates, distinct from the adjacent-anchor inverse-sum obstruction subsumed by the 0407 cut-rank proof.','Fixed-g shear/Green cost requires nondegenerate clean pilots, balance and sparse innovations; recurrence has 2^g subset dependence.','Complex sparse-phase tolerance comparison can accept nonfinite inputs; static branch diagnosis, never executed.','Dyadic aggregate output uses modular pow per event/bin; partial counter is not complete linear word complexity.','Fixed-direction graph completion does not search unknown directions and still forms a dense U B V in this checker.','Local manifests all match; co-sealed old PASS results are not new execution attestations.'],'counts':{'assigned_sources':46,'source_bytes':229887,'source_lines':4872,'master_occurrences':55,'local_manifest_checks':309},'new_coverage_credit':sum(r['new_coverage_credit'] for r in cover)})
# Seal every package file except the seal and its listing. All snapshots are inert.
items=[]
for p in sorted(R.rglob('*')):
 if p.is_file() and p.name not in ['SHA256SUMS.txt','SEAL.json']:
  b=p.read_bytes();items.append({'path':str(p.relative_to(R)),'size_bytes':len(b),'sha256':digest(b)})
listing=''.join(f'{i["sha256"]}  {i["path"]}\n' for i in items);(R/'SHA256SUMS.txt').write_text(listing)
write('SEAL.json',{'package':R.name,'completed_utc':now,'payload_file_count':len(items),'payload_bytes':sum(x['size_bytes'] for x in items),'sha256sums_sha256':digest(listing.encode()),'source_hash_count':46,'new_coverage_credit':sum(r['new_coverage_credit'] for r in cover),'source_execution':False,'source_import':False,'source_compilation':False,'source_parsing':False,'originals_preserved':True,'manifest_file':'SHA256SUMS.txt','verification':'Fresh metadata-only finalization; no supplied source execution.'})
# Fresh verification of the just-written listing.
for i in items:assert digest((R/i['path']).read_bytes())==i['sha256']
print(json.dumps({'files_sealed':len(items),'new_credit':sum(r['new_coverage_credit'] for r in cover),'previously_covered':sum(r['previously_covered'] for r in cover),'recursive_coverage_files':len(paths)-2,'metadata_drifts':len([x for x in metadata if x['changed']]),'sha256sums_sha256':digest(listing.encode()),'all_package_hashes_verified':True},indent=2))
