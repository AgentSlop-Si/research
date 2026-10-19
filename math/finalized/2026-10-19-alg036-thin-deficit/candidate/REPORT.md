# ALG-036: sharp complex Gaussian projector bound and thin-deficit endpoint

Date: 2026-10-19 UTC. Owner: ALG-036; retained priority: 34.
Status: candidate proof; independent review is a separate step.

## 1. Main result, conventions, and scope

Throughout, CN(0,I_d) has density pi^(-d) exp(-||z||_2^2) with respect to Lebesgue measure on C^d=R^(2d). In particular E|z_k|^2=1, while each real and imaginary part has variance 1/2. The infinity norm is max_j |z_j|, with the complex modulus. Logs are natural.

**Theorem 1 (sharp projector/translation bound).** Let P be an orthogonal complex projector on C^N, of complex rank 1<=d<=N. Put p_j=P_jj. For Z~CN(0,P), every b in C^N and every r>0,

    Pr(||Z-b||_infinity <= r)
      <= product_(j:p_j>0) (1-exp(-r^2/p_j))^(p_j)
      <= (1-exp(-N r^2/d))^d.                         (1)

If a zero-leverage coordinate has |b_j|>r, the probability is instead exactly zero. Radius r=0 also has probability zero when d>=1. Thus the last bound in (1) remains valid at r=0. For d=0 the Gaussian is deterministic, and this theorem is replaced by its deterministic indicator.

When d divides N, the last bound is attained at b=0 by the projector onto vectors constant on each of d disjoint coordinate blocks of size N/d. Consequently

    sup_(rank P=d, b in C^N) Pr(||Z-b||_infinity<=r)
       = (1-exp(-N r^2/d))^d                          (2)

on those dimensions, for every r>=0. We do not assert exact sharpness for nondivisible N,d, nor classify all extremizers.

**Theorem 2 (adaptive endpoint).** Let x~CN(0,I_N), U a fixed complex unitary, and R independent of x. An algorithm chooses measurable complex-linear queries a_t* x using only R and earlier answers, stops at an almost-sure finite transcript stopping time T, and returns a measurable transcript-only estimate Xhat. Suppose terminal complex rank deficit D=N-rank(A_T) is at least the deterministic integer d>=1 almost surely. No raw-input access, uncharged norm, input-dependent coefficient side channel, or extra input statistic is allowed. For every C>=0 and 0<epsilon<1,

    Pr(||Xhat-Ux||_infinity <= C||x||_2/sqrt(N))
      <= B_(N,d)(C^2(1+epsilon))
          + exp[-N(epsilon-log(1+epsilon))],          (3)

where, for a>=0,

    B_(N,d)(a) = (1-exp(-Na/d))^d.                   (4)

The first term can be replaced by the expectation of the actual posterior leverage product in (1), evaluated at r=C sqrt(1+epsilon). The conclusion also holds for a countably infinite limiting transcript under the same terminal rank condition. An exceptional rank-condition event of probability eta costs only an additional eta. An expected deficit alone is insufficient.

**Sharp transition.** Fix C>0. For d=d_N tending to infinity define

    w_N = NC^2/d - log d.                            (5)

In the critical regime d asymptotic to N/log N, the upper bound in (3), with epsilon_N=N^(-1/4), has limiting value exp(-exp(-s)) when w_N tends to s in R; it tends to zero when w_N tends to minus infinity. When d divides N, an explicit fixed linear measurement scheme attains these same limits and has success tending to one when w_N tends to plus infinity. These are Gaussian-average success statements. The same relative-error probabilities hold for this homogeneous construction on the normalized sphere. Arbitrary sphere-prior adaptive algorithms are distinguished in Section 9.

In first-order form, if d/(N/log N) tends to a>0, then all admissible schemes have success tending to zero for a>C^2, whereas there exist schemes with Gaussian-average success tending to one for a<C^2. The latter existence holds without divisibility, using nearly equal blocks. A statement only of order N/log N misses both the constant C^2 and the log-log correction at the transition.

## 2. Geometric Brascamp-Lieb, including a short proof for the required inputs

The external primary reference is Bennett, Carbery, Christ, and Tao, *The Brascamp-Lieb inequalities: finiteness, structure and extremals*, Definition 1.1 and Example 1.6 (printed pages 1-3), Definition 2.1 and Remark 2.2 (page 9), and Proposition 2.8 (page 12):
https://math.berkeley.edu/~mchrist/Papers/bcct11.pdf

The constant-one theorem and the equivalence between orthogonal projections and coisometries were checked directly. The specialization below is derived here, rather than attributed to the paper. To keep the mathematical argument self-contained, the needed constant-one inequality is also proved next.

Let B_j:R^n->R^(n_j) be real linear maps and p_j>0 satisfy

    B_j B_j^T = I_(n_j),
    sum_j p_j B_j^T B_j = I_n.                       (6)

Then, for nonnegative bounded compactly supported measurable functions f_j,

    integral_(R^n) product_j f_j(B_j x)^(p_j) dx
       <= product_j (integral f_j)^(p_j).            (7)

For the inputs used below each f_j is a Gaussian density restricted to a disk. They are bounded, compactly supported, and continuous except along a circle. Zero-integral inputs are immediate, so assume all integrals are positive.

Here is a heat-kernel proof. Let u_j(t,y)=(4 pi t)^(-n_j/2) integral exp(-|y-z|^2/(4t)) f_j(z) dz for t>0, and put F(t)=integral product_j u_j(t,B_j x)^(p_j) dx. Set v_j=grad log u_j(t,B_j x). The coisometry identity in (6) and integration by parts give

    F'(t) = integral product_j u_j^(p_j)
              [sum_j p_j |v_j|^2
                 - |sum_j p_j B_j^T v_j|^2] dx >=0. (8)

For completeness, the derivative of log u_j is Delta log u_j+|grad log u_j|^2; also Delta_x log u_j(t,B_j x)=Delta_y log u_j(t,B_j x). Integrating Delta_x log(product u_j^p) times that product gives minus its squared log-gradient. The final inequality follows because the map (sqrt(p_j)v_j)_j -> sum_j sqrt(p_j)B_j^T(sqrt(p_j)v_j) has operator norm one: its product with its transpose is the second identity of (6).

All differentiations and integrations by parts are justified for t in a compact subinterval of (0,infinity): heat convolutions of bounded compactly supported functions have Gaussian tails; their log-derivatives have at most polynomial growth; (6) combines their Gaussian tails into integrable decay in all n directions. Taking traces in (6) gives sum p_j n_j=n. Change variables x=sqrt(t)z. For each j,

    t^(n_j/2) u_j(t,sqrt(t)B_j z)
       -> (4pi)^(-n_j/2) exp(-|B_j z|^2/4) integral f_j.

The product limit integrates to product_j(integral f_j)^p_j, because sum p_j|B_j z|^2=|z|^2. Dominated convergence holds, for t>=1, by compact support and |a-b|^2>=|a|^2/2-|b|^2, yielding an integrable constant times exp(-|z|^2/8). Thus F(infinity) equals that product. For the disk inputs, heat convolution tends to f_j at all points off the boundary circle. Its inverse image under a surjective B_j has Lebesgue measure zero. Fatou's lemma therefore bounds the left side of (7) by liminf_(t->0)F(t). Monotonicity (8) proves (7) for every input needed here. More generally, the same argument uses almost-everywhere convergence at Lebesgue points. No unproved small-ball comparison is hidden in (7).

## 3. Complex-to-real datum and the leverage bound

Factor P=VV* with V:C^d->C^N an isometry, V*V=I_d, and let v_j be its jth row. Then p_j=||v_j||^2, 0<=p_j<=1, sum p_j=d, and Z=Vg with g~CN(0,I_d).

If p_j=0, Z_j=0 deterministically. First test the constraint |b_j|<=r; if it fails, the desired probability is zero. Otherwise omit that row. For each remaining row, let B_j be the realification of the complex-linear map g->v_j g/sqrt(p_j), from C^d to C. Identifying each complex space with its usual real Euclidean space preserves the norm. A unit complex row is a real rank-two coisometry: its real matrix B_j satisfies B_j B_j^T=I_2. Realification of V*V=I_d gives

    sum_(j:p_j>0) p_j B_j^T B_j=I_(2d).              (9)

In particular the common kernel is zero and the geometric datum is nondegenerate. These are the full hypotheses of (7), with real input dimension 2d and output dimensions 2. Define on R^2=C

    f_j(y) = pi^(-1) exp(-|y|^2)
                1_{|sqrt(p_j)y-b_j|<=r}.            (10)

Since a positive power of an indicator is the same indicator, (9) and sum p_j=d imply

    product_j f_j(B_j g)^(p_j)
       = pi^(-d) exp(-||g||^2)
           1_{|v_j g-b_j|<=r for every nonzero row}. (11)

There is no missing factor of two: pi^(-d) exp(-||g||^2) is exactly the proper complex Gaussian density under the stated convention.

The mass integral of (10) is the probability that W~CN(0,p_j) lies in the radius-r disk centered at b_j. A radial nonincreasing density assigns maximal disk mass to the centered disk. One direct proof uses layer cake: each density superlevel set is a centered disk, its intersection with any radius-r disk has area at most the smaller of the two disk areas, and concentric disks attain this value. Integrating over levels proves the assertion. Polar integration then gives

    integral f_j <= 1-exp(-r^2/p_j).                (12)

Equations (7), (11), and (12) prove the first inequality of (1), uniformly in all shifts. No coordinate independence is assumed.

## 4. Concavity, zero leverage, and matching constructions

Fix a=r^2>0 and define h_a(p)=p log(1-exp(-a/p)) for p>0, extended by h_a(0)=0. For t=a/p,

    h_a'(p)=log(1-exp(-t)) - t/(exp(t)-1),
    h_a''(p)= -t^2 exp(t) / [p(exp(t)-1)^2] <0.     (13)

The continuous extension at zero is concave, and strictly concave on [0,infinity). Jensen's inequality with the N leverage values, including zeros, yields

    sum_j h_a(p_j) <= N h_a(d/N)
                    = d log(1-exp(-Na/d)).          (14)

Exponentiation proves the second inequality of (1). If exactly m coordinates have positive leverage, the same reasoning gives the stronger (1-exp(-m r^2/d))^d. Keeping N is a valid ambient bound. For r>0, equality in the ambient Jensen step requires all N leverages to equal d/N; that requirement alone is not asserted sufficient for equality in the whole theorem.

At r=0, Vg is nonatomic because d>=1. At least one nonzero scalar row has a continuous complex Gaussian law, so the probability of matching a specified vector exactly is zero. This handles the case excluded by taking logarithms. At d=0 the distribution is deterministic; no positive-rank formula is applied.

Partition the coordinates into d nonempty blocks with sizes n_1,...,n_d, sum n_l=N. Let u_l be the normalized indicator vector of block l and P=sum_l u_l u_l*. For independent g_l~CN(0,1), the coordinates of Z in block l all equal g_l/sqrt(n_l). Hence at b=0,

    Pr(||Z||_infinity<=r)
       = product_(l=1)^d (1-exp(-n_l r^2)).          (15)

The leverage bound is exactly equal to (15), including for unequal block sizes: each of the n_l coordinates has leverage 1/n_l. If n_l=N/d for all l, (15) equals the final bound (1), proving (2).

For general N=md+k, 0<=k<d, choose d-k blocks of size m and k blocks of size m+1. The resulting exact success is

    (1-exp(-m r^2))^(d-k) (1-exp(-(m+1)r^2))^k.     (16)

This is a useful matching construction away from the critical window. Its integer rounding can have a nonvanishing effect within the critical window. We therefore do not use it to assert the exact universal Gumbel limit for arbitrary nondivisible dimensions.

## 5. Adaptive Gaussian posterior, stopping, and limiting transcripts

Here are full conditioning details so the new small-ball bound does not silently change the model. All random objects can be taken on standard Borel spaces. Draw all independent coins R initially, and write F_t=sigma(R,y_1,...,y_t). Each query row a_t is F_(t-1)-measurable. Initially x|F_0~CN(0,I_N). Inductively suppose

    x|F_(t-1) ~ CN(m,P),

where P projects onto the common kernel of the previous queries. Conditional on F_(t-1), the next row a=a_t is fixed. Put v=a*Pa. If v=0, the response a*x=a*m is already determined and changes neither mean nor covariance. If v>0, write the residual as its component along Pa/sqrt(v) plus the orthogonal residual. The two Gaussian components are independent, and observing y=a*x gives

    m_new=m+Pa(y-a*m)/v,
    P_new=P-Paa*P/v.                                (17)

The vector Pa/sqrt(v) has unit norm and lies in range P. Thus P_new is the orthogonal projector onto range P intersect ker(a*). This proves by induction that

    x|F_t ~ CN(m_t,P_t),
    rank P_t=N-rank(A_t).                           (18)

Arbitrary measurable query branching is allowed. A random row does not carry extra input information because it is chosen from the already conditioned transcript. Independent decoder coins are included in R.

For an almost-sure finite F_t-stopping time T, the event {T=t} is F_t-measurable. Test the conditional-law identity on an arbitrary stopped-transcript event intersected with {T=t}, use (18) at deterministic t, and sum over t. This proves x|F_T~CN(m_T,P_T). The stopping event adds no information beyond the stopped transcript. Conditional on F_T,

    Ux=Um_T+Z_T,   Z_T~CN(0,Q_T),
    Q_T=UP_TU*,   rank Q_T=D.                       (19)

The decoder shift b_T=Xhat-Um_T is fixed under this conditioning, so Theorem 1 applies directly to it.

For a countably infinite terminal transcript F_infinity=sigma(union F_t), the square-integrable martingale m_t=E[x|F_t] converges almost surely and in L2 to m_infinity. Every positive-variance query reduces rank by one. Since there are at most N such reductions, P_t is eventually constant on each path and converges to the projector P_infinity onto the intersection of all query kernels. For fixed h in C^N,

    E[exp(i Re(h*x))|F_t]
      = exp(i Re(h*m_t) - h*P_t h/4).                (20)

Bounded conditional-expectation martingale convergence identifies the limiting conditional characteristic function. First use a countable dense set of h, then continuity. It follows that x|F_infinity~CN(m_infinity,P_infinity). This proves the same estimate for any decoder of that limiting transcript. There is no implicit deterministic query-count bound.

For fixed a>0, d->d log(1-exp(-Na/d)) has negative derivative by (13). Thus B_(N,D)(a)<=B_(N,d)(a) whenever D>=d. Averaging (19) proves

    Pr(||Xhat-Ux||_infinity<=sqrt(a))<=B_(N,d)(a).   (21)

More precisely the conditional success is bounded by the posterior leverage product. If the rank lower bound fails on an event of probability eta, split off that event at cost eta; it is not necessary to condition on it.

## 6. Norm envelopes and relative error, without posterior norm conditioning

Put S=||x||^2. It is the sum of N independent mean-one exponential variables. Chernoff's argument using E exp(lambda S)=(1-lambda)^(-N), lambda<1, gives, for 0<epsilon<1,

    Pr(S>N(1+epsilon))
       <= eta_+(N,epsilon)
       := exp[-N(epsilon-log(1+epsilon))],
    Pr(S<N(1-epsilon))
       <= eta_-(N,epsilon)
       := exp[-N(-epsilon-log(1-epsilon))].          (22)

Indeed optimize the exponential Markov bound at lambda=epsilon/(1+epsilon) for the upper tail and lambda=-epsilon/(1-epsilon) for the lower tail.

For ANY estimate, success together with S<=N(1+epsilon) implies the fixed-radius event at C sqrt(1+epsilon). Apply (21) without conditioning on the norm event, and add the upper-tail probability. This proves (3).

For the fixed linear block construction, its error is P Ux. On S>=N(1-epsilon), the fixed-radius event ||P Ux||_infinity<=C sqrt(1-epsilon) implies relative-error success. Consequently, whenever d divides N, its success probability p_block satisfies the two-sided sandwich

    B_(N,d)(C^2(1-epsilon)) - eta_-(N,epsilon)
       <= p_block
       <= B_(N,d)(C^2(1+epsilon)) + eta_+(N,epsilon). (23)

Bounds can be truncated to [0,1]. No independence between residual error and S is asserted or needed. Neither (3) nor (23) conditions a Gaussian posterior on a norm event.

To realize this construction, query an orthonormal basis of the complement of the desired d-dimensional output residual subspace. Explicitly, for output-basis vectors q_1,...,q_(N-d), query (U*q_l)*x=q_l*Ux, and return sum q_l(q_l*Ux). This uses exactly N-d independent complex-linear measurements and has residual P Ux. It is a deterministic, nonadaptive, admissible scheme for every fixed U. Its arithmetic evaluation cost is not claimed to be small.

## 7. Exact thin-deficit scale and critical window

First consider a deterministic fixed radius C. Write t_N=NC^2/d and lambda_N=d exp(-t_N)=exp(-w_N). For d->infinity and w_N->s finite, exp(-t_N)=exp(-w_N)/d->0 and

    log B_(N,d)(C^2)
      = d log(1-exp(-w_N)/d) -> -exp(-s).            (24)

If w_N->-infinity, B<=exp(-lambda_N)->0. If w_N->+infinity, 1-B<=lambda_N->0; this last inequality is the elementary union bound for d independent factors, or Bernoulli's inequality. These assertions require no coordinate independence in the upper theorem; independence enters only in its attaining construction.

For relative error in the critical regime d asymptotic to N/log N, choose explicitly epsilon_N=N^(-1/4) (for N>1). Then N epsilon_N^2=sqrt(N)->infinity, eta_+ and eta_- both tend to zero, and

    (NC^2/d) epsilon_N = O(log N N^(-1/4)) ->0.      (25)

Thus the parameters of the upper and lower B terms in (23) are w_N plus/minus a quantity tending to zero. This proves the relative-error Gumbel limit exp(-exp(-s)) for the attaining equal-block scheme, the same universal limsup upper bound for all admissible schemes, and universal success tending to zero when w_N->-infinity within this regime. It also proves block success tending to one when w_N->+infinity there. The finite norm envelopes (3) and (23) are valid outside the regime as well.

The threshold defined by t_N=log d is the unique positive solution

    d_c log d_c=NC^2,
    d_c=NC^2/W(NC^2),                               (26)

where W(y) is defined as the positive solution of W exp(W)=y. Elementary inversion gives

    d_c = C^2 N /
          [log N-log log N+log(C^2)+o(1)].           (27)

For bounded real h and d=d_c+h d_c/(log d_c+1)+o(d_c/log d_c), Taylor expansion of NC^2/d-log d at d_c gives w_N->-h. The critical width in rank deficit is therefore d_c/(log d_c+1), of order N/(log N)^2; on equal-block dimensions the limiting success is exp(-exp(h)). This formula describes any integer sequence satisfying the stated w_N limit AND the divisibility condition. It does not assert that all prescribed real widths can be achieved by every fixed-N divisor lattice.

If d/(N/log N)->a>0, then w_N=(C^2/a-1)log N+o(log N), up to lower-order terms. If a>C^2 the universal relative-error success tends to zero. If a<C^2, use (16). With m=floor(N/d), the failure probability at radius C sqrt(1-epsilon_N) is at most

    d exp[-m C^2(1-epsilon_N)]
      <= exp[C^2(1-epsilon_N)]
           d exp[-(N/d)C^2(1-epsilon_N)] ->0.       (28)

Together with the lower norm envelope this proves success tending to one for an admissible construction, without d|N. In particular d=o(N/log N) admits such high Gaussian-average success. Conversely d/(N/log N)->infinity implies universal success tending to zero: t_N=o(log N), while log d is asymptotic to log N, and the upper norm envelope applies.

At the apparent leading-order boundary d=floor(C^2 N/log N), w_N=log log N-log(C^2)+o(1)->+infinity. Nearly equal blocks therefore still succeed with probability tending to one. The true critical location is (27), not that uncorrected expression. For arbitrary sequences whose ratio merely tends to C^2, either limit or a nontrivial critical limit can occur depending on the smaller-order offset.

## 8. Nondivisible dimensions and what is, and is not, sharp

The finite universal upper bound is proved for every N,d. Equality is proved whenever d|N. Nearly equal blocks prove the same first-order threshold for all dimensions. The exact universal extremum and exact critical-window law for arbitrary nondivisible N,d remain unproved here.

To see the possible rounding effect concretely, write N/d=m+theta, theta=k/d in [0,1). For nearly equal blocks at fixed radius C, its expected count of independent block exceedances is

    lambda_block
      = d exp(-NC^2/d)
          [(1-theta)exp(theta C^2)
             + theta exp(-(1-theta)C^2)].            (29)

The bracket is at least one and can stay strictly above one. If theta->theta_0 and w_N->s, (16) therefore tends to exp(-A(theta_0,C)exp(-s)), with A equal to that bracket, rather than automatically exp(-exp(-s)). Shrinking norm envelopes preserve this limit at relative error. Other projector constructions could improve it; (29) does not establish nonattainment of the universal bound.

The theorem is a complex Gaussian disk-product statement. It is not a claim for real Gaussian Cartesian cubes under unchanged constants, for nonproper complex Gaussians, for general covariance matrices without an appropriate new argument, or for independent coordinates of a singular projector. Nonuniform leverage and zero leverage have already been treated explicitly.

## 9. Normalized sphere and deterministic-input quantifiers

Let X=sqrt(N)x/||x||, so X is uniform on the complex sphere of radius sqrt(N). For the fixed linear decoder of Section 6, the error is homogeneous, and exactly, sample by sample,

    ||P Ux||_infinity <= C||x||/sqrt(N)
      iff ||P U X||_infinity <= C.                  (30)

Therefore all lower constructions and their relative-error limits above are also statements about that decoder's success on the normalized sphere. The relative threshold on the unit sphere x/||x|| is C/sqrt(N).

One can also compute the equal-block sphere construction directly. In a unitary basis adapted to the d residual directions, write the N independent Gaussian squared moduli as E_1,...,E_N. Their proportions (E_i/sum E_i) are uniform on the simplex, i.e. Dirichlet(1,...,1): the change of variables from the E_i to their sum S and N-1 proportions has Jacobian S^(N-1), and the joint exponential density exp(-S) therefore has no dependence on those proportions. For each nonempty fixed subset of k residual directions, the probability that all k proportions exceed u is (1-ku)^(N-1) if ku<1, and zero if ku>=1; translate those k simplex coordinates by u and scale the remaining simplex by 1-ku. Inclusion-exclusion with u=C^2/d gives, for N>=2 and C>0,

    p_sphere = sum_(k=0)^d (-1)^k binom(d,k)
                  (1-k C^2/d)_+^(N-1).             (31)

The k=0 term is one; at zero base, the term is zero. For N=1,d=1, success is the deterministic indicator C>=1. At C=0 and d>=1 success is zero. Formula (31) is an exact finite-sphere formula for this construction, and is not equal to the Gaussian fixed-radius product (2). For example N=2,d=1,C=1 yields sphere success one, versus Gaussian fixed-radius success 1-exp(-2). Both statements are consistent with the norm-envelope comparison.

The adaptive Gaussian-posterior proof must NOT be applied verbatim to a sphere prior. Under a sphere prior, a linear-measurement posterior is generally uniform on a residual sphere with transcript-dependent radius, not CN(0,P). Arbitrary translations can behave differently on a sphere. Even a one-dimensional complex sphere is a circle: a small disk centered at zero has zero mass, whereas a suitable translated disk has positive arc mass. Thus the centered Gaussian disk lemma is not a sphere disk lemma.

The universal upper bound transfers to a sphere-prior algorithm if its operation and success event are invariant under positive radial rescaling in the requisite sense: its query rows and stopping rule are unchanged when all answers are scaled by a positive factor, and its decoder scales by that factor. Running that same admissible algorithm on x and X then gives the equivalence (30) with its actual error. Without this property or another proved reduction, no universal upper theorem for all arbitrary sphere-prior adaptive algorithms is asserted here. Access to ||x|| would be an uncharged nonlinear side channel in the stated Gaussian model and is not smuggled into the reduction.

For the original every-fixed-input randomized guarantee on all x in C^N, no sphere reduction is needed. Define p_N(x)=Pr_R(success on fixed x). Whenever the universal Gaussian-average bound is epsilon_N,

    E_x p_N(x)<=epsilon_N,
    Pr_x(p_N(x)>eta)<=epsilon_N/eta for eta>0.       (32)

A proposed p_N(x)>=1-rho_N for every fixed x would force 1-rho_N<=epsilon_N. When the bound tends to zero, there is a deterministic bad input, fixed independently of the later seed draw. Matching Gaussian-average success of the block scheme does NOT prove a matching every-fixed-input randomized guarantee. In fact a nonzero vector in its unmeasured subspace is a possible worst-case obstruction; average-case attainment and worst-case achievability are different claims.

## 10. Block-local consequence and retained boundaries

Under the already accepted original block-local embedding, B>=floor(N/M)-2 fully occupied length-M blocks with at most s complex-linear queries each give the pathwise lower bound

    D>=B(M-s).                                      (33)

One can now insert any deterministic integer lower bound d from (33) into (3), including deficits of order N/log N. For example, if M/log N->kappa>0 and M-s=q is a fixed positive integer, then d/(N/log N)->q/kappa. If q/kappa>C^2, the universal Gaussian-average endpoint success tends to zero. More precise decisions at equality require the actual lower-bound sequence d and w_N, not just its first-order coefficient.

The equal-block residual construction demonstrates sharpness within the unrestricted complex-linear information model. It need not belong to the original block-local architecture, particularly for a prescribed U. Therefore its positive side is NOT claimed as a matching block-local algorithm. No computation-time or Fourier arithmetic lower bound follows. The result concerns retained information, not the cost of realizing dense queries or the decoder.

The previous full-information-on-some-seeds and random-one-coordinate-omission controls remain intact. A pathwise nonzero deficit, or merely an expected deficit, cannot replace the quantitative pathwise condition. With d=1 the sharp fixed-radius upper bound is 1-exp(-NC^2), which tends to one; it deliberately gives no vanishing-success claim.

This completes the proposed projector bound and its thin-deficit Gaussian endpoint consequence. It does not close every ALG-036 question, settle all sphere-prior algorithms, identify the nondivisible exact extremum, establish historical novelty, or alter ownership/priority. No external write or publication was performed in this task.

## 11. Evidence and reproducibility

The fresh, self-authored `controls/check_thin_deficit.py` exercises complex-to-real coisometry/identity normalizations, nonuniform and zero leverage, the concavity formula, fixed-radius block equality, independent numerical integration/Monte Carlo diagnostics, finite sphere inclusion-exclusion, stopping/posterior updates, and the norm-window/critical-limit calculations. It does not load or run a historical program and makes no network requests.

Fresh controls returned PASS: 19 exact complex projectors and 100 rank-two row checks; 20 floating complex projectors; 120 leverage/Jensen bounds; 125 translated-disk checks; 840 equal-block equalities and 5,400 unequal-block bounds; 35 exact posterior updates across 10 adaptive/stopping paths; 8 Gaussian-cube and 6 sphere diagnostics; 45 critical-window rows, 9 nondivisible-rounding checks, and 20 first-order transition rows. Maximum real-identity roundoff was below 9e-16.

`controls/RESULTS.json` records versions, seeds, counts, values, tolerances and the outcome. Finite computations diagnose implementation and transcription errors; the all-dimension proof above does not rely on their sampling. `SOURCE_MANIFEST.json` records the copied baseline and selection documents and the checked primary source. `MANIFEST.sha256` seals the candidate payload except itself. Independent review must read the proof and rerun the fresh controls before accepting the new scope.
