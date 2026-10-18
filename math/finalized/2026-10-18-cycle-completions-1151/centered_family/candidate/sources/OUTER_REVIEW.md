# Independent final review: complete retained outer transfer

18 October 2026 UTC.

## Verdict and exact gate

**PASS for the complete retained-operator stream, exact signed scatter, one final per-coordinate rounding, exact scale-back, every-tape bound, and the qualified source-cost/storage claims.** This review accepts the sealed candidate only in its stated trusted-local and fixed-family scope, with the mandatory dependency cost erratum retained. No runtime correction is required.

The accepted candidate manifest SHA-256 is:

`8aaaac494523950eece750a487561370c92b00d4b1a2ac134c519043b3a72422`.

The new runtime `full_transfer.py` SHA-256 is:

`40d90da471b62fc9ac268b78cbe9f080b149be3789253bb1dbbe43837d5c534a`.

The manuscript SHA-256 is:

`ae04070f8c3184e4d917b53ed43a0228d81a41772cf68fb92ac341da18157b69`.

All 20 manifest members and all 14 source-evidence bindings were independently checked before and after the fresh run. The manifest also matches SEAL.json. The four executed runtime files were byte-identical copies placed in this review directory; the candidate remained unchanged. No historical uploaded implementation was executed and no external write occurred.

This gate does not accept an original-signal producer, full random sparse recovery, its probability statement, independent amplification, or a dense/all-length executable. Formula (2) retains its explicitly missing centering/source/recovery premises and the ALG-034 target distinction. No Q16/STR-Q1 reopening, ALG-034 closure, novelty, or practical performance claim follows.

## Fresh independent execution

The complete production source, candidate oracle/tests, dependency reviews, cost erratum and relevant inherited theorem text were inspected before execution. The reviewer then authored `independent_review.py` and a separate capped launcher. The candidate's tests and oracle were not imported or called.

The capped process exited 0 with empty stderr after 37.278412 seconds, with maximum RSS 16,384 KiB. Limits were 150/160 CPU seconds, 240 wall seconds, 768 MiB address space, 32 MiB per output file and 64 descriptors. All executed source hashes matched before and after. These are process safeguards and measurements, not complexity or speed evidence.

The fresh run verified:

- N=257, M=2048, D=5: every one of 885 coefficients and all 257 rows, with support `(0,1,1024,2047)`, opposite-signed near-cap values, a retained exact zero, and scale `2^31`. The final grid is exponent zero after exact numerator shifting from normalized exponent 24. The output equals the candidate's entire stored output exactly.
- N=512, M=2048, D=5: every one of 441 coefficients and all 512 rows, at scale `2^-17`, final exponent 42 and normalized exponent 25. The row-zero complex value is exactly `(1025/2^27,0)`. The complete output hash matches the candidate's saved hash.
- Both complete runs against a newly authored 320-bit guaranteed target oracle, including rows receiving no contribution. Every exact squared complex error is bounded by the square of the stated conservative bound for formula (1). The maximum ratios, exact integers, complete row intervals and cumulative receipts are saved, not replaced by floating tolerances.
- Exactly one pi setup and one square-root setup in each nonempty full run; scalar coefficient-call and complex-certificate counts equal 885 and 441 respectively. The supported zero in the primary fixture does not suppress coefficient work.
- 5,367 independently derived signed nearest-even controls, including 258 exact signed ties, and 2,000 exact complex-product controls with up to 321-bit signed components. Product checks use distinct sum/difference identities.
- 1,022 guard/classification controls across m=2 through 150; the exact first D=5 block; and the 401-lift/256-row dense counterexample.
- Empty support still returns all 257 zeros and incurs N initialization/output work with no scalar setup.
- Strict cap rejection on both coordinate signs, including a 20,001-bit value, before scalar setup; malformed scale/configuration controls; dense rejection with no scalar setup.
- Actual 20,001-bit original rows with zero medians remain retained and paid at their original width. A 12,004-bit rational beta encoding is accepted and paid at its actual encoding width. Existing 1,001-bit event history, larger existing accounting counters and their receipts remain cumulative.
- Drop-first, drop-intermediate, drop-suffix, repeated, reordered, foreign-source, altered-grid and altered-value controls. Every control fails without a completed result and retains its paid prefix. The suffix case evaluates and pays 220 records before rejecting its missing final item. Repeated completed-run requests and substituted output objects are rejected.

The mutation controls operate only on disposable harness-owned objects. They do not assert hostile-runtime authentication or change the byte-pinned production files. The test harness may retain audit data; that memory is not claimed as production storage.

## Independent oracle and candidate oracle audit

The new oracle uses pi = 8 atan(1/3) + 4 atan(1/7). To justify the identity, tan(2 atan(1/3))=3/4 and tan(2 atan(1/3)+atan(1/7))=1; the angles lie in the first quadrant, so the sum is pi/4. Each arctangent uses 140 exact rational alternating terms and the exact next term to bound its remainder, then rounds outward to 320 bits.

Rational sine arguments are independently reduced modulo two and reflected into [0,1/2]. Exact zeros and units are handled exactly. For other arguments, the entire pi-scaled angle interval is evaluated by forward interval Taylor terms through degree 127, rather than the candidate oracle's Horner polynomial or the production scalar's midpoint/Lipschitz construction. Every arithmetic step rounds outward. Taylor's theorem through degree 128 gives the uniform remainder `2^129/129!`; its ceiling on the 320-bit grid is exactly one. The entire angle interval is below two, making this remainder valid.

The root is enclosed using `isqrt(floor(M*2^640/N))` and the separately asserted squared inequalities `z^2 N <= M*2^640 < (z+1)^2 N`. Rational corner divisions have strictly positive denominator lower endpoints. Signed endpoint powers preserve negative odd powers and include zero for even powers crossing zero. The exact retained coefficient is assembled directly from its sine-ratio/root/phase definition, without a production helper or iterator.

Membership is independently constructed row-first from the literal offsets `-h,...,h+1` modulo M, not from endpoint records. For every returned row the oracle sums exact signed interval products with the independently derived column medians. Let r and i be the farthest rational distances from the normalized output coordinates to those guaranteed target intervals. It checks exactly

`r^2+i^2 <= (eta * sum(|a_k|+|b_k|)/2^P + 2^-b)^2`.

This is a valid conservative test of (1). It does not confuse Cartesian coefficient error with the required complex eta certificate. The universal coefficient guarantee remains the previously accepted scalar proof, supplemented here by independent full-row finite evidence.

The candidate's 256-bit oracle was also reviewed independently: its 160-term atan(1/2)+atan(1/3) identity, outward 48-term Horner sine and exact `2^97/97!` remainder, signed powers, positive quotient denominator, root inequalities and row-first traversal are sound for its fixture. A separate post-run crosscheck proves that all 514 independently computed 320-bit coordinate intervals lie inside the candidate's 256-bit target intervals, after exact grid alignment. No floating approximation is used.

## Complete stream and source binding

For supported k, the lift interval is exactly

`ceil(N(k-h-1)/M) <= r < ceil(N(k+h+1)/M)`.

This is equivalent to `-h <= k-floor(rM/N) <= h+1`. Shifting r by N shifts the floor by M, proving equivalence with the modular row stencil. When t<M, the real interval length Nt/M is strictly less than N, so reduction modulo N is injective. Distinct support indices produce distinct ordered incidences. Thus each row receives at most t terms and `E <= S ceil(Nt/M) <= St`.

FullTransfer owns the accepted iterator and numerical producer. The next ordinal must match; each generated coefficient is validated against its exact incidence, bound source, retained support position and p-grid. Terminal equality with the paid endpoint-length sum catches a missing suffix. This supplies all E terms and precludes successful completion from an omitted zero or small contribution. No E-sized coefficient collection, N-sized phase cache or N-iteration transcendental pass exists in production.

The producer is actual Cartesian-median computation over immutable original rows. Outer separately pays semantic replay and retains those rows. Identity checks are trusted-program invariants, not external historical attestation. The precise absent link to the original source signal is explicitly preserved.

## Signed arithmetic, every-prefix bound and scaling

With `w=P+2m+2`, the strict Cartesian estimate cap implies both estimate numerators have magnitude below `2^w`. The accepted complex coefficient certificate and `|C|<3` imply coefficient numerator magnitudes below `4*2^p`. Each exact Cartesian complex-product contribution is therefore strictly below `2^(p+w+3)` in magnitude.

At most t terms occur in any row prefix. Consequently every prefix has magnitude strictly below

`2^(p+w+3+ceil(log2 t)) = 2^(W_acc-1)`.

This fits the ordinary signed W_acc-bit range, including its asymmetric positive endpoint. The source checks both sums and the row count at every update; cancellation cannot hide a previously overflowing prefix. Integer arithmetic does not wrap.

All four products and both sums are exact. After the complete stream, each Cartesian coordinate is rounded once by signed nearest-even floor/remainder arithmetic. The complex error is at most `2^-b`. When `b-sigma>=0`, changing the denominator exponent is exact; otherwise shifting the numerator by `sigma-b` and setting exponent zero is exact. Both scale branches were exercised with nonzero values.

## Exact dense boundary

The guard is exactly

`D <= floor((2^m-5)/(32m))`.

The unavailable equality t=M is excluded by residues modulo 32 for m>=5 and the elementary D>=5 check for m=2,3,4. Every failed guard therefore has t>M. The ratio `(32Dm+4)/2^m` decreases strictly for m>=2 and tends to zero, so each fixed D has one finite first passing m and all larger m pass. For D=5 this is m=11, corresponding to N=257 through 512.

At N=256, M=1024, D=5 and k=0, h=801 and the lift endpoints are -200 and 201. There are exactly 401 lifts but only 256 residues. Thus an unguarded reuse of the sparse uniqueness argument double-counts incidences. More generally Nt>NM forces repeated incidences in some column when t>M.

FullTransfer rejects before its N arrays and numerical preparation. Its input is a sparse median context, not the original normalized signal. The same unbound context can be compatible with different originals, so this interface cannot implement the prescribed original-signal dense transform. The returned dense requirement is a precise unresolved interface dependency, not an all-length result or random failure.

## Universal versus conditional accuracy

Formula (1) follows unconditionally for every accepted capped sparse output: exact multiplication/summation adds no error, the complete coefficient perturbation contributes at most `eta sum |Z_k|`, the sole row round contributes at most `2^-b`, and scaling is exact. No successful-recovery event is used.

Formula (2) follows only under its stated additional source/centering/recovery premises. Decompose the normalized error into final rounding, `(Ctilde-C)Z`, `C(Z-z)` and `(C-A)z`, where A is the full centered operator. These yield, respectively, `2^-b`, `t eta(1+E_M)R`, `3t E_M R` and `12*4^-s R`; use R>1/2 for the relative rounding term. The inherited tail is applied to exact z, not a failed-tape Z. The multiplier is t rather than E or S.

The finite fixture does not meet all front-end sparse-recovery guards. This does not affect the retained-operator theorem, but it cannot establish a recovery probability or a transform of an unidentified original. ALG-034's projected or reflected projected targets cannot be relabeled as the original input's U_N target.

## Costs and storage: acceptance qualifications

The mandatory dependency erratum remains part of acceptance. Producer and replay separately incur

`T_med = O(1+S+R_rows+S R_rows log(R_rows+1))`

events and the H-based work/storage envelopes. H must cover actual original/header/address widths, existing counter encodings and cumulative event growth. Original rows and sorting/producer context require `O((S R_rows+S+R_rows+1)H)` bits. Their storage is not O(Sm), and repeated validation, failed prefixes or observation calls are not free.

For the stated fixed D,beta,d family, fixed parameter encodings, O(m)-width original data and O(m)-width previous counters, the new outer/accumulator/output fields have O(m) width. The scalar uses O_D(m) events with O_D(m^2)-width intermediates, giving O_D(m^5) schoolbook bit work per coefficient and one lazy setup. Therefore manuscript (3) is safe in addition to the full producer/replay prefixes. The separate N initialization and output passes use bounded-width word operations; (4) follows under the accepted growing-word model, without calling linear bit work linear word work.

Equation (5) inherits exactly these fixed-D/fixed-d and width/history qualifications. It is not a parameter-uniform memory claim for arbitrary d or D. A large positive sigma can add sigma-b bits to each nonzero output numerator. For arbitrary callable parameters, use actual reached outer/output widths in the N term and actual scalar widths, while retaining original-row and prior-counter costs. This scope is already stated in manuscript sections 2 and 6 and must remain attached when quoting (3)-(5); adding “for the same fixed family” immediately before (5) would merely make its scope harder to misread.

All E coefficient evaluations, scalar setup, stream fields, exact products, signed accumulation, N initialization, N outputs, source replay and stored original rows are accounted for. Receipt serialization, hashing, snapshots and independent oracle execution are separately bounded harness work. No D-uniform m^5 assertion or unrestricted m-only original-row/counter claim is accepted.

## Evidence files

- `INDEPENDENT_RESULTS.json`: full fresh receipt/count/control evidence.
- `TRUTH_257.json`, `TRUTH_512.json`: guaranteed independent intervals for every row.
- `ORACLE_CROSSCHECK.json`: all 514 candidate coordinate intervals crosschecked and seal verified.
- `PROCESS_EXIT.json`, `RUN.stdout`, `RUN.stderr`: capped process and source hashes.
- `independent_review.py`, `oracle_crosscheck.py`, `launch_review.py`: complete newly authored executable review sources.
- `PROOF_AUDIT.md`: additional focused read-only proof/cost audit.
- `MANIFEST.json`: hashes for this independent review packet.

The requested scoped stopping condition has been met. The separate original-source, general recovery, dense-dispatch and amplification gates remain open.
