# Independent bounded review: uniform even middle digits

21 October 2026 UTC. **ACCEPTED WITHIN THE EXACT STATED SCOPE.**

This review binds `frozen-source/f020-even-middle-digit-candidate-20261021_v1`, whose frozen MANIFEST.json has SHA-256 `6645bc9ce05b89a9b7276404d60d3024c8b4b261c4afb16470dbb64c2951e82d`. Its REPORT.md is 22,825 bytes, SHA-256 `74edee01d70fb4bf67358436303dfce66a01baaefef764bafdf2236d748208b4`; its SEAL.json has SHA-256 `7666d16f3e7013db049a024b6ba012bb16ab27ef583593dda61c1db59ce2ead7`. All 48 listed files and the exact 50-file inventory pass independent byte verification. Acceptance does not extend to later revisions, public transformations, a repository operation, or a broader theorem.

The accepted scope is every odd prime p, every integer s>3, every even integer 2<=c<p, every characteristic-zero primitive p^s-th root q, and degree n=2p^3+cp. The c=2 conclusion is inherited; the added sector is even 4<=c<p. The accepted c=1 result remains separate and inherited. Odd 3<=c<p is not established by this review.

The unchanged definitions are

    P_0=1, P_1=X, P_(j+1)=X P_j-(1-q^j)P_(j-1),
    H_b(z)=sum_k [b choose k]_q z^k,
    w_j=product_(u=1)^j(1-q^u).

Original ordinary characteristic-zero derivatives, the original Gaussian H, and the original algebraic-square Christoffel-Darboux kernel are retained. No candidate or source program was executed. All computational controls here were written independently. Candidate and source bytes were read, not modified. No external write occurred. The author communicated its architecture, and I read a pre-freeze report before receiving the final frozen identities; this was not a wholly blind review. I independently reconstructed the decisive estimates and subsequently bound the final bytes. No mathematical repair to the frozen packet was needed.

## 1. Source boundary, inherited credit, and documentary limitation

The accepted short-tail assembly covers n=a p^r+d with r>=2, 1<=a<p, and d<p. The target has base-p digits 20c0 and is outside that rectangle. The retained first-two-digit theorem means b<p^2, not arbitrary two occupied positions. The retained smaller block ranges, pure powers, single-leading-digit families, fixed small-prime/order certificates, and conditional local guards do not already establish the present new even sector. This is a bounded audit of inspected accepted sources, not a literature or priority search.

The c=1 and c=2 exact author/review pairs remain inherited. Their complete manifests have respectively 30, 8, 40 and 10 listed files. The general full-disk author/review manifests have 13 and 19 listed files. I independently verified every listed file, exact inventories including manifest/seal, and matching seals at all six original package locations. The c=2 author manifest is `ebff60ce117ad3f9f7830e1053b1edf02f0e6733cf9571ca80e4b6d25544e05e`; its review manifest is `1fd4b414f987ad2244420386d82cfa4a847551eb74f4014bd86056f456712cc6`.

The current 34 documentary bindings, preceding 27 bindings, and older 17 original-location bindings all match their retained snapshots and designated source bytes. Selected snapshots are not represented as complete copied packages. The archive is independently hashed and its cited members are read directly.

The historical b=2p mismatch is genuine: retained report SHA-256 `00a4ad13b0726205f3dd6515a4f4c6e9687622c738efdb3df39360b6bcf593db` differs from historical-review cited original report `6b27fcbdc7aae652afae91fa9e1a8baf84270ef57af75c44c5f35288541686da`. Original author bytes and the original complete package are not claimed recovered or accepted. No historical acceptance is transferred to the changed snapshot. The candidate reconstructs the needed whole-short-block matching argument directly. Its mathematical credit remains inherited, as do the original identities, p-block coefficient fact, and leading-digit full-disk lemmas.

## 2. Legal specialization and usable off-root inputs

Put t=q-1, v(t)=1, e=v(p)=(p-1)p^(s-1), and

    N=p^3, L=p^2, m=(p-1)/2, B=3(p-1)p^2/2,
    K=N+2B, E=N/2+2B, D=N+E-p,
    rho=p-1/2, alpha=1-1/(2p), F=c(p-1/2).

Since n<=2p^3+p(p-1)<p^4<=p^s, every required edge and q-factorial is nonzero, including p=3. The cyclotomic identity v(1-q^j)=p^ord_p(j) applies throughout the required indices. In particular a0=1-q^(2N) has value N.

Write A=P_(2N), M=P_(2N-1). On each disk D_a={v(X-x_a)>=rho}, where x_a=i(q^(a/2)-q^(-a/2)) and 0<=a<p, the accepted general source proves full coefficientwise weights K,E,D,>=E for A,M,A',M'. The respective first three initial polynomials are scalar-unit multiples of Zbar^2+1,Zbar,Zbar, with Zbar=gamma_a Y^L. Therefore M and A' have exact values E,D at any point on the residual locus Zbar^2+1=0, not just at old A roots. The ordinary derivative estimates are proved before residue reduction.

A has exactly 2L boundary roots in each of the p disjoint disks and no others; v(A(0))=K. All A roots have X-value at least one. The selected full-disk source and accepting review support precisely these inputs. No derivative of an inseparable residual is substituted for them.

## 3. Tail indexing and the coefficientwise high-scale argument

Let f be the cp-vertex shifted tail with internal edges b_j=1-q^(2N+j), and g its FIRST-vertex-deleted continuant. Direct original recurrence gives

    P_n=f A-a0 g M.

This g has degree cp-1 and is not the last-deleted polynomial P_(cp-1). The distinction is necessary, not cosmetic.

For a p-vertex block U shifted by 2N+ip, its edge difference from the unshifted p block has value at least p. The h-edge matching difference has coefficient value at least p+h-1 by telescoping products. Combined with the inherited P_p=X^p+lambda X+J, v(lambda)=p-1, lambda/t^(p-1) reducing to epsilon=(-1)^((p+1)/2), and all coefficients of odd J of degree at least three having value >=p-1, this proves:

    U(tY)/t^p -> S(Y)=Y^p+epsilon Y;
    U(rY)/r^p -> Y^p, where r^(2p)=t^(2p-1);
    U'(rY)/t^(p-1) -> epsilon.

The last formula is an original ordinary derivative. Its leading term p X^(p-1) has value e+(p-1)alpha, strictly larger than p-1. The actual coefficient precision used is below e. It is not permissible to derive this formula by differentiating Y^p.

A p block losing one endpoint has p-1 even vertices and weight m at every X-weight beta>1/2, with constant normalized units d=(p-2)!! and h=2^m m! for the two endpoint choices. Wilson's identity gives dh=-1 modulo p. Its derivative has weight >=m-1+beta. A block losing both endpoints has weight >=m-1+beta and derivative >=m-1. All are direct matching estimates; the even constants have unique perfect matchings.

Expand the whole tail by its selected joining edges. For f, let j be their number and a the number of adjacent selected pairs. Exactly a blocks have two removed endpoints, 2j-2a have one removed endpoint, and c-2j+a are intact. The t-scale weight is at least

    cp-j+a(m+1).

The number of runs is j-a<=c/2, so this is at least F+am. With a=0, equality requires the unique perfect matching {1,3,...,c-1}. Its constant unit is C_c=He_c(0)=(-1)^(c/2)(c-1)!!. Since c<p, it is nonzero. All nonconstant terms lie strictly above F. Thus f(tY)/t^F has constant reduction C_c.

For g, let z indicate selection of joining edge 1 and a count twice-incident complete blocks. Its t-scale weight is at least

    m+(c-1)p-j+(a+z)(m+1).

The runs not touching the shortened first block number j-a-z and use at least two complete blocks apiece. Since there are only c-1 complete blocks, j-a-z<=c/2-1. Hence the displayed weight is at least F-m. No residue unit is required.

Parity and these t-scale coefficient bounds give, at every X-Gauss weight x>=1,

    weight(f)=F, constant unit initial; weight(f')>=F-2+x;
    weight(g)>=F-m-1+x; weight(g')>=F-m-1.

For example the f' bound follows termwise from v([X^d]f)>=F-d and d>=2 even; differentiation retains its integer d and gives weight >=F-d+(d-1)x>=F-2+x. The g derivative is analogous with odd d>=1. These are full coefficientwise inequalities, not evaluations at old roots.

The possible leading g residual is h J_c S(Y), where J_c sums products (-i) over maximum nonadjacent subsets of {2,...,c-1}. J_4=-5 and J_6=33 cancel at (5,4) and (11,6). Independent controls also detect J_12=-35685 at (13,12) and J_16=-8294895 at (17,16). This finite list is not asserted exhaustive. Every such cancellation only improves the lower bounds. Treating g as the other deleted neighbor, or claiming its residual always a unit, would fail; the candidate does neither.

## 4. All high roots, all four derivative terms, and no zero

On D_a take x=1 when a!=0 and x=rho centrally. The correction a0gM has weight above fA by at least

    N/2-m-1+x>0.

Consequently the full polynomial has the same degree-2L, nonzero-constant boundary residual as A on each disk. Newton/Weierstrass counting yields exactly 2L boundary roots per disk, counted with multiplicity before simplicity, and none strictly interior.

At each new root, M and A' have exact values E,D; M' has value >=E. Since f is a normalized unit, the root equation A=a0gM/f is legal even if g=0. Original differentiation gives

    P_n'=f A'+f' A-a0 g'M-a0 gM'.

The first term has exact value F+D. The other three have respective lower bounds

    N+E+F-m-3+2x,
    N+E+F-m-1,
    N+E+F-m-1+x.

Subtracting F+D=N+E+F-p gives m-2+2x, m, m+x, all positive for m>=1,x>=1. Thus fA' is uniquely minimal, proving simplicity and v(P_n')=D+F at all 2N high roots. No cancellation of g can threaten that conclusion.

Both g and M are odd. Hence P_n(0)=f(0)A(0) has exact finite value K+F. There is no zero root and no parity-based carry-over from the c=1 result.

## 5. The whole-short-block alpha residual and its ordinary derivative

Let T=P_(cp) be unshifted. At alpha scale the same joining subset with j selected edges and a adjacent pairs has weight at least

    F+a delta, where delta=(p^2-1)/(2p).

Indeed selected joining edges have value p, one-endpoint blocks have weight m, double-endpoint blocks have weight m-1+alpha, and intact blocks have weight p alpha. The j contribution cancels because p+2m=2p alpha. For a=0 the selected joins and endpoint constants contribute product (-i), leaving Y^(p(c-2j)). Summing the nonadjacent path matchings gives exactly

    T(rY)/r^(cp) -> He_c(Y^p).

The original derivative must be reduced separately. Relative to a subset's original weight, differentiating an intact block loses 1/2, differentiating a one-endpoint block loses at most 1-alpha, and differentiating a double-endpoint block loses at most alpha. If a>=1 all derivative terms are strictly above F-1/2; the smallest potentially dangerous gap is delta-alpha+1/2=m>0. If a=0, endpoint derivatives have strict gap alpha-1/2. Only intact-block derivatives survive. With U=t^(p-1)r^((c-1)p), their sum is

    T'(rY)/U -> epsilon He_c'(Y^p), v(U)=F-1/2.

Here He_c' is the derivative in the Hermite variable, then evaluated at Y^p. It is not d/dY[He_c(Y^p)]. The recurrence He_(j+1)=Z He_j-j He_(j-1), together with He_c'=c He_(c-1), proves coprimality of He_c and He_c' because 1,...,c are units. Its even constant C_c is nonzero. Thus the original derivative residual is nonzero at every root location of the repeated alpha residual.

For shifted f versus T, each edge difference has value N. A changed h-edge product has value at least N+h-1. Since alpha>1/2, minimizing the resulting weighted coefficients gives

    weight_alpha(f-T)>=Q=N+cp/2-1,
    weight_alpha(f'-T')>=Q-alpha.

The inequalities Q>F and Q-alpha>F-1/2 follow uniformly from c<=p-1. These are coefficientwise precision statements. They do not identify actual shifted-tail roots with unshifted roots, and they do not posit a common finer separating radius.

## 6. Coarse outer-root count and point-local derivative quotient

Monic factorization and the already proved A-root values show

    A(rY)/r^(2N) -> Y^(2N).

Direct matching bounds for odd degrees give

    weight_alpha(g)>=cp/2-1+alpha,
    weight_alpha(M)>=N-1+alpha.

These bounds are freshly evaluated at alpha; no old high-disk M bound is extended outside its domain. Therefore a0gM lies above Af by

    Delta=p^2-c(p-1)/2-1/p>0.

The full monic polynomial is integral after scaling and has reduction

    P_n(rY)/r^n -> Y^(2N) He_c(Y^p).

Over the algebraically closed residue field, He_c has c distinct nonzero roots; Frobenius is bijective. There are c nonzero normalized root locations, each of multiplicity p. Reduction of a monic integral polynomial, equivalently distinguished-factor/Newton counting, gives exactly p roots counted with multiplicity in each such residue class. Hence exactly cp roots have X-value alpha. This argument does not invoke simple-root Hensel for the inseparable polynomial He_c(Y^p).

At any such root xi, A(xi) is nonzero with exact value 2N alpha. Put R=a0gM/A locally at xi. Polynomial derivative monomial bounds lose at most alpha. The quotient rule, including its A' term, gives

    v(R(xi))>=V=p^2+cp/2-1/p,
    v(R'(xi))>=V-alpha.

There is no claim that A is invertible on the entire alpha disk, which contains the old roots. The local denominator is controlled by its exact value at xi. The two decisive strict gaps are

    V-alpha-(F-1/2)=p^2-c(p-1)/2-1/2-1/(2p)>0,
    Q-alpha-(F-1/2)=N-c(p-1)/2-3/2+1/(2p)>0.

The coarse residue of xi makes He_c'( (xi/r)^p ) nonzero. Consequently T'(xi), and therefore f'(xi)-R'(xi), has exact value F-1/2. Differentiating P_n=A(f-R) at the root kills A'(f-R) exactly, so

    v(P_n'(xi))=2N alpha+F-1/2.

All cp outer roots are simple. They are disjoint from the old disks because alpha<1. The count 2N+cp=n exhausts the degree, excluding any further cluster. General c finer geometry is not claimed; the stronger inherited c=2 geometry is not extrapolated.

## 7. Small prime, cancellation stress case, phases, H, and kernel

At p=3 the allowed even sector is only c=2. Then F=5, D=183/2, K=81 and alpha=5/6. There are 54 high roots of derivative value 193/2, six outer roots of derivative value 99/2, and v(P_60(0))=86. The least high derivative gaps are 1,1,2; the outer derivative error gaps are 19/3 and 71/3. Everything remains strict at p=3,s=4. This case is inherited, not new scope.

The first added case p=5,c=4 has n=270, F=18, D=965/2, K=425 and alpha=9/10. Despite the vanishing first-deleted g residual, all 250 high roots have derivative 1001/2, all 20 outer roots have derivative 485/2, and the constant has value 443. The frozen arithmetic agrees with the independent rational ledger. The author's disclosed pre-freeze arithmetic transcription correction is not a mathematical repair to the frozen proof.

The argument retains actual t, e, integer coefficients, legal specializations and coefficientwise inequalities. The inherited mixed-characteristic p-block statement is valid for every primitive phase, and all subsequent inequalities are uniform. Finite fields are diagnostics, not substitutes for these quantifiers. Any characteristic-zero primitive phase embeds in an algebraic p-adic field; the established algebraic nonvanishing transfers back injectively.

Every P root has positive value, so none is +/-2. The exact identity H_n(v0^2)=v0^n P_n(v0+v0^(-1)) gives a multiplicity-preserving bijection on the analytic branch near v0=i. Both coordinate derivatives are units for odd p, H_n(0)=1, and the n P roots account for all n H roots. At a root,

    H_n'=v0^(n-2)[(n/2)P_n+(v0-v0^(-1))P_n'/2].

The P_n term vanishes and the remaining factor multiplying P_n' is a unit. Thus H_n is squarefree with the stated rootwise ordinary derivative values; no equality of normalized units is asserted.

Consecutive original P polynomials are coprime by backwards recurrence through nonzero edges. The exact diagonal CD identity therefore gives, at each P_n root xi,

    sum_(j=0)^(n-1) P_j(xi)^2/w_j
      =P_n'(xi)P_(n-1)(xi)/w_(n-1) !=0.

These are algebraic squares. Neither Hermitian positivity nor interlacing is invoked.

## 8. Independent controls and final scope

The fresh reviewer coefficient program reconstructs original truncated t-series by Pascal-generated q^j-1 edges. It tests all 34 even-(p,c) cases at p=3,5,7,11,13,17,19, including every shifted p block, full t and alpha residuals, first-deleted tails, and original ordinary derivatives. All truncation precisions are below the least actual e for s=4. Its exhaustive 221,918 joining subsets check the full and deleted path classifications and strict derivative gaps. Rational ledgers cover all 2,090 even-(p,c) pairs for odd primes through 199. The result is 5,254,320 explicit passing checks.

A separate fresh finite-field program verifies full original transfer, all four differentiated terms, full H/P coefficient identities, and the algebraic-square CD polynomial identity in 81 fixtures. These comprise all 54 primitive order-81 phases modulo 811, six order-243 phases modulo 2917, both even middle digits at six order-625 phases modulo 13751, and all three even middle digits at three order-2401 phases modulo 28813. All reductions in these fixtures happen to be squarefree; that observation is not needed by the proof and is not promoted to universal good reduction. The author/inherited modulo-163 bad-reduction example is not a characteristic-zero exception. The finite program has 474 explicit passing checks.

Nine explicit negative mathematical controls reject the universal g-unit shortcut at four cancellation pairs, differentiation of the inseparable alpha residual, three odd-c constant-unit extrapolations, and the old shallow-tail constant scale. The read-only source program has 686 explicit passing checks and rejects seven in-memory inventory mutations: missing file, extra file, changed bytes, wrong declared length, wrong digest, duplicate entry, and path traversal. All four reviewer control suites pass normally and under Python -O with byte-identical JSON. Failures use explicit exceptions, not removable assertions. No candidate/dependency checker is run.

This acceptance establishes the exact original P/H squarefreeness, kernel nonvanishing, exhaustive no-zero root count, coarse alpha classes and every stated ordinary derivative valuation for the frozen even sector. It does not establish odd 3<=c<p, p=2, s<=3, arbitrary degrees, composite orders, global F020/F023 closure, historical novelty, an FFT/cost claim, public-artifact equivalence, repository/table authorization, or recovery/acceptance of the historical b=2p original bytes.
