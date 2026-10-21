# Odd leading digits with every positive even short tail in original F020

Author candidate, 21 October 2026 UTC. Separate verification is required. Accepted sources are unchanged; no external write, self-acceptance, historical novelty, global F020/F023 closure, or FFT/cost improvement is claimed.

## 1. Exact theorem, attribution, and complete conclusions

Let p be prime, c odd with 3<=c<p, d=2m even with 2<=d<p, r>=2, s>r, N=p^r, and n=cN+d. Thus p>=5, c<=p-2, and d<=p-1. Let q be any characteristic-zero primitive p^s-th root. Preserve exactly

    P_0=1, P_1=X, P_(j+1)=X P_j-(1-q^j)P_(j-1),
    H_j(z)=sum_k [j choose k]_q z^k,
    w_j=product_(u=1)^j(1-q^u), w_0=1.

In an algebraic p-adic embedding set t=q-1 and normalize v(t)=1. Put

    e=v(p)=(p-1)p^(s-1), B=r(p-1)p^(r-1)/2,
    K=cN/2+cB, E=(c-1)N/2+cB, D=N+E-p,
    h=floor(r/2), beta=p^h, L=N/beta,
    rho=beta/2                         (r even),
    rho=p^(h-1)(2p-1)/2                (r odd),
    C_m=(2m-1)!!.

THEOREM. Original P_n and H_n are squarefree, and the original algebraic-square Christoffel-Darboux kernel is nonzero at every P_n root, for every parameter and primitive phase above. There are no remaining mathematical exceptions in this bounded sector.

The new coverage is ONLY odd 3<=c<p and even 4<=d<p. The d=2 theorem is already accepted for every such c and is recovered without new credit. The all-leading d=0 theorem was already accepted on 20 October 2026; odd-c d=1 and every odd d are accepted; every even-c short tail is separately accepted. Those are attribution boundaries, not deductions of new coverage here. Exact prior report, review, manifest, and acceptance bindings are retained in SOURCE_BINDINGS.json. No broader table closure is asserted.

For i^2=-1 define beta disjoint disks

    v(X-x_a)>=rho,
    x_a=i(q^(a/2)-q^(-a/2)), 0<=a<beta,

with the square-root branches near 1. All counts below are established WITH MULTIPLICITY before simplicity:

* Each disk has exactly cL high roots: (c-1)L boundary and L strict-interior roots. Their total is cN. Noncentral roots have v(X)=p^ord_p(a). Central boundary roots have v(X)=rho.
* The L central interior roots include exactly one simple root X=0 and L-1 nonzero roots. Their individual deeper valuations are not asserted. The other disks' interior roots are not zero.
* Exactly d additional roots have v(X)=1/2. For tau^2=t their distinct nonzero residues X/tau are precisely the roots of

      M_d(Z)=sum_(u=0)^floor(d/2) d! Z^(d-2u)/(2^u u! (d-2u)!).

The ORIGINAL ordinary derivative and predecessor values are

    v(P_n')=D+m,       v(P_(n-1))=N+E+m-1     at every high root,
    v(P_n')=(n-1)/2,   v(P_(n-1))=(n-1)/2     at every shallow root.

In particular these high formulas include X=0. The original kernel values are

    N-p       at every high root,
    -2cB      at every shallow root.

The corresponding original H ordinary derivative values agree. Its exact z=-1 root is simple and corresponds to X=0. The original monic discriminants satisfy

    v(Disc P_n)=v(Disc H_n)=cN(D+d)+d(d-1)/2.            (1.1)

At r=2 the high disk counts specialize to cp=(c-1)p+p, with one zero and p-1 nonzero central interior roots. No small-prime or r=2 exception occurs, including the endpoint (p,c,d)=(5,3,4), the boundary c=p-2,d=p-1, or any cancellation inherited from a DIFFERENT odd-tail target.

Excluded: c=1 as new credit; c>=p or d>=p; odd tails as new credit; r=1; s<=r; arbitrary intermediate digits/degrees; composite orders; exact deeper nonzero interior valuations; global F020/F023 closure; historical novelty; FFT/cost claims; and self-acceptance of this candidate. Exclusion does not mean false or unproved elsewhere.

## 2. Accepted authority, odd-parity data, and non-circularity

The accepted odd-plus-two report Sections 3-5 and its accepting independent review explicitly confirm the full-disk odd-leading coefficientwise inputs used below. Their pins are

    author manifest db295d917b83f18dc36ddf2f708eadf9e3203f0b60c3ddb5852fbb91a6ee28c4,
    author report   1c10fb9f9f6035ec3c56119a0e1c778e4c1f42eea0b72e630d7ed68c60fc0ff6,
    review manifest 4cf46988f5cfac2432b1d8281432af8defa66334471b176156583da5a60e7316,
    review verdict  b9e3b7ac6dfdad27a07ca83291c355e76241432e12cf0e8e3cac4f1bfbfcc12e.

Their original uniform odd-adjacent authority has manifest 438eb219f3534b41caa13905423c21afb2ae9fb777a8acdfa9b93438d126e032 and report 57ed78b499b62abe3b440ba8875736ebe12e1be2b29f35d1effce8e041b2fbec; its accepting review manifest is a7deb7b69007940e8c7e49155701eabd22e7f81b01ba8012c5c94ee97a68be35. We retain that authority too. No simplicity theorem at cN+1 or cN+2 is used to infer simplicity at cN+d.

The accepted even-leading even-tail report Sections 3-4 supplies the parity-independent finite-tail method, which is rederived here. Its even-c root geometry and zero-free conclusions are NOT imported. The accepted odd-leading odd-tail report/review supplies the audited attribution boundary and corroborates the actual odd r=2 units. Its odd-tail cancellation lifting is not a mathematical dependency of this theorem. SOURCE_BINDINGS distinguishes these roles and pins all exact bytes.

Write A=P_(cN), M=P_(cN-1), a=1-q^(cN). On each ENTIRE high disk, in its scaled coordinate Y and coefficientwise Gauss weight wt, the accepted odd input gives

    wt(A)=K,    in(A)=u_A M_c(Zbar),
    wt(M)=E,    in(M)=u_M M_(c-1)(Zbar),
    wt(A')=D,   in(A')=u_D M_(c-1)(Zbar),
    wt(M')>=E, Zbar=alpha_a Y^L, alpha_a!=0.             (2.1)

The three u's are actual nonzero scalar residues, not presumed equal. The complete A residual has degree cL, with strictly positive normalized weights above that degree. Since c is ODD, M_c has a zero, whereas M_(c-1) has a unit constant term. The M and A' residuals INCLUDE this constant term.

For precision, the complete original Newton expansions underlying this input are

    Q_k=product_(j=1)^k(1-q^(2j)),
    N_k(z)=product_(j=0)^(k-1)(z+q^j),
    H_b=sum_(k=b mod 2) w_b N_k/[w_k Q_((b-k)/2)],
    H_b'=sum_(k=b mod 2,k>=1) sum_(0<=l<k)
        w_b z^(k-l-1)N_l/[Q_((b-k)/2)w_l(1-q^(k-l))].   (2.2)

For M the complete equality indices are k=lN, l=0,2,...,c-1, with Q-index uN+(N-1)/2 and u=(c-1-l)/2. For the original A' the equality pairs have k-l=p^2 and l=l0N for ALL l0=0,2,...,c-1. The constant pivot is present. At r=2 the final pair k=cN is included. The accepted wt(M')>=E is an all-summand bound, not a selection of pivots or an even-c neighbor assertion.

The exact OFF-ROOT coordinate identities are

    H_j(v0^2)=v0^j P_j(X), X=v0+v0^(-1),
    H_j'=v0^(j-2)[(j/2)P_j+(v0-v0^(-1))P_j'/2].        (2.3)

Near v0=i the coordinate derivatives are units. For j=cN the prefactor term has value at least re+K>D, using re>N/2-p. For M the prefactor respects wt(M')>=E. Thus (2.1) is valid off old A-roots and may be evaluated at the NEW target roots. It is not obtained by differentiating an inseparable high residual.

The integer identities M_j=ZM_(j-1)+(j-1)M_(j-2) and M_j'=jM_(j-1) show gcd(M_c,M_(c-1))=1 modulo p: a common root propagates backwards through units to M_0=1. Hence M_c is separable and has exactly one zero and c-1 nonzero roots. On its ENTIRE residual root locus,

    v(M)=E, v(A')=D.                                   (2.4)

This includes every residual-zero interior branch, not merely X=0.

## 3. Exact original finite-tail transfer and fraction-free witness

Let b_j=1-q^(cN+j), j>=1. All relevant original edges and denominators are nonzero, because

    n=cN+d <=(p-2)N+(p-1)<pN<=p^s.

Their actual values and units are

    v(a)=N, a/t^N -> -c,
    v(b_j)=1, b_j/t -> -j             (1<=j<=d-1<p).    (3.1)

Define

    T_0=1,T_1=X, U_0=0,U_1=1,
    T_(j+1)=XT_j-b_jT_(j-1),
    U_(j+1)=XU_j-b_jU_(j-1).

Induction in the ORIGINAL recurrence proves

    F:=P_n=T_d A-aU_d M.                               (3.2)

For example U_2=X and U_4=X^3-(b_2+b_3)X. The U edge set starts at 2, not 1. Put W_d=U_d'T_d-U_dT_d'. Exact ordinary differentiation, before restricting to roots, gives the fraction-free polynomial identity

    S_d:=T_d F'-T_d'F
        =T_d^2 A'-aW_d M-aU_dT_d M'.                   (3.3)

Every prime means an original characteristic-zero ordinary derivative. The identity retains T_d^2, both corrections, and the subtraction T_d'F. At F=0 it says S_d=T_dF'. It neither divides by X nor changes the polynomial or kernel.

## 4. Whole-disk finite-tail bounds, including all auxiliary cancellations

Let x_disk=wt(X): it equals rho centrally and p^ord_p(a_index)>=1 noncentrally. The matching formula gives

    T_d=sum_(S nonadjacent subset {1,...,d-1})
             (-1)^|S| X^(d-2|S|) product_(j in S)b_j,
    U_d=sum_(S nonadjacent subset {2,...,d-1})
             (-1)^|S| X^(d-1-2|S|) product_(j in S)b_j.

The coefficient of X^(2k) in T_(2m) has value at least m-k; the coefficient of X^(2k+1) in U_(2m) has value at least m-1-k. These are bounds on COMPLETE coefficients, so cancellation only improves them. T_d has exactly one constant matching:

    T_d(0)=(-1)^m b_1b_3...b_(2m-1),
    T_d(0)/t^m -> C_m !=0.                             (4.1)

Every factor of C_m is <p, including d=p-1. A nonconstant T term has weight at least m+k(2x_disk-1)>m. Therefore T_d/t^m is a unit everywhere in every high disk, including the strict interiors and X=0. Ordinary differentiation retains the integer coefficients and gives

    wt(T_d)=m, wt(U_d)>=x_disk+m-1,
    wt(T_d')>=x_disk+m-1, wt(U_d')>=m-1,
    wt(W_d)>=2m-1.                                    (4.2)

Indeed U_d'T_d has weight at least 2m-1, while U_dT_d' has weight at least 2m+2x_disk-2>=2m. These bounds also hold pointwise with x=v(X)>=1; at zero the terms involving odd U_d vanish exactly. No coefficient of U_d or W_d is assumed to be a unit.

For an explicit description of the first possible auxiliary cancellation, define V_0=0,V_1=1,V_(j+1)=ZV_j+jV_(j-1). Its even-index linear coefficient b*_m=V_(2m)'(0) obeys

    b*_0=0, b*_m=(2m-2)!!+(2m-1)b*_(m-1),
    b*_m=1,5,33,279,2895,35685,... .

The first possible U_d and W_d units are b*_m and C_m b*_m, respectively. They vanish exactly when p divides b*_m, provided d<p. Every such cancellation, of whatever subsequent depth, IMPROVES (4.2) and cannot affect the decisive unit C_m. The smallest allowed new endpoint has p=5,c=3,d=4 and b*_2=5=0 modulo p. Other examples are d=6,p=11 and d=12,p=13. None is an exception for the theorem. This complete inequality argument, not a finite enumeration of exceptional primes, covers every small prime and r=2 cancellation.

## 5. Exhaustive high counts and ordinary separation, retaining zero

The perturbation aU_dM in (3.2) has weight at least N+E+x_disk+m-1. Its excess over the exact T_dA weight K+m is

    N/2+x_disk-1>0.                                   (5.1)

Thus on each FULL disk the normalized F residual is C_m times the normalized A residual. Its complete degree is cL and coefficients above that degree have positive normalized weight. Since M_c is odd and separable, this gives (c-1)L boundary roots and L strict-interior roots, cL in total with multiplicity. One must not use simple-root Hensel on M_c(alpha_a Y^L). This is the closed-disk Newton/Weierstrass count for its full residual degree.

The beta centers have pairwise distance value at most p^(h-1)<rho, so the disks are disjoint and give cN high roots. Every new root lies on M_c(Zbar)=0; therefore (2.4) applies to each one, including every central/noncentral interior branch.

At such a root the three terms of the fraction-free witness (3.3) have values

    T_d^2 A':          D+2m exactly,
    -aW_d M:           >=N+E+2m-1=D+2m+(p-1),
    -aU_dT_d M':       >=N+E+x+m-1+m=D+2m+(p+x-1).

For nonzero roots x=v(X)>=1; at zero the last term is zero. Both gaps are STRICTLY positive. Thus

    v(S_d)=D+2m, v(F')=D+m.                            (5.2)

The full witness initial is C_m^2 times the accepted A' initial, nonzero on the entire F residual root locus. This proves every high root simple. There is no tie to lift at r=2 or elsewhere. We do NOT assert wt(F')=D+m on the whole disk: the removed T_d'F term can be smaller away from roots.

Because cN and d have opposite parities, A and F are odd, M and T_d even, and U_d odd. Hence F(0)=0 EXACTLY. The witness proves it is simple, so exactly L-1 nonzero roots remain in the central strict interior. A direct check is

    F'(0)=T_d(0)A'(0)-aU_d'(0)M(0).

The first term has value D+m and the second has value at least N+E+m-1=D+m+(p-1). This check covers the p=5 auxiliary cancellation too. The zero-free even-c geometry would be false here and is not used.

The complete high count can also be written

    (beta-1)cL+(c-1)L+(L-1)+1=cN.

No finer claim about the L-1 deeper central roots is needed.

## 6. Actual odd central units and harmless inherited obstruction classes

At r=2 put mu^2=t^p, X=mu Y, epsilon=(-1)^((p-1)/2). The pinned accepted ODD coefficientwise computation gives

    A(mu Y)/(t^(cB)mu^(cp)) -> -epsilon M_c(Y^p),
    M(mu Y)/t^E -> -M_(c-1)(Y^p),
    A'(mu Y)/t^D -> c M_(c-1)(Y^p), D=E+B.             (6.1)

These are not the even-c units; in particular the A' unit has no borrowed -epsilon factor. Equations (4.1), (5.1), and (5.2) give

    F(mu Y)/(t^(cB+m)mu^(cp)) -> -epsilon C_m M_c(Y^p),
    S_d(mu Y)/t^(D+2m) -> c C_m^2 M_(c-1)(Y^p),
    F'(mu Y)/t^(D+m) -> c C_m M_(c-1)(Y^p)              (6.2)

with the last line ONLY at high roots. At the central interior residues Ybar=0, its unit is c C_m M_(c-1)(0), nonzero. At all boundary residues it is nonzero by the complete Hermite coprimality, not a single pivot or copied c=3 constant.

Writing M_c(Y)=Y R_c(Y^2), an inherited adjacent obstruction R_c(-1)=0 or an odd-tail obstruction R_c(-alpha)=0 describes classes in a DIFFERENT target. At any such residual location which also occurs here, M_(c-1)(Y^p) remains nonzero. Thus it cannot cancel (6.2). For example the previously exceptional adjacent pair p=13,c=11 has no exceptional allowed even d. The p=7,c=3 odd-tail d=3 second-layer cancellation also has no implication for even d=4 or 6. Neither new roots nor their deeper displacements are identified with those other targets' roots.

The least allowed prime p=5 and the boundary c=p-2,d=p-1 still have witness gap p-1>=4 and nonzero cC_m. No missing second-order scalar expansion, infinite obstruction scan, or unclassified arithmetic branch remains in this proof.

## 7. Original predecessor and original kernel on every high root

The tail determinant follows by induction in the original finite recurrence:

    T_d U_(d-1)-T_(d-1)U_d=-product_(j=1)^(d-1)b_j.     (7.1)

At an F root, T_d is nonzero and A=aU_dM/T_d. Substitution into P_(n-1)=T_(d-1)A-aU_(d-1)M gives the EXACT identity

    P_(n-1)=aM product_(j=1)^(d-1)b_j/T_d,
    v(P_(n-1))=N+E+m-1.                               (7.2)

Division is by T_d alone, not by X or U_d. Thus (7.2) includes X=0 and even the auxiliary-cancellation classes. At zero it agrees with the original parity formula P_(2k)(0)=(-1)^k product_(j=1)^k(1-q^(2j-1)).

All factorials remain original and nonzero. Since W(N)=N+2B and d-1<p,

    v(w_(n-1))=cN+2cB+d-1.                            (7.3)

The original diagonal Christoffel-Darboux identity at an F root xi is

    sum_(j=0)^(n-1) P_j(xi)^2/w_j
        =P_n'(xi)P_(n-1)(xi)/w_(n-1).

These are ALGEBRAIC squares, not absolute-value squares or a positive kernel. Combining (5.2), (7.2), and (7.3) gives value N-p, finite and hence nonzero, at EVERY high root including zero. No quotient F/X or replacement family is used.

## 8. Exactly d shallow roots from original ordinary recurrences

For tau^2=t define the actual integral scaled polynomials and their ordinary derivatives separately:

    Q_j(Z)=tau^(-j)P_j(tau Z),
    D_j(Z)=tau^(1-j)P_j'(tau Z),
    Q_(j+1)=ZQ_j-[(1-q^j)/t]Q_(j-1),
    D_(j+1)=Q_j+ZD_j-[(1-q^j)/t]D_(j-1),
    Q_0=1,Q_1=Z,D_0=0,D_1=1.

All edge coefficients are integral. The reduction of -(1-q^j)/t is j modulo p, including zero at p-multiples. The integer formula gives M_p=Z^p modulo p, since all nonleading coefficients have one numerator p and unit denominators. Restarting the recurrence at each multiple of p proves

    M_(ap+b)=Z^(ap)M_b modulo p, 0<=b<p.

Consequently the full original polynomial and separately justified ordinary derivative reduce as

    Q_n -> Z^(cN)M_d(Z),
    D_n -> d Z^(cN)M_(d-1)(Z).                          (8.1)

Since d<p, the same recurrence propagation proves M_d separable, and its constant C_m is a unit because d is even. Thus it has exactly d distinct NONZERO residue roots. At each, the second expression in (8.1) is nonzero. Simple-root Hensel applies here and supplies one simple root of value 1/2 per class, with derivative value (n-1)/2. The zero residual is not simple-root lifted; it has already been resolved by the complete high count.

At a shallow root the original predecessor reduces to Z^(cN)M_(d-1)(Z), which is nonzero. Hence its value is also (n-1)/2. Equations (7.3) and the same original kernel give value (n-1)-(cN+2cB+d-1)=-2cB.

Shallow roots lie outside every high disk. Since cN+d=n, these counts exhaust the original monic degree. No unexamined clusters, additional exact zero, or shallow multiplicities remain.

## 9. Original H, discriminants, and every primitive phase

All P roots have positive value or are zero, so none equals +/-2. Near v0=i, the maps X=v0+v0^(-1), z=v0^2 have unit derivatives. Identity (2.3) gives an isometric local coordinate correspondence to z near -1, preserving multiplicity before simplicity. The n distinct P roots map to n distinct original H roots and exhaust its monic degree. At each root the prefactor P_n term in (2.3) vanishes EXACTLY, leaving a unit times the original ordinary P_n derivative. Thus H is squarefree with equal derivative valuations, including a simple root z=-1 from X=0.

The derivative multiplier residue is i^(n-1), not uniformly an even-c scalar. Because n is odd, i^(n-1)=(-1)^((n-1)/2). At r=2 this is (-1)^((c-1)/2+m); at arbitrary r the expression i^(n-1) is the unambiguous one. This unit affects no stated valuation.

Independently, since every original edge 1-q^j, 1<=j<n, is nonzero, a common root of P_n and P_(n-1) would propagate backwards to P_0=1. This corroborates kernel nonvanishing from simplicity and agrees with the stronger explicit high/shallow kernel values.

For a monic squarefree polynomial its discriminant value is the sum of ordinary derivative values at roots. Therefore

    cN(D+m)+d(n-1)/2
       =cN(D+d)+d(d-1)/2,

proving (1.1) for P and H. The d=2 specialization is exactly the already accepted cN(D+2)+1.

Every argument uses the actual t=q-1 and e=(p-1)p^(s-1) of an arbitrary characteristic-zero primitive phase. Original ordinary derivatives precede reduction, and p-divisible integer factors can only increase the lower bounds, never produce false units. For every phase choose an algebraic p-adic embedding. The accepted coefficientwise inputs, strict inequalities, and actual edge units persist for every s>r. Injectivity transfers algebraic nonvanishing to the original phase. No finite-characteristic squarefreeness proxy, numerical phase scan, or root-continuity argument substitutes for this proof.

## 10. Controls, source integrity, and the remaining review gate

Sections 2-9 are the uniform proof. Fresh exact controls are bounded transcription/falsification checks: independent matching versus recurrence tails; full fraction-free and determinant identities; constant units and all possible first-tier auxiliary cancellations in a stated finite sample; odd Hermite constants/coprimeness and central units; full sparse original shallow polynomial and separately evolved ordinary derivative; one complete central high witness control in the smallest new endpoint; zero/predecessor/kernel/discriminant arithmetic; and deliberately wrong parity, edge-start, missing correction, and zero-free formulas.

The central diagnostic uses the original recurrence reduced modulo p with a stated raw integer-lattice margin, not a claim that finite-characteristic squarefreeness implies the theorem. All retained X/t coefficients and bounds excluding omitted terms are stated in its result. No supplied source program is imported or executed. Only new local control and verification scripts are run.

Source snapshots are explicitly PARTIAL documentary snapshots. Their copied manifests describe the ORIGINAL packages, not the partial directories. A fresh read-only audit verifies every listed byte and exhaustive live inventory of the accepted source packages, plus exact author/review acceptance bindings. The original single-leading-digit archive is retained as an untouched archive for the zero-tail attribution audit; public projections and historical identities are distinguished rather than equated. MANIFEST.json and SEAL.json freeze this candidate; verify.py checks its exact inventory, source audit, and deterministic normal/optimized control replay.

The mathematical exceptional set within the stated scope is empty. The open gate is a separate independent verdict on these exact frozen bytes. This candidate does not accept itself and makes no repository, public-package, global-closure, or cost claim.
