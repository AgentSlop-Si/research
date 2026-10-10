"""Exact example: S1=0 branch can contain invertible, corner-regular
C while satisfying first 10 Fourier-support identities. Does not solve
remaining 20, so is not a full FFT factorization.
"""
import json
from pathlib import Path
import numpy as np
from dual_support import primitive_root, P8, constraints
from inverse_quartic import invert_mod,rankmod

def witness(p=12289, seed=2209):
    omega=primitive_root(p,8)
    gamma=1
    rng=np.random.default_rng(seed)
    for iteration in range(200):
        t=int(rng.integers(1,p)); beta=int(rng.integers(1,p))
        H=[1]+list(map(int,rng.integers(1,p,size=6)))
        V=[t]+[0]+list(map(int,rng.integers(1,p,size=5)))+[0]
        b=(t-1+beta*(H[0]-1))*pow(omega-1,-1,p)%p
        a=(1-beta*H[0]-b)%p
        xi=pow(omega,-1,p)
        L=[0]+[(a+b*pow(xi,k,p)+beta*H[k])*pow(t,-1,p)%p for k in range(1,7)]+[1]
        q=[(pow(omega,k,p)-gamma)%p for k in range(8)]
        S=[sum(q[r]*H[r] for r in range(k))%p for k in range(1,7)]
        if S[0]!=0 or any(not s for s in S[1:]):continue
        R=[sum(q[r]*L[r] for r in range(k+1,8))%p for k in range(1,7)]
        if R[0]==0:continue
        V[1]=(-q[1])*pow(R[0],-1,p)%p
        eta=[0,7]+[-(q[k]+V[k]*R[k-1])*pow(S[k-1],-1,p)%p for k in range(2,7)]+[1]
        W=[0]+[H[0]*eta[k]%p for k in range(1,8)]
        U=[1]+[H[k]*pow(H[0],-1,p)%p for k in range(1,7)]+[0]
        C=np.eye(8,dtype=np.int64)
        for i in range(8):
            for j in range(8):
                if i>j:C[i,j]=L[i]*V[j]%p
                elif i<j:C[i,j]=U[i]*W[j]%p
        F=np.array([[pow(omega,i*j,p) for j in range(8)] for i in range(8)],dtype=np.int64)
        B=F@C[:,np.array(P8)]%p
        lo,up=constraints(B,p)
        if any(v for name,v in lo if name.endswith('_1')):continue
        if any(v for name,v in up if name.startswith('upper_1_')):continue
        if rankmod(C,p)!=8 or any(int(B[i,j])==0 for i,j in [(7,0),(0,7)]):continue
        A=invert_mod(C,p)
        if not int(A[7,0]) or not int(A[0,7]):continue
        remain=[v for name,v in lo+up if not (name.endswith('_1') or name.startswith('upper_1_'))]
        assert any(remain)
        return {'prime':p,'omega':omega,'attempts':iteration+1,'s_1':S[0],
            'rank_C':8,'corner_B70':int(B[7,0]),'corner_B07':int(B[0,7]),
            'inverse_corner_A70':int(A[7,0]),'inverse_corner_A07':int(A[0,7]),
            'eliminated_constraints_verified':10,'remaining_nonzero':sum(v!=0 for v in remain),
            'H':H,'V':V,'ETA':eta,'beta':beta,'gamma':gamma,'t':t}
    raise AssertionError('no exception found')
if __name__=='__main__':
    ws=[witness(p) for p in (12289,65537)]
    Path(__file__).with_name('exception_s1_witness.json').write_text(json.dumps(ws,indent=2)+'\n')
    print(json.dumps(ws,indent=2))
