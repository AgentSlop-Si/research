# Independent review of the phase-separated table refinement

10 October 2026. **SCOPED PASS at proof level.**

Reviewed source: `research_cycle_1453/packed_improvement/SPLIT_TABLE_CONSTRUCTION.md`.

Frozen SHA-256: `be8de35159ed47f2a5d0bad71937d83bb7053ef83ae6ce358c0dfd80add78ded`.

The refinement is mathematically compatible with the accepted finite-word, all-input relative-l2 dyadic backend and its output-lattice interface. It changes the approximate executor, not merely its representation. All previously accepted source files remain untouched.

## Accepted change and exact accounting

Set `R=2^b`, `S=R^P`. A phase-dependent unary multiplication table on one packed word, followed by a phase-independent Hadamard table on two words, replaces the large direct response table. The table counts are:

- Frozen packed responses: `(Q-1)S^2+dS`.
- New packed responses: `S^2+(Q-1+d)S`.
- Charged scalar helpers: `QR+R^2`.
- New total: `S^2+(Q-1+d)S+QR+R^2`.

The unary table output is a single b-bit code in each lane because the same **total** quantizer is used. This remains true for malformed inputs and unreachable products that clip. The Hadamard helper contains two output codes, so its payload occupies 2b bits; a packed response occupies 2bP bits. No codomain-width growth or hidden unquantized product is used.

The new large-stage execution uses two table reads instead of one and otherwise O(1) ordinary instructions per word pair. Its cold transform-time bound stays `O_c(N(t+log log N))`, with O_c(N) total words. This is not a stronger transform-time asymptotic bound.

## Why the extra rounding fits

Let `delta=u/128`, `beta=sqrt(N)tau`, and `alpha=sqrt(2N)tau`. The intermediate `M=q(CB)` has error from the exact phase product at most

`[u(1+delta)+delta]||B||+beta <= (1+5/512)u||z||+beta`.

Componentwise truncation, underflow, and clipping are all norm nonincreasing. Consequently the subsequent prequantized vector obeys

`||H_hat(A,M)|| <= (1+u/512)(1+delta)||z|| < (1+u/32)||z||`.

Combining the phase error, Hadamard-scale error, and final quantization yields the draft's conservative bound

`||stage(z)-ideal_stage(z)|| <= 3u||z||+2alpha`.

At the worst allowed `u=1/4`, the bracket multiplying u in the draft's derivation is exactly `2118149/1048576 < 3`. The additive term is below 2alpha because `1+u/512 < sqrt(2)`. These are genuine inequalities with room, not empirical numerical estimates.

The J=v+1 recurrence therefore gives relative error at most `22uJ <= (22/1024)2^-t < 2^-t`. Initial quantization is included. The first-clipping argument explicitly covers both the new unary product and the final Hadamard output. Before the first alleged clipping, the preceding stored-vector norm is controlled; the new intermediate quantizer cannot increase that norm. Each candidate prequantized vector is below `2sqrt(2N)<32N`. No clipping-free error bound is applied to a response already known to clip.

Thus the original p, exponent interval, state width, normalization, and output lattice can all be retained. The all-length compiler can use this backend at its existing `T=t+10` precision without further error amplification or a new representation hypothesis.

## Why complete expansion can avoid P work per response

The scalar F and H tables are actually built and paid for. Their exact dyadic arithmetic uses O(v+p) bits, which is a fixed number of the specified growing RAM words. The leading-bit chunk table makes quantization/encoding constant-word work. Polynomial rational coefficient certificates remain separately charged.

For the complete Cartesian expansion, D must be a power of two and the input fields must partition all m log2(D) key bits, as the final lemma now explicitly requires. All applications satisfy these conditions. A base-D odometer changes fewer than `2D^m` digits over all `D^m` keys. Changing one digit replaces a fixed number of fields by masks and shifts, reads its explicit local scalar response, and replaces a fixed number of response fields. The maintained key need not increase numerically. Each key is still visited once, including when one digit occupies two nonadjacent fields. Thus the table is stored at its actual key without a free transpose or scatter.

Initialization costs O(P) per phase pattern or stage, and helper preparation costs `O(QR+R^2)`. Since each packed table already has at least P entries, the initialization is absorbed. Packed expansion costs O(E_pack), not O(P E_pack). This is a generic Cartesian-product fact that could also accelerate other compatible tables; it is not exclusive to phase separation.

## Preparation and model scope

With the unchanged low-b guard and packing choice:

- `S^2 <= 2^(v/8)`
- `QS <= 2^(9v/128+10)`
- `QR <= 2^(3v/128+10)`
- `R^2 <= 2^(v/32)`
- the leading-bit helper costs at most `O(2^(v/8))`
- coefficient certificates cost `Q poly(v+p) <= 2^(v/128+10) poly(v)`

The strict exponential gaps absorb the fixed polynomial and logarithmic factors, uniformly over the low-b domain. Therefore the dyadic backend's unbudgeted preparation work and space are O(N^(1/8)). The literal N-step/N-word wrapper still provides the computable decision rule and the original scalar fallback still handles failed or ineligible instances.

This O(N^(1/8)) claim concerns **backend preparation**. The all-length wrapper retains its own kernel/phase/helper preparation, including `N^(1/4)poly(n+t)` and `2^t(t+1)^2 poly(n+t)`. The refinement does not establish O(N^(1/8)) for all-length total preparation.

The necessary guard thresholds remain unchanged. At t=2 the first eligible exponent remains v=5120. Even there the reduced total table still lies between `2^640` and `2^641` entries. This is a symbolic memory improvement, not a practical feasibility or performance result.

## Fresh independent controls

The independently authored `fresh_split_review_controls.py` imports only Python's standard library and executes no constructor/predecessor program. It passed:

- 6,400 exhaustive toy response entries across phase-dependent unary tables, a separated-half Hadamard layout, and two small-stage pairing layouts;
- 7,257 explicitly charged odometer digit changes, checking the exact change-count formula, unique key writes, and direct per-key agreement;
- exact rational checks of the worst-u local error constants;
- all four displayed threshold entry-count intervals, including scalar helpers;
- an exact real-floating toy witness showing that extra intermediate rounding changes results.

The witness has `a=b=1/2`, phase and scale `3/4`, one-bit mantissas, minimum positive state 1/2, and truncation toward zero. The original one-rounding map returns `(1/2,0)`; the split map returns `(0,0)`. This is not a failure of the theorem's error target. It rules out describing the construction as bitwise equivalent to the frozen executor.

`SPLIT_REVIEW_CONTROLS.json` records the frozen source hash and completed counts. These tests are not a full certified eager executor. Production correctness, useful crossover, measured performance, fixed-hardware complexity, and external priority remain unverified. No novelty conclusion is needed for the accepted refinement.

## Revision reviewed before final acceptance

After the first reading, the constructor narrowed the generic Cartesian lemma to a power-of-two radix and a complete partition of the dense key bits. That statement-only correction prevents a gap between D^m logical tuples and a potentially larger gapped bit-field address space. It does not change any application, table count, error bound, or fresh control. The final lemma text was reread and the source hash was rechecked. The first review/receipt/control record are preserved with a `_v1` suffix; final acceptance applies to the hash at the top of this note.
