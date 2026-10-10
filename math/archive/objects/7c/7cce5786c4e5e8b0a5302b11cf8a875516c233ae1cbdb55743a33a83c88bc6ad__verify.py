#!/usr/bin/env python3
"""Independent exact checker: does not import topology or rank-cut search code.
Rational coefficient vectors prove identities for independent arbitrary inputs.
Rank witnesses are checked using graph reachability, not search's bitmask pass.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path
import copy,json,time
D=Path(__file__).resolve().parent

def baseline(n):
 pairs=[]
 size=1
 while size<n:
  for first in range(0,n,2*size):
   for j in range(size):pairs.append((first+j,first+j+size))
  size*=2
 return pairs

def target(n):return [[1 if (i&j).bit_count()%2==0 else -1 for j in range(n)] for i in range(n)]

def replay_word(w):
 n=w['width'];v=[[F(i==j) for j in range(n)] for i in range(n)]
 stats=Counter()
 for g in w['word']:
  if g['op']=='h2':
   i,j=g['pair'];assert 0<=i<n and 0<=j<n and i!=j
   a,b=v[i],v[j];v[i]=[x+y for x,y in zip(a,b)];v[j]=[x-y for x,y in zip(a,b)]
   stats['kernel_calls']+=1;stats['scalar_additions']+=2;stats['operand_reads']+=4;stats['scalar_writes']+=2
  elif g['op']=='diagonal':
   assert len(g['values'])==n
   for i,s in enumerate(g['values']):
    q=F(s);assert q
    if q!=1:v[i]=[q*x for x in v[i]];stats['scalar_multiplications']+=1;stats['operand_reads']+=1;stats['scalar_writes']+=1
  elif g['op']=='permutation':
   p=g['sources'];assert sorted(p)==list(range(n));v=[v[i] for i in p]
   stats['materialized_permutation_reads']+=n;stats['materialized_permutation_writes']+=n
  else:raise AssertionError('unknown operation')
 return v,dict(stats)

def verify_word(w,expected):
 val,cost=replay_word(w);assert val==expected,'exact full-state operator mismatch';return cost

def from_witness(n,w):
 s=baseline(n);assert 0<=w['delete']<len(s);del s[w['delete']]
 seen=set()
 for pos,a,b in w['replace']:
  assert pos not in seen and 0<=pos<len(s) and 0<=a<b<n and (a,b)!=s[pos]
  seen.add(pos);s[pos]=(a,b)
 return s

def graph(n,s):
 # Two fresh value nodes per call are the next versions of the same two
 # physical registers, NOT extra simultaneously live data registers.
 edges=[[] for _ in range(n+2*len(s))];current=list(range(n))
 for t,(i,j) in enumerate(s):
  a,b=current[i],current[j];u,v=n+2*t,n+2*t+1
  for x in [a,b]:edges[x].extend([u,v])
  current[i],current[j]=u,v
 return edges,current

def reachable(edges,source,blocked):
 seen=set();stack=[source]
 while stack:
  v=stack.pop()
  if v in seen or v in blocked:continue
  seen.add(v);stack.extend(edges[v])
 return seen

def check_cut(n,w,c):
 s=from_witness(n,w);edges,ends=graph(n,s)
 assert len(c['cut_nodes'])==1 and 0<=c['cut_nodes'][0]<len(edges)
 assert len(set(c['outputs']))==2 and all(0<=o<n for o in c['outputs'])
 assert len(set(c['inputs']))==len(c['inputs'])>n//2 and all(0<=i<n for i in c['inputs'])
 blocked=set(c['cut_nodes'])
 for inp in c['inputs']:
  visits=reachable(edges,inp,blocked)
  assert all(ends[o] not in visits for o in c['outputs']),'cut leaves a path'
 assert c['network_rank_upper_bound']==1 and c['target_rank_lower_bound']==2 and c['permutation_invariant']
 # Certify the target assertion for EVERY possible row-pair, not merely the
 # two named physical output positions. Column permutations retain class sizes.
 h=target(n)
 for a,b in combinations(range(n),2):
  ratio=Counter(h[a][j]*h[b][j] for j in range(n))
  assert max(ratio.values())==n//2
 return True

def full_graph(n,w):
 edges,ends=graph(n,from_witness(n,w))
 return all(all(out in reachable(edges,inp,set()) for out in ends) for inp in range(n))

def mutation_must_fail(f):
 try:f()
 except (AssertionError,IndexError,ValueError):return True
 raise AssertionError('corrupted certificate accepted')

def run():
 start=time.monotonic();summary={'baseline':[],'neighborhoods':[]}
 for n in [4,8,16]:
  w=json.loads((D/f'results/baseline_{n}.json').read_text());cost=verify_word(w,target(n));summary['baseline'].append({'width':n,**cost})
  bad=copy.deepcopy(w);bad['word'][0]['pair'][1]=n;mutation_must_fail(lambda:verify_word(bad,target(n)))
  bad=copy.deepcopy(w);del bad['word'][0];mutation_must_fail(lambda:verify_word(bad,target(n)))
  calls=len(baseline(n));countsum=0
  for r in [0,1,2]:
   f=json.loads((D/f'results/topology_{n}_{r}.json').read_text());rev=json.loads((D/f'results/topology_{n}_{r}_reverse.json').read_text())
   count=calls*comb(calls-1,r)*(comb(n,2)-1)**r
   assert f['labeled_schedules']==rev['labeled_schedules']==count
   assert f['full_support_schedules']==rev['full_support_schedules']
   def loadlines(suffix):return [json.loads(x) for x in (D/f'results/topology_witnesses_{n}_{r}{suffix}.jsonl').read_text().splitlines()]
   witnesses=loadlines('');backwards=loadlines('_reverse')
   assert len(witnesses)==f['full_support_schedules']
   assert sorted(map(lambda w:json.dumps(w,sort_keys=True),witnesses))==sorted(map(lambda w:json.dumps(w,sort_keys=True),backwards))
   for z in witnesses:assert len(z['replace'])==r and full_graph(n,z)
   countsum+=count
  summary['neighborhoods'].append({'width':n,'labeled_schedules_up_to_two_rewirings':countsum})
 records=json.loads((D/'results/single_rank_cut_certificates.json').read_text())
 ws=[json.loads(x) for x in (D/'results/topology_witnesses_16_2.jsonl').read_text().splitlines()]
 assert Counter(json.dumps(w,sort_keys=True) for w in ws)==Counter(json.dumps(z['topology'],sort_keys=True) for z in records)
 for z in records:check_cut(16,z['topology'],z['certificate'])
 bad=copy.deepcopy(records[0]);bad['certificate']['cut_nodes']=[0]
 mutation_must_fail(lambda:check_cut(16,bad['topology'],bad['certificate']))
 bad=copy.deepcopy(records[0]);bad['certificate']['inputs']=list(range(16))
 mutation_must_fail(lambda:check_cut(16,bad['topology'],bad['certificate']))
 # Exact H2-to-C identity over Q(i), represented by rational pairs.
 def add(z,w):return(z[0]+w[0],z[1]+w[1])
 def mul(z,w):return(z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0])
 def mm(a,b):return [[add(mul(a[i][0],b[0][j]),mul(a[i][1],b[1][j])) for j in range(2)]for i in range(2)]
 zero=(F(0),F(0));one=(F(1),F(0));a=(F(1,2),F(1,2));b=(F(1,2),F(-1,2));ss=[[one,zero],[zero,(F(0),F(1))]]
 ans=mm(mm(ss,[[a,b],[b,a]]),ss)
 assert [[mul((F(1),F(-1)),x) for x in row]for row in ans]==[[(F(x),F(0))for x in row]for row in target(2)]
 # Exact source-derived three-H2 word for the unit upper shear.
 shear=json.loads((D/'results/unit_shear.json').read_text());summary['unit_shear']=verify_word(shear,[[1,1],[0,1]])
 assert 31**200 < 32**199
 summary.update({'exact_baselines_verified':3,'full_support_graphs_verified':len(ws),'single_wire_rank_cuts_verified':len(records),
  'cut_input_size_histogram':dict(sorted(Counter(len(z['certificate']['inputs']) for z in records).items())),
  'q_i_kernel_equivalence_verified':True,'safe_conditional_moment_verified':'31^200 < 32^199',
  'deliberate_corruption_tests_passed':8,'independent_basis_inputs':True,'elapsed_seconds':time.monotonic()-start})
 (D/'results/verification_summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
if __name__=='__main__':run()
