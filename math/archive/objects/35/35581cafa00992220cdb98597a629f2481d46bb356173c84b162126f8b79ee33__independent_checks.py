#!/usr/bin/env python3
"""Own exact Green restrictions and finite-field Gauss/CRT controls."""
from pathlib import Path
import random,math,json,sys,itertools
P=65537;RNG=random.Random(510062)
def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def mm(a,b):return [[sum(x*y for x,y in zip(r,c))%P for c in zip(*b)] for r in a]
def inverse(a):
 n=len(a);z=[r[:]+eye(n)[i] for i,r in enumerate(a)]
 for j in range(n):
  k=next(k for k in range(j,n) if z[k][j]);z[j],z[k]=z[k],z[j];v=pow(z[j][j],-1,P);z[j]=[x*v%P for x in z[j]]
  for k in range(n):
   if k!=j:
    v=z[k][j]
    if v:z[k]=[(x-v*y)%P for x,y in zip(z[k],z[j])]
 return [r[n:] for r in z]
def green(pi,w):
 A=eye(len(pi))
 for i,j in enumerate(pi):A[i][j]=(A[i][j]-w[i])%P
 return inverse(A)
def induced(pi,w,S):
 index={s:i for i,s in enumerate(S)};ss=set(S);out=[];weights=[];lengths=[]
 for i in S:
  v=w[i];j=pi[i];length=1
  while j not in ss:v=v*w[j]%P;j=pi[j];length+=1
  out.append(index[j]);weights.append(v);lengths.append(length)
 return out,weights,lengths

def prime(p):return p>=2 and all(p%d for d in range(2,math.isqrt(p)+1))
def factors(n):
 out=[];d=2
 while d*d<=n:
  if n%d==0:
   out.append(d)
   while n%d==0:n//=d
  d+=1
 if n>1:out.append(n)
 return out

def field_for(N,start=1):
 k=start
 while not prime(k*N+1):k+=1
 p=k*N+1
 for base in range(2,p):
  w=pow(base,k,p)
  if pow(w,N,p)==1 and all(pow(w,N//d,p)!=1 for d in factors(N)):return p,w
 raise AssertionError

def gauss(N,w):return sum(pow(w,((N+1)//2)*j*j,P) for j in range(N))%P
def forced_formula(N,w,G,i,j):
 h=(N+1)//2;c=N*G%P
 return (pow(w,i*j,P)-G*pow(w,(-h*(i+j)**2)%N,P)+(c*pow(w,(-h*i*i)%N,P) if i==j else 0))*pow((1+c)%P,-1,P)%P

def main():
 global P
 out={'status':'PASS','uploaded_or_constructor_code_executed':False};cases=0;masked=0;guardchecks=0;entries=0
 for N in [1,2,3,5,7,8,12,17]:
  for trial in range(3):
   seq=RNG.sample(range(N),N);pi=[0]*N
   for i,j in zip(seq,seq[1:]+seq[:1]):pi[i]=j
   for mode in ['nonzero','some_zero','all_zero']:
    wt=[RNG.randrange(2,50) for i in range(N)]
    if mode=='some_zero':wt[trial%N]=0
    if mode=='all_zero':wt=[0]*N
    if math.prod(wt)%P==1:wt[0]=0
    G=green(pi,wt)
    subsets=[list(S) for k in range(1,N+1) for S in itertools.combinations(range(N),k)] if N<=8 else [RNG.sample(range(N),k) for k in [1,2,5,N-1,N]]
    for S in subsets:
     RNG.shuffle(S);subpi,subw,length=induced(pi,wt,S);assert sum(length)==N and math.prod(subw)%P==math.prod(wt)%P;H=green(subpi,subw);sub=[[G[i][j] for j in S] for i in S];assert H==sub;entries+=len(S)**2;cases+=1
     L=[0 if i%3==0 else i+2 for i in range(N)];R=[0 if i%4==1 else i+3 for i in range(N)];actual=[[L[i]*G[i][j]*R[j]%P for j in S] for i in S];expected=[[L[i]*H[a][b]*R[j]%P for b,j in enumerate(S)] for a,i in enumerate(S)];assert actual==expected;masked+=1
    sw=[1]*N;_,ew,_=induced(pi,sw,subsets[0]);assert math.prod(ew)%P==1;guardchecks+=1
 out.update(principal_restriction_cases=cases,checked_entries=entries,singular_endpoint_controls=masked,invalid_guard_preservation=guardchecks)
 # Both Gauss sign classes, odd composite moduli and nonstandard primitive roots.
 gausscases=[]
 for N in [3,5,7,9,11,15,21,25,27,35,45,49,55,63,65,81,85,95,99]:
  P,w0=field_for(N)
  for a in [1,2,N-1]:
   w=pow(w0,a,P);G=gauss(N,w);eps=(-1)**((N-1)//2);assert G*G%P==(eps*N)%P
   minus=sum(pow(w,(-((N+1)//2)*j*j)%N,P) for j in range(N))%P;assert G*minus%P==N%P and minus==(eps*G)%P
   gausscases.append({'N':N,'prime':P,'root':w,'G':G,'sign':eps,'denominator':(1+N*G)%P})
 out['gauss_sign_records']=gausscases
 # Full forced inverses and selected-block formulas, with finite guards explicit.
 blocks=[];denseentries=0
 for N in [5,15,35,45,55,65,85,95]:
  P,w=field_for(N)
  while (1+N*gauss(N,w))%P==0:P,w=field_for(N,(P-1)//N+1)
  G=gauss(N,w);m=N//5;eta=pow(w,m*m,P);assert pow(eta,5,P)==1 and eta!=1
  block=[[forced_formula(N,w,G,m*i,m*j) for j in range(5)] for i in range(5)];derived=[[(pow(eta,i*j,P)-G*pow(eta,(-3*(i+j)**2)%5,P)+(N*G*pow(eta,(-3*i*i)%5,P) if i==j else 0))*pow((1+N*G)%P,-1,P)%P for j in range(5)] for i in range(5)];assert block==derived
  if N<=45:
   invN=pow(N,-1,P);K=[[pow(w,(-i*j)%N,P)*invN%P for j in range(N)] for i in range(N)]
   for i in range(N):K[i][i]=(K[i][i]+pow(w,((N+1)//2)*i*i,P))%P
   B=inverse(K);assert [[B[m*i][m*j] for j in range(5)] for i in range(5)]==block
   for i in range(N):
    for j in range(N):assert B[i][j]==forced_formula(N,w,G,i,j);denseentries+=1
  F=[pow(eta,i*j,P) for i in range(5) for j in range(5)];C=[pow(eta,(-3*(i+j)**2)%5,P) for i in range(5) for j in range(5)];D=[pow(eta,(-3*i*i)%5,P) if i==j else 0 for i in range(5) for j in range(5)];assert C[1]*pow(F[1],-1,P)%P!=C[2]*pow(F[2],-1,P)%P
  blocks.append({'N':N,'prime':P,'G':G,'eta':eta,'target_guard':(1+N*G)%P})
 out['five_coordinate_blocks']=blocks;out['direct_inverse_entries']=denseentries
 # CRT square identity with no guessed Gauss sign and all q^2 summands included.
 square=[]
 for q in [1,3,7,9,11,13,17,21]:
  N=5*q*q;P,w0=field_for(N)
  for a in [1,2,N-1]:
   w=pow(w0,a,P);h=(N+1)//2;m=q*q;eta=pow(w,q**4,P);G=gauss(N,w);g5=sum(pow(eta,3*j*j,P) for j in range(5))%P;assert G==q*g5%P
   xi=pow(w,5,P);sq=sum(pow(xi,5*h*v*v,P) for v in range(m))%P;assert sq==q%P
   assert len({(m*u+5*v)%N for u in range(5) for v in range(m)})==N
   for s in range(q):
    inner=sum(pow(xi,(q*2*5*h*s*t)%(q*q),P) for t in range(q))%P if q>1 else 1
    assert inner==(q%P if s==0 else 0)
   square.append({'q':q,'N':N,'prime':P,'root':w,'eta':eta,'Gauss_N':G,'q_times_Gauss5':q*g5%P})
 out['square_CRT_records']=square
 # Symbolic specialization of the five-by-five coefficient curve modulo q-1.
 P=241;eta=91;g5=sum(pow(eta,3*j*j,P) for j in range(5))%P;assert g5==103
 symbolic=0
 for i in range(5):
  for j in range(5):
   F=pow(eta,i*j,P);C=pow(eta,(-3*(i+j)**2)%5,P);D=pow(eta,(-3*i*i)%5,P) if i==j else 0;num=[F,(-g5*C)%P,0,5*g5*D%P];den=[1,0,0,5*g5%P];assert sum(den)%P==34;value=sum(num)*pow(34,-1,P)%P;assert value==forced_formula(5,eta,g5,i,j);symbolic+=1
 out['symbolic_q_minus_one_entry_reductions']=symbolic;out['good_reduction_denominator']=34
 out['example_infinite_lengths']=[{'k':k,'q':2410*k+1,'N':5*(2410*k+1)**2} for k in [0,1,2,10]]
 for x in out['example_infinite_lengths']:assert x['q']%2==1 and math.gcd(x['q'],5)==1 and x['q']%241==1
 path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('INDEPENDENT_RESULTS.json');path.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['gauss_sign_records','square_CRT_records']},indent=2))
if __name__=='__main__':main()
