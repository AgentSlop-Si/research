"""Independent exact finite-field certificate audits; intentionally not an FFT benchmark."""
from collections import Counter
from math import gcd
from pathlib import Path
import json, random, time
from phase_union import recognize, transform_if_recognized, direct_dft, make_signal, phase_table

CASES=[(7,29,16),(17,103,72),(31,311,260),(63,127,9),
       (119,239,49),(127,509,16),(255,1021,811),(511,3067,64),(1023,4093,16)]

def modular_rank(M,p):
    a=[row[:] for row in M]
    m=len(a); n=len(a[0]) if a else 0
    rank=0
    for j in range(n):
        k=next((k for k in range(rank,m) if a[k][j]%p),None)
        if k is None: continue
        a[rank],a[k]=a[k],a[rank]
        inv=pow(a[rank][j]%p,-1,p)
        a[rank][j:]=[(v*inv)%p for v in a[rank][j:]]
        for k in range(rank+1,m):
            c=a[k][j]%p
            if c:
                a[k][j:]=[(a[k][h]-c*a[rank][h])%p for h in range(j,n)]
        rank+=1
        if rank==m:break
    return rank


def run():
    records=[]
    for n,p,root in CASES:
        a=next(a for a in range(1,n) if gcd(a,n)==1)
        chirp=make_signal(n,p,root,a,[(3% n,11%p)])
        m=n//2
        rank=modular_rank([[chirp[i+j] for j in range(m)] for i in range(m)],p) if n<=127 else None
        assert rank is None or rank==m
        weights=[(3%n,11%p),(n//2,37%p)]
        combined=make_signal(n,p,root,a,weights)
        t0=time.perf_counter();outs,cert=transform_if_recognized(combined,p,root);t1=time.perf_counter()
        assert cert and cert.a==a
        if n<=255:
            expected=direct_dft(combined,p,root)
            assert outs==expected
        else:
            pw=phase_table(n,p,root)
            for k in (0,1,2,n//2,n-1):
                assert outs[k]==sum(combined[j]*pw[(-j*k)%n] for j in range(n))%p
        records.append({'n':n,'field_prime':p,'chirp_a':a,'ordinary_hankel_rank':rank,'hankel_size':m,
            'auto_detected_modes':len(cert.modes),'candidate_a_count':cert.candidate_count,
            'verified_all_bins':n<=255,'verified_selected_bins':n>255,'time_s_single_run':round(t1-t0,6)})
    # Exhaustive parameter subgrid at N=7: varied phases and all pairs of modes.
    n,p,root=CASES[0]
    checks=0
    for a in range(n):
        for b1 in range(n):
            for b2 in range(b1+1,n):
                for c1 in (1,2,5):
                    for c2 in (1,2,5):
                        x=make_signal(n,p,root,a,[(b1,c1),(b2,c2)])
                        outs,cert=transform_if_recognized(x,p,root)
                        assert cert is not None,(a,b1,b2,c1,c2)
                        assert outs==direct_dft(x,p,root), (a,b1,b2,c1,c2)
                        checks+=1
    # Mutation and random noise false-accept audits.
    rng=random.Random(2026100917)
    rejects=0
    for n,p,root in CASES:
        for _ in range(100):
            x=[rng.randrange(p) for _ in range(n)]
            if recognize(x,p,root) is None:
                rejects+=1
            else:
                raise AssertionError(('Unexpected random input certificate', n))
    result={'n_cases':records,'exhaustive_n7_rank2_parameter_cases':checks,
        'random_dense_rejections':rejects,'n_samples_random_dense':len(CASES)*100,
        'status':'exact modular checks succeeded; these results do not constitute a general FFT speedup'}
    Path('audit_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':run()
