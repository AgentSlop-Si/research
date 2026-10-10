#!/usr/bin/env python3
"""Independent Phase8 audit: operation accounting, generic-input obstruction."""
import json,math,random,time
from phase8_weyl_cycle import (P,Costs,exact_circulant_cycle,
  exact_unknown_shift_cycle,exact_circulant_rational_cycle,
  exact_weyl_dynamic,cyclic_linear_synthesize,
  synthesize_circulant_order,synthesize_time_weyl,root_of_unity,full_ntt_oracle)

def record(n,m,rng):
    k=n//m
    v0=[rng.randrange(P) for _ in range(k)]
    x=cyclic_linear_synthesize(v0,m,[19,43],(0,5))
    c=Costs();start=time.perf_counter()
    got,cert,c=exact_unknown_shift_cycle(x,m,c,True)
    elapsed=time.perf_counter()-start
    assert cert['accepted'] and cert['inferred_shift']==5
    oracle=full_ntt_oracle(x)
    assert got==oracle
    bc=Costs();baseline=full_ntt_oracle(x,bc)
    assert got==baseline
    return {'n':n,'k':k,'m':m,
        'special_field_arithmetic_plus_tests':c.total(),
        'special_input_loads':c.input_reads,
        'special_field_arithmetic_and_loads_per_n':round((c.total()+c.input_reads)/n,3),
        'baseline_field_arithmetic_plus_tests_per_n':round(bc.total()/n,3),
        'special_inversions':c.inversions,
        'wall_seconds_python_demo':round(elapsed,4),
        'all_N_outputs_exact':True}

def main():
    rng=random.Random(70086)
    bench=[record(n,m,rng) for n,m in [(512,8),(1024,8),(2048,8),(4096,16),
                   (8192,16),(16384,16),(32768,16),(65536,16)]]
    rng=random.Random(7012)
    reject={'circulant_fixed_shift':0,'weyl_time_varying':0}
    trials=100
    k,m=16,8
    for _ in range(trials):
        v=[rng.randrange(P) for _ in range(k*m)]
        if exact_circulant_cycle(v,m,(0,1)) is None:
            reject['circulant_fixed_shift']+=1
        if exact_weyl_dynamic(v,m) is None:
            reject['weyl_time_varying']+=1
    n=k*m;q=P;s=2;r=1
    # Even allowing any tap coefficients, the image of the generative map
    # has cardinality no more than q^(r*K+r*s), including collisions.
    log10_bound_fixed=(r*k+r*s-n)*math.log10(q)
    log10_bound_unknown=math.log10(k)+log10_bound_fixed
    log10_bound_weyl=(k+s*(m-1)-n)*math.log10(q)
    data={'benchmark':bench,'random_fresh_input_trials':trials,
      'rejections':reject,'uniform_random_input_probability_log10_upper_bound':{
      'fixed_order1_two_taps':log10_bound_fixed,
      'allow_unknown_shift_d':log10_bound_unknown,
      'time_varying_fixed_two_Weyl_dictionary':log10_bound_weyl},
      'model':'exact operations over GF(2013265921), roots only for powers of two dividing p-1',
      'generic_input_worst_case':'ordinary NTT fallback O(NlogN); no uniform linear FFT'}
    with open('AUDIT_RESULTS.json','w') as f:json.dump(data,f,indent=2)
    print(json.dumps(data,indent=2))
if __name__=='__main__':main()
