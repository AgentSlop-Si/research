# Eight explicit Hamiltonian orders escape the balanced additive cut-count obstruction

## Status

This is a constructive geometry lemma, **not a Fourier factorization, faster FFT, or novelty claim**. It provides eight uniformly enumerable Hamiltonian cycles at every dyadic length. For every balanced vertex cut, the sum of their incoming-edge counts is large enough that three eight-term Green layers cannot be rejected by the elementary additive per-term cut-rank budget once N >= 2^17. It does not prove that any sum or product attains that budget, satisfies Fourier coefficient identities, or has a fast recursively closed parameter generator.

The earlier natural-plus-bit-reversal exclusion remains unchanged. The construction changes its fixed two-order geometry to eight new orders. The number of terms, 24 across three layers, must be counted explicitly.

## 1. The eight permutation covers and the external theorem

Write N=2^k, m=2^floor(k/2), r=log2(m). Take a=b=m for even k, and a=2m, b=m for odd k. Identify the vertex (x,y) in Z_a x Z_b with the integer bx+y. For c in {0,1} and epsilon in {-1,+1}, define

    H(c,epsilon)(x,y) = (x+epsilon(2y+c) mod a, y),
    V(c,epsilon)(x,y) = (x, y+epsilon(2x+c) mod b).

These eight labeled maps are permutations; each minus map is the inverse of the corresponding plus map. Parallel arcs and loops are retained. They are cycle covers, not yet Hamiltonian cycles.

The only external spectral input is the classical Margulis–Gabber–Galil theorem. For the square Z_n x Z_n, the sum A of these eight permutation matrices obeys

    |f^T A f| <= 5 sqrt(2) ||f||^2 whenever sum(f)=0.

The official Archive of Formal Proofs source explicitly gives the maps in `mgg_graph_step`, degree eight, and this unnormalized inequality in `mgg_numerical_radius_aux`; its normalized bound is 5 sqrt(2)/8. Source checked 2026-10-09: https://isa-afp.org/browser_info/current/AFP/Expander_Graphs/Expander_Graphs_MGG.html . We invoke this established theorem, not a fresh proof of it. All deductions below are separate elementary arguments.

### Rectangular quotient

For a=2m and b=m, let pi: Z_(2m)^2 -> Z_(2m) x Z_m be pi(x,y)=(x,y mod m). The two points in each fiber differ by (0,m). Every labeled square map descends through pi: an H displacement changes by epsilon*2m under y -> y+m, and a V displacement is independent of y. Thus pi T = Tbar pi, including both signs and both c values. Each fiber has two points and each quotient map is a permutation. Consequently the quotient is an equitable regular multigraph of degree eight, with exactly the displayed rectangular maps.

For any real quotient vector f, put Jf=f composed with pi. Then A_square J=J A_rectangle, ||Jf||^2=2||f||^2, and sum(Jf)=2sum(f). Applying the square inequality to Jf and cancelling two proves the same bound 5 sqrt(2) for the rectangular adjacency. The construction does not discard labels, merge parallel edges, or change their multiplicities.

## 2. Cut expansion before splicing

Let S have size s and let e_T(S)=#{v outside S:T(v) in S}. Let delta=8-5sqrt(2)>0. Since A is symmetric and eight-regular, applying the spectral inequality to 1_S-(s/N)1 gives

    E(S):=sum_T e_T(S) = 8s - 1_S^T A 1_S
         >= delta s(N-s)/N.

For balanced S this is E(S)>=delta N/4. This is a one-direction incoming count; no further factor of two is needed. Each permutation also has equally many incoming and outgoing crossing arcs.

## 3. Deterministic Hamiltonian splicing and the half-loss lemma

Decompose any cover T into c directed cycles. For each cycle choose its least integer vertex a_j, order these representatives increasingly, and put b_j=T(a_j). Replace only the c arcs a_j -> b_j by

    a_j -> b_(j+1 mod c).

If c=1, leave T unchanged. The resulting permutation P is one Hamiltonian cycle: follow a cycle from b_j to a_j, then move to b_(j+1), and continue through all cover cycles. The construction is independent of S.

**Half-loss lemma.** For every S,

    |e_P(S)-e_T(S)| <= floor(c/2).

To prove this, inspect only the selected c arcs. Their tail multiset and head multiset are unchanged. If alpha selected tails lie outside S and beta selected heads lie inside S, the incoming count of either matching lies between max(0,alpha+beta-c) and min(alpha,beta). Its possible range therefore has width

    min(alpha,beta,c-alpha,c-beta) <= floor(c/2).

For c=1 the true loss is zero. The displayed general bound is safe. Bounding the loss by c would waste a factor of two. The proof uses endpoint preservation and works for any permutation splice of these heads.

## 4. Exact cover cycle counts

A translation z -> z+d on Z_h has gcd(h,d) cycles, with gcd(h,0)=h. For h=2^t,

    sum_(z=0)^(h-1) gcd(h,z) = h(1+t/2).

Indeed the z=0 contribution is h; for each valuation j=0,...,t-1 there are 2^(t-j-1) terms of value 2^j, giving t*h/2 more. Assume m>=2 in the following formulas.

For the square, the cycle counts per sign are

    c(H0)=c(V0)=sum_y gcd(m,2y)=m(r+1),
    c(H1)=c(V1)=m,

because all odd steps are units modulo m. Across both signs and both directions, the total is C_square=4m(r+2). The half-loss sum is at most D_square=2m(r+2).

For the rectangle, the counts per sign are

    c(H0)=sum_(y<m) gcd(2m,2y)=m(r+2),
    c(H1)=m,
    c(V0)=sum_(x<2m) gcd(m,2x)=2m(r+1),
    c(V1)=2m.

Their total is C_rectangle=2m(3r+7), and the half-loss sum is at most D_rectangle=m(3r+7). These are exact cover-cycle totals, not estimates. The m=1 cases can be constructed by the same algorithm but are outside these count formulas and the large-N claim.

Combining the expansion and half-loss lemmas gives, for all S,

    sum_(j=1)^8 e_(P_j)(S) >= delta s(N-s)/N - D,

where D is the appropriate expression above. In particular every balanced S satisfies sum_j e_(P_j)(S)>=delta N/4-D.

## 5. The three-layer threshold, checked without floating point

The additive per-term cut-rank budget for three layers, each containing all eight cycle orders, is 3 sum_j e_(P_j)(S). We prove this counting budget exceeds N/2 for every balanced S if

    3(delta N/4-D)>N/2,

equivalently, putting X=22N-12D,

    X>0 and X^2>450N^2.

This last form is an exact integer check. In the square case the condition reduces to

    (22-15sqrt(2))m > 24(r+2).

It holds at r=9, m=512, N=262144, and continues to hold for all larger r because m doubles while r+2 only increases by one. It fails at the preceding dyadic m=256; this means only that this bound is insufficient there.

In the rectangle it reduces to

    (22-15sqrt(2))m > 6(3r+7).

It holds at r=8, m=256, N=131072, and persists for larger r by the same doubling argument. It fails at m=128. Hence every dyadic N>=2^17 is covered.

A simpler rational certificate, independently suggested by the reviewer, uses sqrt(2)<17/12 (since 2<289/144). Thus delta/4>11/48 and the three-layer margin is strictly greater than 3N/16-3D. At the first rectangle threshold D/N=31/512<1/16, giving a rational margin of 768; at the first square threshold D/N=22/512<1/16, giving 15360. Both normalized losses decrease when r increases, proving the entire tail without decimal arithmetic.

At the first rectangle threshold the certified per-layer lower bound is approximately 22503.24994, so the three-layer budget exceeds N/2 by approximately 1973.74982. At the first square threshold the corresponding values are 49614.49988 and 17771.49964. The proof and controls use exact integer radical comparisons rather than these display approximations.

## 6. Connection to weighted Green terms, and its strict limit

Use the convention P e_v=e_(P(v)). For any invertible A=I-D_w P, the complementary inverse-submatrix rank identity gives

    rank(A^(-1)[S,S^c])=rank(A[S,S^c])<=e_P(S).

The sparse crossing block is a partial matching. If all crossing weights are nonzero its rank equals e_P(S). This equality does not require the principal diagonal subblocks of A to be invertible. Diagonal endpoint factors preserve that rank when nonzero; cut-preserving endpoint monomials do likewise. Sum and product rank subadditivity give the additive per-term upper bound. A bank that preserves S contributes zero to it.

Every balanced Fourier cross block has rank at most N/2, simply by its dimensions. The proved edge-count budget is therefore too large to contradict that rank by this particular argument for any balanced S, even before restricting S to unions of bank blocks.

The obstruction tested here uses the **same balanced subset S at every stage**. This does **not** show a lower bound on the rank of a sum of Green terms, on a product, or on its actual network min-cut. Cancellations and more refined obstructions remain possible. Neither non-balanced cuts nor arbitrary multi-stage separators with different intermediate subsets have been eliminated. No Fourier coefficient values, endpoint masks, bank recursion, or compatible seed have been constructed here.

## 7. Uniform enumeration and cost ledger

The maps need constant work per vertex with O(log N)-bit integer coordinates. For each of eight maps:

1. Emit its successor array using the displayed modular formulas.
2. Scan vertices in integer order with a visited bit array; traverse each unvisited cycle once and record its representative.
3. Rotate the representative successors as in section 3.
4. Traverse the resulting Hamiltonian cycle once, starting at vertex zero, to emit its ordering sigma and inverse ordering. Then P=sigma Z sigma^(-1).

The total is O(N) word-RAM operations and O(N) words of storage; no sorting, factorization, cycle search, optimization, or random choice is required. This is not an O(N) bit-complexity claim: emitting the indices already needs Theta(N log N) bits. The deterministic rules are valid for every N in the specified dyadic family.

For supplied edge weights, each nonsingular weighted Hamiltonian Green term can be applied in O(N) field operations by one cyclic first-order recurrence, computing the wrap denominator 1-product(w), then a second scan. Thus applying a supplied eight-term layer is O(N) field operations with eight terms explicitly charged. Taking all weights 1/2 in characteristic zero gives an elementary example where every Green inverse exists. It does not supply Fourier-compatible coefficients. The cost or existence of generating such coefficients remains wholly open.

## 8. Controls, reproducibility, and next gate

`check_expanding_cycles.py` is newly authored from the formulas in this note; it imports no uploaded or inherited research source. It checks exact cycle totals, permutation inverses, quotient commutation, Hamiltonicity, exact changed tails, preserved head sets, the half-loss lemma, full and sampled cuts, exact threshold inequalities, and exact finite-field Green rank/recurrence controls. `CONTROL_RESULTS.json` and `CONTROL_RUN.log` contain its output. The external MGG theorem is not replaced by finite numerical checks.

The next meaningful constructive gate is a full coefficient-compatible identity using these orders, with a valid dyadic seed and an explicitly charged uniform coefficient generator. Merely displaying these cycles is not a candidate FFT.
