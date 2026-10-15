# M-PERMUTATION-DISPLACEMENT: complete implication and closure boundary

Date: 2026-10-14 UTC. Read-only source comparison; fresh bounded controls only.

## Result first

The exact all-field cycle-rank identity is a literal instance of Zaslavsky's canonical gain-graph representation theorem. The complete minimum and unique-extremizer statement follows from that identity by the elementary zero-sum counting proof below, including the essential even-size repair.

This supports classification as a **proved, attributed elementary corollary**, with no standalone novelty claim. It does **not** prove that the full minimum/unique-negation sentence was previously printed. No source located in this bounded comparison states that exact optimization verbatim. If the parent's closure criterion requires a printed predecessor of the complete optimization, this record must remain open; do not relabel the whole result a verbatim rediscovery.

There is no remaining mathematical lemma in the original stated theorem, and the finite-field domain is not a source gap after the Zaslavsky mapping. Independent review of this new attribution mapping is still needed before a status write. No status, table, repository, or external document was changed.

## 1. Frozen original record and full scope

The current Catalogue stable ID is M-PERMUTATION-DISPLACEMENT, row 62 in the 14:10 snapshot; the Research overview row is 91. Its original accepted model is:

- N >= 1; a field K contains an element omega of exact order N.
- F[k,j] = omega^(kj), 0 <= k,j < N.
- One fixed cyclic output shift Z chosen so ZF=FD, with D[j,j]=omega^j. Opposite shift/root signs make the same zero-sum condition.
- An unweighted input permutation P, P e_j=e_pi(j).
- z(P) counts cycles C of pi for which sum(j in C) is 0 modulo N.
- The claim is rank(ZF-FP)=N-z(P), with minimum floor(N/2) over every P, attained uniquely by pi(j)=-j modulo N.

The latest Catalogue X:Z explicitly says the corrected scoped theorem has no missing proof lemma. Weighted monomial input matrices and unrestricted arithmetic runtime are outside this theorem's scope, not unfinished mathematical cases. Larger historical Hankel/transcript/cosine-sine suites are separate from this statement.

Original theorem text read as inert data:

coverage_audit_first89/source_bytes/17b6c569e8a4cad09b87dc56a1901f80326be926a0c3c3b9ca4217e32bcd25b1__RESEARCH.md

SHA256: 17b6c569e8a4cad09b87dc56a1901f80326be926a0c3c3b9ca4217e32bcd25b1.

The old source's even-N equality sentence by itself is incomplete. The latest accepted row supplies the total-index-sum repair, retained explicitly below.

## 2. Primary antecedent and exact field scope

Thomas Zaslavsky, *Biased graphs IV: Geometrical realizations*, Journal of Combinatorial Theory B 89(2) (2003), 231–297, DOI https://doi.org/10.1016/S0095-8956(03)00035-2.

Author-hosted prepublication version: https://people.math.binghamton.edu/zaslav/Tpapers/bg4.pdf . Title page identifies the version as August 18, 2002, trivially revised December 16, 2005. The author's publication index links it as the prepublication version; its printed page numbers below are preprint numbers, not journal pages.

Relevant primary statements: bias rank n-b(S) on printed p.3; canonical incidence vectors on p.8; Theorem 2.1(a) and its proof on p.9. The domain is a gain group embedded multiplicatively in a skew field. The incidence representation realizes the bias matroid, hence has rank n minus its balanced components. Loops and parallel edges are allowed. No characteristic-zero or cycle-length coprimality premise occurs.

Access: the full 62-page primary PDF text was available through web retrieval, and the relevant definitions/theorem/proof were inspected. No local PDF bytes or PDF digest is claimed.

For context only: Gaetz–Gao (2020), https://alco.centre-mersenne.org/item/10.5802/alco.114.pdf , Proposition 3.1 (attributing Shi 2007 Theorem 2.1) and Proposition 2.2 also recover the complex identity through reflection length. That route alone does not justify positive characteristic. It is superseded here by the all-skew-field gain-graph theorem.

## 3. Literal matrix mapping

Construct a directed gain multigraph with vertex set {0,...,N-1} and one edge a_j oriented from pi(j) to j, carrying gain omega^j. Its canonical incidence column is

    x(a_j) = -e_pi(j) + omega^j e_j = (D-P)e_j.

Thus its full incidence matrix is exactly D-P; neither a numerical approximation nor a similarity assumption is needed. If pi(j)=j, the column is (omega^j-1)e_j. In particular j=0 gives a balanced loop and zero column, which the source explicitly allows.

Each graph component is precisely a permutation cycle, with orientation reversed if necessary. Its gain product is omega^(sum of its vertex indices). Exact root order makes this equal to 1 exactly when that sum is zero modulo N. Therefore its number of balanced components is z(P). Applying the primary theorem gives rank(D-P)=N-z(P) over every admitted K.

The Fourier matrix is invertible: its columns form a Vandermonde matrix at N distinct roots. Consequently ZF-FP=F(D-P) has the same rank. If a root of exact order N exists in characteristic p>0, then p does not divide N. This does not require p to avoid the individual permutation-cycle lengths.

An entirely elementary check of the field issue is also available. On each cycle, the homogeneous equations propagate every coordinate from one chosen coordinate using only nonzero weights. Closing the cycle leaves the single scalar condition (product weights-1)t=0. The kernel dimension is exactly one in the balanced case and zero otherwise, even if the characteristic divides the cycle length. No eigenvalue multiplicity or diagonalizability argument is used.

## 4. Complete extremum and uniqueness corollary

Only the vertex 0 can form a zero-sum singleton. Every other zero-sum cycle uses at least two indices, so z(P) <= 1+floor((N-1)/2)=ceil(N/2). Negation attains this value: the zero singleton and all non-self-negative pairs are balanced; for even N the other self-negative index N/2 is a nonbalanced singleton. This proves the rank minimum.

For odd N=2k+1, equality z(P)=k+1 requires the zero singleton, since k+1 cycles of size at least two cannot fit. The remaining k balanced cycles consume all 2k remaining vertices, so all are pairs. Each zero-sum pair is {j,-j}. Thus the only permutation is negation.

For even N=2k, the total sum of indices is N(N-1)/2 = k modulo 2k, which is nonzero. Hence not all permutation cycles can be balanced. If an optimizer lacked the zero singleton, its k balanced cycles would consume all 2k vertices as pairs, contradicting this total sum. Thus {0} is a balanced singleton. The other k-1 balanced cycles use at least 2k-2 vertices. A nonbalanced cycle must still contain at least one vertex. There are only 2k-1 vertices after removing 0, so equality forces exactly k-1 balanced pairs and one remaining nonbalanced singleton. The balanced pairs are inverse pairs, leaving the unique nonzero self-inverse residue k as the singleton. Again the permutation is uniquely negation. N=1 is immediate.

This proves every parameter of the original rank/minimum/unique-extremizer statement without a further analytic, computational, or finite-field assumption. The proof in this section is the project's elementary specialization/corollary, not a quotation or a claim about what Zaslavsky printed.

## 5. Fresh exact finite-field controls

The independently authored standard-library checker check_field_mapping.py was executed with python -I -S. It imports no historical research program. It checks every permutation in these declared domains:

- N=3 over F4=F2[t]/(t^2+t+1): 6 permutations.
- N=7 over F8=F2[t]/(t^3+t+1): 5,040 permutations.
- N=4 over F9=F3[t]/(t^2+1): 24 permutations.

All 5,070 actual matrix ranks match the gain-graph/cycle formula. The asserted minimum and unique negation optimizer also match. Among these, 3,476 permutations have a cycle length divisible by the field characteristic. The checker verifies field inverses and exact root order before testing. These are supplementary controls of a general proof, not its quantifier and not a replay of the inherited 409,113-permutation suite.

## 6. Exact closure recommendation

A justified description is:

“Proved for every field admitting an exact-order-N root. The cycle-rank identity is a direct instance of Zaslavsky's canonical gain-graph representation theorem; the sharp unweighted-permutation minimum and unique negation optimizer are elementary corollaries, with the even-N total-sum argument explicit. No separate originality claim.”

A closure subtype such as CLOSED_PROVED_ATTRIBUTED_COROLLARY is mathematically defensible **if** the original record's attribution gate asks for a complete earlier-theorem implication rather than evidence that every final optimization sentence was previously printed. This packet supplies that implication and all field guards. It is not an authorized status patch and does not supersede the parent's interpretation of the user's completion condition.

If a full printed-predecessor match is required, the precise remaining question is only the historical placement of the sharp optimization/uniqueness corollary. The core identity should no longer be described as an unmatched possible new theorem. Do not reopen weighted monomials, execution, broad FFT, or numerical production as new conditions of this specific theorem.
