"""Certified Q16 compact-window preparation. No recovery engine or floating numerics.

All interval endpoints are integers on an explicit binary grid. The exact
coefficient generator is independent of the rounded transcendental evaluator.
This is a candidate component, with separate reduced-fixture and theorem APIs.
"""
from dataclasses import dataclass, field
from fractions import Fraction
from collections import Counter


class CertificationError(ArithmeticError):
    pass


def integer(x, name, lower=0):
    if type(x) is not int or x < lower:
        raise ValueError(f'{name} must be an integer >= {lower}')
    return x


def power_two(x):
    return type(x) is int and x > 0 and x & (x - 1) == 0


@dataclass
class Ledger:
    operations: Counter = field(default_factory=Counter)
    arithmetic_bit_work_upper: int = 0
    cumulative_integer_bits: int = 0
    max_integer_bits: int = 1
    allocated_slots: int = 0
    parameter_input_bits: int = 0
    max_parameter_bits: int = 1
    def record(self, kind, inputs, output):
        # A conservative schoolbook arithmetic model, not a CPU timer.
        sizes = [max(1, abs(x).bit_length()) for x in (*inputs, output)]
        b = sum(sizes) + 2
        self.operations[kind] += 1
        self.arithmetic_bit_work_upper += 16 * b * b
        self.cumulative_integer_bits += sizes[-1] + 1
        self.max_integer_bits = max(self.max_integer_bits, *sizes)
        return output
    def parameter(self, value):
        if type(value) is not int: raise ValueError('integer parameter required')
        bits=max(1,abs(value).bit_length())
        self.parameter_input_bits += bits
        self.max_parameter_bits=max(self.max_parameter_bits,bits)
        return self.record('parameter_input',(),value)
    def add(self, a, b): return self.record('add', (a,b), a+b)
    def sub(self, a, b): return self.record('subtract', (a,b), a-b)
    def mul(self, a, b): return self.record('multiply', (a,b), a*b)
    def div(self, a, b):
        if b == 0: raise ZeroDivisionError('integer denominator is zero')
        return self.record('floor_divide', (a,b), a//b)
    def ceildiv(self, a, b): return self.sub(0, self.div(self.sub(0,a),b))
    def mod(self, a, b): return self.record('modulo', (a,b), a%b)
    def power(self, a, n):
        integer(n, 'exponent')
        ans = 1
        self.record('power_input', (a,n), 1)
        while n:
            if n & 1: ans = self.mul(ans,a)
            n = self.div(n,2)
            if n: a = self.mul(a,a)
        return ans
    def shift(self, n):
        integer(n, 'binary exponent')
        return self.record('binary_power', (n,), 1 << n)
    def allocate(self, n):
        self.allocated_slots += n
        self.operations['allocated_slots'] += n
        # Zero initialized numeric slots are paid here.
        self.cumulative_integer_bits += n
    def event(self, name, count=1): self.operations[name] += count
    def report(self):
        events = sum(self.operations.values()) + 256
        width = self.max_integer_bits + events.bit_length() + 2
        # Explicit envelope for address/index arithmetic, comparisons, branches,
        # counters, loop bounds and fixed setup formulas not individually traced.
        controls = 512 * events * width * width
        # Deliberately cumulative allocation upper bound, not peak measurement.
        storage = self.cumulative_integer_bits + 512 * events * width
        return dict(operations=dict(sorted(self.operations.items())),
                    arithmetic_bit_work_upper=self.arithmetic_bit_work_upper,
                    bookkeeping_bit_work_upper=controls,
                    total_bit_work_upper=self.arithmetic_bit_work_upper+controls,
                    cumulative_storage_upper_bits=storage,
                    max_observed_integer_bits=self.max_integer_bits,
                    allocated_slots=self.allocated_slots,
                    parameter_input_bits=self.parameter_input_bits,
                    max_parameter_bits=self.max_parameter_bits,
                    model='schoolbook binary arithmetic plus conservative control and cumulative-storage envelope; excludes Python runtime and test oracle')


@dataclass(frozen=True)
class Interval:
    lo: int
    hi: int
    bits: int
    def __post_init__(self):
        if (any(type(x) is not int for x in (self.lo,self.hi,self.bits))
                or self.lo > self.hi or self.bits < 0):
            raise ValueError('invalid dyadic interval')
    def as_fractions(self):
        return Fraction(self.lo, 1 << self.bits), Fraction(self.hi, 1 << self.bits)


def quantize(a, bits, L):
    if a.bits <= bits:
        k = L.shift(bits-a.bits)
        return Interval(L.mul(a.lo,k), L.mul(a.hi,k),bits)
    k = L.shift(a.bits-bits)
    return Interval(L.div(a.lo,k), L.ceildiv(a.hi,k),bits)


def clipped(a, lo, hi, L):
    L.event('interval_intersection')
    if a.hi < lo or a.lo > hi:
        raise CertificationError('analytic enclosure and computed interval are disjoint')
    return Interval(max(a.lo,lo),min(a.hi,hi),a.bits)


def quotient(a,b,L):
    if a.bits != b.bits: raise ValueError('quotient grids differ')
    if b.lo <= 0 <= b.hi: raise ZeroDivisionError('interval denominator contains zero')
    S=L.shift(a.bits)
    lows=[]; highs=[]; L.allocate(8)
    for x in (a.lo,a.hi):
        for y in (b.lo,b.hi):
            n=L.mul(x,S)
            lows.append(L.div(n,y)); highs.append(L.ceildiv(n,y))
    return Interval(min(lows),max(highs),a.bits)


def even_power(a,n,L):
    integer(n,'even exponent',2)
    if n%2: raise ValueError('even exponent required')
    small=0 if a.lo <= 0 <= a.hi else min(abs(a.lo),abs(a.hi))
    large=max(abs(a.lo),abs(a.hi))
    den=L.shift(L.mul(a.bits,L.sub(n,1)))
    return Interval(L.div(L.power(small,n),den),
                    L.ceildiv(L.power(large,n),den),a.bits)


@dataclass(frozen=True)
class Coefficients:
    ell: int
    r: int
    radius: int
    numerators: tuple
    denominator: int


def exact_box_power(ell,r,ledger=None):
    """Exact integer sliding convolution, no sine, roots, floats or FFT."""
    if not power_two(ell) or ell < 2: raise ValueError('ell must be a power of two >=2')
    integer(r,'r',1)
    L=ledger if ledger is not None else Ledger()
    L.record('input',(),ell); L.record('input',(),r)
    old=[1]; L.allocate(1)
    for _ in range(L.mul(2,r)):
        size=L.sub(L.add(len(old),ell),1)
        new=[0]*size; L.allocate(size)
        running=0
        for i in range(size):
            L.event('coefficient_cell')
            if i<len(old): running=L.add(running,old[i])
            previous=L.sub(i,ell)
            if 0<=previous<len(old): running=L.sub(running,old[previous])
            new[i]=running
        old=new
    den=L.power(ell,L.mul(2,r))
    radius=L.mul(r,L.sub(ell,1))
    return Coefficients(ell,r,radius,tuple(old),den)


class Scalar:
    """Finite, predetermined Machin / point-Taylor dyadic enclosures."""
    def __init__(self,bits,ledger):
        integer(bits,'scalar bits',16)
        self.bits=bits; self.L=ledger; self.S=ledger.shift(bits)
        self.terms=ledger.add(bits,8)
        self.pi=self._pi()
        self.sine_calls=0
    def _atan(self,q):
        L=self.L; S=self.S; n=self.terms
        qp=q; q2=L.mul(q,q); lo=hi=0
        for k in range(n):
            d=L.mul(L.add(L.mul(2,k),1),qp)
            a=L.div(S,d); b=L.ceildiv(S,d)
            if k%2: lo=L.sub(lo,b); hi=L.sub(hi,a)
            else: lo=L.add(lo,a); hi=L.add(hi,b)
            qp=L.mul(qp,q2)
            L.event('atan_term')
        tail=L.ceildiv(S,L.mul(L.add(L.mul(2,n),1),qp))
        if n%2: lo=L.sub(lo,tail)
        else: hi=L.add(hi,tail)
        return Interval(lo,hi,self.bits)
    def _pi(self):
        L=self.L; a=self._atan(5); b=self._atan(239)
        p=Interval(L.sub(L.mul(16,a.lo),L.mul(4,b.hi)),
                   L.sub(L.mul(16,a.hi),L.mul(4,b.lo)),self.bits)
        if not (3*self.S < p.lo <= p.hi < 4*self.S):
            raise CertificationError('pi enclosure guard failed')
        if p.hi-p.lo > 20*(self.terms+1):
            raise CertificationError('pi width budget failed')
        return p
    def sin_pi(self,p,q):
        """Enclose sin(pi*p/q); exact integer reduction handles singular roots."""
        integer(q,'argument denominator',1)
        if type(p) is not int: raise ValueError('argument numerator must be integer')
        L=self.L; S=self.S; n=self.terms
        L.event('sine_evaluation'); self.sine_calls+=1
        a=L.mod(p,L.mul(2,q)); sign=1
        if a>q: a=L.sub(L.mul(2,q),a); sign=-1
        if L.mul(2,a)>q: a=L.sub(q,a)
        if a==0:
            L.event('exact_zero_sine'); return Interval(0,0,self.bits)
        if L.mul(2,a)==q:
            L.event('exact_unit_sine'); return Interval(sign*S,sign*S,self.bits)
        alo=L.div(L.mul(self.pi.lo,a),q)
        ahi=L.ceildiv(L.mul(self.pi.hi,a),q)
        x=L.div(L.add(alo,ahi),2)
        radius=max(L.sub(x,alo),L.sub(ahi,x))
        if not 0<=x<=2*S: raise CertificationError('Taylor argument outside [0,2]')
        x2=L.mul(x,x); S2=L.mul(S,S)
        tlo=thi=x; slo=shi=x
        for k in range(1,n):
            den=L.mul(S2,L.mul(L.mul(2,k),L.add(L.mul(2,k),1)))
            tlo=L.div(L.mul(tlo,x2),den)
            thi=L.ceildiv(L.mul(thi,x2),den)
            if k%2: slo=L.sub(slo,thi); shi=L.sub(shi,tlo)
            else: slo=L.add(slo,tlo); shi=L.add(shi,thi)
            L.event('sine_taylor_term')
        # Degree 2n-1; the real sine remainder is <= 2^(2n+1)/(2n+1)!.
        factorial=1
        for k in range(2,L.add(L.mul(2,n),2)):
            factorial=L.mul(factorial,k); L.event('factorial_step')
        tail=L.ceildiv(L.shift(L.add(self.bits,L.add(L.mul(2,n),1))),factorial)
        if tail>1: raise CertificationError('predetermined Taylor tail budget failed')
        margin=L.add(radius,tail)
        out=Interval(L.sub(slo,margin),L.add(shi,margin),self.bits)
        if sign<0: out=Interval(L.sub(0,out.hi),L.sub(0,out.lo),self.bits)
        out=clipped(out,-S,S,L)
        if out.hi-out.lo>64*(n+1):
            raise CertificationError('predetermined sine width budget failed')
        return out


@dataclass(frozen=True)
class WindowSpec:
    M: int
    B: int
    r: int
    P: int
    beta: Fraction | None = None
    @property
    def origin(self):
        return 'reduced_component_fixture' if self.beta is None else 'ebeta_frontend_sparse_parameters'
    @property
    def m(self): return self.M.bit_length()-1
    @property
    def T(self): return self.M//self.B
    @property
    def ell(self): return 8*self.B
    @property
    def g(self): return self.T//4
    @property
    def H(self): return 3*self.T//4
    @property
    def W(self): return 2*self.r*(self.ell-1)+1
    def validate(self,ledger=None):
        """Validate and charge all supplied parameter encodings, including beta."""
        L=ledger if ledger is not None else Ledger()
        L.event('window_validation_call')
        for value in (self.M,self.B,self.r,self.P): L.parameter(value)
        if not power_two(self.M) or self.M<16: raise ValueError('M must be dyadic >=16')
        if not power_two(self.B) or self.B<4: raise ValueError('B must be dyadic >=4')
        integer(self.r,'r',1); integer(self.P,'P',8)
        m=L.sub(self.M.bit_length(),1)
        T=L.div(self.M,self.B)
        if L.mod(self.M,self.B) or T<4: raise ValueError('B must divide M and T>=4')
        ell=L.mul(8,self.B)
        W=L.add(L.mul(L.mul(2,self.r),L.sub(ell,1)),1)
        if W>=self.M: raise ValueError('compact support guard W<M failed')
        if self.beta is not None:
            n,d=validate_beta(self.beta,L)
            expected_B=L.shift(L.ceildiv(L.mul(L.add(d,L.mul(2,n)),m),L.mul(2,d)))
            k=L.shift(L.ceildiv(L.mul(L.mul(2,n),m),d))
            expected_r=L.add(L.mul(2,m),1)
            expected_P=L.add(L.mul(16,m),16)
            minimum_B=L.mul(4096,k)
            if (self.B!=expected_B or self.r!=expected_r or self.P!=expected_P
                    or self.B<minimum_B):
                raise ValueError('theorem provenance requires every accepted E(beta) sparse parameter and guard')
        return self


def validate_beta(beta,L):
    """Charge reading and validating both normalized Fraction integer fields."""
    L.event('beta_validation_call')
    if type(beta) is not Fraction:
        raise ValueError('beta must be an exact Fraction in (0,1/2)')
    n=L.parameter(beta.numerator);d=L.parameter(beta.denominator)
    if n<=0 or L.mul(2,n)>=d:
        raise ValueError('beta must be an exact Fraction in (0,1/2)')
    return n,d


def theorem_spec(m,beta,ledger=None):
    """E(beta) front-end sparse parameters, not the outer all-length dispatch.

    Outer guards (including beta*m>=2 and t<M) remain caller obligations.
    No dense fallback is implemented here. Revalidation is charged if repeated.
    """
    L=ledger if ledger is not None else Ledger()
    L.parameter(m);integer(m,'m',1)
    n,d=validate_beta(beta,L)
    M=L.shift(m)
    k=L.shift(L.ceildiv(L.mul(L.mul(2,n),m),d))
    B=L.shift(L.ceildiv(L.mul(L.add(d,L.mul(2,n)),m),L.mul(2,d)))
    spec=WindowSpec(M,B,L.add(L.mul(2,m),1),L.add(L.mul(16,m),16),beta)
    spec.validate(L)
    if B<L.mul(4096,k): raise ValueError('accepted sparse guard B>=4096k failed; dense path not implemented here')
    return spec


@dataclass(frozen=True)
class Tap:
    t: int
    numerator: int
    bits: int
    enclosure: Interval
    certified_error_grid_units: int  # units 2^-(bits+4), <=16 means <=rho


@dataclass
class PreparedWindow:
    spec: WindowSpec
    coefficients: Coefficients
    C: Interval
    taps: tuple
    ledger: dict
    budget: dict


def prepare_window(spec,ledger=None):
    """Prepare only a compact window. Does not read a source or recover frequencies."""
    L=ledger if ledger is not None else Ledger()
    spec.validate(L)
    M=spec.M; m=spec.m; r=spec.r; P=spec.P
    coef=exact_box_power(spec.ell,r,L)
    # epsilon = 2^-(P+4+3m), sine target <= epsilon/(128*r*M^3).
    j=L.add(L.add(P,11),L.add(L.mul(6,m),(r-1).bit_length()))
    K=L.add(j,L.add(L.mul(2,(j+1).bit_length()),16))
    N=L.add(K,8)
    if L.mul(64,L.add(N,1)) > L.shift(L.sub(K,j)):
        raise CertificationError('fixed guard-precision inequality failed')
    scalar=Scalar(K,L); S=scalar.S
    cbits=L.add(P,L.add(9,L.mul(4,m)))
    dbits=L.add(P,L.add(8,L.mul(3,m)))
    Cscale=L.shift(cbits); C_lo=C_hi=Cscale
    for a in range(1,spec.g+1):
        num=scalar.sin_pi(L.mul(spec.ell,a),M)
        if num.lo==num.hi==0:
            phi=Interval(0,0,K); L.event('exact_zero_phi')
        else:
            den0=scalar.sin_pi(a,M)
            den=Interval(L.mul(spec.ell,den0.lo),L.mul(spec.ell,den0.hi),K)
            ratio=clipped(quotient(num,den,L),-S,S,L)
            phi=clipped(even_power(ratio,L.mul(2,r),L),0,S,L)
        phi=quantize(phi,cbits,L)
        # width <= epsilon/(4M), i.e. <=8 units on this grid.
        if phi.hi-phi.lo>8: raise CertificationError('Phi scalar budget failed')
        C_lo=L.add(C_lo,L.mul(2,phi.lo)); C_hi=L.add(C_hi,L.mul(2,phi.hi))
        L.event('normalizer_positive_term')
    C=clipped(Interval(C_lo,C_hi,cbits),Cscale,L.mul(2*spec.g+1,Cscale),L)
    # C width <= epsilon (on this grid epsilon equals 32M units).
    if C.hi-C.lo>L.mul(32,M): raise CertificationError('C budget failed')
    Dscale=L.shift(dbits); nH=L.add(L.mul(2,spec.H),1)
    taps=[]; L.allocate(spec.W)
    for t in range(coef.radius+1):
        D=dirichlet(t,M,spec.H,scalar,dbits,L)
        # epsilon has 16 units on the Dirichlet output grid.
        if D.hi-D.lo>16: raise CertificationError('Dirichlet budget failed')
        a=coef.numerators[t+coef.radius]
        qbits=L.add(P,4); scale=L.shift(qbits)
        lows=[]; highs=[]; L.allocate(8)
        for d in (D.lo,D.hi):
            for c in (C.lo,C.hi):
                numerator=L.mul(L.mul(L.mul(L.mul(M,a),d),Cscale),scale)
                denominator=L.mul(L.mul(coef.denominator,Dscale),c)
                lows.append(L.div(numerator,denominator))
                highs.append(L.ceildiv(numerator,denominator))
        enclosure=Interval(min(lows),max(highs),qbits)
        # Round midpoint to P grid, signed nearest-even (denominator is 32).
        rounded=nearest_even(L.add(enclosure.lo,enclosure.hi),32,L)
        center=L.mul(rounded,16)
        err=max(abs(L.sub(center,enclosure.lo)),abs(L.sub(center,enclosure.hi)))
        if err>16: raise CertificationError('tap absolute rho certificate failed')
        taps.append(Tap(t,rounded,P,enclosure,err))
        L.event('nonnegative_tap')
    # Evenness is an exact construction invariant; no second trig evaluation.
    nonnegative=taps
    taps=tuple(Tap(-t.t,t.numerator,t.bits,t.enclosure,t.certified_error_grid_units)
               for t in reversed(nonnegative[1:]))+tuple(nonnegative)
    L.allocate(len(taps)); L.event('mirrored_tap',len(nonnegative)-1)
    delta_den=L.power(16,r)
    meets_theorem_delta=L.mul(nH,L.power(M,4))<=delta_den
    budget=dict(
        rho_exponent=P,epsilon_exponent=P+4+3*m,sine_target_exponent=j,
        working_grid_bits=K,scalar_terms=N,normalizer_grid_bits=cbits,
        dirichlet_grid_bits=dbits,tap_enclosure_grid_bits=P+4,
        max_tap_error_grid_units=max(t.certified_error_grid_units for t in taps),
        pass_stop_delta_numerator=nH,pass_stop_delta_denominator=delta_den,
        theorem_delta_M_minus_4=meets_theorem_delta)
    return PreparedWindow(spec,coef,C,taps,L.report(),budget)


def dirichlet(t,M,H,scalar,bits,ledger):
    """D_H(t). Exact limit at every t=0 mod M; no division at singular roots."""
    integer(M,'M',1); integer(H,'H')
    if type(t) is not int: raise ValueError('t must be integer')
    L=ledger; t=L.mod(t,M); n=L.add(L.mul(2,H),1)
    if t==0:
        value=L.mul(n,L.shift(bits)); L.event('exact_dirichlet_limit')
        return Interval(value,value,bits)
    if t>M//2: t=L.sub(M,t)
    num=scalar.sin_pi(L.mul(n,t),M)
    if num.lo==num.hi==0:
        L.event('exact_dirichlet_zero'); return Interval(0,0,bits)
    den=scalar.sin_pi(t,M)
    out=quotient(num,den,L)
    out=clipped(out,-L.mul(n,scalar.S),L.mul(n,scalar.S),L)
    return quantize(out,bits,L)


def nearest_even(n,d,L):
    integer(d,'rounding denominator',1)
    a=L.div(n,d); rem=L.sub(n,L.mul(a,d)); twice=L.mul(2,rem)
    L.event('nearest_even')
    return L.add(a,1) if twice>d or (twice==d and a%2) else a
