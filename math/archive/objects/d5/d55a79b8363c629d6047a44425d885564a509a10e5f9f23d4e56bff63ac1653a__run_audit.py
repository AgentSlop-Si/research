"""Independent-style exact finite experiments for the algebraic arguments."""
import json
from random import Random
from orbit_recovery import (orbits,representatives,binary_collision_family,
    orbit_support_of_difference,dft_selected_exact,dft_bin_exact,lower_bounds,
    subset_sum_cyclotomic_coeffs,target_conjugate_coeffs)
from cyclotomic_interpolation import interpolation_audit,rational_interpolation_rank,rational_interpolant


def run():
    rng=Random(20261009)
    result={'minimal_representatives':[], 'missing_orbit_ambiguity':[],
            'degree_bounds':[], 'exact_interpolation':[], 'exhaustive':{}}
    for n in (2,4,8,16,32,64):
        O=orbits(n)
        q=representatives(n)
        assert len(q)==n.bit_length()
        assert set(O)=={1<<j for j in range(n.bit_length())}
        assert {k for ks in O.values() for k in ks}==set(range(n))
        assert {n//(k & -k) if k else 1 for k in q}==set(O)
        result['minimal_representatives'].append({'N':n,'sample_bins':q,
             'minimal_count':len(q),'orbits':{str(m):len(ks) for m,ks in O.items()}})
        for m,fs in O.items():
            choose_masks=[0,1] if m==1 else [0,1,(1<<(m//2))-1]
            variants=[binary_collision_family(n,m,mask) for mask in choose_masks]
            x0=variants[0]
            known=tuple(k for k in range(n) if k not in fs)
            signature=dft_selected_exact(x0,known)
            for x in variants[1:]:
                assert x!=x0
                assert dft_selected_exact(x,known)==signature
                assert orbit_support_of_difference(x,x0)==fs
            result['missing_orbit_ambiguity'].append({'N':n,'missing_conductor':m,
                'orbit_size':len(fs),'ambiguity_count_lower_bound':2**(m//2) if m>1 else 2,
                'tested_variants':len(variants),'support':fs})
        for _ in range(10):
            xs=[rng.randint(-2,2) for _ in range(n)]
            ys=[rng.randint(-2,2) for _ in range(n)]
            if dft_selected_exact(xs,q)==dft_selected_exact(ys,q):assert xs==ys
    # Exhaustive uniqueness for N=8: 256 binary strings -> 256 different signatures.
    n=8;q=representatives(n)
    sigs={dft_selected_exact([(mask>>j)&1 for j in range(n)],q)
          for mask in range(1<<n)}
    assert len(sigs)==1<<n
    result['exhaustive']={'N':n,'all_binary_inputs':1<<n,'distinct_minimal_signatures':len(sigs)}
    for n in (4,8,16,32,64):
        d=lower_bounds(n)
        if n<=16:
            # Verifies distinct subset sums in exact Q(zeta_n) coordinates.
            d['distinct_primitive_samples']=len({subset_sum_cyclotomic_coeffs(n,i)
                                            for i in range(1<<(n//2))})
        result['degree_bounds'].append(d)
    for n in (4,8):
        result['exact_interpolation'].append(interpolation_audit(n))
    result['degree_eight_rational_example']={
        'excluded_rational_degrees':[rational_interpolation_rank(8,3,d)['max_degree']
                                     for d in range(3,8) if rational_interpolation_rank(8,3,d)['no_rational_solution_proved']],
        'exact_solution_degree':rational_interpolant(8,3,8)['degree'],
        'all_boolean_cases_verified':rational_interpolant(8,3,8)['all_values_verified'],
        'denominator_nonzero_on_all_samples':True}
    return result

if __name__=='__main__':
    data=run()
    with open('audit_results.json','w') as f:json.dump(data,f,indent=2)
    print('orbit sizes, minimal measurements:', [(x['N'],x['minimal_count']) for x in data['minimal_representatives']])
    print('exact interpolation:', data['exact_interpolation'])
    print('checks PASS')
