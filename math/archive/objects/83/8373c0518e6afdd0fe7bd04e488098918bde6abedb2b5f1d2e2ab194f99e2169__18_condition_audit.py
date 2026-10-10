"""Independent floating-point condition control for all-N exact inequalities.

Floating results are audits only; analytic proofs in MIXED_ORDER_GREEN.md.
"""
from math import isqrt
import json
import numpy as np


def condition_control(n):
    T=3*np.eye(n)
    T-=np.diag(np.ones(n-1),1)
    T-=np.diag(np.ones(n-1),-1)
    G=np.linalg.solve(T,np.eye(n))
    order=list(range(0,n,2))+list(range(1,n,2))
    M=G[np.ix_(order,order)] + G/20
    b=n-1
    z=isqrt(b)
    if z*z<b:z+=1
    u=np.ones(n)
    u[0]=z
    H=np.eye(n)-2*np.outer(u,u)/np.dot(u,u)
    S=H@M
    h1=float(np.linalg.cond(H,1))
    m1=float(np.linalg.cond(M,1))
    s1=float(np.linalg.cond(S,1))
    s2=float(np.linalg.cond(S,2))
    assert np.allclose(H@H,np.eye(n),atol=2e-13)
    assert m1<=7+1e-9
    assert s1>=4*(n-1)/175-1e-9
    assert s2<=7+1e-9
    assert np.linalg.matrix_rank(S[:n//2,n//2:])>=n//2-2
    return dict(N=n, kappa_1_householder=h1,kappa_1_M=m1,
                kappa_1_S=s1,kappa_2_S=s2,
                proved_lower_kappa_1_S=4*(n-1)/175,
                proved_upper_kappa_1_M=7,
                proved_upper_kappa_2_S=7)

if __name__=='__main__':
    print(json.dumps([condition_control(n) for n in (8,16,32,64,128,256)],indent=2))
