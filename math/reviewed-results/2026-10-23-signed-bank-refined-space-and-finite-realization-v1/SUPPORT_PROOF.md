# A bounded structural-endpoint refinement of the original signed-bank theorem

23 October 2026. Author candidate, not independently accepted or published.

## 1. Exact claim and credit boundary

Let N be odd, d>=4, N>=6d-5, and m=N-d. Let k contain a supplied primitive Nth root q, with char(k) not dividing N. The negative unnormalized Fourier matrix F[a,t]=q^(-at) is a sum of at most 2m+2 ORIGINAL signed phase-weighted resolvent banks over a genuine algebraic splitting extension L/k:

    B_(epsilon,delta)(alpha,beta;w)
      =(1/N) sum_(j=0)^(N-1) w_j
        (I-alpha S^epsilon-beta q^(epsilon delta j) T^delta)^(-1),
    S e_t=e_(t+1), T e_t=q^t e_t,
    epsilon,delta in {+1,-1}, Delta=1-alpha^N-beta^N != 0.

The same-sign groups use the m distinct nonzero roots of one polynomial g; the two cross-sign singleton nodes are 1; beta=1 throughout. Raw weights may vanish. Signed powers retain their integer meaning in characteristic two. There are no physical zero nodes, derivative atoms, trace replacements, masks, products, new generators, or free root access.

For every odd N>=19, taking d=floor((N+5)/6) gives

    B <= 2N-2floor((N+5)/6)+2.

Relative to the accepted first-order bound 2N-2floor((N+2)/6)+2 on its N>=23 domain, this saves exactly two banks when N is 1 or 3 modulo 6, and agrees when N is 5 modulo 6. The gain is a uniform CONSTANT-TERM refinement on infinite families, NOT a leading-constant improvement: both bounds remain 5N/3+O(1).

The t^2 divisibility and formal-endpoint zero are explicitly present in the original whole-left source. They are not discoveries claimed here. The contribution is retaining these inherited constraints in the accepted first-order proof, thereby reducing its sufficient threshold by three. No novelty, minimum, faster FFT, efficient implementation, base-field splitting, or broader owner closure is claimed. Later coefficient-generator theorems are NOT automatically extended to this new domain.

## 2. Sources and unchanged definitions

SOURCE_BINDINGS.json freezes byte identities of the accepted first-order theorem and ledger, its independent review, and the original whole-left and axis sources. The original whole-left source is AgentSlop-Si/research commit 3834be7716370cfddf84ab1200da62b7887feb05, path math/checkpoints/2026-10-10-1839/sources/research_cycle_1735/common_annihilator_barrier/WHOLE_LEFT_RANK_ENVELOPE.md, Git blob 6a417b39b7788b45e62e79d3083f1ed31887c953, SHA256 8bac3e52ef92ad00ab45ae55ab5cf9190e77e6855b3b752a8e569722f572998c. Section 3 of that source explicitly proves both structural constraints used here.

All fractional exponents mean inverses modulo odd N, not division by 2 or 4 in k. Put

    h=4^(-1) mod N, e=2^(-1) mod N, rho=q^e, C_j=q^(h j^2),
    D(z)=product_(r=2)^(d-1)(1-q^r z), J=m+1=N-d+1.

For all actual columns 0<=j<=m, D(q^j)!=0. At the single formal point J, D(q^J)=0. We never evaluate an envelope quotient at J.

For r=[epsilon a]_N and ell=[delta b]_N, G_(epsilon,delta)(a,b) is [r+ell choose ell]_(q^(epsilon delta)) on r+ell<N and zero otherwise. Every supported Gaussian division below is nonzero, also for composite N. Put f(a,b)=q^(h(a+b)^2). For 1<=b<=(N-1)/2 set

    T_b=1/G_-+(N-b,b),
    v_b(a)=(f(a,b)-T_b G_-+(a,b))/G_++(a,b),
                     1<=a<=N-b-1.

The original recurrence matrix A has row (v_b(a+j))_(j=0)^m for a,b>=1 and a+b<=d-1.

## 3. The refined envelope and its nonsingular inclusion

Define the vector space of polynomial pairs

    V={(P,R): t^2 divides P, deg P<=3d-7, deg R<=d-2,
                C_J P(rho^J)+R(q^J)=0}.

Define E by evaluating ONLY at the actual columns:

    E={((C_j P(rho^j)+R(q^j))/D(q^j))_(j=0)^m : (P,R) in V},
    U=E^perp, U_0={g in U:c_0=0}.

Before the last linear constraint the pair space has dimension

    (3d-8)+(d-1)=4d-9.

That constraint is nonzero, since its value on P=0,R=1 is 1. Hence dim E<=4d-10 and

    dim U >= (m+1)-(4d-10)=N-5d+11>=d+6.

P=0,R=D satisfies the constraint, so all-ones belongs to E and every g in U vanishes at 1.

For an actual row let s=a+b and put

    Q_b=product_(r=1)^b(1-q^r),
    F_(a,b)(z)=D(z)/product_(r=1)^b(1-q^(a+r)z),
    R_(a,b)(z)=product_(r=1)^b(1-q^(a-r)z),
    B_b=T_b(-1)^b q^(b(b+1)/2).

The inherited polynomial-numerator identity is

    D(q^j)v_b(a+j)
      =Q_b q^(h s^2) C_j rho^(sj) F_(a,b)(q^j)
       -B_b R_(a,b)(q^j)F_(a,b)(q^j).

The associated chirp polynomial is Q_b q^(h s^2)t^s F_(a,b)(t^2). Since s>=2 it is divisible by t^2, and its degree is at most 3d-7. Its ordinary part has degree d-2.

Here is an explicit all-characteristic proof of the formal constraint, using polynomial numerators, not a singular quotient. Write z_*=q^J=q^(-(d-1)). If s<d-1, the factor 1-q^(d-1)z remains in F_(a,b), so both numerator terms vanish at J. If s=d-1, then a+J=N-b and f(a+J,b)=1. Moreover

    R_(a,b)(z_*)=product_(r=1)^b(1-q^(-b-r)),
    G_-+(N-b,b)=(-1)^b q^(b(b+1)/2) R_(a,b)(z_*)/Q_b.

Thus B_b R_(a,b)(z_*)=Q_b. The two polynomial numerator terms cancel exactly at J. The chirp scalar in the first is Q_b f(a+J,b)=Q_b. This proof works in characteristic two with the same signed-power conventions. Therefore every original row lies in E and U is contained in ker A. No rank saturation is assumed.

## 4. Degree AND valuation under the accepted first-order operators

Use S for the forward shift of scalar sequences only; it is not an additional physical bank generator. Since C_(j+1)=q^h rho^j C_j, a constant factor S-lambda acts on the chirp polynomial by

    T_lambda P(t)=q^h t P(rho t)-lambda P(t).

For lambda!=0 and P!=0, its degree increases exactly by one and its t-adic valuation stays exactly ord_t(P): the unique lowest-degree term is -lambda times the old lowest term. Both coefficients are units.

The consecutive-factor identity is

    (1-q^2 z)D(qz)=(1-q^d z)D(z).

For x!=0 set

    (L_x y)_j=(1-q^(j+2))y_(j+1)-x(1-q^(j+d))y_j.

Then L_x annihilates x^jD(q^j), sends an ordinary polynomial of degree <=d-2 in q^j to one of degree <=d-1, and sends C_jP(rho^j) to C_j Phi_x(P)(rho^j), where

    Phi_x(P)(t)=q^h t(1-q^2t^2)P(rho t)-x(1-q^dt^2)P(t).

For nonzero P, Phi_x raises degree exactly three: its unique leading term has coefficient -q^(h+2)rho^(deg P) lead(P). It preserves ord_t(P), with unique lowest coefficient -x times the old one. In particular the inherited t^2 factor survives, and Phi_x is injective in every admissible characteristic.

For the derivative target,

    L_1(jD(q^j))=(1-q^(j+d))D(q^j),

an ordinary polynomial of degree d-1. This uses (j+1)-j=1 in k and remains valid in characteristic two.

Finally M_+=product_(r=0)^(d-1)(S-q^r) has order d, kills every ordinary polynomial of degree <=d-1, and raises chirp degree by d while preserving its t-adic valuation. Thus M_+L_x produces a chirp polynomial Q with

    deg Q<=4d-4, t^2 divides Q, deg(Q/t^2)<=4d-6.

If an envelope equality to x^jD(q^j), or to jD(q^j), is known at j=1,...,m, the common formal constraint in V extends it to J=m+1: both target numerators vanish there. This extension is an equality of polynomials evaluated at a point; no envelope denominator is evaluated or cancelled there. Applying L_x and M_+ then leaves zeros at

    j=1,...,m-d, exactly N-2d points.

These rho^j are distinct and nonzero. Under N>=6d-5,

    N-2d >= 4d-5 > 4d-6 >= deg(Q/t^2).

Polynomial interpolation gives Q=0, and operator injectivity gives P=0. All operators are applied only where both sides of the known finite interval exist. Some variable coefficients vanish at residue positions; none is divided by, and no recurrence propagation uses L_x.

## 5. Sparse endpoints and exact fixed divisors

If an envelope vector is supported on {0,1,m}, its scaled numerator is zero for j=2,...,m-1. Apply M=product_(r=0)^(d-2)(S-q^r), of order d-1. The chirp image has degree <=4d-8 and valuation at least two, so after division by t^2 its degree is <=4d-10. It is zero for j=2,...,m-d, exactly N-2d-1 points. The strict inequality needed is

    N-2d-1 > 4d-10, equivalently N>=6d-8,

which follows from the candidate hypothesis. Thus P=0. The remaining ordinary R has m-2>d-2 distinct zeros, so R=0. Therefore delta_0,delta_1,delta_m are jointly independent modulo E. The functionals c_0,c_1,c_m are independent on U; c_1 and c_m remain independent on U_0.

All following arguments also hold over an algebraic closure. A nonzero fixed root x of U_0 implies by linear duality that (x^j) lies in E+span(delta_0). It gives the scaled equality on j=1,...,m, and Section 4 forces P=0. Now the difference R(q^j)-x^jD(q^j) obeys the CONSTANT recurrence

    product_(r=0)^(d-2)(S-q^r)(S-xq^r),

of order 2d-2 with nonzero endpoint coefficients. Since m>=2d-2, its zero interval propagates both ways to all integers. Comparing j=0 and j=N gives x^N=1 because D(1)!=0. Write x=q^s, 0<=s<N. Then R(z)=z^sD(z) modulo z^N-1. The nonzero constant and degree-(d-2) coefficients of D force both s and s+d-2 modulo N into [0,d-2]. Since 2(d-2)<N, this implies s=0. Hence x=1.

If the derivative functional (j) lay in E+span(delta_0), Section 4 with L_1 would similarly force P=0. The remaining difference R(q^j)-jD(q^j) obeys M^2, also in characteristic two. Its 2d-2 order recurrence propagates the m known zeros. At j=0,N it would give 0=ND(1), contradicting char(k) not dividing N.

Sparse independence excludes 0 as a fixed root of U and makes 0 simple on U_0. Derivative exclusion makes the forced root 1 simple even on U_0. Thus

    gcd(U_0)=t(t-1), gcd(U)=t-1.

The new endpoint constraint has not introduced any additional fixed root or unavoidable multiplicity.

## 6. Legal-node guards and the SAME axis degeneration

For a positive-degree linear polynomial space V with gcd(V)=1, its universal polynomial sum_i Z_i f_i is irreducible over k(Z): a factor independent of the parameters would divide every f_i, and total parameter degree one forces such a factor in any factorization. Gauss's lemma applies.

For V_1=U/(t-1), the residual linear coefficient is -c_0-c_1, a nonzero functional by endpoint independence. Hence the universal derivative is nonzero even in characteristic two, and universal irreducibility gives separability. The derivative-at-1 exclusion also makes residual evaluation at 1 nonzero. Therefore degree m, nonzero constant, and squarefreeness are nonzero guards on U_1={g in U:c_m=1}.

For V_0=U_0/[t(t-1)], maximum degree r=m-2, the constant and leading functionals are -c_1 and c_m and are independent. A universal common factor of f and rev_r(f)=t^r f(1/t) would, by irreducibility and equal degrees, imply rev_r(f)=lambda f. Reversal twice gives lambda^2=1, hence lambda=+1 or -1 (only 1 in characteristic two). Comparing parameter coefficients would force a fixed reversal eigenspace, contradicting independent endpoints. The residual reciprocal resultant is therefore nonzero.

Over the algebraic closure choose f with nonzero endpoints and reciprocal-coprime, and normalize g_0=t(t-1)f to be monic. This is an auxiliary zero-constant specialization, never a physical bank. For monic g let p_a be the remainder coefficient vector of t^a mod g, 0<=a<N, and let X_N(g) have rows

    (p_a, 1, p_[-a]_N).

All entries are polynomial in g's coefficients, even at g(0)=0. A row dependence with A(t)=sum_(a=0)^(N-1)A_a t^a is exactly

    g divides A, A(1)=0, g divides J_N A,
    J_N A=t^N A(1/t)+A(0)(1-t^N).

At g_0, A(0)=0; the reversal condition implies rev_r(f) divides A. Reciprocal coprimality and nonzero endpoints ensure the needed coprime factors, including f(1)!=0. Hence t(t-1)f rev_r(f) divides A. Its degree is 2m-2>N-1 because N>2d+1, which follows from N>=6d-5,d>=4. Thus A=0 and rank X_N(g_0)=N.

Consequently one axis minor, the constant guard, and the discriminant are all nonzero polynomials on the SAME nonempty irreducible monic affine slice U_1. Their nonzero product gives a good g over any infinite k. This does not infer legal axis rank directly from reciprocal coprimality.

## 7. Finite coefficients and genuine splitting

The unchanged remainder degree bound gives an axis-minor degree <=d(d+1); the disjoint row ranges require N>2d, already satisfied. The total guard degree is at most

    H=d(d+1)+2m-1.

For k=F_Q containing q, Q>=N+1. Our hypotheses imply N>=19 and d<=(N+5)/6<=N/4. Thus

    H <= N^2/16+9N/4-1 < (N+1)^2/2 <= Q^2/2.

The elementary finite-grid zero bound proves a good coefficient point over E=F_(Q^2), with independent uniform affine sampling success probability greater than 1/2. Tests are exact: c_0!=0, gcd(g,g')=1, rank X_N(g)=N. All failed tests are charged; this is not a deterministic two-trial claim. Deterministic enumeration is also available.

The degree-two coefficient extension does NOT split g. Its actual distinct nonzero roots must be constructed in a genuine splitting extension of degree at most m! over the coefficient field, at most 2m! over F_Q. In finite fields the minimal degree is the lcm of irreducible factor degrees; the overfield F_(Q^(2m!)) suffices, with the explicit exhaustive construction and enumeration costs in the companion ledger. For arbitrary positive-characteristic k, construct over the finite subfield F_p(q) and take its compositum with k. Infinite-field existence is not a finite unpriced field algorithm.

## 8. Original-bank completion and full costs

The original whole-left reconstruction now applies without any new generator theorem. All its needed inequalities were checked: m>=(N-1)/2, b<=m, N>2d+1, and all supported Gaussian factors and physical nodes are nonzero.

For each positive b, solve the nonzero-node Vandermonde moments sum_i U_i x_i^a=v_b(a) on the left interval. For intervals longer than m the exact recurrence from U subset ker A propagates the solution; shorter intervals are padded. Use the -+ singleton amplitude T_b and the +- singleton amplitude zero. Recover -- amplitudes from moments

    sum_i V_i=f(0,b)-T_b-sum_i U_i,
    sum_i V_i x_i^r=(f(N-r,b)-T_b G_-+(N-r,b))/G_--(N-r,b),
                    1<=r<=b-1.

These cover the axis and right interval without changing the left interval. Reflection of both indices and signs fills negative b. For b=0 solve the full-row-rank matrix X_N(g), convert its two moment vectors by Vandermonde inversion, and assign its scalar column to a cross bank. Sector indexing is bijective, so assignments do not conflict.

The Fourier Weyl scalar is gamma=(1/N)sum_t q^(-t^2), nonzero in all allowed characteristics because the two Gauss sums multiply to N under the invertible residue substitution (s,t) -> (s-t,s+t). For each bank set

    beta=1, Delta=-alpha^N,
    w_j=gamma Delta sum_(ell=0)^(N-1)h_ell q^(-epsilon delta j ell).

Primitive-root quantum binomial cancellation gives X_j^N=(alpha^N+1)I for X_j=alpha S^epsilon+q^(epsilon delta j)T^delta, and hence the literal two-sided inverse (I+X_j+...+X_j^(N-1))/Delta. Character inversion matches every Fourier Weyl coefficient exactly. Both cross banks are effective; ineffective same-sign banks may be omitted. This proves the at-most 2m+2 ORIGINAL-bank count.

OPERATION_LEDGER.md rechecks the complete paid model at the new N,d range: field preparation, affine construction, failed candidates, genuine splitting and root recovery, amplitudes, all raw weights, inversions, storage, addressing, and every output coordinate. No root-free evaluator is proposed. Post-root preparation remains O(N^3) root-field arithmetic; the literal warm schedule remains cubic. Dense Fourier evaluation over the original field is already quadratic.

## 9. Structural mechanism limit and controls

Only a fixed number of constraints was restored: the t^2 valuation removes two polynomial degrees, and the inherited formal endpoint adds one known numerator zero. Neither number grows with d. The accepted operator still has order d+1 and the quotient chirp still has degree 4d+O(1), so this mechanism alone leaves the inequality N>=6d+O(1). It cannot improve the 5/3 leading bank constant without an additional d-dependent structural gain. No further slope search is claimed.

Fresh author controls are independently written from the definitions and never import or execute historical or accepted scientific programs. They check the refined envelope, original rows, formal endpoint, operator degree and valuation, sparse independence, exact gcds, derivative exclusion, all range margins, and sampled exact legal/axis witnesses over prime fields and characteristic-two extensions, including composite N. These finite checks are transcription controls, not the uniform proof and not physical splitting-field instantiations. Independent review remains required.
