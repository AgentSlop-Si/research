from __future__ import annotations

import csv
import hashlib
import json
import random
import subprocess
import sys
import unittest
from pathlib import Path
from time import perf_counter

from finite_field import field_for_length, matrix_inverse
from krylov_gate import (
    cycle_denominator,
    directed_diameter,
    max_outdegree,
    minimal_inverse_polynomial_degree,
    multishift_denominator,
    support_radius_gate,
)
from weyl_packet import (
    affine_fourier_minor,
    character_packet_apply,
    literal_character_packet_apply,
    packet_fiber_minor,
)

ROOT = Path(__file__).resolve().parent


def choose_alpha(n: int, p: int) -> int:
    alpha = 2
    while pow(alpha, n, p) == 1:
        alpha += 1
    return alpha


def benchmark_packets():
    rows = []
    for n in (31, 61, 127, 251):
        p, omega = field_for_length(n)
        alpha = choose_alpha(n, p)
        x = [(17 * j * j + 5 * j + 3) % p for j in range(n)]
        s = n // 3
        repeats = 5 if n <= 127 else 3
        t0 = perf_counter()
        for _ in range(repeats):
            fast = character_packet_apply(x, p, omega, alpha, s)
        fast_seconds = (perf_counter() - t0) / repeats
        t0 = perf_counter()
        for _ in range(repeats):
            literal = literal_character_packet_apply(x, p, omega, alpha, s)
        literal_seconds = (perf_counter() - t0) / repeats
        assert fast == literal
        rows.append(
            {
                "N": n,
                "field": p,
                "fast_seconds": fast_seconds,
                "literal_seconds": literal_seconds,
                "speedup": literal_seconds / fast_seconds,
            }
        )
    with (ROOT / "benchmark_results.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    return rows


def exact_results():
    rng = random.Random(20261010)
    packet_cases = []
    for n in (5, 7, 11, 13, 17, 19):
        p, omega = field_for_length(n)
        alpha = choose_alpha(n, p)
        weights = [rng.randrange(p) for _ in range(n)]
        for h in (1, 2):
            det, indices = packet_fiber_minor(weights, p, omega, alpha, h)
            fdet = affine_fourier_minor(
                n,
                p,
                omega,
                indices,
                row_slope=2 % n,
                row_shift=1,
                col_slope=3 % n if n != 3 else 1,
                col_shift=2,
            )
            packet_cases.append(
                {
                    "N": n,
                    "field": p,
                    "h": h,
                    "packet_minor": det,
                    "affine_fourier_minor": fdet,
                    "indices": list(indices),
                }
            )

    krylov_cases = []
    p = 1009
    for n, shifts, weights in [
        (7, [1], [2]),
        (11, [1], [2]),
        (13, [1, 2], [3, 7]),
        (17, [1, 4], [2, 9]),
    ]:
        a = multishift_denominator(n, p, shifts, weights)
        inverse = matrix_inverse(a, p)
        info = support_radius_gate(a, inverse)
        degree = minimal_inverse_polynomial_degree(a, p)
        krylov_cases.append(
            {
                "N": n,
                "shifts": shifts,
                "weights": weights,
                "directed_diameter": info["directed_diameter"],
                "max_outdegree": info["max_outdegree"],
                "size_lower_bound": info["size_lower_bound"],
                "minimal_inverse_polynomial_degree": degree,
                "dense_inverse": info["dense_inverse"],
            }
        )
    return {"packet_minor_cases": packet_cases, "krylov_cases": krylov_cases}


def write_manifest():
    paths = sorted(
        p for p in ROOT.iterdir()
        if p.is_file() and p.name not in {"MANIFEST.sha256", "run_all.log"}
    )
    lines = []
    for path in paths:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        lines.append(f"{digest}  {path.name}")
    (ROOT / "MANIFEST.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    suite = unittest.defaultTestLoader.discover(str(ROOT), pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)

    exact = exact_results()
    bench = benchmark_packets()
    subprocess.run([sys.executable, str(ROOT / "independent_verifier.py")], cwd=ROOT, check=True)
    independent = json.loads((ROOT / "independent_results.json").read_text())

    payload = {
        **exact,
        "benchmark": bench,
        "independent": independent,
        "tests_run": result.testsRun,
        "tests_successful": result.wasSuccessful(),
    }
    (ROOT / "results.json").write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    summary = {
        "tests": result.testsRun,
        "packet_identity_cases": independent["independent_packet_cases"],
        "packet_minor_cases": len(exact["packet_minor_cases"]),
        "all_packet_minors_zero": all(r["packet_minor"] == 0 for r in exact["packet_minor_cases"]),
        "all_affine_fourier_minors_nonzero": all(r["affine_fourier_minor"] != 0 for r in exact["packet_minor_cases"]),
        "max_packet_speedup": max(r["speedup"] for r in bench),
        "krylov_cases": len(exact["krylov_cases"]),
        "all_krylov_degrees_ge_diameter": all(
            r["minimal_inverse_polynomial_degree"] >= r["directed_diameter"]
            for r in exact["krylov_cases"]
        ),
    }
    (ROOT / "RESULT_SUMMARY.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    write_manifest()
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
