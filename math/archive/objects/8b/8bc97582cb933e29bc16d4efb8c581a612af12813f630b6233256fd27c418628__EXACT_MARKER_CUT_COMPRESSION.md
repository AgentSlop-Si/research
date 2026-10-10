# Exact weighted marker-cut recurrence and a faster fresh source

## Result and stopping boundary

For the predecessor's changed retained set

    R = {2^b j : 0 <= j < r},
    A = {n-bit words avoiding 0^b},
    T = R union A, E = complement of T,
    N = 2^n, d = n-b, r = 2^d,

there is an explicit all-input weighted block Schur representation. The added avoiding states do not create arbitrary new eliminated excursions: **A has no edge to E**. Every excursion from R into E has a deterministic increasing marker age. This supplies the following bounded advance:

- The exact nilpotence index of Q_EE is d, for 1 <= b < n.
- R-to-R first-return feedback agrees with the old suffix-only operator only through degree d+1; all higher first-return coefficients are zero.
- R-to-A first-return feedback has exactly one possible degree, d+1, with an explicit weighted smaller-Fourier formula.
- The fresh source costs O(N + |T|(n+1) + N 2^b), with O(N + |T|(n+1)) storage. At the marker choice b=floor(log2(n/(4 ln n))), this is O(Nn/ln n), including all input, setup, output coefficients, and scalar weights.
- An explicit pruned causal inverse and top-recovery schedule is given below. It costs Theta(Nn) at that marker choice. This is a cost certificate for the displayed algorithm, **not a universal arithmetic lower bound**.

Thus the source bill improves on a full-size n-stage trajectory for this changed cut. The weighted inverse/recovery remains the bottleneck. This does not establish a faster complete arbitrary-input FFT.

All claims are algebraic over a field K with a supplied primitive Nth root omega. The cost model counts field additions/multiplications, separately noted inversions, and O(log N)-bit integer/address operations. It is not a bit-complexity theorem. No predecessor files or seals were changed. No predecessor or uploaded executable was imported or run.

## 1. Exact marker-age layers

Use Q e_s = e_(2s mod N) + omega^s e_(2s+1 mod N), with all n-bit words including leading zeros. For s in E, let h be the number of bits strictly after the end of its **rightmost** occurrence of 0^b. Then 1 <= h <= d. Set

    W_h = {h-bit words that start with 1 and avoid 0^b},
    E_h = {2^(b+h) j + w : 0 <= j < 2^(d-h), w in W_h},
    e_h = |E_h| = 2^(d-h) a_b(h-1),                 (1)

where a_b(k) counts k-bit words avoiding 0^b.

These are disjoint exact layers, not automaton-state approximations. Their union is E. The first bit after the rightmost marker must be 1, and the remaining suffix must avoid a new marker; these observations prove (1) in both directions.

Every E-to-E edge goes from E_h to E_(h+1). Appending a new marker instead goes to R. Once h=d, the old rightmost marker shifts out; a next state without a new marker belongs to A. An A state has no old marker, so its next state belongs either to A or to R, never E.

Consequently Q_EE^d=0. This exponent is sharp: start at state 1 in E_1 and append d-1 ones. The path remains in the layers through E_d and has nonzero weight. For a path of length <= n, the appended bits are determined by its source and target, so no second such path cancels it. Therefore Q_EE^(d-1) is nonzero, including d=1 where this is the identity on a nonempty E.

The endpoint case b=n has E empty and T all N coordinates. It needs no elimination and offers no compression; the remaining statements assume b<n.

## 2. The exact weighted block recurrence

Write v_R and v_A for retained polynomial vectors. Let

    D = Q_RR,  J = Q_RA,  H = Q_AA,
    U = Q_(E_1,R),
    L_h = Q_(E_(h+1),E_h),       1 <= h < d,
    V_h = Q_(R,E_h),
    W = Q_(A,E_d),
    F_1 = U,  F_h = L_(h-1) ... L_1 U.

All these are restrictions of the actual weighted Q. No scalar automaton transition substitutes for an n-bit coordinate. The sparse matrices D,J,H together have at most 2|T| edges; the layer maps and exits together have at most 2|E| edges.

For fresh input x, define E-layer source polynomials by

    X_1(z) = x_(E_1),
    X_h(z) = x_(E_h) + z L_(h-1) X_(h-1)(z),
                                            2 <= h <= d.       (2)

Then deg X_h <= h-1. The exact Schur source is

    f_R(z) = x_R + z sum_(h=1)^d V_h X_h(z),
    f_A(z) = x_A + z W X_d(z).                                (3)

The reduced unknowns satisfy

    v_R = f_R + z D v_R + z J v_A
                  + sum_(h=1)^d z^(h+1) V_h F_h v_R,
    v_A = f_A + z H v_A + z^(d+1) W F_d v_R.                  (4)

The eliminated solution itself is

    y_(E_h)(z) = X_h(z) + z^h F_h v_R(z).                    (5)

Equations (2)-(5) follow by substituting the layer equations, with every edge weight unchanged. They hold as formal series, not just through the FFT horizon. The smaller-Fourier representation below is only used within its proved horizon.

At degree n, every X_h term vanishes because h-1 < n. Thus there is no free top term, and

    (Q^n x)_(E_h) = F_h (v_R)_(n-h),
    (Q^n x)_T = v_n.                                         (6)

Different layers in (6) use different arbitrary retained coefficients. A short language automaton does not combine those data vectors.

## 3. Correct changed-language weighted compression

Let eta=omega^(2^b) and let Q_r have the stationary definition with root eta. Define gamma by

    gamma(0)=0, gamma(2a)=gamma(a),
    gamma(2a+1)=gamma(a)+a.

A length-t appended word k from retained source 2^b j has scalar

    eta^(j rev_t(k)) omega^gamma(k).                          (7)

For t<=d and output a of Q_r^t, the appended word is exactly k=a mod 2^t. The old size-r trajectory can therefore be used only with this explicit route and the changed first-return restriction.

### R-to-R feedback

Put kappa=max(0,d+1-b). For 1 <= t <= kappa define C_t by inspecting k=a mod 2^t; keep it only if k starts and ends with 1 and avoids 0^b, and route

    (omega/eta)^gamma(k) q_a
          to retained index 2^b(a-k)+k mod r.                (8)

Then the R-to-R first-return coefficient at length b+t is C_t Q_r^t. All other non-direct R-to-R first-return coefficients vanish:

    K_RR(z) = sum_(t=1)^kappa z^(b+t) C_t Q_r^t.              (9)

Why the changed cutoff is necessary: the initial suffix marker is still present through time d. An excursion without a new marker is therefore in E through that time. At time d+1 it enters A, unless it creates a new marker and returns to R. Hence a first return to R cannot have length >d+1. For lengths <=d+1, no intermediate state can already lie in A, so the old first-return proof applies. This is an exact justification of (9), not an unchanged reuse of the old kernel.

### R-to-A feedback

Write B=W F_d. Its only possible degree is d+1. Put q=Q_r^d u. For each (d+1)-bit word w that starts with 1 and avoids 0^b, let a=floor(w/2). The corresponding n-bit state w has b-1 leading zeros and belongs to A. Then

    (B u)_w = omega^gamma(w) eta^(-gamma(a)) q_a,             (10)

with zero values on the other A states. There is no summation over unrecorded appended words. The source frequency in (7) modulo r depends exactly on the leading d bits a. This proves (10), including all phases.

The reduced Schur matrix through degree n is consequently

    S_T(z) = [ I-zD-K_RR(z)          -zJ          ]
             [ -z^(d+1) B           I-zH         ].          (11)

The A-to-A and A-to-R blocks are explicitly sparse. Equations (9)-(11) are a true weighted retained representation for the changed language.

### Safe pruning and the data actually carried

Define p_t to equal Q_r^t u on those coordinates a whose low t bits lie in W_t, and zero elsewhere. For t<=d,

    p_0=u,  p_t = M_t Q_r p_(t-1).                           (12)

This is valid because each selected appended word has a selected prefix, and appended words have not yet merged for t<=d. It is false to apply this argument unchanged beyond d. Exactly e_t coordinates are structurally present in p_t. Formula (8) uses only p_t; formula (10) uses only p_d.

The number e_t includes both the valid word and the remaining source-prefix coordinates. Keeping only a b-state zero-run machine would discard arbitrary amplitudes and the weights omega^s. The reduction is a sparse weighted trajectory, not a collapse to b scalar states.

A sparse list with generation-stamped scratch arrays implements (12) in O(r+sum e_t) work over a trajectory: each active coordinate has two outgoing edges, invalid appended words are rejected, duplicate values are added, and only touched output entries are initialized. Since e_(t-1)<=2e_t for t>=2 and r=2e_1, charging both input and output lists changes only a constant factor. Dense length-r reinitialization at every step is not assumed free. Routing and every merge in (8) are also charged.

## 4. Fully paid source preparation

Let m=|T| and

    M_b(n) = sum_(h=1)^d h e_h.                              (13)

Prepare the N omega powers consecutively, and prepare state membership, rightmost-marker age, layer lists, and coordinate indices in O(N+n) field/address work and O(N+n) words. One concrete O(N) membership construction uses the binary-parent recurrence for the longest zero run and trailing-zero count. For a fixed-length n-bit word, its leading-zero prefix is handled using its bit length; the all-zero state is handled separately. The rightmost occurrence can similarly be maintained on significant-bit prefixes and, if there is no internal occurrence, obtained from the leading-zero prefix. No scan of n bits per state is needed. Equivalently, an n-step binary trie enumeration carries the current trailing run and rightmost occurrence; the entire binary trie has fewer than 2N nodes.

For the weighted compressed routes, obtain eta by b repeated squarings and charge one scalar inversion of eta. Consecutive power tables for omega, eta, eta^(-1), and omega/eta, followed by gamma(2a)=gamma(a) and gamma(2a+1)=gamma(a)+a in multiplicative form, prepare every phase in (8), (10), and (20) in O(N+n) field/address work. No per-edge exponentiation or uncharged root bank is needed; the scalar inversion is separate in a bit-complexity model.

Read all N input entries. Initialize the dense retained source jet, paying m(n+1) writes. Process (2) in increasing h. Each E_h state carries h scalar coefficients. Sending that polynomial along at most two outgoing weighted edges, either to the next layer or into (3), costs O(h) scalar/address work. In particular coefficient shifts by z are address offsets, while each nonzero edge multiplication and addition is paid. Initializing every layer polynomial is included. This yields

    source work = O(N + m(n+1) + M_b(n)).                    (14)

Only adjacent layer polynomials are needed simultaneously. Using the predecessor's elementary bound a_b(k)<=2(2-2^(-b))^k, put q=1-2^(-b-1). Equation (1) gives e_h<=r q^(h-1), and

    h e_h <= r/(1-q) = 2N.

Thus source storage is O(N+m(n+1)), including the input, output jet, weighted tables, lists, and two live layer polynomials. Storing all layer polynomials simultaneously is unnecessary.

### Exact moment bound

The avoiding-word generating function is

    A_b(z) = sum_(k>=0) a_b(k) z^k
           = (1+z+...+z^(b-1))/(1-z-z^2-...-z^b).            (15)

The denominator is nonzero at z=1/2, and all coefficients are nonnegative. From (1), extending the finite h-sum to infinity and differentiating (15) gives

    M_b(n)/N
       <= 2^(-b-1) [A_b(1/2) + (1/2) A_b'(1/2)]
        = 2^(b+1)-b-2.                                    (16)

This is an all-size identity/bound, not an empirical fit. It also follows from finite-state waiting-time recurrences, but none are needed here. The independent verifier checks the rational identity exactly for 64 b values; the proof is the algebraic generating-function identity.

### Marker regime and comparison

For sufficiently large n choose

    b = floor(log2(n/(4 ln n))).                            (17)

The predecessor proves r<8N ln n/n and |A|<=2N/n^2. Hence

    m=O(N ln n/n),
    M_b(n)=O(Nn/ln n),
    m(n+1)=O(N ln n),
    source work=O(Nn/ln n),
    source storage=O(N ln n).                              (18)

At this b, d=n-O(log n). A full-size d-stage source trajectory has a Theta(Nd)=Theta(Nn) state-visit bill. Equation (18) replaces that bill for the **changed marker-cut source**. It does not retroactively prove a better formula for the predecessor's different suffix-only source. The improvement is an explicit logarithmic factor in n=log2 N, while reading the arbitrary N-vector and writing the retained polynomial data remain charged.

## 5. Paid causal inverse, recovery, and its remaining cost

For arbitrary supplied f(z) through degree n, initialize residuals rho_j=f_j. In increasing j:

1. Set v_j=rho_j.
2. Apply the direct sparse block Q_TT v_j into rho_(j+1).
3. Start p_0=(v_j)_R and use (12). For each t with b+t+j<=n and t<=kappa, route C_t p_t into the R part of rho_(j+b+t).
4. If j+d+1<=n, continue through t=d and route B's formula (10) into the A part of rho_(j+d+1).

All updates are strictly to later coefficients, so induction on j proves that this solves (11). Every source coefficient, residual update, retained output, and scalar multiplication is paid.

For t in 1,...,d, step 3 needs that age for the prefix of starts j<=d-t when t<=kappa. Step 4 needs it for starts 0<=j<b. Their union therefore has exactly max(b,d-t+1) starts. The number of active trajectory-coordinate visits is

    V_inv = sum_(t=1)^d e_t max(b,d-t+1).                    (19)

The total inverse cost is O(N + m(n+1) + V_inv), including reusable setup, with O(N+m(n+1)) storage. The operation-count claim charges the structural lists even when special input values happen to vanish. There are no free polynomial products or unclosed recursive inverses.

To obtain the top E outputs as well, (6) requires F_h(v_R)_(n-h). Its explicit route from p_h is: for a with k=a mod 2^h in W_h, write

    (omega/eta)^gamma(k) (p_h)_a
          to global state 2^b(a-k)+k mod N.                 (20)

This route is injective on the selected a and lands in E_h. Extend the trajectory for each coefficient j through min(d,n-j); at t=n-j use (20). This shares the trajectories already needed by the inverse. The exact joint visit count is

    V_joint = sum_(t=1)^d e_t(n-t+1)
            = (n+1)|E| - M_b(n).                            (21)

Source preparation followed by this joint schedule gives the entire Q^n x, with final phase/reversal and N output writes costing O(N). Formula (6) explains why no free recovery call is missing.

At (17), m=o(N), |E|=N-o(N), and M_b(n)=O(Nn/ln n)=o(Nn). Therefore

    V_joint = (1-o(1))Nn = Theta(Nn).

The inverse-only schedule has the same order, because

    (d+1)|E|-M_b(n) <= V_inv <= n|E|,

and d/n tends to one. This establishes an actual Theta(Nn) visit count for this schedule, not merely a loose O(Nn) bound. It makes no claim about every circuit for S_T inverse, every joint source/solve circuit, or the Fourier transform.

The smaller retained width m=O(N ln n/n) by itself does not yield O(mn) arithmetic. Most E layers are revisited by almost n distinct retained input coefficients in the displayed online inverse. Nilpotence truncates each excursion but does not pay for those repeated weighted data trajectories.

## 6. Exact counterexample and linear-summary boundary

### The old suffix-only kernel cannot be reused unchanged

Over GF(65537), take N=16, n=4, b=2, d=2 and omega=64. From source 0000, the appended path 1100 is

    0000 -> 0001 -> 0011 -> 0110 -> 1100.

In the suffix-only cut its internal states are eliminated, so the old degree-4 first return has weight omega=64 at state 12. In the marker cut, state 0110 avoids 00 and is retained in A at time 3. Thus this is not a first return at time 4. Indeed all new first-return coefficients past d+1=3 vanish. The checker verifies old K_4 e_0=64 e_12 and new K_4 e_0=0 exactly.

### Fresh source has N independent scalar degrees of freedom

The full map x -> f(z) in (3), even restricted to degrees <=d, is injective. If f=0, the formal retained solution is v=0, since S_T(0)=I. Then y(z)=(I-zQ)^(-1)x has zero retained part and eliminated part (I-zQ_EE)^(-1)x_E, a polynomial of degree <d. Hence Q^d x=0. But Q is invertible: the two columns indexed s and s+N/2 form a 2-by-2 block with nonzero determinant -2 omega^s after arranging their common destination pair. Therefore x=0.

Consequently any factorization of this whole source map through a fixed **linear** summary requires dimension at least N. A b-state language recognizer or a single m-vector cannot carry an arbitrary fresh source. This is an information-dimension statement only; it neither prohibits a fast high-rank circuit nor turns rank into an arithmetic lower bound. Likewise an arbitrary supplied retained polynomial has m(n+1) independent coefficients, and its input/output bill cannot be omitted.

## 7. Relation to existing work and exact controls

The underlying unweighted marker/depathing context is already represented in the predecessor and in Zheng, Kingsford and Marcais, [Lower Density Selection Schemes via Small Universal Hitting Sets with Short Remaining Path Length](https://pmc.ncbi.nlm.nih.gov/articles/PMC8066347/) (Journal of Computational Biology, 2021). That paper studies the relation between hitting sets, density, and remaining path length; none of its combinatorial bounds is treated here as a weighted Fourier arithmetic theorem. No novelty claim is made for the age-layer, generating-function, or DAG-elimination techniques. The task-specific conclusions are proved directly above.

The fresh standard-library-only verifier implements Q directly, independently constructs the layers, and compares against explicitly killed full-N propagation. It does not execute earlier code. Run:

    python verify_marker_cut.py

Over GF(65537), for every 1<=b<n and 2<=n<=7, exact-order root checks and the following controls pass:

- 21 parameter sets check layer membership, every allowed edge direction, and exact visit-count identities.
- 1,284 global basis inputs check every source coefficient from the new layer recurrence against direct elimination.
- 988 retained basis inputs check every changed-language weighted feedback coefficient against direct first-return propagation.
- 21 arbitrary polynomial right sides check the complete causal inverse and top forced output.
- 21 fresh arbitrary global inputs check the assembled complete Q^n output.
- 10 full source-map rank checks through N=32 corroborate the separately proved injectivity.
- 64 exact rational generating-function controls check (16).
- The degree-4 counterexample is checked exactly.

The dense zero-filled arrays and modular exponentiation in the verifier are readable finite oracles, not the claimed production cost model. Sparse generation-stamped lists, consecutively prepared powers, binary-parent phase tables, coefficient-array storage, and the paid schedules above define that model.

`MARKER_CUT_CONTROLS.json` and `EXACT_RUN.log` are deterministic. `PREDECESSOR_SEALS_CHECK.log` records the pre-existing seal checks. `MARKER_CUT_SHA256SUMS.txt` seals this report and its controls. Finite checks support but do not replace the all-N proofs.
