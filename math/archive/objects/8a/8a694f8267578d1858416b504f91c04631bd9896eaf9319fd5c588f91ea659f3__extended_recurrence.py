"""Cold exact Fourier evaluation with direct target scans and all shifts.

The accepted class is still verified low-defect (or sparse-input) data.
No fresh arbitrary-input sub-N-log-N Fourier claim is made.
"""
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'fft_rational_reuse_research'))
from fourier_rational import Counted
from detected_fourier import _sparse_fourier, _delta

_AUTO=object()


def target_scan(c,powers,shift,forcing,query):
    """Solve (J-shift I)y=forcing, using necessary Fourier input constraints.

Precondition: forcing=F((E-shift I)query), supplied by the calling evaluator.
No source inverse or dense target matrix is formed. A scalar consistency
check enforces both cyclic endpoint equations.
"""
    n=len(powers)
    if n<4 or len(forcing)!=n or len(query)!=n:
        raise ValueError('incompatible target dimensions')
    if shift==c.zero:
        # v_i=y_(i+1); the final transition coefficient vanishes at q^N=1.
        current=c.neg(forcing[-1])
        out=[c.zero]*n
        out[1]=current
        for i in range(n-1):
            root=powers[i+1]
            current=c.sub(c.mul(c.sub(c.one,root),current),
                          c.mul(root,forcing[i]))
            out[(i+2)%n]=current
        return out,dict(branch='zero_shift_scan',missing_coordinate=None,
                        cyclic_closure_checks=0)

    y0=query[0]
    for value in query[1:]:
        y0=c.add(y0,value)
    # Every generated coordinate is p_i+h_i*y1; y0 is known from the input.
    p=[y0,c.zero]
    h=[c.zero,c.one]
    for i in range(n-1):
        root=powers[i+1]
        a=c.sub(c.one,root)
        b=c.mul(shift,root)
        p.append(c.sub(c.sub(c.mul(a,p[-1]),c.mul(b,p[-2])),
                       c.mul(root,forcing[i])))
        h.append(c.sub(c.mul(a,h[-1]),c.mul(b,h[-2])))

    first_coefficient=h[n]
    first_rhs=c.sub(y0,p[n])
    second_coefficient=c.add(c.one,c.mul(shift,h[n-1]))
    second_rhs=c.sub(c.neg(forcing[-1]),c.mul(shift,p[n-1]))
    missing_coordinate=None
    root_comparisons=0
    if first_coefficient!=c.zero:
        seed=c.mul(first_rhs,c.inv(first_coefficient))
        branch='first_cyclic_equation'
    elif second_coefficient!=c.zero:
        seed=c.mul(second_rhs,c.inv(second_coefficient))
        branch='second_cyclic_equation'
    else:
        if first_rhs!=c.zero or second_rhs!=c.zero:
            raise ValueError('inconsistent cyclic target equations')
        # h is a nonzero target null vector. Similarity implies a unique t
        # with shift=-q^t, and its inverse-Fourier t-coordinate is nonzero.
        negative_shift=c.neg(shift)
        for t,root in enumerate(powers):
            root_comparisons+=1
            if root==negative_shift:
                missing_coordinate=t
                break
        if missing_coordinate is None:
            raise ValueError('singular target has no permitted source eigenvalue')
        step=powers[(-missing_coordinate)%n]
        phase=c.one
        projected_p=projected_h=c.zero
        for i in range(n):
            projected_p=c.add(projected_p,c.mul(phase,p[i]))
            projected_h=c.add(projected_h,c.mul(phase,h[i]))
            if i+1<n:
                phase=c.mul(phase,step)
        if projected_h==c.zero:
            raise ValueError('missing-coordinate functional is unexpectedly zero')
        scalar_n=c.one
        for _ in range(n.bit_length()-1):
            scalar_n=c.add(scalar_n,scalar_n)
        required=c.mul(scalar_n,query[missing_coordinate])
        seed=c.mul(c.sub(required,projected_p),c.inv(projected_h))
        branch='singular_missing_coordinate'

    if (c.mul(first_coefficient,seed)!=first_rhs
            or c.mul(second_coefficient,seed)!=second_rhs):
        raise ValueError('inconsistent cyclic target closure')
    # The two initial coordinates are already known; all N entries are emitted.
    out=[y0,seed]
    for i in range(2,n):
        out.append(c.add(p[i],c.mul(h[i],seed)))
    return out,dict(branch=branch,missing_coordinate=missing_coordinate,
                    root_index_comparisons=root_comparisons,cyclic_closure_checks=2)


def try_extended_fourier(field,n,q,query,*,max_defects=8,shift=_AUTO):
    """Find/verify a low-defect shift, then return every exact Fourier output.

Automatic mode accepts sparse inputs or any shift with <=s defects when
m>2s, including shift zero and roots of unity. Passing a shift verifies that
    specific candidate outside the independent sparse-input fallback. Root
    validity and exact-field representation remain
supplied preconditions. Returns (None, ledger) on an ordinary dense decline.
"""
    if (not isinstance(n,int) or isinstance(n,bool) or n<4 or n&(n-1)
            or len(query)!=n):
        raise ValueError('dyadic N>=4 and exactly N input coordinates required')
    if (not isinstance(max_defects,int) or isinstance(max_defects,bool)
            or max_defects<0):
        raise ValueError('max_defects must be a nonnegative integer')
    c=Counted(field)
    entries=[(i,value) for i,value in enumerate(query) if value!=field.zero]
    stages={}
    automatic=shift is _AUTO
    metadata=dict(accepted=False,input_support=len(entries),input_support_comparisons=n,
        automatic_shift=automatic,full_output_writes=0,ordinary_fft_calls=0,
        anchor_transform_calls=0,stages=stages)
    def decline(reason):
        metadata.update(reason=reason,path='declined',field_operations=dict(c.count))
        return None,metadata
    if len(entries)<=2*max_defects:
        out=_sparse_fourier(c,n,q,entries)
        stages['sparse_input_evaluation']=dict(c.count)
        metadata.update(accepted=True,path='sparse_input',field_operations=dict(c.count),
                        full_output_writes=n)
        return out,metadata

    powers=[field.one]
    for _ in range(1,n):
        powers.append(c.mul(powers[-1],q))
    image=[]
    for i in range(n):
        value=query[i]
        if i+1<n:
            value=c.add(value,c.mul(c.sub(powers[i+1],field.one),query[i+1]))
        image.append(c.neg(c.mul(powers[i],value)))
    stages['root_powers_and_E_action']=dict(c.count)
    if automatic:
        before=dict(c.count)
        balance=0
        numerator=denominator=None
        comparisons=0
        for i,value in entries:
            if balance==0:
                numerator,denominator=image[i],value
                balance=1
            else:
                equal=c.mul(image[i],denominator)==c.mul(numerator,value)
                comparisons+=1
                balance+=1 if equal else -1
        stages['ratio_cancellation']=_delta(before,c.count)
        metadata.update(ratio_comparisons=comparisons,majority_index_steps=len(entries),
                        candidate_balance=balance)
        if balance==0:
            return decline('no_strict_ratio_majority')
        before=dict(c.count)
        shift=field.zero if numerator==field.zero else c.mul(numerator,c.inv(denominator))
        stages['candidate_formation']=_delta(before,c.count)
    metadata['shift']=shift
    before=dict(c.count)
    defect=(list(image) if shift==field.zero else
            [c.sub(value,c.mul(shift,x)) for value,x in zip(image,query)])
    supported=[(i,value) for i,value in enumerate(defect) if value!=field.zero]
    stages['full_residual_verification']=_delta(before,c.count)
    metadata.update(defect_support=len(supported),defect_support_comparisons=n)
    if len(supported)>max_defects:
        return decline('candidate_defect_too_dense')
    before=dict(c.count)
    forcing=_sparse_fourier(c,n,q,supported,roots=powers)
    stages['sparse_defect_evaluation']=_delta(before,c.count)
    before=dict(c.count)
    out,target=target_scan(c,powers,shift,forcing,query)
    stages['direct_target_scan']=_delta(before,c.count)
    metadata.update(accepted=True,path='recurrence',target=target,
                    field_operations=dict(c.count),full_output_writes=n)
    return out,metadata
