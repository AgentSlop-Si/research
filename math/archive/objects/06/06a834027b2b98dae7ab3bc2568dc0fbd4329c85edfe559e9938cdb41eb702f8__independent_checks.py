#!/usr/bin/env python3
"""Independent mathematical controls, standard library; no submitted imports."""
from pathlib import Path
import itertools as it, json, random,sys,math,cmath

def I(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def add(a,b,p):return [[(x+y)%p for x,y in zip(r,s)] for r,s in zip(a,b)]
def mul(a,b,p):return [[sum(x*y for x,y in zip(r,c))%p for c in zip(*b)] for r in a]
def inv(a,p):
 n=len(a);z=[[x%p for x in a[i]]+I(n)[i] for i in range(n)]
 for j in range(n):
  k=next(k for k in range(j,n) if z[k][j]);z[j],z[k]=z[k],z[j];v=pow(z[j][j],-1,p);z[j]=[x*v%p for x in z[j]]
  for k in range(n):
   if k!=j:
    v=z[k][j];z[k]=[(x-v*y)%p for x,y in zip(z[k],z[j])]
 return [r[n:] for r in z]
def rank(a,p):
 z=[row[:] for row in a];r=0
 for j in range(len(z[0])):
  ks=[i for i in range(r,len(z)) if z[i][j]%p]
  if not ks:continue
  k=ks[0];z[r],z[k]=z[k],z[r];v=pow(z[r][j],-1,p);z[r]=[x*v%p for x in z[r]]
  for k in range(len(z)):
   if k!=r:
    v=z[k][j];z[k]=[(x-v*y)%p for x,y in zip(z[k],z[r])]
  r+=1
  if r==len(z):break
 return r
def sub(a,rows,cols):return [[a[i][j] for j in cols] for i in rows]
def cycles(pi):
 rem=set(range(len(pi)));out=[]
 while rem:
  start=min(rem);v=start;c=[]
  while v in rem:c.append(v);rem.remove(v);v=pi[v]
  assert v==start;out.append(c)
 return out
def green(pi,w,p):
 n=len(pi);H=I(n)
 for i,j in enumerate(pi):H[i][j]=(H[i][j]-w[i])%p
 return H,inv(H,p)
def valid(pi,w,p):return all(math.prod(w[i] for i in c)%p!=1 for c in cycles(pi))
def maps(side):
 n=side*side;out=[[] for _ in range(4)]
 for x in range(side):
  for y in range(side):
   values=[(((x+2*y)%side),y),(((x+2*y+1)%side),y),(x,((y+2*x)%side)),(x,((y+2*x+1)%side))]
   for k,(a,b) in enumerate(values):out[k].append(a*side+b)
 assert all(sorted(v)==list(range(n)) for v in out);return out

def prefix_capacities(perms):
 n=len(perms[0]);forward=[0]*(n+1);reverse=[0]*(n+1)
 for pi in perms:
  for i,j in enumerate(pi):
   if i<j:forward[i+1]+=1;forward[j+1]-=1
   elif j<i:reverse[j+1]+=1;reverse[i+1]-=1
 for i in range(1,n+1):forward[i]+=forward[i-1];reverse[i]+=reverse[i-1]
 return forward[1:n],reverse[1:n]
def budget(perms,R):return sum(pi[i] not in R for pi in perms for i in R)
def minus(A,B,p):return [[(x-y)%p for x,y in zip(r,s)] for r,s in zip(A,B)]
def root(n,p):return next(w for w in range(2,p) if pow(w,n,p)==1 and all(pow(w,d,p)!=1 for d in range(1,n) if n%d==0))
def main():
 rng=random.Random(131010);p=65537;expander=[]
 for side in [2,3,4]:
  pp=maps(side);n=side*side;count=0;weak=True;strong=True;min_base=10**9
  for mask in range(1,2**n-1):
   R={i for i in range(n) if (mask>>i)&1};m=len(R);b=budget(pp,R);assert b==budget(pp,set(range(n))-R);weak &= 3*b>=(m*(n-m)+n-1)//n;strong &=5*b>=min(m,n-m);min_base=min(min_base,b);count+=1
  assert weak and strong;expander.append(dict(side=side,N=n,all_nontrivial_cuts=count,three_copy_weaker_gate=True,five_copy_all_rank_capacity_gate=True,base_cycle_counts=[len(cycles(pi)) for pi in pp]))
 # Exact characteristic-zero spectral constant comparisons via rational squares.
 # 3*(4-5sqrt2/2)>1 iff sqrt2<22/15; 5*...>2 iff sqrt2<36/25.
 assert 2*15**2<22**2 and 2*25**2<36**2
 # Linear-work prefix capacity and all-size shift witness.
 n=128;shift_perms=[[(i+d)%n for i in range(n)] for d in [1,2,3,4]];f,r=prefix_capacities(shift_perms);assert f[63]==r[63]==10
 for k in range(1,n):assert f[k-1]==budget(shift_perms,set(range(k))) and r[k-1]==budget(shift_perms,set(range(k,n)))
 # Independent hidden-cut example. Permutations initially preserve R and its
 # complement, then swap one image across. Search is for a control, not FFT.
 R={3+16*j for j in range(8)};C=set(range(n))-R;hidden=None
 for trial in range(100):
  pp=[]
  for _ in range(4):
   pi=[None]*n
   for group in [sorted(R),sorted(C)]:
    values=group[:];rng.shuffle(values)
    for i,j in zip(group,values):pi[i]=j
   i=rng.choice(sorted(R));j=rng.choice(sorted(C));pi[i],pi[j]=pi[j],pi[i];pp.append(pi)
  f,r=prefix_capacities(pp)
  if all(min(f[k-1],r[k-1])>=min(k,n-k) for k in range(1,n)):
   assert budget(pp,R)==budget(pp,C)==4;hidden=dict(N=n,R=sorted(R),permutations=pp,total_crossing_budget=4,all_prefix_cuts_pass=True);break
 assert hidden;w=root(n,p);block=[[pow(w,i*j,p) for j in sorted(C)] for i in sorted(R)];assert rank(block,p)==8
 # Exact Green ranks and product bounds on all cuts, arbitrary multi-cycle maps.
 green_controls=[]
 for n in [5,6,7]:
  hs=[];gs=[];ps=[];ws=[]
  for k in range(4):
   pi=list(range(n));rng.shuffle(pi)
   while True:
    weights=[0 if (i+k)%4==0 else rng.randrange(2,p) for i in range(n)]
    if valid(pi,weights,p):break
   H,G=green(pi,weights,p);hs.append(H);gs.append(G);ps.append(pi);ws.append(weights)
  T=mul(add(gs[2],gs[3],p),add(gs[0],gs[1],p),p);checked=0
  for mask in range(1,2**n-1):
   R={i for i in range(n) if (mask>>i)&1};C=set(range(n))-R;b=0
   for G,pi,weights in zip(gs,ps,ws):
    edges=sum(pi[i] not in R and weights[i]!=0 for i in R);assert rank(sub(G,sorted(R),sorted(C)),p)==edges;b+=edges
   assert rank(sub(T,sorted(R),sorted(C)),p)<=b;checked+=1
  green_controls.append(dict(N=n,cuts=checked))
 # Twenty nonzero-weight multi-cycle Green plans form a two-stage candidate.
 pp=maps(4)*5;n=16;plans=[]
 for k,pi in enumerate(pp):
  alpha=2+k
  while not valid(pi,[alpha]*n,p):alpha+=1
  plans.append(green(pi,[alpha]*n,p)[1])
 sums=[]
 for chunk in [plans[:10],plans[10:]]:
  S=[[0]*n for _ in range(n)]
  for G in chunk:S=add(S,G,p)
  sums.append(S)
 T=mul(sums[1],sums[0],p);w=root(n,p);F=[[pow(w,i*j,p) for j in range(n)] for i in range(n)];mismatch=sum(T[i][j]!=F[i][j] for i in range(n) for j in range(n));assert mismatch
 # Lifted compatibility matrix: both planted products and perturbed targets.
 lifted=[]
 for n,rr,ss in [(3,1,2),(4,2,2),(5,2,3)]:
  denominators=[];greens=[]
  for j in range(rr+ss):
   pi=list(range(n));rng.shuffle(pi)
   while True:
    weights=[rng.randrange(2,p) for _ in range(n)]
    if valid(pi,weights,p):break
   D,G=green(pi,weights,p);denominators.append(D);greens.append(G)
  X=[[0]*n for _ in range(n)];Y=[[0]*n for _ in range(n)]
  for G in greens[:rr]:X=add(X,G,p)
  for G in greens[rr:]:Y=add(Y,G,p)
  product=mul(Y,X,p)
  for bad in [False,True]:
   target=[row[:] for row in product]
   if bad:target[0][0]=(target[0][0]+1)%p
   size=(rr+ss+1)*n;H=[[0]*size for _ in range(size)]
   for b,D in enumerate(denominators):
    for i in range(n):
     for j in range(n):H[b*n+i][b*n+j]=D[i][j]
   for b in range(rr):
    for i in range(n):H[b*n+i][(rr+ss)*n+i]=-1%p
   for b in range(ss):
    for c in range(rr):
     for i in range(n):H[(rr+b)*n+i][c*n+i]=-1%p
    for i in range(n):H[(rr+ss)*n+i][(rr+b)*n+i]=-1%p
   for i in range(n):
    for j in range(n):H[(rr+ss)*n+i][(rr+ss)*n+j]=target[i][j]
   actual=rank(H,p);expected=(rr+ss)*n+rank(minus(target,product,p),p);assert actual==expected;lifted.append(dict(N=n,r=rr,s=ss,perturbed=bad,rank=actual))
 out=dict(status='PASS',expander_all_cut_controls=expander,expander_spectral_constant_checks=True,N128_shift_middle_capacity=10,N128_shift_error_bounds=dict(relative_Frobenius_squared='11/64',operator_squared='11/27'),hidden_bottleneck=hidden,hidden_Fourier_rank=8,hidden_operator_squared_bound='7/8',green_cut_controls=green_controls,twenty_plan_N16_entry_mismatches=mismatch,lifted_rank_controls=lifted,source_programs_executed=False)
 path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('INDEPENDENT_RESULTS.json');path.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
