"""Independently evaluate emitted equations and zero-component-safe identities.
Fresh standard-library code; does not import any research program.
"""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import json,random
ROOT=Path(__file__).resolve().parent
class K:
 def __init__(self,x=0):
  if isinstance(x,K):self.a=x.a
  elif isinstance(x,(list,tuple)):self.a=tuple(Q(v) for v in x)
  else:self.a=(Q(x),Q(0),Q(0),Q(0))
 def __add__(self,y):
  y=K(y);return K([a+b for a,b in zip(self.a,y.a)])
 __radd__=__add__
 def __neg__(self):return K([-a for a in self.a])
 def __sub__(self,y):return self+-K(y)
 def __rsub__(self,y):return K(y)+-self
 def __mul__(self,y):
  y=K(y);r=[Q(0)]*4
  for i,a in enumerate(self.a):
   for j,b in enumerate(y.a):r[(i+j)%4]+=a*b*(-1 if i+j>=4 else 1)
  return K(r)
 __rmul__=__mul__
 def __pow__(self,n):
  if n<0:return self.inv()**(-n)
  r=K(1);v=self
  while n:
   if n%2:r=r*v
   v=v*v;n//=2
  return r
 def inv(self):
  cols=[self*K([int(i==j) for i in range(4)]) for j in range(4)]
  M=[[cols[j].a[i] for j in range(4)]+[Q(i==0)] for i in range(4)]
  for c in range(4):
   k=next(k for k in range(c,4) if M[k][c]);M[c],M[k]=M[k],M[c]
   u=M[c][c];M[c]=[v/u for v in M[c]]
   for k in range(4):
    if k!=c:
     u=M[k][c];M[k]=[a-u*b for a,b in zip(M[k],M[c])]
  return K([M[i][4] for i in range(4)])
 def __truediv__(self,y):return self*K(y).inv()
 def __eq__(self,y):return self.a==K(y).a
 def __bool__(self):return any(self.a)
 def record(self):return [str(a) for a in self.a]
Z=K([0,1,0,0]);N=8;P=[7,0,6,3,4,1,2,5]
F=[[Z**(i*j) for j in range(N)] for i in range(N)]
def mm(A,B):return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def ident(n):return [[K(i==j) for j in range(n)] for i in range(n)]
def inverse(A):
 n=len(A);M=[list(row)+r for row,r in zip(A,ident(n))];det=K(1)
 for c in range(n):
  k=next((k for k in range(c,n) if M[k][c]),None)
  if k is None:raise ValueError('singular')
  if k!=c:M[c],M[k]=M[k],M[c];det=-det
  v=M[c][c];det*=v;M[c]=[a/v for a in M[c]]
  for k in range(n):
   if k!=c:
    v=M[k][c];M[k]=[a-v*b for a,b in zip(M[k],M[c])]
 return [r[n:] for r in M],det

def evalpoly(e,values):
 r=K()
 for t in e['terms']:
  a=K(t['coefficient'])
  for n in t['monomial']:a*=values[n]
  r+=a
 return r

def stage(values,s):
 return [[values[f'{s}_d{i}'] if i==j else (values[f'{s}_l{i}']*values[f'{s}_m{j}'] if i>j else values[f'{s}_u{i}']*values[f'{s}_v{j}']) for j in range(N)] for i in range(N)]
def minor(M,rs,cs):
 r,s=rs;a,b=cs;return M[r][a]*M[s][b]-M[r][b]*M[s][a]
def ladder(M):
 return all(not minor(M,[r,s],[a,b]) for r,s in combinations(range(N),2) for a,b in combinations(range(N),2) if s<a or r>b)
def lower_factors(M):
 R=[i for i in range(N) if any(M[i][j] for j in range(i))]
 C=[j for j in range(N) if any(M[i][j] for i in range(j+1,N))]
 l=[K() for _ in range(N)];m=[K() for _ in range(N)]
 if not R:return l,m
 rr=max(R);cc=min(C);pivot=M[rr][cc]
 if not pivot:return None
 for i in R:l[i]=M[i][cc]
 for j in C:m[j]=M[rr][j]/pivot
 if any(M[i][j]!=l[i]*m[j] for i in range(N) for j in range(i)):return None
 return l,m
def lift(M):
 lo=lower_factors(M);T=[list(r) for r in zip(*M)];up=lower_factors(T)
 return lo is not None and up is not None

assert Z**4==-1 and Z**8==1
assert all(Z**k!=1 for k in [1,2,4])
Finv=[[Z**(-i*j)/8 for j in range(N)] for i in range(N)]
assert mm(F,Finv)==ident(N) and mm(Finv,F)==ident(N)
_,detF=inverse(F)
original=json.load(open(ROOT/'ORIGINAL_IDEAL.json'));relaxed=json.load(open(ROOT/'RELAXED_QUADRICS.json'))
assert original['permutation']==P and len(original['equations'])==64
assert len(relaxed['equations'])==280
used={x for e in original['equations'] for t in e['terms'] for x in t['monomial']}
assert set(original['variables'])-used==set(original['unobservable_variables'])
rng=random.Random(202610181919);origchecks=0;quadchecks=0;invchecks=0;liftchecks=0
for trial in range(3):
 values={x:K(rng.randint(-3,4)) for x in original['variables']}
 A=stage(values,'A');B=stage(values,'B');BP=[[B[i][P[k]] for k in range(N)] for i in range(N)];T=mm(BP,A)
 for e in original['equations']:
  assert evalpoly(e,values)==T[e['row']][e['column']]-F[e['row']][e['column']];origchecks+=1
 assert lift(A) and lift(B);liftchecks+=2
for trial in range(2):
 C=[[K(rng.randint(-2,3)) for j in range(N)] for i in range(N)];FC=mm(F,C)
 B=[[FC[i][P.index(j)] for j in range(N)] for i in range(N)]
 values={f'c{i}_{j}':C[i][j] for i in range(N) for j in range(N)}
 for e in relaxed['equations']:
  if e['stage']=='C':v=minor(C,e['rows'],e['columns'])
  else:v=minor(B,e['rows'],e['columns_in_B'])
  assert evalpoly(e,values)==v;quadchecks+=1
# Zero-component control: cumulative lower stage has a non-liftable bidiagonal inverse.
A=[[K(i>=j) for j in range(N)] for i in range(N)]
C,detA=inverse(A)
assert detA==1 and mm(A,C)==ident(N) and mm(C,A)==ident(N)
assert lift(A) and ladder(C) and not lift(C)
assert C[1][0]==-1 and C[2][1]==-1 and C[2][0]==0
for trial in range(4):
 values={x:K(rng.randint(-3,4)) for x in original['variables']};A=stage(values,'A')
 try:C,detA=inverse(A)
 except ValueError:continue
 assert mm(A,C)==ident(N) and mm(C,A)==ident(N) and ladder(C);invchecks+=140
 assert lift(A);liftchecks+=1
# All zero lower/upper blocks are permitted, including invertible diagonals.
D=[[K(i+1 if i==j else 0) for j in range(N)] for i in range(N)]
assert lift(D) and ladder(D)
patterns=1
for r in range(1,128):
 R=[i+1 for i in range(7) if r>>i&1]
 for c in range(1,128):
  S=[i for i in range(7) if c>>i&1]
  if min(S)<min(R) and max(S)<max(R):patterns+=1
results=dict(status='exact encoding and necessary-reduction checks passed; target membership undecided',field='Q[z]/(z^4+1)',determinant_F8=detF.record(),inverse_permutation=[P.index(j) for j in range(N)],original_polynomial_evaluations=origchecks,relaxation_polynomial_evaluations=quadchecks,random_inverse_ladder_checks=invchecks,zero_pattern_stage_lift_checks=liftchecks,all_zero_triangle_control=True,nonliftable_inverse_boundary_control=True,observable_original_variables=len(used),original_equations=64,relaxed_quadrics=280,possible_nonempty_or_zero_support_patterns_per_triangle=patterns,naive_four_triangle_pattern_combinations=patterns**4)
(ROOT/'CHECKS.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2))
