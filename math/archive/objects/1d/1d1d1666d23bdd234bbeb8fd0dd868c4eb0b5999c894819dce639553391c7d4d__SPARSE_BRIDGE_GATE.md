# Exact sparse-bridge formulation of the smallest surviving Green product

**Research status:** Algebraically proven reformulation, not a Fourier factorization or faster FFT. Meant as a precise symbolic target for the next project phase.

Let `A,B,C,D` be *invertible* weighted cyclic difference matrices `I-diag(w) P_sigma` (single-cycle permutations sigma arbitrary and non-affine). Each has at most **two** nonzero entries per row and column, with O(N) nonzeros overall. Define

    M = (A^(-1)+B^(-1))(C^(-1)+D^(-1)).

The noncommutative identity

    A^(-1)+B^(-1) = A^(-1)(A+B)B^(-1)

holds without assuming A and B commute. Therefore the following **exact bridge identity** holds:

    **A M D = (A+B) (C B)^(-1) (C+D).**                   (B1)

Write `X=A+B`, `Y=C+D`, `K=CB`:

    K has at most 4 nonzero entries per row and column;
    X and Y have at most 3 nonzero entries per row and column;
    all have O(N) nonzero entries.

The matrix `A M D` is therefore a **sparse Schur complement** `X K^(-1) Y` from an explicit O(N)-nonzero graph, even when its entries are globally dense.

If a candidate claims `M=F_N`, it must satisfy the **inverse-free polynomial matrix identity**

    **det(CB) A F_N D = (A+B) adj(CB) (C+D).**           (B2)

For cyclic difference denominators `det(B)=1-prod_i w_B[i]`, and similarly for `C`, so the scalar factor on the left is explicitly

    (1-lambda_C)*(1-lambda_B).

Moreover, `adj(CB)=adj(B) adj(C)`, and for cyclic weighted shifts with `T_B^N=lambda_B I`,

    adj(B) = I+T_B+...+T_B^(N-1).

This produces a **polynomial identity in the edge weights and Fourier root** with no matrix inverse and no numerical fitting assumptions. Root-of-unity identities can be reduced modulo the cyclotomic polynomial; invalid coefficient charts can be eliminated by exact-field witnesses without asserting the converse of modular vanishing. All denominator nonzero conditions must be enforced.

The determinant also imposes a necessary scalar constraint

    det(F_N) prod_{V in {A,B,C,D}} det(V)
      = det(A+B) det(C+D).                                (B3)

An exact identity on every entry is vastly stronger than a graph min-cut passing. The smallest surviving constructor must solve (B2) uniformly in N and satisfy the Fourier covariance `MS=D_N M`, `M e0=ones` (unnormalized convention). An O(N)-sparse Schur complement representation does not itself give an O(N) algorithm for *constructing Fourier's exact phases*: sparse linear systems on general expander-like graphs need not be solvable in linear work.

`python bridge.py` tests (B1) with exact finite-field matrices for lengths 5,7,8,11,13, and deliberately rejects reversing the noncommutative bridge `CB` into `BC`.

**Limit:** The sparse-bridge identity is a direct algebraic consequence of the sum-of-inverses formula; the equivalence alone is not claimed as an unpublished mathematical breakthrough. It is a concrete, verifiable gate for the surviving hypothesis.
