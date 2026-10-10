"""Fresh reviewer algebra/structural checks. Source programs remain inert."""
import json,random,math
P=65537

def E(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def mm(A,B):return [[sum(x*y for x,y in zip(r,c))%P for c in zip(*B)] for r in A]
def iv(A):
 n=len(A);T=[[v%P for v in r]+E(n)[i] for i,r in enumerate(A)]
 for j in range(n):
  ks=[i for i in range(j,n) if T[i][j]]
  if not ks:raise ValueError('singular')
  k=ks[0];T[k],T[j]=T[j],T[k];z=pow(T[j][j],-1,P);T[j]=[v*z%P for v in T[j]]
  for i in range(n):
   if i!=j:
    z=T[i][j];T[i]=[(a-z*b)%P for a,b in zip(T[i],T[j])]
 return [r[n:] for r in T]
def rank(A):
 if not A or not A[0]:return 0
 T=[r[:] for r in A];m=len(T);k=0
 for j in range(len(T[0])):
  ks=[i for i in range(k,m) if T[i][j]]
  if not ks:continue
  u=ks[0];T[k],T[u]=T[u],T[k];z=pow(T[k][j],-1,P);T[k]=[v*z%P for v in T[k]]
  for i in range(k+1,m):
   z=T[i][j];T[i]=[(a-z*b)%P for a,b in zip(T[i],T[k])]
  k+=1
  if k==m:break
 return k

def hidden():
 cuts=entries=blocks=0
 for n in (2,4,8,16,32,64):
  m=n//2;tau=[j for a in range(m) for j in (a,a+m)];T=[[3 if i==j else -1 if abs(i-j)==1 else 0 for j in range(n)] for i in range(n)]
  TT=[[T[tau[i]][tau[j]] for j in range(n)] for i in range(n)]
  for i in range(n):
   for j in range(n):
    z=3 if i==j else -1 if abs(i-j)==2 or {i,j}=={1,n-2} else 0
    assert TT[i][j]==z;entries+=1
  G=iv(T);e=pow(20,-1,P);MG=[[(G[i][j]+e*G[tau[i]][tau[j]])%P for j in range(n)] for i in range(n)]
  for k in range(1,n):
   assert rank([r[k:] for r in TT[:k]])<=3
   assert rank([r[k:] for r in MG[:k]])<=4;cuts+=1
  if n>=8:
   w=pow(3,(P-1)//n,P);F=[[pow(w,tau[i]*tau[j],P) for j in range(n)] for i in range(n)]
   assert rank([r[:m] for r in F[:m]])==rank([r[m:] for r in F[:m]])==m;blocks+=2
 return dict(path_entries=entries,all_prefix_cuts=cuts,full_fourier_halfblocks=blocks)

def reduction():
 rng=random.Random(187009);cases=singular=0
 for n in range(2,14):
  for _ in range(20):
   A=E(n);C=E(n)
   for i in range(1,n):A[i][i-1]=-rng.randrange(7)%P;C[i-1][i]=-rng.randrange(7)%P
   b=[rng.randrange(7) for i in range(n)];e=[rng.randrange(1,7) for i in range(n)];d=[rng.randrange(7) for i in range(n)]
   Ai=iv(A);Ci=iv(C);Ei=[[pow(e[i],-1,P)*int(i==j)%P for j in range(n)] for i in range(n)]
   H=[[(Ai[i][j]*b[j]+Ci[i][j]*e[j]+int(i==j)*d[j])%P for j in range(n)] for i in range(n)]
   K=mm(mm(mm(A,H),Ei),C)
   assert all(K[i][j]==0 for i in range(n) for j in range(n) if abs(i-j)>1)
   assert mm(mm(iv(A),K),[[Ci[i][j]*e[j]%P for j in range(n)] for i in range(n)])==H
   try:Ki=iv(K)
   except ValueError:singular+=1
   else:assert mm(mm(mm(Ei,C),Ki),A)==iv(H)
   cases+=1
 return dict(cases=cases,singular_retained=singular)

def pruned(n,items,w):
 L=n.bit_length()-1;active={int(f'{i:0{L}b}'[::-1],2):a%P for i,a in items};counts=[]
 for s in range(1,L+1):
  B=1<<s;h=B//2;pairs=set()
  for i in active:pairs.add((i//B)*B+i%h)
  nxt={}
  for a in pairs:
   j=a%B;v=active.get(a,0);z=active.get(a+h,0)*pow(w,j*n//B,P)%P;nxt[a]=(v+z)%P;nxt[a+h]=(v-z)%P
  counts.append(len(pairs));active=nxt
 return [active.get(j,0) for j in range(n)],counts

def prunecheck():
 rng=random.Random(178044);cases=coordinates=0
 for L in range(1,9):
  n=1<<L;w=pow(3,(P-1)//n,P)
  for k in sorted(set((0,1,2,min(5,n),n//2,n))):
   for _ in range(3):
    inds=rng.sample(range(n),k);items=[(j,rng.randrange(P)) for j in inds];y,c=pruned(n,items,w)
    assert y==[sum(a*pow(w,j*t,P) for j,a in items)%P for t in range(n)]
    assert all(z<=min(n//2,k*(1<<s)) for s,z in enumerate(c))
    assert sum(c)<=n*(2+math.log2(max(1,k)))
    cases+=1;coordinates+=n
 return dict(cases=cases,coordinates=coordinates)

if __name__=='__main__':
 d={'status':'PASS','hidden_order':hidden(),'tridiagonal_reduction':reduction(),'pruned_fft':prunecheck(),'scope':'Exact reviewer checks; no source-program execution, original benchmark replay or finite-word transcendental implementation certification.'}
 print(json.dumps(d,sort_keys=True,indent=2));open('INDEPENDENT_RESULTS.json','w').write(json.dumps(d,sort_keys=True,indent=2)+'\n')
