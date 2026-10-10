# 05. Column-cleared dual-support polynomial system

Exact SHA-256: `742de8e54efd8f4950ad4f594a80a1d872aab4ab3d7c27ca64d5eb1f9ce9bd1e`

Source: `additions/1646/extracted/fft_spectral_determinant_gate_2026-10-09/previous_research_checkpoint.zip.unpacked/fft_dual_support_gate_2026-10-09/dual_sparse_polynomials.py`

Read scope: lines 1–124, complete. Supplied source was not executed, imported, compiled or parsed.

## Mathematical scope

Constructs 20 residual polynomials in 16 variables over Z[z]/(z^4+1) after ten formal identities vanish. Every B column is cleared by D=t(z−1), with its own S factor where relevant, rather than a global denominator product. construct_dual checks precisely the ten expected zero polynomial names.

## Guards and acceptance

Cleared equations are equivalent to their rational counterparts only with all clearing denominators nonzero. h0, B anchors, det(C), and inverse corners are additional membership guards listed in export metadata, but not enforced by the exported equation list. No saturation or exceptional-chart enumeration is performed. Zero factors can create extraneous algebraic solutions.

## Tests and certificate limits

modular_validation compares all 64 matrix entries and twenty scaled minors using factor_from_dual at two primes and two root variants. It skips failed denominators and does not itself require a positive sample count. test_dual_gate requires twelve accepted samples and exact term equality to the saved equation JSON. The imported factor generator remains a dependency; this batch is not a complete import-closure audit.

## Cost and implementation

Sparse polynomial multiplication is quadratic in operand term counts; fixed-size symbolic expansion can still grow substantially. Stored tests describe degree nine and 8,437 terms; this review did not regenerate those polynomials. No fast transform is implemented.

Finding IDs: F01, F02, F05, F08.
