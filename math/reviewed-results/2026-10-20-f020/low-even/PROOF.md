# F020: the even-degree low-digit family

20 October 2026 UTC. Author candidate for fresh independent review. No external state was changed. This proof addresses an unlimited even-degree family rather than a finite degree ladder.

## 1. Exact statement and limitations

Let p be an odd prime, r>=2, s>r, N=p^r, and q a characteristic-zero primitive p^s-th root. Normalize v(q-1)=1. Use the ORIGINAL polynomials

    P_0=1, P_1=X, P_(j+1)=X P_j-(1-q^j)P_(j-1),
    H_j(z)=sum_(a=0)^j [j choose a]_q z^a.

Let d=2c+1 satisfy 1<=d<p and set n=N+d. Define

    h=floor(r/2), beta=p^h,
    alpha=beta-1 if r is even, and alpha=beta if r is odd,
    B=r(p-1)p^(r-1)/2, D=N+B-p.

Then every root of BOTH original polynomials P_n and H_n is simple. At every P_n root xi, the original algebraic-square kernel

    K_n(xi)=sum_(j=0)^(n-1) P_j(xi)^2/(q;q)_j

is nonzero. More precisely:

* Exactly 2c roots have valuation 1/2. Their original ordinary derivatives have valuation (n-1)/2.
* The remaining N+1 roots have valuation >1/2 and lie in the closed disks v(X-x_a)>=alpha, 0<=a<beta, where x_a=i(q^(a/2)-q^(-a/2)), i^2=-1, and q^(a/2) is the square root congruent to 1.
* At each inner root, putting x=v(xi), the derivative valuation is

      c+x+min(D,N+B-2x).

  In particular it is D+c+1 when x=1, and N+B+c-x when x>p/2. These exhaust the inner roots: their valuations are 1, powers p^j>=p, or at least alpha>p/2. No root has valuation p/2.
* The H_n roots have the identical partition and derivative valuations under v(z+1)=v(X), with disks v(z+q^a)>=alpha.

The requested case n=p^r+1 is c=0. The SAME proof uniformly covers every odd low digit d<p, so the statement is n=p^r+2c+1<p^r+p, with no intermediate digits. It does not cover d=p, arbitrary leading or intermediate digits, arbitrary degrees below p^s, or arbitrary odd-composite orders. No global F020/F023 closure or novelty claim is made.

The two-root near-zero guess is false: already at p=3,r=2,s=3, the exact P_10 Newton hull has vertices (0,15),(4,6),(10,0), so there are FOUR roots of valuation 9/4, not a pair of valuation 3/2. The proof below includes those split roots and every other root without guessing their multiplicities.

## 2. Exact identities and the modified valuation functions

Write w_m=(q;q)_m and W(m)=sum_(j=1)^m p^ord_p(j). For 0<j<p^s, v(1-q^j)=p^ord_p(j). Put

    T_h(m)=m+sum_(b=1)^h (p^b-p^(b-1)) floor(m/p^b),
    R_h(m)=W(m)-T_h(m), A=(N-1)/2.

For odd r retain T=T_h and R=R_h. For EVEN r replace them by

    T(m)=T_h(m)-floor(m/beta),
    R(m)=R_h(m)+floor(m/beta).

Equivalently T is the sum of capped consecutive valuations with cap alpha: its top increment is alpha-p^(h-1), which is positive. Consequently, on ANY disk v(z+q^a)>=alpha, the coefficientwise weight of N_m(z)=product_(j=0)^(m-1)(z+q^j) is at least T(m). Outside all such disks, choose a maximizing delta=v(z+q^a)<alpha, 0<=a<N. For every consecutive string of length l>=1,

    sum v(z+q^j)<alpha+T(l-1).                         (2.1)

Indeed count each residue class modulo p^b, b<=h, using at most ceil(l/p^b) terms, with top increment alpha-p^(h-1). The equality ceil(l/p^b)=1+floor((l-1)/p^b) gives the right side. Strictness holds because an index in the top class has actual distance delta<alpha, or the top class is absent and its count is strictly below the upper bound. The maximizing choice ensures each distance equals min(delta,p^ord_p(j-a)), including a coincident valuation. This is the same geometric counting argument as the accepted proof, with its cap explicitly changed.

The exact BOTH-PARITY Newton and ordinary derivative identities are

    H_b(z)=sum_(0<=k<=b, k=b mod 2)
      w_b N_k(z)/[w_k (q^2;q^2)_((b-k)/2)],             (2.2)

    H_b'(z)=sum_(k=b mod 2,k>=1) sum_(0<=m<k)
      w_b z^(k-m-1)N_m(z)
      /[(q^2;q^2)_((b-k)/2) w_m (1-q^(k-m))].         (2.3)

In particular k=0 is retained for even b. These formal characteristic-zero identities follow from E(zx)/E(-x), E(x)=sum x^j/w_j, and its ORDINARY z derivative, as derived in the retained accepted sources. Every denominator is nonzero at the actual q. Neither a q derivative nor differentiation of a repeated characteristic-p residual substitutes for (2.3).

## 3. The strengthened even-r digit inequality

The essential bounds, valid for BOTH definitions of R above, are

    R(m)<=W(floor(m/2)) for 0<=m<N,
    R(m)<W(m/2) for positive even m<N,               (3.1)
    R(u)+R(N-1-u)=R(N-1), 0<=u<N.                  (3.2)

For odd r these are the accepted pure-power bounds. For r=2h we now prove the strengthened version. Write m=sum_(a=0)^(2h-1) d_a p^a and let e_d=sum d_a. The exact identity

    floor(m/2)=sum_a d_a(p^a-1)/2+floor(e_d/2)

and superadditivity of W give

    W(floor(m/2))>=sum_a d_a a(p-1)p^(a-1)/2
                        +W(floor(e_d/2)),

where the a=0 summand is zero. The contribution to R_h from a>h is d_a(a-h)(p-1)p^(a-1), and it is zero for a<=h. Thus for every a>=h the slack in this digit comparison is

    d_a(2h-a)(p-1)p^(a-1)/2 >= d_a p^(a-h),

because a<=2h-1 and (p-1)p^(h-1)>=2. Summing these inequalities pays for floor(m/beta). The remaining lower-digit contributions are nonnegative. Therefore

    W(floor(m/2))>=R_h(m)+floor(m/beta)+W(floor(e_d/2)).

This proves (3.1). If m is positive even, e_d is positive even, so the final W term is >=1, proving strictness. This is an unlimited digit argument, not a sampled inequality.

The complement formula (3.2) follows termwise from floors since N is divisible by every p-power in R. Also W(A)=B and

    B-R(N-1)=N-2beta+1                     if r=2h,
    B-R(N-1)=((p+1)/2)p^(r-1)-beta         if r=2h+1. (3.3)

Define the useful covering margin

    C=N-alpha-[B-R(N-1)].

Then C=beta in the even-r case, and C=((p-1)/2)p^(r-1) in the odd-r case. In both cases C>=alpha, with strict inequality in the even-r case. We will use d0<alpha, so C-d0>0 regardless of equality at endpoints.

## 4. Pure-power and neighboring bounds on the ENLARGED disks

On each alpha disk, the accepted double-summand proof applies with T and R from Section 2 and (3.1). In (2.3) for H_N, every term has weight at least

    W(N)-[W((N-k)/2)+R(m)+p^ord_p(k-m)].

The bracket has its unique maximum B+p at (k,m)=(p^2,0): for m=0 this is the accepted exact maximization of

    W((N-p^a)/2)+p^a = B+p^a-a(p-1)p^(a-1)/2.

For positive even m, strict (3.1) and superadditivity reduce to a STRICTLY smaller value than the m=0 maximum for j=k-m. For odd m, j is even, and the bracket is <=B because W(j/2)>=p^ord_p(j). These are exactly the exhaustive parity cases, with the stronger R bound now justified.

Thus H_N' has coefficientwise constant unit residual after division by

    L_N=w_N/[(1-q^(p^2))(q^2;q^2)_((N-p^2)/2)],
    v(L_N)=D.

Its leading factor z^(p^2-1) reduces to 1. All other double terms have a strictly larger weight. Hence this is a true whole-disk ordinary derivative bound, not a value transported by guessing at distinguished geometric centers.

The original coordinate identity is H_b(v0^2)=v0^b P_b(v0+v0^(-1)). The branch near i has unit ordinary derivatives because p is odd. It maps the stated P disks to the H disks. In the differentiated identity for P_N, the prefactor derivative term has weight at least v(N)=r v(p)>D, since P_N is integral and v(p)>=N(p-1). Therefore

    v(P_N')=D                                                   (4.1)

coefficientwise as a constant-unit residual on EVERY enlarged disk.

The neighboring bounds also extend:

    v(P_(N-1))=B,     v(P_(N-1)')>=B.                            (4.2)

For H_(N-1), the k=0 term in (2.2) has weight B. For positive even k, strict (3.1) and superadditivity give W(A-k/2)+R(k)<B, so every other term has weight >B. For the ordinary derivative, each term has weight at least 2B minus

    W((N-1-k)/2)+R(m)+p^ord_p(j), j=k-m.

If m is even, j is even, and (3.1) bounds this bracket by W(A-j/2)+p^ord_p(j)<=B. If m is odd, j is odd and less than N; it is bounded by

    W((N-j)/2-1)+p^ord_p(j)=W((N-j)/2)<=B,

because ord_p((N-j)/2)=ord_p(j). The analytic coordinate transfer and differentiated unit prefactor preserve the bounds. These statements concern the enlarged alpha disks, not the whole region v(X)>=1.

For later use H_N is also dominated by its monic Newton term outside the alpha disks. For k=N-2u, comparison with N_N using (2.1) gives the strict lower bound

    N-alpha-W(u)+R(2u-1).

Complementation and (3.1) imply W(u)-R(2u-1)<=B-R(N-1)<=N-alpha. Therefore all other terms have greater weight, proving the assertion without assuming simplicity or root locations.

## 5. Odd shifted tails and the outer-root partition

Put a_j=1-q^j and define A_d,B_d by

    A_0=1, A_1=X; B_0=0, B_1=1,
    A_j=X A_(j-1)-a_(N+j-1)A_(j-2),
    B_j=X B_(j-1)-a_(N+j-1)B_(j-2).

The exact original recurrence gives

    P_(N+d)=A_d P_N-a_N B_d P_(N-1).                          (5.1)

For d=2c+1<p and any x=v(X)>1/2,

    v(A_d)=c+x,  v(B_d)=c,
    v(C_d)=-x,  v(C_d')=-2x,  C_d=B_d/A_d.                   (5.2)

Here X is nonzero. To prove the needed unit assertions, all shifted internal edges have weight 1 and a_(N+j)/(-t) reduces to j. After scaling by lambda^2=-t, the tail A_d reduces to He_d, the monic Hermite polynomial in characteristic p. Its coefficient of Y is (-1)^c(2c+1)!!, nonzero because d<p. Thus the coefficient of X in A_d has exact weight c. Its X^(2j+1) coefficient has weight >=c-j. Similarly B_d is even, its constant is the unique matching product of the even shifted edges and has weight c; its X^(2j) coefficient has weight >=c-j. Every higher term is strictly larger when x>1/2. Write A_d=X U(X^2), B_d=V(X^2). The ordinary logarithmic derivative satisfies

    C_d'/C_d=V'/V-U'/U-1/X,

where here U,V denote the composed polynomials in X. Each of the first two terms has weight >=x-1>-x. Therefore the last term is uniquely least, proving the exact derivative weight in (5.2). No division by A_d at X=0 is made.

For completeness, lambda^(-n)P_n(lambda Y) is integral and reduces to He_n(Y). The monic recurrence He_(j+1)=Y He_j-j He_(j-1) in characteristic p gives He_p=Y^p and blockwise He_(ap+d)=Y^(ap)He_d for d<p. Hence the reduction is Y^N He_(2c+1)(Y). He_(2c+1) is separable: its derivative is (2c+1)He_(2c), and consecutive polynomials are coprime by their recurrence with nonzero coefficients below p. Its zero root is simple because the displayed coefficient of Y is nonzero. Thus its 2c nonzero roots lift simply to roots with valuation 1/2, with original derivative weight (n-1)/2. All remaining N+1 roots, counted with multiplicity at this point, have valuation >1/2. No simple-root lifting is applied to the repeated zero factor.

Finally P_n(0)=-a_N B_d(0)P_(N-1)(0) is nonzero: B_d(0) is the matching product just described and P_(N-1)(0) is its original nonzero odd-edge product. Thus every inner root is nonzero and (5.2) can be used there.

## 6. Complete even root covering, INCLUDING split clusters

Take an inner root xi and choose the branch v0 near i, so v0 and z=v0^2 are units and v(z+1)=x=v(xi)>1/2. Suppose it lies outside EVERY alpha disk. Then d0=x<alpha because the center -1 is among the disks. By Section 4, H_N has the exact valuation of N_N there.

For k=N-1-2u, 0<=u<=A, the k-th term in the FULL EVEN expansion of H_(N-1) has coefficient weight

    W(N-1)-W(k)-W(u)=W(2u)-W(u),

using reflection below N. In (5.1), (5.2) shows that the perturbing term after division by A_d has the extra weight N-d0. Relative to H_N, the k-th perturbing Newton term therefore has weight difference

    N-d0+W(2u)-W(u)-sum_(j=k)^(N-1) v(z+q^j)
      > N-d0-alpha-W(u)+R(2u).                              (6.1)

The consecutive string has length 2u+1, including u=0. By (3.2), (3.1), and superadditivity,

    W(u)-R(2u)
      =W(u)+R(N-1-2u)-R(N-1)
      <=W(u)+W(A-u)-R(N-1)
      <=B-R(N-1).

Thus (6.1) is >C-d0>0, with C from Section 3. Every perturbing term has greater weight than H_N. They cannot cancel H_N, contradicting the root equation (5.1). This covers ALL N+1 inner roots, with multiplicities allowed throughout the argument. Centers modulo beta suffice because their differences then have valuation at least beta>=alpha.

This is why the modification alpha=beta-1 is substantive. Retaining the old even-r cap beta would give C=0 in this calculation and no positive margin. Merely studying the central split or applying the old covering inequality does not prove the theorem.

## 7. Root-dependent ordinary derivative separation

At an inner root, divide (5.1) by A_d, differentiate BEFORE evaluation, and use the root equation. The exact identity is

    P_n'(xi)=A_d(xi)[P_N'(xi)
      -a_N(C_d'(xi)P_(N-1)(xi)+C_d(xi)P_(N-1)'(xi))].       (7.1)

The first bracketed term has valuation D by (4.1). By (4.2) and (5.2), the C_d'P_(N-1) term has exact weight B-2x, whereas C_d P_(N-1)' has weight at least B-x>B-2x. The full perturbation therefore has exact weight N+B-2x. Equality with D could occur only if 2x=p.

That equality is impossible from the COMPLETE covering just proved. The central disk has x>=alpha, and alpha>=p-1>p/2. Every other disk has x=v(x_a)=p^ord_p(a)<=beta/p<alpha. Such an x is either 1<p/2 or at least p>p/2. Hence the two bracketed terms have distinct valuations and cannot cancel. Formula (7.1) proves precisely

    v(P_n'(xi))=c+x+min(D,N+B-2x),

which is finite. This is a derivative statement AT ROOTS. No constant residual for P_n' on a whole translated disk is asserted.

The exact coordinate identity, whose two ordinary coordinate derivatives and unit factors are nonzero units over these roots, transfers multiplicities and derivative valuations to H_n. Roots of P_n reduce to zero and do not meet X=+/-2, and H_n(0)=1, so there is no ramified-coordinate exception.

## 8. The original algebraic-square kernel

Every recurrence edge a_j is nonzero for j<n<p^s. Consecutive P_n and P_(n-1) cannot share a root: the original recurrence would propagate it to P_0=1. The original ordinary Christoffel-Darboux identity evaluated at a P_n root is

    sum_(j=0)^(n-1) P_j(xi)^2/w_j
       =P_n'(xi)P_(n-1)(xi)/w_(n-1).

All factors on the right are nonzero. These are algebraic squares, not absolute-value squares; no positivity, real-rootedness, or complex interlacing argument is used. The proof is in an algebraic p-adic embedding, and algebraic nonvanishing transfers to every characteristic-zero primitive embedding by injectivity and Galois conjugacy.

## 9. Controls and frozen review

The accepted pure-power proof and its fresh challenge, the accepted odd-low-digit proof, and its audit are retained byte-for-byte and identified by SOURCE_BINDINGS.json. They are local sources, not fresh remote retrievals. The new strengthened digit inequality, cap modification, root cover, and odd-tail derivative argument are proved above rather than imported from an accepted even-degree result.

check_exact.py reconstructs the original recurrence and both-parity Newton identities over rational q; verifies the exact shifted-tail and ordinary algebraic-square CD identities; checks Hermite and digit/margin controls on stated finite grids; and computes exact mixed-characteristic H_N derivative and H_(N-1) disk bounds. Actual-field checks use Z[q]/Phi_(p^s), exact q=1+t conversion, and coefficient weights j+phi(p^s)ord_p(c_j) with j<phi(p^s). These weights are distinct modulo phi(p^s), so their minimum is exact even above ramification. No floating roots or characteristic-p truncation substitutes for this arithmetic. Finite grids are falsification and transcription controls only, not the proof of the unlimited theorem.

ATTRIBUTION.md records the exploratory-review overlap and why the expanded family is being submitted for a new final audit. MANIFEST.json and SEAL.sha256 bind the finished package. This author candidate requires a fresh independent audit of these frozen bytes before acceptance. Earlier accepted packages and global owner scope remain unchanged.
