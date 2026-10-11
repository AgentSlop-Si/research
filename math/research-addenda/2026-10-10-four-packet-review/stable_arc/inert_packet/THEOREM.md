# Quantitative arc-signature rigidity for independently dressed Green sums

**Research note, October 11, 2026.** **Status:** a self-contained, mathematically proved *restricted-model* approximation theorem, numerical/combinatorial checks, and one independent finite-field rank check. **Not** a faster arbitrary-input DFT algorithm. **Worldwide mathematical novelty has not been established.**

## Scope and notation

Let \(U_N[k,j]=N^{-1/2}e^{-2\pi i k j/N}\), \(N\ge2\). Let \(W_\ell\) be an arbitrarily weighted Hamiltonian-cycle permutation matrix, with all edge weights nonzero and \(1-\prod_{\rm cycle}w\ne0\). Its Green inverse is \(G_\ell=(I-W_\ell)^{-1}\).

We allow **independently chosen invertible complex monomial matrices** (permutations times diagonal matrices) \(L_\ell,R_\ell\) for **each** summand, rather than just the common endpoint gauges of the earlier project:

\[
 M_N=\sum_{\ell=1}^{q}L_\ell G_\ell R_\ell.
\]

Complex scalar coefficients are included in these monomial scalings. There is no condition-number, phase-positivity, affine-cycle or bounded-magnitude assumption. The number of summands \(q\) is not restricted to two or three.

Set \(n=q+1\) and \(K=n^q\). All errors below are the spectral/operator \(2\)-norm.

## Theorem A: exact and stable arc-signature obstruction

1. **Finite, graph-only error certificate, for any \(N\ge n\).** Fix any \(n\) consecutive rows \(R\) of the target Fourier matrix. The cycle orders and the monomial permutations induce a partition \(\mathcal C\) of its \(N\) input columns into at most \(K\) signature classes. The partition depends on permutations alone, not on complex edge weights. For every class \(C\in\mathcal C\),
   \[
   \operatorname{rank}M_N[R,C]\le q,
   \qquad
   \|M_N-U_N\|_2\ge \sigma_n(U_N[R,C]),
   \]
   where \(\sigma_n\) is zero if \(|C|<n\). Consequently,
   \[
   \boxed{\|M_N-U_N\|_2 \ge \max_{C\in\mathcal C}\sqrt{\lambda_{\min}(U_N[R,C]U_N[R,C]^*)}.}\tag{A1}
   \]
   A second valid bound is
   \[
   \boxed{\|M_N-U_N\|_2\ge\sqrt{\frac1n\sum_{C\in\mathcal C}\lambda_{\min}(U_N[R,C]U_N[R,C]^*)}.}\tag{A2}
   \]
2. **Exact factorization obstruction, even with independent monomial endpoints.** If \(M_N=U_N\), then
   \[
     \boxed{N\le q(q+1)^q}.\tag{A3}
   \]
3. **Uniform stable obstruction.** For all \(N\ge4(q+1)^{q+1}=4nK\),
   \[
   \boxed{\|M_N-U_N\|_2\ge c_q :=\frac1{(2n)^n K^{\,n-1/2}} >0.}\tag{A4}
   \]
   In particular, for *any fixed \(q\)* no family of the above one-layer Green sums can converge in spectral norm to the full normalized DFT as \(N\to\infty\).
4. **Polynomial accuracy needs a growing number of branches.** For each fixed \(\alpha>0\), if a family of the above representations satisfies \(\|M_N-U_N\|_2\le N^{-\alpha}\) for all sufficiently large \(N\), then
   \[
   \boxed{q(N)=\Omega_{\alpha}\Bigl(\sqrt{\log N/\log\log N}\Bigr)}.\tag{A5}
   \]
   This is an approximation bound *only for this representation grammar*. It is not an FFT-operation lower bound.

## Proof

### Step 1: arc signatures still work under separate monomial gauges

Fix \(n\) target output rows. For each summand, its *own* left monomial maps those rows to \(n\) distinct positions on its Hamiltonian cycle; its *own* right monomial maps each target input column to some cycle position. The exact cyclic Green formula shows that the column restricted to the \(n\) marked rows has, **up to one nonzero column-dependent scalar**, a projective direction determined solely by which one of at most \(n\) directed arcs contains that source vertex. An independent left diagonal scales the marked coordinates by constants independent of the source column. The right diagonal scales the full restricted column by one scalar. Neither alters the at-most-\(n\) direction count.

Thus for \(q\) summands the joint arc-signature tuple takes at most \(n^q=K\) values. Inside any one tuple class \(C\), the columns of each summand lie in a single one-dimensional subspace of \(\mathbb C^n\). Their sum has column rank at most \(q=n-1\), proving the first rank assertion. By the Eckart–Young singular-value bound, \(\|(M_N-U_N)[R,C]\|_2\ge\sigma_n(U_N[R,C])\). Taking maxima proves (A1). Taking disjoint column classes, adding their best rank-\(q\) Frobenius residuals, and using \(\|E[R,:]\|_F^2\le n\|E\|_2^2\) proves (A2).

For exact equality, every \(n\) columns of \(U_N[R,:]\) are independent: after extracting a nonzero scalar from each column, the matrix is a Vandermonde \((1,z_j,\ldots,z_j^{n-1})^T\) in distinct \(N\)th roots of unity. A class has at most \(q\) columns, whence \(N\le qK\), proving (A3). This is the independent-endpoint extension of the existing Phase 43 exact bound.

### Step 2: a discrete Fourier density lemma

Let \(C\subset\{0,\dots,N-1\}\) have cardinality \(L\ge\alpha N\) for \(0<\alpha\le1\), and suppose \(N\ge4n/\alpha\). Let \(R\) consist of \(n\) consecutive Fourier output frequencies. Then

\[
\boxed{\sigma_n(U_N[R,C])\ge \frac{\alpha^{n-1/2}}{(2n)^n}.}\tag{L}
\]

**Proof of (L).** Sort \(C=\{c_1<\cdots<c_L\}\) and set \(s=\lfloor L/(2n)\rfloor\ge\alpha N/(4n)\). Form \(n\) disjoint groups of \(s\) points each, alternating with \(s\) unselected points in this sorted sequence; leave the last tail unselected. Any two points taken from different selected groups are separated by at least \(s\) positions in *both cyclic directions* around the complete \(N\)-point frequency grid. Thus their roots of unity have chord distance at least \(\delta=2\sin(\pi s/N)\ge 4s/N\ge\alpha/n\).

For arbitrary complex \(a=(a_0,\dots,a_{n-1})\) with \(\|a\|_2=1\), consider the polynomial \(p(z)=\sum_{r=0}^{n-1}a_r z^r\). Parseval on the unit circle gives \(\max_{|z|=1}|p(z)|\ge1\). Choose one frequency from each of the \(n\) selected groups, obtaining separated unit roots \(z_1,\ldots,z_n\). Lagrange interpolation and \(|z-z_j|\le2\) on the unit circle imply

\[
1\le\sup_{|z|=1}|p(z)|\le (2/\delta)^{n-1}\sqrt n\,\Bigl(\sum_{j=1}^n|p(z_j)|^2\Bigr)^{1/2}.
\]

Average the squared inequality uniformly over all \(s^n\) choices, one from each group. Each point in a selected group appears in the relevant sum in a fraction \(1/s\) of all choices. Hence

\[
\frac1N\sum_{j\in C}|p(e^{-2\pi i j/N})|^2
\ge\frac{s}{N}\frac{(\delta/2)^{2(n-1)}}{n}
\ge\frac{\alpha}{4n}\frac{(\alpha/(2n))^{2(n-1)}}n
=\frac{\alpha^{2n-1}}{(2n)^{2n}}.
\]

The quantity on the left is precisely the Rayleigh quotient of \(U_N[R,C]U_N[R,C]^*\) for an arbitrary unit coefficient vector, up to a unit-modulus factor caused by the starting row frequency. Taking the minimum Rayleigh quotient proves (L). QED.

### Step 3: use the largest arc-signature class

The largest class in the partition from Step 1 has size at least \(N/K\). Set \(\alpha=1/K\) in (L). The hypothesis \(N\ge4nK\) exactly ensures the lemma is applicable, and we obtain

\[\sigma_n(U_N[R,C])\ge\frac{K^{-(n-1/2)}}{(2n)^n}=c_q.\]

Combining with (A1) proves (A4).

### Step 4: branch growth at polynomial precision

For \(q\to\infty\), \(n=q+1\), \(K=n^q\), and

\[\log(1/c_q)= n\log(2n)+(n-1/2)q\log n=O(q^2\log(q+2)).\]

If \(q\le c_\alpha\sqrt{\log N/\log\log N}\) with a sufficiently small fixed \(c_\alpha>0\), then the size condition \(N\ge4nK\) holds for sufficiently large \(N\), while \(c_q>N^{-\alpha}\). This contradicts the requested approximation precision. Thus (A5). QED.

## Fast graph-only certificate cost

For the supplied cycle orderings and branch endpoint permutations, all cycle-position maps can be prepared in \(O(qN)\) operations. Assigning the \(q\) arc-signature labels to every target input column takes \(O(q(q+1)N)\) comparisons, with no Green arithmetic. Construct the \(n\times n\) Fourier Gram matrix of each class by accumulating \(v_jv_j^*/N\) over its columns, in a total of \(O(n^2N)\) complex operations, followed by at most \(K\) eigensolvers of size \(n\). Therefore the straightforward certificate is \(O(q^2N+Kn^3)\), or **O(N) for fixed q**, with all N input column labels read. As in any numerical eigenvalue computation, finite-precision decimal estimates are not exact positivity certificates unless accompanied by intervals.

## Verification summary

- `verify.py` checks **27** independent complex non-affine networks at q=1,2,3, with *independent* random left and right monomial gauges for every summand. In every case the computed arc-signature class count was <= \((q+1)^q\), each class submatrix had rank <= q, and the Fourier Gram spectral and Frobenius certificates were respected.
- Two independent exact modular checks at \(N=256\), \(\mathbb F_{257}\), find 4-column arc classes with Green-sum rank **3** and Fourier rank **4**. The second check uses **independent monomial endpoint maps on all three summands**, not only common endpoint gauges.
- **10,381** adversarial small-subset checks pass the quantile/group separation lemma.
- Two large graph-only certificates: N=256, q=2 yields approx **0.41490585**; N=1024, q=3 yields approx **0.27738415**. These decimals are floating-point diagnostics, not certified interval constants; (A1) itself is an exact mathematical inequality.

All tests are illustrative and finite. The all-N claim comes from the proof.

## Relation to previous work and originality

- **Inherited:** the *exact* rank/arc-signature mechanism and `N<=q(q+1)^q` for a single common-endpoint-gauged q-cycle sum were already in the user's **Phase 43** research, dated October 11, 2026. Do **not** relabel that exact theorem as new.
- **Proposed extension here:** independent endpoint monomial gauges **per summand**, an **explicit uniform operator-norm approximation gap** for fixed q, the **polynomial-precision branch-growth corollary**, and a **linear-work-for-fixed-q graph-only spectral certificate**.
- **Classical ingredients:** Lagrange interpolation, Vandermonde/full-spark Fourier minors, discretized polynomial/Remez inequalities, numerical linear algebra. Related prior literature includes Yomdin's *Remez-type inequality for discrete sets* (2012) and Tikhonov–Yuditskii's *Sharp Remez inequality* (2018). A targeted search did not locate the exact combined theorem, but **priority and journal publishability remain unverified**.
- **Not covered:** products \((G_1+G_2)D(G_3+G_4)\), multiple noncommuting layers, input-adaptive factorizations with uncharged coefficients, nonlinear FFT algorithms, all-precision bit complexity, or unrestricted complex linear circuits. Phase 43's exact **four-row interpolation** at N=8,16 for the two-stage complex-interstage 3+3 network is not contradicted.

## Constructive next gate

Continue Phase 43's **two-layer** architecture, where four rows can already be interpolated exactly at N=8,16 using the allowed complex middle diagonal. The critical unsolved problem is to satisfy *all rows* and Weyl covariance, with an all-length explicit coefficient schedule and all setup costs charged. A partial row fit, submersion rank, or a one-layer lower bound is not an FFT acceleration.
