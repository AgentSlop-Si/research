# Odd leading digits with every odd short tail in original F020

Author candidate, 21 October 2026 UTC. Separate verification is required. No accepted source is changed; no external write, global F020/F023 closure, historical novelty, or FFT/cost conclusion is claimed.

## 1. Exact theorem and attribution boundary

Let p be prime, c odd with 3 <= c < p, d=2m+1 odd with 1 <= d < p, r>=2, s>r, N=p^r, and n=cN+d. Necessarily p>=5 and c<=p-2. Let q be any characteristic-zero primitive p^s-th root. Preserve exactly

    P_0=1, P_1=X, P_(j+1)=X P_j-(1-q^j)P_(j-1),
    H_j(z)=sum_k [j choose k]_q z^k,
    w_j=product_(u=1)^j (1-q^u), w_0=1.

Take an algebraic p-adic embedding, t=q-1 and v(t)=1. Set

    e=v(p)=(p-1)p^(s-1), B=r(p-1)p^(r-1)/2,
    K=cN/2+cB, E=(c-1)N/2+cB, D=N+E-p,
    h=floor(r/2), beta=p^h, L=N/beta,
    rho=beta/2 (r even), rho=p^(h-1)(2p-1)/2 (r odd),
    C=d!!, Btail=(d-1)!!, alpha=Btail/C.

Double factorials are products of positive integers of the indicated parity, with 0!!=1. All their factors are <p, so alpha is a p-adic unit. Define

    M_j(Z)=sum_(u=0)^floor(j/2) j! Z^(j-2u)/(2^u u! (j-2u)!),
    R_c(U)=sum_(u=0)^((c-1)/2) c! U^((c-1)/2-u)/(2^u u! (c-2u)!).

Thus M_c(Z)=Z R_c(Z^2), not R_c(Z^2).

THEOREM. Original P_n and H_n are squarefree, and the original algebraic-square Christoffel-Darboux kernel is nonzero at every P_n root, for all parameters and phases above. There are no unresolved mathematical exceptions within this bounded sector.

New coverage relative to the audited supplied acceptances is odd 3<=c<p and odd 3<=d<p. The d=1 theorem is already accepted, is recovered, and is not newly credited. The accepted all-leading d=0 theorem, uniform odd d=2 theorem, and all even-c tails are separate accepted scopes, not new results here. This is not a claim about historical priority or the absence of every other result in the literature. The auditable scope inventory and exact acceptance pins are in SOURCE_BINDINGS.json and SCOPE_AUDIT.json.

All root counts below include multiplicity BEFORE simplicity is proved. Let

    x_a=i(q^(a/2)-q^(-a/2)), 0<=a<beta, i^2=-1,

where square-root branches are congruent to 1. The beta disjoint disks v(X-x_a)>=rho contain exactly cN+1 high roots:

* Each noncentral disk contains cL roots, (c-1)L on the boundary and L strictly inside. Each root has x=v(X)=p^ord_p(a).
* The central disk contains cL+1 roots, (c-1)L on the boundary and L+1 strictly inside. None is zero.
* At r=2 all p+1 central interior roots have exactly x=p^2/(p+1). At r>=3 no individual deeper interior depth is asserted.
* Exactly d-1 further roots are shallow, all with x=1/2. For tau^2=t, their nonzero residues X/tau are precisely the nonzero roots of M_d.

The original even polynomial P_n has no zero root; v(P_n(0))=N+E+m. At every high root, except the explicitly classified r=2 central boundary classes below,

    v(P_n')=m+min(x+D,N+E-x).                            (1.1)

For r=2 put delta=B/2=p(p-1)/2, choose mu^2=t^p, and write X=mu Y, U=Y^2. Cancellation occurs exactly when

    R_c(-alpha)=0 mod p.                                (1.2)

When it occurs, precisely 2p central boundary roots have Ubar=-alphabar. For each of them, set b=1 if p does not divide 2d+1, and b=2 otherwise. In the second case necessarily p=2d+1>=7. Then

    v(U+alpha)>b,
    v(P_n')=K+delta+m+b.                                (1.3)

No exact deeper displacement is asserted. The normalized original derivative units, with normalizer t^(N+E+m+b)/mu, are

    Btail Y R_c'(-alpha)(2d+1)/12                 (b=1),
    -Btail Y R_c'(-alpha)/160                    (b=2).  (1.4)

They are nonzero. In particular p=7,c=3,d=3 is a genuine simultaneous first-layer/first-correction cancellation, not a missing or nonsimple case. Here alpha=2/3=3 mod 7 and R_3(U)=U+3.

At every shallow root,

    v(P_n')=(n-1)/2=cN/2+m,
    P_n'/tau^(n-1) -> d Z^(cN) M_(d-1)(Z) !=0.          (1.5)

Corresponding original H ordinary derivative valuations agree. The original kernel valuations are

    N-max(p,2x)+b I_affected             at high roots,
    -2cB                                at shallow roots. (1.6)

The two original monic discriminants have the same value

    cN(N+E) - [cN(p-1)/p](p-2)
       + m(2cN+d) + 2p b I,                            (1.7)

where I=1 exactly when r=2 and (1.2) holds, otherwise I=0 (the term bI is then zero).

Excluded: c=1 as new credit, c>=p or d>=p, even d as new coverage, r=1, s<=r, arbitrary intermediate digits/degrees, composite orders, exact deeper r>=3 interior depths, global F020/F023 closure, speed/cost, historical novelty, and self-acceptance of this packet.

## 2. Accepted coefficientwise input and odd-parity data

Write A=P_(cN), M=P_(cN-1), a=1-q^(cN). The accepted uniform odd-adjacent proof and accepting review give the following statements on EACH ENTIRE high disk in its scaled coordinate Y:

    wt(A)=K,    in(A)=u_A M_c(Zbar),
    wt(M)=E,    in(M)=u_M M_(c-1)(Zbar),
    wt(A')=D,   in(A')=u_D M_(c-1)(Zbar),
    wt(M')>=E,  Zbar=alpha_a Y^L, alpha_a!=0.           (2.1)

All displayed u's are nonzero actual scalar residues; they are not assumed equal. A's complete residual degree is cL, and coefficients above that degree have strictly greater normalized value. The M and A' residuals include their constant terms, because c-1 is even. These are characteristic-zero ordinary derivatives taken before reduction.

The input is coefficientwise, not restricted to A-roots. Its exact coordinate identities are

    H_j(v0^2)=v0^j P_j(v0+v0^(-1)),
    H_j'=v0^(j-2)[(j/2)P_j+(v0-v0^(-1))P_j'/2].         (2.2)

On v0 near i the coordinate derivatives are units. For j=cN the prefactor term has value at least re+K>D, using re>N/2-p; for M it respects the full bound wt(M')>=E. Thus (2.1) is valid off old A-roots and may be evaluated at the new roots.

For reference the accepted derivation uses

    Q_k=product_(j=1)^k(1-q^(2j)),
    N_k(z)=product_(j=0)^(k-1)(z+q^j),
    W(k)=sum_(j=1)^k p^ord_p(j),
    H_b=sum_(k=b mod 2) w_b N_k/[w_k Q_((b-k)/2)],
    H_b'=sum_(k=b mod 2,k>=1) sum_(0<=l<k)
          w_b z^(k-l-1) N_l/[Q_((b-k)/2) w_l(1-q^(k-l))]. (2.3)

For M its complete Newton pivots have k=lN for l=0,2,...,c-1, and Q-index uN+(N-1)/2, u=(c-1-l)/2. The complete A' pivots have k-l=p^2 and l=l0 N for l0=0,2,...,c-1. The full M' bound, including all nonpivots, is part of the accepted odd-neighbor lemma. No even-c neighbor estimate is silently substituted.

The identities M_j=Z M_(j-1)+(j-1)M_(j-2) and M_j'=jM_(j-1) imply that M_c and M_(c-1) are coprime modulo p: a common root would propagate to M_0=1 since every needed j-1 is a unit. Consequently M_c is separable, has exactly one zero root and c-1 nonzero roots; R_c is separable and R_c(0)!=0. On the full residual locus M_c(Zbar)=0,

    v(M)=E, v(A')=D.                                   (2.4)

This includes every interior residual-zero class, not only the boundary.

At r=2 the accepted ODD-parity scalar computations give, with epsilon=(-1)^((p-1)/2),

    A(mu Y)/[t^(cB)mu^(cp)] -> -epsilon M_c(Y^p),
    M(mu Y)/t^E -> -M_(c-1)(Y^p),
    A'(mu Y)/t^(E+B) -> c M_(c-1)(Y^p),
    a/t^N -> -c.                                       (2.5)

These signs differ from the even-c signs and will be used explicitly below.

## 3. Original finite-tail transfer and legal analytic division

Put b_j=1-q^(cN+j), j>=1. Define

    f_0=1, f_1=X, g_0=0, g_1=1,
    f_(j+1)=X f_j-b_j f_(j-1),
    g_(j+1)=X g_j-b_j g_(j-1).

Induction in the ORIGINAL recurrence proves

    P_(cN+j)=f_j A-a g_j M.

For d=2m+1 put T=f_d/X and V=g_d. These are even polynomials. Their matching formulas are

    T=sum_(S nonadjacent subset {1,...,2m})
        (-1)^|S| X^(2m-2|S|) product_(j in S)b_j,
    V=sum_(S nonadjacent subset {2,...,2m})
        (-1)^|S| X^(2m-2|S|) product_(j in S)b_j.         (3.1)

In particular the V edge set starts at 2, not 1. Because b_j/t -> -j and d<p, maximal matchings give the respective constant initials C and Btail. Every other term contains X^2/t, whose value is >=1 on every high disk. Thus T/t^m and V/t^m are analytic units throughout those disks. Set

    kappa=V/T, J=XA-a kappa M, F=P_n=TJ.                (3.2)

Here F is the ORIGINAL even polynomial, not F/X. J is an even restricted analytic function on the disk, not generally a polynomial. For the disk weight x_disk (rho centrally and p^ord_p(a_index) otherwise),

    wt(T)=wt(V)=m, kappa -> alpha,
    wt(kappa')>=x_disk-1.                              (3.3)

The last bound comes from differentiating the integral rational function of X^2/t with unit denominator; ordinary integer derivative factors are retained.

## 4. Complete high counts, no zero, and ordinary separation

The weights of TXA and aVM differ by N/2-x_disk>0. Indeed x_disk<=rho<N/2. The noncentral reduction of F is therefore a nonzero scalar times M_c(alpha_a Y^L); the central reduction is a nonzero scalar times Y M_c(alpha_0 Y^L). Residual degrees are respectively cL and cL+1, with all higher coefficients of positive normalized weight. The full-disk reductions and Newton/Weierstrass counting yield the exact high-root partition in Section 1, with multiplicity. One must not apply simple-root Hensel to Y^L.

Disks are disjoint because every pair of distinct centers has distance value at most p^(h-1)<rho. Their counts sum to cN+1. At zero, original parity gives A(0)=0 but M(0) has exact value E; V(0) has value m and a has value N. Hence F(0)=-aV(0)M(0)!=0 and v(F(0))=N+E+m. All high roots satisfy (2.4).

At a high root X!=0, J=0 gives A=a kappa M/X. Ordinary differentiation then gives

    J'=XA'+a kappa M/X-a kappa M'-a kappa'M.             (4.1)

The four terms have respective values or lower bounds

    x+D, N+E-x, N+E, N+E+x-1.                          (4.2)

The last bound is pointwise: (3.3) continues to hold at deeper central points by its integral X^2/t expression. Since every high x>=1, the last two exceed the smaller of the first two. The first two differ by p-2x. They cannot tie noncentrally, where x is an integral power of odd p; centrally rho>p/2 for r>=3, and interior roots have x>rho. Thus only r=2 central boundary roots can tie. Since F'=TJ' at a root, (4.2) proves (1.1) in every other class.

The exact root-compatible ordinary witness, valid off roots too, is

    Qstar=X^2 A'/(aM)+kappa-kappa X M'/M-X kappa',
    XJ'-J=aM Qstar,
    X T F'-(T+XT')F=a T^2 M Qstar.                     (4.3)

For a literal fraction-free polynomial identity, the last right-hand side is

    X^2 T^2 A' + aTVM - aTVXM' - aX(V'T-VT')M.          (4.4)

All division in Qstar is legal at high roots because M has exact value E and T is a proved unit after scaling. Formula (4.4) itself makes sense everywhere. At roots,

    F'=T(aM/X)Qstar.                                  (4.5)

No off-root bound for F' or F_U is inferred from this rootwise equality.

At r=2, (2.5) shows that the first term of Qstar has residual U; the next has residual alpha. The remaining terms have positive value. The boundary equation is R_c(U)^p=0, U!=0. Cancellation is therefore EXACTLY (1.2), and separability gives two Y residue locations, each with p roots counted with multiplicity. All 2p branches must now be lifted, not discarded.

## 5. Complete central slack and the arbitrary-alpha scalar estimate

Assume r=2, so N=p^2, B=N-p, delta=B/2, rho=p/2, g=(p-1)/2. On the central boundary the exact Newton-product weight is

    Tcap(k)=k+(rho-1)ceil(k/p), Delta(k)=Tcap(k)-W(k)/2.

For k=lN+ap+b with 0<=a,b<p,

    2Delta(k)=a(p-1)+b+(p-2)1_(b>0).                   (5.1)

It is zero exactly at N-multiples and otherwise at least 2g. The accepted odd-parity all-term analysis from (2.3) gives:

* Every M nonpivot has value >=E+g; its pivots have k=lN, l even.
* Every A' nonpivot has value >=D+g; its pivots have k-l=N and l=l0N, l0 even.
* Every A nonpivot has value >=K+delta+g; its pivots have k=jN, j odd.

For the derivative the full excess is bounded below by p+W(j-1)/2-p^ord_p(j)+Delta(l), with j=k-l. Orders 0 and 1 give gaps at least p-1 and g; order 2 can attain zero only at j=N, and no larger order occurs since k<=cN<p^3. For A, the N-floor carry supplies the additional delta at every nonpivot. These are complete competing-term bounds, including the constant M and A' pivots.

We prove a new scalar statement adapted to odd parity. Suppose R_c(-alpha)=0 mod p. With S=K+rho (an integer),

    v(F(X))>S+m+p at X^2=-alpha t^p, p>=5,
    v(F(X))>S+m+2p there, p>=7.                         (5.2)

The parity-free product mechanism is attributed to the accepted even-tail lift; its use for odd A is justified explicitly as follows. Work first over F_p((t)), reducing alpha to alphabar. Put z=v0^2, v0 near i, S0=z+1=v0X, and

    R0=product_(j=1)^(p-1)(q^j-1),
    D0=product_(1<=j<2p,j odd,j!=p)(1-q^j),
    C0=w_(2N)/Q_N=product_(j=1)^N(1-q^(2j-1)).

Both residue index sets are F_p^*. Through order two for p>=5,

    R0/t^(p-1)=D0/t^(p-1)=-(1+t/2-t^2/12)+O(t^3).       (5.3)

The normalized edge coefficients are (j-1)/2 and (j-1)(j-2)/6; summing gives first coefficient 1/2, second single-edge sum -1/3, and sum of squared first coefficients -1/4, hence product coefficient -1/12. Wilson gives the leading -1. The first-order use needs only the linear equality.

The exact characteristic-p product

    product_(a=0)^(p-1)(Z+C(1+h)^a)-(Z+C)^p

is divisible by h^(p-1): intermediate Gaussian-binomial coefficients have that h-order, and the extreme correction has order >=p. Group N_N and C0 by residue classes modulo p, using h=t^p. One obtains

    N_N=N_p^p(1+error >=p(p-2)/2),
    C0=-t^N D0^(2p)(1+error >=p(p-2)).                  (5.4)

The first lower bound comes from the zero-residue group: absolute error >=p(p-1), main value p*rho. Other groups have at least the displayed stronger gap. The p-divisible odd-edge group in C0 is exactly [(1-q^p)D0]^p. All these estimates depend only on v(S0)=rho, unchanged by any nonzero alpha.

Write N_p=S0 R with R=product_(j=1)^(p-1)(z+q^j). Then v(R/R0-1)>=rho-1, and S0^2=-alpha zt^p. Since alpha^p=alpha in F_p and z=-1+error of value rho,

    N_N^2/C0=alpha z^p (R/D0)^(2p)+error
            =-alpha+error >p              (p>=5),
            =-alpha+error >2p             (p>=7).      (5.5)

For the second line use the first-order equality in (5.3), rho-1>1, and p(p-2)/2>p. For the third use equality through order two, rho-1>2, and p(p-2)/2>2p. This is an arbitrary-alpha estimate, not substitution of alpha=1.

The uniform block comparisons are

    w_(hN)=h! w_N^h(1+error >=B),
    Q_(uN)=u! Q_N^u(1+error >=B),
    N_(jN)=N_N^j(1+error >=N-rho).

Internal N-shifts have relative value >=N-p=B; endpoints are units since all block indices are <p. The leading odd pivot k=jN, j odd, u=(c-j)/2, is

    c! C0^u N_N^j/[j! 2^u u!]+error >K+bp,             (5.6)

where here b=1 for p>=5 and b=2 for p>=7. Every displayed block error and delta+g exceeds bp. Summing ALL odd pivots and ALL nonpivots therefore gives

    H_(cN)=N_N C0^((c-1)/2) R_c(N_N^2/C0)+error >K+bp.

By (5.5) and R_c(-alpha)=0 in F_p this has value >K+bp. The unit H/P multiplier preserves it. Consequently TXA has value >S+m+bp; aVM has value N+E+m=S+delta+m, and delta>bp in the indicated ranges. This proves (5.2) formally in characteristic p.

For the ORIGINAL mixed-characteristic polynomial, n is even. A coefficient of X^(2l) in P_n is a sum of products of n/2-l recurrence edges. At X^2=-alpha t^p each raw monomial therefore has t-degree at least

    n/2-l+pl=n/2+(p-1)l>=n/2.                          (5.7)

Clear powers of the p-unit denominator C. Formal characteristic p shows every coefficient through S+m+bp is divisible by p. Such coefficients have actual value >=e+n/2, and at the minimal s=3,

    e+n/2-(S+m) >= (p-c)B-(p-1)/2 >bp.                 (5.8)

Here c<=p-2, B=p(p-1), and the first/second ranges above are used. Larger s only improves the margin. Terms not divisible by p already have larger raw degree. Thus (5.2) holds for every original primitive phase. We do not use the generally false shortcut e>S+m+bp.

## 6. Correct odd differential operator and all-root feedback

On the central disk define the even restricted analytic function j by

    J(mu Y)=t^S j(U), U=Y^2.

It is integral: XA has weight S and a kappa M weight S+delta. Its complete residual, using (2.5), is

    j(U) -> -epsilon U^((p+1)/2) R_c(U)^p.              (6.1)

The exact identity (4.3) and the full A', M' bounds give the COEFFICIENTWISE statement

    wt(XJ'-J)>=N+E=S+delta,
    wt(2U j_U-j)>=delta.                              (6.2)

Indeed the four terms X^2A', a kappa M, -a kappa XM', and -aX kappa'M have weights at least N+E, N+E, N+E+rho, and N+E+p-1. The false even-parity assertion wt(j_U)>=delta is NOT used.

By (5.2) and v(T)=m, v(j(-alpha))>bp. Translate j(-alpha+V)=sum h_l V^l. The coefficient of V^l in (6.2) is

    -2alpha(l+1)h_(l+1)+(2l-1)h_l.                     (6.3)

Since delta>bp and h_0 has value >bp, induction for l=0,...,p-2, dividing only by units 2alpha(l+1), gives v(h_l)>bp for 1<=l<p. Separability of R_c at -alpha and (6.1) show that h_p is a unit. All higher coefficients are integral. If any affected root had 0<v(V)<=b, h_p V^p would be uniquely smallest: at most bp, below the constant and all l<p terms, and below all l>p terms. This contradiction proves v(U+alpha)>b for EVERY one of the 2p affected roots, with no simplicity assumption.

The same operator determines the central interior depth. Let h0=(p+1)/2. The constant j(0) has value delta, the coefficient of U^h0 is a unit by (6.1), and for 0<=l<h0 the factor 2l-1 is a p-adic unit. Hence (6.2) gives value >=delta for every such coefficient. The lower Newton segment from (0,delta) to (h0,0) is single; its intermediate coefficients lie strictly above it, and all higher integral coefficients lie above its extension. Thus the h0 small U roots have value delta/h0=B/(p+1), giving exactly p+1 X roots of value p/2+B/[2(p+1)]=p^2/(p+1). Since F and J have the same roots on the disk, this proves the interior assertion without treating J as a polynomial globally.

## 7. Full ordinary derivative ratio and exact tail jets

On the central boundary, pair every ordinary A' pivot with the M pivot having the same even l. With Ahalf=(N-1)/2 and u=(c-1-l)/2, the exact H-side ratio is

    a z^(N-1) Q_(uN+Ahalf)/[Q_(uN) a_N], a_N=1-q^N.

All N-shift errors have relative value >=B. Summing every pivot and using every nonpivot gap >=g gives, after the exact OFF-ROOT H/P ordinary conversion,

    X^2 A'/(aM)=X^2 [2z^N/(z-1)] Q_Ahalf/a_N+error >=g. (7.1)

The prefactor cN A in that conversion has value at least 2e+K>D+2. The ratio is justified at boundary points with v(M)=E, in particular all affected roots. This uses the ODD even-index pivot set, not the even-c odd-index set.

The factorial calculation is independent of c. For a0=(p-1)/2, Ahalf=pa0+a0, the p-divisible even indices contribute no normalized term below t^p. For all other indices the first two normalized coefficients are

    u_j=(2j-1)/2, v_j=(2j-1)(2j-2)/6.

Their multiset consists of a0 full nonzero residue blocks followed by 1,...,a0. Modulo p, the sums are sum u_j=-1/8, sum v_j=1/8, sum u_j^2=1/8. Thus the product's second coefficient is 1/8+((1/64)-(1/8))/2=9/128. Wilson supplies leading -1. Mixed-characteristic discarded coefficients have relative values >=e or >=e+1-p, both >2. Therefore

    Q_Ahalf/(-t^B)=1-t/8+9t^2/128+error >2.              (7.2)

Also a_N/(-t^N)=1+error >2, and 2z^N/(z-1)=1+error >=rho. Combining (7.1)-(7.2), for p>=7 (where g>2 and rho>2),

    X^2 A'/(aM)=U(1-t/8+9t^2/128)+error >2.             (7.3)

For p=5 use only U(1-t/8)+error >1: g=2 is not silently treated as >2.

The finite-tail jets are also parity-independent but must retain their actual alpha. At j<=2m<p,

    -b_j/t=j[1+(j-1)t/2+(j-1)(j-2)t^2/6]+error >2.

The added exponent cN first enters at relative degree N-1>2; integer p-divisible coefficients are higher. Nonmaximal matchings in (3.1) contain X^2/t of value p-1>2. V has unique maximal matching {2,4,...,2m}. T's maximal matchings are

    S_l={1,3,...,2l-1} union {2l+2,2l+4,...,2m}, 0<=l<=m,

with weights w_l=(2l-1)!!(2m)!!/(2l)!!. The ratio recurrence of a_l=(2l-1)!!/(2l)!! gives sum a_l=(2m+1)a_m, weighted mean(l)=m/3 and weighted mean(l^2)=m(3m+2)/15. The last identity is needed only at p>=7. Expansion gives

    V/t^m=Btail[1+m^2 t/2
       +m(m-1)(9m^2+13m+1)t^2/72]+error >2,
    T/t^m=C[1+m(3m-1)t/6
       +m(m-1)(45m^2+35m-22)t^2/360]+error >2.

Replacing even 2k by odd 2k-1 for k<=l changes the first coefficient by -l/2 and the second by ((5-6m^2)l+l^2)/24; averaging gives the stated formulas. Dividing the unit denominator yields

    kappa=alpha[1+(m/6)t+m(7m-27)t^2/360]+error >2       (7.4)

for p>=7. For p=5 its first-order truncation is valid with error >1. These statements apply also at the d=p-2 boundary; all needed factors in C and Btail are units.

## 8. Every cancellation resolved, with the odd-parity units

At each affected root the last two terms in Qstar have values at least rho and p-1. These exceed 1 for p>=5, and 2 for p>=7. Section 6 gives the same strict bound for U+alpha. Substitution in the COMPLETE bracket (4.3) gives

    Qstar=alpha(1/8+m/6)t
       +alpha[m(7m-27)/360-9/128]t^2+error >2            (8.1)

for p>=7, and its first-order truncation for p=5. The constant cancels as the exact rational -alpha+alpha, not only modulo p.

The first coefficient is alpha(2d+1)/24. Unless p divides 2d+1 it is a unit, so v(Qstar)=1. If p divides 2d+1, the range 0<2d+1<2p gives p=2d+1=4m+3>=7. At m=-3/4 mod p,

    m(7m-27)/360-9/128=-1/320 mod p.                    (8.2)

It is a unit for all these primes. The first coefficient then contributes value >=e+1>2; hence v(Qstar)=2 with normalized unit -alpha/320. There is no third cancellation or unclassified arithmetic case.

For the actual original derivative scalar, (2.5) and (4.5) give the base factor

    [T aM/X] / [t^(N+E+m)/mu]
       -> C c M_(c-1)(Y^p)/Y.

At Y^2=-alpha, M_c'=cM_(c-1) and M_c(Y)=Y R_c(Y^2) imply

    cM_(c-1)(Y)=R_c(-alpha)-2alpha R_c'(-alpha)
                =-2alpha R_c'(-alpha).

This scalar is in F_p, hence cM_(c-1)(Y^p) has the SAME value. Therefore the base unit is -2C alpha R_c'(-alpha)/Y. Multiplying by the first or second unit in (8.1)-(8.2) and using 1/Y=-Y/alpha yields exactly (1.4). There is NO borrowed even-c Legendre-symbol factor. The d=1 first-correction unit specializes to Y R_c'(-1)/4, matching its accepted odd-adjacent source.

Since v(TaM/X)=N+E+m-rho=K+delta+m, (4.5) now proves (1.3), and every affected root is simple. Along with Section 4, every high root is simple.

## 9. Shallow roots, original H, original kernel, and discriminants

No original edge or source denominator vanishes: cN+d <=(p-2)N+(p-2)<pN<=p^s. For tau^2=t define the ORIGINAL integral scaled polynomial and its ordinary derivative separately:

    Q_j(Z)=tau^(-j)P_j(tau Z), D_j(Z)=tau^(1-j)P_j'(tau Z),
    Q_(j+1)=ZQ_j-[(1-q^j)/t]Q_(j-1),
    D_(j+1)=Q_j+ZD_j-[(1-q^j)/t]D_(j-1),
    Q_0=1,Q_1=Z,D_0=0,D_1=1.

The edge reduction is -(1-q^j)/t -> j mod p, including zero at p-multiples. M_p=Z^p mod p follows from its integer coefficients. Restarting the recurrence at each multiple of p gives M_(ap+b)=Z^(ap)M_b for 0<=b<p. Consequently

    Q_n -> Z^(cN)M_d(Z), D_n -> d Z^(cN)M_(d-1)(Z).

M_d is separable because d<p. Its d-1 nonzero roots each lift simply and give (1.5); the zero residue is NOT simple-root lifted and is instead resolved by the complete high count above. High cN+1 plus shallow d-1 equals n, so every original root is accounted for.

All roots have positive value and none is +/-2. On the branch v0 near i, (2.2) gives isometric analytic coordinates X=v0+v0^(-1), z=v0^2 near z=-1, preserving multiplicities. At a root the prefactor P_n term in H_n' vanishes exactly, and the remaining multiplier is a unit. Thus all n original H roots are simple, with equal ordinary derivative valuations. No kernel or polynomial is divided by X, and no algebraic square is replaced by an absolute-value square.

The tail determinant follows from its original recurrence:

    f_d g_(d-1)-f_(d-1)g_d=-product_(j=1)^(d-1)b_j.

At a high F root f_d=XT is nonzero, so the original predecessor is

    P_(n-1)=aM product_(j=1)^(d-1)b_j/(XT),
    v(P_(n-1))=N+E+m-x.                               (9.1)

At a shallow root its scaled predecessor is Z^(cN)M_(d-1)(Z)!=0, so its value is (n-1)/2. Also

    v(w_(n-1))=cW(N)+d-1=cN+2cB+2m.

The original ordinary diagonal identity at every root xi is

    sum_(j=0)^(n-1)P_j(xi)^2/w_j
       =P_n'(xi)P_(n-1)(xi)/w_(n-1).

Equations (1.1), (1.3), (1.5) and (9.1) give precisely (1.6), all finite, hence nonzero. Independently, a common P_n,P_(n-1) root would propagate by nonzero original edges to P_0=1. No positivity or interlacing argument is invoked.

The constant term gives total sum of root valuations N+E+m; subtracting the d-1 shallow roots leaves high sum x=N+E. Exactly cN(p-1)/p high roots have x=1; all other high x>=p/2. Summing the minimum in (1.1) over cN+1 high roots gives cN(N+E)-[cN(p-1)/p](p-2). Add m for each high derivative, add the d-1 shallow derivative values, and add b for each of the 2p affected roots. This yields (1.7). The monic H discriminant has the same sum by the unit ordinary-derivative correspondence.

Every argument used the actual t=q-1 and e=(p-1)p^(s-1) of an arbitrary primitive phase. Choose an algebraic p-adic embedding for each phase; all residue units, complete coefficientwise estimates, and raw integer-lattice margins persist. Injectivity transfers the resulting algebraic nonvanishing to the original characteristic-zero phase. This is not a finite-characteristic squarefreeness proxy or a numerical phase extrapolation.

## 10. Verification boundary

Sections 2-9 are a uniform proof from the pinned accepted coefficientwise inputs. New exact controls are bounded transcription and falsification checks, not that proof: the finite-tail polynomial and fraction-free identities, determinant and derivative recurrence, exact matching jets, odd obstruction arithmetic (including the genuine p=7,c=3,d=3 second layer), original characteristic-p scalar recurrence with a quantified mixed-characteristic lattice margin, and complete shallow original/differentiated recurrence reductions. Wrong parity operators, tail-edge starts, first-correction units, and zero counts are negative controls.

Only newly authored control code is executed; no supplied program is imported or run. Source snapshots are explicitly partial, with exact proof/review/manifest identities and freshly checked live source inventories rather than falsely complete standalone copies. MANIFEST.json and SEAL.json freeze this candidate and verify.py checks its complete inventory and deterministic control replay. The independent reviewer must bind these final bytes. Until then this is an author candidate, not an accepted closure of even its stated sector.
