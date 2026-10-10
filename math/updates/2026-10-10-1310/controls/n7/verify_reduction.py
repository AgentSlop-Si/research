#!/usr/bin/env python3
"""Independent exact controls for the N=7 six-bank edge reduction.
Only reads frozen JSON literals; never imports or executes research-source code.
Requires Python 3 and SymPy. Run from any directory.
"""
from pathlib import Path
import hashlib
import json
import sympy as sp
from sympy.polys.rings import ring

HERE=Path(__file__).resolve().parent
q0=sp.Symbol('q')
K=sp.QQ.alg_field_from_poly(sp.Poly(sp.cyclotomic_poly(7,q0),q0),alias='q')
q=K.unit
O,Z=K.one,K.zero
A,y=ring('y',K)
checks={}

def coeffs(c):
    out=list(reversed(c.to_list()))
    return [str(v) for v in out]+['0']*(6-len(out))

def polynomial(p):
    return [coeffs(p.get((i,),Z)) for i in range(p.degree()+1)]

def decode(data):
    return sum((sum((K.convert(sp.Rational(v))*q**j for j,v in enumerate(c)),Z)*y**i for i,c in enumerate(data)),A.zero)

def gcdex_poly(a,b):
    # Self-contained extended Euclidean algorithm over exact polynomial ring K[y].
    r0,r1=a,b; s0,s1=A.one,A.zero; t0,t1=A.zero,A.one
    while r1:
        quot,rem=divmod(r0,r1)
        r0,r1=r1,rem; s0,s1=s1,s0-quot*s1; t0,t1=t1,t0-quot*t1
    unit=O/r0.LC
    r0,s0,t0=r0*unit,s0*unit,t0*unit
    assert s0*a+t0*b==r0
    return r0,s0,t0

# Gaussian coefficients are constructed from their finite product definition.
def gaussian(n,k,z):
    if k<0 or k>n: return Z
    v=O
    for j in range(1,k+1):
        v*= (O-z**(n-k+j))/(O-z**j)
    return v

# Independently derive normalized Fourier Weyl coefficients from the trace formula.
# c(a,b)=1/7 sum_t q^(-b*t-(t+a)*t).
C=sum((q**((-t*t)%7) for t in range(7)),Z)/K.convert(7)
assert C
for a in range(7):
    for b in range(7):
        direct=sum((q**((-b*t-(t+a)*t)%7) for t in range(7)),Z)/K.convert(7)
        assert direct==C*q**((2*(a+b)**2)%7)
checks['all_49_trace_coefficients']=True

# b=1, a=6 fixes singleton amplitude h_y=H/y. Divide remaining equations
# by H*[a+1 choose 1]_q and put m_(a-1)=sum h_i*x_i^a/H.
H=q/(O+q)
assert H==O/(O+q**-1)
m=[]
for a in range(1,6):
    f=q**((2*(a+1)**2)%7)
    forward=gaussian(a+1,1,q)
    backward=gaussian(8-a,1,q**-1)
    m.append((A(f/H)-backward*y**(6-a))/forward)
assert m[0]==A.one
D=m[2]-m[1]**2
Sn=m[3]-m[1]*m[2]
Pn=m[1]*m[3]-m[2]**2
R=D*m[4]-Sn*m[3]+Pn*m[2]
Disc=Sn**2-4*Pn*D
assert R.degree()==9
assert D.degree()==8 and Sn.degree()==7 and Pn.degree()==6
assert Disc.degree()==14
# Cramer's equations and the third Hankel condition, without any rational division.
assert D*m[2]==Sn*m[1]-Pn
assert D*m[3]==Sn*m[2]-Pn*m[1]
assert D*m[4]-Sn*m[3]+Pn*m[2]==R
checks['edge_moments_derived_from_gaussians']=True
checks['moment_recurrence_cramer_identities']=True
checks['R_degree_9']=True

raw={
 'm':[polynomial(p) for p in m], 'D':polynomial(D),
 'S_numerator':polynomial(Sn), 'P_numerator':polynomial(Pn),
 'R':polynomial(R),'discriminant_numerator':polynomial(Disc),'C':coeffs(C),
}
# Compare independently computed constants to source literals, if frozen source present.
source=HERE/'sources'/'EDGE_MOMENT_CERTIFICATE.json'
if source.exists():
    lit=json.loads(source.read_text())
    for key in ('D','S_numerator','P_numerator','R','discriminant_numerator'):
        assert decode(lit[key])==decode(raw[key]),key
    for actual,stated in zip(m,lit['m']): assert actual==decode(stated)
    assert lit['C']==raw['C']
    checks['all_frozen_literal_coefficients_match']=True
    source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
else:
    source_hash=None

guards={'y':y,'D':D,'P_numerator':Pn,'discriminant_numerator':Disc,
        'R_derivative':R.diff(y)}
bezout={}
for name,g in guards.items():
    d,u,v=gcdex_poly(R,g)
    assert d==A.one,name
    bezout[name]={'gcd':'1','R_multiplier':polynomial(u),'guard_multiplier':polynomial(v)}
checks['all_guard_gcds_are_one']=True
checks['R_squarefree']=True

# The row coefficient formula is also checked as a POLYNOMIAL identity directly
# against literal 7x7 matrices for all four signed orientations.
B,al,be=ring('alpha,beta',K)
zero=B.zero; one=B.one

def identity(): return [[one if i==j else zero for j in range(7)] for i in range(7)]
def mul(M,N):
    return [[sum((M[i][k]*N[k][j] for k in range(7)),zero) for j in range(7)] for i in range(7)]
for eps,delta in ((1,1),(-1,1),(1,-1),(-1,-1)):
    X=[[zero for j in range(7)] for i in range(7)]
    for j in range(7):
        X[(j+eps)%7][j]+=al
        X[j][j]+=be*q**((delta*j)%7)
    power=identity(); total=[[zero for j in range(7)] for i in range(7)]
    for n in range(7):
        expected=[[zero for j in range(7)] for i in range(7)]
        for ell in range(n+1):
            r=n-ell
            amp=gaussian(n,ell,q**(eps*delta))*al**r*be**ell
            for j in range(7): expected[(j+eps*r)%7][j]+=amp*q**((delta*ell*j)%7)
        assert power==expected,(eps,delta,n)
        for i in range(7):
            for j in range(7): total[i][j]+=power[i][j]
        power=mul(power,X)
    expected7=[[(al**7+be**7) if i==j else zero for j in range(7)] for i in range(7)]
    assert power==expected7,(eps,delta,'X^7')
    Q=[[(one if i==j else zero)-X[i][j] for j in range(7)] for i in range(7)]
    guard=[[(one-al**7-be**7) if i==j else zero for j in range(7)] for i in range(7)]
    assert mul(Q,total)==guard and mul(total,Q)==guard
checks['signed_gaussian_literal_matrix_identities']=True
checks['original_resolvent_polynomial_identity_all_orientations']=True

# Sector separation and branch-weight synthesis are an exact 7-point identity.
for eps,delta in ((1,1),(-1,1),(1,-1),(-1,-1)):
    for ell in range(7):
        for r in range(7):
            val=sum((q**((eps*delta*j*(r-ell))%7) for j in range(7)),Z)/K.convert(7)
            assert val==(O if r==ell else Z)
checks['branch_phase_synthesis_all_orientations']=True

# Transposition preserves the Fourier matrix and flips epsilon; the phase index
# is reindexed j -> -j, with delta, alpha, beta, and guard unchanged.
for eps,delta in ((1,1),(-1,1),(1,-1),(-1,-1)):
    for j in range(7):
        original=[[zero for v in range(7)] for u in range(7)]
        transformed=[[zero for v in range(7)] for u in range(7)]
        for v in range(7):
            original[(v+eps)%7][v]+=al
            original[v][v]+=be*q**((eps*delta*j+delta*v)%7)
            transformed[(v-eps)%7][v]+=al
            transformed[v][v]+=be*q**(((-eps)*delta*((-j)%7)+delta*v)%7)
        assert [list(row) for row in zip(*original)]==transformed
checks['literal_transpose_symmetry_all_28_branches']=True

# Simultaneous reflection identifies the opposite edge target and all column coefficients.
for a in range(7):
    for b in range(7):
        assert q**((2*(a+b)**2)%7)==q**((2*((-a)%7+(-b)%7)**2)%7)
checks['opposite_edge_reflection']=True

report={
 'status':'PASS: exact edge reduction and legality/sufficiency identities only',
 'field':'Q[q]/(1+q+q^2+q^3+q^4+q^5+q^6), characteristic zero',
 'source_certificate_sha256':source_hash,
 'checks':checks,
 'degrees':{'D':D.degree(),'S_numerator':Sn.degree(),'P_numerator':Pn.degree(),
            'R':R.degree(),'discriminant_numerator':Disc.degree()},
 'gcds':{key:'1' for key in guards},
 'edge_root_count_over_algebraic_closure':9,
 'six_bank_attainment_established':False,
 'remaining_rows_scope':'This edge-only control does not test remaining rows. The independent companion axis-norm control proves the b=0 condition impossible for this mirrored pattern.',
 'independence':'No author/predecessor research code executed, imported, compiled, or parsed. SymPy is used solely for exact algebraic-field and polynomial arithmetic.',
}
(HERE/'INDEPENDENT_EDGE_COEFFICIENTS.json').write_text(json.dumps(raw,indent=2)+'\n')
(HERE/'GUARD_BEZOUT_CERTIFICATES.json').write_text(json.dumps(bezout,indent=2)+'\n')
(HERE/'EXACT_CONTROL_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
