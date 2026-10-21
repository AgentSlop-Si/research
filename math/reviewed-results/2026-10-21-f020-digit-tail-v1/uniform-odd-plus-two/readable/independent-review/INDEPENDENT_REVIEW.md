# Independent review of uniform odd-leading +2 degrees

21 October 2026 UTC. ACCEPTED WITHIN THE EXACT STATED SCOPE. Frozen candidate manifest: db295d917b83f18dc36ddf2f708eadf9e3203f0b60c3ddb5852fbb91a6ee28c4. Frozen report: 1c10fb9f9f6035ec3c56119a0e1c778e4c1f42eea0b72e630d7ed68c60fc0ff6. VERDICT.json and SOURCE_BINDING.json record the exact decision and source binding. The independent derivation was written before reading the new candidate. Only newly authored reviewer programs were executed; no candidate, accepted-source or dependency program was imported or run. No source bytes or external state were changed.

## Scope and source authority

This review concerns exactly p prime, odd 3<=c<p, r>=2, s>r, n=cp^r+2, and every characteristic-zero primitive p^s-th root q. The original P recurrence, original Gaussian-binomial H, ordinary derivatives, and original algebraic-square Christoffel-Darboux kernel are retained. The c=3 +2 subfamily is inherited, not newly credited. New coverage is odd 5<=c<p.

The accepted uniform odd-adjacent author manifest is 438eb219f3534b41caa13905423c21afb2ae9fb777a8acdfa9b93438d126e032 and its separate accepted review manifest is a7deb7b69007940e8c7e49155701eabd22e7f81b01ba8012c5c94ee97a68be35. These genuinely provide coefficientwise profiles for A=P_(cN), M=P_(cN-1), A', and M' across the entire disks. The new theorem is not inferred merely from simplicity at the adjacent degree. Neither its exceptional second layer nor its exact adjacent central-interior depth is imported.

Source verification checks the exact full inventories of these two packages, the inherited c=3 +2 author and reviewer, and the retained c=3 adjacent author; the 453- and 408-entry current archive inventories are checked separately. Historical and projected public byte identities remain distinct. Partial report snapshots are not represented as standalone complete packages.

## Exact identity and uniform domination

Write N=p^r, B=r(p-1)p^(r-1)/2, K=cN/2+cB, E=(c-1)N/2+cB and D=N+E-p. Set a=1-q^(cN), b=1-q^(cN+1), T=X^2-b. Recomputing the two original recurrence steps gives F=P_n=TA-aXM. Ordinary differentiation and elimination give the complete off-root polynomial witness

    S=TF'-2XF=T^2 A'+a(X^2+b)M-aXT M'.

The signs, T square and M' term all matter. At an F root, S=TF', and no division by X excludes zero. The accepted profiles have initials proportional to M_c for A and M_(c-1) for both M and A'. The neighbor derivative has whole-disk weight >=E. The ordinary A' profile transfers off A's roots because the H/P prefactor has weight re+K>D.

Every high disk has Gauss weight x>=1 for X and v(b)=1, so T has fixed valuation 1 with nonzero constant initial. The perturbation aXM is above TA by N/2+x-1>0. Thus F has the same complete high residual root locus as A. Hermite recurrence and p>c prove gcd(M_c,M_(c-1))=1, including the odd zero residual root. Therefore at every high F root, v(M)=E and v(A')=D.

The three witness terms have values D+2, D+p+1, and at least D+p+1+x. The first wins with margins p-1 and at least p-1+x, independently of c, s and r. Consequently every high root has v(F')=D+1. At X=0 the third term vanishes and the same conclusion applies. Directly F'(0)=-bA'(0)-aM(0) has term values D+1 and D+p.

There is no r=2 exception. In particular c=11,p=13 genuinely has an adjacent first-layer obstruction, but that cancellation belongs to another witness. For +2 the strict p-1 margin still holds. The candidate's optional r=2 residual refinement cM_(c-1)(Y^p)=-2R_c'(-1) on the formerly exceptional residue classes is also valid and nonzero; it does not assume the new roots coincide with adjacent roots.

## Counts, zero and the two shallow roots

The beta disjoint high disks each have residual degree cL, zero multiplicity L and c-1 nonzero residual locations of multiplicity L. Their exact closed-disk counts are cL roots per disk: (c-1)L boundary and L strict-interior. These are Newton/Weierstrass counts with multiplicity, not false simple-root lifting of the inseparable substitution Y^L. Total high count is cN.

F is odd, so its exact zero is among the L central interior roots. The derivative witness makes it simple; precisely L-1 central interior roots are nonzero. Nothing is claimed about those nonzero deeper valuations. Noncentral roots retain the value of their center, and the central boundary value is rho.

The integral shallow normalization Q_j(Z)=tau^(-j)P_j(tau Z), tau^2=t, has residual recurrence M_(j+1)=ZM_j+jM_(j-1). The factorial formula gives M_p=Z^p modulo p, and a block induction gives M_(ap+b)=Z^(ap)M_b. Hence the ORIGINAL polynomial and ORIGINAL ordinary derivative reduce to

    Q_n=Z^(cN)(Z^2+1), Q_n'=2Z^(cN+1).

The two distinct nonzero roots Z^2=-1 lift simply, each with v(X)=1/2 and v(F')=(cN+1)/2. They are disjoint from all high disks. The count cN+2 is exhaustive; the one exact zero has not been double-counted. The argument differentiates the actual integral shallow polynomial, not the inseparable high initial.

## Original kernel, H and discriminants

At every high root the exact predecessor relation is P_(n-1)=abM/T, valid also at zero, so its value is N+E. At either shallow root, A has value cN/2 and P_(n-1)=bA/X has value (cN+1)/2. The factorial denominator has value cN+2cB+1. Substitution into the original diagonal Christoffel-Darboux identity gives kernel value N-p at every high root and -2cB at either shallow root. These finite values prove nonvanishing of the original algebraic-square sum, including at zero. No Hermitian positivity or quotient-polynomial kernel is substituted.

The exact H/P coordinate relation has unit coordinate derivatives on the branch near i. Every P root has positive value or is zero, so none is +/-2. At each root the ordinary H derivative prefactor vanishes exactly, and the remaining unit transfers both multiplicity and derivative valuation. Thus both original polynomials are squarefree, and the simple zero corresponds to the simple H root -1.

Summing the original root derivative values gives equal monic discriminant valuations cN(D+2)+1. The p-adic argument uses every phase's own t=q-1 and the full e=(p-1)p^(s-1). An injective algebraic embedding establishes the characteristic-zero conclusion for every primitive phase and every s>r.

## Independent reproducible evidence

The new reviewer controls check the free differential witness, the fraction-free predecessor identity, and cleared original Christoffel-Darboux identities through degree 7. They check Hermite coprimeness for 64 prime/digit pairs through p=31, all new domination and kernel/discriminant margins at r=2,3,4,5, and complete shallow block recurrences at five primes.

Five original cyclotomic recurrence controls use (c,p,r,s,phase): (5,7,2,3,2), (7,11,2,3,3), (11,13,2,3,2), (3,5,3,4,-1), and (5,7,2,4,-1). The cyclic q representation is projected to the complete cyclotomic quotient and converted by exact Pascal substitution to the canonical t basis. Integer ordinary-derivative factors are retained before valuation. Coefficient precision p^3 and int64 accumulation bounds are explicitly certified.

Unlike a guard-only test, the reviewer excludes every omitted X coefficient by the raw recurrence edge-count lattice: the coefficient of X^j in P_k has raw t order at least (k-j)/2. For the witness its bound is (n+1)/2+j(rho-1/2). Chosen cutoffs place every unretained coefficient strictly above every tested target. Low-X truncation is closed under the original recurrence.

The controls consequently check complete central F and S initials, their coprimeness, their full degrees and zero multiplicities, exact-zero derivative and predecessor values, the original zero-kernel valuation, and the complete ordinary M' lower bound. Separate full sparse shallow polynomial and differentiated recurrences run all the way to each target degree, including 1861. Nonprincipal-phase and nonminimal-s controls prevent accidental principal-phase specialization. The c=11,p=13 zero derivative has value 2718 and the original zero kernel value 156, with a nonzero high witness throughout the residual root locus.

Normal and optimized reviewer replays must match CHECK_RESULTS.json byte-for-byte. The inventory verifier uses explicit exceptions rather than asserts and rejects altered, missing, additional, symlinked and unsafe-path fixtures. These are finite falsification diagnostics; the uniform proof rests on the independent derivation above and the explicitly accepted coefficientwise input.

## Bounded decision

The verdict accepts only the exact stated family and conclusions recorded in VERDICT.json, bound to the frozen candidate above. No essential mathematical repair was required; the producer's proof was consistent with the independently recorded derivation. All-root kernel/discriminant refinements and independent control outcomes were communicated before freeze. There is no acceptance of c>=p, r=1, s<=r, other tails or intermediate digits, composite orders, exact deeper interior valuations, global F020/F023 closure, historical novelty, or any FFT/cost claim. No repository or other external write is part of this review.
