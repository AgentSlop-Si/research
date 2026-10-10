# Norm escape that does NOT make an FFT

The previous archive correctly shows that a family with uniformly bounded induced 1-condition requires logarithmically many stages. But this is not a universal FFT bound: an O(N)-cost rank-one stage can have 1-condition Omega(N) *and spectral 2-condition exactly 1*.

For N>=3 take a real unit vector

    v = (1/sqrt(2), 1/sqrt(2(N-1)), ..., 1/sqrt(2(N-1))).

The Householder reflection `H=I-2 v v^T` is real orthogonal, is applied in O(N) arithmetic via `x -> x-2v(v^T x)`, and satisfies `H^(-1)=H`. Its first column has first entry 0 and all other entries `-1/sqrt(N-1)`; therefore

    ||H||_1 >= sqrt(N-1),   kappa_1(H)=||H||_1^2 >= N-1,
    kappa_2(H)=1.

One stage essentially satisfies the prior archive's necessary norm budget for a normalized DFT, while of course not implementing the DFT.

### Stronger exclusion for this rank-one-update escape

Suppose a circuit is a product of `t` stages `I+R_i` with `rank(R_i)<=r`, interspersed with arbitrary unitary monomial matrices (permutations and phases). Let `M` be the product of these monomial matrices with every `I+R_i` replaced by I. Telescoping and rank subadditivity show

    rank(U_N - M) <= t*r.

For `U_N=F_N/sqrt(N)`, with both `U_N` and `M` unitary, the trace overlap obeys

    |tr(M^* U_N)| <= sqrt(N)

because each selected Fourier entry has magnitude `1/sqrt(N)` and M selects one entry in each row/column. Consequently

    ||U_N - M||_F^2 >= 2N-2sqrt(N),
    ||U_N - M||_2 <= 2,
    rank(U_N - M) >= (N-sqrt(N))/2.

Thus `t*r >= (N-sqrt(N))/2`: in particular a constant number of Householder-type rank-one global stages cannot realize the DFT. This is a scoped exact linear-algebra lower bound for **low-rank updates to monomial matrices**, not for quasiseparable Green operators (whose distance from identity need not have low rank).

This control tells us why neither huge ||.||_1 nor full density is sufficient: a viable nonunitary design needs rich global dependence that is not just a small-rank update, without reverting to a telescoping FFT gauge.
