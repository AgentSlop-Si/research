"""Fresh independent N13 rank audit. Historical scientific code is never executed/imported."""
from pathlib import Path
from itertools import permutations
import json, hashlib, time
P=53; N=13; Q=16
ROOT=Path(__file__).resolve().parent
CAND=ROOT/'sources'/'RANK_DATA.json'
FINAL=ROOT/'sources'/'CANDIDATE_CERTIFICATE.json'
assert all(P%k for k in range(2,8))
assert pow(Q,N,P)==1 and Q!=1

def tr(a):
 a=[int(x)%P for x in a]
 while len(a)>1 and not a[-1]: a.pop()
 return a or [0]
def add(a,b):
 c=[0]*max(len(a),len(b))
 for i,x in enumerate(a): c[i]+=x
 for i,x in enumerate(b): c[i]+=x
 return tr(c)
def neg(a):return tr([-x for x in a])
def sub(a,b):return add(a,neg(b))
def scale(a,k):return tr([k*x for x in a])
def mul(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]=(c[i+j]+x*y)%P
 return tr(c)
def divmodp(a,b):
 a=tr(a);b=tr(b);assert b!=[0]
 q=[0]*max(1,len(a)-len(b)+1)
 while a!=[0] and len(a)>=len(b):
  d=len(a)-len(b);c=a[-1]*pow(b[-1],-1,P)%P;q[d]=c
  a=sub(a,[0]*d+scale(b,c))
 return tr(q),a
def gcd(a,b):
 while b!=[0]:a,b=b,divmodp(a,b)[1]
 return scale(a,pow(a[-1],-1,P))
def xgcd(a,b):
 s,t=[1],[0];u,v=[0],[1]
 while b!=[0]:
  q,r=divmodp(a,b);a,b=b,r;s,u=u,sub(s,mul(q,u));t,v=v,sub(t,mul(q,v))
 z=pow(a[-1],-1,P)
 return scale(a,z),scale(s,z),scale(t,z)
def powmod(a,n,m):
 v=[1]
 while n:
  if n&1:v=divmodp(mul(v,a),m)[1]
  a=divmodp(mul(a,a),m)[1];n//=2
 return v
def val(a,x):
 s=0
 for c in a[::-1]:s=(s*x+c)%P
 return s

# Rebuild coefficients by right multiplication in the Weyl algebra.
# (U^r V^l)U = omega^l U^(r+1)V^l.
def table(e,d):
 omega=pow(Q,(e*d)%N,P);D={(0,0):1}
 for degree in range(1,N):
  for r in range(degree+1):
   l=degree-r;D[r,l]=(pow(omega,l,P)*D.get((r-1,l),0)+D.get((r,l-1),0))%P
 return D
T={(e,d):table(e,d) for e in [-1,1] for d in [-1,1]}
def G(e,d,a,b):return T[e,d].get((e*a%N,d*b%N),0)
def moment(a,b):
 den=G(1,1,a,b);isolated=G(-1,1,N-b,b)
 assert den and isolated
 out=[0]*(N-a-b+1)
 out[0]=pow(Q,10*(a+b)**2%N,P)*pow(den,-1,P)%P
 out[-1]-=G(-1,1,a,b)*pow(den*isolated%P,-1,P)
 return tr(out)
ROWS=[(b,a) for b in (1,2) for a in range(b,N-b-7)]
E=[[moment(a+k,b) for k in range(8)] for b,a in ROWS]
A=[r[:7] for r in E];B=[r[7] for r in E]
assert len(ROWS)==6
cand=json.loads(CAND.read_text())
assert E==cand['E7']

# Determinants use scalar Gaussian elimination and degree-bounded Lagrange
# interpolation, independent of the candidate permutation polynomial method.
def scalar_det(M):
 M=[r[:] for r in M];z=1
 for c in range(len(M)):
  r=next((r for r in range(c,len(M)) if M[r][c]),None)
  if r is None:return 0
  if r!=c:M[r],M[c]=M[c],M[r];z=-z
  pivot=M[c][c];z=z*pivot%P;inv=pow(pivot,-1,P)
  for r in range(c+1,len(M)):
   f=M[r][c]*inv%P
   for j in range(c+1,len(M)):M[r][j]=(M[r][j]-f*M[c][j])%P
   M[r][c]=0
 return z%P
DETS=[]
def determinant(M,label):
 n=len(M)
 bound=max(sum(len(M[r][p[r]])-1 for r in range(n)) for p in permutations(range(n)))
 assert bound<P
 values=[scalar_det([[val(e,x) for e in row] for row in M]) for x in range(P)]
 out=[0]
 for i in range(bound+1):
  term=[1];den=1
  for j in range(bound+1):
   if i!=j:term=mul(term,[-j,1]);den=den*(i-j)%P
  out=add(out,scale(term,values[i]*pow(den,-1,P)%P))
 assert all(val(out,x)==values[x] for x in range(P))
 DETS.append({'label':label,'formal_degree_bound':bound,'actual_degree':len(out)-1,'coefficients':out})
 return out
D=[]
for j in range(7):
 M=[[row[k] for k in range(7) if k!=j] for row in A]
 D.append(determinant(M,'delete_column_'+str(j)))
assert D==cand['minors']
assert len(D[0])-1==32 and len(D[6])-1==37
one,U,V=xgcd(D[0],D[6]);assert one==[1]
assert add(mul(U,D[0]),mul(V,D[6]))==[1]

# Prime degree 37 Rabin test requires x^(53^37)=x mod D6 and gcd(x^53-x,D6)=1.
f=scale(D[6],pow(D[6][-1],-1,P));x=[0,1]
z=x[:];frobenius=[]
for k in range(1,38):
 z=powmod(z,P,f)
 frobenius.append({'power':k,'remainder':z})
assert z==x
assert gcd(sub(frobenius[0]['remainder'],x),f)==[1]
assert all(37%k for k in range(2,7))
assert gcd(D[0],D[6])==[1]

# Signed maximal-minor kernel vector, validated as polynomial identity.
C=[scale(d,(-1)**j) for j,d in enumerate(D)]
for row in A:
 s=[0]
 for e,c in zip(row,C):s=add(s,mul(e,c))
 assert s==[0]

# Construct a denominator-free particular solution with two Cramer charts.
# A W_j = -D_j B, with missing component j zero.
W=[]
for omitted in (0,6):
 cols=[k for k in range(7) if k!=omitted]
 M=[[row[k] for k in cols] for row in A]
 w=[[0] for _ in range(7)]
 for loc,k in enumerate(cols):
  MM=[[neg(B[r]) if cc==loc else M[r][cc] for cc in range(6)] for r in range(6)]
  w[k]=determinant(MM,'cramer_omit_'+str(omitted)+'_coefficient_'+str(k))
 for r,row in enumerate(A):
  s=[0]
  for a,b in zip(row,w):s=add(s,mul(a,b))
  assert s==neg(mul(D[omitted],B[r]))
 W.append(w)
H=[add(mul(U,W[0][j]),mul(V,W[1][j])) for j in range(7)]
for r,row in enumerate(A):
 s=B[r]
 for a,b in zip(row,H):s=add(s,mul(a,b))
 assert s==[0]
# Both global formulas must agree with the ordinary h6=lambda chart at y=1.
pinned=[(16,31),(50,25),(19,11),(27,10),(48,15),(50,22),(0,1)]
for lam in range(P):
 cs=[val(c,1) for c in C]; hs=[val(h,1) for h in H]
 tau=(lam-hs[6])*pow(cs[6],-1,P)%P
 got=[(a+tau*b)%P for a,b in zip(hs,cs)]
 assert got==[(a+b*lam)%P for a,b in pinned]
# Independently verify the candidate's final certificate as inert data.
final=json.loads(FINAL.read_text())
assert final['E7']==E and final['maximal_minors_delete_columns_0_through_6']==D
assert final['D6_monic']==f
assert final['bezout']['D0_multiplier']==U and final['bezout']['D6_multiplier']==V
assert final['global_parameterization']['kernel_h0_through_h6']==C
assert final['global_parameterization']['particular_h0_through_h6']==H
assert final['cramer_h0_zero_numerators']==W[0]
assert final['cramer_h6_zero_numerators']==W[1]
ir=final['irreducibility']
assert ir['X_to_53_mod_f']==frobenius[0]['remainder']
assert ir['X_to_53_power_37_mod_f']==z
assert add(mul(ir['f_multiplier'],f),mul(ir['X_to_53_minus_X_multiplier'],sub(frobenius[0]['remainder'],x)))==[1]
# The degree-37 exceptional chart is genuine, but another minor stays invertible.
assert divmodp(D[6],f)[1]==[0]
assert divmodp(mul(U,D[0]),f)[1]==[1]
# A primitive kernel coordinate gives a polynomial inverse parameter.
assert add(mul(U,C[0]),mul(V,C[6]))==[1]
# Targeted corruptions must invalidate independent identities.
def residual(vector):
 out=[]
 for row in A:
  s=[0]
  for a,b in zip(row,vector):s=add(s,mul(a,b))
  out.append(s)
controls={}
bad=[c[:] for c in C];bad[0]=add(bad[0],[1])
controls['kernel_one_coefficient_corruption_rejected']=residual(bad)!=[[0]]*6
bad=[h[:] for h in H];bad[0]=add(bad[0],[1])
controls['particular_one_coefficient_corruption_rejected']=residual(bad)!=[neg(b) for b in B]
controls['bezout_one_coefficient_corruption_rejected']=add(mul(add(U,[1]),D[0]),mul(V,D[6]))!=[1]
controls['minor_one_coefficient_corruption_rejected']=val(add(D[6],[1]),0)!=scalar_det([[val(row[k],0) for k in range(6)] for row in A])
assert all(controls.values())
# All 53 base specializations have full rank; polynomial certificate covers all extensions.
assert all(any(val(d,y) for d in D) for y in range(P))
result={
 'verdict':'ACCEPT bounded rank and affine parameterization claims',
 'source_sha256':hashlib.sha256(CAND.read_bytes()).hexdigest(),
 'final_candidate_certificate_sha256':hashlib.sha256(FINAL.read_bytes()).hexdigest(),
 'negative_controls':controls,
 'degree_37_chart_singularity_verified':True,
 'polynomial_inverse_parameter':'tau=U*(h0-H0)+V*(h6-H6)',
 'method':{'G':'right-multiplication Weyl recurrence','determinants':'scalar Gaussian evaluation with independently bounded polynomial interpolation','irreducibility':'prime-degree Rabin Frobenius/gcd test'},
 'rows_b_a':ROWS,'E7':E,'determinants':DETS,
 'bezout':{'U':U,'V':V,'identity':'U*D0 + V*D6 = 1'},
 'D6_monic':f,'D6_irreducibility':{'degree':37,'frobenius':frobenius,'first_gcd':[1],'last_remainder':z},
 'signed_kernel_vector':C,'global_particular_solution':H,
 'verified_identities':['A*C=0','A*H=-B','U*D0+V*D6=1','all 53 pinned lambdas agree'],
 'claimed_minimum_extension_degree':None,
 'scope':'Rank-drop prerequisite only. No free-cross sixteen-bank existence, exclusion, support splitting, full-sector compatibility, or arithmetic speed result.'}
(ROOT/'CHECK_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'verdict':result['verdict'],'determinant_bounds':[z['formal_degree_bound'] for z in DETS[:7]],'minor_degrees':[len(d)-1 for d in D],'bezout_degrees':[len(U)-1,len(V)-1],'particular_solution_degrees':[len(h)-1 for h in H],'result':str(ROOT/'CHECK_RESULT.json')}))
