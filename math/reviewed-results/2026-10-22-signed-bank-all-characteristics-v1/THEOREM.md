# Uniform signed-bank construction in every admissible characteristic

22 October 2026. Author candidate, not independently accepted. No external publication or research-table change is authorized by this file. Exact source identities are in SOURCE_PINS.json; original source files are preserved unchanged.

## 1. Contract, result, and contribution boundary

Let N be odd, d>=4, N>=8d-10, and m=N-d. Let k be a field containing a primitive Nth root q, with char(k) not dividing N. In characteristic zero the theorem below is already accepted by the pinned 10 October source. The candidate contribution is its extension to every allowed positive characteristic, including characteristic two, together with a finite-field coefficient-descent bound and an explicit, expensive, finite construction ledger.

Use the original generators S e_t=e_(t+1), T e_t=q^t e_t, with indices modulo N, and the negative unnormalized target F[k,t]=q^(-kt). A counted physical bank is exactly

    B_(epsilon,delta)(alpha,beta;w)
      = (1/N) sum_(j=0)^(N-1) w_j
        (I-alpha S^epsilon-beta q^(epsilon delta j) T^delta)^(-1),
    Delta=1-alpha^N-beta^N != 0.

The orientation labels epsilon,delta are integer signs specifying powers; in characteristic two the four generators do not collapse, because S^-1 is not S and T^-1 is not T for odd N>=23. Raw weights are arbitrary field elements, including zero. There is no positivity condition or requirement that every raw branch weight be nonzero. The construction uses nonzero alpha and beta=1, so every branch denominator is -alpha^N != 0. No derivative node, zero-node bank, singular limit, new generator, external endpoint map, product of banks, or trace-bank primitive is admitted.

THEOREM. There is a monic polynomial g in a finite algebraic extension of k, of degree m, with m distinct nonzero roots, such that F is a sum of at most 2m+2 original banks. The same-sign orientations use the roots of g, and each cross orientation has exactly one effective node, chosen to be alpha=1. Equality of these chosen cross nodes is a legal witness choice, not a new restriction on the larger independently-free-cross-singleton grammar.

If k is infinite, g may be chosen in k[t]. If k=F_Q is finite, g may be chosen in F_(Q^2)[t]. The genuine splitting field of g over its coefficient field has degree at most m!, so all bank parameters and weights lie in an extension of F_Q of degree at most 2m!. More precisely the finite-field splitting degree is the least common multiple of the irreducible factor degrees; no polynomial bound on that degree is asserted. A deterministic construction can instead use the overfield F_(Q^(2m!)), without assuming a factorization oracle. The latter is an explicit overfield, not a claim that the actual splitting field has that full degree.

Taking d=floor((N+10)/8), every odd N>=23 therefore has the bound

    2N-2floor((N+10)/8)+2 = 7N/4+O(1)

in every characteristic not dividing N, over the stated extension. There is no assertion of base-field attainment, minimality, a smaller leading bank constant, fast preparation, FFT speedup, numerical stability, or historical novelty. This does not reopen the completed N=13 extension-degree classification and does not close the broader owners M-MAGNETIC-SPAN, NEW-17, or Q35.

The new proof step is not a new Vandermonde or generic-polynomial theorem. It identifies an existing sparse-functional exclusion as the missing separability certificate in positive characteristic, then bounds the simultaneous guard degree to make descent finite and quantitative. The characteristic-zero construction and its classical ingredients remain attributed to the pinned accepted source.

## 2. Original coefficients and the whole-left recurrence

All fractions in exponents below mean inverses modulo the odd integer N. They do not mean division by 2 or 4 in k. Put e=2^-1 mod N, h=4^-1 mod N, rho=q^e, and C_j=q^(h j^2). Then rho is primitive and rho^2=q.

For local nonnegative residues r=[epsilon a]_N and ell=[delta b]_N, let

    G_(epsilon,delta)(a,b)=[r+ell choose ell]_(q^(epsilon delta))

when r+ell<N, and zero otherwise. Every displayed Gaussian coefficient in the supported triangle is nonzero: its product formula has only factors 1-q^j with 0<j<N. The Weyl coefficients of the target are gamma f(a,b), where

    f(a,b)=q^(h(a+b)^2),
    gamma=(1/N) sum_t q^(-t^2) != 0.

For completeness, extracting the coefficient of S^a T^b by (1/N) sum_t q^(-bt) F[t+a,t] and completing the square gives this formula. If G_+ and G_- are the sums with exponents +t^2 and -t^2, then G_+G_-=N: substitute u=s-t,v=s+t and use root orthogonality. The substitution is invertible modulo N even in characteristic two of the coefficient field. Thus gamma is nonzero since N is invertible in k.

For b=1,...,(N-1)/2 define

    T_b=1/G_-+(N-b,b),
    v_b(j)=(f(j,b)-T_b G_-+(j,b))/G_++(j,b),
             1<=j<=N-b-1.

All denominators are nonzero. Let A_(N,m) have rows (v_b(a+j))_(j=0)^m for a,b>=1 and a+b<=d-1. These are precisely all recurrence windows of length m+1 in the whole-left sequences. If g(t)=sum_(j=0)^m c_j t^j with c_m=1 lies in ker A, all these sequences obey its recurrence.

Define

    D(z)=product_(j=2)^(d-1)(1-q^j z),
    E={((C_j P(rho^j)+R(q^j))/D(q^j))_(j=0)^m:
         deg P<=3d-7, deg R<=d-2},
    U=E^perp,  U_0={g in U:c_0=0}.

The pairing is ordinary coefficient pairing, without conjugation. Every D(q^j) is nonzero since 2<=j+index<=N-1. There are at most 4d-7 envelope generators, hence dim U>=N-5d+8>=3d-2.

Here is the algebra proving U is in ker A without a rank-saturation assumption. For s=a+b, put

    Q_b=product_(j=1)^b(1-q^j),
    F_(a,b)(z)=D(z)/product_(j=1)^b(1-q^(a+j)z),
    R_(a,b)(z)=product_(j=1)^b(1-q^(a-j)z),
    B_b=T_b (-1)^b q^(b(b+1)/2).

The quotient F is a polynomial. Gaussian products, including zero-support values, give

    D(q^j)v_b(a+j)
      =Q_b q^(h s^2) C_j rho^(s j) F_(a,b)(q^j)
       -B_b R_(a,b)(q^j)F_(a,b)(q^j).

Its chirp polynomial in rho^j has degree s+2(d-2-b)<=3d-7; its ordinary polynomial has degree d-2. Thus each actual recurrence row belongs to E. The formula is a polynomial/product identity valid in every allowed characteristic, not a characteristic-zero lift. Where the cross triangle is absent, R_(a,b)(q^j) has a zero factor, so the same identity still applies.

Also P=0,R=D gives the all-ones functional in E, and consequently every g in U vanishes at 1.

## 3. Sparse functionals and fixed divisors over an arbitrary characteristic

Work over an algebraic closure when choosing points. Put M=product_(j=0)^(d-2)(S-q^j), where S is the forward shift on sequences. The identity C_(j+1)=q^h rho^j C_j shows that a factor S-lambda sends a chirp polynomial P(t) to

    q^h t P(rho t)-lambda P(t).

For every nonzero P this increases degree by exactly one and is injective, in every characteristic. M kills any ordinary sequence R(q^j) of degree <=d-2.

If a vector of E is supported on {0,1,m}, its scaled sequence C_jP(rho^j)+R(q^j) vanishes for j=2,...,m-1. After M, a chirp polynomial of degree at most 4d-8 vanishes at N-2d-1 distinct rho-points. The inequality N>=8d-10,d>=4 implies N-2d-1>4d-8 and 4d-8<N. Therefore this polynomial is zero, injectivity gives P=0, and the original interval then forces R=0. Thus

    delta_0, delta_1, delta_m are independent modulo E.

Equivalently the coefficient functionals c_0,c_1,c_m are independent on U. On U_0 the functionals c_1,c_m remain independent. These statements include joint independence, not merely individual nonvanishing.

Suppose x!=0 is fixed as a root of every member of U_0. Evaluation at x belongs to E+span(delta_0), so a scaled envelope agrees with x^jD(q^j) for j=1,...,m. Put L_x=product_(j=0)^(d-2)(S-xq^j). Applying ML_x leaves a chirp polynomial of degree at most 5d-9 with N-3d+2 distinct zeros. The latter count is larger because N-8d+11>=1. Thus P=0.

The difference R(q^j)-x^jD(q^j) obeys the monic recurrence ML_x, of order 2d-2 and nonzero constant coefficient. Its known consecutive zero interval has length m>=2d-2, so it propagates both forwards and backwards. At j=0,N, and since D(1)!=0, this yields x^N=1. Write x=q^s. The polynomial identity on the N roots identifies R(z) with z^sD(z) modulo z^N-1. The nonzero constant and leading coefficients of D force s and (s+d-2) mod N into [0,d-2]. Since 2(d-2)<N, this gives s=0, hence x=1.

Finally the derivative-at-1 functional (j)_(j=0)^m does not belong to E+span(delta_0). Otherwise the scaled envelope equals jD(q^j) on j=1,...,m. Apply M^2; it kills jD(q^j) in every characteristic, including two. The same degree and zero count force P=0. Recurrence propagation to 0 and N then gives R(1)=0=ND(1), impossible because char(k) does not divide N. The source's use of characteristic zero in this step was stronger than necessary.

We have proved, over the algebraic closure as well,

    gcd(U_0)=t(t-1),   gcd(U)=t-1.

The sparse-functional exclusion makes the root 0 simple in gcd(U_0); the derivative exclusion makes the root 1 simple. No derivative at an arbitrary moving root has been presumed.

## 4. The missing positive-characteristic separability certificate

For any polynomial space V with gcd(V)=1 and positive maximum degree, its universal polynomial H(Z,t)=sum_i Z_i h_i(t), for a basis h_i, is irreducible in k(Z)[t]. Indeed a factorization in k[t,Z] has total Z-degree one, so one factor lies in k[t] and divides every h_i; it is a unit. Nonunit content over k[Z] would also factor H, so Gauss's lemma gives the assertion over k(Z).

Apply this to V_1={g/(t-1):g in U}. Its gcd is one by Section 3. Write g=(t-1)h. Direct coefficient comparison gives

    h_0=-c_0(g),    h_1=-c_0(g)-c_1(g).

The second is a nonzero functional on U, because delta_0+delta_1 is a nonzero vector supported on {0,1,m} and cannot belong to E. This remains true in characteristic two. Hence the coefficient of t in the universal residual H is not the zero parameter polynomial, and H' is nonzero. Irreducibility then implies gcd(H,H')=1. Thus the generic residual is separable in every characteristic.

This argument does NOT say that a nonzero linear coefficient makes every polynomial squarefree. Irreducibility over the rational parameter field is essential. Specializations may be inseparable or have repeated roots and are rejected by the discriminant test.

The derivative-at-1 exclusion from Section 3 also makes h(1)=g'(1) nonzero generically. Therefore generic g=(t-1)h has degree m, is squarefree, and has nonzero constant. These are nonzero polynomial guards on the same monic affine slice of U, not assertions about arbitrary kernel vectors.

## 5. Full axis rank, including characteristic two

Let V_0={g/[t(t-1)]:g in U_0}, of maximum degree r=m-2. Its gcd is one. Its endpoint functionals are f(0)=-c_1(g) and leading_r(f)=c_m(g), which are independent.

For the universal polynomial f in V_0, let rev_r f=t^r f(1/t). Both its degree and constant are nonzero generically. If f and rev_r f had a common factor, irreducibility gives rev_r f=lambda f. Reversing again gives lambda^2=1. In a field this means lambda=1 or -1, with just lambda=1 in characteristic two. In either case comparison of the independent parameters would put the whole space in one fixed reversal eigenspace, contradicting endpoint independence. Thus the reciprocal resultant is a nonzero polynomial.

Over the infinite algebraic closure choose such an f with nonzero endpoints and normalize g_0=t(t-1)f to be monic. The point g_0 is only an auxiliary polynomial with a zero root; it is not assigned a bank.

For any monic g of degree m define p_a to be the coefficient vector of t^a mod g, for 0<=a<N. Define the N by (2m+1) axis matrix X_N(g), row a, by

    (p_a, 1, p_[-a]_N).

It is defined polynomially even when g(0)=0. A row-dependence polynomial A(t)=sum_(a=0)^(N-1) A_a t^a satisfies exactly

    g divides A,    A(1)=0,    g divides J_N A,
    J_N A=t^N A(1/t)+A(0)(1-t^N).

At g_0, A(0)=0. Reversing the f divisibility in J_N A yields rev_r(f) dividing A. Reciprocal coprimality and nonzero endpoints show that

    t(t-1)f rev_r(f) divides A.

Its degree 2m-2 exceeds N-1, so A=0 and rank X_N(g_0)=N. This proof does not divide by two, use an inverse of t modulo g_0, or assume f squarefree. Therefore one N-column axis minor is a nonzero polynomial on the monic slice U_1={g in U:c_m=1}.

The slice is a nonempty affine linear space. The constant, discriminant, and this axis minor are nonzero polynomials on it, by Sections 3-5. Their product is nonzero in its integral coordinate ring. Over infinite k this gives a k-point satisfying every guard. Over finite k the following quantitative argument supplies an extension-valued point.

## 6. Quantitative finite-field descent

Parametrize U_1 by s=dim U-1 affine coordinates over k. Affine substitution does not increase polynomial degree. The coefficients of p_j=t^j mod g have total degree at most max(0,j-m+1) in the nonleading coefficients of g: this follows by multiplying a remainder by t and replacing t^m by -sum_(i<m)c_i t^i.

In X_N(g), row 0 is constant. The only possibly nonconstant rows are a=1,...,d, from p_(N-a), and a=m,...,N-1, from p_a. These sets are disjoint. Their row-degree maxima are respectively d,d-1,...,1 and 1,2,...,d. Hence every N-column determinant has degree at most

    d(d+1).

The monic degree-m discriminant has total degree at most 2m-2 in every characteristic, since it is the specialization of the integer discriminant polynomial. In characteristic two it may be a square, but its nonvanishing still means squarefreeness. Thus the nonzero simultaneous guard product has total degree at most

    H=d(d+1)+2m-1.

A nonzero polynomial of total degree H has at most H R^(s-1) zeros on F_R^s. An induction on s, separating the leading coefficient in the last variable and using the univariate root bound, proves this elementary estimate. Therefore R>H ensures a good point. Equivalently any grid of H+1 distinct scalars in each coordinate suffices.

If k=F_Q contains a primitive Nth root, N divides Q-1, so Q>=N+1. Here d<=(N+10)/8<=N/4, m<=N and N>=23; consequently

    H <= N^2/16+9N/4-1 < (N+1)^2/2 <= Q^2/2.

The strict middle inequality follows because 7N^2/16-5N/4+3/2>0 for N>=23. Thus F_(Q^2) always suffices and a uniform random affine point there succeeds with probability greater than one half. The test is exact: c_0!=0, gcd(g,g')=1, and rank X_N(g)=N. It does not need to know in advance which axis minor is the nonzero one. The failure set is contained in the zero set of the chosen theoretical guard product.

This is a Las Vegas option with expected fewer than two tested candidates once the field and affine slice are prepared. A deterministic enumeration of all Q^(2s) points is also guaranteed to terminate. Neither statement includes free root finding or free field preparation.

For an arbitrary positive-characteristic k containing q, its subfield F_p(q) is finite. Applying this construction there and taking its compositum with k gives the same degree-at-most-2m! algebraic-extension statement. It does not assert that k itself contains the required coefficient or splitting extension.

## 7. Completion to actual original banks

Let g be a good polynomial and x_1,...,x_m its actual distinct nonzero roots in a splitting field L. Since U is contained in ker A, for each positive b choose ++ amplitudes U_i satisfying

    sum_i U_i x_i^a=v_b(a),  1<=a<=N-b-1.

If the interval length is at least m, solve the first m equations by nonzero-node Vandermonde inversion and propagate using the monic recurrence. If it is shorter, pad the specified consecutive moments to m values and solve. Set the -+ singleton amplitude to T_b and the +- singleton amplitude to zero. Choose -- amplitudes V_i to match

    sum_i V_i=f(0,b)-T_b-sum_i U_i,
    sum_i V_i x_i^r=(f(N-r,b)-T_bG_-+(N-r,b))/G_--(N-r,b),
                 1<=r<=b-1.

Here b<=m. Padding these b moments to m values gives another ordinary Vandermonde solve. These -- sectors touch only a=0 and the right interval a=N-b+1,...,N-1. The ++ group handles a=1,...,N-b-1, and the forced singleton handles a=N-b, so all N coordinates are matched without conflicts. Every divided Gaussian factor is nonzero on its stated triangle.

Reflect both physical indices and both signs to handle negative b. The Gaussian factors and f obey the needed identities as powers and products, in every characteristic. The sector map b to [delta b]_N is a bijection for each orientation, so positive and negative row assignments use different free amplitudes.

For b=0 solve X_N(g) against f(a,0), using its full row rank. Convert its two length-m moment vectors to root amplitudes by the same Vandermonde matrix; allocate its scalar column to one cross bank and zero to the other's axis sector. This covers every original Weyl coefficient, not just necessary recurrence windows.

For a bank with normalized sector amplitudes h_ell set

    w_j=gamma Delta sum_(ell=0)^(N-1) h_ell q^(-epsilon delta j ell),
    beta=1,  Delta=-alpha^N.

The finite character inversion is legal since N is invertible. Let X_j=alpha S^epsilon+q^(epsilon delta j)T^delta. The root-of-unity quantum-binomial identity gives X_j^N=(alpha^N+1)I, so the two-sided literal inverse is (I+X_j+...+X_j^(N-1))/Delta. Expanding it and applying the weights produces exactly gamma times the normalized coefficients just matched. Thus the original bank sum equals the literal negative unnormalized Fourier matrix.

Both cross banks are effective because their forced positive/reflected sectors are nonzero at exclusive coordinates. Any ineffective same-sign bank may be omitted, hence the statement is at most 2m+2, not a false assertion that every listed same-sign node must be active. The resulting field-valued identity is exact; it involves no numerical approximation or sampling of input vectors.

## 8. What this proves and what remains

The theorem is uniform in all odd N>=23 and every admissible characteristic. The sufficient architecture is inherited from the accepted construction, not a newly invented subclass. It supplies an upper bound in the original full dictionary and in its independently-free-cross-singleton subproblem. It supplies no matching lower bound or complete support classification.

The bank constant, whole-left mechanism, reciprocal degeneration, and moment reconstruction are inherited. The additional field scope and coefficient-extension bound require the explicit separability and finite-grid arguments above. Classical generic irreducibility, separability, polynomial avoidance, finite-field extensions, and Vandermonde interpolation are not claimed as new. The proof is source-distinct from isolated N=7,11,13 witnesses and does not supersede their exact field-specific minima.

Read OPERATION_LEDGER.md for field construction, coefficient search, root recovery, operator preparation, full output, storage, and base-field arithmetic costs. Those bounds are deliberately conservative and do not establish a useful FFT runtime. Independent review is required before any acceptance or publication decision.

## Classical background checked

- Keith Conrad, Separable Polynomials, https://kconrad.math.uconn.edu/blurbs/galoistheory/separable1.pdf: an irreducible polynomial is separable exactly when its derivative is nonzero. The proof here supplies both hypotheses, rather than using a characteristic-zero shortcut.
- Andrew Sutherland, MIT 18.783 Lecture 3 (2025), https://math.mit.edu/classes/18.783/2025/LectureNotes3.pdf: finite-field existence, irreducible polynomial representations, and splitting by extension degrees. Our exhaustive construction is intentionally slower than standard algorithms and does not use an unpriced factorization oracle.

The explicit project source pins, not a literature claim, establish what was already accepted and where this candidate extends its scope.
