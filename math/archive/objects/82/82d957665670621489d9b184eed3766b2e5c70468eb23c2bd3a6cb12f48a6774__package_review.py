#!/usr/bin/env python3
"""New metadata-only packager; never executes/imports/parses assigned source code."""
from pathlib import Path
import hashlib,json,shutil
OUT=Path('construction_source_code_review_0241')
AUD=Path('code_coverage_audit_0228')
MASTER=Path('master_v22_integration_20261010/fft_research_master_20261009')
BASE=MASTER/'additions/0038_construction_and_source_synthesis/constructions'
PRIOR=MASTER/'additions/0155_material_coverage_and_new_results/reviews/review_marked_next_pivot_variable_block'
BATCH=AUD/'pending_batches/02_addition_0038_construction_and_source_synthesis_01.json'
sha=lambda b:hashlib.sha256(b).hexdigest()
def write(name,obj): (OUT/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
index=[]
def copy(src,dest):
    src=Path(src);dest=Path(dest);b=src.read_bytes();target=OUT/dest;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(b)
    x={'path':str(dest),'source_path':str(src),'sha256':sha(b),'size_bytes':len(b)};index.append(x);return x
batch=json.loads(BATCH.read_text());copy(BATCH,'INPUT_BATCH.json')
configs=[
('3f2d3e66','chirp_feedback/projective_row_gate','PROJECTIVE_CONSISTENCY_GATE.md','PROJECTIVE_GATE_RESULTS.json','MANIFEST.sha256',[(1,40,'exact matrix/projective primitives'),(41,99,'polynomial and domain arithmetic'),(100,138,'2-SAT'),(139,198,'complete row solver'),(199,218,'extraction and target'),(219,289,'controls'),(290,302,'main and output')],['Selected-row subsystem only; closure is not base-field realization','O(N^3) extraction, finite point enumeration, quadratic clauses/SCC numbering and recursive DFS','Fixed valid fixtures; no general parameter validation'],['recursion_depth','fixture_only_guards','selected_subsystem_not_synthesis']),
('e9ec24c5','bank_interface','CONSTRUCTOR_FROZEN_DELIVERABLES_FOR_CHECKPOINT20.md','CONSTRUCTOR_FROZEN_DELIVERABLES_FOR_CHECKPOINT20.json','SHA256SUMS.txt',[(1,11,'setup/hash membership'),(12,66,'all thirteen fixed records'),(67,90,'seal/payload verification'),(91,110,'inventory generation and self-seal')],['Hard-coded paths and historical queued/accepted statuses','Top-level writes; requires existing OUT and matching self-copy','Assertions, trusted manifest names and first seal token; not untrusted-manifest ingestion'],['stale_historical_statuses','nonportable_paths','trusted_manifest_input']),
('08f12831','bank_interface/iteration_10_marked_tree','NEXT_PIVOT_TREE_AND_SUPPORT_REDUCTION.md','NEXT_PIVOT_RANK_DIAGNOSTIC.json','NEXT_PIVOT_SUPPORT_SHA256SUMS.txt',[],['Prior exact full static read explicitly documented','Reference-tree guard can fail while pivot is invertible','Constant-input sparse jets only; no retained inverse or shrinking recursion'],['prior_evidence_reconciled','reference_chart_guard','constructor_oracle_not_production_schedule']),
('fa55410f','bank_interface/iteration_10_marked_tree','ONE_SCHUR_STEP_AND_TWO_RUN_JET.md','ONE_SCHUR_TWO_RUN_CONTROLS.json','ONE_SCHUR_TWO_RUN_SHA256SUMS.txt',[(1,27,'field solves/K/C'),(28,56,'two-run coefficients/diagnostics'),(57,103,'Schur and full-space controls'),(104,108,'fixed cases/output')],['Twenty fixed finite controls; only one stage and constant input','Per-edge pow, dictionary aggregation, N(log N) diagnostic loops and dense solves are not claimed linear production schedule','Pivot q asserted; singular retained solve fails; no general shape/order validation'],['verifier_cost_not_algorithm_cost','constant_input_only','coupled_inverse_unresolved']),
('74603e67','bank_interface/iteration_10_marked_tree','ROOT_POLE_CANCELLATION_AND_LINEAR_TREE_JET.md','ROOT_POLE_CANCELLATION_CONTROLS.json','ROOT_POLE_CANCELLATION_SHA256SUMS.txt',[(1,31,'exact matrix arithmetic'),(32,59,'tree/kernel jet'),(60,95,'determinant, recovery and marker controls'),(96,105,'fixtures and output')],['Root-pole cancellation, not cheap full bordered inverse','Selected-vector/selected-scalar jet checks do not by themselves prove all-input coefficient identity','Fixed dyadic prime-field fixtures and dense test oracles'],['bounded_control_scope','coupled_inverse_unresolved']),
('5dd8b9d9','bank_interface/iteration_11_variable_block','VARIABLE_BIT_BLOCK_ELIMINATION_AND_WORK.md','VARIABLE_BLOCK_JET_CONTROLS.json','VARIABLE_BLOCK_SHA256SUMS.txt',[],['Prior exact full static read explicitly documented','Full-frontier count only; b near log log N still costs Theta(N log N)','Separate branch/full-system guards do not guarantee packet chart; retained inverse unresolved'],['prior_evidence_reconciled','packet_guard','evaluator_specific_cost']),
('6cd950c7','bank_interface/iteration_9_bank_interface','FOURIER4_GREEN_KERNEL_AND_FOURIER8_CHART.md','FOURIER4_KERNEL_CONTROLS.json','FOURIER4_KERNEL_SHA256SUMS.txt',[(1,28,'rank/root primitives'),(29,46,'F4 kernel/guards'),(47,59,'F8 chart and output')],['F4 split failures recorded separately; global assertions flag is not all-primes construction','Primitive/quadratic root enumeration is bounded fixture work','Narrow F8 chart; no automatic Hamiltonian lift'],['split_distinct_guard','finite_enumeration_cost','no_hamiltonian_batch_lift']),
('5041ae6e','bank_interface/iteration_9_bank_interface','FOURIER8_NONCOMMUTING_ANCHOR_CERTIFICATE.md','FOURIER8_NONCOMMUTING_ANCHOR_CONTROLS.json','FOURIER8_NONCOMMUTING_ANCHOR_SHA256SUMS.txt',[(1,43,'exact cyclotomic ring and routing'),(44,76,'transition forest'),(77,110,'commutator and guarded axis rejection'),(111,144,'targets, controls and output')],['Four adjacent-anchor commutator rejections; four halves-anchor nonsingular-endpoint axis rejections','Restricted shortcut only, not full projective solver; inconclusive is not PASS','Exact unbounded integer coefficients; no bit-cost/stability bound'],['nonsingular_endpoint_scope','fixed_eight_charts','shortcut_not_complete_gate']),
('1106a6c7','bank_interface/iteration_9_bank_interface','MONOMIAL_WEYL_BATCH_CLASSIFICATION.md','MONOMIAL_WEYL_CLASSIFICATION_CONTROLS.json','MONOMIAL_WEYL_CLASSIFICATION_SHA256SUMS.txt',[(1,72,'field/dense reference primitives'),(73,127,'promised sparse recovery'),(128,167,'normal form and controls'),(168,221,'bank and paired-layer family'),(222,234,'main/output')],['Lines 89–95: list-membership assertion is Theta(c^2); d=1 yields c=N','Line 93 exponentiates before root-table construction; linear_pass_counts omit overhead','Promised input and genuine seed required; finite family source inspection does not expand prior theorem acceptance'],['quadratic_recovery_implementation','incomplete_operation_ledger','promised_input_not_circuit_certification']),
('63ad58eb','chirp_feedback/feedback_small_survivors','SMALL_GATE_SURVIVORS.md','SMALL_SURVIVOR_RESULTS.json','MANIFEST.sha256',[(1,55,'finite arithmetic and target'),(56,82,'symbolic N3 exact field'),(83,107,'N3 scans/feedback'),(108,123,'transition helpers'),(124,181,'N5 local/global gate and controls'),(182,185,'output')],['Unpinned SymPy exact-symbolic dependency; no complex numerical stability claim','N3 finite explicit construction; N5 fixed cycle-order rejection only','Characteristic-zero lift uses separate report specialization/guard argument'],['sympy_dependency_unpinned','fixed_small_size_scope','modular_lift_requires_proof'])]
lookup={r['sha256'][:8]:r for r in batch['rows']}
verification=[];rows=[]
for pref,sub,report,res,seal,ranges,findings,tags in configs:
    r=lookup[pref];h=r['sha256'];b=Path(r['local_content']).read_bytes();assert sha(b)==h and len(b)==r['size_bytes'];linecount=len(b.splitlines())
    source=copy(r['local_content'],f'inert_source_snapshots/{h}.txt')
    origin=[]
    for name in [report,res,seal]:origin.append(copy(BASE/sub/name,f'evidence/{pref}/{name}'))
    source_alias=BASE/sub/r['representative_path'].split('/')[-1]
    assert sha(source_alias.read_bytes())==h
    sealchecks=[]
    for line in (BASE/sub/seal).read_text().splitlines():
        if not line.strip():continue
        expected,name=line.split(None,1);name=name.strip().lstrip('*');payload=BASE/sub/name;actual=sha(payload.read_bytes());assert expected==actual
        sealchecks.append({'name':name,'expected':expected,'actual':actual,'match':True})
    assert any(x['actual']==h for x in sealchecks)
    verification.append({'source_seal':str(BASE/sub/seal),'seal_sha256':sha((BASE/sub/seal).read_bytes()),'payloads':sealchecks,'all_match':True})
    if pref in ('3f2d3e66','63ad58eb'):origin.append(copy(BASE/sub/'CHECK_RUN.log',f'evidence/{pref}/CHECK_RUN.log'))
    if pref=='e9ec24c5':origin.append(copy(BASE/sub/'FROZEN_SOURCE_FILES.txt',f'evidence/{pref}/FROZEN_SOURCE_FILES.txt'))
    inherited=pref in ('08f12831','5dd8b9d9')
    rows.append({'sha256':h,'size_bytes':len(b),'line_count':linecount,'original_master_path':r['representative_path'],'master_path':str(MASTER/r['representative_path']),'occurrences':r['occurrences'],'origin':'constructor/reviewer authored','origin_detail':'authored preservation inventory utility' if pref=='e9ec24c5' else 'constructor-authored exact research control','origin_evidence':origin,'source_snapshot':source,'status':'prior_full_static_read_evidence_reconciled' if inherited else 'new_full_static_read_completed','full_static_read':True,'static_inspection_complete':True,'current_review_complete_read':not inherited,'method':'Exact prior report declaration plus provenance/snapshot/manifest SHA256 reconciliation' if inherited else 'Complete inert line-numbered reading and reasoning; no execution/import/compile/parse','extent':{'lines':[1,linecount],'all_bytes_accounted':True,'current_read_sections':[{'start_line':a,'end_line':b,'subject':s} for a,b,s in ranges],'prior_read_inherited':inherited},'source_execution':False,'current_audit_uploaded_execution':'none','historical_execution_evidence':{'kind':'sealed authored-run declaration and control artifact' if pref!='e9ec24c5' else 'sealed authored generator plus generated artifacts','fresh_run_here':False,'exact_command_and_exit_receipt_reconstructed':False,'sealed_controls_not_a_substitute_for_source_read':True},'scope_and_findings':findings,'finding_tags':tags,'precision':'Exact modular/cyclotomic/symbolic arithmetic, or metadata only; no floating stability/bit-complexity certification','report':'REVIEW.md'})
# Verify and preserve exact prior whole-source static-read evidence, not just acceptance.
priorfiles=['MARKED_NEXT_PIVOT_VARIABLE_BLOCK_AUDIT.md','PROVENANCE.json','SEALED_MANIFEST.json','SEALED_MANIFEST.sha256']
prefs={}
for name in priorfiles:prefs[name]=copy(PRIOR/name,f'evidence/prior_marked_audit/{name}')
prior_manifest=json.loads((PRIOR/'SEALED_MANIFEST.json').read_text());expected=(PRIOR/'SEALED_MANIFEST.sha256').read_text().split()[0];assert sha((PRIOR/'SEALED_MANIFEST.json').read_bytes())==expected
checks=[]
for f in prior_manifest['files']:
    actual=sha((PRIOR/f['path']).read_bytes());assert actual==f['sha256'];checks.append({'path':f['path'],'sha256':actual,'match':True})
verification.append({'source_seal':str(PRIOR/'SEALED_MANIFEST.sha256'),'manifest_sha256':expected,'all_manifest_payloads_rehashed':True,'payloads':checks,'all_match':True})
prov=json.loads((PRIOR/'PROVENANCE.json').read_text())
for row in rows:
    if row['status']=='prior_full_static_read_evidence_reconciled':
        s=next(s for s in prov['snapshots'] if s['sha256']==row['sha256']);actual=sha((PRIOR/s['snapshot']).read_bytes());assert actual==row['sha256']
        row['prior_static_read_evidence']={'report':prefs['MARKED_NEXT_PIVOT_VARIABLE_BLOCK_AUDIT.md'],'report_lines':[20,34],'exact_scope_quote':'Reports and checkers were read statically. Neither constructor checker nor any uploaded program was executed or imported.','provenance':prefs['PROVENANCE.json'],'snapshot_original_path':str(PRIOR/s['snapshot']),'snapshot_sha256':actual,'prior_manifest':prefs['SEALED_MANIFEST.json'],'prior_manifest_seal':prefs['SEALED_MANIFEST.sha256'],'all_prior_manifest_payloads_match':True,'fresh_read_of_checker_claimed':False}
# Snapshot queue membership evidence without mutating the auditor's working registry.
for name in ['REVIEW_QUEUE_01_THEORETICAL_GATE.json','REVIEW_QUEUE_02_GREEN_GATE_CODE.json','REVIEW_QUEUE_03_RECOVERED_CORE_IMPLEMENTATIONS.json']:
    data=(AUD/name).read_text();assert not any(r['sha256'] in data for r in rows);copy(AUD/name,'coordination/'+name)
coord={'assignment':'02_addition_0038_construction_and_source_synthesis_01.json','assigned_hashes':len(rows),'queue01_02_03_overlap':[],'auditor_confirmation':'Confirmed by audit_remaining_code_coverage; Queue03 withdrawn. Post-v21 evidence then identified exact prior coverage for 08f12831… and 5dd8b9d9….','post_v21_inherited_hashes':[r['sha256'] for r in rows if r['status']=='prior_full_static_read_evidence_reconciled']}
write('COORDINATION.json',coord)
write('COVERAGE.json',{'review':'construction_source_code_review_0241','scope':'exact-hash source inspection or explicit whole-source evidence reconciliation','source_execution':False,'rows':rows})
write('MANIFEST_VERIFICATION.json',verification)
write('EVIDENCE_INDEX.json',index)
summary={'assigned_hashes':10,'assigned_bytes':sum(r['size_bytes'] for r in rows),'assigned_lines':sum(r['line_count'] for r in rows),'new_full_static_read_hashes':8,'new_full_static_read_bytes':sum(r['size_bytes'] for r in rows if r['current_review_complete_read']),'new_full_static_read_lines':sum(r['line_count'] for r in rows if r['current_review_complete_read']),'prior_full_static_read_reconciled_hashes':2,'all_exact_hashes_accounted':True,'uploaded_or_constructor_source_execution_here':False,'originals_changed':False,'material_defects':['Weyl recover list-membership validation causes quadratic worst-case work omitted from pass counters','Frozen inventory preserves historical queued statuses and hard-coded paths'],'scope_boundaries_preserved':True}
assert summary['assigned_bytes']==88475 and summary['assigned_lines']==1525
write('SUMMARY.json',summary)
# The seal deliberately excludes itself; all originals remain unchanged.
files=[]
for p in sorted(OUT.rglob('*')):
    if p.is_file() and p.name not in ('SEALED_MANIFEST.json','SEALED_MANIFEST.sha256'):
        data=p.read_bytes();files.append({'path':str(p.relative_to(OUT)),'bytes':len(data),'sha256':sha(data)})
write('SEALED_MANIFEST.json',{'review':'construction_source_code_review_0241','status':'sealed','source_execution':False,'files':files})
(OUT/'SEALED_MANIFEST.sha256').write_text(sha((OUT/'SEALED_MANIFEST.json').read_bytes())+'  SEALED_MANIFEST.json\n')
for f in files:assert sha((OUT/f['path']).read_bytes())==f['sha256']
print(json.dumps({'summary':summary,'sealed_files':len(files),'manifest_sha256':sha((OUT/'SEALED_MANIFEST.json').read_bytes())},indent=2))
