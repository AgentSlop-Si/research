#!/usr/bin/env python3
import json,importlib.util
from pathlib import Path
OUT=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('our_fresh_kernel',OUT/'reduce_guarded.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
D=json.loads((OUT/'CERTIFICATE.json').read_text());P={h:m.unpack(ts) for h,ts in D['polynomials'].items()};B=json.loads((OUT/'COMPACT_BRANCH.json').read_text());P.update({h:m.unpack(ts) for h,ts in B['polynomials'].items()});m.POLYS={}
def term(c,es):
 e=[0]*len(m.VS)
 for v,k in es.items():e[m.VS.index(v)]=k
 return {tuple(e):c}
z=m.parse('zeta');T=m.padd(term(z,{}),term(m.neg(m.power(z,9)),{41:1}));T=m.padd(T,term(m.ONE,{11:1,34:1,41:1}));T=m.padd(T,term(m.ONE,{11:1,41:1,49:1}))
A=m.mul(m.sub(m.power(z,9),m.power(z,4)),m.inv(m.sub(z,m.ONE)));U=m.padd(m.pscale(T,A),{m.ZM:m.neg(m.ONE)})
q39=B['definitions'][0];assert q39['variable']==39
assert P[q39['denominator']]==m.pscale(T,m.sub(z,m.ONE))
assert P[q39['numerator']]==m.pscale(U,m.sub(z,m.ONE))
assert P[D['final']['guards']['x91']]==m.pneg(T)
e91=next(e for e in D['events'] if e['kind']=='linear_elimination');c=m.sub(m.power(z,7),m.power(z,6));assert P[e91['denominator']]=={m.ZM:c}
assert P[e91['numerator']]==m.pneg(m.pmul(term(m.ONE,{39:1}),T))
C=dict(status='AUTHOR-PENDING',T=m.keep(T),A=[list(A[0]),A[1]],U=m.keep(U),nonzero_field_constant_c=[list(c[0]),c[1]],polynomials=m.POLYS,identities=['T = zeta - zeta^9*x41 + x11*x41*(x34+x49)', 'A = (zeta^9-zeta^4)/(zeta-1)', 'U = A*T-1', 'x39 = U/T', 'x91 = -U/(zeta^7-zeta^6)'],guards='T != 0 is exactly the negative of normalized guard x91; x39 != 0 is equivalent to U != 0 on this domain. All fourteen retained guards must still hold.',source_variable39=q39,source_variable91=dict(numerator=e91['numerator'],denominator=e91['denominator']),scope='Exact simplification of two already-certified pivots; not a solution and not an impossibility certificate.')
(OUT/'SIMPLIFIED_CORE.json').write_text(json.dumps(C,separators=(',',':'))+'\n')
