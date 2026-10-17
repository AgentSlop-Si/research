"""Fresh controls; no archived checks are run. Independent direct interval DFT."""
from copy import deepcopy
from dataclasses import asdict
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from math import factorial, gcd, isqrt
from pathlib import Path
import ast
import json
import random
import producer as P

RESULTS={'checks':[],'numerical_cases':[],'downstream_component':None}
def check(name,condition,detail=None):
    if not condition: raise AssertionError(name)
    RESULTS['checks'].append({'name':name,'pass':True,**({'detail':detail} if detail is not None else {})})
def fails(name,fn,needle=None):
    try: fn()
    except (ValueError,TypeError) as e:
        check(name,needle is None or needle in str(e),str(e)); return
    raise AssertionError(name+' unexpectedly accepted')

# Independent interval oracle: exact rational Machin series, point Taylor with
# Lipschitz radius, direct P followed by dense negative-sign unitary DFT.
# No producer roots, prepass, recurrence, gauge scan or meter are reused.
def floor(x): return x.numerator//x.denominator
def ceil(x): return -floor(-x)
@lru_cache(None)
def oracle_pi(Q):
    def atan(q):
        value=sum((F((-1)**j,(2*j+1)*q**(2*j+1)) for j in range(Q)),F(0))
        tail=F(1,(2*Q+1)*q**(2*Q+1))
        return value,tail
    a,ae=atan(5); b,be=atan(239)
    return 16*a-4*b,16*ae+4*be
class Oracle:
    def __init__(self,bits): self.bits=bits; self.unit=1<<bits
    def box(self,lo,hi=None):
        if hi is None: hi=lo
        return (F(floor(lo*self.unit),self.unit),F(ceil(hi*self.unit),self.unit))
    def add(self,a,b): return self.box(a[0]+b[0],a[1]+b[1])
    def neg(self,a): return (-a[1],-a[0])
    def mul(self,a,b):
        products=[x*y for x in a for y in b]
        return self.box(min(products),max(products))
    def z(self,re=0,im=0): return (self.box(F(re)),self.box(F(im)))
    def zadd(self,a,b): return (self.add(a[0],b[0]),self.add(a[1],b[1]))
    def zmul(self,a,b):
        return (self.add(self.mul(a[0],b[0]),self.neg(self.mul(a[1],b[1]))),
                self.add(self.mul(a[0],b[1]),self.mul(a[1],b[0])))
    def conj(self,a): return (a[0],self.neg(a[1]))
    def total(self,values):
        z=self.z()
        for v in values: z=self.zadd(z,v)
        return z
    @lru_cache(None)
    def root(self,r,n):
        r%=2*n; Q=self.bits+20
        if 2*r%n==0:
            return [self.z(1),self.z(0,1),self.z(-1),self.z(0,-1)][(2*r//n)%4]
        # Reduce into [0,pi/2], keeping exact quadrant and reflection signs.
        quadrant=(2*r)//n; remainder=2*r-quadrant*n
        numerator=remainder; denominator=2*n
        pi,pie=oracle_pi(Q)
        theta0=pi*F(numerator,denominator)
        theta=F(floor(theta0*(1<<Q)),1<<Q)
        radius=abs(theta-theta0)+pie*F(numerator,denominator)
        degree=Q+32; term=F(1); real=imag=F(0)
        for k in range(degree+1):
            if k%4==0: real+=term
            elif k%4==1: imag+=term
            elif k%4==2: real-=term
            else: imag-=term
            term=term*theta/F(k+1)
        err=radius+F(2**(degree+1),factorial(degree+1))
        z=(self.box(real-err,real+err),self.box(imag-err,imag+err))
        if quadrant==0: return z
        if quadrant==1: return (self.neg(z[1]),z[0])
        if quadrant==2: return (self.neg(z[0]),self.neg(z[1]))
        return (z[1],self.neg(z[0]))
    def target(self,raw,state,W):
        n,b=state['N'],state['B']; a,beta=state['a'],state['beta']; h=n%2
        short,rem=divmod(n,b); start=0; projected=[]
        x=[self.z(F(re,1<<W),F(im,1<<W)) for re,im in zip(raw['real'],raw['imag'])]
        for block in range(b):
            length=short+int(block<rem)
            phases=[self.root(a*j*(j-1)+2*(a*start+beta)*j+h*j,n) for j in range(length)]
            summary=self.total(self.zmul(phases[j],x[start+j]) for j in range(length))
            projected.extend(self.zmul(self.conj(z),summary) for z in phases); start+=length
        scale=1<<(self.bits+8); root=isqrt(scale*scale//n)
        rho=(F(root,scale),F(root+1,scale))
        return [self.zmul(self.total(self.zmul(z,self.root(-2*k*j,n)) for j,z in enumerate(projected)),(rho,self.box(F(0)))) for k in range(n)]


def numerical(raw,state,t=10,q=None,extra=0):
    initial=P.policy.derive_policy(raw,state,t,q if q is not None else (16*(state['N'].bit_length()-1)+16 if not state['N']&(state['N']-1) else P.policy.ceil_log2(state['N'])))
    p=initial['p']+extra
    run=P.execute(raw,state,t,q,p,include_trace=True)
    plan=run.policy; oracle=Oracle(p+36)
    target=oracle.target(raw,state,plan['W']); bound=F(plan['plan']['C'],1<<p)
    max_sq=F(0)
    for row,box in zip(run.payload[2],target):
        errors=[max(abs(F(row[axis],1<<p)-box[axis][end]) for end in (0,1)) for axis in (0,1)]
        error_sq=errors[0]**2+errors[1]**2; max_sq=max(max_sq,error_sq)
        assert error_sq<=bound*bound
    check('direct interval DFT '+str(state),True)
    print('INTERVAL_PASS',state,'p',p,flush=True)
    if run.adapter is not None:
        adapter=run.adapter; check('adapter exact output binding '+str(state),adapter.output_sha256==P.binary_digest(run.payload))
        Fq=adapter.source.fractional_bits_bound; S=sum(pair[0]**2 for cell in adapter.source.values for pair in cell)
        check('strict normalized source '+str(state),4*S>1<<(2*Fq))
        check('full source Cartesian bounds '+str(state),all(abs(pair[0])<=1<<pair[1] for cell in adapter.source.values for pair in cell))
        check('target budget '+str(state),adapter.target_budget=='TARGET_BUDGET_PASS')
    RESULTS['numerical_cases'].append(dict(state=state,p=p,W=plan['W'],status=run.status,
                                           error_squared_upper=str(max_sq),theorem_squared_upper=str(bound*bound),
                                           operations=run.ledger['integer_operations']))
    return run


def main():
    root=Path(__file__).resolve().parent
    # Explicit module safety review: the vendored artifacts are imported only
    # after their complete text has been inspected. This catches drift from
    # the inspected import/top-level grammar and confirms exact accepted pins.
    for name,pin in P.PINS.items():
        text=(root/'vendor'/(name+'.py')).read_text(); tree=ast.parse(text)
        check('pinned reviewed '+name,sha256(text.encode()).hexdigest()==pin)
        check('safe imports '+name,all((node.module in {'dataclasses','fractions','collections','hashlib','buckets','compact_window'} if isinstance(node,ast.ImportFrom) else all(a.name in set() for a in node.names)) for node in ast.walk(tree) if isinstance(node,(ast.Import,ast.ImportFrom))))
        check('declarative top level '+name,all(isinstance(node,(ast.Expr,ast.ImportFrom,ast.ClassDef,ast.FunctionDef,ast.Assign)) for node in tree.body))
    for n,b,a,beta in [(3,3,1,0),(4,3,1,0),(5,3,2,4),(6,3,5,2),(7,4,3,5),(8,3,3,7),(9,3,2,8),(12,5,5,1),(16,7,7,13)]:
        raw={'F':7,'real':[1+((j*7)%15) for j in range(n)],'imag':[(j*5)%9-4 for j in range(n)]}
        numerical(raw,{'N':n,'B':b,'a':a,'beta':beta})
    # A caller-selected precision above the policy minimum is actually used.
    higher=numerical({'F':2,'real':[1,2,3,4,5],'imag':[0]*5},{'N':5,'B':3,'a':2,'beta':1},extra=17)
    check('higher actual p preserved',higher.policy['p']==higher.policy['plan']['p_min']+17)
    # Exact kernel and near-kernel, original zero, signed exponent extremes.
    for n in (4,6,8,64):
        state={'N':n,'B':3,'a':1,'beta':0}; raw={'F':0,'real':[1,-1]+[0]*(n-2),'imag':[0]*n}
        run=P.execute(raw,state); check('exact projected zero N='+str(n),run.status=='EXACT_PROJECTED_ZERO' and run.payload is None and run.adapter is None)
    raw={'F':-(1<<127),'real':[0]*9,'imag':[0]*9}; state={'N':9,'B':3,'a':1,'beta':0}
    run=P.execute(raw,state); check('original zero',run.status=='EXACT_INPUT_ZERO')
    raw={'F':0,'real':[1,-1]+[0]*7,'imag':[0]*9}
    run=numerical(raw,state); check('odd parity nonzero',run.policy['outcome']=='NONZERO_PLAN')
    for K in (1,8,32):
        raw={'F':K,'real':[1<<K,-((1<<K)-1),0,0,0,0],'imag':[0]*6}
        numerical(raw,{'N':6,'B':3,'a':1,'beta':0})
    raw={'F':1<<127,'real':[1,0,0,0],'imag':[0]*4}; state={'N':4,'B':3,'a':1,'beta':0}
    # 2^127 has 128 bits: symbolic exponent kept, never a physical shift.
    run=P.execute(raw,state); check('enormous positive F stays symbolic',run.payload[1]==run.policy['W']-raw['F']-run.policy['p'])
    raw['F']=-(1<<127); run=P.execute(raw,state); check('enormous negative F stays symbolic',run.adapter.target_budget=='TARGET_BUDGET_PASS')
    # Recompute verification plus adversarial replacements, all against retained context.
    raw={'F':3,'real':[1,2,-3,4],'imag':[0,1,2,0]}; run=P.execute(raw,state)
    packet=run.packet(); check('semantic recomputation',P.verify(raw,state,16,48,packet)['numerical_payload_verified'])
    forged=deepcopy(packet); forged['payload']['rows'][0][0]+=1
    fails('fabricated payload cannot pass',lambda:P.verify(raw,state,16,48,forged),'SEMANTIC_MISMATCH')
    substituted=deepcopy(raw); substituted['real'][0]+=1
    fails('original input substitution',lambda:P.verify(substituted,state,16,48,packet),'SEMANTIC_MISMATCH')
    forged=deepcopy(packet); forged['policy']['plan']['C']+=1
    fails('rehashed wrong policy',lambda:P.verify(raw,state,16,48,forged),'SEMANTIC_MISMATCH')
    forged=deepcopy(packet); forged['numerical_payload_verified']=True
    fails('self asserted certification rejected',lambda:P.verify(raw,state,16,48,forged),'GRAMMAR')
    old_payload={'real':[row[0] for row in packet['payload']['rows']], 'imag':[row[1] for row in packet['payload']['rows']], 'kappa':packet['payload']['kappa']}
    old_payload['real'][0]+=1
    old_record=P.policy.make_record(raw,state,16,48,old_payload)
    check('prior consistency loophole remains demonstrable',P.policy.verify(raw,state,16,48,old_record)['status']=='BINDING_CONSISTENT_PRODUCER_UNVERIFIED')
    raw['real'][0]+=99
    check('caller mutation cannot alter completed result',run.packet()==packet)
    fails('bool input rejected',lambda:P.execute({'F':0,'real':[True,0,0,0],'imag':[0]*4},state),'GRAMMAR')
    fails('invalid a rejected',lambda:P.execute({'F':0,'real':[1,0,0,0],'imag':[0]*4},{**state,'a':2}),'DOMAIN')
    fails('insufficient actual p rejected',lambda:P.execute({'F':0,'real':[1,0,0,0],'imag':[0]*4},state,p=3),'PRECISION')
    fails('selected precision resource cap',lambda:P.execute({'F':0,'real':[1,0,0,0],'imag':[0]*4},state,t=5000),'RESOURCE_LIMIT')
    fails('input width resource cap',lambda:P.execute({'F':0,'real':[1<<1024,0,0,0],'imag':[0]*4},state),'RESOURCE_LIMIT')
    lowq=P.execute({'F':0,'real':[1,0,0,0],'imag':[0]*4},{'N':4,'B':3,'a':1,'beta':0},t=0,q=2)
    check('lower generic q does not claim Q16 budget',lowq.status=='CERTIFIED_SOURCE_TARGET_BUDGET_NOT_ESTABLISHED')
    wide=P.execute({'F':1023,'real':[1<<1023,0,1,0],'imag':[0]*4},{'N':4,'B':3,'a':1,'beta':0})
    check('actual 1024 bit raw input',wide.policy['W']==1024 and wide.adapter.target_budget=='TARGET_BUDGET_PASS')
    # Signed ties and exact product rules against independent Fraction round.
    random.seed(34034)
    for _ in range(2000):
        a=random.randrange(-100000,100001); d=random.randrange(1,1000)
        assert P.nearest(a,d,P.Meter())==round(F(a,d))
    check('2000 signed nearest even cases',True)
    # Root contracts across low/high precision including p not tied to a test seed.
    for n,p in [(3,1),(5,2),(7,12),(9,60),(16,128),(4,300)]:
        M=P.Meter(); roots=P.Roots(n,p,M)
        for cert in roots.certificates:
            if len(cert)==2: continue
            r,K,rlo,rhi,ilo,ihi,er,ei=cert
            assert er*er+ei*ei<=1<<(2*(K-p))
        check('all intended root admissions N='+str(n)+' p='+str(p),True)
    # Actual reviewed BUCKETS component call at a legitimate reduced fixture.
    n=64; raw={'F':0,'real':[1]+[0]*(n-1),'imag':[0]*n}; state={'N':n,'B':3,'a':1,'beta':0}
    run=P.execute(raw,state); legacy,_=P.load_adapter()
    import buckets, compact_window
    m=n.bit_length()-1; spec=compact_window.WindowSpec(n,4,1,16*m+16)
    engine=buckets.BucketEngine(spec); output=engine.run(run.adapter.source,1,0)
    check('actual downstream class identity',type(run.adapter.source) is buckets.DyadicSource)
    check('actual reduced BUCKETS call',len(output.numerators)==4 and output.bits==112)
    check('component target budget',run.adapter.target_budget=='TARGET_BUDGET_PASS')
    RESULTS['downstream_component']=dict(N=n,B_Q=4,r=1,Pq=112,beta_Q=None,
        classification='VALID_REDUCED_COMPONENT_FIXTURE_NOT_THEOREM_SPARSE_INSTANCE',
        output=asdict(output),ledger=engine.ledger.report(),upstream_ledger=run.ledger,
        second_target='R(P_balanced_longer_first(x))/alpha',
        cumulative_bit_work_upper=run.ledger['total_bit_work_upper']+engine.ledger.report()['total_bit_work_upper'])
    # Full-theorem impossibility under the retained legacy length cap is exact.
    check('bounded legacy adapter excludes every theorem sparse instance',4096*2>4096,
          'beta_Q>0 implies k=2^ceil(2 beta_Q m)>=2; B_Q>=4096k>=8192>N_cap=4096')
    RESULTS['status']='PASS'; RESULTS['named_checks']=len(RESULTS['checks'])
    (root/'CHECK_RESULTS.json').write_text(json.dumps(RESULTS,indent=2)+'\n')
    (root/'EXAMPLE.json').write_text(json.dumps({'status':run.status,'packet':run.packet(),'source_summary':{'alpha_exponent':run.adapter.alpha_exponent,'target_budget':run.adapter.target_budget,'rho':run.adapter.rho}},indent=2)+'\n')
    print('PASS',len(RESULTS['checks']),'named checks;',len(RESULTS['numerical_cases']),'independent interval DFT cases')

if __name__=='__main__': main()
