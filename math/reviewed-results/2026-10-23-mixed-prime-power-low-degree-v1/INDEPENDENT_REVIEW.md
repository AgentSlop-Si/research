# Independent review: short-overlap prime-character erasure

23 October 2026. **SCOPED PASS; no mathematical repair required.**

## Exact scope and binding

Candidate frozen directory: `prime_square_mixed_low_degree_20261023_frozen_v1`.

- REPORT SHA-256: `a8f46f43cfbe26245421e4e2635c2428eb6b60569207aa1a5f5a0c22a1b63333`.
- MANIFEST SHA-256: `005e68b02ad622a100639f92bb85c6f3d020bc06bf4e9a206cf606c77cda1082`.

For distinct primes p<q, a>=2, N=p^a q and 0<=d<q, a binary square mask R with D[r,c]=R[r,c] zeta^(rc) and either scalar Gram equal to dI exists exactly for d=0 or d=p^j with 0<=j<=a and p^j<q. Necessity applies to every arbitrary mask satisfying the Gram condition; sufficiency is existential, not a claim that every regular mask at an allowed degree works. The boundary degree q is supplied separately by an inherited divisor witness. No degree above q is classified.

At a=2 the below-q sets are {0,1,p} when q<p² and {0,1,p,p²} when q>p². The a=1 result and all prime-power necessity retain their earlier credit. The incremental content is the erasure reduction and its composition at a>=2, not a new prime-power descent theorem. M-SPARSE-DEFECT remains TO RESEARCH, priority 42.

All 17 candidate manifest members and five copied source bodies were checked by SHA-256. The four supplied Git blob identifiers were independently recomputed from the copied bytes. The full repeated-label source proof and review, the mixed-prime scope statement, and the exact inverse-row equality/compactness interface were read; no source program was executed.

## Independent proof check

**Original CRT phases.** Put m=p^a. The idempotents e_m=q(q inverse modulo m) and e_q=m(m inverse modulo q) satisfy e_m+e_q=1, e_m e_q=0, e_m²=e_m and e_q²=e_q modulo N. Thus the original indices r=x e_m+b e_q and c=y e_m+v e_q give zeta^(rc)=alpha^(xy) beta^(bv), with alpha=zeta^e_m and beta=zeta^e_q of exact orders m and q. This changes coordinates, not phases or supports.

**The erased auxiliary matrix.** For d>0, the original matrix is square and one scalar Gram implies invertibility and the other scalar Gram. In particular every column support has exactly d entries. For columns (y,v),(y',v') with v unequal to v', their zero Gram groups as sum_b C_b (beta^(v'-v))^b=0, where C_b is the alpha-weighted intersection in row fiber b. Each C_b lies in K=Q(alpha).

Because gcd(m,q)=1 and alpha beta=zeta, K(beta)=Q(zeta), so its degree over K is phi(mq)/phi(m)=q-1. Therefore beta^(v'-v) has minimal polynomial 1+X+...+X^(q-1) over K. A relation of degree at most q-1 forces all C_b equal, including if the whole polynomial is zero. The overlap has at most d<q rows, so it misses at least one row fiber. Its corresponding C_b is zero, forcing all of them zero. Their sum is exactly the Gram entry after erasing the beta character. For v=v' no beta factor was present in that entry. Diagonals stay d. Consequently the same N-by-N matrix E with entries R alpha^(xy) has E*E=dI and, by square invertibility, EE*=dI. No dimension quotient or support selection has occurred. The d=0 case is separately the zero mask.

This proves the lemma for any m coprime to q. Its strict overlap-size hypothesis is essential to this mechanism: at d=q a nonzero common fiber coefficient is possible. The lemma is not a general coefficient-matching assertion for arbitrary mixed-prime weighted sums.

**Critical repeated-label interface.** Accepted `PRIMEPOWER_REPORT.md` Sections 3–6 and `PRIMEPOWER_REVIEW.md` Section 2 expressly cover every nonempty square size, repeated row and column labels modulo p^a, binary support, row amplitudes p^(k_i/2) with integral k_i>=0, and both Grams dI. The matrix size is not required to equal p^a. The source review explicitly concludes d=p^b with b<=K+a, where K=max k_i.

E has size p^a q, each label repeats q times, every amplitude is 1, and both Grams hold. Thus K=0 and the exact accepted theorem gives d=p^j, 0<=j<=a. No ordinary p^a-by-p^a theorem is substituted for that stronger statement. In the underlying descent, same-label row supports are disjoint by positivity; anchor-pair matching then supplies equal-weight sibling rows, the unitary p-point row transform creates pure residue supports, both Grams force square child blocks, and terminal positive square matrices have singleton supports. These points explain why repeated labels and unrelated dimensions are genuinely permitted. This review checks that interface, not recredits or reexecutes the accepted descent.

**Sufficiency and original norm consequence.** For any divisor d of N the inherited mask floor(r/d)=c modulo N/d has regular degree d. Separate row blocks are disjoint; distinct rows within one block give a complete nontrivial dth-root sum. It has both Grams dI. This realizes all allowed p-powers and the separate degree-q boundary. For 0<d<q<N, s=N-d lies in the accepted original range 1<=s<=N-1. The source equality criterion and its compactness argument therefore yield Delta(N,s)=sqrt(d/N) exactly at the permitted p-powers, and a strict infimum gap at other d in this sector. This is not merely a nonattainment result, but it does not calculate a new gap rate or an excluded optimum. All earlier exact and quantitative conclusions remain intact.

## Fresh independent controls

`fresh_checks.py` was written for this review and uses only standard-library integer polynomial arithmetic. Cyclotomic polynomials are formed by exact division; root sums are reduced by long division. No candidate or historical code is imported, copied into the checker, or run.

The normal and Python -O outputs agree byte-for-byte. There are 1,499,570 active checks, including:

- 20 legal positive square controls at (p,a,q)=(2,2,3),(2,2,5),(2,3,5),(3,2,5),(3,2,7),(5,2,7), including every below-q p-power at these parameters.
- Six of those use a fresh construction R[(x,b),(y,v)]=T[x,y] times the indicator v=b+y modulo q, where T is a divisor mask at character order p^a. These have genuinely repeated labels and 988 nonempty cross-q column intersections in total, rather than only disjoint-column tests. On each fixed b block the restored beta factor is a column phase, so legality is independently understood.
- Both full original Grams and both full erased Grams, with 515,408 entries evaluated overall; 679,856 separate fiber coefficients checked zero; original-index CRT phase congruences and both regularities checked.
- Five exact degree-q boundary masks pass the original Grams but fail erasure. Two degree-regular cyclic near-masks fail the original Gram, rejecting the false regularity-only implication.
- 6,275 short subsets at orders 12 and 20 enumerated independently; all 63 vanishing cases satisfy the required separate-fiber erasure. These are bounded controls, not a census proving the theorem.

Finite controls corroborate the all-parameter argument and the strict boundary. They do not establish new cases beyond the proof's domain or independently rerun the inherited weighted descent.

## Attribution and retained limits

The primary [Lam–Leung paper](https://arxiv.org/pdf/math/9511209), Theorems 3.1 and 3.3 and Corollary 3.4, was independently opened at the relevant passages. It supports the classical cyclotomic cancellation/decomposition context, including the prime-field coefficient-matching mechanism; those ingredients are not credited as new. The primary [Malikiosis–Kolountzakis paper](https://arxiv.org/pdf/1612.01328), Theorems 1.2 and 2.1 and the spectral-set definition, was also read: its spectral condition uses one fixed subset and does not itself supply the missing arbitrary entrywise-mask reduction. The candidate correctly preserves the limited indexed-excerpt retrieval qualification for Bond–Glickfield–Herr; this review does not claim a fresh full-PDF inspection of that source. No historical novelty or blanket nonimplication is certified.

Accepted: the exact below-q degree-existence classification and inherited original inverse-row floor/strict-gap consequences. Not accepted or claimed: full p^a q classification above q, support-block geometry, new quantitative gaps, exact larger optima, computational complexity, physical implementation advantage, historical priority, or owner closure. No external state was changed.
