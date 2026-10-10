"""Explicit all-N separation: O(N)-work separated-generator scan whose
inverse cannot be tridiagonal + low rank (< floor((N+1)/4)).

The algebraic proof over characteristic 0 is in PROOF_CERTIFICATE.md.
These exact finite-field tests independently check the inversion and minors.
"""
from __future__ import annotations
import numpy as np
import random
from sparse_defect import det_mod,rank_mod
from green_woodbury import invert_mod


def scan_matrix(n):
    return 3*np.eye(n,dtype=np.int64)+np.tril(np.ones((n,n),dtype=np.int64),-1)+2*np.triu(np.ones((n,n),dtype=np.int64),1)


def apply_scan(x,p):
    n=len(x)
    left=0;total=sum(map(int,x))%p
    y=np.empty(n,dtype=np.int64)
    for i in range(n):
        xi=int(x[i]); right=(total-left-xi)%p
        y[i]=(3*xi+left+2*right)%p
        left=(left+xi)%p
    return y



def apply_inverse_scan(x,p):
    """Sherman-Morrison scan: invert the dense global S in O(N) work.

    T=I-strict_lower_ones, S=T+2*11^T, T^-1*1=[1,2,4,...].
    y=T^-1*x with y_i=x_i+sum_(j<i) y_j.
    """
    n=len(x)
    D=(pow(2,n+1,p)-1)%p
    if not D:raise ZeroDivisionError('S singular in this field')
    accum=0
    y=[]
    for raw in x:
        z=(int(raw)+accum)%p
        y.append(z)
        accum=(accum+z)%p
    factor=2*accum*pow(D,-1,p)%p
    power=1
    result=np.empty(n,dtype=np.int64)
    for i in range(n):
        result[i]=(y[i]-factor*power)%p
        power=2*power%p
    return result

def explicit_inverse(n,p):
    D=(pow(2,n+1,p)-1)%p
    assert D!=0, 'avoid primes where 2^(n+1)=1'
    invD=pow(D,-1,p)
    mat=np.zeros((n,n),dtype=np.int64)
    for i in range(n):
        for j in range(n):
            if i==j:v=(pow(2,n,p)-1)%p
            elif i>j:v=-pow(2,i-j-1,p)
            else:v=-pow(2,n+i-j,p)
            mat[i,j]=(v*invD)%p
    return mat


def controlled_minor(n,p):
    inv=explicit_inverse(n,p)
    m=(n+1)//4
    R=[4*i for i in range(m)]
    C=[4*j+2 for j in range(m)]
    assert max(C)<n
    selected=inv[np.ix_(R,C)]
    alpha=(-pow(2,-3,p)*pow((pow(2,n+1,p)-1)%p,-1,p))%p
    beta=(-pow(2,n-2,p)*pow((pow(2,n+1,p)-1)%p,-1,p))%p
    expected=beta*pow((beta-alpha)%p,m-1,p)%p
    actual=det_mod(selected,p)
    assert actual==expected and actual!=0,(n,p,m,actual,expected)
    assert rank_mod(selected,p)==m
    return (m,actual,expected)


def check(n,p,seed=777):
    m,det,_=controlled_minor(n,p)
    A=scan_matrix(n)%p
    analytical=explicit_inverse(n,p)
    assert np.array_equal(A@analytical%p,np.eye(n,dtype=np.int64))
    assert np.array_equal(analytical@A%p,np.eye(n,dtype=np.int64))
    if n<=32:
        assert np.array_equal(invert_mod(A,p),analytical)
    rng=random.Random(seed+11*n+p)
    for _ in range(12):
        x=np.array([rng.randrange(p) for _ in range(n)],dtype=np.int64)
        assert np.array_equal(A@x%p,apply_scan(x,p))
        assert np.array_equal(analytical@x%p,apply_inverse_scan(x,p))
        assert np.array_equal(A@apply_inverse_scan(x,p)%p,x)
    # Adversarial tridiagonal baseline, selected offband block unchanged
    T=np.zeros((n,n),dtype=np.int64)
    for i in range(n):
        T[i,i]=rng.randrange(p)
        if i:
            T[i,i-1]=rng.randrange(p)
            T[i-1,i]=rng.randrange(p)
    R=[4*i for i in range(m)];C=[4*i+2 for i in range(m)]
    assert np.all(T[np.ix_(R,C)]==0)
    assert rank_mod((analytical-T)[np.ix_(R,C)],p)==m
    return {'n':n,'p':p,'minimum_rank_defect':m,'minor_determinant':det,
            'dense_operator_exact_vectors':12,'inverse_verified':True}

if __name__=='__main__':
    for p in (12289,65537):
        for n in (8,16,32,64,128):
            print(check(n,p))


def banded_separation(n:int,b:int,p:int):
    """General off-band minor for *every* width-b banded baseline."""
    if not (0<=b<=n-2):raise ValueError('0<=b<=n-2')
    h=b+1;L=2*h
    m=(n+b)//(2*b+2)
    assert m>0
    R=[L*i for i in range(m)]
    C=[L*i+h for i in range(m)]
    assert C[-1]<n and R[-1]<n
    assert all(abs(i-j)>b for i in R for j in C)
    inv=explicit_inverse(n,p)
    D=(pow(2,n+1,p)-1)%p
    invD=pow(D,-1,p)
    alpha=-pow(2,-h-1,p)*invD%p
    beta=-pow(2,n-h,p)*invD%p
    actual=det_mod(inv[np.ix_(R,C)],p)
    predicted=beta*pow((beta-alpha)%p,m-1,p)%p
    assert actual==predicted and actual
    return {'n':n,'bandwidth':b,'p':p,'rank_lower_bound':m,'det_mod_p':actual}
