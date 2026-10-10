# Cross-family proof drafts: charged synthesis, not priority certification

Date: 10 October 2026. Scope: the 178 scoped rows and 144 census families in `novelty_catalogue_0825/merged_catalogue.json`. Every catalogue claim was screened at statement level. Only supporting sources named below received deeper inert-text inspection. No supplied program was executed, imported, compiled, or AST-parsed. The new calculations and proofs below are independent mathematical work. Numbering is internal to this synthesis, not a replacement for the existing manuscript ranking.

## Executive result

The most promising general theory is a **resource-separated compiler**: distinguish (i) how many distinct local maps must be tabulated, (ii) how much precision intermediate conditioning requires, (iii) how much routing and full-vector traffic remains, and (iv) whether verification assumes linearity. Exact ranks alone do not answer any of these four questions.

Three substantial proof packages are developed here: a finite-word local-template compiler; a Rogers–Szegő/Prony collision-conditioning theorem; and a blind, fully verified evaluator for q-Weyl orbit corrections. A sharp nonlinear certification counterexample is also complete. Companion workers supply the new quantitative dyadic cut theorem and guarded arithmetic carry theorem, incorporated by exact reference in `fusion_candidates.json` once their proofs are available.

The mathematical mechanisms behind these combinations are mostly classical. A new-to-this-project synthesis or useful negative theorem is not a worldwide novelty claim.

## T1. Local-energy template compiler with a paid conditioning budget

### Exact model and contract

Let N be the vector dimension and let A_1,...,A_L be invertible complex linear layers with P_j=A_j...A_1, P_0=I, and P_L=U unitary. Suppose

    max_j max(||P_j||_2, ||P_j^{-1}||_2) <= K.

The bound is on the two norms separately. A bound on the condition number alone does not supply it unless a paid scalar rebalancing is given.

Each A_j is a direct sum of blocks of size at most m, with at most T distinct numerical block templates across the entire circuit. Padding smaller blocks with an identity is permitted. All grouping, block addresses, and permutations are supplied or generated in O(NL) work. Optional permutations and scalar diagonal layers may instead be executed directly, but their coefficient preparation, rounding and error are included in the same layer ledger. These optional layers must themselves have O(N) word implementations; calling an arbitrary dense matrix a template is not enough.

Let G bound every template operator norm; G<=K^2 is always a valid, possibly loose choice. The model is an address-capable word RAM with w=C log_2 N bits for a sufficiently large fixed C, constant-word integer arithmetic, shifts, comparison and division. Inputs have O(log N)-bit dyadic descriptions and polynomial dynamic range. Precision is supplied or efficiently computed. L=polylog N and log K, log G, log(1/epsilon)=O(log N). Output is an explicit length-N array of dyadic mantissa/exponent pairs, not an implicit oracle.

Template coefficients must be supplied as certified approximants or produced by a charged procedure. No oracle for arbitrary real constants is free. Let C_coeff be that actual preparation cost.

### T1a: stability of nonlinear local implementations

Suppose each implemented layer a_j satisfies, for every representable v on its legal domain,

    ||a_j(v)-A_j v||_2 <= eta ||v||_2.

Set y_0=x, y_j=a_j(y_{j-1}), and w_j=P_j^{-1} y_j. Then

    ||w_j-w_{j-1}||_2
      <= ||P_j^{-1}||_2 eta ||P_{j-1} w_{j-1}||_2
      <= K^2 eta ||w_{j-1}||_2.

Induction gives ||w_j|| <= (1+K^2 eta)^j ||x||. Telescoping yields

    ||y_L-Ux||_2 <= ((1+K^2 eta)^L-1) ||x||_2.

For 0<epsilon<=1 and eta=epsilon/(2LK^2), the right side is at most epsilon||x||: use (1+epsilon/(2L))^L<=exp(epsilon/2)<=1+epsilon. Nothing in this proof assumes the rounded maps are linear. A finer nonuniform budget replaces K^2 by C_j=||P_j^{-1}|| ||P_{j-1}|| and requires product_j(1+C_j eta_j)-1<=epsilon.

### T1b: a local table attains the layer guarantee

For a nonzero complex block v of length r<=m, let M be the largest absolute real or imaginary component. Choose a dyadic scale s with M<=s<2M. Then every component of u=v/s is in [-1,1] and s<2||v||_2. For zero blocks output zero.

Choose h=2^{-p}<=eta/[64m(G+1)]. Round each real and imaginary component of u to the nearest h-grid point, giving q. There are at most (2/h+1)^{2m} possible padded keys. Write b=2 ceil(log_2(2/h+1)), so the number is at most 2^{mb}.

For every key q and every template B, precompute a dyadic z_B(q) with

    ||z_B(q)-Bq||_2 <= eta/8.

This can be done by certified entry approximants followed by dense finite-word products and rounding. For example O(log(1/eta)+log m) extra fractional bits beyond the coefficient magnitude suffice. All this computation and every table entry are paid.

Return s z_B(q). Since ||u-q||_2<=sqrt(2m)h/2<=mh,

    ||s z_B(q)-Bv||_2
      <= s(eta/8+Gmh)
      < eta ||v||_2.

Direct sums preserve the same relative bound by summing squared block errors. Gathering a block, finding its scale, quantizing and packing its key, reading its table result, scaling and scattering all outputs cost O(m) word operations. Thus a whole layer costs O(N), not O(N/m). This explicitly pays input and output traffic.

A bit-length primitive can be implemented by a paid sublinear universal chunk table if it is absent from the RAM instruction set. Large exponent gaps round to zero by a comparison; they do not require a shift by an unbounded integer.

### Exponent range, table cost and consequence

There is no floating underflow assumption: mantissa/exponent pairs retain all representable block scales. In one layer exponents drift by O(p+log m+log(G+1)); over L=polylog N layers their magnitudes are polylog N, so their binary descriptions use O(log log N) bits. Every coordinate still occupies O(1) words. If a fixed polynomial numerical range is demanded for outputs, an additional final certified global truncation must be charged.

The relevant precision and key width satisfy

    p = O(log m + log(L/epsilon) + log G + 2 log K),
    b = O(p).

If

    log_2 T + mb <= gamma log_2 N, for a fixed gamma<1,

then total cold tabulation is at most N^gamma poly(m,log N), hence o(N) when m=polylog N. Coefficient preparation C_coeff remains additional. Total cost is

    O(NL + N^gamma polylog N + C_coeff),

with O(N+N^gamma polylog N) words. This is an explicit sufficient compiler theorem.

For a circuit admitting L=O(log N/log m) such macro layers, polylogarithmic template diversity, and K=N^{o(1)}, epsilon=N^{-o(1)}, one can choose growing m when the displayed bit budget permits it. With constant K and fixed epsilon, m is of order log N/log log N and the resulting cost is O(N log N/log log N), provided C_coeff is within that cost. F132 supplies a concrete Fourier instance with its own charged root/phase construction.

If this worst-case certificate uses K=N^a for fixed a>0, then its prescribed p is Theta(log N), and this sufficient lookup construction no longer guarantees m tending to infinity. This is not a lower bound on other methods or on individual ill-conditioned circuits; cancellations and sharper directional error analyses may do better.

### Why this is a fusion and what is open

F132 supplies finite-alphabet full-vector relative error and paid cold tables; ALG-055 supplies the role of macro boundaries and condition resets; ALG-080 supplies the warning that a growing-arity unitary gate is not one scalar operation. T1 makes template diversity and conditioning explicit in one contract. Its perturbation calculation and table lookup mechanism are classical. No scalar-arithmetic FFT breakthrough follows. The next concrete check is an eager implementation with tables actually populated at admissible asymptotic radices, followed by model-matched priority comparison.

## T2. Orthogonal residual allocation, with a concrete dyadic projector

Let U be unitary, P an orthogonal projector with an explicitly paid application, and Q=UPU*. Suppose A_s and A_r satisfy relative error bounds eta_s on s=Px and eta_r on r=(I-P)x. Form

    y = Q A_s(s) + (I-Q) A_r(r).

The exact two target pieces lie in orthogonal ranges. Projection cannot enlarge error, so

    ||y-Ux||_2^2 <= eta_s^2 ||Px||_2^2 + eta_r^2 ||(I-P)x||_2^2.

This is a direct Pythagorean theorem, not a new approximation principle. Its useful interface consequence is that the residual may be tabulated at a coarser accuracy when its energy is small, provided decomposition, energy certification, projection and any exact-piece transform are all charged.

For N=QM with powers of two, define

    (Px)_(a+tQ) = mu_a = (1/M) sum_(t=0)^(M-1) x_(a+tQ).

P is the orthogonal projection onto Q-periodic vectors. It uses O(N) dyadic arithmetic, retains a finite-word input contract, and the energy identity is

    ||r||_2^2 = ||x||_2^2 - M sum_a |mu_a|^2.

For a normalized Fourier transform, U_N(Px) is zero outside k=M ell and equals sqrt(M)(U_Q mu)_ell on those bins. Thus Q is just a Fourier-coordinate mask. Compute the short transform with separately chosen accuracy, and explicitly zero those Q bins in the approximate residual output. Their errors are orthogonal.

If eta_s||s||<=epsilon||x||/sqrt(2) and eta_r||r||<=epsilon||x||/sqrt(2), total relative error is at most epsilon. Energies can be certified from exact dyadic sums of squares with O(log N)-bit-sized accumulators up to a constant-factor enlargement of the word, under the stated bounded input description. A rounded energy calculation instead needs directed bounds; subtractive cancellation is not a valid certificate by itself.

This does not claim the short Fourier part is exact over binary numbers, nor that a generic near-structured signal can be decomposed by an exact field recognizer. The periodic projector is a concrete bridge that avoids that mismatch. Standard orthogonal approximation and control-variate ideas are the close antecedents. A useful next experiment is whether adaptive precision meaningfully reduces actual table size or word work; fixed-epsilon asymptotics need not improve.

## T3. Local Rogers–Szegő clusters determine Prony conditioning exactly

### General fixed-degree cluster theorem

Let n be fixed. Suppose n distinct complex nodes have clusters

    z_(a,j)(epsilon) = alpha_a + epsilon xi_(a,j) + O(epsilon^2),

where the alpha_a are pairwise distinct and, in each cluster a, the xi_(a,j) are pairwise distinct. Let m_a be the cluster sizes and m*=max_a m_a. Take epsilon to zero on a fixed admissible path, with uniform bounds in the displayed expansions. Define the square moment Vandermonde

    V_(k,(a,j)) = z_(a,j)^k, 0<=k<n.

Then

    ||V||_2 = Theta(1),
    ||V^{-1}||_2 = Theta(|epsilon|^{-(m*-1)}),
    kappa_2(V) = Theta(|epsilon|^{-(m*-1)}).

Proof: V is bounded because the nodes are bounded, and its constant row gives ||V||>=sqrt(n). The column corresponding to node i in (V^T)^{-1} consists of the coefficients of its Lagrange polynomial

    L_i(z)= product_(j!=i)(z-z_j) / product_(j!=i)(z_i-z_j).

Within cluster a its denominator is Theta(epsilon^{m_a-1}); all between-cluster differences stay bounded away from zero. Its numerator coefficients are bounded, giving the norm upper bound. Its leading coefficient is exactly the reciprocal denominator, giving a matching lower bound for any node in a largest cluster. Finite n turns entry bounds into norm bounds without changing the exponent. This proves the theorem.

As a consistency check, the ordinary discriminant has order

    sum_a m_a(m_a-1)

in epsilon, with leading constant equal to the squared within-cluster Vandermonde products times the nonzero between-cluster differences. The discriminant alone would not imply the smallest-singular-value exponent: the root separation structure is what proves it.

### Application to the guarded RS local theorem

For n=Ad+b, fixed odd d and q(epsilon)=omega(1+epsilon^2)^(1/d), the separated F020 theorem has d clusters of size A at alpha^d=-1 and b isolated residual roots. Its Hermite leading polynomial has simple roots. Under Disc(H_b) Res(z^d+1,H_b)!=0,

    kappa_2(V)=Theta(|epsilon|^{-(A-1)}).

For the one-simple-overlap theorem, the exceptional cluster at -1 has size A+1. With all residual guards and Disc J_(A+1)!=0,

    kappa_2(V)=Theta(|epsilon|^{-A}).

If A=1 in the separated case, no conditioning blow-up is asserted: the exponent is zero. Constants depend on the fixed degree, root and guarded residual data. These are not estimates uniform in growing n.

### Bank interpretation and numerical limitation

The scalar-bank node polynomial is T_m(lambda;q)=(-1)^m H_m(-lambda;q), so lambda=-z and separation magnitudes are unchanged. A moment-to-weight decoder in these first-order pole coordinates therefore has the displayed worst-case sensitivity. It does not follow that the particular chirp weights always blow up: conditioning is a worst-case perturbation statement.

Moreover, at the order-d degeneration, lambda^d=1. If d divides the cycle length N, these limiting nodes are resonant for (I-lambda P)^{-1}. For a normal cyclic shift P,

    ||(I-lambda P)^{-1}||_2 = 1/min_k |1-lambda zeta_N^k|.

Along nonresonant epsilon, an O(epsilon) approach to a resonant node gives an Omega(1/|epsilon|) resolvent blow-up; a zero first-order displacement may be worse. A branch can instead be identically resonant (for example a persistent RS root z=-1 gives lambda=1); its resolvent is undefined, not merely ill-conditioned. Legal first-order banks exclude exact resonance.

Crucial domain boundary: varying q near omega is a local analytic/formal family. It is not a continuous family of primitive roots of a fixed order N, so this theorem cannot be sold as a fixed-N legal chirp-bank path. Its role is to connect the algebraic local theorem to Prony numerics and explain why exact minimal pole count is not a stability certificate.

The general Vandermonde mechanism is classical. Batenkov–Diederichs–Goldman–Yomdin and Batenkov–Demanet–Goldman–Yomdin give substantially more quantitative cluster results in related unit-circle models. The possible package-specific increment is the exact RS cluster exponent and its guarded bank interpretation.

## T4. Blindly learn and apply a potentially full-rank q-Weyl correction

### Interface

Work over a field K with characteristic not dividing N and a supplied primitive Nth root q. Let F_(i,j)=q^(ij), Q=diag(q^i), and suppose a known rank-one operator C^(N-1)=a b^T has vectors a,b with every coordinate nonzero, with its coefficient preparation charged. The source q-Weyl family supplies such a,b in O(N) field work. The input is a raw length-N weight vector c, a fresh length-N x, and an integer cap t with 1<=t<=N/2. Define

    M_c = sum_(j=0)^(N-1) c_j Q^j a b^T Q^j
        = diag(a) F diag(c) F diag(b).

The second Q^j is not its inverse. That orientation matters.

There is an exact recognizer accepting precisely those c having at most t distinct q-Fourier modes,

    c_j = sum_(ell=1)^r gamma_ell q^(u_ell j),
    r<=t, gamma_ell!=0, distinct u_ell mod N.

It discovers the modes and amplitudes, verifies all N raw entries, and on acceptance returns every coordinate of M_c x. Total work is O(Nt+t^3) field operations and O(N+t^2) field words; for fixed t this is O(N) cold work and O(N) space. Root and field discovery and field bit complexity are separate. Rejection is a correct failure of this promise, not a claim that M_c lacks another fast representation.

### Recognition proof

Form H_t=(c_(i+j))_(0<=i,j<t) and compute r=rank H_t. For a true r-mode sequence,

    H_t=V_t diag(gamma_ell) V_t^T,

where V_t has full column rank. Hence H_t has rank r, and its leading r-by-r Hankel block H_r is nonsingular by its Vandermonde determinant. The case r=0 is accepted only after verifying every c_j=0.

For r>0, first reject if the leading H_r is singular; a true r-mode input cannot be rejected this way. Otherwise solve

    sum_(j=0)^(r-1) p_j c_(i+j) = -c_(i+r), 0<=i<r.

For a true sequence, p(z)=z^r+sum p_j z^j is exactly product_ell(z-q^(u_ell)). Scan all N root powers, evaluating p by Horner. Reject unless exactly r distinct allowed nodes are found. Solve the r-by-r Vandermonde system for gamma, reject zero or inconsistent coefficients as appropriate, and regenerate every c_j. Accept only if every entry agrees. Every accepted output is therefore certified, including arbitrary false prefixes. True sequences pass by the preceding factorization and uniqueness.

The matrix preparation and elimination cost O(t^3); root scan and full regeneration cost O(Nt); reading both full arrays costs O(N). Storage includes the dense t-by-t pilot and is O(N+t^2), not unconditionally O(N).

### Fused evaluation and rank

Root orthogonality gives

    (M_c x)_i = N a_i sum_ell gamma_ell b_((-i-u_ell) mod N) x_((-i-u_ell) mod N).

This is r weighted cyclic antidiagonal permutations, evaluated in O(Nr) work with all N outputs written. Because F,diag(a),diag(b) are invertible,

    rank M_c = number of nonzero raw weights c_j.

Thus a single discovered mode with nonzero amplitude already yields a full-rank O(N) operator. This is a constructive demonstration that full rank or a count of rank-one summands is not a lower bound on application work when their coefficients share structure.

This fusion removes the previous source's explicit supplied-short-description assumption by combining its exact orbit identity with fully verified Prony recognition (F015/C06/ALG-006/F142). The combination is useful and complete, but its ingredients are classical sparse exponential interpolation and Fourier orthogonality. The operator family remains a strict restricted class: the source proves that even arbitrary c cannot make it equal the full target H_q(C) in the stated gauge. No arbitrary-input Fourier speedup follows.

## T5. Nonlinear Weyl covariance plus norm and basis checks is insufficient

Let U_N be normalized Fourier, N>=2, and define for x!=0

    s(x)=sum_j |x_j|^4 / (sum_j |x_j|^2)^2,
    f(x)=(1-s(x))/(1-1/N),
    A(x)=exp(i pi f(x)) U_N x,

with A(0)=0. Then:

1. A is continuous, including at zero, and A(c x)=c A(x) for every complex scalar c.
2. ||A(x)||_2=||x||_2.
3. A(c e_j)=U_N(c e_j) for every coordinate vector and scalar.
4. A obeys the exact Fourier covariance identities for every cyclic shift and clock modulation and every x. Indeed s is unchanged by coordinate permutations and coordinatewise phases, and the scalar factor therefore commutes with the Fourier intertwining identities.
5. For any nonzero vector with all coordinate magnitudes equal, s=1/N, f=1, and A(x)=-U_N x. The relative error is exactly 2.

Consequently, even zero all-input Weyl covariance residuals, exact basis calibration and exact output norm conservation do not certify a nonlinear algorithm. The linearity premise in F081's Schur/Weyl-twirl certificate is indispensable. Quantized lookup algorithms such as F132 are generally nonlinear, so they require an independent normwise error proof or a verification theorem that explicitly handles nonlinearity.

This elementary counterexample is a falsification gate, not a new FFT lower bound and not a suggested standalone publication claim. A direct additivity test detects this example; passing a finite set of such tests still does not certify arbitrary nonlinear behavior.

## T6. Accuracy-aware minimum cycle-flow compilation

The accepted q-kernel graph has phase multiplicities c_e and a reference complete orbit h_e with equal total multiplicity. Signed corrections obey delta_e=c_e-h_e=f_(e-1)-f_e; every integer solution is f_e=a_e+t. The exact operator identity is unchanged by circulation because product_e(1-q^e z)=1 modulo z^N.

Attach a nonnegative, direction-symmetric paid weight w_e to each unit correction at edge e. It may represent word work, an externally certified log-condition penalty, or a stated linear combination of the two. Then

    J(t)=sum_e w_e |a_e+t|

is minimized by any weighted median of -a_e. Proof: the one-sided slope is the total weight to the left minus the total weight to the right; at a weighted median those slopes bracket zero. An integer weighted median exists because all a_e are integers.

This extends the unit-pass median compiler to a multi-objective cost certificate. It does not itself prove that the chosen penalty accurately describes numerical error. In particular, forward and inverse filters can have different stability costs; then one must minimize a direction-dependent convex piecewise-linear objective instead of using the symmetric weighted-median formula. Coefficient generation, small-kernel application, correction passes and all traffic remain paid. The q-Fourier factorization's intervening reversal and nonconstant diagonal still prevent automatic use of the orbit rewrite.

This is a classical weighted-median corollary, included as a concrete lower-priority implementation avenue, not a substantive new theorem.

## Primary comparisons checked in this pass

- Ryan Williams, *Matrix-Vector Multiplication in Sub-Quadratic Time (Some Preprocessing Required)*: https://people.csail.mit.edu/rrw/mat-vec3.pdf . Theorems 1.1–1.2 treat finite-semiring matrix-vector queries with paid superquadratic preprocessing. Its table-based mechanism is a close classical antecedent, though it is not a finite-complex relative-l2 Fourier theorem.
- Martin Fuerer, *How Fast Can We Multiply Large Integers on an Actual Computer?*: https://arxiv.org/pdf/1402.1811 . Word-level accounting and actual-computer Fourier methods require a model-matched comparison; no direct theorem equivalence is asserted here.
- Nir Ailon, *An n log n Lower Bound for Fourier Transform Computation in the Well Conditioned Model*: https://arxiv.org/abs/1403.1307 . Its linear-gate model is different from nonlinear lookup with paid word addresses; a bound there does not contradict T1/F132.
- Dmitry Batenkov, Benedikt Diederichs, Gil Goldman, Yosef Yomdin, *The spectral properties of Vandermonde matrices with clustered nodes*: https://arxiv.org/pdf/1909.01927 . The clustered-node conditioning mechanism is established prior art; our short fixed-degree proof is a specialized elementary corollary.
- Dmitry Batenkov, Laurent Demanet, Gil Goldman, Yosef Yomdin, *Conditioning of partial nonuniform Fourier matrices with clustered nodes*: https://arxiv.org/abs/1809.00658 . Further close primary comparison for the conditioning application.
- Alexey Kuznetsov, *Using q-calculus to study LDL^T factorization of a certain Vandermonde matrix*: https://arxiv.org/abs/1507.02959 . Known q-factorial/Fourier machinery underlying the exact orbit sources.

These comparisons establish obvious classical overlap, not worldwide priority clearance. They also do not replace the domain workers' deeper RS and dyadic endpoint literature comparisons.

## Fresh controls and proof review

The independently authored `fresh_checks.py` passed 504 exact finite-field recognition cases, checked 2,784 output coordinates against direct orbit application, and passed 300 exact rational local-quantization cases. Five numerical covariance controls reproduce the maximal-error nonlinear counterexample. These are finite regression controls, not all-size proofs, eager-table validation or performance benchmarks. Mathematical review checked T1–T4 after clarifying coordinatewise nonzero gauges, singular-pilot rejection and identically resonant branches. Independent review accepted T1–T5 with the displayed scope and guards; the accepted T4 wording correction is already incorporated.

## T7. Supplemental inverse-circulant transfer requires a spectral certificate

Let A=U* diag(lambda) U, with U unitary Fourier and every lambda_k nonzero. Suppose the complex dyadic multipliers are supplied or generated with paid O(N) preparation, and certified 0<lambda_min<=|lambda_k|<=lambda_max. Put kappa=lambda_max/lambda_min. With exact charged diagonal multiplication, two nonlinear relative-l2 Fourier calls of tolerance delta produce y with

    ||y-Ax|| <= (2delta+delta^2) lambda_max ||x||
                 <= (2delta+delta^2) kappa ||Ax||.

Indeed the inner transform error is at most delta||x||; diagonal scaling increases it by at most lambda_max, and the outer transform error is at most delta times the perturbed middle vector norm, at most delta lambda_max(1+delta)||x||. Add the two errors. For delta<=1, choose delta<=epsilon/(3kappa). If multiplication or multiplier preparation is rounded, allocate a separately certified share of this budget. The all-length finite-word speedup can transfer when log(kappa/epsilon)=o(log N), subject to every representation and preparation obligation.

This applies conditionally to the Hero17 chirp-convolution interface. It does not manufacture lambda_k=1/(DFT h)_k or its lower spectral bound from an l2-only FFT of h. That missing sup-error and nonzero-spectrum certificate is the decisive dependency, and is exactly why the naive Bluestein preparation route is insufficient. This is a classical conditioned composition, not an additional ranked discovery.
