# Covariance and two center review

Review date: 12 October 2026. This assessment distinguishes algebraic expressiveness from a uniformly cheap implementation. Exact sources are identified in [Source citations](SOURCE_CITATIONS.json).

The covariance archive SHA-256 is `df65803e339c415388fea2e9a27406ae019ec9e1e456ad7edc1001096135cfb1`. Its readable LaTeX theorem source, README, saved JSON results and manifests were reviewed statically. The author's programs were not run. The PDF is retained byte-for-byte; no claim of a fresh visual typesetting audit is made.

The manuscript's central distinctions are soundly stated at the source level:

- For the stated canonical partial transform, exact refinements have the form C=B M_s M_r^−1, with B in the finer covariance commutant. Its stated forward-row support formula is a structural fact, not a general circuit-size lower bound.
- Same-center shears/diagonals and their defined algebraic combinations preserve the singleton coordinate 1 and cannot perform the canonical refinement.
- Two centers generate translation by 2^r. Together with all diagonal projectors they generate the entire coarse commutant. The proof explicitly permits arbitrary sums of matrix units. This supplies algebraic expressiveness, not constant packet length or linear application/preparation cost.
- Individually valid weighted-permutation Green solves can have linear application cost, but an inverse of an arbitrary sum does not thereby become a legal linear-time primitive.
- Conditional O(N log log N) refinement requires a uniform O(N)-per-step compiler for the actual evolving base, including every coefficient, branch and memory/index cost. The manuscript expressly supplies no such compiler.
- Exceptional-row completion has cost O(G(N)+A(N)+N log(q+2)) only with a structurally supplied exact exceptional set, charged construction G and cheap application A. No cheap nearly complete operator M is constructed. Dense materialization/checking would cost Θ(N²).

Its canonical ladder still uses ordinary Θ(N log N) arithmetic; simply naming O(log log N) packets does not reduce that cost. Its bounded-coefficient volume argument explicitly retains bounded gate coefficients and nonvanishing row-gain hypotheses. None of these restricted or conditional statements is a universal Fourier lower bound or a realized fast Fourier upper bound.

### Relationship to previously accepted ACWL results

The previously accepted ACWL results include the common-center singleton obstruction and canonical normal-form/sparse-inverse product obstruction, with the actual evolving-base factor included. The new manuscript's same-center portion overlaps that scope and is not a separate completion of it.

The two-center construction supplies a concrete answer to the algebraic expressiveness part of “specify an enlarged grammar escaping the singleton obstruction.” That is bounded algebraic progress. It leaves the operative existing completion test unchanged: construct a uniformly cheap all-input exact lift under a legal grammar for the actual evolving base and pay all preparation, branches, roots, routing, inverse/solve and normalization costs. The broader ACWL conjecture remains open. NF-07's separately retired bounded stable-extraction witness and still-open efficient ambient evaluator are likewise not changed.

The manuscript's recovered-corpus inventory and historical branch-status digest are not authority for the present state of other research results. Its finite verification totals and “independent” second arithmetic script remain author-reported evidence, not a second researcher or a fresh execution by this reviewer. Any cited external complexity/priority claims were not independently re-researched in this local source-reconciliation task.
