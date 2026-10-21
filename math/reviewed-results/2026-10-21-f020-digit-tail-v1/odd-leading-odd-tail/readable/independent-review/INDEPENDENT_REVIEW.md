# Independent review: odd leading digits with odd short tails

Review date: 21 October 2026 UTC. Verdict: ACCEPTED WITHIN THE EXACT STATED SCOPE. The frozen byte binding is recorded in VERDICT.json and SOURCE_BINDING.json. Only new reviewer-authored programs were executed. No candidate, dependency, or accepted source program was run; no such source was changed; no external write was made.

Reviewed candidate manifest SHA-256: 82f93c18acf191ac58985357666e748f7e944fad3538c4a908faae811c87b392. Reviewed candidate report SHA-256: 692ac1ef6a5958c2ba29fecd84d309f1831f789acf45736467972eb3b256e890.

## Scope and accepted inventory

The reviewed theorem is p prime, odd 3 <= c < p, odd 1 <= d < p, r >= 2, s > r, N=p^r, n=cN+d, and every characteristic-zero primitive p^s-th root q. The newly accepted part is odd d >= 3. The original recurrence is P_(j+1)=X P_j-(1-q^j)P_(j-1), the H polynomial is the original Gaussian-binomial one, all derivatives are ordinary characteristic-zero derivatives, and the diagonal kernel uses algebraic squares with the original q-factorial denominators.

The live source inventories and exact author/reviewer acceptance bindings were independently read and hashed. The accepted cN result already includes odd c. The odd d=1 and d=2 scopes are separately accepted. The even-c odd-tail acceptance explicitly excludes odd c, so it cannot itself accept the new sector. Its parity-free scalar product mechanism and short-tail jets are attributed inputs, not authority to copy even-c parity identities. The current packet correctly credits d=1 as inherited and only odd d>=3 as new coverage relative to these supplied acceptances.

The normalization is beta=p^floor(r/2), L=N/beta. The earlier detached-summary typo is not adopted. This review accepts neither arbitrary degrees/intermediate digits nor global F020/F023 closure, historical novelty, FFT/cost consequences, or future public packaging.

## 1. Coefficientwise input, legal transfer, and all roots

The accepted odd input gives A=P_(cN) odd, M=P_(cN-1) even, wt(A)=K, wt(M)=E, wt(A')=D=N+E-p, and wt(M')>=E on every full high disk. Its A residual is M_c, whereas M and A' have the nonvanishing neighboring residual M_(c-1) at every M_c root. The constant M and A' pivots are present. These are off-root ordinary derivative statements, with the H/P prefactor separately bounded; the proof does not differentiate an inseparable residual.

The finite tail identity is P_n=TJ, J=XA-a*kappa*M, a=1-q^(cN), T=f_d/X, V=g_d, kappa=V/T. T and V are even polynomials with respective constant initials C=d!! and Btail=(d-1)!! after scaling by t^m, m=(d-1)/2. The V matching edge set starts at 2. Since all these tail factors are below p, T/t^m and V/t^m are analytic units on every high disk. Their inversion is legal even at the strict-interior roots. J is correctly treated as a restricted analytic function, not falsely as a global polynomial.

The perturbation aVM is higher than TXA by N/2-x_disk>0. The complete high reductions therefore give cL roots in each noncentral disk, including (c-1)L boundary and L strict-interior roots, and cL+1 roots centrally, including (c-1)L boundary and L+1 strict-interior roots. These are Weierstrass counts with multiplicity, not simple-root Hensel lifts of Y^L. The disjoint total is cN+1. At zero, P_n(0)=-aV(0)M(0) has exact value N+E+m, so there is no zero root.

Independently evolving the original P recurrence and its ordinary derivative at X=tau Z, tau^2=t, yields Z^(cN)M_d(Z) and d Z^(cN)M_(d-1)(Z). Only the d-1 nonzero simple M_d residues are Hensel lifted. They give the remaining roots, all with value 1/2 and derivative value (n-1)/2. Thus (cN+1)+(d-1)=n, and no zero-residue or shallow class is omitted.

At every high root, including both sorts of strict-interior root, v(M)=E and v(A')=D. Using J=0 before simplifying the ordinary derivative gives the four terms with values/bounds x+D, N+E-x, N+E, and N+E+x-1. Except when 2x=p, the smaller of the first two is unique. Noncentral x is an integral power of odd p; central x>=rho>p/2 for r>=3. Hence only the r=2 central boundary can cancel. All other original P derivative values are m+min(x+D,N+E-x).

## 2. Correct odd witness and both lift orders

The exact witness is XJ'-J=aM Qstar, with

    Qstar=X^2 A'/(aM)+kappa-kappa X M'/M-X kappa'.

The corresponding fraction-free polynomial is XT P_n'-(T+XT')P_n. This retains the extra -J term. Replacing it by the even-c J' operator or claiming a global bound on j_U is invalid. On a root the identity is P_n'=T(aM/X)Qstar, and all divisions are justified by the preceding unit statements.

For r=2, X=mu Y, mu^2=t^p, U=Y^2, the actual odd parity scalars imply boundary residual R_c(U)^p=0 and Qstar residual U+alpha, alpha=Btail/C. Thus the obstruction is exactly R_c(-alpha)=0 modulo p. R_c is separable and alpha is nonzero, so exactly two Y locations, with p roots each counted with multiplicity, are affected. A vanishing first residual is not declared to be a repeated characteristic-zero root.

The scalar product argument genuinely handles arbitrary alpha. The grouped-product errors are at least p(p-2)/2 and p(p-2); the R0/D0 products agree through linear order for the first lift and quadratic order for the second. These margins exceed p for p>=5 and 2p for p>=7. Summing all odd A pivots gives N_N*C0^((c-1)/2)*R_c(N_N^2/C0), not the even-c expression. Every omitted A term has gap at least delta+g, and the M/A' gaps are at least g, with delta=p(p-1)/2 and g=(p-1)/2. The full scalar numerator P_n therefore vanishes to value greater than S+m+bp at X^2=-alpha t^p.

The mixed-characteristic transfer uses the original even target P_n. Every raw monomial at that scalar has t-degree at least n/2. Consequently the coefficients killed modulo p have actual value at least e+n/2, and

    e+n/2-(S+m) >= (p-c)B-(p-1)/2 > bp.

This margin is valid at c=p-2 and the largest d=p-2. In particular the d-dependence cancels correctly; the proof does not import the even-c quotient lattice or assume e>S+m+bp. It is uniform for all s>2 and primitive phases.

Writing J(mu Y)=t^S j(U) gives residual -epsilon*U^((p+1)/2)*R_c(U)^p and the coefficientwise operator bound wt(2U j_U-j)>=delta. After translation U=-alpha+V, the controlled coefficients are -2alpha(l+1)h_(l+1)+(2l-1)h_l. The scalar bound and induction through l=p-2, dividing only by units, force all h_l for l<p above bp, while h_p is a unit. A root with 0<v(V)<=b would make h_p V^p uniquely smallest. This proves v(U+alpha)>b for all 2p affected roots before assuming simplicity.

Pairing every even-index A' pivot with its corresponding M pivot gives the full ordinary ratio U(1-t/8+9t^2/128)+error>2 for p>=7. At p=5 only the first-order accuracy is used, since g=2. The independently verified tail ratio is alpha[1+mt/6+m(7m-27)t^2/360]+error>2. The two other bracket terms have strictly higher order. Thus the first correction is alpha(2d+1)/24. If it vanishes, necessarily p=2d+1=4m+3>=7; the second is -alpha/320, a unit. No third unresolved cancellation remains.

The actual odd derivative units, normalized by t^(N+E+m+b)/mu, are Btail*Y*R_c'(-alpha)*(2d+1)/12 for b=1 and -Btail*Y*R_c'(-alpha)/160 for b=2. They follow from cM_(c-1)(Y^p)=-2alpha R_c'(-alpha); there is no copied even-c Legendre-symbol factor. Both signs of Y remain nonzero. At d=1 the first unit recovers the accepted odd-adjacent unit.

## 3. Interior geometry, original kernel, and discriminants

At U=0 the same odd operator forces every coefficient below degree (p+1)/2 to have value at least delta. The constant has exact value delta and that degree's coefficient is a unit. The single lower Newton segment gives exactly p+1 central strict-interior X roots of value p^2/(p+1), including the cases with a separate boundary obstruction. Restricted analyticity of J suffices; T has no roots on the disk. No individual deeper interior depths for r>=3 are accepted.

The exact tail determinant gives, at a high root, P_(n-1)=aM*product_(j=1)^(d-1)b_j/(XT), with value N+E+m-x. At a shallow root the predecessor has value (n-1)/2. Combining this with v(w_(n-1))=cN+2cB+2m proves the claimed original kernel values N-max(p,2x)+b I_affected and -2cB. They are finite. Independently, common roots of P_n and P_(n-1) would propagate through nonzero recurrence edges to P_0=1.

The original H/P coordinate map is an isometry near each root, and its derivative prefactor vanishes exactly at the root. Hence original H multiplicities and ordinary derivative values agree. No algebraic square is replaced by a modulus square. Every phase is covered by its algebraic p-adic embedding, the same integer/rational coefficient lattice, and e=(p-1)p^(s-1).

The high roots have total valuation N+E; precisely cN(p-1)/p have x=1. Summing the checked high derivative formula, the shallow values, and the 2p exceptional corrections gives the claimed discriminant

    cN(N+E)-[cN(p-1)/p](p-2)+m(2cN+d)+2p*b*I.

Thus the kernel and discriminant refinements are accepted, not only squarefreeness.

## 4. Independent evidence and limits

Fresh independent controls verify maximal-matching jets for m=1..17; obstruction arithmetic in the odd sector for primes through 43; all ordinary derivative summands in five parameter cases, including r=3 and c=p-2; and the original shallow polynomial and separately differentiated recurrence. No supplied program is imported or executed.

A direct original characteristic-p P/P' scalar recurrence, followed by the complete fraction-free Qstar bracket, verifies two complementary exceptional cases. For p=7,c=3,d=3, P_150 has scalar value 225, above the required 218, and Qstar has value 2 and unit 5=-alpha/320. For p=13,c=5,d=11, P_856 has scalar value 1292, above the required 1227, and Qstar has value 1 and unit 5. These bounded diagnostics check both lift orders and all bracket terms. They are not substitutes for the uniform proof or numerical tests at selected primitive phases.

No essential mathematical repair was supplied by this reviewer. The accepted bounded sector has no unresolved arithmetic exclusions. Outside it remain c>=p, d>=p, even tails as new coverage, r=1, s<=r, arbitrary intermediate digit strings/degrees, composite orders, global closure, exact deeper r>=3 interior geometry, historical novelty, and FFT/cost assertions. Separate public packaging, upload, or repository acceptance is not implied by this local proof review.
