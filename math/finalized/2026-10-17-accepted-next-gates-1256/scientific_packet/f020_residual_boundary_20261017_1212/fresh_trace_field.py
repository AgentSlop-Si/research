"""Fresh exact QQ(omega) test, using elementary reciprocal trace reduction."""
import argparse,json,time
from pathlib import Path
import sympy as s
from sympy.polys.rings import ring
P=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('d',type=int);ap.add_argument('bs',nargs='*',type=int);args=ap.parse_args()
d=args.d; bs=args.bs or list(range(d)); x=s.symbols('omega'); phi=s.Poly(s.cyclotomic_poly(d,x),x)
K=s.QQ.algebraic_field((phi.as_expr(),x)); R,z=ring('z',K); T,y=ring('y',K); w=K.unit
H=[R.one,1+z]
for n in range(1,max(bs)):H.append((1+z)*H[-1]-z*(1-w**n)*H[-2])
S=[T(2),y]
for n in range(1,d//2):S.append(y*S[-1]-S[-2])
def trace(h):
 n=h.degree();assert n%2==0;m=n//2
 assert all(h[(i,)]==h[(n-i,)] for i in range(n+1))
 return T(h[(m,)])+sum((h[(m+j,)]*S[j] for j in range(1,m+1)),T.zero)
F=1+z**d; Rt=trace(F.exquo(1+z)); records=[]
for b in bs:
 start=time.monotonic();h=H[b];U=h.exquo(1+z) if b%2 else h;Q=trace(U)
 ordinary_trace_gcd=Q.gcd(Q.diff(y)) if Q.degree()>0 else T.one
 node_trace_gcd=Q.gcd(Rt)
 rec={'d':d,'b':b,'trace_degree':int(Q.degree()),
 'trace_derivative_gcd_degree':int(ordinary_trace_gcd.degree()),
 'trace_derivative_gcd_is_one':ordinary_trace_gcd==T.one,
 'trace_node_gcd_degree':int(node_trace_gcd.degree()),
 'trace_node_gcd_is_one':node_trace_gcd==T.one,
 'trace_at_plus_2_nonzero':Q.evaluate(y,K(2))!=K.zero,
 'trace_at_minus_2_nonzero':Q.evaluate(y,K(-2))!=K.zero,
 'elapsed_seconds':time.monotonic()-start}
 rec['ordinary_H_squarefree']=all(rec[k] for k in ['trace_derivative_gcd_is_one','trace_at_plus_2_nonzero','trace_at_minus_2_nonzero'])
 rec['exact_node_gcd']='z+1' if b%2 else '1'
 rec['exact_node_gcd_certified']=rec['trace_node_gcd_is_one'] and rec['trace_at_minus_2_nonzero']
 records.append(rec);print(json.dumps(rec),flush=True)
 (P/f'trace_field_d{d}.json').write_text(json.dumps({'method':'exact QQ(omega) reciprocal trace gcd, with both ramification values checked','records':records},indent=2)+'\n')
