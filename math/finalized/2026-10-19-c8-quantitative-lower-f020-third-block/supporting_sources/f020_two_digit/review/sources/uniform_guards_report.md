# F020: uniform odd-order node separation; the ordinary guard remains open

18 October 2026 UTC. Canonical owner F020; F023 remains its alias. Author proof with fresh transcription controls; independent review is requested. No external write or uploaded-package execution was performed.

## Result and terminal boundary

For every odd integer d >= 3, every primitive dth root omega, and every integer 0 <= b < d, let

    H_b(z;omega) = sum_(k=0)^b [b choose k]_omega z^k,
    U_b = H_b                         when b is even,
    U_b = H_b/(z+1)                   when b is odd.

This packet proves uniformly:

1. gcd(U_b, 1+z^d) = 1 in characteristic zero.
2. The forced odd root is simple: H_b'(-1) != 0 for odd b.
3. H_b has no dth root of +1 as a zero; in particular H_b(1) != 0.

Thus the requested fixed-node guard is settled at author-proof level for all odd orders, a larger domain than odd prime powers. The proof uses the actual Rogers–Szegő q-difference equation, a rotation to real positive Jacobi recurrences on integer and half-integer node lattices, and a sector sum for the forced root. It is not extrapolation from a root-order census. The argument is self-contained below, including all primitive embeddings.

For the ordinary discriminant D_b = Disc_z(H_b), the accepted integral factorization D_b=(q-1)^[b(b-1)/2] V_b is strengthened by a uniform proof that

    D_b is monic of degree b(b^2-1)/3,
    V_b is monic of degree b(b-1)(2b-1)/6.

Consequently V_b mod p is nonzero for every prime p. The finite-t sufficient criterion therefore always has a finite, well-defined t_p(b). But its strict inequality is false for admissible actual-family pairs, already at (p,s,b)=(3,2,4), where t_3(4)=8 >= phi(9)=6 although the characteristic-zero polynomial is squarefree. That proposed universal route stops for a mathematical reason, not a resource limit.

The remaining ordinary guard is reduced precisely to the nonisotropy lemma in Section 6. No proof of that lemma or characteristic-zero counterexample was obtained. Therefore the full uniform prime-power static package is NOT closed; F020 remains TO RESEARCH, priority 58. No automatic all-A extension or census change is justified.

## 1. Algebraic identities and a real-Jacobi lemma

Work first at the principal embedding

    q = exp(i theta), theta = 2 pi/d, d=2h+1.

The q-Pascal identity gives

    H_b(qz) = (1-z)H_b(z) + q^b z H_b(z/q).             (1)

For clarity, comparing z^k coefficients reduces (1) to

    (1-q^k)[b choose k]_q = (1-q^(b-k+1))[b choose k-1]_q.

The degree-b polynomial is reciprocal:

    H_b(z)=z^b H_b(1/z).                              (2)

The three-term recurrence is

    H_0=1, H_1=1+z,
    H_(n+1)=(1+z)H_n-z(1-q^n)H_(n-1).                (3)

We use the elementary real-Jacobi fact: if monic polynomials satisfy

    M_0=1, M_1=X-a_0,
    M_(j+1)=(X-a_j)M_j-beta_j M_(j-1),
    a_j real, beta_j>0,

then every M_j has only real simple zeros. Indeed M_j is the characteristic polynomial of the real symmetric tridiagonal matrix with diagonal a_0,...,a_(j-1) and off-diagonal entries sqrt(beta_1),...,sqrt(beta_(j-1)). Its eigenvalues are real. At an eigenvalue an eigenvector is determined by its first coordinate using the nonzero off-diagonal recurrence; the first coordinate cannot vanish. Hence each eigenspace is one-dimensional, and real-symmetric diagonalizability makes each eigenvalue simple. Only reality, not simplicity, is needed for the separation proof.

## 2. Integer lattice: all roots of 1+z^d except -1

Define, for integral or half-integral j,

    f_j = H_b(-q^j),
    y_j = exp(-i theta(bj/2+j^2/4)) f_j,
    lambda = 2 exp(-i theta(2b+1)/4),
    c_j = cos(j theta/2).

Fractional powers here are explicitly the displayed complex exponentials, not algebraically ambiguous root choices. Substituting z=-q^j in (1), then applying the displayed rotation, gives exactly

    f_(j+1)=(1+q^j)f_j-q^(b+j)f_(j-1),
    y_(j+1)=lambda c_j y_j-y_(j-1).                   (4)

For b<d, the argument of lambda is -pi(2b+1)/(2d), strictly between -pi and 0. In particular lambda is not real. Also c_j>0 for 0<=j<d/2.

Let E_r=product_(a=1)^r(1-q^(2a-1)), E_0=1. Recurrence (3), or pairing coefficients followed by (3), gives the standard evaluations

    H_(2r)(-1)=H_(2r)(-q)=E_r,
    H_(2r+1)(-1)=0,
    H_(2r+1)(-q)=E_(r+1).                             (5)

Every product appearing in (5) is nonzero for the relevant b<d. One quick derivation of the second nonzero evaluation is to use the even equality in (3):

    H_(2r+1)(-q)=E_r[(1-q)+q(1-q^(2r))]
                =E_r(1-q^(2r+1)).

### Even b

Divide y_j by E_(b/2), obtaining polynomials T_j(lambda) with

    T_0=1, T_1=X/2,
    T_(j+1)=X c_j T_j-T_(j-1).

For j>=1 the leading coefficient is L_j=(1/2) product_(a=1)^(j-1)c_a. Normalizing M_j=T_j/L_j gives

    M_0=1, M_1=X,
    M_2=X^2-2/c_1,
    M_(j+1)=X M_j-[1/(c_j c_(j-1))]M_(j-1), j>=2.

All needed recurrence coefficients are positive for j<=h. The real-Jacobi lemma therefore makes T_j(lambda) nonzero for 1<=j<=h. Also f_0=E_(b/2) is nonzero.

### Odd b

Here y_0=0 and y_1 is nonzero by (5). Let S_m=y_(m+1)/y_1. Then

    S_0=1, S_1=c_1 X,
    S_m=X c_m S_(m-1)-S_(m-2), m>=2.

Divide by product_(a=1)^m c_a to obtain a monic real-Jacobi sequence with beta_(m-1)=1/(c_m c_(m-1))>0. Thus y_j, and hence f_j, is nonzero for 1<=j<=h. For h=1 only S_0 is needed; no absent coefficient is invoked.

Finally reciprocity (2) gives

    f_(-j)=(-1)^b q^(-bj) f_j.                        (6)

The indices -h,...,h cover every residue modulo d. Hence H_b is nonzero at every zero -q^j of 1+z^d except j=0 when b is odd.

## 3. The forced odd root is simple

This is already part of the accepted all-odd overlap theorem; we include the short argument to make the current node result self-contained. For b=2r+1<d let g_r=H'_(2r+1)(-1). Differentiating (3) yields

    g_0=1,
    g_r=E_r+(1-q^(2r))g_(r-1).

Consequently

    g_r/E_r = sum_(j=0)^r product_(a=j+1)^r
                          (1-q^(2a))/(1-q^(2a-1)).    (7)

For 1<=a<=r, both 2a and 2a-1 lie strictly between 0 and d. Each ratio in (7) equals

    exp(i pi/d) sin(2a pi/d)/sin((2a-1)pi/d),

a positive real multiple of exp(i pi/d). The product indexed by j has argument (r-j)pi/d in [0,r pi/d], and r pi/d<pi/2. Every term has positive real part, so the sum is nonzero. E_r is nonzero, hence g_r!=0. This covers r=0 as the empty-product case.

For odd b, U_b(-1)=H_b'(-1)=g_r. Together with Section 2 this proves gcd(U_b,1+z^d)=1, including the -1 node itself. The node polynomial 1+z^d is squarefree in characteristic zero, so no multiplicity ambiguity remains.

## 4. Half-integer lattice: no positive dth-root nodes

This additional endpoint result is useful for the remaining ordinary-squarefreeness route.

The elementary product identity

    H_b(r;r^2)=product_(a=1)^b(1+r^a)                 (8)

follows by substituting the product into (3). Set r=-exp(i pi/d). Then r^2=q and, since d is odd, r^d=1. Thus no r^a equals -1, and (8) proves f_(1/2)!=0.

By reciprocity and the rotation in Section 2,

    y_(-1/2)=(-1)^b y_(1/2).

Define T_m=y_(m+1/2)/y_(1/2), m>=0. Equation (4) gives

    T_0=1,
    T_1=c_(1/2) X-(-1)^b,
    T_(m+1)=c_(m+1/2) X T_m-T_(m-1), m>=1.

After division by the positive leading coefficient product_(a=0)^(m-1)c_(a+1/2), these are monic Jacobi polynomials. Their initial diagonal is (-1)^b/c_(1/2); later diagonals vanish; the lower recurrence coefficients are 1/[c_(m+1/2)c_(m-1/2)]>0. The real-Jacobi lemma applies through m=h, since every coefficient used has index at most h-1/2<d/2. Nonreality of lambda proves f_(m+1/2)!=0 for m=0,...,h. Reciprocity supplies the negative half-indices. The indices +/-1/2,...,+/-d/2 cover all d roots z=-q^j of z^d=1, with the endpoint z=1 duplicated. In particular H_b(1)!=0.

## 5. Primitive embeddings and uniform nonzero discriminant reduction

### Embeddings

The proofs above used the principal root q=exp(2pi i/d). Every other primitive omega is q^a with gcd(a,d)=1. The automorphism q -> q^a sends H_b's coefficients, U_b's coefficients, their derivative, and each node -q^j to the corresponding quantities. Equivalently, it sends the nonzero algebraic resultant Res(U_b,1+z^d) to its conjugate. Thus all nonvanishing conclusions hold at every primitive embedding. No positivity assertion is transported between embeddings; only the algebraic nonvanishing is transported.

### Monicity of the discriminant

For b>=2 the Gaussian coefficient [b choose k]_q is monic of degree k(b-k). Work over the Laurent-series field C((t)), where t=q^(-1). For each j=1,...,b set z=t^(2j-b-1)w. The valuation of the k-th term of H_b after this substitution is

    -k(b-k)+k(2j-b-1)=k(k-2j+1).

Its minimum occurs exactly at k=j-1 and k=j. After multiplying by the appropriate power of t, the initial polynomial is

    w^(j-1)(1+w).

At w=-1 this has a simple nonzero root. Formal Hensel lifting (or recursive coefficient solving with nonzero first derivative) therefore gives a root

    rho_j=-q^(b+1-2j)(1+O(q^(-1))).

The valuations are all distinct, so these are all b roots. For i<j the leading term of rho_i-rho_j is -q^(b+1-2i). Therefore

    D_b=product_(i<j)(rho_i-rho_j)^2
       =q^[2 sum_(i=1)^b (b-i)(b+1-2i)](1+O(q^(-1)))
       =q^[b(b^2-1)/3](1+O(q^(-1))).                 (9)

Since D_b is integral, (9) proves that D_b is monic with the stated degree. Dividing by the already accepted monic factor (q-1)^[b(b-1)/2] proves that V_b is monic of degree b(b-1)(2b-1)/6. For b=0,1 the stated discriminant convention gives V_b=1. In particular every reduction V_b mod p is nonzero, for every prime p.

The same two-term Newton polygon proof works directly over F_p((t)), including characteristic two, because the residual root -1 remains a simple root of 1+w. We do not need to assume any positive-characteristic static guard at a root of unity.

## 6. The exact remaining ordinary-squarefreeness lemma

Define the actual continuous-q-Hermite normalization

    P_0(X)=1, P_1(X)=X,
    P_(k+1)(X)=X P_k(X)-(1-q^k)P_(k-1)(X),
    w_k=product_(j=1)^k(1-q^j), w_0=1.

The identity

    H_b(v^2;q)=v^b P_b(v+v^(-1);q)                  (10)

follows from the same recurrence. For k<b<d every w_k is nonzero. The diagonal Christoffel-Darboux identity is

    K_(b-1)(X):=sum_(k=0)^(b-1) P_k(X)^2/w_k
      =[P_b'(X)P_(b-1)(X)-P_b(X)P_(b-1)'(X)]/w_(b-1). (11)

Equation (11) follows by telescoping the two recurrences; its terms are squares, not absolute squares. Consecutive P_b and P_(b-1) have no common zero: a common zero would propagate downwards by nonzero coefficients to P_0=1.

The remaining actual-family lemma is exactly:

    For every odd prime power d=p^s, principal q=exp(2pi i/d),
    2<=b<d, and every root xi of P_b,

        sum_(k=0)^(b-1) P_k(xi;q)^2 / product_(j=1)^k(1-q^j) != 0.   (L)

This is a nonisotropy assertion for the finite complex Jacobi eigenvectors. By (11) it is equivalent to simple roots of P_b. Section 4 excludes P_b(2)=P_b(-2)=0. The map X=v+v^(-1), z=v^2 in (10) is unramified over every relevant z except z=1, which is already excluded. Consequently (L) would prove the requested ordinary z-squarefreeness of H_b. Conversely a repeated P_b root away from the excluded endpoints gives a repeated H_b root. The forced X=0 root for odd b is already simple by Section 3.

No proof of (L) is obtained here. The real-Jacobi reasoning in Sections 2 and 4 applies to polynomials in the lattice spectral parameter lambda, not to P_b in X. It must not be transferred to (L). Here the weights and recurrence coefficients are complex, and (11) is a bilinear kernel without positivity.

For a concrete warning, take the nonzero recurrence coefficients

    u_1=(3-4i)/5, u_2=4/5, u_3=(3+4i)/5.

All have positive real part and strictly increasing arguments. Nevertheless the recurrence R_0=1, R_1=X, R_(j+1)=X R_j-u_j R_(j-1) gives

    R_4=(X^2-1)^2.

Thus nonzero coefficients, positive-real-part coefficients, ordered coefficient arguments, or nonsingular recurrence norms do not establish the required nonisotropy. This is NOT an actual-family counterexample; the geometric coefficients u_j=1-q^j in (L) require an additional argument. The primary Spiridonov–Zhedanov paper likewise explicitly warns that complex recurrence coefficients do not guarantee simple zeros (pages 1–2 of its arXiv version).

### Why the finite-t route also stops

By Section 5, t_p(b)=ord_(q-1)(V_b mod p) is always finite. The retained sufficient implication is

    t_p(b)<phi(p^s) implies D_b(omega)!=0.

A universal strict bound for all b<p^s is false. Fresh exact reconstruction gives

    V_4(q)=(q+1)^2(q^2+q+1)(q^3+3q^2+3q+5)^2
             * (q^4+3q^3+4q^2+3q+5),
    V_4(1+t) mod 3 = t^14-t^13-t^11-t^10+t^9+t^8,
    t_3(4)=8>=6=phi(9).

The exact field control gcd(H_4,H_4')=1 at d=9 confirms again that this is a failure of the sufficient test, not a characteristic-zero counterexample. Any completion through this route must supply a new nonvanishing mechanism for its failing cases, with an unlimited range theorem; merely estimating t or increasing the tested d cannot close the requested guard. Lemma (L) is the precise alternate missing mechanism recorded here.

## 7. Consequences, preserved normalizations, and exclusions

The requested node-separation side no longer needs a separate prime-power argument if this proof is accepted. It also combines with already established ordinary residual squarefreeness wherever that is independently available. In particular, it does not weaken the accepted b<p range, the d=9,25 certifications, the fixed-residual results, or the accepted all-odd overlap theorem.

The existing all-A local theorem may be composed only for (d,b) where ordinary residual squarefreeness has also been established. Since the uniform ordinary guard remains open, this packet does not assert the exact order formula for every b<p^s.

If that missing guard is later proved, the retained expected order is M=dA(A-1)/2+A(b mod 2). For an inherited coefficient C of (q^d-1)^M, the existing normalizations remain

    lim D_n(q)/(q-omega)^M = C(d omega^(-1))^M,
    [D_n/Phi_d^M](omega) = C(d omega^(-1)/Phi_d'(omega))^M,

and for d=p^s the last factor is C(omega^(d/p)-1)^M. No sign, Hermite discriminant product, resultant, overlap g^2 term, or leading-coefficient normalization is rederived or changed here.

F020/F023 status, existing priority, history, paired-support and separate endpoint obligations, historical attribution, arbitrary positive-characteristic guards, conditioning, FFT operation counts, and production implementation claims remain unchanged. No historical novelty or worldwide priority is asserted.

## 8. Checks, source binding, and review status

`check_guards.py` is freshly authored for this packet and uses installed SymPy exact arithmetic. It imports no uploaded or prior research program. The 82 checks cover q-Pascal against the q-difference identity, reciprocity, parity initial values, the half-lattice product, discriminant monicity and deflation through b=6, the exact known t-bound failure, its characteristic-zero squarefreeness at d=9, the q-Hermite transformation, the diagonal CD identity, exact integer/half-integer rotation bookkeeping, selected node controls at the already-covered orders 3, 5, 9, and the failed positivity shortcut. They are small transcription controls, not a new order census. `CHECKS.json` records every check.

One first run stopped because the installed polynomial-ring differentiation API takes a generator index rather than the external SymPy symbol. Changing h.diff(z) to h.diff(0) fixed this checker-interface error. The corrected complete run passed. No mathematical assertion was changed by the repair. Exact commands and outputs are in `RUN_LOG.md`.

Controlling sources were freshly read through the GitHub connector, and exact text copies are retained in `sources/`. `SOURCE_BINDINGS.json` gives pinned URLs, content hashes, and Git blob hashes. The separately supplied local copies contain one extra terminal newline; they were not falsely treated as byte-identical pinned blobs.

Primary literature consulted only for the limitation on complex orthogonality:

- Spiridonov and Zhedanov, “Zeros and orthogonality of the Askey-Wilson polynomials for q a root of unity,” Duke Math. J. 89 (1997), 283–305; arXiv:q-alg/9605034v2, pages 1–2: https://arxiv.org/pdf/q-alg/9605034 . Their top-degree orthogonality result is not used as a simplicity theorem for lower-degree P_b.
- The lattice product and q-difference machinery are classical Rogers–Szegő identities; the direct proofs above avoid relying on an unstated literature theorem. Cigler’s elementary treatment was inspected as background: https://arxiv.org/pdf/1602.07850 . No priority conclusion is inferred from this limited reading.

Independent review remains a separate required acceptance step. The proper terminal result of this scoped research is a uniform node theorem, unconditional nonzero reduction of V_b, and the precise missing ordinary-kernel lemma (L). The full target remains blocked on (L) or another genuine uniform ordinary-squarefreeness mechanism.
