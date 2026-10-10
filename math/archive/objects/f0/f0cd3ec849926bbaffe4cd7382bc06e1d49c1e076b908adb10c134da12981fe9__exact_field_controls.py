"""Independent exact finite-field matrix-rank controls (not proofs over C)."""
from __future__ import annotations
import numpy as np


def prime_root(n:int,p:int):
    if n&(n-1) or (p-1)%n:raise ValueError('n must divide p-1 and be power of two')
    for g in range(2,p):
        z=pow(g,(p-1)//n,p)
        if pow(z,n//2,p)!=1:return z
    raise RuntimeError('no root')


def rank_mod(A,p):
    a=np.array(A,dtype=np.int64,copy=True)%p
    m,n=a.shape;row=0
    for col in range(n):
        if row>=m:break
        piv=np.flatnonzero(a[row:,col])
        if not len(piv):continue
        loc=row+int(piv[0]);a[[row,loc]]=a[[loc,row]]
        inv=pow(int(a[row,col]),-1,p)
        if row+1<m:
            scale=(a[row+1:,col]*inv)%p
            a[row+1:,col+1:]=(a[row+1:,col+1:]-scale[:,None]*a[row,col+1:])%p
            a[row+1:,col]=0
        row+=1
    return row


def fourier_rank_mod(n,rows,cols,p):
    root=prime_root(n,p)
    powers=np.array([pow(root,i,p) for i in range(n)],dtype=np.int64)
    R=np.asarray(rows,dtype=np.int64);C=np.asarray(cols,dtype=np.int64)
    return rank_mod(powers[(R[:,None]*C[None,:])%n],p)


def separated_generator_stage(n,p,rng):
    a,b,c,e,d=[rng.integers(1,p,size=n) for _ in range(5)]
    s=np.zeros((n,n),dtype=np.int64)
    for i in range(n):
        for j in range(n):
            s[i,j]=int((a[i]*b[j] if i>j else c[i]*e[j] if i<j else d[i])%p)
    return s
