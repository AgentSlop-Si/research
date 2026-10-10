# Reproduce the Phase41 supplement

The supplied source files under `source/` are inert provenance and are not executed or imported. Run only the separately authored audit programs.

1. `python fresh_jacobian_audit.py` reconstructs all 26 prime/family/size records from explicit numeric source inputs. It uses direct sparse inversion and fresh inverse differentiation, with ordinary installed Python libraries only. The shared `fresh_reconstruct.py` helper is our newly authored Q26/Q27 arithmetic, not a source program. In the complete research workspace it is imported from `../masks`; a copy is included alongside the final package for standalone use.
2. `python fresh_partial_fit_checks.py` reconstructs saved matrices from JSON parameters without running an optimizer. This requires NumPy and mpmath. The ordinary checks are floating diagnostics. The retained decimal parameters are separately evaluated at110 digits; none is promoted to an exact root certificate.

The real phase Jacobian uses both split embeddings of Q(i) and independently checks their inverse and entry guards. The resulting real/imaginary coefficients are rational; the saved nonzero minors are exact modular evidence of characteristic-zero nonvanishing. Phase ranks and arbitrary-amplitude ranks refer to different domains.

All theorem statements, exceptions and priority limits are in `THEOREMS_AND_AUDIT.md`. The separate `FIXED_BRANCH_SEPARATOR_FUSION.md` gives the exact match to accepted F018, which already prevents a fixed three-cycle sum from being an all-N Fourier route.

No source optimizer run, original timing, universal graph-family enumeration, production Fourier implementation or exact Fourier target-root certificate is claimed. No new environment or external service is required for the bounded exact controls once the listed Python dependencies are installed.
