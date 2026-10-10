"""Linear-work orthogonal Haar mixing: NON-GAUGE norm-budget control, not an FFT.

The full discrete orthonormal Haar transform costs N-1 local two-point
butterflies (only recursive averages, retaining all detail outputs).
Its induced 1-condition grows like sqrt(N) although kappa_2=1.
Combining with an expander Green operator therefore evades the elementary
constant-kappa1 stage count obstruction, but no Fourier identity is known.
"""

from linear_inverse import MOD
from expander_stage import apply_two_path,random_order


def root_half_mod(p=MOD):
    """A field square root of 1/2 using the supplied 8th root of unity."""
    assert (p-1)%8==0
    omega=pow(3,(p-1)//8,p)
    root2=(omega+pow(omega,-1,p))%p
    return root2*pow(2,-1,p)%p


def haar(x,scale=None,p=None):
    n=len(x)
    assert n>=2 and n&(n-1)==0
    if scale is None:
        scale=root_half_mod() if p is not None else 2**(-.5)
    v=list(x)
    detail=[]
    while len(v)>1:
        a=[];d=[]
        for i in range(0,len(v),2):
            u,w=v[i],v[i+1]
            aa=(u+w)*scale
            dd=(u-w)*scale
            if p is not None: aa%=p;dd%=p
            a.append(aa);d.append(dd)
        detail.append(d)
        v=a
    result=v
    for d in reversed(detail):result+=d
    return result


def apply_haar_green(x,order,eps=None,p=MOD):
    return haar(apply_two_path(x,order,eps=eps,p=p),p=p)


def numerical_audit(n):
    import numpy as np
    from scipy.linalg import solve_banded
    assert n&(n-1)==0
    H=np.column_stack([haar(np.eye(n)[:,j]) for j in range(n)])
    err=float(np.max(np.abs(H.T@H-np.eye(n))))
    hn1=float(np.linalg.norm(H,ord=1))
    hni=float(np.linalg.norm(H.T,ord=1))
    order=random_order(n,seed=20261009+n)
    ab=np.zeros((3,n))
    ab[0,1:]=-1;ab[1,:]=3;ab[2,:-1]=-1
    G=solve_banded((1,1),ab,np.eye(n))
    M=G+.01*G[np.ix_(order,order)]
    S=H@M
    n1=float(np.linalg.norm(S,1))
    ni=float(np.linalg.norm(np.linalg.inv(S),1))
    k2=float(np.linalg.cond(S,2))
    # May be full-rank W-I; no rank-one Householder dressing.
    rank=int(np.linalg.matrix_rank(H-np.eye(n)))
    return dict(n=n,orthogonality_error=err,haar_kappa1=hn1*hni,
                haar_minus_identity_rank=rank,
                dressed_kappa1=n1*ni,dressed_kappa2=k2,
                lower_bound_kappa1=(19/101)*n**.5)


if __name__=='__main__':
    import json
    print(json.dumps([numerical_audit(n) for n in (8,16,32,64,128)],indent=2))
