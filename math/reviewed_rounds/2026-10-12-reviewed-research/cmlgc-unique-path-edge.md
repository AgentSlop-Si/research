Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: e7604057cda2699dcf75ee709fbc2bca513062595100ae7d7005279475d2ad4c

---

# Independent review: exact all-entry unique-path Fourier edge cost

Review date: 2026-10-12 UTC. Local research review only; no external writes.

## Verdict and scope

ACCEPT the restricted mathematical theorem in the final sealed candidate bound by REVIEW_SEAL.json:

For N>=2, among finite directed acyclic scalar-weighted networks with disjoint input sources and output sinks, one nonzero path for every boundary pair, and full transfer F_N[i,j]=zeta^(ij), the exact minimum edge count is N sopfr(N). Here sopfr counts prime factors with multiplicity. Every active scalar edge is counted, including unit-weight edges and each occurrence of a reused constant. Zero edges and boundary-invisible edges may first be pruned.

The prime-length minimum is N^2. The power-of-two minimum is 2N log_2 N. The all-length consequence E >= (3/ln 3) N ln N implies the earlier, weaker e N ln N claim. N=1 is separate: disjoint source and sink require one edge; coincident terminals with a zero-length path would instead cost zero and are outside the stated model.

This is an edge-complexity theorem, not a universal scalar-operation, unrestricted linear-circuit, or general FFT lower bound. It does not disprove the CMLGC source conjecture or settle a unique-minor-chart lower bound.

## Independent proof audit

At an active vertex v let J_v be the input indices reaching v and I_v the output indices reachable from v. Every prefix from a fixed input and every suffix to a fixed output are unique; otherwise concatenation produces two boundary paths. In a DAG these concatenations cannot revisit another vertex. Thus the complete boundary matrix on I_v x J_v factors through one scalar at v and is rank one.

Set K_v=<J_v-J_v> in the cyclic group Z/NZ and d_v=|K_v|. Then J_v lies in a coset of K_v. The Fourier rank-one cross-ratios imply that I_v-I_v annihilates K_v. Therefore |J_v|<=d_v and |I_v|<=N/d_v. No full-spark assertion is used for composite N. For u->v, K_u is a subgroup of K_v, so d_u divides d_v; sources have d=1 and sinks d=N.

With f=sopfr and f(1)=0, f(d_v)-f(d_u)=f(d_v/d_u). Sum the telescoping increment along every unique boundary path. An edge u->v is traversed by exactly |J_u||I_v| boundary paths, giving

sum_edges |J_u||I_v| [f(d_v)-f(d_u)] = N^2 f(N).

For r=d_v/d_u>1, each summand is at most (d_u N/d_v)f(r)=N f(r)/r<=N. The inequality f(r)<=r follows by repeatedly applying a+b<=ab for a,b>=2. Edges with r=1 contribute zero. The resulting lower bound is E>=N f(N).

For the weaker logarithmic version, use ln d_v; the edge charge is at most N ln(r)/r<=N/e. Alternatively the rank-one area bound |I_v||J_v|<=N follows from the spectral norm of a normalized Fourier submatrix and gives the logarithmic charging proof using ln |J_v|. Neither derivation needs restrictions on magnitudes or valuations of edge weights.

For sharpness, write N=ab, j=r+a q, k=s+b t. The identity jk congruent to a q s + r s + b r t modulo N gives a independent b-point transforms, then b independent a-point transforms. Twiddles are absorbed into existing outgoing edges of the second stage. Each boundary pair selects exactly one intermediate terminal. Recursing to prime factors gives E(N)=aE(b)+bE(a)=N[f(a)+f(b)]. The construction is ordinary mixed-radix Cooley-Tukey.

The asserted best universal logarithmic coefficient is correct: p/ln p is minimized over primes by p=3, so f(N)>=3 ln N/ln 3, with equality for powers of three.

## Adversarial model checks

- Zero edges: pruning is sound over complex numbers, because a path product is zero exactly when some edge is zero. A nonzero Laurent expression that vanishes at specialization is likewise pruned. Undefined or infinite edge specializations are outside the legal model.
- Multiple nonzero paths whose sum cancels do not qualify as a unique nonzero path. Combining two parallel edges into one changes the represented DAG and must be identified as a separate representation; equal path products also remain two paths.
- Merging and later splitting of disjoint input sets is allowed and accounted for by the reachability rectangles. Reconvergence of two paths from the same input to a live vertex is forbidden by the all-entry condition.
- Arbitrarily many auxiliary vertices and free/reused constants are allowed. Counting each scalar dependency edge prevents a dense multi-input block or a reused coefficient occurrence from becoming one edge. The theorem does not count distinct coefficient values.
- Boundary injections, external pre/post-processing, implicit matrix-valued edges, or side channels must be expanded into the network before using this theorem. Restricting to a submatrix or selected outputs is a different problem.
- Cyclotomic factors of negative valuation can multiply with positive-valuation factors along a single path. Such legal gauge changes do not affect the proof. Additive Laurent cancellation between paths violates its uniqueness premise.
- Cyclic Green resolvents are not finite DAG path sums. A unique simple path does not remove the loop denominator: a state with loop weight 2 has resolvent transfer -1, despite simple-path product 1.
- Permuting terminal order does not invalidate the argument: retain the actual Fourier character labels under the permutation.
- The exact edge minimum should not be relabeled an exact addition minimum. Unit scaling, assignment, fanout, and accumulator conventions can change operation counts. For F_2, the direct optimal graph has four weighted scalar edges but only two additions/subtractions when scaling by +/-1 and fanout are free. The five-edge scope witness also uses two additions/subtractions plus one multiplication by -2 under a common convention. Its five-versus-four comparison concerns graph edges, not arithmetic optimality.

## Fresh independent controls

independent_checks.py was written independently for this review and imports no candidate or uploaded research program. It constructs mixed-radix DAGs directly and checks integer path counts, full monomial exponents modulo N, all divisor labels, all rank-one cross-ratios, every edge's potential charge, and total edge count.

All 69 lengths passed: every N from 2 through 64, and 72,81,96,100,125,128. This checks 152,409 exact boundary coefficients. The checks use equality of root exponents modulo N, not floating point or an unproved finite-field lift.

All nonempty Fourier submatrices were exhaustively checked for N=2..8 using exact cross-ratio exponents. Composite lengths have nontrivial rank-one rectangles (4 at N=4, 48 at N=6, 160 at N=8), preventing accidental reliance on prime full-spark behavior.

check_candidate_certificates.py reads candidate JSON as data and independently rechecks all 17 candidate monomial network certificates: 4,183 exact full matrix coefficients, each edge's serialized cyclotomic weight, unique boundary paths, and exact potential totals. SymPy supplies cyclotomic polynomials; no candidate code is executed. The serialized N=3 Laurent two-path cancellation control was rechecked by exact polynomial reduction: alpha=1/(zeta-1), beta=1-alpha, alpha+beta=1, while the affected boundary entry has two nonzero paths and fails the class guard.

Most importantly, a five-edge F_2 example separates unique minor families from unique entries. Set v=x0+x1, y0=v, y1=v-2x1. Its transfer is exactly F_2. The full 2x2 determinant has one vertex-disjoint boundary path family, of signed weight -2, while the (1,1) entry has two paths with weights 1 and -2. The hub's reachability rectangle is the entire rank-two F_2. This shows exactly why selected unique-family minors do not imply the lower-bound premise.

Other controls cover a Boolean all-ones star (2N edges, one path per pair, rank-one transfer), splitting one edge into two nonzero parallel weights, zero-weight pruning, N=1 terminal conventions, cyclic resolvents, and f(r)<=r for 2<=r<=10000. Finite controls supplement the uniform proof; they are not used to infer it.

## Classical literature and priority calibration

The underlying unambiguous-DAG and rectangle mechanisms are classical. Chistikov, Ivan, Lubiw, and Shallit explicitly identify at-most-one-input-output-path networks with the unambiguous rectifier/SUM model, and define size by edge count. Their results concern Boolean matrices. The present weighted Fourier phase constraints are additional: the all-ones support matrix itself admits a 2N-edge star, so a Boolean support lower bound alone cannot establish this theorem. Source: https://arxiv.org/html/1509.07588, Sections 2 and 3 (arXiv v2, 2016).

The achieving mixed-radix construction is classical Cooley-Tukey, not a new algorithm. Primary bibliographic source: IBM Research, https://research.ibm.com/publications/an-algorithm-for-the-machine-calculation-of-complex-fourier-series. Original paper: Mathematics of Computation 19 (1965), 297-301; DOI 10.1090/S0025-5718-1965-0178586-1. A Stanford-hosted scan was located at https://web.stanford.edu/class/cme324/classics/cooley-tukey.pdf; the browsing tool did not extract its text, so this review's exact recurrence is independently proved above rather than attributed to an unchecked page.

Papadimitriou, Optimality of the Fast Fourier Transform, JACM 26(1), 95-102 (1979), DOI 10.1145/322108.322118, is directly relevant prior art for graph-restricted FFT optimality. The publisher returned HTTP 403, so its exact hypotheses and theorem are not claimed to have been independently inspected here. Ailon's research paper, https://arxiv.org/html/1609.03278, Introduction (v6, 2018), describes Papadimitriou's model in terms of finite-field computation and root-of-unity multipliers. That is not a verification that Papadimitriou already states the present arbitrary-complex-weight all-entry-unique-path N sopfr(N) formula, nor evidence that this formula is novel.

Prior-work comparison status: PARTIAL SEARCH ONLY. An identical previously published theorem has not been verified, so this review establishes neither historical novelty nor definite rediscovery. Accordingly: accept the self-contained scoped theorem; make no worldwide novelty or priority claim. Avoid calling the weighted complex network itself a monotone nonnegative circuit. Do not import an old paper's statements about then-open unrestricted FFT bounds as a claim about the current literature.

## Scope and remaining work

The CMLGC supplied source SHA256 is 3288a1509f92c682c6212ff0669a680b530ee239aecaa89988dff1af8611dd18 (19,213 bytes). The historical accepted review SHA256 is 031050eaaf86dc5cf7119dfcba51db4ce593e9daea944ccd512fac110c2173f8. These are byte-verified separately from mathematical acceptance of this new theorem. Original uploaded code remained inert.

The CMLGC source explicitly permits path sums and Green networks (lines 67-76), selected unique disjoint-family minors (192-203), a triangular minor chart (219-238), and cancellation (333-336). None imposes all-entry uniqueness. The existing CMLGC proposal must therefore remain explicit_conjecture / legal full-row network unconstructed. Its operational research state may advance to progressed_open, with retire_original_obligation=false; only the added all-entry unique-boundary-path subcase is closed.

Accepted result: "Independently accepted restricted obstruction: an all-entry unique-path DAG realizing F_N has sharp edge cost N sopfr(N), attained by classical mixed-radix FFT. This rules out O(N log log N) monomial-entry gluing, but does not exclude selected unique-minor charts, multipath cancellation, or cyclic Green realizations."

Remaining task: "Construct one legal full-row Fourier network outside all-entry uniqueness, with specified topology, exact coefficients and nonzero divisors, full Fourier identity, and charged preparation/evaluation. Selected-minor matching alone remains insufficient."
