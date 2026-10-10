#!/usr/bin/env python3
"""Independent bank invariants and striped Fourier cuts; no source imports."""
import pathlib,json
ROOT=pathlib.Path(__file__).resolve().parent;P=65537
def identity(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def mm(a,b,p=P):
 bt=list(zip(*b));return [[sum(x*y for x,y in zip(row,col))%p for col in bt] for row in a]
def sub(a,b,p=P):return [[(x-y)%p for x,y in zip(r,s)] for r,s in zip(a,b)]
def rank(a,p=P):
 a=[r[:] for r in a];rr=0
 for j in range(len(a[0])):
  k=next((k for k in range(rr,len(a)) if a[k][j]%p),None)
  if k is None:continue
  a[rr],a[k]=a[k],a[rr];iv=pow(a[rr][j],-1,p);a[rr]=[x*iv%p for x in a[rr]]
  for k in range(rr+1,len(a)):
   c=a[k][j]
   if c:a[k]=[(x-c*y)%p for x,y in zip(a[k],a[rr])]
  rr+=1
  if rr==len(a):break
 return rr
def inv(a,p=P):
 n=len(a);a=[r[:]+s for r,s in zip(a,identity(n))]
 for j in range(n):
  k=next(k for k in range(j,n) if a[k][j]%p);a[j],a[k]=a[k],a[j]
  v=pow(a[j][j],-1,p);a[j]=[v*x%p for x in a[j]]
  for k in range(n):
   if k!=j:
    c=a[k][j];a[k]=[(x-c*y)%p for x,y in zip(a[k],a[j])]
 return [r[n:] for r in a]
def power4(a,p=P):a2=mm(a,a,p);return mm(a2,a2,p)
def fourier(n,p=P,gen=3):
 w=pow(gen,(p-1)//n,p);assert pow(w,n,p)==1 and(n==1 or pow(w,n//2,p)!=1)
 return [[pow(w,i*j,p) for j in range(n)] for i in range(n)]

bank_cases=[]
for n,m in [(4,2),(8,2),(8,4),(16,4),(16,8),(32,8)]:
 q=n//m;small=fourier(m);Q=identity(n)
 for j in range(n-1):Q[j+1][j]=(j+2)%P
 Qi=inv(Q)
 for active in [[],[0],list(range(0,q,2)),list(range(q))]:
  B=identity(n);E=[[0]*n for _ in range(n)]
  for b in active:
   for i in range(m):
    E[b*m+i][b*m+i]=1
    for j in range(m):B[b*m+i][b*m+j]=small[i][j]
  K=mm(mm(Qi,B),Q);I=identity(n);Pi=[[x*pow(m*m-1,-1,P)%P for x in row] for row in sub(power4(K),I)]
  assert Pi==mm(mm(Qi,E),Q)
  assert mm(Pi,Pi)==Pi and rank(Pi)==m*len(active)
  assert mm(sub(K,I),sub(I,Pi))==[[0]*n for _ in range(n)]
  assert rank(sub(K,I))==m*len(active)
  K2=mm(K,K);assert sum(K2[j][j] for j in range(n))%P==(n+m*len(active))%P
  bank_cases.append({'N':n,'m':m,'active_blocks':active,'projector_rank':m*len(active)})

# Exact projector false positive: wrong active Fourier spectrum.
p=17;K=[[0]*4 for _ in range(4)]
for j,x in enumerate([6,7,1,1]):K[j][j]=x
I=identity(4);Pi=[[x*pow(3,-1,p)%p for x in row] for row in sub(power4(K,p),I,p)]
assert mm(Pi,Pi,p)==Pi and rank(Pi,p)==2
assert mm(sub(K,I,p),sub(I,Pi,p),p)==[[0]*4 for _ in range(4)]
tr2=sum(mm(K,K,p)[j][j] for j in range(4))%p;assert tr2==2 and tr2!=6
# Normalized F2 has fourth power I and loses the active selector contrast.
F2=[[1,1],[1,p-1]];Fn=[[x*pow(6,-1,p)%p for x in row] for row in F2]
assert power4(Fn,p)==identity(2)

striped=[]
for k in range(2,10):
 n=1<<k;m=1<<(k//2);q=n//m;t=q//2;L=m//t;assert m%t==0
 R=[int(format(i,f'0{k}b')[::-1],2) for i in range(n)]
 first={j for j in range(n) if(j//m)%2==0};other=set(range(n))-first
 natural=[(j+1)%n for j in range(n)];bitrev=[R[(R[j]+1)%n] for j in range(n)]
 enter=lambda pi:sum(j in other and pi[j] in first for j in range(n))
 assert enter(natural)==q//2 and enter(bitrev)==m
 w=pow(3,(P-1)//n,P)
 a=[[pow(w,i*j,P) for j in sorted(other)] for i in sorted(first)]
 actual=rank(a);assert actual==n//2
 eta=pow(w,t*t,P);assert pow(eta,2*L,P)==1 and pow(eta,L,P)!=1
 assert rank([[pow(eta,b*d,P) for d in range(L)] for b in range(L)])==L
 cap=2*q+4*m
 if n>=256:assert cap<n//2
 striped.append({'N':n,'m':m,'q':q,'natural_incoming':q//2,'bitrev_cycle_incoming':m,'four_layer_rank_cap':cap,'Fourier_cross_rank':actual,'strict_exclusion':cap<actual,'small_Vandermonde_block_size':L})

out={'field':P,'abstract_bank_similarity_cases':bank_cases,
 'projector_false_positive':{'field':17,'K_diagonal':[6,7,1,1],'projector_rank':2,'trace_K_squared':2,'required_even_F2_bank_trace':6},
 'normalized_F2_fourth_power_identity':True,'striped_bank_cases':striped,
 'scope':'Necessary bank conditions and a restricted cycle/endpoint exclusion; no constructed paired-Green Fourier factorization.',
 'uploaded_code_executed':False}
(ROOT/'INDEPENDENT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
