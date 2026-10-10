"""Reviewer-authored metadata/seal finalizer; no inspected-source execution."""
from pathlib import Path
import json,hashlib,datetime
P=Path(__file__).resolve().parent;M=Path('fft_research_master_20261009');B=Path('code_coverage_audit_0228');R=Path('post_v22_review_registry_0308/ADDITIVE_CODE_COVERAGE.json')
h=lambda b:hashlib.sha256(b).hexdigest()
# Wall-clock environment reports are not used; task UTC supplied by runtime.
now='2026-10-10T04:43:27Z'
rs=json.loads((P/'SOURCE_MANIFEST.json').read_text());reviews=json.loads((P/'SOURCE_REVIEWS.json').read_text());byid={r['review_id']:r for r in reviews}
# Preserve nearby text showing that the phase9 theorem/review already includes observability.
context=[]
for sid,name,lines in [('S25','THEOREMS.md',[[19,39],[124,150]])]:
 r=next(r for r in rs if r['review_id']==sid);f=(M/r['representative_path']).parent/name;data=f.read_bytes();rel='stored_evidence/S25__THEOREMS.md';(P/rel).write_bytes(data);context.append({'snapshot':rel,'origin':str(f),'sha256':h(data),'inspected_lines':lines,'scope':'Relevant passages read, not a full textual theorem review.'})
f=M/'additions/2318_reviewed/review_incoming_2257_routed/SOURCE_REVIEW.md';data=f.read_bytes();rel='stored_evidence/S25__PRIOR_SOURCE_REVIEW.md';(P/rel).write_bytes(data);context.append({'snapshot':rel,'origin':str(f),'sha256':h(data),'inspected_lines':[[102,110],[126,126]],'scope':'Relevant prior-review paragraphs read; already states zero-mode chosen-controller limitation.'})
(P/'THEORY_CONTEXT_RECONCILIATION.json').write_text(json.dumps(context,indent=2)+'\n')
for sid in ['S25','S26']:
 byid[sid]['findings'].append({'lines':'1-25'if sid=='S25'else'1-13','category':'prior_scope_reconciliation','finding':'Fresh zero-seed counterexample confirms a documentation/API completeness boundary, not a refutation of the qualified theorem. Adjacent THEOREMS.md:27-33 and prior SOURCE_REVIEW.md:102-110 already require nonzero seed spectra for fully identifiable recovery and describe zero modes as a separate chosen-controller branch. Both spatial and spectral counterexamples are in INDEPENDENT_ARITHMETIC_RESULTS.json.'})
for sid,eid in [('S04','E03'),('S07','E05')]:
 byid[sid]['findings'].append({'lines':'89-144'if sid=='S04'else'105-126','category':'stored_log_reconciliation','finding':'Stored log '+eid+' includes the later-defined classes: 11 total tests for phase7 and 13 for phase8. Therefore the direct-script omission is not evidence those stored runs skipped the classes; module discovery includes them. No source tests were rerun here.'})
# Attach explicit stored evidence associations.
ei=json.loads((P/'STORED_EVIDENCE_INDEX.json').read_text())
for review in reviews:review['stored_evidence_ids']=[e['evidence_id']for e in ei if review['review_id']in e['source_review_ids']]
(P/'SOURCE_REVIEWS.json').write_text(json.dumps(reviews,indent=2)+'\n')
# Frozen exact coverage baseline, selected only on full-static status.
inv=json.loads((B/'CODE_COVERAGE_INVENTORY.json').read_text());frozen=[{'sha256':r['sha256'],'coverage_status':r['coverage_status'],'static_inspection_complete':r['static_inspection_complete']}for r in inv if r.get('static_inspection_complete')]
(P/'FROZEN_FULLREAD_HASHES.json').write_text(json.dumps({'inventory_sha256':h((B/'CODE_COVERAGE_INVENTORY.json').read_bytes()),'count':len(frozen),'rows':frozen},indent=2)+'\n')
regraw=R.read_bytes();reg=json.loads(regraw);(P/'REGISTRY_AT_COMPLETION.json').write_bytes(regraw)
prior={r['sha256']for r in frozen}|{r['sha256']for r in reg['rows']};new=[r for r in rs if r['sha256']not in prior]
assert len(new)==45
(P/'DEDUP_RECONCILIATION.json').write_text(json.dumps({'completed_utc':now,'baseline_frozen_fullread_count':len(frozen),'initial_accepted_total':615,'completion_accepted_total':reg['current_full_static_reads'],'registry_initial_sha256':h((P/'REGISTRY_BEFORE.json').read_bytes()),'registry_completion_sha256':h(regraw),'registry_unchanged_during_review':regraw==(P/'REGISTRY_BEFORE.json').read_bytes(),'assigned_batch_rows':47,'skipped_already_accepted_hashes':[r['sha256']for r in json.loads((P/'SKIPPED_ALREADY_REVIEWED.json').read_text())],'fully_read_new_hashes':45,'overlap_at_completion':[],'central_registry_modified_by_review':False},indent=2)+'\n')
# Potential local import targets are hashed, never imported, parsed or executed.
deps=[];covered=prior|{r['sha256']for r in rs}
for r in rs:
 d=(M/r['representative_path']).parent
 for im in r.get('import_references',[]):
  modules=[im['module']]if im.get('module')else im.get('names',[])
  for module in modules:
   if not isinstance(module,str):continue
   f=d/(module.replace('.','/')+'.py')
   rec={'source_review_id':r['review_id'],'module':module,'basis':'Frozen inventory syntactic reference plus same-directory candidate only; no runtime resolution or imported-source closure claim.'}
   if f.is_file():
    hh=h(f.read_bytes());rec.update({'candidate_path':str(f),'candidate_sha256':hh,'hash_in_accepted_or_current_fullread_set':hh in covered})
   else:rec['candidate_path']=None
   deps.append(rec)
(P/'DEPENDENCIES.json').write_text(json.dumps({'dependency_closure_complete':False,'rows':deps},indent=2)+'\n')
# Recheck byte preservation and metadata after all reading.
pres=json.loads((P/'SOURCE_PRESERVATION.json').read_text())
for rec,r in zip(pres,rs):
 cache=Path(r['local_content']);master=M/r['representative_path'];snap=P/r['snapshot'];assert h(cache.read_bytes())==h(master.read_bytes())==h(snap.read_bytes())==r['sha256'];assert cache.stat().st_mtime_ns==rec['cache_stat']['mtime_ns'];assert cache.stat().st_mode==rec['cache_stat']['mode']
(P/'PRESERVATION_FINAL.json').write_text(json.dumps({'all_45_cache_master_snapshot_hashes_match':True,'all_cache_sizes_match':True,'metadata_mtime_mode_unchanged_from_reconciliation':True,'batch_vs_frozen_metadata_drift_rows':0,'source_write_operations_performed':0,'all_sources_preserved':True},indent=2)+'\n')
revsha=h((P/'SOURCE_REVIEWS.json').read_bytes())
coverage={'package':P.name,'completed_utc':now,'assigned_batches':json.loads((P/'ASSIGNMENT_SNAPSHOT.json').read_text())['batch_names'],'assigned_batch_hashes':47,'fully_read_hashes_this_review':45,'new_full_read_hashes':45,'new_coverage_credit':45,'previously_covered_hashes':2,'total_source_bytes_read':sum(r['actual_size']for r in rs),'total_source_lines_read':sum(r['line_count']for r in rs),'all_assigned_new_source_reads_complete':True,'all_research_material_checks_finished':False,'dependency_closure_complete':False,'source_execution':'none','source_import_compilation_syntax_parse':'none','scope_note':'First-to-last inert inspection of 45 new exact source hashes, line-referenced mathematics/implementation/evidence/model findings. Stored evidence is not current runtime proof; fresh reviewer arithmetic is separate; no blanket theorem or novelty acceptance.','rows':[]}
for r in rs:
 coverage['rows'].append({'review_id':r['review_id'],'sha256':r['sha256'],'representative_path':r['representative_path'],'batch':r['batch'],'bytes':r['actual_size'],'lines':r['line_count'],'full_static_inspection':True,'static_inspection_complete':True,'full_source_read':True,'line_ranges':[[1,r['line_count']]],'source_executed_in_review':False,'evidence_file':'SOURCE_REVIEWS.json','evidence_sha256':revsha,'snapshot':r['snapshot']})
(P/'COVERAGE.json').write_text(json.dumps(coverage,indent=2)+'\n')
# Human-readable per-source deliverable.
report=['# Routed factor source review','',f'Completed {now}. Full inert review: 45 exact hashes, {coverage["total_source_lines_read"]:,} lines, {coverage["total_source_bytes_read"]:,} bytes. Two already accepted hashes were excluded.','', '## Main conclusions','', '- Confirmed implementation defect: phase6 transform_legs performs int64 contraction before modular reduction. A legitimate F2013265921 tensor/gauge example gives 841097758 instead of 0. This concerns the NumPy gauge helper, not the Python-integer FFT executor.', '- Confirmed scope boundary: phase9 zero-seed modes can reject members of the broader sparse-innovation family. Both spatial and spectral counterexamples are provided. The adjacent theorem and prior review already impose observable seed spectra; this is not a refutation of that qualified theorem.', '- The phase7/phase8 direct test-script entrypoints omit late-defined classes. Saved logs nevertheless contain all 11/13 tests, consistent with module discovery; do not call those saved runs incomplete.', '- The exploratory rank-r MILP reads a possible missing incumbent and reports its rounded objective without requiring optimal status. Existing saved n=2..6 lines report status 0; that does not remove the unguarded failure path.', '- Preserve existing caveats: N2/F3 invertible Schur-baseline exception; missing Haar z=1 guard; small/partial tests; finite-field versus complex precision; randomized membership; arithmetic proxies; fixed graph/rank/sparsity grammars.', '- No supplied source was executed, imported, compiled or AST-parsed. Only reviewer-authored inert metadata utilities and fresh arithmetic counterexamples ran. No central registry was changed.','', '## Evidence levels','', 'SOURCE_REVIEWS.json is the complete 45-source line-referenced review. COVERAGE.json carries only source-read credit. Source snapshots are byte-exact. STORED_EVIDENCE_RECONCILIATION.json records earlier reported results without promoting them to current execution evidence. INDEPENDENT_ARITHMETIC_RESULTS.json contains only fresh reviewer checks. THEORY_CONTEXT_RECONCILIATION.json reconciles the already-qualified phase9 promise. DEPENDENCIES.json does not claim full import closure.','', '## Individual sources','']
for r in reviews:
 report.extend([f'### {r["review_id"]}: {r["representative_path"]}',f'Exact SHA-256: {r["sha256"]}. Complete read: lines 1–{r["line_count"]}.',''])
 for f in r['findings']:report.append(f'- Lines {f["lines"]} [{f["category"]}]: {f["finding"]}')
 report.append('')
(P/'REVIEW.md').write_text('\n'.join(report)+'\n')
summary={'package':P.name,'new_exact_fullreads':45,'already_covered_skipped':2,'source_bytes':coverage['total_source_bytes_read'],'source_lines':coverage['total_source_lines_read'],'new_fullread_credit':45,'source_execution':False,'full_import_closure':False,'all_material_checks_finished':False,'source_and_metadata_preservation':True,'stored_evidence_files':len(ei),'additional_theory_context_snapshots':len(context),'main_files':['REVIEW.md','SOURCE_REVIEWS.json','COVERAGE.json','INDEPENDENT_ARITHMETIC_RESULTS.json','STORED_EVIDENCE_RECONCILIATION.json','DEDUP_RECONCILIATION.json','PRESERVATION_FINAL.json'],'key_restriction':'Coverage completion does not assert mathematical novelty, unrestricted FFT results, comprehensive runtime correctness, or current reproduction of stored results.'}
(P/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
