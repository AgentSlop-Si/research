# Independent finalization review: exact Mersenne-prime-power radix

Review date: 2026-10-15. Reviewed directory: `mersenne_prime_power_exact/`. Reviewer wrote only `mersenne_independent_finalization/`; no original research file or external service was changed.

## Decision

**Accept the exact-radix arithmetic and the bounded implementation-level negative result. Require a narrow accounting clarification in REPORT.md before treating the report as finalized. The speedup research goal remains open.**

Finalization addendum: the requested accounting and comparator corrections have now been incorporated in the standalone `FINAL_REPORT.md`. The original report remains immutable. The corrected standalone report is accepted at the scoped experiment level, with the broader goal still open.

The requested representation is genuinely implemented: p=2^m−1 and Q=p^d. Direct grouped folding stays in that representation. It is not an arithmetic-progression basis or a finite-extension-field implementation.

The original finite test counts and timing direction reproduce. Additional independent checks pass. No code correctness defect was found on the stated nonnegative-input domain. The report's closing claim about charging operations in both ledgers/timings is too broad: elapsed timing includes executed work, but the diagnostic ledgers omit parts of the work. Also, original timing includes unequal diagnostic instrumentation. These limitations do not reverse the tested failure to beat matched binary conversion, including after an independent clean-code control.

## 1. Independently verified arithmetic

Assume x≥0, m≥2 and integer d≥1. Primality of p is necessary only for the stated prime-power unit-group fact, not the positional conversion.

### Single-p quotient and remainder

Write the current residual x=A·2^m+B, 0≤B<2^m. Since 2^m=p+1,

    x=A p+(A+B).

Maintaining original_input=q p+x, the update q←q+A and x←A+B preserves the invariant exactly. Whenever the loop runs, A≥1 and the residual decreases by A p>0. It stays nonnegative, so termination follows. At loop exit 0≤x<2^m=p+1. At most one final subtraction puts x in [0,p), producing the exact quotient and canonical remainder. Repeated d-fold extraction produces the unique base-Q digit; reconstruction by d applications of (x<<m)−x is multiplication by Q.

### Direct grouped fold, including the sign pattern

Put S=2^(md), Q=(2^m−1)^d and K=S−Q. Then 0<K<S and

    x=A S+B=A Q+(B+A K),  0≤B<S.

The code's general correction is correct because

    K = sum(j=1..d) (−1)^(j+1) binom(d,j) 2^(m(d−j)).

With invariant original_input=q Q+x, the update q←q+A, x←B+A K preserves the invariant and decreases x by A Q whenever A≥1. It therefore terminates. The final subtraction loop establishes 0≤x<Q. This proves exact divmod, rather than merely modular reduction.

For d=2,

    Q=2^(2m)−2^(m+1)+1,
    K=2^(m+1)−1,
    A K=(A<<(m+1))−A.

Thus the new special case is valid. For every m≥2, Q/S≥9/16>1/2; after the main fold loop, at most one subtraction is needed for d=2. The review's clean benchmark uses this fact.

For unrestricted d, neither the final subtraction count nor fold count is uniformly constant. After folding, the subtraction loop can take up to floor((S−1)/Q) iterations. Its scale is S/Q=(1−2^(−m))^(−d), and the contraction factor K/S approaches 1 when d grows with fixed m. General-d binomial terms also contain actual multiplications by binomial coefficients. These costs cannot be replaced by a single free bit operation.

### Carrying, convolution and modulus separation

For nonnegative canonical digits, a coefficient is bounded by min(L_a,L_b)(Q−1)^2. The code's input-specific bound min(L_a,L_b) max(a) max(b) is also valid. The report's L(Q−1)^2 formula is valid for equal operand digit-length bound L. The coefficient bit width grows approximately as 2 log2(Q)+log2(L), so grouping decreases digit count while widening scalar work.

The NTT/CRT implementation selects enough of three moduli to make their product strictly exceed its coefficient bound and verifies available roots at the chosen transform length. Direct coefficient comparisons with an independent schoolbook oracle pass, and deliberately insufficient CRT capacity is rejected. Carry propagation and reconstruction then recover the full integer product. Signed digits/negative inputs are not supported by these routines and were not claimed.

The statement about Z/(p^d) is correct: its unit-group order is p^(d−1)(p−1); for Mersenne prime p with m≥2, p−1=2(2^(m−1)−1), so its 2-adic valuation is exactly 1. Lagrange's theorem excludes a unit of order 4 and larger power-of-two orders. The cited source was inspected: Trinity College Dublin notes, §4.2, Proposition 4.14, PDF page 81 (printed page 4–14), explicitly states the prime-power unit-group order: https://www.maths.tcd.ie/pub/Maths/Courseware/428/Primes-II.pdf#page=81 . The exclusion is the review's immediate deduction from that fact. It concerns this residue ring only; it does not forbid using Q as a radix with other convolution moduli, or establish a lower bound for extension-field transforms or arbitrary algorithms.

## 2. Reproduction and additional coverage

The original sources and original output artifacts are frozen under `source_snapshot/`, with SHA-256 values in `SOURCE_HASHES.json`. The originals were rerun on a local copy and their regenerated data preserved separately under `reproduced/`.

Original tests reproduced:

- 375 complete schoolbook control products
- 375 round trips
- 215 exact single-p divisions
- 210 grouped division/round-trip cases
- 69 parameter-sweep configurations, with three full measured runs per configuration
- 12 matched-size method configurations, with five full measured runs per configuration

The original JSON's grouping count of 210 is a count of cases, each performing both a division and round-trip check; it is not 210+210 independently drawn inputs.

Additional independent tests in `independent_verify.py`:

- 102,400 exhaustive grouped divmod checks: x=0..4095 over 25 (m,d) combinations
- 3,412 boundary/random division checks, including Q^k±1, powers of two, and widths through 1024 bits
- 3,412 encodings checked against native-divmod positional digits and an independently written polynomial reconstruction
- 192 extra schoolbook products
- 960 exact NTT/CRT coefficients checked against independent convolution
- 200 complete NTT/CRT product pipelines, covering zero, asymmetry, all-ones carry cases and random values
- One deliberate CRT-capacity rejection
- Exact primality checks for all seven tested Mersenne primes and seven small no-order-4 controls

The conversion tests include m=4, p=15, as a positive control that conversion does not require primality. These finite tests supplement, rather than replace, the invariant proof above. Details: `INDEPENDENT_CORRECTNESS.json` and `INDEPENDENT_RUN.log`.

The original sweep reproduced its negative direction: best Mersenne versus binary medians were approximately 0.216/0.151 ms at 256 bits, 1.681/0.559 ms at 1024 bits and 5.828/1.181 ms at 2048 bits. The original matched grouped run reproduced 75.658 ms for grouped folding versus 6.352 ms for binary at 8192 bits. Machine load and runtime noise preclude expecting identical decimal timings.

## 3. Comparator audit and accounting repair

### What is comparable

Both paths use the same allocated integer operands, NTT implementation, CRT routine and coefficient-carry code. Their timing interval includes digit conversion, convolution, carrying and reconstruction. The final built-in multiplication assertion is outside that interval. Root/setup work is inside it. Input ingestion is excluded symmetrically. The 38-bit matched comparison uses Q=(2^19−1)^2 against 2^38. Their logarithmic digit capacities are not literally identical, but the realized digit counts, transform lengths and modulus counts are identical for all four recorded inputs.

At 8192 bits, both have 216 digits, 512 transform points, three primes and 20,736 butterflies. No reduction in transform work has been demonstrated. A tuned binary-width sweep is also supplied; it is legitimate to tune both representations rather than comparing grouped Mersenne to an unnecessarily narrow binary radix.

### Necessary qualifications

1. **Unequal diagnostics inside original timing.** `check.py:8,19,26–27` updates ledgers and calls bit_length while binary conversion/reconstruction does not. Grouped conversion still updates a fold counter (`grouped_fold.py:11`). These medians validly describe the executed implementations, but do not isolate intrinsic representation costs or fully optimized algorithms.
2. **Partial ledger, not a bit-complexity certificate.** `check.py:45` creates and discards fresh carry-fold ledgers. `multiply` records scalar operand widths but not complete shift/add counts. Digit assembly executes `a*weight` or `r*weight` (`check.py:18,45`). The saved scan proxies do not itemize every shift, mask, arithmetic operation, allocation, memory movement or carry operation. No global bit-cost upper bound or asymptotic theorem should be inferred from them.
3. **Finite backend.** Three fixed CRT primes provide bounded coefficient capacity and bounded transform lengths. This code is not an unbounded-N multiplier implementation, and it does not establish how to scale the modulus family.
4. **Timing limitations.** Original rows keep medians, not raw per-run distributions; methods are tested in fixed order with one input pair per size. The components are independently computed medians, so their sum need not equal the median total. No statistical significance, global optimum, asymptotic rate, or comparison with optimized native FFT/NTT libraries follows.
5. **No matrix algorithm is tested.** Reshaping digits into an M×M view is a dimension/width observation only. There is no implemented fast matrix kernel or paid reduction showing that reshaping solves integer multiplication more cheaply.

Suggested replacement for REPORT.md's closing accounting sentence:

> The timings include all executed conversion, convolution, carry and reconstruction work. The separate check.py ledgers are partial diagnostics, not a complete bit-operation invoice; in particular, carry-fold work and digit-assembly work are not fully recorded. The original Mersenne timings also include diagnostic ledger overhead absent from the binary path.

A second short addition should cite this independent review and its clean comparator while retaining the unresolved-speedup conclusion.

## 4. Clean matched control

`independent_verify.py` adds a clean 38-bit matched comparison using the same original NTT/CRT backend, the same input-generation seed and one fixed pair per size. It runs nine randomized-order measured repetitions after warm-up and retains every raw trial. All methods use the same complete pipeline and native coefficient carry. Diagnostic work is removed; the clean helpers also inline some calls, hoist radix constants within conversion, and use the proved one-subtraction d=2 finish. Therefore this is an additional clean implementation control, not a claim that deleting only one counter accounts for the timing changes.

The extra `p2_native_divmod` method extracts digits with native divmod by the exact same Q=(2^19−1)^2, then uses the same Mersenne reconstruction. It isolates whether the large penalty is unavoidable for that radix or is largely specific to these repeated folds; it is not a new bit-trick algorithm or a different radix.

Median complete time in milliseconds:

| Operand bits | Clean sequential p folds | Clean grouped p² folds | Same-Q native divmod | Binary 2^38 |
|---:|---:|---:|---:|---:|
| 256 | 0.181 | 0.172 | 0.160 | 0.152 |
| 1024 | 1.027 | 0.906 | 0.587 | 0.563 |
| 2048 | 3.370 | 2.883 | 1.300 | 1.249 |
| 8192 | 83.663 | 66.909 | 7.242 | 6.409 |

At 8192 bits, clean grouped folding spends 60.044 ms on conversion and 66.909 ms end to end, versus binary's 0.069 ms conversion and 6.409 ms end to end. The same-Q native-divmod control takes 0.495 ms conversion and 7.242 ms end to end. Thus the tested grouped fold remains slower even after removing diagnostics and simplifying helper overhead. But the large fold/binary ratio must not be presented as an inherent lower bound on the requested radix; a conventional converter on that very radix nearly removes most of the gap in this bounded experiment.

No tested clean Mersenne implementation beats its matched binary control here. The native-divmod row is still slower and offers no asymptotic result. Raw data and runtime metadata are in `UNINSTRUMENTED_BENCHMARK.json`.

## 5. Exact closure boundary

### Closed for this packet

- The exact requested p^d representation is implemented and canonical for nonnegative integers.
- Single-p and direct p^d fold formulas compute exact quotient/remainder, and reconstruction is exact.
- All specified bounded arithmetic controls and the independent additional controls pass.
- The fixed NTT/CRT backend is an exact conventional comparison within its capacity.
- Direct d=2 grouped folding improves the tested sequential folding implementation.
- These sequential/grouped Python bit-fold implementations do not win against the matched binary comparator on tested inputs; the direction survives the clean control.
- The prime-power-ring root obstruction is correctly scoped to Z/(p^d).

### Still open; not closed by these tests

- Any asymptotic integer-multiplication speedup from this representation
- A complete bit-cost theorem including conversion, wider coefficients, carry/reconstruction and scalable backend
- A faster matrix kernel or a complete paid reduction to matrix multiplication
- Whether another algorithm on the same p^d radix could win at other sizes or after optimization
- Global tuning over m and d or any conclusion over all Mersenne primes
- The extension-field route, which requires a separate representation and cost analysis
- Fastest-library performance, or a universal impossibility result

Recommended final status: **EXACT-RADIX CORRECTNESS ACCEPTED; BOUNDED BIT-FOLD SPEEDUP NOT OBSERVED; ACCOUNTING WORDING REPAIR REQUIRED; GENERAL SPEEDUP GOAL OPEN.**

## Reproduce

From the parent workspace, run:

    python mersenne_independent_finalization/independent_verify.py

To rerun the unmodified original programs without overwriting the frozen snapshot, copy `source_snapshot/` to a fresh scratch directory and run `check.py`, `test_grouped.py`, `benchmark.py`, and `compare_grouped_full.py` there. Their outputs are written beside their source files. Assertions must be enabled.
