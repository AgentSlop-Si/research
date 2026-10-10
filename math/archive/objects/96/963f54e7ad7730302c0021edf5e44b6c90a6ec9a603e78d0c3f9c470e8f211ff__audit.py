"""Deterministic, independent numerical / GF evidence for proved Phase 17 theorems."""
import json
import math
from pathlib import Path
import numpy as np
from phase17_gauge import (
    P,ratio_matrix,ratio_singular_values,normalized_error_gap,
    ratio_c,minimum_rank_budget,rank_k_error_gap,
    modular_gauged_symmetry_defect,modrank,two_sided_defect
)

def audit():
    sizes=[]
    for s in [2,4,6,8,10,12,16,32,64,128]:
        r={'s':s,'N':s*s,'rho':2*ratio_c(s),
           'two_sided_phase_norm_gap':normalized_error_gap(s),
           'necessary_rank_edits_phase_only':minimum_rank_budget(s),
           'necessary_rank_edits_fraction':(1-2*ratio_c(s))/8,
           'predicted_ratio_singular_values':[float(z) for z in ratio_singular_values(s)/(s*s)]}
        if s<=12:
            vals=np.linalg.svd(ratio_matrix(s),compute_uv=False)
            predicted=ratio_singular_values(s)
            r['max_singular_value_abs_discrepancy']=float(np.max(abs(vals[:4]-predicted)))
            r['max_tail_singular_value']=float(max(vals[4:],default=0))
            assert np.max(abs(vals[:4]-predicted))<3e-11
            assert max(vals[4:],default=0)<3e-11
        sizes.append(r)
    gf=[];rng=np.random.default_rng(17400)
    for s,rep in [(4,4),(8,2)]:
        n=s*s
        for run in range(rep):
            di=rng.integers(1,P,size=n,dtype=np.int64)
            do=rng.integers(1,P,size=n,dtype=np.int64)
            rank=modrank(modular_gauged_symmetry_defect(s,di,do))
            assert rank==n
            gf.append({'side':s,'N':n,'run':run,'prime':P,'fourier_defect_rank':rank})
    trials=[];rng=np.random.default_rng(17401)
    for s in [4,8,10]:
        n=s*s
        for run in range(3):
            di=np.exp(2j*np.pi*rng.random(n))
            do=np.exp(2j*np.pi*rng.random(n))
            actual=float(np.linalg.norm(two_sided_defect(s,di,do),'fro')/(2*math.sqrt(n)))
            bound=normalized_error_gap(s)
            assert actual+1e-10>=bound
            trials.append({'side':s,'run':run,'actual_intertwiner_projection_error':actual,'proved_lower_bound':bound})
    result={
      'date':'2026-10-10',
      'status':'Verified necessary conditions for restricted two-sided gauged Green networks; NOT a faster universal FFT.',
      'normalizer_prior_art_warning':'Fourier monomial automorphisms are classical; 2026 J Algebraic Combinatorics Theorem 9 covers the automorphism group.',
      'test_methods_new':15,
      'test_methods_inherited_phase16':19,
      'test_methods_inherited_phase15':16,
      'test_methods_inherited_phase14':22,
      'test_methods_total_rerun':72,
      'limiting_phase_only_error_bound':0.5*math.sqrt(1-2/math.pi),
      'limiting_necessary_rank_edit_fraction':(1-2/math.pi)/8,
      'sizes':sizes,
      'finite_field_generic_gauge_samples':gf,
      'phase_only_trials':trials,
      'assumptions':['N=s^2 with even s>=4','T0 commutes half-grid Pi','T=D_out T0 D_in^-1','approximation bound requires |diag(D)|=1','rank-edits refer to a valid phase-gauged reference'],
      'limitations':['Does not exclude arbitrary curvature-bearing graph weights','Does not prove FFT algebraic-circuit lower bound','No known novel universal faster FFT']
    }
    (Path(__file__).parent/'RESULTS.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print('Audit completed: 10 size-formula cases,',len(gf),'exact modular full-rank gauge trials,',len(trials),'random phase trials')
    print('s=16 exact lower bound:',normalized_error_gap(16),'(correct value)')
    print('limit:',result['limiting_phase_only_error_bound'])
    return result

if __name__=='__main__':audit()
