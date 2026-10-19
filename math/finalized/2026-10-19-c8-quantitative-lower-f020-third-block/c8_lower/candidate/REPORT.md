# Result: explicit all-phase C8 rank-zero lower gap

The new argument proves, in the original unrestricted complex-monomial model and external operator norm,

    sin(3 pi/16 + 1/1000000) < delta_(8,0)
      <= sqrt(1 + sqrt(sqrt(2)-1))/2.

The lower endpoint is 0.5555710644889367420..., improving the accepted lower endpoint by 8.31469334517290149e-7. The inherited exact upper endpoint is 0.6410136997181851621.... This does not establish global optimality of the upper witness.

What is new in the argument:
- Quantitative endpoint localization for the weighted-shift commutator.
- An approximate four-point Fourier phase-product contradiction, forcing small complementary Fourier coefficients with a linear-in-residual bound.
- Approximate half-periodicity of B, without asserting or requiring exact periodicity of either phase matrix.
- Flat-vector tests in the actual U's two-dimensional compressions. These compressions need not be invariant or unitary, and no periodic surrogate is substituted into the global problem.

The proof is in PROOF.md. The fresh checker passes 186 exact identity/inequality assertions, including destructive controls for the asymmetric-cycle coefficient and the minus-sector diagonal sign. Tests verify the displayed algebra and rational margins; they do not by themselves establish novelty or the global theorem. The mathematical argument remains available for independent review.

Reproduction:

    python check_quantitative_gap.py

This writes CHECK_RESULTS.json and ASSERTIONS.json. SymPy is required. No historical checker, optimizer, external service, or other worker was used. One small floating-point diagnostic was used to choose safe constants; it is not a proof premise. All research and writes were local to this new shared directory. The first complete checker run passed in approximately 0.219 seconds of internal elapsed time.

Remaining obstruction: the proven lower endpoint is still far from the upper witness. The exact global optimum and minimizer classification remain open. The largest losses in the present proof come from pointwise Fourier residual bounds and replacing approximate endpoint information by two-dimensional flat-vector tests.
