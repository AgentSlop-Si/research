#!/usr/bin/env python3
"""Fresh characteristic-zero local certificate. No historical package is executed."""
import json,time,hashlib
from pathlib import Path
import sympy as sp
from sympy.polys.domains import QQ
START=time.time(); K=QQ.algebraic_field(sp.exp(sp.I*sp.pi/16)); z=K.unit
O=K.zero; U=K.one; N=8

def zero(n=N,m=N):return [[O for _ in range(m)] for _ in range(n)]
def eye(n=N):return [[U if i==j else O for j in range(n)] for i in range(n)]
def tr(A):return sum((A[i][i] for i in range(len(A))),O)
def add(A,B):return [[a+b for a,b in zip(r,s)] for r,s in zip(A,B)]
def sub(A,B):return [[a-b for a,b in zip(r,s)] for r,s in zip(A,B)]
def scale(A,c):return [[a*c for a in r] for r in A]
def mul(A,B):
 C=zero(len(A),len(B[0]))
 for i,r in enumerate(A):
  for k,a in enumerate(r):
   if a:
    for j,b in enumerate(B[k]):
     if b:C[i][j]+=a*b
 return C
def trans(A):return [list(r) for r in zip(*A)]
def schur(A,B):return [[a*b for a,b in zip(r,s)] for r,s in zip(A,B)]
def frob(A,B):return sum((a*b for r,s in zip(A,B) for a,b in zip(r,s)),O)
def iszero(A):return all(a==O for r in A for a in r)
def matrix_rank(A):
 A=[r[:] for r in A];r=0
 for j in range(len(A[0])):
  p=next((k for k in range(r,len(A)) if A[k][j]),None)
  if p is None:continue
  A[r],A[p]=A[p],A[r];pivot=A[r][j];A[r]=[v/pivot for v in A[r]]
  for k in range(r+1,len(A)):
   f=A[k][j]
   if f:A[k]=[a-f*b for a,b in zip(A[k],A[r])]
  r+=1
  if r==len(A):break
 return r
def encode(x):return [str(q) for q in reversed(x.to_list())]

i=z**8;s=(z-z**-1)/(2*i);c=(z+z**-1)/2;gamma=c*c-s*s;rt2=z**4+z**-4
qe=[0,2,0,10,0,2,0,10];pe=[x+1 for x in qe]
V=[[rt2/4*z**((pe[j]+qe[k]-4*j*k)%32) for k in range(N)] for j in range(N)]
Vc=[[rt2/4*z**((-pe[j]-qe[k]+4*j*k)%32) for k in range(N)] for j in range(N)]
X=scale(add(V,Vc),U/2);Y=scale(sub(V,Vc),U/(2*i))
a=[K.convert(sp.Rational(v,2)) for v in [1,0,-1,0,-1,0,1,0]]
b=[K.convert(sp.Rational(v,2)) for v in [0,1,0,1,0,1,0,1]]
R=[[a[j]*a[k]+b[j]*b[k] for k in range(N)] for j in range(N)];L=sub(eye(),R)
G=scale(mul(mul(mul(L,X),Y),L),U/(s*c))
Omega=scale(sub(scale(L,3),G),U/16)
checks={}
def check(label,result):
 checks[label]=bool(result)
 if not result:raise AssertionError(label)
check('normalized_unitary',mul(trans(Vc),V)==eye())
check('real_projectors',mul(L,L)==L and mul(R,R)==R and iszero(mul(L,R)))
check('baseline_imaginary_spectrum',mul(Y,Y)==add(scale(L,s*s),scale(R,c*c)))
check('witness_symmetric_commuting',trans(X)==X and trans(Y)==Y and mul(X,Y)==mul(Y,X))
check('dual_real_symmetric',trans(G)==G and trans(Omega)==Omega)
check('G_square_L',mul(G,G)==L)
check('G_trace_2',tr(G)==2*U)
check('Omega_trace_1',tr(Omega)==U)
check('Omega_support',mul(L,Omega)==Omega and mul(Omega,L)==Omega)
check('Omega_minimal_polynomial',iszero(mul(sub(Omega,scale(L,U/8)),sub(Omega,scale(L,U/4)))))

W=mul(trans(V),V)
check('spectral_arc_low_eigenvalues',mul(W,L)==add(scale(add(L,G),z**2/2),scale(sub(L,G),z**-2/2)))
check('spectral_arc_high_eigenvalue',mul(W,R)==scale(R,z**14))
Pi=[[K.convert(sp.Rational(1,2)) if (j-k)%4==0 else O for k in range(8)] for j in range(8)]
Hd=[[z**((-8*j*k)%32) for k in range(8)] for j in range(8)]
Hdc=[[z**((8*j*k)%32) for k in range(8)] for j in range(8)]
check('energy_Fourier_HstarH_16Pi',mul(trans(Hdc),Hd)==scale(Pi,16))
check('energy_Fourier_projection',mul(Hd,Pi)==Hd and mul(Pi,Hd)==Hd)

# alpha_0..alpha_3, beta_1..beta_3 are periodic phase coordinates;
# rho_0..rho_3, sigma_0..sigma_3 are their antisymmetric coordinates.
periodic=[];normal=[]
for side,indices in [('p',range(4)),('q',range(1,4))]:
 for r in indices:
  v=[0]*8;v[r]=v[r+4]=1
  periodic.append([[K.convert(v[j] if side=='p' else v[k]) for k in range(8)] for j in range(8)])
for side in ['p','q']:
 for r in range(4):
  v=[0]*8;v[r]=1;v[r+4]=-1
  normal.append([[K.convert(v[j] if side=='p' else v[k]) for k in range(8)] for j in range(8)])

def first(D):
 Y1=schur(X,D)
 H1=add(mul(trans(Y),Y1),mul(trans(Y1),Y))
 return Y1,H1,mul(mul(L,H1),L)
firstp=[first(D) for D in periodic];firstn=[first(D) for D in normal]
check('all_8_normal_first_derivatives_zero',all(iszero(A) for _,_,A in firstn))
rank=matrix_rank([[A[j][k] for _,_,A in firstp] for j in range(8) for k in range(8)])
check('periodic_first_derivative_rank_7',rank==7)
expected_gram=[[5,0,1,0,1,2,1],[0,5,0,1,2,1,2],[1,0,5,0,1,2,1],[0,1,0,5,2,1,2],[1,2,1,2,5,0,1],[2,1,2,1,0,5,0],[1,2,1,2,1,0,5]]
normalized_gram=[[frob(A,B)/(s*c)**2 for _,_,B in firstp] for _,_,A in firstp]
check('normalized_Gram_matches_displayed_integer_matrix',normalized_gram==[[K.convert(v) for v in row] for row in expected_gram])
check('normalized_Gram_determinant_12288',sp.Matrix(expected_gram).det()==12288)
check('dual_annihilates_all_15_derivatives',all(frob(Omega,A)==O for _,_,A in firstp+firstn))

# Effective second Taylor coefficient on the low spectral cluster:
# L(H2 - H1 R H1/gamma)L. Omega is supported on L.
beta=gamma/(4*rt2)
weighted=zero(8,8);uncorrected=zero(8,8)
for j in range(8):
 Yj,Hj,_=firstn[j]
 for k in range(j+1):
  Yk,Hk,_=firstn[k]
  Ycross=schur(Y,schur(normal[j],normal[k]))
  H2jk=sub(scale(add(mul(trans(Yj),Yk),mul(trans(Yk),Yj)),U/2),scale(add(mul(trans(Y),Ycross),mul(trans(Ycross),Y)),U/2))
  Hcorr=scale(add(mul(mul(Hj,R),Hk),mul(mul(Hk,R),Hj)),U/(2*gamma))
  weighted[j][k]=weighted[k][j]=frob(Omega,sub(H2jk,Hcorr))
  uncorrected[j][k]=uncorrected[k][j]=frob(Omega,H2jk)
check('weighted_second_variation_beta_identity',weighted==scale(eye(8),beta))
check('beta_cos_pi_8_over_4_sqrt_2',beta==(z**2+z**-2)/(8*rt2))

# Destructive controls: these must be detected, not treated as certificates.
controls={
 'wrong_second_variation_scalar_rejected':weighted!=scale(eye(8),beta+U/100),
 'omit_resolvent_correction_rejected':uncorrected!=weighted,
 'uniform_dual_weight_rejected':any(frob(scale(L,U/6),A)!=O for _,_,A in firstp),
 'drop_normal_pair_sign_rejected':not iszero(first([[K.convert(1 if j==0 else 0) for k in range(8)] for j in range(8)])[2]),
}
check('all_negative_controls_rejected',all(controls.values()))
output={'status':'PASS','arithmetic':'Q[z]/(z^16+1), z=exp(i*pi/16), characteristic zero','checks':checks,'periodic_derivative_rank':rank,'normal_derivative_dimension':8,'dual_eigenvalues_on_low_space':['1/8 (multiplicity 4)','1/4 (multiplicity 2)'],'second_variation_scalar':'cos(pi/8)/(4*sqrt(2)) > 0','beta_power_basis_ascending':encode(beta),'negative_controls':controls,'elapsed_seconds':time.time()-START,'scope':'Strict local optimality in all 15 phase directions modulo scalar phase transfer. No global minimax certificate.'}
path=Path(__file__).parent/'EXACT_LOCAL_CHECKS.json';path.write_text(json.dumps(output,indent=2)+'\n');print(json.dumps(output,indent=2))
