# Independent review of the N7 eight-bank construction

10 October 2026

## Verdict

**Accepted:** the frozen author's exact eight-bank upper-bound construction in
its stated cubic splitting field, and hence over the complex numbers. This is a
characteristic-zero existence theorem, not only a conditional lemma. The
separate lower-bound claim is not reviewed or accepted by this receipt.

Reviewed author note: [exact eight-bank recipe](03_exact_witness_recipe.md). The following hash identifies the frozen original; public provenance/navigation transformations are recorded in SOURCE_ACCEPTANCE.json.
SHA256: `63ece9aad2e5da50d7381fb7dde34c794bb0589d223db73e9b5783f9d780de74`.

Reviewed literal witness: [EXACT_WITNESS.json](../controls/upper/sources/EXACT_WITNESS.json).
SHA256: `cc7693c49941f5581dbfe26f8529b40dba96b5aa4a6cebb3f331ff1a02fc59ab`.

The author note's explicit selected-square-system, edge, and reflection recipe
is accepted as written. A second direct run of the independent control uses the
frozen author's amplitude polynomials and checks the original matrices again.
This review therefore accepts the actual submitted witness, not merely a
different witness with the same cubic.

## Independently verified result

The negative Fourier matrix of size seven has a legal eight-bank realization
with orientation counts `(n_++,n_-+,n_+-,n_--)=(3,1,1,3)`. The parameters and
weights lie in the splitting field of the explicit cubic below over `Q(q)`,
where q is a primitive seventh root. This is an upper bound of eight only. It
does not by itself prove a minimum, and it does not show that the parameters
already lie in `Q(q)`.

The independent control checks all 56 literal phase branches, both left and
right inverse products, all 49 direct weighted Fourier matrix entries, and all
49 trace-derived Weyl coefficients. It uses exact characteristic-zero
arithmetic throughout. No author or predecessor program is read, parsed,
executed, imported, or compiled by the control.

## Original grammar and exact parameter field

Let `S e_i=e_(i+1 mod 7)`, `T e_i=q^i e_i`. Each bank is

    (1/7) sum_(j=0)^6 w_j
      [I-alpha S^epsilon-beta q^(epsilon delta j)T^delta]^(-1),

with guard `Delta=1-alpha^7-beta^7 != 0`. Set beta=1 in every bank.

In the basis `1,q,...,q^5`, put

    s2=(-8+35q+25q^2+28q^3+q^4-17q^5)/29,
    s3=(-3-5q-16q^2-4q^3+4q^4+19q^5)/29,
    g(t)=t^3+s2*t-s3.

Let `x1,x2,x3` be its three roots in its splitting field. The eight banks are

    (++ x1), (++ x2), (++ x3), (-+ 1),
    (+- 1), (-- x1), (-- x2), (-- x3).

The exact discriminant is

    (665859+635064q+863499q^2+425987q^3+275146q^4-15036q^5)/24389.

Both s3 and this discriminant are nonzero: their displayed numerators have
degree below six and are not zero, while Phi_7 is irreducible over Q. Thus the
three roots are distinct and nonzero. The six root-bank guards are `-xi^7`;
the two singleton guards are -1. Every original denominator is therefore legal.

## Edge moments and the parameterization boundary

Write

    H=q/(1+q),   C=(1/7) sum_(j=0)^6 q^(-j^2).

The normalized Fourier Weyl target is `q^(2(a+b)^2)`. The control also extracts
all 49 coefficients directly from the literal Fourier matrix and checks this
identity; C is nonzero.

For three positive-epsilon banks on the positive-delta side and singleton
parameter y on the negative-epsilon side, the endpoint equations fix
`h_y=H/y` and `sum_i h_i xi=H`. Define atom weights `A_i=h_i xi/H`. Their
moments satisfy `sum_i A_i=1`, and for a=2,...,5,

    m_(a-1)(y)=q^(2(a+1)^2)/(H*[a+1]_q)
                -([8-a]_(q^-1)/[a+1]_q)*y^(6-a).

Here the bracket has index 8-a. All displayed Gaussian denominators are
nonzero. Nonzero roots recover literal amplitudes by `h_i=H A_i/xi`.
Simultaneous reflection gives the negative-delta edge.

For singleton parameter 1, the five edge moments derived independently from
the Gaussian coefficients are

    m0=1,
    m1=-1-q-q^2-q^4-2q^5,
    m2=q,
    m3=-1-2q^2-q^3-q^4-q^5,
    m4=-2q^2-2q^3-q^4-q^5.

Then `D=m2-m1^2=1+4q-q^2+3q^4 != 0`. More generally, for fixed singleton y on
the nonsingular stratum D(y) != 0, an arbitrary cubic sum s1 determines

    s2=[s1(m3-m1*m2)+m1*m3-m4]/D,
    s3=m3-s1*m2+s2*m1.

These equations are exactly the two third-order recurrence conditions on
m0,...,m4. For distinct nonzero roots of
`t^3-s1*t^2+s2*t-s3`, the first three moments determine the three atom weights
by an invertible Vandermonde system; the two recurrence equations supply the
last two moments. Conversely any three-atom sequence with these distinct roots
satisfies the recurrence. This is a necessary-and-sufficient parameterization
on the stated stratum. It does not classify zero-node, coincident-node, or D=0
solutions, nor all possible eight-bank orientation patterns.

The displayed witness chooses y=1 and s1=0. Its edge conditions hold exactly.

## Every row and a complete exact amplitude specification

Work in `A=K[t]/(g)`, `K=Q(q)`. Let `R_r` be the three coefficient coordinates
of `t^r mod g`, in ascending powers of t. For a Fourier row b and bank
orientation `(epsilon,delta)`, put

    r=[epsilon*a]_7,  ell=[delta*b]_7,
    c=[r+ell choose ell]_(q^(epsilon delta)) if r+ell<=6, else 0.

Use the columns `c R_r` for each triple and the column c for each singleton.
In order, the eight transformed columns are the three ++ columns, the -+
singleton, the +- singleton, and the three -- columns. The exact ranks for
b=0,...,6 are

    7, 5, 7, 7, 7, 7, 5.

All seven augmented systems are consistent. Independent exact elimination
sets nonpivot variables to zero and records complete solutions in
[LITERAL_TRACE_RESULTS.json](../controls/upper/LITERAL_TRACE_RESULTS.json). Its full-rank pivot columns, numbered from zero,
are

    b0: [0,1,2,3,5,6,7],
    b2: [0,1,2,3,4,5,6],
    b3: [0,1,2,3,4,6,7],
    b4: [0,1,2,3,4,5,6],
    b5: [0,1,3,4,5,6,7].

Every listed minor has a directly computed nonzero value in K, recorded as six
exact rational coefficients. The edge rows are checked by full augmented
elimination too; they are not accepted merely because some determinant vanishes.
For each bank, b maps bijectively to ell, so the separate row solves use separate
amplitudes and cannot interfere.

For clarity, the transformed triple coefficients are the three moments
`z_d=sum_i h_i xi^d`, d=0,1,2. The independent control obtains the polynomial
`H_ell(t)` of degree at most two from

    Tr_A/K(H_ell(t)t^d)=z_d, d=0,1,2.

The trace Gram matrix is nonsingular, with determinant equal to the displayed
cubic discriminant. Since A is separable, after extension to its splitting
field the trace is the sum of evaluation at the three roots. The Vandermonde
matrix is invertible, so `H_ell(xi)` is exactly the unique node amplitude h_i.
The file records every coefficient of every H_ell, plus the singleton
amplitudes, and therefore specifies all amplitudes without approximate roots.

For a root or singleton alpha in a bank of orientation `(epsilon,delta)`, let
h_ell denote the corresponding recorded amplitude. Define the raw weights by

    w_j=C*(-alpha^7)*sum_(ell=0)^6 h_ell*q^(-epsilon*delta*j*ell).

This is a complete exact specification of all 56 weights. The 1/7 factor is
already present in the original bank definition and is not absorbed into w_j.

## Direct original-matrix control

For each phase j and each of the two triple orientations, the control forms the
literal seven-by-seven matrix

    X_j=t*S^epsilon+q^(epsilon*delta*j)*T^delta

over A. It checks `X_j^7=(t^7+1)I`, computes the inverse candidate
`(I+X_j+...+X_j^6)/(-t^7)`, and verifies multiplication by `I-X_j` on both sides.
Each cubic-algebra identity evaluates at all three roots, covering 42 literal
phase branches. The two singleton orientations are checked separately at
alpha=1, covering the remaining 14 branches.

The raw weight polynomial is multiplied by each inverse. Taking the algebra
trace sums the three root banks, and the singleton contributions are added
directly. The complete weighted sum equals the literal matrix
`F[k,t]=q^(-kt)` in every one of its 49 entries, with no residual or approximate
comparison. Thus the control does not rely solely on the Gaussian coefficient
formula for sufficiency.

## Frozen author recipe and literal-data audit

The first independent run chose its own row solutions by exact elimination.
The second run reads only the frozen inert JSON data. It checks every cubic and
moment coefficient, all row ranks, all reported pivot-column sets and pivot
minors, every transformed row equation, all sector polynomials, the exact three
selected square solves, the explicit b=1 edge formula, and the reflected b=4,5,6
formulas. It also verifies all three supplied quotient inverses by multiplication
and the extra noncollision identity g(1) in the note.

For each triple, its saved sector polynomial satisfies both the independent
trace-pairing equations and the author's Lagrange numerator identity after
multiplication by g'(t). The source run then reconstructs all 56 original phase
weights from those actual saved sector polynomials and repeats the complete
original inverse-matrix and Fourier-entry checks. [AUTHOR_LITERAL_RESULTS.json](../controls/upper/AUTHOR_LITERAL_RESULTS.json)
records this source-hash-bound pass. [LITERAL_TRACE_RESULTS.json](../controls/upper/LITERAL_TRACE_RESULTS.json) retains the
separately chosen independent witness control.

No author source program was executed, imported, compiled, or parsed. Only the
mathematical note and inert exact JSON data were used. The original source hashes are
preserved in the scoped receipt; no author or predecessor program is included.

## Scope and characteristic-zero status

The existence proof is already exact over K and its finite splitting-field
extension. No finite-field witness is being lifted to infer existence. Any
modular calculations used during discovery are unnecessary for this review's
conclusion. In particular, the expanded cubic coefficients have denominators
29 and cannot be reduced term by term modulo 29.

The algebraic witness supplies an eight-bank upper bound only. The separate
lower bound of eight is outside this upper-bound review; the combined checkpoint addresses it independently.
No statement of arithmetic runtime improvement, FFT speedup, or historical
priority is supported or made.


## Reproduction and receipt

From a disposable copy of controls/upper, with Python 3 and SymPy available, run:

    python verify_literal_trace.py
    python verify_literal_trace.py --source sources/EXACT_WITNESS.json

The first command writes [LITERAL_TRACE_RESULTS.json](../controls/upper/LITERAL_TRACE_RESULTS.json); the second writes
[AUTHOR_LITERAL_RESULTS.json](../controls/upper/AUTHOR_LITERAL_RESULTS.json). Both must report PASS. The [scoped acceptance](../receipts/upper_acceptance.json) binds the original verdict, the
control, both results, and frozen author sources by SHA-256. [Source acceptance](../SOURCE_ACCEPTANCE.json) records public relocations. Raw logs are excluded. No remote files
were modified.
