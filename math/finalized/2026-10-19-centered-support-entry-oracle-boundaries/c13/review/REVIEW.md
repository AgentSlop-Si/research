# Independent scoped review: C13 entry-oracle costing and adapter

19 October 2026 UTC.

## Verdict

**Accept the frozen candidate at its stated narrow scope. No mathematical or
implementation correction is required.** This accepts an elementary classical
unstructured-entry-oracle lower bound, its bounded-error extension, and the
tested exact Hamiltonian-route adapter contract. It finishes this scoped
costing/implementation gate. It does **not** accept whole-owner closure, a new
proof of the inherited iff theorem, unrestricted direction discovery, a Fourier
lower bound, an all-length construction, or a novelty/priority claim.

Candidate manifest SHA256:
`4a482ce24330b5083b7aab921ab0ee1516aa940addffc3b80ee5f62e44ce750b`.

All 17 sealed candidate files were hash-verified. The candidate was not edited.
The reported historical source provenance is retained as supplied; this review
does not claim a new external repository or spreadsheet read. The mathematical
source used for interface comparison is the accepted fixed-direction review,
SHA256 `052b4155a0737109131d4d668495be161d867e209c1dea5c27717e366a4d339c`.

The optional sharper observation in `OPTIONAL_STRENGTHENING.md` is separate from
acceptance of the frozen candidate. It is not needed to justify this verdict and
must not silently replace the candidate's stated theorem.

## 1. Deterministic and bounded-error query arguments

Let S = supp(U) union supp(V). Since U and V are invertible, each has a nonzero
determinant term. Consequently there are bijections f and g with
U[f(a),a] != 0 and V[b,g(b)] != 0. Their Cartesian product is a bijection on the
N^2 matrix coordinates. Exactly N^2-|S| pairs (a,b) map outside S.

For a feasible B0 and such a pair, replacing only B0[a,b] by B0[a,b]+delta gives
the off-support sandwich entry

    (U(B0+delta E_ab)V)[f(a),g(b)]
        = delta U[f(a),a] V[b,g(b)] != 0.

The equality uses the necessary off-support identity of the accepted theorem.
No converse is re-proved. Thus each pair supplies an infeasible target with a
one-entry difference. A deterministic algorithm that does not query that entry
has the same complete adaptive transcript on both inputs. This proves the
claimed lower bound on distinct queries on every feasible target in the stated
unpromised input class. Preprocessing U,V does not reveal the varying B entry.

For an invertible feasible B0,

    det(B0+delta E_ab) = det(B0)(1+delta (B0^-1)[b,a]).

There is at most one bad nonzero delta. A field with more than two elements has
at least two nonzero choices, so an invertible rejecting alternative exists in
the same field. The proof is valid for arbitrary fields of that size, not just
the prime fields implemented by the adapter. No extension field or numerical
genericity is being substituted. The field-size qualification is genuinely
needed by this particular perturbation step: a fresh F2 control exhibits a
feasible invertible target whose sole nonzero change at one forbidden
coordinate is singular. That control does not claim the whole lower-bound
statement is false over F2; it identifies the failure of this proof step.

For bounded error epsilon < 1/2, use the same random bits for B0 and a fixed
permitted alternative B_h. Until h is queried, the histories and decisions
coincide. Therefore the difference in acceptance probabilities is at most the
probability of querying h on B0. Correctness forces that difference to be at
least 1-2 epsilon. Summing the indicator expectations over the distinct h gives

    E[number of distinct queries on B0]
        >= (1-2 epsilon)(N^2-|S|).

Adaptivity, repeated queries, and random stopping do not invalidate the argument
for a correct decision procedure. Zero error gives the stated expected-query
special case. These are classical single-entry oracle statements. They do not
cover quantum, matrix-vector, batched, compressed, or symbolic input primitives.

### Dimension cross-check

The off-support condition defines the linear subspace

    W = {B : supp(UBV) is contained in S}.

The map B -> UBV is an invertible linear map on N-by-N matrices, so dim W=|S|.
At most |S| distinct coordinate units E_ab can belong to W, since they are
linearly independent. Hence at least N^2-|S| coordinate directions leave W.
This independently corroborates the matching-based perturbation count.

This use of dimension is legitimate because it counts independent coordinate
directions and then constructs same-transcript alternatives. Dimension alone,
without the entry-query indistinguishability argument, is not a query lower
bound. Any refinement using the smaller unrestricted-scale completion image is
kept in the optional supplement rather than promoted into the frozen theorem.

## 2. Legal nonzero-edge witness family

For the row-action Hamiltonian successor matrix P over Q and N>=3, the candidate
takes U=I-2P, V=I-3P, x=y=1, and B0=U^-1+V^-1. The two prescribed relative
routes are the same legal N-cycle. Every edge weight is nonzero; the base
coordinates are one. Cycle products 2^N and 3^N differ from one. The actual
union support has exactly 2N entries.

The commuting factors give

    B0 = (UV)^-1(2I-5P),
    det(B0) = (2^N-5^N)/((1-2^N)(1-3^N)) != 0.

Thus the candidate's N^2-2N query bound applies with the target-invertibility
promise and does not rely on zero edges. The displayed determinant formula is
valid for an N-cycle with the stated row-action convention. The separately
presented zero-edge example U=V=I is lawful only with the prescribed routes
retained; it does not authorize replacing them. Its nonzero scales require
lambda != 0,1, exactly as stated.

## 3. Adapter versus the actual source contract

The implementation agrees with the accepted source's **different** left/right
permutation orders:

    tau0(i) = r0^-1(r1(i)),
    tau1(i) = s1(s0^-1(i)),
    w0(i) = -b_i/a_i,
    w1(i) = -e_(tau1(i))/d_(tau1(i)).

Those formulas yield U=D_a(I-W0)P_r0 and V=P_s0(I-W1)D_d. The recovered plans
are P_r0^-1(I-W0)^-1 D_(x/a) and D_(y/d)(I-W1)^-1 P_s0^-1. Independent exact
dense reconstruction verifies both the order and diagonal placement.

The code checks the supplied permutations, nonzero bases, Hamiltonian relative
routes, and cycle denominators before evaluating the target. Zero edge weights
do not weaken the fixed-route check. Relative Hamiltonian routes at N>=2 make
the two structural positions in each row/column distinct, so the dictionary
representations do not discard a colliding coefficient within this interface.

Each UBV entry is computed from the at-most-two nonzeros in its U row and V
column. Every off-support entry is visited and rejected if nonzero. Only
at-most-4N supported equations are retained, with coefficients in the correct
order V[i,j] x_i + U[i,j] y_j. The affine solver handles edges, pins, repeated
constraints, contradictions, and forbidden zero-scale parameters. It chooses
parameters within Q or the original prime field and rejects actual field
exhaustion. It never substitutes an extension field.

The source's separately prescribed original endpoint permutations/values are
not inputs to this narrower adapter. The candidate explicitly preserves that
caller-side gate; acceptance here does not remove it. Likewise B need not be
invertible for the inherited sum theorem. Successful answers explicitly report
that target invertibility was not checked. A feedback application must supply
that additional certificate.

### Cost accounting

The advertised bounds are valid in their stated accounting: at most 4N^2 target
calls, at most 12N^2 explicit sandwich multiplication/addition operations, O(N)
field operations in the supported graph stage, O(N^2) explicit forbidden-root
comparisons, and O(N) auxiliary storage with query tracing disabled. The input,
returned certificates, sparse routes, and stored supported equations all have
O(N) size; the caller's target representation is excluded.

One useful implementation clarification, not a required correctness fix: the
12N^2 counter counts the Field.mul/Field.add operations after coercion. Parsing
or normalizing a callback's arbitrary integer/Fraction representation, modular
denominator inversion during coercion, and exact arithmetic bit costs remain
separately charged, as the packet's representation/field-cost exclusions
require. It should not be quoted as a bit-operation bound or as an inclusive
count for noncanonical oracle serialization. Optional trace storage can be
quadratic and is correctly excluded from the O(N) space claim.

## 4. Fresh exact verification

The reviewer's `independent_check.py` uses independently written dense matrix
arithmetic, elimination, finite-field scale enumeration, and plan
reconstruction. It imports only the already inspected current adapter, not the
historical accepted-source program. It checks:

- 22,799 exact target classifications over F2, F3, and F5, including complete
  target enumeration at N=2 for five fresh legal direction pairs per field;
- 18,867 accepted instances reconstructed exactly from the returned plans,
  including nontrivial endpoint permutations and zero edges;
- independently enumerated nonzero-scale images at N=3, so a merely linearly
  consistent but nonzero-infeasible case cannot pass the reference;
- 320 invertible single-coordinate rejecting alternatives over Q at
  N=3,4,5,6,7,8,11, covering every coordinate of the legal nonzero-edge family;
- exact determinant formulas and linear completion-image ranks at those sizes;
- fresh matching-based alternatives over F3, F5, F7, F11, staying in the
  original field and explicitly checking invertibility;
- a concrete F2 failure of the rank-one invertibility-preservation step.

The machine-readable result gives the exact finite-field alternative count.
All tests pass. Separately, a copy of the candidate checker was replayed and its
RESULTS.json matched the sealed candidate output byte-for-byte: 480 graph
systems, 210 positives plus 210 projective-gauge variants, 604 invertible
rejecting alternatives, and 36 general matching controls. The example also
passed. The original candidate source files were not modified.

These are finite exact controls of the implementation and algebraic examples,
not a substitute for the displayed all-size argument, a production benchmark,
or a proof of a different application contract.

## 5. Preserved gates and attribution

The C13 owner remains **TO RESEARCH**. Retain without promotion:

1. General direction selection/discovery.
2. Constructive singular-endpoint-mask cases.
3. Separately prescribed original endpoint/value application contracts.
4. A specific implicit Fourier or feedback-target integration, including exact
   field/root representation, setup, and target-invertibility costs.
5. Topology-, size-, gauge-, and field-matched primary-source comparison and
   worldwide-priority qualification.

The lower bound is elementary unstructured-entry-oracle reasoning. The
single-entry perturbations generally leave a Fourier or other structured
promise class. They impose no lower bound on implicit Fourier formulas,
compressed/symbolic target inputs, matrix-vector oracles, or all-length
construction. A formula-backed callback gives the stated direct upper bound;
it does not make the unstructured lower bound applicable to that formula.

The accepted historical iff theorem remains a dependency with its original
attribution and guards. This review provides no new classical priority claim,
no literature-comparison closure, and no external state change.

## Reproduction

With the frozen candidate as the neighboring directory:

    python3 -B -I independent_check.py

To choose its location explicitly:

    python3 -B -I independent_check.py --candidate /path/to/candidate

A public package that omits administrative source snapshots may run the same
mathematical controls with `--adapter-only`. That mode still verifies the exact
frozen adapter SHA256 and reports that full archival seal verification was
skipped. It must not be represented as a new verification of omitted files.
