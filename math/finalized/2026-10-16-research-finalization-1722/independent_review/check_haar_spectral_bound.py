"""Review-authored controls. Imports no worker or historical source programs.

Exact controls corroborate the root counting/constant inequalities. Floating
controls are explicitly diagnostic and are not the universal proof.
"""
import json
from fractions import Fraction
import numpy as np

q = Fraction(129, 256)
assert 2-q*q > 0 and (2-q*q)**2 > 2
counts = []
for n in range(3, 19):
    N = 2**n
    count = sum(N//4 < 2*j+1 < 7*N//4 for j in range(N))
    assert count == 3*N//4
    assert all(2*j+1 not in (N//4,7*N//4) for j in range(N))
    counts.append({'N':N,'above_threshold':count,'repair_rank':count//2})

def haar(m):
    columns=[np.ones(m)/np.sqrt(m)]
    for width in [2**k for k in range(m.bit_length()-1,0,-1)]:
        for first in range(0,m,width):
            v=np.zeros(m)
            v[first:first+width//2]=1/np.sqrt(width)
            v[first+width//2:first+width]=-1/np.sqrt(width)
            columns.append(v)
    return np.array(columns).T

diagnostics=[]
gamma=np.sqrt(2-np.sqrt(2))-129/256
for N in (8,16,32,64):
    I=np.eye(N,dtype=complex)
    H=haar(N//2)
    R=np.block([[np.zeros_like(H),H],[H.T,np.zeros_like(H)]])
    eps=1/512
    V=(I+1j*eps*R)/np.sqrt(1+eps**2)
    Z=np.roll(I,1,axis=0)
    D=np.diag(np.exp(2j*np.pi*np.arange(N)/N))
    for seed in range(3):
        rng=np.random.default_rng(11000+N*10+seed)
        cs=[]
        for _ in range(2):
            p=rng.permutation(N)
            A=np.zeros((N,N))
            A[p[:-1],p[1:]]=1
            A[p[1:],p[:-1]]=1
            C=np.linalg.solve(I-1j*A/32,I+1j*A/32)
            assert np.linalg.norm(C-I,2) < 1/8
            cs.append(C)
        S=V@cs[0]@cs[1]
        L=I[:,rng.permutation(N)]@np.diag(np.exp(2j*np.pi*rng.random(N)))
        B=I[:,rng.permutation(N)]@np.diag(np.exp(2j*np.pi*rng.random(N)))
        Zp=B@Z@B.conj().T
        Dp=L.conj().T@D@L
        empirical=np.sort(np.linalg.svd(Zp-Dp,compute_uv=False))
        predicted=np.sort(2*np.abs(np.sin((2*np.arange(N)+1)*np.pi/(2*N))))
        assert np.max(np.abs(empirical-predicted)) < 5e-13
        for inverse,T in ((False,S),(True,S.conj().T)):
            distance=float(np.linalg.norm(T-I,2))
            assert distance < 129/512
            E=(L@T@B)@Z-D@(L@T@B)
            sig=np.linalg.svd(E,compute_uv=False)
            good=int(sum(sig>gamma))
            assert good>=3*N//4
            assert np.max(np.abs(E-L@(T@Zp-Dp@T)@B))<5e-13
            diagnostics.append({'N':N,'seed':seed,'inverse':inverse,
                'distance_to_identity':distance,'singulars_above_gamma':good,
                'required':3*N//4})
print(json.dumps({'exact_dyadic_counts':counts,'positive_gamma_exact':True,
 'diagnostics_only':diagnostics,'diagnostic_case_count':len(diagnostics),
 'gamma':float(gamma),'result':'PASS'},indent=2,sort_keys=True))
