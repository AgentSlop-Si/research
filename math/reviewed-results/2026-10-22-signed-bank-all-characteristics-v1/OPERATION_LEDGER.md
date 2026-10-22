# Fully paid construction and literal application ledger

22 October 2026. This ledger accompanies THEOREM.md. It is an explicit upper-bound recipe, not a claim of practical speed or optimality. No supplied or historical program was run. No asymptotic lower bound follows from the bank count.

## 1. Input and cost units

Input is odd N>=23, d=floor((N+10)/8), a certified representation of F_Q, and a supplied q of exact order N. The more general N>=8d-10,d>=4 theorem uses the same ledger. Verify the order by computing successive powers through N, checking q^N=1 and no earlier power is 1: O(N) base-field operations, without an integer-factorization oracle. If the starting field representation itself is not supplied and certified, its construction/certification must be added; it is not silently included in unit-cost field arithmetic.

Let m=N-d, B=2m+2, H=d(d+1)+2m-1, E=F_(Q^2), R=Q^2, and s=dim U-1<=m. A field multiplication, addition and inversion are counted separately. Vector/array addressing, coefficient reads, and writes must also be paid. We explicitly price the enormous splitting overfield; B does not mean B scalar operations.

The finite coefficient construction has a deterministic alternative and a Las Vegas alternative. The latter requires independent uniform E-valued coordinate samples. Their random-bit generation and coefficient writes are charged, not treated as input-free. No sampling claim applies to a nonuniform heuristic distribution.

## 2. Quadratic coefficient-field preparation

Construct E from the supplied F_Q by enumerating at most Q^2 monic quadratics. For each test all Q field elements for a root. A quadratic is irreducible exactly when it has no root, and finite fields have irreducibles of every positive degree. This is O(Q^3) base-field operations and comparisons, using streamed enumeration. Store the selected two coefficients and the polynomial-basis representation. This deliberately elementary guarantee avoids any unpriced irreducibility or factorization routine.

Arithmetic in E has constant-degree polynomial-basis costs over F_Q. Multiplication and reduction take O(1) base multiplications/additions; inversion can use constant-degree extended Euclid, with explicitly paid base inversions, or exponentiation with O(log Q) E multiplications. Either convention must be fixed in an implementation.

If F_Q itself is supplied as F_p[z]/P of degree e, its arithmetic costs and the certification of P remain part of the supplied field interface. With schoolbook polynomial arithmetic, multiplication is O(e^2) operations in F_p, addition O(e), and inversion can be bounded by O(e^3 log p) F_p operations using exponentiation. No machine word is assumed to hold Q, R, m!, or a field element.

## 3. Envelope and legal coefficient polynomial

Prepare q powers, the Gaussian coefficient array, D(q^j), and the enlarged envelope. There are O(N^2) scalar entries. RREF/nullspace and monic-slice parametrization cost O(N^3) field operations and O(N^2) storage; at most O(N) pivot inversions per elimination are charged. This includes actual verification that the monic slice is nonempty, as guaranteed by the proof.

For each chosen affine parameter point, construct g, check c_0!=0, calculate gcd(g,g') by Euclidean division, build all p_j=t^j mod g for 0<=j<N, and rank-test the full N by (2m+1) axis matrix. A conservative bound is O(N^3) E operations plus O(N) inversions, and O(N^2) E storage per test. Building the quotient remainders takes O(Nm) operations. No preselected nonzero axis minor is needed by the algorithm.

- Deterministic choice: enumerate all R^s points. Guaranteed cost O(R^s N^3) E operations, including failures, plus the stated inversion costs. A grid of H+1 distinct E elements per coordinate also suffices, reducing the bound to O((H+1)^s N^3) when that explicit grid is prepared.
- Las Vegas choice: sample s independent uniform E elements per trial. The theorem gives rejection probability at most H/R<1/2, so expected fewer than two tests, or expected O(N^3) E arithmetic after field preparation. Each trial writes s elements and requires expected O(s log R) unbiased random bits using ordinary rejection sampling from bit strings. Verification is deterministic and exact; only the choice is randomized. The probability estimate is not a fixed cap guaranteeing success after two attempts.

This produces actual coefficients of a legal g in E. It does NOT yet produce any root or physical bank.

## 4. Genuine root-field construction, with no oracle

Let t=m!. Every irreducible factor degree r of the squarefree degree-m g satisfies 1<=r<=m and r divides t. Hence all roots lie in the finite overfield L=F_(R^t). This is a known explicit overfield, not an assertion that the minimal splitting field has degree t. The minimal degree is lcm of the factor degrees and is at most t; it may be superpolynomial in N.

To build L without factoring g or assuming an extension oracle:

1. Enumerate at most R^t monic degree-t polynomials over E.
2. For each candidate, divide by every monic polynomial of degrees 1 through floor(t/2). There are fewer than 2R^floor(t/2) such divisors. The candidate is irreducible exactly when none divides it, since a reducible degree-t polynomial has an irreducible factor of degree at most floor(t/2).
3. Monic long division costs O(t^2) E operations. Thus a guaranteed, very loose field-preparation bound is O(t^2 R^(t+floor(t/2))) E operations, including all failed candidates. Existence of a degree-t irreducible over E guarantees termination. Store its t coefficients and use a polynomial basis for L/E.
4. Enumerate the R^t elements of L, evaluate g by Horner, and retain its m roots. This costs O(m R^t) L multiplications/additions and exactly finds all distinct nonzero roots. Check their count, distinctness, nonzeroness, and product polynomial against g. No formal roots or derivative atoms replace actual field elements.

This procedure is astronomically expensive. It is included to make the representation construction fully finite and paid, not to recommend it or claim an efficient compiler. More efficient finite-field factorization/extension algorithms may replace it only with their own justified, charged contracts.

With polynomial-basis degree t, each L multiplication/reduction costs O(t^2) E operations, addition O(t), and inversion by exponent R^t-2 costs O(t^3 log R) E operations. Thus the root scan alone is O(m t^2 R^t) E arithmetic. The field modulus, enumerator, root list, coefficients, guards, raw weights, and outputs must all be represented without fixed-width overflow. At the original base F_Q, every L element has 2t coordinates.

For an infinite input field, the theorem remains an algebraic existence/construction statement with a genuine splitting field of degree at most m!. Its finite-field brute-force costs do not purport to price arbitrary infinite-field or number-field operations. No unqualified bit-complexity statement is made for that interface.

## 5. Amplitudes, branch weights, and operator preparation

All following operations are in the actual root field L, not in a formal quotient containing unspecified roots.

- Build the two Vandermonde matrices with exponents 0,...,m-1 and 1,...,m. They share nodes; the latter differs by invertible column scales. Invert one by elimination once in O(m^3) field arithmetic and O(m) inversions, then pay for those column scales. This is not a fast-Vandermonde oracle.
- For each positive row, pad missing moments and multiply by the prepared inverse; recover the right/axis interval in the same way. Reflection supplies negative rows with paid assignments. All N sectors together cost O(Nm^2) field arithmetic. Prepare f and Gaussian arrays in O(N^2) operations and divisions. The row recurrences may be checked in O(N^3) additional operations.
- Solve the b=0 axis system by ordinary elimination in O(N^3) arithmetic with O(N) inversions, then convert its moment vectors to the two root-amplitude lists. The axis singleton scalar is allocated to one cross bank. No output row is dropped.
- Recover all BN raw weights with direct length-N sums: at most BN^2 multiplications and BN(N-1) additions, plus O(BN) scaling operations. Prepare gamma, Delta, 1/N, alpha inverses, and required powers, with every inversion and coefficient write charged. This is O(N^3) arithmetic overall, not a free transform.
- Store every raw weight, or the application-normalized weight w_j/N. Dividing all BN weights by N can be implemented as BN multiplications after one inversion of N. Prepare for each bank the N values (1-q^k)/alpha and alpha^-1. These are shared within that bank by permuting the phase index, costing O(BN) arithmetic and B inversions.

After the coefficient and root-field stages, all sector/weight/operator preparation is therefore O(N^3) L arithmetic, O(N^2) L storage, and explicitly charged inversions. These costs are not included in the warm application count below.

If literal dense inverse-matrix verification is desired rather than the direct proof, reconstruct the BN sparse branch matrices, solve all N right-hand sides in O(BN^3)=O(N^4) field operations using the same zero-diagonal recurrence, and check both sparse products and the final aggregate. This optional verification cost is separate from both construction and one application. Storing all dense inverses would require O(BN^3)=O(N^4) field elements and is unnecessary; verification can stream them. This report does not claim that this entire enormous root-field construction or dense verification was actually run.

## 6. One literal application, all outputs charged

Every branch has beta=1. In the original equations for v=Q_j^-1 x,

    (1-q^(epsilon delta j+delta i))v_i-alpha v_(i-epsilon)=x_i.

There is exactly one zero diagonal, at i_0=-epsilon j modulo N. Precompute a_(j,i)=(1-q^(epsilon delta j+delta i))/alpha. Once per bank compute b_i=-x_i/alpha, costing N multiplications. The zero-diagonal equation gives v_(i_0-epsilon)=b_(i_0). The remaining N-1 equations, traversed backwards in epsilon, use

    v_(i-epsilon)=a_(j,i)v_i+b_i.

There are N-1 multiplications and N-1 additions per branch. Multiply all N output coordinates by the stored normalized raw weight w_j/N, and sum the N branch vectors. This requires N^2 weight multiplications and N(N-1) accumulation additions per bank. Branch output buffers can be reused.

The conservative warm count per bank is therefore

    2N^2 multiplications,
    2N^2-2N additions.

Summing all B bank vectors gives a complete application budget

    2BN^2 multiplications,
    2BN^2-BN-N additions.

These counts do not simplify zero or unit weights and include all N output coordinates. They assume the prepared a values, alpha inverses, and w/N weights above. Each branch's output reads, weight reads, cyclic index updates, and accumulation writes cost O(N), so the total address/read/write work is O(BN^2), not omitted. Working buffers take O(N) field elements on top of O(BN) operator data. The input and output each cost N field-element reads/writes.

With B=O(N), warm arithmetic remains O(N^3), in a potentially enormous extension field. Expanding multiplications into E costs O(BN^2 t^2) E arithmetic, additions O(BN^2 t); then E costs must be expanded into the supplied base-field interface. Raw weights alone require BN*2t base-field coordinates, or Theta(BNt log Q) bits in a canonical fixed-width coefficient representation. Output writes require N*2t base coordinates unless a separate, verified descent compression is requested and paid.

The proof says that base-field inputs produce base-field Fourier outputs, so a certified implementation may verify and remove the zero extension coordinates after computation, costing O(Nt) base-coordinate checks. It cannot silently treat extension-valued intermediates as base scalars. The comparable dense base-field Fourier schedule costs N^2 multiplications and N(N-1) additions after coefficient preparation. Accordingly this bank construction establishes no arithmetic advantage.

## 7. Closure boundaries

Included: finite coefficient-field construction, all failed coefficient candidates under the chosen algorithm, legal polynomial testing, actual root-field construction, root recovery, amplitudes, raw weights, original branch parameters/denominators, all-output application, storage, addressing, and base-coordinate expansion.

Not claimed: a practical implementation of the astronomically large deterministic splitting overfield; polynomial extension degree; a fast root oracle; fast multi-bank sharing; minimum bank count; full support classification; an FFT runtime improvement; floating-point accuracy; finite-word production qualification; historical novelty; or closure of the broader parent owners.
