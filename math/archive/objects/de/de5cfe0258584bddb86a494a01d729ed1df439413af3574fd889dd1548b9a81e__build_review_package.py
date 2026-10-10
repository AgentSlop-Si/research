"""Reviewer packaging only; handles source as inert bytes/text and review JSON."""
from pathlib import Path
import json,hashlib,datetime,re
O=Path(__file__).parent
sha=lambda b:hashlib.sha256(b).hexdigest()
rows=json.load(open(O/'ASSIGNED_SOURCES.json'));provenance=json.load(open(O/'PROVENANCE.json'));notes={}
for line in (O/'PER_SOURCE_NOTES.txt').read_text().splitlines():
 i,role,findings=line.split('|',2);notes[int(i)]=(role,findings)
assert len(rows)==len(notes)==50
review=[]
for r,p in zip(rows,provenance):
 b=(O/r['snapshot']).read_bytes();assert sha(b)==r['sha256'];n=len(b.decode().splitlines());assert n==r['line_count']
 role,findings=notes[r['index']]
 review.append({'review_id':'S%02d'%r['index'],'index':r['index'],'sha256':r['sha256'],'representative_path':r['representative_path'],'bytes':len(b),'lines':n,'role':role,'full_source_read':True,'full_static_inspection':True,'read_method':'Complete first-to-last line-numbered inert text inspection; no supplied execution/import/compile/AST','line_ranges':[[1,n]],'line_referenced_findings':findings,'source_snapshot':r['snapshot'],'line_numbered_snapshot':'line_numbered/%02d.txt'%r['index'],'archive_provenance':p,'authorship':'origin_unresolved; exact archive identity is verified, authorship is not established by an audit filename','dependency_reconciliation':'DEPENDENCY_RECONCILIATION.json','fresh_checks':'FRESH_REVIEWER_CHECKS.json','stored_checks':'STORED_EVIDENCE_CHECKS.json','source_executed_in_review':False})
(O/'SOURCE_REVIEWS.json').write_text(json.dumps(review,indent=2))
# Freeze registry at completion and calculate additive credit against BOTH snapshots.
regpath=Path('post_v22_review_registry_0308/ADDITIVE_CODE_COVERAGE.json');regbytes=regpath.read_bytes();(O/'REGISTRY_END_SNAPSHOT.json').write_bytes(regbytes);end=json.loads(regbytes);start=json.load(open(O/'REGISTRY_START_SNAPSHOT.json'))
inv=json.load(open(O/'INVENTORY_SNAPSHOT.json'));inv=inv.get('rows',inv) if isinstance(inv,dict) else inv
frozen={r['sha256'] for r in inv if r.get('static_inspection_complete')};prior=frozen|{r['sha256'] for r in start['rows'] if r.get('full_static_inspection')}|{r['sha256'] for r in end['rows'] if r.get('full_static_inspection')}
new=[r['sha256'] for r in rows if r['sha256'] not in prior];overlap=[r['sha256'] for r in rows if r['sha256'] in prior]
assignment=json.load(open(O/'ASSIGNMENT.json'))
(O/'batches').mkdir(exist_ok=True);batch_for={}
for bn in assignment['batch_names']:
 raw=(Path(assignment['batch_directory'])/bn).read_bytes();(O/'batches'/bn).write_bytes(raw)
 for item in json.loads(raw)['rows']:batch_for[item['sha256']]=bn
assert all(r['sha256'] in batch_for for r in rows)
batchhashes={n:sha((Path(assignment['batch_directory'])/n).read_bytes()) for n in assignment['batch_names']}
now=json.load(open(O/'REVIEW_CLOCK.json'))['completed_utc'];revhash=sha((O/'SOURCE_REVIEWS.json').read_bytes())
coverage={'package':str(O),'completed_utc':now,'assigned_batches':assignment['batch_names'],'assigned_batch_hashes':batchhashes,'fully_read_hashes_this_review':[r['sha256'] for r in rows],'new_full_read_hashes':new,'new_coverage_credit':len(new),'previously_covered_hashes':overlap,'total_source_bytes_read':sum(r['bytes'] for r in review),'total_source_lines_read':sum(r['lines'] for r in review),'all_assigned_new_source_reads_complete':True,'all_research_material_checks_finished':False,'dependency_closure_complete':False,'source_execution':'none','source_import_compilation_syntax_parse':'none','registry_modified_by_this_review':False,'registry_start_count':start['current_full_static_reads'],'registry_end_count':end['current_full_static_reads'],'registry_start_sha256':sha((O/'REGISTRY_START_SNAPSHOT.json').read_bytes()),'registry_end_sha256':sha(regbytes),'scope_note':'Complete static review of all50 exact assigned hashes. Auxiliary artifacts are reconciled for provenance, stored results and bounded independent mathematical checks; unassigned candidate dependencies are not credited as read. This does not close the whole research inventory or prove all claims. Existing inventory AST metadata was copied as data only; no fresh AST parsing occurred.','rows':[]}
for r,src in zip(rows,review):coverage['rows'].append({'review_id':src['review_id'],'sha256':r['sha256'],'representative_path':r['representative_path'],'batch':batch_for[r['sha256']],'bytes':src['bytes'],'lines':src['lines'],'full_static_inspection':True,'static_inspection_complete':True,'full_source_read':True,'line_ranges':src['line_ranges'],'source_executed_in_review':False,'evidence_file':'SOURCE_REVIEWS.json','evidence_sha256':revhash,'snapshot':r['snapshot'],'new_coverage_credit':r['sha256'] in new})
(O/'COVERAGE.json').write_text(json.dumps(coverage,indent=2))
# Confirm the previous sealed package still matches its original content manifest.
old=Path('nested_macro_source_review_0447');old_manifest=(old/'SHA256SUMS.txt').read_bytes();old_checks=[]
for line in old_manifest.decode().splitlines():
 h,path=line.split('  ',1);old_checks.append(sha((old/path).read_bytes())==h)
assert all(old_checks)
(O/'PRIOR_PACKAGE_PRESERVATION.json').write_text(json.dumps({'package':str(old),'manifest_sha256':sha(old_manifest),'files_checked':len(old_checks),'all_original_manifest_entries_unchanged':True,'prior_package_modified':False},indent=2))
# Broad dependency candidates are not all required at runtime. Explicitly retain uncertainty.
deps=json.load(open(O/'DEPENDENCY_RECONCILIATION.json'))
unique={x['sha256'] for x in deps['related_code_candidates']};unread=unique-prior-{r['sha256'] for r in rows}
(O/'RECONCILIATION_SUMMARY.json').write_text(json.dumps({'assigned_hashes':50,'source_bytes':coverage['total_source_bytes_read'],'source_lines':coverage['total_source_lines_read'],'start_registry':start['current_full_static_reads'],'end_registry':end['current_full_static_reads'],'new_credit':len(new),'overlap':overlap,'archive_occurrences_verified':50,'source_archives':len({p['archive_sha256'] for p in provenance}),'collected_evidence_objects':len(json.load(open(O/'EVIDENCE_INDEX.json'))),'stored_manifest_records':425,'stored_manifest_matches':423,'stored_manifest_exceptions':2,'stored_hash_references':8,'input_receipts_verified':21,'stored_data_checks':315,'stored_data_checks_passed':314,'expected_flagged_check':'stored_manifest_entries; two accurately documented historical manifest exceptions','fresh_independent_checks':60,'fresh_independent_checks_passed':60,'lexical_import_lines':len(deps['imports']),'candidate_code_occurrences_rehashed':len(deps['related_code_candidates']),'candidate_unique_hashes':len(unique),'unread_candidate_unique_hashes_at_end':len(unread),'all_dependency_candidates_read':False,'source_execution':'none'},indent=2))
report='''# Complete inert source review: reuse batch 0501_b

## Decision summary

All 50 assigned exact source hashes were read from first line to last: **398,794 bytes, 9,286 lines**. Exact source snapshots, line-numbered copies and per-source findings are included. No supplied program was executed, imported, compiled or AST-parsed. Independent checks use newly authored generic matrix arithmetic, primitive arithmetic and stored-data reconciliation only.

The batch supports useful structured reuse, several correctly scoped exact identities, and numerical engineering repairs. It does **not** establish a fresh arbitrary-input exact sub-N-log-N FFT, an unbounded integer-multiplication improvement, a complete finite-precision guarantee, or global novelty. The main practical issues are the unchecked native buffer contract, numerical replay/rebase limitations, incomplete planner-memory guards, older organizer accounting, and inherited provenance records that no longer describe their copied subtrees exactly.

## Findings that change how to use the code

1. **Native pointer boundary needs a strict buffer contract.** S31 L33–38 pass raw pointers and len(x) to C++ without checking complex128 dtype, one-dimensionality or contiguity. S32 L115–127 and L145–151 read/write 2N doubles. A length-eight float64 output has64 bytes while the native code requires128; a wrong dtype/stride can cause out-of-bounds access. The archived benchmark itself uses the intended layout. This finding is static and was not reproduced by dereferencing unsafe pointers.
2. **Literal-zero pruning is still floating arithmetic.** S32 L126–142 scale every component by the global maximum before zero checks. Independent scalar arithmetic confirms 1e-200/1e200 becomes0 although a two-point unitary imaginary output of about7.07e-201 is representable. Homogeneous-scale and unit-scale tiny-branch controls in S31/S34 do not cover this mixed-range case. This does not refute the ideal-arithmetic pruning theorem; it limits component-preservation claims.
3. **Passing tests can document a known wrong numerical answer.** S11 L141–149 intentionally check that represented coefficient1 yields cached answer0 after cancellation, then rebase yields1. The stored diagnostic and an independent scalar witness agree. Coalescing removes event-count dependence, but does not make cached difference arithmetic uniformly stable. S13/S15/S21 also need result-overflow and requested-versus-represented increment caveats.
4. **A no-sample planner can exceed its plan budget.** S19 L173–178 falls back to radix N when no phase table fits and constructs the pruned plan anyway. With prime N=1009, three bins and a16-byte budget, the minimum phase payload is48 bytes and the heuristic selects the pruned plan. Multiple productive candidates can coexist, so individual-plan limits do not bound peak memory. Calibration-result reuse additionally relies on a digest alone, whereas S13 verifies full array equality after hashing.
5. **Version-specific organizer claims matter.** S25 L10–13 claim producer updates remain no more expensive, but L427–435 invoke greedy replanning inside them. Its partition history is an unbounded list (L62,L260), omitted from reported storage. Archived data show5457 cluster-metric calls for32 consumers and201 retained partitions after200 additional replans. S04 corrects the nonconstant-work description, bounds history/cache behavior, replays only the unread suffix and publishes only the requested member even on refresh. Neither greedy grouping scheme proves global optimality.
6. **Exact algebra and complete bills remain separate.** S26 has a valid closed decimation family but three recursive actions and growing filters lead to Theta(N^1.79248...), slower than the existing ordinary-FFT comparator. S28's rank-one feedback and gain updates avoid extra T calls under coordinate observation, but its online scalar counts exclude baseline kernel generation, circuit emission and reciprocal setup; the README discloses those additional costs. S46's exact integer backend has a fixed modulus65537 and a finite digit bound. Its arithmetic objective includes discovery arithmetic but tracks comparisons/copies/addressing separately.
7. **Two inherited manifest exceptions are real, localized and explained.** Of425 stored manifest records,423 match their explicitly resolved archive location. The copied phase6 test log has changed bytes relative to its inherited manifest; the copied sum-product subtree omits one benchmark log still listed by its inherited manifest. Both expected historical artifacts were located and independently rehashed in original/recovered archives. All50 assigned source-byte identities match their selected archive occurrences. These log exceptions do not imply a source hash mismatch or establish malicious change.

## Mathematical scope and independent confirmation

The newly written checker performs60 separately recorded checks, all passing. It uses generic exact dense matrix multiplication/inversion/rank over F97 at N=2,4,8,16 rather than any supplied FFT, gate interpreter, recursive evaluator or resolvent solver. It confirms the finite q-Weyl corner, nilpotence, complete Fourier factorization, both covariance identities, finite resolvent sums, tail ranks, normalized decimation block closure and rank-one closed-graph solution. Other checks cover the rational N=2 finite-exponential counterexample, reduced-network intersection coefficients, the local sketch random-variable identity over64 states, and median order-statistic domination over3125 real five-tuples. These are bounded independent confirmations, not replacements for all-size proofs or uninspected dependencies.

- **Phase9 circuits/range products/organizers (S00–S04):** persistent algebra and selected-output reuse; prepared bases, output copying, metadata and cache policies matter. Tests cover deep graphs, zero factors/bins, finite-field export and bounded replay.
- **Predecode median (S05–S06):** randomized all-output approximation at factorizable lengths. Decoder scheduling lowers its operation proxy, with a polylogarithmically growing factor above ||x||2/sqrt(N); structured exact recovery is probabilistic in ideal arithmetic. The local variance/median mathematics is consistent with independent checks. One-row equivalence tests share their implementation path and therefore add little independent evidence. There is no fixed-roundoff-accuracy or optimized-library timing win here.
- **Reduced-center network (S07):** exact scalar reversible network and dimension calculations, expressly short of tensor recursion or a full published theorem.
- **Hardened relation/query layers (S08–S25):** meaningful fixes for sparse coalescing, history scanning, ownership, invalid cached strategies and atomic rejection. Reports distinguish original, partial overlays and final derivatives. Remaining stability, topology and planner-accounting restrictions are concrete.
- **Finite q-Weyl families (S26–S30,S35–S43,S48–S49):** exact fields with supplied primitive roots; corners and finite polynomial truncation are essential. Related-query transport, rank-one feedback, a linear single resolvent and rank-at-most-r tails do not make arbitrary full transforms cheap. Several comparators explicitly use ordinary radix-two FFTs and additional2N roots.
- **Native energy pruning (S31–S34):** floating full-output implementation, cold algorithmic setup but warmed code/hardware. Ideal maximum-error criterion is weaker than relative-L2 fidelity; zero-only mode is still numerical.
- **Integer correction graph (S44–S47):** finite exact products for shared B and verified candidate differences. Complete discovery is O(Q^2 n); supplied sparse candidates cost O(En); the planner remains O(Q^2). Warm cache keys detect changed identities, not corruption of cached coefficients/context.

## Stored evidence reconciliation

148 auxiliary evidence objects were copied and hashed, with additional historical/receipt snapshots. Data-only reconciliation made315 checks:314 passed, and one deliberately flags the two manifest exceptions described above. All other checked counts/formulas/raw timing summaries reconcile. This review did not rerun the archived programs.

| Family | Recorded population / interpretation |
|---|---|
| Phase9 suites | 9 suite records,253 unittest cases across inherited/current code; not253 new source files |
| Predecode median | 10 archived tests;4 shared-path equivalence checks,18 variance configurations,36 median comparisons,12 sparse configurations totaling144 trials,5 moment configurations |
| Coalesced view | 16 archived tests; cancellation limitation is intentionally among the passes |
| Phase7 | 57 supplied tests; original adversarial run11 tests with9 failures and1 error; patched/packaged run80 tests passes |
| Query v2 / v3 | v2 grows30 to40 tests; v3 original34, core-overlay44, final47; organizer sweep10152 outputs |
| Fixed pair | 720 independent fork cases,3600 stream steps and3600 sibling checks |
| Decimation / boundary / grading | Each13 configurations and138 bases; decimation224 split bases; grading552 related outputs |
| Feedback | 36 configurations,840 full-state bases for each initial/gain map,144 random states,focused rejection/zero controls |
| Fast H(C) / resolvent | 15 configurations,266 bases,843 shifted-resolvent vectors,75 chain outputs |
| Tail aggregate | 48 configurations,1318 bases,96 default/arbitrary-polynomial mixed-vector uses,52 aggregate and42 full-comparator checks |
| Integer correction | 195 main and96 numeric-shift products;125 exhaustively enumerated spanning trees for one four-query scalar-objective case |

Native measurements have147 method/workload rows and1323 raw timing samples, plus64 dynamic-range checks. All reported medians, quartiles and ratios were recomputed from stored raw samples. Among63 approximate cases,31 return all zeros; those account for7 of8 median NumPy wins. The24 nonzero cases with relative-L2 error <=1e-10 have21 median wins versus the faster native baseline and one marginal NumPy win; none have nonoverlapping IQRs versus NumPy. The useful group therefore supports a local native-baseline result, not a demonstrated robust NumPy speedup. Numerical verification reports127 bases and762 method comparisons; one threshold control measures0.12500000000000003 against nominal0.125, explicitly covered by test tolerance.

## Provenance, dependency and coverage boundaries

Every source has a full SHA-256, exact snapshot, byte/line counts, archive SHA/member index, and line-referenced findings below and in SOURCE_REVIEWS.json. Five selected containing archives supply the50 verified occurrences. Eight stored exact-source/document hash references and21 declared input receipts were reconciled; known archives and resolved member bytes were rehashed. Authorship remains origin_unresolved: file names such as independent_review, stored PASS labels and comments do not establish who authored exact bytes. External repository/commit claims in stored documents were not refreshed or certified, and no global novelty search was performed.

Lexical import discovery records305 import lines and343 archive-byte-verified candidate occurrences representing132 distinct code hashes. This is a candidate catalog, not asserted runtime resolution: sys.path overlays, same-name modules and external installed versions require care. Some candidates remain outside full-read coverage. Existing frozen inventory metadata may include old AST fingerprints; these were merely copied as metadata, and no AST parser was used in this review.

All assigned reads are complete. The whole research-material inventory and dependency closure remain open and are explicitly marked false in COVERAGE.json. Central coverage files and the previous sealed0447 package were not edited; the old400-file content manifest was rechecked unchanged. The completion registry snapshot and exact additive credit appear in COVERAGE.json and RECONCILIATION_SUMMARY.json.

## Files to use

- COVERAGE.json: additive exact-hash credit and completion facts
- SOURCE_REVIEWS.json: per-source roles, full-read intervals, findings and provenance
- sources/ and line_numbered/: exact inert snapshots and citation copies
- PROVENANCE.json, DEPENDENCY_RECONCILIATION.json, INPUT_RECEIPT_RECONCILIATION.json: byte identity and dependency candidates
- STORED_EVIDENCE_CHECKS.json, STORED_MANIFEST_RECONCILIATION.json, MANIFEST_EXCEPTIONS.json, LOG_STATUS_CENSUS.json: stored claim reconciliation
- FRESH_REVIEWER_CHECKS.json and independent_math_checks.py: bounded independent confirmation and counterexamples
- SHA256SUMS.txt and SEAL.json: final package content seal

## Per-source full-read findings
'''
for r in review:
 report+='\n### '+r['review_id']+' — '+r['role']+'\n\n'
 report+='Path: `'+r['representative_path']+'`  \nSHA-256: `'+r['sha256']+'`  \nComplete read: lines1–'+str(r['lines'])+', '+str(r['bytes'])+' bytes.  \n'
 report+='Archive: `'+r['archive_provenance']['archive_sha256']+'`, member index'+str(r['archive_provenance']['member_index'])+'.  \n'
 report+='Source citations refer to [the line-numbered snapshot]('+r['line_numbered_snapshot']+').\n\n'+r['line_referenced_findings']+'\n'
(O/'MAIN_REPORT.md').write_text(report)
print(json.dumps({'sources':len(review),'bytes':coverage['total_source_bytes_read'],'lines':coverage['total_source_lines_read'],'new_credit':len(new),'overlap':overlap,'registry_end':end['current_full_static_reads'],'unread_candidate_hashes_at_end':len(unread),'prior_package_files_unchanged':len(old_checks)},indent=2))
