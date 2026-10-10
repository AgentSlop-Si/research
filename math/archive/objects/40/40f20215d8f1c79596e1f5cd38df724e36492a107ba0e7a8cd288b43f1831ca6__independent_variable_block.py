"""Fresh finite-horizon/packet audit with deterministic table-driven frontiers."""
from independent_linear import *
from pathlib import Path
from fractions import Fraction
import json

def automaton(n,b):
 # Independent word counter by trailing-zero automaton, not b-step recurrence.
 states=[1]+[0]*(b-1);counts=[1]
 for t in range(n):states=[sum(states)]+states[:-1];counts.append(sum(states))
 return counts

def frontier(x,h,b,W,p):
 N=len(x);n=N.bit_length()-1;mod=2**b
 values=x[:];nxt=[0]*N;stamp=[-1]*N;active=[s for s in range(N) if s%mod];jets=[];contractions=[];sizes=[];edges=weighted=merges=firstvisits=0
 for L in range(n+1):
  jets.append([(s,values[s]) for s in active]);sizes.append(len(active));contractions.append(sum(h[s]*values[s] for s in active)%p)
  if L==n:break
  next_active=[]
  for s in active:
   for digit in [0,1]:
    t=(2*s+digit)%N
    if t%mod==0:continue
    edges+=1
    if stamp[t]!=L:stamp[t]=L;nxt[t]=0;next_active.append(t);firstvisits+=1
    value=values[s]
    if digit:value=value*W[s]%p;weighted+=1
    nxt[t]=(nxt[t]+value)%p;merges+=1
  values,nxt=nxt,values;active=next_active
 return jets,contractions,{'sizes':sizes,'coefficient_slots':sum(sizes),'valid_edge_updates':edges,'weighted_multiplications':weighted,'merge_additions':merges,'new_target_initializations':firstvisits,'marker_multiplications':sum(sizes),'marker_additions':sum(sizes),'one_time_value_and_stamp_slots':3*N,'length_N_reinitializations_per_level':0}

def check_jet(N,b,p):
 n=N.bit_length()-1;w,W=root_table(N,p);r=list(range(0,N,2**b));e=[s for s in range(N) if s%2**b];Q=qmatrix(N,W,p);EE=block(Q,e,e)
 x=[(13*s*s+19*s+7)%p for s in range(N)];h=[(5*s*s+11)%p for s in range(N)]
 jets,marks,ledger=frontier(x,h,b,W,p);v=[x[s] for s in e];a=automaton(n,b);expected=[2**(n-min(n,b+L))*a[min(n,b+L)] for L in range(n+1)]
 assert ledger['sizes']==expected
 for L,items in enumerate(jets):
  vals=dict(items);assert [vals.get(s,0) for s in e]==v;assert dot([h[s] for s in e],v,p)==marks[L]
  d=min(n,b+L);mask=2**d-1;eligible=[s for s in range(N) if '0'*b not in format(s&mask,'0'+str(d)+'b')]
  assert sorted(vals)==eligible
  v=mv(EE,v,p)
 S=sum(expected);assert S<=N*min(n+1,2**(b+1)-2) and 4*S>=N*min(n+1,2**b)
 assert S==N*sum(Fraction(a[t],2**t) for t in range(b,n))+(b+1)*a[n]
 if b==1:assert S==N
 if b==n:assert S==(n+1)*(N-1)
 basis=0
 if N<=16:
  for j in range(N):
   xx=[int(s==j) for s in range(N)];jj,mmark,_=frontier(xx,h,b,W,p);dd=[xx[s] for s in e]
   for L,items in enumerate(jj):
    vals=dict(items);assert [vals.get(s,0) for s in e]==dd;assert mmark[L]==dot([h[s] for s in e],dd,p);dd=mv(EE,dd,p)
   basis+=1
 return {'N':N,'b':b,'p':p,'basis_controls':basis,'root_table_multiplications':N-1,'ledger':ledger}

def packet(N,b,W,z,p):
 m=N//2;r=N//2**b;P=[[0]*m for _ in range(m)];branches=[]
 for a in range(b):
  T=[[0]*m for _ in range(m)]
  for j in range(m):T[(2**(a+1)*j+2**a)%m][j]=W[(2**a*(2*j+1))%N]
  branches.append(T);P=add(P,T,p,pow(z,a+1,p))
 V=[[0]*m for _ in range(r)];Wmap=[[0]*r for _ in range(m)]
 for j in range(m):V[(2*j+1)%r][j]=1
 for j in range(r):Wmap[(2**b*j)%m][j]=W[(2**b*j)%N]
 return add(eye(m),P,p,-1),V,Wmap,branches

def scalar_case(N,b,p,z):
 w,W=root_table(N,p);Q=qmatrix(N,W,p);R=list(range(0,N,2**b));E=[s for s in range(N) if s%2**b];rr=len(R);ee=len(E)
 QR=block(Q,R,R);RE=block(Q,R,E);ER=block(Q,E,R);EE=block(Q,E,E);D=add(eye(ee),EE,p,-z);DI=inverse(D,p)
 P,V,Wmap,branches=packet(N,b,W,z,p);dp=det(P,p);dd=det(D,p);assert dd==dp
 branchguards=[det(add(eye(N//2),T,p,-pow(z,a+1,p)),p) for a,T in enumerate(branches)]
 full=add(eye(N),Q,p,-z);dfull=det(full,p)
 row={'N':N,'b':b,'p':p,'z':z,'D_determinant':dd,'packet_determinant':dp,'full_determinant':dfull,'individual_branch_determinants':branchguards}
 if DI is None:row['chart']='eliminated_zero';return row
 PI=inverse(P,p);assert PI is not None
 S=add(add(eye(rr),QR,p,-z),mm(mm(RE,DI,p),ER,p),p,-z*z)
 S2=add(add(eye(rr),QR,p,-z),mm(mm(V,PI,p),Wmap,p),p,-pow(z,b+1,p));assert S==S2
 assert det(full,p)==dd*det(S,p)%p
 SI=inverse(S,p)
 if SI is None:row['chart']='retained_zero';return row
 x=[(s*s+13*s+5)%p for s in range(N)];h=[(17*s*s+9)%p for s in range(N)]
 dx=mv(DI,[x[s] for s in E],p);rhs=[(x[s]+z*v)%p for s,v in zip(R,mv(RE,dx,p))];yr=mv(SI,rhs,p)
 ye=mv(DI,[(x[s]+z*v)%p for s,v in zip(E,mv(ER,yr,p))],p);y=[0]*N
 for s,v in zip(R,yr):y[s]=v
 for s,v in zip(E,ye):y[s]=v
 assert mv(full,y,p)==x
 left=mm(DI,ER,p);marker=[(h[R[j]]+z*sum(h[E[i]]*left[i][j] for i in range(ee)))%p for j in range(rr)]
 assert dot(h,y,p)==(dot([h[s] for s in E],dx,p)+dot(marker,yr,p))%p
 row['chart']='guarded_solve';return row

def count_only():
 rows=[];total=0
 for n in list(range(1,25))+[32,64,128,256,512]:
  bs=range(1,n+1) if n<=24 else sorted(set([1,2,3,5,n.bit_length()-1,n]))
  for b in bs:
   N=2**n;a=automaton(n,b)
   for t in range(n+1):assert a[t]==(2**t if t<b else sum(a[t-j] for j in range(1,b+1)))
   S=sum(2**(n-min(n,b+L))*a[min(n,b+L)] for L in range(n+1));assert S<=N*min(n+1,2**(b+1)-2) and 4*S>=N*min(n+1,2**b)
   # Rational generating-function value, including b=1.
   numerator=sum(Fraction(1,2**j) for j in range(b));denominator=1-sum(Fraction(1,2**j) for j in range(1,b+1));assert numerator/denominator==2**(b+1)-2
   if b==1:assert S==N
   if b==n:assert S==(n+1)*(N-1) and sum(a)==2*N-2
   total+=1
   if n>=8 and b==n.bit_length()-1:rows.append({'n':n,'b':b,'S':S,'N':N,'ratio_numerator':S,'ratio_denominator':N*n})
 return {'exact_integer_cases':total,'loglog_scale_examples':rows}

if __name__=='__main__':
 jets=[check_jet(N,b,p) for p in [257,65537] for N in [2,4,8,16,32,64,128] for b in range(1,N.bit_length())]
 scalar=[scalar_case(N,b,p,z) for p in [257,65537] for N in [2,4,8,16,32] for b in range(1,N.bit_length()) for z in [0,1,2]]
 for N in [8,16,32]:
  p=65537;w,_=root_table(N,p);scalar.append(scalar_case(N,1,p,w))
 # Search only a bounded exact control for the insufficiency of separate guards.
 badbranches=[]
 for N,b,p in [(4,2,17),(8,2,97),(8,3,97),(16,2,97)]:
  for z in range(1,p):
   c=scalar_case(N,b,p,z)
   if not c['D_determinant'] and all(c['individual_branch_determinants']):badbranches.append(c);break
 assert badbranches
 out={'status':'passed','constructor_code_executed':False,'jets':jets,'scalar_cases':scalar,'separate_branch_guard_counterexamples':badbranches,'count_only':count_only()}
 Path('VARIABLE_BLOCK_INDEPENDENT_RESULTS.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'status':'passed','jet_cases':len(jets),'basis_controls':sum(c['basis_controls'] for c in jets),'guarded_solves':sum(c['chart']=='guarded_solve' for c in scalar),'scalar_guard_failures':[c for c in scalar if c['chart']!='guarded_solve'],'separate_guard_counterexamples':badbranches,'count_only_cases':out['count_only']['exact_integer_cases']},sort_keys=True))
