"""Auditor-authored exact correction/parameter controls; no uploaded imports."""
import json,random
from fractions import Fraction as Q
from pathlib import Path
r=random.Random(14017)
# The spectral condition of a diagonal real matrix is exact from its diagonal.
def kap(xs):return max(map(abs,xs))/min(map(abs,xs))
assert kap([Q(2),Q(2)])==1 and kap([Q(2),Q(2),Q(1),Q(1)])==2
# Determinant-modulus-one local prefixes have singular extrema bracketing 1.
for v in [Q(1,16),Q(1,2),Q(1),Q(2),Q(9)]:assert kap([v,1/v])==kap([v,1/v,1,1])
# Exact locality-gate constants, no transcendental comparison.
assert 1024*72**604*4 < 73**604
assert 29**2*Q(541,512)<1024
# Half-cut integer threshold: two rank-two stages give rank sum <=4.
assert 2*4 >= 17//2 and 2*4 < 18//2
# One-hot projection product law for arbitrary functions given their values.
checks=0
for n in range(1,17):
 for _ in range(16):
  u=[Q(r.randrange(-9,10),r.randrange(1,10)) for _ in range(n+1)]
  v=[Q(r.randrange(-9,10),r.randrange(1,10)) for _ in range(n+1)]
  for i in range(1,n+1):
   ui=u[i]-u[0];vi=v[i]-v[0]
   assert u[i]*v[i]-u[0]*v[0]==u[0]*vi+v[0]*ui+ui*vi
  checks+=1
assert (2**53+1)-(2**53)==1
assert (float(2**53)+1.0)-float(2**53)==0.0
# Finite-win numerical claims use exact integer comparisons, no FFT claim activated.
assert 31**200 < 32**199
counts={}
for n,G in [(4,4),(8,12),(16,32)]:
 pairs=n*(n-1)//2
 counts[n]=[G,G*(G-1)*(pairs-1),G*(G-1)*(G-2)//2*(pairs-1)**2]
assert sum(counts[16])==210833760
out={'status':'PASS','no_uploaded_code_executed':True,'original_reset_counterexample':{'local_diagonal':[2,2],'local_kappa':1,'padded_diagonal':[2,2,1,1],'padded_kappa':2},'later_shear_repair':'Each prefix determinant modulus1 or separate norm/inverse products handles identity padding. These controls do not certify concrete #130 extraction or finite precision.','locality_exact_constant_checks':2,'halfcut_boundary':{'N17':'not excluded','N18':'excluded for two rank2 stages'},'onehot_product_cases':checks,'float_collection_counterexample':{'exact':1,'binary64':0},'exact_finite_win_moment':True,'neighborhood_count_formula':counts,'exhaustive_210million_schedule_search_replayed':False}
Path(__file__).with_name('BASELINE_CORRECTION_CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
