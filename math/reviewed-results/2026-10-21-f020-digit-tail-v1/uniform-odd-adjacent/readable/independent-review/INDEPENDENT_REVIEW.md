# Independent review: uniform odd-leading adjacent degrees

Review date: 21 October 2026 UTC. Verdict: ACCEPTED WITHIN THE EXACT STATED SCOPE. Reviewed author manifest: 438eb219f3534b41caa13905423c21afb2ae9fb777a8acdfa9b93438d126e032. Reviewed author report: 57ed78b499b62abe3b440ba8875736ebe12e1be2b29f35d1effce8e041b2fbec. Source pins and verdict are also recorded in VERDICT.json and SOURCE_BINDING.json. This review is independent of producer programs: only newly authored reviewer checks were executed. No producer, dependency, or accepted-source file was changed. No external write was made.

## Exact scope and normalization

The reviewed family is odd 3 <= c < p, p prime, r >= 2, s > r, every characteristic-zero primitive p^s-th root q, and degree n=cp^r+1. In particular p>=5. The original recurrence is P_(j+1)=X P_j-(1-q^j)P_(j-1); H is the original Gaussian-binomial polynomial; the kernel uses algebraic squares and the original q-factorial denominators.

Put N=p^r, B=r(p-1)p^(r-1)/2, K=cN/2+cB, E=(c-1)N/2+cB, D=N+E-p. Write A=P_(cN), M=P_(cN-1), a=1-q^(cN), and F=P_n. Crucially F is even and equals XA-aM. It is not P_n/X and has no exact zero.

The accepted result is complete for this bounded family, not merely a first-layer criterion: P_n and H_n are squarefree and the original algebraic-square Christoffel-Darboux kernel is nonzero at every P_n root. The c=3 case is inherited, not newly credited. No c>=p, r=1, s<=r, arbitrary tail or intermediate digit, composite-order, global F020/F023, complexity, or historical-novelty extension is included.

## 1. Accepted input and the new neighbor argument

The accepted single-leading-digit source genuinely covers every 1<=c<p, including odd c. It supplies the coefficientwise half-W cap, complete ordinary derivative residual, block units, and original coordinate identity. Its derivative equality set for odd c includes m=0 as well as m=2N,...,(c-1)N. Thus the constant derivative residual on the odd interior branch is present. These are not even-c conclusions silently extended to odd c.

For b=cN-1, W(b)=2E and the Newton bound is E. Equality requires k=lN with even l=0,2,...,c-1. Every such term attains equality. Under Cminus=omega^(c+1)/(a Q_((N-1)/2)), their sum is c M_(c-1)(Zbar), including its nonzero constant term. The proof retains k=0, which is necessary for the even neighbor.

For the full ordinary neighboring derivative, the subtracted bracket is bounded by E+p^ord_p(j)-W(j)/2. Only j=1,p can reach E+1/2. Parity then makes m odd. If m is not an N-multiple, the half-W bound is strict. If m=lN with odd l, the N-level floor carry makes 2W(a0)<W(2a0). The half-integer lattice gives bracket <=E. Thus weight(M')>=E for all derivative summands, not just selected pivots.

The H/P identity transfers these bounds through unit coordinate derivatives. For A', its extra prefactor has value at least re+K>D. Consequently the accepted ordinary derivative initial is valid coefficientwise off A's root locus, where it is needed at new F roots.

## 2. Complete root partition and separated derivatives

M_c and M_(c-1) are coprime modulo p by their integer recurrence and p>c. The odd M_c has exactly one simple zero residual root. On a noncentral disk, the perturbation aM is strictly higher than XA and the F residual has degree cL, with zero multiplicity L. On the central disk it is Y M_c(alpha Y^L), degree cL+1, with zero multiplicity L+1. Thus each noncentral disk has (c-1)L boundary and L strict-interior roots; the central disk has (c-1)L boundary and L+1 strict-interior roots.

These are closed-disk Newton/Weierstrass counts with multiplicity, not simple-root Hensel lifting of the inseparable Y^L substitution. Their disjoint total is cN+1, so no root class is omitted. M(0) has exact value E; hence F(0) has exact value N+E and none of the central interior roots is zero.

At every F root, including both interior classes, the residual equation is M_c(Zbar)=0. Coprimeness therefore gives v(M)=E and v(A')=D on the entire root locus. At a nonzero root of valuation x,

    F'=aM/X+XA'-aM'.

The first two terms have values N+E-x and x+D; the last has value at least N+E. Except when 2x=p, the smaller term is unique and

    v(F')=min(x+D,N+E-x).

No noncentral root has 2x=p. Central interior roots have x>rho>=p/2. For r>=3, rho>p/2, so this proves all-root simplicity without any additional criterion. The sole possible tie is the r=2 central boundary.

## 3. The genuine first-layer obstruction

For r=2 set d=p(p-1)/2, mu^2=t^p, X=mu Y, U=Y^2, and S=K+p/2. The actual odd-parity scalars give

    A/(t^(cB)mu^(cp)) -> -epsilon M_c(Y^p),
    M/t^E -> -M_(c-1)(Y^p), epsilon=(-1)^((p-1)/2).

Writing M_c(Z)=Z R_c(Z^2), the actual F=t^S f(U) initial is

    f(U) -> -epsilon U^((p+1)/2) R_c(U)^p.

The correct off-root polynomial is J=XF'-F=X^2 A'+aM-aXM', not F' itself. Its initial is

    J/t^(N+E) -> c(Y^2+1)M_(c-1)(Y^p).

Since the neighboring Hermite factor is a unit at F residual roots, the first-layer obstruction is exactly p dividing b_c=R_c(-1). If it occurs, R_c has a simple root at -1, and precisely two Y locations, each of multiplicity p, are affected. Thus exactly 2p roots require another layer. This establishes a vanishing initial, not characteristic-zero nonsimplicity.

Independent arithmetic gives b_3=2, b_5=6, b_7=20, b_9=28, b_11=-936. The allowed pair c=11,p=13 really is exceptional. For b_m=R_(2m+1)(-1), the recurrence b_m=2(2m-1)[b_(m-1)-(m-1)b_(m-2)], b_0=1,b_1=2, has v_2(b_m)=ceil(m/2). Hence every such integer is nonzero. This supplementary arithmetic is not needed for the final all-prime theorem, because the second layer resolves all allowed exceptions.

## 4. Uniform second-layer bounds and odd operator

On the central boundary, the exact Newton-factor value is T0(m)=m+(p/2-1)ceil(m/p). If m=lN+ap+b with 0<=a,b<p,

    2(T0(m)-W(m)/2)=a(p-1)+b+(p-2)1_(b>0).

Nonzero slack is at least g=(p-1)/2>1. With odd c, the neighboring pivots are even k/N, including zero; the ordinary A' pivots have j=N and even m/N, also including zero; the A pivots have odd k/N. Every nonpivot has gap at least g for M and A', and at least d+g>p for A. The full M' bound remains >=E. These exact parity sets and inequalities control all terms needed at relative order one.

The grouped-product identity in characteristic p gives N_N=N_p^p(1+error>p) and C0=-t^N D0^(2p)(1+error>p), with C0 the product of odd edges through 2N-1. The p-unit products R0 and D0 have matching normalized expansion -(1+t/2+O(t^2)). Using (z+1)^2=-zt^p at U=-1 gives v(N_N^2+C0)>W(N)+p.

Every odd leading pivot then reduces, with error >K+p, to its term in

    N_N C0^((c-1)/2) R_c(-1).

If p divides b_c this is zero in characteristic p. Including every nonpivot and the aM correction gives formal order >S+p for F at U=-1.

The mixed-characteristic transfer is valid even when e<S+p. Every raw integer coefficient monomial in P_(2m0), m0=(cN+1)/2, has t degree at least m0 after X^2=-t^p. Thus all formally vanished coefficients have actual value at least e+m0, and

    e+m0-S >= (p-c)B-(p-1)/2 >p.

This is the necessary odd coefficient lattice, not the even quotient lattice. It proves v(f(-1))>p for all s>2 and all primitive phases.

The derivative bound to use is weight(2U f_U-f)>=d, obtained from J. A global bound weight(f_U)>=d would be false, because the derivative of the actual residual has a nonzero U^((p-1)/2)R_c(U)^p term. After h(V)=f(-1+V)=sum a_j V^j, the controlled coefficient is

    -2(j+1)a_(j+1)+(2j-1)a_j.

Since a_0 has value >p and d>p, induction for j=0,...,p-2, dividing only by units, proves v(a_j)>p for 1<=j<p. The coefficient a_p is a unit. An exceptional root with 0<v(V)<=1 would make a_pV^p uniquely smallest, contradicting h(V)=0. Hence every one of the 2p affected roots satisfies v(U+1)>1, without presuming simplicity.

## 5. First nonzero correction and the original derivative unit

Pairing all ordinary A' pivots with the corresponding even-neighbor pivots gives the same scalar ratio a z^(N-1)Q_A*/a_N through relative order one. All omitted terms are higher by g>1. After the exact coordinate identity, whose prefactor is separately higher,

    X^2 A'/(aM)=U(1-t/8)+error>1.

The first correction comes from the actual mixed-characteristic factorial Q_A*/(-t^B)=1-t/8+error>1. Its p-unit edge linear sum is (p^2-1)/8=-1/8 modulo p; the p-divisible edges have no linear contribution. The coordinate factor and a_N normalization contribute no order-one term.

At an affected root, U=-1+error>1 and XM'/M has value >=p/2>1. Consequently the bracket in J=aM[1+X^2 A'/(aM)-XM'/M] is t/8+error>1. It follows that

    v(J)=N+E+1, v(F')=K+d+1.

The actual neighbor unit is -M_(c-1)(Y^p). At Y^2=-1, the Hermite derivative identity gives cM_(c-1)(Y)=-2R_c'(-1). Therefore

    J/t^(S+d+1) -> -R_c'(-1)/4,
    f_U/t^(d+1) -> R_c'(-1)/8 at F roots.

R_c'(-1) is automatically a unit. Under the actual scalar t^(S+d+1)/mu, the original F' unit is Y R_c'(-1)/4, nonzero at both signs of Y. Unlike the even quotient theorem, this original derivative unit is sign-dependent. The report correctly keeps the off-root J and root-only f_U statements distinct.

There is thus no residual arithmetic exclusion after this layer. In particular, the c=11,p=13 first-layer cancellation is resolved rather than denied.

## 6. Central interior depth, original H, kernel, and discriminants

At U=0, f has residual zero multiplicity m1=(p+1)/2 and constant coefficient of value d. The operator bound makes every coefficient below degree m1 have value >=d, because 2j-1 is a p-unit there. The coefficient at m1 is a unit. The Newton polygon therefore has the segment (0,d) to (m1,0), giving p+1 X roots of exact value p^2/(p+1). This holds irrespective of the first-layer obstruction. No analogous exact r>=3 depth is claimed.

All root derivatives are now finite and nonzero. The original H/P coordinate maps have unit derivatives near the roots, and the prefactor term vanishes exactly at a root. They preserve multiplicities and ordinary derivative valuations, proving H squarefree as well. All original recurrence edges below n are nonzero; backward recurrence excludes a common root of P_n and P_(n-1). The original diagonal Christoffel-Darboux identity then has nonzero right side P_n'P_(n-1)/w_(n-1). Its squares are algebraic, not absolute-value squares.

Exactly cN(p-1)/p roots have x=1, all other roots have x>=p/2, and the sum of all root values is N+E. Summing the separated derivative formula gives cN(N+E)-[cN(p-1)/p](p-2). Exactly 2p exceptional r=2 derivatives gain one, giving the report's discriminant correction +2p I. The same sum holds for H. All arguments use arbitrary primitive t=q-1 and the full e bound, so no single-phase or minimum-s specialization is silently extrapolated.

## 7. Independent controls and limitations

The reviewer authored three new programs and never imported or executed supplied producer or dependency code. The reproducible controls include:

- Obstruction recurrence and exact 2-adic nonvanishing through c=61; exact small factorizations and Hermite resultants; original recurrence J and even constant-product identities.
- Complete ordinary derivative and neighboring Newton index checks in seven fixtures, including c=11,p=13 and r=3 cases.
- Actual original cyclotomic P recurrence controls at (c,p,r,s,phase)=(5,7,2,3,2), (7,11,2,3,3), (11,13,2,3,2), and (3,5,3,4,2). The cyclic q ring is projected to the full cyclotomic basis before exact Pascal substitution. X truncation is closed under the recurrence and occurs only beyond the tested valuation threshold. Ordinary derivative integer factors are retained before valuation. These controls check actual A,M,A',M',F,J initials and central Newton counts, including the exceptional first-layer gcd.
- A separate original parity-recurrence implementation carries all U=-1 jets through degree p. For c=11,p=13,s=3 and primitive phases 1,2,-1, it finds v(J(-1))=2731=S+d+1 and unit 5=-R'_11(-1)/4 mod13. All coefficients below V^13 have value >S+p; V^13 is a unit after t^S normalization. Nonexceptional c=9,p=11 and c=7,p=11 serve as negative controls.
- Complete central nonpivot checks for (c,p)=(3,5),(5,7),(7,11),(9,11),(11,13),(15,17), exact grouped-product divisibility and Q first-order coefficients at p=5,7,11,13, and odd lattice margins across bounded prime/digit fixtures.

All numerical work is exact integer/modular arithmetic. The canonical cyclotomic t-basis weights j+e*v_p(coefficient) are distinct modulo e, and p/t^e=-1 is included in initials. Precision and int64 accumulation bounds are explicitly checked. Controls are bounded falsification diagnostics, not a substitute for the unlimited-family proof above.

The only pre-freeze editorial correction requested by this reviewer was to avoid calling f(U) itself even; F(X), not generally f(U), is even. No essential mathematical repair was required. Arithmetic observations and control results were shared during construction; the independently derived proof was checked against the final frozen author bytes before acceptance.

The final source audit verified every one of the 59 candidate entries, every one of the 35 inherited c=3 author entries, and all 453 and 408 entries in the two current leading-digit public archive inventories. Historical manifests and projected public reports were kept distinct through the accepted identity mapping. The independent clean cold replay matched all three result files byte-for-byte under the declared resource caps. Five disposable-fixture inventory negatives were rejected.
