# Structured fusion second pass: proved results and strict boundaries

Date: 10 October 2026. No supplied program was executed, imported, compiled, or AST-parsed. Existing proof documents and primary papers were read as inert text. New scripts in this directory, if any, are independently written falsification controls, not proof substitutes or runtime evidence.

## Result map

- S1 strengthens FUS-04 by giving a paid, scale-invariant prefix-conditioning interface.
- S2 strengthens FUS-05 on dyadic lengths: raw orbit-weight recognition costs O(N log(t+2)+t²), while application remains O(Nr) per new vector. Recognition speed is not application speed.
- S3 strengthens FUS-06 from one condition-number exponent to the entire singular-value exponent profile, with explicit fixed-degree inverse bounds.
- S4 closes a useful FUS-07 special case: certified near-periodic inputs need no residual transform at all.
- S5 extends FUS-08 to any finite family of nonlinear certification probes. It is an impossibility statement about black-box certification without function-class restrictions, not an FFT lower bound.
- S6 combines the published HIKP pointwise sparse-FFT contract with the already-proved centered interpolation kernel. It gives all-integer-length O(N) dense output at F016's weak accuracy scale in an inherited ideal-arithmetic model. The interpolation/rounding transfer is proved separately from the sparse engine's numerical assumptions.

These are complete mathematical propositions, not worldwide novelty certifications. Classical mechanisms are identified explicitly.

## S1. Paid dyadic balancing of intermediate prefix norms

Let A_L...A_1=U be unitary on C^N and P_j=A_j...A_1. Suppose invertibility holds and a charged certificate supplies numbers a_j,b_j>0 with

    ||P_j||₂ ≤ a_j,   ||P_j⁻¹||₂ ≤ b_j,   a_j b_j ≤ Kappa.

For j=1,...,L−1 choose a dyadic s_j=2^{e_j} in

    sqrt(b_j/a_j) ≤ s_j < 2 sqrt(b_j/a_j),

and set s_0=s_L=1. Define A'_j=(s_j/s_{j−1})A_j and P'_j=s_jP_j. Then the final product remains U and

    max_j max(||P'_j||₂, ||(P'_j)⁻¹||₂) ≤ 2 sqrt(Kappa).

Indeed s_j a_j<2sqrt(a_jb_j), while b_j/s_j≤sqrt(a_jb_j). The endpoints have norm 1. Thus the local-error compiler of final_v2 T1 applies with K=2sqrt(Kappa), and uniform implemented layer error

    eta = epsilon/(8 L Kappa)

gives final relative l2 error at most epsilon for 0<epsilon≤1. The sharper nonuniform product condition remains

    product_j (1+||P'_j⁻¹||₂ ||P'_{j−1}||₂ eta_j) − 1 ≤ epsilon.

The scale choice can be made from certified dyadic envelopes by integer exponent comparisons; it does not require a transcendental square-root oracle. One can instead supply integers e_j whose two required inequalities are certified directly. Scale application is an exact mantissa/exponent shift. Charge certificate discovery C_env, coefficient preparation C_coeff, and every O(N) layer gather/scatter. If exponents and coefficients fit the stated finite-word contract, the total is

    O(NL + N^gamma polylog N + C_env + C_coeff),

under the original numerical-template/key-width budget. Distinct scaled numerical templates must be counted: in the worst case at most L times as many as before. Alternatively implement dyadic scalings as separately charged diagonal layers and keep an explicit error ledger. No free SVD, norm oracle, root preparation, or routing is introduced.

Boundary: this repairs the condition-number-only hypothesis only when certified scale information is supplied or computed and paid. A_j=N^a I followed by N^(−a)I has prefix condition number 1 but unbalanced prefix norm N^a; it illustrates why omitting the rebalancing is invalid. The balancing result is elementary numerical linear algebra and does not create a new lower bound.

## S2. Fast certified dyadic recognition of raw q-Weyl orbit weights

Let N be a power of two, E a field of characteristic not dividing N, and q a supplied primitive Nth root. Let a,b be supplied vectors with all coordinates nonzero. Count exact field operations and O(log N)-bit index operations separately from bit complexity. Reading data and constructing all powers of q costs O(N), included below. For raw c∈E^N and supplied cap 1≤t≤N/2, define

    M_c = diag(a) F_q diag(c) F_q diag(b),   (F_q)ij=q^{ij}.

There is a deterministic exact recognizer accepting precisely

    c_j = sum_{ell=1}^r gamma_ell q^{u_ell j},
    r≤t, gamma_ell≠0, distinct u_ell modulo N,

in O(N log(t+2)+t²) work and O(N) words. It returns the modes and amplitudes on acceptance. A fresh x can then be mapped to M_c x in O(Nr+N) work, writing all N outputs. For J fresh vectors, total work is

    O(N log(t+2)+t²+JN(r+1)).

### Recognition proof and full rejection ledger

Run quadratic Berlekamp–Massey on c_0,...,c_{2t−1}, obtaining C(z)=1+C_1z+...+C_rz^r. Reject if its length is greater than t. For a true r-mode sequence, the r×r moment Hankel block is V diag(gamma)V^T with square invertible Vandermonde V; consequently its minimal recurrence is exactly

    C(z)=product_ell (1−q^{u_ell}z).

The first 2t samples determine that recurrence under the promise, including cancellations at early samples. Run length-N input-support-pruned FFT on the coefficient vector of C. Its values C(q^v) for all v cost O(N log(r+2)). Collect roots and reject unless exactly r distinct allowed grid roots occur and C has degree r. Put lambda_ell=q^{u_ell}=q^{−v_ell} for each root q^{v_ell}. When r=0, scan every raw coordinate and accept only the all-zero array.

For r>0, form

    A(z)=C(z) sum_{j=0}^{r−1} c_j z^j mod z^r,
    gamma_ell=−lambda_ell A(lambda_ell⁻¹)/C'(lambda_ell⁻¹).

Quadratic polynomial multiplication and Horner evaluation at all r roots cost O(r²). Reject zero denominators or zero amplitudes. This is the partial-fraction formula for sum gamma_ell/(1−lambda_ell z). Finally synthesize every candidate c_j with one sparse-input FFT on the discovered frequency/amplitude array, costing O(N log(r+1)), and compare all N coordinates. Thus every accepted representation is fully verified; arbitrary off-promise inputs or misleading prefixes reject within the same budget. Root search and all-entry verification are both charged.

The pruning bound follows by input-parity recursion: at depth d there are at most min(2^d,s) active subproblems of length N/2^d for a support of size s. The total combine work is O(N sum_d min(1,s/2^d))=O(N[1+log(s+1)]). Depth-first space is O(N). This is classical FFT pruning.

### Evaluation identity and scope

Character orthogonality gives

    (M_c x)_i = N a_i sum_ell gamma_ell b_{−i−u_ell} x_{−i−u_ell},

with subscripts modulo N. The second F is not an inverse. This is r weighted antidiagonal permutations and costs O(Nr). Moreover

    rank(M_c)=#{j:c_j≠0}.

One nonzero Fourier mode of c already makes M_c full rank, while evaluation costs O(N). The fact that recognition now costs O(N log t+t²) does not prove O(N log r) application: a general sparse cyclic convolution of a dense new vector is a different operation. The safe choice is min of O(Nr) direct application and an ordinary O(N log N) FFT route. For non-dyadic N the accepted earlier O(Nt+t³) recognizer remains available; this statement makes no unsupported all-length pruning claim.

No numerical stability follows from exact field recognition. Roots, field construction, divisions, equality tests and finite-bit realizations retain their stated model costs. The result is a classical Prony/pruning fusion with a useful raw-input interface, not a standalone novelty claim.

## S3. Every singular-value exponent of first-order clusters

Fix n. Partition distinct nodes into clusters of sizes m_a, with

    z_{a,j}(epsilon)=alpha_a+epsilon xi_{a,j}+O(epsilon²),

where the centers alpha_a are pairwise distinct and the directions within each cluster are pairwise distinct. Work along a fixed admissible complex path epsilon→0. Let V_{k,(a,j)}=z_{a,j}^k, 0≤k<n. Sort the multiset

    E = disjoint union over a of {0,1,...,m_a−1}

as e_1≤...≤e_n. For singular values in decreasing order,

    sigma_i(V)=Theta(|epsilon|^{e_i}),   i=1,...,n.

All constants are allowed to depend on n, centers, directions and uniform remainder bounds. This is not a uniform growing-degree theorem.

### Proof by bounded confluent factorization

Write theta_{a,j}=(z_{a,j}−alpha_a)/epsilon. Let B_a have rows theta_{a,j}^k, k=0,...,m_a−1. Each B_a and B_a⁻¹ stays bounded because theta tends to distinct xi. Let B be their block diagonal sum. With v(z)=(1,z,...,z^{n−1})^T, polynomial Taylor expansion is exact. Consequently column (a,k) of V B⁻¹ equals

    epsilon^k v^{(k)}(alpha_a)/k! + O(|epsilon|^{m_a}),

because the terms of order below m_a are exactly interpolated by B_a. Let D have diagonal entries epsilon^k. Then

    V = W(epsilon) D B,

where W(epsilon) tends to the confluent Vandermonde whose columns are v^{(k)}(alpha_a)/k!. It is invertible: a polynomial of degree <n whose prescribed derivatives vanish to orders m_a at all centers is zero. Hence W and W⁻¹ are bounded. Left and right multiplication by uniformly bounded invertible matrices changes each singular value by bounded factors, so the singular-value list is comparable term by term to that of D. This proves the claim.

In particular, ||V||=Theta(1), ||V⁻¹||=Theta(|epsilon|^{−(m_*−1)}), and the determinant order is sum_a m_a(m_a−1)/2. The ordinary discriminant order is twice that last exponent; it does not by itself determine the individual singular values.

### Explicit finite-separation envelope

Suppose |z_i|≤R, distinct-cluster distances are ≥Delta>0, and distances within cluster a lie between d|epsilon| and D_0|epsilon|. Lagrange coefficients give

    ||V⁻¹||₂ ≤ sqrt(n) (1+R)^{n−1}
                 max_a [(d|epsilon|)^{−(m_a−1)} Delta^{−(n−m_a)}].

Indeed each Lagrange numerator has coefficient l1 norm ≤(1+R)^{n−1}, and the Frobenius norm of the inverse bounds its spectral norm. For any node in a largest cluster,

    ||V⁻¹||₂ ≥ [(D_0|epsilon|)^{m_*−1}(2R)^{n−m_*}]⁻¹,

using the leading Lagrange coefficient; take R>0. Together with sqrt(n)≤||V||₂≤sqrt(n sum_{k=0}^{n−1}R^{2k}), these give explicit, conservative condition-number bounds.

### RS application and confluent-coordinate consequence

For guarded separated Rogers–Szegő n=Ad+b local families, there are d clusters of size A and b residual singletons. The exponents are d copies of 0,...,A−1 plus b further zeros. For a guarded one-simple-overlap family, replace one A-cluster and one residual singleton by an (A+1)-cluster; the maximum exponent becomes A. The actual local root/guard theorem must be cited, not inferred from a discriminant.

The scaled confluent coordinates D B gamma are well-conditioned moment coordinates because V gamma=W(D B gamma) and W,W⁻¹ stay bounded. This is a coordinate statement; recovering individual first-order pole weights still requires D⁻¹ and has the indicated worst-case loss. The transformation needs the nodes and epsilon and its cost must be paid. The coordinates do not make singular cyclic resolvents legal: lambda=−z still requires 1−lambda zeta_N^k≠0 for every k. Identically resonant branches are undefined. No claim is made about actual chirp weights necessarily diverging, nor about a continuous fixed-N primitive-root path.

The profile and confluent-coordinate mechanism are classical clustered-Vandermonde analysis; their RS specialization is the package-level application.

## S4. A certified near-periodic early exit

Let N=QM with Q,M powers of two, x a finite dyadic vector, and P the periodic-average projector

    (Px)_{a+tQ}=mu_a=(1/M)sum_t x_{a+tQ}.

Set s=Px,r=x−s,E_s=||s||₂²,E_r=||r||₂²,E=||x||₂². These vectors and energies can be computed exactly with O(N) word operations under bounded O(log N)-bit input and dynamic-range contracts, using a fixed sufficiently wide word multiple. In particular E_s=M sum_a|mu_a|² and E_r=E−E_s; the subtraction is exact, not a floating-point cancellation certificate.

For an efficiently supplied accuracy 0<epsilon≤1, suppose E_r≤epsilon² E. Approximate only the short transform U_Q mu and embed its sqrt(M)-scaled outputs on bins k=M ell; write zero in all other bins. If the short output's squared error after scaling is at most epsilon²E−E_r, the full output has error at most epsilon||x||₂. The exact squared error is the sum of that short error and E_r, by disjoint Fourier supports. No transform of the residual is needed.

A safe strictly interior rule avoids demanding an exact short FFT when the remaining budget is zero: if E_r≤epsilon² E/2, call the short transform at relative tolerance epsilon/2 (a dyadic choice whenever epsilon is dyadic), since E_s≤E. Then total squared error is at most epsilon²E. Handle x=0 separately by writing zeros. All input reads, projection, energy checks, short transform and N output writes are charged:

    O(N + T(Q,epsilon/2)).

For Q bounded or polylogarithmic, the result is O(N) under the corresponding charged short-transform routine. For inputs failing the residual-energy test, use the existing general approximate algorithm; the recognizer never falsely asserts a small residual. This is a classical approximation corollary and an explicit useful accepted family, not a worst-case FFT improvement.

## S5. Finite nonlinear probes remain insufficient

Let G be the finite projective Weyl group acting unitarily on C^N, N≥2. Let a finite set of nonzero probes be given, including all coordinate vectors if desired. There exists a continuous complex-homogeneous, norm-preserving map A:C^N→C^N satisfying exact Fourier Weyl covariance, agreeing with U_N on every probe and every Weyl/complex-scalar orbit of those probes, but having relative error 2 at some nonzero vector.

Proof. Work on complex projective space with its usual compact metric. The union Z of the finitely many projective G-orbits of the probes is finite. Choose a projective point p outside Z, and let O=G p; the two finite invariant sets are disjoint. With invariant projective metric (average any metric over G), the continuous invariant function

    f([x])=dist([x],Z)/(dist([x],Z)+dist([x],O))

is zero on Z and one on O. Set A(x)=exp(i pi f([x]))U_Nx for x≠0, A(0)=0. All claims follow; continuity at zero uses ||A(x)||=||x||. At O, A=−U_N. The same construction accommodates any finite collection of test endpoints used in an adaptive test transcript, by including their Weyl orbits in Z. It does not imply a probabilistic lower bound against a fixed restricted algorithm class.

Thus adding finitely many additivity probes to covariance, norm and basis tests does not certify arbitrary continuous homogeneous nonlinear maps. A positive certificate needs a proved function class, an all-input local-error argument, or other globally controlling assumptions. This extends the elementary FUS-08 negative control and remains classical in spirit.

## S6. All-length linear-output-time weak approximation by sparse transfer

### Precise contract

Fix 0<alpha<1/2 and c>0. Choose a fixed rational beta with alpha<beta<1/2. For every sufficiently large integer N and each fixed x∈C^N independent of fresh randomness, an ideal-arithmetic algorithm returns all N entries y with

    ||y−U_Nx||_infinity ≤ C_alpha N^{−alpha}||x||₂

with probability at least 1−N^{−c}, in O_{alpha,c}(N) work and O_{alpha,c}(N) storage. This theorem inherits the mathematical sparse-FFT arithmetic/filter contract of HIKP Theorem 4.4. It is not a floating-point implementation certificate or a new all-input relative-l2 transform. The new transfer uses certified dyadic interpolation coefficients and proves their error contribution, but it does not silently certify roundoff inside HIKP.

### Published sparse primitive used exactly

Hassanieh–Indyk–Katabi–Price, *Simple and Practical Algorithm for Sparse Fourier Transform*, Theorem 4.4 and Lemma 4.3, provide a dyadic-length sparse output with a squared l∞ bound of the form

    epsilon_0/k · ||X−X_S||₂² + delta²||X||₁²

and failure at most 1/M, in O(sqrt(M k log(M/delta)/epsilon_0) log M) arithmetic work. Here X is the paper's Fourier spectrum and epsilon_0 is a fixed constant. Divide output by sqrt(M) for the unitary convention. By Parseval and ||X||₁≤sqrt(M)||X||₂, the conservative normalized implication is

    ||z_hat−U_M v||_infinity
       ≤ C(k^{−1/2}+sqrt(M)delta)||v||₂.                 (6.1)

The paper's displayed introductory convention is not needed to strengthen this bound. The actual sparse support is at most the routine's work; more explicitly Lemma 4.3 bounds its returned candidate set by 2 d k M/B. No claim of k-sparse output is needed.

Take M=2^{ceil(log₂(4N))}, k a power of two within a factor of two of M^{2beta}, and delta=M^{−D} for a fixed integer D>alpha+4. Then k<M/log M eventually, so the fast regime applies. Sparse work and output support are

    O(M^{1/2+beta} polylog M)=o(N),

and (6.1) is O(M^{−beta})||v||₂. Root, filter and index conventions are those of that published primitive; no l2/l2-to-pointwise implication is substituted.

### Exact centered interpolation and bounds

Embed x_j at signed index j−a mod M with a=floor((N−1)/2), obtaining v with ||v||₂=||x||₂ and support in |j−a|≤M/8. Put z=U_Mv. Let s=ceil(D log₂ M), L=M/4, q=floor(M/(8s)), and

    K(t)=D_L(t)/M · [D_q(t)/(2q+1)]^s,
    D_l(t)=sum_{j=−l}^l exp(−2pi ijt).

As proved in research_finalization_0923/algorithms/THEOREM_AND_PROOF.md §2, the Fourier coefficients of K equal one on the occupied band, are supported in |j|≤3M/8, and lie in [0,1]. Therefore

    U_Nx = D B z,
    B_{ell,k}=sqrt(M/N)K(ell/N−k/M),
    D_{ell,ell}=exp(−2pi i a ell/N).

Let h=16s+1 and retain k=(floor(ell M/N)+j) mod M for j=−h,...,h+1. Call this B_h. Eventually 2h+2<M, so there are no duplicates. The already-proved Schur-tail estimate gives

    ||B−B_h||₂ ≤12·4^{−s}.                              (6.2)

Also |K(t)|≤1, so each retained coefficient has magnitude <3 and

    ||B_h||_{infinity→infinity}≤3(2h+2)=O(log N).        (6.3)

One run returns y=D B_h z_hat. Split error using the exact z:

    y−U_Nx = D B_h(z_hat−z) + D(B_h−B)z.

The first term is bounded pointwise by O(log N)M^{−beta}||x||₂ and the second by (6.2)||x||₂. Since beta>alpha, the sum is O(N^{−alpha})||x||₂. The tail is applied to z, not to an uncontrolled norm of the sparse approximation.

### Sparse scatter and complete cost

Initialize N zeros. For each nonzero coordinate k of z_hat, enumerate target ell whose retained neighborhood contains k. Target centers ell M/N have spacing M/N≥4, so there are O(h) such targets. Enumerate integer ell in the at most three clipped/wrapped intervals

    |ell M/N−(k+jM)|≤h+2,   j∈{−1,0,1},

then test the exact floor/modular retention rule. Rational endpoint rounding uses O(log N)-bit integer division. Every true incidence is found; duplicates from the constant-size interval list are removed or prevented by half-open ownership. The total incidence count is O(S h), where S is the returned sparse support. No dense N-by-h interpolation is performed.

Only O(S h) nonzero contributions and O(S h) active target phases require coefficient preparation. At any nonzero rational argument ell/N−k/M mod 1, distance to an integer is at least 1/(NM). Evaluate sine ratios for D_L and D_q after exact argument reduction to absolute accuracy M^{−D−3} per final retained coefficient, using O(log M) guard bits with a sufficiently large constant factor. At zero use the exact limit (2L+1)/M. Normalized Dirichlet factors have magnitude ≤1; polynomial-time rational interval sine/cosine and square-root algorithms therefore cost polylog M per incidence. Their tiny denominators require only O(log M) additional bits. Power s is computed by repeated multiplication with its O(s) error budget paid. Prepare phase coefficients only on active target rows, at the same accuracy.

On a successful sparse call, ||z_hat||_infinity≤2||x||₂ eventually. Even the crude S≤M bound shows the total coefficient error in any row is at most O(M·M^{−D−3})||x||₂, negligible relative to N^{−alpha}||x||₂. Exact arithmetic accumulation is the declared model; a separate finite-word rounding analysis would be needed for the sparse engine and sums. Per-incidence polylog M work times S=O(M^{1/2+beta}polylog M) remains o(N). Reading x and writing the full array cost O(N), proving the headline.

### High probability and randomness

Repeat an odd constant R=2r−1 number of times independently, with integer r>c+1, and take separate real/imaginary medians at every output. If at least r runs satisfy their all-coordinate bound, the median satisfies the same bound times sqrt(2). Independence gives probability of at least r failed runs ≤2^R M^{−r}≤N^{−c} eventually. O(RN)=O_c(N) dense median/output work is included. Exact uniform sampling on the dyadic index sets is charged; any non-dyadic auxiliary rejection sampling may be capped at a logarithmic-squared trial budget, with its superpolynomially small abort probability added to the failure probability. No fixed deterministic seed is substituted for fresh randomness.

### Meaning for old F016

The dyadic weak-error headline was already a published HIKP corollary. HIKP also explicitly predicts a modest totient-factor extension to general n after Lemma 3.6, although its displayed binning primitive requires B dividing n; this prior all-length discussion further limits any novelty claim. S6 now closes the all-length headline within the inherited arithmetic contract using a complete sparse interpolation transfer. This is a new derivation in this research cycle from classical ingredients, not evidence that the exact all-length corollary was previously printed. F016's Gaussian/Green mechanism may still be separately interesting, but O(N log log N) all-length weak approximation is no longer a compelling novelty headline against this O(N) fusion. Numerical stability and a finite-word implementation remain separate open work. At alpha=1/2 the beta slack disappears and the proof gives no linear-time theorem; this is essential.

Primary link: https://people.csail.mit.edu/haitham/Papers/sFFT.pdf, §4.2, Lemma 4.3 and Theorem 4.4 (PDF pages 8–9). Interpolation proof dependency: research_finalization_0923/algorithms/THEOREM_AND_PROOF.md §2, especially equations (5), (7), (8).
