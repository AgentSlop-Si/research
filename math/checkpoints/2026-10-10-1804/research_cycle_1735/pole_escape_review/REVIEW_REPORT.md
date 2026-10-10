# Independent review: internal gauges and pole escape

## Verdict

The finite-DAG internal-gauge theorem is valid, including zero edge coefficients, disconnected vertices, dead ends, and vertices not reachable from boundary sources. Its application to the accepted fixed-support integral obstruction is valid. A hypothetical algebraic Fourier factorization must contain a negative-valuation full input-output path at each place above 11; an individual negative edge need not by itself be essential.

The first bounded-search valuation vector is a genuine point of the entry-equation tropical prevariety. It is not a viable Fourier factorization valuation: eight two-by-two minor constraints exclude it, and a four-entry initial-form identity gives a direct residue contradiction. No global impossibility with poles or arbitrary complex coefficients has been proved.

## Independence and frozen input

The accepted v34 report and `ROOT_INDEPENDENT_CERTIFICATE_CHECK.json` were read. The topology JSON hash is `4ea6269199f843363e90d3c63c2a0f12df220bbbc4b9b9a1ba59fd79a76a9b`. No source-author or search-author program was executed or imported. All programs in this reviewer directory were written independently; only JSON was read from the other folders. All writes were confined to this reviewer's folder. No external file was written or changed.

The accepted prior result remains: this support cannot produce a rank-one transfer with every entry nonzero over any field. Its valuation-ring consequence excludes every integral Fourier factorization, including allowed zero edges. That result is an input here, not newly re-proved by this review.

## Gauge theorem: proof and edge cases

For a nonzero edge u→v of valuation w, let h be the internal gauge valuation. The transformed valuation is w+h(u)−h(v), and h=0 at the designated input/output boundary. Sums on full boundary paths therefore do not change, proving necessity of nonnegative full-path sums.

For sufficiency delete zero edges and identify every boundary vertex with one vertex b. Every cycle through b splits into source-to-sink paths; a cycle avoiding b would be an original DAG cycle. Thus the full-path condition is exactly the absence of a negative quotient cycle. Attach a new source to every quotient vertex with zero-weight arcs. Shortest distances exist even in an arbitrary ordered abelian value group: remove nonnegative cycles and minimize over finitely many simple paths. Set h(v)=d(v)−d(b). Then h is zero on the boundary and every edge satisfies w+h(u)−h(v)≥0. All distances are finite sums of actual edge values, hence are in the value group and are realized by field elements. This proves the theorem without any connectivity assumption.

No finite value is assigned to a zero coefficient; its edge is simply omitted. Isolated or otherwise boundary-disconnected vertices are covered by the auxiliary source. For a graph with directed cycles, nonnegativity of all internal cycles would be an additional condition, so the DAG assumption matters.

Fresh integer controls passed on 256 exhaustive two-branch diamonds and 2,000 deterministic larger networks, including 51 no-full-path cases. Separately, a closed interval analysis of a one-internal-vertex branch gives 137 integralizable cases out of 256. Two independent branches therefore give exactly 137²=18,769 integralizable cases out of 65,536, independently reproducing the author's 46,767 failures.

## Exact witness review

Paths were reconstructed by forward adjacency traversal from the accepted topology. There are 297 full paths for 121 input-output entries, including 22 unique entries. The search's W2 vector passes every exact integer minimum condition

    min(0, all path valuations for that entry) is attained at least twice.

It has 31 negative entry minima and minimum full-path valuation −4. All coordinates are even; dividing by two gives the same initial face, with minimum valuation −2. This verifies an entrywise tropical necessary-condition witness only.

The 50 initial equations with exactly two terms have an explicit common nonzero ±1 solution over F11. There are 31 equations of the form monomial=1 and 19 of the form monomial ratio=−1. Their exponent matrix has rank 47 over Q and F2. This excludes a binomial-subsystem shortcut for this particular pattern; it does not establish simultaneous initial-form feasibility.

### Four-equation initial-form contradiction

Let x_e be the nonzero leading coefficient of edge e, using zero-based global indices 0–98. Direct path reconstruction verifies these four initial equations for the witness:

    (output 1,input 5): x28*x48*x67 = 1
    (output 1,input 6): x6*x48*x67 = 1
    (output 6,input 5): x28*x48*x83 = 1
    (output 6,input 6): x6*x48*x83 + x12*x36*x72 = 1

The first two imply x28=x6. The third makes the first summand in the fourth equal 1. Hence x12*x36*x72=0, impossible because each leading coefficient is nonzero. This excludes every valuation pattern with these four initial term sets and leading target residues 1, a larger scope than excluding only the displayed ray.

### All two-by-two minors independently checked

The reviewer expanded both determinant terms into products of path monomials, collected identical edge monomials with exact integer coefficients, and canceled them directly. This does not rely computationally on the author's disjoint-path filtering. For all 3,025 minors, every remaining monomial has coefficient ±1.

Exactly eight minors violate the tropical condition after adjoining the Fourier target minor of valuation 1. The failed row/column pairs agree exactly with the author's result. There are four single-monomial minors. For example the exact polynomial identity is

    det H[rows {0,7},columns {0,3}] = −x23*x31*x33*x53*x66*x73.

The displayed valuation ray gives this monomial value 0 at every positive scaling; the Fourier minor has value 1 under v(ζ−1)=1. Thus this ray cannot lift, independently of leading-coefficient choices.

The four-equation contradiction above is the residue manifestation of another failed minor, rows {1,6}, columns {5,6}.

## Exhausting the monomial-minor shortcut

A fresh capped-count matching DP was run for all nonempty minor orders 1 through 11. For each layer and each input subset, it counts injective choices of destination edges by output subset, capping counts at two. Exact integer subset-matrix multiplication composes the three layers; capping at two preserves whether a count is zero, one, or at least two. Unique intermediate subsets and each unique layer matching are retained as certificates.

All 705,431 nonempty minors were covered. Exactly 26 have one disjoint path family: the known 22 entries and four order-two minors. No minor of orders 3–11 has just one family. All minors have at least one family, in agreement with the accepted superconcentrator result.

The 26 edge-incidence rows have rational rank 26. Adjoining the exact required valuation k(k−1)/2 leaves rank 26. Thus these monomial equalities are linearly consistent and do not alone give a global obstruction. This is a rigorous negative result for this specific shortcut, not a Fourier feasibility certificate.

## Algebraic versus complex existence

The author's Nullstellensatz paragraph is correct. The finite polynomial system is defined over Q(ζ). A complex solution implies the extended ideal is proper, hence a solution over the algebraic closure of Q(ζ); finitely many algebraic coordinates lie in a number field. This is an existential replacement, not an assignment of a valuation to the given arbitrary complex tuple. Requiring selected coefficients nonzero must be encoded by the auxiliary equation z·product(coefficients)−1=0. A proof in a gauge chart cannot silently divide by an edge whose nonvanishing has not been established.

## Primary background sources

- Difference constraints and shortest-distance potentials are standard: [MIT 6.006 lecture 17](https://courses.csail.mit.edu/6.006/spring11/lectures/lec17.pdf).
- The minimum-attained-at-least-twice condition is standard tropical hypersurface theory: [Sturmfels, Puiseux Series and Tropical Hypersurfaces, Theorem 2.10](https://math.berkeley.edu/~bernd/tropical/sec2.pdf). Intersection of selected tropical hypersurfaces must not be confused with tropicalization of the full ideal.
- The signed disjoint-path determinant expansion is classical: [Gessel and Viennot, Determinants, Paths, and Plane Partitions](https://www.xavierviennot.org/xavier/articles_files/determinant_89.pdf), and [their 1985 published paper](https://www.sciencedirect.com/science/article/pii/0001870885901215).

No priority claim is made for these general tools. The checked fixed-topology identities and bounded exclusions are the project-specific content.

## Reproduction and receipts

Run each program from the workspace root with Python 3:

    python3 research_cycle_1735/pole_escape_review/review_gauge.py
    python3 research_cycle_1735/pole_escape_review/check_initial_binomials.py
    python3 research_cycle_1735/pole_escape_review/reduce_initial_system.py
    python3 research_cycle_1735/pole_escape_review/review_minors.py
    OPENBLAS_NUM_THREADS=1 python3 research_cycle_1735/pole_escape_review/enumerate_monomial_minors.py

Inputs remain at their explicitly named workspace paths. `REVIEW_RECEIPT.json`, `BINOMIAL_RECEIPT.json`, `LAURENT_REDUCTION.json`, `MINOR_REVIEW_RECEIPT.json`, and `ALL_MONOMIAL_MINORS.json` preserve the exact checks. The longer Laurent elimination is redundant once the four-equation proof is extracted.

## Additional exact checks during refinement

The author supplied a compact rank certificate for the 26 monomial-minor incidence rows. The independently recomputed determinant of the selected 26-by-26 submatrix is −1. The valuation vector with w17=w31=w32=1 and all other weights zero solves all 26 required monomial valuation equations. It does not solve the entrywise tropical system: entry (0,4) has two paths both of valuation 1, making the unit target the unique minimum. This gives a concrete consistency certificate without any stronger feasibility claim; see `MONOMIAL_RANK_REVIEW.json`.

A second reconstructed rational candidate, `relaxed_search_round1.json`, passes all 121 entry conditions and the selected small minor conditions, with seven negative entry minima. The independent full-minor expansion finds 23 failing two-by-two minors. A subsequent candidate, `continuous_cut_round1.json`, likewise passes the 121 entry conditions, with eight negative entry minima, but fails 12 two-by-two minors. Exact rational checks and a first explicit failed minor are in the corresponding `_REVIEW.json` receipts. These additional excluded candidates do not establish infeasibility of the unbounded tropical or algebraic problem. A time limit or lack of a solver incumbent likewise proves no such conclusion.

## Mandatory coefficients and exhaustive gauge charts

All Fourier minors are nonzero. Each monomial minor therefore forces every coefficient in its unique edge product to be nonzero. The 26 one-family minors together force 63 edge coefficients nonzero, exactly 21 in each layer. This adds global indices 17,31,32,33,39,46,84,96 to the 55 already forced by unique entries. These are nonvanishing statements, not assertions that those coefficients have valuation zero.

The forced A edges cover first-internal rows 1–10, and the forced C edges cover all 11 second-internal columns. Choosing one such edge per vertex allows 21 globally safe internal gauge normalizations. The only uncovered first-internal vertex is row 0 of A, with allowed edges 0,11,22. Since CBA=F11 is invertible, A is invertible, so at least one of those three edges is nonzero. The three charts that additionally normalize edge 0, 11, or 22 therefore cover every possible factorization. They need not be disjoint. This supplies complete algebraic chart coverage while preserving the option that any of the other 36 nonmandatory edges may vanish. It does not imply integral gauge normalization or Fourier existence.

`verify_mandatory_edges.py` and `MANDATORY_EDGE_REVIEW.json` record exact indices and one choice of 21 global gauge edges.
