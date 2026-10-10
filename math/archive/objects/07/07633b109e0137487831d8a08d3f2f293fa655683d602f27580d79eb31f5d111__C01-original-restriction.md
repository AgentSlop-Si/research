# Principal restriction of cycle Green sums and an explicit infinite chirp obstruction

## Results and scope

1. A principal submatrix of an invertible weighted Hamiltonian-cycle Green matrix is exactly another Hamiltonian-cycle Green matrix. Effective edges are products along the skipped arcs. No edge division is needed; zero edges and diagonal endpoint masks are preserved.
2. For odd N=5m with gcd(m,5)=1, the equally spaced five-coordinate block of the forced chirp B_N is an explicit two-chirp-plus-diagonal family. It is not B5 when N>5.
3. The sealed N5 projective exclusion makes the positive-sign scalar curve generically forbidden, with a finite algebraic exceptional set. An expanded eliminant and a numerical cutoff are not supplied.
4. There is nevertheless an explicit infinite subfamily with no exception search: for every odd q coprime to 5 with q=1 modulo 241, the forced chirp B_(5q^2) cannot be a sum of two Hamiltonian-cycle Green terms with arbitrary diagonal endpoints. For example, q=2410k+1, k>=0, gives an infinite sequence of such lengths. This follows by exact restriction, an elementary Gauss identity, and the existing closed projective reduction certificate.

All exclusions here concern this forced chirp B and the diagonal-endpoint two-term grammar. They do not exclude arbitrary FFT factorizations, different feedback A, products of Green sums, or unmatched endpoint permutations. They use the preceding N5 certificate, whose independent reconstruction is sealed in review_n5_all_orders/REVIEW.md. The present extension is a separate result awaiting its own independent review.

## 1. Principal Green restriction, including zeros

Let sigma be one N-cycle, and let W have row action

    (Wx)_i=w_i x_(sigma(i)).

Write rho=product_i w_i. Then W^N=rho I and, when 1-rho!=0,

    (I-W)^(-1)=(I+W+...+W^(N-1))/(1-rho).                 (1)

Let S be any nonempty subset of q selected vertices. Traverse sigma from each s in S to the next selected vertex sigma_S(s). Let ell_s be that positive arc length and put

    w_S(s)=product_(t=0,...,ell_s-1) w_(sigma^t(s)).

The induced structural order sigma_S is one q-cycle. Its weighted matrix W_S satisfies

    product_(s in S) w_S(s)=rho,
    [(I-W)^(-1)]_[S,S]=(I-W_S)^(-1).                      (2)

The matrix on the right is expressed in the same ordering of S used to take the principal submatrix; it need not be the cyclic traversal ordering.

Proof: the selected arcs partition all original cycle edges, proving the product identity. In (1), for two distinct selected vertices i,j there is exactly one path length between 0 and N-1 reaching j from i. The numerator is the product along that path. Its factorization into selected arcs is exactly the corresponding numerator for W_S. Both diagonal numerators are 1, and both denominators are 1-rho. This proves every entry of (2).

This proof permits any subset of edge weights to vanish, including every edge. It never divides by an edge or an intermediate arc product. The effective inverse guard is exactly the original guard. If rho=1, both putative Green denominators are singular, and neither is admitted. For q=1 the effective weighted loop has weight rho, and the same formula holds.

For diagonal endpoints L,R, even singular ones,

    [L(I-W)^(-1)R]_[S,S]=L_S(I-W_S)^(-1)R_S.

Therefore restriction preserves a sum of two permitted terms, with induced orders that may differ between the two branches. In particular, every five-coordinate principal restriction lies in the full 24-by24 N5 order universe already classified. Monomial endpoints with unmatched permutations do not in general preserve a principal restriction of the same Green matrix; they are outside this inheritance statement.

## 2. Exact five-coordinate chirp family

Assume N=5m is odd, gcd(m,5)=1, and omega is a primitive complex Nth root. Let

    h=(N+1)/2,
    A_N=diag(omega^(h j^2)),
    G_N=sum_j omega^(h j^2),
    c_N=N G_N,
    B_N=(F_N^(-1)+A_N)^(-1),

where F_N is the unnormalized positive-exponent Fourier matrix. Use S={0,m,2m,3m,4m}, in that displayed order. Put

    eta=omega^(m^2).

Because gcd(m,5)=1, eta is primitive of order5. Also h=3 modulo 5. Define three fixed 5-by5 matrices

    F(eta)_ab=eta^(ab),
    C(eta)_ab=eta^(-3(a+b)^2),
    D(eta)_ab=eta^(-3a^2) delta_ab.

Direct substitution into the odd-chirp formula gives

    B_N[S,S]=[F(eta)-G_N C(eta)+N G_N D(eta)]/(1+N G_N).  (3)

Every exponent and the unnormalized Fourier convention are retained. Over a splitting field of characteristic not dividing 2N, the same identity holds whenever 1+N G_N!=0. That finite-field guard must be checked independently.

Equation(3) does not identify the block with B5. The matrices F,C,D are linearly independent: off the diagonal, the ratios C_01/F_01=eta^2 and C_02/F_02=eta^3 differ, so F and C are independent; D is supported on the diagonal. Thus equality with B5(eta) would force simultaneously G_N=G5(eta) and N G_N=5G5(eta), hence N=5 in characteristic zero. In particular the actual block is different for every N>5.

## 3. One scalar parameter in each Gauss sign class

Let epsilon_N=(-1)^((N-1)/2). Then

    G_N^2=epsilon_N N.                                   (4)

For completeness, the elementary change of variables u=x-y, v=x+y gives G_N G_N^-=N because2 and h are units modulo odd N. The standard Jacobi-character relation for complete quadratic Gauss sums gives G_N^-=(-1/N)G_N=epsilon_N G_N. The relation applies to every primitive additive character, so it is independent of which primitive omega was supplied. The general odd-modulus character identity is stated in Gurevich–Hadani–Howe, Section3.1, equation(3.3), with the Jacobi description in Remark3.3: [primary paper](https://arxiv.org/html/0808.2447).

Put g=G_N. Equations(3) and(4) give the one-parameter families

    H_(eta,epsilon)(g)=F(eta)-g C(eta)+epsilon g^3 D(eta),
    B_N[S,S]=H_(eta,epsilon_N)(g)/(1+epsilon_N g^3).        (5)

For actual complex N>=5, |G_N|=sqrt(N), so the denominator is nonzero. For a general symbolic or finite-field parameter it is a separate guard. Supplied-root and chirp/Gauss preparation still costs O(N) by recurrence; no extra phase convention or hidden Fourier application is introduced here.

## 4. What the N5 certificate implies generically

Fix a primitive eta and take the positive-sign curve H_(eta,+)(g). For each of the 576 order pairs, form the same closed projective necessary system used in the N5 certificate: all joint off-support equations and all maximal augmented scale minors, with target H_(eta,+)(g). Its coefficients are polynomials in g of degree at most 3, and its direction variables lie in (P1)^10.

Projection from this closed family to the g-line is proper. Hence the set Z_(eta,pi,tau) of parameter values admitting a point of that necessary system is algebraically closed. At

    g0=G5(eta),  g0^2=5,

we have H_(eta,+)(g0)=(1+5g0)B5(eta), with nonzero scalar 1+5g0. Multiplying a target by a nonzero scalar does not change whether its projective necessary system has a point: the off-support equations and each augmented minor acquire that scalar. The N5 certificate therefore excludes g0 for every order pair.

Each Z_(eta,pi,tau) is consequently a proper closed subset of an affine line, hence finite. Their union E_eta is finite as well. It contains every positive-sign parameter that could have a two-Green representation, including singular endpoints. This yields a rigorous generic obstruction, not just a numerical neighborhood of g0.

An exact algebraic definition of the exceptional set is the finite union of these 576 proper images, or equivalently the zero set of the product of the monic generators of their radical elimination ideals in Q(eta)[g]. No expanded generator has been computed here. Eliminating g with g^2-N and taking the number-field norm would produce a nonzero polynomial in N containing all positive-sign integer exceptions. Its coefficients and the resulting cutoff remain uncomputed.

Nevertheless the finite-set conclusion is enough to state: among odd N=5m with gcd(m,5)=1 and N=1 modulo 4, only finitely many lengths can evade this principal-block obstruction. The four possible primitive eta values form a finite set, and |G_N| grows with N. This is a quantified existence statement without an explicit cutoff. For the negative-sign curve, the N5 anchor is not on that curve; the same generic conclusion is not asserted without another exclusion point.

The proper-projection fact is the same one used in the N5 arithmetic lift; see [Stacks, projective morphisms are proper](https://stacks.math.columbia.edu/tag/01WC). The inherited N5 certificate supplies the crucial excluded point.

## 5. An elementary square-modulus specialization

A completely explicit infinite family avoids the unexpanded eliminant.

Let q be odd, gcd(q,5)=1, and N=5q^2. Put m=q^2 and eta=omega^(q^4). Every residue modulo N has a unique form

    x=m u+5v,   u modulo 5, v modulo m.

The cross term in h x^2 is a multiple of N. Therefore

    G_N=[sum_(u mod5) eta^(h u^2)]
         [sum_(v mod q^2) (omega^5)^(5h v^2)].

The first factor is G5(eta), since h=3 modulo 5. The second is q. To see this without a square-root/sign convention, for a primitive q^2th root xi and gcd(a,q)=1 write v=s+q t. Then

    sum_(v mod q^2) xi^(a v^2)
      =sum_(s mod q) xi^(a s^2) sum_(t mod q) (xi^q)^(2a s t)
      =q.

Only s=0 survives because q is odd and a is a unit. Here xi=omega^5 and a=5h satisfy those guards. Thus, exactly for every supplied primitive omega,

    G_(5q^2)=q G5(eta).                                   (6)

Writing g5=G5(eta), g5^2=5, formula(3) becomes

    C_q(eta)=[F(eta)-q g5 C(eta)+5q^3 g5 D(eta)]
              /(1+5q^3 g5).                             (7)

This is the actual principal block, not an approximation and not B5 except when q=1.

## 6. Explicit modular inheritance and infinite exclusion

Now assume additionally q=1 modulo 241. The coefficients of(7) lie in Q(eta), and reduce under eta->91 to the N5 coefficients:

    q g5 ->103,
    5q^3 g5 ->33,
    1+5q^3 g5 ->34 !=0.

The ring of definition is explicit. Let K5=Q(eta), g5=1+2(eta^2+eta^3), and D_q=1+5q^3 g5. The block(7) is defined over Z[eta,D_q^(-1)]. Take the prime eta->91 above 241, and localize at it. Because D_q reduces to 34, this localization is valid and its residue field is F241. The target entries are regular at this prime.

There is no reduction of the primitive Nth root to a fifth root. Formula(6) proves that the principal block lies in K5 before any reduction is taken. If one wishes to retain the ambient cyclotomic field KN=Q(omega), the prime of K5 extends to a prime of the integral closure in KN by lying over. Since q=1 modulo 241, the prime 241 does not divide N. Reduction of omega at that extended prime still has exact order N in a finite residue-field extension: the factors of X^N-1 remain pairwise coprime because its derivative is nonzero at every root. Its power eta reduces to 91, but omega need not lie in F241 and is not identified with 91. The specialization responsible for the N5 coefficients is the integer q=1 modulo 241, not a loss of root order.

The denominator has good reduction. The same closed projective special fiber is therefore exactly the one already proved empty by the N5 certificate. Proper good reduction excludes a complex point of the necessary system for C_q(eta), including the singular-endpoint boundary. This argument does not lift an open inverse guard or a modular positive solution.

By Section1, any two-Green representation of the full B_(5q^2) with diagonal endpoints would restrict to such a representation of C_q(eta). This is impossible. Hence:

    q odd, gcd(q,5)=1, q=1 (mod241)
    ==> B_(5q^2) has no sum-of-two-Hamiltonian-Green
        representation with arbitrary diagonal endpoints.

For an explicit unrestricted integer index, q=2410k+1 satisfies all three conditions for every k>=0. No factoring of the ambient cycle orders or enumeration of N! possibilities is involved. Zero edge weights and singular diagonal masks are retained by the restriction lemma and the closed N5 necessary system.

The first nontrivial member of this simple sequence is large; the result is an exact infinite obstruction, not a practical small-size benchmark or a claimed numerical cutoff for all N. It constrains the chirp feedback construction's forced B, not every possible cheap Fourier construction.

## 7. Exact checks and outstanding algebra

The newly authored controls pass 42 Green restriction cases, checking 1050 principal Green entries and 2100 diagonal-ended entries on reordered cycles and subsets, nonzero/two-zero/all-zero edge patterns, and singular endpoint masks. They check that invalid cycle-product guards remain invalid after restriction. Separate exact finite-field controls derive the block in(3), both Gauss sign classes in(4), and the square-modulus identity(6), with every root and feedback denominator recorded. They also exhibit that blocks at N>5 differ from B5.

The infinite-family reduction is checked symbolically as q=1 modulo 241; constructing a dense matrix of size5(2410k+1)^2 is neither required nor used. Nine general odd-m and six square-modulus finite-field cases verify every 25-entry block. Twenty congruence checks cover five explicit integer parameters and all four primitive fifth-root residues. Two deliberately resonant N5 cases over F31 retain the failed denominator and reject inversion, rather than being silently admitted. Exact values appear in RESTRICTION_EXTENSION_RESULTS.json.

What remains uncomputed is the expanded eliminant for E_eta (and a second anchor for the negative-sign curve). Those are not needed for the explicit square-modulus congruence family, whose parameter dependence and good-reduction guards are fully proved above.

Provenance: this extension uses the sealed N5_EXHAUSTIVE_DIAGONAL_ENDPOINT_EXCLUSION.md, the odd-chirp formula, and the fixed-direction closed-minor construction. All control code is newly authored; no uploaded program is executed. The result carries the same target and endpoint scope as the N5 certificate and makes no novelty or general FFT lower-bound claim.
