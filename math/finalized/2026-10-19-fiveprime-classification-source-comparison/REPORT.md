# Order 5q fixed-Fourier masks: bounded prior-art comparison

Checked 19 October 2026. **No directly subsuming theorem was found in the inspected statements. Historical priority remains unresolved.** This is a hypothesis-and-conclusion comparison, not a mathematical re-audit or an exhaustive literature review.

## Exact target

For every prime q>5, N=5q, a primitive complex Nth root ζ, and an arbitrary binary N×N matrix R, set D[r,c]=R[r,c]ζ^(rc). The accepted result says that DD*=D*D=dI is possible exactly for d∈{0,1,5,q,5q}. It classifies degrees, not all supports.

The target theorem, dependency ledger, synthesis, and relevant component passages were inspected. The dependence is significant: P supplies the low and strict-high ranges; F and B split the first interior at q≥11 and q=7; M and U supply the next two interiors; K handles 2q,3q,4q. The literature question concerns the combined arbitrary-mask compatibility argument, rather than whether two-prime cancellation or Fourier divisor constructions were previously known. No proof or numerical control was rerun for this comparison.

For d>0 the target belongs to CGW(N,d;N), the class of complex generalized weighing matrices with nonzero entries among Nth roots. It has the extra **position-by-position phase prescription** D[r,c]/ζ^(rc)∈{0,1}. The UW/CGW terminology alone does not impose this prescription, and arbitrary monomial equivalence need not preserve it.

## Inspected comparisons

### 1. Unit weighing matrices: a genuine partial match, not the classification

Best–Kharaghani–Ramp, *On unit weighing matrices with small weight*, Definition 1 (p.1), Theorem 10 (p.5), Theorem 12 and Corollary 13 (pp.7–8), and Lemma 15 (p.10), allow arbitrary unit-modulus nonzero entries. Theorem 10 directly excludes d=2 here because 5q is odd. The weight-3 and weight-4 classifications concern freely chosen phases; in particular, Corollary 13 permits UW(5q,3), while the target forbids degree 3 with its prescribed phases. This is not a counterexample: the alphabets and positional constraints differ. The paper treats weights below five and a few sporadic weight-five cases, not every degree at order 5q. [Primary preprint, arXiv:1209.4581v2](https://arxiv.org/pdf/1209.4581v2).

### 2. Cyclotomic group-invariant weighing methods require another hypothesis

Tan, *Group Invariant Weighing Matrices*, defines G-invariance on p.1 by simultaneous translation of row and column labels. The generalized multiplier theorem, Theorem 3.4 (pp.7–8), assumes a cyclotomic group-ring element X with XX^(−1)=n, gcd(n,|G|)=1, and an ideal-fixing multiplier. Corollary 4.1 (p.9) gives a bound for G-invariant integer weighing matrices. These are substantive cyclotomic tools, but the target does not assume translation-invariant support, group-developed entries, or coprimality of d and N. The inspected statements provide no reduction from an arbitrary fixed-Fourier mask to that group-ring setting. This is a conditional applicability gap, not proof that no such reduction exists. [Primary paper, arXiv:1610.01914v4](https://arxiv.org/pdf/1610.01914v4).

### 3. Cohomology-developed matrices: prescribed automorphism data, not arbitrary masks

Goldberger–Dula, *Cohomology-developed matrices*, §§1–2 (pp.1–9) studies lifting an automorphism action on a binary support to a monomial action. Theorem 5.2(c) (p.28; proof p.29) yields AA*=cI when the specified (P,P)-action has a single orientable orbit. This is a sufficient orthogonality mechanism inside a representation-defined matrix space. The target starts with arbitrary R and assumes orthogonality; it does not supply that action or the orientable-orbit condition. The inspected theorem does not classify its possible d or establish the missing symmetry reduction. [Primary preprint, arXiv:1903.00471v3](https://arxiv.org/pdf/1903.00471v3); published version: [Journal of Algebraic Combinatorics](https://doi.org/10.1007/s10801-024-01346-7).

### 4. A 2026 CGW classification is expressly symmetry- and size-restricted

Egan–Ó Catháin–Švob, *Complex generalised weighing matrices in centraliser algebras of monomial representations*, Theorem 3.1 (p.6), requires an indecomposable matrix of order n≤80, n≠64, a primitive strong-automorphism permutation group of rank 2–5, and a specified orbital-coefficient condition with k∈{2,3,4,5,6}. The latter bounds the orbital coefficients, not necessarily every phase appearing in a reconstructed matrix. The conclusion is membership up to monomial equivalence in their census. The target neither assumes this symmetry nor bounds q. Proposition 2.7 (p.5) also retains a rank-3 centraliser-algebra hypothesis. Thus neither inspected statement directly supplies the target. [Primary July 2026 preprint, Theorem 3.1](https://arxiv.org/html/2607.16069v1); [PDF](https://arxiv.org/pdf/2607.16069v1).

### 5. Hadamard trades change phases while retaining full Hadamard matrices

Ó Catháin–Wanless, *Trades in complex Hadamard matrices*, Lemma 3 (pp.3–4) characterizes scalar switching of a rectangle through cross-orthogonality; Theorem 7 (pp.6–7) bounds rectangular trade size and identifies the equality case. The objects before and after switching have all entries of modulus one. A zeroed fixed-phase matrix with DD*=dI is a different object, and the target does not assert that its support is a switchable trade. [Primary preprint, arXiv:1502.02353v1](https://arxiv.org/pdf/1502.02353v1).

The newer Crnković–Egan–Švob preprint proves that every complex-Hadamard trade has at least n entries (Theorem 6.3, p.17); Theorem 4.3 (p.10) gives a partition-based switching condition. These conclusions still concern phase replacement and trade size, not the attainable weights of arbitrary zeroed Fourier matrices. [Primary preprint, arXiv:2511.07020v1](https://arxiv.org/pdf/2511.07020v1).

### 6. Two-prime vanishing sums are inherited, essential prior work

Lam–Leung, *On Vanishing Sums of Roots of Unity*, Theorem 3.3 and Corollary 3.4 (pp.7–8), describe the positive two-prime cycle structure and explicitly credit de Bruijn §3. This supplies the local cancellation ingredient used in the accepted proof. For two target rows r,s the sum is over S_r∩S_s, so a theorem about a single vanishing sum does not identify its length with the full row degree d. The global row/column compatibility and exclusions of all interior intervals and q-multiple endpoints are additional claims to compare. [Primary preprint, arXiv:math/9511209v1](https://arxiv.org/pdf/math/9511209v1).

### 7. Spectral-set and Fourier-submatrix theorems remain conditional comparisons

Malikiosis–Kolountzakis, Theorem 1.2 (p.2), implies that a spectral subset of Z_(5q) tiles, hence its cardinality divides 5q. The hypothesis is orthogonality of characters on one common set. Applying it to d requires a reduction of the arbitrary entry-mask problem to such a spectral set; the scalar-Gram hypothesis does not state that reduction. [Primary paper](https://arxiv.org/pdf/1612.01328v2).

Herr–Wiegand, Definition 1.1 (p.2), Theorem 2.1 (p.7), and Theorem 2.6 (p.10), select complete Cartesian submatrices J×K and analyze their primitive sets. Those statements do not quantify over entry-dependent zeros in an N×N mask. This check is included for continuity; the comparisons above expand the coverage well beyond it. [Primary paper](https://arxiv.org/pdf/1909.13145v4).

### 8. Arithmetic GW/CGW conditions: useful source guide, original-source gap

Egan's survey, §2 (pp.3–5), distinguishes complex root-of-unity CGWs from generalized weighing matrices defined over a group-ring quotient. It identifies these classes for prime group order and presents de Launey's prime-alphabet conditions as Theorems 2.3–2.4. Here the natural alphabet order is composite, 5q; one cannot substitute 5 or q without an additional justified phase reduction. Its determinant condition (Lemma 2.2) is necessary but is not stated as the target classification. This paragraph records the inspected survey's scope; the original de Launey theorems were not retrieved. [Survey/source guide, arXiv:2309.07522v2](https://arxiv.org/pdf/2309.07522v2).

## Explicit coverage limits and stopping point

- **de Launey (1984), *On the non-existence of generalized weighing matrices*, pp.117–132:** publisher contents verified, original article unread. The theorem numbering above is from Egan's cross-reference, not a first-hand check. [Publisher volume](https://combinatorialpress.com/ars/vol17a/).
- **Berman (1978), *Families of Generalized Weighing Matrices*, pp.1016–1028:** publisher record/extract inspected; full paper not retrieved in this pass. No theorem-level exclusion of this original is claimed. [Publisher record](https://www.cambridge.org/core/journals/canadian-journal-of-mathematics/article/families-of-generalized-weighing-matrices/91032F29E0984321260A608E67513D16).
- **de Bruijn (1953), *On the factorization of cyclic groups*, pp.370–377:** original unread here; historical credit is supported by Lam–Leung's explicit attribution.
- **Craigen–de Launey (2016), *Constructions for Circulant and Group-Developed Generalized Weighing Matrices*, pp.406–420:** identified through the inspected CGW bibliography; original unread. Likewise, historical books, differently named formulations, and reductions not stated in the passages above remain outside this bounded check.

Searches covered unit/complex/Butson/generalized weighing matrices, cyclotomic and group-invariant methods, cohomology/centraliser classifications, Fourier entry deletion, and Hadamard trades, including the identified 2025–2026 preprints. Searches returning only signal-processing masks were not treated as mathematical prior art. No claim of exhaustive indexing or exhaustive reading is made.

**Recommended disposition:** retain the exact theorem and its classical cancellation attribution, but do not attach a historical novelty claim. A specialist in complex weighing matrices and finite cyclic spectral theory should check whether an existing arbitrary-mask structural theorem or an additional reduction subsumes the global 5q compatibility argument. The precise question is degree necessity for R[r,c]ζ^(rc), with arbitrary binary R, not generic CGW existence or common-support spectral cardinality.

This report contains original comparisons and bibliographic links only. No full papers, extensive quotations, or external writes are included.
