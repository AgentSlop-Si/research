#!/usr/bin/env python3
"""Auditor-authored Phase22 controls; imports only our preserved independent math."""
import itertools,json,math,random,sys
from pathlib import Path
import independent_phase21_math as M
trim,add,mul,ev,rem,gcd=M.trim,M.padd,M.pmul,M.peval,M.premainder,M.pgcd
RNG=random.Random(220991)
def sub(a,b,p):return add(a,[-c%p for c in b],p)
def divlin(a,x,p):
 q=[0]*(len(a)-1);q[-1]=a[-1]
 for j in range(len(q)-2,-1,-1):q[j]=(a[j+1]+x*q[j+1])%p
 assert (a[0]+x*q[0])%p==0
 return trim(q)
def remove_identity(v,p):
 v=trim([c%p for c in v]);k=0
 while len(v)>1 and ev(v,2,p)==0:v=divlin(v,2,p);k+=1
 return v,k
def dickson_full(n,p):
 a=[2];b=[0,1]
 if n==0:return a
 for _ in range(1,n):a,b=b,sub(mul([0,1],b,p),a,p)
 return b
# Independent 2x2 transfer-matrix powering; no source binary-pair recurrence.
def dickson_quotient(n,v,p):
 def matmul(A,B):return [[rem(add(mul(A[i][0],B[0][j],p),mul(A[i][1],B[1][j],p),p),v,p)for j in range(2)]for i in range(2)]
 a=[[[1],[]],[[],[1]]];b=[[[0,1],[p-1]],[[1],[]]]
 while n:
  if n&1:a=matmul(a,b)
  n//=2
  if n:b=matmul(b,b)
 return rem(add(a[0][0],a[1][1],p),v,p)
def sieve(v,n,p,full=None):
 v=trim([c%p for c in v]);assert v
 v,removed=remove_identity(v,p)
 if len(v)<2:return [1],removed
 if full is None:d=dickson_quotient(n,v,p)
 else:d=rem(full,v,p)
 return gcd(v,sub(d,[2],p),p),removed
def bsgs(target,w,n,p):
 q=math.isqrt(n)+1;table={};z=1
 for j in range(q):table.setdefault(z,j);z=z*w%p
 step=pow(w,-q,p);z=target
 for i in range((n+q-1)//q+1):
  if z in table:
   d=(i*q+table[z])%n
   if pow(w,d,p)==target:return d
  z=z*step%p
 return None
def enum_half(g,w,n,p):
 out=[]
 for d in range(1,n//2+1):
  t=(pow(w,d,p)+pow(w,-d,p))%p
  if ev(g,t,p)==0:out+= [d] if d==n-d else [d,n-d]
 return sorted(out)
def enum_linear(g,w,n,p):
 t=-g[0]*pow(g[1],-1,p)%p
 # Independent exhaustive field oracle for quadratic roots, deliberately not a complexity claim.
 roots=[z for z in range(p)if (z*z-t*z+1)%p==0 and pow(z,n,p)==1 and z!=1]
 ds=[bsgs(z,w,n,p)for z in roots];assert all(d is not None for d in ds)
 return sorted(set(ds))
def findroot(n,p):return next(w for w in range(1,p)if pow(w,n,p)==1 and len({pow(w,k,p)for k in range(n)})==n)
def trace_from_U(U,b,p):
 r=U[:];V=[0]*(b+1)
 for j in range(b,-1,-1):
  c=r[b+j];V[j]=c
  for k in range(j+1):r[b+j-2*k]=(r[b+j-2*k]-c*math.comb(j,k))%p
 assert not any(r)
 return trim(V)
def gate(r,w,p,s):
 n=len(r);R=M.dft(r,w,p,4*s);meta={'full_checks':0,'candidate_roots':0}
 if not all(R):return None,{**meta,'reason':'zero-probe'}
 T=[pow(x,-1,p)for x in R];U=M.compress(T,s,p)
 if not any(U):return None,{**meta,'reason':'zero-resultant'}
 b=s*(s+1)*(2*s+1)//6;V=trace_from_U(U,b,p);g,k=sieve(V,n,p)
 roots=enum_linear(g,w,n,p) if len(g)==2 else enum_half(g,w,n,p) if len(g)>1 else []
 old=[d for d in range(1,n)if ev(U,pow(w,d,p),p)==0];assert roots==old
 meta.update({'candidate_roots':len(roots),'trace_gcd_degree':len(g)-1,'identity_factors_removed':k})
 powers=[pow(w,k,p)for k in range(n)]
 for delta in roots:
  z=powers[delta];ga=gcd(M.pencil(T,z,0,s,p),M.pencil(T,z,1,s,p),p)
  if len(ga)!=2:continue
  alpha=-ga[0]%p
  if not alpha:continue
  Y=[T[k]*(1-alpha*pow(z,k,p))%p for k in range(4*s)];A=M.prony(Y,s,powers,p)
  if not A:continue
  Ah=[sum(v*pow(z,e,p)for e,v in A.items())%p for z in powers]
  if not all(Ah):continue
  meta['full_checks']+=1
  lhs=[sum(v*r[(j-e)%n]for e,v in A.items())%p for j in range(n)]
  rhs=[(int(j==0)-alpha*int(j==delta))%p for j in range(n)]
  if lhs!=rhs:return None,{**meta,'reason':'full-certificate-failed'}
  out=[(1-alpha*pow(w,k*delta,p))*pow(Ah[k],-1,p)%p for k in range(n)]
  assert out==M.dft(r,w,p)
  return (A,delta,alpha,out),{**meta,'reason':'accepted'}
 return None,{**meta,'reason':'no-candidate'}
def main():
 exhaust=[];randoms=[];linear=0;factor_cases=0;quotient_cases=0
 for p,n in [(7,3),(13,6),(17,4)]:
  w=findroot(n,p);D=dickson_full(n,p);count=0
  for v in itertools.product(range(p),repeat=3):
   if not any(v):continue
   g,k=sieve(v,n,p,D);oracle=[d for d in range(1,n)if ev(v,(pow(w,d,p)+pow(w,-d,p))%p,p)==0]
   assert (len(g)>1)==bool(oracle) and enum_half(g,w,n,p)==oracle if len(g)>1 else not oracle
   if len(g)==2:assert enum_linear(g,w,n,p)==oracle;linear+=1
   count+=1
  exhaust.append({'p':p,'N':n,'nonzero_polynomials_degree_at_most_2':count})
 for p in [17,31,97,193]:
  for n in range(1,p):
   if (p-1)%n:continue
   w=findroot(n,p);D=dickson_full(n,p);f=[1]
   traces={}
   for d in range(n):traces.setdefault((pow(w,d,p)+pow(w,-d,p))%p,[]).append(d)
   for t,indices in traces.items():
    for _ in range(1 if len(indices)==1 else 2):f=mul(f,[-t%p,1],p)
   assert f==sub(D,[2],p);factor_cases+=1
   for j in range(10):
    v=[RNG.randrange(p)for _ in range(RNG.randrange(1,9))]+[RNG.randrange(1,p)]
    if j%3==0:v=mul(v,[-2%p,1],p)
    if n>1 and j%2==0:
     z=pow(w,RNG.randrange(1,n),p);v=mul(v,[-(z+pow(z,-1,p))%p,1],p)
    vv,_=remove_identity(v,p)
    if len(vv)>1:assert dickson_quotient(n,vv,p)==rem(D,vv,p);quotient_cases+=1
    g,k=sieve(v,n,p);oracle=[d for d in range(1,n)if ev(v,(pow(w,d,p)+pow(w,-d,p))%p,p)==0]
    actual=enum_half(g,w,n,p) if len(g)>1 else []
    assert actual==oracle
    if len(g)==2:assert enum_linear(g,w,n,p)==oracle;linear+=1
    randoms.append({'p':p,'N':n,'gcd_degree':len(g)-1,'removed':k,'candidates':len(actual)})
 # Outside N | p-1 there can be an extension-field-only trace.
 g,_=sieve([1,1],3,5);assert g==[1,1] and not [z for z in range(5)if z!=1 and pow(z,3,5)==1]
 # Identity multiplicity disappears entirely, while the even-order -1 root survives.
 for k in range(1,9):
  v=[1]
  for _ in range(k):v=mul(v,[-2%97,1],97)
  gg,removed=sieve(v,16,97);assert gg==[1]and removed==k
  v=mul(v,[2,1],97);gg,removed=sieve(v,16,97);assert gg==[2,1]and enum_linear(gg,findroot(16,97),16,97)==[8]
 logs=0
 for p,n in [(97,1),(97,3),(97,8),(97,96),(193,32),(193,64)]:
  w=findroot(n,p)
  for d in range(n):assert bsgs(pow(w,d,p),w,n,p)==d;logs+=1
 # Reuse only our auditor-authored baseline fixtures with the new sieve integrated.
 M.gate=gate;applications=M.application_tests()
 result={'status':'PASS','uploaded_code_executed':False,'exhaustive':exhaust,'exhaustive_polynomials':sum(x['nonzero_polynomials_degree_at_most_2']for x in exhaust),'random_trace_cases':len(randoms),'random_cases':randoms,'dickson_full_factorization_cases':factor_cases,'matrix_quotient_checks':quotient_cases,'linear_quadratic_BSGS_cases':linear,'individual_BSGS_indices':logs,'extension_field_domain_counterexample':{'p':5,'N':3,'V':[1,1],'gcd':[1,1],'base_field_nonidentity_roots':0},'identity_multiplicity_controls':16,'integrated_applications':applications,'inherited_solver_control':M.inherited_solver_control()}
 path=Path(sys.argv[1] if len(sys.argv)>1 else 'INDEPENDENT_RESULTS.json');path.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print('PASS',result['exhaustive_polynomials'],'polynomials;',len(randoms),'random traces;',len(applications['probe_preserving_adversaries']),'full-certificate adversaries')
if __name__=='__main__':main()
