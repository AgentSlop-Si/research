# R18 research report — exact finite synthesis, no asymptotic win

**16 October 2026. Bottom line:** the target o(N log N) has not been achieved.
This round replaces the previous approximate frozen circuit by a different,
fully refitted four-stage construction. An outward exact-rational contraction
certificate establishes an exact F16 factorization in its specified affine
chart. The attempts to extend it to N32 did not succeed. Neither an asymptotic
exponent improvement nor a practical FFT speedup follows.

## The actual research change

The research table separates a cheap global operator from a Fourier
factorization. It also already contains C09, a different exact sixteen-point
Green certificate. That finite seed was not ignored or relabeled as new.
The user's Phase46_Theorems.md already has the dense skew-sign scan, and R17
already has scaled recurrence compilation.

R18 uses these scans as ingredients and refits **every stage**. Each stage is

    S = diag(d) + diag(a) H_pi diag(b) + diag(c) H_rho diag(e),

with two independently routed skew-sign matrices H. H=2G-I for a fixed
antiperiodic cyclic inverse G. At N16 there are four stages, eight total
nontrivial cyclic inverses, four free diagonals, and 320 complex parameters.
All eight orders are written explicitly in root_candidate.json. The 256
active parameters are specified by a polynomial system and an isolating
ball; 64 others are fixed dyadic numbers.

This changes the correction class and the previous factors. It does not
contradict R17's one-additional-block exclusion for its *frozen* prefix.
It does not retain a shortened outer FFT or claim that multibase conversion
itself has improved. It tests the cheap-global-stage synthesis question.

## What is certified exactly

With the algebraic coefficients defined by the isolated solution,

    S3 S2 S1 S0 = F16,  F16[i,j]=exp(-2 pi i i j/16)/4.

The same coefficient choices therefore work for every complex 16-vector.
The result is more than agreement on test vectors and more than a small
floating residual. The verifier uses 320-bit dyadic interval centers/radii,
exact integer dot products, and rational comparisons. It encloses all 256
complex residuals and the full 256-by-256 selected Jacobian.

The actual fixed-point bounds are approximately

    ||B f(z0)|| <= 3.5199445847e-90,
    ||I-B J(z0)|| <= 3.9518893205e-9,
    Lipschitz constant < 3.9518906722e-9,
    self-map radius bound < 3.1174915200e-39,
    enclosing ball radius = 2^-100 ~ 7.8886090522e-31.

All deciding inequalities use the exact fractions in exact_certificate.json,
not these displayed decimals. A derivative/Hessian argument and Banach's
contraction theorem prove existence and local uniqueness. See PROOF.md.

**The stored dyadic center is not the exact solution.** Exact constants are
specified by the algebraic root certificate; no radical formula or exact
algebraic-field runtime is supplied. Modular checks of the center only check
the evaluator, not an exact modular Fourier circuit. The certificate and
its checker were authored in this run; independent human/formal proof review
has not occurred.

## Growing-size experiment, including unsuccessful searches

Every fit used the whole normalized Fourier target, not a few training
columns. No sparsity or favorable input distribution was assumed. Eight
completed search records are retained:

| N | Stages | Layout | Completed iterations | Relative Frobenius error at best saved point |
|---:|---:|---|---:|---:|
| 4 | 1 | random, seed 18001 | 11 | 1.1307e-16 |
| 8 | 2 | random, seed 18001 | 18 | 6.9767e-15 |
| 16 | 3 | random, seed 18001 | 200 | 0.2006505 |
| 16 | 4 | random, seed 18001 | 48 | 3.4933e-14, followed by exact local certification |
| 32 | 4 | random, seed 18001 | 160 | 0.5043205 |
| 32 | 4 | cyclic bit-slot orders | 240 | 0.4960762 |
| 32 | 4 | affine/bit-reversal orders | 240 | 0.4645340 |
| 32 | 8 | random, seed 18001 | 160 | 0.1767756 |

The 4- and 8-point numerical fits were NOT formally certified in this round.
Only the 16-point four-stage candidate received the exact interval proof.
The N32 results are bounded local-search outcomes, not topology
impossibility theorems, certified optimal errors, or a proof that exact
solutions cannot exist. The affine/bit-reversal run's maximum coefficient
grew to about 468.4; the random eight-stage run retained a spectral error
near 1. Both limitations are visible in the raw records.

An initial search pass hit a singular normal-equation solve. The guarded
rerun increased the minimum damping and handled that exception. Its failed
log remains in evidence; it is not counted as a successful search. Two
interval test-harness scalar-shape bugs were also corrected, with their
failed logs retained. The final full checks and clean replay use the fixed
sources.

## Costs and what has not become faster

A supplied stage uses exactly 5N multiplications and 8N-4 additions or
subtractions in scan_executor.py, including both endpoint gains and the
free diagonal. It uses O(N) working storage; stage coefficients/routes
occupy O(tN). All gathers/scatters happen in the evaluator.

At N16 with four stages:

| Evaluator | Multiplications | Additions/subtractions |
|---|---:|---:|
| R18 with supplied exact root coefficients | 320 | 496 |
| Straightforward normalized radix-two reference, literal upper count | 48 | 64 |

The previous R17 approximate circuit used 297 multiplications and 311
additions/subtractions. R18 is **not** a cheaper evaluation of that matrix;
it is a different construction with an exact finite existence certificate.
No wall-clock FFT benchmark was performed. Synthesis and root certification
are expensive preparation and were not hidden in a warm-plan speedup.

The density of a stage is not an obstruction to its linear application, but
neither density nor a small number of factors at one N proves a fast
Fourier family. The successful chart has an invertible square Jacobian and
thus also represents a neighborhood of general matrices. That is evidence
of finite expressiveness, not a special Fourier scaling law.

For a uniform family, the required accounting remains

    T(N) = coefficient/route construction cost + O(t(N) N).

A sub-N-log-N result needs t(N)=o(log N) and correspondingly cheap charged
construction. The actual search forms an N-by-N dense target and dense
Jacobians, so it does not furnish that generator. Arbitrary precision,
output accuracy, and stability need separate control in a bit/numerical
model. No conditional exponent is promoted from this finite certificate.

## Fresh checks

| Check | Completed coverage |
|---|---:|
| Exact random supplied-coefficient networks | 90 |
| Networks containing zero coefficients, included above | 45 |
| Vector comparisons with separately formulated dense evaluation | 666 |
| Basis vectors included in those comparisons | 396 |
| Complete arithmetic-count checks | 666 |
| Saved-center basis comparisons over three finite fields (NOT Fourier tests) | 48 |
| Scalar interval endpoint product/sum comparisons | 1,920 |
| Matrix interval product entry comparisons | 1,036 |
| Complex norm bounds on the same scalar cases | 1,920 |
| Exact square-root endpoint checks | 200 |
| Fourier-interval unitarity entry containments | 1,360 |
| Exact dual-number derivative entries | 232 |
| Deliberately malformed executor inputs rejected | 6 |
| Full certificate parameter/preconditioner corruptions rejected | 2 |

Counts overlap: basis vectors and norm controls are not extra independent
experiments. Gaussian-rational and finite-field executor checks are exact.
The exact root proof is the contraction certificate, not a count of these
tests. The changed-center and zero-preconditioner controls correctly fail
its strict inequalities. A clean-extraction replay is recorded separately.
No old research executable was imported into the new validator, and no
remote Sheet or GitHub file was changed.

## Attribution and next gate

Classical skew-prefix/Green identities, diagonal-ended factorizations,
nonlinear least-squares synthesis, and root isolation remain attributed.
The existing C09 seed remains an earlier project result. The external
shea256 exact-DFT work was inspected as a comparison, not imported; its
reported all-length exponent is not this project's result. The external
proof was not rebuilt. See SOURCE_LEDGER.md for precise read scope.

The retained advance is a reproducible exact finite certificate for this
particular four-stage, fixed-holonomy two-scan model. It is not established
worldwide-new mathematics. The missing gate remains a genuinely
Fourier-specific, exact growing-size construction with charged sublogarithmic
stage count and coefficient generation. No further decimal fitting is
substituted for that requirement.
