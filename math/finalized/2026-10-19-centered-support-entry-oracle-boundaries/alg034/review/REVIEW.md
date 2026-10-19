# Independent review: centered-output support obstruction

19 October 2026 UTC.

## Verdict and binding

**PASS_SCOPED_CENTERED_OUTPUT_SUPPORT_OBSTRUCTION.**

The mathematical lower bound, matching representation order, unchanged-source cutoff obstruction, explicit-integer bit count, and unchanged-iterator incidence count are correct in their stated scopes. No mathematical counterexample or missing quantitative factor was found. The reviewer did not modify author files. The author supplied and resealed a minimal repair during review; the final revised packet and all checks below have been verified.

Final reviewed author manifest SHA-256:

`30b228192c017fcf49c35df56dd19fe52dfe49dd6a27dec4731e21fce4f3e2a4`

The initial mathematical review bound manifest `f7e8ff2ff1809ec152f3e8f01029480df4538e76e942744239eb3b12988f7543`; that original manifest is retained as OLD_AUTHOR_MANIFEST.json.

All 21 manifest members verify. All 11 bound snapshots are byte-identical to their named original files. All 37 members of the accepted BV manifest verify, and its manifest hash is `34cb8b6977c3c5b9ce89ad786628e5cf97a2be49a3d11312fccf5433335c0ac6`. The bound current owner-response hash also verifies. This review read the original accepted BV source, its review, the actual outer iterator and sparse-median producer, and the mandatory outer cost erratum.

The reviewed repair changes exactly PROOF.md, REPORT.md, and check_obstruction.py. All accepted runtime/source snapshots, CHECK_RESULTS.json, and the remaining manifest members are unchanged. AUTHOR_REPAIR.diff records the inspected changes. The original-hash guard correctly rejected a rerun after the author resealed, before any checks or imports; its short diagnostic is preserved in REBIND_OLD_HASH_REJECTION.stderr. The full independent audit then reran successfully against the final hash above.

## Resolved original-review findings

1. The original checker imported recognition code before verifying copied source hashes, contrary to PROOF.md section 7. The repaired main() calls verify_sources() before path insertion and before importing bounded_variation or interval_core. A separate reviewer process imports an isolated copy, supplies an intentionally mismatched dependency, and confirms rejection while both recognition modules remain absent from sys.modules. IMPORT_ORDER_CONTROL.json records this independent control. The execution-description defect is resolved.

2. The revised PROOF.md and REPORT.md explicitly credit the classical comb transform, roots-of-unity/geometric-sum cancellation, and Parseval energy counting. They say neither mechanism is new and confine the contribution to this source-bound contract-specific application. The attribution finding is resolved. This review makes no historical-priority claim.

No change to the accepted BV implementation, its theorem, or the outer runtime was needed.

## Independent mathematical derivation

Write lambda=2^a with a in {0,2}, r>=a+3, m=4r, M=2^(4r), N=M/4, and K=2^(2r-4-2a). The input has ones at the J=N/K locations bK and zeros elsewhere, on actual dyadic grid F=h=r+a+1. Since J=2^(2h), raw energy E=J gives exactly the accepted normalization h, normalized norm R=1, and scale sigma=0. A nonzero integer entry is odd, so the common dyadic representation is canonical. All coordinates and the norm are exact.

An independent way to derive the selected coefficients is the ordinary comb identity for the N-point transform:

- (U_N u)_ell vanishes unless ell is a multiple of J.
- At ell=jJ, its value is 1/sqrt(K).
- Zero-padding and centering give z_(4ell)=(1/2) exp(2 pi i a0 ell/N) (U_N u)_ell.

Here a0=N/2-1 and N/2 is divisible by K. Consequently at k_j=(M/K)j,

    z_(k_j) = [1/(2 sqrt(K))] exp(-2 pi i j/K)
             = 2 lambda M^(-1/4) exp(-2 pi i j/K).

This confirms the negative transform sign, the centering phase, the factor 1/2 in the alias identity, and the factor-two tolerance gap independently of the block evaluator. The K coordinates are distinct. If a coordinate is omitted or is retained with value zero, its error is exactly 2 epsilon>epsilon, where epsilon=lambda M^(-1/4). Every valid explicit list must therefore have at least K nonzero retained entries. This proves sqrt(M)/16 for lambda=1 and sqrt(M)/256 for lambda=4.

For every fixed polynomial in log M, sqrt(M)/(M^(1/4) poly(log M)) diverges along this infinite family. Thus a uniform O(M^(1/4) poly(log M)) candidate guarantee for arbitrary originals at this centered tolerance is impossible. A randomized tape emitting fewer than K nonzero entries has no successful simultaneous-error event on the constructed original. This does not exclude a larger union of lists or another output representation.

Strictness is necessary: coefficients of magnitude exactly epsilon can be omitted. The packet uses magnitude 2 epsilon throughout, so no equality-endpoint overcount occurs.

## Parseval and the precise meaning of sharp order

For a general admitted normalized source, sum |z_k|^2=R^2. If H={k:|z_k|>lambda R M^(-1/4)}, then

    |H| < sqrt(M)/lambda^2.

Keep H and round each component to the nearest 2^-P grid point. The complex rounding error is at most 2^-P/sqrt(2), strictly smaller than epsilon for R>1/2, m>=11, P=16m+16. Omitted coordinates already have magnitude at most epsilon. The rounded values remain far below the inherited Cartesian cap 3 M^2 2^P. Thus this is an actual finite-grid representation-existence upper bound with the matching sqrt(M) order.

Finding H, deciding exact threshold comparisons, obtaining all needed coefficient values, producing certificates, and paying source access are not provided by this argument. No general recovery algorithm follows. The lower-bound sequence is only required on the displayed admissible lengths; the proof does not silently infer a theorem for every possible length from finite checks.

## Unchanged BV contract and cap-only failure

There are q=2J maximal blocks because each one is followed by K-1 zeros. The zero-extended Cartesian variation is B=2J. The exact minimal variation factor is

    C=ceil sqrt(N B^2/(4E))=sqrt(NJ)=2^(3r+a).

Thus the family lies outside the accepted C<=8 and q<=64 domain. This is not a counterexample to the accepted BV supplier. With its original cutoff formula T=2^ceil(m/4)=2^r, one obtains

    K_BV=C T=lambda M.

Both M and 4M violate the strict K_BV<M/2 guard, before scalar preparation or coefficient construction. Raising the two family caps alone cannot make this producer succeed. Raising precision does not alter the failed combinatorial guard.

The default dense and descriptor rejections and both recognition-only cap overrides reproduce with complete identical receipts. Dense rejection charges all 1,024 original visits. The diagnostic successful recognitions are not successful producers, source replays, or outer executions.

## Representation and unchanged iterator costs

Every required successful approximation value has modulus at least epsilon. If it is represented as (x+i y)/2^P, then max(|x|,|y|)>=2^(P+a-r)/sqrt(2). In the stated ordinary explicit integer representation, one numerator has magnitude bit length at least P+a-r=63r+16+a. Therefore coefficient magnitudes alone require at least K(P+a-r)=Omega(sqrt(M) m) bits. A symbolic comb formula or compressed integer grammar is outside this representation claim; signs, locations, other components, records, and source associations add costs.

For the actual outer iterator with D=5, h_outer=80m+1 and t=160m+4, N/M=1/4. The two real endpoint arguments differ by the integer t/4=40m+1, so their ceilings differ by exactly that integer for every k, including wraparound columns. Because t<M, those lifted rows reduce to distinct residues. Each retained record, including a retained zero, therefore has exactly 40m+1 incidences. Any successful list has at least K(40m+1) coefficient evaluations in this unchanged full iterator.

This is an implementation-specific evaluation count. It is not an FFT lower bound or a lower bound for all ways of applying a structured transform. The inherited complete outer upper bound, source/replay prefixes, median construction and replay, actual history widths, lazy preparation, scale, all N initializations and all N output writes remain separately charged. The N output stage already exists and is not contradicted by a sublinear-in-N support obstruction. The all-length hypothesis permits O(M^(3/4)) support at beta=1/4 and remains compatible.

## Fresh exact checks

`independent_checks.py` writes only this separate reviewer directory. It verifies hashes before imports and never calls the author's output-writing main(). `INDEPENDENT_CHECKS.json` retains results.

- 128 independently derived exact parameter plans through m=2048 verify normalization, energy, strict gaps, the variation factor, both failed cutoffs, numerator width, rounding margin, guard, and endpoint count. These are integer plans, not transforms at those lengths.
- Every centered coefficient at M=4096 is checked by literal dense-coordinate summation in Z[X]/(X^2048+1), visiting 4,194,304 coordinates, including zeros. Exact support is 3,076; the 1,020 zeros are precisely the alias-grid locations outside the four selected coordinates. Cyclotomic basis uniqueness certifies these exact zero/nonzero statements.
- Twenty additional selected coefficients at m=16, lambda=1 and m=20, lambda=4 are independently assembled through 1,310,720 further dense-coordinate visits.
- Uncentered and opposite-sign phase substitutions are rejected. Four omissions, four retained-zero substitutions, and four wrong-location substitutions fail; four values at exact distance epsilon pass. The numerator-width endpoint is checked with exact integer squares.
- A separate row-first stencil visits all 1,970,176 row/offset incidences and verifies 481 incidences for every one of the 4,096 columns. The unchanged actual iterator, supplied actual computed one-row medians at six test columns, produces all 2,886 incidences with exactly those row sets. These include retained zeros. No scalar coefficient was evaluated, and no complete outer transfer is claimed.
- Every field of the complete frozen CHECK_RESULTS.json reproduces exactly, including all original rejection/recognition receipts. No author file changes occurred; all manifest members reverify after the checks.

The selected necessary coordinates contain exactly one quarter of the target's squared norm. They are not presented as a sufficient full-spectrum approximation. In particular the independent full-spectrum check confirms the much larger exact support and protects against confusing the selected-coordinate argument with exact sparsity.

## Final scope

Accept the final resealed packet as a sharp-order obstruction to extending the special BV O(M^(1/4) polylog M) explicit candidate budget to arbitrary originals under the same centered-target error contract. Both initial small review findings are resolved and independently checked. Preserve the accepted BV supplier, prior exact-centering obstruction, all-length larger support allowance, and all setup/history/replay/output charges. ALG-034 remains open. There is no general Fourier algorithm lower bound, efficient heavy-coordinate recovery, amplification result, practical speedup, successful comb provider, or full comb outer execution here.

No external write or subagent was used in this review. No service limit was encountered.
