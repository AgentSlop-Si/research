# Exact Mersenne-prime-power radix: finalized bounded experiment

2026-10-15

## Result and scope

The precise requested representation, p=2^m−1 prime and grouped radix Q=p^d, works exactly. Direct folding by Q, including the simple d=2 formula, is correct. The implementation and additional independent checks recover exact integer products.

The tested bit-fold implementations do **not** beat a matched binary-radix implementation end to end. Direct p² folding improves the earlier sequential p-fold conversion, but conversion remains the dominant cost. A conventional native-divmod converter using the same exact Q removes most of that penalty in the tested range, so the penalty must not be attributed to every algorithm on the requested radix.

This closes a bounded implementation experiment. It does not establish an asymptotic speedup, a general impossibility result, an optimized-library performance result, or a matrix-multiplication reduction. The broader speedup goal remains open.

This report incorporates the independent arithmetic checks and comparator/accounting corrections in `REVIEW.md`. The previously delivered report and source are preserved unchanged in `source_snapshot/`, with hashes in `SOURCE_HASHES.json`.

## 1. Exact conversion on the requested base

The domain is nonnegative integer inputs, integer m≥2 and integer d≥1. The experiments select Mersenne-prime p values. The conversion identities themselves do not require primality.

### Sequential p folding

For x=A·2^m+B with 0≤B<2^m,

    x=A p+(A+B).

Maintain original_input=q p+x. Updating q←q+A and x←A+B preserves this invariant. Each loop iteration decreases the residual by A p>0. On exit x<2^m=p+1, so at most one final subtraction produces the exact quotient and a remainder in [0,p).

Extracting d successive base-p digits yields one canonical base-Q digit. Reconstruction multiplies by p using (x<<m)−x, repeated d times for multiplication by Q.

### Direct grouped folding

Let S=2^(md) and K=S−Q. If x=A S+B with 0≤B<S, then

    x=A Q+(B+A K).

Maintain original_input=q Q+x and update q←q+A, x←B+A K. Since 0<K<S, the residual stays nonnegative and decreases by A Q whenever the loop runs. The loop terminates; final subtractions of Q make the remainder canonical. This computes exact quotient and remainder, not only a residue.

For d=2,

    Q=(2^m−1)^2=2^(2m)−2^(m+1)+1,
    K=2^(m+1)−1,
    A K=(A<<(m+1))−A.

The direct fold therefore uses the all-ones structure while staying on Q=p². For m≥2, Q>2^(2m−1), so at most one final subtraction is needed after the main folding loop.

For general d,

    K=sum(j=1..d) (−1)^(j+1) binom(d,j) 2^(m(d−j)).

The code evaluates this paid binomial expansion. Its terms, coefficient widths and arithmetic are real work. For growing d, the residual contraction can weaken and the final subtraction count need not be constant: it can reach floor((2^(md)−1)/Q). The d=2 simplification does not establish a uniformly cheap general-d converter.

Q is not an md-bit all-ones word. For example, p=7,d=2 gives Q=49, whereas 2^6−1=63.

## 2. Width and backend accounting

With w=log2(Q), an N-bit operand has approximately L=ceil(N/w) digits. Before carrying, a nonnegative product coefficient is bounded by

    min(L_a,L_b)(Q−1)^2,

and therefore needs approximately 2w+log2(min(L_a,L_b)) bits. Grouping reduces the visible digit count while widening scalar work. Merely reshaping L digits into a square matrix does not provide a multiplication algorithm or make those entries constant-cost scalars. No matrix kernel is implemented in this packet.

The benchmark uses the same conventional radix-2 NTT/CRT backend for Mersenne and binary radices. It selects enough of three fixed NTT primes that their product strictly exceeds an input-specific nonnegative coefficient bound. It checks that the chosen transform length has the required roots. Modular multiplication, CRT reconstruction, native coefficient carry and final integer reconstruction are executed inside the timed interval. The built-in multiplication oracle is checked after the timer stops.

The backend is finite: the fixed primes bound coefficient capacity and supported transform lengths. No scalable family or unbounded-N complexity theorem is supplied.

### What the diagnostic ledgers mean

The timings include all executed conversion, convolution, carry and reconstruction work. The separate `check.py` ledgers are **partial diagnostics**, not a complete bit-operation invoice:

- Carry folding constructs temporary ledgers that are discarded.
- Schoolbook control data record operand widths, not all shift/add work.
- Digit assembly executes arithmetic such as a·weight or r·weight that is not fully itemized.
- Scan proxies do not account individually for every mask, shift, addition, allocation or memory movement.

Arbitrary-width shifts and additions are not assumed to have constant bit cost. Fold counts alone do not establish a bit-complexity bound. The original Mersenne timings also contain ledger updates and bit-length bookkeeping absent from the binary path; they describe those executed implementations rather than isolated intrinsic radix costs. The independent clean comparison below addresses this caveat without claiming an asymptotic result.

## 3. Radix, residue ring and extension field are distinct

1. **Radix Q=p^d:** exact positional grouping, implemented here. Its convolution can use unrelated exact moduli, as this benchmark does.
2. **Residue ring Z/(p^d):** for odd prime p, its unit group has order p^(d−1)(p−1). With p=2^m−1 and m≥2, that order has exactly one factor of 2. Thus it contains no unit of order 4 or any larger power of two. Increasing d alone does not create long radix-2 roots in this ring.
3. **Extension field F_(p^d):** a different algebraic representation, with field-coordinate operations and reconstruction that must be charged. It is not implemented or ruled out here.

The unit-group formula is given in Trinity College Dublin course notes, §4.2, Proposition 4.14, PDF page 81: https://www.maths.tcd.ie/pub/Maths/Courseware/428/Primes-II.pdf#page=81 . The no-order-4 conclusion is the immediate deduction from this formula and Lagrange's theorem. It is not a lower bound against the positional radix or arbitrary transforms.

## 4. Correctness evidence

The original controls were rerun successfully on a copy of the source:

- 375 complete schoolbook control products
- 375 round trips
- 215 exact single-p divisions
- 210 grouped division/round-trip cases
- Small prime-power no-order-4 controls

The independent audit adds:

- 102,400 exhaustive grouped divmod checks
- 3,412 boundary/random division checks
- 3,412 encodings checked against native-divmod positional digits and independent polynomial reconstruction
- 192 schoolbook products
- 960 NTT/CRT coefficients checked against independent convolution
- 200 complete product pipelines, including zero, asymmetric, carry-heavy and random inputs
- A deliberate insufficient-CRT-capacity rejection
- Exact primality checks for all seven tested Mersenne primes and seven small no-order-4 controls

All pass. Tests include conversion with composite p=15 as a control that primality is unnecessary for those identities. The general nonnegative-input correctness argument is the invariant proof above; finite tests provide implementation evidence. Detailed results are in `INDEPENDENT_CORRECTNESS.json`.

## 5. Original bounded sweep, with its measurement limits

The completed sweep uses input lengths 256, 1024 and 2048 bits; Mersenne exponents 3,5,7,13,17,19; and d in 1,2,4 subject to m·d≤40. Binary widths are 4,8,12,16,20,24,32,40. There are 69 configurations, each with three complete timed runs and exact output checks. An earlier interrupted wider sweep supplies no completed timing conclusion.

Original best reported medians, milliseconds:

| Operand bits | Mersenne-prime-power | Tuned binary radix, same backend |
|---:|---:|---:|
| 256 | 0.221 | 0.156 |
| 1024 | 1.650 | 0.596 |
| 2048 | 5.905 | 1.239 |

The best tested Mersenne setting was p=2^19−1,d=2. At 2048 bits, both winning representations use 128 transform points and three primes. The independent rerun reproduced the same negative direction, with approximately 5.828 ms versus 1.181 ms at 2048 bits.

The direct grouped-fold comparison fixes nominal block width 38 and the same inputs/backend. Original five-run complete medians, milliseconds:

| Operand bits | Sequential p folding | Direct p² folding | Binary base 2^38 |
|---:|---:|---:|---:|
| 256 | 0.261 | 0.201 | 0.155 |
| 1024 | 1.774 | 1.046 | 0.619 |
| 2048 | 6.477 | 3.487 | 1.266 |
| 8192 | 133.863 | 77.032 | 6.614 |

These values are retained as measurements of the original instrumented implementations. The independent rerun gives 129.375, 75.658 and 6.352 ms respectively at 8192 bits. The direction reproduces; the exact decimals are machine-dependent.

All recorded matched cases have equal realized digit counts, transform lengths and modulus counts, despite Q being slightly smaller than 2^38. At 8192 bits, each has 216 digits, 512 transform points, three primes and 20,736 butterflies. No transform-work reduction is demonstrated.

These are pure-Python, bounded, single-input-pair-per-size experiments. The original run order was fixed and only medians were retained. Independently computed component medians need not add to the median total. The results are not statistical guarantees, global parameter optima or comparisons with optimized native libraries.

## 6. Independent clean comparator on the exact same radix

The independent comparator uses the same NTT/CRT backend, original matched-input seed, p=2^19−1,d=2, and complete timed pipeline. It runs nine randomized-order repetitions after warm-up and retains raw trials. Diagnostics are removed; helpers also inline some calls, hoist radix constants and use the proved one-subtraction d=2 finish. This is an additional cleaner implementation comparison, not a claim that removing a counter alone explains every change.

A fourth method uses repeated native divmod by the **same** Q=(2^19−1)^2 and the same Mersenne reconstruction. This is a conventional conversion control, not a new algorithmic breakthrough or a different representation.

Complete median milliseconds:

| Operand bits | Clean sequential p folds | Clean grouped p² folds | Same-Q native divmod | Binary 2^38 |
|---:|---:|---:|---:|---:|
| 256 | 0.181 | 0.172 | 0.160 | 0.152 |
| 1024 | 1.027 | 0.906 | 0.587 | 0.563 |
| 2048 | 3.370 | 2.883 | 1.300 | 1.249 |
| 8192 | 83.663 | 66.909 | 7.242 | 6.409 |

At 8192 bits:

- Clean grouped folding: 60.044 ms conversion; 66.909 ms complete
- Same-Q native divmod: 0.495 ms conversion; 7.242 ms complete
- Binary: 0.069 ms conversion; 6.409 ms complete

Direct grouped folding remains slower than binary after removing diagnostics and simplifying helper overhead. Native division on the same radix is much closer, so the large fold-versus-binary gap is mostly a limitation of these repeated-fold implementations in this experiment. No tested clean Mersenne method beats its matched binary control.

Full trial data, runtime information and method details are in `UNINSTRUMENTED_BENCHMARK.json`; the runnable audit is `independent_verify.py`.

## 7. Final closure

**Accepted:** exact p^d positional conversion and reconstruction; direct d=2 grouped folding; the bounded correctness controls; exact conventional NTT/CRT comparison within its capacity; and the scoped observation that the tested bit-fold implementations do not beat binary end to end.

**Open:** a faster algorithm on this radix, global tuning, a scalable end-to-end bit-complexity analysis, a paid matrix kernel/reduction, extension-field alternatives, and any asymptotic speedup claim.

The experiment is finalized at this scope. The broader research goal is unresolved. Neither publication nor a spreadsheet update is implied by this report.
