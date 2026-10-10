"""Independently authored controls. Does not read/import/execute supplied programs."""
import json, math, itertools, random
import numpy as np
from pathlib import Path
OUT=Path(__file__).parent

def mm(a,b,p): return (np.asarray(a,dtype=object)@np.asarray(b,dtype=object))%p
def inv(a,p):
 a=np.asarray(a,dtype=object); n=len(a); z=np.concatenate((a.copy()%p,np.eye(n,dtype=object)),axis=1)
 for j in range(n):
  k=next(k for k in range(j,n) if math.gcd(int(z[k,j]),p)==1)
  z[[j,k]]=z[[k,j]];z[j]=z[j]*pow(int(z[j,j]),-1,p)%p
  for k in range(n):
   if k!=j:z[k]=(z[k]-z[k,j]*z[j])%p
 return z[:,n:]
def root(q,p):return next(z for z in range(2,p) if pow(z,q,p)==1 and all(pow(z,d,p)!=1 for d in range(1,q)))
def phase(q,n,p,z):
 pts=list(itertools.product(range(q),repeat=n)); f=np.array([[pow(z,sum(a*b for a,b in zip(x,y))%q,p) for y in pts] for x in pts],dtype=object)
 return pts,f

def operators(q,n,p,z,C=None,A=None):
 pts,F=phase(q,n,p,z); idx={v:i for i,v in enumerate(pts)}; Q=len(pts)
 if C is not None:
  return np.diag([pow(z,int(np.array(x,dtype=object)@C@np.array(x,dtype=object))*pow(2,-1,q)%q,p) for x in pts]).astype(object)
 if A is not None:
  P=np.zeros((Q,Q),dtype=object)
  for j,x in enumerate(pts):P[idx[tuple(int(v) for v in (A@np.array(x,dtype=object))%q)],j]=1
  return P
 return F

def proj(a,b,p):
 nz=next(((i,j) for i in range(len(a)) for j in range(len(a)) if b[i,j]%p),None)
 if nz is None:return bool(np.all(a%p==0))
 i,j=nz;c=int(a[i,j])*pow(int(b[i,j]),-1,p)%p
 return c!=0 and bool(np.all((a-c*b)%p==0))
def block(A,B,C,D): return np.block([[A,B],[C,D]])

results={'supplied_programs_executed':False,'checks':{}}
# Small exact sign witness, q=3, coefficient field F7.
q=3;p=7;z=2;pts,F=phase(q,1,p,z);Cp=operators(q,1,p,z,C=np.array([[1]],dtype=object)); Cm=operators(q,1,p,z,C=np.array([[-1]],dtype=object)); Pminus=operators(q,1,p,z,A=np.array([[-1]],dtype=object))
source=mm(mm(inv(F,p),Cp,p),F,p);correct=mm(mm(inv(F,p),Cm,p),F,p);bruhat=mm(mm(mm(Cp,Pminus,p),F,p),Cp,p)
results['checks']['upper_sign']={'source_Finv_Cplus_F':source.tolist(),'correct_Finv_Cminus_F':correct.tolist(),'bruhat_Uplus':bruhat.tolist(),'source_matches_Uplus':proj(source,bruhat,p),'correct_matches_Uplus':proj(correct,bruhat,p)}
assert not proj(source,bruhat,p) and proj(correct,bruhat,p)
# Fresh exact words and all-row support, including coherent upper shears.
rng=random.Random(10100958);word_records=[]
for q,n,p in [(3,2,19),(9,2,163)]:
 z=root(q,p);pts,F=phase(q,n,p,z);Q=q**n;I=np.eye(n,dtype=object);O=np.zeros((n,n),dtype=object);W=block(O,-I,I,O)%q
 for trial in range(8):
  S=np.eye(2*n,dtype=object);K=np.eye(Q,dtype=object)
  for st in range(4):
   kind=rng.randrange(3);a=rng.randrange(q);b=rng.randrange(q);c=rng.randrange(q);C=np.array([[a,b],[b,c]],dtype=object)
   if kind==0:G=block(I,O,C,I)%q;R=operators(q,n,p,z,C=C)
   elif kind==1:G=block(I,C,O,I)%q;R=mm(mm(inv(F,p),operators(q,n,p,z,C=-C),p),F,p)
   else:G=W;R=F
   S=mm(G,S,q);K=mm(R,K,p)
  A=S[:n,:n];B=S[:n,n:];D=S[n:,n:]
  image={tuple(int(v) for v in (B@np.array(x,dtype=object))%q) for x in pts};ker=[x for x in pts if all(v==0 for v in (B@np.array(x,dtype=object))%q)]
  supports=[sum(int(v)!=0 for v in row) for row in K]
  assert set(supports)=={len(image)}
  covariance_failures=0
  for i,x in enumerate(pts):
   for j,y in enumerate(pts):
    if K[i,j]:
     for v in ker:
      if (sum(t*u for t,u in zip(v,y))-int((D@np.array(v,dtype=object))@np.array(x,dtype=object)))%q:covariance_failures+=1
  assert covariance_failures==0
  dense=len(image)==Q;matches=None
  if dense:
   Bi=inv(B,q);L=mm(D,Bi,q);R=mm(Bi,A,q)
   Kb=mm(mm(mm(operators(q,n,p,z,C=L),operators(q,n,p,z,A=-B),p),F,p),operators(q,n,p,z,C=R),p)
   matches=proj(K,Kb,p);assert matches
  word_records.append({'q':q,'n':n,'trial':trial,'support':len(image),'dense_bruhat_match':matches,'covariance_failures':covariance_failures})
results['checks']['fresh_words']=word_records
# Six diagonal valuation profiles, direct Gauss sums and formula reconstructed from completing square.
q=9;p=163;z=root(q,p);pts,F=phase(q,2,p,z);I81=np.eye(81,dtype=object);profiles=[]
for vv in [(0,0),(0,1),(1,1),(0,2),(1,2),(2,2)]:
 es=[0 if v==2 else 3**v for v in vv];E=np.diag(es).astype(object);K=mm(mm(inv(F,p),operators(q,2,p,z,C=-E),p),F,p)
 cores=[]
 for v,e in zip(vv,es):
  if not e:cores.append(np.eye(q,dtype=object));continue
  g=3**v;r=q//g;eta=pow(z,g,p);G=sum(pow(eta,(-u*u*pow(2,-1,r))%r,p) for u in range(r))%p
  C=np.zeros((q,q),dtype=object)
  for x in range(q):
   for y in range(q):
    if (y-x)%g==0:C[x,y]=G*pow(r,-1,p)*pow(eta,(((y-x)//g)**2*pow(2,-1,r))%r,p)%p
  cores.append(C)
 predicted=np.kron(cores[0],cores[1])%p;assert np.all((K-predicted)%p==0)
 support=3**sum(2-v for v in vv);assert all(sum(int(y)!=0 for y in row)==support for row in K)
 profiles.append({'valuations':vv,'blocks':3**sum(vv),'row_support':support,'max_cross_ratio_order':3**max(2-v for v in vv),'entrywise_formula_match':True})
results['checks']['valuation_profiles']=profiles
# Complex full spectra and common-gauge constants; these are supporting numeric checks only.
nums=[]
for s in [2,4,6,8,10]:
 N=s*s;j=np.arange(N);tau=s*(j//s)+(j%s+s//2)%s;U=np.exp(-2j*np.pi*np.outer(j,j)/N)/s;Pi=np.eye(N)[:,tau]
 V=Pi@U.conj().T@Pi@U;C=U@Pi-Pi@U;sv=np.linalg.svd(C,compute_uv=False)
 target=np.r_[np.repeat(math.sqrt(2+math.sqrt(2)),N//2),np.repeat(math.sqrt(2-math.sqrt(2)),N//2)]
 H=np.exp(-2j*np.pi*(np.outer(j,tau)-np.outer(tau,j))/N);hs=np.linalg.svd(H,compute_uv=False);rho=2/(s*math.sin(math.pi/s));ht=np.zeros(N);ht[:4]=[N/2*(1+rho),N/2*math.sqrt(max(0,1-rho*rho)),N/2*math.sqrt(max(0,1-rho*rho)),N/2*(1-rho)]
 nums.append({'s':s,'V4_error':float(np.max(abs(np.linalg.matrix_power(V,4)+np.eye(N)))),'commutator_spectrum_error':float(max(abs(sv-target))),'phase_ratio_spectrum_error':float(max(abs(hs-ht)))})
assert max(max(r[k] for k in ['V4_error','commutator_spectrum_error','phase_ratio_spectrum_error']) for r in nums)<1e-9
results['checks']['numerical_spectra']=nums
# Exact 4x4 Gram characteristic polynomial.
import sympy as sp
r,l=sp.symbols('r l');A=sp.Matrix([[1,r,0,0],[r,1,0,0],[0,0,1,-r],[0,0,-r,1]]);B=sp.Matrix([[1,0,r,0],[0,1,0,-r],[r,0,1,0],[0,-r,0,1]])
poly=(A*B).charpoly(l).as_expr();desired=(l-(1+r)**2)*(l-(1-r)**2)*(l-(1-r*r))**2
assert sp.expand(poly-desired)==0
results['checks']['gram_polynomial']=str(sp.factor(poly))
results['status']='PASS: exact algebra controls and numerical supporting spectra; no supplied program execution'
(OUT/'fresh_check_results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({'status':results['status'],'word_count':len(word_records),'profiles':len(profiles),'sign_witness':results['checks']['upper_sign']},indent=2))
