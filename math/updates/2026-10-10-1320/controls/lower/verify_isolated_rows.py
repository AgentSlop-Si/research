#!/usr/bin/env python3
"""Fresh exact independent control; no external research modules are imported."""
import json, hashlib, itertools, time
from pathlib import Path
import sympy as sp
from sympy.polys.rings import ring
BASE=Path(__file__).resolve().parent
K=sp.QQ.algebraic_field(sp.exp(2*sp.pi*sp.I/7))
q=K.unit
zero,one=K.zero,K.one
P,y=ring('y',K)

def qbinom(n,k,t):
    if k<0 or k>n: return zero
    if k==0 or k==n: return one
    # Polynomial recurrence, requiring no divisions or root-of-unity convention.
    vals=[one]+[zero]*k
    for n0 in range(1,n+1):
        old=vals[:]
        for j in range(1,min(n0,k)+1):
            vals[j]=old[j]+t**(n0-j)*old[j-1]
    return vals[k]

def rowcoef(a,b,eps,delta):
    r=(eps*a)%7; ell=(delta*b)%7
    return (r,qbinom(r+ell,ell,q**(eps*delta))) if r+ell<=6 else (r,zero)

def f(a,b): return q**((2*(a+b)**2)%7)
def vec(c):
    arr=list(reversed(c.to_list()))
    return [str(arr[j]) if j<len(arr) else '0' for j in range(6)]
def poly(f0): return [vec(f0.get((j,),zero)) for j in range(f0.degree()+1)]
def modc(c,p=29,z=7):
    v=0
    for a in c.to_list():
        a=sp.Rational(str(a))
        v=(v*z+int(a.p)*pow(int(a.q),-1,p))%p
    return v

def modpoly(f0,p=29,z=7):
    return [modc(f0.get((j,),zero),p,z) for j in range(f0.degree()+1)]

# Full Fourier normalization, derived from trace on matrix units.
C=sum((q**((-t*t)%7) for t in range(7)),zero)/7
assert C!=zero
trace_checks=0
for a,b in itertools.product(range(7),repeat=2):
    actual=sum((q**((-b*t-(t+a)*t)%7) for t in range(7)),zero)/7
    assert actual==C*f(a,b)
    trace_checks+=1

# All opposite-sign support is inspected directly for both isolated rows.
for b,aa in [(1,range(1,7)),(2,range(2,6))]:
    for a,eps in itertools.product(aa,[-1,1]):
        assert rowcoef(a,b,eps,-1)[1]==zero

# Singleton endpoint on the first row determines H/y, with y necessarily nonzero.
r6,c6=rowcoef(6,1,-1,1)
assert r6==1 and c6!=zero
H=f(6,1)/c6
assert H==q/(one+q)
assert rowcoef(6,1,1,1)[1]==zero
assert f(1,1)==H*rowcoef(1,1,1,1)[1]
m=[P.one]
scalar_denominators=[c6]
for a in range(2,6):
    rf,cf=rowcoef(a,1,1,1)
    rr,cr=rowcoef(a,1,-1,1)
    assert rf==a and rr==7-a and cf!=zero
    scalar_denominators.extend([H,cf])
    m.append(f(a,1)/(H*cf)-(cr/cf)*y**(rr-1))
D=m[2]-m[1]**2
Sn=m[3]-m[1]*m[2]
Pn=m[1]*m[3]-m[2]**2
R=D*m[4]-Sn*m[3]+Pn*m[2]
assert R.degree()==9
assert D*m[2]==Sn*m[1]-Pn
assert D*m[3]==Sn*m[2]-Pn*m[1]

# Second row's singleton is independently isolated at a=5.
r5,c5=rowcoef(5,2,-1,1)
assert r5==2 and c5!=zero and f(5,2)==one
assert rowcoef(5,2,1,1)[1]==zero
n={}
scalar_denominators.append(c5)
for a in (2,3,4):
    rf,cf=rowcoef(a,2,1,1)
    rr,cr=rowcoef(a,2,-1,1)
    assert rf==a and cf!=zero
    scalar_denominators.append(cf)
    n[a]=P.ground_new(f(a,2)/cf)-y**(rr-2)*P.ground_new(cr/(c5*cf))
F=D*n[4]-Sn*n[3]+Pn*n[2]
assert F.degree()==9

# Exact verification of universal two-atom identities, including coincident/zero nodes.
x,z,A,B=sp.symbols('x z A B')
mm=[A*x**j+B*z**j for j in range(5)]
d0=mm[0]*mm[2]-mm[1]**2
s0=mm[0]*mm[3]-mm[1]*mm[2]
p0=mm[1]*mm[3]-mm[2]**2
assert sp.expand(s0-(x+z)*d0)==0
assert sp.expand(p0-x*z*d0)==0
assert sp.expand(sp.det(sp.Matrix([[mm[i+j] for j in range(3)] for i in range(3)])))==0
c,d=sp.symbols('c d')
nn={j:c*x**j+d*z**j for j in (2,3,4)}
assert sp.expand(nn[4]-(x+z)*nn[3]+x*z*nn[2])==0

# Exact Q(q)[y] Bezout. This is stronger than the good-reduction control below.
t0=time.monotonic()
print('Computing exact Bezout over Q(q)...',flush=True)
u,v,g=R.gcdex(F)
assert g==P.one and u*R+v*F==P.one
print('Exact Bezout verified.',flush=True)

# Prime reduction with exact coefficient/denominator checks.
p=29; qbar=7
assert sp.isprime(p) and pow(qbar,7,p)==1 and qbar!=1
assert sum(pow(qbar,k,p) for k in range(7))%p==0
assert all(modc(c)!=0 for c in scalar_denominators)
Rbar=modpoly(R); Fbar=modpoly(F)
assert Rbar[-1]!=0 and Fbar[-1]!=0
Fp,t=ring('t',sp.GF(p))
rbar=sum((Fp.ground_new(a)*t**i for i,a in enumerate(Rbar)),Fp.zero)
fbar=sum((Fp.ground_new(a)*t**i for i,a in enumerate(Fbar)),Fp.zero)
ub,vb,gb=rbar.gcdex(fbar)
assert gb==Fp.one and ub*rbar+vb*fbar==Fp.one
res=rbar.resultant(fbar)
assert res!=0

def modlist(p0): return [int(p0.get((i,),Fp.domain.zero))%p for i in range(p0.degree()+1)]
# Independently form the 18x18 Sylvester matrix and eliminate modulo 29.
# Columns encode t^i R and t^i F, i=0,...,8; row powers ascend.
mat=[[0]*18 for _ in range(18)]
for j in range(9):
    for k,c0 in enumerate(Rbar): mat[k+j][j]=c0
    for k,c0 in enumerate(Fbar): mat[k+j][9+j]=c0
work=[row[:] for row in mat]; det=1
for i in range(18):
    pivot=next(j for j in range(i,18) if work[j][i]%p)
    if pivot!=i: work[i],work[pivot]=work[pivot],work[i]; det=-det
    piv=work[i][i]%p; det=det*piv%p; inv=pow(piv,-1,p)
    for j in range(i+1,18):
        fac=work[j][i]*inv%p
        for k in range(i,18): work[j][k]=(work[j][k]-fac*work[i][k])%p
assert det%p!=0
# Odd degree 9 introduces a sign in this ascending convention.
assert det%p==(-int(res))%p

result={
 'scope':'Independent exact obstruction to precisely three banks with a fixed delta sign, any number with the other sign, in characteristic zero.',
 'field':'Q(q), Phi_7(q)=0; q primitive',
 'fourier_trace_checks':trace_checks,
 'row_support_checks':'Opposite delta vanishes for b=1,a=1..6 and b=2,a=2..5.',
 'moments': [poly(e) for e in m], 'D':poly(D),'Sn':poly(Sn),'Pn':poly(Pn),'R':poly(R),
 'n2':poly(n[2]),'n3':poly(n[3]),'n4':poly(n[4]),'F':poly(F),
 'degrees':{name:e.degree() for name,e in [('D',D),('Sn',Sn),('Pn',Pn),('R',R),('F',F)]},
 'exact_bezout':{'U':poly(u),'V':poly(v),'identity':'U*R+V*F=1, verified exactly in Q(q)[y]'},
 'mod29':{'q':7,'R_ascending':Rbar,'F_ascending':Fbar,'R_leading':Rbar[-1],'F_leading':Fbar[-1],
           'scalar_denominator_residues':[modc(c) for c in scalar_denominators],
           'U_ascending':modlist(ub),'V_ascending':modlist(vb),'gcd':1,
           'resultant':int(res)%p,'sylvester_ascending_det':det%p,'sylvester_ascending_matrix':mat},
 'degeneracy_coverage':'No division by D, Pn, x, z, x-z, any amplitude, or a discriminant. Singleton y is forced nonzero by its b=1 endpoint.',
 'independence':'Fresh file; no authored/predecessor research script executed, imported, compiled, or parsed.'
}
(BASE/'EXACT_ROW_CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'degrees':result['degrees'],'Rmod29':Rbar,'Fmod29':Fbar,'resultant_mod29':int(res)%p,'sylvester_det':det%p,'exact_bezout':True,'scalar_denominators_nonzero_mod29':True},indent=2),flush=True)
