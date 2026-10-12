Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: 2ca592c6c64ed4c930ffc8db06a8cd1c28125313e51b8d1e557b1b98740e926f

---

# Independent review: Q27 one same-Green triple

Date: 11 October 2026 UTC.
Verdict: ACCEPT, for the single bounded slice stated below.

## Accepted result and exact scope

In the pinned N=8 Phase42 chart M=S2*S1, each stage is the unweighted sum
of three weighted-cycle Green inverses. Vary exactly stage-1 edges 8, 9,
and 11 over the unit circle, and freeze the other 31 free phases at the
accepted rational-Gaussian witness. Every Green inverse must exist. There
is no independent interstage diagonal.

There is no point of this admissible slice equivalent to F8 by arbitrary
invertible complex external row and column monomials. The same necessary
modulus obstruction excludes equivalence to any nonzero constant-entry-
modulus matrix.

This adds exactly one new coordinate triple to the accepted 128 same-stage
one-edge-per-Green triples. The accepted union therefore contains 129 of
5,984 coordinate triples, leaving 5,855 unclassified. The accepted 34
coordinate circles, selected cross-stage pair, and all 561 pairs remain
unchanged. Their lower-dimensional coverage is not counted again as
three-dimensional coverage.

This review does not accept the author's other 191 promising modular
same-Green cases, any of the 32 consecutive modular cases, any other frozen
witness, four or more moving phases, nonunit internal gains, a free
interstage diagonal, another N, or the full 34-phase Fourier fiber. It
makes no construction, synthesis, runtime, novelty, or priority claim.
The full fiber and construction remain OPEN. No Sheet or GitHub write
was performed.

## Immutable input and predecessor binding

Frozen candidate:
Q27_One_Same_Green_Triple_Author_Candidate_2026-10-11.zip
1,351,082 bytes; SHA256
29a6534d6f65443ab90a40529d59d8c7959ae233d4d1c8a44864e8f86e735b75.

The candidate report SHA256 is
eb97dd51542034c8d428394fde27f7f5142c9b20f1dd689e5e867f0a78b85671.
The exact coefficient data SHA256 is
30c02a278c94359fe2f67b9e0711864ebfc9261977f31b78bdbd20a77f77fd1b.
The exact certificate weights SHA256 is
2cf268f4baf1b258ddea9c10f4c51afc3de8634b1e5957d8b3ce6d6c955c6a16.

All 24 candidate-manifest members were independently byte/hash checked.
All 16 named source bindings were independently checked against available
source bytes. Preserved snapshots and INPUT_BINDINGS.json bind the chart,
all author/reviewer/verdict predecessor records, and the author's queue
snapshot. The latter is source context, not a newly fetched live queue.

The unchanged chart SHA256 is
5528afbbd5b4008a5e0f79043870e72a613e0fd421288d2ce1e5dbffee1c9e98.
The original single-sum exclusion belongs to a different model. The product
predecessors cover the 34 circles, selected pair, all 561 pairs, and exactly
128 triples (s;7,a,b), where s=1,2, a=8,...,15 and b=16,...,23. The new case
(s;8,9,11), s=1, belongs to none of those accepted triple indices.
Predecessor mathematical results are inherited from their accepted reviews;
this review does not claim to rerun every predecessor proof.

Original candidate and predecessor programs were never executed, imported,
compiled, or evaluated. The included original archive remains byte-identical
and inert. The only research program executed was freshly written
independent_review.py, using Python's standard library. It reads chart,
coefficient, weight, selection, and proposed kernel data as untrusted data.
A separate fresh coverage_check.py verifies the finite counting.

## Independent direct-inverse construction

The reviewer reconstructs Gaussian gains as
(a^2-b^2+2ab*i)/(a^2+b^2), checks every unit norm exactly, preserves the six
cycles and destination-index edge convention, and verifies all six witness
holonomies are nonzero unit elements different from 1.

Edges 8, 9, 11 are respectively destination positions 0, 1, 3 of the second
Green branch of stage 1. Their gains are multiplied by x,y,z. Multiplication
by the three frozen unit gains bijectively identifies these relative
variables with the requested absolute unit-phase coordinates. The other
31 free gains and 14 tree-pinned edges do not move.

Let h be the witness holonomy of that branch. Independently reconstructed,

h = (-383187819337037874577 + 235291331868842780736*i)
    / 449660889716782337425,
F = 1-h*x*y*z.

The five fixed inverses are obtained by exact Gaussian elimination on
I-W, with two-sided inverse and determinant checks. Let K be the product
of their five nonzero guards. Let C1 be the sum of the two fixed stage-1
inverses and S2 the fixed stage-2 sum.

For the moving branch the reviewer directly inverts I-W at the eight tensor
nodes (x,y,z) in {0,2}^3, multiplies each inverse by F, and interpolates a
triaffine polynomial matrix B. Every node guard and determinant is checked.
These algebraic nodes are reconstruction controls; zero is not an
admissible phase.

Interpolation is not assumed to be a global formula. The reviewer verifies
coefficientwise in Q(i)[x,y,z] that

(I-W)B = B(I-W) = F*I.

This proves B/F is the actual Green inverse wherever F is nonzero. It is
independent of the author's directed-path numerator construction.
The product numerator is then independently formed as

N = K*S2*(B+F*C1), so N = K*F*M.

All entries are triaffine. This retains the candidate normalization
Delta=K*F, and multiplication order S2*S1. No extra gauge freedom or
interstage diagonal is used. Pinning seven edges in each stage defines
the chart under review; this is not a proof about all unnormalized products.

## Necessary modulus equations, conjugation, and poles

If invertible external complex row/column monomials turn M into F8, the
squared entry moduli of M factor into positive row and column factors.
The array consequently has rank one. Permutations preserve that property,
so every anchored defect

|M[r,c]*M[0,0]|^2 - |M[r,0]*M[0,c]|^2

vanishes for 1<=r,c<=7. This is necessary only. It divides by no matrix
entry, assumes no density, and does not assert Fourier sufficiency.

For a triaffine N define Ntilde=xyz*bar(N)(1/x,1/y,1/z), where the bar
conjugates Gaussian coefficients. The reviewer constructs the 49 exact
polynomials

P_rc = N_rc*N_00*Ntilde_rc*Ntilde_00
       - N_r0*N_0c*Ntilde_r0*Ntilde_0c.

On the unit torus these equal (xyz)^2*|Delta|^4 times the anchored defects.
This is because reciprocal unit variables equal their complex conjugates.
The multiplier is nonzero on the admissible locus. No such interpretation
of conjugate-reciprocal equations is claimed for nonunit variables.

The reconstructed P all divide exactly by F. Constant-term recurrence
computes Q=P/F in the full cubic box, then full polynomial multiplication
checks F*Q=P for all 49 rows. Hence this divisibility is established in
characteristic zero directly, without lifting modular factorization or
relying on numerical vanishing on a pole.

The union of exact quotient supports has 44 monomials. All 2,156 stored
coefficient entries match the frozen candidate, and the 980 cubic-box slots
outside the union are exact zeros. Coefficients beyond the cubic box are
also controlled by the full multiplication-back identities.

Admissibility requires |x|=|y|=|z|=1, the five fixed guards, and F!=0.
The pole x=bar(h), y=z=1 is an actual singular moving inverse, confirmed
by direct elimination. It is rejected, never counted as a feasible point.

## Exact certificate and independent rank proof

The 42 supplied weights are read solely as exact rational pairs. Direct
summation against the independently reconstructed Q coefficients verifies

sum(j=0,...,41) c_j*Q_j = F

at all 44 coefficient positions, including columns 42 and 43 that were not
used in the author's square solve. The reviewer also separately forms the
weighted polynomial sum of the reconstructed P rows and verifies

sum(j=0,...,41) c_j*P_j = F^2.

Every selected row is one of the necessary 49 windows; the order is
r=1,...,6 and c=1,...,7, row major. If all necessary equations vanished at
an admissible point, the identity would give F^2=0, contradicting F!=0.
Equivalently, for I=<P_rc> and s=xyzF, s^2 belongs to I and I:s^infinity=(1).
This exact identity alone establishes the exclusion; the rank calculation
is independently checked supporting information.

For the upper rank bound, two proposed right-kernel vectors are extracted
from inert candidate RREF data. All 98 row/vector products are independently
verified exactly against the reconstructed 49-by-44 matrix. The final two
coordinates of the vectors are (1,0) and (0,1), proving independence.
Their full exact values are preserved in EXACT_RIGHT_KERNEL.json. Therefore
the exact rank is at most 42; the RREF assertion is not accepted merely
because it was supplied.

For the lower bound the reviewer reduces the exact coefficient matrix in
both Gaussian embeddings at each of the verified primes 1,000,000,009 and
998,244,353. Every rational coefficient denominator is explicitly checked
nonzero before reduction. A fixed 42-by-42 minor is nonzero in all four
reductions, with determinants 483883156, 268213964, 968718056, 63965540,
respectively. These are images of the actual exact rational minor, so its
nonzero residue proves exact rank at least 42. Combined with the independent
kernel identities, the rank is exactly 42. No finite-field rootlessness or
scouting rank is promoted to a characteristic-zero feasibility result.

## Fresh controls and limits of their meaning

The fresh program checks 640 fixed-inverse scalar identities, 1,024
reconstruction-node inverse identities, 128 global polynomial matrix-entry
inverse identities (3,456 full degree-box coefficient slots), and all 49
polynomial division/multiplication identities.

Four fresh triples, distinct from the author's points, are used:
(-i,i,-1);
((20+21i)/29,(7-24i)/25,(-15+8i)/17);
((9+40i)/41,(-28+45i)/53,(12-35i)/37);
(3,-2,7).

All six inverses receive exact two-sided/determinant checks at each point.
These provide 3,072 additional inverse-entry identities and 256 direct
numerator comparisons. The three unit points provide 147 comparisons with
actual complex squared-modulus defects. The nonunit point checks algebraic
identities only. These tests are redundant controls, not finite searches
substituted for the exact proof.

Fresh adverse controls:
- Add 1 to each unselected target coefficient in turn: index 42, exponent
  (3,3,2), and index 43, exponent (3,3,3). The all-column checker detects
  exactly the altered coefficient in each case.
- Change the first certificate weight by 1: the exact identity fails.
- Remove coefficient conjugation from reciprocal reversal: all 49 windows
  disagree at the fresh rational unit point.
- Duplicate a row in each selected modular minor: the full-rank check fails.
- Attempt to invert the actual Green pole: exact elimination rejects it.

The independently enumerated triple partition is 224 same-Green, 1,008
same-stage two-plus-one, 128 same-stage three-Green, and 4,624 split-stage.
Only one member of the 224-case class is accepted here. The author's
192-versus-32 modular scouting summary is left as author scouting; it is
neither rerun nor promoted by this review.

## Disposition

ACCEPT these frozen candidate bytes for exactly stage 1 edges (8,9,11),
with all other free phases frozen, unit phases, all six Green guards,
external invertible complex monomials, and no free interstage diagonal.
No material repair is required. The next mathematical gate is another
separately certified same-Green triple or a proved structural coefficient-
space theorem that justifies multiple cases. The full fiber remains open.
