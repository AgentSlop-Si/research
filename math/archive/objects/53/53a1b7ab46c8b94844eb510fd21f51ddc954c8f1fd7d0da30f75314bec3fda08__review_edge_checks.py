"""Independent focused checks; not a timing or asymptotic experiment."""
import json
from pathlib import Path

from adaptive_recurrence import (
    PrimeField, prepare_adaptive, apply_adaptive, expected_online, Counted, denominator,
)
from fft_decoded_baseline import (
    prepare_baseline, apply_baseline,
    expected_online as baseline_online,
    expected_preparation as baseline_preparation,
)
from hybrid import prepare_hybrid, apply_hybrid


def main():
    field = PrimeField(97)
    cases = 0
    for roots in ([2], [2, 3, 5], [2, 3, 5, 7, 11]):
        k = len(roots)
        length = max(2, 1 << (k - 1).bit_length())
        eta = field.root(2 * length)  # Oracle supplies the comparator root.
        for n in (1, 2, 5, 7, 19):
            for strides in (None, [], [1, 1, 3, 121]):
                amplitudes = [(i * i + 4) % 97 for i in range(k)]
                expected = [sum(amplitudes[i] * pow(roots[i], j, 97)
                                for i in range(k)) % 97 for j in range(n)]
                plan = prepare_adaptive(field, n, roots, strides)
                result, counts = apply_adaptive(field, plan, amplitudes)
                assert result == expected
                assert counts['field_operations'] == expected_online(
                    n, k, plan.initial_length, len(plan.taps))
                baseline = prepare_baseline(field, n, roots, eta)
                other, other_counts = apply_baseline(field, baseline, amplitudes)
                assert other == expected
                assert other_counts['field_operations'] == baseline_online(n, k)
                assert baseline.preparation == baseline_preparation(k)
                hybrid = prepare_hybrid(field, n, roots, eta, strides)
                final, final_counts = apply_hybrid(field, hybrid, amplitudes)
                assert final == expected
                cold = sum(hybrid.preparation.values()) + sum(
                    final_counts['field_operations'].values())
                assert cold == sum(hybrid.adaptive.preparation.values()) + min(
                    hybrid.adaptive_online_total, hybrid.baseline_additional_total)
                cases += 1
    dense_controls = []
    for prime in (65537, 998244353):
        field = PrimeField(prime)
        q = field.root(4096)
        roots = [field.power(q, a + 256 * j)
                 for a in (1, 3) for j in range(8)]
        polynomial = denominator(Counted(field), roots)
        nonconstant_terms = sum(x != field.zero for x in polynomial[1:])
        assert nonconstant_terms == 16
        dense_controls.append(dict(prime=prime, nonconstant_terms=nonconstant_terms))
    result = dict(status='PASS', focused_cases=cases, dense_controls=dense_controls,
                  scope='short and nonblock-aligned output; arbitrary nonzero roots; '
                        'stride normalization; exact hybrid cold selection')
    destination = Path(__file__).parent / 'results' / 'independent_edge_checks.json'
    destination.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
