# RECOVER HERE — HERO #17 Phase 18, 10 October 2026

## Absolute goal
Exact sequential `O(N)` for a fresh arbitrary-input, all-output DFT, with charged preprocessing, computation and output. **Still NOT achieved.** No claims about general integer multiplication.

## Immediate predecessor
`fft_hero17_phase17_sparse_graph_feedback_2026-10-10.zip`, embedded in this package as `PHASE17_PREDECESSOR.zip`. Phase17 low-rank graph-feedback and covariance-defect theorems survive; do not restart its quotient search.

## Newly proved and tested

1. Growing-`K` noncommuting Green branches `G_j=(I-alpha*S-beta*q^j*U)^-1`, where `US=q SU`, `U^K=I`, and `N=KM`, have *one exact `O(N)` fused evaluator*:

   `mean_j G_j = [(1-beta^K)I-alpha^K S^K]^-1 * sum_(r<K)alpha^r S^r`.

2. Exact nonsingularity iff `(1-beta^K)^M != alpha^N`; robustly handles zero-pivot branch cases.
3. Rank of the full averaged operator is `N` unless `alpha^N=1`, in which case it is `N-K+1`.
4. Fourier-weighted sector `R_ell` has Gaussian-binomial polynomial evaluator costing `O((ell+1)N+ell^2+K)`; fixed `ell` remains linear, even if `K` grows with `N`.
5. Any sector sum commutes with `S^K`; exact rank of `[F,S^K]` is `N-K` when `N-K` even, otherwise `N`. This forces a corresponding additive-rank correction budget.
6. At odd prime N, Fourier has all `N^2` Weyl coefficients nonzero. One-direction Weyl-line sum requires `N+1` ungauged lines to cover support, or `N` arbitrary affine Weyl lines if endpoint gauges are Weyl monomials. This is NOT a lower bound for products of Green stages.
7. Two Green stages already give full Weyl support in linear work: critical negative control against abusing item 6.

## Reproducibility and measurements

- `python -m unittest -v test_phase18` (25 groups passed).
- `python independent_audit.py` independently solves the original K branches and checks small full matrices via Gaussian elimination.
- At `N=65536`, `K=64`, `p=65537`: 65,536 exact outputs matched; fused charged field operations 655,693 vs 25,231,832 direct shared-prep 64-branch reference = 38.48x fewer for the Green averaging task. NOT a Fourier benchmark.
- `python weyl_line_gate.py` checks full Weyl support and finite projective-plane line coverage at n=3,5,7,11.
- Other exact tests: 121 small Gaussian-reference full vectors; 158 weighted Gaussian-reference cases. Full JSON in `AUDIT_RESULTS.json`.

## Known limits and failure modes

- `R_0` is circulant and cannot equal `F` for N>1. Any sum of these unweighted twirls still commutes with S.
- Every fixed-K weighted sector commutes with `S^K`; sums of these sectors cannot equal Fourier for K<N.
- Linear support cover bounds are grammar-specific. Products of two Green stages can produce full Weyl support and still cost O(N) without being Fourier.
- Scalar field model assumes supplied primitive root and field; implementation accounts for its validation in field-operation ledger and O(sqrt N) RAM integer operations. Root *search* and bit complexity are outside this model.
- The quantum-binomial and finite Weyl ingredients are classical. Publication priority unverified.
- If an inverse denominator is singular, do not use the formula; it is correctly rejected by the implementation.

## Phase 19 highest-value target

Construct a multiorientation **product/branching** Green network that escapes the Weyl-line support grammar and genuinely shares across noncommuting planes, while satisfying both exact Fourier covariance `M S=T^-1 M` and `M e0=ones`. Count every raw-input read, scalar operation, precomputation, root lookup, memory access and explicit output write in a declared model. Compare against both radix FFT and the already-published uniform sub-`N log N` exact-complex bound (OpenAI Math #130), model matched.
