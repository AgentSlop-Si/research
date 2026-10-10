# Exact 99-edge three-layer superconcentrator and Fourier phase-gauge geometry — v33

**Research checkpoint:** 10 October 2026  
**Target:** an exact full-output transform of every fresh arbitrary input, eventually at cost `o(N log N)` in a fully charged, sequential model, ideally `O(N)` or `O(N log log N)`.  
**Status:** an explicit, exhaustively certified, small 3-layer **superconcentrator topology**, a finite-field full-spark specialization with **every minor checked**, a sharp generic gauge-dimension calculation over characteristic zero, a signed/unrestricted-amplitude model audit, and exact controls. **No weight assignment computing `F_11` on the sparse support was found or proved impossible. No new exact FFT speedup is established.**

## 1. Inherited problem and novelty boundary

v31 reduced a half-size Schur/Fourier interface to a superconcentrator topology and identified depth-three `Theta(N log log N)` routing as an information-flow window. That result does not provide the correct Fourier coefficients. v32 examined positive edges with weights restricted to roots of unity, proving an exact prime cyclotomic path-count gap and a restricted phase-alphabet gate. It correctly excluded no unrestricted complex coefficient architecture.

This checkpoint changes models explicitly: **every one of the 99 edges gets an independent arbitrary nonzero complex weight**. There are no positive-only, root-only, or sign restrictions. A finite-field reduction is used solely as a reproducible exact algebraic certificate; it is not a finite-field numerical FFT performance claim. We also locate a classical bounded-coefficient lower bound that dominates the positive-root v32 route even when signed cancellations are allowed.

There is an independent, publicly available October 2026 OpenAI mathematical result reporting exact DFT circuits with a tiny sub-`N log N` power saving in an exact-complex supplied-root model. This project does not reconstruct that algorithm and instead asks for a much stronger, structurally new O(N log log N)/O(N) path. A full novelty/priority literature review has **not** been completed.

## 2. A fully specified 99-edge candidate: three layers of 11 nodes

Let `K` be any field. Inputs, two hidden layers, and outputs each contain exactly 11 nodes. There are three matrices

\[
A,B,C\in K^{11\times11},\quad H=CBA.
\]

Each layer support is the union of three edge-disjoint permutation matchings: every row and column has degree exactly 3. The exact three lists of `(destination,source)` pairs are preserved in `topology_11.json`. The search used a fixed seed and stopped at its first sample surviving preliminary checks; the **final certificate does not rely on the random search**.

The architecture has:

- 11 inputs, 22 hidden nodes, 11 outputs;
- exactly `33+33+33=99` weighted edges;
- 33 scalar sum gates, each with fan-in 3;
- no zero transfer entry forced by the support.

A direct dense 11×11 matrix has 121 edges, so this is already a strictly *subquadratic-size finite example* in the literal edge-count sense (`99<121`). It is **not** an asymptotic family.

### Theorem 2.1 — exact superconcentrator certificate

For every integer `1<=k<=11` and every pair of `k`-element input/output subsets `(I,O)`, the fixed 99-edge graph contains `k` vertex-disjoint directed paths linking `I` to `O`.

The exhaustive checker covered exactly

\[
\boxed{\sum_{k=1}^{11}\binom{11}{k}^{2}
=\binom{22}{11}-1=705431}
\]

terminal-subset pairs, with **zero failures**. This is a literal finite graph theorem established by exhaustive enumeration, not by extrapolating random trials.

**Certificate method.** Each layer is a bipartite graph. For every `k`-element source set, the program uses a subset dynamic program to enumerate all `k`-element output sets attainable by a matching (no repeated vertex). It then composes the resulting three Boolean relations by bitset union. Composition is equivalent to vertex-disjoint paths through the layered graph: each intermediate subset contains exactly the `k` distinct vertices used by the paths. Every resulting row of every relation is full.

The independent verifier uses `networkx` max-flow for 220 additional sampled terminal pairs; those samples are **not** substituted for the exhaustive relation certificate.

## 3. Full-spark is genuinely attained with only 99 weighted edges

Choose the prime field

\[
\boxed{\mathbb F_q,\quad q=1000000123}
\]

and the 99 fixed nonzero edge weights in `weights_11.json`. The matrix `H=CBA` is reproduced, entry for entry, in `transfer_11.txt`.

A separate C++ exact modular checker `all_minors_certificate.cpp` exhausts **all 705431 nonempty square minors** of this concrete matrix and finds that **every determinant is nonzero modulo q**. Modular elimination uses only exact integer operations, with no floating point and no probability-of-error predicate; all of its products fit in unsigned 64-bit arithmetic for the certified `q`.

Thus there exists a full-spark weighted transfer on this support. Moreover, the Lindström–Gessel–Viennot path determinant expansion and Theorem 2.1 show every minor is a nonzero polynomial in independent edge variables. Since there are finitely many minors, a generic specialization over the complex numbers is also full spark.

**Critical:** `H` is **not** claimed to be Fourier. Full-spark and superconcentrator connectivity are necessary for `F_11`, not sufficient.

## 4. A complete Fourier phase-compatibility test for arbitrary weights

For any `11×11` transfer matrix `H` whose entries and anchor first row/column are nonzero, define

\[
R_{ij}(H)=\frac{H_{ij}H_{00}}{H_{i0}H_{0j}},
\qquad 1\le i,j\le10.
\]

The 100 numbers `R_ij` are invariant under arbitrary nonzero diagonal input and output scalings. Conversely, two dense matrices are diagonally equivalent if and only if all these cross ratios agree: after anchoring the first row and column, every other entry is determined by its cross ratio. This is an **if-and-only-if certificate**, not a heuristic.

If `F_11[i,j]=zeta_11^(ij)`, then the complete Fourier phase requirements are

\[
\boxed{R_{ij}(H)=\zeta_{11}^{ij}\quad(1\le i,j\le10).}
\]

For the depth-three network `H=CBA`, each entry `H_ij` is a degree-three polynomial in edge weights. Clearing denominators gives 100 explicit **degree-at-most-six** polynomial equations

\[
\boxed{
H_{ij}H_{00}-\zeta_{11}^{ij}H_{i0}H_{0j}=0.
}
\]

Over `F_q` the primitive 11th root is `zeta=414936531`. For the saved explicit full-spark assignment, **0 of 100** Fourier phase equations hold. The first failure is

`(i,j,residue)=(1,1,379306912)`.

That is a counterexample to *connectivity implies Fourier weights*, **not** an impossibility theorem for *all possible* weights. Reweighting the edges could change the answer.

The scripts additionally check a direct Fourier matrix, arbitrary row/column scalings, and a single-entry mutation to show that the criterion accepts exactly what it claims.

## 5. The sharp projective-gauge dimension theorem for this support

The 99 nonzero edge weights range over an algebraic torus `(K^*)^99`. The graph has 44 vertices: 11 inputs, 22 hidden nodes and 11 outputs.

For any nonzero scalar `lambda_v` at each vertex, transform

\[
w_{u\to v}\longmapsto \frac{\lambda_v}{\lambda_u}w_{u\to v}.
\]

The resulting transfer obeys

\[
H_{ij}\longmapsto\frac{\lambda_{\mathrm{out},i}}
{\lambda_{\mathrm{in},j}}H_{ij},
\]

so every Fourier cross ratio `R_ij` stays unchanged. The underlying undirected graph is connected, and all 99 chosen weights are nonzero. Therefore the only vertex scaling that fixes *all the edge weights* is a common scalar. The gauge action has effective dimension

\[
44-1=43.
\]

Consequently, the algebraic image of the map

\[
(w_e)_{e\in E}\mapsto(R_{ij}(CBA))_{1\le i,j\le10}
\]

has **complex dimension at most**

\[
99-43=56.
\]

### Theorem 5.1 — this dimension upper bound is exact

The Jacobian of the 100 cleared-denominator cross-ratio coordinates against all 99 edge weights was calculated exactly modulo `q=1000000123` at the stored nonzero weight assignment. Its rank is **exactly 56**. The package preserves the original row and column indices of an explicit 56×56 nonzero minor, whose exact determinant residue is

\[
\boxed{915710031\pmod{1000000123}.}
\]

All 44 infinitesimal vertex-gauge directions annihilate that Jacobian; their span has rank 43. Thus the nullspace dimension `99-56=43` consists exactly of the vertex gauge directions at that point.

This is also a **characteristic-zero certificate**: the displayed minor is obtained by evaluating an integer-polynomial numerator at integer edge weights; because its reduction modulo `q` is nonzero and all requisite anchor denominators remain nonzero, that minor is not the zero rational function over `Q` or `C`. Its generic complex rank is therefore at least 56, matching the gauge upper bound.

Therefore:

\[
\boxed{
\dim_\mathbb C\overline{\operatorname{im}(R)}=56.
}
\]

The ambient space of 100 cross-ratios has dimension 100, so the image has **codimension 44**. This is a new, support-specific exact algebraic feasibility gate.

### Theorem 5.2 — the 44 missing constraints are not linear

One might try to identify a simple affine equation among the 100 invariants. For this particular support, **none exists**. The file `affine_invariant_certificate.py` evaluates the 101 rational functions

\[
1,\quad R_{11},R_{12},\ldots,R_{10,10}
\]

at 101 independently specified nonzero integer edge assignments, with the precise 101 seeds preserved in `affine_invariant_certificate.json`. The resulting `101×101` evaluation determinant is

\[
\boxed{763214669\pmod{1000000123}\ne0.}
\]

If any nontrivial affine linear identity with complex constant coefficients held among these functions, **every** 101×101 evaluation determinant would vanish. The displayed modular certificate lifts to characteristic zero because the rational-function numerators/denominators are defined over integers and all anchors at the chosen assignments are nonzero modulo `q` (hence are also nonzero at their integer lifts). Thus the functions are linearly independent over `C`.

Consequently any nonzero polynomial vanishing on the 56-dimensional projective image must have **degree at least two** in the 100 cross-ratio coordinates. We have not proved that a quadratic relation exists; its minimum possible degree is the next exact research gate.

**What the 44-codimension result does NOT say.** A special point such as the actual Fourier cross-ratio tuple may lie in a proper 56-dimensional subvariety even when a random point does not. **Counting equations or dimensions is not a proof that `F_11` is outside this image.** A true exclusion needs an explicit polynomial identity valid for every network weight assignment that fails at the Fourier tuple, or a characteristic-zero algebraic infeasibility certificate. A positive result needs a complete exact weight assignment and charged decoder.

## 6. An independent amplitude barrier dominates the v32 phase-only model

The next result is included as a **prior-art/model correction**, not a newly discovered FFT lower bound. Morgenstern (1973) proved the bounded-coefficient determinant bound for linear computation.

Let an arbitrary linear DAG over the complex numbers compute the **unnormalized** `F_N`, counting every weighted incoming edge. At each noninput vertex `v`, the output linear form is `sum_(e:u->v) w_e f_u`. Define the incoming absolute mass

\[
s_v=\sum_{e:u\to v}|w_e|.
\]

Let `Delta` be the largest absolute determinant of any `N` linear forms already available. Initially, the input forms form the identity and `Delta=1`. Introducing vertex `v` grows `Delta` by at most `max(1,s_v)`, by multilinearity in the new row. Since the Fourier matrix satisfies `F_N F_N^*=N I`,

\[
|\det F_N|=N^{N/2},
\]

and hence every such exact circuit satisfies

\[
\boxed{\sum_v\log\max(1,s_v)\ge\frac N2\log N.}
\tag{6.1}
\]

If every edge has `|w_e|<=1` and vertex `v` has indegree `d_v`, then `s_v<=d_v`. For each integer `d>=1`, `log(d)/d <= log(3)/3`, so for **total charged edge count** `E=sum_v d_v`, 

\[
\boxed{ E\ge\frac{3}{2\log3}N\log N. }
\tag{6.2}
\]

This applies to roots of unity, signed edges and arbitrary cancellation. It shows that v32's positive phase-only circuits cannot deliver `o(N log N)` in this **unnormalized bounded-coefficient model**, even with huge multipath interference and no depth restriction.

More generally, if `1<=B=max(1,max_e|w_e|)`, then

\[
\frac N2\log N\le\sum_v\log(Bd_v)
\le E(\log B+\tfrac{\log3}{3}),
\]

so

\[
\boxed{\log B\ge\frac{N\log N}{2E}-\frac{\log3}{3},}
\tag{6.3}
\]

or `B>=1` if the right side is negative. For `E<=C N log log N`, equation (6.3) requires

\[
B\ge\exp\left(\frac{\log N}{2C\log\log N}-\frac{\log3}{3}\right).
\]

This eventually grows faster than any fixed power of `log N`.

### Crucial normalization caveat

Morgenstern's determinant argument is sensitive to global scaling. The normalized unitary matrix `F_N/sqrt(N)` has determinant modulus one, so the same argument proves no growing lower bound for that matrix. Further, the supplied-root unrestricted-coefficient model permits arbitrarily large complex constants, so (6.2) **must not** be quoted as an unrestricted FFT lower bound.

## 7. Exact gauge-normalization escape for arbitrary complex circuits

There is a simple but instructive converse to the coefficient barrier. For an arbitrary weighted DAG, define nonnegative path mass recursively by

\[
P_j=1\quad\text{at each input,}\qquad
P_v=\sum_{u\to v}|w_{uv}|P_u.
\]

Assume the relevant `P_v` are nonzero. Make the vertex gauge change

\[
w'_{u\to v}=w_{uv}\frac{P_u}{P_v}.
\]

Every *internal* and *normalized-output* vertex now satisfies

\[
\boxed{\sum_{u\to v}|w'_{uv}|=1.}
\]

The normalized circuit computes its original node value divided by `P_v`. Restoring each output costs one scalar multiplication by `P_output`. If the original transfer is the unnormalized Fourier matrix, the triangle inequality implies

\[
P_{\mathrm{out},i}\ge\sum_j|F_{ij}|=N.
\]

Thus unrestricted amplitude can always be moved into the **N endpoint gains**. The new graph has the same internal edge count, but its large endpoint coefficients remain fully charged. The gain lower bound is **not gauge invariant**, and this reweighting alone is not a speedup.

For conventional radix-2 FFTs of lengths 4,8,16,32, the package checks every output coefficient exactly in `Z[zeta_N]` using `Phi_N(x)=x^(N/2)+1`, rather than numerical FFT output comparisons. It also checks the exact Gram identity, and each radix-2 layer's absolute path masses double. The final normalization requires output restoration gain exactly `N`. These are correctness/normalization controls, **not a new algorithm**.

## 8. Operation ledger and experiment status

For this one fixed 11-node support:

| Charged item | Count | Qualification |
|---|---:|---|
| Layers | 3 | Only 11×11 fixed experiment |
| Hidden scalar states | 22 | Output gates 11 more |
| Nonzero edge-weight multiplications | 99 | Some weights could be optimized only after they are known |
| Additions in three-input gates | 66 | 33 gates × 2 |
| Arithmetic events under literal weighted-edge evaluator | 165 | Plus input/output reads and writes |
| Independent weight parameters before gauge | 99 | Unrestricted complex edge values |
| Projective vertex-gauge directions | 43 | Graph connected |
| Effective generic Fourier cross-ratio parameters | 56 | Explicit rank-56 witness |
| Fourier cross-ratio target conditions | 100 | `i,j=1,...,10` |
| Topological route pairs exhaustively checked | 705431 | Exact subset DP |
| Full-spark modular minors exhaustively checked | 705431 | Exact C++ GF(q) elimination |
| Exact `F_11` assignments found | **0** | Not a certified impossibility |

A 16-restart *noncertifying* complex optimizer minimizing `||CBA-F_11||_F^2/121` produced best recorded residual approximately `0.176876844248704`. This numerical failure is **not** an exclusion theorem and does not enter any logical proof. All exact structural assertions instead have independent algebraic certificates.

## 9. Reproducibility and external prior art

Run `python run_all.py` in a clean extraction. This checks the embedded full predecessor v32 ZIP, runs the unit tests and independent verifier, compiles and executes the exact all-minor C++ verifier, and regenerates the machine-readable result summary. The main tests cover 17 groups. An independent verifier reimplements the transfer and tests 220 network-flow cases and 330 exact field minors without importing the main implementations.

Relevant *classical* antecedents: the LGV path-determinant lemma; Valiant/Pippenger and Alon–Pudlák superconcentrators; Morgenstern's 1973 bounded-coefficient lower bound; rank/gauge arguments for matrix-factorization parameterizations. Their ideas must be appropriately attributed. The explicit 99-edge topology, the all-minor modular assignment and the exact 56/43 Jacobian/gauge certificate are **project-specific constructed and checked facts**, not established literature-wide new discoveries or publication claims. The `PRIOR_ART_AUDIT.md` file contains links.

## 10. Strict chain checkpoint: the next algebraic test

**Do not return** to phase-only positive roots, low-treewidth extension models, one-dimensional Weil words, claims that full spark alone is sufficient, or generic determinant lower bounds applied to unrestricted coefficients.

**Best precise v34 target:** on the fixed 99-edge support, eliminate the 99 edge weights modulo its 43-dimensional torus gauge to obtain an **explicit nonzero polynomial in the 100 projective cross ratios**, then substitute the Fourier tuple `R_ij=zeta_11^(ij)` in exact characteristic-zero algebra `Q(zeta_11)`. Either:

1. obtain an explicit Fourier-failing identity plus a complete symbolic elimination proof applying to all nonzero and degenerate weight charts; or
2. find and independently substitute one complete **exact** Fourier-compatible assignment (then investigate all-length generalization and fully charged complexity).

A finite-field failure alone, a numerical optimizer, and a dimension count **are not** an exclusion certificate over `C`. Conversely, the present superconcentrator/full-spark circuit computes **some** matrices fast, not necessarily Fourier.
