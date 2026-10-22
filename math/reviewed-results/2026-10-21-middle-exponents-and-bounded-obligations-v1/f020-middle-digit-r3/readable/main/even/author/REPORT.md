# Uniform even middle digits: n = 2p^3 + cp

21 October 2026 UTC. Author candidate requiring a separate independent review. No source program was executed. No repository, public artifact, or table was changed. This packet does not accept itself.

## 1. The bounded family and exact conclusions

Let p be any odd prime, s>3, q any characteristic-zero primitive p^s-th root, and c an EVEN integer with 2<=c<p. Set n=2p^3+cp. The original definitions remain

    P_0=1, P_1=X, P_(j+1)=X P_j-(1-q^j)P_(j-1),
    H_b(z)=sum_k [b choose k]_q z^k,
    w_j=product_(u=1)^j(1-q^u), w_0=1.

The candidate proves that P_n and H_n are squarefree and, at every root xi of P_n, the original algebraic-square kernel is nonzero:

    sum_(j=0)^(n-1) P_j(xi)^2/w_j != 0.

This is a uniform sector, not a list of isolated cases. The c=2 conclusion is inherited and is NOT new theorem credit. The genuinely added scope is every even 4<=c<p. The accepted c=1 result remains inherited and is neither re-proved nor claimed covered by this even-sector argument. Odd 3<=c<p remains outside this candidate.

In an algebraic p-adic embedding normalize v(t)=1 for t=q-1, retain e=v(p)=(p-1)p^(s-1), and define

    N=p^3, L=p^2, m=(p-1)/2, B=3(p-1)p^2/2,
    K=N+2B, E=N/2+2B, D=N+E-p,
    rho=p-1/2, alpha=1-1/(2p), F=c(p-1/2),
    x_a=i(q^(a/2)-q^(-a/2)), i^2=-1, 0<=a<p,

where the roots of q^a are chosen near 1. The complete disjoint root ledger is:

- Exactly 2L roots on the boundary of each old disk D_a={v(X-x_a)>=rho}, totaling 2N roots. At each of them the ORIGINAL ordinary derivative has value D+F.
- Exactly cp further roots have X-value alpha<1. Choose r with r^(2p)=t^(2p-1). Their nonzero normalized residues y=X/r satisfy He_c(y^p)=0. There are c distinct residue classes, each containing exactly p roots. Their ORIGINAL derivative value is 2N alpha+F-1/2.
- There is no zero and no uncounted root. More exactly v(P_n(0))=K+F.

Here He_j is the monic probabilists' Hermite polynomial, He_0=1, He_1=Z, He_(j+1)=Z He_j-j He_(j-1). The residue field is algebraically closed. Because c<p is even, He_c has c distinct NONZERO roots. Frobenius is bijective on that field, so He_c(Y^p) has c distinct nonzero root locations, each of multiplicity p. We do not simple-root-Hensel-lift that repeated polynomial.

The alpha classes are coarse residue classes {v(X/r-y_l)>0}; no common finer separating radius or exact center is asserted for general c. In particular these roots are not identified with roots of the unshifted short polynomial P_(cp), or with roots of the exact shifted tail. The accepted c=2 theorem has stronger finer-disk geometry, which remains valid but is not re-credited or extrapolated.

## 2. Audit before mathematical credit, and provenance limit

The accepted short-tail assembly covers n=a p^r+d with r>=2, 1<=a<p, and 0<=d<p. A target here has digits 20c0; cp is not d<p. The accepted first-two-digit residual range is b<p^2, not arbitrary two occupied digit positions. Pure powers, a single leading digit, earlier bounded block families, fixed p=3 degrees, fixed order-9/order-25 certificates, and conditional local/all-A guards do not already imply this new sector. The latest middle-digit candidates and their accepting reviews cover c=1 and c=2 exactly; both are inherited.

This is a bounded audit of the inspected accepted source chain, not a global literature or originality search. The original identities, p-block coefficient fact, full-disk leading-two inputs, and whole-short-block matching mechanism remain inherited mathematics. The present candidate proves their uniform shifted-tail perturbation for EVEN c<p, including the first-deleted-tail cancellation guard.

The accepted c=2 author manifest is SHA-256 ebff60ce117ad3f9f7830e1053b1edf02f0e6733cf9571ca80e4b6d25544e05e and its accepting review manifest is 1fd4b414f987ad2244420386d82cfa4a847551eb74f4014bd86056f456712cc6. The c=1 author/review manifest hashes are 3b560b06a3c8c635c771adf31f05c70917fed370266e7c73d71d5b7005787d12 and 6ce8b81464ad0be29fcbf504ad302f7d07a2ad5f25111922a7484ce8879e9fc6. Fresh source controls verify these exact manifests and every listed file; selected documentary snapshots are not presented as complete copied packages.

The historical b=2p discrepancy is preserved. The retained report has SHA-256 00a4ad13b0726205f3dd6515a4f4c6e9687622c738efdb3df39360b6bcf593db, while its historical review cites original report 6b27fcbdc7aae652afae91fa9e1a8baf84270ef57af75c44c5f35288541686da. These are different bytes. Neither the original b=2p report nor its complete original package is claimed recovered or accepted here. The general whole-block residual used below is directly reconstructed, not justified by transferring byte acceptance to the changed snapshot.

## 3. Legal specialization and inherited off-root high-disk coefficients

Write A=P_(2N), M=P_(2N-1), a0=1-q^(2N). The accepted general adjacent-criterion report and its review supply coefficientwise weights K,E,D,>=E for A,M,A',M' on each D_a. Their initial polynomials are respectively nonzero scalar multiples of Zbar^2+1, Zbar, Zbar, and an integral residual, where Zbar=gamma_a Y^L with gamma_a!=0. In particular at the locus Zbar^2+1=0, M and A' have exact values E and D. These are full-disk OFF-OLD-ROOT statements and therefore apply at new roots. A' and M' mean original characteristic-zero ordinary derivatives, never a derivative of an inseparable reduction.

The same accepted inputs give exactly 2L boundary roots of A per disk, exhausting degree 2N, and v(A(0))=K. The centers have mutual distance value one, and rho>1. Every A root has X-value at least one.

The degree bound is uniform:

    n<=2p^3+p(p-1)<p^4<=p^s,
    p^4-[2p^3+p(p-1)]=p[(p-2)p^2-p+1]>0.

It holds at p=3. All used edges and q-factorials are nonzero; for 1<=j<p^s, v(1-q^j)=p^ord_p(j). In particular v(a0)=N.

## 4. Exact tail, local blocks, and three distinct scales

Define b_j=1-q^(2N+j) for 1<=j<cp. Set f_0=1,f_1=X,g_0=0,g_1=1 and apply the same recurrence with edge b_j to f and g. Put f=f_(cp), g=g_(cp). Direct induction in the ORIGINAL recurrence gives

    P_n=f A-a0 g M.                                    (4.1)

The tail f has cp vertices; g is its FIRST-vertex-deleted continuant and has cp-1 vertices. It is not silently replaced by P_(cp-1), which deletes the other endpoint in the unshifted block model. Here f is even and g is odd.

We use three scales without identifying them: the old high disks of radius rho about x_a, the t scale X=tY used for coefficient bounds, and the alpha scale X=rY where v(r)=alpha<1. Bounds are coefficientwise Gauss valuations, not only evaluations at selected roots.

For the unshifted p-block, the inherited coefficient fact is

    P_p=X^p+lambda X+J,
    v(lambda)=p-1, lambda/t^(p-1) -> epsilon=(-1)^((p+1)/2),
    J odd, degrees 3,...,p-2, coefficient values >=p-1.  (4.2)

It follows from [p choose j]_(1+t)=(-1)^(j-1)t^(p-1)/j+O(t^p) modulo p, the exact H/P Laurent identity, and differentiation of the ORIGINAL H_p at -1. The precision p-1 is below e. In particular no formal characteristic-p derivative is substituted for an ordinary derivative.

Every p-block of the shifted cp tail starts at exponent 2N+ip, 0<=i<c. Its edges differ from the unshifted p-block by terms of value at least p (value N at i=0). Telescoping an h-edge matching gives difference-coefficient value at least p+h-1. Thus for every such block U:

    U(tY)/t^p -> S(Y)=Y^p+epsilon Y;
    weight(U at X=rY)>=p alpha, initial Y^p;
    U'(rY)/t^(p-1) -> epsilon.                       (4.3)

At any X-weight x>=1, weight(U)>=p-1+x. For (4.3)'s ordinary derivative, the leading term is p X^(p-1), of value e+(p-1)alpha>p-1. All other non-linear terms have strictly higher derivative weight than p-1. A p=3 block has J=0, which causes no failure.

Let a p-block lose its last or first vertex. The resulting even (p-1)-vertex blocks have weight m at every X-weight beta>1/2. Their normalized constant residues are respectively d=(p-2)!! and h=2^m m!, with dh=-1 modulo p. Their X^(2j) coefficients have values >=m-j and derivatives have weight >=m-1+beta. A block losing both endpoints has p-2 odd vertices, weight >=m-1+beta and derivative weight >=m-1. These are direct matching bounds with unique perfect matchings for the even constants.

The joining edge after block i has exponent 2N+ip, 1<=i<c, value p and normalized residue -i: b_(ip)/t^p -> -i. All these i are nonzero modulo p. This is the correct p-block joining scale. The short d<p unit-tail rule is invalid at d=cp: its relevant double factorial contains p, and its shallow Hermite residual collapses. We do not use that rule.

## 5. Uniform even-c high-scale bounds, without an unjustified g unit

Expand f by the subset J of its c-1 joining edges. Put j=|J| and let a be the number of adjacent selected-edge pairs. There are a twice-incident blocks, 2j-2a once-incident blocks, and c-2j+a intact blocks. At the t scale the subset's weight is at least

    cp-j+a(m+1).

The number of runs is j-a<=c/2. Hence its gap above F=cp-c/2 is at least am. With a=0, equality requires j=c/2, the unique perfect matching {1,3,...,c-1}. Its normalized constant is

    C_c=He_c(0)=(-1)^(c/2)(c-1)!! !=0 modulo p.

Therefore f(tY)/t^F is integral with constant nonzero reduction C_c. Because f is even, this immediately implies at every X-Gauss weight x>=1

    weight(f)=F, with constant nonzero initial;
    weight(f')>=F-2+x.                                (5.1)

Indeed the coefficient of X^d, d>=2 even, has value at least F-d; its differentiated monomial has value >=F-d+(d-1)x>=F-2+x. This deliberately weak bound retains actual ordinary integer multipliers.

For g, the first block has only p-1 vertices. Let z indicate whether its first joining edge is selected, and let a count twice-incident COMPLETE blocks. The same direct classification gives subset weight at least

    m+(c-1)p-j+(a+z)(m+1).

The number of runs not touching the shortened first block is j-a-z<=floor((c-1)/2)=c/2-1. Thus every subset has weight at least F-m. As g is odd, the resulting coefficientwise bounds are

    weight(g)>=F-m-1+x,
    weight(g')>=F-m-1,       x>=1.                    (5.2)

No nonzero initial for g or g' is needed or asserted.

This restriction is essential. The possible t-scale initial is h J_c S(Y), where

    J_c=sum_J product_(i in J)(-i),

with the sum over all size c/2-1 nonadjacent subsets of {2,...,c-1}. The exact cancellation set for this particular residual is {(p,c): p odd prime, c even, 2<=c<p, J_c=0 mod p}. It is NOT an exception set for the theorem. For example J_2=1, J_4=-5, J_6=33: at (p,c)=(5,4) and (11,6) the initial vanishes. Replacing the first-deleted g by the last-deleted neighbor would incorrectly replace J_c by the nonzero Hermite constant. Equations (5.2) survive every such cancellation, since cancellation only increases their valuations. We neither claim those listed examples exhaust the cancellation set nor assume it empty.

## 6. All high roots, every ordinary derivative term, and no zero

On D_a use x=1 for a!=0 and x=rho for a=0. The principal term fA has weight F+K. By (5.2) the correction has weight at least N+F-m-1+x+E. Its gap is

    N/2-m-1+x>0.                                     (6.1)

Hence P_n has the same degree-2L nonzero-constant boundary residual as a scalar unit times A on each old disk. Newton/Weierstrass counting gives exactly 2L boundary roots there, with multiplicity counted BEFORE simplicity is shown. There are none in the strict interior of any old disk.

At every such new root, v(M)=E, v(A')=D, and v(M')>=E. Since f is a normalized unit, the root equation A=a0gM/f is legitimate, even when g=0. Differentiate the exact polynomial (4.1) in characteristic zero:

    P_n'=f A'+f' A-a0 g'M-a0 gM'.                    (6.2)

The first term has exact value F+D=N+E+F-p. By (5.1)-(5.2) the remaining terms have respective lower bounds

    N+E+F-m-3+2x,
    N+E+F-m-1,
    N+E+F-m-1+x.

Their gaps above the first are m-2+2x, m, m+x. All are strictly positive because m>=1 and x>=1. Thus fA' is uniquely minimal, proving v(P_n')=D+F at EVERY high root. Exceptional g cancellation cannot cancel this term and only strengthens the error bounds.

Both g and M are odd, so P_n(0)=f(0)A(0) exactly. Equation (5.1) yields v(P_n(0))=F+K, which is finite. There is no exact zero or extra central root.

## 7. Reconstructing the inherited whole-short-block alpha mechanism

For T=P_(cp), expand by joining subsets as above, now at alpha. Let

    delta=(p^2-1)/(2p)>0.

The subset with j selected joins and a adjacent pairs has weight at least F+a delta. If a=0, its normalized residual is product_(i in J)(-i) Y^(p(c-2j)), because each selected joining edge contributes i after its recurrence sign, while each endpoint pair contributes dh=-1. Summing precisely the nonadjacent subsets is the Hermite matching formula. Therefore

    T(rY)/r^(cp) -> He_c(Y^p).                        (7.1)

This identity and its proof are inherited mathematics, reconstructed here in the original recurrence. At p=3 the allowed even sector is only c=2, and the same proof remains valid.

Reduce the ORIGINAL ordinary derivative separately. Let U=t^(p-1)r^((c-1)p), whose value is F-1/2. In differentiating each exact subset summand:

- hitting an intact p-block gives weight >=F+a delta-1/2;
- hitting a one-endpoint-deleted block gives >=F+a delta-1+alpha;
- hitting a twice-endpoint-deleted block gives >=F+a delta-alpha.

If a>=1, all corresponding gaps above F-1/2 are positive. The smallest third-type gap is delta-alpha+1/2=m>0. If a=0, endpoint derivatives have positive gap alpha-1/2. Thus only derivatives hitting intact p-blocks of a nonadjacent matching survive, each with the epsilon residue in (4.3). Their sum is

    T'(rY)/U -> epsilon He_c'(Y^p).                  (7.2)

He_c' means derivative in its OWN variable Z, evaluated at Z=Y^p; it is not d/dY[He_c(Y^p)]. The ordinary leading p factors were retained before reduction.

Since c<p, He_c'=c He_(c-1) is coprime to He_c by downward recurrence, and He_c(0)=C_c!=0 because c is even. Thus (7.2) is nonzero at every residue root in (7.1), despite the multiplicity p in (7.1).

For the shifted f, each edge differs from the corresponding edge of T by value N. Telescoping an h-edge matching, with h-1 unchanged edges of value at least one, gives coefficient value at least N+h-1 in f-T at degree cp-2h. Because alpha>1/2, minimizing over 1<=h<=cp/2 gives

    weight_alpha(f-T)>=Q:=N+cp/2-1,
    weight_alpha(f'-T')>=Q-alpha.                    (7.3)

The derivative bound is taken before reduction. Since Q>F and Q-alpha>F-1/2 throughout c<p, the shifted tail has the same alpha polynomial and ordinary-derivative residuals as T. This is a precision comparison, not an identification of their actual roots.

## 8. All cp outer roots and their ordinary derivatives

At alpha scale, every root of A has value at least one, so monic factorization gives weight(A)=2N alpha and residual Y^(2N) after scaling by r^(2N). Matching bounds for the odd-degree polynomials g and M give

    weight_alpha(g)>=cp/2-1+alpha,
    weight_alpha(M)>=N-1+alpha.                       (8.1)

Indeed an h-edge matching in odd degree d has value at least h+(d-2h)alpha, minimized at h=(d-1)/2. No high-disk estimate for M is extended to this larger disk.

It follows from (8.1) that the correction a0gM lies strictly above the principal A f weight 2N alpha+F, by

    Delta=p^2-c(p-1)/2-1/p>0.                         (8.2)

Therefore the full, monic, degree-n polynomial has alpha reduction

    P_n(rY)/r^n -> Y^(2N) He_c(Y^p).                  (8.3)

All coefficients are integral after this scaling. The c nonzero residue locations in (8.3) have multiplicity p each. The ordinary Newton-polygon/distinguished-factor count gives exactly cp roots of value alpha, exactly p in each such residue class, counted with multiplicity. This is not a simple-root Hensel argument for the repeated residual. These roots are disjoint from every old high disk because alpha<1. Their count plus the 2N high roots is n, exhausting degree.

For the derivative fix any of these new roots xi. At v(xi)=alpha, A(xi) has exact value 2N alpha and is nonzero. Put R=a0gM/A, a rational function regular near xi. The matching bounds and ordinary derivative monomial estimates imply

    v(R(xi))>=V:=p^2+cp/2-1/p,
    v(R'(xi))>=V-alpha.                              (8.4)

For completeness, differentiate the quotient explicitly: its numerator terms are a0g'MA, a0gM'A and -a0gMA', divided by A^2. Each polynomial derivative loses at most alpha in its coefficientwise alpha bound, including A'>=2N alpha-alpha. This proves (8.4) without claiming A is invertible on the ENTIRE alpha disk, which contains its roots.

The exact gaps needed for (7.3)-(8.4) are

    V-alpha-(F-1/2)=p^2-c(p-1)/2-1/2-1/(2p)>0,
    Q-alpha-(F-1/2)=N-c(p-1)/2-3/2+1/(2p)>0.           (8.5)

They are positive already using c<=p-1. By (7.2), T'(xi) has exact value F-1/2 since the residue y=xi/r satisfies He_c(y^p)=0 and He_c'(y^p)!=0. Equations (7.3),(8.4),(8.5) therefore make f'(xi)-R'(xi) have that same exact value.

At a root, differentiation of P_n=A(f-R) kills A'(f-R) EXACTLY. Consequently

    P_n'(xi)=A(xi)(f'(xi)-R'(xi)),
    v(P_n'(xi))=2N alpha+F-1/2.                       (8.6)

All cp outer roots are simple. This proof establishes simplicity without specifying the finer splitting radius of their p-fold coarse residue classes.

## 9. p=3, exceptional cancellation, all phases, H and kernel

At p=3 only c=2 is permitted in this even sector. Then N=27,K=81,E=135/2,D=183/2,rho=5/2,alpha=5/6,F=5. There are 54 high roots with derivative 193/2 and six outer roots with derivative 99/2; P_60(0) has value 86. This is precisely inherited c=2, not a new p=3 case. The least high derivative gaps are 1,1,2. The outer derivative perturbation gaps in (8.5) are 19/3 and 71/3, respectively. No p>=5-only argument, division by 3, or exceptional omission is used.

The first genuinely new case p=5,c=4 has g's leading t-scale residual identically zero, because J_4=-5. Nevertheless the high derivative remains uniquely supplied by fA'. Here n=270, F=18, alpha=9/10, D=965/2, giving high derivative 1001/2, outer derivative 485/2, and constant value 443. This explicit cancellation is a positive stress test of the lower-bound-only treatment of g, not a characteristic-zero repeated-root exception.

Every proof uses actual t, e, integer recurrences, legal nonzero-edge specialization, and full coefficientwise comparisons. The only p-block mod-p truncation is at precision below e; the universal p-block and matching argument controls the actual mixed-characteristic polynomial. Hence every s>3 and every characteristic-zero primitive phase is covered, not merely finitely tested phases.

All roots of P_n have positive value and cannot be +/-2. In the exact identity

    H_n(v0^2)=v0^n P_n(v0+v0^(-1)),

the branch near v0=i gives a multiplicity-preserving correspondence of all P and H roots. Its two coordinate derivatives are units because p is odd; H_n(0)=1. At a root the exact ordinary derivative identity is

    H_n'=v0^(n-2)[(n/2)P_n+(v0-v0^(-1))P_n'/2].

The P_n term vanishes, and the remaining multiplier is a unit. Thus H_n is squarefree with the same rootwise derivative valuations. No equality of normalized P/H units is claimed.

Consecutive original P polynomials are coprime by backward propagation through the nonzero recurrence edges. The original Christoffel-Darboux identity at a root xi therefore gives

    sum_(j=0)^(n-1) P_j(xi)^2/w_j
       =P_n'(xi)P_(n-1)(xi)/w_(n-1) !=0.

These are algebraic squares, not absolute-value squares. No positivity, interlacing, altered kernel, FFT or cost inference is used. Injective algebraic p-adic embeddings transfer nonvanishing to the original characteristic-zero phases.

## 10. Boundary, fresh controls, and independent review

The precise unresolved middle-digit sector after combining this candidate with the accepted c=1 result is odd 3<=c<p. For odd c, C_c=0: f's high-scale constant-unit argument fails, and the outer Hermite residual includes a zero root. The remaining inner roots and derivative competition require additional work. This is a limitation of the present proof, not a repeated-root claim or rejection of previously accepted results.

Fresh controls are written specifically for this candidate. They reconstruct truncated original recurrence coefficients and ordinary derivatives, whole-block alpha and t residuals, first-deleted-tail cancellation coefficients, joining-subset bounds, and rational gap/count ledgers. Independent finite-characteristic fixtures test original transfer, ordinary differentiated transfer, H/P and algebraic-square CD identities. These are narrow falsification and transcription controls, not the universal proof and not an inference from good finite reduction to characteristic-zero squarefreeness. Bad finite reductions, if encountered, are retained as diagnostics rather than suppressed.

The source audit is read-only and checks exact source bytes and accepted manifest identities. It does not run a supplied source checker. The final machine-readable outputs record the actual finite ranges and counts. A separate reviewer must bind and accept the frozen final bytes; this candidate cannot accept itself. The author communicated the even-sector architecture before freeze, which should be disclosed in review. No public projection, repository/table write, global F020/F023 closure, arbitrary-degree theorem, p=2 or s<=3 statement, composite-order claim, historical novelty, or FFT-speed claim is made.

The completed normal and optimized mathematical runs each pass 72,275 explicit checks and have byte-identical output. They include all 11 even-(p,c) series cases at p=3,5,7,11; all 567 even-(p,c) rational ledgers through p=101; every joining subset in those 11 series cases; and 19 finite-identity phase/degree fixtures at p=3,5,7,s=4. The p=3 phase-70 fixture is retained even though the inherited c=2 work found bad reduction there: these controls test exact identities, not a universal good-reduction assertion. Source normal/optimized outputs are byte-identical and pass 182 explicit checks, including six complete source manifests with 30,8,40,10,13,19 entries, 34 documentary snapshots, and all 17 inherited original-location bindings.

One pre-freeze arithmetic transcription was corrected: the handwritten p=5,c=4 example initially substituted a wrong D and hence a wrong high-derivative number. The formulas and independent rational ledger give D=965/2 and high derivative 1001/2, now displayed correctly. No theorem, bound, cancellation claim, or test was weakened to make this correction.
