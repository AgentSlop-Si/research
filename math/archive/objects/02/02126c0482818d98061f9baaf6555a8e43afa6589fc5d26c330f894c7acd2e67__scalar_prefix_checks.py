"""Independent exact complex-rational checks of six-instruction shear prefixes.

Standard library only. No source code is imported and no numerical SVD is used.
Frobenius norm squares certify upper bounds on both spectral norms.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path
import json


@dataclass(frozen=True)
class QI:
    real: F = F(0)
    imag: F = F(0)

    def __post_init__(self):
        object.__setattr__(self, 'real', F(self.real))
        object.__setattr__(self, 'imag', F(self.imag))

    def __add__(self, other):
        other = qi(other)
        return QI(self.real + other.real, self.imag + other.imag)

    def __neg__(self):
        return QI(-self.real, -self.imag)

    def __sub__(self, other):
        return self + (-qi(other))

    def __mul__(self, other):
        other = qi(other)
        return QI(self.real * other.real - self.imag * other.imag,
                  self.real * other.imag + self.imag * other.real)

    def __truediv__(self, other):
        other = qi(other)
        den = other.abs_squared()
        assert den != 0
        product = self * QI(other.real, -other.imag)
        return QI(product.real / den, product.imag / den)

    def abs_squared(self):
        return self.real ** 2 + self.imag ** 2


def qi(value):
    return value if isinstance(value, QI) else QI(value)


def identity():
    return [[QI(1), QI()], [QI(), QI(1)]]


def mul(a, b):
    return [[sum_qi(a[i][k] * b[k][j] for k in range(2))
             for j in range(2)] for i in range(2)]


def sum_qi(values):
    out = QI()
    for value in values:
        out = out + value
    return out


def inv(a):
    d = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    return [[a[1][1] / d, -a[0][1] / d],
            [-a[1][0] / d, a[0][0] / d]]


def frobenius_squared(a):
    return sum((v.abs_squared() for row in a for v in row), F(0))


def ratio(value):
    value = F(value)
    return {'numerator': str(value.numerator), 'denominator': str(value.denominator)}


def check_word(coefficients, a):
    g, c = 2 ** a, 2 ** (a + 1)
    length = len(coefficients)
    assert all(alpha.abs_squared() <= g * g for alpha in coefficients)
    p = identity()
    largest_norm_squared = F(0)
    largest_inverse_squared = F(0)
    envelope_squared = F(2 ** (2 * length * (a + 1) + 4))
    instructions = 0
    for index, alpha in enumerate(coefficients):
        source, target = index % 2, 1 - index % 2
        before, local = p, identity()
        for beta in (QI(c), alpha - QI(c)):
            assert F(c * c, 4) <= beta.abs_squared() <= F(9 * c * c, 4)
            scale, addition, unscale = identity(), identity(), identity()
            scale[source][source] = beta
            addition[target][source] = QI(1)
            unscale[source][source] = QI(1) / beta
            for instruction in (scale, addition, unscale):
                p = mul(instruction, p)
                local = mul(instruction, local)
                assert mul(p, inv(p)) == identity()
                # An exact rational certificate for the local 4C strong bound.
                assert frobenius_squared(local) <= (4 * c) ** 2
                assert frobenius_squared(inv(local)) <= (4 * c) ** 2
                norm_sq, inverse_sq = frobenius_squared(p), frobenius_squared(inv(p))
                assert norm_sq <= envelope_squared and inverse_sq <= envelope_squared
                largest_norm_squared = max(largest_norm_squared, norm_sq)
                largest_inverse_squared = max(largest_inverse_squared, inverse_sq)
                instructions += 1
        expected = identity()
        expected[target][source] = alpha
        assert local == expected and p == mul(expected, before)
    assert instructions == 6 * length
    return {
        'shears': length, 'scalar_prefixes': instructions, 'A': a, 'C': c,
        'maximum_prefix_frobenius_norm_squared': ratio(largest_norm_squared),
        'maximum_prefix_inverse_frobenius_norm_squared': ratio(largest_inverse_squared),
        'strong_spectral_envelope_squared': ratio(envelope_squared),
        'completed_word_matches_shears': True,
    }


def run():
    cases = [check_word([QI(0), QI(1), QI(-1)], 0),
             check_word([QI(0), QI(1), QI(-1), QI(F(3, 2)), QI(F(-7, 3)),
                         QI(F(3, 5), F(4, 5)), QI(1, 2)], 2)]
    result = {
        'status': 'PASS', 'arithmetic': 'Gaussian rationals via fractions.Fraction',
        'word_cases': len(cases), 'scalar_prefixes': sum(c['scalar_prefixes'] for c in cases),
        'details': cases,
        'scope': 'Exact small-prefix certificate checks, not an FFT or proof of asymptotic cost.',
    }
    path = Path(__file__).with_name('scalar_prefix_certificates.json')
    path.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'details'}))


if __name__ == '__main__':
    run()
