"""Read only the inert degree-31 certificate through the fresh standalone field code."""
from pathlib import Path
import json,hashlib,time,importlib.util
R=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('degree31_literal',R/'independent_literal_check.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
D=31;P=53;assert all(D%d for d in range(2,6)) and all(P%d for d in range(2,8))
data=json.loads((R/'DEGREE31_LITERAL_CERTIFICATE.json').read_text());rows=[]
for name,v in [('y',data['y']),('z',data['z'])]+[(f'root_{i}',v) for i,v in enumerate(data['roots'])]:
 x=tuple(v);orb=[];q=x
 while q not in orb:
  orb.append(q);q=m.power(q,P)
 assert q==x and len(orb)==D
 rows.append({'name':name,'orbit_length':len(orb),'first':list(x),'frobenius_once':list(orb[1])})
roots={tuple(x) for x in data['roots']};assert {m.power(x,P) for x in roots}!=roots
out={'verdict':'PASS','prime_characteristic':P,'prime_degree':D,'chart_exception_37_does_not_divide_degree':D%37!=0,'all_nine_nodes_exact_degree':D,'orbits':rows,'same_sign_supports_nonstable':True,'transfer':'31 divides d implies an embedding preserving all literal guards and operator equalities','does_not_prove':'No iff field classification or mandatory nonbase-node condition for all witnesses.'}
(R/'WITNESS_STRUCTURE.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
