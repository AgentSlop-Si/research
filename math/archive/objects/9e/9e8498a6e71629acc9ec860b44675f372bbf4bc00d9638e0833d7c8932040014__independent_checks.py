#!/usr/bin/env python3
"""Independently authored verifier. Never imports/executes uploaded code."""
import json,random,hashlib,pathlib,itertools
ROOT=pathlib.Path(__file__).resolve().parent
P=65537

def rank(A,p=P):
 A=[list(x) for x in A]
 if not A:return 0
 n=len(A);m=len(A[0]);r=0
 for c in range(m):
  j=next((j for j in range(r,n) if A[j][c]%p),None)
  if j is None:continue
  A[r],A[j]=A[j],A[r];q=pow(A[r][c],-1,p);A[r]=[x*q%p for x in A[r]]
  for j in range(r+1,n):
   q=A[j][c]%p
   if q:A[j]=[(x-q*y)%p for x,y in zip(A[j],A[r])]
  r+=1
  if r==n:break
 return r

def inv(A,p=P):
 n=len(A);B=[[x%p for x in A[i]]+[int(i==j) for j in range(n)] for i in range(n)]
 for c in range(n):
  j=next((j for j in range(c,n) if B[j][c]),None)
  if j is None:return None
  B[c],B[j]=B[j],B[c];q=pow(B[c][c],-1,p);B[c]=[x*q%p for x in B[c]]
  for j in range(n):
   if j!=c:
    q=B[j][c];B[j]=[(x-q*y)%p for x,y in zip(B[j],B[c])]
 return [r[n:] for r in B]

def mul(A,B,p=P):
 return [[sum(x*y for x,y in zip(a,b))%p for b in zip(*B)] for a in A]
def sub(A,R,C):return [[A[i][j] for j in C] for i in R]
def rev(i,m):return int(format(i,f'0{m}b')[::-1],2)
def perm(p):return [[int(i==p[j]) for j in range(len(p))] for i in range(len(p))]
def qs(n,rng):
 a,b,c,d,g,h=[[rng.randrange(0,7) for _ in range(n)] for _ in range(6)]
 X=[[0]*n for _ in range(n)]
 for i in range(n):
  X[i][i]=rng.randrange(0,11)
  for j in range(i):
   z=a[i]*b[j]
   for k in range(j+1,i):z=z*g[k]%P
   X[i][j]=z%P
  for j in range(i+1,n):
   z=c[i]*d[j]
   for k in range(i+1,j):z=z*h[k]%P
   X[i][j]=z%P
 return X

def check_bitrev():
 out=[];prev=None
 for m in range(1,19):
  n=1<<m
  if m%2:w=t=(n+1)//3
  else:w=2*((n//2+1)//3);t=w//2
  A=sum(rev(i,m)<t for i in range(w));B=sum(rev(i,m)<t for i in range(n-w,n))
  assert A-B==(m+1)//2
  if m%2:
   if prev:
    assert A==prev['w']+prev['A'] and B==prev['w']-1+prev['B']
   prev=dict(w=w,A=A,B=B)
  out.append(dict(m=m,N=n,W=w,T=t,A=A,B=B,discrepancy=A-B))
 n=128;w=43;root=pow(3,(P-1)//n,P)
 assert pow(root,n,P)==1 and pow(root,n//2,P)!=1
 F=[[pow(root,i*j,P) for j in range(n-w,n)] for i in range(w)]
 assert rank(F)==43
 return dict(counts=out,N128_fourier_rank=rank(F),field=P,N128_root=root)

def check_qs():
 rng=random.Random(921);inversion_cases=0;cyclic_cases=0;averages=0
 for n in [3,4,8,16]:
  for trial in range(10):
   stages=[qs(n,rng) for _ in range(3)]
   if trial==0:stages[0]=[[0]*n for _ in range(n)]
   for S in stages:
    T=inv(S)
    for k in range(1,n):
     assert rank(sub(S,range(k),range(k,n)))<=1
     assert rank(sub(S,range(k,n),range(k)))<=1
     if T:
      assert rank(sub(S,range(k),range(k,n)))==rank(sub(T,range(k),range(k,n)))
      assert rank(sub(S,range(k,n),range(k)))==rank(sub(T,range(k,n),range(k)))
      inversion_cases+=2
   p1=list(range(n));p2=list(range(n));rng.shuffle(p1);rng.shuffle(p2)
   q2=[p2.index(i) for i in range(n)]
   M=mul(mul(mul(mul(stages[2],perm(p2)),stages[1]),perm(p1)),stages[0])
   for w in range(1,n):
    I=list(range(w));R=[q2[i] for i in I]
    for t in range(n+1):
     a=sum(x<t for x in R);total=0
     for start in range(n):
      J=[(start+j)%n for j in range(w)];C=[p1[j] for j in J];b=sum(x<t for x in C);total+=b
      if (start+t+trial)%max(1,n//2)==0:
       actual=rank(sub(M,I,J));cap=4+w-abs(a-b)
       assert actual<=cap
       ext=rank(sub(stages[0],[i for i in range(n) if i not in J],J));assert ext<=2
       assert rank(sub(stages[1],R,C))<=1+w-abs(a-b)
       cyclic_cases+=1
     assert total==w*t;averages+=1
 # Singular-pivot but invertible separated-generator counterexample.
 L=[[1,0,0],[1,1,0],[0,1,1]]
 assert inv(L) is not None
 return dict(inverse_cut_rank_checks=inversion_cases,cyclic_matrix_rank_cases=cyclic_cases,exact_cyclic_average_cases=averages,separated_generator_counterexample=L)

def fast_cycle_solve(pi,diag,rhs):
 n=len(pi);seen=set();out=[0]*n
 for start in range(n):
  if start in seen:continue
  cycle=[];j=start
  while j not in seen:seen.add(j);cycle.append(j);j=pi[j]
  order=cycle[::-1];z=[];h=[];u=0;v=1
  for j in order:
   d=pow(diag[j],-1,P);u=(rhs[j]-2*u)*d%P;v=-2*v*d%P;z.append(u);h.append(v)
  c=z[-1]*pow(1-h[-1],-1,P)%P
  for j,u,v in zip(order,z,h):out[j]=(u+v*c)%P
 return out

def check_phase16():
 rng=random.Random(922);cases=0;entries=0;weyl=0
 for n in [2,4,8,16,32]:
  w=pow(3,(P-1)//n,P);assert pow(w,n,P)==1 and pow(w,n//2,P)!=1
  F=[[pow(w,i*j,P) for j in range(n)] for i in range(n)]
  perms=[list(range(n)),[(i-1)%n for i in range(n)],list(reversed(range(n)))]
  q=list(range(n));rng.shuffle(q);perms.append(q)
  for pi in perms:
   diag=[(7+pow(w,i,P))%P for i in range(n)]
   L=[[((diag[i] if j==i else 0)+(2 if j==pi[i] else 0))%P for j in range(n)] for i in range(n)]
   Li=inv(L);assert Li is not None
   B=mul(L,F);expected=[[F[i][j]*(7+pow(w,i,P)+2*pow(w,((pi[i]-i)*j)%n,P))%P for j in range(n)] for i in range(n)]
   assert B==expected and mul(Li,B)==F
   for j in range(n):assert fast_cycle_solve(pi,diag,[B[i][j] for i in range(n)])==[F[i][j] for i in range(n)]
   entries+=n*n;cases+=1
  # Signed Weyl atoms: (S^a D^b F)ij = omega^(b*(i-a)+(i-a)*j)
  # (F D^-a S^b)ij = omega^(i*(j+b)-a*(j+b)).
  for a,b in [(-3,2),(1,-4),(0,5),(7,-1),(-2,-2),(0,0)]:
   for i in range(n):
    for j in range(n):
     left=pow(w,(b*(i-a)+(i-a)*j)%n,P)
     right=pow(w,(i*(j+b)-a*(j+b))%n,P)
     assert left==right;weyl+=1
 return dict(permutation_green_cases=cases,exact_forcing_entries=entries,weyl_atom_entries=weyl,field=P,includes_fixed_points=True)

out={'bit_reversal':check_bitrev(),'quasiseparable':check_qs(),'hero1_phase16':check_phase16()}
(ROOT/'INDEPENDENT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
