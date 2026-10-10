# Audit and fusion of the 16:28 UTC Fourier research additions

## Result

The new batch strengthens three separate branches but does not establish an exact arbitrary-input, all-output, sub-N-log-N Fourier transform. Its most useful changes are a smaller regular algebraic target, a one-cycle approximate estimator with sharper covariance, and broader restricted Green-architecture tests.

This report distinguishes source claims, independently reconstructed results, new bounded consequences, inherited controls and unresolved questions. It makes no publication-priority claim.

## 1. Sources and coverage

The three supplied Library items are:

- [private-id]: fft_unit_step_chirp_v9(1).zip.
- [private-id]: fft_green_research_phase18_2026-10-09(1).zip.
- [private-id]: fft_dual_support_onion_gate_2026-10-09(1).zip.

They were resolved directly, downloaded with current Library helpers and retained unchanged. Their IDs, versions, sizes and hashes are in SOURCE_ARCHIVES.json.

The source-level audit covers every member recursively, including Phase17 inside Phase18 and all deeper inherited checkpoints. Counts:

- 562 member occurrences, 381 unique member hashes.
- 90 unique contents absent from the full declared predecessor hash sets: 88 text/data, one nested archive, one compiled binary.
- 472 inherited member occurrences.
- 714 embedded hash references, all passing.

The comparison includes 528 baseline canonical text hashes, recorded baseline Library-file hashes, and both member and top-level source hashes from the 14:50 and 15:20 additions. Two nested archives are byte-identical to previous top-level source archives and are classified as inherited. Byte novelty is not theorem novelty. Earlier inventories remain dated snapshots rather than silently updated totals.

Uploaded source code and the v9 native benchmark were not executed, imported or compiled. Their reported test and timing results remain source-reported. Only freshly written audit checkers were run. Hash verification proves byte consistency, not theorem truth.

## 2. Exact two-stage algebra: genuine reduction, smaller open locus

Source delta: the first dual support elimination produces 20 degree-at-most-nine equations in 16 variables. A second row/column elimination gives eight rational coordinates and 12 residual equations at F8. The eight-coordinate reconstruction generalizes to n>=6 with (n-4)(n-5) residual conditions and the specified permutation pattern.

Independent reconstruction matches all 8,437 exported coefficient terms and proves the ten eliminated polynomials identically zero, rather than merely zero at samples. The three-character recurrence follows directly from Fourier support and an invertibility argument.

The reduction narrows the locus. New S prefix denominators, Delta elimination determinants and the boundary determinant must remain nonzero, alongside inherited t/s anchors, det(C), B-stage corners and inverse-C corners. The independent audit includes explicit saturation data.

A bounded new characteristic-zero example over Q(zeta8) has S1=0 while C, both B corners and both inverse-C corners remain regular. Its denominators and nonzero properties have a valid mod-97 certificate; the selected partial constraints hold by construction. The remaining constraints fail. Thus this is a rigorous exceptional partial point, not a factorization.

Inherited controls retained: old diag(A) and new diag(A^-1) charts differ; unsaturated sextics have spurious solutions; the earlier cofactor saturation and complete 176-quadratic lift remain relevant; the local jet obstruction is still local. No exact F8 solution or exhaustive exclusion has been obtained.

## 3. v9 chirp: one cycle, explicit projector, conditional computation model

Source delta: replacing a*t^2 with a*binom(t,2) makes the recurrence step a, giving one output cycle for a unit modulo prime-power N. A parity-dependent phase yields antiperiodic monodromy and a total/2 seed.

Independent covariance reconstruction gives Q0[n,n']=(M delta[n=n']-1[n congruent n' mod K])/N and modulated versions at other outputs. For M>=2, this equals (M/N) times a rank N-K orthogonal projector. The preceding covariance constant was 2M/N; the robust complex radius improves by sqrt(2), with the same tail formula and streaming word bound.

The specified dyadic finite-precision implementation inherits the safe explicit row bound 800 sqrt(NM) log2(N) u ||x||2, with its full certified-root, normalized short-FFT, exact-index and range assumptions. Total/2 and prefix errors are charged deterministically even though they share data. Odd prime-power numerical constants require their own certified short FFT.

Corrections and qualifications:

- At M=1 the projector is zero, so its norm is zero, not M/N.
- M=Theta(log N) via prime powers is not uniform over growing primes. Prime N has no nontrivial admissible M with K>=M.
- Mixed-prime lengths do not satisfy the same projector identity merely because K>=M.
- Constant-time quantization/equality, word arithmetic and root construction are explicit model assumptions; arithmetic-work statements are not bit-work statements.
- The source description of v8 precision as merely conditional is superseded by the master's independent 15:20 full implementation theorem.
- The source's short-FFT contract scales total error by the exact summary norm, which can vanish under cancellation; the independent theorem separates summary perturbation from FFT rounding. The helper constant 64 is uncertified.
- Native summaries are sequential, root/plan setup is omitted from row timings, and the saved R=5,g=4 settings have a vacuous generic simultaneous failure bound. Timings are source-reported; no practical speed superiority or arbitrary-N fixed-precision guarantee is certified.

The error event is for every fixed input with high probability over independent rows and is simultaneous over output coordinates. It is not an exact arbitrary-input identity or an input-uniform operator-norm approximation result.

### Bounded independent v9 extensions

The exact Fourier-basis interaction test supplies a structured-input corollary: for a fixed input with at most h nonzero Fourier coefficients, an output of one row is exactly correct with probability at least 1-2hM/K. Exact-value Boyer–Moore over R=2s-1 independent rows has all-output failure at most N binom(2s-1,s)(2hM/K)^s. This is an exact-arithmetic/equality theorem on a promised sparse-spectrum class. It does not survive arbitrary floating-point equality and does not solve the unrestricted dense-input problem. No sparse-FFT publication novelty is claimed.

The separately packaged composite_extension/ derives a covariance formula for composite N=KM with 2<=M<=K from Ramanujan sums and orthogonal gcd shells. A direct divisor bound and independently checked dyadic triangular-mask proof establish

||Q|| <= [(M-1)/phi(N)] min{D(N,M), 2(1+ceil(log2 M))^2}.

Its more precise bound sums maximum local displacement counts divided by phi(N/g). The proof explicitly handles loss of orthogonality after coordinate masking. The resulting robust approximation theorem requires a suitable block divisor for low work and retains arithmetic/precision qualifications.

Factorization and phi/divisor preprocessing are charged; O(sqrt(N)) trial division in a word model is at most linear in the array length. The sharper M/phi(N) candidate is conjectural. A sweep over 16,723 admissible pairs through N=5000 found no numerical counterexample, and 146 small pairs compare the spectrum with independent exact-rational entry assembly. Neither check proves a global spectral inequality. The weaker displayed bounds have proofs and may be used; the sharp conjecture may not.

## 4. Newly inherited Phase17: additive Green architectures

Phase17 was not in the preceding master and must be audited as new content even though it arrived inside Phase18.

Its additive architecture permits independently ordered, diagonally gauged, invertible banded Green operators. Each summand uses the same permutation on rows and columns. If q is the number of summands and W the sum of half-bandwidths, a common ordered separator gives crossblock rank at most W. Fourier flatness plus unitarity supplies an all-length rank and uniform operator-norm gap.

Independent bounded improvement: the source's own median-bisection argument guarantees m*=ceil(floor(N/2)/2^(q-1)), rather than only floor(N/2^q). Its approximation bound can use m*.

Combining this improved separator with the complex prime-order Fourier full-spark theorem yields N<=2^q W+1. Two tridiagonal summands therefore fail for every prime N>=11, improving the uploaded prime threshold N>=29. The supporting theorem is characteristic zero; small finite fields may behave differently.

This is a term-count restriction on a specified sum. Products of sums, shared-state circuits and more general non-diagonal mixing need separate analysis. A second independently proved bipartite separator does cover distinct row/column permutations within a summand: each stage retains floor(m/2) strictly separated positions from two independently ordered label lists. Starting from all rows and columns gives floor(N/2^q), retaining the original all-length rank and operator-norm bounds. The prime bound becomes N<=2^q(W+1)-1; two tridiagonal terms with independent endpoints are excluded for prime N>=13. The matched-order ceil improvement is not asserted for this larger model. Adversarial interleaving shows tightness for the particular greedy bisection, not universal optimality among all possible separators.

## 5. Phase18: parity and phase-coherence certificates

The Harper/parity degree proof is correct. For N divisible by four, each parity Jacobi block has exactly one zero mode. Fourier has incompatible actions on those lines, excluding a scalar rational function of H. With parity projectors included, the polynomial degrees are exactly N/2 and N/2-2. This does not prohibit other arithmetic circuits.

The sparse joint-intertwiner characterization is also correct: MT=VM and MV=TM imply M=F(aI+bJ), and one e1 calibration selects F. It is a symbolic certification target; checking identities via all basis probes does not itself accelerate a transform.

For fixed outer factors, the diagonal and two-cycle invariants of monomial similarity veto every intermediate diagonal/permutation at once. The independent checker reconstructs all four sampled source instances and their nonzero exact witnesses. Those controls do not exclude all parameter choices. Modular lifts require nonsingular denominators.

The four-phase real spectral factorization is mathematically valid; it supplies no fast real eigenbasis evaluator. It respects the earlier field-descent and pair-unitary limitations when their hypotheses are kept intact.

The Phase16 archive embedded below Phase17 is byte-identical to the previously audited source. Accordingly, the master's adaptive-pivot correction, entropy continuity and ancilla qualifications supersede stale inherited source summaries.

## 6. Coherent next target

The immediate exact algebraic target is the saturated eight-variable/twelve-equation F8 regular chart, with exceptional branches tracked by the complete lift. A candidate solution must be reconstructed into A and B and checked as a full exact matrix identity; a failed finite-field solve does not prove complex infeasibility.

For genuinely noncommuting products, the Phase18 sparse covariance equations provide a clear acceptance test. High crosscut rank alone is insufficient. A successful symbolic factorization must still include root/coefficient preparation, solves, routing, intermediate reuse, output materialization and numerical cost where claimed.

For approximation, the next operational milestone is an implementation matching the certified dyadic contract. The uploaded native benchmark is evidence about one source implementation only.

This audit stops after the stated source accounting, proof reconstruction, exact/numerical controls and bounded improvements. The unrestricted research target remains unresolved.

