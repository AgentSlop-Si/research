"""Exact Fourier-submatrix ranks for unions of complete dyadic cosets.

N=Q*L with Q=2**a and L=N/Q. Let B subset {0,...,Q-1} and
S = union_{b in B} {b+Q*j : 0<=j<L}.
For rows K any frequency set, let T_q = {s : q+L*s in K}.
Then
 rank(F_N[K,S]) = sum_{q=0}^{L-1} rank(F_Q[T_q,B]).

This is a field-independent exact identity when a primitive Nth root exists
and the characteristic does not divide N. The modular routines below are
only independently checkable positive controls.
"""
import numpy as np


def prim_root(n,p):
    assert (p-1)%n==0
    for g in range(2,p):
        z=pow(g,(p-1)//n,p)
        if pow(z,n,p)==1 and (n==1 or pow(z,n//2,p)!=1):return z
    raise ValueError((n,p))


def rank_mod(X,p):
    A=np.asarray(X,dtype=np.int64).copy()%p
    if not A.size:return 0
    r=0;nr,nc=A.shape
    for j in range(nc):
        if r==nr:break
        inds=np.flatnonzero(A[r:,j])
        if inds.size==0:continue
        k=r+int(inds[0]);A[[k,r]]=A[[r,k]]
        A[r,j:] = (A[r,j:]*pow(int(A[r,j]),-1,p))%p
        if r+1<nr:
            f=A[r+1:,j].copy()
            A[r+1:,j:] = (A[r+1:,j:]-f[:,None]*A[r,j:])%p
        r+=1
    return r


def fourier_submatrix(n,rows,cols,p):
    z=prim_root(n,p)
    return np.array([[pow(z,i*j,p) for j in cols] for i in rows],dtype=np.int64)


def dyadic_union_columns(n,q,bases):
    assert n%q==0 and q&(q-1)==0
    L=n//q
    return sorted(b+q*j for b in bases for j in range(L))


def rank_coset_formula(n,q,bases,rows,p):
    assert n%q==0 and q&(q-1)==0
    L=n//q
    tot=0
    for residue in range(L):
        small_rows=[(k-residue)//L for k in rows if k%L==residue]
        if small_rows and bases:
            tot+=rank_mod(fourier_submatrix(q,small_rows,bases,p),p)
    return tot


def single_consecutive_coset_formula(n,q,b,rows,length):
    # Columns b+q*j, j=0,...,length-1, length<=n//q.
    L=n//q
    assert length<=L and b in range(q)
    return min(length,len({r%L for r in rows}))
