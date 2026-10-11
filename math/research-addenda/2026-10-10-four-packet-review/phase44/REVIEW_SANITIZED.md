# Sanitized publication copy

Original review SHA-256: 2ebae7f1f40e60a4a50cd17fb4319511e0a719fe5d4ee70e2d9f3967366a53b1. Private source identifiers are omitted. Mathematical text is otherwise unchanged. Original review-date statements and historical execution/provenance claims below refer to that original review; they are not fresh claims about this publication assembly. Use the addendum README and replay script for the self-contained mathematical replay and its explicit archive/history exclusions.

# Phase44 bounded independent review

Review UTC date: 2026-10-10. Source-declared research date: 2026-10-11.

## Verdict

The frozen certificate independently passes a fresh interval Banach check for an exact, full 8-by-8 unnormalized negative-sign Fourier matrix, up to nonzero external row and column diagonal scalings. The architecture is four successive sums of three weighted Hamiltonian-cycle Green resolvents, with three **arbitrary nonzero complex** diagonal interstages. This is a finite-size existence result in an expanded amplitude model. It establishes neither the same result with phase-only interstages nor any uniform, unrestricted, or sub-N-log-N FFT algorithm. No publication priority or novelty conclusion was attempted.

The two restricted sparse-inverse inequalities in Theorems 44.1 and 44.2 have sound proofs under their stated hypotheses. They do not bound arbitrary multistage sums-of-Greens circuits. The separate single-Green-per-stage depth bound also remains valid.

## Provenance and execution boundary

- Actual Library report: [private source identifier omitted], FFT_Phase44_Theorems.md, 14,516 bytes.
- Actual Library archive: [private source identifier omitted], fft_green_research_phase44_2026-10-11.zip, 12,460,168 bytes.
- The standalone report is byte-identical to the archive's fft_green_phase44_sparse_inverse/THEOREM.md.
- All 126 entries of the archive's root MANIFEST.sha256 match the archived bytes.
- The Phase44 programs and graph-definition dependencies were inspected only as text. No uploaded program, imported module, optimizer, or inherited verifier was executed.
- Fresh programs fresh_interval_check.py and fresh_controls.py import only standard libraries, mpmath, and NumPy. Their fixed graph orders are independently regenerated from the published seeds and saved in fresh_architecture.json.
- No Sheet, GitHub, or fusion output was changed.

## Architecture and real-variable conventions

The matrix is M = S3 D2 S2 D1 S1 D0 S0, with Sℓ equal to the unweighted sum of three Green resolvents (I−Wℓ,t)^−1. Every directed edge has unit modulus. Each stage has 24 directed multigraph edges and a single common seven-edge spanning tree, giving 17 chord-phase coordinates per stage and 68 phase coordinates in total. The first cycle's seven tree edges are fixed to 1; the other two cycles' eight edges each remain chord variables. This is not an independently fixed seven-edge tree inside every cycle.

Each Dℓ has first diagonal entry 1 and seven entries exp(a+iφ). Its seven phases come before its seven real log-amplitudes in the frozen coordinate array. Three such interstages add 42 real coordinates: 21 phases and 21 log-amplitudes. Total: 110 real variables. The certificate selects 98 distinct variables in a specified order and fixes the remaining 12 real coordinates. The two sets are disjoint and exhaust indices 0 through 109.

All center and preconditioner values are parsed from decimal strings into outward intervals, never through binary64. The 98-by-98 B matrix is a real preconditioner. Equation order is the real parts of 49 row-major complex residuals, followed by their imaginary parts. The target convention is ω8 = exp(−2πi/8).

Suggested wording repair in Theorem 44.3: replace “each internal cycle's spanning-tree gains are 1” with “the gains on a common spanning tree of each three-cycle multigraph are 1.” The numerical definitions and certificate are internally consistent with the latter.

## Fresh interval certificate

The checker reconstructs each Green entry by its directed path product divided by 1−h. It differentiates that explicit formula to obtain dense dG matrices, propagates them through the seven-factor product, and uses the ordinary quotient rule. This differs from the submitted rank-one logarithmic-derivative implementation.

At 70 interval decimal digits and radius 10^−20:

- Maximum preconditioned center residual: 1.9775832252 × 10^−62 (diagnostic upper bound).
- Supremum infinity norm of I−B Dg over the box: 6.2721864348 × 10^−8 (diagnostic upper bound).
- Direct outward-interval comparisons certify residual < radius/4, contraction < 1/2, and residual + contraction × radius < radius.
- Every one of the 12 Green denominators excludes zero. The smallest lower-bound diagnostic for |1−h| is 0.2752698658831879.
- Every normalization denominator in the first row and column excludes zero. The minimum lower-bound diagnostic is 2.3721643678072803.
- All 64 entries of M exclude zero; the minimum lower-bound diagnostic is 1.4209199856236314.
- All 64 normalized Fourier target entries are covered by the evaluated box enclosure. The largest full-matrix center-error upper diagnostic is 5.90 × 10^−64; the box-enclosure error upper diagnostic is 2.824 × 10^−13. This larger enclosure is interval overestimation, not the error at the certified root.

The 55-digit repeat at the source's radius also passes. Its residual bound is 2.2643964863761834 × 10^−47, matching the source diagnostic. Its independently derived contraction enclosure is 6.272186434795803 × 10^−8. The source's smaller 4.70564198759532 × 10^−8 contraction bound was not independently reproduced with the same derivative expression; the fresh, slightly wider bound is still overwhelmingly sufficient. See fresh_interval_55dps_results.json and fresh_interval_results.json. Floating diagnostic strings are not used as logical proof checks.

The 80-digit repeat at radius 10^−21 passes as well, with preconditioned residual upper diagnostic 2.3491982614 × 10^−72 and fresh contraction upper diagnostic 6.8124621053 × 10^−9. The source's 80-digit residual is reproduced; its tighter 5.2459176580 × 10^−9 contraction number remains specific to the submitted derivative enclosure.

Banach's theorem gives a fixed point of T(t)=t−Bg(t) within the closed real box. Since ||I−B Dg||<1, B Dg is invertible, hence square B is invertible. Therefore g(t)=0 at that fixed point. Every cross-ratio with 1≤r,j≤7 is exactly ω8^(rj). Set Lrr=M00/Mr0 and Rjj=1/M0j. Nonzero denominator guards make L and R well defined. The 49 projective equations plus the normalized first row and column give all 64 identities LMR=F8. This is full-matrix equality, not merely selected rows, a generic rank statement, or a small numerical residual.

The exact root is proved to exist near the frozen decimal center. The decimal center itself is not claimed to be the exact root.

## Independent numerical controls

A second program reconstructs W and uses dense linear solves, independently of the path formula. It also implements a scalar cyclic recurrence and applies all 12 Green solves matrix-free.

- Dense direct-solve calibrated full-matrix error: 8.15 × 10^−14.
- Matrix-free all-eight-basis-vector error: 1.18 × 10^−13.
- Matrix-free comparison with NumPy FFT on 24 freshly seeded complex random inputs: 7.70 × 10^−13 maximum error.
- Matrix-free versus independently assembled calibrated dense matrix: 5.37 × 10^−13 maximum error.
- Wrong-sign Fourier target control: error approximately 2.
- Perturbing the first selected real coordinate by 0.001: error approximately 0.6054.
- Setting every interstage log-amplitude to zero without refitting: error approximately 97.10.

The positive controls confirm entry convention, graph orientation, multiplication order, and calibration. The negative controls show this witness depends on its values and amplitude model; they do not prove that another phase-only witness cannot exist. The interstage amplitude range in this certificate is approximately 0.00987065 to 7.78366, substantially different from unity.

## Audit of the restricted obstruction proofs

### Sparse right inverse

Theorem 44.1 assumes M=S D A^−1, where S is a sum of q Green resolvents, D is invertible diagonal, A is invertible, every column of A has at most ρ nonzeros, and every row has at most κ nonzeros. The conclusion is

N ≤ q(1+ρ(κ−1))[ρ(q+1)]^q.

Take m=ρ(q+1) physical output rows that correspond to consecutive Fourier frequencies under the alleged monomial equivalence. The selected Fourier matrix is full spark on at most m columns. The arc-signature partition has at most m^q classes and rank at most q inside each restricted class. The equality MA=SD converts every column to a combination supported on at most ρ Fourier columns. In a signature class, one chosen support intersects at most ρ(κ−1) other supports. Thus a class larger than q(1+ρ(κ−1)) contains q+1 pairwise disjoint nonempty supports by greedy selection. Their union has at most m elements, so full spark makes the corresponding MA columns independent, contradicting class rank ≤q. The case m>N is harmless: prove by contradiction assuming N exceeds the proposed bound, which already ensures m≤N. Row/column permutations and nonzero scalings preserve this reasoning.

For ρ=κ=1 this reduces to N≤q(q+1)^q. For fixed ρ and κ it entails q=Ω(log N/log log N). Both sparsity hypotheses matter. The theorem does not cover an unrestricted dense inverse A or arbitrary extra dense stages.

### Right stage consisting of one cycle

For M=S D (I−W0)^−1, multiplying by I−W0 gives differences of two scaled Fourier columns, with supports equal to edges of the right-hand Hamiltonian cycle. On m=2(q+1) selected rows, q+1 vertex-disjoint equally colored edges would be independent, contradicting signature rank ≤q. A proper subset of cycle edges decomposes into paths, which have a matching of size at least half their edge count. A whole-cycle color class is handled separately: under the contradiction hypothesis N>2q[2(q+1)]^q, the cycle has a matching of at least q+1 edges. Therefore each color class has at most 2q edges, and

N ≤ 2q[2(q+1)]^q.

For q=1,2,3,4 this gives 8,144,3072,80000. The proof correctly permits arbitrary nonzero complex D and arbitrary weighted Hamiltonian cycle orders. Its scope is precisely this restricted two-layer architecture.

### Single Green per stage

For a product of d single Green resolvents with diagonal interstages, the inverse is a product of d matrices I−W, interleaved with diagonals. Each factor has at most two nonzeros per row, so the inverse has at most 2^d nonzeros per row. Every inverse of a monomially equivalent Fourier matrix is dense. Hence N≤2^d and d≥ceil(log2 N). For two single-Green stages this improves the q=1 right-cycle bound to N≤4. It does not apply to sums of multiple Green resolvents per stage and does not conflict with the certified four-stage three-Green witness.

The archived finite-field witness program was not run. These obstruction conclusions follow from the audited symbolic proofs, not from finite-field examples.

## Rank, parameter count and remaining limits

The parameter count P(d,N)=d(4N−1)−2(N−1) gives the necessary generic-projective-target condition d≥ceil(2N(N−1)/(4N−1)). This is a dimension condition, not a Fourier-specific impossibility theorem. The fresh N8 Banach certificate itself proves a nonsingular selected real Jacobian, so full local rank 98 at N8 is independently supported.

The N16,d8 JSON reports 474 parameters, 450 output coordinates and rank 450 modulo two primes. Those finite-field rank computations were inspected but not replayed here. They concern an open set around a test image, not membership of the specific F16 target. The saved attempted F16 fit has maximum projective complex error 3.414566879107864 and explicitly disclaims exact Fourier existence. No F16 existence claim is validated by this review.

Online application uses 12 cyclic solves and three diagonals for this fixed N8 witness. A uniform family of supplied parameters, synthesis cost, precision/conditioning guarantees, and asymptotic FFT improvement remain unresolved. Increasing generic depth proportionally to N would have O(N²) online cost under this implementation. No new fusion is proposed.

## Reproducibility files

Run from any working directory with Python 3, mpmath 1.3.0 and NumPy available:

    python3 fresh_interval_check.py
    python3 fresh_interval_check.py --dps 55 --output fresh_interval_55dps_results.json
    python3 fresh_interval_check.py --dps 80 --radius 1e-21 --output fresh_interval_80dps_results.json
    python3 fresh_controls.py

Each command above runs fresh local review code only. See SOURCE_AND_REVIEW_SHA256.json for file hashes, archive_manifest_check.json for archive checks, fresh_architecture.json for the actual graph orders, the three interval result/log pairs, and fresh_controls_results.json for controls.
