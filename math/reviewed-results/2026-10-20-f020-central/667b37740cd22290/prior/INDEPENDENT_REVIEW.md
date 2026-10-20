# Independent audit: the adjacent degree n = 2 p^r + 1

20 October 2026 UTC. Verdict: **ACCEPTED WITHIN THE PRECISE PARTIAL SCOPE**, subject to the frozen-source bindings in VERDICT.json. This accepts the uniform r>=3 theorem and the uniform r=2 mechanism obstruction, not a full r>=2 squarefreeness theorem.

## Accepted result

Let p be odd prime, r>=2, s>r, N=p^r, and q a characteristic-zero primitive p^s root. Keep the original recurrence P_(j+1)=X P_j-(1-q^j)P_(j-1), P_0=1, P_1=X, and the original Gaussian H polynomial. Use ordinary derivatives and algebraic squares throughout.

The report correctly proves:

- For all r>=3, both H_(2N+1) and P_(2N+1) are squarefree, and the original diagonal algebraic-square kernel is nonzero at every P root.
- For all r>=2, zero is a simple P root with derivative valuation W(N). Each of the beta=p^floor(r/2) disjoint rho disks contains exactly 2N/beta further roots on its boundary, counted with multiplicity before simplicity. The corresponding H root is -1.
- At a nonzero root of valuation x with 2x!=p, the derivative valuation is x+min(D_2,N+E-2x), where E=N/2+2B and D_2=N+E-p. It is not constant across all roots.
- When r=2, all noncentral roots are simple and their original kernels are nonzero. The remaining 2p central nonzero roots are not proved simple by this package.
- In that central r=2 cluster, the exact normalized quotient and ordinary-derivative residuals are (Y^2+1)^p and -2 epsilon Y^(p-2)(Y^2+1). Their common factor is exactly Y^2+1. This is a uniform failure of this leading derivative certificate, not a counterexample to squarefreeness.

No global F020/F023 closure, arbitrary degree/digit extension, odd-composite-order theorem, novelty, or FFT/complexity conclusion is accepted.

## 1. Source identity and scope discipline

The actual restored comparison ZIP has SHA-256 c86929554da6cba650c0eb13ede9384e1515cfd220522983e0031e39331aa5fe. I independently checked all 453 entries of its public root manifest and all seven copied source bindings in the new candidate. The accepted leading-two report, its review and verdict, and the leading-c and low-digit context were read from the restored files. Historical nested review hashes were not substituted for hashes of the public projected copies.

The imported cap is the leading-two half-W cap. In particular the earlier low-digit exclusion of x=p/2 is not imported: it fails for the present central r=2 boundary. Every denominator remains nonzero because 2N+1<pN<=p^s. The endpoint edge has valuation v(1-q^(2N))=N, not 2N.

## 2. Neighbor polynomial and exhaustive ordinary-derivative bound

For b=2N-1, W(b)=2E. The half-W bound and superadditivity place every polynomial Newton bracket below E, with equality only at the admissible odd index k=N. Its scalar is exactly w_(2N-1)/(w_N Q_((N-1)/2)). Therefore the neighbor has weight E and a nonzero Y^L initial on each disk, with exact value E on every boundary.

The derivative proof correctly handles the half-unit issue. Reflection gives the one-variable correction p^ord_p(j)-W(j)/2, whose maximum 1/2 occurs only at j=1,p. For those two odd j, m is even. A positive m cannot be the exceptional odd N, so half-W is strict. If m=0, then a<N but 2a>=N; the floor contribution at N makes 2W(a)<W(2a). All bracket values lie in (1/2)Z, so the strict loss from E+1/2 proves the required bound <=E. Other j already give a correction <=0. Thus no parity case or half-slope equality is omitted.

The ordinary H/P derivative identity is differentiated before reduction. It transfers the neighbor derivative lower bound without discarding the prefactor term. For P_(2N)' off its own roots, the report separately bounds that prefactor term by r e+W(N)>D_2. Hence its use of exact derivative value D_2 on the entire boundary, rather than only at P_(2N) roots, is justified.

## 3. Central polynomial division and complete root counts

The quotient F=P_(2N+1)/X and neighbor quotient G=P_(2N-1)/X are polynomials, not meromorphic definitions at zero. On the central disk, multiplication by X adds precisely rho to the Gauss weight; hence G has weight at least E-rho. On noncentral disks, X has the constant valuation p^ord_p(a)<rho and gives the same lower bound.

The perturbation a_(2N)G has weight at least N+E-rho=W(N)+N/2-rho>W(N). Thus F inherits the actual leading-two residual, including its nonzero constant, degree 2L, and strict loss at all higher degrees. Newton-polygon disk counting gives exactly 2L boundary roots per disk, counting multiplicity. Their total is degree(F)=2N, which supplies the complete cover without assuming simplicity or needing an unproved outside-disk estimate. The nonzero central constant proves F(0)!=0 and the exact zero root simple.

## 4. Root-dependent derivative gate

At a nonzero F root, the identity

F'=P_(2N)'-a_(2N)(M'/X-M/X^2)

is exact in characteristic zero. The M/X^2 term has value E-2x; M'/X has value at least E-x, strictly higher because x>0. Therefore the perturbation has exact value N+E-2x. Its value equals D_2 only at 2x=p.

The complete disk geometry gives x=rho centrally and x=p^ord_p(a) otherwise. No noncentral value is p/2. The formulas for rho show rho=p/2 exactly at r=2 and rho>p/2 at every r>=3. This proves the asserted uniform r>=3 theorem while leaving precisely the central r=2 cluster outside that separation argument. The zero-root derivative is handled separately and is not incorrectly forced into the same formula.

## 5. Actual r=2 phase cancellation

I checked the phase calculation, not just the valuation tie. With N=p^2, B=p(p-1), mu^2=t^p and epsilon=(-1)^((p-1)/2), Wilson/block products give the stated units w_N/t^(N+2B)=-1, Q_((N-1)/2)/t^B=-1, a_(2N)/t^N=-2, and w_(2N)/w_N^2=2 in the residue field.

The N_N initial is -t^B(z+1)^p. Together with the original coordinate factors, this gives P_(2N)/t^(N+2B) initial 1+Y^(2p) and M/(t^(2B)mu^p) initial epsilon Y^p. The accepted unique ordinary derivative pivot at (k,m)=(2N,N) has the correct relative initial -2t^B; the H/P conversion factor has residue 1. Consequently P_(2N)'/(t^(3B)mu^p) has initial -2epsilon Y^p.

In F', the term a_(2N)M'/X has strictly higher weight. The surviving a_(2N)M/X^2 term has initial -2epsilon Y^(p-2), with its plus sign in F'. The sum is exactly -2epsilon Y^(p-2)(Y^2+1). The Laurent calculations used to compare these two quotient terms are legitimate on the boundary; their surviving initials are polynomials and the original F' is a polynomial. No derivative of a repeated residue polynomial replaces the ordinary characteristic-zero derivative.

Both nonzero roots of Y^2+1 have multiplicity p in the F residual. Thus all 2p central roots lie above places where the normalized original derivative residual vanishes. The report carefully concludes only that this certificate fails. A deeper lift or another argument is still needed to prove their simplicity uniformly.

## 6. Kernel and transfer

All original recurrence edges below n are nonzero, so adjacent P polynomials have no common root by backward recurrence to P_0=1. The ordinary CD identity gives the original kernel as P_n'(xi)P_(n-1)(xi)/w_(n-1). This proves kernel nonvanishing exactly where simplicity has been proved, and not at the unresolved central r=2 roots. It uses algebraic squares, not absolute-value squares, positivity or interlacing.

At corresponding roots the H/P coordinate derivatives are units, the prefactor derivative vanishes by the root equation, and no root meets a ramified coordinate point. The stated derivative valuations and simplicity therefore transfer to the original H polynomial. Algebraic nonvanishing transfers between primitive characteristic-zero embeddings.

## 7. Reproducible controls and independence

The mathematical argument above is the uniform audit. Finite controls are falsification/transcription checks only:

- The author checker was cold-replayed in a separate writable copy; its CONTROL_RESULTS.json is exactly identical to the frozen author's JSON. This includes its finite good-prime squarefreeness witnesses, not a uniform theorem inferred from them.
- The new direct-sum integer checker independently tests nine (p,r) pairs, including p=3 through r=5, all neighboring Newton terms and full derivative double sums, the half-slope exceptional set, and the complete cover comparison.
- The new original-P cyclotomic checker independently constructs the quotient and ordinary derivative in six actual fields. The four r=2 cases (p,r,s)=(3,2,3),(3,2,4),(5,2,3),(7,2,3) verify both exact stated residuals and units. Additional (3,3,4),(3,4,5) controls record their separated central derivative initials. Mixed-characteristic weights and differentiation factors are retained even above ramification.

The reviewer first supplied a challenge to naive derivative-residual coprimeness and finite confirmations of the author's sharper obstruction. The author independently derived its quotient mechanism and central cancellation before receiving those confirmations. No essential lemma or proof patch was supplied by this reviewer, and no mathematical revision was requested. Thus no third acceptance is required for a reviewer-created essential proof contribution. A reviewer-created Python cache was removed from the candidate manifest before final binding; the proof report bytes did not change.

## Disposition

No mathematical defect was found. Accept the frozen partial theorem and the precise uniform obstruction within the scope above. The remaining task is strictly the r=2 central nonzero cluster; finite successful squarefreeness witnesses do not close it. Wider F020/F023 scope is unchanged.
