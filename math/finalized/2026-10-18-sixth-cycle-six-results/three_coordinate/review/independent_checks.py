"""Independent source/coverage/ring checks; author programs are never imported."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations,product
from collections import Counter
import json,hashlib,math
R=Path(__file__).resolve().parent; C=json.loads((R/'input/sources/CHART.json').read_text()); p=1000000009
assert C['N']==8 and C['product_order']=='M=S2*S1' and C['sum_coefficients']==[1,1,1]
assert C['free_phase_indices']==list(range(7,24))
assert [s['seed']for s in C['stages']]==[42420,42520]
for s in C['stages']:
 assert len(s['cycles'])==3 and len(s['gaussian_pairs'])==17
 assert all(sorted(c)==list(range(8))for c in s['cycles'])
 assert s['cycles'][0]==list(range(8))
# First seven directed edges are a connected, acyclic undirected tree.
seen={7}
for j in range(7):
 a=C['stages'][0]['cycles'][0][j-1];b=C['stages'][0]['cycles'][0][j]
 assert a in seen and b not in seen;seen.add(b)
assert seen==set(range(8))
def gm(z,w):return(z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0])
hol=[]
for s in C['stages']:
 g=[(F(1),F(0))]*7
 for a,b in s['gaussian_pairs']:
  z=(F(a*a-b*b,a*a+b*b),F(2*a*b,a*a+b*b));assert gm(z,(z[0],-z[1]))==(1,0);g.append(z)
 for branch in range(3):
  h=(F(1),F(0))
  for z in g[branch*8:branch*8+8]:h=gm(h,z)
  assert h not in [(0,0),(1,0)] and gm(h,(h[0],-h[1]))==(1,0);hol.append(h)
assert p>1 and all(p%d for d in range(2,math.isqrt(p)+1))
embeddings=[]
for ii in [569522298,430477711]:
 assert ii*ii%p==p-1
 denominators=[]
 for s in C['stages']:
  for a,b in s['gaussian_pairs']:
   for sig in [-1,1]:denominators.append((a+sig*ii*b)%p)
 assert all(denominators)
 hr=[sum(z.numerator*pow(z.denominator,-1,p)*q for z,q in zip(h,[1,ii]))%p for h in hol]
 assert all(h not in [0,1]for h in hr)
 embeddings.append({'i':ii,'all_68_localized_factors_nonzero':True,'holonomies':hr,'fixed_guards':[(1-h)%p for h in hr]})
coords=[24*s+e for s in range(2)for e in range(7,24)]
all_labels=set(combinations(coords,3));old=set()
for s in range(2):
 old.update((24*s+7,24*s+a,24*s+b)for a in range(8,16)for b in range(16,24))
 old.update(tuple(24*s+e for e in L)for L in combinations(range(8,16),3))
assert len(old)==240 and len(all_labels)==5984
expected=all_labels-old
families={}
for L in sorted(expected):
 occ=Counter((q//24,(q%24)//8)for q in L);stages=Counter(q//24 for q in L)
 if max(occ.values())==3:fam,dim='same_branch_300',46
 elif len(stages)==1:fam,dim='same_stage_210',41
 elif max(occ.values())==2:fam,dim='mixed_same_branch_pair',56
 else:fam,dim='mixed_different_branch_pair',52
 families[L]=(fam,dim)
counts=Counter(f for f,d in families.values())
assert counts==dict(same_branch_300=112,same_stage_210=1008,mixed_same_branch_pair=1904,mixed_different_branch_pair=2720)
for name in ['PRIMARY','CONJUGATE']:
 rs=[json.loads(l)for l in (R/f'input/COVERAGE_{name}.jsonl').read_text().splitlines()]
 assert len(rs)==5744 and len({tuple(r['label'])for r in rs})==5744
 assert {tuple(r['label'])for r in rs}==expected
 for r in rs:
  fam,dim=families[tuple(r['label'])];assert r['family']==fam and r['rank']==r['target']==dim
  assert len(r['windows'])==len(set(r['windows']))==len(r['columns'])==len(set(r['columns']))==dim
  assert all(0<=w<784 for w in r['windows']) and all(0<=c<64 for c in r['columns'])
  assert 0<r['determinant']<p and r['windows_tested']==max(r['windows'])+1
 with (R/f'REVIEW_MINORS_{name}.txt').open('w')as f:
  for r in rs:f.write(' '.join(map(str,r['label']+[r['target'],r['determinant']]+r['windows']+r['columns']))+'\n')
assert (R/'REVIEW_MINORS_PRIMARY.txt').read_bytes()==(R/'input/FIXED_MINORS.txt').read_bytes()
with (R/'REVIEW_CHART.txt').open('w')as f:
 for s in C['stages']:
  for cyc in s['cycles']:f.write(' '.join(map(str,cyc))+'\n')
  for pair in s['gaussian_pairs']:f.write(' '.join(map(str,pair))+'\n')
V=list(product(range(4),repeat=3));dims=[sum(max(v)-min(v)<=2 for v in V),sum(abs(v[0]-v[1])<=2 for v in V),sum(v[0]+v[1]>=2 for v in V),sum(4*(4-abs(d))-3 for d in range(-2,3))]
assert dims==[46,56,52,41]
report={'result':'PASS','source_chart_sha256':hashlib.sha256((R/'input/sources/CHART.json').read_bytes()).hexdigest(),'source_manifest_sha256':hashlib.sha256((R/'input/CORE_MANIFEST.json').read_bytes()).hexdigest(),'labels':5984,'inherited_not_rerun':240,'new_labels':5744,'families':dict(counts),'dimensions':dims,'exact_holonomies':[[str(z)for z in h]for h in hol],'prime_proved_by_trial_division':p,'admissible_embeddings':embeddings,'seed_scope':'Seed metadata checked; original pseudorandom-generation provenance is inherited unless separately supplied.'}
(R/'INDEPENDENT_STRUCTURE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
