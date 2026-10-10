"""Auditor-authored Phase24 graph, conjugation and lazy-certificate controls."""
from pathlib import Path
import json,random,itertools,math
import independent_phase21_math as M
import independent_trace_math as T
RNG=random.Random(240551)

def roots(n,p):
 w=pow(3,(p-1)//n,p);assert pow(w,n,p)==1 and pow(w,n//2,p)!=1
 W=[1]*n
 for j in range(1,n):W[j]=W[j-1]*w%p
 return w,W

def reverse(k,n):return int(format(k,'0'+str(n.bit_length()-1)+'b')[::-1],2)
class Schedule:
 # Independent flat-heap node state, separate primitive labels, in-place data.
 def __init__(self,x,W,p):
  self.a=x[:];self.W=W;self.p=p;self.N=len(x);self.state=[0]*(2*self.N);self.saved=[None]*(2*self.N);self.tags=set();self.adds=self.muls=self.current=self.peak=0;self.closed=False
 def operation(self,node,j,kind):
  tag=(node,j,kind);assert tag not in self.tags;self.tags.add(tag)
  if kind=='M':self.muls+=1
  else:self.adds+=1
 def prepare_branch(self,node,start,size,which):
  h=size//2;old=self.state[node]
  assert which&old==0
  if old==0 and which!=3:
   shift=0 if which==1 else h
   self.saved[node]=self.a[start+shift:start+shift+h];self.current+=h;self.peak=max(self.peak,self.current)
  for j in range(h):
   if old==1:u=self.saved[node][j];v=self.a[start+h+j]
   elif old==2:u=self.a[start+j];v=self.saved[node][j]
   else:u=self.a[start+j];v=self.a[start+h+j]
   if which&1:self.operation(node,j,'A');self.a[start+j]=(u+v)%self.p
   if which&2:
    self.operation(node,j,'D');self.operation(node,j,'M');self.a[start+h+j]=(u-v)*self.W[j*(self.N//size)]%self.p
  self.state[node]|=which
  if old and self.state[node]==3:self.saved[node]=None;self.current-=h
 def preview(self,Q):
  if self.closed:raise ValueError('preview after completed graph rejected in corrected lifecycle')
  Q=set(Q)
  if not Q or any(k<0 or k>=self.N for k in Q):raise ValueError('invalid queries')
  assert not any(self.state)
  stack=[(1,0,self.N,Q)]
  while stack:
   node,start,size,q=stack.pop()
   if size==1:continue
   h=size//2;groups=[{k//2 for k in q if k%2==bit} for bit in [0,1]];which=int(bool(groups[0]))+2*int(bool(groups[1]));self.prepare_branch(node,start,size,which)
   for bit in [1,0]:
    if groups[bit]:stack.append((2*node+bit,start+bit*h,h,groups[bit]))
  assert self.current==self.peak==self.N-len(Q)
  return {k:self.a[reverse(k,self.N)] for k in Q}
 def full(self):
  stack=[(1,0,self.N)]
  while stack:
   node,start,size=stack.pop()
   if size==1:continue
   if self.state[node]!=3:self.prepare_branch(node,start,size,3^self.state[node])
   h=size//2;stack.extend([(2*node+1,start+h,h),(2*node,start,h)])
  self.closed=True;assert self.current==0
  assert self.adds==self.N*(self.N.bit_length()-1) and self.muls==self.N//2*(self.N.bit_length()-1)
  return [self.a[reverse(k,self.N)] for k in range(self.N)]

def tree_count(N,Q):
 adds=muls=backups=eager=0;stack=[(N,set(Q))]
 while stack:
  size,q=stack.pop()
  if size==1:continue
  h=size//2;e={k//2 for k in q if not k%2};o={k//2 for k in q if k%2};eager+=3*h
  if e:adds+=h;stack.append((h,e))
  if o:adds+=h;muls+=h;stack.append((h,o))
  if bool(e)!=bool(o):backups+=h
 return {'adds':adds,'muls':muls,'backup':backups,'eager_arithmetic':eager}

def schedule_controls():
 count=0;basis=0
 for p in [257,65537]:
  for N in [2,4,8]:
   w,W=roots(N,p);x=[RNG.randrange(p) for _ in range(N)];truth=M.dft(x,w,p)
   for bits in range(1,2**N):
    Q=[j for j in range(N) if bits>>j&1];s=Schedule(x,W,p);v=s.preview(Q);c=tree_count(N,Q)
    assert all(v[k]==truth[k] for k in Q) and (s.adds,s.muls)==(c['adds'],c['muls']);assert s.full()==truth
    before=len(s.tags);assert s.full()==truth and len(s.tags)==before;count+=1
  for N in [16,32,64,128,256]:
   w,W=roots(N,p);x=[RNG.randrange(p) for _ in range(N)];truth=M.dft(x,w,p)
   qs=[[0],[N-1],list(range(N)),list(range(10))+[N-1]]+[RNG.sample(range(N),RNG.randrange(1,N+1)) for _ in range(12)]
   for Q in qs:
    s=Schedule(x,W,p);v=s.preview(Q);c=tree_count(N,Q);assert all(v[k]==truth[k] for k in Q);assert s.adds+s.muls==c['adds']+c['muls'];assert s.full()==truth;count+=1
   if N<=64:
    for j in range(N):
     x=[int(i==j) for i in range(N)];s=Schedule(x,W,p);Q=list(range(10))+[N-1];v=s.preview(Q);truth=[W[k*j%N] for k in range(N)];assert all(v[k]==truth[k] for k in Q);assert s.full()==truth;basis+=1
 formulas=[]
 for n in range(4,21):
  N=2**n;c=tree_count(N,list(range(10))+[N-1]);assert c['adds']+c['muls']==49*N//8-12 and c['eager_arithmetic']==129*N//16-33 and c['backup']==N-11
  assert 19*N-(c['adds']+c['muls']+30)==103*N//8-18
  formulas.append({'N':N,**c,'saving_vs_stream':103*N//8-18})
 # Static source lifecycle trace: full(e0) gives all ones; preview(0) then sums them.
 N=16;p=17;w,W=roots(N,p);s=Schedule([1]+[0]*(N-1),W,p);assert s.full()==[1]*N
 try:s.preview([0])
 except ValueError:pass
 else:raise AssertionError('corrected lifecycle failed')
 return {'query_set_cases':count,'basis_cases':basis,'formula_cases':formulas,'source_full_then_preview_counterexample':{'N':16,'p':17,'input':'e0','after_full':[1]*16,'source_subsequent_DC':16,'correct_DC':1,'corrected_guard_rejects':True}}

def matrices(N,W,p):
 L=[[(7+W[i])*int(i==j)+2*int(j==(i-1)%N) for j in range(N)] for i in range(N)]
 P=[[(7+2*W[-i%N])*int(i==j)+int(j==(i-1)%N) for j in range(N)] for i in range(N)]
 return L,P

def mult(A,x,p):return [sum(a*b for a,b in zip(row,x))%p for row in A]

def discover(R,loader,N,w,p,s=4):
 meta={'residual_calls':0,'full_checks':0,'failed_checks':0}
 if not all(R):return None,{**meta,'reason':'zero-probe'}
 inv=[pow(v,-1,p) for v in R];U=M.compress(inv,s,p)
 if not any(U):return None,{**meta,'reason':'zero-resultant'}
 b=s*(s+1)*(2*s+1)//6;V=T.trace_from_U(U,b,p);G,_=T.sieve(V,N,p);ds=T.enum_half(G,w,N,p) if len(G)>1 else []
 if not ds:return None,{**meta,'reason':'trace-gcd-one'}
 powers=[pow(w,j,p) for j in range(N)];r=None
 for delta in ds:
  g=M.pgcd(M.pencil(inv,powers[delta],0,s,p),M.pencil(inv,powers[delta],1,s,p),p)
  if len(g)!=2 or g[0]==0:continue
  alpha=-g[0]%p;Y=[v*(1-alpha*pow(w,k*delta,p))%p for k,v in enumerate(inv)];A=M.prony(Y,s,powers,p)
  if not A:continue
  Ah=M.sparse_eval(A,w,N,p)
  if not all(Ah):continue
  if r is None:r=loader();meta['residual_calls']+=1
  meta['full_checks']+=1;lhs=[sum(a*r[(j-e)%N] for e,a in A.items())%p for j in range(N)];rhs=[(int(j==0)-alpha*int(j==delta))%p for j in range(N)]
  if lhs!=rhs:meta['failed_checks']+=1;continue
  F=[(1-alpha*pow(w,k*delta,p))*pow(Ah[k],-1,p)%p for k in range(N)]
  assert F==M.dft(r,w,p)
  return F,{**meta,'reason':'accepted'}
 return None,{**meta,'reason':'full-certificate-failed' if meta['failed_checks'] else 'no-candidate'}

def integrated(x,w,p):
 N=len(x);W=[pow(w,j,p) for j in range(N)];L,P=matrices(N,W,p);session=Schedule(x,W,p);Q=list(range(10))+[N-1];Y=session.preview(Q)
 R=[((7+W[k])*Y[k]+2*Y[(k-1)%N])%p for k in range(10)]
 r=mult(P,x,p);assert R==M.dft(r,w,p,10)
 forcing,meta=discover(R,lambda:mult(P,x,p),N,w,p)
 if forcing is None:y=session.full()
 else:y=M.solve(L,forcing,p)
 assert y==M.dft(x,w,p)
 return meta

def integration_controls():
 out=[];accepted=[];adversaries=[];conjugation_basis=0
 for N in [16,32,64]:
  p,w=M.field(N);W=[pow(w,j,p) for j in range(N)];L,P=matrices(N,W,p);assert M.determinant(L,p) and M.determinant(P,p)
  for j in range(N):
   x=[int(i==j) for i in range(N)];assert M.dft(mult(P,x,p),w,p)==mult(L,M.dft(x,w,p),p);conjugation_basis+=1
  for trial in range(2):
   for tries in range(100):
    A={j:RNG.randrange(1,p) for j in [0,1,3,7]};Ah=M.sparse_eval(A,w,N,p)
    if not all(Ah):continue
    delta=trial+1;alpha=RNG.randrange(1,p);R=[(1-alpha*pow(w,k*delta,p))*pow(Ah[k],-1,p)%p for k in range(N)];r=M.idft(R,w,p);x=M.solve(P,r,p);meta=integrated(x,w,p)
    if meta['reason']=='accepted':break
   else:raise AssertionError('bounded positive fixture search failed')
   assert meta['residual_calls']==1;accepted.append({'N':N,'p':p,'meta':meta})
   bad=[(r[j]+pow(w,-10*j,p))%p for j in range(N)];assert M.dft(bad,w,p,10)==R[:10];xb=M.solve(P,bad,p);bm=integrated(xb,w,p)
   assert bm['reason']=='full-certificate-failed' and bm['residual_calls']==1 and bm['failed_checks']>=1;adversaries.append({'N':N,'p':p,'meta':bm})
  for trial in range(3):
   meta=integrated([RNG.randrange(p) for j in range(N)],w,p);out.append({'N':N,'p':p,'meta':meta})
  zero=integrated([0]*N,w,p);assert zero['reason']=='zero-probe' and zero['residual_calls']==0
 # Compatible-field engine domain hole, despite valid native graph and Green maps.
 N=16;p=17;w=3;W=[pow(w,j,p) for j in range(N)];L,P=matrices(N,W,p)
 assert M.determinant(L,p)==M.determinant(P,p)==16
 zerosL=[i for i in range(N) if L[i][i]%p==0];zerosP=[i for i in range(N) if P[i][i]%p==0];assert zerosL==[3] and zerosP==[11]
 x=[1]+[0]*15;assert M.solve(L,M.dft(mult(P,x,p),w,p),p)==M.dft(x,w,p)
 ss=Schedule(x,W,p);ss.preview(list(range(10))+[15]);assert ss.full()==[1]*16
 return {'conjugation_basis_controls':conjugation_basis,'accepted':accepted,'strict_ten_probe_adversaries':adversaries,'generic':out,'zero_cases':3,'compatible_engine_domain_counterexample':{'N':16,'p':17,'omega':3,'L_det':16,'P_det':16,'L_zero_diagonal':zerosL,'P_zero_diagonal':zerosP,'source_inv_all_error':'zero diagonal entry','native_fft_valid':True}}


def family_controls():
 out=[]
 for N,p in [(4,5),(8,17)]:
  images=set();parameters=0
  for j in range(N):
   for a in range(1,p):
    ai=pow(a,-1,p)
    for delta in range(1,N):
     for alpha in range(1,p):
      x=[0]*N;x[-j%N]=ai;x[(delta-j)%N]=-alpha*ai%p;images.add(tuple(x));parameters+=1
  bound=(N-1)*(p-1)*N*(p-1)
  assert parameters==bound and len(images)==math.comb(N,2)*(p-1)**2<=bound
  out.append({'N':N,'p':p,'s':1,'P':'identity','parameter_count':parameters,'distinct_family_inputs':len(images),'bound':bound})
 return out

if __name__=='__main__':
 result={'status':'passed','uploaded_code_executed':False,'schedule':schedule_controls(),'integration':integration_controls(),'family_count_controls':family_controls()}
 Path('INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'passed','query_set_cases':result['schedule']['query_set_cases'],'basis_cases':result['schedule']['basis_cases'],'integration':result['integration']},sort_keys=True))
