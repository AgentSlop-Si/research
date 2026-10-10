# Independent review: constant-eight block-coherence refinement

Review date: 10 October 2026. Verdict: PASS. This separate receipt depends on the independently accepted whole-left envelope and uniform guard proof. The earlier constant-thirteen theorem remains unchanged.

## Accepted refined bound

For every odd N≥1025, put d=floor(sqrt(N)/8), m=N−d. There is a representation of the negative Fourier matrix by at most

2N−2floor(sqrt(N)/8)+2 = 2N−sqrt(N)/4+O(1)

permitted signed banks over a splitting field of K=Q(q). The polynomial defining the m distinct nonzero shared same-sign nodes lies in K[t]. The orientation multiplicities are (m,1,1,m), both cross-sign nodes are 1, β=1, and the splitting-field degree is at most m!.

This is a larger additive square-root saving with leading coefficient still 2. It does not establish K-only attainment, approximately 8N/5 banks, unrestricted minimality, efficient construction, an FFT runtime improvement, or historical novelty.

## 1. Independent exact block-Gram proof

Choose a chirp-Fourier atoms, b Fourier atoms, and c coordinate atoms from the three bases already proved mutually unbiased for every odd N. Each within-basis Gram block is an identity. A cross-block has entries of modulus 1/sqrt(N), so its operator norm is at most its Frobenius norm: sqrt(ab/N), sqrt(ac/N), or sqrt(bc/N).

For coefficient-group norms x,y,z≥0, the full Gram quadratic form is therefore bounded below by

x²+y²+z²−2sqrt(ab/N)xy−2sqrt(ac/N)xz−2sqrt(bc/N)yz.

If a≤7d, b≤d, c≤5d, and N≥64d², this lower bound is at least the quadratic form of I−Q/8 on the nonnegative triple, where Q has diagonal zero and off-diagonals sqrt(7), sqrt(35), sqrt(5). Entrywise comparison is being used only on this nonnegative norm triple; arbitrary signed-vector quadratic-form monotonicity is not assumed.

The exact leading principal minors of 8I−Q are

8,
64−7=57,
512−8(7+35+5)−2sqrt(7·35·5)=66.

They are positive. Sylvester's criterion proves 8I−Q positive definite. Thus any nonzero grouped coefficient vector has strictly positive full Gram form, and the selected atoms are linearly independent. The conclusion remains strict at N=64d²; an equality case in the numerical threshold does not create a zero Gram eigenvalue. Empty groups may simply be discarded.

This validates both the author's block argument and the root's separate spectral-radius derivation. The latter is equivalently justified by monotonicity of the spectral radius of nonnegative matrices, together with rho(Q)<8.

## 2. Atom counts and aliasing

For the derivative-functional exclusion, the step-two annihilator degree is r=2(d−1). With the conservative constant-inclusive polynomial degree ranges from the accepted uniform proof,

a=(E_max+1)+(O_max+1)+2r=7d−10,
b=d−1,
c=d+2r−1=5d−5.

These satisfy the block bounds. The two chirp intervals are 0,…,E_max+r and e,…,e+O_max+r. Under N≥7d,

E_max+r≤(7d−11)/2<e=(N+1)/2,
e+O_max+r<N,

so neither overlap nor modular wrapping invalidates their atom count or the subsequent leading-coefficient argument.

For the coordinate-functional exclusion, the corresponding group bounds are a=3d−6, b=d−1, c=d, also covered by 7d,d,5d. Therefore the new block theorem replaces both scalar-coherence uses in the original uniform proof, rather than improving only one of them.

## 3. Every remaining hypothesis is retained

For odd N≥1025, d=floor(sqrt(N)/8)≥4 and N≥64d². For d≥4 this implies all hypotheses needed in the previously reviewed proof:

- N≥7d for distinct/nonwrapping frequency intervals;
- m≥4(d−1), leaving a nonempty interval after step-two annihilation;
- m+1≥3(d−1), sufficient for the ordinary recurrence contradiction;
- m≥(N−1)/2, required by the original physical-row interpolation;
- dim W≥N−5d+12≥(N+1)/2, sufficient for the independent root evaluations in the incidence argument.

No later step uses the old inequality 13d−17<sqrt(N) except to obtain these now-reverified facts and the replaced atom-independence conclusion. Hence coordinate and derivative exclusions, the squarefree pencil, irreducible root-incidence intersection, descent of a good polynomial to K, and the finite grid recipe all remain valid without any logical gap.

At the first admissible order N=1025, d=4, m=1021, and the bound is 2044 banks. The shifted chirp intervals are 0,…,8 and 513,…,521; the derivative groups have sizes 18,3,15. The coefficient-grid recipe still has Nd+2m choices per affine free coordinate and is not asserted efficient.

## 4. Independent exact controls and bindings

fresh_constant_eight_check.py computes the principal minors symbolically from the explicit 3×3 matrix and verifies the integer inequalities, atom counts, and interval separation for every odd N from 1025 through 100001 (49,489 orders). The finite check is supporting evidence; the direct inequalities and positive-definite comparison prove the all-order result. Results are in FRESH_CONSTANT_EIGHT_RESULTS.json.

This review binds two separately authored frozen sources:

- COHERENCE_CONSTANT_EIGHT_ADDENDUM.md, SHA-256 4c30b38a5ae5fef4c95fc2eea79f152dea44de36c81db5934d42fc111dfdb45e.
- research_cycle_1753/ROOT_THREE_BASIS_REFINEMENT.md, SHA-256 9ec7ec4a2c51778183b4686ecb1b879f16dbed0659205c27c8e73f2daa68eb5a.

The underlying complete uniform proof is separately accepted at SHA-256 9404352b64e3569f5cde5ae83e665b16bc03c2a9d0caa977f0c42d1ccbcd9ebb; its independent receipt is UNIFORM_SQRT_REVIEW_RECEIPT.json. The envelope and legal-bank reconstruction are separately accepted in BANK_ENVELOPE_REVIEW_RECEIPT.json. This refinement changes only the coherence estimate and the resulting permissible N,d range.
