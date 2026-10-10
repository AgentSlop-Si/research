from pathlib import Path
import hashlib,json,shutil,zipfile,ast
W=Path('v10_build');P=W/'fft_research_master_20261009';A=P/'additions/1954'; B=Path('fft_research_master_20261009'); R=W/'portable_checks'
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def jwrite(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
# Reruns were performed only in disposable copies of independent audit code.
x=json.loads((A/'divisor_audit/CHECK_RESULTS.json').read_text());y=json.loads((R/'divisor_audit/CHECK_RESULTS.json').read_text());x.pop('runtime_seconds');y.pop('runtime_seconds');assert x==y
assert (A/'divisor_audit/STATIC_CALLS.json').read_bytes()==(R/'divisor_audit/STATIC_CALLS.json').read_bytes()
assert json.loads((A/'graph_audit/independent_graph_results.json').read_text())==json.loads((R/'graph_rerun.json').read_text())
x=json.loads((A/'tensor_audit/independent_results.json').read_text());y=json.loads((R/'tensor_audit/independent_results.json').read_text());x.pop('seconds_diagnostic_only');y.pop('seconds_diagnostic_only');assert x==y
(A/'audits').rmdir()
records=json.loads((A/'source_records.json').read_text())
for r in records:
 if 'divisor_spectrum' in r['filename']:
  r['mathematical_status']='completed independent audit: inherited direct approximation theorem accepted; adaptive planner execution certificate refuted; separate least-prime spectral extension proved'
  r['new_audit_paths']=['additions/1954/divisor_audit/']
 elif 'hero17_tensor' in r['filename']:
  r['mathematical_status']='completed independent audits: selected-split structured exact transforms and guarded graph convolution accepted; separate growing-rank, square-multiplier and output-rank extensions proved; no unrestricted FFT claim'
  r['new_audit_paths']=['additions/1954/tensor_audit/','additions/1954/graph_audit/']
jwrite(A/'source_records.json',records)
intro='''# Six-source synthesis: 19:54 UTC, 9 October 2026\n\nAll six attachment identities are resolved. Four are byte-identical to existing master originals and retain their completed mathematical corrections; two contain new bytes and now have three completed independent audits. The source triage remains an unchanged historical/static snapshot; the final audits below supersede its pending review questions. Original source programs were never imported, executed or compiled.\n\nThe positive result is a larger set of explicitly recognized structured exact transforms and convolutions. The negative implementation finding is a false approximate-dispatcher certificate. Neither yields a general exact faster Fourier transform or a novelty certification.\n\n## HERO17 raw-input recognition: exact on selected structures\n\nFor supplied certified prime-field/root data, bounded-rank balanced CRT tensors and bounded-mode strided fibers are deterministically recognized and produce every Fourier output with the charged bounds. The standalone tensor and fiber branches admit uniform O((1+r)N) arithmetic under their balance guards, with explicit scalar-inversion costs and O(N) space; r=o(log N) therefore gives sub-N-log-N arithmetic on those accepted structured families. Support-coset reduction and fixed-r common-chirp recognition remain valid.\n\nThe default dispatcher selects a single fiber divisor and CRT split. It misses an explicit N=12 input that passes an eligible alternate Q=2 fiber test but fails its default Q=3 and other branches. This is incomplete fast-path coverage, not an incorrect accepted output. Its shipped common-chirp engine also retains a factorial eliminant, so the whole shipped callable does not inherit the standalone growing-rank ledger.\n\nA separate, specified dispatcher with independent tensor/fiber/chirp budgets and the earlier polynomial Toeplitz construction has ledger O(N(1+r_T+r_F+r_C^4)+r_C^(2+3 log_2 3)); it is an independently proved design, not implemented source functionality. Another independent corollary recognizes every integer-polynomial phase at N=d s^2 with the specified Q=s in O_d(N) for fixed d, irrespective of polynomial degree. More generally, each fiber has at most L=N/gcd(N,Q^2) modes. The default divisor must not be assumed to choose this split.\n\nThe independent controls include 118,617 exhaustive row-membership vectors, 591 raw fiber cases, 1,341 all-phase chirp cases, 820 Gauss rows, 160 bounded-square-multiplier polynomial examples and the selected-divisor counterexample. See `tensor_audit/AUDIT_REPORT.md`, `tensor_audit/EXTENSION_AND_FUSION.md` and its bounded primary-source context.\n\n'''
parts=(W/'approved_summary_parts.md').read_text()
tail='''\n## Four resends retain prior corrections\n\n- Sparse-defect: `additions/1930_sparse/` retains the arbitrary-row-sparse escape repair, charged Woodbury setup and pivot/bit qualifications.\n- Phase26: `additions/1930_phase26/` retains the factor-two crossing improvement, strict integer witness and restricted-architecture scope.\n- Mixed-radix v13: `additions/1930_v13/` retains the source phase-test mismatch, bounded randomness/conditioning refinements, and earlier exact-bank/Cooley–Tukey identity.\n- Composite HERO0: `additions/1916/` retains the stronger prior covariance, fixed-input approximation, scaled-projector identity and sampling contract.\n\nThose are paths in the master, not new copies of original archives. `source_records.json` maps each new upload identity to its exact preserved original.\n\n## Interpretation and stopping point\n\nAll three new audits, static triage and six-source request mappings are complete. The false planner certificate is a documented source defect; this update does not claim to repair or execute that planner. A general exact arbitrary-fresh-input, all-output, fully charged asymptotic Fourier improvement remains unestablished. Bit complexity, stable floating-point recognition, optimized practical speed, unrestricted convolution/integer multiplication and publication novelty do not follow. Baseline unread-source and account-coverage limits remain unchanged.\n'''
(A/'INTEGRATED_RESULTS.md').write_text(intro+parts+tail)
(A/'README.md').write_text('''# Six-source verified research update\n\nReceived 9 October 2026, 19:54 UTC. Four exact resends retain prior audits; two new source archives have three completed independent reviews.\n\n## Read first\n\n1. `INTEGRATED_RESULTS.md`: conclusions, new proofs, implementation defects and model limits.\n2. `source_records.json` and `SOURCE_LAYOUT.md`: all six Library identities and where exact originals are preserved.\n3. `tensor_audit/AUDIT_REPORT.md` and `tensor_audit/EXTENSION_AND_FUSION.md`: selected-split exact recognition, the missed-split example and separately budgeted extensions.\n4. `graph_audit/GRAPH_UNION_AUDIT_AND_RANK_FUSION.md`: guarded sparse convolution and the strictly broader output-rank fallback.\n5. `divisor_audit/DIVISOR_SPECTRUM_AUDIT.md`: inherited covariance, false dispatcher guarantee and new least-prime spectrum.\n6. `source_triage/SOURCE_TRIAGE_AND_FUSION.md`: unchanged initial static comparison, with final mathematical dispositions in the above reports.\n7. `ASSEMBLY_VERIFICATION.json`: source/seal integrity and isolated portable check results.\n\n## Trust and reproduction\n\nThe original ZIPs and extracted/source-evidence programs are data only. Do not run or import uploaded code. Only the newly authored independent checkers were run. The tensor and divisor checkers rewrite diagnostic result files, so reproduce them from copies if preserving seals. Tensor and graph use Python's standard library; divisor also uses NumPy. Refer to each audit README for exact commands.\n\nThe addition preserves two new original archive streams once. Four duplicate archives already exist unchanged in the master and are referenced by exact path/hash; their new request identities are not lost. Their approved reports are not newly rediscovered results. No prior whole-master or recursive supplement ZIP is embedded.\n\nThis update establishes structured exact extensions and a concrete certification failure, with no general exact FFT breakthrough or publication-priority claim.\n''')
seals={
 'divisor_audit':{'manifest':'SHA256SUMS.txt','sha256':'0f1e11d417edb1afab530e0b29429cbf135d5eb538cacee12dc588f5815c5a4f','manifest_entries':31,'rerun_comparison':'all semantic results equal; only runtime_seconds excluded; STATIC_CALLS.json byte-identical'},
 'graph_audit':{'manifest':'SHA256SUMS','manifest_entries':7,'manifest_json_sha256':'74c3a0800413eef2a86d781b1441c08e78db102b0e224bd594002f613cd58a23','rerun_comparison':'complete output JSON equal'},
 'tensor_audit':{'manifest':'SHA256SUMS','sha256':'ac5772c55d229a081ba8d711b2ad89c54da8692264892eb62fa6d270cd1dfcea','manifest_entries':8,'rerun_comparison':'all semantic results equal; only seconds_diagnostic_only excluded'}
}
for name,s in seals.items():
 if 'sha256' in s:assert h(A/name/s['manifest'])==s['sha256']
 count=0
 for line in (A/name/s['manifest']).read_text().splitlines():
  digest,path=line.split('  ',1);assert h(A/name/path)==digest,(name,path);count+=1
 assert count==s['manifest_entries']
 s['source_directory_copied_byte_identically']=True
jwrite(A/'ASSEMBLY_VERIFICATION.json',{'verified_utc_date':'2026-10-09','baseline_library_file_id':'[private-id]','baseline_library_version':9,'original_archives_reidentified':6,'new_archive_streams':2,'duplicate_archive_streams_referenced':4,'source_manifest_entries_static_verified':114,'initial_source_python_syntax_checks':45,'new_distinct_first_level_contents':31,'uploaded_code_executed_or_imported':False,'sealed_audits':seals,'triage_historical_manifest_note':'The initial inspection manifest includes working-file snapshots; final audit seals and this addition manifest govern final packaged bytes.','library_write_performed_by_assembly':False})
# Candidate status files; every previous root byte is preserved in checkpoint_history/v9_*.
shutil.copy2(W/'new_readme.md',P/'README.md')
checkpoint=(A/'INTEGRATED_RESULTS.md').read_text()
for name in ['tensor_audit','graph_audit','divisor_audit']:
 checkpoint=checkpoint.replace('`'+name+'/', '`additions/1954/'+name+'/')
checkpoint=checkpoint.replace('`source_records.json`','`additions/1954/source_records.json`')
(P/'CURRENT_CHECKPOINT.md').write_text('# Current Fourier research checkpoint: version 10\n\n'+checkpoint+'\n# Retained version-9 checkpoint\n\nThe following historical checkpoint is preserved unchanged. Its six-source pending status is superseded by the completed update above.\n\n'+(B/'CURRENT_CHECKPOINT.md').read_text())
status=json.loads((B/'ADDITIONS_STATUS.json').read_text());status['later_source_uploads']=34;status['pending_direct_upload_records']=0
status['batches'].append({'received_utc_minute':'2026-10-09T19:54Z','source_origin':'direct user attachments','topic':'Six-source divisor-spectrum and HERO17 update, including four exact resends','status':'complete: static provenance and three independent mathematical audits; prior duplicate-source corrections retained','path':'additions/1954/','source_record_count':6,'new_archive_streams':2,'byte_identical_prior_archives':4,'sources':records,'new_audit_paths':['additions/1954/divisor_audit/','additions/1954/tensor_audit/','additions/1954/graph_audit/']})
status['candidate_state']={'library_file_id':'[private-id]','based_on_library_version':9,'intended_next_version':10,'status':'verified local candidate; Library replacement not performed by assembly'}
status['bounded_audit_status']='All six 19:54 attachments are resolved: four exact resends retain approved audits and two new archives have three completed independent audits. Structured exact extensions, selected-split misses and a false approximate-planner certificate are explicitly scoped. No unrestricted exact FFT advance or novelty certification.'
status['new_mathematical_audits_completed_in_v10']=3
jwrite(P/'ADDITIONS_STATUS.json',status)
pending=json.loads((B/'PENDING_ADDITIONS.json').read_text());pending['status']='The bounded six-source 19:54 review is complete; no source audit remains pending in this candidate. The documented dispatcher defect is not an implemented repair.';pending['as_of_utc']='2026-10-09T20:15:00Z';pending['tasks']=[]
pending['resolved_in_this_candidate']=[{'received_utc_minute':'2026-10-09T19:54Z','topic':'Six-source static and mathematical integration','source_record_count':6,'status':'completed','path':'additions/1954/','source_index':'additions/1954/source_records.json','independent_new_audits':3,'inherited_duplicate_audits':4}]
pending['prior_resolutions_preserved_in']='checkpoint_history/v9_PENDING_ADDITIONS.json'
jwrite(P/'PENDING_ADDITIONS.json',pending)
ver='''\n\n## Master version-10 candidate: six-source 19:54 update\n\nThe exact version-9 archive was verified at 44,446,702 bytes, 3,726 regular files and SHA-256 cfa3c36da73eb7b494e0949f982a20a4f0c3039bc8b778b56468237731f01bc5. Its CRC and all 3,724 active manifest entries passed. Every version-9 root file, including both root manifests, is preserved unchanged under checkpoint_history/v9_*. Earlier addition bytes remain unchanged.\n\nAll six new upload identities resolve: four byte-identical originals already exist in the master, and two genuinely new archive streams are preserved in additions/1954/originals/. The static pass verified six archive CRCs, 114 embedded hash entries and 45 source Python syntax trees, with 31 distinct byte-new first-level contents. The initial static snapshot is separate from final mathematical approval and contains some now-historical audit working-file hashes. Final seals supersede those working-file rows.\n\nThe three complete independent reports and their proofs were reviewed before inclusion. All sealed files were copied byte-identically. Their newly authored checkers passed isolated relocated reruns: graph results match completely, divisor results match after excluding runtime_seconds (with AST evidence byte-identical), and tensor results match after excluding seconds_diagnostic_only. Divisor's 31, graph's 7 and tensor's 8 sealed manifest entries all verify. No uploaded program, test, helper or bytecode was imported, executed or compiled; static source AST parsing and hashing are not execution.\n\nNew proofs remain model-scoped: selected-split exact recognition, separately budgeted structured growing-rank designs, bounded-square-multiplier phases, sharp graph support and output-rank fallback, and least-prime covariance spectra. The uploaded adaptive planner is explicitly uncertified after an exact aggregation counterexample and block/error-budget mismatches. The selected-divisor coverage miss is preserved. No general exact FFT breakthrough, bit-complexity improvement, floating-recognition stability or novelty claim follows.\n\nBoth active root manifests and the addition manifest are regenerated for the packaged bytes. This local assembly performs no Library mutation; any replacement must retain the existing master identity and be guarded against current version 9. Baseline coverage limits remain unchanged.\n'''
(P/'VERIFICATION.md').write_text((B/'VERIFICATION.md').read_text()+ver)
# Manifest utility deliberately excludes its own names.
def manifest(root,names=('SHA256SUMS',)):
 lines=[]
 for f in sorted(root.rglob('*')):
  if f.is_file() and str(f.relative_to(root)) not in names:
   lines.append(h(f)+'  '+f.relative_to(root).as_posix())
 data='\n'.join(lines)+'\n'
 for name in names:(root/name).write_text(data)
 return len(lines)
addition_entries=manifest(A)
# Compact supplement has one exact update tree, inherited proof reports, and no old recursive archives.
S=W/'fft_six_source_verified_20261009';S.mkdir();shutil.copytree(A,S/'update');(S/'inherited_reports').mkdir()
inherited=[('additions/1930_sparse/AUDIT_REPORT.md','sparse_defect_AUDIT_REPORT.md'),('additions/1930_sparse/ARBITRARY_SPARSE_REPAIR.md','sparse_defect_ARBITRARY_SPARSE_REPAIR.md'),('additions/1930_phase26/PHASE26_AUDIT.md','PHASE26_AUDIT.md'),('additions/1930_v13/AUDIT_AND_EXTENSION.md','mixedradix_v13_AUDIT_AND_EXTENSION.md')]
irecs=[]
for old,new in inherited:
 shutil.copy2(P/old,S/'inherited_reports'/new);irecs.append({'master_path':old,'supplement_path':'inherited_reports/'+new,'sha256':h(P/old),'status':'previously approved report, unchanged; not a newly rerun audit'})
irecs.append({'master_path':'additions/1916/COMPOSITE_GREEN_AUDIT.md','supplement_path':'update/divisor_audit/prior_evidence/COMPOSITE_GREEN_AUDIT.md','sha256':h(P/'additions/1916/COMPOSITE_GREEN_AUDIT.md'),'status':'previously approved report already bundled as divisor audit prior evidence'})
assert h(S/irecs[-1]['supplement_path'])==irecs[-1]['sha256']
jwrite(S/'INHERITED_REPORTS.json',irecs)
(S/'README.md').write_text('''# Six-source research supplement\n\n9 October 2026. Start with `update/INTEGRATED_RESULTS.md`.\n\n- Exact structured recognition is valid on specified selected splits; the default dispatcher misses a concrete alternate-split fast path.\n- An independent output-rank convolution fallback strictly extends the original fixed-state guard, with all outputs and costs charged.\n- Divisor v13's approximation bound is inherited and weaker than an existing certificate. Its adaptive planner's advertised guarantee is false; a separate least-prime covariance spectrum is proved.\n- Four exact resends retain their existing corrections.\n\nThere is no general exact FFT breakthrough or novelty certification.\n\n## Contents\n\n`update/` contains the three sealed independent audits, portable checkers/results, two new original archive streams, extracted source evidence, unchanged initial static triage and all six Library request mappings. Only independent audit checkers were executed. Uploaded programs are data only.\n\n`inherited_reports/` contains unchanged earlier reports supporting the duplicate-source dispositions. The composite report is already present under `update/divisor_audit/prior_evidence/`. `INHERITED_REPORTS.json` records every copied report hash and original master path. Earlier full proof/check suites remain in the master.\n\nThe four byte-identical old archives are deliberately not recursively copied into this small supplement; `update/source_records.json` identifies their exact unchanged locations in master version 10, along with the new upload identities. This supplement is not a replacement for the full historical master.\n\nUse each audit README for reproduction. Preserve seals by rerunning the tensor/divisor checkers from copies, since they rewrite result diagnostics. The master Library identity remains [private-id].\n''')
supplement_entries=manifest(S)
root_entries=manifest(P,('SHA256SUMS','SHA256SUMS.txt'))
# No baseline file except the seven allowed root status/manifest files changes.
allowed={'README.md','CURRENT_CHECKPOINT.md','ADDITIONS_STATUS.json','PENDING_ADDITIONS.json','VERIFICATION.md','SHA256SUMS','SHA256SUMS.txt'};changed=[];unchanged=0
for f in B.rglob('*'):
 if f.is_file():
  rel=f.relative_to(B);q=P/rel;assert q.is_file()
  if h(q)==h(f):unchanged+=1
  else:assert str(rel) in allowed,rel;changed.append(str(rel))
for f in B.iterdir():
 if f.is_file():assert h(f)==h(P/'checkpoint_history'/('v9_'+f.name))
for root,filename in [(P,'SHA256SUMS'),(P,'SHA256SUMS.txt'),(A,'SHA256SUMS'),(S,'SHA256SUMS')]:
 for line in (root/filename).read_text().splitlines():
  digest,rel=line.split('  ',1);assert h(root/rel)==digest,rel
for r in records:
 f=P/r['master_archive_path'];assert h(f)==r['sha256'] and f.stat().st_size==r['bytes']
 with zipfile.ZipFile(f) as z:assert z.testzip() is None
for f in A.rglob('*.py'):ast.parse(f.read_text())
def makezip(root):
 out=root.with_suffix('.zip')
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for f in sorted(root.rglob('*')):
   if f.is_file():z.write(f,f.relative_to(root.parent).as_posix())
 with zipfile.ZipFile(out) as z:
  assert z.testzip() is None
  n=len(z.infolist());assert n==len([f for f in root.rglob('*') if f.is_file()])
 return {'path':str(out),'bytes':out.stat().st_size,'sha256':h(out),'regular_files':n,'crc':'PASS'}
result={'status':'verified local candidate, no Library writes','guard_library_file_id':'[private-id]','guard_current_version':9,'intended_next_version':10,'master':makezip(P),'supplement':makezip(S),'baseline_files_unchanged':unchanged,'baseline_files_changed':sorted(changed),'historical_root_files_preserved':11,'root_manifest_entries':root_entries,'addition_manifest_entries':addition_entries,'supplement_manifest_entries':supplement_entries,'new_audits':seals}
jwrite(W/'DELIVERY_METADATA.json',result);print(json.dumps(result,indent=2))
