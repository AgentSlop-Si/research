# Exact rejection of the all-ones inner prefix at N16

The full384-parameter model is specified in `N16_CERTIFICATE_SPECIFICATION.md`. For this bounded test only, fix all256 inner coefficients a_(1,j,i) and a_(2,j,i) to1, while leaving all128 outer coefficients free. The cycle geometry, poles1/2 through1/9, half-active bank, and product H3 H2 B H1 are unchanged.

For every output row, the eight transported Green templates have rank8 and the Fourier target raises the augmented rank to9. Therefore no outer coefficient choice, even allowing zero entries or coefficients in an arbitrary characteristic-zero field extension, can complete this fixed inner prefix.

The exact certificate uses the prime998244353 and z=3^((p-1)/16), verifies z^8=-1 and z^16=1, and checks every rational Green denominator is nonzero modulo p. `N16_OUTER_GATE_RESULTS.json` contains all16 explicit9-by9minors and nonzero determinants, as well as the full8-column elimination charts and residuals. The first minor has row index0 and determinant750393234 modulo p. A nonzero specialization proves that the corresponding minor is nonzero over Q(z)/(z^8+1), so this is a characteristic-zero rejection rather than merely a failed finite-field search.

Finite-field verifier controls recover all128 outer coefficients of a generated admissible product and verify all256 entries; a changed target entry is rejected. The separate seed control confirms that2F16 obeys successor covariance while failing the required first-column seed.

This excludes exactly one fixed256-entry inner prefix. It gives no exclusion of other inner parameters, the full384-variable seed family, different poles, or the broader eight-order architecture. Parameter counts and the existence of the cut-expanding geometry are not evidence that the remaining equations have a solution.
