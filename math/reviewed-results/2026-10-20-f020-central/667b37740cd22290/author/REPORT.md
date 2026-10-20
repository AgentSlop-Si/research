# The remaining central roots at n = 2p² + 1

20 October 2026 UTC. Author candidate, frozen for a new independent whole-argument review. The earlier accepted partial package and its audit are unchanged.

## 1. Result and boundary of the claim

Let p be an odd prime, s > 2, and q a primitive p^s-th root in characteristic zero. Keep the ORIGINAL recurrence

    P_0 = 1, P_1 = X,
    P_(j+1) = X P_j - (1-q^j) P_(j-1).

Choose a p-adic embedding and normalize v(t)=1 for t=q-1. Thus e=v(p)=(p-1)p^(s-1). Put

    N=p², B=p(p-1), W=N+2B, d=B/2, rho=p/2,
    E=N/2+2B, D=N+E-p,
    F(X)=P_(2N+1)(X)/X,
    f(U)=t^(-W) F(X), where X²=t^p U.

The last definition is polynomial in U because F is even. By the accepted partial theorem, precisely 2p nonzero P roots lie in the central disk and all have v(X)=rho. Their U coordinates are units with U+1 of positive valuation. The present candidate proves that ALL these roots are simple. More precisely:

- For p >= 5, every such root satisfies v(U+1)>1 and

      v(f_U(U))=d+1,
      f_U(U)/t^(d+1) has residue 1/8.

  Consequently v(P_(2N+1)'(X))=W+d+1=(7p²-5p+2)/2.

- For p=3, every such root satisfies v(U+1)=4/3 and

      v(f_U(U))=13/3,
      v(P_19'(X))=76/3.

All derivatives are ordinary characteristic-zero derivatives. In particular, the p=3 derivative of the cubic term retains its factor 3 and its valuation e.

Combined with the accepted partial theorem, this proves squarefreeness of the original P_(2p²+1) and H_(2p²+1), and nonvanishing of the original algebraic-square Christoffel-Darboux kernel at every P root, for every odd p and every s>2. This is a completion only of the adjacent leading-two r=2 family. No arbitrary n, other digit pattern, odd-composite order, global F020/F023 closure, FFT-speed, complexity, or novelty claim is made.

The initially suggested mechanism, that the known t^d(U+1) derivative term should dominate, is NOT used for p>=5. A next constant derivative correction at t^(d+1) dominates instead. The suggested mechanism does work for p=3 after a separate exact coefficient calculation.

## 2. Frozen imported facts and notation

SOURCE_BINDINGS.json records the exact prior author and independent-audit manifests and relevant report bytes. The accepted partial author manifest hash is b58aa5d90e5faf2fc3a85afbbe856fe244f819ffee9672248d89ad1a6cc183fc; the accepted audit release manifest hash is 3ef43809ad247d951b0e34c1e9be5c013d68772d74cc45e6d2743a4215f9d5ea.

Write

    w_m=product_(j=1)^m (1-q^j),
    Q_m=product_(j=1)^m (1-q^(2j)),
    N_m(z)=product_(j=0)^(m-1) (z+q^j),
    W(m)=sum_(j=1)^m p^ord_p(j).

The context distinguishes the scalar W=W(N) from the function W(m). For m<=2N,

    W(m)=m+(p-1)floor(m/p)+(N-p)floor(m/N).

The exact ordinary Newton identities are

    H_b(z)=sum_(k=b mod 2) w_b N_k(z)/(w_k Q_((b-k)/2)),
    H_b'(z)=sum_(k=b mod 2,k>=1) sum_(m=0)^(k-1)
       w_b z^(k-m-1) N_m(z)
       /[Q_((b-k)/2) w_m (1-q^(k-m))].

They have no zero denominator because 2N+1<p^s. The coordinate relation is

    H_b(v0²)=v0^b P_b(v0+v0^(-1)),
    H_b'(z)=v0^(b-2)[(b/2)P_b+(v0-v0^(-1))P_b'/2],

where z=v0², X=v0+v0^(-1), and v0 is near i with i²=-1. On the central boundary, v(X)=v(z+1)=rho, v0 and v0-v0^(-1) are units, and

    (z+1)²=z X².

The accepted partial package proves the root count, the polynomial factorization F=P_(2N)-a_(2N)M/X with M=P_(2N-1) and a_j=1-q^j, and the residuals

    f(U) mod maximal ideal = 1+U^p,
    f_U(U)/t^d mod maximal ideal
       = -epsilon U^((p-3)/2)(U+1),
    epsilon=(-1)^((p-1)/2).

In particular f has integral coefficients on the unit U disk, f_U has coefficientwise weight at least d there, and after U=-1+V the residual is V^p. The coefficientwise assertions about f_U follow equivalently by applying the ordinary derivative scaling to the accepted F' residual. They do not arise by differentiating 1+U^p in the residue field.

The accepted bounds v(M)=E on the entire central boundary and v(M')>=E on the closed central disk will also be used. The current proof strengthens the relevant nonpivot gaps rather than assuming they are large enough.

## 3. Exact central cap slack and all competing Newton terms

For an arbitrary point of the central boundary, every factor z+q^j with p dividing j has value rho; every other factor has value 1. Thus

    T_c(m)=v(N_m)=m+(p/2-1)ceil(m/p),
    R_c(m)=W(m)-T_c(m).

Write m=cN+ap+b, 0<=a,b<p, allowing the endpoint m=2N separately with a=b=0. Set Delta_c(m)=W(m)/2-R_c(m). Direct substitution gives the exact identity

    2 Delta_c(m)=a(p-1)+b+(p-2)1_(b>0).                (3.1)

Hence Delta_c vanishes exactly at 0,N,2N, and every other value is at least (p-1)/2. This is an actual central-boundary formula, not the weaker floor-cap used for all disks.

### 3.1 The neighboring polynomial

For b0=2N-1, W(b0)=2E. The k-th Newton term, with a=(b0-k)/2, has value

    E + [W(b0)-2W(a)-W(k)]/2 + Delta_c(k).

The bracket is nonnegative by superadditivity. Since k is odd and 1<=k<=2N-1, only k=N can have zero Delta_c. At that index equality holds and its term is

    C_- N_N, C_-=w_(2N-1)/(w_N Q_A), A=(N-1)/2.

Every other term has value at least E+(p-1)/2. For p>=5 this is a STRICT relative error >1.

### 3.2 The ordinary derivative of H_(2N)

Put j=k-m. A derivative term has value

    2W-W(a)-R_c(m)-p^ord_p(j), a=(2N-k)/2.

Using 2a+m=2N-j, superadditivity, and the exact reflection

    W(2N-j)=2W-N-W(j-1),

gives the lower bound on its excess above D:

    p+W(j-1)/2-p^ord_p(j)+Delta_c(m).                (3.2)

For j not divisible by p, the part before Delta_c is at least p-1. For ord_p(j)=1, it is at least (p-1)/2, attained at j=p. The only j of valuation 2 in 1..2N are N and 2N. At N the part is zero; at 2N it is 3N/2-p, certainly at least (p-1)/2. For j=N, admissibility gives 0<=m<=N and k=m+N even. Thus m=0 is inadmissible, and m=N is the only possible zero of Delta_c. This is precisely the pivot (k,m)=(2N,N).

It follows that the pivot

    C z^(N-1) N_N, C=w_(2N)/(w_N(1-q^N)),

has value D and all other terms have value at least D+(p-1)/2. Again, for p>=5 every error is strictly more than 1 above the pivot. No unexamined term can cancel the first-order correction used below.

### 3.3 The polynomial H_(2N)

For its k-th Newton term the excess above W is

    [W(2N)-2W(a)-W(k)]/2+Delta_c(k), a=(2N-k)/2.

For 0<k<2N, k is even and so k!=N. The N-floor part of the bracket alone is at least N-p, while the remaining floor parts are nonnegative. Thus every term other than k=0,2N has excess at least

    d+(p-1)/2=(p²-1)/2.                             (3.3)

This is >p for all p>=3. The two remaining terms are exactly

    N_(2N)(z)+C_0,
    C_0=w_(2N)/Q_N=product_(j=1)^N(1-q^(2j-1)).    (3.4)

## 4. A sufficiently deep root location for p>=5

It is enough to prove v(f(-1))>p, not its apparent sharper value d. This section proves that weaker bound uniformly, without extrapolating the finite controls.

Because e>W+p for p>=5, any integer polynomial in t whose reduction modulo p has order >W+p also has actual valuation >W+p. Indeed every coefficient divisible by p has value at least e>W+p. The quantity F(X) evaluated at X²=-t^p is an integer polynomial in t. We may therefore compute its required truncation in characteristic p. The auxiliary z coordinate lives in the corresponding algebraic power-series extension; the final even polynomial is the original integer polynomial in t.

We use this elementary grouped-product lemma in characteristic p:

    product_(a=0)^(p-1)(Z+A(1+h)^a) - (Z+A)^p
        is divisible by h^(p-1) in F_p[Z,A,h].      (4.1)

For completeness, the q-binomial product formula makes each intermediate coefficient a multiple of [p choose k]_(1+h), whose h order is p-1 for 1<=k<p. The last coefficient differs from its h=0 value by (1+h)^(p(p-1)/2)-1, of h order at least p. This proves (4.1). No assertion that individual factors have sufficiently high error is made.

Put X²=-t^p, S=z+1, and define

    R_0=product_(j=1)^(p-1)(q^j-1),
    D_0=product_(1<=j<2p, j odd, j!=p)(1-q^j).

Group the indices of N_(2N) as j=b+ap+cN with 0<=a,b<p and c=0,1. In each p-factor block, h=q^p-1=t^p in characteristic p. The main factors z+q^(b+cN) have value rho if b=0 and 1 otherwise. By (4.1), the relative error is at least

    p(p-1)-p rho = p(p-2)/2 > p   if b=0,
    p(p-1)-p = p(p-2) > p         if b!=0.

Replacing q^(b+N) by q^b after taking p-th powers has still higher relative error. Multiplying these finitely many blocks therefore gives

    N_(2N)(z)=N_p(z)^(2p)+error of value >W+p.       (4.2)

For C_0 in (3.4), group odd indices as 2b+1+2ap. All non-p-divisible blocks have relative error >p by the same lemma, now with h=q^(2p)-1 of value p. The p-divisible block is exact:

    product_(a=0)^(p-1)(1-q^(p(2a+1)))
       =[(1-q^p)D_0]^p.

Consequently

    C_0=-t^N D_0^(2p)+error of value >W+p.          (4.3)

Now N_p=S R, where R=product_(j=1)^(p-1)(z+q^j). Each replacement z+q^j by q^j-1 has relative error rho-1>1, so R=R_0(1+error of value >1). Also z=-1+error of value rho>1. Direct first-order products give

    R_0/t^(p-1)=-(1+t/2+O(t²)),
    D_0/t^(p-1)=-(1+t/2+O(t²))                      (4.4)

in characteristic p. The leading units follow because both index sets reduce to F_p^*. Their linear coefficients are respectively

    sum_(j=1)^(p-1)(j-1)/2 = 1/2 mod p,
    sum_(j odd,1<=j<2p,j!=p)(j-1)/2 = 1/2 mod p.

Since S²=zX²=-zt^p, equations (4.4) imply

    N_p²-t^pD_0²=-t^p(zR²+D_0²)

has value strictly larger than (3p-2)+1. Taking its p-th power and using (4.2)-(4.3) shows that the sum of the two main Newton terms has value >W+p. Equation (3.3) shows the other H terms do too. The unit coordinate prefactor then gives v(P_(2N)(X))>W+p at X²=-t^p.

The exact quotient perturbation a_(2N)M/X has value W+d on this boundary, and d>p for p>=5. Hence

    v(f(-1))>p.                                    (4.5)

To turn this into a statement about ALL roots, write f(-1+V)=sum_j a_j V^j. The accepted residual is V^p; all coefficients are integral and a_p is a unit. The ordinary derivative bound gives v(a_j)>=d for 1<=j<p because these j are p-adic units. If a root had 0<v(V)<=1, its a_p V^p term would be strictly lower than: the constant by (4.5), every 1<=j<p term since d>p, and every j>p term by integrality. This is impossible. Therefore every central root has v(V)>1.

## 5. The first derivative correction for p>=5

The exact formula on the nonzero central boundary is

    F'=P_(2N)'-a_(2N)M'/X+a_(2N)M/X².              (5.1)

The M'/X term is higher than M/X² by at least rho>1. The gap calculations in Section 3 show that only the indicated Newton pivots of M and H_(2N)' affect their relative expansion through value 1. The coordinate prefactor term in P_(2N)' has value at least 2e+W, exceeding D by more than 1. Thus the exact pivot ratio gives

    X² P_(2N)'/(a_(2N)M)
      = X² * [2 z^N/(z-1)] * Q_A/(1-q^N)
          * (1+error of value >1).                 (5.2)

No division by a zero is used: M has exact value E on the whole boundary. The factor 2z^N/(z-1) is 1 plus an error of value >1, since z=-1+an element of value rho>1. Also

    (1-q^N)/(-t^N)=1+error of value >1.

For Q_A the normalized leading unit is -1, as in the accepted partial proof. Its linear coefficient comes only from indices not divisible by p. Put a=(p-1)/2, so A=ap+a. Then

    sum_(1<=j<=A,p does not divide j)(2j-1)/2
       =a/2+a²/2=(p²-1)/8=-1/8 mod p.

Indices divisible by p have no linear t correction; their first possible correction has value at least p, or an even higher mixed-characteristic value. Therefore

    Q_A/(-t^B)=1-t/8+error of value >1.              (5.3)

Using X²=t^p U and N=B+p, (5.2)-(5.3) become

    X² P_(2N)'/(a_(2N)M)
       =U(1-t/8+error of value >1).

At a central root, U=-1+V with v(V)>1. Hence the bracket formed by this ratio and the last term of (5.1) is

    1+X²P_(2N)'/(a_(2N)M)=t/8+error of value >1.    (5.4)

Finally let K=t^p a_(2N)M/(2X³t^W). It has value d. The accepted actual Gaussian phase units give

    K/t^d -> -epsilon U^((p-3)/2),

which is 1 at U=-1. Multiplying (5.4) by K, with the strictly higher M' error retained, proves

    f_U(U)/t^(d+1) -> 1/8.

This is nonzero for every odd p>=5. It is an ordinary derivative calculation over characteristic zero with exact first-order Gaussian units.

## 6. The exceptional prime p=3, uniformly in s>=3

Here a nonpivot ordinary derivative term is only 1 above the leading pivot, so Section 5 must not be applied. Instead use a fixed-degree exact polynomial certificate, which proves all s at once.

Put X²=t³(V-1). Define integer polynomials in t,V by

    E_0=O_0=1,
    E_k=t³(V-1)O_(k-1)+[(1+t)^(2k-1)-1]E_(k-1),
    O_k=E_k+[(1+t)^(2k)-1]O_(k-1), 1<=k<=9.

These are exactly E_k=P_(2k) and O_k=P_(2k+1)/X after the stated substitution, not a replacement recurrence. Write O_9=sum_(j=0)^9 C_j(t)V^j. Every monomial in C_j has t degree at least L_j=9+2j: a term of degree l in X² has at least 9-l edge factors of t, and its substitution contributes t^(3l), with l>=j.

The fixed finite recurrence yields the following exact congruences, reproduced in THREE_CERTIFICATE.json with full integer coefficient polynomials and checked by check_controls.py:

    C_0/t^9  = t^16      modulo (3,t^17),
    C_1/t^11 = 2t^17     modulo (3,t^18),
    C_2/t^13 = 2t^11     modulo (3,t^12),
    C_3/t^15 = t^6       modulo (3,t^7).             (6.1)

These are four finite algebraic identities for the one fixed polynomial P_19. They are not an inference from successful cyclotomic tests. The same identities work at every s because e>=18 and

    18+L_j > m_j,
    (m_0,m_1,m_2,m_3)=(25,28,24,21).

Thus the unique lowest monomial of each C_j is its indicated p-unit term, regardless of the cyclotomic relation or the value of s. With f(-1+V)=t^(-21)O_9, the first four coefficient valuations are exactly

    (v(a_0),v(a_1),v(a_2),v(a_3))=(4,7,3,0).       (6.2)

All other a_j are integral by the accepted coefficientwise quotient bound. Because the residual is V³ and the coefficient field has integer valuation group, v(a_j)>=1 for j!=3. In particular v(a_4)>=1.

The Newton comparison in (6.2), with all higher coefficients integral, forces v(V)=4/3 at every root above V=0. At such a root, the ordinary derivative terms have valuations

    a_1: 7,
    2a_2 V: 3+4/3=13/3,
    3a_3 V²: e+8/3 >= 18+8/3,
    4a_4 V³: at least 1+4=5,
    j a_j V^(j-1), j>=5: at least 4(j-1)/3>=16/3.

The unique smallest term is 2a_2V. Therefore v(f_U)=13/3 and every one of these roots is simple. This includes the minimally ramified s=3 case without a separate finite-field exception or any assumption from s>=4.

## 7. Original derivative, H transfer, and kernel

At a nonzero root of F, P_(2N+1)=XF gives

    P_(2N+1)'=X F'=2U t^W f_U.

Since 2 and U are units, Sections 5 and 6 give exactly the derivative valuations in Section 1. There are no additional central roots outside this calculation: the accepted disk count already covers all 2p, with multiplicity before simplicity.

The original H/P coordinate maps have unit derivatives at the corresponding roots, and the prefactor derivative vanishes at a root. Thus multiplicity and ordinary derivative valuations transfer to H. The accepted exact zero-root and noncentral-root results complete squarefreeness of the entire r=2 family.

All recurrence edges below n are nonzero, so backward recurrence proves P_n and P_(n-1) coprime. The original ordinary algebraic Christoffel-Darboux identity is

    sum_(j=0)^(n-1) P_j(xi)^2/w_j
       =P_n'(xi)P_(n-1)(xi)/w_(n-1).

It is now nonzero at every root xi for this family. These are algebraic squares, not absolute-value squares. No positivity or interlacing argument is substituted. Nonvanishing in this p-adic embedding transfers to characteristic-zero primitive embeddings by injectivity and Galois conjugacy.

## 8. Controls, contribution disclosure, and stopping condition

The proof in Sections 3-7 is uniform. Finite controls are auxiliary except for the exact four polynomial identities (6.1), which are a finite symbolic certificate for fixed p=3 and cover every s by the explicit e>=18 inequality.

The release checker does the following:

- Reconstructs the original n=19 recurrence over integer polynomials, records all ten V-coefficient polynomials, verifies the t-divisibility and four exact reductions, and verifies that each lowest p-unit monomial dominates all other integer monomials for every e>=18.
- Directly enumerates the relevant integer Newton weights in several primes, checking the exact slack, claimed nonpivot lower bounds, and unique pivots. This is a transcription/falsification check, not the proof of the inequalities.
- Reconstructs the ORIGINAL recurrence over Z[q]/Phi_(p^s) for the displayed finite fields and evaluates the V-jets. Mixed-characteristic valuation is computed exactly from the degree-<e t representation, with v(p)=e and leading p/t^e residue -1. These controls confirm, but do not prove by extrapolation, the general local behavior.

The author independently derived the 1/8 correction, cap slack, grouped-product argument, and uniform p=3 integer certificate before receiving matching exploratory observations from a simultaneous auditor. That auditor independently identified the same first-order Q_A coefficient and a stronger grouped-product error lemma; the proof above uses the author's weaker lemma (4.1), which is already sufficient. The auditor also suggested splitting p=3 into s=3 and s>=4; this proof instead uses the author's uniform all-e>=18 certificate. No essential lemma was imported from that auditor, but their overlapping exploratory involvement is disclosed. This candidate must receive a NEW whole-argument independent review against its frozen manifest; the simultaneous auditor is not treated as that acceptance reviewer.

The bounded task is complete at the author-candidate level. No further family search or external write is part of this package. If an independent reviewer finds a defect, the claim remains pending and any correction must be frozen as new bytes, without rewriting the accepted earlier packages.
