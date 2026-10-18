# R30 Fourier-window eligibility: a complete scoped answer

Date: 17 October 2026 (UTC).
Result: exact obstruction for an explicit complete radix-two Fourier program,
with a positive control outside R30's implemented coefficient class.
No new Fourier algorithm or unrestricted Fourier lower bound is claimed.

## 1. Result and scope

Let N = 2^D, D >= 1. Consider the standard decimation-in-time (DIT)
radix-two FFT, with bit-reversed input, and every connected component of
every nonempty contiguous interval of its D butterfly stages.

There are exactly

    W_D = sum_{k=1}^D (D-k+1) N/2^k = N(D-1)+1

such component windows. None is equal to an R30 rho = +3 or -3 fused
window, even after arbitrary invertible monomial changes at the two
boundaries (permutations and nonzero diagonal rescalings). Consequently
the number of eligible windows is exactly zero, for every D.

At N = 256 this is zero among 1,793 component windows, across 36
whole-vector stage intervals. This is an algebraic obstruction, stronger
than checking that an opcode sequence is absent.

The declared window family is important. This does not cover every possible
Fourier factorization, arbitrary non-stage-aligned arithmetic subgraphs,
added dense changes of basis, joint evaluation across several windows, or
approximate transforms. It does close the R30 eligibility question for
this explicit natural family.

## 2. The complete Fourier transform being examined

Put omega_N = exp(2 pi i/N), and let

    (F_N)_{r,c} = omega_N^(r c).

This is the unnormalized positive-sign cyclic DFT, not the Fourier
transform of the binary cube. Let P reverse the D binary address bits.

For m = 1,...,D define B_m as follows. For every q divisible by 2^m and
0 <= j < 2^(m-1), set a = q+j, b = a+2^(m-1), and

    (B_m x)_a = x_a + omega_(2^m)^j x_b,
    (B_m x)_b = x_a - omega_(2^m)^j x_b.                 (2.1)

The full identity is

    F_N = B_D B_(D-1) ... B_1 P.                       (2.2)

Here omega_(2^m) = omega_N^(N/2^m). Equation (2.2) is the classical
radix-two Cooley-Tukey factorization. It follows inductively from splitting
the DFT into even and odd input indices:

    (F_N x)_r       = E_r + omega_N^r O_r,
    (F_N x)_(r+N/2) = E_r - omega_N^r O_r.

The input permutation P gives the leaf ordering of that recursion.
The fresh verifier also checks every entry of (2.2), exactly, for
D = 1,...,10.

A window of length k is a component of B_b ... B_a, where
k = b-a+1. Its active address bits are a-1,...,b-1; the remaining
bits are fixed. Thus it has 2^k inputs and outputs, and there are
N/2^k components for each interval. There are D-k+1 intervals of
length k. Summing proves the formula for W_D.

## 3. Exact invariant of these windows

**Unique-path lemma.** Every row and column of each length-k component
has exactly 2^k nonzero entries.

Each stage can change just its own address bit. Across this interval,
each active bit is visited exactly once. Given an input and output
with the same spectator bits, the choice of branch at every stage is
therefore forced. There is exactly one path, and its coefficient is
a product of nonzero twiddles and signs. It cannot cancel against
another path. All 2^k input/output pairs per row/column are present.

This argument also survives inserting arbitrary nonzero diagonal
scalings between stages. Invertible monomial boundary changes preserve
the number of nonzeros in each row and column.

For k = 1 the 2 by 2 component is

    B(t) = [[1,t],[1,-t]],  t != 0.

For a full-support 2 by 2 matrix A define its cross ratio

    chi(A) = A_00 A_11 / (A_01 A_10).

Multiplying rows or columns by nonzero scalars leaves chi unchanged.
Swapping one row or column replaces chi by its reciprocal. For every
butterfly, chi(B(t)) = -1, so its value remains -1 under all these
boundary changes.

## 4. R30 has a different invariant

Use R30's definitions

    C = (1/2) [[1+i,1-i],[1-i,1+i]],
    U_S = tensor product of C on selected axes S,
    Z_v(j,j) = (-1)^popcount(v & j),
    R_(S,v,rho) = U_S^-1 (I-rho Z_v)^-1 U_S.

Assume v != 0 and rho != +/-1. Set w = v & S. Direct one-coordinate
multiplication and tensoring give

    M_v = U_S^-1 Z_v U_S,
    (M_v x)_j =
        (-i)^popcount(w) (-1)^popcount(v & j) x_(j xor w),
    M_v^2 = I,
    R_(S,v,rho) = (I+rho M_v)/(1-rho^2).               (4.1)

The opposite tensor direction changes some phases but not the invariants
below. These are classical conjugation and involution identities.

If w = 0, R is diagonal and has one nonzero per row. If w != 0 and
rho != 0, it has exactly two nonzeros per row. On each pair
{j,j xor w}, its block, up to the common scalar, is

    [[1,rho u],[rho/u,1]],  u != 0.

The product of the two M off-diagonal weights is one, because M^2=I.
The cross ratio is therefore

    chi(R_pair) = 1/rho^2.                            (4.2)

For rho = +/-3 this is 1/9, or 9 after an odd row/column permutation.
Neither value is -1.

Now compare:
- k >= 2: the FFT component has 2^k >= 4 nonzeros per row; R30 has at
  most two. Equality is impossible.
- k = 1: the FFT cross ratio is -1; the R30 pair has ratio 1/9 or 9.
  Equality is impossible. A diagonal R30 instance also fails support.

This proves the exact zero count in Section 1, including boundary
permutations and diagonal scalings. Requiring unobserved internal outputs
or other R30 guards can only make the eligible set smaller.

An alternative, weaker check is that normalized FFT stages are unitary,
whereas the rho = 3 window has eigenvalue magnitudes 1/2 and 1/4.
The support/cross-ratio proof is stronger because it permits arbitrary
nonunitary diagonal boundary rescalings.

## 5. Sharp positive control: rho = +/-i gives the old butterfly

This section is an algebraic extension, not an implemented R30 feature.
For a one-stage component to match (4.1) under the allowed boundary
changes, (4.2) requires rho^2 = -1. Thus the only nonsingular,
nonzero possibilities are rho = +i and -i.

They are sufficient. On one bit set

    Z = diag(1,-1),
    M = C^-1 Z C = [[0,-i],[i,0]],
    R_i = C^-1 (I-i Z)^-1 C
        = (I+i M)/2
        = (1/2) [[1,1],[-1,1]].

Then, for every nonzero t,

    B(t) = 2 Z R_i diag(1,t).                         (5.1)

The rho = -i case follows by a column sign change. Hence, in this
extended class, every one-stage pair is representable: exactly ND/2
pair components, and no k >= 2 component.

There is also a full-transform identity, so this positive control does
not mistake an isolated sparse map for a DFT. Let U_m apply C to address
bit m-1; let Z_m be its parity sign; and let T_m place the twiddle t on
the second input of each butterfly pair and one on its first input.
Define

    R_m = U_m^-1 (I-i Z_m)^-1 U_m.

From (5.1),

    B_m = 2 Z_m R_m T_m,

so

    F_N =
      N (Z_D R_D T_D) ... (Z_1 R_1 T_1) P.            (5.2)

Equation (5.2) is just (2.2) rewritten using classical square-root-of-X
and Walsh/Pauli conjugacy. It contains D whole-vector, single-axis
windows, equivalently ND/2 pair blocks. Fusing each gives the usual
two-output butterfly. There is no larger eligible single-resolvent
window and no arithmetic improvement over ordinary radix two.

R30 only implements rho = +/-3. Therefore the positive control in this
section must not be reported as a successful use of its shipped rewrite.

## 6. Cost, including the actual Fourier program

For (2.2), use in-place butterflies and charge:
- N/2 butterflies per stage;
- two complex additions per butterfly;
- one complex twiddle multiplication except t=1;
- t=i as a sign/swap operation, not a general multiplication.

For D >= 1, the number of general complex twiddle multiplications is

    T_D = ND/2 - 3N/2 + 2.

Indeed there are ND/2 total twiddles, N-1 copies of 1, and N/2-1
copies of i. The total is

    ND complex additions, T_D general complex multiplications.

With the ordinary four-real-multiplication/two-real-addition complex
multiply, this particular implementation uses

    2ND + 2T_D real additions,
    4T_D real multiplications,

plus explicit sign/swaps, coefficient preparation, address operations,
and input/output. These are implementation counts, not optimality claims.

Twiddles can be prepared in O(N) coefficient-field operations and O(N)
coefficient storage from an exact primitive root supplied by the field.
The resident data array is O(N). Indices occupy O(log N) bits. This is
an exact arithmetic/field-operation accounting, not a bit-complexity,
fixed-precision, or wall-clock theorem.

At N = 256:
- 2,048 complex butterfly additions;
- 642 general complex twiddle multiplications;
- 5,380 real additions and 2,568 real multiplications under that
  specified implementation;
- zero eligible rho = +/-3 replacements, so these counts are unchanged.

The R30 number 7,168 -> 1,024 real additions concerns its constructed
tensor/Green/inverse-tensor sandwich. It is not the cost reduction for
this DFT. The two numerical experiments must remain separate.

For (5.2), applying a fused R_i stage, and absorbing its factor 1/2
against the explicit stage factor 2, again costs N complex additions.
The ordinary twiddles remain. Thus (5.2) has exactly the same charged
arithmetic as (2.2).

## 7. Two additional narrowly stated barriers

### 7.1 A chain of global two-sparse rewrites needs logarithmic depth

Suppose a full N by N DFT is represented by a product of full-vector
R30 fused maps, interspersed with arbitrary invertible monomial maps.
Absorb diagonal R30 instances into the monomial maps, and let t count
the remaining non-diagonal factors. Each such factor has at most two
nonzeros per row. The product of t
such factors has at most 2^t per row, since each multiplication at most
doubles the set of reachable input coordinates. The DFT has N nonzeros
per row. Therefore

    t >= log_2 N = D.                                 (7.1)

For the literal R30 rho = +/-3 evaluator, each non-diagonal full-vector
factor costs 4N real additions. Sequentially evaluating these factors
therefore costs at least 4ND real additions, before boundary costs.
This rules out sub-N-log-N arithmetic by simply chaining fewer of these
full-vector O(N) kernels. It is not a lower bound on arbitrary joint
evaluation, nonuniform partial windows, or unrestricted linear circuits.

With only Gaussian-dyadic coefficients and fourth-root phases,
there is an additional elementary coefficient-field obstruction:
every computed matrix entry lies in Q(i), whereas F_N for N >= 8
contains a primitive Nth root outside Q(i). Such a circuit would first
need a larger coefficient class. Allowing exact Fourier-root boundary
coefficients removes this field obstruction but not (7.1).

### 7.2 A conjugated ordinary phase has exponentially many XOR directions

Let eta have order 2N and D_eta = diag(eta^j). Write

    t_h = eta^(2^h),
    D_eta = tensor_h diag(1,t_h).

Every t_h has order at least four, so 1+t_h and 1-t_h are nonzero.
For each selected axis,

    C^-1 diag(1,t_h) C
       = a_h I + b_h M_h,
    a_h=(1+t_h)/2, b_h=(1-t_h)/2.

Conjugating on s selected axes gives exactly 2^s distinct nonzero XOR
directions, one for each subset of those axes. There is no cancellation:
different subsets route to different input columns. Each row therefore
has exactly 2^s nonzeros.

Consequently its expression as a sum of monomial matrices requires at
least 2^s terms; the tensor expansion attains that number. For all D
axes, this is N terms. A bounded-length sum of R30-like monomial terms
cannot replace it.

Applying the factored version directly still takes sN complex additions
and at most 2sN constant complex multiplications, plus any unselected
spectator diagonal. For s=D this is O(N log N). The claim concerns this
explicit evaluation and monomial-sum representation, not every possible
algorithm for the operator.

This strengthens R30's full Walsh-support observation into a support and
arithmetic statement for the actual C-conjugated phase matrix. It does
not convert that matrix into a cyclic DFT.

## 8. Independent exact verification and attribution

The fresh verifier imports no supplied R30 modules and executes no
supplied program. It checks:
- every entry of the full DIT factorization (2.2), for D=1,...,10:
  1,398,100 exact matrix coefficients;
- every row support and all one-stage cross ratios for the declared
  window family: 16,398 component windows across those sizes;
- the C-conjugacy, resolvent, rho=+/-3 obstruction, and rho=+/-i
  positive-control identities using exact Gaussian rational arithmetic;
- independent direct-loop arithmetic counts;
- 65 separately labeled finite-field phase-support corroborations.

The full-transform verifier represents coefficients as exact powers of
a primitive root, verifies disjoint supports before combining branches,
and compares the final exponent for input c/output r with rc mod N.
It uses no floating-point FFT or approximate equality. The Gaussian
checks use rational pairs. The finite-field checks corroborate, rather
than replace, the complex-field proof.

The original source is R30's user-supplied archive, retained privately. Its PROOF.md, REPORT.md,
README.md, and SOURCES.md were read; its programs were not run.
The 54-program duplicate-result audit was not repeated.

Attribution:
- Cooley and Tukey (1965), classical sparse FFT factorization:
  https://web.stanford.edu/class/cme324/classics/cooley-tukey.pdf
- O'Donnell, Analysis of Boolean Functions, Chapter 1, classical
  Fourier-Walsh characters and expansion:
  https://www.cs.cmu.edu/~odonnell/papers/Analysis-of-Boolean-Functions-by-Ryan-ODonnell.pdf
- IBM Qiskit SXGate documentation, the standard square-root-of-X matrix:
  https://quantum.cloud.ibm.com/docs/en/api/qiskit/2.2/qiskit.circuit.library.SXGate

The contribution here is the precise scoped window classification,
count, and cost reconciliation. No historical-priority claim is made.

