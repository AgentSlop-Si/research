# Uniform odd-leading adjacent degrees, including the exceptional central layer

21 October 2026 UTC. Author candidate for independent review. Original F020 normalization. The accepted c=3 family is inherited, not newly credited. No external writes, global closure, historical novelty, or FFT/complexity claim.

## 1. The precise bounded theorem

Let p be prime, 3<=c<p odd, r>=2, s>r, N=p^r, and q any characteristic-zero primitive p^s-th root. Thus p>=5. Keep exactly

    P_0=1, P_1=X, P_(j+1)=X P_j-(1-q^j)P_(j-1),
    H_b(z)=sum_a [b choose a]_q z^a,
    w_j=product_(u=1)^j(1-q^u), w_0=1.

Normalize v(t)=1 for t=q-1 in an algebraic p-adic embedding. Set

    e=v(p)=(p-1)p^(s-1), B=r(p-1)p^(r-1)/2,
    K=cN/2+cB, E=(c-1)N/2+cB, D=N+E-p,
    h=floor(r/2), beta=p^h, L=N/beta,
    rho=beta/2                         (r even),
    rho=p^(h-1)(2p-1)/2                (r odd),
    n=cN+1, A=P_(cN), M=P_(cN-1), a=1-q^(cN), F=P_n.

Define the integer polynomials

    M_j(Z)=j! sum_(u=0)^floor(j/2) Z^(j-2u)/(2^u u! (j-2u)!),
    R_c(U)=sum_(u=0)^((c-1)/2) c! U^((c-1)/2-u)/(2^u u! (c-2u)!),
    b_c=R_c(-1), so M_c(Z)=Z R_c(Z^2).

THEOREM. Both original P_n and H_n are squarefree. The original algebraic-square Christoffel-Darboux kernel is nonzero at every P_n root, for all the parameters and primitive phases above.

There is no zero root, and v(F(0))=N+E. With

    x_a=i(q^(a/2)-q^(-a/2)), i^2=-1, 0<=a<beta,

the beta disjoint closed disks v(X-x_a)>=rho contain all roots, counting multiplicity before simplicity:

- Every noncentral disk contains cL roots, comprising (c-1)L boundary roots and L strict-interior roots. All these roots have v(X)=p^ord_p(a).
- The central disk contains cL+1 roots, comprising (c-1)L boundary roots and L+1 strict-interior roots. None is zero.
- For r=2, all p+1 central strict-interior roots have exactly v(X)=p^2/(p+1). For r>=3, no individual deeper interior depth is asserted.

At a root xi, put x=v(xi). Except for the explicitly described exceptional central boundary roots below, the ORIGINAL ordinary derivative satisfies

    v(F'(xi))=min(x+D,N+E-x).                              (1.1)

For r>=3 there are no exceptions. For r=2 put d=p(p-1)/2 and choose mu^2=t^p. In the central coordinate X=mu Y, U=Y^2, the exceptional class exists precisely when p divides b_c. It consists of exactly 2p roots, counted with multiplicity, with residual U=-1. At every such root,

    v(U+1)>1,
    v(F'(xi))=K+d+1.                                     (1.2)

The usual central boundary value in (1.1) is K+d, so (1.2) is a real extra unit of valuation, not a declaration that the initial cancellation was absent. The new second layer resolves every exceptional root: there is no further arithmetic exclusion.

The corresponding ordinary H_n derivatives have the same valuations and multiplicities. Both monic discriminants therefore have value

    cN(N+E) - [cN(p-1)/p](p-2) + 2p I,                   (1.3)

where I=1 precisely when r=2 and p divides b_c, and I=0 otherwise.

The first-layer obstruction is genuine. For c=3,5,7,9,11 one has b_c=2,6,20,28,-936. Thus the accepted c=3 theorem has no allowed exceptional prime, whereas c=11,p=13 does. The first layer must not be extrapolated from c=3. No theorem for c>=p, r=1, s<=r, arbitrary intermediate digits or tails, composite orders, global F020/F023, speed, or historical priority is claimed.

## 2. Accepted inputs, attribution, and original coordinates

The retained accepted single-leading-digit theorem proves the full cN family for every 1<=c<p, including odd c, with complete coefficientwise polynomial and ORIGINAL ordinary-derivative residuals. Its exact source archive, author report, independent review, and original/public identity mappings are preserved through sources/accepted-c3-author/sources. The accepted c=3 adjacent theorem and its public review are retained separately. Its conclusions are inherited, not credited again.

The accepted even-c adjacent and second-layer theorems do not have odd-c hypotheses. No conclusion for F=P_n/X, or bound for its derivative, is imported into the present even F=P_n. We use their scalar grouped-product mechanism as an attributed starting point, and rederive all odd-parity pivots, counts, operators, and coefficient lattices below. The even second-layer report and review are retained as explicitly partial source snapshots, not falsely labeled complete standalone packages.

Write

    Q_m=product_(j=1)^m(1-q^(2j)),
    N_m(z)=product_(j=0)^(m-1)(z+q^j),
    W(m)=sum_(j=1)^m p^ord_p(j),
    T(m)=sum_(j=1)^m min(p^ord_p(j),rho), R(m)=W(m)-T(m).

All used edge indices are <p^s because cN+1<pN<=p^s. Every displayed denominator is nonzero. The accepted exact identities, valid before reduction, are

    H_b=sum_(k=b mod 2) w_b N_k/[w_k Q_((b-k)/2)],          (2.1)
    H_b'=sum_(k=b mod 2,k>=1) sum_(0<=m<k)
        w_b z^(k-m-1) N_m/[Q_((b-k)/2) w_m (1-q^(k-m))].  (2.2)

They are ordinary characteristic-zero derivative identities, not q-derivatives. On each z=-q^a+lambda Y disk, v(lambda)=rho, the accepted uniform cN input gives

    weight(N_m)>=T(m), R(m)<=W(m)/2,
    equality in the second bound exactly at m=jN,
    W(N)=N+2B, W(jN)=jW(N), W((N-1)/2)=B.

W is superadditive. The half-W assertion follows from the base-p digit formulas for W,R; its hypotheses are all 1<=c<p, not only even c. For omega^2=w_N, Zbar=alpha_a Y^L with alpha_a nonzero,

    N_N/omega -> Zbar,
    H_(cN)/omega^c -> M_c(Zbar),
    H_(cN)'/[C1 omega^(c-1)] -> c M_(c-1)(Zbar),            (2.3)
    C1=w_N/[Q_A0 (1-q^(p^2))], A0=(N-p^2)/2.

The last normalizer has value D. Its complete equality indices are k=m+p^2, m=lN, l=0,2,...,c-1. In particular the constant derivative residual is present for odd c. The relevant accepted block units are

    w_(jN)/w_N^j -> j!, Q_(uN)/w_N^u -> 2^u u!,
    Q_(uN+A*)/(Q_A* w_N^u) -> 2^u u! (0<=A*<N),
    N_(jN)/omega^j -> Zbar^j.                             (2.4)

The polynomial statement never divides by N_N at its zeros. Finally,

    H_b(v0^2)=v0^b P_b(X), X=v0+v0^(-1),
    H_b'=v0^(b-2)[(b/2)P_b+(v0-v0^(-1))P_b'/2].           (2.5)

On the branch v0 near i both coordinate derivatives are units and the disks are carried isometrically to the displayed P disks. For b=cN the prefactor term has weight at least re+K>D, since re>N/2-p. Therefore the accepted ordinary A' residual transfers coefficientwise even OFF A's roots. This justification is needed when evaluating at roots of the new F.

## 3. The full odd-c even-neighbor lemma

Let b=cN-1, A*=(N-1)/2. Then b is even and W(b)=cW(N)-N=2E. In (2.1), putting a0=(b-k)/2, the subtracted bracket W(a0)+R(k) is at most W(b)/2=E. Equality requires k=lN with l even, hence precisely

    l=0,2,...,c-1, a0=uN+A*, u=(c-1-l)/2.

Each attains equality: W(a0)=uW(N)+B. Set the actual scalar

    Cminus=omega^(c+1)/[a Q_A*], v(Cminus)=E.

The l-th equality term normalized by Cminus has residue c! Zbar^l/(l! 2^u u!). Their COMPLETE sum is

    H_(cN-1)/Cminus -> c M_(c-1)(Zbar).                   (3.1)

The k=0 term is essential. This is a new proof for all odd c, not a substitution into an even-c neighbor statement.

For the whole ordinary derivative (2.2), write j=k-m>=1. Exact reflection about cN gives W(b-j)=W(b)-W(j): for 1<=u<cN, ord_p(cN-u)=ord_p(u), including u=lN because c<p. Consequently

    W(a0)+R(m)+p^ord_p(j)
      <= E+[p^ord_p(j)-W(j)/2].                           (3.2)

At fixed d0=ord_p(j) the bracket on the right is maximized at j=p^d0, with value [p^d0-d0(p-1)p^(d0-1)]/2. Its global maximum 1/2 occurs only at j=1,p. For those j parity makes m odd. If m is not a multiple of N the half-W step is strict. Otherwise m=lN, l odd, 1<=l<=c-2, and

    2a0=(c-l)N-1-j,
    floor(2a0/N)=c-l-1 > 2floor(a0/N)=c-l-2.

The N-floor term makes 2W(a0)<W(2a0). Thus the bracket in (3.2) is always strictly less than E+1/2. Since it belongs to the half-integer lattice it is at most E. All derivative terms have weight at least E. The exact coordinate identity (2.5), including its prefactor, transfers the complete bounds to

    weight(M)>=E, weight(M')>=E.                         (3.3)

## 4. All boundary and interior roots

Original parity gives A odd and M,F even. The correct identity is

    F=XA-aM.                                             (4.1)

It is not a quotient identity. At X=0, (3.1) has the nonzero residual cM_(c-1)(0), so v(M(0))=E and v(F(0))=N+E. This also follows from the exact even constant product over the odd recurrence edges up to cN.

On a noncentral disk, X has constant value x=p^ord_p(a)<rho. The XA weight is K+x and the correction aM has weight at least N+E=K+N/2>K+x. Thus the normalized F reduction is a nonzero scalar times M_c(alpha_a Y^L). Centrally the weight is K+rho<N+E, and the reduction is a nonzero scalar times

    Y M_c(alpha_0 Y^L).                                  (4.2)

The integer recurrence M_j=Z M_(j-1)+(j-1)M_(j-2), with M_j'=jM_(j-1), proves M_c and M_(c-1) coprime modulo p. As c<p, M_c has c distinct residue roots, exactly one of which is zero when c is odd. Because L is a p-power, each of its residual locations has multiplicity L after the Y^L substitution. Equation (4.2) adds one to the central zero multiplicity.

The normalized translated polynomial is integral with residual degree cL (noncentrally) or cL+1 (centrally), and all higher coefficients have strictly positive valuation. Closed-disk Newton/Weierstrass counting gives the exact boundary/interior counts in Section 1, with multiplicity. It is not simple-root Hensel lifting of an inseparable residual. The disjoint counts sum to (beta-1)cL+(cL+1)=cN+1, so the root cover is complete and no shallow roots are missing.

At EVERY F root, including both kinds of strict-interior root, M_c(Zbar)=0. Coprimeness gives M_(c-1)(Zbar) nonzero, including Zbar=0. Therefore

    v(M(xi))=E, v(A'(xi))=D.                             (4.3)

## 5. Original derivative separation and the genuine first-layer exception

Every root is nonzero, so (4.1) gives A(xi)=aM(xi)/xi. Ordinary differentiation before reduction yields

    F'(xi)=aM(xi)/xi+xi A'(xi)-aM'(xi).                   (5.1)

For x=v(xi), the first two summands have values N+E-x and x+D; the last has value at least N+E, strictly above the first. Their difference is p-2x. This proves (1.1) whenever 2x!=p. Every noncentral x is an integral power of p, so cannot be p/2. Centrally rho>p/2 for r>=3, and interior roots have x>rho. Thus the only remaining class is the r=2 central boundary.

For this class use the POLYNOMIAL

    J=XF'-F=X^2 A'+aM-aXM'.                              (5.2)

It satisfies J=XF' at F roots. A purported coefficientwise F' residual at this scale would be false because its A term has a lower off-root weight.

Now r=2, N=p^2, B=p(p-1), d=B/2, rho=p/2, mu^2=t^p, X=mu Y. Direct residue products give

    w_N/t^(N+2B) -> -1, Q_A*/t^B -> -1,
    a/t^N -> -c, N_N/(t^B mu^p) -> -i^p Y^p.              (5.3)

For the Q product, A*=ap+a with a=(p-1)/2, and Wilson gives (-1)^a(a!)^2=-1 while (-2)^A*=1. For N_N, the p multiples of p supply (z+1)^p, the remaining factors supply -t^B, and z+1=v0 X exactly. Thus these signs are derived, not fit from controls.

Put epsilon=(-1)^((p-1)/2), eta=overline(omega/(t^B mu^p)); eta^2=-1, and delta=-i^p/eta, so delta^2=1. The actual P scalars in (2.5), using c odd and N=1 mod 4, give

    A(mu Y)/[t^(cB) mu^(cp)] -> -epsilon M_c(Y^p),
    M(mu Y)/t^E -> -M_(c-1)(Y^p).                        (5.4)

For example the second multiplier is i^(1-cN)eta^(c+1)=-1. These odd-parity scalars differ from the accepted even-c ones.

Let S=K+rho, an integer, and define the polynomial f from the even polynomial F by

    F(X)=t^S f(U), U=X^2/t^p.

Equation (5.4) yields the exact central residual

    f(U) -> -epsilon U^((p+1)/2) R_c(U)^p.                (5.5)

The actual scalar ratio of the ordinary A' to M normalizations is a Q_A*/[Q_A0 a_(p^2)]. Here A0=0 and its initial is -c t^B. The H/P multiplier has residue 1, so A'/t^(E+B) -> c M_(c-1)(Y^p). Consequently

    J(mu Y)/t^(N+E) -> c(Y^2+1)M_(c-1)(Y^p).             (5.6)

At a central boundary F root, the only possible zero of (5.6) is Y^2+1. Since the coefficients of M_c are in F_p and delta=+/-1, the boundary residual equation is equivalent to M_c(Y)=0. It meets Y^2=-1 exactly when p divides b_c. R_c has a simple root at -1 in that case, by M_c separability and p odd. There are exactly two such Y locations, each of multiplicity p, hence exactly 2p affected roots. Before the next layer, one can conclude only v(F')>K+d at these roots, not nonsimplicity and not the c=3 formula.

## 6. Complete central slack, with odd-parity pivots

All statements in this section hold for r=2 on the central boundary, in the original mixed-characteristic field and also the formal characteristic-p t-adic field used in Section 7. Precisely

    T0(m)=v(N_m)=m+(rho-1)ceil(m/p),
    Delta(m)=T0(m)-W(m)/2.

Writing m=lN+ap+b, 0<=a,b<p, gives

    2Delta(m)=a(p-1)+b+(p-2)1_(b>0).                     (6.1)

Thus Delta is zero exactly at N-multiples, and otherwise at least g=(p-1)/2>1.

For H_(cN-1), a Newton term has value

    E+[W(cN-1)-2W((cN-1-k)/2)-W(k)]/2+Delta(k).

Its pivots are k=lN, l EVEN, 0,2,...,c-1, with a0=uN+A*, u=(c-1-l)/2. Every omitted term has value >=E+g. The full M' bound is still (3.3); alternatively each derivative term has lower bound E+W(j)/2-p^ord_p(j)+Delta(m). Only j=1,p can lose 1/2, resolved either by Delta(m)>=g or the N-floor carry for odd m/N. This includes every term.

For H_(cN)' a summand with j=k-m has excess above D at least

    p+W(j-1)/2-p^ord_p(j)+Delta(m).                       (6.2)

For ord_p(j)=0 this is at least p-1, and for ord_p(j)=1 at least g. If ord_p(j)=2, j=hN; only h=1 can have zero first part, while h>=2 adds at least W(N)/2. There is no higher order since j<=cN<p^3. The complete pivots therefore are

    j=N, m=lN, l EVEN, 0,2,...,c-1,
    a0=uN, u=(c-1-l)/2.                                 (6.3)

Every omitted term has value >=D+g. Their exact terms are

    w_(cN) z^(N-1) N_(lN)/[Q_(uN) w_(lN) a_N].          (6.4)

For H_(cN), the Newton pivots are k=jN with j ODD, 1,3,...,c. All have value K. If k=lN+v, 0<v<N, the N-floor deficit in W(cN)-2W((cN-k)/2)-W(k) is at least B, while Delta(k)>=g. Hence every omitted term has value >=K+d+g>K+p. These are all-term inequalities, not a finite equality-set census.

## 7. Every exceptional root has v(U+1)>1

Assume p divides b_c. We first prove v(f(-1))>p. Work temporarily with q=1+t over F_p((t)) and X^2=-t^p, using the branch v0 near i, z=v0^2, S0=z+1=v0 X.

### 7.1 The scalar product cancellation, independent of c

For indeterminates Z,A,h over characteristic p,

    product_(a=0)^(p-1)(Z+A(1+h)^a)-(Z+A)^p

is divisible by h^(p-1). Every intermediate coefficient has a Gaussian binomial [p choose k]_(1+h) of order p-1, and the extreme difference has order at least p. This proves a polynomial divisibility statement.

Put R0=product_(j=1)^(p-1)(q^j-1), D0=product_(j odd,1<=j<2p,j!=p)(1-q^j), and C0=w_(2N)/Q_N, the product of the odd edges through 2N-1. Grouping the indices of N_N modulo p in the preceding identity gives

    N_N=N_p^p(1+error of value >p).

The zero residue group has relative error at least p(p-2)/2>p, and the others at least p(p-2)>p. Grouping the odd edges similarly gives

    C0=-t^N D0^(2p)(1+error of value >p).

The group divisible by p is exactly [(1-q^p)D0]^p; the other groups use the polynomial identity. Write N_p=S0 R, R=product_(j=1)^(p-1)(z+q^j). Since rho-1>1, R/R0=1+error of value >1. Direct multiplication gives

    R0/t^(p-1)=-(1+t/2+O(t^2)),
    D0/t^(p-1)=-(1+t/2+O(t^2)).

Both reduced index sets are F_p^*, and the sum of their (j-1)/2 coefficients is 1/2 modulo p. Since S0^2=-zt^p and z=-1+error of value >1,

    v(N_p^2-t^p D0^2)>(3p-2)+1.

Raising to p and using the grouped products proves

    v(N_N^2+C0)>W(N)+p,
    v(N_N^2)=v(C0)=W(N).                                (7.1)

This is the attributed accepted scalar mechanism, rederived without an even-c hypothesis.

### 7.2 Sum all odd leading pivots and transfer the lattice

Uniform block estimates give

    w_(hN)=h!w_N^h(1+error >=B),
    Q_(hN)=h!Q_N^h(1+error >=B),
    N_(jN)=N_N^j(1+error >=N-rho).

For internal edge indices the N-shift is higher by at least N-p=B; endpoint ratios are h+O(t^N), units because h<p. Both error bounds exceed p. Therefore the pivot k=jN, j odd, u=(c-j)/2, is

    c! C0^u N_N^j/(j! 2^u u!) + error of value >K+p.

By (7.1), sum all pivots and the complete nonpivot bound of Section 6 to obtain

    H_(cN)=N_N C0^((c-1)/2) R_c(-1)+error of value >K+p.

The first term is exactly zero in characteristic p. The unit H/P prefactor therefore gives v(A)>K+p, and F=XA-aM has value >S+p because v(aM)>=N+E=S+d and d>p.

This formal calculation must be transferred to the original integer polynomial, not assumed valid in mixed characteristic. Put m0=(cN+1)/2. A coefficient of X^(2l) in F=P_(2m0) is an integer polynomial in t, each monomial containing m0-l recurrence edges. Since every edge is divisible by t, after X^2=-t^p its raw t-degree is at least

    m0-l+pl=m0+(p-1)l>=m0.                              (7.2)

The characteristic-p result says every coefficient through degree S+p is divisible by p. Those terms have actual value at least e+m0, and

    e+m0-S >= (p-c)B-(p-1)/2 >p,                        (7.3)

since odd c<p implies c<=p-2. Terms not divisible by p already have degree >S+p. Thus the actual original polynomial at every primitive phase and every s>2 satisfies

    v(f(-1))>p.                                         (7.4)

This uses the raw coefficient lattice, not the generally false shortcut e>S+p.

### 7.3 The correct odd differential operator controls all lifts

Equation (5.2), (3.3), and the full A' bound show weight(J)>=N+E=S+d on the whole central disk. Since F is even,

    J=t^S(2U f_U-f),
    weight(2U f_U-f)>=d.                                (7.5)

One must NOT replace (7.5) by weight(f_U)>=d; that assertion is false for odd c. Write h(V)=f(-1+V)=sum a_j V^j. Translation preserves the bound in (7.5), whose coefficient at V^j is

    -2(j+1)a_(j+1)+(2j-1)a_j.                           (7.6)

Because v(a_0)>p and d>p, induction for j=0,...,p-2, dividing only by the units 2(j+1), gives v(a_j)>p for 1<=j<p. Equation (5.5), R_c(-1)=0 mod p, and R_c'(-1)!=0 show a_p is a unit; indeed its residue is R_c'(-1). All coefficients are integral.

If an exceptional root had 0<v(V)<=1, the a_p V^p term would uniquely have smallest value: it is <=p, below the constant and every j<p term, and below all j>p terms by integrality. This contradiction proves v(U+1)>1 for EVERY one of the 2p exceptional roots, without assuming simplicity.

## 8. The first ordinary-derivative correction resolves all exceptional roots

At every affected boundary point M has exact value E. Pair the l-th ordinary derivative pivot (6.4) with the corresponding even-neighbor pivot from Section 6. Their exact ratio is

    a z^(N-1) Q_(uN+A*)/[Q_(uN) a_N].                   (8.1)

Each factor in Q_(uN+A*)/Q_(uN) differs from its unshifted Q_A* factor by relative value >=B. Combining this with the COMPLETE nonpivot gaps g>1 gives

    H_(cN)'=a z^(N-1) Q_A* H_(cN-1)/a_N
                 + error of value >D+1.                (8.2)

All term errors individually have this bound, so cancellation among multiple pivots does not invalidate it. In (2.5), the derivative prefactor cN A has value at least 2e+K>D+1. Hence

    X^2 A'/(aM)=X^2 [2z^N/(z-1)] Q_A*/a_N
                      + error of value >1.              (8.3)

The coordinate factor 2z^N/(z-1)=1+error of value >1, since z=-1+error of value rho>1; also a_N/(-t^N)=1+error of value >1 by the binomial coefficients and e+1-N>1.

The actual first-order Q factorial is

    Q_A*/(-t^B)=1-t/8+error of value >1.                 (8.4)

To verify it: non-p-divisible edge j contributes -j[1+(j-1)t/2] after normalization, while p-divisible edges contribute no linear term. The leading product is -1 by Wilson as in (5.3). With a0=(p-1)/2 and A*=a0 p+a0, the sum of linear terms for the even indices is

    sum_(1<=j<=A*,p not dividing j)(2j-1)/2
        = a0/2+a0^2/2=(p^2-1)/8=-1/8 mod p.

All coefficient errors divisible by p have relative value >1, so this is an ORIGINAL mixed-characteristic calculation.

Using N=B+p and X^2=t^p U in (8.3) now gives

    X^2 A'/(aM)=U(1-t/8)+error of value >1.              (8.5)

The exact J identity is

    J=aM[1+X^2 A'/(aM)-X M'/M].                         (8.6)

At every exceptional root, U=-1+error of value >1 by Section 7, and v(X M'/M)>=rho>1 by (3.3). Thus its bracket is t/8+error of value >1. It follows that

    v(J)=N+E+1, v(F')=N+E-rho+1=K+d+1.

This establishes (1.2) for all exceptional roots and all c without another residual obstruction.

For an explicit unit check, (5.4) gives aM/t^(N+E) -> cM_(c-1)(Y^p). At Y^2=-1 this is -2R_c'(-1), since M_c'=cM_(c-1) and M_c(Z)=Z R_c(Z^2). Therefore

    J/t^(S+d+1) -> -R_c'(-1)/4,
    f_U/t^(d+1) -> R_c'(-1)/8 at the roots.              (8.7)

The second assertion uses J=2U t^S f_U at roots. For the original P derivative, with the actual scalar t^(S+d+1)/mu,

    F'/[t^(S+d+1)/mu] -> Y R_c'(-1)/4.                  (8.8)

This is nonzero at both signs of Y. The root-only f_U statement in (8.7) is not asserted off the root locus.

## 9. Exact r=2 central interior depth

This is a consequence of the same odd operator, not a guess about inseparable residuals. Let m1=(p+1)/2. In (5.5), f has residual zero multiplicity m1 at U=0. Its constant coefficient has value d because v(F(0))=N+E=S+d. The coefficient of U^m1 is a unit, and all coefficients are integral. By (7.5), (2j-1) times the coefficient of U^j has value >=d. For 0<=j<m1, 2j-1 is a p-adic unit. Hence each such coefficient has value >=d.

The lower Newton polygon from (0,d) to (m1,0) has a single segment: every intermediate coefficient lies strictly above it, and every higher integral coefficient lies above its extension. Thus precisely m1 U roots have value d/m1=B/(p+1). Passing to X^2=t^p U gives p+1 roots with

    v(X)=p/2+B/[2(p+1)]=p^2/(p+1).

This applies regardless of p dividing b_c. It is compatible with the total root-product valuation and supplies no unsupported deeper r>=3 assertion.

## 10. Original H, all phases, algebraic-square kernel, and discriminants

Modulo the maximal ideal, P_n=X^n and H_n=(1+z)^n, so P roots are not +/-2 and H roots are nonzero. At a corresponding root in (2.5), the prefactor term vanishes exactly and both coordinate derivatives are units. Thus multiplicities and original ordinary derivative values transfer to H_n. Equations (1.1)-(1.2) are finite at every root, proving both polynomials squarefree.

Every original recurrence edge for 1<=j<n is nonzero. A common root of P_n,P_(n-1) would propagate backward to P_0=1. At a P_n root xi the ORIGINAL ordinary Christoffel-Darboux identity is

    sum_(j=0)^(n-1) P_j(xi)^2/w_j
        =P_n'(xi)P_(n-1)(xi)/w_(n-1),

so the original algebraic-square kernel is nonzero. No absolute-value squares, positivity, interlacing, Fourier, or real-root argument is used. All estimates use arbitrary primitive t=q-1 and e=(p-1)p^(s-1); injectivity of the algebraic p-adic embedding and Galois conjugacy give every primitive characteristic-zero phase.

Exactly m=cN(p-1)/p roots have x=1: all roots in noncentral disks whose index is a p-unit. Every other x is at least p/2. Also sum x=N+E from the nonzero constant. Summing the minimum in (1.1) gives

    cN(N+E)-m(p-2).

At exactly 2p exceptional r=2 boundary roots the derivative increases by 1. This proves (1.3), and the H discriminant has the same value by the unit correspondence.

## 11. Controls and review status

The unlimited-family proof is Sections 2-10. Fresh, bounded controls are transcription/falsification tests only: complete neighbor and central derivative equality sets in selected parameters; original recurrence identities; exact obstruction arithmetic; actual original-ring central coefficients; and the original even-target two-jet in the exceptional c=11,p=13 case. The latter checks J=2U F_U-F at U=-1, not the false odd-c global f_U bound. The raw coefficient lattice certifies the mixed-characteristic relevance of the characteristic-p jet.

No supplied source program is imported or executed. Source snapshots are immutable and hash-bound. The candidate is not independently accepted until a separate verifier binds and accepts its final frozen bytes. No external publication or repository operation is part of this work.
