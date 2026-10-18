"""Fresh, bounded, target-explicit dense reference. Standard-library only.

The FIRST_DFT path is a certified direct DFT, not a fast Fourier algorithm.
The SINGLETON_SECOND_NORMALIZED path is exact reversal for B_A=N.
No inherited research code, caller coefficient, or sparse-result callback runs.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from math import isqrt, factorial
import json


@dataclass(frozen=True)
class Limits:
    max_n: int = 128
    max_source_bits: int = 1024
    max_metadata_bits: int = 128
    max_target_bits: int = 128
    max_materialized_shift: int = 8192
    max_numeric_bits: int = 1000000
    max_events: int = 2000000


class Rejected(ValueError):
    def __init__(self, reason, receipt, prior_receipts=()):
        super().__init__(reason)
        self.reason, self.receipt = reason, receipt
        # Completed earlier stages remain separately available on failure.
        # Add each prior receipt and the terminal receipt exactly once.
        self.prior_receipts = tuple(prior_receipts)


class Ledger:
    def __init__(self, limits):
        self.limits = limits
        self.events = self.max_width = self.numeric_work = 0
        self.read_coordinates = self.output_coordinates = 0
        self.coefficients = self.prefix_updates = self.setup_terms = 0
        self.comparison_nodes = 0
        self.logical_slots = self.source_bits = self.output_bits = 0

    def fail(self, reason):
        raise Rejected(reason, self.receipt())

    def op(self, *values):
        widths = []
        for x in values:
            if isinstance(x, Q):
                widths.extend((abs(x.numerator).bit_length()+1,
                               x.denominator.bit_length()+1))
            elif type(x) is int:
                widths.append(abs(x).bit_length()+1)
            else:
                raise TypeError("ledger supports exact scalar arithmetic only")
        # Fraction cross products, division and gcd have at most twice this
        # envelope. Cubic work dominates elementary schoolbook implementations.
        envelope = 2*sum(widths)+64
        self.events += 1
        self.max_width = max(self.max_width, envelope)
        self.numeric_work += 4096*envelope**3
        if envelope > self.limits.max_numeric_bits:
            self.fail("NUMERIC_WIDTH_LIMIT")
        if self.events > self.limits.max_events:
            self.fail("ARITHMETIC_EVENT_LIMIT")

    def receipt(self):
        E = (self.events+self.read_coordinates+self.output_coordinates+
             self.logical_slots+self.source_bits+self.output_bits+self.comparison_nodes+65536)
        V = max(1, self.max_width, self.numeric_work.bit_length(), E.bit_length())+64
        return tuple(sorted({
            "arithmetic_records": self.events,
            "max_arithmetic_envelope_bits": self.max_width,
            "numeric_binary_work_bound": self.numeric_work,
            "charged_units": E,
            "bookkeeping_width": V,
            "total_binary_work_bound": self.numeric_work+65536*E*V**3,
            "cumulative_storage_bit_bound": 4096*E*V,
            "input_coordinates_read": self.read_coordinates,
            "output_coordinates_written": self.output_coordinates,
            "coefficients_certified": self.coefficients,
            "exact_complex_prefix_updates": self.prefix_updates,
            "rational_setup_terms": self.setup_terms,
            "source_description_bits": self.source_bits,
            "output_description_bits": self.output_bits,
            "logical_slots": self.logical_slots,
            "comparison_nodes": self.comparison_nodes,
        }.items()))


def add(a,b,L):
    c=a+b; L.op(a,b,c); return c

def mul(a,b,L):
    c=a*b; L.op(a,b,c); return c

def div(a,b,L):
    c=a/b; L.op(a,b,c); return c


def rne_ratio(a,b):
    if b <= 0: raise ValueError("positive denominator required")
    q,r=divmod(a,b)
    return q + (2*r>b or (2*r==b and q%2!=0))


def rne_q(a):
    return rne_ratio(a.numerator,a.denominator)


def pow2(e):
    return Q(1 << e) if e>=0 else Q(1,1 << -e)


@dataclass(frozen=True)
class Source:
    N: int
    F: int
    entries: tuple
    input_kind: str
    h: int
    energy: int
    max_component_bits: int


def parse(raw,L,allow_large_n=False):
    # Length and exact key-type guards precede iteration/set construction.
    # A malformed dictionary cannot induce an uncharged unbounded key scan.
    if type(raw) is not dict or len(raw)!=4:
        L.fail("SOURCE_GRAMMAR")
    if any(type(k) is not str for k in raw) or set(raw)!={"N","F","kind","data"}:
        L.fail("SOURCE_GRAMMAR")
    N,F,kind,data=raw["N"],raw["F"],raw["kind"],raw["data"]
    if type(N) is not int or N<1 or type(F) is not int:
        L.fail("SOURCE_INTEGER_DOMAIN")
    n_width,f_width=N.bit_length(),F.bit_length()
    L.op(n_width,f_width)
    if max(n_width,f_width)>L.limits.max_metadata_bits:
        L.fail("SOURCE_METADATA_LIMIT")
    L.source_bits += N.bit_length()+abs(F).bit_length()+8
    L.op(N,F)
    if not allow_large_n and N>L.limits.max_n:
        L.fail("DENSE_ALLOCATION_LIMIT")
    if type(kind) is not str or kind not in ("dense","sparse") or type(data) is not list:
        L.fail("SOURCE_REPRESENTATION")
    if kind=="dense" and len(data)!=N:
        L.fail("DENSE_LENGTH")
    if kind=="sparse" and len(data)>N:
        L.fail("SPARSE_LENGTH")
    entries=[]; prev=-1; E=0; W=0; odd=False
    for j,row in enumerate(data):
        L.read_coordinates += 1
        L.logical_slots += 1
        if type(row) is not list or len(row)!=(2 if kind=="dense" else 3):
            L.fail("COORDINATE_GRAMMAR")
        n,a,b=(j,*row) if kind=="dense" else tuple(row)
        if any(type(z) is not int for z in (n,a,b)):
            L.fail("EXACT_INTEGER_REQUIRED")
        if not 0<=n<N or n<=prev:
            L.fail("SOURCE_INDEX_ORDER")
        prev=n
        width=max(a.bit_length(),b.bit_length())
        L.op(width)
        if width>L.limits.max_source_bits:
            L.fail("SOURCE_COMPONENT_LIMIT")
        L.source_bits += n.bit_length()+abs(a).bit_length()+abs(b).bit_length()+5
        L.op(n,a,b)
        if kind=="sparse" and a==b==0:
            L.fail("EXPLICIT_SPARSE_ZERO")
        if a or b:
            entries.append((n,a,b)); W=max(W,width); odd |= bool(a%2 or b%2)
            aa=a*a; bb=b*b; ee=aa+bb
            L.op(a,aa,b,bb,ee,E)
            E+=ee; L.op(E)
    if (entries and not odd) or (not entries and F!=0):
        L.fail("NONCANONICAL_COMMON_GRID")
    h=( (E-1).bit_length()+1)//2 if E else 0
    L.op(E,h)
    return Source(N,F,tuple(entries),kind,h,E,W)


def classification(source,target,D,L):
    if type(target) is not str or target not in ("FIRST_DFT","SINGLETON_SECOND_NORMALIZED"):
        L.fail("UNKNOWN_TARGET")
    if type(D) is not int or D<5 or D.bit_length()>L.limits.max_metadata_bits:
        L.fail("D_DOMAIN")
    N=source.N; m=(4*N-1).bit_length(); M=1 << m; t=32*D*m+4
    L.op(N,D,m,M,t)
    legacy=(N==1<<28 and 1<=len(source.entries)<=16 and
            source.max_component_bits<=1024 and abs(source.F).bit_length()<=128)
    # This flag is only a domain observation; it is NOT a source bridge.
    return tuple(sorted({
        "outer_M":M,"outer_m":m,"outer_t":t,
        "outer_structural_sparse_guard":t<M,
        "legacy_recovery_source_domain":legacy,
        "same_target_sparse_provider_bound":False,
        "target":target,
        "route":"CERTIFIED_DIRECT_DFT" if target=="FIRST_DFT" else "EXACT_REVERSAL",
        "reason":("STRUCTURAL_DENSE_BOUNDARY" if t>=M else "NO_BOUND_SAME_TARGET_SPARSE_PROVIDER")
                 if target=="FIRST_DFT" else "SINGLETON_SECOND_TRANSFORM_IDENTITY",
    }.items()))


def plan(raw,target="FIRST_DFT",D=5,limits=Limits()):
    L=Ledger(limits); source=parse(raw,L,allow_large_n=True)
    info=classification(source,target,D,L)
    return info,L.receipt()


def atan_interval(inv,n,L):
    total=Q(0); power=inv; square=inv*inv; L.op(inv,square)
    for k in range(n):
        term=Q(1,power*(2*k+1)); L.op(power,2*k+1,term)
        total=add(total,term if k%2==0 else -term,L)
        power*=square; L.op(power); L.setup_terms+=1
    nxt=Q(1,power*(2*n+1)); L.op(power,nxt)
    return (total,total+nxt) if n%2==0 else (total-nxt,total)


def pi_interval(g,L):
    a,b=atan_interval(5,g+10,L)
    c,d=atan_interval(239,g+10,L)
    lo=add(mul(Q(16),a,L),-mul(Q(4),d,L),L)
    hi=add(mul(Q(16),b,L),-mul(Q(4),c,L),L)
    if not 3<lo<hi<4: L.fail("PI_INVARIANT")
    return lo,hi


def interval_product(a,b,c,d,L):
    values=[mul(x,y,L) for x in (a,b) for y in (c,d)]
    return min(values),max(values)


def coefficients(N,q,L):
    g=q+8; den=1<<g
    pl,pu=pi_interval(g,L)
    # Outward dyadic reduction prevents rational pi denominators propagating
    # into every Taylor power. All inequalities remain exact.
    pd=1<<(g+16)
    lp=(pl.numerator*pd)//pl.denominator
    up=-((-pu.numerator*pd)//pu.denominator)
    L.op(pl,pu,pd,lp,up)
    pl,pu=Q(lp,pd),Q(up,pd)
    pc=div(add(pl,pu,L),Q(2),L)
    pr=div(pu-pl,Q(2),L)
    square=1<<(2*g); z=isqrt(square//N); L.op(square,N,z)
    sl=Q(z,den); su=sl if z*z*N==square else Q(z+1,den)
    L.op(sl,su,z*z*N)
    K=g+40
    remainder=Q(4**(K+1),factorial(K+1)); L.op(remainder,K)
    table=[]
    for j in range(N):
        a=j if 2*j<=N else j-N
        factor=Q(2*a,N); x=mul(factor,pc,L)
        err=add(mul(abs(factor),pr,L),remainder,L)
        if abs(x)>=4: L.fail("ANGLE_INVARIANT")
        re=Q(1); im=Q(0); term=Q(1)
        for k in range(1,K+1):
            term=div(mul(term,x,L),Q(k),L)
            phase=k%4
            if phase==0: re=add(re,term,L)
            elif phase==1: im=add(im,term,L)
            elif phase==2: re=add(re,-term,L)
            else: im=add(im,-term,L)
            L.setup_terms+=1
        rlo,rhi=interval_product(re-err,re+err,sl,su,L)
        ilo,ihi=interval_product(-im-err,-im+err,sl,su,L)
        rr=rne_q((rlo+rhi)*den/2); ii=rne_q((ilo+ihi)*den/2)
        L.op(rr,ii,rlo,rhi,ilo,ihi)
        dr=max(abs(Q(rr,den)-rlo),abs(Q(rr,den)-rhi))
        di=max(abs(Q(ii,den)-ilo),abs(Q(ii,den)-ihi))
        L.op(dr,di,dr*dr+di*di)
        if dr*dr+di*di>Q(1,1<<(2*q)):
            L.fail("COEFFICIENT_CERTIFICATE")
        if max(abs(rr),abs(ii))>=2*den: L.fail("COEFFICIENT_RANGE")
        table.append((rr,ii)); L.coefficients+=1; L.logical_slots+=2
    return tuple(table),g


@dataclass(frozen=True)
class Result:
    source: Source
    target: str
    pairs: tuple
    denominator_exponent: int
    requested_bits: int
    dispatch: tuple
    receipt: tuple
    alpha_exponent: int

    def data(self):
        return {"source":{"N":self.source.N,"F":self.source.F,
                          "entries":self.source.entries,"kind":self.source.input_kind,
                          "h":self.source.h,"energy":self.source.energy},
                "target":self.target,"pairs":self.pairs,
                "denominator_exponent":self.denominator_exponent,
                "requested_bits":self.requested_bits,"dispatch":dict(self.dispatch),
                "receipt":dict(self.receipt),"alpha_exponent":self.alpha_exponent}


def execute(raw,target="FIRST_DFT",bits=32,D=5,B_A=None,limits=Limits()):
    L=Ledger(limits); source=parse(raw,L); info=classification(source,target,D,L)
    N,F,h=source.N,source.F,source.h
    if type(bits) is not int or not 0<=bits<=limits.max_target_bits:
        L.fail("PRECISION_DOMAIN")
    if B_A is not None and (type(B_A) is not int or B_A!=N):
        L.fail("GENERAL_BLOCK_SOURCE_NOT_IMPLEMENTED")
    if target=="SINGLETON_SECOND_NORMALIZED" and B_A!=N:
        L.fail("SINGLETON_BLOCK_BINDING_REQUIRED")
    if target=="FIRST_DFT":
        m=(N-1).bit_length(); b=bits+m+4; scale=h-F
        shift=max(0,-F) if N==1 else max(0,scale-b)
        exponent=max(0,F) if N==1 else max(0,b-scale)
    else:
        b=h; scale=0; shift=0; exponent=h
    L.op(bits,b,scale,shift,exponent)
    # Never allocate a huge physical scale-back numerator on a metadata promise.
    if shift>limits.max_materialized_shift:
        L.fail("MATERIALIZED_OUTPUT_SHIFT_LIMIT")
    L.logical_slots+=2*N
    if not source.entries:
        pairs=tuple((0,0) for _ in range(N)); exponent=0
    elif target=="SINGLETON_SECOND_NORMALIZED":
        pairs=[(0,0) for _ in range(N)]
        for j,a,c in source.entries:
            k=(-j)%N; pairs[k]=(a,c); L.op(j,k,a,c)
        pairs=tuple(pairs)
    elif N==1:
        _,a,c=source.entries[0]
        pairs=((a<<shift,c<<shift),)
        L.op(a,c,shift,pairs[0][0],pairs[0][1])
    else:
        table,g=coefficients(N,b,L)
        # Dense input is visited fully by parse. This direct evaluator sums all
        # represented nonzeros for every output; worst case is N squared.
        denominator=1<<(h+g-b); L.op(denominator,h,g,b)
        acc_width=source.max_component_bits+g+m+4
        pairs=[]
        for k in range(N):
            ar=ai=0
            for j,a,c in source.entries:
                idx=(j*k)%N; u,v=table[idx]
                p1=a*u; p2=c*v; p3=a*v; p4=c*u
                ar+=p1-p2; ai+=p3+p4
                L.op(j,k,idx,a,c,u,v,p1,p2,p3,p4,ar,ai)
                L.prefix_updates+=1
                if max(abs(ar),abs(ai)) >= 1<<(acc_width-1):
                    L.fail("PREFIX_ACCUMULATOR_RANGE")
            rr=rne_ratio(ar,denominator); ii=rne_ratio(ai,denominator)
            L.op(ar,ai,denominator,rr,ii)
            rr <<= shift; ii <<= shift; L.op(rr,ii,shift)
            pairs.append((rr,ii))
        pairs=tuple(pairs)
    L.output_coordinates=N
    L.output_bits=exponent.bit_length()+8
    for a,c in pairs:
        L.output_bits+=abs(a).bit_length()+abs(c).bit_length()+4
    L.op(L.output_bits,N,exponent)
    # Source/result movement is paid by the production envelope. Canonical
    # exports and complete semantic replays add their own explicit receipts.
    L.logical_slots+=3*len(source.entries)+2*N+128
    return Result(source,target,pairs,exponent,bits,info,L.receipt(),h-F)


def export(result):
    text=json.dumps(result.data(),sort_keys=True,separators=(",",":"))
    # Explicit finite export charge, separate from any future calls.
    w=max(64,len(text).bit_length(),dict(result.receipt)["bookkeeping_width"])
    return text,{"export_bytes":len(text.encode()),
                 "binary_work_bound":65536*(len(text)+4096)*w**3,
                 "cumulative_storage_bit_bound":4096*(len(text)+4096)*w}



def exact_tree_equal(got,expected,L):
    """Compare only the expected shape, without calling supplied equality hooks."""
    L.comparison_nodes+=1
    if type(got) is not type(expected):
        return False
    t=type(expected)
    if t is Result:
        names=("source","target","pairs","denominator_exponent",
               "requested_bits","dispatch","receipt","alpha_exponent")
        return all(exact_tree_equal(getattr(got,k),getattr(expected,k),L) for k in names)
    if t is Source:
        names=("N","F","entries","input_kind","h","energy","max_component_bits")
        return all(exact_tree_equal(getattr(got,k),getattr(expected,k),L) for k in names)
    if t is tuple:
        if len(got)!=len(expected):
            return False
        return all(exact_tree_equal(got[k],expected[k],L) for k in range(len(expected)))
    if t is str:
        if len(got)!=len(expected):
            return False
        L.source_bits+=8*len(expected)
        return got==expected
    if t is int:
        # bit_length reads exact-int size metadata. Reject huge wrong operands
        # before abs(), copying, arithmetic or content equality can scan them.
        if got.bit_length()!=expected.bit_length():
            return False
        L.op(got,expected)
        return got==expected
    if t is bool:
        L.op(int(got),int(expected))
        return got is expected
    raise AssertionError("unexpected trusted result field type")


def verify(raw,result,**kwargs):
    rebuilt=execute(raw,**kwargs)
    # Full original-source replay; digest equality and supplied __eq__ methods
    # are not evidence. The trusted expected tree bounds every traversal.
    L=Ledger(kwargs.get("limits",Limits()))
    try:
        equal=exact_tree_equal(result,rebuilt,L)
    except Rejected as e:
        raise Rejected(e.reason,e.receipt,(rebuilt.receipt,)+e.prior_receipts) from None
    except AttributeError:
        # An exact dataclass allocated without its constructor may lack fields.
        # This is malformed supplied data, not a successful comparison.
        raise Rejected("RESULT_TREE_GRAMMAR",L.receipt(),(rebuilt.receipt,)) from None
    return equal,rebuilt.receipt,L.receipt()
