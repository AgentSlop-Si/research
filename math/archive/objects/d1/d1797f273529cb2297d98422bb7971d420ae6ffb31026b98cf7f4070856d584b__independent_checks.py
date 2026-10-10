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
def monotone(seq):
 best=[]
 for sense in [1,-1]:
  paths=[]
  for i,x in enumerate(seq):
   candidates=[paths[j] for j in range(i) if sense*seq[j]<sense*x];path=(max(candidates,key=len)[:] if candidates else [])+[i];paths.append(path)
  z=max(paths,key=len)
  if len(z)>len(best):best=z
 return best
def pair_rectangle(pi,pa,B=26,m=3):
 first=[v for c in cycles(pi) for v in c if v<B];second=[v for c in cycles(pa) for v in c if v<B];pos={v:i for i,v in enumerate(second)};inds=monotone([pos[v] for v in first]);assert len(inds)>=2*m;labels=[first[i] for i in inds];return labels[:m],labels[-m:]
def poly_det(rows,cols,order=None):
 d={}
 for perm in it.permutations(range(len(rows))):
  exponent=sum(rows[i]*cols[perm[i]] for i in range(len(rows)));exponent=exponent if order is None else exponent%order;sgn=(-1)**sum(perm[i]>perm[j] for i in range(len(rows)) for j in range(i+1,len(rows)));d[exponent]=d.get(exponent,0)+sgn
 return {k:v for k,v in d.items() if v}
def cyclo_zero(d,p,power):
 if power==1:return len({d.get(i,0) for i in range(p)})==1
 return all(len({d.get(r+k*p,0) for k in range(p)})==1 for r in range(p))
def main():
 rng=random.Random(12010);p=1009;cross=[]
 for n in [26,29,35]:
  for trial in range(12):
   pp=[];gg=[]
   for branch in range(2):
    pi=list(range(n));rng.shuffle(pi)
    while True:
     w=[0 if rng.randrange(5)==0 else rng.randrange(2,p) for i in range(n)]
     if valid(pi,w,p):break
    H,G=green(pi,w,p);assert mul(H,G,p)==I(n);pp.append(pi);gg.append(G)
   rows,cols=pair_rectangle(*pp);ranks=[rank(sub(g,rows,cols),p) for g in gg];assert max(ranks)<=1;assert rank(sub(add(*gg,p),rows,cols),p)<=2;cross.append(dict(n=n,rows=rows,columns=cols,ranks=ranks))
 # Sharp ES negative boundary: five decreasing blocks of five increasing levels.
 sharp=[x for b in range(5) for x in range(5*b+4,5*b-1,-1)];assert len(monotone(sharp))==5
 cyclo=[]
 for prime in [7,11,13]:
  sets=list(it.combinations(range(prime),3));cnt=0
  for rows in sets:
   for cols in sets:
    for power in [1,2]:
     d=poly_det(rows,cols,prime**power);assert d and not cyclo_zero(d,prime,power);cnt+=1
  cyclo.append(dict(prime=prime,exact_minors=cnt))
 # Full row-selection check of the Schur degree bound for B=26,m=3.
 degrees=[sum(a[i]-a[0]-i for i in range(3)) for a in it.combinations(range(26),3)];assert max(degrees)==46 and 2*46*25==2300
 for _ in range(1000):
  rows=sorted(rng.sample(range(26),3));cols=sorted(rng.sample(range(26),3));d=poly_det(rows,cols);assert d and max(d)==sum(x*y for x,y in zip(rows,cols));assert max(d)<=1875<2048
 # Composite embedding exponents, including even p-valuation.
 embeddings=[]
 for n in [29,58,841,1682,24389,48778]:
  m=n;v=0
  while m%29==0:m//=29;v+=1
  a=m*29**((v-1)//2 if v%2 else v//2-1);order=29 if v%2 else 841
  assert (a*a*order)%n==0 and a*a*order//n==m;assert (28*a)<n;embeddings.append(dict(N=n,step=a,root_order=order))
 # Product escape on the same separated rectangle; target is deliberately not Fourier.
 escape=None
 for attempt in range(100):
  n=29;ps=[];gs=[]
  for j in range(4):
   pi=list(range(n));rng.shuffle(pi)
   while True:
    w=[rng.randrange(2,p) for _ in range(n)]
    if valid(pi,w,p):break
   ps.append(pi);gs.append(green(pi,w,p)[1])
  rows,cols=pair_rectangle(ps[0],ps[1]);L=add(gs[0],gs[1],p);T=mul(L,add(gs[2],gs[3],p),p)
  if rank(sub(T,rows,cols),p)==3:escape=dict(N=n,one_layer_rank=rank(sub(L,rows,cols),p),product_rank=3,rows=rows,columns=cols);break
 assert escape
 # Polynomial 2N block rank equivalence with both satisfying and failing targets.
 gates=[]
 for n in [3,4,7,8]:
  hs=[];gs=[]
  for j in range(4):
   pi=list(range(n));rng.shuffle(pi)
   while True:
    w=[rng.randrange(2,p) for _ in range(n)]
    if valid(pi,w,p):break
   h,g=green(pi,w,p);hs.append(h);gs.append(g)
  A,B,C,D=hs;T=mul(add(gs[0],gs[1],p),add(gs[2],gs[3],p),p)
  for perturb in [False,True]:
   target=[r[:] for r in T]
   if perturb:target[0][0]=(target[0][0]+1)%p
   cb=mul(C,B,p);cd=add(C,D,p);ab=add(A,B,p);afd=mul(mul(A,target,p),D,p);block=[cb[i]+cd[i] for i in range(n)]+[ab[i]+afd[i] for i in range(n)];br=rank(block,p);assert (br==n)==(not perturb);gates.append(dict(n=n,perturbed=perturb,rank=br))
 thresholds=[]
 for r,t,s,expected in [(2,0,0,2300),(2,0,1,15872),(2,1,0,13524),(3,0,0,34545588)]:
  m=r+t+1;B=(m*(s+2)-1)**(2**(r-1))+1;v=2*(m-1)*(B-m)*(B-1);assert v==expected;thresholds.append(dict(r=r,t=t,s=s,B=B,N0=v))
 out=dict(status='PASS',separated_crosscuts=cross,sharp_25_label_boundary=True,cyclotomic_minors=cyclo,schur_row_sets=len(degrees),power_two_degree_controls=1000,embeddings=embeddings,product_escape=escape,block_rank_gates=gates,thresholds=thresholds,source_code_executed=False)
 path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('INDEPENDENT_RESULTS.json');path.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
