"""New certified constant-block centered-source provider. No inherited imports.

The exact target is U_M J_N u, with N=M/4. Its exact support is 3N+1.
The sparse output is an approximation, never an assertion of exact sparsity.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from math import isqrt


class Rejected(ValueError):
    pass


class Ledger:
    def __init__(self):
        self.events = {}
        self.operations = self.work = self.produced = self.max_width = 0

    def mark(self, name, count=1):
        self.events[name] = self.events.get(name, 0) + count

    def record(self, name, *items):
        widths = []
        for x in items:
            if type(x) is F:
                widths.extend((x.numerator.bit_length()+1, x.denominator.bit_length()+1))
            elif type(x) is int:
                widths.append(x.bit_length()+1)
            else:
                raise AssertionError('unmetered numerical type')
        self.operations += 1
        self.mark(name)
        self.max_width = max(self.max_width, *widths, 1)
        self.work += 4096*(sum(widths)+32)**3
        self.produced += sum(widths)

    def arithmetic(self, kind, a, b):
        if kind == 'add': c = a+b
        elif kind == 'sub': c = a-b
        elif kind == 'mul': c = a*b
        elif kind == 'div': c = a/b
        else: raise AssertionError(kind)
        self.record(kind, a, b, c)
        return c

    def report(self):
        events = sum(self.events.values()) + self.operations + 1024
        width = self.max_width + events.bit_length() + 64
        return {'events': dict(sorted(self.events.items())),
                'arithmetic_records': self.operations,
                'max_numeric_width': self.max_width,
                'arithmetic_bit_work_upper': self.work,
                'control_bit_work_upper': (1 << 20)*events*width**3,
                'cumulative_bits_upper': self.produced+4096*events*width,
                'scope': 'production only; export, oracle, replay and outer are separate'}


def checked_int(x, name, bits, L):
    if type(x) is not int: raise Rejected(name+': exact integer required')
    width = x.bit_length()
    L.record('input_width', width)
    if width > bits: raise Rejected(name+': width limit')
    L.record('input_integer', x)
    return x


@dataclass(frozen=True, slots=True)
class Source:
    m: int
    N: int
    F: int
    real: int
    imag: int
    h: int
    scale: int
    input_kind: str


@dataclass(frozen=True, slots=True)
class Estimates:
    source: Source
    bits: int
    pairs: tuple
    cutoff: int
    exact_support_size: int
    target: str = 'U_M(J_N(u)); u=(real+i*imag)*2^-h on all N coordinates'


def recognize(obj, L, *, max_m=28, max_dense=4096):
    """Accept a supplied constant descriptor or inspect EVERY dense entry."""
    if type(obj) is not dict or len(obj) != 4:
        raise Rejected('input has exactly m,F,kind,data')
    if any(type(k) is not str for k in obj) or set(obj) != {'m','F','kind','data'}:
        raise Rejected('input keys')
    m = checked_int(obj['m'], 'm', 16, L)
    f = checked_int(obj['F'], 'F', 128, L)
    if not 11 <= m <= max_m: raise Rejected('reference m range 11..max_m')
    N = 1 << (m-2)
    kind = obj['kind']
    if type(kind) is not str or kind not in ('constant', 'dense'):
        raise Rejected('kind')
    data = obj['data']
    def pair(p):
        if type(p) not in (tuple,list) or len(p) != 2: raise Rejected('pair shape')
        return (checked_int(p[0], 'real', 1024, L), checked_int(p[1], 'imag', 1024, L))
    if kind == 'constant':
        c = pair(data)
    else:
        if N > max_dense: raise Rejected('dense read ceiling')
        if type(data) not in (tuple,list) or len(data) != N: raise Rejected('dense length')
        c = None
        for p in data:
            value = pair(p)
            L.mark('dense_coordinate_visits')
            if c is None: c = value
            L.record('source_equality', *c, *value)
            if value != c: raise Rejected('not a constant original')
    a,b = c
    if a == b == 0: raise Rejected('nonzero family only; zero uses a separate branch')
    if not (a%2 or b%2): raise Rejected('noncanonical common dyadic grid')
    aa=L.arithmetic('mul',a,a); bb=L.arithmetic('mul',b,b)
    E=L.arithmetic('mul',N,L.arithmetic('add',aa,bb))
    h=((E-1).bit_length()+1)//2
    scale=h-f
    L.record('normalization', E,h,scale,N)
    if abs(scale)>4*m: raise Rejected('outer scale requires |h-F|<=4m')
    return Source(m,N,f,a,b,h,scale,kind)


def outward(x, Q, L):
    scale=1 << Q
    low=x.numerator*scale//x.denominator
    high=-((-x.numerator*scale)//x.denominator)
    L.record('outward_grid',x,Q,scale,low,high)
    return F(low,scale),F(high,scale)


def iadd(a,b,L):
    return (L.arithmetic('add',a[0],b[0]),L.arithmetic('add',a[1],b[1]))


def ineg(a,L):
    r=(-a[1],-a[0]); L.record('interval_negate',*a,*r); return r


def imul(a,b,L):
    vals=[L.arithmetic('mul',x,y) for x in a for y in b]
    L.record('interval_order',*vals)
    return min(vals),max(vals)


def idiv(a,b,L):
    if b[0]<=0<=b[1]: raise Rejected('denominator interval crosses zero')
    vals=[L.arithmetic('div',x,y) for x in a for y in b]
    L.record('interval_order',*vals)
    return min(vals),max(vals)


def cmul(a,b,L):
    real=iadd(imul(a[0],b[0],L),ineg(imul(a[1],b[1],L),L),L)
    imag=iadd(imul(a[0],b[1],L),imul(a[1],b[0],L),L)
    return real,imag


def pi_interval(Q,L):
    def atan(q):
        t=F(1,q); total=F(0)
        for j in range(Q+10):
            term=L.arithmetic('div',t,F(2*j+1))
            total=L.arithmetic('add',total,term if j%2==0 else -term)
            t=L.arithmetic('div',t,F(q*q))
            L.mark('pi_series_terms')
        nxt=L.arithmetic('div',t,F(2*(Q+10)+1))
        other=L.arithmetic('add',total,nxt if (Q+10)%2==0 else -nxt)
        return min(total,other),max(total,other)
    a=atan(5);b=atan(239)
    lo=L.arithmetic('sub',L.arithmetic('mul',F(16),a[0]),L.arithmetic('mul',F(4),b[1]))
    hi=L.arithmetic('sub',L.arithmetic('mul',F(16),a[1]),L.arithmetic('mul',F(4),b[0]))
    lo=outward(lo,Q+16,L)[0];hi=outward(hi,Q+16,L)[1]
    L.mark('pi_preparations')
    return lo,hi


def trig(index,M,Q,pi,L):
    """Enclose cos(pi*index/M), sin(pi*index/M); exact rational Taylor."""
    r=index%(2*M)
    if r>M:r-=2*M
    mid=L.arithmetic('div',L.arithmetic('add',pi[0],pi[1]),F(2))
    rad=L.arithmetic('div',L.arithmetic('sub',pi[1],pi[0]),F(2))
    x=L.arithmetic('mul',F(r,M),mid)
    angle_error=L.arithmetic('mul',F(abs(r),M),rad)
    K=Q+40
    tr,ti=F(1),F(0);sr,si=F(1),F(0)
    for n in range(1,K+1):
        nr=L.arithmetic('div',-L.arithmetic('mul',ti,x),F(n))
        ni=L.arithmetic('div',L.arithmetic('mul',tr,x),F(n))
        tr,ti=nr,ni
        sr=L.arithmetic('add',sr,tr);si=L.arithmetic('add',si,ti)
        L.mark('taylor_steps')
    fact=1
    for n in range(1,K+2):fact=L.arithmetic('mul',fact,n)
    numerator=1 << (2*(K+1))
    L.record('remainder_power',K,numerator)
    error=L.arithmetic('add',F(numerator,fact),angle_error)
    out=[]
    for v in (sr,si):
        lo=outward(L.arithmetic('sub',v,error),Q,L)[0]
        hi=outward(L.arithmetic('add',v,error),Q,L)[1]
        if hi-lo > F(4,1 << Q):raise Rejected('trig enclosure width')
        out.append((lo,hi))
    L.mark('trig_calls')
    return tuple(out)


def reciprocal_root(M,Q,L):
    power=1 << (2*Q)
    a=isqrt(power//M)
    exact=a*a*M==power
    L.record('reciprocal_root',M,Q,power,a,int(exact))
    return F(a,1 << Q),F(a if exact else a+1,1 << Q)


def nearest_even(v,P,L):
    scaled=L.arithmetic('mul',v,F(1 << P))
    lower,remainder=divmod(scaled.numerator,scaled.denominator)
    result=lower+int(2*remainder>scaled.denominator or
                     (2*remainder==scaled.denominator and lower%2))
    L.record('round_nearest_even',scaled,lower,remainder,result)
    return result


def coefficient(source,k,P,pi,root,Q,L):
    N=source.N;M=4*N
    a=(F(source.real,1 << source.h),F(source.imag,1 << source.h))
    L.record('coefficient_normalization',source.real,source.imag,source.h,*a)
    if k == 0:
        ar=L.arithmetic('mul',a[0],F(N));ai=L.arithmetic('mul',a[1],F(N))
        interval=(imul((ar,ar),root,L),imul((ai,ai),root,L))
    elif k%4==0:
        interval=((F(0),F(0)),(F(0),F(0)))
    else:
        den=trig(k,M,Q,pi,L)
        num=trig(N*k,M,Q,pi,L)
        ratio=idiv(num[1],den[1],L)
        # N is even. Center J uses floor((N-1)/2), leaving exp(-pi*i*k/M).
        phase=(den[0],ineg(den[1],L))
        gain=imul(ratio,root,L)
        phase_scaled=(imul(phase[0],gain,L),imul(phase[1],gain,L))
        interval=cmul(((a[0],a[0]),(a[1],a[1])),phase_scaled,L)
    result=[];radii=[]
    for low,high in interval:
        mid=L.arithmetic('div',L.arithmetic('add',low,high),F(2))
        z=nearest_even(mid,P,L)
        radius=max(abs(F(z,1 << P)-low),abs(F(z,1 << P)-high))
        L.record('final_radius',low,high,z,radius)
        result.append(z);radii.append(radius)
    squared=L.arithmetic('add',L.arithmetic('mul',radii[0],radii[0]),L.arithmetic('mul',radii[1],radii[1]))
    if squared>F(1,1 << (2*P)):raise Rejected('coefficient radius certificate')
    L.mark('coefficient_outputs')
    return tuple(result)


def _produce(obj,L=None):
    if L is None:L=Ledger()
    source=recognize(obj,L)
    m=source.m;M=4*source.N;P=16*m+16;Q=P+2*m+16
    K=1 << ((m+3)//4)
    if 160*m+4>=M:raise Rejected('outer dense boundary')
    pi=pi_interval(Q,L);root=reciprocal_root(M,Q,L)
    signed=[k for k in range(-K,K+1) if k==0 or k%4]
    pairs=[]
    for k in sorted(signed,key=lambda k:k%M):
        values=coefficient(source,k,P,pi,root,Q,L)
        if any(abs(v)>=3*M*M*(1 << P) for v in values):raise Rejected('outer cap')
        pairs.append((k%M,values))
        L.record('support_output',k%M,*values)
    return Estimates(source,P,tuple(pairs),K,3*source.N+1),L.report()


def produce(obj,L=None):
    if L is None:L=Ledger()
    try:return _produce(obj,L)
    except Rejected as error:
        error.receipt=L.report()
        raise


def replay(original,answer):
    """Full source recognition and fresh coefficient production, then strict compare."""
    replayed,receipt=produce(original)
    C=Ledger()
    def equal(expected,actual):
        C.mark('comparison_nodes')
        if type(actual) is not type(expected):return False
        if type(expected) is int:
            a,b=expected.bit_length(),actual.bit_length()
            C.record('compare_width',a,b)
            if a!=b:return False
            C.record('compare_integer',expected,actual)
            return expected==actual
        if type(expected) is str:
            C.record('compare_string_length',len(expected),len(actual))
            if len(expected)!=len(actual):return False
            C.mark('compare_string_bytes',len(expected))
            return expected==actual
        if type(expected) is tuple:
            C.record('compare_tuple_length',len(expected),len(actual))
            if len(expected)!=len(actual):return False
            return all(equal(x,y) for x,y in zip(expected,actual))
        if type(expected) in (Source,Estimates):
            return all(equal(getattr(expected,n),getattr(actual,n)) for n in type(expected).__dataclass_fields__)
        raise AssertionError('comparison grammar')
    try:accepted=equal(replayed,answer)
    except AttributeError:accepted=False
    return accepted,{'replay_production':receipt,'comparison':C.report()}
