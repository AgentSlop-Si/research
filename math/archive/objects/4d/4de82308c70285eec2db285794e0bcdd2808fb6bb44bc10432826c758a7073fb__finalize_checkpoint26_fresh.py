from pathlib import Path
import json,hashlib,shutil,datetime,re,collections
B=Path('[local workspace]');W=B/'master_v26_integration_20261010';D=W/'fft_research_master_20261009';S=B/D.name;A=D/'additions/0536_final_static_review_closure';R=B/'post_v22_review_registry_0308'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def inv(p):return {str(x.relative_to(p)):{'bytes':x.stat().st_size,'sha256':sha(x)} for x in sorted(p.rglob('*')) if x.is_file()}
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
# Root approval is a required external gate. This helper never creates it.
approval=json.loads((W/'ROOT_FINAL_APPROVAL.json').read_text());assert approval['finalize_local_checkpoint26'] is True
assert sha(R/'ADDITIVE_CODE_COVERAGE.json')==approval['registry_sha256']
closure=B/'final_review_closure_0535';seal=closure/approval['closure_manifest'];assert sha(seal)==approval['closure_manifest_sha256'];assert sha(closure/'SEAL.json')==approval['closure_seal_sha256']
for line in seal.read_text().splitlines():
 m=re.match(r'^([0-9a-f]{64})\s+\*?(.+)$',line);assert m,(seal,line)
 p=closure/m[2];assert p.is_file() and sha(p)==m[1],(p,'closure seal mismatch')
if not (A/'packages/final_review_closure_0535').exists():shutil.copytree(closure,A/'packages/final_review_closure_0535')
assert inv(closure)==inv(A/'packages/final_review_closure_0535')
coverage=json.loads((R/'ADDITIVE_CODE_COVERAGE.json').read_text());assert coverage['current_full_static_reads']==1684;assert coverage['current_complete_static_inspections']==1686
assert len(coverage['semantic_template_rows'])==2 and len(coverage['rows'])==1500
assert len({x['sha256'] for x in coverage['rows']})==1500
assert not set(x['sha256'] for x in coverage['rows'])&set(x['sha256'] for x in coverage['semantic_template_rows'])
material=json.loads((closure/'MATERIAL_AUDIT.json').read_text());audit=json.loads((closure/'COVERAGE_AUDIT.json').read_text())
assert audit['complete_static_inspection_unique_hashes']==1686 and audit['remaining_program_hashes']==0
snap=A/'registry_snapshots/final_approved';snap.mkdir(exist_ok=True)
for p in R.iterdir():
 if p.is_file() and p.suffix=='.json':shutil.copy2(p,snap/p.name)
shutil.copy2(W/'ROOT_FINAL_APPROVAL.json',A/'ROOT_FINAL_APPROVAL.json')
package_report=json.loads((A/'STAGED_PACKAGE_VERIFICATION.json').read_text())
accepted={x['body']['package']:x['body'] for x in package_report['acceptance_receipts']}
current_accepted={json.loads(p.read_text())['package'] for p in R.glob('POST25*.json') if 'package' in json.loads(p.read_text())}
assert current_accepted.issubset(set(accepted)),('Unstaged acceptance receipts',current_accepted-set(accepted))
assert sum(x.get('new_reads',0) for x in accepted.values())==899
repl={
'FINAL_COVERAGE_SENTENCE':'The frozen program-source universe is fully accounted for by 1,684 accepted first-to-last exact-hash source reads plus two complete generated-source semantic/template audits: 1,686 complete static inspections, with no available program hash still awaiting static inspection.',
'FINAL_COVERAGE_DETAIL':'The frozen inventory contains 906 material identities, 1,686 distinct program-source hashes and one separately classified build-metadata hash. There are 184 inherited full-read hashes and 1,500 accepted additive full-read hashes. Checkpoint 25 held 785 full reads; this checkpoint adds 899 full reads and the two generated-source template audits. The independent closure audit finds no duplicate additive hashes, no baseline/additive overlap, no template/literal overlap and no out-of-universe credit. All cached source bytes and all checked package seal entries match their recorded identities.',
'KEY_FINAL_FINDINGS':(W/'FINAL_FINDINGS_ADDITION.txt').read_text() if (W/'FINAL_FINDINGS_ADDITION.txt').exists() else '',
'AVAILABLE_CLOSURE_DISPOSITION':'The independent closure audit verifies 899 original-byte material identities and five matching-version text snapshots among the 906 frozen identities; two frozen document versions remain unavailable. It also verifies 269 archive containers and 19,932 archive-member occurrences. This closes the available-material static-inspection queue. It does not close missing historical versions, every proof or ancillary assertion, runtime dependency resolution, benchmark replication, account-wide access or publication priority. The unresolved-reference table retains those limits.'
}
text=(W/'SYNTHESIS_DRAFT.md').read_text().replace('The available-material static review has reached its final packaging stage.', 'The available-material static review is complete within the frozen scope described below.')
for k,v in repl.items():text=text.replace(k,v)
assert not any(k in text for k in repl)
(A/'INTEGRATED_RESULTS.md').write_text(text)
for n in ['PRACTICAL_FINDINGS','PUBLICATION_CANDIDATES']:(A/(n+'.md')).write_text((W/(n+'_DRAFT.md')).read_text())
u=(W/'UNRESOLVED_REFERENCES_DRAFT.md').read_text().replace('FINAL_CLOSURE_REFERENCE_NOTE',(W/'FINAL_CLOSURE_REFERENCE_NOTE.txt').read_text() if (W/'FINAL_CLOSURE_REFERENCE_NOTE.txt').exists() else 'The independent closure audit is retained in packages/final_review_closure_0535. Its available-source closure does not erase unresolved historical bytes, proof obligations or runtime qualifications.')
(A/'UNRESOLVED_REFERENCES.md').write_text(u)
rows=['# Exact review coverage','', 'Frozen program hashes: **1,686**. Full first-to-last reads: **1,684**. Complete generated-source template audits: **2**. Program hashes awaiting static inspection: **0**.','', 'All 477 selected text hashes have sealed complete-read records and matching bytes. All 380 explicit in-corpus dependency candidate hashes have accepted static coverage; runtime selection and third-party/build versions are not certified.','', 'The separately classified build-metadata hash is outside the 1,686-program denominator. Coverage credit uses exact SHA256 identity, never basenames. No file is removed by deduplication.','', '| Accepted post25 package | New full reads | Template audits |','|---|---:|---:|']
for n,d in accepted.items():
 if d.get('new_reads') or d.get('new_complete_template_checks'):rows.append(f"| {n} | {d.get('new_reads',0)} | {d.get('new_complete_template_checks',0)} |")
rows+=['','Predecessor checkpoint25: 785 full reads. This checkpoint: 899 additional full reads and two template audits. Total: 1,684 + 2 = 1,686 complete static inspections.','', 'Template audit means whole-byte equivalence to independently reconstructed and mathematically reviewed source templates. It is not recorded as literal first-to-last model reading. The source programs and SMT solver were not executed.','', 'Primary evidence: registry_snapshots/final_approved/ADDITIVE_CODE_COVERAGE.json; packages/final_review_closure_0535/COVERAGE_AUDIT.json; accepted package COVERAGE.json files.','', 'The private inventory receipt in packages/private_research_inventory_0453 remains an earlier 785-read snapshot. No spreadsheet mutation was performed by this integration. All-mathematics correctness, actual runtime closure and priority remain separate from static coverage.']
(A/'REVIEW_COVERAGE.md').write_text('\n'.join(rows)+'\n')
# Root index changes are allowed only after the complete predecessor root has been archived.
g=json.loads((W/'BASELINE_GUARD.json').read_text());baseline=g['canonical_files'];history=D/g['archive_root_snapshots']
assert inv(S)==baseline,'Canonical changed after staging'
for r,data in baseline.items():
 if '/' in r:assert (D/r).is_file() and sha(D/r)==data['sha256'],(r,'inherited nonroot mutation')
 else:assert sha(history/r)==data['sha256'],(r,'archived root mismatch')
(D/'CURRENT_CHECKPOINT.md').write_text(text)
(D/'README.md').write_text('# Fourier research master checkpoint 26\n\nRead additions/0536_final_static_review_closure/INTEGRATED_RESULTS.md. The frozen program universe has 1,684 full source reads plus two complete semantic/template audits, totaling 1,686 static inspections. Available-material static inspection is closed; missing historical versions, proof obligations, runtime provenance and publication priority remain qualified.\n\nAll inherited research files are preserved. The full lossless tar.xz is the complete archive; the compact findings ZIP is a reading copy. This is a locally verified checkpoint; a separate later save receipt establishes Library persistence.\n')
pending=json.loads((D/'PENDING_ADDITIONS.json').read_text());pending['remaining']='Available-material static-inspection queue closed; unresolved historical versions, proof obligations, runtime dependency closure, benchmark replication and novelty remain explicitly qualified.';pending['active_research']=[x for x in pending.get('active_research',[]) if x!='Complete remaining exact-hash source and dependency review'];pending['active_research'].insert(0,'Resolve separately listed missing historical bytes and theorem/runtime obligations where evidence becomes available');pending['checkpoint25_exclusions']=['The logarithmic bounded-separator audit excluded from checkpoint25 is now accepted and included in checkpoint26 with its scoped proof and priority qualifications.'];pending['checkpoint26_coverage']={'full_static_reads':1684,'complete_template_audits':2,'complete_static_inspections':1686,'program_static_inspections_open':0};write(D/'PENDING_ADDITIONS.json',pending)
status=json.loads((D/'ADDITIONS_STATUS.json').read_text());status['checkpoint26']={'addition':str(A.relative_to(D)),'full_static_reads':1684,'template_audits':2,'complete_static_inspections':1686,'available_program_static_inspection_closed':True,'all_mathematical_assertions_proved':False,'runtime_dependency_closure_certified':False,'publication_novelty_certified':False,'new_supplied_source_execution':False,'library_save_status':'local candidate; subsequent receipt required'};write(D/'ADDITIONS_STATUS.json',status)
v=(D/'VERIFICATION.md').read_text();v+='\n\n## Checkpoint 26 available material static closure\n\nAll 16,665 inherited files were matched to the saved checkpoint25 guard before staging. All inherited nonroot bytes remain unchanged; all 11 predecessor root files are archived in checkpoint_history/checkpoint25_root_before_checkpoint26. Accepted post25 package seals and copies were verified. The final approved ledger contains 1,684 literal full reads and two generated-source template audits, with no available program hash left open. The final closure audit verifies the frozen material/archive identities separately. These are static coverage and byte-preservation facts, not a blanket theorem or runtime certification. Only freshly authored metadata/packaging helpers were run. No canonical, Library or Drive mutation is performed by this integration.\n';(D/'VERIFICATION.md').write_text(v)
package_report['status']='FINAL_APPROVED_PACKAGE_SET';package_report['coverage_snapshot']={'full_static_reads':1684,'complete_static_inspections':1686};package_report['registry_snapshot']='registry_snapshots/final_approved';package_report['awaiting']=[];package_report['closure_package']={'name':'final_review_closure_0535','manifest':approval['closure_manifest'],'manifest_sha256':approval['closure_manifest_sha256'],'files':len(inv(closure))};write(A/'STAGED_PACKAGE_VERIFICATION.json',package_report)
# Fresh metadata helper copies document exactly what ran, without executing inherited research helpers.
helpers=A/'packaging_helpers';helpers.mkdir(exist_ok=True)
for n in ['stage_checkpoint26_fresh.py','stage_accepted_packages_fresh.py','finalize_checkpoint26_fresh.py','package_checkpoint26_fresh.py']:
 if (W/n).exists():shutil.copy2(W/n,helpers/n)
checks={'checkpoint':26,'status':'APPROVED_LOCAL_CONTENT_FINALIZED','predecessor_files':len(baseline),'inherited_nonroot_files_unchanged':sum('/' in p for p in baseline),'archived_prior_root_files':len(g['root_files']),'all_accepted_package_seals_match':True,'final_registry_sha256':approval['registry_sha256'],'closure_manifest_sha256':approval['closure_manifest_sha256'],'source_programs_executed':False,'canonical_modified':False,'library_mutated':False,'drive_mutated':False,'full_static_reads':1684,'template_audits':2,'complete_static_inspections':1686,'meaning':'Static review and byte-preservation closure within frozen available scope; unresolved proof/runtime/priority qualifications retained.'};write(A/'CONTENT_VERIFICATION.json',checks)
# Supplement-local digest list covers every added file except itself.
(A/'SHA256SUMS').write_text(''.join(f"{sha(p)}  {p.relative_to(A)}\n" for p in sorted(A.rglob('*')) if p.is_file() and p!=A/'SHA256SUMS'))
# Root digest lists cover all files except the two equivalent self-excluding digest lists.
lines=[f"{sha(p)}  {p.relative_to(D)}\n" for p in sorted(D.rglob('*')) if p.is_file() and p.relative_to(D).as_posix() not in {'SHA256SUMS','SHA256SUMS.txt'}]
for n in ['SHA256SUMS','SHA256SUMS.txt']:(D/n).write_text(''.join(lines))
final=inv(D);write(W/'FINAL_FILE_INVENTORY.json',final);write(W/'CONTENT_VERIFICATION.json',{**checks,'final_files':len(final),'final_bytes':sum(v['bytes'] for v in final.values()),'root_sha256_manifest_sha256':sha(D/'SHA256SUMS')})
print(json.dumps({'files':len(final),'bytes':sum(v['bytes'] for v in final.values()),'status':'FINALIZED_LOCAL_CONTENT_PENDING_ARCHIVE_VERIFICATION'}))
