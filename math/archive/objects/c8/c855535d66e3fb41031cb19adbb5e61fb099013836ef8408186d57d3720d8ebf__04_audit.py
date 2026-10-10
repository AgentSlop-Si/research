"""Self-contained Phase 27 audit producing evidence without overstating scope."""
from __future__ import annotations
import json
from phase27_affine_gap import (random_hamiltonian,affine_rank_audit,
     high_probability_threshold,conjugate_by_transposition,shift_successor,
     permutation_rank_difference,cyclotomic_zero_density)
from phase27_expansion_certificate import certify
from phase27_expander_mixer import audit_balanced_cuts,two_by_two_phase_report
from phase27_green_candidate import seeded_nonaffine_circuit
from phase27_fourier_recovery import recover,MonomialFourier,P
import random


def run()->dict:
    examples=[]
    for n in (32,64,128,256):
        cycle=random_hamiltonian(n,2700+n)
        rank=affine_rank_audit(cycle)
        exact_gap=certify(n,2700+n,delta_den=2)
        near=conjugate_by_transposition(n,0,n//4+1)
        entry={'n':n,'affine_gap':rank,'probabilistic_lower':high_probability_threshold(n)['rank_at_least'],
               'exact_graph_gap':exact_gap,
               'rank_two_trap_difference':permutation_rank_difference(near,shift_successor(n)),
               'dense_trap_nonzero_formula':n*n-3*n+4,
               'rational_mixer_phase':two_by_two_phase_report(n,2700+n)}
        if n<=128:
            entry['rank_two_trap_exact_nonzeros']=cyclotomic_zero_density(near)['nonzeros']
            entry['random_cycle_exact_nonzeros']=cyclotomic_zero_density(cycle)['nonzeros']
        examples.append(entry)
    rng=random.Random(2764)
    n=64
    row=list(range(n));col=list(range(n));rng.shuffle(row);rng.shuffle(col)
    good=MonomialFourier(row,col,[rng.randrange(1,P) for _ in range(n)],
                        [rng.randrange(1,P) for _ in range(n)])
    pos=recover(good.apply,good.transpose,n,max_other_columns=n-1,trials=2,seed=2764)
    g=seeded_nonaffine_circuit(1024,seed=3724)
    bad=recover(g.apply,g.transpose,1024,max_other_columns=8,trials=2,seed=2764)
    return {'phase':'27', 'date':'2026-10-10', 'nonsubNlogN_fft':True,
            'finite_instance_certificates':examples,
            'positive_fourier_probe':{'status':pos.status,'fwd_calls':pos.oracle_calls_forward,
                                      'transpose_calls':pos.oracle_calls_transpose},
            'nonaffine_green_probe':{'status':bad.status,'reason':bad.reason,
                                    'fwd_calls':bad.oracle_calls_forward},
            'all_balanced_cuts_n16':audit_balanced_cuts(16,2716,exhaustive=True),
            'sampled_mixer_cuts_n32_to128':[audit_balanced_cuts(n,2700+n,trials=80)
                for n in (32,64,128)]}

if __name__=='__main__':
    x=run()
    with open('audit.json','w') as f:json.dump(x,f,indent=2)
    print(json.dumps({'positive':x['positive_fourier_probe'],
        'negative':x['nonaffine_green_probe'],
        'n16':x['all_balanced_cuts_n16'],
        'n256':x['finite_instance_certificates'][-1]},indent=2))
