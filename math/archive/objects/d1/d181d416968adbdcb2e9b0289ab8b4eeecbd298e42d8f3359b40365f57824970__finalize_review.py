"""Fresh report/coverage/seal builder for an inert source audit."""
import pathlib,json,hashlib,shutil,datetime,collections
P=pathlib.Path(__file__).parent
H=lambda b:hashlib.sha256(b).hexdigest()
def save(name,obj):(P/name).write_text(json.dumps(obj,indent=2)+'\n')
rows=json.loads((P/'SOURCE_MANIFEST.json').read_text())
assignment=json.loads((P/'ASSIGNMENT_SNAPSHOT.json').read_text())
registry=pathlib.Path('post_v22_review_registry_0308/ADDITIVE_CODE_COVERAGE.json')
shutil.copyfile(registry,P/'REGISTRY_AT_COMPLETION.json')
inv=json.loads((P/'INVENTORY_SNAPSHOT.json').read_text())
reg=json.loads((P/'REGISTRY_AT_COMPLETION.json').read_text())
prior={r['sha256'] for r in inv if r.get('static_inspection_complete')}|{r['sha256'] for r in reg['rows']}
overlap=[r['sha256'] for r in rows if r['sha256'] in prior]
assert not overlap,overlap
findings=[
 {'id':'F01','title':'Weyl callback verifier accepts empty output vectors','source_indices':[57],'severity':'concrete verifier false acceptance','detail':'Output shape is never checked. An empty result satisfies seed universal predicate and produces no zipped defects, yielding passes=true for a non-N-vector callback. Probability bound requires a fixed valid linear map and independent uniform samples. Fresh logical control C01 confirms the vacuity without invoking source. Underlying Weyl characterization remains valid in its stated domain.'},
 {'id':'F02','title':'Direct-script test entrypoints omit appended classes','source_indices':[6,7,53,77],'severity':'invocation-dependent coverage gap','detail':'unittest.main appears before later classes in four files, omitting eleven methods in total under direct execution. Imported discovery includes them; archived logs explicitly name these later methods, so historical recorded runs are not negated. C02 records exact lines/methods/log hashes.'},
 {'id':'F03','title':'Some validators trust stored claims or permit omitted records','source_indices':[21,31,32,35,39,42,46,54,58,66,89],'severity':'validation completeness and freshness','detail':'Examples: phase12 verify_all checks cached ranks/booleans rather than recalculating matrices and only parses thresholds.json; phase35 saved-polynomial loops can be empty; separator ordinary-record check can be vacuous; optional numerical audit copied without freshness check; fixed test counts not discovered. Actual phase35 archived certificates N8/N16 are present, and three archived Fourier/Green witnesses independently reconcile. This does not establish actual false stored theorem data.'},
 {'id':'F04','title':'Root helper does not verify exact order for custom generators','source_indices':[29],'severity':'public parameter boundary','detail':'primitive_root_of_order checks w^n=1 only. C03 gives p17,n4,generator1 producing w1 of order1. Intended default prime/generator examples are not contradicted.'},
 {'id':'F05','title':'Floating diagnostics and cost proxies retain restricted meaning','source_indices':[9,11,12,24,33,35,37,38,50,55,62,65,72,73,76,82,83,87,88,93,96],'severity':'scope/accounting/precision limitation','detail':'Float spectral/rank/tail checks are not interval certificates; planner total-minus-head can erase tiny mass (C04); Frobenius-optimal scalar need not be spectral-optimal; arithmetic/word proxies exclude stated setup, bit-width or verification work. Prime-free ring widths grow; approximate and structured-input results do not establish generic exact sub-NlogN FFT or unit-word cost.'},
 {'id':'F06','title':'Joint-orbit ZIP packaging is payload-consistent but not byte-reproducible','source_indices':[75],'severity':'reproducibility metadata','detail':'ZipFile.write retains filesystem metadata; equal payloads with different timestamps need not have the same archive hash. C07 confirms independently. Fixed file list and post-write payload hashes otherwise avoid stale self-manifest duplication.'}
]
save('FINDINGS.json',findings)
reviews=[]
read_batches=[(1,7,'796124'),(8,13,'cdf94a'),(14,20,'5910d2'),(21,25,'101695'),(26,27,'8989c8'),(28,28,'101695'),(29,35,'984065'),(36,39,'e5b681'),(40,46,'037018'),(47,52,'dbaf41'),(53,57,'b96265'),(58,64,'8e67ff'),(65,71,'361f31'),(72,77,'78df6f'),(78,81,'5f6fa0'),(82,88,'255a6a'),(89,93,'45fe96'),(94,96,'836702')]
receipts=[]
for r in rows:
 b=(P/'sources'/r['sha256']).read_bytes();assert len(b)==r['size_bytes'] and H(b)==r['sha256']
 assert pathlib.Path(r['local_content']).read_bytes()==b
 lines=b.decode().splitlines()
 q=json.loads((P/'per_hash'/f"{r['sha256']}.json").read_text())
 assert q['static_inspection_complete'] and q['full_static_inspection']
 assert q['coverage_intervals']=={'bytes_half_open':[[0,len(b)]],'lines_inclusive':[[1,len(lines)]]}
 q['finding_ids']=[f['id'] for f in findings if r['index'] in f['source_indices']]
 q['first_last_read_evidence']={'first_line':lines[0],'last_line':lines[-1],'last_nonempty_line':next(x for x in reversed(lines) if x.strip()),'source_bytes_sha256':H(b),'total_lines':len(lines),'direct_read_tool_chunk':next(c for lo,hi,c in read_batches if lo<=r['index']<=hi)}
 q['stored_integrity_reconciliation']='STORED_INTEGRITY_RECONCILIATION.json gives manifest/source declarations; historical outputs not current execution.'
 save('per_hash/'+r['sha256']+'.json',q);reviews.append(q)
 receipts.append({'index':r['index'],'sha256':r['sha256'],'size_bytes':len(b),'line_count':len(lines),'coverage_intervals':q['coverage_intervals'],'full_read_evidence':q['first_last_read_evidence'],'direct_read_complete':True})
save('READ_RECEIPTS.json',{'method':'First-to-last direct inert source text reading with line numbers; no supplied execution/import/compile/AST parsing. Initial source26/27 display was truncated and both were reread completely in chunk8989c8. Other listed ranges were complete.','rows':receipts})
save('REVIEWS.json',reviews)
coverage={
 'assigned_batches':assignment['batch_names'],
 'assigned_batch_hashes':{n:H((P/'provenance/assigned_batches'/n).read_bytes()) for n in assignment['batch_names']},
 'fully_read_hashes_this_review':len(rows),'new_full_read_hashes':len(rows),'previously_covered_hashes':[],
 'total_source_bytes_read':sum(x['size_bytes'] for x in rows),'total_source_lines_read':sum(x['line_count'] for x in rows),
 'all_assigned_source_reads_complete':True,'all_research_material_checks_finished':False,'dependency_closure_complete':False,
 'source_execution':'No supplied source run, imported, compiled or AST-parsed. Eight fresh independent controls executed separately.',
 'scope_note':'Exact assigned source coverage only, not whole corpus, runtime dependency/data closure, all mathematical claims or originality.',
 'rows':[{k:q[k] for k in ['index','sha256','size_bytes','representative_path','snapshot_path','static_inspection_complete','full_static_inspection','inspection_method','coverage_intervals','provenance','source_executed_in_review','source_imported_in_review','source_compiled_in_review','source_ast_parsed_in_review','finding_ids']} for q in reviews]
}
save('COVERAGE.json',coverage)
save('SKIPPED_ALREADY_REVIEWED.json',[])
archive=json.loads((P/'ARCHIVE_PROVENANCE.json').read_text())
source_occ=json.loads((P/'SOURCE_OCCURRENCE_CHECKS.json').read_text())
integrity=json.loads((P/'STORED_INTEGRITY_RECONCILIATION.json').read_text())
istats=dict(collections.Counter(x['resolution_status'] for x in integrity))
controls=json.loads((P/'INDEPENDENT_CONTROLS.json').read_text())
oldseal=json.loads((P/'provenance/ORIGINAL_INVENTORY_SEAL.json').read_text())
oldmanifest=H((P/'provenance/ORIGINAL_INVENTORY_SHA256SUMS.txt').read_bytes())
assert oldmanifest==oldseal['manifest_sha256']
save('INPUT_PROVENANCE.json',{
 'assignment':{'path':'next_review_assignment_0456_a/ASSIGNMENT.json','sha256':H((P/'ASSIGNMENT_SNAPSHOT.json').read_bytes())},
 'frozen_inventory':{'snapshot':'INVENTORY_SNAPSHOT.json','sha256':H((P/'INVENTORY_SNAPSHOT.json').read_bytes()),'full_static_reads':sum(bool(x.get('static_inspection_complete')) for x in inv)},
 'additive_registry_start':{'snapshot':'REGISTRY_BEFORE.json','sha256':H((P/'REGISTRY_BEFORE.json').read_bytes())},
 'additive_registry_completion':{'path':str(registry),'snapshot':'REGISTRY_AT_COMPLETION.json','sha256':H((P/'REGISTRY_AT_COMPLETION.json').read_bytes()),'current_full_static_reads':reg['current_full_static_reads']},
 'archive_provenance':{'exact_containers_verified':len(archive),'source_occurrences_verified':len(source_occ),'detail':'ARCHIVE_PROVENANCE.json and SOURCE_OCCURRENCE_CHECKS.json','all_recorded_root_ancestors_revalidated':False},
 'stored_evidence':{'record_count':len(json.loads((P/'STORED_OUTPUTS_INDEX.json').read_text())),'digest_reference_results':istats,'missing_reference_interpretation':'Fourteen referenced external/earlier input filenames are not present in the same container. No substitution by filename similarity; no full external closure claimed.'},
 'original_inventory_seal':{'declared_manifest_sha256':oldseal['manifest_sha256'],'observed_manifest_sha256':oldmanifest,'manifest_digest_matches':True,'all_inventory_members_revalidated':False},
 'source_provenance':'All occurrence, Library archive identity, root-archive and unresolved-origin labels preserved verbatim in SOURCE_MANIFEST.json. Existing import-reference/AST metadata is inherited inventory data; no syntax/AST parse performed by this review.',
 'seal_distinction':'This package seal binds new review snapshots and conclusions; original manifest matches authenticate archived bytes, not historic executions or mathematical validity.',
 'central_registry_modified_by_this_review':False,'previous_packages_modified':False})
validation={
 'assigned_new_exact_hashes':len(rows),'source_bytes':sum(r['size_bytes'] for r in rows),'source_lines':sum(r['line_count'] for r in rows),
 'source_hash_size_matches':len(rows),'individual_reports':len(reviews),'all_coverage_intervals_exactly_cover_source':True,
 'duplicate_hashes_in_new_coverage':len(rows)-len({r['sha256'] for r in rows}),'overlap_with_frozen_inventory_or_completion_registry':len(overlap),
 'original_source_bytes_unchanged':True,'exact_archive_containers_verified':len(archive),'source_archive_occurrences_verified':len(source_occ),
 'original_inventory_manifest_digest_matches':True,'stored_digest_references':istats,
 'fresh_independent_controls_passed':controls['count'],'supplied_programs_run_imported_compiled_or_AST_parsed':False,
 'all_assigned_source_reads_complete':True,'whole_corpus_review_complete':False,'external_dependency_data_closure_complete':False,
 'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()
}
save('VALIDATION.json',validation)
print(json.dumps(validation))
