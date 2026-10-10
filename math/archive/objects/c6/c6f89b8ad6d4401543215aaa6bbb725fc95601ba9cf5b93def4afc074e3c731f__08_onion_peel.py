"""Fourier onion-peel elimination for F8=BPA on a further open patch.

From dual support (lower j1, upper i1), eliminate lower j2 and upper i2
as well, leaving 12 conditions in 8 variables. All calculations exact in
prime fields; rational formulas make characteristic-zero sense for zeta8.
This is a *feasibility reduction*, not a found Fourier factorization.
"""
import json
from pathlib import Path
import numpy as np
from dual_support import P8,primitive_root,constraints


def build_onion(p,omega,x, perm=P8):
    """x=[t,h0,h1,h2,h6,beta,gamma1,gamma2] over GF(p)."""
    assert len(x)==8
    t,h0,h1,h2,h6,beta,gamma,gamma2=[int(v)%p for v in x]
    z=omega%p;xi=pow(z,-1,p)
    def inv(v):
        if v%p==0:raise ZeroDivisionError('nonzero chart failed')
        return pow(v%p,-1,p)
    inv(t);inv(h0);inv(z-1)
    c1=(1+xi+xi*xi)%p
    c2=(xi+xi*xi+pow(xi,3,p))%p
    c3=pow(xi,3,p)
    hs=[h0,h1,h2]
    for k in range(5):hs.append((c1*hs[k+2]-c2*hs[k+1]+c3*hs[k])%p)
    assert len(hs)==8
    H=hs[:6]+[h6]
    assert len(H)==7
    b=(t-1+beta*(h0-1))*inv(z-1)%p
    a=(1-beta*h0-b)%p
    L=[0]+[(a+b*pow(xi,k,p)+beta*H[k])*inv(t)%p for k in range(1,7)]+[1]
    q1=[(pow(z,i,p)-gamma)%p for i in range(8)]
    q2=[(pow(z,2*i,p)-gamma2)%p for i in range(8)]
    S1=[0]*8;S2=[0]*8;R1=[0]*8;R2=[0]*8
    for k in range(1,7):
        S1[k]=sum(q1[i]*H[i] for i in range(k))%p
        S2[k]=sum(q2[i]*H[i] for i in range(k))%p
        R1[k]=sum(q1[i]*L[i] for i in range(k+1,8))%p
        R2[k]=sum(q2[i]*L[i] for i in range(k+1,8))%p
        inv(S1[k])
    # j2 lower support: C[:,6]-rho C[:,7] is three Fourier modes.
    a6=(-q1[6])*inv(S1[6])%p
    b6=(-R1[6])*inv(S1[6])%p
    hs6,hs7=hs[6],hs[7]
    a11=b6*hs6%p; a12=(h6-hs6)%p
    a21=(1-b6*hs7)%p; a22=(hs7-1)%p
    determinant=(a11*a22-a12*a21)%p
    invdet=inv(determinant)
    rhs1=(1-a6*hs6)%p;rhs2=a6*hs7%p
    V6=(rhs1*a22-a12*rhs2)*invdet%p
    rho=(a11*rhs2-rhs1*a21)*invdet%p
    alpha=(-(q1[6]+V6*R1[6])*inv(S1[6])-rho)%p
    if alpha==0:raise ZeroDivisionError('singular C-column pair')
    V=[t]
    deltas={}
    for k in range(1,6):
        delta=(R2[k]*S1[k]-R1[k]*S2[k])%p
        invd=inv(delta)
        V.append((q1[k]*S2[k]-q2[k]*S1[k])*invd%p)
        deltas[k]=delta
    V+=[V6,0]
    ETA=[0]+[-(q1[k]+V[k]*R1[k])*inv(S1[k])%p for k in range(1,7)]+[1]
    U=[1]+[H[k]*inv(h0)%p for k in range(1,7)]+[0]
    W=[0]+[h0*ETA[k]%p for k in range(1,8)]
    C=np.eye(8,dtype=np.int64)
    for i in range(8):
        for j in range(8):
            if i>j:C[i,j]=L[i]*V[j]%p
            elif i<j:C[i,j]=U[i]*W[j]%p
    F=np.array([[pow(z,i*j,p) for j in range(8)] for i in range(8)],dtype=np.int64)
    B=F@C[:,np.array(perm)]%p
    # Check four families of spectral identities, including the ratio anchoring rows/cols.
    assert all((int(B[i,1])-beta*int(B[i,0]))%p==0 for i in range(2,8))
    assert all((int(B[1,j])-gamma*int(B[0,j]))%p==0 for j in range(2,8))
    assert all((int(B[i,2])-rho*int(B[i,0]))%p==0 for i in range(3,8))
    assert all((int(B[2,j])-gamma2*int(B[0,j]))%p==0 for j in range(3,8))
    return C,B,dict(H=H,three_mode=hs,L=L,V=V,ETA=ETA,upper_row_ratios=(gamma,gamma2),
       lower_column_ratios=(beta,rho),rho=rho,alpha=alpha,nonzero_denominators=[t,h0,determinant]+list(deltas.values())+S1[1:7],
       recurrence=(c1,c2,c3))


def mod_check(prime=12289,alternative=False,repeats=100):
    w=primitive_root(prime,8)
    if alternative:w=pow(w,3,prime)
    rng=np.random.default_rng(20261009+prime+int(alternative))
    ok=0
    for it in range(repeats):
        x=list(map(int,rng.integers(1,prime,size=8)))
        try:C,B,internal=build_onion(prime,w,x)
        except ZeroDivisionError:continue
        lower,upper=constraints(B,prime)
        assert len(lower)==15 and len(upper)==15
        removed_lower={f'lower_{i}_1' for i in range(2,7)}|{f'lower_{i}_2' for i in range(3,7)}
        removed_upper={f'upper_1_{j}' for j in range(2,7)}|{f'upper_2_{j}' for j in range(3,7)}
        assert len(removed_lower)==9 and len(removed_upper)==9
        assert all(v==0 for name,v in lower if name in removed_lower)
        assert all(v==0 for name,v in upper if name in removed_upper)
        remaining=[(name,v) for name,v in lower+upper if name not in removed_lower|removed_upper]
        assert len(remaining)==12
        assert any(v for _,v in remaining)
        # Independent vector-space recurrence check.
        hh=internal['H'];a,b,c=internal['recurrence']
        assert all((hh[k+3]-a*hh[k+2]+b*hh[k+1]-c*hh[k])%prime==0 for k in range(3))
        ok+=1
    return dict(prime=prime,primitive_root=w,independent_valid_open_patch_samples=ok,
       eliminated_rank_one_constraints=18,remaining_constraints=12,variables=8,
       closed_form='exact rational functions of eight parameters',status='no Fourier factorization established')

if __name__=='__main__':
    checks=[]
    for p in (12289,65537):
        for variant in (False,True):checks.append(mod_check(p,variant,80))
    Path(__file__).with_name('onion_results.json').write_text(json.dumps(checks,indent=2)+'\n')
    print(json.dumps(checks,indent=2))
