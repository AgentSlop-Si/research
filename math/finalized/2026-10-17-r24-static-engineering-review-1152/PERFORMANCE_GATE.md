# Independent R24 performance-validation gate

This is a proposed experiment specification, not a record that it ran. Stop with a qualified conclusion once the predeclared experiment is complete; do not stop early at a favorable result or extend selectively after an unfavorable result.

## 1. Pin artifacts and semantics

- Pin the R24 ZIP by SHA-256 and every comparator by commit/version and build digest. Obtain independent source review before execution.
- Check exact positive-root, unnormalized length-`N` DFT semantics over the same prime, full outputs in canonical order, same input-preservation contract and residue normalization. Require exact equality, not a floating tolerance.
- Independently replay the supplied full correctness suite with assertions enabled and add basis/direct-DFT checks using a separately written reference. Record `sys.flags.optimize` and `PYTHONOPTIMIZE`; explicit error checks are preferable. Correctness/benchmark checks must not vanish under `-O`.
- Gate failure on any mismatch; do not time only favorable vectors. Include dense random inputs, noncanonical signed residues, and structured/adversarial inputs outside the timer.

## 2. Fixed measurement contract

- Preserve two principal results: (a) prepared plan plus complete one-vector execution, including normalization, permutation, allocation, and output; (b) fresh validation/plan plus the identical execution contract.
- Report process/import startup separately if wanted. Label fresh-plan timing clearly: it does not flush hardware caches. Report validation, planning, conversion and execution as separate breakdowns as well as end-to-end totals.
- Hold the supplied-root assumption fixed for all methods. If a comparator discovers roots internally, expose a comparable precomputed-root mode or count root generation for everyone in an additional comparison.
- Keep temporary output/plan destruction policy consistent and documented. Record peak resident memory and plan storage, not just logical scalar count.

## 3. Hardware/runtime record

Record CPU model/stepping and enabled ISA, allocated cores, affinity, cpuset and CPU quota, governor/frequency/turbo policy, RAM, OS/kernel/libc, Python executable hash/version/build configuration, optimization/JIT status, allocator settings, GC state, all native compiler versions/flags, library versions, thread counts and relevant environment variables. Record background load and throttling/temperature indicators where available. Pin single-thread runs to a stable allocated core if supported. Never infer dedicated cores from `os.cpu_count()` alone.

## 4. Order and statistical design

Predeclare the principal endpoint `N=65,536` and other reported sizes; include adjacent odd-log sizes, e.g. `2^9…2^18`, plus the original small cases. Predeclare seeds, process repetitions and analysis before collecting timings. One reasonable design is 10 independently launched processes, with at least 12 prepared and 8 fresh-plan samples per variant/size/process after equal untimed priming. Log every chronological variant/size/trial/input ID and elapsed time.

Use counterbalanced variant positions and randomize size/mode blocks across processes so variant, process age and increasing size are not confounded. Keep identical input IDs within paired comparisons. Do not discard outliers without a predeclared mechanical rule and show results both ways if any are excluded.

Report raw samples, per-process estimates, ratio-of-medians and paired comparisons, plus a confidence interval based on independent process blocks rather than treating all same-process samples as independent. Predeclare practical equivalence margins. To claim an independent local speedup at the primary endpoint, require exact correctness and a predeclared interval wholly above a ratio of 1 for comparator/R24; otherwise report the result as inconclusive or no observed win. A cross-machine claim additionally needs the same protocol on independently characterized machines.

## 5. Comparable optimized NTT baseline

Use two comparator tiers:

1. **Engineering isolation:** retain the bundled inline radix-two reference, and add an independently reviewed optimized Python radix-four/fused/deferred-reduction implementation with the same API. This asks whether the advantage survives beyond the specific baseline layout.
2. **Practical throughput:** add a pinned, established native exact NTT implementation that supports the same `(p,N)` and output convention. Include Python/native conversion, layout/permutation, normalization, input-copying and wrapper costs in end-to-end comparisons. If separately comparing native kernels, port both methods comparably or label the language/ISA distinction; retain an end-to-end result too. Use the same thread budget and report ISA acceleration.

Do not substitute a library's negacyclic NTT or convolution routine without proving and charging its adaptation to this cyclic DFT. For example, Intel HEXL documents a **negacyclic** NTT and an Intel-targeted API, so it is a candidate only after verifying the current hardware path, modulus/length support, root/order convention and exact adaptation. Its out-of-box timing is not automatically comparable. [Intel HEXL official repository](https://github.com/IntelLabs/hexl).

Planning and execution should remain distinct; established FFT software explicitly trades planning time against execution strategy. That supports the measurement distinction, not any R24 performance conclusion. [FFTW planner documentation](https://www.fftw.org/fftw3_doc/Planner-Flags.html).

## 6. Deliverable and decision

Publish source hashes, environment record, exact invocation/configuration, independent correctness receipt, raw chronological timing data, analysis script and uncertainty summaries. Preserve the old values as author timings even if new results differ. Report separately: identity/count correctness, independent replication versus the bundled reference, same-language optimized comparison, and native-library comparison. None of these performance outcomes changes the proven `Theta(N log N)` operation count or establishes novelty.
