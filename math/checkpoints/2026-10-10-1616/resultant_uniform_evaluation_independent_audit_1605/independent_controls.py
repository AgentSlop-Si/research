"""Independent controls authored from mathematical statements, without author-program imports."""
from fractions import Fraction
from itertools import permutations, product
from collections import Counter
from pathlib import Path
import json, random, hashlib, time
ROOT=Path(__file__).resolve().parent

class Field:
    def __init__(self, tag): self.tag=tag; self.p=0 if tag=='Q' else (2 if tag=='F4' else int(tag[1:])); self.ops=0
    def n(self,a): return Fraction(a) if not self.p else int(a)%self.p
    def add(self,a,b):
        self.ops+=1
        return a+b if not self.p else (a^b if self.tag=='F4' else (a+b)%self.p)
    def neg(self,a): return a if self.tag=='F4' else (-a if not self.p else -a%self.p)
    def sub(self,a,b): return self.add(a,self.neg(b))
    def mul(self,a,b):
        self.ops+=1
        if self.tag=='F4':
            r=0
            while b:
                if b&1:r^=a
                b>>=1;a<<=1
                if a&4:a^=7
            return r
        return a*b if not self.p else a*b%self.p
    def pow(self,a,n):
        if n<0:return self.pow(self.inv(a),-n)
        z=self.n(1)
        while n:
            if n&1:z=self.mul(z,a)
            n//=2
            if n:a=self.mul(a,a)
        return z
    def inv(self,a):
        assert a!=0, 'division by zero'
        self.ops+=1
        return 1/a if not self.p else (self.pow(a,2) if self.tag=='F4' else pow(a,-1,self.p))
    def div(self,a,b): return self.mul(a,self.inv(b))
    def rand(self,rng): return rng.randrange(4) if self.tag=='F4' else self.n(rng.randrange(-3,4))

def trim(a):
    a=list(a)
    while a and a[-1]==0:a.pop()
    return a

def padd(a,b,F):
    c=[F.n(0)]*max(len(a),len(b))
    for i in range(len(c)):c[i]=F.add(a[i] if i<len(a) else F.n(0),b[i] if i<len(b) else F.n(0))
    return trim(c)

def pmul(a,b,F):
    if not a or not b:return []
    c=[F.n(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]=F.add(c[i+j],F.mul(x,y))
    return trim(c)

def cancel(a,b,c,shift,F):
    out=list(a)+[F.n(0)]*max(0,len(b)+shift-len(a))
    for j,y in enumerate(b):out[j+shift]=F.sub(out[j+shift],F.mul(c,y))
    return trim(out)

def peval(a,x,F):
    v=F.n(0)
    for z in reversed(a):v=F.add(F.mul(v,x),z)
    return v

def rem(a,b,F):
    a=trim(a);b=trim(b);assert b
    while len(a)>=len(b) and a:
        a=cancel(a,b,F.div(a[-1],b[-1]),len(a)-len(b),F)
    return a

def permutation_det(P,F):
    n=len(P);ans=[]
    for sigma in permutations(range(n)):
        a=[F.n(-1 if sum(sigma[i]>sigma[j] for i in range(n) for j in range(i+1,n))%2 else 1)]
        for i,j in enumerate(sigma):a=pmul(a,P[i][j],F)
        ans=padd(ans,a,F)
    return ans

def scalar_det(M,F):
    A=[list(r) for r in M];n=len(A);d=F.n(1)
    for j in range(n):
        k=next((k for k in range(j,n) if A[k][j]),None)
        if k is None:return F.n(0)
        if k!=j:A[j],A[k]=A[k],A[j];d=F.neg(d)
        pivot=A[j][j];d=F.mul(d,pivot)
        for i in range(j+1,n):
            if A[i][j]:
                c=F.div(A[i][j],pivot)
                for k in range(j+1,n):A[i][k]=F.sub(A[i][k],F.mul(c,A[j][k]))
                A[i][j]=F.n(0)
    return d

def pivot(row):
    d=max((len(a)-1 for a in row),default=-1)
    if d<0:return (-1,-1)
    return d,max(j for j,a in enumerate(row) if len(a)-1==d)

def weak_det(P,F):
    # Cache pivots; retain only the current linear core and current side column.
    T=[[list(a) for a in row] for row in P];m=len(T);factors=[];nred=0;maxside=0;startops=F.ops;oldscore=None
    while len(T)>1:
        q=len(T);M=[row[:-1] for row in T];v=[row[-1] for row in T];meta=[pivot(row) for row in M]
        degrees0=sum(d for d,p in meta)
        score=sum(m*d+p+1 for d,p in meta if p>=0)
        if oldscore is not None:assert score<=oldscore
        while True:
            seen={};pair=None
            for i,(d,p) in enumerate(meta):
                if p<0:continue
                if p in seen:pair=(seen[p],i);break
                seen[p]=i
            if pair is None:break
            a,b=pair
            if meta[a][0]>meta[b][0]:a,b=b,a
            da,pa=meta[a];db,pb=meta[b];shift=db-da
            c=F.div(M[b][pb][-1],M[a][pa][-1])
            M[b]=[cancel(x,y,c,shift,F) for x,y in zip(M[b],M[a])]
            v[b]=cancel(v[b],v[a],c,shift,F)
            meta[b]=pivot(M[b]);nred+=1
            newscore=sum(m*d+p+1 for d,p in meta if p>=0)
            assert newscore<score;score=newscore
            assert all(d<=1 for d,p in meta)
            delta=degrees0-sum(d for d,p in meta)
            assert 0<=delta<=2*q
            assert all(len(v[i])-1<=meta[i][0]+2+delta for i in range(q))
            maxside=max(maxside,max(len(a)-1 for a in v));assert maxside<=2*m+3
        oldscore=score
        k=next(i for i,(d,p) in enumerate(meta) if p<0)
        h=v[k]
        if (k+q-1)%2:h=[F.neg(x) for x in h]
        if not h:return [],dict(reductions=nred,max_side_degree=maxside,field_ops=F.ops-startops,zero_factor=True)
        factors.append(h);T=[r for i,r in enumerate(M) if i!=k]
    factors.append(T[0][0]);assert nred<=2*m*m
    if not factors[-1]:return [],dict(reductions=nred,max_side_degree=maxside,field_ops=F.ops-startops,zero_factor=True)
    assert sum(len(f)-1 for f in factors)<=m
    z=[F.n(1)]
    for f in factors:z=pmul(z,f,F)
    return z,dict(reductions=nred,max_side_degree=maxside,field_ops=F.ops-startops,zero_factor=False)

def ordinary_resultant(f,g,F):
    f=trim(f);g=trim(g)
    if not f or not g:return F.n(0)
    sign=F.n(1)
    while True:
        r=len(f)-1;s=len(g)-1
        if s==0:return F.mul(sign,F.pow(g[0],r))
        if r<s:
            if r*s%2:sign=F.neg(sign)
            f,g=g,f;continue
        h=rem(f,g,F)
        if not h:return F.n(0)
        if r*s%2:sign=F.neg(sign)
        sign=F.mul(sign,F.pow(g[-1],r-(len(h)-1)))
        f,g=g,h

def padded_resultant(f,g,m,F,sign_mutant=False):
    f=trim(f);g=trim(g)
    if not f or not g:return F.n(0)
    r=len(f)-1;s=len(g)-1
    if r<m and s<m:return F.n(0)
    value=ordinary_resultant(f,g,F)
    if r==m:return F.mul(F.pow(f[-1],m-s),value)
    assert s==m
    if (m*(m-r))%2 and not sign_mutant:value=F.neg(value)
    return F.mul(F.pow(g[-1],m-r),value)

def sylvester(f,g,m,F):
    f=list(f)+[F.n(0)]*(m+1-len(f));g=list(g)+[F.n(0)]*(m+1-len(g))
    S=[]
    for h in (f[::-1],g[::-1]):
        for j in range(m):S.append([F.n(0)]*j+h+[F.n(0)]*(m-1-j))
    return scalar_det(S,F)

def pencil(C,E,F):return [[trim([C[i][j],E[i][j]]) for j in range(len(C))] for i in range(len(C))]

def node(A,B,w,F,omit_tangent_B=False):
    if not w:raise ValueError('zero quotient node')
    m=len(A)
    if w==F.n(1):
        C=[[F.mul(F.n(i+j),A[i][j]) for j in range(m)] for i in range(m)]
        E=[[F.mul(F.n(i+j+(not omit_tangent_B)),B[i][j]) for j in range(m)] for i in range(m)]
        f,_=weak_det(pencil(C,A,F),F);g,_=weak_det(pencil(E,B,F),F)
        return padded_resultant(f,g,m,F)
    C=[[F.neg(F.mul(F.pow(w,i+j),A[i][j])) for j in range(m)] for i in range(m)]
    E=[[F.neg(F.mul(F.pow(w,i+j+1),B[i][j])) for j in range(m)] for i in range(m)]
    f,_=weak_det(pencil(A,C,F),F);g,_=weak_det(pencil(B,E,F),F)
    r=padded_resultant(f,g,m,F)
    den=F.mul(F.pow(w,m*m*(m-1)),F.pow(F.sub(w,F.n(1)),m*m))
    return F.div(r,den)

def s_laurent(n,w,F):
    # Direct finite sum, including endpoints; never divide by w-1.
    z=F.n(0)
    for k in (range(n) if n>=0 else range(n,0)):
        z=F.add(z,F.pow(w,k))
    return z if n>=0 else F.neg(z)

def residual_oracle(A,B,w,F):
    m=len(A)
    N=[[F.mul(F.mul(A[i][j],B[k][l]),s_laurent(1+k-i+l-j,w,F)) for j in range(m) for l in range(m)] for i in range(m) for k in range(m)]
    return scalar_det(N,F)

def encode(v):
    if isinstance(v,Fraction):return str(v)
    if isinstance(v,list):return [encode(x) for x in v]
    if isinstance(v,dict):return {k:encode(x) for k,x in v.items()}
    return v

rng=random.Random(16051010);records=[];mutations=[]
def record(kind,**kw):records.append(dict(kind=kind,**encode(kw)))
for tag in ('Q','F2','F3','F5','F7','F101','F4'):
    F=Field(tag)
    for m in range(1,7):
        for case in range(20):
            C=[[F.rand(rng) for j in range(m)] for i in range(m)]
            E=[[F.rand(rng) for j in range(m)] for i in range(m)]
            if case%5==0:C[0]=[F.n(0)]*m
            if case%5==1:E[-1]=[F.n(0)]*m
            if case%5==2 and m>1:C[-1]=C[0][:];E[-1]=E[0][:]
            if case%5==3:E=[[F.n(0)]*m for _ in range(m)]
            P=pencil(C,E,F);got,stats=weak_det(P,F);want=permutation_det(P,F)
            assert got==want,(tag,m,case,got,want)
            record('pencil',field=tag,m=m,case=case,coefficients=got,**stats)
    # Every scalar degree stratum, with independent padded Sylvester determinant.
    for m in range(1,9):
        for r in range(-1,m+1):
            for s in range(-1,m+1):
                f=[F.rand(rng) for _ in range(r+1)];g=[F.rand(rng) for _ in range(s+1)]
                if f and not f[-1]:f[-1]=F.n(1)
                if g and not g[-1]:g[-1]=F.n(1)
                got=padded_resultant(f,g,m,F);want=sylvester(f,g,m,F)
                assert got==want,(tag,m,r,s,got,want)
                record('padding',field=tag,m=m,r=r,s=s,value=got)
    for m in range(1,6):
        for case in range(14):
            A=[[F.rand(rng) for _ in range(m)] for _ in range(m)]
            B=[[F.rand(rng) for _ in range(m)] for _ in range(m)]
            if case==0:A=[[F.n(0)]*m for _ in range(m)]
            if case in (1,2,3) and m>1:A[-1]=A[0][:]
            if case in (2,3,4) and m>1:B[-1]=B[0][:]
            if case in (5,6):A=[[F.n(i==j) for j in range(m)] for i in range(m)]
            if case in (5,7):B=[[F.n(i==j) for j in range(m)] for i in range(m)]
            nodes=([F.n(1),F.n(-1),Fraction(2),Fraction(-2),Fraction(3,2)] if tag=='Q' else (list(range(1,4)) if tag=='F4' else list(range(1,min(F.p,8)))))
            for w in dict.fromkeys(nodes):
                got=node(A,B,w,F);want=residual_oracle(A,B,w,F)
                assert got==want,(tag,m,case,w,got,want)
                reciprocal=node(A,B,F.inv(w),F);assert got==reciprocal
                record('C03_node',field=tag,m=m,case=case,w=w,value=got,reciprocal=True)
    try:node([[F.n(1)]],[[F.n(1)]],F.n(0),F)
    except ValueError:record('zero_node_rejected',field=tag)
    else:raise AssertionError('zero node accepted')
    print(tag, len(records), flush=True)

# Exhaustive binary 2x2 pencils.
F=Field('F2')
for entries in product((0,1),repeat=8):
    C=[list(entries[:2]),list(entries[2:4])];E=[list(entries[4:6]),list(entries[6:])]
    P=pencil(C,E,F);got,stats=weak_det(P,F);assert got==permutation_det(P,F)
    record('binary_exhaustive_pencil',entries=list(entries),coefficients=got,**stats)

# Exact adversarial controls with deliberately incorrect alternatives.
F=Field('Q');A=[[Fraction(1)]*2 for _ in range(2)];I=[[Fraction(i==j) for j in range(2)] for i in range(2)]
f=[Fraction(0),Fraction(-1)];g=[Fraction(1),Fraction(-10),Fraction(16)]
correct=node(A,I,Fraction(2),F);mutant=F.div(ordinary_resultant(f,g,F),Fraction(16));assert correct!=mutant
mutations.append(dict(name='trim_nonendpoint_padding',correct=correct,mutant=mutant))
correct=node(A,A,Fraction(1),F);mutant=ordinary_resultant([Fraction(-1)],[Fraction(-1)],F);assert correct!=mutant
mutations.append(dict(name='trim_constant_tangent_padding',correct=correct,mutant=mutant))
f=[Fraction(1)];g=[Fraction(1),Fraction(0),Fraction(0),Fraction(1)]
correct=padded_resultant(f,g,3,F);mutant=padded_resultant(f,g,3,F,True);assert correct!=mutant
mutations.append(dict(name='omit_odd_padding_sign',correct=correct,mutant=mutant))
correct=node(I,I,Fraction(1),F);mutant=node(I,I,Fraction(1),F,True);assert correct!=mutant
mutations.append(dict(name='omit_tangent_plus_B',correct=correct,mutant=mutant))
for name,C,E in [
 ('nonzero_columns_do_not_certify_regular',[[1,0],[0,0]],[[0,1],[0,0]]),
 ('singular_constant_and_leading_can_be_regular',[[0,0],[0,1]],[[1,0],[0,0]])]:
    C=[[F.n(x) for x in row] for row in C];E=[[F.n(x) for x in row] for row in E]
    P=pencil(C,E,F);got,_=weak_det(P,F);assert got==permutation_det(P,F)
    mutations.append(dict(name=name,determinant=got,constant_det=scalar_det(C,F),leading_det=scalar_det(E,F)))
F=Field('F2');P=pencil([[0,0],[0,1]],[[1,0],[0,1]],F);got,_=weak_det(P,F)
assert got==[0,1,1] and all(peval(got,w,F)==0 for w in (0,1))
mutations.append(dict(name='base_field_sampling_cannot_test_polynomial_rank',field='F2',determinant=got,values=[peval(got,w,F) for w in (0,1)]))
try:
    F=Field('Q');F.div(F.n(0),F.pow(F.sub(F.n(1),F.n(1)),4))
except AssertionError:
    mutations.append(dict(name='generic_branch_at_w1_divides_by_zero',rejected=True,correct=node(I,I,Fraction(1),F)))

result=dict(status='PASS',authorship='Fresh independent implementation. No author executable was run or imported.',record_count=len(records),counts=dict(Counter(r['kind'] for r in records)),mutation_count=len(mutations),mutations=encode(mutations),records=records)
(ROOT/'INDEPENDENT_CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))
