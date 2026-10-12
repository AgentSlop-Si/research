# Independent scoped acceptance: Q07 ternary raw q-Weyl executor

12 October 2026. Verdict: ACCEPT_BOUNDED_TERNARY_EXACT_REFERENCE_INTERFACE.

## Exact accepted object and boundary

Candidate archive: Q07_Ternary_Raw_Weyl_Extension_CANDIDATE_2026-10-12.zip, SHA256 3a42168c30d80391548a12f55c8a3c05f3a80afb182b1d519c3471286600014c. Source src/ternary_raw_weyl.py: 8ac1fbf964cb2523fe39cdf11ad54569295886e1daafef64984354623f374cab. The archive CRC, exact member set, all 18 manifest payloads, and seven independently compared predecessor/source pins pass. The tested code and author tests were inspected before execution. Their sealed bytes match the inspected fresh source. All frozen payloads remain unchanged after both replays.

Accepted only for N in {3,9,27,81,243,729}; supplied prime N<p<=65537 with N dividing p-1; supplied and verified primitive q; canonical raw residues; 1<=t<=floor(N/2); at most 16 fresh vectors; supplied canonical nonzero a,b when action is requested. These are the stated public API boundaries. Unsupported domains raise DomainError and are not mathematical sparse rejections. The previously accepted dyadic executor was read as inert evidence and was not executed or replaced.

The original raw-mode interface target requires raw all-coordinate recognition/rejection, all positive-sign unnormalized outputs, paid sparse scatter, separately charged O(N(s+1)) action, late/degenerate cases, and preparation/fallback auditing. This acceptance is an additional bounded implementation of that target. It is not a closure of unrestricted fields/lengths or a new generic FFT result.

## Independent evidence

The independent verifier is new code and imports only the exact candidate source. Its expected Fourier outputs use direct field character sums, and membership is decided by the number of nonzero entries of that independently computed complete Fourier vector. Its operator oracle constructs each dense antidiagonal coefficient from the raw Fourier vector, then performs a dense matrix-vector product. Neither expected output calls candidate BM, residue recovery, FFT, scatter, or operator routines. The verifier does not import author helpers.

The passed independent suite contains:

- 2,559 raw input/cap cases: 102 acceptances and 2,457 rejections; paired fft/none policies on every case.
- 53,673 complete DFT coordinates and 56,082 operator coordinates across 198 fresh vectors.
- Every raw vector in F7^3 (343 cases), and every binary length-nine raw vector at every legal cap (2,048 cases).
- Structured, undersized-cap, randomized, zero, impulse and cancellation cases through N=729 and s=floor(N/2), multiple primitive-root orientations, repeated/off-grid poles, and maximal J=16 batches on accepted zero and rejected final impulses.
- 5,945 exact sparse-transform censuses based on occupied residue classes, independent of the candidate recursion.
- 2,559 observed field-call and exact cold-preparation audits; 78 exact accepted-action count audits.
- 38 strict domain refusals and explicit detection of a reversed transform orientation, corrupted last synthesized coordinate, and missing output-write count.
- Cold repeat and returned-result mutation isolation.

All seven reachable observed outcomes are covered: accepted modes, accepted zero, prefix recurrence exceeds cap, connection degree defect, non-distinct/non-grid roots, full input mismatch, and zero-prefix late nonzero. Defensive zero-residue/zero-amplitude branches were inspected, not claimed dynamically reached.

Separately, the exact sealed author suite cold-replays byte-identically: 4,878 cases, 67,602 DFT coordinates, 89,472 operator coordinates, 55 domain refusals and five proper-order refusals. That replay includes exact sparse-polynomial BM trace predictions, high-prime boundary cases, first s-1 cancelled moments, and further kernels and fallback action ledgers. Its evidence is kept separate from the independent totals. An initial independent-harness fixture mistakenly requested cap 2 at N=3; the API correctly refused it. The harness was corrected to cap at floor(N/2), then rerun from the start. No candidate change was needed.

## Proof-to-code assessment

On a power of three, q^N=1 and q^(N/3)!=1 prove exact order N. Cold bounded trial division proves p prime; no root/field discovery is silently assumed. The supplied table is rebuilt every call.

For true s<=t grid modes, the leading moment Hankel matrix factors as V diag(gamma) V^T and is nonsingular. Standard BM on 2t samples thus recovers the degree-s connection, including early cancellations. Roots are found by an explicitly paid evaluation at every allowed grid point, not a free root solver. A degree-r polynomial with exactly r distinct grid roots has precisely the allowed simple roots. The residue identity gamma=-lambda A(lambda^-1)/C'(lambda^-1) has the correct sign. Every candidate coordinate is then synthesized and compared; a misleading prefix is insufficient. At odd maximal cap the final raw coordinate lies outside the prefix and remains included in the complete verification.

The new ternary kernel obeys the positive DFT decomposition A0(k mod m)+w^k A1(k mod m)+w^(2k) A2(k mod m), with two products and additions for each explicit combined output. Both child-zero arrays and active outputs are charged. It supplies the length-dependent argument absent from the earlier dyadic restriction.

Orthogonality places the unnormalized output N gamma_u at k=-u. Expanding diag(a) F diag(c) F diag(b) gives N a_i sum_u gamma_u (b*x)_{-i-u}. The implementation and dense independent oracle agree on that same-sign target; the second Fourier factor is never replaced by an inverse.

Rejected valid inputs retain every completed recognition stage. The fft policy adds the raw transform and two positive transforms per fresh vector; none returns no output arrays. Those routes have identical recognition ledgers. Malformed requests never enter the mathematical rejection/fallback contract.

## Costs and limits

For occupied residue counts a_d modulo 3^d, the independent census reconstructs C=sum_d a_d N/3^d and I=sum_d a_d. It checks 1+3I nodes, h log_3(N) partition records, h occupied leaves, C initializations and output writes, 2C products/additions, and N-h empty-child writes (the h=0 case has one node and N zero writes). Since a_d<=min(3^d,h), this proves the stated O(N(1+log(h+1))) bound. Partition traffic satisfies hL<=C.

Cold multiplication counts are N-1+mu(N)+mu(N/3), with mu(e)=bitlength(e)-1+popcount(e). Root checks, complete table writes, and floor(sqrt(p))-1 trial divisions are independently checked. The observed field-call wrappers also verify phase attribution rather than trusting self-reported totals alone.

Accepted scatter pays N zero initializations and s multiplications/writes. Each fresh action pays Ns additions/terms, N(s+3) multiplications, N b*x writes and N final output writes, including zero support. This preserves O(N(s+1)), not a growing-support O(N log s) shortcut. The explicit arrays and depth-first ternary storage support O(N(1+J)) field-word space.

The split-model bound is O(sqrt(p)+N log(t+2)+t^2+JN(s+1)) plus O(t) scalar inversions. Their actual modular powering adds O(t log p) multiplications. Inversion calls are annotations and are not added again to their included powering products. Rejected fallback adds its transform/action cost on top of failed recognition.

The counters are semantic events. Support nonzero tests and defensive inversion-zero checks belong to their named scan/inversion events, rather than additional field_equal calls. No CPU instruction, allocation, wall time, arbitrary-bit complexity, numerical stability or production-memory certificate is asserted.

## Disposition

This adds only the bounded ternary interface scope. The previously accepted dyadic implementation and underlying mathematical theorem remain valid. Keep unrestricted lengths and fields, extension fields, common-chirp/actual-caller integration, numerical/finite-word production and historical priority open. No new theorem, novelty promotion, generic FFT speedup, or broad gate retirement is accepted. No external write occurred.

Derivative note: private tracking-version and record-integration instructions are omitted. Mathematical statements, domains, independent versus author replay evidence, cost accounting and remaining limits are preserved. Original report SHA-256: `b66b1688daa042aad09a0acf342c6a916fe207e3e2af863c41c0e9916914d17f`.
