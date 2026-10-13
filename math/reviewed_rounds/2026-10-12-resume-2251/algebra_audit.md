# Standalone algebra/publication audit

12 October 2026. Read-only comparison against the live table snapshot retrieved 22:53:50 UTC and repository commit 95419a2bd5d0bf6d3b78747bf163a62a7b9e4b5d. This is an editorial research recommendation, not a change to catalogue rankings, a novelty probability, a new acceptance of inherited proofs, or a worldwide-priority finding.

## Decision

For a standalone mathematics paper, prioritize:

1. **F020: Rogers–Szegő local moving-root forms and ordinary discriminant coefficients.** Best coherent algebraic story and strongest concrete next proof frontier. The exact parameter-specific all-order formulas, rather than general root-of-unity/Hermite machinery, are the defensible comparison target.
2. **F018/C05: independently routed inverse-sum obstruction with sparse/rank corrections.** Best standalone structural lower-bound story. Its current logarithmic branch obstruction is substantially broader and cleaner than the historical C05 log-log statement.
3. **F014: fixed-pair Weyl–Green branch bound.** A compact, explicit theorem with composite-modulus content, but the grammar restrictions and classical rank mechanism reduce its reach.
4. **M-CHIRP-LOWER: forced-feedback two-Green exclusion.** A substantial exact-certificate application, with infinite positive/negative-sign families, but narrower and heavier than the preceding stories.
5. **C03: reciprocal diagonal-pencil resultant.** A focused formula/application note or supporting proposition. The latest general Hankel/Bezoutian bridge is already closed and explicitly classical; do not spend a new cycle rediscovering that bridge.
6. **Projective curvature/equivalence test.** Methods/supporting material. The cross-ratio invariant is explicitly classical and should not lead a novelty pitch.

This ordering compares the inspected algebra candidates. It does not rank the separate prefix, compiler, or raw-recognition programs, which have different purposes and evidence requirements.

## 1. F020: exact statement and why it leads

Let H_n(z;q)=sum_k [n choose k]_q z^k, n=Ad+b, d odd, q(epsilon)=omega(1+epsilon^2)^(1/d), and F(z)=1+z^d. For fixed A>=1, d and b, the accepted separated initial form at alpha^d=-1 is

H_n(alpha+epsilon x;q(epsilon))
=epsilon^A (-1)^A d^(A/2) H_b(alpha;omega) He_A(sqrt(d)x/alpha)+O(epsilon^(A+1)).

Under Disc(H_b) Res(F,H_b)!=0, the ordinary discriminant has order K=dA(A-1)/2 in q^d-1, with leading coefficient

(-1)^(A(d-1)/2) d^(dA(A+1)/2) (product_(j=1)^A j^j)^d Disc(H_b) Res(F,H_b)^(2A).

For odd b, write H_b=(z+1)U, g=U(-1), W=(omega;omega)_b/(omega^2;omega^2)_((d+b)/2), tau=dW/g. The overlap initial form uses

J_(A+1)=He_(A+1)+A(1-tau)He_(A-1)=x He_A-A tau He_(A-1).

The overlap discriminant order is K+A, with leading coefficient

(-1)^(A(d-1)/2) d^(dA(A+1)/2+A) (product_(j=1)^A j^j)^(d-1)
* Disc(J_(A+1)) Disc(U) Res(F,U)^(2A) g^2.

These are ordinary z-derivative discriminants. A q-difference discriminant product cannot replace them.

The current live table and restored reviewed text establish full overlap families for every odd b<=25, every odd d>b, every primitive root in characteristic zero, and every A>=1. General g!=0 and Res(F,U)!=0 are already accepted. The two remaining general guards are distinct:

- Overlap Disc J: general unresolved middle starts at odd b>=27, 2b+1<d<15(b+1)/2, except separately established instances.
- Ordinary residual Disc U: accepted for odd b<=25 at all odd d>b, and odd b>=3 at d>=4b^2. For b27 the remaining general small-order strip is odd d=29..2915, absent separately established instances.

The publication significance comes from a usable, fully normalized local theorem and a systematic guard-removal program. A procession of b-specific certificates alone has diminishing novelty value; a general criterion or general-in-b analytic improvement would make a stronger next conceptual result.

### Prior-work boundary

Static q-Lucas factorization, Hermite limits, mixed-derivative vanishing, root-of-unity coefficient expansions, and resultant/discriminant bookkeeping are established. The earlier theorem-level comparison specifically narrows the possible contribution to the complete RS-specific local initial forms, actual tau, and normalized ordinary leading coefficients.

Fresh primary inspection reconfirmed Schultz–Walker is a Gaussian-sum divisibility/vanishing source, and Sawa–Uchida develops classical quasi-orthogonal resultant/discriminant formulas. Neither fact certifies that the exact RS package is new. Numbering differs between the 2018 preprint and 2019 publication; do not transplant theorem numbers without identifying the version.

- Schultz–Walker primary preprint: https://arxiv.org/pdf/1202.0199
- Sawa–Uchida primary preprint: https://arxiv.org/pdf/1802.00605
- Published Sawa–Uchida: https://www.jstage.jst.go.jp/article/jmath/71/3/71_831/_pdf
- Lubinsky–Saff exact DOI: https://doi.org/10.1007/BF01890574

The exact remaining publication-history checks include the complete Zhedanov 1997 paper and LS citation chain with normalization maps. The inherited source audit's access gaps should not be reported as absence of precedent.

### Concrete progress in this audit

A fresh candidate for b27 overlap is now supplied separately in b27_overlap_candidate.md. It contains 77 rigorous outward interval certificates. Seventy-six middle orders have rho=|tau-1|^2>8/3. The exceptional order d57,k13 has certified 2.275864<=rho<=2.275865, hence rho>9/4. The full repeated-root inequality rho<=2+2/A excludes A>=8; exact original-parameter specializations modulo11 give unit discriminants for A3..7. A1/2 are excluded by nonreality. An alternative original-parameter p5 local certificate also passes.

These are fresh candidate calculations awaiting independent review at this report's writing. No new theorem acceptance is asserted here. If independently accepted, the lower d29..55 and tail d>=211 compose with these 77 middle orders to complete b27 overlap only. Ordinary b27 residual squarefreeness remains open.

## 2. F018/C05: precise current structural result

For a complex flat unitary U, r independently routed inverse branches satisfying the required marked support-lift half-separator bound q, a row-degree-s correction, rank-t correction, and optional diagonal delta in {0,1}, set c=s+1+delta. Exact representation requires

N <= c^2(qr+t)9^r + cq(3^r-1) + 2(c-1).

For ordinary weighted-permutation Green denominators q=2. Independent endpoint permutation supports and zero endpoint weights are allowed. For fixed q,s,t the bound gives r=Omega(log N).

This is the current publishable statement. Historical C05's Schur-positive log-log bound remains a valid earlier route, not an additional discovery or the strongest present claim. The proof combines inverse complementary-rank identities, iterated separator/rectangle selection, correction trimming, and the flat-unitary stable-rank lower bound.

A good paper would foreground the independently routed graph-support class and explicit correction contract. Classical nullity/separators/stable rank are not new primitives. The theorem does not address products/interleavings, unbounded-separator supports, or shared-evaluator arithmetic cost. Fixed-r approximation floors do not automatically imply logarithmic r at every fixed positive error tolerance.

Fresh primary inspection confirms inverse preservation of complementary off-diagonal ranks and same-graph rank algebra in GIRS. This is a genuine mechanism antecedent, not an identified predecessor of the complete independent-route/correction theorem: https://arxiv.org/html/1911.05858#S2.SS1

## 3. F014: exact grammar and rank boundary

At odd N, over a field containing an exact-order Nth root with N invertible, select one common generating ordered Weyl pair U=S^uT^v,V=S^rT^s. All branches have form c_l(I-alpha_l U)^(-1)(I-beta_l V)^(-1), without extra branch-dependent endpoints. Put

D=us-vr a unit, A=u^2+v^2, B=r^2+s^2, delta=(D-ur-vs)/2, m=(N+1)/2.

The accepted bound is

number of branches >= max{N/gcd(N,delta), min(m,N/gcd(N,A)), min(m,N/gcd(N,B))}.

It implies ceil(sqrt N) at every odd N and (N+1)/2 at odd prime powers. The separate canonical (S,T) theorem allows Weyl-monomial endpoints and requires N branches. These endpoint allowances are not interchangeable.

Fresh exact arithmetic in this audit reconfirms that the formula can be only 5 at N15 (directions (1,2),(1,3)) and 7 at N35, below the corresponding half-length bounds. These are bounds from the formula, not constructions with that many branches. Reverse order/depth3 examples already show full Weyl coefficient rank with O(N) application; rank is not an unrestricted operation-count lower bound.

Fresh primary inspection confirms the all-odd-modulus complex Weil/Fourier framework is already in Gurevich–Hadani–Howe, including Theorem2.4. The all-odd framework cannot itself be claimed as new: https://arxiv.org/html/0808.2447

The exact three-way gcd/Hankel maximum has unresolved printed priority. A model-matched predecessor or sharp upper construction is a worthwhile specialist check, but neither is a missing premise of the scoped accepted lower bound.

## 4. Forced feedback and C03

### Forced-feedback exclusion

The live M-CHIRP-LOWER record adds negative-sign N=4820k-5, k>=1, k not congruent to4 mod5, to the earlier positive N=5q^2 congruence family. It excludes sums of two diagonal-ended Hamiltonian Green terms for the forced B_N, including zero-edge and singular-mask boundaries. It leaves unmatched routes, other feedback, products, three-plus branches, generic effective cutoff, and growing full-B construction outside the claim.

The cubic identity (FA)^3=NG I and its rational feedback consequences are useful supporting identities. They do not construct forced B without Fourier work. This limits the standalone algorithmic story even when the algebra is exact.

### Reciprocal diagonal-pencil resultant

For D=diag(1,w,...,w^(m-1)), f=det(A-aDAD), g=det(B-awDBD), use fixed padded degree-(m,m) resultant R. The accepted factorization is

R=w^(v+b)(w-1)^(m^2)V(w+w^(-1)),
v=m(m-1)(4m+1)/6, b=m(m-1)(2m-1)/6, deg V<=b.

The latest bridge gives R=epsilon_m det Bez_m(f,g) universally over commutative rings. On a normalized chart it gives R=epsilon_m alpha^m det H, using the Laurent coefficients of h/u and Barnett congruence. The ring chart requires units, not merely nonzero determinants. The general bridge, endpoint-safe division-free formulas and O(m^3) supplied-node evaluator are already accepted; they are not fresh open discoveries.

Fresh primary inspection of García-Armas–Ghorpade–Ram Proposition3.4 verifies Barnett congruence for every Padé pair, including noncoprime cases: https://arxiv.org/html/1011.1760#S3. The exact full evaluated matrix family may still lack an identified earlier printed match; that is narrower than a new general Hankel/resultant mechanism. Per-node cubic evaluation is not all-coefficient recovery or a Fourier algorithm.

## 5. Projective criterion

An entrywise-nonzero matrix is diagonally/permutation equivalent to F_N exactly when its anchored cross-ratio grid is omega^(alpha_i beta_j) for residue permutations alpha,beta. Composite N requires a unit pivot gcd(t,N)=1, both label permutations, and full-grid verification. Pair histograms alone fail, with Sylvester-Hadamard counterfeits.

The ratio invariant and Fourier character mechanism are explicitly classical. Its certification protocol is useful supporting methodology. Finite-precision certified curvature-energy diagnostics remain separate from exact field statements; floating test code is not an outward-rounded certificate.

## 6. Recommended next proof/counterexample check

First complete independent review of the supplied b27 overlap candidate. The meaningful next guard, after that, is **ordinary b27 residual squarefreeness**, not another rerun of b<=25 or a restatement of the overlap result.

A bounded exact check is available: construct P_13 by

P_0=1, P_1=t+q+q^2,
P_j=(t+q^(2j-1)+q^(2j))P_(j-1)-(1-q^(2j-1))(1-q^(2j-2))P_(j-2).

Form C_13=P_13(2)Disc_t P_13 over Z[q], then F_13=C_13 mod2 and its actual-degree reciprocal gcd G_13=gcd(F_13,F_13^*). The accepted criterion proves all odd d>27 if every root of G_13 has order<=27. Use a full factor/root-order certificate or a complete divisibility certificate by products of q^j-1 for odd j<=27 with multiplicities handled. If an order>27 remains, isolate it and check characteristic-zero cyclotomic divisibility instead of declaring a repeated-root counterexample. The earlier stronger bound by m is already false at m12 (order17); do not reintroduce it.

This has high information gain: either it closes the other b27 guard with a finite exact certificate or identifies concrete exceptional orders/new obstruction. It is more useful than automatically extending the overlap list to b29. A general-in-b root-order theorem or counterexample would have greater conceptual significance than one more bounded family.

## Source and evidence map

Current live records: Catalogue rows4(F020),6(C03),18(projective),30(F018),32(F014),35(C05),36(feedback),54(cubic), plus their current overlays and Theorem register. Live table: https://docs.google.com/spreadsheets/d/1BHaGJHkXxf_UfZdyTKF2zrWNFzIP4IvhaqFMj-83BjU/edit

Restored current repository proof/review sources:

- math/reviewed_rounds/2026-10-12-b25-overlap/rs-b25-full-overlap.md
- math/reviewed_rounds/2026-10-12-b21-overlap/rs-b21-full-overlap.md
- math/reviewed_rounds/2026-10-12-reviewed-research/rs-general-odd.md
- math/reviewed_rounds/2026-10-12-reviewed-research/rs-ordinary-squarefree.md
- math/reviewed_rounds/2026-10-12-prime-sampler-attribution/rs-general-prime-b17-unramified.md
- math/reviewed_rounds/2026-10-12-network-algebra/c03-general-hankel-bridge.md
- math/reviewed_rounds/2026-10-12-reviewed-research/weyl-green-source-comparison.md

Each can be addressed under https://github.com/AgentSlop-Si/research/blob/95419a2bd5d0bf6d3b78747bf163a62a7b9e4b5d/ followed by the exact path. Local restored copies are under research_resume_2251/repo/.

Historical source bodies additionally inspected as historical evidence: rs_manuscript_v3_1704/package/RS_Local_Discriminants_Working_Note_v3.tex; rs_prior_work_1727/package/RS_Theorem_Level_Prior_Work_Audit.tex; coverage_audit_first89/source_bytes/826592d16ce4175f5797aa671ceeea7700aebff31c4c48e1fa3aab8967116b61__PROOF_CERTIFICATE.md; the matching SEALED_PROOF and PRIMARY_SOURCE_COMPARISON files; hankel_priority_1800/packet/REPORT.txt. Historical claims were reconciled to the current overlays rather than called latest.

New local artifacts: b27_overlap_candidate.md, b27_interval_certify.py, b27_interval_certificates.json, b27_d57_finite_A_certificate.json, b27_d57_prime_probe.py/json, exploratory scan files explicitly labeled noncertified, and weyl_formula_controls.json. Only freshly authored mathematical code was executed in this pass. No live spreadsheet, repository or source file was changed.

## Dated outcome addendum, 12 October 2026 23:06 UTC

The independent review has now ACCEPTED the full scoped b27 overlap result: every odd d>27, every primitive order-d root in characteristic zero, every integer A>=1. It independently reconstructs all77 interval certificates with1024-bit outward arithmetic and a different pi identity/Pascal derivative, checks9,548 saved guards, and separately proves the finite A3..7 cases at d57 using prime229 with q=3, g=209, W numerator40, W denominator151, tau=160. Independent cold replay reproduces the saved results byte-identically.

Controlling review: b27_independent_review.md; b27_independent_review_manifest.json; b27_independent_cold_replay.json. The original b27_overlap_candidate.md remains frozen candidate history. This is acceptance of the scoped mathematical extension, not historical novelty, a new canonical identity, a table update, or fullF020 closure.

The next bounded task is now specified in b27_ordinary_residual_next_gate.md. It supplies the exact P13/characteristic-two resultant gate, explains why all odd d>=2917 are already covered by the general4b^2 theorem, and gives explicit success/counterexample/blocker stopping conditions. No ordinary-residual calculation was silently imported from the overlap proof.
