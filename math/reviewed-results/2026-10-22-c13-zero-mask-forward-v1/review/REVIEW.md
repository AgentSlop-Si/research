# Independent review: C13 prescribed one-sided zero-mask constructor

22 October 2026 UTC. Verdict: **ACCEPT, scoped to the exact supplied-skeleton one-sided endpoint grammar.**

The candidate closes the specified prescribed-zero-mask forward-construction child gate for every admitted N>=2. It does not close C13 as a whole, unrestricted singular completion, or a historical novelty claim. The candidate RESULT.md and constructor.py identified below are accepted without a remaining mathematical correction.

## 1. Reviewed identities

Final candidate:

- RESULT.md, SHA256 f6a9d2754c3241f01f9fa54f247a5522c5c151afcd2de3ae475ac61b0dd08e85.
- constructor.py, SHA256 c2d2dc868c652edad228c430808faed70925255fc55aee3542243e096221a6af.
- check.py, SHA256 1805875a55f171868f2bfca9502911bcd7ebfff186053578eb395c93d56ad6a6.
- SOURCE_BINDINGS.json, SHA256 30390cb1964ba5b82708b909b357df5c1b6b0711fe959a6a71c5669a5753f702.
- MANIFEST.json, SHA256 25538ffa33cf3ad6343b045bf659b8586a7108ea59b51f965c2e86652336c2ab.

Every file recorded in the candidate manifest was independently size/hash-checked. REVIEWED_CANDIDATE.json records the full inventory. Administrative worksheet facts are parent-supplied context, not a fresh worksheet inspection or part of the mathematical acceptance.

The immutable inherited sources were independently retrieved from AgentSlop-Si/research at commit a8f8bc0cf82204267004df9f23d1ef02eda540b3:

- [19 October entry-oracle result](https://github.com/AgentSlop-Si/research/blob/a8f8bc0cf82204267004df9f23d1ef02eda540b3/math/finalized/2026-10-19-centered-support-entry-oracle-boundaries/c13/candidate/RESULT.md): 15021 bytes, Git blob ad949ad6a00e060d178882d73849d8c9e34874cb, SHA256 d4b2d4c5553c4cfcc9dbfc72672f714f80c548c750fab1a2adb735468c858791.
- [10 October accepted review](https://github.com/AgentSlop-Si/research/blob/a8f8bc0cf82204267004df9f23d1ef02eda540b3/math/finalized/2026-10-19-centered-support-entry-oracle-boundaries/c13/candidate/sources/c13_review.md): 7250 bytes, Git blob 7e89a84b86e31f54438993645f81d89ed481667a, SHA256 052b4155a0737109131d4d668495be161d867e209c1dea5c27717e366a4d339c.

## 2. The boundary was genuinely open

The accepted review's initial verdict and scale-identity section require all x_i,y_j nonzero and invertible branches. Its original-endpoint section explicitly withholds a singular-endpoint converse and asks for a separate forward identity. The 19 October result retains singular-mask work as open. Therefore this extension is outside the earlier theorem's asserted domain, even though its forward identity is elementary and suggested by the inherited formulas.

The accepted increment is a standard useful exact model completion, not a claim of a new difficult algebraic identity, worldwide priority, or a general solution of singular Green decomposition.

## 3. Mathematical audit

The candidate fixes legal invertible skeletons

U=D_a(I-W0)P_r0,  V=P_s0(I-W1)D_d,

with nonzero a,d, the inherited distinct base/edge slots, exact fixed structural routes, and a nonzero 1-product(w) on every prescribed cycle. The theorem admits N>=2 and only cycle grammars supplied as legal by the caller; it does not invent a singleton convention or declare every possible cycle partition legal. Invertibility alone is not substituted for the separate nonzero-base test. Zero edge weights do not erase or replace a prescribed route.

For exact zero sets Zx,Zy, the allowed branches are only

T0=U^-1D_x=P_r0^-1(I-W0)^-1D_(x/a),
T1=D_yV^-1=D_(y/d)(I-W1)^-1P_s0^-1.

Direct multiplication proves B=T0+T1 if and only if UBV=UD_y+D_xV. Only U and V are inverted, never an endpoint mask or singular branch. The different left/right permutation orders and the right-positioned diagonal in W1 are correct.

The complete matrix identity, including every actual off-support zero, is necessary. The at-most-4N supported equations are V_ij x_i+U_ij y_j=(UBV)_ij. In each affine component, tree propagation has nonzero slope alpha_v. Zero-mask coordinates are root pins; nonzero-mask coordinates are forbidden roots. All non-tree equations and unary pins are checked. Conflicting pins, an affine contradiction, a forced forbidden root, and actual finite-field exhaustion provide valid distinct negative certificates. A free component is feasible exactly when the forbidden roots do not exhaust the actual base field. The proof correctly separates arbitrary effective-field generation from Q/F_p reference enumeration, including infinite fields of positive characteristic and finite extensions.

Both masks all-zero force B=0. A single all-zero branch is permitted without relaxing the skeleton guards. Mixed masks are handled by the same exact pins/exclusions. The rank and zero-column/zero-row statements follow from multiplying a diagonal by an invertible matrix. Projective rescaling preserves masks, routes, and realized branches.

The cyclic anchor formula and backward recurrence give an O(N) field/index-operation application without dividing by an individual edge weight. It remains valid when some or all edge weights vanish. Dense basis reconstruction is separately quadratic.

## 4. Scope is strictly smaller than unrestricted two-sided singular completion

The exclusion has a concrete witness. Over Q at N=3, let P be the successor cycle, U=I-2P, and V=I with its legal fixed zero-weight cycle. Then U^-1=-(I+2P+4P^2)/7. The genuinely two-sided singular branch E00 U^-1 E11=-(2/7)E01 cannot equal U^-1D_x+D_y for any x,y: entry (0,1) forces x_1=1, whereas entry (2,1) forces x_1=0. This is a counterexample to a broader, unclaimed statement, not to the accepted theorem. The candidate includes this boundary witness correctly.

## 5. Cost and reference-code audit

The final constructor was read and checked against the proof, including preparation, actual-support detection, affine forest construction, exact zero pins, field exhaustion witnesses, plan recovery, and forward application. Two early costing issues were corrected before the accepted freeze: permutation validation/cycle traversal are linear rather than sorting per vector, and target normalization is charged separately from the 12N^2 sandwich arithmetic. Exact scalar typing rejects lossy float conversion. The final vector interface also validates length and normalizes exact integer/Fraction entries before application.

The accepted charges are at most 4N^2 target calls, 12N^2 sandwich field operations plus target normalization, O(N) sparse solve field work, conservatively O(N^2) candidate/exhaustion comparisons, O(N) auxiliary storage excluding target/dense output, O(N) per-vector application, and O(N^2) dense reconstruction. General cycle-type list comparison is separately charged O(N log N) integer comparisons. Field setup, prime validation, actual-field element generation, target setup/entry cost, encoding, and representation-sensitive bit costs are not hidden. The stated L_* bit-cost parameter is an execution-dependent intermediate-size bound, not a polynomial input-size guarantee.

The construction does not certify target invertibility. Prepared skeleton/plan objects must be valid and not caller-tampered; the target oracle must be coherent and exact. These are explicit interface assumptions, not silently checked guarantees.

## 6. Independent evidence and execution limits

Only reviewer-authored independent_check.py was executed. No candidate constructor, candidate checker, or supplied historical program was imported or run by this reviewer. The candidate's CHECK_RESULTS.json is author-reported and hash-bound; it is not misrepresented as an independent replay.

The reviewer's exact controls passed:

- 44,064 exhaustive target/mask decisions over F2 at N=3 and F3/F5 at N=2, compared with all direct forward endpoint assignments.
- 360 constructions over Q,F2,F3,F5,F7 at N=2,...,10, including 45 all-zero masks, 620 singular branch instances, 72 all-nonzero-edge cases, nontrivial endpoint permutations, and admitted multiple-cycle patterns.
- 2,160 complete basis-column reconstructions and 360 projective-gauge controls.
- 3,713 cycle-denominator cases, including zero-weight solves and singular denominators.
- Explicit actual-field exhaustion, mixed masks, all-zero/nonzero-target rejection, off-support rejection, and the two-sided scope witness under all 64 one-sided masks.

These bounded checks support, but do not replace, the all-size proof. This is an independent theorem/algorithm and static-reference-code acceptance, not a claim of production readiness or independently executed candidate tests.

## 7. Final disposition

ACCEPT the exact C13 fixed-skeleton prescribed one-sided zero-mask forward-construction child gate and its stated accounting. Preserve all inherited accepted results unchanged. General direction selection, arbitrary two-sided singular endpoints, original endpoint restrictions outside this grammar, target-invertibility requirements, application-specific integration, and attribution/primary comparison remain open. No external resource was modified during this review.
