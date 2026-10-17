"""Fresh independent controls. Standard library, local read/copy/write only.
No candidate test suite or historical producer is imported.
"""
from copy import deepcopy
from dataclasses import FrozenInstanceError
from fractions import Fraction as Q
from hashlib import sha256
from math import gcd, isqrt, factorial
from pathlib import Path
import json
import random
import sys

SOURCE = Path(__file__).resolve().parent.parent/'source'
sys.path.insert(0, str(SOURCE))
import producer as P

RESULTS = {'checks': [], 'source_hashes': {p.relative_to(SOURCE).as_posix(): sha256(p.read_bytes()).hexdigest() for p in [SOURCE/'producer.py',SOURCE/'policy.py',*(SOURCE/'vendor').glob('*.py')]}}
def ok(name, condition, **detail):
    if not condition: raise AssertionError(name)
    RESULTS['checks'].append({'name':name, 'pass':True, **detail})
def reject(name, fn, expected):
    try: fn()
    except (ValueError, TypeError, RecursionError) as exc:
        ok(name, expected in str(exc), exception=str(exc)); return
    raise AssertionError(name + ' accepted')

# Outward rational interval arithmetic, rounded after each operation to keep
# denominator growth bounded. All real elementary functions use a pi identity
# distinct from the producer and independent direct projection/DFT sums.
class Interval:
    def __init__(self, bits):
        self.bits=bits; self.S=1<<bits; self.cache={}
        def atan(q):
            v=sum((Q((-1)**j, (2*j+1)*q**(2*j+1)) for j in range(bits)),Q(0))
            e=Q(1,(2*bits+1)*q**(2*bits+1))
            return v-e,v+e
        a,b=atan(2),atan(3)
        self.pi=self.enclose(4*(a[0]+b[0]),4*(a[1]+b[1]))
    def enclose(self, lo, hi=None):
        if hi is None: hi=lo
        l=lo*self.S; h=hi*self.S
        return (Q(l.numerator//l.denominator,self.S),Q(-((-h.numerator)//h.denominator),self.S))
    def add(self,a,b): return self.enclose(a[0]+b[0],a[1]+b[1])
    def neg(self,a): return (-a[1],-a[0])
    def mul(self,a,b):
        v=[x*y for x in a for y in b]
        return self.enclose(min(v),max(v))
    def divnat(self,a,n): return self.enclose(a[0]/n,a[1]/n)
    def z(self,r=0,i=0): return (self.enclose(Q(r)),self.enclose(Q(i)))
    def plus(self,a,b): return (self.add(a[0],b[0]),self.add(a[1],b[1]))
    def times(self,a,b):
        return (self.add(self.mul(a[0],b[0]),self.neg(self.mul(a[1],b[1]))),self.add(self.mul(a[0],b[1]),self.mul(a[1],b[0])))
    def conj(self,a): return (a[0],self.neg(a[1]))
    def sum(self, values):
        out=self.z()
        for value in values: out=self.plus(out,value)
        return out
    def root(self,r,n):
        r%=2*n
        if (r,n) in self.cache: return self.cache[r,n]
        quadrant=(2*r)//n; rem=2*r-quadrant*n
        if rem==0: z=[self.z(1),self.z(0,1),self.z(-1),self.z(0,-1)][quadrant]
        else:
            theta=self.divnat(self.mul(self.pi,self.enclose(Q(rem))),2*n)
            center=(theta[0]+theta[1])/2
            # Point Taylor at an exact dyadic center; Lipschitz argument error.
            center=Q((center*self.S).numerator//(center*self.S).denominator,self.S)
            e=max(center-theta[0],theta[1]-center)
            term=self.enclose(Q(1)); real=self.enclose(Q(0)); imag=self.enclose(Q(0))
            degree=self.bits+20
            for k in range(degree+1):
                if k%4==0: real=self.add(real,term)
                elif k%4==1: imag=self.add(imag,term)
                elif k%4==2: real=self.add(real,self.neg(term))
                else: imag=self.add(imag,self.neg(term))
                term=self.divnat(self.mul(term,self.enclose(center)),k+1)
            e+=Q(2**(degree+1),factorial(degree+1))
            z=(self.enclose(real[0]-e,real[1]+e),self.enclose(imag[0]-e,imag[1]+e))
            if quadrant==1: z=(self.neg(z[1]),z[0])
            elif quadrant==2: z=(self.neg(z[0]),self.neg(z[1]))
            elif quadrant==3: z=(z[1],self.neg(z[0]))
        self.cache[r,n]=z
        return z
    def target(self, raw, state, W):
        n,b,a,beta=[state[k] for k in ('N','B','a','beta')]
        x=[self.z(Q(re,1<<W),Q(im,1<<W)) for re,im in zip(raw['real'],raw['imag'])]
        projected=[]; start=0
        for block in range(b):
            length=n//b+int(block<n%b)
            phase=[self.root(a*t*(t-1)+2*(a*start+beta)*t+(n%2)*t,n) for t in range(length)]
            d=self.sum(self.times(phase[t],x[start+t]) for t in range(length))
            projected.extend(self.times(self.conj(z),d) for z in phase); start+=length
        h=isqrt(self.S*self.S//n)
        rho=(Q(h,self.S),Q(h+1,self.S))
        return [self.times(self.sum(self.times(z,self.root(-2*k*j,n)) for j,z in enumerate(projected)),(rho,self.enclose(Q(0)))) for k in range(n)]

def numeric(raw,state,t=0,q=None):
    run=P.execute(raw,state,t,q,include_trace=True)
    if run.payload is None: raise AssertionError('unexpected zero numeric control')
    p=run.policy['p']; W=run.policy['W']; oracle=Interval(p+50)
    target=oracle.target(raw,state,W); bound=Q(run.policy['plan']['C'],1<<p)
    worst=Q(0)
    for row,box in zip(run.payload[2],target):
        sq=sum(max(abs(Q(row[a],1<<p)-box[a][i]) for i in (0,1))**2 for a in (0,1))
        worst=max(worst,sq)
    ok('independent direct projected DFT',worst<=bound*bound,state=state,p=p,error_squared_upper=str(worst),bound_squared=str(bound*bound))
    trace=json.loads(run.trace_bytes)
    for certificate in trace['roots']:
        if len(certificate)==2: continue
        r,K,rlo,rhi,ilo,ihi,er,ei=certificate
        independent=oracle.root(r,state['N'])
        for axis,(lo,hi) in enumerate([(rlo,rhi),(ilo,ihi)]):
            assert Q(lo,1<<K)<=independent[axis][0]<=independent[axis][1]<=Q(hi,1<<K)
    ok('independent intended-root enclosure containment',True,state=state)
    ledger=run.ledger
    expected=ledger['policy_bit_work_upper']+ledger['producer_bit_work_upper']+ledger['serialization_bit_work_upper']+ledger['dependency_loading_bit_work_upper']
    if run.adapter: expected+=run.adapter.receipt.total_bit_work_upper
    ok('receipt additive work identity',ledger['total_bit_work_upper']==expected,state=state)
    ok('trace and ledger serialized bytes charged',ledger['serialization_bytes_upper']>=len(run.trace_bytes)+len(run.input_context)+len(run.policy_bytes)+len(run.ledger_bytes),state=state)
    return run

random.seed(341017)
for n,b,a,beta in [(3,3,2,2),(4,4,3,3),(5,5,4,4),(6,5,5,5),(7,3,6,6),(8,7,7,7),(10,3,9,9),(11,7,7,10),(16,16,15,15)]:
    raw={'F':-17,'real':[random.randrange(-8,9) for _ in range(n)],'imag':[random.randrange(-8,9) for _ in range(n)]}
    numeric(raw,dict(N=n,B=b,a=a,beta=beta),q=P.policy.ceil_log2(n))

raw={'F':3,'real':[1,2,-3,4],'imag':[0,1,2,0]}; state=dict(N=4,B=3,a=3,beta=3)
run=P.execute(raw,state); packet=run.packet()
receipt=P.verify(raw,state,16,48,packet)
ok('baseline semantic replay',receipt['numerical_payload_verified'])
for field in ('raw','state','t','q','p'):
    forged=deepcopy(packet)
    if field=='raw': forged['context'][field]['real'][0]+=1
    elif field=='state': forged['context'][field]['beta']=2
    else: forged['context'][field]+=1
    reject('changed retained '+field,lambda:P.verify(raw,state,16,48,forged),'SEMANTIC_MISMATCH')
for kind in ('row','sign','scale','swap','bool','null','policy'):
    forged=deepcopy(packet)
    if kind=='row': forged['payload']['rows'][0][0]+=1
    elif kind=='sign': forged['payload']['rows'][0][0]*=-1
    elif kind=='scale': forged['payload']['kappa']+=1
    elif kind=='swap': forged['payload']['rows'][0],forged['payload']['rows'][1]=forged['payload']['rows'][1],forged['payload']['rows'][0]
    elif kind=='bool': forged['payload']['rows'][0][0]=True
    elif kind=='null': forged['payload']=None
    else: forged['policy']['raw_input_sha256']='0'*64
    reject('forged '+kind,lambda:P.verify(raw,state,16,48,forged),'SEMANTIC_MISMATCH')
# All legacy commitments are genuinely reconstructed, and a fresh legacy
# adapter receipt succeeds on the fabricated output. Neither provides semantic
# equality to the original raw input, which the new replay must reject.
legacy,_=P.load_adapter()
forged=deepcopy(packet); forged['payload']['rows'][0][0]+=1
fp=(forged['payload']['N'],forged['payload']['kappa'],tuple(tuple(r) for r in forged['payload']['rows']))
cert=list(run.adapter.producer_contract.fields); cert[6]=P.binary_digest(fp)
adapted=legacy.adapt(fp,tuple(cert))
old={'real':[r[0] for r in fp[2]],'imag':[r[1] for r in fp[2]],'kappa':fp[1]}
record=P.policy.make_record(raw,state,16,48,old)
ok('fully rehashed forged legacy record accepts consistently',P.policy.verify(raw,state,16,48,record)['status']=='BINDING_CONSISTENT_PRODUCER_UNVERIFIED')
ok('rehashed forged legacy adapter accepts conditionally',adapted.status=='VALID_SOURCE' and adapted.output_sha256==P.binary_digest(fp))
reject('new semantic replay defeats rehashed old record and adapter',lambda:P.verify(raw,state,16,48,forged),'SEMANTIC_MISMATCH')
changed=deepcopy(raw); changed['real'][0]+=1
reject('raw argument substitution',lambda:P.verify(changed,state,16,48,packet),'SEMANTIC_MISMATCH')
export=run.packet(); export['payload']['rows'][0][0]+=1
ok('packet mutation leaves actual immutable payload unchanged',run.packet()==packet)
raw['real'][0]+=99
ok('caller mutation leaves retained context unchanged',run.packet()==packet)
try: run.payload=(0,0,())
except FrozenInstanceError: ok('Run frozen',True)
else: raise AssertionError('Run not frozen')

# Zero branch replay and state/resource grammar. No artificial budget lowering
# or source monkeypatching is used to manufacture test outcomes.
for n,raw,expected in [(4,{'F':0,'real':[0]*4,'imag':[0]*4},'EXACT_INPUT_ZERO'),(6,{'F':0,'real':[1,-1,0,0,0,0],'imag':[0]*6},'EXACT_PROJECTED_ZERO')]:
    s=dict(N=n,B=3,a=1,beta=0); r=P.execute(raw,s,q=3)
    v=P.verify(raw,s,16,3,r.packet())
    ok('verified distinct zero '+expected,r.status==expected and r.payload is None and r.adapter is None and v['numerical_payload_verified'])
reject('N cap excludes 65',lambda:P.execute({'F':0,'real':[1]*65,'imag':[0]*65},dict(N=65,B=3,a=1,beta=0)),'RESOURCE_LIMIT')
reject('raw integer bool rejected',lambda:P.execute({'F':False,'real':[1]*4,'imag':[0]*4},dict(N=4,B=3,a=1,beta=0)),'GRAMMAR')
reject('p cap excludes 4097',lambda:P.execute({'F':0,'real':[1,0,0,0],'imag':[0]*4},dict(N=4,B=3,a=1,beta=0),p=4097),'RESOURCE_LIMIT')
reject('strict packet extra flags',lambda:P.verify({'F':0,'real':[1]*4,'imag':[0]*4},dict(N=4,B=3,a=1,beta=0),16,48,{**packet,'numerical_payload_verified':True}),'GRAMMAR')
malicious=deepcopy(packet); malicious['context']='x'*(4*1024*1024)
reject('untrusted packet serialization bounded',lambda:P.verify({'F':0,'real':[1]*4,'imag':[0]*4},dict(N=4,B=3,a=1,beta=0),16,48,malicious),'RESOURCE_LIMIT')

# Genuine reduced fixture and exact theorem-domain obstruction.
import buckets, compact_window
n=64; s=dict(N=n,B=3,a=1,beta=0); r=P.execute({'F':0,'real':[1]+[0]*63,'imag':[0]*64},s)
spec=compact_window.WindowSpec(64,4,1,112)
engine=buckets.BucketEngine(spec); output=engine.run(r.adapter.source,3,7)
ok('actual independent reduced BUCKETS invocation',len(output.numerators)==4 and output.bits==112 and type(r.adapter.source) is buckets.DyadicSource,origin=spec.origin,queries=engine.ledger.report()['operations']['source_query'])
ok('reduced fixture fails theorem window delta guard',not engine._window.budget['theorem_delta_M_minus_4'])
for m in range(4,13):
    for beta in (Q(1,10**6),Q(1,8),Q(49,100)):
        k=1<<(-((-2*beta.numerator*m)//beta.denominator))
        ok('theorem source-cap obstruction',k>=2 and 4096*k>min(4096,1<<m),m=m,beta=str(beta),k=k)
RESULTS['replay_receipt']=receipt
RESULTS['status']='PASS'; RESULTS['named_checks']=len(RESULTS['checks'])
Path(__file__).with_name('REVIEW_CONTROLS.json').write_text(json.dumps(RESULTS,indent=2)+'\n')
print('PASS',len(RESULTS['checks']),'independent named controls',flush=True)
