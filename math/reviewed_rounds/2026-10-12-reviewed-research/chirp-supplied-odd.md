Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: 83a083cc1d217b30d3fbd2631a3af3fd4db5c2498e9e1d0d04654c067b1b52ff

---

# Independent review: CHIRP supplied odd-phase candidate

11 October 2026 UTC. Decision: **ACCEPT at the stated bounded supplied-candidate scope**.

No mathematical, executable, or documentation repair is required for the reviewed milestone. This acceptance applies to `chirp_fixed_odd.py` at SHA-256 `0f256cb7b35e3bc24bb2eb22fd7ddf1c179ec8801ed68165c440f88267ed7577`, in the 83,500-byte candidate archive at SHA-256 `49dd00a39f3cddaa83881ba9121ab233bc2d739a2e18a80e52418511c41a8464`. It accepts the general dyadic odd-phase Gauss/permutation lemma and the bounded implementation that tries phase zero, then one externally supplied canonical odd phase, then the complete residual-budget dense reference.

It does not accept unknown-phase discovery, even nonzero phase execution, an all-phase sparse algorithm, a global min(B,H) bound, optimized blocked/Toeplitz integration, a universal FFT improvement, optimized-library timing superiority, production certification, or historical priority. Candidate acquisition remains external and may be wrong. Runtime assurance strings and the original packet retain their candidate labels because reviewed sources were kept immutable; this separate verdict records their scoped acceptance.

## Source binding and independence

The ZIP CRC, exact manifest coverage, all 38 payload hashes and lengths, agreement with the supplied unpacked files, and all eight source pins were verified before and after the independent run. The accepted phase-one implementation is SHA-256 `0dd2e0f54851bff04c3f6b9f5b9c29caa1ec9d9089e4df8eae7f341facf430e6`. Its independent acceptance verdict and report were read and matched their archived copies. The dense reference and separate checker remain byte-identical at hashes `7d263f616526bd1123658771afc73bb44fc15282ef8ee0131e48ade0b59d18b7` and `556337c6bc1f4215d1782f82fb63bfd67771152a442af1688bf91080f763699f`.

The reviewer read the report and complete source delta, derived the formulas, and wrote fresh direct-transform, occupied-residue-class, interface, and interruption controls before reading the author's test harness. The author's suite was then replayed in a review-owned copy. Its source-bound result equals the archived result apart from elapsed time. Original uploaded research programs were neither executed nor imported; only the supplied fresh implementation and expressly permitted accepted references were run. No Sheet, GitHub, manuscript, Library original, or author packet was modified. This is an independent project review, not external peer review or machine-checked formal proof.

## Mathematical proof and proof-to-code alignment

Let N=2^m, m>=2, M=N/2, let p be prime with N dividing p-1, and let omega have exact order N. Hence p is odd, omega^M=-1, and N divides M^2. Let a be odd and alpha=a^-1 modulo N. Pairing j with j+M in

    G_a(k) = sum_(j mod N) omega^(a*j^2+k*j)

changes the exponent by a*N*j+a*M^2+k*M, leaving the multiplier (-1)^k. Thus G_a(k)=0 when k is odd. For k=2t,

    a*(j+alpha*t)^2 = a*j^2+2*t*j+alpha*t^2 (mod N).

Translation is a permutation, so G_a(2t)=G_a(0)*omega^(-alpha*t^2). Replacing t by t+M leaves its square unchanged modulo N. This includes N=4 and negative or wrapped representatives. No Gauss square-root convention is needed. The implementation obtains G_a(0) by N actual paid additions and table reads; it does not assume a free value or divide by it.

For verified x_j=omega^(a*j^2) sum_b gamma_b*omega^(b*j), positive-sign unnormalized DFT linearity gives sum_b gamma_b*G_a(k+b). For k=2u+delta only b with parity delta survives. Put

    h_b=(b+delta)/2 mod M,
    q_b=alpha*h_b mod M,
    c_b=gamma_b*omega^(-alpha*h_b^2),
    zeta=omega^(-2).

Then

    DFT(x)[2u+delta] = G_a(0)*omega^(-alpha*u^2)
        * sum_(b parity delta) c_b*zeta^(u*q_b).

The map b to h_b is a bijection in each parity, including b=N-1,delta=1,h_b=0. Since alpha is odd, multiplication by alpha permutes residues modulo M. The q_b are therefore distinct and the c_b remain nonzero. Zeta has exact order M. This proves that the actual two sparse-support M-transforms have precisely the required inputs and root, with no concealed duplicate-support cancellation. Empty parity supports correctly produce paid zero outputs. The sign, parity, index wrap, and final interleaving agree with the source.

The inverse must be taken modulo N for the chirp factors. Modulo M suffices only for q_b. At N=16,p=97,omega=8,a=5, the correct inverse is 13 whereas the half-modulus inverse is 5; direct G_a(2) is 59, while that incorrect completion factor gives 38. Additional independent two-mode adversaries detect both this wrong inverse and omission of the support permutation.

The bit-lifting inverse starts at inverse=1 modulo 2. At modulus bit, adding bit to inverse toggles the next bit of a*inverse because a is odd, without altering lower bits. Doubling bit maintains inverse*a=1 modulo the enlarged modulus. Its final modular verification is paid. There are 2 initializations, m loop tests, m-1 product-bit tests, m-1 doublings, popcount(alpha)-1 additions, and one verification: exactly 3m+popcount(alpha) named events. The invariant and event count hold for every odd residue through the hard N=512 cap, independently of the narrower public canonical phase range.

## Recognition, validation, and compatibility

The public problem fields remain exactly N,p,r,omega,x. The selector is a keyword-only configuration parameter and must be an exact built-in odd integer in [1,256), with a<N/2 additionally required on eligible dyadic N>=4. Validation happens before a phase-zero shortcut, raw reads, or sparse decision. It is paid even on N=2 and non-dyadic inputs where the selector is unused. The added validation totals six events on eligible dyadic inputs, five at N=2, and four on the direct non-dyadic route. Invalidity discovery remains budget-dependent, and selector invalidity can precede input invalidity.

The unchanged CLI uses the default selector 1 and does not accept the packet's separately labelled API request records as its input schema. Eight inherited definitions have identical ASTs. At a=1, independent comparisons preserve mathematical results and every original event category; the only additions are selector validation and, on odd-phase success, the paid modular-inverse and support-permutation events. Source compatibility here means the documented input/API/CLI and mathematical behavior, not identical telemetry labels or equal decisions under the same finite cap.

The code validates all raw entries, primality, and exact root order before mathematical success. It dechirps all N coordinates and runs the accepted cyclic BM/grid-root/partial-fraction method. Wrapped 2r>N prefixes remain valid under the accepted cyclic recovery theorem. It then synthesizes all N recovered coordinates, rechirps with the supplied a, and compares against the original validated x. Independent first-coordinate and last-coordinate corruption controls confirm all N comparisons occur even after a mismatch. A prefix or dechirped intermediate cannot alone produce MEMBER.

Sparse failure is never overall NONMEMBER. Only the unchanged complete dense reference may reject the full family, after restarting its canonical phase schedule with precisely the residual cap. Wrong candidates, every failed attempt, and repeated reference validation/setup remain charged. A global LIMIT is indeterminate and returns neither representation nor DFT, including a denial at the last output write. Hostile Python hooks, OS/runtime failure, and inputs outside the declared family remain outside the inherited guarantee.

## Cost and storage contract

Write K(Q,M) for the complete accepted pruned-FFT event ledger on the actual permuted support. Excluding the two K ledgers and inverse, the output kernel incurs:

- 2N+s phase-index events and 2N+s root reads
- N field additions and 3N/2+s field products
- N/2+s field-entry writes
- s parity tests and s support-permutation events
- 2N DFT writes, including zero initialization and final overwrites

Thus the exact kernel work is

    3*log2(N)+popcount(alpha)+9N+6s+|K(Q0,M)|+|K(Q1,M)|.

The independent predictor counts occupied low-bit residue classes at each depth, rather than reproducing the implementation's recursion. It accounts for active nodes, support routes, empty outputs, zero initialization, overwrites, twiddles, and one- versus two-sided combines category by category. Odd multiplication may change single-child placement, so the actual q support is used; an unchanged FFT ledger is not presumed for a!=1.

A successful supplied-phase route also pays its schedule event, 4N dechirping events, the entire recovery/synthesis ledger, and 3N extra rechirping events, as well as common setup and the failed phase-zero attempt. All operations in the new claimed categories are preceded by payment. Actual field-call auditing includes Fermat-inverse multiplication and power-bit work and includes dense fallback.

The accepted fixed-two-attempt arithmetic scope is O(N log(r+2)+r^2) excluding scalar-inverse internals, with O(r) inversions; their implementation adds O(r log p) field products. The integer inverse adds O(log N) named events. Sparse live field storage is O(N), and retained frontend arrays are included when stating the dense fallback's O(N+r^2) field-cell scope.

These are named event and field-cell contracts, not complete Python-instruction, integer-bit, process-memory, or wall-clock costs. The report explicitly excludes unmetered control/object/JSON/hash overhead and does not equate frontend and dense-reference write detail. A sequence of q supplied candidates would require charging all q attempts; this packet supplies no such enumerator and no cheap candidate-acquisition theorem.

## Fresh executable evidence

All reviewer-owned controls pass:

- 4,571 complete decisions: exhaustive F5^4 with both primitive roots and r=1,2,3; binary-alphabet N=8 cases; all canonical odd phases in selected N=8,16,32 constructed, corrupted, and random cases; direct non-dyadic/N=2 controls; a wrapped-prefix case; and a reviewer-owned N=512 hard-boundary case.
- Routes: 631 supplied odd-phase successes, 1,007 phase-zero successes, 2,897 dense fallbacks, and 36 direct non-dyadic routes. Direct support calculations are the decision oracle on the small/medium cases; direct synthesis/DFT and a separate checker verify the known-member hard-boundary case.
- 10,470 independently computed MEMBER output coordinates and 653 sampled separate-checker decisions, plus a separate hard-boundary checker call.
- 4,400 full output-kernel and exact category-ledger cases, covering every support at N=4 and N=8, every primitive root and every odd phase there, plus empty, endpoint, parity-only, full, and irregular supports through N=512. These comprise 73,344 output coordinates.
- 12,576 direct Gauss coordinates and 37,728 representative shifts; all 510 odd inverses through N=512; 14,591 every-unit internal inverse cutoffs.
- 4,614 end-to-end every-unit cutoffs, including exact completion caps, with full aggregate-category prefix equality and no partial mathematical output. These include a true a=5,N=16 inverse/permutation route with two lift additions.
- 2,933 complete-run exact residual replays and 823 cutoff residual replays; 115 exact a=1 ledger-specialization controls; three actual field-call audits; invalid selectors/inputs; and eight unchanged inherited AST definitions.
- Independent raw-tail and first-mismatch controls reject safely after all N comparisons. Wrong half-modulus inverse and omitted-permutation formulas produce explicit wrong-output witnesses.

The independent N=512,p=7681,omega=62,a=255,r=128 irregular-support fixture completes in 405,218 named units and withholds both witness and DFT at 405,217, at `odd_phase.output_writes`. This is a different fixture from the author's 407,055-unit example; both pass. It is not a claimed speed comparison.

The full same-author suite was separately replayed successfully, reproducing its 5,140 decisions, 1,489 kernel-ledger cases, 510 inverses, 17,696 Gauss coordinates, 4,701 cutoffs, 852 residual replays, malformed-input/CLI controls, and author N=512 boundary. These replay counts are separate from the reviewer-owned evidence and are not added together as independent coverage.

## Conclusion and handoff

The supplied-fixed-odd-candidate sparse milestone and reusable odd-phase output lemma may be recorded as accepted at the exact source hash above. Candidate selection, even-phase execution, global dispatch, production/bit accounting, optimized comparisons, and historical priority remain open. No live project status or publication was changed by this review.
