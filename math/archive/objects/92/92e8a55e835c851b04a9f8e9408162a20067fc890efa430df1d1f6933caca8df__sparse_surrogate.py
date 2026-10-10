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


# ---------------------------------------------------------------------------
# Stronger v2 tradeoffs: vanishing accuracy, heavy+tail sparsification,
# and a rigorous ceiling for every time-domain sparse surrogate.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class AccuracyTradeoff:
    n: int
    epsilon: float
    delta: float
    samples: int
    sparse_b: int
    inner_log2: int
    full_log2: int
    depth_ratio: float
    asymptotic_log_cost: float


@dataclass(frozen=True)
class HeadTailPlan:
    n: int
    epsilon: float
    delta: float
    head_size: int
    head_l1: float
    tail_l1: float
    total_l1: float
    tail_ratio: float
    requested_samples: int
    tail_nnz: int
    support_upper_bound: int
    method: str


def accuracy_tradeoff(n: int, epsilon: float, delta: float) -> AccuracyTradeoff:
    """Operation-count proxy for the universal sparse-surrogate theorem.

    If ``k = Theta(epsilon^-2 log(N/delta))``, the existing sparse-input
    full-output DFT needs ``O(N log(k+2))`` arithmetic.  This helper reports
    the exact theorem sample count, the next radix-2 inner width and the
    corresponding radix-depth ratio.
    """
    n = int(n); eps=float(epsilon); d=float(delta)
    k = universal_sample_count(n, eps, d)
    b = 1 << (max(1, k)-1).bit_length()
    inner = b.bit_length()-1
    full = max(1, n.bit_length()-1) if n > 0 and not (n & (n-1)) else max(1, math.ceil(math.log2(n)))
    return AccuracyTradeoff(
        n=n, epsilon=eps, delta=d, samples=k, sparse_b=b,
        inner_log2=inner, full_log2=full,
        depth_ratio=inner/full,
        asymptotic_log_cost=math.log(max(2.0, k), 2.0),
    )


def head_tail_sample_count_from_norms(
    n: int,
    total_l1: float,
    tail_l1: float,
    epsilon: float,
    delta: float,
) -> int:
    """Samples needed after keeping a head exactly.

    Target guarantee:

        ||U_N y - U_N x||_inf <= epsilon * ||x||_1 / sqrt(N).

    Only the residual tail is randomized.  If its entire deterministic Fourier
    contribution is already below the target (tail_l1 <= epsilon*total_l1),
    zero random samples suffice.
    """
    n=int(n); L=float(total_l1); T=float(tail_l1); eps=float(epsilon); d=float(delta)
    if n < 1: raise ValueError("n must be positive")
    if L < 0 or T < 0 or T > L*(1+1e-12): raise ValueError("bad l1 norms")
    if not (0.0 < eps < 1.0): raise ValueError("epsilon must lie in (0,1)")
    if not (0.0 < d < 1.0): raise ValueError("delta must lie in (0,1)")
    if L == 0.0 or T == 0.0 or T <= eps*L:
        return 0
    rho=T/L
    return max(1, math.ceil((4.0*rho*rho/(eps*eps))*math.log(4.0*n/d)))


def _top_s_indices(a: np.ndarray, s: int) -> np.ndarray:
    s=int(s)
    if s <= 0:
        return np.empty(0,dtype=np.intp)
    if s >= a.size:
        return np.arange(a.size,dtype=np.intp)
    mag=np.abs(a)
    # argpartition is expected linear time and does not fully sort the input.
    return np.argpartition(mag, a.size-s)[a.size-s:].astype(np.intp,copy=False)


def _head_tail_stats(a: np.ndarray, s: int) -> tuple[np.ndarray,float,float,int]:
    idx=_top_s_indices(a,s)
    total=float(np.sum(np.abs(a)))
    if idx.size == 0:
        return idx,0.0,total,int(np.count_nonzero(a))
    head_l1=float(np.sum(np.abs(a[idx])))
    tail_l1=max(0.0,total-head_l1)
    tail_nnz=int(np.count_nonzero(a)) - int(np.count_nonzero(a[idx]))
    return idx,head_l1,tail_l1,max(0,tail_nnz)


def make_head_tail_plan(
    x: Sequence[complex],
    epsilon: float,
    delta: float,
    head_size: int,
) -> HeadTailPlan:
    a=_as_complex_vector(x)
    s=min(max(0,int(head_size)),a.size)
    idx,head_l1,tail_l1,tail_nnz=_head_tail_stats(a,s)
    total=head_l1+tail_l1
    k=head_tail_sample_count_from_norms(a.size,total,tail_l1,epsilon,delta) if total else 0
    if tail_nnz <= k:
        method="exact-tail"
        support=s+tail_nnz
        k=tail_nnz
    elif k == 0:
        method="head-only"
        support=s
    else:
        method="sample-tail"
        support=s+k
    return HeadTailPlan(
        n=a.size,epsilon=float(epsilon),delta=float(delta),head_size=s,
        head_l1=head_l1,tail_l1=tail_l1,total_l1=total,
        tail_ratio=(tail_l1/total if total else 0.0),
        requested_samples=k,tail_nnz=tail_nnz,
        support_upper_bound=min(a.size,support),method=method,
    )


def plan_head_tail(
    x: Sequence[complex],
    epsilon: float,
    delta: float,
    *,
    candidates: Sequence[int] | None = None,
    max_head: int | None = None,
) -> HeadTailPlan:
    """Choose a head size by minimizing the certified sparse-support budget.

    The default candidate family is ``0,1,2,4,...`` up to a polylogarithmic
    head budget.  Each candidate uses an expected-linear ``argpartition``;
    hence the default planning work is ``O(N log log N)`` and remains within
    the target transform bound.
    """
    a=_as_complex_vector(x); n=a.size
    if candidates is None:
        if max_head is None:
            max_head=min(n, max(1, int(math.ceil(math.log2(max(2,n))**2))))
        else:
            max_head=min(n,max(0,int(max_head)))
        vals=[0]
        p=1
        while p < max_head:
            vals.append(p); p*=2
        if max_head not in vals: vals.append(max_head)
        candidates=vals
    plans=[]
    for s in dict.fromkeys(int(v) for v in candidates):
        if 0 <= s <= n:
            plans.append(make_head_tail_plan(a,epsilon,delta,s))
    if not plans: raise ValueError("no valid head candidates")
    return min(plans,key=lambda p:(p.support_upper_bound,p.requested_samples,p.head_size))


def sparsify_head_tail(
    x: Sequence[complex],
    epsilon: float,
    delta: float,
    *,
    head_size: int | None = None,
    plan: HeadTailPlan | None = None,
    rng: np.random.Generator | None = None,
) -> tuple[dict[int,complex],HeadTailPlan]:
    """Keep the largest coordinates exactly and sample only the l1 tail."""
    a=_as_complex_vector(x)
    if rng is None: rng=np.random.default_rng()
    if plan is None:
        plan = plan_head_tail(a,epsilon,delta) if head_size is None else make_head_tail_plan(a,epsilon,delta,head_size)
    if plan.n != a.size: raise ValueError("plan length mismatch")
    idx=_top_s_indices(a,plan.head_size)
    chosen=np.zeros(a.size,dtype=bool); chosen[idx]=True
    out={int(j):complex(a[j]) for j in idx if a[j] != 0}
    residual=a.copy(); residual[chosen]=0
    tail_nz=np.flatnonzero(residual != 0)
    if plan.method == "exact-tail" or tail_nz.size <= plan.requested_samples:
        for j in tail_nz:
            out[int(j)]=complex(a[j])
        return out, HeadTailPlan(**{**plan.__dict__,"method":"exact-tail","requested_samples":int(tail_nz.size),"support_upper_bound":len(out)})
    if plan.requested_samples == 0 or plan.tail_l1 == 0.0:
        return out, plan
    draws=_draw_importance_indices(np.abs(residual),plan.requested_samples,rng)
    jj,counts=np.unique(draws,return_counts=True)
    scale=plan.tail_l1/plan.requested_samples
    for j,c in zip(jj.tolist(),counts.tolist()):
        z=residual[j]
        if z != 0:
            out[int(j)]=out.get(int(j),0j)+complex(c*scale*(z/abs(z)))
    return out, HeadTailPlan(**{**plan.__dict__,"support_upper_bound":len(out)})


def approximate_dft_all_head_tail(
    x: Sequence[complex],
    epsilon: float,
    delta: float,
    *,
    head_size: int | None = None,
    plan: HeadTailPlan | None = None,
    rng: np.random.Generator | None = None,
    backend: str = "scipy",
    return_plan: bool = False,
):
    """All-bin unitary DFT using exact heavy coordinates + sampled residual."""
    a=_as_complex_vector(x)
    sparse,hplan=sparsify_head_tail(a,epsilon,delta,head_size=head_size,plan=plan,rng=rng)
    if len(sparse) >= a.size:
        try:
            from scipy import fft as sp_fft
            out=sp_fft.fft(a,norm="ortho")
        except Exception:
            out=np.fft.fft(a,norm="ortho")
        return (out,hplan) if return_plan else out
    raw,spl=sparse_dft(a.size,sparse.items(),backend=backend,return_plan=True)
    out=raw/math.sqrt(a.size)
    return (out,hplan) if return_plan else out


def best_k_term_l2_tail(x: Sequence[complex], k: int) -> float:
    """Exact best k-term time-domain l2 approximation error."""
    a=_as_complex_vector(x); k=max(0,min(int(k),a.size))
    if k >= a.size: return 0.0
    sq=np.abs(a)**2
    if k == 0: return float(math.sqrt(float(np.sum(sq))))
    # Keep the k largest magnitudes; sum the rest without a full sort.
    cut=a.size-k
    part=np.partition(sq,cut)
    return float(math.sqrt(float(np.sum(part[:cut]))))


def sparse_surrogate_linf_lower_bound(x: Sequence[complex], k: int) -> float:
    """Universal lower bound for *any* k-sparse surrogate y.

    Since U_N is unitary,
        ||U_N(y-x)||_inf >= ||y-x||_2/sqrt(N)
    and every k-sparse y has l2 error at least the best k-term tail of x.
    This bound permits arbitrary signed/complex surrogate weights.
    """
    a=_as_complex_vector(x)
    return best_k_term_l2_tail(a,k)/math.sqrt(a.size)


def flat_natural_scale_support_lower_bound(n: int, eta: float) -> int:
    """Support necessary for natural-scale l_inf accuracy on flat inputs.

    For constant-modulus x, any k-sparse y satisfying

        ||U_N(y-x)||_inf <= eta * ||x||_2/sqrt(N)

    must obey k >= N(1-eta^2).
    """
    n=int(n); eta=float(eta)
    if n < 1: raise ValueError("n must be positive")
    if not (0.0 <= eta <= 1.0): raise ValueError("eta must lie in [0,1]")
    return max(0,math.ceil(n*(1.0-eta*eta)-1e-12))
