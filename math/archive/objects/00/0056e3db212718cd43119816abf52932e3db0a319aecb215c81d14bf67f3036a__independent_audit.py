"""Independent Phase 5 audit: fresh raw vectors, direct separate DFT reference,
independent modular elimination and Prim MST, high-precision stability checks.
"""
import json
import math
import random
from pathlib import Path
from itertools import product
import phase5 as method


def independent_gauss_rank(rows,p):
    a=[[v%p for v in row] for row in rows]
    n=len(a); r=0; cols=len(a[0])
    for j in range(cols):
        pivot=-1
        for i in range(r,n):
            if a[i][j]:pivot=i;break
        if pivot<0:continue
        a[pivot],a[r]=a[r],a[pivot]
        scale=pow(a[r][j],p-2,p)
        a[r]=[(v*scale)%p for v in a[r]]
        for i in range(n):
            if i==r:continue
            c=a[i][j]
            a[i]=[(u-c*v)%p for u,v in zip(a[i],a[r])]
        r+=1
    return r


def independent_raw_dft(x,p,omega):
    n=len(x);a=[]
    for k in range(n):
        acc=0
        for j in range(n):
            acc=(acc+x[j]*pow(omega,(-k*j)%n,p))%p
        a.append(acc)
    return a


def prim_cost(m):
    remaining=set(range(1,m))
    tree={0};cost=0
    while remaining:
        c,i=min((m//math.gcd(m,abs(a-b)),b) for a in tree for b in remaining)
        cost+=c;remaining.remove(i);tree.add(i)
    return cost


def independent_gauge(m,p,omega,x,a):
    """Independent computation uses direct modular elimination instead of imported transforms."""
    n=m*m
    eta=pow(omega,m,p)
    C=[[sum(x[t+m*u]*pow(eta,(-h*u)%m,p) for u in range(m))%p
        for h in range(m)] for t in range(m)]
    output=[0]*n
    for h in range(m):
        lam=[pow(omega,j,p)*pow(eta,(-a[j]*h)%m,p)%p for j in range(m)]
        V=[[pow(lam[j],t,p) for j in range(m)] for t in range(m)]
        aug=[V[i]+[C[i][h]] for i in range(m)]
        for j in range(m):
            pivot=next(i for i in range(j,m) if aug[i][j])
            aug[j],aug[pivot]=aug[pivot],aug[j]
            c=pow(aug[j][j],p-2,p)
            aug[j]=[(c*z)%p for z in aug[j]]
            for i in range(m):
                if i==j:continue
                c=aug[i][j]
                aug[i]=[(q-c*z)%p for q,z in zip(aug[i],aug[j])]
        B=[aug[j][m] for j in range(m)]
        for s in range(m):
            k=h+s*m
            val=0
            for j in range(m):
                coef=sum(pow(omega,(-k*t)%n,p)*pow(lam[j],t,p) for t in range(m))%p
                val=(val+coef*B[j])%p
            output[k]=val
    return output


def audit():
    rng=random.Random(17052026)
    full=0; coefficients=0;rank_checks=0
    for m in (2,3,4,5,6,7,8,9,12,16):
        p,w=method.field_for_m(m)
        for delta in range(1,m):
            for r in sorted(set((1,max(1,m//2),m))):
                a=[j%r for j in range(m)]
                E=[[pow(pow(w,m,p),(-delta*t*a[j])%m,p) for j in range(m)] for t in range(m)]
                result=independent_gauss_rank(E,p)
                expected=len({(delta*z)%m for z in a})
                assert result==expected,(m,delta,r,result,expected)
                rank_checks+=1
        x=[rng.randrange(p) for j in range(m*m)]
        reference=independent_raw_dft(x,p,w)
        for r in sorted(set((1,2,3,m))):
            if r>m:continue
            a=[j%r for j in range(m)]
            got=independent_gauge(m,p,w,x,a)
            assert got==reference,(m,r)
            check,_=method.full_orbit_execution(x,m,p,w,a)
            assert check==got
            full+=1;coefficients+=m*m
    mst_checks=0
    for m in range(2,131):
        pred,_=method.optimal_mask_spanning_tree(m)
        got=prim_cost(m)
        assert got==pred,(m,got,pred)
        mst_checks+=1
    stability=[]
    import mpmath as mp
    mp.mp.dps=130
    for m in (8,16,32):
        w=mp.exp(2*mp.pi*mp.j/(m*m))
        A=mp.matrix([[w**(t*j) for j in range(m)] for t in range(m)])
        _,sing,_=mp.svd(A)
        cond=max(sing)/min(sing)
        bound=mp.sqrt(math.comb(2*m-2,m-1))*(mp.mpf(m)/(2*mp.pi))**(m-1)
        assert cond>=bound
        stability.append({'M':m,'log10_actual_kappa':float(mp.log10(cond)),
                          'log10_proven_lower_bound':float(mp.log10(bound))})
    out={
      'status':'PASS','model':'exact Fp arithmetic with N=M^2 | p-1; separate 130-digit complex stability check',
      'independent_full_arbitrary_dfts':full,'independent_full_output_coefficients':coefficients,
      'independent_mask_ranks':rank_checks,'independent_Prim_MST_checks':mst_checks,
      'rigorous_stability_certificate_tested':stability,
      'disclaimer':'This is not an O(N) arbitrary-input DFT; full_orbit_execution charges dense coefficient solves and output sums.'
    }
    Path('AUDIT_RESULTS.json').write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))


if __name__=='__main__':audit()
