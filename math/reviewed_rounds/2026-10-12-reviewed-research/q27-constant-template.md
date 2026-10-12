Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: 9cc8324a96012846b3c2dd2b09ac87a5984c1353159b30ff3b91bfe08226e543

---

# Q27 consecutive-template obstruction: independent review

Review date: 11 October 2026 UTC.

## Decision: ACCEPT, with the stated narrow scope

The pinned candidate proves that the frozen stage-1 consecutive triple (8,9,10) does not admit the proposed constant-coefficient F² certificate. Its 49-by-44 quotient coefficient matrix has exact rank 41. Its normalized coefficient functional annihilates all 49 quotient polynomials and takes the value 1 on F. The supplied branch-preserving monomial-gauge obstruction is also correct in its expressly limited scope.

This review adds **zero coordinate triples** to any accepted exclusion coverage. It neither promotes a 128/129 coverage figure nor certifies 192 nonconsecutive cases. It proves neither Fourier feasibility nor Fourier nonexistence on the consecutive slice.

No mathematical or scope repair is required for the pinned candidate. The restrictions below are part of this acceptance, rather than optional qualifications.

## Pinned source and independence

Source archive:

Q27_Consecutive_Template_Obstruction_Author_Candidate_2026-10-11.zip

SHA-256:

ad79305f68287582682d6d4c394f6387245ee2eb20abb2de34c2f63c66d5610a

The archive hash and every one of its 17 manifest-listed member hashes and sizes were checked. Its chart hash is 5528afbbd5b4008a5e0f79043870e72a613e0fd421288d2ce1e5dbffee1c9e98. All five predecessor source bindings were independently matched against the extant predecessor files, read as inert bytes. SOURCE_HASHES.json and SOURCE_BINDINGS_VERIFICATION.json record these checks.

The two review programs were written independently for this review. No author or predecessor research program was executed, imported, compiled, or evaluated. The candidate programs were handled only as opaque archive members for hashing. Neither the source packet nor its predecessors were modified. No Sheet, GitHub, or other external write was made.

## Independent coefficient reconstruction

The reconstruction begins solely with CHART.json: N=8, M=S2 S1, both stage sums unweighted, and the declared edge orientation. Gaussian-rational edge weights are rebuilt as (a+ib)/(a-ib). Every weight has exact modulus one.

Five fixed Green matrices were recomputed by direct Gauss-Jordan inversion over Q(i). The active matrix was separately inverted by direct Gauss-Jordan elimination over the full rational function field Q(i)(x,y,z), without the candidate's geometric-series construction. Every inversion was checked in both multiplication orders. The five fixed guards are nonzero and agree with the stored values.

The active holonomy exactly matches the candidate's h and has h conjugate(h)=1. Multiplying the direct active inverse by F=1-hxyz produces a polynomial matrix B with multiaffine support. With the two frozen stage-1 Greens summed as C and the three stage-2 Greens summed as L, the independent reconstruction uses N=L(FC+B).

It then constructs the reciprocal-conjugate numerator Ntilde=xyz conjugate(N)(1/x,1/y,1/z), and every anchored polynomial P_rc directly from the stated four-factor products. Each of the 49 divisions by F has zero remainder and multiplies back exactly. The union of quotient supports has exactly the candidate's 44 ordered monomials. **All 2,156 Gaussian-rational coefficients agree exactly with the pinned coefficient file.** Thus the separation certificate is bound to the actual frozen chart and quotient construction, rather than merely to an unverified coefficient table.

## Exact functional, kernels, and rank

The supplied normalized separator has 44 coordinates. Exact ordinary coefficient-vector dot products give:

- A times the separator equals zero in every one of the 49 rows.
- The coefficient vector of F paired with the separator equals exactly 1.

All three supplied right-kernel vectors were independently checked against all 49 rows, for 147 exact pairings. Their last three coordinates form the 3-by-3 identity, so they are independent and prove rank at most 41. Their recorded free-column metadata and target pairings also match.

For the matching lower bound, a separate fresh program clears denominators row by row in the specified 41-by-41 minor. It recomputes its determinant in characteristic zero using a hand-written fraction-free Bareiss algorithm on pairs of Python integers representing Gaussian integers. Every one of the 22,140 Gaussian divisions is checked for zero remainder. The resulting determinant is nonzero and agrees exactly with the complete stored Gaussian-rational determinant. This proves rank at least 41, hence rank exactly 41. No modular rank observation is used as the determinant proof.

A planted changed quotient coefficient paired with a nonzero separator coordinate is rejected. A separately planted normalization error in the separator is also rejected.

Since the functional is ordinary linear coefficient pairing with fixed Gaussian-rational values, it also extends C-linearly. Consequently F is outside the constant-coefficient row span even over C. Because P_rc=F Q_rc and the polynomial ring is an integral domain, a constant-coefficient identity sum(c_rc P_rc)=F² would imply sum(c_rc Q_rc)=F, contradicting the functional. This is exactly the claimed template obstruction.

## Direct evaluation controls

Six exact parameter triples were used, including the candidate's four triples and two fresh controls: (3,-2,7), and ((20+21i)/29,(7+24i)/25,(9+40i)/41). These include points on and off the unit torus.

At each point and its reciprocal-conjugate point, all six Greens were directly inverted again. Across these controls the verifier checked 72 nonzero guards, 144 two-sided inverse products, and 294 quotient evaluations. It also checked 196 unit-torus modulus identities across four torus samples. Polynomial numerator and reciprocal-conjugate numerator evaluations were checked entry by entry against the direct inverses.

These are consistency controls, not feasibility searches. The coefficientwise reconstruction, functional, and determinant establish the exact conclusions independently of the finite sampling.

## Gauge conclusion and its limit

For each of the four fully free active branches, the two companion branches include the directed standard 8-cycle. The permutation part of a monomial conjugation preserving that weighted cycle must be one of its eight rotations. The independent support check confirms that none of the seven nonidentity rotations commutes with the other frozen companion cycle: all 28 nontrivial-rotation checks pass, with independently enumerated mismatch vertices.

Therefore the permutation part is the identity. A diagonal matrix commuting with the nonzero weights of one full directed cycle has all eight diagonal entries equal, so the monomial matrix is scalar. Commutation with a Green matrix is equivalent to commutation with its underlying W because the relevant inverses exist.

The two fixed companion holonomies are exactly distinct in each of the four cases. Their characteristic polynomials t^8-h differ, precluding a similarity that swaps the two companion branches. The supplied exact holonomy data and every reported mismatch vertex were checked.

This proves only a statement about simultaneous monomial conjugation preserving the individual frozen companion branches, including the possible branch swap that their distinct holonomies exclude. It does **not** classify transformations preserving only their stage sum, separate left/right transformations, transformations altering the frozen chart, or general rational equivalences of the product. In particular, it supplies no additional Fourier exclusion coverage.

## Permitted use and excluded promotion

Accepted use:

1. Cite exact rank 41 for this frozen consecutive quotient matrix.
2. Cite impossibility of the constant-coefficient F² identity for stage 1, edges (8,9,10), with the other phases frozen as specified.
3. Cite the four-branch scalar-only conclusion for monomial conjugations preserving both frozen companions individually, with swaps excluded by distinct holonomies.

Do not infer absence of F² from the full polynomial ideal, impossibility with polynomial multipliers, impossibility of different powers or different necessary invariants, Fourier feasibility, Fourier nonexistence, or a theorem covering all 192 nonconsecutive cases. The combinatorial counts 224 total same-Green triples, 32 consecutive, and 192 nonconsecutive remain combinatorial counts. All prior accepted coverage totals remain unchanged by this review.

## Reproduction and sealed evidence

In a fresh directory with Python 3 and SymPy, run:

1. python rebuild_and_verify.py
2. python check_exact_minor.py

Both use the included SOURCE_AUTHOR_CANDIDATE.zip, whose hash is pinned in their source. They execute no code from it. CHECK_RESULTS.json records reconstruction, kernel, functional, and gauge checks; EXACT_MINOR_REVIEW.json records the independently computed exact determinant. DECISION.json joins these results into the final bounded acceptance. MANIFEST.json seals the review artifacts and SEAL.json identifies the final review archive.
