# A charged two-shear interface for the implemented R30 kernel

18 October 2026. Exact construction and a narrow minimal-interface theorem.
No faster FFT, unrestricted lower bound, or historical-priority claim.

## 1. Result and recommendation

The previous completion proved zero R30 rho=±3 matches in ordinary radix-two
stage-component windows under monomial boundaries. This note changes the
boundary model: it permits two elementary triangular shears.

That change is enough to insert a genuinely eligible rho=3 R30 sandwich into
every butterfly of a complete cyclic DFT. Two is the minimum number of such
shears over Gaussian-dyadic coefficients. A reduction modulo 3 proves the
one-shear obstruction; a fully specified two-shear identity attains it.

The resulting method is dominated by the ordinary butterfly. Its literal
R30-plus-adapters evaluator takes 12 real additions per complex pair, compared
with 4 for the ordinary butterfly, before their common twiddle work. The
boundary-only change should therefore be closed as an FFT optimization attempt
in this separately evaluated scalar model. The construction establishes
eligibility, not useful savings. It does not resolve arbitrary joint circuit
optimization or a different packed-arithmetic model.

## 2. The exact adapter

Work first over complex numbers. Define

    H = [[1,1],[1,-1]],       K = [[1,3],[3,1]],
    U(s) = [[1,s],[0,1]],     L(s) = [[1,0],[s,1]],
    Q = diag(1,i),           C = (1/2)[[1+i,1-i],[1-i,1+i]].

The implemented one-bit R30 instance is

    R = C^-1 (I-3 diag(1,-1))^-1 C
      = -(1/8)[[1,-3i],[3i,1]],
    K = -8 Q^-1 R Q.                                      (2.1)

Direct matrix multiplication gives

    K U(-2) = [[1,1],[3,-5]],
    L(1) K U(-2) = [[1,1],[4,-4]],
    H = diag(1,1/4) L(1) K U(-2)
      = diag(-8,-2) L(1) Q^-1 R Q U(-2).                  (2.2)

Only the two shears are nonmonomial adapters. Every other coefficient is a
Gaussian dyadic, and no division by 3 appears. The implementation uses the
last expression, absorbing the common factor -8 into the output diagonal.

For a butterfly with twiddle t, multiply its second input by t before (2.2):

    [[1,t],[1,-t]] = A R B diag(1,t),
    A = diag(-8,-2) L(1) Q^-1,  B = Q U(-2).              (2.3)

The complete pair program after its ordinary twiddle is:

1. Replace a by a-2b.
2. Replace b by ib.
3. Evaluate the implemented R30 rho=3 pair rule on (a,b).
4. Multiply the second result by -i.
5. Add the first result to the second result.
6. Multiply the first result by -8 and the second by -2.

If original inputs were (a0,b0), step 3 returns

    (-(a0+b0)/8, -i(3a0-5b0)/8).

The final result is exactly (a0+b0,a0-b0).

### Eligibility and what was checked

The unfused interior is exactly TensorNode(axes_mask=1,inverse=False),
ParityGreenNode(parity_mask=1,rho=3), then
TensorNode(axes_mask=1,inverse=True), with axes=1 and no externally observed
internal results. These are the existing R30 compiler's permitted parameter
values, directions, masks, and three-node shape. The adapters sit outside the
window and are not erased. There is no rounding barrier.

This compatibility was checked against the retained R30 source and guards.
The fresh evaluator implements the specified scalar rule and verifies its
map. No supplied R30 program was executed, and no claim of an integration
run against the original compiler is made. `eligible_window.json` records
the exact candidate descriptor.

This is a deliberately constructed occurrence in a different Fourier program;
it does not contradict the zero count in the unmodified radix-two program.

## 3. Why one dyadic shear cannot suffice

Let A0 = Z[i,1/2], the Gaussian-dyadic ring. A monomial matrix has one nonzero
entry in each row and column. The model in this section is an exact 2-by-2
matrix identity on the same two complex coordinates, with no auxiliary lanes,
embedding, projection, nonlinear encoding, or packed word. Its factors are:

- any finite number of implemented one-bit R30 rho=±3 matrices;
- monomial matrices with coefficients in A0;
- at most one elementary shear U(s) or L(s), s in A0.

Suppose their product were H. Its determinant -2 is a unit of A0. Each R30
factor and each shear also has unit determinant. Therefore every intervening
monomial determinant, and hence every one of its nonzero entries, is a unit.
This follows from the elementary fact that each factor of a unit product in a
commutative ring is itself a unit. No unsupported division can be hidden in
one of these boundary scalings.

Reduce all entries modulo 3. Since 2 is invertible and x^2+1 is irreducible
over F3, this is the field F9 = F3[i]. Each rho=±3 R30 factor becomes the
identity: its off-diagonal entries vanish and -1/8 becomes 1. All invertible
monomial matrices remain monomial. A shear has at most three nonzero entries.
Monomial multiplication merely permutes and rescales these entries.

The reduced product thus has at least one zero entry. But

    H mod 3 = [[1,1],[1,2]]

has four nonzero entries. Contradiction. Thus two or more elementary shears
are necessary. Equation (2.2) attains two, even with exactly one R30 block.

The ring restriction matters. Over all rational coefficients one shear is
possible, for example

    H = diag(1,3/4) L(-5/3) K diag(1,1/3).

Its divisions by 3 are outside the implemented Gaussian-dyadic contract.
This is not a theorem about arbitrary exact complex boundary matrices.

## 4. The complete cyclic Fourier construction

Let N=2^D, D>=1, and zeta=exp(2 pi i/N). Let P bit-reverse the D input address
bits. In stage m=1,...,D, pairs are

    (q+j, q+j+2^(m-1)),
    q divisible by 2^m, 0<=j<2^(m-1),
    t=zeta^(j N/2^m).

On each pair apply the twiddle to the second input and then (2.3). Let A_m,
R_m,B_m,T_m be the resulting whole-vector block maps. Then

    F_N = (A_D R_D B_D T_D) ... (A_1 R_1 B_1 T_1) P,       (4.1)
    (F_N)_(r,c) = zeta^(r c).

Proof: (2.3) makes each whole stage exactly the ordinary radix-two DIT stage;
the classical even/odd DFT recurrence yields (4.1). All factors and their order
are supplied; this is not an isolated two-point map being called a full DFT.

There are ND/2 intentionally inserted pair windows, or D batched whole-vector
windows. For arbitrary large N one may compile axes=1 pair instances rather
than exceeding R30's whole-vector axes<=12 guard. This changes call batching,
not arithmetic. The scheme needs D stages and never claims sublogarithmic
mixing depth.

The field-operation identity is valid for arbitrary complex input. The
implemented dyadic scalar evaluator needs an explicit representation of the
roots for N>=8; the next section supplies one, with its cost.

## 5. Exact coefficient-lane representation, fully charged

For N>=4 put ell=N/4 and use

    K_N = Q(i)[z]/(z^ell-i),
    x = sum_(h=0)^(ell-1) x_h z^h,  x_h in Q(i),
    z mapped to exp(2 pi i/N).

This is the cyclotomic field Q(zeta_N): its degree over Q is N/2, so its degree
over Q(i) is N/4. The monic degree-ell relation z^ell=i supplies the displayed
basis. For N=2 use ell=1 and zeta_2=-1 in Q(i). For the implementation use
Gaussian-dyadic x_h, which stay in the same ring under the prescribed maps.

Multiplying by zeta_N^e is a permutation of ell lanes with fourth-root phases:

    h+e = q ell+r  ->  output lane r receives i^q x_h.     (5.1)

The map is bijective. For N=2 use 2e in place of e in this formula. Thus every
R30 call sees Gaussian-dyadic complex numbers and its literal operations are
supported. Apply the two shears and R30 independently on every lane of each
data-coordinate pair. The original kernel has not silently gained arbitrary
root coefficients.

This is explicit expansion, not free compression. It uses N*ell Gaussian
coefficient positions. Gaussian-dyadic inputs embed in lane zero; general
inputs already represented in K_N use all lanes. Input placement, zero
initialization, and output coefficient arrays cost O(N*ell) word operations
and storage. Output is the exact coefficient representation. Conversion to a
floating-point complex output at a chosen precision is a different task and
is not claimed to be free or implemented here.

For each original butterfly, there are ell scalar R30 pairs. Consequently
there are ND*ell/2 actual scalar pair calls. Twiddle application takes ell
lane routes and its sign operations. Computing indices and exponent reductions
uses O(ND*ell) O(log N)-bit word operations in this implementation. The verifier's
bit-reversal construction also uses O(ND) character/index work. No coefficient
oracle or prior-input cache is used.

The representation costs quadratic space for N>=4 and O(N^2 log N) scalar
work for the direct program. It repairs exact eligibility while worsening
complexity. It is not evidence of a fast packed Fourier algorithm.

### Fixed-grid compatibility

If all input real/imaginary lane numerators are multiples of 8, the inputs to
R30 after U(-2) and Q are still multiples of 8. Every /8 operation is therefore
exact. The adapters have no divisions. Each output equals the ordinary sum or
difference of the original inputs, so it is again a multiple of 8. The same
three reserve bits suffice at every stage; they are not consumed stage by
stage. Two reserve bits do not suffice for all inputs: (a0,b0)=(4,0) makes the
first R30 output -1/2.

If real input lane magnitudes are at most M0, each completed stage increases
the coefficient bound by at most two. Within a pair with bound M, U(-2) can
reach 3M and the literal tripling inside R30 can reach 9M; all other
intermediates are within that bound. Thus every intermediate in the D-stage
program has magnitude less than or equal to (9/2)NM0, and the simple bound
5NM0 is safe. Choose a signed width b with 2^(b-1)>5NM0. Shifts, exact divides,
and additions are b-bit operations, not unit-cost bit operations. A direct
bit-cost upper bound is O(ND*ell*b), aside from the stated index work.

## 6. Arithmetic ledger and non-amortization

`OPERATION_LEDGER.md` contains the detailed per-step ledger. With each complex
addition/subtraction implemented by two real additions and all signs charged,
one pair uses exactly

    12 real additions, 14 real negations,
    10 left shifts, 4 exact binary divisions.

The ordinary H pair uses 4 real additions and 2 negations. Both must pay their
same twiddle and data-routing costs. Even if boundary monomial maps were free,
Section 3 requires at least two evaluated complex shears. Combined with the
literal R30 rule's 8 real additions, this yields at least 12 real additions
per pair in this model. The displayed interface attains that addition bound.
This is a lower bound for the specified separately evaluated factor program,
not a minimum arithmetic bound for H or a general circuit lower bound.

A parameter family makes the scaling issue explicit. For units p,q in A0
with pq=4,

    H = diag(1,1/q) L(q-3) K U(p-3) diag(1,1/p).          (6.1)

Neither shear can disappear, since p=3 or q=3 is not a unit in A0. Choices
change scaling costs, not the two required complex additions. Choosing
p=1,q=4 gives (2.2); p=q=2 gives two coefficient -1 shears and shifts some
work to divisions. Rescaling cannot eliminate the minimum within this family.
The modulo-3 proof covers more than this parameterization.

For batched pair evaluation, literal costs add: there are ND/2 independent
pairs, or ND*ell/2 after lane expansion. Calling a single whole-vector kernel
rather than many pair kernels does not remove these scalar additions. The
addition excess is 4ND in the abstract complex program, or 4ND*ell in the
explicit lane program. It grows with N and D rather than amortizing away.

Jointly simplifying across R30 and its adapters can of course recover the
ordinary four-addition butterfly; that simply removes the manufactured
sandwich. This proof neither precludes other cross-stage algorithms nor
assigns them these literal per-factor costs. Hardware SIMD, giant-integer
packing, and auxiliary encodings need separate width/conversion accounting.

Recommended disposition: retain this as a constructive compatibility example
and the sharp dyadic shear-count obstruction. Do not pursue this same local
adapter family as an FFT speedup without a different, fully charged joint
algorithm.

## 7. Fresh verification and relation to the erratum

`verify_interface.py` is fresh standard-library code. It imports no supplied
R30 module, FFT library, NumPy, or SymPy. It checks exact rational Gaussian
matrix identities; 625 rational pair inputs; 625 checked integer-grid pair
inputs; division and overflow failures; all 294,912 monomial/one-shear
sandwiches over F9; and four live algebraic mutation controls.

Default full-transform checks examine all 5,460 Fourier coefficients on input
basis vectors for N=2,4,8,16,32,64. Expanded real-coordinate basis checks through
N=16 compare 17,488 real matrix entries, including every auxiliary lane. Dense
integer-lane inputs through N=256 are independently compared to direct DFT
sums, with all executed arithmetic counts checked. The inputs include zeros;
no numerical nonzero premise or zero shortcut is used.

The prior completion's mandatory erratum is honored: its support-depth and
literal sequential-count conclusions concerned the same N coordinates and
specified evaluator. The auxiliary lanes introduced here are explicitly
outside that representation premise and fully charged. They are not offered
as a contradiction of the erratum or as a free field extension.

The new contribution versus the earlier monomial-only theorem is the explicit
full-DFT embedding of the *implemented* rho=3 kernel, the exact two-shear
threshold over Gaussian dyadics, and the resulting dominated-cost decision.
Elementary basis changes, the R30 conjugacy, and radix-two FFT are classical;
no historical novelty is claimed for them or the factorization trick.
