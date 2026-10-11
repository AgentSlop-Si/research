#!/usr/bin/env python3
"""Fresh reviewer controls. Executes no supplied/inherited research programs.
Exact cyclotomic ranks use integer polynomial quotient arithmetic and row gcd
normalization, with division-free field elimination. Finite sampling verifies
controls only, never substitutes for the reviewed uniform proof.
"""
from itertools import combinations, product
from fractions import Fraction
from math import gcd, lcm, prod
from functools import reduce
from collections import Counter
import json, hashlib
from pathlib import Path

OUT=Path(__file__).resolve().parent
class Cyclotomic:
    def __init__(self, n):
        # Known cyclotomic moduli in ascending order, including leading 1.
        pol={1:[-1,1],2:[1,1],3:[1,1,1],4:[1,0,1],6:[1,-1,1],8:[1,0,0,0,1],16:[1]+[0]*7+[1]}
        self.n=n; self.f=pol[n]; self.d=len(self.f)-1
        self.zero=(0,)*self.d; self.one=(1,)+(0,)*(self.d-1)
        self.powers=[]
        for k in range(n):
            a=[0]*(max(k,self.d-1)+1);a[k]=1;self.powers.append(self.red(a))
        assert self.red([0]*n+[1])==self.one
        for q in range(1,n):assert self.powers[q]!=self.one
    def red(self,a):
        a=list(a)+[0]*max(0,self.d-len(a))
        for k in range(len(a)-1,self.d-1,-1):
            c=a[k]
            if c:
                for j in range(self.d):a[k-self.d+j]-=c*self.f[j]
        return tuple(a[:self.d])
    def mul(self,a,b):
        c=[0]*(2*self.d-1)
        for i,x in enumerate(a):
            if x:
                for j,y in enumerate(b):
                    if y:c[i+j]+=x*y
        return self.red(c)
    def sub(self,a,b):return tuple(x-y for x,y in zip(a,b))
    def add(self,a,b):return tuple(x+y for x,y in zip(a,b))
    def conj(self,a):
        out=self.zero
        for j,x in enumerate(a):
            if x:out=self.add(out,tuple(x*y for y in self.powers[-j%self.n]))
        return out
    def rank(self,M):
        if not M:return 0
        A=[[tuple(x) for x in row] for row in M]
        r=0
        for c in range(len(A[0])):
            p=next((i for i in range(r,len(A)) if A[i][c]!=self.zero),None)
            if p is None:continue
            A[p],A[r]=A[r],A[p]
            for i in range(r+1,len(A)):
                z=A[i][c]
                if z==self.zero:continue
                a=A[r][c]
                A[i]=[self.zero]*(c+1)+[self.sub(self.mul(a,A[i][j]),self.mul(z,A[r][j])) for j in range(c+1,len(A[0]))]
                g=reduce(gcd,(abs(v) for x in A[i] for v in x),0)
                if g>1:A[i]=[tuple(v//g for v in x) for x in A[i]]
            r+=1
            if r==len(A):break
        return r

def bitreverse(n):
    m=n.bit_length()-1
    return [int(f'{i:0{m}b}'[::-1],2) if m else 0 for i in range(n)]

def recurrence(n,k):
    if k==0 or k==n:return 0
    if n==2:return 1
    if k>n//2:return recurrence(n,n-k)
    return (k+1)//2+recurrence(n//4,k//2)

def lower(n,k):
    f=Fraction(k*(n-k),n)
    if k%2:f*=Fraction(n+1,n)
    return (f.numerator+f.denominator-1)//f.denominator

result={'method':'Fresh standard-library exact cyclotomic quotient-field rank controls; no inherited program executed.', 'bit_reversal_profiles':{}, 'critical_N8':{}, 'half_square':{},'finite_abelian_rectangles':{},'rational_algebra':{}}
for n in (1,2,4,8,16):
    K=Cyclotomic(n);b=bitreverse(n)
    p=[K.rank([[K.powers[(b[i]*b[j])%n] for j in range(k,n)] for i in range(k)]) for k in range(1,n)]
    expected=[recurrence(n,k) for k in range(1,n)]
    assert p==expected
    result['bit_reversal_profiles'][str(n)]={'ranks':p,'maximum':max(p,default=0),'sum':sum(p)}
    if n>=4:
        E=range(0,n,2)
        assert K.rank([[K.powers[a*b%n] for b in E] for a in E])==n//4
        result['half_square'][str(n)]={'even_even_rank':n//4}

K=Cyclotomic(8);counts=Counter()
for R in combinations(range(8),3):
    for H in combinations(range(8),5):
        rk=K.rank([[K.powers[a*b%8] for b in H] for a in R]);assert rk>=3;counts[rk]+=1
result['critical_N8']={'rectangles':sum(counts.values()),'rank_distribution':dict(counts)}
counts=Counter()
for R in combinations(range(8),4):
    for H in combinations(range(8),4):
        rk=K.rank([[K.powers[a*b%8] for b in H] for a in R]);assert rk>=2;counts[rk]+=1
result['half_square']['8']['exhaustive_rectangles']=sum(counts.values());result['half_square']['8']['rank_distribution']=dict(counts)

# Exhaustive deficit rank checks for genuinely different group structures.
# All nonempty row and column subsets; squared spectral norm claims are
# checked analytically in REVIEW.md, without floating-point acceptance.
for shape in ((2,2),(3,),(4,),(6,)):
    G=list(product(*(range(x) for x in shape)));n=len(G);e=lcm(*shape);K=Cyclotomic(e)
    T=[[K.powers[sum(a*b*(e//q) for a,b,q in zip(x,y,shape))%e] for y in G] for x in G]
    subs=[tuple(i for i in range(n) if mask>>i&1) for mask in range(1,1<<n)]
    ds={}
    for H in subs:
        HS={G[i] for i in H};mx=0
        for s in G[1:]:
            overlap=sum(tuple((x[j]+s[j])%shape[j] for j in range(len(shape))) in HS for x in HS)
            mx=max(mx,overlap)
        ds[H]=len(H)-mx
    c=0;strict=0;moment_checks=0
    for R in subs:
        for H in subs:
            r=len(R);h=len(H);d=ds[H]
            bound=Fraction(r*h,n)+Fraction(d*r*(n-r),n*n)
            B=h-bound
            rank=K.rank([[T[i][j] for j in H] for i in R])
            ceiling=(bound.numerator+bound.denominator-1)//bound.denominator
            assert rank>=ceiling
            assert 0<=bound<=min(r,h) and B>=0
            I=tuple(i for i in range(n) if i not in R)
            # Direct complementary-Gram squared Frobenius norm, with N^2
            # cleared, independently checked against the overlap expansion.
            trace_n2=K.zero
            for x in H:
                for y in H:
                    g=K.zero
                    for i in I:g=K.add(g,K.mul(K.conj(T[i][x]),T[i][y]))
                    trace_n2=K.add(trace_n2,K.mul(K.conj(g),g))
            expanded=K.zero;HS={G[i] for i in H}
            for si,s in enumerate(G):
                overlap=sum(tuple((x[j]+s[j])%shape[j] for j in range(len(shape))) in HS for x in HS)
                f=K.zero
                for i in I:f=K.add(f,T[i][si])
                expanded=K.add(expanded,tuple(overlap*z for z in K.mul(K.conj(f),f)))
            assert trace_n2==expanded
            # For exponent 2,3,4,6, all real field elements are rational.
            assert all(z==0 for z in trace_n2[1:])
            assert Fraction(trace_n2[0],n*n)<=B
            moment_checks+=1
            base=(r*h+n-1)//n
            strict+=ceiling>base;c+=1
    result['finite_abelian_rectangles']['x'.join(map(str,shape))]={'rectangles':c,'strict_ceiling_improvements':strict,'exact_gram_moment_identity_and_bound_checks':moment_checks}

for n in (8,16,32,64,128,256,512,1024,2048,4096):
    L=n//4;B=Fraction(L)+Fraction(3,4)+Fraction(1,4*L)+Fraction(1,16*L*L)
    assert B<L+1
    assert B==Fraction((2*L+1)**2,n)-Fraction((2*L-1)*(2*L+1),n*n)
    p=[recurrence(n,k) for k in range(1,n)]
    m=n.bit_length()-1
    S=Fraction(n*n,6)+n*(Fraction(m,8)+ (Fraction(1,24) if m%2 else -Fraction(1,6)))
    assert sum(p)==S and max(p)==n//4+1
    if n in (8,16):assert p==[lower(n,k) for k in range(1,n)]
    result['rational_algebra'][str(n)]={'B':str(B),'rank_sum':sum(p),'lower_profile_sum':sum(lower(n,k) for k in range(1,n))}
assert result['bit_reversal_profiles']['4']['maximum']==1
result['status']='PASS'
(OUT/'EXACT_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
