#!/usr/bin/env python3
"""Research driver for rough-length unequal-block Green v14."""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import argparse
import json
import math
import time
import numpy as np

import arbitrary_block_core as core
import covariance as cov
import exact_field_certificate as field_cert


def normalized_dft(x):
    arr = np.asarray(x, dtype=np.complex128)
    return np.fft.fft(arr) / math.sqrt(arr.size)


def analytic_covariance(n: int, blocks: int) -> np.ndarray:
    """Exact unit-average formula, evaluated numerically for small checks."""
    starts, lengths, _ = core.balanced_partition(n, blocks)
    units = [a for a in range(1, n) if math.gcd(a, n) == 1]
    idx = np.arange(n)
    q = np.zeros((n, n), dtype=np.complex128)
    max_len = int(lengths.max())
    for d in range(-(max_len - 1), max_len):
        if d == 0:
            continue
        mask = np.zeros(n, dtype=np.float64)
        for start, ell in zip(starts, lengths):
            s = int(start)
            L = int(ell)
            for t in range(L):
                if 0 <= t + d < L:
                    mask[s + t] = 1.0
        if not np.any(mask):
            continue
        bmat = np.zeros((n, n), dtype=np.complex128)
        for a in units:
            v = np.exp(2j * np.pi * ((a * d) % n) * idx / n)
            bmat += np.outer(v, np.conj(v))
        bmat /= len(units)
        q += (mask[:, None] * bmat * mask[None, :]) / n
    return q


def make_cases(n: int, rng: np.random.Generator):
    j = np.arange(n, dtype=np.float64)
    out = {
        "flat": np.ones(n, dtype=np.complex128) / math.sqrt(n),
        "tone": np.exp(2j * np.pi * 7 * j / n) / math.sqrt(n),
        "spike": np.eye(1, n, 0, dtype=np.complex128).reshape(-1),
        "random_phase": np.exp(2j * np.pi * rng.random(n)) / math.sqrt(n),
    }
    g = rng.normal(size=n) + 1j * rng.normal(size=n)
    out["gaussian"] = g / np.linalg.norm(g)
    return out


def run_all(seed: int = 20261010) -> dict:
    rng = np.random.default_rng(seed)
    results: dict = {
        "metadata": {
            "name": "rough-length unequal-block Green v14",
            "seed": seed,
            "claim_scope": "randomized exact-center approximation; not exact FFT",
        }
    }

    # Decoder / recurrence equivalence.
    decoder_rows = []
    max_decoder_error = 0.0
    max_recurrence_error = 0.0
    for n in [17, 31, 61, 97, 127, 257]:
        for blocks in [3, 5, 7, 11, 16]:
            if blocks >= n:
                continue
            state = core.draw_state(n, rng)
            x = rng.normal(size=n) + 1j * rng.normal(size=n)
            got = core.one_row_estimate(x, blocks, state, "recurrence")
            direct_forcing = core.one_row_estimate(x, blocks, state, "direct")
            ref = core.reference_row(x, blocks, state)
            err = float(np.max(np.abs(got - ref)))
            rec_err = float(np.max(np.abs(got - direct_forcing)))
            max_decoder_error = max(max_decoder_error, err)
            max_recurrence_error = max(max_recurrence_error, rec_err)
            decoder_rows.append({
                "n": n,
                "blocks": blocks,
                "decoder_error": err,
                "recurrence_vs_direct_forcing": rec_err,
            })
    results["decoder_checks"] = decoder_rows

    # Covariance certificates.
    covariance_rows = []
    max_cov_ratio = 0.0
    max_old_new_ratio = 0.0
    for n in [17, 19, 23, 29, 31, 30, 35, 42, 60]:
        for blocks in [3, 4, 5, 7]:
            if blocks >= n:
                continue
            q = analytic_covariance(n, blocks)
            actual = float(np.linalg.eigvalsh(q).max().real)
            starts, lengths, _ = core.balanced_partition(n, blocks)
            new = float(cov.overlap_variance_factor_lengths(n, lengths))
            old = float(cov.old_triangle_variance_factor(n, int(lengths.max())))
            ratio = actual / new if new else 0.0
            max_cov_ratio = max(max_cov_ratio, ratio)
            max_old_new_ratio = max(max_old_new_ratio, old / new if new else 0.0)
            covariance_rows.append({
                "n": n,
                "blocks": blocks,
                "max_block_length": int(lengths.max()),
                "actual_operator_norm": actual,
                "new_overlap_bound": new,
                "old_triangle_bound": old,
                "actual_over_new": ratio,
                "old_over_new": old / new if new else 0.0,
            })
    results["covariance_checks"] = covariance_rows

    # Prime asymptotic tradeoff and bulk-output diagnostics.
    tradeoff = []
    for n in [1009, 10007, 100003, 1000003]:
        # These are primes; the final value is verified by trial factoring in tests.
        for blocks in [max(3, math.ceil(math.log2(n))),
                       max(3, math.ceil(math.log2(n) ** 2)),
                       max(3, math.ceil(math.exp(math.sqrt(math.log(n)))) )]:
            blocks = min(blocks, n)
            length = math.ceil(n / blocks)
            v = float(cov.prime_balanced_closed_form(n, blocks))
            work_proxy = n * math.log2(max(2, blocks)) + blocks * blocks
            tradeoff.append({
                "n": n,
                "blocks": blocks,
                "max_block_length": length,
                "variance_factor": v,
                "rms_factor": math.sqrt(v),
                "work_proxy": work_proxy,
                "work_over_nlogn": work_proxy / (n * math.log2(n)),
            })
    results["prime_tradeoff"] = tradeoff

    # Finite-size max-error/median diagnostics.  Diagnostic only, not proof.
    robust_rows = []
    for n in [1021, 4093]:
        cases = make_cases(n, rng)
        for blocks in [max(3, round(math.log2(n))), max(3, round(math.sqrt(n)))]:
            for row_count in [1, 5, 9]:
                states = [core.draw_state(n, rng) for _ in range(row_count)]
                for name, x in cases.items():
                    target = normalized_dft(x)
                    rows = np.stack([
                        core.one_row_estimate(x, blocks, state, "direct")
                        for state in states
                    ])
                    if row_count == 1:
                        estimate = rows[0]
                    else:
                        estimate = np.median(rows.real, axis=0) + 1j * np.median(rows.imag, axis=0)
                    robust_rows.append({
                        "n": n,
                        "blocks": blocks,
                        "rows": row_count,
                        "case": name,
                        "max_error": float(np.max(np.abs(estimate - target))),
                        "mean_square_per_output": float(np.mean(np.abs(estimate - target) ** 2)),
                    })
    results["robust_diagnostics"] = robust_rows

    exact_cases = field_cert.run_suite()
    results["finite_field_certificate"] = exact_cases

    results["summary"] = {
        "decoder_cases": len(decoder_rows),
        "max_decoder_error": max_decoder_error,
        "max_recurrence_vs_direct_forcing": max_recurrence_error,
        "covariance_cases": len(covariance_rows),
        "max_actual_covariance_over_new_bound": max_cov_ratio,
        "max_old_bound_over_new_bound": max_old_new_ratio,
        "finite_field_cases": len(exact_cases),
        "robust_diagnostic_cases": len(robust_rows),
    }
    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="results.json")
    args = parser.parse_args()
    result = run_all()
    Path(args.output).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result["summary"], indent=2))


if __name__ == "__main__":
    main()
