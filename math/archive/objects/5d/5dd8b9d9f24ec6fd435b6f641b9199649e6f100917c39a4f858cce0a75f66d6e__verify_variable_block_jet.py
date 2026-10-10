#!/usr/bin/env python3
"""Authored exact quotient-frontier and b-bit Schur controls; no uploaded code."""
import json
from pathlib import Path
P=65537

def avoid_count(n,b):
 a=[]
 for t in range(n+1):a.append(2**t if t<b else sum(a[t-j]for j in range(1,b+1)))
 return a

def solve(A,b):
 n=len(b);a=[r[:]+[v]for r,v in zip(A,b)]
 for j in range(n):
  k=next(i for i in range(j,n)if a[i][j]);a[j],a[k]=a[k],a[j];iv=pow(a[j][j],-1,P);a[j]=[v*iv%P for v in a[j]]
  for i in range(n):
   if i!=j:
    t=a[i][j];a[i]=[(v-t*w)%P for v,w in zip(a[i],a[j])]
 return [r[-1]for r in a]
def mv(A,x):return [sum(a*b for a,b in zip(r,x))%P for r in A]
def mm(A,B):return [[sum(a*b for a,b in zip(r,c))%P for c in zip(*B)]for r in A]

def frontier(N,b,w,v):
 n=N.bit_length()-1;mod=2**b;active={s:v[s]for s in range(N)if s%mod};jets=[];sizes=[];work=0
 for t in range(n+1):
  jets.append(active.copy());sizes.append(len(active))
  if t==n:break
  nxt={}
  for s,value in active.items():
   for digit in (0,1):
    r=(2*s+digit)%N
    if r%mod:
     weight=1 if digit==0 else pow(w,s,P)
     nxt[r]=(nxt.get(r,0)+weight*value)%P;work+=1
  active=nxt
 a=avoid_count(n,b)
 exact=[2**(n-min(n,b+t))*a[min(n,b+t)]for t in range(n+1)]
 assert sizes==exact
 assert sum(sizes)<=N*min(n+1,2**(b+1)-2)
 assert 4*sum(sizes)>=N*min(n+1,2**b)
 if b==1:assert sum(sizes)==N
 if b==n:assert sum(sizes)==(n+1)*(N-1)
 return jets,sizes,work

def check(N,b):
 n=N.bit_length()-1;w=pow(3,(P-1)//N,P);M=N//2**b;R=list(range(0,N,2**b));E=[s for s in range(N)if s not in set(R)]
 Q=[[0]*N for _ in range(N)]
 for s in range(N):Q[2*s%N][s]=1;Q[(2*s+1)%N][s]=pow(w,s,P)
 QR=[[Q[i][j]for j in R]for i in R];EE=[[Q[i][j]for j in E]for i in E];RE=[[Q[i][j]for j in E]for i in R];ER=[[Q[i][j]for j in R]for i in E]
 x=[(7*s*s+11*s+3)%P for s in range(N)];h=[(3*s+5)%P for s in range(N)]
 jets,sizes,work=frontier(N,b,w,x);dense=[x[s]for s in E]
 for t,j in enumerate(jets):
  assert [j.get(s,0)for s in E]==dense
  assert sum(h[s]*j.get(s,0)for s in E)%P==sum(h[s]*v for s,v in zip(E,dense))%P
  dense=mv(EE,dense)
 basis_controls=0
 if N<=16:
  for j in range(N):
   xx=[int(i==j)for i in range(N)];jj,_,_=frontier(N,b,w,xx);dd=[xx[s]for s in E]
   for col in jj:
    assert [col.get(s,0)for s in E]==dd;dd=mv(EE,dd)
   basis_controls+=1
 # Fixed-z first-return Schur and the independent packet formula.
 fixed=0
 for z in (0,1):
  D=[[(int(i==j)-z*EE[i][j])%P for j in range(len(E))]for i in range(len(E))]
  # For z=1 some forbidden-subgraph pivots can be singular; keep that guard explicit.
  try:DI=list(map(list,zip(*(solve(D,[int(i==j)for i in range(len(E))])for j in range(len(E))))))
  except StopIteration:continue
  cross=mm(mm(RE,DI),ER);S=[[(int(i==j)-z*QR[i][j]-z*z*cross[i][j])%P for j in range(M)]for i in range(M)]
  rhs=[(x[s]+z*v)%P for s,v in zip(R,mv(RE,mv(DI,[x[s]for s in E])))]
  try:yR=solve(S,rhs)
  except StopIteration:continue
  yE=mv(DI,[(x[s]+z*v)%P for s,v in zip(E,mv(ER,yR))]);y=[0]*N
  for s,v in zip(R,yR):y[s]=v
  for s,v in zip(E,yE):y[s]=v
  assert [(y[i]-z*v)%P for i,v in enumerate(mv(Q,y))]==x
  # Packet matrix on the ones-ending interface.
  m=N//2;Pk=[[0]*m for _ in range(m)]
  for a in range(b):
   for j in range(m):
    dst=(2**(a+1)*j+2**a)%m
    Pk[dst][j]=(Pk[dst][j]+pow(z,a+1,P)*pow(w,2**a*(2*j+1),P))%P
  packet=[[(int(i==j)-Pk[i][j])%P for j in range(m)]for i in range(m)]
  try:PI=list(map(list,zip(*(solve(packet,[int(i==j)for i in range(m)])for j in range(m)))))
  except StopIteration:continue
  V=[[0]*m for _ in range(M)];W=[[0]*M for _ in range(m)]
  for j in range(m):V[(2*j+1)%M][j]=1
  for j in range(M):W[(2**b*j)%m][j]=pow(w,2**b*j,P)
  packcross=mm(mm(V,PI),W)
  assert S==[[(int(i==j)-z*QR[i][j]-pow(z,b+1,P)*packcross[i][j])%P for j in range(M)]for i in range(M)]
  marked0=sum(h[s]*v for s,v in zip(E,mv(DI,[x[s]for s in E])))%P
  markedrow=[(h[R[j]]+z*sum(h[E[i]]*mm(DI,ER)[i][j]for i in range(len(E))))%P for j in range(M)]
  assert sum(a*b for a,b in zip(h,y))%P==(marked0+sum(a*b for a,b in zip(markedrow,yR)))%P
  fixed+=1
 return {'basis_input_jet_checks':basis_controls,'N':N,'b':b,'retained_dimension':M,'packet_interface_dimension':N//2,'exact_frontier_sizes':sizes,'stored_jet_slots':sum(sizes),'weighted_edge_updates':work,'bound_N_min_logN_2powerb':N*min(n+1,2**(b+1)-2),'guarded_Schur_packet_marked_checks':fixed}

cases=[check(N,b)for N in (2,4,8,16,32,64)for b in range(1,N.bit_length())]
large=[]
for n in (8,16,32,64,128):
 b=n.bit_length()-1;a=avoid_count(n,b);N=2**n
 total=sum(2**(n-min(n,b+t))*a[min(n,b+t)]for t in range(n+1))
 large.append({'log2N':n,'b':b,'work_over_N_approx':total/N,'work_over_N_log2N_approx':total/(N*n)})
out={'field':P,'cases':cases,'count_only_large_cases':large,'all_exact_assertions_passed':True,'dense_solves_are_test_oracles_only':True,'uploaded_code_executed':False,'scope':'Exact one b-bit elimination and a charged constant-input eliminated-resolvent jet; no fast retained inverse or closed recursive family.'}
Path(__file__).with_name('VARIABLE_BLOCK_JET_CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'cases':len(cases),'basis_checks':sum(c['basis_input_jet_checks']for c in cases),'fixed_checks':sum(c['guarded_Schur_packet_marked_checks']for c in cases),'count_only_large_cases':large,'all_exact_assertions_passed':True},indent=2))
