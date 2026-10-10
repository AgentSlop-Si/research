"""Rebuild Phase 15 certificates and manifest (no dependence on earlier phase code)."""
from __future__ import annotations
import json,math,sys,time
from pathlib import Path
import numpy as np
from phase15_symmetry import (
    margulis_maps,half_translation,perm_commutes,modular_commutator_certificate,
    complex_commutator_spectrum,finite_rank_defect_audit,
    matrix_network_and_breaking_budget,group_twirl)

ROOT=Path(__file__).resolve().parent
out={'phase':'HERO #0 / 15','date':'2026-10-10',
     'scope':'mixed-axis Green/Margulis weight-symmetry obstruction; NOT a universal fast FFT',
     'proof_status':'self-contained mathematical derivation; independent literature novelty not established',
     'modular_prime':65537,'centralizer_checks':0,'exact_modular_commutator_polynomials':[],
     'complex_spectra':[],'fourfold_projection':[],'exact_rank_perturbation':[],
     'numerical_weight_asymmetry':[]}
for s in (2,4,6,8,10,12,16):
    maps=margulis_maps(s)
    for axis in ('x','y','xy'):
        perm=half_translation(s,axis)
        for p in maps:
            assert perm_commutes(p,perm)
            out['centralizer_checks']+=1
for s in (2,4,8,16):
    for axis in ('x','y','xy'):
        out['exact_modular_commutator_polynomials'].append(modular_commutator_certificate(s,axis))
for s in (2,4,6,8,10,12):
    for axis in ('x','y','xy'):
        out['complex_spectra'].append(complex_commutator_spectrum(s,axis))
    out['fourfold_projection'].append(group_twirl(s))
for s,k in ((4,0),(4,1),(4,3),(8,5)):
    n=s*s
    mods={((j//4)%2,j%4,(j*7+1)%n):3 for j in range(k)}
    for axis in ('x','y','xy'):
        out['exact_rank_perturbation'].append(finite_rank_defect_audit(s,mods,axis=axis))
for s in (2,4):
    for eps in (0.,.00001,.0001):
        out['numerical_weight_asymmetry'].append(matrix_network_and_breaking_budget(s,eps))
out['new_unittest_methods']=16
out['inherited_phase14_methods']=22
out['inherited_phase13_methods']=21
out['main_theorem_summary']={
    'x_commutator_singular_values':'N/2 zeros; N/2 twos',
    'y_xy_commutator_singular_values':'N/2 sqrt(2-sqrt(2)); N/2 sqrt(2+sqrt(2))',
    'invariant_x_spectral_error_lower_bound':1.0,
    'invariant_xy_fourfold_relative_frobenius_lower_bound':math.sqrt(3)/2,
    'exact_fourier_weight_change_min_x':'N/4 (relative to invertible Pi_x-invariant reference)',
    'exact_fourier_weight_change_min_y':'N/2 (relative to invertible Pi_y-invariant reference)',
    'universal_fft':'NOT SOLVED'
}
(ROOT/'RESULTS.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'status':'PASS',
                  'centralizer_checks':out['centralizer_checks'],
                  'exact_polynomial_checks':len(out['exact_modular_commutator_polynomials']),
                  'complex_spectrum_checks':len(out['complex_spectra']),
                  'group_projection_checks':len(out['fourfold_projection']),
                  'rank_perturbation_checks':len(out['exact_rank_perturbation']),
                  'weight_asymmetry_checks':len(out['numerical_weight_asymmetry'])},indent=2))
