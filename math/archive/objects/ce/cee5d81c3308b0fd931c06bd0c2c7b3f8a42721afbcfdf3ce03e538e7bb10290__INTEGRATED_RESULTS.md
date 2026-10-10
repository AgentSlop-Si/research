# Fourier research checkpoint16

9 October 2026 UTC. Independently reviewed mathematical and implementation findings. No project-established general exact sub-N-log-N FFT, and no publication-priority claim.

## The result that changes the construction search

For N=2^k, set m=2^floor(k/2) and q=N/m. Consider L layers, each a sum of weighted cycle inverses using the natural cycle and its bit-reversed conjugate. Allow arbitrary diagonal masks, independent edge/wrap weights, endpoint permutations within each contiguous m-block, and arbitrary additional block-diagonal matrices on those blocks, including any active recursive Fourier bank.

An exact full Fourier factorization requires

    L(q/2 + m) >= N/2.

Proof: select the union I of even-numbered m-blocks. An exact block-DFT/Vandermonde argument proves rank F[I,I-complement]=N/2. The natural cycle has q/2 incoming edges across this cut and its bit-reversed conjugate has m. Complementary inverse-submatrix ranks, then sum/product rank subadditivity, bound each paired layer by q/2+m. Block-diagonal inserted banks contribute zero cross rank.

Thus three such layers fail for every dyadic N>=128; four fail for every dyadic N>=256. In general L must grow as Omega(sqrt N). This is a theorem about these cycle orders and endpoint restrictions, not arbitrary Green products or FFT circuits. It closes the current three-layer root-free natural/bit-reversed full-transform candidate, even though several compressed-path identities remain valid. A literal layer-by-layer executor is distinct from an arbitrary jointly optimized evaluator; no unrestricted runtime lower bound follows.

## What remains positive

- Exact isolated N4 variable-pole synthesis is certified with independent complex interval arithmetic. This is finite-size existence, without a uniform size-lifting algorithm.
- Gauged Green principal blocks close under a precise parameter transformation. Their accumulated correction can have growing rank yet still admit linear-time structured application. Rank growth alone is not an application-time lower bound.
- Hero1 Phase18 has exact full-spectrum recovery for signals whose transformed residual obeys a certified low-degree, sparse-defect cyclic relation, including examples whose individual filter defects are dense but joint defect is sparse. Discovery, rejected candidates, resonant repairs and preprocessing must be charged. It is a restricted-input algorithm.
- The recursive Fourier-mass proposal gives a valid conditional target: a uniform O(N)-cost factorization with one full square-root-scale Fourier bank yields an O(N log log N) arithmetic recurrence; a fixed smaller active fraction can yield O(N). The required global factorization and parameter generator are still unproved.

## Other independently checked boundaries

1. Low-crossing middle permutations collapse four quasiseparable stages into a controlled three-stage family. Both forward and inverse crossing constraints matter. Gray routing passes these particular necessary tests; exact coefficient compatibility remains unsolved. A generic image-dimension deficit does not establish nonmembership of the particular Fourier matrix.
2. A complete fixed-pole N4 elimination excludes the specified poles 1/4 and 1/5 even with independently variable projective couplings. This does not contradict variable-pole finite existence.
3. Routed-grid results include an exact N16 phase-pencil obstruction, an exact minimum-three-term F4 calibration, and a four-native-quadrant exclusion. Each retains its particular routes and phase assumptions.
4. Balanced area routing admits a linear-time construction and stronger support than early routes. Its two-stage state realization is sparse. However, block-diagonal wire transport of both Fourier Weyl generators, and monomial intermediate images in the specified phase-pencil family, are independently excluded. General mixed-wire transport is not excluded by those arguments.
5. Phase31 local rank controls and the v18 additive bank-separation theorem check out in their stated scopes. The v18 prime-length logarithmic branch requirement is for additive independently executed Green terms, not arbitrary products or a general lower bound.
6. Hero17 Phase6 tensor-rank identities and endpoint-gauge support bounds hold. Its tensor cut differs from the same-register operator realignment used elsewhere; their ranks must not be conflated.
7. Hero0 Phase9's dense-controller identity is algebraically valid but unrestricted residual spectra still contain the missing Fourier work. Random syndrome checks are not deterministic exact certificates on every input.

## Corrections and costs retained

For a cyclic filter with shift delta, let g=gcd(N,delta). The short adaptive-family dimension bound d+K applies to the coprime shift case. The reviewed noncoprime bound is min(N,d+K+(g-1)min(d,N/g)); repeated-half vectors provide a counterexample to the unqualified smaller bound.

Inherited Phase17 implementations reject some nonsingular zero-diagonal cases. A repair is included in the independent checks, but this does not imply the uploaded implementation was patched. NTT root planning, omitted arithmetic in source counters, input/output costs, resonance handling and numerical stability remain separately qualified. Finite-field experiments do not establish growing-precision bit bounds or stable complex runtime advantages.

The two newly supplied three-stage bit-reversal archives are byte-identical to the earlier source. Both upload identities are preserved; identical filenames alone were never used to decide equivalence.

## Coverage and continuation

This checkpoint integrates completed post-version15 review payloads and the eight direct uploads from22:57UTC, with their original identities and content hashes. It preserves the previous master and exact source/checker dependencies. Later Phase7, Phase19, Phase32, separation-rank and learned-rational source audits, and newer construction work, are tracked separately rather than silently treated as reviewed here. This is not a refreshed account-wide inventory.

Three construction and three review tracks continue. Next positive candidates must change the cycle geometry or endpoint routing, survive the known cuts, and satisfy the complete Fourier coefficient or Weyl equations with a seed and a uniformly charged parameter-generation rule. Passing a separator test alone is not a factorization.

Complete proofs, original source bytes, independently authored checkers, exact results and portability records are in the full checkpoint. Original uploaded programs were not executed. The compact findings attachment is a summary, not a standalone reproduction package.
