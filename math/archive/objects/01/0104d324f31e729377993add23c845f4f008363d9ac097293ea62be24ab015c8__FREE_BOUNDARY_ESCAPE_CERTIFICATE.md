# Free-boundary escape: exact cancellation, overlapping-cut costs, and a depathing cut

## Result and scope

The predecessor's free-map identity is correct. This pass independently proves and checks it, then sharpens the stopping boundary in three directions:

1. On every remaining free output, the entire forced term is exactly the predecessor's cheap correction. In fact only one of the first b retained coefficients contributes to each such output. Sharing the free and forced circuits can remove this correction, but it leaves precisely the original partial Fourier transform; no information from the late source or inverse reaches these rows.
2. A family of suffix-pattern cuts that covers every output must contain at least the binary necklace number of length b. Repeating the predecessor's paid retained-inverse schedule separately for those cuts costs at least N(n-b)(n-b+1)/(2b) small-state visits. At b approximately 2 log2 n this is Omega(N n^2/log n), even before source and recovery costs. A weaker union-bound certificate already forces Omega(N n) for the same independent schedule.
3. A different, explicit retained language really can make the free block nilpotent at the FFT horizon. It has O(N log n/n) retained coordinates. However, its retained operator is not the predecessor's suffix-zero compressed operator. The existing paid construction still costs O(Nn), and no cheap inverse/source circuit for this new language is supplied.

This is a precise failed-route certificate with a constructive combinatorial cut, not a faster complete FFT and not an unrestricted arithmetic lower bound. Every predecessor file remains unchanged. The new checker imports no predecessor/uploaded executable.

## 1. Notation

Let N=2^n, 1<=b<=n, d=n-b, r=2^d, and omega a supplied primitive Nth root in a field K. The characteristic of K is necessarily different from two. In particular omega is nonzero, its N powers are distinct, and the Fourier matrix is invertible. The exact finite controls use K=GF(65537) with checked primitive roots for N<=128. Set

    Q e_s = e_(2s mod N) + omega^s e_(2s+1 mod N),
    R = {2^b j : 0<=j<r}, E = R complement,
    A = {n-bit words with no occurrence of 0^b},
    B = E Q_EE^n E^T.

All bit words include leading zeros when their fixed length is specified. Write gamma(0)=0, gamma(2a)=gamma(a), gamma(2a+1)=gamma(a)+a. The unique length-n path from source s to terminal word w has scalar

    omega^(s rev_n(w)+gamma(w)).                         (1)

The path uniqueness is special to the length-n horizon: the n appended bits are exactly w. Define eta=omega^(2^b), Q_r analogously, and

    (u_c)_j = sum_(h=0)^(2^c-1) x_(2^(b-c)(j+h r)),
    q_c = Q_r^d u_c,                    0<=c<b.          (2)

For w in A put c=n-bit_length(w), a=floor(w/2^(b-c)), and

    (C x)_w = omega^gamma(w) eta^(-gamma(a)) (q_c)_a.    (3)

Put (Cx)_w=0 for w outside A.

## 2. Independent proof of the predecessor's identity

For a terminal word w containing 0^b, its path visits R when that occurrence has finished, independent of the source. Thus the free row B_w is zero.

If w avoids 0^b, it begins with c zeros, where 0<=c<b. After the first one, no retained visit is possible: a future visit would require an internal run of b zeros. Before that first one, a visit at one of times 0,...,c occurs exactly when the initial state s is divisible by 2^(b-c). These divisibility classes are nested, so their union is the largest one, not a sum with duplicated sources.

Therefore, for w in A,

    (Bx)_w = omega^gamma(w)
              sum_(s not divisible by 2^(b-c))
                  x_s omega^(s rev_n(w)).             (4)

For the excluded sources write s=2^(b-c)j. Because w begins with c zeros,

    rev_n(w) = 2^c rev_(n-c)(w).

Their source phase becomes eta^(j rev_(n-c)(w)). It is periodic in j modulo r, giving precisely u_c. The frequency modulo r depends on the leading d bits

    a = floor(w/2^(b-c)),
    rev_(n-c)(w) = rev_d(a) mod r.

Thus the excluded sum is (3), by the length-d path identity for Q_r. This proves the all-input operator equality

    B = M_A Q^n - C.                                  (5)

It also checks the edge cases d=0, r=1, c=b-1, and b=1. The correction costs O(N+brd): N-r fold visits, b length-r trajectories of d paid sparse stages, and O(N) phase/mask/output work. At b=ceil(2 log2 n)<=n it is O(N).

## 3. Exact shared-computation boundary

Let

    G_L = Q_EE^(L-1) Q_ER,  L>=1,
    H_n(v) = sum_(j=0)^(n-1) G_(n-j) v_j.

The next statement holds for an arbitrary supplied retained polynomial v, with no assumption that it solves a Schur system.

### Single-coefficient selection theorem

For each w in A, with c=n-bit_length(w),

    (H_n(v))_w = (G_(n-c) v_c)_w,                    (6)
    (G_(n-j))_(w, :) = 0 for j != c.                 (7)

Proof for j>=b: a retained state at time j has b low zero bits; because j>=b, those bits occur entirely among the first j appended bits of terminal word w. This would place 0^b in w. Hence it is impossible.

For j<b, n-j>d. Every length-(n-j) path from R has lost all retained source bits at the terminal coordinate, so the terminal word is exactly the appended word, padded with j leading zeros. Its first edge must be one to leave R. Thus its first one occurs exactly at position j+1, forcing j=c. This proves (6)-(7), including all short-trajectory cases without assuming an invertible coordinate route.

Now take the actual retained solution

    v_j = (Q^j x)_R.

For 0<=c<b, any path ending in R at time c must append c zeros: an appended one would still be among the terminal b low bits. All these zero edges have weight one, and their source fibers give

    v_c = u_c.                                       (8)

Applying the predecessor's long-path recovery formula to (6) gives (3). Consequently

    M_A H_n(v_actual) = C x.                          (9)

The reconstructed free rows are therefore identically

    M_A(Bx + H_n(v_actual))
      = M_A Q^n x - Cx + Cx
      = M_A Q^n x.                                   (10)

This is stronger than saying that free recovery is almost a Fourier transform. It identifies exactly which shared work is duplicated and removable. On A, every retained coefficient of degree >=b is annihilated; calculating the difficult later source and running the retained inverse cannot improve these output rows through this recovery map. The cheap early folds restore precisely what elimination deleted.

This does not prohibit a new joint circuit that evaluates the partial Fourier transform directly. It prohibits claiming such a circuit merely by sharing the already derived boundary pieces.

## 4. Overlapping suffix-pattern cuts: a quantitative certificate

For a fixed b-bit pattern p let

    R_p = {s : the b low bits of s equal p},
    A_p = {n-bit words avoiding p}.

For any output w in A_p, a retained visit at time j>=b is impossible. Indeed the b-bit suffix of the state at time j is the substring of w ending at j. Hence

    M_(A_p) G_(n-j)^(p) = 0,  j>=b.                  (11)

Unlike (3), no cheap formula for the early correction for an arbitrary p is assumed here. Equation (11) is just the exact path constraint.

Consider the proposed escape that chooses a set P of patterns and assigns each output to a cut whose pattern occurs in that output. This avoids asking that cut for its free rows. P must hit every n-bit word.

### Counting bound

A pattern can occur at n-b+1=d+1 positions and covers at most (d+1)r outputs. Thus

    |P| (d+1) r >= N.                               (12)

The predecessor's explicit generic retained inverse performs exactly

    T_b = r d(d+1)/2                                (13)

small-state visits in its feedback trajectories. Repeating that schedule independently for each cut would pay

    |P| T_b >= N d/2.                               (14)

This is already Omega(Nn) when b=O(log n), before any source, retained coefficient I/O, or output costs. It grants, favorably, an unproved extension of the same per-cut circuit to every pattern; therefore merely establishing that extension would not close the FFT.

### Stronger necklace bound

Partition b-bit patterns into rotation classes. If P misses one entire class, repeat a word in that class periodically and take its first n bits. Every b-window belongs to that missed class, so this output is not covered. Therefore

    |P| >= Z_b = (1/b) sum_(k=0)^(b-1) 2^gcd(b,k)
                 >= 2^b/b.                          (15)

Combining (13)-(15) yields

    |P| T_b >= N d(d+1)/(2b).                       (16)

At b=ceil(2 log2 n) this is Omega(N n^2/log n). This bound counts the displayed additive schedule, not an inherent arithmetic cost of the transforms. Sharing across cuts, using only selected coefficients, changing the retained inverse, time-dependent cuts, or using a different language requires a separate algorithm and paid schedule; none is ruled out by (16).

The rotation-class argument is proved above, independently of literature. It is the usual necklace lower bound for unavoidable words/decycling sets. Mykkeltveit's original paper proves existence of minimum decycling sets of necklace cardinality, but that result alone gives neither our required horizon nor a weighted Fourier circuit: [A proof of Golomb's conjecture for the de Bruijn graph](https://www.sciencedirect.com/science/article/pii/0095895672900068).

A particularly tempting shortcut is false: retaining the lexicographically smallest representative of every necklace need not even break all cycles. At b=3 those representatives are {000,001,011,111}; the cycle 010 -> 101 -> 010 avoids all of them.

## 5. What every coordinate cut must pay structurally

The following statements apply to an arbitrary coordinate set T, with no suffix-language assumption. Let t=|T|, F its complement, and B_T the full-N embedding of Q_FF^n.

Partition all length-n paths by their last visit to T, including time 0 or time n. This gives exactly

    Q^n = B_T + P_T Q^n
                + sum_(j=0)^(n-1) G_(n-j)^(T) (Q^j)_T.  (20)

There are n+1 correction terms, each factoring through t coordinates. Since Q^n is an invertible diagonally scaled/permuted Fourier matrix,

    rank B_T >= N-(n+1)t.                            (21)

No cost is inferred from rank. It only rules out encoding the arbitrary-input free vector through a smaller linear summary, including for a changed retained language.

There is also a stronger structural restriction if the proposal is to make the free operator zero. Partition the N states into their n-bit rotation classes. Each class is a directed cycle of Q: append the first bit of the current word to rotate it. If T misses a class, the surviving cycle has a length-n walk. At the exact horizon n, the path between a given starting state and terminal state is unique and its weight is nonzero, so this walk cannot cancel against another path. Consequently

    Q_FF^n = 0  implies  |T| >= Z_n >= N/n.          (22)

Equation (22) is the classical necklace lower bound for a feedback vertex set (decycling set) of the binary de Bruijn graph; it is not claimed as a new combinatorial result. Mykkeltveit's theorem attains Z_n for cycle removal. Our desired Q_FF^n=0 is stronger: the remaining graph must have no length-n path, rather than merely no directed cycle. The weighted conclusion here is justified separately by uniqueness of the source-to-target length-n path and its nonzero product of powers of omega. It does not invoke positivity, numerical conditioning, or an assumption that arbitrary sums of paths cannot cancel. See [Mykkeltveit's original paper](https://www.sciencedirect.com/science/article/pii/0095895672900068).

Thus no coordinate language of the old retained size approximately N/n^2 can eliminate the free term altogether. The marker cut below is within a logarithmic factor of this structural lower bound. Equations (21)-(22) do not rule out a cheaper high-rank free operator or a different arithmetic representation.

## 6. Another retained language that really kills the free block

There is a constructive way to remove the free term, but it does not preserve the compressed inverse invariant. Define

    R* = R union A,
    E* = complement of R*.

Then

    (Q_(E*,E*))^n = 0.                              (23)

Proof: consider any length-n path and its terminal n-bit word w. If w avoids 0^b then w belongs to A and the terminal state is retained. Otherwise, when an occurrence of 0^b finishes, the path hits R. No length-n path remains in E* throughout. The conclusion is structural and valid for every choice of edge weights.

### Size and generation cost

Let a_b(k) count k-bit words avoiding 0^b. For k<b it equals 2^k; for k>=b it satisfies

    a_b(k) = sum_(j=1)^b a_b(k-j).

Put rho=2-2^(-b). Since

    sum_(j=1)^b rho^(-j) < 1,

and 2^k <= 2 rho^k for 0<=k<b, induction gives

    a_b(n) <= 2 rho^n
             <= 2N exp(-n/2^(b+1)).                 (24)

For completeness, the first inequality on the geometric sum is equivalent, when b>1, to

    (2-rho)rho^b = (1-2^(-b-1))^b < 1;

b=1 is immediate. The base-case bound follows from Bernoulli's inequality, since (1-2^(-b-1))^(b-1)>=1-(b-1)2^(-b-1)>=1/2.

For sufficiently large n, choose

    b = floor(log2(n/(4 ln n))).

Then

    r < 8N ln n/n,
    |A| <= 2N/n^2,
    |R*| = r+|A| = O(N log n/n).                    (25)

R and A are disjoint, because a word ending in b zeros cannot avoid b zeros. Binary-parent zero-run tables identify R* in O(N) charged integer/address work and O(N) storage. More compact enumeration is unnecessary to the stated bound.

This is a genuine horizon depathing cut. It is a close relative of marker-based universal hitting sets, but (23)-(25) are self-contained. For related primary literature, Zheng, Kingsford, and Marcais prove small depathing sets and show that Mykkeltveit sets can have remaining paths between quadratic and cubic in word length: [Lower Density Selection Schemes via Small Universal Hitting Sets with Short Remaining Path Length](https://pmc.ncbi.nlm.nih.gov/articles/PMC8066347/). In particular, a minimum decycling theorem cannot be silently substituted for an n-step nilpotence theorem.

### Why this still does not close the arithmetic construction

The predecessor's compressed state is a quotient of the single suffix-zero cylinder. Adding A changes both retained coordinates and all first-return languages; it does not produce a stationary size-|R*| Fourier trajectory by the earlier proof. No formula analogous to K_(b+t)=C_t Q_r^t has been established for R*.

A fully charged reference algorithm propagates the sparse full-N state for n stages, costing O(Nn), and reads off all desired retained/source/output values. Nilpotence can truncate a formal inverse; it does not reduce those stages' arithmetic work by itself. Retaining A moves the formerly free almost-Fourier rows into the retained unknown rather than evaluating them. Claiming O(|R*|n), O(N), or a recursively smaller Fourier primitive for the new Schur solve would therefore be an unproved additional result.

This explicitly identifies the next meaningful escape target: derive an all-input weighted compression for the new marker language, including fresh source and recovery, with a circuit paid below Nn. The current work does not provide that circuit.

## 7. Independent controls, files, and replay

The standard-library-only checker was authored in this pass. It implements Q directly, kills retained coordinates after each step for the free/forced oracles, and computes the folded correction separately. It imports or executes no predecessor code.

Run:

    python verify_free_boundary_escape.py

Over GF(65537), every b for N=2,4,8,16,32,64,128 is checked, with exact-order root tests:

- 1,538 global basis inputs verify the predecessor identity (5), and independently check the exact Fourier phases (1).
- The same 1,538 basis inputs verify every early fold (8), forced cancellation (9), and the new nilpotence claim (23).
- 1,510 retained-basis coefficient cases verify the single-coefficient selection rule (7).
- 444 general-pattern late-coefficient cases verify (11).
- Exhaustive enumeration of 329,060 pattern sets over 20 (b,n) choices verifies the coverage bound, necklace necessity, and minimum cover sizes.
- All 65,812 coordinate cuts through N=16 verify the necklace necessity for exact horizon nilpotence; 276 cuts through N=8 also verify the general rank bound by exact field elimination.
- The 010/101 counterexample to lex-minimum necklace representatives is explicit.
- For 32 word lengths b and 257 horizons each, exact integer arithmetic checks the recurrence and the rational majorant underlying (24); no floating-point tolerance is used.

`FREE_BOUNDARY_CONTROLS.json` contains the controls; `EXACT_RUN.log` contains the deterministic summary. `FREE_BOUNDARY_SHA256SUMS.txt` seals this pass. `PREDECESSOR_SEALS_CHECK.log` verifies the pre-existing seals without modifying them. The finite checks support the proofs; no all-size claim is inferred solely from experiments.
