"""Independent arithmetic controls for the proposed rank-two contract.
Only Python standard-library code is used. No author/archive implementation is
imported or executed. This is not a production executor or budget audit.
"""
from itertools import product, permutations
from math import gcd
from pathlib import Path
import hashlib
import json


def spectrum(y, p, w):
    # Independent Fourier-support membership oracle, using the inverse sign.
    n = len(y)
    inv_n = pow(n, -1, p)
    return [inv_n * sum(y[j] * pow(w, (-j*b) % n, p)
                       for j in range(n)) % p for b in range(n)]


def dechirp(x, p, w, a):
    n = len(x)
    return [x[j] * pow(w, (-a*j*j) % n, p) % p for j in range(n)]


def coefficients(x, p, c):
    n = len(x)
    z, u, v, U, V = [x[(c+d) % n] for d in (0, -1, 1, -2, 2)]
    return [z*z*z % p, -2*z*u*v % p, 0,
            (u*u*V+U*v*v) % p, -z*U*V % p]


def eval_poly(e, t, p):
    return sum(v*pow(t, k, p) for k, v in enumerate(e)) % p


def direct_minor(x, c, t, p):
    n = len(x)
    M = [[x[(c+i-j) % n] * pow(t, (i-j)*(i-j-1)//2, p) % p
          for j in range(3)] for i in range(3)]
    return (M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])
            -M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])
            +M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0])) % p


def prefix_candidate(y, p, w):
    n = len(y)
    h0, h1, h2, h3 = [y[j % n] for j in range(4)]
    delta = (h0*h2-h1*h1) % p
    if delta == 0:
        if h0 == 0:
            return None
        node = h1*pow(h0, -1, p) % p
        matches = [b for b in range(n) if pow(w, b, p) == node]
        return [(matches[0], h0)] if len(matches) == 1 else None
    inv_delta = pow(delta, -1, p)
    S = (h0*h3-h1*h2)*inv_delta % p
    P = (h1*h3-h2*h2)*inv_delta % p
    bs = [b for b in range(n)
          if (pow(w, 2*b, p)-S*pow(w, b, p)+P) % p == 0]
    if len(bs) != 2:
        return None
    l0, l1 = [pow(w, b, p) for b in bs]
    c0 = (h1-h0*l1)*pow((l0-l1) % p, -1, p) % p
    c1 = (h0-c0) % p
    return list(zip(bs, (c0, c1))) if c0 and c1 else None


def reconstruct(n, p, w, a, terms):
    return [sum(g*pow(w, (a*j*j+b*j) % n, p) for b, g in terms) % p
            for j in range(n)]


out = {'verdict': 'PASS', 'scope': 'Independent mathematical design controls only; no metered executor accepted'}
small = []
for n, p, w in [(3, 7, 2), (4, 5, 2)]:
    checked = members = determinant_checks = phase_checks = 0
    true_rank_one = true_rank_two = 0
    for x in product(range(p), repeat=n):
        checked += 1
        if not any(x):
            members += 1
            continue
        center = next(j for j, v in enumerate(x) if v)
        coeff = coefficients(x, p, center)
        assert coeff[0] != 0
        for t in range(p):
            assert eval_poly(coeff, t, p) == direct_minor(x, center, t, p)
            determinant_checks += 1
        oracle_phases, design_phases = [], []
        for a in range(n // gcd(2, n)):
            phase_checks += 1
            y = dechirp(x, p, w, a)
            support = [b for b, v in enumerate(spectrum(y, p, w)) if v]
            if len(support) <= 2:
                oracle_phases.append(a)
                true_rank_one += (len(support) == 1)
                true_rank_two += (len(support) == 2)
            t = pow(w, (-2*a) % n, p)
            if eval_poly(coeff, t, p):
                continue
            candidate = prefix_candidate(y, p, w)
            if candidate is not None and reconstruct(n, p, w, a, candidate) == list(x):
                design_phases.append(a)
        assert oracle_phases == design_phases, (n, p, x, oracle_phases, design_phases)
        members += bool(oracle_phases)
    small.append(dict(N=n, p=p, omega=w, raw_vectors=checked, members=members,
                      phase_checks=phase_checks, determinant_checks=determinant_checks,
                      true_rank_one_phases=true_rank_one, true_rank_two_phases=true_rank_two))
out['independent_exhaustive_support_oracle'] = small

n, p, w = 8, 17, 2
x = [1, 1, 1, 1, 2, 1, 1, 1]
e = coefficients(x, p, 0)
phases = []
for a in range(4):
    y = dechirp(x, p, w, a)
    spec = spectrum(y, p, w)
    candidate = prefix_candidate(y, p, w)
    raw = reconstruct(n, p, w, a, candidate) if candidate is not None else None
    phases.append(dict(a=a, phase_point=pow(w, (-2*a) % n, p),
                       quartic_value=eval_poly(e, pow(w, (-2*a) % n, p), p),
                       normalized_inverse_spectrum=spec,
                       support_size=sum(v != 0 for v in spec),
                       first_four_periodic_dechirped=y[:4],
                       prefix_candidate=candidate,
                       raw_mismatch_indices=([j for j in range(n) if x[j] != raw[j]]
                                             if raw is not None else None)))
assert [r['a'] for r in phases if not r['quartic_value']] == [0, 2]
assert all(r['support_size'] == 8 for r in phases)
assert all(r['raw_mismatch_indices'] == [4] for r in phases if not r['quartic_value'])
out['false_prefix_nonmember'] = dict(N=n, p=p, omega=w, x=x, quartic_coefficients=e, phases=phases)

x = [2, 0, 2, 0, 2, 0, 2, 0]
ambiguity = []
for a in range(4):
    spec = spectrum(dechirp(x, p, w, a), p, w)
    terms = [(b, v) for b, v in enumerate(spec) if v]
    assert len(terms) == 2 and reconstruct(n, p, w, a, terms) == x
    ambiguity.append(dict(a=a, terms=terms))
out['four_phase_ambiguity'] = ambiguity

# Direct all-c Gauss sums provide an independent check of both identities.
gauss = []
for n, p, w in [(3, 7, 2), (4, 5, 2), (5, 11, 3), (6, 7, 3),
                (8, 17, 2), (12, 13, 2), (16, 17, 3), (32, 97, 19)]:
    checks = 0
    for a in range(n):
        row = [sum(pow(w, (a*j*j+c*j) % n, p) for j in range(n)) % p for c in range(n)]
        d = gcd(2*a, n)
        K = n // d
        c0 = (-a*K) % d
        for c in range(n):
            assert (c-c0) % d == 0 or row[c] == 0
            assert row[(c+2*a) % n] == pow(w, (-a-c) % n, p)*row[c] % p
            checks += 1
        orbit = [(c0+2*a*j) % n for j in range(K)]
        assert len(set(orbit)) == K
        assert set(orbit) == {c for c in range(n) if (c-c0) % d == 0}
    gauss.append(dict(N=n, p=p, omega=w, all_phase_rows=n, coordinate_checks=checks))
out['direct_gauss_identity_controls'] = gauss
out['reviewer_script_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
Path(__file__).with_name('chirp_rank2_independent_results.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps(out, indent=2))
