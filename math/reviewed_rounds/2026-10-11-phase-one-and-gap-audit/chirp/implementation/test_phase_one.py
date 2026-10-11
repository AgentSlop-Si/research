"""Fresh same-author exact controls; no uploaded research script is imported."""
from collections import Counter
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch
import copy, hashlib, itertools, json, math, random, subprocess, sys, time
import chirp_phase_one as c
import accepted_dispatch_v1 as accepted
import reference_v1 as d
from check_certificate_v1 import check
BASE=Path(__file__).resolve().parent
MAX=d.Limits(512,128,64,20_000_000)
S=Counter(); ROUTES=Counter(); DETAILS={}; CACHE={}; START=time.monotonic()
def root(n,p):
 return next(w for w in range(1,p) if pow(w,n,p)==1 and all(pow(w,k,p)!=1 for k in range(1,n)))
def make(n,p,r,x,w=None): return dict(N=n,p=p,r=r,omega=root(n,p) if w is None else w,x=list(x))
def wave(n,p,w,a,modes):return [sum(g*pow(w,(a*j*j+b*j)%n,p) for b,g in modes)%p for j in range(n)]
def direct(P):
 n,p,w,x=(P[k] for k in ('N','p','omega','x'))
 return [sum(v*pow(w,j*k,p) for j,v in enumerate(x))%p for k in range(n)]
def oracle(P):
 n,p,w,x=(P[k] for k in ('N','p','omega','x'));key=n,p,w
 if key not in CACHE:CACHE[key]=[[[pow(w,(-a*j*j-b*j)%n,p) for j in range(n)] for b in range(n)] for a in range(n//math.gcd(2,n))]
 return [sum(sum(v*q for v,q in zip(x,row))%p!=0 for row in phase) for phase in CACHE[key]]
def ledger(R):
 L=R['ledger'];assert L['work_units']==sum(L['counts'].values())
 if L['limit'] is not None:assert L['work_units']<=L['limit']
 if 'stages' in L:assert sum(L['stages'].values())==L['work_units']
 if 'fallback' in L:
  A,B=L['frontend'],L['fallback'];assert L['work_units']==A['work_units']+B['work_units'];assert B['limit']==L['limit']-A['work_units'];assert Counter(L['counts'])==Counter(A['counts'])+Counter(B['counts']);assert sum(A['stages'].values())==A['work_units']
def decision(P,kind,O=None,certificate=True):
 before=copy.deepcopy(P);R=c.recognize(P,MAX);D=d.recognize(P,MAX);A=accepted.recognize(P,MAX)
 if O is None:O=oracle(P)
 expected='MEMBER' if min(O)<=P['r'] else 'NONMEMBER'
 assert R['status']==D['status']==A['status']==expected,(P,R,D,O)
 assert R['dft']==D['dft']==A['dft'];assert P==before
 if expected=='MEMBER':
  assert R['dft']==direct(P)
  modes=R['representation']['modes'];a=R['representation']['a']
  assert wave(P['N'],P['p'],P['omega'],a,[(m['b'],m['gamma']) for m in modes])==P['x']
 if certificate:assert check(P,R,20_000_000)['status']=='VERIFIED_'+expected;S['certificate_checks']+=1
 if not P['N']&(P['N']-1):
  assert (R['route']=='sparse_frontend')==(O[0]<=P['r'])
  assert (R['route']=='sparse_phase_one')==(O[0]>P['r'] and P['N']>=4 and O[1]<=P['r'])
 if R['route']=='sparse_phase_one':assert R['representation']['a']==1 and R['phase_one']['raw_synthesis_checked']==P['N']
 if R['route'] in ('sparse_frontend','dense_reference_direct'):assert R['ledger']==A['ledger']
 if R['route']=='dense_reference_fallback':assert R['ledger']['fallback']['counts']==D['ledger']['counts']
 ledger(R);S[kind]+=1;S['differential_decisions']+=1;ROUTES[R['route']]+=1
 return R

def fft_cost(indices,n):
 """Independent occupancy-level prediction; does not invoke candidate recursion."""
 C=Counter()
 if not indices:C['field_entry_writes']=n;return C
 for depth in range(n.bit_length()-1):
  size=n>>depth;mod=1<<depth
  groups={q:[i for i in indices if i%mod==q] for q in {i%mod for i in indices}}
  C['pruned_active_nodes']+=len(groups);C['sparse_support_routes']+=len(indices)
  C['field_entry_writes']+=len(indices)+2*size*len(groups)
  C['pruned_combine_positions']+=(size//2)*len(groups)
  for values in groups.values():
   odd=any((i>>depth)&1 for i in values);even=any(not ((i>>depth)&1) for i in values)
   if odd:C['root_table_reads']+=size//2;C['field_multiplications']+=size//2;C['field_additions']+=(size//2)*(2 if even else 1)
 C['pruned_active_nodes']+=len(indices);C['field_entry_writes']+=len(indices)
 return C

def gauss_cost(modes,n):
 m=n//2;s=len(modes)
 C=Counter(phase_index_evaluations=2*n+s,root_table_reads=2*n+s,field_additions=n,field_multiplications=s+3*m,field_entry_writes=m+s,mode_parity_tests=s,dft_output_writes=2*n)
 for delta in range(2):C.update(fft_cost([((q['b']+delta)//2)%m for q in modes if q['b']%2==delta],m))
 return C

# Exhaustive complete decisions. First domains are complete finite fields.
for n,p,rs in [(2,3,[1]),(4,5,[1,2,3])]:
 for w in [v for v in range(1,p) if pow(v,n,p)==1 and all(pow(v,k,p)!=1 for k in range(1,n))]:
  for x in itertools.product(range(p),repeat=n):
   P=make(n,p,1,x,w);O=oracle(P)
   for r in rs:P['r']=r;decision(P,'exhaustive_full_field',O,False)
# Ternary alphabet in F17^8, explicitly not all field vectors.
for x in itertools.product(range(3),repeat=8):
 P=make(8,17,1,x,2);O=oracle(P)
 for r in [1,2]:P['r']=r;decision(P,'exhaustive_ternary_N8',O,False)
print('exhaustive passed',dict(S),flush=True)
rng=random.Random(0xC11F01)
for n,p,reps in [(3,7,12),(5,11,12),(6,13,12),(8,17,50),(12,37,12),(16,97,60),(32,193,25)]:
 ws=[w for w in range(1,p) if pow(w,n,p)==1 and all(pow(w,k,p)!=1 for k in range(1,n))]
 for _ in range(reps):
  w=rng.choice(ws);r=rng.randrange(1,n)
  decision(make(n,p,r,[rng.randrange(p) for _ in range(n)],w),'random_raw')
  for a in [0,1,rng.randrange(n)]:
   modes=[(b,rng.randrange(1,p)) for b in rng.sample(range(n),rng.randrange(r+1))]
   decision(make(n,p,r,wave(n,p,w,a,modes),w),'random_constructed')
print('differentials passed',dict(S),flush=True)

# Every N4 field coefficient vector, all N8 supports, irregular larger supports.
for n,p in [(4,5),(8,17),(16,97),(64,257),(512,7681)]:
 w=root(n,p);table=[pow(w,j,p) for j in range(n)]
 if n==4:mode_sets=[[(b,g) for b,g in enumerate(gs) if g] for gs in itertools.product(range(p),repeat=n)]
 elif n==8:mode_sets=[[(b,rng.randrange(1,p)) for b in range(n) if mask>>b&1] for mask in range(1<<n)]
 else:
  subsets=[list(range(s)) for s in [0,1,2,3,n//2,n]]+[rng.sample(range(n),s) for s in [1,2,3,7,n//2,n]]
  subsets += [list(range(parity,n,2)) for parity in range(2)]
  mode_sets=[[(b,rng.randrange(1,p)) for b in I] for I in subsets]
 for pairs in mode_sets:
  modes=[dict(b=b,gamma=g) for b,g in pairs];meter=c.Meter(20_000_000);detail={}
  out=c._phase_one_dft(modes,table,d.Field(p,meter),detail)
  assert out==direct(make(n,p,max(1,min(n-1,len(modes))),wave(n,p,w,1,pairs),w))
  assert meter.counts==gauss_cost(modes,n),(n,modes,meter.counts,gauss_cost(modes,n))
  assert meter.used==sum(meter.counts.values())==sum(meter.stages.values())
  for delta,trace in enumerate(detail['parity_ffts']):
   I=[((b+delta)//2)%(n//2) for b,g in pairs if b%2==delta]
   for depth in range((n//2).bit_length()):assert trace['calls_by_depth'].get(depth,0)==len({i%(1<<depth) for i in I})
  S['phase_one_output_kernel_exact_cost']+=1
# Direct Gauss sums at every root of several fields, not candidate formula alone.
for n,p in [(4,5),(4,13),(8,17),(8,41),(16,97),(32,97),(64,257)]:
 for w in [q for q in range(1,p) if pow(q,n,p)==1 and pow(q,n//2,p)!=1]:
  G=[sum(pow(w,(j*j+k*j)%n,p) for j in range(n))%p for k in range(n)]
  for k in range(n):assert G[k]==(0 if k%2 else G[0]*pow(w,-(k//2)**2,p)%p);S['gauss_identity_coordinates']+=1
print('kernels passed',dict(S),flush=True)

# Late corruption must fail actual phase-one rechirped synthesis.
w=root(16,97)
for r,x in [(2,[0]*15+[1]),(2,wave(16,97,w,1,[(0,3)])[:-1]+[0]),(2,[pow(5,j,97) for j in range(16)]),(2,[(j+1)*pow(w,j*j+3*j,97)%97 for j in range(16)])]:
 R=decision(make(16,97,r,x,w),'adversarial')
 if x[-1]==0:assert R['phase_one']['status']=='FULL_RAW_SYNTHESIS_REJECT'
# False BM coefficients still require real all-coordinate synthesis.
P=make(16,97,2,wave(16,97,w,1,[(1,3),(5,7)]),w)
for false in [(0,[1]),(1,[1,96]),(3,[1,0,0,1]),(1,[1,0,1])]:
 with patch.object(c,'_bm',return_value=false):R=c.recognize(P,MAX)
 assert R['route']=='dense_reference_fallback' and check(P,R,20_000_000)['status']=='VERIFIED_MEMBER';S['fault_containment']+=1
# No phase-one path for N2. Unsupported 2N-root curvature remains outside family.
assert decision(make(4,17,1,[pow(2,j*j,17) for j in range(4)],4),'unsupported_curvature')['status']=='NONMEMBER'

fixtures=[make(4,5,1,[0]*4),make(4,5,1,[1]*4),make(4,5,1,wave(4,5,2,1,[(1,1)]),2),make(8,17,1,wave(8,17,2,1,[(0,1)]),2),make(8,17,1,wave(8,17,2,2,[(0,1)]),2),make(4,5,1,[1,0,0,0]),make(3,7,1,[1]*3),make(2,3,1,[1,0])]
DETAILS['budget_fixtures']=[]
for P in fixtures:
 R=c.recognize(P,MAX);T=R['ledger']['work_units'];assert R['status'] in ('MEMBER','NONMEMBER')
 for cap in range(T):
  Q=c.recognize(P,replace(MAX,max_work_units=cap));assert Q['status']=='LIMIT' and Q['representation'] is None and Q['dft'] is None,(cap,Q);ledger(Q);S['every_unit_cutoffs']+=1
  if 'fallback' in Q['ledger']:
   D=d.recognize(P,replace(MAX,max_work_units=cap-Q['ledger']['frontend']['work_units']));assert Q['ledger']['fallback']==D['ledger'];assert Q['status']==D['status'];S['residual_fallback_replays']+=1
 assert c.recognize(P,replace(MAX,max_work_units=T))['status']==R['status']
 DETAILS['budget_fixtures'].append(dict(problem=P,status=R['status'],route=R['route'],work_units=T))
print('cutoffs passed',dict(S),flush=True)

# Actual API arithmetic calls must match the aggregate ledger, including fallback.
original={k:getattr(d.Field,k) for k in ('add','sub','mul','inverse','power')}
for P in fixtures:
 seen=Counter()
 def wrapper(k):
  def run(self,*args):
   seen[k]+=1
   if k=='inverse':seen['inverse_bits']+=(self.p-2).bit_length()
   return original[k](self,*args)
  return run
 with patch.multiple(d.Field,**{k:wrapper(k) for k in original}):R=c.recognize(P,MAX)
 C=R['ledger']['counts'];assert C.get('field_additions',0)==seen['add']+seen['sub'];assert C.get('field_multiplications',0)==seen['mul'];assert C.get('scalar_inversions',0)==seen['inverse'];assert C.get('power_calls',0)==seen['power'];assert C.get('power_bit_iterations',0)==seen['inverse_bits'];S['actual_arithmetic_audits']+=1

P=make(8,17,2,[0]*8)
class I(int):pass
class L(list):pass
class Dct(dict):pass
bad=[(None,'INVALID_INPUT'),({},'INVALID_INPUT'),(Dct(P),'INVALID_INPUT')]
for key,val,status in [('N',True,'INVALID_PARAMETERS'),('N',I(8),'INVALID_PARAMETERS'),('N',1,'INVALID_PARAMETERS'),('r',0,'INVALID_PARAMETERS'),('r',8,'INVALID_PARAMETERS'),('omega',0,'INVALID_PARAMETERS'),('omega',1,'INVALID_PARAMETERS'),('omega',17,'INVALID_PARAMETERS'),('p',65,'INVALID_PARAMETERS'),('p',19,'INVALID_PARAMETERS'),('x',[0]*7,'INVALID_INPUT'),('x',[0]*7+[True],'INVALID_INPUT'),('x',[0]*7+[-1],'INVALID_INPUT'),('x',[0]*7+[17],'INVALID_INPUT'),('x',L([0]*8),'INVALID_INPUT')]:bad.append((dict(P,**{key:val}),status))
for Q,status in bad:
 R=c.recognize(Q,MAX);assert R['status']==status and R['representation'] is None and R['dft'] is None;ledger(R);S['invalid_api_controls']+=1
for lim in [None,{},replace(MAX,max_n=True),replace(MAX,max_r=-1),replace(MAX,max_n=513),replace(MAX,max_r=129),replace(MAX,max_p_bits=65),replace(MAX,max_work_units=20_000_001)]:assert c.recognize(P,lim)['status']=='INVALID_PARAMETERS';S['invalid_limit_controls']+=1
for key,val in [('max_n',4),('max_r',1),('max_p_bits',4)]:assert c.recognize(P,replace(MAX,**{key:val}))['status']=='LIMIT';S['dimension_controls']+=1
Q=make(2,(1<<61)-1,1,[0,0],(1<<61)-2);R=c.recognize(Q,replace(MAX,max_work_units=1000));assert R['status']=='LIMIT' and R['ledger']['stage']=='primality';S['prime_limit_controls']+=1
assert c.recognize(dict(P,x=tuple(P['x'])),MAX)['status']=='MEMBER'

# Hard N/r boundary, true nonzero phase, all direct outputs and final-write fail-closed.
n,p=512,7681;w=root(n,p);pairs=[(i*3%n,i+1) for i in range(128)];P=make(n,p,128,wave(n,p,w,1,pairs),w);R=c.recognize(P,MAX)
assert R['status']=='MEMBER' and R['route']=='sparse_phase_one',R['route'];assert R['dft']==direct(P);assert check(P,R,20_000_000)['status']=='VERIFIED_MEMBER'
T=R['ledger']['work_units'];Q=c.recognize(P,replace(MAX,max_work_units=T-1));assert Q['status']=='LIMIT' and Q['dft'] is None and Q['representation'] is None and Q['ledger']['stage']=='phase_one.output_writes';S['hard_boundary_controls']+=1
DETAILS['N512_r128_final_write']=dict(problem=P,total=T,ledger=R['ledger'],short_status=Q['status'],short_reason=Q['reason'])
# Emit reproducible small route examples.
for i,P in enumerate(fixtures):
 (BASE/'examples'/f'fixture_{i}_input.json').write_text(json.dumps(P,indent=2)+'\n');(BASE/'examples'/f'fixture_{i}_result.json').write_text(json.dumps(c.recognize(P,MAX),indent=2)+'\n')
for raw,status in [(json.dumps(fixtures[3]).encode(),'MEMBER'),(b'{"N":4,"N":4}','INVALID_INPUT'),(b'Infinity','INVALID_INPUT'),(b'{}{}','INVALID_INPUT'),(b'\xff','INVALID_INPUT'),(b'['*2000+b']'*2000,'INVALID_INPUT'),(b' '*1048576,'INVALID_INPUT'),(b' '*1048577,'LIMIT')]:
 out=subprocess.run([sys.executable,str(BASE/'chirp_phase_one.py')],input=raw,capture_output=True,check=True);assert json.loads(out.stdout)['status']==status;S['cli_controls']+=1
R=dict(status='PASS',counts=dict(S),routes=dict(ROUTES),details=DETAILS,seconds=time.monotonic()-START,source_sha256={f:hashlib.sha256((BASE/f).read_bytes()).hexdigest() for f in ['test_phase_one.py','chirp_phase_one.py','accepted_dispatch_v1.py','reference_v1.py','check_certificate_v1.py']})
(BASE/'TEST_RESULTS.json').write_text(json.dumps(R,indent=2)+'\n');print(json.dumps({k:v for k,v in R.items() if k!='details'},indent=2))
