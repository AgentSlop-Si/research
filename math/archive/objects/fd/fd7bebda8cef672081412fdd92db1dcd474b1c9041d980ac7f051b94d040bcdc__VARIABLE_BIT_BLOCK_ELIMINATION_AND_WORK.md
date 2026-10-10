# Variable-bit block elimination: an exact work function and the retained inverse

## Result and stopping boundary

For N=2^n and 1<=b<=n, retain the N/2^b shift-register states ending in b zeros and eliminate the others. The elimination is exact as a formal series at z=0. A fully charged sparse-level evaluator computes the eliminated resolvent jet through degree n, for arbitrary constant input x and marker h, in

    O(N min(n+1,2^b)) work.                             (1)

Its exact finite-horizon structural state count is given below. That particular full-frontier evaluator has matching Theta(N min(n+1,2^b)) work; this is not a lower bound for other arithmetic circuits.

At b approximately log2 log2 N, this evaluator costs Theta(N log N), so it does not produce the hoped-for growing-block saving. The retained dimension is N/2^b, but the retained first-return operator has an unconstructed inverse on polynomial unknowns. No closed Fourier recurrence or faster FFT is asserted. This is the stopping point of the bounded construction.

## 1. Operators and exact b-bit Schur elimination

Use the same explicit graph as the preceding marked-tree reports:

    Q e_s=e_(2s mod N)+omega^s e_(2s+1 mod N),

over a field containing a supplied primitive Nth root omega. Let R be the states divisible by 2^b and E their complement. The coordinate projections, injections, and restricted matrices use these fixed sets; no permutation is silently inserted. Put r=|R|=N/2^b and

    D_E(z)=I_E-z Q_EE.

The exact retained Schur operator is

    S_b(z)=I_R-z Q_RR-z^2 Q_RE D_E(z)^(-1)Q_ER.         (2)

For arbitrary x,

    S_b y_R=x_R+z Q_RE D_E^(-1)x_E,
    y_E=D_E^(-1)(x_E+z Q_ER y_R).                       (3)

The marked bilinear value is preserved exactly:

    h^T y=h_E^T D_E^(-1)x_E
        +(h_R^T+z h_E^T D_E^(-1)Q_ER)y_R.              (4)

All identities hold formally because D_E(0)=I. At a scalar z, the inverse chart requires det D_E(z)!=0 and the retained solve requires det S_b(z)!=0. The program never replaces these guards with the individual guards of some tree summands.

The retained zero transition is itself the unweighted doubling tree Q_RR on r coordinates. The expensive part is the coupled first-return contribution in (2), not that isolated tree.

## 2. An exact quotient-frontier evaluator for arbitrary inputs

Write

    D_E(z)^(-1)v=sum_(L>=0) z^L v_L,
    v_0=v,     v_(L+1)=Q_EE v_L.                       (5)

For an arbitrary constant v on E, initialize every E coordinate, including a zero value if it happens to occur. Each transition processes at most two weighted edges per active state; an edge entering R is discarded. Values arriving at the same vertex are added once. The phase on a one-edge is the actual omega^s for its source s, obtained from the charged O(N) root table.

This merges all contributing paths at their common state. It neither spends N operations per bit word nor assumes that phase-dependent paths have equal weights. The arithmetic performed is exactly the sparse matrix-vector recurrence (5).

A deterministic implementation uses N value slots, N integer visit stamps, and active-index lists. It clears only indices reached in the next frontier. All duplicate merges, weighted multiplications, input initialization, marker contractions, and address operations are charged. No length-N array is reinitialized at every level. Retaining the whole jet takes one scalar slot per structural active state; streaming a chosen scalar contraction can use less memory, without changing the stated work bound.

## 3. Exact finite-horizon state count

Let A_b(t) be the number of binary words of length t avoiding b consecutive zeros. Then

    A_b(t)=2^t                 for 0<=t<b,
    A_b(t)=sum_(j=1)^b A_b(t-j) for t>=b.                (6)

At level L, 0<=L<=n, the exact structural frontier is the set of N-bit states whose last

    d_L=min(n,b+L)

bits avoid 0^b. Therefore its size is

    F_(N,b,L)=2^(n-d_L) A_b(d_L).                       (7)

Proof. The initial state and each of the L successive states must avoid suffix 0^b. Read backward from the final state: these conditions are exactly the consecutive b-bit windows in its known suffix of length min(n,b+L). If a constraint reaches beyond that known suffix, choosing the missing initial bits to be ones satisfies it. Thus every state counted by (7) is reachable and every uncounted state is forbidden. For L<=n a specified start/end pair has at most one de Bruijn path, and all path weights are nonzero. Consequently reachability is not a cancellation assumption. The implementation can retain the full structural frontier independently of input-specific zeros.

The full degree-n jet has exactly the following potential coefficient-slot count:

    S(N,b)=sum_(L=0)^n 2^(n-min(n,b+L)) A_b(min(n,b+L)). (8)

Equivalently,

    S(N,b)=N sum_(t=b)^(n-1) A_b(t)/2^t
             +(b+1)A_b(n).                            (9)

The evaluator uses O(N+S(N,b)) arithmetic/addressing and O(N+S(N,b)) storage if all coefficients are kept. These are actual shared state counts, not counts of words alone.

## 4. Generating function and work bounds

The exact word generating function is

    sum_(t>=0) A_b(t) u^t
       =(1+u+...+u^(b-1))/(1-u-u^2-...-u^b).           (10)

This follows from (6), including its initial conditions. At u=1/2 it gives

    sum_(t>=0) A_b(t)/2^t=2^(b+1)-2.                   (11)

The ratios A_b(t)/2^t are nonincreasing: they are the fraction of length-t words that avoid the forbidden run. Since d_L>=L, equations (7)-(11) imply

    S(N,b)<=N min(n+1,2^(b+1)-2).                      (12)

There is also a matching lower bound for this structural evaluator. A length-d_L suffix contains at most L+1 candidate windows for 0^b. The union bound therefore gives F_(N,b,L)>=N/2 whenever L+1<=2^(b-1). Summing those levels yields

    S(N,b)>=(N/4) min(n+1,2^b).                        (13)

Hence S(N,b)=Theta(N min(n+1,2^b)). This lower bound concerns the explicitly materialized frontier/jet evaluator in (5), whose work includes every structural slot. It is not an arithmetic-circuit lower bound for the coefficient, marked scalar, or Fourier transform.

Preparing the O(n) counts in (6) costs O(nb) integer operations on O(log N)-bit words. Because b<=n and n^2=O(N), this preparation is within the O(N) base charge. The frontier algorithm itself need not enumerate the allowed words.

### Required edge cases and scale comparison

- b=1: A_1(t)=1 and (8) gives S(N,1)=N exactly. This recovers the single all-ones-tree jet with a linear coefficient budget.
- b=n: the retained set is {0}; every frontier has N-1 states, so S(N,n)=(n+1)(N-1). Reducing the interface to one coordinate has not made the marked eliminated inverse cheap.
- N=2: n=b=1 gives two stored coefficient slots, consistent with both formulas.
- b=floor(log2 n), for n>=2: 2^b is within a factor two of n, so this evaluator has Theta(N n) work. For example, the exact count ratios S/(N n) at n=8,16,32,64,128 are approximately 0.761, 0.770, 0.775, 0.779, 0.782.

At b=n the total number of allowed words through length n is only 2N-2, while the actual frontier work is (n+1)(N-1). This explicitly demonstrates why an O(N) word count is not an O(N) arbitrary-input algorithm. The quotient-state analysis accounts for the input amplitudes and phases at every level, rather than charging one operation per word.

## 5. Source, marker, and retained-operator costs

The same frontier engine computes all coefficients through degree n of D_E^(-1)x_E for arbitrary x. Contracting each level against arbitrary h_E gives all coefficients of h_E^T D_E^(-1)x_E in O(S) additional operations. Applying Q_RE, Q_ER, or the retained tree at the required levels consists of explicitly charged sparse weighted routing.

Thus the right side of (3), the eliminated marked scalar in (4), and the action of the retained operator (2) on a constant retained vector all have the upper bound (1). The left marked interface can be kept as this shared bilinear program; writing every expanded row coefficient is unnecessary and is not assumed free.

The unknown y_R(z) in (3) is generally a polynomial/formal-series vector. Applying a constant-input coefficient circuit to that unknown introduces further products or convolutions. The bound (1) does not furnish S_b(z)^(-1), nor does it allow that inverse or a polynomial-vector operation to be counted as one scalar instruction.

## 6. The exact remaining packet state and failure of simple closure

The trailing-zero classes are C_t={s:v_2(s)=t}, 0<=t<b, plus R. Their dimensions are N/2^(t+1). Eliminating C_1,...,C_(b-1) uses only finite zero-transition chains and no scalar denominator. It leaves the ones-ending class C_0, of dimension m=N/2, together with R.

Let J_1 inject j into global state 2j+1. The retained packet operator on C_0 is

    P_b(z)=sum_(a=0)^(b-1) z^(a+1) T_a,
    T_a=J_1^T A_1 A_0^a J_1,
    T_a e_j=omega^(2^a(2j+1))
              e_(2^(a+1)j+2^a mod m).                 (14)

Each T_a is separately a weighted functional tree. Its paths append a zeros and then one. But their sum must be inverted as a coupled operator; individual branch inverse guards do not certify I-P_b.

Define the explicit boundary maps

    W_b e_j=omega^(2^b j)e_(2^b j mod m),  j in R,
    V_b e_j=e_(2j+1 mod r),               j in C_0.

Then the same retained first-return operator has the exact representation

    S_b(z)=I_r-z A_(0,r)
              -z^(b+1) V_b(I_m-P_b(z))^(-1)W_b.        (15)

This is independently verified against the direct Schur formula (2). The interface inside the packet inverse remains N/2, even though the final retained set is N/2^b.

The first-return language is: exit R by a one; concatenate arbitrarily many packets 0^a1 with 0<=a<b; return by b zeros. For b>=2 the number of alternating runs is unbounded. For example, the maps of T_0 and T_1 compose to 8j+5 and 8j+6, respectively, in opposite orders; they do not commute. A constant-two-run argument cannot simply be iterated through this packet inverse.

The frontier algorithm already merges these concatenations correctly and gives the rigorous finite-horizon bound (1). What remains unproved is a closed smaller-state representation for the inverse in (15), including its carried sources and markers. In particular, neither the dimension N/2^b nor the individual tree branches establish a recurrence T(N)=T(N/2^b)+O(N).

## 7. Verification and preserved scope

The freshly authored verifier checks all b for N=2,4,8,16,32,64: 21 cases. It checks every exact frontier count (7), the work bounds and edge cases, all jet coefficients for deterministic arbitrary inputs, and marker contractions. For N<=16 it additionally checks 98 basis inputs through every formal degree against independent dense powers. There are 42 guarded fixed-parameter checks of the Schur recovery, packet identity (15), and marked identity (4). The larger n=8,...,128 examples above are count-only integer computations, not Fourier runs at exponentially large N.

All dense products and inverses are bounded test oracles. No uploaded program was executed. The all-input and all-size statements come from the proofs above, and no faster retained inverse is claimed.

Companions: verify_variable_block_jet.py, VARIABLE_BLOCK_JET_CONTROLS.json, VARIABLE_BLOCK_SHA256SUMS.txt.
