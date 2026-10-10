"""Small exact family demonstration, with independent T evaluations as oracle."""
import json
import random
from pathlib import Path
from cache_demo import (prepare_demo,chain,expected_online,apply_t_charged,
                        polynomial_b,cached_polynomial)
from prior_exact_arithmetic import PrimeField


def main():
    rng=random.Random(20261009)
    records=[]
    for prime in (65537,998244353):
        f=PrimeField(prime)
        for n in (8,16,32):
            q=f.root(n)
            assert f.power(q,n)==f.one and f.power(q,n//2)!=f.one
            sparse,kernel,preparation=prepare_demo(f,n,q)
            steps=min(4,n-1)
            vectors=[[int(i==j) for i in range(n)] for j in range(n)]
            vectors.extend([[rng.randrange(prime) for _ in range(n)] for _ in range(4)])
            polynomial=[f.integer(v) for v in (2,-3,5,1)]
            # Check every permitted shorter chain's counts, including zero updates.
            for shorter in range(steps):
                for cached_mode in (False,True):
                    trial=chain(f,sparse,kernel,vectors[-1],shorter,cached_mode)
                    assert trial['field_operations']==expected_online(n,shorter,cached_mode)
            for x in vectors:
                cached=chain(f,sparse,kernel,x,steps,True)
                baseline=chain(f,sparse,kernel,x,steps,False)
                assert cached['inputs']==baseline['inputs']
                assert cached['outputs']==baseline['outputs']
                assert cached['field_operations']==expected_online(n,steps,True)
                assert baseline['field_operations']==expected_online(n,steps,False)
                for seed,output in zip(cached['inputs'],cached['outputs']):
                    independent,_=apply_t_charged(f,kernel,seed)
                    assert output==independent
                px,pb_counts=polynomial_b(f,sparse,polynomial,x)
                expected,_=apply_t_charged(f,kernel,px)
                actual,pc_details=cached_polynomial(f,sparse,polynomial,cached['outputs'][0])
                assert actual==expected
                assert pb_counts==dict(mul=7*n-3,add=3*n)
                assert pc_details['field_operations']==dict(mul=10*n,add=6*n)
            # Reusing a C update for an unrelated input is invalid.
            # B*e0=0, whereas a fresh unchanged e0 has nonzero T*e0.
            control=chain(f,sparse,kernel,vectors[0],1,True)
            assert control['outputs'][1]==[f.zero]*n
            assert control['outputs'][1]!=control['outputs'][0]
            records.append(dict(prime=prime,n=n,steps=steps,
                basis_vectors=n,random_vectors=4,preparation=preparation,
                cached_online=cached['field_operations'],
                baseline_online=baseline['field_operations'],
                cached_total=sum(preparation.values())+sum(cached['field_operations'].values()),
                baseline_total=sum(preparation.values())+sum(baseline['field_operations'].values()),
                logical_output_writes=cached['logical_output_writes'],
                logical_related_input_writes=cached['logical_related_input_writes'],
                retained_input_elements=cached['retained_input_elements'],
                retained_output_elements=cached['retained_output_elements'],
                polynomial_identity_cases=len(vectors),
                unrelated_input_negative_control='PASS',status='PASS'))
    result=dict(status='PASS',configurations=len(records),
        basis_seed_vectors=sum(r['basis_vectors'] for r in records),
        random_seed_vectors=sum(r['random_vectors'] for r in records),
        full_chain_outputs=sum((r['basis_vectors']+r['random_vectors'])*(r['steps']+1) for r in records),
        polynomial_identity_cases=sum(r['polynomial_identity_cases'] for r in records),
        scope='Declared related-input family B^j*x only; not arbitrary fresh FFT speedup',
        details=records)
    out=Path(__file__).parent/'results'
    out.mkdir(exist_ok=True)
    (out/'cache_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='details'},indent=2))
    for r in records[:3]:
        print(f"N={r['n']}: cached total {r['cached_total']}, baseline total {r['baseline_total']}, full output writes {r['logical_output_writes']}")


if __name__=='__main__':
    main()
