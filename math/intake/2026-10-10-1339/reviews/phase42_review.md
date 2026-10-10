# Intake and proof review: novelty report and Phase42 three-row branch

Review date: 10 October 2026. Local review only. No remote files, spreadsheet cells, or repository state were changed. Submitted programs were read as text when needed but were never run, imported, or compiled. All new computations below use the reviewer's separately written programs.

## Result in brief

The novelty report is an exact duplicate of the report already included in the accepted unitary-collinear audit. Its all-length real-collinear theorem and doubled Schur-treewidth constant must not be recounted.

The supplied Phase42 ZIP is a distinct three-row/signature/product branch, not the multirow Phase42 package described by that report. A bounded byte search found no identical complete ZIP and only six inherited member hashes in the existing local corpus. Its elementary finite-signature theorem is correct; its N=128 all-row collision certificate and all eight stated single-sum/product Jacobian ranks have now been independently reconstructed. These are complementary restricted-model results, with no exact Fourier product construction or historical-priority clearance.

## 1. Exact intake and version identity

| Incoming item | Library identity and version | Bytes | SHA-256 |
|---|---|---:|---|
| FFT_RESEARCH_NOVELTY_REPORT_2026-10-10.md | [private source identity]; version 0 | 14,751 | 8204a0d3218f16f2a9a764c655ceae1ddbdb10e16b854d0ff5ee57f4f487849f |
| fft_green_research_phase42_2026-10-10 (1).zip | [private source identity]; version 0 | 5,958,673 | 3681d4c092f7cfe0fc0935903afc8d4254ac8288a173e037f91b7ad359c2ad55 |

The report was read in full. It is byte-for-byte identical to [accepted all-length unitary audit], previously retrieved in the 12:48 audit. This is duplicate evidence, not a new version.

The incoming ZIP has 31 non-directory members totaling 6,086,399 uncompressed bytes. Its main directory is fft_green_phase42_three_row. All 29 entries in its MANIFEST.sha256 match their actual bytes. The manifest does not cover itself or the top-level start-here note.

The report's own ARCHIVE_INVENTORY instead lists a 6,017,450-byte Phase42 ZIP with 35 entries and a main directory fft_green_phase42_multirow. That inventory establishes a different described branch; it is not a substitute for the absent full baseline ZIP and cannot supply a byte-level diff against that branch. Both sources are dated 10 October, without an ordering that proves which branch supersedes the other.

### Actual corpus comparison

The scan excluded this review directory and checked the existing loose-file corpus plus every member at the first archive level of 829 existing local ZIPs: 178,070 member occurrences, with zero ZIP-read failures. Full-ZIP byte-size/hash lookup found no identical existing loose file or first-level ZIP member. All 31 incoming member hashes were also compared, using exact size/hash matches.

Six incoming members match existing bytes:
- The 5,913,220-byte nested previous_full_phase41_checkpoint.zip equals [accepted corrected research cycle] exactly; SHA-256 947ef3cda041d1e167e8013aadd527f9d8a51496d9c3ac90a0391f3580148f3c. It contains 41 entries.
- Five copied dependencies: phase40_holonomy.py, phase40_local_synthesis.py, phase41_exact_jacobian.py, phase41_three_cycle.py, phase41_three_exact.py.

The remaining 25 members had no identical hash in the scanned scope. Nested archives were not recursively rescanned; no claim of exhaustive corpus-newness follows. No local TAR archive was present. Full member hashes, match locations and coverage are retained in the adjacent JSON receipts.

The report's 279 ZIPs, 7,545 distinct text/code bodies and 23,074 listed TAR members describe its historical indexing pass. They are neither theorem counts nor the coverage of this review. Its claim of ten Phase42 tests concerns its other branch; this incoming branch records nine tests. This review did not execute either uploaded test suite.

## 2. Reconciliation of the duplicate novelty report

### The two highlighted deductions

1. **All-N real-collinear unitary Green exclusion.** Already independently accepted in [accepted all-length unitary audit] and linked under current native Q34. For every N>=4 and arbitrary finite term count, ordinary nonsingular single-cycle unitary Green resolvents with coefficients on one common real line in C cannot be invertibly monomial-equivalent to Fourier. Do not reopen or recount it. The separate accepted [accepted phase-averaging independent review] supplies actual real N=2/N=3 witnesses and a finite complex phase-orbit span equal to all constant-diagonal matrices, hence a column-gauged Fourier realization at every legal size. This proves sharpness and essential coefficient-class boundaries; the report's request to classify these small cases has already been satisfied.

2. **Treewidth ceil(N/4)-1.** Already independently accepted as SV28-04 in [accepted complete-extension audit] and carried under SCHUR-V28. Preserve the complete-extension graph with all E/P edges, the actual-field total-nonsingularity hypotheses, and the distinction between dimension/treewidth and operation count. Also preserve the already accepted universal planar quadratic-size realization and the correction that fixed-minor-free extensions are not impossible without a size restriction. The report supplies no additional constant improvement.

### All twelve ranked families

The report's ranking is a historical editorial assessment, not a current master ordering.

| Report entry | Existing evidence/state to preserve | Intake disposition |
|---|---|---|
| 1. Moving Rogers-Szego ordinary discriminant | Q02/Q29; accepted self-contained discriminant manuscript, with five squarefree families s in {3,7,11,15,19}, prime p=1 mod 4 and p not dividing s. General composite/repeated-prime claims remain guarded/open. LS87 classical formulas explicitly attributed; Zhedanov1997 mathematical body and missing LS87 reference page remain comparison gates. | No new proof, no replacement by “exact-looking” or generic priority language. |
| 2. All-N unitary Green exclusion | Q34; accepted exclusion, sharp N=2/N=3 exceptions and exact complex-span counter-scope. | Duplicate, with later accepted boundary material preserved. |
| 3. Independently routed separator inverse sums | Q04/F018; accepted 9^r cutoff and deficit refinements, with fully stated endpoint and separator grammar. | Historical accepted result, not a new discovery. |
| 4. Three legal Green terms on arithmetic 5x5 blocks | Q11; accepted scoped lower/upper certificate chain, fixed arithmetic family and necessary field/endpoint qualifications. | No fresh replay of that older complete certificate here; report does not broaden to full-N three-term Fourier. |
| 5. Schur terminal treewidth | SCHUR-V28; accepted ceil(N/4)-1, actual-field full-spark/total-nonsingularity conditions, planar size counter-scope. | Exact overlap, no count increment. |
| 6. Dyadic endpoint minimax | Q05/C02; accepted standalone endpoint manuscript at dyadic N>=8, exact N/4+1; established bit-reversal hierarchy and N=8 antecedent attributed. Final DV2008 comparison is complete; distinct DV2007 final-journal check remains open. | Report's broad incomplete-priority wording must not erase the completed DV2008 comparison or accepted manuscript. |
| 7. Reciprocal diagonal-pencil resultants | Q17/C03; arbitrary-matrix fixed-homogeneous-degree theorem already independently proved, including specialization/zero-resultant guards. | “Exact-looking” is outdated as a proof-status description; retain classical attribution and unresolved precise priority. |
| 8. Fixed Weyl-Green pair branching | Q15; accepted fixed ordered-pair, odd-size/gcd-sensitive restrictions, with separate endpoint cases. | No change; not an arbitrary Green or Fourier-circuit lower bound. |
| 9. Growing-fiber transform | Q14; accepted promised-input exact algorithm and its charged O(N log(b+2)+sqrt(N)b^2) scope. | No new theorem or generic input improvement. |
| 10. Blind chirp/sparse recognition | Q07/Q13; accepted guarded recognition/application statements with their current cost ledgers. | Keep exact promised families and individual costs; do not merge unlike algorithms. |
| 11. Phase42 phase-budget/rank saturation | The report describes the multirow branch, including q>=2r-1 and nonreal-slot k>=r-2 claims; that is not the supplied three-row branch. | Do not transfer the report's tests or status to this ZIP. New branch reviewed separately below; no all-N target reachability. |
| 12. Finite-word/weak-error/approximate transforms | Q01/Q16 and their later scoped refinements; exact finite-word contracts, supplied precision, probabilistic/approximate error criteria and charged preparation are distinct. | Do not reduce established scoped proofs to generic implementation uncertainty, or upgrade them to exact unrestricted DFT. Other intake workers own any newer material. |

The later [later publication-readiness assessment] assessment remains the relevant bounded editorial ledger. It explicitly preserves the existing endpoint and discriminant drafts and separates correctness, breadth, priority evidence and standalone readiness. The accepted N7 magnetic-bank minimum is now eight over C, attained over an explicit cubic splitting field of Q(q); Q(q)-only attainment is not claimed. The older report and 13:10 partial N7 wording cannot reopen it. Signed magnetic banks remain a different model from ordinary unitary Hamiltonian resolvents.

## 3. Changed Phase42 mathematics

Source theorem SHA-256: c032d5dd36abad8592c53a8f2b91a081f9f5d0a4f71f97fd646724f2c7607663.

### P42-S1. Projective sectors and uniform finite-q obstruction: accepted by fresh proof review

For one nonsingular weighted Hamiltonian cycle, every r-row restriction has at most r projective column classes. In cycle order,

G[i,j] = (p_i/p_j) H^[i<j]/(1-H),

with all weights nonzero and H!=1. Ratios to a selected reference row change only when a selected row position is crossed. Independent input/output monomial endpoints relabel the classes and rescale their vectors.

For q>=1 summands, if q<N select the physical rows mapping to Fourier frequencies 0,...,q under the proposed external equivalence. Each summand has at most q+1 classes, hence at most (q+1)^q joint classes. Inside a joint class the sum's selected columns lie in the span of at most q fixed vectors. A class containing q+1 columns would contradict the nonzero Vandermonde determinant of these consecutive Fourier rows at distinct roots. Consequently

N <= q(q+1)^q.

If q>=N the inequality is already trivial; q=0 gives the zero matrix and cannot represent a positive-size Fourier matrix. This explicitly closes the source proof's implicit q<N case split.

This covers arbitrary nonzero complex edge magnitudes, ordinary legal inverses, and independent per-term monomial endpoints. It is not limited to unitary cycles or real coefficients. It does not cover products or arbitrary dense endpoint maps.

### Relation to the accepted separator theorem

I-W has at most two nonzeros per column. The accepted Q04 theorem therefore applies with separator parameter two and q summands:

N <= 2q*9^q + 2(3^q-1).

External Fourier monomial gauges can be absorbed into the per-term endpoints before applying that flat-unitary theorem. Both restrictions thus hold in this common complex model. A safe combined consequence is

N <= min(q(q+1)^q, 2q*9^q+2(3^q-1)).

The new elementary bound improves finite small-q cutoffs: q=2 gives 18 instead of 340, q=3 gives 192 instead of 4426, and q=4 gives 2500 instead of 52648. Its Omega(log N/log log N) corollary is weaker than the already accepted Omega(log N) separator asymptotic. Preserve the finite-q refinement and alternative proof; do not market it as a stronger asymptotic branch theorem.

Historical priority of this specific signature argument was not cleared by this intake. Its ingredients are elementary cyclic resolvent, projective partition, pigeonhole and Vandermonde facts.

### P42-S2. Exact fixed-order N=128 exclusion: independently reconstructed and accepted

For every four-row set, the three supplied cycle orders partition columns into joint arc sectors. Four columns in one joint sector force a rank-at-most-three 4x4 minor in any additive sum based on these orders, regardless of nonzero complex weights, legal holonomies, scalar coefficients, per-term diagonal endpoints and external monomial equivalence. Every possible external row permutation sends some physical row set to four consecutive Fourier frequencies; those Fourier minors are nonsingular.

The fresh verifier uses sorted interval endpoints and three base-four sector labels, rather than the source program's anchored bit signatures. It validates each input permutation and exhaustively reproduces:

- N=16: 1,820 sets; 268 collisions; 1,552 without
- N=32: 35,960 sets; 32,273 collisions; 3,687 without
- N=64: 635,376 sets; 634,951 collisions; 425 without
- N=128: 10,668,000 sets; all 10,668,000 collide; zero without

This establishes the stated fixed-order family exclusion at N=128, including arbitrary outer row/column permutations. It does not exclude every triple of Hamiltonian orders at N=128. Independent per-term permutations change the pinned orders and are outside this certificate. The lower-size failures are retained as negative controls.

### P42-S3. Three-row conditional capacity: proof and exact nondegeneracy checks accepted

With unit-phase edges and scalar summand coefficients, each sector's column coefficients have fixed moduli. If its 3x3 signature basis V is nonsingular, comparison with c(z)D(1,z,z^2) gives squared-modulus Laurent constraints of degrees -2 through 2. A nonzero constraint has at most four roots on the unit circle. A singular V has a projective span meeting the nonsingular conic in at most two points.

For invertible V, a nonreal ratio between the relevant conjugate(adj(V)[s,0])*adj(V)[s,2] quantities obstructs identical vanishing after division by positive squared coefficient magnitudes. External row-scale factors in the highest coefficient cancel in the comparison. This is a sufficient nonexceptionality test, not a full classification of exceptional signatures.

Fresh literal inverses and both embeddings of i modulo 998244353 verify nonzero determinants and phase cross-differences for all actual classes. The counts/capacities are N16:10/40, N32:9/36, N64:11/44, N128:11/44. The N64/N128 fixed three-row configurations are excluded because 44<N. The weights and selected rows are fixed by this certificate; arbitrary outer row permutations and every possible unit-phase parameter choice are not covered. Arbitrary per-term nonunit diagonal masks would also destroy the fixed-modulus premise.

### P42-S4. Single-sum local real ranks: independently reconstructed and accepted

Using the supplied exact rational-Gaussian parameter data, the reviewer formed the literal I-W matrices, inverted them by independently written Gauss-Jordan elimination, and differentiated G through dG=G(dW)G. At N=8,16,32,64, the three-row anchored-ratio real Jacobian has rank 2N+1, and its first two-row part has rank 2N-2. All four source square-minor residues were reproduced exactly modulo 998244353, using both i embeddings.

Nonzero reductions certify characteristic-zero nonvanishing because all required parameter, inverse and anchored-entry denominators were verified units. The column count gives the matching upper rank. The implicit-function theorem consequently gives a local three-real-dimensional fiber after fixing the first two rows at these regular points. This is a finite-size, fixed-coefficient local statement, not an all-parameter theorem or a Fourier target witness.

### P42-S5. Two-stage product local ranks: independently reconstructed and accepted

For the recorded independently ordered two-stage products, both stages use rational-Gaussian unit phases. The 4N+2-parameter chart has full three-row output rank 4N-4 at N=8,16,32,64. The fresh literal-inverse verifier reproduces every source determinant at the same prime and both i embeddings: ranks 28,60,124,252. Source parameter seeds were treated as the written data specification; source programs were not imported.

This establishes local submersion in a restricted chart. It does not imply that the distant specific Fourier projective target is in its image. The q-summand additive theorem does not apply to this product.

### Important negative-control scope correction

The uploaded phase42_product_control.py uses arbitrary integer finite-field second-stage gains. Its sampled minor/Weyl test is therefore not literally the same rational-Gaussian unit-phase chart used in the differential theorem. This does not invalidate the independently verified product Jacobian theorem, but the two experiments must be labeled separately.

To remove that evidentiary ambiguity, a fresh reviewer control used the actual unit-phase product chart at N=8,16,32,64. Each top-left 4x4 minor is nonzero, and both literal Fourier Weyl equations fail in every matrix entry at the tested reduction. This supports “the sampled unit-phase product is not the literal Fourier matrix.” Failure in the displayed coordinate gauge is not a proof of failure under every possible external monomial gauge.

### Cost boundary

Six legal cycle solves have O(N) online arithmetic once all required weights and inverse holonomies are supplied. No exact all-row Fourier product identity, uniformly inexpensive parameter generation, bounded bit-length, numerical stability, or faster full Fourier evaluator has been proved. Source floating-point finite-difference accuracy was not rerun or promoted in this review.

## 4. Reproducibility and limitations

New programs: fresh_sector_check.cpp and fresh_rank_check.py. Data only: the uploaded cycle text and JSON parameter/certificate records. Evidence outputs: FRESH_SECTOR_RESULTS.jsonl, FRESH_RANK_RESULTS.json, FRESH_SIGNATURE_CAPACITY.json and FRESH_UNIT_PHASE_PRODUCT_CONTROLS.json.

The exact rank reconstructions used one split prime, with both complex embeddings. One nonzero rational minor reduction suffices for the claimed characteristic-zero nonvanishing; this review does not claim to have repeated the source's second-prime tests. The three-row source theorem was read in full, together with its README, checkpoint, validation and prior-art notes and relevant source algorithms. No new scholarly priority search, production benchmark, or broad proof validation of all indexed archive members was performed.

