# Independent audit of Fourier-support checkpoint v33

Completed 10 October 2026. Verdict: the audited finite structural and rational-map certificates pass. They supply no Fourier weight assignment, Fourier exclusion theorem, approximation guarantee, or FFT running-time improvement.

## Frozen source and method

- Source ZIP: `fft_gain_gauge_fourier_v33.zip`; original bytes are preserved separately. Selected audited source files accompany this public copy.
- ZIP SHA-256: `8daa679b23eadec2862fc8f3c4828a3bb87b469fb79536936436522fc5d04020`, matching the supplied expected hash.
- Accompanying note: read in full and preserved separately. Its 302-line content agrees with the scope stated in the ZIP research note.
- All 26 entries of the source manifest independently hash-verified.
- Supplied programs were read as text only. None was run, imported, linked, or used as an executable dependency. The predecessor ZIP was hash-verified but not recursively audited.
- Independent programs written for this audit: `audit_geometry.py`, `audit_finite.cpp`, and `audit_controls.py`. The C++ determinant method is a division-free first-row Laplace recurrence over row/column subsets, unlike the source's elimination checker. Transfer derivatives use dual-number propagation through the sparse evaluator, rather than the source's layer-specific formulas.

## Reproduced results

1. The topology has three 11-by-11 layers, 33 distinct edges per layer, and every row and column has degree three: 99 edges in total.
2. The modulus 1,000,000,123 is prime, verified by trial division through its square root. The stored root 414,936,531 has exact order 11.
3. Multiplying the three weighted layers independently reproduces all 121 entries of the stored modular transfer matrix.
4. All 705,431 nonempty square minors of that matrix are nonzero modulo the stated prime. Counts by order 1 through 11 are 121, 3,025, 27,225, 108,900, 213,444, 213,444, 108,900, 27,225, 3,025, 121, and 1. The full determinant is 500,795,841 modulo the prime.
5. All 705,431 equal-cardinality nonempty input/output subset pairs admit vertex-disjoint paths. The independent checker constructs each layer's exact perfect-matching relation and composes the three relations. No routing failure occurs.
6. The rational cross-ratio derivative has rank 56. Its denominator-squared numerator matrix also has rank 56. The source's specified 56-by-56 minor has determinant 915,710,031 modulo the prime, exactly as reported.
7. The 44 infinitesimal vertex-scaling vectors span dimension 43, and all annihilate the rational derivative.
8. The 101-by-101 evaluation matrix for 1 and the 100 cross ratios, using the source's 101 specified seeds and independently generated assignments, has determinant 763,214,669 modulo the prime. Thus the no-affine-linear-relation certificate reproduces.
9. The saved weighting satisfies zero of the 100 Fourier cross-ratio equations. Its first target residual is 379,306,912 modulo the prime, agreeing with the source.

Independent negative and positive controls also pass: 330 separately eliminated random minors are nonzero; Gaussian elimination confirms the full determinant; identity-matrix minor counts are correct; a duplicated transfer row causes 167,960 zero minors; disconnecting one input causes 352,716 routing failures; the exact field Fourier matrix and arbitrary endpoint scalings satisfy all 100 cross-ratio equations; changing one interior Fourier entry leaves exactly 99 satisfied equations.

## Precision correction: which Jacobian was certified

Write N_ij = H_ij H_00, D_ij = H_i0 H_0j, R_ij = N_ij/D_ij, and t_ij = zeta^(ij).

The source constructs the row matrix

    J_num = D_ij dN_ij - N_ij dD_ij = D_ij^2 dR_ij.

This is the cleared-denominator numerator of the derivative of the rational cross-ratio map. It is not the derivative of the cleared-denominator Fourier target equation

    f_ij = N_ij - t_ij D_ij,

whose derivative is

    df_ij = dN_ij - t_ij dD_ij.

The exact relation is

    J_num = D_ij df_ij - f_ij dD_ij.

At a target solution, f_ij = 0, so these derivatives differ only by invertible row scalings when the anchors are nonzero. At the saved non-target assignment they do not: this audit obtains rank 75 for the target-residual Jacobian, versus 56 for the rational-map derivative. The image of vertex-gauge directions under the target-residual Jacobian has rank 19; only the 22 individual hidden-vertex gauge vectors vanish there. This is consistent with endpoint gauges scaling nonzero target residuals, rather than fixing their values.

Recommended wording: replace “Jacobian of the 100 cleared-denominator cross-ratio coordinates” with “denominator-squared numerator of the Jacobian of the 100 rational cross-ratio coordinates.” This is a precision correction, not a failure of the supplied rank-56 certificate. Rank 75 at the non-target point is not an impossibility certificate or a statement about the dimension of the target solution set.

## Exact characteristic-zero scope

The minors and the rational-map Jacobian numerators are integer polynomials in the edge weights. Their nonzero modular evaluations prove that the corresponding polynomials are nonzero over the integers, rationals, and complex numbers. In fact, interpreting the 99 stored nonzero residue representatives as ordinary integer weights yields a concrete characteristic-zero full-spark transfer: if an integer minor vanished, its modular reduction would vanish too. That integer transfer is not numerically equal to the displayed reduced modular transfer.

The graph's vertex-gauge action has dimension 43 on its edge torus. Consequently the rational cross-ratio image has dimension at most 99 minus 43, or 56. The nonzero modular derivative minor lifts to a nonzero characteristic-zero rational-function minor, proving the reverse bound. The complex Zariski-closed image therefore has dimension 56 and ambient codimension 44.

The nonzero modular evaluation determinant similarly lifts to a nonzero rational determinant at integer assignments whose anchor denominators are nonzero. Therefore 1 and the 100 rational functions are linearly independent over the complex numbers: there is no nonzero affine-linear identity in the cross-ratio coordinates. This does not determine the lowest degree of a nonlinear relation or produce a Fourier-failing relation.

The cross-ratio target equations are an exact diagonal-equivalence criterion on the nonzero-anchor chart. If a weighting on this support satisfied the Fourier tuple, endpoint diagonal factors could be absorbed into the first and last weighted layers to yield the exact Fourier matrix without adding support edges. No such weighting is provided here.

Finite-field failure of the saved assignment excludes that modular assignment, not every complex weighting. A 56-dimensional image can still contain the special Fourier point. Neither codimension 44 nor unsuccessful numerical fitting excludes it. No approximation quality or Fourier error guarantee follows from these structural certificates.

## Runtime and novelty boundary

The literal fixed-support evaluator uses 99 weighted-edge multiplications and 66 additions, or 165 arithmetic events before input/output access costs. This computes the transfer attached to its weights, which the saved weights do not make Fourier. The inequality 99 < 121 compares two fixed-size edge counts; it does not establish an asymptotic subquadratic family, an improvement over the best 11-point Fourier circuit, or a fully charged all-length FFT algorithm.

This audit does not independently validate the source's numerical optimizer, its full predecessor chain, its butterfly-control implementation, or external historical/priority claims. Those are not needed for the finite graph, full-spark, rank, and affine-independence verdict above. The separately mentioned 103-edge Fourier baseline was not imported or accepted as an input to this audit.

## Receipts and reproduction

- `geometry_receipt.json`: exact algebraic and Jacobian checks.
- `finite_receipt.json`: all-minor and routing counts and modular checksums.
- `controls_receipt.json`: mutation and positive controls.
- `manifest_receipt.json`: every verified source manifest entry.
- `geometry_matrices.json`: independently generated transfer, both derivative matrices, rational derivative, gauge vectors, residuals, evaluation matrix, and all 101 sampled weight assignments.
- `independent_input.txt`: independently reconstructed input to the finite checker.
- `AUDIT_SHA256SUMS.txt`: frozen audit artifact hashes.

Reproduction, from this directory:

    python3 audit_geometry.py
    g++ -O2 -std=c++17 audit_finite.cpp -o audit_finite
    ./audit_finite < independent_input.txt > finite_receipt.json
    python3 audit_controls.py

All work remained local. No external file was created, changed, or uploaded.
