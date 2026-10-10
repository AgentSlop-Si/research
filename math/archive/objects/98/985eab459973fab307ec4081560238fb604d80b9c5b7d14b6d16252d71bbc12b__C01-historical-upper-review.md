# Independent review: infinite restricted exact-three Green family

## Verdict and scope

**Accepted.** For every positive odd q coprime to 5 with q≡1 mod241, the specified five-coordinate principal block C_q of the forced chirp resolvent B_(5q²) has minimum exactly three diagonal-ended Hamiltonian Green summands. The two nontrivial branches have reciprocal closing weights; the third is a diagonal correction. All displayed endpoints are nonsingular, every guard holds at both quadratic roots, and all primitive fifth-root embeddings are covered.

This constructs only a 5-by-5 block. It supplies a lower bound of three for full B_(5q²), but no full-matrix upper bound. The source keeps that distinction correctly. All mathematical Sections 1–7 and the scalar/bit-cost qualifications were reviewed. The constructor's code was kept inert; the exact data and manifest were treated as evidence to compare, not executed programs.

The conditional all-length Bluestein bridge is valid in a common exact coefficient field supplying the required roots, with their generation/extension costs included in its premise. A fast transform at supported sizes alone does not magically generate a primitive supported-size root or a square root of an unrelated input root. The source's root-cost caveat must remain attached to the bridge.

## Uniform construction and guards

The accepted principal-restriction theorem gives eta=omega^(q⁴), G_(5q²)=qg and the exact target

C_q=(F−qgH+5q³gD)/(1+5q³g).

The denominator's norm is 1−125q⁶, never zero for integer q. Reversal symmetry gives precisely the six off-diagonal classes used by the synthesis lemma; the q³-dependent diagonal entries are retained in the correction, not dropped. C_q differs from the forced B5 when q>1 and cannot be substituted into the q=1 Fourier recovery formula.

The normalized constants, quadratic and endpoints are recomputed from C_q. The reviewer's sparse integer-polynomial checker independently expands both the residual identity P(d)/(dT) and the reciprocal-pole norm identity. These are identities in arbitrary normalized constants, not numerical fits. The latter gives Norm(t)=1 and conjugate(t)=1/t whenever the guarded formulas are defined.

Let R=Z[eta] localized at (241,eta−91). The cyclotomic integer ring is integrally closed; this localization has residue F241. For every q≡1 mod241, q and q³ reduce to 1, and the target denominator reduces to 34. The reviewer checks these congruences coefficient-wise after substituting q=1+241k, including all 25 target numerators.

The six base-field residues are (20,102,234,89,163,163), as claimed. Hence the normalized constants, leading coefficient and discriminant are units. The monic polynomial reduces to d²+30d+124, whose discriminant 163 is nonsquare. A root in Q(eta) would be integral over the local ring and would reduce to a residue-field root, a contradiction. Thus each admitted parameter has a genuine quadratic extension, not merely a formal reducible quotient.

In the rank-two algebra R[d], conjugation gives inverse(y)=conjugate(y)/Norm(y). The six successive extension norm residues are (124,139,53,1,160,85); the fifteen endpoint residues are

u: (1,44,153,153,44),
v: (41,117,7,7,117),
diagonal correction: (72,113,64,64,113).

All are nonzero. Inductively each denominator is a unit before the next expression is formed, so reduction commutes with every division and the same residues persist for every congruent q. This uniform induction is the decisive argument. Nonzero norms imply nonzero values at both roots, and field embeddings preserve nonzero elements. The proof covers all eight complex embeddings. Oddness and coprimality with 5 are needed for the ambient restriction identity, not for the standalone five-dimensional rational construction.

## Exact minimum and an additional full-ansatz exclusion

The lower bound is the separately accepted closed-projective two-summand exclusion for C_q; its proof includes all Hamiltonian orders, zero edge weights and singular endpoint masks. The present three legal summands give the matching upper bound. Principal restriction carries a full B_N representation to one for C_q, establishing the full lower bound only.

A useful strengthening of the source's Section 5 follows from the already accepted complementary-cut identity. For invertible B_N,

rank B_N[I,I^c]=rank B_N^−1[I,I^c]=rank F_N^−1[I,I^c],

because the chirp term in B_N^−1=A_N+F_N^−1 is diagonal. For I={0,...,k−1}, k=floor(N/2), the Fourier block is a rectangular Vandermonde matrix and has rank k. But the two-natural-cycle-plus-diagonal ansatz has upper off-diagonal entries u_i v_j+t v_i u_j, hence rank at most two across this cut. Therefore **that exact full ansatz is impossible for every odd N≥7**. The N5 positive control is consistent with k=2. Different cycle orders or additional nontrivial branches are not excluded by this argument.

This refinement is a restricted synthesis diagnosis, not a general three-Green impossibility or runtime lower bound.

## Cost and conditional Fourier bridge

For an actual full B_N, the polynomial identity

(1−z)[(1+c)z²+(1−2c)z+(1+c)]=1−[z³−c(1−z)³]

gives the correctly ordered Fourier recovery using three sequential B_N calls. The full family's setup S_N, all k_N branch arrays, endpoints, diagonal corrections, branch sums and chirps give O(S_N+k_N N+N) arithmetic work, at most 3r_N nontrivial Green solves. No division by an individual zero edge is required in a valid Hamiltonian scan. The conditions k_N=o(log N) and S_N=o(N log N) are sufficient for an asymptotic improvement only if a full uniformly generated identity and all scalar/root/precision requirements are supplied. This report supplies none of those missing full-family premises.

For supported M=5(2410k+1)², minimal M≥2n−1 satisfies M=2n+O(sqrt(n))+O(1), with large fixed constants allowed. Bluestein's chirp identity reduces an n-transform to a cyclic convolution at M; the signed kernel indices lie in [−(n−1),n−1], and M≥2n−1 prevents aliasing. Two online transforms plus one kernel transform in setup are all charged. The inverse is a reversal and 1/M scaling of the positive transform. Padding, chirps and explicit writes cost O(M+n). Thus the stated conditional O(n) implication is correct when the hypothetical supported-size transform and compatible-root setup are uniformly O(M). It is not a consequence of the five-coordinate construction.

For the result actually obtained, fixed-dimensional field operations and one quadratic extension generate the factors. Rational-coordinate heights grow as O(log q), since a fixed number of rational operations of bounded degree is used and all denominators stay nonzero. Algebraic coordinates plus the defining quadratic suffice; no numerical root choice is needed. Extracting eta from a supplied ambient omega takes O(log q) field multiplications. Applying the 5-by-5 block takes two five-entry solves plus a diagonal correction and endpoints, not an application of the full ambient matrix.

## Independent controls and coverage

The reviewer reused only the reviewer's own previously sealed rational field implementation, with a newly authored extension checker. It independently reconstructs at q=1,483,1447,1929,2411, plus q=242 and q=965 as standalone algebraic controls outside the ambient odd/coprime-5 restriction. Across seven cases it checks 350 both-root entries, 700 two-sided Green inverse entries, 245 factored scan outputs and all 27 guard residues per case. It also checks the generic integer-polynomial identities and 25 formal target congruences.

Twelve exact Bluestein controls use actual convolution transforms in one compatible finite field. Most use small convolution lengths outside the special supported sequence; they test the general convolution identity, not a nonexistent full supported-family executor. Ten exact minimal-padding checks include a 30-digit target length. Five additional actual chirp-resolvent controls at N5,7,9,13,15 reproduce the full half-cut ranks and the natural-ansatz obstruction. Uniform proofs, not these samples, justify the infinite statements.

Every constructor manifest entry was hash-checked. The constructor report and result JSON are snapshotted as inert sources. The prior B5 and infinite restriction independent seals are identified as explicit dependencies; their programs and full historical packages were not rerun. Original source implementation assertions remain distinct from the reviewer's fresh tests. Full isolated standard-library replay is byte-identical.
