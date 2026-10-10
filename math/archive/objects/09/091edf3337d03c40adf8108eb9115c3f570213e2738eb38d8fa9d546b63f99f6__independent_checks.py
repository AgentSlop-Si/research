"""Fresh independent Phase11 controls. Pure standard library; no source imports."""
from pathlib import Path
from itertools import product
import json,random
rng=random.Random(501117)
def isprime(p):return p>=2 and all(p%d for d in range(2,int(p**.5)+1))
def root(p,n):
 assert isprime(p) and (p-1)%n==0
 return next(w for w in range(1,p) if pow(w,n,p)==1 and all(pow(w,d,p)!=1 for d in range(1,n) if n%d==0))
def dft(x,p,w,inverse=False):
 n=len(x);sgn=1 if inverse else -1;fac=pow(n,-1,p) if inverse else 1
 return [fac*sum(a*pow(w,(sgn*k*j)%n,p) for j,a in enumerate(x))%p for k in range(n)]
def rank(A,p):
 A=[r[:] for r in A];k=0
 for j in range(len(A[0])):
  q=next((q for q in range(k,len(A)) if A[q][j]%p),None)
  if q is None:continue
  A[k],A[q]=A[q],A[k];v=pow(A[k][j],-1,p);A[k]=[v*x%p for x in A[k]]
  for q in range(len(A)):
   if q!=k:
    v=A[q][j];A[q]=[(a-v*b)%p for a,b in zip(A[q],A[k])]
  k+=1
  if k==len(A):break
 return k
# Construct quotient coefficient rows directly from the defining supports.
def state_rows(n,d,p,w):
 m=n//d;rows=[]
 for r in range(d):
  for t in range(m):
   row=[0]*n
   for u in range(d):row[t+u*m]=pow(w,(-r*u*m)%n,p)
   rows.append(row)
 return rows
stat={'full_dfts':0,'coefficients':0,'projector_coordinates':0,'symbolic_nodes':0,'basis_rank_levels':0,'sharp_rank_cases':0,'explicit_rank_matrices':0,'green_vectors':0,'green_equations':0,'green_fullrank_masks':0,'singular_controls':0}
for p,n in [(17,2),(17,4),(17,8),(17,16),(97,32),(257,64)]:
 w=root(p,n);allrows=[];d=1
 while d<=n:
  rows=state_rows(n,d,p,w);assert rank(rows,p)==n;allrows+=list(map(tuple,rows));stat['basis_rank_levels']+=1;d*=2
 assert len(set(allrows))==len(allrows);stat['symbolic_nodes']+=len(allrows)
 for x in [[int(j==s) for j in range(n)] for s in range(min(n,8))]+[[rng.randrange(p) for _ in range(n)],[1]*n]:
  states={(0,t):x[t] for t in range(n)};d=1
  while True:
   m=n//d;rows=state_rows(n,d,p,w)
   for r in range(d):
    for t in range(m):assert states[r,t]==sum(a*b for a,b in zip(rows[r*m+t],x))%p
    spec=dft(x,p,w);filtered=dft([v if k%d==r else 0 for k,v in enumerate(spec)],p,w,True)
    for j in range(n):assert filtered[j]==pow(d,-1,p)*pow(w,(r*(j//m)*m)%n,p)*states[r,j%m]%p;stat['projector_coordinates']+=1
   if d==n:break
   new={};h=m//2
   for r,t in product(range(d),range(h)):
    a=states[r,t];b=states[r,t+h]*pow(w,(-r*h)%n,p)%p;new[r,t]=(a+b)%p;new[r+d,t]=(a-b)%p
   states=new;d*=2
  out=[states[k,0] for k in range(n)];assert out==dft(x,p,w);stat['full_dfts']+=1;stat['coefficients']+=n
# Polynomial helpers implemented independently from coefficient-root definition.
def poly(roots,p):
 out=[1]
 for a in roots:
  nxt=[0]*(len(out)+1)
  for j,v in enumerate(out):nxt[j]=(nxt[j]-a*v)%p;nxt[j+1]=(nxt[j+1]+v)%p
  out=nxt
 return out
def ev(a,x,p):return sum(v*pow(x,j,p) for j,v in enumerate(a))%p
def spectral_matrix(vals,p,w):
 n=len(vals);return [[pow(n,-1,p)*sum(vals[k]*pow(w,(k*(i-j))%n,p) for k in range(n))%p for j in range(n)] for i in range(n)]
for p,n in [(3,2),(7,3),(17,4),(31,5),(13,6),(17,8),(97,12),(17,16),(97,24),(97,32)]:
 w=root(p,n);zs=[pow(w,k,p) for k in range(n)]
 for sz in sorted(set([1,n//2,n-1])):
  K=set(rng.sample(range(n),sz))
  for d in range(1,min(sz,n-sz,3)+1):
   A=poly([zs[k] for k in sorted(set(range(n))-K)[:d]],p);B=poly([zs[k] for k in sorted(K)[:d]],p)
   lam=next(v for v in range(1,p) if all((ev(A,z,p)-v*ev(B,z,p))%p for z in zs));Q=[(a-lam*b)%p for a,b in zip(A,B)];vals=[(int(k in K)-ev(A,z,p)*pow(ev(Q,z,p),-1,p))%p for k,z in enumerate(zs)]
   assert sum(v!=0 for v in vals)==n-2*d;assert rank(spectral_matrix(vals,p,w),p)==n-2*d;stat['sharp_rank_cases']+=1;stat['explicit_rank_matrices']+=1
# Entire normalized degree<=1 rational class at F17,N8, including exceptional0/I.
p=17;n=8;w=root(p,n);zs=[pow(w,k,p) for k in range(n)];best=n;nontrivial=n;tested=0
for q in [[1,0]]+[[q0,1] for q0 in range(p)]:
 dens=[ev(q,z,p) for z in zs]
 if 0 in dens:continue
 for a in product(range(p),repeat=2):
  r=sum((a[0]+a[1]*z)*pow(den,-1,p)%p!=int(k<4) for k,(z,den) in enumerate(zip(zs,dens)));best=min(best,r);tested+=1
  if a!=(0,0) and tuple(q)!=a:assert r>=6;nontrivial=min(nontrivial,r)
assert (best,nontrivial,tested)==(4,6,2890)
stat['exhaustive_rationals']={'tested':tested,'minimum':best,'nontrivial_minimum':nontrivial}
# Dense Green defined by its polynomial matrix, compared to independently solved recurrence.
for p,n in [(7,3),(17,4),(31,5),(13,6),(97,8),(97,12),(97,16),(97,24),(97,32)]:
 w=root(p,n)
 for alpha in range(1,min(p,8)):
  if pow(alpha,n,p)==1:stat['singular_controls']+=1;continue
  iv=pow(1-pow(alpha,n,p),-1,p)
  G=[[iv*pow(alpha,(j-i)%n,p)%p for j in range(n)] for i in range(n)]
  assert all(v for row in G for v in row)
  for x in [[rng.randrange(p) for _ in range(n)],[int(j==n-1) for j in range(n)]]:
   y=[sum(a*b for a,b in zip(row,x))%p for row in G];assert all((y[j]-alpha*y[(j+1)%n])%p==x[j] for j in range(n));stat['green_equations']+=n
   # A differently organized prefix solve with the exact known y0 boundary.
   yy=[0]*n;yy[0]=sum(pow(alpha,j,p)*x[j] for j in range(n))*iv%p
   for j in range(n-1,0,-1):yy[j]=(x[j]+alpha*yy[(j+1)%n])%p
   assert yy==y;stat['green_vectors']+=1
  for K in [set(),set(range(n)),set(range(0,n,2)),{0}]:
   P=spectral_matrix([int(k in K) for k in range(n)],p,w);D=[[(a-b)%p for a,b in zip(row,g)] for row,g in zip(P,G)];assert rank(D,p)==n;stat['green_fullrank_masks']+=1
   if n%2==0 and K==set(range(0,n,2)):
    assert P==[[(int(i==j)+int(j==(i+n//2)%n))*pow(2,-1,p)%p for j in range(n)] for i in range(n)]
# Wrong root cannot give invertible Fourier states; zero-alpha removes fullrank-distance assertion.
assert rank([[1]*8 for _ in range(8)],17)==1
assert rank([[int(i==j)-int(i==j) for j in range(4)] for i in range(4)],17)==0
# Distinct labels with too few measured amplitudes.
M=[[int(bool(k&(1<<b))) for k in range(16)] for b in range(4)];assert len(set(zip(*M)))==16 and rank(M,17)==4
B=lambda e:e.bit_length()-1+bin(e).count('1') if e else 0
counts=[]
for n in [256,1024,4096,65536]:
 L=n.bit_length()-1;online=3*n*L//2;total=online+n-1+B(n)+B(n//2);counts.append({'N':n,'online':online,'total':total})
assert [x['total'] for x in counts]==[3344,16404,77848,1638432]
stat.update(status='PASS',source_code_executed=False,scalar_count_reconstructions=counts,traffic_correction={'green_input_reads':'2N-1 in literal code; source counter recordsN','green_state_reads':'N-1 recurrence reads omitted','array_initialization':'not included in semantic state_writes'},scope='Exact bounded controls and symbolic proofs; no source suite, large historical FFT run, novelty or general FFT speedup claim.')
Path(__file__).with_name('INDEPENDENT_RESULTS.json').write_text(json.dumps(stat,indent=2)+'\n');print(json.dumps(stat,indent=2))
