"""Review-owned inert evidence packager. Never imports/executes supplied sources."""
import hashlib, json
from pathlib import Path

OUT=Path('pending_code_review_0301')
AUDIT=Path('code_coverage_audit_0228')
MASTER=Path('fft_research_master_20261009')
sha=lambda b:hashlib.sha256(b).hexdigest()
def dump(name,obj):
    (OUT/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

inventory=json.loads((AUDIT/'CODE_COVERAGE_INVENTORY.json').read_text())
idx={x['sha256']:x for x in inventory}
selected=json.loads((OUT/'SELECTION.json').read_text())
extra='e56d0718ebc18e85ac4ea2d33568492a35eef10d62244cdb13ca8c86160425af'
hashes=[r['sha256'] for r in selected['rows']]
if extra not in hashes:hashes.append(extra)

# Concise scope reports. REVIEW.md supplies detailed mathematical reasoning.
notes={
'07bbebda0dea':{
 'sections':[(1,58,'Graph maps, half translations and commutator conventions'),(59,107,'Modular DFT, arithmetic guard and polynomial certificates'),(108,171,'Cycles, Green application and dense symmetry'),(172,226,'Breaking budget, spectrum and CLI'),(227,309,'Modular ranks, finite-rank defects and twirl')],
 'math':'Cycle closure, inverse commutator identity, product budget and rank inequalities are consistent under the declared permutation, field and invertibility conditions.',
 'model':'Restricted two-layer mixed-axis Green networks; dense validation and symmetry obstruction, not a general FFT lower bound.',
 'entrypoint':'Twelve modular commutator cases only: s in 2,4,8,16 and axes x,y,xy.',
 'gaps':['CLI omits Green solves, complex spectra, breaking budgets, finite-rank defects and twirl.', 'Commutator indexing assumes an involution.', 'Returned lower_rank_bound is conservative rather than axis-sharp for y/xy.', 'Int64 modular products assume reduced entries; arbitrary custom fields and malformed permutations are not covered.'],
 'deps':[]},
'175f24d4c644':{
 'sections':[(1,79,'FFTW ABI, modular chirps and resource wrapper'),(80,116,'Engine construction and compression'),(117,175,'Blelloch scan, row reconstruction and materialized reference'),(176,211,'Three-grid majority and error/timing reducers'),(212,259,'Full benchmark main')],
 'math':'The finite chirp difference telescopes to the two compressed-FFT boundary terms; odd a and dyadic N give a -1 cycle gauge and a half-total closure seed.',
 'model':'Approximate chirp row using a short FFT, O(N) compression/scan and O(K log K) short transform; fixed finite randomized benchmark.',
 'entrypoint':'One random complex vector and identity row state per dyadic N from 4096 to maxN; five timing reps and three streamed trials.',
 'gaps':['Errors are only printed, with no correctness threshold or failing exit.', 'std::max error reducer can hide NaNs.', 'No demonstrated probability/confidence or all-input approximation guarantee.', 'Constructor divides by M before checking validity; input/state/rows validation is incomplete.', 'FFTW ABI and build/runtime not tested; timings exclude root/plan setup and have allocation asymmetry.'],
 'deps':[]},
'18ad370e5279':{
 'sections':[(1,67,'Field/root/permutation utilities'),(68,124,'Two-sided Fourier core and pair support tests'),(125,158,'Forced sharpness witness'),(159,186,'Hybrid tests and result-producing CLI')],
 'math':'Finite-field roots and factor orientations are consistent; chord witness parameters enforce the common projective ratio algebraically.',
 'model':'Odd chord/support and prime hybrid finite controls; characteristic-zero full spark is an external theorem, not a consequence of these finite tests.',
 'entrypoint':'280 random odd-size stress cases, 14 forced witnesses and 80 prime hybrid cases.',
 'gaps':['Random dense fixtures rarely stress sparse extremal bounds.', 'The aa!=bb or True clause is tautological.', 'Finite-field tests do not prove characteristic-zero full spark.', 'Assertions disappear under Python -O.'],
 'deps':[]},
'25748f16e3a9':{
 'sections':[(1,64,'Character/weighted matrix fusion'),(65,108,'Dense tests and early main'),(109,150,'Permutation powers and cyclic solve'),(151,185,'Vector packet fusion and apply tests')],
 'math':'Character orthogonality and weight-DFT normalization are consistent for 0<=s<b and nonsingular denominators; vector orientation matches the co-archived utility.',
 'model':'Cyclotomic compression identity. General binary permutation powering adds O(N(log b+log s)) work unless exponents are bounded/precomputed.',
 'entrypoint':'Twelve dense n,b cases with all character residues and one weighted packet each; vector test function is not called by this main.',
 'gaps':['Direct s is periodic modulo b but fused s is unreduced; nonsingular s=b counterexample.', 'Negative permutation exponents never terminate in the right-shift loop.', 'Singular vector-test cases advance to the next s without requiring the nominal 48 records.', 'Local algebra dependency has only selected excerpt inspection in this package.'],
 'deps':['28a17bd5e9ba61008c59baaf37131b44e71e421dab59963ac7bdde1115faa3d7']},
'277307a943bf':{
 'sections':[(1,45,'Phase-rank and outer perturbation bounds'),(46,86,'Root-phase Green and exact four-point control'),(87,103,'Numerical gauge audit and main'),(104,149,'Full phase rank, cross-ratio and angle extensions')],
 'math':'The rank-distance and inverse-perturbation formulas are coherent; integer-root Green gauge and half-root sign-matrix descriptions match the companion orientation.',
 'model':'Positive/low-phase-rank bridge obstructions with near-identity outer factors, plus specific complex cyclic controls.',
 'entrypoint':'Five printed complex gauge audits and one exact N=4 cross-ratio assertion.',
 'gaps':['Main does not assert gauge-error or measured-rank targets.', 'Later full-rank/cross-ratio and general-angle helpers are not called by main.', 'phase_rank and inequivalence flags in the half-root function are theorem-derived constants, not computed decisions.', 'Cross-ratios are sampled on four rows/columns; angle rank criterion is thresholded numerical demonstration.'],
 'deps':[extra]},
'282211bf43bc':{
 'sections':[(1,19,'Gate statement and dependencies'),(20,42,'Dense matrix helpers and sparse inverse'),(43,81,'Random factors, sandwich identity, rank gate and CLI')],
 'math':'The ordered identity AXYD=(A+B)B^-1 C^-1(C+D) and Schur complement signs are correct under invertibility.',
 'model':'Dense finite-field checker for two Green-sum layers; no candidate factorization or universal FFT.',
 'entrypoint':'One random nonsingular candidate each at N=4,8,16; sandwich residual identity asserted.',
 'gaps':['No successful Fourier factorization fixture.', 'Rank gate and exact residual are reported separately rather than their equivalence asserted.', 'General shape/root/field contracts are not validated.', 'Only selected cycle_minor_gate excerpts are source-inspected here.'],
 'deps':['56364bdad62069750989f7d24d4ed4d6ab7f3c67b5773e88fd62e55bb8c33fb1']},
'2ef756df67f6':{
 'sections':[(1,31,'Cycle ordering and cyclic Green recurrence'),(32,58,'Parameters, four-Green map, rank-one seed and dense diagnostics'),(59,87,'Weyl loss, optimizer loop and CLI')],
 'math':'Cyclic solve and negative-DFT Weyl covariance convention are consistent; seeded(e0)=v is enforced by an added rank-one term.',
 'model':'Floating-point stochastic optimizer for a four-Green-plus-rank-one map; no claim of finding an FFT.',
 'entrypoint':'Default N=12 and 35 random-probe training steps, with initial/final dense diagnostics.',
 'gaps':['Tested model includes a rank-one correction beyond four Green scans.', 'No final fit tolerance, held-out guarantee, monotonic loss or cycle nonsingularity guard.', 'Dense diagnostics include a general dense matrix product and cannot be counted as linear-work execution.', 'steps=0 accesses an empty loss list; N=0 unsupported; Torch runtime not tested.'],
 'deps':[]},
'502f2f88f41e':{
 'sections':[(1,39,'Prime and valuation helpers'),(40,81,'Displacement-shell count checks'),(82,109,'Rank and trace telescoping'),(110,138,'Parameter-grid CLI and JSON output')],
 'math':'Integer floor counts, geometric rank telescope and rational trace identity are consistent for the declared prime-power domain.',
 'model':'Finite combinatorial/formula certificate, not direct projector construction, rank computation, eigensystem verification or proof-assistant result.',
 'entrypoint':'Finite prime/exponent/mu grid bounded by max-prime, max-exponent and max-M.',
 'gaps':['Ranks/eigenvalues are supplied formulas rather than independently measured projector properties.', 'Empty parameter ranges still return PASS with zero cases.', 'certify_case does not itself validate primality; main supplies primes.', 'Stored output is not a current execution receipt.'],
 'deps':[]},
'5f2169c8f510':{
 'sections':[(1,27,'Rational scan, separated rectangle and Fourier target'),(28,70,'Random degree tests, Fourier contradictions and main')],
 'math':'The separated rectangle is appropriate to the rational recurrence; selected N=17 Fourier blocks are Vandermonde-type with distinct nodes under the default field.',
 'model':'Dense finite-field rank controls for a single rational function of a cyclic shift; no general permutation-network lower bound.',
 'entrypoint':'48 random N,d,e cases and four N=17 Fourier blocks.',
 'gaps':['No streaming implementation or all-coefficient proof.', 'Custom root/modulus correctness remains an imported dependency contract.', 'Only selected algebra_utils excerpts have been inspected here.'],
 'deps':['28a17bd5e9ba61008c59baaf37131b44e71e421dab59963ac7bdde1115faa3d7']},
'5f57fe776284':{
 'sections':[(1,30,'Complete recurrence, bit reversal, maximum and CLI')],
 'math':'Implements the stated rank recurrence with exact integers and terminating dyadic bases; independent proof of that recurrence is not in this program.',
 'model':'A recurrence evaluator, not independent Fourier cut-rank computation.',
 'entrypoint':'Prints predictions for nine sizes 4 through 1024.',
 'gaps':['No independent matrix/rank checks or assertion of the maximum formula.', 'bitrev_perm lacks a dyadic argument check.', 'predicted_qs_rank(1) takes max of an empty range.'],
 'deps':[]},
'651667742c75':{
 'sections':[(1,28,'Lift statement and sparse factors'),(29,54,'Full block matrix'),(55,79,'Direct Green product and exact rank assertion'),(80,88,'Three random fixtures')],
 'math':'Eliminating invertible stage blocks yields F-YX and gives rank(H)=(r+s)N+rank(F-YX), with correct signs and order.',
 'model':'Denominator-free entries in a dense necessary-and-sufficient checker under invertibility; not a fast factorization.',
 'entrypoint':'N,r,s = (4,2,2), (8,2,3), (8,3,2).',
 'gaps':['Invertibility is essential to the equivalence despite denominator-free entries.', 'No known successful Fourier or singular-negative fixture.', 'Nonempty lists and dimension/field compatibility are caller contracts.', 'Dense quadratic storage and generic cubic rank cost.'],
 'deps':['b2a8f46221b209a5221e9d79d9012b7079ec56925b3e055ebb7e16e182ac1c79']},
'6c8a351d4908':{
 'sections':[(1,53,'Stage construction, product prefixes/suffixes and analytic Jacobian'),(54,62,'External executable bridge'),(63,92,'Exact-witness and fresh-input checks plus main')],
 'math':'Derivative locations and surrounding factors match the parametrized product. Nonzero minors establish generic geometry in these dimensions, not Fourier image membership.',
 'model':'Full-dimensional semiseparable-stage geometry at t=N/4+1; stage count scales with N.',
 'entrypoint':'N=8,16,32, each in fields 12289 and 65537; invertible stages, 12 fresh input vectors per field and one stored Jacobian minor per field.',
 'gaps':['Native rankmod executable is not hash-bound to source/build.', 'Recovered isolated source lacks required neighboring data/binary layout.', 'No general overflow/schema/subprocess-timeout guards; supplied exact witness bounds are safe.', 'Fresh-input product checks do not independently test Jacobian derivatives.', 'No current determinant recomputation or historical-run promotion.'],
 'deps':['ac7238f040c7ffb5f9de8c357f61aea9bda1780b5f7d7e60d6faf9426f041cd7']},
'e56d0718ebc1':{
 'sections':[(1,69,'Cyclic Green recurrence, transpose and dense representation'),(70,107,'Weak outer factor and inverse'),(108,132,'Two-mask composition and triplet'),(133,168,'Sinkhorn iteration and marginal diagnostics'),(169,229,'Fourier floors, finite audit and CLI')],
 'math':'Green orientations, outer inverse algebra and Sinkhorn boundary calibration are consistent; boundary matching does not imply Fourier matching.',
 'model':'Positive cyclic Green two-mask calibration and restricted phase obstruction. O(N) field work per apply/iteration after setup, without a general iteration-count guarantee.',
 'entrypoint':'Eight sizes 4–512; dense spectral and first-column assertions only for N<=64.',
 'gaps':['No explicit convergence flag or cap failure; max_iterations=0 leaves variables uninitialized.', 'Large-size and first-row results are mainly reported, not asserted.', 'Inverse/complex-mask and explicit dense-versus-apply/transpose tests absent from this CLI.', 'inverse_apply rebuilds a sorted/validated cycle object, adding setup/comparison work to the linear-field-arithmetic claim.'],
 'deps':[]}
}

# Reconcile exact prior mapped and newer declaration coverage, also for the added companion.
prior=json.loads((OUT/'PRIOR_COVERAGE_CHECK.json').read_text())
evidence=json.loads((AUDIT/'COVERAGE_EVIDENCE.json').read_text())
prior['selected_sha256s']=hashes
prior['frozen_evidence_exact_matches']=[e for e in evidence if e.get('code_sha256') in hashes]
prior['newer_declaration_hits']=[]
for name in prior['newer_declarations_checked']:
    text=Path(name).read_text(errors='replace')
    for h in hashes:
        if h in text:prior['newer_declaration_hits'].append({'file':name,'sha256':h})
prior['added_companion_assignment']='Parent confirmed exact companion hash unassigned elsewhere and authorized it as thirteenth read.'
assert not prior['frozen_evidence_exact_matches'] and not prior['newer_declaration_hits']
dump('PRIOR_COVERAGE_CHECK.json',prior)

(OUT/'inert_source_snapshots').mkdir(exist_ok=True)
rows=[];preserved=[]
for h in hashes:
    r=idx[h];p=Path(r['local_content']);b=p.read_bytes();assert sha(b)==h
    lines=b.splitlines();n=len(lines);note=notes[h[:12]]
    sections=note['sections'];assert sections[0][0]==1 and sections[-1][1]==n
    assert all(sections[i][1]+1==sections[i+1][0] for i in range(len(sections)-1))
    snap=Path('inert_source_snapshots')/(h+'.txt');(OUT/snap).write_bytes(b)
    rootpath=MASTER/r['representative_path']
    rootmatch=sha(rootpath.read_bytes())==h if rootpath.is_file() else None
    row={
      'sha256':h,'size_bytes':len(b),'line_count':n,'names':r['names'],
      'original_master_path':r['representative_path'],'occurrences':r['occurrences'],
      'origin_class':r['origin_class'],'origin_basis':r['origin_basis'],
      'source_snapshot':{'path':str(snap),'source_path':str(p),'sha256':h,'size_bytes':len(b)},
      'status':'new_full_static_read_completed','full_static_read':True,
      'static_inspection_complete':True,'current_review_complete_read':True,
      'method':'Complete inert text reading and mathematical/runtime/test-path reasoning; no supplied source execution, import, compilation, AST parsing, or source modification.',
      'extent':{'lines':[1,n],'byte_range_half_open':[0,len(b)],'all_bytes_accounted':True,'prior_read_inherited':False,
        'current_read_sections':[{'start_line':a,'end_line':z,'subject':s} for a,z,s in sections]},
      'source_execution':False,'current_audit_uploaded_execution':'none',
      'recorded_execution':False,'recorded_execution_boundary':'No exact historical entrypoint receipt newly promoted by this static review.',
      'mathematical_trace':note['math'],'model_boundary':note['model'],'entrypoint_test_scope':note['entrypoint'],
      'findings_and_test_gaps':note['gaps'],'dependency_sha256s':note['deps'],'dependency_runtime_closure':'not established',
      'detailed_report':'REVIEW.md'
    }
    rows.append(row)
    preserved.append({'sha256':h,'code_bytes_path':str(p),'code_bytes_hash_matches':True,
      'original_master_path':str(rootpath),'original_master_hash_matches':rootmatch,'source_snapshot':str(snap),'source_snapshot_hash_matches':sha((OUT/snap).read_bytes())==h})

full={
 'review':'pending_code_review_0301','scope':'Thirteen exact 0155 source hashes: full static inspection only.',
 'source_execution':False,'source_modification':False,'rows':rows
}
dump('COVERAGE.json',full)
selected['rows']=[{**idx[h],'line_count':len(Path(idx[h]['local_content']).read_bytes().splitlines())} for h in hashes]
selected['additional_batch']='pending_batches_v2/02_addition_0155_material_coverage_and_new_results_04.json'
selected['additional_reason']='Directly imported Phase 36 companion; parent-confirmed unassigned elsewhere.'
dump('SELECTION.json',selected)

# Dependency source binding is separate from new complete-read credit.
deps=[
 ('28a17bd5e9ba61008c59baaf37131b44e71e421dab59963ac7bdde1115faa3d7',[[1,16],[36,58],[82,138]],'Selected scalar inverse, matrix multiplication/power, matrix inverse, permutation/polynomial and root routines. Other portions not read.'),
 ('56364bdad62069750989f7d24d4ed4d6ab7f3c67b5773e88fd62e55bb8c33fb1',[[170,227],[383,400]],'Selected permutation decomposition, Green submatrix/inverse and rank implementation; no whole-file credit.'),
 ('b2a8f46221b209a5221e9d79d9012b7079ec56925b3e055ebb7e16e182ac1c79',[[1,134]],'Selected graph, nonsingularity, exact Green, matrix/rank and Fourier implementation; no whole-file credit.'),
 ('ac7238f040c7ffb5f9de8c357f61aea9bda1780b5f7d7e60d6faf9426f041cd7',[[1,41]],'Supporting native source read only, deliberately outside the thirteen-hash full-coverage promotion. No compiled-binary/source equivalence or runtime credit.')
]
(OUT/'dependency_evidence').mkdir(exist_ok=True)
deprecords=[]
for h,ranges,desc in deps:
    r=idx[h];b=Path(r['local_content']).read_bytes();assert sha(b)==h
    lines=b.decode('utf-8').splitlines();excerpt='\n\n'.join('\n'.join(f'{i}: {lines[i-1]}' for i in range(a,z+1)) for a,z in ranges)+'\n'
    rel=Path('dependency_evidence')/(h+'_excerpts.txt');(OUT/rel).write_text(excerpt)
    consumers=[x['sha256'] for x in rows if h in x['dependency_sha256s']]
    bindings=[]
    for consumer in consumers:
        for a in idx[consumer]['occurrences']:
            if a['kind']!='archive_member':continue
            for bocc in r['occurrences']:
                if bocc['kind']=='archive_member' and bocc['archive_sha256']==a['archive_sha256']:
                    bindings.append({'consumer_sha256':consumer,'archive_sha256':a['archive_sha256'],'consumer_member':a['name'],'dependency_member':bocc['name']})
    assert bindings
    deprecords.append({'sha256':h,'names':r['names'],'source_path':r['local_content'],'line_ranges_read':ranges,'excerpts':str(rel),'scope':desc,'credited_as_full_static_inspection':False,'consumers':consumers,'coarchive_bindings':bindings,'binary_or_import_runtime_resolution':'not verified'})
dump('DEPENDENCIES.json',{'source_bound_support_only':deprecords,'full_read_companion':extra,'external_packages':['NumPy','Torch','SymPy','FFTW','Python and C++ runtime/toolchains'],'runtime_closure':'Not established; no executable or import was invoked.'})

# Verify the entire original frozen audit against its existing seal, read-only.
seal=json.loads((AUDIT/'SEAL.json').read_text())
manifest=(AUDIT/'SHA256SUMS.txt').read_bytes()
assert sha(manifest)==seal['manifest_sha256']
verified=0;failures=[]
for line in manifest.decode().splitlines():
    h,name=line.split('  ',1)
    f=AUDIT/name
    if not f.is_file() or sha(f.read_bytes())!=h:failures.append(name)
    else:verified+=1
assert not failures and verified==seal['files']
dump('SOURCE_PRESERVATION.json',{'selected_source_checks':preserved,'all_selected_match':all(x['code_bytes_hash_matches'] and x['source_snapshot_hash_matches'] and x['original_master_hash_matches'] for x in preserved),'frozen_audit_original_manifest_sha256':sha(manifest),'frozen_audit_files_verified':verified,'frozen_audit_failures':failures,'frozen_audit_modified':False,'original_source_modified':False})

summary={'status':'complete','hashes':len(rows),'bytes':sum(r['size_bytes'] for r in rows),'lines':sum(r['line_count'] for r in rows),'new_full_static_reads':len(rows),'reused_prior_full_reads':0,'source_bound_support_dependencies':len(deprecords),'supplied_code_execution':False,'source_modification':False,'exact_historical_run_receipts_reconstructed':0,'frozen_inventory_modified':False,'frozen_inventory_checksum_entries_verified':verified,'report':'REVIEW.md','coverage':'COVERAGE.json','top_findings':['Native error reducer can hide NaNs; benchmark only prints errors.','Cyclotomic fused character index lacks modulo-b contract; negative exponents can loop indefinitely.','Optimizer evaluates a rank-one-corrected model.','CLI/helper coverage gaps and formula-only certificate boundaries.','External rank helper build/runtime closure not established; matching witness integer bounds are safe.']}
assert summary['hashes']==13 and summary['bytes']==70284 and summary['lines']==1903
dump('SUMMARY.json',summary)

reporthash=sha((OUT/'REVIEW.md').read_bytes())
evs=[]
for i,r in enumerate(rows,1):
    evs.append({'id':f'PC0301-{i:02d}','code_sha256':r['sha256'],'kind':'uploaded_static_full','document':'REVIEW.md','document_sha256':reporthash,'scope':'Complete inert source inspection tied to exact bytes; no runtime or correctness-all-inputs implication.','quote_or_record':{'sha256':r['sha256'],'size_bytes':r['size_bytes'],'lines':r['extent']['lines'],'byte_range_half_open':r['extent']['byte_range_half_open'],'inspection':'full inert source inspection; never executed, imported or compiled'},'source_snapshot':r['source_snapshot']['path'],'coverage_document':'COVERAGE.json'})
dump('COVERAGE_EVIDENCE_ADDITION.json',evs)

# Seal all additive files other than the seal itself. This script is included.
items=[]
for p in sorted(OUT.rglob('*')):
    if p.is_file() and p.name not in ('SEALED_MANIFEST.json','SEALED_MANIFEST.sha256','SEAL_VALIDATION.json'):
        b=p.read_bytes();items.append({'path':str(p.relative_to(OUT)),'size_bytes':len(b),'sha256':sha(b)})
dump('SEALED_MANIFEST.json',{'package':'pending_code_review_0301','scope':'Additive evidence; thirteen complete inert source reads.','supplied_code_execution':False,'files':items})
sealed=sha((OUT/'SEALED_MANIFEST.json').read_bytes())
(OUT/'SEALED_MANIFEST.sha256').write_text(sealed+'  SEALED_MANIFEST.json\n')
for item in items:assert sha((OUT/item['path']).read_bytes())==item['sha256']
dump('SEAL_VALIDATION.json',{'sealed_manifest_sha256':sealed,'sealed_files':len(items),'verified_files':len(items),'validation':'All listed file hashes match. This validation file is intentionally outside the sealed manifest to avoid self-reference.','source_hash_count':13,'supplied_code_execution':False})
print(json.dumps(summary,indent=2));print('SEALED_MANIFEST_SHA256',sealed,'FILES',len(items))
