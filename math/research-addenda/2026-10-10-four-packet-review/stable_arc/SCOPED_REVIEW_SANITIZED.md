# Sanitized publication copy

Original review SHA-256: afb48aceae5533b7ec39727a40438662bc5a2464e29c14a320f7b3885be1b49d. Private source identifiers are omitted. Mathematical text is otherwise unchanged. Original review-date statements and historical execution/provenance claims below refer to that original review; they are not fresh claims about this publication assembly. Use the addendum README and replay script for the self-contained mathematical replay and its explicit archive/history exclusions.

# Stable arc signature theorem independent review

## Verdict

The packet's finite certificates A1 and A2, exact obstruction A3, uniform spectral gap A4, and polynomial accuracy consequence A5 are mathematically supported under the explicitly stated model. No change to the numerical constant in A4 is needed. This is a restricted one layer approximation obstruction for the unitary complex DFT. It does not settle a multilayer architecture or imply an FFT operation lower bound.

Retain the existing Phase43 / M-ROUTED-FIELD attribution and routing. The inherited exact arc rank mechanism and common endpoint bound must not be relabeled as new. This review independently validates the supplied argument; it does not certify historical novelty, priority, or publishability, and does not independently reconstruct those earlier project files.

Two harmless precision improvements are recommended for the proof: explicitly define cyclic arc endpoint conventions, and write the Rayleigh identity with conjugated coefficient variables. Both are supplied below. Explicitly stating q is a positive integer would also remove an unnecessary edge case.

## Reviewed sources and execution boundary

The actual Library items were materialized read only:

- Report: [private source identifier omitted], version 0, THEOREM(20261010-233055).md, 10,985 bytes.
- Archive: [private source identifier omitted], version 0, FFT_STABLE_ARC_SIGNATURE_THEORY_2026-10-11.zip, 13,294 bytes.

The report is byte identical to the archive's fft_stable_arc_20261011/THEOREM.md. The archive README, SOURCE_AUDIT.md, theorem, stored results, and verify.py were inspected as data. No uploaded program was executed or imported. All controls in this review were freshly written in fresh_controls.py. Full source hashes and local provenance are recorded in source_manifest.json and SHA256SUMS.txt.

The source labels its research note October 11, 2026. That source date is preserved, not independently inferred from its upload time. No external priority search was undertaken in this review.

## Exact model and dependencies

Let N >= 2 and q >= 1 be integers, n = q+1, and K = n^q. The target is exactly

    U_N[k,j] = N^(-1/2) exp(-2 pi i k j / N).

The field is C. The norm is the unnormalized induced Euclidean operator norm, equivalently the largest singular value. U_N is unitary and has norm one.

Each W_l is a weighted permutation supported on one directed Hamiltonian cycle on all N vertices. Every edge weight is nonzero and its cycle product h_l differs from one. Thus I-W_l is invertible. Each branch has its own invertible complex monomial L_l and R_l, and

    M = sum_l L_l (I-W_l)^(-1) R_l.

No positivity, common endpoint permutation, unit magnitude, bounded coefficient, conditioning, or affine cycle assumption is used. The endpoint diagonals of the APPROXIMANT may be arbitrarily nonunitary. This does not grant an arbitrary nonunitary change to the TARGET or the norm.

A1 and A2 use n distinct rows, with consecutiveness needed for the Fourier independence/density consequences. For A1 as stated N >= n. If n > N, A3's inequality is automatic and no n-row construction is required. All row indices can be interpreted cyclically when the consecutive block wraps around N.

## Independent proof of the arc partition

Fix one branch and list its cycle as v_0,...,v_(N-1), with W e_(v_t) = w_t e_(v_(t+1)). Put beta_0=1, beta_a=product_(t<a) w_t, and h=product_t w_t. Since W^N=hI,

    G = (I+W+...+W^(N-1))/(1-h),
    G[v_a,v_b] = (beta_a/beta_b) h^[a<b] /(1-h).

Here [a<b] is zero or one. This formula follows from the unique directed path of length 0,...,N-1 from source v_b to destination v_a. All beta_a and h are nonzero.

For the selected output rows, the branch's left permutation selects n distinct cycle positions. Sort them as a_1<...<a_n. Partition source positions into the n arcs

    (a_(t-1), a_t]  for t=2,...,n,
    (a_n, N-1] union [0,a_1]  for the wrapping arc.

For each nonwrapping arc, all indicators [a_i<b] are fixed. On the wrapping arc, sources above a_n give the all-one indicator and sources at or below a_1 give the all-zero indicator. Those two vectors differ by the common nonzero scalar h, so they define the same projective direction.

The factors beta_a/(1-h) and the selected left diagonal entries depend only on the output coordinate. The factor beta_b^(-1) and the right diagonal entry depend only on the input column. Therefore each arc determines one projective direction on the selected n rows, including the wrapping arc. Pulling these arc labels back through this branch's right permutation produces at most n labels on target columns, independent of all numerical weights and diagonal values.

For q independently dressed branches, the joint label takes at most n^q=K values. On each class C, every branch has rank at most one, hence M[R,C] has rank at most q=n-1. This argument uses independent branch endpoint permutations directly; no common gauge reduction is assumed.

## Independent proof of the finite certificates

Write E=M-U. For each class C, a rank at most n-1 matrix cannot approximate U[R,C] more closely in spectral norm than its nth singular value. Restricting rows and columns is contractive in operator norm, so

    ||E||_2 >= ||E[R,C]||_2 >= sigma_n(U[R,C]).

When |C|<n, interpret the nth singular value as zero, equivalently use the smallest eigenvalue of the n by n Gram matrix. This proves A1.

For Frobenius norm the squared minimum rank-(n-1) residual is also sigma_n(U[R,C])^2. The classes are disjoint and exhaustive, so

    sum_C sigma_n(U[R,C])^2 <= ||E[R,:]||_F^2
                                  <= n ||E[R,:]||_2^2
                                  <= n ||E||_2^2.

This proves A2, including its factor 1/n. A2 need not be weaker than A1: the fresh N=108, q=2 control gives A1 about 0.423275 and A2 about 0.461534. Neither bound follows by summing spectral residuals directly; the intervening Frobenius argument is necessary.

For n consecutive Fourier rows starting at r_0, the selected column j equals a nonzero scalar times (1,z_j,...,z_j^(n-1)), where z_j=exp(-2 pi i j/N). The n by n determinant on any n distinct columns is a nonzero Vandermonde product. Thus an exact representation has at most q columns in every class, yielding N <= qK, which is A3. This full spark statement is for consecutive rows, not all Fourier minors at composite N. For example, at N=4 rows {0,2} and columns {0,2} give a rank-one block.

## Independent proof of the density lemma and A4

Suppose |C|=L >= alpha N, 0<alpha<=1, and N>=4n/alpha. Sort C as c_1<...<c_L and put s=floor(L/(2n)). Then

    s >= L/(4n) >= alpha N/(4n),
    1 <= s <= N/(2n).

The floor bound is valid because L/(2n)>=2. Choose n groups consisting of selected ranks

    1,...,s; 2s+1,...,3s; ...; 2(n-1)s+1,...,(2n-1)s.

Between adjacent groups there are s unselected members of C. After the last group there are at least s unselected members of C because L>=2ns. Hence any two points from distinct selected groups have distance at least s in BOTH cyclic grid directions. More precisely the constructed minimum distance is at least s+1, but the weaker s suffices. This last tail is what protects the gap across index N-1 to index 0.

For roots z_1,...,z_n chosen one per group, all pairwise chord distances are at least

    delta = 2 sin(pi s/N) >= 4s/N >= alpha/n.

The sine bound holds because 0<=s/N<=1/2. Let p(z)=sum_(r=0)^(n-1) a_r z^r with sum |a_r|^2=1. Continuous Parseval implies sup_(|z|=1) |p(z)|>=1. In the Lagrange formula, every numerator product has magnitude at most 2^(n-1), and every denominator product at least delta^(n-1). Therefore

    1 <= sup |p| <= (2/delta)^(n-1) sum_j |p(z_j)|
                   <= (2/delta)^(n-1) sqrt(n) (sum_j |p(z_j)|^2)^(1/2).

This holds for every one of the s^n choices of nodes. Averaging its squared consequence gives

    (1/s) sum_(j in selected groups) |p(z_j)|^2
        >= (delta/2)^(2n-2)/n.

Consequently

    (1/N) sum_(j in C) |p(z_j)|^2
        >= (s/N) (delta/2)^(2n-2)/n
        >= alpha^(2n-1)/(2n)^(2n).

For complete conjugation precision, if a is any unit vector used in the Gram Rayleigh quotient, then

    a* U[R,C] U[R,C]* a
        = (1/N) sum_(j in C) |sum_r conjugate(a_r) z_j^r|^2.

The factor z_j^r_0 has modulus one and disappears. Conjugation maps the unit coefficient sphere bijectively to itself. Thus the lower polynomial estimate applies to every Gram Rayleigh vector, proving

    sigma_n(U[R,C]) >= alpha^(n-1/2)/(2n)^n.

This is exactly the packet's density lemma. Its wording that the same coefficient vector is 'precisely' the Rayleigh quotient should be read with this harmless conjugation change of variables.

The largest signature class has at least N/K points. Set alpha=1/K. The required density hypothesis is N>=4nK, and A1 now gives

    ||M-U_N||_2 >= c_q = 1 / ((2n)^n K^(n-1/2)).

All constants agree with A4. No condition number of L_l, R_l, or G_l occurs. The argument survives arbitrarily ill-conditioned approximants because its intermediate statement is an exact rank constraint.

## Explicit asymptotic inversion for A5

Use natural logarithms. Direct algebra gives

    log(1/c_q) = (q+1)log 2 + (q^2 + 3q/2 + 1)log(q+1)
               <= 6q^2 log(q+2)   for q>=1.

Let t=log N and fix alpha>0. Suppose

    q <= sqrt(alpha/12) sqrt(t/log t).

For sufficiently large N depending on alpha, q+2<=t, so log(1/c_q)<=alpha t/2. The size condition also holds, because

    log(4nK) = log 4 + (q+1)log(q+1) = O_alpha(sqrt(t log t)) = o(t).

It follows that c_q >= N^(-alpha/2)>N^(-alpha), contradicting the proposed error at most N^(-alpha). This proves A5 with an explicit permissible asymptotic constant. The argument includes bounded q and does not require q(N) to be monotone. If q is already above this threshold there is nothing to prove. Failure of N>=4nK at larger q cannot invalidate the corollary.

## Normalization and field boundary controls

### Scalar target scaling

The model is a cone under every nonzero complex scalar. Accordingly, for fixed N and q,

    inf_M ||M-tU_N||_2 = |t| inf_M ||M-U_N||_2  for t != 0.

The correctly rescaled lower bound is |t|c_q. A normalization with t_N tending to zero cannot retain the same absolute constant. For example, take a cyclic permutation P, G=(I-P/2)^(-1), t_N>0 tending to zero, and M_N=t_N^2 G. These are valid one-branch matrices with invertible endpoint scalings, while

    ||M_N-t_N U_N||_2 <= 2t_N^2+t_N -> 0.

For the unnormalized Fourier matrix F_N=sqrt(N)U_N, the corresponding absolute lower bound is sqrt(N)c_q. For F_N/N it is c_q/sqrt(N). Relative operator error against a scalar multiple has the original constant.

### Nonunitary target scaling even at target norm one

A target A U_N B with fixed invertible monomial A and B has the valid bound

    ||M-AU_NB||_2 >= sigma_min(A) sigma_min(B) c_q,

because A^(-1) M B^(-1) remains in the same grammar. Unit-modulus monomial target changes preserve the original constant. Uncontrolled nonunitary target changes do not.

Here is an explicit counterexample even when the target norm is fixed at one. Fix N>=16 and q=1. Let G=(I-P/2)^(-1), whose entries are all nonzero. Choose a right diagonal B_jj=U_N[0,j]/G[0,j] and set H=GB. The first row of H equals the first row of U_N exactly. Put

    D_epsilon = diag(1,epsilon,...,epsilon),
    delta = epsilon/(1+||H[1:,:]||_2),
    M_epsilon = diag(1,delta,...,delta) H.

All endpoint diagonals are invertible for epsilon>0. The target T_epsilon=D_epsilon U_N has norm one, yet

    ||M_epsilon-T_epsilon||_2 <= 2 epsilon.

Thus no target-normalization-independent gap follows even from requiring target operator norm one. At N=16 and epsilon=10^(-6), the fresh numeric error is about 1.4267023e-6, far below c_1 about 0.02209709. This is a counterexample to an extension beyond the packet, not to the packet's fixed unitary target.

### Field and norm routing

The arc rank identity and Vandermonde exact obstruction are algebraic. They extend to a field containing a primitive Nth root with nonzero edge weights, h_l!=1, and invertible endpoint diagonals. A finite field check must use an Nth root of exact order N; an arbitrary Fourier-like root is insufficient. The fresh controls verify exact order explicitly.

The spectral density lemma, chord geometry, Hermitian positivity, and polynomial accuracy corollary here are complex Euclidean statements. They do not become finite-field spectral theorems. Preserve M-ROUTED-FIELD separation: finite-field controls certify the algebraic rank mechanism only. Their Fourier targets are unnormalized, which is harmless for rank and irrelevant to the complex spectral constant.

The same lower bound holds for unnormalized Frobenius norm because it dominates spectral norm. Dividing Frobenius error by sqrt(N) changes the scale and does not preserve a uniform constant. Entrywise average error, restricted-input error, and arbitrary similarity-transformed norms are not covered.

## Fresh controls and source claim checks

All fresh results and deterministic seeds are in fresh_controls.json. They are supporting finite checks, not substitutes for the preceding proof.

1. Three exact modular independent-endpoint controls used direct path walks to compute Green entries. At N=32, q=2 over F_97, a three-column witness has Green rank 2 and Fourier rank 3. At N=64 and N=256, q=3 over F_257, four-column witnesses have Green rank 3 and Fourier rank 4. Every class and every individual branch restricted to it was checked exactly; respectively 6, 21, and 45 classes were tested.
2. Ten complex controls for q=1,2,3,4 used direct linear solves for I-W, separately permuted/scaled endpoints, and cyclically consecutive target rows that cross index zero. All rank tails were within floating-point residual tolerance; the maximum relative forbidden singular value was below 2e-16. A1 and A2 were respected both by the actual Green sum and a relaxed classwise truncated-SVD approximation, which separately exercises the norm conversion.
3. Exhaustive integer spacing tests checked 63,595 subset/group-count configurations for N=4,...,14 and n=2,3,4 where L>=2n. Every circular gap passed, with minimum slack one grid step above the proof's bound.
4. 105 density controls included clustered, wrapping, spaced, and random subsets. They include the tight size-hypothesis cases N=108,n=3,L=12 and N=1024,n=4,L=16. Every numerical singular value exceeded the proved lower bound.
5. Both scalar shrinkage and norm-one nonunitary target counterexamples were checked numerically, supplementing their exact constructions above.

The source's stored 27 numerical cases, 10,381 spacing cases, two graph-only decimal certificates, and two finite-field witnesses were inspected, not rerun. Its two large graph-only examples use common endpoint maps in the supplied code; this is a valid special case and does not independently test that part of the broader endpoint extension. The fresh controls above do use independent endpoints. The source's status line says 'one' finite-field rank check whereas its final body/results contain two; this is a minor stale summary rather than a mathematical defect.

All displayed numerical singular values are floating-point diagnostics, not interval-certified positivity. Exact positivity and the universal constants in this review come from the proof. The exact modular and integer spacing controls use integer arithmetic.

## Certificate computation and unresolved scope

The stated O(q^2 N + K n^3) cost is reasonable for graph preparation, signature assignment, Gram accumulation, and dense numerical eigensolvers. It is O(N) for fixed q. It reads all input column labels and is a certificate cost, not a DFT evaluation cost. Exact positivity or specified-bit error certification requires additional numerical analysis or interval arithmetic; this operation-count expression is not a bit-complexity theorem.

Products of sums such as (G_1+G_2)D(G_3+G_4), more general two-layer independently gauged architectures, AESGR, and noncommuting multilayer networks remain outside this theorem. An intermediate diagonal can mix the endpoint arc directions, so no reuse of the one-layer rank argument for those models is justified. The packet does not close an all-row construction gate, a Weyl-covariance gate, an all-length coefficient schedule, or the cost-accounting requirements for an algorithm.

## Proposed disposition

Accept as a proved restricted-model quantitative obstruction with explicit normalization and field scope. Record the independent endpoint extension, stable gap, and polynomial-precision branch growth as this packet's proposed contribution relative to its stated project baseline, without historical novelty certification. Keep Phase43 and M-ROUTED-FIELD provenance. Do not merge it into a new fusion claim, advance AESGR or products-of-sums gates, or infer a faster FFT or unrestricted FFT lower bound.

The uncommitted Incomingqueue proposal is provided separately in Incomingqueue_proposal.json. No Sheet or GitHub write was performed.
