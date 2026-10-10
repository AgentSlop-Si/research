"""Research prototype: two real FFTs per complex FFT, packed convolution, and cross-input DAG sharing.

Uses numpy for accuracy / benchmark reference and optional optimized FFTs.
The DAG portion counts radix-2 complex butterflies, not total time, and uses
hash-consing of exact recursive subproblems. This does NOT beat n log n for
arbitrary complex/real Fourier transforms.

Run: python fft_packed_dag_research.py
"""
from __future__ import annotations

import cmath
import math
import random
import statistics
import time
from collections import Counter

import numpy as np


def two_real_ffts_one_complex(a, b):
    """Recover the separate length-N complex FFTs of two real-valued length-N arrays."""
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    if a.shape != b.shape or a.ndim != 1:
        raise ValueError('a and b must be real one-dimensional arrays of equal length')
    n = len(a)
    if not n:
        raise ValueError('n must be positive')
    z = np.fft.fft(a + 1j * b)
    partner = np.conj(z[(-np.arange(n)) % n])
    fa = (z + partner) / 2
    fb = (z - partner) / (2j)
    return fa, fb


def packed_convolution(a, b):
    """Real linear convolution from one forward complex FFT and one inverse FFT.

    Zero-pad so circular convolution agrees with linear convolution.
    Imag(ifft(fft(a + 1j*b)**2))/2 = convolution(a,b).
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    if a.ndim != 1 or b.ndim != 1 or not len(a) or not len(b):
        raise ValueError('nonempty one-dimensional real arrays required')
    target = len(a) + len(b) - 1
    n = 1 << (target - 1).bit_length()
    a_padded = np.pad(a, (0, n - len(a)))
    b_padded = np.pad(b, (0, n - len(b)))
    z = np.fft.fft(a_padded + 1j * b_padded)
    return (np.fft.ifft(z * z).imag[:target]) / 2


class JointFFTGraph:
    """Hash-conses identical FFT subproblems ACROSS arbitrary input arrays.

    Canonical keys are exact, not tolerant approximations. Two separate real
    FFTs can share subgraphs (and results) without packing into one complex
    array. For all-real inputs the same complex radix-2 butterfly code is used.
    """
    def __init__(self):
        self.intern = {}
        self.nodes = []
        self.values = {}
        self.twiddles = {}
        self.butterflies = 0
        self.build_visits = 0

    def build(self, a, off=0, stride=1, n=None):
        if n is None:
            n = len(a)
            if not n or n & (n - 1):
                raise ValueError('length must be a positive power of two')
        self.build_visits += 1
        if n == 1:
            v = complex(a[off])
            key = ('leaf', v)
            node = (1, -1, -1, v)
        else:
            left = self.build(a, off, stride * 2, n // 2)
            right = self.build(a, off + stride, stride * 2, n // 2)
            key = ('internal', n, left, right)
            node = (n, left, right, None)
        ident = self.intern.get(key)
        if ident is None:
            ident = len(self.nodes)
            self.intern[key] = ident
            self.nodes.append(node)
        return ident

    def eval(self, ident):
        if ident in self.values:
            return self.values[ident]
        n, lid, rid, v = self.nodes[ident]
        if n == 1:
            out = (v,)
        else:
            ev = self.eval(lid)
            od = self.eval(rid)
            if n not in self.twiddles:
                self.twiddles[n] = [cmath.exp(-2j * math.pi * k / n) for k in range(n//2)]
            out = [0j] * n
            for k in range(n // 2):
                t = self.twiddles[n][k] * od[k]
                out[k] = ev[k] + t
                out[k+n//2] = ev[k] - t
                self.butterflies += 1
            out = tuple(out)
        self.values[ident] = out
        return out

    def eval_inputs(self, a, b):
        ra = self.build(a)
        rb = self.build(b)
        return self.eval(ra), self.eval(rb)

    def summary(self):
        return {
            'butterflies': self.butterflies,
            'unique_nodes': len(self.nodes),
            'unique_by_size': dict(sorted(Counter(x[0] for x in self.nodes).items())),
            'cached_values': sum(len(x) for x in self.values.values()),
            'build_visits': self.build_visits,
        }


def packed_dag(a, b):
    """One hash-consed complex FFT; split two real spectra in O(N)."""
    if len(a) != len(b):
        raise ValueError('same input lengths required')
    z_input = [complex(x, y) for x, y in zip(a, b)]
    graph = JointFFTGraph()
    root = graph.build(z_input)
    z = graph.eval(root)
    n = len(a)
    out_a, out_b = [], []
    for k in range(n):
        mate = z[(-k) % n].conjugate()
        out_a.append((z[k] + mate) / 2)
        out_b.append((z[k] - mate) / (2j))
    return tuple(out_a), tuple(out_b), graph.summary()


def find_cyclic_shift(a, b):
    """Return right-shift s such that b[j] == a[(j-s)%n], or None.

    KMP search, O(n) comparisons and O(n) extra memory. Exact equality.
    """
    if len(a) != len(b) or not a:
        return None
    n = len(a)
    pi = [0] * n
    j = 0
    for i in range(1, n):
        while j and b[i] != b[j]:
            j = pi[j-1]
        if b[i] == b[j]:
            j += 1
        pi[i] = j
    j = 0
    for i in range(2*n-1):
        value = a[i % n]
        while j and value != b[j]:
            j = pi[j-1]
        if value == b[j]:
            j += 1
        if j == n:
            start = i-n+1
            return (-start) % n
    return None


def shifted_fft_from_reference(fa, shift):
    """FFT(np.roll(a, shift)) from FFT(a), with O(n) arithmetic."""
    n = len(fa)
    phase_step = cmath.exp(-2j * math.pi * shift / n)
    phase = 1+0j
    result = []
    for val in fa:
        result.append(val * phase)
        phase *= phase_step
    return tuple(result)


def tests():
    rng = np.random.default_rng(20261008)
    comparisons = 0
    for n in (1, 2, 3, 4, 8, 16, 32, 64, 256):
        for _ in range(7):
            a = rng.integers(-9, 10, n, dtype=np.int64)
            b = rng.integers(-9, 10, n, dtype=np.int64)
            fa, fb = two_real_ffts_one_complex(a, b)
            assert np.allclose(fa, np.fft.fft(a), rtol=1e-12, atol=1e-10)
            assert np.allclose(fb, np.fft.fft(b), rtol=1e-12, atol=1e-10)
            comparisons += 1
    convchecks = 0
    for la, lb in [(1,1),(1,7),(2,3),(4,4),(7,9),(16,16),(31,5),(39,63)]:
        for _ in range(4):
            a = rng.integers(-9, 10, la)
            b = rng.integers(-9, 10, lb)
            actual = packed_convolution(a,b)
            expected = np.convolve(a, b)
            assert np.allclose(actual, expected, atol=1e-8), (a,b,actual,expected)
            convchecks += 1
    assert np.rint(packed_convolution([4,3,2,1], [8,7,6,5])).astype(int).tolist() == [32,52,61,60,34,16,5]
    assert sum(j*10**i for i,j in enumerate(np.rint(packed_convolution([4,3,2,1],[8,7,6,5])).astype(int))) == 7006652
    graphchecks = 0
    for n in (2, 4, 8, 16, 32, 64, 128):
        for _ in range(5):
            a = rng.integers(0,2,n).tolist()
            b = rng.integers(0,2,n).tolist()
            joint = JointFFTGraph()
            fa, fb = joint.eval_inputs(a,b)
            fpa, fpb, _ = packed_dag(a,b)
            for actual in (fa, fpa):
                assert np.allclose(actual,np.fft.fft(a),atol=1e-8)
            for actual in (fb, fpb):
                assert np.allclose(actual,np.fft.fft(b),atol=1e-8)
            graphchecks += 1
    # Verify autodetected low-rank basis and rank>2 rejection.
    b0=rng.integers(-4,5,67).astype(float)
    b1=rng.integers(-4,5,67).astype(float)
    co=rng.integers(-5,6,(11,2)).astype(float)
    family=co[:,0,None]*b0+co[:,1,None]*b1
    spectra,mode=adaptive_rank_two_fft(family)
    assert mode=='rank2' and np.allclose(spectra, np.fft.fft(family,axis=1),atol=1e-8)
    assert detect_rank_two_real_family(np.stack([rng.standard_normal(67) for _ in range(3)])) is None
    shifts = 0
    for n in (1, 2, 4, 8, 16, 32, 127, 128):
        for _ in range(12):
            a=rng.integers(-50,51,n).tolist()
            s=int(rng.integers(0,n))
            b=np.roll(a,s).tolist()
            recovered=find_cyclic_shift(a,b)
            assert recovered is not None and np.array_equal(np.roll(a,recovered), b), (n,s,recovered)
            assert np.allclose(shifted_fft_from_reference(np.fft.fft(a), recovered),np.fft.fft(b),atol=1e-8)
            shifts+=1
    print(f'TESTS PASSED: packed spectra={comparisons}, packed convolutions={convchecks}, graph FFT pairs={graphchecks}, KMP shifts={shifts}, digit product 1234*5678=7006652')


def shared_dag_experiment():
    print('DAG_COUNTS: N case separate_butterflies joint_dag_butterflies packed_dag_butterflies')
    for n in (256,1024,4096,16384):
        rg = random.Random(121+n)
        a = [rg.randrange(2) for _ in range(n)]
        random_b = [rg.randrange(2) for _ in range(n)]
        patterns = [1,0,1,1,0,1,1,0]
        cases = {
            'independent_bits':(a,random_b),
            'identical_bits':(a,a[:]),
            'shifted_bits':(a,a[-n//8:]+a[:-n//8]),
            'period8_both':(patterns*(n//8), patterns[3:]+patterns[:3] if n==8 else (patterns[3:]+patterns[:3])*(n//8)),
        }
        for label,(x,y) in cases.items():
            standard=n*int(math.log2(n))
            g=JointFFTGraph()
            f,gf=g.eval_inputs(x,y)
            d=g.summary()['butterflies']
            pfa,pfb,sp=packed_dag(x,y)
            packed=sp['butterflies']
            assert np.allclose(f,pfa,atol=1e-6) and np.allclose(gf,pfb,atol=1e-6)
            print(f'{n} {label} {standard} {d} {packed}')


def run_timing(fn, reps=9):
    for _ in range(3): fn()
    times=[]
    for _ in range(reps):
        t=time.perf_counter_ns(); fn(); times.append((time.perf_counter_ns()-t)/1e6)
    return statistics.median(times)


def benchmark_numpy_convolutions():
    print('NUMPY_TIMES_MS: N two_complex_fft_plus_ifft one_packed_complex_fft_plus_ifft two_real_rffts_plus_irfft')
    rng=np.random.default_rng(20261008)
    for n in (1024, 4096, 16384, 65536, 262144):
        a = rng.integers(0,2,n).astype(np.float64)
        b = rng.integers(0,2,n).astype(np.float64)
        za = a+1j*b
        def plain():
            return np.fft.ifft(np.fft.fft(a)*np.fft.fft(b)).real
        def packed():
            return np.fft.ifft(np.fft.fft(za)**2).imag/2
        def real():
            return np.fft.irfft(np.fft.rfft(a)*np.fft.rfft(b),n=n)
        x=plain(); y=packed(); z=real()
        assert np.allclose(x,y,atol=1e-7) and np.allclose(x,z,atol=1e-7)
        t0=run_timing(plain, 9)
        t1=run_timing(packed, 9)
        t2=run_timing(real, 9)
        print(f'{n} {t0:.4f} {t1:.4f} {t2:.4f}')



def benchmark_graph_runtime():
    """Pure Python comparison of cross-input DAG and packed DAG, including bookkeeping."""
    from fft_collision_research import standard_fft
    print('PYTHON_DAG_MS: N case two_standard_fft joint_dag packed_dag')
    for n in (4096, 16384):
        rg = random.Random(808+n)
        first = [rg.randrange(2) for _ in range(n)]
        second = [rg.randrange(2) for _ in range(n)]
        period_a = [1, 0, 1, 1, 0, 0, 1, 0]*(n//8)
        period_b = [0, 1, 1, 0, 0, 1, 0, 1]*(n//8)
        for label, a, b in [('random_bits', first, second), ('period8',period_a,period_b)]:
            def run_two(): return standard_fft(a), standard_fft(b)
            def run_joint():
                g=JointFFTGraph()
                return g.eval_inputs(a,b)
            def run_packed(): return packed_dag(a,b)
            tt=[run_timing(f, reps=3) for f in (run_two,run_joint,run_packed)]
            print(f'{n} {label} ' + ' '.join(f'{v:.4f}' for v in tt))



def detect_rank_two_real_family(signals, tol=1e-9):
    """Discover 0/1/2 real-valued basis vectors, and recover coefficients.

    Return (basis, coeffs) if rank <=2, else None. O(M*N) numeric work
    for this fixed rank, including verification. Not numerically robust
    for extremely ill-conditioned inputs; intended as a research demo.
    """
    X = np.asarray(signals, dtype=np.float64)
    if X.ndim != 2 or not np.isfinite(X).all():
        raise ValueError('must be finite real 2D data')
    m, n = X.shape
    bases=[]
    coeffs=[]
    for row in X:
        if not bases:
            if np.max(np.abs(row)) <= tol:
                coeffs.append([])
                continue
            bases=[row.copy()]
            # retroactively initialize earlier zero rows
            coeffs=[[0.] for _ in coeffs]
            p0=int(np.argmax(np.abs(bases[0])))
            coeffs.append([1.])
            continue
        if len(bases) == 1:
            alpha=row[p0]/bases[0][p0]
            if np.max(np.abs(row-alpha*bases[0])) <= tol*(1+np.max(np.abs(row))):
                coeffs.append([float(alpha)])
                continue
            bases.append(row.copy())
            coeffs=[c+[0.] for c in coeffs]
            coeffs.append([0.,1.])
            determinants=bases[0][p0]*bases[1]-bases[0]*bases[1][p0]
            p1=int(np.argmax(np.abs(determinants)))
            det=determinants[p1]
            if abs(det) <= tol:
                return None
            continue
        det = bases[0][p0]*bases[1][p1]-bases[0][p1]*bases[1][p0]
        alpha=(row[p0]*bases[1][p1]-row[p1]*bases[1][p0])/det
        beta=(bases[0][p0]*row[p1]-bases[0][p1]*row[p0])/det
        predicted=alpha*bases[0]+beta*bases[1]
        if np.max(np.abs(predicted-row)) > tol*(1+np.max(np.abs(row))):
            return None
        coeffs.append([float(alpha),float(beta)])
    if not bases:
        return np.zeros((0,n)),np.zeros((m,0))
    return np.stack(bases),np.asarray(coeffs,dtype=np.float64)


def adaptive_rank_two_fft(signals):
    """Find 2-basis structure and reuse spectra, or fall back to regular FFT."""
    found=detect_rank_two_real_family(signals)
    if found is None:
        return np.fft.fft(signals,axis=1), 'fallback'
    basis, coeffs=found
    if len(basis)==0:
        return np.zeros_like(signals,dtype=np.complex128),'zero'
    return coeffs @ np.fft.fft(basis,axis=1), f'rank{len(basis)}'


def low_rank_family_experiment():
    """If M arrays live in span of r fixed vectors, use r FFTs + O(M r N) output.

    Signals' low-rank representation is known; discovery/verification is NOT timed.
    """
    print('LOW_RANK_MS: N M r independent_batched_fft known_basis_2_ffts autodetect_verify_2_basis_ffts')
    rng=np.random.default_rng(1008)
    for n in (4096,16384,65536):
        m=32; r=2
        basis = rng.standard_normal((r,n))
        coeffs = rng.integers(-3,4,(m,r))
        signals = coeffs @ basis
        assert signals.shape == (m,n)
        def direct(): return np.fft.fft(signals,axis=1)
        def reconstructed():
            f = np.fft.fft(basis,axis=1)
            return coeffs @ f
        assert np.allclose(direct(),reconstructed(),rtol=1e-10,atol=1e-7)
        t1=run_timing(direct,7)
        t2=run_timing(reconstructed,7)
        t3=run_timing(lambda: adaptive_rank_two_fft(signals),7)
        print(f'{n} {m} {r} {t1:.4f} {t2:.4f} {t3:.4f}')

if __name__ == '__main__':
    tests()
    shared_dag_experiment()
    benchmark_numpy_convolutions()
    benchmark_graph_runtime()
    low_rank_family_experiment()
