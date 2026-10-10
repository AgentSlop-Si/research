# Phase defect rank claim comparison

Audit date: 2026-10-10 UTC. This is a bounded mathematical and primary-source comparison, not an exhaustive priority search, a publication recommendation, or a change to any research ranking.

## Main finding

The reviewed statements are mathematically useful, but the evidence does not support presenting their ingredients as new general linear-algebra or Fourier principles. The rank inequality is elementary; its exact pairing converse is an elementary construction; the fixed-gauge spectral-error identity is a direct low-rank approximation corollary; and the sharp Fourier phase-energy formula follows from established finite-abelian Fourier norm results after an explicit doubling-map reduction. The arbitrary-monomial stability correction is an exact invariance of the stated feasible set.

No inspected paper was verified to state the entire invariant and rank sandwich in exactly this packaging. That leaves the history of this particular synthesis unresolved. A failure to locate an identical statement is not evidence that it is novel. Mathematical validity, prior appearance of the exact formulation, significance, and computational consequences are separate questions.

## Objects actually compared

The reviewed model is

\[
\rho(U)=\min\{\operatorname{rank}_{\mathbb C}E:
U=L(B+E)R,\ B\in\mathbb R^{N\times N},\ L,R\text{ invertible complex monomial}\}.
\]

The real core is unrestricted. The correction has only a complex-rank constraint. Approximation is measured by the external operator norm \(\|U-L(B+E)R\|_2\), not a norm after applying arbitrary inverse gauges. These hypotheses are essential to every classification below. There is no prescribed sparsity, architecture, fast multiplication, entry bound, or pre-gauge conditioning constraint.

The local inputs were read without modifying them:

- `research_cycle_2244/phase_defect_review/REVIEW.md`, SHA-256 `7a7bcbebd605268cb9cd7b396ac880d06e91b044ace9e39ad5709f01701b320b`.
- `research_cycle_2249/phase_defect_scope_check/ROOT_SCOPE_CHECK.md`, SHA-256 `8e3566081118ce232c41e23030c2d532fb788e4202409941180bf4a94320ecb1`.

This comparison takes those scoped validity reviews as its mathematical starting point. It does not re-run their certificates or certify a particular Green architecture.

## 1 The elementary rank inequality

For any complex matrix \(E\),

\[
\operatorname{rank}_{\mathbb R}\operatorname{Im}E
=\operatorname{rank}_{\mathbb C}(E-\overline E)
\le 2\operatorname{rank}_{\mathbb C}E.
\]

This follows immediately from rank subadditivity and conjugation preserving rank. A second interpretation uses the standard realification

\[
\mathcal R(E)=\begin{pmatrix}\Re E&-\Im E\\\Im E&\Re E\end{pmatrix}:
\quad\operatorname{rank}_{\mathbb R}\mathcal R(E)=2\operatorname{rank}_{\mathbb C}E,
\]

of which \(\Im E\) is a submatrix. The rank equality follows by complex change of basis to \(\operatorname{diag}(E,\overline E)\).

**Assessment:** an elementary consequence of classical rank algebra, not a defensible standalone novelty claim. This is a self-contained mathematical classification; the search did not establish a first historical appearance of this exact displayed inequality. Do not confuse realification rank with the rank of an entrywise real or imaginary part.

## 2 The exact pairing converse

For a prescribed real matrix \(T\), the reviewed converse is

\[
\min_{\operatorname{Im}E=T}\operatorname{rank}_{\mathbb C}E
=\left\lceil\frac{\operatorname{rank}_{\mathbb R}T}{2}\right\rceil.
\]

It is stronger than the preceding inequality alone, but its upper direction requires only pairing real rank-one summands. An equally short normal-form proof sends \(T\), by invertible real row and column operations, to a rectangular matrix with an identity block of size \(m=\operatorname{rank}T\). Replace each consecutive two-dimensional identity block by

\[
\begin{pmatrix}i&1\\-1&i\end{pmatrix}.
\]

This block has imaginary part \(I_2\) and complex rank one. For odd \(m\), append the one-dimensional block \((i)\); undo the real operations. The lower bound proves optimality.

**Assessment:** an elementary exact converse worth stating clearly, with historical attribution unresolved in this finite search. Its short proof is evidence that it is standard-method material; it is not evidence of a specific published duplicate. No special Fourier result is needed. The variational identity for \(\rho\) follows by applying this lemma after rephasing and choosing the free real core to cancel the real part.

## 3 Fixed gauge spectral error

For \(Y=\operatorname{Im}V\) and \(2r<N\),

\[
\min_{B\text{ real},\,\operatorname{rank}_{\mathbb C}E\le r}
\|V-B-E\|_2=\sigma_{2r+1}(Y).
\]

The underlying spectral best-rank approximation theorem is explicit in Halko, Martinsson and Tropp, section 10.2, immediately following Theorem 10.6: the rank-\(k\) spectral error is \(\sigma_{k+1}\), attributed there to Mirsky. Their reference 97 identifies the 1960 article. [Primary research text](https://arxiv.org/pdf/0909.4061#page=57)

The transfer to the present model is exact: imaginary-part extraction is an operator-norm contraction; its image on complex rank-at-most-\(r\) matrices is precisely the set of real matrices of rank at most \(2r\), by Section 2. A truncated real SVD of \(Y\) supplies the best such image. The free \(B\) cancels the real part of its paired complex lift, leaving exactly the imaginary residual.

**Assessment:** a direct application of classical low-rank approximation plus the elementary pairing lemma. It is not a new spectral approximation principle. It also does not solve the remaining minimization over row and column phases.

The 1936 Eckart–Young paper addresses least squares; this audit does not silently attribute the spectral-norm extension to an uninspected passage of that paper. The original Mirsky body was inaccessible through the tested publisher route. The historical citation and an explicit contemporary statement are verified; inspection of the original 1960 proof is not claimed.

## 4 Fourier phase energy and the two torsion parameter

Let \(U_G\) be the normalized character table, \(N=|G|\), \(g=|G[2]|\), and \(H_{x,\chi}=\chi(2x)\), with conjugations adjusted to the Fourier sign convention. The review proves

\[
\min_{P,Q\text{ diagonal unitary}}\|\operatorname{Im}(PU_GQ)\|_F^2
=\frac{N-\sqrt{Ng}}2.
\]

The most relevant primary antecedent is Gilbert–Rzeszotnik (2010): Theorem 2.1 gives the finite-abelian Fourier operator norms, including \(\|F_K\|_{\infty\to1}=|K|\) for normalized \(F_K\); Theorem 4.7 proves existence of biunimodular functions on every finite abelian group. Their Lemma 4.6 gives the product-group construction. [Original article](https://www.numdam.org/article/AIF_2010__60_4_1317_0.pdf)

Here is the audit's explicit reduction of the reviewed expression to that antecedent. It is a derivation, not a claim that their paper prints the phase-defect formula.

1. The map \(x\mapsto2x\) has kernel of size \(g\) and image \(K=2G\) of size \(M=N/g\).
2. Each image element appears in \(g\) rows of \(H\). Restricting characters of \(G\) to \(K\) gives every character of \(K\), each \(g\) times. Thus row and column permutations turn \(H\) into \(C_K\otimes J_g\), where \(C_K=\sqrt M F_K\) is the unnormalized character table.
3. Consequently \(\|H\|_2=g\sqrt M=\sqrt{Ng}\). This alone gives the reviewed energy lower bound by Cauchy–Schwarz.
4. For phases \(a,b\), maximizing \(\Re(a^THb)\) first over \(a\) gives \(\|Hb\|_1\). A biunimodular vector for \(F_K\), repeated \(g\) times, makes every output modulus \(g\sqrt M\). Hence the maximum is \(Ng\sqrt M=N\sqrt{Ng}\).
5. Substitute into
\[
\|\Im(PU_GQ)\|_F^2=\tfrac12\bigl(N-N^{-1}\Re((p^2)^THq^2)\bigr).
\]
Every phase has a square root, so using \(p^2,q^2\) imposes no further restriction.

**Assessment:** both the lower bound and its attainment are direct consequences of standard character orthogonality, a group-kernel calculation, and established Fourier norm extremals. The dependence on \(g\) is the multiplicity of the doubling map; it is not a new uncertainty parameter that lacks prior harmonic-analysis machinery.

The explicit quadratic chirps in the review also belong to established biunimodular theory. Führ–Rzeszotnik, section 1, displays the odd/even Gauss sequences; Theorem 4.1 identifies biunimodular existence with the \(\infty\to1\) norm attaining the dimension. [Primary paper](https://arxiv.org/html/1506.06738)

Idel–Wolf, Theorem 2, proves diagonal-unitary scaling to row and column sums one for any unitary matrix. This is a broader source of biunimodular existence, but it must be applied to the quotient Fourier unitary here: \(H/\sqrt N\) itself is not unitary when \(g>1\). Their central matrix need not be real. [Primary paper](https://arxiv.org/html/1408.5728)

The rank sandwich then uses elementary consequences: \(\|\Im(PU_GQ)\|_2\le1\), rank at least squared Frobenius norm for a contraction, the pairing lemma, and character inversion for the upper bound. Sharp energy does not imply sharp rank. The general finite-size minimum of \(\rho(U_G)\) remains unsolved by these arguments. For Walsh groups, \(g=N\), so the obstruction is zero. An \(N/4\) leading asymptotic requires \(g=o(N)\).

## 5 Stable error and arbitrary monomial gauges

The stability estimate follows from the same singular-value counting: if the first \(2r\) singular values of \(Y\) are at most one and the rest are at most \(\varepsilon\), then

\[
\frac{N-\sqrt{Ng}}2\le 2r+(N-2r)\varepsilon^2.
\]

For \(2r<N\), this gives the reviewed squared-error lower bound. This is a direct combination of the energy bound and standard low-rank approximation, not an independent stability mechanism.

For arbitrary complex monomial gauges, write \(L=D_1S_1\), \(R=S_2D_2\), with \(D_i\) diagonal unitary and \(S_i\) real invertible monomial. Absorb \(S_1,S_2\) into both core terms. Realness and correction rank are preserved, and the entire external approximant is unchanged. Thus the arbitrary-monomial and diagonal-unitary models have identical feasible approximant sets and identical optimal external errors.

**Assessment:** the scope correction is correct and materially useful for interpreting this manuscript. It is elementary model invariance rather than a new theorem about ill-conditioned norm transformations. It would cease to be automatic with extra non-invariant restrictions on \(B,E\), or with a different pre-gauge error contract. Historical first appearance of this particular observation was not established.

## Nearby literature with different mathematical objects

- **Phase rank:** Goucha–Gouveia minimize the rank of an entire matrix with prescribed entry phases while allowing independent positive entry magnitudes. This is not the present correction rank relative to an unrestricted real core, and its magnitudes are not restricted to separable outer gauges. Definition 1.1 makes the distinction explicit. [Primary paper](https://arxiv.org/pdf/2111.01962#page=2)
- **Phaseless rank:** the same authors instead fix every entry modulus and vary every entry phase independently. For a constant nonzero modulus table, this rank can be one, whereas the reviewed Fourier defect can be positive. This is an immediate model comparison, not a theorem transfer. [Definition 1.1](https://arxiv.org/html/1909.02417)
- **Unitary or Hadamard defect:** Tadej–Życzkowski define a differential dimension deficit for the map \(U\mapsto(|U_{ij}|^2)\), not the rank of an imaginary part or correction. Their Definition 2.1 and Fourier defect formula concern deformations within fixed moduli. The shared word “defect” does not identify the invariants. [Primary paper](https://arxiv.org/pdf/math/0702510#page=4)
- **Real entries of Hadamard matrices:** Liang and coauthors count real entries; their Theorem 9 gives possible counts in specified dimensions. Entry count, Frobenius imaginary energy, and imaginary-part rank are different quantities. These results are relevant context, not a verified duplicate of the rank sandwich. [Primary paper](https://arxiv.org/pdf/1904.10181#page=10)
- **Fourier uncertainty:** Meshulam's Theorems 1.1–1.2 concern supports of a single function and its Fourier transform, with prime and divisor refinements. The phase-energy argument instead maximizes a dense bilinear form. Both use Fourier structure, but the support inequalities do not state the reviewed formula. [Primary preprint](https://arxiv.org/pdf/math/0312407#page=2)
- **Real rank-reducing perturbations:** the Wicks–DeCarlo abstract describes the smallest-norm real perturbation that makes a complex matrix drop rank. Here the real term is free and the complex remainder's rank is constrained. This is a nearby matrix-nearness problem with a different objective; only the publisher abstract was inspected. [Publisher issue and abstract](https://epubs.siam.org/toc/sjmael/15/4)

## Claim language supported by this audit

A defensible description is: “An elementary rank-defect formulation for approximation by a real core and a complex low-rank correction, with Fourier bounds obtained from character orthogonality and classical biunimodular constructions. Under the unrestricted-core external-norm contract, arbitrary monomial gauges reduce exactly to unitary phase gauges.”

Do not claim a new general rank inequality, a new best low-rank spectral approximation theorem, discovery of the chirps, a new all-finite-abelian biunimodular existence theorem, an exact solution of the global Fourier rank minimum, or an FFT lower bound. The present evidence supports a useful synthesis/correction. It neither proves nor disproves that the precise complete formulation has appeared before.

## Finite search scope and remaining limits

The search was closed after 33 query strings in nine topical groups plus targeted openings and within-document searches. The full query inventory and source inspection levels are in `SEARCH_AND_SOURCES.json`. Nine primary research texts had relevant body passages inspected. Additional foundational or neighboring records were kept at explicit metadata/abstract or access-limited status.

Coverage included ordinary low-rank approximation, complex/real rank and realification, phase and phaseless rank, Fourier biunimodular vectors and operator norms, finite-abelian uncertainty, and Hadamard real entries/defect terminology. Search-generated summaries, AI summaries, third-party overview sites, and unverified search snippets were not used as primary proof evidence. The original Eckart–Young endpoint returned an internal error; the Mirsky publisher body was unavailable; a Donoho–Stark scan supplied no readable body through the available returned representation. No repeated retrieval campaign or access-bypass route was used.

This does not cover all books, languages, theses, historical journals, citation descendants, matrix completion terminology, or unpublished work. A publication-priority decision would need a broader targeted historical search, especially for the exact pairing identity and the complete rephased invariant. None of those outstanding searches changes the direct-corollary calculations above.

No external write, upload, commit, ranking edit, source edit, fusion, or submission was performed. Only the requested local audit files were created.
