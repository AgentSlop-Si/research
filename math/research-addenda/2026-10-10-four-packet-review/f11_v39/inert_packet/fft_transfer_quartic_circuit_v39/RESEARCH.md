# Exact global quartic-freeness of the 99-edge transfer variety — v39

**Date:** 11 October 2026  
**Goal:** Fully charged, exact full-output FFT on arbitrary fresh inputs, eventually `o(N log N)` arithmetic and preferably `O(N log log N)` or `O(N)`.  
**Actual result:** A graph-specific exact algebraic-geometry theorem. No exact Fourier edge assignment or faster FFT has been found.

## 1. Preserved object and prior checkpoint

The graph is **exactly** the frozen `topology_11.json` from v33 through v38. It has four vertex layers, each of size 11, and 33 independently weighted edges between each consecutive pair. With its 99 independent edge variables, its transfer is

\[
H(a)=C(a)B(a)A(a),\qquad H_{ij}(a)=\sum_{P:j\rightsquigarrow i}\prod_{e\in P}a_e.
\]

Every path has three edges. The 121 entries have the path-count histogram `22×1`, `42×2`, `39×3`, `16×4`, `2×5`; altogether there are 297 paths.

v38 established that the complex closure of the image of this map has dimension 77, codimension 44, and that its homogeneous coordinate ideal contains no relation in transfer degree 1, 2, or 3. v38 also proved no degree-4 relation using **only 64** one- or two-path entries. The intact v38 bundle is `PRIOR_v38_COMPLETE.zip` (SHA-256 `9e55fd16931b5f084532719f3836309b1092932fd920f5469a74b2279aa6c5bb`).

## 2. Main theorem: zero relations through global quartic degree

Let \(K=\mathbb C\) and define

\[
\phi^*:K[h_{00},\ldots,h_{10,10}]\to K[a_0,\ldots,a_{98}],
\quad h_{ij}\mapsto H_{ij}(a).
\]

**Theorem 2.1 (exact over \(\mathbb C\)).**

\[
\boxed{\ker\phi^*\cap K[h]_{\le4}=\{0\}.}
\]

Equivalently, **all**

\[
\binom{124}{4}=\boxed{9,381,251}
\]

quartic products of the 121 transfer entries are linearly independent after expansion as polynomials in the 99 edge weights. This covers **every** quartic relation in the full output matrix, not only the 64-coordinate subset previously checked.

### Proof, part A: exact row/column multigrading

Give each first-layer edge \(a_e\), of source \(j\), formal column degree \(e_j\in\mathbb N^{11}\). Give each third-layer edge \(c_e\), of destination \(i\), formal row degree \(e_i\). Middle-layer edges have zero row and column multidegrees. Each path contributing to \(H_{ij}\) uses precisely one first-layer edge sourced at \(j\) and one third-layer edge ending at \(i\). Consequently

\[
\operatorname{bideg}H_{ij}=(e_i,e_j).
\]

A product of four transfer entries has therefore one multidegree determined by a **multiset of four row indices** \(R\) and a **multiset of four column indices** \(C\). Distinct pairs \((R,C)\) have disjoint support in the original edge-monomial basis and cannot cancel against one another.

There are exactly

\[
\binom{11+4-1}{4}=1001
\]

row multisets and the same number of column multisets, giving **1,002,001** separate linear-independence problems. Inside one block \((R,C)\), distinct degree-four transfer monomials correspond to different pairings of the four row slots to the four column slots. There are at most \(4!=24\) such pairings; duplicates from repeated labels are removed exactly.

The exhaustive block-size distribution is:

| Number of monomials in one block | Number of blocks |
|---:|---:|
| 1 | 21,901 |
| 2 | 24,200 |
| 3 | 111,925 |
| 4 | 127,050 |
| 6 | 36,300 |
| 7 | 245,025 |
| 12 | 326,700 |
| 24 | 108,900 |
| **Total** | **1,002,001** |

The weighted sum of column counts is exactly **9,381,251**.

### Proof, part B: exact modular evaluation-rank certificates

For a block with \(k\le24\) transfer monomials \(m_1,\ldots,m_k\), evaluate them at 24 deterministic assignments of the original 99 independent edge weights over the finite field \(\mathbb F_{1,000,003}\). Form

\[
E_{st}=m_t(H(a^{(s)})),\quad 1\le s\le24,\ 1\le t\le k.
\]

If \(E\) has column rank \(k\), no polynomial linear dependency among that block's monomials exists. `full_quartic_blocks.cpp` checks all 1,002,001 blocks using exact modular arithmetic. It uses a fixed xorshift64 seed `20261011`; no floating point is used. The first \(k\) rows have full rank except for exactly **one** block; that block attains full rank when all 24 rows are allowed. **No block remains deficient.** A repeatable hash of the complete evaluated transfer data is `6774884542161267937` (FNV64).

An independent verifier, `independent_quartic.cpp`, reimplements the path transfer by directly enumerating the 297 three-edge paths rather than using the primary matrix-product method. It uses a different PRNG, seed `972524161`, prime \(1,000,033\), a separately written enumeration of multiset pairings and a column-oriented rank algorithm. All **1,002,001** blocks and **9,381,251** monomials again have full rank, this time without even needing an extra evaluation row. Its transfer-sample FNV64 hash is `11690676381034439803`. A third verifier, `audit_samples.py`, independently recomputes both fingerprints with explicit Python path sums.

All these evaluated entries and matrices have integer-polynomial formulas before modular reduction. Full rank modulo a prime yields a nonzero integer minor of the formal edge-monomial coefficient matrix. That minor stays nonzero over \(\mathbb Q\), and hence over \(\mathbb C\). Thus the two finite-field computations are **exact characteristic-zero linear-independence certificates**, not random approximations to complex roots.

### Proof, part C: degrees below 4

Every \(H_{ij}\) is homogeneous of total edge degree 3. A polynomial relation mixing different total transfer degrees splits into homogeneous pieces because those pieces have different edge degrees. If there were a nonzero homogeneous transfer relation of degree \(d<4\), multiplying it by \(h_{00}^{4-d}\) would create a nonzero degree-four relation (the target polynomial ring has no zero divisors). Theorem 2.1 follows.

**Scope:** This modular proof establishes the stated result over \(\mathbb C\) (and the two certificate characteristics). Unlike v38's unit-pivot proof through degree 3, v39 does **not** claim validity in every possible characteristic.

## 3. A 77-coordinate transcendence basis and 78-coordinate dependency

The 22 hidden vertices admit independent nonzero gauge rescalings; on the edge torus, these leave \(H=CBA\) unchanged. This gives the structural dimension upper bound \(99-22=77\). v38 verified a nonzero full-size Jacobian minor, proving equality.

v39 improves the *choice of coordinates*: choose the 77 transfer entries with the smallest number of contributing paths (breaking ties by \((i,j)\) lexicographic order). The file `transcendence_basis.json` gives the explicit 77 row IDs and the 77 original edge-weight columns of a Jacobian minor. At the exact integer weight assignment inherited from v38, its determinant is

\[
\boxed{556448\pmod{1,000,003}\ne0.}
\]

This determinant was independently recomputed via the product rule for \(H=CBA\), rather than the original path differentiation. Therefore these **77 specified transfer polynomials are algebraically independent over \(\mathbb C\)** and form a transcendence basis of the function field of the 77-dimensional transfer variety.

Add the next simplest output entry, creating a set of 78. Any 78 functions on a 77-dimensional irreducible variety are algebraically dependent. The supplementary saved `quartic_pivots.npz` certificate nevertheless proves that *all 1,663,740 quartic products* among these 78 outputs are independent. Its monomial expansion contains **21,770,715** path-quartet contributions and **19,337,020** distinct edge monomials, with exact unit-peeling rounds

\[
1,634,924+28,756+60=1,663,740.
\]

This independently reinforces the conclusion that an **already dependent** set of output entries has no equation of degree below 5. The global theorem subsumes the quartic part, but the unit-pivot proof has the stronger any-field scope for this selected subset.

The saved finite-field tangent null vector for these 78 entries has support 76. **Do not treat that sampled modular support alone as proof of a characteristic-zero algebraic-matroid circuit**: the dimension argument establishes dependence of the full 78-set, while the explicitly verified 77-simple-output minor establishes the named transcendence basis.

## 4. Robustness and negative controls

- Independent full-block auditors agree in different prime fields and from different transfer-evaluation algorithms.
- Python path-sum re-evaluation matches both complete sample fingerprints.
- A deliberately degenerate evaluation table, replacing every sample by the first transfer matrix, produces **18,810** persistent rank-deficient blocks across just 20 row multisets. The detector rejects that control as required.
- The predecessor v38 ZIP SHA-256 and ZIP CRC are rechecked.
- The default `python run_all.py` performs **11** test groups; `python run_all.py --extended` additionally regenerates the entire 78-output, 21,770,715-term unit-pivot certificate.
- `MANIFEST.sha256` pins the complete v39 code and saved data. A clean extraction and cold rerun are documented in `run_all.log`.

## 5. Arithmetic ledger and what remains open

If an explicit exact assignment of 99 edge weights for \(F_{11}\) were known, applying this graph to a fresh vector would require exactly **99 scalar multiplications and 66 additions** through its three 33-edge layers. No such weight assignment was constructed, and the graph is for the single length 11. It does **not** establish a uniform all-length FFT family or any new \(o(N\log N)\) arithmetic bound.

The v39 certificates are offline proof computations. Their evaluation, sorting, rank audits and edge-weight selection costs must not be silently counted as a speedup for new input vectors. The actual Fourier feasibility question

\[
\exists a_0,\ldots,a_{98}\in\mathbb C^*,\qquad C(a)B(a)A(a)=F_{11}
\]

**remains unresolved**. The first possible nonzero polynomial identity in *all* 121 transfer coordinates has degree **at least 5**, but no explicit quintic equation or Fourier-separating obstruction is supplied.

## 6. External context and prior-art boundary

Multigraded algebra, polynomial evaluation-rank certificates, Jacobian dimension, algebraic matroids and network path matrices are established techniques. Important background includes the Lindström–Gessel–Viennot determinant method and Kelli Talaska, *Determinants of weighted path matrices* (2012, arXiv:1202.3128). The paper *A two-pronged progress in structured dense matrix-vector multiplication* discusses sparse product width as a representation measure. The contribution here is an **exact exhaustive result for this one frozen graph**, not a claim to have invented those techniques or a literature-wide novelty/prioritization proof.

A separate OpenAI mathematics preprint dated 25 September 2026 states an asymptotic exact all-length DFT bound \(O(N(\log N)^{1-10^{-13}})\) in an exact-complex-register model with supplied roots. That outside result does not provide this project's hypothesized \(O(N\log\log N)\) or \(O(N)\) construction. This project has not independently reproduced the outside theorem.

## 7. Next mathematical gate

A legitimate separating polynomial for \(F_{11}\), if the target lies outside the image closure, now requires **degree at least 5** in the 121 transfer entries. The row/column multigrading reduces degree-5 searches to blocks of at most \(5!=120\) monomials, suggesting a tractable *targeted* strategy rather than one gigantic global expansion. A different route is exact weight elimination using the v37 forced-path-product identity and the v36 coupled cancellation constraints, allowing nonintegral cyclotomic valuations.

**Do not repeat:** degree ≤4 transfer-only identity searches on this same fixed topology; arbitrary-prime characteristic extensions of the new modular proof; mislabeling full-spark compatibility as an exact Fourier factorization; or claiming a single 11-point topology is an asymptotic FFT speedup.
