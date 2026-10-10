"""Exact reversible family reuse for the complete H_q(C) operator."""
from dataclasses import dataclass
from collections import Counter
from fast_hc import Counted,apply_hc


@dataclass
class CovariancePlan:
    fast: object
    weights: list
    preparation: dict


def prepare_covariance(field,fast):
    c=Counted(field)
    n=len(fast.t)
    weights=[c.sub(field.one,fast.forward.powers[j+1]) for j in range(n-1)]
    weights.append(fast.kernel.fft.inverse_n)
    return CovariancePlan(fast,weights,dict(c.count))


def apply_s(field,plan,x):
    """S=(I-A)^-1 Q: weighted prefix sums, N mul and N-1 add."""
    n=len(plan.weights)
    if len(x)!=n:
        raise ValueError('wrong length')
    c=Counted(field)
    out=[c.mul(plan.fast.forward.powers[0],x[0])]
    for j in range(1,n):
        out.append(c.add(out[-1],c.mul(plan.fast.forward.powers[j],x[j])))
    return out,dict(c.count)


def apply_k(field,plan,x):
    """K=-QB+(1/N)A^(N-1): weighted cyclic shift, exactly N mul."""
    n=len(plan.weights)
    if len(x)!=n:
        raise ValueError('wrong length')
    c=Counted(field)
    out=[c.mul(plan.weights[j],x[(j+1)%n]) for j in range(n)]
    return out,dict(c.count)


def chain(field,plan,x,steps,cached):
    """Return all exact H(C) outputs on S**j*x; input updates fully paid."""
    if steps<0:
        raise ValueError('negative steps')
    y,detail=apply_hc(field,plan.fast,x)
    counts=Counter(detail['field_operations'])
    inputs,outputs=[list(x)],[y]
    for _ in range(steps):
        x,cost=apply_s(field,plan,x)
        counts.update(cost)
        if cached:
            y,cost=apply_k(field,plan,y)
            counts.update(cost)
        else:
            y,detail=apply_hc(field,plan.fast,x)
            counts.update(detail['field_operations'])
        inputs.append(x)
        outputs.append(y)
    return dict(inputs=inputs,outputs=outputs,field_operations=dict(counts),
        full_output_writes=(steps+1)*len(x),related_input_writes=steps*len(x),
        retained_field_elements=2*(steps+1)*len(x))
