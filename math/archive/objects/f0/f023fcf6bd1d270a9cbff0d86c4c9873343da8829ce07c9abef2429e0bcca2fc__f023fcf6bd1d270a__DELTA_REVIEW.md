# Sparse-surrogate v2: focused delta review

Source: `research_inputs/sparse_surrogate_v2/fft130_adaptive_merge/`.
Reviewed new v2 research, head/tail code, six new tests and benchmark construction.
Original files remain unchanged. This supplements the earlier v1 review.

## Valid additions

The head/tail sample budget is correct: replacing the full l1 mass by the tail
mass multiplies the required samples by (||tail||_1/||x||_1)^2. The head-only
criterion ||tail||_1<=epsilon||x||_1 follows directly from the Fourier triangle
inequality. The Parseval bound sigma_k(x)_2/sqrt(N), including the flat-input
requirement k>=N(1-eta^2) at RMS-bin accuracy, is valid for complex weights.

The vanishing-accuracy schedules are valid in the stated ideal model. When
epsilon=N^(-o(1)) and delta is polynomially small, k=N^o(1), so sampling and
coalescing costs do not erase the displayed sub-N-log-N transform bound.
The error *multiplier* vanishes; absolute error need not vanish without an
input normalization. For x=(1,...,1), the stated polylogarithmic bound is
sqrt(N)/(log N)^a, which grows.

The new complex-weight support barrier is also valid. Alon's primary
[Theorem 1.1](https://web.math.princeton.edu/~nalon/PDFS/identity1.pdf) applies
to any real n-by-n matrix with diagonal magnitude at least 1/2, off-diagonal
magnitude at most epsilon, and 1/(2sqrt(n))<=epsilon<1/4. It gives rank at least
c log(n)/(epsilon^2 log(1/epsilon)). The proposed realification has n=2N,
diagonal at least 1-epsilon, all off-diagonal entries at most epsilon, and
rank at most 2k. Thus the support conclusion follows with threshold
epsilon>=1/(2sqrt(2N)). This restricts time-domain sparse surrogates; it is
not a runtime lower bound on arbitrary approximate FFT algorithms.

## Corrections needed for compressible-input claims

The source correctly states that its default planner costs O(N log log N).
It repeats full-length selection and scans for each candidate. Consequently
the displayed O(N) and O(N log log log N) compressible *transform* costs are
not the end-to-end costs of that default implementation.

`linear_head_planner.py` repairs this independently: select the largest H
entries once, sort only those H entries, compute prefix masses/nonzero counts,
and evaluate J candidate sizes in O(J). Its cost is O(N+H log H+J), under the
same linear-selection model. For the default H=O(log^2 N), it is O(N).
Applying the selected head may perform another O(N) selection, which preserves
the bound. The 65,536-entry check observes nine source selections versus one.

The compressibility assumption also needs normalization. An absolute envelope
|x|_(j)<=C exp(-cj) does not suffice for an arbitrary family of fresh inputs.
For each N, let all entries equal exp(-N). This satisfies C=c=1 for j=1..N,
but keeping 1-epsilon of its l1 mass requires at least (1-epsilon)N entries.
A sufficient correction is the uniform relative envelope

    |x|_(j) <= C ||x||_1 exp(-cj),

with constants independent of N. Its tail ratio is bounded by a constant times
exp(-cs), giving s=O(log(1/epsilon)). Under this corrected assumption and the
linear planner, the claimed fixed-accuracy O(N) and polylogarithmic-accuracy
O(N log log log N) end-to-end bounds are justified.

## Input-bound plans and numerical behavior

The v2 API checks only a supplied plan's length. Its tail mass, sample budget
and head-only decision depend on the actual input and requested tolerance.
Reusing a spike's head-only plan on a flat vector of length 1024 produced error
31.96875 against target 0.32: a deterministic factor-99.90 violation.
`apply_refreshed_head_plan` treats the plan as a head-size hint and recomputes
the masses/budget for the current input and tolerances in O(N). The reproduced
case then has zero numerical error.

Do not transfer the v1 norm-underflow result to the new head/tail entrypoint.
Fresh tests at flat magnitudes 1e-200 and 1e200 both returned finite, correct
DC values through its exact-tail branch. This is limited numerical evidence;
tail subtraction, sums, phases and FFTs still lack certified rounding bounds.
The unchanged older entrypoint is a separate code path.

## Comparison with the energy-pruned graph

The energy-pruned DIF proof is consistent: nodes at any depth have disjoint
output sets and conserved total squared norm. At most epsilon_E^(-2) nodes
exceed epsilon_E||x||_2; summing node lengths gives

    O(N[1+min(log N,log(1/epsilon_E))]).

This controls error at epsilon_E||x||_2. To meet v2's generally stronger target,
set tau=||x||_1/(sqrt(N)||x||_2) and epsilon_E=epsilon*tau. Its calibrated bound is

    O(N[1+min(log N,log(1/epsilon)+log(1/tau))]).

The calibrated graph does not uniformly improve v2. For an impulse,
tau=N^(-1/2), and every Fourier coefficient exceeds the calibrated threshold
when epsilon<1. The graph executes the entire DIF tree, whereas an exact
sparse-input transform costs O(N). For flat-magnitude inputs tau=1, the scales
agree and the graph's fixed-epsilon ideal work bound is O(N). Output pruning
does not contradict Alon's bound: it does not require a sparse time-domain
surrogate. Neither mechanism establishes an exact arbitrary-input FFT gain.

## Checks and files

- Six new source tests passed; the broader 47-test statement was not rerun.
- Sixteen planner comparisons matched source choices and support budgets.
- The stale-plan failure and refreshed-plan correction were reproduced.
- The v2 benchmark computes its plan before starting `wall_ms`; those saved
  timings exclude planning and are not complete cold-call times.
- `checks.json` records these tests and selection counts; `provenance.json`
  records source hashes and commands. No large benchmarks were rerun.

Run local additions with the v2 source directory on PYTHONPATH:

    PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research_inputs/sparse_surrogate_v2/fft130_adaptive_merge python check_v2.py
