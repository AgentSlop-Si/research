"""Certified, bounded theorem-instance BUCKETS for the constant source 1/sqrt(M).

This is a new algebraic backend, NOT the rounded legacy tap/FFT implementation.
No arbitrary caller-supplied payload is authenticated by this numerical module.
The integration entrypoint independently executes the structured producer.
"""
from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec
import json
import sys

PIN = 'e29741e71c276c156d708f1d9dce6d60ff9d3d2c34a6045b03630c46506dac59'
BASE = Path(__file__).resolve().parent
source_bytes = (BASE / 'vendor' / 'compact_window.py').read_bytes()
if sha256(source_bytes).hexdigest() != PIN:
    raise ValueError('DEPENDENCY_PIN: compact_window')
_name = 'alg034_scale_pinned_compact_window'
if _name in sys.modules:
    _window = sys.modules[_name]
    if getattr(_window, '_verified_source_pin', None) != PIN:
        raise ValueError('DEPENDENCY_IDENTITY: compact_window')
else:
    _spec = spec_from_file_location(_name, BASE/'vendor'/'compact_window.py')
    _window = module_from_spec(_spec)
    sys.modules[_name] = _window
    _spec.loader.exec_module(_window)
    _window._verified_source_pin = PIN
Interval = _window.Interval

M_FIXED = 1 << 28
B_FIXED = 1 << 17
BETA_FIXED = Fraction(5, 56)
K_FIXED = 560
TAYLOR_TERMS = 128
MAX_NUMERIC_OPERATIONS = 30_000_000
MAX_WORKING_INTEGER_BITS = 70_000
MAX_ALLOCATED_SLOTS = 4_000_000

class Failure(ValueError):
    pass

class Meter(_window.Ledger):
    def __init__(self):
        super().__init__()
        self.numeric_operations = 0
        self.bytes_processed = 0
    def record(self, kind, inputs, output):
        self.numeric_operations += 1
        if self.numeric_operations > MAX_NUMERIC_OPERATIONS:
            raise Failure('RESOURCE_LIMIT: numerical operations')
        if max(max(1, abs(x).bit_length()) for x in (*inputs, output)) > MAX_WORKING_INTEGER_BITS:
            raise Failure('RESOURCE_LIMIT: working integer bits')
        return super().record(kind, inputs, output)
    def shift(self, n):
        if type(n) is not int or not 0 <= n < MAX_WORKING_INTEGER_BITS:
            raise Failure('RESOURCE_LIMIT: shift')
        return super().shift(n)
    def allocate(self, n):
        if type(n) is not int or n < 0 or self.allocated_slots + n > MAX_ALLOCATED_SLOTS:
            raise Failure('RESOURCE_LIMIT: allocated logical slots')
        super().allocate(n)
    def bytework(self, n):
        if type(n) is not int or n < 0:
            raise Failure('INTERNAL: byte count')
        self.bytes_processed += n
        self.event('byte_processing', n)
    def report(self):
        out = super().report()
        # Reading, hashing, parsing/compiling bounded trusted dependency source
        # and exporting JSON are charged rather than silently treated as setup.
        byte_work = (1 << 20) * (self.bytes_processed + 1) ** 2
        out['numeric_operations'] = self.numeric_operations
        out['bytes_processed'] = self.bytes_processed
        out['source_and_serialization_bit_work_upper'] = byte_work
        out['total_bit_work_upper'] += byte_work
        out['cumulative_storage_upper_bits'] += 1024*(self.bytes_processed+1)**2
        out['model'] = 'schoolbook bit work; cumulative logical storage; not host CPU/RSS'
        return out

class ShortTaylor:
    """Pinned Machin pi, fresh finite outward sine, one paid shared tail.

    128 terms suffice because the exact factorial-tail inequality is checked.
    Every sine endpoint operation is outward rounded, including the angle radius.
    There is no floating arithmetic or tolerance/retry loop.
    """
    def __init__(self, K, L):
        self.K, self.L = K, L
        original = _window.Scalar(K, L)
        self.S, self.pi = original.S, original.pi
        self.terms = TAYLOR_TERMS
        factorial = 1
        for k in range(2, 2*self.terms+2):
            factorial = L.mul(factorial, k)
            L.event('shared_factorial_step')
        self.tail = L.ceildiv(L.shift(K+2*self.terms+1), factorial)
        if self.tail > 1:
            raise Failure('CERTIFICATE: shared Taylor remainder')
    def sin_pi(self, p, q):
        L, S, n = self.L, self.S, self.terms
        if type(p) is not int or type(q) is not int or q <= 0:
            raise Failure('DOMAIN: sine rational argument')
        L.event('sine_evaluation')
        a=L.mod(p,L.mul(2,q)); sign=1
        if a>q: a=L.sub(L.mul(2,q),a); sign=-1
        if L.mul(2,a)>q: a=L.sub(q,a)
        if a==0:
            L.event('exact_zero_sine'); return Interval(0,0,self.K)
        if L.mul(2,a)==q:
            L.event('exact_unit_sine'); return Interval(sign*S,sign*S,self.K)
        alo=L.div(L.mul(self.pi.lo,a),q)
        ahi=L.ceildiv(L.mul(self.pi.hi,a),q)
        x=L.div(L.add(alo,ahi),2)
        radius=max(L.sub(x,alo),L.sub(ahi,x))
        if not 0 <= x <= 2*S:
            raise Failure('CERTIFICATE: Taylor angle domain')
        x2=L.mul(x,x); S2=L.mul(S,S)
        tlo=thi=x; slo=shi=x
        for k in range(1,n):
            den=L.mul(S2,L.mul(L.mul(2,k),L.add(L.mul(2,k),1)))
            tlo=L.div(L.mul(tlo,x2),den)
            thi=L.ceildiv(L.mul(thi,x2),den)
            if k%2: slo=L.sub(slo,thi); shi=L.sub(shi,tlo)
            else: slo=L.add(slo,tlo); shi=L.add(shi,thi)
            L.event('sine_taylor_term')
        margin=L.add(radius,self.tail)
        out=Interval(L.sub(slo,margin),L.add(shi,margin),self.K)
        if sign<0: out=Interval(L.sub(0,out.hi),L.sub(0,out.lo),self.K)
        return _window.clipped(out,-S,S,L)

@dataclass(frozen=True)
class BucketResult:
    numerators: tuple
    bits: int

@dataclass(frozen=True)
class ScalarCertificate:
    bin_index: int
    numerator: int
    enclosure_low: int
    enclosure_high: int
    enclosure_bits: int
    radius_grid_units: int

class ConstantBucketEngine:
    """Only M=2^28,beta=5/56 and exact positive constant source 2^-14.

    Preparation directly evaluates the same ideal BUCKETS operator in frequency
    space. The run method supports every accepted sigma,tau because the checked
    source is constant. It returns a fully materialized B-entry immutable vector.
    """
    def __init__(self):
        L = self.ledger = Meter()
        L.bytework(len(source_bytes))
        L.bytework(len(Path(__file__).read_bytes()))
        self.spec = _window.theorem_spec(28, BETA_FIXED, L)
        s=self.spec
        if (s.M,s.B,s.T,s.g,s.H,s.r,s.P) != (M_FIXED,B_FIXED,2048,512,1536,57,464):
            raise Failure('INTERNAL: exact theorem fixture')
        if BETA_FIXED*28 < 2:
            raise Failure('DOMAIN: outer beta*m')
        # The actual compact window delta, independent of numerical rho.
        nH=L.add(L.mul(2,s.H),1)
        delta_den=L.power(16,s.r)
        if L.mul(nH,L.power(s.M,4)) > delta_den:
            raise Failure('CERTIFICATE: theorem window delta')
        tail_den=L.power(20,L.mul(2,s.r))
        if L.mul(nH,L.shift(s.P)) > tail_den:
            raise Failure('CERTIFICATE: far-bin zero approximation')
        self.delta=(nH,delta_den)
        self.far_bin_bound=(nH,tail_den)
        scalar=ShortTaylor(K_FIXED,L)
        S=scalar.S
        # |sin(pi*ell*a/M)| repeats, up to sign, with period M/ell=256.
        period=L.div(s.M,s.ell)
        if period!=256: raise Failure('INTERNAL: numerator period')
        sine=[]; L.allocate(period//2+1)
        for a in range(period//2+1):
            sine.append(scalar.sin_pi(a,period))
            L.event('numerator_root_preparation')
        # Retain only three positive-interval sums; no time-window, N-vector,
        # FFT-root table, or full Phi vector is constructed.
        clo=chi=S
        center_lo=center_hi=S
        side_lo=side_hi=0
        stop=L.add(s.T,s.H)
        for a in range(1,stop+1):
            residue=L.mod(a,period)
            if residue>period//2: residue=L.sub(period,residue)
            num=sine[residue]
            if num.lo==num.hi==0:
                phi=Interval(0,0,K_FIXED); L.event('exact_zero_phi')
            else:
                den0=scalar.sin_pi(a,s.M)
                den=Interval(L.mul(s.ell,den0.lo),L.mul(s.ell,den0.hi),K_FIXED)
                if den.lo <= 0: raise Failure('CERTIFICATE: positive denominator')
                ratio=_window.clipped(_window.quotient(num,den,L),-S,S,L)
                phi=_window.clipped(_window.even_power(ratio,2*s.r,L),0,S,L)
            if a<=s.g:
                clo=L.add(clo,L.mul(2,phi.lo)); chi=L.add(chi,L.mul(2,phi.hi))
            if a<=s.H:
                center_lo=L.add(center_lo,L.mul(2,phi.lo))
                center_hi=L.add(center_hi,L.mul(2,phi.hi))
            if a>=s.T-s.H:
                side_lo=L.add(side_lo,phi.lo); side_hi=L.add(side_hi,phi.hi)
            L.event('phi_evaluation')
        C=Interval(clo,chi,K_FIXED)
        if C.lo<S: raise Failure('CERTIFICATE: C>=1')
        self.normalizer=C
        q0=_window.quotient(Interval(center_lo,center_hi,K_FIXED),C,L)
        q1=_window.quotient(Interval(side_lo,side_hi,K_FIXED),C,L)
        certificates=[]
        def certify(index,enclosure):
            u=L.shift(K_FIXED-s.P)
            q=_window.nearest_even(L.add(enclosure.lo,enclosure.hi),L.mul(2,u),L)
            center=L.mul(q,u)
            err=max(abs(L.sub(center,enclosure.lo)),abs(L.sub(center,enclosure.hi)))
            if L.mul(err,err)>L.mul(u,u):
                raise Failure('CERTIFICATE: bucket squared radius')
            cert=ScalarCertificate(index,q,enclosure.lo,enclosure.hi,K_FIXED,err)
            certificates.append(cert); L.allocate(7)
            return q
        main=certify(0,q0)
        side=certify(1,q1)
        certify(s.B-1,q1)
        values=[]; L.allocate(s.B)
        for j in range(s.B):
            value=main if j==0 else side if j in (1,s.B-1) else 0
            values.append((value,0)); L.allocate(3)
            L.event('bucket_output')
        self.result=BucketResult(tuple(values),s.P); L.allocate(s.B+2)
        self.certificates=tuple(certificates); L.allocate(len(certificates)+1)
        self.scalar_terms=TAYLOR_TERMS
        self.max_phi_index=stop
        L.event('constant_engine_preparation')
    def run(self, source_period, source_exponent, sigma, tau):
        L=self.ledger
        self.spec.validate(L)
        if type(source_period) is not tuple or len(source_period)!=4:
            raise Failure('GRAMMAR: constant source period')
        # Type/shape checks precede equality, so unknown __eq__ hooks cannot run.
        for row in source_period:
            if type(row) is not tuple or len(row)!=2 or any(type(x) is not int for x in row):
                raise Failure('GRAMMAR: constant source')
            L.allocate(3)
            for x in row: L.parameter(x)
        if source_period != ((1,0),)*4:
            raise Failure('DOMAIN: constant unit source period')
        if type(source_exponent) is not int or source_exponent != -14:
            raise Failure('DOMAIN: exact normalized constant exponent')
        for x in (source_exponent,sigma,tau): L.parameter(x)
        if not 0<sigma<self.spec.M or sigma%2!=1 or not 0<=tau<self.spec.M:
            raise Failure('DOMAIN: sigma/tau')
        L.event('constant_buckets_call')
        L.allocate(2)
        return self.result
    def evidence(self):
        out={
            'backend':'ALG034_Q16_CONSTANT_FREQUENCY_BACKEND_V1',
            'theorem_parameters':{'m':28,'M':self.spec.M,'beta':[5,56],
                'k':32,'B':self.spec.B,'T':self.spec.T,'g':self.spec.g,'H':self.spec.H,
                'r':self.spec.r,'P':self.spec.P,'W':self.spec.W},
            'window_delta':{'numerator':self.delta[0],'denominator':self.delta[1]},
            'far_bin_error':{'numerator':self.far_bin_bound[0],'denominator':self.far_bin_bound[1]},
            'error_radius':{'coefficient':1,'scale':-self.spec.P},
            'certificates':[c.__dict__ for c in self.certificates],
            'normalizer':self.normalizer.__dict__,
            'max_phi_index':self.max_phi_index,'scalar_grid_bits':K_FIXED,
            'taylor_terms':self.scalar_terms,
            'output_length':len(self.result.numerators),
            'not_legacy_rounded_execution':True,
            'full_recovery_executed':False,
        }
        # Fixed-size evidence only. Export itself is paid, including doubled
        # encoding buffer and a conservative tree/control budget.
        encoded=json.dumps(out,sort_keys=True,separators=(',',':')).encode('ascii')
        self.ledger.bytework(2*len(encoded))
        self.ledger.allocate(4*len(encoded))
        out['resource_receipt']=self.ledger.report()
        return out
