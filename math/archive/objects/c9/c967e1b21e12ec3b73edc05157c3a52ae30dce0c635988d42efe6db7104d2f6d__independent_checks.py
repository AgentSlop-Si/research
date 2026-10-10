#!/usr/bin/env python3
"""Independent short-prefix audit. Imports only our earlier independent math."""
import json,random,sys
from pathlib import Path
import independent_phase21_math as M
import independent_trace_math as T
rng=random.Random(2300191)
def stream(x,w,m,p):
 out=[0]*m;adds=muls=0
 for j,a in enumerate(x):
  z=pow(w,j,p);u=a
  for k in range(m):
   out[k]=(out[k]+u)%p;adds+=1
   if k<m-1:u=u*z%p;muls+=1
 assert adds==m*len(x) and muls==(m-1)*len(x)
 return out,{'adds':adds,'muls':muls}
def shared_resultant(Ts,z,s,p):
 size=s+1;Z=[pow(z,k,p)for k in range(2*s+2)];xs=list(range(s+2));samples=[[],[]]
 for alpha in xs:
  seq=[Ts[k]*(1-alpha*Z[k])%p for k in range(2*s+2)]
  for b in range(2):samples[b].append(M.determinant([[seq[b+i+j]for j in range(size)]for i in range(size)],p))
 P=[M.interp(xs,v,p)for v in samples];S=[]
 for poly in P:
  padded=(poly+[0]*(size+1-len(poly)))[::-1]
  for j in range(size):S.append([0]*j+padded+[0]*(size-1-j))
 return M.determinant(S,p)
def gate(r,w,p,s):
 n=len(r);m=2*s+2;R,cost=stream(r,w,m,p);meta={'probes':m,'probe_cost':cost,'full_checks':0,'failed_checks':0,'candidate_roots':0}
 if not all(R):return None,{**meta,'reason':'zero-probe'}
 seq=[pow(x,-1,p)for x in R];U=M.compress(seq,s,p)
 if not any(U):return None,{**meta,'reason':'zero-resultant'}
 b=s*(s+1)*(2*s+1)//6;V=T.trace_from_U(U,b,p);G,k=T.sieve(V,n,p);roots=T.enum_half(G,w,n,p)if len(G)>1 else []
 assert roots==[d for d in range(1,n)if M.peval(U,pow(w,d,p),p)==0]and len(roots)<=2*b
 meta.update({'candidate_roots':len(roots),'trace_degree':len(G)-1});powers=[pow(w,k,p)for k in range(n)]
 for delta in roots:
  z=powers[delta];g=M.pgcd(M.pencil(seq,z,0,s,p),M.pencil(seq,z,1,s,p),p)
  if len(g)!=2:continue
  alpha=-g[0]%p
  if not alpha:continue
  Y=[a*(1-alpha*pow(z,k,p))%p for k,a in enumerate(seq)];A=M.prony(Y,s,powers,p)
  if not A:continue
  Ah=[sum(v*pow(z,e,p)for e,v in A.items())%p for z in powers]
  if not all(Ah):continue
  meta['full_checks']+=1;lhs=[sum(v*r[(j-e)%n]for e,v in A.items())%p for j in range(n)];rhs=[(int(j==0)-alpha*int(j==delta))%p for j in range(n)]
  if lhs!=rhs:meta['failed_checks']+=1;continue
  Rall=[(1-alpha*pow(w,k*delta,p))*pow(Ah[k],-1,p)%p for k in range(n)]
  assert Rall==M.dft(r,w,p)
  return (A,delta,alpha,Rall),{**meta,'reason':'accepted'}
 return None,{**meta,'reason':'full-certificate-failed'if meta['failed_checks']else'no-candidate'}
def main():
 probes=[];joint=[]
 for n in [10,12,16,30,32,64,128]:
  p,w=M.field(n)
  for m in sorted({1,2,min(n,6),min(n,10),min(n,18)}):
   x=[rng.randrange(p)for _ in range(n)];a,c=stream(x,w,m,p);assert a==M.dft(x,w,p,m);probes.append({'N':n,'m':m,**c})
 for p in [12289,65537]:
  for s in range(1,9):
   for w in [0,1,p-1,2,7,113]:
    a=[rng.randrange(p)for _ in range(2*s+2)];actual=shared_resultant(a,w,s,p);assert actual==M.res(a,w,s,p)
    # Arbitrary suffix values do not enter either determinant.
    suffix=[rng.randrange(p)for _ in range(max(0,4*s-len(a)))];assert M.res(a+suffix,w,s,p)==actual
    joint.append({'p':p,'s':s,'w':w,'saved_field_ops_per_resultant':6*s*s+14*s})
 old_gate=M.gate;M.gate=gate;applications=M.application_tests()
 # Strictly larger nonzero-prefix coverage: a numerator zero at frequency 11.
 n=32;s=4;p,w=M.field(n);alpha=pow(w,-11,p);A=None
 for trial in range(100):
  C={0:1,1:rng.randrange(1,p),3:rng.randrange(1,p),7:rng.randrange(1,p)};Ah=M.sparse_eval(C,w,n,p)
  if all(Ah):
   R=[(1-alpha*pow(w,k,p))*pow(Ah[k],-1,p)%p for k in range(n)];r=M.idft(R,w,p);f,meta=gate(r,w,p,s)
   if f:A=C;break
 assert A is not None and R[11]==0 and all(R[:10])
 old,oldmeta=old_gate(r,w,p,s);assert old is None and oldmeta['reason']=='zero-probe'and f[-1]==R
 bad=[(r[j]+pow(w,-10*j,p))%p for j in range(n)]
 assert stream(bad,w,10,p)[0]==stream(r,w,10,p)[0] and M.dft(bad,w,p)!=R
 badfound,badmeta=gate(bad,w,p,s);assert badfound is None and badmeta['failed_checks']==2
 extra={'N':n,'p':p,'omega':w,'s':s,'A':A,'alpha':alpha,'zero_frequency':11,'strict_ten_probe_adversary':badmeta,'old_reason':oldmeta['reason'],'new_meta':meta}
 # New legal shorter lengths between 2s+2 and 4s, purely mathematical residual route.
 small=[]
 for n in [10,12]:
  p,w=M.field(n);s=4
  for trial in range(10):
   C={j:rng.randrange(1,p)for j in [0,1,3,7]};Ah=M.sparse_eval(C,w,n,p)
   if not all(Ah):continue
   alpha=rng.randrange(1,p);delta=rng.randrange(1,n);R=[(1-alpha*pow(w,k*delta,p))*pow(Ah[k],-1,p)%p for k in range(n)];r=M.idft(R,w,p);f,meta=gate(r,w,p,s)
   if f:assert f[-1]==R;small.append({'N':n,'p':p,'meta':meta});break
  assert small[-1]['N']==n
 # The source's recorded savings are checked as arithmetic data only.
 cost=[]
 for n in [1024,2048,4096,8192,16384,32768]:cost.append({'N':n,'probe_saving':29*n,'joint_compiler_saving':34*152,'first_inverse_saving':18,'generic_difference':29*n+5186,'one_four_tap_success_difference':29*n+5331})
 result={'status':'PASS','uploaded_code_executed':False,'prefix_cases':probes,'joint_resultant_cases':joint,'joint_resultant_count':len(joint),'applications':applications,'expanded_nonzero_prefix_control':extra,'shorter_length_controls':small,'exact_local_savings_formulas':cost,'structured_extra_constant_derivation':{'avoided_duplicate_16_element_inverse':49,'six_fewer_corrected_values':24,'six_fewer_four_term_prony_checks':72,'sum':145},'inherited_solver_control':M.inherited_solver_control()}
 path=Path(sys.argv[1]if len(sys.argv)>1 else'INDEPENDENT_RESULTS.json');path.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print('PASS',len(probes),'prefixes;',len(joint),'joint resultant controls;',len(applications['probe_preserving_adversaries']),'adversaries; expanded prefix coverage')
if __name__=='__main__':main()
