# History, attribution, and retained limits

## C8 phase-defect rank-zero result

The original target is approximation of the normalized eight-point Fourier matrix by arbitrary invertible complex-monomial outer factors around an unrestricted real matrix, measured in the external complex operator norm, with correction rank zero. The accepted phase reduction absorbs real monomial magnitudes and permutations into the real core and removes only diagonal-unitary gauges from the residual norm.

The earlier strict-lower argument established sin(3 pi/16)<delta_(8,0), using the commutator, weighted cycles, endpoint rigidity, Fourier obstruction, and compactness. The later accepted legal upper witness established delta_(8,0)<=sqrt(1+sqrt(sqrt(2)-1))/2. That upper construction uses four-periodicity only for its witness and never establishes a global periodicity reduction. Their complete manifested author and independent-review evidence is retained under supporting_sources/c8_strict_lower and supporting_sources/c8_upper.

The present quantitative argument replaces exact endpoint rigidity by quantitative estimates, controls complementary Fourier coefficients without dividing by them, and uses flat-vector tests on actual two-dimensional compressions. The compressions need not be invariant or unitary. The strict endpoint follows from a strict contradiction at the proposed non-strict residual threshold together with compactness. The new lower endpoint does not close the gap to the inherited upper witness.

The new independent review separately audits normalization, unequal cycle offsets, stability constants, signs, strictness, and the actual-compression argument. Its fresh exact controls supplement that analytical audit. The candidate and review files retain their own attribution and development-stage language. No source is relabeled as a new result of this packaging pass.

The exact global optimum, minimizer classification, and whether nonperiodic phases improve the upper witness remain open. No assertion is added for other dimensions or correction ranks. Previously accepted rank-one, zero-error correction-rank, boundary-rank, and other phase results are not changed. No FFT operation-count, running-time, or algorithmic improvement follows from the claims packaged here.

## F020 third partial p-block

The original polynomial family is

P_0(X;q)=1, P_1(X;q)=X,
P_(n+1)(X;q)=X P_n(X;q)-(1-q^n)P_(n-1)(X;q),
H_n(z;q)=sum_(k=0)^n [n choose k]_q z^k.

The accepted two-digit theorem supplies squarefreeness and the ordinary-square bilinear guard for b<min(2p,p^s), the p-block coefficient theorem, and the outer residual recurrence. The accepted boundary theorem supplies b=2p, auxiliary centers, separating residual, root distances, irreducibility, and discriminant valuation. Their complete manifested evidence is retained under supporting_sources/f020_two_digit and supporting_sources/f020_boundary. Source-bound historical and supplemental derivations are also preserved; they are inherited inputs, not newly claimed results.

The new argument transports the accepted separating residual through b=2p+r, 0<=r<p. It uses the exact joining identity and a strictly positive perturbation gap; the smallest odd-r gap is 1/6 at p=3. At each of the two accepted auxiliary centers the normalized residual is Z^p+cZ, with c=(-1)^((p+1)/2). Simple-root Hensel lifting constructs two disjoint p-root inner clusters. The outer recurrence supplies r-(r mod 2) outer roots. For odd r, the exact zero is simple by the complete distinct-root count, rather than by parity alone.

With v(q-1)=1 and alpha=(2p-1)/(2p), all 2p inner roots have valuation alpha. Within a cluster the distance valuation is 1; between clusters it is alpha. Each outer root has valuation 1/2 and distance valuation 1/2 from every distinct outer or inner root, and from zero when present. The distance from zero to an inner root is alpha. The inner root set is Galois-stable over Q_p(q), and the denominator of alpha proves irreducibility of its degree-2p factor. This does not claim that every full P_b is irreducible.

The discriminant formula uses the stated t-normalized valuation and every pairwise distance. The transfer to the actual H_b excludes both branch values X=2 and X=-2. The kernel uses ordinary squares in the original Christoffel–Darboux normalization; no Hermitian positivity substitution is made. At b=0 the root condition is vacuous.

This is a proof extension within the supplied research chain. Classical Gaussian Rogers–Szego, recurrence, Hensel, valuation, and Christoffel–Darboux ingredients retain their source attribution. No historical-originality or exhaustive literature-priority claim is made. Existing source texts, citations, exact check outputs, and differing historical schemas are preserved byte-for-byte.

The tail unit fails at r=p, so b=3p and later are not covered. For s=1 the theorem remains b<p. Any use with an existing all-A theorem still requires its separate independent guard. F020 remains open, F023 remains its alias, and priority 58 is unchanged. No canonical owner row, score, priority, status census, or record is modified.

## How to read historical evidence

Immutable candidate summaries may still say that independent review is pending. They describe the moment the candidate was frozen. The two new final independent verdicts, bound in FINAL_ACCEPTANCE.json, provide the current scoped scientific acceptance. Earlier review logs and source snapshots retain their original chronology; no historical intermediate is promoted to an independent proof of the new results.

All direct primary source manifests and eight inherited manifest payloads are complete. Every nonarchive file bound by the new independent source receipts is copied unchanged. Duplicate archive containers, exploratory extras, caches, and deeper unbound historical dependencies are excluded with explicit disclosure. These boundaries avoid claiming a recursive archive of the entire research project.
