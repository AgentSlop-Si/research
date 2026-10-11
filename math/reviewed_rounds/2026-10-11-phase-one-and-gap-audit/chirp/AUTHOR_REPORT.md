# CHIRP: fixed phase-one sparse recognition and parity-pruned output

11 October 2026. Status: CANDIDATE; fresh same-author controls pass. Separate independent source review is required before acceptance.

## Result and inherited scope

This is a bounded extension of the independently accepted phase-zero sparse frontend and metered non-dyadic dispatcher. On dyadic inputs it tries phase zero first. If that attempt fails and N>=4, it tries the single fixed canonical phase a=1. That attempt pays for full dechirping, exact sparse recovery, synthesis back into every original raw coordinate, and all N positive-sign unnormalized DFT outputs. Two actual length-N/2 support-pruned transforms implement the nonzero-phase output. The phase schedule is explicit and fixed; no phase oracle, supplied phase hint, uncharged root/Gauss cache, or eliminant selector is used.

If both sparse attempts fail, the byte-unchanged accepted dense recognizer receives only the remaining global budget. It repeats its input, prime and root checks and its complete phase search. All those costs remain paid. NONMEMBER is returned only by that complete fallback. N=2 has no canonical phase one and skips it after one paid schedule test. Structurally eligible non-dyadic inputs retain the accepted direct dense route.

The public input/domain, output convention and caps are unchanged: exactly N,p,r,omega,x; exact built-in headers/residues; supplied prime p with N|(p−1); supplied exact-order-N omega; N>=2 and 1<=r<N. Full primality and root-order validation precede mathematical decisions. Default caps are N128/r64/32 modulus bits/2,000,000 units; hard caps are N512/r128/64 bits/20,000,000 units. Dimension eligibility does not guarantee completion. The CLI retains its 1 MiB finite-JSON cap and duplicate-key rejection. The order-2N-root curvature family, N=1 and r>=N remain outside the API.

MEMBER exposes a fully verified representation and complete DFT. LIMIT is indeterminate and exposes neither, including when the final output write cannot be paid. INVALID_INPUT and INVALID_PARAMETERS describe only checks already completed; a resource limit can prevent discovery of later invalidity. Runtime/OS exceptions and hostile object hooks retain the inherited scope and are not promised to become decision statuses.

Source SHA256: chirp_phase_one.py = 0dd2e0f54851bff04c3f6b9f5b9c29caa1ec9d9089e4df8eae7f341facf430e6. The accepted dispatcher and reference copies are pinned in SOURCE_PINS.json and unchanged. Original uploaded programs were not executed or imported.

## Exact phase-one output identity

Let N=2^m>=4, M=N/2, and omega have order N in F_p. Then p is odd and N is invertible. Define

    G(k) = sum_{j=0}^{N−1} omega^(j²+kj).

Pairing j with j+M changes the summand by omega^(M²+kM)=(-1)^k, since N divides M². Thus G(k)=0 for odd k. For k=2t, completing the square and translating j through the full residue system gives

    G(2t) = omega^(−t²) G(0).

The even formula is independent of the chosen representative of t modulo M: replacing t by t+M changes t² by 2Mt+M², a multiple of N. G(0) is computed directly by N paid table reads and N field additions. There is no square-root oracle or hidden Gauss-sum precomputation.

For x_j=omega^(j²) sum_b gamma_b omega^(bj), the positive-sign DFT equals sum_b gamma_b G(k+b). Write k=2u+delta, delta in {0,1}. Only modes b of parity delta contribute. With b=2v+delta, set h=v+delta modulo M. Then

    DFT[2u+delta] = G(0) omega^(−u²)
        * sum_h [gamma_(2v+delta) omega^(−h²)] (omega^(−2))^(uh).

Each parity map b to h is a bijection onto {0,...,M−1}; distinct recovered frequencies therefore stay distinct and nonzero weights stay nonzero. omega^(−2) has exact order M. This is precisely two sparse-input transforms of length M, followed by paid chirp scaling and interleaved output writes. The code computes only nonempty support subtrees; an empty parity emits a charged zero array. N=4 and both parities are included. No output normalization or inverse-sign convention is silently inserted.

The identity is elementary square completion and a special-case engineering integration, not a new Fourier-transform theorem or a priority claim.

## Recognition and complete verification

The fixed nonzero attempt computes y_j=x_j omega^(−j²) for all N raw coordinates. Its BM prefix, grid-root recovery and partial-fraction amplitudes use the accepted sparse method on y. The connection polynomial must have constant term one, degree equal to recovered order at most r, and exactly that many distinct grid roots. Any sparse rejection proceeds to the next allowed route, never to overall nonmembership.

The recovered modes are synthesized with the actual support-pruned length-N transform. For every j, the synthesized value is multiplied by omega^(j²) and compared to the original validated x_j. All N comparisons run, including after a mismatch. This is a direct raw-coordinate verification of the proposed nonzero-phase representation, not merely a check of its short prefix or of an internally copied dechirping. The accepted cyclic method covers wrapped 2r>N prefixes; no new N>=3r restriction is introduced.

The successful phase-zero arithmetic and ledger are unchanged. The non-dyadic direct-route ledger is unchanged. A completed phase-one candidate uses its own measured stages. Its fallback still starts the immutable complete dense reference from phase zero, without treating prior telemetry as an unchecked certificate.

## Full charged work and precise limitations

There is one cap. Every successful pay increments both its named category and stage; an unaffordable payment raises before the represented field operation or write. A fallback receives cap minus the entire completed prefix. Its aggregate ledger is the exact sum of the prefix and fallback category counts. Failed and interrupted work is retained. The new work includes the schedule test, every full dechirping multiplication/write, every rechirping multiplication and raw comparison, Gauss accumulation, the inverse-square root table, parity-support coefficients, real sparse routing/FFT arrays, chirp scaling, and zero initialization plus overwrite of the full accepted output.

The paid schedule adds one event after a phase-zero rejection. Full phase-one dechirping uses N field multiplications, N root-table reads, N index-evaluation events and N field-entry writes. The modified full synthesis adds N rechirping multiplications, N root reads and N index events to the inherited all-coordinate comparison cost.

For s recovered modes, let K(I,M) be the complete deterministic category ledger of the accepted pruned FFT on support I. The two parity supports I0,I1 have total size s. Excluding the two K ledgers, the exact new output-kernel categories are:

- phase_index_evaluations: 2N+s
- root_table_reads: 2N+s
- field_additions: N
- field_multiplications: 3N/2+s
- field_entry_writes: N/2+s
- mode_parity_tests: s
- dft_output_writes: 2N

Their unit sum is 9N+5s. The whole output cost is that sum plus K(I0,M)+K(I1,M). Fresh tests predict these category counts independently by occupied residue classes at each recursion depth, then compare them with actual metered calls. For a successful phase-one attempt, relative to the already-paid common setup and failed phase-zero attempt, the complete additional cost is one schedule unit, 4N dechirping units, the ordinary sparse recovery/synthesis ledger for y, 3N rechirping units, and the stated full output ledger. Early rejections retain only work actually executed, followed by the fully paid dense fallback.

Ignoring scalar inverse internals, the two-attempt successful sparse route uses O(N log(r+2)+r²) field additions/multiplications and O(r) inversions. The fixed number two of attempts does not introduce an uncharged phase-search factor. Implemented Fermat inversions add O(r bitlen(p)) actual field multiplications. All O(N) reading, validation, synthesis and output events are included where performed. Trial division, input binding and ordinary integer operations retain their separately stated costs. Sparse live field storage is O(N); dense fallback retains its O(N+r²) scope plus O(N) frontend arrays. These are field-cell bounds, not process-memory bounds.

The instrumentation is not a processor-instruction ledger, equal-cost machine model, complete bit-cost theorem, wall-time bound or allocation limit. It counts index-evaluation events but not the full bit cost of their Python arithmetic. Scalar assignments, loop/index/control work, dictionaries, metadata, list-object bookkeeping, JSON parsing/serialization, hashing overhead and runtime allocation are not assigned full machine costs. The Python input is already resident. New frontend array writes are counted more explicitly than in the immutable dense reference. Those qualifications matter for any comparison of summed units; actual arithmetic categories and cold timings are reported separately.

Same-cap statuses can differ from the accepted dispatcher: a new phase-one success can finish before the old dense fallback, while an extra failed phase-one attempt can consume budget previously available to fallback. Replays compare the actual remaining budget. No min(B,H), global sparse bound on dense fallback, or uniform timing improvement is asserted.

## Fresh evidence

TEST_RESULTS.json is bound to the candidate, accepted dispatcher, dense reference, checker and fresh harness hashes. It records:

- 17,618 complete decisions compared with the dense reference, accepted dispatcher and independent direct-dechirped support arithmetic. These include 3,759 complete small-field cases, 13,122 ternary-alphabet cases in F17^8, 183 random raw cases, 549 constructed cases, four adversaries and the unsupported-curvature control. Ternary enumeration is not exhaustive over F17^8.
- 672 complete cases use the new phase-one route; 1,251 use phase zero, 15,503 use actual dense fallback, and 192 route directly for non-dyadic lengths. 737 separate certificate-checker calls also pass.
- 923 full phase-one output cases compare exact direct DFT values, independently predicted complete kernel ledgers and actual active-tree occupancy. They include every coefficient vector in F5^4, all 256 supports at N=8, empty/single-parity/mixed/full and irregular larger supports through N512.
- 2,768 direct Gauss-sum coordinates verify the parity/completion identity across supplied primitive roots in seven length/field pairs.
- 3,323 every-unit end-to-end cutoffs, with no public representation/DFT on LIMIT and no overrun. 892 fallback cutoffs separately replay the exact residual dense budget.
- Eight whole-call arithmetic wrappers confirm actual add/subtract/multiply/inverse/power calls against the aggregate meter, including inverse exponent-bit work and real fallback.
- Four injected BM failures are contained by rejection/full synthesis and verified dense fallback. Invalid API/limit/dimension/prime-exhaustion and eight CLI controls pass.
- A true phase-one N512/r128 fixture passes complete direct DFT and the unchanged checker in 406,494 units. At 406,493 units, the final output write is denied and both representation and DFT are withheld.

These are same-author finite controls, not independent acceptance or formal verification.

## Cold reference comparison, including regressions

BENCHMARK_RESULTS.json contains 165 fresh subprocess samples: five runs for each of three engines on eleven fixtures. The API timer includes validation, both attempted phases, Gauss/root preparation, full output and return-ledger work. A separate timer includes process startup/imports/JSON/teardown. No prepared chirps, Gauss constants, roots or validation cache are supplied. Every engine/fixture agrees on exact decision/output digest, and repeated complete ledgers are identical.

Selected medians in this shared container, in milliseconds (candidate / accepted dispatcher / dense reference):

- Phase one N4,r1: 0.373 / 0.414 / 0.147; units 432 / 463 / 242
- Phase one N8,r2: 0.668 / 0.548 / 0.249; units 927 / 1,000 / 664
- Phase one N64,r1: 1.619 / 3.207 / 2.660; units 4,327 / 11,883 / 9,981
- Phase one N128,r4: 3.492 / 11.531 / 10.508; units 11,921 / 42,978 / 39,318
- Phase one N512,r8: 15.484 / 151.567 / 150.497; units 55,502 / 580,457 / 563,725
- Phase one N512,r128: 144.223 / 2531.873 / 2504.449; units 406,494 / 9,700,785 / 9,564,024
- Phase-two fallback N64,r1: 3.596 / 3.055 / 2.722; units 13,700 / 11,933 / 10,063
- Nonmember impulse N64,r2: 1.663 / 1.271 / 1.004; units 5,045 / 4,702 / 4,112

The N512/r8 phase-one API sample is about 9.79 times faster than the accepted dispatcher; its whole-process medians are 65.069 versus 196.308 ms. The small N4 and N8 candidate cases remain slower than the dense reference. N8 also loses to the accepted dispatcher despite fewer units. A failed extra phase regresses both counted work and observed time. Zero remains slower than the dense reference because it retains the existing sparse route. Phase-zero and non-dyadic candidate ledgers are exactly unchanged, with ordinary timing variation. These eleven fixtures are finite observations with no optimized dense FFT library comparison, production representativeness, confidence interval, universal gain or novelty claim.

## Q13/STR-Q2 scope and review gate

The latest local completed-consolidation metadata for Q13 and STR-Q2 preserves accepted proof/reference, phase-zero sparse and metered-dispatch milestones, while leaving general common-chirp min(B,H), optimized blocked/Toeplitz integration, complete production accounting, optimized FFT comparisons and full-interface historical priority open. The exact scoped records and source hash are in sources/SCOPE_SNAPSHOT.json. This task made no fresh live Sheet read and no Sheet/GitHub, manuscript or earlier Library modification.

ROW_PROPOSALS.json is evidence-only and not applied. This candidate would add just the fixed phase-one sparse/Gauss-output milestone after independent review. The next gate is source-bound review of the output identity and representative reductions, actual sparse recursion, recovery signs, original-raw verification, input/status semantics, exact ledgers, residual fallback and late withholding. General phase selection, all-phase sparse execution, broader production validation, optimized comparisons and priority remain open.
