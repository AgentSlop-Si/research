# Independent acceptance: separated bottom-p ordinary guard

23 October 2026 UTC. ACCEPT the exact family below. Author REPORT.md SHA-256 `0ee61bbaeff0884c76638771e897f929b3998f13c36a969c7cb43c10bc648f6d`; author MANIFEST.json `83e8505fe108e8f4f68bf012e89874d47637f3251f4b0a1be9bc3915f522e0e5`. All 22 manifest members and 16 selected source-copy bindings were verified. No author or historical scientific program was run.

## Exact statement and source boundary

For every odd prime p, even 2<=c<p, odd 1<=d<p, k>=3, r>=k+2, s>r, and characteristic-zero primitive p^s-th root q, the original recurrence polynomial at n=2p^r+c p^k+d p is squarefree. The original ordinary Christoffel–Darboux algebraic-square kernel is nonzero at every root, with the original neighbor P_(n-1). H_n inherits squarefreeness through the unit local coordinate maps. The smallest degree is 543.

This accepts only the displayed separated, one-even-middle, bottom-exponent-one family. It does not accept bottom zero, adjacent k=2, odd middle digits, even terminal digits, or arbitrary numbers of middle digits. All prior successful high-order, fixed and residual certificates retain their credit; incremental coverage is the stated family minus every prior successful certificate, including the exact C_u deflation bound in the author report. There is no F020/F023 owner closure, historical novelty, complexity, stability or FFT claim.

The accepted sparse and two-middle reports/reviews supply full-disk core/neighbor estimates and complete monic covers at levels >=2, including ordinary B'>=E and the outside-cover ratio bounds. Their source scopes were checked, not extended from central-disk data. The new work is the bottom derivative endpoint, a stronger ACTUAL shifted g' estimate, and a separately proved level-one outer cap. No unproved bound from the stopped general-adjacent route is used.

## 1. Bottom carry invariant and ordinary derivative

Write an odd tail as m=cM+dp or m=dp, u=(m-1)/2, G=W(u), h=(p-1)/2. The digits of u are at most h, the units digit is h, and its p-digit is strictly below h. Thus W(m-1)=2G, W(m)=2G+p, and u modulo p^a is strictly below (p^a-1)/2 for every a>1. If 2x+1 has valuation p^b with b>1, subtracting x from u forces carries at all levels 2,...,b. Their defect is at least p^b-p, giving W(x)+W(u-x)+V(2x+1)<=G+p.

The needed extension of the deep cap to a tail below p^2 is independently transparent. At level three, R_3(j)=floor(j/p)/2 for j<p^2; at levels >=4 it is zero. Comparison with W(floor(j/2)) is strict except j=0,1. The usual parity argument gives the stated coarse ordinary derivative losses. No invalid p^2 endpoint is imported at bottom exponent one.

For an odd derivative index delta=2b+1 on a deep disk, the Newton score is at most W(u-b)+V(2b+1). For b<h it is at most G+1; for b>h the carry inequality gives at most G+p-W(b)<=G+h. At b=h it is exactly G+h+1. For even delta the score is at most G. The deep cap is strict away from Newton index zero in this parity, so the unique least term is delta=p, Newton index zero, and the original derivative weight is G+h. The off-root H/P correction is strictly higher.

On the full k disks, the half-W cap leaves delta=p as the only possible equality endpoint. For valuation p^b, b>=2, the extra carry defect gives the score increment [p+p^b-b(p-1)p^(b-1)]/2, strictly below h+1. At delta=p the complete equality set is Newton index bM for b=0,2,...,c, with a=(c-b)M/2+(d-1)p/2. All equality terms are retained; their actual block units sum to M_c(Z), whose constant is nonzero. Therefore f' is exact G+h in every strict k interior, not automatically on its boundary. The off-root chain correction has valuation at least v(p)+G+p/2, strictly larger.

## 2. Actual shifted g': exact cancellation and all parities

I independently checked the finite generating-inverse derivation: ordinary X differentiation gives opposite logarithmic-series terms for the two generating factors. After reindexing, their difference cancels 1-q^delta through

    (1/(1-q^(U+a))-q^delta/(1-q^(U+a+delta)))/(1-q^delta)
      =1/((1-q^(U+a))(1-q^(U+a+delta))).

It yields the author's double sum for the ACTUAL shifted g_m^U, with endpoints 1<=a<b<=m, both original q orientations, and the Chebyshev factor U_(b-a-1). All denominators are legal. Here V(U) exceeds every endpoint valuation, so the two shifted denominator values are exactly V(a),V(b), and the prefactor has weight W(m). Integer Chebyshev coefficients and X reducing to zero do not decrease weights.

With x=floor((a-1)/2), y=floor((m-b)/2), z=u-y, the required score is W(x)+W(y)+V(a)+V(b)<=G+p. I checked all four cases independently:

- Even a, odd b: W(x)+V(a)=W(x+1)<=W(z), followed by the odd-endpoint carry inequality at z.
- Both even: x+1<=z-1 absorbs the two endpoint values into W(z), giving the stronger score <=G.
- Both odd: z-x is a positive multiple of the smaller endpoint valuation. An interval of that length absorbs the smaller value; apply the odd-endpoint inequality at the other endpoint.
- Odd a, even b: put B=V(b)=V(z). If z-x>=B, the same absorption works. Otherwise W(z)-W(x)=B+W(z-x-1). Away from 2(z-x)-1=B, the elementary score V(2v+1)-W(v)<=p finishes. At that exceptional equality, if A=V(a)>B, then z mod C=(C+B)/2 at every p-power B<C<=A. Since u mod C<(C-1)/2, the carries in z+y=u have defect at least A-B. The remaining score is at most G+B-W((B-1)/2)<=G+p. This includes the large-odd-endpoint exception rather than assuming A<=B.

Thus every double-sum term has weight at least G, proving g'>=G on EVERY full deep disk. This is not a residual derivative or a central-only estimate. The finite connection proves g has exact constant weight G there; its weight-G terms have even factors and sum to the exact nonzero g_m^0(0). Actual shift errors are strictly above the retained values because D>=p^2 M0. Full lower disks retain only the weaker g>=G+p-M0 and g'>=G+p-M0-sigma. No full-lower g-unit or division by g is assumed.

## 3. Independent arbitrary-prefix level-one cap

The single outer disk has rho=1-1/(2p). Every q-center differs from -1 by valuation at least one, so N_v has exact initial (z+1)^v throughout this disk. This proves the required coefficientwise statement, not just its value at the center.

A direct quotient calculation independently verifies the block estimate. For b=Qp and x=alpha p+t, 0<=t<p, put F(x)=R_1(b)-R_1(b-x). Superadditivity gives

    F(alpha p)>=p W(alpha)-alpha/2,
    F(alpha p+t)>=p W(alpha+1)-alpha/2-1+t/(2p)  (t>0).

For a=up+w, w=0 gives F(2a)-W(a)>=p(W(u)-u)>=0. Equality requires u<p and no terminal carry, precisely 2u<=e=Q mod p. If w>0, writing 2w=epsilon p+t gives the strictly positive remainder

    epsilon(p-1)/2+p-1-t(p-1)/(2p).

For derivative index delta=lp+v, v=0 and w=0 give lower score difference pW(l-1)-l/2+p(W(u)-u). Its only minimum -1/2 has l=1, u<p and no terminal carry. Proper w>0 is strict. If v>0, the small-block expression is at least p/2, while V(delta)=1, so equality is impossible. Thus the root and ordinary derivative equality sets are exactly those stated in Sections 7.2–7.3 for ANY upper prefix Q, including the actual degree n.

The actual block-factor units give the complete initials Y^b0 M_e(gamma Y^p) and Y^b0 M_(e-1)(gamma Y^p), at weights rho b and rho b-1/2. These factorial coefficients are units since e<p. The correction in the ordinary H/P chain is higher because b is divisible by p. The root initial has full degree b and unit leading coefficient, so all roots lie in this closed disk. For odd e=d, exactly (d-1)p boundary roots occur; the ordinary derivative initial is nonzero there by Hermite coprimality, even though the reduced Y^p map is inseparable. For b=dp its derivative constant is nonzero and rho dp-1/2=G+h. No reduced-root multiplicity is mistaken for a characteristic-zero collision.

## 4. Complete root partition and kernel

On each k or r core boundary where the core residual vanishes, the original neighbor and g are exact units after their indicated weight normalizations. At a full root, delta=v(f)-G>=p and gamma=v(C)-J satisfy delta+gamma=D/2. The f'C term is exact; its three competing derivative terms have gaps 2delta-p-h, delta-h, delta-h, all at least h+1>0. Where the core residual does not vanish, C is exact J and all gaps are at least D/2-h>0, including f=B=0. This also settles deepest strict r interiors.

In each annulus, only C is divided by; the complete monic cover makes it analytic and nonzero. The inherited closest-center ratio estimates allow ties and cover the new bottom annulus with tau<1. The competing gaps are D/2-M0+h+1+rho-2tau, D/2-M0+h+1+rho-tau-sigma, and D/2-M0+h+1-tau. Since M0<=D/p^2 and rho<D/p, they are all strictly positive. Actual shift and off-root correction costs remain included.

After the outer boundary, the disjoint list is: strict outer interior outside k cover; k boundaries; strict k interiors outside r cover; r boundaries; strict r interiors. Strict nesting and complete covers make it exhaustive, without assuming even-prefix squarefreeness. Every root is simple. Consecutive ORIGINAL P_n and P_(n-1) are coprime by recurrence propagation through nonzero edges to P_0=1. Therefore the original ordinary algebraic-square CD identity proves the requested kernel nonvanishing. The unit coordinate maps and characteristic-zero p-adic embeddings transfer the result to every primitive phase.

## Fresh controls and limits

The independent fresh_controls.py imports no author or historical scientific routines. Normal and optimized executions are byte-identical: 442,023 explicit checks. They exhaust all four endpoint parities in five distinct tails, including 43 exceptional large-endpoint carry cases; check the complete strict-k derivative equality sets; and enumerate every root/ordinary-derivative Newton score for nine arbitrary-prefix level-one fixtures, including the actual minimum degree 543. Ninety exact rational polynomial identities verify the ACTUAL shifted ordinary g' double sum for three q values, three shifts and ten lengths. Separate grids verify the bottom-one deep cap and every displayed strict margin.

These are transcription/falsification controls, not a cyclotomic root census or uniform proof by finite samples. No author million-check total is used as independent evidence. A useful hand negative control remains p=3,m=3: P_3' has constant 3t+t^2, of value 2 at the legal high phases, rejecting the old predicted value 1 and matching G+h=2. No squarefreeness failure is inferred from that rejected old mechanism.

The author packet requires no mathematical repair. Acceptance adds only the stated bottom-p family after prior-coverage subtraction; it does not endorse the stopped general-adjacent bound, a sparse j=1 induction, or an efficient root/bit-complexity algorithm.
