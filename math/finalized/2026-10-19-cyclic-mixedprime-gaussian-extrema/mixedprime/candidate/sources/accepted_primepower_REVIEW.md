# Independent review: prime-power Fourier equality-mask classification

Date: 2026-10-19 (UTC). Owner M-SPARSE-DEFECT, priority 42.

## Verdict and exact acceptance scope

**ACCEPT the uniform prime-power classification.** The frozen candidate proves that, for every prime p and every a >= 1, a binary Fourier mask of order N = p^a satisfying D*D = d I_N exists exactly when d = p^b for some 0 <= b <= a. Here D[r,c] = R[r,c] zeta^(rc), zeta is primitive of order N, and 1 <= d <= N. The necessity proof is valid in the original fixed-phase model. Divisor sufficiency is inherited from the accepted equality-criterion construction.

In the original inverse-row problem, for 1 <= d < p^a, this accepts

    Delta_(p^a,p^a-d) = sqrt(d/p^a)  iff  d = p^b, 0 <= b < a.

For every other integer d in that proper range, the inherited compactness/equality criterion gives a strict inequality above the floor. This is an all-prime, all-exponent result, not a finite census conclusion.

**Do not close M-SPARSE-DEFECT or the full uniform divisibility problem.** Mixed-prime necessity, remaining exact nonsharp optima, sharper/optimal quantitative gap rates, and complexity questions remain unresolved. Preserve status TO RESEARCH and priority 42. Existing exact optima and quantitative bounds remain accepted; the scope correction below is mandatory when summarizing the frozen candidate. This review makes no historical-priority or worldwide-novelty claim and changes no external state.

## 1. Frozen object and source binding

The reviewed candidate is `sparse_primepower_classification_20261019_0841`.

- REPORT.md SHA-256: `12807671c7f8a12c1b6315ae18321e95c3564a796ff86799c1e5f9b5f8bb53e2`
- MANIFEST.json SHA-256: `5f615de544e85ab0d64da17c9fbc101cdb48022c4a25be9696622e033af797c8`
- SEAL.sha256 file SHA-256: `534e252d70ca415c879367ff58534029230e309225911f61c7f7059518f859b0`

All 12 candidate manifest entries were checked for byte size and SHA-256. The seal's stated manifest hash matches. An unchanged copy is retained in `candidate_frozen/`; `CANDIDATE_BINDING.json` records the binding. All four candidate source copies were also compared byte-for-byte with their original local files. In particular, the connected N=8,d=4 baseline is the accepted packet `sparse_uniform_divisibility_20261018_2054`, not an altered control.

The author's newly written checker was statically inspected, copied to `candidate_replay/`, and executed there. Its three generated outputs are byte-identical to the frozen candidate outputs. No historical checker, solver, or historical research program was run. The separately authored `independent_checks.py` imports only Python standard-library modules and does not import the candidate checker or any historical program.

### Required scope correction to the candidate's unresolved-work inventory

The final sentence of candidate Section 8 says that all nonsharp exact optimum values and quantitative strict gaps remain open. Read literally, that is overbroad and is **not accepted**. It does not affect the new descent proof, but it must not erase earlier accepted results. In particular, the owner already retains Delta_(3,1)=sqrt(3)/2, the codimension-two and codimension-three sharpness classifications, and the general no-mask bound

    Delta_(N,N-d)^2 >= d/N + 1/[10 N d^(phi(N)-1)].

The polynomial refinements 1/(5N^3) at odd codimension two and 1/(30N^3) at codimension three with 3 not dividing N also remain accepted. These statements were checked against the earlier reports and their independent acceptance reviews, copied as read-only text under `scope_sources/` and bound in `SCOPE_SOURCE_BINDINGS.json`. No earlier program was run or earlier result re-audited.

Consequently the newly excluded prime-power cases inherit the existing quantitative bound: for N=p^a and d not a p-power in 1<=d<N,

    Delta_(p^a,p^a-d)^2 >= d/p^a + 1/[10 p^a d^(p^(a-1)(p-1)-1)].

This is the direct combination of the accepted general bound with the new no-mask classification. It is not a newly proved gap formula or optimal rate. The correct remaining-work wording is “mixed-prime necessity, remaining exact nonsharp optima, and sharper/optimal quantitative gap rates remain open.” The candidate is retained byte-for-byte, with this explicit review qualification.

## 2. The correct induction statement

The proof needs, and actually uses, the following larger class. Fix p and character level a >= 0. Allow any nonempty square size m, arbitrary repeated row and column labels x_i,y_j modulo p^a, nonnegative integral exponents k_i, and binary supports T. Define

    A[i,j] = p^(k_i/2) T[i,j] zeta_a^(x_i y_j).

Assume A*A = AA* = d I_m with d > 0. The common d stays unchanged under descent. The matrix size need not equal the character order, and the exponents need not be uniform.

This is genuinely closed under the proposed construction. Restricting to unrepeated labels, unweighted rows, or size equal to the character order would not be justified. The candidate expressly avoids those restrictions. At the initial binary mask all labels are the original indices and all exponents are zero. Square invertibility supplies the second Gram from the first.

For the enlarged class alone, the proof gives d = p^b for some nonnegative integer b. If K is the maximum initial exponent, the same argument bounds b <= K+a. The sharper b <= a in the candidate theorem correctly uses initial exponents zero.

## 3. Cyclotomic coefficient argument

Let L=p^a, n=L/p, and let h be prime to p. If a rational-coefficient polynomial P of degree less than L vanishes at zeta_a^h, its minimal polynomial is

    Phi_L(X) = 1 + X^n + ... + X^((p-1)n).

Thus P=Q Phi_L with deg Q<n. There is no coefficient overlap between the different terms of Q in this product: for each u<n the coefficients at u,u+n,...,u+(p-1)n all equal Q_u. This proves precisely the required fiber equality, including zeros. It remains valid for rational weights and any primitive-root multiplier h.

The irreducibility justification is sound. After X -> X+1, reduction modulo p is X^((p-1)n), the constant coefficient is p, and the polynomial is monic; Eisenstein applies. No assumption that the relevant overlap is a subset with distinct labels enters this step. Repeated row labels are handled separately by row orthogonality.

## 4. Matching-support lemma: checked in both directions

The potentially delicate step is valid because of a positive-coefficient uniqueness fact. If two different rows have the same exact label x, their inner product is the positive row-amplitude factor times the cardinality of their support intersection. Row orthogonality therefore forces their supports to be disjoint. In particular, at most one row with a prescribed label can contain a fixed column, and hence at most one can contain a prescribed column pair.

For columns j,l in different residue classes modulo p, the column difference is a unit. Their zero Gram entry has coefficients

    beta_x = sum_(r:x_r=x) p^k_r T[r,j] T[r,l].

Because of the preceding disjointness, each beta_x is either zero or the weight of exactly one row. Cyclotomic fiber equality now produces exactly one row at every sibling label x mod n, each containing j,l and having the same p-power weight. It does not merely produce equality of a sum of several row weights.

For a mixed row i, choose two supported anchor columns in different residues. Their pair fixes a unique sibling row at every lifted label. For any additional supported column j, one anchor has a different residue from j. The pair (j,that anchor) produces a sibling row. It must equal the already fixed sibling because two rows of the same label cannot share the anchor. This proves inclusion of the original support in every sibling support. Starting from an arbitrary column of the sibling and using the same two anchors proves the reverse inclusion. Thus supports match exactly; equality of weights was already obtained from the anchor pair.

The grouping is unique: every member has the same support and the same lifted-label fiber, and uniqueness at each exact label excludes a competing group. Hence the matched p-tuples are disjoint, which is necessary to apply the subsequent row transforms simultaneously.

To prove residue balance, compare the two tuple rows whose lifted labels differ by n. Their row Gram gives sum_t b_t omega^t=0, where b_t counts supported columns of residue t modulo p. The prime cyclotomic relation forces all b_t equal. Repeated column labels simply contribute their multiplicities to b_t. Since the original row is nonzero, the common b_t is positive. No transformed row is lost.

Both Gram identities really matter. A useful negative control is the 3-by-2 matrix with rows (sqrt(2),sqrt(2)), (1,-1), (1,-1). Its column Gram is 4 I_2, its character labels at order 2 are x=(0,1,1), y=(0,1), and its row exponents are (1,0,0). Aggregated coefficients balance, but the weight-2 row has no equal-weight sibling. The row Gram fails and the matrix is not square. This does not contradict the candidate; it verifies that dropping its hypotheses would invalidate the matching inference.

## 5. Row Fourier transform, square blocks, and quotient phases

For a matched tuple x_q=u+qn, the p-point unitary row transform produces, for residue t,

    p^((k+1)/2) T[j] zeta_a^(u y_j) 1_(y_j=t mod p).

The factor is sqrt(p) times the old row amplitude, so its squared weight is p^(k+1), exactly as claimed. The sign in the Fourier transform is consistent with the character sign in the entries. The residue balance just proved guarantees that these p output rows are all nonzero. Pure rows remain unchanged. All rows are now confined to one column-residue class.

After grouping rows and columns, each residue block B_t satisfies both B_t B_t*=d I_(r_t) and B_t* B_t=d I_(c_t). The first implies row rank r_t; the second implies column rank c_t. Therefore r_t=c_t. This handles dimensions without assuming square blocks in advance. Empty blocks contain neither rows nor columns and can be discarded; at least one nonempty block remains.

Writing y_j=t+p y'_j and dephasing the row by zeta_a^(-x t) gives (zeta_a^p)^((x mod n)y'_j). For transformed rows replace x by u. These are exact exponent congruences, not phase approximations. All masks stay binary, all new squared row amplitudes stay p-powers, labels may repeat, both Grams stay dI, and every nonempty child is square. Thus the whole induction class is preserved.

These intermediate row-basis changes do not relax the phase condition on the original mask. They are used only to prove a necessary property. Nor are they row/column permutations of the original support. Consequently the proof is compatible with connected original support graphs and does not reinstate the disproved full-block decomposition premise.

## 6. Termination and order-one base

Every descent step reduces the character level by exactly one, independently of matrix dimension. At level zero every entry is nonnegative real. Distinct rows are orthogonal, so their nonempty supports are disjoint. There are m such supports in m columns. Each support must be a singleton, and each column is used. Its row norm gives d=p^k_i.

The nonempty assumption is indispensable: an empty matrix would place no restriction on d. It is present in the candidate and preserved. With initial exponents zero, each level increments a path exponent by at most one, so 0<=b<=a. The proper range d<p^a gives b<a. This closes the induction, including p=2, a=1, d=1, and the full boundary d=N. The latter is a theorem/control boundary, not a new claim about the optimization with s=0.

The accepted equality criterion supplies actual minimizers at the allowed divisors and strict separation of the infimum from the floor at the excluded d. The necessity theorem does not by itself calculate any excluded optimum or a numerical gap.

## 7. Fresh independent exact controls

`independent_checks.py` was written for this review. Its zero tests use polynomial long division, and its matching routine discovers siblings from an anchor pair rather than grouping rows by equal supports in advance. Every child is checked with complete row and column Grams. Its certificates retain all matrix labels, weights, and supports at every node.

All controls passed with empty stderr:

1. **46 divisor controls:** p=2 with a=1,...,6; p=3 with a=1,...,3; p=5 and p=7 with a=1,2; every b=0,...,a. These include d=1, intermediate powers, full d=N, pure rows, mixed rows, and different descent depths.
2. **Connected control:** the literal accepted N=8,d=4 binary mask. Both Grams are exactly 4 I_8, and the bipartite support graph has all 16 vertices in one connected component. Its first-level children have unequal exponents (1,1,0,0) and (1,0,1,0), demonstrating why an unweighted induction would fail. Its terminal exponents are all 2.
3. **Three weighted, repeated-label stress cases:** (p,a)=(2,3),(3,2),(5,1). Direct sums of embedded Fourier blocks of orders p^j, in both row/column orientations, are scaled to a common d=p^a. Their dimensions are respectively 30,26,12; both label lists repeat; row exponents vary; dimensions differ from the character order. They contain both pure and mixed rows and descend to exponent a.
4. **Three explicit order-one controls:** p=2,k=0; p=2,k=4; p=3,k=2, each of size 3 with repeated zero labels. They verify that terminal dimension need not be one or equal the character order.
5. **Exact work across those 53 descent cases:** 2,060 matrices validated; 90,722 row-Gram entries and 90,722 column-Gram entries checked; 1,183 matched tuples; 27,830 direct row-Fourier entry identities; 40,100 dephasing entry identities; 1,188 terminal matrices and 1,240 terminal rows. These are the `descent_counters` in the results, excluding the separately recorded census and negative controls.
6. **Cyclotomic controls:** every coefficient vector over {-1,0,1} at orders 2,4,8,3,9,5,7, totaling 28,791 vectors. Every unit multiplier is checked at each order, as are 14 rational-coefficient balanced/unbalanced examples.
7. **Small exhaustive original-mask controls:** all 66,064 binary masks of orders 2,3,4. Accepted counts by d are: N=2, {1:2,2:1}; N=3, {1:6,3:1}; N=4, {1:24,2:8,4:1}. All accepted matrices also pass both exact Grams. These finite controls are not the proof of necessity.
8. **Negative controls:** a degree-preserving 2-by-2 support switch on the connected mask fails a row Gram; a row-weight corruption fails the row norm; an invalid non-power terminal d fails the base norm; an empty matrix is rejected; and the column-only rectangular countercontrol above demonstrates the importance of the complete class.

The original optimization model was also independently reconstructed in Q[z]/(z^4+1). With H[r,c]=z^(rc), D=H entrywise R, A=H-D, B_tilde=A*/4, and M_tilde=B_tilde^(-1), the checker verifies both inverse products, four nonzeros in every row and column of B_tilde, and both error Grams equal to 4 I_8. The normalized M=M_tilde/sqrt(8) therefore has squared spectral error 1/2 and the original simultaneous inverse sparsity. Both D Grams are retained too. Exact matrices and Gram coefficients are in `INDEPENDENT_ORIGINAL_MODEL.json`.

## 8. Candidate replay and reproducibility

The candidate's new checker independently reports 55 divisor cases, the connected control, a 16-by-16 repeated-label control, 275,704 descent Gram entries, 89 cyclotomic controls, negative tests, and the original inverse witness. Its replay produced byte-identical `RESULTS.json`, `DESCENT_CERTIFICATES.json`, and `CONNECTED_INVERSE_WITNESS.json`; see `CANDIDATE_REPLAY_COMPARISON.json`. The candidate retains the label “pending independent review” in its frozen results, as expected; this review supplies the acceptance decision without modifying the frozen evidence.

From this review directory, run `python independent_checks.py` to reproduce the fresh independent outputs. The replayed candidate script is in `candidate_replay/verify_primepower.py`; running it writes only its own local generated outputs. `MANIFEST.json` binds this review and all retained files except the manifest and its seal; `SEAL.sha256` binds the manifest.

## 9. Final disposition

No proof correction or missing lemma is required for the prime-power conclusion. The candidate's blanket unresolved-work sentence does require the explicit scope qualification in Section 1; its literal claim that all quantitative gaps remain open is not accepted. The stronger weighted induction successfully avoids the previously disproved assumption that every equality mask is a disjoint union of full d-by-d blocks. Accept the prime-power result and its original-model consequences at the scope stated above, preserving the earlier quantitative results. Leave the mixed-prime case and broader owner open. No external write, repository commit, status change, or literature-priority assertion is part of this review.
