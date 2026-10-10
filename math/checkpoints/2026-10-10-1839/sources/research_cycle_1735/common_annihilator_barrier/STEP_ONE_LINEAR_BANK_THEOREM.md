# A uniform 9N/5 + O(1) Fourier signed-bank bound

10 October 2026. Separate new author theorem, pending independent review. The reviewed square-root theorem and the separate step-two linear-saving candidate remain unchanged. This proof uses a step-one chirp variable to combine the parity components before eliminating the ordinary polynomial component.

## 1. Statement and scope

For every odd N≥27, let q be a primitive Nth root, K=Q(q), and put

d=floor((N+13)/10), m=N−d.

Then the negative Fourier matrix F_N is a sum of at most

2N−2floor((N+13)/10)+2 = 9N/5+O(1)

permitted signed banks over a splitting field L/K. The orientation counts are (m,1,1,m). Both same-sign groups use the same m distinct nonzero roots of a monic polynomial g∈K[t], both cross-sign singleton nodes are 1, and every beta is 1. One may take [L:K]≤m!.

This is a Fourier-specific bank-count upper bound with leading coefficient 9/5. It is not an N+O(1) bound, an unrestricted minimum, K-only attainment, an efficient preparation algorithm, or a scalar FFT runtime claim. Every counted object is an individual permitted bank.

## 2. The accepted recurrence setup and combined envelope

Use A=A_(N,m), W=ker_K A and the full physical-row construction in WHOLE_LEFT_RANK_ENVELOPE.md. In particular rank A≤4d−11, so

dim W≥N−5d+12.

Set h=4^(-1) modulo N, e=2^(-1) modulo N, rho=q^e, C_k=q^(h k²), and D(z)=∏_(j=2)^(d−1)(1−q^jz). The element rho is a primitive Nth root and rho²=q. On the actual columns 0≤k≤m, every D(q^k) is nonzero.

Every element of the scaled recurrence row space extends to

B(k)=C_k E(q^k)+C_k rho^k O(q^k)+R(q^k),

deg E≤d−3+floor((d−1)/2),
deg O≤d−3+floor((d−2)/2),
deg R≤d−2.

Introduce t=rho^k and combine the two chirp polynomials:

P(t)=E(t²)+tO(t²).

For both parities of d,

deg P≤3d−7.

Its even and odd coefficients come from E and O, respectively, so P=0 is equivalent to E=O=0. The envelope becomes

B(k)=C_k P(rho^k)+R(q^k).

Let S denote the STEP-ONE forward shift. The identity 2h=e modulo N gives

C_(k+1)=q^h rho^k C_k.

Therefore a factor S−lambda sends the chirp polynomial P to

P(t) ↦ q^h t P(rho t)−lambda P(t).

Every nonzero P gains exactly one degree, with nonzero leading coefficient. The ordinary part remains a polynomial in q^k of degree at most d−2.

## 3. Excluding derivative functionals

Assume d≥4 and N≥10d−13. Fix x≠0 in an algebraic closure of K. If the derivative evaluation vector (k x^(k−1))_(k=0)^m belonged to row(A), its scaled envelope would agree with

k x^(k−1)D(q^k), 0≤k≤m.

Define the two constant-coefficient step-one operators

L_x=∏_(j=0)^(d−2)(S−x q^j)²,
M=∏_(j=0)^(d−2)(S−q^j).

L_x has degree 2(d−1) and annihilates k x^(k−1)D(q^k). M has degree d−1 and annihilates every ordinary component R(q^k). These operators commute. Their product has degree 3d−3.

Consequently M L_x B is a pure chirp C_k P_*(rho^k) with

deg P_*≤(3d−7)+(3d−3)=6d−10,

and it vanishes at the consecutive positions

k=0,…,m−(3d−3),

whose number is N−4d+4. The hypothesis N≥10d−13 gives

N−4d+4≥6d−9>deg P_*.

Also 6d−10<N, so the required initial rho^k values are distinct. Ordinary polynomial interpolation therefore forces P_*=0. Highest-degree preservation through every operator factor forces the original P=0.

Thus R(q^k) alone agrees with k x^(k−1)D(q^k) on k=0,…,m. Their difference has a monic constant-coefficient recurrence of order at most 3(d−1): ordinary roots q^j with multiplicity one and roots xq^j with multiplicity two, 0≤j≤d−2. Since m+1≥3(d−1), equality propagates to all nonnegative k. At k=0 it gives R(1)=0, whereas at k=N it gives R(1)=N x^(N−1)D(1)≠0. This is impossible.

No derivative functional at any nonzero x lies in row(A).

## 4. The three coordinate functionals actually needed

Only delta_0, delta_m and delta_1 are required: they control the constant coefficient, leading coefficient, and derivative at zero. No exclusion of all coordinate functionals is asserted at this stronger range.

Suppose one of these three belongs to row(A). Its scaled envelope B agrees with D(q^j)delta_j on k=0,…,m. Apply M alone. The ordinary component vanishes, and the remaining chirp polynomial has degree at most

(3d−7)+(d−1)=4d−8.

- For j=0, B is zero on k=1,…,m. After M it is zero on k=1,…,m−(d−1), a consecutive interval of length N−2d+1.
- For j=m, use k=0,…,m−1. After M the zero interval is k=0,…,m−d, also of length N−2d+1.
- For j=1, use k=2,…,m. After M the zero interval is k=2,…,m−(d−1), of length N−2d.

Under N≥10d−13,d≥4, each length is at least 4d−7, and 4d−8<N. Distinct rho^k interpolation forces the transformed polynomial to vanish; highest-degree preservation gives P=0. Then R(q^k) agrees with one nonzero delta on m+1 positions, and has m distinct zeros despite degree at most d−2. Hence R=0, contradicting D(q^j)≠0.

The three coordinate functionals are excluded. Along with Section 3, this excludes every finite derivative evaluation functional and proves that neither the leading nor the constant coefficient is forced to vanish on W.

## 5. Every remaining guard is simultaneous

Under d≥4,N≥10d−13,

- m≥(N−1)/2;
- m≥3(d−1), so the combined operator has a nonempty known interval;
- m+1≥3(d−1), as required by the final recurrence argument;
- dim W≥N−5d+12≥(N+1)/2, since N≥10d−23.

Therefore Sections 6–8 of the independently reviewed UNIFORM_SQRT_SAVING_ADDENDUM.md apply using exactly the functional exclusions established here. For completeness, their essential conclusions are:

1. The greatest common divisor of W has no repeated root, because otherwise the corresponding derivative functional would lie in row(A). The constant and leading coefficients are not forced to vanish. After removing the fixed squarefree divisor, a coprime pencil has a generic squarefree degree-m member with nonzero constant. The polynomial space has dimension at least (N+1)/2>1, so no one-dimensional quotient-pencil exception occurs.
2. Because dim W−1≥(N−1)/2, consider the incidence bundle imposing (N−1)/2 distinct nonzero roots with independent evaluation conditions. It contains a squarefree degree-m polynomial: evaluations at all m roots of such a polynomial have kernel exactly its scalar span and therefore rank dim W−1. The bundle is irreducible, so its squarefree open set intersects the nonempty axis-determinant open set. The latter determinant is nonzero at designated roots y_i=q^i, where the selected columns are all N Fourier characters.
3. Full root-coordinate axis rank transfers through invertible Vandermonde maps to a nonzero moment-coordinate minor polynomial in the coefficients of monic g. All defining conditions are over K. An infinite-field open-set argument therefore supplies a coefficient point g∈K[t] satisfying every guard. It does not assert that g splits over K.

No row compatibility, squarefree-node, or axis condition is being replaced by parameter counting.

## 6. Exact construction and actual banks

The bounded exact grid construction from the reviewed proof remains available. Parameterize the monic K-affine kernel and test Nd+2m distinct rational integers per free parameter until the constant, discriminant and axis rank guards hold. A nonzero guard product has degree at most Nd+2m−1, so the finite grid contains a good point.

Take the m roots in a splitting field and perform the whole-left interpolation from WHOLE_LEFT_RANK_ENVELOPE.md, Section 4: each positive row uses the forced −+ singleton, zero +− amplitude, a ++ Vandermonde solve for all left coordinates and a -- solve for the b right/axis moments. The common recurrence supplies every long left interval. Simultaneous reflection gives negative rows, and the axis guard supplies b=0.

Use the original raw weights

w_(n,j)=C Delta_n Σ_(ell=0)^(N−1)h_(n,ell)q^(−epsilon_n delta_n j ell),
C=(1/N)Σ_t q^(−t²), Delta_n=−alpha_n^N.

Every alpha is 1 or a distinct nonzero root of g, so every Delta_n is nonzero. The accepted finite-character transform and literal identity

(I−X_j)^(-1)=(I+X_j+…+X_j^(N−1))/Delta_n

match every Fourier Weyl coefficient and hence the original Fourier matrix. Both inverse products are valid by telescoping. This proves the 2m+2 bank count in the unmodified grammar.

Finally, d=floor((N+13)/10) gives d≥4 for odd N≥27 and N≥10d−13 by definition. All stated hypotheses hold, proving the announced rounding formula.

## 7. Frozen boundaries and source relationship

The prior complex minima and upper bounds, K-only 2N−4 theorem, small splitting-field constructions, and checked N=13,17,35 examples are unchanged. The reviewed constant-eight square-root proof remains a frozen predecessor. The earlier step-two 15N/8 candidate is also preserved separately.

The step-one proof is elementary and algebraic. It does not require a prime-order Fourier theorem, arbitrary-support three-basis full spark, or any claim that mutual unbiasedness alone implies independence. The field extension and finite grid can be very expensive; this is not an FFT speedup. No historical-priority claim is made.
