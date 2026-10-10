#!/usr/bin/env python3
"""Independent exact Phase18 identities and counter-scope controls.
No uploaded modules are imported or executed.
"""
import pathlib,json,math,random
ROOT=pathlib.Path(__file__).resolve().parent
P=2013265921;GEN=31;rng=random.Random(202610092305)
assert P>2 and all(P%d for d in range(2,math.isqrt(P)+1))
def root(n):
 assert (P-1)%n==0
 w=pow(GEN,(P-1)//n,P)
 assert pow(w,n,P)==1
 for q in range(2,n+1):
  if n%q==0 and all(q%d for d in range(2,math.isqrt(q)+1)):
   assert pow(w,n//q,P)!=1
 return w
def dft(v,w):
 n=len(v);out=[];node=1
 for k in range(n):
  cur=1;z=0
  for a in v:z=(z+a*cur)%P;cur=cur*node%P
  out.append(z);node=node*w%P
 return out
def poly(z,q):
 a=0
 for c in reversed(q):a=(a*z+c)%P
 return a
def apply(v,delta,q):
 n=len(v)
 return [sum(c*v[(j-s*delta)%n] for s,c in enumerate(q))%P for j in range(n)]
def decode(v,delta,q,w):
 n=len(v);h=apply(v,delta,q);fh=dft(h,w);target=dft(v,w);out=[];zeros=[]
 for k in range(n):
  den=poly(pow(w,k*delta,P),q)
  if den:out.append(fh[k]*pow(den,-1,P)%P)
  else:out.append(target[k]);zeros.append(k)
 assert out==target
 assert len(zeros)<=min(n,(len(q)-1)*math.gcd(n,delta))
 return {'N':n,'delay':delta,'degree':len(q)-1,'defect_support':sum(bool(x) for x in h),'resonances':len(zeros)}
def cycle_inverse(h,delta,alpha):
 n=len(h);g=math.gcd(n,delta);ell=n//g;closure=(1-pow(alpha,ell,P))%P
 assert closure
 out=[0]*n
 for start in range(g):
  cyc=[(start+t*delta)%n for t in range(ell)];z=0
  for j in cyc:z=(alpha*z+h[j])%P
  prev=z*pow(closure,-1,P)%P
  for j in cyc:prev=(alpha*prev+h[j])%P;out[j]=prev
 assert apply(out,delta,[1,-alpha])==h
 return out
def majority(v,delta):
 assert all(v)
 pair=None;balance=0
 for j in range(len(v)):
  current=(v[j],v[(j-delta)%len(v)])
  if balance==0:pair=current;balance=1
  elif current[0]*pair[1]%P==pair[0]*current[1]%P:balance+=1
  else:balance-=1
 return pair
def reverse_cyclic_solve(diagonal,shift,rhs,p=P):
 n=len(rhs);ib=pow(shift,-1,p);a=1;c=0
 for j in range(n-1,-1,-1):
  slope=-diagonal[j]*ib%p;c=(slope*c+rhs[j]*ib)%p;a=slope*a%p
 assert (1-a)%p
 value=c*pow((1-a)%p,-1,p)%p;out=[0]*n;out[-1]=value
 for j in range(n-1,-1,-1):
  value=(rhs[j]-diagonal[j]*value)*ib%p;out[(j-1)%n]=value
 assert [(diagonal[j]*out[j]+shift*out[(j-1)%n])%p for j in range(n)]==rhs
 return out

cases=[];matrix_entries=0;majority_cases=[]
for n in [4,8,12,16,24,32,48,64,96]:
 w=root(n)
 delays=sorted(set([1,n//2,n-1]))
 for delta in delays:
  v=[rng.randrange(P) for _ in range(n)]
  for q in [[1],[1,-2],[1,-5,6],[1,-pow(w,-delta,P)]]:
   cases.append(decode(v,delta,q,w))
   # Directly verify every F q(S^delta) = diag(q(w^(k delta))) F entry.
   for k in range(n):
    den=poly(pow(w,k*delta,P),q)
    for j in range(n):
     lhs=sum(c*pow(w,k*((j+s*delta)%n),P) for s,c in enumerate(q))%P
     assert lhs==den*pow(w,k*j,P)%P;matrix_entries+=1
  if math.gcd(n,delta)==1:
   # One nonperiodic geometric mode has one boundary defect.
   a=2
   if pow(a,n,P)==1:a=3
   v=[0]*n
   for t in range(n):v[t*delta%n]=pow(a,t,P)
   pair=majority(v,delta);assert pair[0]==a*pair[1]%P
   h=apply(v,delta,[pair[1],-pair[0]])
   assert sum(bool(x) for x in h)==1
   majority_cases.append({'N':n,'delay':delta,'defects':1})

# Dense two-mode long-cycle witness, independently constructed.
n=384;delta=191;w=root(n);v=[0]*n
for t in range(n):v[t*delta%n]=(pow(2,t,P)+pow(3,t,P))%P
assert all(v)
two_modes=decode(v,delta,[1,-5,6],w)
assert two_modes['defect_support']==2
diagp=[(7+2*pow(w,-j,P))%P for j in range(n)]
x=reverse_cyclic_solve(diagp,1,v);assert all(x)
two_modes['input_x_support']=sum(bool(a) for a in x)

# Supplied two-factor union: neither individual filter need be sparse.
union=[]
for n in [128,256,384]:
 w=root(n);d1=n//2-1;d2=n-1
 assert math.gcd(n,d1)==math.gcd(n,d2)==1
 h=[0]*n
 for j,a in [(0,5),(n//3,7),(n-1,11)]:h[j]=a
 v=cycle_inverse(cycle_inverse(h,d2,3),d1,2)
 h1=apply(v,d1,[1,-2]);h2=apply(v,d2,[1,-3]);hh=apply(h1,d2,[1,-3])
 assert hh==h
 fv=dft(v,w);fh=dft(h,w);out=[];zeros=0
 for k in range(n):
  den=(1-2*pow(w,k*d1,P))*(1-3*pow(w,k*d2,P))%P
  if den:out.append(fh[k]*pow(den,-1,P)%P)
  else:out.append(fv[k]);zeros+=1
 assert out==fv and zeros==0
 assert all(v) and all(h1) and all(h2)
 diagp=[(7+2*pow(w,-j,P))%P for j in range(n)];diagl=[(7+pow(w,j,P))%P for j in range(n)]
 x=reverse_cyclic_solve(diagp,1,v);fx=dft(x,w)
 assert all(x) and reverse_cyclic_solve(diagl,2,out)==fx
 union.append({'N':n,'delays':[d1,d2],'alphas':[2,3],'r_support':n,'x_support':n,'individual_defect_supports':[n,n],'joint_defect_support':3,'resonances':0,'full_Green_transform_equals_direct_DFT':True})

# Noncoprime dimension caveat: q=1-z at delay N/2 has kernel dimension N/2.
counter=[]
for n in [8,16,32]:
 delta=n//2
 for j in range(delta):
  v=[0]*n;v[j]=v[j+delta]=1;assert not any(apply(v,delta,[1,-1]))
 counter.append({'N':n,'delay':delta,'degree':1,'K':0,'independent_kernel_vectors':delta,'naive_d_plus_K':1})

# Exact number of resonances of every tested binomial, including alpha zero.
resonance_checks=0
for n in [4,8,12,16,24,32,48,64,96]:
 w=root(n)
 for delta in range(1,n):
  g=math.gcd(n,delta);ell=n//g
  for alpha in [0,1,2,pow(w,delta,P)]:
   actual=sum((1-alpha*pow(w,k*delta,P))%P==0 for k in range(n))
   expected=g if alpha and pow(alpha,ell,P)==1 else 0
   assert actual==expected;resonance_checks+=1

out={'field':P,'primitive_root_base':GEN,'exact_decode_cases':cases,'Fourier_filter_matrix_entries_checked':matrix_entries,
 'guaranteed_majority_cases':majority_cases,'dense_two_mode_case':two_modes,'known_union_cases':union,
 'noncoprime_dimension_counterexamples':counter,'binomial_resonance_count_checks':resonance_checks,
 'scope':'Exact filter identities and controls; no uploaded execution, no reproduction of uploaded benchmark proxies.',
 'uploaded_code_executed':False}
(ROOT/'INDEPENDENT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
