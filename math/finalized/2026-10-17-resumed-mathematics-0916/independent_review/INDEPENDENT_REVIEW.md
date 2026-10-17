# Independent review of the resumed mathematics cycle

17 October 2026. Baseline commit: `bcbc3854c9af6bac7ccaf8378c1629ae63889fbb`.

## Decision

Accept the bounded N13 degree-seven attainment, the two restricted Fourier-factorization obstructions, and the exact-data ALG-064 numerical reference integration at the precise scopes below. Accept the C03 current-gate clarification, with **zero new whole-parent closures**. F015 is unchanged. All parent statuses and priorities remain unchanged; the baseline census is 90 CLOSED / 237 TO RESEARCH / 327 recorded views.

This is scientific artifact acceptance. It does not assert that publication or spreadsheet application has occurred. Those actions need their own final-byte and preservation checks.

Every executable mathematical check in this review was freshly authored. The reviewer did not execute or import historical research programs or the producers' programs. Producer JSON outputs were read as inert data. Imports among the review's own newly authored modules are explicit. Standard-library exact integers and rational arithmetic suffice. Public replay derivatives change only input-file location handling and have been rerun against the frozen candidate bytes.

## 1. N13: degree-seven attainment accepted

Accepted claim: in characteristic 53, with N=13, q=16, the original negative unnormalized Fourier target, and exactly one effective alpha node in each cross-sign orientation, the minimum number of original signed-resolvent physical banks over F_(53^7) is 16. Competing banks may use arbitrary legal beta. The upper certificate itself uses beta=1, allocation (7,1,1,7), y=z=2, and

    H(t)=t^7+40t^6+9t^5+25t^4+31t^3+4t^2+25t+25.

The lower bound of 16 is inherited, explicitly, from the pinned accepted field-uniform lower theorem and its arbitrary-beta binding. This review does not claim to reconstruct that historical polynomial-minor proof. Its scope is stated in the bound source and applies to the free-cross-singleton model. The newly checked literal certificate supplies the upper bound without relying on a necessary recurrence gate as sufficient evidence.

### Independent reconstruction

- Gaussian coefficients were reconstructed with a Pascal recurrence, separately from the producer's search formula. Independent polynomial arithmetic and row reduction reproduce every one of the 2,756 declared (y,lambda) pairs, all affine support polynomials, and the complete absence of missed or duplicate pairs.
- Independent irreducibility-first enumeration finds 407 irreducible degree-seven polynomials, of which exactly eight satisfy all thirteen full sector systems. This is a different gate order from the author's search.
- The author's exact sequential classification was independently reconstructed with a two-equation, one-unknown necessary-gate solve: 2,693 necessary-window failures, two zero-root failures, one repeated-root failure, 52 degree-seven splitting failures, and eight full-sector witnesses. Their pairs and full solutions agree.
- The first H satisfies t^(53^7)=t modulo H and gcd(H,t^53-t)=1. Since seven is prime, these identities prove irreducibility. Its seven Frobenius conjugates are distinct and nonzero; multiplying their actual linear factors gives H coefficient by coefficient.
- A separate extension-field Vandermonde solve reconstructs every bank amplitude and raw weight. Every root, orientation, alpha, beta, nonzero guard, amplitude, raw weight and aggregate entry agrees with the producer's literal certificate.
- Instead of the producer's Gauss–Jordan inversions, this review uses the unique zero diagonal in each literal cyclic-bidiagonal branch to perform exact backward substitution. All 208 inverses pass both left and right products, for 416 inverse identities. All 16 bank matrices are nonzero, and all 169 entries of the original Fourier target match.
- Independent falsification controls give 169 mismatches on deleting the 1/13 average, 144 on reversing the Fourier sign, and 91 on perturbing the final branch weight.

A field embedding into F_(53^d) for 7 dividing d preserves the complete raw identities and nonzero guards. Together with already accepted degree-2/3/5 witnesses, this proves the sufficient condition gcd(d,210)>1. It is not a converse. Degree one retains its accepted minimum 18; the remaining uncovered degrees d>1 are coprime to 210. Unrestricted cross allocations, extension-valued cross-node classifications, other parameters, uniform constructions, novelty and Fourier runtime remain outside this result.

The four recorded views M-MAGNETIC-SPAN, NEW-17, Q35 and NEXT-MAGNETIC-SIGNED remain TO RESEARCH, priority 56.

## 2. Fourier target fiber: two restricted obstructions accepted

The source chart is explicitly

    S[i,i]=d[i], S[i,j]=l[i]m[j] for i>j, S[i,j]=u[i]v[j] for i<j.

Thus each strict lower cut block has rank at most one. This implication comes directly from the allowed coefficient formula, not from a graph-capacity comparison.

### Cyclic-tridiagonal inverse slice

For every N>=8, every middle permutation P, and every primitive Nth root zeta, F[i,j]=zeta^(ij) cannot equal B P A in this chart if either A^-1 or B^-1 is cyclic tridiagonal.

The proof was checked for coefficient-zero and wraparound subcases. A nonzero selected inverse column supported on k-1,k,k+1 has a nonzero restriction to four consecutive Fourier rows, by injectivity of the corresponding 4-by-3 Vandermonde map. Its annihilator row is

    (-t_k^3, a t_k^2, -a t_k, 1), a=1+zeta+zeta^-1, t_k=zeta^k.

A fresh formal multivariate polynomial expansion verifies the exact four-row determinant a^2 times the Vandermonde product. Here a cannot vanish for N>=8. Four such nonzero vectors cannot share a line. This contradicts the required rank-one strict lower block after any middle permutation. Fourier symmetry and transposition prove the either-stage statement. Invertible diagonal target scalings preserve both the chart and inverse-support restriction.

Separate quotient arithmetic at N=8 reproduces the pinned determinant 28zeta^3+28zeta^2+12zeta-12, its printed reciprocal, and field norm 2048. All 70 four-center subsets have nonzero annihilator determinant. The tridiagonal Green inverse example and I+J inverse example were checked in both multiplication orders.

### Separately frozen diagonal-plus-rank-r supplement

For every nonnegative r and N>=4r+4, the factorization is also impossible if either inverse is D+R, D diagonal and rank(R)<=r.

The proof's invertibility step is essential and valid: R injects ker(D), so D has at most r zero diagonal entries. Restricting F D to m consecutive rows and any m columns leaves rank at least m-r. Adding F R can reduce rank by at most r. Hence the block has rank at least m-2r. Setting m=2r+2 gives rank at least two in a strict lower cut block. Transposition and invertible diagonal scaling preserve this class as claimed.

A fresh rational elimination verifies the supplement's concrete stage with diagonal 3, lower entries 1 and upper entries 2, including both-sided inverse equations. Its inverse has entry C[0,2]=-64/511 and disjoint minor C[{0,2},{1,3}]=32/511. It is therefore outside both N=8 inverse restrictions. The combined restrictions do not exhaust the chart.

M-NONLINEAR-COMPATIBILITY remains TO RESEARCH with priority unchanged. The unrestricted 64-equation F8 target ideal is undecided. No image-closure exclusion, general Fourier lower bound or runtime improvement follows.

## 3. ALG-064: exact-data numerical reference bridge accepted

Accepted input contract: finite exactly represented complex dyadic raw data, 0<=d<N, and rational absolute tolerance 0<epsilon<=1. The output is the full unnormalized positive-exponent DFT to the stated absolute tolerance. This is exact-data inference, not stable inference from noisy observations.

The proof and inert source were reviewed at the following interfaces:

1. The entire tail system j>=d is solved exactly. A returned connection retains declared span d even when its polynomial degree is smaller. It is not falsely asserted from the smaller degree onward. Inconsistency triggers the charged fallback.
2. Integer pivot-minor bounds after clearing the dyadic denominator support the conservative rational coefficient and elimination-height ledger. Tiny pivots are paid for and do not establish conditioning.
3. Componentwise rounding with l1 coefficient error at most h gives full-tail defect R<=d h S. Choosing h<=epsilon(2N)^(-d)/(8d(S+1)) meets the accepted numerical evaluator's residual budget. The actual defect is recomputed.
4. The conservative threshold tau=(2N)^(-d) remains valid if the rounded degree drops. The boundary retains its declared span. Full precision inequalities, squared-modulus classification and separately rounded division match the inherited evaluator contract.
5. The rational Machin/Taylor node generator has an explicit error certificate and conservative finite bit/operation ledger. The direct all-bin fallback is separately certified and charged O(N^2) arithmetic. The slower O(N(d+1)^2) exact discovery and failed work are not omitted.

### Independent tests of frozen output bytes

- All 102 saved raw-input/output vectors, totaling **1,115 output entries**, pass an independently authored transcendental oracle. This oracle uses pi=4(atan(1/2)+atan(1/3)), rather than the producer's Machin identity, with independently certified Taylor nodes and exact direct power sums. The author's 1,001 numerical-bin count excludes 114 zero/copy entries; the review checks them too.
- A separate Gaussian-rational complex RREF, rather than the producer's real-block system, reproduces all 102 branch decisions: 70 recurrence, 21 certified direct fallback, ten zero and one copy.
- All 70 recurrence cases independently satisfy exact tail equations, independently rounded defect bounds and coefficientwise cyclic boundary identities.
- An independent exhaustive cap-one comparison passes all 1,089 ternary input sequences at lengths two through six. Every recorded claimed error bound is at most the requested epsilon.

These tests support transcription and integration. The all-input theorem rests on the proof and charged interfaces, not finite test extrapolation. This closes the exact-data reference bridge only. ALG-064 remains TO RESEARCH, priority 42. Stable/noisy recognition, improved root or fallback complexity, non-dyadic raw encodings, real-residual normalization, historical-code integration, resource-limited production certification and practical speed remain separate.

## 4. C03/F015 stopping-condition audit accepted

No whole-parent closure is supported. C03 remains priority 12 and F015 priority 15, both TO RESEARCH.

The compact C03 gate omits explicit full-record residual obligations. The six proposed action/stop clarifications correctly preserve exact-family attribution and legal sparse-recovery requirements. They do not infer full-family prior publication merely from classical ingredients, or legal recovery merely from a zero resultant. The proposal's old-text suffixes and recorded hashes were verified without exporting its native mapping.

The three inspected historical source bodies match both their named SHA-256 digests and Git blob IDs. This is source/preservation verification, not a replay of historical scientific checkers. The audit transparently attributes later acceptance statements whose full byte bodies were not recovered in that audit.

One summary omission was corrected before freeze: F015's source theorem uses N=2^k>=4, Q=2^floor(k/2), M=N/Q and 1<=b<=M/2. The finalized report now retains these assumptions. Its completed inactive comparison stays completed; sharper solver and broader qualification obligations are not erased. F015 receives no new gate or status edit.

## 5. Preserved failed attempts and limits

The review records rather than hides corrections:

- An initial independent census-category assertion used the complete b=3 system in place of the producer's weaker necessary two-window gate. Two zero-root cases fail that stronger system earlier. The attempted checker and failure are retained inert; the corrected checker solves the actual two-window gate and separately verifies the stronger necessary implication. No witness changed.
- The output-oracle loader initially expected key `x`; the frozen producer schema uses `raw_dyadic_input`. This failed before arithmetic and was repaired. The original loader is retained inert.
- The producer reports two expanded ALG-064 test invocations reaching the same final JSON integer-string limit after mathematical assertions. The final implementation outward-rounds only the exported node-radius receipt to a verified dyadic upper bound and reruns the complete suite. The exact reported error and preservation limits are recorded separately; no pre-fix source or failed-run file was retained by that worker.

These are not positive scientific claims. They do not justify executing historical programs, omitting paid failure work, or promoting broader status.

## 6. Frozen acceptance and replay

`ACCEPTANCE.json` binds the exact accepted reports and candidate manifests. `SHA256SUMS.json` binds this review's publication-safe files, excluding caches. The source packets and this review contain no native spreadsheet preimages or mutation payloads.

From this directory, the scientific replay sequence is:

    python n13_independent.py
    python n13_literal_independent.py
    python n13_census_binding.py
    python fourier_uniform_independent.py
    python fourier_controls_independent.py
    python fourier_supplement_independent.py
    python alg064_independent.py
    python alg064_cap_independent.py

The wrappers default to sibling `../reports/` packets and accept an explicit input path where necessary. They execute only review-authored code. Exact final native state, repository commit ancestry and remote blob bytes are a separate application audit after publication; do not interpret this scientific report as that later receipt.
