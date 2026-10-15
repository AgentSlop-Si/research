# Independent adversarial mathematical audit

Date: 2026-10-13 UTC.

## Decision

**ACCEPT** the exact finite bound, the fixed-r, fixed-q best-approximation limit one, and the bounded-q branch-growth corollary, within the stated **bare additive** model and its **all-nonnegative-weight separator hypothesis**. No mathematical repair to the proof or constants is required.

The audited archive is `Separator_Fragmentation_Candidate_20261013.zip`, SHA-256 `a3c374a9a8f1c23f1d4911c90cc8cc2f3b47843ce97318ee4e635b14d2ff5f34`. The unpacked REPORT.md and CONTRACT.md were byte-compared with their archive entries. No candidate or historical code was executed. Fresh controls are corroboration only; acceptance rests on the proof below.

This decision establishes no historical novelty, worldwide priority, algorithmic speedup, product closure, correction extension, or general FFT lower bound.

## Exact accepted statement

Let all matrices in a branch be N-by-N, let N,r,q be positive integers, and let U be unitary with all entries of modulus 1/sqrt(N). Set

T = sum_i L_i Q_i^{-1} R_i,

where Q_i is invertible, L_i and R_i have support contained in possibly different permutation matrices, and the undirected support graph of H_i = [[0,Q_i],[Q_i^T,0]] has a vertex separator of at most q vertices leaving components of at most half the total weight, for every nonnegative weighting. Endpoint coefficients may vanish or be arbitrarily large complex numbers.

For every integer h >= 1, put b=3^h, Q=q(b-1)/2, R=rqh, and P=[b(b-1)]^r. Then

||U-T||_F^2/N >= max(0, 1-r/2^h-(rQ+RP)/N),

and the same right-hand side bounds ||U-T||_2^2 from below.

For avoidance of notation ambiguity, scalar Q above is a deletion budget and differs from branch denominator Q_i.

## Proof audit

### 1. Heredity is sufficient and correctly proved

Extend a weighting of an induced vertex set V by zero outside V. A component of G[V] minus X intersect V is contained in a component of G minus X and hence has weight at most half the weight on V. The selected separator inside V has at most q vertices. This uses the stated quantifier over all weights and does not follow merely from separators for some prior selected markings.

For the actual recursion it is enough that each encountered induced graph has a cardinality-balanced separator. The all-weight property is a clean sufficient global assumption, not an assertion that a particular prior marked-set guarantee is equivalent to it.

### 2. Three-bin packing, depth and deletion budgets are valid

At a node with W vertices, component sizes are at most W/2 and total remaining size is at most W. In next-fit packing, if four bins existed, bins 1 and 2 together would have load greater than W/2, and so would bins 3 and 4. Their total would exceed W, a contradiction. This argument works for odd W without rounding the capacity upward.

At depth h there are at most 3^h leaf groups of size at most 2N/2^h. The maximum number of separator calls is (3^h-1)/2. Their deleted vertices are disjoint across recursion nodes, and their total number is at most Q. Empty groups need no calls. If small groups are entirely deleted, the conclusions become weaker or vacuous rather than false.

### 3. The path-boundary improvement really is qh

For a leaf A, take any original graph edge from v in A to w outside A. At the first recursion level where v and w cease to lie together, they cannot go into distinct child bins: bins contain whole components after removing the separator and have no edges between them. Therefore w belongs to that level's separator on A's ancestor path.

Thus every original neighbor of A outside A lies in the union Z_A of its at most h ancestral separators. In particular, separators deleted in other subtrees are not extra boundary vertices. The full original-matrix cut H_i[A,A^c] has at most qh nonzero columns, so its rank is at most qh. It is unnecessary to pay all Q deleted vertices in the rank bound.

### 4. Inverse-cut rank needs no principal-block invertibility

Here is a direct field-independent proof of the used identity. Let J=A^c and E_J be its coordinate subspace. The kernel of H[A,J] consists of x in E_J with Hx in E_J. Since H is invertible, the map x -> Hx bijects this kernel onto the kernel of H^{-1}[A,J], understood on E_J. Both rectangular matrices have |J| columns and equal kernel dimensions, so their ranks are equal.

This proves rank H^{-1}[A,A^c] = rank H[A,A^c] without Schur-complement pivot assumptions. It applies over the complex numbers, to nonsymmetric matrices, and when either diagonal principal block is singular. The transpose-symmetric lift is therefore legitimate without being Hermitian.

Since H_i^{-1} = [[0,Q_i^{-T}],[Q_i^{-1},0]], restricting to lower-half rows in one leaf and upper-half columns in a different leaf yields inverse rectangles of rank at most qh.

### 5. Independent endpoint maps and deleted area are correct

Every partial monomial support can be completed to a permutation support; zero coefficients cause no obstacle. A branch term on output coordinates has entries

l_x (Q_i^{-1})_{sigma_i(x),tau_i(y)} r_y,

with two independent bijections. Thus endpoint restrictions and scalings cannot increase rank, and no agreement across branches or between the two endpoint permutations is needed.

One deleted lift vertex excludes at most one output coordinate, in exactly one of the two endpoint types. Consequently, if a output rows and c output columns are excluded by any branch, a+c <= rQ. The lost number of matrix entries is N(a+c)-ac <= rQN. There is no missing factor two.

### 6. Same-leaf area and refinement count are correct

For a branch and leaf j, let a_j and d_j be the counts of surviving routed lower and upper vertices. With v_j=a_j+d_j, one has max v_j <= 2N/2^h and sum v_j <= 2N. Hence

sum_j a_j d_j <= (1/4)sum_j v_j^2 <= N^2/2^h.

The union bound over branches loses at most rN^2/2^h entries, with no probabilistic independence premise. Together with endpoint deletion, this leaves good area at least N^2(1-r/2^h)-rQN.

The tuple partition is performed independently on rows and columns. A good ordered tuple pair differs in every coordinate, so at most [b(b-1)]^r nonempty good rectangles occur. Their entries are disjoint even though their row sets or column sets may overlap. Each summand has rank at most qh on each good rectangle and the actual sum has rank at most rqh.

### 7. Energy and operator normalization are correct

Every coordinate submatrix V of U is an operator contraction, with ||V||_2 <= 1, and has squared Frobenius energy equal to its number of entries divided by N. Removing at most R singular directions can remove at most R units of squared energy. Therefore every rank-at-most-R approximation B satisfies

||V-B||_F^2 >= |V|/N-R.

An equivalent elementary proof projects onto the column space of B: the projection has dimension at most R, captures at most R energy because V is a contraction, and the orthogonal residual of V-B equals that of V. This also handles rectangular cells and R exceeding their dimensions; a negative right-hand side remains valid.

Summing over disjoint cells gives ||U-T||_F^2 >= N(1-r/2^h)-rQ-RP. Divide by N and clip by nonnegativity. Since ||E||_F^2 <= N||E||_2^2 for the full N-by-N error, the operator lower bound follows with exactly the same squared constant.

This argument addresses unbounded-coefficient cancellation: it bounds the rank of the actual sum on a cell, never a sum of individual errors. Cross-cell squared errors cannot cancel because cells have disjoint entries. Neither norm nor conditioning bounds on denominators or coefficients are used.

## Sharpness, asymptotics and branch growth

### Legal zero approximation and fixed-parameter limit

For Q_i=I, the support lift is a disjoint matching. Under any nonnegative weighting of total W, at most one matching edge can have total weight greater than W/2. If there is one, delete its heavier endpoint. Its surviving endpoint has weight at most half the edge's weight, hence at most W/2; all other components were already light. This proves a separator budget of one, also covering W=0. Thus the construction is legal for every q>=1.

Taking L_i=0 makes T=0, with relative Frobenius norm and operator norm both exactly one. For fixed r,q, first choose fixed h with r/2^h arbitrarily small, and then send N to infinity. The theorem and the legal zero construction squeeze both best achievable errors to one, uniformly over normalized flat unitaries. This concerns the infimum over the model; no attained optimizer is required.

There is no exact finite-N optimality claim. For example, a legal diagonal approximation can achieve squared relative Frobenius error 1-1/N. That example is consistent with the limiting statement.

### Growth corollary

Write 0 <= eta < 1 and delta=1-eta^2. If either norm error is at most eta and h=ceil(log_2(2r/delta)), then r/2^h <= delta/2, and the raw (unclipped) inequality forces

N <= (2/delta)[rq(3^h-1)/2+rqh{3^h(3^h-1)}^r].

The clipping does not interfere, since the maximum is always at least its raw argument. There is no division by a quantity such as N-R, and thus no hidden pole or missing dimension guard.

Let a=log_2(3) and C_delta=3(2/delta)^a. The ceiling gives 3^h <= C_delta r^a. Also Q <= qb/2, P <= b^{2r}, and h>=1, which imply

N <= (4rqh/delta)(C_delta r^a)^{2r}.

For fixed eta and bounded q, taking logarithms yields log N <= C_eta,q r log(r+1); equivalently r=Omega(log N/log log N). This is not Omega(log N). If q varies, log q must be retained. An immediate equivalent limiting implication is that bounded q and r=o(log N/log log N) still force best achievable errors to tend to one. No product or arbitrary FFT statement is entailed.

### Rounding and small cases

All parameters N,r,q,h are positive integers, (3^h-1)/2 is integral, and h need not be limited by log N. Very large h can delete all vertices or make the bound negative; clipping yields zero. At N=1 the finite bound can be vacuous while exact representation is legal. Large q, large r, or ranks larger than a cell dimension likewise produce no contradiction. Singular Q_i are excluded; no formula has silently extended through a denominator's pole.

The displayed finite comparison is arithmetically correct: at N=64 and r=q=h=1, the new squared relative-Frobenius bound is 25/64, exceeding 377/4096. This verifies the numerical comparison stated in the candidate, without independently certifying the entire predecessor theorem.

## Independent exact controls

Fresh standard-library code, written for this review, passed:

- 31,228 ordered integer packing sequences, original size at most 14; three bins are sometimes necessary.
- All 11,808 invertible 3-by-3 ternary matrices and all eight complementary cuts: 94,464 exact inverse-cut checks, including 21,120 cuts whose relevant principal block is singular.
- 729 nonnegative integer weightings of a three-edge matching, validating the legal zero construction in that finite domain.
- 16 path-lift families with N=16 or 64, r up to 3, h up to 4, independent row/column routing, nontrivial zero masks, and coefficients with magnitude up to one million.
- 641 good refinement cells and 999 branch-cell exact-rank checks, including full original-edge path-boundary checks, deletion and good-area bounds, inverse identities, cell disjointness, and actual exact squared errors.
- 600 exact rational ceiling/growth checks and the displayed finite comparison.

Only two tested universal bounds were positive; the remaining parameter cases intentionally check degeneracies, rank bookkeeping, and vacuity. These finite checks do not certify the infinite parameter domain. The mathematical proof supplies that certification.

Files: `fresh_math_controls.py`, `fresh_math_controls.json`. Script SHA-256: `af898d29d99314881ff1fba62c9ef55f3584f14030798742914c369bf98419b7`.

## Primary-source verification

Three primary documents were independently opened and their relevant clauses checked:

- Chandrasekaran, Epperly and Govindarajan, GIRS v3, Proposition 2.1, printed page 5: complementary off-diagonal ranks are preserved by inversion. The nearby Proposition 2.3 is explicitly common-graph algebra and is not used to merge different branch graphs. https://arxiv.org/pdf/1911.05858v3
- Bodlaender and coauthors, Section 2.1, printed page 5, states all-weight half-component separators for bounded treewidth. Lemma 2.9, printed page 12, gives the three-part formulation; its later proof uses an elementary packing observation. https://sites.cs.ucsb.edu/~daniello/papers/treewidthApproxJ.pdf
- Li and Strang, Theorem 1, printed pages 1-2: truncated singular-value approximation is optimal for unitarily invariant norms, with rectangular matrices and the relevant norms covered. https://cklixx.people.wm.edu/uinorm-note.pdf

These matches confirm that the proof ingredients are classical. They do not independently establish novelty or exhaust literature on the assembled theorem.

## Optional editorial clarifications

These are not acceptance blockers:

1. State explicitly that Q_i,L_i,R_i are N-by-N.
2. State tolerance as 0 <= eta < 1.
3. Define “minimax” if retained; “best approximation error, uniformly over normalized flat unitaries” describes exactly what is proved.
4. Keep the all-weight hypothesis visible whenever comparing this result with weaker selected-marking formulations.
