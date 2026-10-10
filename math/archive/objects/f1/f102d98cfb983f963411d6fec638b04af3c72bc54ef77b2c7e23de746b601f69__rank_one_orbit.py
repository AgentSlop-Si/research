"""Fused Q-modulated highest-power corrections via classical pruned FFTs.

Computes sum_j c_j Q**j C**(N-1) Q**j x, with all N outputs.
O(N(1+log s)) for s supplied coefficients, O(N) cold preparation.
This is a rank-s restricted family, not a faster complete H_q(C) evaluator.
"""
from dataclasses import dataclass
from collections import Counter
from operator import index
from fused_modulated import Counted,FFTPlan,fft
from fixed_kernel import prepare


@dataclass
class OrbitPlan:
    n: int
    count: int
    rounded: int
    roots: list
    coefficients: list
    left: list
    right: list
    leaf: object
    preparation: dict


def prepare_orbit(field,n,q,coefficients):
    if not coefficients or len(coefficients)>n:
        raise ValueError('1..N coefficients required')
    kernel=prepare(field,n,q)
    c=Counted(field)
    roots=[field.one]
    for _ in range(1,n):
        roots.append(c.mul(roots[-1],q))
    # g_(N-1)=N/q; f_(N-1)=N. No independent input-dependent inversion.
    last_g=c.mul(kernel.factorial[-1],roots[-1])
    right=[c.mul(last_g,a) for a in reversed(kernel.middle)]
    rounded=1<<(len(coefficients)-1).bit_length()
    permutation=[0]
    while len(permutation)<rounded:
        doubled=[2*j for j in permutation]
        permutation=doubled+[j+1 for j in doubled]
    leaf=None if rounded==1 else FFTPlan(rounded//2,
        roots[::n//rounded],permutation,field.zero,field.zero)
    counts=Counter(kernel.preparation);counts.update(c.count)
    return OrbitPlan(n,len(coefficients),rounded,roots,list(coefficients),
                     kernel.kernel,right,leaf,dict(counts))


def partial_forward(c,plan,x):
    """First R Fourier coefficients, R the dyadic rounded requested count."""
    n,r=plan.n,plan.rounded
    def visit(start,stride,size):
        if size==r:
            values=[x[start+stride*k] for k in range(r)]
            return values if r==1 else fft(c,plan.leaf,values)
        even=visit(start,2*stride,size//2)
        odd=visit(start+stride,2*stride,size//2)
        return [c.add(a,c.mul(plan.roots[k*(n//size)],b))
                for k,(a,b) in enumerate(zip(even,odd))]
    return visit(0,1,n)


def partial_transpose(c,plan,coefficients):
    """Transpose (not conjugate transpose) of partial_forward, all N outputs."""
    n,r=plan.n,plan.rounded
    if len(coefficients)!=r:
        raise ValueError('R coefficients required')
    out=[c.zero]*n
    def visit(start,stride,size,values):
        if size==r:
            result=values if r==1 else fft(c,plan.leaf,values)
            for k,a in enumerate(result):
                out[start+stride*k]=a
            return
        right=[c.mul(plan.roots[k*(n//size)],a) for k,a in enumerate(values)]
        visit(start,2*stride,size//2,values)
        visit(start+stride,2*stride,size//2,right)
    visit(0,1,n,coefficients)
    return out


def apply_orbit(field,plan,x):
    if len(x)!=plan.n:
        raise ValueError('wrong input length')
    c=Counted(field)
    scaled=[c.mul(a,b) for a,b in zip(plan.right,x)]
    spectrum=partial_forward(c,plan,scaled)
    weighted=[c.mul(a,b) for a,b in zip(plan.coefficients,spectrum)]
    weighted += [field.zero]*(plan.rounded-plan.count)
    decoded=partial_transpose(c,plan,weighted)
    out=[c.mul(a,b) for a,b in zip(plan.left,decoded)]
    return out,dict(field_operations=dict(c.count),
        partial_frequency_count=plan.rounded,requested_frequency_count=plan.count,
        leaf_fft_length=plan.rounded,leaf_fft_calls=0 if plan.rounded==1 else 2*plan.n//plan.rounded,
        full_output_terms_materialized=0,full_output_writes=plan.n,
        returned_output_count=plan.n,input_coordinate_reads=plan.n,
        graph='one pruned partial FFT and its exact transposed graph')


def expected_preparation(n):
    l=n.bit_length()-1
    return dict(mul=8*n+l-4,sub=n-1,neg=n-1,constant_inverse=1)


def expected_online(n,s):
    r=1<<(s-1).bit_length()
    f=n*(r.bit_length()-1)
    out=dict(mul=f+4*n-2*r+s,add=f+n-r)
    if f:
        out['sub']=f
    return out


@dataclass
class ModePlan:
    base: OrbitPlan
    modes: list
    scaled_left: list
    single_weights: object
    preparation: dict


def prepare_modes(field,n,q,modes):
    """Input is t pairs (a,gamma), describing c_j=sum gamma*q**(a*j).

The N individual c_j are never expanded. Duplicate indices are allowed and
their work is conservatively retained. A single-mode specialization stores
its weighted permutation directly, with its extra preparation charged.
"""
    if n<2 or n&(n-1):
        raise ValueError('N must be a power of two at least 2')
    if not modes:
        raise ValueError('at least one Fourier-description mode required')
    normalized=[]
    for a,gamma in modes:
        if isinstance(a,bool):
            raise TypeError('Fourier mode indices must be integers, not booleans')
        normalized.append((index(a)%n,gamma))
    base=prepare_orbit(field,n,q,[field.one])
    c=Counted(field)
    scaled_left=[c.mul(c.integer(n),a) for a in base.left]
    single=None
    if len(normalized)==1:
        a,gamma=normalized[0]
        single=[c.mul(c.mul(value,gamma),base.right[(-i-a)%n])
                for i,value in enumerate(scaled_left)]
    counts=Counter(base.preparation);counts.update(c.count)
    return ModePlan(base,normalized,scaled_left,single,dict(counts))


def apply_modes(field,plan,x):
    n=plan.base.n
    if len(x)!=n:
        raise ValueError('wrong input length')
    c=Counted(field)
    if plan.single_weights is not None:
        a,_=plan.modes[0]
        out=[c.mul(value,x[(-i-a)%n]) for i,value in enumerate(plan.single_weights)]
    else:
        scaled=[c.mul(a,b) for a,b in zip(plan.base.right,x)]
        out=[]
        first,coefficient=plan.modes[0]
        for i,left in enumerate(plan.scaled_left):
            value=c.mul(coefficient,scaled[(-i-first)%n])
            for mode,gamma in plan.modes[1:]:
                value=c.add(value,c.mul(gamma,scaled[(-i-mode)%n]))
            out.append(c.mul(left,value))
    return out,dict(field_operations=dict(c.count),description_mode_count=len(plan.modes),
        expanded_orbit_weight_count=0,full_output_terms_materialized=0,
        full_output_writes=n,returned_output_count=n,
        input_coordinate_reads=n if len(plan.modes)==1 else n,
        transform_calls=0)


def expected_modes_preparation(n,t):
    out=Counter(expected_preparation(n))
    out.update(mul=3*n if t==1 else n)
    return dict(out)


def expected_modes_online(n,t):
    if t==1:
        return dict(mul=n)
    return dict(mul=(t+2)*n,add=(t-1)*n)
