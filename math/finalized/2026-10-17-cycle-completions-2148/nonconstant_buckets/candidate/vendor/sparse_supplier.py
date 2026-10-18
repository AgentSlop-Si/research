"""Fresh bounded sparse-original ALG-034 ideal-target supplier.

B_A=N is retained. Sparse locations are arbitrary; every dyadic N=2**m,
2<=m<=64 is allowed. Exact modal descriptors and separately paid certified
point queries do NOT claim rounded-serial equivalence or a free full DFT.
"""
from dataclasses import dataclass
from hashlib import sha256
from math import isqrt
import json

SCHEMA = 'ALG034_SPARSE_DYADIC_V1'
BACKEND = 'ALG034-SPARSE-MODAL-SUPPLIER-v1'
PACKET = 'ALG034_SPARSE_SUPPLIER_PACKET_V1'
MAX_SUPPORT = 64
MAX_RAW_BITS = 1024
MAX_META_BITS = 128
MAX_M = 64
MAX_QUERY_BITS = 4096
MAX_DATA_BITS = 12288
MAX_OPERATIONS = 1000000
MAX_JSON_BYTES = 2 * 1024 * 1024
EXPORT_BIT_WORK_BOUND = 1 << 100
EXPORT_STORAGE_BITS_BOUND = 1 << 50

class Failure(ValueError):
    pass

class Meter:
    """Paid binary arithmetic envelope; not machine time or peak RSS."""
    def __init__(self):
        self.operations = self.work = self.produced = self.bytes = self.slots = 0
        self.width = 1
        self.events = {}
    def record(self, name, args, values):
        if type(values) is int:
            result = values; vals = (values,)
        else:
            result = values; vals = tuple(values)
        widths = [max(1, abs(x).bit_length()) for x in tuple(args) + vals]
        self.width = max(self.width, *widths)
        self.operations += 1
        if self.width > MAX_DATA_BITS or self.operations > MAX_OPERATIONS:
            raise Failure('RESOURCE_LIMIT: arithmetic envelope')
        # A record contains <=32 elementary operations. This cubic envelope
        # also covers integer square root and conservative bit copying.
        self.work += 4096 * (sum(widths) + 32) ** 3
        self.produced += sum(max(1, abs(x).bit_length()) + 1 for x in vals)
        self.events[name] = self.events.get(name, 0) + 1
        return result
    def physical_power(self, e):
        if type(e) is not int or not 0 <= e <= 6000:
            raise Failure('RESOURCE_LIMIT: physical power')
        return self.record('physical_power', (e,), 1 << e)
    def snapshot(self):
        E = self.operations + self.bytes + self.slots + 4096
        V = self.width + E.bit_length() + 64
        return {'operations': self.operations, 'max_data_integer_bits': self.width,
                'events': dict(sorted(self.events.items())),
                'arithmetic_bit_work_upper': self.work,
                'control_serialization_bit_work_upper': (1 << 16) * E * V**3,
                'total_bit_work_upper': self.work + (1 << 16) * E * V**3,
                'cumulative_storage_upper_bits': self.produced + 4096*E*V,
                'serialized_bytes_charged': self.bytes, 'logical_slots': self.slots,
                'additional_packet_export_bit_work_upper': EXPORT_BIT_WORK_BOUND,
                'additional_packet_export_storage_upper_bits': EXPORT_STORAGE_BITS_BOUND,
                'model': 'conservative binary work/cumulative logical storage; not CPU/RSS'}

def integer(x, name, meter, bits=MAX_META_BITS):
    if type(x) is not int:
        raise Failure('GRAMMAR: '+name+' must be an exact built-in integer')
    if abs(x).bit_length() > bits:
        raise Failure('RESOURCE_LIMIT: '+name+' width')
    return meter.record('input_integer', (), x)

def keys(obj, required, name):
    if type(obj) is not dict or len(obj) != len(required) or any(type(k) is not str for k in obj) or set(obj) != set(required):
        raise Failure('GRAMMAR: '+name+' keys')

def canonical(obj, meter):
    nodes = 0
    budget = MAX_JSON_BYTES
    def walk(v, depth):
        nonlocal nodes, budget
        nodes += 1
        if nodes > 50000 or depth > 16:
            raise Failure('RESOURCE_LIMIT: serialization tree')
        kind = type(v)
        if v is None or kind is bool:
            budget -= 5
        elif kind is int:
            if abs(v).bit_length() > MAX_DATA_BITS:
                raise Failure('RESOURCE_LIMIT: serialized integer')
            budget -= abs(v).bit_length()*30103//100000+3
        elif kind is str:
            if len(v) > 4096:
                raise Failure('RESOURCE_LIMIT: serialized string')
            budget -= 12*len(v)+2
        elif kind is list:
            if len(v) > 256:
                raise Failure('RESOURCE_LIMIT: serialized list')
            budget -= len(v)+2
            for u in v: walk(u, depth+1)
        elif kind is dict:
            if len(v) > 64:
                raise Failure('RESOURCE_LIMIT: serialized dictionary')
            budget -= 2*len(v)+2
            for k,u in v.items():
                if type(k) is not str: raise Failure('GRAMMAR: serialized key')
                walk(k,depth+1); walk(u,depth+1)
        else:
            raise Failure('GRAMMAR: serialized built-in type')
        if budget < 0: raise Failure('RESOURCE_LIMIT: serialized byte budget')
    walk(obj, 0)
    data = json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode('ascii')
    if len(data) > MAX_JSON_BYTES: raise Failure('RESOURCE_LIMIT: serialized bytes')
    meter.bytes += len(data)
    meter.slots += nodes + len(data)
    return data

def ceildiv(a,b):
    return -((-a)//b)

def interval_add(a,b,L):
    return L.record('interval_add', a+b, (a[0]+b[0],a[1]+b[1]))

def interval_neg(a,L):
    return L.record('interval_negate', a, (-a[1],-a[0]))

def interval_mul(a,b,D,L):
    products = (a[0]*b[0],a[0]*b[1],a[1]*b[0],a[1]*b[1])
    # Record products so widths include temporary arithmetic, not just output.
    L.record('interval_products', a+b, products)
    return L.record('interval_multiply_round', products+(D,), (min(products)//D,ceildiv(max(products),D)))

def interval_scale(a,c,L):
    p,q=a[0]*c,a[1]*c
    return L.record('integer_interval_scale', a+(c,), (min(p,q),max(p,q)))

def complex_mul(a,b,D,L):
    ac=interval_mul(a[0],b[0],D,L);bd=interval_mul(a[1],b[1],D,L)
    ad=interval_mul(a[0],b[1],D,L);bc=interval_mul(a[1],b[0],D,L)
    return (interval_add(ac,interval_neg(bd,L),L),interval_add(ad,bc,L))

def sqrt_interval(a,D,L):
    if a[0]<0 or a[1]<a[0]: raise Failure('INVARIANT: square root interval domain')
    low,high=L.record('sqrt_radicands', a+(D,), (a[0]*D,a[1]*D))
    u,v=isqrt(low),isqrt(high)
    if v*v != high: v+=1
    return L.record('integer_square_root_enclosure', (low,high), (u,v))

def root_setup(m,b,L):
    """Outward dyadic enclosures for exp(-2*pi*i / 2**ell), ell=1..m."""
    D=L.physical_power(b)
    roots=[((D,D),(0,0)),((-D,-D),(0,0)),((0,0),(-D,-D))]
    c=(0,0);s=(D,D)
    for ell in range(3,m+1):
        half=L.record('half_angle_argument', c+(D,), ((D+c[0])//2,ceildiv(D+c[1],2)))
        cnew=sqrt_interval(half,D,L)
        if cnew[0]<=0: raise Failure('INVARIANT: positive half-angle cosine')
        # sin(theta/2)=sin(theta)/(2*cos(theta/2)); avoids cancellation.
        nums=L.record('half_angle_sine_numerators', s+(D,), (s[0]*D,s[1]*D))
        snew=L.record('half_angle_sine_division', nums+cnew, (nums[0]//(2*cnew[1]),ceildiv(nums[1],2*cnew[0])))
        c,s=cnew,snew
        roots.append((c,interval_neg(s,L)))
    # Enclosure of N^(-1/2). All m, including odd m, are supported.
    if m%2==0:
        value=D >> (m//2)
        inv=(value,value)
        L.record('exact_dyadic_normalizer',(D,m),inv)
    else:
        rt=sqrt_interval((2*D,2*D),D,L)
        den=1 << ((m+1)//2)
        inv=L.record('odd_dyadic_normalizer', rt+(den,), (rt[0]//den,ceildiv(rt[1],den)))
    L.slots += 8*len(roots)+2
    return tuple(roots),inv,D

def root_at(k,m,roots,D,L):
    out=((D,D),(0,0))
    for bit in range(m):
        if (k>>bit)&1:
            out=complex_mul(out,roots[m-bit],D,L)
    return out

def validate(raw,state,L):
    keys(raw,{'schema','N','F','entries'},'raw')
    keys(state,{'N','B','a','beta'},'state')
    if type(raw['schema']) is not str or raw['schema']!=SCHEMA: raise Failure('GRAMMAR: schema')
    n=integer(raw['N'],'N',L); F=integer(raw['F'],'F',L)
    if n<4 or n&(n-1): raise Failure('DOMAIN: dyadic N>=4')
    m=n.bit_length()-1
    if m>MAX_M: raise Failure('RESOURCE_LIMIT: log2 N')
    st={k:integer(state[k],k,L) for k in ('N','B','a','beta')}
    if st['N']!=n or st['B']!=n: raise Failure('UNSUPPORTED_STRUCTURE: singleton B_A=N')
    if not 0<st['a']<n or st['a']%2!=1 or not 0<=st['beta']<n: raise Failure('DOMAIN: ALG034 state')
    if type(raw['entries']) is not list: raise Failure('GRAMMAR: entries list')
    if len(raw['entries'])>MAX_SUPPORT: raise Failure('RESOURCE_LIMIT: sparse support')
    rows=[]; prev=-1;odd=False;W=0;energy=0;mass=0
    for row in raw['entries']:
        if type(row) is not list or len(row)!=3: raise Failure('GRAMMAR: sparse row')
        j=integer(row[0],'index',L);re=integer(row[1],'real',L,MAX_RAW_BITS);im=integer(row[2],'imag',L,MAX_RAW_BITS)
        if not 0<=j<n or j<=prev: raise Failure('GRAMMAR: sorted unique sparse indices')
        if re==im==0: raise Failure('GRAMMAR: sparse zero row')
        odd=odd or bool(re%2 or im%2);prev=j
        W=max(W,abs(re).bit_length(),abs(im).bit_length())
        energy=L.record('energy_accumulation',(energy,re,im),energy+re*re+im*im)
        mass=L.record('mass_accumulation',(mass,re,im),mass+abs(re)+abs(im))
        rows.append((j,re,im));L.slots+=4
    if rows and not odd: raise Failure('GRAMMAR: remove common numerator powers of two')
    if not rows and F!=0: raise Failure('GRAMMAR: zero has F=0')
    clean={'schema':SCHEMA,'N':n,'F':F,'entries':[list(row) for row in rows]}
    return clean,st,m,W,tuple(rows),energy,mass

@dataclass(frozen=True)
class Supplier:
    status: str
    N: int
    m: int
    entries: tuple
    F: int
    W: int
    h: int
    energy: int
    l1_mass: int
    query_bits: int
    working_bits: int
    roots: tuple
    invsqrtN: tuple
    D: int
    context_bytes: bytes
    policy_bytes: bytes
    descriptor_bytes: bytes
    ledger_bytes: bytes
    @property
    def context(self): return json.loads(self.context_bytes)
    @property
    def policy(self): return json.loads(self.policy_bytes)
    @property
    def descriptor(self): return json.loads(self.descriptor_bytes)
    @property
    def ledger(self): return json.loads(self.ledger_bytes)
    def packet(self):
        # One export pays the separately advertised fixed export envelope.
        return {'schema':PACKET,'context':self.context,'policy':self.policy,
                'descriptor':self.descriptor,'root_table':[[list(r),list(i)] for r,i in self.roots],
                'invsqrtN':list(self.invsqrtN),'working_bits':self.working_bits}
    def query(self,j,require_accepted_radius=False):
        """One paid point query. No cache, implicit N scan, or free replay."""
        L=Meter();j=integer(j,'query.index',L)
        if type(require_accepted_radius) is not bool: raise Failure('GRAMMAR: radius flag')
        if self.status!='NONZERO_EXACT_MODAL_SOURCE': raise Failure('DOMAIN: zero has no normalized source')
        if not 0<=j<self.N: raise Failure('DOMAIN: query index')
        policy=self.policy;plan=policy['plan'];R=self.query_bits;G=R+3
        required=plan['p']-plan['c']-self.W+self.h
        shift=plan['p']+self.h-self.W-G
        compliant=R>=required and shift>=0
        if require_accepted_radius and not compliant:
            raise Failure('PRECISION: query is not an accepted-radius original-grid query')
        total=((0,0),(0,0)); nonaxis=0;root_products=0
        for n,re,im in self.entries:
            k=L.record('phase_index',(n,j,self.N),(n*j)%self.N)
            root_products+=k.bit_count()
            nonaxis+=int(k%(self.N//4)!=0)
            r=root_at(k,self.m,self.roots,self.D,L)
            rr=interval_add(interval_scale(r[0],re,L),interval_neg(interval_scale(r[1],im,L),L),L)
            ii=interval_add(interval_scale(r[0],im,L),interval_scale(r[1],re,L),L)
            total=(interval_add(total[0],rr,L),interval_add(total[1],ii,L))
        den=L.physical_power(self.h)
        box=[];point=[];radii=[]
        step=L.physical_power(self.working_bits-G)
        for a in total:
            a=interval_mul(a,self.invsqrtN,self.D,L)
            a=L.record('normalize_energy_power',a+(den,),(a[0]//den,ceildiv(a[1],den)))
            qnum=L.record('round_box_midpoint',a+(step,),(a[0]+a[1]+step)//(2*step))
            physical=L.record('point_on_work_grid',(qnum,step),qnum*step)
            rad=L.record('point_component_error',a+(physical,),max(abs(physical-a[0]),abs(a[1]-physical)))
            box.append(list(a));point.append(qnum);radii.append(rad)
        sq=L.record('complex_error_squared',tuple(radii),radii[0]**2+radii[1]**2)
        bound=L.physical_power(2*(self.working_bits-R))
        if sq>bound: raise Failure('PRECISION: enclosure cannot certify requested query error')
        formal_width = max(abs(v).bit_length() for v in point) + shift if shift>=0 else None
        if formal_width is not None and formal_width>plan['p']+plan['I']:
            raise Failure('INVARIANT: original-grid stored range')
        payload={'schema':'ALG034_SPARSE_POINT_QUERY_V1','index':j,
                 'context_sha256':sha256(self.context_bytes).hexdigest(),
                 'value_numerators':point,'value_exponent':-G,
                 'enclosure_numerators':box,'enclosure_exponent':-self.working_bits,
                 'complex_error_power':-R,'ideal_target':'U_negative(x)/alpha',
                 'alpha':{'coefficient':1,'scale':self.h-self.F},
                 'accepted_serial_radius_compliant':compliant,
                 'formal_original_grid':({'numerator_bases':point,'common_left_shift':shift,
                                          'kappa':plan['kappa'],'formal_numerator_bits_max':formal_width} if shift>=0 else None),
                 'exact_root_products':root_products,'nonquarter_phase_terms':nonaxis,
                 'original_target_complex_error_power':self.h-self.F-R,
                 'bit_equivalent_to_rounded_serial':False}
        data=canonical(payload,L);L.bytes+=16384;L.slots+=16384
        return Query(data,json.dumps(L.snapshot(),sort_keys=True,separators=(',',':')).encode('ascii'))

@dataclass(frozen=True)
class Query:
    payload_bytes: bytes
    ledger_bytes: bytes
    @property
    def ledger(self): return json.loads(self.ledger_bytes)
    def packet(self): return json.loads(self.payload_bytes)

def execute(raw,state,t=16,q=None,p=None,query_bits=None):
    L=Meter();clean,st,m,W,rows,energy,mass=validate(raw,state,L)
    t=integer(t,'t',L);q=16*m+16 if q is None else integer(q,'q',L)
    if t<0 or q<m: raise Failure('DOMAIN: t>=0 and q>=log2 N')
    if p is not None:
        p=integer(p,'p',L)
        if p<0: raise Failure('DOMAIN: p>=0')
    query_bits=q+4 if query_bits is None else integer(query_bits,'query_bits',L)
    if not 8<=query_bits<=MAX_QUERY_BITS: raise Failure('RESOURCE_LIMIT: query precision 8..4096')
    n,F=clean['N'],clean['F']; h=0;working=0;roots=();inv=(0,0);D=1
    if not rows:
        if p is not None: raise Failure('DOMAIN: zero has no declared p')
        status='EXACT_INPUT_ZERO';plan=None;descriptor=None
    else:
        minimum,index=min((abs(re)+abs(im),j) for j,re,im in rows)
        K=(minimum-1).bit_length();G=W+(n-1)*K;c=n+3*m+6
        pmin=max(W,c+t+1,c+q+G+2)
        p=pmin if p is None else p
        integer(p,'selected p',L)
        if p<pmin: raise Failure('PRECISION: accepted one-shot policy')
        h=((energy-1).bit_length()+1)//2
        A=L.physical_power(h)
        if not A*A>=energy or not A*A<4*energy: raise Failure('INVARIANT: norm interval')
        kappa=W-F-p
        plan={'p':p,'p_min':pmin,'L':2*n,'D':n,'selected_block':index,'A':minimum,
              'K':K,'G':G,'H':1,'c':c,'C_factor':{'coefficient':1,'scale':c},
              'I':n+2*m+10,'kappa':kappa,'mu_scale':-F-(n-1)*K,
              'accepted_serial_radius_factor':{'coefficient':1,'scale':c+kappa},
              'normalized_accepted_radius_required_query_bits':p-c-W+h}
        working=query_bits+W+len(rows).bit_length()+4*m+32
        if working>6000: raise Failure('RESOURCE_LIMIT: working precision')
        roots,inv,D=root_setup(m,working,L)
        descriptor={'schema':'ALG034_EXACT_SPARSE_MODAL_V1','N':n,'F':F,
                    'entries':[list(row) for row in rows],
                    'unitary_sign':-1,'P_identity_reason':'B_A=N singleton blocks',
                    'exact_original_target':'N^(-1/2) sum (re+i im) 2^(-F) exp(-2 pi i n j/N)',
                    'exact_normalized_target':'N^(-1/2) sum (re+i im) 2^(-h) exp(-2 pi i n j/N)',
                    'h':h,'alpha':{'coefficient':1,'scale':h-F},
                    'raw_energy':energy,'raw_l1_mass':mass,
                    'normalized_norm_squared':{'numerator':energy,'denominator_power_two':2*h},
                    'norm_bounds':'1/2 < norm <= 1','representation_error':0,
                    'second_unitary_transform':'R(x)/alpha',
                    'spectral_support':[(-j)%n for j,_,_ in rows]}
        status='NONZERO_EXACT_MODAL_SOURCE'
    policy={'backend':BACKEND,'target':'U_negative(P_balanced_longer_first(x))','W':W,
            't':t,'q':q,'p':p,'plan':plan,'outcome':status,
            'bit_equivalent_to_rounded_serial':False,'numeric_query_budget_independent_of_serial':True}
    context={'raw':clean,'state':st,'t':t,'q':q,'p':p,'query_bits':query_bits}
    cb=canonical(context,L);pb=canonical(policy,L);db=canonical(descriptor,L)
    canonical({'roots':[[list(r),list(i)] for r,i in roots],'inverse_sqrt_N':list(inv),'working_bits':working},L)
    L.bytes+=16384;L.slots+=16384
    ledger=json.dumps(L.snapshot(),sort_keys=True,separators=(',',':')).encode('ascii')
    if len(ledger)>16384: raise Failure('RESOURCE_LIMIT: ledger reserve')
    return Supplier(status,n,m,rows,F,W,h,energy,mass,query_bits,working,roots,inv,D,cb,pb,db,ledger)

def verify(raw,state,t,q,packet,p=None,query_bits=None):
    """Fresh semantic replay binds to independently retained original context."""
    L=Meter();actual=canonical(packet,L)
    run=execute(raw,state,t,q,p,query_bits)
    expected=canonical(run.packet(),L)
    if actual!=expected: raise Failure('SEMANTIC_MISMATCH: original context or source packet')
    extra=L.snapshot()
    return {'status':'SEMANTICALLY_VERIFIED','bound_to_supplied_original_input':True,
            'external_origin_authenticated':False,'historical_execution_attested':False,
            'total_bit_work_upper':run.ledger['total_bit_work_upper']+extra['total_bit_work_upper']+EXPORT_BIT_WORK_BOUND,
            'cumulative_storage_upper_bits':run.ledger['cumulative_storage_upper_bits']+extra['cumulative_storage_upper_bits']+EXPORT_STORAGE_BITS_BOUND}

def verify_query(raw,state,t,q,index,packet,p=None,query_bits=None,require_accepted_radius=False):
    L=Meter();actual=canonical(packet,L)
    run=execute(raw,state,t,q,p,query_bits)
    answer=run.query(index,require_accepted_radius)
    expected=canonical(answer.packet(),L)
    if actual!=expected: raise Failure('SEMANTIC_MISMATCH: point query')
    extra=L.snapshot()
    return {'status':'QUERY_SEMANTICALLY_VERIFIED','bound_to_supplied_original_input':True,
            'external_origin_authenticated':False,'historical_execution_attested':False,
            'total_bit_work_upper':run.ledger['total_bit_work_upper']+answer.ledger['total_bit_work_upper']+extra['total_bit_work_upper']+EXPORT_BIT_WORK_BOUND,
            'cumulative_storage_upper_bits':run.ledger['cumulative_storage_upper_bits']+answer.ledger['cumulative_storage_upper_bits']+extra['cumulative_storage_upper_bits']+EXPORT_STORAGE_BITS_BOUND}

def fixture():
    n=1<<28
    return ({'schema':SCHEMA,'N':n,'F':0,'entries':[[1,1,0],[3,1,0]]},
            {'N':n,'B':n,'a':1,'beta':0})
