# First-order Fourier envelope cancellation: 5N/3 original signed banks

23 October 2026. Author candidate for independent review. No publication or research-table status change is made by this file.

## 1. Result and exact contribution

Let N be odd, d >= 4, N >= 6d-2, and m=N-d. Let k be a field containing a supplied primitive Nth root q, with char(k) not dividing N. There exists a monic polynomial g of degree m with m distinct nonzero roots in a genuine algebraic splitting extension L/k such that the negative unnormalized Fourier matrix

    F[a,t] = q^(-at)

is a sum of at most 2m+2 ORIGINAL individual signed phase-weighted resolvent banks. A bank is exactly

    B_(epsilon,delta)(alpha,beta;w)
      = (1/N) sum_(j=0)^(N-1) w_j
        (I-alpha S^epsilon-beta q^(epsilon delta j) T^delta)^(-1),
    S e_t=e_(t+1),  T e_t=q^t e_t,
    epsilon,delta in {+1,-1},  Delta=1-alpha^N-beta^N != 0.

The same-sign groups use the m roots of g, both cross-sign groups have the single node alpha=1, and every beta=1. These are signed integer powers even in characteristic two. There are no zero-node banks, derivative atoms, trace banks, new generators, products of banks, or external endpoint maps. Raw weights may be zero. All physical nodes are nonzero, and Delta=-alpha^N is a unit.

For infinite k, the coefficients of g can lie in k. For finite k=F_Q, the coefficients can lie in F_(Q^2), and its genuine splitting field has degree at most m! over that coefficient field, hence at most 2m! over F_Q. The coefficient-field degree two is NOT a splitting assertion. All field preparation, root recovery, raw weights, and literal application costs are exposed in OPERATION_LEDGER.md.

Taking d=floor((N+2)/6) gives, for every odd N >= 23 and every admissible characteristic,

    B <= 2N-2floor((N+2)/6)+2 = 5N/3+O(1).

The previously accepted all-characteristic theorem gives N>=8d-10 and leading constant 7/4. This candidate improves the bank constant by replacing its double constant-coefficient annihilation with a first-order variable-coefficient Fourier-envelope cancellation. The original bank grammar, enlarged envelope, generic guards, and physical reconstruction are unchanged. It is a finite-network representation bound, NOT a faster FFT, practical compiler, minimum, base-field attainment, or historical novelty claim.

## 2. Exact source bindings and inherited ingredients

Accepted baseline files:

- baseline/THEOREM.md, SHA256 d994217b228c62bf36c3b0d66d55657733f42fe64aa286d33a95e0e82d23358c.
- Its OPERATION_LEDGER.md, SHA256 41c18c4ab22e95f3b36ae14366f0896ea13a239f44532b08cea92fd0028a54f5.
- Independent acceptance: baseline/INDEPENDENT_REVIEW.md.

SOURCE_BINDINGS.json records these byte identities, the accepted source pins, and freshly recomputed original Git blob and SHA256 identities. In particular the original characteristic-zero enlarged-envelope and axis proof is pinned to AgentSlop-Si/research commit 3834be7716370cfddf84ab1200da62b7887feb05, path math/checkpoints/2026-10-10-1839/sources/research_cycle_1824/axis_nonvanishing/AXIS_NONVANISHING_CANDIDATE.md, Git blob 6b0ccdab3341fe4a1cccfd7fde55ca986a07cd79, SHA256 2a22a99baf19cdc6bd78f90323b77be7b4c1b11c1866286f4a174a731ecb5040.

The whole-left row identity and reconstruction are pinned in the same commit at math/checkpoints/2026-10-10-1839/sources/research_cycle_1735/common_annihilator_barrier/WHOLE_LEFT_RANK_ENVELOPE.md, Git blob 6a417b39b7788b45e62e79d3083f1ed31887c953, SHA256 8bac3e52ef92ad00ab45ae55ab5cf9190e77e6855b3b752a8e569722f572998c.

The proof below reproduces the needed inherited arguments so the new range can be audited throughout; those ingredients are not claimed as new.

## 3. Original Fourier coefficients and unchanged whole-left envelope

Fractions in exponents mean inverses modulo odd N, never division by 2 or 4 in k. Set

    h=4^(-1) mod N, e=2^(-1) mod N, rho=q^e, C_j=q^(h j^2).

Then rho is primitive and rho^2=q. For r=[epsilon a]_N, ell=[delta b]_N define G_(epsilon,delta)(a,b) to be the Gaussian coefficient [r+ell choose ell]_(q^(epsilon delta)) if r+ell<N, and zero otherwise. Every Gaussian coefficient in the supported triangle is nonzero: its numerator and denominator factors 1-q^j all have 0<j<N.

The Weyl coefficients of F in the basis S^a T^b are gamma f(a,b), where

    f(a,b)=q^(h(a+b)^2),  gamma=(1/N) sum_t q^(-t^2) != 0.

Trace extraction gives (1/N) sum_t q^(-bt) F[t+a,t], and completing the square modulo N gives this formula. For the two Gauss sums G_+,G_-, the invertible residue substitution u=s-t, v=s+t gives G_+G_-=N. Hence gamma is nonzero in all allowed characteristics, including two.

For 1<=b<=(N-1)/2 let

    T_b=1/G_-+(N-b,b),
    v_b(j)=(f(j,b)-T_b G_-+(j,b))/G_++(j,b),
             1<=j<=N-b-1.

The recurrence matrix A has row (v_b(a+j))_(j=0)^m for every a,b>=1 with a+b<=d-1. These are exactly all length-(m+1) windows of the whole-left sequences. A monic degree-m g(t)=sum_j c_j t^j in ker A supplies their common recurrence.

Keep the accepted enlarged envelope EXACTLY:

    D(z)=product_(j=2)^(d-1)(1-q^j z),
    E={((C_j P(rho^j)+R(q^j))/D(q^j))_(j=0)^m:
         deg P<=3d-7, deg R<=d-2},
    U=E^perp, U_0={g in U:c_0=0}.

Every D(q^j) is nonzero since 2<=j+index<=N-1. There are at most 4d-7 generators, so

    dim U >= N-5d+8 >= d+6.

The earlier lower bound 3d-2 is NOT used in the new range. All-ones lies in E by P=0,R=D, so every member of U vanishes at 1.

For a recurrence row put s=a+b and

    Q_b=product_(j=1)^b(1-q^j),
    F_(a,b)(z)=D(z)/product_(j=1)^b(1-q^(a+j)z),
    R_(a,b)(z)=product_(j=1)^b(1-q^(a-j)z),
    B_b=T_b (-1)^b q^(b(b+1)/2).

The denominator factors are among those of D, so F is a polynomial. The direct Gaussian product identity is

    D(q^j)v_b(a+j)
      =Q_b q^(h s^2) C_j rho^(sj) F_(a,b)(q^j)
       -B_b R_(a,b)(q^j)F_(a,b)(q^j).

Where the cross triangle is absent, R contains a zero factor and this remains valid. Its chirp polynomial is a scalar times t^s F_(a,b)(t^2), of degree s+2(d-2-b)<=3d-7. Its ordinary polynomial has degree d-2. Thus every original recurrence row belongs to E and U is contained in ker A. No rank-saturation assumption is used.

## 4. New first-order cancellation and its exact zero count

Let S now denote forward shift on scalar sequences indexed by integers; it is not an additional physical bank generator. From C_(j+1)=q^h rho^j C_j, a constant-coefficient factor S-lambda acts on a chirp polynomial as

    P(t) -> q^h t P(rho t)-lambda P(t).

A nonzero P gains exactly one degree with nonzero leading coefficient. Thus any product of these factors is injective on chirp polynomials.

The consecutive-factor structure of D supplies the key identity

    (1-q^2 z)D(qz)=(1-q^d z)D(z).

For x!=0 define the FIRST-ORDER variable-coefficient operator

    (L_x y)_j=(1-q^(j+2))y_(j+1)-x(1-q^(j+d))y_j.

It has the following exact properties.

1. L_x(x^jD(q^j))=0, by the displayed D identity.
2. L_x(R(q^j))=R_x(q^j), where

       R_x(z)=(1-q^2z)R(qz)-x(1-q^dz)R(z),
       deg R_x<=d-1.

3. L_x(C_j P(rho^j))=C_j Phi_x(P)(rho^j), where

       Phi_x(P)(t)=q^h t(1-q^2t^2)P(rho t)
                   -x(1-q^dt^2)P(t).

   If P has degree p and leading coefficient a_p!=0, Phi_x(P) has degree EXACTLY p+3, with leading coefficient -q^(h+2)rho^p a_p!=0. The other summand has degree at most p+2, so no cancellation is possible, in any characteristic.
4. For the derivative target, with j interpreted in the field,

       L_1(jD(q^j))=(1-q^(j+d))D(q^j).

   Indeed the D identity identifies the two multiplying factors, leaving (j+1)-j=1. This is an ordinary polynomial in q^j of degree d-1. It is NOT claimed to vanish under L_1 alone.

Let

    M_+=product_(r=0)^(d-1)(S-q^r).

This order-d constant operator kills every ordinary polynomial of degree at most d-1 evaluated at q^j. It is injective on chirp polynomials and raises their degree exactly d. Consequently M_+ L_x kills the fixed-root target and the ordinary envelope part, and M_+ L_1 kills both the derivative target and ordinary part. A surviving nonzero chirp polynomial would have degree at most

    (3d-7)+3+d=4d-4.

If the starting equality is known at j=1,...,m, applying L_x uses only j=1,...,m-1. Applying M_+ then leaves zeros at j=1,...,m-d-1, precisely

    m-d-1=N-2d-1 >= 4d-3 > 4d-4.

All these rho^j are distinct, and 4d-4<N. Polynomial interpolation therefore forces the transformed polynomial, and by injectivity P itself, to vanish.

IMPORTANT: L_x has vanishing coefficients at some residue positions. The proof never divides by those coefficients and never propagates a recurrence using L_x. Only its algebraic cancellation and the stated finite interval are used. Propagation is done later, after P=0, with a different constant-coefficient operator whose endpoints are units.

This is the precise replacement for the prior order-(2d-2) cancellation, which left N-3d+2 points for degree 5d-9 and required N>=8d-10.

## 5. Endpoint independence and exact fixed divisors

First retain the accepted sparse-support argument, whose weaker needed range is N>=6d-6. If an envelope vector is supported on {0,1,m}, then C_jP(rho^j)+R(q^j)=0 for j=2,...,m-1. Apply

    M=product_(r=0)^(d-2)(S-q^r),

of order d-1. The chirp degree is at most 4d-8 and the zero interval has N-2d-1>4d-8 points. These points are distinct and 4d-8<N. Thus P=0 and then R=0 by ordinary interpolation. Hence delta_0,delta_1,delta_m are jointly independent modulo E. The coefficient functionals c_0,c_1,c_m are independent on U, and c_1,c_m remain independent on U_0.

Suppose a nonzero x is a root of every member of U_0, over an algebraic closure. Linear duality says evaluation at x belongs to E+span(delta_0). Thus some envelope satisfies

    C_jP(rho^j)+R(q^j)=x^jD(q^j), j=1,...,m.

Section 4 gives P=0. Now and ONLY now let

    L_x^old=product_(r=0)^(d-2)(S-xq^r).

The difference R(q^j)-x^jD(q^j) obeys the constant recurrence M L_x^old of order 2d-2 with both leading and constant coefficients nonzero. Its m>=2d-2 consecutive zeros propagate forwards and backwards. At j=0,N, since D(1)!=0, this gives x^N=1. Write x=q^s with 0<=s<N. The identity on N roots gives R(z)=z^sD(z) modulo z^N-1. D has nonzero endpoint coefficients and degree d-2; its two translated endpoints must both lie in [0,d-2]. Since 2(d-2)<N, this forces s=0. Thus x=1.

For multiplicity at 1, suppose the derivative functional (j) belongs to E+span(delta_0). Its scaled envelope equals jD(q^j) on j=1,...,m. Section 4, with the explicit derivative calculation, gives P=0. The remaining difference R(q^j)-jD(q^j) obeys M^2: (S-q^r)^2 kills j q^(rj), including in characteristic two. Again m>=2d-2 lets zeros propagate both ways. At j=0,N this forces 0=ND(1), contrary to char(k) not dividing N.

Sparse independence makes the root 0 simple on U_0 and excludes 0 as a fixed root of U. The derivative exclusion makes 1 simple even on U_0. Therefore, also after extending to an algebraic closure,

    gcd(U_0)=t(t-1),  gcd(U)=t-1.

## 6. All-characteristic legal-root and full-axis guards

These are the accepted guard mechanisms; every range requirement is checked here.

For a polynomial space V with gcd(V)=1 and positive maximum degree, its universal polynomial H=sum Z_i h_i is irreducible over k(Z): a factorization in k[t,Z] has total Z-degree one, so one factor lies in k[t] and divides every basis member, hence is a unit; Gauss's lemma gives the parameter-field conclusion.

Take V_1=U/(t-1). It has gcd one. If g=(t-1)h, then h_0=-c_0 and h_1=-c_0-c_1. Joint sparse independence makes the latter a nonzero parameter functional, so the universal H' is nonzero, even in characteristic two. Irreducibility then gives separability. The derivative-at-1 exclusion makes h(1)=g'(1) generically nonzero as well. Thus full degree, nonzero constant, and squarefreeness are nonzero guards on the monic affine slice U_1={g in U:c_m=1}.

For the axis, take V_0=U_0/[t(t-1)], of maximum degree r=m-2 and gcd one. Its constant and leading functionals are -c_1 and c_m, which are independent. For the universal f, if f and rev_r f=t^r f(1/t) share a factor, irreducibility and equal degree give rev_r f=lambda f. Reversing twice gives lambda^2=1, so lambda=1 or -1 (only 1 in characteristic two). Comparing independent parameter coefficients would place the whole space in a fixed reversal eigenspace and contradict endpoint independence. Hence their reciprocal resultant is nonzero.

Over the algebraic closure choose f with nonzero endpoints and reciprocal-coprime, and normalize g_0=t(t-1)f to be monic. This auxiliary g_0 is NOT assigned physical banks. For any monic g let p_a be the coefficient vector of t^a mod g, 0<=a<N, and form X_N(g) with row a

    (p_a, 1, p_[-a]_N).

All entries are polynomial in g's nonleading coefficients even when g(0)=0; only nonnegative residue powers are used. For A(t)=sum_(a=0)^(N-1) A_a t^a, row dependence is exactly

    g divides A, A(1)=0, g divides J_N A,
    J_N A=t^N A(1/t)+A(0)(1-t^N).

At g_0, A(0)=0. The reversal condition then implies rev_r(f) divides A. The coprime factors t,t-1,f,rev_r(f) force their product of degree 2m-2 to divide A. But

    2m-2>N-1, equivalently N>2d+1,

which follows from N>=6d-2 and d>=4. Thus A=0 and rank X_N(g_0)=N. This establishes one nonzero N-column minor on U_1, not an invalid legal-point inference from reciprocal coprimality.

The constant, discriminant and this axis minor are all nonzero polynomials on the SAME affine linear space U_1. Their product is nonzero. Over infinite k they have a simultaneous nonzero k-point, supplying the desired good g.

## 7. Finite coefficient descent and genuine splitting

For monic degree-m g, the coefficients of t^j mod g have total degree at most max(0,j-m+1) in the nonleading coefficients. The nonconstant row-degree maxima of X_N are d,...,1 on rows 1,...,d and 1,...,d on rows m,...,N-1. They are disjoint because N>2d. Every N-column minor therefore has degree at most d(d+1).

The degree-m monic discriminant has total degree at most 2m-2 in every characteristic, including when it is a square in characteristic two. With the constant guard, the total guard degree is at most

    H=d(d+1)+2m-1.

If k=F_Q contains q then N divides Q-1, so Q>=N+1. Our new range implies d<=N/4 and N>=23, hence

    H <= N^2/16+9N/4-1 < (N+1)^2/2 <= Q^2/2.

The elementary finite-grid zero bound for a nonzero s-variate degree-H polynomial gives at most H R^(s-1) bad points in F_R^s. Taking R=Q^2 proves that E=F_(Q^2) contains a good coefficient point, and uniform affine sampling there succeeds with probability greater than 1/2. Tests are exact: c_0!=0, gcd(g,g')=1, rank X_N(g)=N. Enumeration of all points or an (H+1)-scalar grid is a deterministic alternative. No two-trial deterministic guarantee is asserted.

A genuine splitting extension is still required. The splitting-field degree of a squarefree degree-m polynomial is at most m!. Over finite E its actual degree is the lcm of irreducible factor degrees. The overfield F_(R^(m!)) contains all roots and may be constructed exhaustively as charged in the ledger. It is not a polynomial-degree extension claim. For arbitrary positive-characteristic k containing q, the subfield F_p(q) is finite; construct there and take the compositum with k. For arbitrary infinite k this is an algebraic existence statement, not an unpriced efficient field implementation.

## 8. Completion to all original bank coefficients

Let x_1,...,x_m be the actual distinct nonzero roots of a good g in its splitting field. For each positive b choose ++ amplitudes U_i with

    sum_i U_i x_i^a=v_b(a), 1<=a<=N-b-1.

When the interval has at least m entries, solve its first m entries by the nonzero-node Vandermonde matrix and use the monic recurrence to propagate the rest. Otherwise pad to m entries and solve. Set the -+ singleton amplitude to T_b and the +- singleton amplitude to zero. Choose -- amplitudes V_i satisfying

    sum_i V_i=f(0,b)-T_b-sum_i U_i,
    sum_i V_i x_i^r=(f(N-r,b)-T_bG_-+(N-r,b))/G_--(N-r,b),
                       1<=r<=b-1.

Here b<=(N-1)/2<=m, so these b consecutive moments can be padded and solved. The ++ group handles a=1,...,N-b-1, the forced singleton handles a=N-b, and -- handles the right interval and axis a=0. All Gaussian divisions are on their nonzero support. Thus every coordinate of every positive row is matched.

Reflect both indices and both signs to handle negative b. The target is invariant and the Gaussian products transform accordingly. For each orientation b->[delta b]_N is a bijection, so no sector assignments conflict.

For b=0 solve X_N(g) against f(a,0), using full row rank, and convert the two length-m moment vectors by Vandermonde inversion. Allocate its scalar column to one cross bank, setting the other's axis amplitude to zero.

For a bank with normalized sector amplitudes h_ell put

    w_j=gamma Delta sum_(ell=0)^(N-1) h_ell q^(-epsilon delta j ell),
    beta=1, Delta=-alpha^N.

Let X_j=alpha S^epsilon+q^(epsilon delta j)T^delta. The quantum-binomial identity at the primitive signed commutation root gives X_j^N=(alpha^N+1)I: intermediate Gaussian numerators vanish and their denominators are nonzero. Therefore the literal two-sided inverse is

    (I-X_j)^(-1)=(I+X_j+...+X_j^(N-1))/Delta.

Finite character inversion of the raw weights gives exactly the matched gamma-scaled Weyl coefficients. The sum is the literal negative unnormalized Fourier matrix, not merely a moment identity or a finite test. Both cross banks are effective because their forced exclusive-coordinate sectors are nonzero. Any ineffective same-sign banks may be omitted; the count is at most 2m+2.

## 9. Controls and boundaries

Fresh exact controls are authored in fresh_exact_controls.py. They check the new first-order identities, leading terms, singular variable-coefficient positions, actual original recurrence rows, fixed-divisor gcds, endpoint independence, and all legal coefficient/axis guards over several prime fields and characteristic-two extension fields. They do not instantiate enormous splitting fields or infer an all-N proof from finite tests. No historical supplied code was executed or imported.

The new theorem concerns the original full bank dictionary through a valid sufficient architecture. It proves no matching lower bound, unrestricted optimum, FFT acceleration, numerical stability, base-field attainment, cheap root finding, or closure of broader research owners. The concrete mechanism gain is the q-shift ratio of the actual denominator D, not generic dimension counting, a field-extension restatement, or a new grammar restriction.
