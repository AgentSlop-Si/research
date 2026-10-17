# ALG-064: certified finite-precision evaluation with at most r suspect bins

17 October 2026. **Bounded numerical lemma and evaluator contract; parent remains TO RESEARCH, priority 42.** This is a new, distinct numerical gate after the accepted capped exact-field constructor. It does not reopen or claim the completed Massey comparison, order-two recognition, or capped synthesis.

## 1. Decision and source boundary

The current ALG-064 owner explicitly asks any successor to name a distinct numerical, bit-cost, source-integration or broader-attribution gate. This report selects **finite absolute-error evaluation from supplied dyadic data and connection coefficients, with paid certified Fourier-node approximations**. It proves:

1. For every complex polynomial C with C(0)=1 and degree r, fewer-than-threshold denominators on the Nth-root grid occupy at most r bins at threshold tau=(2N)^(-r).
2. A finite-precision classifier with denominator error at most tau/4 preserves that cardinality. It needs no exact numerical zero test or characteristic-root extraction.
3. The full boundary formula, including the actual recurrence defect, gives an explicit all-output absolute-error certificate. At most r suspect bins use direct Horner evaluation. Every regular bin has a paid precision bound.
4. On exact dyadic recurrence inputs with supplied coefficients and certified nodes, this gives an O(N(L+1))-operation numerical branch at an explicit finite word length. It does not prove that a rounded recurrence recognizer finds suitable coefficients, that field/node generation is free, or that the original implementation realizes this contract.

The current native Catalogue, novelty and overview views and the current repository owner were read. Repository baseline: `d844509088e022fc48d4f02ca378022a9ce67702`. The [accepted capped constructor](https://github.com/AgentSlop-Si/research/blob/d844509088e022fc48d4f02ca378022a9ce67702/math/finalized/2026-10-16-research-finalization-1412/algorithms/REPORT.md), sections 2 and 5, and its [independent acceptance](https://github.com/AgentSlop-Si/research/blob/d844509088e022fc48d4f02ca378022a9ce67702/math/finalized/2026-10-16-research-finalization-1412/independent_review/INDEPENDENT_REVIEW.md), ALG-064 section, already complete exact capped recognition and all-frequency evaluation, while explicitly separating finite precision. The [Phase23 audit](https://github.com/AgentSlop-Si/research/blob/d844509088e022fc48d4f02ca378022a9ce67702/math/archive/objects/c0/c074b19dd40f6a50a5a4a3b91b0e447824f47e90206032d4c88dc8673a723817__13_PHASE23_AUDIT.md), sections 6–7, also leaves cancellation and finite-word stability open. The [original theorem](https://github.com/AgentSlop-Si/research/blob/d844509088e022fc48d4f02ca378022a9ce67702/math/archive/objects/d3/d32912d6f37d714b429fd21f1faaff1457f75c53a87ce91288ab3abe0073180b__THEOREM.md) separately preserves the larger arbitrary-input/noncommuting architectural target. That target is not closed here.

No mathematical novelty or historical-priority claim is made. The new result is the explicit conjunction of elementary root separation, defect accounting and a finite-word interface for this owner.

## 2. Exact data and residual identity

Let N>=2, 1<=L<N, and let x_0,...,x_(N-1) and c_0,...,c_L be complex dyadic rationals with c_0=1. Let

    C(T)=sum_(i=0)^L c_i T^i,  r=deg C<=L,
    X(T)=sum_(j=0)^(N-1) x_j T^j.

The declared span L is retained even if trailing c_i vanish. The target is the unnormalized positive-exponent DFT at t_k=exp(2 pi i k/N). A sign change replaces k by -k. This report does not supply the normalized real-residual postprocessing.

For L<=j<N, compute the actual defect

    e_j=sum_(i=0)^L c_i x_(j-i).

Define boundary polynomials of degree below L:

    P_j=sum_(i=0)^j c_i x_(j-i),
    B_j=sum_(i=j+1)^L c_i x_(N+j-i),  0<=j<L,
    A=P+B,  E(T)=sum_(j=L)^(N-1) e_j T^j.

Coefficient comparison, without any recurrence promise, gives

    C(T)X(T)=P(T)+E(T)+T^N B(T).

Consequently, at each exact target node,

    C(t_k)X(t_k)=A(t_k)+E(t_k).

Put nu(z)=|Re z|+|Im z| and compute the rational upper bounds

    S=sum_j nu(x_j),   H=sum_i nu(c_i),
    K=sum_j nu(A_j),   R=sum_(j=L)^(N-1) nu(e_j).

Then |X(t_k)|<=S and |E(t_k)|<=R. All these quantities and A can be computed exactly with dyadic integer arithmetic. No sampled/prefix residual test is substituted. Exact recurrence inputs have R=0. Small nonzero R gives only the absolute-error guarantee below, never exact membership.

For L=0, C=1 and the only exact recurrence sequence is zero; one can directly certify the supplied data using R=S. This harmless special case is outside the main 1<=L theorem. N=1 is direct copying.

## 3. At most r genuinely small denominators

**Lemma.** For N>=2, C(0)=1, r=deg C>=1 and tau=(2N)^(-r),

    #{k: |C(t_k)|<tau} <= r.

**Proof.** Over C, write C(T)=product_(j=1)^r (1-T/alpha_j), counting roots with multiplicity. Every alpha_j is nonzero. This factorization is only a proof device; the evaluator never constructs it. If the product modulus is below (2N)^(-r), one factor obeys

    |1-t_k/alpha_j| < 1/(2N).

A single alpha cannot obey this inequality at two distinct target nodes t,u. Indeed |alpha-t|<|alpha|/(2N) implies |alpha|<1/(1-1/(2N)). If both held, then

    |t-u| < 2/(2N-1) < 4/N.

But distinct Nth roots are separated by at least 2 sin(pi/N)>=4/N, since sin v>=2v/pi on [0,pi/2]. Contradiction. Thus each root can account for at most one target bin, and their union has size at most r. Repeated characteristic roots cause no problem. QED.

If r=0, C=1 and choose tau=1. There are no small bins. This also covers untapped trailing registers L>r.

The threshold depends on r. A fixed numerical threshold independent of N does not give O(r) suspects. For example C(T)=1-T has |C(t_k)|=2|sin(pi k/N)|, so any fixed positive threshold below 2 captures a number of bins proportional to N. Exact-zero counting alone therefore does not justify a thresholded numerical implementation.

## 4. Certified classification and all-output error

Fix a desired absolute error epsilon with 0<epsilon<=1. Suppose evaluation produces complex dyadics qhat_k, ahat_k with rigorous bounds

    |qhat_k-C(t_k)| <= eta_q,
    |ahat_k-A(t_k)| <= eta_a,

uniformly over k, where

    eta_q <= min(tau/4, epsilon*tau/[8(S+1)]),
    eta_a <= epsilon*tau/8,
    R <= epsilon*tau/8.

Classify a bin as suspect precisely when |qhat_k|<3tau/4. This is decided exactly by comparing squared rational moduli with (3tau/4)^2. No square root or floating comparison is needed. Equality goes to the regular branch.

A suspect obeys |C(t_k)|<tau; the lemma therefore gives **at most r suspects**. A regular bin has |qhat_k|>=3tau/4 and |C(t_k)|>=tau/2. In the regular branch, divide ahat_k by qhat_k and round the result with complex absolute rounding error at most eta_div<=epsilon/4. Call the output y_k. Since

    qhat_k X(t_k)-ahat_k
      = (qhat_k-C(t_k))X(t_k) + (A(t_k)-ahat_k) + E(t_k),

we obtain

    |y_k-X(t_k)|
      <= (eta_q S + eta_a + R)/|qhat_k| + eta_div
      <= epsilon/2 + epsilon/4 < epsilon.

For every suspect, evaluate the original full X at t_k by a certified Horner calculation with absolute error at most epsilon. The complete vector therefore satisfies max_k |y_k-X(t_k)|<=epsilon, including all exact resonances and near resonances. The all-output claim is an absolute bound; relative error at a zero or tiny Fourier output is not promised.

If the computed R exceeds epsilon*tau/8, the numerical fast branch returns **residual certificate failed**. This does not mean the original vector has no low recurrence order or that a better C cannot work. It does not return an uncertified transform. A total algorithm can then use any separately certified full-transform fallback and pay its cost; this report does not treat such a backend as free. Every exact dyadic recurrence with the supplied C automatically passes the defect gate because R=0. Supplying/finding C is a separate interface and cost.

## 5. Explicit fixed-grid precision

Here is one finite-word realization of the evaluation assumptions. It is deliberately conservative, not an optimized precision theorem.

Assume each real/imaginary component of x and c is an integer multiple of 2^(-b). Form A and e exactly, so their components are multiples of 2^(-2b). Choose an integer p>=2b and put rho=2^(-p). Round every real/imaginary component to the nearest multiple of rho. Each resulting complex operation has absolute error less than rho. Allocate enough integer bits; neither overflow nor underflow is allowed. Obtain certified dyadic node approximations z_k with

    |z_k-t_k|<=rho,   rho<=1/N.

The cost of constructing and certifying these nodes is denoted C_roots(N,p), and is added separately. N supplied certificates/approximations must be read. No running-root recurrence is accepted without a bound on its accumulated node error.

For any exact polynomial F of degree D<=N-1 and coefficient modulus sum at most U, Horner evaluation at z_k, rounding after each complex multiply and add, obeys

    |Fhat(z_k)-F(t_k)| <= 3D(U+2)rho.

For D=0, copying the exact coefficient has zero error. To prove the displayed estimate, telescope z^j-t^j to get |z^j-t^j|<=j*rho*(1+rho)^(j-1), so the node contribution is at most 3DUrho. The D multiply/add pairs contribute at most 2D*rho*(1+rho)^D<=6D rho, because (1+1/N)^N<3. Coefficients are represented exactly at p>=2b.

It is thus enough to choose rho so that all of the following hold:

    rho <= 1/N,
    3L(H+2)rho <= min(tau/4, epsilon*tau/[8(S+1)]),
    3L(K+2)rho <= epsilon*tau/8,
    3N(S+2)rho <= epsilon,
    rho <= epsilon/4,
    p >= 2b.

These are explicit positive rational inequalities, and doubling p until they hold is a finite deterministic selection rule. The same p certifies C, A, direct suspect evaluation and final division rounding. If desired, use the actual degrees r and deg A to tighten the first two evaluation charges; retaining L handles trailing-zero coefficients without changing their declared-span boundary formula.

For a compact bound set W=2+S+H+K. Taking logarithms gives a sufficient

    p = O(b + log(1/epsilon) + r log(2N) + log N + log(L+1) + log W).

The product term H(S+1) causes at most 2 log W. The constants are absolute. All logarithms here describe required precision, not a unit-cost assumption for large numbers. A simple oversized sufficient choice is

    p >= 2b + ceil(log2(1/epsilon))
             + (r+2)ceil(log2(2N)) + 2ceil(log2 W) + 10.

It implies the above inequalities for 1<=L<N. Exact rational comparison can instead select the smallest convenient p, avoiding reliance on rounded logarithms.

## 6. Cost and what is not free

Let B_in bound the bit lengths of the exact real/imaginary input and coefficient numerators and their common denominator 2^b. Exact boundary/defect formation and R,S,H,K cost O(N(L+1)) dyadic operations at bit length B_0=O(B_in+log(N+L+1)). This includes input reads and full-tail verification. The common-denominator model is explicit: arbitrarily encoded rationals or algebraic-number recurrences require their own conversion and height analysis.

At working grid p, the magnitudes of Horner intermediates are bounded by constant multiples of H, K or S, plus rounding. Regular divisions have nonzero dyadic denominator and modulus at least 3tau/4. Conservative working integer length is

    B=O(B_0+p+log W+r log(2N)).

Exact squared-threshold comparisons use integers of this order. Complex quotient rounding can be done by exact integer products, integer division and nearest rounding. Let M(B) and D(B) be the charged integer multiplication and division costs. Then the accepted branch has bit-cost upper bound

    C_roots(N,p)
      + O(N(L+1) M(B) + N D(B)),

plus actual input/node-certificate reading and output writing. This is a conservative common-size bound, not a claim that each multiplication is optimal. It includes at most r direct N-term Horner evaluations because r<=L; N all-frequency numerator/denominator scans; boundary preparation O(L^2); exact residual verification; all N divisions or suspect outputs; and N output writes. Storage is O(N+L) words of the relevant sizes if node/output tables are materialized.

Unlike the exact-field report, this finite-word construction uses separately rounded divisions. It does not transfer the one-batch-inversion ledger to floating point. Batch-product stability is not established.

If coefficients and exact input share a modest dyadic representation and r is fixed, the precision grows only logarithmically in N beyond the stated magnitudes and output tolerance. For growing r, the r log N precision penalty is visible. This is neither an arbitrary-input faster DFT nor an improved integer-multiplication bound.

## 7. Verification and remaining obligations

`checks.py` is new standalone standard-library code. It imports or executes no supplied/historical research program. Its exact dyadic and rational controls test the defect identity, squared-threshold branches, regular-bin certificates, direct-bin rounding, untapped registers, near resonances and deliberate residual rejection. Certified Fourier-node approximations used by tests are independently generated by rational Machin/arctangent and Taylor remainder bounds; their cost is test-only, not silently charged as a fast production node constructor. `CHECK_RESULTS.json` states the actual checked ranges and counts. Observed PASS: 455 exact defect identities; 312 exact Gaussian-grid denominator controls (20 sharp controls); 60 accepted vectors with 880 certified all-output checks at N=4,8,16,32; 50 direct suspect bins; four accepted nonzero-defect cases; four late-defect rejections; and 32 adversarial classifier-radius controls. Working fractional precision ranged from 26 to 540 bits. These finite controls support transcription; the all-size result is proved above.

**Close only this new numerical subgate:** the residual-aware fixed-grid all-output evaluator contract with at most r suspect bins and the explicit conditional bit ledger. Preserve the already accepted exact mathematics and the native parent's TO RESEARCH status, priority 42, proof/novelty classifications and complete dated history.

**Still open or separate:** stable/raw-input coefficient discovery and its conditioning; efficient uniformly certified root-table construction and normalization; non-dyadic/algebraic input encodings and coefficient heights; a fully certified total fallback; normalized real-residual implementation; historical source integration/execution; production arithmetic, overflow choices and practical speed; broader arbitrary-input/noncommuting construction and worldwide attribution. This report is not a blanket closure of numerical stability for the whole parent.
