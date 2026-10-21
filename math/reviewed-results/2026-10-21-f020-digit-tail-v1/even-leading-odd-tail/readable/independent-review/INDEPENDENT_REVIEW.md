# Independent review: even leading digits with odd short tails

## Verdict and scope

ACCEPTED WITHIN THE EXACT STATED EVEN-LEADING, ODD-TAIL SECTOR.

This review binds the author candidate `f020-even-leading-odd-tail-candidate-20261021_v1`, author manifest SHA-256 `0eefd9ffec434bd8d05eb8c5143a9025b7826f351863777867d7b27bb277603c`, and author report SHA-256 `2736127334ee95a7090f1ea293b05bdf61a7fc5f9f4afb1b996395b4e9c7fa37` (26,968 bytes). No essential mathematical repair was required by this review. No author file, accepted source, or external service was changed.

The accepted theorem is: if p is an odd prime, c is even with 2 <= c < p, d is odd with 1 <= d < p, r >= 2 and s > r, then the ORIGINAL P_(cp^r+d) and H_(cp^r+d) are squarefree at every characteristic-zero primitive p^s phase. The original algebraic-square Christoffel-Darboux kernel is nonzero at every P root.

Relative to the accepted general-c adjacent family and c=2 odd-tail family, the added range is c >= 4 and odd d >= 3. Those predecessors are inherited, not counted again. The accepted even-tail theorem is not used to infer an odd-tail theorem. The p=3 case is necessarily c=2,d=1, and its r=2 central derivative value 76/3 is inherited from the accepted original P_19 theorem. The new first- and second-correction argument is not applied at p=3.

This is not an arbitrary-n or arbitrary-digit theorem. No acceptance extends to odd c, c >= p, d >= p, r=1, s <= r, composite phase orders, global F020/F023 closure, FFT/cost consequences, or historical novelty.

## Exact new lifting statement

Put N=p^r, B=r(p-1)p^(r-1)/2, K=cN/2+cB, E=(c-1)N/2+cB, D=N+E-p. For d=2m+1 set C=(2m+1)!!, Btail=(2m)!!, and alpha=Btail/C, a rational p-unit. Write M_c(Z)=R_c(Z^2) in the author's positive Hermite convention.

All r>=3 roots and all noncentral r=2 roots are resolved by unequal valuations of the complete ordinary derivative terms. At r=2, the central leading obstruction is exactly R_c(-alpha)=0 modulo p. If it holds, precisely 2p X roots are affected, counted with multiplicity before simplicity is proved. The residual gcd degree is only two; it is not the lifted root count.

For every affected root and p>=5, with X²=t^p U and delta=p(p-1)/2:

- If p does not divide 2d+1, v(U+alpha)>1 and v(P_n')=K+delta+m+1.
- If p divides 2d+1, necessarily p=2d+1>=7, v(U+alpha)>2 and v(P_n')=K+delta+m+2.

The normalized derivative units are respectively

    -Btail chi(alpha) R_c'(-alpha)(2d+1)/12,
     Btail chi(alpha) R_c'(-alpha)/160,

where chi(alpha)=alpha^((p-1)/2) in F_p. Separability makes R_c'(-alpha) a unit, and all other factors are units in the indicated cases. No unresolved exception remains inside the accepted sector. No exact deeper root depth is asserted.

The new p=5,c=4,d=3 boundary is explicitly covered: alpha=4 modulo 5 and R_4(-alpha)=0. It requires the first-order lift and is not a c=2 predecessor. The second-order derivative ratio is deliberately not claimed for p=5, where the nonpivot gap equals two rather than exceeding it.

## Independent reconstruction of the uniform proof

### 1. Original recurrences, continuants, and geometry

The exact short-tail identity P_(cN+d)=f_d A-a g_d M follows from the original recurrence, with A=P_(cN), M=P_(cN-1), a=1-q^(cN). For odd d, T=f_d/X, V=g_d and G=M/X are even polynomials, and P_n/X=TJ where J=A-a(V/T)G.

The matching formulas have the correct different edge starts: T uses indices 1,...,2m, while V uses 2,...,2m. Their high-disk constants are C and Btail. Since every factor is below p, these are units even at the largest allowed odd tail d=p-2. All smaller matchings gain a positive power of X²/t. Therefore T/t^m is an analytic unit on the entire high disk, kappa=V/T is analytic, and wt(kappa')>=x-1 for x=wt(X)>=1.

The perturbation relative to T A gains N/2-x>0, including the central disk. Thus all high-disk residuals and their Weierstrass counts are unchanged. There are beta disjoint disks with cL boundary roots each, a total cN before simplicity. The central constant gives a simple exact zero of P_n with derivative value K+m. The separate original low recurrence and its ordinary derivative give d-1 simple nonzero low roots of value 1/2. Their counts sum to 1+(d-1)+cN=n. No simple-root Hensel argument is misapplied to an inseparable high residual.

All indices are legal: n=cN+d<pN<=p^s, including c=p-1,d=p-2. Source Q exponents are at most cN. Hence all recurrence edges and every used denominator are nonzero.

### 2. Every derivative term and every leading-digit pivot

Ordinary differentiation gives exactly

    J'=A'-a kappa M'/X+a kappa M/X²-a kappa' M/X.

At a high root, P_n'=X T J'. The four values or lower bounds are D, N+E-x, N+E-2x, and N+E-1. The middle and final competitors are strictly above the minimum of the first and third. A tie requires 2x=p, which occurs only centrally at r=2. This proves all r>=3 and all noncentral assertions without using any lift.

The accepted coefficientwise authority is applicable off the old polynomial's roots. Its A and M initials involve M_c and M_(c-1), which are coprime because backwards propagation has unit coefficients 1,...,c. Thus M has exact value E on every new residual root locus, not merely at the old roots. R_c is separable and has nonzero constant.

At r=2 the exact central slack is

    2 Delta(lN+ap+b)=a(p-1)+b+(p-2)1_(b>0).

This bounds every nonpivot in M by E+g, every nonpivot in ordinary A' by D+g, and every nonpivot in A by K+delta+g, with g=(p-1)/2. The ordinary derivative pivots include every odd l=1,3,...,c-1, including the endpoint at k=cN. There are c/2 paired pivots. The complete M' bound remains wt(M')>=E and is not obtained by differentiating a Frobenius residual.

### 3. The genuinely new arbitrary-alpha scalar lemma

This is proved rather than imported from the special U=-1 identity. In formal characteristic p at X²=-alpha t^p, S=z+1=v0 X satisfies S²=-alpha z t^p and v(S)=p/2 for every nonzero alpha. Let R0 and D0 be the products over the author's two exponent sets representing F_p^*. Both normalized products have jet

    -[1+t/2-t²/12]+O(t³).

The coefficient sums use only invertible denominators for p>=5. The grouped-product identity is a polynomial divisibility by h^(p-1), not an estimate fitted to examples. Grouping N_N gives relative gap at least p(p-2)/2; grouping C0 gives gap at least p(p-2), with the p-divisible progression treated exactly. Replacing R by R0 costs rho-1 and z by -1 costs rho.

Consequently N_N²/C0=-alpha with error of value >p for p>=5 and >2p for p>=7. The factor alpha^p=alpha in F_p is explicitly retained. This is valid for arbitrary residual alpha, not merely alpha=1.

The block-shift estimates have gaps B and N-rho. Every even leading-digit pivot is

    c! C0^u N_N^j/(j! 2^u u!),  u=(c-j)/2,

up to the required higher error. Summing ALL pivots yields C0^(c/2)R_c(N_N²/C0), not a selected-pivot substitute. The factorial multipliers are units because c<p. The nonpivot gap delta+g is also strictly larger than the required p or 2p. Hence R_c(-alpha)=0 gives A value >K+bp at the scalar point, where b=1 or 2 as appropriate.

The transfer to characteristic zero is sound even when K>e. Before specialization each coefficient of X^(2l) in A contains cN/2-l recurrence edges, so every raw t monomial after X²=-alpha t^p has degree at least cN/2+(p-1)l. Alpha is in Z_(p); powers of its p-unit denominator can be cleared without valuation loss. All discarded coefficients divisible by p therefore have value at least e+cN/2. At minimal s=3,

    e+cN/2-K >= (p-c)B >= B > bp.

This includes c=p-1 and controls every discarded integer coefficient. It does not use the false shortcut e>K+bp.

### 4. Feedback to every root uses J, not F

The normalized j(U)=J(mu Y)/t^K is integral restricted analytic on the whole central U disk and has residual R_c(U)^p. The original derivative bound gives wt(j_U)>=delta. The extra T_U J term prevents assigning this strong bound to normalized F_U off roots, and the author correctly does not do so.

At U=-alpha, the scalar A estimate and perturbation gap delta>bp give v(j(-alpha))>bp. In j(-alpha+V)=sum h_l V^l, h_p is a unit, all h_l are integral, and v(h_l)>=delta for 1<=l<p. If 0<v(V)<=b, h_p V^p is the unique lowest term, a contradiction. This proves v(U+alpha)>b for ALL 2p affected roots, preserving multiplicity until the derivative conclusion. A scalar derivative is never substituted for a derivative at a root.

### 5. The actual paired ordinary derivative ratio

Each odd-l derivative pivot divided by its corresponding M pivot has exact ratio

    a z^(N-1) Q_(uN+Ahalf)/(Q_(uN) a_N).

The shifted Q segment equals Q_Ahalf with error >=B independently of u. Thus the entire sum has one scalar ratio even for large c; cancellation among pivots cannot worsen the individual absolute error bounds, and M is already known to have exact value E on the affected locus.

The original H/P ordinary derivative formula retains the prefactor term, whose excess is at least 2e+K-D>2. The coordinate factor is 1+error >=rho, and the a_N mixed-characteristic binomial errors are beyond order two. Direct multiplication of the actual Q factors gives

    Q_Ahalf/(-t^B)=1-t/8+9t²/128+error >2.

The p-divisible factors and their discarded integer coefficients are controlled separately. The resulting ratio X²A'/(aM)=U(1-t/8+9t²/128)+error >2 is valid for p>=7. At p=5 only the first-order truncation has sufficient pivot slack. The independent original recurrence diagnostic below explicitly falsifies the unsupported p=5 second-order extrapolation.

### 6. Tail moments, cancellation, and units

The full maximal-matching sum, not just the unique V matching, gives

    kappa=alpha[1+(m/6)t+m(7m-27)t²/360]+error >2

for p>=7, with its first-order version valid for p=5. The second moment denominator five is not silently inverted at p=5. The shift by cN in each tail edge starts beyond the inspected precision, so the jet is genuinely independent of c.

The remaining Qstar terms kappa X M'/M and X kappa' have gaps at least rho and p-1. Root displacement has already been proved beyond the relevant precision. Therefore the complete ordinary derivative bracket begins with alpha(2d+1)t/24. If this coefficient vanishes modulo p, then p=2d+1>=7 and the next coefficient is -alpha/320, a unit. There is no third obstruction.

For the original normalized P unit, the base factor has residue

    -c C epsilon M_(c-1)(Y^p)/Y
      =-2 C chi(alpha)R_c'(-alpha).

The factor chi(alpha) is essential. This identity uses Y²=-alpha and the ordinary Hermite derivative relation, and is independent of the two residual Y signs. Multiplying by the first or second bracket coefficient gives the theorem's units. The source c=2 and d=1 specializations match without replacing arbitrary alpha by one.

### 7. H, the original kernel, and primitive phases

The H/P coordinate map near v0=i is an analytic isometry, and all roots lie in its unramified small-X region, away from +/-2. At a P root the prefactor derivative vanishes exactly. The H derivative multiplier has residue i^(n-1)=(-1)^(c/2+m), so the valuations agree but the units are not silently identified.

Consecutive P polynomials cannot share a root because nonzero recurrence edges propagate a common root to P_0=1. The unchanged telescoping ordinary Christoffel-Darboux identity is therefore nonzero at each root once P_n' is nonzero. It uses algebraic squares, not absolute-value squares. All estimates are uniform in e=(p-1)p^(s-1), and hence apply to every s>r and every primitive characteristic-zero phase.

## Evidence and reproducibility

The uniform proof above establishes the theorem. The finite controls serve only as falsification and transcription checks. The independent program imports neither candidate nor predecessor code. It reconstructs Hermite coefficients by recurrence, tail jets by constant/X-linear recurrence rather than matching enumeration, and scalar derivatives by a separately evolved partial derivative in w=X².

Completed independent controls include:

- 3,401,522 complete Newton and ordinary-derivative term pairs, including every pivot and all nonpivot gaps in the tested boundary rows.
- 18,425 bounded (p,c,d) residue controls through p=101, with separability, obstruction simplicity, and nonzero predicted lifted units.
- Exact rational short-tail jets for m=0,...,50, actual Q-factorial jets for primes 5 through 101, and symbolic positive-coefficient margin polynomials for all p>=5 or p>=7.
- Full residual gcd checks distinguishing degree two from 2p lifted roots.
- Arbitrary-alpha original scalar A recurrences at (p,c,d)=(5,4,3),(11,8,3),(11,8,7), with raw coefficient-lattice margins recorded.
- An independent original-P and w-derivative recurrence at p=5,c=4,d=3 giving scalar A order 140>K+p=135, A derivative ratio [1,3,0], and complete Qstar [0,2,2] modulo 5. Its unsupported second-order extrapolation is rejected. These scalar diagnostics are not used as rootwise derivatives.
- Genuinely mixed second-obstruction residues including (43,24,21), not merely c=2 examples.
- Separate original low-root ordinary derivative recurrences, full symbolic fraction-free witnesses, and explicit negative gates for copied alpha=1, incorrect p=5 slack, Frobenius differentiation, the wrong associated-edge start, the false e-only margin, and the incorrect off-root F_U bound.

The independent byte audit checked all 48 manifest-bound candidate files, the exact manifest/report/seal pins, every selected proof and acceptance snapshot, all 784 manifest-listed files in the eight original source roots, all four review-to-author acceptance bindings, and the pinned 40-file p=3 archive including safe paths and CRCs. The snapshots are explicitly selected evidence, not falsely represented as full historical package copies. No historical source program was executed. Source inventories and accepted bytes were rechecked after replay.

The inspected new author controls cold-replayed byte-identically in isolated normal and optimized Python (0.100 and 0.154 seconds). The independent controls cold-replayed with identical semantic results after excluding timing only (23.389 and 26.473 seconds). Each run had 120 CPU seconds, 150 wall seconds, 1 GiB address space, 16 MiB output, and one numerical thread. The independent semantic digest is `4112462c93745e0f25b9ad3364f24a6ed1f88145bbffe0012240879041df00d0`. Six disposable-copy integrity mutations were rejected: proof edit, missing file, unlisted file, seal mismatch, fully rehashed replacement, and symlink replacement. The original frozen candidate was unchanged.

## Conclusion

The new arbitrary-alpha scalar lift and all-root feedback are established with uniform margins; the conditional fallback is not needed. The exact frozen candidate is accepted for the theorem and derivative statements above. The previously accepted families are not newly credited, and no broader closure or novelty claim is made.
