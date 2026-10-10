#!/usr/bin/env python3
"""Independent sparse-residual/series/Green checks; no uploaded imports."""
import pathlib,json,random,math
R=pathlib.Path(__file__).resolve().parent

def prime(n):return n>=2 and all(n%d for d in range(2,math.isqrt(n)+1))
def field(n):
 length=2*(1<<(n-1).bit_length());multiple=math.lcm(n,length);k=max(1,1000000//multiple)
 while not prime(k*multiple+1):k+=1
 p=k*multiple+1;f=[q for q in range(2,n+1) if n%q==0 and prime(q)]
 for g in range(2,p):
  w=pow(g,(p-1)//n,p)
  if all(pow(w,n//q,p)!=1 for q in f):return p,w,length

def inverse(A,p):
 n=len(A);X=[[v%p for v in A[i]]+[int(i==j) for j in range(n)] for i in range(n)];det=1
 for j in range(n):
  i=next(i for i in range(j,n) if X[i][j]);det=det*(-1 if i!=j else 1)*X[i][j]%p;X[i],X[j]=X[j],X[i];u=pow(X[j][j],-1,p);X[j]=[v*u%p for v in X[j]]
  for i in range(n):
   if i!=j:
    u=X[i][j];X[i]=[(a-u*b)%p for a,b in zip(X[i],X[j])]
 return [row[n:] for row in X],det

def mm(A,B,p):return [[sum(x*y for x,y in zip(a,b))%p for b in zip(*B)] for a in A]
def mv(A,x,p):return [sum(a*b for a,b in zip(row,x))%p for row in A]
def poly(a,b,p):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]=(c[i+j]+x*y)%p
 return c

def add(a,b,p):return [((a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0))%p for i in range(max(len(a),len(b)))]
def rational(r,w,p):
 pairs=[([v],[1,-pow(w,j,p)%p]) for j,v in enumerate(r) if v]
 if not pairs:return [0]*len(r),[0],[1]
 K=len(pairs)
 while len(pairs)>1:
  nxt=[]
  for i in range(0,len(pairs),2):
   if i+1==len(pairs):nxt.append(pairs[i]);continue
   A,B=pairs[i];C,D=pairs[i+1];nxt.append((add(poly(A,D,p),poly(C,B,p),p),poly(B,D,p)))
  pairs=nxt
 A,B=pairs[0];H=1<<(K-1).bit_length();U=[1]+[0]*(H-1)
 for j in range(1,H):U[j]=-sum(B[i]*U[j-i] for i in range(1,min(j,K)+1))%p
 z=(poly(A,U,p)+[0]*H)[:H]
 while len(z)<len(r):
  s=len(z);old=z[s-K:s];cross=poly(B,old,p);c=[cross[K+j] if K+j<len(cross) else 0 for j in range(H)];new=poly([(-x)%p for x in c],U,p);z.extend(new[:H])
 return z[:len(r)],A,B

def reverse_solver(diag,b,rhs,p):
 n=len(diag);bi=pow(b,-1,p);z=[];h=[];indices=[];u=0;v=1
 for k in reversed(range(n)):
  u=(rhs[k]-diag[k]*u)*bi%p;v=-diag[k]*v*bi%p;z.append(u);h.append(v);indices.append((k-1)%n)
 c=z[-1]*pow(1-h[-1],-1,p)%p;out=[0]*n
 for i,u,v in zip(indices,z,h):out[i]=(u+v*c)%p
 return out

def operators(n,p,w):
 powers=[pow(w,j,p) for j in range(n)];ld=[(7+powers[j])%p for j in range(n)];pd=[(7+2*powers[-j%n])%p for j in range(n)]
 L=[[((ld[i] if j==i else 0)+(2 if j==(i-1)%n else 0))%p for j in range(n)] for i in range(n)]
 P=[[((pd[i] if j==i else 0)+(1 if j==(i-1)%n else 0))%p for j in range(n)] for i in range(n)]
 return L,P,ld,pd

rng=random.Random(2217);cases=[];identities=0;outputs=0
for n in [2,3,5,7,8,15,16,17,30,31]:
 p,w,convroot=field(n);F=[[pow(w,i*j,p) for j in range(n)] for i in range(n)];L,P,ld,pd=operators(n,p,w);Li,_=inverse(L,p);Pi,_=inverse(P,p);assert mm(L,F,p)==mm(F,P,p);identities+=n*n
 for K in sorted(set([0,1,2,min(3,n),n])):
  idx=list(range(n));rng.shuffle(idx);r=[0]*n
  for j in idx[:K]:r[j]=rng.randrange(1,p)
  x=mv(Pi,r,p);observed=mv(P,x,p);assert observed==r
  z,A,B=rational(observed,w,p);assert z==mv(F,r,p)
  y=mv(Li,z,p);assert y==mv(F,x,p);assert reverse_solver(ld,2,z,p)==y
  if K==1:assert all(x)
  outputs+=n
  cases.append({'N':n,'K':K,'field':p,'root':w,'available_convolution_length':convroot,'all_outputs_match':True,'dense_input':all(x)})
# Explicit invertible-operator/zero-diagonal exception and a complete reverse-direction repair.
p=17;n=16;w=3;L,P,ld,pd=operators(n,p,w);Li,detL=inverse(L,p);Pi,detP=inverse(P,p);assert detL==detP==16
for b,diag,invmat in [(2,ld,Li),(1,pd,Pi)]:
 for j in range(n):
  rhs=[int(i==j) for i in range(n)];assert reverse_solver(diag,b,rhs,p)==mv(invmat,rhs,p)
exception={'field':p,'N':n,'root':w,'L_zero_diagonal_indices':[i for i,x in enumerate(ld) if not x],'P_zero_diagonal_indices':[i for i,x in enumerate(pd) if not x],'det_L':detL,'det_P':detP,'reverse_solver_basis_cases':32}
assert exception['L_zero_diagonal_indices']==[3] and exception['P_zero_diagonal_indices']==[11]
out={'cases':cases,'exact_identity_entries':identities,'exact_output_entries':outputs,'zero_diagonal_exception':exception,'uploaded_code_executed':False,'audit_polynomial_multiplication':'Naive independently authored reference; no speed claim for checker'}
(R/'INDEPENDENT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'sparse_residual_cases':len(cases),'exact_identity_entries':identities,'exact_output_entries':outputs,'zero_diagonal_exception':exception},indent=2))
