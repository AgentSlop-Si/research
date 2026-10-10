"""Independent baseline controls: no uploaded programs or fixtures are imported."""
import json, random
from fractions import Fraction as Q
P=65537

def mul(A,B,p=P):return [[sum(x*y for x,y in zip(r,c))%p for c in zip(*B)] for r in A]
def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def inv(A,p=P):
 n=len(A);T=[[(a%p) for a in r]+eye(n)[i] for i,r in enumerate(A)]
 for j in range(n):
  k=next(i for i in range(j,n) if T[i][j]);T[j],T[k]=T[k],T[j];z=pow(T[j][j],-1,p);T[j]=[a*z%p for a in T[j]]
  for i in range(n):
   if i!=j:
    z=T[i][j];T[i]=[(a-z*b)%p for a,b in zip(T[i],T[j])]
 return [r[n:] for r in T]
def F(n,w):return [[pow(w,i*j,P) for j in range(n)] for i in range(n)]
def dft(x,w):return [sum(a*pow(w,j*k,P) for j,a in enumerate(x))%P for k in range(len(x))]
def rev(j,L):return int(f'{j:0{L}b}'[::-1],2) if L else 0
def C(n):
 L=n.bit_length()-1;return [[1 if (i&rev(j,L)).bit_count()%2==0 else P-1 for j in range(n)] for i in range(n)]
def valuation(j):return (j&-j).bit_length()-1

def blocks():
 entries=outputs=0
 for L in range(1,8):
  n=1<<L;w=pow(3,(P-1)//n,P);FN=F(n,w);CN=C(n);ni=pow(n,-1,P);U=[[a*ni%P for a in r] for r in mul(FN,CN)]
  BS={}
  for s in range(L):
   m=n//(2**(s+1));wm=pow(w,n//m,P);z=pow(w,n//(2*m),P);mi=pow(m,-1,P)
   BS[s]=[[a*mi%P for a in r] for r in mul([[a*pow(z,j,P)%P for j,a in enumerate(r)] for r in F(m,wm)],C(m))]
  for k in range(n):
   for j in range(n):
    expected=1 if k==j==0 else 0
    if k and j and valuation(k)==valuation(j):
     s=valuation(k);expected=BS[s][(k//2**s-1)//2][(j//2**s-1)//2]
    assert U[k][j]==expected;entries+=1
  assert 2*(n-1)+sum(t*(1<<t) for t in range(L))==n*L
  assert sum((1<<t)-1 for t in range(L))==n-1-L
  for b in range(n):
   x=[int(j==b) for j in range(n)];a=x[:];y=[0]*n
   while len(a)>1:
    m=len(a)//2;s=[(a[j]+a[j+m])%P for j in range(m)];d=[(a[j]-a[j+m])%P for j in range(m)]
    z=pow(w,n//(2*m),P);v=dft([d[j]*pow(z,j,P)%P for j in range(m)],pow(z,2,P))
    for k,vk in enumerate(v):y[(2*k+1)*n//(2*m)]=vk
    assert [((s[j]+d[j])*pow(2,-1,P))%P for j in range(m)]+[((s[j]-d[j])*pow(2,-1,P))%P for j in range(m)]==a
    a=s
   y[0]=a[0];assert y==[FN[k][b] for k in range(n)];outputs+=n
 return dict(block_entries=entries,detail_outputs=outputs)

def forcing():
 rng=random.Random(90471);cases=outputs=0
 for L in range(1,8):
  n=1<<L;q=pow(3,(P-1)//n,P)
  for typ in range(n+5):
   rb=[int(j==typ) for j in range(n)] if typ<n else [rng.randrange(P) for j in range(n)]
   qp=[1]
   for j in range(1,n):qp.append(qp[-1]*q%P)
   x=[0]*n;x[-1]=rb[0]
   for j in range(n-1,0,-1):x[j-1]=(rb[j]-(qp[j]-1)*x[j])%P
   count={'mul':n-1,'add':0,'sub':0};r=[]
   for j in range(1,n):r.append(((qp[j]-1)*x[j]+x[j-1])%P);count['sub']+=1;count['mul']+=1;count['add']+=1
   values=[x[-1]]*n;s=0
   for j,a in enumerate(r,1):
    if not a:continue
    s+=1;v=a
    for k in range(n):
     values[k]=(values[k]+v)%P;count['add']+=1
     if k<n-1:v=v*qp[j]%P;count['mul']+=int(k<n-1)
   y=[0]*n;y[1]=values[0]
   for k in range(1,n):y[(k+1)%n]=((1-qp[k])*y[k]+values[k])%P;count['sub']+=1;count['mul']+=1;count['add']+=1
   assert y==dft(x,q)
   assert count=={'mul':(s+3)*(n-1),'add':s*n+2*(n-1),'sub':2*(n-1)}
   cases+=1;outputs+=n
 return dict(cases=cases,outputs=outputs)

def scan_and_inverse():
 rng=random.Random(84013);scan=wood=general=0
 for n in range(2,15):
  for t in range(1,8):
   for _ in range(3):
    factors=[]
    for a in range(t):
     A=[[0]*n for _ in range(n)]
     for i in range(n):
      A[i][i]=rng.randrange(1,P)
      if i:A[i][i-1]=rng.randrange(P)
     perm=rng.sample(range(n),n);B=[[A[i][perm[j]] for j in range(n)] for i in range(n)];factors.append(B)
    M=eye(n)
    for A in factors:M=mul(M,A)
    assert max(sum(bool(v) for v in r) for r in M)<=2**t
    assert min(sum(bool(v) for v in r) for r in M)<=2**(t-1);scan+=1
  # Source inverse identity for deliberately noncommuting invertible matrices.
  A=[[10 if i==j else -1 if abs(i-j)==1 else 0 for j in range(n)] for i in range(n)]
  perm=rng.sample(range(n),n);B=[[A[perm[i]][perm[j]] for j in range(n)] for i in range(n)]
  Ai=inv(A);Bi=inv(B);e=pow(20,-1,P);M=[[(Ai[i][j]+e*Bi[i][j])%P for j in range(n)] for i in range(n)]
  core=[[(B[i][j]+e*A[i][j])%P for j in range(n)] for i in range(n)];Mi=mul(mul(B,inv(core)),A)
  assert mul(M,Mi)==mul(Mi,M)==eye(n);general+=1
  K=[[10 if i==j else -1 if abs(i-j)==1 else -2 if abs(i-j)==2 else 0 for j in range(n)] for i in range(n)]
  U=[[int(i==0),int(i==n-1)] for i in range(n)];UT=list(map(list,zip(*U)));CC=[[0,P-1],[P-1,0]];Ki=inv(K);W=mul(Ki,U)
  tiny=mul(UT,W);tiny=[[(tiny[i][j]+CC[i][j])%P for j in range(2)] for i in range(2)]
  correction=mul(mul(mul(W,inv(tiny)),UT),Ki);R=[[(Ki[i][j]-correction[i][j])%P for j in range(n)] for i in range(n)]
  update=mul(mul(U,CC),UT);actual=[[(K[i][j]+update[i][j])%P for j in range(n)] for i in range(n)]
  assert mul(actual,R)==mul(R,actual)==eye(n);wood+=1
 return dict(scan_words=scan,generic_inverse_sum_cases=general,woodbury_cases=wood)

def cap():
 c=0
 for L in range(1,33):
  b=(L-1).bit_length();q=1-Q(L,2**b)
  assert Q(L,2**b)>Q(1,2)
  for R in range(1,6):
   tprob=sum(q**j/Q(2**b) for j in range(R));success=1-q**R
   assert tprob/success==Q(1,L);c+=1
 return c
if __name__=='__main__':
 d={'status':'PASS','dyadic_details':blocks(),'forcing':forcing(),'inverse':scan_and_inverse(),'conditional_sampler_cases':cap(),'scope':'Fresh checks of specified algebra, not execution of source code, saved benchmarks, or full external theorems.'}
 print(json.dumps(d,sort_keys=True,indent=2));open('INDEPENDENT_RESULTS.json','w').write(json.dumps(d,sort_keys=True,indent=2)+'\n')
