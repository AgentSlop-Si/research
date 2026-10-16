# Independent bounded review of v12 direct-axis layout

Date: 2026-10-16. Scope: inert package inspection, pinned-source comparison, exact rational checks, and reviewer-authored abstract schedule checks. No supplied program was imported or executed. No external write, table promotion, theorem registration, novelty ranking, or full-pipeline acceptance was performed.

## Finding

The local scheduling replacement is mathematically supported, conditional on the inherited arbitrary-gap chunk-swap contract. No counterexample was found in the equal/neighboring-width address formulas, CRT reversal, or Gaussian logical-order argument. Both the supplied epsilon=1/40 certificate and the parent's additional epsilon=1/21 witness satisfy the checked conditional inequalities. This is a local schedule and cost-certificate result, not an independently certified complete sub-n-log-n implementation.

The independent review strengthens the preliminary source check but does not discharge its full-machine, analytic, rank-construction, or novelty obligations.

## Bound inputs and sources

Package: `subnlogn_research_checkpoint_v12_direct_layout_2026-10-16.zip`, 354353 bytes, SHA-256 `6c6eb3a45a0a5059bdff543c91c66ef8de71115cdef4183f27abc79ec1468e13`. The archive hash was recomputed in this review. Selected documents and programs were extracted as inert text into `review_inert/` solely for inspection.

Primary source: `openai/math`, revision `1581d4cbdd69a0faf34b2089614fe2a814316a6a`, under `preprints/Integer-multiplication-below-n-log-n-September-23-2026/build/sections/`. Six fetched source texts are retained in `review_sources/`; `SOURCE_INDEX.json` records exact URLs, Git blob IDs, byte counts and SHA-256 hashes. Each saved file's computed Git blob ID matches the connector's returned ID.

- [03-motifs.tex](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Integer-multiplication-below-n-log-n-September-23-2026/build/sections/03-motifs.tex#L671-L701): rank deficits and exponent certification.
- [04-swap.tex](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Integer-multiplication-below-n-log-n-September-23-2026/build/sections/04-swap.tex#L285-L300), and [its final construction](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Integer-multiplication-below-n-log-n-September-23-2026/build/sections/04-swap.tex#L391-L416): complete arbitrary-gap swap contract and unequal-width correction.
- [05-layers.tex](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Integer-multiplication-below-n-log-n-September-23-2026/build/sections/05-layers.tex#L631-L715): parameterized recurrence and fixed guard constant; also lines 826-919 for the final interface.
- [06-transforms.tex](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Integer-multiplication-below-n-log-n-September-23-2026/build/sections/06-transforms.tex#L174-L225): retained transform-layout interface and cost.
- [07-resampling.tex](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Integer-multiplication-below-n-log-n-September-23-2026/build/sections/07-resampling.tex#L300-L403): padded tensor maps, validity semantics, adjacent schedules and line setup.
- [08-assembly.tex](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Integer-multiplication-below-n-log-n-September-23-2026/build/sections/08-assembly.tex#L295-L308): CRT reversal; lines 63-190 for size/prime generation and lines 824-1003 for final costs and machine boundary.

The [prior intake note](https://github.com/AgentSlop-Si/research/blob/0f3ef16aa4f38ef0c3aee37a296a954dfb7df2d4/math/intake/2026-10-16-v12-direct-layout/PRELIMINARY_SOURCE_CHECK.md) was read as historical scope, not as proof of the claims.

## 1. Arbitrary gap and unequal widths

The source contract is explicitly for a complete Cartesian bit array on [P] x [2^u] x [G] x [2^u] x [B], with arbitrary positive P,G,B. Its O(V u^tau) includes shape processing, padding/unpadding and fixed-tape cleanup. There is no adjacent-only restriction to remove. A fixed-width record payload can be included in the spectator suffix; the bit-volume V must include every payload bit.

The code's `swap_axes`, lines 37-53, uses prefix=product(shape before i), gap=product(intermediate shapes), suffix=product(shape after j). If widths differ, the extra leading bit enters the prefix, giving exactly twice the original prefix range. The two transformations are:

- Longer first: e X M Y -> e Y M X -> Y M e X.
- Longer second: X M e Y -> e X M Y -> e Y M X.

The bit insertion positions in the code are respectively offset+b+middle and offset+a+middle. They agree with these field transformations. The gap's own order is preserved. Static inspection of `binary_chunk_swap` confirms that its gap argument passes through both resize calls and the q-ary swap; `move_digit` preserves the other field order. Their underlying full recursive correctness and cost are inherited, not independently re-proved here.

The v12 implementation rejects axis widths differing by more than one and excludes size-one axes. These restrictions match the eventual assembly, where t_i is r or r/2 and ell>=2. They should not be generalized to arbitrary shapes without further work.

## 2. Reversal and numerical logical order

Mirrored transpositions (i,d-1-i) are disjoint. Thus exactly floor(d/2) direct swaps give the same complete field reversal as the old adjacent reversal, with no changes to the CRT rotations before or after it. This proof does not depend on the payload values or the toy circuit's test inputs.

For Gaussian exposure, the adjacent schedule and the direct schedule use different orders for the *other* coordinates. Both expose exactly the same ordered line for each fixed tuple of those other logical coordinates. The physical-to-logical descriptor makes the validity predicate identical for that tuple. The same logical axis's line map is called, using its original source and target lengths; then the permutation is undone before the next logical axis is processed. The `valid[axis]` update occurs after restoration. Hence the resulting logical array is identical after each axis, by induction.

This argument permits rounded, nonlinear line maps. It does not require operations on different axes to commute. It does require that each line's result be determined by that line, its fixed axis parameters and specified arithmetic, rather than an unmodeled state that changes with the enumeration of independent lines. Inspection of the supplied Gaussian code shows fixed per-axis parameters and deterministic weight generation/cache lookups; counters/cache activity can differ without changing mathematical outputs. Arbitrary user-supplied stateful arithmetic callbacks are outside this equivalence claim.

Each tensor map therefore uses exactly 2(d-1) direct axis calls, instead of d(d-1) adjacent calls. The final physical axis requires none. Holding the full padded target box throughout is essential: shrinking the actual box during compression would invalidate the width argument.

To challenge the argument independently of identity/roundtrip tests, reviewer-authored code compared adjacent versus direct exposure with a nonlinear integer-floor line map, both expansion and compression, all axis orders for six small mixed-width shapes. All 82 comparisons agreed, including validity zeros; a separate witness established that reversing logical axis order actually changes outputs in this model. This is evidence for the conjugation/order argument, not a Gaussian numerical test and not execution of v12.

## 3. Rational certificate and complete displayed parameter conditions

The second checker independently reconstructed the h=100 network counts, obtaining eta_bit=339/22587335000000 and eta_complex=73/19906842167500. It reconstructed the guard quantity B from the complex rank/wire counts and verified m^10<B<m^11, hence nu=11 and C1=20. The guard exponent does not arise from the new schedule or vary with the chosen tau/sigma.

The positive 100-term exponential partial sum at L=13815511/1000000 exceeds 10^6. Therefore L>ln(10^6), and choosing a=eta_bit/L, b=eta_complex/L gives strict valid rank-recurrence exponents tau=1-a and sigma=1-b. The inequality is strict despite equality L*a=eta_bit, because exp(-x)>1-x and ln(m)<L.

With beta=1/2, delta=1/16, lambda=1-a^2, lambda'=1-a^2/2 and c=a(1-2a)/(2(1-a)), the checked conditions include:

- 0<tau,sigma<1 and 0<delta<1/8.
- max(tau,sigma)<lambda<1.
- tau(1+c/beta)<lambda.
- max(lambda,sigma+beta(1-sigma))<lambda'<1.
- Positive rational c, epsilon, kappa; epsilon<1/12; C1*epsilon<1.
- All seven revised margins at least 2*kappa, preserving the transform-layout row p*K^(tau-1).
- epsilon*c<1-epsilon, so K/ell tends to zero; this also follows from the retained positive prefix margin.

For epsilon=1/40, kappa equals the package fraction and is approximately 7.375908518826216e-27. The minimum margin is g2=epsilon*c*a=2*kappa. The old fourth margin is negative, so this parameter point cannot be accepted under the old layout row.

For the parent's separate epsilon=1/21 point, all other parameters unchanged, kappa=11953912917367085649/850851697197626926824852499140022180502001800, approximately 1.4049349559668982e-26. The minimum margin remains g2=2*kappa, and the guard slack is 1-20/21=1/21. The improvement over supplied v12 kappa is exactly 40/21. This is an additional conditional witness, not a replacement certificate or an optimality claim.

An important citation qualification: the *final stated* simultaneous-layer proposition fixes the original tau=sigma=1-2^-50. V12's sharper unequal exponents are supported by reusing the preceding explicitly parameterized recurrence proof, plus the same rank, guard and interface hypotheses. A polished transfer argument should say this explicitly; it should not imply that the proposition as written already quantifies over v12's tau and sigma.

The finite rational checks are not a complete all-size selector. The remaining eventual hypotheses include p>100, d>=2, ell>=2, K<=ell-1, enough reserved work/row axes, polynomial-size descriptors, t_i in {r/2,r}, distinct odd source primes, gcd(s_i,t_i)=1, 2<=alpha<sqrt(p), t_i/s_i-1>p/alpha^4, correct disk-grid/record-width bounds, small accumulated error and a cutoff beyond every condition. The inspected source assembly derives these from its size choices and strict exponent inequalities. For v12, that derivation is inherited and must be carried into the conditional transfer; passing a finite JSON certificate alone does not verify it.

## 4. Cost and machine boundary

The justified local layout replacement is O(V*d*(1+ell^tau)) instead of O(V*d^2*(1+ell^tau)). With V=Tp=Theta(n), p=Theta(log n), d=Theta(p^epsilon), ell=Theta(p^(1-epsilon)), the layout power becomes tau+epsilon*(1-tau), with margin (1-tau)*(1-epsilon).

Fixed sequential workspaces can be reused between calls; the number of direct calls changes, not the number of tapes. Descriptors have polynomial-in-p size/work. The existing per-line setup count O(d*T*poly(p)/r) remains negligible since r exceeds every fixed power of p. These are compositional consequences of the inherited contracts, not independently measured properties of Python's lists or arithmetic.

In particular the Python implementation runs per-entry disk/zero-padding checks, codecs, Python iteration, and arbitrary-precision arithmetic. Their existence and ledgers do not establish a complete finite-alphabet tape-time bound. For example `_check_box` performs numerical disk checks, so an O(dV) statement about pure permutation scans/codecs must not silently be read as an O(dV) bound for every diagnostic operation in `apply`. The paper's proved norm invariants can justify omitting redundant diagnostics in a theoretical machine; a whole implementation proof would need to make that choice and its costs explicit.

The formal target is deterministic fixed-finite-alphabet, fixed-multitape multiplication of two n-bit integers, including leading zeros, with a 2n-bit product and a schoolbook fallback below one fixed cutoff. It is not a unit-cost arbitrary-complex DFT problem. The package's finite explicit-parameter wrapper and no-saving control circuit do not instantiate the enormous rank-saving network or establish the all-size theorem.

The ratio kappa_v12/kappa_v11=1/[40*a*(1-a)] is an exponent-saving ratio, not a runtime ratio. Even the necessary condition K>=2 gives log2(ceil(log2 n))>=1/(epsilon*c): about 7.364143366454844e13 at epsilon=1/40 or 3.866175267388793e13 at epsilon=1/21. Floors can impose a stricter condition. Neither number is a sufficient crossover, practical size estimate, or speed benchmark.

## Evidence and remaining limits

`second_review_checks.py` and `SECOND_REVIEW_RESULTS.json` are newly authored checker/results artifacts. They do not import the supplied modules. The parent's `independent_contract_checks.py` and results were read and assessed, not used as a substitute for this review's derivations. Its 450 symbolic swap cases, 510 reversal shapes and 3076 expose/restore cases are finite symbolic evidence, not independent certification of recursive primitives or all numerical inputs.

The package's reported Gaussian, CRT, product and timing tests remain supplied evidence; none was replayed. No claim is made here about the truth of every imported analytic theorem, compiled rank-saving circuit, uniform construction, exact precision/storage/control contract, full recursive-Fermat run, full pipeline timing, world-first status, or applicability to arbitrary complex DFTs. No table row or global algorithm status should be promoted from this bounded intake alone.
