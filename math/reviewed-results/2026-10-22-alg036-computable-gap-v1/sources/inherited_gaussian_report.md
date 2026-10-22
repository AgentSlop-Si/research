# ALG-036: equality, strict nondivisible gap, and failure of the rounded-block optimizer

Date: 2026-10-19 UTC. Owner: ALG-036; inherited priority 34 is unchanged.
Status: scoped proof candidate, awaiting independent review. Exact nondivisible maximizers remain open in this packet.

## 1. Results and inherited starting point

Let 1 <= d <= N be integers, let P be an orthogonal complex rank-d projector, and let Z have the proper complex Gaussian law CN(0,P). The convention is that CN(0,I_d) has density pi^(-d) exp(-||g||_2^2), so E|g_j|^2=1. The infinity norm uses complex moduli. Write

    F_r(P,b) = Pr(max_j |Z_j-b_j| <= r),
    p_j = P_jj,
    L_r(P) = product_(p_j>0) (1-exp(-r^2/p_j))^p_j,
    U_(N,d)(r) = (1-exp(-N r^2/d))^d,
    M_(N,d)(r) = sup_(rank P=d, b in C^N) F_r(P,b).

The reviewed ALG-036 thin-deficit packet proves F_r(P,b) <= L_r(P) <= U_(N,d)(r), and equal-block attainment when d divides N. Those inequalities, their complex normalization, and the concavity calculation are inherited results, not claimed as new here. The source report and review are recorded in SOURCE_MANIFEST.json.

This packet proves the following for every finite r>0.

1. Equality F_r(P,b)=L_r(P) holds exactly for phase-block projectors with constant magnitudes on each block, with b zero on every positive-leverage coordinate and |b_j|<=r on each zero-leverage coordinate. The block sizes need not agree.
2. Equality F_r(P,b)=U_(N,d)(r) holds exactly when d divides N, b=0, and, up to coordinate permutation and multiplication of coordinates by unit complex numbers, P is the projector onto d constant-coordinate blocks of common size N/d.
3. For d not dividing N, the supremum is attained and is strictly smaller than U_(N,d)(r). Thus there is a genuine positive gap delta_(N,d)(r)=U_(N,d)(r)-M_(N,d)(r)>0, uniform over all projectors and all translations at those fixed parameters. This is a nonquantitative gap, not an explicit formula for delta.
4. Nearly equal blocks are not the nondivisible optimizer in general. In fact, for every nondivisible N,d, a constant-diagonal projector beats every projector whose rows are partitioned into orthogonal complex-line groups, once r^2 > log(N)/(N/d-floor(N/d)).
5. In the smallest nondivisible case (N,d)=(3,2), at r^2=log 16,

       rounded blocks:             3825/4096,
       equal-diagonal construction: >=3904/4096,
       true maximum:               >=3904/4096 and <3969/4096.

   The construction therefore improves the rounded-block value by at least 79/4096, with an exact rational proof and no simulation. Conversely, the rounded-block construction beats this particular equal-diagonal construction at r^2=1/100. Neither comparison identifies the global maximizer at either radius.

The exact remaining gate is the maximization of a continuous, explicitly given integral over a two-dimensional compact simplex already for N=3,d=2. Section 8 specifies that integral. Nothing here settles sphere-prior algorithms, a critical-window gap uniform in changing N,d, arithmetic complexity, worst-case achievability, or all of ALG-036.

## 2. Primary equality theorem and its precise use

The additional primary source is Stefan Ingi Valdimarsson, *Optimisers for the Brascamp-Lieb inequality*, Israel J. Math. 168 (2008), 253-274, DOI 10.1007/s11856-008-1067-1. The author-hosted preprint was read directly:

https://uni.hi.is/siv/files/2017/07/optimisers.pdf

The relevant locations in that 17-page preprint are Definition 8 and Definition 9, printed page 10; Theorem 12, page 12; and the extension from Schwartz functions to general nonnegative integrable functions, pages 15-16. Page numbers refer to the preprint, not journal pagination.

Here is the specific consequence used. For geometric projection data sum_j c_j Pi_(E_j)=I with c_j>0, form all nonzero intersections obtained by choosing E_j or E_j-perp at each index. These are mutually orthogonal independent subspaces. On their orthogonal complement, equality inputs have Gaussian factors; on independent components they have common integrable factors. In particular, an output space contained in the dependent component has an everywhere-positive Gaussian input, up to a positive multiplier. Inputs on the same independent component are proportional. The theorem covers L1 inputs, including the disk-truncated densities used below.

This is an application of the published equality theorem, not a claim to have reproved its full classification. The following complex-line argument is the specialization established in this packet.

## 3. Equality in the refined leverage bound

### 3.1 Remove zero rows and force centering

Fix r>0. If p_j=0 then Z_j=0 almost surely. If |b_j|>r at such an index, F_r(P,b)=0, whereas L_r(P)>0. Equality is impossible. Otherwise that deterministic constraint may be omitted, including when |b_j|=r.

Factor P=VV* with V:C^d -> C^N an isometry. For each nonzero row v_j of V put B_j=v_j/sqrt(p_j), considered as a complex-linear map C^d -> C and also as its realification. It is a real rank-two coisometry, and

    B_j B_j*=I_C,                  sum_j p_j B_j*B_j=I_(C^d).

The accepted proof uses the nonnegative integrable input

    f_j(y) = pi^(-1) exp(-|y|^2) 1_{|sqrt(p_j)y-b_j|<=r}.

The proof has the chain

    F_r(P,b) <= product_j (integral f_j)^p_j <= L_r(P).

Each centered Gaussian disk integral is strictly larger than its translated version if its center is nonzero. To verify strictness, express the strictly radially decreasing Gaussian by its disk superlevel sets. At the superlevel radius equal to the test-disk radius, two distinct disks of the same radius have intersection area strictly less than the disk area. The strict loss persists on an interval of superlevel radii of positive measure. Integrating the loss proves strict inequality. All the exponents p_j are positive and all integrals are positive. Consequently equality in the chain forces b_j=0 at every nonzero row.

The remaining inputs, after identifying C isometrically with E_j=range(B_j*) in C^d, are

    f_j(x) = pi^(-1) exp(-||x||^2) 1_{||x||<=r/sqrt(p_j)},  x in E_j.

Each is a nonzero compactly supported density on a complex line E_j. In real notation E_j has dimension two. The geometric datum is sum_j p_j Pi_(E_j)=I, and the E_j span C^d.

### 3.2 Independent components are whole complex lines

Every E_j and its real orthogonal complement are invariant under multiplication by i. Therefore each intersection in Valdimarsson's independent decomposition is a complex-linear subspace.

An intersection that chooses E_j-perp at every index is zero, because the E_j span the entire space. Any nonzero independent component K must therefore be contained in at least one E_j. As a nonzero complex subspace of a complex line, K equals that E_j. For every other index k, the defining intersection forces either K subset E_k, in which case E_k=K, or K subset E_k-perp, in which case E_k is orthogonal to K.

It follows that independent components are exactly those row lines that are either identical or orthogonal to every row line. In particular, any row line not equal to an independent component is orthogonal to all independent components and hence is contained in the dependent component D.

If D were nonzero, at least one E_j would be contained in D: otherwise every row line would lie among the independent components, and their span would be the entire space, contradicting D nonzero. Valdimarsson's equality theorem would make that f_j an everywhere-positive Gaussian, up to scale. This contradicts its nonzero bounded disk support. Hence D=0.

Thus equality forces the distinct row lines to be pairwise orthogonal. There are exactly d distinct lines, because they span C^d. Partition the positive-leverage indices into classes I_1,...,I_d according to their common line, and put n_l=|I_l|.

### 3.3 Equal magnitudes inside each line class

On a shared independent line, the equality theorem makes the inputs proportional almost everywhere. Since they are the same Gaussian density cut off at radii r/sqrt(p_j), proportionality is possible only if these radii agree. Indeed, unequal positive radii give an annulus of positive area on which one input vanishes and the other is positive. Because r>0, p_j is constant within each class I_l.

Restricting the geometric identity to its common line gives

    sum_(j in I_l) p_j = 1.

Therefore p_j=1/n_l on I_l. Choosing an orthonormal basis indexed by the d row lines, the row v_j has precisely one nonzero entry, equal to zeta_j/sqrt(n_l), where |zeta_j|=1. Consequently

    P = sum_(l=1)^d u_l u_l*,
    (u_l)_j = zeta_j/sqrt(n_l) for j in I_l, and 0 otherwise.

All coordinates outside the classes are zero-leverage coordinates. This is the asserted phase-block form.

Conversely, for a projector of this form and the specified b, the coordinate event is exactly the intersection of d independent events |g_l|<=sqrt(n_l)r. Its probability is

    product_(l=1)^d (1-exp(-n_l r^2)).

The n_l identical leverage factors with exponent 1/n_l multiply to the same expression. This proves both necessity and sufficiency, including zero rows and their allowable translations.

## 4. Equality in the ambient rank-only bound

The inherited strict concavity calculation is, for a=r^2>0,

    h_a(p)=p log(1-exp(-a/p)),       h_a(0)=0,
    h_a''(p)=-a^2 exp(a/p)/(p^3 (exp(a/p)-1)^2)<0,  p>0.

Its continuous extension is strictly concave on [0,infinity). Jensen over all N leverage values, including zeros, is equality exactly when every p_j=d/N. In particular, no zero-leverage coordinate is permitted in ambient equality.

If F_r(P,b)=U_(N,d)(r), both inequalities in F<=L<=U are equalities. Section 3 supplies the phase-block structure and b=0. On block l its leverage is 1/n_l, and hence 1/n_l=d/N for every l. Thus n_l=N/d is an integer and d divides N. Conversely every such equal-size phase-block projector with b=0 attains U, as inherited from the original calculation.

This gives the complete equality classification of the ambient bound at finite positive radius. Equal diagonal leverage alone is not enough: unless the complex-line geometry also has the stated block form, the first inequality is strict.

## 5. From nonattainment to a uniform strict gap

Pointwise strictness by itself would not rule out a sequence approaching U. We now show the supremum is attained. We first dispose of all translations, including shifts outside the singular Gaussian support.

### 5.1 Centering maximizes probability, with a direct proof

Fix V as above and set

    A_b = {g in C^d: ||Vg-b||_infinity <= r}.

For R>0, let C_b(R)=A_b intersect {||g||_2<=R}. These are compact convex sets, and C_-b(R)=-C_b(R). Convexity of both norm balls gives

    (C_b(R)+C_-b(R))/2 subset C_0(R).

The standard auxiliary geometric theorem invoked here is the classical Brunn-Minkowski inequality: for nonempty measurable sets A,B in R^n, volume((A+B)/2)^(1/n) >= (volume(A)^(1/n)+volume(B)^(1/n))/2 whenever the sets involved are measurable. Applied to these compact convex sets in real dimension 2d, it gives

    volume(C_0(R)) >= volume(C_b(R)).

The conclusion is immediate if the latter volume is zero; otherwise it is the usual inequality applied to two sets of equal volume. Layer-cake integration of exp(-||g||_2^2) over its centered ball superlevel sets yields F_r(P,b)<=F_r(P,0). This proof works directly in the nonsingular variable g and makes no unsupported continuity claim for shifted degenerate Gaussians. In particular,

    M_(N,d)(r) = max_(rank P=d) F_r(P,0),

provided the centered maximum exists.

### 5.2 Centered continuity and compactness

The set

    G_(N,d) = {P in C^(N x N): P=P*, P^2=P, tr(P)=d}

is closed and bounded, hence compact. The trace condition fixes the rank for Hermitian idempotents.

Let G~CN(0,I_N), so PG~CN(0,P). If P_k tends to P in this set, P_k G tends to PG pointwise under this common coupling. For r>0, the boundary event max_j |(PG)_j|=r has probability zero. Indeed, it is contained in the union of the events |(PG)_j|=r. When p_j>0 the scalar coordinate has a continuous complex Gaussian density, and when p_j=0 it is identically zero, which is strictly inside the radius-r disk. Thus dominated convergence gives

    F_r(P_k,0) -> F_r(P,0).

The maximum over G_(N,d) is attained. If d does not divide N, Section 4 rules out its equality with U. Therefore

    M_(N,d)(r) = U_(N,d)(r)-delta_(N,d)(r),
    delta_(N,d)(r)>0.

This gap holds for all translations by the centering inequality. It is a rigorous existence statement; this packet does not supply a computable lower bound for delta.

The same argument gives joint continuity in (P,r) for r>0. Therefore M and delta are continuous in r, and for fixed nondivisible N,d the gap has a positive minimum on every compact interval 0<r_0<=r<=r_1<infinity. No uniformity as N,d change, r tends to zero, or r tends to infinity is asserted.

## 6. Rounded blocks fail for every nondivisible family at sufficiently large radius

There exists a constant-diagonal rank-d projector for every N,d. For example let V be any d columns of the normalized N-by-N discrete Fourier matrix. The elementary roots-of-unity orthogonality identity gives V*V=I_d and ||v_j||^2=d/N. This is solely a finite frame construction. It makes no claim about FFT complexity or query implementation costs.

For this P, every scalar coordinate has variance d/N. Independence is unnecessary for the union bound:

    F_r(P,0) >= 1-N exp(-N r^2/d).                         (6.1)

For comparison, consider any rank-d projector whose nonzero rows occupy d mutually orthogonal complex lines. Allow unequal magnitudes within a line. If that class has n_l coordinates, its leverage values sum to one, so their maximum is at least 1/n_l. The probability of satisfying that entire class is

    1-exp(-r^2 / max_(j in I_l) p_j) <= 1-exp(-n_l r^2).

Classes are independent. Thus constant magnitudes maximize probability within each class. Zero coordinates cannot improve the best value; with at most N positive coordinates, at least one of the d class sizes is at most m=floor(N/d). The total success probability is at most

    1-exp(-m r^2).                                         (6.2)

If d does not divide N, N/d-m>0. Whenever

    r^2 > log(N)/(N/d-m),

we have N exp(-N r^2/d) < exp(-m r^2). The lower bound (6.1) strictly exceeds the upper bound (6.2). The constant-diagonal construction therefore beats every orthogonal-line block projector at these radii. By Section 5, translations cannot rescue any of them.

For completeness, among constant-magnitude block projectors using all coordinates, nearly equal block sizes are best: log(1-exp(-a t)) is strictly concave in t>0, so moving one coordinate from a block at least two larger to the smaller block increases the product. This concerns only that block family, not the global maximum.

## 7. Two exact comparisons for rank 2 in three coordinates

### 7.1 A rational large-radius counterexample

Take

    P_equal = I_3 - (1/3) 1 1*,
    P_block = [[1/2,1/2,0],[1/2,1/2,0],[0,0,1]].

Both are orthogonal rank-two complex projectors. P_equal has diagonal 2/3; P_block has block sizes 2 and 1. Set a=r^2=log 16. Then exp(-a)=1/16 and exp(-3a/2)=1/64. The union bound and exact block probability give

    F_r(P_equal,0) >= 1-3/64 = 61/64 = 3904/4096,
    F_r(P_block,0) = (1-1/16)(1-1/256) = 3825/4096.

The difference is at least 79/4096>0. The inherited ambient upper is (1-1/64)^2=3969/4096, and Section 5 makes that upper strict for the true maximum. Hence

    3825/4096 < 3904/4096 <= M_(3,2)(sqrt(log 16)) < 3969/4096.

The lower bound for P_equal need not be its exact probability. The rational inequalities already prove the counterexample.

### 7.2 The same equal-diagonal plane loses to blocks at a small radius

Write the plane of P_equal as z=(x,y,-x-y). Its induced real four-dimensional volume element is 3 dA(x)dA(y): the complex Gram determinant of this parameterization is 3. Scaling x and y by r shows

    F_r(P_equal,0) <= C a^2,
    C = 3 - 9 sqrt(3)/(4 pi) < 9/5,
    a=r^2.

Here the coefficient is the density-at-zero normalized section volume. To derive it, let D be the unit disk. For fixed x with |x|=s<=1, the allowed y lie in D intersect (D-x), whose area is

    2 arccos(s/2) - (s/2) sqrt(4-s^2).

Therefore the normalized coefficient is

    C = (6/pi) integral_0^1 s [2 arccos(s/2)-(s/2)sqrt(4-s^2)] ds
      = 3 - 9 sqrt(3)/(4 pi).

The probability bound simply replaces exp(-||z||^2) by 1 on the section. The estimate C<9/5 is elementary; for instance pi<22/7<15 sqrt(3)/8, where the latter comparison follows by squaring positive numbers.

For the block projector, integrate its density over the independent disks |g_1|<=sqrt(2a), |g_2|<=sqrt(a). Throughout this product, ||g||^2<=3a, while its normalized volume is 2a^2. Thus

    F_r(P_block,0) >= 2a^2 exp(-3a) >= 2a^2(1-3a).

At a=1/100, this is (97/50)a^2>(9/5)a^2>C a^2. So blocks beat the equal-diagonal plane at this explicit radius. This proves only a comparison of two constructions. It does not prove blocks globally optimal for any positive radius.

## 8. Exact remaining gate in the smallest nondivisible case

Every rank-two projector in C^3 is P=I-u u* for a unit vector u. Diagonal unitary invariance of the modulus event removes the phases, so the centered probability depends only on

    q_j=|u_j|^2,            q_j>=0,          q_1+q_2+q_3=1.

Coordinate permutations also preserve it. We can choose the label with q_3=max_j q_j>=1/3. Let alpha=sqrt(q_1/q_3), beta=sqrt(q_2/q_3). The plane is parameterized by

    z=(x,y,-alpha x-beta y).

Its complex Gram determinant, hence its real four-volume factor, is 1/q_3. Consequently the exact centered probability is

    Phi_r(q) = 1/(pi^2 q_3) integral_{
        |x|<=r, |y|<=r, |alpha x+beta y|<=r
      } exp[-|x|^2-|y|^2-|alpha x+beta y|^2] dA(x)dA(y).

This formula remains valid when q_1 or q_2 is zero because q_3>=1/3. It and Section 5 give the exact reduction

    M_(3,2)(r) = max_{q_j>=0, sum q_j=1, q_3=max q_j} Phi_r(q).

The unresolved task is to identify this maximizer, or its maximum value, as a function of r. The present packet does not prove that a maximizer has two equal q_j, that only the block and equal-diagonal candidates compete, or that a transition occurs at a specified radius. It also does not give the numerical value of the strict gap. The two exact comparisons warn against assuming one radius-independent optimizer.

## 9. Checks, limitations, and provenance

The fresh self-authored checker controls/check_nondivisible.py performs exact symbolic projector, Jacobian, concavity, and rational-comparison checks; exact small-section integration; finite block identities; and numerical diagnostics of the elementary all-dimension sufficient threshold. These checks supplement the proofs and cannot establish the general equality theorem, compactness argument, or global optimizer.

No historical program was executed. The inherited files were only read and hashed. No external write, GitHub commit, publication, or modification of the inherited packet was performed. This packet closes the finite-positive-radius equality and nonattainment questions and disproves the rounded-block optimum in general. It leaves exact nondivisible extrema, their changing-dimension asymptotics, and the broader ALG-036 gates open.
