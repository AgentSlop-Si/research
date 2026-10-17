# ALG-034: all-integer-length exact-dyadic zero and precision policy

16 October 2026. Baseline: AgentSlop-Si/research at `35d9dcdc3f3869de75b33b2b09705222e8d09e8d`.

## Disposition and new scope

**Scoped mathematical completion, proposed for independent acceptance.** For every integer N>=3, exact common-grid complex dyadic input and the genuine specified serial producer, the projected-zero decision and finite one-shot precision policy extend beyond the already accepted power-of-two case. The extension uses the actual odd/even phase convention, exact cyclotomic reduction, an explicit nonzero separation floor, and a complete paid prepass. It does not require a numerical zero tolerance or an unbounded retry.

The generic precision parameter below is independent of the dyadic-only Q16 eligibility contract. Nothing here creates an all-size source adapter, authenticates a producer, executes a historical program, relaxes any wrapper cap, proves original-input Fourier recovery, or provides a fast backend. The existing ALG-034 parent remains TO RESEARCH, priority 48. The prior dyadic theorem and completed bounded-wrapper audit are retained without reopening or crediting them again.

A separate finite-query obstruction makes the arbitrary-real boundary precise: exact projected-zero decision cannot be a universally terminating procedure from unrestricted approximation-oracle access alone. That obstruction does not apply to exact dyadic input, symbolic inputs with additional structure, or ordinary approximate-output tasks.

## 1. Source binding and previous completion

The current-baseline [v14 source](https://github.com/AgentSlop-Si/research/blob/35d9dcdc3f3869de75b33b2b09705222e8d09e8d/math/archive/objects/a0/a0a5d23b1ca51bfe2b2734d64ee4cf0cce61e7735eac04a060a99430749113ef__RESEARCH_20261009-201937_.md) was fetched in full and byte-matched to SHA-256 `a0a5d23b1ca51bfe2b2734d64ee4cf0cce61e7735eac04a060a99430749113ef`. Its later numerical qualifications, rather than its historical fast-path implementation claims, govern this report.

The accepted serial-producer report is SHA-256 `8dcc83d64316a136cb482fd04cff81ebaf7bf2351ab61fec1f02d8eadaf81cf8`; its independent acceptance is `31820fc28ff120f5982d4be0a03922600f06c3b7fb1a707b2617ae6e65201bf4`. Both local bodies are bound to exact members of the accepted archive. The current-baseline [precision-archive manifest](https://github.com/AgentSlop-Si/research/blob/35d9dcdc3f3869de75b33b2b09705222e8d09e8d/math/reviewed_rounds/2026-10-13-reviewed-1354/MANIFEST.json) was fetched and matched to that local archive's bytes, SHA-256 and Git-blob identity. The analogous [bounded-wrapper manifest](https://github.com/AgentSlop-Si/research/blob/35d9dcdc3f3869de75b33b2b09705222e8d09e8d/math/reviewed_rounds/2026-10-13-reviewed-1625/MANIFEST.json) was also checked. No remote binary download is claimed.

The immediately preceding [dyadic policy report](https://github.com/AgentSlop-Si/research/blob/35d9dcdc3f3869de75b33b2b09705222e8d09e8d/math/finalized/2026-10-16-finalization-cycle-0001/alg034-zero-policy/REPORT.md) has SHA-256 `b2578bccccdd4dfc95038c07cb625ee014ffda86cef35d73d764e356f78f9f9c`; its independent acceptance has SHA-256 `1a3628ea577d13ef9bb19ee6afc8dd251c1eba59badc8a8b50ac735970463cff`. Those complete local texts and the accepted review ZIP were inspected. A separate current-baseline remote readback of the published report was also byte-matched. The current open-record index already records the dyadic-only result. This report adds the general cyclotomic field, paid polynomial construction/reduction, generic relative-precision interface, and approximation-oracle boundary. It does not re-claim the prior power-of-two theorem as new. `SOURCE_BINDINGS.json` states exact verification methods, including any local-only antecedent binding.

The current ALG-034 owner record and [baseline open index](https://github.com/AgentSlop-Si/research/blob/35d9dcdc3f3869de75b33b2b09705222e8d09e8d/math/finalized/2026-10-15-rebuilt-open-record-index/open-record-index.json) identify ALG-034. This is a continuation of that owner, not a new algorithm or a new novelty ranking. Full native preimages are not redistributed in this packet.

## 2. Exact domain, phases and target

Assume integers N>=3, 3<=B<=N, 0<a<N with gcd(a,N)=1, and 0<=beta<N. Use the longer-blocks-first balanced partition with starts s_b and positive lengths ell_b. All input and state data are exact. Write

    x_j=(u_j+i v_j) 2^(-F),   u_j,v_j,F integers,
    h=N mod 2,   R=exp(pi i/N),
    r_(b,t)=a t(t-1)+2(a s_b+beta)t+h t modulo 2N,
    S_(b,t)=R^r_(b,t),
    d_b=sum_(t=0)^(ell_b-1) S_(b,t) x_(s_b+t),
    (P x)_(s_b+t)=conjugate(S_(b,t)) d_b,
    Y=U_N P x.

Here U_N is the unitary negative-sign DFT. There is no factor 1/ell_b in P, so P is not being treated as an orthogonal projection. Precisely,

    ||Y||_2^2=||P x||_2^2=sum_b ell_b |d_b|^2.       (1)

If the original input is nonzero, let W>=1 be the actual maximum Cartesian numerator bit length and put e=W-F. The accepted specified producer, with its intended-root, exact-index, rounding, range and input/output-binding premises, supplies

    ||Yhat-Y||_infinity <= Delta = 2^e C 2^(-p),
    H=min(binomial(N+B-1,B),2^(N-B)),
    C=64 H B 2^B N^2,

provided p>=W and 2 C 2^(-p)<=2^(-t), for the requested integer t>=0. This producer already covers all N>=3. It uses B direct seeds and a serial order-B recurrence; substituting a historical FFT path is not covered.

Exact common-grid conversion, if needed, must pay the actual exponent spread and resulting numerator width. The input domain is not uncertain physical measurements or unrestricted real oracles.

## 3. All-length zero theorem

Set

    L=lcm(2N,4),  eta=exp(2 pi i/L),  D=phi(L),
    f(X)=Phi_L(X),
    e_(b,t)=(L/(2N)) r_(b,t) modulo L.

Then L<=4N, R=eta^(L/(2N)), and i=eta^(L/4). For each block first aggregate coefficients with exponents reduced modulo L:

    g_b(X)=sum_t [u_(s_b+t) X^e_(b,t)
                    +v_(s_b+t) X^((e_(b,t)+L/4) mod L)],
    h_b(X)=g_b(X) mod f(X),   deg h_b<D.

The symbol h_b for a remainder is distinct from the parity scalar h. All coefficients and divisions are exact integers because f is monic. By construction,

    2^F d_b=g_b(eta)=h_b(eta).                              (2)

The cyclotomic polynomial f is the minimal polynomial of eta over Q, so (2) vanishes if and only if h_b is the zero polynomial. Equation (1) gives the exact decision:

    Y=0  iff  P x=0  iff  every h_b=0.                     (3)

The classical irreducibility, degree, integer-coefficient and conjugacy facts used here are stated and proved in [Keith Conrad, Cyclotomic Extensions, Theorem 2.5 and Section 5](https://kconrad.math.uconn.edu/blurbs/galoistheory/cyclotomic.pdf). Their content was checked; no new cyclotomic theorem is claimed.

Every original coordinate and block must be inspected before reporting (3), with actual input/state identity preserved. An approximate-zero payload or a digest of an untrusted declaration does not establish (3). For example, N=6, B=3, a=1, beta=0 and x=e_0-e_1 give exact projected zero despite nonzero original input.

The odd-length term is essential. At N=9, B=3, a=1, beta=0 and x=e_0-e_1, the true first summary is 1-exp(pi i/9), which is nonzero. Dropping h t falsely yields zero. Also, the power-of-two shortcut Phi_N=X^(N/2)+1 cannot be substituted for the general f: at L=12, Phi_12=X^4-X^2+1 is zero at eta but has nonzero remainder modulo X^6+1. General cyclotomic coefficients need not lie in {0,+1,-1}; Phi_420 already has magnitude-two coefficients. The ledger below therefore allows coefficient growth.

The older smaller-field power-of-two algorithm remains a valid specialization and can retain its better constants. The universal L used here is deliberately convenient rather than minimal.

## 4. Nonzero separation without reduced-coefficient-height inflation

For every block with h_b nonzero, compute A_b=||g_b||_1 after aggregating equal exponents modulo L. Select one with minimal A_b, breaking ties by block order, and write A for its mass. Then A>=1 and

    A_b <= sum_(j in I_b)(|u_j|+|v_j|) < 2 ell_b 2^W.

Use the mass of the original aggregated polynomial, not an unproved small-height assumption for h_b. Every conjugate g_b(eta^r), gcd(r,L)=1, has modulus at most A even when the remainder coefficients are larger.

The nonzero value z=g_b(eta) is an algebraic integer. Its field norm is a nonzero integer, hence

    1 <= product_(gcd(r,L)=1) |g_b(eta^r)|
       <= |g_b(eta)| A^(D-1).

Thus |g_b(eta)|>=A^(-(D-1)). Equivalently, multiplication by h_b on the integer basis of Q[X]/(f) has a nonzero integer determinant. This determinant is only a proof device; it is not computed by the policy. The classical embedding-product and integrality facts are given in [J. S. Milne, Algebraic Number Theory, Corollaries 2.20–2.21](https://www.jmilne.org/math/CourseNotes/ANT.pdf).

Put

    K=ceil(log2 A),   G=W+(D-1)K,
    mu=2^(-F-(D-1)K)=2^e 2^(-G).                           (4)

The bit-length definition gives K=0 for A=1. Equations (1)–(4) imply

    ||Y||_2 >= mu >0.                                      (5)

Since D<=L<=4N and K<=W+ceil(log2(2 ceil(N/B))), G=O(N(W+log N)). Only the exponent encoding of mu is stored. No huge number 2^|F|, 2^G or A^(D-1) is required just to plan precision. The prepass can nevertheless have large polynomial-arithmetic cost; it is paid below.

This is an input-dependent sufficient floor, not a width-independent condition bound. At N=6, B=3, x_k=e_0-(1-2^(-k))e_1 has W=k+1, F=k and g_0=1 after common-grid aggregation. Consequently A=1, G=k+1 and mu=2^(-k), while the actual target norm is sqrt(2)2^(-k). Near-kernel dependence survives.

## 5. Generic one-shot relative-precision theorem

Choose an integer q>=ceil(log2 N), and define rho=2^(-q). This is a generic mathematical tolerance, not an assertion of Q16 admissibility. Let c=ceil(log2 C) and choose the actual planned fractional precision

    p_star=max{W, c+t+1, c+q+G+2}.                          (6)

If a genuine accepted serial producer executes at p>=p_star under all its premises, then Yhat is nonzero. For any positive normalization alpha satisfying alpha>=||Yhat||_2/2, its certified radius meets

    Delta/alpha <=rho.                                     (7)

Proof: (6) supplies exact normalized loading, the inherited upstream precision inequality, and

    Delta <=rho mu/4.

Because sqrt(N)rho<1 for N>=3 and the stated q, norm comparison gives

    ||Yhat||_2 >= ||Y||_2-sqrt(N)Delta >3mu/4>0.

Therefore alpha>3mu/8 and Delta/alpha<(2/3)rho<=rho. This proves (7) with slack. The bound compares the true target and actual returned vector under the producer theorem; it is not derived from a guessed relation between precision and a rounded normalization exponent.

An exact dyadic vector Yhat admits such an alpha: choose a power-of-two lambda with ||Yhat||_2<=lambda<2||Yhat||_2 using its exact squared norm and exact power-of-four comparisons, then use alpha=lambda/d with d in {1,2}. No numerical square root is needed for this selection. This establishes the generic mathematical normalization inequality only. A deployment's immutable-source grammar, doubling/quantization, output range, metadata and downstream eligibility still require their own valid implementation and paid checks.

On the existing dyadic N=2^m branch, the accepted bridge uses q=Pq=16m+16 and its existing alpha contract; this satisfies the generic premise and recovers its allowance. For non-dyadic N, this report does not claim a Q16 adapter or inherit its eligibility by changing m to ceil(log2 N).

## 6. Finite policy and deployment boundary

The mathematical policy has these mutually distinguished outcomes:

1. Validate exact input, canonical state, positive balanced partition and integer t,q. Reached rejected-prefix work is charged. All-zero original numerators may return EXACT_INPUT_ZERO before construction of f.
2. Otherwise run the full exact zero prepass. If every h_b vanishes, return EXACT_PROJECTED_ZERO bound to the original input/state. Report Y=0 if that is the requested sampled target. Do not relabel the original input zero, fabricate a producer receipt or normalize a zero source. An explicitly requested zero vector requires N output writes.
3. If some h_b is nonzero, return the finite plan (4),(6), or actually run a genuine available producer and then perform the exact required validation. This work delivers a mathematical plan; no implementation of an authentic production producer or adapter is furnished here.
4. A resource or interface restriction returns its truthful block, not successful execution. For the old bounded wrapper retain dyadic N with 4<=N<=4096, actual payload-width and metadata limits, its exact domain and all downstream requirements. For an actual run at p use its actual I=B+2ceil(log2 N)+10 and kappa=W-F-p. The sufficient universal width check is p+I<=65536 at that same p. Failure of that upper-bound certificate does not prove actual output overwidth. Any actual overwidth or invalid metadata remains a real interface rejection.

No policy outcome changes the correct second ideal Fourier target. With the same negative unitary transform, U_N^2=R, so the second target is R P_(a,beta)x/alpha, not U_N x. This precision gate controls numerical error in a sampled row and does not remove sampling/projection error.

## 7. Fully paid setup, arithmetic, movement, storage and outputs

Here is a deliberately elementary finite implementation bound. It makes no speed claim. Let J=ceil(log2(4N+1)); E be the full input/state/tolerance/exponent metadata length; and W be the actual maximum numerator width (take W=1 for an all-zero cost bound). M(s)>=s denotes a justified s-bit multiplication bound. All array reads, writes, clears, copies and scans below count at their actual integer widths.

### 7.1 Cyclotomic setup, constructed rather than assumed

For n=1,...,L, begin with X^n-1 and successively perform exact monic long divisions by every already computed Phi_d with d|n and d<n. The final quotient is Phi_n. Discover the divisors by explicit integer divisibility tests; factorization is not an oracle. This is wasteful but finite.

There are at most L^2 divisions and each uses O(L^2) integer multiply/add operations. Before each division, the exact dividend is a product of distinct remaining roots of X^n-1, so its coefficient l1 norm is at most 2^n. Every divisor has coefficient l1 norm at most 2^L. One long-division cancellation enlarges the current coefficient l1 bound by at most 1+2^L; there are at most L cancellations. All temporary integer widths are therefore at most O(L^2+log(L+2)). Put T0=L^2+3L+4 as a safe width envelope. Then

    cyclotomic setup work: O(L^4 M(T0)+L^2 J^2),
    retained cyclotomic table and setup scratch: O(L^3) bits.

The final Phi_n coefficient sizes are O(n) bits by the root-product bound; total retained table coefficients are O(L^2). The O(L^3) storage includes the larger scratch. A smaller construction may be substituted only with its own valid ledger. If schoolbook multiplication is used, the displayed setup bound is O(L^8), not near-linear.

### 7.2 Exact input prepass and block reductions

Form one degree-<L g_b at a time, clearing and scanning its dense array, adding at most 2ell_b exact monomials, recording A_b, and reducing modulo f by monic long division. A raw g_b has l1 norm <2N2^W. Using at most L cancellations and ||f||_1<=2^D<=2^L gives an intermediate width

    S=O(W+log(N+2)+L^2).

There are O(BL^2) multiply/add steps for all reductions. Paying exact phase computation, modular indexing and gcd validation conservatively gives

    prepass work: O(NW+N J^3+B L^2 M(S)+E),
    retained input, one-block scratch and metadata: O(NW+L S+B J+E) bits.

This includes every input read, coefficient clear, zero/mass scan, movement of exact coefficients, and the decision. Keeping all remainders as a separate proof trace adds O(B L S) bits/writes; the streaming bound does not include such a trace. A separate independent verifier must pay its own full prepass. Common-grid conversion and immutable copying are additional actual costs when not already performed.

### 7.3 Plan construction and inherited serial production

Let L_H=O(B log(N+B+1)) bound exact binomial-planning intermediates, and V bound actual integer widths in C,K,G,p,F,t,q and output scale metadata. Exact binomial updates, power/bit-length comparisons and the constant-many exponent calculations cost, for example, O(B L_H^2+V^2+N+E) with schoolbook multiplication/division. The numeric magnitudes p and |F| are not charged as unit-size metadata. No exponential-sized real number is materialized just to represent (4).

Actual production is a separate, cumulative obligation. With

    Aop=NB+B^2+N,  I=B+2ceil(log2 N)+10,
    ell_num=p+I+4,
    T=O((p+1)^3 log(p+2)+(p+1)J),

the accepted producer's conservative bit-work ledger is

    O(NW+log(|F|+2)
      +(N+B^2) M(J)log(J+2)
      +B M(L_H)log(L_H+2)
      +N(p+1) M(T)log(T+2)
      +Aop M(ell_num)log(ell_num+2)),

plus actual state/tolerance metadata. It pays exact normalization/loading, root/phase and inverse-square-root construction, coefficient formation, direct seeds, all serial recurrence work, normalization/gauge scan, and N exact scaled outputs. A suitable native fixed-integer main arithmetic removes its last rational-gcd factor; this packet certifies no such implementation. Retained producer storage is

    O(NW+(N+B)ell_num+T+L_H+log(|F|+2)),

plus metadata. Add the entire cyclotomic setup/prepass/planning ledger rather than hiding it in a free upstream source. Safe cumulative retained storage is the sum of the displayed bounds; freeing prior arrays may reduce it.

The generic exact norm for normalization needs N squared-integer accumulations. If returned Cartesian grid numerators have width Q, a simple paid bound is O(N M(Q+log(N+2))+E_out) bit work, with an accumulator of O(Q+log N) bits, plus actual payload reads and scalar metadata. The norm exponent is handled symbolically. Copies, signed requantization, any doubling, immutable source creation, actual downstream preparation/calls, reconstruction and final output are additional. This generic norm bound does not replace the accepted wrapper's stronger validation ledger.

The mathematical precision exponent can be O(N(W+log N)+q+t); certified root generation at that precision may dominate everything else. There is no hidden bounded-precision word assumption, free data movement, free validation, free norm, free output tape, free producer retry, host-resource promise, or sub-FFT conclusion.

## 8. Why unrestricted approximation-oracle zero decision remains impossible

Fix any admitted N,B,a,beta. Suppose a deterministic procedure receives a real coordinate only through dyadic approximations answering requested precisions k with absolute error at most 2^(-k), and is required to decide exactly whether P x=0 for every real input, always terminating.

Run it on the identically zero input with all oracle replies zero. Termination uses finitely many queries; let k_max be the largest queried precision, taking k_max=0 if none. Choose epsilon=2^(-k_max-1)>0 and replace only the first real coordinate by epsilon. All the same zero replies remain legal for this alternative input, since epsilon is smaller than every queried error radius. The deterministic transcript and answer are identical. Yet S_(0,0)=1, so the first summary is epsilon and P x is nonzero. The procedure is wrong on one input.

Therefore no such universally terminating exact zero decider exists in that interface. This is a representation-specific indistinguishability argument, not a lower bound on approximate Fourier transforms, on promised nonzero inputs with a supplied separation bound, or on symbolic real representations with a decidable equality theory. Exact finite dyadic input supplies the additional information used in Sections 3–5; its bit cost cannot be removed while retaining those guarantees.

## 9. Fresh controls, limitations and owner proposal

The freshly authored `checks.py` imports only the Python standard library. No supplied producer, old checker, wrapper or downstream program was imported or executed. `CHECK_RESULTS.json` records exact polynomial-factor identities, independent long-division/companion reductions, multiplication-matrix determinants versus conjugate products, precision-plan inequalities, kernel/near-kernel examples, and controls for parity and non-binomial reduction. These are finite corroboration, not a production execution certificate or a substitute for the proof.

The precise suggested disposition is COMPLETE_SCOPED_ALL_LENGTH_EXACT_DYADIC_POLICY, conditional on independent mathematical acceptance. Archive that child gate against repeat dispatch, while retaining ALG-034 TO RESEARCH at priority 48. Remaining owner gates are the authentic executable/certified producer and its source binding, compatible all-size adapter, actual valid downstream integration, any richer arbitrary-data interface, stable fast backend, full recovery, practical resource guarantees, and novelty/priority review.

The proposed current-action/pass-stop prefixes update only this mathematical subcase; they must retain existing history and all full-owner stopping conditions. Native writes, source publication and final application remain separate parent operations. No remote mutation occurred in this research task.
