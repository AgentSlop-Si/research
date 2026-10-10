"""Reviewer-authored exact controls; no source programs are imported."""
from fractions import Fraction as Q
from itertools import combinations
from math import comb,gcd
import random,json

def conv(a,b,p):
 n=len(a);return [sum(a[j]*b[k-j] for j in range(k+1))%p for k in range(n)]
def kernel(n,q,p):
 h=[1]
 for j in range(1,n):h.append(h[-1]*pow(1-pow(q,j,p),-1,p)%p)
 return h

def flow():
 rng=random.Random(791304);cases=coeffs=passes=0
 for n,p,gen in [(4,17,3),(8,17,3),(16,97,5),(32,193,5)]:
  q=pow(gen,(p-1)//n,p);assert pow(q,n,p)==1 and pow(q,n//2,p)!=1;h=kernel(n,q,p)
  for b in [2**j for j in range(1,n.bit_length())]:
   base=[e*n//b for e in range(b)];fam=[base,[(e+1)%n for e in base],[1 if e==0 else e for e in base]]+[[rng.randrange(n) for _ in range(b)] for _ in range(8)]
   for es in fam:
    counts=[es.count(e)-base.count(e) for e in range(n)];a=[];s=0
    for c in counts:s-=c;a.append(s)
    assert a[-1]==0;med=sorted(a)[(n-1)//2];f=[z-med for z in a];D=sum(map(abs,f));assert all(counts[e]==f[e-1]-f[e] for e in range(n))
    assert D==min(sum(abs(z+t) for z in a) for t in range(-b,b+1))
    short=kernel(n//b,pow(q,b,p),p);v=[short[j//b] if j%b==0 else 0 for j in range(n)]
    for e,ff in enumerate(f):
     c=pow(q,e,p)
     for _ in range(abs(ff)):
      if ff>0:
       for j in range(n-1,0,-1):v[j]=(v[j]-c*v[j-1])%p
      else:
       for j in range(1,n):v[j]=(v[j]+c*v[j-1])%p
      passes+=1
    target=[1]+[0]*(n-1)
    for e in es:target=conv(target,[h[j]*pow(q,e*j,p)%p for j in range(n)],p)
    assert v==target;cases+=1;coeffs+=n
 return dict(graphs=cases,coefficients=coeffs,unit_filter_passes=passes)

def qboundary():
 ncases=entries=0
 for n,p,g in [(2,17,3),(4,17,3),(8,17,3),(16,97,5),(32,193,5)]:
  q=pow(g,(p-1)//n,p);h=kernel(n,q,p);T=[[h[i-j] if i>=j else 0 for j in range(n)] for i in range(n)]
  B=[[((q-pow(q,-i,p))%p) if j==i+1 else 0 for j in range(n)] for i in range(n)]
  C=[[((B[i][j]+int(i==j)*pow(q,-i,p)-int(i==n-1 and j==0)*q*pow(n,-1,p))%p) for j in range(n)] for i in range(n)]
  left=[[sum(T[i][k]*B[k][j] for k in range(n))%p for j in range(n)] for i in range(n)];right=[[sum(C[i][k]*T[k][j] for k in range(n))%p for j in range(n)] for i in range(n)];assert left==right;ncases+=1;entries+=n*n
 return dict(cases=ncases,entries=entries)

def positive_eigenvalues(A):
 # Exact symmetric elimination: tested matrices have no zero pivot.
 A=[r[:] for r in A];pos=0
 while A:
  inds=[i for i in range(len(A)) if A[i][i]]
  if not inds:
   assert all(v==0 for r in A for v in r);break
  k=inds[0];A[0],A[k]=A[k],A[0]
  for r in A:r[0],r[k]=r[k],r[0]
  a=A[0][0];pos+=int(a>0);A=[[A[i][j]-A[i][0]*A[0][j]/a for j in range(1,len(A))] for i in range(1,len(A))]
 return pos

def green():
 rng=random.Random(752416);cases=entries=0
 for n in (6,8,12,16):
  d=[1,3]
  for j in range(2,n+1):d.append(3*d[-1]-d[-2])
  G=[[Q(d[min(i,j)]*d[n-1-max(i,j)],d[n]) for j in range(n)] for i in range(n)]
  for i in range(n):
   for j in range(n):assert 3*G[i][j]-(G[i-1][j] if i else 0)-(G[i+1][j] if i<n-1 else 0)==int(i==j);entries+=1
  for _ in range(18):
   perm=rng.sample(range(n),n);I=set(rng.sample(range(n),n//2));J=sorted(set(range(n))-I);I=sorted(I);e1=sum((i in I)!=(i+1 in I) for i in range(n-1));inverse=[0]*n
   for a,b in enumerate(perm):inverse[b]=a
   e2=sum((inverse[i] in I)!=(inverse[i+1] in I) for i in range(n-1));E=e1+e2
   X=[[G[i][j]+G[perm[i]][perm[j]]/100 for j in J] for i in I]
   XX=[[sum(a*b for a,b in zip(r,s))-int(i==j)*Q(1,2500**2) for j,s in enumerate(X)] for i,r in enumerate(X)]
   strong=(e1+2)//3 if 5*e1>=E else max(0,(e2+2)//3-e1)
   assert positive_eigenvalues(XX)>=strong>=E//15;cases+=1
 # Entropy constant and N32 bound, certified by integer inequalities.
 assert 15**3125>2**12209
 assert 132*1000*2**224<97*15**60
 patterns=0
 for n in (4,6,8,10,12,14,16):
  hist=[0]*n
  for inds in combinations(range(n),n//2):
   S=set(inds);hist[sum((i in S)!=(i+1 in S) for i in range(n-1))]+=1;patterns+=1
  assert sum(hist)==comb(n,n//2)
  for t in range(n):assert sum(hist[:t+1])<=2*sum(comb(n-1,j) for j in range(t+1))
 return dict(path_inverse_entries=entries,exact_rational_singular_value_controls=cases,balanced_patterns=patterns,entropy_rational_threshold='c>1627/5000',N32_failure_bound='less than97/1000 by integer inequality')

def median():
 rng=random.Random(722316);cases=0
 for n in range(1,41):
  q=gcd(n,4)
  for _ in range(10):
   x=[(rng.randrange(-5,6),rng.randrange(-5,6)) for j in range(n)];res=0;meanres=0
   for a in range(q):
    for c in (0,1):
     vals=[x[j][c] for j in range(a,n,q)];m=sorted(vals)[(len(vals)-1)//2];z=sum(abs(v-m) for v in vals);assert z==min(sum(abs(v-u) for v in vals) for u in range(-5,6));res+=z;mu=Q(sum(vals),len(vals));meanres+=sum(abs(v-mu) for v in vals)
   assert res<=meanres and res<=sum(abs(a)+abs(b) for a,b in x);cases+=1
 return cases
if __name__=='__main__':
 d={'status':'PASS','cycle_flow':flow(),'q_weyl_boundary':qboundary(),'green_expansion':green(),'median_controls':median(),'scope':'New reviewer exact algebra and certificate controls; no original scripts or source execution logs replayed.'}
 print(json.dumps(d,sort_keys=True,indent=2));open('INDEPENDENT_RESULTS.json','w').write(json.dumps(d,sort_keys=True,indent=2)+'\n')
