# Independent review of Q31's common-cycle regular-jet attempt

10 October 2026. Verdict: **SCOPED PASS**, including the separately versioned quadratic-chirp supplement. Q31's constructive objective remains open; its already accepted conditional reduction is unchanged.

## 1. Exactly what was reviewed

The frozen main manuscript is `../regular_jet/CONSTRUCTIVE_ATTEMPT_AND_BARRIER.md`, SHA-256 `760b2c3d7786db4c9fc6fb569f1f60bf4bc9b14e7d58a31c82961952c3850993`. The separate supplement is `../regular_jet/CHIRP_GAUGE_SUPPLEMENT_v1.md`, SHA-256 `d937da228387c2f8345e581b017885a20aef24e36666bed6ad52034a52a83830`.

I read the actual original sparse-jet theory, original Necklace theory, existing Necklace audit, current bound Sheet snapshot, original Phase 22 certificate and audit, quasi-Hermite review, two-Cayley feedback obstruction, and whole-word rational-fusion obstruction. These conclusions are grounded in the cited original materials. The source-binding receipt records their paths and current hashes. Original files were not changed. Candidate and uploaded programs were read only as text; none were executed or imported. All executed controls in this review were newly authored here, and the chirp control imports only this review's own matrix oracle.

The current Q31 contract was checked in Research queue row 34 of the supplied Sheet snapshot. It requires a uniformly generated origin-regular scalar program on **N raw inputs**, with the formal one/two-coordinate quadratic jet of x^T F_N x/2. The whole preparation and fresh-input work, indexing, code generation, and N output writes are charged. The inherited compiler gives O(s+N) work **and storage**; it does not give O(N) storage from an O(N log log N) source automatically. A finite-field pointwise identity or support-selected decoder does not meet the formal contract.

The Necklace continuation instead searches for a priced rectangular P: K^N -> K^(2N) around H = Hessian Psi(gamma), a symmetric 2N-by-2N carrier, such that P^T H P = F_N. This is dimensionally consistent. Both T e_0 = 1 and T S = D_omega T are required by its alternate certificate. Merely producing a cheap dense T is insufficient.

## 2. Independent proof of the main density/support gate

Use S e_j = e_(j+1 mod N), F_ij = omega^(ij), and ordinary transpose, with no complex conjugation. Let Q=q(S), q(t)=sum_(a=0)^r q_a t^a, r<N, and Q invertible. Since the N roots omega^j are distinct, Q is invertible exactly when q(omega^j) is nonzero for every j. A primitive root in a field also ensures that the characteristic does not divide N.

For M-by-N R, M-by-M H, and P=R Q^(-1), the equality P^T H P=F becomes

    R^T H R = Q^T F Q.

In particular the transpose is on the left denominator. No step replaces it with Q or reverses the order of a noncommuting product.

The (i,j) entry on the right is, directly from Q's columns,

    sum_(a,b) q_a q_b omega^((i+a)(j+b))
      = omega^(ij) sum_b q_b q(omega^(j+b)) (omega^i)^b.

Thus, for fixed j, divide by the nonzero omega^(ij) and evaluate a degree-at-most-r polynomial L_j at the N distinct roots. In the manuscript's hypotheses its constant coefficient is q_0 q(omega^j), which is nonzero. It has at most r roots, so every column of Q^T F Q has at least N-r nonzeros.

Now assume R has at most s nonzeros per column and d per row, and H has at most Delta nonzeros per row. A row of R^T begins at at most s carrier coordinates; H reaches at most s Delta coordinates; the final R reaches at most s Delta d output coordinates. Each row of R^T H R therefore has at most s Delta d nonzeros. Comparing total supports, rather than silently comparing a row count with an unrelated column count, gives

    N(N-r) <= nnz(R^T H R) <= N s Delta d,
    N-r <= s d Delta.

The statement is valid. H's symmetry is natural for this application but not necessary for this total-support proof. Without symmetry a row-support upper bound cannot be called a column-support upper bound; the supplied proof does not make that mistake. Cancellation, zero entries, or overlapping paths only lower the upper bound.

Two optional refinements are mathematically valid but are not required to accept the frozen statement:

- q_0 != 0 can be dropped: select any b with q_b != 0. The corresponding coefficient q_b q(omega^(j+b)) in L_j is nonzero. Distinct b are distinct polynomial exponents because r<N.
- If actual sparsity is known, N(N-r) <= d Delta nnz(R) is also valid. Neither refinement alters the advertised four-Green threshold.

## 3. All gains and branch coefficients are covered

For four legal scalar gains a_l, q(t)=product_l(1-a_l t) has degree at most four, q(0)=1, and q(S) is invertible because each a_l^N != 1. The two branch numerators are sums of lambda_l times the product of the other three factors. Each therefore has degree at most three. The factorization P Q=R holds as a polynomial identity in S, not as a numerical fit.

With R formed by stacking the two numerator maps, a row has at most four nonzeros, and an input column has at most eight. Interleaving the two edge blocks only permutes the carrier coordinates and preserves these counts. Repeated gains, zero gains, zero coefficients, and exact cancellation of a whole branch remain within these upper bounds. No division by a gain or coefficient is used.

The original Necklace locality proof bounds every carrier row by

    Delta_k <= k 2^max(0,k-n-1).

This follows by anchoring one edge of a closed binary word. When k>=n+1, its prescribed n-bit source and appended bit leave k-n-1 free bits; when k<=n, periodic consistency permits at most one word. Each possible anchored word contributes at most k edge labels. This is independent of baseline or necklace coefficients, including zero baselines. Our exhaustive structural controls also retain repeated-edge diagonal contributions.

For k=n+2, Delta<=2(n+2), hence

    N-4 <= 64(n+2)

is necessary. At n=10 it would require 1020<=768, a contradiction. The difference increases after n=10 because the next increment is 2^n-64>0. Therefore every dyadic N>=1024 is excluded, uniformly over all legal gains and branch coefficients and over retuned baselines/necklace coefficients at that horizon. N=512 is **not** excluded by this displayed universal inequality. Particular failed samples below 1024 remain particular samples.

The general fixed-horizon-offset bound N-4 <= 32(n+c)2^max(0,c-1) is also correct. If c is fixed, or 2^c=O(log n), its right side is o(2^n), so eventual exclusion follows. This is a representation bound, not a runtime lower bound for a growing number of rational terms or a different shared circuit.

## 4. Source regularity and cost

The centered source

    Phi(x)=Psi(gamma+Px)-Psi(gamma)-gradient(Psi)(gamma)^T Px

has zero constant and linear terms and Hessian P^T H P. This explicit centering repairs the possible mismatch between an uncentered Necklace source and the original full degree-two jet contract. All four Green inversions have input-independent guarded denominators 1-a_l^N. With prepared constants, Phi is polynomial in x, so every intermediate input-dependent operation remains origin-regular.

Four constant-gain cyclic recurrences, their transpose circuits, generation of canonical root powers, and centering each cost O(N). The original accepted necklace enumeration charges copying each representative, reconstructing its starting state, all repeated edge occurrences, and scalar circuit emission; at k=n+2 the total is O(2^k)=O(N). The gradient needed for centering can be obtained in O(k) per monomial with prefix/suffix products, even at a zero baseline. No dense Hessian is part of the production evaluator. Choosing gains (2,3,5,7) in characteristic zero supplies a literal uniform example; arbitrary supplied gains only give the same cost once their generation is also charged.

Accordingly this is an actual O(N)-work scalar family and O(N)-work operator family, with O(N) append-only storage at fixed c. The theorem proves it does not yield Fourier in the stated growing-size subclass. Exact scalar complexity says nothing by itself about bit complexity, numerical conditioning, hardware performance, or root discovery. Fixed finite-field controls do not supply primitive roots for unbounded N.

## 5. Independent review of the chirp supplement

Let C_ii=omega^(h i^2+ell i), with integer h,ell, and W=C S C^(-1). The wraparound is legitimate using only the supplied N-th root: replacing i by i+N changes the exponent by a multiple of N. All powers W^a remain monomial weighted shifts, so the four-Green numerator support counts are unchanged.

Direct expansion gives

    (q(W)^T F q(W))_ij = omega^(ij) sum_(a,b) q_a q_b
      omega^[h(a^2+b^2)+ell(a+b)+ab]
      (omega^i)^(2ha+b) (omega^j)^(a+2hb).

For fixed j, its Laurent exponents in z=omega^i lie in an interval of width at most w=(2|h|+1)r. Coefficients with the same exponent may cancel. However, invertibility of q(W) and F makes every matrix column nonzero, so the Laurent polynomial is not identically zero. Multiplication by a monomial makes it an ordinary polynomial of degree at most w without changing its nonzero-root zeros. If w<N, every column therefore has at least N-w nonzeros, and the same support comparison proves

    N-(2|h|+1)r <= s d Delta.

The argument is correct, including signed h, arbitrary integer linear phase ell, and q_0=0. When w>=N the bound is vacuous. A fixed h is eventually excluded by N-4(2|h|+1)<=64(n+2), and h in {-2,-1,0,1,2} is excluded for every dyadic N>=1024 as claimed. More broadly the same starting threshold works for |h|<=31, but the supplement makes the narrower, valid claim.

We found an exact warning against the constant-term shortcut: over F17 with N=8, omega=2, h=-1, ell=0, q=(1,1,1), q(W) is invertible but one Laurent column's constant coefficient vanishes. The supplement correctly uses matrix invertibility rather than that shortcut. Its O(N) preparation uses the recurrence for consecutive C ratios; fixed h and reduced ell do not introduce uncharged roots.

This excludes one common bounded-curvature gauge. Arbitrary varying weights, nonquadratic gauges, distinct cycles, or growing curvature outside the quantitative inequality remain outside the certificate. Changing the representation merely removes this proof's premise; it is not evidence of Fourier compatibility.

## 6. Relationship to earlier project results and published ingredients

The sparse-marking obstruction previously required P itself to have bounded row/column support. Here P is generally dense; R=Pq(S), not P, is sparse. Thus applying that earlier theorem directly would be invalid.

The prior two-Cayley feedback argument already used sparse denominator clearing and a Fourier support-product inequality. Its fixed rational feedback transfer permits an arbitrary common weighted cycle. In the present problem the intervening sparse H is otherwise unrestricted, so T=P^T H P need not be a scalar rational function of S, and one-sided clearing generally leaves a dense factor. The explicit second clearing and contiguous polynomial-support calculation provide the new project-specific specialization. This is a close extension of the same obstruction strategy, not a fundamentally new Fourier lower-bound method.

For perspective, Q^T F Q=(Q^T diag(q(omega^i))) F. Each row of the first factor has at most r+1 nonzeros. Applying only the earlier support-product lemma would yield the weaker necessary condition N<=(r+1)s d Delta. The degree-r polynomial evaluation argument strengthens its Fourier-support lower bound from N/(r+1) to N-r in this natural ordering. For r=4 and the stated carrier, that generic support-product route first excludes dyadic N>=8192, while the reviewed root-count bound excludes N>=1024. This is a comparison of certificate strength, not a complexity improvement.

The earlier whole-word rational-fusion theorem uses quasiseparable cut ranks in one common order. Row sparsity of an arbitrary carrier H does not ensure small cut ranks in that order: a symmetric permutation exchanging the two coordinate halves has one nonzero per row and full half-cut rank. Thus its cut-rank premise cannot silently be inferred here. The present theorem also does not exclude general independently ordered Green products covered by neither premise.

The root-count mechanism is classical polynomial evaluation/Vandermonde reasoning. Reed and Solomon's original paper, pages 300–301, explicitly evaluates low-degree polynomials at distinct field elements and uses the nonzero Vandermonde determinant to show uniqueness from any sufficient evaluation subset. This is direct primary context for the density ingredient, rather than a novelty claim for it. [Reed–Solomon, 1960](https://sites.math.rutgers.edu/~zeilberg/akherim/ReedS1960.pdf)

The Hessian-vector mechanism remains inherited classical differentiation. Pearlmutter's author manuscript, Sections 2–3, derives it by directionally differentiating gradient computation without materializing the Hessian. [Pearlmutter, 1994](https://www.bcl.hamilton.ie/~barak/papers/nc-hessian.pdf)

The Phase 22 recognition algorithm is likewise not a regular origin selector: a regular rational U(b_0,b_1) equal formally to u on (a,au) for two distinct u would give two values for U(0,0). The fixed-rank linear transcript obstruction is inherited. The full-order Vandermonde identity with Y=F D_h V is a correct but circular factorization; explicitly preparing all N jets takes N^2 entries, and the bounded-order recognition condition 2R<=N cannot be invoked at R=N. The quasi-Hermite exclusion theorem solves a different local algebraic guard and supplies no missing transport. These compatibility observations check; they do not invalidate the existing structured-input algorithms.

Historical priority for the exact packaged two-sided inequality has not been established by this bounded comparison. Appropriate classification: a scoped research-log refinement using elementary established ingredients. It does not warrant a new general FFT algorithm, universal arithmetic lower bound, external peer-review claim, or discovery-count increment.

## 7. Fresh controls and final disposition

Review-owned `independent_controls.py` passed:

- Exhaustive F5,N=4 polynomial enumeration: 625 polynomials, all 256 invertible denominator cases checked for matrix/formula equality and the support bound, including 52 with q_0=0.
- 270 additional invertible polynomial cases over F17, F97 and F257, through N=32.
- 125 four-Green matrix identities, including zero/repeated gains and zero/canceling/scaled branch coefficients.
- 100 rectangular sparse-product cases and two row/column-counting negative controls.
- 72 exhaustive closed-word structural locality cases, through N=512 and horizons n+3.
- Eight independent formal centering/Hessian controls, including zero baselines.
- A singular-denominator negative control: q=1-t^2, N=4 over F17 gives two zero columns after clearing, violating the asserted positive density if Q-invertibility is omitted.
- The exact dyadic threshold inequality for n=3 through 64. The all-N threshold is separately proved above.

Review-owned `independent_chirp_controls.py` passed 216 direct matrix cases, 3,240 columns, signed curvatures -4 through 4, three linear phases, and 108 q_0=0 cases. It also checked 21 direct weighted-shift columns at N=1024 for h=-3 through 3, and found the exact constant-term cancellation control described above.

These are finite exact arithmetic corroborations, not source-program replays, asymptotic benchmarks, or proofs by sampling. The all-parameter conclusions follow from the displayed proofs. No corrections to the frozen main theorem or supplement were required.

**Final disposition:** accept both scoped obstruction statements and the cheap centered candidate's cost/regularity ledger. Retain Q31 as “Construction blocked” and its conditional proof as closed. Independent-cycle/nonquadratic low-work Fourier synthesis remains the unresolved task.
