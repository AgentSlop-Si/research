# Phase 44 — Sparse-inverse barrier and exact full 8-point Fourier factorization

**Research date:** October 11, 2026. **Scope:** Theorems concern particular matrix circuit families. The first two are general mathematical derivations. The third is a computer-assisted **exact finite-size existence theorem**, certified by interval arithmetic. It is not a sub-\(N\log N\) Fourier transform for arbitrary \(N\), and priority/publication novelty has **not** been established.

## 0. Definitions

Let \(N\ge 2\), \(\omega_N=e^{-2\pi i/N}\), and \(F_N=(\omega_N^{rj})_{0\le r,j<N}\) denote the unnormalized complex DFT. Let \(W\) be a weighted directed Hamiltonian-cycle shift: \(W e_{v_j}=w_{j+1}e_{v_{j+1}}\), where all weights are nonzero and \(h=\prod_jw_j\ne1\). Its Green resolvent \(G_W=(I-W)^{-1}\) is well defined and can be applied in \(O(N)\) field operations once the weights are supplied.

A *one-layer* \(q\)-Green sum is \(S=\sum_{s=1}^q\alpha_sG_{W_s}\) with arbitrary complex coefficients \(\alpha_s\). Outer *monomial equivalence* to \(F_N\) permits arbitrary row and column permutations and nonzero row/column diagonal scalings. It does NOT permit arbitrary dense external transforms.

**Arc signature lemma (Phase 43, included here for clarity).** Given \(m\) selected rows, the restricted column of a single Hamiltonian Green resolvent has at most \(m\) distinct projective directions. For a sum of \(q\) Greens, grouping columns by their \(q\) arc signatures yields at most \(m^q\) groups, each spanning dimension at most \(q\) on those \(m\) rows. The underlying entry identity for one cycle is

\[
(G_W)_{v_a,v_b}=\frac{\beta_a}{\beta_b}\frac{h^{[a<b]}}{1-h},\qquad \beta_a=\prod_{t=1}^{a}w_t,\quad\beta_0=1.
\]

**Fourier full-spark lemma.** For any \(m\le N\) consecutive Fourier frequencies (in cyclic order), the \(m\times N\) Fourier submatrix has every collection of \(m\) distinct columns independent. To see this, factor out a nonzero root of unity depending on the first selected row, leaving columns \((1,z,z^2,\ldots,z^{m-1})^T\) at distinct nodes \(z=\omega_N^j\). Thus any \(k\le m\) columns are independent. This persists under all outer monomial equivalences.

## Theorem 44.1 — bounded-degree sparse right inverse amplifies the Phase 43 obstruction

Suppose \(A\in\mathbb C^{N\times N}\) is invertible; every column of \(A\) has at most \(\rho\) nonzero entries; and every row of \(A\) has at most \(\kappa\) nonzero entries, with positive integers \(\rho,\kappa\). Let \(D\) be any invertible diagonal. If

\[
M=SDA^{-1},\qquad S=\sum_{s=1}^q\alpha_s (I-W_s)^{-1}
\]

is monomially equivalent to \(F_N\), then

\[
\boxed{N\le q\bigl(1+\rho(\kappa-1)\bigr)\bigl[\rho(q+1)\bigr]^q.}
\]

In particular, for fixed \(\rho,\kappa\), full Fourier representations of this type require \(q=\Omega(\log N/\log\log N)\) as \(N\to\infty\).

**Proof.** It is enough to consider \(N\) larger than the stated upper bound, which ensures \(N\ge m=\rho(q+1)\). Select the \(m\) physical output rows corresponding under the alleged row permutation to \(m\) consecutive Fourier frequencies. By the arc-signature lemma, the \(m\)-row columns of \(SD\) partition into at most \(m^q\) classes, with each class of rank at most \(q\). Right multiply the assumed equality \(M=SDA^{-1}\) by \(A\), obtaining \(MA=SD\).

A column of \(MA\) is a linear combination of at most \(\rho\) columns of \(M\), at positions in the support of that column of \(A\). Choose \(q+1\) columns of \(A\) with pairwise disjoint nonempty supports. Their products under the \(m\) selected rows of \(M\) are independent: all the involved Fourier columns number at most \(\rho(q+1)=m\) and are independent; their coefficient vectors are nonzero and supported on disjoint sets.

Within any signature class, choosing one column eliminates at most \(\rho(\kappa-1)\) other columns whose supports intersect its support, because each support row occurs in at most \(\kappa\) columns. A greedy independent-set selection therefore gives \(q+1\) disjoint-support columns if the class contains more than \(q(1+\rho(\kappa-1))\) columns. That would produce \(q+1\) independent columns in the same at-most-\(q\)-dimensional restricted span of \(SD\), a contradiction. Thus every class has at most \(q(1+\rho(\kappa-1))\) columns; there are at most \(m^q\) classes. The bound follows. □

**Recovery of Phase 43:** when \(A\) is monomial, \(\rho=\kappa=1\), and the result recovers \(N\le q(q+1)^q\).

## Theorem 44.2 — sharper two-layer bound when the right stage is one cycle

Let \(W_0\) be another arbitrary invertible-holonomy weighted Hamiltonian cycle, and let \(S\) be any \(q\)-Green sum as in Theorem 44.1. If

\[
\boxed{M=SD(I-W_0)^{-1}}
\]

is monomially equivalent to \(F_N\), then

\[
\boxed{N\le 2q[2(q+1)]^q.}
\]

Here \(D\) may have **arbitrary nonzero complex amplitudes and phases**, not only unit phases; the graph cycles and internal edge weights may be arbitrary and independently permuted.

**Proof.** Choose \(m=2(q+1)\) consecutive Fourier output frequencies and the corresponding physical rows. The identity \(M(I-W_0)=SD\) says that the column indexed by a vertex \(j\) on the right-hand Hamiltonian cycle equals \(M_{:,j}-a_jM_{:,\pi(j)}\) for a nonzero weight \(a_j\) and its successor \(\pi(j)\). Color edge \(j\to\pi(j)\) by the at-most-\(m^q\) Green-arc signature of column \(j\) of \(S\). If \(q+1\) edges of the same color are vertex-disjoint, then their Fourier differences are independent on the selected \(m=2(q+1)\) rows, because their supports are disjoint and involve at most \(m\) independent Fourier columns. But the same columns of \(SD\) lie in a fixed span of dimension \(q\), contradiction.

Any subset \(E\) of the \(N\)-cycle edges that is not the entire cycle decomposes into paths. In each path, taking alternate edges produces a matching of size at least \(|E|/2\) (rounding up per path). If the entire cycle has more than \(2q+1\) edges it too has a matching of at least \(q+1\) edges. Therefore, at \(N>2q[2(q+1)]^q\), **each signature color occurs on at most \(2q\) edges**. Summing over at most \(m^q\) colors gives \(N\le2qm^q\), contradiction. □

| Left Green terms \(q\) | Rigorous two-layer upper bound on \(N\) |
|---:|---:|
| 1 | 8 (improved to **4** by the sparse-inverse support argument below) |
| 2 | 144 |
| 3 | 3,072 |
| 4 | 80,000 |

**Simple stronger special case \(q=1\).** If \(M=G_2DG_1\) has only one Green per stage and is invertible, then

\[
M^{-1}=(I-W_1)D^{-1}(I-W_2)
\]

has at most four nonzeros in each row, since both \(I-W_i\) have at most two nonzeros per row. The inverse of every monomially equivalent Fourier matrix has **no zero entries**, so \(N\le4\). More generally, the inverse of a product of \(d\) single Green resolvents with diagonal interstages has at most \(2^d\) nonzeros per row; thus such a network needs \(d\ge\lceil\log_2N\rceil\) to represent Fourier. This does **not** apply to sums of two or more Greens at each layer.

**Exact finite-field checks.** `phase44_witness.py` tests \(q=1,2,3,4\) beyond the respective bounds, at \(N=16,256,4096,131072\), in each of two prime fields. A signature class containing \(q+1\) pairwise vertex-disjoint cycle edges is extracted, and the associated \(m\times(q+1)\) submatrix has rank \(q+1\) on the Fourier side but at most \(q\) on the summed-Green side. The script checks the matrix identity \((SDG_0)(I-W_0)=SD\) independently at \(N=8\). These finite-field examples are demonstrations of the argument; the proof is universal over \(\mathbb C\).

## Theorem 44.3 — exact FULL 8-point DFT using four three-Green stages

Consider the architecture

\[
M=S_3D_2S_2D_1S_1D_0S_0,\qquad
S_\ell=\sum_{t=0}^{2}\bigl(I-W_{\ell,t}\bigr)^{-1},
\]

where the twelve cycles in `phase44_multistage_rank.py:specs(8,4)` have precisely the fixed orders generated by the committed seeds; each internal cycle's spanning-tree gains are 1; remaining chord gains are \(e^{i\theta}\) for real angles \(\theta\); and each interstage diagonal is \(D_\ell=\operatorname{diag}(1,e^{a_1+i\phi_1},\ldots,e^{a_7+i\phi_7})\) for real \(a,\phi\). There are 110 real variables in this gauge-fixed parameterization.

**Existence claim.** There exist real parameters for this exact finite architecture and nonzero external diagonal matrices \(L,R\) such that

\[
\boxed{F_8=L M R}\tag{44.3}
\]

**Computer-assisted proof.** Let \(f:\mathbb R^{110}\to\mathbb R^{98}\) be the real and imaginary parts of all the 49 complex projective Fourier conditions

\[
f_{r,j}(x)=\frac{M_{r,j}(x)M_{0,0}(x)}{M_{0,j}(x)M_{r,0}(x)}-\omega_8^{rj},\qquad 1\le r,j\le7.
\]

The frozen certificate `phase44_full_N8_box.json` specifies exact rational-decimal values for 12 coordinates, exact rational-decimal center values for the other 98 coordinates, and an exact rational-decimal \(98\times98\) preconditioner \(B\). Denote the 98 variable coordinates by \(t\), the resulting square function by \(g(t)\), and the closed box of max-radius \(r=10^{-20}\) around the saved center by \(\mathcal B\).

A separate interval verifier (`phase44_full_interval.py`, 55 decimal digits, all complex trigonometric/exponential operations enclosed by outward intervals) establishes the following **strict inequalities**:

\[
\boxed{\|B g(t_0)\|_\infty\ <2.265\times10^{-47},\qquad
\sup_{t\in\mathcal B}\|I-BDg(t)\|_\infty<4.706\times10^{-8}.}
\]

The actual verifier compares outward intervals directly against stronger convenient rational thresholds \(r/4\) and \(1/2\); the displayed decimal numerical upper bounds are diagnostics, not the logical check. Hence the Banach map \(T(t)=t-Bg(t)\) maps \(\mathcal B\) into itself and is a contraction. It has a fixed point. Because \(I-BDg\) has operator norm less than 1, \(BDg\) is invertible throughout the box, so \(B\) itself is invertible. The fixed point therefore satisfies \(g(t)=0\).

At that root all denominators in \(f\) are nonzero (ensured by interval evaluation) and all Green holonomies remain different from 1. Take \(L_{r,r}=M_{0,0}/M_{r,0}\) and \(R_{j,j}=1/M_{0,j}\); then the exact projective conditions give \(LMR=F_8\) entrywise. This proves (44.3), rather than merely numerical approximation. □

The **higher precision independent rerun** at 80 interval decimal digits and radius \(10^{-21}\) passes too, with a reported contraction upper bound of \(5.246\times10^{-9}\). It is preserved in `phase44_full_N8_interval_80dps_audit.json`.

**Executor independent verification.** The approximate center parameters, rounded to ordinary double precision, support a *matrix-free* online implementation with 12 cyclic Green solves and three interstage complex diagonals. Comparing it against NumPy FFT on twelve random complex input vectors yields maximum absolute output error \(8.6\times10^{-13}\). This numerical test is independent of the existence proof. The linear-time online cost applies to fixed-size fixed-depth supplied gains; no all-length FFT complexity claim is implied.

## Theorem 44.4 — local full-matrix reachability and its parameter-count limitation

For \(d\) independent stages summing three **unit-edge** weighted cycles each, using fully complex diagonal interstages, the gauge-fixed model has

\[
P(d,N)=d(2N+1)+2(d-1)(N-1)=d(4N-1)-2(N-1)
\]

real internal parameters (with external row/column scalings factored out). The target space of complex matrices having nonzero entries modulo row/column diagonal scalings has real dimension \(2(N-1)^2\). Therefore generic full-projective local reachability is **impossible** unless

\[
\boxed{d\ge\left\lceil\frac{2N(N-1)}{4N-1}\right\rceil.}
\]

This is a **dimension condition for generic targets**, not a Fourier-specific lower bound. The special Fourier target might lie in lower-dimensional images.

Using four independent Green-sum stages at \(N=8\) and eight stages at \(N=16\), both generated by `specs(N,d)`, the full real Jacobians attain the respective target maximum ranks:

| Size \(N\) | Stages \(d\) | Real variables | Real output dimension | Verified Jacobian rank |
|---:|---:|---:|---:|---:|
| 8 | 2 | 48 | 98 | 48 |
| 8 | 3 | 79 | 98 | 79 |
| **8** | **4** | **110** | **98** | **98** |
| **16** | **8** | **474** | **450** | **450** |

Every rank was obtained independently modulo \(998244353\) and \(2013265921\) by constructing the real/imaginary Jacobian at rational-Gaussian unit-circle points, evaluating its rational entries in both embeddings of \(i\), and reducing its rank. Therefore these are exact characteristic-zero **local-rank certificates**. By the submersion theorem, each of the last two models reaches an open set of complex full-matrix projective targets near the corresponding test points.

**Important:** At \(N=16,d=8\), this proves only an open-set statement. Direct attempts to solve the **specific \(F_{16}\)** target have **not succeeded** (saved log target residual is large), and there is no proof of exact Fourier membership there. The exact full Fourier target is certified at \(N=8\) only.

## Complexity, publication status, and Phase 45 target

One weighted cyclic resolvent is applied using a cyclic first-coordinate solve followed by a forward recurrence in \(O(N)\) arithmetic. Consequently, \(d\) three-Green stages cost \(O(3dN)\) online, **when graph orders, weights, and external calibrations are already supplied**. The finite exact theorem uses \(d=4\) only at \(N=8\). The demonstrated generic full-rank pattern \(d\approx N/2\) would cost \(O(N^2)\) if naively extended; it **does not** beat the FFT. Parameter synthesis, precision, conditioning, and uniform families are not solved.

Prior art on sparse matrix factorization and Fourier butterfly decompositions is substantial; independent literature novelty and peer review remain pending. In particular see Ben Lee Volk et al., *Lower Bounds for Matrix Factorization* (CCC 2020, DOI: 10.4230/LIPIcs.CCC.2020.5), and butterfly-factorization works. None of those references establishes priority for this exact weighted-Green finite-size representation; nor did we find enough evidence to claim it is a literature-first result.

**Next mathematical gate:** Either (i) certify full \(F_{16}\) membership at an architecture with a manageable number of Green stages, or (ii) discover a **uniform, structured** family with \(d=O(1)\) and constant Green count, including a rigorous input-independent parameter synthesis method. Do **not** mistake increasing \(d\sim N/2\) for an asymptotic FFT improvement.
