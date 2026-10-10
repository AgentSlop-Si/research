#!/usr/bin/env python3
"""Independent marked-cycle and first-Schur review. No submitted code imports."""
import json,math,random,sys
from pathlib import Path
import independent_math as M
rng=random.Random(100310)
def eye(n):return [[int(i==j)for j in range(n)]for i in range(n)]
def mm(A,B,p):return [[sum(x*y for x,y in zip(r,c))%p for c in zip(*B)]for r in A]
def mv(A,x,p):return [sum(a*b for a,b in zip(r,x))%p for r in A]
def add(A,B,p,c=1):return [[(a+c*b)%p for a,b in zip(r,s)]for r,s in zip(A,B)]
def scale(A,c,p):return [[v*c%p for v in r]for r in A]
def inv(A,p):
 n=len(A);cols=[M.solve(A,[int(i==j)for i in range(n)],p)for j in range(n)]
 if any(c is None for c in cols):return None
 return [list(r)for r in zip(*cols)]
def qdata(N,p,w):
 A0=[[0]*N for _ in range(N)];A1=[[0]*N for _ in range(N)]
 for j in range(N):A0[2*j%N][j]=1;A1[(2*j+1)%N][j]=pow(w,j,p)
 C=[[pow(w,i,p)*(int(j==i)-int(j==i+N//2))%p for j in range(N)]for i in range(N//2)]
 J=[[int(i==2*j+1)for j in range(N//2)]for i in range(N)]
 return A0,A1,add(A0,A1,p),C,J
def phi(r):
 s=0;prefix=0
 for b in bin(r)[2:]:s+=int(b)*prefix;prefix=2*prefix+int(b)
 return s
def rev(r,n):return int(format(r,'0'+str(n)+'b')[::-1],2)if n else 0
def Kmatrix(A0,n,z,p):
 N=len(A0);E=[[int(i==0)for _ in range(N)]for i in range(N)];A=eye(N);K=[[0]*N for _ in range(N)]
 for t in range(n):K=add(K,scale(add(A,E,p,-1),pow(z,t,p),p),p);A=mm(A0,A,p)
 assert A==E
 return K,E
def Kjet(x,p):
 N=len(x);n=N.bit_length()-1;rows=[]
 for j in range(N):rows.append([0]*(n if j==0 else (j&-j).bit_length()))
 for j in range(1,N):rows[j][0]=x[j]
 for h in range(n):
  for j in range(1<<h,N,1<<(h+1)):
   dest=2*j%N
   if dest:
    for k,v in enumerate(rows[j]):rows[dest][k+1]=(rows[dest][k+1]+v)%p
 for j in range(1,N):
  for k,v in enumerate(rows[j]):rows[0][k]=(rows[0][k]-v)%p
 assert sum(map(len,rows))==2*N-2
 return rows
def evaluate(rows,z,p):return [M.peval(r,z,p)for r in rows]
def state_step(state,bit,W,p):
 stride,c,vals=state;N=len(W);ns=min(2*stride,N);nc=(2*c+bit)%ns;out=[0]*(N//ns)
 for j,v in enumerate(vals):
  node=c+stride*j;dest=(2*node+bit)%N;idx=(dest-nc)//ns
  out[idx]=(out[idx]+v*(W[node]if bit else 1))%p
 return ns,nc,out
def slot_budget(N):
 n=N.bit_length()-1;sizes=[]
 for r in range(N):
  if r==0:sizes.append(2*n);continue
  t=(r&-r).bit_length()-1;v=r>>t;h=0
  while v&1:h+=1;v>>=1
  sizes.append(n+t+1 if r==N-(1<<t)else t+h+2)
 bound=5*N+(n*n-3*n-10)//2
 assert sum(sizes)==bound and bound<=6*N
 return sizes
def two_run(x,w,p):
 N=len(x);n=N.bit_length()-1;W=[pow(w,j,p)for j in range(N)];lam=pow(w,-1,p)
 out=[[0]*s for s in slot_budget(N)];series=[[0]*min(s,n+1)for s in slot_budget(N)];v=(1,0,x[:]);visits=0
 def put(rows,j,k,value):assert k<len(rows[j]);rows[j][k]=(rows[j][k]+value)%p
 for a in range(n+1):
  mass=sum(v[2])%p;y=v
  for b in range(n):
   stride,c,vals=y;visits+=len(vals);assert len(vals)==max(N//2**(a+b),1)
   for j,value in enumerate(vals):
    node=c+stride*j;put(out,node,a+b,value)
    if a<n:put(out,node,a+b+1,-lam*value)
    if a+b<=n:put(series,node,a+b,value)
   put(out,0,a+b,-mass)
   if a<n:put(out,0,a+b+1,lam*mass)
   if a+b<=n:put(series,0,a+b,-mass)
   y=state_step(y,0,W,p)
  v=state_step(v,1,W,p)
 assert visits==sum(max(N//2**(a+b),1)for a in range(n+1)for b in range(n)) and visits<4*N+n*n<=6*N
 # Independent full-length vector-power convolution oracle, intentionally uncompressed.
 aa=[x[:]]
 for a in range(1,n+1):
  v=[0]*N
  for j,z in enumerate(aa[-1]):v[(2*j+1)%N]=(v[(2*j+1)%N]+pow(w,j,p)*z)%p
  aa.append(v)
 expected=[[0]*(2*n)for _ in range(N)];truncated=[[0]*(n+1)for _ in range(N)]
 for a in range(n+1):
  numerator=[(aa[a][i]-(lam*aa[a-1][i]if a else 0))%p for i in range(N)]
  vals=numerator;orig=aa[a];mass=sum(vals)%p;omass=sum(orig)%p
  for b in range(n):
   for i in range(N):expected[i][a+b]=(expected[i][a+b]+vals[i]-mass*int(i==0))%p
   if a+b<=n:
    for i in range(N):truncated[i][a+b]=(truncated[i][a+b]+orig[i]-omass*int(i==0))%p
   vals=[sum(vals[j]for j in range(N)if 2*j%N==i)%p for i in range(N)]
   orig=[sum(orig[j]for j in range(N)if 2*j%N==i)%p for i in range(N)]
 for i in range(N):
  assert out[i]+[0]*(2*n-len(out[i]))==expected[i]
  assert series[i]+[0]*(n+1-len(series[i]))==truncated[i]
  for d in range(n+1):assert expected[i][d]==(truncated[i][d]-(lam*truncated[i][d-1]if d else 0))%p
 h=[rng.randrange(p)for _ in x];contract=[sum(h[i]*expected[i][d]for i in range(N))%p for d in range(2*n)]
 assert contract==[sum(h[i]*(out[i][d]if d<len(out[i])else 0)for i in range(N))%p for d in range(2*n)]
 return out,series,{'N':N,'p':p,'state_visits':visits,'full_numerator_slots':sum(map(len,out)),'series_slots':sum(map(len,series)),'degree_bound':2*n-1}
def haar(v,w,N,z,p):
 if len(v)==1:return [(2*z-1)*pow(1-z,-1,p)*v[0]%p]
 h=len(v)//2;child=haar([(v[j]+v[j+h])%p for j in range(h)],w*w%p,N//2,z,p);out=[0]*len(v)
 for j in range(h):out[2*j]=z*child[j]%p;out[2*j+1]=pow(w,2*j+1,p)*(v[j]-v[j+h])%p
 return out
def full_source_controls():
 cases=[];partial=traces=marks=jets=0;phasefails=0
 for N in [2,4,8,16,32]:
  p=65537;w=pow(3,(p-1)//N,p);n=N.bit_length()-1;A0,A1,Q,C,J=qdata(N,p,w);power=eye(N)
  for t in range(n+1):
   L=2**t;m=N//L
   expected=[[0]*N for _ in range(N)]
   for r in range(N):
    prefix,v=divmod(r,L)
    for a in range(L):s=a*m+prefix;expected[r][s]=pow(w,s*rev(v,t)+phi(v),p)
   assert power==expected;partial+=1
   if t==n:Qn=power
   power=mm(Q,power,p)
  F=[[pow(w,i*j,p)for j in range(N)]for i in range(N)]
  assert [[Qn[rev(k,n)][j]*pow(w,-phi(rev(k,n)),p)%p for j in range(N)]for k in range(N)]==F
  assert sum(phi(i)==0 for i in range(N))==n+1 and all(phi(i)<N for i in range(N))
  if N>=4:assert [Qn[rev(k,n)]for k in range(N)]!=F;phasefails+=1
  x=[rng.randrange(p)for _ in range(N)];v=[rng.randrange(p)for _ in range(N//2)];z=3
  G0=inv(add(eye(N),A0,p,-z),p);H=mm(mm(C,G0,p),J,p);assert mv(H,v,p)==haar(v,w,N,z,p)
  assert inv(H,p) is not None
  trace=[];power=eye(N)
  for k in range(1,n+3):
   power=mm(Q,power,p);truth=sum(power[j][j]for j in range(N))%p;acc=0
   for a in range(2**k):
    word=format(a,'0'+str(k)+'b');window=(word*((n+k-1)//k+2))[:n];s=int(window,2)
    emit=(word+word)[n%k:n%k+k];u=int(emit,2);acc+=pow(w,s*rev(u,k)+phi(u),p)
   assert acc%p==truth;trace.append(truth);traces+=1
  if N<=16:
   d=M.interp(list(range(N+1)),[M.determinant(add(eye(N),Q,p,-z),p)for z in range(N+1)],p);d+= [0]*(n+3-len(d))
   newton=[1]
   for j in range(1,n+3):newton.append(-sum(newton[j-k]*trace[k-1]for k in range(1,j+1))*pow(j,-1,p)%p)
   assert newton==d[:n+3];jets+=1
   h=[rng.randrange(p)for _ in range(N)];W=[r[:]+[x[i]]for i,r in enumerate(Q)]+[h+[0]]
   e=M.interp(list(range(N+2)),[M.determinant(add(eye(N+1),W,p,-z),p)for z in range(N+2)],p);e+=[0]*(n+3-len(e));quot=[]
   for j in range(n+3):quot.append((e[j]-sum(d[k]*quot[j-k]for k in range(1,j+1)))%p)
   target=sum(a*b for a,b in zip(h,mv(Qn,x,p)))%p;assert -quot[n+2]%p==target
   W0=[r[:]+[x[i]]for i,r in enumerate(Q)]+[[0]*(N+1)];W1=[[0]*(N+1)for _ in range(N)]+[h+[0]];base=eye(N+1);tan=[[0]*(N+1)for _ in range(N+1)]
   for _ in range(n+2):tan=add(mm(tan,W0,p),mm(base,W1,p),p);base=mm(base,W0,p)
   assert sum(tan[i][i]for i in range(N+1))*pow(n+2,-1,p)%p==target;marks+=1
  cases.append({'N':N,'online_additions':N*n,'online_multiplications':n*(N//2-1)+N-n-1})
 return {'stationary_cases':cases,'partial_matrix_identities':partial,'trace_identities':traces,'determinant_jets':jets,'marked_determinant_and_dual_trace_cases':marks,'omitted_phase_failures':phasefails}
def stage_case(N,p,w,z):
 n=N.bit_length()-1;m=N//2;A0,A1,Q,C,J=qdata(N,p,w);K,E=Kmatrix(A0,n,z,p)
 assert mm(add(eye(N),A0,p,-z),K,p)==add(eye(N),E,p,-1)
 assert all(K[i][0]==0 for i in range(N))and all(sum(K[i][j]for i in range(N))%p==0 for j in range(N))
 x=[rng.randrange(p)for _ in range(N)];kj=Kjet(x,p);assert evaluate(kj,z,p)==mv(K,x,p)
 H=mm(mm(C,K,p),J,p);B=[[(int(i==j)-z*H[i][j])%p for j in range(m)]+[-int(i==0)%p]for i in range(m)]+[[-z%p]*m+[(1-z)%p]]
 F=add(eye(N),Q,p,-z);det=M.determinant(F,p);assert M.determinant(B,p)==det
 record={'N':N,'p':p,'z':z,'full_determinant':det,'K_slots':sum(map(len,kj))}
 if det:
  f=mv(C,mv(K,x,p),p);rhs=f+[sum(x)%p];sol=M.solve(B,rhs,p);u,t=sol[:-1],sol[-1]
  y=[(a+z*b+t*int(i==0))%p for i,(a,b)in enumerate(zip(mv(K,x,p),mv(mm(K,J,p),u,p)))]
  assert y==M.solve(F,x,p)
  h=[rng.randrange(p)for _ in range(N)];ah=[z*sum(h[i]*K[i][2*j+1]for i in range(N))%p for j in range(m)]+[h[0]]
  assert sum(a*b for a,b in zip(h,y))%p==(sum(a*b for a,b in zip(h,mv(K,x,p)))+sum(a*b for a,b in zip(ah,sol)))%p
 if N<8:return record
 l=N//4;ev=list(range(0,m,2));od=list(range(1,m,2));blocks=lambda R,S:[[H[i][j]for j in S]for i in R]
 EE,EO,OE,OO=blocks(ev,ev),blocks(ev,od),blocks(od,ev),blocks(od,od)
 expectedOO=[[0]*l for _ in range(l)];expectedOE=[[0]*l for _ in range(l)]
 for j in range(l):expectedOO[(2*j+1)%l][j]=pow(w,4*j+3,p);expectedOE[2*j%l][j]=pow(w,4*j+1,p)
 assert OO==expectedOO and OE==expectedOE
 D=add(eye(l),OO,p,-z);q=(1-z*pow(w,-1,p))%p;assert M.determinant(D,p)==q;record['pivot_q']=q
 if not q:record['new_chart_declined']=True;return record
 Di=inv(D,p);fb=mm(mm(EO,Di,p),OE,p);S=add(add(eye(l),EE,p,-z),fb,p,-z*z)
 onesDi=[sum(Di[i][j]for i in range(l))%p for j in range(l)]
 red=[S[i]+[-int(i==0)%p]for i in range(l)]+[[(-z-z*z*sum(onesDi[k]*OE[k][j]for k in range(l)))%p for j in range(l)]+[(1-z)%p]]
 assert q*M.determinant(red,p)%p==det
 if det:
  fo=[f[i]for i in od];fe=[f[i]for i in ev];g=mv(Di,fo,p);rr=[(a+z*b)%p for a,b in zip(fe,mv(EO,g,p))]+[(sum(x)+z*sum(g))%p]
  ss=M.solve(red,rr,p);ee,tt=ss[:-1],ss[-1];oo=mv(Di,[(a+z*b)%p for a,b in zip(fo,mv(OE,ee,p))],p)
  assert [u[i]for i in ev]==ee and [u[i]for i in od]==oo and t==tt
  assert fo==[pow(w,2*j+1,p)*(x[2*j+1]-x[2*j+1+m])%p for j in range(l)]
 L=[[int(i==4*j+3)for j in range(l)]for i in range(N)];assert mm(A1,L,p)==mm(L,OO,p)
 if N==32 and p==65537 and z==1:
  odd2=list(range(1,l,2));control=[[S[i][j]for j in odd2]for i in odd2]
  assert control==[[1,0,0,0],[65535,513,2,65025],[16384,49153,16385,49153],[30151,50827,35386,14711]]
  record['next_pivot']=control;record['first_column_offdiagonal_nonzeros']=3
 return record
def additional_source_guards():
 controls=[]
 for N in [4,8,16]:
  p=65537;w=pow(3,(p-1)//N,p);n=N.bit_length()-1;A0,A1,Q,C,J=qdata(N,p,w)
  Qadj=list(map(list,zip(*qdata(N,p,pow(w,-1,p))[2])))
  assert mm(Qadj,Q,p)==scale(eye(N),2,p)
  for A,start,rows in [(A0,1,[2**j for j in range(n)]+[0]),(A1,0,[2**j-1 for j in range(n+1)]),(Q,0,[2**j-1 for j in range(n+1)])]:
   x=[int(i==start)for i in range(N)];cols=[]
   for j in range(n+1):cols.append(x);x=mv(A,x,p)
   minor=[[cols[j][i]for j in range(n+1)]for i in rows];assert M.determinant(minor,p)
  b=1<<n.bit_length();xi=pow(3,(p-1)//b,p);a=7;total=[[0]*N for _ in range(N)]
  for j in range(b):
   G=inv(add(eye(N),Q,p,-a*pow(xi,j,p)),p);assert G is not None
   total=add(total,scale(G,pow(xi,-j*n,p)*pow(b,-1,p)%p,p),p)
  Qn=eye(N);Qb=eye(N)
  for _ in range(n):Qn=mm(Qn,Q,p)
  for _ in range(b):Qb=mm(Qb,Q,p)
  rhs=scale(mm(Qn,inv(add(eye(N),Qb,p,-pow(a,b,p)),p),p),pow(a,n,p),p)
  assert total==rhs and total!=scale(Qn,pow(a,n,p),p)
  controls.append({'N':N,'alias_packet_size':b,'alias_denominator_required':True,'weighted_unitarity_identity':True,'three_Krylov_minors_nonzero':True})
 return controls
def main():
 source=full_source_controls();stages=[];two=[]
 for N in [2,4,8,16,32]:
  p=65537;w=pow(3,(p-1)//N,p)
  for z in [0,1,2,3]:stages.append(stage_case(N,p,w,z))
  if N>=8:stages.append(stage_case(N,p,w,w))
 for N in [8,16,32]:
  p=97;w=pow(5,(p-1)//N,p)
  for z in [0,1,3]:stages.append(stage_case(N,p,w,z))
 special=stage_case(2,3,2,1);assert special['full_determinant']==2
 # At the root pole the upper block M can be singular while the full border is invertible.
 _,_,_,C,J=qdata(2,3,2);K,_=Kmatrix(qdata(2,3,2)[0],1,1,3);assert add(eye(1),mm(mm(C,K,3),J,3),3,-1)==[[0]]
 for N in [2,4,8,16,32,64,128]:
  p=65537;w=pow(3,(p-1)//N,p)
  for kind in ['dense','lifted']:
   x=[rng.randrange(p)if kind=='dense'or i%4==3 else 0 for i in range(N)];out,ser,record=two_run(x,w,p);record['input_type']=kind;two.append(record)
   if N<=32:
    A0,A1,Q,C,J=qdata(N,p,w);z=3;K,_=Kmatrix(A0,N.bit_length()-1,z,p);y=M.solve(add(eye(N),A1,p,-z),x,p);q=(1-z*pow(w,-1,p))%p
    assert evaluate(out,z,p)==[q*a%p for a in mv(K,y,p)]
 simple=[]
 for n in range(1,7):
  N=2**n;count=0
  for a in range(N):
   for v in range(N):
    s=a;seen={s};ok=True
    for bit in format(v,'0'+str(n)+'b'):
     s=(2*s+int(bit))%N
     if s in seen:ok=False
     seen.add(s)
    count+=ok
  lower=max(0,N*N-math.comb(n+1,2)*N);assert count>=lower;simple.append({'N':N,'simple_paths':count,'proved_lower_bound':lower})
 for n in range(1,21):
  N=2**n;assert sum(max(N//2**(a+b),1)for a in range(n+1)for b in range(n))<4*N+n*n<=6*N
  formula=sum(k*(k+2)*2**(n-k-1)for k in range(1,n))+sum(n+t+1 for t in range(n))+2*n
  assert formula==5*N+(n*n-3*n-10)//2<=6*N
 result={'status':'PASS','uploaded_code_executed':False,'constructor_code_executed':False,'source_identity_controls':source,'additional_source_guards':additional_source_guards(),'pole_free_and_first_schur_cases':stages,'singular_M_invertible_border':special,'two_run_complete_numerators':two,'all_size_integer_bounds_checked_through_n':20,'simple_paths':simple,'source_haar_inverse_z1_guard':'static missing explicit guard; theorem domain excludes z=1','unresolved':'inverse of reduced border and polynomial-unknown feedback costs'}
 path=Path(sys.argv[1]if len(sys.argv)>1 else 'INDEPENDENT_RESULTS.json');path.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print('PASS',len(stages),'pole/Schur cases;',len(two),'complete two-run numerator controls')
if __name__=='__main__':main()
