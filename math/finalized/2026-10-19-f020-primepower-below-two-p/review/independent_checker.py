#!/usr/bin/env python3
"""Fresh independent exact transcription controls; finite checks are not the theorem proof."""
import json, math, pathlib
from fractions import Fraction
ROOT = pathlib.Path(__file__).resolve().parent
RESULTS=[]
def record(name, condition, detail=None):
    assert condition, (name, detail)
    RESULTS.append({'name':name,'passed':True,'detail':detail})
def add(a,b):
    c=dict(a)
    for m,v in b.items():
        c[m]=c.get(m,0)+v
        if not c[m]:del c[m]
    return c
def shift(a,dx=0,dt=0,mul=1):
    return {(x+dx,t+dt):v*mul for (x,t),v in a.items()}
def make_P(nmax):
    P=[{(0,0):1},{(1,0):1}]
    for k in range(1,nmax):
        out=shift(P[-1],dx=1)
        for j in range(1,k+1):out=add(out,shift(P[-2],dt=j,mul=math.comb(k,j)))
        P.append(out)
    return P
def reduced(P,p):return {m:c%p for m,c in P.items() if c%p}
def minval(P,scale,p):
    return min(t+scale*x for (x,t),c in reduced(P,p).items())
def initial(P,scale,p):
    d=reduced(P,p); m=min(t+scale*x for x,t in d)
    ans={x:c for (x,t),c in d.items() if t+scale*x==m}
    return m,ans
def hermite(n,p):
    H=[{0:1},{1:1}]
    for k in range(1,n):
        out={j+1:c for j,c in H[-1].items()}
        for j,c in H[-2].items():out[j]=(out.get(j,0)+k*c)%p
        H.append({j:c for j,c in out.items() if c%p})
    return H[n]
def times(A,B,p):
    C={}
    for i,c in A.items():
        for j,d in B.items():C[i+j]=(C.get(i+j,0)+c*d)%p
    return {j:c for j,c in C.items() if c}
def polyrem(A,B,p):
    A=dict(A)
    while A and max(A)>=max(B):
        k=max(A)-max(B); c=A[max(A)]*pow(B[max(B)],-1,p)%p
        for j,d in B.items():
            A[j+k]=(A.get(j+k,0)-c*d)%p
            if not A[j+k]:del A[j+k]
    return A
def squarefree(A,p):
    B={j-1:j*c%p for j,c in A.items() if j and j*c%p}
    while B:A,B=B,polyrem(A,B,p)
    return bool(A) and max(A)==0
P=make_P(26)
for p in [3,5,7,11,13]:
    c=(-1)**((p+1)//2)%p
    val,ini=initial(P[p],1,p)
    record(f'p={p}: middle p-block initial',val==p and ini=={p:1,1:c},{'valuation':val,'initial':ini})
    record(f'p={p}: middle residual separable',squarefree(ini,p))
    for b in range(p):
        h=hermite(b,p)
        record(f'p={p},b={b}: Hermite residual squarefree',squarefree(h,p))
    for r in range(p):
        b=p+r
        val,ini=initial(P[b],0.5,p)
        H=hermite(r,p)
        expect={j+p:c for j,c in H.items()}
        record(f'p={p},r={r}: outer initial',val==b/2 and ini==expect,{'valuation':val})
        if r%2==0:
            val,ini=initial(P[b],1,p)
            const=H[0]
            exp={p:const,1:const*c%p}
            record(f'p={p},r={r}: even-r middle initial',val==p+r/2 and ini==exp,{'valuation':val,'initial':ini})
            record(f'p={p},r={r}: even-r middle separable',squarefree(ini,p))
        elif p>3:
            val,ini=initial(P[b],1,p)
            a=H[1]
            exp={p+1:a,2:a*c%p}
            record(f'p={p},r={r}: odd-r middle initial',val==p+(r+1)/2 and ini==exp,{'valuation':val,'initial':ini})
            inner_scale=(p+1)/4
            val,ini=initial(P[b],inner_scale,p)
            record(f'p={p},r={r}: final quadratic',val==(3*p+r-2)/2 and set(ini)=={0,2} and squarefree(ini,p),{'valuation':val,'scale':inner_scale,'initial':ini})
        else:
            val,ini=initial(P[b],1,p)
            record('p=3,r=1: coalesced quartic scale',val==4 and ini=={4:1,2:1,0:1},{'initial':ini,'separable_mod_3':squarefree(ini,p)})
            record('p=3,r=1: quartic mod-3 scale is NOT separable',not squarefree(ini,p))
# Verify the b=2p residual using exact rational weights and integer recurrence coefficients.
for p in [3,5,7,11,13]:
    alpha=Fraction(2*p-1,2*p)
    val,ini=initial(P[2*p],alpha,p)
    record(f'p={p}: b=2p boundary',val==2*p-1 and ini=={2*p:1,0:p-1},{'valuation':str(val),'scale':str(alpha),'initial':ini})
    record(f'p={p}: b=2p residual inseparable',not squarefree(ini,p))
# Independently reconstruct shifted continuants and the joining-edge determinant identity.
def mul(A,B):
    C={}
    for (x,t),a in A.items():
        for (y,u),b in B.items():
            C[(x+y,t+u)]=C.get((x+y,t+u),0)+a*b
    return {m:c for m,c in C.items() if c}
def cont(size,start_edge):
    if size==0:return {(0,0):1}
    A={(0,0):1};B={(1,0):1}
    for k in range(start_edge,start_edge+size-1):
        C=shift(B,dx=1)
        for j in range(1,k+1):C=add(C,shift(A,dt=j,mul=math.comb(k,j)))
        A,B=B,C
    return B
for p in [3,5,7]:
    for r in range(1,p+1):
        F=cont(r,p+1);G=cont(r-1,p+2)
        join=mul(G,P[p-1]);left=mul(F,P[p])
        for j in range(1,p+1):left=add(left,shift(join,dt=j,mul=math.comb(p,j)))
        record(f'p={p},r={r}: exact block continuant',left==P[p+r])
# Exact coefficient identity P_4 and the q-Hermite transform are checked separately via SymPy.
import sympy as S
x,z,v,q=S.symbols('x z v q')
qP=[S.Integer(1),x]
for k in range(1,12):qP.append(S.expand(x*qP[-1]-(1-q**k)*qP[-2]))
H=[S.Integer(1),1+z]
for k in range(1,12):H.append(S.expand((1+z)*H[-1]-z*(1-q**k)*H[-2]))
for b in range(13):
    diff=S.expand(H[b].subs(z,v**2)-v**b*qP[b].subs(x,v+1/v))
    record(f'b={b}: original Rogers-Szego transform',diff==0)
A=(1-q)*(q*q+2*q+3); B=(1-q)**2*(q*q+q+1)
record('exact P4 formula',S.expand(qP[4]-(x**4-A*x*x+B))==0)
record('P4 quadratic discriminant factor',S.expand(A*A-4*B-(1-q)**2*(q**4+4*q**3+6*q*q+8*q+5))==0)
# P4 at odd prime powers p=3 is inherited; independently check all primitive 9th roots in exact Q(q).
Phi=S.cyclotomic_poly(9,q)
record('P4 constant nonzero at order 9',S.rem(B,Phi,q)!=0)
record('P4 quadratic discriminant nonzero at order 9',S.rem(A*A-4*B,Phi,q)!=0)
(ROOT/'INDEPENDENT_CHECKS.json').write_text(json.dumps({'purpose':'Transcription controls only; no finite census is used to prove the universal theorem.','checks':RESULTS,'passed':len(RESULTS)},indent=2)+'\n')
print(f'{len(RESULTS)} independent exact checks passed.')
