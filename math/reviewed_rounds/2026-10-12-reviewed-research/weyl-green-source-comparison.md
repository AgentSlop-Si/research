Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: 755bdbfc6c65780890c526bd5ecc47b092792ba35f5eb388b734486afd0e43be

---

Weyl–Green and Fourier–Green: bounded priority gate
11 October 2026 UTC

DECISION

Retain the accepted restricted-representation theorems. No exact earlier publication of the complete fixed-pair gcd/Hankel branch inequality was identified in the sources inspected here. Worldwide priority therefore remains unresolved. Its defensible description is a specialized algebraic application of established Fourier/Weil, character-rank and Prony/Hankel tools, with explicit composite-modulus arithmetic and grammar guards. It is not a new general rank, uncertainty, semiseparable or FFT lower-bound theory.

Two concrete changes are warranted. First, credit the all-odd-modulus complex Weil framework correctly: Gurevich–Hadani–Howe already works over Z/nZ for arbitrary odd n. Second, reconcile C05's novelty row with its accepted later separator extension. The novelty row currently describes only the historical log-log bound, whereas Catalogue 35 already records the correction-compatible logarithmic branch bound with independent endpoint routes. This is a stale view, not a new result.

The pass closes a bounded source/model attribution gate and prepares existing-row addenda. It does not clear worldwide priority, declare publication acceptance, redo finite proof checkers, enlarge a grammar, change the ranking, or add a discovery. No Sheet or GitHub writes occurred. All mathematical source programs remained inert.

1. EXACT LIVE IDENTITIES AND EVIDENCE DEPTH


- NEW-02, an existing refinement view of F014: New results 5; novelty 55; overview 79.
- C05: Catalogue 35; novelty 27. Its current correction-compatible statement is a specialization/refinement of the accepted F018/TH-04 route, not another newly counted theorem.
- Source comparisons 8 is specifically PRIMARY-FOURIER | F014. Its source hash belongs to Delvaux–Van Barel 2008. Do not silently turn that row into a multisource record while leaving a single-source hash.

Fresh inert-text inspection covered the complete original F014 proof certificate and accepted audit; the complete accepted composite proof P06; and the original C05 THEOREMS.md and accepted audit. P06's bytes hash to 6fbe518c9837cfd73a198f9dfc77ecd9a0ffecdcf2a99ab7a0428ebd1c65f091, exactly the reviewed_artifact_sha256 in R17. The original F014 proof hashes to 826592d16ce4175f5797aa671ceeea7700aebff31c4c48e1fa3aab8967116b61. The C05 original theorem body was read directly from its exact master-archive member and hashes to c3dde844ca9984ec9b609677d538d8d6528151257d2a843b9d2a3f79c371d757.

Original audit bytes were freshly matched: F014 f600c061b00911e10d500ee29c375e7052553ae4d91c9fbfafb7be85e7b7c5b2 and C05 f155488c0657b63b2192a6a1ecd7e2264ce4c0e1051b9e084b4dee22bbbf2a07. Their separately declared repository exports have different hashes. These identities are not interchangeable; no corruption or new audit acceptance is inferred from the difference.

The final DV2008 comparison and the detailed 10 October separator comparison were reused, not presented as fresh literature discoveries. The latter's old missing-author-body sentence is superseded by Catalogue 35's dated recovery addendum. The current bridge's recovered author hash is 79a5f64c11c47e39eb1fe90f7f6d51743dc9e4f1a9d89a5c505ce17835a86c0f; its acceptance and recovery status are inherited in this pass. There is no justification to reopen that resolved absence claim.

2. PUBLICATION-SAFE MODEL STATEMENTS

2A. Canonical F014 grammar, with Weyl endpoints

Let N >= 3 be odd, K contain an exact-order Nth root omega, and char(K) not divide N. Put S e_j=e_(j+1), T e_j=omega^j e_j, TS=omega ST, and F[i,j]=omega^(ij). A branch is a scalar multiple of a left Weyl monomial, (I-alpha S)^(-1)(I-beta T)^(-1), and a right Weyl monomial, with alpha^N != 1 and beta^N != 1. The displayed multiplication order is mandatory. Parameters and monomial endpoints may vary between branches. An exact sum of b such branches equal to F requires b >= N.

Reason: the coefficient array in the ordered S^a T^b basis is an outer product for one legal branch, including its endpoint shifts and characters. Fourier's coefficient array is a nonzero Gauss factor times row and column chirps times [omega^(ab/2)], hence has rank N. Rank subadditivity is the entire lower-bound principle.

2B. General fixed-pair grammar, without additional endpoints

Choose one ordered pair U=S^uT^v, V=S^rT^s with D=us-vr a unit modulo N. Every branch is c_l(I-alpha_l U)^(-1)(I-beta_l V)^(-1), using this same pair, with alpha_l^N != 1 and beta_l^N != 1. Parameters may lie in one common extension field. Zero parameters are allowed, using 0^0=1 in the finite geometric expansion. There are no additional branch-dependent Weyl endpoints.

Set A=u^2+v^2, B=r^2+s^2, h=ur+vs, delta=(D-h)/2 modulo N, and m=(N+1)/2. The accepted lower bound is

 b >= max{N/gcd(N,delta), min(m,N/gcd(N,A)), min(m,N/gcd(N,B))}.

It implies b >= ceil(sqrt(N)) for every odd N and b >= (N+1)/2 for every odd prime power. If delta is a unit, b >= N; if delta=0, the half-length bound holds even at mixed composite N. The formula does not imply a universal half-length bound for every mixed composite; its minimum can be 5 at N=15.

The actual ordered word phase gives Fourier coefficients

 C'[i,j]=Gamma omega^(-A i^2/4+uv i/2-B j^2/4+rs j/2+delta ij).

After separate row/column scalings, their rank is the order of omega^delta. The nonwrapping m by m Hankel lift of the j=0 slice has rank min(m,ord(omega^(-A/2))); the other slice gives B. One branch contributes at most one to each of these three ranks. Finally AB=h^2+D^2 implies gcd(gcd(N,delta),gcd(N,A))=1 because every prime divisor of N is odd and D is a unit. This elementary arithmetic joins the classical rank bounds.

Keep 2A and 2B separate. A cyclically shifted geometric sequence may have Hankel rank two, so allowing Weyl endpoints in 2A does not allow them in 2B. Changing the pair independently by branch, mixed orders, arbitrary diagonal gauges and deeper paths remain excluded. Reverse-order and three-stage Green paths can already have full Weyl coefficient rank while applying in O(N) field operations. Thus no unrestricted arithmetic or runtime lower bound follows.

2C. Historical C05 and its current accepted scope

Historical C05 is over C. A denominator is I-W with W a weighted permutation, arbitrary cycle decomposition and zero edge weights permitted, each cycle-product different from 1. Branches may have scalar weights and singular diagonal left/right masks. There is one additive layer, plus a rank-t correction, a correction with at most s entries in each row, and a free diagonal. Unmatched row/column routes are absent in that historical proof.

For r >= 1, t,s >= 0, put m=r+t+1, L=m(s+2), B=(L-1)^(2^(r-1))+1. Equality to Fourier is impossible when

 N > 2(m-1)(B-m)(B-1).

The proof assembles rank-one inverse crosscuts, iterated monotone subsequence extraction, deletion of sparse-correction columns, and a small-arc Schur-positive Fourier determinant. The r=2,t=s=0 threshold is N>2300. The prime-factor and N=4096 controls have separate cyclotomic proofs. The Schur positivity argument is not a finite-field theorem.

Current Catalogue 35 already accepts the more general separator consequence. For a complex flat unitary U, r independently routed inverse branches whose required marked support-lift restrictions admit half-balanced separators of size at most q, row-degree-s and rank-t corrections, and an optional diagonal delta in {0,1}, put d=s+1+delta. An exact representation requires

 N <= d^2(qr+t)9^r+dq(3^r-1)+2(d-1).

For ordinary weighted-permutation Green denominators q=2. Independent endpoint permutation supports and zero endpoint weights are permitted. Fixed q,s,t imply r=Omega(log N). This statement and the older log-log theorem must not be conflated or counted twice. The newer bound does not remove the additive-layer/support-lift restrictions or prove a product-network or shared-evaluator runtime lower bound.

3. PRIMARY COMPARISON CERTIFICATE

A. All-odd Weil/Gauss framework: established antecedent.
Gurevich, Hadani and Howe, arXiv:0808.2447v3, §§1.1-1.3, pp.2-3; Theorem 2.4, p.5. The complex Heisenberg and Weil setup is explicitly for arbitrary odd n, and the DFT/Weyl-element identification also has all-odd scope. Only §1.4's explicit character formula is prime-specific. This paper is not an inspected statement of the permitted-resolvent branch inequality. The all-odd ambient framework cannot be claimed as the project's new extension.
https://arxiv.org/pdf/0808.2447v3

B. Exponential sums and Hankel rank: exact classical component.
Plonka and Tasche, Prony Methods for Recovery of Structured Functions, §2, equations (7)-(8) and following factorization, author-PDF pp.3-4; §3, pp.7-8. The Hankel factorization through Vandermonde matrices gives the standard term-count/rank mechanism. Substituting each branch's geometric slice gives the project's rank-at-most-b inequality. The quadratic-chirp rank is then a direct Vandermonde specialization. These are elementary applications of that established mechanism, not a new Prony theorem. The paper does not state the full fixed-pair composite gcd maximum.
https://num.math.uni-goettingen.de/~gplonka/pdfs/gamm-preprint.pdf
https://doi.org/10.1002/gamm.201410011

C. Green crosscuts: classical inverse-block rank, exact specialization.
Chandrasekaran, Epperly and Govindarajan, Graph-Induced Rank Structures, Proposition 2.1, p.5, and Proposition 2.3, pp.7-8. For a cycle-concatenated order, each off-diagonal cut block of I-W has at most one crossing directed edge. Proposition 2.1 preserves that cut rank under inversion; restriction and diagonal masks cannot increase it. This directly recovers C05's rank-one crosscut ingredient. Proposition 2.3 concerns compatible graph partitions and does not itself select a common rectangle across unrelated branch orders.
https://arxiv.org/pdf/1911.05858v3

D. Simultaneous order extraction: classical theorem, iterated application.
Erdos and Szekeres, A combinatorial problem in geometry, Compositio Mathematica 2 (1935), pp.467-468, give the increasing/decreasing subsequence theorem and the sharp product obstruction. Repeatedly applying it supplies C05's exponent 2^(r-1). This is an application with r orders, not a new subsequence principle. The scanned text was read; screenshot retrieval was unavailable, and a local PDF fetch returned 403. No successful local or visual PDF inspection is claimed.
https://www.numdam.org/article/CM_1935__2__463_0.pdf

E. Prime uncertainty/full minors: known theorem, not project novelty.
Tao, An uncertainty principle for cyclic groups of prime order, arXiv:math/0308286v6, Theorem 1.1 p.2 and Lemma 1.3 p.3. The all-square-minor nonsingularity used in the prime-only variant is explicitly attributed there to Chebotarev. It is a complex prime-order result. It does not by itself give C05's all-composite small-arc threshold or a permitted-resolvent term count.
https://arxiv.org/pdf/math/0308286

F. Final Fourier hierarchy comparison: reuse completed work.
Delvaux and Van Barel, Rank-deficient submatrices of Fourier matrices, LAA 429 (2008), 1587-1605. The preserved completed comparison covers the final numbered results, including generalized Vandermonde structure, prime full spark, digit-reversal rank-one hierarchy and prime-power one-vector support extrema. Its F014 section already says the exact ordered two-resolvent gcd/Hankel theorem is not stated there. Its result cannot be converted into worldwide priority clearance. This pass reused that comparison rather than rereading the complete external PDF.
https://doi.org/10.1016/j.laa.2008.04.043

G. Current C05 separator extension: reuse its specific comparison.
The saved separator audit already compares the full independent-routing/correction contract with nullity, GIRS, final TQS, weighted treewidth separators and frame/gain-graph sources. It classifies the complete cutoff as a specialized synthesis with unresolved priority. Its exact classical nullity source is Vandebril–Van Barel, Theorem 1/Corollary 1, pp.4-5; its TQS comparison uses Theorem 4.4 and Propositions 4.6-4.8, pp.1575-1576. No new generic claim about these frameworks is warranted here.
https://www.cs.kuleuven.be/publicaties/rapporten/tw/TW397.pdf
https://repository.tudelft.nl/file/File_6b7549c8-222e-4316-8ac4-a113d7d4da1e

H. Displacement rank: background classification only.
Kailath, Kung and Morf's 1979 paper establishes the displacement-rank literature. The publisher record and abstract were available; its full theorem body was not inspected here, so no exact theorem-level nonmatch is asserted for that paper. A displacement rank such as rank(LA-AR), an off-diagonal cut rank, a Hankel lift of a coefficient slice, and the Weyl coefficient-array rank are different defined objects. Their lower bounds cannot be transferred without a model-preserving argument.
https://doi.org/10.1016/0022-247X(79)90124-0

4. WHAT IS AND IS NOT A NEW PROFILE THEOREM

F014 studies three ranks after choosing an ordered Weyl coordinate basis. C05 constructs one common physical row/column rectangle across several independently ordered inverse terms. Neither statement is the catalogue's separate all-permutation Fourier cut-rank minimax, nor an assertion that all balanced Fourier minors have some stronger rank. Ordinary matrix rank of Fourier, Weyl coefficient rank, separation/cut profiles, displacement rank and scalar-support uncertainty must remain distinct in titles and abstracts.

The classical matches are source-backed: inverse complementary ranks, the one-cycle rank-one consequence, geometric-sum Hankel rank, monotone subsequence selection and prime full minors. The precise assembled branch contracts were not located verbatim in this bounded comparison. A short new derivation from classical components is not evidence that its complete formulation is new, difficult, sharp or publishable. Conversely, common classical ingredients alone do not establish that an exact earlier publication already contains the full quantified contract.

5. REMAINING GATE AND STOPPING CONDITION

F014 / NEW-02: before an originality or main-paper claim, complete a model-matched specialist/citation comparison for sums of two ordered resolvents of one finite-quantum-torus generating pair, preserving the no-extra-endpoint rule. The exact target is the three-way gcd/Hankel maximum and its all-odd/prime-power consequences. A source that proves only Weil theory, scalar uncertainty, finite exponential recovery, displacement rank, or a different product order does not close this gate. Record either an exact predecessor plus a substitution map, or a qualified bounded nonmatch. The current pass reaches the latter outcome, not priority clearance.

C05: preserve it as a historical specialized synthesis and make the already accepted independent-routing/correction update visible. Carry its priority question inside the existing F018 comparison rather than launching a duplicate family. Keep the small-arc all-composite Fourier-minor statement separately identified if the author wishes to claim novelty for that particular lemma. Its exact cutoff has not been certified as an independently new or optimal theorem here.

Publication-ready mathematical exposition can use §2 now, with the source distinctions in §3. Publication originality, editorial significance and external expert review remain open. Matching constructions/sharpness or wider grammars are optional new research directions, not missing premises of the accepted lower bounds.

6. PROPOSED REGISTER TREATMENT

EXISTING_ROW_PROPOSALS.json contains old-value-bound addenda for the current scope, evidence depth, comparison and remaining gates. It preserves assessment bands and priority ranks. The writer should re-read each target, confirm the exact row ID, and reconcile any subsequent updates before applying. Historical text is retained below dated addenda; no source-specific comparison row is repurposed.

The proposals update F014, NEW-02 and Q15 across their existing views. C05's novelty scope/model/limitations gain the later accepted bridge and its inherited evidence boundary. No edit is proposed to ALG-047: sharing a family label is not proof that its distinct two-line product theorem received this audit.

SOURCE AND EXECUTION LIMITS

Only source retrieval, inert text reading, archive-member extraction, hashes and report assembly were performed. There was no supplied-code execution, import, compilation, AST parsing, mathematical certificate replay or new experiment. Earlier acceptance and finite-check counts remain attributed to their earlier reviewers. Search was bounded to the exact ingredient/model questions; negative search results carry no novelty proof. Full external papers are not bundled. SOURCE_BINDINGS.json records exact local project bytes, PRIMARY_COMPARISONS.json records primary locators and access depth, and the manifest seals the deliverable.
