# Third independent adversarial audit: exact global C8 rank-zero minimum

20 October 2026 UTC.

## Verdict

**ACCEPT both frozen whole proofs. No mathematical gap or counterexample was found.**

For the normalized Fourier matrix F[j,k] = exp(-2 pi i j k/8)/sqrt(8), the exact result is

    min over invertible complex monomial L,R and arbitrary real C
        ||F - L C R||_2
      = min over diagonal unitary P,Q ||Im_entry(P F Q)||_2
      = (1/2) sqrt(1 + sqrt(sqrt(2)-1)).

This is a full original-model, external-operator-norm, correction-rank-zero result. It is not restricted to a guessed periodic family. The positive-Hermitian-minimum replacement proves that a hypothetical better nonperiodic pair has a no-worse periodic replacement. The remaining finite-dimensional inequalities exclude that replacement exactly.

The developer proof uses opposite-pair balancing. The independent verifier uses an exhaustive compact-maximizer/KKT argument. Both scalar proofs and the shared all-phase reductions were audited separately. My new exact checker passed 44 controls; finite sampling, optimization, source-program execution, and historical checker execution played no role in this review.

Acceptance applies to these exact bytes:

- Developer PROOF.md: SHA-256 776acb79b13199fe5b52c5e352c89135b93ff8100848cbc78598969a53fd7936.
- Independent verifier PROOF.md: SHA-256 773e372f70ff1494310d0e8daa3c07aaf69473364f8e595fd7d734a9ac76a191.

The source paths, lengths, and before/after digests are in SOURCE_BINDINGS_BEFORE.json and SOURCE_BINDINGS_AFTER.json. Frozen local copies are included. The prior accepted upper witness and its earlier independent review are also bound. Their historical statement that the global lower problem remained open is superseded only by the present new lower proof; their mathematics is unchanged.

## 1. Original model, not an internal or condition-number-weighted norm

An arbitrary invertible complex monomial L has exactly one nonzero entry in each row and column. Select each row's unit complex phase to write L=D_L M_L with D_L diagonal unitary and M_L real invertible monomial. Select column phases on the right to write R=M_R D_R. For every real C, the product M_L C M_R is real; invertibility makes this a bijection of all real matrices. Thus the set of original approximants equals the set of D_L C' D_R with diagonal-unitary exterior matrices and unrestricted real C'. No nonunitary multiplier is applied to a residual, so arbitrary monomial magnitudes and permutations do not create a conditioning loophole.

For a fixed V=P F Q, the matrix map Im_entry Z=(Z-conjugate Z)/(2i) is contractive in the complex operator norm by the triangle inequality and equality of the norms of Z and conjugate Z. For every real C', ||V-C'|| >= ||Im_entry V||; C'=Re_entry V attains equality. Exterior unitary multiplication preserves the original norm.

For unitary V=X+iY, the real part of V*V=I gives X^T X+Y^T Y=I, while Re_entry(V^T V)=X^T X-Y^T Y. Therefore Y^T Y=(I-Re_entry W)/2, W=V^T V. The matrix W is symmetric and unitary, so Re_entry W=Herm(W). With A=P^2 and B=Q^2, Q^{-1} W Q=F A F B is a UNITARY similarity, hence carries the Hermitian part by unitary conjugation. Thus

    ||Im_entry(P F Q)||_2^2
      = (1-lambda_min(Herm(F A F B)))/2.

Every diagonal-unitary A,B has diagonal-unitary square roots. All phases, all real cores, and all original monomial factors are retained.

## 2. The all-phase replacement and the forbidden-commutation challenge

I separately derived the replacement before reading the supplied proof. For C=F A F, its entries depend only on j+k modulo eight. If H shifts j by four, H C H=C for arbitrary, not necessarily periodic, A. Averaging Herm(C B)>=c I and its H-conjugate gives

    Herm(C E)>=c I, E=(B+H B H)/2.

E is diagonal and four-periodic with entry moduli at most one. Write E=D T with D diagonal unitary and four-periodic and 0<=T<=I. If a zero entry occurs, it can be assigned a common phase in its paired positions. In fact c>0 rules out a zero entry because the corresponding diagonal element of Herm(C E) would be zero. Either version of this observation is valid.

The essential normalization implication is not a generally invalid Loewner-order division by T. Put Z=C D. For an eigenvector Zx=lambda x of unit norm, unitarity gives Z*x=conjugate(lambda)x and hence x*Z=lambda x*. Therefore

    c <= x*Herm(Z T)x = Re(lambda) x*T x.

Since 0<=x*T x<=1 and c>0, Re(lambda)>=c. The complete orthonormal eigenbasis of the unitary Z then proves Herm(Z)>=c I. This step neither asserts nor needs ZT=TZ. Positive c is essential to this implication and is available in the contradiction because the target m is positive.

The replacement first makes B four-periodic while keeping A arbitrary. The products (F A)(F B) and (F B)(F A) are unitarily similar through the unitary F A. Applying the same argument with their roles swapped makes A four-periodic without changing the already chosen B. Swapping back retains the same Hermitian lower bound.

This is an existence replacement. Neither proof claims that every minimizing phase pair is periodic, or that an average of phase matrices is itself unitary.

## 3. Full sectors, determinant signs, and trace contraction

For four-periodic phases, my checker constructs the normalized full 8-by-8 Fourier matrix directly from the exact eighth-root cycle and verifies its unitarity and symmetry. It constructs all eight real orthonormal sector vectors, and checks the full matrix identity T^T F A F B T=diag(M0,M1,M2,M3) with a0,...,a3,b0,...,b3 independent symbolic variables. Thus this is not a numerical phase test or a check only at the candidate witness.

With alpha=(a0+a2)/2, beta=(a0-a2)/2, gamma=(a1+a3)/2 and delta=-i(a1-a3)/2, the four blocks in both proofs are correct. Their determinants are respectively

    a0 a2 b0 b2,
    -a1 a3 b0 b2,
    -a0 a2 b1 b3,
    -a1 a3 b1 b3.

In particular det(M0)det(M3)=-det(M1)det(M2). Each trace, each sign, and each off-sector zero is covered by exact generic controls.

The four normalized absolute traces can be placed in a nonnegative 2-by-2 matrix R that is the entrywise product of one matrix having unit Euclidean row norms and one having unit Euclidean column norms. The developer uses its transpose, equivalently reversing the two norm conditions. Both layouts are valid. For arbitrary complex x,y, apply Cauchy-Schwarz to the double sum using the row-normalized factor with |y_i| and the column-normalized factor with |x_j|. This proves |y*R x|<=||y|| ||x|| and hence ||R||_2<=1. Nonnegative entries, not any illicit matrix-product identity, are used.

If every eigenphase lies in [-theta,theta] with theta<pi/2, take the ACTUAL two principal phases of each sector and define their midpoint nu_i and nonnegative half-separation beta_i. Then |nu_i|+beta_i<=theta and |tr(M_i)|/2=cos(beta_i). In particular beta_i<pi/2, so absolute trace does not introduce an extra cosine sign or branch. The determinant relation gives

    nu0+nu3-nu1-nu2 = pi/2 modulo pi.

Every real representative of this congruence has absolute value at least pi/2. Consequently sum |nu_i|>=pi/2 and

    sum arccos(|tr(M_i)|/2) <= 4 theta-pi/2.

There is no choice of determinant-square-root branch that can evade this argument.

## 4. Independent audit of opposite-pair balancing

For a positive 2-by-2 contraction R=[[a,b],[c,d]], every entry is strictly below one. Holding a,d fixed, increase b,c by a common factor until the first norm-one boundary. Existence follows by continuity and unbounded growth under continued scaling. Along the path up to the first crossing it remains a contraction; at the boundary strict positive companions in each row prevent any entry from reaching one. This can only increase the arcsine objective.

At norm one, det(I-R^T R)=0. Writing q=bc gives the exact identities

    (b+c)^2=(1-ad+q)^2-(a-d)^2,
    [q-(1-a)(1-d)][q-(1+a)(1+d)]>=0.

Because q<1<(1+a)(1+d), the allowed root branch is q<=(1-a)(1-d). The cosine addition formula gives

    cos(asin b+asin c)=sqrt(K+2adq)-q,
    K=a^2+d^2-a^2 d^2.

Its derivative is ad/sqrt(K+2adq)-1<0 because K-a^2 d^2>0. At q=(1-a)(1-d), the radical is the positive quantity a+d-ad, and the cosine equals 1-2(1-a)(1-d). Both angles being compared lie in [0,pi]; cosine is injective and decreasing there. This proves the claimed two-angle inequality with every sign and branch retained.

Let t=sqrt((1-a)(1-d)). Replacing b,c by t,t produces a symmetric contraction with eigenvalues 1 and a+d-1. If all original entries are at least m>0, the q bound shows t>=m, while a,d>=m gives t<=1-m. Its column-swapped matrix [[t,a],[d,t]] is still a contraction. A second application bounds asin a+asin d by 2 asin(1-t). Finally asin t+asin(1-t) is convex and symmetric, so its maximum on [m,1-m] is its common endpoint value, provided m<=1/2. Subtracting from 2pi proves the sharp four-arccosine inequality. Equality is realized by [[m,1-m],[1-m,m]], whose norm is one.

I found no missing boundary in this argument. The proof is stronger than required, valid throughout 0<m<=1/2.

## 5. Independent audit of exhaustive KKT boundary cases

The verifier's separate proof is valid on its stated sufficient interval 0<m<=1-1/sqrt(2). This narrower interval contains the target exactly.

The feasible set is compact and nonempty. Positive lower bounds imply every entry is bounded strictly below one, so the arcsine objective is smooth and strictly convex entrywise. A maximizer has norm one. The top singular value is simple: R^T R has strictly positive off-diagonal entry, hence distinct eigenvalues. Its second singular value is strictly less than one.

- No active lower entry: perturb in both directions along the second singular-vector rank-one direction. The top singular value remains one for sufficiently small perturbations, while all entries remain above m. Strict convexity contradicts a maximum at the midpoint.
- Exactly one active lower entry: permute to a=m. The smooth boundary f=det(I-R^T R)=0 has f_d=-2[d(1-a^2)+abc]<0, so d is locally a function of b,c. The b and c stationarity equations reduce exactly to (sqrt((1-b^2)(1-c^2))-ad)(b sqrt(1-c^2)-c sqrt(1-b^2))=0. The first factor is strictly positive: row bounds give sqrt(1-b^2)>=a and sqrt(1-c^2)>=d, and equality in both would give two unit-norm rows with positive inner product, impossible for a contraction. Thus b=c. Positivity of the resulting symmetric matrix means its norm-one Perron eigenvalue is +1, giving d=1-b^2/(1-a). The derivative along this curve is 2/sqrt(1-b^2)-2/sqrt(2(1-a)-b^2)>0 for a<1/2. A small increase of b leaves d>m, contradicting maximality.
- At least two adjacent active entries: the other row or column has norm at most one, so its two arcsines sum to at most pi/2. The bound pi/2<=2 asin(1-m) is exactly the stated interval restriction. This covers three or four active entries as well.
- Two opposite active entries: write R=[[m,u+v],[u-v,m]], v>=0, s=sqrt(m^2+v^2). Its singular values are |u+s| and |u-s|, so norm=u+s. For an upper bound, increase u to 1-s. The free entries remain positive and below one. Differentiating their arcsine sum in v, the required sign follows after squaring positive factors from the exact difference 4m^2 v>=0. The derivative is nonpositive and is strictly negative for v>0. Returning to v=0 gives b=c=1-m and the stated sharp bound.

These cases exhaust every possible maximizer. My independent symbolic controls rederived the stationarity factor, symmetric radical simplification, both opposite-entry singular squares, and the squared derivative difference. No numerical KKT solver was used.

## 6. Fixed threshold, radical branches, and contradiction

Set h=sqrt(sqrt(2)-1), m=(1-h)/2 and theta*=acos m. Since 0<h<1, 0<m<1/2 and theta* is strictly between pi/4 and pi/2. Also h>sqrt(2)-1, so m<1-1/sqrt(2), satisfying even the narrower KKT version.

The relation h^2=sqrt(2)-1 gives

    (sqrt(2)(1-m)-m)^2=1-m^2.

The left square root candidate is positive because m<1/2. Thus sqrt(1-m^2)=sqrt(2)(1-m)-m, and cos(theta*-pi/4)=1-m. Both theta*-pi/4 and acos(1-m) lie in (0,pi/2), fixing the exact identity

    acos(1-m)=theta*-pi/4.

A strictly better original-model approximation would have Hermitian spectral minimum c>m. Unitarity implies c<=1, and theta=acos c satisfies theta<theta*<pi/2. The all-phase replacement yields periodic phases with every eigenphase in [-theta,theta]. Their four trace quantities are each at least c>m and form the exact contraction above.

The scalar lemma is applied with the FIXED m, not with c. Therefore neither c>1/2 nor c>1-1/sqrt(2) creates a domain loophole. It gives a sum of arccosines at least 4theta*-pi/2, whereas the determinant-center argument gives at most 4theta-pi/2. These contradict theta<theta*. This proves the global lower bound, rather than only a necessary condition at a stationary point.

## 7. Attainment and exact external residual

The accepted explicit phases have h as above, z=h+i sqrt(2-sqrt(2)), and w=sqrt((1+h)/2)+i sqrt((1-h)/2). The positive radical convention gives |z|=|w|=1 and w^2=z. Squaring the listed P,Q yields the listed A,B without a missing sign in the third entry of B.

My generic block checker independently substitutes the exact A,B and confirms traces/determinants (1-h,1) in sectors 0,3 and ((1-i)(1+h)/sqrt(2),-i) in sectors 1,2. The former sector pair has phases plus/minus theta*. The latter has phases -pi/4 plus/minus (theta*-pi/4). Thus the full eigenvalues are exp(i theta*) twice, exp(-i theta*) four times, and exp(i(theta*-pi/2)) twice. Their minimum real part is exactly m. The half-angle formula gives defect sqrt((1-m)/2)=(1/2)sqrt(1+h).

The actual legal original-model choice is C=Re_entry(P F Q), L=P*, R=Q*, with zero correction. Its residual is P* i Im_entry(P F Q) Q*, so its EXTERNAL norm is exactly the same value. This supplies the matching upper bound and an attained minimum, not merely an infimum.

## 8. Exact controls, independence, and exclusions

The new program independent_exact_checks.py constructs its own exact Fourier matrix, full sector basis, polynomial identities, and radical substitutions. It imports no candidate or historical code and executes none. All 44 controls pass, and all four bound source files have unchanged hashes before and after the checks. Assertions are exact symbolic equalities or exact algebraic comparisons; there is no numerical tolerance. The universal matrix inequalities and all boundary/branch arguments are justified analytically above rather than inferred from these finite controls.

No external state was modified. No novelty claim was investigated or accepted. The result is specifically N=8, correction rank zero, unrestricted real core and invertible complex-monomial exterior factors in the external operator norm. It does not settle other dimensions, positive correction ranks, restricted-core models, or classification of every minimizer. In particular, no classification follows merely from existence of a no-worse periodic replacement.
