# Exact compressed boundary maps and the remaining almost-complete transform

## Result

Continue the FFT-horizon Schur construction with N=2^n, b retained zero bits, r=N/2^b=2^d, and a supplied primitive Nth root omega. The following boundaries are now explicit and charged:

1. The fresh-input polynomial right side has an exact batched formula using one full-size stationary trajectory of d stages and at most b small r-state trajectories. Cost: O(N(d+1)+rbd), with all N input entries included.
2. The forced eliminated recovery, for an arbitrary supplied polynomial retained solution through degree n, costs O(N+rnd). It uses the small trajectory, then explicit suffix replication. At b=ceil(2 log2 n), this and the retained inverse both cost O(N).
3. The free eliminated top coefficient is exactly a mask of Q_N^n x minus a correction applicable in O(N+brd) work. The mask keeps A_b(n) rows, where A_b(n) counts n-bit words avoiding b zeros. At b=ceil(2 log2 n), it keeps N-O(N/n) rows, and the correction is O(N).

Thus the remaining free-term primitive is equivalent, up to the stated additive work, to this specified almost-complete partial Fourier transform. The boundary source's present full-size trajectory still costs Theta(Nn) at that b. No rank argument is used as an arithmetic lower bound, and the complete arbitrary-input FFT is not closed below N log N.

All earlier sealed files remain unchanged. This is an additional bounded result with its own exact checks.

## 1. Conventions and required maps

Use

    Q_N e_s=e_(2s mod N)+omega^s e_(2s+1 mod N),
    R={2^b j:0<=j<r},  E=R complement,
    D_E=I-z Q_EE,
    S_b=I-z A_r-z^2 Q_RE D_E^(-1)Q_ER.

For a fresh arbitrary constant N-vector x, the exact block solution is

    f(z)=x_R+z Q_RE D_E^(-1)x_E,
    v(z)=S_b(z)^(-1)f(z),
    y_E(z)=D_E^(-1)x_E+G_b(z)v(z),
    G_b(z)=z D_E^(-1)Q_ER.                           (1)

All statements below are modulo z^(n+1). Only the final coefficient y_n=Q_N^n x is required for the full transform. The earlier report gives the retained inverse on arbitrary polynomial f in O(r(n+1+d^2)+n).

Let eta=omega^(2^b), and let Q_r have the same stationary definition with root eta. Define gamma by gamma(0)=0, gamma(2a)=gamma(a), gamma(2a+1)=gamma(a)+a. Let rev_L reverse exactly L bits. A length-L path with appended word w has weight

    omega^(s rev_L(w)+gamma(w))                     (2)

from source s. The identity includes wrapped source states because omega^N=1.

## 2. Forced recovery from the retained polynomial

Write

    G_b(z)=sum_(L>=1) z^L G_L,
    G_L=Q_EE^(L-1) Q_ER.

A surviving path from R starts with one and contains no b-zero run. Its word need not end with one. Let O_(b,L) be exactly those L-bit words.

### Short paths: 1<=L<=d

For a length-r vector u, compute q_L=Q_r^L u. For each a in {0,...,r-1}, let w=a mod 2^L. If w belongs to O_(b,L), route

    (omega/eta)^gamma(w) (q_L)_a

into the global output coordinate

    y=2^b(a-w)+w mod N.                              (3)

This map is injective on the selected a. Formula (2) gives the weight and endpoint immediately: a=2^L j+w mod r becomes y=2^(b+L)j+w mod N. There is no N-dimensional frontier in this part.

### Longer paths: d<L<=n

Compute q_d=Q_r^d u once. For each word w in O_(b,L), let

    a=floor(w/2^(L-d)).

Then

    (G_L u)_w = omega^gamma(w) eta^(-gamma(a)) (q_d)_a,

and all other coordinates vanish.                         (4)

To prove (4), the endpoint has lost all source bits because b+L>=n, and therefore equals w itself. The source frequency rev_L(w) modulo r depends only on the leading d bits a, namely rev_d(a). The full length-r trajectory q_d already contains that Fourier value multiplied by eta^gamma(a). This gives the correction in (4). This proof also handles d=0: q_0=u and r=1.

Equations (3)-(4) preserve every arbitrary input amplitude and phase. They do not assume equal weights for different appended suffixes.

### Arbitrary polynomial input and charged work

For v(z)=sum_(j=0)^n z^j v_j, the required coefficient is

    [z^n]G_b(z)v(z)=sum_(j=0)^(n-1) G_(n-j) v_j.    (5)

Run the small trajectory for v_j only through min(d,n-j). Across all j the exact number of small stages is

    sum_(j=0)^n min(d,n-j)
      =d(n+1)-d(d+1)/2.                              (6)

Each stage costs O(r). For the full sparse jet, short-path routing costs the same order. The number of candidate longer words over all j and lengths is

    sum_(L=d+1)^n (n-L+1) 2^(L-1) < 2N.             (7)

The top-coefficient-only schedule needs no more work. Prepare omega powers, omega^gamma(w), and maximum zero-run data for w<N in O(N), and the eta inverse-phase table in O(r), using the binary-parent recurrences. Every suffix, rejection, phase multiplication, accumulation, and output write is charged.

Therefore forced recovery costs O(N+rnd). The desired top coefficient can accumulate directly into one initialized N-vector. A full sparse jet can instead emit degree/coordinate/value records and sort/merge them by fixed-width radix passes; its record count is O(N+rnd), rather than a mandatory dense N-by-n rectangle. No uncharged polynomial multiplication is present.

## 3. Fresh-input source: an exact batched formula

Let P_a project a global vector onto coordinates divisible by 2^a. Define b folded retained vectors, c=0,...,b-1, by

    (u_c)_j=sum_(h=0)^(2^c-1) x_(2^(b-c)(j+h r)),
    0<=j<r.                                         (8)

Their total preparation visits are sum_c 2^c r=N-r. In particular u_0=x_R. These are explicit input sums, not precomputed transforms.

### Zero-only prefix

For 1<=L<=b, first hitting R at time L must use only zero edges, and

    (f_L)_y=sum_(s: v_2(s)=b-L,
                   s/2^(b-L)=y mod r) x_s.          (9)

Route each s outside R once, at L=b-v_2(s), to obtain all these coefficients in O(N). Set f_0=x_R.

### Remaining coefficients

For t=1,...,d, compute X_t=Q_N^t x using one shared full-size trajectory. Define J_t on its output coordinate a by examining w=a mod 2^t. Keep a exactly when:

- w is odd and nonzero;
- w has no b-zero run;
- its leading-zero count c=t-bit_length(w) is less than b.

Let F_b fold a global coordinate a to a mod r, summing duplicates. Define

    g_(b+t)=F_b J_t Q_N^t x.                         (10)

Let K(z)=I-z A_r-S_b(z), the retained first-return feedback already compressed in the preceding report. Then the complete source is

    f(z)=x_R+sum_(L=1)^b z^L f_L
         +sum_(t=1)^d z^(b+t) g_(b+t)
         -sum_(c=0)^(b-1) z^c K(z)u_c
                 mod z^(n+1).                      (11)

Terms whose minimum degree exceeds n need not be evaluated.

### Proof of the subtraction

A path first reaching R at time b+t consists of a t-bit word w ending with one, followed by b zero bits. Suppose w has c leading zeros. Those initial c zeros are legal precisely when the initial source is not divisible by 2^(b-c). Equation (10) temporarily includes every source. Its forbidden input subspace is therefore P_(b-c)x.

Write w as its tau=t-c non-leading bits. For a source s=2^(b-c)j, formula (2) has source phase

    omega^(2^(b-c) j 2^c rev_tau(w))
      =eta^(j rev_tau(w)).

The retained endpoint is 2^(b+tau)j+w mod r, and the phase has period r in j. Summing j modulo r gives exactly u_c in (8). The forbidden contribution is consequently K_(b+tau)u_c, shifted by c degrees. This proves (11), with no commutation or independent-branch guard assumption.

### Cost and the remaining materialized trajectory

The shared global trajectory in (10) costs O(Nd); its masks and folds cost O(Nd) with all duplicate merges included. Preparing (8)-(9) costs O(N). Apply the constant-input retained feedback circuit to u_c only through degree n-c; all these corrections cost O(rbd), and at most b r retained input entries are carried. Thus

    source work = O(N(d+1)+rbd),
    source storage = O(N+r(n+1)).                    (12)

Since br<=N, the stated work is O(N(d+1)). For small b the previously reviewed eliminated-frontier algorithm can be better; (12) is not claimed to replace that useful bound in every regime.

At b approximately 2 log2 n, d=n-O(log n), so (12) is still O(Nn). This particular materialized trajectory really visits Theta(Nd) potentially contributing rows: when 2^b>=4d, a union bound leaves at least one quarter of all t-bit words satisfying the odd/no-b-zero condition at every t<=d, so J_t retains at least N/4 rows. This is only a cost boundary for the displayed trajectory evaluator, not for other circuits.

## 4. Free eliminated term equals a large partial transform minus a cheap correction

Embed the free top coefficient back into all N coordinates, with zeros on R:

    B_b x = E Q_EE^n E^T x.

Let A be the set of n-bit words containing no run of b zeros, including leading zeros in that test. Let M_A select those output rows. For w in A, define

    c=n-bit_length(w),
    a=floor(w/2^(b-c)).

Here 0<=c<b and 0<=a<r. Prepare u_c as in (8) and q_c=Q_r^d u_c. Define an N-output linear correction C_b by

    (C_b x)_w=omega^gamma(w) eta^(-gamma(a)) (q_c)_a,
                   w in A,
    (C_b x)_w=0,    w outside A.                     (13)

Then the exact operator equality is

    B_b = M_A Q_N^n - C_b.                           (14)

Proof: at time n the appended word is the final state w. Surviving paths require that w avoid b zeros. If its initial zero run has length c, the forbidden starting states are precisely P_(b-c). Their source frequency is divisible by 2^c, so the same folding argument used for (11) yields u_c. Reducing the frequency modulo r gives the leading d-bit index a, and the phase correction is exactly (13).

### Fully charged correction

- Prepare the u_c using N-r input visits.
- Compute b separate length-r stationary trajectories of d stages, costing O(brd).
- Generate the N word/phase/leading-zero records in O(N).
- Route exactly one correction value to each allowed output word, with O(N) scalar products and output writes.

Thus C_b is applicable in O(N+brd) work and O(N+br) storage. Since br<=N, storage is O(N). At b=ceil(2 log2 n), brd=O(N log n/n), so the correction is O(N). Every FFT in this statement is paid for as d sparse Q_r stages; none is a free oracle.

Equation (14) gives two reductions with that same additive work:

- an evaluator for the indicated masked Q_N^n gives B_b x by subtraction;
- an evaluator for B_b gives the indicated masked Q_N^n x by addition.

This establishes equivalence to the specified partial transform, not an algorithmic hardness theorem or a reduction to every output of the full transform.

### How much of the transform remains?

The number of retained rows is A_b(n), the number of n-bit words avoiding b zeros. The union bound gives

    N-A_b(n) <= (n-b+1) N/2^b=(n-b+1)r.              (15)

For b=ceil(2 log2 n), the omitted rows are O(N/n): almost the entire transform remains in (14).

The correction C_b factors through the b r values of u_0,...,u_(b-1), so rank C_b<=br. Since Q_N is invertible in characteristic different from two,

    rank(Q_N^n-B_b) <= (N-A_b(n))+br <= (n+1)r,
    rank B_b >= N-(n+1)r.                            (16)

The row-deletion component in Q_N^n-B_b is not proved cheaply applicable merely because it has few rows. Only C_b has the cheap application schedule above. Rank (16) does not prove Fourier hardness, nor does it supply the missing rows in linear time. It does show why an unspecified O(rn)-dimensional linear summary cannot encode the free map at the large-b choice: its actual rank is near N.

For reference, Q_N^n is precisely a Fourier transform with a fixed bit-reversal and diagonal phase:

    (Q_N^n x)_w=omega^gamma(w)
                     sum_s x_s omega^(s rev_n(w)).   (17)

Thus the remaining partial-transform claim has an exact input/output convention.

## 5. Why transposing forced recovery does not remove the source cost

There is an exact weighted reversal symmetry. Let B reverse n bits, let D have diagonal omega^(-gamma(s)), and set V=BD. Since gamma(s)=gamma(rev_n(s)), V is symmetric. Directly checking each edge gives

    V Q_N = Q_N^T V.                                (18)

For example, write s=epsilon*N/2+a. Dropping its top bit in the next state removes epsilon*rev_(n-1)(a) from gamma, exactly matching the reversed edge weight. This proves the identity without complex conjugation or positivity assumptions.

But reversal maps the retained suffix-zero set R to the prefix-zero interval

    P={0,...,r-1}.

Let H_R(z)=z Q_RE(I-zQ_EE)^(-1). Writing the monomial restrictions of V explicitly by their row/column sets gives

    H_R(z)^T
      = V_(E,P^c) [z(I-zQ_(P^c,P^c))^(-1)Q_(P^c,P)]
                     (V^(-1))_(P,R),                (19)

where the last factor is the (P,R) block of V^(-1). The equality is simply the transpose followed by the similarity (18). Both endpoint weights must be retained.

The bracket in (19) is forced recovery from P, not from R. The cheap routes (3)-(4) were proved for suffix-zero input support R. For P, even unrestricted short propagation has 2^L r output positions until L=b, rather than the r-coordinate support of the suffix-zero case. The retained geometry has changed. Transposition itself is free of asymptotic overhead for a given linear circuit, but (19) does not provide that different circuit. No unjustified application of the suffix-zero cost to a prefix-zero problem is made.

## 6. Complete charged stopping boundary

Combining the supplied operations at b near 2 log2 n:

- Read fresh global input: O(N).
- Construct f: currently O(N(n-b+1)).
- Solve the full retained polynomial jet: O(N).
- Evaluate the forced top recovery: O(N).
- Evaluate the free top recovery: equivalent within O(N) to the A_b(n)-row partial transform in (14).
- Write all global outputs and apply the final phase/reversal: O(N).

The exact remaining construction target is a faster evaluator for the right-side source (11) and, especially, the almost-complete partial transform (14), with arbitrary fresh input. Replacing the free term by Q_N^n would put the original Fourier task back into the algorithm. Neither a speculative recursion, a cheap low-rank label, nor the formal Schur identity closes this gap.

## 7. Exact checks and replay

`verify_compressed_boundaries.py` is freshly authored, uses only the Python standard library, and imports no earlier constructor/uploaded code. Its direct oracles apply Q_N and explicitly remove the eliminated/retained coordinates after each step.

Every b for N=2,4,8,16,32,64,128 is checked over GF(65537), with explicit root-order tests:

- 1,538 global basis inputs verify every source coefficient in (11) and the free equality (14);
- 247 retained basis inputs verify every forced-recovery coefficient (3)-(4);
- 28 arbitrary polynomial retained inputs verify the whole forced-recovery jet;
- 7 exact weighted transpose identities (18), plus 28 complete endpoint-weighted source/transpose-recovery identities (19);
- 8,256 integer-only word-count controls through n=128 verify (15), without running exponentially large transforms;
- exact stage and candidate-word counts (6)-(7).

The verifier's dense zero-filled coefficient arrays and readable modular powers are bounded oracles. The sparse/streaming production costs are the explicit schedules above. A relocated replay must reproduce the JSON and log byte-for-byte.
