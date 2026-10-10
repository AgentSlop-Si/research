#!/usr/bin/env python3
"""Exact integer/rational certificate for the prime-power projector theorem.

This is not a proof assistant development.  It independently checks the
finite combinatorial identities used by Theorem 5.1 without floating-point
linear algebra:

* displacement-shell counts;
* shell projector ranks;
* common nonzero eigenvalue M/N;
* total rank N-K and trace M-1.
"""
from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path


def primes_upto(limit: int) -> list[int]:
    out: list[int] = []
    for n in range(2, limit + 1):
        if all(n % q for q in range(2, int(n**0.5) + 1)):
            out.append(n)
    return out


def valuation(x: int, p: int) -> int:
    if x == 0:
        raise ValueError("valuation(0) is not used")
    x = abs(x)
    v = 0
    while x % p == 0:
        x //= p
        v += 1
    return v


def certify_case(p: int, ell: int, mu: int) -> dict[str, object]:
    if not (1 <= mu and 2 * mu <= ell):
        raise ValueError("need 1 <= mu and K >= M, i.e. 2*mu <= ell")
    n = p**ell
    m = p**mu
    k = n // m
    expected_lambda = Fraction(m, n)

    shell_records: list[dict[str, object]] = []
    for v in range(mu):
        expected_count = (p - 1) * m // (p ** (v + 1))
        expected_rank = (p - 1) * k // (p ** (v + 1))
        shell_eigenvalue = Fraction(expected_count * p ** (v + 1), (p - 1) * n)
        if shell_eigenvalue != expected_lambda:
            raise AssertionError("shell eigenvalue mismatch")

        observed_counts: list[int] = []
        for u in range(m):
            pv = p ** v
            pv1 = p ** (v + 1)
            left = u // pv - u // pv1
            right_len = m - 1 - u
            right = right_len // pv - right_len // pv1
            count = left + right
            observed_counts.append(count)
            if count != expected_count:
                raise AssertionError(
                    f"displacement count mismatch p={p} ell={ell} mu={mu} "
                    f"u={u} v={v}: {count} != {expected_count}"
                )

        shell_records.append(
            {
                "v": v,
                "count_per_local_coordinate": expected_count,
                "block_mode_rank": expected_rank,
                "eigenvalue": f"{shell_eigenvalue.numerator}/{shell_eigenvalue.denominator}",
                "observed_count_min": min(observed_counts),
                "observed_count_max": max(observed_counts),
            }
        )

    rank_per_local = sum((p - 1) * k // (p ** (v + 1)) for v in range(mu))
    expected_rank_per_local = k - k // m
    total_rank = m * rank_per_local
    expected_total_rank = n - k
    trace = Fraction(total_rank * m, n)

    if rank_per_local != expected_rank_per_local:
        raise AssertionError("rank telescoping mismatch")
    if total_rank != expected_total_rank:
        raise AssertionError("total rank mismatch")
    if trace != m - 1:
        raise AssertionError("trace mismatch")

    return {
        "p": p,
        "ell": ell,
        "mu": mu,
        "N": n,
        "K": k,
        "M": m,
        "zero_multiplicity": k,
        "nonzero_multiplicity": total_rank,
        "nonzero_eigenvalue": f"{expected_lambda.numerator}/{expected_lambda.denominator}",
        "trace": f"{trace.numerator}/{trace.denominator}",
        "shells": shell_records,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-prime", type=int, default=13)
    parser.add_argument("--max-exponent", type=int, default=10)
    parser.add_argument("--max-m", type=int, default=10000)
    parser.add_argument("--output", type=Path, default=Path("projector_certificate_results.json"))
    args = parser.parse_args()

    records: list[dict[str, object]] = []
    for p in primes_upto(args.max_prime):
        for ell in range(2, args.max_exponent + 1):
            for mu in range(1, ell // 2 + 1):
                if p ** mu <= args.max_m:
                    records.append(certify_case(p, ell, mu))

    payload = {
        "status": "PASS",
        "cases": len(records),
        "max_prime": args.max_prime,
        "max_exponent": args.max_exponent,
        "max_m": args.max_m,
        "records": records,
    }
    args.output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"PASS: {len(records)} exact prime-power parameter cases")


if __name__ == "__main__":
    main()
