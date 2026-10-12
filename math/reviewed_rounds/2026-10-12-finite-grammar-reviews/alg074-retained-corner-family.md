Publication derivative of an independently reviewed research report. Private tracking and delivery details are omitted; source identity, exact finite scope, review method and open obligations are retained. Original source-report SHA-256: fa04612928d034e914191ff50669e97d0c1b373601b1e0e87f05354b908c5896.

# ALG074 independent retained-corner review

Date: 2026-10-12 UTC.

## Verdict and exact bytes

ACCEPT_BOUNDED_FINITE_47_BY_47_RETAINED_FAMILY for the complete explicit
rational matrix family at dimensions (23,25). The broader ALG-074 emitted-witness contract remains open; this acceptance does not resolve novelty or historical priority.

The accepted candidate is exactly
`ALG074_Retained_Corner_Full_Sweep_CANDIDATE_2026-10-12.zip`, 118,771 bytes,
SHA-256 `5804d6735d1fe8f76ee1f1a5a48b58b457dd358da4f9d83a987ac9f6689b7f8a`.
Its manifest SHA-256 is
`4cd163559bf133cec2be622d71a33a638528e87a9592f3efbd21e9dfac811ba8`.
All 18 payloads and complete manifest coverage are checked. All six source
pins have checked byte counts, SHA-256 and Git blob SHA-1; all four
scientific source identities are independently compared to the preceding
frozen packet. The other two files preserve LICENSE and NOTICE.

No original supplier program or downloaded binary was executed. Only the newly authored reviewer checkers and a cold
compilation of the reviewed fresh sweep were run.

## Result that is now closed

For all binom(23,3)*binom(25,3)=4,073,300 retained pairs, the literal matrix

M_ij=-1+x_(R_i)[R_i=C_j]+y_(i mod25)[i mod25=(528+j) mod25]

has the prescribed rightmost-pivot order. Here R and C retain the exact
duplicated middle labels and x/y retain their exact source-defined
two-valued rational weights. The profile consists of nine singletons,
one contiguous width-21 run and one contiguous width-17 run.

The complete statement comprises 191,445,100 nonzero rational pivots and
1,409,361,800 exact ordered-zero instances. The earlier ten-pair-only
limitation is superseded for this explicit finite matrix family only.

## Independent evidence

1. Independently reconstructed physical labels, both incidence spanning
   trees and every coefficient of the 2,209 matrix entries in the
   49-feature factorization. All 47 rank cuts were recomputed over Q:
   38 nontrivial feature-partition cuts and nine trivial suffix bounds.
   The proof in `EXACT_ZERO_PROOF.md` shows that these bounds force all
   346 ordered zeros for every weight assignment on which the preceding
   prescribed pivots exist. This is a universal exact zero proof.
2. Independently replayed all ten exceptional pairs using Fraction
   elimination, checking all 470 nonzero rational pivots, all 3,460 exact
   zeros and every first failed modular row. Three ordinary rational
   controls also pass. Incorrect offset and first-pivot-order mutations
   are rejected.
3. Audited the fresh exhaustive C++ implementation, including complete
   lexicographic triple enumeration, fixed row/column order, modular
   inverse recurrence, sparse Gaussian updates, exception retention,
   per-thread state and all integer bounds. Each product is at most
   1,000,004,000,004, safely below signed 64-bit range. Additions and the
   worst-case zero-error counter also remain within signed 32-bit range.
   Previously eliminated columns may retain stale stored values, but are
   excluded from every later active-column and ordered-zero operation.
4. Independently verified the optimized first-pivot Schur construction as
   a polynomial identity in all 48 weights on all 2,162 remaining cells.
   This covers every parameter choice; the optimization is not justified
   by sampling. Forty-five direct dense-matrix modular controls pass.
   All ten primary-prime exceptions still have full modular rank 47,
   demonstrating why full invertibility alone does not certify the
   prescribed intermediate pivots.
5. Bound the complete sealed sweep output to every one of the 1,771
   source count/product records, every exception and failure row, and the
   global counters. The fresh exhaustive sweep covers all 4,073,300 pairs;
   its 4,073,290 successful modular profiles plus the ten rational
   repairs cover the entire family. The author also supplied a final-byte
   full cold replay. The reviewer deliberately did not duplicate that
   entire exhaustive sweep, consistent with the split audit assignment.
6. Cold-extracted the immutable archive, cold-compiled its reviewed C++
   source at a different optimization setting, and ran a 2,300-pair pilot
   with one thread. Its complete pivot trace agrees with the sealed
   output. The reviewer separately reconstructed 6,900 direct dense
   matrices for first-triple indices 1, 247 and 1225, which differ from
   the author's direct-control indices. Every complete per-row pivot
   trace, count, determinant product and exception list agrees. The
   64-bit traces are diagnostics, not cryptographic proof or a replacement
   for source review and exhaustive coverage.
7. Replayed the exact cut and exception checker from the final archive's
   frozen source bytes and compared the complete result to the sealed
   candidate output. The prime 1,000,003 is deterministically proved by
   trial division, and all input denominators are eligible.

## Why the field argument is valid

Nonzero modular pivots lift inductively because initial denominators and
all preceding pivot denominators are units at the chosen prime. Each
rational Schur operation therefore reduces to the finite-field operation.
Zero residues are never lifted to rational zeros. The separate rank-cut
proof supplies all exact zeros, and all ten modular failures are handled
by exact rational arithmetic. No claimed probability of success is used.

The source counters include partial exceptional runs:

- 191,444,880 = 47*4,073,290 + 250 successful modular pivots
- 1,409,360,440 = 346*4,073,290 + 2,100 ordered-zero residue checks

Adding the exact repairs yields the complete rational counts stated above.
The contiguous runs are rows 1..21 / corner columns 25..45 and rows
28..44 / corner columns 2..18. Their physical last-bank columns are
553..573 and 530..546. No separated pivots are gathered.

## Boundaries that remain open

The literal label/offset binding is not a verification of the actual
575-dimensional tensor basis or controlled-permutation implementation.
The ambient width-481 child remains conditional on its separate tensor,
Schur and physical compiler interfaces. The present profile has total
width 47, not 528 or 575.

Also retain the open obligations for the original stacked h23/h25
serialized words, their complete dirty replay and paid reclamation;
missing width16 certificates; ordered-affine and complete-record
fixed-tape compilation; spectators, parked ancestors and base cases;
n-dependent eligible-prime/setup, copied-center and endpoint streams;
stock/layout/routing, bit and precision charges; exact recovery and a
common all-size threshold. No integer-multiplication complexity theorem,
FFT/exact-complex transfer, search optimality or priority promotion follows.

The PR34 assembly text remains an explicitly conditional historical
reference. Nothing in this review converts its imported geometric,
semantic or physical hypotheses into proved interfaces.

## Reproduction

Run `review_sealed_candidate.py` with the included candidate archive,
its exact SHA-256 above, and a new empty `--cold-root`. Python 3 and g++
with OpenMP are required. `audit_exact_cuts.py` and
`review_kernel_controls.py` also run independently. The sealed results
record every check; binaries and Python bytecode are not evidence payloads.

The accepted scope is the finite rational family described above. All broader geometry, source-availability and implementation obligations remain as listed in the preceding section.
