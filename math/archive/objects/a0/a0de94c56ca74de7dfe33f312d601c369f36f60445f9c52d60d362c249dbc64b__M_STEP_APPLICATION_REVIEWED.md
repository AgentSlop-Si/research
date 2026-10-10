# M-step product: an actual raw-coordinate application circuit

Continuation of JOINT_ORBIT_REPORT.md. The first-order identity can be iterated exactly and does give a useful scalar-denominator kernel equation. The fully specified application circuit below still costs Theta(N log N) in its chosen radix schedule. This is a construction/accounting result, not an unrestricted lower bound.

## 1. Exact iterated identity and coefficient recurrence

Work in R=K[X]/(X^M-eta), modulo z^M. Define

    P_r(X,z)=product_(j=0)^(r-1)(1+X^j z).

Iterating D_X(z)=(1+z)D_X(Xz) gives

    D_X(z)=P_M(X,z) D_X(eta z).

The coefficient p_s=[z^s]P_M, 0<=s<M, is

    p_s = X^binom(s,2) F_M(X)/(F_s(X)F_(M-s)(X))
        = product_(j=0)^(s-1)(X^j-eta) /
          product_(j=1)^s(1-X^j).

Therefore

    (1-X^s)p_s=(X^(s-1)-eta)p_(s-1).

All denominators are invertible in R: they are nonzero at every q_h. For 1<=s<M, coefficient extraction from the M-step identity gives

    (1-eta^s) k_s = sum_(r=1)^s p_r eta^(s-r) k_(s-r).

The scalar 1-eta^s is nonzero. This is a valid triangular kernel-preparation equation. A direct implementation charges its convolution sums; scalar denominators alone do not make the whole computation linear.

## 2. Why the same equation is not a free solve for arbitrary input

For arbitrary input polynomial a(z), let y(z)=D_X(z)a(z). Then

    y(z)=P_M(X,z)D_X(eta z)a(z),
    y(eta z)=D_X(eta z)a(eta z).

One cannot replace D_X(eta z)a(z) by y(eta z). The ratio a(z)/a(eta z) is input-dependent and need not exist in R[z]/z^M. In particular arbitrary fresh input may have zero or nonunit constant coefficient. The operator relation is instead

    M_D T_eta = M_(P_M) T_eta M_D.

It remains an intertwining statement requiring an application circuit.

## 3. Product factorization and its literal cost

For dyadic r,

    P_(2r)(X,z)=P_r(X,z)P_r(X,X^r z).

Writing T_r f(z)=f(X^r z), multiplication by the second factor is

    T_r M_(P_r) T_r^(-1).

T_r and its inverse are monomial routes in raw (lag,u) coordinates, with known scalar phases. Thus they cost O(N) at the full M-by-M ambient size.

If this factorization is used literally as an application tree, each level doubles the number of independent applications. With A(1)=Theta(N),

    A(2r)=2A(r)+O(N),
    A(M)=Theta(MN).

There are M linear factors, each applying one full-array shifted addition. The shared algebraic description does not mean a logarithmic number of passes. An equivalent recursive implementation with factored routes can remove repeated route work, but still performs the M full-array shifted additions in this literal circuit.

## 4. A shrinking compiled-product recurrence

Instead compile P_r as an R-valued polynomial and multiply at the next doubled degree. Only one P_r is prepared at each level; its second copy is obtained by monomial coefficient routes. R multiplication is twisted cyclic convolution in u. After untwisting X=omega S, multiplication of two degree-r polynomials is a two-dimensional polynomial/cyclic convolution with O(Mr) cells. Retain the top coefficient by using lag length at least 2r+1, for example 4r at a dyadic stage; using 2r would alias that coefficient.

With ordinary exact FFT multiplication,

    C(2r)=C(r)+O(Mr log(Mr)).

The sum over r=1,2,4,...,M/2 is O(M^2 log M)=O(N log N), not M times that bound. The final polynomial has O(N) scalar coefficients. All coefficient generation and kernel transforms are included. Preparing the same kernel in spectral h coordinates via the q-binomial coefficient recurrence also costs O(N) arithmetic after the row Fourier basis is already available; converting its full coefficient table back to raw coordinates costs O(N log M).

This is a genuine shrinking degree-doubling preparation algorithm. It does not yet apply the polynomial to arbitrary raw data.

## 4A. Stronger raw preparation: O(N) via cyclic solves

The preceding compiled-product construction is valid but not optimal for preparation. Both P_M and D admit direct O(N) raw coefficient preparation, an improvement supplied and independently checked in review.

Represent X=omega S on the length-M raw u coordinate, where S f[u]=f[u-1]. The p_s recurrence is

    (I-omega^s S^s)p_s
      = (omega^(s-1)S^(s-1)-eta I)p_(s-1).

For s=1,...,M-1, let d=gcd(s,M) and L=M/d. Each cycle of S^s has length L, and the solve denominator is

    delta_s=1-(omega^s)^L=1-eta^(s/d),

which is nonzero because 0<s/d<M. If a cycle is indexed so that its equations are y_j-c y_(j-1)=b_j, then

    y_0=(b_0+c b_(L-1)+...+c^(L-1)b_1)/(1-c^L),
    y_j=b_j+c y_(j-1),   1<=j<L.

Two cycle passes cost O(L); summing all d cycles costs O(M). For s=M, the left side is simply (1-eta)I, still invertible. Starting with the delta vector p_0=1, all M+1 coefficient rows therefore cost O(M^2)=O(N).

Likewise

    (I-omega^s S^s)k_s
      =omega^(s-1)S^(s-1)k_(s-1)

prepares the entire raw inverse kernel D in O(N). Prepare the root/phase table in O(N), generate all delta_s from it, and batch-invert the M denominators with one scalar inversion and O(M) field operations. The cycle routes, right-hand sides, and every coefficient write are charged. All coefficients of both kernels occupy O(N) words. Integer gcd work over s<=M is O(M log M) word operations and is absorbed by O(N) for M>=2.

These are raw tables, with no input Fourier bank or Fourier conversion assumed. To use them in the application circuit below, their two-dimensional FFTs still cost O(N log N), and every fresh arbitrary input still needs the stated application work. The improvement is linear kernel preparation, not a linear matrix-vector application oracle.

## 5. Explicit application as one two-dimensional convolution

Let M be a power of two. Retain the full degree-M P_M; an input of degree <M gives a product of degree <=2M-1. Thus a lag transform of length L=2M gives exact ordinary convolution without wraparound. The u coordinate has length M and uses the twist X=omega S.

To apply P_M to all raw input coefficients:

1. Embed the raw input in the M-by-2M grid, zero in the upper M lag positions, and apply the known u twist.
2. Compute its two-dimensional FFT (length M in u and length 2M in lag).
3. Multiply pointwise by the fully charged transform of P_M.
4. Invert the two-dimensional FFT, undo the twist, and keep lag coefficients 0,...,M-1 if only the truncated product is wanted.

This circuit uses O(N) words and O(N log M) arithmetic. Both dimensions halve in a standard balanced radix recurrence:

    B(M)=4B(M/2)+Theta(M^2),
    B(M)=Theta(M^2 log M)=Theta(N log N).

The recurrence explicitly counts sharing across all h: the u Fourier bank is part of this two-dimensional transform, rather than M uncharged independent conversions. Sharing the kernel or its transformed values does not remove these input-dependent transforms.

For a straightforward butterfly ledger, exploit input zero padding to do only M active length-M u transforms, then M length-2M lag transforms. One forward bank uses

    (N/2)log_2 M + N log_2(2M)
      = (3N/2)log_2 M+N

radix-2 butterflies. Invert lag first and recover only the requested M u rows to get the same count on the inverse side. Thus these two data-dependent banks alone use

    3N log_2 M+2N

butterflies, before pointwise products, phase handling, or charged kernel preparation. This is a count for this explicit unpruned lag-FFT circuit; it is not a minimum for every possible pruned or output-only circuit.

## 6. Exact near-full support of the compiled multiplier

There is no large support saving in this particular 2D FFT circuit. Let rho=omega^(M/2), of exact order 2M. At spectral channel h and lag-transform node rho^ell, the multiplier is

    P_M(q_h,rho^ell)=product_(j=0)^(M-1)(1+q_h^j rho^ell).

It vanishes exactly when q_h^j belongs to the subgroup of order 2M. Since q_h has order M^2, this means M/2 divides j. Among 0<=j<M there are exactly two such indices, j=0 and j=M/2, and they give distinct ell. Explicitly the zero indices are ell=M and ell=M-1+Mh modulo 2M; the second is M-1 for even h and 2M-1 for odd h.

Consequently exactly two of the 2M multipliers vanish in every h channel. The full M-by-2M multiplier grid has exactly

    2N-2M

nonzero entries. Skipping these zeros saves O(M) pointwise products, not the transform banks. The full circular embedding has 2M zero modes, but the requested truncated degree-<M multiplication is invertible because P_M has constant coefficient 1; the embedding zeros do not imply information loss in that truncated map. This exact support statement applies to the full degree-M product P_M and the specified dyadic padding. If one first discards its top coefficient, the sampled polynomial changes and this zero count need not remain true.

## 7. The remaining useful construction question

The M-step identity successfully moves one set of coefficient denominators to scalars, but its product application is a nontrivial two-dimensional convolution with near-full transformed support. The literal factor tree costs Theta(MN); the explicitly shared application circuit costs Theta(N log N). Raw kernel preparation itself improves to O(N) by the cyclic solves in section 4A.

The next meaningful escape would be a raw-coordinate factorization of M_(P_M) or the full inverse-recovery/output composition that has fewer than logarithmically many O(N)-cost application levels, or a multilevel circuit whose per-level active work genuinely decreases. It must handle arbitrary input without using an input polynomial inverse. Bounded stationary kernel order is already excluded by the shifted Hankel determinant in the preceding report; near-full multiplier support only excludes a sparse-frequency shortcut inside the displayed 2D convolution schedule. Neither excludes genuinely different nonstationary, nonuniform, or output-only circuits.

## 8. A concrete noncommuting power formulation

Let T f(z)=f(Xz), Z multiply by z modulo z^M, and A=(I+Z)T. Then induction using T Z=X Z T gives

    A^r=M_(P_r) T^r,
    M_(P_M)=A^M T_eta^(-1).

Both A and T_eta are explicitly O(N)-applicable raw operators; A is a monomial shear followed by a one-step lag addition. The formula is an actual circuit with M passes. Repeated squaring gives a short description of A^M but not a logarithmic-cost application oracle: at the rth doubling the power is precisely the degree-r product already charged above. This identifies a concrete compression target, namely the Mth power of this specific sparse noncommuting operator, without assuming that its power is cheap.

## Exact controls

`check_m_step.py` imports only the independently authored NTT/field helper in the frozen sibling milestone_1 directory. It checks 620 coefficient recurrences, 98 doubled polynomial products, 680 transformed kernel entries including every claimed zero, and 12 complete raw twisted two-dimensional convolution applications with 2,040 output coefficients. Cases are M=2,4,8,16. All agree with independent direct ring-polynomial multiplication. The explicit invalid-substitution control uses a(z)=z, M=4, p=17, eta=13: y has z coefficient 1 whereas P_M y(eta z) has z coefficient 13.
