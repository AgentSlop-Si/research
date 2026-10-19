# NF-03 / ALG-EVEN-PRONY-EXTRA-POLE: polynomial-bit preparation for the accepted large-parameter family

Candidate, 19 October 2026. This is an algorithmic continuation of the existing row, not a new mathematical family. Independent review has not yet been completed.

## 0. Result and exact scope

For every even N=2h>=4, keep exactly the accepted family

    q=exp(2*pi*i/N), m=h+1, L=10N^3+2, t=2^L,
    B(z)=z P_h(z)+t P_(h-1)(z).

Given p>=1, there is a deterministic, fully charged algorithm that prepares all m labeled legal roots, weights and residues to the tolerances needed by the accepted relative-error-2^(-p) application contract in polynomial bit time. One deliberately conservative bound is

    T_prepare = O~((N^8+Np)^3).

Here O~ suppresses polylogarithmic factors. The root-isolation/refinement engine alone has the smaller bound O~(N^9+Np), in the coefficient-access model of the cited theorem. These are different claims. The larger bound above pays for actually generating this family's coefficients, oracle retries, elementary certificate reconstruction, and the exact rational Vandermonde solve.

The exponential grid is eliminated. It is replaced by a published certified all-roots algorithm and m local certificates. The same family still has unscaled moment Vandermonde condition number at least 2^(2N^4), by the accepted review. The paid application still uses O(N^2) rational operations and the accepted conservative bit bound. This result proves polynomial preparability, not useful conditioning, a practical implementation, a fast Fourier transform, minimal h-pole realization, universal t=1, or external novelty.

The algorithms and original checks in this packet are new. No inherited program was executed. The checks do not implement Pan's factorization or the entire Mehlhorn–Sagraloff–Wang root engine; their general certified termination and complexity are invoked as a published theorem.

## 1. Bound inputs and source contract

The following exact local documents were read as inert text and their SHA-256 hashes checked:

- Accepted family proof: `even_pole_family_1656/deliverable/PROOF.md`, SHA-256 `ad435354eceb014f2e28cedc6563181505076fdc1ef9421eba14bb546e06ff2f`, especially Sections 3–7.
- Independent acceptance: `even_pole_review_1709/deliverable/INDEPENDENT_REVIEW.md`, SHA-256 `a30ef2da27595b1749d18724b33a95e54f0fe7513fed92a9b7a98e6133d10667`.

Write P_n as in those sources. We reuse their all-N proofs of legality, the common-Weyl bank identity, conditioning, and application. We do not silently upgrade their exponential preparation implementation.

External algorithmic source: K. Mehlhorn, M. Sagraloff and P. Wang, *From Approximate Factorization to Root Isolation with Application to Cylindrical Algebraic Decomposition*, arXiv:1301.4870v2, https://arxiv.org/pdf/1301.4870v2. The input model is in Section 2.1 (PDF page 6); Theorems 3 and 4 are in Section 2.3 (PDF pages 18–19).

For a monic complex degree-n polynomial with known distinct-root count, put sigma_i=min_(j!=i)|z_i-z_j|, D_i=product_(j!=i)(z_i-z_j) for simple roots, and

    J=sum_i [log_2 max(1,|D_i|^(-1))+log_2 max(1,sigma_i^(-1))].

Theorems 3–4 supply certified all-root disks of radius below 2^(-kappa), at cost O~(n^3+n^2 tau+nJ+n kappa), using absolute coefficient precision O~(n Gamma+J+n kappa). Here tau bounds coefficient logarithms and Gamma bounds root logarithms. Their cost model assumes coefficient delivery at approximately reading cost. Section 2.2 and the proofs include failed certification and precision doubling. We separately pay the actual oracle below. Only the complex, known-root-count theorem is applied; the integer-coefficient specialization is not applied to B.

## 2. Accepted bounds, retained exactly

Set

    R=2^(L+N+1),
    delta=(2R)^[-Nm(m-1)],
    eta=(2R^N)^[-Nm],
    rho=eta(2R)^[-(N-1)],
    K_V=m(2R/delta)^(m-1),
    W_b=m K_V, G_b=2 W_b R^N,
    H_V=m^2(2R)^(m-1),
    a_min=R^[-(m-1)], d_0=delta^(m-1), A_0=(4R)^m.

Every root alpha_i is simple and satisfies

    a_min<=|alpha_i|<=R,
    |alpha_i-alpha_j|>=delta,
    |1+alpha_i^N|>=eta,
    dist(alpha_i,{z:z^N=-1})>=rho,
    |B'(alpha_i)|>=d_0.

The root count is known to be m from the accepted resultant/norm proof, rather than discovered numerically. The polynomial is monic, so the normalization hypothesis is exact. Its chosen complex embedding is prescribed by q=exp(2*pi*i/N).

The logarithmic sizes of R, delta^(-1), eta^(-1), rho^(-1), a_min^(-1), d_0^(-1), A_0, K_V, W_b, G_b and H_V are bounded, respectively, by O(N^3), O(N^6), O(N^6), O(N^6), O(N^4), O(N^7), O(N^4), O(N^7), O(N^7), O(N^7), O(N^4). Products, minima and dyadic rounding of these constants therefore have polynomial-sized exponent descriptions. When explicit dyadic numbers are needed, writing their full numerators and denominators is charged as well.

## 3. An actual cyclotomic coefficient oracle

### 3.1 Symbolic construction with no root-embedding ambiguity

Work first in Z[X,z]. Form R_n(z)=product_(k=0)^(n-1)(z-X^k), then multiply its z^j coefficient by X^[n(n-1)/2-j(j-1)/2]. This constructs P_n(X,z) without dividing by X, reducing modulo a cyclotomic polynomial, factoring an auxiliary polynomial, or choosing a numerical conjugate. The required phase exponents are nonnegative. The X-degree of every coefficient is at most n(n-1)<=N^2; the full integer coefficient l1 norm of P_n(X,z) is at most 2^n.

Thus B(X,z)=sum_(j=0)^m H_j(X)z^j has X-degree at most N^2 and full integer l1 norm at most 2^(L+N)<R. Its H_j coefficients have O(N^3) bits. Dense shifted-array multiplication constructs the two R_n in O(N^4) integer additions of O(N) bits, and inserting t costs at most O(N^6) bit operations. A safe one-time bound O(N^6) is used below. The leading coefficient H_m=1 is set exactly.

Evaluation at the explicitly enclosed transcendental expression exp(2*pi*i/N) selects precisely the desired cyclotomic embedding. The exact mathematical coefficient lies in Q(q); an algebraic-number root oracle is not being assumed.

### 3.2 Certified unit root in cubic bit time

Here is an elementary fixed-point routine for absolute error at most 2^(-Q), Q>=1. All rounds are to nearest multiples of 2^(-f), with coordinate error at most epsilon=2^(-f). Put

    M=Q+40, f=M+ceil(log_2(M+1))+20.

For a=5 and a=239, start with t_0=round_f(1/a), and use

    t_(j+1)=round_f[-t_j (2j+1)/(a^2(2j+3))], 0<=j<M-1.

Sum the M terms exactly on the fixed-point lattice. Each recurrence multiplier has modulus <=1/25, so each term's error is below 2 epsilon. The alternating-series tail is below 2^(-4M). Consequently the dyadic Machin approximation pi_hat=16 sum_5-4 sum_239 has error at most 40M epsilon+20*2^(-4M).

Let x_hat=round_f(2 pi_hat/N). Since N>=4, its error from 2pi/N is at most 21M epsilon+10*2^(-4M), and x_hat lies in [0,2]. Form v_0=1 and v_(j+1)=round_f(v_j x_hat/(j+1)) through degree M. The exact term is x_hat^j/j!. Its recurrence error E_j satisfies E_j<=2E_(j-1)/j+epsilon, hence E_j<=3 epsilon for all j (check j=1,2 separately). Exact fixed-point signed sums of the even and odd terms give cosine and sine approximations.

Their combined rounding error is at most 6(M+1)epsilon. The complex Taylor remainder is at most 2^(M+1)/(M+1)!<2^(5-M); changing the real argument adds at most twice its error if an l1 complex bound is used. Thus the final total error is bounded by

    55(M+1)epsilon+20*2^(-4M)+2^(5-M) < 2^(-Q).

The inequalities are deliberately loose. The O(M) arithmetic steps involve O(Q+log Q)-bit numbers; integer divisors and the temporarily multiplied small integer indices cost O(log Q) additional bits. Schoolbook multiplication and division give O~((Q+1)^3) bit operations and polynomial storage. This also specifies outward error bounds, rather than trusting a library trigonometric function. An exact power of i is not substituted for the general routine in the mathematical algorithm.

### 3.3 Certified coefficient delivery and its charge

On an absolute coefficient-precision request A>=1, choose

    Q >= A+ceil(log_2(64N^2 R))+2,
    f_B >= A+ceil(log_2(128mN^2))+4.

The first also guarantees 2^(-Q)<=N^(-2). Obtain q_hat by Section 3.2. The accepted telescoping bound, or direct differentiation of the H_j, gives

    sum_j |H_j(q_hat)-H_j(q)| <= 4N^2 R |q_hat-q| <= 2^(-A)/64.

Evaluate each H_j at q_hat by Horner's rule. After each complex multiplication, round each real coordinate to the f_B-bit fractional lattice. Add the integer coefficient exactly. Since |q_hat|<=1+N^(-2), an error introduced anywhere is amplified by at most (1+N^(-2))^(N^2)<3. With at most N^2 stages per coefficient, the total l1 error from all rounding is at most 6mN^2*2^(-f_B)<2^(-A)/256. Intermediate magnitudes are below 4R, so their integer parts use O(N^3) bits. The leading coefficient is exactly one.

This delivers, in particular, l1 coefficient error below 2^(-A-1), stronger than the absolute A-oracle requirement. Gaussian dyadic coordinates at a finer lattice are harmless; truncating to any required output lattice with one extra guard bit still meets the absolute error contract. The real-coordinate version of the input convention extends to complex coefficients by treating both coordinates and paying these constant guards.

With S=A+N^3+log(A+2), the actual charge for one entire coefficient vector is

    C_oracle(A)=O~(S^3+N^3 S^2+N^6).

There are O(mN^2)=O(N^3) Horner steps, each on O(S)-bit operands, including the high-precision q_hat input. The one-time symbolic cost need not be repeated.

### 3.4 All oracle retries are paid

Cache coefficient vectors with certified l1 errors. On a request finer than the cache, construct the next power-of-two precision at least two bits above the request. For smaller requests, truncate each cached real coordinate to A+ceil(log_2(m+1))+4 fractional bits and include both the cached error and the truncation error. This preserves the required absolute error and costs only the near-reading cost at the requested precision; do not reread or return the entire high-precision cache for every coarse request. The maximum constructed precision is at most twice the maximum requested precision plus a constant. The sum of cubic/quadratic construction costs over cache doublings is bounded by a constant multiple of the last cost, up to logarithmic baseline terms. Request servicing and coefficient reads are already covered by the root engine's reading-cost model. This prevents a hidden charge for repeated oracle construction and does not assume that unsuccessful certification can be ignored.

## 4. Root-engine substitution and exact ledger

Apply MSW with n=k=m and multiplicities all equal to one. Its geometric quantities satisfy

    tau<=L+N=O(N^3), Gamma<=log_2 R=O(N^3),
    log_2 max(1,sigma_i^(-1))<=D:=log_2(delta^(-1))=O(N^6),
    log_2 max(1,|D_i|^(-1))<=(m-1)D=O(N^7),
    J<=m^2 D=O(N^8).

These bounds are for B itself in the prescribed embedding. There is no passage to a degree-m*phi(N) norm polynomial and no spurious multiplicity from conjugate coincidences.

For a center-accuracy exponent kappa=p+O(N^7), the engine therefore costs

    O~(m^3+m^2 tau+mJ+m kappa)=O~(N^9+Np),

and its maximum absolute coefficient request is bounded by

    O~(m Gamma+J+m kappa)=O~(N^8+Np).

The n*kappa term in the published coefficient-precision bound is retained. It is not silently changed to kappa. Section 5 constructs precisely such a kappa from the downstream tolerances. The theorem includes adaptive factorization, failed certification and refinements; Section 3.4 pays the additional cost of responding to every resulting coefficient request.

## 5. Complete, compact, independently checkable root disks

This section makes the output certificate explicit, while avoiding the old grid. Its m centers come from the certified all-root engine.

### 5.1 Downstream tolerance selection

For epsilon_out=2^(-p), define positive rational tolerances

    v_g=epsilon_out rho/(32m),
    v_b=v_g/[16(2R)^N],
    u_c=v_b/(16m K_V).

Choose r to be a positive dyadic no larger than every entry of

    1/2, 2^(-p-2), a_min/4, delta/16, rho/4,
    eta/[8N(2R)^(N-1)],
    1/(8K_V H_V),
    v_b/(16K_V H_V W_b),
    v_g/[8W_b N(2R)^(N-1)],
    epsilon_out rho^2/(32mG_b),
    d_0/(64mA_0).

Take the largest power of two 2^(-j) below that rational minimum (or a specified power of two within a factor two of it). All these rational comparisons and exponent computations are effective. Their logarithms show log_2(1/r)=p+O(N^7), as an upper bound; a minimum becomes a maximum of these exponents.

Put e_c=d_0 r/(256m A_0). Invoke Theorem 4 to radius below 2^(-kappa), with

    kappa=ceil(log_2(1/e_c))+4 = p+O(N^7).

Round each returned center to a complex dyadic lattice of step 2^(-kappa-3). Its total error from its exact root is less than e_c. The rounded centers w_i have O(p+N^7) bits per real coordinate including their O(N^3)-bit integer parts. Distinct roots cannot round to the same center.

### 5.2 Elementary certificate at each center

Return disks D_i={z:|z-w_i|<r}. They each contain the corresponding root. To produce local checkable certificates independent of the engine's internal clustering representation, request a coefficient vector with l1 error at most

    theta=d_0 r/(4096m A_0).

Taylor-shift that dyadic vector exactly at each w_i. Let a_k=B^(k)(w_i)/k! and let a_hat_k be the computed Taylor coefficient. Since |w_i|<=2R,

    |a_hat_k-a_k| <= theta(1+|w_i|)^m <= E:=theta A_0.

No algebraic equality test or floating-point error model is needed. For any complex rational a define U(a)=|Re a|+|Im a| and L(a)=max(|Re a|,|Im a|). The following entirely rational strict inequality certifies exactly one zero by Rouché:

    U(a_hat_0)+2E + sum_(k=2)^m [U(a_hat_k)+2E] r^k
         < [L(a_hat_1)-E] r.                         (RC)

Indeed U(a_hat_k)+2E bounds |a_k| above, and L(a_hat_1)-E bounds |a_1| below. The lower bound must be positive. No square-root routine is required.

The check always succeeds at these centers. At an exact root alpha,

    |B'(alpha)|>=d_0, |B(w_i)|<=A_0 e_c,
    |B'(w_i)-B'(alpha)|<=m A_0 e_c,
    sum_(k>=2)|a_k| r^k<=A_0 r^2.

These follow from the product/Taylor l1 envelope A_0, exactly as in the accepted proof. Since r<=1/2 and r<=d_0/(64mA_0), the true rational upper-side surrogate is at most

    2 A_0 e_c+2 A_0 r^2 <= 5d_0 r/(128m),

whereas L(a_1)r>=d_0 r/4. Replacing exact Taylor coefficients by their error-enclosed dyadic values changes these two sides together by at most (4m+2)E<d_0 r/512. For m>=3 this leaves a strict positive margin. This proves finite successful certification at the prescribed precision; an inconclusive inequality is not refined indefinitely or accepted.

Check pairwise disjointness by exact squared-distance comparisons of the rational centers against (2r)^2. Root separation and e_c<r imply center distances >=delta-2r>2r, so these checks succeed. There are m disjoint certified one-root disks for a degree-m polynomial, proving complete coverage and absence of duplicate roots.

### 5.3 Labels, nonzero disks and legal denominators

Label the first batch by lexicographic order of the exact rational pairs (Re w_i,Im w_i); this is a computational convention, not an order on exact algebraic roots. Each root's mathematical identity is the prescribed q embedding, B, and its disk. A radical representation is not required.

For subsequent refinements, match new centers to old centers within delta/2. Same-root centers are at distance at most r+r'<=delta/8; different-root centers are at distance at least 7delta/8. Thus the matching is unique, can be done by O(m^2) exact squared comparisons, and preserves labels even when two exact roots have equal real parts. Do not independently re-sort each refinement and presume its labels remain unchanged.

Every point z in a returned disk is within 2r of its root. The selected r implies |z|>=a_min/2, distance from the forbidden set at least rho/2, and

    |1+z^N| >= eta-N(2R)^(N-1)*2r >= 3eta/4.

Here |z|<=2R and the ordinary telescoping power bound was used. In particular all rounded centers are nonzero and every denominator needed downstream is legal with a certified positive margin. These are formal certificate bounds; no unresolved numerical test of whether a denominator is zero is left over.

### 5.4 Certificate work

Write K=p+N^7. The additional coefficient request has A_cert=O(K). The compact centers, r and error enclosures have O(K) bits. An exact Taylor shift at one center costs O(m^2) rational operations; across m centers this is O(N^3). Because all inputs are dyadic and powers have degree at most m, operands can use a common power-of-two denominator with O(NK) bits; no generic exponential denominator-growth estimate is used. Exact rational (RC) evaluation and all disk comparisons fit a conservative O(N^7 K^2) schoolbook bit bound. This includes forming the r powers and writing the O(N^2) Taylor-certificate numbers. It is deliberately looser than a tightly optimized certificate routine.

## 6. Weights, residues and endpoint constants are paid

Use the centers w_i in V_tilde[k,i]=w_i^k, 0<=k<m. Approximate each c_k=q^[k(k-1)/2] within u_c by the same certified q routine, with its O(N^2) phase exponents paid. Use the fixed-point monomial Horner recurrence from Section 3.3 and round the final real coordinates to O(K)-bit dyadics, with K=p+N^7, spending at most half u_c on evaluation and half on final rounding. Do not pass unrounded exact q_hat powers into the linear system. The root errors e<=r meet the Section 5.1 tolerances. The accepted inverse-perturbation argument gives

    ||V_tilde^(-1)||_2<=2K_V,
    ||beta_solve-beta||_2<=2K_V[m u_c+H_V e W_b]<=v_b/4.

Solve the Gaussian-rational system exactly with row pivoting and fraction-free elimination (or an equivalent reduced-fraction method with the usual minor representation). Round each real and imaginary coordinate of beta_solve within v_b/(8m); the vector rounding error is below v_b/4, so ||beta_tilde-beta||_2<=v_b/2<v_b.

To spell out operand sizes: all matrix entries and moments can share a power-of-two denominator with O(NK) bits; after clearing it, every input integer has O(NK) bits. A minor of order at most m has O(N^2K+N log N) bits by its determinant expansion. Fraction-free elimination with nonzero pivots keeps entries within the corresponding minor bounds. Gaussian integers can be divided exactly using their real and imaginary parts with quadratic schoolbook cost. O(N^3) arithmetic steps therefore fit O~(N^7K^2) bit operations. Allowing O~(N^9K^2) instead would also leave the headline bound unchanged. An ordinary unpivoted floating-point solve is not justified here.

Next form gamma_i=beta_tilde_i(1+w_i^N) exactly and round each real coordinate within v_g/8. Before rounding, the accepted estimate gives

    |gamma_i-gamma_i_exact|
      <=2(2R)^N v_b + W_b N(2R)^(N-1)e <= v_g/4.

The rounding adds less than v_g/4, so the final residue error is below v_g. In this display gamma_i_exact denotes beta_i(1+alpha_i^N). Keep zero weights/residues; deciding exact vanishing is unnecessary. The accepted rank bound still guarantees at least h nonzero exact weights.

Construct the endpoint diagonal phases and 1/sqrt(N) to error epsilon_out/(64N), paying the same phase routine and a rational square-root bisection or exact integer-square-root procedure. Their cost is polynomial and bounded by the already stated preparation charge. Store dyadic root centers, weights, residues and endpoint constants at the proved tolerances, with corresponding root certificates and labels.

## 7. Complete preparation ledger

Let

    K=p+N^7, A=N^8+Np=N K.

The occurrence of O~ in the maximum requested precision only adds polylogarithms after taking the fixed powers below. The separate charges are:

- Symbolic X-coefficient construction: O(N^6), once.
- Certified MSW root engine, including its certification retries: O~(N^9+Np).
- Real coefficient delivery through the doubling cache: O~(A^3+N^3A^2+N^6).
- Compact-center conversion, m local certificates, disk labels and margins: O~(N^7K^2), conservatively.
- Moments, exact rational Vandermonde solve, rounded weights/residues, endpoint constants: O~(K^3+N^7K^2), conservatively.
- Output: at most polynomially many bits, already paid in these charges. A certificate need not print enormous dyadic denominators in decimal; numerator-plus-binary-exponent encoding is permitted, with full-size materialization charged whenever used arithmetically.

Since K>=N^7, every listed term is bounded by O~(A^3). This proves

    T_prepare = O~((N^8+Np)^3)

with polynomial working storage. The conservative exponent is a consequence of choosing an elementary cubic-bit trigonometric oracle, not a lower bound or an optimized complexity claim. In particular, it is false to present O~(N^9+Np) as the fully charged result of this packet.

All algorithms have a stated stopping condition: fixed term counts for scalar generation, exact coefficient error budgets, the MSW certified stopping theorem with known root count, finite local certificate checks whose margin is proved above, and exact nonsingular elimination. There is no random retry or exhaustive search left in the construction.

## 8. Application and conditioning do not improve

Prepared constants meet stronger versions of the accepted Section 7 tolerances:

    e<=rho/2, e<=epsilon_out rho^2/(16mG_b),
    residue error<=epsilon_out rho/(16m).

Thus the same signed-shift bank perturbation bound and endpoint/normalizer rounding argument apply unchanged. For b-bit dyadic input, the final relative output error is below 2^(-p). Application uses the accepted first-order signed cyclic recurrence, all m branches and both paid endpoint diagonals:

    O(N^2) rational operations,
    O(N^6(p+b+N^7)^2) bit operations,

in addition to this separately charged one-time preparation. The proof has not turned pole coordinates into Fourier coordinates at no cost.

The accepted coefficient argument still yields kappa_2(V)>=2^(2N^4) for this unscaled family. Polynomial bit complexity is compatible with exponentially large condition numbers when their binary logarithms are polynomial. Nothing here improves that conditioning, proves a useful floating-point scheme, or establishes a subquadratic application.

## 9. Evidence and remaining boundary

The new control script in `controls/check_preparation.py` tests the fixed-point unit-root generator, the coefficient construction/oracle, the all-center Rouché check with positive and negative cases, label matching, the logarithmic precision ledger, and an actual N=4 instance with three independently recertified disks. Numerical Newton candidates are used only in that finite N=4 diagnostic; every retained disk there is subsequently checked using exact Gaussian rationals. They are not substituted for the general MSW engine in the proof.

The exact test inventory, results and run hash are in `evidence/CHECK_RESULTS.json` and `evidence/RUN.txt`. These controls corroborate implementation details and finite cases. The all-N theorem is the argument above plus the cited certified algorithm, not a finite experiment.

Proposed existing-row action after independent review: close the exponential-versus-polynomial preparation bottleneck for this specific accepted large-t family. Retain useful conditioning, practical preparation/execution, h-pole optimality and t=1 as open. No external write, row mutation, repository commit or historical executable run is part of this packet.
