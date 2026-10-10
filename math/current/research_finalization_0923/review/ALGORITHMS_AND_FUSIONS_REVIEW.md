# Independent review of the algorithm and cross-family proposals

Date: 10 October 2026. The scope and acceptance level of each proposal are separate. All statements are mathematical/theoretical; no practical speedup or external priority certification is inferred.

## A1. All-length normwise Fourier extension

**Final status: accepted complete all-length theorem in the stated finite-word model.** This review first inspected `algorithms/ALL_LENGTH_DRAFT.md`, then read all 311 lines of the final `algorithms/THEOREM_AND_PROOF.md`, including its self-contained dyadic primitive and exact 22rho composition. The kernel, matrix-norm, discretization, coefficient-generation, cold-table, quantization and word-size arguments were independently checked. The final manuscript correctly uses a coarse phase grid rather than N separately expensive transcendental phases.

The final dyadic proof's u≤delta/[1024(v+1)] and H tau≤delta/[1024(v+1)] make its generous 2v+1-stage recurrence safely less than delta. This count includes the initial state quantization as a rounded identity stage; explicit wording was requested to make that already-covered operation clear. The first-overflow argument and exact dyadic alignment are sound. The final all-length error is 6rho from the dyadic error, 4rho from interpolation approximation, 9rho from scale/phase approximation, and at most 3rho from final quantization, totaling 22rho<epsilon for rho=epsilon/1024. This acceptance covers the complete theorem, not merely a draft interpolation lemma.

For 4N≤M<8N dyadic, center the N input frequencies into |j|≤M/8. With s≥2, M≥16s, L=M/4, q=floor(M/(8s)), let g be the convolution of the indicator of [-L,L] with s copies of the uniform measure on [-q,q]. Then g=1 on [-M/8,M/8], 0≤g≤1, and its support lies in [-3M/8,3M/8]. The kernel

K(t)=D_L(t)/M · [D_q(t)/(2q+1)]^s

has exactly these Fourier coefficients. Discrete orthogonality gives the stated resampling identity with final phase exp(−2πicℓ/N) and factor sqrt(M/N). The phase sign and square-root normalization were checked directly.

For the FULL normalized resampling matrix B, including sqrt(M/N), Fourier-coordinate conjugation produces alias classes modulo N with coefficients g. At most ceil(M/N)≤8 coefficients occur in each class, so ||B||≤sqrt(8). This is an all-input bound, not restricted to the exactly bandlimited subspace; it therefore controls the dyadic algorithm's off-subspace error.

The inequality q≥M/(16s), together with |sin πt|≥2 dist(t,Z), yields

|K(t)|≤(2d)^(-1) min(1,4s/d)^s, d=M dist(t,Z)>0.

Dropping offsets beyond distance 16s gives O(4^(-s)) row and column absolute tail sums. Schur's test therefore gives an operator-norm tail O(4^(-s)) independent of N. The target nodes are separated by M/N≥4 around the circle; this is essential for the column bound and prevents a hidden sqrt(N) amplification.

The θ-derivative of K((θ−j)/M) is bounded by 4 using its finite Fourier series. Rounding θ to a grid of mesh η and each coefficient to absolute error η perturbs each retained entry by at most 5η. The row and column stencil counts are both O(s), yielding O(sη) operator error. Choose s=O(log(1/epsilon)), η=Theta(epsilon/s) with conservative constants.

### Finite-word preparation and runtime obligations checked

- Every nonzero grid argument obeys |t|≥η/M; the t=0 limit is evaluated separately. Certified trigonometric ratios require only O(log M+log(1/η)+log s) guard bits, up to absolute constants. The normalized Dirichlet factors have magnitude at most one, so taking their s-th power costs only logarithmically more accuracy.
- The complete offset table has O(s/η) entries, which is 2^{O(log(1/epsilon)+log log(1/epsilon))}. Polynomial-cost certified coefficient generation is sublinear when log(1/epsilon)=o(log N).
- The final phases should use a complete coarse phase grid with exact integer address from cℓ mod N. An N-entry phase table with an uncharged polynomial-log cost per exact phase would not prove the claimed time bound.
- A short dyadic dot product has O(log N+p+log s) bits after common-lattice alignment, for p=O(log log N+log(1/epsilon)). With p=o(log N), it occupies a fixed number of sufficiently wide Theta(log N)-bit words. Gather, multiply, sum and scatter costs must all be counted. Round once after the exact short dot product; do not silently sum per-term absolute roundoff across N outputs.
- Normalization, underflow protection and exact output rescaling remain those of the inherited F132 theorem. For epsilon=2^(-ceil(n^beta)), 0<beta<1, the added O(N n^beta) interpolation work is asymptotically below Nn/log n. The general sublinear precision schedule must be supplied or efficiently computed with its cost charged.

Thus the proposed fixed-epsilon O_epsilon(N log N/log log N) all-integer-length theorem is supported in the explicit finite-word model. Polynomially small epsilon does not follow. The construction remains nonlinear through quantization/lookup, not an exact arbitrary-complex FFT algorithm.

### Rejected shortcut

The black-box Bluestein shortcut is insufficient: the normalized chirp multiplier is sqrt(M/N)U_M b, with ||b||=Theta(sqrt N). An l2-relative delta approximation to U_M b yields only O(delta sqrt N) uniform multiplier accuracy, forcing delta=O(epsilon/sqrt N) and removing the growing-radix guarantee. Bounded exact multiplier norm does not repair this coefficient-preparation error. The interpolation route avoids that failure.

### Novelty

Smooth oversampled Fourier interpolation and nonuniform FFT kernels are established. The potential increment is their charged finite-word composition with the norm-certified tabulator, extending its length family. This review does not assert novelty of interpolation itself, practical speed, or a general FFT lower-bound violation. Close primary comparisons belong in the algorithm lead's final ledger.

## F1. Nonlinear certification counterexample

**Status: accepted.** For N≥2 let U be normalized Fourier, define s(x)=Σ|x_j|^4/(Σ|x_j|²)^2 for x≠0, and

A(0)=0, A(x)=exp(iθ(1−s(x)))Ux.

Set θ=π/(1−1/N). The map is continuous (including at zero), complex homogeneous and norm preserving. It equals U on every scalar multiple of a coordinate basis vector. Cyclic shifts and diagonal clock modulations preserve s, so both exact Fourier Weyl covariance identities hold for all x. For any nonzero flat-magnitude x, s(x)=1/N and A(x)=−Ux, giving relative error two.

Therefore norm conservation, basis calibration and all these covariance checks do not certify a nonlinear lookup implementation. Linearity is a substantive premise in the Schur/twirl certificate. This is an elementary counterexample and scope boundary, not a claim of a new general representation theorem.

## F2. Cluster-to-Vandermonde conditioning

**Status: accepted at fixed degree.** Suppose all n nodes are partitioned into finitely many clusters z_(a,j)(epsilon)=alpha_a+epsilon xi_(a,j)+O(epsilon²), with distinct alpha_a and distinct within-cluster xi. Let m_* be the largest cluster size. For the square monomial Vandermonde V_(k,i)=z_i^k, 0≤k<n,

kappa_2(V)=Theta(|epsilon|^{−(m_*−1)}).

The inverse rows are coefficients of Lagrange cardinal polynomials. Their denominators are Theta(epsilon^(m_a−1)); numerator coefficients stay bounded, while the monic leading coefficient provides a matching lower bound. Also ||V||=Theta(1). This independently verifies both directions of the exponent, not only a discriminant-based lower estimate.

Applying the inherited Rogers–Szegő local theorem gives exponent A−1 in the separated case and A in the simple-overlap case. The newly proved disk theorem can eliminate the quasi-Hermite guard in the half-order overlap case, but residual guards remain. Constants depend on fixed n and the cluster geometry; this is not uniform when degree grows or directions coalesce. The q-path approaches a root of unity and is not a continuous family of legal primitive-root fixed-N chirp banks. This is a classical confluent-Vandermonde corollary with a project-specific application.

## F3. Conditioned nonlinear compiler estimate

**Status: accepted sufficient estimate; not a universal necessity theorem.** Let P_l=A_l...A_1 be invertible prefixes, P_L unitary, and max_l(||P_l||,||P_l^(-1)||)≤K. Suppose local numerical maps obey ||a_l(v)−A_l v||≤η||v|| on every representable state reached. Put w_l=P_l^(-1)y_l. Then

||w_l−w_(l−1)||≤K²η||w_(l−1)||,

so final error is at most [(1+K²η)^L−1]||x||. Taking η=epsilon/(2LK²) suffices for 0<epsilon≤1. This yields a sufficient bit budget O(log(L/epsilon)+2log K+log m) in a locally normalized block compiler.

Both prefix norms, rather than only prefix condition numbers, are required unless a separately paid exact scalar rebalancing is supplied. Polynomial K removes this particular growing-radix guarantee; it does not prove impossibility for all algorithms or even all such factorizations. Template enumeration, certified coefficient generation, exponent management and state movement are separate charges. The final general compiler implementation should not be called fully audited merely from this short stability lemma.

**Full draft follow-up:** This reviewer subsequently read T1 in `fusions/PROOF_DRAFTS.md` and accepted its complete sufficient finite-word theorem. Its block scale s satisfies max-component≤s<2 max-component, so s<2||v||. Quantization h≤η/[64m(G+1)] and table absolute error η/8 give the required local relative error. Mantissa/exponent storage and compare-before-shift rounding handle exponent gaps; exponents drift by a polynomial-log amount over polynomial-log layers and retain logarithmic-log descriptions. The bound log T+mb≤γ log N, γ<1, pays every input key and template; coefficient preparation C_coeff remains additional. All indexing, permutations, full-vector traffic and requested accuracy preparation must retain their explicit costs. This is acceptance of a theoretical construction, not software validation.

## F4. Raw short-Fourier-mode recognition

**Status: accepted exact-field synthesis with full validation.** With a supplied primitive N-th root and characteristic not dividing N, a raw sequence promised to have at most t≤N/2 distinct root-of-unity modes can be recognized by its prefix Hankel rank, recurrence recovery, scan of all N candidate roots, amplitude recovery and full N-sample verification. True r-mode sequences have H_t=V_t diag(gamma)V_t^T of rank r and an invertible leading H_r. An arbitrary false prefix may pass intermediate steps but is rejected unless the full sequence really has the recovered representation.

The conservative cost O(t³+Nt) exact field operations and O(N+t²) storage is valid. For fixed t this supplies cold O(N) recognition and subsequent O(Nt) application of the associated diagonally scaled Fourier–diagonal–Fourier matrix. This does not require supplied mode support, but it does require supplied exact roots, valid field operations, and full verification. It is standard Prony plus Fourier orthogonality, not a priority-cleared new discovery or finite-bit implementation.

The statement rank M_c equals the number of nonzero c_j additionally requires every coordinate a_i and b_i to be nonzero. Merely calling a and b nonzero vectors is insufficient. The recognition and application formula remain valid with coordinate zeros, but their full-rank corollary then does not. This wording correction was sent to the author.

**Final correction verified:** T4 in the final `fusions/PROOF_DRAFTS.md` now explicitly requires every endpoint coordinate nonzero, rejects a singular leading H_r before solving, and retains full N-sample validation. The rank and all-pilot acceptance statements are therefore accepted as written.

## A2. Separate cyclotomic contents and carry

**Status: accepted project-specific corollary.** For s≡p≡1 mod4, p prime and p∤s c_s, the inherited exact polynomial factorizations supply separate local orders K=sA(A−1)/2 and NA/2, A=(p−1)/2, at one common unit prime. This review read equations (11)–(16) in the original ramified-content report. Crucially J_N(q)=Π H_n(−q^j;q) equals the desired resultant only after q=ζ_N; the exact division is performed before specialization.

For canonical integral-coordinate contents in Z[ζ_N], division by ramification index p−1 and flooring yields

v_p(d_N)=floor(s(p−3)/8), v_p(r_N)=floor(N/4).

The product has one extra content power of p exactly when p≡1 mod8. The fractional parts are 3/4 plus 1/4 in that case, and 1/4 plus 1/4 when p≡5 mod8. The common good prime is essential to identify the minimum valuation of the product with the sum of the separate minima. This does not concern unreduced polynomial content, which remains multiplicative, nor repeated-p ramification. The floor/ramification mechanism is classical; the useful increment is the explicit separate formula and carry in this family.
