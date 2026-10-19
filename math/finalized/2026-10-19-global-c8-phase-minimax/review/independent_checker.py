#!/usr/bin/env python3
"""Fresh characteristic-zero controls for the independent commutator review.
No author, predecessor, or historical program is imported or executed.
"""
from fractions import Fraction as Fq
from pathlib import Path
import json
import sympy as sp

N=16
ZERO=(Fq(0),)*N
ONE=(Fq(1),)+(Fq(0),)*(N-1)
def scalar(x): return (Fq(x),)+(Fq(0),)*(N-1)
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def neg(a): return tuple(-x for x in a)
def sub(a,b): return add(a,neg(b))
def scale(a,x): return tuple(Fq(x)*y for y in a)
def zp(k):
    k%=32
    a=[Fq(0)]*N
    a[k%16]=Fq(1 if k<16 else -1)
    return tuple(a)
def mul(a,b):
    out=[Fq(0)]*N
    for i,x in enumerate(a):
        if not x: continue
        for j,y in enumerate(b):
            if not y: continue
            k=i+j
            out[k%16]+=x*y*(1 if k<16 else -1)
    return tuple(out)
def cj(a):
    out=ZERO
    for i,x in enumerate(a):
        if x: out=add(out,scale(zp(-i),x))
    return out
def matadd(A,B): return [[add(x,y) for x,y in zip(r,s)] for r,s in zip(A,B)]
def matsub(A,B): return [[sub(x,y) for x,y in zip(r,s)] for r,s in zip(A,B)]
def ms(A,x): return [[mul(t,x) for t in r] for r in A]
def tr(A): return list(map(list,zip(*A)))
def mcj(A): return [[cj(t) for t in r] for r in A]
def star(A): return tr(mcj(A))
def mm(A,B):
    out=[]
    for r in A:
        rr=[]
        for c in zip(*B):
            value=ZERO
            for x,y in zip(r,c): value=add(value,mul(x,y))
            rr.append(value)
        out.append(rr)
    return out
def outer(a,b): return [[mul(x,y) for y in b] for x in a]
def eye(n): return [[ONE if j==k else ZERO for k in range(n)] for j in range(n)]
def diag(a): return [[a[j] if j==k else ZERO for k in range(len(a))] for j in range(len(a))]
def trace(A):
    value=ZERO
    for j in range(len(A)): value=add(value,A[j][j])
    return value
checks=[]
def ck(name,value):
    if not value: raise AssertionError(name)
    checks.append(name)

# Exact Fourier coefficient checks, without numerical exponentials.
z=zp(1); ii=zp(8)
rho=scale(sub(zp(4),zp(12)),Fq(1,4))
FF=[[mul(rho,zp(-4*j*k)) for k in range(8)] for j in range(8)]
I=eye(8)
ck('normalization rho^2=1/8',mul(rho,rho)==scalar(Fq(1,8)))
ck('F symmetric',FF==tr(FF))
ck('F unitary',mm(star(FF),FF)==I)
coefficients=0
for j in range(8):
    for k in range(8):
        for l in range(8):
            ck_name=mul(FF[j][l],FF[l][k])==scale(zp(-4*(j+k)*l),Fq(1,8))
            if not ck_name: raise AssertionError('generic A Fourier Hankel coefficient')
            coefficients+=1
checks.append('all 512 generic A coefficients in F A F are cyclic-Hankel')

# Arbitrary formal Hankel entries and arbitrary nonzero symbolic B entries.
c=sp.symbols('c0:8')
b=sp.symbols('b0:8',nonzero=True)
S=sp.zeros(8)
for j in range(8): S[(j+1)%8,j]=1
C=sp.Matrix(8,8,lambda j,k:c[(j+k)%8])
ck('arbitrary cyclic-Hankel C S = S^T C',C*S==S.T*C)
BB=sp.diag(*b)
Binv=sp.diag(*[1/t for t in b])
T=Binv*S*BB
K=S.T*Binv*S.T*BB
Kdirect=sp.zeros(8)
for j in range(8): Kdirect[(j-2)%8,j]=b[j]/b[(j-1)%8]
ck('all weighted shift entries K e_j=(b_j/b_{j-1})e_{j-2}',K==Kdirect)
x=sp.Symbol('x')
gamma=b[0]*b[2]*b[4]*b[6]/(b[1]*b[3]*b[5]*b[7])
ck('generic characteristic polynomial (x^4-Gamma)(x^4-Gamma^-1)',sp.cancel(K.charpoly(x).as_expr()-(x**4-gamma)*(x**4-1/gamma))==0)
K4=K**4
ck('generic fourth power on parity subspaces',all(sp.cancel(K4[j,k]-(gamma if j%2==0 else 1/gamma))==0 if j==k else K4[j,k]==0 for j in range(8) for k in range(8)))

# Sharp witness, derived afresh in Q[z]/(z^16+1), z=exp(i*pi/16).
q=[zp(k) for k in [0,2,0,10,0,2,0,10]]
p=[mul(z,t) for t in q]
P=diag(p); Q=diag(q)
V=mm(mm(P,FF),Q)
X=ms(matadd(V,mcj(V)),scalar(Fq(1,2)))
Y=ms(matsub(V,mcj(V)),scale(ii,Fq(-1,2)))
s=mul(scale(ii,Fq(-1,2)),sub(z,zp(-1)))
cc=scale(add(z,zp(-1)),Fq(1,2))
a=[scalar(Fq(t,2)) for t in [1,0,-1,0,-1,0,1,0]]
d=[scalar(Fq(t,2)) for t in [0,1,0,1,0,1,0,1]]
R=matadd(outer(a,a),outer(d,d))
L=matsub(I,R)
ck('V unitary',mm(star(V),V)==I)
ck('X,Y real and symmetric',mcj(X)==X and mcj(Y)==Y and tr(X)==X and tr(Y)==Y)
ck('R rank-two projector from orthonormal a,b',mm(R,R)==R and trace(R)==scalar(2) and mm(tr([a,d]),[a,d])==R)
ck('L rank-six projector',mm(L,L)==L and trace(L)==scalar(6))
ck('Y a = c b',mm(Y,[[t] for t in a])==[[mul(cc,t)] for t in d])
ck('Y b = c a',mm(Y,[[t] for t in d])==[[mul(cc,t)] for t in a])
ck('Y^2=s^2 I+(c^2-s^2)R',mm(Y,Y)==matadd(ms(I,mul(s,s)),ms(R,sub(mul(cc,cc),mul(s,s)))))
u=[add(v,mul(ii,w)) for v,w in zip(a,d)]
E=ms(outer(u,u),cc)
Core=matsub(X,ms(matsub(outer(a,a),outer(d,d)),cc))
Residual=matsub(V,matadd(Core,E))
Yres=matsub(Y,ms(matadd(outer(a,d),outer(d,a)),cc))
ck('Core real',mcj(Core)==Core)
ck('legal original residual V-Core-E=iYres',Residual==ms(Yres,ii))
ck('sharp residual Yres^2=s^2 L',mm(Yres,Yres)==ms(L,mul(s,s)))
ck('original outer residual identity',matsub(FF,mm(mm(star(P),matadd(Core,E)),star(Q)))==mm(mm(star(P),Residual),star(Q)))
minors=0
for j in range(8):
    for k in range(j+1,8):
        for l in range(8):
            for m in range(l+1,8):
                if sub(mul(E[j][l],E[k][m]),mul(E[j][m],E[k][l]))!=ZERO: raise AssertionError('rank-one minor')
                minors+=1
ck('all 784 minors vanish and E nonzero',minors==784 and any(t!=ZERO for row in E for t in row))
W=mm(tr(V),V)
ck('witness Y^T Y=(I-Re W)/2',mm(tr(Y),Y)==ms(matsub(I,ms(matadd(W,mcj(W)),scalar(Fq(1,2)))),scalar(Fq(1,2))))
Bphase=diag([mul(t,t) for t in q])
S8=[[ONE if j==(k+1)%8 else ZERO for k in range(8)] for j in range(8)]
Kw=mm(mm(mm(star(S8),star(Bphase)),star(S8)),Bphase)
ck('witness K^4=-I (endpoint necessity)',mm(mm(mm(Kw,Kw),Kw),Kw)==ms(I,scalar(-1)))
M=mm(mm(mm(FF,diag([mul(t,t) for t in p])),FF),Bphase)
Tw=mm(mm(star(Bphase),S8),Bphase)
ck('witness M T M*=S*',mm(mm(M,Tw),star(M))==star(S8))
ck('witness K=M T M* T*',mm(mm(mm(M,Tw),star(M)),star(Tw))==Kw)

# Exact spectral multiplicities, using Lagrange projectors rather than rank elimination.
w=sp.Symbol('w')
def inva(t):
    poly=sum(sp.Rational(a.numerator,a.denominator)*w**j for j,a in enumerate(t))
    pp=sp.Poly(sp.invert(poly,w**16+1),w)
    out=tuple(Fq(pp.nth(j)) for j in range(16))
    if mul(t,out)!=ONE: raise AssertionError('field inverse')
    return out
mspectrum=[(2,4),(-2,2),(14,2)]
projs=[]
for exp,multiplicity in mspectrum:
    eig=zp(exp)
    project=I
    denom=ONE
    for other,_ in mspectrum:
        if other==exp: continue
        project=mm(project,matsub(M,ms(I,zp(other))))
        denom=mul(denom,sub(eig,zp(other)))
    project=ms(project,inva(denom))
    ck('M spectral projector z^'+str(exp)+' rank '+str(multiplicity),mm(project,project)==project and trace(project)==scalar(multiplicity) and mm(matsub(M,ms(I,eig)),project)==ms(I,ZERO))
    projs.append(project)
ck('M spectral projectors sum to I',matadd(matadd(projs[0],projs[1]),projs[2])==I)
kspectrum=[(4,2),(-4,2),(12,2),(-12,2)]
kprojs=[]
for exp,multiplicity in kspectrum:
    eig=zp(exp)
    project=I
    denom=ONE
    for other,_ in kspectrum:
        if other==exp: continue
        project=mm(project,matsub(Kw,ms(I,zp(other))))
        denom=mul(denom,sub(eig,zp(other)))
    project=ms(project,inva(denom))
    ck('K spectral projector z^'+str(exp)+' rank '+str(multiplicity),mm(project,project)==project and trace(project)==scalar(multiplicity) and mm(matsub(Kw,ms(I,eig)),project)==ms(I,ZERO))
    kprojs.append(project)
ck('K spectral projectors sum to I',matadd(matadd(kprojs[0],kprojs[1]),matadd(kprojs[2],kprojs[3]))==I)
u,v=sp.symbols('u v')
ck('scalar centering squared gap identity',sp.expand((1-u*u)-(1+u*u-2*u*v)-2*u*(v-u))==0)

# Mutation controls: each deliberately incorrect identity must fail.
controls={
    'wrong shift direction C S = S C rejected': C*S != S*C,
    'wrong one-step K=S^T B^-1 S B rejected': K != S.T*Binv*S*BB,
    'wrong squared witness correction rejected': mm(Yres,Yres) != ms(I,mul(s,s)),
    'wrong rank-one correction sign rejected': matsub(V,matadd(Core,ms(E,scalar(-1)))) != ms(Yres,ii),
    'closed original arc at most five rejected by six endpoint eigenvalues': sum(d for e,d in mspectrum if abs(e)<=2)==6,
    'closed K arc at most two rejected by four endpoint eigenvalues': sum(d for e,d in kspectrum if abs(e)<=4)==4,
}
ck('all six mutation controls rejected',all(controls.values()))
result={'status':'PASS','arithmetic':'Characteristic zero: rational cyclotomic field Q[z]/(z^16+1) and symbolic rational functions. No floating-point evaluations.','checks':checks,'generic_fourier_coefficients':coefficients,'rank_one_minors':minors,'witness_M_spectrum':mspectrum,'witness_K_spectrum':kspectrum,'mutation_controls':controls,'limits':'These finite identities support, but do not replace, the independent universal analytic proof. No historical or author code was executed.'}
path=Path(__file__).parent/'INDEPENDENT_RESULTS.json'
path.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
