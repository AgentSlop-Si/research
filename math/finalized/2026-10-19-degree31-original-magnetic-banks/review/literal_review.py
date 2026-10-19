#!/usr/bin/env python3
"""Fresh degree-31 review. Inert JSON only; no candidate code is imported.

Prime polynomials use ordinary integer convolution and Euclidean division.
Original branch inverses use the closed cyclic-bidiagonal adjugate, rather
than Gaussian elimination, inverse recurrence, or a discovery interpolation.
"""
import argparse, copy, hashlib, json, math, random, time
from pathlib import Path
P, D, N, QROOT = 53, 31, 13, 16
ORDER = P ** D
ZERO = (0,) * D
ONE = (1,) + (0,) * (D - 1)

def require(ok, message):
    if not ok:
        raise ValueError(message)

def trim(a):
    a = [x % P for x in a]
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a

def polyadd(a, b, sign=1):
    z = list(a) + [0] * max(0, len(b) - len(a))
    for i, v in enumerate(b):
        z[i] += sign * v
    return trim(z)

def polymul(a, b):
    z = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            z[i + j] += x * y
    return trim(z)

def divrem(a, b):
    a, b = trim(a), trim(b)
    require(b != [0], 'prime polynomial division by zero')
    q = [0] * max(1, len(a) - len(b) + 1)
    il = pow(b[-1], -1, P)
    while a != [0] and len(a) >= len(b):
        offset, v = len(a) - len(b), a[-1] * il % P
        q[offset] = v
        for i, c in enumerate(b):
            a[offset + i] -= v * c
        a = trim(a)
    return trim(q), a

def pgcd(a, b):
    while b != [0]:
        a, b = b, divrem(a, b)[1]
    return trim([v * pow(a[-1], -1, P) for v in a])

def ppow(a, e, h):
    z = [1]
    while e:
        if e % 2:
            z = divrem(polymul(z, a), h)[1]
        a = divrem(polymul(a, a), h)[1]
        e //= 2
    return z

def prime(n):
    return n >= 2 and all(n % p for p in range(2, math.isqrt(n) + 1))

class Field:
    def __init__(self, modulus):
        self.modulus = modulus
        require(len(modulus) == D + 1 and modulus[-1] == 1, 'degree-31 monic modulus')
        require(all(type(x) is int and 0 <= x < P for x in modulus), 'canonical modulus')
        require(prime(P) and prime(D), 'prime characteristic and extension degree')
        self.inverses = {}
        # Establish field status before exposing any extension-field inversion.
        x, frob = [0, 1], [0, 1]
        remainders = []
        for k in range(1, D + 1):
            frob = ppow(frob, P, modulus)
            remainders.append(frob)
        gcd = pgcd(modulus, polyadd(remainders[0], x, -1))
        require(frob == x and gcd == [1], 'Rabin irreducibility test')
        self.field_proof = {'prime_degree': D, 'characteristic_prime': P,
            'modulus_ascending': modulus, 'frobenius_remainders': remainders,
            'last_remainder': frob, 'gcd_with_X53_minus_X': gcd,
            'proof': 'h divides X^(53^31)-X, which is squarefree; factor degrees divide prime 31; gcd excludes degree one.'}
    def element(self, a):
        require(isinstance(a, list) and len(a) == D, 'field coordinate length')
        require(all(type(x) is int and 0 <= x < P for x in a), 'canonical field coordinates')
        return tuple(a)
    @staticmethod
    def scalar(a):
        return (a % P,) + (0,) * (D - 1)
    @staticmethod
    def add(a, b):
        return tuple((x + y) % P for x, y in zip(a, b))
    @staticmethod
    def sub(a, b):
        return tuple((x - y) % P for x, y in zip(a, b))
    @staticmethod
    def scale(a, s):
        return tuple(x * s % P for x in a)
    def mul(self, a, b):
        if a == ZERO or b == ZERO:
            return ZERO
        if not any(a[1:]):
            return self.scale(b, a[0])
        if not any(b[1:]):
            return self.scale(a, b[0])
        # Ordinary convolution with unbounded integers and generic monic division.
        raw = [0] * (2 * D - 1)
        for i, x in enumerate(a):
            for j, y in enumerate(b):
                raw[i + j] += x * y
        for k in range(len(raw) - 1, D - 1, -1):
            coefficient = raw[k] % P
            for j, c in enumerate(self.modulus[:-1]):
                raw[k - D + j] -= coefficient * c
        return tuple(x % P for x in raw[:D])
    def power(self, a, e):
        require(type(e) is int and e >= 0, 'unbounded nonnegative exponent')
        z = ONE
        while e:
            if e % 2:
                z = self.mul(z, a)
            a = self.mul(a, a)
            e //= 2
        return z
    def inverse(self, a):
        require(a != ZERO, 'field division by zero')
        if a not in self.inverses:
            r0, r1, t0, t1 = self.modulus[:], trim(a), [0], [1]
            while r1 != [0]:
                q, r2 = divrem(r0, r1)
                r0, r1 = r1, r2
                t0, t1 = t1, polyadd(t0, polymul(q, t1), -1)
            require(len(r0) == 1 and r0[0], 'Euclidean inverse gcd')
            z = divrem(trim([x * pow(r0[0], -1, P) for x in t0]), self.modulus)[1]
            z = tuple(z + [0] * (D - len(z)))
            require(self.mul(a, z) == ONE, 'Euclidean inverse check')
            self.inverses[a] = z
        return self.inverses[a]

def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()

def validate_schema(data, f):
    require(data['degree'] == D and data['characteristic'] == P, 'field metadata')
    require(data['field_modulus_ascending'] == f.modulus, 'field representation')
    y, z = f.element(data['y']), f.element(data['z'])
    require(y != ZERO and z != ZERO, 'nonzero independent cross nodes')
    roots = [f.element(x) for x in data['roots']]
    h = [f.element(x) for x in data['H']]
    require(len(roots) == 7 and len(set(roots)) == 7 and ZERO not in roots, 'seven actual distinct nonzero roots')
    require(len(h) == 8 and h[-1] == ONE and h[0] != ZERO, 'monic support annihilator')
    product = [ONE]
    for x in roots:
        v = [ZERO] * (len(product) + 1)
        for i, c in enumerate(product):
            v[i] = f.sub(v[i], f.mul(x, c))
            v[i + 1] = f.add(v[i + 1], c)
        product = v
    require(product == h, 'support polynomial product')
    require(len(data['banks']) == 16, 'sixteen original banks')
    counts, supports = {}, {}
    for b in data['banks']:
        e, d = b['epsilon'], b['delta']
        require(type(e) is int and type(d) is int and e in (-1, 1) and d in (-1, 1), 'signed orientations')
        alpha, guard = f.element(b['alpha']), f.element(b['guard'])
        require(alpha != ZERO and type(b['beta']) is int and b['beta'] == 1, 'constructive beta-one subfamily')
        require(len(b['amplitudes']) == len(b['weights']) == 13, 'thirteen weights and amplitudes per bank')
        for value in b['amplitudes'] + b['weights']:
            f.element(value)
        actual_guard = f.sub(ONE, f.add(f.power(alpha, 13), f.scalar(pow(b['beta'], 13, P))))
        require(guard == actual_guard and guard != ZERO, 'original pole guard')
        counts[e, d] = counts.get((e, d), 0) + 1
        supports.setdefault((e, d), []).append(alpha)
    require(counts == {(1, 1): 7, (-1, 1): 1, (1, -1): 1, (-1, -1): 7}, 'allocation 7,1,1,7')
    require(set(supports[1, 1]) == set(supports[-1, -1]) == set(roots), 'same-sign support binding')
    require(supports[-1, 1] == [y] and supports[1, -1] == [z], 'cross-node binding')
    require(len(data['matrix']) == 13 and all(len(row) == 13 for row in data['matrix']), 'stored target shape')
    for r, row in enumerate(data['matrix']):
        for c, value in enumerate(row):
            require(f.element(value) == f.scalar(pow(QROOT, (-r * c) % N, P)), 'stored negative Fourier target')
    return roots

def gaussian_tables():
    # Pascal recurrence, independent of the candidate's quotient product.
    tables = {}
    for e in (-1, 1):
        for d in (-1, 1):
            omega = pow(QROOT, (e * d) % N, P)
            table = [[0] * N for _ in range(N)]
            table[0][0] = 1
            for n in range(1, N):
                table[n][0] = table[n][n] = 1
                for k in range(1, n):
                    table[n][k] = (table[n - 1][k - 1] + pow(omega, k, P) * table[n - 1][k]) % P
            tables[e, d] = table
    return tables

def check_weights(data, f, gamma):
    checks = 0
    for bank in data['banks']:
        guard = tuple(bank['guard'])
        amps = list(map(tuple, bank['amplitudes']))
        weights = list(map(tuple, bank['weights']))
        e = bank['epsilon']
        for j in range(N):
            v = ZERO
            for b in range(N):
                v = f.add(v, f.scale(amps[b], pow(QROOT, (-e * b * j) % N, P)))
            require(f.mul(f.scale(guard, gamma), v) == weights[j], 'raw weight forward transform')
            checks += 1
        for b in range(N):
            v = ZERO
            for j in range(N):
                v = f.add(v, f.scale(weights[j], pow(QROOT, (e * b * j) % N, P)))
            require(f.mul(v, f.inverse(f.scale(guard, N * gamma))) == amps[b], 'amplitude inverse transform')
            checks += 1
    return checks

def branch_adjugate(f, alpha_powers, guard_inverse, e, d, j):
    diagonal = [(1 - pow(QROOT, (e * d * j + d * r) % N, P)) % P for r in range(N)]
    require(diagonal.count(0) == 1, 'one zero branch diagonal')
    inverse = [[ZERO] * N for _ in range(N)]
    for c in range(N):
        for distance in range(N):
            r = (c + e * distance) % N
            # Cofactor = alpha^distance times the product outside the
            # directed path c,c+epsilon,...,r. The determinant is the guard.
            coeff = 1
            for offset in range(distance + 1, N):
                coeff = coeff * diagonal[(c + e * offset) % N] % P
            inverse[r][c] = f.scale(f.mul(alpha_powers[distance], guard_inverse), coeff)
    return diagonal, inverse

def verify(data, f, quiet=False):
    roots = validate_schema(data, f)
    require(pow(QROOT, N, P) == 1 and all(pow(QROOT, k, P) != 1 for k in range(1, N)), 'exact order thirteen')
    invn = pow(N, -1, P)
    gamma = sum(pow(QROOT, (-t * t) % N, P) for t in range(N)) * invn % P
    require(gamma == 7, 'Gauss normalization')
    weight_checks = check_weights(data, f, gamma)
    tables = gaussian_tables()
    total = [[ZERO] * N for _ in range(N)]
    bank_hashes, inverse_hashes, nonzero_counts = [], [], []
    sector_sums = [[ZERO] * N for _ in range(N)]
    inverse_equalities = bank_weyl_equalities = 0
    last_inverse = None
    for bi, bank in enumerate(data['banks']):
        e, d = bank['epsilon'], bank['delta']
        alpha, guard = tuple(bank['alpha']), tuple(bank['guard'])
        amps, weights = list(map(tuple, bank['amplitudes'])), list(map(tuple, bank['weights']))
        powers = [ONE]
        for k in range(13):
            powers.append(f.mul(powers[-1], alpha))
        require(guard == f.scale(powers[13], -1), 'beta-one determinant')
        gi = f.inverse(guard)
        matrix = [[ZERO] * N for _ in range(N)]
        for j in range(N):
            diagonal, inv = branch_adjugate(f, powers, gi, e, d, j)
            for r in range(N):
                for c in range(N):
                    ident = ONE if r == c else ZERO
                    # These are actual sparse products M V and V M, with
                    # M[r,r]=diag[r], M[r+epsilon,r]=-alpha.
                    left = f.sub(f.scale(inv[r][c], diagonal[r]), f.mul(alpha, inv[(r - e) % N][c]))
                    right = f.sub(f.scale(inv[r][c], diagonal[c]), f.mul(alpha, inv[r][(c + e) % N]))
                    require(left == ident and right == ident, 'both original inverse orders')
                    inverse_equalities += 2
                    matrix[r][c] = f.add(matrix[r][c], f.scale(f.mul(weights[j], inv[r][c]), invn))
            inverse_hashes.append(digest(inv))
            last_inverse = inv
        nonzero = sum(x != ZERO for row in matrix for x in row)
        require(nonzero > 0, 'every original bank effective')
        nonzero_counts.append(nonzero)
        bank_hashes.append(digest(matrix))
        for a in range(N):
            for b in range(N):
                weyl = ZERO
                for t in range(N):
                    weyl = f.add(weyl, f.scale(matrix[(t + a) % N][t], invn * pow(QROOT, (-b * t) % N, P)))
                r, ell = (e * a) % N, (d * b) % N
                g = 0 if r + ell >= N else tables[e, d][r + ell][ell]
                normalized = f.scale(f.mul(powers[r], amps[b]), g)
                require(weyl == f.scale(normalized, gamma), 'literal bank versus independent Weyl expansion')
                bank_weyl_equalities += 1
                sector_sums[a][b] = f.add(sector_sums[a][b], normalized)
                total[a][b] = f.add(total[a][b], matrix[a][b])
        if not quiet:
            print('reviewed original bank', bi + 1, flush=True)
    sectors, target_checks, opposite_sign, omitted_normalization, weight_perturbation = 0, 0, 0, 0, 0
    target_weyl = []
    for a in range(N):
        row = []
        for b in range(N):
            direct = sum(pow(QROOT, (-(t + a) * t - b * t) % N, P) for t in range(N)) * invn % P
            normalized = direct * pow(gamma, -1, P) % P
            require(normalized == pow(QROOT, 10 * (a + b) ** 2 % N, P), 'direct target Weyl extraction')
            require(sector_sums[a][b] == f.scalar(normalized), 'full sector equation')
            row.append(direct)
            sectors += 1
            target = f.scalar(pow(QROOT, (-a * b) % N, P))
            require(total[a][b] == target == tuple(data['matrix'][a][b]), 'literal negative unnormalized Fourier equality')
            target_checks += 1
            opposite_sign += total[a][b] != f.scalar(pow(QROOT, (a * b) % N, P))
            omitted_normalization += f.scale(total[a][b], N) != target
            weight_perturbation += f.add(total[a][b], f.scale(last_inverse[a][b], invn)) != target
        target_weyl.append(row)
    require(min(opposite_sign, omitted_normalization, weight_perturbation) > 0, 'semantic mutation controls')
    rootset = set(roots)
    orbit_lengths = []
    for x in roots + [tuple(data['y']), tuple(data['z'])]:
        y = x
        for period in range(1, D + 1):
            y = f.power(y, P)
            if y == x:
                break
        require(y == x, 'Frobenius orbit closes')
        orbit_lengths.append(period)
    return {'verdict': 'PASS', 'degree': D, 'field_order': str(ORDER), 'field_order_bits': ORDER.bit_length(),
        'field_proof': f.field_proof, 'banks': 16, 'roots': 7, 'pole_guards': 16,
        'raw_weights': 208, 'amplitudes': 208, 'raw_and_inverse_transform_equalities': weight_checks,
        'original_branches': 208, 'inverse_orders': 416, 'inverse_entry_equalities': inverse_equalities,
        'bank_weyl_equalities': bank_weyl_equalities, 'sector_equalities': sectors,
        'target_entry_equalities': target_checks, 'target_weyl_coefficients': target_weyl,
        'nonzero_bank_entry_counts': nonzero_counts, 'inverse_matrix_sha256': inverse_hashes,
        'bank_matrix_sha256': bank_hashes, 'node_frobenius_orbit_lengths': orbit_lengths,
        'nonstable_support': {f.power(x, P) for x in roots} != rootset,
        'semantic_mutations': {'opposite_Fourier_sign_mismatches': opposite_sign,
            'omitted_one_over_13_mismatches': omitted_normalization,
            'last_raw_weight_plus_one_mismatches': weight_perturbation},
        'method': 'Fresh Python ordinary-convolution field arithmetic; Euclidean inverses; closed cyclic adjugates; literal sparse inverse products; direct Fourier/Weyl extraction and Pascal Gaussian coefficients.'}

def mutation_controls(data, f):
    gamma = 7
    mutations = []
    def reject(name, change, check):
        bad = copy.deepcopy(data)
        change(bad)
        try:
            check(bad)
        except ValueError as exc:
            mutations.append({'name': name, 'verdict': 'REJECTED', 'check': str(exc)})
        else:
            raise ValueError('Mutation incorrectly accepted: ' + name)
    def bump(vec):
        vec[0] = (vec[0] + 1) % P
    reject('noncanonical coordinate', lambda x: x['y'].__setitem__(0, P), lambda x: validate_schema(x, f))
    reject('zero original guard', lambda x: x['banks'][0].__setitem__('guard', list(ZERO)), lambda x: validate_schema(x, f))
    reject('one raw weight plus one', lambda x: bump(x['banks'][-1]['weights'][-1]), lambda x: check_weights(x, f, gamma))
    reject('one amplitude plus one', lambda x: bump(x['banks'][0]['amplitudes'][0]), lambda x: check_weights(x, f, gamma))
    reject('one target entry plus one', lambda x: bump(x['matrix'][0][0]), lambda x: validate_schema(x, f))
    reject('duplicate support root', lambda x: x['roots'].__setitem__(1, x['roots'][0][:]), lambda x: validate_schema(x, f))
    # A reducible degree-31 polynomial must be rejected before inversion.
    try:
        Field([0] * D + [1])
    except ValueError as exc:
        mutations.append({'name': 'reducible modulus X31', 'verdict': 'REJECTED', 'check': str(exc)})
    else:
        raise ValueError('Reducible modulus accepted')
    return mutations

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('certificate', type=Path)
    parser.add_argument('--output', type=Path, default=Path('LITERAL_REVIEW.json'))
    parser.add_argument('--quiet', action='store_true')
    args = parser.parse_args()
    raw = args.certificate.read_bytes()
    data = json.loads(raw)
    f = Field(data['field_modulus_ascending'])
    receipt = verify(data, f, args.quiet)
    receipt['inert_json_mutations'] = mutation_controls(data, f)
    receipt['certificate_sha256'] = hashlib.sha256(raw).hexdigest()
    receipt['checker_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    args.output.write_text(json.dumps(receipt, indent=2) + '\n')
    print('PASS: 16 original banks, 208 branches, 169 negative Fourier entries; all 13 sectors and mutation controls.')

if __name__ == '__main__':
    main()
