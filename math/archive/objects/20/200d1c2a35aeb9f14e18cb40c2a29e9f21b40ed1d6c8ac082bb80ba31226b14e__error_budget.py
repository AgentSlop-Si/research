"""Conditional coefficient-rounding certificates, using rational bounds."""
from fractions import Fraction
import math


def _ceil_norm(values):
    square=sum(int(v)**2 for v in values)
    root=math.isqrt(square)
    return root+int(root*root!=square)


def convolution_rounding_bound(a,b,epsilon_a,epsilon_b,epsilon_inverse=0,roundoff=0):
    """Sufficient bound assuming the stated transform errors REALLY hold.

    Merely supplying a Monte-Carlo probability bound does not verify that event.
    roundoff is an externally certified absolute coefficient-error allowance.
    """
    a,b=list(a),list(b)
    if not a or not b or any(not isinstance(v,int) for v in a+b):
        raise ValueError('nonempty integer coefficient vectors required')
    ea,eb,ei,rho=map(Fraction,(epsilon_a,epsilon_b,epsilon_inverse,roundoff))
    if min(ea,eb,ei,rho)<0:raise ValueError('error allowances must be nonnegative')
    la,lb=sum(abs(v) for v in a),sum(abs(v) for v in b)
    qa,qb=_ceil_norm(a),_ceil_norm(b)
    forward=ea*la*qb+eb*lb*qa+ea*eb*la*lb
    inverse=ei*(qa+ea*la)*(qb+eb*lb)
    total=forward+inverse+rho
    return {'forward_product_error_bound':forward,
            'inverse_error_bound':inverse,'roundoff_allowance':rho,
            'total_coefficient_error_bound':total,
            'conditionally_safe_nearest_integer_rounding':total<Fraction(1,2),
            'norm_one_a':la,'norm_one_b':lb,'norm_two_upper_a':qa,'norm_two_upper_b':qb}


def unique_integer_from_interval(lower,upper):
    """Return the unique integer in an externally certified closed interval."""
    lower,upper=Fraction(lower),Fraction(upper)
    if lower>upper:raise ValueError('reversed interval')
    lo=-(-lower.numerator//lower.denominator)
    hi=upper.numerator//upper.denominator
    if lo!=hi:raise ValueError('interval does not contain exactly one integer')
    return lo
