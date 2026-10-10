Public source-text preservation. This is the source author’s research statement, not the corrected review. Read [the accepted support audit](../../reviews/01_schur_support.md) for the controlling field, edge-depth, cost and generic-weight qualifications. The source text below is unchanged. Source-reported numerical results are not independent checks; source programs and predecessor archives are not included. Preservation and hashing do not certify every sentence or establish priority. Historical source wording about an open exact target concerns the source project; it is not a current literature-wide claim. The source’s broader claim that rank or connectivity methods are exhausted is narrowed in the audit to total-nonsingularity or connectivity alone.

# Superconcentrator interface gate — v31

**Checkpoint:** 10 October 2026  
**Primary target:** exact, full-output DFT of an arbitrary fresh input in fully charged sequential `o(N log N)` arithmetic.  
**Status:** an exact rank/flow theorem for arbitrary linear DAGs, its application to the sharp v30 Schur interface, imported tight bounded-depth routing bounds, and positive full-spark circuit controls. **No exact faster FFT is constructed.**

---

## 1. Starting point

v30 established that a same-branch Schur realization of a totally nonsingular `N x N` target needs an interface of dimension at least

\[
q\ge \lfloor N/2\rfloor.
\]

The bound is sharp as a rank theorem: exact Fourier Schur realizations with `q=floor(N/2)` were constructed, but their injection, extraction and interface blocks were dense. The remaining question was no longer interface dimension. It was:

> Can a linear-dimensional interface be routed and solved by a sparse exact circuit using `o(N log N)` work?

This checkpoint identifies the exact support property forced on that complete correction circuit.

---

## 2. Linear DAG model

Let `G` be a finite directed acyclic graph with `n` distinguished input vertices and `n` distinguished output vertices. Give each edge `e` a scalar weight `w_e` over a field.

The transfer matrix `T_G` is defined by path sums:

\[
(T_G)_{ij}
=
\sum_{P:j\leadsto i}\prod_{e\in P}w_e.
\]

Evaluating all gates in topological order costs one multiply-add per edge, plus terminal reads/writes. Thus the charged scalar work is `Theta(|E(G)|)` for a fixed prepared graph.

No restriction is imposed on layers, fan-in, fan-out, coefficient magnitudes or the origin of the graph. A Schur interface, a collection of branch solves, or any other exact linear routing network can be expanded into this model by charging all of its arithmetic edges.

---

## 3. Main theorem: transfer rank is bounded by disjoint-path capacity

For input subset `I` and output subset `O` of equal size, let

\[
\nu_G(I,O)
\]

be the maximum number of pairwise vertex-disjoint directed paths from `I` to `O`.

### Theorem 3.1 — rank/flow gate

For every weighted linear DAG,

\[
\boxed{
\operatorname{rank} T_G[O,I]
\le
\nu_G(I,O).
}
\tag{3.1}
\]

### Proof

If `nu_G(I,O)=r`, the vertex version of Menger's theorem supplies a vertex cut `S` of size `r` separating the selected inputs from the selected outputs. Every selected input-to-output path meets `S`.

Run the linear circuit from values supported only on `I`. The vector reaching the selected outputs is a linear function of the `r` scalar gate values at `S`. Therefore the map from the `|I|` selected inputs to the `|O|` selected outputs factors through an `r`-dimensional space. Its rank is at most `r`. QED.

The proof also works directly with a chosen separator, without invoking a minimum-cut theorem.

### Corollary 3.2 — full-spark transfer implies a superconcentrator

If every square minor of `T_G` is nonzero, then for every equal-size input and output subsets there are that many vertex-disjoint paths. Hence:

\[
\boxed{
G\text{ is an }n\text{-superconcentrator.}
}
\tag{3.2}
\]

This is a support condition, independent of edge weights once the transfer is totally nonsingular.

---

## 4. Application to the v30 Schur correction

In the sharp same-branch v30 setup, write the target as

\[
M=T+R,
\]

where `T` is triangular in the branch order and `R` is the complete interface correction.

Let

\[
m=\lfloor N/2\rfloor.
\]

Choose the first `m` branch-order rows and the last `m` branch-order columns. The triangular baseline vanishes on this rectangle:

\[
T[I,J]=0.
\]

For a prime complex Fourier target, or any endpoint monomial equivalent, Chebotarev nonvanishing gives

\[
\operatorname{rank}M[I,J]=m.
\]

Therefore

\[
R[I,J]=M[I,J]
\]

is totally nonsingular on all of its square subblocks. By Theorem 3.1, the **complete circuit implementing the correction from these `m` inputs to these `m` outputs must be an `m`-superconcentrator**.

This statement includes every charged component:

- sparse injection routing;
- branch forward/backward solves;
- interface routing;
- the interface solver;
- extraction routing.

No part can be treated as a free dense factor.

---

## 5. Bounded-depth consequences

The superconcentrator literature now gives immediate architecture-specific cost gates.

### 5.1 One middle layer / depth two

Radhakrishnan and Ta-Shma proved that the minimum number of edges in a depth-two `m`-superconcentrator is

\[
\boxed{
\Theta\!\left(
\frac{m\log^2m}{\log\log m}
\right).
}
\tag{5.1}
\]

Thus a correction implemented as one sparse input-routing layer, independent middle states, and one sparse output-routing layer requires

\[
\Omega\!\left(
\frac{N\log^2N}{\log\log N}
\right)
\]

edges at `m=floor(N/2)`. This is asymptotically larger than `N log N`.

So the v30 sharp rank factorization cannot be turned into a faster FFT by merely finding sparse depth-two factors.

### 5.2 Two middle layers / depth three

Alon and Pudlak proved the tight order

\[
\boxed{
\Theta(m\log\log m)
}
\tag{5.2}
\]

for depth-three superconcentrators.

Consequently:

- an exact depth-three interface cannot be `O(N)`;
- but its support lower bound remains `o(N log N)`.

This isolates a genuine remaining asymptotic window:

\[
\boxed{
\text{a phase-compatible depth-three interface of size }\Theta(N\log\log N).
}
\]

The connectivity theorem does not construct its Fourier weights.

### 5.3 Growing depth

Pippenger constructed `n`-superconcentrators with at most `40n` edges, logarithmic depth and bounded degree. Therefore support connectivity alone cannot rule out an `O(N)` exact linear circuit.

Any further exact obstruction must use Fourier-specific phase compatibility, not only full rank, total nonsingularity, expansion, treewidth or separator size.

---

## 6. Positive theorem: linear-size full-spark transforms exist

The preceding limitation is real, not a weakness of the proof.

Assign a distinct indeterminate `x_e` to every edge of a superconcentrator DAG and form its path-sum transfer matrix `T(x)` over the rational-function field.

### Theorem 6.1 — generic superconcentrator transfer is totally nonsingular

For every equal-size terminal subsets `I,O`,

\[
\boxed{
\det T(x)[O,I]\ne0.
}
\tag{6.1}
\]

### Proof

The Lindstrom--Gessel--Viennot determinant identity expresses the minor as the signed sum of weights of vertex-disjoint path families from `I` to `O`.

The superconcentrator property supplies at least one such family. Distinct vertex-disjoint path families use distinct edge sets and hence produce distinct monomials in the independent variables `x_e`. Therefore the determinant polynomial is nonzero. QED.

Since there are finitely many minors, over every infinite field there is a simultaneous scalar specialization for which all of them stay nonzero.

Combining this with Pippenger's linear-size superconcentrators gives:

\[
\boxed{
\text{There exist totally nonsingular }n\times n\text{ linear transforms with }O(n)
\text{ exact circuit edges.}
}
\tag{6.2}
\]

This is a nonuniform existence statement. It does not give explicit Fourier-compatible weights, a fixed-precision implementation, or a uniform coefficient generator.

### Interpretation

Total nonsingularity is enough to force superconcentrator support, but it is **not** enough to force `N log N` arithmetic. Full-spark transforms can live on linear-size deep DAGs.

The missing ingredient for Fourier is its exact cyclotomic phase pattern.

---

## 7. Exact executable checks

The package contains a standalone finite-field implementation of:

- path-sum transfer evaluation;
- vertex-splitting max flow for disjoint paths;
- exhaustive superconcentrator verification;
- exhaustive minor verification;
- depth-two factor circuits;
- Benes network controls.

### 7.1 Exhaustive small depth-two supports

Restricting to exactly `n` middle vertices, every support was exhausted at `n=2,3`.

| `n` | minimum edges | number of minimizing supports |
|---:|---:|---:|
| 2 | 6 | 12 |
| 3 | 11 | 216 |

These are small-instance controls, not a proof of the asymptotic theorem.

### 7.2 Benes controls

The exact path checks verified:

| `n` | nodes | edges | depth | terminal-subset pairs checked |
|---:|---:|---:|---:|---:|
| 4 | 16 | 24 | 3 | 69 |
| 8 | 48 | 80 | 5 | 12,869 |

Both graphs are superconcentrators.

Over `F_1000003`, the first deterministic random nonzero edge assignment at each size produced a totally nonsingular transfer:

- `69` minors checked at `n=4`;
- `12,869` minors checked at `n=8`.

This is an exact finite-field positive control for the LGV theorem.

### 7.3 Fourier rectangle controls

The v30 half-rectangles were checked at finite-field Fourier lengths `5,7,11`; every displayed square rectangle had full rank. The entire block was full-spark in the tested fields for lengths `5` and `7`.

A transparent exact depth-two realization `X=M,Y=I` has a superconcentrator support, as Theorem 3.1 predicts, but uses quadratic dense routing.

### 7.4 Negative control

Deleting all edges into one output of the complete depth-two network creates a terminal pair with zero disjoint-path capacity. The corresponding transfer block has rank zero for every edge-weight assignment.

### Test status

\[
\boxed{10/10\text{ automated test groups pass}.}
\]

A second implementation independently verifies the Benes path property, all finite-field minors, and the Fourier rectangle ranks without importing the primary module.

---

## 8. Operation ledger

| Interface architecture for the `m=floor(N/2)` correction | Forced/support cost | Exact FFT status |
|---|---:|---|
| Depth 2 | `Theta(m log^2 m / log log m)` edges | asymptotically worse than `N log N` |
| Depth 3 | `Theta(m log log m)` edges | possible sub-`N log N` support; Fourier weights unknown |
| Benes-style control | `Theta(m log m)` edges | routable/full-spark generic weights; not Fourier |
| General logarithmic-depth superconcentrator | `O(m)` edges exists | connectivity permits linear size; Fourier weights unknown |
| Dense sharp v30 interface | rank `m`, dense routing | exact but not fast |

Coefficient preparation, graph construction, memory traffic and output writes remain charged in any future candidate.

---

## 9. Prior-art and claim boundary

Classical ingredients include:

- Pippenger's linear-size superconcentrators;
- Alon--Pudlak depth-two/depth-three bounds;
- Radhakrishnan--Ta-Shma's tight depth-two bound;
- Menger's theorem;
- the Lindstrom--Gessel--Viennot determinant identity;
- Chebotarev nonvanishing for prime Fourier minors.

Primary references:

1. N. Pippenger, *Superconcentrators*, SIAM J. Comput. 6 (1977), 298--304, DOI `10.1137/0206022`.
2. N. Alon and P. Pudlak, *Superconcentrators of depths 2 and 3; odd levels help (rarely)*, JCSS 48 (1994), 194--202, DOI `10.1016/S0022-0000(05)80027-3`.
3. J. Radhakrishnan and A. Ta-Shma, *Bounds for Dispersers, Extractors, and Depth-Two Superconcentrators*, SIAM J. Discrete Math. 13 (2000), 2--24, DOI `10.1137/S0895480197329508`.
4. B. Lindstrom, *On the Vector Representations of Induced Matroids*, Bull. London Math. Soc. 5 (1973), 85--90, DOI `10.1112/blms/5.1.85`.

The project-specific contribution is the FFT-facing composition:

1. apply the exact rank/flow gate to the sharp v30 Schur correction rectangle;
2. translate bounded-depth superconcentrator bounds into fully charged interface gates;
3. exhibit exact finite-field full-spark controls on explicit routing networks;
4. show precisely why total nonsingularity cannot finish an FFT lower bound.

No literature-wide novelty or priority claim is made.

---

## 10. Honest conclusion and next gate

We still do **not** have an exact `o(N log N)` FFT.

v31 proves:

\[
\boxed{
\text{the sharp linear-dimensional Schur interface must contain a half-size superconcentrator.}
}
\]

Therefore:

- depth two is too expensive;
- depth three has the right `N log log N` scale but lacks Fourier-compatible weights;
- logarithmic depth can have linear support, so graph connectivity alone cannot reject an `O(N)` circuit.

The next exact experiment is now phase-specific:

> Construct a depth-three `Theta(N log log N)` superconcentrator interface whose path-sum transfer is the prime Fourier half-rectangle, or derive a cyclotomic/path-family invariant proving that no such weight assignment exists.

A successful construction must then be inserted into the full Schur system with all coefficient synthesis, branch solves, interface work and output reconstruction charged. A negative theorem must use more than ranks and minors, because generic linear-size superconcentrators already realize totally nonsingular transforms.
