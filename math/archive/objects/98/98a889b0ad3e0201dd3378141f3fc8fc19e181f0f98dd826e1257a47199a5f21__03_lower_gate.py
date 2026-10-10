"""Independent four-column *lower* stage gate; counterpart of prior upper gate."""
from pathlib import Path
import sys,itertools,collections,time
ROOT=Path(__file__).parent
from prior_loader import activate;activate()
from universal_gate import gate as upper_gate, det, inv_mod, random_sep, mul
from polynomial_resultant import lift_poly
from triple_gate import modrank
from adjacent_tail import equations
from inverse_quartic import poly_eval
from dual_support import P8,primitive_root

def build_lower_gate(p,Q,U,L,perm=P8):
    Y=[]
    for out_col in (0,1,2,3):
        j=perm[out_col]
        rows=list(range(3,8)) if out_col!=3 else list(range(4,8))
        v0=[int(k==j) for k in range(8)]
        v1=[U[k] if k<j else 0 for k in range(8)]
        v2=[L[k] if k>j else 0 for k in range(8)]
        Y.append([[sum(Q[i][k]*vec[k] for k in range(8))%p for vec in (v0,v1,v2)] for i in rows])
    A,B,C,T=Y
    cof=[(-1)**i*det([T[k] for k in range(4) if k!=i],p)%p for i in range(4)]
    ell=[sum(cof[i]*A[i+1][j] for i in range(4))%p for j in range(3)]
    K=[]
    for i in range(5):K.append([*A[i],*[-x%p for x in B[i]],0,0,0])
    for i in range(5):K.append([*A[i],0,0,0,*[-x%p for x in C[i]]])
    K.append(ell+[0]*6)
    return K

def positive_controls():
    from random import Random
    rng=Random(20261009)
    P=[[int(P8[j]==k) for j in range(8)] for k in range(8)]
    ans={}
    for p in (12289,65537):
        ok=0
        while ok<100:
            C,U,L=random_sep(p,rng)
            B,_,_=random_sep(p,rng)
            try: Ci=inv_mod(C,p)
            except ZeroDivisionError:continue
            # B=Q C P where column j of P selects C's column perm[j].
            Q=mul(mul(B,[list(row) for row in zip(*P)],p),Ci,p)
            K=build_lower_gate(p,Q,U,L)
            r=modrank(K,p)
            assert r<=8, (p,r)
            ok+=1
        ans[p]=ok
    return ans

def audit(p=17):
    from universal_gate import gate
    z=primitive_root(p,8)
    F=[[pow(z,i*k,p) for k in range(8)] for i in range(8)]
    eq,W,E3,E4,Q=equations()
    ct=collections.Counter(); witnesses=[]
    st=time.monotonic()
    for h in itertools.product(range(p),repeat=4):
        if not h[0]:continue
        vec=[0]+list(h)+[0]
        a,b,c=[poly_eval(P,vec,p,z) for P in E3]
        d,e,f=[poly_eval(P,vec,p,z) for P in E4]
        Delta=(a*e-b*d)%p
        if not Delta:continue
        t=(-c*e+b*f)*pow(Delta,-1,p)%p
        beta=(-a*f+c*d)*pow(Delta,-1,p)%p
        if not t or poly_eval(eq[2],[t]+list(h)+[beta],p,z):continue
        ct['old_cubic_candidates']+=1
        U,L,data=lift_poly(p,z,h)
        Ku=gate(p,F,U,L)
        if modrank(Ku,p)>=9:
            ct['upper_rejected']+=1;continue
        ct['upper_survivors']+=1
        Kl=build_lower_gate(p,F,U,L)
        rl=modrank(Kl,p)
        ct['lower_rank_'+str(rl)]+=1
        if rl>=9:
            ct['lower_rejected']+=1
            if len(witnesses)<6:
                witnesses.append(dict(h=h,t=t,beta=beta,rank=rl))
        else:ct['both_survivors']+=1
    return dict(p=p,z=z,counts=dict(ct),examples=witnesses,seconds=time.monotonic()-st)

if __name__=='__main__':
 print('positive',positive_controls(),flush=True)
 print('audit',audit(),flush=True)
