# Proof certificate — four-stage FFT block projection and second-order span

**10 October 2026.** These statements concern the saved **fixed** `N=256` affine permutations and the separated-generator subfamily of order-one quasiseparable stages. All stage coefficients are independently variable complex numbers. This is **not** a new FFT algorithm or a general FFT lower bound.

## Definitions

For each stage `S_k`,

\[
(S_k)_{ij}=\begin{cases}
a^{(k)}_i b^{(k)}_j&i>j,\\
d^{(k)}_i&i=j,\\
c^{(k)}_i e^{(k)}_j&i<j.
\end{cases}
\]

With `P_i x = x[p_i]` for the three exact permutations in `AFFINE_LAYOUT.json`, let

\[
\Phi=S_4P_3S_3P_2S_2P_1S_1.
\]

The map from the 5120 scalar generator coefficients to the leading `m×m` block is polynomial over the integers. `jacobian_joint_blocks.py` forms its Jacobian analytically by inserting rank-one derivatives into the product; `verify_joint_gate.py` independently tests representative derivative columns by exact finite differences of the full matrix product.

## Theorem A (polynomial independence on the leading 28×28 block)

**There exists no nonzero polynomial in the 784 leading block entries that vanishes for every product** of the specified four stages. The same is true if the stages are required to be invertible.

**Certificate:** `GENERATOR_POINT_1.json` is an explicit integer coefficient assignment. `witness28.json` contains 784 exact parameter column indices. The corresponding **square 784×784 Jacobian minor** has nonzero determinants

\[
\det J_{784}\equiv5424\pmod{12289},\qquad
\det J_{784}\equiv42512\pmod{65537}.
\]

Both fields use the identical integer coefficient assignment and identical 784 selected columns. Thus that integer determinant is nonzero, and the complex Jacobian is surjective onto these 784 output entries at this parameter point. By the complex analytic inverse/submersion theorem, the polynomial map's image contains a nonempty Euclidean-open subset of `C^784`; no nonzero polynomial can vanish on its entire image. The invertible-stage parameter locus is Zariski-dense in coefficient space because stage determinants are nonzero polynomials (each stage can equal the identity), so an identity holding on only invertible products would extend to all products, also impossible.

This theorem concerns a **universal polynomial identity**; it does **not** say the map hits every particular 28×28 target exactly, and it does not settle the 256-point Fourier matrix.

## Theorem B (second-order coordinate completeness)

Fix the two middle stages and write

\[
K=P_3S_3P_2S_2P_1,\qquad M=S_4KS_1.
\]

For independently variable outer diagonal parameters, the mixed second derivative is

\[
\frac{\partial^2M_{uv}}{\partial d^{(4)}_i\,\partial d^{(1)}_j}
=\delta_{ui}\delta_{vj} K_{ij},
\]

or, as matrices, `∂²M/∂d4_i ∂d1_j = K[i,j] E_ij`. This is an **exact polynomial identity**, with no inverses, nonzero-anchor assumptions, or numerical approximations. Hence if `K[i,j] != 0` on a coordinate rectangle, the mixed second derivatives span the entire vector space of matrices supported on that rectangle.

At `GENERATOR_POINT_1.json`, the 1024 entries of the leading 32×32 block of `K` are **all nonzero modulo 12289**. Therefore they are all nonzero as integers, and the **second-order osculating space of the 32×32 projected map is the full 1024-dimensional space over C**. The program checks one mixed finite difference directly, obtaining exactly `K[0,0]=11557 (mod 12289)` in the (0,0) output cell and zero in all other cells.

## Theorem C (no universal affine-linear relations — all lengths)

For **any** `N` and any fixed interstage permutations, the four-stage separated-generator family satisfies **no nontrivial affine-linear identity in its entire `N×N` output matrix**.

Choose both middle stages as `I+epsilon J` for any positive epsilon, where `J` is the all-ones matrix. This belongs to the separated-generator stage family and is invertible. Permutations preserve `J`, so `K=P3(I+epsilon J)P2(I+epsilon J)P1 = P3P2P1 + (2epsilon+N epsilon²)J`; all of its entries are strictly positive. Take the outer stages to be independent nonsingular diagonal matrices `diag(x_i)` and `diag(y_j)`. Then `M_ij=K_ij x_i y_j`.

If `sum lambda_ij M_ij = c` for every invertible choice of the stage coefficients, then the polynomial `sum lambda_ij K_ij x_i y_j - c` vanishes for all nonzero choices of `x_i,y_j`. The distinct monomials `x_i y_j` and the constant monomial are linearly independent, so `c=0` and all `lambda_ij=0`.

This does **not** exclude nonlinear polynomial relations.

## Additional finite-field observations (NOT characteristic-zero theorems)

At the explicit integer generator point, the local Jacobian rank of the leading 32×32 output block is **906 over each** `GF(12289)` and `GF(65537)`. The leading 29×29 block ranks 831 of 841 over the first field. The same 32×32 **output matrix** itself has full matrix rank 32. These modular Jacobian deficiencies **do not prove** that the complex Jacobian is deficient; rank over C can be larger than a modular specialization. In particular, they do not prove a polynomial identity vanishes on the whole image.

As an exact modular curvature witness, adjoining the mixed derivative `K[0,0] E_00` to a 906-column independent Jacobian basis raises rank to 907 over GF(12289). Moreover, a square matrix built from 906 Jacobian columns at `GENERATOR_POINT_1.json` and 118 at `GENERATOR_POINT_2.json` has determinant **4142 modulo 12289**. These checks independently corroborate the absence of a *fixed* first-order linear constraint, though Theorem C supplies a stronger proof.

## Verification

`OPENBLAS_NUM_THREADS=1 python verify_joint_gate.py`

The script checks analytic derivatives against full product perturbations, both nonzero Jacobian minor determinants, both modular local-rank observations, the complete mixed-second-derivative coordinate identity, and the two-point tangent-span minor. `rankmod.cpp` carries out integer finite-field elimination and prints pivot coordinates. The previous 64-gate archive is included as `prior_checkpoint_full.zip`.
