Public source-text preservation. This is the submitted theorem, with the one source-program reproduction direction replaced as recorded in [the transformation manifest](../../SOURCE_EXPORT_TRANSFORMS.json). Read [the accepted restricted audit](../../reviews/03_phase_cone.md): gain-graph switching is classical; O(N+q) charges discrete preprocessing only; rigorous threshold certification and magnitude validation carry separate costs. Prior unitary-collinear and complex phase-averaging theorems retain their accepted scopes. Source-reported tests are historical. No source programs are included, and preserving this text is not a universal FFT lower bound or priority certification.

# Spectral Phase-Cone Rigidity for Fourier and Green Networks

**October 10, 2026 — research manuscript / proof candidate for independent review**

## Executive statement

We derive a conditioning-independent spectral obstruction for attempting to realize a normalized discrete Fourier transform by *positive real mixing stages* separated by a bounded total angular budget of complex diagonal phase masks. The bound applies to any number of such stages, arbitrary non-affine Hamiltonian-cycle orderings, and arbitrary complex input/output monomial gauges. Unlike a single-Green inverse-sparsity theorem, it remains applicable when the **full circuit has a dense inverse**. Unlike the earlier Phase 22 connected-Gram obstruction, it allows **several internal complex phase masks** and proves an explicit **operator-norm approximation gap**.

**No universal exact `O(N)` FFT or global publication novelty is claimed.** All claims below refer to the stated cone-constrained architecture.

## 1. Definitions

For `N >= 2`, let `U_N` be the **normalized** DFT

\[
(U_N)_{jk}=N^{-1/2}e^{-2\pi i jk/N},\qquad 0\le j,k<N.
\]

Let `K(theta,phi)` be the closed circular cone (including zero) of complex numbers whose arguments lie in the arc `[phi-theta,phi+theta]`, where `0 <= theta < pi/2`:

\[
 K(\theta,\phi)=\{r e^{i\alpha}:r\ge0,\ |\alpha-\phi|\le\theta\}.
\]

A matrix `C` has **phase width at most `W`** if all its entries belong to the same rotated cone `K(W/2,phi)`. The cone is convex when `W < pi`.

An **outer monomial gauge** is an invertible matrix formed from a permutation and a nonzero diagonal. We allow different monomial gauges on both sides.

## 2. Core theorem: stable phase-cone rigidity

**Theorem 1.** Let `N >= 2`, and let `C in C^{N x N}` have phase width at most `W < pi`. For any two invertible complex monomial matrices `L,R`, put `M=L C R`. Then, writing `epsilon = ||M-U_N||_2` and `c=cos(W/2)>0`,

\[
 \boxed{\varepsilon\ \ge\ \max\left\{0,\frac{c\sqrt N-1}{c\sqrt N+1}\right\}.}\tag{2.1}
\]

Here `||.||_2` is the operator norm induced by the Euclidean norm. The bound is **independent of** (i) the condition numbers of `L,R,C`, (ii) the entries of the underlying Green matrices, and (iii) the input/output permutations.

It also holds with `U_N` replaced by **any flat unitary matrix** (every entry has modulus `1/sqrt(N)`). The proof uses only flatness and unitarity.

### Proof

Strip off the permutation and **unit-modulus** parts of the outer monomial factors using unitary left/right transformations. After these transformations, `M` becomes a matrix `Q=D_1 C D_2`, where `D_1,D_2` are positive diagonal matrices, while `U_N` becomes another flat unitary matrix `H`. These unitary transformations preserve the spectral error `epsilon`. Multiplying both matrices by a common scalar phase if necessary, assume every entry of `Q` lies in `K(W/2,0)`, so

\[
 \Re Q_{jk}\ge c|Q_{jk}|.
\]

Write `E=Q-H`. Unitarity gives `||H||_2=1` and `|1^T H 1| <= N`. The error bound `||E||_2 = epsilon` implies both

\[
 |1^T E 1|\le N\varepsilon,
 \quad \|E\|_F\le\sqrt N\varepsilon,
 \quad \sum_{jk}|E_{jk}|\le N\|E\|_F\le N^{3/2}\varepsilon.
\]

Flatness gives `sum_{jk}|H_{jk}|=N^{3/2}`, so the triangle inequality yields

\[
 \sum_{jk}|Q_{jk}|\ge N^{3/2}(1-\varepsilon).
\]

Since each entry of `Q` lies in the same cone,

\[
 c N^{3/2}(1-\varepsilon)
 \le c\sum_{jk}|Q_{jk}|
 \le \Re(1^TQ1)
 \le |1^TH1|+|1^TE1|
 \le N(1+\varepsilon).
\]

If `c sqrt(N) <= 1`, (2.1) is trivial. Otherwise rearrange to obtain

\[
 \varepsilon\ge\frac{c\sqrt N-1}{c\sqrt N+1}.
\]

This also holds for `epsilon >= 1`, when the right-hand side is strictly below 1. QED.

### Exact case and required phase spread

If `M=U_N`, Theorem 1 forces

\[
 \boxed{W \ge 2\arccos(N^{-1/2}).}\tag{2.2}
\]

As `N` grows,

\[
 2\arccos(N^{-1/2})=\pi-2N^{-1/2}+O(N^{-3/2}).
\]

Thus a Fourier realization requires an entrywise phase span approaching **180 degrees**, even after arbitrary row/column complex scalings and permutations.

For a target spectral error `0 <= epsilon_0 < 1`, we must have

\[
 \boxed{\cos(W/2)\le\frac{1+\varepsilon_0}{\sqrt N(1-\varepsilon_0)}.}\tag{2.3}
\]

Equivalently, if the right side is less than 1, the minimum phase width is

\[
 W\ge 2\arccos\left(\frac{1+\varepsilon_0}{\sqrt N(1-\varepsilon_0)}\right).
\]

**Uniform stability consequence:** For every fixed `W <= pi - eta` with `eta>0`, every such architecture satisfies `liminf_{N->infty}||M_N-U_N||_2>=1` (not a claim that the error equals 1). In fact (2.1) approaches 1 from below as `1-O(N^{-1/2})`.

### Independent exact proof for epsilon=0

With `Q=H` flat unitary, let `e=N^{-1/2}(1,...,1)^T`. Each row of `H` has inner product with `e` of absolute value at least `c`. As the rows of `H` are an orthonormal basis, Bessel's identity gives

\[
 1=\sum_{j=0}^{N-1}|\langle H_{j,:},e\rangle|^2\ge Nc^2.
\]

Hence `W>=2 arccos(1/sqrt(N))` without using the approximation argument.

The exact threshold is attained at `N=2`: the rephased Fourier matrix

\[
 2^{-1/2}\begin{pmatrix}1&i\\i&1\end{pmatrix}
\]

has phase width `pi/2`. The lower bound is **not claimed sharp for Fourier matrices at higher N**.

## 3. A multistage phase-budget theorem

**Lemma 2 (phase-cone preservation).** Let `A_0,...,A_t` be real, entrywise nonnegative matrices of compatible dimensions. For `j=1,...,t`, let `D_j` be a diagonal matrix whose nonzero entries have phases lying in some arc of width `w_j`. Put `W=sum_j w_j` and assume `W<pi`.

Then every entry of

\[
 C=A_0D_1A_1D_2\cdots D_tA_t
\]

lies in a **single** complex sector of width at most `W` (the angular sum of the chosen arcs). This remains true when every `A_j` is a sum of any number of real nonnegative matrices, including differently permuted weighted cyclic Green operators.

**Proof.** Expand every entry as a sum over intermediate path indices. Each summand is a nonnegative real scalar times a product of one diagonal entry from each `D_j`. Its argument lies in the sum of the selected arcs, an interval of width `W<pi`. That angular sector is a convex cone, so all nonnegative sums remain inside it. QED.

**Theorem 3 (multimask Fourier phase budget).** Under Lemma 2, for arbitrary invertible complex outer monomial gauges `L,R`,

\[
 \boxed{\|L A_0D_1A_1\cdots D_tA_t R-U_N\|_2
 \ge \max\left\{0,\frac{\sqrt N\cos(W/2)-1}{\sqrt N\cos(W/2)+1}\right\}.}\tag{3.1}
\]

For **exact** Fourier equality, the **sum** of internal phase-mask arc widths must satisfy

\[
 \boxed{\sum_j w_j\ge2\arccos(N^{-1/2})}\tag{3.2}
\]

whenever their sum is less than `pi` (when the sum is at least `pi`, the necessary inequality is automatically satisfied, but no sector estimate follows).

This counts angular phase diversity rather than arithmetic operations. The number of masks may grow with `N`; no bound on the number of positive mixing stages is required.

## 4. Specialization to four Green branches

For a Hamiltonian-cycle permutation `P` and a positive weighted shift `T=diag(w)P`, assume `prod_i w_i<1`. Then `T^N=pI` and

\[
 (I-T)^{-1}=\frac{I+T+\cdots+T^{N-1}}{1-p}
\]

has **strictly positive real entries**. Its application uses an `O(N)` recurrence. Permuting input/output indices and multiplying by positive diagonal weights preserves entrywise positivity. Thus

\[
 A=G_1+G_2,\quad B=G_3+G_4
\]

are positive even with independent, non-affine Hamiltonian cycles. With a single middle phase mask `D`, the formula

\[
 M=L A D B R
\]

satisfies (2.1), where `W` is the shortest arc containing the phases of `D` (provided `W<pi`). **No assumption that `A` is nearly monomial, that one Green branch dominates, or that `A,B` have bounded condition numbers is needed.**

The `t>=2` theorem applies to products of several such positive Green sums with multiple phase masks. Such products may have a **fully dense inverse**, so the previously proved inverse-footprint theorem does not automatically apply.

## 5. Why a wide phase budget is necessary but not sufficient

If all internal masks have values on one real line (for example all entries `+1` or `-1`), then the middle core is real, possibly signed. All of its nonzero 2x2 cross-ratios are real and stay real under arbitrary complex row/column diagonal gauges. For `N>=3`, the Fourier cross-ratio of rows `(0,1)` and columns `(0,1)` is `exp(-2pi i/N)`, which is non-real. Thus such a circuit cannot equal `U_N` for `N>=3`, even though the `+/-` phases span a *closed* semicircle of width `pi` and evade Theorem 1's narrow-cone condition.

This is the established **projective curvature** invariant from project Phase 20, included here as a complementary requirement rather than claimed as a new result. Widening the mask-phase budget is **necessary, not sufficient**, for exact Fourier phases.

## 6. Quantitative consequences and numerical checks

For `W=0` (positive-real middle core), the lower bound is `(sqrt(N)-1)/(sqrt(N)+1)`.

| N | Minimum exact phase width (degrees) | Bound for W=0 | Bound for W=120 degrees |
|---:|---:|---:|---:|
| 4 | 120.00 | 0.3333 | 0 |
| 8 | 138.59 | 0.4776 | 0.1716 |
| 16 | 151.04 | 0.6000 | 0.3333 |
| 64 | 165.64 | 0.7778 | 0.6000 |
| 256 | 172.83 | 0.8824 | 0.7778 |
| 1024 | 176.42 | 0.9394 | 0.8824 |

The original source reports 84 numerical phase-cone tests, one exact `N=2` control, and 900 random row/column-rephased Fourier matrices checked for minimum phase width. Its programs and archive-inventory tooling are excluded here. See [independent reproduction](../../REPRODUCE.md) for this packet’s fresh controls. Numerical tests corroborate the inequalities; all-length validity rests on the proofs.

## 7. Provenance, prior art, and limitations

**Provenance:**
- Master archive `fft_research_master_20261009.zip`, Phase 20: projective Fourier cross-ratios and Weyl covariance.
- Master archive Phase 22: connected-Gram obstruction for **one** complex diagonal mask between real invertible mixers **without freely complex outer diagonal gauges**, plus positive-Green corollary. This result is stronger than the *exact* phase-budget condition in that narrower one-mask model; it must not be relabeled as new.
- The October 10 `fft_projective_stability_20261010` and `fft_two_cluster_complex_green_20261010` proofs: projective spectral bounds for a nearly monomial stage and a dominant Green branch, respectively.
- The October 10 `fft_stable_inverse_dimension_20261010`: sparse-plus-low-rank inverse spectral barrier; this cannot in general be applied to a product of Green sums having dense inverses.
- This note's **new-to-project** target is the unconditional (on conditioning and stage dominance) *stable phase-budget bound*, extended to **arbitrarily many positive real mixing stages and multiple complex internal diagonal masks**, with **arbitrary complex outer monomial gauges**.

**Prior art:** Flat unitaries/complex Hadamard matrices, phase-gauge equivalence, positive complex cones, matrix-norm inequalities, and Fourier cross-ratio invariants are classical. The proof is elementary enough that the statement may already be implicit in the literature. Targeted web searches as of this checkpoint did not establish publication originality; a dedicated mathematical-literature search and independent review are needed.

**Limitations:**
1. This does **not** prove an exact or approximate `O(N)` FFT construction.
2. It does **not** exclude general four-Green stages with unrestricted complex edge phases or masks whose cumulative phase budget reaches `pi`.
3. It does **not** apply when the mixing stages have arbitrary complex coefficients whose path terms wrap the circle; positivity or a common phase-cone hypothesis is essential.
4. The lower bound is for the **normalized** DFT in complex operator 2-norm, not bit complexity or a finite-field norm.
5. The claimed error floor is a *lower bound*, not an attained optimum for the restricted Green family.

### Source URLs

- OpenAI exact-DFT result #130: https://github.com/openai/math/blob/main/lean/docs/130.md
- T. Banica, *Invitation to Hadamard matrices*: https://arxiv.org/abs/1910.06911
- Source archive references and exact inventory: `SOURCE_AUDIT.md`, `SOURCE_INVENTORY.json`.

## 8. Complex-weighted cycles: the graph-holonomy extension

The preceding theorem is **not limited to globally real-looking coefficients**. Complex weighted Green stages that share a removable vertex-phase gauge can be tested by graph potentials.

### Lemma 4 (phase-cocycle integrability on a union of cycles)

Consider an undirected underlying graph on vertices `{0,...,N-1}` that is the union of several directed Hamiltonian cycles. Give each oriented edge `u -> v` a nonzero complex weight `w_{uv}=|w_{uv}|exp(i phi_{uv})` (multiple edges are allowed). The following are equivalent:

1. There exists a unitary diagonal `H=diag(exp(i theta_u))` so that **all** transformed edge weights `exp(-i theta_u) w_{uv} exp(i theta_v)` are positive real.
2. There is a vertex-phase potential satisfying

   \[ \theta_v-\theta_u\equiv-\phi_{uv}\pmod{2\pi}\quad\text{for all oriented edges}. \]

3. Every closed walk of the **undirected union multigraph** has zero signed total edge phase modulo `2pi`.

**Proof.** The equivalence of (1)–(2) is direct from the transformed edge phase. Summing (2) along any closed walk telescopes, proving (2) implies (3). Conversely, fix a root in each component and integrate the prescribed phase differences along a spanning tree; the closed-walk condition makes every non-tree edge consistent. QED.

For edge phases that are integral multiples of `2pi/q`, a weighted union-find with potentials in `Z/qZ` checks this condition in `O(|E| alpha(N))` amortized operations; a static BFS/DFS checks it in `O(N+|E|)` operations. This is an **exact graph certificate** when the phase labels are represented exactly. Trivial holonomy for *each cycle separately* does **not** imply that their union has zero phase frustration.

### Theorem 5 (holonomy-corrected four-Green phase barrier)

Suppose the two-stage architecture is

\[
 M=L (G_1+G_2)D(G_3+G_4) R,
\]

where every `G_j=(I-T_j)^{-1}` is a weighted cyclic Green inverse. Assume every edge magnitude is positive and the product of edge magnitudes on each cycle is less than 1. Assume the union of the first two Hamiltonian-cycle edge sets admits a common phase potential `H_A` from Lemma 4, and independently that the union of the last two admits a common potential `H_B`.

Then

\[
 G_1+G_2=H_A A_+H_A^{-1},\quad
 G_3+G_4=H_B B_+H_B^{-1},
\]

for **strictly positive** real matrices `A_+, B_+`. Put

\[
 D_{\rm eff}=H_A^{-1} D H_B.
\]

Let `W` be the shortest circular arc width containing the phases of all nonzero diagonal entries of `D_eff`. If `W<pi`, then **for arbitrary complex outer monomial gauges** `L,R`,

\[
 \boxed{\|M-U_N\|_2\ge
 \max\left\{0,\frac{\sqrt N\cos(W/2)-1}
 {\sqrt N\cos(W/2)+1}\right\}.}\tag{8.1}
\]

For exact equality, `W >= 2 arccos(N^{-1/2})`. The theorem remains valid for **non-affine Hamiltonian cycles and genuinely complex-looking edge coefficients**, so long as their edge phases admit the common stage-level gauge. There is **no** assumption that the two cycles have the same ordering.

**Proof.** The common phase potential conjugates each sparse weighted shift `T_j` in the stage into a positive real weighted shift. Inverting `I-T_j` preserves the similarity. By the positive finite geometric-series representation, each real Green inverse is strictly positive. Thus

\[
 M=(L H_A) A_+ D_{\rm eff} B_+(H_B^{-1}R),
\]

which is Theorem 3 with one mask. QED.

### Consequence: what an actual phase escape must change

In the stated four-Green model, a candidate can evade Theorem 5 only by violating at least one of the following **combined** conditions:

- shared phase-potential integrability of either Green pair; or
- a narrow effective interface phase sector (`W<2 arccos(1/sqrt(N))` for exact equality, or the stronger error-dependent threshold for approximation).

Evading this test **does not prove** Fourier compatibility; the separate Weyl identities and quadratic Segre conditions remain essential. The theorem certifies a necessary phase-frustration/budget condition, not a sufficient synthesis rule.

### Exact and numerical checks

`verify_graph_holonomy.py` constructs two genuinely different Hamiltonian cycles per stage with exact phase labels in `Z/17Z`, verifies their common vertex-potential constraints both by a weighted disjoint-set union and independently by BFS, applies all four complex Green inverses, and confirms that dephasing recovers strictly positive sums. It checks the error bound at `N=4,8,12,16,24,32`. A control uses different stage potentials on the two individual cycles: each cycle separately has trivial holonomy, but the combined constraints are inconsistent; both independent graph solvers reject it.

## 9. Near-linear graph/union/histogram rejection oracle

**Theorem 6 (discrete-phase rejection oracle).** In Theorem 5, suppose all directed edge phases and the diagonal phases of `D` are supplied as integer residues modulo `q`, representing multiples of `2pi/q`, where `q=O(N)`. Suppose the four cycle permutations and edge weights (or their positive magnitudes and phase labels) are given explicitly, and each cycle's edge-magnitude product is below 1.

A deterministic algorithm performs **`O(N+q)` modular-word operations** to:

1. test shared phase-potential integrability of each *two-cycle union graph*;
2. if both pass, recover stage vertex potentials modulo `q`;
3. compute all effective phase residues for `D_eff=H_A^{-1}D H_B`;
4. find the shortest circular arc enclosing the effective phases via an `O(q)` occupancy histogram and its largest circular gap.

If the resulting width `W<pi` violates the exact or approximate phase-width requirement from Theorem 5, the algorithm outputs a **sound no-go certificate for the entire network, for all outer complex monomial gauges**, without computing even one dense Green matrix entry.

**Proof.** Both stage union graphs have at most `2N` directed edges on `N` vertices, hence BFS/DFS potential propagation uses `O(N)` operations (or weighted union-find `O(N alpha(N))`). A circular occupancy table has `q` bins; filling it takes `O(N)`, scanning for the largest empty gap takes `O(q)`. Arc width is `2pi times (q-largest_gap)/q`; this is invariant under the global potential additive constants, since those shift every residue equally. Apply Theorem 5 to reject whenever its inequality is violated. QED.

**Representation and computation caveat:** The exact graph and histogram operations are integer arithmetic; evaluating and comparing the final trigonometric inequality may require an algebraic-number/interval certificate if one wants a *machine-checked* zero-error result. The mathematical threshold itself is exact. With arbitrary real phase labels rather than modular labels, sorting them to find the shortest circular arc requires `O(N log N)` comparisons in this simple implementation. This is **linear-work rejection of a restricted circuit family**, not an `O(N)` FFT executor.

### What this contributes relative to the prior archive

The user's Phase 20–26 files already contain full Weyl tests, graph cuts, and projective invariants. The new mechanism combines a **shared phase-holonomy graph test** with an **all-depth phase-cone spectral bound** to reject networks even when graph ranks look sufficient and the inverse is dense. It gives a natural union-find/phase-table precursor to expensive nonlinear gauge-fitting experiments.
