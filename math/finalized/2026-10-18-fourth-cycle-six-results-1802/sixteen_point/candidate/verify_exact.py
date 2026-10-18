"""Standalone exact verifier. Uses only the Python standard library.
The discovery code, SymPy, and historical programs are not imported.
"""
from pathlib import Path
from itertools import product
import json,hashlib,copy,math
BASE=Path(__file__).resolve().parent;N=16;P=97;ORDER=(1,3,7,5)

def plus(a,b,k=1,p=P):
 out=a.copy()
 for m,c in b.items():
  q=(out.get(m,0)+k*c)%p
  if q:out[m]=q
  else:out.pop(m,None)
 return out

def times(a,b,p=P):
 out={}
 for m,c in a.items():
  for n,d in b.items():
   e=tuple(x+y for x,y in zip(m,n));v=(out.get(e,0)+c*d)%p
   if v:out[e]=v
   else:out.pop(e,None)
 return out

def scaled(a,c,p=P):return {m:v*c%p for m,v in a.items() if v*c%p}
def shifted(a,n):return {tuple(x+y for x,y in zip(m,n)):v for m,v in a.items()}

def unpack(rows,n):
 out={}
 for m,c in rows:
  assert len(m)==n and all(isinstance(u,int) and u>=0 for u in m)
  m=tuple(m);assert m not in out and 0<c<P;out[m]=c
 return out

def equations(ns):
 n=sum(ns);one={(0,)*n:1};cs=[{} for _ in range(N)];cs[0]=one;var=0
 for stride,count in zip(ORDER,ns):
  ts=[(0,one)]
  for j in range(1,count+1):
   e=[0]*n;e[var]=1;var+=1;ts.append((stride*j,{tuple(e):1}))
  ds=[{} for _ in range(N)]
  for i,a in enumerate(cs):
   for k,b in ts:ds[(i+k)%N]=plus(ds[(i+k)%N],times(a,b))
  cs=ds
 return [plus(scaled(cs[i],(-1)**i),cs[i+8],-1) for i in range(8)]

def check_trace(d,mutate=False):
 assert d['N']==N and d['prime']==P and tuple(d['stride_order'])==ORDER
 ns=tuple(d['counts']);assert sum(ns)==7
 fs=equations(ns);known=[];terms=0
 for i,node in enumerate(d['nodes']):
  q=unpack(node['polynomial'],7);terms+=len(q);kind=node['kind']
  if kind=='input':
   assert i<8 and node['index']==i;v=fs[i]
  elif kind=='scale':
   j=node['source'];assert j<i;v=scaled(known[j],node['scale'])
  else:
   assert kind=='spair_reduce';a=node['left'];b=node['right'];assert 0<=a<i and 0<=b<i
   for e in (node['left_shift'],node['right_shift']):assert len(e)==7 and all(isinstance(t,int) and t>=0 for t in e)
   v=plus(shifted(known[a],node['left_shift']),shifted(known[b],node['right_shift']),-1)
   for j,packed in node['reductions']:
    assert 0<=j<i;v=plus(v,times(unpack(packed,7),known[j]),-1)
   v=scaled(v,node['scale'])
  assert v==q,('invalid derivation',ns,i)
  known.append(q)
 assert 0<=d['final']<len(known) and known[d['final']]=={(0,)*7:1}
 return len(known),terms

# Integral arithmetic in Z[a]/(a^16+1), independently constructed.
def cyc(c):
 out=[0]*16
 for i,v in enumerate(c):out[i%16]+=v*(-1)**(i//16)
 return out

def ringmul(a,b):
 c=[0]*31
 for i,v in enumerate(a):
  for j,w in enumerate(b):c[i+j]+=v*w
 return cyc(c)
def ringadd(a,b):return [u+v for u,v in zip(a,b)]
def apow(k):
 k%=32;c=[0]*16;c[k%16]=(-1)**(k//16);return c

def check_matrix():
 C=[[apow(-((i-j)%16)**2) for j in range(16)] for i in range(16)]
 Q=[[apow(((i-j)%16)**2) for j in range(16)] for i in range(16)]
 for i in range(16):
  for j in range(16):
   v=[0]*16
   for k in range(16):v=ringadd(v,ringmul(C[i][k],Q[k][j]))
   assert v==[16*int(i==j)]+[0]*15
 # Full parity and gauge-shift identities, needed by the normalization.
 q=[apow(t*t) for t in range(16)]
 for t in range(16):assert [(-1)**t*u for u in q[t]]==q[(t-8)%16]
 for r in range(16):
  for t in range(16):assert q[(t-r)%16]==ringmul(apow(r*r-2*r*t),q[t])
 # A wrong target entry must fail the same exact matrix identity.
 C[0][0][0]+=1;bad=[0]*16
 for k in range(16):bad=ringadd(bad,ringmul(C[0][k],Q[k][0]))
 assert bad!=[16]+[0]*15
 return {'matrix_entries':256,'parity_coefficients':16,'shift_coefficients':256,'corrupted_target_rejected':True}

def apply_resolvent(v,alpha,p):
 n=len(v);mult=adds=0;h=v[0]
 for x in v[1:]:h=(alpha*h+x)%p;mult+=1;adds+=1
 d=pow((1-pow(alpha,n,p))%p,-1,p);out=v.copy();out[-1]=d*h%p;mult+=1
 for i in range(n-1):out[i]=(v[i]+alpha*out[i-1])%p;mult+=1;adds+=1
 return out,mult,adds

def check_application():
 count=0
 for a in range(97):
  if pow(a,16,97)==1:continue
  for j in range(16):
   v=[int(k==j) for k in range(16)];w,m,b=apply_resolvent(v,a,97)
   assert (m,b)==(31,30)
   assert [(w[k]-a*w[k-1])%97 for k in range(16)]==v;count+=1
 return {'basis_applications':count,'multiplications_per_factor':31,'additions_per_factor':30}

def trim(a):
 while len(a)>1 and a[-1]%P==0:a.pop()
 return [c%P for c in a]
def pmul(a,b):
 r=[0]*(len(a)+len(b)-1)
 for i,c in enumerate(a):
  for j,d in enumerate(b):r[i+j]=(r[i+j]+c*d)%P
 return trim(r)
def prem(a,b):
 a=trim(a.copy());b=trim(b.copy());ib=pow(b[-1],-1,P)
 while len(a)>=len(b) and a!=[0]:
  c=a[-1]*ib%P;d=len(a)-len(b)
  for i,t in enumerate(b):a[i+d]=(a[i+d]-c*t)%P
  a=trim(a)
 return a
def ppow(a,n,m):
 r=[1]
 while n:
  if n&1:r=prem(pmul(r,a),m)
  a=prem(pmul(a,a),m);n//=2
 return r
def pgcd(a,b):
 while b!=[0]:a,b=b,prem(a,b)
 return [(v*pow(a[-1],-1,P))%P for v in a]
def psub(a,b):
 r=[0]*max(len(a),len(b))
 for i,c in enumerate(a):r[i]+=c
 for i,c in enumerate(b):r[i]-=c
 return trim(r)
def check_finite_upper():
 a=19;zeta=46;assert a*zeta%P==1 and pow(a,16,P)==96
 factors=[[78,1],[19,65,43,1],[77,57,71,1],[50,5,51,7,1],[50,18,67,64,1]]
 out=[19]
 for f in factors:out=pmul(out,f)
 q=[pow(a,t*t,P) for t in range(16)];assert out==q
 for f in factors:
  d=len(f)-1
  assert ppow([0,1],P**d,f)==prem([0,1],f)
  for r in range(1,d//2+1):
   assert pgcd(psub(ppow([0,1],P**r,f),[0,1]),f)==[1]
 assert pgcd(q,[96]+[0]*15+[1])==[1]
 return {'a':19,'zeta':46,'monic_factor_degrees':[1,3,3,4,4],'splitting_degree_lcm':12,'factorization_and_irreducibility':'PASS','pole_gcd':'1','resolvent_count':15}

def main():
 files=sorted((BASE/'parity7_traces').glob('*.json'));expected={ns for ns in product(range(8),repeat=4) if sum(ns)==7 and ns==max(ns[k:]+ns[:k] for k in range(4))}
 seen=set();nodes=terms=0;mutations=0;input_mutations=0
 for f in files:
  d=json.loads(f.read_text());ns=tuple(d['counts']);assert ns not in seen;seen.add(ns);nn,tt=check_trace(d);nodes+=nn;terms+=tt
  damaged=copy.deepcopy(d);damaged['nodes'][damaged['final']]['polynomial'][0][1]=2
  try:check_trace(damaged)
  except AssertionError:mutations+=1
  else:raise AssertionError('corrupted final certificate accepted')
  damaged=copy.deepcopy(d);damaged['nodes'][0]['polynomial'][0][1]=(damaged['nodes'][0]['polynomial'][0][1]+1)%97
  try:check_trace(damaged)
  except AssertionError:input_mutations+=1
  else:raise AssertionError('corrupted defining equation accepted')
 assert seen==expected,(len(seen),len(expected),expected-seen)
 allpatterns=[ns for ns in product(range(8),repeat=4) if sum(ns)==7]
 assert len(allpatterns)==120 and len(expected)==30
 for ns in allpatterns:assert max(ns[k:]+ns[:k] for k in range(4)) in seen
 # Root assumptions and the projective zero-count premises at the reduction prime.
 roots=[t for t in range(97) if pow(t,16,97)==1];assert len(roots)==16
 signfix=[t for t in roots if pow(t,8,97)==96];assert len(signfix)==8
 zero_cases=0
 for s in range(1,16,2):
  assert len({pow(t,s,97) for t in roots})==16
  for u in range(97):
   for v in range(97):
    if u==v==0:continue
    assert sum((u+v*pow(t,s,97))%97==0 for t in roots)<=1;zero_cases+=1
 result={'status':'PASS','prime':97,'seven_factor_count_vectors':120,'rotation_representatives':30,'derivation_nodes':nodes,'stored_node_terms':terms,'corrupted_certificate_controls_rejected':mutations,'corrupted_input_controls_rejected':input_mutations,'root_count':16,'sign_fix_roots':8,'projective_binomial_zero_count_controls':zero_cases,'full_matrix_and_normalization':check_matrix(),'application_controls':check_application(),'finite_upper':check_finite_upper(),'scope':'At least eight odd-stride factors, hence at least eight total stages, at N=16 in characteristic zero and characteristic 97; upper fifteen retained in the declared splitting fields.'}
 (BASE/'CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
