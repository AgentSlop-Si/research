#!/usr/bin/env python3
"""Standalone fresh replay checker. Does not import the reducer or inherited code.
Coefficient multiplication uses ordinary convolution followed by descending
Phi_11 reduction (different from the reducer's cyclic-convolution route).
"""
import ast, collections, functools, hashlib, json, math, pathlib, time
from fractions import Fraction
ROOT=pathlib.Path(__file__).resolve().parents[2];OUT=pathlib.Path(__file__).resolve().parent
ZERO=((0,)*10,1);ONE=((1,)+(0,)*9,1)
def normal(a,d=1):
 a=list(a)
 while len(a)>10:
  k=len(a)-1;c=a.pop()
  for j in range(k-10,k):a[j]-=c
 a += [0]*(10-len(a))
 if d<0:a=[-v for v in a];d=-d
 g=math.gcd(d,*a);return tuple(v//g for v in a),d//g
def plus(a,b):return normal([x*b[1]+y*a[1] for x,y in zip(a[0],b[0])],a[1]*b[1])
def minus(a):return tuple(-v for v in a[0]),a[1]
@functools.lru_cache(maxsize=100000)
def times(a,b):
 if a==ZERO or b==ZERO:return ZERO
 if a==ONE:return b
 if b==ONE:return a
 out=[0]*19
 for i in range(10):
  for j in range(10):out[i+j]+=a[0][i]*b[0][j]
 return normal(out,a[1]*b[1])
@functools.lru_cache(maxsize=10000)
def invert(a):
 assert a!=ZERO
 import sympy as s
 z=s.Symbol('z');expr=sum(s.Rational(v,a[1])*z**i for i,v in enumerate(a[0]))
 q=s.Poly(s.invert(expr,sum(z**i for i in range(11)),z),z)
 fs=[Fraction(q.nth(i)) for i in range(10)];d=math.lcm(*(v.denominator for v in fs))
 r=normal([int(v*d) for v in fs],d);assert times(a,r)==ONE;return r

def cpow(a,n):
 r=ONE
 for _ in range(n):r=times(r,a)
 return r
@functools.lru_cache(maxsize=70000)
def coefficient(expr):
 def visit(n):
  if isinstance(n,ast.Constant) and type(n.value) is int:return normal([n.value])
  if isinstance(n,ast.Name) and n.id=='zeta':return normal([0,1])
  if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub):return minus(visit(n.operand))
  if isinstance(n,ast.BinOp):
   if isinstance(n.op,ast.Pow):
    assert isinstance(n.right,ast.Constant) and 0<=n.right.value<=100
    return cpow(visit(n.left),n.right.value)
   a,b=visit(n.left),visit(n.right)
   if isinstance(n.op,ast.Add):return plus(a,b)
   if isinstance(n.op,ast.Sub):return plus(a,minus(b))
   if isinstance(n.op,ast.Mult):return times(a,b)
   if isinstance(n.op,ast.Div):
    assert all(v==0 for v in b[0][1:]) and b[0][0]
    return normal([v*b[1] for v in a[0]],a[1]*b[0][0])
  raise ValueError(ast.dump(n))
 return visit(ast.parse(expr,mode='eval').body)

def unpack(ts):
 p={}
 for m,a,d in ts:
  assert len(m)==LEN and min(m)>=0 and len(a)==10 and d>0
  c=normal(a,d);assert c==(tuple(a),d) and c!=ZERO and tuple(m) not in p
  p[tuple(m)]=c
 return p

def pack(p):return [[list(m),list(c[0]),c[1]] for m,c in sorted(p.items())]
def hpoly(p):return hashlib.sha256(json.dumps(pack(p),separators=(',',':')).encode()).hexdigest()
def pplus(p,q):
 r=p.copy()
 for m,c in q.items():
  v=plus(r.get(m,ZERO),c)
  if v==ZERO:r.pop(m,None)
  else:r[m]=v
 return r

def pproduct(p,q):
 out={}
 for m,c in p.items():
  for n,d in q.items():
   k=tuple(a+b for a,b in zip(m,n));v=plus(out.get(k,ZERO),times(c,d))
   if v==ZERO:out.pop(k,None)
   else:out[k]=v
 return out

def ppower(p,n):
 r={ZM:ONE}
 for _ in range(n):r=pproduct(r,p)
 return r

def substitute_horner(p,j,num,den):
 by={}
 for m,c in p.items():
  a=list(m);e=a[j];a[j]=0;by.setdefault(e,{})[tuple(a)]=c
 d=max(by,default=0)
 r=by.get(d,{})
 # Homogeneous Horner: after k descents, numerator degree k / denominator^k.
 denpow={ZM:ONE}
 for i in range(d-1,-1,-1):
  denpow=pproduct(denpow,den)
  r=pplus(pproduct(r,num),pproduct(by.get(i,{}),denpow))
 return r,d

def exact_quotient(p,g):
 lm=max(g);lc=invert(g[lm]);r=p.copy();q={}
 if len(g)==1:
  if any(any(a<b for a,b in zip(m,lm)) for m in p):return None
  return {tuple(a-b for a,b in zip(m,lm)):times(c,lc) for m,c in p.items()}
 import heapq
 heap=[tuple(-v for v in m) for m in r];heapq.heapify(heap)
 while r:
  while True:
   m=tuple(-v for v in heapq.heappop(heap))
   if m in r:break
  if any(a<b for a,b in zip(m,lm)):return None
  shift=tuple(a-b for a,b in zip(m,lm));c=times(r[m],lc);q[shift]=plus(q.get(shift,ZERO),c)
  for n,d in g.items():
   k=tuple(a+b for a,b in zip(n,shift));v=plus(r.get(k,ZERO),minus(times(c,d)))
   if v==ZERO:r.pop(k,None)
   else:
    if k not in r:heapq.heappush(heap,tuple(-x for x in k))
    r[k]=v
 return q

def statistics(es):
 ps=list(es.values());return dict(variables=[v for j,v in enumerate(VS) if any(any(m[j] for m in p) for p in ps)],equations=len(ps),terms=sum(map(len,ps)),max_terms=max(map(len,ps),default=0),nonzero_constant=any(set(p)=={ZM} for p in ps))

def main():
 global VS,LEN,ZM
 started=time.monotonic();path=OUT/'CERTIFICATE.json';D=json.loads(path.read_text());VS=D['variables'];LEN=len(VS);ZM=(0,)*LEN
 for f,h in [(D['input_equations_file'],D['input_equations_sha256']),(D['input_guards_file'],D['input_guards_sha256']),('research_cycle_1758/symbolic_independent_review/RECEIPT.json',D['input_receipt_sha256'])]:assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h
 P={}
 for h,ts in D['polynomials'].items():
  p=unpack(ts);assert hpoly(p)==h;P[h]=p
 source=json.loads((ROOT/D['input_equations_file']).read_text())
 es={}
 for i,eq in enumerate(source['remaining_equations']):
  p={}
  for t in eq['terms']:
   assert all(x==0 for j,x in enumerate(t['exponent']) if j not in VS)
   m=tuple(t['exponent'][v] for v in VS);c=coefficient(t['coefficient']);assert c!=ZERO and m not in p;p[m]=c
  eid=str(i);assert p==P[D['initial']['equations'][eid]];es[eid]=p
 gd=json.loads((ROOT/D['input_guards_file']).read_text());gs={}
 for v in gd['nonzero_surviving_coordinates']:
  m=[0]*LEN;m[VS.index(v)]=1;gs['x'+str(v)]={tuple(m):ONE}
 for g in gd['nonzero_guard_polynomials']:
  p={}
  for t in g['terms']:
   ex=dict(t['exponent']);m=tuple(ex.get(v,0) for v in VS);p[m]=normal(t['coefficient_numerators'],t['coefficient_denominator'])
  gs['g'+str(g['eliminated_mandatory_edge'])]=p
 assert {k:hpoly(v) for k,v in gs.items()}==D['initial']['guards']
 assert statistics(es)==D['initial']['statistics'];print('INPUTS VERIFIED',statistics(es),flush=True)
 counts=collections.Counter();eliminated=[]
 for step,e in enumerate(D['events']):
  if e['kind']=='cancel':
   k=e['equation'];assert es[k]==P[e['dividend']] and gs[e['guard']]==P[e['divisor']]
   assert pproduct(P[e['divisor']],P[e['quotient']])==es[k]
   es[k]=P[e['quotient']];counts['cancellations']+=1
  elif e['kind']=='linear_elimination':
   j=VS.index(e['variable']);eid=e['source_equation'];num=P[e['numerator']];den=P[e['denominator']]
   assert all(m[j]==0 for m in num) and all(m[j]==0 for m in den)
   vm=[0]*LEN;vm[j]=1
   assert pplus(pproduct(den,{tuple(vm):ONE}),{m:minus(c) for m,c in num.items()})==es[eid]==P[e['source']]
   nz=e['denominator_nonzero'];p={ZM:normal(*nz['constant'])}
   for gid in nz['guard_factors']:p=pproduct(p,gs[gid])
   assert p==den and p
   assert {x['equation'] for x in e['equation_transforms']}==set(es)
   new={}
   for row in e['equation_transforms']:
    k=row['equation'];assert es[k]==P[row['old']]
    q,d=substitute_horner(es[k],j,num,den);assert d==row['denominator_power'] and q==P[row['new']]
    if q:new[k]=q
   assert eid not in new
   assert {x['guard'] for x in e['guard_transforms']}==set(gs)
   ng={}
   for row in e['guard_transforms']:
    k=row['guard'];assert gs[k]==P[row['old']]
    q,d=substitute_horner(gs[k],j,num,den);assert q and d==row['denominator_power'] and q==P[row['new']];ng[k]=q
   es,gs=new,ng;eliminated.append(e['variable']);counts['linear_eliminations']+=1
  else:raise ValueError(e['kind'])
  print('EVENT',step,e['kind'],'VERIFIED',flush=True)
 assert {k:hpoly(v) for k,v in es.items()}==D['final']['equations']
 assert {k:hpoly(v) for k,v in gs.items()}==D['final']['guards']
 assert statistics(es)==D['final']['statistics'] and eliminated==D['final']['eliminated_variables']
 result=dict(status='PASS: author-side standalone exact replay; independent review pending',certificate_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),checker_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),checks=dict(counts),final_statistics=statistics(es),guards_preserved=len(gs),runtime_seconds=time.monotonic()-started)
 (OUT/'CHECK_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':main()
