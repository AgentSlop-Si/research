#!/usr/bin/env python3
"""Fresh independent reconstruction. Standard library; no source code imported."""
import cmath,math,json,random,sys,itertools
from pathlib import Path
P=65537
R=random.Random(472043)
def inv(x):return pow(x%P,-1,P)
def mm(a,b):return [[sum(x*y for x,y in zip(row,col))%P for col in zip(*b)] for row in a]
def ident(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def matinv(a):
 n=len(a);z=[row[:]+ident(n)[i] for i,row in enumerate(a)]
 for j in range(n):
  k=next(k for k in range(j,n) if z[k][j]%P);z[j],z[k]=z[k],z[j];z[j]=[x*inv(z[j][j])%P for x in z[j]]
  for k in range(n):
   if k!=j:
    c=z[k][j];z[k]=[(x-c*y)%P for x,y in zip(z[k],z[j])]
 return [row[n:] for row in z]
def rank(a):
 if not a:return 0
 a=[r[:] for r in a];k=0
 for j in range(len(a[0])):
  q=next((q for q in range(k,len(a)) if a[q][j]%P),None)
  if q is None:continue
  a[k],a[q]=a[q],a[k];a[k]=[x*inv(a[k][j])%P for x in a[k]]
  for q in range(k+1,len(a)):
   c=a[q][j];a[q]=[(x-c*y)%P for x,y in zip(a[q],a[k])]
  k+=1
  if k==len(a):break
 return k

def bm(s,cap):
 C=[1];B=[1];L=0;delta=1;age=1;ops=0
 for n in range(len(s)):
  disc=s[n]
  for j in range(1,L+1):disc=(disc+C[j]*s[n-j])%P;ops+=1
  if not disc:age+=1;continue
  old=C[:];scale=disc*inv(delta)%P
  if len(C)<len(B)+age:C += [0]*(len(B)+age-len(C))
  for j,b in enumerate(B):C[j+age]=(C[j+age]-scale*b)%P;ops+=1
  if 2*L<=n:
   L=n+1-L
   if L>cap:return None,ops
   B=old;delta=disc;age=1
  else:age+=1
 return C[:L+1],ops

def amplitudes(nodes,s):
 # Lagrange coefficients are rows of inverse transposed Vandermonde.
 poly=[1]
 for a in nodes:
  z=[0]*(len(poly)+1)
  for i,c in enumerate(poly):z[i]=(z[i]-a*c)%P;z[i+1]=(z[i+1]+c)%P
  poly=z
 out=[];r=len(nodes)
 for a in nodes:
  q=[0]*r;q[-1]=poly[-1]
  for i in range(r-2,-1,-1):q[i]=(poly[i+1]+a*q[i+1])%P
  assert (poly[0]+a*q[0])%P==0
  den=sum(c*pow(a,i,P) for i,c in enumerate(q))%P
  out.append(sum(c*s[i] for i,c in enumerate(q))*inv(den)%P)
 return out

def prony(s,eta,cap):
 C,ops=bm(s,cap)
 if C is None:return None,ops
 r=len(C)-1
 if not r:return ([] if not any(s) else None),ops
 roots=[];a=1
 for h in range(len(s)):
  z=0
  for c in C:z=(z*a+c)%P;ops+=1
  if not z:roots.append((h,a))
  a=a*eta%P
 if len(roots)!=r:return None,ops
 cs=amplitudes([a for h,a in roots],s);modes=[(h,c) for (h,a),c in zip(roots,cs) if c]
 reconstructed=[0]*len(s)
 for h,c in modes:
  a=pow(eta,h,P);v=c
  for j in range(len(s)):reconstructed[j]=(reconstructed[j]+v)%P;v=v*a%P;ops+=1
 return (modes if reconstructed==s else None),ops

def direct(x,w):return [sum(v*pow(w,(-i*j)%len(x),P) for j,v in enumerate(x))%P for i in range(len(x))]
def aggregate(x,Q,budget):
 N=len(x);M=N//Q;w=pow(3,(P-1)//N,P);eta=pow(w,Q,P);remaining=budget;cert=[];work=0;heavy=0;threshold=M//3
 for t in range(Q):
  y=x[t::Q]
  if M<3:
   coeff=direct(y,eta);modes=[(h,c*inv(M)%P) for h,c in enumerate(coeff) if c];work+=M*M
  else:
   modes,cost=prony(y,eta,min(threshold,remaining));work+=cost
   if modes is None:
    if remaining<=threshold:return None,dict(work=work,heavy=heavy,early=True)
    coeff=direct(y,eta);modes=[(h,c*inv(M)%P) for h,c in enumerate(coeff) if c];work+=M*M;heavy+=1
    assert len(modes)>threshold
  if len(modes)>remaining:return None,dict(work=work,heavy=heavy,early=False)
  remaining-=len(modes);cert.extend((t,h,c) for h,c in modes)
 out=[0]*N
 for t,h,c in cert:
  for k in range(h,N,M):out[k]=(out[k]+M*c*pow(w,(-k*t)%N,P))%P
 return out,dict(work=work,heavy=heavy,modes=len(cert),early=False)

def synth(Q,M,counts):
 N=Q*M;eta=pow(3,(P-1)//M,P);x=[0]*N
 for t,r in enumerate(counts):
  for h in R.sample(range(M),r):
   v=R.randrange(1,P);a=pow(eta,h,P)
   for u in range(M):x[t+Q*u]=(x[t+Q*u]+v)%P;v=v*a%P
 return x

def main():
 result={'status':'PASS','uploaded_or_constructor_code_executed':False};spec=0;maxerr=0.
 # Verify exact analytic Gram form numerically without assuming an SVD routine.
 for N in range(2,41):
  w=cmath.exp(-2j*math.pi/N)
  for d in range(2,N+1):
   if N%d:continue
   m=N//d;g=math.gcd(d,m)
   for a in range(d):
    A=list(range(a,N,d));B=[i for i in range(N) if i%d!=a]
    for u,i in enumerate(A):
     for v,j in enumerate(A):
      actual=sum(w**(i*k-j*k) for k in B)/N
      phase=w**(a*d*(u-v));pred=int(u==v)-(phase/d if (u-v)%(m//g)==0 else 0)
      err=abs(actual-pred);maxerr=max(maxerr,err);assert err<2e-12
    spec+=1
 result['coset_gram_cases']=spec;result['gram_tolerance']='2e-12'
 # Exact modular cut ranks, all divisors and cosets for dyadic sizes.
 ranks=0
 for N in [2,4,8,16,32,64]:
  w=pow(3,(P-1)//N,P)
  for d in [2**r for r in range(1,N.bit_length())]:
   m=N//d;g=math.gcd(d,m)
   for a in range(d):
    A=list(range(a,N,d));B=[i for i in range(N) if i%d!=a]
    z=[[pow(w,(-i*j)%N,P) for j in B] for i in A];assert rank(z)==(m if g<d else m-m//g);ranks+=1
 result['exact_coset_ranks']=ranks
 # LSB trie implementation reconstructed independently; compare every node.
 triechecks=0;multiscale=0
 for k in range(1,10):
  N=1<<k
  for test in range(5):
   edges=[(R.randrange(N),R.randrange(N)) for _ in range(3*N)];edges=[e for e in edges if e[0]!=e[1]]
   levels=[[0]*(1<<r) for r in range(k+1)]
   for u,v in edges:
    tz=((u-v)&-(u-v)).bit_length()-1;levels[k][u]+=1;levels[tz][u% (1<<tz)]-=1
   for r in range(k,0,-1):
    for a,c in enumerate(levels[r]):levels[r-1][a% (1<<(r-1))]+=c
   for r,row in enumerate(levels):
    for a,c in enumerate(row):assert c==sum(u%(1<<r)==a and v%(1<<r)!=a for u,v in edges);triechecks+=1
   h=k//2;lhs=sum(max(0,h-(((u-v)&-(u-v)).bit_length()-1)) for u,v in edges);assert lhs==sum(sum(levels[r]) for r in range(1,h+1));multiscale+=1
 result['trie_cut_values']=triechecks;result['multiscale_identities']=multiscale
 # Genuine Green complementary cuts; sum/product fixed-frame rank budgets.
 cutchecks=0;productchecks=0
 for N in [4,8,16]:
  greens=[];plans=[]
  for t in range(4):
   order=R.sample(range(N),N);pi=[0]*N
   for i,j in zip(order,order[1:]+order[:1]):pi[i]=j
   weights=[0 if (i+t)%5==0 else R.randrange(1,50) for i in range(N)];K=ident(N)
   for i in range(N):K[i][pi[i]]=(K[i][pi[i]]-weights[i])%P
   greens.append(matinv(K));plans.append((pi,weights))
  H=[[(greens[0][i][j]+2*greens[1][i][j])%P for j in range(N)] for i in range(N)];J=[[(3*greens[2][i][j]+greens[3][i][j])%P for j in range(N)] for i in range(N)];T=mm(H,J)
  subsets=[{i for i in range(N) if mask>>i&1} for mask in range(1,1<<N-1)] if N<=8 else [set(R.sample(range(N),R.randrange(1,N))) for _ in range(100)]
  for A in subsets:
   B=set(range(N))-A;bud=0
   for G,(pi,wt) in zip(greens,plans):
    c=sum(pi[i] in B and wt[i]!=0 for i in A);assert rank([[G[i][j] for j in B] for i in A])==c;bud+=c;cutchecks+=1
   assert rank([[T[i][j] for j in B] for i in A])<=bud;productchecks+=1
 result['green_cut_identities']=cutchecks;result['product_sum_cut_controls']=productchecks
 # Full raw recognition, including heavy fibers, budget exhaustion and zeros.
 cases=[];bins=0;heavy=0
 for Q,M in [(1,1),(2,2),(2,4),(4,4),(4,8),(8,8),(8,16),(16,16),(16,32)]:
  N=Q*M
  profiles=[[0]*Q,[1]*Q,[min(M,Q)]+[1]*(Q-1),[M]+[0]*(Q-1),[M]*Q]
  profiles += [[R.randrange(M+1) for _ in range(Q)] for _ in range(3)]
  for counts in profiles:
   x=synth(Q,M,counts);K=sum(counts);want=direct(x,pow(3,(P-1)//N,P))
   for budget in sorted(set([0,max(0,K-1),K,K+2])):
    got,stats=aggregate(x,Q,budget);assert (got is not None)==(K<=budget)
    if got is not None:assert got==want;bins+=N
    assert stats['work']<=40*(N+M*budget+budget*budget)
    heavy+=stats['heavy'];cases.append(dict(N=N,Q=Q,M=M,K=K,budget=budget,accepted=got is not None,heavy=stats['heavy']))
 result['recognition_cases']=len(cases);result['accepted']=sum(c['accepted'] for c in cases);result['rejected']=sum(not c['accepted'] for c in cases);result['verified_output_bins']=bins;result['heavy_fallbacks']=heavy;result['recognition_records']=cases
 # Monotone-cap generic negative controls against independently known exact DFT support.
 generic=0
 for Q,M in [(2,8),(4,8),(8,16)]:
  for _ in range(8):
   x=[R.randrange(P) for i in range(Q*M)];eta=pow(3,(P-1)//M,P);K=sum(sum(c!=0 for c in direct(x[t::Q],eta)) for t in range(Q))
   for budget in [0,Q,2*Q,K]:
    got,_=aggregate(x,Q,budget);assert (got is not None)==(K<=budget)
    if got is not None:assert got==direct(x,pow(3,(P-1)//(Q*M),P))
    generic+=1
 result['generic_recognition_controls']=generic
 fullrank=[]
 for Q in [8,16,32]:
  M=Q;N=Q*Q;eta=pow(3,(P-1)//M,P);x=[0]*N
  for t in range(Q):
   modes=range(M) if t==0 else [t]
   for h in modes:
    for u in range(M):x[t+Q*u]=(x[t+Q*u]+(h+1)*pow(eta,h*u,P))%P
  assert rank([x[t::Q] for t in range(Q)])==Q
  got,stats=aggregate(x,Q,2*Q-1);assert got==direct(x,pow(3,(P-1)//N,P));assert stats['heavy']==1
  fullrank.append({'N':N,'fiber_matrix_rank':Q,'largest_fiber_modes':Q,'total_modes':2*Q-1})
 result['full_rank_concentrated_mode_controls']=fullrank
 out=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('INDEPENDENT_RESULTS.json');out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='recognition_records'},indent=2))
if __name__=='__main__':main()
