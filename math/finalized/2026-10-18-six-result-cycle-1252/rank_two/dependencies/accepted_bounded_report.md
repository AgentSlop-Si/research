# Higher-rank Fourier tilings: balanced divisors and twice-prime lengths

Date: 18 October 2026. Owner: M-RECTANGLE-TILING, priority 42.
Status: new author-side theorem and checks; independent acceptance pending.

## Result

Let

\[
D_N=\min_{d\mid N}(d+N/d),\qquad N\ge2.
\]

Partition all entries of the complex cyclic Fourier matrix into nonempty, disjoint Cartesian rectangles. If a rectangle has side lengths \(a_t,b_t\) and matrix rank \(r_t\), charge the declared independent-contraction objective

\[
\mathcal C=\sum_t r_t(a_t+b_t).
\]

**Theorem.** If \(D_N^2<8N\), then the exact optimum over arbitrary-rank disjoint tilings is

\[
\boxed{\min\mathcal C=N D_N.}
\]

Every minimizing tiling consists entirely of rank-one rectangles. Every tile is a full product of a subgroup coset and an annihilator coset, with side lengths a minimizing divisor pair. Consequently every optimizer has exactly \(N\) tiles, each of area \(N\).

This settles the higher-rank extension for a complete infinite family of nonsquare composite lengths, rather than repeating the accepted rank-one theorem. The hypothesis holds whenever the closest divisor pair \(d\le e\), \(de=N\), has

\[
e/d<3+2\sqrt2.
\]

In particular it holds at every power of 2, 3, or 5. For nonsquare powers \(p^{2k+1}\), with \(p\in\{2,3,5\}\), the optimum is

\[
p^{3k+1}(p+1).
\]

**Additional theorem.** For every odd prime \(p\), at \(N=2p\) the same exact optimum and rank-one-only equality conclusion hold, with

\[
\boxed{\min\mathcal C=2p(p+2).}
\]

This includes arbitrarily unbalanced lengths outside the balanced-divisor hypothesis. The proof uses the accepted characteristic-zero prime-Fourier nonvanishing-minors theorem in a new same-parity submatrix reduction; see Section 3a.

Perfect-square and prime-length results were already accepted in the source; their overlap is not counted as a new theorem. The new content is the arbitrary-rank conclusion at eligible nonsquare composite lengths, the forced rank-one equality structure, and the bounds below.

For all lengths, including outside the theorem's hypothesis, the same argument gives the improved general sandwich

\[
N\min\{D_N,2\sqrt{2N}\}\ \le\ \min\mathcal C\ \le\ N D_N.
\tag{1}
\]

No claim of worldwide novelty is made. The argument is a short combination of the accepted subgroup classification with integrality of rank and the standard stable-rank estimate.

## 1. Exact source and model boundary

The repository source baseline is commit `49287d9072fb034d320138f1a762edd13afd98a9`. Its open-record index states that M-RECTANGLE-TILING's genuine remaining owner gate is the higher-rank disjoint-tile optimum for general nonsquare composite \(N\). The October 9 Phase7 audit, fetched afresh through the repository connector at that exact commit, proves:

1. The rank-one optimum \(N D_N\), using the subgroup/annihilator classification.
2. The arbitrary-rank lower bound \(2N^{3/2}\), and equality at perfect squares.
3. The prime characteristic-zero optimum from full spark.

That audit explicitly leaves general nonsquare composite higher-rank optimality open. The exact published source bytes have SHA-256 `ed3a259cc88ecb2cf12092f612aabaeb917885fe84147cf2feb99802d1fd32c4` and Git blob `58be131bc82c3ccc7dfb15b435d01bd9edd17942`; both were reconstructed from the fetched bytes. The filename retains the earlier unsanitized artifact's SHA-256 `795e4df8406b0accd35e25f8a0e64015f66c3993c973b29b14bdf823c3c1e56b`, which is not the published copy's byte hash. The published copy replaces private Library identifiers with `[private-id]`; it is the actual source used here. The fresh copies and precise URLs are in SOURCE_PHASE7_AUDIT.md, SOURCE_OPEN_GATE.json, and SOURCES.json. No local historical artifact was treated as current without a pinned repository read.

We retain precisely the disjoint, no-sharing, rank-factor endpoint-incidence objective. The theorem uses the complex Fourier matrix, with a supplied primitive root. Scalar normalization by \(N^{-1/2}\) does not affect ranks or the objective. Arbitrary overlapping/cancelling factorizations and circuits sharing intermediate sums between rectangles are outside the model. No arithmetic-circuit lower bound, cold-cost guarantee, bit-cost bound, FFT speedup, finite-field norm statement, or production claim follows.

## 2. Two local inequalities

Write \(F_N[k,j]=\omega^{-kj}\), with \(\omega\) a primitive complex \(N\)-th root. Let \(R,C\) be nonempty row and column sets of sizes \(a,b\), and let \(r=\operatorname{rank}F_N[R,C]\).

### Lemma 1: stable rank, retaining integer rank

\[
ab\le Nr,\qquad r\in\{1,\ldots,\min(a,b)\}.
\tag{2}
\]

**Proof.** Every entry has modulus one, so the squared Frobenius norm is \(ab\). Restricting rows and columns does not increase operator norm, while \(F_N^*F_N=NI\); hence every singular value of the rectangle is at most \(\sqrt N\). There are exactly \(r\) nonzero singular values, so their squared sum is at most \(Nr\). Nonempty Fourier rectangles contain a nonzero entry, giving \(r\ge1\). □

For any \(r\ge2\), arithmetic-geometric mean and (2) now yield the strictly stronger rank-stratified bound

\[
\frac{r(a+b)}{ab}
\ge \frac{2r}{\sqrt{ab}}
\ge 2\sqrt{\frac rN}
\ge 2\sqrt{\frac2N}.
\tag{3}
\]

This is the missing local observation: the source's bound did not separate the integer cases \(r=1\) and \(r\ge2\).

### Lemma 2: exact rank-one density and its equality case

If \(r=1\), then

\[
a+b\ge \frac{D_N}{N}\,ab.
\tag{4}
\]

Equality forces \(R\) to be a full coset of some subgroup \(H\le\mathbb Z_N\) of order \(d\), \(C\) to be a full coset of its annihilator \(H^\perp\) of order \(N/d\), and \(d+N/d=D_N\).

**Proof.** Choose \(k_0\in R\), \(j_0\in C\). Rank one is equivalent to every multiplicative four-entry ratio being one, so

\[
N\mid(k-k_0)(j-j_0)\quad\text{for all }k\in R,j\in C.
\]

Let \(H\) be generated by all row differences. Then \(R\subseteq k_0+H\) and \(C\subseteq j_0+H^\perp\). Writing \(d=|H|\), we get \(a\le d\), \(b\le N/d\), and

\[
\frac{a+b}{ab}=\frac1a+\frac1b
\ge\frac1d+\frac dN
=\frac{d+N/d}{N}\ge\frac{D_N}{N}.
\]

Equality in the first inequality requires simultaneously \(a=d\) and \(b=N/d\); the last inequality requires the minimizing divisor pair. These conditions are also sufficient. □

Lemma 2 is reproved here to make the extension self-contained; its rank-one content is inherited, not counted as new.

## 3. Global optimality, strict equality, and a quantitative gap

Let \(A_{\ge2}\) be the total area of tiles whose rank is at least two. Disjoint coverage gives total area \(N^2\). Applying (4) to rank-one tiles and (3) to the others gives

\[
\mathcal C\ge N D_N+
\left(2\sqrt{\frac2N}-\frac{D_N}{N}\right)A_{\ge2}.
\tag{5}
\]

If \(D_N^2<8N\), the coefficient of \(A_{\ge2}\) is strictly positive. Thus every tiling costs at least \(N D_N\), and any tiling containing a rank-at-least-two tile costs strictly more. Equality additionally forces equality in every rank-one inequality (4), giving the claimed full-coset structure. Every such tile has area \(N\), so precisely \(N\) are required.

To attain the bound, choose a minimizing divisor pair \(d e=N\), and put

\[
R_u=\{u+ke:0\le k<d\},\quad 0\le u<e,
\]
\[
C_v=\{v+\ell d:0\le\ell<e\},\quad 0\le v<d.
\]

The \(N\) rectangles \(R_u\times C_v\) partition the matrix. Their row and column difference products are multiples of \(N\), so each has rank one. Their total cost is \(N(d+e)=ND_N\). This proves attainment and the theorem.

Formula (5) also quantifies near-optimality. On this domain, a tiling of cost at most \(ND_N+E\) satisfies

\[
A_{\ge2}\le\frac{N E}{2\sqrt{2N}-D_N}.
\tag{6}
\]

For arbitrary \(N\), using the smaller of the two local density constants instead gives the lower bound in (1); the same coset construction gives its upper bound.

### 3a. Exact completion for every twice-prime length

Let \(N=2p\), with \(p\) an odd prime. For any Fourier rectangle with \(a\le b\),

\[
r\ge\left\lceil a/2\right\rceil.
\tag{7}
\]

To prove (7), take the larger parity class among its rows and the larger parity class among its columns. They contain at least \(\lceil a/2\rceil\) and \(\lceil b/2\rceil\) elements. Write these row and column indices as \(k_0+2u\) and \(j_0+2v\), with distinct \(u,v\) modulo \(p\). After invertible row and column diagonal factors, their Fourier submatrix is \((\omega^{-4uv})_{u,v}\). Since \(\omega^4\) has exact order \(p\), it is a prime-length complex Fourier submatrix. The classical prime nonvanishing-minors theorem, already used in the pinned Phase7 audit's Section 2, makes its rank the smaller of its side lengths. This proves (7). No finite-field full-spark assertion is imported.

Here \(D_N=p+2\), and the target local density is

\[
D_N/N=\tfrac12+\tfrac1p.
\]

Rank-one tiles obey Lemma 2. For every rank-at-least-two tile the following inequalities are strict:

- If \(a=2\), then \(r(a+b)/(ab)\ge1+2/b\ge1+1/p>1/2+1/p\).
- If \(a=3\), then \(r(a+b)/(ab)\ge2/3+2/b\ge2/3+1/p>1/2+1/p\).
- If \(a\ge4\), (7) gives \(r(a+b)/(ab)\ge1/2+a/(2b)\ge1/2+a/(4p)\ge1/2+1/p\). Equality in this chain could only occur with \(a=4\), \(b=2p\), \(r=2\). But a Fourier rectangle containing every column has full row rank \(a=4\), excluding that candidate. Thus this case is strict as well.

The case \(a=1\) cannot have rank at least two. Summing these inequalities proves the additional theorem, with precisely the same rank-one equality structure and attaining coset tiling. This is a complete all-primes argument, not a finite census. Its sole external mathematical ingredient is the characteristic-zero prime-minor theorem inherited from the source; the primary research exposition Garcia, Karaali and Katz, *An improved uncertainty principle for functions with symmetry*, [arXiv:1807.07648v4, Section 1.1, Theorem 1.1](https://arxiv.org/html/1807.07648v4), was also freshly read. Its unitary normalization does not affect minor nonvanishing, and replacing its chosen primitive root by any other only permutes rows.

## 4. Complete domain and examples

The function \(d+N/d\) decreases for positive \(d\le\sqrt N\). Thus \(d\) can be taken as the largest divisor at most \(\sqrt N\), and \(e=N/d\). Setting \(t=e/d\ge1\), the hypothesis becomes

\[
\frac{(d+e)^2}{de}=t+2+t^{-1}<8,
\]

equivalent to \(t<3+2\sqrt2\). This is an exact domain test, implementable using integers as \((d+e)^2<8N\). No numerical square-root decision is required. Equality cannot occur for positive integer \(d,e\), because it would force the rational ratio \(e/d\) to equal the irrational \(3+2\sqrt2\).

For \(N=p^{2k+1}\), the closest divisor pair is \(p^k,p^{k+1}\). The test is \((p+1)^2<8p\), which holds for \(p=2,3,5\). The new nonsquare composite cases begin at \(8,27,125\), respectively. More generally the theorem includes such lengths as \(6,10,12,14,15,18,20,21,22,24,33,35,39,45,50,51,75\), among infinitely many others.

Examples of exact objective values are \(N=6\): 30; \(N=10\): 70; \(N=22\): 286; \(N=27\): 324; \(N=35\): 420; and \(N=125\): 3750. These are endpoint-incidence objective values, not measured arithmetic runtimes.

## 5. Exact stopping boundary, not a full-parent closure

The remaining general nonsquare composite problem is not settled. The additional twice-prime theorem does settle \(N=26\), with optimum 390, using information beyond stable rank. At \(N=57=3\cdot19\), however, the nearest divisor pair is \(3,19\), so \(D_{57}=22\) and \(D_{57}^2=484>456=8N\). Neither completion theorem applies. Formula (1) gives

\[
114\sqrt{114}\le\min\mathcal C\le1254.
\]

The simple stable-rank relaxation cannot prove the upper endpoint is optimal: the integer tuple

\[
N=57,\quad a=10,\quad b=11,\quad r=2
\]

obeys \(ab=110\le Nr=114\) and \(2\le r\le\min(a,b)\), but

\[
Nr(a+b)=2394<2420=D_Nab.
\]

This is an exact counterexample only to the proposed local inequality from those relaxed premises. It is **not** an actual Fourier submatrix, **not** a valid competing tiling, and **not** evidence that the full conjectured optimum is false. A further proof for unbalanced lengths needs additional Fourier-specific rank information or a different global argument. We do not manufacture such information from the relaxation.

The bounded theorem's stopping condition is the complete proof and source-bound independent review of this explicitly stated domain. The owner remains TO RESEARCH at priority 42. No record is archived or closed, and no census/status/score/novelty change is authorized by this report.

## 6. Costs and inherited implementation qualifications

The objective is the source's declared sum \(r_t(a_t+b_t)\). The construction is explicit but its coefficients, root table, subgroup enumeration, storage, input reads, and output writes are not free. The theorem does not equate the objective with a complete cold executor invoice.

The earlier rank-one execution audit's qualification is preserved: a literal loop accumulating from zero performs \(N\) extra first-term additions; direct initialization realizes the stated ledger. Shared execution can instead give classical Cooley–Tukey, outside this independent-tile optimization. Neither fact is altered by the new optimum theorem.

All norm arguments are complex. Exact modular checks below are corroborative controls; no finite-field version of the singular-value proof is asserted. Arbitrary invertible endpoint changes, which can destroy Fourier structure, are not allowed. Row/column permutations or nonzero diagonal rescalings preserve rectangle ranks and permit transport of this purely rank-based objective by relabeling/scaling; the proof itself is given at the declared Fourier representative.

## 7. Fresh, independently written checks

`check_theorem.py` uses only the Python standard library and imports no uploaded or repository scientific program. It checks:

1. The strict integer density inequality for every feasible rank-at-least-two scalar shape, at every eligible \(2\le N\le160\). Only the smallest admissible rank \(\max(2,\lceil ab/N\rceil)\) needs testing because the cost increases with rank.
2. Exact coset partitions, rank-one four-entry divisibility, the rank-one objective, and the divisor-domain equivalence at \(2\le N\le128\).
3. Deterministically selected Fourier submatrices at new nonsquare lengths over independently constructed prime splitting fields, plus exact contiguous Vandermonde controls. Modular ranks are not substituted for complex norms. A nonzero reduced minor gives a valid characteristic-zero rank lower bound for the same cyclotomic minor; the controls are supplementary and are not the all-length proof.
4. The exact \(N=26\) and \(N=57\) relaxed-premise counterexamples, claimed prime-power families, and the twice-prime theorem's local rank-shape inequality with its excluded full-column equality candidate.

Results, counts, and hashes are recorded in RESULTS.json and MANIFEST.json. These checks do not replay the original checker or source executor, and do not claim an exhaustive new proof audit of the research table.

## Proposed next-gate wording after independent acceptance

The higher-rank disjoint-tile optimum is now proved on the complete balanced-divisor domain D_N²<8N and, separately, at every N=2p with p odd prime: its value is N D_N and all optimizers are rank-one full coset tiles. The first family includes every power of 2, 3 or 5; earlier square/prime scopes are preserved rather than recounted. General nonsquare composite lengths outside these two domains remain open. The new universal lower bound is N min(D_N,2sqrt(2N)); the N=57 shape (10,11,2) shows the stable-rank-only local argument is insufficient outside the proved domain, without supplying an actual Fourier counterexample. Continue only with additional Fourier-specific rank information or a legal competing tiling. Preserve disjoint/no-sharing, characteristic-zero prime-minor, complex-field, preparation/storage/I/O and literal-loop qualifications. Parent TO RESEARCH, priority 42 unchanged.
