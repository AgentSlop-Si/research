Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: 0efc16698960219f7d9e03e6e73a9f1d045ae62429e0bb2f2e7841c8314d50b8

---

# Q32 native API and compiler qualification: independent acceptance review

11 October 2026 UTC.

## Verdict

**Accept the bounded, hook-free versioned C API and the reported GCC 14.2 Linux
x86_64 qualification, with the fixture-cardinality erratum below.** No unresolved
arithmetic, ABI, normal-return mutation, overlap, or concurrency defect was found
within this contract. The complete `Q32::native-qualification` gate remains open.
This accepts an implementation/qualification advance, not a new numerical
theorem, optimized-FFT speedup, discovery, priority claim, or production-readiness
certificate.

The immutable candidate archive is
`Q32_Native_API_Compiler_Qualification_CANDIDATE_2026-10-11.zip`, SHA-256
`560bad5c8b4624a7bed40f1b416c1bb40618e33da76d33b23890d43d72e6afd1`.
The reviewed implementation SHA-256 is
`044d5f5b5a81bd94fb08a4b58c8189506d0ae99372d3ba35f310acca13278753`.
The header SHA-256 is
`883fe6eaba0a8a8e81c5c026656e8b2a9233fc97aa53f27d0b8456dc5db5fc38`.
The table SHA-256 is
`5aa22148816690a49a348c4fe427ec21b33b28471d27f7bfa72eef63ed5f9923`.

The inherited positive normalized F60 contract remains p=32, exact dyadic input,
exact norm at most 65,536, and
`||output - U60 input||_2 < (28R + 22)/2^32`.
Input quantization, relative error, other lengths, precisions or radii, alternate
sign/normalization, outer fusion, and general-N claims remain outside acceptance.

## Nonblocking documentation erratum

The candidate RESULTS.md phrase “1,801 distinct admitted vectors” is inaccurate.
There are **1,801 admitted fixture entries, representing 1,800 unique vectors**.
Zero-based entries 4 and 601 both contain the positive cap in component zero and
zero everywhere else: `basis_0_281474976710656` equals `dense_boundary_1`.
Every reported call is still executed; call totals and successful checks are
unchanged. This review corrects the wording without altering the immutable
candidate seal. Table updates and summaries must use the corrected count.

The reviewer-selected fixture contains 1,608 unique vectors. Eleven also occur
in the candidate fixture, so the union contains 3,397 unique inputs. This is
sample coverage, not the basis of the all-input theorem.

## Provenance and clean reproduction

The reviewer independently verified the archive digest, extracted its 51 members,
and verified all 50 SHA256SUMS entries before executing anything from it. The
candidate source, header, tables, independent oracle and accepted predecessor
review pins matched. Five provenance entries were also compared with the actual
accepted predecessor directories, rather than relying solely on copied receipts.
The preceding accepted native implementation is
`fe21832d5a60c4a5c711a422c81b121bebeb71000942711f88f947d32ec6d5cc`;
the accepted independent oracle is
`63d1892dc9326f8939df1a8edbc36fb7c2087ae910e0beeb6c3c95e559d6b8c7`.

The complete archive-only qualification and cold benchmark were rebuilt and
rerun. All eight compiler-profile test records, exports, full fixture bytes and
14 rigorous true-transform interval records reproduced exactly. Elapsed times
and rebuilt-binary hashes are recorded as fresh observations rather than forced
to match. This reproduced 108,775 candidate API calls and 1,801 separate accepted
source differential-control calls. Expected outputs come from the accepted
independent dense oracle, not the candidate transform.

Only project-authored candidate, predecessor, oracle and reviewer code was
executed. No original historical uploaded program was executed. No repository,
spreadsheet, external service or candidate source was changed.

## Source and arithmetic review

The new source removes public Stats, method, mutation, precision and scalar-test
interfaces. The only defined dynamic export is `q32_f60_eval_v1`; this was checked
on all eight rebuilt shared-library profiles, including instrumented profiles.
The actual C11 callers are separately compiled, and the additional reviewer
callers link to shared libraries rather than just implementation object files.
The explicit fixed-width return and versioned symbol identify this ABI version;
the `size_t`/pointer/native encoding remains the declared 64-bit platform ABI.
Compile guards are necessary target conditions, not automatic qualification of
every compiler that defines GCC-compatible macros.

The source diff was reviewed against the accepted predecessor. The 573-step
recurrence, immutable table bytes, permutation, widened Gaussian formulas and
separate normalization are unchanged. The rounding scale is now fixed at 32;
its unsigned-magnitude, remainder and parity construction is unchanged. Copies
and visibility/namespace cleanup do not introduce another arithmetic path.

The reviewer independently parsed the pinned table, checked every source and
coefficient reference, and propagated exact nonnegative integer bounds through
all operations over the larger component box `|component| <= 2^48`. This
reproduced, without native arithmetic:

- 260 additions, 184 subtractions, 69 central products, 60 normalizations
- Maximum stored component bound 166,431,846,018,056,192, below 2^58
- Maximum combined widened raw component bound
  92,282,779,474,624,083,313,819,648, below 2^87
- Validation-sum bound `120 * 2^96`, below 2^103
- Every operation reads initialized SSA slots; all 60 outputs are final
  normalization results

Consequently the signed 64-bit additions, narrowing and negation, signed
128-bit multiplication and combination, and unsigned 128-bit validation
accumulation stay in range. Extreme signed inputs fail before squaring.
Nearest-even's fixed shifts are valid and its rounded magnitude remains safely
representable. This argument transfers the pinned accepted theorem and also
rechecks its arithmetic-width obligation; sanitizer sampling is supplementary.
The independent 192-bit oracle recertified all central coefficient components
and the normalizer against the pinned table.

## Argument, overlap and failure semantics

Null and exact byte-count checks precede all input/output access. Wrong lengths
return status 1 even for inaccessible pointers or out-of-domain contents. All
input bytes are copied into local typed storage before validation or output.
Domain rejection returns status 2 before the plan/kernel/final copy. Hence every
normal nonzero return preserves all output bytes, including input/output overlap.
The successful final copy reads a separate local output array, so arbitrary
partial overlap and unaligned external buffers do not create memcpy overlap or
alignment undefined behavior. Successful calls write exactly 960 bytes.

This guarantee assumes the declared valid-buffer, lifetime and synchronization
conditions. It does not validate arbitrary address ownership or recover from
false extents, process faults, stack exhaustion, data races or a signal during
the successful final output copy. Those exclusions are correctly disclosed.

## Additional independent controls

The new 1,608-vector fixture targets every preweave-row sign pattern, coherent
large inputs, exact integer points immediately inside the norm sphere, and
near-axis tangent cases. All 120 output components are checked against the
independent dense evaluator. Ten selected new cases additionally satisfy the
inherited error envelope against rigorous 192-bit true-transform intervals.

Across seven separately loaded shared-library variants, the reviewer executed
39,256 additional calls:

- 1,608 complete-output admitted calls per variant
- 2,081 disjoint-output rejects per variant: INT64_MIN/MAX and cap +/- 1 at
  every component, 1,200 just-outside exact norm cases, random box inputs and
  the full signed-cap box
- 1,919 unchanged-buffer rejects per variant, covering every relative overlap
  offset from -959 through +959

Separate C11 shared-library clients passed O3, hardened O2, UBSan, ASan+UBSan,
and an additional ThreadSanitizer build. Each ran 22,268 calls:

- All 1,608 independently selected vectors with varied byte alignments,
  complete outputs, canaries and unchanged separate input
- 260 read-only-output or inaccessible-pointer rejection controls, including
  64-bit byte-count bit patterns and read-only in-place domain failure
- 400 calls under all four floating-point rounding modes with pre-existing
  floating exception flags, unchanged result/rounding mode/flags
- 20,000 concurrent varied-vector calls across eight threads, with both
  directions of arbitrary partial overlap local to each caller and surrounding
  byte preservation checks

Those five C clients add 111,340 calls. Total new reviewer adversarial calls are
150,596, in addition to the reproduced candidate suite. All have zero mismatch.
ASan/UBSan and TSan returned success with empty diagnostic streams. Leak checking
alone is disabled for ASan under the inherited ptrace limitation; no successful
leak check is claimed. TSan's bounded run adds race-detection evidence, not a
proof for arbitrary callers or synchronization patterns. The immutable candidate
correctly says TSan had not been performed at author submission; this review
adds that later observation.

## Resource and concurrency scope

The numerical implementation has fixed local input/output/SSA/plan objects,
const shared tables, no heap allocation, recursion, callbacks, mutable shared
numeric state, lazy initialization, I/O or internal locks. Stable inputs and
independent writable outputs therefore have no shared mutable numerical state.
The varied concurrent tests and bounded TSan run support that source argument.
Caller races on external buffers remain outside the contract.

The payload ledger of 16,768 bytes and per-call fixed-plan copying are accurate.
The O3 reported 6,688-byte entry and 10,104-byte kernel frames are compiler
diagnostics, not a portable total stack/RSS guarantee. The author suite's eight
configured 65,536-byte guarded pthread stacks reproduced across all eight
profiles. The new varied-concurrency clients use ordinary default thread stacks;
they do not broaden the 64 KiB observation. Other runtimes, signal handling,
sanitizer overhead, loaders and deployment resource ceilings remain separate.

No other GCC version, compiler family, architecture, host class or real deployment
has been qualified here. No constant-time, real-time, memory-traffic, physical
resource or security certification follows from these runs.

## Cold benchmark audit

The fresh full-output cold benchmark passed all byte checks. Kernel and direct
methods use the same deterministic dyadic input and a common absolute error
target; each output is compared to its own independent correctly rounded
expected vector. The inherited schoolbook direct method has the stronger
`(11R+6)/2^32` bound. Equality of their output bits is not required.

The reviewer process-cold medians were 0.695245 ms for the kernel and 0.698179 ms
for schoolbook direct, with substantially overlapping ranges. Author submission
had the opposite median ordering. Fresh certification plus process medians
were 55.993088 ms and 79.739772 ms, respectively. Compilation is separately
recorded. The timed boundaries do include process/loader/IPC, input construction,
admission, per-call plan preparation, transform and complete output serialization;
the extra certification series additionally includes fresh pinned preparation.

These are noisy one-host, process-cold diagnostics. They establish no practical
speedup, verified cache-cold behavior, portable latency target, or optimized-FFT
advantage. Installed FFTW without an all-admitted-input error contract for the
exact build does not satisfy the matched-certified-accuracy comparison gate.

## Reproduction

The review bundle contains the exact original candidate archive, reviewer
scripts/fixture/records, and fresh qualification/benchmark reports. From an empty
directory, verify the bundle seal, extract `original_candidate.zip` into
`candidate/`, and verify its SHA256SUMS before running:

1. `PYTHONDONTWRITEBYTECODE=1 python candidate/q32_native_qualification_2200/qualify.py`
2. `PYTHONDONTWRITEBYTECODE=1 python candidate/q32_native_qualification_2200/benchmark_cold.py`
3. `PYTHONDONTWRITEBYTECODE=1 python independent_controls.py`
4. `PYTHONDONTWRITEBYTECODE=1 python run_adversarial.py`

Use the declared GCC 14.2 Linux x86_64 environment. Binary artifacts are generated
locally, not supplied as trusted executables. See REVIEW_RECEIPT.json for the
machine-readable verdict and exact evidence hashes.

## Scope and remaining work

> Independently accepted bounded hook-free p32 positive normalized F60 C API

> and GCC 14.2 Linux x86_64 qualification; 1,801 author fixture entries (1,800

> unique), 108,775 reproduced API calls, plus independent adversarial and

> ASan/UBSan/TSan controls. Full Q32 native-qualification remains open; no

> practical speedup or new theorem/priority claim.

Close only independent review of this exact bounded API/source and tested

compiler/caller slice. Keep open:

1. An optimized FFT comparison with an all-admitted-input certified error bound

   matching the declared target and fully charged relevant cold costs

2. Broader compiler/hardware/deployment qualification

3. Production caller integration beyond bounded C11 tests

4. Actual deployment and physical-resource guarantees

Keep inherited precision/radius/length, input-quantization and outer/fusion

boundaries unchanged. Do not mark the complete Q32 gate or task complete.
