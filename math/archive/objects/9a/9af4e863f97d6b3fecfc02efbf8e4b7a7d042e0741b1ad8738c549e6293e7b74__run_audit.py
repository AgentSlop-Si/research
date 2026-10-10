"""Focused exact audit; Python whole-field reference work is not algorithm work."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import random

from galois_defect import signed_action, transform, hybrid_transform


P = 998244353


def root_for(n):
    # Test-field constant/root generation; the algorithm API explicitly takes
    # a supplied root, verifies its order and prepares all its powers itself.
    return pow(3, (P-1)//n, P)


def direct(values, root):
    return [sum(value*pow(root, j*k, P) for j, value in enumerate(values)) % P
            for k in range(len(values))]


def structured(n, rng):
    """Dense-family generator with telescoping P_5 defects of support <=2."""
    inv2 = (P+1)//2
    state = [rng.randrange(1, P)]
    q = 2
    while q <= n:
        m = q//2
        if q <= 4:
            reduced = [rng.randrange(P) for _ in range(m)]
        else:
            seed = [0]*m
            seed[1] = rng.randrange(1, P)
            reduced = [0]*m
            current = seed
            for _ in range(max(1, q//8)):
                reduced = [(a+b) % P for a, b in zip(reduced, current)]
                current = signed_action(current, P, Counter())
        state = [((a+b)*inv2) % P for a, b in zip(state, reduced)] + [
                 ((a-b)*inv2) % P for a, b in zip(state, reduced)]
        q *= 2
    return state


def main():
    rng = random.Random(9017)
    accepted_checks = 0
    dense_checks = 0
    reference_checks = 0
    rows = []
    for n in (1, 2, 4, 8, 16, 32, 64, 128, 256, 1024):
        omega = root_for(n)
        for case in range(3):
            values = structured(n, rng)
            original = list(values)
            fast = transform(values, P, omega)
            baseline = transform(values, P, omega, use_fast_path=False)
            hybrid = hybrid_transform(values, P, omega)
            assert fast['accepted']
            assert values == original
            assert fast['values'] == baseline['values']
            assert hybrid['values'] == baseline['values']
            assert hybrid['counts']['output_writes'] == n
            assert fast['counts']['output_writes'] == n
            assert fast['counts']['input_reads'] == n
            if n >= 2:
                expected = 9*n-12+2*fast['counts'].get('sparse_terms',0)+fast['counts'].get('neg',0)
                assert fast['field_operations'] == expected
                assert hybrid['field_operations'] <= baseline['field_operations']+n-3+hybrid['counts'].get('neg',0)
            if n <= 64:
                assert fast['values'] == direct(values, omega)
                reference_checks += 1
            accepted_checks += 1
            dense_checks += all(values)
            if case == 0:
                rows.append({'n': n, 'all_input_entries_nonzero': all(values),
                             'fast_operations': fast['field_operations'],
                             'baseline_operations': baseline['field_operations'],
                             'hybrid_operations':hybrid['field_operations'],
                             'hybrid_choices':hybrid['choices'],
                             'supports': fast['supports'],
                             'counts': fast['counts'],
                             'preparation_counts': fast['preparation_counts'],
                             'after_discovery_counts': fast['after_discovery_counts']})
    generic_checks = 0
    for n in (16, 32, 64, 256):
        values = [rng.randrange(1, P) for _ in range(n)]
        got = transform(values, P, root_for(n))
        assert not got['accepted']
        assert got['values'] == transform(values, P, root_for(n), use_fast_path=False)['values']
        hybrid = hybrid_transform(values, P, root_for(n))
        assert hybrid['values'] == got['values']
        assert hybrid['counts']['output_writes'] == n
        assert got['counts']['output_writes'] == n
        generic_checks += 1
    # Zero and uniform inputs meet the cap zero; a generic q=4 input also
    # works because multiplication by five is the identity modulo four.
    zero_cap_checks = 0
    for n in (1, 2, 4, 8, 32, 128):
        for values in ([0]*n, [7]*n):
            got = transform(values, P, root_for(n), max_defect=0)
            assert got['accepted']
            assert got['values'] == transform(values, P, root_for(n), use_fast_path=False)['values']
            zero_cap_checks += 1
    invalid_checks = 0
    for values, p, root, cap in (([], P, 1, 2), ([1,2,3], P, 1, 2),
                                  ([1,2], P, 1, 2), ([1,P], P, P-1, 2),
                                  ([1,2], P, P-1, -1), ([1,True], P, P-1, 2)):
        try:
            transform(values, p, root, max_defect=cap)
        except ValueError:
            invalid_checks += 1
        else:
            raise AssertionError('invalid argument accepted')
    # Independent recurrence identity at every odd frequency, independent
    # of the support restriction used by the optimization.
    identity_checks = 0
    for q in (4, 8, 16, 32, 64):
        m, omega = q//2, root_for(q)
        reduced = [rng.randrange(P) for _ in range(m)]
        acted = signed_action(reduced, P, Counter())
        defect = [(a-b) % P for a,b in zip(acted,reduced)]
        for k in range(1,q,2):
            original = sum(v*pow(omega,j*k,P) for j,v in enumerate(reduced)) % P
            shifted = sum(v*pow(omega,j*((5*k)%q),P) for j,v in enumerate(reduced)) % P
            delta = sum(v*pow(omega,j*k,P) for j,v in enumerate(defect)) % P
            assert (shifted-original) % P == delta
            identity_checks += 1
    root = Path(__file__).resolve().parent
    result = {'status':'PASS', 'structured_transforms':accepted_checks,
              'fully_dense_structured_inputs':dense_checks,
              'independent_direct_dft_checks':reference_checks,
              'generic_fallback_checks':generic_checks,
              'zero_cap_checks':zero_cap_checks, 'invalid_checks':invalid_checks,
              'odd_orbit_identity_checks':identity_checks, 'cost_rows':rows,
              'hybrid_full_output_checks':accepted_checks+generic_checks,
              'source_sha256':hashlib.sha256((root/'galois_defect.py').read_bytes()).hexdigest(),
              'scope':'Restricted exact full-output linear-time fast path; no general FFT improvement.'}
    (root/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='cost_rows'},indent=2))


if __name__ == '__main__':
    main()
