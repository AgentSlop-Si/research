"""Exact dyadic detail decomposition, independent of FFT implementation.

This is an offline quadratic oracle and identity verifier, not a fast FFT.
Only Python standard-library arithmetic is used.
"""
from __future__ import annotations

import json
from pathlib import Path


def root(n, p):
    if n < 1 or n & (n - 1) or (p - 1) % n:
        raise ValueError("unsupported length")
    q = pow(3, (p - 1) // n, p)
    assert pow(q, n, p) == 1
    assert n == 1 or pow(q, n // 2, p) != 1
    return q


def dft(x, q, p):
    return [sum(v * pow(q, k*j, p) for j, v in enumerate(x)) % p
            for k in range(len(x))]


def details(x, p):
    """Invertible O(N) split into dc and detail vectors of sizes 1,2,...,N/2."""
    x = list(x)
    blocks = {}
    while len(x) > 1:
        m = len(x) // 2
        blocks[m] = [(x[j] - x[j+m]) % p for j in range(m)]
        x = [(x[j] + x[j+m]) % p for j in range(m)]
    return x[0], blocks


def undo_details(dc, blocks, p):
    inv2 = pow(2, -1, p)
    x = [dc]
    for m in sorted(blocks):
        d = blocks[m]
        assert len(x) == len(d) == m
        x = ([(x[j]+d[j])*inv2 % p for j in range(m)] +
             [(x[j]-d[j])*inv2 % p for j in range(m)])
    return x


def from_details(dc, blocks, n, p):
    out = [0] * n
    out[0] = dc
    for m, d in blocks.items():
        phase = root(2*m, p)
        twisted = [v * pow(phase, j, p) % p for j, v in enumerate(d)]
        transformed = dft(twisted, phase*phase % p, p)
        stride = n // (2*m)
        for k, value in enumerate(transformed):
            out[stride*(2*k+1)] = value
    return out


def reverse_bits(j, length):
    answer = 0
    for _ in range(length):
        answer = 2*answer + (j & 1)
        j >>= 1
    return answer


def c_entry(k, j, n):
    return -1 if (k & reverse_bits(j, n.bit_length()-1)).bit_count() % 2 else 1


def valuation(j):
    return (j & -j).bit_length()-1 if j else -1


def verify_blocks(n, p):
    """Compare every entry of FC/N against the claimed diagonal blocks."""
    q = root(n, p)
    invn = pow(n, -1, p)
    entries = 0
    for k in range(n):
        for j in range(n):
            actual = sum(pow(q, k*t, p)*c_entry(t, j, n)
                         for t in range(n))*invn % p
            if k == 0 or j == 0:
                expected = int(k == j == 0)
            elif valuation(k) != valuation(j):
                expected = 0
            else:
                s = valuation(k)
                m = n >> (s+1)
                a, b = (k >> s)//2, (j >> s)//2
                phase = pow(q, 1 << s, p)
                expected = sum(pow(phase, (2*a+1)*t, p)*c_entry(t, b, m)
                               for t in range(m))*pow(m, -1, p) % p
            assert actual == expected, (n, p, k, j)
            entries += 1
    return entries


def cost(n):
    """Count additions for this decomposition with standard radix-two sub-FFTs.

    This is a mathematical schedule count, not Python execution cost.
    Twiddle multiplication counts deliberately shown separately from additions.
    """
    L = n.bit_length()-1
    haar_additions = 2*(n-1)
    block_additions = sum((1 << t)*t for t in range(L))
    detail_phase_slots = n-1
    nonunit_detail_phases = n-1-L
    assert haar_additions + block_additions == n*L
    return {"n": n, "haar_additions": haar_additions,
            "block_fft_additions": block_additions,
            "total_additions": haar_additions+block_additions,
            "ordinary_radix_two_additions": n*L,
            "detail_phase_slots": detail_phase_slots,
            "nonunit_detail_phases": nonunit_detail_phases,
            "additional_block_fft_twiddles": "required; not included in additions",
            "storage_words": "O(N), including all detail vectors and output",
            "preprocessing": "O(N) scalar powers across the disjoint blocks"}


def run():
    cases = []
    for p in (65537, 998244353):
        for n in (2, 4, 8, 16, 32, 64):
            for col in range(n):
                x = [int(j == col) for j in range(n)]
                dc, blocks = details(x, p)
                assert undo_details(dc, blocks, p) == x
                assert from_details(dc, blocks, n, p) == dft(x, root(n,p), p)
            cases.append({"n":n, "p":p, "basis_vectors":n,
                          "block_entries":verify_blocks(n,p), "passed":True})
    report = {"claim":"Exact identity verified; no asymptotic speedup.",
              "cases":cases,
              "basis_vectors_total":sum(c["basis_vectors"] for c in cases),
              "block_entries_total":sum(c["block_entries"] for c in cases),
              "costs":[cost(1 << L) for L in (4,8,12,16,20)],
              "proof_scope":"All-N derivation in README; finite checks are regression evidence."}
    Path(__file__).with_name("results.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({k:report[k] for k in ("claim","basis_vectors_total","block_entries_total")}))


if __name__ == "__main__":
    run()
