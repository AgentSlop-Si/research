# Binary packing: accepted scope

Read the [source report](source/REPORT.md) together with the final review's mandatory [centering clarification](review/SCOPE_CLARIFICATION.md) and [acceptance verdict](review/VERDICT.json).

The accepted results include the legal uncentered actual-packed-length witness, the translated-window/volume analysis, and the exact terminating uniformly padded independent-node recursion with cost n exp(Θ(log n/log log n)).

The original common-centering argument establishes row-height/slot-width resistance. It does not establish unqualified actual-packed-length resistance after centering. An actual-length version additionally requires a zero block immediately before the final constant block in each operand. The final review proves this sufficient placement and records a native-rank counterexample without it.

The completed branch does not settle genuinely input-adaptive recursion, cross-node sharing or fused recovery, unrestricted multiplication, prime-Mersenne compatibility, a limiting leading exponential constant, or historical priority.

Source and review files are frozen historical artifacts subject only to the packet's explicit locator adaptations. Read the [release index](../README.md) and [adaptation ledger](../ADAPTATIONS.json) for byte-binding and reproduction boundaries.
