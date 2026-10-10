"""An eight-coordinate rational open chart for four spectral constraints at *any* n.

This certifies a partial Fourier-factorization constraint, not the full FFT.
For F_n = B P A, C=A^-1 in a separated-generator rank-one chart, assume
p0=n-1,p1=0,p2=n-2. Eliminate lower columns 1,2 and upper rows 1,2
in the B rank-one identities. Exactly (n-4)(n-5) conditions remain,
expressible in [t,h0,h1,h2,h_(n-2),beta,gamma1,gamma2] only.
Proof is field-independent for a primitive n-th root and denominators !=0.
"""
from __future__ import annotations
from pathlib import Path
import json
import numpy as np
from dual_support import primitive_root,constraints,P8
from inverse_quartic import rankmod

def build(n,p,z,perm,variables):
    assert n>=6 and len(variables)==8 and len(perm)==n
    assert perm[0]==n-1 and perm[1]==0 and perm[2]==n-2
    assert sorted(perm)==list(range(n))
    t,h0,h1,h2,hlast,beta,gamma1,gamma2=(int(w)%p for w in variables)
    xi=pow(z,-1,p)
    def inv(a):
        if a%p==0:raise ZeroDivisionError('exceptional determinant/anchor')
        return pow(a%p,-1,p)
    inv(t);inv(h0);inv(z-1)
    c1=(1+xi+xi*xi)%p
    c2=(xi+xi*xi+pow(xi,3,p))%p
    c3=pow(xi,3,p)
    hs=[h0,h1,h2]
    for k in range(n-3):
        hs.append((c1*hs[k+2]-c2*hs[k+1]+c3*hs[k])%p)
    assert len(hs)==n
    H=hs[:n-2]+[hlast]
    b=(t-1+beta*(h0-1))*inv(z-1)%p
    a=(1-beta*h0-b)%p
    L=[0]+[(a+b*pow(xi,k,p)+beta*H[k])*inv(t)%p for k in range(1,n-1)]+[1]
    q1=[(pow(z,k,p)-gamma1)%p for k in range(n)]
    q2=[(pow(z,2*k,p)-gamma2)%p for k in range(n)]
    S1=[0]*n;S2=[0]*n;R1=[0]*n;R2=[0]*n
    for k in range(1,n-1):
        S1[k]=sum(q1[i]*H[i] for i in range(k))%p
        S2[k]=sum(q2[i]*H[i] for i in range(k))%p
        R1[k]=sum(q1[i]*L[i] for i in range(k+1,n))%p
        R2[k]=sum(q2[i]*L[i] for i in range(k+1,n))%p
        inv(S1[k])
    # Lower column 2: 3-mode extrapolation of h_0..h_(n-3).
    k=n-2
    aa=-q1[k]*inv(S1[k])%p
    bb=-R1[k]*inv(S1[k])%p
    star0,star1=hs[n-2],hs[n-1]
    u11=bb*star0%p;u12=(hlast-star0)%p
    u21=(1-bb*star1)%p;u22=(star1-1)%p
    det=(u11*u22-u12*u21)%p
    Vlast=((1-aa*star0)*u22-u12*(aa*star1))*inv(det)%p
    rho=(u11*(aa*star1)-(1-aa*star0)*u21)*inv(det)%p
    eta_last=-(q1[k]+Vlast*R1[k])*inv(S1[k])%p
    alpha=(eta_last-rho)%p
    if alpha==0:raise ZeroDivisionError('singular C-column pair')
    V=[t];delta_list=[]
    for k in range(1,n-2):
        delta=(R2[k]*S1[k]-R1[k]*S2[k])%p
        V.append((q1[k]*S2[k]-q2[k]*S1[k])*inv(delta)%p)
        delta_list.append(delta)
    V+=[Vlast,0]
    ETA=[0]+[-(q1[k]+V[k]*R1[k])*inv(S1[k])%p for k in range(1,n-1)]+[1]
    U=[1]+[H[k]*inv(h0)%p for k in range(1,n-1)]+[0]
    W=[0]+[h0*ETA[k]%p for k in range(1,n)]
    C=np.eye(n,dtype=np.int64)
    for i in range(n):
        for j in range(n):
            if i>j:C[i,j]=L[i]*V[j]%p
            elif i<j:C[i,j]=U[i]*W[j]%p
    F=np.array([[pow(z,i*j,p) for j in range(n)] for i in range(n)],dtype=np.int64)
    B=F@C[:,np.array(perm)]%p
    assert all((B[i,1]-beta*B[i,0])%p==0 for i in range(2,n))
    assert all((B[1,j]-gamma1*B[0,j])%p==0 for j in range(2,n))
    assert all((B[i,2]-rho*B[i,0])%p==0 for i in range(3,n))
    assert all((B[2,j]-gamma2*B[0,j])%p==0 for j in range(3,n))
    return C,B,dict(H=H,star=hs,L=L,V=V,ETA=ETA,rho=rho,
         lower_ratio_2=rho,upper_ratio_1=gamma1,upper_ratio_2=gamma2,
         denominators=[t,h0,det]+S1[1:n-1]+delta_list,alpha=alpha)

def verify(n,p,samples=20,seed=0):
    z=primitive_root(p,n)
    rng=np.random.default_rng(seed+31*n+p)
    perm=P8 if n==8 else [n-1,0,n-2]+list(map(int,rng.permutation(np.arange(1,n-2))))
    validated=0;full_rank=0;rest_fail=0;anchors=0
    for index in range(samples):
        x=list(map(int,rng.integers(1,p,size=8)))
        try:C,B,data=build(n,p,z,perm,x)
        except ZeroDivisionError:continue
        low,up=constraints(B,p)
        vanish_low={f'lower_{i}_1' for i in range(2,n-1)}|{f'lower_{i}_2' for i in range(3,n-1)}
        vanish_up={f'upper_1_{j}' for j in range(2,n-1)}|{f'upper_2_{j}' for j in range(3,n-1)}
        assert all(v==0 for name,v in low if name in vanish_low)
        assert all(v==0 for name,v in up if name in vanish_up)
        assert len(vanish_low|vanish_up)==4*n-14
        remains=[(name,v) for name,v in low+up if name not in vanish_low|vanish_up]
        assert len(remains)==(n-4)*(n-5)
        rest_fail+=any(v for name,v in remains)
        validated+=1
        if rankmod(C,p)==n:full_rank+=1
        if B[n-1,0]%p and B[0,n-1]%p:anchors+=1
        # The 8 coordinates can be read back from C and B on anchors.
        if B[n-1,0]%p and B[0,n-1]%p:
            roundtrip=[int(C[n-1,0]),int(C[0,n-1]),int(C[1,n-1]),int(C[2,n-1]),
                int(C[n-2,n-1]),int(B[n-1,1])*pow(int(B[n-1,0]),-1,p)%p,
                int(B[1,n-1])*pow(int(B[0,n-1]),-1,p)%p,
                int(B[2,n-1])*pow(int(B[0,n-1]),-1,p)%p]
            assert roundtrip==x,(roundtrip,x)
    return dict(n=n,p=p,w=z,permutation=perm,samples=validated,full_rank_stages=full_rank,
       both_B_anchors_nonzero=anchors,remaining_nonzero_test_cases=rest_fail,
       eliminated_rank_identities=4*n-14,remaining_rank_identities=(n-4)*(n-5),free_parameters=8)

if __name__=='__main__':
    stats=[]
    for n in (8,16,32,64):
        for p in (12289,65537):
            stats.append(verify(n,p,20,20261009))
    path=Path(__file__).with_name('general_onion_results.json')
    path.write_text(json.dumps(stats,indent=2)+'\n')
    print(json.dumps(stats,indent=2))
