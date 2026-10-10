# Rational approximation and the algebraic-encoding boundary

Date: 10 October 2026. Separate supplement to the pinned amplitude-field theorem v2. This supplement does not change that theorem or any accepted approximate-transform result.

## Conclusions

For every odd prime p, a fixed three-phase palette realizes arbitrarily accurate entrywise approximations to the entire unnormalized Fourier matrix Fp using nonnegative rational amplitudes. The coefficients can be bounded independently of p, and B fractional bits suffice existentially for entrywise error at most 2^(−B). The depth-one construction still has up to 2p²−4p+3 edges and quadratic evaluation work.

Conversely, two phases cannot approximate arbitrarily well, even with arbitrary nonnegative real amplitudes. The exact best uniform root-to-cone error is

    c_p = 1                         if p ≡ 3 (mod 4),
    c_p = cos(π/(2p))               if p ≡ 1 (mod 4).

This is an entrywise minimax infimum. A separate, non-sharp operator argument gives relative spectral error at least sqrt((p−1)/(6p)) ≥ 1/3 for every two-phase depth-one realization.

Thus the exact rational-amplitude coverage gate is not stable under arbitrarily small error. It cannot be applied unchanged to an approximate packed transform. Neither the approximation construction nor the field-encoding observation is a speedup or a historically novel claim.

## 1. Model and norms

Take ζ=exp(2πi/p), p an odd prime, and Fp[i,j]=ζ^(ij), for 0≤i,j<p. Phases are selected from the actual pth roots. All amplitudes are nonnegative real numbers; for the upper construction they are nonnegative rationals. Zero-amplitude terms are omitted, so every retained edge has strictly positive amplitude. Parallel direct input-output edges are charged individually. No endpoint phases or normalization constants are free.

For a complex matrix E, write ||E||_max=max_(i,j)|E_ij|, ||E||_F for the Frobenius norm, and ||E||₂ for the spectral norm. We use

    ||E||₂ ≤ ||E||_F ≤ p ||E||_max,
    ||Fp||₂ = sqrt(p).

The induced infinity norm is different from the entrywise maximum norm. These are standard norm comparisons, also discussed in [Higham, Accuracy and Stability of Numerical Algorithms, Chapter 6](https://epubs.siam.org/doi/10.1137/1.9780898718027.ch6).

## 2. A uniformly well-conditioned three-phase palette

Set

    a = floor((p+1)/3),     S = {0, a, p−a}.

For p=3 this is the entire phase set. For every odd prime p≥5, write p=3m+1 or 3m+2. The three circular gaps in exponent units are a,p−2a,a, and direct substitution gives

    p/5 ≤ each gap ≤ 3p/7.

The smallest ratio 1/5 occurs at p=5, and the largest 3/7 at p=7. The p=3 gaps also satisfy these bounds. In angular units each gap Δ therefore belongs to [2π/5,6π/7], strictly below π. Since sin(π/7)≥2/7 by concavity of sine on [0,π/2],

    sin Δ ≥ 2/7.

Every target root lies on or between two adjacent palette rays u=exp(iα) and v=exp(i(α+Δ)). If its angle is α+t, where 0≤t≤Δ, the exact decomposition is

    exp(i(α+t)) = A u + B v,
    A = sin(Δ−t)/sin Δ,
    B = sin(t)/sin Δ.

Both coefficients are nonnegative, and

    0 ≤ A,B ≤ 7/2.

A palette target uses its one exact coefficient 1. Every other target uses two strictly positive real coefficients. This is elementary planar positive-cone geometry. The field-constrained exact theorem requires more than this planar argument; here rational approximation removes that exact constraint.

The elementary positive-basis background is classical. For a modern primary-source discussion see [Hare and Song, On the Cardinality of Positively Linearly Independent Sets](https://arxiv.org/abs/1509.07496), alongside the Davis reference in the core theorem. These sources are context, not an attribution of the precise Fourier quantization statement.

## 3. Dyadic quantization: entrywise accuracy and coefficient bits

Fix an integer B≥1. For each nonnegative coefficient x∈[0,7/2], choose the nearest nonnegative multiple q of 2^(−B), with ties to even. Then

    |q−x| ≤ 2^(−B−1).

Two coefficients occur in an entry and the phases have modulus one, so quantizing both gives

    |q₁u+q₂v−ζ^k| ≤ |q₁−A|+|q₂−B| ≤ 2^(−B).

This bound uses nearest rounding. Flooring both coefficients would only justify a bound below 2·2^(−B).

Because 7/2 itself lies on the dyadic grid for B≥1, 0≤q≤7/2. Each amplitude has at most B fractional bits and two integer bits, apart from fixed encoding overhead. Palette coefficients 1 remain exact. Therefore a depth-one positive-rational matrix M_B exists with

    ||M_B−Fp||_max ≤ 2^(−B),
    number of edges ≤ 2p²−4p+3.

The edge count is an upper bound after quantization: very small coefficients may round to zero and be omitted. Before quantization the count equals 2p²−4p+3, because phase 0 occurs 2p−1 times and each of the two other palette phases occurs p−1 times. Every other entry uses two edges.

### Certified generation without an exact-rounding oracle

Nearest rounding of the exact irrational coefficient states an existence theorem. It need not be implemented by deciding an exact half-grid equality. A constructive version adds two guard bits:

1. Compute a rational enclosing interval for each exact coefficient, of width less than 2^(−B−4).
2. Round its midpoint to the nearest nonnegative multiple of 2^(−B−2), clipping a negative rounded value to zero.
3. The per-coefficient error is less than 2^(−B−2), so the two-term entry error is strictly below 2^(−B−1), in particular below 2^(−B).

The two added fractional bits change neither the O(log(1/ε)) entrywise precision statement nor the field: all retained amplitudes are rational. The fresh controls below implement this guarded construction with exact rational interval certificates.

For p≥5 the exact field theorem with K=Q demands all p phases, whereas the three fixed phases above approach Fp to any positive tolerance. The limiting coefficient vector need not lie in Q. This elementary density phenomenon is the precise reason an exact field obstruction cannot simply be reused as an approximate lower bound.

## 4. Matrix error, normalization, and phase precision

The entrywise estimate implies

    ||M_B−Fp||₂ ≤ ||M_B−Fp||_F ≤ p·2^(−B),
    ||M_B−Fp||₂ / ||Fp||₂ ≤ sqrt(p)·2^(−B).

Thus relative spectral error at most τ is guaranteed by

    B ≥ ceil(log₂(sqrt(p)/τ)).

An entrywise O(log(1/ε)) coefficient-bit claim therefore becomes O(log p+log(1/τ)) when a relative operator guarantee is required. The argument does not silently identify these two accuracy notions.

For the normalized target U=Fp/sqrt(p), one option is to approximate its cone coefficients A/sqrt(p),B/sqrt(p) directly by rationals. With dyadic step 2^(−B), the entrywise error is again at most 2^(−B), and absolute operator error is at most p·2^(−B), so B≥ceil(log₂(p/τ)) suffices. This preserves the rational-amplitude model. Alternatively, one can scale the unnormalized approximant by 1/sqrt(p), but that scaling is a separate generally irrational operation and must be explicitly allowed and charged.

The construction so far assumes exact pth-root phases. If a retained phase is also perturbed by at most η in complex modulus, two quantized coefficients bounded by 4 each add at most 8η entrywise error. Floating-point accumulation or finite-word execution contributes further errors requiring its own analysis. This supplement is not an end-to-end stability theorem for a numerical evaluator.

## 5. The sharp two-phase entrywise barrier

For a palette S of at most two pth roots, let C(S) be its cone of nonnegative real combinations. Define

    e(S) = max_(0≤k<p) distance(ζ^k,C(S)),
    c_p = min_(|S|≤2) e(S).

The same number is the infimum if coefficients are restricted to nonnegative rationals, since rational points are dense in each such cone and only finitely many targets occur. Attainment with rational coefficients is not asserted.

### A quick uniform barrier

Every two-ray cone is contained in a closed half-plane through zero. Choose a unit normal n such that Re(conj(n)w)≥0 for all w in the cone. Some pth root lies within angular distance π/p of −n, so its projection is at most −cos(π/p). Its distance to the cone is at least cos(π/p). Hence c_p≥cos(π/p).

### Exact minimax value

Rotate and, if necessary, reflect the palette to {1,ζ^a}, where 1≤a≤(p−1)/2. The shorter cone has angular width Δ=2πa/p. A unit root in the polar cone has closest cone point zero and distance exactly one. The polar arc has center

    β = π+Δ/2

and angular length π−Δ.

If a≤(p−3)/2, that arc has length at least 3π/p, exceeding the root spacing 2π/p, and contains a root. Thus e(S)=1. It remains to take a=(p−1)/2:

- If p≡3 mod4, then a is odd, and (p+a)/2 is an integer. The polar center β is itself the angle of a pth root, so e(S)=1.
- If p≡1 mod4, then a is even. The polar center is halfway between adjacent roots; those nearest roots are at angular distance π/p from the center. The polar half-width is only π/(2p), so neither is in the polar cone. Their closest boundary-ray projection has perpendicular distance sin(π/2−π/(2p))=cos(π/(2p)). Every other root is at least as close to the cone. Thus e(S)=cos(π/(2p)).

A singleton palette cannot improve the optimum. This proves the displayed formula for c_p. It includes p=3, where c_3=1. Examples are c_5=cos(π/10) and c_7=1.

This is sharp for worst-entry absolute approximation. It is not stated as the sharp matrix-operator barrier.

## 6. A separate conservative two-phase operator barrier

The following argument was proposed in the independent review and checked independently here. It strengthens the mere worst-entry obstruction without claiming operator optimality.

Let M have every entry in a fixed cone generated by at most two pth-root rays. Choose a containing half-plane and let the normal projection of target phase r be

    x_r = cos(θ+2πr/p).

Set Q=Σ_(x_r<0) x_r² and let m be the number of negative terms. Orthogonality of roots gives

    Σ_r x_r=0,     Σ_r x_r²=p/2,     m≤(p+1)/2.

Positive terms lie in [0,1], so their squared sum is at most their sum, which equals the absolute sum of the negative terms. Cauchy–Schwarz therefore gives

    p/2 ≤ Q + sqrt(mQ) ≤ Q + sqrt((p+1)Q/2).

If Q<p/6, the right side is strictly below

    p/6 + sqrt(p(p+1)/12) ≤ p/2,

where the last inequality is equivalent to p≥3. Hence Q≥p/6.

Every phase occurs at least p−1 times in Fp. Since an entry constrained to the half-plane incurs squared error at least x_r² whenever x_r<0,

    ||M−Fp||_F² ≥ (p−1)Q ≥ p(p−1)/6.

Finally ||E||₂≥||E||_F/sqrt(p), giving

    ||M−Fp||₂ / sqrt(p) ≥ sqrt((p−1)/(6p)) ≥ 1/3.

This holds with arbitrary nonnegative real amplitudes, so also with rational amplitudes. Combining it with the three-phase upper construction shows that three is the minimum global palette size for arbitrarily accurate relative-spectral approximation, and in particular for any target relative error below 1/3.

The hypothesis is a single global cone for all entries, as in depth one. A deeper network with two edge phases can create more than two path phases; the bound must not be transferred to such a network merely from its edge alphabet size. Free input/output phase gauges would also alter the model.

## 7. Cold costs and what one algebraic parameter can hide

Only p target phases need separate coefficient generation; all p² entries reuse their residue-class coefficients. Nevertheless generating the coefficients, constructing the p² labeled incidences, and applying the resulting dense-depth-one map are distinct charged tasks.

An elementary cold generator can use Machin's arctangent identity to enclose π and Taylor series on bounded angles to enclose sines. For Q=B+ceil(log₂p)+O(1), O(Q) terms suffice for each bounded-angle enclosure, with rational endpoints and a constant number of guard bits because every denominator sine is at least 2/7. One may carry common denominators so that the intermediate integers have O(Q² log Q) bits. This gives O(pQ) arithmetic operations on integers of that size for the coefficient table, followed by ordinary rational division/rounding. It is a conservative elementary generation account, not an optimized transcendental-evaluation bound or a unit-cost claim for growing integers.

The table has O(pB) coefficient bits, plus indexing overhead. Materializing all direct edges requires Θ(p²) records and Ω(p²) work; a literal bit representation includes O(log p+B) bits per record. Evaluation still performs Θ(p²) edge operations in the usual scalar model. An on-demand edge stream can reduce stored graph data but not this work count. No O(p log p), O(p log log p), or packed-evaluation advantage follows.

For comparison with the exact field theorem, consider its explicit exact triangle with a=(p−1)/2 and λ=2cos(π/p). Define

    P₀(t)=1,  P₁(t)=t,  Pₙ(t)=tPₙ₋₁(t)−Pₙ₋₂(t).

The two exact cone coefficients for target ζ^k, 1≤k≤a, are P₂ₖ(λ) and P₂ₖ₋₁(λ), using Pₙ(2cos x)=sin((n+1)x)/sin x. Thus one algebraic generator suffices, but Q(λ)=E+ has degree (p−1)/2. Conversely, applying the core theorem to the field generated by all amplitudes in any exact three-phase Fp realization shows that this field must contain E+.

More generally an exact s-phase realization with finite-degree amplitude field K forces [K:Q]≥(p−1)/(s−1). Parameter count therefore does not bound field degree or coefficient-description cost. At the same time, a large algebraic field degree does not automatically become a lower bound in an exact complex-RAM model that already grants arbitrary complex constants as unit-cost scalars. The computation model must decide which coefficient costs are charged.

## 8. Fresh controls and source position

`fresh_rational_controls.py` is standalone, newly authored, and imports only the Python standard library. It does not import the exact-control program or any uploaded/source-package code. All equalities, signs, rounding checks, and error upper bounds use rational arithmetic. Machin/Taylor intervals certify trigonometric values; the squared complex error is expanded into a rational interval rather than compared using a floating-point tolerance.

The construction controls cover 55 (p,B) cases: p=3,5,7,11,13,17,19,29,43,67,101 and B=2,4,8,12,20. They check 1,575 target-root certificates, all 92,015 Fourier entries, the amplitude and bit bounds, the guarded quantization error, and the depth-one edge upper bound. The separate two-phase test enumerates every rotation/reflection separation class at all 25 odd primes through 101, equivalent to 37,417 two-element palettes, and verifies the sharp entrywise minimax expression by exact angle ordering. Additional controls test 600 half-plane orientations for the conservative operator argument at p=3,5,7,11,13,17,19.

Final exact totals and certificates are in `FRESH_RATIONAL_RESULTS.json` and `FRESH_RATIONAL_RUN.log`. Finite orientation checks support the controls; the analytic argument above proves the all-orientation operator claim.

The literature check found the established positive-basis and matrix-norm frameworks cited above. The coefficient-density observation and planar construction are elementary. The sharp discrete two-ray expression and this combined cost-accounted presentation have not been historically priority-cleared. The appropriate status is a proved scope/robustness supplement with unresolved historical novelty, not a new fast-transform theorem or a replacement for the accepted approximate packed theorem.
