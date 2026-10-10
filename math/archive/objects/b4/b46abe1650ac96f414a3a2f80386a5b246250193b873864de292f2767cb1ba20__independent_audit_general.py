"""Independent double-entry audit of the generalized phase-union certificate.

Direct reference does NOT call the production direct_dft helper, and the
Hankel determinant checker reconstructs the matrix and eliminates it anew.
"""
import json
import random
import time
from collections import defaultdict
from math import comb, gcd
from pathlib import Path

from phase_union_general import phase_table, make_signal, transform_if_recognized, phase_eliminant, evaluate_poly, recognize

CASES=[(7,29,16),(17,103,72),(31,311,260),(63,127,9),
       (119,239,49),(127,509,16),(255,1021,811),(511,3067,64),(1023,4093,16)]


def independent_direct_dft(x,p,omega):
    n=len(x)
    out=[]
    for k in range(n):
        root=pow(omega, (-k)%n,p)
        t=1
        y=0
        for v in x:
            y=(y+(v%p)*t)%p
            t=t*root%p
        out.append(y)
    return out


def independent_determinant(A,p):
    A=[row[:] for row in A]
    m=len(A)
    result=1
    for j in range(m):
        pivot=next((i for i in range(j,m) if A[i][j]%p),None)
        if pivot is None:return 0
        if pivot!=j:
            A[pivot],A[j]=A[j],A[pivot]
            result=-result
        t=A[j][j]%p
        result=result*t%p
        scale=pow(t,-1,p)
        for row in range(j+1,m):
            multiplier=A[row][j]*scale%p
            for h in range(j,m):
                A[row][h]=(A[row][h]-multiplier*A[j][h])%p
    return result%p


def run():
    rng=random.Random(1700917)
    counts=defaultdict(int)
    worst_candidate_count=0
    examples=[]
    for r in (1,2,3,4,5,6):
        for n,p,w in CASES:
            if n<3*r:continue
            avals=[0,1,n-1]
            for divisor in (3,7,17):
                if n%divisor==0:avals.append(divisor)
            for a in sorted(set(t % n for t in avals)):
                s=min(r,3) if n>=63 else min(r,2)
                b_choices=rng.sample(range(n),s)
                modes=[(b,rng.randrange(1,p)) for b in b_choices]
                x=make_signal(n,p,w,a,modes)
                t0=time.perf_counter()
                y,cert=transform_if_recognized(x,p,w,r)
                elapsed=time.perf_counter()-t0
                if cert is None:
                    raise AssertionError(('missed structured input',n,r,a,modes))
                if n<=255:
                    expected=independent_direct_dft(x,p,w)
                    assert y==expected,(n,r,a)
                    counts['all_bins_verified']+=n
                else:
                    pw=phase_table(n,p,w)
                    for k in (0,1,2,13,n//3,n//2,n-1):
                        expected=sum(x[j]*pw[-k*j % n] for j in range(n))%p
                        assert y[k]==expected,(n,r,a,k)
                        counts['sample_bins_verified']+=1
                counts['structured_full_runs']+=1
                worst_candidate_count=max(worst_candidate_count,cert.candidates_found)
                if r==3 and n in (17,63,127,511) and a in (0,1):
                    examples.append(dict(n=n,p=p,r=r,a=a,detected_a=cert.a,
                        detected_modes=len(cert.modes),candidates=cert.candidates_found,
                        reference='all_binned' if n<=255 else 'selected_bins',
                        elapsed_python_s=round(elapsed,6)))
                if r<=4 and n<=127:
                    center=next((j for j in range(r,n-r) if x[j]),None)
                    assert center is not None
                    start=center-r
                    coefficients=phase_eliminant(x,start,r,p)
                    for _ in range(3):
                        t=rng.randrange(1,p)
                        poly=evaluate_poly(coefficients,t,p)
                        mat=[[x[start+i+j]*pow(t,(i+j)*(i+j-1)//2,p)%p
                              for j in range(r+1)] for i in range(r+1)]
                        direct=independent_determinant(mat,p)
                        # Raw determinant = t^(min exponent) * elim(t)
                        min_exp=(r+1)*r*(r-1)//2
                        assert direct==pow(t,min_exp,p)*poly%p,(n,r,a,t,direct,poly)
                        counts['independent_determinants']+=1
    # Some random unstructured samples may fit a tiny structured family by chance;
    # every accepted certificate is verified against the raw input, so to audit
    # soundness, check all output bins even on an accidental acceptance.
    for r in (1,2,3,4):
        for n,p,w in CASES[:7]:
            if n<3*r:continue
            for _ in range(100):
                x=[rng.randrange(p) for i in range(n)]
                cert=recognize(x,p,w,r)
                if cert is None:
                    counts['random_rejected']+=1
                else:
                    from phase_union_general import transform_certified
                    assert transform_certified(cert)==independent_direct_dft(x,p,w)
                    counts['random_accepted_and_verified']+=1
    report={
        'status':'PASS: exact model-specific tests, not a general FFT result',
        'tested_r':[1,2,3,4,5,6],
        'tested_n':[n for n,_,_ in CASES],
        'counts':dict(counts),
        'max_phase_candidates_observed':worst_candidate_count,
        'max_phase_candidate_bound_r6':comb(8,3),
        'illustrative_runs':examples,
        'complexity_model':'fixed-r exact prime-field arithmetic; supplied prime p and primitive root omega',
    }
    Path('audit_results_general.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':run()
