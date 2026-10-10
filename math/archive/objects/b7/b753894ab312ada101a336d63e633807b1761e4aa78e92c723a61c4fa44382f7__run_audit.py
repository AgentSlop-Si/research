import json
import random
from pathlib import Path
from affine_reuse import (prepare, execute, inverse, batched_word, charge,
                         apply_t, apply_k, apply_j, independent_word,
                         expand_scalar, execute_scalar, serpentine_word, anchor_word)


def main():
    rng = random.Random(991009)
    cases, basis_count, batch_basis_count, random_count = [], 0, 0, 0
    for p in [65537, 998244353]:
        for n in [2, 4, 8, 16, 32]:
            plan = prepare(n, p)
            word, inverse_word = plan['word'], inverse(plan['word'], p)
            for j in range(n):
                x = [int(j == k) for k in range(n)]
                assert execute(word, x, p) == apply_j(plan, x)
                assert execute(inverse_word, execute(word, x, p), p) == x
                assert apply_t(plan, apply_k(plan, x)) == apply_j(plan, apply_t(plan, x))
                basis_count += 1
            batches = 4
            full = batched_word(plan, batches)
            scalar = expand_scalar(full, p)
            separate = independent_word(plan, batches)
            serpentine = serpentine_word(plan, batches)
            serpentine_scalar = expand_scalar(serpentine, p)
            anchor = anchor_word(plan, batches)
            anchor_scalar = expand_scalar(anchor, p)
            size = (batches + 2) * n
            inputs = []
            if n <= 8:
                inputs += [[int(i == j) for i in range(size)] for j in range(size)]
                batch_basis_count += size
            inputs += [[rng.randrange(p) for _ in range(size)] for _ in range(5)]
            random_count += 5
            for initial in inputs:
                expected = initial[:]
                x = initial[:n]
                for r in range(batches):
                    tx = apply_t(plan, x)
                    for i, value in enumerate(tx):
                        expected[(2 + r)*n+i] = (expected[(2 + r)*n+i]+value) % p
                    x = apply_k(plan, x)
                got = execute(full, initial, p)
                assert got == expected
                assert execute_scalar(scalar, initial, p) == expected
                assert execute(separate, initial, p) == expected
                assert execute(serpentine, initial, p) == expected
                assert execute_scalar(serpentine_scalar, initial, p) == expected
                assert execute(anchor, initial, p) == expected
                assert execute_scalar(anchor_scalar, initial, p) == expected
                assert execute(inverse(full, p), got, p) == initial
                assert execute(inverse(serpentine, p), got, p) == initial
                assert execute(inverse(anchor, p), got, p) == initial
            cases.append({'p': p, 'n': n, 'batches': batches,
                          'affine_update': charge(word), 'transparent_batch': charge(full),
                          'serpentine_batch': charge(serpentine),
                          'anchor_batch': charge(anchor),
                          'independent_replay': charge(separate)})
    edge_basis_count = 0
    for p in [65537, 998244353]:
        plan = prepare(4, p)
        for batches in [1, 2]:
            size = (batches+2)*4
            anchor = anchor_word(plan, batches)
            scalar = expand_scalar(anchor, p)
            separate = independent_word(plan, batches)
            for coordinate in range(size):
                initial = [int(i == coordinate) for i in range(size)]
                expected = execute(separate, initial, p)
                assert execute(anchor, initial, p) == expected
                assert execute_scalar(scalar, initial, p) == expected
                assert execute(inverse(anchor, p), expected, p) == initial
                edge_basis_count += 1
    comparison = []
    for n, batches in [(32, 4), (64, 4), (128, 8)]:
        plan = prepare(n)
        comparison.append({'n': n, 'batches': batches,
                           'transparent_batch': charge(batched_word(plan, batches)),
                           'serpentine_batch': charge(serpentine_word(plan, batches)),
                           'anchor_batch': charge(anchor_word(plan, batches)),
                           'independent_replay': charge(independent_word(plan, batches))})
    result = {'status': 'PASS', 'affine_basis_vectors': basis_count,
              'batch_full_state_basis_vectors': batch_basis_count,
              'anchor_edge_case_basis_vectors': edge_basis_count,
              'batch_random_full_states': random_count, 'cases': cases,
              'instruction_comparisons': comparison,
              'scope': 'Exact finite-field checks and gate counts; no timing or arbitrary FFT speed claim.'}
    target = Path(__file__).with_name('audit_results.json')
    target.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({key: value for key, value in result.items()
                      if key not in ['cases', 'instruction_comparisons']}, indent=2))


if __name__ == '__main__':
    main()
