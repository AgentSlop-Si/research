"""Fresh certified all-length positive DFT fallback. Standard library only.

Every returned component is an exact Fraction with power-of-two denominator.
The numerical backend uses integer fixed grids; roots use exact rationals.
No floating-point function, external package, or historical source is run.
"""
from fractions import Fraction as F
from dataclasses import dataclass, asdict
from collections import Counter


def bitwidth(v):
    if isinstance(v, F):
        return max(abs(v.numerator).bit_length(), v.denominator.bit_length())
    return abs(v).bit_length()


class Meter:
    def __init__(self):
        self.counts = Counter()
        self.widths = Counter()
    def record(self, phase, operation, *values, count=1):
        self.counts[phase + ':' + operation] += count
        for v in values:
            self.widths[phase] = max(self.widths[phase], bitwidth(v))
    def export(self):
        return {'counts': dict(sorted(self.counts.items())),
                'max_operand_or_result_bits': dict(sorted(self.widths.items()))}


@dataclass(frozen=True)
class FailureCharge:
    """A pass-through charge from an already performed unsuccessful front end.

    Scalar operations/width summarize its invoice; bit_cost_expression is a
    symbolic upper bound, not an observed CPU instruction count. The caller
    remains responsible for a truthful and complete front-end invoice.
    """
    label: str
    scalar_operations: int
    operand_bits: int
    bit_cost_expression: str
    detail: str = ''
    def validate(self):
        if (not isinstance(self.label, str) or not self.label or
            type(self.scalar_operations) is not int or self.scalar_operations < 0 or
            type(self.operand_bits) is not int or self.operand_bits < 0 or
            not isinstance(self.bit_cost_expression, str) or not self.bit_cost_expression or
            not isinstance(self.detail, str)):
            raise ValueError('malformed failed-work invoice')


def round_ratio(n, d):
    """Nearest integer, ties toward positive infinity; d is positive."""
    return (2*n + d) // (2*d)


def round_fraction(v, scale, meter=None, phase='roots'):
    n = v.numerator * scale
    q = round_ratio(n, v.denominator)
    if meter:
        meter.record(phase, 'rational_to_grid', v, n, q, scale)
    return q


def cadd(a, b):
    return (a[0]+b[0], a[1]+b[1])


def csub(a, b):
    return (a[0]-b[0], a[1]-b[1])


def cmul(a, b, divisor, meter, phase):
    # Both output components are rounded only once; l1 error <= one output ulp.
    ar, ai = a; br, bi = b
    rr = ar*br-ai*bi; ii = ar*bi+ai*br
    z = (round_ratio(rr, divisor), round_ratio(ii, divisor))
    meter.record(phase, 'complex_multiply_round', ar, ai, br, bi, rr, ii, *z, divisor)
    return z


class RootFactory:
    """Roots exp(2*pi*i*k/n), grid 2^(-p-4), certified l1 error <= 2^-p."""
    def __init__(self, p, meter):
        self.p = p; self.h = F(1, 1 << p); self.scale = 1 << (p+4)
        self.meter = meter
        limit = self.h / 65536
        def atan_inverse(q):
            total = F(0); qpow = q; j = 0; sign = 1
            while True:
                term = F(sign, (2*j+1)*qpow)
                total += term
                meter.record('roots', 'atan_term', total, term, qpow)
                j += 1; sign = -sign; qpow *= q*q
                remainder = F(1, (2*j+1)*qpow)
                meter.record('roots', 'atan_stop_compare', remainder, limit, qpow)
                if remainder <= limit:
                    return total, remainder
        a, ea = atan_inverse(5); b, eb = atan_inverse(239)
        raw = 16*a-4*b
        pi_scale = 1 << (p+12)
        self.pi = F(round_fraction(raw, pi_scale, meter), pi_scale)
        self.pi_error = 16*ea+4*eb+abs(self.pi-raw)
        meter.record('roots', 'machin_combine', raw, self.pi, self.pi_error)
        # Degree m with the ordinary Taylor Lagrange bound for both components.
        m = 0; remainder = F(4)
        while remainder > self.h/128:
            m += 1; remainder *= F(4, m+1)
            meter.record('roots', 'degree_selection', remainder, m)
        self.degree = m; self.taylor_error = remainder
        self.root_count = 0
        self.max_radius = F(0)
    def root(self, k, n):
        k %= n
        if 2*k > n:
            k -= n
        angle = F(2*k, n)*self.pi
        if abs(angle) >= 4:
            raise ArithmeticError('certified argument reduction failed')
        term = F(1); re = F(0); im = F(0)
        for j in range(self.degree+1):
            if j:
                term *= angle/F(j)
            residue = j % 4
            if residue == 0: re += term
            elif residue == 1: im += term
            elif residue == 2: re -= term
            else: im -= term
            self.meter.record('roots', 'taylor_term', term, re, im, angle)
        qr = round_fraction(re, self.scale, self.meter)
        qi = round_fraction(im, self.scale, self.meter)
        radius = (2*self.pi_error + 2*self.taylor_error +
                  abs(F(qr,self.scale)-re)+abs(F(qi,self.scale)-im))
        self.meter.record('roots', 'radius_verification', radius, self.h)
        if radius > self.h:
            raise ArithmeticError('root certificate failed')
        self.max_radius = max(self.max_radius, radius)
        self.root_count += 1
        return qr, qi


def radix2(values, roots, sign, p, meter):
    """Unnormalized sign +/- DFT; radix-2 DIT with explicit bit reversal."""
    a = list(values); length = len(a); levels = length.bit_length()-1
    if length != 1 << levels or sign not in (-1,1):
        raise ValueError('invalid radix-2 call')
    j = 0
    for i in range(1,length):
        bit = length >> 1
        while j & bit:
            j ^= bit; bit >>= 1
            meter.record('fft', 'bit_reversal_step', j, bit)
        j ^= bit
        if i < j: a[i],a[j] = a[j],a[i]
        meter.record('fft', 'permutation_index', i, j)
    span = 2
    while span <= length:
        half = span//2; stride = length//span
        for start in range(0,length,span):
            for j in range(half):
                root = roots[j*stride]
                if sign == -1: root = root[0], -root[1]
                u = a[start+j]
                v = cmul(a[start+j+half], root, 1 << (p+4), meter, 'fft')
                plus,minus = cadd(u,v),csub(u,v)
                a[start+j],a[start+j+half] = plus,minus
                meter.record('fft', 'butterfly_add_subtract', *u, *v, *plus, *minus)
        span *= 2
    meter.record('fft', 'transform', count=1)
    return a


def validate(x, epsilon, cap=None):
    if not isinstance(x, (tuple,list)) or not x:
        raise ValueError('N must be positive')
    if not isinstance(epsilon, (int,F)) or isinstance(epsilon,bool):
        raise ValueError('tolerance must be exact rational')
    epsilon = F(epsilon)
    if not 0 < epsilon <= 1:
        raise ValueError('tolerance outside (0,1]')
    if cap is not None and (type(cap) is not int or not 0 <= cap < len(x)):
        raise ValueError('malformed recurrence cap')
    clean = []; b = 0; S = F(0)
    for z in x:
        if not isinstance(z,(tuple,list)) or len(z) != 2:
            raise ValueError('complex data must be exact component pairs')
        pair=[]
        for value in z:
            if not isinstance(value,(int,F)) or isinstance(value,bool):
                raise ValueError('components must be exact integers or Fractions')
            value=F(value); denominator=value.denominator
            if denominator & (denominator-1):
                raise ValueError('non-dyadic input')
            b=max(b,denominator.bit_length()-1)
            pair.append(value); S += abs(value)
        clean.append(tuple(pair))
    return clean,epsilon,b,S


def certified_dft(x, epsilon, failed_work=(), cap=None):
    """Total fallback, not recurrence discovery. Preserve all predecessor charges.

    cap is optional validation metadata, not a trigger to redo discovery. Calling
    this function directly is an explicit choice of the fallback interface.
    """
    x,epsilon,b,S=validate(x,epsilon,cap)
    failed_work=tuple(failed_work)
    for charge in failed_work:
        if not isinstance(charge,FailureCharge):
            raise ValueError('failed-work invoice type')
        charge.validate()
    N=len(x); meter=Meter()
    meter.record('input','complex_components',count=2*N)
    for z in x:
        meter.record('input','exact_validation',*z)
    meter.record('input','tolerance_validation',epsilon)
    predecessor=[asdict(charge) for charge in failed_work]
    base={'N':N,'cap':cap,'failed_work':predecessor,
          'failed_scalar_operations':sum(c.scalar_operations for c in failed_work),
          'failed_bit_cost_sum':[c.bit_cost_expression for c in failed_work]}
    if N == 1 or S == 0:
        y=list(x) if N==1 else [(F(0),F(0)) for _ in x]
        meter.record('output','complex_write',count=N)
        base.update(branch='exact_copy' if N==1 else 'exact_zero',p=b,L=1,
                    absolute_error_bound=F(0),meter=meter.export(),root_count=0)
        return y,base
    L=1
    while L < 2*N-1: L <<= 1
    ell=L.bit_length()-1
    C=2*L*(2*ell+3)
    D=(S+1)*((L+1)*C+C*C)+1
    K=4*D+4*(ell+1)*(S*L+1)+S+3
    p=b; Q=1 << p
    while Q < L or K/Q > epsilon:
        p += 1; Q <<= 1
        meter.record('precision','selection_iteration',Q,K,epsilon)
    h=F(1,Q)
    roots=RootFactory(p,meter)
    chirps=[roots.root(j*j,2*N) for j in range(N)]
    twiddles=[roots.root(j,L) for j in range(L//2)]
    a=[(0,0)]*L; bb=[(0,0)]*L
    for j,z in enumerate(x):
        zz=tuple(v.numerator*(Q//v.denominator) for v in z)
        a[j]=cmul(zz,chirps[j],16*Q,meter,'chirp_input')
        r=(chirps[j][0],-chirps[j][1])
        # Retain b on the root grid h/16. All FFT arrays use this grid.
        bb[j]=r
        if j: bb[L-j]=r
    # a was rounded to h, but FFT common grid is h/16. This only improves
    # every butterfly and product rounding bound used in the proof.
    a=[(16*z[0],16*z[1]) for z in a]
    AA=radix2(a,twiddles,1,p,meter)
    BB=radix2(bb,twiddles,1,p,meter)
    PP=[cmul(aa,bb,16*Q,meter,'pointwise') for aa,bb in zip(AA,BB)]
    inv=radix2(PP,twiddles,-1,p,meter)
    y=[]
    for k in range(N):
        # Divide by L and convert h/16 -> h in one correctly rounded operation.
        conv=(round_ratio(inv[k][0],16*L),round_ratio(inv[k][1],16*L))
        meter.record('normalization','complex_divide_round',*inv[k],*conv,16*L)
        val=cmul(conv,chirps[k],16*Q,meter,'chirp_output')
        y.append((F(val[0],Q),F(val[1],Q)))
        meter.record('output','complex_write',*val)
    # Store a compact outward radius receipt, not enormous transient fractions.
    radius_units=(roots.max_radius*Q*256)
    radius_units=-(-radius_units.numerator//radius_units.denominator)
    base.update(branch='bluestein_radix2',L=L,ell=ell,p=p,raw_denominator_bits=b,
                S=S,C=C,D=D,K=K,absolute_error_bound=K*h,
                root_error_bound=F(radius_units,Q*256),root_count=roots.root_count,
                root_taylor_degree=roots.degree,meter=meter.export(),
                expected_butterflies=3*(L//2)*ell,
                fft_data_fractional_bits=p+4)
    assert base['absolute_error_bound'] <= epsilon
    assert base['root_error_bound'] <= h
    assert meter.counts['fft:complex_multiply_round'] == base['expected_butterflies']
    return y,base
