# Exact rank-rigidity theorem for the saved four-stage FFT layout

**October 10, 2026.** The results below concern only the **fixed 256-point, three-affine-permutation layout** stored in `AFFINE_LAYOUT.json`. There is no Fourier factorization here; this is a theorem about necessary coefficient structure *if* a factorization exists.

## Stage class and rank budgets

Fix arbitrary complex matrices `S1,S2,S3,S4` with two-sided quasiseparable order ≤1. That means every strictly lower or upper off-diagonal submatrix crossing a contiguous cut has rank ≤1. Include all degenerate generators, singular matrices and zero entries. Suppose

\[
F_{256}=S_4P_3S_3P_2S_2P_1S_1.
\]

For an **arbitrary** choice of diagonal matrices `Dj`, set `Ej = Sj-Dj` and `hj = rank(Ej)` (ordinary matrix rank, not quasiseparable order). No invertibility of the `Dj` is assumed. For each nonempty subset `J` of `{1,2,3,4}`, the certificates prove

\[
\boxed{\sum_{j\in J}h_j\ge b_J}
\]

with these exact lower bounds:

| Replacement set J | b_J | Input parity mask | Intermediate cut budget | Fourier rank |
|---|---:|---:|---:|---:|
| {1} | 38 | 157 | 90 | 128 |
| {2} | 44 | 44 | 84 | 128 |
| {3} | 69 | 236 | 59 | 128 |
| {4} | 46 | 136 | 82 | 128 |
| {1,2} | 119 | 79 | 9 | 128 |
| {1,3} | 118 | 59 | 10 | 128 |
| {1,4} | 112 | 65 | 16 | 128 |
| {2,3} | 109 | 152 | 19 | 128 |
| {2,4} | 95 | 240 | 33 | 128 |
| {3,4} | 105 | 48 | 23 | 128 |
| {1,2,3} | 127 | 236 | 1 | 128 |
| {1,2,4} | 127 | 109 | 1 | 128 |
| {1,3,4} | 127 | 136 | 1 | 128 |
| {2,3,4} | 127 | 128 | 1 | 128 |
| {1,2,3,4} | 128 | 1 | 0 | 128 |

In particular:

\[
\boxed{h_1+h_2+h_3+h_4\ge119+69+46=234.}
\]

This last bound combines the independent inequalities for `{1,2}`, `{3}` and `{4}`. The vector `(70,49,69,46)` satisfies all 15 inequalities and sums to 234. Therefore 234 is the strongest total-rank lower bound obtainable by merely combining **these** 15 linear inequalities; it is **not** evidence that actual FFT factors with those ranks exist.

## Why each 15-entry inequality is valid

For each initial binary parity mask `a`, let `A0={x: parity(x & a)=0}` (128 coordinates). Transport this set through the fixed permutations: `A_{j}={i : p_j[i] belongs to A_{j-1}}`, for j=1,2,3. Set `C=A0`, `R=(A3)^c`. Let `d(A)` count the number of changes between membership and nonmembership on the natural line of 256 coordinates.

A two-sided quasiseparable order-one stage has off-diagonal cross-partition rank at most `d(A)`. Each boundary lets at most one forward/backward scalar information channel cross, so this follows either from the rank-one interval decomposition or by an explicit scalar-flow graph.

Replacing stages in `J` by **diagonal** matrices leaves them with zero cross-partition cost. Consequently the replacement product `M_J` obeys

\[
\operatorname{rank}(M_J[R,C])\le \sum_{j\notin J}d(A_{j-1})=c_J(a).
\]

Changing `Sj` to `Dj` in any product alters that product by a matrix of rank at most `rank(Sj-Dj)=hj`. Sequentially replacing stages yields the telescoping inequality

\[
\operatorname{rank}(F_{256}[R,C])\le c_J(a)+\sum_{j\in J}h_j.
\]

For every row in the table, the input mask in `EXACT_CERTIFICATES.json` has `c_J(a)=128-b_J`, and the corresponding Fourier submatrix has full rank 128 over the complex numbers. Rearranging proves the theorem. No stage coefficient appears in the certificate.

## Exact characteristic-zero Fourier rank certificates

The unnormalized Fourier matrix is `F[i,j] = zeta_256^(i*j)` for one primitive complex 256th root `zeta_256`. A determinant of its 128×128 selected submatrix is an algebraic integer in `Z[zeta_256]`.

We evaluate the same determinant in two prime fields, modulo **12289** (primitive 256th root **8340**) and modulo **65537** (root **282**). Each primitive root is a zero of `Phi_256(X)=X^128+1`. If the complex cyclotomic determinant were zero, every compatible modular image would be zero. But **all 30 modular determinants are nonzero**. Their exact residues, input/output index sets and path boundary counts are stored in `EXACT_CERTIFICATES.json` and recreated without floating point by `verify_rank_rigidity.py`.

A further `audit_all_parity_cuts.py` checks Fourier block ranks for **all 255 masks in each field**, plus **3,825 integer maximum-flow calculations** (all 15 nonempty subsets of stages times all 255 masks). Every stored witness is also an exact min-cut of the full scan graph. The search establishes optimality **within this parity-mask/min-cut family**, not among arbitrary subsets or nonlinear coefficient relations.

## Extension to inverse stages and generator support

When `Sj` and an invertible diagonal `Dj` are invertible, `rank(Sj-Dj)=rank(Sj^{-1}-Dj^{-1})`. Thus the same restrictions apply to low-global-rank deviations of the outer inverse stages used in the previous checkpoint, provided the diagonal comparison matrices are invertible.

For separated generators `L_ij=a_i b_j` below and `U_ij=c_i e_j` above the diagonal, ordinary rank obeys `rank(L+U) ≤ rank(L)+rank(U)`. Therefore each lower bound also constrains how many independent lower/upper generator contributions may remain active. It does **not** imply that a rank-one quasiseparable stage has ordinary rank one: a strictly lower triangular matrix with rank-one off-diagonal blocks can itself have rank N−1.

## Limitations

- The theorem does not exclude the saved four-stage exact factorization. An order-one quasiseparable stage can be far from every diagonal in ordinary matrix rank while costing O(N) arithmetic to apply.
- No asymptotic faster-than-FFT construction is given.
- These are necessary rank conditions. Satisfying them is not sufficient for exact Fourier coefficient compatibility.
- The 15 inequalities are certified for this saved N=256 layout and not claimed for all choices of permutations.
