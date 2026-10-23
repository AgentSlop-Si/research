# ALG-009: three raw ratios remove the specialized linear-gcd gate

Candidate, 23 October 2026 UTC. Independent acceptance is pending. This is a
strict enlargement of the Phase20 resultant selector's guaranteed family, not
complete coverage of all fixed-grid models, historical novelty, or an FFT
speedup. No historical research program was executed.

## 1. Exact source and unchanged target

The original Phase20 theorem is `sources/THEOREM.md`, 9,788 bytes, SHA-256
`b49a3863273c2c80cb211e71711d0575cd3ac96bac32f4ac293f48a77b0f7ec9`.
It was read from the preserved 9,679,918-byte Phase20 archive, SHA-256
`c20b633a0e8a7be1ee81ab65765a15e3fb77a39d3315c7139cef5d88aa1333c3`.
The static corrected gate, fetched at repository commit
`1dadcbac912a22c88ad0950bc0488978b5bf919d`, is
`math/finalized/2026-10-16-source-repairs-0126/alg009_static/corrected/resultant_gate.py`.
Its 9,201 bytes, copied as text here, have SHA-256
`09ef37694af956394b82f55bf366e121849cbaf7f4d89caff5527aad9a142ef4`.
It skips every candidate whose specialized monic gcd is not degree one.

The accepted fixed-root-grid comparison v2 is bound by report SHA-256
`521efc5a7291d062862246ed16d5e4448e75a13ac32e810b10e9665051bfbedf` and
independent-acceptance SHA-256
`a949b4629cddf70b1b2f224d14f89fe8bc4425adeb8e6a35c69705eda981a897`.
Its canonical archive hash was checked. Fresh native overview B52:Q52 still
records ALG-009 TO RESEARCH, priority 42, with coverage and paid execution open.
The current repository finalized tree was traversed recursively (7,611 entries,
not truncated), and the reviewed-results directory checked; no later named
ALG-009 recovery packet was found there. This is a scoped duplicate check, not
an exhaustive historical-priority search.

Keep the original concrete domain: a supplied certified prime p>55, N>=8,
and supplied omega of exact order N in F_p. In particular N is nonzero in F_p.
Input and output are explicit length-N vectors with canonical field-element
representations, not oracle access or compressed output. Define

    R_k = sum_(j=0)^(N-1) r_j omega^(kj),
    h_j = r_j - alpha r_(j-delta mod N).

An admissible relation has 1<=delta<N, alpha!=0, exactly one or two nonzero h_j,
and at most one grid zero of 1-alpha omega^(k delta). Zero-defect descriptions
are not admitted. No oracle evaluations outside the fixed grid are provided.

Compute and pay for the same eight samples R_0,...,R_7 as the original gate.
Set Y_k(a,w)=R_k(1-a w^k) and

    P_u(a,w)=det(Y_(u+i+j)(a,w))_(i,j=0)^2,  u=0,1.

Let T(w) be the same six-by-six Sylvester determinant of the two cubics in a,
padded to degree three. No factor is canceled and no minimal polynomial is
substituted. The remaining nondegeneracy hypothesis is exactly T not identically
zero. Only the linear-specialized-gcd hypothesis is removed.

## 2. The inherited resultant facts, including degree drops

For an admissible relation, Y_k(alpha,omega^delta) is the Fourier transform of
h, hence a sum of at most two exponential sequences. Both 3-by-3 Hankel
determinants vanish. A common finite root alpha makes the padded Sylvester
matrix singular even when either specialized cubic drops degree: evaluation
at alpha is a nonzero functional annihilating the image of the linear map

    (U,V) -> U P_0 + V P_1,  deg U,deg V <=2,

from a six-dimensional space to polynomials of degree at most five. Thus
T(omega^delta)=0. No converse is asserted.

For each determinant term the three Fourier indices sum to 3u+6. Therefore
deg_w P_0<=6 and deg_w P_1<=9; homogeneity of the padded determinant gives
deg T<=3*6+3*9=45. If T is nonzero, there are at most 45 distinct candidate
shifts because omega^d, 1<=d<N, are distinct. These are inherited source facts,
not claimed as new here. They allow leading-degree drops, multiple common
alpha roots, zero specialized polynomials, and repeated roots of T.

## 3. A support consequence of T not identically zero

If r has at most two nonzero coordinates, its sequence R_k is a sum of at
most two exponential sequences. At a=0, each P_u(0,w) is the corresponding
Hankel determinant of R and vanishes identically in w. Thus a divides both
P_0 and P_1 in F_p[w][a]. Over F_p(w), their padded Sylvester determinant is
zero, so T is the zero polynomial.

Consequently T!=0 implies that r has at least three nonzero coordinates.
This is a deduction from the existing hypothesis, not an additional input
restriction. It also explains why sparse inputs are handled by the explicit
zero-resultant decline, not by a hidden extra recovery promise.

## 4. Three-ratio coverage lemma

Choose any three distinct indices i_1,i_2,i_3 with r_(i_t)!=0. The same three
indices can be used for every shift. For a candidate d propose

    a_t(d) = r_(i_t+d mod N) / r_(i_t),  t=1,2,3.

For a true admissible (delta,alpha),

    a_t(delta)-alpha = h_(i_t+delta mod N) / r_(i_t).

Translation by delta is bijective, even when gcd(delta,N)>1. The three target
indices are distinct and h has support size at most two. At least one of the
three displayed right sides is zero. Hence one proposal equals true alpha.

This argument concerns relation defects h, not corrupted observations of r.
A raw coordinate may occur in several pairs or be both a numerator and a
denominator; this changes nothing about the displayed identity. There are at
most two bad *target equations*. Nonzero anchor values make every division
legal. A zero numerator gives candidate zero and may be rejected, but the
guaranteed clean ratio cannot be zero because true alpha is nonzero. Repeated
proposal values, repeated/short-period input patterns, noncoprime shifts and
overlapping coordinate positions require no further assumption. The argument
also works with one defect; its stated three proposals preserve the two-defect
uniform bound.

## 5. Complete deterministic nonzero-resultant recovery

The executor is fully specified in `paid_executor.py` and its operation ledger.

1. Construct and check the supplied root table, then compute the eight direct
   Fourier probes. Recover T by 46 fixed-field evaluations and direct Lagrange
   interpolation at 0,...,45. These nodes are distinct because p>55.
2. If T=0, explicitly decline. Otherwise evaluate T at every omega^d,
   1<=d<N, and retain the at most 45 zero positions. Index recovery is this
   scan itself; no discrete logarithm or extension-field root solver is used.
3. Find three nonzero raw entries once and invert their values once. At each
   retained shift try the three ratios above, including every failed attempt
   in the aggregate budget. Reject alpha=0.
4. For each nonzero candidate, scan the raw relation. Reject as soon as three
   defects are found; accept the support count only after the entire scan
   confirms exactly one or two. Then scan all N denominators to count actual
   poles and reject if there is more than one. A degree-one gcd and the
   extra two Hankel-filter checks are unnecessary: raw certification is
   stronger. Omitting them does not omit any output or soundness obligation.
5. For the first admissible full certificate, evaluate its one or two defect
   streams on every grid point. Divide at every nonpole; compute each pole
   value by its own paid direct Fourier sum from the original r. Return all
   N coordinates. If no candidate is certified, decline with all work charged.

**Theorem.** For every input in the supplied-prime-field/supplied-root domain
with T!=0 and at least one admissible relation, this procedure returns the
entire exact F_N r within at most 45 shift roots and 135 raw-ratio proposals,
using O(N) field operations and O(N) field-element storage. Its deterministic
fast-recovery probability is one on this stated family. For arbitrary raw r,
any accepted output is correct; a decline does not assert model absence.

**Proof.** The true delta is included by Section 2. Three anchors exist by
Section 3, and Section 4 supplies its true alpha within three proposals.
That proposal passes the exact original support and pole policies. Every
earlier accepted proposal is also correct by Fourier shift diagonalization:

    F_N h = diag(1-alpha omega^(k delta)) F_N r.

Division recovers nonpoles, and raw direct sums recover the remaining at most
one coordinate. All stages have the bounded schedule in the ledger. No
random success event, unbounded restart, genericity assumption, or unknown
degree search is hidden. QED.

The pole-count formula remains Z=g when alpha^(N/g)=1 and Z=0 otherwise,
where g=gcd(N,delta). The executor uses a complete denominator scan instead
of that exponentiation test, so it handles the original noncoprime zero-pole
cases without the old over-rejection and still rejects every multipole
candidate. Cancellation of H/Q is never used to guess a pole value.

## 6. Exact strict-extension witnesses

The primary witness has N>8, so eight probes are not the full output. Take
p=97, N=16, omega=8, and

    r=(80,4,42,70,52,22,69,18,30,50,51,85,77,96,63,8).

For delta=1 and alpha=34, h_0=2,h_2=3 and all other defects vanish. There are
no poles. T(2)=46 and the only nontrivial subgroup roots are d=1,15, with
specialized monic gcds a^2+75a+77 and a^2+69a+63. Both are quadratic, so the
historical linear-gcd selector declines all shift candidates. The new gate
finds alpha=34 from r_1/r_0 and returns

    F_N r=(41,0,22,23,10,94,75,18,14,0,67,75,18,40,51,53).

The independent reviewer supplied this witness, and the author's separately
authored controls recomputed it. `STRICT_EXTENSION_WITNESS_N16.json` contains
its full original resultant and old-selector data. The N=8 witness below is
retained as an additional exact control, not the main public example.

Take p=97, N=8, omega=64 and

    r=(65,9,49,62,28,77,42,67).

For delta=1 and alpha=27, h has values h_0=2,h_4=3 and is zero elsewhere.
There are no poles. The exact original padded resultant satisfies T(2)=78.
Its only nontrivial subgroup roots are d=1,7. Their monic specialized gcds are

    d=1: a^2+57a+60,
    d=7: a^2+64a+76.

Thus the original linear-gcd selector declines every shift, even after the
accepted resonance-guard correction. The new selector obtains 27=r_1/r_0
and returns

    F_N r=(11,51,26,43,66,40,75,14).

`STRICT_EXTENSION_WITNESS.json` contains all 33 resultant coefficients, the
two specialized gcds, and the exact output. New independent-control code
computed this data without importing any historical code. Its old-selector
comparison is a mathematical reimplementation, not a source execution claim.
Independent review can verify the witness directly against the stated
definitions. The strict extension is project-gate coverage, not a claim that
the underlying elementary ratio method is historically new.

## 7. Original x input and Green wrapper are not discarded

The original theorem uses L=7I+2S+D, P=7I+S+2D^(-1), with LF_N=F_N P.
For original x, first pay for r=P x. On the unchanged constructor domain,
pay setup and L solve to recover y=L^(-1)F_N r=F_N x. As the historical audit
requires, all source-inverted diagonal entries and cyclic solve factors
must be nonzero; invertibility alone does not suffice for that constructor.
The new raw-r gate does not silently relax those guards or assert that a
given Nth root supplies the historical fallback's additional roots.

The primary N=16 witness has the original-input lift

    x=(19,18,6,6,4,12,34,88,66,12,33,35,75,56,64,6),
    F_N x=(49,84,28,19,86,60,86,94,68,39,7,60,65,74,0,67).

Here P x is the N=16 r above, all L/P diagonal entries are nonzero, and
det(L)=det(P)=71 in F_97. Explicit diagonals and cyclic factors are in the
control output. The source-defined Green construction is therefore valid
at this supplied root, independently of any default root-generator choice.

The N=8 witness also has an original-input lift, independently checked
with exact dense linear algebra solely as control work:

    x=(23,45,13,2,44,13,31,52),
    P x=r,
    F_N x=(29,4,14,36,96,35,32,35).

The P diagonal is (9,4,60,73,5,10,51,38), the L diagonal is
(8,71,29,57,6,40,82,54), and all entries and both cyclic factors are nonzero.
This binds the strict extension to the original supplied-root mathematical
model. It is not execution of historical GreenSparse: its default generator
31 would choose a different root over F_97. No default-generator equivalence
or nine-module source validation is claimed.

## 8. Predecessor overlap and the full-hybrid boundary

A targeted static audit of `PHASE19_THEOREM.md`, `blind_discovery_static.txt`
and `hybrid_phase20_static.txt` is essential to the claim's scope. The older
Phase19 bounded-defect detector already obtains alpha at a candidate shift
by a five-edge raw-ratio majority for K=2, assuming nowhere-zero raw entries.
It discovers shifts through adjacent-ratio classes and subset counts, with a
proved guarantee under coprimality and wrap-class separation. Therefore raw
ratio recovery at a known shift is an existing project ingredient, not new
here. This note replaces majority identification with three list proposals,
chooses nonzero anchors to handle raw zeros, and combines that elementary
certificate mechanism with the original at-most-45 resultant shift list.

In fact the N=16 witness above has adjacent-ratio counts 14,1,1. The old
subset-count list includes u=1 and hence delta=1; its five-edge majority
recovers alpha=34. The earlier Phase19 ratio branch accepts this witness.
The N=8 witness similarly has adjacent-ratio counts 6,1,1 and is also accepted
by that earlier branch. The historical hybrid tries it before the
inverse/resultant gates. Thus both witnesses are strict against the Phase20
linear-gcd selector only,
NOT evidence of additional full-hybrid accepted inputs, nor of a runtime
improvement to the old hybrid on this input. No such claim is made here.

Phase19 Theorem C instead assumes a sparse circular inverse C(S)r=e_0, which
forces every R_k to be nonzero; it does not cover arbitrary two-defect
relations. The separate `blind_sparse_rational_static.txt` also uses a
degree-one specialized gcd. The inspected Phase19 theorems do not state the
same full nonzero-T recovery
guarantee, but absence of that statement does not prove that the logical
union of the existing branches has smaller coverage. That comparison remains
unestablished. The bounded result here is a simpler complete guarantee for
the nonzero-resultant branch and removal of its named linear-gcd obligation,
with a fully paid proposed executor. It is an integration/coverage theorem,
not novelty of its algebraic ingredients or a new discovery count.

## 9. Remaining frontier

The zero-resultant family remains uncovered by this gate. This is one removed
nondegeneracy condition, not recovery of every one/two-defect fixed-grid input.
The exact-theorem comparison to external interpolation literature, historical
priority, full historical implementation execution and literal operation
ledger, early-hybrid N>=8 correction, and extra-root fallback domains stay
separate and open. The new executor keeps N>=8 and p>55. Its optional direct
fallback is paid O(N^2); it does not claim the historical O(N log N) fallback
without the latter's additional resources and validation.

No Prony, root enumeration, field construction, bit complexity, floating-point
stability, constant-factor speed advantage, generic FFT improvement, owner
closure, discovery-count change, or novelty clearance follows from this
bounded extension. ALG-009 remains TO RESEARCH, priority 42.
