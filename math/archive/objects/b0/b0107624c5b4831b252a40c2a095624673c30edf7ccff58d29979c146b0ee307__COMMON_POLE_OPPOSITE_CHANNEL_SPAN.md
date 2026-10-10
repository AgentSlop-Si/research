# Exact opposite-channel span obstruction for the eight common-pole routes

## Result and scope

Fix the eight nested N64 routes in this package. Give all eight Green operators one common complex pole t with t^64 != 1. No operator of the form

    M = sum_(j=0)^7 diag(a_j) (I-t P_j)^(-1)

can annihilate the high-x minus input sector while acting nontrivially on the plus sector. The masks a_j are arbitrary complex vectors, with zeros allowed. This includes every constant-coefficient linear combination. Thus these eight common-pole orders cannot supply a pure plus-to-minus mixer in the declared left-mask grammar.

For t != 0 the stronger fact is that annihilating minus forces every one of the 512 physical coefficients to vanish. The proof uses two exact determinant polynomials at each of 32 independent physical rows; their gcds have roots only at t=0 or at 64th roots of unity.

At the explicit pole t=1/2, all plus-annihilating operators are exactly

    diag(a) K,  K = G_H0minus - G_H0plus.

Here rank K=16. The pure minus-to-plus subfamily has a(i+32)=-a(i), and its rank is 16 whenever all mask entries are nonzero. This classifies that direction, including its paid masks and scan cost. It does not exclude arbitrary unequal pole schedules, operators with both channels present, products of layers, or the full N64 Fourier coefficient problem.

## 1. Exact routes, sectors, and conventions

Indices are v=8x+y for 0<=x,y<8. The eight labels, in order, are

    H0-, H0+, H1-, H1+, V0-, V0+, V1-, V1+.

Start from the corresponding MGG covers and least-representative splices on the 4-by-4 grid, then apply the already declared deterministic four-sheet nested lift to the 8-by-8 grid. The complete 64-entry successor arrays are included in `COMMON_POLE_SPAN_CERTIFICATE.json`, together with the source-label ordering. These are not independently spliced N64 routes.

Permutation matrices act by P e_v=e_(p(v)). Put

    X e_v = e_((v+32) mod 64),  Pi_sigma=(I+sigma X)/2.

All eight routes commute with X and satisfy P_j^32=X. This is checked from their successor arrays. Identify the sigma sector with C^32 by

    E_sigma e_k = e_k + sigma e_(k+32),  0<=k<32.

For every route define

    q_j(k) = p_j(k) mod 32,
    epsilon_j(k) = (-1)^floor(p_j(k)/32).

The exact sector restrictions are

    P_j E_+ = E_+ Q_j,
    P_j E_- = E_- S_j,
    Q_j e_k = e_(q_j(k)),
    S_j e_k = epsilon_j(k) e_(q_j(k)).

Every q_j is a 32-cycle. The product of its epsilon signs is -1, so Q_j^32=I and S_j^32=-I. All eight q_j tables and all eight signed-edge tables are supplied. Therefore

    G_j(t) E_+ = E_+ (I-t Q_j)^(-1),
    G_j(t) E_- = E_- (I-t S_j)^(-1).

Their denominators are respectively 1-t^32 and 1+t^32, both nonzero under t^64 != 1. This explicitly characterizes each route on both sectors without treating either projector as a free implementation primitive.

The H0-minus and H0-plus routes have identical q_j tables. They have different signed tables. Hence G_0(t) Pi_+=G_1(t) Pi_+ at every legal common pole.

## 2. Exact row-frame formula

Let pos_j(v) be the position of v on route j, starting at vertex 0. For a physical output row i and 0<=k<32, set

    d_j(i,k) = (pos_j(i)-pos_j(k)) mod 64,
    h_j(i,k) = d_j(i,k) mod 32,
    e_j(i,k) = floor(d_j(i,k)/32).

Then the eight-by-32 projected row frame is

    V_i^sigma[j,k]
       = G_j(t)[i,k] + sigma G_j(t)[i,k+32]
       = sigma^e_j(i,k) t^h_j(i,k) / (1-sigma t^32).

The 64-cycle geometric sum proves this formula. The second half of the output rows obeys V_(i+32)^sigma=sigma V_i^sigma, so only i=0,...,31 need separate certificates.

For a left-masked sum, row i of M E_sigma is the linear combination of the eight rows of V_i^sigma with coefficient vector (a_0(i),...,a_7(i)). These coefficient vectors are independent across physical output rows. This is why row-wise rank proves an obstruction even for completely arbitrary left masks, rather than just constant scalar coefficients.

## 3. Universal minus rank: a finite polynomial certificate

Remove the common denominator 1+t^32 from V_i^-. Its entries are signed monomials, (-1)^e t^h. For every i=0,...,31, the certificate supplies two eight-column sets and their exact integer determinant polynomials f_i(t), g_i(t). Each has degree at most 248.

It also supplies their monic gcd d_i in Q[t]. The verifier regenerates both determinants with an exact subset determinant algorithm and recomputes the polynomial gcd. It then verifies the factorization

    d_i(t) = t^v_i product_r c_(i,r)(t),
    c_(i,r)(t) divides t^64-1.

No approximate root test is used. For t != 0 and t^64 != 1, d_i(t) cannot vanish. Two polynomials both vanishing at t would force their gcd to vanish there. Therefore at least one of the two determinant minors is nonzero, and

    rank V_i^-(t)=8

for every such complex t. The same holds at i+32 by symmetry.

For example, the row-0 certificate uses columns

    [0,1,2,3,5,8,9,10] and [26,12,6,0,14,3,24,18].

Their monic gcd is

    t^40 (t-1) (t^16+1)^2.

All of its roots violate the declared guards. The machine-readable certificate contains the full polynomials and analogous data for every row; checking only the example row would not establish the arbitrary-mask statement.

The 64 universal minors are supplemented by 32 exact seven-by-seven plus minors evaluated at t=1/2. These prove the separate plus-sector classification below. Plus rank seven is not asserted at every legal complex common pole.

## 4. Opposite-channel impossibility in this span

For nonzero legal t, suppose M Pi_-=0. Equivalently, M E_-=0. The rank-eight frame in every physical row forces

    a_0(i)=...=a_7(i)=0  for every i.

Thus M=0. In particular, no nonzero M can satisfy M=Pi_- M Pi_+, the pure plus-input to minus-output condition. Nor can a constant-coefficient linear combination cancel the minus restriction while retaining a nonzero plus restriction.

The degenerate legal pole t=0 is handled separately: every Green equals I and M is a diagonal matrix diag(sum_j a_j). A diagonal matrix that annihilates E_- is zero. The operator-level no-go therefore also holds at t=0, although the coefficient representation is then nonunique and the rank-eight assertion does not apply.

For nonzero legal t, the 512-dimensional physical coefficient map into full operators is injective because its minus restriction is injective. Its restriction to minus-input matrices has dimension 512. This is an exact span statement for the fixed eight routes and one common pole; no general Fourier or runtime impossibility follows.

## 5. Complete plus-kernel and mixer classification at t=1/2

At t=1/2, each plus frame has rank seven. The exact equality between its H0 rows supplies the one-dimensional kernel

    span((1,-1,0,0,0,0,0,0)).

The 32 seven-minors certify there is no further dependence. Consequently

    M Pi_+=0  iff  M=diag(a) K,
    K=G_0(1/2)-G_1(1/2).

This is a 64-dimensional space of operators. Equivalently, the plus-input restriction of the physical coefficient space has rank 448 and kernel dimension 64. The constant-coefficient Green span has dimension eight; its plus restriction has dimension seven and its minus restriction dimension eight.

For any nonzero legal common t, the relative permutation P_0^(-1)P_1 consists of 16 transpositions and 32 fixed points. Hence rank(P_0-P_1)=16. The resolvent identity gives

    K(t)=t G_0(t)(P_0-P_1)G_1(t),
    rank K(t)=16,
    K(t)=Pi_- K(t) Pi_-.

The full relative-cycle list is included and regenerated. At t=1/2 every row of K is nonzero, which also follows from minus-frame independence. Moreover K_(i+32,:)=-K_(i,:). Therefore

    diag(a) K = Pi_+ diag(a) K Pi_-

holds exactly when a(i+32)=-a(i). This pure minus-to-plus subspace has 32 free complex mask entries. If all a(i) are nonzero, left multiplication by diag(a) is invertible and its rank is exactly 16. Masks with zeros may lower the rank, never raise it.

Taking a=chi_x, +1 on the first half and -1 on the second, recovers the explicit rank-16 mixer. Application uses exactly two length-64 Green scans, a vector subtraction, and a mask application. In the original grammar the two left masks are a and -a on labels 0 and 1. Both can be everywhere nonzero, and no extra route, right mask, projector, or endpoint permutation is silently added.

A standalone member of this plus-kernel family forces all six other term masks to zero. It therefore does not meet an additional requirement that every coefficient in an eight-term layer be nonzero. Adding such a component to another allowed layer must retain and verify the full coefficient accounting.

## 6. Relation to the accepted seed and the full problem

The accepted N16 seed uses distinct poles 1/2,1/3,...,1/9. A common-pole schedule changes that design. Neither this classification nor the earlier rank-16 component supplies a seed-preserving coefficient lift. It also does not prohibit layers whose plus and minus input blocks are both present; those are not one-way components and may have cancellations only after further composition.

The exact full 1536-coefficient N64 problem, arbitrary unequal pole schedules, and genuinely mixing prefix laws remain open. The conclusion here is specifically that the existing eight common-pole orders, with arbitrary left endpoint masks, do not close both pure directed sector channels.

## 7. Reproduction and provenance

`python check_common_pole_span.py --verify` regenerates all eight nested routes, their sector tables, the 64 universal minus minors and gcd factorizations, the 32 half-pole plus minors, and the relative-permutation rank certificate. It compares the resulting exact data with the saved JSON. The checker uses Python and SymPy for exact integer/rational polynomial arithmetic; it does not use a numerical root finder or a numerical coefficient fit. An extra exact evaluation at t=2 independently checks each determinant's sign against a direct matrix determinant.

All programs in this package were newly authored in this construction track. No uploaded source was executed. The earlier signed-pole package is preserved unchanged. Independent review is a separate acceptance step.
