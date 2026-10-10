"""Fresh exact-integer controls for the independently derived wrapper.

Only this new program is executed. It imports no research code. These controls
are finite falsification checks, not asymptotic proofs or coefficient tests.
"""

import hashlib
import json
from pathlib import Path


def ceil_log2(a):
    assert a > 0
    return (a - 1).bit_length()


root = Path(__file__).resolve().parents[2]
source_specs = [
    ("research_cycle_0958/algorithms/FINAL_THEOREM_AND_PROOF.md",
     "c8a775230a824872c23fc48b351e03d63878154bcfb314a8cca689842e31fc8d"),
    ("q01_finalization_1345/revision_v3/public/Q01_FINALIZATION.md",
     "9ab67e663abe0cca45299dfecbca6c4852fbcd77e5c078a62292c2b8e3f2374b"),
    ("q01_finalization_review_1350/public/INDEPENDENT_ACCEPTANCE.md",
     "be2ab749b57363972ac5d937b74ee62d7512cc08d2af0b0bedff779465ca29d0"),
    ("packed_fft_candidate_1355/executor_derivation/DYADIC_PACKED_THEOREM.md",
     "bb40decffd28b87a88065880363ff099b0d22071ef976bc67a8195c9b9db6d6f"),
]
sources = []
for path, expected in source_specs:
    actual = hashlib.sha256((root / path).read_bytes()).hexdigest()
    assert actual == expected, (path, actual, expected)
    sources.append({"path": path, "sha256": actual, "matches": True})

parameter_pairs = 0
nonpreparation_fast_guard_pairs = 0
for N in range(2, 8193):
    n = ceil_log2(N + 1)
    M = 1 << ceil_log2(4 * N)
    v = M.bit_length() - 1
    H = 1 << ceil_log2(2 * N - 1)
    k = H.bit_length()
    assert 4 * N <= M < 8 * N
    assert v in (n + 1, n + 2)
    assert 2 * N <= H < 4 * N
    assert 2 * N - 1 <= H
    for t in range(2, n + 1):
        parameter_pairs += 1
        s = t + 16
        h = 16 * s + 1
        a = t + 16 + ceil_log2(h + 2)
        assert (1 << a) >= (1 << (t + 16)) * (h + 2)
        assert 2 * h + 2 == 32 * t + 516
        q = t + (H.bit_length() - 1) + ceil_log2(k) + 13
        # u <= epsilon/(8192*k*H); final bound <= epsilon/4.
        assert (1 << (q - t)) >= 8192 * k * H
        assert (1 << (q - t)) >= 4 * 2048 * k * H
        assert (1 << q) >= 500 * k
        assert (1 << q) >= 8 * k
        if n >= 10 and 4 * t <= n:
            nonpreparation_fast_guard_pairs += 1
            assert t + 10 <= v + 1
            assert M >= 16 * s
            assert 2 * h + 2 < M

# Check guards symbolically through enormous lengths using only bit lengths.
large_n_guard_checks = 0
for n in range(10, 4097):
    t = n // 4
    smallest_M = 1 << (n + 1)
    assert t + 10 <= n + 2
    assert smallest_M >= 16 * (t + 16)
    assert 32 * (t + 16) + 4 < smallest_M
    large_n_guard_checks += 1

result = {
    "status": "passed",
    "source_integrity": sources,
    "lengths": 8191,
    "precision_parameter_pairs": parameter_pairs,
    "low_precision_nonpreparation_guards_checked": nonpreparation_fast_guard_pairs,
    "large_bit_length_guard_checks": large_n_guard_checks,
    "limits": [
        "No numerical FFT or interpolation executor was tested here.",
        "No coefficient-certificate or runtime benchmark is claimed.",
        "The new scalar fallback and composition rely on the written proof.",
        "No source or uploaded program was run, imported, compiled, or AST-parsed.",
    ],
}
out = Path(__file__).with_name("PARAMETER_CONTROL_RESULTS.json")
out.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
