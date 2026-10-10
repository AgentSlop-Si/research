"""Deterministic Phase 16 research audit; all numerical results are checks, not proofs."""
from __future__ import annotations
import hashlib
import json
import math
from pathlib import Path
import numpy as np
from phase16_gauge import (
    PRIME,margulis_maps,half_y,monomial_centralizer_cases,commutator_rank_for_gauge,
    phase_gauge_commutator_lower_bound,phase_gauge_e0_commutator,
    one_green_rook_no_go,numerical_one_green_check,make_gauge_weights,
    recover_common_gauge,spanning_gauge_residuals,
)
from positive_small_factor import exact_F4_green_product
import sympy as sp

ROOT=Path(__file__).parent


def sha(path:Path)->str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    rng=np.random.default_rng(160016)
    positives={str(n):len(monomial_centralizer_cases(n)) for n in (4,8,16,32,64)}
    ranks=[]
    for s in (4,8,16):
        n=s*s
        choices=[[1]*n]+[[int(v) for v in rng.integers(1,PRIME,size=n)] for _ in range(3)]
        for i,d in enumerate(choices):
            rank=commutator_rank_for_gauge(s,d)
            assert rank==n
            ranks.append({'N':n,'trial':i,'commutator_rank':rank})
    phase_bounds=[]
    for s in (4,6,8,16,32,64):
        phase_bounds.append({'side':s,'N':s*s,
            'proved_error_lower_bound':phase_gauge_commutator_lower_bound(s)})
    phase_stress=[]
    for s in (4,8,16):
        n=s*s;b=2*phase_gauge_commutator_lower_bound(s)
        errs=[]
        for _ in range(8):
            D=np.exp(2j*math.pi*rng.random(n))
            e=phase_gauge_e0_commutator(s,D)
            assert e+1.e-9>=b
            errs.append(e)
        phase_stress.append({'side':s,'min_norm_comm_e0':min(errs),'proved_minimum':b})
    rook=[]
    for s in (3,4,5,6,8,16,32,64):rook.append(one_green_rook_no_go(s))
    numerical=[numerical_one_green_check(s,.30) for s in (4,5,6,8)]
    s=8;perms=margulis_maps(s);const=[2,3,5,7]
    d=[int(v) for v in rng.integers(1,PRIME,size=s*s)]
    w=make_gauge_weights(perms,const,d)
    out=recover_common_gauge(perms,w,const)
    assert out is not None
    residuals=spanning_gauge_residuals(perms,w,const)
    assert residuals['defects']==[]
    F4=exact_F4_green_product()
    assert sp.simplify(F4['Y']*F4['X']-F4['F'])==sp.zeros(4)
    certificate={
        'N':4,'exact_arithmetic':'SymPy cyclotomic/algebraic complex numbers',
        'fourier_unnormalized':[[str(F4['F'][i,j]) for j in range(4)] for i in range(4)],
        'first_rook_factor_X':[[str(sp.simplify(F4['X'][i,j])) for j in range(4)] for i in range(4)],
        'second_rook_factor_Y':[[str(sp.simplify(F4['Y'][i,j])) for j in range(4)] for i in range(4)],
        'first_stage_weight_vectors':[[str(sp.simplify(v)) for v in row] for row in F4['stage_x']['weights']],
        'second_stage_weight_vectors':[[str(sp.simplify(v)) for v in row] for row in F4['stage_y']['weights']],
        'permutation_order':['identity','x_flip','identity','y_flip'],
        'proof_status':'Each of 8 resolvents invertible; stage sums equal X,Y and YX=F4 exactly',
        'all_length_conclusion':'NONE',
    }
    (ROOT/'EXACT_F4_CERTIFICATE.json').write_text(json.dumps(certificate,indent=2),encoding='utf-8')
    counts={'phase16_test_methods':19,'rerun_phase15_test_methods':16,'rerun_phase14_test_methods':22}
    for name,expected in (('phase16_tests.log','Ran 19 tests'),
                          ('inherited_phase15_tests.log','Ran 16 tests'),
                          ('inherited_phase14_tests.log','Ran 22 tests')):
        data=(ROOT/name).read_text()
        assert expected in data and data.rstrip().endswith('OK'),(name,'log was not passing')
    result={
        'date':'2026-10-10',
        'status':'Restricted Green-network structural research; universal exact FFT target UNSOLVED',
        'counts':counts,
        'positive_monomial_centralizer_instances':positives,
        'gauged_commutator_full_rank_checks':ranks,
        'phase_gauge_proved_error_bounds':phase_bounds,
        'phase_gauge_random_stress':phase_stress,
        'single_green_rook_exclusion_sides':rook,
        'single_green_numerical_stress':numerical,
        'gauge_detector_example':{'N':64,'generator_edge_occurrences':4*64,
                                  'connected_components':residuals['components'],
                                  'defect_count':len(residuals['defects'])},
        'small_exact_positive_control':{'N':4,'two_layers':True,'greens_per_layer':4,
                                         'exact_symbolic_matrix_residual':0,
                                         'certificate':'EXACT_F4_CERTIFICATE.json'},
        'scope_limits':[
            'Monomial centralizer theorem includes complex roots, not a full characterization of the Fourier commutant.',
            'Pure-gauge no-go assumes one common diagonal gauge for every resolvent occurrence.',
            'Uniform quantitative lower bound requires |d_i|=1.',
            'The k>=N/2 defect barrier requires Zariski-generic D and counts each changed occurrence.',
            'Single Green + rook obstruction is not a no-go for sums of two or more resolvents.',
            'Exact F4 construction is a finite positive control only.',
            'No universal exact o(N log N) algorithm has been proved in this project.',
        ],
        'source_sha256':{x.name:sha(x) for x in (ROOT/'phase16_gauge.py',ROOT/'positive_small_factor.py',ROOT/'test_phase16.py')},
    }
    (ROOT/'RESULTS.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({'status':'PASS','exact_F4':True,'phase16_tests':19,
                      'phase15_tests':16,'phase14_tests':22,
                      'gauged_rank_checks':len(ranks),
                      'new_exact_uniform_fft':False},indent=2))

if __name__=='__main__':main()
