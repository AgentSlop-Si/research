"""Fresh paid port of the accepted Cartesian-median sparse numerical API.

The accepted API is MedianResult(pairs, bits), defined in phase_medians.py
SHA256 recorded in SOURCE_PINS.json. This implementation is new and requires
review. It supplies actual numerical outputs, not a caller-provided echo label.
It does not turn supplied estimate rows into random-recovery provenance.
"""
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class MedianResult:
    pairs: tuple
    bits: int

@dataclass(frozen=True, slots=True)
class _Origin:
    M: int
    bits: int
    output: MedianResult
    candidates: tuple
    rows: tuple
    capability: object

@dataclass(frozen=True, slots=True)
class ProducedMedians:
    M: int
    output: MedianResult
    _origin: _Origin
    _capability: object


def verify_produced(produced,L,replay=False):
    L.charge(count=12)
    if type(produced) is not ProducedMedians or type(produced._origin) is not _Origin:
        raise ValueError('exact produced median run required')
    origin=produced._origin
    if type(produced.output) is not MedianResult or type(origin.output) is not MedianResult:
        raise ValueError('exact immutable MedianResult required')
    L.integer(produced.M);L.integer(origin.M)
    L.integer(produced.output.bits);L.integer(origin.bits)
    if produced._capability is not origin.capability or produced.output is not origin.output:
        raise ValueError('mixed or substituted produced output')
    if produced.M!=origin.M or produced.output.bits!=origin.bits:
        raise ValueError('mixed produced header')
    if replay:
        rerun=produce_medians(origin.M,origin.bits,origin.candidates,origin.rows,L)
        if type(produced.output.pairs) is not tuple or len(rerun.output.pairs)!=len(produced.output.pairs):
            raise ValueError('accepted-output semantic replay mismatch')
        for expected,actual in zip(rerun.output.pairs,produced.output.pairs):
            if type(actual) is not tuple or len(actual)!=2 or type(actual[1]) is not tuple or len(actual[1])!=2:
                raise ValueError('exact sparse pair required')
            for value in (actual[0],actual[1][0],actual[1][1]): L.integer(value)
            L.charge(expected[0],expected[1][0],expected[1][1],actual[0],actual[1][0],actual[1][1],count=12)
            if expected!=actual:
                raise ValueError('accepted-output semantic replay mismatch')
        L.charge(origin.M,origin.bits,count=8+len(origin.candidates))
    return produced.output


def _sort(values,L):
    """Fresh bounded paid merge sort; no uncharged library sorting."""
    length=len(values)
    src=list(values);dst=[0]*length
    L.charge(length,count=2*length+4)
    step=1
    while step<length:
        for start in range(0,length,2*step):
            mid=min(start+step,length);end=min(start+2*step,length)
            left=start;right=mid
            for out in range(start,end):
                take=right==end or (left<mid and src[left]<=src[right])
                value=src[left] if take else src[right]
                dst[out]=value
                if take:left+=1
                else:right+=1
                L.charge(value,length,start,step,out,count=16)
        src,dst=dst,src;step*=2
        L.charge(step,length,count=8)
    return src


def produce_medians(M,P,candidates,rows,L):
    """Produce the accepted numerical MedianResult API from supplied estimate rows.

    Rows are exact immutable tuples of integer Cartesian pairs. This fresh port
    eliminates only the historical EstimateResult dataclass wrapper. It does not
    claim actual BUCKETS/phase origin, fresh tapes, or successful sparse recovery.
    Output binding below is genuine to this computed result in trusted execution.
    """
    from outer_wrapper import ReceiptLedger
    if type(L) is not ReceiptLedger:
        raise ValueError('exact ReceiptLedger required')
    L.integer(M);L.integer(P)
    if M<4 or M&(M-1) or P<8:
        raise ValueError('M must be a power of two >=4; P>=8 required')
    L.charge(M,P,count=12)
    if type(candidates) is not tuple:
        raise ValueError('exact immutable candidate tuple required')
    previous=-1
    for k in candidates:
        L.integer(k)
        if not 0<=k<M or k<=previous:
            raise ValueError('candidates must be valid, sorted and distinct')
        L.charge(k,previous,M,count=8);previous=k
    if type(rows) is not tuple or not rows or len(rows)%2!=1:
        L.charge();raise ValueError('a positive odd immutable tuple of rounds required')
    count=len(candidates);length=len(rows)
    L.charge(count,length,count=12)
    for row in rows:
        L.charge(count,length,count=8)
        if type(row) is not tuple or len(row)!=count:
            raise ValueError('estimate row shape mismatch')
        for pair in row:
            L.charge(count=4)
            if type(pair) is not tuple or len(pair)!=2:
                raise ValueError('exact Cartesian pair required')
            L.integer(pair[0]);L.integer(pair[1])
    pairs=[]
    for column,k in enumerate(candidates):
        re=[];im=[]
        for row in rows:
            a,b=row[column];re.append(a);im.append(b)
            L.charge(a,b,column,k,count=12)
        real=_sort(re,L)[length//2];imag=_sort(im,L)[length//2]
        pairs.append((k,(real,imag)))
        L.charge(real,imag,k,count=16)
    output=MedianResult(tuple(pairs),P)
    cap=object();origin=_Origin(M,P,output,candidates,rows,cap)
    L.charge(M,P,count=16+count)
    return ProducedMedians(M,output,origin,cap)
