"""Fresh REVIEW-09 exact checks. Read only inert JSON; execute no inherited code."""
from pathlib import Path
from fractions import Fraction as Q
from math import isqrt
import json, hashlib, ast
D=Path(__file__).resolve().parents[1]; I=D/'inputs'; OUT={}
def load(glob):return json.loads(next(I.glob(glob)).read_text())
def ga(x,y):return (x[0]+y[0],x[1]+y[1])
def gm(x,y):return (x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def mm(A,B):return [[tuple(map(sum,zip(*(gm(x,y) for x,y in zip(row,col))))) for col in zip(*B)] for row in A]
def l1(x):return abs(x[0])+abs(x[1])
# Four quadratic extension generators; d_j are in the earlier tower.
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def neg(a):return tuple(-x for x in a)
def sub(a,b):return add(a,neg(b))
def ds(n):
 if n==1:return (Q(-1),)
 a=[Q(0)]*n;a[0]=1;a[1]={2:-2,4:8,8:-16}[n];return tuple(a)
def mult(a,b):
 if len(a)==1:return (a[0]*b[0],)
 n=len(a)//2;a0,a1=a[:n],a[n:];b0,b1=b[:n],b[n:]
 return add(mult(a0,b0),mult(ds(n),mult(a1,b1)))+add(mult(a0,b1),mult(a1,b0))
def invert(a):
 if len(a)==1:
  assert a[0];return (1/a[0],)
 n=len(a)//2;x,y=a[:n],a[n:];g=invert(sub(mult(x,x),mult(ds(n),mult(y,y))));return mult(x,g)+neg(mult(y,g))
def const(n):return (Q(n),)+(Q(0),)*15
zero=const(0);one=const(1)
def gen(k):return tuple(Q(i==k) for i in range(16))
def parse(s):
 def visit(n):
  if isinstance(n,ast.Constant) and type(n.value)==int:return const(n.value)
  if isinstance(n,ast.Name) and n.id=='I':return gen(1)
  if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub):return neg(visit(n.operand))
  if isinstance(n,ast.BinOp):
   a,b=visit(n.left),visit(n.right)
   if isinstance(n.op,ast.Add):return add(a,b)
   if isinstance(n.op,ast.Sub):return sub(a,b)
   if isinstance(n.op,ast.Mult):return mult(a,b)
   if isinstance(n.op,ast.Div):return mult(a,invert(b))
  if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='sqrt' and len(n.args)==1 and not n.keywords:
   a=visit(n.args[0]);roots={add(one,mult(const(-2),gen(1))):gen(2),add(one,mult(const(8),gen(1))):gen(4),add(one,mult(const(-16),gen(1))):gen(8)}
   return roots[a]
  raise ValueError(ast.dump(n))
 return visit(ast.parse(s,mode='eval').body)
def ident(n):return [[one if i==j else zero for j in range(n)] for i in range(n)]
def amul(A,B):return [[sumalg(mult(x,y) for x,y in zip(row,col)) for col in zip(*B)] for row in A]
def sumalg(xs):
 out=zero
 for x in xs:out=add(out,x)
 return out
def ainv(A):
 n=len(A);a=[r.copy()+ident(n)[i] for i,r in enumerate(A)]
 for j in range(n):
  k=next(k for k in range(j,n) if a[k][j]!=zero);a[j],a[k]=a[k],a[j];iv=invert(a[j][j]);a[j]=[mult(x,iv) for x in a[j]]
  for k in range(n):
   if k!=j:
    c=a[k][j];a[k]=[sub(x,mult(c,y)) for x,y in zip(a[k],a[j])]
 return [r[n:] for r in a]
c=load('EXACT_F4*');orders=[[0,1,2,3],[2,3,0,1],[0,1,2,3],[1,0,3,2]];stages=[];nz=0
for key,targetkey in [('first_stage_weight_vectors','first_rook_factor_X'),('second_stage_weight_vectors','second_rook_factor_Y')]:
 branches=[]
 for w,perm in zip(c[key],orders):
  w=list(map(parse,w));nz+=sum(x==zero for x in w);A=ident(4)
  for i in range(4):A[i][perm[i]]=sub(A[i][perm[i]],w[i])
  G=ainv(A);assert amul(A,G)==ident(4) and amul(G,A)==ident(4);branches.append(G)
 stage=[[sumalg(G[i][j] for G in branches) for j in range(4)] for i in range(4)]
 assert stage==[[parse(x) for x in row] for row in c[targetkey]];stages.append(stage)
assert amul(stages[1],stages[0])==[[parse(x) for x in row] for row in c['fourier_unnormalized']]
assert nz==12
assert all(stages[s][r][c]==zero for s in range(2) for r in range(4) for c in range(4) if r//2!=c//2 and r%2!=c%2)
assert parse(c['first_stage_weight_vectors'][2][0])!=parse(c['first_stage_weight_vectors'][2][1])
OUT['M-FOURIER4-GREEN_phase16']={'eight_two_sided_inverse_checks':True,'stage_sums_and_full_negative_F4_identity':True,'zero_edge_occurrences':nz,'identity_branch_nonscalar':True,'all_divisions_checked_units_in_exact_quadratic_tower':True,'no_inherited_eval_or_sympify':True}
print('F4 eight-resolvent exact certificate passed',flush=True)

(D/'checks/F4_REPLAY.json').write_text(json.dumps(OUT,indent=2)+'\n')
