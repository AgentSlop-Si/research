# F020: the complete single-leading-digit family n = c p^r

20 October 2026 UTC. Author candidate for a separate fresh audit. No external state was changed. This proof extends the accepted leading-two family; it does not assert arbitrary base-p digits.

## 1. Theorem in the original normalizations

Let p be an odd prime, r >= 2, s > r, 1 <= c < p, N = p^r, n = cN, and q a characteristic-zero primitive p^s-th root. Work in an algebraic p-adic embedding, normalize v(q-1)=1, and put

    P_0 = 1, P_1 = X,
    P_(j+1) = X P_j - (1-q^j) P_(j-1),
    H_j(z) = sum_(a=0)^j [j choose a]_q z^a,
    w_j = (q;q)_j,
    B = r(p-1)p^(r-1)/2,
    h = floor(r/2), beta = p^h, L = N/beta,
    rho = beta/2                       if r is even,
    rho = p^(h-1)(2p-1)/2              if r is odd,
    D_c = (c+1)N/2 + cB - p.

Then BOTH original polynomials H_n and P_n are squarefree. At EVERY root their original ordinary derivative has valuation D_c. In particular

    v(Disc H_n) = v(Disc P_n) = n D_c.

All H_n roots belong to the beta pairwise disjoint closed disks

    v(z+q^a) >= rho, 0 <= a < beta.

Every disk has exactly cL roots, with multiplicity counted before squarefreeness is proved. If c is even, all cL roots lie on its boundary. If c is odd, exactly L roots lie in its strict interior and exactly (c-1)L lie on its boundary. The theorem makes no assertion about the deeper geometry of those L interior roots.

There is a precise residual description. Choose omega with omega^2=w_N and lambda with v(lambda)=rho. On each disk put z=-q^a+lambda Y and let

    X_a(Y) = N_N(-q^a+lambda Y)/omega,
    N_k(z) = product_(j=0)^(k-1) (z+q^j), N_0=1.

The reduction of X_a is alpha_a Y^L, alpha_a != 0. Define the monic integer polynomial

    M_c(X) = c! sum_(k=0)^floor(c/2) X^(c-2k)/[2^k k! (c-2k)!].

Then the normalized original polynomial has reduction

    H_n(-q^a+lambda Y)/omega^c  ->  M_c(alpha_a Y^L).

With A=(N-p^2)/2 and

    C_1 = w_N / [(q^2;q^2)_A (1-q^(p^2))],

the normalized ORIGINAL ORDINARY derivative has reduction

    H_n'(-q^a+lambda Y)/(C_1 omega^(c-1))
        -> c M_(c-1)(alpha_a Y^L).

Here v(C_1 omega^(c-1))=D_c. The polynomials M_c and c M_(c-1) are coprime over characteristic p because c<p. Thus the derivative reduction is nonzero at every root of the polynomial reduction, including Y=0 when c is odd. No derivative of the repeated polynomial in Y is used.

The corresponding P disks have centers

    x_a = i(q^(a/2)-q^(-a/2)), i^2=-1,

using square roots congruent to 1. Their radii, counts, interior/boundary conclusions, and derivative valuations are the same. At every P_n root xi, the ORIGINAL algebraic-square kernel is nonzero:

    sum_(j=0)^(n-1) P_j(xi)^2/w_j != 0.

This is uniform in all stated p,r,s,c. It does not prove arbitrary intermediate digits, arbitrary n<p^s, odd-composite orders, or global F020/F023 closure.

## 2. Exact identities before reduction

Because n<p^s, all denominator factors used here are nonzero. For positive j<=n,

    v(1-q^j)=p^ord_p(j).

The factors 1-q^(2j) appearing below also have 2j<=n<p^s and the same valuation as 1-q^j. Write

    W(m)=sum_(j=1)^m p^ord_p(j), Q_m=(q^2;q^2)_m.

The exact Newton and ordinary derivative identities are

    H_b(z)=sum_(0<=k<=b, k=b mod 2) w_b N_k(z)/(w_k Q_((b-k)/2)),       (2.1)

    H_b'(z)=sum_(k=b mod 2, k>=1) sum_(0<=m<k)
        w_b z^(k-m-1) N_m(z)/(Q_((b-k)/2) w_m (1-q^(k-m))).           (2.2)

For completeness, let E(x)=sum x^j/w_j as a formal series over Q(q). The identities E(qx)=(1-x)E(x), E(x)E(-x)=sum x^(2u)/Q_u, and E(zx)/E(-x)=sum N_k(z)x^k/w_k give (2.1). Ordinary formal differentiation, using

    partial_z log(E(zx)/E(-x))=sum_(j>=1) z^(j-1)x^j/(1-q^j),

gives (2.2). Specialization is legitimate because no displayed denominator vanishes. This is ordinary differentiation in characteristic zero, not a q derivative and not differentiation after reduction. The k=0 term in (2.1) is included for even b.

## 3. The full single-digit half-W bound and complete root cover

Set

    T(m)=sum_(j=1)^m min(p^ord_p(j),rho), R(m)=W(m)-T(m).

We have p^(h-1)<rho<p^h and

    T(m)=m+sum_(b=1)^(h-1)(p^b-p^(b-1)) floor(m/p^b)
              +(rho-p^(h-1)) floor(m/p^h).                            (3.1)

Both W and R are linear in the base-p digits of m. For a<h, R(p^a)=0<W(p^a)/2. For h<=a<=r, substitution of either formula for rho gives

    R(p^a)=W(p^a)/2-(r-a)(p-1)p^(a-1)/2.                              (3.2)

Since m<=cN<p^(r+1), digitwise summation proves

    R(m)<=W(m)/2, with equality exactly at m=jN, 0<=j<=c.              (3.3)

Also W(N)=N+2B, W(jN)=jW(N), and T(jN)=R(jN)=jW(N)/2. The floor formulas give superadditivity W(x)+W(y)<=W(x+y). As every p-power in the floor formula for R divides n,

    R(x)+R(n-1-x)=R(n-1), 0<=x<n,
    R(n-1)=cW(N)/2-N+rho.                                            (3.4)

The last increment in R(n) is N-rho because ord_p(n)=r, not because n=N. For every 1<=u<=floor(n/2), (3.3)-(3.4) imply

    W(u)-R(2u-1)
      =W(u)+R(n-2u)-R(n-1)
      <=W(u)+W(n-2u)/2-R(n-1)
      <=W(n)/2-R(n-1)=N-rho.                                        (3.5)

The second inequality uses 2W(u)<=W(2u) and superadditivity.

To prove the complete cover, suppose z is outside all disks centered at -q^a for 0<=a<n, and choose a maximizing delta=v(z+q^a)<rho. For j!=a,

    v(z+q^j)=min(delta,p^ord_p(j-a)).

If the two entries coincide, a larger value would contradict maximality, so there is no cancellation exception. For any consecutive string of ell>=1 indices in 0,...,n-1, residue-class counting gives

    sum v(z+q^j) < rho+T(ell-1).                                    (3.6)

Indeed at each level p^b the count is at most ceil(ell/p^b)=1+floor((ell-1)/p^b), giving the non-strict bound using the positive increments in (3.1). If the top residue class occurs its actual contribution is strictly smaller because delta<rho; if absent its count is strictly smaller than the positive ceiling. For delta<1 strictness is immediate as well.

Compare a nonmonic Newton term k=n-2u to N_n. For 1<=j<n we have ord_p(n-j)=ord_p(j): if j is not a multiple of N this follows below level r; if j=tN with 1<=t<c, both j and n-j have order r because c<p. Thus the exact endpoint reflection is

    W(n)-W(n-2u)=N+W(2u-1).

Using (3.6), the valuation of this Newton term minus the valuation of N_n is strictly greater than

    N-rho-W(u)+R(2u-1)>=0

by (3.5). Therefore N_n uniquely dominates and H_n(z)!=0. This proves the cover without assuming simplicity. Centers congruent modulo beta give the same disk, whereas distinct residues modulo beta have center distance at most p^(h-1)<rho. The beta displayed disks are therefore disjoint and sufficient.

## 4. Coefficientwise weights and all block units

On z=-q^a+lambda Y, use the coefficientwise Gauss valuation, the minimum of coefficient valuations. A factor z+q^j has weight min(rho,p^ord_p(j-a)), with weight rho when j=a. Counting each residue class at least floor(k/p^b) times shows that N_k has weight at least T(k).

Consequently the k-th Newton term has weight at least

    W(n)-[R(k)+W((n-k)/2)] >= cW(N)/2.                               (4.1)

If k is not a multiple of N, the first half-W inequality is strict. Equality occurs exactly for k=jN with 0<=j<=c and j=c mod 2: then (n-k)/2=((c-j)/2)N and all digit counts are exact. This proves integrality after division by omega^c and excludes every other term from the residual.

We now establish the units, not only their valuations. For 0<=j<=c,

    w_(jN)/w_N^j -> j!.                                              (4.2)

To see this, split the numerator into blocks lN+i, 0<=l<j, 1<=i<=N. For i<N the ratio (1-q^(lN+i))/(1-q^i) reduces to 1, because the added exponent lN has valuation N strictly above p^ord_p(i). For i=N the ratio is a geometric sum and reduces to l+1. Multiplying gives j!, a nonzero residue because j<p. The case j=0 has value 1.

For 0<=t<=floor(c/2),

    Q_(tN)/w_N^t -> 2^t t!.                                         (4.3)

Indeed Q_(tN)/w_(tN)=product_(i=1)^(tN)(1+q^i) reduces to 2^(tN)=2^t in characteristic p, since N=p^r. Then use (4.2). All these quotients have valuation zero.

On any fixed disk, each block product N_N with its exponents shifted by lN has the same normalized initial polynomial as N_N itself. Every changed factor differs by q^i(q^(lN)-1), of valuation N>rho, while the unchanged factor has weight at most rho. Thus, coefficientwise,

    N_(jN)/omega^j -> (alpha_a Y^L)^j,                               (4.4)

where exactly L factors of N_N have indices congruent to a modulo beta. Those factors have initial term lambda Y; the others have nonzero constant initial terms. In particular alpha_a!=0. This statement does not divide by N_N and remains valid at Y=0.

Combining (4.2)-(4.4), the surviving Newton term j=c-2t reduces, after normalization by omega^c, to

    c! (alpha_a Y^L)^j/[j! 2^t t!].

Their sum is exactly M_c(alpha_a Y^L). No phase or unit is left unspecified beyond the common nonzero coordinate factor alpha_a.

## 5. Hermite coprimeness and exact disk counts

The polynomials M_j satisfy the integer identities

    M_0=1, M_1=X,
    M_j=X M_(j-1)+(j-1)M_(j-2),
    dM_j/dX=j M_(j-1).                                              (5.1)

They follow directly from the displayed coefficients (these coefficients are integers). For 1<=j<=c<p, all required recurrence multipliers and j are units in the residue field. A common root of M_c and M_(c-1) would propagate backward through (5.1) to M_0=1. Hence M_c and cM_(c-1) are coprime and M_c has c distinct roots in the algebraically closed residue field.

Since L=p^(r-h), the polynomial M_c(alpha_a Y^L) has c distinct residual root locations, each of multiplicity L. If c is even, its constant term is c!/[2^(c/2)(c/2)!], a unit. If c is odd, zero is a simple root of M_c, and therefore a root of multiplicity L of the Y residual.

The normalized translated H_n is integral, its reduction has degree cL and nonzero leading coefficient, and every coefficient above cL has positive valuation. The standard Newton-polygon count (or the equivalent distinguished-polynomial factorization on the closed unit disk) gives exactly cL roots with v(Y)>=0, counting multiplicity. Reduction multiplicities give L roots above each residual root location. In particular the zero residual accounts for exactly L roots with v(Y)>0 when c is odd, including any exact zero, and none when c is even. All remaining roots have v(Y)=0. These counts do not assume simple roots or apply simple-root Hensel lifting to a repeated residual. Their total beta*cL=n agrees with the independent all-root cover.

## 6. Every ordinary-derivative equality term and its unit

In (2.2), put d=k-m>=1 and a0=(n-k)/2. On a closed rho-disk, the (k,m) summand has weight at least

    W(n)-[W(a0)+R(m)+p^ord_p(d)].                                    (6.1)

Here z is a unit, reducing to -1. By half-W and superadditivity, the bracket is at most

    W(n-d)/2+p^ord_p(d)
      = cW(N)/2-N/2+[p^ord_p(d)-W(d-1)/2].                           (6.2)

The reflection is exact for 1<=d<=n, including d=n, by the same valuation symmetry used in Section 3.

The last square bracket has its UNIQUE maximum p at d=p^2. At a fixed b=ord_p(d), its unique maximum occurs at the smallest possible d=p^b, since W is strictly increasing. Its value is

    g_b=p^b-b(p-1)p^(b-1)/2,
    g_(b+1)-g_b=p^(b-1)(p-1)[p-b(p-1)]/2.

The difference is positive for b=0,1 and negative for all b>=2. The permitted range contains p^2 because r>=2 and n>=N. Thus no finite parameter search is needed.

Equality in (6.2) also forces m=lN by (3.3). Parity and the bound k=m+p^2<=n give exactly

    l=c-1,c-3,...,0 or 1,
    t=(c-1-l)/2,
    m=lN, k=lN+p^2, a0=tN+A, A=(N-p^2)/2.                        (6.3)

Conversely, all these pairs attain equality. The base-p digits of A are (p-1)/2 in positions 2,...,r-1 and zero elsewhere. Doubling A has no carries. Also 2t+l=c-1<p, so doubling a0 and adding m introduce no carries. Hence both superadditivity steps are equalities. The maximum bracket is cW(N)/2-N/2+p, and every other summand has strictly greater weight than D_c.

We must sum, not select one of, the surviving terms. Their exact expressions are

    w_(cN) z^(p^2-1) N_(lN)(z)/[Q_(tN+A) w_(lN)(1-q^(p^2))].         (6.4)

The needed shifted factorial identity is

    Q_(tN+A)/(Q_A w_N^t) -> 2^t t!.                                 (6.5)

Indeed divide first by Q_(tN)Q_A. The remaining product for 1<=i<=A is

    (1-q^(2tN+2i))/(1-q^(2i)),

and each ratio reduces to 1 since i<N and the added exponent 2tN has strictly larger valuation (t=0 is trivial). Then apply (4.3). This proves the phase identity for the actual shifted factorial rather than assuming it from valuation alone.

We have W(A)=B-p(p-1), so

    v(C_1)=W(N)-W(A)-p^2=N+B-p,
    v(C_1 omega^(c-1))=(c+1)N/2+cB-p=D_c.

Using (4.2), (4.4), and (6.5), the reduction of (6.4) divided by C_1 omega^(c-1) is

    c! (alpha_a Y^L)^l/[l! 2^t t!].

The factor z^(p^2-1) reduces to 1 because z reduces to -1 and p^2-1 is even. Summing exactly all equality terms yields

    c! sum_t (alpha_a Y^L)^(c-1-2t)/[2^t t! (c-1-2t)!]
       = c M_(c-1)(alpha_a Y^L).

At any root z of H_n, the complete cover makes Y integral and Section 4 gives M_c(alpha_a Ybar^L)=0. Section 5 gives c M_(c-1)(alpha_a Ybar^L)!=0. Thus the ORIGINAL ordinary derivative has valuation exactly D_c and is nonzero at EVERY root. This remains valid for all interior roots when c is odd, even though individual positive-l equality terms vanish there. It also remains valid when D_c exceeds v(p); the exact characteristic-zero identity and scalar normalization were retained throughout.

## 7. Transfer to original P derivatives, discriminants, and square kernels

The original coordinate identity is

    H_n(v0^2)=v0^n P_n(v0+v0^(-1)).                                  (7.1)

Modulo the maximal ideal P_n reduces to X^n, so its roots reduce to zero and are not +/-2. Also H_n(0)=1. At a corresponding root v0 reduces to +/-i; both ordinary coordinate derivatives 2v0 and 1-v0^(-2) are units since p is odd. Differentiating (7.1) BEFORE evaluating at a root kills the term proportional to P_n and transfers root multiplicity and derivative valuation exactly, up to units. The branch near i maps the H disks isometrically to the P disks centered at x_a stated above. This proves all P assertions without asserting an unjustified off-root P derivative identity.

Both polynomials are monic, so their discriminants, up to sign, are the products of their original derivatives at their roots. The valuation nD_c follows.

Every original recurrence edge 1-q^j with 1<=j<n is nonzero. Consecutive P_n,P_(n-1) cannot share a root, because recurrence propagation would contradict P_0=1. The ordinary diagonal Christoffel-Darboux identity at a P_n root xi is

    sum_(j=0)^(n-1) P_j(xi)^2/w_j
       =P_n'(xi) P_(n-1)(xi)/w_(n-1).

Every factor on the right is nonzero. These are algebraic squares, not absolute-value squares; no positivity, real-rootedness, interlacing, or Fourier assertion is used. Algebraic nonvanishing in this p-adic embedding transfers to the original algebraic polynomials and every characteristic-zero primitive embedding by Galois conjugacy.

## 8. Controls, attribution, and scope

The uniform proof is in Sections 2-7. The finite controls in check_exact.py are separate transcription/falsification checks: digit inequalities and complete equality sets, Hermite identities/coprimeness, original rational-q Newton/ordinary-derivative/H-P/CD identities, and actual cyclotomic mixed-characteristic coefficient valuations and units. The field controls use the original H recurrence in Z[q]/Phi_(p^s), translate its actual coefficients, then extract exact weights from q=1+t with degree below e=phi(p^s). The weights j+e ord_p(coefficient), for j<e, have distinct residues modulo e, so the minimum is exact even above e. The leading unit uses p/t^e reducing to -1. Expected field units are calculated from the proved block formulas, not fitted from actual coefficients.

The accepted leading-two report and its independent audit are retained byte-for-byte under sources and hash-bound. Their half-W cap and ordinary-derivative maximization provide the starting structure. A research collaborator supplied the UNPROVED general block/Hermite mechanism; this candidate proves its block units, shifted derivative units, equality sets, covering and original-normalization transfers. In particular odd c changes the geometry: strict-interior roots cannot be excluded. This is collaborative derivation, not independent acceptance. A separate auditor must bind the final frozen package. Wider F020/F023 scope is unchanged.
