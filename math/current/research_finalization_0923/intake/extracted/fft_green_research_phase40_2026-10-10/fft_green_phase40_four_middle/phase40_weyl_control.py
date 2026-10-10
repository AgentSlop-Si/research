"""Exact matrix-free Fourier phase audit for a product of three sums
of two independently weighted Hamiltonian-cycle Green resolvents.

Negative controls are finite-instance evidence only. Positive control
uses the ordinary radix-two DFT over a finite field.
"""
from __future__ import annotations
import random
from phase40_holonomy import random_problem, double_green_apply

def fft_positive(x,p,g):
    n=len(x)
    assert n>=2 and n&(n-1)==0 and (p-1)%n==0
    y=[int(v)%p for v in x]
    j=0
    for i in range(1,n):
        bit=n>>1
        while j&bit:j^=bit;bit>>=1
        j^=bit
        if i<j:y[i],y[j]=y[j],y[i]
    omega=pow(g,(p-1)//n,p)
    m=2
    while m<=n:
        wm=pow(omega,n//m,p)
        for start in range(0,n,m):
            w=1
            for k in range(m//2):
                a=y[start+k]
                b=y[start+k+m//2]*w%p
                y[start+k]=(a+b)%p
                y[start+k+m//2]=(a-b)%p
                w=w*wm%p
        m*=2
    return y

def green_product(n,p,g,seed=40):
    rng=random.Random(seed+n+p)
    pairs=[]
    for t in range(3):pairs.append(random_problem(n,p,seed+1000*t))
    root=pow(g,(p-1)//n,p)
    mask1=[pow(root,(j*j+3*j)%n,p) for j in range(n)]
    mask2=[pow(root,(3*j*j+j+1)%n,p) for j in range(n)]
    def apply(x):
        y=double_green_apply(*pairs[2],x,p)
        y=[v*m%p for v,m in zip(y,mask2)]
        y=double_green_apply(*pairs[1],y,p)
        y=[v*m%p for v,m in zip(y,mask1)]
        return double_green_apply(*pairs[0],y,p)
    return apply

def defect_counts(apply,n,p,g,seed=44040):
    rng=random.Random(seed+n+p)
    x=[rng.randrange(1,p) for _ in range(n)]
    omega=pow(g,(p-1)//n,p)
    power=[pow(omega,k,p) for k in range(n)]
    fx=apply(x)
    zx=[x[(i-1)%n] for i in range(n)]
    dx=[x[i]*power[i]%p for i in range(n)]
    y1=apply(zx)
    y2=apply(dx)
    d1=[(y1[i]-power[i]*fx[i])%p for i in range(n)]
    d2=[(y2[i]-fx[(i+1)%n])%p for i in range(n)]
    return (sum(v!=0 for v in d1),sum(v!=0 for v in d2))

if __name__=='__main__':
    for p,g in ((998244353,3),(2013265921,31)):
        for n in (8,16,32,64,128):
            control=defect_counts(lambda x: fft_positive(x,p,g),n,p,g)
            assert control==(0,0),control
            failure=defect_counts(green_product(n,p,g),n,p,g)
            assert failure!=(0,0)
            print(dict(N=n,prime=p,reference=control,weighted_green_product=failure))
