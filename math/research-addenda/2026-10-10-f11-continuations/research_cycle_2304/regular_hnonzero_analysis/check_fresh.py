"""Independent standard-library verifier for this packet. All upstream inputs are inert JSON."""
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path
from copy import deepcopy
import json,hashlib,time,signal
signal.signal(signal.SIGALRM, lambda *a: (_ for _ in ()).throw(TimeoutError('240-second exact-check bound')))
signal.alarm(240)
OUT=Path(__file__).parent;C=json.loads((OUT/'CANDIDATE.json').read_text());a=json.load(open('research_cycle_2014/fused_chart_atlas/CERTIFICATE.json'))
ZERO=(Q(0),)*10;ONE=(Q(1),)+(Q(0),)*9
@lru_cache(maxsize=200000)
def cmul(a,b):
 t=[Q(0)]*19
 for i,x in enumerate(a):
  if x:
   for j,y in enumerate(b):
    if y:t[i+j]+=x*y
 for j in range(18,9,-1):
  h=t[j]
  if h:
   for k in range(10):t[j-10+k]-=h
 return tuple(t[:10])
def cadd(a,b):return tuple(x+y for x,y in zip(a,b))
def add(a,b):
 out=dict(a)
 for m,c in b.items():
  v=cadd(out.get(m,ZERO),c)
  if v!=ZERO:out[m]=v
  else:out.pop(m,None)
 return out
def neg(a):return {m:tuple(-x for x in v) for m,v in a.items()}
def mul(a,b):
 out={}
 for m,x in a.items():
  for n,y in b.items():
   h=tuple(i+j for i,j in zip(m,n));v=cadd(out.get(h,ZERO),cmul(x,y))
   if v!=ZERO:out[h]=v
   else:out.pop(h,None)
 return out
def one(n):return {(0,)*n:ONE}
def var(n,j):m=[0]*n;m[j]=1;return {tuple(m):ONE}
def power(a,k,n):
 out=one(n)
 for _ in range(k):out=mul(out,a)
 return out
def parse(ts):
 out={}
 for m,v,d in ts:
  assert len(v)==10 and d>0 and tuple(m) not in out
  co=tuple(Q(x,d) for x in v);assert co!=ZERO;out[tuple(m)]=co
 return out
def raw_eval(ts,variables,env):
 n=4;deg=[max((row[0][j] for row in ts),default=0) for j in range(len(variables))];ids=[j for j,k in enumerate(deg) if k];D=one(n);pw={}
 for j in ids:
  N,d=env[variables[j]];D=mul(D,power(d,deg[j],n));pw[j]=[mul(power(N,k,n),power(d,deg[j]-k,n)) for k in range(deg[j]+1)]
 N={}
 for ex,v,d in ts:
  t={(0,)*n:tuple(Q(x,d) for x in v)}
  for j in ids:t=mul(t,pw[j][ex[j]])
  N=add(N,t)
 return N,D
def divpair(n,d):return mul(n[0],d[1]),mul(n[1],d[0])
def eq(p,q,label):assert p==q,label
pins=C['source_hashes']
for p,h in pins.items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h,p
receipt=json.load(open('research_cycle_2016/three_input_atlas_review/RECEIPT.json'))
assert receipt['candidate_sha256']==pins['research_cycle_2014/fused_chart_atlas/CERTIFICATE.json']
pp={}
for p,h in a['source_hashes'].items():
 assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h
 for key,val in json.load(open(p)).get('polynomials',{}).items():
  if len(key)==64:pp[key]=val
v7=a['variables'];v16=[0,11,22,25,34,39,41,44,49,52,55,65,83,88,91,92]
base=next(x for x in a['branches'] if x['name']=='H_nonzero__regular')
checks=[]
def check_struct(c):
 assert c['variables']==[11,34,41,83]
 assert c['original_E41']==a['equations']['41']
 assert len(c['branches'])==2
 x,y=c['branches']
 assert x['name']=='E41_A_nonzero' and x['inputs']==[11,83] and x['added_conditions']==['A!=0'] and x['q_reconstruction']=={'numerator':'-B','denominator':'A'}
 assert y['name']=='E41_A_zero' and y['inputs']==[11,41,83] and y['added_conditions']==['A=0'] and y['added_equations']==['B=0'] and y['q_reconstruction']=='q remains a retained input'
 assert x['evaluation_order']=='Bind q=-B/A first; then execute the accepted branch definitions unchanged.' and x['reverse_map']=={'type':'projection','coordinates':[11,83]}
 assert y['evaluation_order']=='Execute the accepted branch definitions unchanged.' and y['reverse_map']=={'type':'projection','coordinates':[11,41,83]}
 for row in c['branches']:
  assert row['retained_branch']==base
  assert len(row['retained_branch']['retained_equations'])==50
  assert len(row['retained_branch']['retained_guards'])==19
 assert not any(c['claims'][k] for k in ['zero_pivot_infeasibility','chart_feasibility','dimension','novelty','full_fourier_factorization'])
check_struct(C);checks.append('exhaustive coefficient split and every original predicate retained')
P7={k:parse(v) for k,v in a['polynomials'].items()};x,b,c,q,d,e,r=[var(7,i) for i in range(7)]
eq(P7['F_D88'],add(mul(mul(mul(q,P7['F_M']),d),x),P7['F_K0']),'D88 affine identity')
eq(P7['F_J'],add(mul(P7['F_A'],P7['F_N88']),mul(P7['F_B'],P7['F_K0'])),'J identity')
eq(P7['x0_num'],neg(P7['F_J']),'regular x numerator')
eq(P7['x0_den'],mul(mul(mul(P7['F_B'],q),P7['F_M']),d),'regular x denominator')
eq(P7['F_E35_reduced'],add(mul(P7['F_A'],r),P7['F_B']),'E35 r relation')
checks += ['regular r=-B35/A35 with D88=-A35*N88/B35 and all denominator guards']
y0={m:v for m,v in P7['Q_x92_num'].items() if m[0]==0}
eq(add(P7['Q_x92_num'],mul(mul(x,d),P7['Q_x92_den'])),y0,'y shift')
N25=pp[next(x for x in a['inherited_definitions'] if x['variable']==25)['numerator']];t25=parse(N25)
for m,v in t25.items():
 assert m[v16.index(92)]<=1
 if m[0]:
  assert m[0]==1 and m[v16.index(65)]==1 and m[v16.index(92)]==0
  paired=list(m);paired[0]=0;paired[v16.index(65)]=0;paired[v16.index(92)]=1
  assert t25.get(tuple(paired))==v
 if m[v16.index(92)]:
  assert m[0]==0 and m[v16.index(65)]==0
  paired=list(m);paired[0]=1;paired[v16.index(65)]=1;paired[v16.index(92)]=0
  assert t25.get(tuple(paired))==v
assert all(not any(m[v16.index(j)] for j in [0,65,92]) for m in parse(pp[a['equations']['41']]))
checks += ['N25 affine shift invariant and E41 independent of representative coordinates']
zeta=(Q(0),Q(1))+(Q(0),)*8
unit=one(4);env0={0:({},unit),11:(var(4,0),unit),34:(var(4,1),unit),41:(var(4,2),unit),83:(var(4,3),unit),22:(unit,unit),49:(add({(0,0,0,0):zeta},neg(var(4,1))),unit)}
def algebra(cand):
 env=deepcopy(env0)
 def pol(name):return raw_eval(a['polynomials'][name],v7,env)
 for rec in cand['coordinate_ledger']:
  ind=rec['variable'];basis=rec['basis']
  if ind==65:expected={'numerator':'Q_d_num','denominator':'Q_d_den','kind':'atlas'};raw=divpair(pol('Q_d_num'),pol('Q_d_den'))
  elif ind==92:expected={'numerator':'Q_x92_num','denominator':'Q_x92_den','kind':'atlas'};raw=divpair(pol('Q_x92_num'),pol('Q_x92_den'))
  elif ind==88:expected={'numerator':'-F_B','denominator':'F_A','kind':'E35 consequence'};nn=pol('F_B');raw=divpair((neg(nn[0]),nn[1]),pol('F_A'))
  else:
   df=next(t for t in a['inherited_definitions'] if t['variable']==ind);expected={'numerator':df['numerator'],'denominator':df['denominator'],'kind':'original'};raw=divpair(raw_eval(pp[df['numerator']],v16,env),raw_eval(pp[df['denominator']],v16,env))
  assert basis==expected
  N,D,T=parse(rec['num']),parse(rec['den']),parse(rec['raw_denominator_over_reduced_denominator']);eq(raw[0],mul(N,T),f'coordinate {ind} numerator');eq(raw[1],mul(D,T),f'coordinate {ind} denominator divisor')
  env[ind]=(N,D)
 assert [t['variable'] for t in cand['coordinate_ledger']]==[65,92,88,25,39]
 raw=raw_eval(pp[a['equations']['41']],v16,env);N,D,T=parse(cand['E41_num']),parse(cand['E41_den']),parse(cand['E41_denominator_quotient']);eq(raw[0],mul(N,T),'original E41 numerator binding');eq(raw[1],mul(D,T),'original E41 denominator divisor')
 cn,cd=parse(cand['c_num']),parse(cand['c_den']);eq(cn,pol('Q_c_num')[0],'c numerator binding');eq(cd,pol('Q_c_den')[0],'c denominator binding');assert all(m[1]==m[2]==0 for poly in [cn,cd] for m in poly)
 k=cand['c_clearing_exponent'];assert k==max(m[1] for m in N)
 clear={}
 for m,v in N.items():
  rest=list(m);rest[1]=0;term=mul({tuple(rest):v},mul(power(cn,m[1],4),power(cd,k-m[1],4)));clear=add(clear,term)
 PP,AA,BB=[parse(cand[n]) for n in ['P','A','B']]
 eq(clear,PP,'cleared E41 polynomial');eq(PP,add(mul(AA,var(4,2)),BB),'q affine coefficient split')
 assert AA and BB and all(m[1]==m[2]==0 for poly in [AA,BB] for m in poly)
 return True
start=time.monotonic();algebra(C);checks+=['five rational coordinates and all cancellation divisors','original E41 numerator and denominator rebound','c support only b,e','E41=(A*q+B)/((b*H)^3*D_E) on the guarded chart']
print('Exact baseline passed in',round(time.monotonic()-start,3),'seconds',flush=True)
# Algebraic controls use the same multiplication checks, with no candidate-hash gate.
controls=[]
def reject(name,mutator,fn):
 t=deepcopy(C);mutator(t)
 try:fn(t)
 except AssertionError:controls.append(name);return
 raise AssertionError('mutation escaped: '+name)
reject('delete exceptional branch',lambda t:t['branches'].pop(),check_struct)
reject('delete exceptional compatibility',lambda t:t['branches'][1]['added_equations'].clear(),check_struct)
reject('delete original q nonzero guard',lambda t:t['branches'][0]['retained_branch']['retained_guards'].pop('x41'),check_struct)
reject('delete original residual',lambda t:t['branches'][1]['retained_branch']['retained_equations'].pop('41'),check_struct)
reject('alter q reconstruction sign',lambda t:t['branches'][0]['q_reconstruction'].update(numerator='B'),check_struct)
reject('unsupported feasibility claim',lambda t:t['claims'].update(chart_feasibility=True),check_struct)
reject('corrupt A coefficient',lambda t:t['A'][0][1].__setitem__(0,t['A'][0][1][0]+1),algebra)
reject('corrupt denominator quotient',lambda t:t['coordinate_ledger'][0]['raw_denominator_over_reduced_denominator'][0][1].__setitem__(0,t['coordinate_ledger'][0]['raw_denominator_over_reduced_denominator'][0][1][0]+1),algebra)
reject('alter E41 numerator',lambda t:t['E41_num'][0][1].__setitem__(0,t['E41_num'][0][1][0]+1),algebra)
reject('alter E41 denominator',lambda t:t['E41_den'][0][1].__setitem__(0,t['E41_den'][0][1][0]+1),algebra)
reject('change c clearing exponent',lambda t:t.update(c_clearing_exponent=2),algebra)
result={'status':'PASS: fresh author-side exact verification, independent review pending','checks':checks,'negative_controls_rejected':controls,'candidate_sha256':hashlib.sha256((OUT/'CANDIDATE.json').read_bytes()).hexdigest(),'source_pins_checked':len(a['source_hashes'])+len(pins),'arithmetic':'standard-library Fraction; polynomial addition and multiplication only; no field division, resultants, numerical roots or finite fields','historical_programs_executed':False,'scope':'H!=0 regular chart only; generic 2-input E41 pivot with retained 3-input exceptional chart; all 50 residuals and 19 original guards preserved','elapsed_seconds':round(time.monotonic()-start,3)}
(OUT/'CHECK_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2),flush=True)
