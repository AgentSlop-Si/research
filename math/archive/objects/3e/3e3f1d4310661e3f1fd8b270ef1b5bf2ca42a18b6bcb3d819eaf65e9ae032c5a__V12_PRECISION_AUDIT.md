# v12 centered lift: precision audit and charged constructive repair

9 October 2026. Independent supplement to `fft_hero1_centered_v12_20261009.zip`. The uploaded programs were read as text, never executed or imported. This report gives sufficient mathematical contracts and a constructive replacement design; it does not certify NumPy, SciPy, BLAS, the uploaded implementation, or an optimized implementation of the replacement.

## Conclusions

1. Centering genuinely reduces the certified Bessel rank. All 24 saved rank choices and all 28 saved v12 finite-grid parameter choices independently reproduce at 110 decimal digits. For N=511, Q=512, the tail-only target 10^-8 requires R=15 uncentered and R=11 centered. With M=8 and the source's complete deterministic bound, the 10^-8 choice is R=11, H=4, bound approximately 4.1122890220851245e-9. These targets exclude stochastic and numerical error.
2. The source correctly declines an unconditional finite-precision theorem. Its balanced-product explanation still needs a correction: logarithmic multiplication depth does **not** imply logarithmic worst-case forward error for a product. A product with k leaves contains k-1 local multiplicative errors. Both ordinary arithmetic error and reused-root error can be O(ku).
3. A charged repair preserves O(N) carrier arithmetic: reanchor every B=Theta(p/log p) positions, compute anchors and transition roots by bounded-argument Taylor series, and use p+O(log p) working bits. It gives uniform absolute carrier error at most 2^-p. Pi setup costs O(p) scalar arithmetic separately. The same device can prepare the dyadic root table needed by the inherited decoder.
4. The centered summary-interface ledger below retains a rank-independent leading error envelope. With certified preparation and balanced sums, the earlier sufficient mantissa order b=log2(N log N/g)+O(1) survives, with O(log b) guard bits. This is a theorem about a specified replacement, not about the saved floating-point code.
5. Bessel constants are not free. A factorial-series construction costs O(K(R+H)L_B+M(H+1)L_B) scalar operations, L_B=O(b/log b), plus argument/leading-factor preparation. For fixed H and the established shrinking-error scaling this is o(RN). No finite exact Bessel generator is claimed.
6. Centering does not stabilize the forward order recurrence. At N=511, M=8, R=11 its smallest nonzero active argument is pi/512; one seed-error mode has a lower amplification bound requiring 95.276 extra bits. The actual scalar amplification in our control is about 2^105.276. This obstruction concerns a proposed recurrence substitute; v12 itself uses separate library Bessel evaluations.

## 1. Product depth is not a forward-error bound

Suppose a complex multiplication is modeled by fl(xy)=xy(1+delta), |delta|<=nu, with adequate exponent range. This normwise model follows from ordinary real arithmetic with nu<=8u when u is small; it is sufficient here, not an assertion that all allowed errors occur in one actual IEEE run.

A binary product tree with k nonzero leaves has k-1 internal multiplication nodes. Recursively expanding the computed result gives

    computed_product = exact_product * product_(internal nodes v)(1+delta_v).

Its relative error is at most (1+nu)^(k-1)-1. Tree depth does not replace k-1 in this formula. The same issue applies to any prefix produced from disjoint product subtrees. A Blelloch prefix may add a few identity multiplications, but its bound is still O(ku), not O(u log k).

For a sharp model counterexample choose every internal error to be exp(i epsilon)-1. With exact unit-modulus leaves, the final error magnitude is

    |exp(i(k-1)epsilon)-1|,

which is asymptotic to (k-1)|epsilon|. If both supplied transition roots instead have the same multiplicative perturbation exp(i epsilon), a length-k prefix acquires exp(i k epsilon), even with exact later arithmetic. Unit-modulus normalization alone cannot remove either phase error.

Thus the source's root requirement O(target/N) is necessary for a safe unanchored two-root scheme, but root accuracy by itself is not a complete repair. Multiplication precision must also accommodate O(N) accumulation, or one must reanchor/replace the scheme. The source's O(log N) *depth* count remains algebraically correct.

The checker records twelve admissible-error controls, at p=24,53,80 and k=16,256,4096,65536. They are model counterexamples, not claims that identical signed rounding occurs in a particular floating-point library.

## 2. Explicit O(N+p)-arithmetic carrier repair

### 2.1 Exact integer arguments

Set q=2^ceil(log2 N), j_k=floor((2kq+N)/(2N)), r_k=kq-Nj_k, and c=(N-1)/(2q). Compute these with unbounded exact integers. Then

    phi_k = exp(-i*pi*(N-1)*r_k/(q*N)),
    |r_k|<=N/2.

The anchor exponent has absolute value <=pi/2. The two transition exponents are

    a_d = -2*pi*c*(q-dN)/N, d=1,2,

and have absolute value <=pi. No subtractive computation of kq/N-j_k is required. Rational quotients are rounded only after their exact integer numerators and denominators are formed.

### 2.2 Concrete sufficient parameters

Let eta=2^-p, p>=2. Define

    B = minimum integer L>=1 for which pi^L/L! <= eta/128,
    L_gamma = minimum L>=1 for which pi^L/L! <= eta/(128 B),
    P = p + ceil(log2(2^18 B (L_gamma+1))).

Use outward upper bounds for pi when selecting these integers. The displayed formulas describe mathematical sufficient parameters, not the source's binary64 rank-selection functions.

Prepare a rational pi approximation with absolute error <=2^-P. Use P-bit round-to-nearest arithmetic, no underflow/overflow, correctly rounded rational argument conversion, and ordinary four-product/two-addition complex multiplication. At each index s=0,B,2B,... evaluate phi_s directly with B Taylor terms. Compute each transition root with L_gamma terms. Starting from its anchor, form the remaining at most B-1 carrier values by ordinary sequential multiplication by the appropriate root. A balanced within-block product scheme may also be used, with its actual O(Bu) bound.

### 2.3 Error proof

For real |a|<=pi, the integral form of the Taylor remainder gives

    |exp(ia)-sum_(j=0)^(L-1)(ia)^j/j!| <= pi^L/L!.

For a rounded bounded argument, the sum of absolute Taylor terms is at most exp(pi) plus a negligible perturbation. Generate terms by t_j=t_(j-1)(ia)/j and sum them. Standard real relative-error expansion, with 16L*2^-P<=1/2, gives a conservative absolute rounding-and-argument allowance

    1024 (L+1) 2^-P.

One way to see the constant is to bound each term-generation path and all subsequent additions by gamma_(16L), then multiply by exp(pi); add the bounded argument-conversion and pi errors. Since gamma_(16L)<=32L*2^-P, the resulting constant is smaller than 1024(L+1). Correctly rounded rational conversion and pi error are included. There is no cancellation-based relative-accuracy claim for the sum.

The selected P therefore makes this allowance <=eta/(256 B). Combining it with the tails yields anchor error <=eta/64 and root error <=eta/(64 B), using slack in the displayed constants. Each within-block multiplication has nu<=8*2^-P<=eta/(64 B).

For a position s+t, 0<=t<B, all exact factors have modulus one, so expansion of the perturbed product yields

    |computed_phi_(s+t)-phi_(s+t)|
       <= (1+eta/64)(1+eta/(64B))^(2t)-1
       < eta.

This proves the uniform bound. The proof handles root perturbations and arithmetic perturbations separately; it does not rely on small product-tree depth.

### 2.4 Work, setup, and storage

Stirling's estimate gives B,L_gamma=Theta((p+1)/log(p+2)). There are ceil(N/B) anchors, each costing O(B), two O(L_gamma) root preparations, and O(N) within-block multiplications. Total: O(N+p) scalar arithmetic and O(N) storage if the full carrier is retained. Working precision is P=p+O(log p).

Pi is also charged. For example, Machin's identity pi=16 atan(1/5)-4 atan(1/239), alternating-series remainder bounds, O(P) terms, and directed-rounding evaluation with O(log P) extra guard bits produce the required interval. This is O(P) scalar arithmetic at P+O(log P) bits. It is not a free pi oracle. The checker below isolates the carrier arithmetic and uses a high-precision pi reference; it does not purport to implement this outward-rounded pi certificate.

Exact grid/argument/index preparation uses O(N) operations on O(log N)-bit integers, with their bit cost charged separately. Carrier output writes are included.

The same reanchoring lemma generates the full 2q-th-root lookup table exp(i*pi*s/q), 0<=s<2q, in O(q+p) scalar arithmetic. At anchors reduce angles to [-pi,pi]; the one geometric transition remains unit modulus. All quadratic/linear phase exponents in the inherited decoder can then be evaluated by exact modular indexing into this certified table. This supplies uniformly accurate phase values without iterating one approximate root q times without resets. Short-FFT twiddles come from the same table.

## 3. Centered, rank-independent numerical envelope

Write Z=pi(N-1)/(2q)<=pi/2 and Delta=pi(M-1)/q. Active block arguments satisfy |z_b|<=Z. Inactive blocks have exactly zero padded input and can be skipped. Form centered arguments by the exact rational numerator

    z_b=pi*(2bM-(N-1))/(2q),

rather than cancellation of two separately rounded fractions. Local arguments are delta_t=pi*t/q. Exact zero arguments remain zero.

A safe family of uniform majorants is

    m_0=1,
    m_j=exp(pi^2/32)*(pi/4)^j/j! for j>=1,
    B_c=m_0+2 sum_(j>=1)m_j
       =1+2 exp(pi^2/32)(exp(pi/4)-1)
       =4.2487755731188234142879... .

Let ell_0=1 and

    ell_h=exp(Delta^2/[4(h+1)])*(Delta/2)^h/h!, h>=1,
    ell_-h=ell_h,
    Lambda_H=sum_(|h|<=H)ell_h.

For every retained order, define

    v_r=sum_(|h|<=H)m_|r-h| ell_h,
    B_RH=sum_(r=0)^(R-1)w_r v_r, w_0=1, w_r=2 for r>=1.

Both sequences are symmetric. Hence v_-r=v_r and convolution summation proves the sharper exact envelope

    B_RH <= sum_(r in Z)v_r = B_c Lambda_H.

There is no extra factor two and no leading R. For fixed H and bounded Delta this is a constant. This is a **sum of uniform majorants**; replacing it with an arbitrary pointwise sum-of-Bessel-values bound inside a sum of l2 norms would be unjustified. The parallel kernel audit derives sharper pointwise constants, which have a different role.

Let C be the block compression map, D=U_q C*, X=||x||2, and G_h=C diag(J_h(delta))x. Then

    ||G_h||2 <= sqrt(M) ell_h X,
    d_r=sum_h diag(J_(r-h)(z_b))G_h,
    ||d_r||2 <= sqrt(M) v_r X.

These inequalities apply to signed centered arguments without change.

## 4. Complete sufficient row-error ledger

The required inherited decoder interface is the one already isolated in the v11 audit:

    ||Dhat(d)-D(d)||infinity <= epsilon_D ||d||2
    for every independently supplied represented summary d,
    epsilon_D = C_D u log(q) sqrt(q).

A full-row compression-plus-decoder bound does not alone imply this interface. Input conversion into the decoder's storage type must be included. A sufficient implementation uses a radix-2 FFT with O(u)-accurate twiddles, uniformly O(u)-accurate phase tables, and balanced addition scans. Stagewise FFT perturbation gives O(u log K) l2 error. The exact gauged forcing has l1 norm <=2 sqrt(q)||d||2, giving the displayed scan bound. Exact modular indices, a certified normalizer, adequate exponent range, and u log q small are assumptions of this explicit contract.

Assume local channels, block coefficients, and summary synthesis satisfy

    ||Ghat_h-G_h||2 <= e_G sqrt(M) ell_h X,
    ||fhat_rh-J_(r-h)(z)||infinity <= e_B m_|r-h|,
    ||dhat_r-sum_h diag(fhat_rh)Ghat_h||2
       <= e_S sum_h ||diag(fhat_rh)Ghat_h||2.

Set rho=(1+e_G)(1+e_B)(1+e_S)-1. Then

    ||dhat_r-d_r||2 <= rho sqrt(M)v_r X,
    ||Dhat(dhat_r)-D(d_r)||infinity
       <= [epsilon_D sqrt(M)(1+rho)+M rho] v_r X.

For the Clenshaw output, assume an absolute allowance chi times the absolute sum of its supplied coefficients. A sufficient explicit allowance is

    chi = t*(1+3R^2/2)/(1-t*(1+3R^2/2)) + e_x*(R-1)^2,

where t=O(u) bounds the local residuals of the specified complex recurrence, e_x bounds Chebyshev-node rounding, both exact and rounded nodes lie in [-1,1], and t*(1+3R^2/2)<1. The proof uses |T_r|<=1 and |U_r|<=r+1; node error uses |T'_r|<=r^2. Compute nodes from exact integer residuals and clamp a correctly rounded endpoint to [-1,1] if needed.

Let eta_C bound the absolute carrier error, sigma_N the relative error in sqrt(q/N), and nu_F the relative normwise error of the final multiplication. Put

    sigma_F=(1+eta_C)(1+sigma_N)(1+nu_F)-1,
    A=epsilon_D sqrt(M)(1+rho)+M rho,
    P0=(1+rho)(M+epsilon_D sqrt(M)).

The complete error relative to the *same-state ideal truncated fused row* is

    eta_fp <= sqrt(q/N) B_RH X
        * { A + [(1+sigma_F)(1+chi)-1] P0 }.             (FP)

This includes local channels, summary coefficients, synthesis, decoder, Clenshaw, nodes, output carrier, normalizer, and final multiplication. Deterministic truncation/fusion bias and stochastic row error remain separate. No unbiasedness of the rounded row is needed.

With balanced channel reductions, certified Bessel preparation, fixed H, carrier eta_C=O(u) from Section 2, and accurate normalizers,

    e_G=O(u log M), e_B=O(u), e_S=O(u log(2H+1)),
    e_x=O(u), sigma_N=O(u), nu_F=O(u),

so (FP) becomes

    eta_fp=O(B_c Lambda_H
       [u log(q) sqrt(Mq)+u M(log M+R^2+1)] X).

For M=Theta(log N), R=Theta(log N/log log N), the first term dominates. To allocate a fixed fraction of g sqrt(M/N)X to numerical error it suffices that

    u <= c*g/(N log N),
    b >= log2(N log N/g)+O(1),

with the constant depending on the specified operation contracts. Working/guard precision is b+O(log b+log(R+H+1)). This preserves the repaired leading v11 order. The unanchored carrier at the same precision does not inherit this conclusion automatically.

Aggregation must enlarge its row allowance for eta_fp. The source's robust radius excludes this term. Finite-precision norms, threshold construction, and grid classification require outward margins or exact integer/rational comparisons to implement the inherited probability contract; the supplied library code does not establish them. This report certifies the deterministic row-composition implication, not unexamined majority-grid decisions.

## 5. Charged Bessel generation

For integer m>=0 use the classical factorial series

    J_m(z)=(z/2)^m/m! * sum_(j>=0)
          (-z^2/4)^j m!/[j!(m+j)!].

For |z|<=Z0, a=Z0/2, the tail after j=L_B-1 satisfies

    |tail| <= (|z|/2)^m/m! * exp(a^2)*a^(2L_B)/(L_B!)^2.

This follows from m!/(m+j)!<=1/j! and (L_B+l)!>=L_B!l!. For all relevant active centered/local arguments one can use Z0=pi/2 in the inherited M^2<=q regime (small identity cases handled separately), or a rational upper bound such as 8/5. Choose L_B so this dimensionless tail is <=u/16. Then L_B=O((b+1)/log(b+2)).

Generate leading factors across m by p_(m+1)=p_m*z/[2(m+1)], and series terms by

    t_(j+1)=-t_j*z^2/[4(j+1)(m+j+1)].

The sum of absolute terms is <=exp(a^2), a fixed constant. Relative argument errors O(u/(R+H+L_B+1)), from certified pi and exact rational-grid numerators, affect an order-m leading power by O(mu/(R+H+L_B+1)). The O(m+L_B) term-generation/addition paths are therefore controlled by b+O(log(R+H+L_B+1)) guard bits, giving the required O(u)m_m or O(u)ell_h absolute majorized error. Very small nonzero z is handled through relative argument preparation; at z=0 the known exact values are used. This is not a uniform relative-error claim for a Bessel value near a zero.

Negative orders and signed arguments use exact parity. A single per-block table of orders 0,...,R+H-1 supplies every shifted order r-h. Charge

    O(K(R+H)L_B+M(H+1)L_B)

scalar operations and O(K(R+H)+M(H+1)) coefficient storage, plus O(K(R+H)+M(H+1)) leading-factor preparation. The simpler redundant signed-channel implementation has a larger constant but the same fixed-H order. Adequate exponent range is required: the magnitude exponents may reach O((R+H+L_B)(log q+log(R+H+L_B))) in naive no-underflow evaluation. Alternatively discard terms only with a certified accumulated bound.

For b=Theta(log N), R,L_B=Theta(log N/log log N), K=Theta(N/log N), the dominant block coefficient work is

    O(K R L_B)=O(N log N/(log log N)^2)=o(RN).

The source's O((2H+1)RK) fusion line charges applications/synthesis, not this coefficient preparation. Its proxy omits the special-function work and cannot determine true constant-factor speedups. Finite factorial-series evaluation is approximate; it does not supply a finite exact Bessel oracle.

The classical series and identities were checked against NIST DLMF: https://dlmf.nist.gov/10.2.E2 , https://dlmf.nist.gov/10.12 , and https://dlmf.nist.gov/10.23.E2 . The error estimates and resource composition here are independently derived.

## 6. Complete arithmetic ledger and bit-model boundary

For a fixed number of local channels and randomized rows, a constructive replacement pays for:

- O(N) exact grid and O(q) modular phase indexing on O(log N)-bit integers.
- O(q+b) certified dyadic-root/carrier setup using reanchored Taylor evaluation, plus O(b) pi preparation. Shared tables may be reused across rows.
- O(q) local input/channel preparation and balanced reductions.
- O(K R L_B+M(H+1)L_B) Bessel preparation, with the charged guards above.
- O(RK) summary synthesis; O(RK log K) short FFTs.
- O(Rq) full gauged addition scans and O(RN) streamed Clenshaw updates.
- O(N) final carrier applications/output writes per row.
- Certified square roots/normalizers via bounded-interval Newton iteration, O(log b) scalar steps with growing precision; robust norm/grid work charged separately.

With the established scaling, this is O(RN) scalar arithmetic. It removes no rank-R scans or short FFT bank, and proves no O(N log log N) total algorithm. O(N) coefficient/work storage holds when R=O(M).

If Mul(P) is the cost of P-bit multiplication, a conservative bit ledger multiplies the scalar-arithmetic total by the actual P-bit operation costs and adds exact-integer indexing, exponent bookkeeping, input/output conversion, and random-state generation. At P=b+O(log b), one may write an arithmetic part O(RN Mul(P)) under a model where divisions are implemented within that cost up to stated logarithmic overhead; do not silently identify it with O(RN) bit operations. No exact Fourier or integer-multiplication improvement follows.

The previous blocked polynomial-prefix construction remains an exact-field-arithmetic subroutine without a finite-precision certificate. Centering reduces some constants but provides no automatic stability proof for its monomial conversion, product/remainder trees, or multipoint evaluation. This report does not import that uncertified subroutine into (FP).

## 7. Forward recurrence remains a separate obstruction

For any positive 0<z<1, the seed perturbation recurrence

    e_0=0, e_1=delta,
    e_(r+1)=(2r/z)e_r-e_(r-1)

has

    |e_R| >= |delta| (R-1)! z^(-(R-1)).

The elementary positivity/monotonicity induction from the earlier bridge audit applies unchanged. Negative z reduces to the same absolute amplification by alternating signs. Centered grid arguments may be zero, requiring a separate exact branch, and their nonzero spacing is controlled by pi/(2q), rather than the old pi/K mode.

Independent controls give:

- N=511, M=8, R=11: minimum nonzero |z_b|=pi/512; log2 lower amplification 95.27609982, actual 105.27608760.
- N=4095, M=8, R=14: minimum pi/4096; lower 167.06644527, actual 180.06644507.
- N=65535, M=16, R=19: minimum pi/65536; lower 310.78059798, actual 328.78059798.

These are allowed seed-error amplification controls, not evidence that SciPy incurs those errors or that v12 runs this recurrence. Any proposed forward-order replacement for separately generated coefficients must pay this conditioning cost or use a different, proved-stable formulation.

## 8. Reproducibility and exact scope of checks

Run `python independent_precision_checks.py` with Python and mpmath. `SOURCE_RESULT_SUMMARY.json` is copied inert source data for parameter comparison. The checker imports no uploaded code and uses no source implementation as an oracle.

Saved results:

- 24 source rank rows and 28 complete v12 parameter choices independently reproduce.
- Exact integer grids and 32,896 carrier transition identities at N=1,...,257; largest high-precision discrepancy about 4.24e-111.
- 12 adversarial product-error-model controls demonstrate linear accumulation despite logarithmic tree depth.
- 12 explicitly rounded reanchored controls at p=24,53,80 and N=37,257,1025,4095; largest observed error/2^-p approximately 0.000172184.
- 287 factorial-series Bessel controls at orders 0,...,40, including negative, zero, endpoint, and tiny arguments. Fifteen series terms suffice for the checked 80-bit majorized target.
- Four symmetric-envelope convolution mass checks and three forward-recurrence amplification controls.

The mpmath reference and explicit round-to-nearest simulator are numerical corroboration. They are not interval proofs, end-to-end performance benchmarks, or a production arbitrary-precision FFT implementation. The analytic proofs above supply the sufficient error bounds; an implementation certificate must verify each stated primitive and aggregation contract.
