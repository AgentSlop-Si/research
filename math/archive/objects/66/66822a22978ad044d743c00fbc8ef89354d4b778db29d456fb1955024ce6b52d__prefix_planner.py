"""Deterministic linear selection and full-prefix Fourier-surrogate planner.

Algorithmic bounds use the corrected source's ideal arithmetic model.
Python floats, logarithms, random bits and downstream FFTs are not a certified
implementation of that probability theorem. Prefix sums of computed float
magnitudes use exact Fractions to avoid subtractive-cancellation decisions.
"""
from dataclasses import dataclass
from fractions import Fraction
import math
import random


def _parameters(epsilon, delta):
    try:
        epsilon, delta = float(epsilon), float(delta)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError('epsilon and delta must be finite numeric parameters') from exc
    if not (math.isfinite(epsilon) and 0 < epsilon < 1 and
            math.isfinite(delta) and 0 < delta < 1):
        raise ValueError('epsilon and delta must be finite and strictly between 0 and 1')
    return epsilon, delta


def _snapshot(values):
    try:
        x = tuple(complex(v) for v in values)
    except (TypeError, ValueError) as exc:
        raise ValueError('need a one-dimensional complex sequence') from exc
    n = len(x)
    if not n or n & (n-1):
        raise ValueError('input length must be a positive power of two')
    if any(not (math.isfinite(v.real) and math.isfinite(v.imag)) for v in x):
        raise ValueError('input values must be finite')
    return x


def _small_sort(values, keys, stats):
    out = list(values)
    for i in range(1, len(out)):
        item, j = out[i], i
        while j:
            stats['selection_comparisons'] += 1
            if not keys[item] < keys[out[j-1]]:
                break
            out[j] = out[j-1]
            j -= 1
        out[j] = item
    return out


def _select(values, rank, keys, stats):
    """BFPRT median-of-five selection; keys include unique index tie-breaks."""
    stats['selection_calls'] += 1
    stats['selection_partition_volume'] += len(values)
    if len(values) <= 5:
        return _small_sort(values, keys, stats)[rank]
    medians = []
    for start in range(0, len(values), 5):
        group = _small_sort(values[start:start+5], keys, stats)
        medians.append(group[len(group)//2])
    pivot = _select(medians, len(medians)//2, keys, stats)
    lower, upper = [], []
    for item in values:
        stats['selection_comparisons'] += 1
        if keys[item] < keys[pivot]:
            lower.append(item)
        else:
            stats['selection_comparisons'] += 1
            if keys[pivot] < keys[item]:
                upper.append(item)
    if rank < len(lower):
        return _select(lower, rank, keys, stats)
    if rank == len(lower):
        return pivot
    return _select(upper, rank-len(lower)-1, keys, stats)


@dataclass(frozen=True)
class Candidate:
    head_size: int
    residual_mass: Fraction
    requested_samples: int
    actual_draws_if_chosen: int
    support_upper_bound: int
    method: str


@dataclass(frozen=True)
class PrefixPlan:
    version: str
    snapshot: tuple
    epsilon: float
    delta: float
    cap: int
    magnitude_fractions: tuple
    magnitudes: tuple
    total_mass: Fraction
    nonzero_indices: tuple
    ordered_top_indices: tuple
    prefix_masses: tuple
    candidates: tuple
    chosen: Candidate
    lambda_numeric: float
    selection_stats: tuple


def _candidate(m, s, total, prefix, epsilon, budget_factor):
    residual = total-prefix
    if total == 0 or residual <= Fraction(epsilon)*total:
        requested = 0
    else:
        raw = budget_factor*residual*residual/(total*total)
        requested = -(-raw.numerator//raw.denominator)
    if s+requested >= m:
        return Candidate(s,residual,requested,0,m,'exact-input')
    if requested == 0:
        return Candidate(s,residual,0,0,s,'head-only')
    return Candidate(s,residual,requested,requested,s+requested,'sample-tail')


def plan_prefix(values, epsilon, delta, *, max_head=None):
    epsilon, delta = _parameters(epsilon,delta)
    x = _snapshot(values)
    n = len(x)
    if max_head is not None and (not isinstance(max_head,int) or
                                 isinstance(max_head,bool) or max_head < 0):
        raise ValueError('max_head must be a nonnegative integer or None')
    magnitudes = tuple(math.hypot(v.real,v.imag) for v in x)
    if any(not math.isfinite(a) for a in magnitudes):
        raise OverflowError('a complex magnitude is outside the floating-point range')
    masses = tuple(Fraction(a) for a in magnitudes)
    total = sum(masses,Fraction(0))
    nonzero = tuple(j for j,a in enumerate(magnitudes) if a != 0)
    m = len(nonzero)
    requested_cap = max(1,(n.bit_length()-1)**2) if max_head is None else max_head
    cap = min(m,requested_cap)
    keys = tuple((-a,j) for j,a in enumerate(magnitudes))
    stats = {'selection_calls':0,'selection_partition_volume':0,
             'selection_comparisons':0,'input_values_scanned':n,
             'selected_indices':cap,'candidate_count':cap+1}
    if cap == 0:
        top = []
    elif cap == m:
        top = list(nonzero)
    else:
        cut = _select(list(nonzero),cap-1,keys,stats)
        top = []
        for j in nonzero:
            stats['selection_comparisons'] += 1
            if keys[j] <= keys[cut]:
                top.append(j)
    top.sort(key=lambda j: keys[j])
    assert len(top) == cap
    prefix = [Fraction(0)]
    for j in top:
        prefix.append(prefix[-1]+masses[j])
    # Logs are evaluated without forming 4N/delta, which can overflow.
    logarithm = math.log(4*n)-math.log(delta)
    factor = 4*Fraction(logarithm)/(Fraction(epsilon)**2)
    candidates = tuple(_candidate(m,s,total,prefix[s],epsilon,factor)
                       for s in range(cap+1))
    chosen = min(candidates,key=lambda c:(c.support_upper_bound,
                        c.actual_draws_if_chosen,c.head_size))
    return PrefixPlan('full-prefix-v1',x,epsilon,delta,cap,masses,magnitudes,total,
        nonzero,tuple(top),tuple(prefix),candidates,chosen,logarithm,
        tuple(sorted(stats.items())))


def construct_surrogate(values, epsilon, delta, *, plan, rng=None):
    """Validate binding, then copy or sample. Exact bypass occurs before RNG use.

    Returns sparse entries and clearly separated construction metadata.
    Sorted uniforms and one residual scan avoid a hash/coalescing assumption.
    """
    epsilon, delta = _parameters(epsilon,delta)
    x = _snapshot(values)
    if not isinstance(plan,PrefixPlan) or plan.version != 'full-prefix-v1':
        raise ValueError('unsupported plan')
    if plan.snapshot != x or plan.epsilon != epsilon or plan.delta != delta:
        raise ValueError('stale plan: input or requested parameters differ')
    chosen = plan.chosen
    info = {'method':chosen.method,'head_size':chosen.head_size,
            'requested_samples':chosen.requested_samples,'actual_draws':0,
            'copied_nonzeros':0,'sampled_distinct_indices':0,
            'support_upper_bound':chosen.support_upper_bound,
            'realized_support':0,'input_binding_values_checked':len(x),
            'reused_selected_indices':True,'selection_calls_during_construction':0}
    if chosen.method == 'exact-input':
        entries = [(j,x[j]) for j in plan.nonzero_indices]
        info['copied_nonzeros'] = len(entries)
        info['realized_support'] = len(entries)
        return entries,info
    head = plan.ordered_top_indices[:chosen.head_size]
    entries = [(j,x[j]) for j in head]
    info['copied_nonzeros'] = len(head)
    if chosen.method == 'head-only':
        info['realized_support'] = len(entries)
        return entries,info
    k = chosen.requested_samples
    assert 0 < k and chosen.head_size+k < len(plan.nonzero_indices)
    if rng is None:
        rng = random.Random()
    uniforms = sorted(float(rng.random()) for _ in range(k))
    if any(not (0 <= u < 1) for u in uniforms):
        raise ValueError('random generator must supply values in [0,1)')
    targets = [Fraction(u)*chosen.residual_mass for u in uniforms]
    selected = [False]*len(x)
    for j in head:
        selected[j] = True
    cumulative, cursor = Fraction(0),0
    for j in plan.nonzero_indices:
        if selected[j]:
            continue
        cumulative += plan.magnitude_fractions[j]
        count = 0
        while cursor < k and targets[cursor] < cumulative:
            cursor += 1
            count += 1
        if count:
            magnitude = float(chosen.residual_mass*count/k)
            phase = complex(x[j].real/plan.magnitudes[j],x[j].imag/plan.magnitudes[j])
            value = magnitude*phase
            if not (math.isfinite(value.real) and math.isfinite(value.imag)):
                raise OverflowError('sampled coefficient is outside the floating-point range')
            info['sampled_distinct_indices'] += 1
            if value != 0:
                entries.append((j,value))
    assert cursor == k and cumulative == chosen.residual_mass
    info['actual_draws'] = k
    info['realized_support'] = len(entries)
    info['sorted_uniform_count'] = k
    info['residual_scan_nonzeros'] = len(plan.nonzero_indices)-len(head)
    assert len(entries) <= chosen.support_upper_bound
    return entries,info
