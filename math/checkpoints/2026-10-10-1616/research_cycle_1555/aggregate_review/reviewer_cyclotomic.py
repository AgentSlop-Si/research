"""Fresh independent exact controls. No source or author programs are imported."""
from fractions import Fraction
from itertools import combinations, permutations
from collections import Counter
from pathlib import Path
import json, hashlib, time

P=5
D=4
ZERO=(Fraction(0),)*D
ONE=(Fraction(1),)+(Fraction(0),)*(D-1)

def add(x,y): return tuple(a+b for a,b in zip(x,y))
def neg(x): return tuple(-a for a in x)
def sub(x,y): return add(x,neg(y))
def mul(x,y):
    q=[Fraction(0)]*(2*D-1)
    for i,a in enumerate(x):
        if a:
            for j,b in enumerate(y):
                if b:q[i+j]+=a*b
    for k in range(len(q)-1,D-1,-1):
        for h in range(D):q[k-D+h]-=q[k]
    return tuple(q[:D])
def scale(x,a): return tuple(v*a for v in x)
def power(k):
    k%=P
    if k<D:return tuple(Fraction(i==k) for i in range(D))
    return (Fraction(-1),)*D
POWERS=[power(k) for k in range(P)]
def conjugate(x,a):
    y=ZERO
    for k,v in enumerate(x): y=add(y,scale(POWERS[a*k%P],v))
    return y
def inv(x):
    assert x!=ZERO
    y=ONE
    for a in (2,3,4):y=mul(y,conjugate(x,a))
    n=mul(x,y)
    assert all(z==0 for z in n[1:]) and n[0]
    return scale(y,1/n[0])
def echelon(rows):
    m=[list(r) for r in rows]; piv=[]; r=0
    for c in range(len(m[0])):
        k=next((k for k in range(r,len(m)) if m[k][c]!=ZERO),None)
        if k is None:continue
        m[r],m[k]=m[k],m[r]
        u=inv(m[r][c]);m[r]=[mul(z,u) for z in m[r]]
        for k in range(r+1,len(m)):
            a=m[k][c]
            if a!=ZERO:m[k]=[sub(v,mul(a,z)) for v,z in zip(m[k],m[r])]
        piv.append(c);r+=1
        if r==len(m):break
    return m,piv

def nullvector_rank4(m,piv):
    assert len(piv)==4
    free=next(c for c in range(5) if c not in piv)
    x=[ZERO]*5;x[free]=ONE
    for r,c in reversed(list(enumerate(piv))):
        v=ZERO
        for j in range(c+1,5):v=add(v,mul(m[r][j],x[j]))
        x[c]=neg(v)
    return x

def wire_pattern_3():
    off=[(i,j) for i in range(3) for j in range(3) if i!=j]
    hist=Counter()
    for k in range(3):
        for s in combinations(off,k):
            if k<2:kind='inverse_support_no_expansion'
            else:
                (i,j),(u,v)=s
                if i==v and j==u:kind='two_cycle'
                elif j==u or v==i:kind='three_vertex_chain'
                else:kind='inverse_support_no_expansion'
            hist[k,kind]+=1
    return [{'off_diagonal_entries':k,'pattern':s,'count':n} for (k,s),n in sorted(hist.items())]

