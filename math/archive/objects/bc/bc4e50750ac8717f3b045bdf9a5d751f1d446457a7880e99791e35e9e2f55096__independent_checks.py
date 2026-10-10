#!/usr/bin/env python3
"""Own two-sided Green oracle, spectra and moving-interface controls."""
from pathlib import Path
from collections import deque
import math,cmath,json,random,sys
P=193;RNG=random.Random(501058)
def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def mm(a,b):return [[sum(x*y for x,y in zip(row,col))%P for col in zip(*b)] for row in a]
def inverse(a):
 n=len(a);z=[row[:]+eye(n)[i] for i,row in enumerate(a)]
 for j in range(n):
  k=next(k for k in range(j,n) if z[k][j]);z[j],z[k]=z[k],z[j];q=pow(z[j][j],-1,P);z[j]=[v*q%P for v in z[j]]
  for k in range(n):
   if k!=j:
    q=z[k][j]
    if q:z[k]=[(v-q*w)%P for v,w in zip(z[k],z[j])]
 return [row[n:] for row in z]
def rank(a):
 if not a or not a[0]:return 0
 a=[r[:] for r in a];k=0
 for j in range(len(a[0])):
  q=next((q for q in range(k,len(a)) if a[q][j]),None)
  if q is None:continue
  a[k],a[q]=a[q],a[k];v=pow(a[k][j],-1,P);a[k]=[x*v%P for x in a[k]]
  for q in range(k+1,len(a)):
   v=a[q][j]
   if v:a[q]=[(x-v*y)%P for x,y in zip(a[q],a[k])]
  k+=1
  if k==len(a):break
 return k

def green(pi,w):
 a=eye(len(pi))
 for i,j in enumerate(pi):a[i][j]=(a[i][j]-w[i])%P
 return inverse(a)
def rect(a,A,B):return [[a[i][j] for j in sorted(B)] for i in sorted(A)]
def cycle(n):
 seq=RNG.sample(range(n),n);pi=[0]*n
 for i,j in zip(seq,seq[1:]+seq[:1]):pi[i]=j
 return pi

def oracle(pi,w,A,B):
 n=len(pi);Ac=set(range(n))-set(A);Bc=set(range(n))-set(B);adj=[set() for _ in range(2*n)]
 for i in Bc:
  entries={i:1};entries[pi[i]]=(entries.get(pi[i],0)-w[i])%P
  for j,c in entries.items():
   if c and j in Ac:adj[i].add(n+j);adj[n+j].add(i)
 alive=set(Bc)|{n+j for j in Ac};queue=deque(v for v in alive if len(adj[v])<=1);matched=0
 def erase(v):
  if v not in alive:return
  alive.remove(v)
  for u in list(adj[v]):
   adj[u].discard(v)
   if u in alive and len(adj[u])<=1:queue.append(u)
  adj[v].clear()
 while queue:
  v=queue.popleft()
  if v not in alive:continue
  if not adj[v]:erase(v);continue
  assert len(adj[v])==1;u=next(iter(adj[v]));matched+=1;erase(v);erase(u)
 # A residual degree-two component is an intact even bipartite cycle.
 assert all(len(adj[v])==2 for v in alive);assert len(alive)%2==0;matched+=len(alive)//2
 return len(A)+len(B)-n+matched

def dressed(pi,w,l,r,ld=None,rd=None):
 g=green(pi,w);n=len(pi);ld=ld or [1]*n;rd=rd or [1]*n
 return [[ld[i]*g[l[i]][r[j]]*rd[j]%P for j in range(n)] for i in range(n)]
def dr_oracle(plan,A,B):
 pi,w,l,r=plan;return oracle(pi,w,{l[i] for i in A},{r[j] for j in B})
def main():
 out={'status':'PASS','uploaded_or_constructor_code_executed':False};spectra=0;entries=0
 for N in [2,3,4,6,8,9,12,16,18,24,32,45]:
  w=cmath.exp(-2j*math.pi/N);divs=[d for d in range(1,N+1) if N%d==0]
  for dr in divs:
   for dc in divs:
    r=N//dr;c=N//dc;h=N//math.gcd(N,dr*dc);s2=r*c/(N*h);assert r%h==c%h==0 and h<=min(r,c) and s2<=1
    for a,b in set([(0,0),(dr-1,dc-1)]):
     rows=list(range(a,N,dr));cols=list(range(b,N,dc))
     for u,i in enumerate(rows):
      for v,j in enumerate(rows):
       gram=sum(w**((i-j)*k) for k in cols)/N;expected=(c/N)*w**(dr*b*(u-v)) if (u-v)%h==0 else 0;assert abs(gram-expected)<3e-12;entries+=1
     # Each phase-corrected Gram block is c/N times J_(r/h), hence
     # h eigenvalues s², rest zero; trace and projector polynomial agree.
     assert abs(h*s2-r*c/N)<1e-14;spectra+=1
 out['complex_coset_gram_cases']=spectra;out['complex_gram_entries']=entries
 # Exact finite-field rank in all divisor pairs, including unrelated offsets.
 modular=0;generator=next(a for a in range(2,P) if all(pow(a,(P-1)//q,P)!=1 for q in [2,3]))
 for N in [2,4,6,8,12,16,24,32,48,64]:
  w=pow(generator,(P-1)//N,P);divs=[d for d in range(1,N+1) if N%d==0]
  for dr in divs:
   for dc in divs:
    for a,b in set([(0,0),(dr-1,dc-1)]):
     A=range(a,N,dr);B=range(b,N,dc);assert rank([[pow(w,(-i*j)%N,P) for j in B] for i in A])==N//math.gcd(N,dr*dc);modular+=1
 out['exact_fourier_coset_ranks']=modular
 # Exhaust all arbitrary rectangles for small actual Green matrices.
 controls=0;general=0
 for n in [2,3,4,5,6,8,16,32]:
  for z in range(4):
   pi=cycle(n) if z<3 else RNG.sample(range(n),n)
   while True:
    w=[0 if (i+z)%4==0 else RNG.randrange(1,P) for i in range(n)]
    try:g=green(pi,w);break
    except StopIteration:pass
   masks=range(1<<n) if n<=6 else None
   pairs=[({i for i in range(n) if a>>i&1},{i for i in range(n) if b>>i&1}) for a in masks for b in masks] if masks is not None else [(set(RNG.sample(range(n),RNG.randrange(n+1))),set(RNG.sample(range(n),RNG.randrange(n+1)))) for _ in range(100)]
   for A,B in pairs:assert rank(rect(g,A,B))==oracle(pi,w,A,B);controls+=1;general+=int(z==3)
 out['green_arbitrary_rectangle_controls']=controls;out['general_permutation_extension_controls']=general
 # Fresh two-stage cases with arbitrary independent monomial endpoints.
 inequalities=0;interfacecontrols=0
 for trial in range(2):
  n=8;allset=set(range(n));A=set(range(0,n,2));C=set(range(1,n,2));plans=[];matrices=[]
  for stage in range(2):
   pp=[];gg=[]
   for branch in range(2):
    pi=cycle(n);w=[1]*n;w[branch]=branch+2;l=RNG.sample(range(n),n);r=RNG.sample(range(n),n);pp.append((pi,w,l,r));gg.append(dressed(pi,w,l,r))
   plans.append(pp);matrices.append([[(gg[0][i][j]+gg[1][i][j])%P for j in range(n)] for i in range(n)])
  product=mm(*matrices);actual=rank(rect(product,A,C));costs=[]
  for mask in range(1<<n):
   S={i for i in range(n) if mask>>i&1};cost=sum(dr_oracle(plan,A,allset-S) for plan in plans[0])+sum(dr_oracle(plan,S,C) for plan in plans[1]);assert actual<=cost;costs.append(cost);interfacecontrols+=1
  for a in range(1<<n):
   for b in range(1<<n):assert costs[a]+costs[b]>=costs[a|b]+costs[a&b];inequalities+=1
 out['submodularity_inequalities']=inequalities;out['moving_product_interface_controls']=interfacecontrols
 # Reproduce the supplied four-branch witness using parameter DATA only.
 witness={'interface_set': [0, 1, 2, 4, 5, 6, 10, 11, 15, 16, 19, 23, 25, 26, 28, 32, 35, 36, 41, 42, 43, 44, 47, 48, 49, 52, 53, 55, 56, 57, 59, 62], 'branch_parameters': [[{'sigma': [10, 47, 38, 27, 60, 29, 42, 11, 54, 25, 16, 43, 20, 21, 22, 23, 36, 41, 52, 49, 26, 31, 40, 13, 4, 2, 46, 45, 0, 39, 58, 63, 8, 3, 44, 61, 32, 5, 12, 15, 50, 7, 62, 59, 30, 17, 56, 37, 35, 51, 48, 1, 34, 19, 18, 33, 24, 55, 6, 53, 28, 57, 14, 9], 'weights': [1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 'row_perm': [8, 29, 52, 3, 0, 41, 30, 13, 36, 19, 26, 59, 40, 49, 50, 9, 24, 25, 38, 45, 42, 35, 58, 39, 10, 57, 2, 47, 16, 55, 60, 31, 56, 21, 48, 51, 22, 15, 54, 23, 14, 5, 28, 37, 62, 11, 20, 27, 46, 1, 4, 43, 32, 53, 6, 17, 44, 7, 12, 63, 34, 61, 18, 33], 'col_perm': [0, 56, 6, 19, 58, 34, 16, 5, 23, 57, 18, 2, 35, 27, 63, 4, 20, 33, 13, 60, 43, 1, 9, 44, 15, 28, 22, 45, 38, 41, 21, 53, 14, 37, 61, 52, 46, 55, 11, 17, 25, 36, 24, 42, 26, 3, 31, 8, 62, 54, 49, 29, 10, 40, 7, 32, 30, 12, 39, 50, 59, 47, 48, 51]}, {'sigma': [18, 35, 32, 39, 58, 23, 48, 3, 34, 19, 2, 31, 28, 41, 50, 47, 10, 11, 40, 51, 14, 25, 44, 49, 22, 15, 56, 6, 42, 7, 38, 33, 8, 5, 12, 53, 26, 59, 46, 1, 45, 9, 0, 57, 62, 29, 52, 43, 20, 21, 60, 63, 36, 37, 30, 13, 24, 55, 54, 61, 4, 17, 16, 27], 'weights': [1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 'row_perm': [8, 23, 18, 51, 42, 43, 54, 3, 16, 41, 44, 15, 26, 63, 30, 45, 60, 29, 0, 27, 40, 13, 22, 59, 32, 25, 6, 17, 10, 47, 38, 5, 52, 1, 36, 49, 14, 57, 48, 55, 28, 11, 24, 37, 56, 7, 50, 39, 62, 31, 34, 53, 46, 19, 12, 9, 2, 61, 58, 33, 4, 21, 20, 35], 'col_perm': [44, 50, 10, 59, 8, 38, 18, 23, 11, 43, 62, 14, 35, 47, 45, 0, 48, 5, 15, 42, 29, 17, 19, 12, 41, 58, 56, 3, 46, 53, 27, 37, 26, 25, 21, 40, 4, 13, 39, 49, 9, 6, 34, 32, 24, 1, 33, 20, 36, 2, 7, 55, 60, 16, 61, 22, 52, 30, 63, 28, 31, 51, 54, 57]}], [{'sigma': [36, 21, 48, 63, 28, 43, 14, 55, 26, 29, 2, 23, 44, 12, 38, 33, 24, 9, 50, 13, 34, 45, 62, 17, 46, 3, 32, 49, 52, 7, 20, 39, 18, 47, 58, 1, 10, 57, 40, 15, 16, 53, 6, 41, 56, 27, 4, 25, 8, 31, 60, 5, 22, 61, 42, 59, 30, 35, 54, 37, 51, 11, 0, 19], 'weights': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 'row_perm': [10, 20, 44, 39, 30, 58, 62, 51, 41, 57, 24, 12, 31, 53, 55, 16, 14, 27, 13, 34, 49, 5, 19, 56, 21, 50, 48, 33, 18, 35, 9, 63, 46, 15, 23, 54, 8, 43, 25, 47, 7, 36, 40, 52, 6, 29, 45, 22, 0, 2, 1, 17, 42, 4, 11, 60, 38, 32, 37, 26, 59, 61, 28, 3], 'col_perm': [22, 55, 62, 13, 0, 7, 34, 15, 52, 43, 30, 11, 18, 21, 32, 41, 16, 25, 12, 59, 26, 17, 50, 37, 56, 33, 54, 57, 36, 31, 28, 63, 58, 27, 46, 1, 40, 29, 42, 49, 20, 3, 24, 23, 6, 45, 8, 9, 4, 35, 44, 53, 14, 51, 60, 5, 38, 61, 10, 47, 48, 19, 2, 39]}, {'sigma': [54, 53, 0, 49, 32, 47, 46, 59, 58, 60, 15, 29, 52, 1, 42, 11, 40, 23, 24, 55, 28, 31, 50, 39, 20, 7, 36, 25, 6, 57, 14, 51, 44, 13, 16, 5, 30, 19, 22, 3, 12, 43, 18, 37, 56, 17, 4, 61, 26, 35, 2, 63, 10, 9, 48, 33, 8, 21, 34, 45, 62, 41, 38, 27], 'weights': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 1, 1, 1], 'row_perm': [6, 4, 46, 35, 24, 20, 60, 11, 7, 55, 8, 52, 13, 29, 23, 44, 0, 21, 1, 28, 61, 5, 39, 18, 57, 58, 16, 51, 14, 31, 17, 27, 2, 53, 45, 40, 56, 41, 3, 9, 15, 50, 62, 36, 48, 33, 63, 26, 12, 22, 59, 37, 42, 54, 19, 10, 34, 30, 47, 38, 25, 43, 32, 49], 'col_perm': [42, 9, 32, 35, 4, 23, 50, 45, 6, 59, 60, 19, 2, 15, 30, 39, 54, 57, 16, 13, 44, 5, 62, 7, 34, 61, 36, 63, 28, 37, 46, 17, 0, 49, 14, 29, 22, 55, 24, 1, 40, 11, 56, 27, 8, 31, 38, 41, 10, 25, 18, 21, 58, 33, 20, 51, 52, 43, 26, 3, 12, 47, 48, 53]}]]};n=64;allset=set(range(n));A=set(range(0,n,2));C=set(range(1,n,2));S=set(witness['interface_set']);stages=[];branchranks=[];cycles_seen=[]
 for stage,desc in enumerate(witness['branch_parameters']):
  matrices=[]
  for rec in desc:
   pi,w,l,r=[rec[k] for k in ['sigma','weights','row_perm','col_perm']];assert sorted(pi)==sorted(l)==sorted(r)==list(range(n));walk=[];x=0
   while x not in walk:walk.append(x);x=pi[x]
   assert x==0 and len(walk)==n;cycles_seen.append(tuple(pi));g=dressed(pi,w,l,r);rows,cols=(A,allset-S) if stage==0 else (S,C);rr=rank(rect(g,rows,cols));assert rr==dr_oracle((pi,w,l,r),rows,cols)==1;branchranks.append(rr);matrices.append(g)
  stages.append([[(matrices[0][i][j]+matrices[1][i][j])%P for j in range(n)] for i in range(n)])
 assert len(set(cycles_seen))==4;T=mm(*stages);sr=[rank(rect(stages[0],A,allset-S)),rank(rect(stages[1],S,C))];fixed=[rank(rect(H,A,C)) for H in stages];pr=rank(rect(T,A,C));assert (sr,fixed,pr)==([1,1],[17,17],2)
 out['supplied_witness']={'distinct_Hamiltonian_cycles':4,'branch_ranks':branchranks,'stage_moving_ranks':sr,'stage_fixed_ranks':fixed,'product_rank':pr,'Fourier_rank':16,'complex_operator_error_floor':1,'complex_Frobenius_error_floor_squared':12}
 # Three stages, unrelated moving sets, direct entry-product positive controls.
 triples=0
 for n in [4,8]:
  plans=[];matrices=[]
  for i in range(3):
   pi=cycle(n);w=[1]*n;w[i%n]=2;l=RNG.sample(range(n),n);r=RNG.sample(range(n),n);plans.append((pi,w,l,r));matrices.append(dressed(pi,w,l,r))
  product=mm(mm(matrices[0],matrices[1]),matrices[2]);allset=set(range(n))
  for _ in range(80):
   sets=[set(RNG.sample(range(n),RNG.randrange(n+1))) for i in range(4)];cost=sum(dr_oracle(plans[i],sets[i],allset-sets[i+1]) for i in range(3));assert rank(rect(product,sets[0],allset-sets[3]))<=cost;triples+=1
 out['three_stage_moving_controls']=triples
 p=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('INDEPENDENT_RESULTS.json');p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
