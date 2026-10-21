# Independent review: odd-leading even short tails in original F020

21 October 2026 UTC. This is a separate mathematical and byte-bound review. Acceptance applies only to the author manifest and report identified in VERDICT.json and SOURCE_BINDING.json. The author and inherited source files were read, not modified; none of their programs was imported or executed. All executable controls here were written afresh by this reviewer. There were no external writes and no essential mathematical repair supplied to the author.

## 1. Verdict and exact scope

ACCEPTED WITHIN THE EXACT STATED SCOPE.

Let p be prime, c odd with 3<=c<p, d even with 2<=d<p, r>=2, s>r, N=p^r, and q any characteristic-zero primitive p^s-th root. Retain the original recurrence P_0=1, P_1=X, P_(j+1)=XP_j-(1-q^j)P_(j-1), the original Gaussian-binomial H_n, and the original algebraic-square Christoffel-Darboux kernel, with n=cN+d. The original P_n and H_n are squarefree; the original kernel is nonzero at every P_n root. The new coverage is only even 4<=d<p. The d=2 theorem, all-leading d=0 theorem, odd tails, and every even-leading short-tail result are inherited and are not re-credited.

Set t=q-1 and v(t)=1 in an algebraic p-adic embedding. Write e=(p-1)p^(s-1), B=r(p-1)p^(r-1)/2, K=cN/2+cB, E=(c-1)N/2+cB, D=N+E-p, h=floor(r/2), beta=p^h and L=N/beta. The disk radius in valuation is rho=beta/2 if r is even and rho=p^(h-1)(2p-1)/2 if r is odd. With i^2=-1 and square-root branches near 1, the beta centers are x_a=i(q^(a/2)-q^(-a/2)), 0<=a<beta.

The accepted complete conclusions are:

- Each disk v(X-x_a)>=rho contains cL roots, first counted with multiplicity: (c-1)L boundary roots and L strict-interior roots. All beta disks account for cN high roots. Noncentral roots have value p^ord_p(a); central boundary roots have value rho.
- The central L strict-interior roots include exactly one simple root X=0 and L-1 nonzero roots. Individual deeper valuations of the nonzero interior roots are not asserted.
- There are exactly d further simple roots with value 1/2. If tau^2=t, the nonzero residues of X/tau are the d distinct roots of M_d(Z)=sum_u d!Z^(d-2u)/(2^u u!(d-2u)!).
- At every high root, including zero, v(P_n')=D+d/2 and v(P_(n-1))=N+E+d/2-1. The original kernel has value N-p.
- At each shallow root, v(P_n')=v(P_(n-1))=(n-1)/2 and the original kernel has value -2cB.
- The corresponding ordinary H derivative values agree, and z=-1 is its exact simple root corresponding to X=0.
- Both original monic discriminant values are cN(D+d)+d(d-1)/2.

There is no exceptional parameter left within this bounded sector, including r=2, p=5,c=3,d=4, and c=p-2,d=p-1. Excluded are c=1 as new credit, c>=p, d>=p, r=1, s<=r, arbitrary intermediate digits or degrees, composite orders, exact deeper nonzero interior depths, global F020/F023 closure, historical novelty, and FFT or cost claims. Exclusion does not assert those other cases false.

## 2. Evidence and independence

I first checked the recurrence transfer and the decisive valuation arithmetic from the original objects, while the candidate was available but before accepting any frozen bytes. I then inspected its complete proof and the inherited proofs. I do not claim that this derivation preceded all exposure to the candidate text. The endpoint, symbolic-tail, shallow, and cyclotomic controls use only newly written code; their results do not replace the uniform proof.

The exact dependency audit independently reads every manifest-listed byte and checks the exhaustive live inventory of eight accepted source packages, with four exact author-report/author-manifest acceptance pairs. Partial snapshots are explicitly identified as such and are compared byte for byte with their live sources. The original single-leading-digit archive is retained untouched; both its outer and accepted-theorem manifests are checked exhaustively, together with acceptance and verdict pins. Historical original-report identities and public-projection identities remain distinct and are connected by the archive's explicit acceptance mapping.

The primary coefficientwise authority is the accepted uniform odd-adjacent report, with author manifest 438eb219f3534b41caa13905423c21afb2ae9fb777a8acdfa9b93438d126e032 and accepted review manifest a7deb7b69007940e8c7e49155701eabd22e7f81b01ba8012c5c94ee97a68be35. The accepted odd-plus-two author manifest is db295d917b83f18dc36ddf2f708eadf9e3203f0b60c3ddb5852fbb91a6ee28c4, with review manifest 4cf46988f5cfac2432b1d8281432af8defa66334471b176156583da5a60e7316. These sources explicitly supply the full-disk original-derivative facts, not merely simplicity at neighboring degrees. The even-leading even-tail theorem supplies an attributed finite-tail method, not its incompatible zero-free geometry. The odd-tail package is an attribution boundary and corroborating scalar source, not an imported cancellation-lifting dependency.

## 3. Accepted input applies to the new root locus

Put A=P_(cN), M=P_(cN-1), and a=1-q^(cN). On each entire high disk, with its scaled coordinate Y and Zbar=alpha_a Y^L, alpha_a nonzero, the accepted input is

    wt(A)=K,  in(A)=u_A M_c(Zbar),
    wt(M)=E,  in(M)=u_M M_(c-1)(Zbar),
    wt(A')=D, in(A')=u_D M_(c-1)(Zbar),
    wt(M')>=E.

The scalars are actual nonzero residues; they are not presumed equal. The complete A initial has degree cL, with all higher coefficients strictly above the normalized weight. Since c is odd, both the M and A' initials have essential nonzero constant terms. The original Newton expansion for H_(cN-1) has equality indices k=lN, l=0,2,...,c-1. The ordinary A' double expansion has equality pairs k-l=p^2 and l=l0N over the same complete even set, including the constant pair and the r=2 endpoint. The accepted M' bound is an all-summand inequality, not a pivot-only inference.

The off-root identity H_j'=v0^(j-2)[(j/2)P_j+(v0-v0^(-1))P_j'/2], where H_j(v0^2)=v0^jP_j(v0+v0^(-1)), transfers the derivative information on whole disks. The j=cN prefactor term has value at least re+K>D. Thus A' may be evaluated at the new P_n roots, not only at old A roots.

The integer Hermite recurrence M_j=ZM_(j-1)+(j-1)M_(j-2) and ordinary derivative M_j'=jM_(j-1) show that M_c and M_(c-1) are coprime modulo p: a common root would propagate through units to M_0=1. Hence M_c is separable, with exactly one zero and c-1 nonzero roots, and M_(c-1) is nonzero on its entire root locus. At every new root with this residue, v(M)=E and v(A')=D, including all residual-zero interior branches.

## 4. Independent finite-tail derivation and uniform strict margin

Let d=2m and b_j=1-q^(cN+j). The original edges have v(a)=N with a/t^N tending to -c, and v(b_j)=1 with b_j/t tending to -j for 1<=j<d<p. All are nonzero because n<pN<=p^s.

Define T_0=1,T_1=X,U_0=0,U_1=1, with both sequences satisfying V_(j+1)=XV_j-b_jV_(j-1). Applying the original recurrence gives

    F=P_n=T_d A-aU_d M.

The U edge set starts with b_2, not b_1. For instance U_4=X^3-(b_2+b_3)X. Differentiation is ordinary in characteristic zero. With W=U_d'T_d-U_dT_d', direct expansion gives the exact fraction-free identity

    S=T_dF'-T_d'F=T_d^2A'-aWM-aU_dT_dM'.

This retains the square T_d^2, both corrections, and the subtraction of T_d'F. No X division or quotient target is introduced.

The nonadjacent-edge matching expansion gives lower bounds m-k on the valuation of the complete X^(2k) coefficient of T_d, and m-1-k on the complete X^(2k+1) coefficient of U_d. Cancellations improve these inequalities. T_d has the unique constant matching (-1)^m b_1b_3...b_(2m-1), whose normalized initial is C_m=(2m-1)!!, a unit for d<p. For x=wt(X)>=1 on any high disk, every nonconstant T term has weight greater than m. Therefore T_d has the exact fixed value m everywhere in the disk. The complete bounds are

    wt(U_d)>=x+m-1, wt(T_d')>=x+m-1,
    wt(U_d')>=m-1, wt(W)>=2m-1.

The perturbation aU_dM exceeds T_dA by N/2+x-1>0. The full residual root locus of F is therefore the accepted M_c(alpha_aY^L)=0, not a truncated or changed polynomial. At each root, the three witness values are

    D+2m exactly;
    at least N+E+2m-1 = D+2m+(p-1);
    at least N+E+x+2m-1 = D+2m+(p+x-1).

At X=0 the last term is zero. Both gaps are uniformly positive. Thus v(S)=D+2m and, because S=T_dF' at an F root, v(F')=D+m. No r=2 tie exists and no auxiliary coefficient is required to be a unit. This proves all high roots simple without differentiating the inseparable high residual.

The complete residual degree and closed-disk Newton/Weierstrass count give cL roots per disk, with (c-1)L boundary and L interior roots. Simple-root Hensel is not applied to Y^L. Distances between distinct centers have value at most p^(h-1)<rho, so the disks are disjoint. Original parity makes F odd and F(0)=0 exactly. The witness proves this zero simple, so it accounts for one, not all, of the central L interior roots. The exact count is (beta-1)cL+(c-1)L+(L-1)+1=cN.

## 5. Smallest endpoint and ordinary-derivative negative control

For p=5,c=3,d=4,r=2, N=25, B=20, E=85, K=97.5, D=105, m=2 and rho=2.5. The auxiliary linear coefficient of U_4 is initially 2+3=5, so it vanishes modulo 5. The direct original recurrence shows U_4'(0) has value 2 with initial 4, rather than the generic lower bound 1. Meanwhile T_4/t^2 has initial 3 and remains a unit.

With mu^2=t^5 and X=mu Y, the fresh complete control obtains

    A: weight 97.5, initial 4Y^15+2Y^5;
    M: weight 85, initial 4(Y^10+1);
    A': weight 105, initial 3(Y^10+1);
    F: weight 99.5, initial 2Y^15+Y^5;
    S: weight 109, initial 2(Y^10+1).

On the F residual root locus, Y^15+3Y^5=0, the last initial is nonzero by the complete M_3/M_2 coprimality. Thus the high derivative value is 107. At zero its normalized initial is 4, and the predecessor has value 111 with initial 4. The original kernel value is 107+111-198=20=N-p. The discriminant value is 75*(105+4)+6=8181.

Crucially, the entire-disk F' initial has weight 101 and polynomial 3Y^16+4Y^6. Therefore an off-root claim wt(F')=107 would be false. The candidate correctly restricts the final derivative value to its roots and uses the fraction-free subtraction. The independently derived ordinary A' scalar is +c, not the even-leading -epsilon scalar.

The sparse computation retains X degrees through 45 and t degrees through 120. Original edge matching forces the X^k coefficient of P_j to have raw t degree at least (j-k)/2. At X=t^(5/2)Y, the first omitted X degree has weight at least 131.5 in P_79 and 129 in its derivative, both above the witness target 109; omitted t terms have weight at least 121. Possible p-divisible coefficient carries have e>=100 and raw weight at least 41 in S, so value at least 141>109. For F' the carry bound is 139>107, and for A' it is 137>105. Thus all claimed initials are complete and the finite-characteristic calculation has explicit mixed-characteristic margins. It is not a finite-characteristic squarefreeness proxy.

## 6. Original predecessor, shallow roots, kernel, H and discriminants

The exact tail determinant is T_(d-1)U_d-U_(d-1)T_d=product_(j=1)^(d-1)b_j. At a high F root, T_d alone is invertible, giving

    P_(n-1)=aM product_(j=1)^(d-1)b_j/T_d.

Its value is N+E+m-1. The formula includes X=0 and every auxiliary-cancellation class. Also v(w_(n-1))=cN+2cB+d-1. In the original algebraic-square CD identity, the kernel at a root is P_n'P_(n-1)/w_(n-1), so its high value is N-p. This is not a positive or Hermitian kernel and is not the kernel of F/X.

For tau^2=t, normalize Q_j(Z)=tau^(-j)P_j(tau Z) and separately D_j(Z)=tau^(1-j)P_j'(tau Z). Their original recurrence and ordinary differentiated recurrence are integral; reduction gives the Hermite recurrence with edge j modulo p. The integer formula gives M_p=Z^p, and restarting at p-multiples gives M_(ap+b)=Z^(ap)M_b. Consequently

    Q_n reduces to Z^(cN)M_d(Z),
    D_n reduces to d Z^(cN)M_(d-1)(Z).

Since d<p and M_d has the unit constant C_m, it has d distinct nonzero residual roots, and the derivative is nonzero at each. Ordinary simple-root Hensel now applies legitimately, giving exactly d shallow simple roots with value 1/2. The predecessor reduction is Z^(cN)M_(d-1), nonzero there. Its value and the derivative value are both (n-1)/2, yielding kernel value -2cB. The cN high roots and d shallow roots exhaust the monic degree n.

Every P root has positive value or is zero, so is not +/-2. Near v0=i, X=v0+v0^(-1) and z=v0^2 have unit coordinate derivatives. The exact H/P identity preserves multiplicity and bijects the n P roots to n H roots. At a root, the prefactor derivative term vanishes exactly, leaving a unit multiplier with residue i^(n-1), so the ordinary derivative valuations agree. The root X=0 maps to the simple H root z=-1. The discriminant calculation is the sum of the ordinary derivative valuations:

    cN(D+m)+d(n-1)/2 = cN(D+d)+d(d-1)/2.

Every step uses the actual t=q-1 and e for an arbitrary primitive phase. The accepted inputs, edge units, and strict inequalities hold for every s>r. An injective algebraic p-adic embedding transfers the resulting nonvanishing to the original characteristic-zero phase.

## 7. Fresh executable controls and their limits

The independent controls check symbolic nonadjacent matchings, complete fraction-free identities, constant products, and tail determinants for even d=2,4,6,8,10; all derivative corrections are retained. Hermite coprimality and all allowed tail constants are tested for primes through 37. The auxiliary-cancellation sample includes p=5,d=4; p=11,d=6; p=13,d=12; p=17,d=16; p=29,d=28; p=31,d=8; and p=37,d=36. This is a finite diagnostic, not an exhaustive exceptional-prime classification, which is unnecessary because the proof uses lower bounds.

Separately evolved full sparse shallow polynomials and ordinary derivatives pass at (p,c,r,d)=(5,3,2,4), (5,3,3,4), (7,3,2,4), (7,5,2,6), (11,9,2,10), and (13,11,2,12), together with predecessor, count, kernel, and discriminant arithmetic.

A second control uses actual primitive 125th roots at all 100 phases in F_4001 and F_251 for n=79. It constructs P from the original recurrence and H independently from Gaussian-binomial coefficients, checks the complete H/P coefficient identity, checks ordinary derivative gcds, and checks the original algebraic-square kernel identity modulo P and predecessor coprimality. Every phase modulo 4001 is squarefree for both original P and H, and the kernel is coprime to P. Modulo 251, phase 26 has a degree-two derivative gcd for both P and H and a degree-two kernel gcd; the other 99 phases do not. This is a bad finite reduction, not a characteristic-zero exception. It is retained explicitly as a negative control against confusing arbitrary finite-field squarefreeness with the uniform theorem.

Deliberately wrong formulas are rejected: starting U with b_1, omitting the M' correction, unsquaring T in the witness, declaring the odd target zero-free, asserting the high root derivative value off root, and borrowing the even-leading scalar. Normal and optimized Python runs must be byte-identical. All these controls and the exact source-byte audit are frozen in this review; finite controls corroborate, but do not prove, the uniform result.
