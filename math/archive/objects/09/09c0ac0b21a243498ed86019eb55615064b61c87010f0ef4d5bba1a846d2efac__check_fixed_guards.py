#!/usr/bin/env python3
"""Independent exact arithmetic for algebraic-seed pulled-back inner inverses."""
from pathlib import Path
from fractions import Fraction as F
from math import lcm
import sys,json,hashlib
from geometry import routes,projection
BASE=Path(__file__).parent
sys.path.insert(0,str(BASE/'seed_audit'))
from independent_verifier import cproduct,normnum,shapecheck,as_fraction,fraction_record

def verify():
 raw=(BASE/'seed_audit/sources/DYADIC_AFFINE_CHART.json').read_bytes();sha=hashlib.sha256(raw).hexdigest()
 assert sha=='904d7d24bf3aeee0a7c206eb8fd98ee11045fbc22cc97a105511b51907e1b188'
 chart=json.loads(raw);cert=json.loads((BASE/'seed_audit/INDEPENDENT_CERTIFICATE.json').read_text());assert cert['chart_sha256']==sha
 e=as_fraction(cert['bounds']['residual_upper_bound']);q=as_fraction(cert['bounds']['contraction_factor_bound']);rho=F(2,10**12)
 assert 0<q<1 and e/(1-q)<rho
 cr,ci=chart['center_real'],chart['center_imag'];vr,vi=chart['directions_real'],chart['directions_imag'];assert chart['dyadic_exponent']==60
 for v in (vr,vi):shapecheck(v,[3,16,8,256])
 for c in (cr,ci):shapecheck(c,[3,16,8])
 denoms=[d**64-1 for d in range(2,10)];L=lcm(*denoms);D=(1<<60)*L;gs=[]
 for j,p in enumerate(routes()):
  d=j+2;g=[[0]*64 for _ in range(64)];inv=[0]*64
  for col in range(64):
   row=col
   for power in range(64):g[row][col]=d**(64-power)*(L//denoms[j]);row=p[row]
  for i,v in enumerate(p):inv[v]=i
  assert all(d*g[i][k]-g[inv[i]][k]==d*L*int(i==k) for i in range(64) for k in range(64));gs.append(g)
 pcs=json.loads((BASE/'sources/FIXED_INNER_PRECONDITIONERS.json').read_text());saved=json.loads((BASE/'sources/FIXED_INNER_GUARDS.json').read_text());out=[]
 assert len(pcs)==2
 for ell in range(2):
  h=tuple([[sum(c[ell][projection(i)][j]*gs[j][i][k] for j in range(8)) for k in range(64)] for i in range(64)] for c in (cr,ci))
  assert all(h[part][i^32][k^32]==h[part][i][k] for part in range(2) for i in range(64) for k in range(64))
  largest=0
  for i in range(64):
   small=projection(i);total=0
   for k in range(64):
    coeff=[gs[j][i][k] for j in range(8)]
    for t in range(256):total+=abs(sum(coeff[j]*vr[ell][small][j][t] for j in range(8)))+abs(sum(coeff[j]*vi[ell][small][j][t] for j in range(8)))
   largest=max(largest,total)
  derivative=F(largest,D);proposed=pcs[ell];assert proposed['layer']==ell and proposed['denominator_exponent']==80
  R=proposed['real'],proposed['imag']
  for part in R:shapecheck(part,[64,64])
  RS=1<<80;prod=cproduct(R,h)
  for i in range(64):prod[0][i][i]-=RS*D
  defect=F(normnum(prod),RS*D);rn=F(normnum(R),RS);bound=defect+rn*derivative*rho;assert bound<1
  row={'center_inverse_defect':defect,'preconditioner_norm':rn,'seed_direction_bound':derivative,'root_radius':rho,'total_nonsingularity_bound':bound}
  assert saved['results'][ell]['layer']==ell
  for k,v in row.items():assert v==as_fraction(saved['results'][ell][k]),(ell,k)
  out.append({'layer':ell,**{k:fraction_record(v) for k,v in row.items()}});print('Exact fixed inner guard',ell,float(bound),'PASS',flush=True)
 result={'status':'ACCEPTED_BOTH_ALGEBRAIC_FIXED_INNER_GUARDS','chart_sha256':sha,'derived_root_bound':fraction_record(e/(1-q)),'source_fractions_match_exactly':True,'results':out,'scope':'Both literal N64 inner pullbacks invertible at the actual accepted N16 algebraic root'}
 (BASE/'FIXED_GUARD_RESULTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
if __name__=='__main__':verify()
