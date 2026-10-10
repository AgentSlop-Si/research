# Independent review of the step-two and step-one linear bank savings

Review date: 10 October 2026. Verdict: **PASS for both separately frozen theorems.** The step-one theorem is the stronger result. This review reconstructs the new elimination arguments and checks all transferred guards; it does not merely infer correctness from numerical controls. No prior accepted proof or author source was modified.

## 1. Accepted statements and exact scope

Let N be odd, q a primitive Nth root, and K=Q(q). The accepted whole-left signed-bank architecture has orientation multiplicities (m,1,1,m), beta=1 throughout, both cross-sign singleton nodes equal to 1, and the same m distinct nonzero nodes in both same-sign groups.

Two results pass independently:

1. **Step two:** for every odd N≥45, d=floor((N+19)/16), m=N−d gives at most 2N−2floor((N+19)/16)+2 banks. Its leading coefficient is 15/8.
2. **Step one:** for every odd N≥27, d=floor((N+13)/10), m=N−d gives at most **2N−2floor((N+13)/10)+2** banks. Its leading coefficient is **9/5**.

In both cases the defining monic polynomial lies in K[t]; its individual roots, amplitudes, and raw weights may lie in a splitting field L/K, with [L:K]≤m!. These are upper bounds on actual individual banks in the original grammar. They are not K-only attainment, unrestricted minima, N+O(1) bounds, efficient preparation algorithms, scalar FFT runtime improvements, or historical-priority claims. The existing smaller-order results remain unchanged and can be stronger at individual orders.

## 2. Accepted prerequisites restated with their hypotheses

Set h=4^(-1), e=2^(-1) modulo N, rho=q^e, and C_k=q^(h k²). For d=N−m≥4 and m≥(N−1)/2, the accepted whole-left matrix A has rows indexed by positive a,b with a+b≤d−1:

A_(a,b),k=v_b(a+k), 0≤k≤m,

v_b(j)=[q^(h(j+b)²)−T_b G_-+(j,b)]/G_++(j,b),
T_b=1/G_-+(N−b,b).

All denominators are nonzero on these ranges. The common recurrence kernel W=ker A has dimension w≥N−5d+12 because rank A≤4d−11. This rank bound does not itself secure any legal-polynomial guard.

Put D(z)=product_(j=2)^(d−1)(1−q^j z). For 0≤k≤m, 2≤j+k≤N−1, so D(q^k)≠0. Every element of the column-scaled row space extends to

B(k)=C_k E(q^k)+C_k rho^k O(q^k)+R(q^k),

deg E≤u=d−3+floor((d−1)/2),
deg O≤v=d−3+floor((d−2)/2),
deg R≤d−2.

The additional divisibility and endpoint relation from the sharper rank proof may safely be discarded for the exclusions below. We do not assume that the extended representation is unique; the arguments force every possible representing triple in a purported counterexample to vanish.

All functional exclusions are taken after extension to C. Elementary finite-dimensional duality says that a functional vanishes on W_C if and only if its vector belongs to row(A_C). Column scaling therefore takes derivative evaluation at x≠0 to k x^(k−1)D(q^k), and a coefficient functional delta_j to D(q^j)delta_j.

## 3. Independent step-two proof

Write S_2 B(k)=B(k+2), and b_0=d−1. The exact identity

C_(k+2)=q^(k+1) C_k

and rho²=q show that a factor S_2−lambda transforms the three polynomials by

E(z) ↦ q z E(q²z)−lambda E(z),
O(z) ↦ q² z O(q²z)−lambda O(z),
R(z) ↦ R(q²z)−lambda R(z).

If E has degree s and leading coefficient a≠0, its new leading coefficient is a q^(2s+1) at degree s+1. For O the coefficient is a q^(2s+2). These are nonzero regardless of lambda. Thus each chirp transformation is injective and raises every nonzero degree exactly one. The ordinary degree does not increase.

### 3.1 Derivative exclusion

Assume d≥4 and N≥16d−19. For x≠0 define

L_x=product_(j=0)^(d−2)(S_2−x²q^(2j))²,
M=product_(j=0)^(d−2)(S_2−q^(2j)).

The first operator has degree 2b_0 in S_2 and kills k x^(k−1)D(q^k): expand D, and each term is a scalar times k(xq^j)^k, whose repeated step-two eigenvalue is x²q^(2j). The second operator has degree b_0 and kills every ordinary R(q^k). Both operators are polynomials in the same shift and commute.

If derivative evaluation lay in row(A), applying M L_x to its scaled envelope would give a pure chirp, with component degrees ≤u+3b_0 and ≤v+3b_0, vanishing on exactly the known interval

0≤k≤m−6b_0.

All shifts used lie in the original interval 0,…,m; there is no periodic shortcut across an unmatched sample. The interval length is N−7d+7.

After division by the nonzero C_k, the result is a sum of at most

(u+3b_0+1)+(v+3b_0+1)=9d−12

ordinary characters. Here u+v+2=3d−6. Their frequencies lie in [0,u+3b_0] and [e,e+v+3b_0], using the representative e=(N+1)/2. They are disjoint modulo N and do not wrap. Indeed

u+3b_0≤(9d−13)/2<e,
v+3b_0≤(9d−14)/2<(N−1)/2,

where strictness follows from N≥16d−19 and d≥4. Consecutive evaluation of s distinct characters has a nonzero Vandermonde determinant, including for composite N. The inequality

N−7d+7≥9d−12

is precisely N≥16d−19. Consequently all transformed character coefficients vanish; the injective polynomial transformations force original E=O=0.

The remaining ordinary-recurrence contradiction is proved in Section 5 below and excludes the derivative functional.

### 3.2 Coordinate exclusion and explicit requested endpoint checks

For any delta_j, its scaled envelope is zero on one of [0,j−1] or [j+1,m] for at least ceil(m/2) consecutive samples. Applying M reduces that interval length by 2b_0 and leaves at most

(u+b_0+1)+(v+b_0+1)=5d−8

distinct chirp-demodulated frequencies. Thus a sufficient original length is 7d−10. From m≥15d−19,

ceil(m/2)≥7d−10,

since (15d−19)/2−(7d−10)=(d+1)/2>0. The nonwrap inequalities already checked are stronger than needed here. Consecutive Vandermonde interpolation again forces E=O=0. The original R then has m distinct zeros among 0,…,m, with m>d−2 and m<N, and therefore vanishes. This contradicts its nonzero value D(q^j).

For clarity, the three special coordinates alone also suffice. Apply M to their zero intervals:

- delta_0: original [1,m], surviving [1,m−2b_0], length N−3d+2.
- delta_m: original [0,m−1], surviving [0,m−1−2b_0], length N−3d+2.
- delta_1: original [2,m], surviving [2,m−2b_0], length N−3d+1.

Each length is ≥5d−8 under the stated range. Thus the root's proposed three-coordinate shortcut has the correct indices as well. The stronger all-coordinate claim belongs to this step-two range only.

## 4. Independent step-one proof

The key improvement is to combine the parity pieces before shifting. Set t=rho^k and

P(t)=E(t²)+tO(t²).

Since rho is primitive and rho²=q, B(k)=C_k P(rho^k)+R(q^k). Even and odd powers are disjoint, so P=0 is equivalent to E=O=0. Directly checking both parities of d gives

max(2u,2v+1)=3d−7.

For S B(k)=B(k+1), the identity 2h=e modulo N gives

C_(k+1)=q^h rho^k C_k.

Therefore S−lambda acts on the chirp polynomial as

P(t) ↦ q^h t P(rho t)−lambda P(t).

If P has degree s with leading coefficient a≠0, its transformed leading coefficient is a q^h rho^s at degree s+1. It cannot cancel against the second summand of degree s. This proves exact degree growth and injectivity for every scalar lambda. The ordinary component transforms by R(z)↦R(qz)−lambda R(z) and never gains degree.

### 4.1 Derivative exclusion

Assume d≥4 and N≥10d−13. For x≠0 define the step-one operators

L_x=product_(j=0)^(d−2)(S−xq^j)²,
M=product_(j=0)^(d−2)(S−q^j).

The degree-2b_0 operator L_x kills k x^(k−1)D(q^k); the degree-b_0 operator M kills the ordinary component. If derivative evaluation belonged to the recurrence row space, M L_x B would be C_k P_*(rho^k), with degree bound

deg P_*≤3d−7+3b_0=6d−10.

It is known to vanish precisely on the safe interval

0≤k≤m−3b_0,

which has N−4d+4 samples. The total operator uses only original positions 0,…,m. The numerical hypothesis is exactly

N−4d+4≥6d−9.

Moreover 6d−10<N, and this whole zero block has length <N (d≥4). Thus its rho-powers are distinct. A polynomial of degree ≤6d−10 vanishing at ≥6d−9 distinct points is zero. This forces P_*=0 and, by injectivity of all transformations, P=0. There is no frequency-aliasing assumption left implicit and no prime-order restriction. Section 5 supplies the final contradiction.

### 4.2 Precisely the three necessary coefficient functionals

The step-one result does not require or assert exclusion of every delta_j. It excludes delta_0, delta_m and delta_1. Applying M alone produces a chirp polynomial of degree ≤4d−8 and the following intervals:

- delta_0: [1,m−b_0], length N−2d+1.
- delta_m: [0,m−1−b_0]=[0,m−d], length N−2d+1.
- delta_1: [2,m−b_0], length N−2d.

Every operator input lies in the corresponding original zero interval. The shortest surviving length is ≥4d−7 because N≥10d−13 implies N≥6d−7 for d≥4. Every displayed block has length <N, and 4d−8<N. Interpolation at distinct rho-powers forces the transformed polynomial to vanish, then injectivity forces P=0. The ordinary R has m distinct q-power zeros and degree ≤d−2; m>d−2. Hence R=0, contradicting D(q^j)≠0.

The derivative functional at x=0 is delta_1, with its usual polynomial-derivative interpretation; no expression 0·0^(-1) is used. These three exclusions establish the leading, constant, and zero-derivative guards needed later. The stronger all-coordinate half-interval estimate does not follow throughout this new range (for example d=5,N=37 is already insufficient for that particular estimate); neither reviewed step-one source claims it.

## 5. The final ordinary contradiction, with no discarded endpoint

After either derivative-elimination argument, original E=O=0 and

R(q^k)=k x^(k−1)D(q^k), 0≤k≤m.

Let T be the step-one shift. Their difference is killed by the monic operator

product_(j=0)^(d−2)(T−q^j)(T−xq^j)²,

of degree 3b_0. This remains an annihilator when roots coincide; a smaller minimal recurrence is unnecessary. Since m+1≥3b_0, the first 3b_0 consecutive zeros and the monic recurrence propagate forward to all nonnegative k. At k=0, R(1)=0. At k=N, periodicity of q^k gives

R(1)=N x^(N−1)D(1).

The right side is nonzero: characteristic is zero, x≠0, and D(1) has only factors 1−q^j with 2≤j≤d−1<N. This contradiction is exact. It does not presume x^N=1 or periodicity of the derivative target.

## 6. Numerical hypotheses and the boundary orders

For the stronger range d≥4,N≥10d−13:

- N≥2d−1, so m≥(N−1)/2 and every original whole-left definition is valid.
- N≥4d−3, so m≥3(d−1) and the combined step-one zero block is nonempty.
- m+1≥3(d−1), enough for the final recurrence.
- N≥10d−23, so w≥N−5d+12≥(N+1)/2.
- The coordinate and degree-distinctness inequalities were checked explicitly above.

Each follows immediately by subtracting the required right-hand side from 10d−13 and using d≥4. The step-two range N≥16d−19 implies all of these and also its stronger step-two shift/frequency conditions.

For d=floor((N+13)/10), every odd N≥27 gives d≥4 and N≥10d−13. At N=27, d=4,m=23: the derivative zero block has 15 samples against polynomial degree 14; the shortest coordinate block has 19 samples against degree 8; w≥19≥14; and the bank bound is 48.

For d=floor((N+19)/16), every odd N≥45 gives d≥4 and N≥16d−19. At N=45,d=4,m=41: the derivative zero block has 24 samples against 24 distinct frequencies; the two expanded frequency ranges are [0,11] and [23,34]; and the bank bound is 84.

## 7. Independent check of the squarefree, nonzero, monic guard

Because delta_m and delta_0 do not vanish on W_C, neither leading nor constant coefficient is identically zero there. Their two complements intersect, so choose a degree-m member with nonzero constant. Let H be the common monic divisor of W_C. If H had a repeated root x, derivative evaluation at x would vanish on all W_C, contrary to Sections 3–5. Thus H is squarefree. Also H(0)≠0 by the constant-functional exclusion.

The residual space V=W_C/H has no common root and dimension w>1. Choose f∈W_C of degree m with f(0)≠0. Its quotient A=f/H has positive degree, because otherwise all of W_C would be scalar multiples of H. Since V has no common root, there is B∈V that avoids every root of A: each prohibition is one proper linear hyperplane and C is infinite. Then A and B are coprime and their ratio is nonconstant.

Only finitely many parameters lambda yield a multiple root of A+lambda B. Such roots arise from the finite roots of the nonzero Wronskian A'B−AB', with the exceptional denominator cases handled by coprimality. Only finitely many further parameters cause A+lambda B to meet a root of H or kill its leading or constant coefficient. Avoiding these parameters gives a degree-m, squarefree member H(A+lambda B) of W_C with nonzero constant.

Consequently these good-polynomial conditions form a nonempty Zariski-open subset of P(W_C). This is an actual finite-exception argument, not dimension counting or an assumption that generic homogeneous solutions are monic.

## 8. Independent check of the simultaneous axis guard

Put r_0=(N−1)/2. The inequality w−1≥r_0 is essential and was checked above. Let U be the set of ordered r_0-tuples Y of distinct nonzero complex numbers whose evaluation functionals on W_C are independent. It is open in the irreducible tuple space.

To prove U and its good incidence locus are nonempty, take a degree-m squarefree good g∈W_C. Evaluation at all m roots has kernel exactly the line Cg: any polynomial of degree at most m vanishing at all these distinct roots is a multiple of g. The evaluation rank is therefore w−1, and r_0 independent evaluations can be selected from those roots.

Over U, the incidence variety of pairs (Y,[g]) with g vanishing at all designated nodes is the projectivization of an evaluation-kernel vector bundle of rank w−r_0≥1. It is irreducible, and its good-polynomial open subset is nonempty by the preceding construction.

The root-axis determinant formed from the r_0 ++ columns, the singleton column, and the r_0 -- columns has rows

(y_1^a,…,y_(r_0)^a,1,y_1^[-a]_N,…,y_(r_0)^[-a]_N), 0≤a<N.

It is a nonzero polynomial in Y. At y_i=q^i, its columns are the N distinct Fourier characters, so its determinant is nonzero. That particular tuple need not lie in U; this is not assumed. Its nonzero locus and U are nonempty opens of the same irreducible tuple space, so they intersect. The corresponding axis-open subset in the incidence bundle is therefore nonempty.

The two nonempty opens in the irreducible incidence variety intersect. At such a point g is squarefree, degree m, and nonzero at zero, while a subset of its roots already gives full axis rank. Thus the axis condition is simultaneous with the good-polynomial conditions, rather than merely independently satisfiable.

## 9. Descent to K and a finite exact recipe

Normalize the resulting complex g to be monic. For a monic g, write p_a for the coefficient vector of t^a modulo g, 0≤a<N. Evaluation at all roots is an invertible Vandermonde transformation on each m-column block, so full root-axis rank is equivalent to full rank of the moment-axis matrix with rows (p_a,1,p_[-a]_N).

Each moment entry is polynomial in the lower monic coefficients over K. At the complex good point, at least one N-column moment minor is nonzero. Therefore the product of that minor, c_0, and the discriminant is not the zero polynomial on the monic affine kernel. This affine kernel is itself defined over K and has a K-affine parametrization: the leading coefficient functional is nonzero on W_K. Since K is infinite, the nonzero guard product has a K-valued point. Thus the defining g can be chosen in K[t]. Only the coefficient polynomial is descended; its individual roots are not asserted to lie in K.

For the advertised bounded recipe, coefficients of t^a mod g have degree at most a−m+1 for a≥m, by induction on a, and degree zero for a<m. As a≤N−1, their degree is at most d. An N-column moment-axis minor has degree at most Nd. The discriminant has degree at most 2m−2, so the guard product has degree at most Nd+2m−1. Affine parametrization does not increase degree. A Cartesian grid with Nd+2m distinct rational integers per free coordinate cannot vanish identically on a nonzero polynomial of that total-degree bound. Testing c_0, discriminant, and full axis rank therefore terminates on this finite grid. This is not an efficiency claim.

## 10. Transfer to actual legal banks

All hypotheses of the previously reviewed whole-left realization are now met. Its positive physical rows work as follows. The −+ singleton has its forced amplitude T_b; the +− singleton has zero amplitude. Distinct nonzero roots allow ++ Vandermonde interpolation on the whole left interval. If there are more than m entries, the common recurrence propagates every remaining one; the matrix contains every required whole-left window. If fewer, a truncated consecutive-power Vandermonde solve suffices.

The -- group fits the b right/axis moments because b≤(N−1)/2≤m. The supports are disjoint in the needed way, and the exclusive coordinate a=N−b is already handled by T_b. Simultaneous reflection (a,b)↦(−a,−b) swaps ++ with -- and the cross orientations, using the same nodes; thus negative rows cause no new bank count or sector conflict. The now-proved moment-axis rank handles b=0.

Each alpha is either 1 or a distinct nonzero root of g; beta=1. Consequently Delta=−alpha^N≠0, so the literal geometric resolvent and finite-character inverse weight transform from the accepted construction are legal. They recover every Fourier Weyl coefficient and hence the original Fourier matrix. There are 2m+2 individual banks and N(2m+2) raw phase weights. Root splitting has degree at most m! over K. No root orbit or trace is counted as one bank.

## 11. Fresh controls and source preservation

The accompanying fresh_linear_saving_check.py was newly written for this review. It imports only Python standard-library modules and imports or executes no inherited research code. It verifies exact integer inequalities for all 49,988 odd orders from 27 through 100001 for step one, and all 49,979 odd orders from 45 through 100001 for step two. It separately constructs 24 prime-field controls at prime and composite N, checking chirp shifts, the parity merger, polynomial operator transformations, derivative annihilation, coordinate interval shrinkage, leading degrees, and nonzero Vandermonde products. No floating-point test is used.

FRESH_LINEAR_SAVING_RESULTS.json records those controls. These finite tests support boundary and implementation checks; Sections 2–10 provide the all-order characteristic-zero proof. The frozen source copies and their SHA-256 digests are recorded in SOURCE_BINDINGS.json and the two separate theorem receipts. Accepted predecessor files and the two author theorem files remain unchanged.
