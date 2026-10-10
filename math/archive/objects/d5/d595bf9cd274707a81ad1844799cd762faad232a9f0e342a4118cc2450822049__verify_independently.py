"""Independent replay of the bounded h=24 complex-label refinement.

Uses the pinned upstream checker and histogram emitter to cross-check the
experiment, then a separately written rational moment enclosure. This checks
finite labels, counts and moments, not the full asymptotic multiplication or
all-length exact-DFT theorems.
"""
from fractions import Fraction as Q
from decimal import Decimal, localcontext
from math import factorial
from pathlib import Path
import json
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "upstream"))
from producer import NStar3
from frames import Checker
import hist as upstream_hist


def log_bounds(x):
    k = 0
    while x >= 2:
        x /= 2
        k += 1

    def atanh_bounds(u):
        lo = 2 * sum((u ** (2*j+1) / Q(2*j+1) for j in range(50)), Q(0))
        hi = lo + 2 * u**101 / Q(101) / (1-u*u)
        return lo, hi

    l2, u2 = atanh_bounds(Q(1, 3))
    lo, hi = atanh_bounds((x-1)/(x+1))
    return k*l2 + lo, k*u2 + hi


def exp_lower(x):
    return sum((x**j / Q(factorial(j)) for j in range(12)), Q(0))


def exp_upper(x):
    assert 0 <= x < 13
    # For j >= 12, successive Taylor terms have ratio at most x/13.
    return exp_lower(x) + x**12 / Q(factorial(12)) / (1-x/13)


def moment_bounds(certificate, saving):
    W, m = certificate["W"], certificate["m"]
    lo = hi = Q(0)
    for width, count in certificate["hist"].items():
        width = int(width)
        l, u = log_bounds(Q(m, width))
        weight = Q(width*count, W*m)
        lo += weight * exp_lower(saving*l)
        hi += weight * exp_upper(saving*u)
    return lo, hi


def dec(q):
    with localcontext() as ctx:
        ctx.prec = 50
        return str(Decimal(q.numerator)/Decimal(q.denominator))


def main():
    result = json.loads((HERE / "reduction_results.json").read_text())
    published = json.loads((HERE / "upstream" / "round6-histograms.json").read_text())
    assert result["source_commit"] == "f2176bc1124821bf17eb63725bd366d7bdc020a3"
    assert result["h"] == 24
    assert sorted((int(r), n) for r, n in result["baseline"]["hist"].items()) == [
        tuple(x) for x in published["cx"]["hist"]
    ]

    circuit = NStar3(24)
    checker = Checker(circuit)
    for change in result["changed_labels"]:
        assert len(checker.label(change["node"])) == len(change["old"])
        checker.lab[change["node"]] = change["new"]
    label_check = checker.run()
    assert label_check["bad"] == 0
    dimensions = {node: len(checker.label(node)) for node in circuit.active}
    upstream_hist.label_dims = lambda new_circuit: dimensions
    rebuilt = upstream_hist.build(24, copied=True)
    for field in ("W", "m", "s"):
        assert rebuilt[field] == result["modified"][field]
    assert rebuilt["hist"] == {int(r): n for r, n in result["modified"]["hist"].items()}
    assert rebuilt["maxrank"] < rebuilt["m"]

    checks = {}
    for name in ("baseline", "modified"):
        certificate = result[name]
        saving = Q(certificate["a"])
        assert sum(int(r)*n for r, n in certificate["hist"].items()) == certificate["s"]
        lower, upper = moment_bounds(certificate, saving)
        next_lower, next_upper = moment_bounds(certificate, saving+Q(1, 10**12))
        assert upper < 1
        assert next_lower > 1
        checks[name] = dict(
            saving=str(saving),
            moment_upper_below_one=True,
            next_grid_moment_lower_above_one=True,
            upper_margin_decimal=dec(1-upper),
            next_grid_lower_excess_decimal=dec(next_lower-1),
        )
    summary = dict(
        source_commit=result["source_commit"],
        changed_labels=len(result["changed_labels"]),
        upstream_concrete_label_check=label_check,
        published_baseline_histogram_matches=True,
        upstream_modified_histogram_matches=True,
        W=rebuilt["W"], m=rebuilt["m"], s=rebuilt["s"], max_child=rebuilt["maxrank"],
        exact_rational_moment_checks=checks,
        relative_saving_gain_decimal=dec(Q(result["modified"]["a"])/Q(result["baseline"]["a"])-1),
        scope="Finite-label and recurrence-moment audit only; no full asymptotic theorem or novelty claim.",
    )
    (HERE / "independent_verification.json").write_text(json.dumps(summary, indent=2)+"\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
