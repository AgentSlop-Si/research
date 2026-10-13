# Independent ACCEPT: Q27 comparison slice (stage 2; edges 8, 9, 12)

## Decision

ACCEPT the submitted z-affine coefficient certificate for exactly the source-bound,
original guarded unit-complex slice (2; 8, 9, 12). The candidate archive SHA-256 is
1286e65362e4b67165291ab62b8d2d175a353853de73c92d2812b964a8c9af69.

This is an independent certificate check, not a replay of the author's checker.
Only the new independent_check.py was executed. No candidate or historical Python
program was executed, imported, evaluated, or used as a library. Their bytes were
read solely as archive members when verifying manifests. The historical inert
source definitions were read as specifications for reconstruction.

All 49 original defects, 64 full numerator entries, six original guards, frozen
48-gain witness, and all normalized quotient coefficients match reconstruction.
Both requested identities pass literal coefficient comparison over Q(i):

  sum_j (a_j + z b_j) q_j = d H f,
  sum_j ((a_j + z b_j)/c_j) P_j = d H f^2.

The second accumulation uses all reconstructed original P_j directly; it is not
inferred by multiplying the first result by f. The first accumulation considers
58 monomials and the second 82, including coefficients that must cancel to zero.
No selected solver rows, numerical samples, modular ranks, or hashes substitute
for these complete characteristic-zero checks.

The 56 stored nonzero terms comprise 42 z-linear and 14 constant coefficients.
Their Gaussian-integer numerators, exact positive common denominator d, and exact
positive contents c_j were checked. The common denominator has 5,368 decimal
digits, with gcd(d, all real and imaginary numerators) = 1. The largest stored
scalar has 17,830 bits. There are 2,821 original-polynomial and 1,932 normalized-
quotient nonzero coefficients.

## Reconstruction and the original model

The pinned chart has N = 8, two stages, three branches per stage, coefficient 1 on
each branch, and product order M = S2 S1 with S_s = G_s0 + G_s1 + G_s2. For each
cycle, edge 8b+j sends cycle[j-1] to cycle[j]. G_sb = (I-W_sb)^(-1).

The spanning forest is re-created independently using connected-component sets,
not the source disjoint-set function. In each stage edges 0 through 6 form the
tree, and the remaining 17 edges are free coordinates. The two stage seeds 42420
and 42520 reconstruct all six cycles and all 34 Gaussian pairs. A free witness
gain is (a+ib)/(a-ib); all 48 edge gains are verified to have modulus 1. Moving
variables x,y,z multiply only stage-2 edges 8,9,12. The other 31 free phases and
all tree gains remain frozen. No diagonal conjugation, interstage matrix, branch
weight, product-order change, or alternative witness enters the accepted model.

All six guards are retained separately:

  1-h10 != 0, 1-h11 != 0, 1-h12 != 0,
  1-h20 != 0, f = 1-h21 xyz != 0, 1-h22 != 0.

For an eight-cycle matrix, only the identity and full-cycle permutations
contribute to det(I-W), so det(I-W) = 1 minus the product of the eight gains.
Every h_sb is independently re-created from the eight edge gains. The five
inactive guards are separately checked nonzero constants. For the active branch,

  h21 = (-4335586066535028372496 + 1298149621513208810103 i)
        / 4525759492081695535625,
  H = 4525759492081695535625 > 0.

Sparse polynomial matrix powers independently establish W21^8 = h21 xyz I.
With B = I + W21 + ... + W21^7, both (I-W21)B and B(I-W21) equal f I.
The same two-sided finite-power identities are verified for every other branch.
Consequently, on the original guarded domain,

  n = (B + f(G20+G22)) S1 = f M.

The least positive integer clearing all real and imaginary coefficient
denominators of n is independently recomputed as

  S = 47657433783260301946927308623286197903901526077573294125500000.

All entries of N = S n are Gaussian-integral and triaffine. Every coefficient of
all 64 entries agrees with the candidate's frozen original numerator.

## Original equations and exact normalization

Define the coefficient-conjugate reversal entrywise by

  Ntilde(x,y,z) = xyz conjugate(N)(1/x,1/y,1/z).

Here conjugate(N) conjugates coefficients. All 49 anchored defects are rebuilt,
for 1 <= r,c <= 7, with the original anchor (0,0):

  P_rc = N_rc N_00 Ntilde_rc Ntilde_00
         - N_r0 N_0c Ntilde_r0 Ntilde_0c.

The sparse polynomial division algorithm independently divides each P_j by f,
checks zero remainder, computes its positive rational content c_j, and normalizes
the result to a Gaussian-integral primitive q_j. Multiplication back verifies
P_j = f c_j q_j for every j. All original and quotient coefficients agree with
the freeze. This normalization introduces only nonzero rational scalar divisions;
no original guard, variable, matrix entry, or anchor is divided out.

## Why this proves the accepted exclusion

Assume x,y,z have unit complex modulus and every original guard is nonzero.
Reciprocal variables then equal their complex conjugates, so evaluated Ntilde is
xyz times the ordinary complex conjugate of evaluated N. Therefore

  P_rc = S^4 (xyz)^2 |f|^4
         (|M_rc M_00|^2 - |M_r0 M_0c|^2).

Suppose M were obtained from a matrix whose entries all have the same nonzero
modulus by invertible complex row and column monomial operations. After row and
column permutations, each squared entry modulus is a positive constant times a
row factor times a column factor. Every 2-by-2 squared-modulus minor, hence each
of the 49 displayed anchored minors, is zero. This necessary condition applies
in particular to external monomial equivalence to F8. Thus all P_j would vanish.

The directly checked original-polynomial identity then gives d H f^2 = 0. Since
d > 0, H > 0, the field has characteristic zero, and the original active guard
requires f != 0, this is impossible. This proves exclusion of the one nominated
guarded unit-torus slice. No sufficiency claim for the anchored minor equations
is needed, and no additional matrix-entry nonvanishing assumption is imposed.

Algebraically f^2 belongs to the ideal of the 49 original polynomials over Q(i).
This ideal becomes the unit ideal upon localization at f, and consequently on the
domain localized at xyz and all six guards. The algebraic identity remains valid
in characteristic-zero field extensions. The modulus/Fourier interpretation above
specifically uses unit-complex moving gains and ordinary complex conjugation.

## Exact direct-matrix corroboration and pole

The checker independently Gaussian-eliminates every original I-W_sb at the
frozen witness (x,y,z) = (1,1,1), and at two additional exact rational unit triples:

  ((3+4i)/5, (5+12i)/13, (8+15i)/17),
  ((20+21i)/29, (-7+24i)/25, (9-40i)/41).

For all 18 inverses it verifies determinant = the corresponding original guard
and both inverse multiplication orders. At each triple it checks all 64 entries
of N = S f M and all 49 exact complex-modulus bridges. The certificate target is
nonzero at all three points. These checks supplement the polynomial proof.

The point (1,1,conjugate(h21)) lies on the unit torus, has f = 0, and keeps all
five inactive guards nonzero. Independent elimination detects singularity of its
original active I-W21. The cleared target d H f^2 vanishes there. This actual
Green-inverse pole is excluded by the original model; denominator clearing does
not admit it, and the certificate is not an unguarded claim.

## Negative controls

All 18 controls pass. Full exact nonzero residual witnesses are retained in
results/NEGATIVE_CONTROLS.json for the 13 coefficient/model corruption controls:

- Add 1 to a nonzero multiplier's real numerator
- Omit one nonzero multiplier
- Replace d by d+1
- Replace target f^2 by f
- Reverse the target sign
- Change one content denominator by 1
- Inject unsupported x^9, y^9, or z^9 coefficients separately
- Omit coefficient conjugation when rebuilding all 49 defects
- Reverse stage multiplication and rebuild all original polynomials
- Change the third moving edge to 11 and rebuild the complete wrong model
- Move the variables to stage 1 and rebuild the complete wrong model

Byte/scope controls separately reject candidate-byte and chart-byte mutations,
a wrong-stage label, and a missing guard. These four are identified as binding
controls, not presented as wrong-model polynomial computations. The eighteenth
control is the exact singular-original-inverse test at the active pole.

## Source, freeze, and coverage audit

Every manifest member's size and SHA-256 is verified in the candidate archive,
its accepted-193 archive, and that archive's original author input. Member paths
are unique and safe, manifest paths are unique, and the manifests cover exactly
all remaining members. The accepted input, chart, ledger, and three inert source
snapshots are bound by hashes recorded in results/VERDICT.json.

The frozen input and contract are bound by their full byte hashes both in the
certificate and in the zero-solve freeze receipt. Their complete mathematical
contents are independently reconstructed. The archive records a pre-solve freeze,
but the archive alone cannot independently prove its wall-clock creation order.
This limitation does not affect the checked certificate or its exclusion proof.
No historical-source authenticity, canonical repository state, author identity,
freshness of discovery, minimal degree, solve-count, modular-rank upper bound,
or independent recovery of historical programs is claimed. The pinned inert
snapshots supply the model definition and retain their inherited provenance limit.

The pinned accepted-193 ledger is independently checked as a duplicate-free union
of the 192 inherited source labels and (2;8,9,11). The inherited 192-label set is
compared with its separately pinned source ledger. None equals (2;8,9,12).
The full three-coordinate label universe is C(34,3) = 5,984.

Only this new label is independently accepted here. Inheriting the prior accepted
193 proofs, which are not rerun in this review, the resulting union is exactly
194/5,984, leaving 5,790 labels unclassified. The union and its distinct labels are
serialized in results/COVERAGE_194.json. Label distinctness is not a classification
of overlaps among slices, and no other label is inferred excluded.

The full 34-phase problem remains OPEN. No full-fiber, all-route, other-witness,
other-architecture, historical-novelty, complexity, or speed conclusion follows.
No failure-to-find-certificate argument is used. No Sheet or GitHub write occurred.
