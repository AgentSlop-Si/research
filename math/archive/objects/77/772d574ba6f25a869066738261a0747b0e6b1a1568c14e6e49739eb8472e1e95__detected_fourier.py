"""Deterministic cold Fourier evaluator for verified low-defect inputs.

Uses a majority of exact Ex_i/x_i ratios to discover a favorable shift.
The fallback handles sparse inputs. This is a conditional family evaluator,
not an algorithm accelerating arbitrary fresh dense inputs.
"""
from collections import Counter

from fourier_rational import Counted, _power, prepare_fourier_rational
from rational_reuse import solve_band


def _delta(before, after):
    return {key: after[key]-before.get(key,0) for key in after
            if after[key] != before.get(key,0)}


def _sparse_fourier(c, n, q, entries, roots=None):
    """Complete positive-sign DFT of explicit sparse entries; all gates paid."""
    steps = ([_power(c,q,j) for j,_ in entries] if roots is None
             else [roots[j] for j,_ in entries])
    terms = [value for _,value in entries]
    out = []
    for k in range(n):
        value = c.zero
        for j,term in enumerate(terms):
            value = c.add(value,term)
            if k+1 < n:
                terms[j] = c.mul(term,steps[j])
        out.append(value)
    return out


def try_detected_fourier(field,n,q,query,*,max_defects=8):
    """Return (full exact DFT, metadata), or (None, charged decline metadata).

q is a supplied primitive Nth root. Acceptance covers all inputs with at
most 2s nonzero coordinates, and all inputs for which some nonzero lambda,
lambda**N != 1, gives at most s nonzeros in (E-lambda I)query, s=max_defects.
No nonzero Fourier anchor is used. Every accepted output is freshly computed.
"""
    if (not isinstance(n,int) or isinstance(n,bool) or n<4 or n&(n-1)
            or len(query)!=n):
        raise ValueError('dyadic N>=4 and an exactly N-coordinate input required')
    if (not isinstance(max_defects,int) or isinstance(max_defects,bool)
            or max_defects<0):
        raise ValueError('max_defects must be a nonnegative integer')
    c=Counted(field)
    entries=[(i,value) for i,value in enumerate(query) if value!=field.zero]
    m=len(entries)
    stages={}
    metadata=dict(accepted=False,input_support=m,input_support_comparisons=n,
        supplied_root_order=n,paid_anchor_transform_calls=0,
        ordinary_fft_calls=0,full_output_writes=0,stages=stages)

    def decline(reason, **extra):
        metadata.update(path='declined',reason=reason,field_operations=dict(c.count),**extra)
        return None,metadata

    if m<=2*max_defects:
        result=_sparse_fourier(c,n,q,entries)
        stages['sparse_input_evaluation']=dict(c.count)
        metadata.update(accepted=True,path='sparse_input',field_operations=dict(c.count),
            phase_root_count=m,phase_roots_from_existing_table=False,
            full_output_writes=n)
        return result,metadata

    # Paid E action and q powers, shared with the eventual sparse-defect DFT.
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

    # Boyer-Moore cancellation on ratios without forming or dividing each one.
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
            balance += 1 if equal else -1
    stages['ratio_cancellation']=_delta(before,c.count)
    metadata.update(ratio_comparisons=comparisons,majority_index_steps=m,
                    candidate_balance=balance)
    if balance==0:
        return decline('no_strict_ratio_majority')

    before=dict(c.count)
    shift=c.mul(numerator,c.inv(denominator))
    metadata['detected_shift']=shift
    if shift==field.zero:
        stages['candidate_and_root_test']=_delta(before,c.count)
        return decline('zero_shift_excluded')
    if _power(c,shift,n)==field.one:
        stages['candidate_and_root_test']=_delta(before,c.count)
        return decline('root_of_unity_shift_excluded')
    stages['candidate_and_root_test']=_delta(before,c.count)

    # Candidate selection never substitutes for verifying the full residual.
    before=dict(c.count)
    defect=[c.sub(value,c.mul(shift,x)) for value,x in zip(image,query)]
    supported=[(i,value) for i,value in enumerate(defect) if value!=field.zero]
    stages['full_residual_verification']=_delta(before,c.count)
    metadata.update(defect_support=len(supported),defect_support_comparisons=n)
    if len(supported)>max_defects:
        return decline('candidate_defect_too_dense')

    # Existing solver independently prepares all its coefficients. Its duplicate
    # power work is conservatively retained and explicitly charged below.
    plan=prepare_fourier_rational(field,n,q,shift)
    stages['cold_rational_preparation']=plan.preparation
    before=dict(c.count)
    forcing=_sparse_fourier(c,n,q,supported,roots=powers)
    stages['sparse_defect_evaluation']=_delta(before,c.count)
    result,solve_count=solve_band(field,plan.target,forcing)
    stages['target_solve']=solve_count
    counts=Counter(c.count)
    counts.update(plan.preparation)
    counts.update(solve_count)
    metadata.update(accepted=True,path='detected_recurrence',field_operations=dict(counts),
        phase_root_count=len(supported),phase_roots_from_existing_table=True,
        full_output_writes=n,duplicate_solver_preparation_paid=True)
    return result,metadata
