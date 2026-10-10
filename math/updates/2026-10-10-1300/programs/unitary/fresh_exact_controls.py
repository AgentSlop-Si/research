#!/usr/bin/env python3
"""Fresh audit controls. No submitted implementation is read, imported, or run.
Exact arithmetic in Q[x]/(x^4-x^2+1), x=exp(2*pi*i/12).
"""
from fractions import Fraction as F
from itertools import permutations, product
from pathlib import Path
import json, hashlib, random, time

class E:
    __slots__=("a",)
    def __init__(self,v=0):
        if isinstance(v,E): self.a=v.a
        elif isinstance(v,(tuple,list)): self.a=tuple(F(x) for x in v)
        else: self.a=(F(v),F(0),F(0),F(0))
    def __add__(self,v):
        v=E(v); return E(tuple(x+y for x,y in zip(self.a,v.a)))
    __radd__=__add__
    def __neg__(self): return E(tuple(-x for x in self.a))
    def __sub__(self,v): return self+-E(v)
    def __rsub__(self,v): return E(v)+-self
    def __mul__(self,v):
        v=E(v); a=[F(0)]*7
        for i,x in enumerate(self.a):
            if x:
                for j,y in enumerate(v.a):
                    if y:a[i+j]+=x*y
        for k in range(6,3,-1):
            a[k-2]+=a[k];a[k-4]-=a[k]
        return E(a[:4])
    __rmul__=__mul__
    def __truediv__(self,v):
        assert isinstance(v,(int,F))
        return E(tuple(x/v for x in self.a))
    def __eq__(self,v):return self.a==E(v).a
    def __pow__(self,k):
        assert k>=0
        out=E(1);a=self
        while k:
            if k&1:out=out*a
            a=a*a;k//=2
        return out
    def conj(self):return sum((c*ROOTS[(-j)%12] for j,c in enumerate(self.a)),E(0))
    def real(self):return self==self.conj()
    def __bool__(self):return any(self.a)
    def __str__(self):return "["+",".join(map(str,self.a))+"]"
Z=E(0);ONE=E(1);x=E((0,1,0,0));ROOTS=[x**k for k in range(12)]
omega=ROOTS[4];ii=ROOTS[3]
assert x**12==1 and x**6==-1 and omega**3==1 and ii**2==-1

def zero(n):return [[Z for j in range(n)] for i in range(n)]
def eye(n):return [[E(int(i==j)) for j in range(n)] for i in range(n)]
def add(A,B):return [[a+b for a,b in zip(r,s)] for r,s in zip(A,B)]
def sub(A,B):return [[a-b for a,b in zip(r,s)] for r,s in zip(A,B)]
def scale(c,A):return [[c*a for a in r] for r in A]
def mm(A,B):
    n=len(A);C=zero(n)
    for i in range(n):
        for k in range(n):
            if A[i][k]:
                for j in range(n):
                    if B[k][j]:C[i][j]=C[i][j]+A[i][k]*B[k][j]
    return C
def star(A):return [[A[j][i].conj() for j in range(len(A))] for i in range(len(A))]
def diagconj(A,t):
    return [[ROOTS[(4*(t[i]-t[j]))%12]*A[i][j] for j in range(len(A))] for i in range(len(A))]
def cycle(n,H,order=None,phases=None):
    order=list(range(n)) if order is None else order
    phases=[ONE]*(n-1)+[H] if phases is None else phases
    W=zero(n)
    for k,b in enumerate(order):W[order[(k+1)%n]][b]=phases[k]
    return W
def green(W,d):
    n=len(W);A=eye(n);S=zero(n)
    for k in range(n):
        S=add(S,A);A=mm(A,W)
    return scale(d,S)
def constant_diag(A):return all(A[j][j]==A[0][0] for j in range(len(A)))
def offskew(A):return all(A[i][j]==-A[j][i].conj() for i in range(len(A)) for j in range(len(A)) if i!=j)
def assert_green(W,G,H,d):
    n=len(W);I=eye(n)
    assert mm(W,star(W))==I
    assert mm(sub(I,W),G)==I and mm(G,sub(I,W))==I
    assert add(G,star(G))==I
    assert all(G[j][j]==d for j in range(n))
    assert all(G[i][j] for i in range(n) for j in range(n))
    A=I
    for _ in range(n):A=mm(A,W)
    assert A==scale(H,I)

started=time.time()
out={"arithmetic":"exact rational coefficients in Q(zeta_12)",
     "submitted_code_executed":False,"source_tests_replayed":False}
enums=[]
for n in range(2,10):
    count=0;tested=0;witness=[]
    for b in permutations(range(n)):
        tested+=1;c=(b[1]-b[0])%n
        ok=all(((i-j)*(b[i]-b[j])-c)%n==0 for i in range(n) for j in range(i))
        if ok:count+=1;witness.append(list(b))
    assert count==(2 if n==2 else 6 if n==3 else 0)
    enums.append({"N":n,"permutations":tested,"constant_paired_crossratio_count":count,"witnesses":witness})
out["exhaustive_permutations"]=enums

rng=random.Random(20261010);checks=[];allGs={}
for n in range(2,11):
    gs=[]
    for k in range(4):
        h_exp=6 if k%2==0 else 8;H=ROOTS[h_exp]
        d=E(F(1,2)) if h_exp==6 else (1-omega)/3
        exps=[rng.randrange(12) for _ in range(n-1)]
        exps.append((h_exp-sum(exps))%12)
        order=list(range(n));rng.shuffle(order)
        W=cycle(n,H,order,[ROOTS[j] for j in exps]);G=green(W,d)
        assert_green(W,G,H,d);gs.append(G)
        checks.append({"N":n,"holonomy_exponent_mod12":h_exp,"order":order,"edge_exponents_mod12":exps})
    allGs[n]=gs
out["literal_inverse_checks"]=checks
sums=[]
for n,gs in allGs.items():
    for q in (0,1,2,7,17):
        cs=[(k%5)-2 for k in range(q)]
        if q>=2:cs[-1]=-sum(cs[:-1]) # Explicit zero-sum signed case.
        M=zero(n)
        for k,c in enumerate(cs):M=add(M,scale(E(c),gs[k%4]))
        assert constant_diag(M) and offskew(M)
        assert add(M,star(M))==scale(E(sum(cs)),eye(n))
        lam=(1+ii)/3;L=scale(lam,M)
        # Dividing by lam is unnecessary: exact scaled identity verifies it.
        assert add(scale(lam.conj(),L),scale(lam,star(L)))==scale(lam*lam.conj()*sum(cs),eye(n))
        sums.append({"N":n,"q":q,"coefficients":cs})
out["signed_real_sum_checks"]=sums

# Singular holonomy=1 is genuinely excluded, rather than inverted.
for n in range(2,11):
    W=cycle(n,ONE)
    assert all(sum(row,Z)==ONE for row in W)
    assert all(sum(row,Z)==Z for row in sub(eye(n),W))
out["singular_unit_holonomy_kernel_checks"]=list(range(2,11))

# N2 actual one-term boundary witness.
W2=cycle(2,E(-1));G2=green(W2,E(F(1,2)))
F2=[[E(1),E(1)],[E(1),E(-1)]]
X2=[[F2[a][b]*E(1 if b==0 else -1)/2 for b in range(2)] for a in range(2)]
assert G2==X2
out["N2_boundary_witness"]=True

# N3 actual nine-term signed-real boundary witness.
d=(1-omega)/3;W3=cycle(3,omega**2);G3=green(W3,d)
X3=[[d*omega**((a*b-b*b)%3) for b in range(3)] for a in range(3)]
assert constant_diag(X3) and offskew(X3)
nums=[[4,4,1],[1,-2,1],[4,-2,-2]]
S=zero(3)
for u,v in product(range(3),repeat=2):
    t=(0,u,v);Wt=diagconj(W3,t);Gt=diagconj(G3,t)
    assert_green(Wt,Gt,omega**2,d)
    S=add(S,scale(E(F(nums[u][v],9)),Gt))
assert S==X3 and sum(map(sum,nums))==9
out["N3_boundary_witness"]={"passed":True,"coefficient_numerators_over9":nums}

# N4 exact noncollinear countercontrol using the explicit 27-term formula.
n=4;W4=cycle(n,E(-1));G4=green(W4,E(F(1,2)))
X4=[[ii**((a*b-b*b)%4) for b in range(n)] for a in range(n)]
S=zero(n);coeff=[]
for tail in product(range(3),repeat=3):
    t=(0,)+tail;alpha=ONE
    for a in range(n):
        for b in range(n):
            if a!=b:
                sign=1 if a>=b else -1
                alpha+=sign*X4[a][b]*omega**((-(t[a]-t[b]))%3)
    alpha=2*alpha/27
    Wt=diagconj(W4,t);Gt=diagconj(G4,t)
    assert_green(Wt,Gt,E(-1),E(F(1,2)))
    S=add(S,scale(alpha,Gt));coeff.append((t,alpha))
assert S==X4
pair=next((a,b) for a in coeff for b in coeff if not (a[1]*b[1].conj()).real())
assert not offskew(X4)
out["N4_noncollinear_control"]={"passed":True,"q":27,
 "coefficients":[{"t":t,"alpha_in_power_basis":str(a)} for t,a in coeff],
 "noncollinear_pair":[{"t":t,"alpha_in_power_basis":str(a)} for t,a in pair],
 "target":"F4 diag(1,-i,1,-i)"}

# Nonunitary control: dropping unitarity loses the Hermitian part identity.
W=scale(E(2),W2);G=scale(E(F(1,5)),add(eye(2),W)) # W^2=-4I.
assert mm(sub(eye(2),W),G)==eye(2) and add(G,star(G))!=eye(2)
out["nonunitary_identity_negative_control"]=True

out["all_passed"]=True
out["elapsed_seconds"]=round(time.time()-started,3)
p=Path(__file__).with_name("fresh_exact_results.json")
p.write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"all_passed":True,"permutations_tested":sum(a["permutations"] for a in enums),
                 "literal_cycle_cases":len(checks),"signed_sum_cases":len(sums),
                 "N2_N3_boundary_witnesses":True,"N4_noncollinear_control":True,
                 "elapsed_seconds":out["elapsed_seconds"]},indent=2))

