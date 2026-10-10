"""Fresh reviewer sealing/checking tool; no supplied code execution."""
import json,hashlib,shutil
from pathlib import Path
O=Path(__file__).parent;name=O.name;now='2026-10-10T05:35:33Z';R=json.load(open(O/'ASSIGNED_SOURCES.json'));S=json.load(open(O/'SOURCE_REVIEWS.json'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(O/n).write_text(json.dumps(d,indent=2)+'\n')
# Copy rather than modify the changing central registry.
shutil.copy2('post_v22_review_registry_0308/ADDITIVE_CODE_COVERAGE.json',O/'REGISTRY_END_SNAPSHOT.json')
start=json.load(open(O/'REGISTRY_START_SNAPSHOT.json'));end=json.load(open(O/'REGISTRY_END_SNAPSHOT.json'));inv=json.load(open(O/'INVENTORY_SNAPSHOT.json'));base={r['sha256']for r in inv if r.get('static_inspection_complete')};before=base|{r['sha256']for r in start['rows']};after=base|{r['sha256']for r in end['rows']};assigned={r['sha256']for r in R}
assert len(assigned)==25 and sum(r['size_bytes']for r in R)==109783
for r in R:
 assert sha(Path(r['local_content']))==r['sha256']==sha(O/'sources'/r['sha256'])
 assert len((O/'sources'/r['sha256']).read_bytes())==r['size_bytes']
for r in S:
 assert r['lines']==r['read_scope']['last_line'] and r['read_scope']['first_line']==1
 assert all(r['read_scope'][k]is False for k in ['source_executed','source_imported','source_compiled','source_AST_parsed'])
assert sum(r['lines']for r in S)==2449
write('ASSIGNMENT.json',{'batch_directory':'remaining_source_queue_0502','batch_names':['batch_05.json'],'batch_sha256':sha(O/'ASSIGNED_BATCH.json'),'source_hash_count':25,'source_bytes':109783,'scope':'Complete first-to-last inert reading, exact byte/archive provenance, per-source line findings, dependency and stored-output reconciliation. No supplied execution, import, compilation, or AST parsing. No automatic mathematical/novelty certification.'})
write('DEDUPLICATION.json',{'frozen_inventory_full_static_reads':len(base),'starting_registry_total':start['current_full_static_reads'],'ending_registry_total':end['current_full_static_reads'],'assigned_unique_hashes':25,'overlap_at_start':sorted(assigned&before),'overlap_at_end':sorted(assigned&after),'new_coverage_credit_at_seal':len(assigned-after),'start_registry_sha256':sha(O/'REGISTRY_START_SNAPSHOT.json'),'end_registry_sha256':sha(O/'REGISTRY_END_SNAPSHOT.json'),'inventory_sha256':sha(O/'INVENTORY_SNAPSHOT.json'),'central_registry_modified_by_this_review':False})
write('READ_DISPLAY_LOG.json',{'read_method':'Full line-numbered inert text display, no source execution/import/compilation/AST. All source-display outputs were complete rather than truncated.','groups':[{'source_indices':list(range(0,4)),'line_scope':'first to last for each source'},{'source_indices':list(range(4,9)),'line_scope':'first to last for each source'},{'source_indices':list(range(9,20)),'line_scope':'first to last for each source'},{'source_indices':[20,21,22],'line_scope':'first to last for each source'},{'source_indices':[23],'line_ranges':[[1,240],[241,438]]},{'source_indices':[24],'line_ranges':[[1,232]]}],'total_source_lines':2449,'source_hash_count':25})
evidence_sha=sha(O/'SOURCE_REVIEWS.json')
rows=[{'review_id':r['review_id'],'sha256':r['sha256'],'representative_path':r['representative_path'],'batch':'batch_05.json','bytes':r['bytes'],'lines':r['lines'],'full_static_inspection':True,'static_inspection_complete':True,'full_source_read':True,'line_ranges':[[1,r['lines']]],'source_executed_in_review':False,'evidence_file':'SOURCE_REVIEWS.json','evidence_sha256':evidence_sha,'snapshot':r['source_snapshot'],'new_coverage_credit':r['sha256']not in after}for r in S]
write('COVERAGE.json',{'package':name,'completed_utc':now,'assigned_batches':['batch_05.json'],'assigned_batch_hashes':25,'fully_read_hashes_this_review':25,'new_full_read_hashes':len(assigned-after),'new_coverage_credit':len(assigned-after),'previously_covered_hashes':len(assigned&after),'total_source_bytes_read':109783,'total_source_lines_read':2449,'all_assigned_new_source_reads_complete':True,'complete_assignment_review':True,'all_research_material_checks_finished':False,'dependency_closure_complete':False,'mathematical_or_novelty_certification':False,'source_execution':'none','source_import_compilation_syntax_parse':'none','scope_note':'Complete first-to-last inert inspection of all 25 assigned exact hashes; fresh reviewer metadata and independent arithmetic only. Historical outputs remain labeled historical. No central registry change.','rows':rows})
write('ORIGINAL_PRESERVATION_CHECK.json',{'source_original_hashes_reverified':25,'source_originals_unchanged':True,'prior_sealed_packages_modified':False,'central_registry_modified':False,'writes_limited_to_this_new_package':True})
# Seal all package files except the manifest/seal themselves.
files=sorted(p for p in O.rglob('*')if p.is_file()and p.name not in ['SHA256SUMS.txt','SEAL.json'])
(O/'SHA256SUMS.txt').write_text(''.join(sha(p)+'  '+str(p.relative_to(O))+'\n'for p in files))
for line in (O/'SHA256SUMS.txt').read_text().splitlines():
 h,rel=line.split('  ',1);assert sha(O/rel)==h
write('SEAL.json',{'package':name,'sealed_utc':now,'file_count':len(files),'sealed_bytes':sum(p.stat().st_size for p in files),'sha256sums_sha256':sha(O/'SHA256SUMS.txt'),'coverage_sha256':sha(O/'COVERAGE.json'),'source_reviews_sha256':evidence_sha,'assigned_sources':25,'source_bytes':109783,'source_lines':2449,'new_coverage_credit':len(assigned-after),'uploaded_source_execution':'none','uploaded_source_import_compile_AST':'none','central_registry_modified':False,'fresh_reviewer_check_groups':18,'fresh_F8_matrix_entries':64,'fresh_F8_minor_matrices':16072,'fresh_F16_matrix_entries':256,'all_package_digest_checks_passed':True})
print((O/'SEAL.json').read_text());print('Seal SHA256',sha(O/'SEAL.json'))
