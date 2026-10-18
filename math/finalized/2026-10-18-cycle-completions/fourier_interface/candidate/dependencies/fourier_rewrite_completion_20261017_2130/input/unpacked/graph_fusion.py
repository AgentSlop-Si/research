"""R30: exact graph export/audit and a guarded C/Green sandwich rewrite.

The R29/Alman--Rao kernel is reused, not claimed as a new transform.
A tensor is NOT a cyclic DFT. The new rule is a classical conjugation identity.
No timing, asymptotic FFT improvement, or fixed-grid drop-in claim is implied.
"""
from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Sequence
import sys

BASE = Path(__file__).resolve().parent / 'baseline_r29'
sys.path.insert(0,str(BASE))
import recycle_tensor as r29

@dataclass(frozen=True)
class Graph:
    inputs: int
    ops: tuple
    outputs: tuple
    label: str

    def counts(self):
        c=Counter(op for op,args,k in self.ops)
        return {k:c[k] for k in ('add','neg','divide','left')}

    def evaluate(self, values: Sequence, *, bits: int|None=None):
        """Exact rational evaluation, or checked integer-grid evaluation.

        bits=None uses supplied exact int/Fraction values with rational division.
        With bits, every intermediate must be an integer in the signed range;
        this preserves exactness, and rejects unsupported fixed-grid inputs.
        Counts are incremented at executed arithmetic, not from a cost formula.
        """
        if len(values)!=self.inputs or any(type(x) not in (int,Fraction) for x in values):
            raise ValueError('complete exact real-word input required')
        if bits is not None and (type(bits)is not int or bits<2):
            raise ValueError('signed width must be at least two')
        def checked(x):
            if bits is not None:
                if type(x)is not int:raise ValueError('integer grid required')
                if not -(1<<(bits-1))<=x<(1<<(bits-1)):
                    raise OverflowError('signed intermediate overflow')
            return x
        nodes=[checked(x) for x in values];c=Counter()
        for op,args,k in self.ops:
            c[op]+=1
            a=nodes[args[0]]
            if op=='add':v=a+nodes[args[1]]
            elif op=='neg':v=-a
            elif op=='left':v=a*(1<<k)
            elif op=='divide':
                if bits is None:v=Fraction(a,1<<k)
                else:
                    if a%(1<<k):raise ValueError('inexact binary division')
                    v=a//(1<<k)
            else:raise ValueError('unsupported opcode')
            nodes.append(checked(v))
        return [nodes[j] for j in self.outputs],{k:c[k] for k in ('add','neg','divide','left')}

    def export(self):
        return {'label':self.label,'inputs':self.inputs,
                'nodes':[{'id':self.inputs+t,'op':op,'args':list(args),'shift':k}
                         for t,(op,args,k) in enumerate(self.ops)],
                'outputs':list(self.outputs),'counts':self.counts()}

    def dot(self):
        lines=['digraph arithmetic {','rankdir=LR;']
        for j in range(self.inputs):lines.append(f'v{j} [label="x{j}",shape=box];')
        for t,(op,args,k) in enumerate(self.ops):
            v=self.inputs+t;label=op+(f' {k}' if op in ('left','divide') else '')
            lines.append(f'v{v} [label="{label}"];')
            for a in args:lines.append(f'v{a} -> v{v};')
        for j,v in enumerate(self.outputs):
            lines.append(f'o{j} [label="y{j}",shape=box]; v{v} -> o{j};')
        return '\n'.join(lines+['}'])+'\n'


def _tensor_fiber(b,values,mode,inverse):
    axes=(len(values)).bit_length()-1
    if not axes:return list(values)
    sign=-1 if inverse else 1
    z=[b.phase(v,-sign*j.bit_count()) for j,v in enumerate(values)]
    re=r29._walsh(b,[v[0] for v in z],mode)
    im=r29._walsh(b,[v[1] for v in z],mode)
    half,odd=divmod(axes,2);out=[]
    for j,v in enumerate(zip(re,im)):
        x,y=b.phase(v,sign*(half-j.bit_count()))
        if odd:x,y=(b.sub(x,y),b.add(x,y)) if sign==1 else (b.add(x,y),b.sub(y,x))
        out.append((b.div(x,half+odd),b.div(y,half+odd)))
    return out


def _append_tensor(b,values,mask,mode='ar4',inverse=False):
    n=len(values);out=list(values)
    selected=[j for j in range(n.bit_length()-1) if (mask>>j)&1]
    if not selected:return out
    offsets=[sum(((t>>j)&1)<<axis for j,axis in enumerate(selected))
             for t in range(1<<len(selected))]
    for base in range(n):
        if base&mask:continue
        ids=[base|o for o in offsets]
        result=_tensor_fiber(b,[values[j] for j in ids],mode,inverse)
        for j,z in zip(ids,result):out[j]=z
    return out


def _finish(b,outputs,label):
    return Graph(b.inputs,tuple(b.ops),tuple(a for z in outputs for a in z),label)


def tensor_graph(axes, mode='ar4', inverse=False):
    if type(axes)is not int or not 0<=axes<=12:raise ValueError('axes 0..12')
    if mode not in ('ar4','ar8','walsh'):raise ValueError('known Walsh kernel')
    n=1<<axes;b=r29.Builder(n)
    outputs=_tensor_fiber(b,[(2*j,2*j+1) for j in range(n)],mode,inverse)
    return _finish(b,outputs,f'R29 {mode} C tensor {axes}, inverse={inverse}')

@dataclass(frozen=True)
class TensorNode:
    axes_mask: int
    inverse: bool=False

@dataclass(frozen=True)
class ParityGreenNode:
    parity_mask: int
    rho: int=3

@dataclass(frozen=True)
class BarrierNode:
    label: str='unknown operation / truncation'

@dataclass(frozen=True)
class FusionPlan:
    axes: int
    selected: int
    parity: int
    first_inverse: bool
    rho: int

    @property
    def xor_mask(self):return self.selected&self.parity

    def phase(self,j):
        # U^{-1} Z_v U = (-i)^wt(v&S) Z_v X_(v&S), U=C_S.
        sign=-1 if self.first_inverse else 1
        return (-sign*self.xor_mask.bit_count()+2*((j&self.parity).bit_count()&1))%4


def recognize(axes,nodes):
    """Accept only an entire exact, unobserved three-node sandwich.

    The caller must keep observable intermediate outputs as separate graph nodes;
    this function never deletes an observed branch. Unknown intervening operators
    or rounding barriers are refused, not moved through a tensor.
    """
    if type(axes)is not int or not 1<=axes<=12:raise ValueError('axes 1..12')
    if len(nodes)!=3 or not isinstance(nodes[0],TensorNode) or not isinstance(nodes[1],ParityGreenNode) or not isinstance(nodes[2],TensorNode):
        raise ValueError('exact tensor / parity-Green / inverse-tensor pattern required')
    first,mid,last=nodes;n=1<<axes
    if type(first.inverse)is not bool or type(last.inverse)is not bool or first.inverse==last.inverse:
        raise ValueError('opposite tensor directions required')
    if type(first.axes_mask)is not int or first.axes_mask!=last.axes_mask or not 0<=first.axes_mask<n:
        raise ValueError('identical legal tensor axes required')
    if type(mid.parity_mask)is not int or not 0<mid.parity_mask<n:
        raise ValueError('nonzero parity mask in address range')
    if type(mid.rho)is not int or mid.rho not in (3,-3):
        raise ValueError('this checked dyadic compiler supports rho=+/-3 only')
    return FusionPlan(axes,first.axes_mask,mid.parity_mask,first.inverse,mid.rho)


def sandwich_graph(plan,mode='ar4'):
    n=1<<plan.axes;b=r29.Builder(n);x=[(2*j,2*j+1) for j in range(n)]
    y=_append_tensor(b,x,plan.selected,mode,plan.first_inverse)
    z=[]
    for j,pair in enumerate(y):
        parity=(j&plan.parity).bit_count()&1
        # (I-rho Z_v)^{-1}: rho=3 -> -1/2 on even, 1/4 on odd.
        negative=(parity==0) if plan.rho==3 else (parity==1)
        z.append(tuple(b.neg(b.div(v,1)) if negative else b.div(v,2) for v in pair))
    out=_append_tensor(b,z,plan.selected,mode,not plan.first_inverse)
    return _finish(b,out,'unfused C/parity-Green/inverse-C')


def fused_graph(plan):
    n=1<<plan.axes;b=r29.Builder(n);x=[(2*j,2*j+1) for j in range(n)];out=[]
    for j in range(n):
        z=b.phase(x[j^plan.xor_mask],plan.phase(j))
        if plan.rho==-3:z=tuple(b.neg(v) for v in z)
        pair=[]
        for a,c in zip(x[j],z):
            three=b.add(b.left(c,1),c)
            pair.append(b.neg(b.div(b.add(a,three),3)))
        out.append(tuple(pair))
    return _finish(b,out,'fused (I+rho*M_v)/(1-rho^2)')


def linear_forms(graph):
    """Bounded exact audit, not a claimed linear-cost synthesis algorithm.

    Each row represents numerator * 2**(-exponent). Dense rows are explicit;
    auditing B positions takes superlinear storage/time and is kept offline.
    """
    n=graph.inputs
    forms=[(tuple(int(i==j) for j in range(n)),0) for i in range(n)]
    for op,args,k in graph.ops:
        v,e=forms[args[0]]
        if op=='add':
            w,f=forms[args[1]];m=max(e,f)
            v=tuple((x<<(m-e))+(y<<(m-f)) for x,y in zip(v,w));e=m
        elif op=='neg':v=tuple(-x for x in v)
        elif op=='divide':e+=k
        elif op=='left':e-=k
        nonzero=[abs(x) for x in v if x]
        if nonzero:
            t=min((x&-x).bit_length()-1 for x in nonzero)
            if t:v=tuple(x>>t for x in v);e-=t
        else:e=0
        forms.append((v,e))
    return forms


def output_matrix(graph):
    f=linear_forms(graph)
    return tuple(f[j] for j in graph.outputs)


def audit_additions(graph):
    """Find previously available proportional linear forms, exactly.

    Sign/power-of-two copies are audit matches, NOT claimed free runtime ops.
    A 'redundant add' is an addition whose whole form was already available.
    This does not optimize multi-node algebraic subgraphs or prove minimality.
    """
    forms=linear_forms(graph);seen={};duplicates=[];distinct=Counter()
    for i,(v,e) in enumerate(forms):
        nz=next((x for x in v if x),0)
        key=tuple(-x for x in v) if nz<0 else v
        op='input' if i<graph.inputs else graph.ops[i-graph.inputs][0]
        if key in seen:
            if op=='add':duplicates.append({'node':i,'prior_node':seen[key]})
        else:seen[key]=i;distinct[op]+=1
    return {'label':graph.label,'counts':graph.counts(),
            'redundant_additions':duplicates,'distinct_normalized_forms':len(seen),
            'scope':'exact reuse of already computed forms up to sign/power of two; not optimality'}


def direct_c(values,axes,selected,inverse=False):
    """Independent original 2x2 matrix action, no R29 Walsh helper."""
    x=[(Fraction(r),Fraction(i)) for r,i in values]
    sign=-1 if inverse else 1
    for bit in range(axes):
        if not selected&(1<<bit):continue
        out=x[:]
        for j in range(1<<axes):
            if j&(1<<bit):continue
            k=j^(1<<bit);ar,ai=x[j];br,bi=x[k]
            out[j]=((ar+br-sign*(ai-bi))/2,(ai+bi+sign*(ar-br))/2)
            out[k]=((ar+br+sign*(ai-bi))/2,(ai+bi-sign*(ar-br))/2)
        x=out
    return x


def direct_sandwich(values,plan):
    y=direct_c(values,plan.axes,plan.selected,plan.first_inverse)
    z=[]
    for j,pair in enumerate(y):
        denom=1-plan.rho*(-1)**((j&plan.parity).bit_count()&1)
        z.append(tuple(v/denom for v in pair))
    return direct_c(z,plan.axes,plan.selected,not plan.first_inverse)


def walsh_phase_support(axes,p=998244353,generator=3):
    n=1<<axes
    if (p-1)%(2*n):raise ValueError('required root unavailable')
    eta=pow(generator,(p-1)//(2*n),p)
    if pow(eta,n,p)!=p-1:raise ValueError('not a primitive 2N-th root')
    x=[pow(eta,j,p) for j in range(n)];h=1
    while h<n:
        for base in range(0,n,2*h):
            for j in range(h):
                a,c=x[base+j],x[base+j+h]
                x[base+j]=(a+c)%p;x[base+j+h]=(a-c)%p
        h*=2
    for v,s in enumerate(x):
        prod=1
        for h in range(axes):prod=prod*(1+(-1)**((v>>h)&1)*pow(eta,1<<h,p))%p
        if prod!=s:raise AssertionError('separate Walsh-product formula failed')
    return {'axes':axes,'N':n,'root':eta,'nonzero_Walsh_terms':sum(s!=0 for s in x),
            'independent_factor_check':True}


def graph_from_program(program):
    """Decode the ACTUAL R29 reusable-slot bytecode back into logical SSA.

    A fresh node is created on every slot write. Reusing the same physical slot
    does not incorrectly identify two different values as one graph node.
    """
    n=2*(1<<program.axes);slots={i:i for i in range(n)};ops=[]
    names=('add','neg','divide','left')
    for op,dest,ia,ib,k,free1,free2 in r29._FORMAT.iter_unpack(program.code):
        args=(slots[ia],slots[ib]) if op==0 else (slots[ia],)
        new=n+len(ops);ops.append((names[op],args,k));slots[dest]=new
        for f in (free1,free2):
            if f!=r29._NONE:slots.pop(f,None)
    return Graph(n,tuple(ops),tuple(slots[i] for i in program.outputs),
                 f'actual R29 bytecode: {program.axes} axes, {program.mode}, inverse={program.inverse}')


def structural_cse(graph):
    """Merge identical arithmetic operations, with exact local identities.

    No numerical values, tolerance tests, or cached previous inputs are consulted.
    Algebraic equality is exact. Zero-shift and double-negative nodes are removed;
    signs and shifts still needed in the resulting graph remain explicit paid ops.
    This is not a search over all equivalent arithmetic circuits.
    """
    ops=[];alias={j:j for j in range(graph.inputs)};intern={}
    for t,(op,args,k) in enumerate(graph.ops):
        args=tuple(alias[a] for a in args)
        if op=='add':args=tuple(sorted(args))
        if op in ('left','divide') and k==0:
            new=args[0]
        elif op=='neg' and args[0]>=graph.inputs and ops[args[0]-graph.inputs][0]=='neg':
            new=ops[args[0]-graph.inputs][1][0]
        else:
            key=(op,args,k)
            if key in intern:new=intern[key]
            else:
                new=graph.inputs+len(ops);ops.append(key);intern[key]=new
        alias[graph.inputs+t]=new
    outputs=tuple(alias[a] for a in graph.outputs)
    # Backwards reachable-only cleanup; all requested outputs are retained.
    live=set(outputs);needed=[]
    for t in reversed(range(len(ops))):
        node=graph.inputs+t
        if node in live:
            needed.append(t);live.update(ops[t][1])
    rename={j:j for j in range(graph.inputs)};kept=[]
    for t in reversed(needed):
        op,args,k=ops[t];rename[graph.inputs+t]=graph.inputs+len(kept)
        kept.append((op,tuple(rename[a] for a in args),k))
    return Graph(graph.inputs,tuple(kept),tuple(rename[a] for a in outputs),
                 graph.label+' [structural CSE]')


def compile_window(axes,nodes,*,observed_intermediates=()):
    """Safe public wrapper for a whole three-node graph window.

    Positions 0 and 1 denote the first tensor and middle solve outputs. When
    either is externally observed, this conservative optimizer refuses to erase
    that computation. Fan-out-aware partial rewriting is not implemented.
    """
    if observed_intermediates:
        raise ValueError('cannot erase an externally observed intermediate')
    return fused_graph(recognize(axes,nodes))
