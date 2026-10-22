# ALG-036 computable nondivisible Gaussian gap

Date: 22 October 2026 UTC. Status: proof candidate for separate verification.

## 1. Result and exact scope

For integers `1 <= d <= N` with `d` not dividing `N`, and rational numbers `0 < r0 <= r1 < infinity`, the procedure below terminates and returns a rational number `gamma > 0` such that, for every complex orthogonal rank-`d` projector `P`, every `b in C^N`, and every real `r in [r0,r1]`,

    Pr(||CN(0,P)-b||_infinity <= r)
        <= (1-exp(-N r^2/d))^d - gamma.                 (1.1)

The convention throughout is proper complex Gaussian: `CN(0,I_d)` has density `pi^(-d) exp(-||g||_2^2)`, and `E|g_j|^2=1`. Norm constraints use complex moduli, not separate real and imaginary coordinate constraints.

This is an explicit effective-compactness certificate, not a practical optimizer or a useful closed-form gap rate. It specifies finite rational grids, exact acceptance tests, rigorous integration, rational rounding, a positive stopping test, and a proof of termination for every admissible input. A very large gap-dependent work bound is given in Section 8. No numerical execution of the full search is claimed.

The only inherited mathematical dependencies are the accepted centering, ambient-envelope equality, and compactness results described in the task. Their source is Sections 1, 4, and 5 of:

- https://github.com/AgentSlop-Si/research/blob/dc3fdc543c9688dfed3afb5c58797d8655c3db9d/math/finalized/2026-10-19-cyclic-mixedprime-gaussian-extrema/gaussian/candidate/REPORT.md

The current scope boundary is:

- https://github.com/AgentSlop-Si/research/blob/e6ff6681109d94ffe21248f92a5a0823d6b71cf4/math/finalized/2026-10-20-alg036-gaussian/README.md

In particular, set

    F(P,r) = Pr(||CN(0,P)||_infinity <= r),
    U(r) = (1-exp(-N r^2/d))^d,
    Delta = min_{rank P=d, r0<=r<=r1} [U(r)-F(P,r)].     (1.2)

The inherited results imply `Delta > 0` and `F_r(P,b) <= F(P,r)`. They are not reproved here. The value of `Delta` is not an input to the algorithm. Translations are eliminated before any continuity argument: no joint continuity in arbitrary translations at zero-leverage rows is asserted.

This closes exactly the computable positive compact-interval gap gate, conditional on the stated accepted dependencies and acceptance of this proof. It does not settle general maximizers, changing-dimension critical-window rates, efficiency, adaptivity, information models, block-local constructions, historical novelty, or complete attribution. ALG-036 remains TO RESEARCH, priority 34; the already closed `N=3,d=2` optimizer is not rerun.

## 2. A uniform boundary estimate including zero leverage

If `X ~ CN(0,p)` and `p>0`, the density of `|X|` at `t>0` is

    f_p(t) = (2t/p) exp(-t^2/p)
           = (2/t) (t^2/p) exp(-t^2/p)
           <= 2/(e t).

Consequently, for `s>=r0` and `0<h<=r0/2`,

    Pr(s-h <= |X| <= s+h) <= 8h/r0.                   (2.1)

Indeed, throughout the interval `t>=r0/2`, its density is at most `4/(e r0) <= 4/r0`, and the interval length is `2h`. If `p=0`, `X=0` almost surely, so the probability in (2.1) is zero. The same inequality holds without a positive lower bound on `p`.

For any centered complex Gaussian vector `Z` whose coordinate variances can be zero, a union bound gives

    Pr(s-h <= ||Z||_infinity <= s+h) <= 8Nh/r0,        (2.2)

provided its coordinates are proper complex Gaussian (possibly degenerate). Independence among the coordinates is not required. For positive `s-h`, any relevant boundary atom is absent, so the choice of strict versus non-strict annulus endpoints makes no difference.

Let `P,Q` be orthogonal projectors and `||P-Q||_op<=eta`. Couple them as `PG,QG`, where `G~CN(0,I_N)`. For an integer `T>=1`, on the event that every `|G_j|<=T`,

    ||(P-Q)G||_infinity <= eta ||G||_2 <= eta N T.

The complementary event has probability at most

    N exp(-T^2) <= N 2^(-T),                          (2.3)

because `T^2 >= T log 2`. If `eta N T <= r0/2`, (2.2) therefore gives, uniformly for `s>=r0`,

    |F(P,s)-F(Q,s)|
        <= omega(eta,T)
        := N 2^(-T) + 8N^2 T eta/r0.                 (2.4)

For completeness, a joint centered modulus follows in exactly the same coupling: for `r,s>=r0` and `eta N T+|r-s|<=r0/2`, the right side is

    N 2^(-T) + (8N/r0)(eta N T+|r-s|).               (2.5)

The algorithm below needs only (2.4), using monotonicity in the radius separately.

## 3. An explicitly enumerable rational projector net

Fix rational `0<eta<=1/4`, and put

    K = ceil(4Nd/eta).

Enumerate every complex `N`-by-`d` matrix `W` whose real and imaginary entries lie in

    {-1,-1+1/K,...,1-1/K,1}.

There are exactly `(2K+1)^(2Nd)` such matrices. Form the Hermitian rational matrix `A=W*W`. Retain `W` exactly when both

    A-(1/4)I_d  and  4I_d-A

are positive definite. This is a finite exact rational test: for each matrix, all leading principal minors must be positive, by the Hermitian Sylvester criterion. Thus every retained matrix satisfies

    (1/4)I_d < A < 4I_d.                              (3.1)

Associate the exact rational projector

    Q_W = W A^(-1) W*.                               (3.2)

It is Hermitian, idempotent, and has rank `d`. The inverse and all entries in (3.2) are computable by rational arithmetic. Duplicate projectors may be retained without harm.

These projectors form an operator-norm `eta`-net of all rank-`d` orthogonal projectors. To prove this, take `P=VV*`, `V*V=I_d`, and round every real and imaginary entry of `V` to the nearest grid point. This is possible in `[-1,1]` because each entry of an isometry has modulus at most one. For the resulting `W`,

    e := ||W-V||_F
       <= sqrt(2Nd)/(2K) <= Nd/K <= eta/4 <= 1/16.

Every singular value of `W` is in `[1-e,1+e]`, so (3.1) holds strictly and this `W` is retained. In the polar decomposition, let `S=W(W*W)^(-1/2)`. Then `S*S=I_d`, and the singular value bounds give `||S-W||_op<=e`. Hence `||S-V||_op<=2e`, and

    ||Q_W-P||_op = ||SS*-VV*||_op
                 <= 2||S-V||_op <= 4e <= eta.        (3.3)

The polar factor is used only in the coverage proof. It is not computed by the algorithm. In particular, no irrational representative, feasibility oracle, or unproved effective description of the Grassmannian is needed.

## 4. Rational certified integration in real dimension 2d

Input to this subroutine is a retained rational matrix `W`, a rational radius `s>=r0`, and rational accuracy `0<epsilon<=1`. It returns rational numbers `l_F,u_F` such that

    l_F <= F(Q_W,s) <= u_F,     u_F-l_F <= epsilon.    (4.1)

### 4.1 The correct nonsingular integral

Write `A=W*W` and `D=det A`. Let `Y~CN(0,A^(-1))`. Its density on `C^d`, identified with `R^(2d)`, is

    f(y) = D pi^(-d) exp(-y*Ay).                      (4.2)

Then `WY~CN(0,Q_W)`, including when some rows of `W` are zero. Thus

    F(Q_W,s) = integral 1_{H(y)<=s} f(y) dy,
    H(y) = max_j |(Wy)_j|.                           (4.3)

By (3.1), `||W||_op<2`, so `H` is `2`-Lipschitz in the Euclidean norm. The realification of `A` has the same spectral bounds as `A`. With `q=y*Ay` and `D<=4^d`,

    ||grad f(y)||
        = 2||Ay|| D pi^(-d) exp(-q)
        <= 4 sqrt(q) 4^d exp(-q)
        <= L := 4^(d+1).                             (4.4)

Here `||Ay||<=sqrt(lambda_max(A))sqrt(q)<=2sqrt(q)` and `sqrt(q) exp(-q)<=1` for all `q>=0`. This is a global Lipschitz bound, not one depending on the integration box.

### 4.2 Tail and explicit mesh

Choose the least integer `m>=1` satisfying

    d 2^(-m) <= epsilon/4.

Set

    B=2m,           V_box=(2B)^(2d),
    tau=epsilon/(4 V_box),
    h_max=min{r0/(8d), epsilon r0/(128Nd),
              epsilon/(8 L d V_box)},
    M=ceil(2B/h_max),        h=2B/M.

All these quantities are rational or integer and positive. Divide the real cube `[-B,B]^(2d)` into `M^(2d)` cells of side `h`, using their rational centers `c`. Boundaries between cells may be assigned arbitrarily because they have zero `Y`-probability.

Every diagonal entry of `A^(-1)` is at most `4`. Leaving this real cube implies `|Y_j|>B` for at least one complex coordinate. Therefore

    Pr(Y outside cube)
        <= d exp(-B^2/4)
        = d exp(-m^2) <= d 2^(-m) <= epsilon/4.       (4.5)

Write `t_tail=d 2^(-m)` for this rational bound.

### 4.3 Cell classification and scalar rounding

A point of a cell is at Euclidean distance at most `sqrt(2d)h/2 <= d h` from its center. Set `rho=2d h`. By the choice of mesh, `2rho<=r0/2`, in particular `s-rho>0`.

Classify a cell as follows, using only exact comparisons of rational squared moduli:

- IN if every `|(Wc)_j|^2 <= (s-rho)^2`.
- OUT if at least one `|(Wc)_j|^2 > (s+rho)^2`.
- UNCERTAIN otherwise.

Every IN cell lies in `{H<=s}`. Every OUT cell is disjoint from `{H<=s}`. On an UNCERTAIN cell,

    s-2rho < H(y) <= s+2rho.

Under (4.2), `WY~CN(0,Q_W)`. Applying (2.2) with annulus half-width `2rho`,

    Pr(Y in the union of UNCERTAIN cells)
        <= 16N rho/r0 = 32Nd h/r0 <= epsilon/4.       (4.6)

For each center, compute rational `a_c,b_c` with

    0 <= a_c <= f(c) <= b_c,       b_c-a_c <= tau.

Section 5 gives an elementary terminating interval algorithm for this operation. Define

    l_c=max{0,a_c-Ldh},       u_c=b_c+Ldh.

By (4.4), `l_c<=f(y)<=u_c` throughout the cell, and

    u_c-l_c <= tau+2Ldh.                              (4.7)

Return the enclosure obtained from

    l_F = sum_{IN cells} l_c h^(2d),
    u_F = t_tail + sum_{IN or UNCERTAIN cells} u_c h^(2d),

after intersecting it with `[0,1]`. The intersection is nonempty because it contains the true probability.

The upper-minus-lower width before clamping is at most

    t_tail
    + Pr(Y in UNCERTAIN cells)
    + V_box(tau+2Ldh)
    <= epsilon/4 + epsilon/4 + epsilon/4 + epsilon/4
    = epsilon.                                       (4.8)

For the third term, subtract the exact cell integral on UNCERTAIN cells and use (4.7); on IN cells use (4.7) directly. OUT cells contribute nothing to either bound. This proves (4.1) with explicit tail, boundary, mesh, and rounding errors, including zero-leverage coordinates.

## 5. Fully rational enclosures of the elementary constants

No floating-point library is a correctness oracle. The following ordinary rational series suffice.

For `q>=0` rational, enclose `exp(-q)` by reciprocating positive enclosures of `exp(q)`. If

    S_n=sum_{j=0}^n q^j/j!,

and `n+2>=2q`, ratios between successive omitted terms are at most `1/2`. Thus

    S_n <= exp(q) <= S_n+2q^(n+1)/(n+1)!,
    1/(S_n+2q^(n+1)/(n+1)!) <= exp(-q) <= 1/S_n.      (5.1)

The interval widths tend to zero. The case `q=0` can be handled exactly. For `pi`, use Machin's identity

    pi = 16 arctan(1/5) - 4 arctan(1/239),

and alternating rational partial sums for `arctan x`. Their next terms bound the remainder. Taking enough terms gives any requested positive rational enclosure of `pi`, with lower endpoint greater than one.

Multiply positive intervals, invert positive intervals in reverse endpoint order, and take integer powers using rational arithmetic. As all constituent intervals shrink, the resulting interval for

    D pi^(-d) exp(-c*Ac)

shrinks to its value. Increase series lengths until its width is at most `tau`. This is a terminating rational stopping test and supplies the interval used in Section 4.

The same method, using (5.1) at `q=N a^2/d`, gives a rational enclosure `[l_U(a),u_U(a)]` of `U(a)` of width at most any prescribed positive rational `epsilon`. Intersect intermediate probability-valued intervals with `[0,1]` if desired. Every rounding operation is outward by construction.

## 6. The complete algorithm

Validate that `N,d` are positive integers, `d<=N`, `d` does not divide `N`, and the rational endpoints satisfy `0<r0<=r1`. Reject inadmissible inputs rather than making a strict-gap claim for them.

For `k=1,2,3,...` perform the following finite stage.

1. Set `epsilon=2^(-k)`. Choose the least integer `T>=1` such that `N 2^(-T)<=epsilon`. Set

       eta=min{1/4, epsilon r0/(8N^2 T)},
       omega=N 2^(-T)+8N^2 T eta/r0.

   Then `omega<=2epsilon`, and `eta N T<=epsilon r0/(8N)<=r0/2`, so (2.4) applies.

2. Enumerate the retained matrices `W` from Section 3 with this `eta`.

3. If `r1>r0`, set

       theta=epsilon/(2N r1),
       J=max{1,ceil((r1-r0)/theta)},
       a_i=r0+i(r1-r0)/J,        b_i=a_(i+1),
       i=0,...,J-1.

   If `r1=r0`, use just one degenerate interval `a_0=b_0=r0` and set `J=1`.

4. For every interval and every retained `W`, compute the Section 4 enclosure of `F(Q_W,b_i)` with width at most `epsilon`. Independently compute the Section 5 enclosure of `U(a_i)` with width at most `epsilon`. Put

       gamma_k=min_{W,i} [l_U(a_i)-u_F(Q_W,b_i)]-omega. (6.1)

5. If `gamma_k>0`, return the rational number `gamma=gamma_k` and stop. Otherwise proceed to stage `k+1`.

All enumerations, retained-matrix tests, classifications, scalar comparisons, sums, minima, and the stopping comparison are finite exact rational operations. Each stage has at least one retained matrix, for example the coordinate isometry with the first `d` rows equal to `I_d` and the other rows zero.

## 7. Soundness and strict termination

### 7.1 Every positive returned value is valid

Take any rank-`d` orthogonal projector `P` and `r in [r0,r1]`. By (3.3), choose a retained `W` with `||P-Q_W||_op<=eta`. Choose an interval `[a_i,b_i]` containing `r`. The envelope and centered event probability are nondecreasing in the radius. Therefore

    U(r)-F(P,r)
        >= U(a_i)-F(P,b_i)
        >= U(a_i)-F(Q_W,b_i)-omega
        >= l_U(a_i)-u_F(Q_W,b_i)-omega
        >= gamma_k.                                  (7.1)

This proves (1.1) whenever the algorithm returns, using inherited centering for every translation `b`. It also shows that every finite-stage lower bound is sound even before it becomes positive.

### 7.2 The search must return

On the radius interval,

    0<=U'(r)
      =2N r exp(-N r^2/d)(1-exp(-N r^2/d))^(d-1)
      <=2N r1.                                       (7.2)

Thus `U(b_i)-U(a_i)<=epsilon`; this is also true for the degenerate interval. Each retained `Q_W` is an actual rank-`d` projector, so (1.2) gives

    U(b_i)-F(Q_W,b_i)>=Delta.

The two scalar probability enclosures have width at most `epsilon`, and `omega<=2epsilon`. Consequently every summand in (6.1), after subtracting `omega`, is at least

    Delta - epsilon - epsilon - epsilon - 2epsilon
        = Delta-5epsilon.                            (7.3)

Hence

    gamma_k >= Delta-5*2^(-k).

Since the inherited theorem supplies `Delta>0`, any stage with `2^(-k)<Delta/5` returns a positive rational number. The algorithm does not need to know `Delta`, a bound on it, or a maximizing projector. This establishes termination for all admissible `N,d,r0,r1`, not just a fixed small-dimensional case.

## 8. Explicit cost characterization and practical limitations

At stage accuracy `epsilon`, Section 6 uses

    T=min{integer t>=1: N2^(-t)<=epsilon},
    K=ceil(4Nd/eta),
    at most (2K+1)^(2Nd) candidate frame matrices,
    J<=1+2N r1(r1-r0)/epsilon

for a nondegenerate radius interval; for a point interval `J=1`. The integrator uses the explicit `m,B,V_box,L,h_max,M` of Section 4 and `M^(2d)` cells per probability evaluation. A crude bound on the number of processed integration cells is therefore

    (2K+1)^(2Nd) * J * M^(2d).                        (8.1)

Each cell needs finitely many rational operations on the quadratic form and `N` complex linear forms, plus the certified scalar series. Rejected matrices need only the finite exact definiteness tests. Repeated projectors, repeated endpoint enclosures, and shared values may be cached, but no such optimization is needed for correctness.

For fixed `N,d,r0,r1`, as `epsilon` tends to zero,

    K=O(epsilon^(-1) log(1/epsilon)),
    J=O(epsilon^(-1)),
    M=O(epsilon^(-1) [log(1/epsilon)]^(2d+1)).

Thus the cell-count bound is

    O_tilde(epsilon^(-(2Nd+2d+1))),                   (8.2)

where the suppressed powers of logarithms and constants depend on the fixed input parameters. The exponent loses the final `+1` when `r0=r1`. The quadratic arguments in the integration exponentials satisfy `q<=8d B^2`. For fixed numeric inputs, individual scalar series evaluations and individual quadratic or linear form evaluations can use polynomial-in-`log(1/epsilon)` bit work as accuracy increases. This is not a bound for the full rational accumulation: summing independently denominated cell bounds can grow accumulator denominators substantially. Neither (8.2) nor the gap-dependent expression below bounds accumulator growth or full bit runtime. No uniform polynomial bit-complexity in the encoded inputs `N,d,r0,r1` is claimed. Bound (8.2) is an explicit cell-count characterization, not a claim of efficient numerical implementation.

By (7.3), the dyadic search stops by an accuracy smaller than `Delta/5`. Accordingly (8.1), or at fixed inputs an enormous gap-dependent bound of order `O_tilde(Delta^(-(2Nd+2d+1)))`, bounds its cell work. This is not an input-only quantitative lower bound on `Delta`; `Delta` itself may be extremely small and no useful dimensional or endpoint rate is obtained. The net is highly redundant, the quadrature is deliberately crude, and no feasible runtime is promised.

The named computability gate is genuinely closed by a terminating rational output algorithm. If the intended gate instead means a practically evaluable bound or a nontrivial analytic rate as `N,d` or the radius interval vary, this result does not close that stronger gate. Those distinctions must be retained in any catalogue annotation.

## 9. Reproducibility and disposition

The proof and pseudocode specify the entire algorithm; no historical or supplied program is invoked. This candidate does not claim an executed full-search numerical certificate, an identified optimizer, or independent acceptance before the separate review. The rational identities, Gaussian normalization, global density gradient, annulus estimate, finite coverage, quadrature error budget, and positive stopping argument are individually auditable.

No external write, repository commit, sheet edit, or publication was performed in preparing this candidate. The scope remains the all-size, fixed-input computability certificate above. The parent ALG-036 disposition and priority remain unchanged.
