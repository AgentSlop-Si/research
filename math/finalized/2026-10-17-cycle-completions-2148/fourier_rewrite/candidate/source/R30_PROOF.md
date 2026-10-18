# R30: exact graph audit and guarded tensor/Green conjugation

Date: 18 October 2026.
Status: graph tooling and a classical operator rewrite, implemented and checked
at the stated scopes. No cyclic-DFT speedup, new exponent, or worldwide novelty
is claimed. All checking is author-side, not independent external review.

## 1. What a graph means here

A scalar node is one logical input or one exact arithmetic result. Directed
edges name its operands. A physical register may hold several logical values
at different times; those MUST be separate nodes. `graph_from_program` reads
R29's actual 12-byte instructions and versions every slot write to recover
single-assignment (SSA) dataflow. It does not identify values merely because
they occupy the same buffer or happen to coincide on one numerical input.

The graph is acyclic even when the mathematical operation is a cyclic Green
solve: its executed recurrence plus closure calculation is a finite acyclic
program. The index graph of the recurrence and the arithmetic dependency DAG
are different objects.

Inputs, coefficient preparation, reads/writes, required outputs, and precision
belong in the complete cost. Fewer storage slots (R29) is not fewer arithmetic
nodes. Common-subexpression elimination and graph rewriting are established
compiler methods, including FFTW's generator; they are not R30 inventions.

## 2. Exact bounded graph audit

Every real-word intermediate in the R29 graph is a dyadic linear form in all
real/imaginary input words. The verifier explicitly computes its integer
coefficient vector plus a common power-of-two denominator. It normalizes sign
and common powers of two and checks whether the form was already computed.
A repeated addition form could potentially reuse an earlier node, with its
required scaling still charged. No hash-only, numerical, or randomized equality
is used.

All 54 actual programs (dimensions 0..8, three kernels, two directions) have
zero additions whose complete normalized form repeats a previously available
form. Ordinary structural CSE is implemented and its full output maps checked.
This does NOT prove minimum addition count: distributive rewrites, other
subgraph identities, and changed algorithms are outside that audit.

The dense symbolic audit is deliberately OFFLINE and bounded. It can require
quadratic or larger work/storage; it is not the fast transform itself and is
not silently excluded from a uniform synthesis claim. Graph extraction and
literal structural interning use the program size, but dictionary performance
is not claimed to give a worst-case linear-time theorem.

## 3. A precise cross-operator fusion

Let N=2^D and work over C (or a characteristic-not-two splitting field with i).
Put

    C = ((1+i,1-i),(1-i,1+i))/2.

Let S be a set of binary address bits and U_S the tensor of C on those bits,
with identity on all others. For a nonzero binary mask v, define

    (Z_v x)_j = (-1)^popcount(v & j) x_j.

This is a diagonal SIGN mask, not an arbitrary Fourier phase mask. Let

    Q_v(rho) = I - rho Z_v.

Both parities occur for v!=0, so this diagonal is invertible exactly when
rho != +1,-1. The candidate graph window is

    x -> U_S -> Q_v(rho)^(-1) -> U_S^(-1) -> y.

Every intermediate is internal to the window. A requested/observed internal
output must not be erased. `compile_window` conservatively refuses such a
window, as well as mismatching tensor axes/directions, an unknown intermediate
operation or rounding barrier, invalid masks, and unsupported coefficients.
The implemented dyadic cases are rho=+3,-3, not unrestricted rho.

### One-coordinate identity

With X=((0,1),(1,0)) and Z=diag(1,-1), direct multiplication gives

    C^(-1) Z C = -i Z X.

Tensoring and preserving spectators gives, with w=v & S,

    M_v = U_S^(-1) Z_v U_S,
    (M_v x)_j = (-i)^popcount(w) (-1)^popcount(v & j) x_(j xor w).

When the first tensor is U_S^(-1), replace -i with +i. Each M_v is a signed/
fourth-root-phase permutation (a monomial operator). In particular,

    M_v^2 = I.

Indeed the two parity signs multiply to (-1)^popcount(w) and the squared
fourth-root phase equals the same sign; their product is one.

Conjugation respects products and inverses. Therefore

    U_S^(-1) (I-rho Z_v)^(-1) U_S
      = (I-rho M_v)^(-1)
      = (I+rho M_v)/(1-rho^2).                       (1)

This is a standard basis-conjugation/Pauli/involution identity, not a newly
discovered Fourier decomposition. It joins the C-tensor component used in
R29 with the weighted-permutation Green class of R23. The phase and direction
are essential; arbitrary phases cannot be commuted through U by assertion.

For rho=3, (1) is -(I+3M_v)/8. Its eigenvalues are -1/2 and 1/4, so it is
nonsingular. All constants are Gaussian dyadics and all divisions are by powers
of two; no singular compression, limiting parameter, or unproved inverse is used.
For rho=-3 the two eigenvalue sectors are interchanged.

## 4. Exact evaluation and charged work

For rho=3, each complex output is computed as follows:

1. read x_j and x_(j xor w), applying the specified fourth-root phase to the latter;
2. compute three times each real component by a left shift and an addition;
3. add the original component, divide exactly by eight, and negate.

The literal scalar graph therefore uses 4N real additions, 2N left shifts,
2N exact divides, plus O(N) explicit sign negations. Input/output, phases,
routes, coefficients, graph generation, and storage use O(N) field/word work
in a resident-array model with unit-cost O(log N)-bit index operations. This
is not O(N) bit complexity. The reference can also evaluate exact rationals;
it does not call a numerical FFT or use previous input answers.

For the recorded N=256, S=all eight axes, v=5, rho=3, forward-first example:

                         unfused R29 sandwich   fused graph
    real additions               7168               1024
    explicit negations           2240                768
    exact binary divides         2560                512
    left shifts                  1020                512

The 7168 additions are TWO AR4 tensor calls. This is NOT a comparison to one
R29 call or one FFT. The 85.714% reduction concerns additions for this entire
constructed sandwich; no elapsed-time speed ratio was measured.

The fused intermediate magnitude is at most 4M if each input real/imaginary
numerator has magnitude <=M, since M_v only swaps/signs components. Divisibility
by eight is checked in the integer-grid executor. Sufficient input reserve is
three fractional zero bits. The composed old implementation can require more
reserve and headroom; the tested integer inputs deliberately support BOTH.
This release is not a general replacement for the upstream tape/precision
contract. It uses resident exact scalar instructions and separately checks
four examples through the actual old bit-word arena.

## 5. Why this does not yet beat FFT

The fused matrix in (1) has at most two nonzeros in each row and column. For
N>2 it is not a cyclic Fourier matrix, whose entries are all nonzero. The
sandwich was a costly representation of an already sparse linear operation.
Removing that representation overhead is useful graph rewriting, not a new
linear-time algorithm for a dense Fourier transform.

No occurrence of this full sandwich is supplied by a single R29 tensor call.
This experiment does not demonstrate enough eligible occurrences inside a full
Fourier construction to change its arithmetic exponent. There is no full-FFT
benchmark or throughput claim. The C tensor is a binary-cube operator, not the
cyclic DFT on N coefficients.

A general Fourier phase cannot simply be labeled Z_v. To illustrate the missing
scope, take eta primitive of order 2N and d(j)=eta^j. Its Walsh coefficient at
binary frequency v, up to normalization, is

    product_(h=0)^(D-1) (1 + (-1)^v_h eta^(2^h)).      (2)

Each eta^(2^h) has order at least four. Every factor in (2) is nonzero, so all
N Walsh coefficients are nonzero. The ten finite-field controls independently
check the whole product formula and full support. This mask is not a single
parity term, nor a bounded-length sum of such terms.

It can be represented as a product of D single-bit diagonal factors, but
rewriting and applying all of those separately still costs O(ND). That is an
accounting boundary for this proposed use, not a general Fourier lower bound.

## 6. Verification scope

- 54 actual R29 bytecode exports and full CSE map checks; zero repeated normalized
  addition results, for the precise family and dimensions above.
- 420 full exact symbolic sandwich/fused matrix comparisons. These check the
  complete linear maps in their configurations, not sampled numerical residuals.
- 4416 exact rational vector comparisons against separately formulated direct
  products of the ORIGINAL 2x2 C, diagonal solve, and inverse C. Basis cases are
  included in that count; 73504 real output entries are compared.
- 12 larger checked-integer vector comparisons through D=10, including selected
  nonadjacent axes; 10752 real output entries. Four additional checks run the
  original R29 bit-word arena on both sides of the diagonal solve.
- Exact operation counters, invalid-pattern refusals, externally observed-output
  refusal, division/overflow controls, and live arithmetic mutation controls.
- Ordinary eta^j phase support through N=1024, not complete DFT evaluations.

Counts overlap where described. No external reviewer, other model, or proof
assistant participated. Earlier graph-mincut work is retained as prior research,
not rebranded as a newly invented approach. No repository or research-table write
was performed.
