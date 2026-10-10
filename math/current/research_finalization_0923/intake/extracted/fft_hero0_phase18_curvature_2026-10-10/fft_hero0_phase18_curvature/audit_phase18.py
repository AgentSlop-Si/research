"""Regenerate all central Phase 18 certificates and written numerical evidence."""
import json,math,sys,time,hashlib
from pathlib import Path
import numpy as np
from phase18_curvature import (modular_polyphase_certificate,
    exact_commutator_singular_values,direct_fourier_commutator,
    curvature_gate,linear_time_curvature_certificate,
    modular_fourier_weyl_gate,forest_gauge_holonomies)
from phase17_gauge import P,modular_fourier,modrank,half_grid_permutation,mod_matmul,margulis_permutations
from test_phase18 import Phase18Tests

out=Path(__file__).resolve().parent
results={
    'phase':'HERO0_PHASE18',
    'date':'2026-10-10',
    'claim_scope':'restricted Green graph necessary bounds only, no uniform FFT speedup',
    'inherited_result':'Order-eight spectrum and singular values proved in Phase 15; reverified, NOT new',
    'exact_field_polynomial_checks':[], 'complex_spectrum_checks':[],
    'energy_bound_examples':[]
}
for s in (2,4,8,16):
    results['exact_field_polynomial_checks'].append(modular_polyphase_certificate(s))
for s in (2,4,6,8,10,12,16):
    spec=np.linalg.svd(direct_fourier_commutator(s),compute_uv=False)
    expected=exact_commutator_singular_values(s)
    results['complex_spectrum_checks'].append({'s':s,'n':s*s,
        'max_singular_discrepancy':float(np.max(abs(spec-expected))),
        'relative_commutator_frobenius_squared':float(sum(spec**2)/(s*s))})
fixture=Phase18Tests()
for s in (4,8):
    for mode in ('raw','flat','strong'):
        layers,d=fixture._network(s,2026+s,mode)
        slow=curvature_gate(s,layers,phase_gauge=d)
        cheap=linear_time_curvature_certificate(s,layers,phase_gauge=d)
        results['energy_bound_examples'].append({'s':s,'mode':mode,
            'actual_relative_fro_error':slow['actual_relative_fro_error'],
            'matrix_raw_error_floor':slow['raw_symmetry_error_floor'],
            'matrix_flat_error_floor':slow['flat_gauge_error_floor'],
            'linear_time_raw_error_floor':cheap['relative_fro_error_floor_raw'],
            'linear_time_flat_error_floor':cheap['relative_fro_error_floor_flat'],
            'paired_energy_per_n':slow['paired_energy_normalized'],
            'flat_energy_per_n':slow['flat_energy_normalized'],
            'edge_visits_linear_cert':cheap['read_weight_entries'],
            'max_resolvent_norm':slow['max_green_norm_g']})
results['exact_weyl_controls']={
    'fourier':modular_fourier_weyl_gate(modular_fourier(16)),
}
assert all(r['fft_factorization_failures']==r['polyphase_conjugation_failures']==r['order_eight_failures']==0
           for r in results['exact_field_polynomial_checks'])
assert all(r['max_singular_discrepancy']<1e-10 for r in results['complex_spectrum_checks'])
assert all(x['actual_relative_fro_error']+1e-10 >=max(x['linear_time_raw_error_floor'],x['linear_time_flat_error_floor'])
           for x in results['energy_bound_examples'])
assert results['exact_weyl_controls']['fourier']['passes']
(out/'RESULTS.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps({'phase':'18','modular_lengths':[4,16,64,256],
                  'spectrum_sides':[2,4,6,8,10,12,16],
                  'energy_examples':len(results['energy_bound_examples']),
                  'all_certificates_passed':True},indent=2))
