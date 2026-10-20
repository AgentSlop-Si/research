# Fresh full-family adversarial audit: F020 even low digits

20 October 2026 UTC. This is a fresh audit of the finished full-family candidate, separate from the exploratory reviewer whose overlapping tail suggestion is disclosed in its ATTRIBUTION.md. I supplied no proof lemma or correction to the author. This review uses exact original normalizations, independently reconstructs the unlimited proof, and binds the frozen candidate below. No external state was changed.

## 1. Verdict and exact accepted scope

**PASS, with no mathematical revision requested**, for the frozen candidate:

- Author REPORT.md SHA-256: aa6dc8a3181a8064261ddaf5012584139b522860f5fe51ba8aa27b94ead3d83f
- Author MANIFEST.json SHA-256: 3cb73ce47384069bcaa2570bb93cb5df6658916f791165de38b5200ac7fa7c5d

The accepted scope is every odd prime p, every r>=2 and s>r, every odd low digit 1<=d=2c+1<p, degree n=N+d with N=p^r, and every characteristic-zero primitive p^s-th root q. Use the original polynomials

    P_0=1, P_1=X, P_(j+1)=X P_j-(1-q^j)P_(j-1),
    H_n(z)=sum_a [n choose a]_q z^a.

Normalize v(q-1)=1. Set h=floor(r/2), beta=p^h, alpha=beta-1 for even r and alpha=beta for odd r, B=r(p-1)p^(r-1)/2, and D=N+B-p. The accepted conclusions are:

- Every root of both original P_n and H_n is simple.
- Exactly 2c P_n roots have valuation 1/2, with ordinary derivative valuation (n-1)/2.
- The remaining N+1 roots are nonzero, have valuation greater than 1/2, and all lie in the closed alpha disks centered at x_a=i(q^(a/2)-q^(-a/2)), 0<=a<beta.
- At an inner P_n root xi with x=v(xi), the ordinary derivative has exact valuation c+x+min(D,N+B-2x). Such x is either 1, a power p^j>=p arising from a noncentral disk, or at least alpha in the central disk. In particular x is never p/2.
- The corresponding H_n roots satisfy v(z+1)=v(xi), belong to the asserted H disks, and have the same derivative valuations.
- At every P_n root, the original algebraic-square kernel sum_(j<n) P_j(xi)^2/(q;q)_j is nonzero.

The requested n=p^r+1 case is c=0. This fresh verdict explicitly includes the entire odd-tail extension, not merely c=0. It does not accept d=p, intermediate digits, larger leading digits, arbitrary degrees below p^s, arbitrary odd composite orders, or any global F020/F023 closure. It makes no novelty or historical-priority assertion. Earlier accepted dependencies remain unchanged.

## 2. Exact ordinary identities and valuation framework

I reconstructed the formal generating argument. Write w_m=(q;q)_m and E(x)=sum x^m/w_m. The equation E(qx)=(1-x)E(x) gives the even series E(x)E(-x)=sum x^(2u)/(q^2;q^2)_u. The quotient E(zx)/E(-x) has coefficients N_k(z)/w_k with N_k(z)=product_(j=0)^(k-1)(z+q^j), by its functional equation. Multiplying the two series yields the Newton expansion for every degree b, with k congruent to b modulo 2. The even expansion retains k=0.

Ordinary differentiation gives the logarithmic derivative sum_(j>=1) z^(j-1)x^j/(1-q^j), hence the full double sum for H_b'. These are characteristic-zero formal identities, and the relevant finite denominators do not vanish at the actual q. No q derivative or derivative of a Frobenius residual is substituted. The independent checker reconstructs the original H and P recurrences at q=3/2,-3,5 and verifies both parity identities, the full algebraic-square CD identity, and the shifted continuant identity through degree 13. These are transcription controls; the formal argument proves the identities without a finite-degree restriction.

For j<p^s, v(1-q^j)=p^ord_p(j), and v(p)=e=p^(s-1)(p-1). Thus W(m)=sum_(j=1)^m p^ord_p(j) is the exact valuation of w_m. The functions T and R in the candidate really are capped consecutive-distance sums and their tails. For even r the replacement T=T_h-floor(m/beta) changes the top cap from beta to beta-1, rather than making an informal approximation to the old disks. The top increment alpha-p^(h-1) is positive, including p=3,r=2.

On an alpha disk, each consecutive length-m product has coefficientwise weight at least T(m). Outside all such disks, choose a center maximizing delta=v(z+q^a). Then every distance equals min(delta,p^ord_p(j-a)); a cancellation in the equal-valuation case would contradict maximality. Counting a residue class modulo each p^b yields the strict estimate for every consecutive length-l string:

    sum v(z+q^j) < alpha+T(l-1).

Strictness is valid at the endpoints: the top class either occurs, in which case its actual distance is less than alpha, or is absent, in which case its count is below the positive ceiling bound. No assumption that the closest center is -1 is made here. The later variable d0=v(X)=v(z+1) need not equal this maximizing delta.

## 3. The strengthened digit inequality, including the smallest endpoint

For even r=2h, write m=sum_(a=0)^(2h-1) d_a p^a and E_d=sum d_a. Since p is odd,

    floor(m/2)=sum_a d_a(p^a-1)/2+floor(E_d/2).

The floor expression for W proves superadditivity, and W((p^a-1)/2)=a(p-1)p^(a-1)/2. The contribution of the digit d_a to R_h, for a>h, is d_a(a-h)(p-1)p^(a-1). For a>=h, the remaining payment per digit, divided by p^(a-h), is

    (2h-a)(p-1)p^(h-1)/2 >= 1.

This pays exactly the extra floor(m/beta) in R. Lower-digit contributions are nonnegative. Thus

    W(floor(m/2)) >= R(m)+W(floor(E_d/2)).

For positive even m, E_d is positive even, so the last term is at least 1. This proves the required strict inequality only where it is needed, without falsely assuming strictness for odd m.

The limiting payment case p=3,r=2,h=1,a=1 is equality, not a failure: alpha=2, B=6, D=12, and R(3)=W(1)=1. Positive even m still has the separate digit-sum gap. The ordinary derivative proof uses the strict estimate for positive even m and only the non-strict estimate for odd m, so this exceptional equality causes no missing case.

For odd r=2h+1 the same digit argument has a<=2h and requires no extra payment, giving the accepted bound for R_h and its strict positive-even version. The complement formula R(u)+R(N-1-u)=R(N-1) follows termwise from floors in either definition. Endpoint evaluation gives

    B-R(N-1)=N-2beta+1                    (r even),
    B-R(N-1)=((p+1)/2)p^(r-1)-beta       (r odd).

Therefore C=N-alpha-[B-R(N-1)] equals beta for even r and ((p-1)/2)p^(r-1) for odd r; in both cases C>=alpha. This is the positive covering margin needed below. The modified cap is substantive: simply retaining the old even-r cap would not produce this margin.

## 4. Every enlarged disk: pure-power ordinary derivative and neighbor bounds

In the exact double derivative sum for H_N, the bound on a term is W(N) minus

    W((N-k)/2)+R(m)+p^ord_p(k-m).

At m=0, fixing a=ord_p(k) makes the maximum unique at k=p^a. Its value is B+g_a, where g_a=p^a-a(p-1)p^(a-1)/2. The increments are positive through a=2 and negative thereafter, giving the unique maximum B+p at a=2. This includes N=p^2, where k=p^2 is the endpoint, not an absent index.

For positive even m, the strengthened strict inequality and superadditivity give a strict reduction to the corresponding m=0 comparison for j=k-m. For odd m, j is even and W(j/2)>=p^ord_p(j), reducing the bracket to at most B. These three cases exhaust the entire double sum. Thus the surviving term is exactly L_N z^(p^2-1), with

    L_N=w_N/[(1-q^(p^2))(q^2;q^2)_((N-p^2)/2)],  v(L_N)=D.

Since z reduces to -1, this yields constant residual 1 after division by L_N on every enlarged alpha disk. It is a legitimate whole-disk assertion for the pure-power H_N', not an extrapolation from roots or special centers.

For H_(N-1), the k=0 term of the full even Newton expansion has weight B. Every positive even k term is strictly larger by R(k)<W(k/2) and superadditivity. For its ordinary derivative, let j=k-m. If m is even, j is even, and the bracket is bounded by W((N-1)/2-j/2)+p^ord_p(j)<=B. If m is odd, j is odd, and it is bounded by

    W((N-j)/2-1)+p^ord_p(j)=W((N-j)/2)<=B.

The equality uses ord_p((N-j)/2)=ord_p(j), valid for 0<j<N. This covers every derivative summand and does not require an unjustified strict inequality for odd m.

The original identity H_b(v0^2)=v0^b P_b(v0+v0^(-1)) has integral analytic inverse near v0=i because p is odd. The coordinate derivatives and needed prefactors are units. For P_N', its differentiated prefactor contributes N times an integral polynomial and hence weight at least r e>D; this holds uniformly since e>=N(p-1). For the neighbor, the differentiated prefactor contributes weight at least B. Therefore the exact bounds transfer to

    v(P_N')=D,  v(P_(N-1))=B,  v(P_(N-1)')>=B

on every enlarged disk. The candidate correctly does not assert these neighbor bounds throughout the larger region v(X)>=1.

## 5. Every admissible odd tail and the outer-root partition

The shifted continuant identity is exact with A_0=1,A_1=X and B_0=0,B_1=1:

    P_(N+d)=A_d P_N-(1-q^N)B_d P_(N-1).

For d=2c+1<p, all its internal shifted edges have valuation 1. With lambda^2=-(q-1), their reductions give the Hermite recurrence coefficients j. The coefficient of X in A_d has exact valuation c because the coefficient of Y in He_(2c+1) is (-1)^c(2c+1)!!, a nonzero residue for d<p. The constant coefficient of B_d is the unique product of the c alternating even shifted edges and also has exact valuation c. Higher coefficients have the bounds stated in the candidate. Hence for every nonzero X with x=v(X)>1/2,

    v(A_d)=c+x,  v(B_d)=c,  v(B_d/A_d)=-x.

Write A_d=X U(X^2), B_d=V(X^2). The composed-polynomial logarithmic derivatives U'/U and V'/V have valuation at least x-1, whereas 1/X has valuation -x. Since x>1/2, the latter is uniquely least. Consequently C_d'= (B_d/A_d)' has exact weight -2x. This is ordinary differentiation in X; the notation for composed U and V is read consistently. For c=0 the first two logarithmic derivative terms vanish, leaving the same conclusion.

The global scaled P recurrence is integral and reduces to He_n. The vanishing recurrence coefficient at every multiple of p gives He_(ap+d)=Y^(ap)He_d. Thus the residual is Y^N He_(2c+1). For d<p, the derivative identity He_d'=d He_(d-1) and downward recurrence prove separability. Its zero root is simple by the displayed linear coefficient; its other 2c roots are nonzero and simple. Only these 2c nonzero roots are lifted by simple-root Hensel lifting, giving their exact original derivative valuation (n-1)/2. The remaining N+1 roots, still counted with multiplicity, have valuation greater than 1/2.

The potential division issue at zero is explicitly resolved: P_N(0)=0, but P_(N-1)(0), B_d(0), and 1-q^N are all nonzero matching products. Hence P_n(0) is nonzero. Every inner root is nonzero, and the tail quotient is legitimate at each such root. No whole central-disk division by the odd polynomial A_d is claimed.

## 6. Complete root covering, including all split clusters and all neighbor terms

First, outside the alpha disks, the full odd Newton expansion of H_N is uniquely dominated by its monic N_N term. The consecutive-distance estimate gives each lower-term valuation difference strictly greater than N-alpha-W(u)+R(2u-1), which is nonnegative before the strict comparison by complementarity and the digit bound. Thus v(H_N)=v(N_N) at all such points.

Now suppose an inner P_n root xi lies outside every alpha disk, and put d0=v(xi)=v(z+1). Then 1/2<d0<alpha because the center -1 is present. After division by A_d and coordinate conversion, the perturbation multiplying H_(N-1) has exact weight N-d0; the additional coordinate factor v0 is a unit.

For EVERY term of the even expansion of H_(N-1), write k=N-1-2u, with 0<=u<=(N-1)/2. Its coefficient has exact weight W(2u)-W(u), by reflection below the pure power N. This includes u=0 and the final k=0 term. The removed consecutive string has length 2u+1. Consequently the perturbing term relative to N_N has weight difference strictly greater than

    N-d0-alpha-W(u)+R(2u).

The complement formula and superadditivity give

    W(u)-R(2u)
      =W(u)+R(N-1-2u)-R(N-1)
      <=B-R(N-1).

Thus every perturbing term is strictly above H_N by more than C-d0>0. Their sum cannot cancel H_N. This contradicts the root equation and proves that ALL N+1 inner roots are covered, with multiplicity allowed throughout the argument. No guess about the number of central roots enters the proof. Centers modulo beta suffice because their differences have valuation at least beta>=alpha.

The adverse exact example is preserved and independently reproduced: p=3,r=2,s=3 gives the P_10 lower hull (0,15),(4,6),(10,0). There are four central roots of valuation 9/4, not a pair of valuation 3/2. These roots are within alpha=2 and outside the old beta=3 central disk. The disproved two-root heuristic is not used anywhere in the accepted argument.

## 7. Root-only ordinary derivative elimination and the noncancellation barrier

Differentiate the exact quotient identity before evaluation. At an inner root, the term multiplying the derivative of A_d vanishes by the root equation, leaving

    P_n'(xi)=A_d(xi)[P_N'(xi)
      -(1-q^N)(C_d'(xi)P_(N-1)(xi)+C_d(xi)P_(N-1)'(xi))].

The first bracketed term has exact valuation D. The C_d' neighbor term has exact valuation B-2x, while the other neighbor derivative term has valuation at least B-x, strictly larger because x>0. The full perturbation therefore has exact valuation N+B-2x. Equality with D could occur only at 2x=p.

The complete cover excludes that value. The central disk gives x>=alpha>=p-1>p/2. For a noncentral representative 0<a<beta, the center has valuation p^ord_p(a)<=beta/p<alpha, forcing the same valuation for every point in its disk. It is either 1<p/2 or a power at least p>p/2. Thus the two bracketed terms have distinct valuations at EVERY inner root, and the derivative cannot vanish. Multiplication by A_d gives exactly the claimed derivative formula. Its two stated specializations, D+c+1 at x=1 and N+B+c-x at x>p/2, follow directly.

This is solely an ordinary derivative statement AT ROOTS for the mixed degree n. No nonzero constant residual for P_n' or H_n' on a whole translated disk is needed or asserted. Such an extension would already be impossible for P_n' on the central disk, since n is even and P_n'(0)=0. The proof's division and elimination are correctly restricted to the nonzero roots.

## 8. Coordinate transfer, algebraic-square kernels, and mixed characteristic

All P roots reduce to zero, and the relevant v0 values reduce to a square root of -1. The maps v0->v0+v0^(-1) and v0->v0^2 therefore have unit ordinary derivatives. The roots do not meet X=+/-2, and H_n(0)=1. On the branch near i, z+1=v0 X, so both the valuation partition and multiplicities transfer, and at roots the differentiated prefactor term vanishes. The ordinary derivative valuations for H and P are identical.

All relevant recurrence edges and w_(n-1) are nonzero since n<p^s. A common root of consecutive original P polynomials would propagate backwards to P_0=1, which is impossible. The exact original ordinary CD identity at a root is

    sum_(j<n) P_j(xi)^2/w_j=P_n'(xi)P_(n-1)(xi)/w_(n-1).

Every factor on the right is nonzero. These are algebraic squares, not absolute-value squares. No real-rootedness, positivity, or complex interlacing argument is used. The algebraic nonvanishing established in a p-adic embedding transfers to every primitive characteristic-zero embedding.

There is no hidden requirement D<e. The exact finite-field-factor valuations and ordinary identities are valid above ramification. The independent actual-field code reconstructs original H and P in Z[q]/Phi_(p^s), reduces to degree less than e, and converts each coefficient to q=1+t by the direct binomial formula. For 0<=j<e, the weights j+e ord_p(c_j) are distinct modulo e, making their minimum exact even when it exceeds e. The residue conversion p/t^e=-1 is retained, not discarded. Ordinary derivatives are taken on the exact characteristic-zero polynomial BEFORE translated-disk evaluation.

## 9. Independent controls, replay, and frozen-byte conclusions

check_independent.py uses only the Python standard library and imports no author or earlier reviewer implementation. It records:

- 119 prime/exponent integer grids: p=3,5,7,11,13,19,37 and 2<=r<=18. Small ranges are exhaustive; larger ones use boundary points and a fixed random seed. Tests include strengthened digit inequalities, strict even cases, complementarity, both covering estimates, the unique pure-power derivative winner, and every neighbor derivative case on exhaustive small grids.
- Independent rational recurrence checks through degree 13 for both-parity Newton expansions, ordinary derivatives, the full algebraic-square CD identity, and shifted tails.
- Exact mixed-characteristic cases (3,2,3), (3,2,4), (3,3,4), (3,4,5), (5,2,3), and (7,2,3). Every alpha-center is checked in the first five cases, and centers 0,1,6 in the last. These verify H_N' constant residual INCLUDING its exact L_N unit, H_(N-1) constant-unit bounds, and ordinary neighbor derivative bounds.
- Exact shifted A_d/B_d leading units and coefficient weights for EVERY odd 1<=d<p in all those cases, plus original-P Newton hulls for all those degrees. Every hull has exactly 2c roots of valuation 1/2 and N+1 inner roots, with no valuation p/2. The N=81 case checks all nine enlarged disks with D=186>e=162. A larger-s case independently checks that the argument is not tied to minimal ramification.

The exact controls all passed. They are falsification and transcription controls, not finite substitutes for Sections 2-8.

The candidate's check_exact.py and check_adverse_hulls.py were separately replayed in an isolated temporary copy. Every mathematical value in EXACT_CHECKS.json agreed after removing elapsed-time fields; the adverse-hull output agreed byte-for-byte. The original candidate was verified again afterwards and remained unchanged.

verify_frozen.py validates the expected report and manifest hashes, the seal, all 14 manifest entries, the exact candidate inventory, and all four retained source bindings. The retained accepted pure-power and odd-low-digit reports/reviews additionally matched their original local bytes. These are retained local sources, not fresh remote retrievals. No source chronology beyond available evidence is inferred; the candidate's attribution disclosure is preserved, and this separate final audit certifies the complete frozen proof independently of the exploratory overlap.

VERDICT.json provides the machine-readable acceptance and precise limitations. MANIFEST.json and SEAL.sha256 bind this completed review package. No external write, repository mutation, new delegation, arbitrary-degree inference, or global closure is part of this verdict.
