"""New data-only reconciliation builder. Existing programs are never imported/run."""
from pathlib import Path
import json, hashlib, re, collections, csv
ROOT=Path('fft_research_master_20261009')
BASE=Path('code_coverage_audit_0228')
OUT=Path('generated_receipt_reconciliation_0254')
DOCS=OUT/'evidence_documents'; DOCS.mkdir(exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
rows=json.loads((OUT/'SCOPE_ROWS.json').read_text())
original_evidence={e['id']:e for e in json.loads((BASE/'COVERAGE_EVIDENCE.json').read_text())}
master_files={x['path']:x for x in json.loads((BASE/'MASTER_FILE_HASHES.json').read_text())}
expected_root_seal=json.loads((BASE/'INPUT_SNAPSHOT.json').read_text())['master_root_seals_sha256']['SHA256SUMS.txt']
seal_path=ROOT/'SHA256SUMS.txt'
if sha(seal_path.read_bytes())!=expected_root_seal:seal_path=ROOT/'checkpoint_history/v21_SHA256SUMS.txt'
assert sha(seal_path.read_bytes())==expected_root_seal
(OUT/'ORIGINAL_MASTER_V21_SHA256SUMS.txt').write_bytes(seal_path.read_bytes())
master_seal={}
for j,line in enumerate(seal_path.read_text().splitlines(),1):
 h,p=line.split(maxsplit=1);master_seal[p.lstrip('*').removeprefix('./')]={'sha256':h,'line':j}
assert sha(seal_path.read_bytes())==expected_root_seal
# Per-target document selection is a judgment, not an automatic execution inference.
# D = named historical run/replay declaration; O = observed attributed output only;
# S = static import/support relationship; A = auxiliary or archival utility with no direct receipt.
config={
1:('D','PHASE18_PHASE17_INDEPENDENT_AUDIT.md README.md','PORTABLE_RUN.log independent_phase18.log independent_phase18_results.json','../../README.md @VERIFICATION.md','Group-level historical rerun declaration names the 16:28 branch checkers; branch report and README identify this checker and run summary. No exact historical argv recovered.'),
2:('D','V9_INDEPENDENT_AUDIT.md README.md','PORTABLE_RUN.log independent_v9_run.log independent_v9_results.json','../../README.md @VERIFICATION.md','16:28 branch rerun declaration plus the explicitly successful run summary; exact historical argv remains unrecorded.'),
3:('D','PHASE13_AUDIT.md README.md','independent_phase13_results.json','VERIFICATION.txt','Verification explicitly says all six checker commands in README passed. This exact script is among those six.'),
4:('D','ALL_RESEARCH_MAP.md README.md','haar_split_control.json','VERIFICATION.txt','Verification explicitly says all six checker commands in README passed; this is one of them.'),
5:('D','README.md PROOF.md','results.json','../VERIFICATION.txt ../README.md','Parent verification names the six passed commands, including whole_word/check_whole_word.py. The historical working-directory clause is retained.'),
6:('A','REPRODUCE.md REVIEW.md','','','Shared package-integrity utility; reproduction instructions and bundle existence do not document its direct invocation. Its full source checks listed manifest entries only, not manifest self-hash or undeclared extra files.'),
7:('S','INDEPENDENT_REVIEW.md','VERIFIED_RESULTS.json review_run.log portable_replay.log','PORTABLE_REPLAY.json','exact_utils.py is an imported helper. The receipt commands independent_checks.py, never exact_utils.py; module/function coverage is not inferred.'),
8:('O','FIXED_INTERFACE_EXTERIOR_UNIQUENESS.md','EXTERIOR_UNIQUENESS_CONTROLS.json','EXTERIOR_UNIQUENESS_SHA256SUMS.txt','Constructor role and saved controls are bound. No explicit historical invocation or completed-run receipt was found; controls are not converted into a command receipt.'),
9:('O','NONZERO_MASK_BUTTERFLY_CONTROL.md','NONZERO_BUTTERFLY_CONTROLS.json','NONZERO_BUTTERFLY_SHA256SUMS.txt','Authored finite controls and their sealed output are present; no explicit historical invocation/replay receipt was located.'),
10:('O','ORIGINAL_BANK_ORIENTATION_ADDENDUM.md','ORIGINAL_ORIENTATION_CONTROLS.json','ORIGINAL_ORIENTATION_SHA256SUMS.txt','Report identifies authored checker and saved results; this is output attribution without an explicit past invocation.'),
11:('D','INFINITE_CHIRP_EXCLUSION.md REPRODUCE.md','CHECK_RUN.log EXACT_RESULTS.json','PORTABILITY.json','Portability record explicitly describes copying only the newly authored checker and a byte-identical isolated replay. The reproduction instruction identifies the sole mathematical checker; no historical command string is asserted.'),
12:('O','ODD_CHIRP_CUBIC_GATE.md','ODD_CHIRP_RESULTS.json','MANIFEST.sha256','Report records completed check counts and per-case data. It does not preserve argv or an explicit past invocation; retain report-attributed controls separately from a direct run receipt.'),
13:('D','TWO_CAYLEY_FEEDBACK.md','TWO_CAYLEY_RESULTS.json','MANIFEST.sha256','Report explicitly says the completed run passed all 18 cases after identifying the named newly authored script; no exact command receipt exists.'),
14:('D','PHASE22_AUDIT.md REPLAY.md','INDEPENDENT_RESULTS.json INDEPENDENT_RUN.log','PORTABILITY.json INDEPENDENT_CODE_PROVENANCE.json','Same bytes are a direct Phase22 checker and later Phase24/25 imported helper. Original report records actual relocated replay; do not let a later support alias erase original entrypoint history.'),
15:('S','INDEPENDENT_REVIEW.md','FIXED_GUARD_RESULTS.json SECTOR_RESULTS.json portable_replay.log','PORTABLE_REPLAY.json','geometry.py is statically imported by two checkers. Recorded replay.py orchestrates these checkers. It has no standalone main/test body; no direct invocation is claimed.'),
16:('O','EXACT_SOURCE_FORCED_RECOVERY_AND_FREE_TERM.md','COMPRESSED_BOUNDARY_CONTROLS.json EXACT_RUN.log','COMPRESSED_BOUNDARY_SHA256SUMS.txt','Exact controls/log are preserved, but the report says replay must reproduce them rather than recording a completed replay. No command receipt manufactured from the PASS log.'),
17:('A','REPRODUCE.md FAILED_ROUTES.md','POLE_RATIONAL_DATA.json','MANIFEST.sha256','Explicitly optional exploratory SymPy helper; final certificate checker neither imports it nor reads its output. Source has top-level symbolic work and writes POLE_RATIONAL_DATA.json; its historical invocation is unverified.'),
18:('A','REPRODUCE.md FAILED_ROUTES.md','','MANIFEST.sha256','Explicitly exploratory modular probe, unnecessary to final replay; no corresponding direct run receipt was found. It prints bounded finite probes at import/top level.'),
19:('A','REPRODUCE.md FAILED_ROUTES.md','','MANIFEST.sha256','Explicitly exploratory SymPy probe, unnecessary to final replay; no direct run receipt. Top-level symbolic calculation prints diagnostics, not a reusable imported helper.'),
20:('O','THREE_GREEN_RESTRICTED_FAMILY.md REPRODUCE.md','EXACT_EXTENSION_RESULTS.json CHECK_RUN.log','PORTABILITY.json','PORTABILITY.json has a replay command string but no success/returncode/completed-replay assertion. Treat that string as reproduction metadata, not proof the command ran.'),
21:('O','EXACT_RESTRICTED_NTT.md','EXACT_NTT_CHECKS.json','SHA256SUMS.json','Named authored checker and reported passed finite controls; no direct historical invocation receipt. No transfer from its independent mathematical review or other checker.'),
22:('O','RANDOM_BINARY_OCCUPANCY.md','OCCUPANCY_CHECKS.json','SHA256SUMS.json','Report-attributed exhaustive finite counts and saved data, not an invocation transcript.'),
23:('O','WORD_ARRAY_ADDENDUM.md','WORD_ARRAY_CHECKS.json','SHA256SUMS.json','Report describes passed finite controls and a cost-only run, but no command or replay identity is recorded. Save this as reported control evidence, not a recovered command.'),
24:('O','REVIEW.md','BOUNDED_LEMMA_RESULTS.json bounded_check.log','','Reproduction instruction plus JSON/log PASS is output evidence; no explicit past invocation or relocation receipt found for this exact checker.'),
25:('A','REVIEW.md','COVERAGE.json','','Ledger-construction provenance utility requiring the original canonical corpus; explicitly not needed for algebra replay. Ledger existence is not a receipt that this exact generator ran.'),
26:('D','README.md','VERIFICATION.txt','','README identifies VERIFICATION.txt as recorded successful package verification and names verify_package.py as its checker. No exact historical command argv recovered.'),
27:('O','V12_AUDIT_AND_EXTENSION.md','CHECK_RESULTS.json CHECK_RUN.log','../README.md','The report attributes all computations to this exact checker and parent README describes completed results/run logs. Preserved output exists, but no explicit invocation/replay receipt was recovered.'),
28:('S','PHASE25_AUDIT.md README.md','CHECK_RESULTS.json RUN.log','PORTABILITY_CHECK.json','Imported frontier solver, not the directly invoked independent_checks.py entrypoint. Top-level definitions only; report and static import identify support relationship.'),
29:('D','PHASE25_AUDIT.md README.md','CHECK_RESULTS.json RUN.log','PORTABILITY_CHECK.json','Report explicitly identifies successful run and portability record says only the independently authored checker was executed with returncode 0. Helper remains separately classified.'),
30:('D','COMPRESSED_SCHUR_HORIZON_AUDIT.md','INDEPENDENT_RESULTS.json INDEPENDENT_RUN.log','PORTABILITY_CHECK.json','Report explicitly: only newly authored independent_compressed_checks.py was executed. Portability record binds exact checker/results hashes; it is not mere bundle support.'),
31:('D','REVIEW.md REPRODUCE.md','INDEPENDENT_RESULTS.json CHECK_RUN.log','PORTABILITY.json','Report and portability describe isolated standard-library replay with no source programs available, tied to the sole named checker.'),
32:('D','PHASE13_AUDIT.md','INDEPENDENT_RESULTS.json INDEPENDENT_RUN.log','PORTABILITY_CHECK.json INDEPENDENT_CODE_PROVENANCE.json','Report explicitly records actual relocated run; portability has the exact checker and result hashes. No exact argv copied into a fabricated receipt.'),
33:('D','PHASE14_AUDIT.md','INDEPENDENT_RESULTS.json INDEPENDENT_RUN.log','PORTABILITY_CHECK.json','Report explicitly records an actual relocated standard-library run with identical checker/results bytes, bound in the portability record.'),
34:('D','PHASE24_AUDIT.md','INDEPENDENT_RESULTS.json INDEPENDENT_RUN.log','PORTABILITY_CHECK.json INDEPENDENT_CODE_PROVENANCE.json','Report records actual execution of named checker in a relocated directory. Later Phase25 uses the same hash under independent_phase24_math.py as support; both roles coexist.'),
35:('D','PHASE25_AUDIT.md','INDEPENDENT_RESULTS.json INDEPENDENT_RUN.log','PORTABILITY_CHECK.json INDEPENDENT_CODE_PROVENANCE.json','Named checker reproduction command is adjacent to an actual relocated replay declaration; exact hashes in portability bind the entrypoint and separate imported helpers.'),
36:('D','PHASE26_AUDIT.md','INDEPENDENT_RESULTS.json INDEPENDENT_RUN.log','PORTABILITY_CHECK.json','Explicit named execution declaration and exact-hash relocated replay; original bundle-only mapping was overly narrow.'),
37:('S','MARKED_NEXT_PIVOT_VARIABLE_BLOCK_AUDIT.md','NEXT_PIVOT_INDEPENDENT_RUN.log VARIABLE_BLOCK_INDEPENDENT_RUN.log','PORTABILITY_CHECK.json','Definition-only linear algebra support imported by both independently run entrypoints. Its copied hash is not a direct-entrypoint receipt.'),
38:('D','MARKED_NEXT_PIVOT_VARIABLE_BLOCK_AUDIT.md','NEXT_PIVOT_INDEPENDENT_RESULTS.json NEXT_PIVOT_INDEPENDENT_RUN.log','PORTABILITY_CHECK.json','Report names both run commands and an actual fresh-directory replay; exact code/results/log hashes bind this entrypoint separately from the linear helper.'),
39:('D','MARKED_NEXT_PIVOT_VARIABLE_BLOCK_AUDIT.md','VARIABLE_BLOCK_INDEPENDENT_RESULTS.json VARIABLE_BLOCK_INDEPENDENT_RUN.log','PORTABILITY_CHECK.json','Report names both run commands and an actual fresh-directory replay; exact code/results/log hashes bind this entrypoint separately from the linear helper.'),
40:('D','PHASE20_AUDIT.md README.md','results.json PORTABLE_RUN.log COORDINATOR_PORTABLE_RUN.log','../README.md ../VERIFICATION.json','Coordinator verification explicitly lists this branch relocated validation log; parent README identifies checker command. This is historical group/branch execution evidence, not a newly repeated run.'),
41:('D','CHARGED_TAYLOR_PRECISION_EXTENSION.md','check_results.json check_run.log PORTABLE_RUN.log COORDINATOR_PORTABLE_RUN.log','../README.md ../VERIFICATION.json','Coordinator verification explicitly lists Taylor relocated validation log and the parent README names its checker command; report also links full records.'),
42:('D','REVIEW.md','results.json PORTABLE_RUN.log COORDINATOR_PORTABLE_RUN.log','../README.md ../VERIFICATION.json','Coordinator verification explicitly lists twisted-bound relocated validation log; parent README identifies the command and branch.'),
43:('D','SOURCE_PROVENANCE.md README.md','PROVENANCE_RUN.log PORTABLE_PROVENANCE_RUN.log','VERIFICATION.json @VERIFICATION.md','Master historical declaration explicitly says portable provenance checks passed; README names its independent provenance command. Branch output remains narrowly source-integrity evidence.'),
44:('D','PROOF_OR_OBSTRUCTION.md','check_results.json PORTABLE_RUN.log','../VERIFICATION.json ../README.md @VERIFICATION.md','Verification.json marks this named Prony branch portable_rerun_passed and README specifies its checker. No historical exact argv beyond group documentation is claimed.'),
45:('D','V11_AUDIT.md','CHECK_RESULTS.json CHECK_RUN.log PORTABLE_RUN.log','../VERIFICATION.json ../README.md','Report explicitly calls CHECK_RUN.log actual run output and identifies the checker; portability metadata separately records the branch rerun.'),
46:('A','README.md VERIFICATION.md','','PORTABILITY_CHECK.json','Wrapper source statically dispatches three auditors. Reports say auditors reran, but do not specifically say this wrapper was invoked. Keep wrapper itself direct-execution-unverified rather than inherit child receipts.'),
47:('D','WINDOW_AUDIT.md','CHECK_RESULTS.json RUN.log','../VERIFICATION.md ../PORTABILITY_CHECK.json @additions/1845/VERIFICATION.md','Exact byte reuse as prior_window_audit/independent_checks.py in 1845 has explicit named launch transcript and report. Static path/hash binding avoids relying on filename alone.'),
48:('D','VERIFICATION.md','SOURCE_ARCHIVES.json','PORTABILITY_CHECK.json','Report explicitly names this auditor among four rerun programs; external preserved transcript names its launch. No source implementation was run in this reconciliation.'),
49:('D','README.md VERIFICATION.md','','PORTABILITY_CHECK.json','Report explicitly says runner launched from outside package. Full wrapper source identifies its four subprocesses; external log carries that wrapper\'s named launch and completion lines.'),
50:('D','WOODBURY_AUDIT.md','CHECK_RESULTS.json RUN.log','../VERIFICATION.md ../PORTABILITY_CHECK.json','Report explicitly names this rerun auditor; preserved transcript names woodbury_audit/independent_checks.py. The DFT module remains imported support.'),
51:('S','WOODBURY_AUDIT.md','CHECK_RESULTS.json RUN.log','../VERIFICATION.md','Function-only evaluator imported by the Woodbury checker. Recorded 9,600 standalone evaluator comparisons are reported function exercise via the harness, not direct execution of this file or all-branch coverage.'),
52:('D','BRIDGE_AUDIT_AND_CONSTRUCTION.md','CHECK_RESULTS.json CHECK_RUN.log','','Report explicitly identifies CHECK_RUN.log as actual output of the named independently authored checker.'),
53:('O','AUDIT_AND_EXTENSION.md README.md','CHECK_RESULTS.json CHECK_RUN.log','','Recorded output self-identifies this exact checker_sha256. Strong exact output attribution, but no separate historical argv/returncode/replay receipt; do not fabricate one.'),
54:('D','DIVISOR_SPECTRUM_AUDIT.md README.md','CHECK_RESULTS.json CHECK_RUN.log','','Report explicitly says completed run is preserved in CHECK_RUN.log next to named checker command.'),
55:('D','AUDIT_REPORT.md README.md','independent_results.json independent_run.log','','README explicitly calls the saved log the original run and names independent_checks.py. Diagnostic timing and mathematical limits stay separate.'),
56:('O','JOINT_ORBIT_REPORT.md README.md','CHECK_RESULTS.json','SHA256SUMS.txt','Named constructor checker and full-output controls are documented. No explicit historical invocation or isolated run receipt located; do not borrow the separate independent reviewer\'s receipt.'),
57:('A','README.md','LAYOUT_PROBE.json','PORTABILITY.json','Optional NumPy exploratory probe. PORTABILITY.json explicitly concerns independent_checks.py, not this probe. Source writes to a hard-coded original workspace path; its portability is not implied.'),
58:('D','README.md','EXACT_CHECK_RESULTS.json EXACT_CHECK_RUN.log','','README explicitly states a relocated run from a fresh directory and different working directory produced byte-identical exact results and log.'),
59:('O','NETWORK_REVIEW.md','INDEPENDENT_NETWORK_RESULTS.json INDEPENDENT_NETWORK_RUN.log','','Report attributes graph controls, with saved results/log; no command/run receipt specific to independent_network_check.py. Separate verify_n2048_cut.py evidence must not be transferred.'),
60:('D','EQUAL_OUTER_REVIEW.md','VERIFIED_RESULTS.json review_run.log','PORTABLE_REPLAY.json','Portability explicitly says full_exact_checker_repeated with byte-identical result and records stdout. The report identifies verify_equal_outer.py; historical exact argv absent.'),
61:('O','PHASE5_REVIEW.md','PHASE5_REVIEW_RESULTS.json RUN.log','SEAL.json','Newly reproduced exact-evidence section attributes controls to the named checker, but no historical command or replay receipt survives in the inspected sources.'),
62:('O','PHASE8_REVIEW.md','PHASE8_REVIEW_RESULTS.json RUN.log','SEAL.json','Named reviewer checker and control counts/log retained. No explicit historical command/replay receipt; regeneration claims are not converted into argv.'),
63:('O','AUDIT.md','RESULTS.json RUN.log','SHA256SUMS','Named reproduction instruction and saved independent finite-control output; direct historical invocation remains unverified.'),
64:('D','INDEPENDENT_REVIEW.md','INDEPENDENT_RESULTS.json INDEPENDENT_RUN.log','PORTABILITY.json','Portability expressly records relocated_check passed and byte-identical results. Package contains the named standalone checker; no exact historical command string is asserted.'),
65:('O','SOURCE_REVIEW.md REPRODUCE.md','INDEPENDENT_RESULTS.json INDEPENDENT_RUN.log','','Named checker, control report and log exist, but a command instruction is not a past execution receipt. No transfer from other same-name independent_checks.py files.'),
66:('D','REVIEW.md REPRODUCE.md','COMPARISON_RESULTS.json COMPARISON_RUN.log','PORTABILITY.json','Review and portability jointly record isolated relocated replay of the named comparison checker; the identical verify_seal.py utility gets no run credit from it.'),
}
assert set(config)==set(range(1,67))
fullread={6,7,15,17,18,19,28,37,46,49,51,57}
role={6:'package_integrity_utility',7:'imported_library',15:'imported_library',17:'optional_exploratory_entrypoint',18:'optional_exploratory_entrypoint',19:'optional_exploratory_entrypoint',25:'ledger_construction_utility',28:'imported_library',37:'imported_library',46:'subprocess_orchestrator',49:'subprocess_orchestrator',51:'imported_evaluator',57:'optional_exploratory_entrypoint'}
source_index={}; evidence=[]; ledger=[]
def source(path):
 p=Path(path).resolve(); b=p.read_bytes();h=sha(b); key=str(p);snapshot_read_path=p
 rel=str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else None
 expected=master_seal.get(rel,{}).get('sha256')
 live_sha=h
 if expected and h!=expected:
  archived=ROOT/'checkpoint_history'/('v21_'+p.name)
  assert archived.exists() and sha(archived.read_bytes())==expected, (p,'Snapshot source unavailable')
  snapshot_read_path=archived;b=archived.read_bytes();h=sha(b)
 if key not in source_index:
  portable=f'evidence_documents/{h[:20]}__{p.name}'; (OUT/portable).write_bytes(b)
  rel=str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else None
  seal=master_seal.get(rel) if rel else None
  if seal: assert seal['sha256']==h,(p,'changed from root seal')
  source_index[key]={'path':key,'snapshot_read_path':str(snapshot_read_path),'observed_live_path_sha256':live_sha,'live_path_has_advanced_beyond_snapshot':live_sha!=h,'sha256':h,'size_bytes':len(b),'portable_path':portable,'line_count':len(b.decode(errors='replace').splitlines()),'master_relative_path':rel,'master_seal_binding':seal,'provenance_scope':'sealed master snapshot' if seal else 'external local historical artifact, separately hashed'}
 return source_index[key]
def cite(index,p,kind,selectors=None):
 info=source(p); lines=(OUT/info['portable_path']).read_text(errors='replace').splitlines(); ranges=[]
 if selectors:
  for selector in selectors:
   hits=[j for j,l in enumerate(lines) if selector in l]
   for j in hits:
    a=max(0,j-1);b=min(len(lines),j+4);ranges.append({'first_line':a+1,'last_line':b,'text':'\n'.join(lines[a:b])})
  extent='Explicit cited line ranges; full file bytes retained and hashed. No whole-document substantive review claimed.'
 else:
  if len(lines)<=24:ranges=[{'first_line':1,'last_line':len(lines),'text':'\n'.join(lines)}]
  extent='Complete artifact retained as data; metadata/content attribution only, not executed. Large numeric arrays were not manually revalidated.'
 eid=f'GR{len(evidence)+1:04d}'
 evidence.append({'id':eid,'scope_row':index,'code_sha256':rows[index-1]['sha256'],'kind':kind,'source':info,'inspection_extent':extent,'selected_ranges':ranges})
 return eid
def resolve(d,s):return ROOT/s[1:] if s.startswith('@') else (d/s).resolve()
selects=['was executed','were rerun','completed run','actual run','actual relocated','relocated replay','relocated run','isolated','passed portable','Only newly','run output','original run','Run ','python ','python3 ','imports only','are imported','newly authored','newly written','newly reproduced','only checker','checker_sha256','run summary','successful run','executed only','portable_rerun_passed','relocated_validation_logs','All six','launching the runner']
for i,r in enumerate(rows,1):
 cls,reports,outputs,extras,note=config[i];p=ROOT/r['representative_path'];d=p.parent
 assert sha(p.read_bytes())==r['sha256'];assert sha(Path(r['local_content']).read_bytes())==r['sha256']
 assert master_seal[r['representative_path']]['sha256']==r['sha256']
 ids=[];seen=set()
 for kind,names in [('report_or_reproduction_instruction',reports),('recorded_output_artifact',outputs),('receipt_or_binding_context',extras)]:
  for name in names.split():
   q=resolve(d,name)
   if q in seen:continue
   seen.add(q)
   ids.append(cite(i,q,kind,(selects+[p.name]) if q.suffix=='.md' else None))
 # Original mapped authorship/support evidence is never overwritten.
 for oldid in r['evidence_ids']:
  old=original_evidence[oldid];q=Path(old['document']);q=q if q.is_absolute() else ROOT/q
  if q.exists() and q not in seen:
   seen.add(q);ids.append(cite(i,q,'original_evidence_context',(selects+[p.name]) if q.suffix=='.md' else None))
 # Verify and retain applicable local package seals only as byte bindings.
 seal_bindings=[]
 for parent in [d,*list(d.parents)[:3]]:
  if not parent.is_relative_to(ROOT):continue
  for nm in ['SEALED_MANIFEST.json','SEALED_MANIFEST.sha256','SHA256SUMS','SHA256SUMS.txt','MANIFEST.sha256','SHA256SUMS.json']:
   q=parent/nm
   if q.exists() and q.is_file() and q.stat().st_size<1000000:
    s=q.read_text(errors='replace')
    if r['sha256'] in s:
     inf=source(q);ls=s.splitlines();hits=[j for j,l in enumerate(ls) if r['sha256'] in l]
     seal_bindings.append({'source':inf,'lines_with_code_sha256':[j+1 for j in hits],'binding_extent':'Observed exact code digest in package manifest; this establishes package membership, not execution.'})
 src=source(p) if i in fullread else {'path':str(p),'sha256':r['sha256'],'size_bytes':r['size_bytes']}
 rec={'scope_row':i,'code_sha256':r['sha256'],'size_bytes':r['size_bytes'],'representative_path':r['representative_path'],'sealed_inventory_status':r['coverage_status'],'original_evidence_ids':r['evidence_ids'],'original_authorship_or_support_evidence_preserved':True,'primary_role':role.get(i,'mathematical_or_integrity_checker_entrypoint'),'reconciliation_class':{'D':'historical_named_execution_or_replay_report_bound','O':'attributed_control_outputs_without_direct_run_receipt','S':'imported_support_relationship_only','A':'authored_auxiliary_without_direct_run_receipt'}[cls], 'historical_named_entrypoint_execution_evidenced':cls=='D','historical_exact_argv_receipt':None,'reproduction_instructions_are_execution_receipts':False,'new_execution_or_import':False,'full_static_read':{'complete_bytes_read':i in fullread,'extent':{'first_line':1,'last_line':len(p.read_text().splitlines()),'first_byte_inclusive':0,'last_byte_exclusive':r['size_bytes']} if i in fullread else None,'purpose':'Complete inert-source role/control-flow inspection; not general correctness, mathematical proof, or branch-coverage review.' if i in fullread else 'No full-source-read credit claimed by this reconciliation. Reports/import spans only where identified.','source':src if i in fullread else None},'support_import_edges':[],'evidence_ids':ids,'package_hash_bindings':seal_bindings,'master_code_seal_binding':master_seal[r['representative_path']],'conclusion':note,'remaining_boundary':'Recorded historical reports are attributed evidence, not new replay, trusted runtime tracing, full dependency closure, all-branch testing, or correctness proof.'}
 ledger.append(rec)
# Support edges are tied to actual sibling code bytes and inert import lines.
edges={7:[('independent_checks.py',6,6)],15:[('check_fixed_guards.py',7,7),('check_sectors.py',6,6)],28:[('independent_checks.py',8,9)],37:[('independent_next_pivot.py',2,2),('independent_variable_block.py',2,2)],51:[('independent_checks.py',13,13)]}
for i,ee in edges.items():
 d=(ROOT/rows[i-1]['representative_path']).parent
 for nm,a,b in ee:
  p=d/nm;info=source(p);ls=p.read_text().splitlines()
  ledger[i-1]['support_import_edges'].append({'importer':info,'imported_code_sha256':rows[i-1]['sha256'],'imported_local_path':str(d/Path(rows[i-1]['representative_path']).name),'first_line':a,'last_line':b,'text':'\n'.join(ls[a-1:b]),'extent':'Literal sibling import relationship only; no runtime import tracing or exhaustive function exercise claimed.'})
# Executed wrapper -> imported support chain for geometry.
q=ROOT/rows[14]['representative_path'];replay=q.parent/'replay.py';ledger[14]['support_orchestration']=source(replay)
ledger[14]['support_orchestration_extent']='Entire 12-line replay.py read inertly: invokes check_fixed_guards.py/check_sectors.py among four subprocesses; PORTABLE_REPLAY.json names replay.py. No execution performed.'
# Exact historical command strings are copied only where the historical record itself names the command.
for i,cmd in [(3,'python3 independent_phase13_checks.py'),(4,'python3 verify_haar_split.py'),(5,'(cd whole_word && python3 check_whole_word.py)')]:
 ledger[i-1]['historical_exact_argv_receipt']={'command_text':cmd,'type':'README command explicitly included by VERIFICATION.txt all-six-commands-passed declaration','caveat':'Shell text as recorded, not a raw argv/OS process receipt.'}
# External original-output transcripts strengthen the 1845 launch mapping without changing snapshot identity.
for i in [47,48,49,50,51]:
 for nm in ['INDEPENDENT_RERUN.log','PORTABLE_RERUN.log']:
  p=Path('materials_1845')/nm
  ledger[i-1]['evidence_ids'].append(cite(i,p,'external_historical_named_launch_transcript',['Running independent auditor:','PASS: every independent auditor completed.','standalone_linear_evaluator_exact_comparisons']))
 # Exact sibling source binding in the old supplement; hash comparison only.
 rel=rows[i-1]['representative_path'].removeprefix('additions/1845/')
 if i==47:rel='prior_window_audit/independent_checks.py'
 q=Path('materials_1845/supplement')/rel
 assert q.exists() and sha(q.read_bytes())==rows[i-1]['sha256'],(i,q)
 ledger[i-1]['external_transcript_code_binding']={'path':str(q),'sha256':sha(q.read_bytes()),'method':'Exact byte equality with sealed inventory target; logged script names resolved inside this historical supplement. No timestamp/process attestation inferred.'}
# Dual-role historical helpers under later aliases; identity equality is checked explicitly.
for i,paths in [(14,['additions/0155_material_coverage_and_new_results/reviews/review_hero1_phase24/independent_trace_math.py','additions/0155_material_coverage_and_new_results/reviews/review_hero1_phase25/independent_trace_math.py']),(34,['additions/0155_material_coverage_and_new_results/reviews/review_hero1_phase25/independent_phase24_math.py'])]:
 ledger[i-1]['additional_support_aliases']=[]
 for rel in paths:
  p=ROOT/rel;assert sha(p.read_bytes())==rows[i-1]['sha256']
  importer=p.parent/'independent_checks.py';ls=importer.read_text().splitlines();hits=[j for j,l in enumerate(ls) if p.stem in l and ('import' in l or '.py' in l)]
  ledger[i-1]['additional_support_aliases'].append({'alias_path':rel,'sha256':rows[i-1]['sha256'],'importer':source(importer),'source_lines':[{'line':j+1,'text':ls[j]} for j in hits],'scope':'Same bytes, different package role. Earlier direct-execution evidence and later support identity are independent axes.'})
# Phase25 uses the Phase22 trace helper transitively through the copied Phase24 module.
for alias in ledger[13].get('additional_support_aliases',[]):
 if not alias['source_lines']:
  importer=ROOT/'additions/0155_material_coverage_and_new_results/reviews/review_hero1_phase25/independent_phase24_math.py'
  ls=importer.read_text().splitlines()
  alias['relationship']='transitive import via independent_phase24_math.py, not a direct import in independent_checks.py'
  alias['intermediate_importer']=source(importer)
  alias['intermediate_source_lines']=[{'line':j+1,'text':l} for j,l in enumerate(ls) if 'independent_trace_math' in l and 'import' in l]
 else:alias['relationship']='direct literal import'

# Validate self-identifying output without upgrading it into an invocation receipt.
for nm in ['CHECK_RESULTS.json','CHECK_RUN.log']:
 p=(ROOT/rows[52]['representative_path']).parent/nm
 assert json.loads(p.read_text())['checker_sha256']==rows[52]['sha256']
ledger[52]['output_self_identification']={'field':'$/checker_sha256','value':rows[52]['sha256'],'matched_files':['CHECK_RESULTS.json','CHECK_RUN.log'],'scope':'Self-reported exact checker identity in saved output; no independent process receipt.'}
counts=collections.Counter(r['reconciliation_class'] for r in ledger)
unresolved=[{'scope_row':r['scope_row'],'code_sha256':r['code_sha256'],'path':r['representative_path'],'reason':r['conclusion'],'needed_to_upgrade':'A historical explicit invocation/completed-run or replay record tied to this byte hash; do not execute existing code merely to repair history. Current output attribution is retained.','evidence_ids':r['evidence_ids']} for r in ledger if r['reconciliation_class']=='attributed_control_outputs_without_direct_run_receipt']
aux=[{'scope_row':r['scope_row'],'code_sha256':r['code_sha256'],'path':r['representative_path'],'reason':r['conclusion'],'action':'No standalone execution obligation created. Preserve role and unknown history; no fake run claim.'} for r in ledger if r['reconciliation_class']=='authored_auxiliary_without_direct_run_receipt']
preservation_before=json.loads((OUT/'SEALED_INPUT_HASHES_BEFORE.json').read_text());preservation_after={p.name:sha(p.read_bytes()) for p in BASE.iterdir() if p.is_file()}
assert preservation_before==preservation_after
summary={'snapshot':json.loads((BASE/'INPUT_SNAPSHOT.json').read_text()),'scope_exact_hashes':66,'original_status_counts':dict(collections.Counter(r['coverage_status'] for r in rows)),'reconciliation_counts':dict(counts),'full_inert_source_reads_for_role_only':len(fullread),'named_historical_execution_evidenced':sum(x['historical_named_entrypoint_execution_evidenced'] for x in ledger),'direct_execution_receipt_unresolved_checker_hashes':len(unresolved),'auxiliary_hashes_with_unknown_direct_execution_history':len(aux),'support_only_hashes':sum(x['reconciliation_class']=='imported_support_relationship_only' for x in ledger),'original_support_only_rows_now_named_historical_execution':sum(x['sealed_inventory_status']=='generated_recorded_run_support_only' and x['historical_named_entrypoint_execution_evidenced'] for x in ledger),'evidence_records':len(evidence),'source_documents_retained':len(source_index),'sealed_inventory_changed':False,'existing_code_executed_or_imported':False,'completion':'All 66 role/evidence questions are reconciled. Historical receipts remain honestly unresolved for the stated shortlist; this is not a claim all 66 programs ran or all code was reviewed.'}
for name,obj in [('RECONCILIATION.json',ledger),('RECONCILIATION_EVIDENCE.json',evidence),('EVIDENCE_SOURCE_INDEX.json',list(source_index.values())),('UNRESOLVED_RECEIPTS.json',unresolved),('AUXILIARY_HISTORY_BOUNDARIES.json',aux),('SUMMARY.json',summary),('PRESERVATION_CHECK.json',{'passed':True,'before':preservation_before,'after':preservation_after,'scope':'Every pre-existing top-level file in sealed code_coverage_audit_0228; version-21 master root seal recovered and verified (live master may have advanced); all retained source documents match version-21 sealed digests where present.'})]:
 (OUT/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
with (OUT/'RECONCILIATION.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['scope_row','sha256','path','original_status','role','class','named_historical_execution_evidenced','full_inert_role_read','conclusion'])
 for r in ledger:w.writerow([r['scope_row'],r['code_sha256'],r['representative_path'],r['sealed_inventory_status'],r['primary_role'],r['reconciliation_class'],r['historical_named_entrypoint_execution_evidenced'],r['full_static_read']['complete_bytes_read'],r['conclusion']])
print(json.dumps(summary,indent=2))
