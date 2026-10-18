"""Fresh production outer iterator and immutable, concrete median-output binding.

Numerical producer dependency: fresh sparse_output.py port of the accepted
MedianResult API. Binding is an in-process trusted-program invariant, not an
attestation of hostile Python state or external historical execution.
"""
from dataclasses import dataclass
from sparse_output import ProducedMedians, MedianResult, verify_produced


class ReceiptLedger:
    """Cumulative conservative schoolbook accounting for control and I/O work."""
    __slots__ = ('events', 'bit_work', 'produced_bits', 'max_bits', 'fields')
    def __init__(self):
        self.events = 0
        self.bit_work = 0
        self.produced_bits = 0
        self.max_bits = 1
        self.fields = 0
    def charge(self, *values, count=1):
        # Source-level upper envelope includes fixed-length tuple/dataclass
        # control, bounded loop/address/counter work and integer copies.
        width = max((abs(v).bit_length()+1 for v in values), default=1)
        width = max(width, (self.events+count+1).bit_length(), 1)
        self.events += count
        self.bit_work += count * 256 * width * width
        self.produced_bits += count * 64 * width
        self.max_bits = max(self.max_bits, width)
    def integer(self, value):
        self.charge()
        if type(value) is not int:
            raise ValueError('exact built-in integer required')
        self.charge(value)
        self.fields += 1
        return value
    def report(self):
        return {name: getattr(self, name) for name in self.__slots__}


@dataclass(frozen=True, slots=True)
class Header:
    N: int
    M: int
    D: int
    estimate_bits: int


@dataclass(frozen=True, slots=True)
class Geometry:
    N: int
    M: int
    D: int
    m: int
    s: int
    h: int
    t: int
    J: int
    K: int
    p: int
    dense_required: bool


def geometry(header, ledger):
    ledger.charge()
    if type(header) is not Header:
        raise ValueError('exact Header required')
    N, M, D, P = (ledger.integer(x) for x in
                   (header.N, header.M, header.D, header.estimate_bits))
    if N < 1 or D < 5 or P < 8:
        raise ValueError('N>=1, D>=5 and estimate_bits>=8 required')
    target = 1 << (4*N-1).bit_length()
    ledger.charge(N, M, D, P, target, count=16)
    if M != target:
        raise ValueError('M must equal 2^ceil(log2(4N))')
    m = M.bit_length()-1
    s = D*m
    h = 16*s+1
    t = 2*h+2
    J = (D+5)*m+s.bit_length()+8
    K = J+2*(J+1).bit_length()+16
    p = (D+3)*m+3
    ledger.charge(m,s,h,t,J,K,p,count=32)
    return Geometry(N,M,D,m,s,h,t,J,K,p,t>=M)


@dataclass(frozen=True, slots=True)
class Binding:
    header: Header
    run: ProducedMedians
    output: MedianResult
    support: tuple
    geometry: Geometry
    endpoints: tuple
    _owner: object


@dataclass(frozen=True, slots=True)
class Incidence:
    binding: Binding
    ordinal: int
    support_ordinal: int
    k: int
    ell: int
    lifted: int


@dataclass(frozen=True, slots=True)
class _CoefficientOrigin:
    owner: object
    incidence: Incidence
    result: object


@dataclass(frozen=True, slots=True)
class Coefficient:
    incidence: Incidence
    real: int
    imag: int
    p: int
    real_enclosure: object
    imag_enclosure: object
    certificate: object
    _origin: _CoefficientOrigin


class Outer:
    """A source-pinned single-run wrapper with no arbitrary record input path.

    Enumeration is lazy and contains only support and incidence loops. Numerical
    setup is lazy at the first selected coefficient. The public emitter checks
    binding and incidence identity arithmetic before forwarding to the kernel.
    Repeated binding validation accumulates charges; preparation never resets.
    """
    def __init__(self, header, produced, ledger=None):
        if ledger is not None and type(ledger) is not ReceiptLedger:
            raise ValueError('exact ReceiptLedger required')
        self.ledger = ledger if ledger is not None else ReceiptLedger()
        L = self.ledger
        G = geometry(header, L)
        verify_produced(produced, L, replay=True)
        output = produced.output
        if produced.M != G.M or output.bits != header.estimate_bits:
            raise ValueError('accepted-output header mismatch')
        # Deep immutable exact fields and sorted order are independently checked
        # at this boundary. No canonicalization or hashing is used or hidden.
        L.charge()
        if type(output) is not MedianResult or type(output.pairs) is not tuple:
            raise ValueError('exact immutable MedianResult required')
        L.integer(output.bits)
        support = []
        previous = -1
        for entry in output.pairs:
            L.charge(previous,G.M,count=8)
            if type(entry) is not tuple or len(entry)!=2:
                raise ValueError('exact sparse pair required')
            k, pair = entry
            L.integer(k)
            if not 0 <= k < G.M or k <= previous:
                raise ValueError('support must be sorted, unique and in range')
            if type(pair) is not tuple or len(pair)!=2:
                raise ValueError('exact Cartesian pair required')
            L.integer(pair[0]); L.integer(pair[1])
            L.charge(k,pair[0],pair[1],count=8)
            support.append(k); previous=k
        L.charge(len(support),G.M,count=8+len(support))
        self._owner = object()
        endpoints=[]
        prefix=0
        if not G.dense_required:
            for k in support:
                r0=-((-G.N*(k-G.h-1))//G.M)
                r1=-((-G.N*(k+G.h+1))//G.M)
                endpoints.append((r0,r1,prefix))
                prefix+=r1-r0
                L.charge(G.N,G.M,k,r0,r1,prefix,count=32)
        self.binding = Binding(header,produced,output,tuple(support),G,tuple(endpoints),self._owner)
        self.kernel = None
        self.last_failure = None
    def validate_binding(self, binding):
        L=self.ledger
        L.charge(count=16)
        if type(binding) is not Binding or binding is not self.binding:
            raise ValueError('mixed or substituted binding')
        if binding._owner is not self._owner:
            raise ValueError('mixed binding owner')
        verify_produced(binding.run,L)
        if binding.output is not binding.run.output:
            raise ValueError('substituted accepted output')
        return binding.geometry
    def incidences(self):
        B=self.binding; L=self.ledger; G=self.validate_binding(B)
        if G.dense_required:
            self.last_failure='OUTER_DENSE_REQUIRED'
            return
        ordinal=0
        for column,k in enumerate(B.support):
            r0,r1,prefix=B.endpoints[column]
            L.charge(G.N,G.M,k,r0,r1,ordinal,column,count=24)
            for lifted in range(r0,r1):
                ell=lifted%G.N
                L.charge(lifted,ell,k,ordinal,column,G.N,count=24)
                yield Incidence(B,ordinal,column,k,ell,lifted)
                ordinal+=1
    def _validate_incidence(self, incidence):
        L=self.ledger
        if type(incidence) is not Incidence:
            L.charge(); raise ValueError('exact Incidence required')
        G=self.validate_binding(incidence.binding)
        for x in (incidence.ordinal,incidence.support_ordinal,incidence.k,
                  incidence.ell,incidence.lifted): L.integer(x)
        if G.dense_required:
            raise ValueError('OUTER_DENSE_REQUIRED')
        column=incidence.support_ordinal
        if not 0<=column<len(self.binding.support) or self.binding.support[column]!=incidence.k:
            raise ValueError('substituted support index')
        k=incidence.k
        r0=-((-G.N*(k-G.h-1))//G.M)
        r1=-((-G.N*(k+G.h+1))//G.M)
        L.charge(G.N,G.M,k,r0,r1,incidence.lifted,count=24)
        if not r0<=incidence.lifted<r1 or incidence.ell!=incidence.lifted%G.N:
            raise ValueError('substituted incidence')
        # Endpoint/prefix records were paid once at bind time; each check is O(1).
        br0,br1,prefix=self.binding.endpoints[column]
        L.charge(br0,br1,prefix,incidence.lifted,count=8)
        expected=prefix+incidence.lifted-br0
        if incidence.ordinal!=expected:
            raise ValueError('substituted incidence ordinal')
        return G
    def coefficient(self, incidence):
        G=self._validate_incidence(incidence)
        if self.kernel is None:
            from production_scalar import CoefficientEngine, Paid
            self.kernel=CoefficientEngine(G.N,G.M,G.D,Paid())
            self.ledger.charge(G.N,G.M,G.D,count=16)
        # Kernel returns a source-defined record, wrapped without a new rounding.
        result=self.kernel.coefficient(incidence.ell,incidence.k)
        self.ledger.charge(result.real_integer,result.imag_integer,result.p,
                           result.real_enclosure.lo,result.real_enclosure.hi,
                           result.imag_enclosure.lo,result.imag_enclosure.hi,
                           result.radius_squared,result.eta_squared_grid,count=32)
        return Coefficient(incidence,result.real_integer,result.imag_integer,result.p,
                           result.real_enclosure,result.imag_enclosure,result,
                           _CoefficientOrigin(self._owner,incidence,result))

    def validate_coefficient(self, record):
        L=self.ledger
        L.charge(count=24)
        if type(record) is not Coefficient or type(record._origin) is not _CoefficientOrigin:
            raise ValueError('exact emitted Coefficient required')
        origin=record._origin
        if origin.owner is not self._owner or record.incidence is not origin.incidence or record.certificate is not origin.result:
            raise ValueError('mixed or substituted coefficient origin')
        self._validate_incidence(record.incidence)
        result=origin.result
        for value in (record.real,record.imag,record.p): L.integer(value)
        if record.real_enclosure is not result.real_enclosure or record.imag_enclosure is not result.imag_enclosure:
            raise ValueError('substituted coefficient enclosure')
        fields=(record.real,record.imag,record.p,record.real_enclosure,record.imag_enclosure)
        expected=(result.real_integer,result.imag_integer,result.p,result.real_enclosure,result.imag_enclosure)
        L.charge(record.real,record.imag,record.p,result.radius_squared,result.eta_squared_grid,count=32)
        if fields!=expected or result.ell!=record.incidence.ell or result.k!=record.incidence.k:
            raise ValueError('substituted coefficient fields')
        if result.radius_squared>result.eta_squared_grid:
            raise ArithmeticError('coefficient certificate defect')
        return record
