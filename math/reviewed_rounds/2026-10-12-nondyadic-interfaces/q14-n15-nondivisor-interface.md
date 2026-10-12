# Independent bounded review: Q14 N15 nondivisor interface

12 October 2026. Verdict: ACCEPT_BOUNDED_N15_EXACT_DENSE_INTERFACE. This review concerns only the exact sealed N=15 direct-bin interface; the broad growing-fiber gate remains open.

## Exact object and current obligation

Candidate archive: Q14_N15_Nondivisor_Interface_CANDIDATE_2026-10-12.zip, SHA256 37caa34b7c7b086ce7b46b988dd8e47d7dd6bbf91745d5ac42a9dbb30cb959f7, 232,823 bytes. Source interface.py: e18ae733ac7be30e89ad60aedbdc31a5aa429cf7c14258476f95f6537abc1dff. All 16 declared payloads plus MANIFEST.json, the archive CRC, and seven source pins were independently verified against their local originals. The cold candidate source and fresh tests were inspected before execution. Evidence snapshots, including the predecessor interface.py, remained inert.

The original Q14 completion test calls for one declared representation/regime, direct binning with charged reads, rejection, Green and fallback, and preservation of the accepted conservative repair unless a sharper uniform constructor is supplied. The bounded milestone examined here is one non-dyadic length. The candidate advances only that bounded milestone at N=15, Q=3, M=5 over Q(zeta_15), with all B=1,...,5 and affine label maps sigma=1,...,4, offset=0,...,4. Thus B=2,3,4 are genuinely nondivisors of M. There is no padded transform or assumed cyclic quotient to B points.

The field representation is exactly eight Fraction coefficients modulo Phi_15. Cap budgets are 0,1,2 and aggregate budgets 0,...,15. The positive unnormalized transform, exact full raw-input reads, explicit 15 output elements, complete candidate verification and raw-input fallback target are retained. The previously accepted dyadic repair and F015's separate accepted theorem are unchanged.

## Pre-seal correction and algebraic review

Static independent review found the preliminary kernel used the wrong sign for convolution y[d-u]. For a fiber character omega^(-h d), a positive-sign kernel would select label[-h], while the recovery addressed label[h]. The author corrected the sign before sealing. The exact accepted bytes use

g_r[u]=(1/5) sum_{h:label[h]=r} omega^(-h u).

Convolution then yields H_r(d)=sum_{h:label[h]=r} c_h omega^(-h d), and the paid five-shift demodulation recovers c_h. The independent suite checks every projector on every character for every legal hash setting and explicitly rejects the reversed-kernel mutation. This correction is part of the review history, not a post-seal candidate modification.

All collisions and cancellations are allowed: no single bucket sample is used as a nonempty/empty certificate. The representation of a candidate must have distinct legal labels, canonical nonzero amplitudes and correct shape. All five reconstructed coordinates are compared, even after a mismatch. Since complete recovery computes the actual five coefficients, cap/aggregate refusals are exact support violations. The source pays the entire attempted fiber before rejecting; every raw coordinate was already validated/read. No heavy/light asymptotic shortcut is inferred.

The output formula X[k]=5 sum_t c_{t,k mod5} z^(kt) follows directly by writing j=t+3u. Its normalization and sign are correct. Every returned vector has all 15 explicit coordinates.

## Independent verification method

The reviewer verifier is freshly authored and imports only the exact new interface. It derives Phi_15 by exact polynomial division of (x^15-1)(x-1) by (x^5-1)(x^3-1). Its expected transforms gather raw rational coefficients into cyclic exponent slots, then reduce the resulting polynomial. This does not call the candidate's Arithmetic, root table, binning, certification, output synthesis or Green recurrence. Fiber support is computed by direct five-character sums. Green residuals are independently constructed before support classification. Expected final outputs always come from the original raw input's direct DFT.

The suite covers all 100 bucket/hash settings, all support cardinalities and cap boundaries, aggregate boundaries, genuinely non-rational cyclotomic coefficients, early and late impulses, zero budgets, strict representation/parameter refusal, cold repeat and output-mutation isolation. It independently wraps field methods to observe their actual phase/call counts, and separately checks exact bin sample, full-read, comparison and final-output obligations.

False/malformed candidate injection and resource exceptions are required to propagate. They never justify heaviness and never silently trigger ordinary fallback. A candidate differing only in the last fiber coordinate is rejected after all five comparisons. Reversing the kernel sign is detected.

An early reviewer-harness assertion treated float length 15.0 as if it were the supported integer length. The candidate correctly rejected it without reading the unsupported domain. The verifier was corrected to require exact integer type, then rerun from the start. No sealed candidate change was needed.

## Passed finite evidence

The independent final suite passes 207 API cases, 186 complete output vectors / 2,790 coordinates, all 100 bucket/hash settings, and 1,500 projector-character checks. It has 195 exact bin-count audits, 128 independently observed field-call audits, 38 exact fallback-cost audits, 24 Green controls, 24 non-rational coefficient cases, 225 root-product checks and four inversion checks. All 36 domain-refusal controls, seven candidate mutations, the reversed-kernel mutation, last-coordinate mutation, three resource-exception propagation controls, and cold/result isolation pass.

The exact sealed author suite also cold-replays byte-identically: 275 normal API cases plus six guard controls, 281 ledger audits, 180 full vectors / 2,700 coordinates, all 100 hash settings, all 32 support subsets, 1,500 kernel-entry comparisons and 1,400 nontrivial-kernel full-support checks. These author totals are distinct from the independent totals. All frozen payloads remain unchanged after execution.

Finite tests supplement the reviewed algebraic correctness/completeness argument; they do not exhaust all Fraction inputs, prove arbitrary-bit complexity or establish an all-length production implementation.

## Green and fallback guards

With P=alpha I+beta S+gamma D^-1 and L=alpha I+beta D+gamma S, F P=L F. The source checks every actual d_j=alpha+beta z^j and then the cyclic closure 1-product_j(-gamma/d_j). Inversion of P or L alone is insufficient: (0,0,1) is invertible but violates every local denominator. The closure-zero and late-zero cases also retain domain-refusal semantics. Guard failure and support refusal are distinct.

When permitted by the caller's flag, either valid-input refusal produces the ordinary direct DFT of the saved original input. Support refusal after a Green residual never transforms that residual as the fallback output. Successful Green cases are compared directly with the original raw DFT. Malformed representation/parameters do not receive fallback, and internal/resource faults propagate.

## Costs and scope guard

This is dense ideal character-projector binning. It has deterministic zero random bits, zero leakage/error and zero failure probability in its exact field, and pays full kernels and all five shifts. None of these exact statements implies numerical stability or a fast sparse constructor.

For f attempted fibers and total support R, the source has 14 cold products; 5B kernel products and 25 kernel additions; f(25B+30) recovery products and f(25B+25) additions; 5R full-certificate products/additions; and 60 products/45 additions for complete successful output synthesis. It reads all 15 raw elements, compares 5f reconstructed elements, writes 5Bf bin samples, reads 25f demodulation samples, and writes either no final vector or all 15 outputs. Independent observed call counts corroborate the field-operation ledger.

The ordinary fallback separately charges 225 products, 225 additions and 225 raw rereads, plus explicit output writes. This is O(N^2). It is not called an FFT. Each attempted fiber's direct convolution and recovery cost O(BM^2+M^2). The wider symbolic loop bound and O(N+BM+K) field-word storage are compatible with the source, but finite N=15 checks do not establish a fast all-length implementation.

The Green guard expands each inverse into eight field products and rational Gaussian elimination. Counts for expanded inversions must not be added again to a unit-cost-inversion ledger. Rational operations have unbounded Fraction bit cost; normalization, gcd, allocation, VM instructions and physical runtime are not certified. The indexed allowances are abstract bookkeeping.

The full-support ideal-kernel observation is correctly limited: at prime length, every nonempty proper ideal selector has nonzero entries at every time coordinate, by the minimal polynomial Phi_p. This excludes shortening this exact selector while preserving all its character responses. It does not lower-bound all binning algorithms, fast evaluation of dense kernels, approximate windows, randomized methods or Fourier circuits. Naive nondivisor folding also fails shift covariance, but this does not prove arbitrary-length impossibility.

## Disposition

Accept only the bounded N15 exact direct-bin/Green/fallback API after the results recorded in VERDICT.json. Keep the main gate progressed_open. Preserve fast arbitrary-length/windowed HIKP binning, the sharper STR-Q5 paid uniform RIP constructor, other lengths/representations, finite-word/bit/numerical production, and historical priority as open. No inherited faster discovery bound is assigned to these dense kernels. No new theorem identity/count, novelty promotion, generic FFT speedup or external write follows.

Derivative note: the private tracking-version reference is replaced by its mathematical milestone. The exact Q(zeta_15) representation, pre-seal sign correction, proof, independent and author evidence, dense costs and remaining limitations are unchanged. Original report SHA-256: `f29fc2dc9b76d44f2cf0ecf560879a210057398d69b9901a31b59ab4d4d8dfab`.
