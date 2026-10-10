# Phase 40: projective five-cycle certificates and graph-holonomy synthesis

**10 October 2026 — research checkpoint.**  All exact certificates below are in finite fields with characteristic-zero lifting where explicitly stated. **No general-input sub-\(N\log N\) FFT or faster integer-multiplication algorithm has been found.** This is a restricted Green-circuit analysis, not a universal FFT lower bound.

## 1. The eight-Green architecture

Let \(N=2^m\), and let each \(W_s\) be the cyclic permutation matrix of a prescribed Hamiltonian ordering. Let \(G_s=(I-\alpha_s W_s)^{-1}\), all defined and invertible. We fix the outer two-Green sums \(A,C\) from Phase 39, preserve its middle three \(G_0,G_1,G_2\), and add an independent fourth middle cycle Green \(G_3\), with fixed coupling \((2+3i)/13\). The **only** variable middle coefficients are \(\lambda,\mu,\rho\):

\[
F_N=A D_1 P_1 (G_0+\lambda G_1+\mu G_2+\rho G_3) P_2D_2 C.
\]

Here \(D_1,D_2\) are **arbitrary invertible complex diagonals** and \(P_1,P_2\) are **arbitrary permutations**. \(F_N=(\zeta_N^{jk})_{j,k}\) is the unnormalized positive-exponent DFT. Because \(A,C\) are invertible, define \(T=A^{-1}F_NC^{-1}\). Write \(x=(x_0:x_1:x_2:x_3)\), and \(B(x)=\sum_{s=0}^3x_sG_s\). We prove more than the desired affine restriction \(x_0=1\): **there is no nonzero projective coupling** for the certified family.

## 2. Five-cycle theorem: five quadrics, one square certificate

Fix two distinct middle rows \(r_0,r_1\), and five distinct middle columns \(c_0,\dots,c_4\), to which the two selected target rows and five selected target columns would be mapped under the unknown permutations. For each pair \(a,b\), define the homogeneous quadratic

\[
q_{ab}(x)=T_{0a}T_{1b}B_{r_1c_a}(x)B_{r_0c_b}(x)
-T_{0b}T_{1a}B_{r_1c_b}(x)B_{r_0c_a}(x).
\]

**Lemma 40.1 (gauge elimination).** If \(T=D_1P_1B(x)P_2D_2\) for an admissible \(x\), then every \(q_{ab}(x)=0\). Proof: substitute \(T_{ij}=u_iB_{r_ic_j}(x)v_j\); the two products are equal. This does not divide by entries that may be zero.

Use the five edges of a column-index Hamiltonian cycle
\((0,1),(1,2),(2,3),(3,4),(4,0)\). Multiply each of their five quadrics by each of \(x_0,x_1,x_2,x_3\), and express the resulting twenty cubics in the 20-dimensional space of homogeneous degree-three polynomials in four variables. This defines a **20×20 Macaulay coefficient matrix** \(K_3\).

**Theorem 40.2 (exact no-root certificate).** If \(\det K_3\ne0\), then there is no complex nonzero projective \(x\) satisfying even those five necessary phase constraints. Therefore that mapping cannot be an exact Fourier factorization with any choices of the two diagonal masks.

*Proof.* The twenty cubic multiples span **every** homogeneous cubic polynomial. At a purported common projective root \(x\ne0\), all twenty vanish; so every cubic vanishes, including \(x_j^3\) with \(x_j\ne0\), contradiction.

**Minimality within this degree-three linear-span method.** Four quadratic equations provide at most \(4\cdot4=16\) cubic multiples, fewer than the required 20. Thus **at least five** quadratic equations are needed to produce this particular full-degree cubic certificate. This is not a general minimal-certificate theorem in higher degrees.

### A mathematical falsification check

One fixed five-cycle does **not** always suffice. At \(N=16\), for example, the ordered rows \((2,8)\) and columns \((8,10,3,2,5)\) give cubic rank **19**, at both exact audit primes. The alternative cycle \((0,1),(1,2),(2,4),(4,3),(3,0)\) has rank **20** for the *same* mapping. Another counterexample: rows \((2,5)\), columns \((2,6,8,5,3)\). Using **all ten** \(2\times2\) minors also gives rank 20 at these examples. Rank deficiency of a *selected certificate* therefore does **not** establish that a Fourier-compatible coupling exists.

The native verifier offers an optional `rescue` mode: try the first five-cycle; if its rank is deficient, try the second five-cycle. Every full-rank test is a valid impossibility witness. If both fail, the answer is simply **undecided** by that gate.

## 3. Exact family-specific theorem at N=8

The fixed rational-Gaussian Green parameters are specified by the packaged source (`phase38_joint_masks.py`, `phase39_bivariate.py`, `phase40_four_green.py`). The eight middle/outer cycle orders are deterministic. All denominators and both outer mixers are nonzero/invertible under the tested reductions.

**Theorem 40.3 (complete small-size exclusion).** At \(N=8\), no complex triple \((\lambda,\mu,\rho)\), no two invertible complex diagonal masks, and no two intermediate permutations produce the DFT for this **particular** eight-Green family.

*Certificate.* For each of the **376,320** ordered assignments of two middle rows and five middle columns, the native verifier obtained rank \(20/20\) over both \(\mathbb F_{998244353}\) and \(\mathbb F_{2013265921}\). Every full permutation pair induces one of these local assignments. A nonzero determinant in either valid split-prime reduction implies that the original algebraic determinant in the cyclotomic/rational coefficient field is nonzero; denominators were units in the reductions. Therefore the no-root statement holds over characteristic zero and hence over \(\mathbb C\).

**Generic stability corollary.** Keeping the **cycle orderings fixed**, the rank-20 determinant for each mapping is a rational function of the fixed scalar Green parameters and outer weights. Its value is not identically zero, as certified by a single successful specialization. A finite product of these nonzero rational functions is again nonzero. Thus a nonempty Zariski-open set of such fixed scalar parameters excludes the full Fourier factorization in this architecture at \(N=8\). This is not a statement for all graph orderings or all sizes.

### Larger exact mapping samples, not all-permutation proofs

The current packaged audit contains the following exact modular checks, with the adaptive second-cycle certificate, and **zero undecided mappings**:

| N | 998244353 mappings | 2013265921 mappings | Notes |
|---:|---:|---:|---|
| 8 | 376,320 | 376,320 | **Complete enumeration** |
| 16 | 1,000,000 | 250,000 | Pseudorandom samples; 15 and 3 mappings required the alternative cycle |
| 32 | 100,000 | 100,000 | Pseudorandom samples |
| 64 | 50,000 | 50,000 | Pseudorandom samples |
| 128 | 25,000 | 25,000 | Pseudorandom samples |

This proves an exclusion for **each checked mapping**, not for every mapping at \(N>8\). Earlier interrupted long validation runs are not counted in this table.

## 4. A constructive graph/union observation: N+1 independent holonomies

Consider two Hamiltonian cycles on a common set of \(N\) vertices. Regard their \(2N\) directed weighted edges as a **labelled multigraph**, so an edge in each of two different resolvents is a separate edge even when endpoints coincide. A common vertex diagonal similarity \(D\) changes each edge weight by

\[
w_{u\to v}\mapsto \widetilde w_{u\to v}=w_{u\to v}D_u/D_v.
\]

Select a spanning tree with union-find. Fix the root diagonal potential to 1 and propagate potentials along tree edges so that every transformed tree weight is 1. All other transformed edge weights are invariant under further vertex-gauge changes.

**Theorem 40.4 (simultaneous gauge normal form).** For any connected labelled directed graph with \(E\) nonzero-weight edges and \(N\) vertices over a field, the common diagonal-gauge classes are parameterized by exactly \(E-N+1\) multiplicative chord invariants. For two Hamiltonian cycles this is **\(N+1\)**; for one Hamiltonian cycle it is **1**.

*Proof.* Every connected spanning tree contains \(N-1\) edges. Tree normalization uses the \(N-1\) independent vertex-potential ratios; the root scalar is immaterial. No nontrivial relative vertex rescaling preserves all tree weights 1, hence every remaining chord weight is an invariant. Conversely, prescribing arbitrary nonzero chord weights with all tree weights 1 gives a representative of every possible gauge class.

If \(W_s\) is the weighted successor matrix for one cycle, then
\(W_s=D\widetilde W_sD^{-1}\), and therefore
\((I-W_s)^{-1}=D(I-\widetilde W_s)^{-1}D^{-1}\). The same **common** \(D\) works for both resolvents. The algorithm uses union-find plus a tree traversal, \(O(N)\) field operations for a fixed number of cycles.

The classical abstract ingredient is **gain-graph switching theory**; see the prior-art file. The application here makes the phase degrees of freedom in our noncommuting Green-sum architecture explicit. It is **not** an FFT factorization.

## 5. New constructive local phase theorem: full Jacobian rank

Let \(M(h)=G_1(h)+G_2(h)\), where the tree-normalized edge weights are fixed at 1 and the \(N+1\) chord weights \(h\) vary independently. Select the first two rows and columns 0,1,2,3,4, assuming those ten entries are nonzero. Define four gauge-invariant ratios

\[
R_j(h)=\frac{M_{0j}(h)M_{10}(h)}{M_{1j}(h)M_{00}(h)},\quad j=1,2,3,4.
\]

For a chord edge \(e:u\to v\) belonging to cycle \(s\), inverse differentiation gives

\[
\frac{\partial (G_s)_{ab}}{\partial h_e}=(G_s)_{av}(G_s)_{ub},
\quad\text{since}\quad d(I-W_s)^{-1}=G_s\,(dW_s)\,G_s.
\]

Consequently its **logarithmic cross-ratio Jacobian** is

\[
\frac{\partial\log R_j}{\partial h_e}=
\frac{(G_s)_{0v}(G_s)_{uj}}{M_{0j}}+
\frac{(G_s)_{1v}(G_s)_{u0}}{M_{10}}-
\frac{(G_s)_{1v}(G_s)_{uj}}{M_{1j}}-
\frac{(G_s)_{0v}(G_s)_{u0}}{M_{00}}.
\]

(The notation \(d\log\) is rational differential notation, not a call to a complex logarithm.)

For the exact labelled graphs and small integer weights generated by `phase40_holonomy.random_problem`, **one common choice of four chord columns** has a nonzero \(4\times4\) minor at both split audit primes for each of \(N=8,16,32\). The precise columns and determinant residues are in `phase40_jacobian_certificates.json`.

**Theorem 40.5 (finite-size complex algebraic dominance).** For these explicitly tested fixed cycle orderings, with generic complex nonzero chord weights, the map \(h\mapsto(R_1,R_2,R_3,R_4)\) is dominant: its image contains a nonempty Zariski-open set in the four-dimensional target phase-ratio torus.

*Proof.* A nonzero modular \(4\times4\) minor at an integral parameter tuple, with all denominator factors nonzero in the reduction, proves that this rational minor is **nonzero over \(\mathbb Q\)**. Hence its Jacobian has rank four at a characteristic-zero point. The characteristic-zero Jacobian/dominance criterion for rational maps of smooth algebraic tori implies dominance; a dense constructible image contains a nonempty Zariski-open set.

**Careful scope:** edge gains and chord holonomies are allowed to be arbitrary **nonzero complex numbers**, not restricted to unit-modulus phases; generic local target ratios are achievable in that model, but we have **not** shown the particular four ratios of a Fourier transform are among them, nor simultaneous agreement for all rows and columns, nor a general-\(N\) synthesis algorithm. The result does not establish control using unit-modulus edge phases alone. Offline precomputation of those holonomy parameters remains an unresolved cost.

## 6. Weyl negative control and complexity

The two Hamiltonian Green solves, and a product of three sums of two such independently weighted solves separated by diagonal phase masks, have **linear field-operation application cost once the weights are supplied**. The attached `phase40_weyl_control.py` constructs the six-resolvent product and tests

\[
MZ=DM,\qquad MD=Z^{-1}M
\]

on independent exact random vectors. The reference radix-two Fourier transform satisfies both. The sampled weighted Green products fail both equations at every tested coordinate, \(N=8,16,32,64,128\), in both audit primes. This rejects the **sampled weights**, not every possible assignment of the \(N+1\) phase holonomies.

The eight-Green scalar-coupling executor matches dense matrix multiplication on every tested vector, but its fixed parameters are **proved insufficient** at \(N=8\). The online \(O(N)\) arithmetic of a *failed candidate* is not a valid FFT speedup. Field arithmetic and parameter lookup also do not settle exact complex precision, bit complexity, or preprocessing and memory costs.

## 7. Research gate for Phase 41

1. Treat the \(N+1\) chord holonomies of two independent weighted Green cycles as the *actual synthesis parameters* (not only scalar Green coefficients). Choose target Fourier cross-ratios and attempt exact algebraic lifting, with admissibility and denominator conditions tracked.
2. Use the four-ratio full-rank Jacobian certificate as a local controllability check, then insist that any candidate satisfy **all** projective ratios and both exact Weyl equations.
3. Require a reproducible generator for complex parameters and exact \(O(N)\) or genuinely sub-\(N\log N\) total work **including generation, precomputation, precision, and movement**. Prove the algorithm uniformly for every \(N\); finite-instance interpolation is not enough.

**Claims of originality are not established by these experiments.** The project-specific certificate and application warrant a serious prior-art audit before claiming a standalone paper.
