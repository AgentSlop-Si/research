"""Exact structured ALG-034 target producer, with no length-sized allocation.

This is a NEW backend. It proves its exact target directly; it does not claim
to execute, or to reproduce the rounded output of, the serial backend.
Only canonical dyadic inputs supported on quarter-axis indices and B_A=N are
accepted. The target is U_negative(P x), where singleton blocks imply P x=x.
All large precision-grid powers are represented by explicitly typed exponents.
"""
from dataclasses import dataclass
from hashlib import sha256
import json

SCHEMA = 'ALG034_SPARSE_DYADIC_V1'
BACKEND = 'ALG034-EXACT-AXIS-SUPPORT-v1'
PACKET = 'ALG034_EXACT_STRUCTURED_PACKET_V1'
TARGET = 'U_negative(P_balanced_longer_first(x))'
MAX_M = 64
MAX_RAW_BITS = 1024
MAX_META_BITS = 128
MAX_JSON_BYTES = 65536


class Failure(ValueError):
    pass


class Meter:
    """Conservative paid schoolbook model, not Python time or peak RSS."""
    def __init__(self):
        self.count = self.work = self.produced = self.slots = self.bytecount = 0
        self.width = 1
        self.events = {}
    def event(self, name, amount=1):
        self.events[name] = self.events.get(name, 0) + amount
    def record(self, name, args, value):
        sizes = [max(1, abs(v).bit_length()) for v in (*args, value)]
        self.width = max(self.width, *sizes)
        self.count += 1
        self.work += 128 * (sum(sizes) + 8) ** 2
        self.produced += sizes[-1] + 1
        self.event(name)
        if self.width > 4096 or self.count > 20000:
            raise Failure('RESOURCE_LIMIT: integer arithmetic envelope')
        return value
    def add(self, a, b): return self.record('add', (a,b), a+b)
    def sub(self, a, b): return self.record('subtract', (a,b), a-b)
    def mul(self, a, b): return self.record('multiply', (a,b), a*b)
    def div(self, a, b): return self.record('floor_divide', (a,b), a//b)
    def mod(self, a, b): return self.record('modulo', (a,b), a%b)
    def bits(self, a): return self.record('bit_length', (a,), abs(a).bit_length())
    def power2(self, a):
        # Physical powers are only length metadata or tiny exact root units.
        if type(a) is not int or not 0 <= a <= MAX_M:
            raise Failure('RESOURCE_LIMIT: forbidden materialized power')
        return self.record('binary_power', (a,), 1 << a)
    def alloc(self, n):
        self.slots += n
        self.event('allocated_slots', n)
    def bytes(self, n):
        self.bytecount += n
        self.event('serialized_bytes', n)
    def snapshot(self):
        events = self.count + self.slots + self.bytecount + 1024
        width = self.width + events.bit_length() + 32
        controls = 4096 * events * width ** 2
        return {
            'events': dict(sorted(self.events.items())),
            'integer_operations': self.count,
            'max_metered_data_integer_bits': self.width,
            'arithmetic_bit_work_upper': self.work,
            'control_serialization_bit_work_upper': controls,
            'total_bit_work_upper': self.work + controls,
            'cumulative_storage_upper_bits': self.produced + 4096*events*width,
            'allocated_slots': self.slots,
            'serialized_bytes_charged': self.bytecount,
            'model': 'schoolbook binary arithmetic and cumulative logical storage; not CPU/RSS',
        }


def exact_int(v, name, L, bits=MAX_META_BITS):
    if type(v) is not int:
        raise Failure('GRAMMAR: '+name+' must be an exact built-in integer')
    width = abs(v).bit_length()
    if width > bits:
        raise Failure('RESOURCE_LIMIT: '+name+' width')
    return L.record('input_integer', (), v)


def keys(obj, required, name):
    if (type(obj) is not dict or len(obj) != len(required)
            or any(type(k) is not str for k in obj)
            or set(obj) != set(required)):
        raise Failure('GRAMMAR: '+name+' keys')


def canonical(obj, L):
    remaining = [512]
    budget = [MAX_JSON_BYTES]
    def check(v, depth=0):
        remaining[0] -= 1
        if depth > 16 or remaining[0] < 0:
            raise Failure('RESOURCE_LIMIT: bounded serialization tree')
        kind = type(v)
        if v is None or kind is bool:
            budget[0] -= 5
        elif kind is int:
            exact_int(v, 'serialized integer', L, 4096)
            budget[0] -= abs(v).bit_length()*30103//100000+2
        elif kind is str:
            budget[0] -= 2+12*len(v)
        elif kind is list:
            if len(v) > 128:
                raise Failure('RESOURCE_LIMIT: serialization list')
            budget[0] -= 2+len(v)
            for x in v: check(x,depth+1)
        elif kind is dict:
            if len(v) > 64:
                raise Failure('RESOURCE_LIMIT: serialization dict')
            budget[0] -= 2+2*len(v)
            for k,x in v.items():
                if type(k) is not str: raise Failure('GRAMMAR: serialization keys')
                check(k,depth+1); check(x,depth+1)
        else:
            raise Failure('GRAMMAR: unsupported serialized type')
        if budget[0] < 0:
            raise Failure('RESOURCE_LIMIT: serialization byte budget')
    check(obj)
    result = json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode('ascii')
    if len(result) > MAX_JSON_BYTES:
        raise Failure('RESOURCE_LIMIT: serialized byte length')
    L.bytes(len(result)); L.alloc(len(result))
    return result


def validate(raw, state, L):
    keys(raw, {'schema','N','F','entries'}, 'raw')
    if type(raw['schema']) is not str or raw['schema'] != SCHEMA:
        raise Failure('GRAMMAR: raw schema')
    keys(state, {'N','B','a','beta'}, 'state')
    s = {k:exact_int(state[k],'state.'+k,L) for k in ('N','B','a','beta')}
    n = exact_int(raw['N'],'raw.N',L)
    F = exact_int(raw['F'],'raw.F',L)
    if n < 4 or n & (n-1):
        raise Failure('DOMAIN: dyadic N >= 4 required')
    m = L.sub(L.bits(n),1)
    if m > MAX_M:
        raise Failure('RESOURCE_LIMIT: log2 N exceeds 64')
    if m % 2:
        raise Failure('UNSUPPORTED_STRUCTURE: N must be a square power of two')
    if s['N'] != n or s['B'] != n:
        raise Failure('UNSUPPORTED_STRUCTURE: singleton blocks B_A=N required')
    if not 0 < s['a'] < n or s['a'] % 2 != 1 or not 0 <= s['beta'] < n:
        raise Failure('DOMAIN: invalid ALG-034 phase state')
    entries = raw['entries']
    if type(entries) is not list:
        raise Failure('GRAMMAR: raw.entries must be an exact list')
    if len(entries) > 4:
        raise Failure('UNSUPPORTED_STRUCTURE: at most four quarter-axis entries')
    quarter = L.div(n,4)
    copied = []
    prev = -1
    odd = False
    W = 0
    for pos, row in enumerate(entries):
        if type(row) is not list or len(row) != 3:
            raise Failure('GRAMMAR: sparse entry must be [index,real,imag]')
        index = exact_int(row[0],'entry.index',L)
        real = exact_int(row[1],'entry.real',L,MAX_RAW_BITS)
        imag = exact_int(row[2],'entry.imag',L,MAX_RAW_BITS)
        if not prev < index < n or index < 0:
            raise Failure('GRAMMAR: sparse indices must be strictly sorted residues')
        if L.mod(index,quarter):
            raise Failure('UNSUPPORTED_STRUCTURE: non-quarter-axis input support')
        if real == 0 and imag == 0:
            raise Failure('GRAMMAR: zero sparse entries are forbidden')
        odd = odd or bool(real%2 or imag%2)
        W = max(W,L.bits(real),L.bits(imag))
        copied.append((index,real,imag)); prev=index
        L.alloc(4)
    if not entries and F != 0:
        raise Failure('GRAMMAR: zero input has canonical F=0')
    if entries and not odd:
        raise Failure('GRAMMAR: remove common powers of two from sparse numerators')
    copied = tuple(copied); L.alloc(len(copied))
    clean = {'schema':SCHEMA,'N':n,'F':F,'entries':[list(row) for row in copied]}
    return clean,s,m,W,copied


@dataclass(frozen=True)
class ExactRun:
    status: str
    N: int
    period: tuple
    value_exponent: int
    pgrid_shift: object
    kappa: object
    context_bytes: bytes
    policy_bytes: bytes
    payload_bytes: bytes
    ledger_bytes: bytes
    @property
    def context(self): return json.loads(self.context_bytes)
    @property
    def policy(self): return json.loads(self.policy_bytes)
    @property
    def ledger(self): return json.loads(self.ledger_bytes)
    def packet(self):
        # Exports are additionally charged by EXPORT_BIT_WORK_BOUND below.
        return {'schema':PACKET,'context':self.context,'policy':self.policy,
                'payload':json.loads(self.payload_bytes)}


# Fixed conservative envelope for one bounded export (not execute/replay).
EXPORT_BIT_WORK_BOUND = 2**70
EXPORT_STORAGE_BITS_BOUND = 2**42


def execute(raw,state,t=16,q=None,p=None):
    """Produce exact U P x on the admitted structured family, or reject.

    Output is a period-four exact common-grid sequence. Formal p-grid integers
    are represented by `period[j%4] * 2**pgrid_shift`, never materialized.
    The precision policy is the accepted all-length formula specialized by
    proof to singleton blocks, not a scan or cyclotomic table approximation.
    """
    L=Meter()
    clean,s,m,W,entries=validate(raw,state,L)
    n,F=clean['N'],clean['F']
    t=exact_int(t,'t',L)
    q=L.add(L.mul(16,m),16) if q is None else exact_int(q,'q',L)
    if t<0 or q<m: raise Failure('DOMAIN: t>=0 and q>=log2 N required')
    if p is not None:
        p=exact_int(p,'p',L)
        if p<0: raise Failure('DOMAIN: p must be nonnegative')
    raw_bytes=canonical(clean,L)
    raw_digest=sha256(b'ALG034:EXACT-STRUCTURED:RAW:v1\0'+raw_bytes).hexdigest()
    L.bytes(len(raw_bytes)+32)
    common={'backend':BACKEND,'target':TARGET,'W':W,'t':t,'q':q,
            'raw_input_sha256':raw_digest,'exact_error':{'coefficient':0,'scale':0},
            'bit_equivalent_to_rounded_serial':False}
    if not entries:
        if p is not None: raise Failure('DOMAIN: zero input must not declare precision')
        period=((0,0),)*4
        value_exponent=0; shift=kappa=None
        policy={**common,'outcome':'EXACT_INPUT_ZERO','p':None,'plan':None}
        payload=None
        status='EXACT_INPUT_ZERO'
    else:
        # At B=N, Phi_(2N)=X^N+1 and each singleton polynomial is
        # real + imag*X^(N/2), already reduced and nonzero.
        mass,index=min((L.add(abs(re),abs(im)),j) for j,re,im in entries)
        K=L.bits(L.sub(mass,1))
        G=L.add(W,L.mul(L.sub(n,1),K))
        c=L.add(n,L.add(L.mul(3,m),6))
        p_min=max(W,L.add(L.add(c,t),1),L.add(L.add(L.add(c,q),G),2))
        if p is None: p=p_min
        if p<p_min: raise Failure('PRECISION: p below accepted one-shot policy')
        # The exponent integer must itself fit the metadata resource cap.
        exact_int(p,'selected p',L)
        I=L.add(n,L.add(L.mul(2,m),10))
        shift=L.sub(L.sub(p,W),L.div(m,2))
        if shift<0: raise Failure('INVARIANT: accepted policy did not align exact grid')
        kappa=L.sub(L.sub(W,F),p)
        value_exponent=L.sub(-F,L.div(m,2))
        quarter=L.div(n,4)
        # Exact fourth roots exp(-2*pi*i*u/4). No approximate phases.
        roots=((1,0),(0,-1),(-1,0),(0,1))
        out=[]
        for frequency_mod4 in range(4):
            real=imag=0
            for j,re,im in entries:
                phase=L.mod(L.mul(L.div(j,quarter),frequency_mod4),4)
                ar,ai=roots[phase]
                real=L.add(real,L.sub(L.mul(re,ar),L.mul(im,ai)))
                imag=L.add(imag,L.add(L.mul(re,ai),L.mul(im,ar)))
            out.append((real,imag)); L.alloc(3)
        period=tuple(out); L.alloc(4)
        if not any(x for row in period for x in row):
            raise Failure('INVARIANT: exact invertible transform returned zero')
        formal_width=max(L.bits(x) for row in period for x in row)+shift
        if formal_width>p+I:
            raise Failure('INVARIANT: exact output exceeds accepted stored range')
        policy={**common,'outcome':'NONZERO_EXACT_PLAN','p':p,'plan':{
            'L':L.mul(2,n),'D':n,'selected_block':index,'A':mass,'K':K,'G':G,
            'H':1,'C_factor':{'coefficient':1,'scale':c},'c':c,
            'p_min':p_min,'I':I,'kappa':kappa,
            'accepted_serial_radius_factor':{'coefficient':1,'scale':L.add(c,kappa)},
            'mu_scale':L.sub(-F,L.mul(L.sub(n,1),K)),
            'formal_p_grid_numerator_bits_max':formal_width}}
        payload={'schema':'ALG034_EXACT_PERIOD_FOUR_V1','N':n,
                 'period':[list(row) for row in period],
                 'value_exponent':value_exponent,
                 'formal_p_grid':{'common_left_shift':shift,'kappa':kappa},
                 'target':TARGET,'exact_error':{'coefficient':0,'scale':0}}
        status='EXACT_TARGET_CERTIFIED'
    context={'raw':clean,'state':s,'t':t,'q':q,'p':p}
    context_bytes=canonical(context,L)
    policy_bytes=canonical(policy,L)
    payload_bytes=canonical(payload,L)
    # Pay a fixed ledger encoding reserve, including its own bounded counters.
    L.bytes(16384); L.alloc(16384)
    ledger=L.snapshot()
    ledger['additional_packet_export_bit_work_upper']=EXPORT_BIT_WORK_BOUND
    ledger['additional_packet_export_storage_upper_bits']=EXPORT_STORAGE_BITS_BOUND
    ledger_bytes=json.dumps(ledger,sort_keys=True,separators=(',',':')).encode('ascii')
    if len(ledger_bytes)>16384: raise Failure('RESOURCE_LIMIT: ledger reserve')
    return ExactRun(status,n,period,value_exponent,shift,kappa,
                    context_bytes,policy_bytes,payload_bytes,ledger_bytes)


def verify(raw,state,t,q,packet,p=None):
    """Paid full semantic recomputation against independently retained context."""
    L=Meter()
    keys(packet,{'schema','context','policy','payload'},'semantic packet')
    actual=canonical(packet,L)
    run=execute(raw,state,t,q,p)
    expected=canonical(run.packet(),L)
    if actual!=expected: raise Failure('SEMANTIC_MISMATCH: fresh exact recomputation differs')
    ledger=L.snapshot()
    return {'status':'SEMANTICALLY_VERIFIED','bound_to_supplied_original_input':True,
            'external_origin_authenticated':False,'historical_execution_attested':False,
            'exact_target_certified':run.status=='EXACT_TARGET_CERTIFIED',
            'total_bit_work_upper':run.ledger['total_bit_work_upper']+ledger['total_bit_work_upper']+EXPORT_BIT_WORK_BOUND,
            'cumulative_storage_upper_bits':run.ledger['cumulative_storage_upper_bits']+ledger['cumulative_storage_upper_bits']+EXPORT_STORAGE_BITS_BOUND}


def fixture():
    n=1<<28
    return ({'schema':SCHEMA,'N':n,'F':0,'entries':[[0,1,0]]},
            {'N':n,'B':n,'a':1,'beta':0})
