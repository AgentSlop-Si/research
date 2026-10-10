"""New all-length rank criterion for a 3-frequency Fourier tail and col5.
Full proof in PROOF.md; tests exact modular field arithmetic.
"""
from __future__ import annotations
from pathlib import Path
import sys,random,json
from prior_loader import activate;activate()
import _bootstrap
from dual_support import primitive_root
from triple_gate import modrank
from universal_gate import det
ROOT=Path(__file__).parent

def mat(n,p,z,U,L):
    m=n-3
    rows=[]
    for i in range(m):
        V=[pow(z,i*j,p) for j in range(3)]
        e5=pow(z,5*i,p)
        up=sum(U[k]*pow(z,i*k,p) for k in range(5))%p
        low=sum(L[k]*pow(z,i*k,p) for k in range(6,n))%p
        rows.append(V+[e5,up,low])
    return rows

def draw(n,p,z,rng,matched):
    a=[rng.randrange(p) for _ in range(3)]
    L=[0]*n
    for k in range(3,n):L[k]=sum(a[r-1]*pow(z,r*k,p) for r in (1,2,3))%p
    U=[rng.randrange(p) for _ in range(n)]
    if matched:
        # Force U3:U4 = L3:L4 to create a nontrivial intersection.
        scalar=rng.randrange(1,p)
        U[3],U[4]=scalar*L[3]%p,scalar*L[4]%p
    return U,L

def audit_lengths(samples=50):
    rng=random.Random(20261009)
    out=[]
    for n in (8,16,32,64):
        for p in (12289,65537):
            z=primitive_root(p,n)
            cnt={'matched_rank_le_5':0,'generic_rank_6':0,'generic_determinant_nonzero':0,'constant_ratio_checks':0,'n8_exceptions':0}
            ratios=set()
            for rep in range(samples):
                matched=bool(rep%2)
                U,L=draw(n,p,z,rng,matched)
                M=mat(n,p,z,U,L)
                r=modrank(M,p)
                D=(U[3]*L[4]-U[4]*L[3])%p
                if n>=9:
                    assert (r<=5)==(D==0),('n>=9 rank fail',n,p,U,L,r,D)
                    if matched:cnt['matched_rank_le_5']+=1
                    else:
                        cnt['generic_rank_6']+=r==6
                    if D:
                        det6=det([row[:6] for row in M[:6]],p)
                        cnt['generic_determinant_nonzero']+=det6!=0
                        ratios.add(det6*pow(D,-1,p)%p)
                else:
                    if r<=5 and D:cnt['n8_exceptions']+=1
            if n>=9:
                assert len(ratios)==1 and 0 not in ratios,(n,p,ratios)
                cnt['constant_ratio_checks']=len(ratios)
            out.append(dict(n=n,p=p,z=z,checks=samples,**cnt,determinant_ratio=(next(iter(ratios)) if ratios else None)))
            print(out[-1],flush=True)
    return out

if __name__=='__main__':
    out=audit_lengths()
    (ROOT/'BOUNDARY_LOCK_TESTS.json').write_text(json.dumps(out,indent=2)+'\n')
