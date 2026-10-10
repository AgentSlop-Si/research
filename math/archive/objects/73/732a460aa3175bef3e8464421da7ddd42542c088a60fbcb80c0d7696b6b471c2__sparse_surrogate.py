"""Random input sparsification followed by a classical input-pruned full DFT.

Research target
---------------
For a fresh arbitrary dense vector x in C^N (N a power of two), construct a
k-sparse unbiased surrogate y, then compute *all* N Fourier coefficients of y
with the existing sparse DFT decomposition.

The theorem is for the unitary DFT U_N = F_N / sqrt(N):

    P[ ||U_N y - U_N x||_inf > eps ||x||_2 ] <= delta

provided

    k >= 4*tau2(x)/eps^2 * log(4N/delta),
    tau2(x) = ||x||_1^2 / (N ||x||_2^2) <= 1.

The proof is coordinatewise Hoeffding + a union bound.  The sparsification
lemma is a standard Maurey/importance-sampling phenomenon; the research
question is the algorithmic composition with the input-pruned full-output DFT.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence
import numpy as np

from hybrid_sparse import sparse_dft


@dataclass(frozen=True)
class SurrogatePlan:
    n: int
    epsilon: float
    delta: float
    l1: float
    l2: float
    tau2: float
    requested_samples: int
    actual_draws: int
    support_size: int
    sparse_b: int | None
    method: str


def _as_complex_vector(x: Sequence[complex]) -> np.ndarray:
    a = np.asarray(x, dtype=np.complex128)
    if a.ndim != 1 or a.size < 1:
        raise ValueError("x must be a nonempty 1-D vector")
    if not np.all(np.isfinite(a.real)) or not np.all(np.isfinite(a.imag)):
        raise ValueError("x must be finite")
    n = int(a.size)
    if n & (n - 1):
        raise ValueError("current sparse DFT backend requires power-of-two length")
    return a


def flatness_tau2(x: Sequence[complex]) -> float:
    a = _as_complex_vector(x)
    l1 = float(np.sum(np.abs(a)))
    l2 = float(np.linalg.norm(a))
    if l2 == 0.0:
        return 0.0
    return (l1 * l1) / (a.size * l2 * l2)


def universal_sample_count(n: int, epsilon: float, delta: float) -> int:
    """Samples for error <= epsilon * ||x||_1/sqrt(N), independent of x."""
    n=int(n); eps=float(epsilon); d=float(delta)
    if n<1: raise ValueError("n must be positive")
    if not (0.0 < eps < 1.0): raise ValueError("epsilon must lie in (0,1)")
    if not (0.0 < d < 1.0): raise ValueError("delta must lie in (0,1)")
    return max(1, math.ceil((4.0/(eps*eps))*math.log(4.0*n/d)))


def sufficient_sample_count(x: Sequence[complex], epsilon: float, delta: float) -> int:
    """Samples for the weaker adaptive error <= epsilon * ||x||_2."""
    a = _as_complex_vector(x)
    eps = float(epsilon); d = float(delta)
    if not (0.0 < eps < 1.0):
        raise ValueError("epsilon must lie in (0,1)")
    if not (0.0 < d < 1.0):
        raise ValueError("delta must lie in (0,1)")
    l2 = float(np.linalg.norm(a))
    if l2 == 0.0:
        return 0
    t2 = flatness_tau2(a)
    return max(1, math.ceil((4.0 * t2 / (eps * eps)) * math.log(4.0 * a.size / d)))


def _draw_importance_indices(weights: np.ndarray, k: int, rng: np.random.Generator) -> np.ndarray:
    """Draw iid indices proportional to nonnegative weights.

    Uses one cumulative scan plus binary searches.  The theoretical algorithm
    can equivalently sort k uniforms and merge them with the cumulative scan in
    O(N + k log k) time.
    """
    if k <= 0:
        return np.empty(0, dtype=np.intp)
    total = float(weights.sum())
    if total <= 0.0:
        return np.empty(0, dtype=np.intp)
    cdf = np.cumsum(weights, dtype=np.float64)
    # Guard the final endpoint against accumulated roundoff.
    cdf[-1] = total
    u = rng.random(k) * total
    return np.searchsorted(cdf, u, side="right").astype(np.intp, copy=False)


def sparsify_input(
    x: Sequence[complex],
    epsilon: float,
    delta: float,
    *,
    rng: np.random.Generator | None = None,
    samples: int | None = None,
) -> tuple[dict[int, complex], SurrogatePlan]:
    """Return the sampled k-sparse surrogate as an index->value dictionary."""
    a = _as_complex_vector(x)
    eps = float(epsilon); d = float(delta)
    if rng is None:
        rng = np.random.default_rng()
    l1 = float(np.sum(np.abs(a)))
    l2 = float(np.linalg.norm(a))
    if l2 == 0.0:
        plan = SurrogatePlan(a.size, eps, d, 0.0, 0.0, 0.0, 0, 0, 0, None, "zero")
        return {}, plan
    tau2 = (l1*l1)/(a.size*l2*l2)
    k = sufficient_sample_count(a, eps, d) if samples is None else int(samples)
    if k < 1:
        raise ValueError("samples must be positive for nonzero input")

    weights = np.abs(a)
    draws = _draw_importance_indices(weights, k, rng)
    idx, counts = np.unique(draws, return_counts=True)
    values: dict[int, complex] = {}
    scale = l1 / k
    for j, count in zip(idx.tolist(), counts.tolist()):
        z = a[j]
        # j cannot have zero weight if it was sampled.
        phase = z / abs(z)
        values[int(j)] = complex(count * scale * phase)

    plan = SurrogatePlan(
        n=a.size, epsilon=eps, delta=d, l1=l1, l2=l2, tau2=tau2,
        requested_samples=k, actual_draws=k, support_size=len(values),
        sparse_b=None, method="importance-with-replacement",
    )
    return values, plan


def approximate_dft_all(
    x: Sequence[complex],
    epsilon: float,
    delta: float,
    *,
    rng: np.random.Generator | None = None,
    samples: int | None = None,
    backend: str = "scipy",
    scale: str = "l2",
    exact_sparse_bypass: bool = True,
    fallback_dense_if_k_ge_n: bool = True,
    return_plan: bool = False,
):
    """Approximate every unitary DFT coefficient of a fresh dense input.

    If the sufficient number of draws reaches N, the default implementation
    falls back to a complete numerical FFT.  This does not affect the fixed-
    epsilon asymptotic result, for which k=O(log N).
    """
    a = _as_complex_vector(x)
    if scale not in ("l2","l1_ceiling"):
        raise ValueError("scale must be 'l2' or 'l1_ceiling'")
    requested = samples
    if requested is None and scale == "l1_ceiling":
        requested = universal_sample_count(a.size, epsilon, delta)

    # The O(N) scan needed for norms also reveals exact support.  If that
    # support is already smaller than the Monte-Carlo budget, do no sampling.
    nz = np.flatnonzero(a != 0)
    budget = sufficient_sample_count(a,epsilon,delta) if requested is None else int(requested)
    if exact_sparse_bypass and 0 < nz.size <= budget:
        exact = {int(j):complex(a[j]) for j in nz}
        raw,spl = sparse_dft(a.size, exact.items(), backend=backend, return_plan=True)
        l1=float(np.sum(np.abs(a))); l2=float(np.linalg.norm(a)); tau2=(l1*l1)/(a.size*l2*l2) if l2 else 0.0
        plan=SurrogatePlan(a.size,float(epsilon),float(delta),l1,l2,tau2,budget,0,int(nz.size),spl.b,"exact-sparse-bypass")
        out=raw/math.sqrt(a.size)
        return (out,plan) if return_plan else out

    sparse, plan0 = sparsify_input(a, epsilon, delta, rng=rng, samples=requested)
    k = plan0.requested_samples
    if plan0.method == "zero":
        out = np.zeros(a.size, dtype=np.complex128)
        return (out, plan0) if return_plan else out

    if fallback_dense_if_k_ge_n and k >= a.size:
        try:
            from scipy import fft as sp_fft
            out = sp_fft.fft(a, norm="ortho")
        except Exception:
            out = np.fft.fft(a, norm="ortho")
        plan = SurrogatePlan(**{**plan0.__dict__, "method":"dense-fallback"})
        return (out, plan) if return_plan else out

    raw, spl = sparse_dft(a.size, sparse.items(), backend=backend, return_plan=True)
    out = raw / math.sqrt(a.size)
    plan = SurrogatePlan(**{**plan0.__dict__, "sparse_b":spl.b, "method":"sparse-pruned"})
    return (out, plan) if return_plan else out


def theorem_failure_bound(n: int, epsilon: float, tau2: float, k: int) -> float:
    """The explicit union-bound upper bound 4N exp(-k eps^2/(4 tau^2))."""
    if tau2 <= 0.0:
        return 0.0
    return min(1.0, 4.0*n*math.exp(-k*epsilon*epsilon/(4.0*tau2)))
