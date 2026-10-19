"""Certified sparse centered spectrum for recognized bounded-variation originals.

Numerical interval primitives are frozen accepted constant-provider code. This
module changes source recognition, target formula, cutoff and source replay.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent/'runtime'))
from interval_core import (Ledger,Rejected,checked_int,pi_interval,reciprocal_root,
    trig,iadd,ineg,imul,idiv,cmul,nearest_even)

@dataclass(frozen=True, slots=True)
class Source:
    m:int
    N:int
    F:int
    blocks:tuple  # (exclusive end, real integer, imaginary integer)
    energy:int
    variation_l1:int
    variation_factor:int
    h:int
    scale:int
    input_kind:str

@dataclass(frozen=True, slots=True)
class Estimates:
    source:Source
    bits:int
    pairs:tuple
    cutoff:int
    working_bits:int
    target:str='negative unitary U_M J_N u; u is the normalized block original'

def recognize(obj,L,*,max_m=28,max_dense=4096,max_blocks=64,max_factor=8):
    if type(obj) is not dict or len(obj)!=4:
        raise Rejected('input has exactly m,F,kind,data')
    if any(type(k) is not str for k in obj) or set(obj)!={'m','F','kind','data'}:
        raise Rejected('input keys')
    m=checked_int(obj['m'],'m',16,L)
    f=checked_int(obj['F'],'F',128,L)
    if not 11<=m<=max_m:raise Rejected('reference m range 11..max_m')
    N=1<<(m-2);kind=obj['kind'];data=obj['data']
    if type(kind) is not str or kind not in ('blocks','dense'):raise Rejected('kind')
    if type(data) not in (list,tuple):raise Rejected('data sequence')
    def pair(p):
        if type(p) not in (list,tuple) or len(p)!=2:raise Rejected('pair shape')
        return (checked_int(p[0],'real',1024,L),checked_int(p[1],'imag',1024,L))
    blocks=[]
    if kind=='blocks':
        if not 1<=len(data)<=max_blocks:raise Rejected('block count ceiling')
        last=0;previous=None
        for p in data:
            if type(p) not in (list,tuple) or len(p)!=3:raise Rejected('block triple shape')
            end=checked_int(p[0],'endpoint',m+1,L);value=pair(p[1:])
            L.mark('block_records_read');L.record('block_order',last,end,N,*value)
            if not last<end<=N:raise Rejected('strict partition endpoints')
            if previous==value:raise Rejected('adjacent equal blocks are not canonical')
            blocks.append((end,*value));last=end;previous=value
        if last!=N:raise Rejected('partition does not cover original')
    else:
        if N>max_dense:raise Rejected('dense read ceiling')
        if len(data)!=N:raise Rejected('dense length')
        previous=None
        for j,p in enumerate(data):
            value=pair(p);L.mark('dense_coordinate_visits');L.record('dense_position',j)
            if previous is not None:L.record('adjacent_comparison',*previous,*value)
            if value!=previous:
                if previous is not None:blocks.append((j,*previous))
                previous=value
        blocks.append((N,*previous))
        if len(blocks)>max_blocks:raise Rejected('block count ceiling after full dense scan')
    if not any(a%2 or b%2 for _,a,b in blocks):
        if all(a==b==0 for _,a,b in blocks):raise Rejected('nonzero family only')
        raise Rejected('noncanonical common dyadic grid')
    energy=0;variation=0;last=0;prev=(0,0)
    for end,a,b in blocks:
        square=L.arithmetic('add',L.arithmetic('mul',a,a),L.arithmetic('mul',b,b))
        energy=L.arithmetic('add',energy,L.arithmetic('mul',end-last,square))
        da=L.arithmetic('sub',a,prev[0]);db=L.arithmetic('sub',b,prev[1])
        variation=L.arithmetic('add',variation,abs(da)+abs(db))
        last=end;prev=(a,b)
    variation=L.arithmetic('add',variation,abs(prev[0])+abs(prev[1]))
    if energy==0:raise Rejected('nonzero family only')
    numerator=L.arithmetic('mul',N,L.arithmetic('mul',variation,variation))
    denominator=L.arithmetic('mul',4,energy)
    factor=isqrt(numerator//denominator)
    if factor*factor*denominator<numerator:factor+=1
    L.record('variation_certificate',numerator,denominator,factor)
    assert factor>=1 and factor*factor*denominator>=numerator
    if factor>max_factor:raise Rejected('variation factor exceeds structured-family ceiling')
    h=((energy-1).bit_length()+1)//2;scale=h-f
    L.record('normalization',energy,h,scale,N)
    if abs(scale)>4*m:raise Rejected('outer scale requires |h-F|<=4m')
    return Source(m,N,f,tuple(blocks),energy,variation,factor,h,scale,kind)

def coefficient(source,k,P,pi,root,Q,L):
    N=source.N;M=4*N;zero=(F(0),F(0));total=(zero,zero)
    if k==0:
        ar=ai=0;start=0
        for end,a,b in source.blocks:
            ar=L.arithmetic('add',ar,L.arithmetic('mul',end-start,a))
            ai=L.arithmetic('add',ai,L.arithmetic('mul',end-start,b));start=end
        ar=F(ar,1<<source.h);ai=F(ai,1<<source.h)
        L.record('zero_coefficient_normalization',ar,ai)
        total=(imul((ar,ar),root,L),imul((ai,ai),root,L))
    else:
        denominator=trig(k,M,Q,pi,L)[1];start=0;a0=(N-1)//2
        for end,a,b in source.blocks:
            numerator=trig((end-start)*k,M,Q,pi,L)[1]
            ratio=idiv(numerator,denominator,L)
            phase=trig((2*a0-start-end+1)*k,M,Q,pi,L)
            gain=imul(ratio,root,L)
            wave=(imul(phase[0],gain,L),imul(phase[1],gain,L))
            ar=F(a,1<<source.h);ai=F(b,1<<source.h)
            L.record('block_coefficient_normalization',start,end,a,b,ar,ai)
            term=cmul(((ar,ar),(ai,ai)),wave,L)
            total=(iadd(total[0],term[0],L),iadd(total[1],term[1],L));start=end
            L.mark('coefficient_block_terms')
    answer=[];radii=[]
    for low,high in total:
        mid=L.arithmetic('div',L.arithmetic('add',low,high),F(2))
        z=nearest_even(mid,P,L)
        radius=max(abs(F(z,1<<P)-low),abs(F(z,1<<P)-high))
        L.record('final_radius',low,high,z,radius)
        answer.append(z);radii.append(radius)
    squared=L.arithmetic('add',L.arithmetic('mul',radii[0],radii[0]),L.arithmetic('mul',radii[1],radii[1]))
    if squared>F(1,1<<(2*P)):raise Rejected('coefficient complex-radius certificate')
    L.mark('coefficient_outputs')
    return tuple(answer)

def produce(obj,L=None):
    if L is None:L=Ledger()
    try:
        source=recognize(obj,L);m=source.m;M=4*source.N;P=16*m+16
        q=len(source.blocks);Q=P+2*m+q.bit_length()+20
        K=source.variation_factor*(1<<((m+3)//4))
        L.record('cutoff',q,Q,K,M)
        if K>=M//2:raise Rejected('sparse cutoff must be below Nyquist')
        if 160*m+4>=M:raise Rejected('outer dense boundary')
        pi=pi_interval(Q,L);root=reciprocal_root(M,Q,L);pairs=[]
        for k in sorted(range(-K,K+1),key=lambda k:k%M):
            values=coefficient(source,k,P,pi,root,Q,L)
            if any(abs(v)>=3*M*M*(1<<P) for v in values):raise Rejected('outer coefficient cap')
            pairs.append((k%M,values));L.record('support_output',k%M,*values)
        return Estimates(source,P,tuple(pairs),K,Q),L.report()
    except Rejected as error:
        error.receipt=L.report();raise

def replay(original,answer):
    fresh,receipt=produce(original);C=Ledger()
    def equal(expected,actual):
        C.mark('comparison_nodes')
        if type(actual) is not type(expected):return False
        if type(expected) is int:
            a,b=expected.bit_length(),actual.bit_length();C.record('compare_width',a,b)
            if a!=b:return False
            C.record('compare_integer',expected,actual);return expected==actual
        if type(expected) is str:
            C.record('compare_string_length',len(expected),len(actual))
            if len(expected)!=len(actual):return False
            C.mark('compare_string_bytes',len(expected));return expected==actual
        if type(expected) is tuple:
            C.record('compare_tuple_length',len(expected),len(actual))
            if len(expected)!=len(actual):return False
            return all(equal(x,y) for x,y in zip(expected,actual))
        if type(expected) in (Source,Estimates):
            return all(equal(getattr(expected,n),getattr(actual,n)) for n in type(expected).__dataclass_fields__)
        raise AssertionError('comparison grammar')
    try:okay=equal(fresh,answer)
    except AttributeError:okay=False
    return okay,{'replay_production':receipt,'comparison':C.report()}
