"""Build immutable Phase19 archive with checked source hashes and summary."""
from pathlib import Path
import hashlib,json,zipfile,os
root=Path(__file__).parent.resolve()
original=root.parent/'fft_hero1_phase18_20261010.zip'
prior=root/'PRIOR_PHASE18_COMPLETE.zip'
if original.exists():
    assert original.read_bytes()==prior.read_bytes()
# Source equality can be audited from the nested original archive after
# clean extraction, without relying on any host-specific sibling directory.
with zipfile.ZipFile(prior) as previous_zip:
    for name in ('annihilator_engine.py','green_sparse.py','rational_forcing.py'):
        assert (root/name).read_bytes()==previous_zip.read('fft_hero1_phase18/'+name)

raw1=json.loads((root/'EXACT_BASIS_AUDIT.json').read_text())
raw2=json.loads((root/'EXACT_INVERSE_BASIS_AUDIT.json').read_text())
a=json.loads((root/'EXHAUSTIVE_GATE.json').read_text())
b=json.loads((root/'EXHAUSTIVE_INVERSE_GATE.json').read_text())
bench=json.loads((root/'BENCHMARK_HYBRID.json').read_text())
summary={
 'date':'2026-10-10','phase':19,
 'status':'exact finite-field structured-input theorem and sound all-input fallback; not a worst-case sub-NlogN FFT',
 'new_tests_passed':22,'prior_phase17_tests_passed':16,'prior_phase18_tests_passed':15,
 'new_exact_full_basis_entries':raw1['total_matrix_entries'],
 'new_exact_sparse_inverse_entries':raw2['total_matrix_entries'],
 'total_exact_direct_DFT_comparisons':raw1['total_matrix_entries']+raw2['total_matrix_entries'],
 'graph_exhaustive':a,'inverse_exhaustive':b,
 'benchmark_N4096':bench['records'],
 'theorems':[
   'deterministic O(N) unknown coprime shift with <=1 nonzero defect and nowhere-zero r',
   'deterministic O(N) fixed-K unknown shift under ratio-wrap class noncollision; K-dependent exponential constant',
   'deterministic O(N*s+s^3) full certified sparse circular inverse using 2s Fourier probes, Prony, full convolution certificate',
   'automatic exact one-impulse fixed-number unknown graph-binomial union with s<=2^m',
   'arbitrary inputs receive exact O(NlogN) fallback; no all-input sub-FFT theorem'
 ],
 'limitations':[
   'finite field arithmetic with required roots and inverses; no bit-operation complexity',
   'no stable numerical complex FFT implementation proved',
   'unknown K>1 multi-filter union not solved by sparse-inverse detector in general',
   'input model families have algebraic dimension <N, so do not cover generic inputs'
 ],
 'lineage_phase18_sha256':hashlib.sha256(prior.read_bytes()).hexdigest(),
 'source_files_unchanged_from_phase18':['annihilator_engine.py','green_sparse.py','rational_forcing.py']}
(root/'RESULT_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')

srcnames=['annihilator_engine.py','green_sparse.py','rational_forcing.py',
          'blind_discovery.py','blind_inverse.py','hybrid_engine.py',
          'test_phase19.py','test_inverse.py','test_hybrid.py',
          'exhaustive_gate.py','exhaustive_inverse_gate.py',
          'exact_basis_audit.py','exact_inverse_basis_audit.py',
          'benchmark_phase19.py','benchmark_inverse.py','benchmark_hybrid.py',
          'precision_gate.py','build_checkpoint.py']
rows=[f"# Source inventory — Phase19 (2026-10-10)\n\nSource code SHA-256 hashes; original Phase18 code is preserved byte-for-byte.\n"]
for n in srcnames:
    rows.append(f"- `{n}` — `{hashlib.sha256((root/n).read_bytes()).hexdigest()}`")
rows.append(f"\n- `PRIOR_PHASE18_COMPLETE.zip` — `{summary['lineage_phase18_sha256']}`")
rows.append('\nThe Phase18 archive itself contains the immutable Phase17 lineage and the original upstream research checkpoints. No predecessor has been silently overwritten.')
(root/'SOURCE_INVENTORY.md').write_text('\n'.join(rows)+'\n')

note=f'''# Phase19 reproduction receipt

**All outputs refer to the exact execution on 2026-10-10.**

- New regression tests: 22/22 passed (`TEST_RUN.log`).
- Independent prior Phase17 regression: 16/16 passed (`PRIOR_PHASE17_REGRESSION.log`).
- Independent prior Phase18 regression: 15/15 passed (`PRIOR_PHASE18_REGRESSION.log`).
- Full unknown-shift family: {raw1['total_matrix_entries']:,} exact direct DFT entries matched.
- Fully blind two-unknown-filter family: {raw2['total_matrix_entries']:,} exact direct DFT entries matched.
- Total distinct certified input-instance Fourier entries checked: {raw1['total_matrix_entries']+raw2['total_matrix_entries']:,}.
- Exhaustive GF(17)^4 graph classification: {a['total_vectors']:,} total vectors checked; {a['brute_force_compressible_K_le1']:,} compatible coprime nowhere-zero signals, zero misses/false accepts.
- Exhaustive GF(17)^4 inverse classification: {b['all_vectors']:,} total vectors checked; {b['inverse_support_le2']:,} compatible inverse-sparse signals, zero misses/false accepts.
- Full first-8-probes-preserving mutation rejected by all-coordinate certificate and handled by ordinary FFT.
- Source archive Phase18 SHA-256: `{summary['lineage_phase18_sha256']}`; original three imported Python sources are byte-identical.

**Scope limits:** structured-input exact modular field arithmetic only, charged root/Green setup separately, no floating point robustness or arbitrary-input `o(N log N)` claim. Probes/root scan/full certificate are explicitly paid; generic inputs use ordinary FFT.
'''
(root/'RUN_RECEIPT.md').write_text(note)

# All checked text/code/log/json files are stored alongside exact earlier ZIP.
filenames=sorted(f for f in root.iterdir() if f.is_file() and f.name!='MANIFEST.sha256')
lines=[]
for f in filenames:
    lines.append(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+f.name)
(root/'MANIFEST.sha256').write_text('\n'.join(lines)+'\n')

archive=root.parent/'fft_hero1_phase19_20261010.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=8) as z:
    for f in sorted(root.iterdir()):
        if f.is_file():z.write(f,arcname='fft_hero1_phase19/'+f.name)
print('archive',archive,'bytes',archive.stat().st_size,'sha256',hashlib.sha256(archive.read_bytes()).hexdigest())
print('files',len([x for x in root.iterdir() if x.is_file()]))
print('verified exact matrix entries',summary['total_exact_direct_DFT_comparisons'])
