# Phase 41 — unit-circle Green rigidity and three-cycle local phase freedom

**Date:** October 10, 2026. **Status:** One uniform restricted impossibility theorem; exact finite-field certificates of real/complex local Jacobian ranks; numerical partial Fourier synthesis. **NOT a new sub-`N log N` FFT or integer-multiplication bound.**

## 1. Setup, field of validity, and conventions

An ordered Hamiltonian cycle is represented by its weighted cyclic permutation matrix \(W\), with the nonzero entry at directed edge \(u\to v\) equal to \(w_{vu}\). It is an *admissible Green cycle* if the product \(H=\prod w_{vu}\ne1\). Then

\[
G_W=(I-W)^{-1}=\frac{I+W+\cdots+W^{N-1}}{1-H}.
\]

If every edge gain has modulus one, \(W\) is unitary and every Green entry is nonzero and has the same modulus \(1/|1-H|\): each entry of the numerator is the weight of exactly one directed path from its input vertex to its output vertex. No bounded-conditioning assumption is imposed.

The DFT is \(F_N=[\omega^{ij}]\), \(\omega=e^{2\pi i/N}\), without normalization. We allow arbitrary **external** row/column permutations and invertible complex diagonal scalings. They preserve anchored cross-ratios.

## 2. Exact all-length two-unit-cycle obstruction

**Theorem 41.1.** Suppose \(G_1,G_2\) are admissible weighted Hamiltonian-cycle Green inverses, all edge gains have absolute value one, and \(a,b\in\mathbb C\). For every \(N>8\), there are no invertible diagonal matrices \(L,R\) and permutation matrices \(P,Q\) such that

\[
F_N=LP(aG_1+bG_2)QR.
\]

This holds for independently chosen cycle orders, arbitrary unit edge phases, arbitrary complex scalar coefficients \(a,b\), and arbitrarily ill-conditioned admissible resolvents. It does *not* apply to non-unit edge amplitudes, three or more Green summands, or products of such sums.

**Proof.** Let \(G=(I-W)^{-1}\). For any two different output rows \(u,v\), the ratio \(G_{u,j}/G_{v,j}\) takes **at most two distinct values** as input column \(j\) varies. Indeed, cancel the common directed path from \(j\) until the cycle first reaches one of \(u,v\). The remaining multiplier is either the path product from \(v\) to \(u\), or the reciprocal of the path product from \(u\) to \(v\). Both have absolute value one because the individual edge gains do.

Fix any row pair \(u,v\). For each cycle \(s=1,2\) write \(r_{s,j}=G_s[u,j]/G_s[v,j]\in\mathbb T\), with at most two choices as \(j\) varies. Also set \(G_s[v,j]=g_s t_{s,j}\), where \(g_s=1/|1-H_s|>0\) and \(|t_{s,j}|=1\). For a fixed pair \((r_1,r_2)\) of row-ratio signatures, let \(A=ag_1\), \(B=bg_2\) and \(t_j=t_{2,j}/t_{1,j}\in\mathbb T\). Then the ratio of the two rows of the sum is

\[
\frac{(aG_1+bG_2)_{u,j}}{(aG_1+bG_2)_{v,j}}
 =\phi(t_j)=\frac{A r_1+B r_2 t_j}{A+B t_j}.
\]

There are at most \(2\cdot2=4\) different signatures. Suppose the whole matrix is externally equivalent to the DFT. Then for these two rows the modulus of their ratio is the same constant \(K>0\) at every column (DFT entries are flat in magnitude, and external row/column scalings cancel in each row ratio). For one fixed signature,

\[
(1-K^2)(|A|^2+|B|^2)
 +2\operatorname{Re}\!\left[\overline A B(\overline{r_1}r_2-K^2)t\right]=0,
\qquad |t|=1.
\]

If \(A=0\) or \(B=0\), or if \(r_1=r_2\), the ratio \(\phi\) is constant. Otherwise the displayed equation is nontrivial: if it vanished identically, averaging over the circle forces \(K=1\), after which the cross coefficient forces \(r_1=r_2\), a contradiction. A nontrivial equation of the form \(c+2\Re(dt)=0\) has at most two solutions on the unit circle. Thus, within each signature, at most two distinct complex row-ratio values survive the constant-modulus condition. Across all signatures there are **at most eight** distinct row ratios.

For the Fourier transform choose two adjacent frequency rows, whose ratio is \(\omega^j\) or \(\omega^{-j}\); it takes \(N\) distinct values over the columns. Arbitrary row/column permutations or nonzero diagonal scalings cannot change this count for the corresponding row pair. For \(N>8\) this contradicts the eight-value bound. \(\square\)

**Interpretation:** This is stronger than a random-instance phase mismatch, but *much narrower* than a general Fourier complexity lower bound. It is a new proved result in this project; its independent publication novelty has not been established.

## 3. A strict real-dimensional phase-only local bound

Fix scalar coefficients \(a=b=1\), rows 0 and 1, and anchor columns \(0,1,\ldots,k\), with \(k\ge2\). Define the \(k\) anchored projective ratios

\[
R_j=\frac{M_{0j}M_{10}}{M_{1j}M_{00}},\qquad j=1,\ldots,k.
\]

**Theorem 41.2.** When both cycles have unit-modulus edge gains, the real differential rank of the map from all edge phases to these \(k\) complex ratios is at most

\[
\boxed{\min(2k,k+2)}.
\]

**Proof.** Apply a common *unitary* vertex-diagonal conjugation to put the first cycle into canonical form with only its closing holonomy \(H_1\ne1\) free. The second cycle has closing holonomy \(H_2\ne1\) and potential vector \(d=(d_0,\ldots,d_{N-1})\), whose common scalar is irrelevant. Set \(d_1=1\). For entries on rows \(0,1\) and columns \(0,\ldots,k\), only \(H_1,H_2,d_0,d_2,\ldots,d_k\) occur. These are **\(k+2\) independent real circle parameters**. The anchored ratios are invariant under the common diagonal conjugation. A smooth map factoring through a \((k+2)\)-real-dimensional torus has differential rank at most \(k+2\), and the output space has dimension \(2k\). \(\square\)

**Qualification:** The rank bound counts the scalar coefficients as **fixed**. If their relative complex scalar is another adjustable parameter, it can add up to two further real degrees of freedom. Theorem 41.1, unlike this local theorem, already allows arbitrary coefficients.

The bound is attained for the project's fixed graph orders and explicit rational-Gaussian *unit-circle* chord gains, in independently audited split-prime reductions:

| N | k=2 (real rank) | k=3 | k=4 |
|---:|---:|---:|---:|
| 8 | 4 | 5 | 6 |
| 16 | 4 | 5 | 6 |
| 32 | 4 | 5 | 6 |
| 64 | not separately saved | not separately saved | 6 |

Each chord gain is \(w_e=(a_e+i b_e)/(a_e-i b_e)\in\mathbb Q(i)\) and has modulus one over \(\mathbb C\). The derivative in its phase is \(i w_e\partial/\partial w_e\). The real and imaginary derivative coefficients belong to \(\mathbb Q\). Evaluating \(i\) at its two split-prime embeddings \(\pm\sqrt{-1}\), then taking \((z+\bar z)/2\) and \((z-\bar z)/(2i)\), yields a rational real Jacobian reduced modulo each prime. A nonzero minor in either valid reduction proves the corresponding exact rational determinant is nonzero. See `phase41_unit_jacobian_certificates.json` for the actual minors and residues.

This *falsifies* a tempting inference from Phase 40: the complex rank-four Jacobian for freely varying complex edge gains **does not** imply an 8-real-dimensional local image when gains are constrained to unit modulus.

## 4. Three unit-phase Green cycles escape the local dimension barrier

Three independently ordered cycles contain \(3N\) edge phases. A common vertex gauge eliminates \(N-1\), leaving **\(2N+1\) independent phase holonomies**. A full anchored two-row signature has \(N-1\) complex ratios, i.e. \(2N-2\) real target coordinates.

**Theorem 41.3 (finite-size local controllability).** For the specifically recorded three-cycle orders at \(N=8,16,32,64\), the real Jacobian of the map

\[
(\mathbb S^1)^{2N+1}\longrightarrow\mathbb C^{N-1},\qquad
h\longmapsto(R_1,\ldots,R_{N-1})
\]

has **full real rank \(2N-2\)** at a specified rational-Gaussian unit-circle gain assignment. Nonzero full-row-rank square minors were verified independently modulo 998244353 and 2013265921 and consequently lift to nonzero rational minors in characteristic zero. Therefore, by the real submersion theorem, the image of the phase-only map contains an ordinary Euclidean-open subset of the possible \(N-1\) complex row-pair ratios at each certified size.

| N | Independent phase holonomies | Real target dimension | Certified real rank |
|---:|---:|---:|---:|
| 8 | 17 | 14 | 14 |
| 16 | 33 | 30 | 30 |
| 32 | 65 | 62 | 62 |
| 64 | 129 | 126 | 126 |

This is a **local** theorem. It does not prove the particular Fourier target is in that open image, does not show a three-cycle full-DFT factorization, and does not provide an efficient construction of exact target gains. Numerical fits did match all \(N-1\) target ratios for the first two Fourier rows at \(N=8,16,32\), but the third row failed in every case. Those fits are evidence only and are not exact root certificates.

## 5. Allowing amplitude: full complex local freedom from two cycles

**Theorem 41.4 (finite-size complex local controllability).** For the recorded orders at \(N=8,16,32,64,128\), if all nonzero complex edge gains are allowed, the Jacobian of all \(N-1\) anchored row-pair ratios with respect to the \(N+1\) complex chord parameters has full complex rank \(N-1\), independently checked at two split primes. Consequently the rational map is dominant over \(\mathbb C\) for these fixed orders. This follows from the characteristic-zero Jacobian criterion for rational maps.

A separate nonlinear search matched the *specific* target \(R_j=\omega^{-j}\) for every \(j=1,\ldots,N-1\) at \(N=8,16,32\), with max component residual around \(10^{-11}\). At \(N=8,16\), high-precision complex Newton corrections reduced residuals below \(10^{-80}\). **These remain numerical root evidence, not a validated interval/exact existence proof.** At \(N=32\), the resulting full mixing matrix was significantly ill-conditioned. Its third Fourier row is still wrong.

### An exact Möbius escape template (not yet embedded into a Green circuit)

If unit-gain equality \(|r_1|=|r_2|=1\) is relaxed, a nonconstant Möbius map can have a full unit-circle image. For example

\[
\phi(t)=\frac{2+\tfrac12t}{1+t},\qquad
z\in\mathbb T,\quad t=\frac{2-z}{z-\tfrac12}.
\]

Then \(|t|=2\) and \(\phi(t)=z\) exactly, so a suitable *amplitude-asymmetric* local row-pair mixer can supply arbitrarily many desired Fourier phases with one scalar per column. This is only a local algebraic **template**; the \(t_j\) have not been shown to arise simultaneously from a consistent family of weighted Green cycles that computes the DFT.

## 6. Full Fourier verification and costs

For every numerical partial synthesis, dephase the mixing matrix by

\[
\widetilde M_{ij}=\frac{M_{ij}M_{00}}{M_{i0}M_{0j}}.
\]

The first two Fourier rows match to roughly \(10^{-11}\), but the next row has order-one or larger error (see `phase41_full_audit.json`). Nothing passes the complete Fourier Weyl equations. The online application cost of two or three weighted Hamiltonian Green solves is \(O(N)\) **given** all edges and normalization constants. Our synthesis fits require expensive offline nonlinear computation, depend separately on \(N\), and have no uniform exact construction/bit-complexity or numerical stability analysis. They do not constitute an FFT complexity improvement.

## 7. Research gate for Phase 42

- Study whether a **uniform explicit** three-cycle unit-phase construction can satisfy several *different* Fourier row pairs at once. The Phase 41 two-row Jacobian rank is not a guarantee of coherence across all rows.
- Analyze whether the two-cycle amplitude-asymmetric Möbius template can be embedded into a globally consistent Green network with bounded amplitudes and cheap parameter generation.
- Demand \(MZ=DM\), \(MD=Z^{-1}M\), normalization, and a proof for every \(N\). Account for the time required to construct exact weights, their bit lengths, and all memory movement.
- Prior art: Fourier/Hadamard projective equivalence and complex ratio invariants are established; the project-specific eight-value result and exact Jacobian certificates require independent literature review before claiming publication originality.
