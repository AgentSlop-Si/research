# Uniform odd-leading two-step tails in the original F020 normalization

21 October 2026 UTC. Author candidate for separate independent review. The already accepted c=3 subfamily is inherited, not newly credited. No external writes, global closure, historical novelty, or FFT/complexity claim.

## 1. Exact bounded theorem

Let p be prime, c odd with 3<=c<p, r>=2, s>r, N=p^r, and q any characteristic-zero primitive p^s-th root. In particular p>=5 and c<=p-2. Preserve the original objects

    P_0=1, P_1=X, P_(j+1)=X P_j-(1-q^j)P_(j-1),
    H_j(z)=sum_k [j choose k]_q z^k,
    w_j=product_(u=1)^j(1-q^u), w_0=1.

In an algebraic p-adic embedding put t=q-1 and normalize v(t)=1. Write

    e=v(p)=(p-1)p^(s-1), B=r(p-1)p^(r-1)/2,
    K=cN/2+cB, E=(c-1)N/2+cB, D=N+E-p,
    h=floor(r/2), beta=p^h, L=N/beta,
    rho=beta/2                         if r is even,
    rho=p^(h-1)(2p-1)/2                if r is odd,
    n=cN+2.

THEOREM. Original P_n and H_n are squarefree, and the original algebraic-square Christoffel-Darboux kernel is nonzero at every P_n root. There are no mathematical exceptional parameters inside this scope.

With i^2=-1 and square-root branches near 1, let

    x_a=i(q^(a/2)-q^(-a/2)), 0<=a<beta.

The complete root partition, whose counts are first established with multiplicity, is:

- The beta disjoint disks v(X-x_a)>=rho each contain cL roots: (c-1)L boundary roots and L strict-interior roots. These account for cN roots. At every one the ORIGINAL ordinary derivative has value D+1, and the original kernel has value N-p.
- Noncentral roots have v(X)=p^ord_p(a). The central boundary roots have v(X)=rho. The L central strict-interior roots include EXACTLY one simple root at X=0 and L-1 nonzero roots. No individual deeper nonzero interior valuations are asserted.
- Exactly two further roots have value 1/2. With tau^2=t and X=tau Z, their distinct nonzero residues are Z^2=-1. Each has ordinary derivative value (cN+1)/2 and kernel value -2cB.

The exact zero is included in the high count, not discarded or confused with the whole inseparable residual-zero class. Its derivative has value D+1; its corresponding simple H root is z=-1. Corresponding ordinary H derivatives have the same valuations as P derivatives. Both original monic discriminants have value

    v(Disc P_n)=v(Disc H_n)=cN(D+2)+1.                    (1.1)

For r=2 specifically, beta=L=p and rho=p/2. Every high disk contains cp roots, (c-1)p on its boundary and p strictly inside. The central interior contains one zero and p-1 nonzero roots. This holds also at c=p-2 and at the smallest endpoint p=5,c=3. The accepted c=3 theorem is recovered, not counted as a new result; new coverage is odd 5<=c<p.

Excluded: other tails, arbitrary intermediate digits/degrees, c>=p, c=1 as new credit, p=3, r=1, s<=r, composite orders, exact deeper nonzero interior valuations, global F020/F023 closure, novelty and FFT/cost claims. Exclusions do not assert that such cases are false or otherwise unknown.

## 2. Accepted sources, precise dependency and non-circularity

The complete accepted uniform odd-adjacent author package and complete independent review are retained under sources/accepted-uniform-adjacent-author and sources/accepted-uniform-adjacent-review. Their exact pins are

    author manifest 438eb219f3534b41caa13905423c21afb2ae9fb777a8acdfa9b93438d126e032
    author report   57ed78b499b62abe3b440ba8875736ebe12e1be2b29f35d1effce8e041b2fbec
    review manifest a7deb7b69007940e8c7e49155701eabd22e7f81b01ba8012c5c94ee97a68be35
    review verdict  76b3fe4907feea9d8b4310fa6f71c07f5af1b6dfef6ccd8897e289cf00250157.

That verdict explicitly accepts the exact author report and manifest for every odd 3<=c<p. The mathematical input used here is its Sections 2-3: coefficientwise profiles for A=P_(cN), M=P_(cN-1), their ORIGINAL ordinary derivatives, and the off-root H/P coordinate transfer. Its theorem that P_(cN+1) is simple is NOT used to infer that P_(cN+2) is simple. Its r=2 second-layer lifting argument and its adjacent central interior depth are not dependencies of this proof.

The accepted c=3 next-tail author and review are retained as explicitly partial report/scope/acceptance snapshots under sources/inherited-c3-*. Their review manifest is 5604e3e05385e1d33d763e7fe282efd5a107f45c3923d9d8ad1eb1960cd73064. This establishes inherited scope and attribution. The new proof applies uniform accepted coefficientwise inputs to an exact original recurrence identity, rather than extrapolating c=3 constants or treating c=3 as new credit.

SOURCE_BINDINGS inventories every retained byte. Fresh source verification checks complete source manifests, the acceptance binding, and the nested single-leading-digit archive inventories. It distinguishes current public-projection bytes from preserved historical author/reviewer identities and never equates their different hashes. No supplied module is executed or imported.

## 3. Whole-disk coefficientwise input and residual coprimeness

Set

    A=P_(cN), M=P_(cN-1), a=1-q^(cN), b=1-q^(cN+1).

On each entire high disk, in its scaled analytic coordinate Y, the accepted input states

    wt(A)=K,      in(A)=u_A M_c(Zbar),
    wt(M)=E,      in(M)=u_M M_(c-1)(Zbar),
    wt(A')=D,     in(A')=u_D M_(c-1)(Zbar),
    wt(M')>=E,    Zbar=alpha_a Y^L, alpha_a!=0,          (3.1)

where all three u's are actual nonzero scalar residues and need not coincide. The integer polynomials here are

    M_j(Z)=sum_(u=0)^floor(j/2) j! Z^(j-2u)/(2^u u! (j-2u)!).

The ordinary derivatives in (3.1) are taken in characteristic zero before reduction. The residual degree of A is cL; coefficients above cL have strictly greater normalized weight. The full M residual includes its constant term, since c-1 is even. The ordinary A' residual likewise includes its constant: the complete accepted derivative pivots have k-m=p^2 and m=lN for l=0,2,...,c-1. The even-neighbor pivots are k=lN over the same even l. The complete derivative bound wt(M')>=E is over all summands, not just equality pivots.

For clarity, the exact OFF-ROOT coordinate identity is

    H_j(v0^2)=v0^j P_j(v0+v0^(-1)),
    H_j'=v0^(j-2)[(j/2)P_j+(v0-v0^(-1))P_j'/2].        (3.2)

On v0 near i both coordinate derivatives are units. For j=cN, the prefactor term has weight at least re+K>D, because re>N/2-p. Thus the ordinary A' input transfers on full disks and can be evaluated at the NEW roots, not only old A roots. The M prefactor has weight at least E and does not invalidate its derivative bound.

The recurrences

    M_j=Z M_(j-1)+(j-1)M_(j-2), M_j'=j M_(j-1)

show gcd(M_c,M_(c-1))=1 in characteristic p. Indeed a common root would propagate backward, using every nonzero j-1<p, to M_0=1. As c is a unit, M_c is separable. It is odd, and M_(c-1)(0)=(c-1)!/[2^((c-1)/2)((c-1)/2)!] is nonzero modulo p. Hence M_c has exactly c distinct residue roots: zero and c-1 nonzero roots. Under the purely inseparable Y^L substitution each root has multiplicity L. In particular on the ENTIRE residual locus M_c(Zbar)=0,

    v(M)=E, v(A')=D.                                   (3.3)

This includes all strict-interior classes and X=0 in the central disk.

Since c<=p-2 and N>=25,

    cN+2 <=(p-2)N+2 <pN<=p^s.

All original recurrence edges and kernel denominators below are nonzero, including at every r=2 endpoint. The actual primitive-phase units are

    v(a)=N, a/t^N -> -c;    v(b)=1, b/t -> -1.          (3.4)

## 4. Exact two-step transfer and fraction-free ordinary witness

Apply the ORIGINAL recurrence twice:

    G:=P_(cN+1)=XA-aM,
    F:=P_(cN+2)=(X^2-b)A-aXM.                          (4.1)

With T=X^2-b, ordinary differentiation followed by exact cancellation gives

    S:=T F'-2XF=T^2 A'+a(X^2+b)M-aXT M'.              (4.2)

This is a polynomial identity away from as well as on roots. At F=0 it says S=T F'. There is no division by X, so zero is retained. The square on T, the plus sign in X^2+b, and the M' correction are necessary. We do not differentiate an inseparable residual to assert the actual ordinary derivative profile.

On a noncentral disk, wt(X)=x_disk=p^ord_p(a_index)>=1. On the central disk it is rho>=p/2>1. The center distances and rho from the accepted disks give these constant Gauss weights. Since wt(X^2)>=2>v(b),

    wt(T)=1, T/t -> 1, wt(X^2+b)=1.                    (4.3)

Thus T has the fixed value 1 throughout every high disk, including its strict interior and X=0.

## 5. High root counts and the exact ordinary derivative

The TA term has weight K+1 and residual u_A M_c(alpha_a Y^L). The other term aXM has weight at least N+E+x_disk, and its strict excess is

    N+E+x_disk-(K+1)=N/2+x_disk-1>0.                  (5.1)

Consequently F has the same high residual polynomial as A on EVERY disk. Its residual degree is cL, zero multiplicity L, and c-1 nonzero residual locations each of multiplicity L; coefficients above cL have positive normalized value. Closed-disk Newton/Weierstrass counting therefore gives exactly cL roots counted with multiplicity, with (c-1)L boundary and L strict-interior roots. This uses the complete residual degree, not simple-root Hensel lifting of Y^L.

The beta disk centers have pairwise distance values at most p^(h-1)<rho. The disks are disjoint and supply cN roots. Every one lies on M_c(Zbar)=0, so (3.3) holds at each, including residual-zero branches and the exact point X=0.

At any such root, the three summands in (4.2) have values

    T^2 A':          D+2 exactly,
    a(X^2+b)M:       N+E+1=D+p+1,
    aXT M':          at least N+E+1+v(X).

At X=0 the third summand is simply zero; otherwise v(X)>=x_disk>=1. Their gaps above the first are p-1 and at least p-1+x_disk. They are STRICTLY positive uniformly in c,r,s and every root. Hence

    v(S)=D+2, v(F')=D+1.                               (5.2)

The witness residual is a nonzero scalar times M_(c-1)(alpha_a Y^L), nonvanishing on the complete F residual locus. All cN high roots are therefore simple. There is no arithmetic cancellation left to resolve.

In particular the previously exceptional adjacent residue condition p divides R_c(-1), where M_c(Z)=Z R_c(Z^2), is harmless for this next-tail target. For r=2, X=mu Y with mu^2=t^p, the accepted actual scalar is

    A'/t^D -> c M_(c-1)(Y^p).

Here T/t ->1, and the two correction terms have gap at least p-1. At a boundary residual Y^2=-1 with R_c(-1)=0,

    c M_(c-1)(Y^p)=-2 R_c'(-1)!=0.                    (5.3)

Thus the 2p roots in those next-tail residue classes have the SAME value D+1 as all other high roots. No statement that the new roots coincide with adjacent roots, or inherit their lift depth, is made. No exceptional exclusion or second-layer argument is needed. At r=2, even c=p-2 leaves the same gap p-1>=4; p=5,c=3 is the inherited lowest endpoint.

## 6. Exact zero, original predecessor and algebraic-square kernel

Original parity gives A,F odd, and M,G even. Therefore F(0)=0 exactly. The central residual-zero multiplicity L counts that point with all other central interior roots. Formula (5.2) proves zero is simple, so exactly L-1 nonzero central interior roots remain. As a direct check,

    F'(0)=-bA'(0)-aM(0).

The two terms have values D+1 and N+E=D+p. The first is uniquely smaller, including every r=2 endpoint. Also

    G(0)=-aM(0), v(G(0))=N+E.                          (6.1)

At EVERY high F root, division by T is allowed and (4.1) gives A=aXM/T. Substitution in G=XA-aM yields

    G=abM/T, v(G)=N+E.                                (6.2)

This identity also holds at X=0; unlike an expression divided by X, it does not silently lose that root.

The ORIGINAL diagonal Christoffel-Darboux identity at an F root is

    sum_(j=0)^(n-1) P_j(X)^2/w_j=F'(X)G(X)/w_(n-1).   (6.3)

This is the original sum of algebraic squares, not absolute-value squares, not a positive kernel and not the kernel of F/X. The accepted block factorial value W(N)=N+2B yields

    v(w_(n-1))=v(w_(cN+1))=cN+2cB+1.

Using (5.2) and (6.2), at ALL high roots the kernel value is

    (D+1)+(N+E)-(cN+2cB+1)=N-p.                       (6.4)

This is finite, so the kernel is nonzero, including at the exact zero. The explicit recurrence check P_(2k)(0)=(-1)^k product_(u=1)^k(1-q^(2u-1)) and P_(2k+1)(0)=0 confirms that no normalization or cancellation in the original zero kernel was changed.

## 7. Exactly two shallow roots from the original recurrence

Take tau^2=t and define the actual integral polynomials

    Q_j(Z)=tau^(-j)P_j(tau Z),
    V_j(Z)=tau^(1-j)P_j'(tau Z).

Every edge has value at least 1. The original recurrence and its ordinary differentiated recurrence give

    Q_(j+1)=ZQ_j-[(1-q^j)/t]Q_(j-1),
    V_(j+1)=Q_j+ZV_j-[(1-q^j)/t]V_(j-1),
    Q_0=1,Q_1=Z,V_0=0,V_1=1.                          (7.1)

Modulo the maximal ideal, -(1-q^j)/t reduces to j mod p, including zero for p-divisible j. Therefore Q_j reduces to M_j. The factorial formula for M_p shows all nonleading coefficients divisible by p, so M_p=Z^p mod p. An induction by blocks of length p in the recurrence, starting at M_(ap)=Z^(ap) and using the zero edge j=ap, proves

    M_(ap+b)=Z^(ap)M_b mod p, 0<=b<p.                  (7.2)

At n=cN+2 the coefficientwise reductions of the original polynomial and its separately justified ordinary derivative are

    Q_n -> Z^(cN)(Z^2+1), V_n ->2 Z^(cN+1).           (7.3)

In the second reduction cN is zero modulo p and 2 is a unit. Differentiating an already integral shallow polynomial is valid; this is not the invalid operation of differentiating a high-scale inseparable residual to guess a characteristic-zero valuation.

The two distinct residue roots Z^2=-1 are simple, and V_n is nonzero at each. Simple-root Hensel lifting gives one simple root in each class, of value 1/2 and ordinary derivative value

    (n-1)/2=(cN+1)/2.                                  (7.4)

Both lie outside all high disks, which have X values at least 1. Together with cN high roots they exhaust the degree cN+2. There are no omitted shallow or zero branches.

At either shallow root, Q_(cN) reduces to Z^(cN), which is nonzero, so v(A)=cN/2. The final recurrence F=XG-bA=0 gives G=bA/X and v(G)=(cN+1)/2. The original kernel (6.3) has value

    (cN+1)-(cN+2cB+1)=-2cB.                            (7.5)

## 8. Original H, all primitive phases and discriminants

All P roots have positive value or are zero, so none is +/-2. On v0 near i the maps X=v0+v0^(-1) and z=v0^2 have unit ordinary derivatives. Each of the n distinct P roots is mapped to a distinct H root near -1 by (3.2), preserving multiplicity. At a root the prefactor term in the ordinary H derivative vanishes exactly; the other factor is a unit. Thus the ordinary H derivative values are exactly (5.2) and (7.4). The n roots exhaust H's monic degree and prove its squarefreeness. The simple zero P root maps to z=-1.

All edges 1-q^j for 1<=j<n are nonzero. Independently, a common P_n,P_(n-1) root would propagate backward by the original recurrence to P_0=1. Combined with proven simplicity this verifies nonzero (6.3) at every root. The explicit high and shallow valuations above are stronger and remain statements about algebraic squares, not positivity.

For any characteristic-zero primitive phase, choose an algebraic p-adic embedding and use that phase's own t=q-1. All accepted coefficientwise inputs and new steps use the actual ramification e=(p-1)p^(s-1). The edge units (3.4), coordinate units, strict inequalities and root counts apply unchanged. Injectivity of the embedding transfers algebraic nonvanishing to the original phase. No finite-characteristic squarefreeness proxy is substituted for the characteristic-zero conclusion.

For a monic squarefree polynomial the discriminant valuation is the sum of ordinary derivative values at its roots. Consequently

    cN(D+1)+2(cN+1)/2=cN(D+2)+1.

The same sum applies to the original H polynomial by its unit derivative correspondence. No unknown individual deeper interior root depth is needed.

## 9. New reproducible controls and remaining review gate

The unlimited-family proof is Sections 3-8. Newly authored bounded controls are exact transcription/falsification checks, not the proof: formal two-step and fraction-free identities with deliberately wrong variants; cleared ORIGINAL Christoffel-Darboux identities; finite-field Hermite coprimeness and prior-adjacent obstruction arithmetic; complete shallow original/differentiated recurrence reductions; and mixed-characteristic original cyclotomic recurrence sections for explicitly listed parameter/phase choices, including new c>3 and the previously exceptional adjacent c=11,p=13 pair.

The cyclotomic checks state their retained X-degree explicitly. Larger examples use low-X sections containing all predicted central equality pivots plus guard coefficients; they do NOT claim that unretained higher coefficients have been checked. Those higher coefficients are covered by the uniform proof and accepted whole-disk input. Complete q-to-t conversion within the cyclotomic basis retains integer p-adic factors before ordinary differentiation. Precision exceeds every reported valuation. Source programs are not run; only the newly authored controls are cold-replayed, normally and with Python optimization, with explicit failure checks rather than assert-only validation.

MANIFEST and SEAL bind the frozen candidate. verify.py independently checks the exhaustive inventory, exact accepted-source bindings and fresh control replay. This author packet does not accept itself. A separate independent verdict on the frozen bytes remains the sole gate. No mathematical obstruction remains inside the stated scope; no public upload or repository write is part of this task.
