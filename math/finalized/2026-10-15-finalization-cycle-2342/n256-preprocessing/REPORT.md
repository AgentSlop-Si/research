# N256: branch-complete rank preprocessing and exact endpoint elimination

Date: 2026-10-15 UTC. Tasks: N256-FULL-MODEL-20261011 and N256-SOLVER-SATURATION-20261011.

## Disposition

**Equivalent formulation simplifications only. Fourier feasibility remains OPEN.**

Two safe changes are proved below:

1. Replace the union of normalized kernel charts for the accepted mask64 rank gate by one rank-factorization system. It covers every rank stratum without choosing a kernel chart and lowers the maximum raw-generator degree from five to four.
2. Remove the complete model's first-stage scanning states, whose inputs are fixed basis columns. This removes 130,560 variables and the same number of equations while preserving degree at most two, support at most four, and every solution branch.

These are standard algebraic preprocessing principles applied to the pinned model. They do not constitute a new Fourier obstruction, an admissible root, a novelty claim, a solver-runtime result, or an FFT operation-count improvement. No solver, imported program, archived test suite, or network request was run.

## 1. Pinned source and exact scope

The parent supplied repository snapshot AgentSlop-Si/research, main e5c9c53f7d34e8d858e781d2d5321393aec7e85c. This report directly checked recovered local source bytes; it does not independently assert that a new remote commit exists.

Copied source files and their independently recomputed SHA256 values:

- `sources/PROOF_CERTIFICATE.md`: 9e3936a8c45f0d912beac775e73f57a66e3ac638fe1ceca04be3c9b4492ab490.
- `sources/AFFINE_LAYOUT.json`: 77c5c0fcdcfa850dac44dd34dbe3188539aa9cb143f22978b86127add76b8e45.
- `sources/RESEARCH.md`: 34b357277f25adcff11d212c54b624baabb9e070ce86adc9f60e6fbb2e85d482.

The original recovered copies are under `following_twentyfive_breadth_1351/packet/sources/`, with the hash-prefixed filenames. Live workbook anchor supplied by the parent: 1BHaGJHkXxf_UfZdyTKF2zrWNFzIP4IvhaqFMj-83BjU, overview row 139 and Incoming queue row 33. This worker did not edit that workbook.

Work over a field K containing the target coefficients, specifically Q(zeta_256) or C for the complex problem. Let U_ij = zeta_256^(ij)/16, and let the permutation convention be (P_s x)_i = x_[p_s(i)]. Keep the three maps encoded by `affine_shuffle_columns` unchanged. The archived Toffoli list is unused.

Every stage has the exact shared separated generators

    S_ij = a_i b_j  if i > j;
           d_i      if i = j;
           c_i e_j  if i < j.

Do not substitute a broader cut-rank or transfer-generator quasiseparable class. The target is

    S4 P3 S3 P2 S2 P1 S1 = U.

For the isolated outer gate put G = P1 S1 U^(-1) S4 P3 and let B = G[I,J] be the archived 128-by-128 mask64 block with rank allowance 16. The results below hold uniformly for any fixed I,J of those sizes, hence apply without modifying those archived selectors. This report does not materialize a new selector list or claim to instantiate all solver coefficients.

## 2. Chart-free rank-factorization lemma

**Lemma.** For B in K^(128 by 128), the following are equivalent:

(a) rank(B) <= 16.

(b) There exist C in K^(128 by 16), D in K^(16 by 128) with B = C D.

(c) At least one of the source's normalized 112-column kernel charts is feasible.

**Proof.** If B = CD, its column space is contained in the span of the 16 columns of C, so rank(B) <= 16. Conversely let rank(B) = r <= 16. Select a basis of r columns of B, arrange them in C_r, and express every column of B in that basis to form D_r. Then B = C_r D_r. Append 16-r zero columns to C_r and 16-r zero rows to D_r. This gives the required C,D, including B=0. The equivalence of (a) and (c) is the source's kernel-basis normalization argument: nullity at least 112 supplies an independent 112-column kernel matrix, and one nonsingular row minor can be normalized to identity. No kernel chart is singled out in (b). QED.

In particular, **do not impose rank(C)=rank(D)=16, normalize a preferred factor minor, or add a nonzero factor-minor guard.** Such additions would lose lower-rank solutions or chart branches. C,D are allowed to be zero or rank deficient.

The direct equations are

    B_ij - sum_(ell=0)^15 C_iell D_ellj = 0.

There are 4,096 auxiliary variables and 16,384 equations. Each B entry has degree at most four in raw outer-stage generators because it is bilinear in entries of S1 and S4, and each stage entry has degree at most two. Thus the equations have maximum total degree four. If B is supplied as a matrix-entry variable, these factorization equations themselves are quadratic, but the equations defining B must still be counted.

Compared with one normalized kernel chart, this uses 2,304 more auxiliary variables and 2,048 more equations, but represents the entire existential union at once. It is not a proof of a runtime advantage; the direct B polynomials are dense, and rank factorization introduces its own nonunique witnesses.

### Required outer guards

The isolated gate still requires det(S1) and det(S4) to be nonzero. Retain the accepted reciprocal determinant-transfer equations, including the reciprocal variables. Removing their reciprocals or merely saturating and then projecting a closure would not impose the same open condition.

Under the accepted source convention, the two guarded stages add 1,030 auxiliary variables and equations, of degree at most three. Counting all 2,560 raw outer generator coordinates, the direct one-gate rank-factor system therefore has:

- 7,686 unknowns = 2,560 + 4,096 + 1,030.
- 17,414 equations = 16,384 + 1,030.
- Maximum total degree four.

These counts include the eight unused outer generator coordinates, exactly as the raw-source convention does. They exclude other mask gates and every middle-stage compatibility equation. The guard count is inherited from the accepted saturation source; the independent reviewer checked that convention against its nested source document.

The rank-factorization equivalence is stated over fields. It must not be promoted to an equivalence for arbitrary commutative rings without additional hypotheses about rank and module factorizations. The determinant guards remain unit conditions if working over rings.

## 3. Optional quadratic core for the single rank gate

This section makes the raw-generator degree claim explicit without introducing dense 256-by-256 stage-entry matrices. It is a mathematical template, not an executed or benchmarked solver.

Write M = U^(-1), enumerate J as j_0,...,j_127, and let q_v = p3^(-1)(j_v). Introduce T in K^(256 by 128) by

    T_iv = M_iq_v d4_q_v
           + b4_q_v sum_(k>q_v) M_ik a4_k
           + e4_q_v sum_(k<q_v) M_ik c4_k.

This is exactly T = U^(-1) S4 P3[:,J]. These 32,768 equations are degree at most two; each has at most 257 monomial terms including -T_iv.

For each column v introduce the first-stage scan states

    L_0v = 0, R_255,v = 0 (literal constants),
    L_(i+1),v - L_iv - b1_i T_iv = 0,
    R_iv - R_(i+1),v - e1_(i+1) T_(i+1),v = 0.

There are 65,280 free scan-state variables and the same number of recurrence equations. For each i in I set h=p1(i) and impose

    d1_h T_hv + a1_h L_hv + c1_h R_hv
      - sum_(ell=0)^15 C_iell D_ellv = 0.

The 16,384 final equations have degree two and support at most 19. The unique scan recurrences prove their left side is exactly B_iv minus (CD)_iv, so projection to the raw generators is precisely the same rank gate as Section 2, including every lower-rank branch.

Before determinant guards the counts are:

- 104,704 unknowns = 2,560 raw + 32,768 T + 65,280 states + 4,096 factors.
- 114,432 equations = 32,768 T definitions + 65,280 recurrences + 16,384 final equations.
- Maximum degree two, support at most 257.

Adding the accepted 1,030-variable cubic determinant guard construction gives 105,734 unknowns and 115,462 equations, **maximum degree three**, not two. This guarded single-gate system must not be advertised as the complete quadratic Fourier model. It is also not sparse to the source's support-four standard.

## 4. Exact first-stage elimination in the complete quadratic model

The complete source system fixes x^(1,j)=e_j. Consequently its first-stage running sums are not free nonlinear unknowns:

    L_i^(1,j) = b_j^(1) if j < i, otherwise 0;
    R_i^(1,j) = e_j^(1) if j > i, otherwise 0.

Substitute these values and remove every first-stage sum variable and its recurrence equation. The stage-1 output/coupling becomes simply

    x_i^(2,j) = S1_[p1(i),j],

whose right side is one raw generator d, one product ab, or one product ce. Keep x^(2,j) as an intermediate variable; eliminating it too would generally raise later equations to degree three.

**Proof of equivalence.** Every original solution obeys the displayed formulas by its unique triangular prefix/suffix recurrences, so it projects to a reduced solution. Conversely every reduced solution extends uniquely by those formulas to a solution of all removed recurrences and original first-stage output equations. No division, pivot choice, nonzero generator, genericity condition, or rank chart is used. The remaining equations are unchanged. QED.

For N=256 the eliminated count is 2N(N-1)=130,560. The reduced complete model has:

- 593,408 raw unknowns = 723,968 - 130,560.
- 653,824 equations = 784,384 - 130,560.
- Maximum degree two and support at most four.

The counts continue to include all 5,120 raw generator coordinates, including the original 16 unused coordinates. The reduced model remains exactly equivalent to all 65,536 Fourier entries, and full equality to invertible U still forces all four stages invertible. It therefore needs no added determinant saturation, exactly as in the accepted full-model source.

## 5. Precise unresolved boundary

Neither reduction supplies values of the 5,120 full-model generators, proves the full ideal inconsistent, or upgrades a synthetic positive control to a Fourier witness.

A one-gate rank-factor witness, even with both outer determinants nonzero, still leaves the following exact middle problem:

    S3 P2 S2 = P3^(-1) S4^(-1) U S1^(-1) P1^(-1).

Here S2,S3 must have the same shared separated-generator form. Satisfying further masks does not remove that obligation. Final acceptance still needs an exact root of the complete Fourier model or an infeasibility certificate covering all allowed generators/branches. A modular witness alone would not establish a complex solution, and a rejection of a saved parameter point is not an exclusion of all points.

Recommended next mathematical object: an exact middle-factor compatibility criterion retaining zero-generator/reset branches, or a characteristic-zero infeasibility certificate for the full reduced system. No such criterion or certificate was obtained in this bounded read-only pass. The prior pivot checks and Phase52 local path-isolation result were not repeated or broadened.
