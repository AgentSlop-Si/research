"""Exact cache propagation on the declared family x_j=B**j x_0.

This consumes the previous sibling package; it does not replace that package.
The reference T action is quadratic. An ordinary convolution implementation can
replace its first call, giving O(N log N+rN) work for this related-input family.
"""
import sys
from pathlib import Path
from collections import Counter

SOURCE = Path(__file__).resolve().parent.parent / 'fft_qweyl_boundary_research'
sys.path.insert(0, str(SOURCE))
from operators import prepare_sparse, apply_c_charged, horner_c
from fixed_kernel import Counted, prepare, lower_convolution


def prepare_demo(field, n, q):
    """Both methods pay these exact same two existing preparation routines."""
    sparse = prepare_sparse(field,n,q)
    kernel = prepare(field,n,q)
    counts = Counter(sparse.preparation)
    counts.update(kernel.preparation)
    return sparse,kernel,dict(counts)


def apply_b(field, sparse, x):
    if len(x) != sparse.n:
        raise ValueError('wrong input length')
    return [field.mul(sparse.upper[j],x[j+1])
            for j in range(sparse.n-1)] + [field.zero]


def apply_b_charged(field, sparse, x):
    c = Counted(field)
    out = apply_b(c,sparse,x)
    return out,dict(c.count)


def apply_t_charged(field,kernel,x):
    c = Counted(field)
    out = lower_convolution(c,kernel.kernel,x)
    return out,dict(c.count)


def chain(field,sparse,kernel,x,steps,cached):
    """Return all x_j and all y_j; storage is honestly O((steps+1)*N)."""
    if steps < 0:
        raise ValueError('negative steps')
    n=sparse.n
    y,counts=apply_t_charged(field,kernel,x)
    arithmetic=Counter(counts)
    inputs,outputs=[list(x)],[y]
    for _ in range(steps):
        x,bcounts=apply_b_charged(field,sparse,x)
        arithmetic.update(bcounts)
        if cached:
            y,details=apply_c_charged(field,sparse,y)
            arithmetic.update(details['field_operations'])
        else:
            y,tcounts=apply_t_charged(field,kernel,x)
            arithmetic.update(tcounts)
        inputs.append(x)
        outputs.append(y)
    return dict(inputs=inputs,outputs=outputs,
        field_operations=dict(arithmetic),
        logical_output_writes=(steps+1)*n,
        logical_related_input_writes=steps*n,
        retained_input_elements=(steps+1)*n,
        retained_output_elements=(steps+1)*n,
        initial_t_calls=1,subsequent_t_calls=0 if cached else steps,
        c_updates=steps if cached else 0,b_updates=steps)


def expected_online(n,steps,cached):
    if cached:
        return dict(mul=n*(n+1)//2+steps*(3*n-1),
                    add=n*(n-1)//2+steps*n)
    return dict(mul=(steps+1)*n*(n+1)//2+steps*(n-1),
                add=(steps+1)*n*(n-1)//2)


def polynomial_b(field,sparse,coefficients,x):
    if not coefficients:
        raise ValueError('nonempty coefficients required')
    c=Counted(field)
    out=[c.mul(coefficients[-1],v) for v in x]
    for coefficient in reversed(coefficients[:-1]):
        previous=apply_b(c,sparse,out)
        out=[c.add(previous[j],c.mul(coefficient,x[j]))
             for j in range(sparse.n)]
    return out,dict(c.count)


def cached_polynomial(field,sparse,coefficients,cached_tx):
    return horner_c(field,sparse,coefficients,cached_tx)
