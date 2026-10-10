#!/usr/bin/env python3
"""Fresh bounded exact guarded continuation; all inherited files are data only."""
import ast, collections, functools, hashlib, json, math, pathlib, time
from fractions import Fraction
ROOT=pathlib.Path(__file__).resolve().parents[2]
OUT=pathlib.Path(__file__).resolve().parent
VS=(0,11,22,25,34,39,41,44,49,52,55,65,83,88,91,92)
N=len(VS); ZM=(0,)*N
ZERO=((0,)*10,1); ONE=((1,)+(0,)*9,1)
CAP_TERMS=50000; CAP_TOTAL=300000; CAP_MULTIPLICATIONS=2000000

def norm(a,d=1):
 if not any(a):return ZERO
 if d<0:a=tuple(-v for v in a);d=-d
 g=math.gcd(d,*a)
 return tuple(v//g for v in a),d//g

def add(a,b):
 if a==ZERO:return b
 if b==ZERO:return a
 g=math.gcd(a[1],b[1]);da=b[1]//g;db=a[1]//g
 return norm(tuple(x*da+y*db for x,y in zip(a[0],b[0])),a[1]*da)
def neg(a):return tuple(-x for x in a[0]),a[1]
def sub(a,b):return add(a,neg(b))
@functools.lru_cache(maxsize=100000)
def mul(a,b):
 if a==ZERO or b==ZERO:return ZERO
 if a==ONE:return b
 if b==ONE:return a
 c=[0]*11
 for i,x in enumerate(a[0]):
  if x:
   for j,y in enumerate(b[0]):
    if y:c[(i+j)%11]+=x*y
 return norm(tuple(c[i]-c[10] for i in range(10)),a[1]*b[1])
@functools.lru_cache(maxsize=10000)
def inv(a):
 assert a!=ZERO
 # Fresh field inverse: solve multiplication-by-a against the unit vector.
 rows=[]
 cols=[mul(a,(tuple(int(i==j) for i in range(10)),1)) for j in range(10)]
 for i in range(10):rows.append([Fraction(c[0][i],c[1]) for c in cols]+[Fraction(i==0)])
 for j in range(10):
  k=next(k for k in range(j,10) if rows[k][j]);rows[j],rows[k]=rows[k],rows[j]
  q=rows[j][j];rows[j]=[v/q for v in rows[j]]
  for k in range(10):
   if k!=j and rows[k][j]:
    q=rows[k][j];rows[k]=[x-q*y for x,y in zip(rows[k],rows[j])]
 r=[row[-1] for row in rows];d=math.lcm(*(x.denominator for x in r))
 ans=norm(tuple(int(x*d) for x in r),d);assert mul(a,ans)==ONE
 return ans

def power(a,n):
 if n<0:return power(inv(a),-n)
 r=ONE
 while n:
  if n&1:r=mul(r,a)
  n//=2
  if n:a=mul(a,a)
 return r

@functools.lru_cache(maxsize=70000)
def parse(s):
 def walk(t):
  if isinstance(t,ast.Constant) and isinstance(t.value,int):return norm((t.value,)+(0,)*9)
  if isinstance(t,ast.Name) and t.id=='zeta':return ((0,1)+(0,)*8,1)
  if isinstance(t,ast.UnaryOp) and isinstance(t.op,ast.USub):return neg(walk(t.operand))
  if isinstance(t,ast.UnaryOp) and isinstance(t.op,ast.UAdd):return walk(t.operand)
  if isinstance(t,ast.BinOp):
   a=walk(t.left)
   if isinstance(t.op,ast.Pow):
    assert isinstance(t.right,ast.Constant) and isinstance(t.right.value,int)
    return power(a,t.right.value)
   b=walk(t.right)
   if isinstance(t.op,ast.Add):return add(a,b)
   if isinstance(t.op,ast.Sub):return sub(a,b)
   if isinstance(t.op,ast.Mult):return mul(a,b)
   if isinstance(t.op,ast.Div):return mul(a,inv(b))
  raise ValueError(ast.dump(t))
 return walk(ast.parse(s,mode='eval').body)

def padd(a,b):
 c=dict(a)
 for m,v in b.items():
  w=add(c.get(m,ZERO),v)
  if w==ZERO:c.pop(m,None)
  else:c[m]=w
 return c

def pscale(a,c):return {m:mul(v,c) for m,v in a.items()} if c!=ZERO else {}
def pneg(a):return {m:neg(v) for m,v in a.items()}
def pmul(a,b,cap=True):
 if not a or not b:return {}
 if cap and len(a)*len(b)>CAP_MULTIPLICATIONS:raise SizeLimit(f'product work {len(a)}*{len(b)}>{CAP_MULTIPLICATIONS}')
 c={}
 for m,v in a.items():
  for n,w in b.items():
   e=tuple(x+y for x,y in zip(m,n));q=add(c.get(e,ZERO),mul(v,w))
   if q==ZERO:c.pop(e,None)
   else:c[e]=q
  if cap and len(c)>CAP_TERMS:raise SizeLimit(f'intermediate terms {len(c)}>{CAP_TERMS}')
 return c

def ppow(a,n):
 r={ZM:ONE}
 while n:
  if n&1:r=pmul(r,a)
  n//=2
  if n:a=pmul(a,a)
 return r

class SizeLimit(Exception):pass

def exact_div(a,b):
 """Single-divisor lex division; first irreducible leading term disproves divisibility."""
 assert b
 if not a:return {}
 lm=max(b);iv=inv(b[lm]);r=dict(a);q={};steps=0
 while r:
  m=max(r)
  if any(x<y for x,y in zip(m,lm)):return None
  e=tuple(x-y for x,y in zip(m,lm));c=mul(r[m],iv)
  q[e]=add(q.get(e,ZERO),c)
  for n,v in b.items():
   k=tuple(x+y for x,y in zip(e,n));w=sub(r.get(k,ZERO),mul(c,v))
   if w==ZERO:r.pop(k,None)
   else:r[k]=w
  steps+=1
  if steps>CAP_TERMS or len(r)>CAP_TERMS:raise SizeLimit('division work/terms cap')
 return q

def pack(p):return [[list(m),list(c[0]),c[1]] for m,c in sorted(p.items())]
def unpack(p):return {tuple(m):(tuple(a),d) for m,a,d in p}
def digest(p):return hashlib.sha256(json.dumps(pack(p),separators=(',',':')).encode()).hexdigest()
POLYS={}
def keep(p):
 h=digest(p);POLYS.setdefault(h,pack(p));return h

def from_old(ts):
 p={}
 for t in ts:
  e=t['exponent'];assert all(v==0 for i,v in enumerate(e) if i not in VS)
  m=tuple(e[v] for v in VS);assert min(m)>=0
  c=parse(t['coefficient']);assert c!=ZERO and m not in p;p[m]=c
 return p

def from_guard(ts):
 p={}
 for t in ts:
  es=dict(t['exponent']);assert set(es)<=set(VS)
  m=tuple(es.get(v,0) for v in VS)
  p[m]=norm(tuple(t['coefficient_numerators']),t['coefficient_denominator'])
 return p

def stat(eqs):
 ps=[p for p in eqs.values() if p]
 return dict(variables=[v for j,v in enumerate(VS) if any(any(m[j] for m in p) for p in ps)],equations=len(ps),terms=sum(map(len,ps)),max_terms=max(map(len,ps),default=0),nonzero_constant=any(set(p)=={ZM} for p in ps))

EVENTS=[];ATTEMPTS=[]
def cancel(eqs,guards):
 changed=False
 divisors=list(guards.items())
 for eid,p in list(eqs.items()):
  for gid,g in divisors:
   if len(g)==1 and ZM in g:continue
   while p:
    try:q=exact_div(p,g)
    except SizeLimit as e:
     ATTEMPTS.append(dict(action='cancel',equation=eid,guard=gid,status='size_limit',reason=str(e)));break
    if q is None:break
    EVENTS.append(dict(kind='cancel',equation=eid,guard=gid,dividend=keep(p),divisor=keep(g),quotient=keep(q)))
    print('CANCEL',eid,gid,len(p),'->',len(q),flush=True)
    p=q;changed=True
    if set(p)=={ZM}:break
  eqs[eid]=p
 return changed

def certified_factorization(p,guards):
 if not p:return None
 q=p;factors=[]
 for gid,g in guards.items():
  if len(g)==1 and ZM in g:continue
  while q and set(q)!={ZM}:
   try:r=exact_div(q,g)
   except SizeLimit:return None
   if r is None:break
   factors.append(gid);q=r
 if set(q)=={ZM}:return dict(guard_factors=factors,constant=q[ZM])
 return None

def coeffs(p,j):
 by={}
 for m,c in p.items():
  d=m[j];n=list(m);n[j]=0;by.setdefault(d,{})[tuple(n)]=c
 return by

def substituted(p,j,num,den):
 by=coeffs(p,j);d=max(by,default=0)
 if not d:return dict(p),0
 r={}
 for i,q in by.items():r=padd(r,pmul(q,pmul(ppow(num,i),ppow(den,d-i))))
 if len(r)>CAP_TERMS:raise SizeLimit(f'output terms {len(r)}>{CAP_TERMS}')
 return r,d

def save_json(name,obj):
 (OUT/name).write_text(json.dumps(obj,separators=(',',':'))+'\n')

def main():
 start=time.monotonic()
 rp=ROOT/'research_cycle_1758/symbolic_independent_review/RECEIPT.json'
 assert hashlib.sha256(rp.read_bytes()).hexdigest()=='7aa78ab0122f0dacf4231937c608ee1022c793cbeefb2c29ec82356c58d76c2e'
 receipt=json.loads(rp.read_text())
 src='research_cycle_1734/pole_escape/full_fourier_linear_reduction.json'
 gp='research_cycle_1758/symbolic_independent_review/FINAL_COORDINATE_GUARDS.json'
 for f,h in [(src,receipt['source_hashes'][src]),(gp,receipt['review_artifact_hashes']['FINAL_COORDINATE_GUARDS.json'])]:
  assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h
 data=json.loads((ROOT/src).read_text());gd=json.loads((ROOT/gp).read_text())
 eqs={str(i):from_old(e['terms']) for i,e in enumerate(data['remaining_equations'])}
 labels={str(i):e['label'] for i,e in enumerate(data['remaining_equations'])}
 guards={}
 for v in gd['nonzero_surviving_coordinates']:
  m=list(ZM);m[VS.index(v)]=1;guards['x'+str(v)]={tuple(m):ONE}
 for g in gd['nonzero_guard_polynomials']:guards['g'+str(g['eliminated_mandatory_edge'])]=from_guard(g['terms'])
 initial=dict(equations={k:keep(p) for k,p in eqs.items()},guards={k:keep(p) for k,p in guards.items()},labels=labels,statistics=stat(eqs))
 print('LOADED',stat(eqs),flush=True)
 save_json('INITIAL.json',initial)
 eliminated=[];rounds=0
 while True:
  rounds+=1;cancel(eqs,guards)
  if stat(eqs)['nonzero_constant']:stop='nonzero constant contradiction';break
  candidates=[]
  for eid,p in eqs.items():
   for j,v in enumerate(VS):
    if v in eliminated:continue
    by=coeffs(p,j)
    if max(by,default=0)!=1:continue
    a=by[1];cert=certified_factorization(a,guards)
    if cert is not None:
     b=by.get(0,{});candidates.append((len(b)*len(a),len(p),v,eid,j,a,pneg(b),cert))
  candidates.sort(key=lambda x:x[:4])
  print('ROUND',rounds,'STATS',stat(eqs),'SAFE_PIVOTS',[(c[2],c[3],len(c[5]),len(c[6])) for c in candidates],flush=True)
  if not candidates:stop='no guard-divisible factor and no certified safe linear pivot';break
  committed=False
  for _,__,v,eid,j,den,num,cert in candidates:
   try:
    next_eq={};changes=[]
    for oid,p in eqs.items():
     q,d=substituted(p,j,num,den)
     if q:next_eq[oid]=q
     changes.append(dict(equation=oid,old=keep(p),new=keep(q),denominator_power=d))
     if sum(map(len,next_eq.values()))>CAP_TOTAL:raise SizeLimit('total equation terms cap')
    next_guards={};gchanges=[]
    for gid,g in guards.items():
     q,d=substituted(g,j,num,den)
     assert q,'guard vanishes identically on this pivot; contradiction must be checked explicitly'
     next_guards[gid]=q;gchanges.append(dict(guard=gid,old=keep(g),new=keep(q),denominator_power=d))
    ev=dict(kind='linear_elimination',variable=v,source_equation=eid,source=keep(eqs[eid]),numerator=keep(num),denominator=keep(den),denominator_nonzero=dict(guard_factors=cert['guard_factors'],constant=[list(cert['constant'][0]),cert['constant'][1]]),equation_transforms=changes,guard_transforms=gchanges)
    EVENTS.append(ev);eqs=next_eq;guards=next_guards;eliminated.append(v);committed=True
    print('PIVOT',v,eid,'=>',stat(eqs),flush=True);break
   except SizeLimit as e:
    ATTEMPTS.append(dict(action='pivot',variable=v,equation=eid,status='size_limit',reason=str(e)))
    print('LIMIT',v,eid,str(e),flush=True)
  if not committed:stop='all certified safe linear pivots exceed explicit polynomial-size/work limits';break
 final=dict(equations={k:keep(p) for k,p in eqs.items()},guards={k:keep(p) for k,p in guards.items()},statistics=stat(eqs),eliminated_variables=eliminated,stop_reason=stop)
 cert=dict(format='sparse cyclotomic polynomial DAG v1',variables=VS,coefficient_basis='1,zeta,...,zeta^9; Phi11(zeta)=0',input_receipt_sha256=hashlib.sha256(rp.read_bytes()).hexdigest(),input_equations_file=src,input_equations_sha256=receipt['source_hashes'][src],input_guards_file=gp,input_guards_sha256=receipt['review_artifact_hashes']['FINAL_COORDINATE_GUARDS.json'],polynomials=POLYS,initial=initial,events=EVENTS,final=final,attempts=ATTEMPTS,limits=dict(max_polynomial_terms=CAP_TERMS,max_system_terms=CAP_TOTAL,max_product_pairs=CAP_MULTIPLICATIONS),status='AUTHOR-PENDING: not independently reviewed',runtime_seconds=time.monotonic()-start)
 save_json('CERTIFICATE.json',cert);save_json('FINAL.json',final)
 summary={k:v for k,v in cert.items() if k not in ['polynomials','initial','events','final']};summary.update(initial_statistics=initial['statistics'],final=final,events=len(EVENTS),cancellations=sum(e['kind']=='cancel' for e in EVENTS),linear_eliminations=sum(e['kind']=='linear_elimination' for e in EVENTS),polynomials=len(POLYS))
 save_json('SUMMARY.json',summary)
 print('DONE',json.dumps(summary),flush=True)
if __name__=='__main__':main()
