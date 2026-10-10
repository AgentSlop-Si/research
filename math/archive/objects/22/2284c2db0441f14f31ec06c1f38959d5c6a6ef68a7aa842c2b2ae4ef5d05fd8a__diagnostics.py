"""Small reproducible numerical and reclamation diagnostics, not a sweep."""
import json
from pathlib import Path
import statistics
import time
import numpy as np
from coalesced_projected import CoalescedProjectedFourier, modular_phase
from vendor.projected_fourier import ProjectedFourierState


def main():
    result = {}
    p = np.ones((2, 1), complex)
    c = [1e16, -1e16]
    old = ProjectedFourierState(1, [0], p, c)
    new = CoalescedProjectedFourier(1, [0], p, c)
    old.add_coefficient(0, 1)
    new.add_coefficient(0, 1)
    result["sub_ulp_no_op"] = dict(represented_state_fft=0., original=float(old.query()[0].real), coalesced=float(new.query()[0].real))
    new = CoalescedProjectedFourier(1, [0], np.ones((1, 1)), [1e16])
    new.add_coefficient(0, -1e16)
    new.add_coefficient(0, 1)
    result["snapshot_subtraction_cancellation"] = dict(represented_state_fft=1., coalesced=float(new.query()[0].real), explicit_rebase=float(new.rebase()[0].real))
    n = 1 << 20
    bins = np.array([n-1, n-2, n//2])
    dense = np.zeros(n, complex)
    dense[-1] = 1
    expected = np.fft.fft(dense)[bins]
    unreduced = np.exp((-2j*np.pi*(n-1)/n)*bins.astype(float))
    reduced = modular_phase(n, bins, n-1)
    result["high_index_phase"] = dict(n=n, j=n-1, bins=bins.tolist(),
        original_max_abs_error=float(np.max(np.abs(unreduced-expected))),
        reduced_max_abs_error=float(np.max(np.abs(reduced-expected))))
    rng = np.random.default_rng(9911)
    basis = rng.normal(size=(4, 64)) + 1j*rng.normal(size=(4, 64))
    bins = np.array([0, 1, 2, 11, 31, 32, 61, 63])
    state = CoalescedProjectedFourier(64, bins, np.fft.fft(basis)[:, bins])
    max_error = 0.
    for t in range(20000):
        state.add_coefficient(t % 4, complex(*rng.normal(size=2)))
        answer = state.query()
        expected = np.fft.fft(state.coefficients @ basis)[bins]
        max_error = max(max_error, float(np.max(np.abs(answer-expected))))
    result["long_incremental_drift"] = dict(queries=20000, max_abs_error=max_error,
        final_abs_error=float(np.max(np.abs(answer-expected))),
        rebased_abs_error=float(np.max(np.abs(state.rebase()-expected))))
    # Isolate the u-dependent rebuild/clear tail. Fabricated pending snapshots
    # describe u previously-nonzero points, all now zero: r=k=0 and q=1.
    # Construction and dict population are excluded ONLY in this diagnostic,
    # explicitly unlike the full-stream end-to-end benchmark.
    rows = []
    for u in (64, 1024, 8192):
        samples = []
        for _ in range(51):
            state = CoalescedProjectedFourier(8192, [0], np.empty((0, 1)))
            state.pending = {("p", j): complex(j+1, -0.25) for j in range(u)}
            begin = time.perf_counter_ns()
            state.query()
            samples.append(time.perf_counter_ns()-begin)
        rows.append(dict(u=u, q=1, r=0, k=0, median_query_ns=statistics.median(samples), raw_ns=samples))
    result["reclamation_diagnostic"] = rows
    Path("results/diagnostics.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({k: v for k, v in result.items() if k != "reclamation_diagnostic"}, indent=2))
    print("Rebuild/clear median microseconds:", [(r["u"], r["median_query_ns"]/1000) for r in rows])


if __name__ == "__main__":
    main()
