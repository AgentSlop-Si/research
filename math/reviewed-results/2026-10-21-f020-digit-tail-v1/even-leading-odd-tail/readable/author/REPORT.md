# Every even leading digit with every odd short tail

Author candidate, 21 October 2026 UTC. This is a uniform proof in the original F020 normalization, subject to independent review. It neither accepts itself nor claims arbitrary-degree/global F020 closure, an FFT improvement, or historical novelty.

## 1. Statement, inherited work, and complete root partition

Let p be an odd prime, 2<=c<p even, d=2m+1 with 1<=d<p odd, r>=2, s>r, N=p^r, and n=cN+d. Let q be any characteristic-zero primitive p^s-th root. Keep exactly

    P_0=1, P_1=X, P_(j+1)=X P_j-(1-q^j)P_(j-1),
    H_j(z)=sum_k [j choose k]_q z^k,
    w_j=product_(u=1)^j(1-q^u), w_0=1.

Choose an algebraic p-adic embedding, put t=q-1, v(t)=1, and define

    e=v(p)=(p-1)p^(s-1), B=r(p-1)p^(r-1)/2,
    K=cN/2+cB, E=(c-1)N/2+cB, D=(c+1)N/2+cB-p,
    h=floor(r/2), beta=p^h, L=N/beta,
    rho=beta/2 if r even, rho=p^(h-1)(2p-1)/2 if r odd,
    C=(2m+1)!!, Btail=(2m)!!, alpha=Btail/C.

Empty double factorials are 1, so at d=1, C=Btail=alpha=1. All factors of C and Btail are less than p; alpha is a p-adic unit. Define

    M_j(Z)=j! sum_(k=0)^floor(j/2) Z^(j-2k)/(2^k k!(j-2k)!),
    R_c(U)=sum_(k=0)^(c/2) c! U^(c/2-k)/(2^k k!(c-2k)!).

Thus M_c(Z)=R_c(Z^2). THEOREM: for all the parameters above, the original P_n and H_n are squarefree, and the original algebraic-square Christoffel-Darboux kernel is nonzero at every P_n root.

The previously accepted general-c d=1 family and c=2 all-odd-tail family are inherited, not newly credited. The added range relative to those sources is c>=4 and odd d>=3, with p>=5. The even-tail theorem is only a transfer-convention comparison, not authority for any odd-tail inference. The proof below establishes the full p>=5 statement directly from accepted coefficientwise inputs and explicit new arbitrary-alpha lifting. At p=3 necessarily c=2,d=1: r>=3 is inherited, and r=2 uses the accepted original P_19 result with central derivative value 76/3. The new first/second correction argument does NOT apply at p=3.

All roots, including multiplicity before simplicity is proved, are:

* One exact zero, with v(P_n'(0))=K+m.
* Exactly d-1 low roots, all with v(X)=1/2. If tau^2=t and X=tau Z, their nonzero residuals are precisely the nonzero roots of M_d, and

      v(P_n')=(n-1)/2=cN/2+m,
      P_n'/tau^(n-1) -> d Z^(cN) M_(d-1)(Z) !=0.

* In each of the beta disjoint disks v(X-x_a)>=rho, where

      x_a=i(q^(a/2)-q^(-a/2)), 0<=a<beta, i^2=-1,

  with square roots congruent to 1, exactly cL high roots lie on the boundary. Their X-values are rho centrally and p^ord_p(a) for a!=0. At r>=3, or at any noncentral high root,

      v(P_n')=m+x+min(D,N+E-2x), x=v(X).

For the remaining r=2 central roots, put delta=p(p-1)/2, X=mu Y, mu^2=t^p, U=Y^2. The residual equation is R_c(U)^p=0, all U are nonzero. When Ubar != -alphabar,

    v(P_n')=K+delta+m.

Cancellation occurs EXACTLY when

    R_c(-alpha)=0 mod p.                                  (1.1)

If (1.1) holds, there are exactly 2p affected X roots, counted with multiplicity until the derivative proof. At EVERY affected root, for p>=5,

    p does not divide 2d+1:
        v(U+alpha)>1,
        v(P_n')=K+delta+m+1;
    p divides 2d+1 (necessarily p=2d+1>=7):
        v(U+alpha)>2,
        v(P_n')=K+delta+m+2.                              (1.2)

No exact deeper depth is asserted. If chi(alpha)=alphabar^((p-1)/2) in F_p, the affected normalized original P derivative units are respectively

    -Btail chi(alpha) R_c'(-alpha)(2d+1)/12,
     Btail chi(alpha) R_c'(-alpha)/160.                    (1.3)

They are nonzero in the corresponding cases. For p=5 only the first line can occur; the second denominator is used only for p>=7. At d=1 these recover -R_c'(-1)/4; at c=2 and its simultaneous obstruction they recover C/160, consistently with the accepted sources.

The precise leading obstruction has an integer form

    O_(c,m)=C^(c/2) R_c(-Btail/C) in Z,
    Res(R_c,U+alpha)=(-1)^(c/2) R_c(-alpha).

Since p does not divide C, (1.1) is equivalent to p dividing O_(c,m). This is a non-tautological coefficient criterion, not an unknown lifted derivative. Sections 6-9 resolve all of its possible roots; it leaves no exceptional parameter in this sector.

The scope includes c=p-1 and the largest allowed odd d=p-2, independently and simultaneously. It excludes p=2, odd c, c>=p, d>=p, r=1, s<=r, composite orders, arbitrary/intermediate digit strings, global F020/F023 closure, FFT/cost claims, and historical novelty. No external write is made.

## 2. Exact coefficientwise authority and all derivative pivots

Set A=P_(cN), M=P_(cN-1), a=1-q^(cN). The accepted general-c adjacent-criterion author's Sections 2-5 and 7, with its exact accepting review, provide unconditional OFF-ROOT coefficientwise facts. Its criterion for the DIFFERENT degree cN+1 is not a hypothesis. On every full high disk, with scaled coordinate Y and coefficientwise Gauss weight wt,

    wt(A)=K, in(A)=nonzero scalar * M_c(Zbar),
    wt(M)=E, in(M)=nonzero scalar * c M_(c-1)(Zbar),
    wt(A')=D, in(A')=nonzero scalar * c M_(c-1)(Zbar),
    wt(M')>=E, Zbar=alpha_a Y^L, alpha_a!=0.               (2.1)

The A initial has degree cL and nonzero constant. All coefficients above cL have higher normalized weight. Primes always mean the original ordinary characteristic-zero derivative, not differentiation of an inseparable residual.

For clarity, all original derivative pivots, including boundary ones, are retained. Write

    a_j=1-q^j, Q_b=product_(j=1)^b(1-q^(2j)),
    N_b(z)=product_(j=0)^(b-1)(z+q^j), W(b)=sum_(j=1)^b p^ord_p(j).

The exact identities are

    H_b=sum_(k=b mod 2) w_b N_k/[w_k Q_((b-k)/2)],
    H_b'=sum_(k=b mod 2,k>=1)sum_(0<=u<k)
        w_b z^(k-u-1)N_u/[Q_((b-k)/2)w_u a_(k-u)].        (2.2)

Let omega^2=w_N, Ahalf=(N-1)/2, A0=(N-p^2)/2. The A Newton pivots have k=jN, j even, 0<=j<=c, and sum to M_c. The ordinary derivative pivots are ALL

    u=lN, k=lN+p^2, l=1,3,...,c-1.

After normalization by [w_N/(Q_A0 a_(p^2))]omega^(c-1), their sum is cM_(c-1), with value D. At c=4 BOTH l=1 and l=3 terms are necessary; at r=2 the final pair reaches k=cN. In general there are c/2 pivots. The M Newton pivots are k=lN for those same odd l, with normalization omega^(c+1)/(a Q_Ahalf), and sum cM_(c-1).

The complete M' lower bound uses every term of (2.2), not only those pivots: reflection and the cap give a subtracted score at most E+[p^ord_p(j)-W(j)/2]. Only j=1,p can exceed E, by 1/2. If u is not a multiple of N the cap is strict. If u=lN, parity forces l even, and the N-level carry in 2v=cN-1-u-j makes the inequality strict. Half-integrality proves wt(M')>=E. The H/P coordinate conversion retains the prefactor derivative; for A its value is at least re+K>D. These are the audited coefficientwise statements used here.

The integer recurrences

    M_j=Z M_(j-1)+(j-1)M_(j-2), M_j'=j M_(j-1)

show that M_c and M_(c-1) are coprime mod p, by propagation to M_0=1. More exactly Res(M_c,M_(c-1))=product_(j=1)^(c-1)j^j. Thus R_c is separable with nonzero constant. On the ENTIRE residual locus M_c(Zbar)=0, including roots of new tails, (2.1) gives exactly v(M)=E and v(A')=D.

For r=2 the accepted actual normalizations, with epsilon=(-1)^((p-1)/2), are

    A(mu Y)/t^K -> M_c(Y^p)=R_c(Y^2)^p,
    M(mu Y)/[t^(cB)mu^((c-1)p)] -> epsilon M_(c-1)(Y^p),
    A'(mu Y)/[t^((c+1)B)mu^((c-1)p)] -> -c epsilon M_(c-1)(Y^p),
    a/t^N -> -c.                                         (2.3)

These are general-c units. The factor c in the M Newton sum is cancelled by the factor c in its scalar denominator a; it must not be inserted again in the second line.

## 3. Exact odd tail, ordinary derivative witness, and high-root counts

Put b_j=1-q^(cN+j), j>=1. Define

    f_0=1, f_1=X, g_0=0, g_1=1,
    f_(j+1)=X f_j-b_j f_(j-1),
    g_(j+1)=X g_j-b_j g_(j-1).

The original recurrence gives P_(cN+j)=f_j A-a g_j M. For d=2m+1, put

    T=f_d/X, V=g_d, G=M/X, F=P_n/X,
    F=T A-a V G=T J, J=A-a kappa G, kappa=V/T.           (3.1)

T,V,G are even polynomials. The matching formulas are

    T=sum_(S nonadjacent subset {1,...,2m})
         (-1)^|S| X^(2m-2|S|) product_(j in S)b_j,
    V=sum_(S nonadjacent subset {2,...,2m})
         (-1)^|S| X^(2m-2|S|) product_(j in S)b_j.        (3.2)

The V edge start is b_2, not b_1. Since b_j/t -> -j, and d<p, T/t^m and V/t^m have constant initials C and Btail on every high disk. All other terms contain a positive power of Wshort=X^2/t, of value at least 1. Their coefficients are integral in Wshort. Thus T/t^m is an analytic unit on each full high disk, kappa is analytic there, and at x=wt(X)>=1,

    wt(T)=wt(V)=m, kappa -> alpha,
    wt(kappa')>=x-1.                                    (3.3)

The last inequality is ordinary differentiation in X of the integral rational function of X^2/t, whose denominator is an analytic unit. All integer derivative factors remain before reduction.

The perturbation a V G has weight at least N+E+m-x, while T A has weight K+m. The difference N/2-x is strictly positive since x<=rho<N/2. Therefore each high disk has the unchanged residual C times that of A. Newton/Weierstrass counting gives exactly cL boundary roots of F, counted with multiplicity. The beta disks are disjoint, and give cN roots. This does not use simple-root Hensel lifting on M_c(alpha_a Y^L). The central normalized constant is a unit, so F(0) has value K+m and P_n has a simple exact zero.

Differentiate the whole J in characteristic zero:

    J'=A'-a kappa M'/X+a kappa M/X^2-a kappa' M/X,
    Qstar=X^2 A'/(aM)+kappa-kappa X M'/M-X kappa',
    J'=(aM/X^2)Qstar.                                    (3.4)

Every displayed division is legal at a high root: X!=0, M has exact value E, and T is a proved unit after scaling. Alternatively the fraction-free witness

    S=T F'-T'F=T^2 A'-a(V'T-VT')G-aVT G'

is an exact polynomial identity. At a high root,

    P_n'=X F'=X T J',                                    (3.5)

because F=TJ=0. No whole-disk derivative bound is assigned to F from that rootwise identity.

The four terms of J' have respective values or lower bounds

    D exactly, N+E-x, N+E-2x exactly, N+E-1.

If 2x!=p, the first and third have unequal values, and the other two are strictly larger than their minimum. Noncentral x is an integer power of odd p, so cannot satisfy 2x=p. Centrally x=rho equals p/2 only for r=2, and is greater than p/2 for r>=3. This proves every r>=3 and every noncentral high-root value in Section 1.

At r=2, (2.3) and (3.4) show that the initial of Qstar is U+alpha. The two remaining terms have positive relative weights at least rho and p-1. Since R_c is separable and alpha!=0, cancellation is exactly (1.1), and if it occurs precisely two nonzero Y residuals satisfy Y^2=-alpha, each with p lifted roots counted with multiplicity. This proves the exact obstruction and the count 2p before any lift.

## 4. Uniform central gaps, without discarding any competitor

Now r=2, N=p^2, B=N-p, delta=B/2, rho=p/2, g=(p-1)/2. On the central boundary the exact Newton-product weight is

    Tcap(j)=j+(rho-1)ceil(j/p), Delta(j)=Tcap(j)-W(j)/2.

For j=lN+ap+b, 0<=a,b<p,

    2 Delta(j)=a(p-1)+b+(p-2)1_(b>0).                    (4.1)

Thus Delta is zero only at multiples of N, otherwise at least g. The accepted general-c central proof obtains, term by term from (2.2):

* Every nonpivot of H_(cN-1) has value >=E+g.
* Every nonpivot of H_(cN)' has value >=D+g.
* Every nonpivot of H_(cN) has value >=K+delta+g.

For the derivative, the full excess bound is p+W(j-1)/2-p^ord_p(j)+Delta(u), where j=k-u. Divisibility zero gives at least p-1, divisibility one gives at least g, and divisibility two only attains zero at j=N and u=lN, l odd. Higher divisibility is impossible because j<=cN<p^3. The N-level carry supplies the additional delta in the nonpivot even-polynomial estimate. These bounds are uniform at c=p-1. They concern all competing terms, not one selected pivot.

The central first-order lift will use g>1 for p>=5; the second-order lift uses g>2 for p>=7. The sharp p=3 failure g=1 is retained, not hidden. The full M' bound remains wt(M')>=E from Section 2.

## 5. New arbitrary-alpha scalar lifting lemma

This is the step that must NOT be inferred merely from the accepted U=-1 case. Let alpha be the actual rational Btail/C, and suppose R_c(-alpha)=0 mod p. We prove

    v(A(X))>K+p at X^2=-alpha t^p, p>=5,
    v(A(X))>K+2p at X^2=-alpha t^p, p>=7.                (5.1)

First work in characteristic p with alphabar in F_p^*, q=1+t, and z=v0^2, X=v0+v0^(-1), v0 near i. Put S=z+1=v0 X; then S^2=zX^2=-alpha z t^p. Define

    R0=product_(j=1)^(p-1)(q^j-1),
    D0=product_(1<=j<2p, j odd, j!=p)(1-q^j),
    C0=w_(2N)/Q_N=product_(j=1)^N(1-q^(2j-1)).

Both residue index sets are F_p^*. For p>=5, expansion of each edge through its third term gives

    R0/t^(p-1)=D0/t^(p-1)=-(1+t/2-t^2/12)+O(t^3).       (5.2)

Indeed the normalized first and second coefficients are (j-1)/2 and (j-1)(j-2)/6; their sums over F_p^* are 1/2 and -1/3, and the sum of squared first coefficients is -1/4. The second product coefficient is -1/3+((1/2)^2+1/4)/2=-1/12. Wilson gives -1. The first-order version only needs equality through t.

The exact characteristic-p product

    product_(a=0)^(p-1)(Z+C(1+h)^a)-(Z+C)^p

is divisible by h^(p-1). Intermediate Gaussian-binomial coefficients have h-order p-1; the extreme correction has order >=p. Grouping N_N by j=b+pa, using h=t^p, therefore gives

    N_N=N_p^p(1+error of value >=p(p-2)/2).              (5.3)

This remains valid at the present scalar points, since v(S)=rho independently of the nonzero alpha. For the zero-residue group the absolute error is >=p(p-1) while its main product has value p*rho; for other groups the relative gap is at least p(p-2). Grouping C0's odd indices gives

    C0=-t^N D0^(2p)(1+error of value >=p(p-2)).          (5.4)

The p-divisible group is exactly [(1-q^p)D0]^p. Write N_p=S R, R=product_(j=1)^(p-1)(z+q^j). Then v(R/R0-1)>=rho-1 and v(z+1)=rho. Consequently

    N_N^2/C0
       = alpha z^p (R/D0)^(2p)+error
       = -alpha+error of value >p for p>=5,
       = -alpha+error of value >2p for p>=7.             (5.5)

Here alpha^p=alpha in characteristic p is essential. For the first line use equality through t in (5.2), rho-1>1, and p(p-2)/2>p. For the second use equality through t^2, rho-1>2, and p(p-2)/2>2p, valid for p>=7. The nonzero value of alpha changes no estimate. This is the explicit extension from -1 to arbitrary -alpha.

All general-c leading pivots can now be summed without losing their relative errors. Uniform block comparisons give

    w_(hN)=h! w_N^h(1+error >=B),
    Q_(uN)=u! Q_N^u(1+error >=B),
    N_(jN)=N_N^j(1+error >=N-rho),

in the ranges h,j<=c and u<=c/2 actually used. These follow because a shift by N changes an internal edge by value N whereas its original value is <=p; endpoint multipliers are units since c<p. For j even and u=(c-j)/2, the k=jN Newton pivot is

    c! C0^u N_N^j/[j! 2^u u!]+error of value >K+bp,

where b=1 for p>=5 and b=2 for p>=7. The bounds B, N-rho, and delta+g all exceed bp in the corresponding ranges. Summing every pivot and every nonpivot yields

    H_(cN)(z)=C0^(c/2) R_c(N_N^2/C0)+error >K+bp.        (5.6)

Since R_c(-alpha)=0 in F_p, (5.5) proves value >K+bp. The H/P prefactor is a unit, so this proves (5.1) formally in characteristic p.

To transfer the ORIGINAL integer polynomial, evaluate A at X^2=-alpha t^p with alpha=Btail/C in Z_(p). A coefficient of X^(2l) is a sum of products of cN/2-l recurrence edges. Every raw t monomial therefore has degree at least

    cN/2+(p-1)l >= cN/2.

Multiplication by a power of the p-unit C clears all denominators without changing valuations. The characteristic-p result says every coefficient through degree K+bp is divisible by p. Each such coefficient has actual valuation at least e+cN/2, and

    e+cN/2-K >= (p-c)B >= B > bp.                       (5.7)

The inequalities hold at minimal s=3 and at c=p-1; larger s only improves them. All other coefficients have raw degree >K+bp. Thus (5.1) holds in the original mixed-characteristic field at every primitive phase. No unsupported assertion e>K+bp is used.

## 6. Feedback to ALL affected roots, on J rather than F

On the full central disk write J(mu Y)=t^K j(U). The analytic function j is integral and restricted: A/t^K is integral, a kappa G/t^K has weight at least delta, and T/t^m is a unit. Its residual is R_c(U)^p.

The original ordinary J' has coefficientwise weight >=D. A' has that bound. For G=M/X, ordinary division/differentiation gives wt(G')>=E-2rho; hence wt(a kappa G')>=N+E-p=D. The remaining term a kappa'G has weight >=N+E-1>D. Therefore the exact chain rule gives

    J'(mu Y)=2t^K mu^(-1)Y j_U(U), wt(j_U)>=delta.       (6.1)

Division by Y is legal coefficientwise because J is even. This strong bound is on J_U, NOT on F_U: F=TJ has an additional T_U J term off its roots.

At U=-alpha, (5.1) and delta>bp show v(j(-alpha))>bp, with b=1 for p>=5 and b=2 for p>=7. Translate j(-alpha+V)=sum h_l V^l. Since R_c is separable and R_c(-alpha)=0 mod p, h_p is a unit and h_l reduces to zero for l<p. Integrality and (6.1) give v(h_l)>=delta>bp for 1<=l<p. The constant has value >bp. If an affected root had 0<v(V)<=b, h_p V^p would be uniquely lowest: below the constant, below all l<p terms, and below all l>p terms by integrality. This is impossible. Thus EVERY affected root satisfies v(U+alpha)>b, with no simplicity assumption and all 2p roots retained.

## 7. The full general-c ordinary derivative ratio through order two

Pair each ordinary derivative pivot indexed by odd l with the matching M pivot. At r=2 their exact H-side ratio is

    a z^(N-1) Q_(uN+Ahalf)/[Q_(uN) a_N], u=(c-1-l)/2.

For every such u, Q_(uN+Ahalf)/Q_(uN)=Q_Ahalf(1+error >=B), because each shifted factor has relative error >=N-p=B. Hence summing ALL pivots still gives a single scalar ratio. The nonpivot gaps g from Section 4 and v(M)=E on the affected residual locus justify division by M after summing. The original H/P ordinary derivative conversion, including its prefactor term, yields

    X^2 A'/(aM)
      = X^2 [2z^N/(z-1)] Q_Ahalf/a_N + error >=g.        (7.1)

The prefactor term is higher by at least 2e+K-D, larger than two. On the central locus, 2z^N/(z-1)=1+error >=rho. Also a_N/(-t^N)=1+error >2, since discarded integer binomial terms have relative value >=e+1-N>2.

Let a0=(p-1)/2, Ahalf=pa0+a0. In Q_Ahalf the p-divisible indices contribute no normalized positive characteristic-p coefficient below t^p. For the others the normalized first and second coefficients are

    u_j=(2j-1)/2, v_j=(2j-1)(2j-2)/6.

The unit-index multiset is a0 complete nonzero residue blocks followed by 1,...,a0. The sums are

    sum u_j=-1/8, sum v_j=1/8, sum u_j^2=1/8.

Thus the product's second coefficient is 1/8+((1/64)-(1/8))/2=9/128. Wilson gives leading unit -1. Discarded mixed-characteristic terms have relative value at least e for unit edges or e+1-p for p-divisible edges, both >2. Consequently

    Q_Ahalf/(-t^B)=1-t/8+9t^2/128+error >2.              (7.2)

For p>=7, g>2 and rho>2, so on the affected residual locus

    X^2 A'/(aM)=U(1-t/8+9t^2/128)+error >2.             (7.3)

For p=5 retain only the first order: g>1, rho>1 give U(1-t/8)+error >1. The claimed second-order accuracy is NOT assigned to p=5, where g=2.

## 8. Exact short-tail jet, independent of c

At central points, for j<=2m<p,

    -b_j/t=j[1+(j-1)t/2+(j-1)(j-2)t^2/6]+error >2.

The added exponent cN first changes this characteristic-p expansion at relative degree N-1>2. Discarded p-divisible integer coefficients are also higher. Nonmaximal matchings of T/t^m or V/t^m contain X^2/t of value p-1>2 for p>=5. Thus the jets reduce to maximal matchings.

V has the unique maximal matching {2,4,...,2m}. T has matchings S_l={1,3,...,2l-1} union {2l+2,2l+4,...,2m}, 0<=l<=m, with weights w_l=(2l-1)!!(2m)!!/(2l)!!. The ratio recurrence for a_l=(2l-1)!!/(2l)!! proves

    sum a_l=(2m+1)a_m,
    weighted mean(l)=m/3,
    weighted mean(l^2)=m(3m+2)/15.

The first two identities needed for first order have p-unit denominators for p>=5. The second-moment formula is used only for p>=7. Expanding each maximal matching gives

    V/t^m=Btail[1+m^2 t/2
      +m(m-1)(9m^2+13m+1)t^2/72]+error >2,
    T/t^m=C[1+m(3m-1)t/6
      +m(m-1)(45m^2+35m-22)t^2/360]+error >2.

For completeness, replacing even2k by odd2k-1 for k<=l changes the first coefficient by -l/2, and changes the second coefficient by ((5-6m^2)l+l^2)/24. Averaging gives precisely these expressions. Division by the proved analytic unit gives

    kappa=alpha[1+(m/6)t+m(7m-27)t^2/360]+error >2,       (8.1)

for p>=7. For p=5 use only alpha[1+mt/6]+error >1. The actual rational alpha is retained, rather than replacing it by 1 after identifying an obstruction. No assumption about c=2 is present.

## 9. Cancellation, nonzero second correction, and actual units

On an affected root the last two terms in Qstar from (3.4) have values at least rho and p-1. At first order these exceed one for p>=5; at second order they exceed two for p>=7. By Section 6 the displacement U+alpha has the same strict bounds. Combining (7.3), (8.1), and the entire bracket gives

    Qstar=alpha(1/8+m/6)t
      +alpha[m(7m-27)/360-9/128]t^2+error >2            (9.1)

for p>=7, and its first-order truncation for p=5. The constant cancels as the exact rational -alpha+alpha, not merely modulo p. The first coefficient is alpha(2d+1)/24.

If p does not divide 2d+1, this is a unit and v(Qstar)=1. If it divides 2d+1, the inequalities 0<2d+1<2p imply p=2d+1=4m+3>=7. Then m=-3/4 mod p and

    m(7m-27)/360-9/128=-1/320 mod p.                   (9.2)

This is a unit for every p>=7. The first coefficient is p-divisible and contributes value at least e+1>2. Therefore v(Qstar)=2 and its normalized unit is -alpha/320. No third cancellation survives. In particular the simultaneous case at d=p-2 cannot occur for p>=5, although that boundary remains covered by the first correction when obstructed.

Since v(aM/X^2)=D and v(T)=m, (3.5) proves (1.2). To check actual units, at an affected residual Y with Y^2=-alpha the normalized base factor X T(aM/X^2), of value K+delta+m, has residue

    -c C epsilon M_(c-1)(Y^p)/Y
      =-2 C chi(alpha) R_c'(-alpha).                   (9.3)

Indeed Y^(p-1)=(-alpha)^((p-1)/2) and epsilon times that is chi(alpha); the identity cM_(c-1)(Y)=2Y R_c'(Y^2) supplies the remaining factor. This is independent of the two Y signs and nonzero by separability. Multiplying (9.3) by the first or second Qstar unit gives exactly (1.3). At an unobstructed central residual the same base expression times U+alpha is nonzero, giving value K+delta+m. Every affected branch, every original derivative term, and every c/2 pivot has now been accounted for.

## 10. Low roots, boundaries, original H, phases, and kernel

No edge or source denominator vanishes: n=cN+d<pN<=p^s, since (p-c)N-d>=N-(p-2)>0. The source Q indices also satisfy 2u<=cN, so their exponents lie below p^s. Unit tail factorials remain units at c=p-1 and d=p-2.

For the low roots evolve both original recurrences separately:

    Q_j(Z)=tau^(-j)P_j(tau Z), D_j(Z)=tau^(1-j)P_j'(tau Z),
    Q_(j+1)=ZQ_j-[(1-q^j)/t]Q_(j-1),
    D_(j+1)=Q_j+ZD_j-[(1-q^j)/t]D_(j-1).

They are coefficientwise integral, with Q_0=1,Q_1=Z,D_0=0,D_1=1. Reduction has -(1-q^j)/t -> j mod p, including zero at multiples of p. The integer formula gives M_p=Z^p mod p. Restarting the recurrence at each multiple of p shows M_(ap+b)=Z^(ap)M_b for 0<=b<p. Therefore

    Q_n -> Z^(cN)M_d(Z), D_n -> d Z^(cN)M_(d-1)(Z).

Because d<p, M_d is separable and has one simple zero and d-1 simple nonzero roots. Only those nonzero low residuals are used for simple-root Hensel lifting. They supply exactly d-1 simple low roots with the derivative units in Section 1. Their value1/2 separates them from all high roots. The counts 1+(d-1)+beta*cL=n exhaust the original degree, with no missing central class or root.

The exact coordinate identities are

    H_n(v0^2)=v0^n P_n(X), X=v0+v0^(-1),
    H_n'(z)=v0^(n-2)[(n/2)P_n+(v0-v0^(-1))P_n'/2].

All P roots have positive valuation and are not +/-2. On the branch v0 near i these are analytic isometries, covering all n roots near z=-1 and preserving multiplicities. At roots the prefactor term vanishes exactly. The remaining derivative multiplier has residue

    i^(n-1)=(-1)^(c/2+m).

Hence H derivative valuations agree and units are multiplied by this sign, not by a copied c=2 sign. The high H disks are v(z+q^a)>=rho.

Every recurrence edge 1-q^j for 1<=j<n is nonzero. A common root of P_n and P_(n-1) would propagate backwards to P_0=1. The original ordinary diagonal identity at any root xi is

    sum_(j=0)^(n-1) P_j(xi)^2/w_j
       =P_n'(xi)P_(n-1)(xi)/w_(n-1) !=0.

These are algebraic squares, not absolute-value squares; no positivity or real interlacing is invoked. Every estimate used the original integer/rational coefficient lattice and e=(p-1)p^(s-1), uniformly for every s>r. Choose a p-adic embedding for each characteristic-zero primitive phase; the same proof applies, and injectivity/Galois conjugacy transfers the conclusions. No fixed-phase or minimal-s numerical extrapolation is used.

## 11. Controls, exact evidence, and remaining gate

The frozen source pins bind the accepted general coefficientwise authority and its review, the general d=1 lift and its review, and the c=2 all-tail lift and its review. The even-tail report is pinned only as a convention comparison. Sources are read and hashed; no supplied source program is imported or executed. New controls are bounded transcription/falsification checks, not a census: independent short-tail matching/recurrence and derivative witness checks, exact first/second coefficient identities, selected fresh arbitrary-alpha obstructions including p=5,c=4,d=3, low original derivative recurrences, and a small original scalar recurrence check. Scalar original P' is not substituted for rootwise P': the diagnostic uses the complete Qstar bracket.

The mathematical remaining lemma in the requested bounded formulation was the arbitrary-alpha scalar bound and its all-root feedback. Sections 5-6 supply that lemma explicitly, including its p=5 first-order boundary and the raw coefficient-lattice margin at c=p-1. Thus there is no claimed unresolved exceptional case inside the stated sector. The open gate is a fresh independent review of these exact bytes, particularly (5.5)-(5.7), the all-pivot ratio (7.1), and the chi(alpha) unit in (9.3). If any of those stronger steps fails review, Sections 1-4 still give the unconditional r>=3 theorem and exact r=2 sufficient criterion R_c(-alpha)!=0, preserving exactly 2p exceptional roots when it vanishes. This fallback is not an assertion of nonsimplicity. No external publication, repository, or accepted source is changed.
