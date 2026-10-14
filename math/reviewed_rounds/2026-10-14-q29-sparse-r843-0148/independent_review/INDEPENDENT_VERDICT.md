# Q29 full sparse kernel: independent scoped acceptance

Date: 2026-10-14 UTC.

## Verdict

**ACCEPT, scoped to the exact coefficient array R843(w;z) modulo (25, Phi3375(z), w^100), the checked implementation, and the reported finite execution.** A separately authored direct-monic-division implementation independently reproduces every one of the 180,000 output coordinates. A fresh rebuild of the producer source reproduces them again. Independent Gaussian-binomial controls and the complete producer seal also pass.

This acceptance does not cover a pi-basis conversion, normalization by pi^60, a normalized F jet, a discriminant calculation or nonvanishing result, a residual-branch resolution, or an asymptotic/FFT-speed claim. The producer explicitly excludes these conclusions. The auxiliary checksum name has one nonblocking metadata caveat described below; SHA-256 and byte-for-byte comparisons govern acceptance.

The producer's cyclic-ring calculation is implementation-diverse evidence by the same author. This document and the new direct-monic checker supply the separate-reviewer evidence. Those are distinct provenance categories.

## Exact reviewed output and seals

- Producer directory: `sparse_r843_producer/`.
- Producer manifest: SHA-256 `8c31f1792ff77809666cb601ad4cf3c70d28f904a7b74ea00083764c87aa23b4`, containing 270 files. Every size and SHA-256 matches.
- Producer archive: `Q29_Exact_Sparse_R843_W100_Producer_2026-10-14.zip`, SHA-256 `41d53445db96577f72054729356b82727efbef015cd43be33389313707c42a28`.
- Accepted coefficient SHA-256: `ebf51150ffbed6e87f3e08875451176963670801c59ffd9128336a02c43ca38c`.
- Exactly 180,000 bytes, all between 0 and 24, including 172,968 nonzero bytes.
- Byte offset 1800*k+j is the residue of the coefficient of w^k z^j for 0 <= k < 100 and 0 <= j < 1800.

The producer's packed-kernel output, its cyclic-ring output, this reviewer's direct-monic output, and the reviewer's freshly rebuilt producer output are identical as bytes. `CONTROL_AUDIT.json` pins the reviewed sources, receipts, report, manifest, seal, and coefficient files. The original review bundle included the unchanged producer archive. This publication edition substitutes its explicitly hash-mapped publication-safe producer projection; the original archive remains separately hash-pinned and unchanged locally.

## Independent derivation of the recurrence and reciprocal quotient

Work first in the integral polynomial ring Z[q,x], before any reduction modulo 25. Define H_n(x;q) as the sum over k of Gaussian binomial(n,k)_q x^k. The Gaussian Pascal identity gives

H_(n+1) = (1+x) H_n - (1-q^n) x H_(n-1).

For n >= 1, eliminate the intervening even index by applying this identity twice and substituting

(1+x) H_(n-1) = H_n + (1-q^(n-1)) x H_(n-2).

For n=2m-1 and m >= 2, the result is

H_(2m+1) = [(1+x)^2 - x(2-q^(2m-1)-q^(2m))] H_(2m-1)
             - x^2 (1-q^(2m-1))(1-q^(2m-2)) H_(2m-3).

The Gaussian row is symmetric in k. Thus each odd H_(2m+1) vanishes at x=-1 by pairing its coefficients, and its quotient U_(2m+1)=H_(2m+1)/(1+x) is an integral reciprocal polynomial of degree 2m. The polynomials x^(m-k)(1+x)^(2k), for k=0,...,m, form an integral unitriangular basis of such reciprocal polynomials: their highest powers are x^(m+k), each with coefficient one. Consequently there is a unique integral polynomial R_m(w;q) satisfying

U_(2m+1)(x;q) = x^m R_m(x+x^(-1)+2;q)
              = sum_(k=0)^m r_(m,k)(q) x^(m-k)(1+x)^(2k).

Dividing the displayed odd-index identity by (1+x)x^m gives

R_m = (w-2+q^(2m-1)+q^(2m)) R_(m-1)
      - (1-q^(2m-1))(1-q^(2m-2)) R_(m-2).

The seeds are R_0=1 and R_1=w-2+q+q^2; setting R_(-1)=0 makes the formula valid also at m=1. The production seed and first step match these values. No division by a nonunit in Z/25Z occurs: the polynomial identities and quotient construction are integral before reduction.

Writing P=R_(m-1), Q=R_(m-2), D=(1-q^(2m-2))Q and T=(1+q)P+D gives

wP-2P-D+q^(2m-1)T,

which expands into exactly this recurrence. In particular the Q coefficient is -1+q^(2m-2)+q^(2m-1)-q^(4m-3). The separately authored checker implements this expanded coefficient directly, without the producer's D/T intermediates.

## Quotient ring and packed monomial map

3375=3^3*5^3 and

Phi3375(z) = Phi15(z^225)
           = z^1800-z^1575+z^1125-z^900+z^675-z^225+1.

The polynomial is monic, so every coefficient has a unique remainder of z degree below 1800 even over Z/25Z. Direct descending monic division independently verifies that it divides z^3375-1. Thus z^3375=1 in the target ring, and reducing a monomial exponent modulo 3375 is valid.

For z^(225*b+r), 0 <= b < 8 and 0 <= r < 225, multiplication by z^(225*a+s) produces residue r+s modulo 225 and block exponent b+a+carry. The production plan divides each block exactly at r=225-s and reduces the resulting power of y=z^225 by Phi15(y). The intervals have lengths 225-s and s, cover the original block without overlap, and target the correct z-residue intervals. The modulo-15 block index is valid because y^15=1 in this quotient. Empty carry intervals are skipped correctly, including s=0.

Independent integer division confirms that all required Phi15 image coefficients are 0, +1 or -1. Both the maximum image l1 norm and maximum output-row l1 norm are six. Thus a shifted canonical input contributes at most 6*24=144 in absolute value to one coordinate. Staged bounds are: D at most 24+144=168; T at most 24+24+144=192; N before its shift between -72 and 24, then at most 216 in absolute value. Every accumulator is safely inside int16_t. Modulo-25 normalization is exact integer arithmetic, with negative remainders brought back to 0,...,24. No characteristic-5 shortcut is used.

The same-author cyclic comparison is also valid: since (z^3375-1) is contained in the ideal generated by Phi3375, there is a quotient homomorphism from the cyclic ring to the target ring. Computing the recurrence there and reducing monically at the end must map to the same answer. This reasoning does not promote a same-author check into independent authorship.

## Loop, truncation and output audit

The source uses m=1,...,M inclusively, with M=843, rather than a shortened benchmark loop. At the start of step m, P and Q contain R_(m-1) and R_(m-2). Their live coefficient widths are a=min(m,L) and b=min(m-1,L); the new width is n=min(m+1,L). These are correct also at m=1 and when the width first reaches L=100.

D is zeroed through width a before Q is copied through width b; the extra newly live coefficient therefore cannot contain stale data. T is rebuilt through a. N is rebuilt through n, including the wP contribution from P[k-1] and no negative coefficient index. The buffer swaps set Q to the old P and P to the new N. Beyond the increasing live degree, the reused arrays remain zero until explicitly initialized. No term lowers w degree, so discarding w^100 and higher commutes exactly with every recurrence step.

The output iterates the full final P buffer of length L*1800, canonicalized by the last recurrence step, in the stated order. The source's work counters were independently reproduced:

- 849,703,500 signed scatter coordinate updates;
- 571,320,000 counted dense arithmetic updates;
- 428,488,200 modular normalizations.

These counters are defined arithmetic categories, not total CPU instructions or memory traffic. They exclude loads, stores, loop control, preparation, output and other bookkeeping.

## Independently executed verification

Only newly authored code from this task was compiled or executed. No historical scientific code was imported or run. All writes stayed in the local review directory; there were no network requests or external writes.

1. Fresh C++ direct-monic checker: construct the expanded recurrence polynomial in ordinary z coordinates, then divide descending by the seven-term Phi3375 at each step. It uses neither a cyclic ring, period wrapping, Phi15 block maps nor fused D/T intermediates. All m=0,...,8 full small outputs match the producer.
2. Run that independent checker at m=843, w<100. All 180,000 coordinates match both producer outputs.
3. Recompile the producer source into a reviewer-owned executable and rerun the full case. All bytes match again.
4. Independently construct every Gaussian row for n=1,3,...,17 from the coefficient of t^k in product_(j=0)^(n-1)(1+t*q^j), then remove the factor q^(k(k-1)/2). This is a different finite construction from the producer's q-Pascal implementation. Divide by 1+x integrally, substitute q=z or q=z^1001, reduce by direct monic division, and compare the reconstructed U from the stored R coefficients. All 18 cases pass.
5. Independently compare all stored truncation runs at widths 1, min(2,m+1), min(4,m+1). Every byte agrees with the corresponding full small output prefix.
6. Independently verify period reduction, integer map bounds, operation counts, all 270 producer manifest entries, and the final manifest seal.

`REPRODUCTION_RECEIPT.json` and `CONTROL_AUDIT.json` contain the detailed results and commands. The original failed reviewer manifest check is retained: it expected the preliminary string-valued manifest schema, while the final schema uses {bytes, sha256}. The corrected check validates both fields. There was no producer-byte mismatch and all preceding mathematical assertions had passed. This is disclosed in `INITIAL_AUDIT_FAILURE.json`, with the original checker text retained.

## Timing and resource interpretation

The producer's measured primary full-kernel wall time was 0.473105316 seconds. Preparation was 0.001919247 seconds and writing was 0.002805758 seconds; the full launched process was 0.481710282 seconds. These intervals must not be conflated. Its entire primary compilation/control/timing/gate/full-run driver took 2.082052624 seconds wall and 2.100132948 seconds charged CPU, with peak child RSS 88,648 KiB.

The producer's same-author expanded cyclic kernel took 0.511629601 seconds wall, followed by 0.001359460 seconds monic reduction and separate preparation/writing. Its successful driver took 1.094386945 seconds wall and 1.091393 seconds child CPU. The disclosed initial compiler warning failure took 0.522132172 shell-observed seconds; its CPU was not separately retained. It must remain part of the audit history.

The fresh independent direct-monic full kernel took 1.59365 seconds wall. The fresh production rebuild's kernel took 0.450889939 seconds, with 0.001641276 seconds preparation and 0.002702234 seconds writing. The full reviewer reproduction harness took 3.213542269 seconds wall and 3.218348 seconds charged parent-plus-child CPU. Peak child RSS, including compilers, was 88,952 KiB. The separate successful control/seal audit took 0.236938219 seconds wall and 0.236762065 seconds CPU, with 11,676 KiB peak RSS. The initial reviewer schema check used 0.197049108 shell-observed seconds; separate CPU was not retained.

The review harness sets a 180-second wall alarm, cumulative remaining-CPU admission below 120 seconds, process CPU limits, a 512 MiB address-space limit for itself and children, and subprocess wall timeouts. The short additional control audit has its own stricter 170-second/110-second limits; observed combined reviewer computation is below four seconds wall and CPU apart from negligible file packaging. This is a finite measured execution far below the requested envelope. Neither review nor producer claims an operating-system aggregate cgroup guarantee for arbitrary modified controllers/descendants. Per-process address-space limits and maximum child RSS are not measurements of aggregate concurrent RSS.

The eightfold empirical budget estimates are admission heuristics. They are not a proof of a general time bound. No conclusion about optimality, asymptotic complexity relative to FFT, uniform scaling, or repeatability of the exact timing constants is accepted. Very short CPU subintervals have coarse resolution; a reported zero is not proof that the operation was free.

## Nonblocking checksum metadata caveat

The producer field named `fnv1a64` starts its rolling XOR/multiply checksum from 1469598103934665603. The conventional FNV-1a 64-bit offset basis is 14695981039346656037. Thus the stored value should be interpreted as the implemented seed-specific FNV-style checksum, not a standard FNV-1a digest. The multiply/XOR computation is deterministic, but this label is imprecise. No producer artifact was modified during review. This has no effect on the coefficient arithmetic, the independent byte comparisons, or the accepted SHA-256 digest.

## Explicit precision and mathematical boundary

The accepted bytes are in the z basis of (Z/25Z)[z]/Phi3375(z), not in a valuation-readable alpha/pi basis. Statements in the producer report about that representation's established relationship to a mixed-characteristic precision contract are background from the separate contract, not a new basis-conversion verification in this review.

The integral identity at x=-1-v is

U1687(-1-v;q) = sum_(k=0)^843 (-1)^(843+k) r_(843,k)(q) v^(2k)(1+v)^(843-k).

Consequently the retained 100 R coefficients determine the raw U jet through v^199 modulo 25: omitted terms have v degree at least 200. Neither producer nor reviewer materialized this transformation. Substitution v=pi*Y, basis conversion, exact divisibility/normalization by pi^60, and the precision losses needed to claim a normalized F modulo pi^140 still require their own guarded calculation. This acceptance supplies none of those missing operations.

The coefficients of w^100 through w^843 are absent. A full discriminant of R843 has not been computed, and no nonvanishing, residual repeated-branch or global problem conclusion follows from this finite kernel acceptance.
