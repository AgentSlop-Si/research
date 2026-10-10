"""Executable O(Nr) Green+low-rank inverse stage, exact over finite fields.

For A=T+U V^T with tridiagonal T, compute A^{-1}x using a Thomas
plan plus Woodbury.  This is an actual dense global operator with
N-linear fresh-input cost at fixed r, illustrating the new theorem's scope.
"""
from __future__ import annotations
import random
import numpy as np
from sparse_defect import rank_mod


class TriSolve:
    def __init__(self,n:int,p:int,diag=None,lower=None,upper=None):
        self.p=p;self.n=n
        self.diag=tuple(int(z)%p for z in (diag or [5]*n))
        self.low=tuple(int(z)%p for z in (lower or [-1]*(n-1)))
        self.up=tuple(int(z)%p for z in (upper or [-1]*(n-1)))
        self.ell=[];piv=[self.diag[0]]
        assert piv[0]
        for i in range(1,n):
            h=self.low[i-1]*pow(piv[i-1],-1,p)%p
            val=(self.diag[i]-h*self.up[i-1])%p
            assert val
            self.ell.append(h);piv.append(val)
        self.inv=[pow(z,-1,p) for z in piv]

    def apply(self,x):
        n,p=self.n,self.p
        y=list(map(int,x))
        for i in range(1,n):y[i]=(y[i]-self.ell[i-1]*y[i-1])%p
        y[n-1]=y[n-1]*self.inv[n-1]%p
        for i in range(n-2,-1,-1):
            y[i]=(y[i]-self.up[i]*y[i+1])*self.inv[i]%p
        return np.array(y,dtype=np.int64)

    def matrix(self):
        T=np.zeros((self.n,self.n),dtype=np.int64)
        for i in range(self.n):
            T[i,i]=self.diag[i]
            if i:
                T[i,i-1]=self.low[i-1]
                T[i-1,i]=self.up[i-1]
        return T


def invert_mod(M,p):
    A=np.array(M,dtype=np.int64,copy=True)%p
    n=A.shape[0]
    assert A.shape==(n,n)
    right=np.eye(n,dtype=np.int64)
    for j in range(n):
        inds=np.flatnonzero(A[j:,j]);assert len(inds)>0,'singular'
        k=j+int(inds[0])
        if j!=k:
            A[[j,k]]=A[[k,j]]
            right[[j,k]]=right[[k,j]]
        inv=pow(int(A[j,j]),-1,p)
        A[j,:]=A[j,:]*inv%p
        right[j,:]=right[j,:]*inv%p
        for i in range(n):
            if i==j:continue
            fac=int(A[i,j])
            if fac:
                A[i,:]=(A[i,:]-fac*A[j,:])%p
                right[i,:]=(right[i,:]-fac*right[j,:])%p
    assert np.array_equal(A,np.eye(n,dtype=np.int64))
    return right


class GreenLowRank:
    def __init__(self,T:TriSolve,U,V):
        self.T=T;self.p=T.p
        self.U=np.array(U,dtype=np.int64)%T.p
        self.V=np.array(V,dtype=np.int64)%T.p
        n,r=self.U.shape
        assert self.V.shape==(n,r) and n==T.n
        self.Z=np.column_stack([T.apply(self.U[:,j]) for j in range(r)]) if r else np.empty((n,0),dtype=np.int64)
        K=(np.eye(r,dtype=np.int64)+self.V.T@self.Z)%T.p
        self.Kinv=invert_mod(K,T.p) if r else K

    def apply(self,x):
        p=self.p
        y=self.T.apply(x)
        r=self.U.shape[1]
        if not r:return y
        v=self.V.T@y %p
        q=self.Kinv@v%p
        return (y-self.Z@q)%p

    def inverse_matrix(self):
        return (self.T.matrix()+self.U@self.V.T)%self.p


def check_green(n:int,r:int,p:int,seed:int=207):
    rng=random.Random(seed+n*13+r*7+p)
    T=TriSolve(n,p)
    for attempt in range(50):
        U=np.array([[rng.randrange(1,p) for _ in range(r)] for _ in range(n)],dtype=np.int64)
        V=np.array([[rng.randrange(1,p) for _ in range(r)] for _ in range(n)],dtype=np.int64)
        try:G=GreenLowRank(T,U,V);break
        except AssertionError:continue
    else:raise AssertionError('failed to find invertible lowrank correction')
    A=G.inverse_matrix()
    denseG=invert_mod(A,p)
    zeros=int(np.count_nonzero(denseG==0))
    rankE=rank_mod(U@V.T%p,p)
    assert rankE<=r
    for _ in range(20):
        x=np.array([rng.randrange(p) for _ in range(n)],dtype=np.int64)
        y=G.apply(x)
        assert np.array_equal(y, denseG@x%p)
        assert np.array_equal(A@y%p,x)
    return dict(n=n,p=p,r=r,rank_E=rankE,zero_entries_of_global_stage=zeros,
                vectors_verified=20,stage_inverse_rank=n)

if __name__=='__main__':
    for p in (12289,65537):
        for n in (8,16,32,64):
            print(check_green(n,1,p))
