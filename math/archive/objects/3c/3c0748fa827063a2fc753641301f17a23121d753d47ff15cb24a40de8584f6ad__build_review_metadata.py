"""Reviewer-authored metadata builder; reads source bytes only for size/hash integrity."""
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone

root = Path('green_gate_code_review_0238')
queue_path = Path('code_coverage_audit_0228/REVIEW_QUEUE_02_GREEN_GATE_CODE.json')
queue_bytes = queue_path.read_bytes()
queue = json.loads(queue_bytes)
(root / 'INPUT_QUEUE.json').write_bytes(queue_bytes)

info = {
'phase30_dimension_gate.py': {
 'dependencies': ['phase30_four_parameter.py','phase30_macaulay.py'],
 'findings': ['G06'],
 'semantics': 'General q-variable minor coefficient construction and lifting; five-term rank-deficiency controls; Segre threshold requires restricted-map distinction.',
 'boundary': 'Threshold is a limitation of unsaturated window exclusion; no positive factorization certificate. Same source in Phase31 imports changed four-parameter dependency.'},
'phase30_macaulay.py': {
 'dependencies': ['phase30_four_parameter.py'],
 'findings': ['G04','G06'],
 'semantics': 'Entire four-variable anchored/full-minor construction, lifting, elimination, determinants, planted controls, sample and exhaustive mapping paths.',
 'boundary': 'Canonical field arithmetic sound by inspection; false-positive risk arises from overreading deficient ranks, truncated coverage or unbound streams. Phase31 dependency differs.'},
'phase29_two_parameter.py': {
 'dependencies': ['phase28_synthesis.py','phase28_polynomial.py'],
 'findings': ['G02','G06'],
 'semantics': 'Three-generator family, transverse slice full-degree/leading-term producer, Euclidean Bezout proof and weak saved validator.',
 'boundary': 'Producer certifies no common component, not no points; saved validator accepts explicit invalid-degree object and lacks family binding.'},
'phase28_synthesis.py': {
 'dependencies': [],
 'findings': ['G05','G06'],
 'semantics': 'Dense exact arithmetic, Fourier/root construction, monomial invariants and exact recovery, seeded Green generators, trace invariants.',
 'boundary': 'Field/root/canonical-residue/Hamiltonian preconditions; no all-length numerical FFT or unrestricted-complex positive lifting.'},
'phase28_polynomial.py': {
 'dependencies': ['phase28_synthesis.py'],
 'findings': ['G06'],
 'semantics': 'Every affine product/division, trace moment clearing, interpolation, Euclidean gcd/Bezout and exceptional-factor function.',
 'boundary': 'Correct generated-domain polynomial arithmetic; poles cause exceptions; full degrees and good reduction must be verified separately.'},
'fullminor_audit.cpp': {
 'dependencies': [],
 'findings': ['G03','G06'],
 'semantics': 'Full fixed-N8 native monomial/minor/rank kernel, row-index records, input/output and nested limit handling.',
 'boundary': 'Unlimited enumeration sound by inspection at documented primes; optional limit non-prefix bug; external matrix identity and complete artifact integrity not established by binary.'},
'fullminor_audit_generic.cpp': {
 'dependencies': [],
 'findings': ['G06'],
 'semantics': 'Full n=8/16 native coefficient and exact rank code; matrix stride, linear interval enumeration and rank-only stream.',
 'boundary': 'No execution; correct intended interval logic; success exit includes deficient/empty cases; read family binding/output integrity required externally.'},
'phase28_executor.py': {
 'dependencies': ['phase28_synthesis.py'],
 'findings': ['G06'],
 'semantics': 'Cyclic recurrence, dataclass preparation, seeded two-term sum and dense-comparison main block read.',
 'boundary': 'O(n) apply for fixed number of terms and correctly sized input; setup power/sort costs and shape validation remain. Main-block assertions not executed.'},
'phase29_executor.py': {
 'dependencies': ['phase28_synthesis.py','phase28_executor.py','phase29_two_parameter.py'],
 'findings': ['G06'],
 'semantics': 'Entire seeded three-term executor; coefficient substitution and independent third-cycle gauge alignment.',
 'boundary': 'Inherits exact-domain and preparation-cost limitations; computes candidate middle product, not Fourier transform.'},
'phase29_macaulay.py': {
 'dependencies': ['phase29_two_parameter.py'],
 'findings': ['G01','G06'],
 'semantics': 'Entire ternary quadrics/lift, Gaussian rank, determinant, N4 full permutations, saved verifier, random and exhaustive partial anchor audits.',
 'boundary': 'Exact generated-domain algebra sound by inspection; saved verifier accepts empty coverage and empty minors. Full span only negative certificate.'},
'phase30_four_parameter.py': {
 'dependencies': ['phase29_two_parameter.py','phase28_synthesis.py','phase29_executor.py'],
 'findings': ['G06'],
 'semantics': 'Fourth seeded Green family, combine, affine four-term executor and cycle recurrence.',
 'boundary': 'O(n) application; initialization-O(n) docstring unsupported literally; nu=1 executor; sys.path insertion can alter imported bytes.'},
}
name_to_hash = {entry['occurrences'][0]['name'].split('/')[-1]: entry['sha256'] for entry in queue['code']}
entries=[]
for entry in queue['code']:
    p=Path(entry['local_content']); raw=p.read_bytes()
    assert len(raw)==entry['size_bytes']
    assert hashlib.sha256(raw).hexdigest()==entry['sha256']
    name=entry['occurrences'][0]['name'].split('/')[-1]
    notes=info[name]
    entries.append({
        'sha256': entry['sha256'], 'size_bytes': len(raw), 'name': name,
        'local_content': str(p), 'language': 'C++' if name.endswith('.cpp') else 'Python',
        'evidence_id': 'GREEN_GATE_STATIC_0238_' + entry['sha256'][:16],
        'status': 'full_static_review_complete',
        'full_read_extent': {'bytes_start_inclusive': 0, 'bytes_end_exclusive': len(raw), 'lines_start_inclusive': 1, 'lines_end_inclusive': len(raw.splitlines()), 'all_source_lines_read': True},
        'hash_and_size_reverified': True,
        'source_modified': False, 'uploaded_source_executed': False,
        'uploaded_source_imported': False, 'uploaded_source_compiled': False,
        'source_body_duplicate_status': 'Exact hashes only; all listed occurrences have same source-body coverage; no near-duplicate substitution.',
        'runtime_dependency_closure_status': 'Not executed; intended Phase28-30 dependencies statically reviewed where mapped; Phase31 closure is not treated as unchanged.',
        'review_summary': notes['semantics'], 'claim_boundary': notes['boundary'],
        'finding_ids': notes['findings'],
        'intended_uploaded_dependencies': [{'name': dep, 'sha256': name_to_hash[dep], 'status': 'full_static_review_in_this_queue'} for dep in notes['dependencies']],
        'occurrences': entry['occurrences'],
    })
prior=Path('fft_research_master_20261009/additions/2213_ongoing/review_green_phase30/PHASE30_REVIEW.md')
coverage={
 'review_id': 'GREEN_GATE_STATIC_0238',
 'completed_utc': datetime.now(timezone.utc).isoformat(),
 'review_type': 'Full inert source inspection plus separately authored elementary controls',
 'queue_path': str(queue_path), 'queue_sha256': hashlib.sha256(queue_bytes).hexdigest(),
 'counts': {'source_hashes':len(entries),'python_hashes':9,'cpp_hashes':2,'source_bytes':sum(x['size_bytes'] for x in entries),'source_lines':sum(x['full_read_extent']['lines_end_inclusive'] for x in entries),'full_static_reviews':11,'uploaded_execution_count':0,'uploaded_import_count':0,'uploaded_compile_count':0},
 'prior_mathematical_evidence': {'path':str(prior),'sha256':hashlib.sha256(prior.read_bytes()).hexdigest(),'status':'Read as prior independent theorem/run scope; no historical reexecution in this review.'},
 'external_variant_boundary': [
  {'name':'phase28_executor.py','sha256':'3dfe9ebadcfeeaf07352d7147b1b9630274c4c3485e0d0afa6a54a72578224e5','size_bytes':2560},
  {'name':'phase29_executor.py','sha256':'0d1729266f035486322c6e07a2f89b0d69cf6b9973b265cb29dceac8d32b2ea0','size_bytes':961},
  {'name':'phase30_four_parameter.py','sha256':'96024cd7e2d6e59fd75734c718835282c4f6a924cf3178066c36ec20c1765575','size_bytes':3446},
 ],
 'external_variant_status': 'Phase31 variants hashed to distinguish dependency closure; their source bodies are outside this exact queue, with no new review credit claimed here.',
 'files': entries,
}
(root/'COVERAGE.json').write_text(json.dumps(coverage,indent=2)+'\n')
findings=[
 {'id':'G01','severity':'high_for_certificate_acceptance','file':'phase29_macaulay.py','lines':[[145,155],[82,103]],'title':'Empty witness coverage and empty minors accepted','effect':'Saved verifier can return True without checking 576 valid 15x15 minors.','controls':['COUNTEREXAMPLE_EMPTY_WITNESSES.json','COUNTEREXAMPLE_EMPTY_MINOR.json'],'theorem_impact':'Does not contradict prior independent family reconstruction.'},
 {'id':'G02','severity':'high_for_certificate_acceptance','file':'phase29_two_parameter.py','lines':[[135,140]],'title':'Saved slice validator accepts zero leading degrees and lacks family binding','effect':'Invalid-degree fake polynomial object satisfies all checks.','controls':['COUNTEREXAMPLE_BAD_SLICE.json'],'theorem_impact':'Main certificate producer has stronger checks; prior theorem remains separate.'},
 {'id':'G03','severity':'medium_limited_run_correctness','file':'fullminor_audit.cpp','lines':[[98,105]],'title':'Limit exits only inner enumeration loop','effect':'limit=1 or 0 checks 336 mappings, and limited output can be non-prefix.','controls':['INDEPENDENT_CONTROL_RESULTS.json'],'theorem_impact':'Default complete run unaffected.'},
 {'id':'G04','severity':'medium_artifact_contract','file':'phase30_macaulay.py','lines':[[257,296]],'title':'Packed record documentation claims unsaved determinant','effect':'Degree-three record is 21 bytes, not promised 25; only sample determinants exist in JSON.','controls':['INDEPENDENT_CONTROL_RESULTS.json'],'theorem_impact':'Correct record interpretation and reconstruction required.'},
 {'id':'G05','severity':'medium_general_api_low_seeded_scope','file':'phase28_synthesis.py','lines':[[125,140]],'title':'Raw zero counting gives false exclusion for noncanonical residues','effect':'Matrices equal in F_p can be reported excluded.','controls':['INDEPENDENT_CONTROL_RESULTS.json'],'theorem_impact':'Canonical generated matrices unaffected.'},
 {'id':'G06','severity':'precondition_and_claim_boundaries','file':'multiple','lines':[],'title':'Field/root, dependency, binary integrity, dimension and cost boundaries','effect':'Arbitrary moduli, changed imports, exit codes, rank-only streams, sampled deficiencies and setup cost require explicit scope.','controls':[],'theorem_impact':'Documented independently reconstructed fixed-family scope retained.'},
]
for f in findings:
 if f['file'] in name_to_hash:f['sha256']=name_to_hash[f['file']]
(root/'FINDINGS.json').write_text(json.dumps({'findings':findings,'details':'REVIEW.md','all_source_bytes_unchanged':True},indent=2)+'\n')
(root/'COUNTEREXAMPLE_EMPTY_MINOR.json').write_text(json.dumps({'prime':998244353,'n':4,'seed':2804,'full_rank_cases':576,'pivot_witnesses':{'0123/0123':{'selected_rows':[],'determinant_modp':1}}},indent=2)+'\n')
print(json.dumps(coverage['counts'],indent=2))
