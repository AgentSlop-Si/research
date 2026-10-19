# Independent review: explicit all-phase C8 rank-zero gap

19 October 2026 UTC.

## Verdict

**PASS. No correction to the claimed theorem or its proof is required.**

For normalized F8, arbitrary invertible complex monomial outer factors, an unrestricted real core, zero correction rank, and the external complex operator norm, the candidate proves

\[
\sin(3\pi/16+10^{-6}) < \delta_{8,0}
\le \frac12\sqrt{1+\sqrt{\sqrt2-1}}.
\]

The lower endpoint is approximately 0.5555710644889367420, an improvement of approximately 8.31469334517290149e-7 over the previously certified lower endpoint. The inherited upper endpoint remains approximately 0.6410136997181851621. Neither equality at the upper endpoint nor the exact global optimum is established.

Frozen candidate proof: `/workspace/shared/phase_rankzero_quantitative_20261019_1347/PROOF.md`, SHA-256 `755ea834b423038c67d4c813324d196045fe3594609780cd806d8afa0adfa4a0`.

The fresh independent checker passed **1,190 exact assertions** in approximately 0.460 seconds of measured computation. These checks supplement the all-phase analytical audit below; they are not presented as a finite sampling certificate. Candidate and historical checkers were neither imported nor executed. All frozen source files remained byte-identical.

## 1. Original model, normalization, and the minimum

The phase reduction is exact for the stipulated unrestricted model. Write arbitrary invertible complex monomials as L = D_L M_L and R = M_R D_R, with diagonal-unitary D factors and invertible real monomial M factors. The middle matrix M_L C M_R ranges over all real matrices. Hence the represented approximants are exactly diagonal-unitary gauges of arbitrary real matrices; no nonunitary factor is applied to the residual norm.

For any complex matrix Z, entrywise imaginary part is contractive in complex operator norm because Im Z = (Z - conjugate Z)/(2i), and conjugation preserves that norm. Thus, for V = P F Q,

\[
\min_{C\text{ real}}\|V-C\|_2=\|\operatorname{Im}V\|_2,
\]

with equality at C = Re V. Only unitary P and Q are removed from the external residual. This validates the phase minimization without a hidden magnitude, conditioning, permutation, or internal-norm restriction.

For unitary V = X+iY, W = V^T V is symmetric and unitary and

\[
Y^T Y=(I-(W+W^*)/2)/2.
\]

Symmetry makes the Hermitian part of W equal its entrywise real part. W is unitarily similar to U = F A F B through Q, where A = P² and B = Q². Therefore ||Y|| ≤ sin(theta/2) implies all principal eigenphases of U lie in [-theta,theta], and Re_H U ≥ cos(theta) I. The argument never applies entrywise real part to the nonsymmetric U.

The checker independently constructs the normalized full eight-point Fourier matrix and checks Fourier unitarity, this similarity, the Gram identity, and the actual external residual identity at an explicit nonperiodic phase control. A destructive normalization control rejects the unnormalized Fourier matrix. The universal derivation above, rather than that example, establishes the model reduction for all phases.

The phase torus is compact and the objective is continuous. This matters for the strict endpoint: rejecting every phase choice with residual at most the candidate threshold rejects the minimizing phase choice, so the minimum itself is strictly greater than that threshold. Mere pointwise strictness without compactness would not suffice to make this conclusion about an infimum.

## 2. Commutator localization and quantitative endpoint rigidity

Set theta0 = 3pi/8, epsilon = 1/500000, theta = theta0+epsilon, and c = cos(theta). The elementary bound pi > 3 gives theta < pi/2.

With S e_j = e_(j+1), T = B* S B, C = F A F, and U = C B, the cyclic-Hankel identity C S = S* C and unitarity give

\[
K=UTU^*T^*=S^*B^*S^*B,
\qquad K e_j=(b_j/b_{j-1})e_{j-2}.
\]

No periodicity is used. The identity K-I = (UT-TU)U*T* preserves the norm exactly. The spectral theorem gives

\[
\|U-cI\|\le\sin\theta,
\qquad \|K-I\|\le2\sin\theta.
\]

For a unit-modulus eigenvalue exp(i kappa) of K, |exp(i kappa)-1| = 2|sin(kappa/2)|. Because kappa is principal and theta < pi/2, this is equivalent to |kappa| ≤ 2theta. There is no branch ambiguity.

The even and odd weighted cycles have products Gamma and Gamma^-1, so each cycle's eigenvalues form a square. The forbidden open gap is centered at -1 and has width pi/2-4epsilon. Choosing the square's rotation relative to the square with angles ±pi/4 and ±3pi/4, avoidance of that gap forces a unique offset d in [-2epsilon,2epsilon]. The inverse cycle product gives opposite offset -d: the relation exp(4i(d+d'))=1 and |4(d+d')|≤16epsilon<2pi excludes every nonzero multiple of 2pi. This remains valid when a vertex is on a closed permitted-arc endpoint.

Thus the positive endpoint eigenvalues are lambda_e = exp(i(3pi/4+d)) and lambda_o = exp(i(3pi/4-d)); their exact product is -i. The corresponding negative endpoints are i lambda_e and i lambda_o.

For a normalized K eigenvector v with eigenvalue exp(2is), define a = v*Uv and D = T U* T*. The exact equation Dv = exp(2is)U*v yields v*Dv = exp(2is) conjugate(a). Both U and D have Hermitian part at least cI. Adding their expectation inequalities gives

\[
2\cos s\,\operatorname{Re}(e^{-is}a)\ge2c.
\]

Here cos s is positive. Since U is unitary,

\[
\|(U-e^{is}I)v\|^2
=2-2\operatorname{Re}(e^{-is}a)
\le2(1-c/\cos s).
\]

At all four extreme cycle eigenvalues, |s| is between theta0-epsilon and theta0+epsilon. The mean-value bound

\[
\cos|s|-\cos\theta
\le(\theta-|s|)\sin\theta\le2\epsilon\sin\theta
\]

and cos|s|≥cos(theta)>0 imply

\[
2(1-c/\cos s)\le4\epsilon\tan\theta<10\epsilon.
\]

Moving exp(is) to the appropriate fixed endpoint u = exp(i theta0) or conjugate(u) costs at most epsilon. Hence the candidate's uniform residual bound rho = sqrt(10epsilon)+epsilon is valid. The strict comparison tan(theta)<5/2 is certified below.

## 3. Exact recurrences and Fourier error normalization

Writing the normalized endpoint eigenvectors as x_t/2 on even positions and y_t/2 on odd positions is correct: each cycle has four equal-modulus coordinates. Setting x0 = y0 = 1 fixes harmless phases. With d_t = b_(2t) and e_t = b_(2t+1), the recurrences give exactly

\[
e_t x_t y_t=e_0(-i)^t,
\qquad
d_t x_t y_{t-1}=e_0\lambda_o^{-1}(-i)^t.
\]

The second coefficient is lambda_o^-1. Replacing it by lambda_e^-1 is invalid when the two cycle offsets differ. This issue is handled correctly in the candidate and explicitly rejected by an independent destructive control.

Let omega = i and use the unitary four-point Fourier normalization 1/2. For the even vector, each entry of F8 B xi equals D_k/sqrt(8), and each entry of F8* xi equals X_(-k)/sqrt(8). For the odd vector the corresponding factors are zeta^(-j) E_k/sqrt(8) and zeta^j Y_(-k)/sqrt(8), where zeta = exp(i pi/4). After cancelling the unit-modulus zeta^(-j), their ratio is zeta^(2j) = omega^k.

Consequently a vector residual at most rho produces the displayed coordinate residual bound eta = sqrt(8)rho = 2sqrt(2)rho in both equations. The normalization is not missing a factor of two or a square root.

The exact recurrence/Fourier identities are

\[
D_k=e_0\lambda_o^{-1}\omega^{-k-1}\overline{Y_{-k-1}},
\qquad E_k=e_0\overline{X_{-k-1}}.
\]

Taking absolute values gives both inequalities (3.4). Multiplying the first approximate equation by E_k and the second by D_k cancels their common a_j without division. The error is bounded by eta(|E_k|+|D_k|). Since lambda_o^-1 omega^-1 = lambda_e, this is precisely the candidate's (3.5), including its coefficient and right-hand side. Zeros cause no difficulty. The two-step modulus comparison and both Parseval equalities follow immediately.

The fresh checker verifies the recurrences, both Fourier formulas, all eight-coordinate normalization factors, and the no-division error cancellation symbolically, allowing unequal cycle offsets.

## 4. Complementary small Fourier coefficients

Let m = min|X_n| and M = max|X_n|. Parseval gives M≥1. If m>5eta, both X and Y have no zero coefficients. Every adjacent pair of X coefficients includes one from the maximum's parity, whose modulus is at least M-2eta. Applying the shifted modulus bounds to Y proves

\[
|z_n|\ge m(M-2\eta),\quad
|w_n|\ge(m-\eta)(M-3\eta),\quad
|z_n-\lambda_e w_n|\le\eta(2M+\eta).
\]

The normalized phase inequality is valid with the stated square-root denominator: subtracting |z||w| times its squared left-hand side from |z-w|² gives exactly (|z|-|w|)²≥0.

As eta<1/50, M≥1, and m>5eta,

\[
\frac{\sqrt{|z_n||w_n|}}{mM}
>\sqrt{(24/25)(4/5)(47/50)}>21/25,
\]

while 2M+eta < (101/50)M. The four-factor product-difference estimate and telescoping phase products then give

\[
|1-\lambda_e^4|
<4\frac{101/50}{21/25}\frac15
=202/105<199/100.
\]

Conversely lambda_e^4 = -exp(4id), so

\[
|1-\lambda_e^4|=2|\cos(2d)|
\ge2\cos(4\epsilon)>199/100.
\]

Here |2d|≤4epsilon<pi/2 ensures the cosine comparison and positive branch. The elementary bound cos t≥1-t²/2 proves the last strict margin rationally. This contradiction forces m≤5eta. The same-parity comparison then makes both X coefficients in that parity at most 7eta, and both complementary-parity Y coefficients at most 8eta.

The normalized inverse Fourier transform gives exactly the stated half-shift estimates, with 14eta and 16eta. Their product error is at most 30eta, using the unit modulus of all coordinates. Combined with (-i)²=-1 in both recurrence identities, this proves |b_(j+4)-b_j|≤30eta. All four even and odd indices, including wraparound indices, obey the same formulas.

This is only approximate periodicity of B. Neither exact periodicity of B nor approximate/exact periodicity of A is subsequently assumed.

## 5. The actual non-invariant compressions

Replacing the two second-half even coordinates of xi by their prescribed half-shift copies gives a unit vector v in the appropriate even half-shift subspace. Its two coordinates in the standard sector basis have equal modulus. The distance bound is

\[
\|v-\xi\|^2\le2(14\eta/2)^2=98\eta^2,
\]

so ||v-xi||≤7sqrt(2)eta. Since ||U-uI||≤2, its residual is at most r = rho+14sqrt(2)eta. The modulated endpoint vector i^t x_t/2 has K eigenvalue i lambda_e and the opposite half-shift sign; the same construction yields a flat vector in the other even sector with residual at most r at conjugate(u).

The following step is valid without invariant subspaces. For a unitary U, a unit vector v, and unit-modulus z,

\[
\|(U^*-\bar zI)v\|=\|(U-zI)v\|.
\]

If w is the flat orthogonal complement to v inside a chosen two-dimensional subspace, both |w*Uv| and |v*Uw| are therefore at most r. With the flat basis phases included, the exact identity is

\[
M_{11}-M_{22}=v^*Mw+w^*Mv,
\]

where M is the compression in its standard orthonormal coordinates. Thus its diagonal difference is at most 2r even when the compression is nonnormal or nonunitary. No eigenvalue or norm property of a surrogate compression is invoked.

For an arbitrary cyclic-Hankel C and arbitrary B, direct compression of the actual U = C B gives

- even,+ diagonals: (c0+c4) beta0 and (c0+c4) beta2;
- even,- diagonals: (c0-c4) beta0 and -(c0-c4) beta2;

where beta0=(b0+b4)/2 and beta2=(b2+b6)/2. The minus-sector sign is essential and is correct. The fresh checker verifies these identities with fully independent symbolic c_j and b_j. It also constructs an exact nonperiodic unitary control in which the even,+ subspace is not invariant and its compression is not unitary, demonstrating why no such assumption can be silently supplied.

Accretivity of the actual U makes the real part of every compressed diagonal at least c. Since |beta_j|≤1, both |c0+c4| and |c0-c4| are at least c. Division by these nonzero scalars is therefore justified and yields

\[
|\beta_0-\beta_2|\le2r/c,
\qquad |\beta_0+\beta_2|\le2r/c.
\]

For two unit phases, |(b+b')/2|² = 1-|b-b'|²/4. Hence each |beta_j|²≥1-225eta². Applying the parallelogram identity to the preceding two estimates gives exactly

\[
r\ge\frac{c\sqrt{1-225\eta^2}}{\sqrt2}.
\]

The expression under the square root is positive by the independent rational margins below.

## 6. All numerical margins and strictness

Every numerical bound used in the candidate has a valid exact certificate. A convenient chain is:

1. sqrt(2)<283/200. This gives cos(3pi/8)>191/500 and sin(3pi/8)<231/250 by positive squaring.
2. The global derivative bounds for sine and cosine give c>191/500-epsilon and sin(theta)<231/250+epsilon. Their positive ratio is strictly less than 5/2, proving the tan bound.
3. Positive squaring proves rho<9/2000 and eta<8/625<1/50.
4. The rational product (24/25)(4/5)(47/50) exceeds (21/25)². Also 202/105<199/100 and 2-(4epsilon)²>199/100.
5. The candidate's separated bound on r using sqrt(2)<17/12 is valid. Independently, eta=2sqrt(2)rho gives the exact simplification r=57rho, so r<513/2000=0.2565<13/50. No correction or improved claim is needed to use this simpler verification.
6. c>19/50 and 1-225(8/625)²>(49/50)². Thus sqrt(1-225eta²)>49/50.
7. The exact rational inequality ((19/50)(49/50))²>2(13/50)² proves that the forced lower bound on r exceeds 13/50.

This contradicts the upper bound on r. Informational direct evaluations are r≈0.2550257494349760254 and the forced threshold≈0.2656769200271322801, but no numerical evaluation is a premise of the proof.

The hypothetical residual assumption was non-strict (at most sin(theta/2)); the numerical contradiction is strict. Thus the exact threshold itself is excluded, not merely smaller values. Compactness, as addressed in Section 1, establishes the advertised strict lower bound for delta.

## 7. Relation to the accepted upper bound and scope of progress

The independent accepted upper review at `/workspace/shared/phase_rankzero_exact_review_20261019_1227/REVIEW.md` certifies the legal witness norm sqrt(1+sqrt(sqrt(2)-1))/2. Its verdict and its binding to the original upper-witness proof were checked, and the entire review directory was frozen in the source receipts. That theorem is inherited here; the witness proof and its checker were not rerun or counted as new work.

The prior strict lower proof already established nonattainment at sin(3pi/16), with compactness supplying an unspecified positive gap. The present candidate quantifies that gap, adapting the earlier commutator/Fourier obstruction and replacing exact endpoint rigidity by quantitative estimates. The actual-compression argument is what permits that adaptation without a global periodicity reduction. This review certifies the mathematical advance relative to those local accepted packets, not literature novelty.

The exact optimum, minimizer classification, and whether unrestricted nonperiodic phases can improve the upper witness remain open. This review asserts nothing about other dimensions or correction ranks.

## 8. Reproduction and integrity

Run `python independent_exact_controls.py` inside this review directory. SymPy is required. The fresh program writes its own results, assertion list, and source receipts only in this new review directory. It does not execute candidate or historical code, perform optimization, use numerical tolerances for assertions, or contact external services.

Source snapshots before and after the checks are identical and include every candidate file, every accepted-upper-review file, the original upper-witness proof, and the inherited lower proof. The candidate's own manifest was verified. Four destructive controls cover normalization, exchanged cycle coefficients, false compression unitarity, and the minus-sector sign.

No external state was modified and no worker was spawned. All planned review work completed; no timeout, partial control, or pending calculation is represented as a pass.
