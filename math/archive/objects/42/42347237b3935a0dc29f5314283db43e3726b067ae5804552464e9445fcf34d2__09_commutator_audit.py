"""Uniform (possibly near-resonant) shift-commutator rank obstruction.
For constant-coefficient tridiagonal path denominators B,
rank([B^-1,Z])<=2, independent of spectral condition number.
Their noncommuting products/sums have additive rank budget.
This proof DOES NOT cover arbitrary coordinate permutations/diagonal masks.
"""
from __future__ import annotations
import numpy as np
from numeric_audit import Fhat,Zmat


def path_toeplitz(n,a,b,c):
    return a*np.eye(n,dtype=complex)+b*np.diag(np.ones(n-1),-1)+c*np.diag(np.ones(n-1),1)

def analyze_stationary(n, q=2,t=2,near_resonant=False):
    Z=Zmat(n); stages=[]; stage_ranks=[]
    for k in range(t):
        S=np.zeros((n,n),complex)
        for j in range(q):
            if near_resonant:
                a=1.0
                b=-(1-1/n)*(0.5-(k+j)*0.004)
                c=-(1-1/n)*(0.5-(k+2*j)*0.005)
            else:
                a=3.1+0.17*k+0.13*j
                b=-0.48+0.05*k
                c=-0.37+0.04*j
            B=path_toeplitz(n,a,b,c)
            S+=np.linalg.inv(B)
        stages.append(S)
        stage_ranks.append(int(np.linalg.matrix_rank(S@Z-Z@S, tol=1e-7)))
    M=np.eye(n,dtype=complex)
    for S in stages:M=S@M
    C=M@Z-Z@M
    rk=int(np.linalg.matrix_rank(C,tol=1e-7))
    norm_error=float(np.linalg.norm(M-Fhat(n),2))
    floor=float(np.sqrt(max(0,0.5-rk/n)))
    return dict(n=n,q=q,t=t,stage_ranks=stage_ranks,
                measured_commutator_rank=rk,proved_rank_budget=2*q*t,
                full_fourier_commutator_rank=n,
                actual_spectral_error=norm_error,guaranteed_error_floor=floor)

if __name__=='__main__':
    import json
    print(json.dumps({
      'stable':[analyze_stationary(n) for n in (16,32,64)],
      'near_resonant':[analyze_stationary(n,near_resonant=True) for n in (16,32,64)]
    },indent=2))
