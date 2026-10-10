# Prime-cyclotomic path-count and phase-alphabet gates — v32

**Date:** 10 October 2026  
**Question:** Can the depth-three `Θ(N log log N)` superconcentrator support window identified in v31 be made into an **exact prime Fourier transform** by labeling its edges with simple Fourier phases?  
**Status:** Proved exact obstructions for *restricted positive phase-only circuits*, together with sharp positive and negative controls. **No faster exact Fourier transform is constructed, and the general arbitrary-complex-weight depth-three problem is not resolved.**

## 0. Provenance and inherited boundary

The v31 package, preserved byte-for-byte as `PRIOR_v31_COMPLETE.zip`, proved an exact flow/rank necessary condition: the support graph of any linear DAG whose transfer is a prime Fourier matrix must be a superconcentrator. The following tight size statements are **external**, not project discoveries:

- Depth 2: `Θ(N log² N / log log N)` edges — Radhakrishnan and Ta-Shma.
- Depth 3: `Θ(N log log N)` edges — Alon and Pudlák.
- Growing depth: linear-size superconcentrators exist — Pippenger.

These bounds certify **possible information routes**, not Fourier coefficients. Our v32 question is what happens when network coefficients are restricted to the bare roots of unity.

As of October 2026, the public OpenAI mathematics repository separately *reports* a deterministic exact-complex-arithmetic all-length DFT upper bound `O(N (log N)^(1-10^-13))` in a specialized supplied-root model (result #130). That is not this project and not a practical floating-point or bit-complexity bound. This report does **not** claim that every exact sub-`N log N` result is unknown; the narrower goal here is a new explicit phase-compatible depth-three network / still stronger `O(N)` method.

## 1. Exact model and scope

Let `p>=2` be prime, `ζ=exp(2πi/p)`, and let `F_p[i,j]=ζ^(ij)` be the **unnormalized** Fourier matrix.

The proposed circuit is a finite DAG with `p` distinguished inputs and `p` distinguished outputs. Each edge has a weight from the multiplicative cyclic group

`{1,ζ,...,ζ^(p-1)}`

**with positive unit multiplicity**. Parallel edges are charged separately. Each gate computes the sum of all weighted incoming values; outputs are linear in the input. There are no arbitrary complex multipliers, independent scalar factors, negative edge signs, divisions, or implicit coefficients supplied by an oracle. A path `P` contributes exactly one Fourier phase `ζ^(e(P))`, where `e(P)` is the sum of edge exponents modulo `p`. The transfer coefficient is the sum of these path contributions.

An edge is charged as one scalar multiply/add/routing event. The main theorem is **not** a lower bound for arbitrary complex linear circuits; modern FFTs use substantially richer coefficients, including negative signs and normalized mixtures.

## 2. Exact multiplicity gap: one path or a full `p`-gon

For an input-output pair `(j,i)`, let `c_r(i,j)>=0` be the number of directed paths whose total phase equals `ζ^r`. All paths are counted with edge identity (parallel edges yield distinct paths). Then:

`T_G[i,j] = Σ_(r=0)^(p-1) c_r(i,j) ζ^r`.

### Theorem 2.1 — prime-cyclotomic path-count rigidity

If `T_G[i,j]=ζ^(ij)` exactly, then there is a **unique nonnegative integer** `t_(i,j)` such that

\[
\boxed{c_r(i,j)=t_{i,j}+\mathbf1_{\{r\equiv ij\pmod p\}}\quad\text{for every }r.}
\]

Consequently:

\[
\boxed{\#\text{paths}(j\to i)=1+p\,t_{i,j}.}
\]

If `t=0`, the path is unique and has exactly the target phase. If `t>=1`, every phase residue is represented and the smallest possible nonunique count is `p+1`.

**Proof.** The integer polynomial

`g(z)=Σ_r (c_r−1[r=ij]) z^r`

has degree at most `p−1` and vanishes at `ζ`. The minimal polynomial of `ζ` over `Q` is `Φ_p(z)=1+...+z^(p−1)`, so `g(z)=t Φ_p(z)` for some rational `t`. Because every coefficient of `g` is integer, `t` is integer; since the `p−1` coefficients other than the target are nonnegative, `t>=0`. Coefficient comparison proves the formula. QED.

This is an elementary application of the classical theory of vanishing sums of roots of unity (compare Lam–Leung, 2000). **The project-specific combination** is the path-sum/count interpretation, the exact phase-alphabet gate, and the unique-path Fourier circuit consequence below; it has **not** been novelty-cleared.

### Corollary 2.2 — phase coverage per pair

Every exact Fourier entry must include **at least one** path with the exact target phase `ζ^(ij)`; if there are multiple paths, there must be at least one path with **every one** of the `p` possible phases. There is no positive-unit-root representation of `ζ^(ij)` using `2,...,p` paths.

## 3. Bounded global phase alphabet is impossible at bounded depth

Assume every edge exponent belongs to one global set `A⊂Z/pZ`, `|A|=s`, and every source-to-sink path uses at most `d` edges.

The phase of a path is a sum of at most `d` elements of `A`. Since addition of exponents is commutative, the exponent depends only on the count of each of the `s` labels. By stars and bars, the number of possible count vectors is at most

\[
\boxed{\binom{d+s}{s}.}
\]

For a strictly layered circuit whose paths **all** use exactly `d` edges, the sharper upper bound is

\[
\boxed{\binom{d+s-1}{s-1}.}
\]

### Theorem 3.1 — phase-alphabet/depth barrier

If

\[
\boxed{\binom{d+s}{s}<p,}
\]

then **no circuit whatsoever**, regardless of its total number of edges or vertices, can compute `F_p` in the phase-only model. For exactly `d` layers, replace the left side by `binom(d+s−1,s−1)`.

**Proof.** The set of reachable phase residues has fewer than `p` elements. The Fourier entries in row `i=1` require every target `ζ^j`, `j=0,...,p−1`. By Corollary 2.2 the target phase must actually occur on a path for each `j`. A missing residue is an immediate contradiction. QED.

**Example.** At `p=101`, depth at most 3 and global alphabet size `s=4`, there are at most `binom(7,4)=35` path-phase residues, so the Fourier transform is impossible at *any* edge count in this restricted model. For an exactly 3-edge layered graph, at least `s=8` distinct global phase labels are necessary even to pass the phase-coverage check; `s=7` yields `binom(9,6)=84<101`. The at-most-depth-three necessary threshold is `s=7` (`binom(10,7)=120`). These bounds are necessary, never sufficient.

For fixed `d`, the necessary alphabet size grows as `Ω(p^(1/d))` (with different harmless constants for exact vs variable depths). A fixed phase alphabet cannot yield any bounded-depth all-prime-length Fourier circuit in this positive-root model.

### Extension: positive rational phase amplitudes

The phase **coverage** obstruction is not limited to unit-amplitude edges. Suppose each edge has weight `a_e ζ^(r_e)` with positive rational `a_e`. For each pair the residue masses `c_r` are nonnegative rationals. The same minimal-polynomial proof gives `c_r=t+1[r=ij]` with **rational** `t>=0`. Thus every target phase still has to occur, and the global alphabet/depth impossibility is unchanged. However, the **integer path-count gap fails**: two paths of weights `(1/2)ζ^(ij)` each already compute `ζ^(ij)`. The quadratic unique-path edge theorem cannot be invoked without the unit/integer-multiplicity condition. The independent group-ring tests include this counterexample, preventing accidental extension to unrestricted rational weights.

## 4. If phase cancellations are absent, edge cost is quadratic

### Lemma 4.1 — unique paths plus nonzero `2×2` minors

Let `M` be an `n×n` matrix over a field in which every entry and every `2×2` minor is nonzero. Suppose its transfer is realized by a weighted DAG with **exactly one path between each input and each output**. Then

\[
\boxed{|E|\ge n^2.}
\]

This holds for **arbitrary nonzero edge weights** once the graph is promised unique-path; it is not peculiar to cyclotomic labels.

**Proof.** For each vertex `v`, let `I(v)` be the inputs reaching `v` and `O(v)` the outputs reachable from `v`. If both sets had at least two elements, uniqueness of all terminal paths would force `M[O(v),I(v)]` to be an outer product of the (unique) prefix and suffix path weights, with rank one. This contradicts the nonzero `2×2` minors. Hence every vertex satisfies `|I(v)|=1` or `|O(v)|=1` whenever both sets are nonempty.

For each terminal pair `(i,j)`, follow its unique path from input `j` to output `i`. The starting vertex reaches every output and the final vertex reaches only output `i`. Mark the **first edge** `u→v` along the path where the number of reachable outputs drops to one. Then `|O(u)|>=2`, hence `|I(u)|=1`, and `|O(v)|=1`. That edge cannot occur on a terminal path for any other input/output pair, so the association from the `n²` terminal pairs to these edges is injective. Thus `|E|>=n²`. QED.

### Corollary 4.2 — low path multiplicity forces quadratic work

In the phase-only prime Fourier model, suppose every terminal pair has at most `p` paths. By Theorem 2.1 each pair then has **exactly one** path. Fourier has nonzero `2×2` minors because the determinant of rows `i≠k` and columns `j≠l` is nonzero exactly when

`(i−k)(j−l) != 0 (mod p)`.

Therefore

\[
\boxed{|E|\ge p^2.}
\]

A network smaller than `p²` edges, such as the `Θ(p log log p)` superconcentrator **support** target from v31, would have to realize the Fourier phases through some input/output pairs with `p+1` or more paths, including full sets of `p` canceling phase residues. That remains possible in principle; this corollary does **not** rule it out.

The edge bound is sharp: direct input-to-output edges labeled `ζ^(ij)` use precisely `p²` edges and one path per pair.

## 5. Mandatory negative control: path multiplicity is cheaply inflatable

There is a `3p`-edge phase-only circuit with **zero transfer** and exactly `p` paths between every input and output:

- one edge from each input into a common hub;
- `p` parallel edges, labeled `ζ^0,...,ζ^(p−1)`, from that hub to another hub;
- one edge from the second hub to each output.

The transfer is zero because `Σ_r ζ^r=0`.

Adding this gadget to the `p²` direct Fourier edges creates an exact Fourier circuit of `p²+3p` edges and **`p+1` paths for every pair**, with residue vector

`(1,1,...,1)+e_(ij)`.

Thus path counts alone are not a robust unrestricted complexity measure. One can manufacture an enormous number of paths with only `O(p)` overhead. A successful stronger theorem must forbid or account for these common zero packets, instead of charging every canceling path as an independent operation.

If signed edge weights are permitted, a two-parallel-edge `+1`/`−1` gadget already has zero transfer using only two paths per pair. This is outside the theorem: `−1` is **not** a `p`-th root when `p` is odd.

### Composite-length boundary

The prime assumption is mathematically essential, not cosmetic. Let `z=exp(2πi/6)` be a primitive sixth root. Its quadratic minimal polynomial gives `z^2=z-1`, hence `z^5=1-z` and

\[
\boxed{z+z^5=1.}
\]

Thus *two* positively weighted sixth-root paths can already realize the target phase 1. Neither the `1 (mod p)` count formula nor the prime Fourier all-`2×2`-minors argument can be generalized silently to arbitrary composite lengths. The package includes this exact quotient-ring counterexample.

## 6. Exact reproduction

All arithmetic is in the integer group ring `Z[C_p]` reduced modulo `Φ_p`. There is **no floating-point tolerance** and no FFT call in the certificate.

`cyclotomic_path_gate.py` implements a generic topologically ordered path-count evaluator with `p` residue counts per DAG state, precise root-equality reduction, phase alphabets, explicit Fourier circuits and cancelling controls.

`independent_verifier.py` does **not** import that module. It enumerates paths directly by depth-first search, independently performs the integer polynomial reduction `z^(p−1)=−Σ_(r<p−1)z^r`, and verifies the `p+1`-path Fourier construction.

Automated tests cover 14 groups:

1. exhaustive short integer count vectors at `p=3,5,7`;
2. arbitrary `p`-gon multiplicities;
3. exact direct and layered Fourier circuits at `p=3,5,7,11`;
4. distinct-edge injection certificate for unique-path networks;
5. zero-circuit and nonunique positive Fourier controls;
6. phase-sumset / multiset upper bounds;
7. signed (out-of-model) two-path cancellation;
8. explicit mutation rejection;
9. edge-order invariant evaluation;
10. `p=101` alphabet exclusion;
11. embedded-v31 hash and CRC;
12. rational-amplitude phase coverage and its two-half-path counterexample;
13. exact composite-length counterexample (`ζ_6+ζ_6^5=1`);
14. random sparse-graph negative controls.

`python run_all.py` reproduces the results. The archive embeds the full v31 ZIP unchanged and checks its SHA-256.

## 7. Claim ledger and next research gate

**Proved within this precise model:** the root-path multiplicity gap; mandatory target-phase coverage; the alphabet/depth impossibility; the unique-path full-spark `n²` edge bound; exact cheap zero-packet negative controls.

**Not established:** an exact `o(N log N)` Fourier algorithm by our graph/Green route; an unrestricted lower bound; a fixed-precision or bit-complexity bound; practical speed superiority; a literature-wide novelty claim. The root-of-unity gap follows from classical cyclotomic algebra, and depth-three superconcentrator support bounds are classical.

**Next exact gate:** permit **signed/unrestricted complex coefficients**, but seek an *efficiently checkable phase-compatibility invariant* for a candidate depth-three `O(N log log N)` support, beyond full spark / max flow / cyclotomic positive-cone counting. A viable construction must exhibit weights satisfying **every Fourier entry**, independently verify the identity, and charge every edge, coefficient preparation, routing operation and output write. If no construction survives, a valid impossibility result must explain why even with arbitrary canceling complex weights the Fourier matrix cannot inhabit the selected circuit class.

## References (background, not priority assertions)

- Lam and Leung, *On vanishing sums of roots of unity*, Journal of Algebra 224 (2000), 91–109, DOI `10.1006/jabr.1999.8089`.
- Alon and Pudlák, *Superconcentrators of depths 2 and 3; odd levels help (rarely)*, JCSS 48 (1994), 194–202, DOI `10.1016/S0022-0000(05)80027-3`.
- Radhakrishnan and Ta-Shma, *Bounds for dispersers, extractors, and depth-two superconcentrators*, SIAM J. Discrete Math. 13 (2000), 2–24, DOI `10.1137/S0895480197329508`.
- OpenAI Math result 130, *An explicit power saving for the exact discrete Fourier transform* (September 25, 2026), https://github.com/openai/math/blob/main/lean/docs/130.md . The all-length exact-complex model is separate from this phase-only investigation.
