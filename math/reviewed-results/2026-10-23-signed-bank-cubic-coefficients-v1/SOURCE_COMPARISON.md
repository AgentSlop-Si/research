# Bounded primary-source comparison: scalar-span coprime selection

23 October 2026 UTC. Read-only research, with local report creation only. No mathematical acceptance, novelty label, table, repository, or historical program was changed.

## Result

**Known deterministic polynomial-time solvability is established by a matched reduction to an existing constructive matrix-space theorem.** This is stronger attribution than merely calling the ingredients “genericity” or Schwartz–Zippel. The reduction preserves the original scalar span, arbitrary characteristic, repeated factors, and an optional nonzero linear functional. It requires no factoring or computed extension.

**An equal/better predecessor for the candidate's O((s+v)L^2) schoolbook selector, O(v) scalar-trial amortization, or complete O(N^3) deterministic coefficient stage was not established in this bounded pass.** This is a source gap, not historical novelty clearance. A general polynomial-time theorem must not be relabeled as a matching cubic algorithm.

## 1. Frozen target

Input: a nonzero degree-v polynomial a, polynomials b_1,...,b_s of degree at most L with L>=v, and gcd(a,b_1,...,b_s)=1. Output must be p=sum c_j b_j with c_j in k and gcd(a,p)=1. Optionally phi(p)!=0 for a supplied nonzero k-linear functional phi on W=span_k{b_j}. A represented distinct-scalar list is part of the effective field interface.

The candidate reverse-gcd theorem claims O((s+v)L^2) additions/multiplications, O((s+v)L) inversions, and O(sL+v^2+L) storage, using v+2 distinct supplied scalars, with s,L,v=O(N) in the two original pencils. Its mathematical status is **candidate**, not changed by this report. The accepted fast-axis packet currently gives the preceding O(N^4) deterministic coefficient-stage bound. The expected Las Vegas O(N^3) bound already predates this candidate.

Exact local source hashes and original-pencil bindings are in BINDINGS.json. The original gate N odd, d>=4, N>=8d-10 and all root-field/bank obligations remain unchanged.

## 2. Inspected primary theorem

G. Ivanyos, M. Karpinski, Y. Qiao, M. Santha, *Generalized Wong sequences and their applications to Edmonds' problems*, J. Computer and System Sciences 81(7) (2015), 1373–1386, [DOI 10.1016/j.jcss.2015.04.006](https://doi.org/10.1016/j.jcss.2015.04.006). Primary bodies inspected: [author/institutional manuscript](https://opus.lib.uts.edu.au/bitstream/10453/159685/2/rkone_journal_20150205.pdf), Theorem 2, Section 5.2, Algorithm 1; also [arXiv v2](https://arxiv.org/pdf/1307.6429v2), Theorem 2 and Section 5.

Theorem 2 supplies a deterministic polynomial-time constructive SDIT algorithm on an algebraic RAM for triangularizable n-by-n matrix spaces over fields with at least n+1 elements. Triangularizability may hold only over an extension; the algorithm does not construct that extension. It returns scalar coefficients of a nonsingular combination, when one exists. Algorithm 1 uses recursive first Wong sequences and tests pairs of scalars from an (n+1)-element set when assembling a solution. Its claimed bound is polynomial time, not an explicit cubic bound. The base-field result is not restricted to characteristic zero or perfect fields. The inspected text does not give the reverse-gcd degree-drop amortization.

## 3. Exact reduction, derived here

This section is our mathematical mapping, not a claim that the source paper states a polynomial-selection corollary.

Normalize a to monic and let R=k[t]/(a). For each original b_j form the v-by-v matrix M_j of multiplication by its residue in R, in the coefficient basis 1,t,...,t^(v-1). For c=(c_1,...,c_s),

    M(c)=sum_j c_j M_j = multiplication by p=sum_j c_j b_j modulo a.
    M(c) nonsingular  <=>  p is a unit in R  <=>  gcd(a,p)=1.

The last equivalence is the ordinary unit criterion. A Bezout identity may prove it, but **no polynomial-coefficient Bezout combination is returned as p**. The output is assembled from the original b_j using only the scalar coefficients returned by the matrix algorithm.

Let C be the companion multiplication matrix of t modulo a. Then M_j=b_j(C). Over an algebraic closure, a basis triangularizing C triangularizes every polynomial b_j(C). Thus the supplied matrix space satisfies the theorem's triangularizability promise without computing roots, factors, eigenvectors, or an extension.

Multiplicity is retained. If a splits over the algebraic closure as product_r (t-r)^(m_r), then

    det M(c) = product_r (sum_j c_j b_j(r))^(m_r).

The joint gcd condition makes each displayed linear factor nonzero as a polynomial in c. Therefore the determinant polynomial is nonzero, of degree v. A grid of v+1 distinct represented scalars contains a nonvanishing point. This proves existence only; the actual deterministic selection is furnished by the cited constructive algorithm, not an exponentially enumerated grid. Neither squarefreeness nor separability is used.

For the endpoint contract use instead

    B_j = diag(M_j, phi(b_j)),       n=v+1.

These matrices still commute and are simultaneously triangularizable. Their scalar-combination determinant is

    det(sum_j c_j B_j) = det M(c) * phi(sum_j c_j b_j).

Since phi is nonzero on W, this is a nonzero polynomial of degree v+1. The supplied v+2-element list is sufficient. Crucially, phi is evaluated on the **original polynomials**, not on arbitrarily chosen quotient representatives; phi need not descend to R. This avoids a possible endpoint-loss error.

## 4. Paid implementation comparison

The conversion is not free. Reducing each b_j modulo monic a costs O(Lv) schoolbook field operations. Once its first column is known, successive columns of M_j are obtained by multiplying a residue by t and reducing once, in O(v) operations each. Thus all matrices cost O(sLv+s v^2+sL) operations, including optional functional evaluations and scalar-output reconstruction, and O(sv^2+sL) stored field elements if materialized.

For a fully priced, deliberately conservative implementation of the cited matrix algorithm, put n=v or v+1. With ordinary elimination and its printed two-scalar grid, a bound is

    O(sLv + s^2 n^5 + n^6) field operations,

where inversions and equality tests are charged as field operations. Here is our accounting, not an exponent claimed by the authors: at matrix dimension r, each first-Wong iteration is a collection of images/preimages computable in O(sr^3); at most r iterations for each of s generators cost O(s^2 r^4). Common kernels, quotient maps, and basis changes fit below this. The (r+1)^2 grid tests cost O(r^5) using cubic determinants. Summation over strictly decreasing recursive dimensions gives the displayed bound. Matrices and scratch space can be stored within polynomial space; even the top-level explicit input already has s n^2 entries.

This upper bound is intentionally not tight and is **not a lower bound** on this source or this problem. Homogeneity already permits replacing the two-scalar grid by a one-scalar pencil; that observation alone does not yield the candidate's total O(v) trials or compact schoolbook bound. Structured specialization may do much better, but must be proved and priced rather than silently imported.

For s,L,v=O(N), the materialized general method therefore establishes deterministic polynomial-time selection with a conservative O(N^7) implementation, not a verified O(N^3) baseline. The candidate retains the compact polynomial representation and offers the sharper charged bound. No claim of asymptotic superiority to all prior algorithms follows.

## 5. What this permits saying

- Safe: “Deterministic polynomial-time scalar-span coprime selection, including the endpoint constraint and repeated factors, is a consequence of known constructive triangularizable matrix-space algorithms.”
- Safe: “The proposed reverse-gcd implementation provides a compact O(N^3) coefficient-stage bound relative to the current project's O(N^4) deterministic implementation, subject to independent mathematical review.”
- Unsafe: “Deterministic selection is a new problem/result,” “the published theorem already proves this precise cubic bound,” or “the reverse-gcd amortization is historically new.”
- Unchanged: no smaller-bank, efficient root-splitting/recovery, full cold-compiler, bit-complexity, or Fourier/FFT speedup claim.

## 6. Search boundary and stopping condition

This bounded pass searched scalar coprime combinations, constructive prime avoidance, unit/nonzero-divisor selection in subspaces, and constructive singularity testing for commuting/triangularizable matrix spaces. The matched theorem above is based on inspected primary bodies, not abstracts alone. Polynomial Bezout algorithms, randomized gcd-combination results, arbitrary coprime-pair generation, and unpriced factoring were not used as substitutes. Other module-isomorphism and Cartan-subalgebra papers were locators only, not claimed matches. One earlier-module-paper PDF timed out; no conclusion depends on it. PDF screenshot attempts were unavailable; readable primary PDF text was inspected, without claiming page-image verification or byte-identical archival certification.

Stop this pass here. A useful next attribution pass should be triggered by a concrete source claiming the same compact scalar-span algorithm or an explicit equal/better operation bound, not by an unbounded search for novelty clearance. External PDFs are linked, not redistributed.
