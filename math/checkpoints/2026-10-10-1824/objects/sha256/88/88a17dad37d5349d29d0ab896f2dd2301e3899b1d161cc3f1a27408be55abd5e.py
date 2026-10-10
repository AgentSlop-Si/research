#!/usr/bin/env python3
"""Checker for compact triangular reduction and original guard irreducibility.
Uses the separately authored checker arithmetic, never generator code.
"""
import json,hashlib,importlib.util,time
from pathlib import Path
OUT=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('standalone_checker',OUT/'check_guarded.py');c=importlib.util.module_from_spec(sp);sp.loader.exec_module(c)
start=time.monotonic();mainpath=OUT/'CERTIFICATE.json';D=json.loads(mainpath.read_text());c.VS=D['variables'];c.LEN=len(c.VS);c.ZM=(0,)*c.LEN
P={h:c.unpack(ts) for h,ts in D['polynomials'].items()}
def read_polys(doc):
 for h,ts in doc['polynomials'].items():
  p=c.unpack(ts);assert c.hpoly(p)==h
  if h in P:assert P[h]==p
  P[h]=p

def dependencies(p):return {v for j,v in enumerate(c.VS) if any(m[j] for m in p)}

def check_compact(path,parentstage,earlier_eliminated):
 B=json.loads(path.read_text());read_polys(B)
 if 'parent_certificate_sha256' in B:assert B['parent_certificate_sha256']==hashlib.sha256(mainpath.read_bytes()).hexdigest()
 stage=D[parentstage];gs={k:P[h] for k,h in stage['guards'].items()};es={k:P[h] for k,h in stage['equations'].items()}
 assert B['guards']==stage['guards'];free=set(B['free_variables']);available=set(free);eliminated=[]
 for e in B['definitions']:
  v=e['variable'];eid=e['source_equation'];source=P[e['source']];num=P[e['numerator']];den=P[e['denominator']]
  assert v not in available and source==es[eid]
  assert dependencies(num)|dependencies(den)<=available
  assert set(e['dependencies'])==dependencies(num)|dependencies(den)
  vm=[0]*c.LEN;vm[c.VS.index(v)]=1
  assert c.pplus(c.pproduct(den,{tuple(vm):c.ONE}),{m:c.minus(a) for m,a in num.items()})==source
  proof=e['denominator_nonzero'];constant=c.normal(*proof['constant']);assert constant!=c.ZERO
  product={c.ZM:constant}
  for gid in proof['guard_factors']:
   assert dependencies(gs[gid])<=available
   product=c.pproduct(product,gs[gid])
  assert product==den and den
  eliminated.append(v);available.add(v);es.pop(eid)
 assert B['reconstruction_order']==eliminated
 assert B['equations']=={k:c.hpoly(p) for k,p in es.items()}
 assert set(free)|set(eliminated)==set(stage['statistics']['variables'])
 assert not set(free)&set(eliminated)
 assert len(es)==B['equations_count'] and len(gs)==B['guards_count']
 assert all(dependencies(p)<=available for p in es.values())
 print('COMPACT VERIFIED',path.name,'free_variables',len(free),'equations',len(es),'eliminated',eliminated,flush=True)
 return dict(free_variables=sorted(free),equations=len(es),guards=len(gs),compact_eliminations=eliminated,prior_expanded_eliminations=earlier_eliminated)

# Every original guard is primitive of degree one in a selected coordinate.
G=json.loads((OUT/'GUARD_IRREDUCIBILITY.json').read_text());read_polys(G)
for row in G['proofs']:
 g=P[row['polynomial']];a=P[row['leading_coefficient']];b=P[row['constant_coefficient']];v=row['linear_variable'];j=c.VS.index(v);vm=[0]*c.LEN;vm[j]=1
 assert v not in dependencies(a)|dependencies(b)
 assert c.pplus(c.pproduct(a,{tuple(vm):c.ONE}),b)==g
 assert c.hpoly(g)==D['initial']['guards'][row['guard']]
 if 'nonzero_constant_remainder' in row:
  q=P[row['quotient']];r=P[row['nonzero_constant_remainder']];assert set(r)=={c.ZM}
  assert c.pplus(c.pproduct(a,q),r)==b
 elif 'leading_factors' in row:
  product={c.ZM:c.normal(*row['leading_constant'])};seen=set()
  for f in row['leading_factors']:
   fac=P[f['factor']];w=f['variable'];wj=c.VS.index(w);root=P[f['root']];rem=P[f['nonzero_remainder']]
   assert not root or set(root)=={c.ZM}
   z=[0]*c.LEN;z[wj]=1;assert fac==c.pplus({tuple(z):c.ONE},{m:c.minus(x) for m,x in root.items()})
   assert f['factor'] not in seen;seen.add(f['factor']);product=c.pproduct(product,fac)
   r,d=c.substitute_horner(b,wj,root,{c.ZM:c.ONE});assert r==rem and rem
  assert product==a
 else:assert set(a)=={c.ZM}
 print('IRREDUCIBLE GUARD VERIFIED',row['guard'],flush=True)
assert len(G['proofs'])==6

# Exact exhaustive initial direct divisibility scan for all certified irreducible factors.
initial_es={k:P[h] for k,h in D['initial']['equations'].items()};initial_gs={k:P[h] for k,h in D['initial']['guards'].items()};tests=0
for eid,p in initial_es.items():
 for gid,g in initial_gs.items():
  assert c.exact_quotient(p,g) is None,(eid,gid)
  tests+=1
print('INITIAL NONDIVISIBILITY VERIFIED',tests,'exact tests',flush=True)
# The preserved 13-variable branch uses the original checkpoint.
old=check_compact(OUT/'compact_13/COMPACT_BRANCH.json','initial',[])
new=check_compact(OUT/'COMPACT_BRANCH.json','final',D['final']['eliminated_variables'])
C=json.loads((OUT/'SIMPLIFIED_CORE.json').read_text());read_polys(C)
T=P[C['T']];U=P[C['U']];A=c.normal(*C['A']);z=c.normal([0,1]);zm1=c.plus(z,c.minus(c.ONE));cc=c.normal(*C['nonzero_field_constant_c'])
assert A==c.times(c.plus(c.cpow(z,9),c.minus(c.cpow(z,4))),c.invert(zm1))
assert U==c.pplus(c.pproduct({c.ZM:A},T),{c.ZM:c.minus(c.ONE)})
assert cc==c.plus(c.cpow(z,7),c.minus(c.cpow(z,6))) and cc!=c.ZERO
q39=C['source_variable39'];assert q39==json.loads((OUT/'COMPACT_BRANCH.json').read_text())['definitions'][0]
assert P[q39['denominator']]==c.pproduct({c.ZM:zm1},T)
assert P[q39['numerator']]==c.pproduct({c.ZM:zm1},U)
assert P[D['final']['guards']['x91']]=={e:c.minus(v) for e,v in T.items()}
vm=[0]*c.LEN;vm[c.VS.index(39)]=1
assert P[C['source_variable91']['numerator']]=={e:c.minus(v) for e,v in c.pproduct({tuple(vm):c.ONE},T).items()}
assert P[C['source_variable91']['denominator']]=={c.ZM:cc}
print('SIMPLIFIED TWO-COORDINATE CORE VERIFIED',flush=True)
result=dict(status='PASS: author-side exact auxiliary verification; independent review pending',compact_final=new,preserved_compact_checkpoint=old,original_guards_proved_irreducible=6,initial_exact_nondivisibility_tests=tests,files={f:hashlib.sha256((OUT/f).read_bytes()).hexdigest() for f in ['CERTIFICATE.json','COMPACT_BRANCH.json','GUARD_IRREDUCIBILITY.json','SIMPLIFIED_CORE.json','check_auxiliary.py','check_guarded.py']},runtime_seconds=time.monotonic()-start)
(OUT/'AUXILIARY_CHECK_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2),flush=True)
