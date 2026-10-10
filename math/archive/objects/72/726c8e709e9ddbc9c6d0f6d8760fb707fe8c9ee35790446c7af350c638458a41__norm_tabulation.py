"""Norm-certified tabulated Fourier research implementation.

Two modes are deliberately distinct:
* Small EagerBlockTable objects really enumerate EVERY padded input key.
* High-accuracy ReferenceFFT evaluates only requested table entries. It tests
  the exact dyadic circuit/error bounds; its observed runtime is NOT the
  all-tables-built word-RAM asymptotic algorithm.

All simulated arithmetic, including rounded complex products, is exact
integer/dyadic arithmetic. Only comparison with an independent DFT converts
outputs to high-precision real/complex numbers. No numerical FFT is used here.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from math import isqrt
from typing import Sequence


def pow2(k: int) -> Fraction:
    return Fraction(1 << k, 1) if k >= 0 else Fraction(1, 1 << (-k))


def floor_log2_fraction(x: Fraction) -> int:
    if x <= 0:
        raise ValueError('Positive argument required.')
    k = x.numerator.bit_length() - x.denominator.bit_length()
    return k if x >= pow2(k) else k - 1


def ceil_log2_fraction(x: Fraction) -> int:
    k = floor_log2_fraction(x)
    return k if x == pow2(k) else k + 1


def trunc_fraction(x: Fraction) -> int:
    return x.numerator // x.denominator if x >= 0 else -((-x.numerator) // x.denominator)


@lru_cache(maxsize=None)
def pi_interval(bits: int) -> tuple[Fraction, Fraction]:
    """Rigorous rational interval using Machin and alternating atan series."""
    target = pow2(-bits-8)
    def atan_interval(q: int) -> tuple[Fraction, Fraction]:
        z = Fraction(1, q)
        power = z
        total = Fraction(0)
        j = 0
        while True:
            total += (-1 if j & 1 else 1) * power / (2*j+1)
            j += 1
            power *= z*z
            nxt = (-1 if j & 1 else 1) * power / (2*j+1)
            if abs(nxt) <= target:
                return min(total, total+nxt), max(total, total+nxt)
    a,b = atan_interval(5)
    c,d = atan_interval(239)
    return 16*a-4*d, 16*b-4*c


@lru_cache(maxsize=None)
def phase_rational(index: int, order: int, bits: int) -> tuple[Fraction, Fraction, Fraction]:
    """Approximate exp(-2*pi*i*index/order), with rigorous norm error bound."""
    if order < 1:
        raise ValueError('Root order must be positive.')
    j = index % order
    if 2*j > order:
        j -= order
    lo,hi = pi_interval(bits+12)
    theta = -Fraction(2*j, order) * ((lo+hi)/2)
    theta_error = abs(Fraction(2*j,order)) * (hi-lo)/2
    # Integral Taylor remainder for exp(i*theta): <= |theta|^(L+1)/(L+1)!.
    real = Fraction(1)
    imag = Fraction(0)
    term = Fraction(1)
    degree = 0
    target = pow2(-bits-12)
    while True:
        degree += 1
        term *= theta / degree
        residue = degree % 4
        if residue == 0:
            real += term
        elif residue == 1:
            imag += term
        elif residue == 2:
            real -= term
        else:
            imag -= term
        remainder = abs(term*theta/(degree+1))
        if degree >= 4 and remainder <= target:
            return real, imag, theta_error+remainder


@lru_cache(maxsize=None)
def dyadic_coefficient(index: int, order: int, scale_length: int, bits: int) -> tuple[int,int,int,Fraction]:
    """Dyadic approximation to exp(-2*pi*i*j/order)/sqrt(scale_length).

    Return real numerator, imaginary numerator, denominator exponent, and a
    rigorous upper bound on the complex absolute coefficient error.
    """
    if scale_length < 1:
        raise ValueError('scale_length must be positive')
    a,b,phase_error = phase_rational(index,order,bits)
    guard = bits+12
    root_num = isqrt((1 << (2*guard)) // scale_length)
    root_approx = Fraction(root_num,1 << guard)
    root_error = pow2(-guard)
    nr = trunc_fraction(a*root_approx*(1 << bits))
    ni = trunc_fraction(b*root_approx*(1 << bits))
    # sqrt(2)*roundoff bounded by 2*roundoff; |phase exact| = 1.
    bound = root_approx*phase_error + root_error + 2*pow2(-bits)
    return nr,ni,bits,bound


@dataclass(frozen=True)
class FloatAlphabet:
    """Explicit finite floating alphabet. p is FRACTION bits, not total bits."""
    p: int
    emin: int
    emax: int

    def __post_init__(self):
        if self.p < 0 or self.emax < self.emin:
            raise ValueError('Invalid alphabet.')

    @property
    def exponent_count(self): return self.emax-self.emin+1
    @property
    def exponent_bits(self): return self.exponent_count.bit_length()
    @property
    def real_bits(self): return self.p+self.exponent_bits+1
    @property
    def complex_bits(self): return 2*self.real_bits
    @property
    def lattice_exp(self): return self.emin-self.p
    @property
    def u(self): return pow2(-self.p)
    @property
    def tau(self): return pow2(self.emin)

    def quantize(self, numerator: int, exponent: int = 0) -> tuple[int,bool]:
        """Truncate numerator*2^exponent; overflow saturates and is flagged."""
        if numerator == 0:
            return 0,False
        negative = numerator < 0
        a = abs(numerator)
        e = a.bit_length()-1+exponent
        if e < self.emin:
            return 0,False
        overflow = e > self.emax
        if overflow:
            e = self.emax
            m = (1 << (self.p+1))-1
        else:
            shift = a.bit_length()-1-self.p
            m = (a >> shift) if shift >= 0 else (a << (-shift))
        fraction = m-(1 << self.p)
        exponent_code = e-self.emin+1
        sign_code = int(negative) << (self.p+self.exponent_bits)
        return sign_code | (exponent_code << self.p) | fraction, overflow

    def decode(self, code: int) -> int:
        """Return lattice integer; padding/invalid codes are mapped to zero."""
        if code < 0 or code >= (1 << self.real_bits):
            raise ValueError('Code does not fit real alphabet word.')
        ec = (code >> self.p) & ((1 << self.exponent_bits)-1)
        if ec == 0 or ec > self.exponent_count:
            return 0
        mantissa = (1 << self.p)+(code & ((1 << self.p)-1))
        value = mantissa << (ec-1)
        return -value if (code >> (self.p+self.exponent_bits)) & 1 else value

    def combine(self, real_code: int, imag_code: int) -> int:
        return real_code | (imag_code << self.real_bits)

    def split(self, code: int) -> tuple[int,int]:
        mask=(1 << self.real_bits)-1
        return code & mask, (code >> self.real_bits) & mask

    def complex_integer(self, code: int) -> tuple[int,int]:
        a,b=self.split(code)
        return self.decode(a),self.decode(b)

    def quantize_complex(self, real: int, imag: int, exponent: int=0) -> tuple[int,bool]:
        a,oa=self.quantize(real,exponent)
        b,ob=self.quantize(imag,exponent)
        return self.combine(a,b),oa or ob

    def complex_fraction(self, code: int) -> tuple[Fraction,Fraction]:
        a,b=self.complex_integer(code)
        return a*pow2(self.lattice_exp),b*pow2(self.lattice_exp)


def pack(codes: Sequence[int], width: int) -> int:
    key=0
    mask=(1 << width)-1
    for j,v in enumerate(codes):
        if v < 0 or v > mask:
            raise ValueError('Value exceeds packed field width.')
        key |= v << (j*width)
    return key


def unpack(key: int, count: int, width: int) -> list[int]:
    mask=(1 << width)-1
    return [(key >> (j*width)) & mask for j in range(count)]


class BlockKernel:
    def __init__(self, alphabet: FloatAlphabet, length: int):
        if length < 1 or length & (length-1):
            raise ValueError('Block length must be a power of two.')
        self.alphabet=alphabet
        self.length=length
        self.bits=alphabet.p+(length.bit_length()-1)+10
        self.coef=[dyadic_coefficient(j,length,length,self.bits) for j in range(length)]
        self.max_coefficient_error=max(c[3] for c in self.coef)
        assert self.max_coefficient_error*length <= alphabet.u/8

    def evaluate(self, codes: Sequence[int]) -> tuple[list[int],int]:
        if len(codes) != self.length:
            raise ValueError('Wrong block length.')
        values=[self.alphabet.complex_integer(c) for c in codes]
        out=[]
        overflows=0
        for k in range(self.length):
            rr=ii=0
            for j,(ar,ai) in enumerate(values):
                cr,ci,_,_=self.coef[(j*k)%self.length]
                rr += ar*cr-ai*ci
                ii += ar*ci+ai*cr
            value,overflow=self.alphabet.quantize_complex(rr,ii,self.alphabet.lattice_exp-self.bits)
            out.append(value)
            overflows += int(overflow)
        return out,overflows


class EagerBlockTable:
    """Complete, not lazy: all 2^(complex_bits*length) padded keys enumerated."""
    def __init__(self, kernel: BlockKernel, max_entries: int=1 << 18):
        self.kernel=kernel
        self.width=kernel.alphabet.complex_bits
        size=1 << (self.width*kernel.length)
        if size > max_entries:
            raise ValueError(f'Eager table has {size} entries, over explicit budget {max_entries}.')
        self.outputs=[]
        for key in range(size):
            values=unpack(key,kernel.length,self.width)
            result,_=kernel.evaluate(values)
            self.outputs.append(pack(result,self.width))

    def apply(self,codes:Sequence[int]) -> list[int]:
        if len(codes) != self.kernel.length:
            raise ValueError('Wrong block length.')
        return unpack(self.outputs[pack(codes,self.width)],len(codes),self.width)


def parameters(log2_length:int, epsilon:Fraction, gamma:Fraction=Fraction(1,4)) -> dict:
    if log2_length < 1 or not (0 < epsilon <= Fraction(1,4)):
        raise ValueError('Need log2_length>=1 and 0<epsilon<=1/4.')
    n=log2_length
    p=ceil_log2_fraction(Fraction(1024*(n+1),1)/epsilon)
    # tau <= eps/[1024*N*(n+1)] without constructing an enormous N integer.
    emin=floor_log2_fraction(epsilon/Fraction(1024*(n+1),1))-n
    alphabet=FloatAlphabet(p,emin,n+4)
    limit=(gamma*n)//alphabet.complex_bits
    radix=1 if limit < 2 else 1 << (int(limit).bit_length()-1)
    macro_bits=0 if radix==1 else radix.bit_length()-1
    levels=n if radix==1 else (n+macro_bits-1)//macro_bits
    return dict(log2_N=n,epsilon=str(epsilon),p=p,emin=emin,emax=n+4,
                complex_bits=alphabet.complex_bits,radix=radix,
                macro_bits=macro_bits,macro_levels=levels,
                padded_table_key_bits=radix*alphabet.complex_bits,
                table_budget_bits=int(gamma*n),
                phase_grid_bits=p+8,ordinary_fallback=(radix==1))


class ReferenceFFT:
    """Exact-dyadic accuracy simulator using LAZY block entries, not a speed demo."""
    def __init__(self,length:int,epsilon:Fraction,radix:int=4):
        if length < 2 or length & (length-1):
            raise ValueError('Length must be a power of two >=2.')
        if radix < 2 or radix & (radix-1):
            raise ValueError('Radix must be a power of two >=2.')
        self.N=length
        self.n=length.bit_length()-1
        self.epsilon=epsilon
        self.spec=parameters(self.n,epsilon)
        self.alphabet=FloatAlphabet(self.spec['p'],self.spec['emin'],self.spec['emax'])
        self.radix=radix
        self.phase_bits=self.alphabet.p+8
        self.phase_order=1 << self.phase_bits
        self.twiddle_bits=self.alphabet.p+10
        self.kernels={}
        self.twiddles={}
        self.entries={}
        self.stats={}

    def _twiddle(self,code:int,index:int,order:int) -> int:
        idx=((2*(index%order)*self.phase_order+order)//(2*order))%self.phase_order
        if idx not in self.twiddles:
            self.twiddles[idx]=dyadic_coefficient(idx,self.phase_order,1,self.twiddle_bits)
        cr,ci,_,bound=self.twiddles[idx]
        # Grid-angle discrepancy <= pi/phase_order, with pi<4.
        assert bound+Fraction(4,self.phase_order) <= self.alphabet.u/8
        ar,ai=self.alphabet.complex_integer(code)
        result,ov=self.alphabet.quantize_complex(ar*cr-ai*ci,ar*ci+ai*cr,
                                               self.alphabet.lattice_exp-self.twiddle_bits)
        self.stats['twiddle_applications'] += 1
        self.stats['overflows'] += int(ov)
        return result

    def _block(self,codes:list[int]) -> list[int]:
        m=len(codes)
        if m not in self.kernels:
            self.kernels[m]=BlockKernel(self.alphabet,m)
        key=(m,pack(codes,self.alphabet.complex_bits))
        if key not in self.entries:
            ans,ov=self.kernels[m].evaluate(codes)
            self.entries[key]=(ans,ov)
            self.stats['slow_entry_constructions'] += 1
        ans,ov=self.entries[key]
        self.stats['block_applications'] += 1
        self.stats['overflows'] += ov
        return list(ans)

    def _run(self,codes:list[int]) -> list[int]:
        L=len(codes)
        if L==1:
            return codes
        if L <= self.radix:
            return self._block(codes)
        r=self.radix
        s=L//r
        children=[self._run(codes[a::r]) for a in range(r)]
        out=[0]*L
        for k in range(s):
            v=[self._twiddle(children[a][k],a*k,L) for a in range(r)]
            z=self._block(v)
            for t in range(r):
                out[k+s*t]=z[t]
        return out

    def run_integer(self,x:Sequence[tuple[int,int]]) -> tuple[list[tuple[Fraction,Fraction]],dict]:
        if len(x) != self.N:
            raise ValueError('Wrong input length.')
        self.stats=dict(twiddle_applications=0,block_applications=0,
                        slow_entry_constructions=0,overflows=0)
        maximum=max(max(abs(a),abs(b)) for a,b in x)
        if maximum==0:
            return [(Fraction(0),Fraction(0))]*self.N,dict(self.stats)
        scale=maximum.bit_length()  # max normalized component in [1/2,1).
        initial=[]
        for a,b in x:
            v,ov=self.alphabet.quantize_complex(a,b,-scale)
            initial.append(v)
            self.stats['overflows'] += int(ov)
        codes=self._run(initial)
        ans=[]
        for code in codes:
            a,b=self.alphabet.complex_fraction(code)
            ans.append((a*(1<<scale),b*(1<<scale)))
        return ans,dict(self.stats)
