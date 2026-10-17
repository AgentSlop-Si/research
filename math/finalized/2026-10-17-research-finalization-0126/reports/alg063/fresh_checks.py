"""Fresh exact tests only. All imported mathematical code was authored here."""
import hashlib
import itertools
import json
import random
from collections import Counter
from pathlib import Path

from recognize_twisted_dft import raw_twisted_dft


def direct(x, p, w):
    # Dense oracle: explicit independent modular exponentiation at every entry.
    return [sum(v * pow(w, j * k, p) for j, v in enumerate(x)) % p
            for k in range(len(x))]


def promise(x, r, p):
    m = sum(v != 0 for v in x)
    residuals = [sum((x[j] - z * x[j - 1]) % p != 0
                     for j in range(len(x))) for z in range(p)]
    return m <= 2 * r or min(residuals) <= r, residuals


def primitive(p, n):
    return next(w for w in range(1, p)
                if pow(w, n, p) == 1
                and all(pow(w, k, p) != 1 for k in range(1, n)))


def main():
    stats = Counter()
    digest = hashlib.sha256()
    examples = {}
    worst = {"ratio": 0}

    def check(x, r, p, w, group, brute=True):
        answer = raw_twisted_dft(x, r, p, w)
        cert, counts = answer["certificate"], answer["counts"]
        if brute:
            admissible, residuals = promise(x, r, p)
            assert cert["accepted"] == admissible
        if cert["accepted"]:
            assert answer["output"] == direct(x, p, w)
        if cert["branch"] == "twisted_residual":
            a, b = cert["a"], cert["b"]
            assert b != 0
            assert cert["residual_nnz"] <= r
            assert len(cert["resonant_bins"]) <= 1
            if cert["resonant_bins"]:
                stats["resonant_successes"] += 1
            if cert["residual_nnz"] == 0:
                stats["zero_residual_successes"] += 1
        assert counts["inv"] <= 1
        n = len(x)
        # Conservative symbolic ledger bounds, independent of p.
        assert counts["mul"] <= n * (2 * r + 14)
        assert counts["add_sub"] <= n * (2 * r + 4)
        assert counts["eq"] <= 7 * n
        cost = counts["mul"] + counts["add_sub"] + counts["eq"]
        ratio = cost / (n * (r + 1))
        if ratio > worst["ratio"]:
            worst.update({"ratio": ratio, "N": n, "r": r, "p": p,
                          "counts": dict(counts), "branch": cert["branch"]})
        stats[group] += 1
        stats[cert["branch"]] += 1
        digest.update(json.dumps([x, r, p, w, answer], sort_keys=True).encode())
        examples.setdefault(cert["branch"], {"x": x, "r": r, "p": p,
                                              "omega": w, "answer": answer})
        return answer

    for p, n in [(2, 1), (3, 2), (5, 4), (7, 3), (13, 3)]:
        w = primitive(p, n)
        for x in itertools.product(range(p), repeat=n):
            for r in range(n + 1):
                check(list(x), r, p, w, "exhaustive_raw_cases")

    rng = random.Random(630017)
    for p, n in [(17, 8), (97, 8), (97, 12), (193, 16), (257, 32), (257, 64)]:
        w = primitive(p, n)
        orders = [list(range(n)), list(reversed(range(n)))]
        for _ in range(7):
            order = list(range(n))
            for _ in range(2):
                i, j = rng.sample(range(n), 2)
                order[i], order[j] = order[j], order[i]
            orders.append(order)
        for order in orders:
            successors = [0] * n
            for t, j in enumerate(order):
                successors[j] = order[(t + 1) % n]
            s = sum(successors[j] != (j + 1) % n for j in range(n))
            for z in sorted(set([0, 1, 2, 3] + [pow(w, k, p) for k in range(n)])):
                x = [0] * n
                for t, j in enumerate(order):
                    x[j] = pow(z, t, p)
                r = min(n, 2 * s + (pow(z, n, p) != 1))
                result = check(x, r, p, w, "geometric_inclusion_cases", brute=False)
                assert result["certificate"]["accepted"]
        for _ in range(30):
            x = [rng.randrange(p) for _ in range(n)]
            r = rng.randrange(n + 1)
            check(x, r, p, w, "random_raw_cases")
        # Construct piecewise geometric sequences, often outside permuted powers.
        for z in [0, 1, 2, pow(w, 3, p)]:
            x = [3]
            breaks = {n // 3, 2 * n // 3}
            for j in range(1, n):
                x.append(rng.randrange(p) if j in breaks else z * x[-1] % p)
            check(x, 3, p, w, "piecewise_geometric_cases")

    # Full verification is essential: this dense vector has a majority ratio 1
    # but two cyclic breaks, so r=1 must reject.
    rejection = check([1, 1, 1, 1, 1, 2, 2, 2], 1, 17, primitive(17, 8),
                      "named_negative_controls")
    assert not rejection["certificate"]["accepted"]
    examples["majority_without_small_residual"] = rejection
    # Full-support z=1 character has d=0: resonance must retain nonzero DC.
    homogeneous = check([3] * 8, 0, 17, primitive(17, 8), "named_positive_controls")
    assert homogeneous["output"] == [7, 0, 0, 0, 0, 0, 0, 0]
    examples["homogeneous_resonance"] = homogeneous
    # Scaling gives a raw vector that need not contain 1, so it cannot be a
    # permutation of (1,z,...,z^(N-1)) for any z.
    extra = check([2] * 8, 0, 17, primitive(17, 8), "named_positive_controls")
    assert extra["certificate"]["accepted"]
    examples["strict_family_extension"] = extra

    malformed = [([], 0, 17, 1), ([1], -1, 17, 1), ([1], 2, 17, 1),
                 ([1], True, 17, 1), ([17], 0, 17, 1), ([True], 0, 17, 1),
                 ([1, 1], 0, 17, 1), ([1, 1], 0, 17, 3)]
    for args in malformed:
        try:
            raw_twisted_dft(*args)
        except ValueError:
            stats["malformed_rejections"] += 1
        else:
            raise AssertionError("malformed input accepted")

    output = {"status": "PASS", "statistics": dict(sorted(stats.items())),
              "ordered_case_digest_sha256": digest.hexdigest(),
              "worst_count_ratio_observed": worst, "examples": examples,
              "scope": "Fresh finite exact controls, not uniform proof or production acceptance",
              "inherited_programs_executed": False}
    Path(__file__).with_name("CHECK_RESULTS.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: v for k, v in output.items() if k != "examples"}, indent=2))


if __name__ == "__main__":
    main()
