# NF-03: an explicit all-even-length legal pencil family, with a paid but expensive preparation contract

Candidate, 11 October 2026. This document advances the existing NF-03 row; it is not a new fusion row. Independent review is pending.

## Result in one paragraph

For every even integer N=2h>=4, take q=exp(2*pi*i/N), m=h+1, the already accepted moment polynomials P_n below, and the **closed-form integer parameter**

    L = 10 N^3 + 2,       t_N = 2^L,
    B_N(z) = z P_h(z) + t_N P_(h-1)(z).

Every one of its m roots is nonzero and simple and avoids alpha^N=-1. Thus it gives the accepted at-most-h+1 legal common-Weyl Green representation, now with an actual parameter family and explicit separation, conditioning, precision and preparation bounds. The bounds are intentionally very conservative. In fact this family is provably badly conditioned: its unscaled moment Vandermonde has condition number at least exp(Omega(N^4)). A completely specified exhaustive certified root-preparation route has exponential bit cost, not a fast-FFT cost. This is an effective growing-length construction, not a useful growing-degree stability theorem or production implementation.

The exact h-pole optimum and the universal choice t=1 remain open. No claim of new general resultant, root-isolation, Prony, Vandermonde or chirp theory is made. No new external-priority conclusion is made.

## 1. Bound sources and target

The accepted P02 body, SHA-256 f6412a2cb78457a2fddd62a6e688095cb82528b4457ad1454dbbe069179937d6, Section B, proves the pencil construction and moment propagation. R16 explicitly accepts that body and restricts its conclusion to h<=Q<=h+1. Its saved algebra controls are retained as evidence, not replayed or relabeled as new tests here.

The accepted P05 body, SHA-256 02ec40df49f0585c57f98d3af7cbb9867216773f98a2998db9d51237fd69b787, Section S3, supplies the finite-separation Lagrange inverse envelope. R21 accepts its fixed-degree statement; the present estimates are proved below for this particular growing-length family and do not enlarge the old fixed-degree theorem by inference.

The earlier extension PROOF_OR_OBSTRUCTION.md, SHA-256 d6f5ac8d0cbd7f48cf928139dd60d275c79ad7b566d3c772795bb91d0d3a4861, fixes the same P_n/B_t conventions. The Phase 21 THEOREM.md defines the negative-sign normalized Fourier target. Exact copied-source hashes and the source-member location are in SOURCE_LEDGER.json. All inherited executable files were left inert.

Let omega=q^(-1), Z e_j=e_(j+1 mod N), D=diag(omega^j),

    T = D^(-1) Z,       Q = diag(q^(-j^2)),
    c_k = q^[k(k-1)/2],
    Fhat[i,j] = q^(-ij)/sqrt(N).

Then T is unitary, T^N=-I, and the accepted target identity is

    Fhat = (Q/sqrt(N)) C(T),     C(T)=sum_(k=0)^(N-1) c_k T^k.

The m columns below are first-order moment/pole coordinates. They are not Fourier coordinates and no basis application is free.

For numerical application it is convenient to use the signed cyclic shift S:

    S e_j=e_(j+1) for j<N-1,   S e_(N-1)=-e_0,
    E_L[j,j]=q^[-j(j-1)/2],    E_R[j,j]=q^[-j(j+1)/2].

Direct multiplication gives T=E_R^(-1) S E_R and E_L E_R=Q. Consequently

    Fhat = (1/sqrt(N)) E_L C(S) E_R.

This is exactly the same target and conjugate scalar bank. It uses two paid unit-modulus diagonal applications and the signed shift with rational entries. Indeed c_(r+N)=-c_r, so C(S)[i,j]=q^[(i-j)(i-j-1)/2], and the endpoint exponents reduce to -ij. The signs at the wrap are essential.

## 2. Accepted pencil facts reused

Define

    R_n(z)=prod_(k=0)^(n-1)(z-q^k)=sum_j r_(n,j) z^j,
    P_n(z)=sum_(j=0)^n q^[n(n-1)/2-j(j-1)/2] r_(n,j) z^j.

P_n is monic, lies in Z[q][z], and P_n(0)=(-1)^n q^[n(n-1)] has modulus one. For L_0(z^k)=c_k,

    L_0(z^s P_n)=0 (0<=s<n).

The accepted nonzero Hankel determinants imply gcd(zP_h,P_(h-1))=1. Put F=zP_h and G=P_(h-1). Then

    W=F'G-FG'

has degree 2h-1 and leading coefficient 2. Therefore Res_z(F+tG,F'+tG') is a nonzero polynomial in t. Also Res_z(F+tG,z^N+1) is nonzero: each of the N forbidden nodes excludes at most one t. These are algebraic statements over K=Q(q), not numerical experiments.

For a legal t, matching c_0,...,c_h in the m-node Vandermonde propagates all N moments by the order-m recurrence. This previously accepted part is not reproved as a new result.

## 3. A closed-form legal parameter: coefficient height and a norm

For every embedding sigma:K->C, sigma(q) is a primitive Nth root on the unit circle. Coefficient l1 norms in z obey

    ||sigma(P_n)||_1 <= 2^n.

This follows by expanding R_n as a product of n unit-root linear factors; the coefficient phases defining P_n have modulus one. The same argument in the bivariate (z,t) coefficient norm gives

    ||sigma(B_t)||_1 <= 2^h + 2^(h-1) <= 2^N,
    ||sigma(partial_z B_t)||_1 <= m 2^N <= N 2^N.

Set

    A(t)=Res_z(B_t,partial_z B_t) Res_z(B_t,z^N+1).

It is nonzero and belongs to Z[q][t]. The two Sylvester matrices have sizes s_1=2m-1=N+1 and s_2=m+N, both at most 2N. Each entry's t-coefficient l1 norm is at most N 2^N. Expanding determinants and using the submultiplicative coefficient l1 norm,

    ||sigma(A)||_1
       <= s_1! s_2! (N 2^N)^(s_1+s_2)
       <= (2N)^(4N) (N 2^N)^(4N)
       <= 2^(9N^2) <= 2^(10N^2).

The penultimate inequality uses log2(N)<=N/2 for N>=4.

Let d=[K:Q]=phi(N)<=N and take the coefficientwise field norm

    H(t)=prod_sigma sigma(A(t)).

It is a nonzero polynomial in Z[t]: the product is Galois-fixed and its coefficients are algebraic integers. Its coefficient l1 norm is at most 2^(10N^3). Its leading coefficient is a nonzero integer, of absolute value at least one. The elementary Cauchy root bound therefore places every zero of H in

    |t| <= 1 + 2^(10N^3).

For completeness, if |u|>1+max_(j<e)|a_j/a_e| for a polynomial of degree e, the leading term exceeds the sum of all lower terms, by summing the geometric series; hence u is not a root. A nonzero constant H presents no exception.

Our t_N=2^(10N^3+2) is outside this disk. Hence both resultants at t_N are nonzero. Finally B_N(0)=t_N P_(h-1)(0)!=0. Thus B_N has m distinct nonzero legal roots for every even N>=4. This proof does not compute or search for bad parameters and does not assume t=1 works.

## 4. Explicit uniform bounds for this family

Use the following positive dyadic constants (the deliberately weaker integer exponents simplify certification):

    R     = 2^(L+N+1),
    delta = (2R)^[-N m(m-1)],
    eta   = (2 R^N)^[-Nm],
    rho   = eta (2R)^[-(N-1)],
    K_V   = m (2R/delta)^(m-1),
    W_b   = m K_V,
    G_b   = 2 W_b R^N.

Their binary exponent descriptions have polynomial length. For every root alpha_i,

    R^[-(m-1)] <= |alpha_i| <= R,
    |alpha_i-alpha_j| >= delta  (i!=j),
    |1+alpha_i^N| >= eta,
    dist(alpha_i,{z:z^N=-1}) >= rho.

Proof of the root radius: every conjugate B_N has coefficient l1 norm at most 2^h+t_N 2^(h-1) <= 2^(L+N). Cauchy's bound gives R. Its constant has absolute value t_N, so the product of the m root moduli is t_N; removing the other factors gives the lower radius bound.

Proof of separation: the nonzero discriminant D_B is a cyclotomic algebraic integer. At every embedding it has modulus at most

    M_D=(2R)^[m(m-1)],

from its root-difference product. Its nonzero integer field norm gives |D_B|>=M_D^[-(d-1)]>=M_D^[-(N-1)]. Isolate one squared root difference in that product and bound all remaining factors by 2R. This gives the stronger bound

    |alpha_i-alpha_j| >= (2R)^[-N m(m-1)/2+1],

which implies delta. This use of a norm depends on the uniform bounds over ALL embeddings, supplied above.

Proof of the nonpole margin: J=Res_z(B_N,z^N+1) is nonzero integral, and every conjugate has modulus at most (2R^N)^m. The same norm argument, followed by removal of the other m-1 factors, gives

    |1+alpha_i^N| >= (2R^N)^[-(Nm-1)] >= eta.

Factor alpha_i^N+1 over the N unit-modulus forbidden nodes. Every other distance is at most R+1<=2R, giving rho.

For V[k,i]=alpha_i^k, 0<=k<m, Lagrange interpolation gives

    ||V^(-1)||_2 <= sqrt(m) (1+R)^(m-1) delta^[-(m-1)] <= K_V,
    ||V||_2 <= m R^(m-1),
    kappa_2(V) <= m R^(m-1) K_V.

The inverse estimate follows by bounding each Lagrange numerator's coefficient l1 norm by (1+R)^(m-1), each denominator by delta^(m-1), and the inverse Frobenius norm by sqrt(m) times that bound. No SVD or condition-number oracle is used.

Let beta solve V beta=(c_0,...,c_(m-1)). Then

    ||beta||_2 <= K_V sqrt(m) <= W_b,
    gamma_i=beta_i(1+alpha_i^N),   |gamma_i|<=G_b.

The exact bank identity is

    C(T)=sum_i gamma_i (I-alpha_i T)^(-1).

All m denominators are legal. Zero gamma_i can simply be retained or omitted; deciding which weights are exactly zero is not required for the at-most-m representation. The accepted Hankel rank still ensures at least h nonzero weights.

For either unitary shift T or S,

    ||(I-alpha_i T)^(-1)||_2 <= rho^(-1),
    kappa_2(I-alpha_i T) <= (1+R)/rho.

Indeed their spectra are exactly the N roots of -1, and the smallest singular value of I-alpha_i T is min_tau |1-alpha_i tau|=dist(alpha_i,E), because E is closed under inversion.

The logarithms of R, delta^(-1), rho^(-1), K_V and G_b are respectively O(N^3), O(N^6), O(N^6), O(N^7) and O(N^7). These are uniform upper bounds, not polynomial condition-number bounds.

## 5. This particular explicit family is necessarily poorly conditioned

The coefficient of z^(m-2)=z^(h-1) in B_N is t_N plus a coefficient of P_h of absolute value at most 2^h. If M=max_i |alpha_i|, the elementary symmetric coefficient bound yields

    M^2 >= (t_N-2^h)/binom(m,2).

The final row of V contains alpha_i^(m-1), so ||V||_2>=M^(m-1). Also sigma_min(V)<=||V^T e_0||_2=sqrt(m); transposition preserves the singular values even for complex matrices. Consequently

    kappa_2(V) >= [ (t_N-2^h)/binom(m,2) ]^[(m-1)/2] / sqrt(m)
               = exp(Omega(N^4)).

This is an actual obstruction to claiming this large-t family as a well-conditioned pole-coordinate implementation. It is not a lower bound on Fourier computation or on every possible legal node family. Cancellations can keep the final normalized target unitary even while this representation is ill-conditioned.

## 6. Certified preparation: explicit exhaustive route and its cost

The following route is deliberately elementary. It establishes an effective preparation bound without assuming a free root finder, root oracle, exact complex arithmetic or unproved precision behavior. It is not proposed as an efficient implementation and its enormous grid was not run in the controls.

### 6.1 Root disks to arbitrary requested accuracy

Given a requested integer p>=1, put M_2=2^ceil(log2 m),

    A_0=(4R)^m,       d_0=delta^(m-1),
    r=min(2^(-p-2), delta/8, d_0/(16 M_2 A_0)),
    s=d_0 r/(64 M_2 A_0).

All are explicit dyadics. Enumerate the grid centers w in s(Z+iZ) with |Re(w)|,|Im(w)|<=R+1. At each center form the exact Taylor coefficients a_k=B_N^(k)(w)/k! using certified coefficient approximations, and test with outward bounds the strict inequality

    |a_0| + sum_(k=2)^m |a_k| r^k < |a_1| r.                 (RD)

Rouche's theorem comparing the polynomial with a_1(z-w) certifies exactly one root in that disk. Keep a certified disk unless it intersects an already kept disk. Stop after m pairwise disjoint certified disks. Every accepted disk has radius r and thus defines one exact algebraic root without claiming an explicit radical formula.

Here is a uniform termination and precision proof. Near a true root alpha, choose the nearest grid point w. Its distance is at most s. Since |alpha|<=R, the center belongs to the enumerated square. At alpha, |B'_N(alpha)|>=d_0. For every enumerated center, |w|<=2R; the product formula bounds the sum of absolute Taylor coefficients by (1+|w|+R)^m<=A_0. The same bound holds for Taylor coefficients at a root. For e=|w-alpha|<=s<=1,

    |B_N(w)|<=A_0 e,
    |B'_N(w)-B'_N(alpha)|<=m A_0 e,
    sum_(k>=2)|a_k|r^k<=A_0 r^2.

The definitions imply |a_1|>=d_0/2, |a_0|<=d_0 r/64 and the higher-order sum is at most d_0 r/16. Thus the true inequality (RD) has positive margin at least d_0 r/4. The constants retain ample slack.

Compute the entire coefficient vector of B_N with l1 error at most

    theta = d_0 r/(1024 M_2 A_0).

Its Taylor vector at any center has l1 error at most theta (1+|w|)^m<=theta A_0. Bound each modulus by rational upper/lower bounds of width at most

    zeta = d_0 r/(1024 M_2).

The error in both sides of (RD) together is less than d_0 r/16. Therefore every nearest-root grid point is certified at this single prescribed precision. An inconclusive center is rejected; it is never refined indefinitely. Certificates may include other centers too, but any certified disk contains one root. Two disks for distinct roots cannot intersect because delta>4r. Thus greedy nonintersection cannot discard every disk for any root, and the procedure ends with m disks.

A coefficient construction achieving theta is also explicit. As a polynomial in q, each P_n coefficient has degree at most n(n-1)<=N^2 and total bivariate integer coefficient l1 norm at most 2^n. For |qhat-q|=u<=N^(-2), the telescoping power identity bounds the l1 error in B_N by

    3N^2 u (2^h+t_N 2^(h-1)) <= 4N^2 R u.

It therefore suffices to obtain a dyadic qhat with certified error <=min(N^(-2),theta/(8N^2 R)), and perform the polynomial construction in exact rational arithmetic. This preparation includes constructing the product polynomials and multiplying their coefficient phases, rather than assuming them supplied.

For a completely elementary source of qhat, use Machin's identity pi=16 arctan(1/5)-4 arctan(1/239), the alternating arctangent series with its next-term error, and sine/cosine Taylor series at 2pi/N with factorial remainder. O(b_q+1) terms suffice for b_q requested bits, with explicit rational remainder bounds. Round the final interval to a dyadic center only when its radius is within the required tolerance. Rational square roots for modulus bounds use bisection and exact squared comparisons. These are terminating arithmetic procedures; no library floating-point error claim is substituted.

The square contains at most

    G_grid = (8R/s)^2

grid centers (an upper bound, not the exact count). Polynomial formation needs O(N^2) rational arithmetic operations, with exponentiation of the phase factors also paid. Each center needs O(m^2) rational operations for the Taylor shift, plus the modulus-bisection work. log2(1/s)=p+O(N^7) as an upper bound. The complete node-preparation cost is

    2^[O(p+N^7)] bit operations,

with polynomial working storage when the grid is streamed and only accepted disks are retained. This bound includes construction of q, B_N, the grid addresses, the rejection tests, and all output disks. A safe explicit form is

    O((1+G_grid) S_0^20) bit operations,
    O(S_0^10) bits of working storage,
    S_0 = 2+N+p+ceil(log2 R)+ceil(log2(1/s)).

To verify the deliberately loose polynomial factor, exact truncated elementary series use O(S_0) terms with rational bit lengths O(S_0^3); rounding qhat to a dyadic prevents those series denominators from propagating. The q-polynomial exponents are at most N^2, and the Taylor shift has degree m, so its rational operands have O(S_0^5) bits. Schoolbook arithmetic and O(S_0^5) exact bisection steps are bounded by S_0^20 per center. Counter and disk storage fit the stated storage bound. No fast-arithmetic theorem is needed.

### 6.2 Weights and residues, including their precision

The root disks label roots consistently. For approximate centers alpha_tilde, let their maximum error be e<=1. Define

    H_V=m^2 (2R)^(m-1).

The telescoping power formula gives ||V_tilde-V||_2<=H_V e. If e<=1/(4 K_V H_V), then ||V_tilde^(-1)||_2<=2K_V by the geometric-series inverse identity. If each moment approximation has error at most u_c, solve the rational Vandermonde system exactly. The resulting beta_tilde satisfies

    ||beta_tilde-beta||_2 <= 2 K_V [m u_c + H_V e W_b].       (BW)

Thus to achieve a requested beta-error v_b>0, it is sufficient to set

    u_c <= v_b/(8m K_V),
    e <= min(1/(4K_V H_V), v_b/(8K_V H_V W_b)).

The right side of (BW) is then at most v_b/2; the other half can pay dyadic output rounding. Moment phases are prepared by the same certified q/Taylor route, with their maximum exponents O(N^2) paid.

For gamma=beta(1+alpha^N), exact rational formation from approximate roots and weights gives

    |gamma_tilde-gamma|
       <= 2(2R)^N v_b + W_b N(2R)^(N-1) e.

To achieve a residue error v_g, it suffices to use

    v_b <= v_g/[8(2R)^N],
    e <= v_g/[4 W_b N(2R)^(N-1)],

again retaining slack for final dyadic rounding. All required root, moment, weight and residue precisions are p+O(N^7) bits for target absolute error 2^(-p). Substituting that root accuracy into the grid bound still gives 2^[O(p+N^7)] bit preparation.

Exact rational Gaussian elimination with pivoting costs O(m^3) rational operations. Its numerators and denominators are bounded by minors of the input dyadic matrix; expansion of an m-by-m determinant gives at most m! products, proving polynomial bit sizes in m and the supplied precision. Fraction-free or reduced-fraction elimination keeps that bound. No claim is made for unpivoted floating-point elimination. Recovering algebraic radicals or deciding zero residues is not required.

## 7. Paid application and a conservative finite-precision contract

Let eps=2^(-p), p>=1. Suppose every root is approximated with error e and every residue with error v_g, where

    e <= min(rho/2, eps rho^2/(16m G_b)),
    v_g <= eps rho/(16m).

Then the perturbed denominators are legal and

    ||(I-alpha_tilde S)^(-1)||_2 <= 2/rho,
    ||(I-alpha_tilde S)^(-1)-(I-alpha S)^(-1)||_2 <= 2e/rho^2.

The first statement follows from the distance margin, and the second from the resolvent identity. Therefore the exact rational approximate bank satisfies

    ||C_tilde(S)-C(S)||_2
       <= m(2v_g/rho + 2G_b e/rho^2) <= eps/4.             (AB)

Combine these tolerances with Section 6.2 by taking the minimum; the required scalar precision is still p+O(N^7), and the full preparation remains exponential.

Each approximate resolvent is applied with a paid O(N) first-order recurrence. For y=(I-aS)^(-1)x, compute

    b=sum_(k=1)^(N-1) a^(N-1-k) x_k,
    y_0=(x_0-a b)/(1+a^N),
    y_i=a y_(i-1)+x_i  (1<=i<N).

Horner evaluation computes b and a^N in O(N) work. Do this for all m branches and sum their weighted outputs: O(Nm)=O(N^2) rational operations and O(N+m) scalar working registers if the branches are streamed. The root-to-weight solve and all m root/residue preparations are separate setup costs. Nothing here applies m dense basis columns for free.

For a fully digital output statement, let the input real/imaginary components be dyadic rationals whose numerators and denominators have at most b bits. Handle the zero vector separately. Approximate each endpoint phase and 1/sqrt(N) with absolute error at most a_0=eps/(64N), and evaluate the endpoints, the approximate bank, and normalization in exact rational arithmetic. The exact C(S) has norm sqrt(N) by the Fourier identity and unitary endpoints; (AB) gives ||C_tilde||<=sqrt(N)+eps/4<=2N. With approximate diagonal norms <=2 and approximate normalizer <=2, expansion of the two endpoint errors and the normalizer error adds at most 16N a_0<=eps/4. Adding (AB) after exact endpoint/normalizer scaling gives total operator error at most eps/2 before output rounding.

Finally round each real/imaginary output component to absolute error at most eps*2^(-b)/(16N). A nonzero input has ||x||_2>=2^(-b); the rounding contribution is at most eps||x||_2/8. Hence the full error is <eps||x||_2. All scalar tolerances are constructive, and the preceding slack pays separate dyadic rounding of prepared constants. The endpoint phases and square root are generated by the same rational-series/bisection methods, not taken as exact machine constants.

Exact dyadic-to-rational recurrence evaluation avoids an unproved floating-point accumulation model. Its numerators and denominators, including the sum over m different branch denominators, have O(N^2(p+b+N^7)) bits: a branch denominator 1+a^N has O(N) times its input bit length, and multiplying at most m branch denominators pays another factor m. Reading x and writing all N results are included. Schoolbook arithmetic gives the conservative application bound

    O(N^6 (p+b+N^7)^2) bit operations,

plus the already charged preparation. This is a mathematical implementation contract, not a benchmark or certification of a production program. Storing the exact rational running output needs polynomial bits; no O(N) fixed-word memory assertion is made.

## 8. Evidence and exact remaining scope

Fresh controls in this packet test only the new ingredients: the closed-form parameter, exact modular legal guards and all moment recurrences, the signed-shift endpoint target identity, small exact cyclotomic resultant-norm coefficient bounds, and the explicit Rouché-grid validator on small rational control polynomials with positive and negative cases. They do not rerun inherited source suites. Finite tests are not the proof for all N.

This candidate supplies a closed-form legal growing-length family with proven uniform but extremely poor envelopes and an explicit expensive certified preparation route. It does not supply a useful low-condition family, a polynomial-time pole-preparation algorithm, a production executor, an h-pole optimum, a universal t=1 theorem, or a subquadratic Fourier application. Those distinctions must remain visible in NF-03 and Q20/Q08.

Proposed row action after independent review: accept only this effective large-parameter construction as a scoped NF-03 result; retain the useful-conditioning and practical-preparation continuation as open. Do not label all NF-03 construction goals or all growing-degree stability work complete.
