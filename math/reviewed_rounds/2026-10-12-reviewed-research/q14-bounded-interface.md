Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: 08ca541550c0a54c866148626b5b20b66afa5fc6cd4207bc7d9c04bb215a2f7c

---

Independent review: Q14 bounded growing-fiber interface
2026-10-11 UTC

VERDICT

ACCEPT the bounded executable API over Q(zeta_N), for N in {4,8,16,32,64}, with the exact declared cap/aggregate semantics, guarded Green solve, full output or explicit rejection, cold preparation, and separately identified heavy/global transforms. This is a bounded implementation acceptance of the already accepted conservative STR-Q5 repair. It does not close Q14's full remaining-interface gate, establish a new theorem, certify an exhaustive concrete cost ledger, or promote novelty.

Final accepted candidate: Q14_Bounded_Growing_Fiber_Interface_CANDIDATE_v2_2026-10-11.zip
SHA256 df944c2044a4549931fcb213b2c39aeef6ba56f91d53ac140e11e0c7a35391a1; 66,262 bytes.
Source interface.py: 84671007daa1c90d57c5dd7788c51996c2cbb51b4f834a56e27a9756a3bd5738.
Contract: d04bbd2a6076293b39c1713f46aa2d9737f2dc06ba43eda7ce429389d405200a.
Author tests: 7c380a99cd3c32f5f58cb3e63cb8dc3d89584130e39259c9d69fb86426bbe367.

I verified the archive CRC, all 13 payload sizes/hashes, and the absence of extra payload members. V1 is retained immutably. V2 changes prose only; its implementation, tests, and author result bytes equal the tested V1 payloads. Original uploaded research programs and historical verifiers were not run. The fresh candidate was read before execution; only that candidate, its freshly authored tests, and independently written review controls were executed.

INDEPENDENT EVIDENCE

1. The author suite was run cold from the extracted frozen source. Its full FRESH_RESULTS.json is byte-identical to the supplied final report: 1,027 API cases, 428 complete exact vectors / 6,992 bins, 580 heavy transforms and 73 ordinary global fallbacks. This is a reproducibility check, not the independent oracle.
2. independent_tests.py is freshly written. Its DFT directly shifts and adds rational polynomial coefficients modulo z^(N/2)+1. It imports no author test helpers and calls no candidate arithmetic, roots, FFT, recognizer, or Green recurrence to obtain expected outputs/support. It covers dense non-rational cyclotomic coefficients as well as rational examples.
3. Independent API checks: 910 cases, 343 support accepts, 537 support rejections and 30 Green-domain controls. There are 392 complete exact DFT output comparisons / 5,232 bins, 604 aggregate cases, 516 heavy transforms, 126 complete zero-budget scans, 49 ordinary global fallbacks, and 147 separately observed field-operation/root-call counter audits.
4. Additional controls: 155 malformed API cases, 15 unsupported length controls, 40 malformed/false candidate injections, 5 changed-final-coordinate candidate checks, 15 injected resource-exception propagation checks, 5 cold-call preparation controls, 30 field arithmetic/inversion controls, and one computed nondivisor-folding counterexample.
5. tree_invariants.py independently rebuilds frontier branching levels and evaluates filter characters directly. Its 216 recognizer cases cover 1,132 frontier selections and 6,428 character/isolation checks. It checks the 2^w<=|S| property, exact one/zero filter values on the selected/other frontier cones, recovered normalized amplitudes, true support classification, and the 6 b log2 M iteration limit.

All checks pass. These finite controls do not establish all-length asymptotics or replace the accepted mathematical proof.

ALGORITHM AND SEMANTICS AUDIT

The selected frontier, finite filter expansion, consecutive samples, known-mode subtraction, and 6 b ell work cutoff match the accepted conservative discovery proof. The consecutive-sample Vandermonde injectivity is the completeness premise; there is no unconstructed RIP set or undocumented promise solver in this source. The zero cap gives an empty candidate followed by the full coordinate comparison. For nonzero cap, each emitted label/amplitude is validated, all candidate coordinates are synthesized by the pruned radix-two routine, and all M exact comparisons occur even after a mismatch. A short prefix is never the final certificate.

Cap mode rejects at the first uncertified fiber. Aggregate mode uses B=min(M/2,max(1,ceil(K0/Q))*log2 M), performs a separately labeled full transform on each failed light fiber, tests all M coefficients for zero, normalizes amplitudes by M, and stops before final synthesis if the accumulated true support exceeds K0. Each heavy fiber has actual support>B; the independent cases verify the success bound floor(K0/(B+1)) and rejection bound floor(K0/(B+1))+1. K0=0 performs the complete residual zero scan with no heavy transform. The earlier constant-average ALG-081 method stays a distinct comparator.

The synthesis identity and normalization are correct under the positive-exponent transform convention. Every returned vector contains N explicit exact elements. Accepted cap runs include N certification reads; every valid-shape raw list is read in full before support/Green decisions. Late raw-coordinate corruption and corrupted final candidate coordinates are detected. Invalid representation, budget, fallback flag, Green triple, or length is never relabeled mathematical support failure. Resource exceptions propagate rather than being converted into false heaviness evidence.

The public transform helper constructs a new Engine and root table on every call. Low-level Engine reuse intentionally accumulates its ledger and is not the cold public contract. Independent repeated public calls produce identical counters including all N root-table slots.

GREEN AUDIT

The source uses P=alpha I+beta S+gamma D^-1 and L=alpha I+beta D+gamma S, with F P=L F. It computes actual local denominators d_j=alpha+beta z^j and cyclic closure 1-product_j(-gamma/d_j), refusing zero denominators before the recurrence. The recurrence composes affine maps, closes the cycle, then scans once to recover the original input's full transform. Independent direct DFT comparisons include all supported lengths and genuinely cyclotomic parameter values.

Invertibility is not silently substituted for these guards. Alpha=beta=0,gamma=1 gives invertible P=D^-1 and L=S but zero local diagonal, and is domain-rejected. Alpha=1,beta=0,gamma=-1 fails cyclic closure. Alpha=beta=gamma=1 exercises a later zero diagonal. If fallback is explicitly requested, these valid-input guard failures produce an ordinary full FFT of the original raw input. A support rejection after forming a Green residual also falls back to the original input, never to the residual. Both behavior and separate fallback counters are verified.

ACCOUNTING CORRECTIONS AND ACCEPTED LIMITS

Two precision issues were corrected during review before final acceptance:

- Canonical coefficient scans initially appeared in abstract word allowances. The final implementation records them separately, and the contract explicitly excludes coefficient scans and representation work from the inherited abstract field/index asymptotics.
- An earlier phrase suggested all rational-polynomial work was paid. The final V2 contract now accurately identifies those lower-level counters as partial source instrumentation and allowances. They are not a complete machine-operation audit: initial polynomial copies, every unsuccessful trim comparison, integer gcd, allocation and interpreter work are not individually certified.

The 147 independent call-counter audits confirm that field additions, negations, multiplications, inversions, equality/zero tests, and root lookup events are counted when called, in their actual phases. Raw-read, comparison-read, heavy-transform, preparation and final-output obligations are separately inspected and tested. Abstract word allowances are conservative source-level bookkeeping, not measured Python instruction counts.

The inherited cap/aggregate formulas describe the accepted abstract field-element/index algorithm. They DO NOT bound the sum of all ledger counters. Even cold canonical validation and dense root-tuple construction require Theta(N^2) rational-slot work as N varies; field elements have N/2 rational coefficients, and input coefficient bit sizes and intermediate growth are unbounded. This executable is only capped at N=64. No finite-word theorem, numerical conditioning/stability contract, asymptotic physical speed, practical crossover or production-memory claim is accepted.

SOURCE PROVENANCE AND UNCHANGED FRONTIERS

The original F015 theorem is retained at a5c0da63f7761f91c26cf7662afb0ba5f7874f330db36791addde9bf6c58f045. The accepted conservative repair is retained at 787960e75967cc6e2bec564bdd72a92fc937ad853a4611408e430442eb002ff9. Their proof scopes are reused, not experimentally reproved. This source implements D_M(b)=O((b+1)^3(1+log M)^3), not the sharper original F015 Q b^2 discovery profile. F015's own accepted sharper supplied-field theorem remains unchanged. The separate missing paid uniform RIP/sample constructor belongs to the attempted sharper STR-Q5 plug-in, and must not be misdescribed as retracting F015's accepted theorem.

Direct arbitrary-length HIKP binning with complete bucket/error/randomness/cost contract is still open. The executable rejects nondyadic lengths. The independent folding test actually computes fold(e_2) and fold(S e_2) for n=3,B=2: both second Fourier bins are 1 although cyclic character covariance would demand -1. This rules out that naive nondivisor substitution only; it is not an all-length impossibility theorem. Sharper constructor, finite-word/bit/numerical, production and full-interface historical-priority obligations remain open.

ROW DISPOSITION

Use ROW_GUIDANCE.json only as a local append proposal after live stable-ID and exact-cell revalidation. The Sheet remains paused, and this review performs no external write. Record bounded independent implementation acceptance in the existing Q14/STR-Q5 views and scope notes for F015/ALG-002/ALG-081. Preserve old history and accepted mathematical scopes, the separate old constant-average comparator, and every remaining arbitrary-length/numerical/priority gap. No new theorem count, general-input sub-N-log-N claim, or novelty promotion is authorized by this result.
