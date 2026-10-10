"""New audit-only packaging and inert data checks; never executes supplied code."""
import hashlib, json, pathlib, difflib, collections
OUT=pathlib.Path(__file__).resolve().parent
AUDIT=pathlib.Path('code_coverage_audit_0228')
MASTER=pathlib.Path('master_v22_integration_20261010/fft_research_master_20261009')
BATCH=AUDIT/'pending_batches/02_addition_0038_construction_and_source_synthesis_02.json'
def digest(b): return hashlib.sha256(b).hexdigest()
def write(name,x): (OUT/name).write_text(json.dumps(x,indent=2)+'\n')
evidence=[]
def snapshot(src,dest):
 src=pathlib.Path(src);dst=OUT/dest;dst.parent.mkdir(parents=True,exist_ok=True);raw=src.read_bytes();dst.write_bytes(raw)
 obj=dict(path=dest,source_path=str(src),sha256=digest(raw),size_bytes=len(raw));evidence.append(obj);return obj
batch=json.loads(BATCH.read_text());hs={r['sha256'] for r in batch['rows']}
assert len(hs)==8 and sum(r['size_bytes']for r in batch['rows'])==54430
snapshot(BATCH,'evidence/ASSIGNED_BATCH.json')
inventory=json.loads((AUDIT/'CODE_COVERAGE_INVENTORY.json').read_text())
current=[r for r in inventory if r['sha256'] in hs]
post=json.loads((AUDIT/'POST_V21_MAPPED_CODE.json').read_text())
reconciliation=dict(scope='Exact hash, before adding this review; name matches and mathematical acceptance not inherited',current_inventory_rows=current,post_v21_exact_hash_matches=[x for x in post if x['sha256'] in hs],coordinator_confirmation='All eight hashes remain unverified_exact_hash in the corrected current mapping; none overlaps Queue01–07 or the completed constructor10 batch.',coordinator='[review identity omitted]',current_whole_source_coverage_reused=False)
assert len(current)==8 and not reconciliation['post_v21_exact_hash_matches']
write('PRIOR_EVIDENCE_RECONCILIATION.json',reconciliation)
root=MASTER/'additions/0038_construction_and_source_synthesis/constructions/chirp_feedback'
manifest_checks=[]
for group in ['fixed_direction_completion','n5_chirp_cycle_classification','principal_restriction_extension']:
 gp=root/group
 for line in (gp/'MANIFEST.sha256').read_text().splitlines():
  sha,name=line.split(None,1);name=name.strip();actual=digest((gp/name).read_bytes());assert actual==sha
  manifest_checks.append(dict(group=group,name=name,expected_sha256=sha,actual_sha256=actual,match=True))
 for f in sorted(gp.iterdir()):
  if f.is_file() and f.suffix in {'.md','.json','.log','.csv','.sha256'}:
   snapshot(f,f'evidence/construction/{group}/{f.name}')
for name in ['review_fixed_direction_completion','review_n5_all_orders','review_principal_restriction_extension']:
 gp=root.parent.parent/'reviews'/name
 for n in ['REVIEW.md','REPRODUCE.md','SOURCE_PROVENANCE.json','SOURCE_CERTIFICATE_COMPARISON.json','PORTABILITY.json','SEALED_MANIFEST.json','SEALED_MANIFEST.sha256']:
  f=gp/n
  if f.exists():snapshot(f,f'evidence/independent_reviews/{name}/{n}')
snapshot('construction_source_code_review_0241/COVERAGE.json','evidence/DEPENDENCY_PRIOR_COVERAGE.json')
helperhash='3f2d3e66aa8df8207998c0d56fea0528d7e02ec4bec5546c13d1fc102504e871'
deps=[]
for p in [pathlib.Path('research_round_2156/projective_row_gate/check_projective_gate.py'),root/'n5_chirp_cycle_classification/_projective_gate_helpers.py']:
 actual=digest(p.read_bytes());assert actual==helperhash;deps.append(dict(path=str(p),sha256=actual,static_read_reused_from='evidence/DEPENDENCY_PRIOR_COVERAGE.json',read_as_code_this_review=False,executed_this_review=False))
write('DEPENDENCIES.json',deps)
sections=[[(1,7,'header and dynamic dependency initialization'),(8,44,'structural directions and Green guards'),(45,101,'sparse sandwich and affine graph completion'),(102,151,'cyclic scans and reconstruction'),(152,193,'directional checks and positive fixtures'),(194,227,'negative fixtures and output')],[(1,7,'local dependency initialization'),(8,44,'structural directions and guards'),(45,101,'sparse sandwich and graph solver'),(102,151,'scan and reconstruction'),(152,193,'directional and positive fixtures'),(194,227,'negative fixtures and main')],[(1,27,'dependency, rank and determinant'),(28,40,'limit directions and augmented matrix'),(41,68,'eight N5 controls, N3 minors and output')],[(1,4,'dependency and saved input'),(5,22,'transport graph and domains'),(23,29,'survivor traversal and output')],[(1,41,'extension arithmetic, import and data'),(42,56,'projective root enumeration'),(57,92,'exact elimination helpers'),(93,142,'complete fixed branch traversal, minor and gauge checks'),(143,146,'summary and output')],[(1,11,'target and cycle universe'),(12,22,'576 row subsystems, results and output')],[(1,17,'inputs, cycle catalogue and exact target'),(18,32,'saved branch metadata consistency'),(33,45,'CSV indices and hard-coded summary claims')],[(1,40,'dense matrix primitives and restriction'),(41,71,'Green and mask controls'),(72,115,'Gauss roots, diagnostic fields and target blocks'),(116,138,'chirp, square and resonance controls'),(139,155,'modular family samples and output')]]
findings=[['dense_verification_not_query_counter','assertion_sensitive_acceptance','fixed_direction_not_unrestricted_search','absolute_dependency_path','prime_field_parameter_enumeration'],['local_dependency_near_version','assertion_sensitive_acceptance','extension_parameter_enumeration_bounded','no_standalone_run_receipt'],['necessary_boundary_controls_only','eight_not_twelve_N5_controls','dense_fixture_arithmetic','top_level_output_side_effect'],['trusted_intermediate_data','N5_only','singular_transition_assertion','top_level_output_side_effect'],['fixed_exclusion_fixture','computed_nonzero_minors','two_roots_per_component_assumption','continuous_columns_reported','top_level_output_side_effect'],['row_subsystem_survival_not_full_completion','factorial_cycle_enumeration','N5_only','top_level_output_side_effect'],['metadata_consistency_not_independent_verifier','determinants_and_ranks_not_recomputed','literal_summary_fields','assertion_sensitive_acceptance','top_level_output_side_effect'],['bounded_finite_controls_not_infinite_proof','dense_setup_and_field_preparation','invalid_subset_not_prevalidated','sympy_dependency','top_level_output_side_effect']]
log_map={
 'check_scale_completion.py':('fixed_direction_completion','CHECK_RUN.log','FIXED_DIRECTION_RESULTS.json'),
 '_scale_completion_helpers.py':('n5_chirp_cycle_classification','COMPLETION_SCREEN.log','COMPLETION_SCREEN_RESULTS.json'),
 'check_minor_positive_controls.py':('n5_chirp_cycle_classification','MINOR_POSITIVE_CONTROLS.log','MINOR_POSITIVE_CONTROLS.json'),
 'inspect_domains.py':('n5_chirp_cycle_classification','SURVIVOR_DOMAINS.log','SURVIVOR_DOMAINS.json'),
 'screen_completions.py':('n5_chirp_cycle_classification','COMPLETION_SCREEN.log','COMPLETION_SCREEN_RESULTS.json'),
 'screen_orders.py':('n5_chirp_cycle_classification','ORDER_SCREEN.log','ORDER_SCREEN_RESULTS.json'),
 'summarize_classification.py':('n5_chirp_cycle_classification','CLASSIFICATION_SUMMARY.log','CLASSIFICATION_SUMMARY.json'),
 'check_restriction_extension.py':('principal_restriction_extension','CHECK_RUN.log','RESTRICTION_EXTENSION_RESULTS.json')}
rows=[];historical=[]
for ix,r in enumerate(batch['rows']):
 raw=pathlib.Path(r['local_content']).read_bytes();sha=digest(raw);assert sha==r['sha256'] and len(raw)==r['size_bytes']
 original=MASTER/r['representative_path'];assert digest(original.read_bytes())==sha
 snap=snapshot(r['local_content'],f'inert_source_snapshots/{sha}.txt');lines=len(raw.splitlines());assert sections[ix][-1][1]==lines
 name=pathlib.Path(r['representative_path']).name;group,log,result=log_map[name]
 hist=dict(sha256=sha,kind='reported authored-run declaration and package-bound control artifact' if ix!=1 else 'intended imported helper; caller output artifact only',log_path=f'evidence/construction/{group}/{log}',result_path=f'evidence/construction/{group}/{result}',manifest_path=f'evidence/construction/{group}/MANIFEST.sha256',fresh_run_here=False,exact_command_and_exit_receipt_reconstructed=False,exact_historical_executing_source_attested=False,standalone_main_run_established=False if ix==1 else None,sealed_controls_not_a_substitute_for_source_read=True,independent_review_did_not_execute_constructor=True)
 historical.append(hist)
 rows.append(dict(sha256=sha,size_bytes=len(raw),line_count=lines,original_master_path=r['representative_path'],master_path=str(original),occurrences=r['occurrences'],origin='constructor/reviewer authored',origin_detail='newly authored constructor/control/reporting utility; not an original uploaded implementation',origin_evidence=[f'evidence/construction/{group}/MANIFEST.sha256']+[x['path']for x in evidence if x['path'].startswith(f'evidence/construction/{group}/')and x['path'].endswith('.md')],source_snapshot=snap,status='new_full_static_read_completed',full_static_read=True,static_inspection_complete=True,current_review_complete_read=True,method='Complete inert source reading and reasoning; no source execution/import/compile/AST parsing',extent=dict(lines=[1,lines],all_bytes_accounted=True,prior_read_inherited=False,current_read_sections=[dict(start_line=a,end_line=b,subject=s)for a,b,s in sections[ix]]),source_execution=False,current_audit_uploaded_execution='none',recorded_execution=False,recorded_execution_note='No exact historical command/exit/source-hash execution receipt reconstructed; preserve separately the reported authored-run artifacts',historical_execution_evidence=hist,finding_tags=findings[ix],scope_and_findings=findings[ix],precision='Exact modular arithmetic and metadata; no floating stability or bit-complexity certification',report='REVIEW.md'))
assert sum(r['line_count']for r in rows)==919
write('COVERAGE.json',dict(review='constructor_batch2_static_review_0249',scope='Exact-hash complete static inspection, no supplied-code execution',source_execution=False,rows=rows))
write('HISTORICAL_EVIDENCE.json',historical)
write('MANIFEST_DATA_CHECKS.json',manifest_checks)
a=(OUT/'inert_source_snapshots'/f"{rows[0]['sha256']}.txt").read_text().splitlines(True);b=(OUT/'inert_source_snapshots'/f"{rows[1]['sha256']}.txt").read_text().splitlines(True)
(OUT/'EXACT_NEAR_VERSION_DIFF.txt').write_text(''.join(difflib.unified_diff(a,b,fromfile=rows[0]['sha256'],tofile=rows[1]['sha256'])))
# Newly authored data-only crosschecks, not a replay of any supplied program.
cdir=root/'n5_chirp_cycle_classification'
order=json.loads((cdir/'ORDER_SCREEN_RESULTS.json').read_text());domain=json.loads((cdir/'SURVIVOR_DOMAINS.json').read_text());comp=json.loads((cdir/'COMPLETION_SCREEN_RESULTS.json').read_text());pos=json.loads((cdir/'MINOR_POSITIVE_CONTROLS.json').read_text());summary=json.loads((cdir/'CLASSIFICATION_SUMMARY.json').read_text())
data_checks=dict(description='Counts and metadata from inert saved artifacts; no determinant/rank arithmetic or source program replay',row_result_records=len(order['results']),distinct_pairs=len({(x['first'],x['second'])for x in order['results']}),survivor_pairs=len(order['survivors']),domain_pairs=len(domain),completion_branches=len(comp['branches']),branch_status_counts=dict(collections.Counter(x['status']for x in comp['branches'])),saved_rank_pairs=dict(collections.Counter(str((x['rank_scale'],x['rank_augmented']))for x in comp['branches'])),N5_positive_controls=len(pos['genuine_N5_controls']),N3_minor_count=pos['N3_all_7_by_7_minors_checked'],summary_status=summary['status'],all_manifest_entries_match=True,manifest_entries_verified=len(manifest_checks),supplied_source_executed=False)
assert (data_checks['row_result_records'],data_checks['distinct_pairs'],data_checks['survivor_pairs'],data_checks['domain_pairs'],data_checks['completion_branches'])==(576,576,192,192,624)
assert data_checks['branch_status_counts']=={'REJECT:off_support_entry':480,'REJECT:conflicting_linear_pins':144}
assert data_checks['N5_positive_controls']==8 and data_checks['N3_minor_count']==36
write('INERT_DATA_CHECKS.json',data_checks)
write('EVIDENCE_INDEX.json',evidence)
write('SUMMARY.json',dict(status='complete',hashes=8,bytes=54430,lines=919,new_full_static_reads=8,reused_prior_full_reads=0,supplied_code_execution=False,source_modification=False,authorship='all eight constructor/control or reporting utilities',exact_historical_run_receipts_reconstructed=0,report='REVIEW.md',coverage='COVERAGE.json',data_checks='INERT_DATA_CHECKS.json'))
# Rehash untouched inputs at finish.
checks=[]
for r in rows:
 for path in [AUDIT/'code_bytes'/r['sha256'],pathlib.Path(r['master_path'])]:
  actual=digest(path.read_bytes());assert actual==r['sha256'];checks.append(dict(path=str(path),sha256=actual,unchanged=True))
write('SOURCE_PRESERVATION.json',checks)
seal={str(p.relative_to(OUT)):digest(p.read_bytes())for p in sorted(OUT.rglob('*'))if p.is_file()and p.name not in ['SEALED_MANIFEST.json','SEALED_MANIFEST.sha256']}
write('SEALED_MANIFEST.json',dict(review='constructor_batch2_static_review_0249',files=seal))
sealraw=(OUT/'SEALED_MANIFEST.json').read_bytes();(OUT/'SEALED_MANIFEST.sha256').write_text(f'{digest(sealraw)}  SEALED_MANIFEST.json\n')
# Verify written seal immediately with the independent standard-library routine above.
assert all(digest((OUT/name).read_bytes())==sha for name,sha in seal.items())
print(json.dumps(dict(status='sealed',hashes=len(rows),bytes=sum(r['size_bytes']for r in rows),lines=sum(r['line_count']for r in rows),sealed_files=len(seal),manifest_sha256=digest(sealraw),inert_manifest_entries_verified=len(manifest_checks)),indent=2))
