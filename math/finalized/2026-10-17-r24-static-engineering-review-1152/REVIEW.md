# R24 engineering review, 17 October 2026

## Decision

**Scoped acceptance: internally consistent classical engineering result, supported by static algebra/source review and a reproducible audit of the supplied data.** No substantive transform-identity, arithmetic-count, or timing-summary error was found. Uploaded programs were not executed, and the reported speedups have not been independently reproduced. This review does not establish novelty, a general sub-`N log N` algorithm, or superiority to an optimized NTT library.

The author reports, at `N=65,536`, prepared medians of 86.776653 ms for R24, 117.948687 ms for inline radix two, and 462.026952 ms for generic R23. Their ratios are correctly calculated: **1.359221×** and **5.324323×**, respectively. Cold medians are 98.302717 ms, 127.838651 ms, and 1739.168944 ms, giving **1.300459×** over inline radix two. These remain author timings.

## Material and reproducibility

- Source archive: `fft_R24_speedrun_2026-10-17.zip`.
- Archive SHA-256: `c82b7f54f626087d40bc6c066f3529846ee5578ddd27d25cf34a18829f2c570c`.
- A separate author-side receipt reports complete exact-validation replay and 32 smoke-timing calls, with no full 336-call benchmark rerun. These are author claims, not independent replay evidence.
- Source-file line references below refer to the reviewed, hash-checked source archive. That archive is not included in this static-review publication.
- This is a publication-safe derivative of the review: private conversation and Library locators were removed; substantive findings and limitations are retained. The original review hash is recorded in SOURCE_BINDING.json.

The review-authored `audit_metadata.py` reads ZIP members as data. It does not import or execute any archive module. Given the separately obtained pinned source archive, run `python audit_metadata.py --archive /path/to/fft_R24_speedrun_2026-10-17.zip` to reproduce `metadata_audit.json`. The source archive is not distributed in this review-only packet. It verifies all **18** manifest payloads, every stored median/range/quartile/ratio, **336** raw sample records, all **18** seeded input hashes, arithmetic-count formulas, and validation-coverage totals from the documented loop bounds. It does not regenerate transform outputs or timings. Matching hashes establish consistency of these artifacts, not independent attestation that the runs occurred. The separate original R23 ZIP was not independently compared; its five preserved-member hashes are internally consistent with the R24 provenance record.

## Algebra and cost

For successive widths `2h,4h`, put `w=root^(Nj/(4h))` and `iota=root^(N/4)`. Ordinary first-level outputs are

- `A=a+w²b`, `B=a−w²b`, `C=c+w²d`, `D=c−w²d`.

The next level gives `A+wC`, `B+iota*wD`, `A−wC`, `B−iota*wD` in the four stored positions. Expanding these expressions gives exactly the R24 code's `w²b,wc,w³d` quartet. Thus the fused kernel is two classical DIT levels, with no discarded input/output or singular inverse. Bit reversal and an optional final width-`N` radix-two level complete the construction. The `N=1` case is the identity over the residue field. See `speedrun_fft.py:33–40,51–76,78–130` and `PROOF.md:25–66`.

After input normalization, operands and multipliers are in `[0,p)`. Each product is reduced before reuse; its magnitude is below `p²`, including the signed `(c−d)*iota`. Unreduced sums have magnitude below `4p`. Exact integer arithmetic therefore preserves the field identity without hidden growing integer packing. Unbounded initial Python integer inputs still incur their actual normalization bit cost.

At width `W=4^k`, each block uses one multiplication in its `j=0` quartet and four in each remaining quartet. Across all blocks this is `N−3N/W` multiplications, `2N` additions, and `2N−3N/W` reductions. Summing the geometric series, including the optional tail, yields, for `g=log2(N)`:

- R24 and inline radix two: `M=Ng/2−N+1`, `A=Ng`.
- R24 reductions excluding the `N` input reductions: `Ng−N+1` for even `g`; `Ng−N/2+1` for odd `g`.
- Inline radix two reductions excluding input reductions: `3Ng/2−N+1`.

The generic R23 count `2Ng` multiplications and `(5N/2)floor(g/2)+N(g mod 2)` additions also agrees with its source. At `N=16`, the R24/inline ledger is 17 multiplications and 64 additions, versus generic R23's 128 and 80. The runtime improvement is consistent with fewer reductions, intermediate stores, and interpreter overhead; these data do not separately measure each cause.

Direct plans store `O(N)` residues and indices. Reading a materialized R23 control still requires `O(N log N)` work. Prime validation uses trial division, so total constructor cost for arbitrary growing `p` is not a uniform `O(N)` bit-complexity claim. For fixed benchmark prime `998244353=119·2^23+1`, supported power-of-two roots stop at `N=2^23`. A genuine asymptotic family must state how its fields grow. Online field/index operation count remains **Theta(N log N)**.

## Benchmark fairness and limitations

The source does several things correctly (`speedrun.py:55–107`): four same-interpreter variants, identical seeded inputs and roots, full outputs, randomized variant order within every trial, prepared/cold separation, and correctness checking outside the timers. R24 and the stronger inline reference share validation, normalization and bit reversal; both skip unit twiddles. Cold timing includes fresh prime/root validation, plan construction and execution. Input generation, supplied-root generation, imports, process startup, checksums and comparisons are excluded for all variants. Temporary-plan/output destruction is intentionally outside timing. “Cold” therefore means a fresh plan in an already-running process, not a cold CPU/cache or fresh process.

The raw data contain six sizes × four variants × (nine prepared + five cold) trials = 336 samples. At `N=65,536`, even the slowest R24 sample is faster than the fastest inline sample in both modes; this is encouraging within-run evidence, not a cross-machine confidence statement.

Limitations:

1. **All timed sizes have even `log2(N)`**: 16, 256, 1024, 4096, 16384, 65536. Odd-log tail correctness is covered by author validation; its performance is not measured here.
2. Random ordering is appropriate but not exact position balancing. Nine/five trials in one process do not establish cross-run variation; chronological order and CPU frequency/load are not logged. All prepared measurements precede cold measurements, and sizes increase monotonically.
3. Recorded metadata include Python 3.13.5/GCC 14.2.0, Linux/kernel/glibc, AMD EPYC 9V74, `cpu_count=5`, GC enabled, and single-thread intent. Affinity/cgroup quota, frequency/governor, Python optimization flags, build/allocator details, background load and thermal conditions are missing. `cpu_count=5` is not proof of five dedicated CPUs. Correctness uses Python `assert`; a future replay must verify assertions are enabled or replace them with explicit checks.
4. The inline reference is materially stronger than the generic solver but is still one ordinary Python radix-two implementation. Neither an independently optimized same-language fused kernel nor a native optimized exact NTT library was tested. FFTW/NumPy complex transforms would not be a directly equivalent arithmetic baseline.
5. The **author clean replay reran exact validation and a 32-call CLI smoke benchmark only**. The receipt explicitly says the full 336-call benchmark was not rerun. This review also did not rerun it.

The existing report already limits its headline to local measurements, so these are boundaries and next-validation requirements, not evidence that the recorded numbers are false. `PERFORMANCE_GATE.md` specifies the independent gate.

## One narrow overbroad claim

The statement that the compatibility checker rejects every altered control is broader than its actual shape checks. `compile_r23_control` compares the first `n` entries of the five coefficient/route arrays (`speedrun_fft.py:245–261`) but does not explicitly require those arrays to have length exactly `n`.

A static counterexample construction is: create the ordinary `FourierControl(4,4,Field(17))`, then append `0` to `control.stages[0].a`. The compiler's root extraction, metadata checks and four compared entries are unchanged, so this extra unused entry is accepted. The baseline `Stage.apply` also reads only indices `0…n−1` (`baseline_r23/fusion.py:71`), so the original and compiled transforms remain identical. **This is an inert trailing-entry acceptance, not a wrong-transform counterexample.** The construction was reasoned from source, not executed. The 48 recorded active-entry/cycle/order/flag rejection tests remain consistent with their stated coverage.

Suggested wording: “checks all execution-relevant coefficients/routes and rejects the tested semantic mutations.” Alternatively add exact-length checks and a trailing-entry regression case. No source files were changed by this review.

## Publication boundary

A defensible statement is: “A static review verified the classical fused-butterfly identity and arithmetic counts, and independently recomputed the supplied benchmark summaries. The author reports a 1.36× local prepared-plan gain over the bundled inline Python radix-two reference at 65,536 points. Independent performance replication and optimized-NTT comparisons remain open.”

Keep this engineering review separate from any other research branch's proof or promotion gate. Do not describe data-only validation as a benchmark replay, formal verification, external human review, or a new Fourier complexity result.
