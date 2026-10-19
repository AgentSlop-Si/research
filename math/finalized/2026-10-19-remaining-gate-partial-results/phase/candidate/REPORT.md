# Result: a new unrestricted local certificate and a quantitative global interval

19 October 2026 UTC.

The sharp unrestricted C8 phase minimax remains open. This packet does not prove δ=sin(π/16) or produce a counterexample.

## New results

1. A global lower bound valid for every arbitrary diagonal unitary P,Q:

       σ₃(Im(PF₈Q)) ≥ sin(π/16)/sqrt(13+4sqrt(3)cos(π/16))
                       = 0.0438487379148837407… .

   It follows from a quantitative Fourier-energy localization of nonperiodic phases, followed by an angular spectral perturbation estimate and the accepted periodic-sector theorem. It does not misuse the zero-error periodicity implication at positive error.

2. The previously accepted upper witness at sin(π/16) is a strict local minimum over all fifteen phase directions modulo scalar phase transfer. This includes all eight genuinely nonperiodic directions.

   The first variation on the six-dimensional low spectral cluster has rank seven. Its seven normalized coefficient matrices have Gram determinant 12288. The eight nonperiodic directions are precisely its kernel. A positive trace-one dual weight annihilates every first variation. After including the motion of the spectral subspace, its second variation on the kernel is exactly

       [cos(π/8)/(4sqrt(2))] ||ν||² > 0    for ν≠0.

   An analytic cluster reduction plus this certificate handles the nonsmooth third singular value rigorously. No explicit neighborhood radius is claimed.

3. The remaining sharp global assertion has an exact structured spectral formulation: every open arc of angular width π/4 contains at most five eigenvalues of F₈AF₈B for arbitrary diagonal unitary A,B. Equivalently, every unitary cyclic Hankel C and diagonal unitary D satisfy σ₃(C−D)≥2sin(π/16). This lemma remains unresolved.

## Files and verification

- `PROOF.md`: both new proofs, full phase coordinates, finite exact identities, and their analytic consequence.
- `GLOBAL_LEMMA.md`: exact remaining spectral lemma and proof of equivalence to the sharp minimax.
- `exact_local_checker.py`: newly written characteristic-zero checker in Q[z]/(z¹⁶+1), z=exp(iπ/16). It checks the explicit derivative matrices, Gram determinant, dual weight, all 36 second-variation coefficients, Fourier-energy projection identities, and witness eigenvalue arc endpoints.
- `EXACT_LOCAL_CHECKS.json` and `exact_local_stdout.txt`: exact-check results and negative controls.
- `REVIEW.md`: completed independent mathematical review accepting the two partial results and the exact remaining-lemma equivalences.
- `sources/`: frozen accepted proofs and reviews read as prerequisites; none was imported or executed.
- `explore_tangent.py`: fresh numerical tangent exploration used only to discover the subsequent exact certificate. It is not a lower proof, a global search, or a phase-grid certificate.

## Boundaries

The original unrestricted real core, complex rank-one correction, external operator norm, and arbitrary invertible monomial absorption remain unchanged. No finite grid, conditioning restriction, new matrix size, exact-rank substitute, or external publication is introduced. Strict local optimality does not classify global minimizers and does not close the sharp positive-error owner.

The stopping result is a precise unresolved global spectral lemma after a distinct dual-weight spectral-variation mechanism. The new lower bound and local theorem are useful partial results; they must not be labeled a solution of the sharp global minimax.
