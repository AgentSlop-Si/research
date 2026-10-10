Public source-text preservation. This is the source author’s research statement, not the corrected review. Read [the accepted support audit](../../reviews/01_schur_support.md) for the controlling field, edge-depth, cost and generic-weight qualifications. The source text below is unchanged. Source-reported numerical results are not independent checks; source programs and predecessor archives are not included. Preservation and hashing do not certify every sentence or establish priority. Historical source wording about an open exact target concerns the source project; it is not a current literature-wide claim. The source’s broader claim that rank or connectivity methods are exhausted is narrowed in the audit to total-nonsingularity or connectivity alone.

# Chain checkpoint — superconcentrator interface gate v31

## Inherited state

- v28: arbitrary non-covariant low-treewidth Schur extensions are impossible; high-treewidth exact linear-time solves exist.
- v29: a common-order opposite-DAG sum needs `Omega(N^(3/2))` explicit denominator edges.
- v30: a same-branch Fourier Schur block needs interface dimension `floor(N/2)`, sharply; small-rank routing is impossible.
- Exact arbitrary-input cyclic sub-`N log N` FFT remains open.

## New rank/flow theorem

For any weighted linear DAG transfer `T_G` and equal-size terminal subsets `I,O`,

`rank T_G[O,I] <= maximum number of vertex-disjoint I-to-O paths`.

Hence a totally nonsingular transfer circuit has superconcentrator support.

## v30 Schur consequence

The v30 triangular baseline vanishes on a `m x m` rectangle with `m=floor(N/2)`, while the prime Fourier target has full rank on every square subblock. Therefore the complete interface-correction circuit on that rectangle must be an `m`-superconcentrator.

## Depth gates

- Depth 2: tight size `Theta(m log^2 m / log log m)`, asymptotically worse than `N log N`.
- Depth 3: tight size `Theta(m log log m)`; rules out linear work but leaves a genuine sub-`N log N` window.
- Logarithmic depth: linear-size superconcentrators exist, so connectivity alone cannot rule out `O(N)`.

## Positive control

By the Lindstrom--Gessel--Viennot identity, independent generic edge weights on any superconcentrator give a totally nonsingular path-sum matrix. Combined with linear-size superconcentrators, this proves that full-spark transforms can have `O(N)` exact nonuniform linear circuits.

Thus future obstructions must use Fourier phase compatibility, not only minors, separators, treewidth or expansion.

## Verification

- 10 automated test groups pass.
- Exhaustive depth-two `q=n` minima: 6 edges at `n=2`, 11 edges at `n=3`.
- Benes networks at `n=4,8` pass all 69 / 12,869 terminal-subset path tests.
- First deterministic finite-field weight assignments at both sizes are totally nonsingular (69 / 12,869 minors).
- Prime Fourier half-rectangles have full rank in all checked cases.
- Independent verifier passes.
- v30 predecessor ZIP is embedded and hash-checked.

## Do not repeat

- a one-middle-layer sparse Schur interface as a sub-`N log N` candidate;
- an `O(N)` constant-depth interface justified only by expansion;
- claiming total nonsingularity itself forces `N log N` work;
- treating generic full-spark superconcentrator weights as Fourier-compatible weights.

## Exact next target

Either construct a depth-three `Theta(N log log N)` superconcentrator with exact Fourier phase weights, or prove a cyclotomic/path-family incompatibility theorem. The rank/connectivity gate is now exhausted.
