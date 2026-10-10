#!/usr/bin/env python3
"""Independent Phase5 controls. No uploaded source imports/execution."""
import itertools,json,math,random
from pathlib import Path
def field(n):
 p=n+1
 while any(p%d==0 for d in range(2,math.isqrt(p)+1)):p+=n
 proper=[d for d in range(1,n) if n%d==0]
 for w in range(2,p):
  if pow(w,n,p)==1 and all(pow(w,d,p)!=1 for d in proper):return p,w
 raise AssertionError
def solve(A,b,p):
 a=[row[:]+[v] for row,v in zip(A,b)];n=len(A)
 for j in range(n):
  i=next(i for i in range(j,n) if a[i][j]);a[i],a[j]=a[j],a[i]
  iv=pow(a[j][j],-1,p);a[j]=[v*iv%p for v in a[j]]
  for i in range(n):
   if i==j:continue
   z=a[i][j];a[i]=[(x-z*y)%p for x,y in zip(a[i],a[j])]
 return [a[i][-1] for i in range(n)]
def rank(A,p):
 a=[row[:] for row in A];r=0
 for j in range(len(a[0])):
  i=next((i for i in range(r,len(a)) if a[i][j]),None)
  if i is None:continue
  a[i],a[r]=a[r],a[i];iv=pow(a[r][j],-1,p);a[r]=[v*iv%p for v in a[r]]
  for i in range(r+1,len(a)):
   z=a[i][j];a[i]=[(x-z*y)%p for x,y in zip(a[i],a[r])]
  r+=1
  if r==len(a):break
 return r
def dft(x,w,p):return [sum(v*pow(w,-k*t,p) for t,v in enumerate(x))%p for k in range(len(x))]
def mst_prim(m):
 seen={0};dist=[0]+[m//math.gcd(m,j) for j in range(1,m)];cost=0
 while len(seen)<m:
  j=min((j for j in range(m) if j not in seen),key=lambda j:dist[j]);cost+=dist[j];seen.add(j)
  for k in range(m):
   if k not in seen:dist[k]=min(dist[k],m//math.gcd(m,k-j))
 return cost
def mst_formula(m):
 L=1;ans=0
 for d in range(2,m+1):
  if m%d==0:
   nxt=math.lcm(L,d);ans+=d*(m//L-m//nxt);L=nxt
 return ans
def run():
 rng=random.Random(202610092216);out={'full_raw_cases':0,'full_dft_bins':0,'transition_rank_cases':0,'arbitrary_gauge_edge_entries':0,'mst_cases':0,'composite_rigidity_cases':[],'stable_large_mask_cases':[]}
 for m in range(2,13):
  p,w=field(m*m);eta=pow(w,m,p);n=m*m
  schedules=[[0]*m,list(range(m)),[rng.randrange(m) for _ in range(m)]]
  for a in schedules:
   x=[rng.randrange(p) for _ in range(n)];C=[dft([x[t+m*u] for u in range(m)],eta,p) for t in range(m)]
   output=[0]*n
   for h in range(m):
    lam=[pow(w,j-m*h*a[j],p) for j in range(m)]
    assert len(set(lam))==m
    V=[[pow(v,t,p) for v in lam] for t in range(m)]
    B=solve(V,[C[t][h] for t in range(m)],p)
    K=[[sum(pow(pow(w,-h-s*m,p)*lam[j]%p,t,p) for t in range(m))%p for j in range(m)] for s in range(m)]
    assert sum(v!=0 for row in K for v in row)==m*m-m+1
    assert sum(K[s][h]!=0 for s in range(m))==1
    out['arbitrary_gauge_edge_entries']+=m*m
    for s in range(m):output[h+s*m]=sum(K[s][j]*B[j] for j in range(m))%p
   assert output==dft(x,w,p);out['full_raw_cases']+=1;out['full_dft_bins']+=n
   for delta in range(m):
    E=[[pow(eta,-delta*t*a[j],p) for j in range(m)] for t in range(m)]
    assert rank(E,p)==len({delta*z%m for z in a});out['transition_rank_cases']+=1
  # All requested adjacent mask ranks are possible in the omega^j universal gauge.
  for r in range(1,m+1):
   a=[j%r for j in range(m)];E=[[pow(eta,-t*a[j],p) for j in range(m)] for t in range(m)]
   assert rank(E,p)==r;out['transition_rank_cases']+=1
 for m in range(2,201):
  assert mst_prim(m)==mst_formula(m);out['mst_cases']+=1
 for m in range(2,7):
  count=0;total=0
  for a in itertools.product(range(m),repeat=m):
   exact=all(len({(j-h*a[j])%m for j in range(m)})==m for h in range(m))
   criterion=all((j-k)%math.gcd(a[j]-a[k],m)!=0 for j in range(m) for k in range(j))
   assert exact==criterion;count+=exact;total+=1
  if m in (2,3,5):assert count==m
  out['composite_rigidity_cases'].append({'M':m,'all_shear_schedules':total,'universally_invertible_schedules':count})
 for m in [4,8,16,32,64]:
  p,w=field(m*m);eta=pow(w,m,p);a=[2*j%m for j in range(m)]
  assert all(math.gcd(1-2*h,m)==1 for h in range(m))
  # Fourier Gram identity algebraically: sum_t eta^(t*(e_j-e_k)) = M delta_jk.
  for h in range(m):
   e=[(j-h*a[j])%m for j in range(m)];assert len(set(e))==m
  E=[[pow(eta,-t*a[j],p) for j in range(m)] for t in range(m)];rr=rank(E,p);assert rr==m//2
  out['stable_large_mask_cases'].append({'M':m,'all_h_fourier_permutations':True,'adjacent_mask_rank':rr,'complex_condition_number':1})
 # General affine classification, without assuming M prime or prime-power.
 for m in range(2,101):
  primes=[p for p in range(2,m+1) if m%p==0 and all(p%d for d in range(2,math.isqrt(p)+1))];rad=math.prod(primes)
  for c in range(m):assert all(math.gcd(1-c*h,m)==1 for h in range(m))==(c%rad==0)
 out['affine_classification_lengths']=99
 return out
if __name__=='__main__':
 r=run();Path(__file__).with_name('PHASE5_REVIEW_RESULTS.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
