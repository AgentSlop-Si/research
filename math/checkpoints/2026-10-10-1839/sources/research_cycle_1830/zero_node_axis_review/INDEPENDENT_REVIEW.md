# Independent review: zero-node axis degeneration

10 October 2026. Verdict: **accept the frozen generic-axis theorem, its simultaneous legal-guard theorem, and the resulting uniform 7N/4 + O(1) Fourier signed-bank upper bound.** This is a separate result. The previously accepted 9N/5 theorem and the corrected direct-axis criterion remain unchanged. The previously rejected automatic reciprocal-coprime/full-axis shortcut remains rejected.

The exact reviewed inputs and output hashes are recorded in `REVIEW_RECEIPT.json`, `SOURCE_BINDINGS.json`, and `MANIFEST.sha256`. The main proof reviewed is the frozen `research_cycle_1824/axis_nonvanishing/AXIS_NONVANISHING_CANDIDATE.md` with SHA256 `2a22a99baf19cdc6bd78f90323b77be7b4c1b11c1866286f4a174a731ecb5040`; its companion degeneration lemma has SHA256 `41b8640186cafab43a27052dd628bd8799e15702bedb6462750fef5312ccfbae`. No author or predecessor program was imported or executed. All numerical controls were independently implemented in `independent_zero_node_audit.py`.

## 1. Accepted statement and exact scope

Let N be odd, q a primitive Nth root in characteristic zero, K=Q(q), d≥4, N≥8d−10, and m=N−d. The enlarged-envelope annihilator U defined in the author note lies in the actual whole-left recurrence kernel W. Its monic affine slice contains a nonempty K-defined open set of polynomials with nonzero constant coefficient, distinct roots, and full physical quotient-axis rank N. The same simultaneous open set is consequently nonempty on the monic slice of W.

With d=floor((N+10)/8), every odd N≥23 satisfies these hypotheses. The unchanged whole-left construction then represents the negative Fourier matrix by at most

    2N−2floor((N+10)/8)+2 = 7N/4+O(1)

individual permitted signed banks over the splitting field of one monic degree-m polynomial in K[t]. Orientation multiplicities are (m,1,1,m); both same-sign groups use its m distinct nonzero roots, both cross-sign singleton nodes are 1, and all beta parameters are 1. The splitting-field degree is at most m!.

This establishes a Fourier-specific uniform bank-count upper bound. It does not establish unrestricted minimality, N+O(1), a K-split realization, efficient preparation, scalar FFT complexity, or historical priority. The elementary polynomial, recurrence, reversal, separability, and open-set tools are classical ingredients; this review certifies their stated application and conclusion, not novelty.

## 2. Enlarged-envelope containment and dimensions

The proof correctly uses an enlarged, unconstrained envelope. There is no reliance on recurrence-rank saturation, the constrained triple space having full evaluation rank, or an endpoint relation surviving an unproved elimination.

For actual recurrence row (a,b), with a,b≥1 and a+b≤d−1, the inherited Gaussian product identity gives a chirp polynomial proportional to

    t^(a+b) F_(a,b)(t²),   deg F_(a,b)=d−2−b.

Its degree is 2d−4+a−b≤3d−7, while the ordinary component has degree d−2. The denominators D(q^k) are nonzero because 2≤j+k≤N−1. Thus every actual row belongs to the displayed E, and annihilators reverse the inclusion to U⊆W.

The number of envelope parameters is (3d−6)+(d−1)=4d−7, so

    dim U ≥ N−5d+8 ≥ 3d−2.

No injectivity of this envelope parameterization is needed. The polynomial pair P=0,R=D gives the all-ones coefficient functional directly, so every g in U vanishes at 1. This proves a fixed root only for the selected U, not for every possible recurrence kernel.

## 3. Sparse functionals and exact elimination endpoints

The step-one shift identity C_(k+1)=q^h rho^k C_k is correct because 2h=e modulo odd N. Each factor S−lambda maps P to q^h tP(rho t)−lambda P(t). Its first term supplies a unique new highest degree, so the map is injective and increases degree by exactly one whenever P is nonzero. This statement does not depend on lambda being nonzero.

For an envelope vector supported on {0,1,m}, the known zero interval is k=2 through m−1. Applying M of order d−1 yields k=2 through m−d, with exactly N−2d−1 points. The transformed chirp degree is at most 4d−8. The sufficient sparse-functional threshold N≥6d−6 follows from strict interpolation, and is implied by the theorem's N≥8d−10,d≥4. All rho-points are distinct: the interval length is below N, and 4d−8<N. Once P=0, the original ordinary polynomial R has m−2>d−2 distinct zeros and is zero.

Consequently delta_0, delta_1, and delta_m are independent modulo E. This is stronger than merely excluding the three individual coordinate vectors. It correctly implies that c_1 and c_m are independent on U_0=U∩{c_0=0}, because U_0^perp=E+span(delta_0). Thus U_0 contains full-degree polynomials, its fixed zero root is simple, and the two residual endpoint functionals are independent. The constant and leading guards on U are also nonzero.

## 4. Exact fixed divisors, including multiplicities

If x≠0 is a fixed root of U_0 over an algebraic closure, evaluation at x belongs to E+span(delta_0), so the scaled envelope equals x^kD(q^k) only on k=1 through m. The proof never improperly uses the omitted k=0 equality. Applying M L_x, of order 2d−2, leaves a pure chirp of degree at most 5d−9 with zeros at k=1 through m−2d+2. There are exactly N−3d+2 zeros. The decisive difference is

    (N−3d+2)−(5d−9)=N−8d+11≥1.

The degree is below N and the evaluation nodes are distinct, so P=0. The remaining equality R(q^k)=x^kD(q^k) satisfies an invertible constant-coefficient recurrence of order at most 2d−2. There are at least that many known consecutive zero differences. Its monic leading and nonzero constant coefficients justify forward and backward propagation, including the formerly missing position 0. Comparison at 0 and N yields x^N=1.

The author's cyclic-frequency argument correctly forces x=1. Its assertion that D has nonzero coefficients follows from the q-binomial product with all factor exponents strictly below N. A simpler independent check only uses D's two endpoints: if x=q^s, the nonzero constant and leading coefficients force s and s+d−2 modulo N into [0,d−2]. First s lies in that interval; then 2(d−2)<N prevents wraparound, so s+d−2≤d−2 and s=0.

For derivative evaluation at 1, M² has the same order, transformed degree, and zero count. Once P=0, the invertible recurrence propagates R(q^k)=kD(q^k) from k=1,...,m to all integers. At 0 and N this requires both R(1)=0 and R(1)=ND(1), impossible in characteristic zero. The positive-characteristic caveat is real; the universal theorem is correctly restricted to characteristic zero.

These results establish gcd(U_0)=t(t−1). They also establish gcd(U)=t−1: a root fixed on U is fixed on U_0, the constant functional excludes 0, and derivative evaluation excludes a double root at 1. Base extension causes no gap, since the linear annihilator and recurrence arguments are made over the algebraic closure and gcds commute with field extension.

## 5. Universal polynomial, primitivity, and reversal

The universal-polynomial lemma is valid. For a positive-degree linear polynomial space V with gcd(V)=1, the polynomial F_univ=ΣZ_i f_i has total parameter degree one. In a factorization over F[t,Z], one factor is independent of all Z_i and hence lies in F[t]; it must divide every f_i, so it is a unit. This proves irreducibility in the full polynomial ring.

Because F_univ has positive t-degree, a nonunit content in F[Z] would itself give a nontrivial factorization. It is therefore primitive as a polynomial in t over F[Z], and Gauss's lemma gives irreducibility over F(Z)[t]. This explicitly justifies the required primitivity step; irreducibility after a specialization is neither assumed nor needed.

The generic constant and leading coefficients are nonzero. Hence fixed-grade reversal has the same degree r, and any common factor with F_univ makes its reversal proportional to it. Applying reversal twice gives lambda²=1, so in characteristic zero lambda is one fixed sign. Comparing independent parameter coefficients places every f in the same reversal eigenspace.

For V=U_0/[t(t−1)], the endpoints are f(0)=−c_1(g) and leading_r(f)=c_m(g). Their independence excludes either reversal eigenspace, and consequently the reciprocal resultant is a nonzero parameter polynomial. Together with the two endpoint guards, this has a K-point because K is infinite. Normalization produces the claimed monic g_0=t(t−1)f in U_0. This proof needs no assertion that every pencil has a reciprocal-coprime member.

## 6. Quotient-axis duality at the zero node

The quotient axis is defined at zero-constant monic polynomials: every exponent is an ordinary nonnegative residue, and no inverse of t occurs. Taking a row linear combination indexed by A(t)=ΣA_a t^a gives the three conditions A mod g=0, A(1)=0, and J_N A mod g=0, exactly as claimed. This direct coefficient pairing extends the earlier duality beyond its nonzero-constant hypothesis without importing an inverse-remainder formula.

At g_0=t(t−1)f, divisibility g_0|A forces A(0)=0, so J_N A=t^N A(1/t). In the Laurent polynomial ring, f|J_N A reverses to rev_r(f)|A; since rev_r(f) has nonzero constant, removing powers of t loses no factor. Also g_0|A. The factors f and rev_r(f) are coprime, neither has a root at 0, and reciprocal coprimality excludes a root at 1. Thus

    t(t−1)f rev_r(f) divides A.

Its degree is 2m−2, exceeding N−1 by N−2d−1≥6d−11>0. Therefore A=0 and the quotient-axis rank is N. Repeated factors within f would not invalidate this argument; squarefreeness is not needed at the degeneration. The zero node is solely a point at which to evaluate a polynomial minor, never a node of a counted bank.

## 7. Simultaneous guards and descent

The monic slice U_1 is a nonempty affine linear space defined over K. The full-rank degeneration g_0 lies in this exact slice. It certifies one nonzero axis-minor polynomial on U_1. The constant coefficient is separately nonzero there by simultaneous nonvanishing of constant and leading linear functionals followed by normalization.

For the discriminant, dividing the exact fixed divisor t−1 from U leaves a gcd-one space. Its universal polynomial is irreducible over the parameter field and separable in characteristic zero. The derivative-at-1 exclusion makes the residual evaluation at 1 nonzero. A generic residual is therefore squarefree and avoids 1; restoring t−1 gives a squarefree full-degree g. Leading normalization transports this nonvanishing discriminant condition to U_1.

The three guards live on the same integral affine coordinate ring. Their product is nonzero, and the infinite-field avoidance argument gives a K-valued point where all three hold. This is an exact descent argument and requires no K-split roots. Extending that point to W_1 proves the asserted nonempty open condition there too. No parameter count alone supplies a guard.

## 8. Actual signed-bank reconstruction and arithmetic range

For d=floor((N+10)/8) and odd N≥23, d≥4 and 8d−10≤N. In the whole proof, m≥(N−1)/2, m≥2d−2, m−2>d−2, positive residual degree, and 2m−2>N−1 all hold. These follow directly by replacing N with its lower bound 8d−10; no asymptotic-only inequality is used.

The legal g is in the actual recurrence kernel, has degree m, and has m distinct nonzero roots in its splitting field. For every positive physical row b≤(N−1)/2≤m, the ++ Vandermonde solve supplies the first m long-left coordinates and the whole-left recurrence supplies the rest. Shorter rows use a truncated consecutive-power solve. The forced −+ singleton handles the exclusive coordinate; the -- moments supply the axis/right interval; the +− singleton amplitude is zero. Reflection supplies the negative rows without adding banks. The full quotient-axis rank supplies b=0, and the moment-to-root transformation is invertible because roots are distinct.

The accepted raw sector-to-weight transform then assigns every bank its original N raw weights. Every alpha is either a nonzero root or 1, so Delta=−alpha^N is nonzero. The finite resolvent identity (I−X)^−1=(I+...+X^(N−1))/Delta is legal in both multiplication orders, and the finite-character transform matches the original Fourier coefficients. Both cross-sign singleton roots may coincide with a same-sign root 1: orientation labels distinguish the banks and no within-group repeated node is introduced. This proves the actual 2m+2 count, rather than a moment-only or relaxed factorization claim.

## 9. Fresh exact controls and limitations

`INDEPENDENT_EXACT_CONTROLS.json` records 36 passing cases: every odd N from 23 to 81, plus 87, 95, 103, 119, 127, and 151, always with d=floor((N+10)/8). They include composite N and multiple threshold-near d values.

For each case the new program independently:

- finds a prime p>N and verifies an exact-order N root q;
- builds the enlarged unscaled envelope directly and computes U and U_0 by exact finite-field elimination;
- verifies the three sparse functionals are independent modulo E, the two residual endpoint functionals are independent, and derivative evaluation at 1 is not forced;
- computes the exact kernel gcds t−1 and t(t−1), and checks all nonzero finite-field evaluation points;
- rebuilds Gaussian coefficients by q-Pascal recursion and verifies actual whole-left rows lie in E and annihilate U;
- finds and records a monic squarefree zero-node witness with reciprocal-coprime residual and full quotient-axis rank;
- finds and records a legal monic squarefree nonzero-constant witness with full axis rank;
- solves quotient-coordinate amplitudes and verifies every positive and reflected negative physical coefficient row, followed by the b=0 axis solve.

These tests are exact modular implementation controls, not a proof by finite extrapolation. Their modular witness coefficients are not asserted to be characteristic-zero lifts. The uniform existence and K descent rest on the audited proof above. No source was altered and no external write was performed.

The frozen author's 12 threshold-near control records were also independently reconstructed from inert JSON data. `AUTHOR_DATA_RECHECK.json` records a complete pass for all supplied envelope and recurrence matrices, field/order checks, ranks, chosen minor determinants, homogeneous and affine bases, parameterized witnesses, fixed/derivative/reciprocal gcds, and axis minors. Each author legal witness additionally passed all physical-row solves in the independent implementation. The author's complete manifest and its four predecessor source bindings match the bytes read for this review.
