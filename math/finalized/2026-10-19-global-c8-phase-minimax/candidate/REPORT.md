# Result: the sharp unrestricted phase minimum

The remaining global gate closes by a cyclic-shift commutator argument:

min over diagonal unitary P,Q of σ₃(Im(PF₈Q)) = sin(π/16).

Equivalently, every open arc of width π/4 contains at most five eigenvalues, counted with multiplicity, of F₈ A F₈ B for arbitrary diagonal unitaries A,B. This is an analytic uniform theorem, not a phase-grid conclusion or an extrapolation of the earlier local result.

## The new mechanism

Let S e_j=e_{j+1}, M=F₈AF₈B, and T=B*SB. Cyclic Hankel structure gives

M T M* T* = S*B*S*B.

The right side is a weighted two-step shift with two four-cycles. Its characteristic polynomial is

(x⁴−Γ)(x⁴−Γ⁻¹),  Γ=(b₀b₂b₄b₆)/(b₁b₃b₅b₇).

Consequently every open π/2 arc contains at most two of its eigenvalues.

If M had six eigenvalues in an open π/4 arc, rotate the arc to 1 and replace those six eigenvalues by 1, obtaining a unitary M₀ with rank(M₀−I)≤2. Its commutator K₀ fixes at least four dimensions. For E=M₀*M, the scalar-centering estimate

||E−cos(π/8)I|| < sin(π/8)

implies ||K−K₀||<2sin(π/8). Singular-value min–max then puts at least four eigenvalues of K inside the open π/2 arc centered at 1, a contradiction.

The accepted exact witness attains sin(π/16). The original unrestricted-real-core, complex-rank-one operator-norm objective has the same value by its fixed-phase imaginary-rank-two reduction, restated in the proof.

## Deliverables

- PROOF.md: self-contained universal proof, all phase/shift conventions, multiplicity and endpoint treatment, original objective reduction, and explicit attaining witness.
- exact_global_checker.py: new reproducible symbolic and characteristic-zero checks; imports no previous research program.
- EXACT_GLOBAL_CHECKS.json and exact_global_stdout.txt: successful checks of arbitrary-variable identities, exact boundary spectra, and destructive controls.
- REVIEW.md and REVIEW_VERDICT.json: independent acceptance, including an independent exact verifier and final author-proof hash binding.
- PROVENANCE.json and MANIFEST.json: prior accepted witness/source references and content hashes.

The lower bound does not use the earlier local phase analysis, the four-periodic-sector lower theorem, or the earlier coarse bound. No literature-novelty claim is made. No external files, messages, or repositories were changed by this work.
