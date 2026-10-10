"""Deterministic reproducibility audit. Prints one JSON object.
Use: OPENBLAS_NUM_THREADS=1 python audit.py > audit.json
This is a set of exact finite-field falsification checks and numerical controls,
not a search/proof of a new sub-NlogN DFT.
"""
from __future__ import annotations
from dataclasses import asdict
import json
from weyl_gate import (P,modular_root,ntt,check_weyl,seeded_product,
                       seeded_near_resonant_product,NearResonantGreen,
                       DiagonalAfter,ScaledFFT)
from projective_gate import (MaskedPermutedFFT,cross_ratio_witness,
                             column_pair_fingerprint,full_monomial_gate,dense_from_oracle)
from numeric_audit import (sharp_gap_control,sharp_sparse_weyl_gap,
                           random_sparse_covariance,inverse_sparse_floor,near_resonance_real)
from commutator_mod import modular_commutator_audit
from commutator_audit import analyze_stationary
from real_mask_audit import audit_real_mask


def run():
    data={'phase':20,'date':'2026-10-09','research_status':'no proven new sub-NlogN FFT',
          'field_prime':P,'normalization':'sqrt(N)^-1',
          'model':'exact finite-field circuits plus independent numerical theorem audits'}

    data['weyl_positive_controls']=[asdict(check_weyl(ntt,n,trials=2 if n<=1024 else 1,seed=200+n))
                                     for n in (8,16,32,256,1024,16384,65536)]
    data['one_equation_adversaries']=[asdict(check_weyl(DiagonalAfter(n),n,trials=1,seed=201+n))
                                      for n in (8,16,64)]
    data['wrong_scalar_controls']=[asdict(check_weyl(ScaledFFT(n,7),n,trials=1,seed=202+n))
                                   for n in (8,16,64)]

    green=[];resonant=[]
    for n in (8,16,32,64,256,1024,4096,16384):
        G=seeded_product(n,seed=19)
        green.append({'n':n,'seed':19,'weyl':asdict(check_weyl(G,n,trials=1,seed=311+n)),
                      'two_column':asdict(column_pair_fingerprint(G,n))})
    for n in (8,16,32,64,256,1024,4096,16384,65536):
        G=seeded_near_resonant_product(n,seed=21)
        resonant.append({'n':n,'seed':21,'weyl':asdict(check_weyl(G,n,trials=1,seed=411+n)),
                         'two_column':asdict(column_pair_fingerprint(G,n))})
    data['independently_permuted_green_sums']=green
    data['independently_permuted_near_resonant_green_sums']=resonant

    data['outer_gauge_positive_controls']=[
        {'n':n,'seed':17,
         'two_column':asdict(column_pair_fingerprint(MaskedPermutedFFT(n,17),n)),
         'complete_matrix_test':asdict(full_monomial_gate(dense_from_oracle(MaskedPermutedFFT(n,17),n))) }
        for n in (8,16,32,64)]

    data['sharp_weyl_gap']=[sharp_gap_control(n) for n in (8,16,32,64,128)]
    data['sharp_sparse_column_gap']=[sharp_sparse_weyl_gap(64,s,3) for s in (1,2,3,7,15)]
    data['random_sparse_column_bound']=[random_sparse_covariance(n) for n in (8,32,64)]
    data['inverse_sparse_approximation_floor']=[inverse_sparse_floor(n,3,t=t)
                                                  for n,t in ((16,1),(32,1),(64,1),(32,2),(64,2))]
    data['stationary_green_exact_commutator']=[modular_commutator_audit(n) for n in (8,16,32,64)]
    data['stationary_green_spectral_error']=[analyze_stationary(n,near_resonant=False) for n in (16,32,64)]
    data['stationary_near_resonant_spectral_error']=[analyze_stationary(n,near_resonant=True) for n in (16,32,64)]
    data['near_resonant_single_green_real']=[near_resonance_real(n) for n in (16,32,64,128)]
    data['real_one_mask_rigidity']=[audit_real_mask(n) for n in (4,8,16,32,64,128)]

    # Explicit assert gates from evidence, so audited claims fail closed.
    assert all(x['passed'] for x in data['weyl_positive_controls'])
    assert all(x['first_equation'] and not x['second_equation'] for x in data['one_equation_adversaries'])
    assert all(x['first_equation'] and x['second_equation'] and not x['calibrated'] for x in data['wrong_scalar_controls'])
    assert all(not x['weyl']['passed'] and x['two_column']['excluded'] for x in green+resonant)
    assert all(x['complete_matrix_test']['equivalent'] and not x['two_column']['excluded'] for x in data['outer_gauge_positive_controls'])
    assert all(abs(x['ratio']-1)<1e-10 for x in data['sharp_weyl_gap'])
    assert all(abs(x['ratio']-x['exact_gap'])<1e-10 for x in data['sharp_sparse_column_gap'])
    assert all(x['product_rank']<=x['upper_bound'] and x['Fourier_commutator_rank']==x['n']
               for x in data['stationary_green_exact_commutator'])
    assert all(x['measured_mixed_mask_entries']==0 and x['rank_real']+x['rank_imag']==x['n']
               for x in data['real_one_mask_rigidity'])
    return data

if __name__=='__main__':print(json.dumps(run(),indent=2))
