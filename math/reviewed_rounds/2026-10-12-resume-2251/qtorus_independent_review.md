# Independent review: three-orientation frontier obstruction

12 October 2026 UTC. Status: accepted at the restricted symbolic scope below, subject to ordinary external peer review. Historical novelty is unassessed.

## Reviewed claim

For prime-power m>=5 and N=m^2, a sum of three separately input/output-diagonally gauged quantum-torus resolvents with precisely the identity, phi(a,c)=(-c,a+c), and psi(a,c)=(a+c,a) orientations cannot be made equal to the N-point Fourier matrix by outer invertible diagonal scalings and row/column permutations. Every branch uses a primitive m-th root, nonzero alpha,beta, and nonzero inverse denominator 1-alpha^m-beta^m. Different branches may use different primitive roots and coefficients.

## Independent symbolic check

The source entry formula has support u+v<m. On the frontier u+v=m-1, the Gaussian coefficient is b_u=(-1)^u q^(-u(u+1)/2), so b_u^2=q b_(u-1)b_(u+1).

For horizontal rows (a,c),(a,c+1) and columns (a+1,c+2),(a+1,c+3), only the phi branch survives. Its u matrix is [[2,3],[1,2]], and v=m-1-u. Both other branch supports are absent. For diagonal rows (a,c),(a+1,c-1) and columns (a+3,c-2),(a+4,c-3), only the identity branch survives, with u=[[m-3,m-4],[m-2,m-3]], v=[[2,3],[1,2]]. These canonical differences lie between 1 and m-2 for every m>=5.

For each surviving branch, total alpha and beta exponents agree between the two determinant products. Their q phase ratio is q^-1, cancelling the Gaussian coefficient ratio q; signs also agree. Arbitrary separate left/right diagonal branch gains preserve the zero minor because there is only one surviving branch on the complete rectangle. Coordinate wrap changes root exponents only by multiples of m.

The row-edge directions (0,1) and (1,-1) generate Z_m^2, giving a connected graph of row pairs with zero minors on distinct columns. If N is a prime power, a zero Fourier minor forces its row difference divisible by the underlying prime. Under any row permutation, all edges would therefore connect equal residue classes; connectedness would put all N distinct labels in one residue class, impossible. Column permutations and nonzero diagonal scaling preserve this argument.

## Fresh independent controls

Independently authored review_qtorus_frontier.py checks support isolation and exact symbolic exponent cancellation at all translated rectangles for every integer m=5..40: 44,220 minor checks pass. It does not import or execute supplied archive code. The finite controls corroborate the formulas; the preceding symbolic argument supplies the all-size conclusion. Results: qtorus_independent_review_controls.json.

## Boundaries

This closes only the specified three-additive-orientation Fourier-synthesis route for prime-power m>=5, including m=8 and16. It leaves m=4, different orientations, extra non-diagonal layers, products, and other Fourier algorithms unresolved. It does not contradict the source's repair of its particular earlier two-orientation witnesses: the new witnesses use different columns and frontier support. It is not an unrestricted Fourier lower bound, a positive fast FFT, or a verified worldwide-first theorem. The source's finite-field tests alone would not have proved the symbolic claim.

Source: [FFT_Qtorus_Phase_Bridge_2026-10-13.zip](sources/FFT_Qtorus_Phase_Bridge_2026-10-13.zip), SHA-256 0cc2147504a83677b16ee9f3f0cb57b62ebe20bb28120167a54b82444f59c690.
