# Fourier research checkpoint17

9 October 2026 UTC. Five completed review packages, including the latest direct Phase19 upload. No general project FFT breakthrough or historical-priority claim.

## Main positive result: blind sparse inverse discovery

Hero1 Phase19 removes supplied-filter information from a useful structured-input case. If an unknown circular polynomial C with at most s nonzero taps satisfies C(S)r=e0, the method can recover C, certify every cyclic equation, and output the complete Fourier vector in O(Ns+s³) exact field arithmetic. It uses 2s explicitly charged Fourier dot products, recurrence recovery, evaluation at all N subgroup nodes, a small interpolation solve and a full convolution certificate. Require 1<=s<=N/2, a supplied primitive Nth root, and characteristic not dividing N.

For fixed s the promised-family arithmetic cost is linear. An unknown invertible product of a fixed number of graph binomials driven by one unknown impulse is included; combined taps are recovered without factoring that product. Generic input is not covered. Rejected cases need an admissible ordinary FFT fallback, whose root requirements can be stronger than those of the abstract theorem. The all-input O(N log N) guarantee uses fixed detection caps; variable s retains its cubic term and the graph-defect cap retains exponential candidate growth.

Independent checks cover all83,521 vectors in GF(17)^4,402 unknown-delay examples,172 inverse-sparse examples,36 unknown unions and a deliberately changed vector preserving the training Fourier samples but rejected by the full certificate. Original uploaded programs were not executed.

### Phase19 corrections

- Discovery recovers a valid delay representation; the original orientation is not identifiable because reversing the delay and adjusting multiplier/impulse can describe the same signal.
- Graph counters omit subtractions in projective comparisons and full candidate scans. At N4096 the saved one-defect arithmetic proxy103,242 becomes at least113,891 after those10,649 missing subtractions alone. These are corrections to source counters, not wall-clock benchmarks.
- Inherited solver admissibility, root planning, omitted rational arithmetic and conditioning qualifications remain. Exact finite-field recovery does not establish stable floating-point or bit-complexity performance.
- The accepted advance is relative to Phase18. Standard Prony/annihilating-filter ingredients are prior art; historical novelty remains unassessed.

## Other source reviews

### Hero0 Phase10

A length-M frequency stream obeying an order-at-most-d recurrence can be learned from2d samples under the full-stream promise, with explicit guard2d<=M. Its rational finite-sum evaluator handles roots of the denominator by direct repair. The claimed promised-family bound survives with setup charged. Randomized membership tests can falsely accept a nonpromised input and are not deterministic all-input exactness certificates. Some source root-preparation work was omitted from printed counts.

The same-register Fourier realignment has exact rankA² for the stated dyadic split N=AB,A<=B, and flat nonzero singular values sqrt(B/A) under unitary normalization. Its approximation consequence is correct at that same split. This is distinct from the earlier four-leg tensor partition and does not turn tensor rank into scalar runtime.

### Separation-rank theory and Phase32

The additive separation theorem extends the earlier prime-only bound to all complex Fourier lengths through stable rank. With d branch order pairs, a common separated square has side m=floor(N/2^d); if branch rank budgets sum to R, exact representation requires m²<=NR. For Q weighted Hamiltonian Green summands this forces at least one-half log2(N)-O(log log N) branches at all lengths; the stronger prime full-spark bound is separate. The operator-norm error floor is also proved. These are additive representation restrictions, not theorems about products of sums.

Phase32's generic q-column interpolation theorem is valid, and illustrates why matching selected columns or selected-basis Weyl tests is insufficient. Independent reconstruction through N4096 reproduces every saved operator fingerprint, while the actual unfitted columns and global identities fail as stated. Sixteen of17 saved probe-column labels are wrong because a loop overwrote the index; the comparisons themselves are correct. Corrected labels are retained. The positive-integer sampling law also needs N>=2 or a separate pole exclusion at N=1.

### Hero17 Phase7

Rank-one Fourier rectangles satisfy the exact subgroup classification and disjoint endpoint-incidence optimum N min_(d divides N)(d+N/d). The higher-rank independent contraction bound holds in its declared no-sharing cost model. Shared evaluation returns classical Cooley–Tukey. The literal source tile loop omits N first-term zero additions from its ledger; direct initialization repairs that discrepancy. Floating MILP status is corroboration, not a formal exact certificate; the symbolic theorem establishes the optimum independently.

## Additional reviewed layout exclusion

The two-stage balanced-area/complement grid-Green architecture with diagonal middle cannot equal the complex Fourier matrix for any dyadic grid side M>=8, N=M², even with arbitrary edge masks, diagonal factors, zeros and cancellations. The column route is coordinate complement, not bit reversal. Exact finite cuts cover M8 through128, and an analytic area/lattice bound supplies the effective tail M>=256. A general middle permutation is not excluded: it must satisfy a positive linear area-crossing demand, then all remaining coefficient conditions.

This is separate from checkpoint16's natural/bit-reversed paired-cycle layer theorem. Their classes and thresholds must not be conflated.

## Preservation and next work

The prior master is preserved byte-for-byte outside intentionally updated root summaries; previous root files are archived. The five direct source identities and additional supporting Library archives remain attributable in each review package. Source files are inert; independently authored checkers and their relocated replay records are included. This is a bounded source review, not a refreshed exhaustive account inventory.

The private theorem page now includes the checked layer-count proof and its exact scope. New nonlinear cycle-bank capacity, sparse bank-interface certificates and annihilator-feedback constructions are separate ongoing tracks. None is silently promoted by this checkpoint to a Fourier factorization. The compact attachment is a findings summary; complete reproducibility material is in the full checkpoint and persistent master.

## Historical version16

# Fourier research checkpoint16

9 October 2026 UTC. Independently reviewed mathematical and implementation findings. No project-established general exact sub-N-log-N FFT, and no publication-priority claim.

## The result that changes the construction search

For N=2^k, set m=2^floor(k/2) and q=N/m. Consider L layers, each a sum of weighted cycle inverses using the natural cycle and its bit-reversed conjugate. Allow arbitrary diagonal masks, independent edge/wrap weights, endpoint permutations within each contiguous m-block, and arbitrary additional block-diagonal matrices on those blocks, including any active recursive Fourier bank.

An exact full Fourier factorization requires

    L(q/2 + m) >= N/2.

Proof: select the union I of even-numbered m-blocks. An exact block-DFT/Vandermonde argument proves rank F[I,I-complement]=N/2. The natural cycle has q/2 incoming edges across this cut and its bit-reversed conjugate has m. Complementary inverse-submatrix ranks, then sum/product rank subadditivity, bound each paired layer by q/2+m. Block-diagonal inserted banks contribute zero cross rank.

Thus three such layers fail for every dyadic N>=128; four fail for every dyadic N>=256. In general L must grow as Omega(sqrt N). This is a theorem about these cycle orders and endpoint restrictions, not arbitrary Green products or FFT circuits. It closes the current three-layer root-free natural/bit-reversed full-transform candidate, even though several compressed-path identities remain valid. A literal layer-by-layer executor is distinct from an arbitrary jointly optimized evaluator; no unrestricted runtime lower bound follows.

## What remains positive

- Exact isolated N4 variable-pole synthesis is certified with independent complex interval arithmetic. This is finite-size existence, without a uniform size-lifting algorithm.
- Gauged Green principal blocks close under a precise parameter transformation. Their accumulated correction can have growing rank yet still admit linear-time structured application. Rank growth alone is not an application-time lower bound.
- Hero1 Phase18 has exact full-spectrum recovery for signals whose transformed residual obeys a certified low-degree, sparse-defect cyclic relation, including examples whose individual filter defects are dense but joint defect is sparse. Discovery, rejected candidates, resonant repairs and preprocessing must be charged. It is a restricted-input algorithm.
- The recursive Fourier-mass proposal gives a valid conditional target: a uniform O(N)-cost factorization with one full square-root-scale Fourier bank yields an O(N log log N) arithmetic recurrence; a fixed smaller active fraction can yield O(N). The required global factorization and parameter generator are still unproved.

## Other independently checked boundaries

1. Low-crossing middle permutations collapse four quasiseparable stages into a controlled three-stage family. Both forward and inverse crossing constraints matter. Gray routing passes these particular necessary tests; exact coefficient compatibility remains unsolved. A generic image-dimension deficit does not establish nonmembership of the particular Fourier matrix.
2. A complete fixed-pole N4 elimination excludes the specified poles 1/4 and 1/5 even with independently variable projective couplings. This does not contradict variable-pole finite existence.
3. Routed-grid results include an exact N16 phase-pencil obstruction, an exact minimum-three-term F4 calibration, and a four-native-quadrant exclusion. Each retains its particular routes and phase assumptions.
4. Balanced area routing admits a linear-time construction and stronger support than early routes. Its two-stage state realization is sparse. However, block-diagonal wire transport of both Fourier Weyl generators, and monomial intermediate images in the specified phase-pencil family, are independently excluded. General mixed-wire transport is not excluded by those arguments.
5. Phase31 local rank controls and the v18 additive bank-separation theorem check out in their stated scopes. The v18 prime-length logarithmic branch requirement is for additive independently executed Green terms, not arbitrary products or a general lower bound.
6. Hero17 Phase6 tensor-rank identities and endpoint-gauge support bounds hold. Its tensor cut differs from the same-register operator realignment used elsewhere; their ranks must not be conflated.
7. Hero0 Phase9's dense-controller identity is algebraically valid but unrestricted residual spectra still contain the missing Fourier work. Random syndrome checks are not deterministic exact certificates on every input.

## Corrections and costs retained

For a cyclic filter with shift delta, let g=gcd(N,delta). The short adaptive-family dimension bound d+K applies to the coprime shift case. The reviewed noncoprime bound is min(N,d+K+(g-1)min(d,N/g)); repeated-half vectors provide a counterexample to the unqualified smaller bound.

Inherited Phase17 implementations reject some nonsingular zero-diagonal cases. A repair is included in the independent checks, but this does not imply the uploaded implementation was patched. NTT root planning, omitted arithmetic in source counters, input/output costs, resonance handling and numerical stability remain separately qualified. Finite-field experiments do not establish growing-precision bit bounds or stable complex runtime advantages.

The two newly supplied three-stage bit-reversal archives are byte-identical to the earlier source. Both upload identities are preserved; identical filenames alone were never used to decide equivalence.

## Coverage and continuation

This checkpoint integrates completed post-version15 review payloads and the eight direct uploads from22:57UTC, with their original identities and content hashes. It preserves the previous master and exact source/checker dependencies. Later Phase7, Phase19, Phase32, separation-rank and learned-rational source audits, and newer construction work, are tracked separately rather than silently treated as reviewed here. This is not a refreshed account-wide inventory.

Three construction and three review tracks continue. Next positive candidates must change the cycle geometry or endpoint routing, survive the known cuts, and satisfy the complete Fourier coefficient or Weyl equations with a seed and a uniformly charged parameter-generation rule. Passing a separator test alone is not a factorization.

Complete proofs, original source bytes, independently authored checkers, exact results and portability records are in the full checkpoint. Original uploaded programs were not executed. The compact findings attachment is a summary, not a standalone reproduction package.

## Historical version15

# Reviewed Fourier research checkpoint 15

9 October 2026 UTC. Fourteen frozen review/construction payloads extend checkpoint14. The user's three-construction/three-review research split continues separately. This checkpoint establishes no project-specific general exact sub-N-log-N FFT and makes no publication-priority claim.

## Positive result: exact F8 membership

The normalized 8-point complex Fourier matrix admits three separated-generator order-one quasiseparable stages with repeated bit reversal. A rational interval-contraction certificate proves membership of this specific target, rather than relying on a floating residual or generic dimension count. Independent verification rebuilds all64 selected Jacobian columns by exact finite differences and checks the target with integer sqrt2 bounds. Contraction<0.027855 and self-map radius<1.304e-11 inside a 2^-30 ball.

The exact coefficients are specified implicitly as the unique local polynomial-system root. This is a fixed-size existence theorem; it supplies neither closed-form constants nor a uniform coefficient-generation algorithm. See review_f8_certificate/INDEPENDENT_REVIEW.md.

## Structured-input algorithms that survive review

- Hero0 Phase8: for a fixed-order recurrence with fixed raw shift dictionary, learning and fully verifying the relation can give exact O(N) full output on the eligible family, with all roots/length assumptions stated. A time-varying Weyl-control variant gives O(N log log N). These families do not contain generic independent inputs. See review_orbits_phase8/PHASE8_REVIEW.md.
- Hero1 Phase17: inspect the residual of a fixed invertible sparse preconditioner. If its actual support has size K, the exact supplied-root arithmetic bound is O(N log(K+1)+K log^2(K+1)). Generic inputs have K=N; the ordinary FFT fallback remains. Root planning, missing operation-counter terms and finite-field diagonal exceptions are documented. A reverse-direction cyclic solve repairs the zero-diagonal exception in O(N). See review_hero1_phase17/PHASE17_AUDIT.md.
- Universal geometric-bank kernel preparation now has an O(N) raw-coordinate recurrence. Its dense application still costs O(N log N) in the verified schedule. Growing-radix expansion creates N b input-dependent entries; repeated coefficient tables alone do not remove this work. See review_orbits_iteration2 and review_orbits_iteration3.

## Sharper structural boundaries

1. The newly supplied repeated-bit-reversal proof excludes three full order-one quasiseparable stages for every dyadic N>=64. For N=32m it separates a rank13m Fourier block through12m+1 scalar wires. The source supplies the uniform construction; our independently authored graph checks and determinant controls verify it. This sharpens the prior N128 witness. It is restricted to that layout. See three_stage/approved_bitrev64_source_milestone/AUDIT.md.
2. Four repeated-bit-reversal order-one stages fail at N2048: a scalar cut676 contradicts Fourier rank683. This is a single-length exclusion, not a theorem about every four-stage permutation layout. See review_four_stage/NETWORK_REVIEW.md.
3. Two quasiseparable stages with one internal permutation satisfy N<=4(r1+r2)+1 under the stated Fourier endpoint ordering. Rank-one stages therefore fail for N>=10. At prime complex lengths arbitrary endpoints are covered by full-spark. The separate three-stage discrepancy obstruction also extends to arbitrary endpoint permutations at prime lengths. See review_two_green_v17/TWO_STAGE_BOUNDARY_EXTENSION.md and PRIME_ENDPOINT_COROLLARY.md.
4. FCUT proves a quadratic nonzero-count bound for a particular sparse sandwich: at prime p, nnz>=ceil(p*ceil(p/2)/2), including singular sparse factors and zero weights. Dense matrices can still have fast application algorithms, so this is not a quadratic arithmetic lower bound. See review_fcut/FCUT_AUDIT.md.
5. A routed rational Green-pencil row has coordinate-span dimension at most s q when its left support is s and the right stage is a q-term combination of fixed rational matrices. A primitive Fourier row requires dimension phi(N). This gives an all-dyadic-square N>=16 exclusion for the specified shifted two-term rational pencil. Over a degree-d number field the weaker necessary bound is phi(N)<=d s q. Arbitrary complex endpoint column masks and root-valued coefficient families are outside that simple argument. See review_routed_green_products/REVIEW.md.
6. The concrete non-affine fixed-pole N4 family is excluded on the entire equal-outer projective locus and on both one-infinite-outer loci, with all zero-middle branches accounted for. The finite unequal-outer regular locus remains under investigation. See review_nonaffine_green_parameters.
7. Phase30 exactly exhausts the fixed-outer four-term-middle window model at N4/8/16, including11,289,600 N16 mappings with full-rank cubic certificates. It closes the preceding N16 candidate locus for that model; it does not exclude arbitrary Green factorizations. See review_green_phase30/PHASE30_REVIEW.md.

## Gauge and accounting correction

Hero17 Phase5's cheap transition-mask/MST score depends strongly on basis gauge and is not an arithmetic complexity bound. Simultaneous Fourier-root gauge invertibility for shears a_j is equivalent to gcd(a_j-a_k,M) not dividing j-k for each pair. Affine shears a_j=cj+d satisfy it precisely when rad(M) divides c. Stable bases can still have high transition-mask rank; clustered geometric bases may be ill-conditioned. See review_orbits_phase5/PHASE5_REVIEW.md.

## What remains active

The three construction tracks now study richer routed phase-valued Green products, tunable non-affine Green parameters with size-uniform constraints, and changed four-stage layouts with symbolic cut/compatibility equations. Paired reviewers verify exact certificates and complete application/preparation ledgers. Unsealed ongoing results are excluded. The remaining goal is a correct growing-length construction whose entire charged cost beats N log N, not a collection of small fits.

## Evidence and reproducibility

Original new archives, provenance, independent proof reports, exact certificate data and identified independent checkers are preserved. Uploaded programs were not executed. Individual seals are retained; supplemental seals and dependency files are included so the directory layout is reproducible. Source-reported benchmark counts remain distinguished from independently rerun checks. Inspect each report for field, precision, endpoint and supplied-root assumptions before applying a theorem. No current account-wide completeness claim is made.

## Historical checkpoint14

# Current checkpoint version14

# Research synthesis after the three construction and three review split

9 October 2026 UTC. This checkpoint preserves six completed, independently cross-checked milestones, the new ranking text, and the seven attachments received at 21:59. Later construction iterations remain active and are outside this frozen checkpoint. No general arbitrary-input exact FFT breakthrough or publication-priority claim is established.

## Main mathematical result

For an exact factorization F_N = S3 P2 S2 P1 S1, with quasiseparable cut orders r3,r2,r1 and arbitrary internal permutations, cyclic-window localization and averaging imply

D(P2 inverse) <= 2r1+r2+r3,
D(P1) <= r1+r2+2r3,

where D is unnormalized permutation grid discrepancy. The classical planar discrepancy theorem then forces r1+r2+r3 = Omega(log N). Thus three fixed-order stages cannot give a growing-length Fourier family under these endpoint hypotheses. At least one Fourier endpoint must be natural or affine with coprime stride; the other may be arbitrary. This covers the full quasiseparable class, including zero generators and degenerate branches. It does not cover both arbitrary non-affine endpoints at composite lengths, four stages, or global matrices outside the stipulated cut-rank class.

Repeated bit reversal has the explicit stronger formula r1+r2+r3 >= ceil(log2(N)/2) at dyadic N. At N128, a43-by-43 Fourier block has rank43 while three order-one stages in that layout have rank at most42. The uploaded widths6 and8 missed this larger witness.

The rank-order bound is not an unrestricted scalar-operation lower bound. A high-order matrix could have another cheap representation. The imported discrepancy theorem is classical; priority of its application here remains unverified. Full proofs, independent controls and source attribution are in three_stage/ and review_three_stage/. A concise private note is at [private source omitted] .

## Exact positive controls and changed construction targets

The exceptional-Green track gives an exact characteristic-zero F4 identity using three dense, pairwise noncommuting mixers, each a weighted sum of two diagonally gauged cycle resolvents. All coefficients, nonzero denominator guards and both Weyl identities are explicit. This is a finite regression control in a tunable-outer family, not a scalable construction: the reciprocal two-pole dressing cannot extend beyond N4. Its general same-operator reciprocal mechanism needs the two term counts to sum to at least N. The source's stricter unweighted unit-diagonal denominator model is not silently identified with the weighted example.

The ranking's single sum of two weighted-cycle inverses is also asymptotically excluded by an existing separator argument, now checked against the actual denominator definition. Even independent cycle orders, zero edge weights and outside diagonal gauges obey m squared <=2N, m=ceil(floor(N/2)/2). This excludes N30,31 and every N>=34, including dyadic N>=64. Products of sums are outside that additive proof.

The active Green continuation changes a real hypothesis: non-affine cycle sums may have cut rank growing linearly while retaining O(N) application. The active scan continuation examines four stages and altered layouts. Neither direction is presumed feasible merely because a previous obstruction does not apply.

## Universal orbit recovery and its exact limits

For the square universal orbit basis, an explicit two-convolution geometric-Vandermonde inverse and a one-convolution forward map reduce the displayed N^(3/2) recovery/evaluation route to O(N log N) arithmetic and O(N) storage. Raw-input Fourier banks, root tables, a global batch inversion, all kernel transforms and outputs are charged. Suitable smooth convolution roots must be supplied or separately obtained; an arbitrary finite field with just an Nth root does not automatically satisfy this contract.

The full composition cancels the Vandermonde inverse and returns ordinary Cooley–Tukey. A sparse two-variable kernel recurrence is exact, but applying it to arbitrary input is not automatically linear. Nonzero shifted Hankel determinants rule out bounded stationary scalar recurrence compression of this particular kernel. The canonical complex orbit basis has condition number at least exp(Omega(sqrt(N) log N)); this is a sensitivity lower bound for those explicit coordinates, not a sufficient precision schedule or an algorithm-independent bit bound. See joint_orbit/ and review_orbits/PEER_REVIEW.md.

## New material with genuine restricted-input progress

Hero0 Phase7 recognizes unknown projective cyclic template classes directly from raw input, including exact zero patterns, and combines all factors before the small output transforms. On eligible lengths N=Km, m=Theta(log N), accepted rank/template parameter r gives O(N(r+log log N)) exact work with O(N) field words. It can handle dense inputs with all Green modes, full ordinary block rank and maximal Hankel rank. Generic inputs remain outside the finite union of restricted families. The shipped floating/field/root, missing-counter and unimplemented-fallback qualifications are recorded.

The Phase7-to-orbit coordinate map is proved exactly. One dense Phase7 template can require temporal orbit count growing as m/2, so the different compression models cannot be substituted for one another without a proof. The orbit gate's square sparse-edge lower bound is sharpened to every choice of shear/scale orbits, but only for explicit edge accumulation.

Hero1 Phase16 supplies the well-conditioned cyclewise operator L=7I+D+2P and the exact equivalence between evaluating LF and evaluating F up to linear work. Its shipped separate powers and sorting require corrected setup to attain linear preparation. Dense forcing alone is not a quadratic-work lower bound.

Phase29's fixed seeded two-coupling families are excluded over C at N4 and N8 by independently reconstructed full certificates. At N16 only a finite candidate-locus bound of131072 is established. Retuned outer families remain different problems. Displacement-v16's permutation minimum and uniqueness are valid with the supplied even-length parity repair; its state/transcript barriers retain their restricted models.

## Unchanged baseline and evidence

The strongest independently audited all-length positive result remains the conditional O(N log log N) additive approximation for fixed alpha<1/2 in its supplied-constant exact-complex/RAM model. The older coarse bounded-input Word-RAM O(N) approximation proof was already complete; ranking entry8 was stale. Neither is an exact arbitrary-input FFT or ordinary machine-precision guarantee.

All original bytes and source identities are retained in reviewer payloads. The two three-tap resends are byte-identical to the prior source, and the directly supplied orbit gate matches the separately discovered copy. No uploaded program was executed. Independently authored exact tests, analytic proofs, historical source logs and optional numerical diagnostics remain distinct. The research continues with three construction tracks and three paired review tracks; completed checkpoints do not signify that the broader search has finished.

## Preserved previous checkpoint

The following text retains its earlier date and scope.

# Current Fourier research checkpoint version 13

# Seven-upload synthesis: structured exact extensions and sharper gates

9 October 2026 UTC. This bounded update audits seven upload identities in four tracks against verified master version 12. The two polyphase-v15 uploads are byte-identical; the centered-v12 resend is byte-identical to an already audited master source. Thus the batch contains six distinct outer archive streams, five with new source bytes. No additional archive is included. Byte novelty is not mathematical novelty.

## Current result and exact target

The strongest independently audited all-length positive result in this collection remains unchanged: for fixed 0<alpha<1/2 and c>0, sufficiently large N and each fixed input independent of fresh randomness, O_(alpha,c)(N log log N) supplied-constant exact-complex/RAM work produces every output within C_alpha N^(-alpha)||x||_2, with failure at most N^(-c). The earlier bounded fair-bit sampling, coefficient, padding and output contracts remain essential. This is additive norm-scaled approximation, not exact recovery or a finite-precision certificate.

This batch adds exact fast paths for larger, explicitly restricted input families and sharper construction filters. These materials do not establish the project's arbitrary-fresh-input, explicit-all-output exact sub-N-log-N evaluator. This is a project-specific conclusion, not a claim that no exact improvement exists in any arithmetic model. The Phase28 report records an external exact-Fourier scope claim separately; its complete proof was not independently certified here.

## 1. Unknown shear, dense orbit unions and sparse Green innovations

Read `shear_trace/audit/AUDIT_REPORT.md` and `shear_trace/audit/CONFLUENT_FUSION.md`.

The three supplied mechanisms give sound exact full-DFT paths: a discovered shear/scale followed by Newton recognition; a fixed exact-g dense orbit union recovered through channel traces; and later sparse innovations under its Green recurrence. They inspect fresh raw input, discover the needed parameters and residual support, and validate every sample before acceptance. Their promised coverage requires the stated identifiable first-pair or clean nondegenerate 2g-row pilot. Exact-g is not automatically at-most-g; zero component spectra, repeated shifts or colliding channel eigenvalues can reject. A valid order-two Newton input explicitly demonstrates that a favorable representation need not satisfy the single-gauge pilot.

For fixed structural orders, balanced N=QM with Q²,M²=O(N), total event budget O(Q), and a supplied suitable prime field p=N^O(1), recognition, bounded rejection and all-output work are O(N). The complete ledger charges pilot transforms, Hankel/Vandermonde solves, scalar inversions, raw residual discovery, all failed attempts, tables and output writes. Growing g retains a 2^g N term; the printed structural counters are not exhaustive. The unchanged shipped dispatcher does not call the new branches.

The extension is genuine within the selected structured toolkit. A full-rank two-orbit N=64 witness defeats every one of 1,536 scalar/shift gauges at Newton orders 1, 2 and 3 under budget 8. Adding a sparse innovation gives a further exact witness. Independently, the confluent bridge joins repeated-pole Newton behavior and multiple shear orbits, recovering unknown multiplicities through a fixed-total-order composition search and full raw validation. With fixed total order D, a clean nondegenerate 2D-row pilot and the same balance/field/budget assumptions, its complete work remains O_D(N). This bridge is a proved design with dense reference checks, not a fast implementation added to the upload, and it does not include every dirty-pilot or early-innovation Newton case.

The universal g=M orbit basis still has a different, superlinear recovery/evaluation path; its displayed all-output formula has gN terms. Rank-one displacement is not ordinary rank one and does not supply a linear evaluator. Exact finite-field nonsingularity does not give numerical conditioning over C.

## 2. Sparse global phase support recognized from raw input

Read `sparse_phase/audit/PHASE6_SPARSE_SUPPORT_AUDIT.md`.

Phase6 adds a second exact structured path in a different block layout. For fixed factorization Q=KM, even Q, K>=M>=2, a fixed unit chirp slope and shift, and a suitable exact field/root, it discovers the common active phase set from raw input. Accepted support size r causes at most r full short-transform discoveries; rejection at cap R causes at most R+1. No input-dependent support advice is supplied for free.

Accepted work is O(Q+rQ+rK log K+(r+1)M log M), including root-table preparation from supplied roots, certificates, decoders, accumulation and all Q outputs. Rejection before decoding costs O(Q+RQ+(R+1)M log M). For M=Theta(log Q), this becomes O((r+1)Q), hence a restricted sub-Q-log-Q path whenever r=o(log Q). Storage is O(Q) field words. Field/root discovery, inversions, a growing chirp search and finding an eligible factorization retain their explicit costs; there is no new arbitrary-length theorem from free padding.

The class has Kr degrees of freedom and can have maximal ordinary Hankel rank even at one mode. Exact witnesses establish noninclusion in both directions with the prior rank-one common-chirp family. Nonetheless r<M gives a finite union of proper subspaces, and generic inputs remain outside it. The safe fusion with other exact paths is a fixed, fully charged dispatcher in compatible fields and lengths, with all prior rejection work paid.

Three source qualifications matter: the displayed counters omit at least r(Q-1) seed additions plus other setup costs; the executors reject rather than implementing the prose's FFT fallback; and the floating threshold can accept a nonzero full-support input as empty support, so it is not exact membership certification. The entropy obstruction is inherited and restricted to two-coordinate unitary gates. At r=M the complete-bank endpoint is the already known ordinary FFT.

## 3. Boundary-aware witnesses and Phase28 coupling exclusions

Read `multistage/research/MULTISTAGE_PHASE28_AUDIT.md` and `multistage/research/BOUNDARY_ANNIHILATOR_EXTENSION.md`.

The local annihilator and Casoratian arguments survive. An independent one-sided boundary refinement constructs a three-sparse Fourier mismatch already at N>=18, improving the uploaded constructive threshold N>=24. The inherited existential two-stage exclusion starts at N>=17 and remains stronger as a cutoff. The new result improves the explicit witness. At rank one, two boundary windows sharpen the three-stage necessary layout condition from k>=W-5 to k>=W-3. These require the stated quasiseparable coordinates and Fourier endpoint hypotheses; they are neither universal three-stage exclusions nor unrestricted arithmetic lower bounds.

Phase28's two-sided monomial invariants eliminate every choice of the two masks and permutations for fixed mixer candidates. For the specified N=4,8,16 networks, independently identified invariant polynomials, full Bezout checks, nonzero leading coefficients and valid cyclotomic reduction support the all-complex-coupling exclusions. The N=16 removed factor is justified in characteristic zero and only restores zero-entry cases incompatible with the target. N=32,64,128 have fixed-coupling vetoes only. Retuned outer mixers, different orders/gauges, multiple free parameters and untested lengths are not excluded.

Preparation and synthesis remain charged: source permutation validation and separate root powers need more than the stated linear apply work; dense inversions and coupling-polynomial synthesis are offline superlinear work. The noncanonical-residue API counterexample and inherited shorter-cycle helper limitation remain explicit. A cheap Green sum apply does not grant its inverse or an exact Fourier construction.

## 4. Polyphase v15 is an alternate inherited endpoint

Read `polyphase/audit/POLYPHASE_V15_AUDIT.md`.

The summary-demixing identity is correct, including signs, frequency routing and normalization. It eliminates the literal complete Green-scan bank, but the surviving circuit is ordinary mixed-radix Cooley–Tukey with O(Q log Q) work and O(Q) storage, already proved in the earlier exact bridge and Phase5 audit. The substantive new source is an alternative standalone implementation. The centered-v12 resend adds no new bytes or audit result.

The demixing algebra permits zero/nonunit slopes and K<M where the separate single-cycle Green helper does not. Unitarity requires the correct normalized coordinates and unit-modulus phases. The literal raw-input implementation still charges summary formation and all remaining short-transform banks. Its endpoint is not a lower bound on every conceivable output-only circuit. The inherited approximation, fair-bit sampler repair and finite-precision limitations are unchanged.

## Evidence and integration boundary

All four reports were approved after independent review. Seven original upload identities, exact outer bytes and inherited-source mappings are retained. Duplicate files needed by the portable sealed layouts remain present and are explicitly classified by hash; they are not counted as new research. Five independently authored checkers provide relocated reproduction. Exact finite controls, analytic proofs, numerical diagnostics and uploaded historical test claims remain distinct. No uploaded source program, test, helper or bytecode was executed, imported or compiled.

The current gain is a larger verified structured exact union, a constructive repeated-pole extension, corrected fresh-input work ledgers and stronger bounded filters. No publication novelty, practical speed superiority, bit-complexity improvement, complete floating-point certificate or general Fourier lower bound is established.

# Retained version 12 checkpoint

The prior text below is preserved unchanged. The new section above gives the bounded seven-upload update; prior statements retain their original scope and date.

# Current Fourier research checkpoint version 12

# Phase 5 joint-frame and Gaussian barrier update

This bounded update adds one 20:44 UTC source and two approved independent audit tracks after the delivered version-11 checkpoint. Start with `joint_frame/audit/PHASE5_JOINT_FRAME_AUDIT.md`; the separate probability review is `gaussian_barrier/GAUSSIAN_MEASUREMENT_BARRIER_AUDIT.md`. The source is preserved unchanged and was not executed.

## Current positive result remains unchanged

The strongest current all-length result remains the conditional randomized approximation already audited in version 11: for fixed 0<alpha<1/2 and c>0, sufficiently large N and each fixed input independent of fresh randomness, O_(alpha,c)(N log log N) exact supplied-constant RAM work produces all explicit outputs within C_alpha N^(-alpha)||x||_2, with failure at most N^(-c). Coefficient access, bounded fair-bit sampling, padding and output work retain their earlier contracts. It is additive norm-scaled approximation, not exact Fourier computation, a finite-precision implementation certificate, or a bit-complexity improvement.

The exact arbitrary-fresh-input, all-output sub-N-log-N Fourier target remains unmet. The structured exact results, fixed-factor compatibility gates and correlated-scan obstruction in earlier additions remain unchanged.

## Accepted Phase 5 content and corrections

1. **Complete-bank collapse is inherited.** Eliminating all separate Green scans reaches ordinary mixed-radix Cooley–Tukey, already proved in `additions/1717/astra_exact_bridge/EXACT_BRIDGES.md`. The supplied joint evaluator costs O(Q log Q), including its stated banks, and O(Q) storage. Creating and then undoing complete summaries is unnecessary if raw input is present. This is revalidation of an existing endpoint, not a new exact faster FFT or a publication-novelty claim.

2. **Normalization matters.** The displayed local transfer in normalized summary coordinates is unitary. The physical map from one raw input block to the selected M Fourier outputs instead has singular values 1/sqrt(K). For z=D/sqrt(M), the complete synthesis z→U_Qx is unitary. Rank-deficient spectral approximation therefore fails in those exact coordinates, without implying a general arithmetic lower bound. The algebraic identity needs Q=KM; Green helper and finite-field root conditions remain separate.

3. **Finite-population sampling improves constants.** With E_r=P_r/M mutually orthogonal and a uniform size-s subset S, Pbar_S=(M/s)E_S. Its mean-square error is (M-s)||x||²/s, and its exact fixed-subset operator error is max(1,M/s−1) for s<M, zero for s=M. Arbitrary fixed linear postprocessing preserves the full covariance reduction factor (M-s)/(s(M-1)) against population covariance. To inherit the earlier all-Q-beta Gaussian covariance certificate, independently sample the unit base slope and beta_0 uniformly modulo K; a fixed beta_0 is insufficient. Independently sampled groups support median amplification. Deterministic Gaussian truncation and rounding bias remain separately charged even at s=M. The deterministic Gaussian-remainder factor improves from M to M/s, while the phase-rounding bound is unchanged. Fixed s changes constants, not the accepted alpha<1/2 exponent or exactness.

4. **The Gaussian obstruction has precise information and probability scope.** Under input-independent measurement randomness, at most s<M linear observations per fixed occupied M-cell block, and no additional input information, posterior rank deficit d≥B(M-s), B≥floor(N/M)−2, yields the single-coordinate success bound min(1,4C²N^(2−2alpha)/d + exp[−(3−log 4)N]). The norm cutoff is an event inclusion, not conditioning a Gaussian on the norm event. A d-dimensional small-ball argument strengthens average success to exp(−Omega(N)) for fixed C, fixed alpha>1/2 and d≥cN/log N. It therefore refutes an every-fixed-input high-probability guarantee in that model. Transcript-only adaptive linear queries are covered only with the same pathwise deficit and no raw-input or other side channel. Rank deficiency alone is insufficient: random omission of one coordinate is a counterexample for 1/2<alpha<1. The alpha=1/2 boundary remains unresolved by this argument; the earlier alpha<1/2 approximation is unaffected.

5. **Determinant gates require the actual input basis and target.** For Q independent raw coordinates, explicitly producing the unnormalized recovered-input K-transform bank Z=Cx gives |det C|=K^(Q/2), hence at least (Q/2)log_2 K gates in the stated binary coefficient-bound-one linear model. Free unnormalized summaries D=Hx have |det H|=M^(Q/2); the remaining D→Z determinant is (K/M)^(Q/2). The different old per-phase bank W=RD has |det R|=K^(Q/2), with raw x→W determinant Q^(Q/2). These stages must not be conflated. For isometric N-to-Q padding, a rectangular Cauchy–Binet minor gives max(0,(N/2)log_2 K−(1/2)log_2 binomial(Q,N)) ≥ max(0,(N/2)log_2 K−Q/2), an Omega(N log K) obstruction for explicitly producing that intermediate when Q=Theta(N) and K grows. Nonunit Gaussian weights require their determinant factor. The normalized output-only map has determinant magnitude one. No unrestricted Fourier arithmetic lower bound follows.

## Evidence and remaining gate

Both independent reports were approved before integration. All sealed payload hashes and the preserved source archive pass verification. A relocated run of the independently authored checker reproduces the saved JSON exactly: 3,948 aggregate Fourier entries and 23,172 individual Green-scan entries over 15 small prime-field cases, 40 local transfers, and 29 exhaustive subset-size moment cases. Largest scaled numerical residual is about 1.58e-14. Exact finite-field tests require suitable roots and use unnormalized algebra; floating diagnostics do not certify all sizes or working precision. Uploaded programs and their saved tests remain source evidence only.

The next exact gate remains a concrete input-independent global output-only circuit with a Fourier identity and fully charged preparation, arithmetic, memory, exceptions and output work. A numerical claim also needs a complete precision contract. No broad search, practical speedup, unrestricted lower bound or novelty claim is established by this update.

# Retained version 11 checkpoint

The prior text below is preserved unchanged. The new section above gives the bounded Phase 5 update; all earlier scopes remain intact.

# Current Fourier research checkpoint version 11

# Roadmap and material synthesis

9 October 2026 UTC. This update reconciles the three roadmap tracks and the three new-material tracks, together with the HERO1 Phase14 and independent Gaussian cross-check. The exact arbitrary-fresh-input, all-output, fully charged sub-N-log-N Fourier target remains open. The outcomes are separate: an all-length randomized approximation in a supplied-constant RAM model; larger explicitly recognized structured exact families; and finite verifier, conditioning and obstruction improvements.

## Three roadmap tracks

### Reconciled direction map

The roadmap is preserved unchanged and reviewed against version 10. Its eight directions mix exact identities, restricted obstructions, structured-input algorithms and approximation theorems. Pure products of weighted-cycle Green resolvents still require at least ceil(log2 N) factors: non-affine cycle order does not remove inverse row-support growth. Sums, dense-inverse separated-generator scans and genuinely fused circuits require separate analysis. Exact phase-bank completion already has an ordinary Cooley–Tukey evaluator; completing the bank does not itself give a faster transform.

Read `roadmap/ROADMAP_REVIEW.md` and `roadmap/CLAIM_LEDGER.json`.

### Complete fixed-factor Weyl compatibility gate

For fixed invertible outside factors, complete diagonal Weyl-word fingerprints give a necessary and sufficient middle-monomial compatibility test after exact support/ratio checks and scalar calibration. The fingerprints are collision-free; an explicit counterfeit defeats the former six-word screen. The direct reference construction costs O(N^4) arithmetic and O(N^3) storage. This is a finite compatibility diagnostic, not coefficient synthesis, a Green factorization, or a faster Fourier evaluator.

Read `weyl_gate/WEYL_COMPILER_GATE.md`. Ten positive, ten negative and three collision controls pass over the stated finite field. The general proof is distinct from those finite controls.

### Correlated shared-scan obstruction

For the actual first Bessel forcing on the specified equal-block family, moving the output weight inside one fixed scan with the same diagonal extension requires repair rank at least max(0,K-1-(Q-N)). At N=Q-1 this is K-2, excluding bounded-rank repair as K grows. The arbitrary summary vector is realized by actual inputs in the stated one-local-channel setting.

The theorem permits fast structured high-rank repairs, different input weights and cancellation across all channels. It is neither an arithmetic lower bound nor a finite-precision result. Read `shared_channel/CORRELATED_SCAN_OBSTRUCTION.md`; the checks contain 198 exact determinants, 864 boundary-cycle checks and 396 correlated rank inequalities.

## Three material tracks

### Non-affine and twisted Green operators

Phase27's cycle-rank, all-affine gap, finite expansion and scoped gauge-recovery conclusions survive. Its `direct_green` helper needs a single-cycle restriction or a cyclewise formula: the supplied identity-permutation example computes the wrong resolvent. Four structural probes form a candidate; full validation remains necessary and may incur ordinary FFT work.

The twisted audit preserves the N>=10 asymmetric two-stage, N>=6 homogeneous two-stage and N>=15 homogeneous three-stage exclusions with their exact endpoint hypotheses. An independent construction replaces a generic coupling by the explicit integer lambda=m!(2*20^N)^m+2 for N=2m, avoiding all exceptional complementary-cut roots. Its representation takes Theta(N^2) bits. Positive coupling remains excluded from Fourier equivalence; cheap forward/transpose application does not grant a cheap inverse, and good whole-matrix conditioning does not certify every cut minor.

Read `nonaffine_twisted/audit/NONAFFINE_TWISTED_AUDIT.md`. Both unchanged uploaded outer archives are preserved. Redundant extracted copies of already preserved predecessor ZIPs are omitted with exact mappings; their bytes still remain inside the original archives.

### Rough lengths and the all-length approximation theorem

The v14 unequal-block executor, overlap covariance and HERO0 weighted rough-modulus Green identity are supported in their declared arithmetic models. The general shipped v14 storage is O(N+B^2); its median-count helper has an explicit overflow/nontermination certificate in the affected parameter range. Source benchmark claims are not independent reruns.

The two complementary audits support the following conditional all-length result: for each fixed 0<alpha<1/2 and c>0, sufficiently large N, and each fixed input independent of fresh random states, all Fourier bins can be explicitly approximated within C_alpha N^(-alpha)||x||_2 with failure at most N^(-c), using O_(alpha,c)(N loglog N) ideal arithmetic/RAM work and O_(alpha,c)(N) memory. The model supplies exact length-dependent exponential/root bases, supports exact complex arithmetic and bounded-word integer/RAM work, and uses the stated bounded fair-bit sampling repair. It is not one random map certified for every input simultaneously.

The independent Gaussian review charges rough padding, Gaussian truncation, midpoint rounding, all short convolutions, coefficient generation from supplied bases and output writes. The elementary rough-modulus estimate improves the variance to O(log N/N). Choosing h>(1+c)/(1-2alpha) in 2h-1 independent repetitions absorbs the polynomial failure budget. The source's fixed seed and a cap on high-level sampler calls alone do not establish this randomness/work contract.

Read `rough_length/audit/ROUGH_LENGTH_AND_COPRIME_GREEN_AUDIT.md` and `gaussian_crosscheck/GAUSSIAN_ALL_LENGTH_AUDIT.md`. These do not establish exact Fourier recovery, finite-precision correctness, bit complexity, practical speed superiority or publication novelty. The tolerance is additive on the total input norm, rather than relative accuracy for each Fourier bin.

### Delta and Newton structured exact union

The selected-factor, fixed-order Newton theorem recognizes raw inputs whose globally budgeted spectral differences satisfy its guard, and returns every exact finite-field Fourier output on acceptance. Dense initial fibers are allowed. Balanced dimensions, fixed order and O(Q) event budget give linear work, with explicit field/root, inversion, recognition and output charges. Rejection denotes nonmembership in the selected structured union.

The optional-reset recognizer has a concrete N=16 greedy-coverage counterexample. A complete replacement keeps the largest B-1 transition costs as resets; all unsuccessful recognition work remains charged. This repair is a proved design, not a source patch. The default divisor restriction remains, and the unchanged shipped `fused_fft.py` never calls Delta/Newton.

For cyclic convolution, an independent union of output-state, output-rank and fixed-order output-variation guards strictly expands the accepted reconstruction family. Explicit actual sparse-input graph families separate rank and first variation in both directions. The raw Newton theorem pays dM^2 for arbitrary dense anchors. Graph output reconstruction instead pays dMH using the inherited active-column bound, so the extra M^2=O(N) guard is unnecessary there; the Q^2/input-mode constraints stay in force. These are different APIs and cannot be interchanged.

Read `delta_newton/audit/AUDIT_REPORT.md` and `delta_newton/audit/EXTENSIONS_AND_FUSION.md`. The exact tensor/fiber resend remains a distinct upload identity with unchanged source bytes and inherited prior findings. Neither the structured union nor its growing-budget corollary gives arbitrary-input exact Fourier recovery.

## HERO1 Phase14 and the shared exact-bank gate

This HERO1 Phase14 is distinct from the older master `phase14/` package. Its exact projection, energy, Gram-union and stationary Toeplitz identities survive. The stationary q=M frame gives an exact arbitrary-input factorization, but its evaluator retains FFT-scale work. Bounded q transforms a proper subspace and supplies an exact-arithmetic full-vector residual identity outside it. A fixed proper orthogonal projector has worst-case relative full-vector error exactly one.

The independent stationary-frame perturbation bound provides uniform conditioning when K is sufficiently large relative to M, including bounded conditioning at q=M and K>=4M. It is a local exact-frame statement, not a complete floating-point scan guarantee. Removing only the M long scans leaves coefficient formation and the bank of short FFTs to be charged. The antiperiodic scan proof assumes G>=2; G=1 uses the direct odd-transform fallback.

Read `hero1_phase14/HERO1_PHASE14_AUDIT.md` and `hero1_phase14/PORTABLE_REPRODUCTION.md`. The complete 9,352,867-byte source ZIP is unchanged. Its 32 genuinely byte-new top-level contents are copied separately; all nested mathematical predecessors are inherited by hash. Two additional new archive-stream/checksum contents are packaging changes, not new mathematics.

## Combined interpretation

The update supports three separate outcomes:

1. An all-length randomized approximate transform with O_(alpha,c)(N loglog N) supplied-constant RAM work, additive input-norm-scaled error, independent fresh randomness and explicit sampling qualifications.
2. Larger selected structured exact Fourier and convolution families, including Newton differences and complementary graph rank/variation guards with fully charged recognition.
3. Finite compatibility diagnostics, conditioning refinements and restricted obstructions that sharpen tests for still-unconstructed exact candidates.

The version-10 roadmap review keeps its original cutoff. Its status statements are historical evidence; the approved current statuses are the synthesis above. A restricted no-go theorem must not become a general arithmetic lower bound, and a finite certificate or a fast operator with large cut ranks does not become a Fourier construction. No exact arbitrary-fresh-input all-output asymptotic improvement, practical measured speedup, finite-precision implementation certificate, general integer-multiplication result or publication-priority conclusion is claimed.

## Integrity and evidence boundaries

Eight source request identities are recorded in `source_records.json`: one roadmap note and seven archive requests, of which one archive is an exact resend. Six archive streams carry new source bytes. The three roadmap components and three material tracks are all completed, with the Phase14 audit and independent Gaussian review included. The inherited 349-item Library snapshot and its earlier unread/account-coverage limits are unchanged.

All original outer files are retained with exact hashes. Uploaded source code, tests and bytecode remain data and were not executed, imported or compiled. Only independently authored checkers were rerun; exact finite checks, floating diagnostics, analytic proofs and source-recorded historical tests are labeled separately. Original worker seals remain unchanged and describe their original workspace layouts. The active integrated manifest covers the delivered layout, while `SOURCE_SEAL_VERIFICATION.json` and copy mappings record all intentional layout differences.

# Retained version 10 checkpoint

The prior text below is preserved unchanged. The new synthesis above supplies current statuses for this bounded batch.

# Current Fourier research checkpoint: version 10

# Six-source synthesis: 19:54 UTC, 9 October 2026

All six attachment identities are resolved. Four are byte-identical to existing master originals and retain their completed mathematical corrections; two contain new bytes and now have three completed independent audits. The source triage remains an unchanged historical/static snapshot; the final audits below supersede its pending review questions. Original source programs were never imported, executed or compiled.

The positive result is a larger set of explicitly recognized structured exact transforms and convolutions. The negative implementation finding is a false approximate-dispatcher certificate. Neither yields a general exact faster Fourier transform or a novelty certification.

## HERO17 raw-input recognition: exact on selected structures

For supplied certified prime-field/root data, bounded-rank balanced CRT tensors and bounded-mode strided fibers are deterministically recognized and produce every Fourier output with the charged bounds. The standalone tensor and fiber branches admit uniform O((1+r)N) arithmetic under their balance guards, with explicit scalar-inversion costs and O(N) space; r=o(log N) therefore gives sub-N-log-N arithmetic on those accepted structured families. Support-coset reduction and fixed-r common-chirp recognition remain valid.

The default dispatcher selects a single fiber divisor and CRT split. It misses an explicit N=12 input that passes an eligible alternate Q=2 fiber test but fails its default Q=3 and other branches. This is incomplete fast-path coverage, not an incorrect accepted output. Its shipped common-chirp engine also retains a factorial eliminant, so the whole shipped callable does not inherit the standalone growing-rank ledger.

A separate, specified dispatcher with independent tensor/fiber/chirp budgets and the earlier polynomial Toeplitz construction has ledger O(N(1+r_T+r_F+r_C^4)+r_C^(2+3 log_2 3)); it is an independently proved design, not implemented source functionality. Another independent corollary recognizes every integer-polynomial phase at N=d s^2 with the specified Q=s in O_d(N) for fixed d, irrespective of polynomial degree. More generally, each fiber has at most L=N/gcd(N,Q^2) modes. The default divisor must not be assumed to choose this split.

The independent controls include 118,617 exhaustive row-membership vectors, 591 raw fiber cases, 1,341 all-phase chirp cases, 820 Gauss rows, 160 bounded-square-multiplier polynomial examples and the selected-divisor counterexample. See `additions/1954/tensor_audit/AUDIT_REPORT.md`, `additions/1954/tensor_audit/EXTENSION_AND_FUSION.md` and its bounded primary-source context.

## Graph-union convolution: accepted guard and a broader exact rank fallback

For validated length-M sparse Fourier fibers, the matched-label formula has the correct negative carry phase and factor M. With fixed input-mode bounds, N=QM, Q^2=O(N), and the post-cancellation state guard S<=CQ, it materializes every convolution output in O(N) exact-field work. Cancellation/revival bookkeeping can have E events rather than S, so the edge/event charge remains explicit. Public certificate-only functions trust their inputs; the raw-input wrapper is the validation boundary.

An independent sharp bound is S<=min(N,E,sqrt(Q Kx Ky)), where Kx and Ky count input modes. A separate fallback accepts fixed rank d of the merged coefficient matrix. Its active-column count H<=min(Kx,Ky,M) makes both dQH and dMH linear under the stated fixed-parameter contract; no M^2=O(N) condition is needed. An explicit family with one mode per x fiber and at most two per y fiber has S/Q tending to infinity but output rank one, so the fallback strictly extends every fixed state-budget rule. This is a distinct family from the maximal-input-rank example and is not functionality attributed to the uploaded source.

The independent suite reproduces 7,062 complete convolution pairs, 38,171 output bins, 18 full-input-rank controls, four tight state-growth constructions and seven rank-one escape families, including unbalanced lengths. It is a restricted exact convolution improvement, not an arbitrary-input FFT or integer-multiplication result. See `additions/1954/graph_audit/GRAPH_UNION_AUDIT_AND_RANK_FUSION.md`.

## Divisor-spectrum v13: inherited approximation bound, an exact certificate failure, and a spectral refinement

The direct composite covariance and least-prime approximation theorem are valid for fixed inputs and ideal arithmetic. The displayed divisor bound was already proved in the earlier master, and the previous mask-count bound is strictly stronger. The semiprime specialization must separate distinct primes from prime squares: at N=p^2 and M=p the divisor bound is 2/p and the older bound is 1/p. The balanced-semiprime approximation exponent survives, but is inherited.

The uploaded adaptive planner's generic execution certificate is false. Its offset/Bessel execution uses quantized three-grid aggregation while its guarantee is for coordinate medians. An exact N=3 example fails with probability one at the requested tolerance even though the planner advertises failure below 0.00008. Bessel execution also omits a deterministic addition-error budget and can execute a different M from the certified M. These are exact/static certification defects, not merely an absence of benchmark evidence. The direct-composite theorem remains valid; the adaptive planner must stay explicitly uncertified.

A separate new spectral reduction resolves the least-prime case. For p the least prime divisor, W_p[u,v]=p-1-|u-v|. If p^2 divides N, the covariance satisfies Q_cov^2=((p-1)/phi(N))Q_cov and has exact norm (p-1)/phi(N). Otherwise its norm is [(p-1)-lambda_min(W_p)/p]/phi(N), with the explicit rational bound [(p-1)-1/(2p)]/phi(N). This refines constants and the structural description, not the asymptotic frontier. The complete planner-setup argument is N^(1/2+o(1)) word arithmetic, although the source's numerical work proxy is not a complete charge and its other certification defects remain.

Independent checks include 9,275 exact admissible-pair comparisons, 32,895 Ramanujan identities, exact rational spectral controls and the exact aggregation counterexample. The general proof is separate from finite checks and floating spectral diagnostics. See `additions/1954/divisor_audit/DIVISOR_SPECTRUM_AUDIT.md`.

## Four resends retain prior corrections

- Sparse-defect: `additions/1930_sparse/` retains the arbitrary-row-sparse escape repair, charged Woodbury setup and pivot/bit qualifications.
- Phase26: `additions/1930_phase26/` retains the factor-two crossing improvement, strict integer witness and restricted-architecture scope.
- Mixed-radix v13: `additions/1930_v13/` retains the source phase-test mismatch, bounded randomness/conditioning refinements, and earlier exact-bank/Cooley–Tukey identity.
- Composite HERO0: `additions/1916/` retains the stronger prior covariance, fixed-input approximation, scaled-projector identity and sampling contract.

Those are paths in the master, not new copies of original archives. `additions/1954/source_records.json` maps each new upload identity to its exact preserved original.

## Interpretation and stopping point

All three new audits, static triage and six-source request mappings are complete. The false planner certificate is a documented source defect; this update does not claim to repair or execute that planner. A general exact arbitrary-fresh-input, all-output, fully charged asymptotic Fourier improvement remains unestablished. Bit complexity, stable floating-point recognition, optimized practical speed, unrestricted convolution/integer multiplication and publication novelty do not follow. Baseline unread-source and account-coverage limits remain unchanged.

# Retained version-9 checkpoint

The following historical checkpoint is preserved unchanged. Its six-source pending status is superseded by the completed update above.

# Current Fourier research checkpoint

9 October 2026. The five direct sources received at 19:06–19:10 are now independently audited and integrated: bounded common-chirp recognition, centered v12, multistage bit reversal, Phase25 and offset-class v12. They provide scoped exact algorithms, approximation refinements, explicit implementation corrections and restricted representation certificates. No new exact arbitrary-fresh-input, all-output sub-N-log-N evaluator has been established.

## Exact bounded common-chirp recognition and polynomial-cost phase certificate

For fixed r>=1, N>=3r and a supplied prime field containing a certified primitive Nth root omega, the recognizer accepts exactly vectors

`x[j]=omega^(a*j^2) sum_(ell=1)^s c_ell omega^(b_ell*j)`, with 0<=s<=r,

distinct active frequencies and nonzero active coefficients. The zero vector is handled as the empty representation. Recognition and all accepted transform outputs cost O_r(N) exact field arithmetic under the stated field/root contract; rejection means only nonmembership in this structured family.

The phase eliminant has degree at most D=binom(r+2,3), not necessarily exactly D. Its normalized matrix is polynomial Toeplitz with nonzero constant leading minors. This replaces factorial expansion with independently verified polynomial-cost constructions: exact Bareiss O(r^9), or truncated-series nonsymmetric Levinson with Karatsuba/Newton arithmetic O(r^(2+3 log2(3))) and one scalar inversion. No p>D assumption or division by an integer index is needed. With L=N/gcd(2,N) and C=min(D,L), charged candidate processing gives `O(T(r)+S(N,r)+C(Nr+r^3)+N)`, where `S=O(min(L(D+1),D+L^log2(3)))`. Growing-r setup, verification and storage do not disappear; this is not a general linear-time FFT.

The original independent audit classified 118,617 finite-field vectors with no false decisions in those tested spaces. The extension includes 210 coefficient comparisons, 388 scalar determinant comparisons, 123 Toeplitz/Bareiss comparisons through rank 16 and explicit p<D examples. These controls support the included general proofs. The original note and audit are unchanged. See `additions/1906_chirp/`.

The [delivered private theorem note]([private source omitted]) summarizes this result. Novelty is unconfirmed: prior-art review is focused and incomplete, and the common-chirp model and determinant/Toeplitz ingredients are classical.

## Centered v12: approximation certificate and constructive precision repair

Centering the active interval halves the largest Bessel argument. An independent sharper envelope on 0<=z<=pi/2 is `sum_(r in Z)|J_r(z)| = 1+integral_0^z J_0(t)dt < 2.278`, replacing the source's 4.25 fusion factor. Centering each occupied block at its own midpoint additionally halves the local argument, with one table for full blocks and at most one for the final partial block. At the recorded N=511, target 10^-8 proxy, the specified refinement permits H=3 instead of H=4 at R=11. This is a certified parameter/proxy improvement, not an independently measured runtime speedup.

Balanced product-tree depth does not imply logarithmic forward error: a k-leaf product still accumulates k-1 multiplication errors, and root reuse can also accumulate O(ku) error. A constructive repair reanchors every Theta(p/log p) positions, prepares bounded-angle Taylor anchors/roots with charged pi setup, and uses p+O(log p) bits to obtain uniform absolute carrier error 2^-p in O(N+p) arithmetic. A conditional summary-interface ledger and charged Bessel-series construction preserve the earlier sufficient leading mantissa order, with guard bits. They certify a specified replacement design, not the uploaded NumPy/SciPy implementation.

Centering does not stabilize the forward Bessel order recurrence. At the supplied N=511 example one mode already requires over 95 additional seed-accuracy bits by the lower amplification bound. All R short transforms and decoder passes remain charged; the shrinking-error arithmetic order and exact-summary rank barrier remain unchanged. See `additions/1906_centered/` for separate identity and precision reports.

## Multistage bit reversal: exact finite-size geometry, not Fourier synthesis

For t separated-generator stages with fixed intervening permutations, the all-size complex image-dimension bound is `min(N^2,N+t(4N-6))`. It follows from the 5N-6 dimensional stage family and the free (t-1)N-dimensional diagonal boundary gauge action. Generic matrix coverage requires at least `ceil((N^2-N)/(4N-6))` stages; this does not prove a Fourier lower bound.

All 34 saved modular Jacobian ranks and six full-row minors were independently reproduced. Nonzero integer-polynomial minors prove the corresponding complex dimensions for N=8,16,32. Gauge directions exhaust the kernel at every saved subthreshold depth. Appending identity stages extends full dimension to every larger depth for those same sizes. No all-N saturation theorem or representation of the specific Fourier matrix is established; the demonstrated fully charged generic executor is quadratic at its threshold family.

See `additions/1908/`. The 548,427-byte original source archive, absent from the standalone audit ZIP, is now preserved there unchanged. All original audit files remain byte-identical except the package manifest, whose approved original is retained separately.

## Phase25: correct affine-run identities and a complete exact frontier solver

The supplied affine-run geometric DFT identity handles z=0 and resonant ratios, with charged O(rN+r log N) field work for supplied structure/root data. The two-run dyadic cycle and twisted four-track cut-rank certificates are valid in their stated models, including the hidden rank-five cut and its approximation floor.

Two individually admissible cyclic resolvents may have a singular sum: the additional determinant `det(2I-alpha W-beta Z)` must be nonzero. The uploaded band-LU/Woodbury schedule also misses cases with zero unpivoted pivots or a singular band base, even when the full target is invertible. Exact counterexamples are retained.

An independently authored whole-matrix row-pivoted frontier solver covers every nonsingular admissible instance of this fixed-width family in O(N) exact field setup, application and storage, detecting singularity without the band-base assumptions. For complex |alpha|,|beta|<1 the sum is nonsingular with the strengthened condition estimate in the report; this does not prove floating-point backward stability. Exact controls include 21,714 stride cases, 1,846 direct affine-transform comparisons, 289 small-field parameter pairs and larger inverse checks through N=16,384. See `additions/1909/`.

## Offset-class v12: unbiased approximation with an accuracy-dependent row count

Under explicit half-up nearest-grid rounding, there are exactly L=N/gcd(N,Q) offset classes, namely congruence classes of target indices modulo L. A deterministic linear-time class plan avoids redundant sorted-uniqueness validation in the source. In the legal prime-power regime M^2<=Q, the ideal row is unbiased with per-output variance at most `(M/N)||x||_2^2`. A fresh row costs `O(L[Q+K log K])`; fixed-cofactor input lengths admit O(N) arithmetic rows with M=Theta(log Q). Exact-center means exact expectation, not exact realized transform outputs.

Accuracy and failure must be specified together. Near the variance scale with constant g, the stated all-output guarantee uses Theta(log(N/delta)) rows. At any fixed weaker power accuracy N^-alpha with alpha<1/2, a suitable constant number of rows instead suffices for polynomially high success probability on fixed-cofactor lengths. This positive regime is preserved without presenting it as an exact FFT or an unrestricted all-length result.

The scan-state rank certificate needs distinct post-cut future queries and a linear-state/no-reread model; its bound is min(R,L_after), not a general Omega(RN) time theorem. Exact-grid edge handling, N=1 identity behavior, modular integer range, modulation error, roots/FFT contracts and robust numerical aggregation remain explicit qualifications.

The claimed missing v11 core is not missing from the exact predecessor archive in this chain: the core and reference are byte-identical to preserved earlier sources. A separate conversation admits a failure of some export, which does not identify that export with this archive. See `additions/1910/` for the exact artifact comparison, independent covariance proof, conditional precision transfer and retained original archives.

## Derived slowly growing-rank fast path

The approved polynomial ledger directly gives `O(Nr^4+r^(2+3 log2(3)))` field additions/multiplications, O(N+r^4) storage and O(r^4) cached scalar field inversions. Thus `r=o((log N)^(1/4))` permits `o(N log N)` recognition and accepted full-output transforms within the same common-quadratic-chirp family. This is a genuine relaxation beyond fixed r, not arbitrary-input Fourier recovery. The separate derivation, root/field contract, inversion accounting and fallback qualification are in `GROWING_RANK_CHIRP_COROLLARY.md`; it is not an alteration of the sealed original supplement, a numerical-stability claim or a novelty verdict.

## Newly discovered Library sources: static review only

Four additional generated archives are preserved unchanged in `additions/1930_static/`, separately from direct uploads. Twenty-five Python files parse and all four manifests/72 original member hashes verify; original programs were not imported, executed or compiled. HERO17's newly available code accompanies a note byte-identical to the already audited chirp note and does not include the later independent polynomial-cost extension. Its historical tests remain historical.

Phase26, the sparse-defect gate and mixed-radix v13 now also have completed independent mathematical reviews, summarized below. Initial static observations remain separately labeled and do not replace those proofs. In particular, the M-bank identity is inherited from the prior 17:17 checkpoint rather than a new discovery. Filenames dated October 10 are retained alongside October 9 Library creation context. Composite HERO2 is now independently audited and integrated as described below.

## Completed composite and late Library mathematical reviews

All four reviews that were awaiting incorporation are now approved and included; the bounded batch has no pending deep review. These independent reports supplement the preserved original/static evidence, without converting source-recorded tests into independent test runs.

### Composite HERO0 phase 2

The composite cycle executor and randomized approximate contract are valid for the stated factorizable lengths. Its physical map is a scaled orthogonal projection P with P^2=MP, not an idempotent projection. The uploaded covariance coefficient M(M-1)/phi(N) is weaker than the previously accepted composite certificate, which remains the primary bound. The fixed-row binomial tail also consolidates an earlier v9 result. Capped candidate counts do not automatically bound random-bit rejection work, and the offset fallback retains sampling/sorting costs needing explicit repair. This is useful restricted-length approximate implementation work, not a new exact or all-length advance. Original archive, all 24 source files, prior comparison evidence and independent checks are retained in `additions/1916/`.

### Sparse-defect inverse-stage theorem and a repaired escape example

For an arbitrary row-q-sparse baseline B, the Fourier rank defect satisfies `rank(F_N-B)>=floor(N/(q+1))`, robust under endpoint monomials. Telescoping gives the stated sparse-plus-low-rank inverse-stage product restriction, including singular sparse baselines. The uploaded bandwidth-only witness proof did not establish its broader arbitrary-row-sparsity claim.

The independent repair closes that specific gap: for the separated scan S with lower/diagonal/upper entries 1/3/2 and every row-q-sparse B,

`rank(S^-1-B)>=ceil(floor(N/(q+2))/(2q+1))`.

The proof uses interleaved nonsingular minors and a bounded-degree support graph, covers every support pattern and coefficient choice, and survives arbitrary endpoint monomials. At fixed q the defect is linear in N. Both S and its inverse have linear exact-scalar application, demonstrating a genuine separation of restricted operator classes, not a Fourier factorization. Explicit rational outputs can still require Theta(N^2) bits. Woodbury setup is `O(N+Nr^2+r^3)`, with fresh application `O(N+Nr+r^2)`; no-pivot Thomas code covers only a smaller chart. See `additions/1930_sparse/`.

### Mixed-radix v13

The independently checked physical one-row operator is exactly F_N P with the intended interleaved scaled projector. Unbiasedness, per-output covariance, rank and fixed-state/global error formulas hold under the stated randomness contract. The source's finite-field completed-bank checker reverses a one-row phase convention; averaging conceals that mismatch. The independent checker verifies the recurrence before bank averaging and closes this test-coverage gap.

Full column-state independence is sufficient but not necessary: a shared random slope with conditionally pairwise-independent beta phases preserves the covariance and reduces seed requirements. The normalized stacked complete bank is perfectly conditioned, and a common downstream twiddle perturbation loses the single-row M amplification under exact bank averaging. These are bounded improvements; they do not remove the scan/FFT work or give a complete numerical certificate.

Exact beta-bank completion and its ordinary Cooley–Tukey collapse were already established at 17:17. They are not new v13 discoveries. The independent suite checks 211,344 recurrence/composition entries and 19 exact covariance-projector cases, alongside the inherited completed-bank controls. See `additions/1930_v13/`.

### Phase26 simultaneous common-character cuts

For dyadic N and the specified products of sums of weighted Hamiltonian-cycle Green inverses, with bounded affine step magnitudes, exceptional edges, diagonal gates and affine interstage permutations, the common-character theorem is valid. A sharper Hamiltonian crossing budget halves the previous signed-edge allowance:

`rank <= min(N/2, T floor((N-1)/r)+sum_q floor(b_q/2))`, with `r=floor((N-1)^(1/s))`.

For bounded steps and bridges per term, exact Fourier representation still requires `Q=Omega(log N/log log N)` term occurrences; the same obstruction holds at fixed operator error below 1/sqrt(2). This is a restricted representation result, not an unrestricted circuit-time lower bound or a theorem for arbitrary internal non-affine permutations. The source's floating witness search can accept equality where strictness is required; an independent integer pigeonhole routine enforces `r*abs(t)<N`. The strengthened finite thresholds 7,12,21,36 are necessary-only certificates, not factorization constructions. Earlier Phase25 nonsingularity and pivot corrections remain in force. See `additions/1930_phase26/`.

All nine new mathematical audits in this bounded update are complete, alongside the distinct static/source-availability review. No new arbitrary-input exact faster Fourier transform, universal FFT lower bound, or integer-multiplication complexity improvement has been established by this project batch.

## Consolidated interpretation

The chirp and Phase25 developments are concrete restricted exact algorithms. Centered and offset-class v12 concern randomized approximation with distinct bias/variance/precision guarantees. Bit-reversal Jacobian dominance is a representation result for generic matrices at specified sizes. These statements cannot be merged into an arbitrary-input faster exact Fourier evaluator. Earlier complete F8 exception accounting, endpoint restrictions, parity/Gram statements, summary-rank bounds and charged setup requirements remain in force.

Completion of this bounded batch and its separately classified static source inventory are recorded in `PENDING_ADDITIONS.json` and `ADDITIONS_STATUS.json`. Static code/lineage review does not promote source-recorded tests or new mathematical claims to independently checked results. Baseline unread-source and account-coverage limits remain unchanged.

# Retained version 8 checkpoint

The five 19:06–19:10 sources listed as pending in the historical text below are completed above. Other new-source statuses are governed by the current pending inventory.


9 October 2026. All explicitly tracked later sources through the 18:48 UTC upload are now independently audited and integrated. This includes the 18:45 Phase24/window pair, 18:47 HERO0 note and 18:48 endpoint-rank archive. The separately discovered Phase23/window sources remain distinguished from direct uploads. No new exact arbitrary-fresh-input, all-output sub-N-log-N evaluator has been established.

## Phase24: sorting correction and a complete restricted evaluator

The stable-binary-sorting shift defect has exact rank `r=2 floor(T/2)`, with T the noncyclic transition count. Over iid fair binary inputs its exact law is `Pr(r=2k)=binom(N,2k+1)/2^(N-1)`, with mean N/2-1 and variance N/4 for N>=3. A fixed rank cap covers only polynomially many binary inputs. An explicit simultaneous bound over every nonzero cyclic stride, including noncoprime ones, gives rank at least N/8 with probability tending to one. These are restrictions on this cyclic-reference correction architecture, not general FFT lower bounds.

The nearby-order Woodbury identity is valid away from the root locus, with small correction determinant exactly one. The source needs two corrections: no nontrivial defect cycle exists at T<=1, so s=r+1 applies only at T>=2; and its s=0 implementation repeats z^N at every output, adding avoidable N log N work unless the shared factor is hoisted.

An independent sparse twisted-difference executor computes all outputs of a supplied and verified near-order geometric input in O(N(s+1)) field arithmetic and O(N) storage, where s counts changed successor edges. It handles every z, including the root locus, with at most one singular output evaluated directly. Input-family checks, permutation validation, roots/normalization, inversions, bits and complex conditioning remain charged. It is an improved special-input method, not a new arbitrary-input transform.

Reports and portable evidence: `additions/1845/`. Its source pair has 736 recursive occurrences, 550 distinct contents, 13 byte-new contents against the declared predecessor union, and 873 passing embedded checksums. The accompanying window archive is byte-identical to the already audited 18:25/18:28 source.

## HERO0: operator bridge, precision obstruction and conditional scan improvement

The Bessel/operator recurrence, inverse identity and Cauchy-minor representation obstruction are correct in their stated models. The straightforward forward cycle amplifies an initial b=1 Fourier-mode error by at least `(R-1)! (K/pi)^(R-1)` after R orders for K>=4. Thus a hypothetical cheap H application alone does not supply the required numerical stability or preserve the previous leading precision budget.

The selected-output prefix-scan commutator already has a full-rank minor for degree-one output weights. A constant-rank correction cannot move those weights inside one common scan on unrestricted forcings. The actual channel forcings are correlated, so this does not exclude a specialized joint evaluator, and full rank is not a multiplication-cost lower bound.

A bounded exact-field construction evaluates the polynomial scan subproblem in

`O(Q(R/B+B) log^2(M+R))`

operations with O(Q) storage, given monomial coefficients, `1<=B<=R<=M`, `B|K`, `Q=KM` and `M^2<=Q`. Taking an admissible B comparable to sqrt(R) gives `O(Q sqrt(R) log^2(M+R))`; use its minimum with the ordinary O(QR) scan. An asymptotic saving requires `log^4(M+R)=o(R)`. Root/forcing preparation, generic multipoint node setup and output materialization are charged. For the Bessel/Chebyshev branch, a conservative O(KR^2) coefficient conversion is additionally charged; it is not hidden as free preparation.

This is a **conditional scan-only arithmetic improvement**. The R independent K-point Fourier channel transforms still cost O(RK log K)=O(RN), leaving the current total O(RN). Exact Bessel generation is unspecified; a finite-precision/bit-complexity certificate and a practical optimized implementation for the blocked method remain absent. The older scan precision contract cannot automatically certify the new conversion and product/remainder-tree operations. No overall speedup or stability improvement is claimed.

The corrected offset statement uses the residue -Nj, equivalently -Nat for j=a*t mod Q. The checker already used that expression. See `additions/1847/independent_bridge/BRIDGE_AUDIT_AND_CONSTRUCTION.md`. The original note is preserved as a complete 143-line Library text extraction matching the reported 11,664-byte size; its hash is explicitly an extraction hash, not a separately downloaded raw-blob hash.

## Optimal endpoint rank: a one-matrix result with clear product limits

Over C, for dyadic N>=8, the exact minimum quasiseparable rank of Fourier over arbitrary independent input/output permutations is N/4+1. Double bit reversal attains it. Its cut-rank recurrence and parity-dependent total-rank formula are correct, with asymptotically optimal leading total N^2/6.

The independent odd-cut refinement gives lower bounds `ceil(k(N-k)(N+1)/N^2)` at odd k and `ceil(k(N-k)/N)` at even k. They match bit reversal pointwise at N=8 and N=16, proving exact minimum upper-right total ranks 14 and 48. Finite-size total optimality at larger N is not established.

For common-coordinate-order products, quasiseparable ranks add, so s stages of rank at most r require sr>=N/4+1. Uncharged interstage permutations and differently ordered stage representations prevent using that inference directly. A rank statement is not an unrestricted arithmetic-operation lower bound.

The older two-stage bound N<=9r^2+7r retains its natural/affine-input endpoint restriction. The new one-matrix theorem does not extend its endpoint scope. The independently reproduced N=8 subset, optimized-support and trace screens do not improve the previous 15,728-survivor window screen. See `additions/1848/`; all 15 source-manifest entries and the inherited window archive hash verify.

## Consolidated outcome and scope

The strongest new constructive results remain restricted-input exact evaluators and a conditional improvement to an approximate-method scan subproblem. Every proposed arbitrary-input construction still needs a scalable exact identity, exception coverage, an efficient full evaluator, charged coefficient/root preparation, and an appropriate numerical or bit-cost contract. The F8 polynomial systems and exceptional charts remain open where previously stated. The earlier parity, Gram, uniform Prony, unitary, summary-rank and precision results remain in force.

Twenty-two later direct-upload records and two Library-discovered source records are now integrated, with known identical copies labeled separately. Earlier baseline read/coverage limits are unchanged: completing these bounded new-source audits does not imply that all historic source texts or account conversations have been fully reviewed. Five newer direct source records received at 19:06–19:10 remain pending: the bounded-chirp note, centered v12 archive, bit-reversal multistage geometry archive, Phase25 archive and offset-class joint v12 archive. Their claims are not promoted here. `PENDING_ADDITIONS.json` records their exact known identities and review status; completion of the earlier bounded audits does not declare the research problem solved.

# Retained version 7 checkpoint

Pending-source references below are historical. Phase24, HERO0 and the endpoint audit are completed above. All previous accepted results and restrictions are retained.


## Verified Phase23 and interval-window addition

9 October 2026. Integrates the exact 18:24/18:25 Library-generated archives against master version 6, including the finalized 17:42 supplement and all earlier verified work through 18:07. A distinct 18:28 same-name window archive was also downloaded and proved byte-identical. No new exact arbitrary-input, all-output sub-N-log-N evaluator has been established.

## Accepted source results

- The general window rank-nullity lemma is correct with actual transform-submatrix ranks. Its simplified Vandermonde version permits arbitrary Fourier output order, but Fourier inputs must remain in natural or affine coprime-stride order. The source's N<=9r^2+9r+3 consequence for two stages of both quasiseparable ranks <=r is valid in this scope.
- The N=8 full-window filter leaves 15,728 of 40,320 permutations, compared with 28,584 under the old bilateral filter. The 12,856 extra rejections and all endpoint-permuted N=8/N=16 Cooley–Tukey positive controls were independently reproduced. The latter controls decisively prohibit silently applying the simplified Vandermonde gate to arbitrary input permutations.
- Phase23's geometric resolvent, sparse cyclic-difference formulas, binary Hankel rank obstruction and exact inverse-residual support count are correct. They establish exact special-input linear-work routes and architecture-specific limitations. The original exponential detector requires split distinct roots in the working field; it is not a complete recognizer for arbitrary order-two recurrences.
- The classical binary Hankel rank distribution bounds low-complex-exponential-rank coverage by 2^(2r-N+1) for r<N/2. This is a restriction on low-order input descriptions, not a lower bound on arbitrary Fourier algorithms. Leading Hankel rank alone is not sufficient to recognize the entire input's recurrence.

## Independent bounded extensions

1. A strengthened marker-gap argument gives N<=9r^2+7r for r>=1 in the same natural/affine-input endpoint model. Thus two rank-one stages are excluded for N>=17, improving the source's N>=22 cutoff. A source-supplied N=16 permutation passes all window tests, making 16 the sharp maximum length permitted by this necessary rank-one filter; it is not an actual factorization.
2. The entire all-window test reduces exactly to six endpoint checks and three sliding-minimum/maximum passes. A monotone-deque implementation costs O(N) comparisons/indexing and O(N) space, and agrees with exhaustive testing on all N=8 permutations and varying asymmetric ranks. This speeds the architectural filter, not the transform.
3. A square-root-free rational generating-function executor handles every verified fixed-coefficient recurrence of order at most two, including repeated and nonsplit roots. A raw-input recognizer is complete for this class. All Fourier outputs require O(N) field arithmetic plus charged root/normalization setup and a constant number of inversions; at most two singular Fourier nodes are evaluated by O(N) direct sums each. It strictly enlarges the original restricted-input branch without improving arbitrary-input worst-case complexity.
4. For supported dyadic N>=8 over GF(998244353), the original exponential detector accepts exactly six binary words. Combined with its first/second-difference threshold, the original adaptive fast path accepts exactly N(N-1)+4 of the 2^N binary inputs, strengthening the source upper bound N(N-1)+34. This exact characterization concerns the original detector, not every possible recurrence/Green algorithm.

## Cost and construction implications

The new recurrence executor avoids data-dependent square roots and splitting-field preparation. Exact equality testing, finite-field inversion, primitive-root/normalizer preparation, coefficient representation and bit precision remain explicitly charged according to the chosen model. A fixed modulus with bounded supported lengths is not an unbounded asymptotic family. No floating-point stability guarantee is supplied by the algebraic formulas near singular denominators.

The window result prevents scaling a natural/affine-input two-rank-one-stage ansatz beyond N=16, regardless of its internal permutation. A viable architecture must enlarge ranks or stage count, use genuinely non-affine input order, or leave that architecture; each surviving candidate still needs exact full Fourier identities and a fully charged executor. The special-input recurrence result is constructive but has exponentially sparse coverage on uniform binary inputs at fixed order. Neither result resolves the arbitrary-fresh-input, all-output target.

## Evidence and integration

All paths in this section are relative to `additions/1825/`. Reports: `window_audit/WINDOW_AUDIT.md`, `phase23_audit/PHASE23_AUDIT.md`, and `SOURCE_PROVENANCE.md`. Run `python3 run_independent_audits.py` for the independently authored checks only.

Two distinct archive streams contain 721 recursive member occurrences, 536 distinct byte contents and 27 byte-new contents relative to the explicit predecessor hash union. All 860 embedded checksum entries pass. Both immediate nested predecessors exactly match the already audited 18:07 archives. Complete inert source archives, identity/version records, duplicate-copy hash evidence, independent checkers and results are included. No uploaded program or bytecode was executed or imported, and no novelty or publication-priority claim is made.

## Later direct inputs still pending

The 18:45 Phase24 archive, 18:47 HERO0 note and 18:48 optimal-endpoint archive are being reviewed separately; their new mathematical claims are not included as verified findings here. The accompanying 18:45 window archive was independently compared byte-for-byte and is identical to the now-verified 18:25 source. Exact identities and statuses are in PENDING_ADDITIONS.json.

# Retained version 6 checkpoint

Historical pending references in the retained text describe earlier snapshots. The Phase23/window discovery review is now completed above; the 17:42 review remains completed.


All uploaded batches through18:07 UTC are now independently audited, including the previously pending17:42 Phase21/v11 supplement. Two newer Library-discovered checkpoints are under separate review and are not included as verified findings. There is still no new exact arbitrary-input all-output sub-N-log-N evaluator established by this project.

9 October 2026. This resolves the previously pending 17:42 batch. Paths in this section are relative to additions/1742/. The independently verified18:07 results remain included below. The new evidence does not establish a fully charged exact arbitrary-input all-output transform below N log N.

## Provenance and exact F8 status

The new mathematical sources are Phase21 Weyl–Green research and all-length fused v11. The third archive is the same triple-intersection source bytes as the 17:17 upload. This was checked by the explicit Library identity, a fresh separate retrieval, raw-byte comparison and all 214 recursive members, not by filename. Preserve every prior exact F8 residual, resultant, saturation/corner condition and exceptional chart.

The complete batch contains 671 recursive member occurrences, 487 unique member hashes and 29 byte-new text/data/source-program contents versus the declared prior union; all 815 embedded checksum entries pass. Phase21's nested Phase20 and v11's unit-step core are unchanged. No uploaded source program or binary was executed.

## Phase21 exact representations and sharper barriers

- The Weyl chirp identity, flat dense Green example, common-Weyl pole budget q≥N/2 with arbitrary outside diagonal scales, weighted same-order sum/product bound Q≥N/2, and full-rank cheap commutator example are correct in their stated even-length domains.
- Wraparound cross-ratios sharpen the common-generator coefficient form: the otherwise geometric multiplier rho must satisfy rho^N=1.
- The degree-N/2 Prony polynomial is independently reconstructed. Nonzero derivative/forbidden-pole resultants certify matching N/2-pole complex representations for all supplied dyadic lengths4..8192, plus18 listed non-dyadic lengths. These are finite characteristic-zero certificates; the uniform N/2-pole claim remains open.
- A new uniform construction proves h≤minimum common-Weyl pole count≤h+1 for every even N=2h≥4. The pencil zP_h+tP_(h−1) preserves the required moments; consecutive coprimality and a finite bad-parameter count guarantee a valid integer t in {1,…,4h}. This is a representation existence result, not a runtime improvement. See `prony_extension/PROOF_OR_OBSTRUCTION.md`; symbolic degree8 and67finite-size controls independently pass.
- Every arbitrarily ordered weighted-cycle inverse has cross-cut rank exactly equal to the number of nonzero directed cycle edges crossing into the row half. Products/sums add this budget; masks cost zero; inserted permutations have their own crossing cost. Exact Fourier requires total budget≥N/2. Reverse direction alone still costs one and does not escape.
- For Fourier halfblock C, let v_N=tr(CC*−(CC*)²)=O(log N). A rank-q candidate block with q<N/4 has spectral error≥sqrt(max(0,1−v_N/(N/4−q))). The floor tends to1 for q=o(N), and for q≤(1/4−epsilon)N. An explicit odd-harmonic upper bound on v_N makes this quantitative.
- Term/crossing counts remain representation restrictions, not unrestricted shared-evaluator runtime lower bounds. Many same-order terms with a genuinely efficient shared evaluation are not excluded.

See `phase21_audit/PHASE21_AUDIT.md` and the explicit modular certificates.

## Fused all-length approximation and numerical qualifications

- Clenshaw streaming and Neumann block/local Bessel fusion are algebraically valid. Fixed-H storage is O(N); R decoder/short-FFT/output passes remain, so total shrinking-error work stays O(RN).
- H=0 fusion admits the sharper deterministic bias tau_R+Delta, Delta=pi(M−1)/Q, independent of an additional R multiplier. Its variance envelope remains (M/N)(1+tau_R)²||x||²; Delta enters the deterministic bias.
- G_(-h)=(-1)^h G_h, so only H+1 independent local channels per block remain. L fixed rows retain rank at most L(H+1)K, regardless of R; uniform exact summary-only recovery requires L(H+1)K≥N and, with a full input block, L(H+1)≥M.
- The source's full-row floating-point hypothesis does not automatically certify rounded fused summaries. A summary-decoder contract, summable uniform coefficient majorants, explicit summary/Clenshaw rounding and charged phase/Bessel generation are necessary. The independent sufficient ledger preserves the proposed leading precision order once those stronger contracts are met; it does not certify the uploaded SciPy/NumPy implementation or fixed binary64.
- A specified certified Bessel series generator can keep preparation within O(RN) arithmetic in the theorem regime, but its cost is not free and is not contained in the advertised O(N+RK) input-traversal saving. Bit cost, exponent range, integer overflow and robust classification/radius errors remain charged.
- The separate frozen-block rational-Taylor variant uses unweighted block summaries, O(N+RK) input-side arithmetic and O(RN) decoder work. Its deterministic bias is Delta+eta+|rho|^R/R! with |rho−pi|≤eta. This is a charged approximate exact-arithmetic variant; its fused numerical path still needs a summary-level contract.

See `v11_audit/V11_AUDIT.md` and `v11_audit/FP_CONTRACT_REVIEW.md`. Keep fixed-input simultaneous-output guarantees distinct from uniform operator accuracy and exact all-input recovery.

## Combined next target

The old complete chirp bank still reduces to Cooley–Tukey under its known evaluator, and the exact near-grid correction still has rank N/gcd(N,Q). Fusion does not change those exact statements. Any proposed speedup must supply a scalable exact identity, complete exception coverage and a fully charged shared evaluator. Classical identities and finite prototype tests are not novelty or production-certification evidence.


# Retained checkpoint including18:07 results

The historical pending references below describe the previous version; the17:42 review is now complete as stated above.

Verified updates include the 18:07 UTC Phase22 and bilateral uploads and the previous master through 17:17 UTC. The separate 17:42 mathematical supplement remains pending; its hashes are used only for provenance comparison. No new exact arbitrary-input all-output sub-N-log-N evaluator has been established.

9 October 2026. This addition can be merged into the authoritative master through 17:17 without waiting for the separate 17:42 mathematical supplement, which remains pending unless independently finalized. All paths here are relative to additions/1807/. No exact arbitrary-fresh-input, all-output sub-N-log-N evaluator has been established.

## New exact structural facts

- Phase22's real one-mask connected-Gram obstruction is sound. A stronger exact characterization is available: for real invertible A, existence of real invertible B and one nonzero complex diagonal Q in F=A Q P B is equivalent to J A=A E for a diagonal reflection-parity matrix E with entries ±1. This characterizes the left factor when the right factor is free, not a specified pair or a fast evaluator. Positive real left Green sums fail it.
- The bilinear finite-field Gram screen is necessary for fixed A,B and every middle Q,P. The 24 sample vetoes and 12 deliberately valid recoveries are independently reproduced. Zero-diagonal/collision branches remain inconclusive; Gram equality and one calibrated entry are insufficient for Fourier equality.
- F=H Q C is an exact cheap parity/axis extraction with C a real orthogonal cosine/sine residual. C still requires at least N(log2 N-1)/2 two-coordinate unitary gates in that restricted model. The sparse covariance and full first column uniquely specify the linear C, but do not evaluate Cx cheaply.
- The finite-field covariance test requires a fixed deterministic linear oracle and independent uniform challenges. It uses one seed call plus two calls per challenge. The uploaded apply_R repeats modular exponentiation, so its advertised linear overhead is not met as written; an independently specified consecutive-power recurrence repairs the coefficient/application count. Root/field setup and precision remain separate costs.
- The all-length tail-rank theorem gives min(t,N-1-max(pi[-t:])) <= r_lower(C)+r_upper(B), with a mirror prefix inequality. It covers general quasiseparable ranks in the fixed endpoint order. The unchanged tail (1,2,5) is excluded for every N>=9 with two rank-one stages, but N=8 remains open.
- For a constant rank sum s, every suffix/prefix inequality reduces exactly to the corresponding first/last s+1 boundary test. At s=2, 28,584 of 40,320 N=8 permutations pass. A closed-form count and the disjoint-boundary uniform-permutation bound P(pass)<= (s+1)^4/[N(N-1)] are proved. Passing is only necessary.
- The inherited 11-by-9 rank gate has no independent extra maximal minors: 45 vanish identically and the remaining 10 are constant multiples of Dhat=-DB DH. All 55 were independently reconstructed. Rank<=8 is exactly DB DH=0 within this rescaled polynomial family; original feasibility equations and all exceptional branches remain required.
- DB's homogenized coefficient matrix has exact rank four, with the nonzero 11251 modulo 12289 witness reproduced, so the quadric is absolutely irreducible in characteristic zero. Its unique affine singular point has h0=h1=0, so it is smooth on the inherited regular h0!=0 chart. Its zero locus is not excluded.
- The six-column auxiliary boundary gate has rank 4+rank([[U3,-L3],[U4,-L4]]) for N>=9. Its leading determinant is -(U3 L4-U4 L3) times the six-node Vandermonde. N=8 remains a genuine rank-deficient exception. The report supplies the direct proof absent from the source's referenced proof file.

Reports and reproducible evidence: `TWO_LATEST_AUDIT.md`, `phase22_audit/`, `bilateral_audit/`, `tail_screen_extension/`.

## Provenance

Two new outer source archives; 691 recursive member occurrences; 507 distinct contents; 34 byte-new text/data/source-program contents against the declared source union through 17:42. All 833 embedded checksum entries pass. The embedded Phase21 and triple-intersection archives exactly match prior sources. No uploaded executable, source program or bytecode was run. The supplementary archive contains full inert sources, source identities, explicit hash comparison data and independently authored checks.

No unrestricted lower bound, new exact transform or novelty claim follows from these results. The earlier verified exact residual systems, exception coverage and model limitations remain in force. The 17:42 Prony, cycle-crossing and fused-summary additions keep their separate pending/completed status; their source hashes are used here only for deduplication, and this audit does not promote them automatically.


# Retained checkpoint through 17:17 UTC

Current through the three archives received at 17:17 UTC on 9 October 2026. The three newer uploads received at 17:42 UTC are being audited separately and are not included as verified results here. No new exact arbitrary-input, all-output sub-N-log-N transform has been established by this project.

9 October 2026. Verified additions through the 17:17 UTC upload. All report paths in this latest section are relative to additions/1717/. Earlier residual systems and exception coverage remain preserved below.

## Current answer

The new materials do not establish an unrestricted, fully charged exact all-output transform below N log N. They give a genuine characteristic-zero slice exclusion in the fixed F8 search, stronger restricted approximation obstructions, complete Weyl certification tools, and an all-integer-length randomized approximate lift. An independently specified rational-Taylor variant closes the source's Bessel coefficient-preparation gap at the arithmetic level and supplies a conditional precision ledger.

## Exact F8 structural chart

- The new 11-by-9 multi-column gate has rank at most eight for the intended invertible globally separated inverse-stage/final-stage factorization. The source's standalone theorem needs the nonzero-column/invertibility hypothesis. If the fourth output multiplier is zero, invertibility forces the projected four-row basis to have rank at most two, so its cofactor vector is zero; no new nonzero multiplier guard is needed.
- On `h0 Delta T != 0`, an exactly reconstructed 250-term degree-eight minor is `Dhat=-DB DH`, with nine-term quadratic DB and 105-term sextic DH. All 924 exported cyclotomic coefficient vectors match.
- `Res_h6(W,Dhat)` at `h0=1,h1=h2=0` reduces to 6 modulo `(17,zeta8-9)`. This nonzero exact resultant proves the specified regular complex slice has no factorization. It does not exclude other base points or denominator branches.
- The nonzero 37-term and 476-term eliminated resultants constrain the base to a proper hypersurface union. The necessary four-structural-variable locus has dimension at most two, not proven empty.
- A new exact refinement proves the base where W is identically zero in h6 has at most 12 points. A degree-six elimination resultant and a fixed nonzero quadratic leading coefficient certify this. Its free-h6 stratum has dimension at most one; the overall dimension bound remains two.
- Independent GF(17) enumeration reproduces 4,596 candidates and ranks 9/8/7/6 with counts 3,266/1,203/125/2. Another 630 invertible exact positive controls pass, including zero-column multipliers and zero diagonal entries.

The gate/resultants are necessary additions, not replacements for the complete Fourier equations. Keep the old saturation/corner conditions, all excluded branches and the full separated-generator lift. Report and scripts: `triple_audit/`.

## Green Phases19 and20

- Full Weyl duality `MZ=DM`, `MD=Z^-1M` identifies the scalar Fourier family at every integer length; one scalar calibration gives F. The sharp Frobenius residual gap is `2 sin(pi/N)`. Small raw residuals at increasing N do not imply fixed accuracy.
- A fixed linear finite-field oracle can be checked in `1+3h` calls. If its stacked residual rank is rho, independent uniform tests pass with exact probability `p^(-h rho)`. This is not a linearity test, a characteristic-zero proof, or a cheaper evaluator of the candidate.
- Projective root/histogram tests are necessary, not sufficient. Sylvester Hadamards pass every pair histogram and fail Fourier equivalence. The complete anchored-grid criterion extends to arbitrary N; the independent implementation uses a gcd-unit pivot, while the source implementation is dyadic.
- A stronger conditioning-free inverse-support bound is proved: one inverse row of support s implies `||M-F||_2>=sqrt(1-s/N)`. Pure inverse products with support bound s^t therefore have error at least `sqrt(max(0,1-s^t/N))`. Sums do not inherit inverse sparsity.
- A stronger common-frame stationary bound is proved: rank commutator at most r<N implies error at least `cos((2 floor(r/2)+1)pi/(2N))`. For t stages of q stationary path Green terms, r<=2qt, so the floor tends to one when qt=o(N). Arbitrary masks and independent path permutations require separate treatment.
- Newly supplied nested Phase19 independently verifies fixed-middle-monomial signatures, the banded inverse one-norm bound `(b/a^2)[1+2w(b/a)^2]`, resulting gain/conditioning budgets, and the one-Harper-middle-monomial exclusion. Call/stage counts do not prove an unrestricted scalar-operation lower bound for shared computation.
- The real-core and one-complex-mask axis-count restrictions are correct under their distinct assumptions. Dense positive controls do not supply a fast transform.

Reports: `phase19_audit/`, `phase20_audit/`. Exact source-family reconstructions at N=8,16,32 match. Larger source experiments are preserved as source-reported and were not rerun.

## Exact bridge and phase-aware Green extension

- For fixed a, beta_h=beta_0+hK gives M orthogonal block projectors P_h/M whose sum is I. Averaging the complete row bank therefore gives exactly F. Fewer than M rank-K row sketches cannot determine every arbitrary input from that linear transcript alone, even with nonlinear decoding. The exact/adaptive/randomized scope is made explicit in the bridge report.
- The straightforward complete bank costs O(NM+N log K); at M=Theta(log N) this is Theta(N log N). Shared local analysis gives the ordinary N log M plus N log K factorization scale. No universal shared-evaluator lower bound follows from these schedules.
- The exact near-grid residual matrix has Vandermonde rank N/gcd(N,Q), with Q the dyadic lift length. An exact separated correction needs at least that many terms; at odd N its rank is N. Completing the beta bank for each short approximate term computes the truncated center exactly without removing its bias. Different nonseparable corrections remain outside this obstruction.
- A new independently reviewed phase-aware displacement obstruction permits products of sums of c D^a P B^-1 P^-1 D^b, with constant-coefficient path denominators, integer linear phases and independent affine conjugations P. Common-frame displacement costs at most rho=2 per inverse; affine-conjugated paths cost at most rho=4.
- For b expanded branches and d distinct total phases, exact Fourier equality requires `N<=d(1+sum r_branch)<=d(1+rho t b)<=b+rho t b^2`. Fixed summand bound q>=2 therefore forces t=Omega(log N), without conditioning assumptions. One branch forces t>=(N-1)/rho. A common phase at even N improves the exact rank target to N and admits the same cosine spectral-error bound.
- Arbitrary diagonals, arbitrary path permutations, independent left/right affine factors and bare affine-multiplier wiring are outside that grammar. The reviewer gives a nearly full-rank bare-affine counterexample. This is an architectural stage bound, not an unrestricted scalar-operation lower bound.

Reports: `astra_exact_bridge/` and independent `twisted_bound_review/REVIEW.md`.

## All-length approximation and charged variant

- The v10 dyadic near-grid Bessel/Chebyshev lift is algebraically valid. Using the same state for all rank terms preserves per-output variance `(M/N)(1+tau_R)^2 ||x||_2^2`, without an R multiplier. Its deterministic bias is at most `tau_R ||x||_2` per coordinate.
- This is a fixed-input randomized simultaneous-output approximation, not arbitrary exact recovery. It does not automatically preserve the previous sparse-spectrum exact promise after input weighting.
- The uploaded prototype uses Theta(RN) Chebyshev storage, uncharged/uncertified special-function evaluations and floating grid indices. Naive forward Bessel recurrence is an unstable repair. N=1 needs its direct case. The endpoint failure target N^(-a) is vacuous at a=0 unless multiplied by a fixed constant below one.
- The independent rational-Taylor variant generates a rational rho approximating pi via finite Machin sums, with certified error eta, and tail `eta+|rho|^R/R!`. Streamed powers/factorial recurrences and exact integer indices charge coefficient generation in O(RN+log(1/eta)) arithmetic work for a fixed number of random rows, with O(N) arithmetic storage.
- Under the inherited specified dyadic row/root contract, its deterministic rounding ledger covers weights, coefficients, row error, cancellation, sum, normalizer and robust classification/radii. It is conditional implementation mathematics, not certification of the uploaded binary64 code. Growing rational/floating bit costs and exponent range remain charged.

Reports: `lift_audit/`, `taylor_extension/`. Independent full-state covariance controls through Q=32 agree numerically; 6,240 exact-rational finite-precision recurrence checks pass. Numerical controls corroborate proofs without certifying a production evaluator.

## Provenance and reproduction

The batch adds 77 new byte contents versus the declared source union through 16:46: 73 text/data files, three bytecode files and one new nested Phase19 archive. There are 656 recursive member occurrences, 472 unique hashes and 799 passing embedded checksum entries. Full sources, Library identities, hashes, fresh independent scripts and portable rerun records are preserved. Uploaded code and bytecode were never executed.

Main synthesis: `THREE_LATEST_AUDIT.md`. Source inventory: `SOURCE_PROVENANCE.md` and JSON records. No publication-priority or chat-only completeness claim is made.


# Retained detailed checkpoint through 16:46 UTC

The following earlier results remain valid within their stated models. The latest section above and additions/1717/ supersede its frontier descriptions where indicated.

9 October 2026. Includes the baseline master, the 14:50 and 15:20 additions, the three archives received at 16:28 UTC, and the spectral-determinant archive received at 16:46 UTC. Original dated inventories and audits remain preserved.

## Goal and present answer

The target remains an independently justified exact Fourier transform for every fresh arbitrary input and every output coordinate, with genuinely sub-N-log-N charged work. Root/coefficient preparation, routing, conversions, workspace, precision where claimed, and explicit outputs count.

The project has not established that target. Nor do its restricted obstructions prove an unrestricted Fourier arithmetic lower bound. Approximation, sparse-spectrum exact recovery, Boolean inputs, finite-field controls, pair-unitary circuits, additive Green sums and unrestricted complex arithmetic are different models.

## 1. Exact algebraic route: a 12-equation regular target, with exceptions retained

The fixed-permutation F8 two-separated-generator-stage problem retains its independently reconstructed older formulations:

- 30 quartics in 26 variables for an inverse-stage regular chart.
- 25 sextics in 21 variables after Fourier-support elimination; on the nonzero-t chart, primitive cancellation gives four cubics, six quartics, one quintic and fourteen sextics.
- 176 quadratics in 184 variables for the complete separated-generator lift, including zero-anchor corners.

The 16:28 dual-support/onion source gives two further reductions on smaller explicit open loci:

- First lower-column and upper-row elimination: 20 polynomials in 16 variables, degree at most 9.
- A second column gives a three-character recurrence; a second row eliminates the remaining interior generators. For n>=6 and the specified first three permutation entries, the selected conditions have an eight-parameter rational reconstruction, with (n-4)(n-5) remaining identities. At n=8 this leaves 12 rational equations in eight parameters.

Neither statement solves those remaining equations or proves inconsistency. The eight parameters do not parametrize complete Fourier factorizations without the residual conditions.

The new reconstruction requires nonzero first-row prefix expressions S, second-row elimination determinants Delta, and a boundary 2-by-2 determinant. These join the previous nonzero denominators, second-stage anchors, det(C), and inverse-stage corner conditions. The independent audit supplies a characteristic-zero Q(zeta8) exceptional partial point with S1=0 and all required old determinant/corner conditions nonzero, certified through a valid mod-97 reduction. It proves the new S exclusion is substantive, but fails the remaining equations and is not a full factorization.

The old normalization fixes diag(A), while the inverse chart fixes diag(A^-1); they are not interchangeable. The exact example A=(7/6)I-(1/6)J has diagonal one but inverse (6/7)I-(6/7)J has zero diagonal. The earlier regular-chart saturation product had degree 59, with a degree-60 reciprocal equation. Clearing denominators in the newer rational system likewise cannot silently discard excluded branches. An independently exported 3,750-node exact rational circuit records the eight-variable F8 target and 29 nonzero guards.

The older unsaturated sextics contain a spurious all-ones-matrix beta-line. Neither the original rank-60-to-61 local jet obstruction nor the newer reduced chart excludes F8 globally. The complete lift remains necessary for exception coverage.

### Latest exact-branch refinement: spectral determinant and adjacent tail

The 16:46 audit independently matches the 45-term quartic Q, three degree-seven upper resultants, a five-variable necessary determinant circuit, and the 31-term cubic W. All 898 polynomial coefficients match. These necessary projections supplement the twelve residual equations; they are not sufficient replacements. A nonzero Jacobian witness establishes algebraic independence, not emptiness or the codimension of the zero fiber.

The adjacent-column tail lemma is useful on excluded onion branches: separated tails, invertibility and the actual upper-stage rank constraint force two tail recurrences without dividing by S or Delta. Substitution into the normalized lower-generator formula still requires its own assumptions. Solving the tail recurrences introduces a new nonzero affine pivot; its zero branch remains open. Full factorization of W is undetermined.

A fresh GF(17), z=9 enumeration reproduces 78,608 h tuples and zero full-B successes among 2,546 invertible candidates; 1,927 also meet every final corner guard. Of 12,358 reconstruction rejects, 710 have alpha=0 and dependent columns, while 11,648 are omitted denominator branches. The search retains zero beta-coefficient and singular gamma cases where permitted. This is a finite-field open-branch exclusion, not a complex-field or extension-field exclusion. No valid exact F8 factorization or characteristic-zero nonexistence certificate was found.

Full report and exact certificates: `additions/1646/SPECTRAL_DETERMINANT_AUDIT.md`. Retain all twelve residuals, the nonzero guards and the complete lift for broader exception coverage.

## 2. Approximate chirp route: unit-step decoding and sharper variance

The inherited v7/v8 dyadic construction used two output cycles and covariance (2M/N) times a rank K(M-1)/2 projector. The specified v8 gauge decoder already had a complete independent numerical contract in the 15:20 audit.

v9 replaces the quadratic phase with the integer-valued binomial phase a*t*(t-1)/2. For N=p^L=KM, with K and M powers of the same prime, M>=2 and K>=M, a unit step gives one output cycle. A parity-dependent linear phase makes its monodromy -1, so one balanced scan supplies both total and prefixes, including the seed.

For each output the exact one-row error covariance is

Q_m = (M/N) Pi_m,

where Pi_m is an orthogonal projector of rank N-K. At output zero,

Q_0[n,n'] = (M delta[n=n'] - 1[n congruent to n' mod K])/N.

Thus its nullspace is the K-periodic input subspace; other outputs have the corresponding diagonal modulation. This is an explicit covariance/error-nullspace statement, not an arbitrary-input exact-transform construction. At M=1 the covariance is zero, so its norm is zero rather than M/N.

The same three shifted grids and Boyer–Moore counters give simultaneous all-output error at most

(5/sqrt(2)) g sqrt(M/N) ||x||2

with failure at most 2N exp(-R D(1/2 || 1/g^2)), under the exact-arithmetic quantization contract and its stated parameter range. The deterministic radius improves by sqrt(2) compared with the preceding construction. Work per row remains O(N+K log K); streaming storage is O(N) words.

Claims obtained by choosing M=Theta(log N) require a fixed or bounded prime, or explicit prime-dependent constants. A nearby power of an unbounded prime need not be Theta(log N); prime N has no nontrivial admissible M under K>=M. Mixed-prime lengths do not inherit the projector theorem merely from K>=M.

For the specified dyadic implementation, the earlier explicit bound transfers:

row numerical error <= 800 sqrt(NM) log2(N) u ||x||2,

provided 8u log2(N)<=0.01 and the same certified-root/normalizer, exact-index, range, pairwise-summary and normalized radix-2 short-FFT contract holds. The v9 seed charges half the total-scan error plus prefix error deterministically; no independence assumption is needed. Odd prime powers still need an explicit certified short-FFT constant.

Taking u <= theta g/[800 N log2(N)] bounds deterministic numerical error by a chosen fraction of the stochastic radius. Certified norms and inflated grid radii preserve the failure argument. This theorem covers the specified implementation, not the uploaded NumPy/native prototypes or arbitrary fixed IEEE precision. Root setup, exact represented-grid classification, bit cost, exponent range and input/output bits remain charged. Space is O(N) words, not bits. Source benchmark timings are source-reported and were not rerun. The source's short-FFT input-error contract needs a separate input-perturbation term when exact summaries cancel; the independent theorem supplies it. Its default constant 64 is not certified. Native summaries are sequential, timings omit root/plan setup, and the saved five-row benchmark parameters have a vacuous generic all-output confidence bound.

### Two bounded extensions, with different guarantees

An independent exact structured-input corollary is available for a fixed input with at most h nonzero Fourier coefficients. For prime-power N, a row's off-diagonal Fourier interaction requires m-j congruent to a*d mod K for some 0<|d|<M. Its diagonal equals one, and the interaction probability is at most 2M/K. Consequently exact-value Boyer–Moore on R=2s-1 rows recovers every output exactly except with probability at most

N binom(2s-1,s) (2hM/K)^s.

This uses exact arithmetic, exact complex equality, a sparse-spectrum promise and charged root/short-FFT primitives. It is not an exact dense-input or finite-precision result. For fixed h and fixed prime, choosing M=Theta(log N) and three rows gives O(N) arithmetic work and O(h^2 log^4(N)/N) failure. This is a restricted sparse-Fourier corollary, not a novelty claim or the unrestricted project target.

For arbitrary composite N=KM with 2<=M<=K, the projector shortcut fails, but an independent masked-shell proof gives a usable variance bound. Let D(N,M) count divisors g of N with g<M and let L=ceil(log2 M). Then

||Q|| <= [(M-1)/phi(N)] min{D(N,M), 2(L+1)^2}.

The extension provides a sharper computable shell-count bound as well. Substituting the proved variance proxy into the robust decoder gives a composite-length approximation with an explicit accuracy loss. Factorization and phi/divisor preparation are charged: trial division takes O(sqrt(N)) word divisions for array length N, so these need not be hidden oracles. Linear work per row still requires an appropriate divisor M near log N; no uniform all-integer-length speed theorem follows. The stronger tested inequality ||Q||<=M/phi(N) remains a conjecture. Numerical sweeps and exact rational-entry checks do not prove it.

## 3. Independently ordered Green sums: a broader restricted obstruction

The newly included nested Phase17 studies the additive architecture

A = sum_r L_r P_r^-1 B_r^-1 P_r R_r,

where each B_r is invertible with half-bandwidth w_r in its own order, P_r conjugates both row and column labels of that summand, and L_r,R_r are diagonal. Put W=sum_r w_r. Coefficients may be complex, nonunitary, noncommuting and ill-conditioned.

A common separator exists in all q orders with equal group size at least

m* = ceil(floor(N/2) / 2^(q-1)).

The uploaded weaker floor(N/2^q) bound remains valid. Across this separator A has rank at most W. Every normalized Fourier submatrix of size m has squared Frobenius norm m^2/N and operator norm at most one. Hence exact equality requires m*^2<=WN. When m*>W and m*^2>WN, the uniform operator-norm error is at least

sqrt((m*^2/N-W)/(m*-W)).

For bounded bandwidth this forces logarithmically many summands, but does not prove a scalar-operation lower bound for shared-state evaluation. It does not cover arbitrary products of sums or arbitrary non-diagonal outside mixers. The independently permuted row/column case is covered by the separate weaker separator extension below.

A bounded independent synthesis combines the sharper separator with the complex prime-order DFT's full-spark theorem: for prime N, exact equality requires N<=2^q W+1. In particular, two tridiagonal Green summands are excluded for every prime N>=11. This uses characteristic-zero Chebotarev theory, not arbitrary finite-field full-spark. It improves the uploaded prime monotone-chain threshold, with no publication-priority claim.

A second independent extension closes the source's proposed escape through distinct row and column permutations inside each summand. Sorted row/column position lists always admit strictly separated subsets of size floor(m/2), even if their original label sets overlap. Iterating gives m=floor(N/2^q), so the original all-length rank and spectral-gap bounds also hold for sum_r L_r P_r^-1 B_r^-1 Q_r R_r with independent P_r,Q_r. For prime N this gives N<=2^q(W+1)-1. The stronger ceil-rounded matched-order bound is not claimed here; two tridiagonal terms with independent endpoints are excluded at prime N>=13.

Products of Green sums can escape the additive crosscut bound. Passing that rank test is necessary architectural progress, not evidence of correct Fourier coefficients or a low-cost transform.

## 4. Harper and phase coherence: exact certificates, no fast executor

Phase18 adds a sparse self-dual operator H=T+V, where T is the cyclic nearest-neighbor shift sum and V is the cosine diagonal. For N divisible by four, the even and odd reflection sectors are irreducible Jacobi matrices, each with one zero mode. Fourier acts differently on those two zero lines, so no scalar rational function of H with an invertible denominator equals F.

Adding reflection parity gives a correct polynomial representation with exact degrees N/2 and N/2-2. The top even coefficient is 1/(2 sqrt(N)). Direct sparse Horner application is quadratic; degree alone is not an unrestricted arithmetic lower bound.

For even N>=4, the joint commutant of T and V is span{I,J}. Therefore the exact sparse intertwining identities MT=VM and MV=TM force M=F(aI+bJ); calibrating M e_1=F e_1 fixes M=F. These are useful symbolic certification targets. Exhaustively probing them is not a faster black-box equality algorithm.

For fixed invertible outside factors A,B, Weyl covariance of A Q P B forces A^-1 D A and B Z B^-1 to be monomially similar. Diagonal multisets and directed two-cycle products give necessary vetoes for every intermediate diagonal Q and permutation P at once. A veto for sampled fixed factors is not an all-parameter exclusion. Modular nonzero witnesses lift only when the relevant root map and inverses/denominators reduce correctly.

The real eigenbasis identity F=O Lambda O^T with a four-phase diagonal Lambda is a positive algebraic control. No fast O application is provided; allowing its growing coefficient field also explains why it does not contradict the earlier single-mask field-descent obstruction.

## 5. Unitary route and earlier filters retained

- Phase15's exact normalized Fourier factorization uses N log2(N)/2 pair-unitary gates. Its Fourier-bank costs are not removed by further optimizing the already-linear fold.
- Phase16 compiles a full path/Haar–Green stage into at most (11N/2)-8 pair-unitary gates, giving at least N log2(N)/(11N-16) stages for exact F. Adaptive prefix pivoting repairs a generic degenerate-column pivot issue. Parameter preparation is not automatically linear-time.
- Entropy continuity retains logarithmic stage count for exactly unitary approximants with fixed error below one in the stated operator or normalized-Frobenius norms. Zero-initialized ancillas do not remove the pair-unitary count; nonunitary/shared-state circuits remain outside this result.
- Common-order noncommuting tridiagonal resolvents retain additive expanded-expression cut-rank budgets. This is a consequence of inverse rank and rank subadditivity, not a general Fourier lower bound.
- Products with inverse-stage row sparsities s_j require product(s_j)>=N. Dense inverses and sums need separate analysis.
- Common-base rational functions, low-cut-rank local-port solves, field descent and Galois phase-support tests retain their original stated scopes.
- Quadratic polynomial decoding of a deficient fixed linear sketch cannot recover every Boolean input's full linear target; worst-case randomized success is at most 3/4. Cubic interpolation escapes that restriction without supplying a faster transform. Realification and conjugate-bin symmetry remain explicit.

## 6. Why the branches do not collapse into one claim

The chirp result is a fixed-input probabilistic coordinate-error guarantee with a nonlinear robust decoder. The Green-sum bound concerns uniform operator-norm approximation by a particular linear architecture. The unitary entropy theorem concerns reversible two-coordinate gates. The polynomial/rational reductions characterize specified algebraic charts. A success or obstruction in one is not automatically transferable to the others.

Dense support, high cut rank, fast individual solves, correct covariance, small polynomial systems and exact small examples each address only part of the target. A candidate exact algorithm still needs complete identities for arbitrary input and size, exception handling, and a fully charged evaluator.

## Decisive next results

1. Solve or exclude the explicitly saturated 12-equation F8 regular system, then cover every excluded branch using the complete lift. Numerical residuals and finite-field infeasibility alone do not settle the complex problem.
2. For a noncommuting product candidate, prove the two sparse intertwining identities symbolically and calibrate one vector, while verifying that its architecture and total cost escape the applicable rank and entropy restrictions.
3. Implement the specified certified dyadic v9 numerical contract before claiming an end-to-end practical guarantee. A precision theorem does not certify the uploaded benchmark binary.

## Source and evidence record

The baseline remains a dated snapshot of 349 Library items and 528 canonical text contents. The 14:50 and 15:20 additions contribute respectively 50 and 58 byte-new contents relative to their declared predecessor sets. The 16:28 batch contributes 90 relative to all preceding member and top-level source hashes: 88 text/data contents, one new nested Phase17 archive stream and one compiled binary. Two other nested archives match previously supplied top-level archives and are inherited. Its 562 recursive member occurrences have 381 unique hashes, and all 714 embedded hash entries pass.

The 16:46 addition has 194 recursive member occurrences, 180 unique byte contents and 29 byte-new contents relative to the declared preceding union; all 490 embedded checksum entries pass. Its nested predecessor exactly matches the 16:28 dual-support archive.

Uploaded code and the compiled binary were not executed. Independent proof reconstructions, fresh check scripts, finite-field controls, numerical stress tests and source-reported claims are labeled separately. No publication-priority claim is made. Chat-only account coverage remains unverified.

## Navigation

- Latest determinant audit and exact/finite-field checks: additions/1646/.
- Three-branch fusion, source inventory, full proofs and checks: additions/1628/.
- Previous precision, inverse-support and Phase16 audit: additions/1520/.
- Previous jet and streaming comparison-only audit: additions/1450/.
- Baseline catalog and 528 source texts: library/.
- Earlier baseline checkpoint: checkpoint_history/baseline_CURRENT_CHECKPOINT.md.
- Earlier exact/real/Boolean corrections and route map: prior_synthesis/, boolean/, phase14/ and nonlinear/.
- Chat-only coverage limits: CONVERSATIONS.md.


## Next source batch outside this version

Six new attachments received at 19:54 UTC are assigned to a separate next-version review. They are not included as verified findings here; the completed nine-audit batch above remains unchanged.
