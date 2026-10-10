#!/usr/bin/env python3
"""Non-expanded triangular branch and small irreducibility certificates."""
import json,importlib.util,hashlib
from pathlib import Path
OUT=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('our_fresh_kernel',OUT/'reduce_guarded.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
D=json.loads((OUT/'scan_15000/CERTIFICATE.json').read_text());P={h:m.unpack(ts) for h,ts in D['polynomials'].items()}
es={k:P[h] for k,h in D['initial']['equations'].items()};gs={k:P[h] for k,h in D['initial']['guards'].items()}
m.POLYS.clear()
def keep(p):return m.keep(p)
def dependencies(p):return [v for j,v in enumerate(m.VS) if any(e[j] for e in p)]
steps=[]
for v,eid in [(91,'55'),(44,'0'),(55,'2')]:
 by=m.coeffs(es[eid],m.VS.index(v));assert set(by)<=set([0,1]);den=by[1];num=m.pneg(by.get(0,{}));proof=m.certified_factorization(den,gs);assert proof
 steps.append(dict(variable=v,source_equation=eid,source_label=D['initial']['labels'][eid],source=keep(es[eid]),numerator=keep(num),denominator=keep(den),dependencies=sorted(set(dependencies(num)+dependencies(den))),denominator_nonzero=dict(guard_factors=proof['guard_factors'],constant=[list(proof['constant'][0]),proof['constant'][1]])))
 print('COMPACT',v,'D_FACTORS',proof['guard_factors'],'NUM_TERMS',len(num),'DEN_TERMS',len(den))
initial_g={k:keep(g) for k,g in gs.items()}
comp=dict(status='AUTHOR-PENDING: formal rational-circuit reduction, independent review pending',format='triangular rational polynomial evaluation circuit v1',coefficient_basis=D['coefficient_basis'],variables=m.VS,free_variables=[v for v in m.VS if v not in [91,44,55]],reconstruction_order=[91,44,55],definitions=steps,guards=initial_g,equations={k:h for k,h in D['initial']['equations'].items() if k not in ['55','0','2']},equation_polynomial_source='CERTIFICATE.json: initial equations / polynomials',polynomials=m.POLYS,semantics='Evaluate each definition numerator and denominator using free coordinates and earlier definitions, then set x_variable=numerator/denominator. Evaluate every listed equation and guard at those assignments. Equations must equal zero and all guards must be nonzero. Each denominator is a nonzero constant times the explicitly listed original guards; its guard dependencies are available earlier in the reconstruction order.',equations_count=56,guards_count=14,nonzero_constant_contradiction_claimed=False,factorization_claimed=False,stop_reason='The expanded branch hit 50,000-term and 2,000,000 product-pair bounds. This compact branch commits the remaining two already-certified acyclic pivots only; it does not claim an exhaustive new circuit-level pivot search.')
(OUT/'COMPACT_BRANCH.json').write_text(json.dumps(comp,separators=(',',':'))+'\n')
# Irreducibility certificates for the six original reconstruction guards.
m.POLYS={};proofs=[]
for gid,g in gs.items():
 if not gid.startswith('g'):continue
 v=39 if gid=='g98' else 91 if gid in ['g96','g95'] else 25 if gid in ['g89','g46'] else 11
 by=m.coeffs(g,m.VS.index(v));a=by[1];b=by.get(0,{})
 row=dict(guard=gid,polynomial=keep(g),linear_variable=v,leading_coefficient=keep(a),constant_coefficient=keep(b))
 if set(a)=={m.ZM}:
  row.update(proof='linear in selected variable with nonzero field-unit leading coefficient')
 elif gid in ['g89','g46']:
  ab=m.coeffs(a,m.VS.index(83));assert set(ab[0])==set(ab[1])=={m.ZM}
  root=m.neg(m.mul(ab[0][m.ZM],m.inv(ab[1][m.ZM])));rem,_=m.substituted(b,m.VS.index(83),{m.ZM:root},{m.ZM:m.ONE});assert set(rem)=={m.ZM}
  quotient=m.exact_div(m.padd(b,m.pneg(rem)),a);assert quotient is not None
  row.update(proof='primitive linear polynomial: b=a*q+c with nonzero field constant c, so gcd(a,b)=1',quotient=keep(quotient),nonzero_constant_remainder=keep(rem))
 else:
  # a = zeta*x34*x41*(x83-zeta^7); all three irreducible factors miss b.
  factors=[]
  for w in [34,41]:
   ex=list(m.ZM);ex[m.VS.index(w)]=1;f={tuple(ex):m.ONE};rem={e:c for e,c in b.items() if not e[m.VS.index(w)]};assert rem
   factors.append(dict(factor=keep(f),variable=w,root=keep({}),nonzero_remainder=keep(rem)))
  z=m.parse('zeta');root=m.power(z,7);ex=list(m.ZM);ex[m.VS.index(83)]=1;f={tuple(ex):m.ONE,m.ZM:m.neg(root)};rem,_=m.substituted(b,m.VS.index(83),{m.ZM:root},{m.ZM:m.ONE});assert rem
  factors.append(dict(factor=keep(f),variable=83,root=keep({m.ZM:root}),nonzero_remainder=keep(rem)))
  p={m.ZM:z}
  for f in factors:p=m.pmul(p,m.unpack(m.POLYS[f['factor']]))
  assert p==a
  row.update(proof='primitive linear polynomial: leading coefficient factors explicitly; b has a nonzero remainder modulo each distinct irreducible linear factor',leading_constant=[list(z[0]),z[1]],leading_factors=factors)
 proofs.append(row)
(OUT/'GUARD_IRREDUCIBILITY.json').write_text(json.dumps(dict(status='AUTHOR-PENDING',polynomials=m.POLYS,proofs=proofs,conclusion='Each of the six original reconstruction guards is irreducible over Q(zeta11) in the final sixteen-coordinate polynomial ring. Thus an exact initial division scan against these six guards and eight mandatory coordinates exhausts direct cancellation by factors certified only from these guards.'),separators=(',',':'))+'\n')
