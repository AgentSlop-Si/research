# F020: low-order cyclotomic deflation beyond the ramified bound

16 October 2026 UTC. Author-proved bounded refinement, pending independent review. No repository or research-table writes were made. No supplied research program was executed.

## Result and exact boundary

The accepted q=1 deflation can be strengthened by removing a uniform product of low-order cyclotomic factors forced by the actual Rogers–Szegő coefficients. For every odd d with 3 <= d <= m, put

    k_d = floor(m/d),
    rho_d = ((d-1)/2) k_d + floor(k_d/2),
    e_d = ((d+1)/2) k_d + floor(k_d/2).

Over F2[q], with Phi_bar_d the reduction of the integral cyclotomic polynomial,

    Phi_bar_d^k_d divides E_m,
    Phi_bar_d^rho_d divides R_m,
    M_m := product_(3<=d<=m, d odd) Phi_bar_d^e_d divides Q_m.

The endpoint bound is exact when d divides m, at every irreducible component of Phi_bar_d. The resultant bound is a lower bound, not an exact formula.

Let N=m(m+1)(2m+1)/3, v=ceil(m/2), and retain the accepted

    kappa = m + 3 floor(m^2/4) + 2 floor(m/4).

Define

    Delta_m = sum_(3<=d<=m, d odd) phi(d) e_d,
    C_m = N-v-kappa-Delta_m.

Then the actual polynomial

    F_m = Q_m / (q^v (q+1)^kappa M_m)

is nonzero, monic, and has degree C_m. For every odd D>2m+1,

    phi(D)>C_m  implies  Phi_bar_D does not divide Q_m.

Combined with the previously accepted characteristic-zero discriminant implication, this proves ordinary residual squarefreeness at the orders selected by this stronger filter. It does not prove the all-order result, the four-channel paired-support theorem, or overlap simplicity. F020 remains OPEN / TO RESEARCH, priority 58; its separate endpoint gate remains 53. No status, score, or open/closed count change is justified.

This is a bounded all-m coefficient result, not another fixed-m support census. No historical novelty or publication-priority claim is made.

## 1. Actual-family definitions and read sources

Throughout,

    P_0=1, P_1=X+q+q^2,
    P_j=(X+q^(2j-1)(1+q))P_(j-1)
         +(1+q^(2j-1))(1+q^(2j-2))P_(j-2), j>=2,
    P_m(X;q)=A_old(X^2;q)+X B_old(X^2;q),
    E_m=P_m(0;q), R_m=Res(A_old,B_old), Q_m=E_m R_m.

The actual Gaussian polynomial satisfies

    H_(2m+1)(z;q)=(z+1)z^m P_m(z+z^-1;q).

The accepted nonzero degree theorem is deg Q_m=N, and the actual reversal is Q_m*=q^N Q_m(q^-1). No padded reversal is used.

The accepted endpoint identity is

    E_j=D_j+(1+q^(2j))E_(j-1),
    D_j=product_(a=1)^j(1+q^(2a-1)), E_0=1.

The previously published deflation report was freshly fetched at the parent's pinned commit and read directly:

- [Accepted ramified deflation](https://github.com/AgentSlop-Si/research/blob/0339a31eb6109f0b96074ab8321f8653641e7530/math/finalized/2026-10-16-mathematical-development-1221/f020/REPORT.md).

The local source-bound complementary and endpoint-transport reports were also read for the above definitions and endpoint identity. Their full SHA-256 values are recorded in SOURCE_BINDINGS.json. A local source hash is not represented as a fresh remote byte-identity claim.

## 2. Endpoint divisibility at every odd low order

Fix an irreducible f dividing Phi_bar_d, d odd >=3. Its root has exact order d. Every odd exponent u satisfies

    v_f(1+q^u)=1 if d divides u, and 0 otherwise.

Indeed an odd power polynomial has nonzero derivative at its nonzero roots. Therefore

    v_f(D_j)=floor((2j+d-1)/(2d)) >= floor(j/d).

We prove v_f(E_j)>=floor(j/d) by induction. If d does not divide j, the desired floor is unchanged from j-1, so both terms of the endpoint recurrence have at least that valuation. If j=kd, then v_f(D_j)=k, while

    v_f(1+q^(2j))=2^(1+v_2(k)) >=2.

The second term has valuation at least (k-1)+2=k+1. Thus at this boundary there is no cancellation with the first term and v_f(E_(kd))=k exactly. This proves the bound and its stated exact boundary for every irreducible component f. Since Phi_bar_d is squarefree, Phi_bar_d^floor(m/d) divides E_m.

The argument is entirely in F2[q]. In particular it never confuses multiplicity of a spectral root X with multiplicity in the parameter q.

## 3. Static specialization and a forced square divisor

Fix alpha of exact odd order d=2h+1. Write

    2m+1=A d+r, 0<=r<d, k=floor(A/2)=floor(m/d).

The Gaussian specialization is

    H_(Ad+r)(z;alpha)=(1+z^d)^A H_r(z;alpha).            (3.1)

For completeness, this follows from the finite q-binomial product, grouped into A complete d-blocks and one r-block. Each complete block specializes to 1+t^d. Comparing coefficients gives the q-Lucas relation. The phase q^[j(j-1)/2] in the finite product causes no extra factor: after writing j=ld+s, its phase differs from s(s-1)/2 by a multiple of d, because d is odd. In characteristic two there is no sign discrepancy. Summing the coefficient identity gives (3.1); composite d is allowed.

Define the fixed monic polynomial CYC_d(X) by

    (1+z^d)/(1+z)=z^h CYC_d(z+z^-1).

It has degree h, constant coefficient 1, and simple roots alpha^j+alpha^-j, 1<=j<=h. Distinctness follows from u+u^-1=v+v^-1 only when u=v or uv=1. This statement concerns all nontrivial dth roots, and does not require d prime.

If A=2k, then r is odd, and (3.1) gives exactly

    P_m(X;alpha)=X^k CYC_d(X)^(2k) P_((r-1)/2)(X;alpha).

If A=2k+1, then r is even. Reciprocity gives a monic polynomial V_r of degree r/2 with H_r(z;alpha)=z^(r/2)V_r(z+z^-1). In this case

    P_m(X;alpha)=X^k CYC_d(X)^(2k+1) V_r(X;alpha).

These identities use (z+1)^2=z(z+z^-1), and include r=0 or r=1 using V_0=P_0=1. In either case the square

    [X^floor(k/2) CYC_d(X)^k]^2

is a polynomial divisor of P_m(X;alpha).

All coefficients of CYC_d lie in F2. Therefore the specialized spectral split A_old(Y;alpha), B_old(Y;alpha) has the common monic divisor

    Y^floor(k/2) CYC_d(Y)^k,

of degree rho_d=h k+floor(k/2). This conclusion is about both coefficients of the unique even/odd split, not about a norm or a single endpoint branch.

## 4. Lifting spectral corank to parameter multiplicity

Let S(q) be the Sylvester matrix of the generic spectral split. One split polynomial is monic of its full degree: A_old when m is even, B_old when m is odd. Thus after reduction modulo an irreducible f|Phi_bar_d, the corank of S is the degree of the specialized common gcd, including a zero other polynomial. It is at least rho_d by Section 3.

Here is also a formulation that avoids any implicit specialized-degree convention. A common monic divisor G of degree rho supplies rho independent kernel vectors in the Sylvester map: multiply the divided coefficient pair by 1,Y,...,Y^(rho-1). The full-degree monic member ensures these vectors satisfy the generic degree bounds and are independent. When the other member is zero, the kernel has at least the monic member's degree, which is again enough.

For a square matrix over the local DVR F2[q]_(f), corank at least rho modulo f forces its determinant to be divisible by f^rho. Lift invertible residue-field row and column operations to invertible matrices over the DVR; after these operations, at least rho rows have all their entries in (f). Expanding the determinant gives the claimed valuation. Hence

    v_f(R_m)=v_f(det S)>=rho_d.

Apply this independently to every f|Phi_bar_d. Its squarefreeness then gives Phi_bar_d^rho_d|R_m. This is the required bridge from spectral specialization multiplicity to parameter multiplicity; specialization alone would not justify a higher valuation.

Together with Section 2 this proves Phi_bar_d^e_d|Q_m. The distinct odd-order cyclotomic polynomials are pairwise coprime modulo two because their roots have distinct exact odd orders. They are also coprime to q(q+1). Thus all the proved factors multiply, proving the exact integral quotient F_m in the opening statement.

## 5. Stronger filter and the still-missing lemma

Every factor removed in M_m has order at most m; q+1 has order one, and q has no nonzero root. Consequently Phi_bar_D is coprime to the entire removed divisor whenever D>2m+1. For such odd D,

    Phi_bar_D|Q_m iff Phi_bar_D|F_m.

Since Phi_bar_D is squarefree of degree phi(D), phi(D)>C_m excludes divisibility. This tests all primitive components at once, rather than confusing a single primitive factor with the whole cyclotomic polynomial.

The refinement is strict as a numerical sufficient condition. At the already studied control m=3, the accepted bound is 17 and this bound is 13, so D=17, phi(D)=16 now passes the inequality. This is not claimed to be a newly solved finite family or previously unknown m=3 result. At m=12 the obstruction degree decreases from 1168 to 1006. Neither example justifies a new support-census stage.

The remaining full-cyclotomic component-selection lemma is now precisely

    Phi_bar_D does not divide F_m
    for every m>=1 and every odd D>2m+1 with phi(D)<=C_m.       (5.1)

For each fixed m, these candidate D are finite: phi(D)^2>=D for odd D, since each prime-power contribution p^(a-2)(p-1)^2 is at least one for p>=3. Hence (5.1) only has candidates D<=C_m^2. This arithmetic finiteness does not establish the all-m quantifier and is not a proposal to launch a growing census.

Even (5.1) would prove only the sufficient modular all-components criterion for characteristic-zero ordinary residual squarefreeness. The owner's stronger four-channel gate still requires

    (Q_m,Q_m*)=(1) in F2[q,1/L_(2m+1)]

for all m, or a certified actual-family high-order reciprocal common factor. Removing M_m is harmless for that localized question because its factors already divide the support of L_(2m+1), but it does not supply the missing Bezout certificate. The residual problem still includes distinct inverse Frobenius components, self-reciprocal components, endpoint/collision mixtures, and collisions at different spectral coordinates. General overlap simplicity remains separate.

Accordingly the present bounded lemma is complete at author-proof level; the broad mathematical task is not finalized. No all-m support theorem, counterexample, historical-priority assessment, or FFT consequence is asserted.

## 6. Reproducible author checks and controls

Run `python check_low_order.py` in this packet. The self-authored program uses only the Python standard library and imports no supplied research programs. It implements bit-polynomial F2[q] arithmetic, Gaussian q-Pascal reconstruction, reciprocal trace folding, the independent three-term trace recurrence, and a fraction-free Sylvester determinant.

At the previously studied controls m=1,2,3,4,12, it checks the recurrence against Gaussian reconstruction, actual degree/q-content, all newly forced low-order factors, the precise spectral divisor, every endpoint exact boundary present, and the full combined quotient degree. It checks the strict inequality example above and rejects an extra endpoint factor at its sharp boundaries. There is no irreducible-factor support census or new growing m grid.

The recorded author run passed 46 assertions. Source bindings and output are separate files. These checks do not replace the uniform proofs or independent review.
