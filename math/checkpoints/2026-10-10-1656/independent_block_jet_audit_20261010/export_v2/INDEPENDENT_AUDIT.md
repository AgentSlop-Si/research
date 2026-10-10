# Independent audit: four-stage block-jet dominance at N = 256

Date: 10 October 2026. Status: the scoped dominance and second-order claims pass independent exact checks. This is an algebraic certificate, not a Fourier factorization, FFT executor, asymptotic improvement, or general FFT lower bound.

## 1. Source and independence

Audited source: `fft_joint_block_jet_checkpoint_2026-10-10.zip`, whose identity is recorded in SOURCE_ARCHIVE_LEDGER.json at the export root.

Archive SHA-256:

`0d5713c58ac450839fc1385996a72b8fba7ca548ccb0dd4667090bc0f4d414f3`

All 17 extracted members were compared byte-for-byte with the archive. All 16 entries in its embedded SHA-256 manifest matched. The full source inventory is in `SOURCE_PROVENANCE.json`. The separate report reference was unavailable; the complete README, research narrative, proof certificate, and verifier program texts inside the ZIP were inspected instead. The source archive is the mathematical evidence.

No supplied Python/C++ program was executed or imported. This audit copies only five JSON data files: layout, two integer points, and the two selected-column witnesses. Its fresh differential code uses explicit permutation matrices and dense triangular masks, rather than the source's gather-index contexts and cumulative sums. Its C++ eliminator was written independently; both 784-square determinants were also checked by a separate NumPy/Python eliminator.

Key source-data SHA-256 values:

| File | SHA-256 |
|---|---|
| AFFINE_LAYOUT.json | 77c5c0fcdcfa850dac44dd34dbe3188539aa9cb143f22978b86127add76b8e45 |
| GENERATOR_POINT_1.json | 0a86a4a741eade955e5202dd938a114342ce4fa8778f86c0b9499c5f7995fd73 |
| GENERATOR_POINT_2.json | 9c40d36e819325644e63048d84cd3bb37e5b677564bbd47e87b148ea8ae0f35c |
| witness28.json | 72fa24d34dd33e00d4856bd46cdcc0c049af069f099c5038cd7f5f198ef17dd5 |
| two_point_minor_indices.json | 6ef0c4c726a910306e1903840af8795fee6fd09e4f3a4195e26aa6e7adea2671 |

## 2. Exact map and conventions

Each of four stages has five independently variable length-256 coefficient vectors, in order `(d,a,b,c,e)`, and entries

\[
S^{(s)}_{ij}=\begin{cases}
a^{(s)}_i b^{(s)}_j,&i>j,\\
d^{(s)}_i,&i=j,\\
c^{(s)}_i e^{(s)}_j,&i<j.
\end{cases}
\]

The certified polynomial map is

\[
\Phi=S^{(4)}P_3S^{(3)}P_2S^{(2)}P_1S^{(1)}.
\]

For a stored bit-column list `c`, `p(i)` is the bitwise XOR of `c[b]` for set bits `b` of `i`, and `(Px)_i=x_{p(i)}`. The three column lists are:

- `(190,52,71,48,22,117,118,121)`
- `(58,20,167,24,254,26,247,78)`
- `(140,249,103,236,246,36,32,51)`

All three are verified bijections of 0 through 255. Their complete arrays are saved in `EXPLICIT_PERMUTATIONS.json`.

Important scope detail: `AFFINE_LAYOUT.json` also contains a five-gate Toffoli sequence. The source Jacobian code does not apply it, and neither does this certificate. The accepted theorem concerns the three affine-column permutations above. It must not be relabeled a certificate for a Toffoli-modified map.

The map is defined over the integers, with no inverses or denominators. Its total degree is at most eight. The characteristic-zero theorem allows arbitrary complex generator coefficients; it imposes no reality, positivity, unitarity, conjugacy, Fourier-value, or bounded-coefficient restriction. Parameter column number is `1280*s + 256*t + i`, with zero-based stage `s`, coefficient type `t` in `(d,a,b,c,e)`, and coordinate `i`. There are 5120 formal parameters. Sixteen boundary parameters do not occur in the map: `a_0,b_255,c_255,e_0` in every stage.

The 784 output coordinates are exactly `(i,j)` with `0 <= i,j < 28`, flattened row-major. The 784 distinct selected parameter columns are exactly `witness28.json:pivots_784`; bounds, uniqueness, output indices, and common use across both primes were checked. Both primes, 12289 and 65537, were checked by trial division. The stored integer witnesses are used directly; no pseudorandom-generator recreation is needed.

## 3. Fresh exact results

| Check | Modulus | Independent result |
|---|---:|---:|
| Selected leading-28×28 Jacobian minor | 12289 | rank 784, determinant 5424 |
| Same integer point and same selected columns | 65537 | rank 784, determinant 42512 |
| Leading-32×32 full coefficient Jacobian, point 1 | 12289 | rank 906 |
| Leading-32×32 full coefficient Jacobian, point 1 | 65537 | rank 906 |
| Leading-32×32 full coefficient Jacobian, point 2 | 12289 | rank 906 |
| Combined selected tangents, 906 columns from point 1 and 118 from point 2 | 12289 | rank 1024, determinant 4142 |
| Leading-32×32 output matrix itself, point 1 | both primes | rank 32 |
| Point-1 tangent plus `K[0,0] E_00` | 12289 | rank 907 |

The two 784-square determinants agree between the independent C++ and Python elimination implementations. Each main-prime differential was checked against full-product finite differences in 20 active parameter directions covering all stage/type pairs, plus all 16 inactive boundary parameters. An independent N=4 control checks every one of its 80 derivative columns.

The point-1 stage determinants are:

- modulo 12289: `11645, 2187, 2109, 4066`
- modulo 65537: `13152, 33714, 32694, 45567`

Thus all four actual integer witness stages are nonsingular in characteristic zero. Invertibility is not merely inferred from density of a separate parameter locus.

Additional leading-block ranks at point 1 modulo 12289 are 256/256 at 16×16, 400/400 at 20×20, 576/576 at 24×24, 784/784 at 28×28, and 831/841 at 29×29. These are scoped to the specified point and field. The narrative's center/off-diagonal block observations are not part of this fresh certificate.

Negative controls passed:

- Replacing one column of the 784-square minor with another selected column gives rank 783 and determinant zero.
- Setting every stage coefficient to zero gives the zero first derivative.
- Independent small square-matrix tests detect both a nonzero determinant and a duplicate-row singularity in each checked field.

All intermediate products are reduced modulo the prime. Dense int64 matrix-product accumulations are bounded by `256*65536^2 = 1099511627776`, safely below signed-int64 overflow. Eliminator products use uint64. The exact modular results are not floating-point rank estimates.

## 4. Accepted dominance theorem, including invertible stages

Let `pi_28` select the leading 28×28 coordinates of the specified map. Then

\[
\pi_{28}\circ\Phi:\mathbb C^{5120}\longrightarrow\mathbb C^{784}
\]

is dominant. Equivalently, its 784 coordinate polynomials are algebraically independent over the complex numbers: there is no nonzero polynomial in these 784 output entries vanishing for every parameter choice. This remains true with all four stages required to be invertible.

Proof: specialize the selected Jacobian determinant to the saved integer point. Its residue 5424 modulo 12289 is nonzero, so the determinant is a nonzero integer. The complex derivative is therefore surjective at that point. Fixing the other parameters gives a 784-variable map with nonsingular derivative, whose image contains a complex Euclidean-open neighborhood by the inverse-function theorem. A polynomial vanishing on the full image vanishes on that neighborhood, hence is zero. All witness stages have nonzero integer determinants, as independently checked modulo 12289. Invertibility persists on a neighborhood of the witness, so the same argument applies within the invertible-stage locus. The second prime is an independent arithmetic cross-check; one nonzero residue already suffices logically.

The actual source point also yields a characteristic-zero lower bound of 906 for the leading-32×32 Jacobian rank, because a 906-square modularly nonzero subminor lifts to a nonzero integer subminor. It gives no characteristic-zero upper bound of 906. Consequently the evidence only places the generic characteristic-zero leading-32×32 image dimension between 906 and 1024.

Dominance does not mean surjectivity onto every prescribed 28×28 target. It does not show that the Fourier leading block, much less the full Fourier matrix, is attained. It does not extend automatically to a restricted coefficient family or a different interstage layout.

## 5. Second-order and affine-linear statements

Put `K=P3*S3*P2*S2*P1`, so `M=S4*K*S1`. Direct differentiation of the polynomial product gives

\[
\frac{\partial^2 M}{\partial d^{(4)}_i\,\partial d^{(1)}_j}=K_{ij}E_{ij}.
\]

This identity has no invertibility or anchor condition. At the saved integer witness all 1024 entries `K_ij`, `0 <= i,j < 32`, are nonzero modulo 12289 and therefore nonzero integers. In particular `K_00=11557` in that field. Six independently reconstructed full-product mixed finite differences, including all four rectangle corners, match the exact single-coordinate formula. Hence the mixed second derivatives at this point span all 1024 output coordinates in characteristic zero.

For every length N and any fixed interstage permutations, the same four-stage separated-generator family has no nontrivial universal affine-linear relation in its entire output matrix, including on the invertible-stage locus. To see this, choose both middle stages as `I+J`, where J is the all-ones matrix. These stages are permitted and invertible in characteristic zero, and

\[
K=P_3P_2P_1+(N+2)J
\]

has no zero entries. Choosing invertible outer diagonal stages gives `M_ij=K_ij*x_i*y_j`. An affine relation `sum(lambda_ij*M_ij)=c` valid for every nonzero x and y is a polynomial identity in distinct monomials `x_i*y_j` and 1. Its coefficients force `c=0` and every `lambda_ij=0`.

Neither a full second-order span nor the full two-point tangent span excludes nonlinear relations. For example, the map `(x,y) -> (x^2,xy,y^2)` has second derivatives spanning all three coordinates, but its image satisfies `v^2=uw`. Moreover, the full N=256 stage map has only 5120 formal parameters and 65536 output entries, so its full output coordinates necessarily have nonlinear algebraic dependencies; the absence of affine relations does not contradict this dimension bound.

The 32×32 modular rank defects are pointwise finite-field observations. They do not prove a universal tangent defect, generic complex rank 906, a complex codimension of 118, a universal nonlinear compatibility identity beginning at block size 29, or Fourier infeasibility.

## 6. Arithmetic-cost scope

Given already available generator coefficients, one separated stage can be applied by two exclusive weighted scans:

\[
y_i=a_i\sum_{j<i}b_jx_j+d_ix_i+c_i\sum_{j>i}e_jx_j.
\]

For N >= 2, the explicit fresh executor uses `5N-4` scalar multiplications and `4N-6` scalar additions per stage, with multiplication/addition by prescribed coefficients charged. At N=256, four stages use 5104 multiplications plus 4072 additions, totaling 9176 scalar field operations. Three explicit permutations gather 768 entries; those data movements are reported separately, not silently called arithmetic. Storage and coefficient loading are linear in N.

These counts were instrumented and checked against dense products at lengths 2, 3, 8, and 256, and for the complete supplied four-stage operator on a fresh deterministic input. They are an upper bound for this generic operator application, not a cost minimum. They do not include finding or certifying Fourier-realizing coefficients, building a uniform family of layouts, coefficient-generation cost, bit complexity, or a real-arithmetic conversion of complex scalar operations. The supplied coefficients are a Jacobian witness, not a Fourier assignment. Therefore these counts establish no FFT speedup or new asymptotic Fourier algorithm.

## 7. Reproduction and acceptance boundary

Run the two commands in README.md with Python 3, NumPy, and g++. No network access or original source executable is required. `FRESH_RESULTS.json` records all main results, selected pivot columns, derivative probes, matrix digests, and runtime versions. `BOUNDARY_AND_COST_RESULTS.json` records additional block ranks and instrumented application counts.

Accepted: the exact fixed-layout leading-28×28 dominance theorem, the nonsingular witness, the exact mixed-second-derivative identity and full coordinate span, the all-length absence of affine-linear identities, and the explicitly scoped modular observations.

Not accepted or claimed: a Fourier assignment, full-map dominance, a universal nonlinear obstruction or non-obstruction for the full matrix or leading-32×32 projection, a proof of generic complex rank 906, any unverified center/off-diagonal observation, a Toffoli-layout certificate, or an asymptotic FFT conclusion.
