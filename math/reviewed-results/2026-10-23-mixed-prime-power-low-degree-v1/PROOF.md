# Short-overlap prime-character erasure for repeated-prime Fourier masks

Date: 2026-10-23 UTC. Proof candidate, pending independent review. Owner M-SPARSE-DEFECT remains TO RESEARCH, priority 42. No historical novelty, full support classification, whole-owner closure, exact nonsharp optimum, improved gap rate, or Fourier/FFT complexity claim is made.

## 1. Prior-result gate and exact new scope

The prime-power degree theorem is **already accepted**, not a new target. Its original report and independent review are bound in `sources/PRIMEPOWER_REPORT.md` and `sources/PRIMEPOWER_REVIEW.md`. They prove necessity for arbitrary binary square fixed-Fourier masks at every order p^a. More importantly for the present reduction, the accepted proof explicitly covers square matrices of arbitrary size with repeated character labels and row weights p^(k_i/2). The independent review's Section 2 confirms this enlarged class and the terminal bound b <= K+a. This report reuses that accepted theorem; it does not claim new prime-power descent credit.

The accepted mixed-prime report and review, also copied as exact Git blobs, complete N=2q and the low-degree N=pq case but expressly leave p^a q outside those conclusions. The now accepted distinct-odd-semiprime theorem is preserved as inherited; it is not counted again.

**New reduction and theorem candidate.** Let p<q be distinct primes, a>=2, N=p^a q, and zeta any primitive complex Nth root. For an arbitrary binary N-by-N matrix R define

    D[r,c] = R[r,c] zeta^(rc).

Within the sector 0<=d<q, there exists a mask with either D*D=dI or DD*=dI exactly when

    d = 0, or d = p^j with 0<=j<=a and p^j<q.              (1.1)

The reduction also works at a=1, but that low-degree semiprime result is already accepted and receives no new credit. The proof does not impose row-independent supports, rectangular row-Gram substitutes, Cartesian supports, free phases, or a full-block support decomposition. Both original Grams and all column degrees are retained.

In the specifically selected prime-square slice N=p^2 q:

- If p<q<p^2, the degrees below q are exactly {0,1,p}.
- If q>p^2, the degrees below q are exactly {0,1,p,p^2}.
- Equality q=p^2 is impossible because q is prime and p>=2.

The boundary d=q has the already known divisor witness. Thus one may equivalently include that one boundary in these degree-existence lists by adjoining q. No assertion for any d>q is made here.

## 2. Original indices and both Grams

Set m=p^a. Put

    e_m = q (q^(-1) mod m),     e_q = m (m^(-1) mod q)

as residues modulo N. These are complementary CRT idempotents. Use the literal original indices

    r = x e_m + b e_q,     c = y e_m + v e_q,
    x,y in Z/m,           b,v in Z/q.

Let alpha=zeta^e_m and beta=zeta^e_q. Their orders are m and q, and exactly

    zeta^(rc) = alpha^(xy) beta^(bv).                     (2.1)

For d>0, either scalar Gram identity makes the original square matrix invertible and therefore implies the other. Each original row and column has precisely d supported entries. We will use the full column Gram in the reduction. The d=0 case is immediate and is separated from every invertibility argument.

## 3. The short-overlap prime-character erasure lemma

The following lemma is valid for any m coprime to q, not just a prime power. Its conclusion is a justified auxiliary transformation, not a change to the original existence problem.

**Lemma.** Suppose the original binary square matrix in (2.1) satisfies D*D=dI with 0<d<q. Erase the q-character while keeping the same support and the same number of rows and columns:

    E[(x,b),(y,v)] = R[(x,b),(y,v)] alpha^(xy).             (3.1)

Then

    E*E = EE* = dI.                                      (3.2)

In particular, E is square of size mq; its character order is m, and its row and column labels modulo m each repeat q times. No quotient, submatrix selection, or assumed dimension reduction occurs.

**Proof.** Let K=Q(alpha). Since gcd(m,q)=1, the cyclotomic degree formula gives

    [K(beta):K] = phi(mq)/phi(m) = q-1.

Indeed K(beta)=Q(zeta): alpha beta=zeta because e_m+e_q=1 modulo N. Therefore the minimal polynomial over K of beta^h, for any nonzero h modulo q, is

    Phi_q(X) = 1+X+...+X^(q-1).                           (3.3)

Take distinct columns c=(y,v) and c'=(y',v'). If v=v', their original column Gram already equals the corresponding column Gram of E, so it vanishes.

If v!=v', group the original zero column Gram by the row's q-label b. Define

    C_b = sum_(rows r=(x,b)) R[r,c] R[r,c'] alpha^(x(y'-y)) in K.

Then

    sum_(b=0)^(q-1) C_b (beta^(v'-v))^b = 0.             (3.4)

By (3.3), a polynomial over K of degree at most q-1 vanishing there must be a scalar multiple of Phi_q. Consequently

    C_0=C_1=...=C_(q-1).                                (3.5)

The overlap of the two column supports contains at most d<q rows, because each column has degree d. Hence some q-label b_0 is absent from this overlap, and C_(b_0)=0. Equation (3.5) forces every C_b=0. Their sum is precisely the corresponding column Gram of E, which therefore vanishes as well.

All column diagonals remain d because only unit-modulus factors were erased. Thus E*E=dI. E is still square and d>0, so EE*=dI follows by invertibility. Its support is unchanged, so both original regularity conditions also remain unchanged. This proves the lemma.

The omitted-label argument is the decisive hypothesis. It does not assert coefficient matching in unrestricted mixed-prime weighted systems. In particular, it does not contradict the accepted order-six weighted cancellation obstruction in the prior mixed-prime report, Section 8.

## 4. Application of the already accepted enlarged prime-power theorem

Take m=p^a in the lemma. E has the form

    E[i,j] = p^(0/2) T[i,j] alpha^(x_i y_j),

with a binary T, arbitrary repeated labels x_i,y_j modulo p^a, square size p^a q, and both Grams dI. It lies exactly in the accepted enlarged prime-power class, with every initial exponent k_i=0. The class does **not** require matrix size equal to character order or distinct labels.

The accepted weighted character-filtration descent terminates at singleton row supports and proves d=p^j, with 0<=j<=a because initial exponents are zero. Thus every possible d in 0<d<q satisfies (1.1). The only new mathematical step used to reach that accepted class is Section 3's short-overlap erasure.

This application is not an inference from tensor-product constructions or a spectral-submatrix theorem. It uses the independently accepted repeated-label square theorem at exactly its reviewed hypotheses. It also makes no claim that an arbitrary successful mask contains a d-by-d Hadamard submatrix.

## 5. Inherited sufficiency and original inverse-row consequence

For any divisor d of N, put h=N/d and use the already accepted literal-phase mask

    R[r,c]=1 iff floor(r/d)=c modulo h.

Each row and column has degree d. Different row blocks have disjoint supports. For two different rows in the same block, the row Gram is a scalar phase times a complete nontrivial dth-root sum and vanishes. Hence both Grams equal dI. These inherited witnesses supply every p^j listed in (1.1), as well as d=q at the boundary. The zero mask supplies d=0. No new construction credit is asserted.

The original inverse-row equality criterion and compactness/attainment argument are copied unchanged as `sources/INVERSE_ROW_ACCEPTANCE.md`. For the normalized complex Fourier target, invertible approximants, simultaneous sparsity of every inverse row, and spectral norm, the candidate theorem implies, for 0<d<q and s=N-d,

    Delta(N,s)=sqrt(d/N) iff d=p^j, 0<=j<=a.

All other integer d in that sector have a strict infimum gap, not merely nonattainment. The existing general quantitative no-mask bounds continue to apply without any new gap-rate credit. The known exact Delta(3,1), half-density, codimension-two/codimension-three and other accepted scopes remain unchanged. This report does not supply an exact larger optimum at excluded budgets.

## 6. Primary-literature comparison and attribution boundary

The erasure proof uses only standard cyclotomic field degrees and the minimal polynomial of a prime root. Lam and Leung's primary paper, *On vanishing sums of roots of unity*, Theorems 3.1 and 3.3 and Corollary 3.4, provides the related classical squarefree-coset and two-prime cycle decompositions. Its proof also uses linear disjointness of the prime cyclotomic fields. These algebraic ingredients are classical, not new discoveries. Relevant passages were read at https://arxiv.org/pdf/math/9511209, pp. 6-8.

Malikiosis and Kolountzakis, *Fuglede's conjecture on cyclic groups of order p^n q*, Theorem 1.2, proves that spectral subsets tile; their cardinalities therefore divide the group order. Their Definition of spectrality and Theorem 2.1 use a single fixed support set. The original matrix here instead permits arbitrary pair-dependent column intersections. The inspected theorem does not directly classify these masks, and no reduction to a spectral subset is claimed. Relevant primary passages were read at https://arxiv.org/pdf/1612.01328, pp. 2-6.

Bond, Glickfield and Herr's *On the existence of complex Hadamard submatrices of the Fourier matrices* concerns selected row-by-column submatrices, not arbitrary entrywise supports. The indexed primary excerpt inspected identifies that domain and its inherited divisor examples. Direct PDF retrieval returned HTTP 502, so this report does not claim a full-paper read. Primary URL: https://par.nsf.gov/servlets/purl/10088774; DOI: https://doi.org/10.1515/dema-2019-0001.

This bounded check found no direct full-mask theorem in those inspected passages. That is not a certification of historical novelty. The present candidate should be credited, at most, as a new-in-this-record reduction and a composition with the accepted prime-power theorem. Primary facts and all prior theorem scopes retain their credit. No claim of a newly discovered prime-power theorem, spectral cardinality theorem, or two-prime cancellation theorem is made.

## 7. Fresh exact controls and precise guard failures

`fresh_controls.py` is new standard-library code. It imports or executes no historical scientific code. It implements integer cyclotomic reduction independently, checks original-index CRT phases, both full original Grams, both full erased Grams, regularity and the separate zero fiber coefficients used in Section 3.

The completed normal run covers 25 positive cases, four valid boundary masks of degree d=q, and six regular negative near-masks. It checks 556,630 original Gram entries, another 556,630 erased Gram entries, 278,315 literal CRT congruences, and 1,449,326 separate fiber coefficients. An additional 8,216 short-support subsets are enumerated at selected small orders; every vanishing subset of cardinality below q passes the coefficient-erasure implication. Four of the positive controls shift the q-column label independently with the p^a-column coordinate, giving rows whose q-column labels vary and nonempty overlaps between columns with different q-labels. They check a genuinely nonempty vanishing fiber coefficient rather than testing only disjoint cross-q supports. These checks corroborate the proof, not an exhaustive census of all square masks.

The boundary controls are exact legal square masks: each degree-q divisor mask passes both original Grams, while its erased matrix fails both Grams. Thus the strict d<q guard is demonstrably necessary for this particular erasure mechanism. They are not counterexamples to the low-degree theorem or to general divisibility. The six negative masks retain equal row and column degrees but fail both original Grams, preventing regularity alone from being mistaken for existence.

The full outputs include exact nonzero failure residues, parameters, and counts. The normal and optimized Python runs have identical scientific outputs, with no assertion-dependent validation; both stderr files are empty. Source hashes and the package manifest bind the evidence. Independent mathematical review remains required before acceptance or publication.

## 8. Remaining task boundary

The selected prime-square low-degree slice is resolved by this candidate if independently accepted; the same argument works uniformly for all a>=2 below q. The full classification at N=p^a q, every degree above q, higher mixed orders, support geometry, exact nonsharp optima, improved gaps, broad sparse-column/fixed-frame commutator obligations, paid preparation/solve/decomposition/output/bit costs, stability and implementation remain outside this result. The current semiprime classification, prime-power theorem, N=2q theorem, connected (8,4) obstruction to full-block geometry and all earlier accepted results are unchanged.

No external state was changed. This is a local candidate packet, not self-acceptance, a table update, or a repository publication.
