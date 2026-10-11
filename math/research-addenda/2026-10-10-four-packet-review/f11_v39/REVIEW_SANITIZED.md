# Sanitized publication copy

Original review SHA-256: b8014bd20d64c34ab94b4f441e3e70bedf9ac086eccf37eab82a37b0dbebd152. Private source identifiers are omitted. Mathematical text is otherwise unchanged. Original review-date statements and historical execution/provenance claims below refer to that original review; they are not fresh claims about this publication assembly. Use the addendum README and replay script for the self-contained mathematical replay and its explicit archive/history exclusions.

# Independent bounded review: frozen F11 transfer variety, v39

Review completed 2026-10-10 UTC. The source labels itself 2026-10-11; that label is not the review date.

## Verdict

**Accept the scoped algebraic conclusions after complete fresh, data-only replay.** For this exact fixed 99-edge support, the pullback from all 121 formal transfer coordinates is injective on polynomials of total degree at most four over characteristic zero, and over fields of characteristics 1,000,003 and 1,000,033. The selected 78-coordinate quartic subcertificate has the stronger every-field scope. The specified 77 coordinates form a characteristic-zero transcendence basis of the 77-dimensional transfer-image closure.

No Fourier membership, Fourier impossibility, general FFT speedup, or literature-priority result follows. Existing target-specialized parameter-chart work remains valid and useful within its previously checked scope.

## Sources and exact object binding

- Standalone report: `[private source identifier omitted]`, backing file `[private source identifier omitted]`, `RESEARCH(20261010-233239).md`, 11,964 bytes; SHA-256 `61e946e4435f03218618372e0392a3a20eeccb8b8a9586caef2f2767cbf33cc1`.
- ZIP: `[private source identifier omitted]`, backing file `[private source identifier omitted]`, `fft_transfer_quartic_circuit_v39.zip`, 11,477,245 bytes; SHA-256 `1425fc7321cda9bd47ce17384e2c5e3c4c762b5077bc2014dabd708133b2f5b5`.
- The report is byte-identical to ZIP `RESEARCH.md`. ZIP CRC checks and all 24 entries of its manifest pass. `source_pins.json` records every outer member's SHA-256.
- The ordered `topology_11.json` is byte-identical to both the original `research_cycle_1734/pole_escape/topology_11.json` and the v38 review input. SHA-256: `4ea6269199f843363e90d3c63c2a0f12df220bbbc4b9b9a9a1ba59fd79a76a9b`.
- The nested `PRIOR_v38_COMPLETE.zip` SHA-256 is `9e55fd16931b5f084532719f3836309b1092932fd920f5469a74b2279aa6c5bb`, exactly the accepted v38 source pin in `research_cycle_2237/f11_v38_review/`. Its ZIP CRC, all 19 manifest entries, and contained topology were also checked.

Edges are ordered exactly as in the original: A IDs 0–32, B 33–65, C 66–98; each layer contains 33 distinct `(destination, source)` pairs and has indegree/outdegree three. Coordinates are `11*output+input`; H=CBA. Fresh sparse propagation reconstructs 297 paths, with counts 22×1, 42×2, 39×3, 16×4, and 2×5 across all 121 entries. No isomorphism or unverified relabeling is substituted for byte identity. `topology_edges.txt` agrees with that ordered JSON.

## Exhaustive global quartic replay

No uploaded or inherited research program was executed or imported. Fresh review code consumes inert JSON, text, and NPZ arrays. The official Library materialization helper was used only to retain source-file identity metadata.

The Python preparation independently reconstructs every transfer sample in two ways: sparse propagation of input basis vectors through the three layers, and sums over reconstructed paths. It trial-divides both moduli to verify primality. It reproduces all 2,904 evaluated entries for each prime and their stipulated sample fingerprints:

| Prime | Seed and generator | Transfer-sample FNV64 |
|---|---|---|
| 1,000,003 | 20261011, 64-bit xorshift | 6774884542161267937 |
| 1,000,033 | 972524161, 64-bit LCG | 11690676381034439803 |

The fresh C++ rank checker enumerates every sorted quartet of coordinate IDs `0<=a<=b<=c<=d<121`, exactly `binom(124,4)=9,381,251` columns. It places each quartet into its sorted four-row/four-column margins. This enumeration is different from the packet programs' pairing/permutation enumeration; every formal quartic monomial is generated once before partitioning.

There are `binom(14,4)=1,001` possible row margins and 1,001 column margins, giving 1,002,001 nonempty blocks. The complete independently counted distribution is:

| Columns per block | Blocks |
|---:|---:|
| 1 | 21,901 |
| 2 | 24,200 |
| 3 | 111,925 |
| 4 | 127,050 |
| 6 | 36,300 |
| 7 | 245,025 |
| 12 | 326,700 |
| 24 | 108,900 |

The weighted sum is 9,381,251. The maximum is 24. Both complete exact modular rank replays pass:

- Modulo 1,000,003: 1,002,001 blocks all full rank. Exactly one first-square evaluation matrix is singular: row margin `(0,0,5,6)`, column margin `(3,4,5,8)`, 12 columns, first 12 rows rank 11, all 24 rows rank 12. A separate Python column-span calculation confirms both ranks.
- Modulo 1,000,033: 1,002,001 blocks all full rank, with no singular first-square matrix.
- Degenerate control using repeated copies of the first sample: exactly 18,810 deficient blocks among all 20,020 blocks in the first 20 row margins. This reproduces the claimed detector rejection.

These are complete fresh replays, not source-only assertions, random subsamples of blocks, or floating-point rank estimates. Rank-phase timings were approximately 6.56 and 6.21 seconds; those timings exclude compilation, preparation, and partition construction and are not arithmetic complexity claims.

## Why this proves the stated field scope

The first-layer variables carry their input-column degrees, and third-layer variables carry their output-row degrees; middle-layer variables have zero such degrees. Thus H_ij has bidegree `(e_i,e_j)`. Different margin blocks have disjoint edge-monomial support, so dependencies split by blocks. Repeated row/column labels do not create an omission: direct enumeration already counts each quartic monomial once, and any block has at most 4! distinct pairings.

For a block, its exact evaluation matrix is a linear image of its integer edge-monomial coefficient matrix after reduction modulo p. Full evaluation rank therefore forces full coefficient-column rank modulo p. A maximal coefficient minor is nonzero modulo p, hence is a nonzero integer. Consequently the same columns are independent over Q and every characteristic-zero field, including C. The verified ranks also prove independence over F_p and all its field extensions for each of the two certificate primes.

One successful prime would suffice for characteristic zero. Two successful primes do **not** establish the global quartic statement in every characteristic. No universal determinant-unit certificate was supplied or inferred for all 121 quartic coordinates.

For lower degrees, multiply a hypothetical nonzero homogeneous relation in the *formal source coordinate ring* K[h] by a coordinate power to reach degree four. That product is nonzero because K[h] is a domain, contradicting quartic injectivity. Mixed coordinate degrees cannot cancel after pullback because H is homogeneous of edge degree three. The inherited v38 full-coordinate degree-at-most-three theorem retains its separately verified every-field scope.

## Selected78 unit certificate and named77 basis

The selected coordinates are independently reconstructed as the 78 entries of smallest path count, breaking ties by row-major ID. They match the JSON exactly. NPZ loading disables pickle; expected arrays, dimensions, dtypes, and digest are checked.

All 1,663,740 quartic columns were expanded, accounting for every 21,770,715 path-quartet contribution and independently sorting/counting 19,337,020 distinct edge monomials. Every saved pivot is a valid distinct degree-12 edge monomial with four edges from each layer. Every pivot has coefficient exactly one in its own column. All 32,223 occurrences in other columns occur in strictly earlier elimination rounds; none occur in the same or a later round. The complete round counts are 1,634,924; 28,756; 60. The reconstructed little-endian round/high/low digest is `e02dc2043da82e12005acfb95d5660fa483c508c394f78f6cdd950031c3f386d`.

Ordering columns by these rounds gives a unit-triangular coefficient minor, with determinant ±1. This proves quartic independence for the selected78 over every field, hence no selected-coordinate relation of degree at most four over every field. For finite fields this means formal polynomial equality in K[a], not equality merely as functions on the finite point set K^99.

At the stored 99 nonzero weights, a fresh derivative calculation verifies the named77-by77 minor determinant 556,448 modulo 1,000,003, full Jacobian rank 77, and 22 independent gauge tangent vectors annihilated by the Jacobian. The nonzero minor lifts to characteristic zero. The free action of the 22-dimensional internal-vertex gauge torus on the dense nonzero-edge domain gives image dimension at most 99−22=77; the Jacobian gives equality. Thus the named77 outputs are algebraically independent and form a transcendence basis. Adding the 78th gives a dependent set, whose first possible relation has degree at least five.

The saved modular tangent nullvector is checked, including support 76. This is a sampled tangent diagnostic, not proof that its 76-element support is a characteristic-zero algebraic-matroid circuit. No such circuit claim is accepted.

## Boundaries and effect on existing work

The conclusion excludes only nonzero polynomials P in the **formal transfer coordinates** of total degree at most four that vanish identically under the generic substitution h=H(a). It does not exclude parameter equations imposed by a particular target, equations involving both h and a, localized/rational equations with guards, or target-specialized eliminants.

In particular, the existing F11 E25/E41 equations and resultant chains impose target equality in parameter coordinates and are not generic low-degree H-only identities. Their existing accepted chart guards, saturation conditions, and specialization scope continue to govern them. The v39 theorem neither contradicts those eliminations nor justifies stopping useful target-feasibility work. No new chart fusion or target-specialized elimination was attempted in this review.

A polynomial separating F11 from this image closure, if one exists, must have transfer degree at least five. This does not show that a quintic exists, that F11 lies outside the closure, that F11 is attained, or that a point in the closure lies in the image. Fourier membership and nonexistence remain unresolved here. Codimension 44 does not establish 44 ideal generators or a complete intersection.

The hypothetical fresh-input ledger of 99 scalar products and 66 additions describes evaluating this one supported three-layer map with supplied weights. No Fourier weights, uniform all-length family, cost of finding weights, or asymptotic speedup is established. The source's external literature discussion and separate preprint were not independently researched; no novelty claim is accepted.

## Reproducibility and status

`run_fresh_review.py` compiles and runs only the fresh review C++ files and invokes only the fresh review Python checkers. Inputs are the actual inert source files, accepted original topology, and accepted v38 review data. `independent_replay_results.json`, execution logs, `source_pins.json`, and `RECEIPT.json` delimit what was checked and pin the deliverables. Every principal mathematical certificate claimed above was replayed completely; the producer's own program execution history and claimed clean-run procedure remain source-only historical claims.

The Incoming queue row is a proposal only. No repository, sheet, Library, or other external write was performed by this review.
