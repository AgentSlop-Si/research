# A uniform 15N/8 + O(1) Fourier signed-bank bound

10 October 2026. New author theorem, pending independent review. All previously accepted files, including the constant-eight square-root bound, remain frozen. This theorem uses an elementary interval-elimination lemma instead of a coherence estimate.

## Statement

For every odd N≥45, let q be a primitive Nth root, K=Q(q), and put

d=floor((N+19)/16), m=N−d.

Then the negative Fourier matrix F_N is a sum of at most

2N−2floor((N+19)/16)+2 = 15N/8+O(1)

permitted signed banks over a splitting field L/K. The orientation multiplicities are (m,1,1,m). Both same-sign groups use the same m distinct nonzero roots of a monic g∈K[t], both cross-sign singleton nodes are 1, and every beta is 1. One may take [L:K]≤m!.

This improves the leading coefficient of the Fourier-specific bank upper bound from 2 to 15/8. It does not give N+O(1), the unrestricted minimum, K-only attainment, an efficient construction, or a scalar FFT runtime improvement.

## 1. Recurrences and the known sufficient criterion

Use the whole-left matrix A_(N,m) from WHOLE_LEFT_RANK_ENVELOPE.md. Its rows are (v_b(a),…,v_b(a+m)), indexed by positive a,b with a+b≤d−1, where

T_b=1/G_-+(N−b,b),
v_b(j)=(q^(h(j+b)^2)−T_b G_-+(j,b))/G_++(j,b),
h=4^(-1) modulo N.

The already established rank bound is rank A≤4d−11. Its kernel W has dimension at least N−5d+12. A monic degree-m kernel polynomial with nonzero constant, nonzero discriminant, and full axis rank gives exactly the claimed bank architecture. The complete physical-row interpolation and original resolvent proof are in Section 4 of that note.

Here the parameter choice gives d≥4 and N≥16d−19. It also gives m≥(N−1)/2 and dim W≥(N+1)/2.

## 2. The explicit interval-elimination mechanism

After scaling column k by D(q^k), D(z)=∏_(j=2)^(d−1)(1−q^jz), every row-space element extends to

B(k)=C_k E(q^k)+C_k q^(ek)O(q^k)+R(q^k),
C_k=q^(h k²), e=(N+1)/2,

deg E≤u=d−3+floor((d−1)/2),
deg O≤v=d−3+floor((d−2)/2),
deg R≤d−2.

All D(q^k), 0≤k≤m, are nonzero. The elementary identity C_(k+2)=q^(k+1)C_k is the only quadratic-phase input needed in the new step.

Let S be the step-two shift and let M=∏_(j=0)^(d−2)(S−q^(2j)). This kills the ordinary R component. Each factor S−lambda maps the chirp polynomials to qzE(q²z)−lambda E(z) and q²zO(q²z)−lambda O(z). It increases the degree of every nonzero such polynomial by exactly one. After killing R, a sufficiently long zero interval therefore forces both chirp components to vanish by an ordinary consecutive-row Vandermonde matrix. This works at composite and prime odd orders.

The complete elementary lemma, including every interval length and nonwrapping condition, is proved in research_cycle_1735/three_basis_feasibility/STRUCTURED_INTERVAL_ELIMINATION.md.

## 3. Uniform legal-polynomial guards

For a derivative evaluation functional at x≠0, the scaled B would equal kx^(k−1)D(q^k) on k=0,…,m. Apply

L_x=∏_(j=0)^(d−2)(S−x²q^(2j))²,

then M. The total shift-operator degree is 3(d−1). The pure-chirp result has at most 9d−12 distinct ordinary Fourier frequencies, and vanishes on N−7d+7 consecutive positions. N≥16d−19 is exactly the sufficient Vandermonde inequality. The frequency intervals remain disjoint and do not wrap. Highest-degree preservation forces original E=O=0. The remaining agreement R(q^k)=kx^(k−1)D(q^k) propagates by a recurrence of order at most 3(d−1); k=0 and k=N contradict each other. Thus no derivative functional lies in row(A).

For a coordinate functional delta_j, the scaled B has a zero interval of length at least ceil(m/2). Applying M leaves a pure chirp with at most 5d−8 frequencies. The sufficient inequality is ceil(m/2)≥7d−10, which follows from the same N bound. This excludes every coordinate functional, in particular those forcing the leading or constant coefficient to vanish and the derivative functional at zero.

The accepted squarefree-pencil argument now applies: the common divisor of W has no repeated root, leading and constant coefficients are not forced to zero, and a generic degree-m pencil member is squarefree with nonzero constant.

The accepted root-incidence argument also applies because dim W≥(N+1)/2. It simultaneously imposes (N−1)/2 distinct nonzero roots whose ++, -- and singleton columns give an invertible axis matrix. The axis determinant is a nonzero polynomial in those designated roots, witnessed by y_i=q^i. Irreducibility of the evaluation-kernel incidence bundle ensures this axis condition intersects the squarefree open condition; it is not an unsupported parameter count.

Full axis rank transfers to a nonzero polynomial moment minor in the coefficients of g. All conditions are defined over K, so a nonempty open subset of the monic K-affine kernel has a K-valued point. This places the defining g in K[t]; it does not place its individual roots in K.

## 4. Exact construction and original-bank equality

An explicit bounded construction is available: parameterize the monic affine kernel over K and test a Cartesian grid of Nd+2m distinct rational integers in each free coordinate until the constant, discriminant and axis rank guards hold. The nonzero guard polynomial has degree at most Nd+2m−1. Hence some tested point works. This is finite but potentially exponentially costly.

Take the m roots in a splitting field. For every positive physical row b, assign the −+ singleton its forced T_b, set the +− singleton amplitude to zero, interpolate the whole left interval with ++ amplitudes at these m nodes, and fit the b right/axis moments with -- amplitudes. The recurrence guarantees every long left interval; m≥b guarantees the other solve. Reflect simultaneously to assign negative physical rows, and use the full-rank axis solve for b=0.

The original raw weights are

w_(n,j)=C Delta_n Σ_(ell=0)^(N−1) h_(n,ell)q^(−epsilon_n delta_n j ell),
C=(1/N)Σ_t q^(−t²), Delta_n=−alpha_n^N.

Every alpha is 1 or a distinct nonzero root of g, so Delta_n≠0. The finite character transform and the literal resolvent identity

(I−X_j)^(-1)=(I+X_j+…+X_j^(N−1))/Delta_n,
X_j=alpha_n S^epsilon_n+q^(epsilon_n delta_n j)T^delta_n,

match all Fourier Weyl coefficients and therefore the original matrix. Both inverse products follow by telescoping. Every root occurrence is counted as an individual bank; no trace or Galois orbit is treated as a bank.

## 5. Interpretation and preserved results

There are 2m+2 whole banks and N(2m+2) raw phase weights. The coefficient-field preparation and root splitting costs are not an arithmetic-complexity theorem. The legal grammar is unchanged.

The accepted complex minima at N=3,5,7, the N=11 upper bound and restricted optimum, the K-only 2N−4 theorem, and all smaller-field specializations remain unchanged. The separately checked N=13,17,35 constructions remain useful at their individual orders. The reviewed square-root theorem is retained as a frozen predecessor rather than edited in place.

The new all-order guard step is an elementary combination of constant-coefficient annihilation and consecutive Vandermonde interpolation. It does not rely on arbitrary-support full spark of a union of mutually unbiased bases. No historical-priority claim is made.
