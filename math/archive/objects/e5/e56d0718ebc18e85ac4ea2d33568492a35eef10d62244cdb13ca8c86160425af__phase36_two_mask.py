"""Phase 36: two internal masks, positive Green bridge, Fourier phase rigidity.

Core Green applications and transpose applications cost O(N) arithmetic per vector.
Numerical Sinkhorn calibration is an approximation to the positive scaling
problem, not an exact algebraic FFT factorization.
"""
from __future__ import annotations
import argparse
import json
import math
from dataclasses import dataclass
from random import Random

import numpy as np


def cycle_from_seed(n: int, seed: int) -> list[int]:
    seq = list(range(n))
    Random(seed).shuffle(seq)
    # Distinct random Hamiltonian orders; they are not claimed expanders here.
    return seq


@dataclass
class CyclicMarkovGreen:
    cycle: list[int]
    beta: float

    def __post_init__(self):
        self.n = len(self.cycle)
        assert sorted(self.cycle) == list(range(self.n))
        assert 0 < self.beta < 1
        self.reverse_cycle = [self.cycle[0]] + list(reversed(self.cycle[1:]))
        self.position = np.empty(self.n, dtype=np.int64)
        for j, index in enumerate(self.cycle):
            self.position[index] = j

    def _apply_one(self, x: np.ndarray, order: list[int]) -> np.ndarray:
        """Return (1-beta)*(I-beta W_order)^(-1) x, O(N) arithmetic.

        W_order maps e_{order[j]} to e_{order[j+1]} with wraparound.
        """
        x = np.asarray(x)
        assert x.ndim == 1 and x.shape[0] == self.n
        y = np.zeros(self.n, dtype=np.result_type(x, np.float64))
        s = y.dtype.type(0)
        for j in range(1, self.n):
            s = self.beta * s + x[order[j]]
        y[order[0]] = (x[order[0]] + self.beta * s) / (1 - self.beta ** self.n)
        for j in range(1, self.n):
            y[order[j]] = x[order[j]] + self.beta * y[order[j-1]]
        return (1 - self.beta) * y

    def apply(self, x):
        return self._apply_one(x, self.cycle)

    def transpose_apply(self, x):
        return self._apply_one(x, self.reverse_cycle)

    def dense(self):
        n = self.n
        pos = self.position
        powers = (pos[:, None] - pos[None, :]) % n
        return ((1-self.beta) / (1-self.beta**n)) * self.beta ** powers

    def ratio_bound(self):
        return self.beta ** (-(self.n-1))


@dataclass
class WeakOuter:
    green: CyclicMarkovGreen
    eta: float = 0.01

    def __post_init__(self):
        assert 0 < self.eta < 0.5
        self.n = self.green.n

    def apply(self, x):
        x = np.asarray(x)
        return (1-self.eta)*x + self.eta*self.green.apply(x)

    def transpose_apply(self, x):
        x = np.asarray(x)
        return (1-self.eta)*x + self.eta*self.green.transpose_apply(x)

    def dense(self):
        return (1-self.eta)*np.eye(self.n) + self.eta*self.green.dense()

    def inverse_apply(self, x):
        """Exact algebraic inverse of (1-eta)I+eta K, using one cyclic solve.

        K=(1-beta)*(I-beta W)^-1; the numerator denominator factor is
        a I - b W, a=1-eta*beta, b=(1-eta)*beta.
        One cyclic Green solve with beta'=b/a applies A^-1 in O(N).
        """
        x=np.asarray(x)
        z=np.empty_like(x,dtype=np.result_type(x,np.float64))
        cyc=self.green.cycle
        for j in range(self.n):
            z[cyc[j]] = x[cyc[j]] - self.green.beta*x[cyc[j-1]]
        a=1-self.eta*self.green.beta
        b=(1-self.eta)*self.green.beta
        green=CyclicMarkovGreen(cyc,b/a)
        return green.apply(z)/(a-b)


@dataclass
class TwoMaskCircuit:
    A: WeakOuter
    B: CyclicMarkovGreen
    C: WeakOuter
    x: np.ndarray
    y: np.ndarray

    def apply(self, vec):
        return self.A.apply(self.x * self.B.apply(self.y * self.C.apply(vec)))

    def transpose_apply(self, vec):
        return self.C.transpose_apply(self.y * self.B.transpose_apply(self.x * self.A.transpose_apply(vec)))

    def dense(self):
        return self.A.dense() @ (self.x[:,None] * self.B.dense() * self.y[None,:]) @ self.C.dense()


def make_green_triplet(n: int, eta=0.01):
    beta = 1-1/n
    return (WeakOuter(CyclicMarkovGreen(cycle_from_seed(n, 36001), beta), eta),
            CyclicMarkovGreen(cycle_from_seed(n, 36007), beta),
            WeakOuter(CyclicMarkovGreen(cycle_from_seed(n, 36013), beta), eta))


def sinkhorn_green(A: WeakOuter, B: CyclicMarkovGreen, C: WeakOuter,
                   tolerance=1.e-12, max_iterations=250):
    """Solve boundary calibration via positive matrix scaling.

    r=A[0,:], c=C[:,0]; find diag(u) B diag(v) with row r and col c.
    Return x=u/r, y=v/c so that A diag(x) B diag(y) C matches
    the unnormalized Fourier matrix's first row and column.
    """
    n = A.n
    assert B.n == C.n == n
    e0 = np.eye(1,n,0,dtype=float).ravel()
    r = A.transpose_apply(e0)
    c = C.apply(e0)
    assert min(r.min(), c.min()) > 0
    assert abs(sum(r)-1)<1e-10 and abs(sum(c)-1)<1e-10
    v = np.ones(n)
    steps = 0
    for k in range(1,max_iterations+1):
        u = r / B.apply(v)
        v = c / B.transpose_apply(u)
        v /= np.mean(v)
        u = r / B.apply(v)
        col = v * B.transpose_apply(u)
        relative_error = float(np.max(np.abs(col / c - 1)))
        steps = k
        if relative_error < tolerance:
            break
    x = u/r
    y = v/c
    circuit = TwoMaskCircuit(A,B,C,x,y)
    return circuit, dict(iterations=steps, relative_marginal_error=relative_error,
                         x_spread=float(x.max()/x.min()),
                         y_spread=float(y.max()/y.min()),
                         kernel_spread=float(B.ratio_bound()))


def fourier_matrix(n):
    t=np.arange(n,dtype=np.int64)
    return np.exp((-2j*np.pi/n)*(t[:,None]*t[None,:]))/math.sqrt(n)


def projective_phase_floor(n):
    """All x_i,y_j complex and ALL entrywise-positive B are included."""
    g=math.gcd(2,n)
    return max(0.5*math.sqrt(1-1/n),
               math.sqrt(max(0., (1-math.sqrt(g/n))/2)))


def sandwich_phase_floor(n, delta_A, delta_C):
    """For M=A D1 P1 B P2 D2 C, B positive, ||A-I||2<=delta_A, etc."""
    assert 0<=delta_A<1 and 0<=delta_C<1
    scale=(1-delta_A)*(1-delta_C)
    return max(0., scale*(projective_phase_floor(n)+1)-1)


def audit(n_values=(4,8,16,32,64,128,256,512), eta=0.01):
    entries=[]
    for n in n_values:
        A,B,C=make_green_triplet(n,eta)
        circ,fit=sinkhorn_green(A,B,C)
        e0=np.zeros(n);e0[0]=1
        first_col=circ.apply(e0)
        first_row=circ.transpose_apply(e0)
        e1=np.zeros(n);e1[1]=1
        next_col=circ.apply(e1)
        w=np.exp(-2j*np.pi*np.arange(n)/n)
        next_mismatch=float(np.max(np.abs(next_col-w)))
        bound=sandwich_phase_floor(n,2*eta,2*eta)
        record=dict(N=n, calibration_iterations=fit['iterations'],
                    max_first_col_error=float(np.max(np.abs(first_col-1))),
                    max_first_row_error=float(np.max(np.abs(first_row-1))),
                    max_second_col_error=next_mismatch,
                    analytical_phase_error_floor=bound,
                    two_mask_spreads=[fit['x_spread'],fit['y_spread']],
                    middle_kernel_spread_bound=fit['kernel_spread'],
                    scaling_relative_error=fit['relative_marginal_error'])
        if n<=64:
            F=fourier_matrix(n)
            M=circ.dense()/math.sqrt(n)
            distance=float(np.linalg.norm(M-F,2))
            record['measured_operator_norm_error']=distance
            assert distance+1e-9 >= bound
            assert np.max(np.abs(M@e0-F@e0)) <1e-9
        entries.append(record)
    return dict(phase=36, result='positive Green two-mask calibration plus Fourier phase spectral obstruction',
                Green_apply='O(N)', Sinkhorn_per_iteration='O(N)',
                overall_exact_FFT=False, cases=entries)


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',default='audit.json')
    args=ap.parse_args()
    report=audit()
    with open(args.output,'w') as f: json.dump(report,f,indent=2);f.write('\n')
    for e in report['cases']:
        print(f"N={e['N']:4} sinkhorn={e['calibration_iterations']:2} first_cross={max(e['max_first_col_error'],e['max_first_row_error']):.2e} next_col={e['max_second_col_error']:.4g} spectral_floor={e['analytical_phase_error_floor']:.6f}")
