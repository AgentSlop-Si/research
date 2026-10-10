#!/usr/bin/env python3
"""Reviewer authored Bruhat kernels, projective cocycle, and paid word fusion."""
import itertools,json,random
from pathlib import Path
R=random.Random(230523)
def prime(q):return q>1 and all(q%d for d in range(2,int(q**.5)+1))
def mul(S,T,n):
 a,b,c,d=S;e,f,g,h=T
 return ((a*e+b*g)%n,(a*f+b*h)%n,(c*e+d*g)%n,(c*f+d*h)%n)
def mm(A,B,p):return [[sum(x*y for x,y in zip(r,c))%p for c in zip(*B)] for r in A]
def scaled(A,x,p):return [[v*x%p for v in r] for r in A]
def L(t,n):return (1,0,t%n,1)
def U(t,n):return (1,t%n,0,1)
def D(a,n):return (a,0,0,pow(a,-1,n))
def group(n):return [(a,b,c,d) for a,b,c,d in itertools.product(range(n),repeat=4) if (a*d-b*c)%n==1]
results=[];pairs=0;kernel_entries=0;words=0
for n in [3,5,7,11,13]:
 p=next(q for q in range(n+1,10000,n) if prime(q))
 omega=next(pow(g,(p-1)//n,p) for g in range(2,p) if pow(g,(p-1)//n,p)!=1)
 powers=[pow(omega,k,p) for k in range(n)];assert pow(omega,n,p)==1
 # All tables have linear preparation, including inverses in the parameter field.
 inv=[0]*n;inv[1]=1
 for k in range(2,n):inv[k]=(-(n//k)*inv[n%k])%n
 assert all(k*inv[k]%n==1 for k in range(1,n))
 chi=[-1]*n;chi[0]=0
 for x in range(1,n):chi[x*x%n]=1
 gauss=sum(powers[x*x%n] for x in range(n))%p;assert gauss and gauss*gauss%p==chi[n-1]*n%p
 assert all(sum(powers[a*x*x%n] for x in range(n))%p==chi[a]*gauss%p for a in range(1,n))
 half=inv[2];I=(1,0,0,1);W=(0,n-1,1,0)
 def rho(S):
  a,b,c,d=S
  if b:
   v=inv[2*b%n]
   return [[powers[((d*x*x-2*x*y+a*y*y)*v)%n] for y in range(n)] for x in range(n)]
  # Chirp C_(c/a) followed by the dilation P_a.
  return [[powers[(c*inv[a]*x*x*half)%n] if x==a*y%n else 0 for y in range(n)] for x in range(n)]
 def lambda_pair(S,T):
  b=S[1];e=T[1]
  if not b or not e:return 1
  bb=mul(S,T,n)[1]
  if not bb:return n%p
  q=bb*inv[(2*b*e)%n]%n
  return chi[q]*gauss%p
 elements=group(n);cache={s:rho(s) for s in elements};small=0;big=0
 for S in elements:
  a,b,c,d=S
  if b:
   factors=[L(d*inv[b],n),D(-b%n,n),W,L(a*inv[b],n)]
   prod=I;op=cache[I]
   for T in factors:prod=mul(prod,T,n);op=mm(op,cache[T],p)
   assert prod==S and op==cache[S];assert all(all(r) for r in cache[S]);big+=1
  else:
   assert mul(L(c*inv[a],n),D(a,n),n)==S
   assert mm(cache[L(c*inv[a],n)],cache[D(a,n)],p)==cache[S]
   assert all(sum(x!=0 for x in r)==1 for r in cache[S]);small+=1
  kernel_entries+=n*n
 assert small==n*(n-1) and big==n*n*(n-1) and len(elements)==n*(n*n-1)
 lul=[];ulu=[]
 for x,y,z in itertools.product(range(n),repeat=3):
  if mul(mul(L(x,n),U(y,n),n),L(z,n),n)==W:lul.append([x,y,z])
  if mul(mul(U(x,n),L(y,n),n),U(z,n),n)==W:ulu.append([x,y,z])
 assert lul==[[1,n-1,1]] and ulu==[[n-1,1,n-1]]
 assert mm(mm(cache[L(1,n)],cache[U(-1,n)],p),cache[L(1,n)],p)==cache[W]
 if n==5:
  for S,T in itertools.product(elements,repeat=2):
   scalar=lambda_pair(S,T);assert scalar
   assert mm(cache[S],cache[T],p)==scaled(cache[mul(S,T,n)],scalar,p);pairs+=1
 for length in [1,2,3,5,12,30]:
  for trial in range(5):
   word=[R.choice(elements) for j in range(length)];sym=I;scalar=1;op=cache[I]
   for S in word:scalar=scalar*lambda_pair(sym,S)%p;sym=mul(sym,S,n);op=mm(op,cache[S],p)
   assert op==scaled(cache[sym],scalar,p);words+=1
 # All pairs of individually monomial stages stay monomial; structural group closure.
 borel=[s for s in elements if not s[1]]
 assert all(mul(S,T,n)[1]==0 for S,T in itertools.product(borel,repeat=2))
 results.append({'N':n,'coefficient_prime':p,'omega':omega,'small_cell':small,'big_cell':big,'group_size':len(elements),'gauss':gauss,'LUL':lul[0],'ULU':ulu[0],'word_lengths':[1,2,3,5,12,30]})
out={'status':'PASS','fields':results,'direct_kernel_entries':kernel_entries,'projective_pairs_exhaustive_N5':pairs,'paid_scalar_word_controls':words,'source_code_executed':False,'cost_correction':'A fresh length-t word needs O(t+N) preprocessing/easy work plus at most one Fourier call; scalar tables and extraction included.'}
Path('INDEPENDENT_RESULTS.json').write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(json.dumps(out,sort_keys=True))
