import json,hashlib,itertools,math
from fractions import Fraction as F
from pathlib import Path
OUT=Path(__file__).resolve().parent
BASE=OUT/'input'/'sources'
EXPECTED={'PROOF.md':'dbc5794d7680b91102e41d2bfcdcd5ad92e488fc75460ea540fad7fe159edde8','REVIEW.md':'79adf45b1526f71728240f40c8fd2b7d3a019cda161a0b308b01b630dc307df2','CHART.json':'5528afbbd5b4008a5e0f79043870e72a613e0fd421288d2ce1e5dbffee1c9e98'}
for n,h in EXPECTED.items(): assert hashlib.sha256((BASE/n).read_bytes()).hexdigest()==h
c=json.loads((BASE/'CHART.json').read_text())
assert c['N']==8 and c['product_order']=='M=S2*S1' and c['sum_coefficients']==[1,1,1] and c['free_phase_indices']==list(range(7,24))
assert [s['seed'] for s in c['stages']]==[42420,42520]
p=1000000009; roots=[569522298,430477711]
assert all(p%d for d in range(2,math.isqrt(p)+1))
assert all((r*r+1)%p==0 for r in roots) and sum(roots)==p
mul=lambda a,b:(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
records=[]; gains=[]
for si,s in enumerate(c['stages']):
 assert len(s['gaussian_pairs'])==17
 assert len(s['cycles'])==3 and all(sorted(cy)==list(range(8)) for cy in s['cycles'])
 gs=[(F(1),F(0))]*7
 for a,b in s['gaussian_pairs']:
  assert all((a+r*b)%p and (a-r*b)%p for r in roots)
  gs.append((F(a*a-b*b,a*a+b*b),F(2*a*b,a*a+b*b)))
 assert all(u*u+v*v==1 for u,v in gs)
 gains.append(gs)
 for bi in range(3):
  h=(F(1),F(0))
  for g in gs[8*bi:8*bi+8]:h=mul(h,g)
  assert h!=(1,0) and h!=(0,0) and h[0]*h[0]+h[1]*h[1]==1
  reductions=[]
  for r in roots:
   z=(h[0].numerator*pow(h[0].denominator,-1,p)+r*h[1].numerator*pow(h[1].denominator,-1,p))%p
   assert z and z!=1
   reductions.append(z)
  records.append({'stage':si,'branch':bi,'holonomy':[str(x) for x in h],'modular_holonomies':reductions})
labels=[(s,b,list(es)) for s in range(2) for b in [1,2] for es in itertools.combinations(range(8*b,8*b+8),4)]
assert len(labels)==len(set((s,b,tuple(e)) for s,b,e in labels))==280
support=[a for a in itertools.product(range(4),repeat=4) if max(a)-min(a)<=2]
assert len(support)==146 and (0,0,0,0) in support
header=['// Fresh independent data extraction from byte-pinned CHART.json.','#pragma once','const int cycles[2][3][8]='+json.dumps([s['cycles'] for s in c['stages']]).replace('[','{').replace(']','}')+';','const int pairs[2][17][2]='+json.dumps([s['gaussian_pairs'] for s in c['stages']]).replace('[','{').replace(']','}')+';']
support126=[v for v in support if sum(abs(v[j]-v[(j+1)%4]) for j in range(4))<=4]
hsupport=[v for v in itertools.product(range(3),repeat=4) if max(v)-min(v)<=1 and sum(abs(v[j]-v[(j+1)%4]) for j in range(4))<=2]
assert len(support126)==126 and len(hsupport)==27
(OUT/'independent_chart.h').write_text('\n'.join(header)+'\n')
res={'status':'PASS','sources':EXPECTED,'prime':p,'roots':roots,'exact_holonomies':records,'labels':labels,'monomials':support,'count':len(labels),'support_dimension':len(support),'refined_support':support126,'refined_dimension':len(support126),'H_support':hsupport,'H_dimension':len(hsupport)}
(OUT/'INDEPENDENT_STRUCTURE.json').write_text(json.dumps(res,indent=2)+'\n')
print('PASS: source bytes, all six exact norm-one nontrivial holonomies, 68 Gaussian denominator factors in both embeddings, 280 labels, initial dimension146, refined Q dimension126, H dimension27')
