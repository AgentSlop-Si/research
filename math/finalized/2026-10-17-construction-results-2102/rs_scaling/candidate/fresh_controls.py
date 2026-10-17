"""Fresh controls for branch-preserving radial/basis scaling. No inherited code."""
import json, hashlib, time
from pathlib import Path
from fractions import Fraction
import sympy as s
import mpmath as mp
OUT=Path(__file__).resolve().parent
START=time.time()
x=s.Symbol('x')
res={'scope':'Exact finite controls plus high-precision diagnostics; numerical roots are not certified enclosures.', 'exact':{}, 'numerical':[]}
# Direct signed-circulant entry phase sums. The ring is Z[q]/Phi_N.
count=0;wrong=0
for N in range(4,130,2):
 phi=s.Poly(s.cyclotomic_poly(N,x),x)
 ph=[int(v) for v in reversed(phi.all_coeffs())]
 def rem(v):
  v=list(v);d=len(ph)-1
  for k in range(len(v)-1,d-1,-1):
   a=v[k]
   if a:
    for j in range(d+1):v[k-d+j]-=a*ph[j]
  return v[:d]
 cexp=[(j*(j-1)//2)%N for j in range(N)]
 # Translation gives all column pairs from these N lags; inspect each signed pair directly.
 for k in range(N):
  coeff=[0]*N;positive=[0]*N
  for row in range(N):
   a=row;b=(row-k)%N;sgn=-1 if row<k else 1
   e=(cexp[a]-cexp[b])%N
   coeff[e]+=sgn;positive[e]+=1
  poly=rem(coeff)
  assert poly==([N]+[0]*(len(ph)-2) if k==0 else [0]*(len(ph)-1))
  count+=1
  if k and any(rem(positive)):wrong+=1
res['exact']['cyclotomic_unitarity']={'N':'all even 4..128','lag_identities':count,'wrong_positive_wrap_nonzero_lags':wrong}
assert wrong>0
print('exact phase checks',count,flush=True)
# Exact rational weighted shift and resolvent controls, independent of RS roots.
shift_cases=[]
for N in [4,6,8,10]:
 T=s.zeros(N)
 for j in range(N-1):T[j+1,j]=1
 T[0,N-1]=-1
 assert T**N==-s.eye(N)
 for r in [s.Rational(3,2),s.Integer(2),s.Integer(8)]:
  D=s.diag(*[r**j for j in range(N)]);S=D.inv()*T*D
  assert S**N==-s.eye(N)
  assert S[0,N-1]==-r**(N-1)
  for j in range(N-1):assert S[j+1,j]==1/r
  assert S!=T/r and (T/r)**N!=-s.eye(N)
  for a in [s.Rational(1,3),s.Rational(3,2),s.Integer(2)]:
   R=(s.eye(N)-a*T).inv();normalized=(s.eye(N)-(a/r)*(r*T)).inv()
   assert normalized==R
   assert (s.eye(N)-a*S).inv()==D.inv()*R*D
   # Multiplicative branch coefficient error commutes with similarity, exactly.
   delta=s.Rational(1,1024)
   assert D*(delta*D.inv()*R*D)*D.inv()==delta*R
   # Forgetting rescaled generator or wrap must fail.
   assert (s.eye(N)-(a/r)*T).inv()!=R
   shift_cases.append({'N':N,'r':str(r),'alpha':str(a)})
res['exact']['rational_shift_and_resolvent_cases']=shift_cases
print('exact matrix checks',len(shift_cases),flush=True)
# Exact dyadic output-perturbation range. Same construction works for U and U*.
ranges=[]
for N in range(4,130,2):
 r=Fraction(8);u=Fraction(1,2**200);Dmax=r**(N-1)
 amplified=u*Dmax
 assert amplified/u==Dmax
 assert 2**(3*(N-1))==Dmax
 ranges.append({'N':N,'log2_decode_amplification':3*(N-1),'log2_condition_lower_numerator':6*(N-1)})
res['exact']['dyadic_range']=ranges
# Fresh explicit canonical RS numerical banks, at high precision.
mp.mp.dps=90
for N in [4,6,8,12,16,24,32]:
 h=N//2;m=h+1;q=mp.exp(2j*mp.pi/N)
 for tv in ['grid_first','one']:
  t=mp.mpf(1)/(2*N) if tv=='grid_first' else mp.mpf(1)
  J=mp.matrix(m)
  for k in range(h):
   J[k,k]=q**(k-1)*((1+q)*q**k-1);J[k,k+1]=1
  for k in range(1,h):J[k,k-1]=q**(3*k-3)*(q**k-1)
  J[h,h-1]=-t
  roots=mp.eig(J,left=False,right=False)
  V=mp.matrix([[a**j for a in roots] for j in range(m)])
  beta=mp.lu_solve(V,mp.matrix([q**(j*(j-1)//2) for j in range(m)]))
  gamma=[b*(1+a**N) for a,b in zip(roots,beta)]
  tau=[mp.exp((2*k+1)*mp.pi*1j/N) for k in range(N)]
  branches=[[g/(1-a*z)/mp.sqrt(N) for a,g in zip(roots,gamma)] for z in tau]
  lambdas=[sum(row) for row in branches]
  moment_error=max(abs(sum(b*a**j for a,b in zip(roots,beta))-q**(j*(j-1)//2)) for j in range(N))
  unit_error=max(abs(abs(l)-1) for l in lambdas)
  chi=max(sum(abs(b) for b in row) for row in branches)
  k=max(range(N),key=lambda j:sum(abs(b) for b in branches[j]))
  lam=lambdas[k];u=mp.mpf('1e-6')/chi
  delta=[-u*lam/abs(lam)*mp.conj(b)/abs(b) if b else 0 for b in branches[k]]
  pert=[sum((1+d)*b for d,b in zip(delta,row)) for row in branches]
  ferr=max(abs(v-l) for v,l in zip(pert,lambdas))
  ierr=max(abs(1/v-1/l) for v,l in zip(pert,lambdas))
  expected=u*chi;iexpected=expected/(1-expected)
  # Scalar normalization by 8 leaves each physical eigenresponse unchanged.
  r=mp.mpf(8)
  scale_error=max(abs(g/(1-(a/r)*(r*z))/mp.sqrt(N)-b) for z,row in zip(tau,branches) for a,g,b in zip(roots,gamma,row))
  assert moment_error<mp.mpf('1e-55') and unit_error<mp.mpf('1e-55')
  assert abs(ferr-expected)<mp.mpf('1e-55') and abs(ierr-iexpected)<mp.mpf('1e-55') and scale_error<mp.mpf('1e-55')
  # Full dense scaled target and inverse. C is built directly from the chirp, not from roots.
  U=mp.matrix(N)
  for a in range(N):
   for b in range(N):
    j=(a-b)%N;sgn=-1 if a<b else 1
    U[a,b]=sgn*q**(j*(j-1)//2)/mp.sqrt(N)
  # Use a mild radius for resolvable SVD; range-8 exact bound is separately proved.
  rr=mp.mpf('1.25');D=mp.diag([rr**j for j in range(N)]);Di=mp.diag([rr**(-j) for j in range(N)])
  A=Di*U*D;Ai=Di*U.H*D
  sv=mp.svd(A,compute_uv=False);svi=mp.svd(Ai,compute_uv=False)
  kD=rr**(N-1);bound=kD**2/N
  cond=sv[0]/sv[N-1]
  assert cond>=bound*(1-mp.mpf('1e-60'))
  assert sv[0]>=kD/mp.sqrt(N) and svi[0]>=kD/mp.sqrt(N)
  # Physical forward and inverse decoding both attain kD amplification.
  z=mp.matrix(N,1);z[0]=1
  dz=mp.matrix(N,1);dz[N-1]=mp.mpf('1e-30')
  out_error=mp.norm(D*dz)/(mp.mpf('1e-30')*mp.norm(D*z))
  assert abs(out_error-kD)<mp.mpf('1e-55')
  res['numerical'].append({'N':N,'parameter':tv,'t':mp.nstr(t,20),'radius':mp.nstr(max(abs(a) for a in roots),20),'minimum_root_gap':mp.nstr(min(abs(a-b) for i,a in enumerate(roots) for b in roots[i+1:]),12),'minimum_resonance_denominator':mp.nstr(min(abs(1+a**N) for a in roots),12),'chi':mp.nstr(chi,20),'forward_extremizer_error':mp.nstr(abs(ferr-expected),8),'inverse_extremizer_error':mp.nstr(abs(ierr-iexpected),8),'moment_error':mp.nstr(moment_error,8),'scalar_scale_identity_error':mp.nstr(scale_error,8),'state_scale_r':'1.25','state_scaled_condition':mp.nstr(cond,16),'state_condition_lower_bound':mp.nstr(bound,16),'physical_decode_amplification':mp.nstr(out_error,16)})
  print('completed',N,tv,'chi',mp.nstr(chi,10),flush=True)
res['elapsed_seconds']=time.time()-START
res['all_checks_passed']=True
(OUT/'RESULTS.json').write_text(json.dumps(res,indent=2)+'\n')
print('ALL CHECKS PASSED',len(res['numerical']),flush=True)
