"""Exact structural rank-cut certificates for temporal pair-call networks."""
from itertools import combinations
from pathlib import Path
import json,time
D=Path(__file__).resolve().parent

def schedule(n):
 return [(i,i^(1<<s)) for s in range(n.bit_length()-1) for i in range(n) if i&(1<<s)==0]
def materialize(n,w):
 ss=schedule(n);del ss[w['delete']]
 for p,a,b in w['replace']:ss[p]=(a,b)
 return ss

def support(n,seq,cut=None):
 a=[(1<<i) if i!=cut else 0 for i in range(n)]
 for g,(i,j) in enumerate(seq):
  z=a[i]|a[j]
  a[i]=0 if n+2*g==cut else z
  a[j]=0 if n+2*g+1==cut else z
 return a

def single_cut(n,seq):
 allbits=(1<<n)-1
 for node in range(n+2*len(seq)):
  remaining=support(n,seq,node)
  for i,j in combinations(range(n),2):
   lost=allbits&~(remaining[i]|remaining[j])
   if lost.bit_count()>n//2:
    return {'cut_nodes':[node],'outputs':[i,j],'inputs':[k for k in range(n) if lost>>k&1],
     'network_rank_upper_bound':1,'target_rank_lower_bound':2,'permutation_invariant':True}
 return None

def run():
 start=time.monotonic();ws=[json.loads(x) for x in (D/'results/topology_witnesses_16_2.jsonl').read_text().splitlines()]
 rejected=[];remaining=[]
 for w in ws:
  ss=materialize(16,w);c=single_cut(16,ss)
  (rejected if c else remaining).append({'topology':w,'certificate':c} if c else w)
 (D/'results/single_rank_cut_certificates.json').write_text(json.dumps(rejected,indent=2))
 (D/'results/after_single_rank_cuts.json').write_text(json.dumps(remaining,indent=2))
 result={'candidates':len(ws),'rejected_single_bottleneck':len(rejected),'remaining':len(remaining),'elapsed_seconds':time.monotonic()-start}
 (D/'results/rank_cut_summary.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)
if __name__=='__main__':run()
