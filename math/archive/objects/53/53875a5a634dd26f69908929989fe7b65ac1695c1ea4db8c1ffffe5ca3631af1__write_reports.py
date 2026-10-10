"""Render manually authored static-review notes; never interpret supplied code."""
import json,pathlib,datetime
O=pathlib.Path('fusion_phase_source_review_0408')
R={}
def note(i,role,logic,guards,cost,evidence,findings):
 R[i]={'role':role,'logic_and_correctness':logic,'guards_and_domain':guards,'charged_cost':cost,'evidence_numbers':evidence,'findings_and_limits':findings}
note(1,'Phase-14 numerical bank, Gram, and one-root regression suite',
'Lines 13-134 compare normalized FFT output, projected-input energy, known/adaptive masks, exhaustive six-bank selection, adversarial uniform energy, and odd-length degeneration. Lines 137-206 check commutators, union projections and singular/empty families. Lines 208-224 compare one-root compression/decoding against inherited implementations and a materialized FFT. These are meaningful finite numerical comparisons; lines 198-206 only check the stated rank formula algebraically, not an independently computed matrix rank.',
'Fixed seeded complex128 inputs, explicit invalid mask/budget and repeated-state tests. Output/error assertions allow tolerances and do not certify rigorous rounding bounds. Dependencies are exact-hash identified separately; inherited modules are absent from new_source_files but present inside the original archive.',
'Test-only FFT references and exhaustive combinations are intentionally outside the executor ledger. Brute fixed-pass optimum costs combinatorial enumeration of m*M banks; selected tiny case has six banks.',
[18,19,20,24,1,16],
'REGRESSION14.log records 17 earlier groups, whereas this source defines 18 including RootTableTests; TEST_PHASE14_Q.log records 18, and RUN_ALL_LOG includes the added test. Preserve both log generations. No new source execution or all-input precision certification.')
note(2,'Stationary Toeplitz and orbit-collision regression suite',
'Lines 15-25 check E mod K, numerical rank and Hermitian Toeplitz construction; 27-39 verify block factorization; 41-59 compare q=1/2 to generic Gram union and q=M to normalized FFT; 61-79 check nonorthogonality and an omitted-channel witness; 81-87 compare exact collision counts to a formula.',
'All hard-coded cases satisfy dyadic/divisibility and K>=M assumptions. This test file does not test unsupported helper dimensions. Existing audit notes a construction/helper guard omission at G=32,M=3, while supported stationary_eval validates dimensions. That dependency caveat is retained without attributing failure to the supported archived cases.',
'Dense numerical rank, Gram and FFT comparisons are verifier work. The assertion dyadic_green_scans=n*M is a proxy check, not measured runtime or a lower bound.',
[1,9,15,16,19,20],
'Numerical residual cancellation and conditioning remain distinct from exact projection identities. No general stability theorem follows from these samples.')
note(3,'Integrity-checked Phase-14 materialization helper',
'Lines 4-11 pin one archive by both byte count and SHA-256, CRC-test all members and assert an expanded-size total. Lines 12-22 reject absolute/traversal/backslash/encrypted/symlink entries, require one root, and only create missing files or compare existing identical bytes. Top-level execution would write files; this review only read it.',
'Assertions are essential and disappear under optimized Python. Existing target parent symlinks are not checked. Strong fixed archive identity substantially bounds ordinary intended use, but this is not a hardened extractor for arbitrary archives or adversarial output directories.',
'Archive hashing and CRC/decompression read the compressed/expanded bytes, then extraction rereads members; memory includes the full archive and each member. Not an FFT algorithm.',
[2,3,5],
'Original archive independently identified as 2f09f244ad60479aa4e61320ad9f6584c3ae08e3e18c447793583045a7940f04, 9,352,867 bytes. No extractor was run; original-source identity checks and archive member reads are separately documented.')
note(4,'Phase-27 audit orchestrator',
'Lines 15-29 combine exhaustive affine rank, exact positive-definite graph certificates and density/cross-ratio probes at N=32..256. Lines 30-37 construct a positive monomial-Fourier control and a negative Green circuit; 38-46 distinguish full N=16 cut enumeration from sampled higher sizes. Main writes audit.json and prints a subset.',
'Domain relies on the adjacent Phase-27 modules. Fixed seeds are reproducibility, not fresh randomness. passes_sample is correctly retained for the positive randomized equality gate; the negative necessary-condition witness is stronger than a failure to recover.',
'Affine enumeration is O(N^3) arithmetic; Bareiss is O(N^3) growing-integer work; cyclotomic histogram density O(N^3); cut enumeration is exponential at N=16 and bounded samples above it. None is a fast transform.',
[29,32,33,34,38],
'Saved sizes, affine counts, rank-two formulas and graph pivot counts reconcile. Pivot digests alone do not store full pivot sequences or independently reproduce certificates. Archived numerical/modular evidence is not a newly executed run.')
note(5,'Exact affine-rank, cyclic Green, and cyclotomic-zero helpers',
'Lines 15-44 implement permutation cycle rank; 47-97 build shifts/Hamiltonian cycles and exhaustively compare all N^2/2 affine maps. Lines 100-114 give the stated union-bound threshold. Lines 117-156 perform modular elimination and dense Green differences. Lines 159-180 use the power-of-two cyclotomic half-histogram vanishing criterion.',
'cycle_count validates a permutation, but permutation_rank_difference does not first validate q and affine_rank_audit does not validate p. direct_green requires a single Hamiltonian cycle but does not enforce it; repeated visits overwrite rather than sum. Hand counterexample: n=4,p=17,alpha=2,identity successor returns 4I, whereas (I-2I)^-1=16I. Archived callers use actual Hamiltonian cycles and the shift, so this does not invalidate their results.',
'Affine audit O(N^3) time/O(N) workspace; histogram density O(N^3); dense Green O(N^2); rank O(N^3), ignoring modular bit costs. Sorting validators add O(N log N).',
[31,32,33,38,117],
'Optional limited affine scan is explicitly nonexhaustive. Generic permutation/prime-field inputs need validation; fixed valid archived rank certificates remain separately supported. This is a conditional API correctness defect, not a discovered failing archived instance.')
note(6,'Phase-27 dense modular Green-sum cut/phase probes',
'Lines 19-27 form the weighted sum of two Hamiltonian resolvents over the fixed prime. Lines 30-54 compute complementary cut ranks, exhaustively only through N=16 or by seeded samples. Lines 63-77 evaluate one anchored 2x2 Fourier necessary cross-ratio and reject if it is not an Nth root.',
'Prime field, invertible lambda denominator, valid positive N and subset coordinates are assumed. trials=0 yields checked_cuts=0 and min_rank=N, so consumers must honor the count. The graph-gap and exceptional-lambda theorem is not tested by merely sampling one rational lambda.',
'O(N^2) matrix construction; each dense cut rank O(N^3); exhaustive binomial cut count or specified trials. The O(N) Green application claim in the docstring is not the cost of these dense diagnostic routines.',
[32,33,38],
'Archive reports all 12,870 balanced N=16 cuts (minimum 4), 80 samples at each N=32/64/128 (11/23/48), and modular exclusions. Code explicitly warns finite-field rejection is not automatically a complex equivalence proof.')
note(7,'Exact finite-instance graph-gap certificate',
'Lines 14-20 form a symmetric integer multigraph Laplacian. Lines 23-42 apply symmetric fraction-free Bareiss updates and require strictly positive pivots and exact divisions. Lines 45-63 form K=d*N*L+d*J-N*I; positive definiteness implies lambda_2(L)>1/d and the stated balanced-cut edge bound.',
'Power-of-two N>=8 and d>=1 are checked. The raw pivot function assumes square symmetric input without validating it. d=1 leaves the all-ones eigenvalue zero and therefore cannot pass, even if the orthogonal gap exceeds one; supported archived calls use d=2.',
'O(N^3) integer arithmetic, O(N^2) matrix storage; integers grow with determinant/minor bit size, so not O(N^3) unit-cost machine arithmetic. Full pivots are transient; stored digest is not an independently checkable pivot list.',
[32,33,38],
'Finite N=32,64,128,256 certificates do not establish a uniform deterministic expander family. Current review checked saved metadata/digest agreement with test literals, not the expensive pivot computations.')
note(8,'Finite-field Fourier monomial recovery gate',
'Lines 22-50 provide a validated radix-2 NTT; 58-70 batch-invert nonzero values. Lines 73-122 implement known monomial Fourier maps and recovered prediction. Lines 136-209 use first-column ratios, primitive phase differences and two transpose probes to recover permutations/gauges; 210-222 validate by random forward vectors and return passes_sample, never proved.',
'Positive power-of-two sizes and trial budgets are checked; root enforces divisibility by P-1. Correctness presumes fixed linear oracles and a consistent true transpose. seed=None is needed for the stated random-error interpretation; fixed seeds can be anticipated. trials=0 deliberately permits an unvalidated structural sample. Several low-level methods omit vector-length checks; predict checks its length.',
'O(N) root dictionary/phase work per candidate, O(N log N) predictor per validation, plus all oracle and transpose costs. Worst-case N-1 candidate columns; expected roughly two candidates only for actual Fourier permutations. Roughly five structural oracle calls excludes extra validation calls.',
[32,33,38],
'Cannot equate a low probe count with a fast DFT executor. The fixed prime supports only bounded dyadic sizes. Archive reports positive passes_sample and a two-column necessary-condition rejection for its negative circuit.')
note(9,'Nonaffine Green candidate circuit executor',
'Lines 14-25 use two recurrence passes and the cyclic denominator to solve a Green term in cycle order. Lines 35-52 prepare the denominator and reverse traversal for transpose with swapped diagonal factors. Lines 55-85 sum terms and reverse layer order for transpose; lines 88-106 create reproducible valid permutations and root-valued gauges.',
'Checks matching gauge lengths, nonresonance, and nonempty circuit. Does not check order is a permutation or input dimensions; malformed order duplicates/omissions therefore break the model. Generated orders are actual shuffled permutations. Empty GreenSum terms give zero; negative/zero layer count reaches the empty-circuit guard.',
'O(L*T*N) field operations/application for L layers,T terms, O(L*T*N) stored coefficients and O(N) intermediate workspace; root table recurrence and shuffles also charged. No inverse of a Green sum is provided.',
[32,33,38],
'Forward/transpose consistency tests and negative Fourier probes are archived. A fast candidate map is not a Fourier construction; sampled rejection does not prohibit all retuned parameters.')
note(10,'Phase-27 regression suite',
'Lines 14-46 test cycle rank via dense Green inversion only against the shift, rank-two perturbations, exact affine counts and probabilistic thresholds. Lines 49-83 check Fourier zero histograms and the density trap. Lines 86-159 test NTT, gauge recovery, corruption rejection and Green transpose. Lines 162-189 distinguish sampled cuts and exact pivot-digest controls.',
'Hard-coded valid permutations, nonzero gauges and fixed prime avoid the raw helper guard omissions. No short-cycle direct_green case, inconsistent-transpose oracle, trials=0 or invalid dimensions are covered.',
'Verifier includes O(N^3) affine/cyclotomic/rank work and exponential N=16 cut enumeration; this cannot be charged as linear candidate execution. Digests compare prior saved values rather than expose all integer pivots.',
[29,32,38],
'All 17 test names appear in the archived discovery log. Finite tests are controls, not universal identities or asymptotic complexity measurements.')
note(11,'Asymmetric two-stage separated-envelope witness',
'Lines 19-34 compute column-envelope prefix/suffix application and adjacent annihilators; 42-56 apply independent lower/upper column weights and divide by the output envelope. Lines 59-77 compare two Fourier witness columns and the stage product through local differences, then count supports/common zeros.',
'Equal lengths, n>=3, prime p, valid permutation, nonzero input/right and output/left envelopes, and a primitive Fourier root are assumed rather than validated. Gauge zip products silently truncate mismatched lengths. Supported tests generate valid inputs. Returned counts are evidence to interpret, not a standalone universal yes/no classifier.',
'Envelope application O(N), but certificate computes two dense DFTs O(N^2) modular powers. source_union repeatedly calls both full s1.apply functions inside an N-coordinate sum, adding another O(N^2) implementation cost.',
[39,40,44,47],
'Archived affine-endpoint and arbitrary-gauge controls are present. A witness for this asymmetric class must not be extended to arbitrary nonaffine Fourier endpoint reordering or unrestricted circuits.')
note(12,'Homogeneous scans and twisted bidiagonal witnesses',
'Lines 14-52 implement prefix/suffix scans, orientation and A/B intertwiners. Lines 55-89 provide permutation and finite-field Fourier helpers. Lines 92-129 build two/three-stage Fourier witness columns; 132-146 verify gauged circulant eigenvectors with a!=b and nontrivial twist.',
'Helpers assume nonempty vectors, genuine equal-size permutations, prime p and exact root order. nth_root_of_unity only asserts divisibility; primitive_root relies on primality. Scalar endpoints are rejected by witness_column/orientation-dependent helpers and handled separately in tests. Assertions can be disabled.',
'Scans/intertwiners O(N), direct DFT O(N^2) modular powers; primitive-root factoring roughly O(sqrt(p)) trial work. circulant_gauge_test explicitly creates N vectors and scan applications, O(N^2).',
[40,44,47],
'Correctly separates support/alphabet obstructions from generic sparse-butterfly circuits. Dense witness construction is not an O(N) Fourier executor.')
note(13,'Twisted, weighted and asymmetric gate tests',
'Lines 5-93 define five initial test groups for intertwiners, eigenvectors, support/alphabet obstructions and a classical FFT positive control. Lines 97-239 define six additional weighted, asymmetric, endpoint and quadratic-certificate groups. Affine endpoint phases are explicitly expanded and checked.',
'All sampled gauges are nonzero residues and roots divide the selected primes. The main guard at line 95 precedes six later tests: direct python test_twisted_gate.py discovers only the initial five because unittest.main normally exits. Import/discovery sees all eleven.',
'Finite modular tests contain quadratic DFT/eigenvector work, many seeds and dense pair checks. Positive classical FFT is restricted to fixed N=16; it protects model scope rather than prove a new fast algorithm.',
[43,44,47],
'Archived verifier explicitly invokes -m unittest -v test_twisted_gate and logs all eleven names, so the direct-invocation flaw does not invalidate that saved run. Fresh execution was not performed.')
note(14,'Twisted-gate nested regression runner',
'Lines 12-17 run subprocesses and surface failures. Lines 19-20 invoke unittest as a module, correctly discovering all eleven current tests. Lines 22-31 use a temporary extraction, reject paths escaping it, then invoke the predecessor runner. Final PASS text is fixed and assumes the invoked source versions.',
'The prior ZIP is not pinned here by a digest and expansion size/symlink/encryption are not checked by this wrapper. Path containment is checked before extractall. It executes uploaded programs if run; this review did not invoke it. The master extracted tree omits the prior ZIP, but the exact predecessor is recoverable from the preserved enclosing archive.',
'Cost is delegated suites plus complete extraction and unbounded captured stdout/stderr; no timeout. This is reproducibility infrastructure, not algorithmic arithmetic.',
[43,46,47],
'Archived log contains 11 current plus 7 predecessor plus 3 older smoke groups. Exact nested ZIP f0bcde62ec1a8fff9609a463c79025edc6ac150fd910f55ccc2cfd3cc56d885b identified inertly; no claim that all nested historical tests ran.')
note(15,'Weighted homogeneous scan extension',
'Lines 10-29 build diagonal conjugations for B_left/B_right and A so the same intertwining survives nonzero left/right gauges. Lines 32-52 use two adjacent columns, compare the Fourier side against the product side, and return support/common-zero counts and full vectors.',
'Construction asserts equal left/right lengths and ordinary nonzero truthiness, but nonzero multiples of p pass that check and fail modular inversion. Input dimensions can silently truncate through zip. n>=3 and valid permutation/root/prime are assumed. Scalar endpoint scans are explicitly rejected.',
'O(N) weighted scan/conjugation per call plus per-entry modular inversions; witness has two O(N^2) dense DFTs. Precomputation of inverses is not cached, so its field/integer costs should be included.',
[40,44,47],
'Existing finite tests use canonical nonzero residues, so unguarded modulo-zero and length inputs are potential unsupported-input failures, not archived counterexamples.')
note(16,'Coprime rough-cofactor Gaussian plan builder',
'Lines 14-38 implement a standard sieve, first sufficiently large prime, and sequential search for a cofactor avoiding smaller primes. Lines 41-59 choose M near log2(c*N), Q=M*K, Gaussian bandwidth and bucket count; assert coprime proper displacements, K>=M, oversampling and narrow support. profile exposes padding statistics.',
'N>=64,c>=4,0<alpha<1/2 are checked. Direct GaussianPlan construction bypasses create validation, so user-supplied nonpositive halfwidth/sigma2/buckets are not comprehensively rejected. Integer type assumptions and finite values are implicit. Archive uses positive defaults/explicit valid widths.',
'Sieve O(M log log M), trial cofactor search O(gap*pi(M)) divisibility operations, plus plan fields. Claimed subpolynomial padding search needs its number-theoretic bound; source loop alone is not that proof.',
[48,49,50,57,58],
'Q~4N is a padding construction; this helper does not compute a DFT. Arbitrary customized plan parameters must not inherit the default theorem without checking its inequalities.')
note(17,'Batched complete-phase summaries and exact-frame check',
'Lines 13-20 form chirp-weighted blocks and an inverse M-point FFT with correct M scaling for positive phase summaries. Lines 22-38 compare naive compression and average M separate Green decoders against a normalized full FFT. Lines 39-45 disclose remaining K-FFTs and M scans.',
'Positive m dividing q, valid state and reshape conditions are inherited rather than checked locally; m=0/empty dimensions fail. The listed cases and plan-generated m are valid. Error tolerances are finite numerical checks.',
'Batched compression O(Q log M); M decoders cost O(Q log K+Q*M), so total O(Q(log M+log K)+Q*M). The printed O(Q log Q) assumes intended M=O(log Q); it is not a uniform bound for arbitrary accepted divisors.',
[52,53,54],
'Archived four transform errors are at most 1.603e-14. This is a genuine scope qualification on the generic cost label, not a failure of archived exact-frame identities.')
note(18,'Gaussian interpolation/projection prototype',
'Lines 24-85 define validated plans, integer phase buckets and contiguous runs; 88-150 preweight centered input and implement equivalent short-FFT and direct Gaussian gridding. Lines 153-164 combine random Green rows by coordinatewise complex medians. Lines 167-215 report analytic bounds and work proxies; 230-266 add a explicitly labeled sharper theorem-candidate bound.',
'create checks N, oversample, M/K, L/H, support width, positive sigma2 and block size, but direct dataclass construction bypasses checks. Functions use complex128 and scalar exponentials; NaN/overflow/custom extreme parameters are not uniformly guarded. Fixed seeds are not adversarial randomized guarantees. The inherited projector identity and covariance theorem remain dependencies.',
'One row charges O(Q+K log K), O(N log L) short convolution plus segment/bucket overhead. Median stacks rows*N values. Quadratic exponential coefficients are generated by NumPy exp here; claimed ideal recurrence/coefficient model is distinct. work_profile is a proxy and shares a single bucket-setup charge although each row creates its own kernel cache.',
[49,50,57,58],
'Full-length FFT appears only in __main__ reference and external verifiers. Header approximation claims are idealized/theorem-dependent, not exact FFT or fixed-precision guarantees. No empirical archived failure inferred from unsupported customization.')
note(19,'Exact-frame and per-seed noninjectivity checks',
'Lines 19-41 average all M projected signals/spectra to test the identity frame. Lines 44-85 fix fewer than M states, locate a fully supported block, use an SVD null vector, undo Gaussian preweighting and compare zero measurements against a nonzero normalized DFT target.',
'Requires rows<M and a fully occupied block, but does not validate positive rows or existence before next(). Current n/rows choices satisfy these preconditions. SVD nullity and tolerances are numerical rather than exact symbolic rank proofs.',
'Frame loop costs O(Q*M+Q log K), with O(Q) running arrays; kernel check uses an rows-by-M SVD and several full Green decodes. Printed Theta(Q*M) omits potential dominant Q log K outside the intended M~log Q regime.',
[55,56],
'Saved kernel measurements are about 1e-16 and targets nonzero for N=127/257/509. The witness is selected after fixing seeds, so it refutes exact per-seed injectivity, not a per-fixed-input randomized approximation theorem.')
note(20,'Phase-4 padding/covariance/end-to-end verifier',
'Lines 18-53 independently construct a dense covariance Gram operator; 56-75 enumerate all unit slopes and beta values through the projector; 78-100 compare these and an improved bound. Lines 103-119 validate padding, and 122-143 compare seven-row estimates with FFT references for random/impulse cases.',
'Assertions encode q>=4N, divisibility, K>=M and coprime displacement assumptions. End-to-end threshold max(0.5,4*N^-1/3) is deliberately loose; it does not establish asymptotic rates. Positive customized plans are passed. Finite output checks are present.',
'Dense covariance O(M*phi(Q)*N^2) work/O(N^2) memory; projector enumeration costs approximately O(phi(Q)*Q^2). These deliberately expensive verifiers are excluded from the candidate executor. Full FFT is a reference here.',
[50,57,58],
'Saved artifact has eleven padding profiles, three exhaustive covariance cases and fourteen end-to-end cases. Agreement is numerical and fixed-size; neither exact characteristic-zero theorem nor a precision guarantee is established by these outputs alone.')
note(21,'Unequal-block recurrence Green decoder',
'Lines 34-108 validate unit chirps and balanced nonwrapping partitions and compress local phases. Lines 111-163 materialize block-rank-one maps and balanced summation/scans. Lines 166-245 implement FFT convolution and blocked exponential recurrence; 248-307 provide a direct forcing oracle and boundary weights; 310-348 decode the antiperiodic cycle using half-total seed and exclusive prefix.',
'High-level partition/state/dimension/method guards are useful. Raw recurrence with zero nodes eventually raises; raw boundary/decoder inputs need consistency beyond equal lengths. NumPy int64 index products may overflow at sufficiently large dimensions; dtype extension does not enlarge all preprocessing precision, and pairwise_sum casts to built-in complex.',
'Claimed algebraic cost O(N+(N/B)M(B)+B^2), with quadratic setup and O(B^2) Vandermonde storage plus O(N) sequence/scan arrays; FFT multiplication gives O(N log B+B^2). Direct forcing uses O(NB) work/storage. Unit sampling is capped and can raise rather than promise deterministic success.',
[59,60,61,67,68,70,71,73],
'Archived benchmark documents actual numerical instability in six of fifteen valid cases, including enormous/nonfinite results. This invalidates a blanket stable-binary64 interpretation, which the source explicitly disclaims; it does not by itself invalidate the algebraic recurrence identity.')
note(22,'Unequal-block timing/stability benchmark',
'Lines 13-24 time callbacks and convert nonfinite errors to infinity. Lines 27-51 test prime sizes and three block choices, comparing recurrence to direct forcing and a materialized reference, then record stability flags using 1e-5. Lines 52-57 write CSV and print.',
'No positive repeat guard, so repeat=0 would make min empty. The fixed main uses 2/4 repeats and valid block counts. Overflow/invalid warnings are suppressed for timing but safe_error explicitly preserves failure as infinity rather than a successful residual.',
'Timing includes recurrence and direct-forcing execution and full reference DFT; results are environment-specific best-of timings without warmup or confidence intervals. Direct-forcing oracle O(NB) can dominate.',
[68,70,71],
'Saved fifteen rows reconcile with summary: nine stable, six unstable. All measured recurrence ratios to NumPy FFT exceed 45. No practical speed advantage or universal numerical reliability follows.')
note(23,'Exact rational covariance bounds and row-budget helper',
'Lines 12-41 trial-factor integers and form displacement weights; 44-104 compute rational overlap, triangle, prime and least-prime-factor formulas. Lines 107-133 turn variance into bulk and median/union bounds.',
'overlap_variance_factor_lengths checks nonempty/sum/no-wrap but omits strictly positive individual lengths. prime closed form omits block domain; least-prime helper n=1 reaches min(empty). Row budgeting checks failure probability but not tolerance>0 or variance>=0. For per-component p in [1/4,1/2), its crude 2^r*p^((r+1)/2) bound does not decay and 2.0**rows eventually overflows before the 100000 cap. This is an accepted-parameter helper bug; archived calls have smaller p and do not demonstrate this failure.',
'Repeated trial factoring for each displacement can be expensive; rational numerator/denominator growth is charged, not constant-time. Budget loop should use a stable log-domain bound and distinguish uncertifiable parameters.',
[61,67,68,73],
'The helper docstring says smallest odd count certified by its bound, not an optimal median tail. Exact covariance results and supported archive controls remain separate from missing guards and floating overflow.')
note(24,'Unequal-block exact finite-field certificate',
'Lines 23-82 implement balanced partitions and a naive polynomial recurrence. Lines 85-147 independently form chirp projections, direct DFT, boundary recurrence and antiperiodic scan in the fixed prime; the returned passed flag follows exact equality. Lines 150-158 select forty bounded cases satisfying the root and no-wrap requirements.',
'run_case checks 2N divides P-1 but assumes positive N, valid block count and nonempty units. Root order<=0 and invalid partitions lack robust guards. Suite inputs satisfy those assumptions. Modular exponentiation of nonzero phases makes the inverse legitimate for generated data.',
'Direct reference is O(N^2) modular exponentiation/summation; naive polynomial recurrence roughly O(NB+B^2) field arithmetic plus exponentiation. This certificate deliberately does not implement fast polynomial multiplication or claim source runtime.',
[60,61,62,68,73],
'Forty saved finite cases support modular consistency only, not all lengths or a proof over complex numbers. Fixed prime is not an unbounded-size implementation.')
note(25,'Unequal-block research driver',
'Lines 18-61 provide numerical Fourier/covariance and five signal families. Lines 64-125 gather decoder and dense covariance controls; 127-147 report idealized work tradeoffs; 149-174 gather robust diagnostics using direct forcing; 176-188 attach modular certificates and aggregate counts.',
'run_all only has fixed cases; it records many numerical quantities without asserting tolerances. Maximum aggregation can hide NaN behavior in general, though archived small decoder values are finite. The robust branch uses direct O(NB) forcing, so its error diagnostics do not measure the fast recurrence stability.',
'Dense covariance O(M*phi(N)*N^2), numerical eigensolves O(N^3), and direct robust forcing O(rows*N*B), plus finite-field suites. work_proxy N log B+B^2 is a theoretical operation estimate, not the cost of this driver.',
[60,68,73],
'Archived counts 30 decoder,36 covariance,40 field,60 robust reconcile. Maximum covariance ratio 1.000000000000006 is floating roundoff at an exact bound, not a rigorous excess proof. No new runs or unconditional approximation acceptance.')
note(26,'Unequal-block regression suite',
'Lines 15-52 test partitions, recurrence/direct forcing and materialized decoder; 54-89 test covariance formulas and modular suite; 91-102 test bulk bounds and an amplification-cost inequality. Unlike the other two test modules, unittest.main follows all definitions.',
'Tests cover small/modest N and B<=16 recurrence, not large high-order instability cases. Guard/empty/negative input cases and row-budget p in [1/4,1/2) are absent. The amplification test only asserts a lower inequality if rows>0, so an inability to certify can pass silently.',
'Finite numerical/field controls include dense covariance/eigensolve work. Small test durations do not establish asymptotic executor work or stability.',
[61,68,71],
'Archived eleven test groups pass while the separate larger benchmark has six failures of its stability threshold; these are compatible evidence at different domains and must both remain visible.')
note(27,'Scoped bounded-coefficient determinant check',
'Lines 14-24 construct the unnormalized K-point Fourier matrix, use slogdet, and compare M times its log determinant with Q*log2(K)/2. The return explicitly scopes the lower-bound interpretation to independently computed unnormalized intermediate transforms and coefficients of magnitude at most one.',
'Positive integer M,K are assumed; no generic validation. This is numerical determinant evidence, not a mechanically verified circuit lower-bound proof. Free normalization/scaling or avoiding the stated intermediates changes the model.',
'O(K^2) storage/O(K^3) numerical determinant computation; the output gate count is a theoretical scoped lower bound, not the cost of this script.',
[77,78,86],
'Seven saved determinant cases agree numerically. No unrestricted FFT lower bound or obstruction to a different architecture is established here.')
note(28,'Cross-lineage Phase-4 versus joint-frame numerical check',
'Lines 15-19 extract a prior bundle and import its core/exact_batch; lines 20-38 compare chirp bases, batched summaries and averaged old decoders against the new joint collapse at four sizes. Assertions enforce small errors.',
'This runner uses extractall without its own archive identity/path checks and modifies sys.path; preexisting sys.modules entries could defeat intended dependency provenance in a reused interpreter. Intended standalone subprocess is cleaner. Inert review independently pins the nested ZIP and exact core/batch member hashes.',
'Four checks combine M old decoders O(Q*M+Q log K) with O(Q log Q) joint transforms; no full Q FFT oracle occurs in this particular runner, although other tests use one.',
[76,79,86],
'Archived maximum cross-lineage error is 1.4571e-14. Nested composite_cycle_core hash 226e18d6cbae68b5c064a5c4a0b4aa0e7762405ecbf7613c136240ae176e610e matches the direct Phase-4 dependency; exact_batch matches assigned hash. No nested program executed here.')
note(29,'Exact modular phase-frame and mixed-radix identity checks',
'Lines 11-39 trial-test primes and roots of exact order. Lines 41-83 construct arbitrary nonzero local chirps, summarize/recover the full phase frame, and compare a direct mixed-radix transform against a full modular DFT. The chosen sign convention is internally consistent and need not match NumPy signs to check this algebra.',
'Positive q,m dividing q and K>=M are asserted; q=0/1 or nonpositive m are unsupported. Prime/root search is unbounded and not an asymptotically cheap root oracle. Generated root powers and m are nonzero modulo the found prime.',
'Naive local transforms cost O(Q*M), K-transforms O(Q*K), and direct oracle O(Q^2), plus modular-power costs and prime search. This is an exact verifier, not a fast FFT implementation.',
[80,81,86],
'Ten saved finite instances report zero residuals; hashes store test-vector identities but not complete vectors. Regenerating them requires the specified algorithm/PRNG; no fresh run or all-length claim.')
note(30,'Joint complete-frame collapse and finite-population moments',
'Lines 17-59 implement chirp phases, batched summaries, their inverse and an ordinary normalized Cooley-Tukey factorization. Lines 61-88 compare against a reference and explicitly sum projectors; 90-126 exhaustively average subset errors and exhibit a missing-phase kernel; 128-153 time the collapse and save results.',
'chirp_base validates divisibility,K>=M and unit a but does not first validate positive m/q. Inverse summaries uses conjugate(base), valid because generated base has unit magnitude; arbitrary external base values need this contract. Empty subset/generic wrong shapes are not supported.',
'Fresh-input complete-frame path O(Q log M+Q log K+Q log M)=O(Q log Q), O(Q) main workspace. Diagnostic projector stack costs O(Q*M); exhaustive subset moments cost exponentially many subsets with O(M*Q) stored projections. Benchmarks time collapse after precomputed summaries.',
[77,82,86,87],
'Archived ten frame cases and eighteen finite-population s values are finite controls. Source correctly identifies its exact aggregate as classical mixed-radix structure, not a new sub-Q-log-Q FFT.')
note(31,'Measurement-only rank/posterior-variance diagnostic',
'Lines 15-54 isolate occupied padded blocks, build s phase measurements, estimate rank by SVD and project a normalized Fourier matrix onto block kernels. Lines 55-77 compare missing dimensions, posterior trace and a nonzero omitted witness.',
'Checks q>=4N,divisibility,K>=M and 1<=s<M, but requires a fully occupied block and positive N without an explicit early check. SVD threshold is numerical; distinct valid phases yield the intended ranks for archived cases. Gaussian prior and measurement-only architecture are essential.',
'Explicit N-by-N Fourier matrix O(N^2) memory/work to construct, plus block SVDs and dense projected responses. This is an offline distributional diagnostic, not the linear sketch executor.',
[77,83,86],
'Six stored cases satisfy trace=rank deficit numerically. It does not apply to an algorithm that rereads input or obtains other measurements, and does not refute a per-fixed-input randomized approximation theorem.')
note(32,'Local phase-transfer unitarity and rank gate',
'Lines 14-21 form U_M diag(unit phases) U_M^T. Since transpose of a unitary matrix is unitary, the generated transfer is unitary. Lines 23-54 check singular values and individual-block responses against normalized FFT targets, including phase/block normalization.',
'Valid chirp dimensions and index bounds are enforced via assertions/dependency. Nonempty ells/bs are assumed; empty lists fail at max/min. Error>=1 is for rank-deficient approximation to this normalized local operator, not every global algorithm.',
'Per pair dense M-matrix operations/SVD O(M^3); repeated chirp construction and Q-point reference FFTs add overhead. Sixteen pairs per archived Q are diagnostic work, separate from FFT execution cost.',
[77,84,85,86],
'Ten stored cases have unit singular values within numerical tolerance and small one-block errors. No transfer to unrestricted circuit lower bounds or global cancellation across blocks.')
note(33,'Phase-5 subprocess suite runner',
'Lines 5-20 run six named scripts sequentially from a fixed directory, record return code/timing/output tails and stop at first failure. Lines 22-24 persist results and exit nonzero for a recorded failed child.',
'Top-level code runs on import, so it must not be imported for review. No timeout, subprocess source hash pinning or exception handler for launch errors; output captured in full before retaining tails. Current fixed list is nonempty.',
'Sum of all child diagnostic costs plus process and output capture overhead. A successful script exit is not equivalent to universal mathematical validation.',
[86],
'Saved suite_results contains the six exact listed script names in order and all returncode=0. Current review checked that metadata only and did not rerun the suite.')
note(34,'Phase-28 trace/coupling audit',
'Lines 12-29 generate six fixed triples and require a nonzero trace-invariant difference plus full-signature exclusion. At N=4/8 they compare scalar-coupling polynomial specialization with the expected denominator product times trace gap; lines 30-34 save scope metadata.',
'Depends on exact phase28_synthesis/polynomial versions and their configured prime/generator. The characteristic-zero note requires valid reductions/denominators and source polynomial identity; a nonzero modular value alone without that mapping is insufficient.',
'Dense construction/inversion and invariant processing at least O(N^3); symbolic polynomial specialization can be much more expensive. No linear-time synthesis claim belongs to this driver.',
[91,93,94,95,96,117],
'Six saved trace differences were independently checked as modular subtraction; N=4/8 saved specializations agree. Dependencies are hashed but not newly full-reviewed here. Existing noncanonical-residue API caveat in synthesis is preserved and does not affect generated canonical-residue cases.')
note(35,'Saved Phase-28 Bezout certificate builder',
'Lines 8-17 request fixed N=4/8/16 exceptional-coupling certificates, assert gcd=[1] and verification_passes, and write compact coefficient JSON with printed SHA-256 and degrees.',
'Dependency returns are trusted beyond two assertions. The builder itself does not derive or independently verify coefficient provenance, nonzero leading terms or lifting conditions; those are delegated to polynomial source/proofs. Files overwrite prior certificates if run.',
'Certificate construction is offline dense/polynomial work in dependency; writing/hashing linear in serialized coefficient size. Small output size does not imply cheap synthesis.',
[93,94,97,98,99,117],
'Reviewer independently checked the three saved coefficient Bezout identities without executing this builder or its dependencies. That verifies stored arithmetic only, not all characteristic-zero premises or the defining matrix-polynomial derivation.')
note(36,'Phase-28 synthesis, polynomial and executor tests',
'Lines 7-112 define ten initial invariant/equivalence controls, including deliberate inconclusive repeated signatures and a dense positive outer-factor construction. Lines 116-206 define seven polynomial, positivity, Bezout, linear executor and interpolation controls. All use bounded finite fields or a finite float positivity illustration.',
'Line114 unittest.main precedes seven later tests, so direct script invocation runs only ten, whereas discovery imports all seventeen. The runbook uses discovery and its log lists all seventeen. Tests generate canonical residues and do not cover the documented raw-zero representation bug in equivalence_test.',
'Dense matrices/inversions and polynomial/interpolation checks are offline work; the executor test compares to dense multiplication and does not charge coefficient preparation or claim cheap inverse.',
[91,94,102,115,117],
'The direct-invocation limitation is real but does not invalidate archived discovery results. Fixed N=4/8/16 all-coupling claims have additional lifting/degree premises; N=32/64/128 fixed-coupling vetoes are not all-coupling certificates.')
note(37,'Saved Bezout arithmetic verifier',
'Lines 9-19 load three coefficient files, require the expected size/prime and degree metadata, and verify U*P1+V*P2=[1] using dependency arithmetic. It prints current hashes rather than comparing to expected trusted hashes.',
'Asserts nonzero_reduced_leading_coeffs flag rather than recomputing it, and it does not reconstruct defining polynomials or validate removed denominator factors/characteristic-zero degrees. Thus arbitrary internally consistent coefficient data could pass this arithmetic check without being the intended matrix certificate.',
'Naive polynomial multiplication quadratic in degrees, plus JSON reading/hashing. Independent arithmetic verification is substantially less than full matrix-polynomial construction, but not complete source/proof validation.',
[91,93,94,97,98,99,117],
'Reviewer-authored coefficient check confirms all three actual saved identities and leading residues. Provenance still relies on the recorded exact source hashes and prior independent polynomial-identification evidence; no new dependency execution occurred.')
note(38,'Local annihilator and window-rank gate library',
'Lines 17-138 supply modular rank/determinant/nullspace, true permutation convention and bit reversal. Lines 141-189 implement O(N) separated-generator scans and two-sided annihilator bases, including zero generators. Lines 201-250 use a Cauchy-Binet Casoratian degree bound to find a two-stage witness for N>=24. Lines 253-315 minimize ordering defect and compare projected three-stage ranks for natural consecutive Fourier endpoints.',
'Assumes prime p, primitive root, correct stage-array lengths, genuine permutations and valid window coordinates; many checks are asserts. Raw matrix-vector zip silently truncates dimensions. Casoratian helper assumes nonempty independent rows of suitable width. Correct witness scope explicitly needs natural-order endpoints; bit-reversed endpoints cannot inherit a full Vandermonde minor claim.',
'Stage application O(N) field work; dense DFT witness O(N^2) modular powers. General Casoratian is binomial in width/rank. Window-pair search O((N-W+1)^2 * W log W) due to repeated sorts/binary searches, plus O(NW+W^3) projected-rank work. Fixed 5x3 two-stage determinant work is constant-sized.',
[103,105,107,110,113,114,115,117],
'Saved finite witnesses support the scoped gate; absence of a three-stage violating window is inconclusive. Literal sum may include a trivial extra addition beyond the straight-line 5N-1 addition schedule, as the earlier audit records. No unrestricted FFT lower bound.')
note(39,'Dense independent three-stage reconstruction check',
'Lines 9-25 build explicit permutation matrices and the full product S3*P2*S2*P1*S1, avoiding the fast scan path. Lines 26-37 form annihilator-compressed Fourier/product matrices, compare ranks and conditionally assert exclusion.',
'Uses the same rank/nullspace/gate helpers and therefore is independent of scan application, not entirely independent of all arithmetic/logic. Fixed valid dimensions/prime/layouts avoid generic guard omissions. It does not require every layout to be excluded.',
'Dense matrix construction/storage O(N^2), multiplication O(N^3), window search and small compressed rank work. Nine fixed cases are offline controls.',
[105,107,110],
'Archived nine cases have rF=4 and varied rM/defect; bitrev/bitrev can have small observed product rank despite an inconclusive structural bound. Do not turn that observation into a uniform exclusion theorem.')
note(40,'Local-annihilator experiment generator',
'Lines 6-28 collect seven finite two-stage witnesses and 76 layout/width entries. Lines 30-39 additionally and unconditionally produce bitrev_all_widths for N=16/32/64. Lines 41-60 collect six random-layout sampling records and three explicit three-stage rank checks, then write EXPERIMENT_RESULTS.json.',
'Fixed cases and seeds reproduce a bounded exploration. Top-level loops execute on import. A sampled layout fraction is not a probability theorem and a no-violation result is not factorization existence.',
'Repeated quadratic window-pair scans with O(W log W) each, further summed over all widths in the added sweep; has a coarse O(N^4 log N) bound. Exact Fourier probes are dense; no linear-time exploration claim.',
[103,104,112],
'ACTUAL SAVED-EVIDENCE GAP: archived EXPERIMENT_RESULTS.json lacks bitrev_all_widths despite this source unconditionally generating it. Both exact source and output hashes match the co-packaged SHA manifest. The JSON cannot be the complete unmodified output of this source version. Existing seven witnesses/76 entries/six samples/three ranks are retained, but no archived evidence for the added all-width sweep is credited.')
note(41,'Local-annihilator and window-gate regression suite',
'Lines 12-58 test roots/rank, degenerate nullspaces, Casoratian identity/root count and scan/dense agreement. Lines 60-123 test locality, two-stage witnesses, conditional three-stage ranks and exact permutation counts. Lines 125-159 explicitly protect against nonaffine endpoint rank overclaims and test subset expectation plus rank-two-middle generalization.',
'Fixed valid fields/roots/permutations and substantial zero-generator coverage. Boundary N=24 explicitly tested. APIs are not hardened against invalid lengths/composite moduli. The endpoint correction is a substantive negative control and cannot be discarded.',
'Dense modular matrices, determinant checks, window enumeration and 120^2 subset pairs are verifier costs. Eleven groups are bounded tests, not exhaustive coefficients/permutations for growing N.',
[110,113,115,117],
'Archived eleven groups pass. No early unittest main issue here: it is after all tests. Preserves the source warning that bit reversal on both Fourier endpoints destroys the consecutive-minor shortcut.')
note(42,'Archive hash/CRC verifier',
'Lines 4-13 read a manifest and assert every listed file has the claimed hash; lines 14-16 CRC-test the predecessor ZIP; lines 17-18 print counts. This checks bytes and ZIP integrity only, not supplied program correctness or theorem validity.',
'Manifest is neither authenticated nor checked for complete expected membership; empty manifest vacuously passes file loop. Joined paths are not contained under root, and asserts disappear under -O. Reads whole files into memory. Intended co-packaged manifest has concrete entries.',
'O(total listed bytes + decompressed ZIP bytes), memory bounded by largest read file plus zip decompression buffers. No code execution in this verifier itself, although current review did not run it.',
[112,118],
'Independent reviewer manifest checks found all available listed files match; inherited twisted ZIP cb918c3f72b57a2734d0c1953f2dfbde63d9bf38d869047ed6e3d93a3ab7f0bc was hashed directly. A matching manifest does not fix the source/output completeness gap in run_experiments.')
note(43,'Historical multistage archive extraction/comparison helper',
'Lines 4-8 hash the then-current master, 10-24 extract selected ZIPs with size/path/symlink/no-overwrite assertions and read-only chmod, 25-31 compare embedded manifests, and 32-34 save summary/data. master_matches means byte equality in that captured master only.',
'Hard-coded historical paths; root.mkdir intentionally fails if rerun into an existing target. No backslash/encryption/parent-symlink guard; embedded manifest paths are not contained. Assertions and all(empty) can overstate success if inputs/manifests absent. Safe only within the intended trusted local research setup, not arbitrary archives.',
'Hashes every master file and stores match paths; cost O(total master bytes+archive expanded bytes), memory largest file/member and records. It would mutate file modes/write extraction if executed, so it was not run.',
[118,117],
'Saved comparison includes unique_member_hash_count and unique_byte_new_hash_count beyond this literal script output, consistent with postprocessing; provenance cannot be reduced to the shown script alone. Historical newness relative to an old master is not current exact-hash coverage credit.')
note(44,'Polyphase exact-collapse timing benchmark',
'Lines 14-35 compare joint and collapsed outputs with normalized NumPy FFT at five sizes; first two also use naive complete frame. medtime repeats callbacks and returns median. Main writes JSON and union-key CSV.',
'Only fixed valid sizes tested; no accuracy assertions or finite-value checks in the benchmark, so stored errors need inspection. reps=0 would yield a NaN median. Results depend on the exact adjacent polyphase_exact module, hashed separately but not newly reviewed here.',
'Timings include each whole dependency call, whereas previous joint-collapse benchmark starts from precomputed summaries. Different timing boundaries must not be compared as like-for-like. All methods retain O(Q log Q) or slower complete-frame work.',
[128,130,131,132],
'Saved five errors are around 1e-15 and all joint/collapsed times are slower than NumPy FFT. No practical speedup claim is warranted. Output values remain archived diagnostics, not a fresh benchmark.')
note(45,'Exact modular polyphase-collapse certificate',
'Lines 16-57 define finite-field roots/phases/DFT and all-phase summaries; 60-87 perform K-point transforms, invert local phase channels, shift indices by a*t and assemble final mixed-radix outputs; 94-115 compare basis/dense vectors to direct DFT.',
'Checks divisibility by m and supported root orders but omits positive dimensions, input length and inverse-zero guards; inv(0) returns zero. Generated phases and valid M are nonzero in the fixed field. Arbitrary low-level inputs cannot inherit that guarantee.',
'Naive modular transforms and repeated root/power computation cost O(Q*K+Q*M) plus O(Q^2) direct references per test vector; this is a certificate, not the fast floating executor or unbounded-N arithmetic model.',
[128,133,134],
'Archived Q=56 and119 check every basis vector and six dense vectors. Q=136 and238 check only first24 basis vectors plus six dense vectors; status exact means exact modular arithmetic on these tests, not exhaustive all-input verification at those latter sizes.')
rows=json.loads((O/'INPUT_ROWS.json').read_text());deps=json.loads((O/'DEPENDENCIES.json').read_text());ev=json.loads((O/'EVIDENCE_MANIFEST.json').read_text())
assert set(R)==set(range(1,46))
reports=[]
for row in rows:
 i=row['source_index'];r=R[i]
 report={'source_index':i,'name':pathlib.Path(row['representative_path']).name,'sha256':row['sha256'],'representative_path':row['representative_path'],'source_snapshot':row['snapshot'],'source_bytes':row['size_bytes'],'source_lines':row['source_lines'],'read_ranges':[[1,row['source_lines']]],'inspection_method':'Complete line-numbered text inspection; no source execution, importing, compilation, AST parsing, or synthesized execution of source.',**r}
 report['dependencies']=[d for d in deps if d['source_index']==i]
 report['stored_evidence']=[ev[n-1] for n in r['evidence_numbers']]
 report['global_boundary']='Static source coverage is not theorem acceptance, successful current execution, provenance proof of a historical run, full dependency closure, or completion of all research checks.'
 report['report_path']=f'reports/{i:02d}_{row["sha256"][:12]}.md'
 text=f'# Source {i:02d}: {report["name"]}\n\nSHA-256: `{row["sha256"]}`\n\nPath: `{row["representative_path"]}`\n\nAll {row["source_lines"]} lines ({row["size_bytes"]:,} bytes) were read. Source execution/import/compile/AST parsing: none.\n'
 for key,title in [('role','Role'),('logic_and_correctness','Complete logic review'),('guards_and_domain','Guards and domain'),('charged_cost','Charged costs'),('findings_and_limits','Findings and evidence limits')]:text+=f'\n## {title}\n\n{report[key]}\n'
 text+='\n## Exact dependencies\n\n'
 for d in report['dependencies']:
  cs=d['candidates'];text+='- '+d['module']+': '+('; '.join(c['sha256']+' ('+c['resolution']+')' for c in cs) if cs else 'standard-library/external dependency; no source version pinned here')+'\n'
 text+='\n## Preserved stored evidence\n\n'+'\n'.join('- `'+e['snapshot']+'` SHA-256 `'+e['sha256']+'` (original `'+e['path']+'`)' for e in report['stored_evidence'])+'\n\n'+report['global_boundary']+'\n'
 (O/report['report_path']).write_text(text);reports.append(report)
(O/'SOURCE_REPORTS.json').write_text(json.dumps(reports,indent=2))
print('Wrote',len(reports),'full reports; prose characters',sum(sum(len(str(r[k])) for k in ['role','logic_and_correctness','guards_and_domain','charged_cost','findings_and_limits']) for r in reports))
