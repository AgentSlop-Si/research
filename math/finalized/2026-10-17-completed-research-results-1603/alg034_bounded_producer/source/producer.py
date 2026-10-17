"""Fresh exact raw-input -> accepted serial producer -> pinned bounded adapter.

The public verifier RECOMPUTES the deterministic arithmetic on separately supplied
original input. Digests never substitute for semantic equality. Trusted Python,
standard library, this source/dependencies, no concurrent input mutation and no
interpreter tampering are the program model; this is not remote attestation.
"""
from dataclasses import dataclass, asdict
from hashlib import sha256
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
import json
import sys
import policy

MAX_P = 4096
MAX_OPERATIONS = 4_000_000
MAX_WORKING_BITS = 100_000
PINS = {
    'compact_window': 'e29741e71c276c156d708f1d9dce6d60ff9d3d2c34a6045b03630c46506dac59',
    'buckets': 'df3937a632217a8a1342545b803169ff8da062117b3837796386509b64f650d1',
    'paid_source': '5cd35d6b3dc1dd6b077db3f1b957cbf4794479aa1b0e592008edf83fa5216d2b',
}


class Failure(ValueError):
    pass


class Meter:
    """Paid integer arithmetic + generous elementary-control/storage envelope.

    Limits are implementation resource restrictions. Exceeding one never emits
    a successful numerical certificate. Work units are a schoolbook bit model,
    not Python instructions, wall clock, RSS, or a hardware guarantee.
    """
    def __init__(self):
        self.events = {}; self.count = self.work = self.produced = self.slots = 0
        self.width = self.stored_width = self.product_width = 1
    def event(self, key, n=1):
        self.events[key] = self.events.get(key, 0) + n
    def record(self, name, args, out):
        sizes = [max(1, abs(x).bit_length()) for x in (*args, out)]
        self.width = max(self.width, *sizes)
        self.count += 1; self.event(name)
        if self.count > MAX_OPERATIONS or self.width > MAX_WORKING_BITS:
            raise Failure('RESOURCE_LIMIT: metered integer operations/width')
        self.work += 128 * (sum(sizes) + 8) ** 2
        self.produced += sizes[-1] + 1
        return out
    def add(self,a,b): return self.record('add',(a,b),a+b)
    def sub(self,a,b): return self.record('subtract',(a,b),a-b)
    def mul(self,a,b): return self.record('multiply',(a,b),a*b)
    def div(self,a,b): return self.record('floor_divide',(a,b),a//b)
    def ceildiv(self,a,b): return -self.div(-a,b)
    def shift(self,n):
        if not 0 <= n <= MAX_WORKING_BITS: raise Failure('RESOURCE_LIMIT: shift')
        return self.record('binary_power',(n,),1<<n)
    def mod(self,a,b): return self.record('modulo',(a,b),a%b)
    def alloc(self,n): self.slots += n; self.event('allocated_slots',n)
    def snapshot(self):
        events = self.count + self.slots + sum(self.events.values()) + 1024
        width = self.width + events.bit_length() + 16
        control = 4096 * events * width ** 2
        return dict(events=dict(sorted(self.events.items())), integer_operations=self.count,
                    arithmetic_bit_work_upper=self.work, control_bit_work_upper=control,
                    producer_bit_work_upper=self.work+control,
                    cumulative_produced_integer_bits=self.produced,
                    cumulative_storage_upper_bits=self.produced+4096*events*width,
                    max_working_integer_bits=self.width, max_stored_grid_bits=self.stored_width,
                    max_product_accumulator_bits=self.product_width,
                    allocated_slots=self.slots)


def nearest(n,d,M):
    """Signed round-to-nearest, ties to even, for integer numerator n / d>0."""
    a=M.div(n,d); remainder=M.sub(n,M.mul(a,d)); twice=M.mul(2,remainder)
    M.event('nearest_even')
    return M.add(a,1) if twice>d or (twice==d and a%2) else a


class Roots:
    """Finite outward integer intervals for intended exp(pi*i*r/N).

    Machin pi plus Taylor of sin/cos of the enclosed positive angle. Every
    operation is outward-rounded. The final exact squared endpoint-radius test
    is the admission criterion, so no approximate root equation is relied on.
    """
    def __init__(self,n,p,M):
        self.n,self.p,self.M=n,p,M
        self.K=p+32+2*policy.ceil_log2(p+64)
        self.S=M.shift(self.K); self.u=M.shift(self.K-p)
        self.terms=p+32; self.degree=p+64
        def atan(q):
            lo=hi=0; qp=q; q2=M.mul(q,q)
            for j in range(self.terms):
                den=M.mul(2*j+1,qp)
                a=M.div(self.S,den); b=M.ceildiv(self.S,den)
                if j%2: lo=M.sub(lo,b); hi=M.sub(hi,a)
                else: lo=M.add(lo,a); hi=M.add(hi,b)
                qp=M.mul(qp,q2); M.event('atan_term')
            tail=M.ceildiv(self.S,M.mul(2*self.terms+1,qp))
            if self.terms%2: lo=M.sub(lo,tail)
            else: hi=M.add(hi,tail)
            return lo,hi
        alo,ahi=atan(5); blo,bhi=atan(239)
        self.pi=(M.sub(M.mul(16,alo),M.mul(4,bhi)),M.sub(M.mul(16,ahi),M.mul(4,blo)))
        if not 3*self.S<self.pi[0]<=self.pi[1]<4*self.S:
            raise Failure('ROOT_CERTIFICATE: Machin interval')
        factorial=1
        for j in range(2,self.degree+2): factorial=M.mul(factorial,j)
        self.tail=M.ceildiv(M.shift(self.K+3*(self.degree+1)),factorial)
        self.table=[]; self.certificates=[]; M.alloc(2*n)
        for r in range(2*n):
            value,certificate=self.make(r); self.table.append(value); self.certificates.append(certificate)
        self.table=tuple(self.table); self.certificates=tuple(self.certificates)
    def make(self,r):
        M,S=self.M,self.S
        if (2*r)%self.n==0:
            axis=((2*r)//self.n)%4
            unit=M.shift(self.p)
            z=((unit,0),(0,unit),(-unit,0),(0,-unit))[axis]
            return z,(r,'exact_quadrant')
        lo=M.div(M.mul(r,self.pi[0]),self.n)
        hi=M.ceildiv(M.mul(r,self.pi[1]),self.n)
        if not 0<=lo<=hi<8*S: raise Failure('ROOT_CERTIFICATE: angle interval')
        tlo=thi=S; rlo=rhi=ilo=ihi=0
        for k in range(self.degree+1):
            if k%4==0: rlo=M.add(rlo,tlo); rhi=M.add(rhi,thi)
            elif k%4==1: ilo=M.add(ilo,tlo); ihi=M.add(ihi,thi)
            elif k%4==2: rlo=M.sub(rlo,thi); rhi=M.sub(rhi,tlo)
            else: ilo=M.sub(ilo,thi); ihi=M.sub(ihi,tlo)
            if k<self.degree:
                den=M.mul(S,k+1)
                tlo=M.div(M.mul(tlo,lo),den)
                thi=M.ceildiv(M.mul(thi,hi),den)
            M.event('root_taylor_term')
        rlo=M.sub(rlo,self.tail); rhi=M.add(rhi,self.tail)
        ilo=M.sub(ilo,self.tail); ihi=M.add(ihi,self.tail)
        zr=nearest(M.add(rlo,rhi),2*self.u,M)
        zi=nearest(M.add(ilo,ihi),2*self.u,M)
        er=max(abs(M.sub(M.mul(zr,self.u),rlo)),abs(M.sub(M.mul(zr,self.u),rhi)))
        ei=max(abs(M.sub(M.mul(zi,self.u),ilo)),abs(M.sub(M.mul(zi,self.u),ihi)))
        if M.add(M.mul(er,er),M.mul(ei,ei))>M.mul(self.u,self.u):
            raise Failure('ROOT_CERTIFICATE: intended complex root error exceeds 2^-p')
        return (zr,zi),(r,self.K,rlo,rhi,ilo,ihi,er,ei)
    def __call__(self,r):
        self.M.event('root_table_lookup')
        return self.table[self.M.mod(r,2*self.n)]


def inverse_sqrt(n,p,M):
    K=p+16; target=M.div(M.shift(2*K),n)
    # Finite greedy integer square root, not an uncharged special-function call.
    root=0
    for bit in range((target.bit_length()+1)//2-1,-1,-1):
        trial=M.add(root,M.shift(bit))
        if M.mul(trial,trial)<=target: root=trial
        M.event('sqrt_bit')
    top=root if M.mul(M.mul(root,root),n)==M.shift(2*K) else M.add(root,1)
    guard=M.shift(K-p); rho=nearest(M.add(root,top),2*guard,M)
    if max(abs(M.sub(M.mul(rho,guard),root)),abs(M.sub(M.mul(rho,guard),top)))>guard:
        raise Failure('ROOT_CERTIFICATE: inverse square root')
    return rho,(K,root,top)


class Fixed:
    def __init__(self,p,I,M): self.p,self.I,self.M,self.unit=p,I,M,M.shift(p)
    def stored(self,z):
        for c in z:
            width=abs(c).bit_length(); self.M.stored_width=max(self.M.stored_width,width)
            if width>self.p+self.I: raise Failure('RANGE: stored grid exceeds accepted budget')
        self.M.alloc(2); return z
    def add(self,z,w): return self.stored((self.M.add(z[0],w[0]),self.M.add(z[1],w[1])))
    def sub(self,z,w): return self.stored((self.M.sub(z[0],w[0]),self.M.sub(z[1],w[1])))
    def neg(self,z): return self.sub((0,0),z)
    def conj(self,z): return (z[0],self.M.sub(0,z[1]))
    def mul(self,z,w):
        M=self.M
        a=M.sub(M.mul(z[0],w[0]),M.mul(z[1],w[1]))
        b=M.add(M.mul(z[0],w[1]),M.mul(z[1],w[0]))
        for c in (a,b):
            bits=abs(c).bit_length(); M.product_width=max(M.product_width,bits)
            if bits>2*(self.p+self.I)+3: raise Failure('RANGE: exact product accumulator')
        return self.stored((nearest(a,self.unit,M),nearest(b,self.unit,M)))
    def half(self,z): return self.stored((nearest(z[0],2,self.M),nearest(z[1],2,self.M)))
    def total(self,values):
        out=(0,0)
        for z in values: out=self.add(out,z)
        return out


def serial(raw,state,plan,M):
    n,b=state['N'],state['B']; a,beta=state['a'],state['beta']; p=plan['p']
    starts,lengths=state['starts'],state['lengths']; h=state['h']; W=plan['W']
    R=Roots(n,p,M); A=Fixed(p,plan['plan']['I'],M)
    shift=M.shift(p-W)
    x=tuple(A.stored((M.mul(re,shift),M.mul(im,shift))) for re,im in zip(raw['real'],raw['imag']))
    def phase(s,t): return a*t*(t-1)+2*(a*s+beta)*t+h*t
    d=tuple(A.total(A.mul(R(phase(s,t)),x[s+t]) for t in range(length))
            for s,length in zip(starts,lengths)); M.event('compression_blocks',b)
    c=tuple(R(-phase(s,length)) for s,length in zip(starts,lengths))
    w=tuple(A.sub(d[j],A.mul(c[j-1],d[j-1])) for j in range(b)); M.event('boundary_blocks',b)
    coeff=[(A.unit,0)]
    for s in starts:
        old=coeff; coeff=old+[(0,0)]; M.alloc(len(coeff)); lam=R(-2*s)
        for j in range(1,len(coeff)): coeff[j]=A.sub(coeff[j],A.mul(lam,old[j-1]))
    seq=[A.total(A.mul(ww,R(-2*s*k)) for s,ww in zip(starts,w)) for k in range(b)]
    for k in range(b,n): seq.append(A.neg(A.total(A.mul(coeff[j],seq[k-j]) for j in range(1,b+1))))
    rho,rho_certificate=inverse_sqrt(n,p,M)
    f=tuple(A.mul(z,(rho,0)) for z in seq)
    gauge=tuple(R(a*j*(j-1)+2*beta*j+h*j) for j in range(n))
    u=tuple(A.mul(A.conj(gauge[j]),f[(a*j)%n]) for j in range(n))
    v0=A.half(A.total(u)); prefix=(0,0); out=[(0,0)]*n; M.alloc(n)
    for j in range(n):
        out[(a*j)%n]=A.mul(gauge[j],A.sub(v0,prefix)); prefix=A.add(prefix,u[j])
    M.event('final_output_cells',n)
    return tuple(out),dict(roots=R.certificates,rho=rho_certificate,
                          d=d,w=w,coefficients=tuple(coeff),s=tuple(seq),f=f,
                          gauge=gauge,u=u,v0=v0)


def load_adapter():
    """Load text-reviewed, exact pinned files; never follow an arbitrary path."""
    directory=Path(__file__).resolve().parent/'vendor'; read_bytes=0
    for name,pin in PINS.items():
        path=directory/(name+'.py'); data=path.read_bytes(); read_bytes+=len(data)
        if sha256(data).hexdigest()!=pin: raise Failure('DEPENDENCY_PIN: '+name)
        existing=sys.modules.get(name)
        if existing is not None:
            if getattr(existing,'__alg034_checked_pin__',None)!=pin:
                raise Failure('DEPENDENCY_IDENTITY: conflicting '+name)
            continue
        spec=spec_from_file_location(name,path); mod=module_from_spec(spec)
        sys.modules[name]=mod
        try: spec.loader.exec_module(mod)
        except Exception:
            del sys.modules[name]; raise
        mod.__alg034_checked_pin__=pin
    return sys.modules['paid_source'],read_bytes


def binary_digest(payload):
    h=sha256(b'ALG034-OUTPUT-v1\0')
    n,kappa,rows=payload
    for z in (n,kappa,*(v for row in rows for v in row)):
        size=(abs(z).bit_length()+7)//8
        h.update(bytes([int(z<0)])+size.to_bytes(4,'big')+abs(z).to_bytes(size,'big'))
    return h.hexdigest()


@dataclass(frozen=True)
class Run:
    status: str
    input_context: bytes
    policy_bytes: bytes
    payload: object
    adapter: object
    trace_bytes: bytes
    ledger_bytes: bytes
    @property
    def policy(self): return json.loads(self.policy_bytes)
    @property
    def ledger(self): return json.loads(self.ledger_bytes)
    def packet(self):
        return {'schema':'ALG034_SEMANTIC_PACKET_V1','context':json.loads(self.input_context),
                'policy':self.policy,'payload':None if self.payload is None else
                {'N':self.payload[0],'kappa':self.payload[1],'rows':[list(x) for x in self.payload[2]]}}


def policy_cost_envelope(raw,state,plan):
    """Conservative schoolbook upper envelope; details in PROOF.md.

    Entire prepass/setup/input/plan/serialization is charged on EVERY call,
    even if policy's deterministic cyclotomic cache happens to be warm.
    """
    n,b=state['N'],state['B']; L=4*n; W=max(1,plan['W'])
    V=max(abs(x).bit_length() for x in [raw['F'],plan['t'],plan['q'],plan['p'] or 0])+32
    T0=L*L+3*L+4; S=W+T0+4*n+32
    # 4 MiB canonical byte/tree traversal is conservatively included.
    work=2**20*((L+1)**4*(T0+1)**2+(n+b*(L+1)**2)*(S+V+1)**2+(4*1024*1024)*(8192+V)**2)
    storage=2**20*((L+1)**3+(n+b*(L+1))*S+4*1024*1024*8+V)
    return work,storage


def execute(raw,state,t=16,q=None,p=None,adapt=True,include_trace=False):
    """Validate/copy exact caller context, execute, optionally adapt actual output.

    q defaults to the legacy Q16 tolerance on dyadic lengths, otherwise ceil(log2 N).
    Original/projected zero return before normalization. Out-of-adapter-domain
    nonzero lengths still have a numerically certified producer payload.
    """
    s=policy.validate_state(state); n=s['N']
    raw=policy.vectors(raw,'F',n,policy.MAX_RAW_BITS,'raw')
    state={k:s[k] for k in ('N','B','a','beta')}
    if type(adapt) is not bool or type(include_trace) is not bool: raise Failure('GRAMMAR: boolean option')
    if q is None: q=16*(n.bit_length()-1)+16 if n>=4 and not n&(n-1) else policy.ceil_log2(n)
    plan=policy.derive_policy(raw,state,t,q,p)
    context=policy.canonical_bytes(dict(raw=raw,state=state,t=t,q=q,p=plan['p']))
    pcost,pstorage=policy_cost_envelope(raw,s,plan)
    if plan['outcome']!='NONZERO_PLAN':
        return Run(plan['outcome'],context,policy.canonical_bytes(plan),None,None,b'{}',
                   policy.canonical_bytes(dict(policy_bit_work_upper=pcost,policy_storage_upper_bits=pstorage,
                                               no_producer_or_adapter_call=True)))
    if plan['p']>MAX_P: raise Failure('RESOURCE_LIMIT: selected p exceeds 4096')
    M=Meter(); rows,trace=serial(raw,s,plan,M)
    if not any(c for row in rows for c in row): raise Failure('INVARIANT: accepted nonzero plan produced zero')
    payload=(n,plan['plan']['kappa'],rows)
    adapter=None; status='NUMERICALLY_CERTIFIED_PRODUCER'; dep_bytes=0
    if adapt:
        if n<4 or n&(n-1): status='NUMERICALLY_CERTIFIED_ADAPTER_LENGTH_OUT_OF_DOMAIN'
        else:
            legacy,dep_bytes=load_adapter()
            cert=(legacy.PRODUCER,legacy.TARGET,legacy.PHASES,legacy.ORDER,legacy.PREMISE,
                  plan['raw_input_sha256'],binary_digest(payload),n,s['B'],s['a'],s['beta'],
                  raw['F'],plan['W'],plan['p'],t,plan['plan']['C'],0)
            # Actual widths and legacy metadata grammar are checked by the adapter;
            # p+I is only a sufficient width check, never an overwidth conclusion.
            try: adapter=legacy.adapt(payload,cert)
            except legacy.Rejection as error:
                raise Failure('ADAPTER_REJECTION: '+error.code+': '+error.path) from error
            if adapter.status!='VALID_SOURCE': raise Failure('INVARIANT: nonzero source did not adapt')
            status='CERTIFIED_SOURCE_TARGET_BUDGET_PASS' if adapter.target_budget=='TARGET_BUDGET_PASS' else 'CERTIFIED_SOURCE_TARGET_BUDGET_NOT_ESTABLISHED'
    trace_bytes=json.dumps(trace if include_trace else {},sort_keys=True,separators=(',',':')).encode()
    ledger=M.snapshot()
    # Charge serialization, actual emitted trace bytes and dependency parsing/
    # hashing conservatively. The ledger itself gets a bounded 64 KiB reserve.
    serialization_bytes=len(trace_bytes)+len(context)+len(policy.canonical_bytes(plan))+65536
    serialization_work=128*(serialization_bytes+1)*(ledger['max_working_integer_bits']+128)**2
    dependency_work=2**20*(dep_bytes+1)**2 if dep_bytes else 0
    ledger.update(policy_bit_work_upper=pcost,policy_storage_upper_bits=pstorage,
                  dependency_read_bytes=dep_bytes,dependency_loading_bit_work_upper=dependency_work,
                  serialization_bytes_upper=serialization_bytes,serialization_bit_work_upper=serialization_work,
                  semantic_verifier_runs=0)
    if adapter is not None:
        ledger['adapter_receipt']=asdict(adapter.receipt)
        ledger['total_bit_work_upper']=pcost+ledger['producer_bit_work_upper']+adapter.receipt.total_bit_work_upper+dependency_work+serialization_work
        ledger['total_cumulative_storage_upper_bits']=pstorage+ledger['cumulative_storage_upper_bits']+adapter.receipt.cumulative_storage_upper_bits+8*(dep_bytes+serialization_bytes)
    else:
        ledger['total_bit_work_upper']=pcost+ledger['producer_bit_work_upper']+serialization_work
        ledger['total_cumulative_storage_upper_bits']=pstorage+ledger['cumulative_storage_upper_bits']+8*serialization_bytes
    return Run(status,context,policy.canonical_bytes(plan),payload,adapter,
               trace_bytes,
               json.dumps(ledger,sort_keys=True,separators=(',',':')).encode())


def verify(raw,state,t,q,packet,p=None):
    """Paid semantic verification, not an attestation/receipt parser.

    Exact recomputation rejects any different payload even if every attacker-
    editable commitment is rehashed. Supply independently retained raw context.
    The returned flag is computed by this function, never read from the packet.
    """
    policy.keys(packet,{'schema','context','policy','payload'},'semantic packet')
    # Bound all untrusted objects before running the more expensive computation.
    actual=policy.canonical_bytes(packet)
    run=execute(raw,state,t,q,p,adapt=False)
    if actual!=policy.canonical_bytes(run.packet()): raise Failure('SEMANTIC_MISMATCH: recomputation differs')
    return dict(status='SEMANTICALLY_VERIFIED',numerical_payload_verified=True,
                bound_to_supplied_original_input=True,external_origin_authenticated=False,
                original_execution_history_attested=False,recomputation_bit_work_upper=run.ledger.get('total_bit_work_upper',run.ledger['policy_bit_work_upper'])+2*run.ledger['policy_bit_work_upper'],
                recomputation_cumulative_storage_upper_bits=run.ledger.get('total_cumulative_storage_upper_bits',run.ledger['policy_storage_upper_bits'])+2*run.ledger['policy_storage_upper_bits'],
                verification_serialization_paid_by_two_extra_policy_envelopes=True)
