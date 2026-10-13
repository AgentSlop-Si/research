# Q16 resource-blocker evidence: independent review

2026-10-13 UTC

## Verdict

**ACCEPT_RESOURCE_BLOCKER_EVIDENCE_ONLY. No evidence repair is required.**

The one recorded approved attempt terminated by SIGXCPU, and the external receipt correctly records the resource outcome. This accepts the source-bound resource-blocker evidence. It does not accept or reject numerical integration, establish any individual case completion, or authorize another run. Actual source-pinned same-class integration and paid-ledger reconciliation remain unestablished.

The reviewer read the sources, launcher, receipts, reports and seals and ran only a new inert hash/JSON/archive/AST checker. All 124 checks passed. No scientific module, candidate harness, external launcher, authoring utility or historical test was executed by this reviewer.

## Exact evidence binding

- Candidate archive: `Q16_Pinned_Integration_Resource_Blocker_2026-10-13.zip`, 72,113 bytes
- Archive SHA-256: `87aa46bd62b491f4beea1bd55f988d2081aae8a2cf16b5fd866f3ee7383d2261`
- Candidate manifest SHA-256: `db8c3b6293e956461d6c8198b3b4aa9c728635e9ae5862ba71282aec47b0e4ce`
- Post-exit receipt SHA-256: `82f335db0c0d1c2c1ee23f8df0758ec39d0061aaff84ad277771a4ab9cc1afb2`
- Launcher SHA-256: `526fd4fd652fe98dc88182baf68667d9eaaadf718645a69ac46eb01eea2f7369`
- Original contract SHA-256: `5cacca0da872029d62c7f5d498310ae4c6a1a1a4ef997c735ec650163fb7ffce`
- Frozen harness SHA-256: `2fbc1e77618b095cf11ef367b55806e507745922ef4f7ba9fade88c827f7e236`
- Prior independent static-review archive SHA-256: `a39b2c4ca2ffd4d8fd2e713564f34ae42ea47375ec00c4f8bd5bc3f248c7d3a5`

All 13 unique resource-archive members agree with the sealed working copy. Its seal and all 11 manifest payloads verify. The nested frozen contract and independent static-review archives retain their exact pins. All 15 original contract payloads remain unchanged, independently checked against current files rather than trusting the post-run booleans alone.

The six scientific pins remain:

| Module | SHA-256 |
|---|---|
| exact_source | 8334e657dd0048bdb91459e5f6e126080c7513d341ef3d17665b05422a8bbada |
| compact_window | e29741e71c276c156d708f1d9dce6d60ff9d3d2c34a6045b03630c46506dac59 |
| buckets | df3937a632217a8a1342545b803169ff8da062117b3837796386509b64f650d1 |
| location_decode | e3b592c40906d860d58c12cf7e21f17c6560cb8c95e7bcde4c161b0d52881c3a |
| phase_medians | 45c0c6a59cac18912278dcda183fe8e5bea2a19398cb61fc1bf8ec97cac5a788 |
| pipeline | c3a2da5a11ceba2cfa0df7bbb346525013e740e7bc170b3d27dfadc3f2be4d3b |

The runtime executable currently matches SHA-256 `fa67443527ed9647f760d807e2a38f26340757123e643c4639cf273ed15d5ea7`, and CPython version/direct standard-library source pins match the contract. Launch checks bind these same values. The unchanged trusted-runtime assumption covers transitive stdlib and bytecode; these records are not a new operating-system attestation or proof against concurrent malicious tampering.

## What the receipt establishes

| Observation | Recorded value |
|---|---:|
| Started UTC | 2026-10-13T20:27:57.105497+00:00 |
| Observed exit UTC | 2026-10-13T20:29:59.304473+00:00 |
| Raw wait status | 24 |
| Child exit-code representation | -24 |
| Terminating signal | SIGXCPU (24) |
| User CPU seconds | 122.105437 |
| System CPU seconds | 0.029787 |
| Total CPU seconds | 122.135224 |
| Elapsed wall seconds | 122.19877721200464 |
| Peak RSS KiB | 45,240 |
| External wall deadline triggered | false |
| stdout / stderr bytes | 0 / 0 |
| Scientific result file | absent |
| Recorded attempts / retries | 1 / 0 |

The raw wait status independently decodes to SIGXCPU and exit representation -24 using standard-library wait-status routines. CPU fields sum correctly. Monotonic elapsed time agrees with the UTC timestamps within stamping overhead. Both empty-log digests verify, and the result is absent in the current filesystem as well as the receipt.

The configured CPU limits were soft 120 seconds and hard 125 seconds. The observed total is 2.135224 seconds above the soft value and below the hard backstop. The evidence therefore **does not establish measured CPU <=120 seconds**. It records observed signal-delivery/accounting overshoot without claiming that the threshold was raised. No kernel event trace is supplied to attribute the precise overshoot mechanism; none is needed to identify the recorded resource blocker. Under the inspected program and trusted-host premise, SIGXCPU is consistent with the configured CPU boundary. The wall deadline did not fire.

RSS is a high-water diagnostic, not address-space consumption or source-model storage. The 512 MiB address-space cap must not be misrepresented as an RSS measurement. No scientific output, successful constructor receipt, final ledger count or source-model paid total was emitted.

## Launcher and stopping behavior

The launcher is additive and does not change the approved scientific bytes, harness, input cases, runtime or caps. Before its single subprocess creation, it checks original/archive/review pins and manifests, rejects an existing scientific result, and creates its launch receipt exclusively. Existing receipt/log files prevent silently repeating the same output-directory launch. Its source contains one Popen call site and no retry loop.

The child command exactly preserves the approved interpreter, `-I -S -B`, absolute harness path and exact --run-approved contract digest. The launcher sets CPU (120,125), address space (536870912,536870912), regular-file size (8388608,8388608), descriptors (64,64) and core (0,0) before exec. Thus startup is covered, strengthening the original harness's post-import installation of identical limits. The child receives closed unrelated descriptors, stdin from DEVNULL, controlled local stdout/stderr files and a minimal environment. A new session makes the 180-second emergency group kill target the spawned child group.

The parent polls wait4 for this exact child. On termination it receives that child's final resource record, decodes the status, closes the logs, measures elapsed wall time, hashes/stats the logs, tests result existence, and writes a separate post-exit JSON receipt. In this SIGXCPU path the parent remains alive, so the child CPU limit cannot prevent the receipt write. The receipt is complete and sealed. The launcher's own final exit 1 communicates child failure; it does not replace the child's recorded -24 status.

These operations are local. Source inspection finds no upload, account operation or network action in the launcher or six scientific modules. The previous source-safety boundary and audit-hook limitations remain in force. The runtime and launcher are trusted fixed code; the evidence is not intended as adversarial host forensics.

The post-exit receipt's generic scope string names startup, reconciliation, serialization and shutdown. The delivery addendum and report explicitly limit it to work **actually performed before termination**. They do not assert that every listed stage was reached. This clarification resolves the static-review resource condition. The alias-control addendum also accurately restricts the authored post-return mutation checks to nonzero cases, without claiming they completed during this interrupted run.

## Limits of inference

The harness has no progress checkpoints and writes its scientific result only after its success path finishes. Empty logs and absence of that file establish no completed numerical artifact. They do not identify the active function, the number of imported modules, a completed constructor/case, or the state of the independent ledger observer at interruption. The planned six successful constructors, six consumers, nine ledgers and fourteen in-profile reports cannot be reported as achieved counts.

Likewise, SIGXCPU is neither an arithmetic counterexample nor a successful conformance result. Prior scoped source-level acceptances are preserved. No all-length, recovery-probability, dense-fallback, interpolation, outer-rounding, amplification, alpha-endpoint, exact-DFT, relative-l2 or speed conclusion follows.

## Static cost observations, not a timeout diagnosis

The following are reproducible source-level observations relevant to a future, separately reviewed proposal. No timing experiment, historical rerun or parameter change was performed.

1. `integration_harness.py:137–145` is a global profile callback. Before rejecting unrelated filenames/events, each callback reads the frame and constructs/stringifies `ROOT/'source_bytes/compact_window.py'`. This is in-memory pathlib work, not filesystem resolution. Unselected Python and C profiling events still incur this dispatch overhead.
2. The 5,000,000 cap increments only selected Ledger method `call` events at lines 147–149. It is not a cap on total profiling callbacks. Return and C events, numerical helper methods, harness/reference work and trusted-library calls can invoke the callback without incrementing that counter.
3. Selected record observations duplicate integer-width/counter work deliberately for independent verification. Widths are reconstructed by `bin(abs(x))` and frame locals are inspected. This is paid runtime/verification overhead, separate from the scientific schoolbook ledger.
4. The plan intentionally pays six separate actual/reference pipelines and one extra engine. Each engine repeats window, root and scale preparation. That repetition is part of the approved finite control design, not an accidental unpaid reuse.
5. `phase_medians._phase` creates a fresh Scalar for every candidate; Scalar constructs its Machin pi enclosure. The planned q=1 paired cases would collectively perform 64 phase preparations. The q=0 cases omit per-candidate phase work but still require their consumer preparations. None of those planned counts is confirmed as reached here.

A future design could examine cached immutable dispatch keys, exact code-object filtering, or fresh synthetic profiling controls while preserving independent ledger semantics. Any resulting harness change or new historical run requires a new frozen review and an approval-scope check. This review makes no such change and gives no rerun permission. The observed timeout cannot be attributed to any one hotspot without additional authorized evidence.

## Disposition

The resource blocker is accepted at its exact recorded scope. The approved one-shot operation is over and stopped. No retries, expanded caps, smaller replacement cases, changed instrumentation or other historical executions were undertaken by this review. Preserve the inconclusive numerical status and surface the resource result separately from scientific acceptance.
