from pathlib import Path
import json
import numpy as np
import sparse_surrogate as source
from linear_head_planner import linear_plan_head_tail, apply_refreshed_head_plan


def main():
    rng = np.random.default_rng(901)
    comparisons = 0
    for n in [1, 8, 64, 1024]:
        inputs = [np.zeros(n), np.ones(n),
                  rng.normal(size=n)+1j*rng.normal(size=n),
                  np.exp(-.2*np.arange(n)).astype(complex)]
        for x in inputs:
            a = source.plan_head_tail(x, .2, .05)
            b = linear_plan_head_tail(x, .2, .05)
            assert (a.head_size, a.requested_samples, a.method) == (
                    b.head_size, b.requested_samples, b.method)
            assert a.support_upper_bound == b.support_upper_bound
            comparisons += 1
    n = 1024
    spike = np.full(n, 1e-5, dtype=complex)
    spike[0] = 10
    stale = source.make_head_tail_plan(spike, .01, .05, 1)
    flat = np.ones(n, dtype=complex)
    bad = source.approximate_dft_all_head_tail(flat, .01, .05, plan=stale)
    good = apply_refreshed_head_plan(flat, .01, .05, plan=stale)
    ref = np.fft.fft(flat, norm='ortho')
    target = .01*np.sqrt(n)
    bad_ratio = float(np.max(np.abs(bad-ref))/target)
    good_ratio = float(np.max(np.abs(good-ref))/target)
    assert bad_ratio > 99 and good_ratio < 1e-10
    # Count full-vector selections, independently of wall-clock noise.
    real_partition = np.argpartition
    counts = {}
    try:
        for label, function in [('source', source.plan_head_tail),
                                ('single_selection', linear_plan_head_tail)]:
            calls = [0]
            def counted(*args, **kwargs):
                calls[0] += 1
                return real_partition(*args, **kwargs)
            np.argpartition = counted
            function(np.ones(65536), .18, .02)
            counts[label] = calls[0]
    finally:
        np.argpartition = real_partition
    assert counts['single_selection'] == 1 < counts['source']
    result = {'status': 'PASS', 'planner_comparisons': comparisons,
        'same_length_stale_plan_error_over_target': bad_ratio,
        'refreshed_plan_error_over_target': good_ratio,
        'argpartition_calls_n65536': counts,
        'scope': 'Focused numerical regressions and actual selection-call count; no exact-complex or certified-roundoff claim.'}
    Path(__file__).with_name('checks.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
