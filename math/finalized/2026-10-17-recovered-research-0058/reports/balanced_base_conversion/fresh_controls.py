"""Fresh standalone exactness/ledger controls, authored 2026-10-17.

No historical code is imported. Python big integers are correctness oracles,
not a claim about bit-array timing. Only the explicit counters represent ledgers.
"""
import hashlib
import json
import random
from pathlib import Path


def split_cascade(x, m, d, s, k=None):
    assert m >= 2 and d >= 1 and s >= 2
    k = s // 2 if k is None else k
    assert 1 <= k < s
    p = (1 << m) - 1
    assert 0 <= x < p ** (d * s)
    stages = d * k
    residual = [0] * stages
    quotient = 0
    volume = 0
    mask = (1 << m) - 1
    for block in reversed(range(d * s)):
        chunk = (x >> (block * m)) & mask
        for i in range(stages):
            old = residual[i]
            z = old + chunk
            e = int(z >= p)
            chunk = old + e
            residual[i] = z - e * p
            volume += m
            assert 0 <= chunk <= mask and 0 <= residual[i] < p
        quotient = (quotient << m) | chunk
    remainder = 0
    assembly = 0
    for count, r in enumerate(reversed(residual), 1):
        remainder = (remainder << m) - remainder + r
        assembly += count * m
        assert remainder.bit_length() <= count * m
    assert (quotient, remainder) == divmod(x, p ** stages)
    assert volume == m * (d * s) * stages
    assert assembly == m * stages * (stages + 1) // 2
    return quotient, remainder, volume, assembly


def convert_tree(x, m, d, size):
    p = (1 << m) - 1
    assert size >= 1 and size & (size - 1) == 0
    assert 0 <= x < p ** (d * size)
    if size == 1:
        return [x], 0, 0
    q, r, vol, assembly = split_cascade(x, m, d, size)
    low, low_v, low_a = convert_tree(r, m, d, size // 2)
    high, high_v, high_a = convert_tree(q, m, d, size // 2)
    return low + high, vol + low_v + high_v, assembly + low_a + high_a


def reconstruct_tree(digits, m, d):
    size = len(digits)
    if size == 1:
        return digits[0], 0
    low, vl = reconstruct_tree(digits[:size // 2], m, d)
    high, vh = reconstruct_tree(digits[size // 2:], m, d)
    v = high
    for _ in range(d * size // 2):
        v = (v << m) - v
        assert v.bit_length() <= d * m * size
    v += low
    assert v.bit_length() <= d * m * size
    return v, vl + vh + (d * size // 2) * (d * m * size)


def base_q_oracle(x, q, count):
    out = []
    for _ in range(count):
        x, r = divmod(x, q)
        out.append(r)
    assert x == 0
    return out


def volume_formula(m, d, size):
    return d * d * m * size * (size - 1)


def assembly_formula(m, d, size):
    h = size.bit_length() - 1
    numerator = m * d * d * size * (size - 1) + m * d * size * h
    assert numerator % 4 == 0
    return numerator // 4


def run():
    rng = random.Random(202610170058)
    counts = {"arbitrary_split_cases": 0, "balanced_roundtrips": 0,
              "coverage_cases": 0, "one_group_cases": 0, "negative_controls": 0}
    rows = []
    # Arbitrary split location: the stage count is dk, including non-half splits.
    for m in [2, 3, 4, 5, 7, 13]:
        p = (1 << m) - 1
        for d in [1, 2, 3, 5]:
            q = p ** d
            for s in [2, 3, 4, 7, 8, 13]:
                for k in sorted({1, s // 2, s - 1}):
                    cap = q ** s
                    samples = {0, 1, cap - 1, q ** k - 1, q ** k, rng.randrange(cap)}
                    for x in samples:
                        split_cascade(x, m, d, s, k)
                        counts["arbitrary_split_cases"] += 1
    # Exhaustive small capacities and reproducible larger cases.
    for m in [2, 3, 4, 5, 7, 13]:
        p = (1 << m) - 1
        for d in [1, 2, 3, 5, 7]:
            q = p ** d
            for size in [1, 2, 4, 8, 16, 32]:
                cap = q ** size
                if cap <= 7000:
                    samples = range(cap)
                else:
                    samples = {0, 1, cap - 1, cap - 2, cap // 2,
                               q ** (size // 2), q ** (size // 2) - 1,
                               rng.randrange(cap), rng.randrange(cap)}
                for x in samples:
                    digits, volume, assembly = convert_tree(x, m, d, size)
                    assert digits == base_q_oracle(x, q, size)
                    rebuilt, rebuild_volume = reconstruct_tree(digits, m, d)
                    assert rebuilt == x
                    assert volume == rebuild_volume == volume_formula(m, d, size)
                    assert assembly == assembly_formula(m, d, size)
                    counts["balanced_roundtrips"] += 1
                    if size == 1:
                        counts["one_group_cases"] += 1
                if size >= 2:
                    C = d * m * size
                    v = volume_formula(m, d, size)
                    # Exact ratio V/(C^2/m) = 1-1/L without floating point.
                    assert v * m * size == C * C * (size - 1)
                    rows.append({"m": m, "d": d, "L": size, "C": C,
                                 "division_volume": v,
                                 "root_volume": d*d*m*size*size // 2,
                                 "assembly_capacity": assembly_formula(m,d,size),
                                 "ratio_to_C_squared_over_m": (size-1)/size})
    for m in [2, 3, 4, 7, 13, 31]:
        p = (1 << m) - 1
        for d in [1, 2, 3, 7, 15]:
            for N in sorted({d*m, d*m+1, 2*d*m, 4*d*m-1, 7*d*m, 127*d*m}):
                target = (N + d*(m-1)-1) // (d*(m-1))
                L = 1 << (target - 1).bit_length()
                C = d*m*L
                assert L >= 2 and N <= C < 4*N
                assert p ** (d*L) >= (1 << N)
                counts["coverage_cases"] += 1
    # All bad shortcuts are rejected by exact counterexamples.
    assert divmod(20, 3**2) != divmod(20, 3)
    counts["negative_controls"] += 1
    assert 3**2 != 2**4 - 1
    counts["negative_controls"] += 1
    assert 1*3 + 1 != (1 << 2) + 1  # Q digits are not binary concatenation.
    counts["negative_controls"] += 1
    assert 2**4 - 1 >= 3**2  # c_s-bit capacity alone is not Q^s coverage.
    counts["negative_controls"] += 1
    assert volume_formula(4, 5, 1) == 0  # no quadratic split at one leaf.
    counts["negative_controls"] += 1
    result = {
        "status": "PASS", "scope": "fresh all-stage exactness and symbolic ledgers; no timing claim",
        "counts": counts, "ledger_rows": rows,
        "declared_grammar": "L power of two; fixed ds input chunks; dk full states; binary materialized remainders",
        "composite_p_included": [15, 63],
        "historical_code_executed": False,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    # m=6 explicitly verifies p=63 in addition to the main grid's p=15.
    for x in [0, 1, 63**16-1]:
        digits, vol, ass = convert_tree(x, 6, 2, 8)
        assert reconstruct_tree(digits, 6, 2)[0] == x
        assert vol == volume_formula(6,2,8) and ass == assembly_formula(6,2,8)
        counts["balanced_roundtrips"] += 1
    path = Path(__file__).with_name("CONTROL_RESULTS.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "counts": counts,
                      "ledger_rows": len(rows), "output": str(path)}, indent=2))


if __name__ == "__main__":
    run()
