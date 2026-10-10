"""Independent mathematical operation ledger; never loads uploaded Python."""
import json,hashlib,zipfile,functools
from pathlib import Path
p=998244353
@functools.lru_cache(None)
def prune_cost(n,support):
 if n==1 or not support:return 0
 even=tuple(j//2 for j in support if j%2==0);odd=tuple(j//2 for j in support if j%2)
 local=0 if not odd else (n if not even else 3*(n//2))
 return local+prune_cost(n//2,even)+prune_cost(n//2,odd)
def recurrence_and_cost(samples):
 C=[1];past=[1];L=0;delay=1;last=1;cost=0
 for index in range(len(samples)):
  disc=samples[index]
  for j in range(1,L+1):disc=(disc+C[j]*samples[index-j])%p;cost+=2
  if disc==0:delay+=1;continue
  cost+=2;scale=disc*pow(last,-1,p)%p;old=C[:]
  C += [0]*max(0,len(past)+delay-len(C))
  for j in range(len(past)):C[j+delay]=(C[j+delay]-scale*past[j])%p;cost+=2
  if L*2<=index:past=old;L=index+1-L;last=disc;delay=1
  else:delay+=1
 return C[:L+1],cost
records=[]
source=json.loads(Path('source/RESULTS.json').read_text())
for rec in source['groups']['operation_profiles']:
 N=rec['N'];m=math_isqrt=__import__('math').isqrt(N);assert m*m==N;Q=m;b=rec['b'];root=pow(3,(p-1)//m,p);roots=[pow(root,j,p) for j in range(m)]
 cost=2*N+Q*b;bm_cost=0;root_cost=0;verify_cost=0;synthesis_cost=0;amplitude_cost=0
 for t in range(Q):
  H=[(t+j)%m for j in range(b)]
  samples=[sum((2*b if j==0 else 1)*roots[(-h*u)%m] for j,h in enumerate(H))%p for u in range(2*b)]
  C,bmc=recurrence_and_cost(samples);assert len(C)==b+1 and C[0]==1
  # Confirm every recovered grid root directly for this independent count model.
  for h in H:
   value=0
   for a in reversed(C):value=(value*roots[h]+a)%p
   assert value==0
  bm_cost+=bmc;root_cost+=prune_cost(m,tuple(j for j,v in enumerate(C) if v));verify_cost+=prune_cost(m,tuple(sorted(H)));amplitude_cost+=5*b*b+6*b
 for h in range(m):synthesis_cost+=prune_cost(Q,tuple(sorted((h-j)%m for j in range(b))))
 cost+=bm_cost+root_cost+verify_cost+amplitude_cost+synthesis_cost
 baseline=N+3*(N//2)*(N.bit_length()-1)
 assert cost==rec['new_arithmetic'] and baseline==rec['baseline_arithmetic']
 assert rec['K']==Q*b and rec['old_theorem_MK']==N*b and rec['old_theorem_K_squared']==(Q*b)**2
 assert rec['ratio']==cost/baseline
 records.append({'N':N,'b':b,'new_arithmetic':cost,'baseline_arithmetic':baseline,'BM':bm_cost,'root_grid':root_cost,'amplitudes':amplitude_cost,'full_verification':verify_cost,'bucket_synthesis':synthesis_cost,'root_table_and_output':2*N,'mode_phase':Q*b})
# Independently derive all deterministic test-loop cardinalities, without claiming execution.
small=2*sum(2*len({0,1,min(3,n),n//2,n}) for n in [1,2,4,8,16,32,64,128]);assert small==140
accepted=2*sum(sum(len({0,1,b}) for b in {1,max(1,m//4),m//2}) for m in [4,8,16,32,64,128]);assert accepted==90
rejected=2*sum(len({1,max(1,m//4),m//2}) for m in [4,8,16,32,64,128]);assert rejected==34
forged=2*sum(sum(len({0,1,b}) for b in {1,max(1,m//4),m//2} if 2*b<m) for m in [4,8,16,32,64,128]);assert forged==54
assert 2*sum([4,8,16,32,64])==248
expected={'pruned_cases':140,'mode_accept':90,'mode_reject':34,'forged':54,'end_to_end_random':2*11*3*2,'atomic_fiber_inputs':248,'green':2*7*3,'green_denominator_rejections':2*2,'aggregate_accept':2*5*3*2,'aggregate_reject':2*5*(2*2+1),'aggregate_fully_heavy':2*5*2}
Path('PROFILE_MODEL_RESULTS.json').write_text(json.dumps({'status':'PASS','operation_profiles':records,'test_loop_cardinalities':expected,'source_programs_executed':False,'word_proxy_exactly_reproduced':False,'original_random_test_execution_reproduced':False},indent=2,sort_keys=True)+'\n')
print('All six arithmetic profiles independently derived, including 7516160 versus 7340032.')
