# Compatibility of the newly supplied algorithm branches

Read 10 October 2026. These files are new intake, not replacements for the frozen catalogue. Only mathematical prose was inspected; no supplied program was executed, imported, compiled or AST-parsed. All reported historical test counts and finite-field ranks remain source-level claims unless separately noted.

## Coherent sparse-jet lifting

Source: intake/extracted/fft_coherent_sparse_jet_lifting_2026-10-10/fft_sparse_jet_lifting/THEORY.md.

The stated regular-program theorem is sound on paper: correct formal quadratic restrictions on every one- and two-coordinate plane force Hessian(Phi)(0)=F_N; a forward-over-reverse Hessian-vector construction evaluates F_N v with constant-factor gate overhead and O(s+N) storage. Conversely, a Fourier circuit evaluates the quadratic potential in T(N)+O(N) work. This is a precise equivalence/reduction, not an independently faster algorithm.

The compatibility gate is important. F132 includes quantization, underflow and input-dependent tables, so it does not provide a regular exact arithmetic program with the required jet. Its extension as a quantized real function is locally zero in an underflow neighborhood of the origin. The exact growing-fiber recognizer also selects support-dependent branches; differentiating its zero-input branch does not recover the common quadratic jet. Finite-field pointwise equality is weaker than a formal identity, exactly as the supplied Frobenius example shows.

The Fourier-minus-diagonal rank bound uses an off-diagonal square Vandermonde submatrix and is valid at composite lengths in the supplied-root field model. The separable-product analysis correctly retains zero-anchor cases. These are representation/term-count obstructions; they do not give unrestricted circuit time lower bounds or a new coherent source circuit.

## Hero 1 Phase 28, nested 60-point kernel

Source: intake/extracted/fft_hero1_phase28_20261010/fft_hero1_phase28/THEOREM.md.

The displayed tensor exchange rule follows by comparing the two neighboring preweave or postweave costs. Its scope is the given fixed codelets. Substituting the stated 60-point cost into the outer mixed-radix ledger gives the reported lower-order 46H execution saving and 29-operation extra cold setup. The leading 90H log2 H term remains unchanged. The exact short codelet identities and claimed cyclotomic/test certificates were not independently executed in this pass.

A normalized U_60 response table is compatible with F132. It is a constant-size local backend, so it does not create the asymptotic growing-radix saving. If the Winograd pre/post factors themselves are used in finite-precision execution, their intermediate norms must be bounded; exact algebraic equality of the final product alone is not a numerical-stability certificate. Directly tabulating the final normalized U_60 avoids that issue.

## Hero 17 Phase 16, Fourier–Green interface

Sources: intake/extracted/fft_hero17_phase16_fourier_green_interface_2026-10-10/PROOF_CERTIFICATE.md and RESEARCH.md.

The consecutive-support zero bound is a degree argument, and its endpoint-diagonal quotient consequence s+t>=N+1 is sound as stated. The chirp identity Q=L C_h R follows by expanding the quadratic exponent at t=j+s. Odd N ensures the displayed half-integer-looking quadratic phases are periodic. The sharpness construction does not establish denominator invertibility in every field; the claimed finite-field ranks remain source-level evidence here.

The fusion with normwise tabulation is conditional: applying C_h^{-1} cheaply requires an independently prepared and certified multiplier 1/DFT(h), including a lower spectral bound. An l2-accurate transform of h only gives a potentially sqrt(N)-worse multiplier sup bound. The explicit Bluestein obstruction in THEOREM_AND_PROOF.md demonstrates why an l2 contract alone cannot erase this preparation cost.

If compatible finite-word multipliers are supplied with a certified condition ratio kappa and charged preparation, two approximate unitary FFT calls apply the diagonalized operator with relative output error O(kappa delta). Choosing delta=epsilon/(C kappa) preserves the sub-N-log-N bound when log(1/epsilon)+log kappa=o(log N). This is a useful conditional certificate transfer, not a proof that the required inverse multipliers are already available or that the exact Green construction has become a faster universal FFT.
