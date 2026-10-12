Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: 07c908c530a034ceb56c9d380ec803d139e41359294263e05fbfa13ecf05b797

---

# Q27 affine-multiplier certificate: independent review

Date: 11 October 2026 UTC. Decision: **ACCEPT, with the exact scope below.**

## Accepted result

For the pinned N=8 Phase42 chart, vary only stage-1 edges **(8,9,10)** over
the unit circle and freeze the other 31 free phases at the specified witness.
Each stage remains the sum of its three cycle Green inverses with coefficients
(1,1,1); the product is M=S2*S1; all six Green inverses must exist; and there is
no free interstage diagonal.

This admissible three-phase slice contains no matrix externally equivalent to
F8 by arbitrary invertible complex row and column monomials. The same necessary
modulus obstruction excludes equivalence to any nonzero constant-entry-modulus
matrix. This is an exact nonexistence result on one pinned coordinate slice,
not a feasible realization, a theorem about all consecutive triples, or a
theorem about the full 34-phase fiber.

The independently checked certificate is

    sum a_rc(z) Q_rc(x,y,z) = F(x,y,z),   F = 1-hxyz,

and, separately checked directly on the defect polynomials,

    sum a_rc(z) P_rc(x,y,z) = F(x,y,z)^2.

There are 47 nonzero multiplier terms across 41 windows: 41 constants and six
z-linear terms. Their coefficients are exact Gaussian rationals. The old
constant-coefficient obstruction was rechecked against the newly reconstructed
quotients, so degree one is the least possible total multiplier-degree bound in
this particular F-squared format. No claim about the rank of the complete
degree-one system is needed or made.

No repair is required for the frozen candidate. The following scope limits
form part of acceptance.

## Frozen source and independence

Candidate archive:

    Q27_Consecutive_Affine_Multiplier_Author_Candidate_2026-10-11.zip

SHA-256:

    0eb10862e9c6b00650f13432c45d8c2834965985ec16afbf545bcc4e8ecee512

Candidate manifest SHA-256:

    135bb80593200e69adced6764bd0974cbfd94827340b20dc580b75dcc0711fcd

Certificate SHA-256:

    10a9830ecbd70e92f94716a89d5e61ad3146d03161539c55cff5831b59743a5f

Chart SHA-256:

    5528afbbd5b4008a5e0f79043870e72a613e0fd421288d2ce1e5dbffee1c9e98

Quotient coefficient packet SHA-256:

    9945bb75990a960b2da0ade2e96da6831ec90bdf21256df9e47a94415eb0079a

All 26 candidate-manifest members were verified by size and SHA-256. All seven
declared predecessor source bindings were checked against the existing files.
The predecessor dual snapshot was also verified byte-for-byte against the
original candidate archive nested inside its accepted independent review
archive, whose SHA-256 is
42d853a9b2a02e6bdfe84e4e92d2f60a2b50e91853833c9f8eb0666e47eab999.

The reviewer wrote and executed only a fresh review program. Candidate and
predecessor programs were not executed, imported, compiled, or evaluated.
Candidate code could be read as text; it was not the computational checker.
The original research files remained unchanged. No Sheet, GitHub, or other
external write was performed. Predecessor coverage results are inherited from
their accepted reviews; this review does not claim to rerun all predecessor
exclusion proofs.

## Independent Green construction and fixed chart

The reviewer reconstructs each witness weight from its integer pair as

    (a^2-b^2 + 2ab i)/(a^2+b^2).

All 48 weights have exact unit modulus. The seven tree-pinned edges in each
stage remain one, leaving 34 free phases before selecting the three moving
ones. The destination convention is checked: edge 8b+j maps cycle[j-1] to
cycle[j]. Edges 8,9,10 are positions 0,1,2 of branch 1 in stage 1, with zero-based
branch indexing. Multiplication of their nonzero frozen unit gains by x,y,z
bijectively parametrizes the same absolute unit-phase coordinates. The other
31 free phases and 14 tree-pinned edges do not move.

The five fixed matrices I-W are inverted by a fresh Gauss-Jordan algorithm over
Q(i). The active I-W is inverted directly by the same algorithm over
Q(i)(x,y,z). This is independent of the author's directed-path numerator
construction. All six inverses are checked in both multiplication orders.
The determinant accumulated during each elimination agrees exactly with its
Green denominator.

The five inactive guards are nonzero constants. The active determinant is F,
with

    h = (-383187819337037874577 + 235291331868842780736 i)
        / 449660889716782337425.

Its norm is one and h is not one. Multiplying the direct active inverse by F
produces a polynomial matrix B. Full polynomial multiplication independently
checks (I-W)B=B(I-W)=F I. With C the two fixed stage-1 Greens and L the three
fixed stage-2 Greens, the numerator is N=L(FC+B)=FM. Every entry is triaffine.
There is no additional diagonal inserted into this construction, and no
transfer by a gauge change to a different frozen chart is used.

## Defects, conjugation, division, and coefficient signs

For triaffine N the checker forms the coefficient-conjugate reciprocal
polynomial matrix

    Ntilde = xyz * conjugate(N)(1/x,1/y,1/z).

Every Gaussian coefficient is conjugated and every exponent is complemented
componentwise. The 49 anchored defects are formed directly as

    P_rc = N_rc N_00 Ntilde_rc Ntilde_00
           - N_r0 N_0c Ntilde_r0 Ntilde_0c,   1 <= r,c <= 7.

Exact polynomial division gives P_rc=F Q_rc for every window. Every remainder
is zero, and full multiplication back checks all 49 identities. The union of
quotient supports is exactly the supplied set of 44 monomials; all 2,156
Gaussian-rational coefficient entries agree with the sealed data. These checks
establish the normalization and sign of F and of each defect independently of
the stored coefficient table. No matrix entry is divided out.

On the unit torus the reciprocal variables equal their conjugates. Consequently

    P_rc = (xyz)^2 |F|^4
           (|M_rc|^2 |M_00|^2 - |M_r0|^2 |M_0c|^2).

Invertible complex row and column scalings and permutations of a nonzero
constant-entry-modulus matrix yield an array of squared entry moduli of rank
one. Every anchored defect above must therefore vanish for Fourier equivalence.
Only this necessary implication is used. It neither asserts sufficiency of
these equations nor needs a nonzero-entry normalization.

## Complete exact multiplier identity

Each serialized numerator is interpreted literally as a Gaussian integer and
divided by the one common nonzero Gaussian-integer denominator. Window indices,
row-major quotient order, monomial exponents, total degree, distinctness, and
nonzero terms are all checked. There are no hidden numerical approximations.

The reviewer clears one rational integer denominator across the reconstructed
polynomials and target, then accumulates the complete polynomial identity using
Gaussian integer pairs. Thus no coefficient is truncated or projected onto
selected solve columns. The residual is exactly zero at every exponent.

For all possible degree-at-most-one multiplier monomials (1,x,y,z), the quotient
expanded support contains 85 monomials. All are controlled, including the two
outside the author's 83-column square solve:

- index 83: exponent (4,3,2);
- index 84: exponent (4,3,3).

The checker also directly sums the reconstructed P polynomials, rather than only
inferring the second identity by multiplying the Q identity by F. Its complete
degree-one expanded support has 119 monomials. The residual against F squared
is identically zero. Outside these full supports every coefficient is zero by
complete polynomial accumulation, not by assuming a degree bound from a scout.

The predecessor normalized coefficient functional is separately rechecked by
ordinary, nonconjugated coefficient pairing. It annihilates all 49 freshly
reconstructed Q rows and pairs with F to exactly one. This excludes constant
multipliers even over C, since the functional extends C-linearly. Coupled with
the present affine certificate, it proves the minimal degree assertion. Neither
finite-field membership, modular rank, the solver's internal equations, nor
finite sampling is used as the proof of the certificate.

## Adversarial and direct controls

The full checker rejects:

- adding one to a multiplier numerator;
- omitting a nonzero term;
- deleting every linear term;
- changing the common denominator;
- replacing target F by F squared in the quotient identity;
- relabelling all z multipliers as x multipliers;
- adding one to either unselected target coefficient, separately;
- omitting coefficient conjugation, which changes all 49 P windows.

Five fresh exact parameter triples were checked: three unit-torus points and
two nonunit algebraic controls. They differ from the current author's samples:

    (-i, i, -1)
    ((20+21i)/29, (7-24i)/25, (-15+8i)/17)
    ((9+40i)/41, (-28+45i)/53, (12-35i)/37)
    (3, -2, 7)
    (-3, 4+i, 2-i).

At each point and its reciprocal-conjugate, all six matrices were directly
inverted again. This gives 60 direct inverses, 120 two-sided inverse products,
60 nonzero-guard checks, 245 quotient evaluations, 320 numerator entry checks,
320 reciprocal-conjugate numerator entry checks, and 147 comparisons with
actual unit-torus squared-modulus defects. The nonunit points test algebraic
identities only; no unit-torus interpretation is assigned to them.

At the exact unit-torus pole (conjugate(h),1,1), F is zero and the actual active
matrix I-W is singular by direct elimination. It is rejected. A pole is never
treated as an admissible point or a feasible Fourier realization.

These tests are redundant controls. The complete exact polynomial identities
are the proof. If Fourier equivalence held at an admissible point, every P_rc
would vanish, so the certificate would force F squared to vanish, contrary to
the active Green guard F != 0.

## Coverage and prohibited promotions

The accepted predecessor set contains the 128 triples

    (s;7,a,b),   s in {1,2}, a in {8,...,15}, b in {16,...,23},

plus the separately accepted stage-1 triple (8,9,11). The source coverage file
was compared with the full exact 128-element set. The new tuple (1;8,9,10) is
distinct from all 129 existing cases. The accepted union is therefore

    130 of C(34,3)=5,984 coordinate triples,
    leaving 5,854 coordinate triples unclassified.

The accepted 34 circles, selected cross-stage pair, and all 561 pairs are
unchanged and are not counted again as three-dimensional coverage. The earlier
constant-template obstruction added zero triples; this affine exclusion adds
exactly one now.

No other consecutive triple, no additional nonconsecutive triple, and no
all-192-nonconsecutive-case theorem is accepted here. The combinatorial counts
224 same-Green triples, 32 consecutive triples, and 192 nonconsecutive triples
do not provide exclusion certificates. No symmetry transfer is established.
Different witnesses, nonunit internal gains, a free interstage diagonal, other
N, four or more moving phases, and the full 34-phase Fourier fiber remain
outside this review. The full fiber and construction remain OPEN. No runtime,
novelty, priority, or unrestricted synthesis claim follows.

## Reproduction and disposition

Run `python review_affine.py` in this review directory with Python 3 and SymPy.
It reads the included sealed candidate archive and predecessor data snapshots
as inert bytes. CHECK_RESULTS.json records the full independent checks;
DECISION.json records this bounded acceptance. The fresh-directory rerun is
recorded in REPRODUCTION_CHECK.json. MANIFEST.json binds the final review files;
SEAL.json names and hashes the final review archive.

**ACCEPT exactly the pinned stage-1 (8,9,10) exclusion and the minimal affine
degree conclusion described here. No mathematical or scope repair is required.**
