# Independent audit: inverse-chart, Fourier support, and complete quadratic lift

9 October 2026. All uploaded Python was treated as source text/data: none was executed or imported. The independent checker uses newly authored sparse cyclotomic arithmetic, subset determinant expansion, modular matrix inversion, and exact rational controls. All source coefficient exports were compared coefficient-for-coefficient, not only sampled.

## Verdict

The three main representations are correct within the explicitly stated model and patches:

| Representation | Equations | Variables | Maximum degree | Terms | Distinct monomials |
|---|---:|---:|---:|---:|---:|
| Inverse-stage regular chart | 30 | 26 | 4 | 1,268 | 389 |
| Fourier-support regular chart | 25 | 21 | 6 | 1,749 | 550 |
| Complete separated-generator lift | 176 | 184 | 2 | 800 | 737 |

Every coefficient of all three supplied exports matches the independent reconstruction over Z[z]/(z^4+1). No material error was found in their scoped equivalence claims. They do not establish that the fixed F8 factorization exists or is impossible. They do not establish a new asymptotic FFT algorithm or lower bound.

There are useful further exact results: explicit factored inverse-corner saturation; a patch-equivalent degree-reduced version of eleven equations; a singular beta-line in the reduced system; and a concrete distinction between the old and new diagonal-normalization patches. These are documented below and proved in `EXPLICIT_SATURATION_EXTENSION.md`.

## 1. What the quartic representation really covers

For P with row ordering [7,0,6,3,4,1,2,5], the correct image is B=F C P^-1, so column j of C P^-1 is column p_j of C. The independently rebuilt export uses precisely that orientation.

An invertible separated-generator stage has crossing ranks at most one. Its inverse has the same lower and upper crossing ranks. This is the classical nullity theorem, confirmed against the primary [Strang–Nguyen paper](https://epubs.siam.org/doi/abs/10.1137/S0036144503434381) and [Vandebril's author-hosted discussion](https://people.cs.kuleuven.be/~raf.vandebril/homepage/publications/papers_html/nullity/node3.html). A short independent proof is available: for the first k-coordinate subspace E, the two lower crossing ranks are k minus the dimensions of E∩S^-1 E and E∩S E. The invertible map S identifies those intersections. The upper case follows by using the complementary coordinate subspace.

Nonzero corner anchors then let the crossing-rank identities reconstruct global separated generators. This last condition is essential: preservation of crossing ranks alone does not preserve the entire finite global-generator parameterization at zero corners.

Right-scaling C by a nonsingular diagonal D can normalize diag(C)=1 if every diagonal is nonzero. It changes A to D^-1 A and B to B P D P^-1, preserving BPA and the stage family. Lower/upper scalar generator gauges then set L7=U0=1 when C70 and C07 are nonzero. The 26 coordinates and the 15+15 anchored B equations follow. With B70 B07≠0, those equations reconstruct every strict-lower and strict-upper B entry; diagonal entries are unrestricted.

### The new regular patch is not literally the old regular patch

The earlier adjugate construction required nonzero diag(A). This inverse construction requires nonzero diag(A^-1). These conditions are different. For n=8, set

A=(7/6)I-(1/6)J,   C=A^-1=(6/7)I-(6/7)J.

Both matrices are globally separated and all four corner anchors are nonzero. All A diagonal entries are one, but all C diagonal entries are zero. An exact rational multiplication verifies AC=I. Thus the new chart cannot be advertised as an unconditional replacement for every point of the old normalized chart. This is a stage-level domain example, not a Fourier factorization. The source correctly states the new diagonal requirement; the distinction should remain visible in subsequent synthesis.

## 2. Fourier support and the sextic export

Let beta=B71/B70. Because p0=7 and p1=0, the eliminated identities are exactly the vanishing of F(C[:,0]-beta C[:,7]) in rows 2 through 7. With a primitive eighth root in characteristic other than two, inverse Fourier expansion gives the span of 1 and z^-k. The endpoint rows determine a,b uniquely because z-1≠0. Dividing by t=C70 then solves L1 through L6. Replacing s U_i by h_i and W_j/s by eta_j also requires s=h0≠0.

The independently constructed Ctilde=t(z-1)C matches every supplied sextic coefficient. More strongly, all six linear frequency expressions Btilde_i1-beta Btilde_i0, i=2,...,7, vanish as formal polynomials. Consequently the five omitted anchored equations vanish formally, not merely at sample points.

Fresh checks used all four primitive-root embeddings in each of GF(17), GF(97), and GF(257), including zero-valued interior generators: 144 quartic evaluations, 144 complete reduced-coordinate round trips, and 144 comparisons of all thirty original minors after denominator clearing passed. The ratio beta is uniquely recovered whenever the stipulated B70 anchor is nonzero.

The raw reduced equations still contain spurious singular roots. Setting every one of the twenty non-beta coordinates to one makes C=J for every beta. All 25 equations vanish identically along this whole line, while det(C)=0 and B70=0. This was verified symbolically, retaining beta as a free variable. Reducing the number of variables did not remove the need for saturation.

## 3. Complete quadratic system

The 128 entry variables plus 56 generator variables are correctly counted. The 112 off-diagonal realization equations and 64 entries of BPA=F give precisely 176 quadratics and 800 terms. The permutation indices and every coefficient were independently verified.

This is genuinely complete for the stated separated-generator family, including all zero-generator and zero-anchor cases. No division or normalization is present. In characteristic zero, invertibility of F forces A and B invertible automatically. The encoding is not complete for the larger order-one quasiseparable family: that family permits boundary reset patterns that one global pair of lower/upper generators cannot realize.

Ninety-six independently generated sparse/zero-anchor synthetic products satisfy the corresponding exact target equations. These are implementation controls with synthetic targets, not evidence that F8 has a solution. Comparing numbers of equations and unknowns is not a feasibility proof or an independence claim.

## 4. Exact additions produced by this audit

- For any n≥2 separated stage S, the lower inverse-corner numerator is -L[n-1]V[0] times the product of d[k]-L[k]V[k] over k=1,...,n-2. The upper formula is its transpose analogue. These identities make the inverse-anchor requirements explicit without a generic adjugate computation.
- For n=8 normalized C, each corner cofactor has 64 monomials and degree 13. Independent formal cofactor expansion matches the product formula exactly. Exhaustive GF(2) testing covered all 2,048 n=3 generator/diagonal assignments, including 344 invertible cases; 330 zero-heavy integer examples at n=2,...,12 also passed.
- An explicit factored saturation product for the reduced system is exported, including all lower and upper gap polynomials and the determinant matrix. Its nonvanishing agrees with direct inverse-corner testing in all 144 reduced samples.
- Dividing removable powers of t, already required nonzero, gives an equivalent 25-equation system with four cubics, six quartics, one quintic, and fourteen sextics. Multiplication by the removed powers exactly recovers every supplied polynomial.

The straightforward saturation product has degree 59. Appending a single reciprocal equation raises that equation's degree to 60; the headline sextic degree refers to the unsaturated equations. This is not a flaw, but it matters for honest solver planning. Factored saturation or separate localizations may be preferable. No claim that the revised system is computationally easy is made.

## 5. Provenance, reproducibility, and next decision

All 131 listed source-manifest hashes match. The 110 files under the new prior_checkpoint directory are byte-for-byte identical to the previously extracted algebraic-jet package. Inherited tests are not new independent corroboration.

Run `python independent_inverse_checks.py` from this audit directory, or supply --source-dir and --output-dir. The default source location is ../source_material/fft_inverse_quartic_gate_2026-10-09. Only Python's standard library is needed. The checker reads three polynomial JSON exports and the hash manifest; it never imports source-package code. Results and the audit extensions are regenerated alongside the script.

The next decisive target remains an exact solution of the regular saturated ideal or a characteristic-zero unit-ideal certificate, followed by separate exceptional-patch coverage if claiming full-model impossibility. Work over Q(z) as the coefficient field while allowing solutions in its algebraic closure; restricting variable values to Q(z) itself would be an unwarranted extra constraint. Numerical misses, finite-field misses, equation counts, or raw singular roots do not settle the problem.
