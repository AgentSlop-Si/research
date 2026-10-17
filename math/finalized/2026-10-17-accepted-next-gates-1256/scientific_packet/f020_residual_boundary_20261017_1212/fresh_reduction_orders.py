"""Fresh exploration of the q=1 order in discriminants reduced modulo p."""
import json,time
from pathlib import Path
import sympy as s
from sympy.polys.rings import ring
P=Path(__file__).resolve().parent
records=[]
for p,bs in [(3,range(3,9)),(5,range(5,11)),(7,[7,8])]:
 T,q=ring('q',s.GF(p));R,z=ring('z',T.to_domain());H=[R.one,1+z]
 for n in range(1,max(bs)):H.append((1+z)*H[-1]-z*(1-q**n)*H[-2])
 for b in bs:
  t=time.monotonic();D=H[b].resultant(H[b].diff(z));Ds=D.shift(s.GF(p).one)
  v=min(k[0] for k in Ds) if Ds else None
  rec={'prime':p,'b':b,'disc_order_mod_p_at_1':v,'V_order_mod_p_at_1':None if v is None else v-b*(b-1)//2,'elapsed_seconds':time.monotonic()-t,'resultant_shifted_sparse':{str(k[0]):int(c) for k,c in sorted(Ds.items())}}
  records.append(rec);print(json.dumps(rec),flush=True)
  (P/'reduction_orders.json').write_text(json.dumps(records,indent=2)+'\n')
