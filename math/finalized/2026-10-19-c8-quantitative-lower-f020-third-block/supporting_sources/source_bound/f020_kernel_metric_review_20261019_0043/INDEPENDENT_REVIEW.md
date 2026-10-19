# Independent review: F020 actual-family kernel metric obstruction

19 October 2026 UTC. Review of the frozen candidate in `f020_kernel_metric_obstruction_20261019_0038`.

- Author manifest SHA-256: `0021b58bc86300759b5bc0640082525b531220244abdfbce07bfc8bc27cedaaf`.
- Author report SHA-256: `3b0673fbfc3252175ccf5177c481d40535a22cd416205f26468998fe1e3feee2`.

## Verdict

**ACCEPT_SCOPED. No blocking correction.** The actual-family proofs establish:

1. For every odd root order d and every 3 <= b < d, no diagonal similarity of J_b is normal.
2. For every primitive odd-order q of order d >= 5, no nonconstant affine transform of J_4 is similar to a Hermitian matrix, even under an arbitrary nondiagonal similarity.
3. J_d has real simple Chebyshev spectrum and positive-definite Hermitian self-adjointness metrics, but every such metric has nonzero cross-block coupling across every residual cut 2 <= b < d. Its compression equation has a nonzero boundary defect.

These are unlimited-range obstructions to the stated mechanisms, proved from the actual coefficients 1-q^k. They do not prove or disprove the missing ordinary nonisotropy lemma. No characteristic-zero counterexample, uniform ordinary-squarefreeness theorem, automatic all-A extension, owner closure, priority change, census extension, or historical-priority conclusion is supplied. F020 remains open, with F023 its alias, as in the accepted baseline.

The inspected fresh author checker passed all 19 assertions when copied unchanged and replayed in this review's separate directory. Independent fresh controls passed 55 exact/source-integrity assertions. These controls are supplementary transcription checks, not the proof of the unlimited conclusions or a root-order census.

## 1. Actual matrix, branch choice, and missing kernel

The retained accepted author report Section 6 and its accepted independent review define exactly P_(k+1)=X P_k-(1-q^k)P_(k-1), with P_0=1, P_1=X, and w_k the product of the nonzero coefficients. The candidate uses the corresponding symmetric tridiagonal matrix, not either of the different real Jacobi matrices in the node-separation argument.

For primitive q and 1 <= k < d, q^k != 1, and Re(1-q^k)=1-Re(q^k)>0. Thus principal square roots a_k exist, are nonzero, and commute with complex conjugation on this domain. Expanding the tridiagonal determinant proves det(XI-J_b)=P_b. The displayed eigenvector with coordinate P_k(xi)/(a_1...a_k) satisfies every row, including the terminal row because P_b(xi)=0. The independent controls verify this directly for the generic four-vertex symmetric matrix before any q substitution.

An irreducible tridiagonal eigenvector is determined by its first coordinate, which cannot vanish, so each eigenspace has dimension one. Its bilinear self-product is precisely the diagonal Christoffel-Darboux kernel in the baseline. Consecutive P polynomials have no common root by downward recurrence. Hence the accepted diagonal CD identity makes kernel nonvanishing equivalent to P_b'(xi)!=0. Neither ordinary Hermitian positivity nor the generic positive-real-part condition can be substituted for this bilinear assertion.

An arbitrary similarity to a normal matrix, without a separately constructed mechanism, would indeed assume diagonalizability. Here one-dimensional eigenspaces then imply simple spectrum, the missing assertion itself. The candidate correctly restricts its first no-go theorem to diagonal similarities.

## 2. Diagonal-normality obstruction

For an irreducible zero-diagonal tridiagonal T with superdiagonal s_k and subdiagonal t_k, normality first implies |s_1|=|t_1| at the upper-left diagonal entry. Subsequent diagonal entries inductively imply |s_k|=|t_k|. The distance-two entries imply

    s_k conjugate(t_(k+1)) = conjugate(t_k) s_(k+1).

Division by nonzero subdiagonal factors makes s_k/conjugate(t_k) a common unimodular number c. Thus every product s_k t_k=c |t_k|^2 lies on a single complex ray with positive multipliers. This necessity holds for arbitrary dimension; no finite control is doing the inductive work.

The stated converse is also correct: if the products equal c r_k with r_k>0, choose a square root rho of c and target symmetric off-diagonal entries rho sqrt(r_k). Recursively choosing diagonal-similarity ratios to obtain these superdiagonal entries forces the subdiagonal entries to coincide, by invariance of the edge products. The result is rho times a real symmetric matrix, hence normal.

For actual J_b the invariant products are 1-q^k. Their first ratio is (1-q^2)/(1-q)=1+q. A primitive root of odd order d>=3 is nonreal. Consequently this ratio is nonreal and cannot be a positive real number. As soon as b>=3 the first two edges suffice. This covers all primitive embeddings and arbitrary nonzero complex diagonal entries. It does not forbid arbitrary nondiagonal similarities to normal matrices, which are outside this first theorem's scope.

## 3. Affine-Hermitian obstruction for J_4

The actual recurrence gives P_4=X^4-A X^2+B with

    A=(1-q)(q^2+2q+3),
    B=(1-q)^2(q^2+q+1).

Both are nonzero for the stated primitive odd orders d>=5. One can also see A!=0 because it is the sum of three coefficients with positive real parts; B!=0 follows since q and q^3 are not 1.

The scale-invariant ratio is R=B/A^2. With q=c+i s, c^2+s^2=1, and a=1+2c, its expression is

    R=a/[4q(a-i s)^2],
    Im R=-a s c(c+2)/[4(a^2+s^2)^2].

Direct expansion confirms the imaginary denominator numerator s c(c+2). None of a, s, or c can vanish at primitive odd order d>=5: these cases would force order 3, order 1 or 2, or order 4, respectively. The denominator is positive and c+2>0. Thus R is nonreal at every relevant embedding; the principal-embedding sign is negative as claimed.

Independently parameterizing the unit circle by q=(1+i t)/(1-i t), with real t, gives

    Im R = -t(t-1)(t+1)(t^2-3)(t^2+3)
             / [2(t^4-2t^2+9)^2].

This agrees exactly with the candidate and exposes the same exceptional unit-circle points. The excluded point q=-1 is even order and irrelevant.

Suppose tau J_4+sigma I were similar to a Hermitian matrix, tau!=0. Its trace is 4 sigma, so sigma is real. Its real spectrum would therefore make tau J_4 have real spectrum. Equivalently its monic characteristic polynomial would have real coefficients, including -tau^2 A and tau^4 B. Since A!=0, their scale-invariant ratio R would be real, contradicting the preceding calculation. This argument does not assume simple spectrum and applies to every invertible similarity.

The positive-metric formulation is equivalent: if M>0 and M(tau J_4)=(tau J_4)* M, conjugating by M^(1/2) produces a Hermitian matrix. The affine real shift has no effect on that condition.

The conclusion is fully compatible with simplicity. Since B!=0 and R is nonreal, A^2-4B!=0. The two roots of the polynomial in X^2 are nonzero and distinct, so P_4 has four distinct roots. The independent exact quartic discriminant is 16 B(A^2-4B)^2. This remains a previously covered subfamily, not a newly claimed squarefreeness range.

## 4. Full-order metrics and every residual cut

For primitive q of order d, conjugation sends q^k to q^(-k), so u_(d-k)=conjugate(u_k). The right-half-plane principal square roots preserve conjugation, proving the full reversal identity exactly.

For 0<k<d, the Gaussian product for [d choose k]_q has a numerator factor 1-q^d and no zero denominator factor, proving [d choose k]_q=0. The endpoint coefficients are 1. Thus H_d(z;q)=1+z^d. Combining the baseline transformation H_d(v^2)=v^d P_d(v+v^(-1)) with the defining Laurent identity for Chebyshev polynomials gives P_d(X)=2T_d(X/2). This supplies the actual unlimited proof of the full spectrum; independent controls at already covered orders 3,5,9 merely check transcription.

Those Chebyshev roots are real and distinct. Therefore J_d is diagonalizable and, if J_d=V Lambda V^(-1) with Lambda real, W=(V^(-1))*V^(-1)>0 satisfies WJ_d=J_d*W. Existence of positive full-order metrics is valid.

Residual reversal instead has the exact additive defect

    u_(b-k)=1-q^b+q^b conjugate(u_k).

Since b<d, the defect 1-q^b is nonzero. More decisively, tr(J_b^2)=2 sum_(k=1)^(b-1)(1-q^k), so at q=exp(2 pi i a/d),

    Im tr(J_b^2)
      = -2 sin((b-1)pi a/d) sin(b pi a/d)/sin(pi a/d).

For gcd(a,d)=1 and 2<=b<d, neither numerator sine nor denominator sine vanishes. The principal embedding has both numerator sines positive and positive denominator, giving the asserted strict negative sign. Other primitive embeddings may change sign but not nonvanishing. Hence J_b cannot have all real eigenvalues, because the trace of its square is the sum of their squares with algebraic multiplicity. In particular no positive-definite Hermitian M can make J_b self-adjoint.

If a positive metric W for J_d were block diagonal across b | d-b, its positive principal block M would satisfy M J_b=J_b* M, a contradiction. Thus every full positive metric has a nonzero off-diagonal block N at every stated cut.

The displayed compression formula also has the correct conjugations and signs:

    M J_b-J_b* M = conjugate(C) N* - N C^T.

The independent controls verify this using full 2-by-2 formal matrix blocks, preserving order of multiplication rather than reducing to commuting scalar blocks. Its right-hand side cannot be zero for a positive M, by the same residual trace obstruction. Applying a residual eigenvector produces the stated boundary identity. This is not a positive representation of the bilinear norm v^T v. Neither the nonzero cross-block metric nor the full-order real spectrum proves the missing residual nonisotropy.

## 5. Evidence, reproducibility, and exclusions

The supplied frozen manifest hash matches exactly. All 11 manifest-declared files match their recorded byte counts and SHA-256 hashes before and after this review. The four retained source copies are byte-identical to the local originals named in SOURCE_BINDINGS.json, and the accepted baseline report hash agrees with its accepted review/verdict. These are local supplied-source verifications; no fresh remote GitHub retrieval is claimed.

The complete candidate, checker, run log, retained accepted author report, accepted review, verdict, and provenance metadata were inspected. No historical research program was imported or executed. The only replay was the current inspected candidate's fresh checker, copied to `author_replay/` before execution so that it could not rewrite the frozen candidate's CHECKS.json. The replay code is byte-identical, all 19 assertions passed, and the resulting CHECKS.json is byte-identical to the frozen candidate's output.

Fresh independent controls cover the actual symmetric characteristic polynomial, eigenvector recurrence, quartic discriminant, rational-unit-circle invariant, diagonal-similarity product invariance, full matrix compression, full-order recurrence transcription at already covered orders, exact finite-sine-sum algebra, residual reversal, source bindings, and before/after input integrity. All 55 assertions passed on their first execution. The code and log are retained beside this review.

The candidate's two earlier exploratory probes are accurately separated from its proof and certification. Their description does not turn them into new finite-order certifications or characteristic-zero counterexamples. The retained initial author checker failure is an explicit symbol-identity/transcription-interface issue, and the unchanged corrected checker passes in review. No claim here relies on the candidate's exploratory web search or any historical-originality assessment.

## Terminal result

The frozen candidate is scientifically accepted for exactly the three stated mechanism obstructions. The requested nonisotropy lemma and unrestricted ordinary guard remain open. A future proof must supply independent control of the actual complex bilinear kernel or another valid actual-family mechanism. This review performs no external write or canonical-record change.
