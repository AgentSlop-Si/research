"""Deterministic reproducible exploratory counts and exact counter-witnesses."""
import json,random,hashlib
from annihilator_gate import (Stage,bit_reversal,nth_root,two_stage_witness,
                              three_stage_gate,three_stage_projected_ranks)

res={"date":"2026-10-10","computational_certificate_only":True,"theorems_proven_separately":True,"finite_field_tests":[],"permutation_gates":[],"sampling":[]}
for n in (24,32,64,128):
 for p in (12289,65537):
  if (p-1)%n:continue
  w=nth_root(n,p)
  rng=random.Random(991*n+p)
  order=list(range(n));rng.shuffle(order)
  s1=Stage.random(n,p,219*n+7,0.28)
  s2=Stage.random(n,p,587*n+11,0.22)
  cert=two_stage_witness(n,s1,s2,order,w,p)
  res['finite_field_tests'].append({k:cert[k] for k in ('n','p','omega','j','input','projected_fft','projected_product','determinant','bad_determinant_windows','intersecting_windows','guaranteed_witnesses')})

for n in (16,32,64,128):
 ids=list(range(n));br=bit_reversal(n)
 rng=random.Random(n+17);p1=rng.sample(ids,n);p2=rng.sample(ids,n)
 for name,pp1,pp2 in [('identity/identity',ids,ids),('bitrev/bitrev',br,br),('bitrev/identity',br,ids),('random/random',p1,p2)]:
  for W in (6,8,10,12,16):
   if W>=n:continue
   gate=three_stage_gate(n,pp1,pp2,W)
   res['permutation_gates'].append({'n':n,'W':W,'layout':name,
      'violating_pairs':gate['violating_window_pairs'],'minimum_defect':gate['defect'],
      'minimum_pair':[gate['I_start'],gate['J_start']],
      'required_defect':W-5})

for n in (16,32,64):
 br=bit_reversal(n)
 minimum_margin=9999
 violating_widths=[]
 for W in range(6,n):
  gate=three_stage_gate(n,br,br,W)
  minimum_margin=min(minimum_margin,gate['defect']-(W-5))
  if gate['excludes_factorization']:violating_widths.append(W)
 res.setdefault('bitrev_all_widths',[]).append({'n':n,'checked_widths':n-6,
    'minimum_margin':minimum_margin,'violating_widths':violating_widths})

for n in (32,64,128):
 ids=list(range(n));samples=40 if n<128 else 20
 for W in (6,8):
  violations=0;totalpairs=0
  for seed in range(samples):
   rng=random.Random(1661*n+81*seed)
   p1=rng.sample(ids,n);p2=rng.sample(ids,n)
   gate=three_stage_gate(n,p1,p2,W)
   violations+=int(gate['excludes_factorization'])
   totalpairs+=gate['violating_window_pairs']
  res['sampling'].append({'n':n,'W':W,'samples':samples,
     'random_layouts_excluded':violations,'violating_window_pairs_total':totalpairs})

p=12289;n=64;w=nth_root(n,p)
ids=list(range(n));br=bit_reversal(n)
for layout,p1,p2 in [('identity/identity',ids,ids),('bitrev/identity',br,ids),('random/random',random.Random(17).sample(ids,n),random.Random(23).sample(ids,n))]:
 cert=three_stage_gate(n,p1,p2,6)
 stages=[Stage.random(n,p,100+7*i,0.1) for i in range(3)]
 ranks=three_stage_projected_ranks(n,stages,(p1,p2),cert,w,p)
 res.setdefault('explicit_three_stage_certs',[]).append({'layout':layout,'window':{k:cert[k] for k in ('I_start','J_start','W','R','C','defect','cut','orientation')},'rank':ranks})

with open('EXPERIMENT_RESULTS.json','w') as f:json.dump(res,f,indent=2)
print('witnesses',len(res['finite_field_tests']))
print('permutation gate entries',len(res['permutation_gates']))
print('three-stage examples')
for entry in res['explicit_three_stage_certs']:print(entry['layout'],entry['rank'])
print('random sampling')
for entry in res['sampling']:print(entry)
