# R25 larger-block audit

17 October 2026. Static algebra/source review and independently recomputed data; no submitted program was imported or executed.

## Decision

**Accept the narrow engineering and negative-scaling conclusions.** No substantive error was found in the regrouping identity, online arithmetic/reduction counts, conservative integer-width bounds, or supplied timing summaries. R25 is an optional reusable-plan experiment. The evidence does not establish a general speedup, an independently reproduced benchmark, novelty, or an `o(N log N)` transform.

At `N=65,536`, the main recorded prepared medians are **97.299046 ms** for boundary-only eight-level R25 and **105.386641 ms** for contemporaneously rerun R24: **1.083121×** comparator/candidate, or **7.6742% less time**. Their cold medians are **158.171393 ms** and **120.522133 ms**: R25 takes **31.2385% more time**. These remain author measurements.

The robust mathematical result is narrower and stronger than an empirical scaling fit: every partition of the same classical butterfly computation preserves **`A=Ng` and `M=Ng/2−N+1`**, where `g=log2 N`. Removing reductions or grouping those operations into larger kernels does not remove this workload.

## Artifact and audit integrity

- Archive: `fft_R25_growing_blocks_2026-10-17.zip`.
- SHA-256: `dbf3d6c92a8529d025e85382a64af59718a38fb4b5b66682552b49ee8bbcaef6`.
- All **46** manifest-covered files verified; the archive also contains its manifest.
- All **19** preserved R24 members match both the R25 provenance record and the earlier reviewed R24 source byte-for-byte.
- All **324** counted sample values, **54** statistical distributions, aggregate/individual JSON copies, and **48** chronological main-run order records are consistent. Recorded randomized orders reproduce from the source's seeds after consuming its input RNG draws.
- The superseded confirmation's **36** samples are retained and arithmetically consistent, but are excluded from the reported 324 calls.
- All **44** stored width records have the claimed ledger, derived coefficient-storage counts, and a measured peak no higher than the stated conservative ceiling. Their measured peaks themselves were not reproduced.
- Reviewer-written exact formal-exponent sanity checks verify **786,420 coefficients across 72 local group maps**. Separate arithmetic checks cover **4,096 arbitrary level partitions through `g=12`**. These are supplementary finite structural checks, not execution of the submitted code or a proof-assistant certificate.

`audit_metadata.py` is a new, standard-library-only auditor. It reads the ZIP and replay receipt as data. `metadata_audit.json` records the results. Run `python audit_metadata.py`; optionally pass `--r24-source` with the prior R24 source directory to repeat the external baseline-byte comparison. Source references below are relative to the ZIP; extracted copies are in `source/extracted/`.

Hashes demonstrate artifact consistency, not independent attestation that the author's computations occurred. Transform-output hashes, measured maximum widths, generated-source character counts, and all runtime measurements were not independently regenerated.

## Algebra and exact accounting

Let `N=2^g`, with a primitive `N`th root `omega` in an odd prime field. A group starts after `s` levels, so `h=2^s`; it combines `q` levels, with `B=2^q`. For the positions `base+j+h*l`, define `w=omega^(Nj/(Bh))`, `zeta=omega^(N/B)`, and let `rev_q` reverse `q` bits. Consecutive DIT levels give

`out_k = sum_l zeta^(k*l) w^l x_(rev_q(l))`.

Equivalently, preweight slot `l` by `w^rev_q(l)` and apply the ordinary bit-reversed-input `B`-point DIT graph with root `zeta`. The source's twiddle table uses exactly these preweights (`fused_blocks.py:117–129`); the emitted butterfly exponents and final output reductions match this graph (`25–61`). The initial global bit reversal and successive groups compose to the full unnormalized positive-root DFT (`105,132–138`). A final shorter group uses the same identity. `N=1` normalizes and returns the single residue.

Delaying a remainder preserves the result because reduction from exact integers to the field respects addition and multiplication. This requires exact integers, which Python supplies here; it is not permission to overflow a fixed-width implementation.

One local codelet uses `Bq` additions/subtractions and `Bq/2−B+1` nonunit multiplications. Across a group, there are `N/B` calls, of which `N/(Bh)` have `j=0` and no preweights. Thus

- `A_group=Nq`.
- `M_group=Nq/2−N/h+N/(Bh)`.

For any partition `q_1+...+q_c=g`, adjacent group widths make the last two terms telescope:

- `A=Ng`.
- `M=Ng/2−N+1`.
- `R_boundary=N(c+1)` including input normalization.
- `R_products=M+N(c+1)` including input normalization.

For fixed maximum block size `q`, `c=ceil(g/q)`. These are online payload-integer arithmetic counts. They exclude planning, coefficient generation, index arithmetic, validation, allocation, and other interpreter work. The selected `vector_reads`/`vector_writes` fields omit the separate type scan, constant/index accesses, local-variable traffic and interpreter traffic; they are not total memory traffic.

At `N=65,536`, R24 and both R25 variants have `M=458,753`, `A=1,048,576`. Including input normalization, R24 has `1,048,577` remainders; boundary `q=4` has `327,680`, and boundary `q=8` has `196,608`. The latter reduction ratio is about **5.33334×**, but this is not a total-work or runtime ratio.

## Integer width, storage, and asymptotics

Set `ell=bit_length(p)` and start after input normalization. For the product-reduced policy, every nontrivial product is reduced, while successive sums grow by at most a factor two per local level. Magnitudes are bounded by `B p` for carried values and `B p²` for unreduced products; `2 ell+q` bits suffice. For boundary-only reduction, preweights start below `p²`, the first level has no internal multiplier, and each later level grows the common bound by less than `2p`. Hence every magnitude is less than `2^q p^(q+1)`, and `(q+1)ell+q` bits suffice. Both bounds are conservative and apply to absolute magnitude, not a signed machine-word representation. Arbitrarily large supplied inputs incur their actual normalization cost first.

For the 30-bit benchmark field, boundary `q=4` and `q=8` ceilings are **154** and **278** bits. The separate author audit reports peaks of **148** and **266** bits. These observations fit the proven bounds; they do not prove those ceilings are attained or independently validate the instrumentation. The clean replay expressly did **not** rerun these two larger-width measurements.

Stored preweights per group are `(B−1)(h−1)` and local constants are `B/2−1`; summing over increasing widths gives `O(N)` stored coefficients. This is a count of residue slots, not bytes or peak resident memory. Source generation emits `O(Bq)` arithmetic statements and pays variable/index-name lengths; ordinary Python compilation is included in cold calls. Trial-division prime validation remains charged and is not uniformly linear in arbitrary `p`.

For a hypothetical uncapped generator, choosing `q=Theta(log g)` reduces explicit remainders to `Theta(Ng/log g)`. It still performs `Ng` additions and `Theta(Ng)` multiplications, with boundary-policy widths `O(ell log g)`. Even granting unit-cost arithmetic on these wider integers does not remove the unchanged operation count. The actual executable only accepts `1≤q≤8` (`fused_blocks.py:13,65–69,95–103`); its growing mode refuses larger choices. The fixed field `998244353=119·2^23+1` only supports power-of-two orders through `2^23`; its growing choice is at most five levels. An infinite asymptotic claim must specify a compatible field/root family.

This is an obstruction for the emitted graph and its regroupings. It is not a lower bound on Fourier transforms, other Green constructions, or a different within-block circuit. See `NEGATIVE_SCALING_BOUNDARY.md` for the exact reuse rule in future searches.

## What the benchmark does and does not show

The main run compares six variants, at `N=1,024,4,096,16,384,65,536`, with nine prepared and three cold calls per variant/size: **288** calls. A separately run, fresh-input confirmation compares three selected candidates with the same repetition counts: **36** further calls. Each main size uses three input vectors; repetition counts must not be described as independent input counts.

Main prepared medians, milliseconds:

| N | R24 | Boundary q=4 | Boundary q=8 |
|---:|---:|---:|---:|
| 1,024 | 0.943728 | 0.852805 | 0.800118 |
| 4,096 | 4.384131 | 4.036708 | 3.867886 |
| 16,384 | 20.825310 | 21.464617 | 18.899314 |
| 65,536 | 105.386641 | 99.758153 | 97.299046 |

The eight-level candidate has lower prepared medians at all four reported sizes. Its ratio against R24 declines from 1.17949× to 1.08312× across those points; no exponent inference is justified. Four-level R25 regresses at `N=16,384`. At `N=65,536`, eight-level R25 wins only six of nine same-trial prepared comparisons; ranges overlap substantially: R24 **103.921249–209.970852 ms**, eight-level R25 **89.946651–223.151247 ms**. It loses all three corresponding cold comparisons. No significance statement follows from these small, dependent same-process samples.

The final confirmation's prepared medians are R24 **115.722870 ms**, four-level **103.562744 ms**, and eight-level **102.216993 ms**; eight-level R25/R24 cold medians are **161.680962/133.537870 ms**. The confirmation direction is consistent, but it is an author check after candidate selection, not external replication. Its earlier version was correctly preserved and excluded because preceding-plan destruction could occur within the next timer; the corrected version releases cold plans outside timers.

The main source uses identical seeded inputs, full outputs, shared root semantics, randomized within-trial variant order, and correctness checks outside the timer (`speedrun.py:24–52`). All methods include input type validation, normalization, permutation, complete arithmetic, and output allocation. Fresh-plan calls add validation, planning, and generated-code compilation. Root generation, RNG, verification, imports and process startup are outside timing. “Cold” means a fresh plan in a running process, not a cold CPU cache. Assignment to `y` can release the previous output inside the timed interval in both benchmark scripts; this is shared behavior, not evidence of a variant-specific speed gain.

Important limits:

1. The optional six-variant `N=262,144` run exceeded a **45-second command limit**. No completed file or partial timings from that attempt are included. This is **no performance evidence at that size**, not a measured per-transform timeout or asymptotic failure. Its planned width audit was subsequently run separately at `N=65,536`.
2. All timed main sizes have even `log2 N`. Different tail sizes and odd-log performance remain unmeasured here.
3. Main metadata record Python **3.13.5 / GCC 14.2.0**, Linux/glibc, **Intel Xeon Platinum 8573C**, enabled GC and the timer. They omit affinity/quota, frequency/governor, allocator/build flags, optimization/JIT state verification, background load and thermal data. Confirmation has no separate environment or chronological-order record.
4. The original R24 publication used an **AMD EPYC 9V74**. Its old numbers must not be compared directly with this Intel run; the R25 report correctly reruns R24 as the comparator.
5. Checks use Python `assert`; optimization flags are not recorded. Source intent to check every output and recorded PASS statements do not independently establish that assertions were enabled.
6. Input generation precedes all timing, prepared precedes cold, and no process-level counterbalanced repetition is recorded. Exploratory screening retained only approximate medians, not its complete samples. The final benchmark preserves unfavorable samples; it does not establish a preregistered candidate choice or absence of selection effects.
7. There is no independently optimized same-language fusion competitor or native exact-NTT library comparison. Comparators share validation/permutation helpers. Complex NumPy/FFTW timings would not supply equivalent exact-field semantics.

## Correctness and replay coverage

The small-suite loop bounds agree with **334 plans**, **4,174 candidate-vector comparisons**, **2,088 basis cases**, **292 inverse roundtrips**, **13 invalid-request rejections**, and **592 input/root cases** in its direct-oracle section. More precisely, **4,132** comparisons are in that direct-DFT section; the remaining **42** are deeper cases at 256, 512 and 1,024 points using the inline radix-two reference. All 334 plans are instrumented according to source, but only the 42 deeper width records are serialized.

The large-suite records agree with **40** full-vector candidate comparisons across **10** shared vectors and **3,489,792** checked output entries. The candidates are boundary `q=4`, boundary `q=6`, products `q=4`, and growing boundary blocks. At `N=262,144`, growing means **q=5**, not q=8 (`validate.py:102–113`). Therefore the large-suite endpoint must not be attributed to the eight-level candidate. Eight-level checks are present in the deeper small suite and at `N=65,536` in timing/width data.

The separate clean-replay receipt matches the archive digest and lists manifest verification plus the exact small and large suites. It explicitly excludes **benchmarks, exploration, and the separate large-width audit**. This review does not upgrade those author-side checks to independent execution, independent human review, or formal verification.

## Attribution and publication boundary

Generated FFT codelets are an established technique described by the [FFTW generator documentation](https://fftw.org/fftw3_doc/Generating-your-own-code.html). Reducing modular-reduction frequency via redundant arithmetic is also established, including [Harvey's NTT arithmetic paper](https://arxiv.org/abs/1205.2926). These references support attribution only; R25's arbitrary-precision boundary policy is not claimed identical to Harvey's bounded-word method. This audit conducted no comprehensive priority search.

A defensible summary is: “R25 preserves the classical FFT arithmetic workload while reducing modular reductions through larger generated kernels. A separate static/data audit found its counts, conservative widths and supplied summaries consistent. The author records a 1.083× prepared-plan improvement over rerun R24 at 65,536 points, alongside a 31.24% cold-time regression. No independent performance replication or sub-`N log N` algorithm is established.”

Before promoting a practical speed claim, use independently reviewed code, explicit correctness failures instead of removable assertions, a pinned environment, repeated fresh processes, counterbalanced mode/size order, tail sizes, and comparable optimized exact-NTT baselines. Preserve the fresh-plan and reusable-plan results separately. None of those performance checks can change the exact negative arithmetic conclusion for this graph.
