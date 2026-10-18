"""Fresh exact source checks and combinatorial template dimensions (standard library)."""
from pathlib import Path
from fractions import Fraction as F
import json,itertools,hashlib,math
ROOT=Path(__file__).resolve().parent
C=json.loads((ROOT/'sources/CHART.json').read_text())
def add(a,b):return(a[0]+b[0],a[1]+b[1])
def mul(a,b):return(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def conj(a):return a[0],-a[1]
def inverse(a):
 d=a[0]**2+a[1]**2
 assert d
 return a[0]/d,-a[1]/d
def cj(a,b):return mul((F(a),F(b)),inverse((F(a),F(-b))))
hs=[]
for s in C['stages']:
 gains=[(F(1),F(0))]*7+[cj(a,b)for a,b in s['gaussian_pairs']]
 assert len(gains)==24 and all(mul(z,conj(z))==(1,0)for z in gains)
 for b in range(3):
  h=(F(1),F(0))
  for z in gains[b*8:(b+1)*8]:h=mul(h,z)
  assert h!=(1,0) and mul(h,conj(h))==(1,0)
  hs.append(h)
prime=1000000009
assert all(prime%d for d in range(2,math.isqrt(prime)+1))
for im in [569522298,prime-569522298]:
 assert im*im%prime==prime-1
 for s in C['stages']:
  for a,b in s['gaussian_pairs']:assert (a+im*b)%prime and (a-im*b)%prime
 for h in hs:
  vals=[int(x.numerator)*pow(int(x.denominator),-1,prime)%prime for x in h]
  v=(vals[0]+im*vals[1])%prime
  assert v and v!=1
coords=list(itertools.product(range(2),range(7,24)))
alllabels=list(itertools.combinations(coords,3))
def accepted(L):
 return L[0][0]==L[2][0] and ((L[0][1]==7 and 8<=L[1][1]<=15 and 16<=L[2][1]<=23)or 8<=L[0][1]<L[1][1]<L[2][1]<=15)
def family(L):
 if L[0][0]==L[2][0]:return 'same_branch_300'if L[0][1]//8==L[2][1]//8 else'same_stage_210'
 i=0 if L[0][0]==L[1][0]else 1
 return'mixed_same_branch_pair'if L[i][1]//8==L[i+1][1]//8 else'mixed_different_branch_pair'
remaining=[L for L in alllabels if not accepted(L)]
assert len(alllabels)==5984 and len(remaining)==5744
counts={k:sum(family(L)==k for L in remaining)for k in sorted({family(L)for L in remaining})}
assert counts=={'same_branch_300':112,'same_stage_210':1008,'mixed_same_branch_pair':1904,'mixed_different_branch_pair':2720}
V=list(itertools.product(range(4),repeat=3))
V46=[e for e in V if max(e)-min(e)<=2]
V56=[e for e in V if abs(e[0]-e[1])<=2]
V52=[e for e in V if e[0]+e[1]>=2]
assert (len(V46),len(V56),len(V52))==(46,56,52)
# The curved intersection has five Laurent x-degree blocks. In each block,
# evaluation and t,z derivatives are independent since both degrees are >=1.
blocks={delta:(4-abs(delta))*4 for delta in range(-2,3)}
assert sum(blocks.values())==56 and sum(n-3 for n in blocks.values())==41
records=[json.loads(l)for l in (ROOT/'COVERAGE_PRIMARY.jsonl').read_text().splitlines()]
expect={tuple(s*24+e for s,e in L):family(L)for L in remaining}
assert len(records)==len(expect)
seen=set();stats={}
for r in records:
 L=tuple(r['label']);assert L in expect and L not in seen and r['family']==expect[L];seen.add(L)
 assert r['rank']==r['target']=={'same_branch_300':46,'same_stage_210':41,'mixed_same_branch_pair':56,'mixed_different_branch_pair':52}[r['family']]
 assert 0<r['determinant']<prime
 assert len(r['columns'])==len(set(r['columns']))==r['target']
 assert len(r['windows'])==len(set(r['windows']))==r['target']
 stats.setdefault(r['family'],[]).append(r['windows_tested'])
assert seen==set(expect)
# Data only, used by the independently structured fixed-minor verifier.
with (ROOT/'FIXED_MINORS.txt').open('w')as f:
 for r in records:f.write(' '.join(map(str,r['label']+[r['target'],r['determinant']]+r['windows']+r['columns']))+'\n')
report={'chart_sha256':hashlib.sha256((ROOT/'sources/CHART.json').read_bytes()).hexdigest(),'all_labels':len(alllabels),'accepted_not_rerun':240,'remaining_checked':len(records),'families':counts,'prime':prime,'embeddings':[569522298,prime-569522298],'exact_holonomies':[[str(t)for t in h]for h in hs],'template_dimensions':[46,56,52,41],'windows_tested_range':{k:[min(v),max(v)]for k,v in stats.items()}}
assert report['chart_sha256']=='5528afbbd5b4008a5e0f79043870e72a613e0fd421288d2ce1e5dbffee1c9e98'
(ROOT/'STRUCTURE_CHECKS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
