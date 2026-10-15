# Lean verification pilot: specification only

15 October 2026. **No Lean proof has been compiled or kernel-checked.**

The first target is the classical identity `rank(I-P) = N - number_of_cycles(P)` over every field, with fixed points counted. The attached specification constructs the kernel as scalar functions on the cycle quotient, then uses rank-nullity. It is a prerequisite of the accepted research, not a formal verification of every result that uses it.

Lean and Lake were absent. Installation of the official Lean 4/mathlib toolchain was authorized, but the official release download was rejected by the execution environment's network policy. No software was installed and no alternate route around that denial was attempted. The installation blocker does not refute the theorem.

## Files
- `PermutationCycleRank.spec.md`: unimplemented theorem contracts and proof plan.
- `DEPENDENCY_MAP.json`: documentation-based dependency map; imports have not been compiled.
- `SOURCE_BINDING.json`: exact accepted-source hash and public source link.

A successful future deliverable must pin a compatible Lean/mathlib version, include complete `.lean` files with no `sorry`/`admit` or added theorem axioms, record a successful clean build and list the final theorem's axioms. Standard Lean foundations must be distinguished from unproved project hypotheses. Tests or an unchecked declaration do not meet this acceptance criterion.

This pilot makes no novelty, faster-FFT or new complexity claim. It needs an allowed environment with a usable toolchain before implementation and kernel verification can continue.
