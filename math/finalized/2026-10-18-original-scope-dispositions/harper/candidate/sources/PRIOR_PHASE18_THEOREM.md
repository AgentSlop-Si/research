# Phase 18 — Harper duality, exact polynomial depth, and Green-product Fourier phase gates

**Date:** October 9, 2026  
**Status:** Symbolic arguments plus reproducible exact finite-field certificates. **NOT an `o(N log N)` FFT.**

## 0. Provenance and prior art

The finite periodic Harper matrix, its commutation with the DFT, and the repeated zero eigenvalue when `4|N` are **known**, not original claims. See Barker–Candan–Hakioğlu–Kutay–Ozaktas, *The discrete harmonic oscillator, Harper's equation, and the discrete fractional Fourier transform*, J. Phys. A 33 (2000), 2209–2222, DOI `10.1088/0305-4470/33/11/304`; and *On the raising and lowering difference operators for eigenvectors of the finite Fourier transform*, J. Phys.: Conf. Ser. 597 (2015), 012012. Our project-specific work below derives and audits: (a) exact optimal polynomial degrees and a leading coefficient for the parity-resolved Harper representation, (b) a one-column sparse intertwiner certificate, and (c) an all-permutation/diagonal phase veto for *fixed* nonunitary Green-sum products. **No literature-priority claim.**

## 1. Conventions and the self-dual sparse operator

Take `N` divisible by four, `ω=exp(-2πi/N)` and normalized `F[j,k]=ω^(jk)/sqrt(N)`. Let `Z e_k=e_(k+1 mod N)` and `D e_k=ω^k e_k`. Directly,

`F Z=D F`, `F D=Z^(-1) F`, and `F^2=J`, where `J e_k=e_(-k mod N)`.

Set `T=Z+Z^-1`, `V=D+D^-1=diag(2 cos(2πj/N))`, `H=T+V`, `K=T-V`.

**Weyl/Harper duality:**

`F T=V F`, `F V=T F`, so `F H=H F` and `F K=-K F`.

`H` is real symmetric and cyclic tridiagonal, with `3N` or fewer nonzero entries for `N>=5`. Application `Hx` takes linear arithmetic. Nonexceptional `(H-λI)^-1 x` is executable with a cyclic-tridiagonal solver in `O(N)` arithmetic (the corner correction is rank two).

## 2. Exactly two zero modes, split by reflection

The reflection `J` commutes with `H`. Its `+` parity sector has dimension `L_+=N/2+1`, with real orthonormal basis

`e_0`, `(e_j+e_(N-j))/sqrt(2)` for `1<=j<N/2`, `e_(N/2)`.

Its `−` sector has dimension `L_-=N/2-1`, with basis `(e_j-e_(N-j))/sqrt(2)` for `1<=j<N/2`.

In these bases `H_+` and `H_-` are real symmetric *irreducible tridiagonal* Jacobi matrices. Both have diagonal `v_j=2cos(2πj/N)` on their respective `j` intervals. `H_+` has offdiagonal weights `(sqrt(2),1,...,1,sqrt(2))`; `H_-` has unit offdiagonal weights. Their spectra are therefore individually simple.

Write `N=4m`. In both blocks the dimension is odd (`2m+1`, `2m-1`) and the potential changes sign under index reversal `j ↦2m-j`: `v_(2m-j)=-v_j`. Offdiagonal weights are reversal-symmetric. Define the signed reflection in either block by `C u_j=(-1)^j u_(L-1-j)`, with positions counted locally. Then `C H_± C^-1 = -H_±`.

Hence each odd-dimensional Jacobi block has spectrum symmetric about zero and contains a zero eigenvalue. Simplicity makes its zero eigenvalue **one-dimensional**. Therefore `dim ker H=2`, with one zero mode `v_+` in `J=+1` and one `v_-` in `J=-1`.

`F` commutes with `H` and `J` and preserves each zero line. Since `F²=J`, on these lines it acts by `λ_+∈{+1,-1}` and `λ_-∈{+i,-i}` respectively. Thus **there is no single scalar function** `f` defined on the spectrum of `H` with `F=f(H)`. In particular no `p(H)/q(H)` with `q(H)` invertible equals `F`, regardless of degrees or number of partial-fraction resolvents. This is a restricted *single-commuting-operator* no-go, not a bound for arbitrary noncommuting Green sums.

## 3. Sharp parity-resolved polynomial identity

Each `H_±` is a real symmetric irreducible tridiagonal matrix with `L_±` simple eigenvalues. As `F` commutes with `H` and with `J`, its restriction `F_±` is a polynomial of `H_±` of degree at most `L_±-1`, uniquely so at these degrees. Therefore, for uniquely determined polynomials `p_±` of degrees at most `N/2`, `N/2-2`,

`F = p_+(H)(I+J)/2 + p_-(H)(I-J)/2`.

The upper bounds are **attained exactly**:

- Row `0` and column `N/2` are at cyclic graph distance `N/2`; `H^d[0,N/2]=0` for `d<N/2`, while `F[0,N/2]=1/sqrt(N)`. Reflection fixes coordinate zero, so the `−` projector does not contribute to that entry. Thus `deg p_+>=N/2`. At distance exactly `N/2`, only the two shortest circular routes contribute, so `H^(N/2)[0,N/2]=2` and

  **`coeff_(N/2)(p_+)=1/(2 sqrt(N))`.**

- In the antisymmetric Jacobi basis, first and last coordinates are `N/2-2` steps apart. At smaller degrees the relevant entry of any polynomial of `H_-` is zero. The true Fourier entry is `(ω^(N/2-1)−ω^(-(N/2-1)))/sqrt(N) = -(2i/sqrt(N))sin(2π/N)`, which is nonzero. Therefore `deg p_-=N/2-2`, and the same Fourier entry is its highest coefficient because all odd-block offdiagonal weights are 1.

**Exact degree theorem:**

`deg p_+=N/2`, `deg p_-=N/2-2` for every `N>=4` divisible by four.

This is a degree obstruction **for polynomial functional calculus**. It is not an arithmetic circuit lower bound: identities with different noncommuting operators, rational functions in a larger algebra, shared computation DAGs, or nonstandard arithmetic primitives are not covered. A direct Horner evaluation of these polynomials using sparse `H` takes `Θ(N²)` arithmetic; an unexplored algorithm exploiting the coefficients more deeply might do better.

### Independent exact audit

`harper_certificate.py` works over the prime `998244353`, using primitive `N`th roots and modular square roots. It constructs the parity Jacobi matrices, finds both zero eigenvectors by recurrence, verifies their inequivalent Fourier eigenvalues, interpolates the two polynomials by an upper-triangular Krylov first-row system, and independently checks **every matrix entry** after polynomial evaluation. All cases `N=4,8,16,32,64,128` pass, including exact leading-coefficient identities. `harper_audit.json` preserves the output.

## 4. One four-phase mask: a positive algebraic control, not a speedup

Because `F` is complex symmetric and unitary, its real and imaginary parts are commuting real symmetric matrices. They can be simultaneously diagonalized by a real orthogonal basis `O`, and `F^4=I` gives

`F=O Λ O^T`, `Λ[j,j]∈{1,-1,i,-i}`.

A concrete `O` can be assembled from real eigenvectors of `H_+` and `H_-`, because each Jacobi spectrum is simple. `spectral_basis_control.py` independently reconstructs `F` with maximum absolute entrywise error below `2.3e-14` for `N=8,16,32,64,128`.

**Consequence:** high-order diagonal Fourier phases can be reduced to a single *quaternary* phase mask if the surrounding *real* basis transforms are unrestricted. This does not contradict Phase 14's Galois field obstruction: the real basis has algebraic coefficients whose field degree grows with `N` and has no demonstrated fast executor.

Also, if `O` is compiled into `g` two-coordinate real orthogonal gates, the pair `O,O^T` with the free diagonal phase mask implements `F` in at most `2g` such gates. The standard unitary-gate matrix-entropy lower bound for `F` then implies `g >= (N/4)log₂ N`. This **restricted orthogonal-gate** bound is inherited from Ailon's entropy framework (Phase 16), not a lower bound on arbitrary Green/nonunitary circuits.

## 5. New sparse two-generator phase-coherence certificate

For arbitrary `N>=4` even, define `T` and `V` as above. Their *joint commutant* consists exactly of

`{X: XT=TX and XV=VX} = {a I+b J : a,b∈C}`.

**Proof:** In the parity basis, `V` is diagonal with distinct values within each parity sector (because `cos θ` is strictly decreasing on `[0,π]`). Thus a matrix commuting with `V` has diagonal `++/--` blocks; each cross-parity block can have nonzero entries only at matching interior indices. `T_±` are irreducible Jacobi tridiagonal blocks. Commuting with `T` forces each diagonal block to be scalar. The cross-parity blocks vanish: the first even endpoint, absent from the odd sector, gives `sqrt(2)*x_1=0`, and the tridiagonal recurrence forces all interior `x_j=0`. Thus `X=aP_++bP_-=cI+dJ`.

Let `M` be any linear candidate circuit (not assumed unitary or invertible). If it satisfies both exact sparse intertwining identities

**`M T=V M` and `M V=T M`,**

then `F^-1 M` commutes with both `T,V`, so necessarily

**`M=F(aI+bJ)`** for scalars `a,b`. A **single calibration vector** suffices to select the actual Fourier transform:

**`M e_1=F e_1` implies `M=F`,** since `e_1` and `Je_1=e_(N-1)` are independent.

This gives a compact *symbolic proof target* for Green-product circuits: derive two identities against sparse known operators, then test one vector. It is not a faster black-box equality test if the identities themselves must be checked by exhaustive input probing; the already-known stronger Weyl relation `MZ=DM` plus a first-column calibration also suffices. The merit here is the symmetric Harper/Green algebraic formulation.

`dual_intertwiner.py` checks both identities exactly over the finite field for `F`, `FJ`, and arbitrary linear combinations; the one-vector distinction passes at `N=4..128`. Four independently sampled two-sum Green products fail both intertwiners at every entry at `N=8,16,32,64`.

## 6. Universal middle-mononomial veto for FIXED Green-product factors

Let `M=A Q P B`, with fixed invertible `A,B`, middle arbitrary invertible diagonal `Q` and arbitrary permutation `P`, and let `Z,D` be as in Section 1. The necessary covariance `MZ=DM` implies

`U (QP)=(QP) V`, with **`U=A^-1 D A`** and **`V=B Z B^-1`**.

Therefore `U` and `V` are *monomially similar*: diagonal multisets agree, and so do all permutation-invariant directed cycle products, including

`multiset_i U[i,i] = multiset_i V[i,i]`,

`multiset_{i<j} U[i,j]U[j,i] = multiset_{i<j} V[i,j]V[j,i]`.

A mismatch in either invariant rules out **every** possible intermediate permutation and invertible diagonal mask for these **fixed** outer factors, without enumerating either. This is a necessary-only test.

Without `P`, the equation `UQ=QV` is solved *exactly* by a graph potential: for every nonzero matrix position, `q_i/q_j=U[i,j]/V[i,j]`; check edge support and multiplicative consistency on cycles. `weyl_gate.py` implements it with modular field arithmetic and includes a positive control that reconstructs the correct diagonal mask up to a global factor.

For sampled two-Green-sum factors with *N-th root chirp gauges* (so the stages already contain high-order Fourier phases), all arbitrary middle monomial masks are ruled out by **both** invariants at `N=8,16,32,64`. Those are finite counterexamples for parameter-fixed stage instances, not any all-parameter impossibility theorem. Exact modular nonzero witnesses prove the corresponding lifted cyclotomic-stage contradictions in characteristic zero provided their inverses reduce nonsingularly. The sampled raw products have full support and completely fail `MZ=DM`.

**Cost warning:** the Green stages each apply through two tridiagonal solves and diagonals/permutations in `O(N)` arithmetic. The dense `O(N³)` inversion in the audit is only for offline verification of the fixed small examples; it is *not* an executor for an FFT.

## 7. Important research status

**Verified:** the sharp polynomial-degree theorem in the scalar-plus-parity Harper algebra; existing Harper zero-mode obstruction reproved; one-mask real spectral control; sparse dual-intertwiner characterization; exact all-middle-mononomial vetoes for specified two-sum Green factors; positive controls that prevent rejecting valid diagonal gauges.

**Not proved:** no universal impossibility theorem for products of noncommuting Green sums with tunable high-order coefficients; no exact sub-`N log N` FFT; no linear-time Fourier eigenbasis; no improvement to integer-multiplication bit complexity.

**Next gate (Phase 19):** seek a product of independently ordered, *noncommuting* shifted Green operators whose composed transfer map satisfies `M T=V M`, `M V=T M` *symbolically* (not just finite numerical fitting). Eliminate arbitrary central diagonal/permutation masks first using the exact monomial similarity invariants. If a candidate passes the two sparse equations, fix its scalar/gauge with the one-vector probe and verify a complete matrix identity independently. Count actual scalar operations, root-coefficient preparation, memory movement, and stability. Do not repeat single-Harper rational functions, direct spectral polynomial interpolation, or unitary butterfly fusion.
