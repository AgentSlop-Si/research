Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: f2da7d6d25994e33fb736d2167c26fa4f4d9db370203a64bc57d3db8e02c0655

---

# Independent review: NF-04 finite-word magnetic interface

Date: 2026-10-12. Verdict: **ACCEPT, narrowly scoped interface obstruction and paid extraction certificate.** The broad NF-04 numerical construction remains open. No external writes were made.

## 1. Reviewed object and provenance

The author candidate is `NF04_Finite_Word_Interface_Obstruction_CANDIDATE_2026-10-12.zip`, SHA-256 `5d6faf635187e2c3a4f3c7997907b83fe1b28e03f7c6128d1ac06a522726569e`. Its proof is pinned at SHA-256 `6b5372194abc37644b450725fd4cf9ef2233f6e8a13a23b05030c069258d9ee6`. The candidate's manifest, all fourteen payload hashes, and equality with the reviewed local files are verified in `INPUT_VERIFICATION.json`. The archive is included unchanged under `inputs/`.

The accepted algebraic source pins are SP07 `d2dadcecf110563ab0f775c18fd3b93733927b572608c0dc4ebf4d22a38d2649`, SP08 `b789f632ed2e40ace52f1f342198e385c2cd620669161cafa77575b8271a5b9e`, and Phase20 `c57900857d6c8914c1c23594bbdfa702e925cdebeb87db622e19c9cbb8297801`. Those bytes were independently hashed and read. The author's repository receipt pins Phase20 to commit `a5e6b606623578230194e6f9e459e5e68c39043d`; this review does not claim a second independent live repository fetch.

All author/source scripts remained inert: no import, execution, compilation, or AST parsing. Only the newly authored reviewer script in `controls/review_controls.py` was run. Finite controls support, rather than replace, the general proofs below.

## 2. Definitions and noninterchangeable operators

For the magnetic average, let N=KM, omega be a supplied primitive Nth root, q=omega^M, S e_i=e_(i+1 mod N), U e_i=q^i e_i. Then US=qSU,

    Q_j=I-alpha S-beta q^j U,
    D=(1-beta^K)I-alpha^K S^K,
    Delta=(1-beta^K)^M-alpha^N,
    R_w=(1/K) sum_j w_j Q_j^(-1).

The guards include an admissible field/root and Delta nonzero. Distinct exact character modes use w_j=sum_l gamma_l q^(-jl). The source's sparse sector formulas share D^(-1); their unit-cost field ledger does not specify rounded input semantics or numerical precision.

The separate chart fixes a primitive Nth root omega, the unnormalized negative-exponent DFT F[k,t]=omega^(-kt), G(s)=sum_t omega^(-t^2-st), and C[a,b]=G(a+b)/N. With delta=1-alpha^N-beta^N and phi_s=product_(j=1)^s(1-omega^j), its triangular sector scalar is

    g[a,b]=alpha^a beta^b phi_(a+b)/(delta phi_a phi_b), a+b<N,
    W[a,b]=C[a,b]/g[a,b], a+b<N; W[a,b]=0 otherwise.

This g uses the normalized double character average, including 1/N^2. W is an auxiliary weight-coordinate matvec, not R_w and not the full cross-index Weyl synthesis. The scalar in W is delta, not delta^(-1). Multiplying F by 1/sqrt(N) correspondingly scales C and W; no normalization is silently changed here.

## 3. Independently proved input-information obstruction

### 3.1 Noncommuting magnetic pair, author's fixed-point convention

Define round_p(x) as nearest multiple of 2^(-p), ties to even. It has p fractional bits; it is not a p-total-significand floating-point format. For every integer p>=2 and every integer B>=p+4, put h=2^(-B), N=K=2, q=-1, alpha=3/5, beta_-=4/5-h, beta_+=4/5+h, w=(1,1), x=e_0.

The two literal branch matrices at each beta are

    Q_0=[[1-beta,-alpha],[-alpha,1+beta]],
    Q_1=[[1+beta,-alpha],[-alpha,1-beta]].

Their commutator has off-diagonal entries of opposite signs and magnitude 4 alpha beta, so neither legal problem is a commuting or zero-parameter specialization. Both determinants equal 1-alpha^2-beta^2. Direct inversion and averaging give

    Delta_-=h(8/5-h)>0, Delta_+=-h(8/5+h)<0,
    R_w=(I+alpha S)/Delta,
    y_-=(1,3/5)/[h(8/5-h)],
    y_+=-(1,3/5)/[h(8/5+h)].

These are all coordinates, with ||x||_infinity=||x||_2=1. The fractional part of 2^p(4/5) is a nonzero fifth, at least 1/10 from any half-integer rounding boundary. Meanwhile 2^p h<=1/16. Therefore both beta values strictly round to the same value; every other input is identical between the pair, whether held exact or rounded identically.

The first-coordinate gap is

    |y_-[0]-y_+[0]|=(16/5)/[h((8/5)^2-h^2)] >=5/(4h).

For any single output z determined only by their common quantized input, the triangle inequality gives

    max(||z-y_-||_infinity,||z-y_+||_infinity) >=5/(8h).

This holds regardless of subsequent internal arithmetic precision. Since B is unbounded for fixed p, no fixed such input quantization can support a uniform bounded absolute error for all intended original inputs in this legal family. The conclusion remains valid if the algorithm emits an interval required to be narrower than the output gap. Refusing ambiguous data is legitimate, but is not successful evaluation of every legal original input.

The conclusion does not apply to a different contract in which the rounded numbers themselves define the target, or to an interface that supplies exact coefficients or progressively tighter certified input enclosures. No generic adaptive-precision impossibility follows.

### 3.2 All-dyadic companion and explicitly different floating-point convention

At N=K=2, beta=0, alpha=1 plus or minus h, x=(1/2,1/2), direct diagonalization along the all-ones vector yields respectively -2^(B-1)(1,1) and +2^(B-1)(1,1). Both determinants 1-alpha^2 are nonzero. Under the author's fractional-bit convention both alphas strictly round to 1 for B>=p+2.

The reviewer additionally checked a conventional binary nearest-rounding format with p total significand bits and sufficient exponent range. Its neighbors of 1 are 1-2^(-p) below and 1+2^(1-p) above. If B>=p+2, both 1 plus or minus 2^(-B) lie strictly inside the rounding cell of 1. The same opposite-output obstruction therefore holds for that separate model. These conventions must not be merged into one ambiguous use of “p-bit.”

This is information loss before evaluation. It is not proof that computing the inverse of an exactly represented, legal p-bit matrix is impossible, nor an unrestricted numerical-algorithm lower bound.

## 4. Independently reconstructed range and condition-number witness

At N=3 let z=i sqrt(3), omega=(-1+z)/2, beta=1/2, alpha=2^(-B), B>=1. Then delta=7/8-2^(-3B)>=3/4. Direct evaluation gives G(0)=-z and G(2)=2+omega. At a=2,b=0 the q-factorials cancel, yielding

    W[2,0]=delta 2^(2B)(1/2+z/6),
    Re(W e_0)[2]=7*2^(2B-4)-2^(-B-1) >=2^(2B-2).

The complete matrix in the author proof agrees with the independently constructed matrices from literal branch inverses and character averages. In particular,

    ||W e_0||_2 >=delta 2^(2B)/sqrt(3),
    ||W e_2||_2 =4 delta/sqrt(3).

The reverse triangular nonzero diagonal proves invertibility. The variational singular-value bounds then imply kappa_2(W)>=2^(2B-2). Neither result uses a small delta. The unitary coefficient operator C therefore does not confer conditioning on the entrywise quotient chart W.

### Range is not mantissa complexity

A fixed-point output whose integer range is bounded independently of B eventually cannot approximate the real coordinate even within absolute error 1. Ordinary dense fixed-point serialization needs Omega(B) integer bits. This is a format-qualified range statement.

An exponent-based representation can encode an exponent of order B using O(log(B+1)) bits. Moreover, for this real coordinate alone the three-significant-bit value 7*2^(2B-4) has error 2^(-B-1). Thus for B>=t-1 it already meets an absolute target 2^(-t) with a constant-size significand and a growing exponent. This explicit control prevents promotion of the range proof into a universal Omega(B)-mantissa lower bound.

For exact representation of this particular real coordinate and B>=2, the reduced rational numerator is 7*2^(3B-3)-1, of bit length 3B, and the denominator is 2^(B+1). That is an exact dense-representation fact, not an approximate-output or arbitrary-encoding lower bound. The imaginary component and generic full outputs have their own precision requirements, handled by the paid interval export below. No near-optimal mantissa bound is claimed.

## 5. Recognition, root parity, and sufficient perturbation guards

At K=4, q=i, compare w=(1/2,1/2,1/2,1/2) with w+h e_0, h=2^(-p-3). They share the same p-fractional-bit rounded vector, but their exact negative-character coefficient vectors are respectively (1/2,0,0,0) and (1/2+h/4,h/4,h/4,h/4). Their exact support sizes are 1 and 4. An exact sparsity decision for the intended original weights is therefore not determined by the observed data. The reviewer also checked a perturbation at coordinate 1 so that the character sign is observable, rather than hidden by the all-equal coefficient example.

Approximate sparse recovery is a different, viable contract. For residual max_j|r_j|<=eta, B_Q>=max_j||Q_j^(-1)||_infinity, the normalized average satisfies

    ||(R_w-R_model)x||_infinity <=eta B_Q ||x||_infinity.

This follows by applying the triangle inequality before averaging. A promise separating zero from nonzero coefficients, exact symbolic inputs, or a certified residual must replace unqualified exact zero testing.

For exact omega=i at N=4, the reduced-exponent wrong-parity polynomial is G(1)=2+2omega^2=0. Replacing omega by i(1+h) changes it to -4h-2h^2, although the root-order residual tends to zero. This is a counterexample to treating a near-root as an exact root. The exact parity theorem itself remains valid. A certified exact root specification plus structural zero masks, or appropriate output enclosures, can preserve its consequences.

The author's quantitative bounds also pass independent proof review. With rho=|alpha|+|beta|, d=1-beta^K, c=alpha^K, geometric identities give

    B_Q <= [sum_(t<K)rho^t] [sum_(t<M)|d|^(M-1-t)|c|^t]/|Delta|.

This is finite whenever the source guards hold, including d=0 or c=0, with zeroth powers interpreted as 1. It need not be small. For certified ||Q_hat_j-Q_j||_infinity<=e and B_Q e<1, the inverse identity and Neumann series give

    ||Q_hat_j^(-1)-Q_j^(-1)||_infinity <=B_Q^2 e/(1-B_Q e).

Adding separately input-vector perturbation, weight perturbation, inverse perturbation, and certified arithmetic error gives exactly the four-term error budget in author section 6. Its quantities must be certified rather than estimated by unguarded floating-point tests. In particular the budget does not itself provide eta_exec for a sparse recognizer, recurrence, FFT, convolution, or full-output implementation.

## 6. Paid complete-output extraction

For a known exact Q(i sqrt(3)) output y_j=a_j+b_j i sqrt(3), the author's bisection creates an integer m satisfying m^2<=3*2^(2P)<(m+1)^2. With c=max(0,ceil(log2 max_j|b_j|)), P=t+c+4, this encloses sqrt(3) in an interval of width 2^(-P). Rounding a_j and the midpoint of b_j times that interval to multiples of 2^(-t-2) gives complex error at most

    2^(-t-2)+max_j|b_j| 2^(-P-1) <=(9/32)2^(-t).

The code handles negative b_j by ordering endpoints. The bisection requires O(P) integer-square tests on O(P)-bit values, hence an elementary O(P^3) schoolbook bit upper bound. Endpoint arithmetic, rational coefficient sizes, and serialization are separately chargeable. This is a valid restricted conversion lemma, not a completed all-input fast numerical executor.

The reviewer implemented a different exporter: exact integer square root, lower endpoint multiplication, and t+3 fractional output bits, then certified each full complex coordinate using an exact rational upper bound on squared error. All 210 exported coordinates passed at t=8 or t=32. This shows directly that the witness family remains computable when scale-dependent precision and output cost are allowed.

## 7. Fresh independent evidence

The reviewer uses Python standard-library integer/Fraction arithmetic only. The fresh run checks:

- 63 literal 3-by-3 branch inverses, each multiplied back to the identity.
- 63 complete normalized double-sector matrices, including all zero sectors.
- 35 full chart vectors against a separate literal polynomial convolution.
- 70 full dyadic vector exports, totaling 210 complex output coordinates.
- 12 noncommuting fixed-point collision pairs, checking both full output vectors, determinant legality, commutators, quantization, and half-gap.
- 12 all-dyadic binary-significand collision pairs, plus exactly representable noncollision controls.
- 5 sparse-support collisions with a shifted-coordinate Fourier-sign control.
- 4 exact-root versus near-root parity controls.

The chart B values are 1,2,3,8,24,53,113. The collision p values are 2,3,8,24,53,113, with two independent B offsets in each model. These are finite correctness controls, not an exhaustive machine-ABI qualification. The reviewer did not execute the author program or adopt its historical run as independent evidence.

## 8. Numerical-analysis antecedents and novelty boundary

The numerical mechanisms are established. The standard link between sensitivity and distance to singularity is treated by Demmel, *On condition numbers and the distance to the nearest ill-posed problem* (1987); the publisher summary explicitly includes matrix inversion. Only the available summary was consulted here, not the paywalled article. https://doi.org/10.1007/BF01400115

Higham's author-written explanations distinguish conditioning of a problem from backward/forward stability of an algorithm. They support interpreting these witnesses as interface and conditioning warnings, without turning them into a new instability theorem for every implementation. https://nhigham.com/2020/03/19/what-is-a-condition-number/ and https://nhigham.com/2020/03/25/what-is-backward-error/

Goldberg's 1991 paper, in its official Oracle-hosted reprint, explicitly separates significand precision, exponent range, rounding error, and out-of-range values. That distinction is essential to the limited range conclusion in section 4. https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html

Demmel's *The complexity of accurate floating point computation* states its own specific accuracy and efficiency model; its abstract was consulted as a scope comparator, not as proof of the present claims. https://arxiv.org/abs/math/0305004

The two-input indistinguishability proof, Neumann bounds, resolvent identity, and rational interval extraction are elementary uses of classical principles. The packet's contribution is an explicit, checked project-interface diagnosis. No worldwide priority or new general floating-point lower bound is certified.

## Scope and remaining work

Status: “Independent scoped acceptance: finite-word interface obstruction and paid quadratic-field extraction control; numerical construction remains open.”

Finding: “Legal noncommuting inverse inputs can collapse under fixed input quantization; chart output range and kappa_2 are unbounded already at N=3 with delta>=3/4; exact sparse support is ambiguous from rounded weights. Require certified input semantics, scale/separation, residual/parity handling, and complete numerical cost/error bounds.”

Still open: a frozen general coefficient/root representation, admissible parameter/scale family, support-or-residual recognizer, certified precision escalation, numerical convolution/recurrence error, charged preparation and refusal paths, and complete output costs in a single bit/RAM model. 

Accepted exact-field and H17/Phase20 results remain unchanged. The interface diagnosis does not close the positive finite-word construction or certify a Fourier speedup.
