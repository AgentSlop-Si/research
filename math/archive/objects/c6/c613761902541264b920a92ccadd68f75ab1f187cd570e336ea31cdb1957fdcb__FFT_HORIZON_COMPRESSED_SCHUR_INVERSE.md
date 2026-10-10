# An exact FFT-horizon compressed Schur evaluator and formal inverse

## Bounded result

The retained variable-bit Schur operator has a finite-horizon compression that does not materialize eliminated frontiers. With N=2^n, 1<=b<=n, r=N/2^b=2^d, its entire degree-n action on one constant retained vector is computable in O(r(d+1)+n) field/address work. Its degree-n inverse on an arbitrary supplied polynomial right-hand side costs

    O(r(n+1+d^2)+n) work and O(r(n+1)+r+n) words.       (A)

There is an explicit online algorithm for (A), not an unclosed recursion. The representation is exact modulo z^(n+1); no full rational closure past that horizon is claimed. At b=ceil(2 log2 n)<=n, (A) is O(N). At b approximately log2 n it remains O(N log N).

This solves a retained inverse, with the right side already supplied. Constructing that side from a fresh arbitrary N-vector and recovering all eliminated outputs remain separately charged operations. The currently verified complete construction still takes O(N log N). No faster full FFT or unrestricted lower bound is asserted.

## 1. Exact target

Work over a field K containing a supplied primitive Nth root omega. Let

    Q_N e_s = e_(2s mod N) + omega^s e_(2s+1 mod N).

Let R={2^b j:0<=j<r}, E=R complement, and let Q_AB restrict rows to A and columns to B. Define

    S_b(z)=I_r-z A_r-z^2 Q_RE(I_E-z Q_EE)^(-1)Q_ER,
    A_r e_j=e_(2j mod r).

Formal inverses exist at zero. The exact task solved here is

    v(z) = S_b(z)^(-1) f(z) mod z^(n+1)               (1)

for every supplied f(z) in (K[z]/z^(n+1))^r. Arbitrary supplied polynomial markers h(z) are preserved: the top coefficient [z^n] h(z)^T v(z) adds O(r(n+1)) work. There is no numerical pivot guard or scalar specialization in this formal algorithm.

Write

    K_L=Q_RE Q_EE^(L-2) Q_ER  for L>=2.

Then S_b=I-z A_r-sum_(L>=2) z^L K_L. All K_L with L<=b vanish. The compression below gives every K_(b+t), 1<=t<=d.

## 2. Weighted path identity

For a binary word encoded by k, define

    gamma(0)=0,
    gamma(2a)=gamma(a),
    gamma(2a+1)=gamma(a)+a.

Leading or trailing zero bits do not change gamma. Let rev_t(k) reverse exactly t bits. Appending a t-bit word k to source j in the size-r graph with primitive root eta gives endpoint

    a=2^t j+k mod r

and path weight

    eta^(j rev_t(k)+gamma(k)).                        (2)

The proof is induction: the next one-edge multiplies by eta raised to the current state; reduction modulo r does not change that scalar. Source-dependent contributions sum to j rev_t(k), and source-independent contributions obey the gamma recurrence.

For t<=d and a fixed output a, the appended word is uniquely k=a mod 2^t. Thus the complete coordinate (Q_r^t v)_a contains exactly the relevant input fold for that word, including all phases. Here

    eta=omega^(2^b),
    Q_r e_j=e_(2j mod r)+eta^j e_(2j+1 mod r).

This r-dimensional stationary trajectory is the compressed state. It has no eliminated N-dimensional frontier.

## 3. First-return words and the fold

A first return from R of length L=b+t, L<=n, consists exactly of a t-bit word k followed by b zero bits, where k:

- has length t and starts with one;
- ends with one;
- contains no run of b consecutive zeros.

Call this set B_(b,t). Leaving R requires the first one. The final one must be followed by exactly b zeros; otherwise the return happened earlier. Avoiding the forbidden run before that final tail is precisely the remaining condition.

For such a word the endpoint on retained coordinates is

    y=2^(b+t) j+k mod r,

and its weight in the size-N graph is

    eta^(j rev_t(k)) omega^gamma(k).                  (3)

Set zeta=omega/eta. Define the explicit sparse routing C_t:K^r->K^r by processing a=0,...,r-1, putting k=a mod 2^t, and, only if k belongs to B_(b,t), routing

    zeta^gamma(k) v_a  to  y=2^b(a-k)+k mod r.        (4)

Different a may merge, and each merge is charged. Combining (2)-(4) proves the all-input identity

    K_(b+t) = C_t Q_r^t,    1<=t<=d.                 (5)

Indeed multiplying (2) by zeta^gamma(k) gives (3); folding its endpoint gives the specified y. The input fibers partition exactly when the a routes merge.

Consequently the complete target operator is

    S_b(z) = I-z A_r-sum_(t=1)^d z^(b+t) C_t Q_r^t
                   mod z^(n+1).                    (6)

Equation (6) is an equality of operators, not just equality on selected inputs or markers.

## 4. Representation, generation, and constant-input application

The representation stores:

- r consecutive powers eta^a;
- r phase corrections c_k=zeta^gamma(k);
- r word-validity bits, with their auxiliary trailing-zero/run data during setup;
- integers b,d,r and the routing rule (4).

All tables cost O(r+n) setup, including obtaining eta by repeated squaring and zeta by a charged scalar inversion. Prepare zeta^a by a consecutive-power recurrence. Then

    c_(2a)=c_a,  c_(2a+1)=c_a zeta^a

generates every correction in O(r) operations. Trailing-zero counts and maximum zero-run lengths are also generated by the binary-parent recurrence in O(r) integer/address operations. The length-t leading-bit test is k>=2^(t-1); oddness and the maximum zero run finish the membership test. No per-edge exponentiation, hash table, free Fourier transform, or hidden root bank is used.

For one constant v, stream v_t=Q_r v_(t-1), t=1,...,d, and apply C_t to each v_t. Each stage has O(r) charged state updates and routing work. Initializing and recycling dense r-vectors is included. The scalar field inversion has the usual separate cost in a bit-complexity model.

The feedback coefficient support is also small. If B_b(t)=|B_(b,t)|, then exactly

    B_b(t) max(r/2^(b+t),1)                           (7)

retained rows are structurally present in coefficient b+t. Different words occupy different low-bit residue classes. Summing (7) gives O(r+dr/2^b) sparse coefficient slots: use B_b(t)<=2^(t-1), separate t<=d-b from the remaining geometrically growing tail. Thus an emitted sparse jet need not occupy a dense r-by-n rectangle. Its computation nevertheless pays for the dense length-r trajectory at each stage.

No recursive Fourier improvement is assumed: this is simply d sparse Q_r applications, with every one of their O(rd) operations charged.

## 5. Arbitrary polynomial application and exact online inverse

For a supplied polynomial v(z), formula (6) gives a direct algorithm. For each coefficient v_j, compute only t<=n-j-b of its trajectory. The exact count of length-r feedback state visits is

    r sum_(j=0)^(d-1) (d-j) = r d(d+1)/2.            (8)

Applying I-z A_r, reading the input coefficients, and writing the output cost O(r(n+1)). The representation therefore closes under the required polynomial application with the bound (A), without treating coefficient convolutions as scalar operations.

For the inverse, initialize residual coefficient arrays rho_j=f_j, j=0,...,n. For j=0,...,n in increasing order:

1. Set v_j=rho_j.
2. If j<n, add A_r v_j to rho_(j+1).
3. Starting with u=v_j, for t=1,...,n-j-b, set u=Q_r u and add C_t u to rho_(j+b+t).

All updates go strictly to later coefficients. At stage j the residual is exactly the right-hand side of the coefficient-j equation from (6); induction therefore proves (1). Step 3 has exactly the state-visit count (8). This is a complete causal straight-line schedule. It neither invokes an unresolved smaller inverse nor postulates compressed polynomial closure.

Storage is O(r(n+1)) for residuals and solution, O(r) reusable trajectory scratch, and O(r+n) prepared tables and counters. A top marked coefficient uses the sum of h_j^T v_(n-j), with all r(n+1) scalar products charged. The representation is not a claim of cheap general multiplication or inversion of arbitrary rational circuits: the proved operation is the specific prefix (6).

## 6. Boundary maps are not free

For a fresh arbitrary global input x, exact block elimination still requires

    f(z)=x_R+z Q_RE(I-z Q_EE)^(-1)x_E,               (9)
    y_E(z)=(I-z Q_EE)^(-1)(x_E+z Q_ER v(z)).         (10)

The first task is not covered by (5), because x_E is arbitrary on the eliminated coordinates. The second task requests global eliminated outputs. Their costs are not included in the retained bound (A).

There is a simple exact obstruction to using a single r-dimensional *linear input summary* for every coefficient of (9). For 1<=L<=b, first hitting R at time L must use only zero edges; a one would need at least b further zeros. The initial state therefore has 2-adic valuation exactly b-L, and

    [z^L] f(z)_y
      = sum_(s: v_2(s)=b-L, s/2^(b-L)=y mod r) x_s. (11)

For r>=2 the possible y are the r/2 odd coordinates. These row functionals are disjoint nonempty sums, both across y and across L. Hence the first b source coefficient maps together have rank exactly br/2. For r=1 they are b disjoint nonempty class sums and have rank b. Thus any factorization through one fixed r-vector is impossible when b>=3, or when r=1 and b>=2. This is a narrow linear-summary obstruction, not an arithmetic lower bound; larger or polynomial summaries remain possible.

A full reference construction computes (9), uses the new inverse, and recovers (10) by coefficient recurrence in the original sparse system. Its verified cost remains O(Nn), with N input and output coordinates charged. The fresh checks compare every recovered coefficient, not merely the retained one.

## 7. Failed extensions and precise stopping boundary

### Extending the same route beyond the FFT horizon

For t>d, the state a of Q_r^t no longer determines the appended word k. Distinct words have already merged and may have different first-return validity and phase corrections. Formula (4), unchanged, rejects every word because a<r<2^(t-1).

Concrete exact counterexample: GF(65537), N=16, b=2, r=4, omega=64, input (1,2,3,4). The unchanged route gives zero at return degree 5, while the exact coefficient is

    (0,57313,0,510).

Thus the claim is deliberately modulo z^(n+1). An exact infinite rational representation or longer-horizon closure needs a new invariant.

### Using the wrong trajectory length

The return length is b+t, but the compressed trajectory is Q_r^t, not Q_r^(b+t). Appending leading zeros in the latter changes the bit-reversed source frequency by 2^b. Phase correction alone cannot fix this. The b-bit *output fold* in (4) is essential.

### Inferring a full FFT from the retained O(N) solve

Choosing b near 2 log2 n pays for the retained polynomial inverse, but not (9)-(10). The source rank obstruction above also prevents replacing both maps by an unspecified single-vector wrapper. No recurrence for the complete arbitrary-input Fourier task follows from (A).

## 8. Independently runnable exact checks

`verify_compressed_schur.py` was authored for this result and uses only the Python standard library. It imports or executes no earlier constructor or uploaded program. Run:

    python verify_compressed_schur.py

The checks use GF(65537), explicitly verify each supplied root's exact order, and cover every b for N=2,4,8,16,32,64,128. They include:

- 247 retained basis inputs across 28 parameters: all coefficients in (5)-(6), against sparse full-N elimination;
- 56 exact support-count checks for (7);
- 28 arbitrary polynomial applications against independently generated full-N feedback coefficients;
- 28 online formal inverse tests, including supplied polynomial markers;
- 28 fresh-global-input recoveries, checking every coefficient of every global coordinate and a nontrivial marker;
- exploratory full source-jet ranks through N=64, separately labeled as finite evidence;
- the explicit degree-5 failed extension above.

The `Prepared` class implements the table-driven retained inverse with reusable length-r stages and checks the exact stage count (8). Other routines deliberately use readable powers and small dense rank elimination as verification oracles; they are not those algorithms' cost models. All-size claims follow from the proofs above.
