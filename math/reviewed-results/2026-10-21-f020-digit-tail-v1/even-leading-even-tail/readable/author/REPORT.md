# Every even leading digit with every positive even short tail

Author candidate, 21 October 2026 UTC. Original F020 normalization. This is an exact uniform extension using accepted coefficientwise inputs, not self-acceptance, a claim of historical novelty, or arbitrary-degree closure.

## 1. Statement and complete root partition

Let p be an odd prime, let c and d be even integers with 2 <= c < p and 2 <= d < p, let r >= 2 and s > r, and let q be any characteristic-zero primitive p^s-th root of unity. Put N=p^r, m=d/2, n=cN+d. Use exactly

    P_0=1, P_1=X, P_(j+1)=X P_j-(1-q^j)P_(j-1),
    H_j(z)=sum_k [j choose k]_q z^k,
    w_j=product_(u=1)^j (1-q^u), w_0=1.

Choose an algebraic p-adic embedding, set t=q-1, and normalize v(t)=1. Define

    e=v(p)=(p-1)p^(s-1), B=r(p-1)p^(r-1)/2,
    K=cN/2+cB, E=(c-1)N/2+cB, D=(c+1)N/2+cB-p=N+E-p,
    h=floor(r/2), beta=p^h, L=N/beta,
    rho=beta/2                    if r is even,
    rho=p^(h-1)(2p-1)/2           if r is odd,
    C_m=(2m-1)!!.

Write the integer Hermite polynomials in the sign convention

    M_j(Z)=j! sum_(k=0)^floor(j/2) Z^(j-2k)/[2^k k! (j-2k)!].

THEOREM. Original P_n and H_n are squarefree, and the original algebraic-square Christoffel-Darboux kernel is nonzero at every P_n root, for every parameter and primitive phase just stated. There is no exceptional prime or residual obstruction inside this scope.

The complete P_n root partition, with ordinary characteristic-zero derivative values, is:

1. Exactly d low roots, each with v(X)=1/2. If tau^2=t and X=tau Z, their distinct nonzero residues are the roots of M_d(Z). At each such root,

       v(P_n'(X))=(n-1)/2,
       P_n'(X)/tau^(n-1) -> d Z^(cN) M_(d-1)(Z) != 0.

2. In each of the beta disjoint closed disks

       v(X-x_a)>=rho,
       x_a=i(q^(a/2)-q^(-a/2)), 0<=a<beta, i^2=-1,

   with square roots of q^a congruent to 1, there are exactly cL high roots, all on the boundary. On every one,

       v(P_n'(X))=D+m.

   Their X-values are rho centrally and p^ord_p(a) for a!=0. Each disk has c distinct nonzero residual locations, with L roots counted with multiplicity over each location before simplicity is established. Their total is cN.

There is no zero root, and v(P_n(0))=K+m. The corresponding original H_n derivatives have the same valuations; the H/P derivative multiplier has residue i^(n-1)=(-1)^(c/2+m-1)i, not a fixed c=2 sign.

Both prime boundaries c=p-1 and d=p-1, separately and simultaneously, are included. At p=3 the only pair is c=d=2, which is retained rather than newly credited. All c=2 even tails and c=4,d=2 are accepted predecessors. The added parameter range relative to those two supplied predecessors consists of c>=4,d>=2 even, except (c,d)=(4,2); this comparison does not assert novelty against other work.

Excluded: p=2; odd leading digits or tails; c>=p or d>=p; r=1; s<=r; composite orders; arbitrary or intermediate base-p digits; squarefreeness in unrelated auxiliary finite characteristics; global F020/F023 closure; FFT, complexity-improvement, or historical-novelty claims. An exclusion is not a claim that a case is false or unknown elsewhere.

## 2. Exact accepted authority and scope of the imported statements

The six unchanged author/review packages are included completely under dependencies. Their manifest SHA-256 pins are:

    general-author   e19104be98018ea10de85dd648b3b2634664150ea24994300e28ac56fe889ec7
    general-review   a7990e625de81f3797ac13bbad7d7c817eb65aee195e5690f84de6ca7540c3c7
    c2-even-author   c7b391df43fc8fb0fb14fab06ddd1d4e722d791469fc2593017ef27d8d9a88d3
    c2-even-review   419d478b906e68600983a1b209ed53e0f05c532875d409398ee7ae9e168cb012
    c4-plus2-author  07682f06811d03a7df5cfdf966b885c206af0fc30b2414b8609b89eafe28a653
    c4-plus2-review  940a49a2c461813aea78c76a410b8615efc16ab21f4b7d7e1aa2578cc7e0382b

The general report hash is 639b35b0b603fccc44a57c1f5321fc7efc5c9007510b0cd12d714eefc0d5820c, and its accepting review report hash is 67dc7c923f4e0ace97b9246c9303a2fa3633eeaadea850449a22a9f62c0355f0. Source inventory verification is freshly written and read-only. None of the accepted programs or control suites is executed.

Set A=P_(cN), M=P_(cN-1). The imported facts are the UNCONDITIONAL coefficientwise statements of general-author Sections 2-5, whose off-root transfer and complete derivative terms are explicitly audited in general-review, Uniform mathematical audit Sections 1-4. On every FULL high disk, using its scaled coordinate Y and a coefficientwise Gauss weight wt, they give

    wt(A)=K,    in(A)=nonzero scalar * M_c(Zbar),
    wt(M)=E,    in(M)=nonzero scalar * c M_(c-1)(Zbar),
    wt(A')=D,   in(A')=nonzero scalar * c M_(c-1)(Zbar),
    wt(M')>=E, Zbar=alpha_a Y^L, alpha_a!=0.                 (2.1)

The normalizations are actual scalars in the original field, not guessed units. The A residual has degree cL and nonzero constant, and all higher coefficients have strictly greater normalized weight. The source's condition for the DIFFERENT degree cN+1, including its r=2 obstruction, is NOT a hypothesis of (2.1). The facts are valid for all even c<p, r>=2, s>r, including c=p-1.

For precision, these are not new bounds inferred from the accepted c=2 or c=4 cases. Here is the complete general-c pivot content of the accepted authority. Write

    a_j=1-q^j, Q_b=product_(j=1)^b(1-q^(2j)),
    N_b(z)=product_(j=0)^(b-1)(z+q^j), W(b)=sum_(j=1)^b p^ord_p(j).

Its exact Newton expansion and complete ordinary derivative are

    H_b=sum_(k=b mod 2) w_b N_k/[w_k Q_((b-k)/2)],
    H_b'=sum_(k=b mod 2,k>=1) sum_(0<=u<k)
      w_b z^(k-u-1)N_u/[Q_((b-k)/2)w_u a_(k-u)].              (2.2)

The cap R(j)=W(j)-sum_(u=1)^j min(p^ord_p(u),rho) <= W(j)/2 has equality exactly at j=lN on 0<=j<=cN. Put omega^2=w_N. For A the Newton equality indices are k=(c-2u)N, u=0,...,c/2, with their full sum M_c. For the A ordinary derivative the unique maximizing increment is k-u=p^2, and the equality pairs are ALL

    u=lN, k=lN+p^2, l=1,3,...,c-1.

Let A0=(N-p^2)/2 and C1=w_N/[Q_A0 a_(p^2)]. For each l the actual normalized contribution is

    c! Zbar^l/[l! 2^v v!], v=(c-1-l)/2.

Thus their entire sum, after normalization by C1 omega^(c-1), is c M_(c-1)(Zbar), with weight D. At c=4 BOTH pairs (N,N+p^2) and (3N,3N+p^2) contribute, respectively 12 Zbar and 4 Zbar^3. At r=2 the last pair is the endpoint k=cN and is included. For general c there are c/2 pairs, not two and not one.

The neighbor's Newton equality indices are k=lN with the same odd l, and with Ahalf=(N-1)/2 and Cminus=omega^(c+1)/[a_(cN) Q_Ahalf], its residual is c M_(c-1). The full M' bound is not an assertion about selected pivots. In its complete derivative sum, reflection and the cap give the subtracted score at most

    E+[p^ord_p(j)-W(j)/2], j=k-u.

Only j=1,p can exceed E, by at most 1/2. If u is not a multiple of N the cap is strict. Otherwise u=lN with l even; writing 2v=cN-1-u-j gives

    floor(2v/N)=c-l-1 > 2 floor(v/N)=c-l-2.

The N-level carry makes the bound strict. Half-integrality then gives the score <=E. This covers every derivative term, including prime-boundary cases. The general H/P conversion retains the prefactor ordinary derivative; for A its contribution has weight at least re+K>D. This establishes the off-root A' input rather than just values at old roots.

The integer identities

    M_j=Z M_(j-1)+(j-1)M_(j-2), M_j'=j M_(j-1)

imply, by backwards propagation through unit coefficients, that M_c and M_(c-1) are coprime modulo p. More exactly,

    Res(M_c,M_(c-1))=product_(j=1)^(c-1) j^j.                 (2.3)

The usual monic resultant convention is used; the formula follows by induction in the recurrence. M_c has c distinct roots and constant C_(c/2), a unit. Consequently at ANY point of the residual locus M_c(Zbar)=0, not merely an earlier polynomial's root, (2.1) gives

    v(M)=E, v(A')=D.                                       (2.4)

No additional general-c coefficientwise input is missing.

## 3. Exact transfer and its fraction-free ordinary-derivative witness

Define the original short edges b_j=1-q^(cN+j), j>=0. There is no vanishing edge or denominator:

    pN-n=(p-c)N-d >= N-(p-1)>0, n<pN<=p^s.

All source denominators have indices at most cN, hence below n, and all new recurrence edges are below n. The valuations and actual initial units are

    v(b_0)=N, b_0/t^N -> -c,
    v(b_j)=1, b_j/t -> -j       (1<=j<=d-1<p).              (3.1)

Define tail polynomials by

    T_0=1, T_1=X, U_0=0, U_1=1,
    T_(j+1)=X T_j-b_j T_(j-1),
    U_(j+1)=X U_j-b_j U_(j-1)  (j>=1).

Induction in the ORIGINAL P recurrence gives the exact identity

    F:=P_(cN+d)=T_d A-b_0 U_d M.                             (3.2)

U_d has degree d-1 and its edge start is b_2, not b_1: U_2=X, U_4=X^3-(b_2+b_3)X. Define

    W_d=U_d'T_d-U_d T_d',
    S_d=T_d F'-T_d'F
       =T_d^2 A'-b_0 W_d M-b_0 U_d T_d M'.                  (3.3)

Every prime denotes the ordinary characteristic-zero derivative. The b_j are independent of X. Formula (3.3) includes both correction terms, the squared T multiplier, and the original T_d' cancellation. It will be used before substituting F=0. It is not by itself a simplicity theorem.

## 4. Uniform tail estimates on whole high disks

Write x=wt(X). Centrally x=rho; otherwise x=p^ord_p(a), so x>=1. The matching expansion of a tridiagonal recurrence proves that the coefficient of X^(2k) in T_(2m) is a signed sum of products of exactly m-k short edges. Similarly the coefficient of X^(2k+1) in U_(2m) is a signed sum of products of m-1-k short edges. The claims follow as well by induction: multiplication by X adds no edge, while the other recurrence term adds one edge and reduces the index by two. Therefore the respective coefficient values are at least m-k and m-1-k, even if there is cancellation.

T_(2m) has the unique constant matching

    T_(2m)(0)=(-1)^m b_1 b_3 ... b_(2m-1),
    T_(2m)(0)/t^m -> C_m !=0 mod p.                         (4.1)

Every odd factor of C_m is <p, including d=p-1. For k>=1 a nonconstant T term has weight >=m+k(2x-1)>m. Thus T_d/t^m has constant initial C_m and is an analytic unit EVERYWHERE on every high disk. Direct ordinary differentiation keeps all integer factors and gives

    wt(T_d)=m, wt(U_d)>=x+m-1,
    wt(T_d')>=x+m-1, wt(U_d')>=m-1,
    wt(W_d)>=2m-1.                                        (4.2)

Indeed U_d'T_d has weight >=2m-1, and U_d T_d' has weight >=2m+2x-2>=2m. A p-divisible derivative coefficient can only improve these lower bounds. No auxiliary U or W coefficient is assumed to be a unit.

## 5. Complete high-root geometry and simplicity

The perturbation in (3.2) has coefficientwise weight at least

    N+E+x+m-1=K+m+(N/2+x-1)>K+m.                           (5.1)

The normalized F residual is therefore C_m times the corresponding normalized A residual. It has degree cL, nonzero constant, and higher coefficients have positive normalized weight. The closed-disk Newton polygon (equivalently Weierstrass preparation) gives exactly cL roots counted with multiplicity, all on the boundary. Since L is a power of p and M_c is separable with nonzero roots, there are exactly c residual locations, each with multiplicity L. This is a multiplicity count, NOT simple-root Hensel lifting on M_c(alpha Y^L).

Distinct disk centers have distance valuation at most p^(h-1)<rho; the disks are disjoint. The total high-root count is beta*cL=cN. At each of THESE NEW high roots the residual equation M_c(Zbar)=0 holds, so (2.4) applies to M and A'. In (3.3) the three terms have values

    T_d^2 A':          D+2m, exactly,
    -b_0 W_d M:        >=N+E+2m-1=D+2m+(p-1),
    -b_0 U_d T_d M':   >=N+E+x+2m-1=D+2m+(p+x-1).

Both gaps are strictly positive for every c,d,r,s in scope. Hence

    v(S_d)=D+2m.

At a root F=0, the EXACT identity S_d=T_d F' and v(T_d)=m give

    v(F')=D+m.                                             (5.2)

Thus all cN high roots are simple. The full-disk witness initial is C_m^2 times the A' initial. This is nonzero on the entire residual root locus. There is deliberately NO assertion that wt(F')=D+m on the whole disk: away from roots, the T_d'F term can have smaller weight. The witness removes that term exactly.

For comparison only, one may divide by the proved unit T_d and put J=F/T_d, R=U_d/T_d. Then

    J'=A'-b_0 R'M-b_0 R M',
    wt(R')>=-1, wt(R)>=x-1.

This explains the c-independent gaps. In the adjacent +1 problem, R=1/X has derivative value -2x and can tie A'. No such tie exists for this even tail. A prime divisor of the adjacent obstruction M_c(i) is NOT an exception here.

Since U_d is odd, U_d(0)=0. Equations (3.2) and (4.1) give F(0)=T_d(0)A(0) and v(F(0))=K+m. In particular no exact zero is factored out, omitted, or counted.

## 6. Actual central units, including variable c

This section checks the signs and normalization rather than importing the c=2 display unchanged. Assume r=2. Then B=N-p, rho=p/2. Put mu^2=t^p, X=mu Y, and epsilon=(-1)^((p-1)/2). The accepted general coefficientwise computation uses the actual edge unit a_j/t^(p^ord_p(j)) -> -j/p^ord_p(j). Its block products give

    w_N/t^(N+2B) -> -1,
    Q_Ahalf/t^B -> -1,
    a_(cN)/t^N -> -c,
    N_N(z)/(t^B mu^p) -> -i^p Y^p.                         (6.1)

The Q sign follows from Wilson: with a=(p-1)/2 and Ahalf=ap+a, the product of j/p^ord_p(j) is (-1)^a(a!)^2=-1; (-2)^Ahalf=1. N_N's p central factors contribute (z+1)^p, and z+1=v0 X with v0bar=i.

Let eta be the initial of omega/(t^B mu^p), so eta^2=-1, and delta=-i^p/eta, so delta^2=1. The normalized A scalar is i^(-cN)eta^c=1, since c is even and N=p^2 is 1 modulo 4. Evenness gives M_c(delta Y^p)=M_c(Y^p). For the neighbor the scalar, INCLUDING the c in its Hermite residual and the c in a_(cN), is

    i^(1-cN)eta^(c+1)delta=-i^(p+1)=epsilon.

Thus the actual original P residuals are

    A(mu Y)/t^K -> M_c(Y^p),
    M(mu Y)/[t^(cB)mu^((c-1)p)] -> epsilon M_(c-1)(Y^p).    (6.2)

The ratio of the H derivative and neighbor normalizing scalars is exactly

    [C1 omega^(c-1)]/Cminus
      =a_(cN) Q_Ahalf/[Q_A0 a_(p^2)].

At r=2, A0=0, and its initial is -c t^B. The H/P conversion multiplies this ratio by 2v0^2/(v0^2-1), whose residue is 1, while its prefactor error is strictly higher by Section 2. Consequently

    A'(mu Y)/[t^((c+1)B)mu^((c-1)p)]
       -> -c epsilon M_(c-1)(Y^p).                         (6.3)

This normalization has value D. Combining (4.1), (5.1), and the strict witness gaps yields

    F(mu Y)/t^(K+m) -> C_m M_c(Y^p),
    S_d(mu Y)/[t^((c+1)B+2m)mu^((c-1)p)]
       -> -c C_m^2 epsilon M_(c-1)(Y^p).

At every high root, and ONLY rootwise for this last display,

    F'(mu Y)/[t^((c+1)B+m)mu^((c-1)p)]
       -> -c C_m epsilon M_(c-1)(Y^p) !=0.                 (6.4)

Both c and C_m are units at the two prime boundaries. Coprimality (2.3) rules out cancellation of the FULL multi-pivot polynomial at an M_c root. No factor Y^2+1 is present. In particular (c,p)=(8,11),(10,19),(16,17), where the adjacent criterion has a leading cancellation, have no central obstruction for any allowed even d.

## 7. All auxiliary cancellations are harmless

The leading short-edge residues depend on j, not c, because cN is p-divisible. Define integer associated Hermite polynomials

    V_0=0, V_1=1, V_(j+1)=Z V_j+j V_(j-1).

Under X=tau Z, tau^2=t, the residues of tau^(-d)T_d(tau Z) and tau^(1-d)U_d(tau Z) are respectively M_d and V_d. Set

    b_0^*=0, b_m^*=V_(2m)'(0)
         =(2m-2)!!+(2m-1)b_(m-1)^*.

Here 0!!=1. The recurrence follows from V_(2m-1)(0)=(2m-2)!! and differentiation of the integer polynomial recurrence. The first b_m^* are 1,5,33,279,2895,35685. On a high disk, the first possible U_d term is b_m^* X t^(m-1), and the first possible W_d term is C_m b_m^* t^(2m-1). Thus the exact first-tier cancellation condition is

    p divides b_m^*, d=2m<p.                               (7.1)

Outside (7.1), the corresponding lower bounds for U_d and W_d are attained. Inside it, those normalized coefficients vanish, and the weights strictly improve; other terms or further cancellations can only improve them more. This statement includes full-disk Gauss weights, since all higher X powers have strictly larger weight when x>=1. Examples include d=6,p=11 and d=12,p=13, the latter a boundary d=p-1 case. These are NOT exceptional pairs for the theorem. The proof in Section 5 uses only inequalities (4.2) and survives all depths of auxiliary cancellation.

The only decisive tail coefficient is C_m, whose factors are all <p. For d>=p+1 this unit can fail; that range is explicitly excluded, not silently inferred from finite fixtures. Within scope, neither a central multi-pivot cancellation nor an auxiliary tail cancellation leaves an unresolved root-lifting obligation.

## 8. Exactly d low roots, including d=p-1

Set tau^2=t and evolve the original polynomial and its ORIGINAL ordinary derivative separately:

    Q_j(Z)=tau^(-j)P_j(tau Z), R_j(Z)=tau^(1-j)P_j'(tau Z),
    Q_(j+1)=ZQ_j-[(1-q^j)/t]Q_(j-1),
    R_(j+1)=Q_j+ZR_j-[(1-q^j)/t]R_(j-1),
    Q_0=1,Q_1=Z,R_0=0,R_1=1.

All coefficients are integral. Since -(1-q^j)/t reduces to j mod p, including zero when p divides j, Q reduces to M_j and R to its separately evolved differentiated recurrence. The integer formula for M_p gives M_p=Z^p mod p: every nonleading term has numerator divisible by p and denominator prime to p. Starting at each multiple of p, where the recurrence coefficient vanishes, induction through the next p-1 steps gives

    M_(ap+b)=Z^(ap)M_b, a>=0, 0<=b<p.

The derivative recurrence, or formal differentiation after this justified coefficientwise low reduction, gives

    Q_n -> Z^(cN)M_d(Z),
    R_n -> d Z^(cN)M_(d-1)(Z).                             (8.1)

No high-root simplicity is inferred by differentiating an inseparable residual. Section 5 independently used the original high ordinary derivative.

Since d<p, backwards propagation in the Hermite recurrence gives gcd(M_d,M_(d-1))=1 modulo p; since d is a unit, M_d'=d M_(d-1) is coprime to M_d. Its constant C_m is also a unit. Equivalently,

    Res(M_d,M_(d-1))=product_(j=1)^(d-1) j^j,
    Disc(M_d)=(-1)^(d(d-1)/2) product_(j=1)^d j^j.

All possible prime divisors are <=d, so the boundary d=p-1 creates no exception. Over the algebraically closed residue field M_d has exactly d distinct nonzero roots. Simple-root Hensel lifting applies to THESE nonzero low classes and supplies exactly one simple root per class, with v(X)=1/2 and the nonzero derivative residue (8.1), hence value (n-1)/2.

The low roots are outside every high disk, where X-values are >=1. The counts exhaust the original monic degree:

    d+beta*cL=d+cN=n.

There are no additional clusters, no unexamined zero residual contribution beyond the high roots, and no zero root. This proves every original P_n root simple.

## 9. Original H, every primitive phase, and the algebraic-square kernel

The exact identities are

    H_n(v0^2)=v0^n P_n(X), X=v0+v0^(-1),
    H_n'(z)=v0^(n-2)[(n/2)P_n+(v0-v0^(-1))P_n'/2].

All counted P roots have positive valuation, so none is +/-2. On the branch v0 near i, the coordinate maps z=v0^2 and X=v0+v0^(-1) have unit derivatives, and give an analytic isometry near z=-1. They map the n distinct P roots to n distinct H roots and preserve multiplicity before simplicity; degree n exhausts H_n. In particular the corresponding high H disks are v(z+q^a)>=rho. At any root the term proportional to P_n vanishes EXACTLY. The remaining multiplier is a unit with residue

    i^(n-1)=(-1)^(c/2+m-1)i.

Thus root-derivative valuations agree, while normalized units are not identified. This varies with c: at d=2 it is -i for c=2 but +i for c=4. Using the c=2 multiplier unchanged would be incorrect.

All recurrence edges 1-q^j, 1<=j<n, are nonzero by n<p^s. A common root of P_n and P_(n-1) would propagate backwards to P_0=1. At every P_n root xi the ORIGINAL diagonal Christoffel-Darboux identity therefore gives

    sum_(j=0)^(n-1) P_j(xi)^2/w_j
      =P_n'(xi)P_(n-1)(xi)/w_(n-1) !=0.

These are algebraic squares, not absolute-value squares. No real-root interlacing, Hermitian positivity, or replacement polynomial family is used.

The accepted coefficientwise statements and every new step use the actual mixed-characteristic lattice e=(p-1)p^(s-1). Integer factors are retained before reduction; p-divisibility never falsely creates a unit. For any characteristic-zero primitive phase choose an algebraic p-adic embedding and its own t=q-1. The same proof applies uniformly for every s>r. Injectivity, or Galois conjugacy, carries nonvanishing to every primitive phase. No auxiliary finite-characteristic simplicity is asserted.

## 10. Fresh minimal controls and remaining gates

The proof is Sections 2-9. Finite controls are transcription and falsification checks, not a proof of uniformity. Newly written standard-library controls use:

- Exact symbolic independent matching/recurrence expansions for short tails, and the full fraction-free identity with independent A,A',M,M' symbols.
- The complete general-c Hermite pivot sum, including both c=4 pivots and all c/2 pivots for selected larger digits, exact integer constant units, and central residual gcds.
- A small set of new (p,c,d) residue fixtures including c=d=p-1, an adjacent-obstructed c, and a harmless auxiliary-cancellation boundary. Low original-polynomial and ordinary-derivative residue recurrences are evolved separately, without accepted code or high-degree cyclotomic scans.
- Negative controls for an omitted correction, missing square, wrong U edge start, a single selected derivative pivot, a copied c=2 central scalar/H multiplier, and a discarded low derivative.

Source and candidate inventory verification are separate from these controls. Source pins, complete byte inventories, author/review bindings, and a manifest/seal protect the candidate. A cold replay of only the NEW controls must equal the stored result under normal and optimized Python. No supplied program is imported or executed; no accepted control is rerun; no unrelated module is run. No external repository, document, Library item, or source package is changed.

The mathematical exceptional set within scope is empty. The open gate is independent review of these exact frozen bytes, with a separate publication/delivery audit only if later requested. This author candidate does not accept itself.
