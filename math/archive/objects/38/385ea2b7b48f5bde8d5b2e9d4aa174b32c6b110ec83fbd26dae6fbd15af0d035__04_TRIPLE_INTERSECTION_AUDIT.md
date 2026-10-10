# Independent audit: four-column compatibility gate

9 October 2026. Uploaded code was read only as source text; no uploaded Python or binary was imported or executed. The three checkers in this folder were independently authored. They read the four original JSON files in `input_data/` as inert comparison data. No existing master file was modified.

## Result

The new characteristic-zero exclusion and four-variable dimension bound are verified, with a small repair to the structural lemma's statement and proof. They do not establish a full complex nonexistence theorem or a faster FFT.

- Reconstructed the old Fourier quartic and adjacent-column recurrences directly, then formed their coefficient determinant W. No previous executable or coefficient file is needed.
- Rebuilt the polynomial 11×9 matrix from Fourier columns and the stated rescaled generators. Its full selected 9×9 symbolic determinant equals −DB·DH exactly.
- Every one of 924 exported cyclotomic coefficient vectors matches: Δ,T,V,M,W,DB,DH,Dhat,RDB,RDH. The determinant has 250 terms/degree 8, with factors of 9 terms/degree 2 and 105 terms/degree 6. The two resultants have 37 terms/degree 5 and 476 terms/degree 15.
- The fixed slice h0=1,h1=h2=0 has exact nonzero resultant; its reduction modulo (17,z−9) is 6. The exclusion is genuinely over the complex numbers on the specified regular slice.
- Exact polynomial division independently verifies the nondivisibility used in the dimension bound. The necessary candidate set in the four h variables has dimension at most two.
- A fresh GF17 enumeration reproduces the 4,596 prior survivors and ranks 9:3266, 8:1203, 7:125, 6:2. There were also 256 direct modular full-matrix/minor checks and 630 independently constructed invertible positive controls.
- An additional exact certificate strengthens the exceptional-fiber analysis: the base points where W is identically zero as a polynomial in h6 form a finite set. A degree-six univariate resultant and a constant nonzero quadratic leading coefficient give the elementary bound of at most twelve such base points. Their free-h6 stratum therefore has dimension at most one. The overall dimension bound remains at most two.

## 1. Structural lemma: necessary correction and completed proof

A precise sufficient statement is:

Let C be an invertible globally separated-generator matrix, Q any 8×8 matrix, and D=Q C P^{-1} have globally separated upper rank-one generators, with P=(7,0,6,3,4,1,2,5). Form the stated Y1,Y2,Y5,Y4, cofactor vector η and matrix K. Then rank K≤8.

The proof does not require Q or D invertible, once C is invertible. The weaker sufficient condition is that the chosen coefficient triples for C columns 1,2,4,5 are nonzero; invertibility ensures this without a generator-specific condition.

Write cj=(dj,Wj,Vj) for the coefficients of C column j in the ordered basis (ej,U-head,L-tail). Every cj is nonzero because C is invertible. The first-five-row projected output columns corresponding to j=1,2,5 are Yj cj.

1. If any of these three projections vanishes, put its nonzero cj in that block of a nine-vector and zeros in the other blocks. The first ten rows of K kill it. If it is the first block, the last row also kills it because A cj=0; otherwise the last row does not touch that block.
2. Otherwise the three output upper-column multipliers are nonzero, and rescaling the three cj gives a common nonzero vector q in all three column images. This supplies a nonzero kernel vector for the first ten rows.
3. If output column 4 has nonzero upper multiplier, its first four entries show q[0:4] lies in col(Y4), so ηᵀq[0:4]=0.
4. If output column 4 has zero upper multiplier, Y4 c4=0. Since c4 is nonzero, rank(Y4)≤2. All of its 3×3 cofactors vanish, so η=0 and the eleventh equation is automatic.

Step 4 is missing from the uploaded prose proof; it repairs the apparent division by a potentially zero fourth multiplier. No new nonzero fourth-multiplier guard is needed. The independent controls deliberately include this case and also permit zero C diagonal entries while retaining invertibility.

The standalone statement in PROOF_CERTIFICATE.md says C is separated but does not explicitly require C invertible. Read literally for arbitrary possibly zero C, it is false. Set C=D=0 using d=W=V=0 but retain the U,L generators recorded in `modular_results.json`; choose the invertible F8 over GF17 with z=9. The resulting K has rank 9 and selected minor 3. The intended application has C=A^{-1}, so its invertibility already supplies the missing hypothesis. This wording defect does not invalidate the regular-chart conclusions.

## 2. Polynomial and resultant verification

The exact checker works over Q[z]/(z^4+1) using SymPy's algebraic field and independently implemented exterior-product determinant accumulation. It reconstructs the three-character H recurrence, scaled lower generator, Fourier spectral quartic Q, and the two high-frequency tail recurrence equations. Their coefficient rows in t and β give W and the affine eliminants Δ,T,V.

From the prescribed Uhat,Lhat it constructs all four Y matrices and η, then the entire 11×9 K. It evaluates the selected rows (0,1,2,5,6,7,8,9,10) symbolically and checks the exact factorization −DB·DH, rather than relying only on sample evaluations. It also reconstructs the two Sylvester determinants defining the resultants. All output coefficient vectors are checked integral in the cyclotomic basis (1,z,z²,z³).

At (h0,h1,h2)=(1,0,0), reduction sends z to 9 modulo 17 and gives W=10+14x+16x²=16(x−2)(x−12). At x=2 and x=12 respectively:

- Δ: 14, 9
- T: 8, 10
- Dhat: 3, 2
- DB: 6, 3
- DH: 8, 5

The exact slice resultant, in coefficient order (1,z,z²,z³), is

(1211698059904852984594432,
 −1992767561947272609529856,
 1606653735723273839181824,
 −278796638724462678638592).

Its reduction is 6. The two shorter resultants evaluate to 16 and 11 modulo 17; their product is 6. A nonzero reduction proves the exact resultant is a nonzero algebraic integer. Thus W and Dhat have no common root in C on that slice. This proof does not assume a putative complex solution reduces to a prime-field solution.

The source's original unrescaled minor at x=12 is 8, while the polynomial rescaled minor is 2; these are different matrices related by nonzero basis scalings. There is no contradiction between `universal_gate_results.json` and the polynomial certificate.

## 3. Dimension claim and stronger exceptional-fiber certificate

Every regular candidate satisfies W=0 and Dhat=−DB·DH=0, so its base (h0,h1,h2) satisfies RDB·RDH=0. Both resultants are nonzero, so this base lies in a proper algebraic hypersurface union of dimension at most two.

Write W=W2(h0,h1,h2)h6²+W1(h0,h1,h2)h6+W0(h0,h1,h2). Outside the base where all three coefficients vanish, each fiber has at most two h6 values. The exceptional base requires care; a nonzero resultant alone would not bound its fiber dimension.

The original argument is correct: W2 is a nonzero linear polynomial, and exact division gives nonzero remainder W1 mod W2. Hence their common base has dimension at most one; allowing free h6 gives at most two.

The independent refinement goes further. Eliminate h0 by W2, whose h0 coefficient is a fixed nonzero cyclotomic constant. Let r1 and r0 be the remainders of W1 and W0 on division by W2. They are polynomials of total degrees two and three in h1,h2. Their gcd is one, and an independently constructed 5×5 Sylvester determinant Res_h1(r1,r0) is a nonzero degree-six polynomial in h2. The h1² coefficient of r1 is a fixed nonzero constant. Therefore there are at most six h2 values, at most two h1 values per h2, and a unique h0 for each pair. Exact coefficients are in `finite_fiber_results.json`.

This proves a finite exceptional base with an explicit simple upper bound of twelve points. It does not determine which points meet h0ΔT≠0 or any remaining Fourier identities. It does not reduce the overall dimension bound below two.

The bound concerns the necessary locus in the four structural variables, not an independently proved dimension bound on every variable of the older complete lift or on unrestricted factorizations.

## 4. Finite-field and zero-column controls

The modular checker reimplements matrix rank, determinant, inverse, the generator projection, and the polynomial lift using only Python's standard library. It performs:

- 64 full-matrix polynomial/minor comparisons at each prime 17,97,12289,65537, including parameter choices on zero-guard sets.
- Exhaustive s≠0 GF17 testing, retaining W=0 and ΔT≠0. Since Δ is invertible, this is exactly the t,β elimination branch of the three prior affine necessary equations. It reproduces all four rank counts.
- 210 controls at each prime 97,12289,65537. Separated C,D are generated independently and retained only when both are invertible. Q=D P C^{-1} is then constructed and D=Q C P^{-1} checked directly.
- Seven control modes: unrestricted; fourth upper multiplier zero; each of output upper multipliers 5,6,7 zero; the first five output upper-generator entries all zero; and zero C column-4 diagonal together with zero fourth output upper multiplier.

All 630 controls satisfy rank K≤8. The deliberately fourth-multiplier-zero modes verify η=0, confirming the completed proof. These controls support but do not replace the algebraic proof.

## 5. Scope and exclusions that remain

The polynomial lifting is valid on the inherited regular chart and requires h0ΔT≠0. This adds no permission to discard older guards: the earlier row-prefix, onion-elimination, boundary determinant, inverse-stage, anchor and invertibility assumptions remain in force wherever their reconstruction is used. The standalone structural gate itself needs none of the onion divisions, but its four-variable substituted form cannot automatically cover branches excluded while deriving those generators or solving t,β.

Retain separate branches for h0=0, Δ=0, T=0, zero anchors and the broader full-generator lift. Retain every remaining exact Fourier residual; neither W,Dhat nor the two resultant equations are sufficient for a factorization. Fixed shuffle, globally separated generators, inverse normalization and the specific Fourier root convention are part of the claim. The result does not cover arbitrary permutations, all quasiseparable matrices, unrestricted arithmetic algorithms, or arbitrary matrix sizes.

No full complex no-solution certificate or exact sub-N-log-N Fourier evaluator has been found. A bounded exploratory factorization attempt on W did not complete; no claim of irreducibility or complete factorization is made.

## Reproduction

Run from any location with Python 3 and SymPy installed:

    python independent_exact_audit.py
    python independent_modular_audit.py
    python independent_finite_fiber_check.py

All paths are relative to each checker file. The first command creates independently reconstructed coefficient data used by the other two. The original uploaded Python is unnecessary. Normal runs took approximately six seconds, one second and one second respectively in this environment; timings are audit convenience, not FFT performance claims. `exploratory/` is not required for any verification.
