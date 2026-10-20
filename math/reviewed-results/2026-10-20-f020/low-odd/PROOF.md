# F020: a uniform two-digit family beyond pure powers

20 October 2026 UTC. Candidate for independent adversarial review. No external mutation. The accepted pure-power theorem is used in its exact audited scope and retained byte-for-byte in sources/. This candidate is not yet independently accepted.

## 1. Statement in the original normalization

Let p be an odd prime, r>=2, s>r, N=p^r, and let q be a characteristic-zero primitive p^s-th root. Set t=q-1 and v(t)=1. Let

    P_0=1, P_1=X, P_(j+1)=X P_j-(1-q^j)P_(j-1),
    H_j(z)=sum_(a=0)^j [j choose a]_q z^a.

Choose any integer c with 0<=2c<p and put n=N+2c. Write

    h=floor(r/2), beta=p^h,
    B=r(p-1)p^(r-1)/2, D=N+B-p.

Then all roots of both original polynomials P_n and H_n are simple. More precisely:

- Exactly 2c P_n roots have valuation 1/2. At each of these roots the original ordinary derivative has valuation (n-1)/2.
- The remaining N P_n roots have valuation >1/2 and lie in the closed disks v(X-x_a)>=beta, where 0<=a<beta and

      x_a=i(q^(a/2)-q^(-a/2)), i^2=-1,

  with q^(a/2) the square root congruent to 1. At each of these roots the original ordinary derivative has valuation D+c.
- For H_n the same partition is obtained using v(z+1)=1/2 or >1/2, with the inner disks v(z+q^a)>=beta. The original ordinary H_n derivative has the same valuations as the corresponding P_n derivative.
- Consequently,

      v(Disc P_n)=v(Disc H_n)=N(D+c)+c(n-1).

- At every P_n root xi the original algebraic-square kernel

      K_n(xi)=sum_(j=0)^(n-1) P_j(xi)^2/(q;q)_j

  is nonzero.

This is a uniform family with arbitrarily large r and all admissible even low digits. For c>0 its base-p expansion has two nonzero digits, 1 in position r and 2c in position 0. It is not a finite degree ladder. The theorem does not include even degrees, a leading digit greater than one, arbitrary intermediate digits, arbitrary b<p^s, or arbitrary odd composite orders. No global F020/F023 closure is claimed.

## 2. Exact accepted input and finite identities

Put w_m=(q;q)_m, W(m)=sum_(j=1)^m p^ord_p(j), and

    T_h(m)=m+sum_(j=1)^h (p^j-p^(j-1))floor(m/p^j),
    R_h(m)=W(m)-T_h(m),
    A=(N-1)/2.

The accepted pure-power theorem supplies the following facts, for every indicated p,r,s, not merely on a finite grid:

1. R_h(m)<=W(floor(m/2)) for 0<=m<N, strictly for positive even m.
2. R_h(u)+R_h(N-1-u)=R_h(N-1) for 0<=u<N.
3. W(A)=B and B-R_h(N-1)<=N-beta.
4. On every disk v(z+q^a)>=beta, H_N' has a coefficientwise unit residual and exact valuation D. On the corresponding P disk the ORIGINAL ordinary derivative P_N' has a coefficientwise unit residual and valuation D.
5. The consecutive-string distance bound from the accepted root-cover proof: outside all these disks, choose a maximizing delta=v(z+q^a)<beta for 0<=a<N. For every consecutive string of l>=1 indices among 0,...,N-1,

      sum v(z+q^j)<beta+T_h(l-1).

All these inputs have proofs in the retained accepted report and independent review. W is superadditive, immediately from its floor formula. For all 0<j<=n<p^s, v(1-q^j)=p^ord_p(j).

The exact geometric Newton basis is N_k(z)=product_(j=0)^(k-1)(z+q^j). For every degree b (both parities),

    H_b(z)=sum_(0<=k<=b, k congruent b mod 2)
       w_b N_k(z)/[w_k(q^2;q^2)_((b-k)/2)].                 (2.1)

For even b the k=0 term MUST be retained. The exact ordinary derivative identity is

    H_b'(z)=sum_(k congruent b mod 2, k>=1) sum_(0<=m<k)
       w_b z^(k-m-1)N_m(z)
       /[(q^2;q^2)_((b-k)/2)w_m(1-q^(k-m))].              (2.2)

These follow formally from E(zx)/E(-x), E(x)=sum x^j/w_j, as proved in the accepted source. Every denominator is nonzero at the actual q. No q derivative or differentiation of a characteristic-p residual replaces the ordinary derivative.

## 3. The outer roots: a separable low digit, not a repeated-root inference

Adjoin lambda with lambda^2=-t, so v(lambda)=1/2. The scaled original recurrence shows Q_b(Y)=lambda^(-b)P_b(lambda Y) is monic and integral. Its reduction is the classical monic Hermite recurrence in characteristic p:

    He_0=1, He_1=Y, He_(j+1)=Y He_j-j He_(j-1).

Indeed (1-q^j)/(-t) reduces to j, including 0 when p divides j. The integer closed formula

    He_m(Y)=sum_(k=0)^floor(m/2)
       (-1)^k m!/[2^k k!(m-2k)!] Y^(m-2k)

proves He_p=Y^p modulo p: each coefficient with k>0 is divisible by p. The recurrence then gives, block by block,

    He_(ap+d)=Y^(ap) He_d,  0<=d<p.

At the block boundary, the coefficient ap in the recurrence is zero modulo p; this proves the induction without dividing by ap. In particular,

    Q_n mod maximal ideal = Y^N He_(2c)(Y).

For 0<2c<p, He_(2c) is separable: its ordinary derivative is 2c He_(2c-1), and consecutive Hermite polynomials are coprime by their recurrence and its nonzero coefficients 1,...,2c-1. Also He_(2c)(0)=(-1)^c(2c-1)!! is nonzero modulo p. For c=0 use He_0=1.

Therefore exactly 2c roots lift the nonzero simple residual roots. They have v(X)=1/2 and, since Q_n' is a unit there,

    v(P_n'(X))=(n-1)/2.

All remaining N roots, counted initially with multiplicity, have v(X)>1/2. This use of simple-root lifting concerns only the explicitly separable outer factor, never the repeated factor Y^N.

The exact identity H_b(v0^2)=v0^b P_b(v0+v0^(-1)) transfers this partition. Here v0 is a coordinate, not the valuation. Above the roots, v0 is a unit reducing to a square root of -1, and

    z+1=v0 X.

Thus v(z+1)=v(X). The coordinate derivatives are units because p is odd. Multiplicities and ordinary derivative valuations transfer exactly at roots.

## 4. Mixed-digit inner root covering: change the dominant term to k=N

Let H_n(z)=0 and v(z+1)>1/2. Suppose z is outside all beta disks from Section 1. In (2.1), compare every term with the k=N term, not with the monic k=n term. Its coefficient has valuation

    W(n)-W(N)-W(c)=2c-c=c.

For k=N+2a, 1<=a<=c, the relative term valuation is

    -a+sum_(j=N)^(N+2a-1) v(z+q^j)>0.                    (4.1)

Every distance in this sum is >1/2, because v(z+1)>1/2 and v(q^j-1)>=1. This explains why the old monic-term pivot must be replaced.

For k=N-2u<N, 1<=u<=A, exact reflection below the pure power still gives W(N)-W(k)=N+W(2u-1). The relative term valuation, using the accepted consecutive-string bound, is strictly greater than

    N-beta+c-W(u+c)+R_h(2u-1).                          (4.2)

The decisive new inequality is

    W(u+c)-c-R_h(2u-1)<=B-R_h(N-1)<=N-beta.              (4.3)

To prove its first inequality, complement the tail and use the accepted digit bound:

    W(u+c)+R_h(N-2u)
      <=W(u+c)+W(A-u)
      <=W(A+c)=B+c.

The last equality is exact: the low base-p digit of A is (p-1)/2, and adding c< p/2 creates no carry. Equivalently, every integer A+1,...,A+c is prime to p, so W(A+c)-W(A)=c.

Thus (4.2) is nonnegative before the strict distance inequality, and every k<N term also has strictly higher valuation than k=N. The unique least-valuation term cannot sum to zero, a contradiction. All N inner roots are therefore covered. Centers modulo beta suffice, as in the accepted theorem. This proof does not assume their simplicity or infer them from the outer residual.

## 5. A needed neighboring-polynomial lemma on exactly these disks

On every accepted beta disk, the ORIGINAL polynomials satisfy

    v(P_(N-1))=B,   v(P_(N-1)')>=B,                    (5.1)

where these are coefficientwise disk bounds, and the first is a unit bound valid at every point. This is not asserted on the entire region v(X)>=1.

Proof first in H. By the consecutive-factor count, wt(N_m)>=T_h(m). In the even-degree expansion (2.1) for N-1, the k=0 term has valuation W(N-1)-W(A)=B. For positive even k<N, its bracket satisfies

    W(A-k/2)+R_h(k)<W(A-k/2)+W(k/2)<=B.

Since W(N-1)=2B, all k>0 terms have valuation >B. Hence H_(N-1) has a coefficientwise constant unit residual after division by its k=0 coefficient.

For its ordinary derivative use the COMPLETE double sum (2.2). Its term weight is at least 2B minus

    W((N-1-k)/2)+R_h(m)+p^ord_p(k-m).                  (5.2)

Put j=k-m. If m is even, then j is even. Superadditivity and the digit bound make (5.2) at most

    W(A-j/2)+p^ord_p(j)<=B,

because W(j/2)>=j/2>=p^ord_p(j).

If m is odd, j is odd and j<N. The corresponding upper bound is

    W((N-j)/2-1)+p^ord_p(j)=W((N-j)/2)<=B.

The equality uses ord_p((N-j)/2)=ord_p(j), since 0<j<N=p^r and p is odd. Thus every ordinary derivative term has weight >=B. Transfer through H_(N-1)(v0^2)=v0^(N-1)P_(N-1)(X); its unit analytic coordinate maps and their derivatives preserve the lower bound. The differentiated prefactor contributes a multiple of H_(N-1) of weight >=B as well. This proves (5.1).

## 6. Root-dependent derivative elimination, not an unjustified translated residual

Write a_j=1-q^j. Define polynomials A_d and B_d by

    A_0=1, A_1=X;  B_0=0, B_1=1,
    A_d=X A_(d-1)-a_(N+d-1)A_(d-2),
    B_d=X B_(d-1)-a_(N+d-1)B_(d-2).

Induction in the original recurrence gives the exact identity

    P_(N+d)=A_d P_N-a_N B_d P_(N-1).                  (6.1)

For d=2c with 0<d<p, all shifted edges a_(N+j), 1<=j<d, have valuation 1. Every inner beta disk lies in v(X)>=1. The continuant coefficients or the recurrence give there

    v(A_d)=c,
    v(A_d')>=c-1+v(X)>=c,
    v(B_d)>=c-1+v(X)>=c,
    v(B_d')>=c-1.                                    (6.2)

For the equality in the first line, the constant coefficient of A_(2c) is the unique perfect-matching product

    (-1)^c product_(j=1)^c a_(N+2j-1),

of valuation c; every positive X power has strictly greater valuation at v(X)>=1. Each coefficient of X^(2j) in A_(2c) has valuation >=c-j; each coefficient of X^(2j+1) in B_(2c) has valuation >=c-1-j. These also prove the derivative lower bounds directly with ordinary derivatives.

Let C=B_d/A_d. It is analytic on the inner disks and

    v(C)>=0,  v(C')>=-1.                             (6.3)

At an inner root xi of P_n, divide (6.1) by the nonzero A_d and then DIFFERENTIATE BEFORE evaluating. The term containing A_d' vanishes at the root, giving exactly

    P_n'(xi)=A_d(xi) [P_N'(xi)
      -a_N(C'(xi)P_(N-1)(xi)+C(xi)P_(N-1)'(xi))].     (6.4)

The pure-power derivative has valuation D at every point of these disks. By (5.1), (6.3), and v(a_N)=N, the subtracted term has valuation at least

    N+B-1=D+(p-1)>D.

Consequently v(P_n'(xi))=c+D and it cannot vanish. For c=0 the assertion is the accepted theorem itself. Crucially, we prove (6.4) AT A ROOT. We do not claim P_n' has a constant unit residual on the whole translated disk: the extra A_d'P_N term need not admit the same bound away from roots.

## 7. Discriminants and original algebraic-square kernels

Section 3 gives exactly 2c outer roots with derivative valuation (n-1)/2, and Sections 4-6 give the remaining N roots with derivative valuation D+c. Both classes are simple. The monic discriminant product formula gives

    N(D+c)+2c(n-1)/2=N(D+c)+c(n-1).

The unit coordinate factors in Section 3 give the same result for H_n. Consecutive original P polynomials are coprime because all recurrence edges are nonzero for indices below p^s. The original ordinary Christoffel-Darboux identity at a root is

    K_n(xi)=P_n'(xi)P_(n-1)(xi)/w_(n-1).

Its factors are nonzero. This uses ordinary algebraic squares, not absolute-value squares or positivity. Algebraic nonvanishing holds in every primitive characteristic-zero embedding by injectivity and Galois conjugacy. No constant valuation is asserted for all kernel values.

## 8. Exact limitations: parity, digits, and distinguished translations

1. Arbitrary degree is not obtained by replacing N everywhere by b. The reflection and tail complement identities are tied to N=p^r. For example, the old monic root-cover lower bound at b=3p^2, h=1, k=1 is -p^2 for every odd p>=5. Thus the accepted inequality fails uniformly, not just at an isolated small case. It is a failure of that sufficient bound, not a counterexample to squarefreeness.

2. The low-digit argument requires W(A+c)=B+c. If c=(p+1)/2, the interval ends at (N+p)/2, which has p-adic order 1; then W(A+c)=B+c+(p-1), so the proof acquires a positive deficit. In addition d=2c=p+1 has a repeated zero Hermite factor. This pinpoints two independent changes needed beyond the stated digit range. Larger low digits and intermediate digits need new inequalities and new residual factors; finite testing does not repair them.

3. Even b has a k=0 Newton term, and H_b(-1)=w_b/(q^2;q^2)_(b/2) is nonzero. The reciprocal identity gives H_b'(-1)=-(b/2)H_b(-1), not a distinguished-root derivative. In particular the exact pure-power-neighbor b=N+1 has H_b(-1) of valuation N+B. At b=p^2+1 and beta=p, the old monic k=0 covering bound

      W(b)-W(0)-W(b/2)-beta-T_1(b-1)

   equals -p. Thus that covering inequality fails already on an unlimited even-degree family. Also the low-degree factor A_d is odd for odd d, so it vanishes at X=0 and cannot be divided out uniformly on the central disk. The even case requires a separate central-cluster analysis. None of these observations proves an even-degree counterexample.

4. For odd b, H_b(-1)=0 is automatic by reciprocity, but H_b(-q^a)=0 is NOT automatic. For example H_1(-q)=1-q is nonzero. A derivative valuation at the distinguished root cannot be translated to all geometric centers by replacing -1 with -q^a. This proof instead supplies root covering, a genuine disk bound for the accepted P_N derivative, and exact root-dependent elimination. The resulting new derivative theorem is not a guessed translation of the distinguished-root formula.

5. Pure-power degrees, all previously accepted cases, the global owner scope, and the F023 alias are preserved unchanged. The largest proved scope here is precisely the stated two-digit odd-degree family.

## 9. Reproducibility and frozen-byte review

check_exact.py uses exact rational/integer and finite-field arithmetic. It reconstructs the original P/H recurrences, ordinary derivatives, the continuant identity, both-parity Newton identity, Hermite residuals, modified root-cover inequality, and the neighboring derivative bound. It also gives finite-field nonzero-resultant certificates for selected characteristic-zero instances. These are falsification and transcription controls, not the proof of the uniform theorem. No floating roots, characteristic-p truncation above ramification, or numerical evidence substitutes for Sections 3-7.

All mathematical inequalities and identities use exact characteristic-zero factor valuations. In particular no bound assumes D<v(p); the theorem includes every ramification range. SOURCE_BINDINGS.json identifies retained local accepted bytes, not a fresh remote retrieval. MANIFEST.json and SEAL.sha256 seal this final artifact. A fresh adversarial review must bind those bytes before acceptance.
