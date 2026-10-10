# Fixed-pair convolution kernels and Phase 7 source audit

Date: 2026-10-08 UTC. Source inspected: `fft_phase7_persistent_convolution(2).zip`, especially `persistent_chain.py`, `RESEARCH.md`, and `benchmark.py`.

## Main result

The submitted one-factor update identity is correct. A useful next implementation target is a **fixed editable pair** with four maintained convolution kernels. It handles sparse changes to both factors in `O(N(1+s_a+s_b))` ring operations per persistent fork, including array-copy/output costs, after explicitly charged preparation. The bilinear cross term is included through the update order. This is a consequence of ordinary bilinearity, not a new general FFT or integer-multiplication theorem. No production implementation or performance improvement is claimed by the attached exact test.

## 1. Four-kernel invariant

All vectors have the same circular period `N`; `*` means circular convolution. Two factors `a,b` may change. The product `R` of every other factor is fixed. Maintain:

```
R = product of the fixed factors (e_0 if there are none)
U = b * R
V = a * R
Y = a * b * R
```

For sparse additive changes `d_a,d_b`, update in this order:

```
Y_after_a = Y + d_a * U
V_after_a = V + d_a * R
Y_after_b = Y_after_a + d_b * V_after_a
U_after_b = U + d_b * R
```

The new state is `(R,U_after_b,V_after_a,Y_after_b)`. Expanding only the last output verifies

```
Y_after_b = Y + d_a*U + d_b*V + d_a*d_b*R.
```

The use of **updated** `V_after_a` is essential. At `N=4`, take `a=b=e_0`, `R=e_0`, and `d_a=d_b=e_1`. The correct result is `[1,2,1,0]`; omitting the cross term returns `[1,2,0,0]`.

Each sparse convolution is a sum of circular shifts. Two such convolutions are required per factor change, so the arithmetic scales with `N(s_a+s_b)`, rather than explicitly enumerating `s_a*s_b` cross pairs. Materializing or preserving forked output/kernel arrays contributes `O(N)` additional work.

### Shift and gain extension

Let `T_s` denote a circular shift. For changes

```
a' = g_a T_sa(a) + d_a
b' = g_b T_sb(b) + d_b,
```

use

```
Y_after_a = g_a T_sa(Y) + d_a*U
V_after_a = g_a T_sa(V) + d_a*R
Y_after_b = g_b T_sb(Y_after_a) + d_b*V_after_a
U_after_b = g_b T_sb(U) + d_b*R.
```

There is no division, so zero gains and zero Fourier coefficients are safe algebraically. The sparse residuals are in current signal coordinates. A persistent implementation must allocate changed arrays or use safe copy-on-write, preserving all parent states and avoiding in-place aliasing between the two updates.

## 2. Preparation, memory, and amortization

With the package's real-FFT approach, preparing all `m` seed spectra costs `O(mN log N)`. Given those spectra, form the fixed complement spectrum without division in `O(mN)`, then form the spectra of `R,U,V,Y` and apply up to four inverse FFTs in `O(N log N)`. Previously prepared arrays can be reused, but their preparation cannot disappear from an end-to-end comparison.

The four kernel arrays occupy `4N` scalars, about `32N` bytes with float64, in addition to seed arrays/spectra, factor descriptions, metadata, temporary arrays, and retained versions. `R` can be shared by all descendants while the fixed factors stay unchanged. A fork changing both factors generally needs up to `3N` new maintained kernel scalars, so retaining `L` such full states costs `Theta(LN)` additional space. A mutable stream can release obsolete arrays.

For `L` versions with `s_a,s_b` sparse changes each, a representative cost is

```
preparation + O(L N(1+s_a+s_b)),
```

plus input/edit acquisition and bookkeeping. This is useful only when the editable pair remains fixed or complement preparation is sufficiently reused. Arbitrarily selecting new pairs can require new complement work and cache space; the fixed-pair bound does not cover that workload for free. A dispatcher should compare setup plus expected future reuse against a full FFT route, and charge cache misses/eviction.

This bound is for dense kernel/output maintenance. It is not automatically an `O(Q(s_a+s_b))` bound for only `Q` requested **time coefficients**. If the updated complement must be evaluated only at positions induced by the other delta, cross-pair dependencies reappear. With immutable baseline kernels, the direct selected-time formula costs `O(Q(1+s_a+s_b+s_a*s_b))`; maintaining a whole updated kernel costs `O(Ns_a)` instead. Choose between these costs. Selected **frequency bins** are different: the four-kernel invariant is pointwise there, so fixed-bin caches can be updated without time-domain support expansion.

## 3. More than two editable factors

For `t` editable factors, distributing `(b_i+d_i)` gives up to `2^t` subset terms. The two-factor result does not eliminate this general dependency.

One exact maintained-kernel generalization stores `K_S`, the convolution of all factors except editable positions in subset `S`, for every `S` in the editable set. For an additive change to position `j`:

```
K_S' = K_S + d_j * K_(S union {j})    if j is not in S
K_S' = K_S                           if j is in S.
```

The source kernel in each update excludes `j`, so it remains unchanged during this edit. There are `2^(t-1)` affected kernels per edited factor, `O(2^t N)` kernel storage, and `O(2^(t-1) N(1+s_j))` work per such edit. For `t=2` this is precisely the four-kernel construction. This is a reasonable small-`t` specialization, not an efficient unrestricted-`t` replacement for a factored spectral product.

Another simple optimization: when all modified factors have only gain/shift changes and no sparse residual, combine their gains and shifts into one global gain and shift of the cached base convolution. The current Phase 7 dispatcher unnecessarily uses its native spectral route once more than one factor is marked modified. A similar reduction works when only one factor has a sparse residual and the remaining changes are gains/shifts; form products of the other gains directly, without dividing by potentially zero gains.

## 4. Reproducible exact check

Run `python verify_fixed_pair_kernels.py` with standard Python. No NumPy, SciPy, uploaded source, package installation, or executable from the archive is required.

The completed run used Python 3.12.14 and passed:

- 720 independent fork cases at circular periods 1 through 12;
- 3,600 accumulating two-factor stream steps;
- 3,600 sibling-fork checks;
- comparison with direct integer circular convolution and with the explicit cross-term formula;
- negative and zero gains, circular shifts, zero factors, support collisions, an empty fixed-factor complement, and immutable parent checks.

All arithmetic is Python integer arithmetic. These are finite exact correctness checks, not a performance benchmark, exhaustive proof, or validation of floating-point numerical stability. The derivation above supplies the algebraic proof. Full results are in `verification_results.json`.

## 5. Source-level cost corrections

Line references are to the uploaded `persistent_chain.py`.

1. **Warm single-modified-factor frequency queries still hash all seed IDs.** `_fixed_product_bin` (296–304) uses a cache key containing the length-`m` `seed_ids` tuple. `_cache_bin` (276–288) repeatedly probes dictionaries with that key. On the tested CPython runtime, tuple hashes are recomputed by visiting each item, so a hot cache lookup costs `Theta(m)` just to hash this tuple. Consequently, the source's specialized hot `Q`-bin path includes `Theta(Qm)` hashing, in addition to `O(Qk+log m)` algebra/access, rather than the advertised implementation-level `O(Qk+log m)`. Use an interned baseline object with a constant-size stable identity, preserved across same-seed forks. CPython's primary source explicitly shows the uncached loop: [tupleobject.c, Python 3.12](https://raw.githubusercontent.com/python/cpython/3.12/Objects/tupleobject.c). An independent check hashed a key containing 128 instrumented items seven times and observed 896 item-hash calls.

2. **Node allocation and end-to-end update time are different claims.** Rewriting one balanced-tree path creates `O(log m)` graph nodes (250–256), but `with_factor` line 391 checks seed membership in a list, costing up to `O(S)` for `S` registered seeds. Initial `chain` checks each input against that list (239–241), which can cost `O(mS)`. A seed-owner token or identity-checked ID-indexed lookup removes this scan. The residual edit tuple is copied and sorted (84–90), costing up to `O(k log k)`; modified-index frozenset unions (397) copy their contents. None of this disproves structural sharing, but allocation bounds must not be presented as the runtime bound of the whole edit operation.

3. **Concatenation does not preserve balance.** `chain` builds a balanced tree, but `convolve_with` (410–415) simply joins two roots. Repeatedly appending one factor creates height `Theta(m)`, not `O(log m)`. Factor access and rewriting are recursive (250–264), so the log-depth promise needs a balanced join implementation or a restriction to the initial balanced tree. The same concern applies to recursive cached-bin traversal. This is a source-derived issue; separate execution results may provide a reproduced recursion failure.

4. **Warm-root and warm-subtree caches are distinct.** An unmodified call to `frequencies` uses `_fixed_product_bin` (421–422), not `_bin_value`, while a multiple-modified-factor call uses `_bin_value` (440–441). Therefore warming an unmodified root does not itself warm the subtree-node caches used by the general factored route. The theoretical update-path reuse bound needs the relevant node/bin entries actually present and not evicted.

5. **Memory figures are not complete process memory.** `memory_report` (364–373) counts raw seed/base/complement arrays and counts bin entries/nodes. It does not report Python object/key overhead, residual tuples, modified sets, retained version metadata, or peak temporary arrays. Treat its byte counters as partial array accounting; profile retained-version and peak process memory separately.

## 6. Correct claims, limits, and comparison design

- The submitted single-factor formula is exact over a commutative coefficient ring. Its `Theta(N)` full-output claim for a constant number of edits is appropriately conditional on preparation and is output-optimal in a scalar-output model. It does not accelerate arbitrary fresh input acquisition/transforms.
- When multiple factors change, the factored Fourier product includes all cross terms automatically, without symbolic expansion. The current `spectral_half` implementation pays `O(N(m+K))` work for pending residuals plus one `O(N log N)` inverse FFT. Its base-factor phase arrays and repeated exponentials are an obvious implementation target, rather than an algebraic breakthrough.
- The shipped benchmark's principal wins compare against a prepared-kernel FFT route, not a hand-specialized incremental update. The negative specialized-frequency comparison is useful and honestly disclosed. A fixed-pair follow-up should include both a hand-written four-kernel baseline and a full FFT route, with preparation, cold/hot cases, stream/fork retention, and output/copy costs matched.
- The full-output benchmark computes every output but checks only three positions per version in its principal case (`benchmark.py` 40 and 55). Separate regression tests may cover full arrays; any statement that the benchmark itself verified every coefficient should be narrowed.
- The package executes float64/complex128 operations. Algebraic exactness and the separate modular audit do not make its outputs bit-exact. Long products and repeated updates can overflow, underflow, or accumulate cancellation error. Periodic rebuilds and adversarial stability checks need measurement. The fixed-pair integer script does not establish the stability of a floating-point implementation.
- Integer-operation counts are not bit complexity. Exact integer coefficients grow, and an NTT/CRT realization would need coefficient bounds, enough primes, compatible transform lengths, and reconstruction costs. No improved general integer-multiplication exponent follows.
- Related established incremental Fourier work includes the authors' [eFFT implementation and publications](https://github.com/raultapia/efft). That is a relevant comparison target, not evidence of a head-to-head result here. Query-specific transform choices also have established precedents; [FFTW's pruned FFT discussion](https://www.fftw.org/pruned.html) emphasizes both workload and numerical tradeoffs. No novelty claim has been established by this audit.

## Recommended next implementation order

1. Replace large tuple cache keys and linear ownership scans; make the claimed warm-query/update costs measurable.
2. Preserve balanced joins or explicitly constrain the API's balance promise.
3. Collapse pure gain/shift changes before selecting a dense algorithm.
4. Prototype the fixed-editable-pair kernel path with a measured setup/reuse threshold and explicit persistent-memory accounting.
5. Add matched end-to-end baselines and stability/retained-version workloads before claiming a practical speedup.
