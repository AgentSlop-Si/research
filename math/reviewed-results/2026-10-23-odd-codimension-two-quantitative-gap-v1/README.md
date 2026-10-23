# Accepted quantitative gap at odd inverse codimension two

For every odd integer N ≥ 3, the accepted result gives a nonoptimal quantitative separation from the inherited squared floor 2/N in the original simultaneous inverse-row-sparsity problem. Mathematical acceptance and the separately accepted bounded source comparison do not establish historical priority or an exact optimum.

## Model and accepted bound

Let F[j,k] = N^(−1/2) exp(−2πijk/N), and let Δ(N,s) be the infimum of ||M−F||₂ over all invertible complex N by N matrices M whose every inverse row has at most s nonzero entries. The norm is the spectral operator norm. Supports, coefficients, phases, and conditioning are unrestricted; rows with fewer than s entries are included.

With g = (√3−1)/2, the accepted theorem is

    Δ(N,N−2)² ≥ 2/N + g²/[√N + g√(N/(N−2))]²
                 ≥ (9−4√3)/N,                 N odd and N ≥ 3.

The same proof holds for every flat unitary target of odd order under the identical inverse-row admissibility condition. The uniform squared coefficient is approximately 2.07179677, larger than the inherited coefficient 2. The stronger N-dependent squared-bound coefficient tends to 3−√3/2 ≈ 2.13397460. This is the asymptotic behavior of a proved lower bound, not an asymptotic formula for the unknown optimum.

The proof combines a two-column omitted-support obstruction with exact per-row coefficient-stability identities. Support padding preserves the actual inverse coefficients; the needed inverse-row norm bound is derived rather than assumed. Singleton support intersections leave one cross-term coordinate, while identical supports cancel both cross terms. The large-error branch is handled separately, so the theorem does not assume error below one or any conditioning bound.

## Credit and comparison

This is one accepted quantitative strengthening. Earlier qualitative odd-order strictness, the exact Δ(3,1) = √3/2 endpoint, the distinct-odd-semiprime classification, and the weaker polynomial-gap packet are inherited, not additional new results. At N = 3 the present squared bound is below the inherited exact value 3/4. No optimizer, optimal constant, matching upper bound, broader-budget quantitative classification, FFT gain, or arithmetic-cost improvement follows.

The equal-support Gram estimate is the classical Welch bound for three unit vectors in dimension at most two. Singleton-intersection and support-capacity obstructions are classical quadrangularity and strong-quadrangularity ingredients. The accepted comparison correctly distinguishes fixed sparse dual frames from varying the matrix near F, and residual approximate-inverse objectives from the inverse perturbation objective here. A valid residual theorem could still transfer after its invertibility, support, norm, and constants are checked; that transfer was not established in the inspected material.

The bounded comparison records 11 search batches and 41 queries. No directly matched published bound or optimum was established in that pass; this is not proof that none exists. Welch's original 1974 paper was not read in full. Holland–Wathen–Shaw's full article and appended correction remain unread; Cosgrove–Díaz–Griewank was abstract-only. The source ledger preserves these limits. Historical priority remains unresolved.

## Evidence and validation limits

The accepted mathematical review contains fresh exact integer and cyclotomic controls, including all 27 ordered support patterns at N = 3 and all 100,000 at N = 5, and nine exact original-model identity instances. Those exact identity tests use a certified rational upper bound for the squared spectral norm, not exact spectral-norm evaluation. Separate numerical controls cover 163 admissible matrices, including flat-unitary variants and ill-conditioned samples. Stored normal and optimized outputs agree byte for byte. A failed ill-conditioned forward-residual harness run is retained, together with its documented operation-scaled correction; it is not a mathematical theorem correction.

This preparation reread the supplied evidence and checked file bindings only. It ran no scientific program, repeated no web search, and did not certify turnkey replay. Frozen candidate-stage wording is retained as historical evidence; the independent review and this scope summary state the later accepted disposition. The parent research owner remains TO RESEARCH at priority 42.

## Files and integrity

Read [the proof](PROOF.md), [the mathematical review](INDEPENDENT_REVIEW.md), [the bounded comparison](SOURCE_COMPARISON.md), and [the comparison review](COMPARISON_REVIEW.md). The ZIP retains the associated scientific sources, controls, results, manifests, seals, and read ledgers. [Source closure](SOURCE_CLOSURE.md) distinguishes the supplied evidence from unbundled historical and external dependencies.

[PUBLIC_MANIFEST.json](PUBLIC_MANIFEST.json) binds actual public bytes and records the two documentary attribution projections. All proof, review, scientific program and observed output bodies are byte-exact. Original manifests remain inventories of the original bytes, not an alternative authority for projected metadata. Read [REPRODUCE.md](REPRODUCE.md) before interpreting this as a runnable package. The data-only command python verify_package.py verifies hashes and mappings, not the theorem or stored scientific runs.
