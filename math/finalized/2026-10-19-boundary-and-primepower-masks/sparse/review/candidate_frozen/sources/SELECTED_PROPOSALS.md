# Three source-bound completion tasks

Selection: 19 October 2026. No external writes, historical-program execution, owner changes, or acceptance claims.

Baseline: the independently reviewed staged index at `partial_gate_sheet_sync_20261019_0045/index/stage/math/finalized/2026-10-15-rebuilt-open-record-index/open-record-index.json`. All 225 current open records were read. Census: 102 CLOSED / 225 TO RESEARCH / 327 views. Publication of that derivative is separate. The two active F020 and phase-minimax tasks are excluded.

## Recommended order

1. **Prove sharp Gaussian deficit transition** — ALG-036, unchanged priority 34. Strongest immediate candidate: a concrete primary-theorem route and matching construction are available, but the proposed result is NOT accepted.
2. **Prove endpoint-anchor size lifting** — M-SCAN-DIMENSION, unchanged priority 34. An exact all-dyadic missing lemma, with the full chart and all guards already accessible.
3. **Classify prime-power Fourier masks** — M-SPARSE-DEFECT, unchanged priority 42. A new uniform arithmetic-family proof target; deliberately avoid the disproved full-block reduction. Higher mathematical risk than task 1.

These are three distinct mathematical tasks, not promises of three parent closures. No stored priority is changed by the dispatch order.

## 1. ALG-036: sharp thin-deficit endpoint

### Sources

- Accepted report, Sections 1–8: `/workspace/shared/alg036_endpoint_20261018_2053/REPORT.md`.
- Independent acceptance: `/workspace/shared/alg036_endpoint_review_20261018_2112/REVIEW.md`.
- Immutable report: https://github.com/AgentSlop-Si/research/blob/7769fb444edb0b63ebbce7e31dc52966ba08f4f0/math/finalized/2026-10-18-sixth-cycle-six-results/gaussian_endpoint/candidate/REPORT.md
- New readable primary ingredient: Bennett–Carbery–Christ–Tao, *The Brascamp–Lieb inequalities: finiteness, structure and extremals*, Definition 1.1 and Example 1.6, printed pages 1–3: https://math.berkeley.edu/~mchrist/Papers/bcct11.pdf . The 64-page author-hosted body was opened and the exact geometric datum and constant-one statement checked. The requested specialization below is an inference to prove, not a theorem quoted from that source.

### Exact next lemma and construction

For every complex orthogonal rank-d projector P on C^N, Z distributed CN(0,P), b in C^N, and r>=0, prove or refute

    Pr(max_j |Z_j-b_j| <= r) <= (1-exp(-N r^2/d))^d,  1<=d<=N.

Prove matching equality when d divides N using d disjoint equal-size coordinate blocks, each residual vector constant on its block and normalized. This would identify the exact fixed-radius projector/translation extremum on those dimensions.

Concrete proof route to check: write P=VV*, V*V=I_d, let p_j be the squared norm of row j, and omit zero rows after handling their deterministic coordinate constraint. Normalize each nonzero complex row into a real rank-two coisometry B_j. Verify B_j B_j*=I_2, sum p_j B_j*B_j=I_(2d), and sum p_j=d. Apply geometric Brascamp–Lieb to disk indicators times Gaussian densities, use the already accepted translated-disk inequality, and check concavity of p log(1-exp(-r^2/p)). Pay particular attention to the complex-to-real normalization, zero diagonal variances, arbitrary translations and r=0. No independence of the N coordinates may be assumed.

Carry the lemma through the accepted transcript-only adaptive posterior/stopping proof. Quantify the thin-deficit transition at d on the order of N/log N, and, where the equal-block construction applies, the critical window N C^2/d-log d. Transfer to the relative-norm radius C||x||_2/sqrt(N) by explicit shrinking upper/lower norm-concentration envelopes; do not condition the Gaussian posterior on the norm event. Distinguish a matching Gaussian-average measurement scheme from an every-fixed-input randomized guarantee.

### Previous limits and completion

The old l2-volume argument did not settle the endpoint. The accepted sequential-coordinate product bound settled fixed positive deficit fraction but explicitly left thin deficits open; merely substituting a smaller delta in its coarsened inequality is not this task. Expected deficit and mere nonzero deficit are insufficient, as the retained full-information/random-one-omission controls show.

Complete with an independently checked sharp finite bound, admissible matching construction and quantitative thin-deficit consequence, or a literal counterexample identifying the failed proposed lemma. Keep no-side-channel, independent-seed and pathwise-rank conditions. No Fourier arithmetic lower bound, production result, historical novelty or whole ALG-036 closure follows.

## 2. M-SCAN-DIMENSION: all-dyadic endpoint-anchor lemma

### Sources

- Full exact formulation, Sections 2–5: `/workspace/shared/bitrev_uniform_20261018_1919/candidate/REPORT.md`.
- Review and its indispensable good-anchor qualification: `/workspace/shared/bitrev_uniform_20261018_1919/review_independent/REVIEW.md`.
- Original chart source: `/workspace/shared/bitrev_uniform_20261018_1919/candidate/sources/PROOF_CERTIFICATE.md`.
- Immutable report: https://github.com/AgentSlop-Si/research/blob/b1093eb6705fbef4e6dfcc0e29e69f6a5d31e21e/math/finalized/2026-10-18-fifth-cycle-six-results/bit_reversal/candidate/REPORT.md

### Exact next lemma

For every N=2^m>=8, t=N/4+1, actual m-bit-reversal P, and T=3I+L+L^T+E_00, prove that the N^2 by t(5N-6) integer matrix

    H[(r,s),(k,i,j)] = ((TP)^k)[r,i] ((PT)^(t-1-k))[j,s],
    0<=k<t, |i-j|<=2,

has row rank N^2 over Q. Equivalently, if all matrices (PT)^(t-1-k) Z^T (TP)^k have zero entries throughout the pentadiagonal band, prove Z=0.

The substantive route is a dual-observability or nonzero complementary-Schur-block argument using the exact doubling identities in Section 5, including t_(2n)=2t_n-1 and

    Q_n^T T_(2n) Q_n = [[3I+E_00, I+L_n], [I+L_n^T, 3I]].

A proof must handle the interleaver and both coupling blocks. An explicit new all-size anchor is admissible only if this precise anchor is disproved and its original-chart regularity and threshold rank are proved; do not substitute generic maximal-rank assertions.

### Previous failures and completion

The identical centrosymmetric anchor T=3I+L+L^T has an all-depth annihilator at every odd bit length >=5. The endpoint perturbation breaks that particular symmetry but this alone proves no rank theorem. Copying old finite minors into a supposed block diagonal ignores the nonzero coupling. N=8,16,32 already pass; no N=64 census is requested.

A successful uniform lemma transfers through the accepted inverse-tridiagonal/pentadiagonal tangent equivalence to the original all-dyadic generic-dominance threshold. Otherwise give an exact algebraic family of annihilators or one exact endpoint-anchor counterexample and state that it rejects only this anchor, not generic dominance. A timeout, restated missing lemma or another finite passing rank is not a completed mathematical result. Preserve nonzero neighbors and all leading/trailing principal-minor guards. Fourier membership, intermediate-depth gauge completeness and runtime claims remain separate.

## 3. M-SPARSE-DEFECT: prime-power arithmetic classification

### Sources

- Exact equality criterion and prime base case: `/workspace/shared/sparse_defect_budget_20261018_1240/REPORT.md`, Results 1–4 and Sections 2–6.
- Counterexample to the old full-block route and exact remaining cyclotomic system: `/workspace/shared/sparse_uniform_divisibility_20261018_2054/REPORT.md`, Sections 2–8.
- Independent acceptance: `/workspace/shared/sparse_uniform_divisibility_review_20261018_2112/REVIEW.md`.
- Immutable latest report: https://github.com/AgentSlop-Si/research/blob/7769fb444edb0b63ebbce7e31dc52966ba08f4f0/math/finalized/2026-10-18-sixth-cycle-six-results/sparse_divisibility/candidate/REPORT.md

### Exact next lemma

Set N=p^a for any prime p and integer a>=1. For a primitive N-th complex root zeta, let D[r,c]=R[r,c]zeta^(rc), where R is binary with d ones in every column and 1<=d<N. Prove or refute

    D*D=dI  implies  d=p^b for an integer 0<=b<a.

Divisor sufficiency is already proved, so this single uniform necessity theorem would completely classify floor sharpness at every prime-power length. It is not a request for another weight or tested order. Any exact non-p-power d witness also refutes the original unrestricted divisibility conjecture.

Use prime-power cyclotomic cancellation and the filtration of characters by p-adic order, retaining BOTH whole Gram identities and the original Fourier phases. The exact cyclotomic equations in the latest report provide the starting algebra. A descent proof must explicitly justify its induced subspaces, dimensions and integrality at every level; do not assume that the binary mask itself quotients to smaller full blocks. This route is a proposed research approach, not an established intermediate lemma or promised theorem.

### Previous failures and completion

The connected (N,d)=(8,4) mask and its N=8m,d=4m odd-m family disprove universal disjoint-full-square-block reduction. They satisfy divisibility and must be positive controls for any new invariant. Weight-three structure does not generalize automatically. The (12,5) MILP time limits prove nothing and lie outside this proposed prime-power proof; no repeat is requested. Arbitrary-phase weighing matrices, one-row constraints, or numerical near-orthogonality change the problem.

Complete with a uniform prime-power theorem and its exact consequence for Delta_(N,N-d), or an exact binary counterexample with every Gram entry and original inverse-row minimizer verified. A failed auxiliary premise alone does not close the prime-power classification. Leave mixed-prime necessity and every nonsharp exact optimum open unless separately proved. The owner and all priorities remain unchanged.

## Selection boundaries

Not selected: magnetic degree 31, rectangle N=2873, another fixed RS layer, larger chirp tests, repeated accepted implementation/comparison gates, or missing-byte owners without a new locator. Q2's canonical displacement obstruction and the F8 elimination timeout are preserved; no genuinely validated new cold solver/elimination mechanism was found here. The original all-N sparse divisibility problem is not falsely called solved by selecting a prime-power theorem. No new publication, numerical execution, benchmark, owner, score or closure is authorized by this selection.
