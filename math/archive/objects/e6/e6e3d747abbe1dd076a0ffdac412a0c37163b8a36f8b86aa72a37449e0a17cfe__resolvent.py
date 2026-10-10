"""Linear-work shifted resolvent of the exact cyclic bidiagonal C."""
import sys
from pathlib import Path
from dataclasses import dataclass
from collections import Counter
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'fft_qweyl_boundary_research'))
from fixed_kernel import Counted
from operators import prepare_sparse


@dataclass
class ResolventPlan:
    sparse: object
    inverse_weights: list
    preparation: dict


def prepare_resolvent(field,n,q):
    sparse=prepare_sparse(field,n,q)
    c=Counted(field)
    weights=sparse.upper+[sparse.corner]
    prefix=[field.one]
    for w in weights:
        prefix.append(c.mul(prefix[-1],w))
    # Their product is exactly -1, so this batch inversion needs no inverse.
    inverse_product=c.neg(field.one)
    inverse_weights=[field.zero]*n
    for j in range(n-1,-1,-1):
        inverse_weights[j]=c.mul(inverse_product,prefix[j])
        if j:
            inverse_product=c.mul(inverse_product,weights[j])
    counts=Counter(sparse.preparation)
    counts.update(c.count)
    return ResolventPlan(sparse,inverse_weights,dict(counts))


def solve(field,plan,lam,x):
    """Solve (lambda I-C)y=x for any nonzero lambda, all coordinates.

The parameter-dependent preparation is charged on every call; one inversion
involves lambda**N, never any vector input. No division by lambda-q**(-i).
"""
    if lam==field.zero:
        raise ValueError('C is singular; lambda must be nonzero')
    n=plan.sparse.n
    if len(x)!=n:
        raise ValueError('wrong input length')
    parameter=Counted(field)
    a=[parameter.mul(parameter.sub(lam,u),w)
       for u,w in zip(plan.sparse.diagonal,plan.inverse_weights)]
    lam_n=lam
    for _ in range(n.bit_length()-1):
        lam_n=parameter.mul(lam_n,lam_n)
    inverse_lam_n=parameter.inv(lam_n)
    c=Counted(field)
    b=[c.neg(c.mul(v,w)) for v,w in zip(x,plan.inverse_weights)]
    affine_offset=field.zero
    for ai,bi in zip(a,b):
        affine_offset=c.add(c.mul(ai,affine_offset),bi)
    y=[c.mul(affine_offset,inverse_lam_n)]
    for j in range(n-1):
        y.append(c.add(c.mul(a[j],y[-1]),b[j]))
    total=Counter(parameter.count)
    total.update(c.count)
    return y,dict(parameter_preparation=dict(parameter.count),
                  vector_action=dict(c.count),field_operations=dict(total),
                  full_output_writes=n,
                  logical_temporary_element_writes=2*n)


def expected_preparation(n):
    l=n.bit_length()-1
    return dict(mul=4*n+l-1,sub=n-1,neg=2,constant_inverse=1)


def expected_solve(n):
    l=n.bit_length()-1
    return dict(mul=4*n+l,sub=n,constant_inverse=1,neg=n,add=2*n-1)
