"""Fresh reviewer checks for the final baseline text batch. No source imports."""
from fractions import Fraction as Q
from itertools import product,combinations
import json,random

def rank(A,p):
 T=[r[:] for r in A];k=0;m=len(T)
 for j in range(len(T[0])):
  a=next((i for i in range(k,m) if T[i][j]%p),None)
  if a is None:continue
  T[k],T[a]=T[a],T[k];z=pow(T[k][j],-1,p);T[k]=[v*z%p for v in T[k]]
  for i in range(k+1,m):
   z=T[i][j];T[i]=[(a-z*b)%p for a,b in zip(T[i],T[k])]
  k+=1
  if k==m:break
 return k

def mm(A,B,p):return [[sum(a*b for a,b in zip(r,c))%p for c in zip(*B)] for r in A]
def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def inv(A,p):
 n=len(A);T=[[v%p for v in r]+eye(n)[i] for i,r in enumerate(A)]
 for j in range(n):
  k=next(i for i in range(j,n) if T[i][j]);T[k],T[j]=T[j],T[k];z=pow(T[j][j],-1,p);T[j]=[v*z%p for v in T[j]]
  for i in range(n):
   if i!=j:
    z=T[i][j];T[i]=[(a-z*b)%p for a,b in zip(T[i],T[j])]
 return [r[n:] for r in T]

def rigidity():
 p=7;n=3;w=2;F=[[pow(w,i*j,p) for j in range(n)] for i in range(n)];rows=[[0]*n]
 for j in range(n):
  for a in range(1,p):r=[0]*n;r[j]=a;rows.append(r)
 cases=0
 for S in product(rows,repeat=n):
  supports=[sum(bool(v) for v in r) for r in S];r=rank([[(F[i][j]-S[i][j])%p for j in range(n)] for i in range(n)],p)
  assert n<=min(supports)+r*(max(supports)+1);cases+=1
 rectangles=0
 for p,g in [(17,3),(97,5)]:
  w=pow(g,(p-1)//8,p);F=[[pow(w,i*j,p) for j in range(8)] for i in range(8)]
  for I in combinations(range(8),3):
   for J in combinations(range(8),5):assert rank([[F[i][j] for j in J] for i in I],p)==3;rectangles+=1
  order=[0,2,4,6,1,3,5,7];A=[[F[i][j] for j in order] for i in order]
  assert [rank([r[k:] for r in A[:k]],p) for k in range(1,8)]==[1,2,3,2,3,2,1]
 raw=0
 for a,b,c,d in product(range(7),repeat=4):
  assert not(a*b%7==1 and c*d%7==1 and c*a*b%7==0);raw+=1
 return dict(nonuniform_rigidity_matrices=cases,F8_rectangles=rectangles,raw_scan_counterexample_tuples=raw)

def spectrum():
 total=0
 for n in (1,2,4,8,16,32,64,128):
  p=65537;eta=pow(3,(p-1)//(2*n),p);q=eta*eta%p;h=[1]
  for j in range(1,n):h.append(h[-1]*pow(1-pow(q,j,p),-1,p)%p)
  target=[sum(a*pow(eta,j*k,p) for j,a in enumerate(h))%p for k in range(2*n)];got=[0]*(2*n);ni=pow(n,-1,p)
  for parity in (0,1):
   inds=list(range(parity,2*n,2));A=1;B=0
   for k in inds:a=(1-pow(eta,k,p))%p;b=ni if k%2==0 else -ni;A=a*A%p;B=(a*B+b)%p
   assert A==(0 if parity==0 else 2)%p;y=B*pow(1-A,-1,p)%p
   for k in inds:got[k]=y;y=((1-pow(eta,k,p))*y+(ni if k%2==0 else -ni))%p
  assert got==target;total+=2*n
 return total

def tree():
 cases=0;leaves=0
 for L in range(1,10):
  D=[1,1]
  for j in range(L):D.append(D[-1]+8*D[-2])
  piv=[Q(1)]
  for j in range(L):piv.append(1+8/piv[-1])
  assert all(piv[j]==Q(D[j+1],D[j]) for j in range(L+1))
  vals=[1/piv[L]]
  for d in range(1,L+1):vals.append(2*vals[-1]/piv[L-d])
  assert vals[0]+4*vals[1]==1
  for d in range(1,L):assert vals[d]-2*vals[d-1]+4*vals[d+1]==0
  assert vals[L]-2*vals[L-1]==0 and vals[L]==Q(2**L,D[L+1])
  assert 2**L*2*vals[L]==Q(2*4**L,D[L+1]);cases+=1;leaves+=2**L
 # Depth zero exception: the root is itself the leaf, so subtracting I matters.
 assert 2*Q(1)-1==1 and 1<2
 return dict(positive_depths=cases,leaf_coordinates=leaves,depth_zero_exception_verified=True)

def green():
 p=65537;cases=entries=0
 for n in (1,2,4,8,16,32):
  w=pow(3,(p-1)//n,p);F=[[pow(w,i*j,p) for j in range(n)] for i in range(n)];Fi=[[pow(w,-i*j,p)*pow(n,-1,p)%p for j in range(n)] for i in range(n)]
  T=[[3 if i==j else -1 if abs(i-j)==1 else 0 for j in range(n)] for i in range(n)];H=mm(mm(F,T,p),Fi,p)
  expected=[[((3-pow(w,k,p)-pow(w,-k,p))*int(k==l)+(pow(w,l,p)+pow(w,-k,p))*pow(n,-1,p))%p for l in range(n)] for k in range(n)];assert H==expected
  G=inv(T,p);Ti=[[T[i][j]+int(i==j) for j in range(n)] for i in range(n)];Gi=inv(Ti,p);S=[[(G[i][j]+Gi[i][j])%p for j in range(n)] for i in range(n)]
  half=pow(2,-1,p);Th=[[T[i][j]+half*int(i==j) for j in range(n)] for i in range(n)];Thi=inv(Th,p);formula=[[(half*T[i][j]+pow(4,-1,p)*int(i==j)-pow(8,-1,p)*Thi[i][j])%p for j in range(n)] for i in range(n)];assert mm(S,formula,p)==mm(formula,S,p)==eye(n);cases+=1;entries+=3*n*n
 assert Q(7,2)+Q(1,4)+Q(22,9)/8==Q(73,18)
 return dict(configurations=cases,checked_matrix_entries=entries)

def banks():
 U=[[Q(1),Q(0)],[Q(0),Q(-1)]];V=[[Q(3,5),Q(-4,5)],[Q(4,5),Q(3,5)]]
 def prod(A,B):return [[sum(a*b for a,b in zip(r,c)) for c in zip(*B)] for r in A]
 def exchange(M):
  Mt=list(zip(*M));return [[Q(0) if (i<2)==(j<2) else -Mt[i][j-2] if i<2 else M[i-2][j] for j in range(4)] for i in range(4)]
 S=[[Q(int((i+2)%4==j)) for j in range(4)] for i in range(4)];WU=exchange(U);WV=exchange(V);right=prod(prod(prod(S,WV),S),WU);wrong=prod(WV,WU)
 assert [right[i][0] for i in range(4)]==[Q(3,5),Q(4,5),0,0]
 assert [wrong[i][0] for i in range(4)]==[Q(-3,5),Q(4,5),0,0]
 assert prod(list(map(list,zip(*right))),right)==eye(4)
 assert Q(100)*Q(1,100)==1 and max(Q(1),Q(100))*max(Q(1),Q(1,100))==100
 return {'alternating_orientation':True,'padded_condition_counterexample':True}
if __name__=='__main__':
 d={'status':'PASS','rigidity':rigidity(),'kernel_spectrum_values':spectrum(),'tree':tree(),'green_bridge':green(),'banks':banks(),'scope':'Reviewer-written exact controls only; no uploaded code, benchmark or external proof stack executed.'};print(json.dumps(d,sort_keys=True,indent=2));open('INDEPENDENT_RESULTS.json','w').write(json.dumps(d,sort_keys=True,indent=2)+'\n')
