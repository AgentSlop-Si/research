"""Auditor-authored Good-Thomas, optimized schedule, codelet and entropy checks."""
import json,itertools,random,cmath,math
from pathlib import Path
import independent_phase24_math as H
import independent_phase21_math as M
RNG=random.Random(251778)
class Tight(H.Schedule):
 def prepare_branch(self,node,start,size,which):
  h=size//2;old=self.state[node];assert which&old==0
  if old==0 and which!=3:
   shift=0 if which==1 else h;self.saved[node]=self.a[start+shift:start+shift+h];self.current+=h;self.peak=max(self.current,self.peak)
  for j in range(h):
   if old==1:u,v=self.saved[node][j],self.a[start+h+j]
   elif old==2:u,v=self.a[start+j],self.saved[node][j]
   else:u,v=self.a[start+j],self.a[start+h+j]
   if which&1:self.operation(node,j,'A');self.a[start+j]=(u+v)%self.p
   if which&2:
    self.operation(node,j,'D');difference=(u-v)%self.p
    if j:self.operation(node,j,'M');difference=difference*self.W[j*(self.N//size)]%self.p
    self.a[start+h+j]=difference
  self.state[node]|=which
  if old and self.state[node]==3:self.current-=h;self.saved[node]=None
 def full(self):
  stack=[(1,0,self.N)]
  while stack:
   node,start,size=stack.pop()
   if size==1:continue
   if self.state[node]!=3:self.prepare_branch(node,start,size,3^self.state[node])
   h=size//2;stack.extend([(2*node,start,h),(2*node+1,start+h,h)])
  self.closed=True;assert self.current==0
  t=self.N.bit_length()-1;assert self.adds==self.N*t and self.muls==self.N//2*t-self.N+1
  return [self.a[H.reverse(k,self.N)] for k in range(self.N)]
class Triple:
 def __init__(self,a,b,c,eta,p,omit_extra_identity=False):
  self.val={'a':a,'b':b,'c':c};self.p=p;half=pow(2,-1,p);self.u=-half%p;self.v=(eta-eta*eta)*half%p;self.adds=self.muls=0;self.opt=omit_extra_identity
 def get(self,name):
  if isinstance(name,int):name='y'+str(name)
  if name in self.val:return self.val[name]
  def plus(a,b,sgn=1):self.adds+=1;return (self.get(a)+sgn*self.get(b))%self.p
  def mul(c,a):
   if self.opt and c==1:return self.get(a)
   self.muls+=1
   return c*self.get(a)%self.p
  if name=='t':v=plus('b','c')
  elif name=='d':v=plus('b','c',-1)
  elif name=='u':v=mul(self.u,'t')
  elif name=='mid':v=plus('a','u')
  elif name=='z':v=mul(self.v,'d')
  elif name=='y0':v=plus('a','t')
  elif name=='y1':v=plus('mid','z')
  elif name=='y2':v=plus('mid','z',-1)
  else:raise AssertionError(name)
  self.val[name]=v;return v
 def full(self):return [self.get(k) for k in range(3)]

def table(n,w,p):
 x=[1]*n
 for j in range(1,n):x[j]=x[j-1]*w%p
 return x
class GT:
 def __init__(self,x,w,p):
  self.N=len(x);self.G=self.N//3;self.w=w;self.p=p;G=self.G;assert G>=2 and G&(G-1)==0
  self.a=pow(3,-1,G);self.b=pow(G,-1,3);self.e=pow(w,G,p);self.W=table(G,pow(w,3,p),p)
  self.rows=[Tight([x[(3*self.a*j+G*self.b*k)%self.N] for j in range(G)],self.W,p) for k in range(3)];self.tr={};self.done=False
 def coords(self,k):return k*self.a%self.G,k*self.b%3
 def code(self,j,vals):
  if j not in self.tr:self.tr[j]=Triple(*[vals[r][j] for r in range(3)],self.e,self.p)
  return self.tr[j]
 def preview(self,Q):
  if self.done:raise ValueError('completed graph')
  J={self.coords(k)[0] for k in Q};vals=[r.preview(J) for r in self.rows]
  out={k:self.code(self.coords(k)[0],vals).get(self.coords(k)[1]) for k in Q}
  assert sum(r.peak for r in self.rows)==self.N-3*len(J)
  return out
 def full(self):
  vals=[r.full() for r in self.rows];out=[0]*self.N
  for j in range(self.G):
   y=self.code(j,vals).full()
   for k in range(3):out[(3*j+self.G*k)%self.N]=y[k]
  self.done=True;assert self.cost()==9*self.G*(self.G.bit_length()-1)//2+5*self.G+3
  return out
 def cost(self):return sum(r.adds+r.muls for r in self.rows)+sum(t.adds+t.muls for t in self.tr.values())

def CT(x,w,p):
 N=len(x);G=N//3;W=table(G,pow(w,3,p),p);cost=0;row=[]
 for k in range(3):
  s=Tight(x[k::3],W,p);row.append(s.full());cost+=s.adds+s.muls
 out=[0]*N;eta=pow(w,G,p)
 for j in range(G):
  a,b,c=(row[k][j] for k in range(3))
  if j:b=b*pow(w,j,p)%p;c=c*pow(w,2*j,p)%p;cost+=2
  tr=Triple(a,b,c,eta,p);v=tr.full();cost+=tr.adds+tr.muls
  for k in range(3):out[j+G*k]=v[k]
 return out,cost

def root(N,p,g):
 w=pow(g,(p-1)//N,p);assert (p-1)%N==0 and pow(w,N,p)==1 and pow(w,N//2,p)!=1 and pow(w,N//3,p)!=1;return w

def algebra():
 rows=[];basis=0;subset=0;badlayout=0
 for p,g,lengths in [(97,5,[6,12,24,48,96]),(2013265921,31,[6,12,24,48,96,192])]:
  for N in lengths:
   w=root(N,p,g);x=[RNG.randrange(p) for _ in range(N)];truth=M.dft(x,w,p);G=N//3
   queries=[[0],[N-1],list(range(N)),list(range(min(10,N)))+[N-1]]
   if N==6:queries += [[k for k in range(N) if mask>>k&1] for mask in range(1,2**N)]
   else:queries += [RNG.sample(range(N),RNG.randrange(1,N+1)) for _ in range(10)]
   for Q in queries:
    s=GT(x,w,p);v=s.preview(set(Q));assert all(v[k]==truth[k] for k in Q);assert s.full()==truth;cost=s.cost();assert s.full()==truth and s.cost()==cost;subset+=1
   ct,c=CT(x,w,p);assert ct==truth and c-cost==2*(G-1)
   if N<=96:
    for j in range(N):
     x=[int(i==j) for i in range(N)];s=GT(x,w,p);Q=list(range(min(10,N)))+[N-1];v=s.preview(set(Q));target=[pow(w,j*k,p) for k in range(N)];assert all(v[k]==target[k] for k in Q);assert s.full()==target;basis+=1
   # Correct input/output CRT maps must not be interchanged.
   f=GT(list(range(N)),w,p);actual=f.full();wrong=[0]*N
   for j in range(G):
    for k in range(3):wrong[(3*f.a*j+G*f.b*k)%N]=f.tr[j].get(k)
   if wrong!=actual:badlayout+=1
   rows.append({'N':N,'p':p,'GT':cost,'CT':c,'saving':c-cost})
 # Exceptional field coefficient equals 1, despite the declared skip-one model.
 N=6;p=7;w=5;eta=pow(w,2,p);assert eta==4
 tr=Triple(1,2,3,eta,p);tc=Triple(1,2,3,eta,p,True);assert tr.full()==tc.full()==M.dft([1,2,3],eta,p)
 assert (tr.adds,tr.muls)==(6,2) and (tc.adds,tc.muls)==(6,1)
 s=GT(list(range(N)),w,p);assert s.full()==M.dft(list(range(N)),w,p);assert s.cost()==22
 return {'cases':rows,'full_basis_vectors':basis,'query_set_cases':subset,'wrong_output_CRT_controls':badlayout,'identity_codelet_exception':{'N':6,'p':7,'primitive_root':5,'eta':eta,'coefficient':tr.v,'literal_source_codelet_cost':8,'skip_all_identity_cost':7,'literal_full_GT':22,'skip_all_identity_full_GT':20}}

def codelets():
 count=0
 for p,eta in [(7,2),(7,4),(13,3),(97,35),(2013265921,pow(31,(2013265921-1)//3,2013265921))]:
  assert eta!=1 and pow(eta,3,p)==1
  for _ in range(5):
   a=[RNG.randrange(p) for k in range(3)];truth=M.dft(a,eta,p)
   for order in itertools.permutations(range(3)):
    tr=Triple(*a,eta,p)
    for k in order:assert tr.get(k)==truth[k]
    before=tr.adds+tr.muls;assert tr.full()==truth and tr.adds+tr.muls==before==8;count+=1
 return count

def integrate(x,w,p):
 N=len(x);W=table(N,w,p);L,P=H.matrices(N,W,p);s=GT(x,w,p);q=list(range(10))+[N-1];v=s.preview(q)
 prefix=[((7+W[k])*v[k]+2*v[(k-1)%N])%p for k in range(10)]
 assert prefix==M.dft(H.mult(P,x,p),w,p,10)
 forcing,meta=H.discover(prefix,lambda:H.mult(P,x,p),N,w,p)
 y=s.full() if forcing is None else M.solve(L,forcing,p)
 assert y==M.dft(x,w,p);return meta

def integrations():
 out=[]
 for N in [12,24,48]:
  p,w=M.field(N);W=table(N,w,p);L,P=H.matrices(N,W,p);assert M.determinant(P,p) and M.determinant(L,p)
  for trial in range(100):
   A={j:RNG.randrange(1,p) for j in [0,1,3,7]};Ah=M.sparse_eval(A,w,N,p)
   if not all(Ah):continue
   alpha=RNG.randrange(1,p);R=[(1-alpha*pow(w,k,p))*pow(Ah[k],-1,p)%p for k in range(N)];r=M.idft(R,w,p);x=M.solve(P,r,p);pos=integrate(x,w,p)
   if pos['reason']=='accepted':break
  else:raise AssertionError('fixture search')
  bad=[(r[j]+pow(w,-10*j,p))%p for j in range(N)];neg=integrate(M.solve(P,bad,p),w,p);assert neg['failed_checks']==2 and neg['residual_calls']==1
  generic=integrate([RNG.randrange(p) for j in range(N)],w,p);assert generic['reason']!='accepted'
  out.append({'N':N,'p':p,'accepted':pos,'adversary':neg,'generic':generic})
 # Mixed-length Green constructor hole; GT remains valid.
 N=12;p=13;w=2;W=table(N,w,p);L,P=H.matrices(N,W,p);assert M.determinant(L,p)==M.determinant(P,p)==12
 zL=[i for i in range(N) if L[i][i]%p==0];zP=[i for i in range(N) if P[i][i]%p==0];assert zL==[5] and zP==[8]
 s=GT([1]+[0]*11,w,p);assert s.full()==[1]*12
 return {'cases':out,'Green_constructor_hole':{'N':12,'p':13,'omega':2,'L_det':12,'P_det':12,'L_zero_diagonal':zL,'P_zero_diagonal':zP}}

def entropy():
 rows=[]
 for N in [2,4,8,16,32]:
  A=[[complex(i==j) for j in range(N)] for i in range(N)];levels=[0.0];steps=[];size=N
  phi=lambda X:-sum(abs(z)**2*math.log2(abs(z)**2) for r in X for z in r if abs(z)>1e-13)
  while size>1:
   h=size//2
   for start in range(0,N,size):
    for j in range(h):
     before=phi(A);u=A[start+j][:];v=A[start+h+j][:];phase=cmath.exp(-2j*math.pi*j/size)
     A[start+j]=[(a+b)/math.sqrt(2) for a,b in zip(u,v)];A[start+h+j]=[phase*(a-b)/math.sqrt(2) for a,b in zip(u,v)];change=phi(A)-before;assert abs(change-2)<1e-9;steps.append(change)
   levels.append(phi(A));size=h
  F=[[cmath.exp(-2j*math.pi*i*j/N)/math.sqrt(N) for j in range(N)] for i in range(N)]
  error=max(abs(A[H.reverse(i,N)][j]-F[i][j]) for i in range(N) for j in range(N));assert error<1e-12
  if N>=4:assert any(abs(A[i][j]-F[i][j])>1e-3 for i in range(N) for j in range(N))
  assert all(abs(v-N*i)<1e-9 for i,v in enumerate(levels))
  rows.append({'N':N,'gate_count':len(steps),'levels':levels,'canonical_F_requires_output_bitreversal':N>=4,'max_reordered_error':error})
 return rows

if __name__=='__main__':
 out={'status':'passed','uploaded_code_executed':False,'GT_CT':algebra(),'codelet_order_cases':codelets(),'integration':integrations(),'entropy':entropy()}
 Path('INDEPENDENT_RESULTS.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'passed','GT_CT':out['GT_CT'],'codelet_order_cases':out['codelet_order_cases'],'integration':out['integration']},sort_keys=True))
