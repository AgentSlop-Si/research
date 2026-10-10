#!/usr/bin/env python3
"""Independent good-reduction certificate for the mirrored N=7 six-bank pattern.
Derives all edge moments at p=29,q=7 directly, and expands the row-zero
augmented determinant by complementary 3x3 minors. Does not import or execute
any author's program or the companion verifier.
"""
from pathlib import Path
import hashlib
import itertools
import json
import sympy as sp
from sympy.polys.rings import ring
HERE=Path(__file__).resolve().parent
p,q=29,7
F=sp.GF(p); B,t=ring('t',F)
assert pow(q,7,p)==1 and all(pow(q,i,p)!=1 for i in range(1,7))
assert sum(pow(q,i,p) for i in range(7))%p==0

def inv(x): return pow(x%p,-1,p)
def gauss(n,k,z):
    r=1
    for j in range(1,k+1): r=r*(1-pow(z,n-k+j,p))*inv(1-pow(z,j,p))%p
    return r
H=q*inv(1+q)%p
m=[]
for a in range(1,6):
    g=gauss(a+1,1,q)
    h=gauss(8-a,1,inv(q))
    m.append((B(pow(q,2*(a+1)**2,p)*inv(H))-h*t**(6-a))*inv(g))
assert m[0]==B.one
D=m[2]-m[1]**2; Sn=m[3]-m[1]*m[2]; Pn=m[1]*m[3]-m[2]**2
R=D*m[4]-Sn*m[3]+Pn*m[2]
leading=int(R.LC)%p
R=R*inv(leading)
assert R.degree()==9

def egcd(a,b):
    r0,r1=a,b; s0,s1=B.one,B.zero; v0,v1=B.zero,B.one
    while r1:
        c,r=divmod(r0,r1)
        r0,r1=r1,r; s0,s1=s1,s0-c*s1; v0,v1=v1,v0-c*v1
    z=inv(int(r0.LC)); r0,s0,v0=r0*z,s0*z,v0*z
    assert s0*a+v0*b==r0
    return r0,s0,v0

gcds={}; inverses={}
for name,G in {'t':t,'D':D,'P_numerator':Pn,'discriminant_numerator':Sn**2-4*Pn*D,'R_derivative':R.diff(t)}.items():
    g,a,b=egcd(R,G)
    gcds[name]=g.degree()
    assert g==B.one,name
    inverses[name]=b%R
Dinv=inverses['D']; S=Sn*Dinv%R; P=Pn*Dinv%R
U=[B.one,B.zero]; V=[B.zero,B.one]
for a in range(2,7):
    U.append((S*U[-1]-P*U[-2])%R)
    V.append((S*V[-1]-P*V[-2])%R)
Y=[[U[a],V[a],t**((-a)%7)] for a in range(7)]
W=[[t**a,U[(-a)%7],V[(-a)%7]] for a in range(7)]

def sign(perm): return -1 if sum(perm[i]>perm[j] for i in range(len(perm)) for j in range(i+1,len(perm)))%2 else 1
perms3=[(perm,sign(perm)) for perm in itertools.permutations(range(3))]
def det3(rows):
    ans=B.zero
    for perm,s in perms3:
        v=B(s)
        for i in range(3): v=v*rows[i][perm[i]]%R
        ans+=v
    return ans%R

def array(f,n=9): return [int(f.get((i,),F.zero))%p for i in range(n)]
# Laplace expand in the disjoint column groups {0,1,2}, {3,4,5}, {6}.
A=[[0]*9 for _ in range(9)]
for last in range(7):
    other=[i for i in range(7) if i!=last]
    for I in itertools.combinations(other,3):
        J=tuple(i for i in other if i not in I)
        sy=det3([Y[i] for i in I]); sv=det3([W[i] for i in J])
        factor=sign(list(I)+list(J)+[last])*pow(q,2*last*last,p)
        cy,cv=array(sy),array(sv)
        for i in range(9):
            for j in range(9): A[i][j]=(A[i][j]+factor*cy[i]*cv[j])%p

monomials=[array(t**k%R) for k in range(17)]
# Basis index 9*i+j means y^i v^j. Column j is A times basis element j.
M=[[0]*81 for _ in range(81)]
for i0 in range(9):
    for j0 in range(9):
        col=9*i0+j0
        for i in range(9):
            for j in range(9):
                c=A[i][j]
                if not c: continue
                yi=monomials[i+i0]; vj=monomials[j+j0]
                for a,ca in enumerate(yi):
                    if not ca: continue
                    for b,cb in enumerate(vj):
                        if cb: M[9*a+b][col]=(M[9*a+b][col]+c*ca*cb)%p

def determinant(M):
    M=[row[:] for row in M]; d=1
    for c in range(len(M)):
        pivot=next((r for r in range(c,len(M)) if M[r][c]),None)
        if pivot is None: return 0
        if pivot!=c: M[c],M[pivot]=M[pivot],M[c]; d=-d
        v=M[c][c]; d=d*v%p; iv=inv(v)
        for r in range(c+1,len(M)):
            if not M[r][c]: continue
            factor=M[r][c]*iv%p
            for k in range(c,len(M)): M[r][k]=(M[r][k]-factor*M[c][k])%p
    return d%p
norm=determinant(M)
assert norm==14,norm
# Solve M*x=e0, giving an explicit inverse as independently verifiable certificate.
aug=[row[:]+[int(i==0)] for i,row in enumerate(M)]
for c in range(81):
    r=next(r for r in range(c,81) if aug[r][c])
    aug[c],aug[r]=aug[r],aug[c]
    z=inv(aug[c][c]); aug[c]=[(v*z)%p for v in aug[c]]
    for r in range(81):
        if r==c or not aug[r][c]: continue
        f=aug[r][c]; aug[r]=[(a-f*b)%p for a,b in zip(aug[r],aug[c])]
ainv=[row[-1] for row in aug]
assert all(sum(M[i][j]*ainv[j] for j in range(81))%p==int(i==0) for i in range(81))

source=HERE/'sources'/'AXIS_QUOTIENT_CERTIFICATE.json'
comparison=None
if source.exists():
    lit=json.loads(source.read_text())
    assert lit['R_mod_p']==array(R,10)
    flat=sum(A,[]); transpose=[A[i][j] for j in range(9) for i in range(9)]
    assert lit['axis_element'] in (flat,transpose)
    assert lit['axis_norm_mod_p']==norm
    comparison={'all_coefficients_match':True,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
                'source_order':'y-major' if lit['axis_element']==flat else 'v-major'}
matrix_source=HERE/'sources'/'AXIS_MULTIPLICATION_MATRIX.json'
matrix_comparison=None
if matrix_source.exists():
    lit=json.loads(matrix_source.read_text())
    assert lit['matrix']==M
    assert lit['R_leading_mod_p']==leading
    assert lit['R_monic_mod_p']==array(R,10)
    assert lit['D_mod_p']==array(D,D.degree()+1)
    assert lit['D_inverse_mod_R']==array(Dinv)
    assert lit['determinant_mod_p']==norm
    matrix_comparison={'all_6561_matrix_entries_match':True,
                       'source_sha256':hashlib.sha256(matrix_source.read_bytes()).hexdigest()}

result={
 'status':'PASS: mirrored multiplicity pattern excluded by exact good-reduction certificate',
 'prime':p,'q_mod_prime':q,'R_leading_coefficient_before_monic':leading,
 'R_monic_coefficients_low_to_high':array(R,10),
 'guard_gcd_degrees':gcds,
 'D_inverse_coefficients_low_to_high':array(Dinv),
 'axis_element_basis':'index 9*i+j denotes y^i*v^j',
 'axis_element_coefficients':sum(A,[]),'axis_inverse_coefficients':ainv,
 'multiplication_determinant_mod_prime':norm,
 'source_comparison':comparison,'matrix_source_comparison':matrix_comparison,
 'excluded_orientation_multiset':['++','++','-+','+-','--','--'],
 'characteristic_zero_consequence':'No full Fourier representation with this multiset, even in an algebraically closed characteristic-zero field containing q.',
 'other_six_bank_patterns_decided':False,
 'six_bank_attainment_established':False,
 'method':'Complementary-minor expansion of augmented row-zero determinant, then exact 81-by-81 multiplication determinant and explicit inverse. No source code used.',
}
(HERE/'INDEPENDENT_AXIS_NORM_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
(HERE/'AXIS_MULTIPLICATION_MATRIX_MOD29.json').write_text(json.dumps(M)+'\n')
print(json.dumps({k:v for k,v in result.items() if 'coefficients' not in k},indent=2))
