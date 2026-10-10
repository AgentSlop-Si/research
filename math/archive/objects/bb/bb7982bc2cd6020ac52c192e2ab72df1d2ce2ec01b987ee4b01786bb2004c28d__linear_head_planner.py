"""Single-selection numerical planner; supplied v2 source stays unchanged.

With largest candidate H and J candidates, planning takes O(N+H log H+J)
under the same linear-selection model as the source. For its default
H=O(log^2 N), this is O(N). Floating error remains uncertified.
"""
import math
import numpy as np
from sparse_surrogate import (
    HeadTailPlan, _as_complex_vector, head_tail_sample_count_from_norms,
    make_head_tail_plan, approximate_dft_all_head_tail,
)


def linear_plan_head_tail(x, epsilon, delta, *, candidates=None, max_head=None):
    a = _as_complex_vector(x)
    n = a.size
    if not 0 < float(epsilon) < 1 or not 0 < float(delta) < 1:
        raise ValueError('epsilon and delta must lie in (0,1)')
    if candidates is None:
        h = (min(n, max(1, math.ceil(math.log2(max(2, n))**2)))
             if max_head is None else min(n, max(0, int(max_head))))
        candidates = [0]
        p = 1
        while p < h:
            candidates.append(p)
            p *= 2
        candidates.append(h)
    candidates = sorted({int(s) for s in candidates if 0 <= int(s) <= n})
    if not candidates:
        raise ValueError('no valid head candidates')
    h = max(candidates)
    mag = np.abs(a)
    total = float(np.sum(mag))
    nnz = int(np.count_nonzero(a))
    if h == 0:
        top = np.empty(0, dtype=np.intp)
    elif h == n:
        top = np.arange(n)
    else:
        top = np.argpartition(mag, n-h)[n-h:]
    top = top[np.argsort(mag[top])[::-1]]
    mass = np.r_[0.0, np.cumsum(mag[top])]
    nonzero = np.r_[0, np.cumsum(mag[top] != 0)]
    plans = []
    for s in candidates:
        head_l1 = float(mass[s])
        tail_l1 = max(0.0, total-head_l1)
        tail_nnz = nnz-int(nonzero[s])
        k = head_tail_sample_count_from_norms(n, total, tail_l1,
                                              epsilon, delta) if total else 0
        if tail_nnz <= k:
            method, support, k = 'exact-tail', s+tail_nnz, tail_nnz
        elif k == 0:
            method, support = 'head-only', s
        else:
            method, support = 'sample-tail', s+k
        plans.append(HeadTailPlan(n, float(epsilon), float(delta), s,
            head_l1, tail_l1, total, tail_l1/total if total else 0.0,
            k, tail_nnz, min(n, support), method))
    return min(plans, key=lambda p: (p.support_upper_bound,
                                    p.requested_samples, p.head_size))


def apply_refreshed_head_plan(x, epsilon, delta, *, plan, **kwargs):
    """Treat a supplied plan as a head-size hint, never as input-independent data.

    Recomputing its masses/support/budget costs O(N), matching the mandatory
    input scan. It also applies the currently requested epsilon and delta.
    """
    refreshed = make_head_tail_plan(x, epsilon, delta, plan.head_size)
    return approximate_dft_all_head_tail(x, epsilon, delta,
                                         plan=refreshed, **kwargs)
