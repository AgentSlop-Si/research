# Joint diagonal sums in the square-packed Mersenne route

17 October 2026. Bounded successor to the accepted base-conversion and independent-block-product accounts. Candidate pending independent review.

## Result

Replacing M² independent block products by an exact linear-bilinear diagonal-sum kernel is a real algebraic improvement: the least number of scalar products is 2M−1 over the rationals. A complete elementary evaluation/interpolation construction attaining this count is given below, with its coefficient growth, integer divisions, conversion and binary reconstruction charged.

That improvement does not provide a uniform strict N log N child-potential contraction for the specified square-packed route. Here M² base-Q digits are packed into M binary-encoded blocks, Q=(2^m−1)^d, and every nonzero linear form is separately materialized as a fixed-capacity integer. Each scalar child needs at least the original block width. For arbitrary growing parameter sequences, the ratio of the resulting child potential to the parent potential has liminf at least 1. If the inherited full-scan conversion is required to stay within O(N log N), the liminf is at least 3/2; if M also grows, it is at least 2.

These are lower bounds on the declared recursive invoice, not direct lower bounds on running time or on all integer multiplication algorithms. A better jointly evaluated, nonlinear, carry-aware or differently represented interface is not excluded. The complete original speedup route remains open.

## 1. Source linkage and owner check

The primary source is the pinned 15 October experiment, FINAL_REPORT.md, especially §2 (no matrix kernel supplied) and §7 (paid matrix reduction remains open), read at repository commit e3f3fd2fde808e577989907f00740c16905dbeb1:

https://github.com/AgentSlop-Si/research/blob/e3f3fd2fde808e577989907f00740c16905dbeb1/math/finalized/2026-10-15-experiment-reviews/mersenne_independent_finalization/FINAL_REPORT.md

The immediately preceding accepted report, “A paid streamed divider for the exact grouped Mersenne radix,” §6, explicitly leaves a jointly evaluated diagonal-sum kernel open after charging M² independently executed products. This successor addresses that documented missing kernel only in the integer-linear bilinear, separately materialized scalar-child grammar. It does not repeat the predecessor's divider proof or either already-accounted Θ(N²/m) converter.

The full pinned open-record index was inspected, including all 237 titles and the complete records matching Mersenne, radix, packing, base and matrix terms. No exact native owner for the 15 October Mersenne experiment was identified. FUS-12 is a theorem-precision numerical Fourier executor; PACK-01 is a particular accepted-refusal source-recovery gate; ALG-025/026 are finite-word Reif comparisons; ALG-075 concerns a separate historical thin-rectangle construction. None can honestly own this result. The previously distinguished archived ALG-072 is not reopened. OWNER_CELL_CHANGE_PROPOSAL.json is empty. No new canonical research ID, status, score or priority is proposed.

The relevant predecessor source hashes and pinned repository identities are in SOURCE_REGISTER.json. Pre-existing reports were read as static evidence; their programs were not executed. Fresh checks in this packet test exact arithmetic only.

## 2. Parameters, target and cost grammar

Let m≥2, d≥1, and M≥2 be integers. Define

    p=2^m−1, Q=p^d, w=log2 Q, R=Q^M,
    n=M²w, N=ceil(n), h0=Mw=n/M,
    h=bit_length(R−1)=ceil(h0), C=dmM².

The equalities for h and N hold because the odd integers R and Q^(M²) are not powers of two. An input 0≤X<Q^(M²)=R^M has canonical base-R blocks x_0,...,x_(M−1), each in [0,R). Define y similarly. The desired complete coefficient output is

    s_k=sum_(i+j=k) x_i y_j, 0≤k≤2M−2,
    XY=sum_k s_k R^k.

Thus the output has 2M−1 coefficients, not the M² entries of an outer-product matrix. The coefficients satisfy 0≤s_k≤M(R−1)² and have O(h+log M) bits.

This report's bilinear grammar is

    z_t=A_t(x) B_t(y), 1≤t≤r,
    s_k=sum_t c_(k,t) z_t,

where A_t and B_t are nonzero integer linear forms and c_(k,t) are rational constants. Every scalar product is invoked independently; each input linear form is materialized in a fixed-capacity signed integer buffer sufficient for every permitted block vector. A child contributes Φ(H_t)=H_t log2 H_t to the declared one-operand recursive potential, where H_t is the maximum of its two allocated magnitude widths. Signs, coefficients, additions, exact divisions, copies, storage and all other work are paid separately and nonnegatively.

The grammar permits shared linear preparation, but it does not permit merging the nonlinear work of multiple scalar-product children while still billing them as independent recursive calls. The potential is a recurrence-accounting device, not an assertion that every H-bit multiplication costs Ω(H log H). Rational input forms can be accommodated by first clearing each form's denominators and recording those factors in the decoder; their integer numerator buffers remain paid. An algorithm using a different factored/fractional interface is outside this specific width contract.

Primality of p is unused. Any application requiring it still owes selection and certification; there is no assumption of an all-size supply of Mersenne primes.

## 3. Sharp bilinear count and unavoidable allocated width

### Theorem 1: exact full-coefficient bilinear rank is 2M−1

Suppose the displayed kernel is correct for every pair of block vectors in [0,R)^M. That domain includes the standard basis vectors e_i and e_j. Their convolution is exactly e_(i+j). Every output of the bilinear formula belongs to the rational span of its r decoder columns c_t. Taking all basis pairs shows that this span contains every standard basis vector of Q^(2M−1). Therefore r≥2M−1.

No positivity assumption on intermediate forms or decoder coefficients is used. Cancellations do not invalidate the span argument. The lower bound only concerns the full vector of coefficient outputs and the stipulated scalar products.

For an upper bound, evaluate the degree-(M−1) input polynomials at r=2M−1 distinct rational points, multiply their values, then interpolate their degree-at-most-(2M−2) product. The concrete integer-point construction in §5 proves attainability with integer input forms and rational output coefficients. Hence the rank is exactly 2M−1 in this grammar.

### Lemma 2: every nonzero child requires H_t≥h

Choose a nonzero coefficient a_j in A_t. The permitted input with x_j=R−1 and all other entries zero gives |A_t(x)|=|a_j|(R−1)≥R−1. Its full-domain magnitude buffer therefore needs at least h bits. The same applies to B_t. Thus H_t≥h for every active child.

This is a fixed-capacity bound. The maximizing input can differ by child, and no simultaneous large-value claim is made. An adaptive implementation that skips a zero form or shortens its actual child may have a different data-dependent invoice; this theorem does not rule it out. Likewise an exact denominator cannot erase the cost of an explicitly materialized numerator simply by changing the numerical scale.

Consequently the complete child invoice has the necessary lower bound

    P_child=sum_t Φ(H_t) ≥ (2M−1) h log2 h.

## 4. Square packing does not yield a fixed potential contraction

First ignore harmless ceilings and put

    ρ0=((2M−1)h0 log2 h0)/(n log2 n)
       =(2−1/M) [log2(Mw)/log2(M²w)].

Since w=d log2 p≥log2 3>1,

    ρ0 ≥ (2−1/M)/2 = 1−1/(2M).

For fixed M and n→∞, w→∞ and ρ0→2−1/M≥3/2. For unbounded M, the displayed inequality gives liminf at least 1. Together these prove, uniformly over all sequences n→∞, liminf ρ0≥1: given ε>0, choose a finite cutoff on M so that all larger M satisfy ρ0≥1−ε, then use the fixed-M limit uniformly on the remaining finite set.

The actual parent has N=ceil(n). Since h≥h0,

    P_child/Φ(N) ≥ ρ0 · [n log2 n/(N log2 N)].

The bracket tends uniformly to 1 as n→∞, proving

    liminf_(N→∞) P_child/Φ(N) ≥ 1.

Therefore there is no constant η>0 such that this declared invoice satisfies P_child≤(1−η)Φ(N) at all sufficiently large sizes in an admitted growing parameter family. This closes only the fixed strict contraction gate. A noncontracting potential is not itself an algorithmic lower bound, and no conclusion about every possible solution of a more detailed recurrence is asserted.

### The elementary-conversion tradeoff strengthens the conclusion

For the inherited balanced full-scan converter take M to be a power of two, so its M² grouped positions meet the accepted power-of-two leaf contract. That converter's bit work is Θ(C²/m). Because

    C/n = m/log2 p ∈(1,2],
    C²/m = C·dM² = Θ(n dM²),

keeping this prescribed conversion within O(N log N) requires dM²=O(log N). Requiring o(N log N) instead requires dM²=o(log N). These statements are about the inherited full-scan implementation and padded capacity, including zero-valued tree branches.

As d≥1, the O(N log N) condition implies log M=O(log log N)=o(log N). Hence

    log h0/log n = 1−log M/log n →1,
    liminf P_child/Φ(N) ≥3/2.

If M→∞ as well, the lower limit is at least 2. Thus within the accepted elementary representation path, making conversion cheap enough leaves a sizeable independent-child potential expansion, even after the sharp reduction from M² to 2M−1 products. This combines the earlier conversion result with the new joint-kernel rank/width ledger; it is not a repeated converter lower-bound claim.

## 5. A fully paid sharp-rank kernel

The following simple construction is deliberately not optimized. It demonstrates exact attainability and exposes the work that a rank count omits. It is classical polynomial evaluation/interpolation, not a new multiplication mechanism.

Let r=2M−1, t=0,...,r−1 and ℓ=ceil(log2 r). Compute

    u_t=sum_i x_i t^i, v_t=sum_i y_i t^i, z_t=u_t v_t.

A common safe operand capacity is

    H=h+ceil(log2 M)+(M−1)ℓ+1.

Indeed u_t and v_t are nonnegative and at most M(R−1)r^(M−1)<2^H. Ordinary Horner evaluation, multiplying only by the ℓ-bit constant t, costs O(Hℓ) per step using schoolbook shifts and additions. Both input transforms therefore cost O(M²Hℓ); their r products contribute r T(H) if uniformly padded to this common capacity. More refined individual capacities can only improve this upper bound.

For exact interpolation let D=(r−1)! and

    L_t(z)=product_(0≤j<r,j≠t)(z−j) / product_(j≠t)(t−j),
    a_(k,t)=D [z^k] L_t(z).

Because product_(j≠t)(t−j)=(-1)^(r−1−t)t!(r−1−t)!, all a_(k,t) are integers. The coefficient ℓ1 norm of the numerator polynomial is at most product_(j≠t)(1+j)≤r^(r−1), and D divided by the absolute denominator is binom(r−1,t)≤2^(r−1). Thus a uniform signed-magnitude bound is

    |a_(k,t)| < 2^K, K=(r−1)(ℓ+1)+1.

D also fits K bits. The decoder forms

    b_k=sum_t a_(k,t) z_t, s_k=b_k/D.

Polynomial interpolation proves divisibility by D and exact equality to the desired coefficient. It is not legitimate to omit these divisions merely because the final values are integral.

A safe accumulator capacity is B=2H+K+ceil(log2 r)+2. Multiplication by a K-bit integer constant, signed accumulation and ordinary binary long division by D give total decoder work O(M²BK). This includes the O(MBK) exact-division term. It uses elementary operations rather than silently calling another generic multiplication routine for those constants.

For cold setup, build each numerator polynomial by successive multiplication by (z−j), and the binomial factor by Pascal addition. There are O(M³) scalar coefficient updates with O(K)-bit values and O(ℓ)-bit multipliers. Constructing factorial D and all r² signed decoder coefficients by these same elementary operations fits the conservative upper bound O(M³K²). Storage for the decoder table is O(M²K). These are safe coarse bounds; no optimality is claimed.

Since K=O(M log M), B=O(H+K) and H=O(h+M log M), the overhead is explicitly finite and paid. Small point choices, special divisions and shared interpolation can improve it, but require their own account. The proof of rank minimality supplies no low-cost preparation/decoder theorem.

## 6. Full conversion, packing and reconstruction invoice

For dyadic M≥2, use the inherited balanced converter separately for each N-bit-padded input promised below Q^(M²). It outputs M² canonical Q-digits with C=dmM² allocated binary payload bits. Its Θ(C²/m) implementation cost is already proved in the accepted predecessor; this report imports that result, not a faster oracle.

Group consecutive M Q-digits into the M binary-encoded R-blocks. Direct Horner within each block replaces every multiplication by Q with d repetitions of v←(v<<m)−v. With fixed capacity dmM per block this costs O(d²mM²) per block, hence O(d²mM³) in total, plus copies. It lies within O(C²/m). Keeping groups factored instead changes the downstream input representation and requires a separately proved kernel.

After the diagonal kernel, evaluate sum_k s_k R^k by Horner. Each multiplication by R uses dM shift/subtract steps, followed by addition of the next s_k. There are fewer than 2M steps. The actual input product is below Q^(2M²), so every nonnegative high-to-low partial Horner value fits 2C bits. This gives O(dM²C)=O(C²/m) work, including coefficient additions and final binary output. No separate coefficient-carry pass is necessary in this specific evaluator; ordinary exact integer addition handles the overlaps. If a downstream caller instead requests canonical Q-digits before binary output, its carry/materialization work must be added rather than assumed away.

With the concrete sharp-rank kernel, a complete conservative recurrence account is

    T(N) ≤ r T(H)
           + O(C²/m + M²Hℓ + M²BK + M³K² + C),
    r=2M−1,
    H=h+ceil(log2 M)+(M−1)ℓ+1,
    ℓ=ceil(log2 r), K=(r−1)(ℓ+1)+1,
    B=2H+K+ceil(log2 r)+2.

This is conditional only on the chosen paid recursive multiplication routine T for the r children. If H is not smaller than N, the displayed construction is still a finite exact reduction, but it is not a shrinking recurrence. Coefficient setup is cold and charged once per call here; reusing it can remove that repeated setup term only in an explicitly warm model. Input reads, table/child-output traffic, signs, exact divisions and all 2N padded binary output bits fit the displayed bounds in a bit-array arithmetic model. This is not a certified fixed-tape implementation or a runtime benchmark.

For arbitrary A-bit inputs with dm≤A, choose the smallest dyadic M≥2 with M²≥ceil(A/[d(m−1)]) so the capacity promise covers every input. Then M²<4 ceil(A/[d(m−1)]) and the padded C is O(A). When dm>A, a one-group or other short-input branch needs its own account. The theorem above concerns the charged padded parent N, not an incorrectly rounded-down digit count.

## 7. Why the bound does not settle output-only multiplication

The final integer is a single scalar bilinear form

    XY=(sum_i R^i x_i)(sum_j R^j y_j).

As an unconstrained scalar-output bilinear map, this has rank one. Its direct implementation has one N-bit child, so it has no size reduction, but it decisively demonstrates why the 2M−1 coefficient-output lower bound cannot be copied to a carry-aware output-only interface.

Likewise, a nonlinear decoder, modular/extension representation, shared recursive product executor, adaptive short/zero-child policy, or a nonsquare packing rule can evade a hypothesis of the present theorem. Such an escape is not yet a faster algorithm, and the theorem does not prohibit it.

The precise remaining constructive lemma for a fixed-contraction route is: give a uniform exact interface for every permitted binary input pair, with a declared block representation and complete conversion/preparation/readout costs, whose actual recursive children have paid widths h_t<N and satisfy sum_t h_t log2 h_t≤(1−η)N log2 N for a fixed η>0, while the fully paid nonrecursive overhead is o(N log N) with sufficient quantified slack for the claimed recurrence. Alternatively, replace that sufficient certificate by a different complete recurrence proof establishing the desired end-to-end bound. The unresolved step is not merely reducing M² formal products to 2M−1.

## 8. Source comparison and verification boundary

The official GNU MP manual's “Toom 3-Way Multiplication” describes coefficient blocking, five point products replacing nine cross products, interpolation including exact divisions, and final overlapping-coefficient reconstruction. “Higher degree Toom'n'half” states the 2r−1 point count for equal r-piece splits. These confirm that the positive sharp-rank construction is classical. The present proof and cost specialization are supplied directly; no historical novelty or exhaustive priority claim is made.

https://gmplib.org/manual/Toom-3_002dWay-Multiplication

https://gmplib.org/manual/Higher-degree-Toom_0027n_0027half

Both pages were read directly on 17 October 2026. The comparison concerns the algebraic pattern, not a claim that this deliberately coarse decoder matches current GMP's implementation or performance.

Fresh standalone controls check the coefficient-output span, exact interpolation and integer denominators, the H/K/B bounds, complete original-base round trips and products, zero/carry-heavy cases, and the distinction between full coefficient and final scalar targets. Their exact counts appear in CONTROL_RESULTS.json. Python arbitrary-precision arithmetic is an exact oracle, not timing evidence. Neither historical programs nor the earlier candidate checkers were run.

Disposition: the specified linear-bilinear full-coefficient fixed-contraction gate has a complete candidate proof and paid upper construction. The broader Mersenne/adaptive-base multiplication route, improved conversion, output-only/shared kernel and any practical or asymptotic speed advantage remain open. No external write or table change was made.
