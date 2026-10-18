# Fresh-source pre-execution review

2026-10-17. Author review, not independent acceptance.

Read all freshly authored modules before execution: outer_wrapper.py,
sparse_output.py, production_scalar.py, regression.py and launch.py. AST parse
succeeded. Historical modules under sources/ were read as text only and are not
in the subprocess import path. No old test runner or scientific source executes.

The wrapper has only four-support or accepted-output support loops, one incidence
range with exactly the signed ceiling endpoints, and constant-size record checks.
Per-support endpoint prefixes are prepared and charged once, so record ordinal
verification has no O(S) rescan. There are no N/M-sized arrays, phase tables,
full-vector scans, sorting in the outer stage, or coefficient setup during
iteration. Selected numerical calls enter the freshly reviewed kernel only.
The all-incidence regression stores and pays through its test/host cap an E-sized
receipt, while the production iterator streams O(1) records at a time.

The fresh Cartesian-median producer stores the immutable original candidate and
row tuples, computes every output by paid bottom-up merge sorts, and emits the
accepted numerical MedianResult field semantics. Binding repeats those actual
median calculations from original context and compares the exact result, rather
than relying on an echo label or a dataclass's self-asserted numerical fields.
It rejects replaced output identity before replay; even coordinated output plus
origin replacement fails exact replay when the supplied rows do not justify it.
Subsequent binding checks are constant-time under trusted unchanged memory.
The adapter neither accepts serialized state nor authenticates external origin.
The source/context is supplied median inputs, not an executed theorem-scale
random sparse pipeline. That higher provenance gate explicitly remains open.

Exact type checks precede untrusted numerical field operations. Validation and
rejection retain their cumulative ledger prefix. Separate scalar and outer
ledgers are never reset; their sum is the composed charge. The producer/replay
sort cost is an additional explicit charge, not hidden in the coefficient bound.

The scalar source's fixed-term atan/Taylor/factorial/root loops are bounded by K;
signed endpoint powers use logarithmic square-and-multiply with full large
intermediate widths charged. Certificate failure is deterministic implementation
failure. No dynamic historical imports, callbacks, or external writes exist.
The launcher enforces finite CPU, wall, address-space, file-size and descriptor
caps and records actual process exit, stdout/stderr and pre/post hashes.
