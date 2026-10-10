# A linear common-annihilator envelope for Fourier signed banks

10 October 2026. New author note, pending independent review. No accepted file is changed. The all-order result below is a rank bound and an exact sufficient criterion, not an unconditional asymptotic bank upper bound.

## 1. Result and unresolved guard

Let N be odd, q a primitive Nth root, K=Q(q), h=4^(-1) modulo N, and f(a,b)=q^(h(a+b)^2). Keep the accepted signed-bank grammar, beta=1, the same m nodes in ++ and --, and one node 1 in each cross-sign orientation. Assume m≥(N−1)/2 and put d=N−m≥4.

There is an explicitly defined matrix A_(N,m) over K with m+1 columns whose rank satisfies

rank A_(N,m) ≤ min((d−1)(d−2)/2, 4d−11).

A monic polynomial g in its kernel, with degree m, nonzero constant, distinct roots, and the axis rank condition below, gives at most 2m+2 permitted banks over its splitting field. Every physical row is compatible by an explicit interpolation construction.

In particular d=floor((N+11)/5) makes 4d−11≤m and forces a nonzero homogeneous kernel. This is suggestive of an approximately 8N/5 count, but the rank bound does NOT establish that the kernel contains a monic squarefree polynomial with nonzero constant, or that the axis condition holds. Those uniform assertions remain open. A vector with zero leading coefficient is insufficient: its shorter polynomial has additional recurrences that were not imposed. Parameter counting is not used to bypass these issues.

The separately certified orders in Section 6 do satisfy every guard in characteristic zero. They give new bounds M_C(13)≤18, M_C(17)≤24, and M_C(35)≤54. These are individual orders, not an asymptotic theorem.

## 2. The whole-left sequences

Use the accepted Gaussian factors G_(epsilon,delta)(a,b), equal to [r+ell choose ell]_(q^(epsilon delta)) for r+ell≤N−1 and zero otherwise, where r=[epsilon a]_N and ell=[delta b]_N. For 1≤b≤(N−1)/2 define

T_b=1/G_-+(N−b,b),
v_b(j)=(f(j,b)−T_b G_-+(j,b))/G_++(j,b),  1≤j≤N−b−1.

All stated denominators are nonzero. The scalar T_b is forced by the exclusive coordinate a=N−b, where the target equals 1.

For every a,b≥1 with a+b≤d−1, put the row

(v_b(a), v_b(a+1), …, v_b(a+m))

in A_(N,m). These are exactly all length-(m+1) windows of the whole-left sequences. Because d≤(N+1)/2, every b used lies in the positive half of the physical rows. The number of rows is (d−1)(d−2)/2.

If g(t)=Σ_(k=0)^m c_k t^k, c_m=1, then A c=0 is exactly the common recurrence condition for all these sequences. It is stronger than imposing recurrences only on the central interval a=b,…,N−b−1. Central recurrences alone generally do not settle the multiple left-boundary entries that must share a single +− amplitude. Here that amplitude is deliberately set to zero, and the full left interval is interpolated instead.

## 3. Proof of the 4d−11 rank bound

Write e=2^(-1) modulo N and introduce the ordinary polynomial

D(z)=∏_(j=2)^(d−1)(1−q^j z), degree d−2.

For every actual column k=0,…,m, D(q^k)≠0: all exponents j+k lie between 2 and N−1. Therefore multiplying column k of A by D(q^k) preserves rank.

For a row (a,b), write t=a+b≤d−1 and

P_(a,b)(z)=∏_(j=1)^b(1−q^(a+j)z),
R_(a,b)(z)=∏_(j=1)^b(1−q^(a−j)z),
F_(a,b)(z)=D(z)/P_(a,b)(z).

The quotient is a polynomial because the denominator's factors have indices a+1,…,a+b inside 2,…,d−1. Let Q_b=∏_(j=1)^b(1−q^j) and B_b=T_b(−1)^b q^(b(b+1)/2). The Gaussian product formulas give, including their zero-support values,

D(q^k)v_b(a+k)
 = Q_b q^(h t²) q^(h k²) q^(e t k) F_(a,b)(q^k)
   − B_b R_(a,b)(q^k)F_(a,b)(q^k).

For entries outside the support of G_-+, its product numerator contains a factor 1−q^0=0, so the same identity remains valid.

Put C_k=q^(h k²), rho=q^e. If t=2u, then q^(e t k)=(q^k)^u; if t=2u+1, it is rho^k(q^k)^u. Thus every scaled row has the form

C_k E(q^k) + C_k rho^k O(q^k) + R(q^k).

The three polynomial components lie in these spaces:

- E has degree at most E_max=d−3+floor((d−1)/2), is divisible by z, and is also divisible by 1−q^(d−1)z when d is even.
- O has degree at most O_max=d−3+floor((d−2)/2), is divisible by z, and is also divisible by 1−q^(d−1)z when d is odd.
- R has degree at most d−2.

The z factors follow from u≥1. The additional endpoint factor follows because the largest t of the indicated parity is then at most d−2. The total dimension of this direct sum of polynomial spaces is

(E_max−1_(d even)) + (O_max−1_(d odd)) + (d−1) = 4d−10.

There is one additional linear relation. Put k_*=m+1=N−d+1 and z_*=q^(−(d−1)). Every row triple satisfies

C_(k_*) E(z_*) + C_(k_*) rho^(k_*) O(z_*) + R(z_*) = 0.

Indeed, if t<d−1, F_(a,b)(z_*)=0. If t=d−1, the underlying numerator at the formal endpoint a+k_*=N−b is f(N−b,b)−T_b G_-+(N−b,b)=1−1=0. This argument evaluates the polynomial numerator after cancellation; it does not divide by the vanishing Gaussian denominator at that endpoint.

This is a nonzero linear functional on the displayed direct-sum space, since its coefficient on the constant polynomial in the R component is 1. Its kernel has dimension 4d−11. Evaluation on the m+1 actual columns cannot increase dimension. This proves the rank bound for every odd N under the stated range assumptions, including composite N.

## 4. Exact row compatibility and legal nodes

Suppose c is a kernel vector with c_m=1, c_0≠0 and Res(g,g')≠0. Let x_1,…,x_m be its distinct nonzero roots in a splitting field L/K.

For positive b, set the −+ singleton amplitude to T_b and the +− singleton amplitude to zero. Choose ++ amplitudes U_i so that

Σ_i U_i x_i^a = v_b(a),  1≤a≤N−b−1.

If the sequence has length at least m, solve its first m equations at exponents 1,…,m. Their Vandermonde determinant is nonzero, and A c=0 propagates every remaining entry by recurrence. If its length is below m, truncated consecutive-power Vandermonde interpolation directly solves it.

Choose -- amplitudes V_i to realize the following b moments:

Σ_i V_i = f(0,b)−T_b−Σ_i U_i,
Σ_i V_i x_i^r = (f(N−r,b)−T_b G_-+(N−r,b))/G_--(N−r,b), 1≤r≤b−1.

This is possible because b≤m. These -- sectors affect only a=0 and the right interval N−b+1,…,N−1. The ++ assignments handle a=1,…,N−b−1; the forced singleton handles a=N−b; all N coordinates are covered without disturbing another interval. All Gaussian denominators are nonzero on the indicated support.

Reflect simultaneously (a,b) to (−a,−b) and exchange ++ with -- and −+ with +− to assign all negative physical rows. The shared node set makes the reflection an assignment to existing banks, and f is invariant.

For b=0, let p_a be the m-vector of coefficients of t^a modulo g, 0≤a≤N−1. Define the N by (2m+1) axis matrix with a-th row

(p_a, 1, p_[-a]_N).

The remaining guard is that this matrix have rank N. A nonzero N-column minor then specifies an exact axis solve over K. Moment-to-root Vandermonde interpolation gives the actual L-valued sector amplitudes. Each orientation's sector map b to [delta b]_N is bijective, so the row assignments do not conflict across sectors.

Finally put C=(1/N)Σ_t q^(−t²), Delta_n=−alpha_n^N, and

w_(n,j)=C Delta_n Σ_(ell=0)^(N−1) h_(n,ell) q^(−epsilon_n delta_n j ell).

All alpha_n are 1 or nonzero roots of g. Hence every original resolvent is legal. Finite-character orthogonality and

(I−X_j)^(-1)=(I+X_j+…+X_j^(N−1))/Delta_n,
X_j=alpha_n S^epsilon_n+q^(epsilon_n delta_n j)T^delta_n,

give exactly the matched Weyl coefficients and therefore the literal Fourier matrix. Both inverse products follow by telescoping. This counts 2m+2 whole banks and N(2m+2) raw weights. It does not assert scalar arithmetic complexity, a faster FFT, or a minimal unrestricted bank count.

## 5. A characteristic-zero lifting certificate

Finite-field solutions alone are not lifted. Instead, a characteristic-zero polynomial is DEFINED by a selected linear system over K, with certain nonpivot coefficients fixed to the integer residues recorded in the certificate and c_m=1.

Let R be the analytical rank bound in Section 1. If reduction at a prime (p,q−q_0) exhibits rank R and a nonzero R by R minor using only columns 0,…,m−1, choose its rows and coefficient columns. Solve those characteristic-zero equations for those R coefficients; fix all other nonleading coefficients as stated above. The minor is a unit in the local ring, so this solve exists there. The analytical bound proves the entire characteristic-zero matrix has rank exactly R. Its remaining rows are therefore linear combinations of the selected rows, and ALL recurrence equations hold exactly.

The coefficients reduce to the recorded modular polynomial. If its constant, resultant, and selected axis minor are all nonzero, the same guards are nonzero in K. Thus the polynomial defined over K has m distinct nonzero roots, and the full row construction of Section 4 is valid in characteristic zero. This method needs no assumption that an arbitrary finite-field solution lifts, and no assumption that a nonempty coefficient open set has a K-split point.

## 6. Three new exact examples

The files N13_LIFT_CERTIFICATE.json, N17_LIFT_CERTIFICATE.json and N35_LIFT_CERTIFICATE.json specify the selected equations, coefficient columns, fixed integer coefficients, all modular rows, and modular controls. They are complete finite recipes for polynomials over K, rather than numerical algebraic approximations.

- N=13, m=8, d=5: 18 banks; prime p=53, q_0=16. R=6. The defining minor, constant, resultant and axis minor residues are respectively 13, 14, 32, 49.
- N=17, m=11, d=6: 24 banks; p=103, q_0=72. R=10. The four residues are 35, 9, 7, 3.
- N=35, m=26, d=9: 54 banks; p=71, q_0=49. R=25. The four residues are 29, 37, 39, 69.

Each q_0 has exact order N. The first two recurrence systems have full row rank, so their exact compatibility does not need the refined rank envelope. The order-35 system has 28 rows and rank 25: the 4d−11 bound is essential to certify its characteristic-zero dependencies from its nonzero 25-minor.

All m nodes occur as actual individual roots and are counted separately in both same-sign orientations. Each splitting field has degree at most m! over K. No K-only attainment is claimed. The raw branch counts are 234, 408 and 1890, respectively.

Fresh controls also solve and verify every physical coefficient row modulo its indicated prime. These are supplementary checks of the direct characteristic-zero proof, not substitutes for it. No predecessor research program was executed or imported.

## 7. Stronger order-eleven obstruction in a restricted architecture

N11_FULL_QUINTIC_OBSTRUCTION.json records six central-window rows at (23,q−2): four length-six windows from b=1 and two from b=2. Their 6 by 6 determinant is 4 modulo 23. All defining Gaussian denominators are units. Thus the characteristic-zero matrix is invertible.

Whenever the −+ orientation consists of exactly one effective node alpha=1, the exclusive coordinates force its amplitudes T_1 and T_2. The central intervals of rows b=1,2 then involve only that singleton and the ++ group. If the ++ group had at most five effective nodes, their product annihilator, padded to degree five if necessary, would give a nonzero vector in the displayed kernel. This is impossible. The argument does not assume a depressed polynomial, common ++/-- nodes, or any bound on the number of -- nodes. It also works over every characteristic-zero extension of K.

Reflection forces at least six -- nodes when the +− orientation likewise has exactly one node alpha=1. Therefore within the architecture with one cross-sign singleton at alpha=1 in each orientation, at least 14 banks are necessary. The accepted order-eleven 14-bank construction attains this restricted optimum over its splitting field. This does not establish the unrestricted minimum at N=11, and it says nothing new about whether 14 banks can be attained entirely over K.

## 8. Boundary of what has been proved

The all-order contribution is the rank envelope and the sufficient exact-guard criterion. The concrete new upper bounds are only the three separately certified orders above. A uniform 8N/5 theorem requires proving monicity, absence of unavoidable repeated/zero roots, and a nonzero axis minor throughout an infinite family. Neither the rank bound nor the experimental files prove those facts.

The moment/annihilator and Vandermonde ingredients are classical. The bound derived here concerns the particular Fourier whole-left sequences and their coupled signed-bank realization. No historical priority claim is made. Accepted base-field, smaller-field, and small-order witness files were read as inert mathematical source material and remain unchanged.
