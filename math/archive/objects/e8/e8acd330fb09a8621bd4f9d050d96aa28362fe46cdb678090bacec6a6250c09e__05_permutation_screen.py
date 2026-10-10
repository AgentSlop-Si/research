"""Exact small-n and deterministic Monte Carlo screening of permutation rank bounds."""
from pathlib import Path
import itertools,random,json,collections
ROOT=Path(__file__).parent

def required_ranksum(P):
 n=len(P)
 return max(max(min(t,n-1-max(P[-t:])), min(t,min(P[:t]))) for t in range(1,n))

def run():
 exact={}
 for n in (6,7,8):
  count=collections.Counter(required_ranksum(P) for P in itertools.permutations(range(n)))
  exact[str(n)]={'counts_by_min_required_rank_sum':dict(sorted(count.items())),
     'pass_rank_sum_two':sum(v for k,v in count.items() if k<=2),
     'total':sum(count.values())}
 assert exact['8']['pass_rank_sum_two']==28584
 rng=random.Random(20261009);samples={}
 for n in (16,32,64):
  count=collections.Counter()
  for rep in range(10000):
   P=list(range(n));rng.shuffle(P);count[required_ranksum(P)]+=1
  samples[str(n)]={'count':10000,'seed':20261009,
     'passes_ranksum_two':sum(v for k,v in count.items() if k<=2),
     'distribution':dict(sorted(count.items()))}
 out={'exact_permutation_counts':exact,'random_permutation_screen':samples,
      'disclaimer':'Ranksum screening is a necessary test, not a count of possible factorizations; random large-N counts are sampled, not exhaustive.'}
 (ROOT/'PERMUTATION_SCREEN.json').write_text(json.dumps(out,indent=2)+'\n')
 print('Exact N8 pass',exact['8']['pass_rank_sum_two'],'of',exact['8']['total'],flush=True)
 print('Random pass rates',{n:v['passes_ranksum_two'] for n,v in samples.items()},flush=True)
 return out
if __name__=='__main__':run()
