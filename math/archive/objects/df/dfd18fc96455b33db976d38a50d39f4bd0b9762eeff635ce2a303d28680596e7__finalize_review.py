"""Seal this review and reconcile metadata; does not execute supplied sources."""
import json,pathlib,hashlib,datetime,collections
O=pathlib.Path('fusion_phase_source_review_0408'); S=pathlib.Path('[local workspace]')
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(name,data): (O/name).write_text(json.dumps(data,indent=2)+'\n')
rows=json.loads((O/'INPUT_ROWS.json').read_text());reports=json.loads((O/'SOURCE_REPORTS.json').read_text());base=json.loads((O/'BASELINE_MANIFEST.json').read_text());ev=json.loads((O/'EVIDENCE_MANIFEST.json').read_text());wanted={r['sha256'] for r in rows};now=datetime.datetime.now(datetime.timezone.utc).isoformat()
# All completed-coverage documents are searched for assigned hashes, irrespective of schema.
def hits(v):
 out=[]
 if isinstance(v,dict):
  h=v.get('sha256',v.get('source_sha256',v.get('content_sha256')))
  if h in wanted:out.append(v)
  for x in v.values():out.extend(hits(x))
 elif isinstance(v,list):
  for x in v:out.extend(hits(x))
 return out
curpaths=[S/'code_coverage_audit_0228/CODE_COVERAGE_INVENTORY.json',S/'post_v22_review_registry_0308/ADDITIVE_CODE_COVERAGE.json']+sorted(p for p in S.rglob('COVERAGE.json') if O not in p.parents)
cur=[];mentions=collections.defaultdict(list);(O/'completion_baseline').mkdir(exist_ok=True)
for p in curpaths:
 b=p.read_bytes();h=sha(b);snap='completion_baseline/'+h+'.json';(O/snap).write_bytes(b);cur.append({'path':str(p),'sha256':h,'snapshot':snap,'bytes':len(b)})
 for r in hits(json.loads(b)):
  mentions[r.get('sha256',r.get('source_sha256',r.get('content_sha256')))].append({'path':str(p),'record':r})
# None of these hashes appears in any completed coverage at the completion point.
# Frozen inventory rows exist but explicitly have static_inspection_complete=false.
dedup=[]
for r in rows:
 mm=mentions[r['sha256']];prev=[x for x in mm if pathlib.Path(x['path']).name!='CODE_COVERAGE_INVENTORY.json']
 inv=[x for x in mm if pathlib.Path(x['path']).name=='CODE_COVERAGE_INVENTORY.json']
 prior_full=any(x['record'].get('static_inspection_complete') or x['record'].get('full_static_inspection') for x in inv)
 # Any other matching document needs manual reconciliation; do not silently give double credit.
 assert not prev, ('Concurrent matching coverage needs review',r['sha256'],prev)
 dedup.append({'sha256':r['sha256'],'frozen_inventory_full_static_inspection':prior_full,'matching_completed_coverage':prev,'new_coverage_credit':not prior_full})
assert len(dedup)==45 and all(x['new_coverage_credit'] for x in dedup)
dump('COMPLETION_BASELINE_MANIFEST.json',{'checked_at_utc':now,'sources':cur})
old={e['path']:e for e in base['coverage_sources']};new={e['path']:e for e in cur}
drift={'baseline_capture_utc':base['captured_at_utc'],'completion_check_utc':now,'authorized_concurrent_baseline_changes':[{'path':p,'before_sha256':old[p]['sha256'],'after_sha256':new[p]['sha256']} for p in old.keys()&new.keys() if old[p]['sha256']!=new[p]['sha256']],'new_coverage_documents':[new[p] for p in new.keys()-old.keys()],'missing_previous_coverage_documents':[old[p] for p in old.keys()-new.keys()],'original_source_drift':[],'note':'Mutable registry/integration metadata drift is distinct from original source drift. This worker made no central-registry edits.'}
orig=json.loads((O/'ORIGINAL_SOURCE_MANIFEST.json').read_text());pres=[]
for x in orig:
 p=pathlib.Path(x['path']);actual=sha(p.read_bytes()) if p.is_file() else None;good=actual==x['expected_sha256'];pres.append({**x,'completion_sha256':actual,'preserved':good})
 if not good:drift['original_source_drift'].append(pres[-1])
# Also verify all local source snapshots and preserved evidence bytes against captured hashes.
snapcheck=[{'path':r['snapshot'],'sha256':sha((O/r['snapshot']).read_bytes()),'matches':sha((O/r['snapshot']).read_bytes())==r['sha256']} for r in rows]
evidencecheck=[{'path':e['path'],'snapshot':e['snapshot'],'source_preserved':pathlib.Path(e['path']).is_file() and sha(pathlib.Path(e['path']).read_bytes())==e['sha256'],'snapshot_preserved':sha((O/e['snapshot']).read_bytes())==e['sha256']} for e in ev]
assert all(p['preserved'] for p in pres) and all(x['matches'] for x in snapcheck) and all(x['source_preserved'] and x['snapshot_preserved'] for x in evidencecheck)
dump('BASELINE_DRIFT.json',drift);dump('ORIGINAL_PRESERVATION_CHECK.json',{'checked_at_utc':now,'all_original_sources_preserved':True,'source_locations_checked':len(pres),'sources':pres,'source_snapshots':snapcheck,'evidence':evidencecheck,'baseline_drift_record':'BASELINE_DRIFT.json'})
dump('DEDUP_RECONCILIATION.json',{'baseline_sources':len(base['coverage_sources']),'completion_sources':len(cur),'method':'Exact SHA-256 only; no basename/AST/role-only credit. Frozen full flags and every completed COVERAGE recursively searched; latest registry read again.','assigned_hashes':45,'new_hashes':45,'prior_full_hashes':0,'rows':dedup})
findings=[
 {'id':'F01','classification':'actual_archived_evidence_incompleteness','sources':[40,42],'title':'Saved experiment JSON omits an unconditional current-source section','detail':'run_experiments.py lines30-39 unconditionally adds bitrev_all_widths. Saved EXPERIMENT_RESULTS.json lacks it although both source/output hashes match the embedded manifest. No credit for a saved all-width sweep; existing sections retained. No gate/theorem invalidation inferred.'},
 {'id':'F02','classification':'actual_archived_numeric_failures','sources':[21,22,25,26],'title':'Six valid v14 benchmark rows fail binary64 stability threshold','detail':'Stored CSV has 15 rows, nine stable and six unstable: (1009,100),(2039,121),(4093,144),(8191,169),(16381,28),(16381,196). First has error8.6606e214, four are inf, and (16381,28) has1.7981e-5 against1e-5 threshold. Algebraic exactness remains separate; source explicitly disclaims stability.'},
 {'id':'F03','classification':'potential_invocation_failure_archived_runs_unaffected','sources':[13,36],'title':'Early unittest.main skips later tests on direct execution','detail':'Twisted direct script sees5 instead of11 groups; Phase28 direct script sees10 instead of17. Archived runbooks use module/discovery and logs include all 11/all 17. Thus no archived run invalidation.'},
 {'id':'F04','classification':'unsupported_input_correctness_defect','sources':[5,9],'title':'Unvalidated cycle/permutation assumptions','detail':'direct_green overwrites visits for shorter cycles. Hand derivation n4,p17,alpha2,identity successor gives4I instead of16I. Generated archived Hamiltonian cases and shift controls are unaffected. GreenTerm order/dimensions also lack full validation.'},
 {'id':'F05','classification':'accepted_parameter_helper_defect_no_archived_failure','sources':[23,26],'title':'Variance row-count bound can overflow before its cap','detail':'For p in[1/4,1/2), 2^r*p^((r+1)/2) does not decay, but helper only rejects p>=1/2 and evaluates floating2**r until overflow. Positive tolerance/nonnegative variance/positive partition guards are incomplete. No supplied helper executed and no failure of archived smaller-p calls claimed.'},
 {'id':'F06','classification':'cost_scope_qualification','sources':[17,19],'title':'Complete separate scans need a Q*M term','detail':'Generic cost is O(Q log Q+Q*M). O(Q log Q) summary is valid in intended M=O(log Q) regime, not every accepted divisor. Theta(Q*M) labels also omit possible Q log K domination outside that regime.'},
 {'id':'F07','classification':'verification_scope_boundary','sources':[34,35,36,37,45],'title':'Saved exact-field certificates have bounded and provenance-dependent scope','detail':'All three stored Bezout coefficient identities independently verified; matrix-polynomial derivation and characteristic-zero lifting not re-executed/re-proved. v15 full-basis coverage exists onlyQ56/Q119;Q136/Q238 use24 basis vectors plus6 dense vectors.'},
 {'id':'F08','classification':'dependency_and_packaging_boundary','sources':[1,2,14,28,34,35,36,37,44],'title':'Exact dependency identities are not new whole-source review','detail':'Adjacent modules and inherited archive members hashed/snapshotted; core dependency text not fully newly reviewed unless it belongs to assigned 45. 198 embedded entries checked:183 available match,15 omitted from selective extracted trees; no mismatches. Inherited members recovered by identity where relevant. No runtime closure claimed.'},
 {'id':'F09','classification':'historical_metadata_postprocessing','sources':[43],'title':'Historical source comparison contains extra postprocessed counts','detail':'Saved SOURCE_COMPARISON includes unique_member_hash_count and unique_byte_new_hash_count beyond literal script construction. Historical byte-new counts cannot substitute for current whole-source coverage.'},
 {'id':'F10','classification':'inherited_caveat_retained_no_new_credit','sources':[2,34,36],'title':'Previously documented helper/interface caveats remain scoped','detail':'Phase14 helper divisibility omission and Phase28 noncanonical-residue zero-count problem are already preserved in prior audit evidence. Supported validated evaluator inputs and generated canonical-residue certificate cases are unaffected; no new whole-source dependency credit awarded.'}
]
dump('FINDINGS.json',findings)
coverage=[]
for row,rep in zip(rows,reports):
 coverage.append({'sha256':row['sha256'],'name':rep['name'],'representative_path':row['representative_path'],'assigned_batch':row['assigned_batch'],'bytes':row['size_bytes'],'lines':row['source_lines'],'fully_read_line_intervals':[[1,row['source_lines']]],'full_static_inspection':True,'static_inspection_complete':True,'source_executed':False,'source_executed_in_review':False,'source_imported':False,'source_compiled':False,'source_parsed':False,'inspection_method':rep['inspection_method'],'new_coverage_credit':True,'prior_full_coverage_package':None,'snapshot':row['snapshot'],'review_file':rep['report_path'],'finding_ids':[f['id'] for f in findings if row['source_index'] in f['sources']],'dependency_closure_complete':False})
cov={'package':'fusion_phase_source_review_0408','completed_utc':now,'assigned_batches':list(dict.fromkeys(r['assigned_batch'] for r in rows)),'assigned_batch_hashes':45,'fully_read_hashes_this_review':45,'new_full_read_hashes':45,'new_coverage_credit_count':45,'new_additive_full_static_reads':45,'previously_covered_hashes':0,'total_source_bytes_read':203307,'total_source_lines_read':5046,'all_assigned_source_reads_complete':True,'all_research_material_checks_finished':False,'dependency_closure_complete':False,'source_execution':'none','central_registry_modified':False,'scope_note':'45 exact assigned source texts read fully, without executing/importing/compiling/AST-parsing supplied programs. Saved data arithmetic checked separately. No global research completion, theorem acceptance, historical execution rerun or full dependency closure claimed.','baseline_sources_checked_at_start':len(base['coverage_sources']),'completed_coverage_and_inventory_sources_checked_at_end':len(cur),'current_additive_registry_sha256_at_completion':next(e['sha256'] for e in cur if pathlib.Path(e['path']).name=='ADDITIVE_CODE_COVERAGE.json'),'rows':coverage}
dump('COVERAGE.json',cov)
report='# Fusion and phase source review, 0408\n\nCompleted full text review of 45 exact assigned hashes: 203,307 bytes and 5,046 lines. All 45 are new static-review credit against the frozen inventory, additive registry and every completed coverage document visible at start and completion. No supplied program was executed, imported, compiled or AST-parsed. Central registry was not changed.\n\n## Main findings\n\n'
for f in findings:report+=f'### {f["id"]}: {f["title"]}\n\nClassification: {f["classification"]}. Sources: '+', '.join(str(i) for i in f['sources'])+'.\n\n'+f['detail']+'\n\n'
report+='## Evidence and identity\n\n137 original evidence documents were snapshotted (705,524 bytes). Available embedded manifest entries have no hash mismatches. Reviewer-authored JSON/CSV/hash arithmetic checked saved counts, differences and all three Bezout identities. Those arithmetic checks do not execute the source generators or reconstruct their full mathematical dependencies. Full details: ARTIFACT_CHECKS.json, EMBEDDED_MANIFEST_CHECKS.json, ARCHIVE_DEPENDENCY_IDENTITIES.json and DEPENDENCIES.json.\n\nThe original snapshot baseline and completion baseline are distinct. Any concurrent integration/registry changes are recorded in BASELINE_DRIFT.json, separately from original-source preservation. All90 original code-byte/master-source locations and all 45 review snapshots retain expected SHA-256 identities.\n\n## Per-source review index\n\n'
for rep in reports:report+=f'- {rep["source_index"]:02d}. [{rep["name"]}]({rep["report_path"]}) ({rep["source_lines"]} lines; `{rep["sha256"]}`)\n'
report+='\n## Boundaries\n\nFull assigned-source reads are complete. The entire research program is not fully checked. Dependencies are identified but not all newly read; historical logs are preserved evidence, not fresh executions; randomized/finite-field tests are not blanket complex-field proofs; numerical failures and incomplete evidence remain explicitly recorded. The result contains no source repairs and adds no universal FFT breakthrough claim.\n'
(O/'REVIEW_REPORT.md').write_text(report)
(O/'README.md').write_text('# Review package\n\nStart with REVIEW_REPORT.md. COVERAGE.json carries exact-hash credit flags. SOURCE_REPORTS.json and reports/ contain 45 full source reviews. sources/ are inert exact snapshots. Baseline, completion-baseline, evidence and dependencies are preserved byte data. Reviewer-authored helpers only read/hash/organize data or verify saved integer arithmetic; no uploaded program execution occurred.\n\nSee SHA256SUMS.txt and SEAL.json for package integrity.\n')
# All files except self-referential seal outputs.
files=sorted(p for p in O.rglob('*') if p.is_file() and p.name not in ['SHA256SUMS.txt','SEAL.json'])
sealtext=''.join(sha(p.read_bytes())+'  '+str(p.relative_to(O))+'\n' for p in files)
(O/'SHA256SUMS.txt').write_text(sealtext)
dump('SEAL.json',{'created_utc':now,'package':'fusion_phase_source_review_0408','sealed_file_count':len(files),'sha256sums_sha256':sha(sealtext.encode()),'coverage_sha256':sha((O/'COVERAGE.json').read_bytes()),'review_report_sha256':sha((O/'REVIEW_REPORT.md').read_bytes()),'source_hashes':45,'new_credit_hashes':45,'source_preservation':'all 90 original locations and 45 snapshots match frozen assigned identities','source_execution':'none','central_registry_modified':False})
print(json.dumps({'new':45,'bytes':203307,'lines':5046,'coverage_sha256':sha((O/'COVERAGE.json').read_bytes()),'sealed_files':len(files),'baseline_changed':len(drift['authorized_concurrent_baseline_changes']),'new_coverage_documents':len(drift['new_coverage_documents']),'source_drift':len(drift['original_source_drift'])},indent=2))
