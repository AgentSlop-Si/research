# Local annihilator / three-stage Fourier certificate

**October 10, 2026.** Theorems and proof in characteristic zero. Exact finite-field experiments independently verify the finite instances but **are not substitutes for the proofs**. No new Fourier algorithm or asymptotic arithmetic upper bound is claimed.

## Definitions

Let `F_N[i,j]=omega^(i*j)`, for `omega` a primitive complex `N`th root of unity, and let `S` be an `N × N` quasiseparable matrix of order at most `r`: at every cut `c`,

- `rank(S[c:N,0:c]) <= r`;
- `rank(S[0:c,c:N]) <= r`.

The usual separated-generator rank-one model, with `S[i,j]=a_i b_j` below the diagonal, arbitrary diagonal, and `S[i,j]=c_i e_j` above the diagonal, belongs to this larger class. We allow singular stages, zero generators, arbitrary complex coefficients and arbitrary **internal** permutation matrices. Input and output Fourier indices remain in natural order except where a corrected formula explicitly mentions endpoint permutations.

All ranks in the proofs are over `C`. No assumption on coefficient magnitudes, positivity, unitary structure, or numerical conditioning is used.

## Lemma 1: local annihilator subspaces

Choose a consecutive interval `J` of `W` input-column coordinates for a rank-`r` quasiseparable matrix `S`.

Rows above `J` form a matrix of rank at most `r`, as do the rows below `J`. Stacking the two matrices gives rank at most `2r`. There is therefore a subspace `X_J ⊂ C^W`, of dimension at least `W-2r`, whose elements extended by zero outside `J` satisfy `supp(Sx) ⊂ J`.

Dually, for a consecutive interval `I` of `W` output-row coordinates, there is a space `Y_I ⊂ C^W` of dimension at least `W-2r` such that every `y` extended by zero outside `I` obeys `supp(y^T S) ⊂ I`.

The statement includes all degenerate generator and diagonal cases, since only rank subadditivity is used.

In particular, for `r=1`, an input interval of width 3 has a nonzero localized vector, while an output interval of width 5 has at least three linearly independent localized covectors.

## Lemma 2: nonzero finite Fourier Casoratian

Let `A` be an `s × w` matrix of full row rank `s`, where `1<=s<=w<=N`, and define `p_a(z)=sum_{u=0}^{w-1} A[a,u] z^u`. Set

`D(z)=det( p_a(omega^h*z) )`, with `a,h=0,...,s-1`.

Then

`D(z) = z^(s(s-1)/2) Q(z)`, with `Q` a **nonzero** polynomial of degree at most `s(w-s)`.

*Proof of the degree bound.* Cauchy–Binet expands `D` as a sum over `s` distinct exponent indices `0<=k_1<...<k_s<=w-1`. The associated power of `z` is `k_1+...+k_s`. The smallest possible exponent is `s(s-1)/2`; the largest is `s(w-1)-s(s-1)/2`. Their difference is `s(w-s)`.

*Proof of nonvanishing.* Perform invertible constant row operations on the `s` polynomials to get linearly independent polynomials `f_1,...,f_s` having **distinct degrees** `d_1,...,d_s`, all less than `N`. This is ordinary Gaussian elimination on polynomial coefficients, starting with the largest degree. The leading coefficient of their Casoratian as a polynomial in `z` equals

`(product of the leading coefficients) * det(omega^(h*d_a))_(a,h)`.

The latter is a Vandermonde determinant on distinct points `omega^d_a` and is nonzero. Constant row operations multiply the determinant by a nonzero scalar, so the original `D` cannot be the zero polynomial.

**Key specialization:** for `s=3,w=5`,

`D(z)=z^3 Q(z)`, `deg Q<=6`, `Q!=0`.

Thus at most six distinct nonzero values of `z` annihilate the determinant. The claim remains valid for an arbitrarily chosen rank-three row space supported on the five consecutive exponent positions, including exceptional zero generators.

## Theorem A: explicit three-sparse rejection of two stages

For every `N>=24` and any `N×N` quasiseparable order-one matrices `S_1,S_2` and internal permutation `P`,

`F_N != S_2 P S_1`.

Moreover, a witness `x` supported on **three consecutive coordinates** can be constructed such that the difference is detected by three row functionals supported on the first five output coordinates.

*Proof.* Fix output interval `I={0,1,2,3,4}`. Lemma 1 gives independent `y_0,y_1,y_2` supported on `I` satisfying `supp(y_a^T S_2) ⊂ I`. Collect them into `Y`, a full-row-rank `3×5` matrix.

For each `j=0,...,N-3`, put `J_j={j,j+1,j+2}`. Lemma 1 gives a nonzero `x_j` supported on `J_j` with `supp(S_1 x_j) ⊂ J_j`. When `P(J_j)` is disjoint from `I`, every component of `Y S_2 P S_1 x_j` is zero.

Each of the five elements of `P^{-1}(I)` belongs to at most three sliding input intervals `J_j`. Thus **at most 15** indices `j` are forbidden by an intersection `P(J_j) ∩ I != empty`.

Let `omega` be a primitive `N`th root and define `p_a(z)=sum_{i=0}^4 Y[a,i] z^i`. On `J_j`, the matrix `Y F_N[:,J_j]` is `[p_a(omega^(j+h))]_(a,h=0..2)`. Its determinant equals `omega^(3j) Q(omega^j)` with the nonzero degree-≤6 polynomial of Lemma 2. It can be singular for **at most six** values of `j`.

Of the `N-2` input triples, at least `(N-2)-15-6 = N-23` have both nonintersection and nonsingular Fourier projection. Since `N>=24`, choose such a `j`. Nonzero `x_j` has `Y F_N x_j !=0`, while `Y S_2 P S_1 x_j=0`. This disproves equality, and is a constructive mismatch certificate. QED.

**Scope:** natural Fourier endpoints, or affine/coprime-stride endpoint reorderings after appropriate phase and primitive-root adjustments. The bound `N>=24` is **weaker** than the previously saved two-stage rank barrier for natural endpoints. The new feature is an explicit sparse mismatch vector and a polynomial determinant certificate without nonzero-generator assumptions.

## Theorem B: general three-stage interval-rank gate

Let `M=S_3 P_2 S_2 P_1 S_1`, where stage `S_i` has quasiseparable order `r_i`. Pick consecutive input and output windows `J,I`, both of length `W`, in the stage coordinates. Define the middle-coordinate supports

- `C=P_1(J)` for the input of `S_2`;
- `R=P_2^{-1}(I)` for the output of `S_2`.

Let `k(R,C)` be the minimum number of **rows of R plus columns of C** that must be removed to put every remaining row strictly to one side of every remaining column in middle-stage coordinate order. In symbols, with a cut `c`:

`k = min_c { #(R>c)+#(C<=c), #(R<=c)+#(C>c) }`.

For any target matrix `T` with `h=rank(T[I,J])`, the equality `T=M` necessarily implies

`h <= 2r_1 + 2r_3 + r_2 + k(R,C)`.

*Proof.* Lemma 1 gives an input compression `X` with `W-2r_1` independent vectors supported in `J`, such that `S_1 X` remains supported in `J`; and an output compression `Y` with `W-2r_3` independent rows supported in `I`, such that `Y S_3` remains supported in `I`. Passing the outside factors and permutations leaves a compression of the middle submatrix `S_2[R,C]`.

After deleting the `k` exceptional rows/columns, the remaining middle submatrix crosses one strict upper/lower cut, so has rank at most `r_2`. Restoring each deleted row or column increases rank by at most one. Hence

`rank(Y M X) <= rank(S_2[R,C]) <= r_2 + k`.

By Sylvester's rank inequality, because `Y` and `X` have respective ranks at least `W-2r_3` and `W-2r_1`,

`rank(Y T X) >= h - 2r_3 - 2r_1`.

Equality `T=M` requires the two bounds to be consistent, giving the claim. QED.

For the **natural-order Fourier matrix**, every `W×W` submatrix with consecutive input and output indices is invertible: it becomes a Vandermonde matrix (times invertible diagonals) with distinct `N`th roots of unity. Consequently `h=W`, and the necessary condition is

`k >= W-(2r_1+r_2+2r_3)`.

For **three rank-one stages**, this simplifies to

`k >= W-5`.

At `W=6`, *any* pair of windows whose middle supports are strictly ordered (`k=0`) rules out that three-stage architecture. No generator normalization, nonzero corners, or bounded coefficient assumptions are needed.

**Endpoint correction:** if the Fourier input or output is independently reordered non-affinely, the Vandermonde shortcut `h=W` can fail. Use the actual rank `h=rank(T[I,J])` in the general inequality; NEVER substitute `W` automatically. For prime-order Fourier matrices every square minor is known to be nonzero by Chebotarëv's theorem, so `h=W` remains true for arbitrary endpoint permutations at prime length. This latter full-spark fact is classical, not established by our finite-field power-of-two experiments.

## Lemma 3: expected count of ordered pairs under random permutations

Let `P_1` and `P_2` be independent uniformly random permutations. Fix a pair of length-`W` endpoint windows with `2W<=N`. Their middle sets `C,R` are independent uniformly random `W`-subsets. They are strictly separated (`k=0`) with probability

`2 * binomial(N,2W) / binomial(N,W)^2`.

*Proof:* pick the common `2W`-element union in `binomial(N,2W)` ways, and choose which of its two ordered halves is `R`; there are two choices. Divide by the total `binomial(N,W)^2` ordered pairs of independent subsets. The probability is zero if `2W>N`.

Therefore the **expected number of strictly separated endpoint window pairs** is

`(N-W+1)^2 * 2*binomial(N,2W)/binomial(N,W)^2`.

For fixed `W=6` and large `N`, this is asymptotic to `(N-5)^2 / 462`. This is an expectation, **not** a proved high-probability statement, because overlapping windows produce dependent events.

## Exact computational certificate details

`annihilator_gate.py` implements the formula for `D(z)` by independent Cauchy–Binet sums of modular determinants, then compares every root evaluation with a directly computed Fourier 3×3 determinant. It finds explicit three-sparse witnesses for each tested `N>=24`, including singular and zero-generator stages.

`test_new_gate.py` has eleven independent regression groups (two exact prime fields, `12289` and `65537`, and power-of-two lengths through 128). `independent_verifier.py` builds the **full dense three-stage product** from explicit permutation matrices, independently of the linear-work executor, and checks nine rank witnesses. `EXPERIMENT_RESULTS.json` records observed permutation counts and exact stage-compression ranks. Positive checks of randomized stage products ensure that the new rank gate does not reject valid *matrix products* in its stated model.

The coefficients are those of the exact NTT analogue. Nonzero modular polynomial/determinant witnesses also provide valid characteristic-zero nonvanishing examples, but sampled modular ranks cannot establish a universal complex theorem. The universal theorems above follow instead from the algebraic arguments.

## What was NOT proved

- No exact factorization of `F_N` into fewer than logarithmically many unrestricted global stages.
- No lower bound excluding all three-stage quasiseparable architectures: bit reversal at both internal boundaries survives the present necessary test.
- No `O(N)` or `o(N log N)` implementation from these constructions.
- No global lower bound on all complex-arithmetic Fourier circuits; the theorems concern restricted quasiseparable factorization architectures.
- No priority or external mathematical novelty claim; these are results and verification developed for this research checkpoint.
