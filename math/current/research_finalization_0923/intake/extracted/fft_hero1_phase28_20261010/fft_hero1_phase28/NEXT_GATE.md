# Hero #1 — Phase 29 exact Fourier research gates

## A. Noncoprime multiwire fusion — highest priority

For `G=4H` with even `H`, the cross-stage root tensor `omega_G^(u q)` remains, and this Phase 28 circuit still pays `45(H−1)` nonidentity field multiplications. The cross-ratio invariant forbids *monomial* removal of all these factors, **not** general noncommuting multiwire sharing.

A credible new candidate must:

1. Construct one complete exact scalar DAG for a block of two or more `(4,H)` stages, including the operations hidden in any graph or matrix solver.
2. Show that the all-input fully charged saving survives after **restoring complete output values**; do not count a higher-arity Fourier operator as one scalar gate.
3. Search optimized NTT implementations and classical Winograd/split-nesting prior art before claiming novelty.
4. Separate reusable coefficient tables from one-shot setup, index operations, memory, field-bit cost and precision.
5. Provide a recurrence with a strict asymptotic bound if claiming any genuine `o(N log N)` improvement; an `O(N)` per-level constant reduction is insufficient.

## B. Automate diagonal tensor-codelet synthesis

Use the verified exchange condition from `THEOREM.md`: pre order increasing `δ_i/p_i`, post order decreasing `δ_i/q_i`. Enumerate other exact 2-, 4-, 8-, 16-, and 32-point pre/diag/post codelets. Only accept kernels with fully expanded scalar costs and independent exact symbolic or modular proof.

Investigate replacing the `(3,5,4)` nested 60-point stage with a **genuinely better cost** after accounting for extra intermediate widths. Published WFTA real-operation tables quote a length-60 example, so priority claims require explicit distinction in arithmetic convention and an exhaustive prior-art review.

## C. Precision/bit gate

The current algebraic factorization works over complex roots as an identity. Turn it into floating-point code with bounded errors, and report actual wall-clock speed versus FFTW, pocketfft, and highly tuned NTT baselines. A field-operation improvement is not automatically a practical improvement.

## D. Global breakthrough goal

The unrestricted exact `o(N log N)` goal has a published 2026 claim with an extremely small exponent improvement in an unbounded-coefficient model. The public comparator Lean theorem file inspected in Phase 27 contains `sorry` placeholders. Keep public manuscript claims, formal proof scope, actual executable complexity, and our distinct finite-field circuit model separate. To surpass the claimed bound, show a rigorously larger power saving or a meaningful precision/bit-cost advance—without simply reusing CrocSwap's exponent machinery.

## Falsification criteria

- Counterexample on a complete Fourier basis, or wrong sign/CRT map.
- Per-gate scalar count omits either pre/post additions or coefficient preparation.
- Polynomial-width intermediate tensors allocated or recomputed free.
- Difference claimed against a deliberately inferior FFT baseline.
- A fixed `Θ(N)` saving described as `o(N log N)` complexity.
