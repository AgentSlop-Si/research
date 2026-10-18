# Sources and attribution

Read-only source inputs:

1. `../fourier_rewrite_completion_20261017_2130/PROOF.md`, SHA-256
   `475a32ecfadd70dabe8e815a793241a213138e620a177d3e8bc00a5d5914ff9c`.
   Used for the exact Fourier stage definitions, prior monomial-only scope,
   R30 coefficient class, and previous cost baseline.
2. `../fourier_rewrite_final_review_20261017_2141/REVIEW.md` and `ERRATUM.md`.
   The mandatory clarification is preserved in this work: same-coordinate
   support arguments do not govern auxiliary encodings; literal evaluator
   costs are not minimum circuit costs; field extensions need a representation
   and charged conversion/application. See this proof §§5–7.
3. Retained original R30 `input/unpacked/PROOF.md`, `REPORT.md`, and
   `graph_fusion.py` in the prior completion. Read as source text; not executed.
   Inspected `recognize`, `compile_window`, `fused_graph`, and the fixed-grid
   arithmetic checks to establish exact permitted masks, coefficient, and
   direction. No duplicate-result audit was repeated.

Classical attribution, re-opened on 18 October 2026:

- Cooley and Tukey (1965), the radix-two FFT factorization:
  https://web.stanford.edu/class/cme324/classics/cooley-tukey.pdf
- IBM Qiskit 2.2 SXGate reference, the standard C=(sqrt X) matrix:
  https://quantum.cloud.ibm.com/docs/en/api/qiskit/2.2/qiskit.circuit.library.SXGate

The two-shear construction and modulo-3 minimal-interface argument are proved
in this package. No claim of historical priority is made. The point of this
continuation is an explicit compatibility boundary and an honest optimization
stop decision, not rebranding elementary matrix factorization as a breakthrough.
