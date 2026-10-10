"""Assemble and seal reviewer-owned static evidence; never execute supplied sources."""
from pathlib import Path
import json,hashlib,shutil,datetime,re
P=Path(__file__).parent
H=lambda b:hashlib.sha256(b).hexdigest()
def save(name,obj): (P/name).write_text(json.dumps(obj,indent=2)+'\n')
rows=json.loads((P/'SOURCE_MANIFEST.json').read_text());parent=json.loads((P/'PARENT_REVIEWS.json').read_text());worker=json.loads((P/'worker_materials/REVIEWS.json').read_text());wr=json.loads((P/'worker_materials/READ_EVIDENCE.json').read_text());reviews=worker+parent;by={r['sha256']:r for r in reviews};assert len(by)==len(reviews)==86
receipts=[]
for f in sorted((P/'read_evidence').glob('sources_*.txt')):
 ids=list(map(int,f.stem.removeprefix('sources_').split('_')));records=[]
 for i in ids:
  r=rows[i-1];assert ('===== END SOURCE '+str(i)+'; '+str(r['size_bytes'])+' bytes; '+str(r['line_count'])+' lines =====') in f.read_text();records.append({'index':i,'sha256':r['sha256'],'bytes_half_open':[0,r['size_bytes']],'lines_inclusive':[1,r['line_count']]})
 receipts.append({'command':'python '+str(P/'read_sources.py')+' '+' '.join(map(str,ids)),'output_file':str(f.relative_to(P)),'output_sha256':H(f.read_bytes()),'records':records,'output_truncated':False,'output_displayed_first_to_last':True,'receipt_basis':'Complete command output was returned through functions.exec/exec_command and read first-to-last in this review; no supplied source execution.'})
for x in wr['read_receipts']:
 x=dict(x);x['output_file']=str(Path(x['output_file']).relative_to(P));receipts.append(x)
save('READ_EVIDENCE.json',{'method':'Full first-to-last inert text reads by parent (52) and worker (34), not AST/syntax/manifest inference. Numbered output receipts bind unmodified source bytes through per-source SHA256.','source_hashes':86,'source_bytes':413910,'source_lines':9466,'read_receipts':receipts,'source_execution':False,'source_import':False,'source_compilation':False,'source_AST_parsing':False})
findings=[]
for f in wr['significant_findings']:
 x=dict(f);x['source_indices']=[i+1 for i in f['indices']];x['source_sha256s']=[rows[i]['sha256'] for i in f['indices']];x['index_convention_note']='Original worker indices are zero-based; source_indices are package one-based.';findings.append(x)
new=[
 ('MEX-01','confirmed execution-path defect',[83],[(196,213)],'Direct unittest.main exits before Phase7ImportTests is defined, skipping its test under direct script invocation. Discovery/import mode may include it.','No uploaded execution; follows Python unittest.main default exit semantics and source ordering.'),
 ('MEX-02','confirmed malformed-input validation defect',[62],[(7,14)],'affine_from_columns([2]) at k=1 constructs [0,2], passes uniqueness, but is not a permutation of [0,1]. Valid k-bit invertible descriptors remain unaffected.','Fresh arithmetic counterexample; downstream rank_permutation_difference rejects malformed permutations.'),
 ('MEX-03','confirmed raw-ABI input-boundary defect',[82],[(9,14),(32,38)],'Generated fixed-shape C++ evaluator does not normalize negative sparse-position remainder. n4, position -1 and zero edit positions derive out[-1]. Generic evaluator normalizes it.','No C++ compiled or run. Requires caller-supplied noncanonical sparse offset; does not refute correct canonical plans.'),
 ('MEX-04','qualified representation limit',[61],[(14,25),(31,43)],'NumPy int64 modular products need a safe modulus/size bound. Configured primes12289/65537 are safe; unrestricted large primes can overflow before reduction.','No within-configured-domain failure asserted.'),
 ('MEX-05','confirmed overgeneralized-assumption counterexample',[37],[(69,95)],'A local diagonal scale100I has condition1, but identity padding gives condition100. Alternating bank orientation is essential for noncommuting orthogonal factors.','Fresh rational padding control and static rational bank witness; not a universal FFT lower bound.'),
 ('MEX-06','historical implementation-accounting defect reconciled',[51,56],[(161,197),(24,49)],'Archived gauge ledger omits one literal addition per call; shrinking prototype repacks at least2NG scalar lanes even on cache hits. Stored reports and numerical ledgers agree.','Source assertions and archived outputs reconciled; predecessor programs not re-executed, corrected schedule distinct from original prototype.'),
 ('MEX-07','qualified valid exact-field mechanism',[48,50,72,75],[(120,128),(85,120),(102,120),(52,74)],'Path-Green/resolvent and inhomogeneous q-orbit formulas are scoped exact-field mechanisms. Linear preparation, sparse forcing or related-input reuse does not establish arbitrary-input full FFT improvement.','Fresh signed-norm, Green inverse and q-forcing identity controls; root/cyclotomic bit costs retained.'),
 ('MEX-08','test-evidence limitation',[85,86],[(93,118),(74,94)],'Modular comparisons round small float64 output against exact schoolbook residues. These are bounded consistency checks, not an exact arbitrary-integer production implementation.','No supplied tests run; AOT binary/source build equivalence not established.'),
 ('MEX-09','conservative status-label limitation',[53],[(122,124)],'block_fits is sufficient B<2^(L-1); failure status B_gt_N does not itself establish B>N for every N with ceiling-log L.','Positive certified flags remain conservative; no error-bound refutation.'),
]
for fid,classification,ids,ranges,text,basis in new:
 findings.append({'id':fid,'classification':classification,'source_indices':ids,'source_sha256s':[rows[i-1]['sha256'] for i in ids],'source_line_ranges':ranges,'finding':text,'evidence_basis':basis})
save('FINDINGS.json',findings)
for r in rows:
 x=by[r['sha256']];x['index']=r['index'];x['provenance']={'batch_name':r['batch_name'],'occurrences':r['occurrences'],'root_archive_sha256s':r['root_archive_sha256s'],'containing_library_archive_ids':r.get('containing_library_archive_ids',[]),'origin_class':r['origin_class'],'origin_basis':r['origin_basis']};x['finding_ids']=[f['id'] for f in findings if r['sha256'] in f['source_sha256s']];x['current_review_test_status']='Supplied tests/programs not run; archived outputs are historical. Fresh reviewer controls appear separately.'
 for k in ['source_executed_in_review','source_imported_in_review','source_compiled_in_review','source_ast_parsed_in_review']:assert x[k] is False
 assert x['coverage_intervals']=={'bytes_half_open':[[0,r['size_bytes']]],'lines_inclusive':[[1,r['line_count']]]}
 assert H((P/'sources'/r['sha256']).read_bytes())==H(Path(r['local_content']).read_bytes())==r['sha256']
 for item in x['source_line_evidence']:
  span=item.get('lines',item.get('lines_inclusive'));assert 1<=span[0]<=span[1]<=r['line_count']
 save('per_hash/'+r['sha256']+'.json',x)
reviews=sorted(by.values(),key=lambda r:r['index']);save('REVIEWS.json',reviews)
registry_path=Path('post_v22_review_registry_0308/ADDITIVE_CODE_COVERAGE.json');shutil.copyfile(registry_path,P/'REGISTRY_AT_COMPLETION.json');registry=json.loads((P/'REGISTRY_AT_COMPLETION.json').read_text());seen={r['sha256'] for r in registry['rows']};inventory=json.loads((P/'provenance/CODE_COVERAGE_INVENTORY.json').read_text());prior={r['sha256'] for r in inventory if r.get('static_inspection_complete')};overlap=seen|prior;newhash=[r for r in reviews if r['sha256'] not in overlap]
coverage={'assigned_batches':json.loads((P/'ASSIGNMENT_SNAPSHOT.json').read_text())['batch_names'],'fully_read_hashes_this_review':86,'new_full_read_hashes':len(newhash),'previously_covered_hashes':[r['sha256'] for r in reviews if r['sha256'] in overlap],'total_source_bytes_read':413910,'total_source_lines_read':9466,'all_assigned_source_reads_complete':True,'all_research_material_checks_finished':False,'dependency_closure_complete':False,'source_execution':'none; supplied code not executed/imported/compiled/AST-parsed','scope_note':'Full exact static source coverage for this86-hash assignment only; no whole-corpus completion, no current uploaded-test pass or novelty adjudication.','rows':[{'sha256':r['sha256'],'full_static_inspection':True,'static_inspection_complete':True,'source_executed_in_review':False,'source_imported_in_review':False,'source_compiled_in_review':False,'source_ast_parsed_in_review':False,'new_coverage_credit':r['sha256'] not in overlap,'report':'per_hash/'+r['sha256']+'.json','source_bytes':r['size_bytes'],'source_lines':r['line_count']} for r in reviews]};save('COVERAGE.json',coverage)
archive=json.loads((P/'ARCHIVE_RECONCILIATION.json').read_text());checks=json.loads((P/'ARCHIVE_CHECKSUM_RECONCILIATION.json').read_text());refs=json.loads((P/'STORED_HASH_REFERENCES.json').read_text());controls=json.loads((P/'INDEPENDENT_CONTROLS.json').read_text());oldseal=json.loads((P/'provenance/SEAL.json').read_text());manifest_ok=H((P/'provenance/SHA256SUMS.txt').read_bytes())==oldseal['manifest_sha256'];assert manifest_ok
save('INPUT_PROVENANCE.json',{'assignment':{'path':'next_review_assignment_0456_b/ASSIGNMENT.json','snapshot':'ASSIGNMENT_SNAPSHOT.json','sha256':H((P/'ASSIGNMENT_SNAPSHOT.json').read_bytes())},'batch_snapshots':[{'path':str(f.relative_to(P)),'sha256':H(f.read_bytes())} for f in sorted((P/'provenance/assigned_batches').glob('*.json'))],'frozen_inventory':{'snapshot':'provenance/CODE_COVERAGE_INVENTORY.json','sha256':H((P/'provenance/CODE_COVERAGE_INVENTORY.json').read_bytes())},'registry_before_sha256':H((P/'REGISTRY_BEFORE.json').read_bytes()),'registry_completion_sha256':H((P/'REGISTRY_AT_COMPLETION.json').read_bytes()),'registry_completion_aggregate':registry['current_full_static_reads'],'original_inventory_manifest_digest_matches':manifest_ok,'original_inventory_seal_members_all_rechecked':False,'selected_archive_roots_reopened':18,'selected_archive_source_occurrences_rehashed':119,'source_origin_unresolved_preserved':True,'central_registry_modified':False,'original_sources_modified':False,'source_execution':'none','dependency_resolution':'Candidate paths/bytes reconciled; dynamic import/runtime and binary closure not certified.'})
validation={'assigned_exact_hashes':86,'source_bytes':413910,'source_lines':9466,'source_hash_and_size_matches':86,'individual_reports':len(reviews),'all_coverage_intervals_exact':True,'overlap_with_frozen_or_completion_registry':86-len(newhash),'new_additive_coverage':len(newhash),'archives_hash_verified':len(archive),'source_archive_occurrences_verified':sum(len(a['source_occurrences']) for a in archive),'archive_checksum_entries_matched':sum(x['match'] is True for x in checks),'stored_hash_references_matched':sum(x['resolution']=='exact_member_match' for x in refs),'stored_results_preserved':52,'fresh_independent_control_records':controls['control_records'],'fresh_independent_control_groups':controls['groups'],'supplied_programs_run_imported_compiled_or_AST_parsed':False,'all_assigned_source_reads_complete':True,'whole_corpus_review_complete':False,'dependency_closure_complete':False,'novelty_adjudicated':False,'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()};save('VALIDATION.json',validation)
report=f'''# Material-extension exact-source review

## Result

All 86 assigned hashes were read first to last: 413,910 bytes and 9,466 lines. {len(newhash)} hashes are new coverage relative to the frozen inventory and completion registry. Exact source snapshots, numbered-text read receipts and individual line-referenced reviews are included. Supplied code was never executed, imported, compiled or AST-parsed. Fresh reviewer arithmetic completed 20 records in 8 control groups.

## Concrete findings and boundaries

- tests/test_algebra_fft.py lines 196–213: direct execution exits through unittest.main before defining the appended legacy import test. Discovery mode can include it (MEX-01).
- permutation_edits.py lines 7–14: uniqueness alone admits malformed bit descriptors, e.g. columns=[2] yields [0,2] at k=1. Downstream permutation-distance validation rejects that input; valid layouts are unaffected (MEX-02).
- native_shape_a2b.cpp lines 32–38: a negative raw sparse offset gives a negative C++ remainder and unsafe output index. Generic native code normalizes it. This concerns the raw ABI outside canonical prepared-plan input, not the valid update formula (MEX-03).
- Exact modular rank code uses NumPy int64. Its configured primes are safe; arbitrary larger moduli need overflow bounds (MEX-04).
- Local condition one does not survive identity padding: 100I padded by I has condition 100. This is an actual counterexample to that overgeneralized premise, not a universal FFT lower bound (MEX-05).
- Historical gauge and shrinking-prototype reports reconcile: one literal add is omitted per gauge call; cached shrinking rows still incur at least 2NG scalar repacking visits. Corrected analytic schedules remain distinct from that implementation (MEX-06).
- Trusted caches, supplied transform anchors, primitive roots, validated internal certificates and compressed modes are genuine preconditions. The reviewed source usually states them explicitly (MAT-01–10).

## What remains valid within scope

Path-Green/resolvent formulas, q-orbit boundary forcing, median cycle-flow correction and the two-impulse mixed polynomial identity survive fresh independent checks. Apparent fast paths are restricted to related inputs, detected structure, sparse forcing, fixed operator patterns, approximate normalized outputs or prepared polynomial updates. Orbit spectrum preparation is linear field work, while its online convolution remains ordinary FFT work. None of these sources establishes an unrestricted arbitrary-input full-output sub-N-log-N FFT.

Finite characteristic-zero rank obstructions are for specified recurrence architectures and shuffles. Stored gaps are 4 at N=256, 122 at N=2048 and 137 at N=4096; their arithmetic reconciles, but no imported rank oracle or flow code was rerun. Correctness and novelty are separate: no novelty priority is awarded by this static package.

## Provenance and stored evidence

18 archive roots were reopened and hash-verified. All 119 assigned source occurrences were rehashed by archive member index and name. All 110 selected archived checksum entries match. 52 result/certificate JSON snapshots are preserved; 29 embedded source/data hash references match actual archive members. Stored orbit totals reconcile to 2,254 basis cases, 1,044 spectrum points and 104 median checks. Benchmark cold totals match their rounded setup-plus-stream values; no timing claim was rerun.

Historical PASS strings, stored timings and binary availability are not current execution evidence. Source/dependency candidates were mapped and rehashed where present; dynamic import selection, installed third-party versions, native binary/source correspondence and complete transitive closure remain uncertified. Original files and central coverage registry were not modified. The inventory's original seal-manifest digest matches, but not all original inventory members were revalidated.

## Files

REVIEWS.json and per_hash/ contain every exact review. READ_EVIDENCE.json binds complete text receipts. COVERAGE.json is the additive ingestion surface. FINDINGS.json, INDEPENDENT_CONTROLS.json, DEPENDENCY_RECONCILIATION.json, ARCHIVE_RECONCILIATION.json and stored-result reconciliation files preserve the separate evidence classes. SHA256SUMS.txt and SEAL.json bind this package. This closes this assignment only, not the entire corpus.
'''
(P/'REPORT.md').write_text(report)
files=[]
for f in sorted(P.rglob('*')):
 if f.is_file() and f.name not in ('SHA256SUMS.txt','SEAL.json') or f.is_file() and f.parent!=P and f.name in ('SHA256SUMS.txt','SEAL.json'):
  b=f.read_bytes();files.append({'path':str(f.relative_to(P)),'bytes':len(b),'sha256':H(b)})
manifest=''.join(f"{r['sha256']}  {r['path']}\n" for r in files);(P/'SHA256SUMS.txt').write_text(manifest)
save('SEAL.json',{'package':P.name,'scope':'86 exact assigned full static source reads; not entire-corpus completion or uploaded execution','source_hashes':86,'source_bytes':413910,'source_lines':9466,'source_executed_in_review':False,'supplied_source_imported_compiled_or_AST_parsed':False,'new_full_read_hashes':len(newhash),'fresh_independent_control_count':20,'payload_manifest_sha256':H(manifest.encode()),'files':files})
for r in files:assert H((P/r['path']).read_bytes())==r['sha256']
print(json.dumps({'package':str(P),'new_hashes':len(newhash),'payload_files':len(files),'payload_manifest_sha256':H(manifest.encode()),'seal_sha256':H((P/'SEAL.json').read_bytes()),'validation':validation},indent=2))
