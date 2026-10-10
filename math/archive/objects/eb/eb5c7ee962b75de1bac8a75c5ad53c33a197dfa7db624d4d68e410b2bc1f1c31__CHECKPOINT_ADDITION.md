# Checkpoint addition: three archives received at 17:17 UTC

9 October 2026. Append these results to the existing master through its 16:46 determinant checkpoint. Preserve prior full residual systems, exception coverage and the distinct exact/approximate models.

## Current answer

The new materials do not establish an unrestricted, fully charged exact all-output transform below N log N. They give a genuine characteristic-zero slice exclusion in the fixed F8 search, stronger restricted approximation obstructions, complete Weyl certification tools, and an all-integer-length randomized approximate lift. An independently specified rational-Taylor variant closes the source's Bessel coefficient-preparation gap at the arithmetic level and supplies a conditional precision ledger.

## Exact F8 structural chart

- The new 11-by-9 multi-column gate has rank at most eight for the intended invertible globally separated inverse-stage/final-stage factorization. The source's standalone theorem needs the nonzero-column/invertibility hypothesis. If the fourth output multiplier is zero, invertibility forces the projected four-row basis to have rank at most two, so its cofactor vector is zero; no new nonzero multiplier guard is needed.
- On `h0 Delta T != 0`, an exactly reconstructed 250-term degree-eight minor is `Dhat=-DB DH`, with nine-term quadratic DB and 105-term sextic DH. All 924 exported cyclotomic coefficient vectors match.
- `Res_h6(W,Dhat)` at `h0=1,h1=h2=0` reduces to 6 modulo `(17,zeta8-9)`. This nonzero exact resultant proves the specified regular complex slice has no factorization. It does not exclude other base points or denominator branches.
- The nonzero 37-term and 476-term eliminated resultants constrain the base to a proper hypersurface union. The necessary four-structural-variable locus has dimension at most two, not proven empty.
- A new exact refinement proves the base where W is identically zero in h6 has at most 12 points. A degree-six elimination resultant and a fixed nonzero quadratic leading coefficient certify this. Its free-h6 stratum has dimension at most one; the overall dimension bound remains two.
- Independent GF(17) enumeration reproduces 4,596 candidates and ranks 9/8/7/6 with counts 3,266/1,203/125/2. Another 630 invertible exact positive controls pass, including zero-column multipliers and zero diagonal entries.

The gate/resultants are necessary additions, not replacements for the complete Fourier equations. Keep the old saturation/corner conditions, all excluded branches and the full separated-generator lift. Report and scripts: `triple_audit/`.

## Green Phases19 and20

- Full Weyl duality `MZ=DM`, `MD=Z^-1M` identifies the scalar Fourier family at every integer length; one scalar calibration gives F. The sharp Frobenius residual gap is `2 sin(pi/N)`. Small raw residuals at increasing N do not imply fixed accuracy.
- A fixed linear finite-field oracle can be checked in `1+3h` calls. If its stacked residual rank is rho, independent uniform tests pass with exact probability `p^(-h rho)`. This is not a linearity test, a characteristic-zero proof, or a cheaper evaluator of the candidate.
- Projective root/histogram tests are necessary, not sufficient. Sylvester Hadamards pass every pair histogram and fail Fourier equivalence. The complete anchored-grid criterion extends to arbitrary N; the independent implementation uses a gcd-unit pivot, while the source implementation is dyadic.
- A stronger conditioning-free inverse-support bound is proved: one inverse row of support s implies `||M-F||_2>=sqrt(1-s/N)`. Pure inverse products with support bound s^t therefore have error at least `sqrt(max(0,1-s^t/N))`. Sums do not inherit inverse sparsity.
- A stronger common-frame stationary bound is proved: rank commutator at most r<N implies error at least `cos((2 floor(r/2)+1)pi/(2N))`. For t stages of q stationary path Green terms, r<=2qt, so the floor tends to one when qt=o(N). Arbitrary masks and independent path permutations require separate treatment.
- Newly supplied nested Phase19 independently verifies fixed-middle-monomial signatures, the banded inverse one-norm bound `(b/a^2)[1+2w(b/a)^2]`, resulting gain/conditioning budgets, and the one-Harper-middle-monomial exclusion. Call/stage counts do not prove an unrestricted scalar-operation lower bound for shared computation.
- The real-core and one-complex-mask axis-count restrictions are correct under their distinct assumptions. Dense positive controls do not supply a fast transform.

Reports: `phase19_audit/`, `phase20_audit/`. Exact source-family reconstructions at N=8,16,32 match. Larger source experiments are preserved as source-reported and were not rerun.

## Exact bridge and phase-aware Green extension

- For fixed a, beta_h=beta_0+hK gives M orthogonal block projectors P_h/M whose sum is I. Averaging the complete row bank therefore gives exactly F. Fewer than M rank-K row sketches cannot determine every arbitrary input from that linear transcript alone, even with nonlinear decoding. The exact/adaptive/randomized scope is made explicit in the bridge report.
- The straightforward complete bank costs O(NM+N log K); at M=Theta(log N) this is Theta(N log N). Shared local analysis gives the ordinary N log M plus N log K factorization scale. No universal shared-evaluator lower bound follows from these schedules.
- The exact near-grid residual matrix has Vandermonde rank N/gcd(N,Q), with Q the dyadic lift length. An exact separated correction needs at least that many terms; at odd N its rank is N. Completing the beta bank for each short approximate term computes the truncated center exactly without removing its bias. Different nonseparable corrections remain outside this obstruction.
- A new independently reviewed phase-aware displacement obstruction permits products of sums of c D^a P B^-1 P^-1 D^b, with constant-coefficient path denominators, integer linear phases and independent affine conjugations P. Common-frame displacement costs at most rho=2 per inverse; affine-conjugated paths cost at most rho=4.
- For b expanded branches and d distinct total phases, exact Fourier equality requires `N<=d(1+sum r_branch)<=d(1+rho t b)<=b+rho t b^2`. Fixed summand bound q>=2 therefore forces t=Omega(log N), without conditioning assumptions. One branch forces t>=(N-1)/rho. A common phase at even N improves the exact rank target to N and admits the same cosine spectral-error bound.
- Arbitrary diagonals, arbitrary path permutations, independent left/right affine factors and bare affine-multiplier wiring are outside that grammar. The reviewer gives a nearly full-rank bare-affine counterexample. This is an architectural stage bound, not an unrestricted scalar-operation lower bound.

Reports: `astra_exact_bridge/` and independent `twisted_bound_review/REVIEW.md`.

## All-length approximation and charged variant

- The v10 dyadic near-grid Bessel/Chebyshev lift is algebraically valid. Using the same state for all rank terms preserves per-output variance `(M/N)(1+tau_R)^2 ||x||_2^2`, without an R multiplier. Its deterministic bias is at most `tau_R ||x||_2` per coordinate.
- This is a fixed-input randomized simultaneous-output approximation, not arbitrary exact recovery. It does not automatically preserve the previous sparse-spectrum exact promise after input weighting.
- The uploaded prototype uses Theta(RN) Chebyshev storage, uncharged/uncertified special-function evaluations and floating grid indices. Naive forward Bessel recurrence is an unstable repair. N=1 needs its direct case. The endpoint failure target N^(-a) is vacuous at a=0 unless multiplied by a fixed constant below one.
- The independent rational-Taylor variant generates a rational rho approximating pi via finite Machin sums, with certified error eta, and tail `eta+|rho|^R/R!`. Streamed powers/factorial recurrences and exact integer indices charge coefficient generation in O(RN+log(1/eta)) arithmetic work for a fixed number of random rows, with O(N) arithmetic storage.
- Under the inherited specified dyadic row/root contract, its deterministic rounding ledger covers weights, coefficients, row error, cancellation, sum, normalizer and robust classification/radii. It is conditional implementation mathematics, not certification of the uploaded binary64 code. Growing rational/floating bit costs and exponent range remain charged.

Reports: `lift_audit/`, `taylor_extension/`. Independent full-state covariance controls through Q=32 agree numerically; 6,240 exact-rational finite-precision recurrence checks pass. Numerical controls corroborate proofs without certifying a production evaluator.

## Provenance and reproduction

The batch adds 77 new byte contents versus the declared source union through 16:46: 73 text/data files, three bytecode files and one new nested Phase19 archive. There are 656 recursive member occurrences, 472 unique hashes and 799 passing embedded checksum entries. Full sources, Library identities, hashes, fresh independent scripts and portable rerun records are preserved. Uploaded code and bytecode were never executed.

Main synthesis: `THREE_LATEST_AUDIT.md`. Source inventory: `SOURCE_PROVENANCE.md` and JSON records. No publication-priority or chat-only completeness claim is made.
