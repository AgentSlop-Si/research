"""Fresh exact characteristic-zero RS residual checks; no inherited code imports."""
import argparse, json, time
from pathlib import Path
import sympy as s
from sympy.polys.rings import ring
P=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('d',type=int);parser.add_argument('bs',nargs='*',type=int); args=parser.parse_args()
d=args.d; bs=args.bs or list(range(d)); x=s.symbols('omega'); phi=s.Poly(s.cyclotomic_poly(d,x),x)
K=s.QQ.algebraic_field((phi.as_expr(),x)); R,z=ring('z',K); w=K.unit
H=[R.one,1+z]
for n in range(1,max(bs)):
 H.append((1+z)*H[-1]-z*(1-w**n)*H[-2])
F=1+z**d; records=[]
for b in bs:
 start=time.monotonic(); h=H[b]
 # Definitions used by the inherited local theorem.
 ordinary_gcd=h.gcd(h.diff(z)) if b else R.one
 F_gcd=h.gcd(F)
 U=h.exquo(1+z) if b%2 else h
 residual_gcd=U.gcd(U.diff(z)) if U.degree()>0 else R.one
 deflated_F_gcd=U.gcd(F)
 rec={'d':d,'b':b,'coefficient_field':f'QQ[omega]/Phi_{d}',
 'ordinary_gcd_degree':int(ordinary_gcd.degree()),
 'ordinary_gcd_is_one': ordinary_gcd==R.one,
 'cyclotomic_node_gcd_is_expected':F_gcd==((1+z) if b%2 else R.one),
 'cyclotomic_node_gcd_degree':int(F_gcd.degree()),
 'local_residual_degree':int(U.degree()),
 'local_residual_derivative_gcd_is_one':residual_gcd==R.one,
 'local_residual_F_gcd_is_one':deflated_F_gcd==R.one,
 'elapsed_seconds':time.monotonic()-start}
 records.append(rec); print(json.dumps(rec),flush=True)
 (P/f'exact_field_d{d}.json').write_text(json.dumps({'method':'direct polynomial gcd over exact cyclotomic number field via SymPy ANP','phi_ascending':[int(phi.nth(i)) for i in range(phi.degree()+1)],'records':records},indent=2)+'\n')
